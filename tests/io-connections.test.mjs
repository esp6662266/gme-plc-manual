import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFile} from 'node:fs/promises';
import {validateConnections} from '../scripts/validate-io-connections.mjs';
const root=new URL('../all-in-one/',import.meta.url),read=async p=>JSON.parse(await readFile(new URL(p,root)));
const notes=await read('registers/io-search-reference-notes.json'),pages=await read('registers/drawing-search-pages.json'),data=await read('registers/all-in-one-data.json');
const context=vm.createContext({URLSearchParams});
for(const path of ['assets/io-search-model.js','assets/io-connections.js'])vm.runInContext(await readFile(new URL(path,root),'utf8'),context);
const M=context.GMEIOSearchModel,C=context.GMEIOConnections,byAddress=new Map(notes.records.map(r=>[r.address,r]));
const options={resources:data.resources,pages:pages.pages};
test('six reviewed connection profiles use original pages with explicit parallel and field boundaries',()=>{
  assert.deepEqual(notes.records.filter(r=>r.trace).map(r=>r.address).sort(),['13.6','14KA10','14KA6','14KA8','8.10','8.9'].sort());
  const result=validateConnections(notes,options);assert.equal(result.nodes,93);assert.equal(result.routes,14);
  for(const r of notes.records.filter(r=>r.trace)){assert.equal(r.trace.basis,'original_drawing_visual_comparison');assert.ok(r.trace.unknowns.some(x=>x.includes('현재')));}
  assert.deepEqual(byAddress.get('13.6').trace.parallel.nodes.map(n=>n.label),['14KA5','14KA6','14KA7','14KA8','14KA10']);
  assert.ok(!byAddress.get('13.6').trace.routes[0].nodes.some(n=>n.kind==='coil'));
});
test('wire and contact paths preserve exact terminal numbers, AC source and STO orientation',()=>{
  const a=byAddress.get('8.9').trace.routes[0],b=byAddress.get('8.10').trace.routes[0];
  assert.deepEqual(a.nodes.map(n=>n.label),['8T1','8.7','14KA9','8.9','14KA10','8.11','X1:419']);
  assert.deepEqual(b.nodes.map(n=>n.label),['8T1','8.8','14KA9','8.10','14KA10','8.12','X1:420']);
  assert.equal(a.nodes[4].terminals,'1 → 2');assert.equal(b.nodes[4].terminals,'3 → 4');
  assert.deepEqual(byAddress.get('14KA6').trace.routes.slice(0,3).map(r=>r.nodes.find(n=>n.label==='14KA6').terminals),['6 → 5','2 → 1','4 → 3']);
  const supply=byAddress.get('13.6').trace.routes[0];assert.equal(supply.nodes[0].label,'110Vac 9.8');
  assert.equal(supply.nodes.find(n=>n.label==='13KA1').terminals,'23 → 24');
  assert.match(supply.nodes.find(n=>n.label==='13KA1').detail,/단자 번호/);
  for(const tag of ['14KA6','14KA8','14KA10'])assert.deepEqual(byAddress.get(tag).trace.coil,{a1:'13.6',a2:'0Vac 9.9',page:15,fg:14});
});
test('every route node has its own located printed token and a source-matched page',async()=>{
  const cache=new Map();
  for(const r of notes.records.filter(r=>r.trace)){const t=r.trace;for(const node of [...t.routes.flatMap(r=>r.nodes),...(t.parallel?.nodes||[]),...(t.parallel?[t.parallel.return_node]:[])]){
    if(!cache.has(node.page))cache.set(node.page,await read('registers/drawing-search/oem-'+String(node.page).padStart(3,'0')+'.json'));
    const page=cache.get(node.page);assert.equal(page.source_sha256,notes.source_sha256);assert.equal(node.fg,node.page-1);
    const hits=M.locate(page,node.query);assert.ok(hits.length,node.label+' page '+node.page);
    if(node.focus){const selected=hits[M.nearest(hits,node.focus)];assert.ok(Math.abs((selected.bbox[0]+selected.bbox[2])/2-node.focus[0])<.02);}
  }}
  const terminal=byAddress.get('8.9').trace.routes[0].nodes.at(-1);assert.equal(terminal.query,'419');
});
test('rendered traces remain reviewed-only, escaped, and use independent location queries',()=>{
  const record=byAddress.get('14KA10'),allowed=new Set([notes.source]);
  const html=C.render(record,{allowed,query:'14KA10',selectedRoute:'burner-2'});
  assert.match(html,/data-io-location-query="420"/);assert.match(html,/data-io-location-query="8\.10"/);assert.match(html,/data-io-location-focus="0\.457,0\.65"/);
  assert.match(html,/value="burner-2" selected/);assert.ok(!html.includes('data-io-location-query="419"'));
  assert.match(html,/data-io-trace="reviewed-14KA10" open/);
  assert.ok(!C.render(record,{allowed,query:'13.6'}).includes('data-io-trace="reviewed-14KA10" open'));
  assert.equal(C.render({...record,kind:'ocr'},{allowed}),'');
  const unsafe=structuredClone(record);unsafe.trace.routes[0].nodes[0].label='<img src=x onerror=bad()>';
  assert.ok(!C.render(unsafe,{allowed}).includes('<img'));assert.match(C.render(unsafe,{allowed}),/&lt;img/);
  assert.ok(!C.render(record,{allowed:new Set()}).includes('data-io-drawing='));
});
test('related searches reset restrictive filters while preserving main equipment scope and browser history hashes',()=>{
  const hash=C.relatedHash('#view=io-search&equipment=P01&scope=all&search-kind=ocr&search-equipment=BC01&search-common=0&q=8.9','14KA10');
  const p=new URLSearchParams(hash.slice(1));assert.equal(p.get('q'),'14KA10');assert.equal(p.get('view'),'io-search');assert.equal(p.get('equipment'),'P01');assert.equal(p.get('scope'),'all');
  for(const key of ['search-kind','search-equipment','search-common'])assert.ok(!p.has(key));
});
test('invalid source, node geometry and non-reference traces are rejected before publishing',()=>{
  for(const mutate of [n=>{n.records[0].kind='ocr';},n=>{n.records[0].trace.source_sha256='bad';},n=>{n.records[0].trace.routes[0].nodes[0].url='https://example.com/a.pdf#page=9';},n=>{n.records[0].trace.routes[0].nodes[0].focus=[-1,1];}]){
    const bad=structuredClone(notes);mutate(bad);assert.throws(()=>validateConnections(bad,options));
  }
  assert.equal(M.nearest([{bbox:[.1,.1,.2,.2]},{bbox:[.7,.1,.8,.2]}],[.75,.15]),1);
  assert.equal(M.nearest([{bbox:[.1,.1,.2,.2]}],[Infinity,0]),0);
});

test('reviewed explanations without route profiles stay valid and never invent connection nodes',()=>{
  assert.ok(notes.records.some(r=>r.kind==='reference'&&!r.trace));
  const allowed=new Set([notes.source]);
  for(const r of notes.records.filter(r=>!r.trace))assert.equal(C.render(r,{allowed,query:r.address}),'');
  const traced={...notes,records:notes.records.filter(r=>r.trace)};
  assert.deepEqual(validateConnections(notes,options),validateConnections(traced,options));
});
