/** Inspect exported reports in an isolated local Chromium browser.
 * No web server, network connection, production browser profile or database use.
 * Node built-ins only; Chromium's DevTools pipe drives real navigation/clicks.
 */
import {spawn} from 'node:child_process';
import {mkdir, readFile, writeFile} from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {setTimeout as delay} from 'node:timers/promises';
import assert from 'node:assert/strict';

const [browser, bundleArg, outputArg, mode] = process.argv.slice(2);
if (!browser || !bundleArg || !outputArg) {
  throw new Error('Usage: node tools/check_reporting_browser.mjs BROWSER_EXE REVIEW_BUNDLE OUTPUT_DIRECTORY');
}
const bundle = path.resolve(bundleArg), output = path.resolve(outputArg);
await mkdir(output, {recursive: true});
const child = spawn(browser, ['--headless', '--no-sandbox', '--disable-gpu',
  '--no-first-run', '--no-default-browser-check', '--disable-background-networking',
  '--disable-extensions', '--remote-debugging-pipe', '--user-data-dir=' + path.join(output, 'profile')],
  {stdio: ['ignore', 'pipe', 'pipe', 'pipe', 'pipe'], windowsHide: true});
let next = 0, buffer = '', stderr = '', sessionId;
const pending = new Map();
child.stderr.on('data', chunk => { stderr += chunk; });
child.stdio[4].on('data', chunk => {
  buffer += chunk;
  let end;
  while ((end = buffer.indexOf('\0')) >= 0) {
    const message = JSON.parse(buffer.slice(0, end));
    buffer = buffer.slice(end + 1);
    if (pending.has(message.id)) {
      const {resolve, reject, timer} = pending.get(message.id);
      clearTimeout(timer);
      pending.delete(message.id);
      if (message.error) reject(new Error(JSON.stringify(message.error)));
      else resolve(message.result);
    }
  }
});
function command(method, params = {}, session = sessionId) {
  const id = ++next;
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      pending.delete(id);
      reject(new Error('DevTools timeout: ' + method));
    }, 20000);
    pending.set(id, {resolve, reject, timer});
    child.stdio[3].write(JSON.stringify({id, method, params, ...(session ? {sessionId: session} : {})}) + '\0');
  });
}
async function evaluate(expression) {
  const value = await command('Runtime.evaluate', {expression, returnByValue: true, awaitPromise: true});
  if (value.exceptionDetails) throw new Error(JSON.stringify(value.exceptionDetails));
  return value.result.value;
}
async function waitFor(expression) {
  for (let attempt = 0; attempt < 80; attempt++) {
    if (await evaluate(expression)) return;
    await delay(100);
  }
  throw new Error('Page condition did not become true: ' + expression);
}
async function navigate(file, fragment = '') {
  const url = pathToFileURL(path.join(bundle, file)).href + fragment;
  const result = await command('Page.navigate', {url});
  assert(!result.errorText, result.errorText);
  await waitFor(`location.href === ${JSON.stringify(url)} && document.readyState === 'complete'`);
  await delay(250);
}
async function screenshot(name) {
  await delay(100);
  const result = await command('Page.captureScreenshot', {format: 'png'});
  await writeFile(path.join(output, name + '.png'), Buffer.from(result.data, 'base64'));
  screenshots++;
}
async function click(selector) {
  const point = await evaluate(`(() => {
    const a = document.querySelector(${JSON.stringify(selector)});
    if (!a) throw new Error('Missing link');
    for (let p = a.parentElement; p; p = p.parentElement) if (p.tagName === 'DETAILS') p.open = true;
    a.scrollIntoView({block:'center'});
    const r = a.getClientRects()[0];
    return {x:r.x + Math.min(r.width / 2, 30), y:r.y + r.height / 2, href:a.href};
  })()`);
  await command('Input.dispatchMouseEvent', {type: 'mousePressed', x: point.x, y: point.y, button: 'left', clickCount: 1});
  await command('Input.dispatchMouseEvent', {type: 'mouseReleased', x: point.x, y: point.y, button: 'left', clickCount: 1});
  await waitFor(`location.href === ${JSON.stringify(point.href)} && document.readyState === 'complete'`);
  await delay(250);
  return point.href;
}
const checks = [];
let screenshots = 0;
let outcome;
try {
  const version = await command('Browser.getVersion');
  const {targetId} = await command('Target.createTarget', {url: 'about:blank'});
  ({sessionId} = await command('Target.attachToTarget', {targetId, flatten: true}));
  await command('Page.enable');
  await command('Runtime.enable');
  await command('Emulation.setDeviceMetricsOverride', {width: 1440, height: 1100, deviceScaleFactor: 1, mobile: false});
  await navigate('examples.html');
  await screenshot('index');
  await click('a[href="outcomes.html"]');
  const delivery = JSON.parse(await readFile(path.resolve('examples/reporting/delivery-status.json'), 'utf8'));
  const deliveryText = await evaluate('document.body.innerText');
  assert(!deliveryText.includes('Duplicate usable timestamps and selected duplicate-Run rejection'));
  for (const row of [...delivery.completed, ...delivery.unverified]) {
    assert(deliveryText.includes(row.item), 'Delivery status item missing: ' + row.item);
    assert(deliveryText.includes(row.outcome || row.available), 'Delivery status explanation missing: ' + row.item);
    if (row.needed) assert(deliveryText.includes(row.needed), 'Completion condition missing: ' + row.item);
  }
  for (const row of delivery.earlier_assessment) {
    assert(deliveryText.includes(row.id), 'Earlier review ID missing: ' + row.id);
    assert(deliveryText.includes(row.status), 'Earlier review status missing: ' + row.id);
    assert(deliveryText.includes(row.outcome), 'Earlier review disposition missing: ' + row.id);
  }
  for (const row of delivery.query_outcomes) {
    assert(deliveryText.includes(row.case), 'Named query case missing: ' + row.case);
    assert(deliveryText.includes(row.disposition), 'Query disposition missing: ' + row.case);
  }
  await screenshot('delivery-completed');
  await click('a[href="#unverified"]');
  await screenshot('delivery-unverified');
  await click('a[href="investigations/new-contradiction.html#explanation"]');
  assert((await evaluate('document.getElementById("explanation").innerText')).includes('zero'), 'Empty-result explanation missing');
  await click('a[href="../outcomes.html"]');
  assert((await evaluate('location.href')).endsWith('/outcomes.html'));
  checks.push({name:'delivery-status', earlier_items_present:true, gaps_and_needed_evidence_present:true, direct_example_and_return:true});
  if (mode === '--delivery-status-only') {
    await navigate('investigations/relative-path-all-members.html', '#explanation');
    await click('a[href="../outcomes.html#query-outcomes"]');
    assert(await evaluate('(() => { const r=document.getElementById("query-outcomes").getBoundingClientRect(); return r.top>=0 && r.top<innerHeight; })()'));
    const queryTable = await evaluate('document.getElementById("query-outcomes").nextElementSibling.nextElementSibling.innerText');
    assert(queryTable.includes('Work status'));
    assert(queryTable.includes('1 diagnostic(s), 32 occurrence(s).'));
    assert(queryTable.includes('0 diagnostic(s), 0 occurrence(s).'));
    assert(queryTable.includes('input_validation'));
    await screenshot('earlier-query-outcomes');
    await click('#outcome-symbol-needs-selector a');
    assert((await evaluate('document.getElementById("explanation").innerText')).includes('before any database request'));
    await click('a[href="../outcomes.html"]');
    await click('a[href="#earlier-assessment"]');
    await screenshot('earlier-assessment');
    checks.push({name:'earlier-review-reconciliation', original_items:delivery.earlier_assessment.length,
      named_query_outcomes:delivery.query_outcomes.length, remaining_groups:delivery.unverified.length,
      direct_link_from_current_report:true, query_result_and_return:true});
  }
  if (mode !== '--delivery-status-only') {
  const reportNames = mode === '--message-search-only' ? ['message-unrecognized', 'message-context-switch', 'history-positions', 'stored-data-io'] :
    mode === '--source-labels-only' ? ['relative-path-all-members', 'unresolved-genuine-paths', 'resolution-content-independent'] :
    mode === '--relative-path-only' ? ['relative-path-all-members', 'relative-path-other-directory'] :
    mode === '--no-path-only' ? ['pathless-emission', 'pathless-archive', 'mixed-archive-source-context'] :
    mode === '--recursion-only' ? ['recursion-scoped-report'] :
    mode === '--resolution-only' ? ['unresolved-genuine-paths', 'synthetic-unresolved-paths', 'resolved-paths',
    'unresolved-excludes-existing-and-pathless', 'resolution-content-independent', 'unresolved-archive-unknown', 'archive-path-without-playset'] :
    mode === '--path-filter-only' ? ['file-path-all', 'required-partial', 'path-excludes-unlocated', 'path-only-unlocated',
    'synthetic-required-missing-files', 'synthetic-find-missing-files', 'synthetic-unmentioned-file',
    'synthetic-directory', 'synthetic-absolute-file', 'synthetic-member-missing-files', 'archive-path-without-playset'] :
    mode === '--followup-only' ? ['worked-five-runs', 'five-predecessors', 'five-successors', 'both-sides-history',
    'synthetic-missing-files', 'synthetic-missing-hotspots', 'synthetic-find-missing-files', 'synthetic-required-missing-files', 'synthetic-stored-missing-reference',
    'syntax-archive-equals', 'syntax-archive-brace', 'syntax-archive-localization', 'syntax-archive-substitutions', 'syntax-archive-statement', 'archive-required-playset'] :
    ['template-only', 'worked-full', 'hotspots', 'previously-observed', 'new', 'syntax',
    'new-contradiction', 'hotspots-contradiction', 'symbol-needs-selector', 'no-eligible', 'required-partial', 'dlc-path', 'syntax-window'];
  for (const name of reportNames) {
    const data = JSON.parse(await readFile(path.join(bundle, 'investigations', name + '.json'), 'utf8'));
    await navigate('examples.html');
    await click(`a[href="investigations/${name}.html#explanation"]`);
    const state = await evaluate(`(() => {
      const explanation = document.getElementById('explanation');
      const r = explanation.getBoundingClientRect();
      return {url:location.href, top:r.top, height:innerHeight, overflow:document.documentElement.scrollWidth > innerWidth,
        text:explanation.innerText, evidence:explanation.querySelector('#explanation-evidence').innerText,
        scripts:document.scripts.length,
        remote:performance.getEntriesByType('resource').filter(r => /^https?:/.test(r.name)).map(r=>r.name)};
    })()`);
    assert(state.top >= 0 && state.top < state.height, name + ': explanation anchor is outside viewport');
    assert(!state.overflow, name + ': page overflows viewport');
    assert.equal(state.scripts, 0);
    assert.deepEqual(state.remote, []);
    assert(state.text.includes(data.explanation.question), name + ': question missing from integrated explanation');
    for (const expected of data.explanation.expected) assert(state.text.includes(expected), name + ': expected behavior missing');
    for (const result of data.explanation.result) assert(state.text.includes(result), name + ': actual result text missing');
    assert(state.evidence.length > 0, name + ': supporting evidence missing');
    if (name === 'required-partial') {
      assert.equal(data.status, 'completed');
      assert(state.evidence.includes('sea_minority_on_actions.txt'));
      assert(!state.evidence.includes("Data error in loc string 'duke_male_holder_irish'"));
      assert(!state.text.includes('Cannot evaluate the mod/file filter'));
    }
    if (name === 'template-only') {
      assert(state.evidence.includes('<KEY> trigger [ <REASON> ]'));
      assert(state.evidence.includes('All matches by Run'));
    }
    if (name.startsWith('message-')) {
      assert(state.evidence.includes('Where the search matched'));
      assert(state.evidence.includes('Assigned template'));
      assert(state.evidence.includes(name === 'message-unrecognized' ? 'Template literal text' : '<REASON> slot'));
      const table = await evaluate('document.getElementById("message-matches").textContent');
      for (const row of data.rollups.message_matches.buckets) {
        assert(table.includes(String(row.distinct_records)));
        for (const ref of row.templates) assert(table.includes(ref.template_id));
      }
      await click('a[href="#D1"]');
      const detail = await evaluate('document.getElementById("D1").innerText');
      const message = await evaluate('document.querySelector("#D1 pre.message").textContent');
      assert.equal(message, data.records[0].message.replace(/\r\n?/g, '\n'));
      assert(detail.includes('Stored location'));
      await screenshot(name + '-match-location');
      await navigate('investigations/' + name + '.html', '#explanation');
    }
    if (name === 'history-positions') {
      for (let offset = -5; offset <= 5; offset++) {
        assert(state.evidence.includes(offset === 0 ? 'Run 0 (selected)' : 'Run ' + (offset > 0 ? '+' : '') + offset));
      }
      assert.equal(data.window.positions.filter(p => !p.available).length, 4);
      assert(state.evidence.includes('Not available'));
      assert.equal(data.coverage.comparison_errors.length, 0);
      assert.equal(data.coverage.comparison_unavailable.length, 0);
    }
    if (name === 'stored-data-io') {
      await click('a[href$="/io-verification.json"]');
      const receipt = JSON.parse(await evaluate('document.body.innerText'));
      assert.equal(receipt.traced_processes, 2);
      assert.deepEqual(receipt.raw_log_or_model_artifact_accesses, []);
      await navigate('investigations/' + name + '.html', '#explanation');
    }
    if (name.startsWith('synthetic-')) assert(state.text.includes('Synthetic verification fixture'));
    if (['synthetic-missing-files', 'synthetic-unresolved-paths', 'unresolved-genuine-paths'].includes(name)) {
      assert(state.evidence.includes('File not found'));
    }
    if (name === 'resolved-paths' || name === 'resolution-content-independent') assert(state.evidence.includes('Resolved'));
    if (name.startsWith('pathless-')) {
      assert(state.evidence.includes('Source lookup: not applicable.'));
      assert(!state.text.includes('Incomplete source coverage'));
    }
    if (name.startsWith('syntax-archive-')) assert(state.text.includes('Recorded playset is unavailable.'));
    if (name === 'relative-path-all-members') {
      assert(state.text.includes('optional leading slash'));
      for (const candidate of data.records[0].candidates) assert(state.evidence.includes(candidate.member.name));
      assert.deepEqual(data.records[0].candidates.map(c => c.member.load_order), [114, 115]);
      const rows = await evaluate(`(() => {
        const table = [...document.querySelectorAll('#explanation-evidence table')].find(t => t.tHead.innerText.includes('Error source'));
        return {headers: [...table.tHead.rows[0].cells].map(c => c.innerText),
          rows: [...table.tBodies[0].rows].map(r => [...r.cells].map(c => c.innerText))};
      })()`);
      assert.deepEqual(rows.headers, ['Load order', 'Mod name', 'File path', 'Line', 'Error source']);
      assert.equal(rows.rows[0][0], '114');
      assert.equal(rows.rows[0][4], '—');
      assert.equal(rows.rows[1][0], '115');
      assert.equal(rows.rows[1][4], 'Yes');
      assert(!state.evidence.includes('Current file candidate'));
      assert(!state.evidence.includes('recorded load order'));
      assert.equal(data.records[0].file_line_sources[0].error_source.member.load_order, 115);
    }
    await screenshot(name + '-explanation');
    if (name === 'recursion-scoped-report') {
      await click('a[href="#source-coverage"]');
      const countsText = await evaluate('document.getElementById("source-coverage").innerText');
      assert(countsText.includes('Files checked (names/paths)'));
      assert(countsText.includes('Folders checked'));
      await screenshot('recursion-counts');
      await click('a[href$="/recursion-verification.html"]');
      const receiptText = await evaluate('document.body.innerText');
      assert(receiptText.includes('scope/count comparisons passed'));
      assert(receiptText.includes('whole root, recursive, cold'));
      assert(receiptText.includes('root only, cold'));
      await screenshot('recursion-independent-comparison');
      await navigate('investigations/' + name + '.html', '#explanation');
    }
    await click(`a[href="../examples.html#case-${name}"]`);
    const returnVisible = await evaluate(`(() => { const r=document.getElementById('case-${name}').getBoundingClientRect(); return r.top>=0 && r.top<innerHeight; })()`);
    assert(returnVisible, name + ': return anchor outside viewport');
    checks.push({name, status: data.status, explanation_visible: true, question_expected_result_and_evidence_together: true,
      return_visible: true, offline: true});
    console.log('Browser route passed:', name);
  }
  if (!['--followup-only', '--path-filter-only', '--resolution-only', '--recursion-only', '--no-path-only', '--relative-path-only', '--source-labels-only', '--message-search-only'].includes(mode)) {
  for (const [name, file, anchor] of [
    ['template-pattern', 'template-only', '#T1'], ['template-diagnostic', 'template-only', '#D2'],
    ['worked-runs', 'worked-full', '#window'], ['dlc-diagnostic', 'dlc-path', '#D1'],
    ['matching-diagnostic', 'required-partial', '#D1'],
    ['worked-diagnostic', 'worked-full', '#D1']]) {
    await navigate('investigations/' + file + '.html', '#explanation');
    await click(`#explanation-evidence a[href="${anchor}"]`);
    assert(await evaluate(`(() => {const r=document.querySelector(${JSON.stringify(anchor)}).getBoundingClientRect(); return r.top>=0 && r.top<innerHeight;})()`), name + ': evidence target outside viewport');
    await screenshot(name);
    checks.push({name, direct_click_from_explanation: true, target_visible: true});
  }
  await navigate('investigations/worked-full.html', '#explanation');
  const appendix = await click('#explanation-evidence a[href^="worked-full-sources.html#"]');
  assert(appendix.includes('-sources.html#'));
  const source = await evaluate(`(() => { const e=document.getElementById(location.hash.slice(1)); return {text:e.innerText, marked:e.querySelectorAll('mark').length}; })()`);
  assert(source.marked > 0, 'Referenced source line must be marked');
  await screenshot('source-excerpt');
  await click('section:target a');
  assert((await evaluate('location.href')).includes('worked-full.html#'));
  checks.push({name: 'verbose-appendix', direct_reference_from_explanation: true, marked_line: true, return_link: true});
  } else if (mode !== '--message-search-only') {
    await navigate('investigations/synthetic-missing-files.html', '#explanation');
    await click('a[href$="/error.log"]');
    const fixtureText = await evaluate('document.body.innerText');
    assert.equal((fixtureText.match(/Script system error!/g) || []).length, 2);
    assert(fixtureText.includes('__08b_nonexistent_'));
    await screenshot('synthetic-input');
    checks.push({name:'fixture-input-link', two_emissions:true, fake_paths_visible:true});
  }
  }
  await command('Emulation.setDeviceMetricsOverride', {width: 390, height: 844, deviceScaleFactor: 1, mobile: false});
  const narrowPages = mode === '--message-search-only' ? [['narrow-search', 'investigations/message-unrecognized.html', '#message-matches'],
    ['narrow-slot-match', 'investigations/message-context-switch.html', '#D1']] :
    mode === '--delivery-status-only' ? [['narrow-delivery', 'outcomes.html', '#unverified']] : [['narrow-index', 'examples.html', ''],
    ['narrow-explanation', 'investigations/template-only.html', '#explanation'],
    ['narrow-diagnostic', 'investigations/template-only.html', '#D2']];
  for (const [name, file, fragment] of narrowPages) {
    await navigate(file, fragment);
    assert(await evaluate('document.documentElement.scrollWidth <= innerWidth'), name + ': page overflow');
    await screenshot(name);
  }
  outcome = {status: 'passed', browser: version.product, checks, screenshots,
    note: 'Automated real-browser navigation/layout checks. Inspect the PNGs separately for visual quality.'};
} catch (error) {
  outcome = {status: 'failed', checks, error: String(error.stack || error)};
  process.exitCode = 1;
} finally {
  await writeFile(path.join(output, 'browser-verification.json'), JSON.stringify(outcome, null, 2));
  await writeFile(path.join(output, 'browser.stderr.txt'), stderr);
  const exited = new Promise(resolve => child.once('exit', resolve));
  await command('Browser.close', {}, null).catch(() => {});
  await Promise.race([exited, delay(2000)]);
  if (child.exitCode === null && child.signalCode === null) child.kill();
  await Promise.race([exited, delay(2000)]);
  // Only this tool's spawned browser and pipes are owned here. A Windows Chrome
  // shutdown can acknowledge Browser.close while leaving its child pipe open.
  for (const stream of child.stdio) stream?.destroy();
  child.unref();
  console.log(JSON.stringify(outcome, null, 2));
}
