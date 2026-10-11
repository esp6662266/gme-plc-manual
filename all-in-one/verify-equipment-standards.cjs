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

const priorHistory={...changed,backup_restore_history:[{past:'A'}]},incomingHistory={...changed,title:'history changed',backup_restore_history:[{past:'B'}]};
const historyMerged=plain(tools.applyUnifiedRestore([priorHistory],tools.planRestore([priorHistory],[incomingHistory]),{0:'replace'},()=> 'new-copy')).notes[0];assert.deepEqual(historyMerged.backup_restore_history,[{past:'A'},{past:'B'}]);
const generator=fs.readFileSync(__dirname+'/build-control-spec.py','utf8');assert.ok(!generator.includes('runpy.run_path'));
const entry=fs.readFileSync(__dirname+'/index.html','utf8');assert.ok(!/<script[^>]+src=["'][^"']*(?:virtual-plc|simulator-workspace)\.js/.test(entry));
for(const p of data.equipment_standards.profiles){const source=standard.profile(data,p.priority_key),drawing=data.drawing_workspace.profiles.find(r=>r.key===p.priority_key);assert.equal(source.source_pairs.length,drawing.circuit.paths.length);for(const path of drawing.circuit.paths)assert.equal(source.source_pairs.filter(p=>p.signal===path.signal).length,1);}
console.log(JSON.stringify({status:'passed',scope:'equipment selection, mismatched nested key, foreign record isolation, unknown fields, zero/blank comparison, reference version, unified backup legacy formats, 1001-note round trip, malformed keys/records, cross-equipment ID conflicts, provenance and merged limits, explicit generator and frozen script loading boundaries',registered_profiles:data.equipment_standards.profiles.map(p=>p.priority_key)}));
