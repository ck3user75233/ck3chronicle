import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { decode, encode } from '../../.ck3chronicle/wip/tooling/work-state/toolchain/node_modules/@toon-format/toon/dist/index.mjs';
import { decodeTrekkerOutput } from '../../tools/work_state/toon_output.mjs';

// Offline reproduction from genuine saved records; never invokes the tracker.
const fixture = JSON.parse(readFileSync(new URL('./fixtures/cmt-132.json', import.meta.url), 'utf8').replace(/^\uFEFF/, ''));

test('pinned decoder reproduces the committed CMT-132 response failure', () => {
  assert.throws(() => decode(encode(fixture.comment), { strict: true }),
    /Expected 10 inline array items, but got 18/);
});

test('adapter preserves the exact comment response, including punctuation', () => {
  assert.deepStrictEqual(decodeTrekkerOutput(encode(fixture.comment), decode), fixture.comment);
});

test('adapter preserves genuine comment-list table values', () => {
  assert.deepStrictEqual(decodeTrekkerOutput(encode(fixture.comments), decode), fixture.comments);
});

test('adapter preserves nested native history snapshots', () => {
  assert.deepStrictEqual(decodeTrekkerOutput(encode(fixture.history), decode), fixture.history);
});
