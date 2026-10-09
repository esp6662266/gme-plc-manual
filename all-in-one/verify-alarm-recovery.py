"""Verify alarm manual evidence against native XML and preserved trace indexes."""
from pathlib import Path
from collections import Counter
import hashlib, json, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
report=ROOT/'alarm-recovery-verification.json'
report.write_text(json.dumps(dict(status='checking',scope='Native source comparison; no execution'))+'\n')
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
tag=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s).replace('"','').casefold()
data=load('registers/alarm-recovery.json')
model=load('registers/program-model.json');nets={n['id']:n for n in model['networks']}
trace=load('registers/signal-trace.json');repair=load('registers/repair-decision.json')
expected={'BC01':[1785,1786],'FN04':[1809],'RD01':[1787],'MC04':[1791],
          'VS01':[1794],'FN01':[1798],'FN02':[1796],'FN03':[1801],'FN06':[1802],
          'PV01':[1815,1816],'PV02':[1817,1818],'MV01':[1226,1714],'MV03':[1226,1714],'MV06':[1226,1714]}
motor_ids=list(expected)[:9]
selected_alarms={'MV01':['Allarm.MV01_FAULT'],'MV03':['Allarm.MV03_FAULT'],'MV06':['Allarm.MV_06_FAULT']}
selected_timers={'MV01':['Tag_92'],'MV03':['Tag_94'],'MV06':['Tag_97']}
context_nets={'PV01':[1921,1922],'PV02':[1923,1924]}
context_names={'MV01':['WorkData.W33','WorkData.W34'],'MV03':['WorkData.W29','WorkData.W30'],'MV06':['WorkData.W19','WorkData.W20']}
declarations=load('sources/decoded-original/identifier-declarations.json')
network_map={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
assert {p['id']:p['source_networks'] for p in data['profiles']}==expected
assert data['plc_changes']==data['field_verified']==data['tia_verified']==0
assert data['simulator_behavior_tests']=='not_rerun' and data['simulator_development']=='stopped_by_user'
assert all(sha(f)==digest for f,digest in data['sources'].items())
totals=Counter();profiles={p['id']:p for p in data['profiles']};unique_proofs={}
for p in data['profiles']:
    r=next(r for r in repair['records'] if r['plc_id']==p['id'])
    assert p['priority_key']==r['key'] and p['boundary']==r['boundary']=='source_linked'
    assert not p['field_verified'] and not p['tia_verified'] and p['repairs_completed']==0
    assert p['request_reset_actions']==r['request_reset_actions']
    assert p['family']==('motor' if p['id'] in motor_ids else 'gate' if p['id'].startswith('PV') else 'damper')
    assert (ROOT/'alarm-guides'/(p['id']+'.html')).is_file()
    proofs={n['network']:n for n in p['native_networks']}
    assert list(proofs)==p['source_networks']+context_nets.get(p['id'],[])
    for n in p['native_networks']:
        original=nets[n['network']];root=ET.parse(ROOT/n['file']).getroot()
        assert n['file']==original['file'] and n['sha256']==sha(n['file'])
        assert n['network_index']==original['index'] and n['block']==original['block']
        parts=[dict(uid=x.get('UId'),gate=x.get('Gate'),negated_pins=[c.get('PinName') for c in x if tag(c)=='Negated']) for x in root.iter() if tag(x)=='Part']
        wires=[dict(uid=w.get('UId'),endpoints=[dict(kind=tag(x),uid=x.get('UId'),pin=x.get('PinName')) for x in w]) for w in root.iter() if tag(w)=='Wire']
        refs={x.get('UId'):dict(ref_id=x.get('RefId'),name=original['refs'][x.get('UId')].get('name')) for x in root.iter() if tag(x)=='ORef'}
        assert n['parts']==parts and n['wires']==wires and n['refs']==refs
        if n['network'] in unique_proofs:assert unique_proofs[n['network']]==n
        unique_proofs[n['network']]=n
    expected_alarms=list(dict.fromkeys(a['name'] for i in p['source_networks'] for a in nets[i]['actions'] if a['gate']=='SCoil' and a['name'].startswith('Allarm.')))
    if p['id'] in selected_alarms:expected_alarms=selected_alarms[p['id']]
    assert [a['name'] for a in p['alarms']]==expected_alarms
    expected_timers=[dict(network=i,**a) for i in p['source_networks'] for a in nets[i]['actions'] if a['gate']=='SdCoil' and (p['id'] not in selected_timers or a['name'] in selected_timers[p['id']])]
    assert [{k:v for k,v in a.items() if k not in ['native_upstream','value_declarations']} for a in p['timers']]==expected_timers
    for timer in p['timers']:
        value=next(x for x in timer['native_upstream']['reference_pins'] if x['part']==timer['uid'] and x['pin']=='value')
        decl=[d for d in declarations if d['uid']==value['oref'] and d['rid']==value['ref_id'] and d['nid']==network_map[timer['network']]['inferred_original_nid'] and d['name']==value['name']]
        assert timer['value_declarations']==decl and decl and value['name']==timer['preset']['literal']
        assert all(d['kind']=='LiteralConstant' for d in decl)
    expected_contexts=[dict(network=i,**a) for i in context_nets.get(p['id'],p['source_networks'] if p['id'] in context_names else []) for a in nets[i]['actions'] if p['id'] not in context_names or a['name'] in context_names[p['id']]]
    assert [{k:v for k,v in a.items() if k!='native_upstream'} for a in p['context_actions']]==expected_contexts
    for alarm in p['alarms']:
        expected_actions=[dict(network=i,**a) for i in p['source_networks'] for a in nets[i]['actions'] if a['name']==alarm['name']]
        assert [{k:v for k,v in a.items() if k!='native_upstream'} for a in alarm['actions']]==expected_actions
        assert {a['gate'] for a in alarm['actions']}=={'SCoil','RCoil'}
        uses=[u for u in trace['usages'] if u['scope']=='Global' and canon(u['name'])==canon(alarm['name'])]
        assert alarm['usages']==uses
        assert alarm['all_static_writers']==[u for u in uses if u['role']=='write']
        assert alarm['other_scope_usages']==[u for u in trace['usages'] if u['scope']!='Global' and canon(u['name'])==canon(alarm['name'])]
        totals.update(alarm_references=len(uses),alarm_writes=len(alarm['all_static_writers']))
    for action in [a for alarm in p['alarms'] for a in alarm['actions']]+p['timers']+p['context_actions']:
        proof=proofs[action['network']];parts={x['uid']:x for x in proof['parts']}
        # Independent predecessor closure over native input/output endpoints.
        predecessors={uid:set() for uid in parts}
        for wire in proof['wires']:
            outputs={x['uid'] for x in wire['endpoints'] if x['kind']=='PCon' and x['pin']=='out'}
            for x in wire['endpoints']:
                if x['kind']=='PCon' and (x['pin'] in ['in','pre','en'] or x['pin'] and x['pin'].startswith('in') and x['pin'][2:].isdigit()):
                    predecessors[x['uid']].update(outputs)
        reach={action['uid']}
        while True:
            more=reach|{x for uid in reach for x in predecessors[uid]}
            if more==reach:break
            reach=more
        assert action['native_upstream']['parts']==sorted(reach,key=int)
        expected_contacts=[]
        for uid in reach:
            part=parts[uid]
            if part['gate'] not in ['Contact','PContact','NContact']:continue
            for wire in proof['wires']:
                if any(x['kind']=='PCon' and x['uid']==uid and x['pin']=='operand' for x in wire['endpoints']):
                    for x in wire['endpoints']:
                        if x['kind']=='OCon':expected_contacts.append(dict(part=uid,gate=part['gate'],negated_pins=part['negated_pins'],wire=wire['uid'],oref=x['uid'],**proof['refs'][x['uid']]))
        order=lambda rows:sorted(json.dumps(x,sort_keys=True) for x in rows)
        assert order(action['native_upstream']['contacts'])==order(expected_contacts)
        refs=[]
        for wire in proof['wires']:
            for x in wire['endpoints']:
                if x['kind']=='PCon' and x['uid'] in reach:
                    refs.extend(dict(part=x['uid'],gate=parts[x['uid']]['gate'],pin=x['pin'],wire=wire['uid'],oref=c['uid'],**proof['refs'][c['uid']]) for c in wire['endpoints'] if c['kind']=='OCon')
        assert action['native_upstream']['reference_pins']==refs
        totals['command_contact_references']+=len(expected_contacts)

# The repair-relevant differences are native pin facts, not simulated outcomes.
bc=profiles['BC01'];trip=next(a for a in bc['alarms'] if a['name']=='Allarm.BC_01_FC')
reset=next(a for a in trip['actions'] if a['gate']=='RCoil')
assert any(c['name']=='Inputs.BC01 trip wire' and c['negated_pins']==['operand'] for c in reset['native_upstream']['contacts'])
ordinary_resets=[a for p in data['profiles'] for alarm in p['alarms'] if alarm['name']!='Allarm.BC_01_FC' for a in alarm['actions'] if a['gate']=='RCoil']
for a in ordinary_resets:
    assert {c['name'] for c in a['native_upstream']['contacts']}=={'ON','Flag.RESET_ALLARM',a['name']}
fn3=profiles['FN03'];inv=next(a for a in fn3['alarms'] if a['name']=='Allarm.FN03_INV')
inv_set=next(a for a in inv['actions'] if a['gate']=='SCoil')
assert 'Tag_66' not in {c['name'] for c in inv_set['native_upstream']['contacts']}
assert len(fn3['timers'])==2 and {t['uid'] for t in fn3['timers']}=={'854','908'}
assert all(t['preset']['literal']=='S5T#35S' for t in fn3['timers'])
assert {t['preset']['literal'] for t in profiles['FN04']['timers']}=={'S5T#17S'}
assert {t['preset']['literal'] for t in profiles['RD01']['timers']}=={'S5T#5S'}
assert [a['name'] for a in profiles['FN06']['alarms']]==['Allarm.MBVA01_FAULT']
assert {t['preset']['literal'] for t in profiles['PV01']['timers']}=={'S5T#4S','S5T#7S'}
assert {t['preset']['literal'] for t in profiles['PV02']['timers']}=={'S5T#7S'}
for device,value in [('MV01','S5T#150mS'),('MV03','S5T#150S'),('MV06','S5T#150MS')]:
    p=profiles[device];assert len(p['timers'])==1 and p['timers'][0]['preset']['literal']==value
    assert len(p['alarms'])==1 and len(p['alarms'][0]['actions'])==4
    assert len(p['context_actions'])==2 and all(a['gate']=='Move' and a['value']['literal']=='0' for a in p['context_actions'])
    comparison_sets=[a for a in p['alarms'][0]['actions'] if a['network']==1714]
    assert len(comparison_sets)==2
    for a in comparison_sets:
        assert len(a['native_upstream']['contacts'])==2  # includes common and branch ON through native pre pin
        refs=[x for x in a['native_upstream']['reference_pins'] if x['gate'] in ['Gt','Lt']]
        assert len(refs)==2 and {x['pin'] for x in refs}=={'in1','in2'}
        assert next(x for x in refs if x['pin']=='in1')['name'] in context_names[device]
        assert not any(name in json.dumps(a['condition']) for other,names in context_names.items() if other!=device for name in names)
forms=load('registers/repair-record-forms.json')
for form in forms['profiles']:
    assert form['evidence_plan']['sources']['registers/alarm-recovery.json']==sha('registers/alarm-recovery.json')
    for step in form['evidence_plan']['steps']:
        alarm_links=[x for x in step['source_links'] if x['path'].startswith('alarm-guides/')]
        wanted=form['reference_plc_id'] in expected and step['step_id'] in ['stop','recovery']
        assert len(alarm_links)==int(wanted)
        if wanted:assert alarm_links[0]['path']=='alarm-guides/'+form['reference_plc_id']+'.html'
assert len(data['profiles'])==14 and sum(len(p['alarms']) for p in data['profiles'])==29
for n in unique_proofs.values():totals.update(native_parts=len(n['parts']),native_wires=len(n['wires']),native_orefs=len(n['refs']))
result=dict(status='passed',date='2026-10-08',guides=14,motor_guides=9,actuator_guides=5,alarms=29,timer_commands=21,
    native_networks=len(unique_proofs),profile_network_references=sum(len(p['native_networks']) for p in data['profiles']),
    context_actions=sum(len(p['context_actions']) for p in data['profiles']),ordinary_reset_branches=len(ordinary_resets),**totals,
    source_hashes_checked=len(data['sources']),alarm_recovery_sha256=sha('registers/alarm-recovery.json'),
    field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',
    simulator_behavior_tests='not_rerun',scope='Native XML/trace references and manual integration only; not execution')
report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
