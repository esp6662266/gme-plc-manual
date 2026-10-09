"""Independent native channel/reference audit; no PLC or simulator execution."""
from pathlib import Path
from collections import Counter
import hashlib,json,csv,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
tag=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s or '').replace('"','').casefold()
report=ROOT/'sensor-measurement-verification.json';report.write_text(json.dumps(dict(status='checking'))+'\n')
d=load('registers/sensor-measurement.json');m=load('registers/program-model.json');nets={n['id']:n for n in m['networks']}
t=load('registers/signal-trace.json')['usages'];declarations=load('sources/decoded-original/identifier-declarations.json')
map_={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
assert all(sha(f)==s for f,s in d['sources'].items())
assert not d['field_verified'] and not d['tia_verified'] and d['plc_changes']==0
assert d['simulator_development']=='stopped_by_user' and d['simulator_behavior_tests']=='not_rerun'
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

expected=[('TC01',1739,272),('TC02',1740,274),('TC03',1741,276),('TC04',1731,256),('TC05',1732,260),('TC06',1742,278),('TC07',1743,280),('TC09',1733,386),('TC10',1734,390),('PSH01',1745,284),('PSH02',1746,286),('PSH03',1747,320),('PC01',1775,322),('DP01',1773,398),('DP02',1774,400),('RO01',1748,352),('RO02',1749,354),('RO03',1750,356),('RO04',1751,358)]
assert [(c['id'],c['network'],int(c['raw_symbol']['백업 주소'][3:])) for c in d['channels']]==expected
symbols=list(csv.DictReader((ROOT/'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
hmi=list(csv.DictReader((ROOT/'registers/equipment-hmi.csv').open(encoding='utf-8-sig')))
names=list(dict.fromkeys(v for c in d['channels'] for k,vs in c['call']['bindings'].items() if k!='IN0' for v in vs))
assert [s['name'] for s in d['signals']]==names and len(names)==95
for s in d['signals']:
    assert s['scope']=='Global'
    assert s['usages']==[u for u in t if u['scope']=='Global' and canon(u['name'])==canon(s['name'])]
    assert s['other_scope_usages']==[u for u in t if u['scope']!='Global' and canon(u['name'])==canon(s['name'])]
    for u in s['usages']+s['other_scope_usages']:
        p=proofs[u['network']]
        assert p['refs'][u['oref']]['name']==u['name']
        w=next(w for w in p['wires'] if w['uid']==u['wire'])
        assert dict(kind='PCon',uid=u['part'],pin=u['pin']) in w['endpoints']
        assert dict(kind='OCon',uid=u['oref'],pin=None) in w['endpoints']
    total['signal_pin_references']+=len(s['usages']);total['other_scope_references']+=len(s['other_scope_usages'])
assert d['selected_networks']==sorted({1658,1659,1071}|{u['network'] for s in d['signals'] for u in s['usages']+s['other_scope_usages']})
assert sorted(proofs)==d['selected_networks'] and len(proofs)==42
def base(a):return {k:v for k,v in a.items() if k!='native_upstream'}
checks=[]
for c in d['channels']:
    p=proofs[c['network']];call=p['calls'][0]
    assert c['call']=={k:v for k,v in call.items() if k not in ['cref_ref_id','block_ref_id','native_declarations']}
    assert call['callee']=='Signal linearization' and call['bindings']['IN0']==['ON']
    assert c['raw_symbol']==next(s for s in symbols if canon(s['원본 심볼'])==canon(call['bindings']['Analog_input'][0]))
    focus=list(dict.fromkeys(v for k,vs in call['bindings'].items() if k!='IN0' for v in vs))
    assert c['focus']==focus
    transfers=[dict(network=1071,**a) for a in nets[1071]['actions'] if a.get('value',{}).get('op')=='read' and canon(a['value']['name'])==canon(call['bindings']['Analog_input'][0])]
    assert [base(a) for a in c['raw_transfers']]==transfers
    assert [base(a) for a in c['post_actions']]==[dict(network=c['network'],**a) for a in nets[c['network']]['actions']]
    out=next(s for s in d['signals'] if s['name']==call['bindings']['OutValue'][0])
    ofr=next(s for s in d['signals'] if s['name']==call['bindings']['Out_of_range'][0])
    assert c['value_usages']==out['usages'] and c['ofr_usages']==ofr['usages']
    assert c['value_reads']==[u for u in out['usages'] if u['role']=='read']
    assert c['value_writes']==[u for u in out['usages'] if u['role']=='write']
    assert c['hmi_reference_rows']==[h for h in hmi if h['설비 ID']==c['id']]
    expected_comparisons=list({(u['network'],u['part']):u for u in c['value_reads'] if u['gate'] in ['Gt','Ge','Lt','Le','Eq','Ne','Sub','Add','Mul','Div']}.values())
    assert [x['usage'] for x in c['comparison_uses']]==expected_comparisons
    checks.extend((dict(network=x['usage']['network'],uid=x['usage']['part']),x['native_upstream']) for x in c['comparison_uses'])
    checks.append((dict(network=c['network'],uid=call['uid']),c['native_upstream']))
    checks.extend((a,a['native_upstream']) for a in c['raw_transfers']+c['post_actions'])
    assert c['circuit']['diagram_visually_reviewed'] and not c['circuit']['current_hardware_verified']
    assert c['circuit']['page']==c['circuit']['fg']+1 and c['circuit']['module_page']==c['circuit']['module_fg']+1
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
def pin(i,uid,name):
    p=proofs[i];return [p['refs'][r['uid']]['name'] for w in p['wires'] if any(x['kind']=='PCon' and x['uid']==uid and x['pin']==name for x in w['endpoints']) for r in w['endpoints'] if r['kind']=='OCon']
assert pin(1750,'566','in1')==['Data.Oxigen_RO02'] and pin(1750,'566','in2')==['11'] and pin(1750,'566','out')==['Data.RO03']
assert pin(1658,'181','in2')==['28000'] and pin(1658,'193','in')==['-9999']
cs={c['id']:c for c in d['channels']}
assert cs['PSH01']['call']['bindings']['OutValue']==['Data.Press_PC01'] and cs['PC01']['call']['bindings']['OutValue']==['Data.PC_01']
assert cs['PSH01']['value_reads']==[] and {u['network'] for u in cs['PC01']['value_reads']}=={1901,1987}
assert {u['network'] for u in cs['TC01']['value_writes']}=={1092,1739}
assert {u['network'] for u in cs['TC02']['value_writes']}=={1092,1740}
assert all(u['legacy_simulation_block'] for c in [cs['TC01'],cs['TC02']] for u in c['value_writes'] if u['network']==1092)
assert len(cs['RO03']['value_writes'])==2
off_ids=['TC05','TC07','TC10','RO01','RO02','RO03','RO04']
for c in d['channels']:
    assert c['native_upstream']['contacts'][0]['name']==('OFF' if c['id'] in off_ids else 'ON')
    assert c['native_upstream']['contacts'][0]['negated_pins']==[]
    assert c['call']['enable']['args'][1]['name']==('OFF' if c['id'] in off_ids else 'ON')
assert d['observations'][0]['channels']==off_ids
assert sum(bool(c['raw_transfers']) for c in cs.values())==15
assert [c['id'] for c in d['channels'] if not c['hmi_reference_rows']]==['TC09','TC10','DP01','DP02']
assert len(d['observations'])==7 and any('Data.Oxigen_RO02' in o['text'] for o in d['observations'])
pages={p['page']:p['text'] for p in load('sources/electrical-page-text.json')}
assert '-30°C......250°C' in pages[80] and '-30...350°C' in pages[105]
assert 'SPARE' in pages[79] and 'SPARE' in pages[172]
assert d['reviewed_fgs']==[75,76,77,78,79,80,81,104,106,107,108,110,169,171,172]
for fg in d['reviewed_fgs']:
    assert 'assets/sensor-circuits/FG'+str(fg)+'.png' in d['sources']
for c in cs.values():assert str(int(c['raw_symbol']['백업 주소'][3:])) in pages[c['circuit']['module_page']]
for f,digest in load('registers/simulator-freeze.json')['files'].items():assert sha(f)==digest
for f in ['procedures/BR01.html','repair-guides/P11.html']:
    assert 'sensor-measurement.html' in (ROOT/f).read_text()
form=next(f for f in load('registers/repair-record-forms.json')['profiles'] if f['key']=='P11')
assert form['evidence_plan']['sources']['registers/sensor-measurement.json']==sha('registers/sensor-measurement.json')
assert 'sensor-measurement.html' in json.dumps(form)
text=(ROOT/'sensor-measurement.html').read_text()
for c in d['channels']:
    start=text.index('id="sensor-'+c['id']+'"')
    end=text.find('<h2',start+1)
    section=text[start:end] if end>=0 else text[start:]
    for term in [c['raw_symbol']['백업 주소'],c['call']['bindings']['OutValue'][0],c['call']['bindings']['Coeff'][0],c['call']['bindings']['Zero'][0],'증상별 관찰·배제·다음 확인','HMI 표시와 PLC값이 맞지 않음','호출 앞 en 조건:']:
        assert term in section,(c['id'],term)
    assert ('(OFF)' if c['id'] in off_ids else '(ON)') in section
    assert 'IN0 값 핀: ON' in section
    assert 'sensor-measurement.html#sensor-'+c['id'] in (ROOT/('procedures/'+c['id']+'.html')).read_text()
assert 'view=review' in text and 'view=evidence-review' not in text
result=dict(status='passed',date='2026-10-08',channels=19,temperature_channels=9,pressure_channels=6,oxygen_channels=4,
 native_networks=len(proofs),signal_scopes=len(d['signals']),reviewed_fgs=15,source_hashes_checked=len(d['sources']),
 sensor_measurement_sha256=sha('registers/sensor-measurement.json'),field_verified=False,tia_verified=False,plc_changes=0,
 simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun',simulator_files_hashes_unchanged=True,
 scope='Native bindings/refs and hashed visually reviewed OEM paths; not current hardware configuration or PLC execution',**dict(total))
report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
