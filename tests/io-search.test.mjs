import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, access } from 'node:fs/promises';
import vm from 'node:vm';
import { buildIndex, csv } from '../scripts/build-io-search-index.mjs';
const context=vm.createContext({});vm.runInContext(await readFile(new URL('../all-in-one/assets/io-search-model.js',import.meta.url),'utf8'),context);
const M=context.GMEIOSearchModel,index=await buildIndex();
const search=(q,filter)=>M.search(index.records,q,filter);
test('search covers every preserved PLC and HMI symbol, including unassigned and shared references',()=>{
  assert.equal(index.counts.plc,789);assert.equal(index.counts.hmi,782);
  assert.ok(index.records.some(r=>r.kind==='plc'&&!r.equipment.length));
  const shared=index.records.find(r=>r.kind==='plc'&&r.equipment.length>1);
  for(const equipment of shared.equipment)assert.ok(search(shared.symbol,{equipment,kind:'plc'}).some(r=>r.id===shared.id));
  assert.ok(search('Q0.0').some(r=>r.kind==='circuit'&&r.title.includes('기동 명령')&&r.equipment.includes('BC01')));
  assert.equal(search('Q0.0')[0].kind,'circuit');
  for(const q of ['I3.2','I8.1'])assert.ok(search(q)[0].address.toUpperCase().startsWith('%'+q+' /'));
  assert.ok(search('I0.0').some(r=>r.kind==='circuit'&&r.title.includes('운전 응답')));
  assert.ok(search('IW394').some(r=>r.symbol==='fn04_current'));
});
test('optional percent, spaces, fullwidth and DB bit notations search the same address',()=>{
  const ids=q=>Array.from(search(q),r=>r.id).sort();
  for(const q of ['%q0.0','q 0 . 0','Ｑ０．０'])assert.deepEqual(ids(q),ids('Q0.0'));
  for(const q of ['DB11.DBX0.0','DB11.X0.0','%DB11.DBX0.0'])assert.deepEqual(ids(q),ids('DB11,X0.0'));
  assert.ok(search('DB11.DBX0.0').some(r=>r.kind==='hmi'&&r.symbol==='BC_01\\RispostaA'));
});
test('complete identifier boundaries preserve address widths and adjacent numbers',()=>{
  const records=['I0.0','I10.0','I0.01','IW2','IW20','IB2','8.9','18.9','8.90'].map((address,i)=>({id:String(i),address,title:address,text:'',source:'',kind:'plc',equipment:[],equipment_names:[]}));
  for(const address of ['I0.0','IW2','8.9'])assert.deepEqual(Array.from(M.search(records,address),r=>r.address),[address]);
  assert.equal(search('번호없음987654321').length,0);assert.equal(search('x').length,0);
  const combined=search('I0.0 Q0.0');assert.ok(combined.some(r=>r.address==='%I0.0'));assert.ok(combined.some(r=>r.address==='%Q0.0'));
});
test('filters, historical status, original spelling and escaping stay explicit',()=>{
  assert.ok(search('기동 명령',{kind:'circuit',equipment:'BC01'}).every(r=>r.kind==='circuit'&&r.equipment.includes('BC01')));
  assert.ok(index.records.filter(r=>r.equipment.includes('CC01')).every(r=>r.status.includes('철거')));
  const html=M.highlight('<img src=x onerror="bad()"> %q0.0','Q0.0');assert.ok(!html.includes('<img'));assert.ok(html.includes('&lt;img'));assert.match(html,/%<mark>q0\.0<\/mark>/);
  assert.ok(search('DB11,X0.0').filter(r=>r.kind==='hmi').every(r=>r.boundary.includes('미확인')));
});
test('index has current sources and every evidence link points to a preserved public file',async()=>{
  assert.deepEqual(JSON.parse(await readFile(new URL('../all-in-one/registers/io-search-index.json',import.meta.url))),index);
  const paths=new Set(index.records.flatMap(r=>r.links.map(l=>l.url.split('#')[0])));
  for(const path of paths){assert.ok(!path.includes('..'));await access(new URL('../all-in-one/'+path,import.meta.url));}
});
test('CSV parser preserves quoted comments, commas, newlines and BOM',()=>{
  assert.deepEqual(csv('\uFEFFname,description\r\na,"one, two\nthree ""four"""\r\n'),[{name:'a',description:'one, two\nthree "four"'}]);
});
