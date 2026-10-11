import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, readFile, rm, symlink, chmod } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { spawn } from 'node:child_process';
import { findPython } from '../scripts/python-runner.mjs';
import { assertPackageInventory, copyVerifiedManual, packagePaths } from '../scripts/package-inventory.mjs';
const digest=x=>createHash('sha256').update(x).digest('hex');
test('Python discovery accepts supported python3, skips old versions, and respects explicit paths',()=>{
  const calls=[];
  const probe=(command,args,options)=>{calls.push([command,args,options]);return {status:0,stdout:JSON.stringify(command==='python3'?[3,9,6]:[3,12,1])};};
  assert.equal(findPython({env:{},platform:'darwin',probe}).command,'python');
  assert.equal(findPython({env:{GME_PYTHON:'/path with spaces/한글 python'},probe}).command,'/path with spaces/한글 python');
  assert.equal(calls.at(-1)[0],'/path with spaces/한글 python');
  assert.equal(calls.at(-1)[2].env.GME_PYTHON,'/path with spaces/한글 python');
  assert.equal(findPython({env:{},platform:'win32',probe:()=>({status:0,stdout:'[3,11,2]'})}).command,'py');
  assert.equal(findPython({env:{},platform:'darwin',probe:()=>({status:0,stdout:'[3,10,0]'})}).command,'python3');
  assert.throws(()=>findPython({env:{GME_PYTHON:'missing'},probe:()=>({error:new Error('ENOENT')})}),/3.10/);
  assert.throws(()=>findPython({env:{},probe:()=>({status:0,stdout:'[3,9,9]'})}),/3.10/);
  for(const stdout of ['{}','"unexpected"','null','false'])assert.throws(()=>findPython({env:{},probe:()=>({status:0,stdout})}),/3.10/);
});
test('Python CLI forwards child failures and interruption', {skip:process.platform==='win32',timeout:12000},async()=>{
  const temp=await mkdtemp(join(tmpdir(),'gme-python-')),fake=join(temp,'python with spaces');
  await writeFile(fake,'#!'+process.execPath+'\nif(process.argv.includes("-c")){console.log("[3,12,1]");process.exit(0)}\nif(process.argv.includes("env"))process.exit(process.env.PYTHONOPTIMIZE==="0"?0:9);\nif(process.argv.includes("wait")){console.log("READY");setInterval(()=>{},1000)}else process.exit(7);\n');await chmod(fake,0o755);
  const launch=(args,interrupt=false)=>new Promise((resolve,reject)=>{
    const child=spawn(process.execPath,['scripts/python-runner.mjs',...args],{cwd:process.cwd(),env:{...process.env,GME_PYTHON:fake,PYTHONOPTIMIZE:'1'},stdio:['ignore','pipe','pipe']});
    const timer=setTimeout(()=>{child.kill('SIGTERM');reject(new Error('child timeout'));},5000);
    child.stdout.on('data',data=>{if(interrupt&&data.toString().includes('READY'))child.kill('SIGINT');});
    child.once('error',reject);child.once('exit',code=>{clearTimeout(timer);resolve(code);});
  });
  try {assert.equal(await launch(['exit']),7);assert.equal(await launch(['env']),0);assert.equal(await launch(['wait'],true),130);}
  finally {await rm(temp,{recursive:true,force:true});}
});
test('package inventory rejects extra, missing and symbolic files, and copies only checked bytes',async(t)=>{
  const temp=await mkdtemp(join(tmpdir(),'gme-inventory-')),source=join(temp,'source'),destination=join(temp,'output');
  await mkdir(source);const text='source bytes',manifest={files:[{file:'asset.txt',sha256:digest(text)}]};
  const raw=JSON.stringify(manifest);manifest.manifest_sha256=digest(raw);
  await writeFile(join(source,'asset.txt'),text);await writeFile(join(source,'all-in-one-package-manifest.json'),raw);
  try {
    await assertPackageInventory(source,manifest);await copyVerifiedManual(source,destination,manifest);
    assert.equal(await readFile(join(destination,'asset.txt'),'utf8'),text);
    await writeFile(join(source,'user-record.json'),'{}');await assert.rejects(assertPackageInventory(source,manifest),/extra.*user-record/);await rm(join(source,'user-record.json'));
    await rm(join(source,'asset.txt'));await assert.rejects(assertPackageInventory(source,manifest),/missing.*asset/);await writeFile(join(source,'asset.txt'),'changed');
    await assert.rejects(copyVerifiedManual(source,join(temp,'changed-output'),manifest),/changed/);await writeFile(join(source,'asset.txt'),text);
    await t.test('file and directory symbolic links are refused',async(st)=>{
      try {await symlink(join(source,'asset.txt'),join(source,'alias.txt'));}
      catch(error){if(process.platform==='win32'&&error.code==='EPERM'){st.skip('Windows symbolic-link permission unavailable');return;}throw error;}
      await assert.rejects(assertPackageInventory(source,manifest),/symbolic/);await rm(join(source,'alias.txt'));
      await symlink(destination,join(source,'alias-dir'),process.platform==='win32'?'junction':'dir');await assert.rejects(assertPackageInventory(source,manifest),/symbolic/);await rm(join(source,'alias-dir'));
    });
    await mkdir(join(source,'__pycache__'));await writeFile(join(source,'__pycache__','ignored.pyc'),'cache');await writeFile(join(source,'.DS_Store'),'cache');await assertPackageInventory(source,manifest);
    for(const file of ['../outside','/absolute','a\\b','C:/outside','asset.txt'])assert.throws(()=>packagePaths({files:[{file},{file}]}));
  } finally {await rm(temp,{recursive:true,force:true});}
});
