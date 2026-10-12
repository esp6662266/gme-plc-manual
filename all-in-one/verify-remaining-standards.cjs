/* Critical backup pin directions and ownership boundaries; no PLC execution. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const read=f=>fs.readFileSync(path.join(__dirname,f),'utf8');
const data=JSON.parse(read('registers/all-in-one-data.json'));
const map=new Map(JSON.parse(read('sources/decoded-original/network-map.json')).map(n=>[n.document_id,n]));
const xml=n=>read('sources/decoded-original/'+map.get(n).xml_file);
const part=(n,uid,gate)=>assert.match(xml(n),new RegExp('<Part UId="'+uid+'" Gate="'+gate+'"'));
function wire(n,uid,pins){const body=xml(n).match(new RegExp('<Wire UId="'+uid+'">[\\s\\S]*?</Wire>'))?.[0];assert.ok(body,n+':'+uid);for(const pin of pins)assert.ok(body.includes(pin),n+':'+uid+':'+pin);}
const p=(u,pin)=>'<PCon UId="'+u+'" PinName="'+pin+'" />',o=u=>'<OCon UId="'+u+'" />';
part(1070,'78','Move');wire(1070,'88',[o('81'),p('78','in')]);wire(1070,'90',[p('78','out1'),o('82')]);wire(1070,'89',[p('78','eno'),p('79','en')]);
const globalWord=read('sources/decoded-original/0629-IdentXmlPart.xml').split('</GlobalAccess>').find(t=>t.includes('RID="26"')&&t.includes('NID="1" UID="82"'));
assert.ok(globalWord&&globalWord.includes('AO="144"')&&globalWord.includes('BIRID="4"')&&globalWord.includes('AK="Write"'));
const wordInput=read('sources/decoded-original/0627-IdentXmlPart.xml').split('</SimpleAccess>').find(t=>t.includes('RID="25"')&&t.includes('NID="1" UID="81"'));
assert.ok(wordInput?.includes('AO="144"')&&wordInput.includes('R="Input"')&&wordInput.includes('T="Word:'));
const inputParent=read('sources/decoded-original/0628-IdentXmlPart.xml').split('</DepDBBlock>').find(t=>t.includes('RID="4"')&&t.includes('NID="1" UID="82"'));
assert.ok(inputParent?.includes('<TOD N="13"'));
part(1614,'69','Move');wire(1614,'92',[o('82'),p('69','in')]);wire(1614,'93',[p('69','out1'),o('83')]);
part(1616,'144','Move');wire(1616,'167',[o('157'),p('144','in')]);wire(1616,'168',[p('144','out1'),o('158')]);
// Siren coil is parallel with the SD timer. It is not delayed by a series timer contact.
wire(933,'295',[p('256','out'),p('261','in'),p('265','in')]);wire(933,'288',[p('265','operand'),o('279')]);
// Edge memory is a separate pin, not an additional emergency cause.
part(1846,'21','PContact');wire(1846,'49',[p('21','bit'),o('51')]);wire(1846,'50',[p('21','operand'),o('52')]);wire(1846,'48',[p('21','out'),p('22','en')]);wire(1846,'35',[p('22','eno'),p('23','en')]);
// Run-hour token is Move literal1, not a cumulative Add to HOUR.
part(1018,'1118','Move');assert.ok(!xml(1018).includes('<Part UId="1118" Gate="Add"'));
wire(1018,'1146',[o('1132'),p('1118','in')]);wire(1018,'1147',[p('1118','out1'),o('1133')]);
const one=read('sources/decoded-original/0616-IdentXmlPart.xml').split('</LiteralConstant>').find(t=>t.includes('NID="20" UID="1132"'));
assert.ok(one?.includes('V="1"'));
part(1776,'1693','Add');wire(1776,'1756',[p('1693','out'),o('1732')]);
// PV02 raw Close and processed Close references are both contacts, not Coil writes.
part(1923,'30','Contact');part(1923,'31','Contact');wire(1923,'65',[o('44'),p('30','operand')]);wire(1923,'67',[o('45'),p('31','operand')]);
const keys=data.catalog_rollout_scope.current_batch_catalog_ids;
assert.equal(keys.length,81);assert.equal(new Set(keys).size,81);assert.equal(data.equipment_standards.profiles.length,149);
const profile=k=>data.equipment_standards.profiles.find(p=>p.selection_key===k),schema=k=>data.repair_record_forms.profiles.find(p=>p.key===k);
for(const k of keys){const v=profile(k),s=schema(k);assert.ok(v&&s,k);assert.equal(v.field_verified,false);assert.equal(v.tia_verified,false);assert.equal(v.repairs_completed,0);assert.ok(v.completion.existing_pending.length);assert.ok(s.signals.length);for(const section of ['overview','io','control','circuits','alarms','repair','completion'])assert.ok(v.reviewed_sections[section]?.length,k+':'+section);}
for(const k of ['CY01','CY02','CY03','CY04','CY05','CYL-CL01','CYL-CL02','CYL-CL03','CYL-CL04','CYL-CL05','CYL-CL06','CYL-CL07','CYL-CL08','CYL-CL09','CYL-CL10','CYL-CL12','ZT02','ZT03','ZT04','ZT05','ZT06','LS34','LS35']){
 assert.ok(schema(k).signals.every(x=>!x.addresses.length&&!x.refs.length),k+':no borrowed parent PLC channel');
}
assert.equal(profile('SYS-SIMULATION').type,'software_reference_only');assert.equal(profile('SYS-SIMULATION').source_pairs.length,0);
assert.ok(JSON.stringify(profile('SYS-SIMULATION').reviewed_sections).includes('영구중지'));
for(const name of ['DOTS-REMAINING-HANDOFF-20261012.json','DOTS-ASSET-62-HANDOFF-20261012.json']){
 const receipt=JSON.parse(read('catalog-sources/'+name));for(const f of receipt.files){const b=fs.readFileSync(path.join(__dirname,'catalog-sources',f.file));assert.equal(b.length,f.bytes);assert.equal(crypto.createHash('sha256').update(b).digest('hex'),f.sha256);}
}
console.log(JSON.stringify({status:'passed',new_documents:81,total_preserved_manuals:149,official_original_drafts:71,scope:'original Word directions, edge-memory pins, direct horn coil, HOUR Move1, Close raw/processed contacts, non-borrowed component channels and stopped reference document; no PLC execution'}));
