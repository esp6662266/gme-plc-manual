/* Actual catalog IDs, original pin witnesses, and record preservation. */
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),crypto=require('node:crypto');
const clone=x=>JSON.parse(JSON.stringify(x)),sandbox={window:{},TextEncoder};
for(const file of ['repair-records','note-record-store','equipment-standard','bc01-tools'])vm.runInNewContext(fs.readFileSync(__dirname+'/assets/'+file+'.js','utf8'),sandbox);
const {GMEEquipmentStandard:standard,GMEBC01Tools:tools,GMERepairRecords:repair,GMENoteStore:store}=sandbox.window;
const data=JSON.parse(fs.readFileSync(__dirname+'/registers/all-in-one-data.json'));
const valid=new Set(data.equipment.map(e=>e.id).concat(data.priority.map(p=>p.key)));
const keys=fs.readdirSync(__dirname+'/catalog-profiles').filter(f=>f.endsWith('.json')).map(f=>f.slice(0,-5));
for(const key of keys){
 const p=standard.profile(data,key),schema=data.repair_record_forms.profiles.find(f=>f.key===key);
 assert.equal(p.catalog_id,key);assert.equal(p.priority_key,null);assert.equal(p.selection_key,key);assert.ok(valid.has(key));
 assert.equal(p.field_verified,false);assert.equal(p.tia_verified,false);assert.equal(p.repairs_completed,0);
 for(const [file,hash]of Object.entries(p.source_hashes))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(__dirname+'/'+file)).digest('hex'),hash,file);
 for(const [section]of standard.sections){const items=standard.items(data,key,section);assert.ok(items.length);for(const item of items){const h=standard.render(data,key,{bc01Section:section,bc01Item:item.id,bc01Text:'large',bc01Find:''});assert.ok(h.includes('standard-content-title'));assert.ok(!h.includes('undefined'));for(const [label,url]of item.links){assert.ok(data.resources.includes(url.split('#')[0]),key+':'+label);const [path,anchor]=url.split('#');if(anchor&&path.endsWith('.html'))assert.ok(fs.readFileSync(__dirname+'/'+path,'utf8').includes('id="'+anchor+'"'),key+':'+url);}}}
 for(const path of data.drawing_workspace.profiles.find(x=>x.key===key).circuit.paths){const matched=p.source_pairs.filter(pair=>pair.signal===path.signal);if(path.source_pair_status==='not_identified'){assert.equal(matched.length,0,key+':no invented direct PLC pair');assert.ok(path.source_pair_boundary&&path.check);assert.equal(path.native_symbol_references.length,0);}else assert.equal(matched.length,1,key+':missing path source pair '+path.signal);}
 const note={id:'qa-'+key,equipment:key,title:'QA only',text:'',updated:'2026-10-11T13:00:00Z',future:{zero:0,blank:'',flag:false},repair_observation:clone(repair.collect(schema,{first_symptom:'QA only',[schema.signals[0].id+'_value']:'0'}))};
 note.repair_observation.future={zero:0,blank:'',flag:false};
 note.repair_observation.observations.push({id:'unknown-new-signal',value:'',future:{retained:false}});
 const foreign={...note,id:'qa-other',equipment:'P01',repair_observation:undefined};
 const envelope=tools.backupEnvelope([foreign,note],data,note.updated,key);
 const incoming=clone(tools.parseBackup(JSON.stringify(envelope),store.decodeNotes,valid,schema));assert.deepEqual(incoming.notes,[note]);assert.equal(incoming.skipped,1);
 const next=clone(note);next.title='QA after';next.repair_observation.observations[0].value='';delete next.future;
 const merged=clone(tools.applyRestore([foreign,note],tools.planRestore([foreign,note],[next]),{0:'replace'},()=> 'copy',key));
 assert.deepEqual(merged.notes[0],clone(foreign));assert.deepEqual(merged.notes[1].future,note.future);assert.deepEqual(merged.notes[1].repair_observation.future,note.repair_observation.future);
 assert.ok(clone(tools.comparisonRows(note,next,schema)).some(r=>r.key.endsWith(':value')&&r.changed));
 assert.throws(()=>tools.parseBackup(JSON.stringify({...envelope,notes:[{...note,repair_observation:{...note.repair_observation,equipment:'P01'}}]}),store.decodeNotes,valid,schema));
 const hostile=clone(data),target=standard.profile(hostile,key);target.reviewed_sections.overview[0].value.blocks=[{type:'paragraph',text:'<img src=x onerror=alert(1)> **safe** `code`'}];
 const h=standard.render(hostile,key,{bc01Section:'overview',bc01Item:target.reviewed_sections.overview[0].id,bc01Text:'standard',bc01Find:''});assert.ok(h.includes('&lt;img'));assert.ok(!h.includes('<img src=x'));assert.ok(h.includes('<strong>safe</strong>'));assert.ok(h.includes('<code>code</code>'));
}
const fn=standard.profile(data,'FN05');assert.equal(fn.signal_trace.signals.length,5);assert.equal(fn.alarm.alarms[0].address,'DB3.DBX3.1');assert.equal(fn.alarm.timers[0].preset,'S5T#2S');
const xml=file=>fs.readFileSync(__dirname+'/sources/decoded-original/'+file+'-FlgNet.xml','utf8');
function wire(text,id,pins){const body=text.match(new RegExp('<Wire UId="'+id+'">[\\s\\S]*?</Wire>'))?.[0];assert.ok(body,id);for(const pin of pins)assert.ok(body.includes(pin),id+':'+pin);}
const motor=xml('0270'),alarm=xml('0448'),hours=xml('0331');
wire(motor,'24',['<PCon UId="22" PinName="out" />','<PCon UId="1132" PinName="in" />']);
wire(motor,'1133',['<PCon UId="1132" PinName="out" />','<PCon UId="1097" PinName="in2" />']);
wire(motor,'1135',['<PCon UId="1134" PinName="out" />','<PCon UId="1106" PinName="in" />']);
assert.match(alarm,/<Part UId="1274" Gate="Contact">\s*<Negated PinName="operand" \/>/);
wire(alarm,'1249',['<OCon UId="1239" />','<PCon UId="1225" PinName="value" />']);
wire(alarm,'1254',['<PCon UId="1231" PinName="operand" />','<OCon UId="1243" />']);
assert.match(hours,/<Part UId="2522" Gate="Move">/);assert.ok(!hours.includes('<Part UId="2522" Gate="Add">'));
wire(hours,'2550',['<OCon UId="2536" />','<PCon UId="2522" PinName="in" />']);
wire(hours,'2551',['<PCon UId="2522" PinName="out1" />','<OCon UId="2537" />']);
const declaration=fs.readFileSync(__dirname+'/sources/decoded-original/0616-IdentXmlPart.xml','utf8');assert.ok(declaration.split('</LiteralConstant>').some(t=>t.includes('RID="7"')&&t.includes('NID="46" UID="2536"')&&t.includes('V="1"')));
const sc=standard.profile(data,'SC01');assert.equal(sc.signal_trace.signals.length,5);assert.equal(sc.alarm.timers[0].preset,'S5T#2S');
const scmotor=xml('0258'),scalarm=xml('0438'),schours=xml('0321');
wire(scmotor,'24',['<PCon UId="22" PinName="out" />','<PCon UId="825" PinName="in" />']);
wire(scmotor,'826',['<PCon UId="825" PinName="out" />','<PCon UId="790" PinName="in2" />']);
wire(scmotor,'828',['<PCon UId="827" PinName="out" />','<PCon UId="799" PinName="in" />']);
assert.match(scalarm,/<Part UId="900" Gate="Contact"><Negated PinName="operand" \/>/);
wire(scalarm,'875',['<OCon UId="865" />','<PCon UId="851" PinName="value" />']);
wire(scalarm,'880',['<OCon UId="869" />','<PCon UId="857" PinName="operand" />']);
assert.match(schours,/<Part UId="1928" Gate="Move">/);
wire(schours,'1956',['<OCon UId="1942" />','<PCon UId="1928" PinName="in" />']);
wire(schours,'1957',['<PCon UId="1928" PinName="out1" />','<OCon UId="1943" />']);
const pv=standard.profile(data,'PV03'); assert.equal(pv.signal_trace.signals.length,14); assert.deepEqual(Array.from(pv.alarm.timers,t=>t.preset),['S5T#5S','S5T#5S']);
const pvout=xml('0272'),pvmem=xml('0290'),pvalarm=xml('0453'),liw=xml('0273');
wire(pvout,'1169',['<PCon UId="1168" PinName="out" />','<PCon UId="1144" PinName="in1" />']);
wire(pvout,'1171',['<PCon UId="1170" PinName="out" />','<PCon UId="1144" PinName="in2" />']);
wire(pvout,'1160',['<PCon UId="1144" PinName="out" />','<PCon UId="1147" PinName="in" />']);
wire(pvmem,'84',['<PCon UId="80" PinName="out" />','<PCon UId="82" PinName="in3" />']);
wire(pvmem,'72',['<PCon UId="69" PinName="out" />','<PCon UId="65" PinName="in3" />']);
assert.match(pvmem,/<Part UId="69" Gate="Contact">\s*<Negated PinName="operand" \/>/);
wire(pvalarm,'1760',['<OCon UId="1741" />','<PCon UId="1709" PinName="value" />']);
wire(pvalarm,'1772',['<OCon UId="1750" />','<PCon UId="1727" PinName="value" />']);
wire(liw,'1233',['<PCon UId="1190" PinName="out" />','<PCon UId="1196" PinName="in" />','<PCon UId="1257" PinName="in" />']);
wire(liw,'1258',['<PCon UId="1257" PinName="out" />','<PCon UId="1201" PinName="in" />']);
const pvtime=fs.readFileSync(__dirname+'/sources/decoded-original/0656-IdentXmlPart.xml','utf8');assert.ok(pvtime.split('</LiteralConstant>').some(t=>t.includes('RID="175"')&&t.includes('NID="46" UID="1741"')&&t.includes('NID="46" UID="1750"')&&t.includes('SV="S5T_x0023_5S"')));
for(const key of keys){const schema=data.repair_record_forms.profiles.find(f=>f.key===key);for(const field of ['circuit_pages','construction_pages'])for(const link of schema.evidence_plan[field]){assert.ok(link.label);assert.ok(data.resources.includes(link.path.split('#')[0]));}}

const mv=standard.profile(data,'MV02');assert.equal(mv.signal_trace.signals.length,21);assert.equal(mv.alarm.timers[0].preset,'S5T#150MS');
const mvout=xml('0343'),mvfault=xml('0159'),mvcount=xml('0352'),mvencoder=xml('0513'),mvcalls=xml('0032');
for(const uid of ['310','312','326','338','352'])assert.match(mvout,new RegExp('<Part UId="'+uid+'" Gate="Contact">\\s*<Negated PinName="operand" />'));
wire(mvout,'295',['<OCon UId="259" />','<PCon UId="227" PinName="operand" />']);
wire(mvcalls,'353',['<PCon UId="352" PinName="out" />','<PCon UId="341" PinName="en" />']);
assert.match(mvcalls,/<Part UId="352" Gate="Contact" \/>/);
wire(mvfault,'442',['<OCon UId="376" />','<PCon UId="265" PinName="value" />']);
wire(mvcount,'1865',['<PCon UId="1624" PinName="out" />','<PCon UId="1630" PinName="in" />','<PCon UId="1633" PinName="en" />']);
wire(mvcount,'1872',['<PCon UId="1638" PinName="out" />','<PCon UId="1644" PinName="in" />','<PCon UId="1647" PinName="en" />']);
wire(mvencoder,'64',['<OCon UId="39" />','<PCon UId="25" PinName="in2" />']);
const declRaw=f=>fs.readFileSync(__dirname+'/sources/decoded-original/'+f+'-IdentXmlPart.xml','utf8');
assert.ok(declRaw('0571').split('</LiteralConstant>').some(t=>t.includes('RID="8"')&&t.includes('NID="1" UID="376"')&&t.includes('SV="S5T_x0023_150MS"')));
assert.ok(declRaw('0675').split('</LiteralConstant>').some(t=>t.includes('RID="211"')&&t.includes('NID="46" UID="39"')&&t.includes('V="100"')));
assert.ok(declRaw('0620').split('</LiteralConstant>').some(t=>t.includes('RID="149"')&&t.includes('NID="12" UID="1792"')&&t.includes('V="1000"')));
assert.ok(declRaw('0620').split('</LiteralConstant>').some(t=>t.includes('RID="151"')&&t.includes('NID="12" UID="1797"')&&t.includes('SV="_x002D_1000"')&&t.includes('V="64536"')));

const mv05=standard.profile(data,'MV05');assert.equal(mv05.signal_trace.signals.length,23);assert.equal(mv05.alarm.timers[0].address,'%T15');assert.equal(mv05.alarm.timers[0].preset,'S5T#150MS');
const mv05out=xml('0346'),mv05enc=xml('0515'),mv05pid=xml('0475'),mv05ox=xml('0530');
wire(mv05out,'628',['<PCon UId="552" PinName="out" />','<PCon UId="678" PinName="in" />','<PCon UId="680" PinName="in" />']);
wire(mv05out,'697',['<PCon UId="696" PinName="out" />','<PCon UId="567" PinName="in3" />']);
wire(mv05out,'635',['<OCon UId="596" />','<PCon UId="561" PinName="operand" />']);
wire(mv05out,'649',['<OCon UId="605" />','<PCon UId="576" PinName="operand" />']);
wire(mvfault,'475',['<OCon UId="400" />','<PCon UId="313" PinName="value" />']);
wire(mv05enc,'1303',['<OCon UId="1279" />','<PCon UId="1242" PinName="in2" />']);
wire(mv05ox,'525',['<PCon UId="483" PinName="out" />','<PCon UId="22" PinName="in" />']);
wire(mv05ox,'24',['<PCon UId="22" PinName="out" />','<PCon UId="490" PinName="in" />']);
for(const [rid,uid,value]of [['157','1825','700'],['159','1830','64836']])assert.ok(declRaw('0620').split('</LiteralConstant>').some(t=>t.includes('RID="'+rid+'"')&&t.includes('NID="12" UID="'+uid+'"')&&t.includes('V="'+value+'"')));
assert.ok(declRaw('0675').split('</LiteralConstant>').some(t=>t.includes('RID="211"')&&t.includes('NID="33" UID="1279"')&&t.includes('V="100"')));
assert.ok(mv05pid.includes('<Instance UId="149" RefId="20" />'));assert.ok(declRaw('0665').split('</AufDBBlock>').some(t=>t.includes('N="PID_MV05"')&&t.includes('RID="20"')&&t.includes('<TOD N="22"')));
assert.ok(standard.items(data,'MV05','circuits').some(item=>JSON.stringify(item).includes('FG137/PDF138')&&JSON.stringify(item).includes('Rev2')));
const er=standard.profile(data,'ER01');assert.equal(er.signal_trace.signals.length,13);assert.equal(er.alarm.timers[0].address,'DB32');assert.equal(er.alarm.timers[0].preset,'T#2S');
const erout=xml('0271'),erton=xml('0456'),erinput=xml('0397');
wire(erout,'1158',['<PCon UId="1157" PinName="out" />','<PCon UId="30" PinName="in" />']);
wire(erout,'32',['<PCon UId="30" PinName="out" />','<PCon UId="1129" PinName="in" />']);
wire(erout,'28',['<PCon UId="26" PinName="out" />','<PCon UId="1155" PinName="in" />']);
wire(erton,'51',['<PCon UId="23" PinName="out" />','<PCon UId="28" PinName="IN" />']);
wire(erton,'30',['<OCon UId="37" />','<PCon UId="28" PinName="PT" />']);
wire(erton,'38',['<PCon UId="28" PinName="Q" />','<PCon UId="24" PinName="in" />']);
wire(erinput,'129',['<PCon UId="86" PinName="out" />','<PCon UId="125" PinName="in" />']);
assert.ok(erton.includes('<Instance UId="29" RefId="312" />'));
assert.ok(declRaw('0654').split('</AufDBBlock>').some(t=>t.includes('N="Er_01_Run_Rit"')&&t.includes('RID="312"')&&t.includes('<TOD N="32"')));
assert.ok(declRaw('0656').split('</LiteralConstant>').some(t=>t.includes('RID="311"')&&t.includes('NID="49" UID="37"')&&t.includes('T="Time"')&&t.includes('V="2000"')));
assert.ok(declRaw('0629').split('</GlobalAccess>').some(t=>t.includes('RID="148"')&&t.includes('AO="180"')&&t.includes('NID="1" UID="126"')&&t.includes('AK="Write"')));
const ch=standard.profile(data,'CH01');assert.equal(ch.signal_trace.signals.length,13);assert.deepEqual(Array.from(ch.alarm.timers,t=>t.preset),['S5T#10S','S5T#2S']);
const chout=xml('0255'),chfault=xml('0435'),chhours=xml('0318');
wire(chout,'772',['<PCon UId="771" PinName="out" />','<PCon UId="736" PinName="in" />','<PCon UId="739" PinName="in" />','<PCon UId="773" PinName="in" />']);
wire(chout,'774',['<PCon UId="773" PinName="out" />','<PCon UId="744" PinName="in" />']);
wire(chfault,'788',['<PCon UId="787" PinName="out" />','<PCon UId="798" PinName="in" />','<PCon UId="789" PinName="in" />']);
wire(chfault,'22',['<PCon UId="789" PinName="out" />','<PCon UId="755" PinName="in" />']);
assert.ok(chhours.includes('<Part UId="1766" Gate="Move">'));
wire(chhours,'1794',['<OCon UId="1780" />','<PCon UId="1766" PinName="in" />']);
wire(chhours,'1795',['<PCon UId="1766" PinName="out1" />','<OCon UId="1781" />']);
assert.ok(declRaw('0606').split('</LiteralConstant>').some(t=>t.includes('RID="125"')&&t.includes('NID="24" UID="750"')&&t.includes('SV="S5T_x0023_10S"')));
assert.ok(declRaw('0656').split('</LiteralConstant>').some(t=>t.includes('RID="28"')&&t.includes('NID="22" UID="763"')&&t.includes('SV="S5T_x0023_2S"')));
assert.ok(declRaw('0616').split('</LiteralConstant>').some(t=>t.includes('RID="7"')&&t.includes('NID="32" UID="1780"')&&t.includes('V="1"')));
const vr1=standard.profile(data,'VR01');assert.equal(vr1.signal_trace.signals.length,13);assert.equal(vr1.alarm.timers[0].address,'%T63');assert.equal(vr1.alarm.timers[0].preset,'S5T#2S');
const vr1out=xml('0251'),vr1fault=xml('0432'),vr1hours=xml('0315'),fnshared=xml('0252');
wire(vr1out,'627',['<PCon UId="626" PinName="out" />','<PCon UId="608" PinName="in" />']);
wire(vr1out,'625',['<PCon UId="624" PinName="out" />','<PCon UId="604" PinName="in" />']);
wire(vr1fault,'686',['<PCon UId="685" PinName="out" />','<PCon UId="696" PinName="in" />','<PCon UId="687" PinName="in" />']);
wire(vr1fault,'22',['<PCon UId="687" PinName="out" />','<PCon UId="653" PinName="in" />']);
assert.ok(vr1hours.includes('<Part UId="1604" Gate="Move">'));
wire(vr1hours,'1632',['<OCon UId="1618" />','<PCon UId="1604" PinName="in" />']);
wire(vr1hours,'1633',['<PCon UId="1604" PinName="out1" />','<OCon UId="1619" />']);
wire(fnshared,'700',['<PCon UId="699" PinName="out" />','<PCon UId="701" PinName="in" />','<PCon UId="703" PinName="in" />']);
assert.ok(declRaw('0656').split('</LiteralConstant>').some(t=>t.includes('RID="28"')&&t.includes('NID="19" UID="661"')&&t.includes('SV="S5T_x0023_2S"')));
assert.ok(declRaw('0606').split('</LiteralConstant>').some(t=>t.includes('RID="112"')&&t.includes('NID="21" UID="670"')&&t.includes('V="13632"')));
assert.ok(declRaw('0616').split('</LiteralConstant>').some(t=>t.includes('RID="7"')&&t.includes('NID="29" UID="1618"')&&t.includes('V="1"')));
const vr2=standard.profile(data,'VR02');assert.equal(vr2.signal_trace.signals.length,13);assert.equal(vr2.alarm.timers[0].address,'%T67');assert.equal(vr2.alarm.timers[0].preset,'S5T#2S');
const vr2out=xml('0254'),vr2fault=xml('0434'),vr2hours=xml('0317'),vr2reset=xml('0338');
wire(vr2out,'712',['<PCon UId="711" PinName="out" />','<PCon UId="713" PinName="in" />','<PCon UId="715" PinName="in" />']);
wire(vr2out,'716',['<PCon UId="715" PinName="out" />','<PCon UId="697" PinName="in" />']);
wire(vr2fault,'754',['<PCon UId="753" PinName="out" />','<PCon UId="764" PinName="in" />','<PCon UId="755" PinName="in" />']);
wire(vr2fault,'22',['<PCon UId="755" PinName="out" />','<PCon UId="721" PinName="in" />']);
assert.ok(vr2hours.includes('<Part UId="1712" Gate="Move">'));
wire(vr2hours,'1740',['<OCon UId="1726" />','<PCon UId="1712" PinName="in" />']);
wire(vr2reset,'2988',['<PCon UId="2987" PinName="out" />','<PCon UId="2946" PinName="en" />']);
assert.ok(declRaw('0656').split('</LiteralConstant>').some(t=>t.includes('RID="28"')&&t.includes('NID="21" UID="729"')&&t.includes('SV="S5T_x0023_2S"')));
assert.ok(declRaw('0616').split('</LiteralConstant>').some(t=>t.includes('RID="7"')&&t.includes('NID="31" UID="1726"')&&t.includes('V="1"')));
const vr3=standard.profile(data,'VR03');assert.equal(vr3.signal_trace.signals.length,13);assert.equal(vr3.alarm.timers[0].address,'%T84');assert.equal(vr3.alarm.timers[0].preset,'S5T#2S');
wire(xml('0266'),'1043',['<PCon UId="1042" PinName="out" />','<PCon UId="1024" PinName="in" />']);
wire(xml('0444'),'1128',['<PCon UId="1127" PinName="out" />','<PCon UId="1138" PinName="in" />','<PCon UId="1129" PinName="in" />']);
wire(xml('0444'),'22',['<PCon UId="1129" PinName="out" />','<PCon UId="1095" PinName="in" />']);
wire(xml('0327'),'2334',['<OCon UId="2320" />','<PCon UId="2306" PinName="in" />']);
wire(xml('0340'),'3099',['<PCon UId="3070" PinName="eno" />','<PCon UId="3073" PinName="en" />']);
assert.ok(declRaw('0656').split('</LiteralConstant>').some(t=>t.includes('RID="28"')&&t.includes('NID="32" UID="1103"')&&t.includes('SV="S5T_x0023_2S"')));
assert.ok(declRaw('0616').split('</LiteralConstant>').some(t=>t.includes('RID="7"')&&t.includes('NID="42" UID="2320"')&&t.includes('V="1"')));
/* READY10-02: preserve distinct reset/output and timer/set branches. */
for(const [key,motorFile,alarmFile,hourFile,timer,output,request,raw,processed,set,reset,sd,notRun,hourMove,constant,hourOut]of [
 ['VR04','0267','0445','0328','%T93','%Q4.4','DB2.DBX2.6','%I5.5','DB13.DBX5.5','1129','1134','1123','1172','2360','2374','2375'],
 ['VR05','0268','0446','0329','%T94','%Q4.5','DB2.DBX2.7','%I5.6','DB13.DBX5.6','1163','1168','1157','1206','2414','2428','2429'],
 ['VR06','0269','0447','0330','%T95','%Q4.6','DB2.DBX3.0','%I5.7','DB13.DBX5.7','1197','1202','1191','1240','2468','2482','2483']
]){
 const p=standard.profile(data,key);assert.equal(p.alarm.timers[0].address,timer);assert.equal(p.alarm.timers[0].preset,'S5T#2S');
 const signal=id=>p.signal_trace.signals.find(s=>s.id===id);assert.ok(signal('output').addresses.includes(output));assert.ok(signal('request').addresses.includes(request));assert.ok(signal('raw-feedback').addresses.includes(raw));assert.ok(signal('feedback').addresses.includes(processed));
 const a=xml(alarmFile),h=xml(hourFile);assert.ok(a.includes('<Part UId="'+set+'" Gate="SCoil"'));assert.ok(a.includes('<Part UId="'+reset+'" Gate="RCoil"'));
 assert.match(a,new RegExp('<Part UId="'+notRun+'" Gate="Contact">\\s*<Negated PinName="operand" />'));
 wire(a,'21',['<PCon UId="'+notRun+'" PinName="out" />','<PCon UId="'+sd+'" PinName="in" />']);
 assert.ok(h.includes('<Part UId="'+hourMove+'" Gate="Move">'));assert.ok(!h.includes('<Part UId="'+hourMove+'" Gate="Add">'));
 const nid={VR04:'43',VR05:'44',VR06:'45'}[key];assert.ok(declRaw('0616').split('</LiteralConstant>').some(t=>t.includes('RID="7"')&&t.includes('NID="'+nid+'" UID="'+constant+'"')&&t.includes('V="1"')));
 for(const section of ['io','control','alarms','repair'])assert.ok(!JSON.stringify(standard.items(data,key,section)).includes('Word0'));
 assert.ok(JSON.stringify(standard.items(data,key,'io')).includes('총8개'));
}
wire(xml('0268'),'1071',['<PCon UId="1070" PinName="out" />','<PCon UId="1072" PinName="in" />','<PCon UId="1074" PinName="in" />']);
wire(xml('0263'),'24',['<PCon UId="22" PinName="out" />','<PCon UId="969" PinName="in" />']);
wire(xml('0219'),'64',['<PCon UId="29" PinName="out" />','<PCon UId="30" PinName="pre" />','<PCon UId="31" PinName="in" />']);
wire(xml('0219'),'66',['<OCon UId="44" />','<PCon UId="30" PinName="in2" />']);
assert.ok(declRaw('0596').split('</GlobalAccess>').some(t=>t.includes('N="DP_01_SOGLIA_1"')&&t.includes('NID="29" UID="44"')&&t.includes('BO="1104"')));
wire(xml('0340'),'3105',['<PCon UId="3076" PinName="eno" />','<PCon UId="3079" PinName="en" />']);
assert.ok(declRaw('0563').split('</GlobalAccess>').some(t=>t.includes('RID="26"')&&t.includes('NID="3" UID="288" AK="Write"')&&t.includes('AO="16"')&&t.includes('BIRID="23"')));
/* VR06: ER01 command and Testing release request, not the separate output coil. */
wire(xml('0269'),'1104',['<PCon UId="1103" PinName="out" />','<PCon UId="1107" PinName="in" />','<PCon UId="1111" PinName="in" />']);
for(const uid of ['1107','1109'])assert.match(xml('0269'),new RegExp('<Part UId="'+uid+'" Gate="Contact">\\s*<Negated PinName="operand" />'));
wire(xml('0269'),'1108',['<PCon UId="1107" PinName="out" />','<PCon UId="1109" PinName="in" />']);
wire(xml('0269'),'1096',['<PCon UId="1074" PinName="out" />','<PCon UId="1079" PinName="in" />']);
wire(xml('0269'),'1112',['<PCon UId="1111" PinName="out" />','<PCon UId="1083" PinName="in" />']);
wire(xml('0259'),'24',['<PCon UId="22" PinName="out" />','<PCon UId="869" PinName="in" />']);
wire(xml('0261'),'913',['<PCon UId="888" PinName="out" />','<PCon UId="891" PinName="in" />']);
wire(xml('0261'),'934',['<PCon UId="933" PinName="out" />','<PCon UId="935" PinName="in" />']);
wire(xml('0261'),'936',['<PCon UId="935" PinName="out" />','<PCon UId="894" PinName="in2" />']);
wire(xml('0261'),'26',['<PCon UId="31" PinName="out" />','<PCon UId="900" PinName="in" />']);
wire(xml('0340'),'3108',['<PCon UId="3079" PinName="eno" />','<PCon UId="3082" PinName="en" />']);
/* SC10: own automatic counters, VR04 request reset, and shared washing writers. */
const sc10=standard.profile(data,'SC10');assert.equal(sc10.signal_trace.signals.length,17);assert.equal(sc10.alarm.timers[0].address,'%T81');assert.equal(sc10.alarm.timers[0].preset,'S5T#2S');
assert.ok(JSON.stringify(standard.items(data,'SC10','io')).includes('총8개'));
wire(xml('0262'),'24',['<PCon UId="22" PinName="out" />','<PCon UId="946" PinName="in" />']);
wire(xml('0262'),'947',['<PCon UId="946" PinName="out" />','<PCon UId="911" PinName="in2" />']);
wire(xml('0262'),'949',['<PCon UId="948" PinName="out" />','<PCon UId="920" PinName="in" />']);
assert.match(xml('0441'),/<Part UId="1036" Gate="Contact">\s*<Negated PinName="operand" \/>/);
wire(xml('0441'),'21',['<PCon UId="1036" PinName="out" />','<PCon UId="987" PinName="in" />']);
wire(xml('0441'),'22',['<PCon UId="1027" PinName="out" />','<PCon UId="993" PinName="in" />']);
assert.ok(declRaw('0656').split('</LiteralConstant>').some(t=>t.includes('RID="28"')&&t.includes('NID="29" UID="1001"')&&t.includes('SV="S5T_x0023_2S"')));
for(const [file,uid,nid,value,wireId,setUid,outUid]of [['0164','602','3','5','690','434','604'],['0165','946','4','6','1039','771','948']]){
 wire(xml(file),wireId,['<PCon UId="'+setUid+'" PinName="operand" />','<OCon UId="'+outUid+'" />']);
 assert.ok(declRaw('0578').split('</LiteralConstant>').some(t=>t.includes('NID="'+nid+'" UID="'+uid+'"')&&t.includes('V="'+value+'"')));
}
assert.ok(xml('0324').includes('<Part UId="2144" Gate="Move">'));
wire(xml('0324'),'2172',['<OCon UId="2158" />','<PCon UId="2144" PinName="in" />']);
assert.ok(declRaw('0616').split('</LiteralConstant>').some(t=>t.includes('NID="39" UID="2158"')&&t.includes('RID="7"')&&t.includes('V="1"')));
wire(xml('0339'),'3043',['<PCon UId="3014" PinName="eno" />','<PCon UId="3017" PinName="en" />']);
wire(xml('0219'),'53',['<PCon UId="23" PinName="out" />','<PCon UId="24" PinName="pre" />','<PCon UId="25" PinName="in" />']);
assert.ok(xml('0219').includes('<Part UId="24" Gate="Le">'));
wire(xml('0202'),'600',['<PCon UId="599" PinName="out" />','<PCon UId="547" PinName="en" />','<PCon UId="601" PinName="in" />']);
assert.ok(declRaw('0596').split('</GlobalAccess>').some(t=>t.includes('N="LAVA"')&&t.includes('BO="1840"')&&['571','574','577','581'].every(uid=>t.includes('NID="6" UID="'+uid+'"'))));
/* SC11: independent branches, shared BF02 threshold, and fifth reset Move. */
const sc11=standard.profile(data,'SC11');assert.equal(sc11.signal_trace.signals.length,19);assert.equal(sc11.alarm.timers[0].address,'%T82');assert.equal(sc11.alarm.timers[0].preset,'S5T#2S');
assert.ok(JSON.stringify(standard.items(data,'SC11','io')).includes('총8개'));
wire(xml('0263'),'24',['<PCon UId="22" PinName="out" />','<PCon UId="969" PinName="in" />']);
wire(xml('0263'),'970',['<PCon UId="969" PinName="out" />','<PCon UId="934" PinName="in2" />']);
wire(xml('0263'),'972',['<PCon UId="971" PinName="out" />','<PCon UId="943" PinName="in" />']);
assert.match(xml('0442'),/<Part UId="1070" Gate="Contact">\s*<Negated PinName="operand" \/>/);
wire(xml('0442'),'21',['<PCon UId="1070" PinName="out" />','<PCon UId="1021" PinName="in" />']);
wire(xml('0442'),'22',['<PCon UId="1061" PinName="out" />','<PCon UId="1027" PinName="in" />']);
wire(xml('0442'),'1068',['<PCon UId="1067" PinName="out" />','<PCon UId="1032" PinName="in" />']);
assert.ok(declRaw('0656').split('</LiteralConstant>').some(t=>t.includes('RID="28"')&&t.includes('NID="30" UID="1035"')&&t.includes('SV="S5T_x0023_2S"')));
wire(xml('0164'),'691',['<PCon UId="436" PinName="operand" />','<OCon UId="605" />']);
wire(xml('0165'),'1040',['<PCon UId="773" PinName="operand" />','<OCon UId="949" />']);
wire(xml('0325'),'2226',['<OCon UId="2212" />','<PCon UId="2198" PinName="in" />']);
assert.ok(declRaw('0616').split('</LiteralConstant>').some(t=>t.includes('NID="40" UID="2212"')&&t.includes('RID="7"')&&t.includes('V="1"')));
wire(xml('0339'),'3046',['<PCon UId="3017" PinName="eno" />','<PCon UId="3020" PinName="en" />']);
wire(xml('0219'),'64',['<PCon UId="29" PinName="out" />','<PCon UId="30" PinName="pre" />','<PCon UId="31" PinName="in" />']);
wire(xml('0219'),'76',['<PCon UId="33" PinName="out" />','<PCon UId="78" PinName="in" />']);
assert.ok(declRaw('0596').split('</GlobalAccess>').some(t=>t.includes('N="DP_02"')&&t.includes('NID="29" UID="43"')&&t.includes('BO="1936"')));
assert.ok(declRaw('0596').split('</GlobalAccess>').some(t=>t.includes('N="DP_01_SOGLIA_1"')&&t.includes('NID="29" UID="44"')&&t.includes('BO="1104"')));
wire(xml('0202'),'604',['<PCon UId="603" PinName="out" />','<PCon UId="559" PinName="en" />']);
wire(xml('0264'),'1033',['<PCon UId="1032" PinName="out" />','<PCon UId="972" PinName="in5" />']);
/* MC03: OFF alarms, distinct standby/testing reset, and raw Monitor source. */
const mc03=standard.profile(data,'MC03');assert.equal(mc03.signal_trace.signals.length,17);assert.equal(mc03.alarm.timers[0].address,'%T53');assert.equal(mc03.alarm.alarms.length,2);
assert.equal((xml('0360').match(/<ORef /g)||[]).length,8);assert.ok(JSON.stringify(standard.items(data,'MC03','io')).includes('실제 피연산자 미결속')); 
wire(xml('0246'),'348',['<PCon UId="347" PinName="out" />','<PCon UId="349" PinName="in" />']);
wire(xml('0246'),'350',['<PCon UId="349" PinName="out" />','<PCon UId="306" PinName="in2" />']);
wire(xml('0246'),'354',['<PCon UId="353" PinName="out" />','<PCon UId="306" PinName="in3" />']);
wire(xml('0246'),'356',['<PCon UId="355" PinName="out" />','<PCon UId="318" PinName="in" />']);
for(const uid of ['347','349','353'])assert.match(xml('0246'),new RegExp('<Part UId="'+uid+'" Gate="Contact">\\s*<Negated PinName="operand" \/>'));
assert.ok(declRaw('0658').split('</SimpleAccess>').some(t=>t.includes('N="OFF"')&&t.includes('NID="10" UID="395"')&&t.includes('NID="11" UID="407"')&&t.includes('AO="1"')));
wire(xml('0426'),'21',['<PCon UId="432" PinName="out" />','<PCon UId="383" PinName="in" />']);
wire(xml('0426'),'424',['<PCon UId="423" PinName="out" />','<PCon UId="425" PinName="in" />']);
wire(xml('0426'),'426',['<PCon UId="425" PinName="out" />','<PCon UId="389" PinName="in" />']);
wire(xml('0426'),'430',['<PCon UId="429" PinName="out" />','<PCon UId="394" PinName="in" />']);
assert.match(xml('0427'),/<Part UId="426" Gate="Contact">\s*<Negated PinName="operand" \/>/);
wire(xml('0427'),'433',['<PCon UId="432" PinName="out" />','<PCon UId="406" PinName="in" />']);
wire(xml('0311'),'1308',['<OCon UId="1294" />','<PCon UId="1280" PinName="in" />']);
assert.ok(declRaw('0616').split('</LiteralConstant>').some(t=>t.includes('NID="23" UID="1294"')&&t.includes('RID="7"')&&t.includes('V="1"')));
wire(xml('0336'),'2854',['<PCon UId="2825" PinName="eno" />','<PCon UId="2828" PinName="en" />']);
assert.ok(declRaw('0556').split('</SimpleAccess>').some(t=>t.includes('N="MC03_torque"')&&t.includes('RID="240"')&&t.includes('AK="Monitor"')&&t.includes('AO="52"')));
const rawTorque=data.repair_record_forms.profiles.find(x=>x.key==='MC03').signals.find(x=>x.id==='raw-torque');assert.deepEqual(rawTorque.refs,[]);assert.deepEqual(rawTorque.reference_documents,['sources/decoded-original/0556-IdentXmlPart.xml']);
/* MC05: retain unavailable output/alarm logic and the actual OFF-gated Set. */
const mc05=standard.profile(data,'MC05');assert.deepEqual(mc05.alarm.timers,[]);assert.deepEqual(mc05.alarm.alarms,[]);
assert.ok(xml('0164').includes('<Part UId="458" Gate="RCoil"'));
assert.ok(xml('0165').includes('<Part UId="793" Gate="SCoil"'));
wire(xml('0165'),'1054',['<PCon UId="789" PinName="out" />','<PCon UId="1149" PinName="in" />']);
wire(xml('0165'),'1150',['<PCon UId="1149" PinName="out" />','<PCon UId="793" PinName="in" />']);
assert.ok(declRaw('0575').split('</SimpleAccess>').some(t=>t.includes('N="OFF"')&&t.includes('NID="4" UID="958"')&&t.includes('AO="1"')));
wire(xml('0336'),'2860',['<PCon UId="2831" PinName="eno" />','<PCon UId="2834" PinName="en" />']);
assert.ok(declRaw('0616').split('</LiteralConstant>').some(t=>t.includes('NID="51" UID="2846"')&&t.includes('V="0"')));
const mc05Form=data.repair_record_forms.profiles.find(x=>x.key==='MC05');
for(const id of ['output','raw-run','raw-torque'])assert.deepEqual(mc05Form.signals.find(x=>x.id===id).refs,[]);
assert.ok(JSON.stringify(standard.items(data,'MC05','circuits')).includes('E6.4(SS09)는 밖'));
/* LD01: door permission, alternate vibration branch, TON Q, and literal HOUR1. */
const ld=standard.profile(data,'LD01');assert.equal(ld.signal_trace.signals.length,35);
assert.deepEqual(Array.from(ld.alarm.timers,t=>t.preset),['S5T#2S','S5T#2S','T#10S']);
const ldm=xml('0259'),ldv=xml('0261'),ldton=xml('0161'),ldhour=xml('0322');
wire(ldm,'872',['<PCon UId="871" PinName="out" />','<PCon UId="873" PinName="in" />']);
wire(ldm,'874',['<PCon UId="873" PinName="out" />','<PCon UId="841" PinName="in" />']);
wire(ldv,'25',['<PCon UId="894" PinName="out" />','<PCon UId="31" PinName="in" />']);
wire(ldton,'25',['<PCon UId="21" PinName="Q" />','<PCon UId="282" PinName="in" />']);
assert.match(ldton,/<Part UId="314" Gate="Contact">\s*<Negated PinName="operand" \/>/);
assert.match(ldhour,/<ORef UId="2050" RefId="7" \/>/);
wire(ldhour,'2065',['<PCon UId="2036" PinName="out1" />','<OCon UId="2051" />']);
const ldf=data.repair_record_forms.profiles.find(x=>x.key==='LD01');
assert.deepEqual(Array.from(ldf.signals.find(x=>x.id==='local-vib-start').addresses),[]);
assert.deepEqual(Array.from(ldf.signals.find(x=>x.id==='level-ton').refs),[]);
const ldMap=JSON.parse(fs.readFileSync(__dirname+'/sources/decoded-original/network-map.json'));
for(const d of [1201,1202]){const row=ldMap.find(x=>x.document_id===d);assert.equal(row.inferred_original_nid,null);assert.equal(Object.keys(row.resolved_operands).length,0);assert.equal((xml(row.xml_file.slice(0,4)).match(/<ORef /g)||[]).length,8);}
/* BF01: shared cleaning and OFR are not physical Run or a second filter alarm. */
const bf1=standard.profile(data,'BF01');assert.equal(bf1.signal_trace.signals.length,34);
const bfEnable=xml('0219'),bfForza=xml('0200'),bfTime=xml('0201'),bfStep=xml('0218'),bfDP=xml('0540');
wire(bfEnable,'51',['<PCon UId="22" PinName="out" />','<PCon UId="23" PinName="in" />']);
wire(bfEnable,'53',['<PCon UId="23" PinName="out" />','<PCon UId="24" PinName="pre" />','<PCon UId="25" PinName="in" />']);
assert.match(bfEnable,/<Part UId="24" Gate="Le">/);
wire(bfForza,'22',['<PCon UId="460" PinName="out" />','<PCon UId="21" PinName="in2" />']);
wire(bfTime,'501',['<PCon UId="500" PinName="out" />','<PCon UId="457" PinName="en" />','<PCon UId="462" PinName="en" />']);
wire(bfStep,'49',['<PCon UId="23" PinName="out" />','<PCon UId="24" PinName="en" />','<PCon UId="25" PinName="pre" />','<PCon UId="27" PinName="pre" />']);
assert.equal(bf1.alarm.timers.find(t=>t.address==='%T114').preset,'S5T#3M');
assert.match(bfDP,/<Part UId="1146" Gate="Lt">/);assert.match(bfDP,/<Part UId="1149" Gate="Lt">/);
wire(bfDP,'1200',['<PCon UId="1149" PinName="out" />','<PCon UId="1152" PinName="in" />']);
const bff=data.repair_record_forms.profiles.find(x=>x.key==='BF01');
assert.deepEqual(Array.from(bff.signals.find(x=>x.id==='enable').addresses),[]);
assert.deepEqual(Array.from(bff.signals.find(x=>x.id==='run').addresses),['%M180.3']);
assert.deepEqual(Array.from(bff.signals.find(x=>x.id==='ofr').addresses),['DB3.DBX24.3']);
assert.equal(bf1.alarm.alarms.length,2);
/* BF02: own response chain, even step, DP02 interface, and source model conflict. */
const bf2=standard.profile(data,'BF02');assert.equal(bf2.signal_trace.signals.length,37);
wire(bfEnable,'62',['<PCon UId="28" PinName="out" />','<PCon UId="29" PinName="in" />']);
wire(bfEnable,'64',['<PCon UId="29" PinName="out" />','<PCon UId="30" PinName="pre" />','<PCon UId="31" PinName="in" />']);
wire(bfEnable,'76',['<PCon UId="33" PinName="out" />','<PCon UId="78" PinName="in" />']);
assert.match(bfEnable,/<Part UId="30" Gate="Le">/);
const bf2Pulse=xml('0205'),bf2Analog=xml('0522');
wire(bf2Pulse,'1007',['<PCon UId="894" PinName="out" />','<PCon UId="1066" PinName="in" />']);
wire(bf2Pulse,'1067',['<PCon UId="1066" PinName="out" />','<PCon UId="898" PinName="in" />']);
wire(bf2Analog,'24',['<PCon UId="1556" PinName="Out_of_range" />','<OCon UId="23" />']);
const bf2f=data.repair_record_forms.profiles.find(x=>x.key==='BF02');
assert.deepEqual(Array.from(bf2f.signals.find(x=>x.id==='run').addresses),['%M180.4']);
assert.deepEqual(Array.from(bf2f.signals.find(x=>x.id==='dp-raw').addresses),['%IW400:P']);
assert.deepEqual(Array.from(bf2f.signals.find(x=>x.id==='ofr').addresses),['DB3.DBX24.5']);
const bf2Circuits=JSON.stringify(standard.items(data,'BF02','circuits'));
assert.ok(bf2Circuits.includes('6ES7523-1BL00-0AA0')&&bf2Circuits.includes('6ES7523-1BL01-0AB0'));
assert.ok(!JSON.stringify(standard.items(data,'BF02','circuits').find(x=>x.id==='review-4-2')).includes('6ES7523-1BL01-0AA0'));
assert.equal(bf2f.signals.find(x=>x.id==='ofr').role,'responses');
/* Temperature channels keep their own call gates and lack-of-evidence boundaries. */
for(const [key,file,wireID,contact,call,raw,result]of [
 ['TC03','0491','376','375','356','%IW276:P','DB1.DBW112'],
 ['TC01','0489','336','335','316','%IW272:P','DB1.DBW110'],
 ['TC02','0490','356','355','336','%IW274:P','DB1.DBW108'],
 ['TC06','0492','396','395','376','%IW278:P','DB1.DBW120'],
 ['TC05','0482','86','85','66','%IW260:P','DB1.DBW118'],
 ['TC07','0493','416','415','396','%IW280:P','DB1.DBW190'],
 ['TC09','0483','106','105','86','%IW386:P','DB1.DBW262'],
 ['TC04','0481','66','65','46','%IW256:P','DB1.DBW116'],
 ['TC10','0484','126','125','106','%IW390:P','DB1.DBW264']]){
 const form=data.repair_record_forms.profiles.find(x=>x.key===key);
 assert.deepEqual(Array.from(form.signals.find(x=>x.id==='raw').addresses),[raw]);
 assert.deepEqual(Array.from(form.signals.find(x=>x.id==='result').addresses),[result]);
 wire(xml(file),wireID,[`<PCon UId="${contact}" PinName="out" />`,`<PCon UId="${call}" PinName="en" />`]);
}
const bearingAlarm=xml('0529');
wire(bearingAlarm,'560',['<PCon UId="559" PinName="out" />','<PCon UId="455" PinName="in" />']);
wire(bearingAlarm,'25',['<PCon UId="561" PinName="out" />','<PCon UId="22" PinName="in" />']);
wire(bearingAlarm,'26',['<PCon UId="22" PinName="out" />','<PCon UId="476" PinName="in" />']);
assert.match(bearingAlarm,/<Part UId="22" Gate="Contact"\s*\/>/);
assert.ok(!xml('0539').includes('Gate="SdCoil"'));
wire(xml('0539'),'1151',['<PCon UId="1068" PinName="out" />','<PCon UId="1177" PinName="in" />','<PCon UId="1082" PinName="in" />']);
for(const [key,page]of [['TC03',32],['TC01',56],['TC02',56],['TC06',23],['TC05',33],['TC07',30],['TC09',60],['TC04',33]]){
 const drawing=data.drawing_workspace.profiles.find(x=>x.key===key),path=drawing.circuit.paths.find(x=>x.fg===null);
 assert.equal(path.sheet_id,'construction-'+page);assert.equal(drawing.sheets.find(x=>x.id===path.sheet_id).page,page);
}
const tc10draw=data.drawing_workspace.profiles.find(x=>x.key==='TC10');assert.equal(tc10draw.circuit.paths.length,0);
const tc11=standard.profile(data,'TC11'),tc11form=data.repair_record_forms.profiles.find(x=>x.key==='TC11');
assert.equal(tc11.source_pairs.length,0);assert.equal(tc11.alarm.timers.length,0);assert.equal(tc11.alarm.alarms.length,0);
assert.ok(tc11form.signals.every(x=>x.addresses.length===0&&x.refs.length===0));
assert.equal(data.drawing_workspace.profiles.find(x=>x.key==='TC11').circuit.paths.length,0);
console.log(JSON.stringify({status:'passed',catalog_profiles:keys,scope:'catalog identity, original hashes, native call and alarm branches, temperature gate differences, TC10 external endpoints and TC11 PLC evidence unavailable, safe rendering and record preservation; no PLC execution'}));

// PV05: preserved tank-ready logic and external valve circuit, never PLC behavior execution.
if(keys.includes('PV05')) {
 const nitrogen=standard.profile(data,'PV05'),nx=xml('0538');
 assert.equal(nitrogen.alarm.timers.length,0);
 assert.equal(nitrogen.signal_trace.signals.length,9);
 for(const uid of ['955','964'])assert.match(nx,new RegExp('<Part UId="'+uid+'" Gate="Contact"><Negated PinName="operand" />'));
 assert.match(nx,/<Part UId="27" Gate="Contact" \/>/);
 wire(nx,'29',['<PCon UId="27" PinName="out" />','<PCon UId="929" PinName="in" />']);
 wire(nx,'33',['<PCon UId="31" PinName="out" />','<PCon UId="935" PinName="in" />']);
 wire(nx,'34',['<PCon UId="964" PinName="out" />','<PCon UId="31" PinName="in2" />']);
 assert.equal((nx.match(/<Part /g)||[]).length,10);assert.equal((nx.match(/<Wire /g)||[]).length,18);
 const cfg=JSON.parse(fs.readFileSync(__dirname+'/catalog-profiles/PV05.json'));
 assert.equal(cfg.drawing.circuit.paths.length,6);
 assert.deepEqual(cfg.drawing.circuit.paths.filter(p=>p.source_pair_status==='not_identified').map(p=>p.signal),['박스 전원','공통 요청','자동 부하','PV05 직접 가지']);
 assert.equal(cfg.draft_sha256,'2c4b9395ce65cedf795f2b3277f9ffc60df93826edccf322e602353ad98ce17f');
 const branch=cfg.drawing.circuit.paths.find(p=>p.signal==='PV05 직접 가지');assert.ok(branch.nodes.some(s=>s.includes('X2:13')));assert.ok(branch.nodes.some(s=>s.includes('X2:14')));assert.ok(!branch.nodes.some(s=>s.includes('96KT1')));
 assert.ok(cfg.extra_sources.includes('sources/decoded-original/0634-IdentXmlPart.xml'));
 console.log(JSON.stringify({status:'passed',scope:'PV05 exact original pins, original draft, unavailable direct PLC pairs, 6 electrical paths; static only'}));
}

// ZT01: own channel, S/R overlap, and FN01-owned downstream timing. Static evidence only.
if(keys.includes('ZT01')) {
 const cfg=JSON.parse(fs.readFileSync(__dirname+'/catalog-profiles/ZT01.json'));
 const form=data.repair_record_forms.profiles.find(x=>x.key==='ZT01');
 for(const [id,addr] of [['raw-p','%IW282:P'],['raw-i','%IW282'],['mirror','DB13.DBW46'],['value','DB1.DBW192'],['ofr','DB3.DBX21.7'],['vibration','DB3.DBX9.0']]) assert.deepEqual(Array.from(form.signals.find(s=>s.id===id).addresses),[addr]);
 assert.deepEqual(Array.from(form.signals.find(s=>s.id==='local-stop').addresses),[]);
 const zx=xml('0494'), za=xml('0536'), zf=xml('0252'), zs=xml('0253');
 wire(zx,'28',['<PCon UId="435" PinName="out" />','<PCon UId="416" PinName="en" />']);
 wire(zx,'430',['<OCon UId="423" />','<PCon UId="416" PinName="IN0" />']);
 wire(zx,'431',['<OCon UId="424" />','<PCon UId="416" PinName="Analog_input" />']);
 wire(zx,'434',['<OCon UId="427" />','<PCon UId="416" PinName="OutValue" />']);
 wire(xml('0398'),'94',['<OCon UId="82" />','<PCon UId="75" PinName="in" />']);
 wire(xml('0398'),'95',['<OCon UId="83" />','<PCon UId="75" PinName="out1" />']);
 wire(za,'907',['<PCon UId="906" PinName="out" />','<PCon UId="862" PinName="in" />']);
 wire(za,'900',['<PCon UId="866" PinName="out" />','<PCon UId="869" PinName="in" />']);
 assert.match(za,/<Part UId="848" Gate="Gt">/);assert.match(za,/<Part UId="851" Gate="Lt">/);assert.match(za,/<Part UId="866" Gate="Lt">/);
 wire(zf,'698',['<PCon UId="697" PinName="out" />','<PCon UId="707" PinName="in3" />']);
 wire(zf,'27',['<PCon UId="705" PinName="out" />','<PCon UId="661" PinName="in" />']);
 wire(zs,'721',['<PCon UId="720" PinName="out" />','<PCon UId="676" PinName="in4" />']);
 assert.equal(cfg.alarm_reference.timers.find(t=>t.address==='%T123').preset,'S5T#10S');
 assert.equal(cfg.alarm_reference.timers.find(t=>t.address==='%T130').preset,'S5T#1H_30M');
 assert.equal(cfg.draft_sha256,'c3fabd9f9a34ad5433610642f11ad6703bee2065d89703c73865ffa433e761fb');
 assert.equal(cfg.drawing.circuit.paths.find(p=>p.signal==='시공 후보').sheet_id,'construction-58');
 assert.ok(cfg.drawing.circuit.paths.find(p=>p.signal==='모듈 원시 입력').nodes.some(s=>s.includes('26 I5+')));
 console.log(JSON.stringify({status:'passed',scope:'ZT01 native channel/gates, own 10s versus shared FN01 90min, S/R overlap preserved, construction sheet selection; no execution'}));
}

// PV06 keeps its external timed branch, separate from PV05 direct branch.
if(keys.includes('PV06')) {
 const cfg=JSON.parse(fs.readFileSync(__dirname+'/catalog-profiles/PV06.json'));
 assert.equal(cfg.draft_sha256,'f07123ef8c0ab2d8c53f84fac8704841eec0c30f87d64a4250b5123c92ab1305');
 assert.equal(cfg.alarm_reference.timers.length,0);
 const path=cfg.drawing.circuit.paths.find(p=>p.signal==='PV06 시간접점 가지');
 for(const text of ['96KT1 접점18–15','X2:15','X2:16'])assert.ok(path.nodes.some(n=>n.includes(text)));
 assert.ok(!path.nodes.some(n=>n.includes('X2:13')||n.includes('X2:14')));
 assert.equal(path.source_pair_status,'not_identified');assert.equal(path.native_symbol_references.length,0);
 const out=xml('0401');
 wire(out,'64',['<OCon UId="39" />','<PCon UId="25" PinName="in" />']);
 wire(out,'66',['<PCon UId="25" PinName="out1" />','<OCon UId="40" />']);
 const form=data.repair_record_forms.profiles.find(x=>x.key==='PV06');
 assert.deepEqual(Array.from(form.signals.find(s=>s.id==='output-word').addresses),['%QW6']);
 assert.deepEqual(Array.from(form.signals.find(s=>s.id==='output-mirror').addresses),['DB14.DBW6']);
 assert.ok(cfg.extra_sources.includes('sources/decoded-original/0634-IdentXmlPart.xml'));
 assert.ok(cfg.drawing.sheets.some(s=>s.id==='pid'&&s.page===1));
 console.log(JSON.stringify({status:'passed',scope:'PV06 external timed branch and output-word mirror direction; PLC timer count0 not external timer absence'}));
}

// Passive stack records are observations, never imported nearby PLC signals.
for(const [key,hash] of [['CM01','2755852ef71fb8152f53e3b090e2fb275ab8614a9693d36482927f82e0ccd86c'],['CM02','50678774825f2a19c684b68b701432ecb8f57b796a0fe7b3b9d240e6a430fc7b']])if(keys.includes(key)){
 const cfg=JSON.parse(fs.readFileSync(__dirname+'/catalog-profiles/'+key+'.json'));
 assert.equal(cfg.draft_sha256,hash);assert.equal(cfg.signal_reference.signals.length,0);
 assert.equal(cfg.extra_locations.length,0);assert.equal(cfg.source_pairs.length,0);
 assert.equal(cfg.alarm_reference.alarms.length,0);assert.equal(cfg.alarm_reference.timers.length,0);
 assert.equal(cfg.drawing.circuit.paths.length,0);
 assert.ok(cfg.record_form.signals.length>0&&cfg.record_form.signals.every(s=>s.addresses.length===0&&s.refs.length===0));
 assert.equal(cfg.drawing.sheets.find(s=>s.id==='pid').fg,null);
 console.log(JSON.stringify({status:'passed',scope:key+' passive identity and observation records, own PLC/paths unverified; related ownership not imported'}));
}

if(keys.includes('UC01')) {
 const cfg=JSON.parse(fs.readFileSync(__dirname+'/catalog-profiles/UC01.json'));
 assert.equal(cfg.draft_sha256,'ab5809bcf9b27971ef2bf0a2c208973f00f67537481fe8aeb3e511aaa2f9666a');
 assert.equal(cfg.signal_reference.signals.length,0);assert.equal(cfg.source_pairs.length,0);assert.equal(cfg.drawing.circuit.paths.length,0);
 assert.ok(cfg.record_form.signals.every(s=>!s.addresses.length&&!s.refs.length));
 for(const page of [3,5,32,58])assert.ok(cfg.drawing.sheets.find(s=>s.page===page).revision.includes('CHECKED J.H.Kim'));
 assert.ok(JSON.stringify(cfg.supplements).includes('core2'));assert.ok(JSON.stringify(cfg.supplements).includes('core4S'));
 console.log(JSON.stringify({status:'passed',scope:'UC01 location versus ownership, masked rows/cores unresolved, checked versus approved footer correction'}));
}
if(keys.includes('PV14')) {
 const cfg=JSON.parse(fs.readFileSync(__dirname+'/catalog-profiles/PV14.json')), output=xml('0216'), alarm=xml('0215');
 assert.equal(cfg.draft_sha256,'d6bf4ab3c186d9859fd4d4ebc33f992217741cf444d81b3ea8bc6f7f89f942a0');
 wire(output,'25',['<PCon UId="2037" PinName="out" />','<PCon UId="2004" PinName="in" />']);
 wire(output,'2031',['<PCon UId="2007" PinName="out" />','<PCon UId="2012" PinName="in" />']);
 wire(output,'24',['<PCon UId="22" PinName="out" />','<PCon UId="2007" PinName="in5" />']);
 for(const uid of ['2032','2034','2036'])assert.match(alarm,new RegExp('<Part UId="'+uid+'" Gate="Contact">\\s*<Negated PinName="operand" />'));
 wire(alarm,'2016',['<PCon UId="1979" PinName="out" />','<PCon UId="1986" PinName="in" />','<PCon UId="2038" PinName="in" />']);
 wire(alarm,'2039',['<PCon UId="2038" PinName="out" />','<PCon UId="1991" PinName="in" />']);
 wire(alarm,'2043',['<PCon UId="2042" PinName="out" />','<PCon UId="1996" PinName="in" />']);
 wire(xml('0397'),'111',['<PCon UId="112" PinName="operand" />','<OCon UId="113" />']);
 wire(xml('0397'),'104',['<PCon UId="105" PinName="operand" />','<OCon UId="106" />']);
 assert.equal(cfg.alarm_reference.timers.length,1);assert.equal(cfg.alarm_reference.timers[0].preset,'S5T#20S');
 for(const [id,addr]of [['output','%Q17.0'],['open','DB13.DBX22.0'],['hmi-open','DB11.DBX74.0'],['reset','DB2.DBX6.0'],['hmi-reset','DB2.DBX13.4']])assert.deepEqual(cfg.record_form.signals.find(s=>s.id===id).addresses,[addr]);
 for(const id of ['hmi-open','hmi-close','hmi-reset'])assert.equal(cfg.record_form.signals.find(s=>s.id===id).refs.length,0);
 assert.ok(cfg.drawing.circuit.paths.find(p=>p.signal==='밸브 부하').nodes.some(s=>s.includes('5–9')));
 for(const p of [35,60])assert.ok(cfg.drawing.sheets.find(s=>s.page===p).revision.includes('CHECKED J.H.Kim'));
 console.log(JSON.stringify({status:'passed',scope:'PV14 five-request OR, fault clears manual only, own20s alarm, HMI mismatches and source footer correction'}));
}

if(keys.includes('CR01')) {
 const cfg=JSON.parse(fs.readFileSync(__dirname+'/catalog-profiles/CR01.json'));
 assert.equal(cfg.drawing.circuit.paths.length,0);assert.equal(cfg.alarm_reference.alarms.length,0);
 const x=xml('0457');assert.match(x,/<Part UId="23" Gate="Contact">\s*<Negated PinName="operand" \/>/);
 wire(x,'41',['<PCon UId="23" PinName="out" />','<PCon UId="27" PinName="in" />']);
 wire(x,'45',['<PCon UId="36" PinName="out" />','<PCon UId="37" PinName="in" />']);
 wire(xml('0397'),'90',['<PCon UId="78" PinName="out1" />','<OCon UId="82" />']);
 assert.ok(cfg.record_form.signals.every(s=>s.boundary.includes('공통 계통')));
 console.log(JSON.stringify({status:'passed',scope:'CR01 cabinet identity and related common110V evidence, no exclusive ownership assigned'}));
}
if(keys.includes('SYS-AUTO')) {
 const cfg=JSON.parse(fs.readFileSync(__dirname+'/catalog-profiles/SYS-AUTO.json'));
 assert.equal(cfg.type,'software');assert.equal(cfg.drawing.sheets.length,0);assert.equal(cfg.drawing.circuit.paths.length,0);assert.equal(cfg.record_form.signals.length,12);
 assert.equal(cfg.alarm_reference.timers.length,6);
 const display=xml('0163');assert.match(display,/<Part UId="115" Gate="Contact">\s*<Negated PinName="operand" \/>/);
 wire(display,'107',['<PCon UId="87" PinName="out1" />','<OCon UId="99" />']);
 wire(display,'111',['<PCon UId="93" PinName="out1" />','<OCon UId="102" />']);
 wire(xml('0164'),'851',['<PCon UId="835" PinName="Q" />','<PCon UId="837" PinName="in" />']);
 wire(xml('0168'),'35',['<PCon UId="22" PinName="eno" />','<PCon UId="23" PinName="en" />']);
 wire(xml('0237'),'50',['<PCon UId="49" PinName="out" />','<PCon UId="34" PinName="in" />','<PCon UId="36" PinName="in" />']);
 for(const [lr,w,m]of [['58','126','60'],['63','137','65'],['68','148','70'],['72','156','74'],['76','164','78']])wire(xml('0169'),w,[`<PCon UId="${lr}" PinName="Q" />`,`<PCon UId="${m}" PinName="en" />`]);
 console.log(JSON.stringify({status:'passed',scope:'SYS-AUTO software signals, display branch direction, request versus safety/output, TON LRef boundaries'}));
}
if(keys.includes('SYS-HMI')) {
 const cfg=JSON.parse(fs.readFileSync(__dirname+'/catalog-profiles/SYS-HMI.json'));
 assert.equal(cfg.type,'software');assert.equal(cfg.drawing.circuit.paths.length,0);
 for(const id of ['local-run','local-response','local-alarm','status'])assert.deepEqual(cfg.record_form.signals.find(s=>s.id===id).addresses,[]);
 wire(xml('0355'),'57',['<PCon UId="41" PinName="out" />','<PCon UId="59" PinName="in" />']);
 wire(xml('0401'),'84',['<PCon UId="32" PinName="out1" />','<OCon UId="54" />']);
 wire(xml('0401'),'88',['<PCon UId="85" PinName="out1" />','<OCon UId="90" />']);
 wire(xml('0158'),'38',['<PCon UId="28" PinName="out" />','<PCon UId="33" PinName="in" />','<PCon UId="40" PinName="in" />','<PCon UId="64" PinName="IN" />','<PCon UId="73" PinName="IN" />']);
 for(const [lr,w,coil]of [['64','67','48'],['73','77','60']])wire(xml('0158'),w,[`<PCon UId="${lr}" PinName="Q" />`,`<PCon UId="${coil}" PinName="in" />`]);
 const map=JSON.parse(fs.readFileSync(__dirname+'/sources/decoded-original/network-map.json')),caller=map.find(n=>n.document_id===1178);
 assert.equal(caller.inferred_original_nid,null);assert.equal(Object.keys(caller.resolved_operands).length,0);
 console.log(JSON.stringify({status:'passed',scope:'SYS-HMI local/global separation, QW mirror direction, separate Reset requests and TOF, unresolved caller retained'}));
}
if(keys.includes('PV14')){
 const cfg=JSON.parse(fs.readFileSync(__dirname+'/catalog-profiles/PV14.json')),p=cfg.drawing.circuit.paths.find(p=>p.signal==='출력');
 assert.ok(p.nodes.some(n=>n.includes('단자39 3L+')&&!/단자\s*40(?:\s|$)|\b3M\b/.test(n)));
 assert.ok(p.nodes.some(n=>n.includes('단자40 3M→−0Vdc152.4')));
}
// UI role labels must not turn ordinary Coil/processed data into latch/raw-input claims.
if(keys.includes('SYS-HMI')){
 const c=JSON.parse(fs.readFileSync(__dirname+'/catalog-profiles/SYS-HMI.json'));
 for(const id of ['physical-reset','local-alarm','local-run','out0','out20','out22'])assert.equal(c.record_form.signals.find(s=>s.id===id).role,'responses');
}
if(keys.includes('ZT01')){
 const c=JSON.parse(fs.readFileSync(__dirname+'/catalog-profiles/ZT01.json'));
 for(const id of ['ofr','prealarm'])assert.equal(c.record_form.signals.find(s=>s.id===id).role,'responses');
}
