import test from 'node:test';
import assert from 'node:assert/strict';
import { createDocumentsHandler, MAX_FILE_SIZE } from '../src/documents-service.mjs';

function memoryStore() {
  const entries = new Map(); let revision = 0; let failMetadata = false;
  return {
    entries,
    setFailure: value => { failMetadata = value; },
    async set(key,data,options={}) { const old=entries.get(key); if(options.onlyIfNew&&old || options.onlyIfMatch&&old?.etag!==options.onlyIfMatch)return{modified:false}; const etag=String(++revision); entries.set(key,{data,etag});return{modified:true,etag}; },
    async setJSON(key,data,options) { if(failMetadata)throw new Error('storage unavailable');return this.set(key,structuredClone(data),options); },
    async get(key) { return entries.get(key)?.data ?? null; },
    async getWithMetadata(key) { return entries.get(key) ?? null; },
    async list({prefix}) {return{blobs:[...entries.keys()].filter(key=>key.startsWith(prefix)).map(key=>({key}))};},
    async delete(key){entries.delete(key);},
  };
}
function upload(values={}, contents='PV01 점검 기록') {
  const form=new FormData(); for(const [key,value] of Object.entries({title:'PV01 점검 기록',category:'report',note:'A/B 센서 확인',...values}))form.set(key,String(value));
  form.set('file',new File([contents],values.filename||'report.md'));
  return new Request('https://gme.test/api/documents',{method:'POST',headers:{origin:'https://gme.test'},body:form});
}
test('login is required and another account cannot list or download private files',async()=>{
  const store=memoryStore();let user=null;const handle=createDocumentsHandler({getUser:async()=>user,getStore:()=>store});
  assert.equal((await handle(new Request('https://gme.test/api/documents'))).status,401);
  user={id:'owner-a'};const saved=await (await handle(upload())).json();
  const download=`https://gme.test/api/documents/${saved.document.familyId}/${saved.document.id}`;
  assert.equal(await (await handle(new Request(download))).text(),'PV01 점검 기록');
  user={id:'owner-b'};assert.deepEqual((await(await handle(new Request('https://gme.test/api/documents'))).json()).documents,[]);
  assert.equal((await handle(new Request(download))).status,404);
  assert.equal((await handle(upload({previousId:saved.document.familyId,previousVersion:1}))).status,404);
});
test('revisions preserve original content, stale changes are refused, and downloads are attachments',async()=>{
  const store=memoryStore();const handle=createDocumentsHandler({getUser:async()=>({id:'owner'}),getStore:()=>store});
  const first=await(await handle(upload())).json();
  const secondResponse=await handle(upload({previousId:first.document.familyId,previousVersion:1},'두 번째 기록'));
  assert.equal(secondResponse.status,201);const second=await secondResponse.json();assert.equal(second.version,2);
  assert.equal((await handle(upload({previousId:first.document.familyId,previousVersion:1}))).status,409);
  const listed=await(await handle(new Request('https://gme.test/api/documents'))).json();assert.equal(listed.documents.length,2);
  const response=await handle(new Request(`https://gme.test/api/documents/${first.document.familyId}/${first.document.id}`));
  assert.equal(await response.text(),'PV01 점검 기록');assert.match(response.headers.get('content-disposition'),/^attachment;/);assert.equal(response.headers.get('cache-control'),'no-store');assert.equal(first.document.sha256.length,64);
});
test('cross-site, invalid file, oversize and storage failures cannot produce visible incomplete records',async()=>{
  const store=memoryStore();const handle=createDocumentsHandler({getUser:async()=>({id:'owner'}),getStore:()=>store});
  const cross=upload();cross.headers.set('origin','https://bad.test');assert.equal((await handle(cross)).status,403);
  assert.equal((await handle(upload({filename:'bad.html'}))).status,400);
  assert.equal((await handle(upload({},new Uint8Array(MAX_FILE_SIZE+1)))).status,413);
  store.setFailure(true);assert.equal((await handle(upload())).status,503);assert.equal(store.entries.size,0);
});
test('a concurrent update cannot overwrite an existing revision',async()=>{
  const store=memoryStore();const handle=createDocumentsHandler({getUser:async()=>({id:'owner'}),getStore:()=>store});
  const first=await(await handle(upload())).json();
  const requests=[upload({previousId:first.document.familyId,previousVersion:1},'A'),upload({previousId:first.document.familyId,previousVersion:1},'B')];
  const responses=await Promise.all(requests.map(handle));assert.deepEqual(responses.map(response=>response.status).sort(),[201,409]);
  const list=await(await handle(new Request('https://gme.test/api/documents'))).json();assert.equal(list.documents.length,2);
  assert.equal([...store.entries.keys()].filter(key=>key.includes('/files/')).length,2);
});
