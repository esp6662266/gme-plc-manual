/* Profile isolation and generator boundaries. No simulator execution. */
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const plain=x=>JSON.parse(JSON.stringify(x)),sandbox={window:{},TextEncoder};
for(const n of ['repair-records','note-record-store','equipment-standard','bc01-tools'])vm.runInNewContext(fs.readFileSync(__dirname+'/assets/'+n+'.js','utf8'),sandbox);
const {GMEEquipmentStandard:standard,GMEBC01Tools:tools,GMERepairRecords:repair,GMENoteStore:store}=sandbox.window;
const data=JSON.parse(fs.readFileSync(__dirname+'/registers/all-in-one-data.json'));
assert.equal(standard.profile(data,'P99'),null);assert.throws(()=>standard.referenceContext(data,'P99'),/구현/);
assert.equal(standard.profile(data,'P01').specification.id,'BC01');
const synthetic=plain(data);synthetic.equipment_standards.profiles=synthetic.equipment_standards.profiles.filter(p=>p.priority_key!=='P02');synthetic.equipment_standards.profiles.push({priority_key:'P02',catalog_id:'FN04',source_hashes:{'QA-only':'f'.repeat(64)},source_bundle_sha256:'e'.repeat(64),tools:{restore:true}});
const schema=data.repair_record_forms.profiles.find(p=>p.key==='P02'),valid=new Set(data.equipment.map(e=>e.id).concat(data.priority.map(p=>p.key)));
const note={id:'qa-fn04',equipment:'P02',title:'QA only',text:'QA only',updated:'2026-10-11T05:00:00Z',future:{retained:1},repair_observation:plain(repair.collect(schema,{first_symptom:'QA only',[schema.signals[0].id+'_value']:'0'}))};
const foreign={...note,id:'qa-bc01',equipment:'P01',repair_observation:undefined};
const input=JSON.stringify(tools.backupEnvelope([foreign,note],synthetic,'2026-10-11T05:00:00Z','P02'));
const incoming=plain(tools.parseBackup(input,store.decodeNotes,valid,schema));assert.deepEqual(incoming.notes,[note]);assert.equal(incoming.skipped,1);
assert.throws(()=>tools.parseBackup(JSON.stringify({...JSON.parse(input),notes:[{...note,repair_observation:{...note.repair_observation,equipment:'P01'}}]}),store.decodeNotes,valid,schema));
const changed=plain(note);changed.repair_observation.observations[0].value='1';changed.title='QA changed';delete changed.future;
const plan=plain(tools.planRestore([foreign,note],[changed]));
const merged=plain(tools.applyRestore([foreign,note],plan,{0:'replace'},()=> 'copy','P02'));
assert.deepEqual(merged.notes[0],plain(foreign));assert.deepEqual(merged.notes[1].future,note.future);assert.equal(merged.notes[1].repair_observation.observations[0].value,'1');
assert.throws(()=>tools.applyRestore([foreign,note],plan,{0:'replace'},()=> 'copy','P01'),/밖/);
assert.ok(plain(tools.comparisonRows(note,changed,schema)).some(r=>r.key.endsWith(':value')&&r.changed));
assert.equal(tools.referenceContext(synthetic,'P02').source_bundle_sha256,'e'.repeat(64));assert.notEqual(tools.referenceContext(synthetic,'P02').source_bundle_sha256,tools.referenceContext(synthetic).source_bundle_sha256);
const p02=standard.profile(data,'P02');
assert.ok(p02,'FN04 pilot profile is required in v1.4.0');
if(p02){
 const read=f=>JSON.parse(fs.readFileSync(__dirname+'/registers/'+f));
 assert.deepEqual(plain(p02.specification),read('control-spec.json').specifications.find(p=>p.id==='FN04'));
 assert.deepEqual(plain(p02.alarm),read('alarm-recovery.json').profiles.find(p=>p.id==='FN04'));
 assert.deepEqual(plain(p02.regulation),read('regulation-manual.json').loops.find(p=>p.id==='FN04'));
 assert.equal(p02.specification.direct_rules.length,22);assert.equal(p02.specification.direct_rules.filter(r=>r.opaque).length,3);assert.equal(p02.alarm.alarms.length,2);assert.equal(p02.alarm.timers[0].preset.literal,'S5T#17S');
 assert.equal(p02.source_pairs.find(p=>p.signal==='속도 설정').path,'networks/network-1689.html#gme-fn04-wire-875');assert.equal(p02.source_pairs.find(p=>p.signal==='전류 전달').path,'networks/network-1770.html#gme-fn04-wire-1491');
 const crypto=require('node:crypto');for(const [f,h] of Object.entries(p02.source_hashes))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);
 for(const loc of p02.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
 const route=standard.normalize(data,'P02',new URLSearchParams('section=bad&item=bad&text=bad'));assert.equal(route.bc01Section,'overview');assert.equal(route.bc01Text,'standard');
}
const p15=standard.profile(data,'P15');assert.ok(p15,'FN01 profile is required in v1.5.0');
const readRegister=f=>JSON.parse(fs.readFileSync(__dirname+'/registers/'+f));
assert.deepEqual(plain(p15.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='FN01'));
assert.deepEqual(plain(p15.alarm),readRegister('alarm-recovery.json').profiles.find(p=>p.id==='FN01'));
assert.equal(p15.regulation,null);assert.equal(p15.specification.direct_rules.length,20);assert.equal(p15.specification.direct_rules.filter(r=>r.opaque).length,3);
assert.equal(p15.alarm.alarms.length,2);assert.equal(p15.alarm.timers.length,1);assert.equal(p15.alarm.timers[0].preset.literal,'S5T#2S');
assert.deepEqual(p15.control_reference.native_refs.map(r=>r.rule_id),['1845:60','1845:65','1845:70','1845:74','1845:78']);assert.ok(p15.control_reference.native_refs.every(r=>r.opaque));
assert.equal(p15.specification.direct_rules.find(r=>r.rule_id==='1951:685')['정적 조건식'],'((ON AND Allarm.FN_01_FAULT) OR (ON AND Allarm.FN01_INV) OR (ON AND [Data.SET_PERC_VT01 = 0]) OR (ON AND Stop_Fan_FN01) OR ((ON AND Allarm.HYDROGEN_BOX_FAULT) AND NOT [UNDER TESTING]))');
assert.deepEqual(p15.source_pairs.map(p=>p.path),['networks/network-1951.html#gme-fn01-part-689','networks/network-1798.html#gme-fn01-part-740','networks/network-1798.html#gme-fn01-part-744','networks/network-1685.html#gme-fn01-wire-504','networks/network-1772.html#gme-fn01-wire-1531']);
assert.equal(data.repair_record_forms.profiles.find(p=>p.key==='P15').signals.length,4);
const resetXML=fs.readFileSync(__dirname+'/sources/decoded-original/0253-FlgNet.xml','utf8');
assert.match(resetXML,/<Part UId="724" Gate="Contact">\s*<Negated PinName="operand" \/>/);assert.match(resetXML,/<Wire UId="725">\s*<PCon UId="724" PinName="out" \/>\s*<PCon UId="676" PinName="in5" \/>/);
assert.match(resetXML,/<Wire UId="709">\s*<PCon UId="676" PinName="out" \/>\s*<PCon UId="685" PinName="in" \/>/);
const native2s=fs.readFileSync(__dirname+'/sources/decoded-original/0656-IdentXmlPart.xml','utf8');const timerDeclaration=native2s.split('</LiteralConstant>').find(s=>s.includes('RID="28"'));assert.ok(timerDeclaration.includes('NID="20" UID="695"'));assert.ok(timerDeclaration.includes('SV="S5T_x0023_2S"'));
const crypto15=require('node:crypto');for(const [f,h] of Object.entries(p15.source_hashes))assert.equal(crypto15.createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);
for(const loc of p15.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
assert.deepEqual(plain(standard.sections.map(([section])=>standard.items(data,'P15',section).length)),[3,4,21,5,4,5,5]);
for(const [key,total] of [['P02',49],['P15',47]]){let rendered=0;for(const [section] of standard.sections)for(const item of standard.items(data,key,section)){const html=standard.render(data,key,{bc01Section:section,bc01Item:item.id,bc01Text:'standard',bc01Find:''});assert.ok(html.includes('standard-content-title'));assert.ok(!html.includes('undefined'));rendered++;}assert.equal(rendered,total);}
const fn01Overview=standard.render(data,'P15',{bc01Section:'overview',bc01Item:'baseline',bc01Text:'standard',bc01Find:''});assert.ok(fn01Overview.includes('FG47/48'));assert.ok(!fn01Overview.includes('FG59/60'));
const fn01Timer=standard.render(data,'P15',{bc01Section:'alarms',bc01Item:'timer',bc01Text:'large',bc01Find:'Tag_63'});assert.ok(fn01Timer.includes('S5T#2S'));assert.ok(!fn01Timer.includes('S5T#17S'));
const fn01Schema=data.repair_record_forms.profiles.find(p=>p.key==='P15');
const fn01Note={id:'qa-fn01',equipment:'P15',title:'QA FN01',text:'',updated:'old',future:{retained:1},repair_observation:plain(repair.collect(fn01Schema,{first_symptom:'QA FN01',[fn01Schema.signals[0].id+'_value']:'0'}))};
const fn01Incoming=plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note,fn01Note],data,'2026-10-11T05:00:00Z','P15')),store.decodeNotes,valid,fn01Schema));assert.deepEqual(fn01Incoming.notes,[fn01Note]);assert.equal(fn01Incoming.skipped,1);
assert.throws(()=>tools.parseBackup(JSON.stringify(tools.backupEnvelope([{...fn01Note,repair_observation:{...fn01Note.repair_observation,equipment:'P02'}}],data,'2026-10-11T05:00:00Z','P15')),store.decodeNotes,valid,fn01Schema));
assert.equal(tools.referenceContext(data,'P15').source_bundle_sha256,p15.source_bundle_sha256);assert.notEqual(p15.source_bundle_sha256,p02.source_bundle_sha256);

const p16=standard.profile(data,'P16');assert.ok(p16,'FN02 profile is required in v1.6.0');
assert.deepEqual(plain(p16.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='FN02'));
assert.deepEqual(plain(p16.alarm),readRegister('alarm-recovery.json').profiles.find(p=>p.id==='FN02'));
assert.equal(p16.regulation,null);assert.equal(p16.control_reference.id,'VT02');assert.equal(p16.control_reference.controller_evidence,null);
assert.equal(p16.specification.direct_rules.length,15);assert.deepEqual(p16.specification.direct_rules.filter(r=>r.opaque).map(r=>r.rule_id),['1026:1553','1050:2890']);
assert.equal(p16.alarm.alarms.length,2);assert.equal(p16.alarm.timers[0].name,'Tag_61');assert.equal(p16.alarm.timers[0].preset.literal,'S5T#2S');
assert.deepEqual(p16.source_pairs.map(p=>p.path),['networks/network-1948.html#gme-fn02-part-596','networks/network-1796.html#gme-fn02-part-655','networks/network-1796.html#gme-fn02-part-662','networks/network-1688.html#gme-fn02-wire-671','networks/network-1767.html#gme-fn02-wire-1471']);
assert.equal(p16.source_locations.find(l=>l.network===1770&&l.kind==='wire'&&l.uid==='1491').path,'networks/network-1770.html#gme-fn04-wire-1491');
assert.equal(data.repair_record_forms.profiles.find(p=>p.key==='P16').signals.length,4);
const native16=fs.readFileSync(__dirname+'/sources/decoded-original/0431-FlgNet.xml','utf8');
assert.match(native16,/<Part UId="655" Gate="Contact">\s*<Negated PinName="operand" \/>/);
assert.match(native16,/<Wire UId="640">\s*<OCon UId="630" \/>\s*<PCon UId="655" PinName="operand" \/>/);
const native16timer=fs.readFileSync(__dirname+'/sources/decoded-original/0656-IdentXmlPart.xml','utf8').split('</LiteralConstant>').find(s=>s.includes('RID="28"'));assert.ok(native16timer.includes('NID="18" UID="627"'));assert.ok(native16timer.includes('SV="S5T_x0023_2S"'));
const off16=fs.readFileSync(__dirname+'/sources/decoded-original/0164-FlgNet.xml','utf8');assert.match(off16,/<Wire UId="31">\s*<PCon UId="794" PinName="out" \/>\s*<PCon UId="539" PinName="in" \/>/);
assert.ok(p16.control_reference.text_refs.every(r=>r.evidence==='backup_search_index_text_not_compiled_or_native_instruction_listing'));
for(const [f,h] of Object.entries(p16.source_hashes))assert.equal(crypto15.createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);
for(const loc of p16.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
assert.deepEqual(plain(standard.sections.map(([section])=>standard.items(data,'P16',section).length)),[3,4,16,5,4,5,5]);
for(const [section] of standard.sections)for(const item of standard.items(data,'P16',section)){const html=standard.render(data,'P16',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(html.includes('standard-content-title'));assert.ok(!html.includes('undefined'));}
const fn02Control=standard.render(data,'P16',{bc01Section:'control',bc01Item:'regulation',bc01Text:'standard',bc01Find:''});assert.ok(fn02Control.includes('원본 제어기 실행명령 근거는 미확보'));assert.ok(fn02Control.includes('FN04_Current'));assert.ok(fn02Control.includes('PID하한35'));
const schema16=data.repair_record_forms.profiles.find(p=>p.key==='P16');const note16={...fn01Note,id:'qa-fn02',equipment:'P16',repair_observation:plain(repair.collect(schema16,{first_symptom:'QA FN02',[schema16.signals[0].id+'_value']:'0'}))};
assert.deepEqual(plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([fn01Note,note16],data,'2026-10-11T06:00:00Z','P16')),store.decodeNotes,valid,schema16)).notes,[note16]);
assert.throws(()=>tools.parseBackup(JSON.stringify(tools.backupEnvelope([{...note16,repair_observation:{...note16.repair_observation,equipment:'FN02'}}],data,'2026-10-11T06:00:00Z','P16')),store.decodeNotes,valid,schema16));
assert.notEqual(tools.referenceContext(data,'P16').source_bundle_sha256,p15.source_bundle_sha256);

const p17=standard.profile(data,'P17');assert.ok(p17,'FN03 profile is required in v1.7.0');
assert.deepEqual(plain(p17.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='FN03'));
assert.deepEqual(plain(p17.alarm),readRegister('alarm-recovery.json').profiles.find(p=>p.id==='FN03'));
assert.equal(p17.regulation,null);assert.equal(p17.type,'motor_softstarter');
assert.equal(p17.specification.direct_rules.length,14);assert.deepEqual(p17.specification.direct_rules.filter(r=>r.opaque).map(r=>r.rule_id),['1031:1823','1051:2952']);
assert.equal(p17.alarm.timers.length,2);assert.deepEqual(p17.alarm.timers.map(t=>[t.uid,t.name,t.preset.literal]),[['854','Tag_66','S5T#35S'],['908','Tag_66','S5T#35S']]);
const inv17=p17.alarm.alarms.find(a=>a.name==='Allarm.FN03_INV').actions.find(a=>a.gate==='SCoil');assert.equal(inv17.uid,'856');assert.ok(!JSON.stringify(inv17.condition).includes('Tag_66'));
const fault17=p17.alarm.alarms.find(a=>a.name==='Allarm.FN_03_FAULT').actions.find(a=>a.gate==='SCoil');assert.ok(JSON.stringify(fault17.condition).includes('Tag_66'));
assert.deepEqual(p17.source_pairs.map(p=>p.path),['networks/network-1954.html#gme-fn03-part-749','networks/network-1801.html#gme-fn03-part-858','networks/network-1801.html#gme-fn03-part-855']);
const native17=fs.readFileSync(__dirname+'/sources/decoded-original/0436-FlgNet.xml','utf8');
assert.match(native17,/<Part UId="858" Gate="Contact">\s*<Negated PinName="operand" \/>/);assert.match(native17,/<Part UId="855" Gate="Contact">\s*<Negated PinName="operand" \/>/);
assert.match(native17,/<Wire UId="887">\s*<OCon UId="869" \/>\s*<PCon UId="854" PinName="value" \/>/);assert.match(native17,/<Wire UId="915">\s*<OCon UId="911" \/>\s*<PCon UId="908" PinName="value" \/>/);
const time17=native2s.split('</LiteralConstant>').find(s=>s.includes('RID="325"'));assert.ok(time17.includes('NID="23" UID="869"'));assert.ok(time17.includes('NID="23" UID="911"'));assert.ok(time17.includes('SV="S5T_x0023_35S"'));
const trace17=readRegister('signal-trace.json').devices.find(p=>p.id==='FN03');assert.deepEqual(plain(p17.signal_trace.signals.slice(0,trace17.signals.length)),trace17.signals);
assert.deepEqual(p17.signal_trace.signals.slice(-2).map(s=>[s.name,s.addresses]),[['Memo_M25_Running',['%M180.1']],['FP_M25_Run',['%M180.2']]]);
const decl17=fs.readFileSync(__dirname+'/sources/decoded-original/0658-IdentXmlPart.xml','utf8');
for(const signal of p17.signal_trace.signals.slice(-2)){
 const xml=decl17.match(new RegExp('<SimpleAccess><ID N="'+signal.name+'"[^>]*>[\\s\\S]*?</SimpleAccess>'))?.[0];assert.ok(xml,signal.name);
 for(const u of signal.usages){const c=xml.match(new RegExp('<C NID="23" UID="'+u.oref+'"[^>]*/>'))?.[0];assert.ok(c,u.oref);assert.equal(u.declarations[0].kind,'SimpleAccess');assert.equal(u.declarations[0].access_kind,c.match(/AK="([^"]+)"/)?.[1]||null);}
}
assert.ok(p17.control_reference.native_refs.find(r=>r.rule_id==='1801:73').opaque);assert.ok(p17.specification.inputs.every(r=>r['자료형']==='bool'));assert.equal(p17.specification.outputs.length,1);
for(const [f,h] of Object.entries(p17.source_hashes))assert.equal(crypto15.createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);
for(const loc of p17.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
assert.deepEqual(plain(standard.sections.map(([section])=>standard.items(data,'P17',section).length)),[3,4,15,3,4,5,5]);
for(const [section] of standard.sections)for(const item of standard.items(data,'P17',section)){const html=standard.render(data,'P17',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(html.includes('standard-content-title'));assert.ok(!html.includes('undefined'));}
const control17=standard.render(data,'P17',{bc01Section:'control',bc01Item:'regulation',bc01Text:'standard',bc01Find:''});for(const text of ['TOR5','RUN4','두 타이머를70초로 합산','Tag_66 접점이 없습니다','전용 아날로그','110Vac'])assert.ok(control17.includes(text),text);
const schema17=data.repair_record_forms.profiles.find(p=>p.key==='P17');assert.equal(schema17.signals.length,4);const note17={...fn01Note,id:'qa-fn03',equipment:'P17',repair_observation:plain(repair.collect(schema17,{first_symptom:'QA FN03',[schema17.signals[0].id+'_value']:'0'}))};
assert.deepEqual(plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note16,note17],data,'2026-10-11T06:00:00Z','P17')),store.decodeNotes,valid,schema17)).notes,[note17]);
assert.throws(()=>tools.parseBackup(JSON.stringify(tools.backupEnvelope([{...note17,repair_observation:{...note17.repair_observation,equipment:'FN03'}}],data,'2026-10-11T06:00:00Z','P17')),store.decodeNotes,valid,schema17));
assert.notEqual(tools.referenceContext(data,'P17').source_bundle_sha256,p16.source_bundle_sha256);

const p18=standard.profile(data,'P18');assert.ok(p18,'FN06 profile is required in v1.8.0');
assert.deepEqual(plain(p18.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='FN06'));
assert.deepEqual(plain(p18.alarm),readRegister('alarm-recovery.json').profiles.find(p=>p.id==='FN06'));
assert.equal(p18.type,'motor_directstarter');assert.equal(p18.regulation,null);
assert.equal(p18.specification.direct_rules.length,9);assert.deepEqual(p18.specification.direct_rules.filter(r=>r.opaque).map(r=>r.rule_id),['1032:1877','1051:2955']);
assert.deepEqual(p18.control_reference.native_refs.map(r=>r.rule_id),['1843:554','1844:898','1847:897','1955:772']);
assert.deepEqual(p18.alarm.alarms.map(a=>a.name),['Allarm.MBVA01_FAULT']);
assert.deepEqual(p18.alarm.timers.map(t=>[t.uid,t.name,t.preset.literal]),[['817','Tag_67','S5T#2S']]);
assert.deepEqual(p18.source_pairs.map(p=>p.path),['networks/network-1955.html#gme-fn06-part-776','networks/network-1802.html#gme-fn06-part-866']);
const native18=f=>fs.readFileSync(__dirname+'/sources/decoded-original/'+f,'utf8');
const wire18=(xml,id,endpoints)=>{const w=xml.match(new RegExp('<Wire UId="'+id+'">[\\s\\S]*?</Wire>'))?.[0];assert.ok(w,id);for(const e of endpoints)assert.ok(w.includes(e),id+' '+e);};
const alarm18=native18('0437-FlgNet.xml');
assert.match(alarm18,/<Part UId="866" Gate="Contact">\s*<Negated PinName="operand" \/>/);
wire18(alarm18,'841',['<OCon UId="831" />','<PCon UId="817" PinName="value" />']);
wire18(alarm18,'842',['<OCon UId="832" />','<PCon UId="817" PinName="operand" />']);
wire18(alarm18,'21',['<PCon UId="866" PinName="out" />','<PCon UId="817" PinName="in" />']);
wire18(alarm18,'846',['<OCon UId="835" />','<PCon UId="823" PinName="operand" />']);
wire18(alarm18,'851',['<OCon UId="838" />','<PCon UId="828" PinName="operand" />']);
assert.ok(timerDeclaration.includes('NID="24" UID="831"'));
const timer18=native18('0658-IdentXmlPart.xml').match(/<SimpleAccess><ID N="Tag_67"[^>]*>[\s\S]*?<\/SimpleAccess>/)?.[0];
for(const text of ['RID="99"','AO="91"','R="Timer"','NID="24" UID="832" OID="45" AK="Write"','NID="24" UID="833"'])assert.ok(timer18.includes(text),text);
const request18=native18('0257-FlgNet.xml');
for(const uid of ['22','802'])assert.match(request18,new RegExp('<Part UId="'+uid+'" Gate="Contact">\\s*<Negated PinName="operand" />'));
wire18(request18,'799',['<PCon UId="798" PinName="out" />','<PCon UId="767" PinName="in1" />']);
wire18(request18,'24',['<PCon UId="22" PinName="out" />','<PCon UId="802" PinName="in" />']);
wire18(request18,'803',['<PCon UId="802" PinName="out" />','<PCon UId="767" PinName="in2" />']);
wire18(request18,'789',['<PCon UId="767" PinName="out" />','<PCon UId="772" PinName="in" />']);
wire18(request18,'805',['<PCon UId="804" PinName="out" />','<PCon UId="776" PinName="in" />']);
assert.equal(p18.specification.direct_rules.find(r=>r.rule_id==='1955:772')['정적 조건식'],'((ON AND Allarm.MBVA01_FAULT) OR ((ON AND NOT [Inputs.RD01 run]) AND NOT [UNDER TESTING]))');
const burner18=native18('0174-FlgNet.xml');
wire18(burner18,'53',['<PCon UId="36" PinName="out" />','<PCon UId="38" PinName="in1" />']);
wire18(burner18,'45',['<PCon UId="228" PinName="out" />','<PCon UId="38" PinName="in2" />']);
const hours18=native18('0320-FlgNet.xml');assert.match(hours18,/<Part UId="1874" Gate="Move">/);
wire18(hours18,'1902',['<OCon UId="1888" />','<PCon UId="1874" PinName="in" />']);
wire18(hours18,'1903',['<PCon UId="1874" PinName="out1" />','<OCon UId="1889" />']);
wire18(hours18,'1904',['<PCon UId="1874" PinName="eno" />','<PCon UId="1877" PinName="en" />']);
const word18=native18('0397-FlgNet.xml');
assert.match(word18,/<Part UId="35" Gate="Move" DisableENO="true">/);
wire18(word18,'39',['<OCon UId="36" />','<PCon UId="35" PinName="in" />']);
wire18(word18,'40',['<PCon UId="35" PinName="out1" />','<OCon UId="37" />']);
wire18(word18,'41',['<PCon UId="27" PinName="eno" />','<PCon UId="35" PinName="en" />']);
const inputWord18=native18('0627-IdentXmlPart.xml').match(/<SimpleAccess><ID N="Tag_180"[^>]*>[\s\S]*?<\/SimpleAccess>/)?.[0];
for(const text of ['RID="10"','NID="1" UID="36"','T="Word:','AO="32"','R="Input"'])assert.ok(inputWord18?.includes(text),text);
const dbWord18=native18('0629-IdentXmlPart.xml').match(/<GlobalAccess><ID N="" S="Global" RID="11"[^>]*>[\s\S]*?<\/GlobalAccess>/)?.[0];
for(const text of ['NID="1" UID="37" AK="Write"','T="Word:','AO="32"','BIRID="4"'])assert.ok(dbWord18?.includes(text),text);
for(const [file,rid] of [['0628-IdentXmlPart.xml','4'],['0655-IdentXmlPart.xml','247']]){
 const dep=native18(file).match(new RegExp('<DepDBBlock><ID N="Inputs" S="Global" RID="'+rid+'"[^>]*>[\\s\\S]*?</DepDBBlock>'))?.[0];
 assert.ok(dep?.includes('TOD N="13"')&&dep.includes('CID="638561979615757134"'),file);
}
const response18=native18('0657-IdentXmlPart.xml').match(/<GlobalAccess><ID N="" S="Global" RID="291"[^>]*>[\s\S]*?<\/GlobalAccess>/)?.[0];
for(const text of ['NID="24" UID="867"','AO="35"','N="FEEDBACKMOTOR FN-06"','BO="35"','BIRID="247"'])assert.ok(response18?.includes(text),text);
const call18=native18('0030-FlgNet.xml');assert.match(call18,/<Part UId="37" Gate="Contact"><Negated PinName="operand" \/>/);
wire18(call18,'42',['<PCon UId="25" PinName="eno" />','<PCon UId="37" PinName="in" />']);
wire18(call18,'43',['<PCon UId="37" PinName="out" />','<PCon UId="28" PinName="en" />']);
wire18(call18,'44',['<OCon UId="45" />','<PCon UId="37" PinName="operand" />']);
assert.ok(p18.control_reference.native.includes(1070)&&p18.control_reference.native.includes(1613));
for(const [f,h] of Object.entries(p18.source_hashes))assert.equal(crypto15.createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);
for(const loc of p18.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
assert.deepEqual(plain(standard.sections.map(([section])=>standard.items(data,'P18',section).length)),[3,4,10,2,3,5,5]);
for(const [section] of standard.sections)for(const item of standard.items(data,'P18',section)){const html=standard.render(data,'P18',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(html.includes('standard-content-title'));assert.ok(!html.includes('undefined'));}
const control18=standard.render(data,'P18',{bc01Section:'control',bc01Item:'regulation',bc01Text:'standard',bc01Find:''});
for(const text of ['M26','MBVA01_FAULT','RD01 가지','HOUR Move1','원인 해소 접점은 없습니다','네 대상 선언은 미해석','보존 simulation1084'])assert.ok(control18.includes(text),text);
const schema18=data.repair_record_forms.profiles.find(p=>p.key==='P18');assert.equal(schema18.signals.length,4);
const note18={...fn01Note,id:'qa-fn06',equipment:'P18',repair_observation:plain(repair.collect(schema18,{first_symptom:'QA FN06',[schema18.signals[0].id+'_value']:'0'}))};
assert.deepEqual(plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note17,note18],data,'2026-10-11T06:00:00Z','P18')),store.decodeNotes,valid,schema18)).notes,[note18]);
assert.throws(()=>tools.parseBackup(JSON.stringify(tools.backupEnvelope([{...note18,repair_observation:{...note18.repair_observation,equipment:'FN06'}}],data,'2026-10-11T06:00:00Z','P18')),store.decodeNotes,valid,schema18));
assert.notEqual(tools.referenceContext(data,'P18').source_bundle_sha256,p17.source_bundle_sha256);

const p08=standard.profile(data,'P08');assert.ok(p08,'MC04 profile required');
assert.deepEqual(plain(p08.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='MC04'));
assert.deepEqual(plain(p08.alarm),readRegister('alarm-recovery.json').profiles.find(p=>p.id==='MC04'));
assert.equal(p08.specification.direct_rules.length,18);assert.equal(p08.regulation,null);
assert.equal(p08.alarm.timers.length,1);assert.equal(p08.alarm.timers[0].name,'Tag_57');assert.equal(p08.alarm.timers[0].preset.literal,'S5T#5S');assert.equal(p08.alarm.alarms.length,2);
assert.deepEqual(p08.control_reference.native_refs.map(r=>r.rule_id),['1843:460','1844:799','1847:954','1941:340']);
assert.equal(p08.specification.direct_rules.find(r=>r.rule_id==='1941:340')['정적 조건식'],'((ON AND Allarm.MC_04_FAULT) OR (ON AND Allarm.MC04_INV) OR ((ON AND NOT [Inputs.VS01 run]) AND NOT [Allarm.Maintenance_ON]))');
const r08=native18('0247-FlgNet.xml');for(const u of ['26','380'])assert.match(r08,new RegExp('<Part UId="'+u+'" Gate="Contact">\\s*<Negated PinName="operand" />'));
wire18(r08,'29',['<PCon UId="380" PinName="out" />','<PCon UId="333" PinName="in3" />']);wire18(r08,'365',['<OCon UId="352" />','<PCon UId="344" PinName="operand" />']);
const t08=native18('0656-IdentXmlPart.xml').split('</LiteralConstant>').find(s=>s.includes('RID="175"'));for(const x of ['NID="12" UID="451"','S5T_x0023_5S','V="1280"'])assert.ok(t08.includes(x));
const alarm08=native18('0428-FlgNet.xml');wire18(alarm08,'34',['<PCon UId="32" PinName="out" />','<PCon UId="437" PinName="in" />']);assert.match(alarm08,/<Part UId="500" Gate="Contact">\s*<Negated PinName="operand" \/>/);
const off08=native18('0658-IdentXmlPart.xml').match(/<SimpleAccess><ID N="OFF"[^>]*>[\s\S]*?<\/SimpleAccess>/)?.[0];assert.ok(off08?.includes('RID="46"')&&off08.includes('NID="13" UID="35"'));
const speed08=native18('0474-FlgNet.xml');wire18(speed08,'55',['<PCon UId="27" PinName="out" />','<OCon UId="39" />']);
const spare08=native18('0664-IdentXmlPart.xml').match(/<SimpleAccess><ID N="102A5_SPARE3"[^>]*>[\s\S]*?<\/SimpleAccess>/)?.[0];for(const x of ['RID="145"','NID="18" UID="39" AK="Write"','AO="2352"','R="Output"','T="Word:'])assert.ok(spare08.includes(x),x);
const mul08=native18('0661-IdentXmlPart.xml').split('</LiteralConstant>').find(s=>s.includes('RID="16"'));assert.ok(mul08.includes('NID="18" UID="38"')&&mul08.includes('V="272"'));
const current08=native18('0678-IdentXmlPart.xml').match(/<SimpleAccess><ID N="MV04_M18A"[^>]*>[\s\S]*?<\/SimpleAccess>/)?.[0];for(const x of ['RID="472"','NID="52" UID="26"','AO="2592"','R="Input"','SAM="Peripherie"','T="Int:'])assert.ok(current08.includes(x),x);
wire18(native18('0526-FlgNet.xml'),'35',['<OCon UId="26" />','<PCon UId="22" PinName="Analog_input" />']);
for(const [part,source,outWire,sourceRef,destRef] of [['22','23','24','25','26'],['42','52','54','45','46']]){assert.match(word18,new RegExp('<Part UId="'+part+'" Gate="Move" DisableENO="true">'));wire18(word18,source,['<OCon UId="'+sourceRef+'" />','<PCon UId="'+part+'" PinName="in" />']);wire18(word18,outWire,['<PCon UId="'+part+'" PinName="out1" />','<OCon UId="'+destRef+'" />']);}
const maintenance08=native18('0604-IdentXmlPart.xml').match(/<GlobalAccess><ID N="" S="Global" RID="6"[^>]*>[\s\S]*?<\/GlobalAccess>/)?.[0];for(const x of ['NID="1" UID="41" OID="9" AK="Write"','NID="11" UID="381"','N="Allarm"','N="Maintenance_ON"','AO="61"'])assert.ok(maintenance08.includes(x),x);
wire18(native18('0237-FlgNet.xml'),'50',['<PCon UId="49" PinName="out" />','<PCon UId="34" PinName="in" />','<PCon UId="36" PinName="in" />']);
for(const [f,h] of Object.entries(p08.source_hashes))assert.equal(crypto15.createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);
for(const loc of p08.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
assert.deepEqual(plain(standard.sections.map(([section])=>standard.items(data,'P08',section).length)),[3,4,19,5,4,5,5]);
for(const [section] of standard.sections)for(const item of standard.items(data,'P08',section)){const html=standard.render(data,'P08',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(html.includes('standard-content-title'));assert.ok(!html.includes('undefined'));}
const html08=standard.render(data,'P08',{bc01Section:'control',bc01Item:'regulation',bc01Text:'standard',bc01Find:''});for(const x of ['MV04_M18A','OFF','VS01 가지','102A5_SPARE3','HOUR+1이아닙니다','8대상'])assert.ok(html08.includes(x),x);
const schema08=data.repair_record_forms.profiles.find(p=>p.key==='P08');assert.equal(schema08.signals.length,5);
const note08={...fn01Note,id:'qa-mc04',equipment:'P08',repair_observation:plain(repair.collect(schema08,{first_symptom:'QA MC04',[schema08.signals[0].id+'_value']:'0'}))};assert.deepEqual(plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note18,note08],data,'2026-10-11T06:10:00Z','P08')),store.decodeNotes,valid,schema08)).notes,[note08]);assert.notEqual(tools.referenceContext(data,'P08').source_bundle_sha256,p18.source_bundle_sha256);

const p09=standard.profile(data,'P09');assert.ok(p09);
assert.deepEqual(plain(p09.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='VS01'));
assert.deepEqual(plain(p09.alarm),readRegister('alarm-recovery.json').profiles.find(p=>p.id==='VS01'));assert.equal(p09.regulation,null);
assert.equal(p09.specification.direct_rules.length,16);assert.equal(p09.alarm.alarms.length,2);assert.equal(p09.alarm.timers.length,1);assert.equal(p09.alarm.timers[0].preset.literal,'S5T#2S');
assert.deepEqual(p09.control_reference.native_refs.map(r=>r.rule_id),['1843:456','1844:786','1847:975','1943:377']);
for(const [id,value] of [['1943:377','((ON AND Allarm.VS_01_FAULT) OR (ON AND Allarm.VS01_INV))'],['1944:425','(((OFF AND NOT [Flag.M_VS_01]) AND NOT [Inputs.VS01 run]) AND NOT [Allarm.VS_01_FAULT])'],['1944:431','((OFF AND Flag.M_VS_01) OR (OFF AND Allarm.VS_01_FAULT) OR (OFF AND Allarm.VS01_INV))'],['1944:444','(((OFF AND NOT [Inputs.VS01 run]) AND Start VS01 BRAKE) AND Tag_117)'],['1050:2884','Tag_48']])assert.equal(p09.specification.direct_rules.find(r=>r.rule_id===id)['정적 조건식'],value);
const brake09=native18('0249-FlgNet.xml');assert.match(brake09,/<Part UId="439" Gate="SdCoil"/);wire18(brake09,'494',['<PCon UId="493" PinName="out" />','<PCon UId="439" PinName="in" />','<PCon UId="495" PinName="in" />']);wire18(brake09,'496',['<PCon UId="495" PinName="out" />','<PCon UId="444" PinName="in" />']);
for(const [rid,name,ao,area] of [['74','Start VS01 BRAKE','88','Memory'],['77','Tag_117','69','Timer'],['78','Braking VS01','397','Output']]){const d=native18('0602-IdentXmlPart.xml').match(new RegExp('<SimpleAccess><ID N="'+name+'"[^>]*>[\\s\\S]*?</SimpleAccess>'))?.[0];for(const x of ['RID="'+rid+'"','AO="'+ao+'"','R="'+area+'"'])assert.ok(d.includes(x),x);}
for(const [file,rid,uid] of [['0656','28','559'],['0606','76','455']]){const d=native18(file+'-IdentXmlPart.xml').split('</LiteralConstant>').find(s=>s.includes('RID="'+rid+'"'));for(const x of ['UID="'+uid+'"','SV="S5T_x0023_2S"','V="512"'])assert.ok(d.includes(x));}
const t09=native18('0658-IdentXmlPart.xml').match(/<SimpleAccess><ID N="Tag_59"[^>]*>[\s\S]*?<\/SimpleAccess>/)?.[0];for(const x of ['RID="66"','NID="16" UID="560"','AO="60"','R="Timer"'])assert.ok(t09.includes(x));
wire18(native18('0337-FlgNet.xml'),'2926',['<PCon UId="2925" PinName="out" />','<PCon UId="2884" PinName="en" />']);wire18(native18('0313-FlgNet.xml'),'1470',['<OCon UId="1456" />','<PCon UId="1442" PinName="in" />']);
assert.deepEqual(p09.source_pairs.map(p=>p.path),['networks/network-1943.html#gme-vs01-part-381','networks/network-1794.html#gme-vs01-part-604','networks/network-1794.html#gme-vs01-part-608']);
for(const [f,h] of Object.entries(p09.source_hashes))assert.equal(crypto15.createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);
for(const loc of p09.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
assert.deepEqual(plain(standard.sections.map(([section])=>standard.items(data,'P09',section).length)),[3,4,17,3,4,5,5]);
for(const [section] of standard.sections)for(const item of standard.items(data,'P09',section)){const h=standard.render(data,'P09',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(h.includes('standard-content-title'));assert.ok(!h.includes('undefined'));}
const h09=standard.render(data,'P09',{bc01Section:'control',bc01Item:'regulation',bc01Text:'standard',bc01Find:''});for(const x of ['M11.0','Q49.5','T60','T69','NOT INV가없고','HOUR+1이아닙니다','8바인딩','두모터'])assert.ok(h09.includes(x),x);
const schema09=data.repair_record_forms.profiles.find(p=>p.key==='P09');assert.equal(schema09.signals.length,4);const note09={...fn01Note,id:'qa-vs01',equipment:'P09',repair_observation:plain(repair.collect(schema09,{first_symptom:'QA VS01',[schema09.signals[0].id+'_value']:'0'}))};assert.deepEqual(plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note08,note09],data,'2026-10-11T06:30:00Z','P09')),store.decodeNotes,valid,schema09)).notes,[note09]);assert.notEqual(tools.referenceContext(data,'P09').source_bundle_sha256,p08.source_bundle_sha256);


const p05=standard.profile(data,'P05');assert.ok(p05);assert.equal(p05.type,'pneumatic_double_gate');assert.equal(p05.specification.direct_rules.length,39);assert.equal(p05.source_pairs.length,8);
assert.deepEqual(plain(standard.sections.map(([s])=>standard.items(data,'P05',s).length)),[3,4,40,8,6,5,5]);
assert.deepEqual(plain(p05.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='PV01'));assert.deepEqual(plain(p05.alarm),readRegister('alarm-recovery.json').profiles.find(p=>p.id==='PV01'));
assert.deepEqual(p05.alarm.timers.map(t=>[t.uid,t.preset.literal]),[['1453','S5T#4S'],['1471','S5T#4S'],['1517','S5T#7S'],['1535','S5T#7S']]);
const pvXML=f=>fs.readFileSync(__dirname+'/sources/decoded-original/'+f+'-FlgNet.xml','utf8');
assert.match(pvXML('0279'),/<Part UId="418" Gate="Contact" \/>/);assert.match(pvXML('0279'),/<ORef UId="389" RefId="48" \/>/);assert.match(pvXML('0279'),/<Wire UId="419">\s*<PCon UId="418" PinName="out" \/>\s*<PCon UId="372" PinName="in4" \/>/);
for(const [wire,contact,move]of [['562','561','345'],['568','567','401']])assert.match(pvXML('0277'),new RegExp('<Wire UId="'+wire+'">\\s*<PCon UId="'+contact+'" PinName="out" \\/>\\s*<PCon UId="'+move+'" PinName="en" \\/>'));
const pvDecl=(f,rid)=>fs.readFileSync(__dirname+'/sources/decoded-original/'+f+'-IdentXmlPart.xml','utf8').split(/<(?=SimpleAccess>|GlobalAccess>|LiteralConstant>|DepDBBlock>)/).find(s=>s.includes(' RID="'+rid+'"'));
for(const [rid,region,offset]of [['47','Memory','645'],['48','Memory','1'],['49','Output','43'],['50','Output','42'],['124','Input','70'],['126','Input','71']]){const t=pvDecl('0607',rid);assert.ok(t.includes('AO="'+offset+'"'));assert.ok(t.includes('R="'+region+'"'));}
assert.ok(pvDecl('0610','130').includes('SV="false" V="0"'));assert.ok(pvDecl('0610','24').includes('SV="S5T_x0023_1S"'));assert.ok(pvDecl('0656','320').includes('SV="S5T_x0023_7S"'));assert.ok(pvDecl('0656','322').includes('SV="S5T_x0023_4S"'));
assert.match(pvXML('0397'),/<Wire UId="55">\s*<OCon UId="47" \/>\s*<PCon UId="43" PinName="in" \/>/);assert.match(pvXML('0397'),/<Wire UId="57">\s*<PCon UId="43" PinName="out1" \/>\s*<OCon UId="48" \/>/);assert.ok(pvDecl('0627','15').includes('AO="64"'));assert.ok(pvDecl('0629','16').includes('BIRID="4"'));assert.ok(pvDecl('0628','4').includes('N="13"'));
for(const f of ['0060','0061','0578','0607','0608','0609','0610','0623','0624','0626','0627','0628','0629','0631','0655'])assert.ok(p05.source_hashes['sources/decoded-original/'+f+'-IdentXmlPart.xml']);
for(const [f,h]of Object.entries(p05.source_hashes))assert.equal(crypto15.createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);
for(const loc of p05.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
for(const [section]of standard.sections)for(const item of standard.items(data,'P05',section)){const html=standard.render(data,'P05',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(!html.includes('undefined'));assert.ok(html.includes('standard-content-title'));}
const pvControl=standard.render(data,'P05',{bc01Section:'control',bc01Item:'regulation',bc01Text:'standard',bc01Find:''});for(const s of ['M80.5','OFF Contact418','1초','SEC은Bool','HMI','17바인딩','DB13 Word8'])assert.ok(pvControl.includes(s),s);
const schema05=data.repair_record_forms.profiles.find(p=>p.key==='P05');const note05={...fn01Note,id:'qa-pv01',equipment:'P05',repair_observation:plain(repair.collect(schema05,{first_symptom:'QA PV01',[schema05.signals[0].id+'_value']:'0'}))};const parsed05=plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note09,note05],data,'2026-10-11T07:00:00Z','P05')),store.decodeNotes,valid,schema05));assert.deepEqual(parsed05.notes,[note05]);assert.equal(parsed05.skipped,1);assert.notEqual(tools.referenceContext(data,'P05').source_bundle_sha256,p09.source_bundle_sha256);

const p07=standard.profile(data,'P07');assert.ok(p07);assert.equal(p07.type,'pneumatic_double_gate');
assert.deepEqual(plain(p07.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='PV02'));
assert.deepEqual(plain(p07.alarm),readRegister('alarm-recovery.json').profiles.find(p=>p.id==='PV02'));
assert.deepEqual(p07.alarm.timers.map(t=>[t.uid,t.preset.literal]),[['1581','S5T#7S'],['1599','S5T#7S'],['1645','S5T#7S'],['1663','S5T#7S']]);
assert.deepEqual(plain(standard.sections.map(([s])=>standard.items(data,'P07',s).length)),[3,4,40,8,6,5,5]);
assert.deepEqual(p07.source_pairs.map(p=>p.path),['networks/network-1920.html#gme-pv02-part-724','networks/network-1920.html#gme-pv02-part-717','networks/network-1923.html#gme-pv02-part-23','networks/network-1923.html#gme-pv02-part-30','networks/network-1924.html#gme-pv02-part-23','networks/network-1924.html#gme-pv02-part-30','networks/network-1919.html#gme-pv02-part-686','networks/network-1919.html#gme-pv02-part-690']);
for(const [f,h]of Object.entries(p07.source_hashes))assert.equal(crypto15.createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);
for(const loc of p07.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
const schema07=data.repair_record_forms.profiles.find(p=>p.key==='P07');assert.equal(schema07.signals.length,8);
const note07={...fn01Note,id:'qa-pv02',equipment:'P07',repair_observation:plain(repair.collect(schema07,{first_symptom:'QA PV02',[schema07.signals[0].id+'_value']:'0'}))};
const parsed07=plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note05,note07],data,'2026-10-11T07:30:00Z','P07')),store.decodeNotes,valid,schema07));assert.deepEqual(parsed07.notes,[note07]);assert.equal(parsed07.skipped,1);
assert.notEqual(tools.referenceContext(data,'P07').source_bundle_sha256,p05.source_bundle_sha256);
for(const [section]of standard.sections)for(const item of standard.items(data,'P07',section)){const html=standard.render(data,'P07',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(!html.includes('undefined'));assert.ok(html.includes('standard-content-title'));}
const schemas=data.repair_record_forms.profiles;
const allEnvelope=rows=>JSON.stringify(tools.unifiedBackupEnvelope(rows,data),null,2);
const parseAll=raw=>plain(tools.parseUnifiedBackup(raw,store.decodeNotes,valid,schemas));
const memo={id:'qa-catalog',equipment:'FN04',title:'Catalog separate context',text:'0',updated:'old',extra:{zero:0,blank:'',nil:null}};
assert.deepEqual(parseAll(allEnvelope([note,foreign,memo])).notes,plain([note,foreign,memo]));
assert.deepEqual(parseAll(allEnvelope([])).notes,[]);
const many=Array.from({length:1001},(_,i)=>({...memo,id:'many-'+i}));assert.equal(parseAll(allEnvelope(many)).total,1001);
const legacy={application:'GME All-in-One',note_id:note.id,title:note.title,updated:note.updated,observation:{...note.repair_observation,name:'original legacy name'}};
assert.equal(parseAll(JSON.stringify(legacy)).notes[0].name,'original legacy name');assert.ok(!Object.hasOwn(parseAll(JSON.stringify(legacy)).notes[0],'saved_with'));
const rawLegacy=JSON.stringify({schema_version:1,application:'GME All-in-One',notes:[memo]});assert.deepEqual(parseAll(rawLegacy).notes,[memo]);
for(const bad of [false,0,null])assert.throws(()=>parseAll(allEnvelope([{...memo,repair_observation:bad}])));
for(const rows of [[memo,memo],[{...memo,equipment:'NO-SUCH-KEY'}],[{...note,repair_observation:{...note.repair_observation,equipment:'FN04'}}]])assert.throws(()=>parseAll(allEnvelope(rows)));
assert.throws(()=>parseAll(JSON.stringify({...legacy,notes:[]})),/함께/);assert.throws(()=>parseAll(JSON.stringify({schema_version:1,application:'GME All-in-One',notes:{}})),/배열/);
assert.throws(()=>parseAll(rawLegacy.replace('"zero":0','"zero":1e400')),/숫자/);
const otherId={...memo,id:note.id},cross=plain(tools.planRestore([note],[otherId]));assert.throws(()=>tools.applyUnifiedRestore([note],cross,{0:'replace'},()=> 'new-copy'));assert.equal(tools.applyUnifiedRestore([note],cross,{0:'copy'},()=> 'new-copy').notes[1].equipment,'FN04');
const evidenceNote={...note,saved_with:{application_version:'old-version',source_bundle_sha256:'old-hash',unknown_evidence:'preserve'}};
const legacyReplace=plain(tools.applyUnifiedRestore([evidenceNote],tools.planRestore([evidenceNote],[changed]),{0:'replace'},()=> 'new-copy')).notes[0];
assert.ok(!Object.hasOwn(legacyReplace,'saved_with'));assert.deepEqual(legacyReplace.backup_restore_history[0].previous_saved_with,evidenceNote.saved_with);assert.equal(legacyReplace.future.retained,1);
const partial={...changed,saved_with:{application_version:'imported-version'}};const partialReplace=plain(tools.applyUnifiedRestore([evidenceNote],tools.planRestore([evidenceNote],[partial]),{0:'replace'},()=> 'new-copy')).notes[0];assert.deepEqual(partialReplace.saved_with,partial.saved_with);
const oldRows={...note,repair_observation:{...note.repair_observation,observations:Array.from({length:1000},(_,i)=>({id:'old-'+i,value:'0'}))}},newRows={...changed,repair_observation:{...changed.repair_observation,observations:Array.from({length:1000},(_,i)=>({id:'new-'+i,value:''}))}};
parseAll(allEnvelope([oldRows]));parseAll(allEnvelope([newRows]));const over=tools.applyUnifiedRestore([oldRows],tools.planRestore([oldRows],[newRows]),{0:'replace'},()=> 'new-copy');assert.throws(()=>parseAll(allEnvelope(over.notes)),/ID/);assert.equal(over.notes[0].repair_observation.observations.length,2000);
assert.deepEqual(plain(tools.unifiedBackupEnvelope([note,memo],data).generated_with.equipment_references.FN04.source_hashes),{});

const p19=standard.profile(data,'P19');assert.ok(p19,'MV01 profile required in v1.13.0');
assert.deepEqual(plain(p19.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='MV01'));assert.deepEqual(plain(p19.alarm),readRegister('alarm-recovery.json').profiles.find(p=>p.id==='MV01'));assert.deepEqual(plain(p19.regulation),readRegister('regulation-manual.json').loops.find(p=>p.id==='MV01'));
assert.equal(p19.type,'motorized_valve');assert.equal(p19.specification.direct_rules.length,16);assert.deepEqual(p19.specification.direct_rules.filter(r=>r.opaque).map(r=>r.rule_id),['1702:143','1703:25','1703:26']);assert.deepEqual(p19.alarm.timers.map(t=>[t.name,t.preset.literal]),[['Tag_92','S5T#150mS']]);assert.deepEqual(p19.alarm.alarms.map(a=>a.actions.map(x=>[x.network,x.uid])),[[[1226,'254'],[1226,'342'],[1714,'1598'],[1714,'1612']]]);
assert.deepEqual(plain(standard.sections.map(([section])=>standard.items(data,'P19',section).length)),[3,4,17,7,3,5,5]);assert.equal(p19.source_pairs[6].path,'networks/network-1756.html#gme-mv01-wire-75');
const mv19Control=standard.render(data,'P19',{bc01Section:'control',bc01Item:'regulation',bc01Text:'standard',bc01Find:''});for(const txt of ['S5T#150mS','W33>2000','W34<−2000','19핀','9핀','10실인수','INT#0','CH0.A','3.5~5A'])assert.ok(mv19Control.replaceAll('&gt;','>').replaceAll('&lt;','<').includes(txt),txt);
for(const [file,hash] of Object.entries(p19.source_hashes))assert.equal(require('node:crypto').createHash('sha256').update(fs.readFileSync(__dirname+'/'+file)).digest('hex'),hash,file);
const schema19=data.repair_record_forms.profiles.find(p=>p.key==='P19'),note19={...fn01Note,id:'qa-mv01',equipment:'P19',repair_observation:plain(repair.collect(schema19,{first_symptom:'QA MV01',[schema19.signals[0].id+'_value']:'0'}))};assert.equal(schema19.signals.length,7);assert.deepEqual(plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([fn01Note,note19],data,'2026-10-11T08:00:00Z','P19')),store.decodeNotes,valid,schema19)).notes,[note19]);assert.throws(()=>tools.parseBackup(JSON.stringify(tools.backupEnvelope([{...note19,repair_observation:{...note19.repair_observation,equipment:'P20'}}],data,'2026-10-11T08:00:00Z','P19')),store.decodeNotes,valid,schema19));assert.notEqual(tools.referenceContext(data,'P19').source_bundle_sha256,tools.referenceContext(data,'P07').source_bundle_sha256);

const p20=standard.profile(data,'P20');assert.ok(p20,'MV03 profile in v1.14.0');
assert.deepEqual(plain(p20.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='MV03'));assert.deepEqual(plain(p20.alarm),readRegister('alarm-recovery.json').profiles.find(p=>p.id==='MV03'));assert.deepEqual(plain(p20.regulation),readRegister('regulation-manual.json').loops.find(p=>p.id==='MV03'));
assert.equal(p20.specification.direct_rules.length,27);assert.deepEqual(p20.specification.direct_rules.filter(r=>r.opaque).map(r=>r.rule_id),['1707:44','1707:48']);assert.deepEqual(p20.alarm.timers.map(t=>[t.name,t.preset.literal]),[['Tag_94','S5T#150S']]);assert.equal(p20.alarm.timers[0].preset.value,150000);assert.deepEqual(p20.alarm.alarms.map(a=>a.actions.map(x=>[x.network,x.uid])),[[[1226,'286'],[1226,'350'],[1714,'1662'],[1714,'1676']]]);
assert.deepEqual(plain(standard.sections.map(([s])=>standard.items(data,'P20',s).length)),[3,4,28,7,3,5,5]);assert.equal(p20.source_pairs[6].path,'networks/network-1758.html#gme-mv03-wire-71');
const m20=n=>fs.readFileSync(__dirname+'/sources/decoded-original/'+n+'-FlgNet.xml','utf8');
assert.ok(m20('0159').includes('<PCon UId="281" PinName="value" />'));assert.ok(pvDecl('0571','83').includes('SV="S5T_x0023_150S"'));assert.ok(pvDecl('0571','83').includes('V="8528"'));
wire18(m20('0345'),'54',['<PCon UId="546" PinName="out" />','<PCon UId="53" PinName="in2" />']);wire18(m20('0345'),'31',['<PCon UId="539" PinName="out" />','<PCon UId="53" PinName="in1" />']);
wire18(m20('0184'),'29',['<PCon UId="28" PinName="out" />','<PCon UId="1670" PinName="in" />']);for(const uid of ['38','34'])assert.ok(pvDecl('0585','233').includes('UID="'+uid+'"'));
wire18(m20('0508'),'56',['<OCon UId="30" />','<PCon UId="22" PinName="SetCountValue" />']);assert.ok(m20('0508').includes('<ORef UId="30" />'));assert.ok(m20('0508').includes('<ORef UId="28" />'));
const c20=standard.render(data,'P20',{bc01Section:'control',bc01Item:'regulation',bc01Text:'standard',bc01Find:''}).replaceAll('&gt;','>').replaceAll('&lt;','<');for(const txt of ['S5T#150S','W29>3400','W30<−3400','21핀','10실인수','반대 방향 Q1.7/Q2.0 차단 접점은 없습니다','PIW320','0.25kW','2.2kW','NOT','INT#0'])assert.ok(c20.includes(txt),txt);
const path20=standard.render(data,'P20',{bc01Section:'circuits',bc01Item:'path-0',bc01Text:'standard',bc01Find:''});assert.ok(path20.includes('정정 근거:0345/1706'));assert.ok(!path20.includes('모드·반대 출력·리미트'));
for(const [f,h]of Object.entries(p20.source_hashes))assert.equal(require('node:crypto').createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);
for(const loc of p20.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
for(const [section]of standard.sections)for(const item of standard.items(data,'P20',section)){const h=standard.render(data,'P20',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(!h.includes('undefined'));assert.ok(h.includes('standard-content-title'));}
const schema20=data.repair_record_forms.profiles.find(p=>p.key==='P20'),note20={...fn01Note,id:'qa-mv03',equipment:'P20',repair_observation:plain(repair.collect(schema20,{first_symptom:'QA MV03',[schema20.signals[0].id+'_value']:'0'}))};assert.equal(schema20.signals.length,9);assert.deepEqual(plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note19,note20],data,'2026-10-11T08:30:00Z','P20')),store.decodeNotes,valid,schema20)).notes,[note20]);assert.throws(()=>tools.parseBackup(JSON.stringify(tools.backupEnvelope([{...note20,repair_observation:{...note20.repair_observation,equipment:'P19'}}],data,'2026-10-11T08:30:00Z','P20')),store.decodeNotes,valid,schema20));assert.notEqual(tools.referenceContext(data,'P20').source_bundle_sha256,p19.source_bundle_sha256);


const p21=standard.profile(data,'P21');assert.ok(p21,'MV06 profile in v1.15.0');
assert.deepEqual(plain(p21.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='MV06'));assert.deepEqual(plain(p21.alarm),readRegister('alarm-recovery.json').profiles.find(p=>p.id==='MV06'));assert.deepEqual(plain(p21.regulation),readRegister('regulation-manual.json').loops.find(p=>p.id==='MV06'));
assert.equal(p21.regulation.controller,null);assert.equal(p21.type,'motorized_valve_shared_inverter');assert.equal(p21.source_pairs.length,10);assert.equal(p21.source_pairs[9].path,'networks/network-1760.html#gme-mv06-wire-75');
const m21=n=>fs.readFileSync(__dirname+'/sources/decoded-original/'+n+'-FlgNet.xml','utf8');
// Verify polarity, branch sharing and actual native comparison, without evaluating PLC behavior.
assert.match(m21('0349'),/<Part UId="915" Gate="Contact">\s*<Negated PinName="operand" \/>/);wire18(m21('0349'),'27',['<OCon UId="28" />','<PCon UId="915" PinName="operand" />']);wire18(m21('0349'),'916',['<PCon UId="915" PinName="out" />','<PCon UId="931" PinName="in" />']);
assert.match(m21('0347'),/<Part UId="624" Gate="Le">/);assert.match(m21('0347'),/<Part UId="618" Gate="Ge">/);assert.ok(pvDecl('0620','186').includes('SV="_x002D_5"'));
const raw21=fs.readFileSync(__dirname+'/sources/decoded-original/0617-IdentXmlPart.xml','utf8').match(/<SimpleAccess><ID N="PSH02"[^>]*>[\s\S]*?<\/SimpleAccess>/)?.[0];assert.ok(raw21?.includes('AO="2288"')&&raw21.includes('R="Input"')&&raw21.includes('SAM="Peripherie"'));
assert.match(m21('0455'),/<Part UId="22" Gate="Contact">\s*<Negated PinName="operand" \/>/);wire18(m21('0455'),'25',['<PCon UId="22" PinName="out" />','<PCon UId="1818" PinName="in" />','<PCon UId="1827" PinName="in" />']);
assert.ok(pvDecl('0658','236').includes('UID="1838"')&&pvDecl('0658','236').includes('UID="44"'));assert.ok(pvDecl('0571','8').includes('SV="S5T_x0023_150MS"'));assert.ok(pvDecl('0571','8').includes('V="21"'));
assert.ok(m21('0510').includes('<ORef UId="30" />'));wire18(m21('0510'),'75',['<PCon UId="23" PinName="CountValue" />','<OCon UId="47" />']);wire18(m21('0516'),'1514',['<OCon UId="1489" />','<PCon UId="1454" PinName="in" />']);
const c21=standard.render(data,'P21',{bc01Section:'control',bc01Item:'regulation',bc01Text:'standard',bc01Find:''}).replaceAll('&gt;','>').replaceAll('&lt;','<');for(const t of ['≤−5','PIW286','!ON915','S5T#150MS','W19>2200','W20<−2200','CNTV4_100','21핀','10선언미해석','5–9','LS34/35','별개구간'])assert.ok(c21.includes(t),t);
const path21=standard.render(data,'P21',{bc01Section:'circuits',bc01Item:'path-0',bc01Text:'standard',bc01Find:''});assert.ok(path21.includes('부하접점5–9'));assert.ok(!path21.includes('접점1→9'));const open21=standard.render(data,'P21',{bc01Section:'circuits',bc01Item:'path-3',bc01Text:'standard',bc01Find:''});assert.ok(open21.includes('교정Reset 절차는확인되지'));assert.ok(!open21.includes('고장·교정 조건'));
for(const [f,h]of Object.entries(p21.source_hashes))assert.equal(require('node:crypto').createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);
for(const loc of p21.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
for(const [section]of standard.sections)for(const item of standard.items(data,'P21',section)){const h=standard.render(data,'P21',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(!h.includes('undefined'));assert.ok(h.includes('standard-content-title'));}
const schema21=data.repair_record_forms.profiles.find(p=>p.key==='P21'),note21={...fn01Note,id:'qa-mv06',equipment:'P21',repair_observation:plain(repair.collect(schema21,{first_symptom:'QA MV06',[schema21.signals[0].id+'_value']:'0'}))};assert.deepEqual(plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note20,note21],data,'2026-10-11T09:30:00Z','P21')),store.decodeNotes,valid,schema21)).notes,[note21]);assert.throws(()=>tools.parseBackup(JSON.stringify(tools.backupEnvelope([{...note21,repair_observation:{...note21.repair_observation,equipment:'P20'}}],data,'2026-10-11T09:30:00Z','P21')),store.decodeNotes,valid,schema21));assert.notEqual(tools.referenceContext(data,'P21').source_bundle_sha256,p20.source_bundle_sha256);

const p06=standard.profile(data,'P06');assert.ok(p06,'RD01 batch01 profile');
assert.deepEqual(plain(p06.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='RD01'));assert.deepEqual(plain(p06.alarm),readRegister('alarm-recovery.json').profiles.find(p=>p.id==='RD01'));assert.equal(p06.regulation,null);assert.equal(p06.control_reference.controller_evidence,null);
assert.equal(p06.specification.direct_rules.length,26);assert.equal(p06.specification.direct_rules.filter(r=>r['블록']==='simulation').length,2);assert.deepEqual(p06.specification.direct_rules.filter(r=>r.opaque).map(r=>r.rule_id),['1019:1175','1020:1229','1049:2825']);assert.deepEqual(p06.alarm.timers.map(t=>[t.name,t.preset.literal]),[['Tag_54','S5T#5S']]);
assert.deepEqual(plain(standard.sections.map(([section])=>standard.items(data,'P06',section).length)),[3,4,27,8,4,5,5]);
const rd06Draw=data.drawing_workspace.profiles.find(p=>p.key==='P06');assert.equal(rd06Draw.circuit.paths.length,8);assert.equal(rd06Draw.sheets.find(s=>s.id==='oem-22').page,23);assert.equal(p06.source_pairs[7].path,'networks/network-1938.html#gme-rd01-part-268');
const rawRD=readRegister('electrical-trace.json').devices.find(d=>d.id==='RD01');assert.equal(rawRD.paths.length,5);assert.ok(rawRD.paths[0].destination.includes('접점1→9'));
assert.ok(rd06Draw.circuit.paths[0].destination.includes('5/9'));assert.ok(rd06Draw.circuit.paths[7].nodes[0].includes('−0Vdc10.6'));assert.ok(rd06Draw.circuit.paths[7].nodes[0].includes('(21/5)'));assert.ok(rd06Draw.circuit.paths[7].nodes[1].includes('110Vac9.7'));
const rdXML=n=>fs.readFileSync(__dirname+'/sources/decoded-original/'+n+'-FlgNet.xml','utf8');
wire18(rdXML('0243'),'33',['<PCon UId="280" PinName="out" />','<PCon UId="35" PinName="in" />']);assert.match(rdXML('0243'),/<Part UId="35" Gate="Contact">\s*<Negated PinName="operand" \/>/);
assert.match(rdXML('0465'),/<Part UId="406" Gate="Lt">/);assert.match(rdXML('0465'),/<Part UId="414" Gate="Gt">/);wire18(rdXML('0465'),'453',['<PCon UId="422" PinName="out" />','<OCon UId="437" />']);
wire18(rdXML('0244'),'282',['<OCon UId="271" />','<PCon UId="257" PinName="value" />']);assert.ok(pvDecl('0656','175').includes('SV="S5T_x0023_5S"'));assert.ok(pvDecl('0656','28').includes('NID="9" UID="363"'));
const c06=standard.render(data,'P06',{bc01Section:'control',bc01Item:'regulation',bc01Text:'large',bc01Find:''});for(const t of ['SAM=None IW332','Peripherie PIW332','PQW290','SEC Bool0','HOUR Move1','5선언미결속','4미결속','S5T#5S','S5T#2S'])assert.ok(c06.includes(t),t);
for(const [f,h]of Object.entries(p06.source_hashes))assert.equal(require('node:crypto').createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);for(const loc of p06.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
for(const [section]of standard.sections)for(const item of standard.items(data,'P06',section)){const h=standard.render(data,'P06',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(!h.includes('undefined'));assert.ok(h.includes('standard-content-title'));}
const schema06=data.repair_record_forms.profiles.find(p=>p.key==='P06'),note06={...fn01Note,id:'qa-rd01',equipment:'P06',repair_observation:plain(repair.collect(schema06,{first_symptom:'QA RD01',[schema06.signals[0].id+'_value']:'0'}))};assert.equal(schema06.signals.length,5);assert.deepEqual(plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note21,note06],data,'2026-10-11T10:00:00Z','P06')),store.decodeNotes,valid,schema06)).notes,[note06]);assert.throws(()=>tools.parseBackup(JSON.stringify(tools.backupEnvelope([{...note06,repair_observation:{...note06.repair_observation,equipment:'P21'}}],data,'2026-10-11T10:00:00Z','P06')),store.decodeNotes,valid,schema06));assert.notEqual(tools.referenceContext(data,'P06').source_bundle_sha256,p21.source_bundle_sha256);

const p11=standard.profile(data,'P11');assert.ok(p11,'BR01 external interface profile');
assert.deepEqual(plain(p11.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='BR01'));assert.deepEqual(plain(p11.regulation),readRegister('regulation-manual.json').loops.find(p=>p.id==='BR01'));assert.equal(p11.control_reference.controller_evidence,null);assert.equal(readRegister('alarm-recovery.json').profiles.find(p=>p.id==='BR01'),undefined);
const burner11=readRegister('burner-interface.json');for(const g of p11.alarm.alarms)assert.deepEqual(plain(g.actions),burner11.actions.filter(a=>a.name===g.name));assert.deepEqual(plain(p11.alarm.timers),burner11.actions.filter(a=>a.gate==='SdCoil'));assert.equal(p11.alarm.alarms.find(g=>g.name==='Allarm.BURNER_START_FAULT').actions.some(a=>a.gate==='SCoil'),false);
const drawing11=data.drawing_workspace.profiles.find(p=>p.key==='P11');for(const path of drawing11.circuit.paths.slice(8,12)){assert.ok(path.nodes.some(n=>n.includes('접점5→9')));assert.ok(!path.nodes.some(n=>n.includes('접점1→9')));}assert.ok(drawing11.circuit.paths[12].nodes.some(n=>n.includes('단자1')));assert.ok(drawing11.circuit.paths[12].nodes.some(n=>n.includes('단자5')));assert.ok(drawing11.circuit.paths[12].destination.includes('S5T#4S'));assert.ok(drawing11.circuit.paths[12].destination.includes('3sec'));
wire18(rdXML('0182'),'631',['<OCon UId="620" />','<PCon UId="611" PinName="operand" />']);wire18(rdXML('0184'),'29',['<PCon UId="28" PinName="out" />','<PCon UId="1670" PinName="in" />']);assert.match(rdXML('0184'),/<Part UId="28" Gate="Contact">\s*<Negated PinName="operand" \/>/);assert.match(rdXML('0184'),/<Part UId="1670" Gate="Contact" \/>/);wire18(rdXML('0468'),'624',['<PCon UId="590" PinName="out" />','<OCon UId="606" />']);wire18(rdXML('0398'),'187',['<OCon UId="176" />','<PCon UId="170" PinName="in" />']);
assert.ok(fs.readFileSync(__dirname+'/sources/decoded-original/0586-IdentXmlPart.xml','utf8').includes('S5T_x0023_4S'));
const c11=standard.render(data,'P11',{bc01Section:'control',bc01Item:'regulation',bc01Text:'large',bc01Find:''});for(const t of ['literal77','정·부정직렬','3초','S5T#4S','PQW308','SAM=None QW308','PIW360','IW360 SAM=None','12 ORef','Set원천'])assert.ok(c11.includes(t),t);
for(const [f,h]of Object.entries(p11.source_hashes))assert.equal(crypto15.createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);for(const loc of p11.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));assert.ok(data.resources.includes('alarm-guides/BR01.html'));
for(const [section]of standard.sections)for(const item of standard.items(data,'P11',section)){const h=standard.render(data,'P11',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(!h.includes('undefined'));assert.ok(h.includes('standard-content-title'));}
const schema11=data.repair_record_forms.profiles.find(p=>p.key==='P11'),note11={...fn01Note,id:'qa-br01',equipment:'P11',repair_observation:plain(repair.collect(schema11,{first_symptom:'QA BR01',[schema11.signals[0].id+'_value']:'0'}))};assert.deepEqual(plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note06,note11],data,'2026-10-11T10:30:00Z','P11')),store.decodeNotes,valid,schema11)).notes,[note11]);assert.throws(()=>tools.parseBackup(JSON.stringify(tools.backupEnvelope([{...note11,repair_observation:{...note11.repair_observation,equipment:'P06'}}],data,'2026-10-11T10:30:00Z','P11')),store.decodeNotes,valid,schema11));assert.notEqual(tools.referenceContext(data,'P11').source_bundle_sha256,p06.source_bundle_sha256);

const p10=standard.profile(data,'P10');assert.ok(p10,'CC01 passive candidate');assert.equal(p10.type,'passive_body_candidate');assert.deepEqual(plain(p10.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='CC01'));
for(const k of ['inputs','outputs','internal','hmi','networks','direct_rules'])assert.deepEqual(plain(p10.specification[k]),[]);assert.deepEqual(plain(p10.signal_trace.signals),[]);assert.deepEqual(plain(p10.alarm.alarms),[]);assert.deepEqual(plain(p10.alarm.timers),[]);assert.equal(readRegister('alarm-recovery.json').profiles.find(p=>p.id==='CC01'),undefined);assert.equal(p10.regulation,null);assert.equal(p10.control_reference.controller_evidence,null);assert.deepEqual(plain(p10.control_reference.native),[1742,1751,1071,1658,1659]);
assert.deepEqual(plain(standard.sections.map(([section])=>standard.items(data,'P10',section).length)),[3,4,1,4,2,3,5]);
const drawing10=data.drawing_workspace.profiles.find(p=>p.key==='P10');assert.equal(drawing10.circuit.source_reference_only,true);assert.ok(drawing10.circuit.paths.every(p=>p.ownership_verified===false));assert.deepEqual(plain(p10.source_pairs.map(p=>p.path)),['networks/network-1742.html#gme-cc01-wire-391','networks/network-1071.html#gme-cc01-wire-88','networks/network-1751.html#gme-cc01-wire-590','networks/network-1071.html#gme-cc01-wire-184']);
for(const item of standard.items(data,'P10','io')){const h=standard.render(data,'P10',{bc01Section:'io',bc01Item:item.id,bc01Text:'standard',bc01Find:''});assert.ok(h.includes('直接'.replace('直接','직접')+' I/O·HMI·LAD·구동부·알람·타이머는 미확보'));assert.ok(h.includes('주변 참고'));}
const c10=standard.render(data,'P10',{bc01Section:'control',bc01Item:'regulation',bc01Text:'large',bc01Find:''});for(const t of ['XML695','별칭','논리695개 의미검토가 아닙니다','OFF M0.1','IN0 Wire589 ON M0.0','PIW278','IW278 SAM=None','PIW358','IW358 SAM=None','−9999','PB16A','PB18A','EN미호출'])assert.ok(c10.includes(t),t);
wire18(rdXML('0492'),'391',['<OCon UId="384" />','<PCon UId="376" PinName="Analog_input" />']);wire18(rdXML('0501'),'588',['<OCon UId="581" />','<PCon UId="594" PinName="operand" />']);wire18(rdXML('0501'),'589',['<OCon UId="582" />','<PCon UId="575" PinName="IN0" />']);wire18(rdXML('0398'),'88',['<OCon UId="78" />','<PCon UId="73" PinName="in" />']);wire18(rdXML('0398'),'90',['<PCon UId="73" PinName="out1" />','<OCon UId="79" />']);wire18(rdXML('0398'),'184',['<OCon UId="174" />','<PCon UId="169" PinName="in" />']);
for(const [f,h]of Object.entries(p10.source_hashes))assert.equal(crypto15.createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);for(const loc of p10.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
for(const [section]of standard.sections)for(const item of standard.items(data,'P10',section)){const h=standard.render(data,'P10',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(!h.includes('undefined'));assert.ok(h.includes('standard-content-title'));}
const schema10=data.repair_record_forms.profiles.find(p=>p.key==='P10');assert.deepEqual(plain(schema10.signals),[]);const collect10=plain(repair.collect(schema10,{first_symptom:'QA CC01: 미확보'}));assert.deepEqual(collect10.observations,[]);const note10={...fn01Note,id:'qa-cc01',equipment:'P10',repair_observation:{...collect10,future:{zero:0,blank:'',flag:false},observations:[{id:'future-unknown-signal',value:'0',future:{keep:false}}]}};
assert.deepEqual(plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note11,note10],data,'2026-10-11T11:00:00Z','P10')),store.decodeNotes,valid,schema10)).notes,[note10]);assert.throws(()=>tools.parseBackup(JSON.stringify(tools.backupEnvelope([{...note10,repair_observation:{...note10.repair_observation,equipment:'P11'}}],data,'2026-10-11T11:00:00Z','P10')),store.decodeNotes,valid,schema10));assert.notEqual(tools.referenceContext(data,'P10').source_bundle_sha256,p11.source_bundle_sha256);

const noName10=plain(note10.repair_observation);noName10.decision_observations.push({id:'future-step',observation:'future evidence'});const summary10=repair.summary(noName10);assert.ok(summary10.includes('future-unknown-signal：0'));assert.ok(summary10.includes('future-step：future evidence'));assert.ok(!summary10.includes('undefined'));assert.deepEqual(plain(noName10.observations),plain(note10.repair_observation.observations));

const p12=standard.profile(data,'P12');assert.ok(p12,'AB01 body candidate');assert.equal(p12.type,'passive_body_candidate');assert.deepEqual(plain(p12.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='AB01'));assert.equal(p12.specification.inputs.length,2);for(const k of ['outputs','internal','hmi','networks','direct_rules'])assert.deepEqual(plain(p12.specification[k]),[]);assert.equal(readRegister('alarm-recovery.json').profiles.find(p=>p.id==='AB01'),undefined);assert.equal(p12.regulation,null);assert.equal(p12.control_reference.controller_evidence,null);assert.equal(p12.control_reference.native.length,30);
assert.deepEqual(plain(standard.sections.map(([section])=>standard.items(data,'P12',section).length)),[3,4,1,15,9,3,5]);assert.equal(p12.alarm.alarms.length,7);assert.deepEqual(plain(p12.alarm.timers.map(t=>[t.network,t.uid,t.preset.literal])),[[1979,'155','S5T#6S'],[1979,'198','S5T#6S'],[1986,'770','S5T#1M'],[1984,'599','S5T#1M'],[1985,'685','S5T#1M'],[931,'229','S5T#1S']]);assert.ok(p12.alarm.alarms.every(a=>a.source_reference_only));
const draw12=data.drawing_workspace.profiles.find(p=>p.key==='P12');assert.equal(draw12.circuit.source_reference_only,true);assert.ok(draw12.circuit.paths.every(p=>p.ownership_verified===false));assert.deepEqual(plain(draw12.circuit.paths.slice(0,4).map(p=>p.native_symbol_references[0].uid)),['324','344','56','58']);assert.equal(draw12.circuit.paths[13].native_symbol_references[0].uid,'154');assert.equal(draw12.circuit.paths[14].native_symbol_references[0].uid,'620');
wire18(rdXML('0527'),'255',['<PCon UId="165" PinName="eno" />','<PCon UId="169" PinName="pre" />']);wire18(rdXML('0527'),'287',['<PCon UId="179" PinName="en" />','<PCon UId="186" PinName="pre" />','<PCon UId="189" PinName="pre" />','<PCon UId="192" PinName="pre" />']);wire18(rdXML('0534'),'809',['<PCon UId="754" PinName="en" />','<PCon UId="761" PinName="pre" />','<PCon UId="764" PinName="pre" />']);assert.match(rdXML('0534'),/<Part UId="834" Gate="Contact">\s*<Negated PinName="operand" \/>/);wire18(rdXML('0158'),'38',['<PCon UId="28" PinName="out" />','<PCon UId="33" PinName="in" />','<PCon UId="40" PinName="in" />']);wire18(rdXML('0493'),'409',['<OCon UId="402" />','<PCon UId="415" PinName="operand" />']);
const c12=standard.render(data,'P12',{bc01Section:'control',bc01Item:'regulation',bc01Text:'large',bc01Find:''});for(const t of ['참조2/출력0/HMI0/직접LAD·규칙0','TC02-only의TC01_OFR/EnableTC01','Add.eno직렬아님','Sub.eno','&gt;400 OR','±100정확값','OFF M0.1','ServiceBitM1000.0','DB2X13.4≠PLC RESET_ALLARM DB2X6.0','현재설정미확정','6SB2'])assert.ok(c12.includes(t),t);
for(const [f,h]of Object.entries(p12.source_hashes))assert.equal(crypto15.createHash('sha256').update(fs.readFileSync(__dirname+'/'+f)).digest('hex'),h,f);for(const loc of p12.source_locations)assert.ok(fs.readFileSync(__dirname+'/'+loc.path.split('#')[0],'utf8').includes('id="'+loc.path.split('#')[1]+'"'));
for(const [section]of standard.sections)for(const item of standard.items(data,'P12',section)){const h=standard.render(data,'P12',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(!h.includes('undefined'));assert.ok(h.includes('standard-content-title'));}
const schema12=data.repair_record_forms.profiles.find(p=>p.key==='P12');assert.deepEqual(plain(schema12.signals),[]);const note12={...fn01Note,id:'qa-ab01',equipment:'P12',repair_observation:plain(repair.collect(schema12,{first_symptom:'QA AB01'}))};assert.deepEqual(note12.repair_observation.observations,[]);assert.deepEqual(plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note10,note12],data,'2026-10-11T11:30:00Z','P12')),store.decodeNotes,valid,schema12)).notes,[note12]);assert.throws(()=>tools.parseBackup(JSON.stringify(tools.backupEnvelope([{...note12,repair_observation:{...note12.repair_observation,equipment:'P10'}}],data,'2026-10-11T11:30:00Z','P12')),store.decodeNotes,valid,schema12));assert.notEqual(tools.referenceContext(data,'P12').source_bundle_sha256,p10.source_bundle_sha256);

// HE01 owns no inferred process channels. Its surrounding transcription uses
// the common renderer, including the chain/action shapes which failed UI QA.
const p13=standard.profile(data,'P13');assert.ok(p13);assert.deepEqual(plain(p13.specification),readRegister('control-spec.json').specifications.find(p=>p.id==='HE01'));
for(const k of ['inputs','outputs','internal','hmi','networks','direct_rules'])assert.deepEqual(plain(p13.specification[k]),[]);
assert.deepEqual(plain(p13.signal_trace.signals),[]);assert.equal(readRegister('alarm-recovery.json').profiles.find(p=>p.id==='HE01'),undefined);assert.equal(p13.regulation,null);assert.equal(p13.control_reference.controller_evidence,null);
assert.ok(p13.alarm.alarms.every(a=>a.source_reference_only));assert.deepEqual(plain(p13.alarm.timers.map(t=>[t.uid,t.preset.literal])),[['342','S5T#3S'],['372','S5T#3S'],['415','S5T#3S']]);
assert.equal(p13.source_pairs.length,13);assert.ok(data.drawing_workspace.profiles.find(p=>p.key==='P13').circuit.paths.every(p=>p.ownership_verified===false));
wire18(rdXML('0528'),'491',['<PCon UId="352" PinName="eno" />','<PCon UId="356" PinName="pre" />']);wire18(rdXML('0528'),'512',['<PCon UId="382" PinName="eno" />','<PCon UId="386" PinName="pre" />']);wire18(rdXML('0528'),'544',['<PCon UId="396" PinName="en" />','<PCon UId="403" PinName="pre" />','<PCon UId="406" PinName="pre" />','<PCon UId="409" PinName="pre" />']);
let rendered13=0;for(const [section]of standard.sections)for(const item of standard.items(data,'P13',section)){const h=standard.render(data,'P13',{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(h.includes('standard-content-title'));assert.ok(!h.includes('undefined'));rendered13++;}assert.equal(rendered13,34);
const schema13=data.repair_record_forms.profiles.find(p=>p.key==='P13');assert.deepEqual(plain(schema13.signals),[]);const note13={...fn01Note,id:'qa-he01',equipment:'P13',repair_observation:plain(repair.collect(schema13,{first_symptom:'QA HE01'}))};note13.repair_observation.observations=[{id:'future-unknown-signal',value:'0',future:{keep:false}}];
assert.deepEqual(plain(tools.parseBackup(JSON.stringify(tools.backupEnvelope([note12,note13],data,'2026-10-11T11:40:00Z','P13')),store.decodeNotes,valid,schema13)).notes,[note13]);assert.ok(repair.summary(note13.repair_observation).includes('future-unknown-signal：0'));
const priorHistory={...changed,backup_restore_history:[{past:'A'}]},incomingHistory={...changed,title:'history changed',backup_restore_history:[{past:'B'}]};
const historyMerged=plain(tools.applyUnifiedRestore([priorHistory],tools.planRestore([priorHistory],[incomingHistory]),{0:'replace'},()=> 'new-copy')).notes[0];assert.deepEqual(historyMerged.backup_restore_history,[{past:'A'},{past:'B'}]);
const generator=fs.readFileSync(__dirname+'/build-control-spec.py','utf8');assert.ok(!generator.includes('runpy.run_path'));
const entry=fs.readFileSync(__dirname+'/index.html','utf8');assert.ok(!/<script[^>]+src=["'][^"']*(?:virtual-plc|simulator-workspace)\.js/.test(entry));
for(const p of data.equipment_standards.profiles){const key=p.selection_key||p.priority_key,source=standard.profile(data,key),drawing=data.drawing_workspace.profiles.find(r=>r.key===key);if(p.selection_key){assert.ok(source.source_pairs.length>=drawing.circuit.paths.filter(path=>path.source_pair_status!=='not_identified').length,key+':identified paths require original pairs');for(const pair of source.source_pairs)assert.ok(source.source_locations.some(loc=>loc.path===pair.path),key+':'+pair.signal);}else assert.equal(source.source_pairs.length,drawing.circuit.paths.length);for(const path of drawing.circuit.paths){const matches=source.source_pairs.filter(p=>p.signal===path.signal);if(path.source_pair_status==='not_identified'){assert.equal(matches.length,0,key+':no invented PLC pair');assert.ok(path.source_pair_boundary&&path.check,key+':missing-pair explanation');assert.equal(path.native_symbol_references.length,0,key+':no claimed direct PLC pins');}else assert.equal(matches.length,1);}}
console.log(JSON.stringify({status:'passed',scope:'equipment selection, mismatched nested key, foreign record isolation, unknown fields, zero/blank comparison, reference version, unified backup legacy formats, 1001-note round trip, malformed keys/records, cross-equipment ID conflicts, provenance and merged limits, explicit generator and frozen script loading boundaries',registered_profiles:data.equipment_standards.profiles.map(p=>p.selection_key||p.priority_key)}));
