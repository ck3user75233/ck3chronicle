// All Trekker access is through the public CLI, under one canonical lock.
import * as fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import { randomUUID } from 'node:crypto';

const STORE = String.raw`C:\Users\nateb\Documents\ck3chronicle\.ck3chronicle\wip\tooling\work-state`;
const TOOLCHAIN = path.join(STORE, 'toolchain');
const LOCK = path.join(STORE, '.access-lock');
const PENDING = path.join(STORE, 'incomplete-operation.json');
const DB = path.join(STORE, '.trekker', 'trekker.db');
const BUN = path.join(TOOLCHAIN, 'node_modules', 'bun', 'bin', 'bun.exe');
const CLI = path.join(TOOLCHAIN, 'node_modules', '@obsfx', 'trekker', 'bin', 'trekker.js');
const PINS = { '@obsfx/trekker': '1.11.0', '@toon-format/toon': '2.1.0', bun: '1.3.10',
  commander: '13.1.0', dayjs: '1.11.19', 'drizzle-orm': '0.38.4' };
const STATUSES = ['todo', 'in_progress', 'completed', 'wont_fix', 'archived'];
const TERMINAL = new Set(['completed', 'wont_fix', 'archived']);
const HANDOFF = ['handoff:pending', 'handoff:changes', 'handoff:received'];
const HELP = `Protected Trekker pilot (JSON output). Always invoke this absolute helper.
  pilot.mjs help
  pilot.mjs versions | init | task-list | epic-list
  pilot.mjs team-state TEAM
  pilot.mjs task-show ID | epic-show ID | comments ID | dependencies ID
  pilot.mjs history [ID]
  pilot.mjs task-create REQUEST.json | epic-create REQUEST.json
  pilot.mjs task-update ID REQUEST.json | epic-update ID REQUEST.json
  pilot.mjs comment ID REQUEST.json | checkpoint ID REQUEST.json
  pilot.mjs delivery ID REQUEST.json | receipt ID REQUEST.json
  pilot.mjs dependency-add ID PREREQUISITE_ID
See docs/TREKKER_CLI_PILOT_HANDOFF.md for request fields and recovery.
No raw CLI, SQL, delete, wipe, config, subtask or cascade-complete operation.
Store: ${STORE}`;

function requireThat(condition, message) { if (!condition) throw new Error(message); }
function object(value, label) {
  requireThat(value && typeof value === 'object' && !Array.isArray(value), `${label}: expected object`);
  return value;
}
function text(value, label) {
  requireThat(typeof value === 'string' && value.trim() && !value.includes('\0'), `${label}: nonempty text required`);
  return value;
}
function id(value) {
  requireThat(typeof value === 'string' && /^[A-Z][A-Z0-9]*-[1-9][0-9]*$/.test(value), 'Expected a native Trekker ID');
  return value;
}
function team(value) {
  requireThat(typeof value === 'string' && /^[a-z][a-z0-9-]*$/.test(value), 'Expected a team slug');
  return value;
}
function readJson(file) { return JSON.parse(fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '')); }
function durableJson(file, value, exclusive = false) {
  const fd = fs.openSync(file, exclusive ? 'wx' : 'w');
  try { fs.writeFileSync(fd, JSON.stringify(value, null, 2) + '\n'); fs.fsyncSync(fd); }
  finally { fs.closeSync(fd); }
}
function fields(request, allowed) {
  object(request, 'request');
  for (const key of Object.keys(request)) requireThat(allowed.includes(key), `Unsupported field: ${key}`);
}
function tags(value) {
  requireThat(value === null || typeof value === 'string', 'Incomplete read: tags missing or invalid');
  return (value || '').split(',').map(x => x.trim()).filter(Boolean);
}
function tagInput(value, label) {
  requireThat(Array.isArray(value), `${label}: expected an array`);
  return value.map(x => {
    text(x, label);
    requireThat(x === x.trim() && !/[,\r\n]/.test(x), `${label}: invalid tag`);
    return x;
  });
}
function ownership(values) {
  requireThat(values.filter(x => x.startsWith('team:')).length === 1, 'Exactly one team: tag is required');
  for (const prefix of ['team:', 'producer:', 'receiver:']) {
    const matches = values.filter(x => x.startsWith(prefix));
    requireThat(matches.length <= 1, `Conflicting ${prefix} tags`);
    for (const match of matches) team(match.slice(prefix.length));
  }
  requireThat(values.filter(x => x.startsWith('producer:')).length === values.filter(x => x.startsWith('receiver:')).length,
    'Meaningful deliveries need both producer: and receiver: tags');
  requireThat(values.filter(x => x.startsWith('handoff:')).every(x => HANDOFF.includes(x)), 'Unknown handoff tag');
  requireThat(values.filter(x => HANDOFF.includes(x)).length <= 1, 'Conflicting handoff tags');
}
function record(value, kind, expected) {
  object(value, kind);
  id(value.id);
  if (expected) requireThat(value.id === expected, 'Incomplete read: unexpected record ID');
  text(value.title, 'record title');
  requireThat(STATUSES.includes(value.status), 'Incomplete read: unknown status');
  requireThat(Number.isInteger(value.priority) && value.priority >= 0 && value.priority <= 5, 'Incomplete read: priority');
  requireThat(value.description === null || typeof value.description === 'string', 'Incomplete read: description');
  if (kind === 'task') {
    tags(value.tags);
    requireThat(value.parentTaskId === null, 'Only top-level tasks are supported');
  }
  return value;
}

let decode;
let uncertainChild = false;
let mutation = null;
function runtime() {
  requireThat(process.platform === 'win32', 'This canonical pilot is configured for Windows');
  for (const [name, version] of Object.entries(PINS)) {
    const actual = readJson(path.join(TOOLCHAIN, 'node_modules', name, 'package.json'));
    requireThat(actual.version === version, `Required ${name}@${version}, found ${actual.version}`);
  }
  requireThat(fs.existsSync(CLI) && fs.existsSync(BUN), 'Pinned CLI or Bun executable is missing');
  const result = spawnSync(BUN, ['--version'], { encoding: 'utf8', shell: false, windowsHide: true });
  requireThat(!result.error && result.status === 0 && result.stdout.trim() === PINS.bun, 'Bun version check failed');
  return { store: STORE, bunExecutable: BUN, cliEntry: CLI, node: process.version, dependencies: PINS };
}
function cli(args, writes = false) {
  if (writes) {
    if (!mutation) {
      requireThat(!fs.existsSync(PENDING), 'An incomplete operation requires inspection before further writes');
      mutation = { token: randomUUID(), operation: process.argv.slice(2), startedAt: new Date().toISOString(),
        completedSteps: [], attempting: args };
      durableJson(PENDING, mutation, true);
    } else {
      mutation.attempting = args;
      durableJson(PENDING, mutation);
    }
  }
  // The package bin detects Bun and loads its CLI; no shell/shim/PATH lookup.
  const result = spawnSync(BUN, [CLI, '--toon', ...args], {
    cwd: STORE, encoding: 'utf8', shell: false, windowsHide: true,
    maxBuffer: 16 * 1024 * 1024,
  });
  if (result.error || result.signal) uncertainChild = true;
  requireThat(!result.error && result.status === 0 && !result.signal,
    `CLI ${args.slice(0, 2).join(' ')} failed: ${result.error?.message || result.stderr || result.signal || result.status}. ` +
    (mutation ? 'A write may have committed; inspect before retrying.' : 'Read is incomplete.'));
  requireThat(!result.stderr.trim(), `Unexpected CLI stderr; outcome requires inspection: ${result.stderr}`);
  requireThat(result.stdout.trim(), 'Incomplete CLI output');
  const value = decode(result.stdout, { strict: true });
  requireThat(value !== undefined && value !== null && value.success !== false, 'Invalid or unsuccessful CLI result');
  if (writes) {
    mutation.completedSteps.push({ args, result: value });
    mutation.attempting = null;
    durableJson(PENDING, mutation);
  }
  return value;
}
function pages(args, key = 'items') {
  const items = [], seen = new Set();
  let total;
  for (let page = 1; ; page++) {
    const result = object(cli([...args, '--limit', '50', '--page', String(page)]), 'page');
    requireThat(Number.isInteger(result.total) && result.total >= 0 && result.page === page && result.limit === 50 &&
      Array.isArray(result[key]), 'Incomplete pagination metadata');
    if (total === undefined) total = result.total;
    requireThat(total === result.total && result[key].length === Math.min(50, total - items.length),
      'Incomplete or changing paginated result');
    for (const item of result[key]) {
      object(item, 'page item');
      requireThat(item.id !== undefined && !seen.has(item.id), 'Repeated/missing ID in paginated result');
      seen.add(item.id);
      items.push(item);
    }
    if (items.length === total) return items;
  }
}
function tasks() { return pages(['task', 'list']).map(x => record(x, 'task')); }
function show(taskId, kind = 'task') { return record(cli([kind, 'show', id(taskId)]), kind, taskId); }
function comments(taskId) {
  return pages(['comment', 'list', id(taskId)]).map(c => {
    id(c.id); text(c.content, 'comment content'); text(c.author, 'comment author');
    requireThat(c.taskId === taskId, 'Incomplete comment read: task ID mismatch');
    return c;
  });
}
function dependencies(taskId) {
  const result = object(cli(['dep', 'list', id(taskId)]), 'dependencies');
  requireThat(result.taskId === taskId && Array.isArray(result.dependsOn) && Array.isArray(result.blocks),
    'Incomplete dependencies');
  for (const edge of [...result.dependsOn, ...result.blocks]) { id(edge.taskId); id(edge.dependsOnId); }
  requireThat(result.dependsOn.every(x => x.taskId === taskId) && result.blocks.every(x => x.dependsOnId === taskId),
    'Dependency direction mismatch');
  return { ...result, prerequisites: result.dependsOn.map(x => show(x.dependsOnId)),
    dependents: result.blocks.map(x => show(x.taskId)) };
}
function append(taskId, author, content) {
  show(taskId); // Re-read before every mutation, including the second delivery step.
  const result = cli(['comment', 'add', id(taskId), `--author=${author}`, `--content=${content}`], true);
  requireThat(result.taskId === taskId && result.content === content && result.author === author, 'Comment output mismatch');
  requireThat(comments(taskId).some(c => c.id === result.id && c.content === content && c.author === author),
    'Comment read-back failed; do not retry blindly');
  return result;
}
function checkPatch(request, kind, creating) {
  fields(request, ['title', 'description', 'priority', 'status', ...(kind === 'task' ?
    [creating ? 'tags' : 'addTags', ...(creating ? [] : ['removeTags']), 'epic'] : [])]);
  if (creating || request.title !== undefined) text(request.title, 'title');
  if (creating || request.description !== undefined) text(request.description, 'description with governing links');
  if (request.status !== undefined) requireThat(STATUSES.includes(request.status) &&
    !(kind === 'epic' && request.status === 'wont_fix'), 'Invalid status');
  if (request.priority !== undefined) requireThat(Number.isInteger(request.priority) && request.priority >= 0 && request.priority <= 5, 'Invalid priority');
  if (request.epic !== undefined && request.epic !== null) id(request.epic);
  for (const key of ['tags', 'addTags', 'removeTags']) if (request[key] !== undefined) tagInput(request[key], key);
  if (!creating) requireThat(Object.keys(request).length > 0, 'Empty update');
}
function writeRecord(kind, taskId, request) {
  const creating = !taskId;
  checkPatch(request, kind, creating);
  const before = creating ? null : show(taskId, kind);
  const expected = { ...request };
  if (kind === 'task') {
    const values = creating ? tagInput(request.tags, 'tags') : tags(before.tags);
    const remove = request.removeTags || [];
    const next = [...new Set([...values.filter(x => !remove.includes(x)), ...(request.addTags || [])])];
    ownership(next);
    // Preserve unrelated tags byte-for-byte when the request does not edit tags.
    expected.tags = creating || request.addTags || request.removeTags ? next.join(',') : before.tags;
    delete expected.addTags; delete expected.removeTags;
    if (request.epic) show(request.epic, 'epic');
  }
  if (kind === 'epic' && TERMINAL.has(request.status)) {
    const children = tasks().filter(x => x.epicId === taskId);
    requireThat(children.every(x => TERMINAL.has(x.status) && !tags(x.tags).some(t => ['handoff:pending', 'handoff:changes'].includes(t))),
      'Epic still contains unresolved work or receipts');
  }
  const args = [kind, creating ? 'create' : 'update', ...(creating ? [] : [taskId])];
  for (const key of ['title', 'description', 'priority', 'status', 'tags', 'epic']) {
    if (expected[key] === undefined || (key === 'tags' && !creating && !request.addTags && !request.removeTags)) continue;
    if (key === 'epic' && expected[key] === null) args.push('--no-epic');
    else args.push(`--${key}=${expected[key] ?? ''}`);
  }
  const result = record(cli(args, true), kind, taskId);
  const after = show(result.id, kind);
  for (const key of ['title', 'description', 'priority', 'status', 'tags']) {
    const desired = expected[key] !== undefined ? expected[key] : before?.[key];
    if (desired !== undefined) requireThat(after[key] === desired, `Write read-back mismatch: ${key}`);
  }
  if (kind === 'task') requireThat(after.epicId === (request.epic !== undefined ? request.epic : before?.epicId ?? null), 'Epic read-back mismatch');
  return after;
}
function checkpoint(taskId, request) {
  fields(request, ['author', 'completed', 'stoppingPoint', 'nextAction', 'evidenceLimits', 'artifacts', 'ownerDecisions']);
  const sections = ['completed', 'stoppingPoint', 'nextAction', 'evidenceLimits', 'artifacts', 'ownerDecisions'];
  const content = '[checkpoint]\n' + sections.map(key => `${key}: ${text(request[key], key)}`).join('\n');
  return append(taskId, text(request.author, 'author'), content);
}
function handoff(taskId, request, receiving) {
  fields(request, ['author', 'evidence', 'limits', 'nextAction', ...(receiving ? ['outcome'] : [])]);
  for (const key of ['author', 'evidence', 'limits', 'nextAction']) text(request[key], key);
  if (receiving) requireThat(['received', 'changes'].includes(request.outcome), 'Receipt outcome must be received or changes');
  const before = show(taskId), values = tags(before.tags);
  ownership(values);
  requireThat(values.some(x => x.startsWith('producer:')) && values.some(x => x.startsWith('receiver:')), 'Delivery requires producer and receiver tags');
  requireThat(!TERMINAL.has(before.status), 'Reopen a prematurely closed delivery explicitly before recording handoff');
  if (receiving) requireThat(values.some(x => ['handoff:pending', 'handoff:changes'].includes(x)), 'Receipt requires an outstanding delivery');
  const state = receiving ? request.outcome : 'pending';
  const note = append(taskId, request.author,
    `[${receiving ? 'receipt' : 'delivery'}:${state}]\nevidence: ${request.evidence}\nlimits: ${request.limits}\nnextAction: ${request.nextAction}`);
  const after = writeRecord('task', taskId, { removeTags: HANDOFF, addTags: [`handoff:${state}`] });
  return { comment: note, task: after, closure: 'Status unchanged; separately disclose follow-ups before closing.' };
}
function warnings(task, notes) {
  const result = [], values = tags(task.tags), handoffs = values.filter(x => x.startsWith('handoff:'));
  try { ownership(values); } catch (error) { result.push(error.message); }
  if (!notes.some(c => c.content.startsWith('[checkpoint]\n'))) result.push('No continuation checkpoint recorded');
  if (TERMINAL.has(task.status) && values.some(x => ['handoff:pending', 'handoff:changes'].includes(x))) result.push('Closed status contradicts unresolved receipt');
  if (handoffs.length && !values.some(x => x.startsWith('receiver:'))) result.push('Handoff has no receiver');
  if (values.some(x => x.startsWith('receiver:')) && TERMINAL.has(task.status) && !values.includes('handoff:received')) result.push('Closed delivery lacks recorded receipt; inspect explicit disposition');
  const latest = notes.find(c => /^\[(delivery|receipt):/.test(c.content));
  const expected = latest?.content.match(/^\[(?:delivery|receipt):(pending|changes|received)\]/)?.[1];
  if (expected && !values.includes(`handoff:${expected}`)) result.push('Latest delivery/receipt comment contradicts tags; possibly interrupted update');
  return result;
}
function teamState(name) {
  team(name);
  const inventory = tasks(), active = [], incoming = [], outgoing = [], contradictions = [];
  const related = inventory.filter(t => tags(t.tags).some(x => [`team:${name}`, `producer:${name}`, `receiver:${name}`].includes(x)));
  for (const task of related) {
    const values = tags(task.tags), notes = comments(task.id), issues = warnings(task, notes);
    const deps = dependencies(task.id);
    const item = { task, governingLinksAndDescription: task.description, comments: notes,
      latestContinuation: notes.find(c => c.content.startsWith('[checkpoint]\n')) || null,
      latestRecordedAction: notes[0] || null, dependencies: deps,
      blockers: deps.prerequisites.filter(x => !TERMINAL.has(x.status) || tags(x.tags).some(t => ['handoff:pending', 'handoff:changes'].includes(t))), warnings: issues };
    if (values.includes(`team:${name}`) && !TERMINAL.has(task.status)) active.push(item);
    if (values.includes(`receiver:${name}`) && values.includes('handoff:pending')) incoming.push(item);
    if (values.includes(`producer:${name}`) && values.some(x => ['handoff:pending', 'handoff:changes'].includes(x))) outgoing.push(item);
    if (issues.some(x => !x.startsWith('No continuation'))) contradictions.push({ id: task.id, warnings: issues });
  }
  return { team: name, totalTasksRead: inventory.length, active, incoming, outgoing, contradictions,
    note: 'Prepared work is todo. Read recorded next action and owner assignment; readiness never dispatches work.' };
}

function parseInvocation() {
  const [operation, ...args] = process.argv.slice(2);
  const arities = { versions: [0], init: [0], 'task-list': [0], 'epic-list': [0], 'team-state': [1],
    'task-show': [1], 'epic-show': [1], comments: [1], dependencies: [1], history: [0, 1],
    'task-create': [1], 'epic-create': [1], 'task-update': [2], 'epic-update': [2],
    comment: [2], checkpoint: [2], delivery: [2], receipt: [2], 'dependency-add': [2] };
  requireThat(arities[operation]?.includes(args.length), HELP);
  return { operation, args };
}
function dispatch(operation, args, versions) {
  const [first, second] = args;
  switch (operation) {
    case 'versions': return versions;
    case 'init': {
      requireThat(!fs.existsSync(path.join(STORE, '.trekker')), 'State directory already exists; inspect, do not reinitialize');
      const result = cli(['init'], true);
      requireThat(result.success === true, 'Initialization did not report success');
      return { initialization: result, tasks: tasks(), epics: pages(['epic', 'list']) };
    }
    case 'task-list': return tasks();
    case 'epic-list': return pages(['epic', 'list']).map(x => record(x, 'epic'));
    case 'task-show': return { task: show(first), comments: comments(first), dependencies: dependencies(first) };
    case 'epic-show': return { epic: show(first, 'epic'), tasks: tasks().filter(x => x.epicId === first) };
    case 'comments': show(first); return comments(first);
    case 'dependencies': show(first); return dependencies(first);
    case 'history': return pages(['history', ...(first ? ['--entity', id(first)] : [])], 'events');
    case 'team-state': return teamState(first);
    case 'task-create': return writeRecord('task', null, readJson(first));
    case 'epic-create': return writeRecord('epic', null, readJson(first));
    case 'task-update': return writeRecord('task', id(first), readJson(second));
    case 'epic-update': return writeRecord('epic', id(first), readJson(second));
    case 'comment': {
      const request = readJson(second); fields(request, ['author', 'content']);
      return append(id(first), text(request.author, 'author'), text(request.content, 'content'));
    }
    case 'checkpoint': return checkpoint(id(first), readJson(second));
    case 'delivery': return handoff(id(first), readJson(second), false);
    case 'receipt': return handoff(id(first), readJson(second), true);
    case 'dependency-add': {
      show(first); show(second);
      const before = dependencies(first);
      if (before.dependsOn.some(x => x.dependsOnId === second)) return { alreadyPresent: true, ...before };
      cli(['dep', 'add', id(first), id(second)], true);
      const after = dependencies(first);
      requireThat(after.dependsOn.some(x => x.dependsOnId === second), 'Dependency read-back failed');
      return after;
    }
  }
}

let ownsLock = false;
try {
  if (process.argv.length === 2 || (process.argv.length === 3 && process.argv[2] === 'help')) {
    console.log(HELP);
  } else {
    const { operation, args } = parseInvocation();
    requireThat(fs.existsSync(path.join(STORE, 'RETAIN-WORK-STATE.txt')), 'Canonical store is not prepared; run install.ps1 first');
    try { fs.mkdirSync(LOCK); ownsLock = true; }
    catch (error) {
      if (error.code === 'EEXIST') throw new Error(`Protected route busy or recovery required: ${LOCK}. Never expire a lock by age.`);
      throw error;
    }
    durableJson(path.join(LOCK, 'owner.json'), { pid: process.pid, host: os.hostname(),
      startedAt: new Date().toISOString(), operation, executable: process.execPath }, true);
    const versions = runtime();
    const require = createRequire(path.join(TOOLCHAIN, 'package.json'));
    ({ decode } = await import(pathToFileURL(require.resolve('@toon-format/toon')).href));
    requireThat(typeof decode === 'function', 'Pinned TOON decoder unavailable');
    if (!['versions', 'init'].includes(operation)) requireThat(fs.existsSync(DB), 'Pilot is not initialized; no implicit/per-worktree initialization');
    const recovery = fs.existsSync(PENDING) ? readJson(PENDING) : null;
    const result = dispatch(operation, args, versions);
    // Publish the successful result before clearing the recovery marker.
    await new Promise((resolve, reject) => process.stdout.write(JSON.stringify({ ok: true, store: STORE,
      recoveryRequired: recovery, result }, null, 2) + '\n', error => error ? reject(error) : resolve()));
    if (mutation) fs.unlinkSync(PENDING);
  }
} catch (error) {
  console.error(JSON.stringify({ ok: false, error: error.message, store: STORE,
    incompleteOperation: fs.existsSync(PENDING) ? PENDING : null, lockRetained: uncertainChild }));
  process.exitCode = 1;
} finally {
  if (ownsLock && !uncertainChild) {
    // A killed helper cannot reach here, so its lock remains for manual recovery.
    try { fs.unlinkSync(path.join(LOCK, 'owner.json')); fs.rmdirSync(LOCK); }
    catch (error) { console.error(`Lock cleanup incomplete: ${error.message}`); process.exitCode = 1; }
  }
}
