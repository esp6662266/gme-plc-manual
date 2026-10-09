"""Validate application data contracts and every dynamic document route.

This checks integration and preserved evidence, not PLC or simulator execution.
Browser observations are recorded separately in all-in-one-browser-verification.json.
"""
from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import hashlib
import csv
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
(ROOT/'all-in-one-verification.json').write_text(json.dumps(dict(status='checking',scope='Current integration/source checks; no execution'))+'\n')
data = json.loads((ROOT / 'registers/all-in-one-data.json').read_text())
source = json.loads((ROOT / 'registers/control-spec.json').read_text())
specs = {s['id']: s for s in source['specifications']}

class Ids(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.add(attrs['id'])

assert len(data['equipment']) == len(specs) == 248
assert len({d['id'] for d in data['equipment']}) == 248
assert len(data['priority']) == len({p['key'] for p in data['priority']}) == 23
assert Counter(p['match'] for p in data['priority']) == {'tag':14, 'candidate':4, 'unknown':5}
assert all(not p['identity_verified'] for p in data['priority'])
assert all(not p['plc_id'] or p['plc_id'] in specs for p in data['priority'])
assert all(not p['plc_id'] for p in data['priority'] if p['match'] == 'unknown')
assert not data['priority_source']['edges_imported']
assert data['execution'] == {'engine_implemented':True, 'plc_connected':False, 'tia_verified':False, 'full_cpu_emulation':False}
assert data['virtual_results']['failed'] == 0
assert data['virtual_results']['full_design_tests_passed'] == 0
assert data['program_counts']['networks'] == 426
assert data['virtual_results']['model_sha256'] == hashlib.sha256((ROOT/'registers/program-model.json').read_bytes()).hexdigest()
assert len(data['tests']) == 577 and all(t['상태'] == '설계·미실행' for t in data['tests'])
assert len(data['verification']) == 1060 and all(v['상태'] == '확인 대기' for v in data['verification'])
assert len(data['conflicts']) == 18
assert data['work_scope']['simulator_development']=='stopped_by_user'
assert data['work_scope']['simulator_tests']=='frozen'
freeze=json.loads((ROOT/'registers/simulator-freeze.json').read_text())
assert all(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==digest for f,digest in freeze['files'].items())
construction=json.loads((ROOT/'registers/construction-reference.json').read_text())
assert data['construction_reference']==construction
assert construction['pages']==64 and construction['equipment_guides']==22
assert construction['field_verified']==construction['plc_changes']==construction['simulator_changes']==0
assert not construction['approved_as_built_verified']
assert hashlib.sha256((ROOT/construction['source']).read_bytes()).hexdigest()==construction['sha256']
construction_text={p['page']:p['text'] for p in json.loads((ROOT/'sources/can-decoating-page-text.json').read_text())}
construction_pages=json.loads((ROOT/'registers/construction-page-index.json').read_text())
assert [p['page'] for p in construction_pages]==list(range(1,65))
assert all(p['drawing_code'] in construction_text[p['page']] for p in construction_pages)
masked={(m['page'],r) for m in construction['masked_rows'] for r in m['rows']}
cables=json.loads((ROOT/'registers/construction-power-cables.json').read_text())+json.loads((ROOT/'registers/construction-control-cables.json').read_text())
assert len(cables)==construction['power_rows']+construction['control_rows']==51
assert len({r['key'] for r in cables})==len(cables)
assert len(masked)==construction['masked_rows_known']==9
assert all((r['page'],r['row']) not in masked and r['visible'] and not r['field_verified'] for r in cables)
assert all(r['cable'] in construction_text[r['page']] and r['row'] in construction_text[r['page']] for r in cables)
assert all(r['page'] not in [19,50] for r in cables)
construction_reviews=json.loads((ROOT/'registers/construction-review.json').read_text())
assert len(construction_reviews['items'])==construction['new_review_items']==7
assert all(not r['resolved'] and not r['field_verified'] for r in construction_reviews['items'])
assert len(construction['priority'])==23 and sum(not p['guide'] for p in construction['priority'])==5
assert all(not p['plc_id'] and not p['guide'] for p in construction['priority'] if p['match']=='unknown')
assert data['review_counts']['improvement_candidates'] == len(json.loads((ROOT/'registers/improvement-review.json').read_text())['items'])
electrical=json.loads((ROOT/'registers/electrical-trace.json').read_text())
assert data['review_counts']['electrical_paths'] == sum(len(d['paths']) for d in electrical['devices'])
assert data['review_counts']['electrical_devices'] == len(electrical['devices'])
assert electrical['field_verified'] == 0 and electrical['plc_changes'] == 0
symbols=list(csv.DictReader((ROOT/'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
symbols_by_address={s['백업 주소'].upper():s['원본 심볼'].lower() for s in symbols}
page_text={p['page']:p['text'] for p in json.loads((ROOT/'sources/electrical-page-text.json').read_text())}
native_networks={n['id']:n for n in json.loads((ROOT/'registers/program-model.json').read_text())['networks']}
unresolved_addresses=0
direct_references=0
def fg_page(fg):return int(fg)+(1 if int(fg)>5 else 0)+(2 if int(fg)>180 else 0)
for d in electrical['devices']:
    assert d['id'] in specs
    assert d['pages']==[fg_page(f) for f in d['sheets']]
    assert all((ROOT/'assets/circuits'/f'FG{f}.png').is_file() for f in d['sheets'])
    for path in d['paths']:
        if path['backup'] is None:
            unresolved_addresses+=1
            assert path['backup_verified'] is False and path['backup_status']=='address_unresolved'
            assert not path['native_symbol_references']
            assert len(path['drawing_labels'])==2
        else:
            address,name=path['backup'].split(' / ',1)
            assert symbols_by_address[address.upper()]==name.lower(),(d['id'],path['backup'])
            expected={(n['id'],uid) for n in native_networks.values() for uid,r in n['refs'].items() if (r['name'] or '').casefold()==name.casefold()}
            observed={(r['network'],r['uid']) for r in path['native_symbol_references']}
            assert observed==expected,(d['id'],path['backup'],'direct references')
            for ref in path['native_symbol_references']:
                n=native_networks[ref['network']]
                assert n['refs'][ref['uid']]['name'].casefold()==name.casefold()
                assert ref['file']==n['file'] and ref['block']==n['block']
                direct_references+=1
        for label in path.get('drawing_labels',[path['drawing']]):
            label=label.replace('±','')
            assert label in page_text[fg_page(path['fg'])],(d['id'],path['fg'],label)
    assert all(id in native_networks for id in d['networks'])
assert unresolved_addresses==electrical['unresolved_backup_addresses']==3
assert direct_references==electrical['direct_symbol_reference_count']
assert electrical['simulator_behavior_tests']=='not_rerun'
signal_trace=json.loads((ROOT/'registers/signal-trace.json').read_text())
assert signal_trace['source_networks']==426 and len(signal_trace['devices'])==data['review_counts']['signal_guides']==19
assert len(signal_trace['usages'])==signal_trace['usage_count']==data['review_counts']['signal_pin_usages']==4961
assert signal_trace['field_verified']==signal_trace['plc_changes']==0 and signal_trace['simulator_behavior_tests']=='not_rerun'
assert hashlib.sha256((ROOT/signal_trace['source']).read_bytes()).hexdigest()==signal_trace['source_sha256']
local=lambda x:x.tag.rsplit('}',1)[-1]
xmls={id:ET.parse(ROOT/n['file']).getroot() for id,n in native_networks.items()}
wires={id:{w.get('UId'):w for w in root.iter() if local(w)=='Wire'} for id,root in xmls.items()}
parts={id:{p.get('UId'):p.get('Gate') for p in root.iter() if local(p)=='Part'} for id,root in xmls.items()}
source_maps={n['document_id']:n for n in json.loads((ROOT/'sources/decoded-original/network-map.json').read_text())}
declaration_docs={}
for r in signal_trace['usages']:
    n=native_networks[r['network']];wire=wires[r['network']][r['wire']]
    assert n['file']==r['file'] and n['block']==r['block']
    assert any(local(x)=='OCon' and x.get('UId')==r['oref'] for x in wire)
    assert any(local(x)=='PCon' and x.get('UId')==r['part'] and x.get('PinName')==r['pin'] for x in wire)
    assert parts[r['network']].get(r['part'],'CRef')==r['gate']
    assert n['refs'][r['oref']]['name']==r['name']
    for decl in r['declarations']:
        if decl['file'] not in declaration_docs:declaration_docs[decl['file']]=ET.parse(ROOT/decl['file']).getroot()
        matched=False
        for node in declaration_docs[decl['file']]:
            ident=next((x for x in node if local(x)=='ID'),None)
            if ident is None or ident.get('RID')!=n['refs'][r['oref']]['ref_id']:continue
            for c in ident.iter():
                if local(c)=='C' and c.get('UID')==r['oref'] and c.get('NID')==source_maps[r['network']]['inferred_original_nid']:
                    if decl['kind']==local(node) and decl['scope']==ident.get('S') and decl['access_kind']==c.get('AK'):matched=True
        assert matched,(r['network'],r['oref'],decl)
    if r['scope']=='Global':assert r['declarations'] and all(d['scope']=='Global' for d in r['declarations'])
    elif r['name']:assert r['identity'].startswith(r['block']+'::')
    if r['role']=='write':
        assert (r['gate'] in ('Coil','SCoil','RCoil','SdCoil') and r['pin']=='operand') or (r['gate'] in ('Move','Add','Sub','Mul','Div','Convert') and re.fullmatch(r'out\d*',r['pin'])) or (r['declarations'] and all(d['access_kind']=='Write' for d in r['declarations']))
signal_devices={d['id']:d for d in signal_trace['devices']}
fn04_run=next(s for s in signal_devices['FN04']['signals'] if s['name'].casefold()=='inputs.fn04 run')
assert fn04_run['global_write_networks']==[1070,1085] and fn04_run['global_writes']==2
mv03_open=next(t for t in signal_trace['transfers'] if t['network']==1070 and t['part']=='147')
assert mv03_open['source']=='MV03_Open' and mv03_open['target']=='Inputs.MV03 open' and mv03_open['inverted'] is True
assert any(r['name']=='BR01_GAS_SP' and r['network']==1687 and r['gate']=='Mul' and r['pin']=='out' and r['role']=='write' for r in signal_trace['usages'])
assert any(r['name']=='Risposta' and r['block']=='hmi standard motors' and r['scope']=='Local' for r in signal_trace['usages'])
assert all(s['global_writes']==sum(r['role']=='write' and r['scope']=='Global' for r in s['usages']) for d in signal_trace['devices'] for s in d['signals'])
assert signal_trace['main_calls']==[c for c in json.loads((ROOT/'registers/program-model.json').read_text())['calls'] if c['caller']=='main' and str(c['callee']).casefold() in ('simulation','hmi inputs','hmi output','motors 1','r1 scraps gate 2','burner control','valve control loop')]
common=json.loads((ROOT/'registers/common-control.json').read_text())
assert len(common['priority_profiles'])==data['review_counts']['common_guides']==23
assert len(common['networks'])==31 and len(common['stages'])==97 and len(common['checks'])==10
assert common['plc_changes']==common['field_verified']==0
assert common['simulator_development']=='stopped_by_user' and common['simulator_behavior_tests']=='not_rerun'
assert all(c['status']=='확인 대기' for c in common['checks'])
for path,digest in common['sources'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
def operand_at(id,uid,pin):
    refs=[]
    for wire in wires[id].values():
        if any(local(x)=='PCon' and x.get('UId')==uid and x.get('PinName')==pin for x in wire):
            refs.extend(native_networks[id]['refs'][x.get('UId')]['name'] for x in wire if local(x)=='OCon')
    return refs
def upstream_parts(id,uid,pin,seen=None):
    seen=set() if seen is None else seen
    if (uid,pin) in seen:return set()
    seen.add((uid,pin));found=set()
    for wire in wires[id].values():
        if not any(local(x)=='PCon' and x.get('UId')==uid and x.get('PinName')==pin for x in wire):continue
        for x in wire:
            if local(x)!='PCon' or x.get('PinName') not in ('out','eno','Q'):continue
            producer=x.get('UId');found.add(producer);gate=parts[id].get(producer)
            inputs=('in','en') if gate in ('Contact','PContact','Coil','SCoil','RCoil','Move','SdCoil') else ('in1','in2','in3','in4','en')
            for dest_pin in inputs:found|=upstream_parts(id,producer,dest_pin,seen)
    return found
for row in common['stages']:
    id=row['network'];uid=row['part'];a=next(a for a in native_networks[id]['actions'] if a['uid']==uid)
    assert row['gate']==parts[id][uid]==a['gate'] and row['target']==a['name']
    assert row['condition']==a['condition'] and row['value']==a.get('value')
    target_pin='out1' if row['gate']=='Move' else 'operand'
    assert operand_at(id,uid,target_pin)==[row['target']],(id,uid)
    predecessors=upstream_parts(id,uid,'en' if row['gate']=='Move' else 'in')
    native_counts={float(value) for pred in predecessors if parts[id].get(pred)=='Eq' and operand_at(id,pred,'in1')==['Data.Tempo_presetting'] for value in operand_at(id,pred,'in2')}
    assert set(row['counter_values'])==native_counts,(id,uid,row['counter_values'],native_counts)
    native_off=any(operand_at(id,pred,'operand')==['OFF'] for pred in predecessors if parts[id].get(pred)=='Contact')
    assert row['additional_off']==native_off,(id,uid)
    for w in row['connections']:
        actual=wires[id][w['wire']]
        assert [(x['kind'],x['uid'],x['pin']) for x in w['endpoints']]==[(local(x),x.get('UId'),x.get('PinName')) for x in actual]
assert common['calls']==[c for c in json.loads((ROOT/'registers/program-model.json').read_text())['calls'] if c['network'] in common['networks']]
for p in common['priority_profiles']:
    original=next(x for x in data['priority'] if x['key']==p['key'])
    assert all(p[k]==original[k] for k in ('name','plc_id','match','note'))
    if not p['plc_id'] or p['plc_id'] in ('CC01','AB01','HE01'):assert not p['signals'] and not p['stage_locations']
assert operand_at(1841,'59','in1')==['Data.Tempo_presetting'] and operand_at(1841,'59','in2')==['1']
assert operand_at(1841,'59','out')==['Data.Tempo_presetting'] and operand_at(1841,'92','operand')==[None]
assert operand_at(1846,'21','operand')==['Allarm.Emergency_module_fault'] and operand_at(1846,'21','bit')==['Tag_292']
for uid,rid,name,file in [('64','77','TOF','0568'),('73','77','TOF','0568'),('72','78','IEC_Timer_0_DB','0569'),('74','84','IEC_Timer_1_DB','0569')]:
    root=ET.parse(ROOT/('sources/decoded-original/'+file+'-IdentXmlPart.xml')).getroot()
    assert any(ident.get('N')==name and ident.get('RID')==rid and any(c.get('NID')=='9' and c.get('UID')==uid for c in ident.iter()) for node in root for ident in node if local(ident)=='ID')
assert operand_at(930,'64','PT')==operand_at(930,'73','PT')==['T#3s']
assert operand_at(930,'48','operand')==['103A7'] and operand_at(930,'60','operand')==['Reset_Inverter']
assert operand_at(931,'229','value')==['S5T#1S']
assert all((ROOT / p).is_file() for p in data['resources'])

routes = set()
routes.update(f"priority-guides/{p['key']}.html" for p in data['priority'])
routes.update(['improvement-review.html','electrical-trace.html','work-progress.html','work-progress.html#current','work-progress.html#sequence','work-progress.html#status'])
alarm_recovery=json.loads((ROOT/'registers/alarm-recovery.json').read_text())
alarm_report=json.loads((ROOT/'alarm-recovery-verification.json').read_text())
assert alarm_report['status']=='passed'
assert alarm_report['alarm_recovery_sha256']==hashlib.sha256((ROOT/'registers/alarm-recovery.json').read_bytes()).hexdigest()
assert alarm_recovery['field_verified']==alarm_recovery['tia_verified']==alarm_recovery['plc_changes']==0
assert data['review_counts']['alarm_guides']==len(alarm_recovery['profiles'])==14
assert alarm_recovery['simulator_development']=='stopped_by_user' and alarm_recovery['simulator_behavior_tests']=='not_rerun'
burner=json.loads((ROOT/'registers/burner-interface.json').read_text())
burner_report=json.loads((ROOT/'burner-interface-verification.json').read_text())
assert burner_report['status']=='passed' and burner_report['burner_interface_sha256']==hashlib.sha256((ROOT/'registers/burner-interface.json').read_bytes()).hexdigest()
assert data['burner_interface_counts']=={'networks':16,'signals':32}
assert burner['simulator_development']=='stopped_by_user' and burner['simulator_behavior_tests']=='not_rerun'
routes.update(['burner-interface.html'+anchor for anchor in ['', '#workflow','#boundary','#permit','#reset','#sequence','#transition','#timers','#circuit','#checks','#native','#index']])
routes.add('registers/burner-interface.json')
process=json.loads((ROOT/'registers/process-measurement.json').read_text())
process_report=json.loads((ROOT/'process-measurement-verification.json').read_text())
assert process_report['status']=='passed' and process_report['process_measurement_sha256']==hashlib.sha256((ROOT/'registers/process-measurement.json').read_bytes()).hexdigest()
assert data['process_measurement_counts']=={'channels':4,'outputs':2,'alarms':11}
routes.update('measurement-trace.html'+a for a in ['', '#channels','#linear','#flow','#outputs','#hmi','#writes','#checks','#native'])
routes.update('process-stop-alarms.html'+a for a in ['', '#stop','#alarms','#repair','#checks']+['#alarm-'+str(i) for i in range(1,12)])
routes.add('registers/process-measurement.json')
sensor=json.loads((ROOT/'registers/sensor-measurement.json').read_text())
sensor_report=json.loads((ROOT/'sensor-measurement-verification.json').read_text())
assert sensor_report['status']=='passed' and sensor_report['sensor_measurement_sha256']==hashlib.sha256((ROOT/'registers/sensor-measurement.json').read_bytes()).hexdigest()
assert data['sensor_measurement_counts']=={'channels':19,'networks':42,'fgs':15}
routes.update('sensor-measurement.html'+a for a in ['', '#index','#repair','#checks','#native']+['#sensor-'+c['id'] for c in sensor['channels']])
routes.add('registers/sensor-measurement.json')
regulation=json.loads((ROOT/'registers/regulation-manual.json').read_text())
reg_report=json.loads((ROOT/'regulation-manual-verification.json').read_text())
assert reg_report['status']=='passed' and reg_report['regulation_manual_sha256']==hashlib.sha256((ROOT/'registers/regulation-manual.json').read_bytes()).hexdigest()
assert data['regulation_counts']=={'loops':9,'networks':33,'texts':10}
routes.update('regulation-manual.html'+a for a in ['', '#index','#native','#texts','#writes','#checks']+['#loop-'+l['id'] for l in regulation['loops']]+['#native-'+str(i) for i in regulation['native_ids']]+['#text-'+str(t['id']) for t in regulation['indexed_texts']])
routes.add('registers/regulation-manual.json')
encoder=json.loads((ROOT/'registers/encoder-position.json').read_text())
enc_report=json.loads((ROOT/'encoder-position-verification.json').read_text())
assert enc_report['status']=='passed' and enc_report['encoder_position_sha256']==hashlib.sha256((ROOT/'registers/encoder-position.json').read_bytes()).hexdigest()
assert data['encoder_position_counts']=={'channels':5,'networks':26,'counter_calls':5,'calibration_paths':2}
routes.update('encoder-position.html'+a for a in ['', '#index','#native','#writes','#checks']+['#position-'+c['id'] for c in encoder['channels']]+['#native-'+str(i) for i in encoder['native_ids']])
routes.add('registers/encoder-position.json')
hmi_transfer=json.loads((ROOT/'registers/hmi-transfer.json').read_text())
hmi_report=json.loads((ROOT/'hmi-transfer-verification.json').read_text())
assert hmi_report['status']=='passed' and hmi_report['hmi_transfer_sha256']==hashlib.sha256((ROOT/'registers/hmi-transfer.json').read_bytes()).hexdigest()
assert data['hmi_transfer_counts']=={'tags':782,'windows':17,'native_networks':47,'priority_profiles':23,'shared_address_groups':2}
routes.update('hmi-transfer.html'+a for a in ['', '#tags','#profiles','#shared','#windows','#native','#repair','#writes','#checks']+['#profile-'+p['key'] for p in hmi_transfer['profiles']]+['#'+a['anchor'] for a in hmi_transfer['tags']]+['#native-'+str(i) for i in hmi_transfer['native_ids']])
routes.add('registers/hmi-transfer.json')
recipe_settings=json.loads((ROOT/'registers/recipe-settings.json').read_text())
recipe_report=json.loads((ROOT/'recipe-settings-verification.json').read_text())
assert recipe_report['status']=='passed' and recipe_report['recipe_settings_sha256']==hashlib.sha256((ROOT/'registers/recipe-settings.json').read_bytes()).hexdigest()
assert data['recipe_settings_counts']==recipe_settings['counts']
routes.update('recipe-settings.html'+a for a in ['', '#repair','#recipe','#fields','#writers','#startup','#hmi','#native','#profiles','#checks']+['#profile-'+p['key'] for p in recipe_settings['profiles']]+['#field-'+x['field'] for x in recipe_settings['load_fields']]+['#native-'+str(i) for i in recipe_settings['native_ids']]+['#index-'+str(x['id']) for x in recipe_settings['indexed_texts']]+['#claim-'+x['key'] for x in recipe_settings['claims']])
routes.add('registers/recipe-settings.json')
identity=json.loads((ROOT/'registers/unresolved-identity.json').read_text())
identity_report=json.loads((ROOT/'unresolved-identity-verification.json').read_text())
assert identity_report['status']=='passed' and identity_report['json_sha256']==hashlib.sha256((ROOT/'registers/unresolved-identity.json').read_bytes()).hexdigest()
assert data['unresolved_identity_counts']==identity['counts']
routes.update(['unresolved-identity.html','registers/unresolved-identity.json']+['unresolved-identity.html#identity-'+p['key'] for p in identity['profiles']]+['unresolved-identity.html#candidate-'+c['id'] for c in identity['candidates']])
body_manual=json.loads((ROOT/'registers/body-manual.json').read_text())
body_report=json.loads((ROOT/'body-manual-verification.json').read_text())
assert body_report['status']=='passed' and body_report['body_manual_sha256']==hashlib.sha256((ROOT/'registers/body-manual.json').read_bytes()).hexdigest()
assert data['body_manual_counts']==body_manual['counts']
assert {n['id'] for n in data['equipment_status_notes']}==({'MV04','SC12','PV04','P22','P23'} | ({'EV'+str(i).zfill(2) for i in range(1,91)} & {v['id'] for v in json.loads((ROOT/'registers/control-spec.json').read_text())['specifications']}))
assert data['project_work_scope']==body_manual['project_work_scope'] and data['project_work_scope']['phase']=='priority23_first' and data['project_work_scope']['full_catalog_role']=='preserved_reference_only'
assert data['manual_exclusion_ranges']==body_manual['manual_exclusion_ranges'] and data['manual_exclusion_ranges'][0]['start']==1 and data['manual_exclusion_ranges'][0]['end']==90
assert data['equipment_status_notes']==body_manual['equipment_status_notes'] and data['current_priority_count']==21 and data['excluded_priority']==['P22','P23']
routes.update('body-manual.html'+a for a in ['', '#cables','#checks','#native','#alarms-AB01']+['#'+q+p['id'] for p in body_manual['profiles'] for q in ['body-','flow-','symptoms-']]+['#'+s['id'] for p in body_manual['profiles'] for s in p['symptoms']]+['#'+c['id'] for c in body_manual['checks']])
routes.add('registers/body-manual.json')
routes.update(p['pid_image'] for p in body_manual['profiles'])
audit=json.loads((ROOT/'registers/requirements-audit.json').read_text())
audit_report=json.loads((ROOT/'requirements-audit-verification.json').read_text())
assert audit_report['status']=='passed' and audit_report['requirements_audit_sha256']==hashlib.sha256((ROOT/'registers/requirements-audit.json').read_bytes()).hexdigest()
assert data['requirements_audit_counts']==audit['counts']
routes.update('requirements-audit.html'+a for a in ['', '#requirements','#priority','#equipment','#limits']+['#equipment-'+r['id'] for r in audit['equipment']]+['#priority-'+p['key'] for p in audit['priority']]+['#'+r['id'] for r in audit['requirements']])
routes.update('operator-guide.html'+a for a in ['', '#start','#repair','#structure','#records','#pending','#limits','#install'])
routes.update(['registers/requirements-audit.json','registers/requirements-audit.csv'])

routes.update('sources/decoded-original/'+d['file'] for a in burner['actions'] for d in a.get('value_declarations',[]))
routes.update(['alarm-recovery.html','registers/alarm-recovery.json'])
for profile in alarm_recovery['profiles']:
    routes.update('alarm-guides/'+profile['id']+'.html'+anchor for anchor in ['', '#alarms','#timers','#contacts','#request','#writes','#native'])
    if profile['context_actions']:routes.add('alarm-guides/'+profile['id']+'.html#context')
    routes.update('sources/decoded-original/'+d['file'] for t in profile['timers'] for d in t['value_declarations'])
    routes.update(n['file'] for n in profile['native_networks'])
    routes.update(d['file'] for a in profile['alarms'] for r in a['usages'] for d in r['declarations'])
impact=json.loads((ROOT/'registers/improvement-impact.json').read_text())
impact_report=json.loads((ROOT/'improvement-impact-verification.json').read_text())
assert impact_report['status']=='passed' and impact_report['guides']==len(impact['items'])==6
assert impact_report['impact_sha256']==hashlib.sha256((ROOT/'registers/improvement-impact.json').read_bytes()).hexdigest()
assert impact['changes_applied']==impact['field_verified']==impact['tia_verified']==0
assert impact['simulator_behavior_tests']=='not_rerun' and impact['simulator_development']=='stopped_by_user'
for path,digest in impact['sources'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
for item in impact['items']:
    routes.add(item['guide'])
    routes.update(item['guide']+anchor for anchor in ['#calls','#native','#signals'])
    routes.update(item['guide']+'#focus-'+str(i) for i in range(1,len(item['signals'])+1))
    routes.update(p['file'] for p in item['seed_evidence'])
    routes.update('networks/network-'+str(r['network'])+'.html' for s in item['signals'] for r in s['usages'])
    routes.update(d['file'] for s in item['signals'] for r in s['usages'] for d in r['declarations'])
    routes.update('networks/network-'+str(r['network'])+'.html' for s in item['signals'] for r in s['other_scope_usages'])
    routes.update('sources/decoded-original/'+d['file'] for c in item['direct_calls_and_known_ancestors'] for d in c['native_declarations'])
routes.update(['construction-guide.html'])
routes.update(p['guide'] for p in construction['profiles'])
routes.update(f"circuit-guides/{d['id']}.html" for d in electrical['devices'])
routes.update(f"circuit-guides/{d['id']}.html#signal-{i}" for d in electrical['devices'] for i in range(1,len(d['paths'])+1))
routes.add('signal-trace.html')
routes.update(f"signal-guides/{d['id']}.html{fragment}" for d in signal_trace['devices'] for fragment in ('','#multiple','#transfer','#signals'))
routes.update('common-control.html'+fragment for fragment in ('','#calls','#signals','#sequences','#sequence-1','#sequence-2','#sequence-5','#sequence-6','#native-paths','#reset','#restart','#priority','#checks'))
routes.update('common-guides/'+p['key']+'.html' for p in common['priority_profiles'])
repair=json.loads((ROOT/'registers/repair-decision.json').read_text())
assert len(repair['records'])==data['review_counts']['repair_guides']==23
assert Counter(r['boundary'] for r in repair['records'])=={'source_linked':15,'body_candidate':3,'identity_unresolved':5}
assert repair['field_verified']==repair['repairs_completed']==repair['plc_changes']==0
assert repair['simulator_development']=='stopped_by_user' and repair['simulator_behavior_tests']=='not_rerun'
assert sum(len(r['decisions']) for r in repair['records'])==99
priority_by_key={p['key']:p for p in data['priority']}
common_by_key={p['key']:p for p in common['priority_profiles']}
repair_sources=set()
for r in repair['records']:
    p=priority_by_key[r['key']]
    assert all(r[k]==p[k] for k in ('name','plc_id','match'))
    assert not r['field_verified'] and r['repairs_completed']==0
    assert {(a['network'],a['part']) for a in r['common_stages']}=={(a['network'],a['part']) for a in common_by_key[r['key']]['stage_locations']}
    for a in r['common_stages']:
        assert a==next(x for x in common['stages'] if (x['network'],x['part'])==(a['network'],a['part']))
        repair_sources.add(a['source'])
    for b in r['bindings']:
        normalized=b['name'].replace('"','').casefold()
        assert b['addresses']==[s['백업 주소'].upper() for s in symbols if s['원본 심볼'].replace('"','').casefold()==normalized]
        assert b['refs']
        for ref in b['refs']:
            n=native_networks[ref['network']]
            assert ref['source']==n['file'] and n['refs'][ref['oref']]['name'].replace('"','').casefold()==normalized
            assert any(local(x)=='OCon' and x.get('UId')==ref['oref'] for w in wires[ref['network']].values() for x in w)
            repair_sources.add(ref['source'])
    for a in r['output_actions']+r['request_reset_actions']+r['monitoring_actions']:
        n=native_networks[a['network']]
        assert a['source']==n['file']
        assert {k:v for k,v in a.items() if k not in ('network','source')}==next(x for x in n['actions'] if x['uid']==a['uid'])
        assert parts[a['network']][a['uid']]==a['gate']
        target_pin='out1' if a['gate']=='Move' else 'out' if a['gate'] in ('Add','Sub','Mul','Div') else 'operand'
        assert a['name'] in operand_at(a['network'],a['uid'],target_pin)
    for n in r['source_networks']:repair_sources.add(native_networks[n]['file'])
    if r['boundary']=='source_linked':
        assert {d['id'] for d in r['decisions']}=={'request','permit','response','stop','recovery'}
        assert r['bindings'] and r['output_actions']
        output_names={b['name'].replace('"','').casefold() for b in r['bindings'] if b['role']=='outputs'}
        assert output_names=={a['name'].replace('"','').casefold() for a in r['output_actions']}
        assert all(a['gate']=='Coil' for a in r['output_actions'])
        request_names={b['name'].replace('"','').casefold() for b in r['bindings'] if b['role']=='requests'}
        assert all(a['gate']=='RCoil' and a['name'].replace('"','').casefold() in request_names for a in r['request_reset_actions'])
        if r['plc_id'] in ('MV01','MV03','MV06'):
            expected={'MV01':{'Allarm.MV01_FAULT','WorkData.W33','WorkData.W34'},'MV03':{'Allarm.MV03_FAULT','WorkData.W29','WorkData.W30'},'MV06':{'Allarm.MV_06_FAULT','WorkData.W19','WorkData.W20'}}[r['plc_id']]
            assert {a['name'] for a in r['monitoring_actions'] if a['network']==1714}==expected
    else:
        assert not r['bindings'] and not r['output_actions'] and not r['source_networks'] and not r['common_stages']
        assert {d['id'] for d in r['decisions']}=={'identity','local','recovery'}
    template=json.loads((ROOT/('registers/repair-observation-'+r['key']+'.json')).read_text())
    assert template['equipment']==r['key'] and template['reference_plc_id']==r['plc_id']
    assert template['status']=='미작성' and not template['field_verified']
    assert template['timestamp'] is None and template['observations']==[] and template['recovery_evidence']==[]
    routes.update('repair-guides/'+r['key']+'.html'+fragment for fragment in ('','#decision','#boundary','#common-stages','#output-evidence','#signal-boundary','#monitor-evidence','#recovery'))
assert set(repair['sources'])==repair_sources
for path,digest in repair['sources'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
routes.add('repair-decision.html')
record_forms=json.loads((ROOT/'registers/repair-record-forms.json').read_text())
hub=json.loads((ROOT/'registers/evidence-review.json').read_text())
hub_by_id={r['id']:r for r in hub['items']}
evidence_steps=0
assert data['repair_record_forms']==record_forms
assert len(record_forms['profiles'])==23 and len({p['key'] for p in record_forms['profiles']})==23
assert record_forms['source']['sha256']==hashlib.sha256((ROOT/record_forms['source']['path']).read_bytes()).hexdigest()
assert not record_forms['field_verified'] and record_forms['repairs_completed']==record_forms['plc_changes']==0
for profile in record_forms['profiles']:
    original=next(r for r in repair['records'] if r['key']==profile['key'])
    assert profile['reference_plc_id']==original['plc_id'] and profile['boundary']==original['boundary']
    assert profile['steps']==original['decisions']
    assert [{k:v for k,v in s.items() if k!='id'} for s in profile['signals']]==original['bindings']
    for signal in profile['signals']:
        routes.update('networks/network-'+str(ref['network'])+'.html' for ref in signal['refs'])
    routes.update(profile['manual']+'#'+step['common'] for step in profile['steps'])
    assert not profile['field_verified'] and not profile['identity_confirmed']
    assert len({s['id'] for s in profile['signals']})==len(profile['signals'])
    if original['boundary']!='source_linked':assert not profile['signals']
    routes.update([profile['manual'],profile['blank_template']])
    plan=profile['evidence_plan']
    assert not plan['field_verified']
    assert [s['step_id'] for s in plan['steps']]==[s['id'] for s in original['decisions']]
    for path,digest in plan['sources'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    for section in [plan['preflight']]+plan['steps']:
        assert section['requirements'] and all(r['owner'] and r['work'] for r in section['requirements'])
        routes.update(r['path'] for r in section.get('source_links',[]))
        for review in section['reviews']:
            item=hub_by_id[review['id']]
            for field in ['title','observation','next_check','links','source_file']:
                assert review[field]==item[field],(profile['key'],review['id'],field)
            assert review['status']==item['source_status']
            if review['relationship']=='identity':assert item['kind']=='identity' and item['source_id']==profile['key']
            elif review['relationship']=='declared':assert original['plc_id'] and original['plc_id'] in item['equipment_ids']
            elif review['relationship']=='related':assert original['plc_id'] and original['plc_id'] in item['related_equipment_ids'] and original['plc_id'] not in item['equipment_ids']
            else:assert review['relationship']=='global' and item['global_scope']
            if original['boundary']!='source_linked':assert item['kind']!='common'
            routes.update(r['path'] for r in review['links'])
    routes.update(r['path'] for r in plan['circuit_pages']+plan['construction_pages'])
    circuit=next((c for c in electrical['devices'] if c['id']==original['plc_id']),None) if original['boundary']=='source_linked' else None
    if circuit:
        assert plan['circuit_equipment']==circuit['equipment'] and plan['circuit_distinction']==circuit['distinction']
        response=next(s for s in plan['steps'] if s['step_id']=='response')
        assert [r['work'] for r in response['requirements'] if r['owner']=='회로 작업지의 확인 대기']==circuit['pending']
        assert plan['circuit_pages']==[dict(label='OEM FG'+str(fg)+' · PDF '+str(page),path=electrical['source']+'#page='+str(page)) for fg,page in zip(circuit['sheets'],circuit['pages'])]
    else:assert plan['circuit_equipment'] is None and not plan['circuit_pages']
    if original['boundary']!='source_linked':assert not plan['construction_pages']
    evidence_steps+=len(plan['steps'])
assert record_forms['counts']==dict(profiles=23,signals=sum(len(p['signals']) for p in record_forms['profiles']),steps=99)
assert evidence_steps==99
hub=json.loads((ROOT/'registers/evidence-review.json').read_text())
assert data['evidence_review']==hub
assert len(hub['items'])==len({r['id'] for r in hub['items']})==64
assert hub['counts']==Counter(r['kind'] for r in hub['items'])==dict(source=18,construction=7,common=10,improvement=6,identity=23)
assert hub['field_verified']==hub['plc_changes']==0
assert hub['original_pending_register_count']==1060 and hub['design_tests_preserved']==577
assert hub['simulator_behavior_tests']=='not_rerun' and hub['simulator_development']=='stopped_by_user'
origins={
    'source':{r['ID']:r for r in data['conflicts']},
    'construction':{r['id']:r for r in construction_reviews['items']},
    'common':{r['id']:r for r in common['checks']},
    'improvement':{r['id']:r for r in json.loads((ROOT/'registers/improvement-review.json').read_text())['items']},
    'identity':{p['key']:p for p in data['priority']},
}
repair_by_id={r['plc_id']:r for r in repair['records'] if r['plc_id']}
global_refs={(r['network'],r['oref']) for r in signal_trace['usages'] if r['scope']=='Global'}
for item in hub['items']:
    assert item['id']==item['kind']+':'+item['source_id']
    assert item['raw']==origins[item['kind']][item['source_id']]
    assert not item['field_verified'] and not item['identity_verified'] and not item['resolved']
    assert item['equipment_ids']==[x for x in item['declared_scope'] if x in specs]
    assert item['unmapped_scope']==[x for x in item['declared_scope'] if x not in specs]
    assert len(item['related_equipment_ids'])==len(set(item['related_equipment_ids']))
    assert item['related_equipment_ids']==[r['equipment'] for r in item['relationship_evidence']]
    for relation in item['relationship_evidence']:
        assert relation['equipment'] in repair_by_id and relation['equipment'] not in item['equipment_ids']
        names={b['name'].replace('"','').casefold() for b in repair_by_id[relation['equipment']]['bindings']}
        assert relation['refs']
        for ref in relation['refs']:
            assert ref['network'] in item['networks'] and (ref['network'],ref['oref']) in global_refs
            assert native_networks[ref['network']]['refs'][ref['oref']]['name']==ref['name']
            assert ref['name'].replace('"','').casefold() in names
    expected_keys=[p['key'] for p in data['priority'] if p['plc_id'] and p['plc_id'] in item['equipment_ids']+item['related_equipment_ids']]
    if item['kind']=='identity':
        expected_keys=list(dict.fromkeys([item['source_id']]+expected_keys))
        if item['raw']['match']=='unknown':assert not item['equipment_ids'] and not item['related_equipment_ids'] and not item['networks']
    assert item['priority_keys']==expected_keys
    routes.add('evidence-review.html#review-'+item['kind']+'-'+item['source_id'])
    routes.update(x['path'] for x in item['links'])
for path,digest in hub['sources'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
for d in data['equipment']:
    s = specs[d['id']]
    for field in ('inputs','outputs','internal','hmi','networks','source_conflicts','pending',
                  'plc_execution_verified','field_verified','simulator_model_ready'):
        assert d[field] == s[field], (d['id'],field)
    assert d['direct_rule_count'] == len(s['direct_rules'])
    assert d['test_count'] == len(s['test_designs'])
    assert d['verification_count'] == len(s['verification'])
    assert not d['simulator_model_ready']
    routes.update([f"devices/{d['id']}.html", f"devices/{d['id']}.html#work",
                   f"control-specs/{d['id']}.html", f"control-specs/{d['id']}.html#fault", f"procedures/{d['id']}.html"])
    for n in d['networks']: routes.add(f"networks/network-{n['문서 ID']}.html")
    if d['parent']: assert d['parent'] in specs

# Drawing UI reuses existing evidence, and supports current21 only.
drawing=data['drawing_workspace'];assert [p['key'] for p in drawing['profiles']]==[p['key'] for p in data['priority'][:21]]
for path,digest in {**drawing['source_hashes'],**drawing['preview_hashes']}.items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    assert path in data['resources'],path
expected_circuits={d['id']:d for d in electrical['devices']}
for profile in drawing['profiles']:
    priority=next(p for p in data['priority'] if p['key']==profile['key'])
    device=next((d for d in data['equipment'] if d['id']==priority['plc_id']),{})
    assert profile['plc_id']==priority['plc_id'] and profile['match']==priority['match']
    assert profile['circuit']==expected_circuits.get(priority['plc_id'])
    assert not profile['identity_verified'] and not profile['field_verified']
    sheets=profile['sheets'];assert len({s['id'] for s in sheets})==len(sheets)
    assert {s['kind'] for s in sheets}<={'OEM 전기','P&ID','시공·케이블','HMI 참고'},profile['key']
    assert [s['fg'] for s in sheets if s['kind']=='OEM 전기']==list(dict.fromkeys(device.get('circuit_fgs',[])+device.get('electrical_fgs',[])))
    assert [s['page'] for s in sheets if s['kind']=='시공·케이블']==device.get('construction_pages',[])
    for sheet in sheets:
        assert sheet['image'] and sheet['image'] in drawing['preview_hashes']
        assert (ROOT/sheet['image']).read_bytes()[:8]==b'\x89PNG\r\n\x1a\n'
        if sheet['kind']=='OEM 전기':
            fg=str(sheet['fg']);n=int(fg) if fg.isdigit() else None
            expected={'5A':6,'180A':182,'180B':183}.get(fg) or n+(n>5)+2*(n>180)
            assert sheet['page']==expected and sheet['source']==electrical['source']
        elif sheet['kind']=='시공·케이블':
            assert sheet['source']==construction['source'] and sheet['image']==f"assets/construction/P{sheet['page']:02}.png"
        elif sheet['kind']=='P&ID':assert sheet['source']=='sources/PID_1684n002I.pdf' and sheet['page']==1
        else:assert sheet['id']=='hmi' and sheet['source']==sheet['image']=='assets/HMI_DECOATER.png'
        routes.add(sheet['source']+('#page='+str(sheet['page']) if sheet['page'] else ''))
        routes.add(sheet['image'])
    if priority['match']=='unknown':assert not profile['circuit'] and {s['id'] for s in sheets}=={'pid','hmi'}
assert 'C05' in next(p for p in drawing['profiles'] if p['key']=='P02')['warnings'][0]
assert 'CORE=4' in next(p for p in drawing['profiles'] if p['key']=='P01')['warnings'][0]
parsers = {}
for route in routes:
    u = urlsplit(route); p = ROOT / unquote(u.path)
    assert p.is_file(), route
    assert u.path in data['resources'], route
    if u.fragment and p.suffix=='.pdf':
        assert re.fullmatch(r'page=\d+',u.fragment),route
        page=int(u.fragment.split('=')[1])
        pdf_pages={'Electrical_Can_Decoating_20241118.pdf':64,'Electrical_Rev2.pdf':265,'PID_1684n002I.pdf':1}
        assert p.name in pdf_pages and 1<=page<=pdf_pages[p.name],route
    elif u.fragment:
        if p not in parsers:
            parser = Ids(); parser.feed(p.read_text()); parsers[p] = parser
        assert u.fragment in parsers[p].ids, route
entry = (ROOT / 'index.html').read_text()
assert 'data-gme-app="all-in-one"' in entry
for ref in ('assets/all-in-one.css','assets/all-in-one.js','assets/all-in-one-data.js','assets/program-model-data.js','assets/virtual-plc.js','assets/simulator-workspace.js','assets/note-record-store.js','assets/repair-records.js'):
    assert ref in entry and (ROOT / ref).is_file()
assert "(ROOT/'manual-catalog.html').write_text" in (ROOT / 'build-manual.py').read_text()
assert "runpy.run_path(str(ROOT / 'build-all-in-one.py')" in (ROOT / 'build-control-spec.py').read_text()

result = dict(drawing_profiles=len(drawing['profiles']),drawing_previews=len(drawing['preview_hashes']),drawing_original_source_hashes_checked=True,body_manual_counts=body_manual['counts'],requirements_audit_counts=audit['counts'],status='passed', equipment=248, priority=23, priority_tag_matches=14,
              priority_role_candidates=4, priority_unmatched=5, dynamic_routes_checked=len(routes),
              tests_preserved_unexecuted=577, pending_checks_preserved=1060,
              source_equipment_fields_preserved=True, single_entry='index.html',
              simulator_engine_implemented=True, isolated_executable_networks=data['program_counts']['executable'],
              virtual_model_tests_passed=data['virtual_results']['passed'], plc_connected=False,
              priority_diagnostic_guides=23, electrical_paths=data['review_counts']['electrical_paths'],
              electrical_guides=data['review_counts']['electrical_devices'],electrical_sheets=data['review_counts']['electrical_sheets'],
              electrical_unresolved_encoder_addresses=unresolved_addresses,electrical_direct_symbol_references=direct_references,
              static_signal_guides=len(signal_trace['devices']),static_signal_pin_usages=signal_trace['usage_count'],
              local_signal_scopes_separated=signal_trace['local_usages_separated'],
              common_source_networks=len(common['networks']),common_stage_writes=len(common['stages']),
              common_priority_guides=len(common['priority_profiles']),common_checks_pending=len(common['checks']),
              priority_repair_guides=len(repair['records']),repair_decision_branches=sum(len(r['decisions']) for r in repair['records']),
              evidence_review_items=len(hub['items']),evidence_review_counts=hub['counts'],
              repair_record_forms=record_forms['counts'],
              repair_evidence_steps=evidence_steps,
              improvement_candidates=data['review_counts']['improvement_candidates'],
              improvement_impact_guides=len(impact['items']),
              sensor_measurement_channels=len(sensor['channels']),sensor_measurement_networks=len(sensor['selected_networks']),
              recipe_setting_fields=len(recipe_settings['load_fields']),recipe_native_networks=len(recipe_settings['native_ids']),recipe_index_texts=len(recipe_settings['indexed_texts']),
              hmi_transfer_tags=len(hmi_transfer['tags']),hmi_transfer_windows=len(hmi_transfer['windows']),hmi_transfer_native_networks=len(hmi_transfer['native_ids']),
              encoder_position_channels=len(encoder['channels']),encoder_native_networks=len(encoder['native_ids']),
              regulation_loops=len(regulation['loops']),regulation_native_networks=len(regulation['native_ids']),regulation_indexed_texts=len(regulation['indexed_texts']),
              process_measurement_channels=len(process['channels']),process_measurement_outputs=len(process['outputs']),process_stop_alarm_names=len(process['alarms']),
              burner_interface_networks=len(burner['selected_networks']),burner_interface_signals=len(burner['signals']),
              motor_alarm_recovery_guides=sum(p['family']=='motor' for p in alarm_recovery['profiles']),
              motor_alarm_latches=sum(len(p['alarms']) for p in alarm_recovery['profiles'] if p['family']=='motor'),
              actuator_alarm_recovery_guides=sum(p['family']!='motor' for p in alarm_recovery['profiles']),
              actuator_alarm_latches=sum(len(p['alarms']) for p in alarm_recovery['profiles'] if p['family']!='motor'),
              construction_pages=64,construction_guides=22,construction_selected_rows=51,
              construction_review_items_pending=7,masked_cable_rows_excluded=9,
              simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun',
              simulator_files_hashes_unchanged=True,
              scope='application integration and preserved source data; not PLC/TIA execution')
(ROOT / 'all-in-one-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
