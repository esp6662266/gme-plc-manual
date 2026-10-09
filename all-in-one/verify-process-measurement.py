"""Audit process conversion/call/stop evidence against native XML; no evaluation."""
from pathlib import Path
from collections import Counter
import hashlib, json, csv, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
tag=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s or '').replace('"','').casefold()
report=ROOT/'process-measurement-verification.json';report.write_text(json.dumps(dict(status='checking',scope='Native source; no execution'))+'\n')
d=load('registers/process-measurement.json');m=load('registers/program-model.json');nets={n['id']:n for n in m['networks']}
t=load('registers/signal-trace.json')['usages'];declarations=load('sources/decoded-original/identifier-declarations.json')
map_={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
analog=[1658,1659,1686,1687,1724,1752,1753,1754,1755,1834]
alarm_nets=[1227,1979,1980,1981,1985,1986,1987,1990,1991]
names=['Allarm.MAX_MAX_TC09','Allarm.MAX_MAX_TC01_TEMP','Allarm.MAX_TC04_TEMP','Allarm.MAX_TC05_TEMP','Allarm.MAX_MAX_TC03_TEMP','Allarm.RO01_Signal_Fault','Allarm.TC01_TC02_COMP_FAULT','Allarm.Low_Aspiration','Allarm.PSL_AIR_LOW','Allarm.HYDROGEN_BOX_FAULT','Allarm.EmergencyStopTC1_2']
assert d['analog_networks']==analog and d['alarm_networks']==alarm_nets
assert d['selected_networks']==sorted(analog+alarm_nets+[1858])
assert [p['network'] for p in d['native_networks']]==d['selected_networks']
assert not d['field_verified'] and not d['tia_verified'] and d['plc_changes']==0
assert d['simulator_development']=='stopped_by_user' and d['simulator_behavior_tests']=='not_rerun'
assert all(sha(f)==s for f,s in d['sources'].items())
proofs={p['network']:p for p in d['native_networks']};total=Counter()
for p in d['native_networks']:
    i=p['network'];n=nets[i];root=ET.parse(ROOT/n['file']).getroot()
    assert p['file']==n['file'] and p['sha256']==sha(n['file']) and p['block']==n['block'] and p['index']==n['index'] and p['title']==n['title']
    parts=[dict(uid=x.get('UId'),gate=x.get('Gate'),attributes=dict(x.attrib),negated_pins=[c.get('PinName') for c in x if tag(c)=='Negated'],templates=[dict(attributes=dict(c.attrib),value=c.text) for c in x if tag(c)=='TemplateValue']) for x in root.iter() if tag(x)=='Part']
    assert p['parts']==parts
    wires=[dict(uid=w.get('UId'),endpoints=[dict(kind=tag(x),uid=x.get('UId'),pin=x.get('PinName')) for x in w]) for w in root.iter() if tag(w)=='Wire']
    assert p['wires']==wires
    refs={}
    for x in [x for x in root.iter() if tag(x)=='ORef']:
        uid=x.get('UId');rid=x.get('RefId');name=n['refs'][uid].get('name')
        refs[uid]=dict(ref_id=rid,name=name,declarations=[v for v in declarations if v['uid']==uid and v['rid']==rid and v['nid']==map_[i]['inferred_original_nid'] and v['name']==name])
    assert p['refs']==refs
    calls=[]
    for c in [c for c in m['calls'] if c['network']==i]:
        ref=next(x for x in root.iter() if tag(x)=='CRef' and x.get('UId')==c['uid']);block=next(x for x in ref if tag(x)=='CodeBlock')
        decl=[v for v in declarations if v['uid']==block.get('UId') and v['rid']==block.get('RefId') and v['nid']==map_[i]['inferred_original_nid'] and v['name']==c['callee']]
        assert decl
        calls.append(dict(**c,cref_ref_id=ref.get('RefId'),block_ref_id=block.get('RefId'),native_declarations=decl))
        # Independently rebuild every parameter binding from native wire endpoints.
        bindings={}
        for w in wires:
            for pin in w['endpoints']:
                if pin['kind']=='PCon' and pin['uid']==c['uid'] and pin['pin'] not in ['en','eno']:
                    binding=[refs[x['uid']]['name'] for x in w['endpoints'] if x['kind']=='OCon']
                    if binding:bindings[pin['pin']]=binding
        assert c['bindings']==bindings
    assert p['calls']==calls
    total.update(native_parts=len(parts),native_wires=len(wires),native_orefs=len(refs),native_calls=len(calls))

def base(a):return {k:v for k,v in a.items() if k not in ['native_upstream','value_declarations']}
def reads(v):
    if isinstance(v,dict):
        if v.get('op')=='read':yield v['name']
        for x in v.values():yield from reads(x)
    elif isinstance(v,list):
        for x in v:yield from reads(x)
assert [base(a) for a in d['analog_actions']]==[dict(network=i,**a) for i in analog for a in nets[i]['actions']]
assert [a['name'] for a in d['alarms']]==names
commands=list(d['analog_actions'])+[d['stop_action']]
for a in d['alarms']:
    assert a['scope']=='Global'
    expected=[dict(network=i,**x) for i in alarm_nets for x in nets[i]['actions'] if x['name']==a['name']]
    assert [base(x) for x in a['actions']]==expected
    timer_names={n for x in expected for n in reads(x['condition']) if n.startswith('Tag_')}
    timers=[dict(network=i,**x) for i in alarm_nets for x in nets[i]['actions'] if x['gate']=='SdCoil' and x['name'] in timer_names]
    assert [base(x) for x in a['timers']]==timers
    support_names={canon(n) for x in expected+timers for n in reads(x['condition'])}
    supports=[dict(network=i,**x) for i in {x['network'] for x in expected} for x in nets[i]['actions'] if x['gate'] in ['Add','Sub','Mul','Div','Convert'] and canon(x['name']) in support_names]
    assert [base(x) for x in a['support_actions']]==supports
    assert a['usages']==[u for u in t if u['scope']=='Global' and canon(u['name'])==canon(a['name'])]
    assert a['other_scope_usages']==[u for u in t if u['scope']!='Global' and canon(u['name'])==canon(a['name'])]
    assert a['writer_coverage']==('selected_original_set_reset' if expected else 'no_exact_global_writer_in_reconstructed_index')
    if expected:assert {x['gate'] for x in expected}=={'SCoil','RCoil'}
    commands+=a['actions']+a['timers']+a['support_actions']
assert base(d['stop_action'])==dict(network=1858,**next(a for a in nets[1858]['actions'] if a['name']=='Flag.Start_Burner'))
assert d['stop_alarm_names']==list(dict.fromkeys(n for n in reads(d['stop_action']['condition']) if n.startswith('Allarm.')))
assert len(d['stop_alarm_names'])==15 and set(names)<=set(d['stop_alarm_names'])
checks=[(a,a['native_upstream']) for a in commands]+[(dict(network=c['network'],uid=c['call']['uid']),c['native_upstream']) for c in d['channels']]
for a,closure in checks:
    p=proofs[a['network']];nodes={x['uid']:x for x in p['parts']};nodes.update({c['uid']:dict(gate='CRef',negated_pins=[]) for c in p['calls']})
    pred={uid:set() for uid in nodes}
    for w in p['wires']:
        outs={x['uid'] for x in w['endpoints'] if x['kind']=='PCon' and x['pin'] in ['out','eno']}
        for x in w['endpoints']:
            if x['kind']=='PCon' and (x['pin'] in ['in','en','pre'] or x['pin'] and x['pin'].startswith('in') and x['pin'][2:].isdigit()):pred[x['uid']].update(outs)
    reach={a['uid']}
    while True:
        added=reach|{x for uid in reach for x in pred[uid]}
        if added==reach:break
        reach=added
    assert closure['nodes']==sorted(reach,key=int)
    pins=[];contacts=[]
    for w in p['wires']:
        for x in w['endpoints']:
            if x['kind']!='PCon' or x['uid'] not in reach:continue
            for ref in w['endpoints']:
                if ref['kind']!='OCon':continue
                row=dict(part=x['uid'],gate=nodes[x['uid']]['gate'],pin=x['pin'],wire=w['uid'],oref=ref['uid'],name=p['refs'][ref['uid']]['name'],ref_id=p['refs'][ref['uid']]['ref_id'])
                pins.append(row)
                if row['gate'] in ['Contact','PContact','NContact'] and row['pin']=='operand':contacts.append(dict(**row,negated_pins=nodes[x['uid']]['negated_pins']))
    assert closure['reference_pins']==pins and closure['contacts']==contacts
    total['command_contact_references']+=len(contacts)
    if a.get('gate')=='SdCoil':
        value=next(x for x in pins if x['part']==a['uid'] and x['pin']=='value')
        assert a['value_declarations']==p['refs'][value['oref']]['declarations'] and a['value_declarations']
        assert value['name']==a['preset']['literal'] and all(x['kind']=='LiteralConstant' for x in a['value_declarations'])
        total['timer_commands']+=1
circuit=next(x for x in load('registers/electrical-trace.json')['devices'] if x['id']=='BR01')
assert [(c['network'],c['address']) for c in d['channels']]==[(1752,'%IW360'),(1753,'%IW362'),(1754,'%IW364'),(1755,'%IW366')]
for c in d['channels']:
    assert c['call']==proofs[c['network']]['calls'][0] and c['call']['callee']=='Signal linearization'
    assert c['circuit']==next(x for x in circuit['paths'] if x['backup'].upper().startswith(c['address']+' '))
assert [(o['network'],o['address'],o['value'],o['scale'],o['part']) for o in d['outputs']]==[(1686,'%QW310','Data.Burner_Air_Out','272','536'),(1687,'%QW308','Data.Burner_Gas_Out','285','590')]
for o in d['outputs']:assert o['circuit']==next(x for x in circuit['paths'] if x['backup'].upper().startswith(o['address']+' '))
def pin(i,uid,name):
    p=proofs[i];return [p['refs'][r['uid']]['name'] for w in p['wires'] if any(x['kind']=='PCon' and x['uid']==uid and x['pin']==name for x in w['endpoints']) for r in w['endpoints'] if r['kind']=='OCon']
assert pin(1686,'536','in2')==['272'] and pin(1687,'590','in2')==['285']
assert pin(1658,'181','in2')==['28000'] and pin(1658,'193','in')==['-9999']
for uid in ['164','167','174']:
    part=next(x for x in proofs[1658]['parts'] if x['uid']==uid)
    assert {x['attributes']['Name']:x['value'] for x in part['templates']}=={'SrcType':'Int','DestType':'DInt'}
assert pin(1658,'170','in1')==['App5'] and pin(1658,'170','in2')==['App6']
assert pin(1658,'177','in1')==['App3'] and pin(1658,'177','in2')==['App4']
assert pin(1754,'669','in')==['1'] and pin(1754,'669','out1')==['Data.MASSICO_FLOW_GAS']
assert nets[1755]['actions']==[]
assert nets[1659]['writes']==['outvalue']
lookup={a['name']:a for a in d['alarms']}
assert [u['role'] for u in lookup['Allarm.EmergencyStopTC1_2']['usages']]==['read']
reset=next(a for a in lookup['Allarm.PSL_AIR_LOW']['actions'] if a['gate']=='RCoil')
assert any(x['name']=='Inputs.Low Pressure Air' and x['negated_pins']==[] for x in reset['native_upstream']['contacts'])
low=next(a for a in lookup['Allarm.Low_Aspiration']['actions'] if a['gate']=='RCoil')
assert {'Inputs.FN01 Run','Inputs.FN04 Run'}<={x['name'] for x in low['native_upstream']['contacts']}
hyd=next(a for a in lookup['Allarm.HYDROGEN_BOX_FAULT']['actions'] if a['gate']=='SCoil')
assert any(x['name']=='Inputs.NITROGEN TANK READY' and x['negated_pins']==['operand'] for x in hyd['native_upstream']['contacts'])
assert any(x['name']=='ServiceBit' for x in hyd['native_upstream']['contacts'])
assert {x['name']:x['preset']['literal'] for a in d['alarms'] for x in a['timers']}=={'Tag_100':'S5T#6S','Tag_103':'S5T#3S','Tag_104':'S5T#1M','Tag_105':'S5T#1M','Tag_107':'S5T#1M','Tag_108':'S5T#1M','Tag_109':'S5T#30S'}
symbols=list(csv.DictReader((ROOT/'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
assert len(d['signals'])==66 and sum(s['scope']=='Local' for s in d['signals'])==10
for s in d['signals']:
    selected=lambda u: u['scope']==s['scope'] and (s['block'] is None or u['block']==s['block'])
    assert s['usages']==[u for u in t if canon(u['name'])==canon(s['name']) and selected(u)]
    assert s['other_scope_usages']==[u for u in t if canon(u['name'])==canon(s['name']) and not selected(u)]
    assert s['symbols']==[x for x in symbols if s['scope']=='Global' and canon(x['원본 심볼'])==canon(s['name'])]
    if s['scope']=='Local':assert s['block']=='signal linearization' and s['symbols']==[]
    total['signal_pin_references']+=len(s['usages']);total['other_scope_references']+=len(s['other_scope_usages'])
assert d['hmi_reference_rows']==[r for r in csv.DictReader((ROOT/'registers/equipment-hmi.csv').open(encoding='utf-8-sig')) if r['설비 ID']=='BR01']
assert len(d['observations'])==6 and all('확인 대기' in o['status'] for o in d['observations'])
for file in ['repair-guides/P11.html','procedures/BR01.html']:
    text=(ROOT/file).read_text();assert 'measurement-trace.html' in text and 'process-stop-alarms.html' in text
form=next(x for x in load('registers/repair-record-forms.json')['profiles'] if x['key']=='P11')
assert form['evidence_plan']['sources']['registers/process-measurement.json']==sha('registers/process-measurement.json')
assert 'measurement-trace.html' in json.dumps(form) and 'process-stop-alarms.html' in json.dumps(form)
result=dict(status='passed',date='2026-10-08',native_networks=len(proofs),input_channels=4,output_channels=2,
 process_alarm_names=11,alarms_with_original_actions=10,unresolved_alarm_writers=1,stop_alarm_references=15,
 analog_commands=len(d['analog_actions']),signal_scopes=66,local_signal_scopes=10,source_hashes_checked=len(d['sources']),
 process_measurement_sha256=sha('registers/process-measurement.json'),field_verified=False,tia_verified=False,plc_changes=0,
 simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun',scope='Native conversion/call/alarm source coverage; not execution or protective setting approval',**dict(total))
report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
