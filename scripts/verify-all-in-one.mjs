import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
export async function verifyAllInOne(root) {
  const directory=join(root,'all-in-one');
  const json=async file=>JSON.parse(await readFile(join(directory,file),'utf8'));
  const sha=async file=>createHash('sha256').update(await readFile(join(directory,file))).digest('hex');
  const manifest=await json('all-in-one-package-manifest.json');
  assert.equal(manifest.simulator_development,'stopped_by_user');
  assert.equal(manifest.simulator_behavior_tests,'not_rerun');
  assert.equal(manifest.fresh_verification_runs.length,14);
  assert.ok(manifest.fresh_verification_runs.every(run=>run.status==='passed'));
  for(const item of manifest.files) assert.equal(await sha(item.file),item.sha256,`Package file changed: ${item.file}`);
  const freeze=await json('registers/simulator-freeze.json');
  for(const [file,hash] of Object.entries(freeze.files)) assert.equal(await sha(file),hash,`Stopped simulator source changed: ${file}`);
  const data=await json('registers/all-in-one-data.json');
  assert.equal(data.project_work_scope.phase,'priority23_first');
  assert.equal(data.project_work_scope.current_priority_count,21);
  assert.equal(data.project_work_scope.full_catalog_role,'preserved_reference_only');
  assert.equal(data.project_work_scope.priority_completion_proven,false);
  console.log(`GME source package verified: ${manifest.files.length+1} files; 14 saved source checks; simulator hashes unchanged`);
}
