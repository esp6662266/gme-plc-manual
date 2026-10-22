import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFile} from 'node:fs/promises';
const context=vm.createContext({AbortController,setTimeout,clearTimeout,fetch});
vm.runInContext(await readFile(new URL('../all-in-one/assets/io-search-loader.js',import.meta.url),'utf8'),context);
const create=context.GMEIOSearchLoader.create;
const core={schema_version:2,version:'test',build_id:'same-build',manual_path:'registers/io-search-manual.json',counts:{plc:1,manual:1},records:[{id:'plc',kind:'plc'}]};
const manual={schema_version:1,version:'test',build_id:core.build_id,records:[{id:'manual',kind:'manual'}]};
const response=value=>({ok:true,json:async()=>value});
test('core resolves independently, concurrent requests share work, and records survive manual failure/retry',async()=>{
  let coreCalls=0,manualCalls=0;
  const loader=create({fetch:async path=>{if(path.includes('manual.json')){if(++manualCalls===1)throw new Error('offline');return response(manual);}coreCalls++;return response(core);}});
  await Promise.all([loader.load('core','test'),loader.load('core','test')]);
  assert.equal(coreCalls,1);assert.equal(loader.records().length,1);
  await assert.rejects(loader.load('manual','test'));
  assert.equal(loader.states.core.status,'ready');assert.equal(loader.records().length,1);
  await loader.load('manual','test');
  assert.equal(coreCalls,1);assert.equal(manualCalls,2);assert.equal(loader.records().length,2);
  assert.equal(loader.records('ocr').length,1);assert.equal(loader.records('manual')[0].id,'manual');
});
test('timeout aborts stalled body decoding and retry can succeed',async()=>{
  let timeoutCallback,aborted=false,calls=0;
  const loader=create({setTimer:callback=>{timeoutCallback=callback;return 1;},clearTimer:()=>{},fetch:async(_,{signal})=>{calls++;signal.addEventListener('abort',()=>{aborted=true;});return calls===1?{ok:true,json:()=>new Promise(()=>{})}:response(core);}});
  const pending=loader.load('core','test');const rejected=assert.rejects(pending,/초과/);timeoutCallback();await rejected;
  assert.ok(aborted);assert.equal(loader.states.core.status,'error');
  await loader.load('core','test');assert.equal(loader.states.core.status,'ready');
});
test('mixed deployment data and invalid core schemas are rejected without losing ready core',async()=>{
  const loader=create({fetch:async path=>response(path.includes('manual.json')?{...manual,build_id:'old-build'}:core)});
  await loader.load('core','test');await assert.rejects(loader.load('manual','test'),/현재 검색 색인/);
  assert.equal(loader.states.core.status,'ready');assert.equal(loader.states.manual.status,'error');
  await assert.rejects(create({fetch:async()=>response({...core,schema_version:1})}).load('core','test'),/형식/);
  await assert.rejects(create({fetch:async()=>response(core)}).load('core','old'),/버전/);
});
test('late timed-out responses cannot overwrite a successful retry and subscriptions can dispose',async()=>{
  let release,calls=0,callback,notifications=0;
  const loader=create({setTimer:fn=>{callback=fn;return 1;},clearTimer:()=>{},fetch:()=>++calls===1?new Promise(resolve=>{release=resolve;}):Promise.resolve(response(core))});
  const unsubscribe=loader.subscribe(()=>notifications++);
  const old=loader.load('core','test');const failure=assert.rejects(old);callback();await failure;
  await loader.load('core','test');unsubscribe();const before=notifications;
  release(response({...core,build_id:'stale'}));await Promise.resolve();await Promise.resolve();
  assert.equal(loader.states.core.value.build_id,'same-build');assert.equal(notifications,before);
});
