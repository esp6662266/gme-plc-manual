/* Local observation persistence and source boundaries, no control execution. */
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const sandbox={window:{}};vm.runInNewContext(fs.readFileSync(__dirname+'/assets/repair-records.js','utf8'),sandbox);
const api=sandbox.window.GMERepairRecords;
const plain=v=>JSON.parse(JSON.stringify(v));
const schemas=JSON.parse(fs.readFileSync(__dirname+'/registers/repair-record-forms.json','utf8')).profiles;
const bc=schemas.find(r=>r.key==='P01'),unknown=schemas.find(r=>r.key==='P22');
const blank=plain(api.collect(bc,{}));
assert.equal(blank.timestamp,null);assert.equal(blank.first_alarm,null);
assert.ok(blank.observations.every(r=>r.value===null&&r.observed_at===null&&r.evidence===null));
assert.equal(blank.identity_confirmed,false);assert.equal(blank.field_verified,false);
assert.deepEqual(plain(api.collect(unknown,{})).observations,[]);
assert.equal(plain(api.collect(unknown,{})).reference_plc_id,'');
const signal=bc.signals[0].id;
const values={first_symptom:'QA only, not field data',record_status:'수리 완료',[signal+'_value']:'0',[signal+'_observed_at']:'2026-10-08T02:30',[signal+'_evidence']:'QA source','step_permit':'Compared without commands',unresolved:'one\ntwo'};
const record=plain(api.collect(bc,values));assert.equal(record.observations[0].value,'0');assert.equal(record.status,'관찰 기록');
assert.deepEqual(record.unresolved,['one','two']);assert.equal(record.decision_observations.find(s=>s.id==='permit').observation,values.step_permit);
const roundtrip=plain(api.fromRecord(record,bc));const back=plain(api.collect(bc,roundtrip,record));assert.deepEqual(back,record);
assert.throws(()=>api.collect(unknown,values,record),/invalid_repair_record/);
assert.throws(()=>api.fromRecord(record,unknown),/invalid_repair_record/);
const extended={...record,custom:{retain:true},observations:record.observations.concat([{id:'future-signal',extra:'retain'}])};
extended.observations[0].extra='source-era field';const merged=plain(api.collect(bc,roundtrip,extended));
assert.deepEqual(merged.custom,extended.custom);assert.equal(merged.observations[0].extra,'source-era field');assert.equal(merged.observations.at(-1).id,'future-signal');
assert.notEqual(api.keyFor('P01'),'P01');assert.notEqual(api.keyFor('P01'),api.keyFor('P02'));
const html=api.render(bc,{title:'<script>unsafe</script>',first_symptom:'<img src=x>'},[]);
assert.ok(!html.includes('<script>unsafe'));assert.ok(html.includes('&lt;script&gt;unsafe'));
assert.ok(html.includes('data-doc="networks/network-1935.html"'));
assert.ok(api.summary(record).includes('0 / 2026-10-08T02:30 / QA source'));
const fn=schemas.find(r=>r.key==='P02');
assert.ok(api.render(fn,{},[]).includes('M31 FN-04와 M36 FN-04A'));
assert.ok(fn.evidence_plan.steps.find(s=>s.step_id==='response').reviews.some(r=>r.id==='construction:C05'&&r.relationship==='declared'));
assert.ok(fn.evidence_plan.steps.find(s=>s.step_id==='permit').reviews.some(r=>r.id==='common:COM-08'&&r.relationship==='related'));
assert.ok(api.render(fn,{},[]).includes('원본 신호 참조로 연관된 자료'));
assert.ok(unknown.evidence_plan.steps.every(s=>s.reviews.every(r=>!r.id.startsWith('common:'))));
assert.ok(api.render(unknown,{},[]).includes('직접 제어 신호는 배정하지 않습니다'));
for(const schema of schemas.filter(r=>r.boundary!=='source_linked')){
  assert.ok(schema.evidence_plan.steps.find(s=>s.step_id==='recovery').requirements.some(r=>r.owner==='전용 제어기·현장'&&r.work.includes('연동 접속')));
  assert.ok(!api.render(schema,{},[]).includes('owner</strong> · work'));
}
const evil=plain(bc);evil.evidence_plan.preflight.requirements[0].work='<img src=x onerror=alert(1)>';
assert.ok(!api.render(evil,{},[]).includes('<img src=x onerror='));
let links=0;
for(const schema of schemas){
  for(const match of api.render(schema,{},[]).matchAll(/data-doc="([^"]+)"/g)){
    const [path,anchor]=match[1].split('#');
    if(path.endsWith('.pdf')){assert.ok(fs.existsSync(__dirname+'/'+path));assert.match(anchor,/^page=\d+$/);links++;continue;}
    const source=fs.readFileSync(__dirname+'/'+path,'utf8');
    if(anchor)assert.ok(source.includes('id="'+anchor+'"'),path+'#'+anchor);links++;
  }
}
console.log(JSON.stringify({status:'passed',profiles:schemas.length,source_links:links,scope:'blank observations, round trip, source scope, unknown fields and escaping; no PLC or simulator tests'}));
