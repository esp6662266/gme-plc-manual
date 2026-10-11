import assert from 'node:assert/strict';
import { lstat, readdir, mkdir, copyFile, readFile } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { createHash } from 'node:crypto';
const manifestName='all-in-one-package-manifest.json';
export function packagePaths(manifest) {
  const paths=manifest.files.map(item=>item.file).concat(manifestName),seen=new Set();
  for(const path of paths) {
    assert.ok(typeof path==='string' && path && !path.includes('\\') && !path.includes('\0') && !path.startsWith('/') && !path.includes(':') && path.split('/').every(p=>p && p!=='.' && p!=='..'),'Unsafe package path: '+path);
    assert.ok(!seen.has(path.toLowerCase()),'Duplicate package path: '+path);seen.add(path.toLowerCase());
  }
  return paths;
}
export async function assertPackageInventory(directory,manifest) {
  assert.ok(!(await lstat(directory)).isSymbolicLink(),'Package directory must not be a symbolic link');
  const actual=[];
  async function walk(folder,prefix='') {
    for(const name of await readdir(folder)) {
      const path=join(folder,name),relative=prefix+name,info=await lstat(path);
      assert.ok(!info.isSymbolicLink(),'Package symbolic link refused: '+relative);
      if(name==='.DS_Store' || name==='__pycache__')continue;
      if(info.isDirectory())await walk(path,relative+'/');
      else {assert.ok(info.isFile(),'Non-regular package entry: '+relative);actual.push(relative);}
    }
  }
  await walk(directory);
  const expected=packagePaths(manifest),extra=actual.filter(p=>!expected.includes(p)),missing=expected.filter(p=>!actual.includes(p));
  assert.ok(!extra.length && !missing.length,'Package inventory differs; extra: '+extra.join(', ')+'; missing: '+missing.join(', '));
  return expected;
}
export async function copyVerifiedManual(source,destination,manifest) {
  const paths=await assertPackageInventory(source,manifest);
  for(const path of paths) {
    const target=join(destination,path);await mkdir(dirname(target),{recursive:true});await copyFile(join(source,path),target);
    const expected=path===manifestName ? manifest.manifest_sha256 : manifest.files.find(item=>item.file===path).sha256;
    assert.equal(createHash('sha256').update(await readFile(target)).digest('hex'),expected,'Copied package file changed: '+path);
  }
}
