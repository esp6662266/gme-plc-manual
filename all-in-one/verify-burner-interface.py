"""Audit native BR01 pins/timer declarations and integration, never evaluate logic."""
from pathlib import Path
from collections import Counter
import hashlib, json, csv, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
tag=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s or '').replace('"','').casefold()
report=ROOT/'burner-interface-verification.json'
report.write_text(json.dumps(dict(status='checking',scope='Native source/links; no execution'))+'\n')
data=load('registers/burner-interface.json')
model=load('registers/program-model.json');nets={n['id']:n for n in model['networks']}
trace=load('registers/signal-trace.json')['usages']
network_map={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
declarations=load('sources/decoded-original/identifier-declarations.json')
selected=[1854,1855,1856,1857,1858,1859,1861,1862,1863,1865,1866,1867,1868,1869,1871,1872]
assert data['selected_networks']==selected
assert data['equipment']=='BR01' and data['priority_key']=='P11'
assert data['field_verified']==data['tia_verified']==False and data['plc_changes']==data['repairs_completed']==0
assert data['simulator_development']=='stopped_by_user' and data['simulator_behavior_tests']=='not_rerun'
assert all(sha(f)==digest for f,digest in data['sources'].items())
assert data['circuit']==next(d for d in load('registers/electrical-trace.json')['devices'] if d['id']=='BR01')
assert data['block_index']==[dict(id=n['id'],index=n['index'],title=n['title'],file=n['file'],detailed=n['id'] in selected,legacy_source_only='simulation' in n['title'].casefold()) for n in model['networks'] if n['block']=='burner control']
assert len(data['block_index'])==24
assert list(n['network'] for n in data['native_networks'])==selected
proofs={p['network']:p for p in data['native_networks']};total=Counter()
for n in data['native_networks']:
    original=nets[n['network']];root=ET.parse(ROOT/n['file']).getroot()
    assert n['file']==original['file'] and n['sha256']==sha(n['file']) and n['block']==original['block']
    assert n['network_index']==original['index'] and n['title']==original['title']
    parts=[dict(uid=x.get('UId'),gate=x.get('Gate'),negated_pins=[c.get('PinName') for c in x if tag(c)=='Negated']) for x in root.iter() if tag(x)=='Part']
    wires=[dict(uid=w.get('UId'),endpoints=[dict(kind=tag(x),uid=x.get('UId'),pin=x.get('PinName')) for x in w]) for w in root.iter() if tag(w)=='Wire']
    refs={x.get('UId'):dict(ref_id=x.get('RefId'),name=original['refs'][x.get('UId')].get('name')) for x in root.iter() if tag(x)=='ORef'}
    assert n['parts']==parts and n['wires']==wires and n['refs']==refs
    total.update(native_parts=len(parts),native_wires=len(wires),native_orefs=len(refs))
expected=[dict(network=i,**a) for i in selected for a in nets[i]['actions']]
assert [{k:v for k,v in a.items() if k not in ['native_upstream','value_declarations']} for a in data['actions']]==expected
order=lambda rows:sorted(json.dumps(x,sort_keys=True) for x in rows)
for a in data['actions']:
    p=proofs[a['network']];parts={x['uid']:x for x in p['parts']}
    predecessors={uid:set() for uid in parts}
    for w in p['wires']:
        outputs={x['uid'] for x in w['endpoints'] if x['kind']=='PCon' and x['pin']=='out'}
        for x in w['endpoints']:
            if x['kind']=='PCon' and (x['pin'] in ['in','pre','en'] or x['pin'] and x['pin'].startswith('in') and x['pin'][2:].isdigit()):predecessors[x['uid']].update(outputs)
    reach={a['uid']}
    while True:
        more=reach|{x for uid in reach for x in predecessors[uid]}
        if more==reach:break
        reach=more
    assert a['native_upstream']['parts']==sorted(reach,key=int)
    expected_contacts=[]
    for uid in reach:
        part=parts[uid]
        if part['gate'] not in ['Contact','PContact','NContact']:continue
        for w in p['wires']:
            if any(x['kind']=='PCon' and x['uid']==uid and x['pin']=='operand' for x in w['endpoints']):
                expected_contacts.extend(dict(part=uid,gate=part['gate'],negated_pins=part['negated_pins'],wire=w['uid'],oref=x['uid'],**p['refs'][x['uid']]) for x in w['endpoints'] if x['kind']=='OCon')
    assert order(a['native_upstream']['contacts'])==order(expected_contacts)
    reference_pins=[]
    for w in p['wires']:
        for x in w['endpoints']:
            if x['kind']=='PCon' and x['uid'] in reach:
                reference_pins.extend(dict(part=x['uid'],gate=parts[x['uid']]['gate'],pin=x['pin'],wire=w['uid'],oref=c['uid'],**p['refs'][c['uid']]) for c in w['endpoints'] if c['kind']=='OCon')
    assert a['native_upstream']['reference_pins']==reference_pins
    total['command_contact_references']+=len(expected_contacts)
    if a['gate']=='SdCoil':
        v=next(x for x in reference_pins if x['part']==a['uid'] and x['pin']=='value')
        decl=[d for d in declarations if d['uid']==v['oref'] and d['rid']==v['ref_id'] and d['nid']==network_map[a['network']]['inferred_original_nid'] and d['name']==v['name']]
        assert decl==a['value_declarations'] and decl and v['name']==a['preset']['literal']
        assert all(d['kind']=='LiteralConstant' for d in decl)
        total['timer_commands']+=1
symbols=list(csv.DictReader((ROOT/'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
expected_signals=['Flag.Start_Burner','Flag.Burner_ready','Enable start burner(1)','Enable start burner','Rem. Start/Stop Burner','Start Burner','Lock Burner','Programmed stop burner','Allarm.BURNER_LDU_FAULT','Allarm.BURNER_START_FAULT','Allarm.SERVOMOTOR_MIN_POS_ALL','m491','APP M10.2','Rst allarm Burner','Tag_142','Burner On','Inputs.Burner On','Inputs.Burner ON and OK','Burner ON and OK','WorkData.BR01_State','WorkData.BR01_CleanTime','WorkData.W5','Open MV03 for washing','Close MV03 for Burner Startup','Start High Flame','Foced Spark','Main flame ON','Data.Burner_Panel_SetPoint','Flag AutoBurner','Flag.AUTO_BURNER','ON','OFF']
assert [s['name'] for s in data['signals']]==expected_signals
for s in data['signals']:
    assert s['scope']=='Global'
    assert s['usages']==[u for u in trace if u['scope']=='Global' and canon(u['name'])==canon(s['name'])]
    assert s['other_scope_usages']==[u for u in trace if u['scope']!='Global' and canon(u['name'])==canon(s['name'])]
    assert s['symbols']==[x for x in symbols if canon(x['원본 심볼'])==canon(s['name'])]
    total['signal_pin_references']+=len(s['usages'])
    total['other_scope_references']+=len(s['other_scope_usages'])
sig={s['name']:s for s in data['signals']}
for name,addr in [('Enable start burner(1)','%M48.0'),('Enable start burner','%M48.2'),('Rem. Start/Stop Burner','%Q6.5'),('Start Burner','%M48.3'),('Rst allarm Burner','%Q6.7')]:assert [x['백업 주소'].upper() for x in sig[name]['symbols']]==[addr]
assert [(u['network'],u['gate']) for u in sig['Allarm.BURNER_START_FAULT']['usages'] if u['role']=='write']==[(1869,'RCoil')]
act=lambda n,uid:next(a for a in data['actions'] if a['network']==n and a['uid']==uid)
assert act(1863,'472')['preset']['literal']=='S5T#4S'
assert [a['preset']['literal'] for a in data['actions'] if a['network']==1854 and a['gate']=='SdCoil']==['S5T#6S','S5T#2S','S5T#2S']
assert len([a for a in data['actions'] if a['gate']=='SdCoil' and a['name']=='Tag_142'])==2
assert act(1868,'1669')['name']==act(1868,'1306')['name']=='Close MV03 for Burner Startup'
assert {tuple(c['negated_pins']) for c in act(1868,'1669')['native_upstream']['contacts'] if c['name']=='Inputs.MV03 Close'}=={(),('operand',)}
assert any(c['name']=='Inputs.MV03 open' and c['negated_pins']==['operand'] for c in act(1868,'1188')['native_upstream']['contacts'])
assert any(x['name']=='77' for x in act(1868,'1281')['native_upstream']['reference_pins'])
assert 'ENABLE SPARK FOR 3 sec' in next(p['text'] for p in load('sources/electrical-page-text.json') if p['page']==100)
assert len(data['symptoms'])==6 and len(data['observations'])==7 and all('확인 대기' in o['status'] for o in data['observations'])
assert all(o['networks'] and set(o['networks'])<=set(selected) for o in data['observations'])
# Links must reach the integrated repair material and the BR01 record comparison stages.
assert 'burner-interface.html' in (ROOT/'repair-guides/P11.html').read_text()
assert 'burner-interface.html' in (ROOT/'procedures/BR01.html').read_text()
forms=load('registers/repair-record-forms.json')
p11=next(p for p in forms['profiles'] if p['key']=='P11')
text=json.dumps(p11,ensure_ascii=False)
assert 'burner-interface.html' in text
assert p11['evidence_plan']['sources']['registers/burner-interface.json']==sha('registers/burner-interface.json')
result=dict(status='passed',date='2026-10-08',burner_networks=len(proofs),block_index_networks=24,
 actions=len(data['actions']),signals=len(data['signals']),symptoms=len(data['symptoms']),pending_source_observations=len(data['observations']),
 source_hashes_checked=len(data['sources']),burner_interface_sha256=sha('registers/burner-interface.json'),
 field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun',
 scope='Native Part/Wire/ORef and static reference coverage; not PLC execution or burner recovery',**dict(total))
report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
