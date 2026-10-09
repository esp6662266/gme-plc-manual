"""Independent native XML and exact index-text integrity audit. No execution."""
from pathlib import Path
import csv,hashlib,html,json,xml.etree.ElementTree as ET
from collections import Counter
ROOT=Path(__file__).resolve().parent
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
tag=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s or '').replace('"','').casefold()
report=ROOT/'encoder-position-verification.json';report.write_text(json.dumps(dict(status='checking',scope='Native and index-text integrity; no execution'))+'\n')
d=load('registers/encoder-position.json');m=load('registers/program-model.json');ns={n['id']:n for n in m['networks']};decls=load('sources/decoded-original/identifier-declarations.json');mp={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
expected=[11,1070,1226,1658,1659,1702,1703,1704,1706,1707,1708,1711,1712,1713,1714]+list(range(1756,1767))
assert d['native_ids']==expected and [p['id'] for p in d['native']]==expected
assert not d['field_verified'] and not d['tia_verified'] and d['plc_changes']==0
assert d['simulator_development']=='stopped_by_user' and d['simulator_behavior_tests']=='not_rerun'
assert all(sha(p)==h for p,h in d['sources'].items())
def shape(x):
    return {'tag':tag(x),'attributes':dict(x.attrib),'text':x.text.strip() if x.text else None,'children':[shape(c) for c in x]}
def dec(i,x):return [v for v in decls if v['nid']==mp[i]['inferred_original_nid'] and v['uid']==x.get('UId') and v['rid']==x.get('RefId')]
counts=Counter();ps={p['id']:p for p in d['native']};pid=[]
for p in d['native']:
    i=p['id'];n=ns[i];r=ET.parse(ROOT/n['file']).getroot()
    assert p['file']==n['file'] and p['sha256']==sha(n['file']) and p['title']==n['title'] and p['block']==n['block'] and p['index']==n['index']
    assert p['tree']==shape(r)
    wires=[{'uid':w.get('UId'),'ends':[{'kind':tag(x),'uid':x.get('UId'),'pin':x.get('PinName')} for x in w]} for w in r.iter() if tag(w)=='Wire']
    assert p['wires']==wires
    refs={x.get('UId'):{'ref_id':x.get('RefId'),'name':n['refs'][x.get('UId')]['name'],'declarations':dec(i,x)} for x in r.iter() if tag(x)=='ORef'}
    assert p['refs']==refs
    source_nodes=[x for x in next(x for x in r if tag(x)=='Parts') if tag(x) in ['Part','LRef','CRef']]
    assert len(p['nodes'])==len(source_nodes)
    for node,x in zip(p['nodes'],source_nodes):
        assert node['uid']==x.get('UId') and node['kind']==tag(x) and node['gate']==x.get('Gate') and node['tree']==shape(x) and node['declarations']==dec(i,x)
        assert node['children_declarations']==[{'kind':tag(y),'uid':y.get('UId'),'rid':y.get('RefId'),'declarations':dec(i,y)} for y in x if tag(y) in ['Instance','CodeBlock']]
        pins=[]
        for w in wires:
            for pin in w['ends']:
                if pin['kind']=='PCon' and pin['uid']==x.get('UId'):
                    pins.append({'pin':pin['pin'],'wire':w['uid'],'references':[dict(oref=q['uid'],**refs[q['uid']]) for q in w['ends'] if q['kind']=='OCon'],'peers':[q for q in w['ends'] if q!=pin and q['kind']!='OCon']})
        assert node['pins']==pins
        if tag(x)=='LRef':
            assert node['declarations'] and node['children_declarations']
            assert all(c['declarations'] for c in node['children_declarations'])
            pid.append((i,x.get('UId'),node['declarations'][0]['name'],node['children_declarations'][0]['declarations'][0]['name']))
    counts.update(native_parts=sum(tag(x)=='Part' for x in source_nodes),native_lrefs=sum(tag(x)=='LRef' for x in source_nodes),native_crefs=sum(tag(x)=='CRef' for x in source_nodes),native_wires=len(wires),native_orefs=len(refs))
assert pid==[(11,'366','CONT_S','PIDMV01'),(1756,'23','High_Speed_Counter','MV01_Encoder'),(1757,'22','High_Speed_Counter','MV02_Encoder'),(1758,'22','High_Speed_Counter','MV03_Encoder'),(1759,'23','High_Speed_Counter','MV05_Encoder'),(1760,'23','High_Speed_Counter','MV06_Encoder')]
def node(i,uid):return next(n for n in ps[i]['nodes'] if n['uid']==uid)
def vals(n,pin):return [r['name'] for p in n['pins'] if p['pin']==pin for r in p['references']]
def gate_nodes(i,gate):return [n for n in ps[i]['nodes'] if n['gate']==gate]
def find(i,gate,pin,value):return next(n for n in gate_nodes(i,gate) if vals(n,pin)==[value])
def neg(n):return [x['attributes']['PinName'] for x in n['tree']['children'] if x['tag']=='Negated']
def peers(n,pin):return [q for p in n['pins'] if p['pin']==pin for q in p['peers']]
electrical=load('registers/electrical-trace.json')
hmi=list(csv.DictReader((ROOT/'registers/equipment-hmi.csv').open(encoding='utf-8-sig')))
assert [c['id'] for c in d['channels']]==['MV01','MV02','MV03','MV05','MV06']
for j,c in enumerate(d['channels']):
 id_=c['id'];ri=c['reading_network'];di=c['data_network'];call=next(n for n in ps[ri]['nodes'] if n['kind']=='LRef');conv=next(n for n in ps[di]['nodes'] if n['kind']=='CRef')
 assert ri==1756+j and di==1762+j and c['software_index']==j
 assert c['counter_call']==call and c['conversion_call']==conv
 assert not c['field_verified'] and not c['tia_verified'] and c['plc_changes']==0
 assert vals(call,'SwGate')==[f'fill_unit1.CONTROL_SIGNALS.SW_GATE{j}'] and vals(call,'CountValue')==[f'fill_unit1.ACT_CNTV{j}']
 assert c['raw_count']==f'fill_unit1.ACT_CNTV{j}' and c['total']==f'CNT_Act_{j}' and c['memory']==f'Memory encoder.Encoder_CH{j:02d}' and c['divided']==f'CNTV{j}_100' and c['divided_memory']==f'Memory encoder.Encoder_CH{j:02d}_10' and c['position']==f'Data.Pot_{id_}'
 sim=find(ri,'Contact','operand','Simulation(1)');em=find(ri,'Contact','operand','EM_OK')
 assert neg(sim)==['operand'] and not neg(em)
 assert {'kind':'PCon','uid':em['uid'],'pin':'out'} in peers(call,'en')
 assert {'kind':'PCon','uid':sim['uid'],'pin':'out'} in peers(em,'in')
 unknown=[p for p in call['pins'] if p['pin']=='SetCountValue'][0]
 assert len(unknown['references'])==1 and unknown['references'][0]['ref_id'] is None and unknown['references'][0]['name'] is None
 assert vals(call,'ErrorAck')==(['Flag.RESET_ALLARM'] if j==0 else [None])
 assert vals(call,'EventAck')==(['Flag.RESET_ALLARM'] if j==0 else [None])
 add=find(di,'Add','out',c['total']);div=find(di,'Div','out',c['divided'])
 assert vals(add,'in1')==[c['memory']] and vals(add,'in2')==[c['raw_count']]
 assert vals(div,'in1')==[c['total']] and vals(div,'in2')==['100']
 for n in [add,div]:assert {'tag':'TemplateValue','attributes':{'Name':'SrcType','Type':'Type'},'text':'DInt','children':[]} in n['tree']['children']
 assert any(vals(n,'in')==[c['divided']] and vals(n,'out1')==[c['divided_memory']] for n in gate_nodes(di,'Move'))
 assert any(vals(n,'in')==['0'] and vals(n,'out1')==[c['divided_memory']] for n in gate_nodes(di,'Move'))
 assert any(vals(n,'in')==['INT#0'] and vals(n,'out1')==[c['memory']] for n in gate_nodes(di,'Move'))
 g=find(di,'Coil','operand',f'fill_unit1.CONTROL_SIGNALS.SW_GATE{j}');assert c['gate_coil']==g
 closed=find(di,'Contact','operand','Inputs.MV03 Close' if id_=='MV03' else id_+'_Close')
 assert neg(closed)==['operand'] and {'kind':'PCon','uid':closed['uid'],'pin':'out'} in peers(g,'in')
 assert any(vals(n,'operand')==[f'fill_unit1.CONTROL_SIGNALS.SW_GATE{j}'] and neg(n)==['operand'] for n in gate_nodes(di,'Contact'))
 assert vals(conv,'IN0')==['ON'] and vals(conv,'Analog_input')==[c['divided_memory']] and vals(conv,'OutValue')==[c['position']] and vals(conv,'Out_of_range')==[f'Allarm.Pot_{id_}_OFR']
 assert conv['children_declarations'][0]['declarations'][0]['name']=='Signal linearization'
 assert vals(conv,'Coeff')==(['Coeff.Coeff_MV06'] if id_=='MV06' else [f'Coeff.COEFF_TRASM_{id_}'])
 assert vals(conv,'Zero')==(['Coeff.Zero_MV06'] if id_=='MV06' else [f'Coeff.ZERO_TRASM_{id_}'])
 assert any(vals(n,'in')==[c['total']] and vals(n,'out1')==[c['memory']] for n in gate_nodes(1761,'Move'))
 assert neg(find(1761,'Contact','operand','EM_OK'))==['operand']
 assert c['hmi_reference_rows']==[r for r in hmi if r['설비 ID']==id_]
 assert c['circuit_reference']==next((x for x in electrical['devices'] if x['id']==id_),None)
 monitor=c['command_monitor'];up=monitor['open'];down=monitor['close'];threshold=[2000,1000,3400,700,2200][j]
 assert (up,down)==[('WorkData.W33','WorkData.W34'),('WorkData.W35','WorkData.W36'),('WorkData.W29','WorkData.W30'),('WorkData.W31','WorkData.W32'),('WorkData.W19','WorkData.W20')][j]
 assert vals(find(1713,'Add','out',up),'in2')==['1'] and vals(find(1713,'Sub','out',down),'in2')==['1']
 assert vals(find(1714,'Gt','in1',up),'in2')==[str(threshold)] and vals(find(1714,'Lt','in1',down),'in2')==[str(-threshold)]
 assert monitor['open_threshold']==threshold and monitor['close_threshold']==-threshold
 assert c['calibration_network']=={'MV01':1703,'MV03':1707}.get(id_)
 if c['calibration_network']:
  ci=c['calibration_network'];mv=find(ci,'Move','out1',id_+'_Encoder.NewCountValue')
  assert vals(mv,'in')==['0'] and mv['tree']['attributes']['DisableENO']=='true'
  assert neg(find(ci,'Contact','operand',id_+'_Encoder.SetCountValue'))==['operand']
  assert vals(next(n for n in gate_nodes(ci,'RCoil')),'operand')==['HMI_DB.ResetEncoderProcedure_'+id_]
  assert vals(next(n for n in gate_nodes(ci,'Coil')),'operand')==[id_+'_Encoder.SetCountValue']
# Position transfer and command counters must not be presented as the same measurement.
assert vals(find(1658,'Div','in2','28000'),'in1')==['App3']
assert vals(find(1658,'Gt','in1','Analog_input'),'in2')==['-1382']
assert any(vals(n,'in2')==['32767'] for n in gate_nodes(1658,'Le'))
assert any(vals(n,'in')==['-9999'] for n in gate_nodes(1658,'Move'))
assert neg(find(1659,'Contact','operand','IN0'))==['operand']
trace=load('registers/signal-trace.json')['usages'];selectors=[]
symbols=list(csv.DictReader((ROOT/'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
source_paths={'registers/program-model.json','registers/signal-trace.json','sources/live_index.json','sources/block_summary.json','sources/decoded-original/network-map.json','sources/decoded-original/identifier-declarations.json','registers/plc-symbols.csv','registers/equipment-hmi.csv','registers/electrical-trace.json'}
for p in d['native']:
 source_paths.add(p['file'])
 for ref in p['refs'].values():source_paths.update('sources/decoded-original/'+x['file'] for x in ref['declarations'])
 for n in p['nodes']:
  source_paths.update('sources/decoded-original/'+x['file'] for x in n['declarations'])
  source_paths.update('sources/decoded-original/'+x['file'] for child in n['children_declarations'] for x in child['declarations'])
 for uid in p['refs']:
  for u in trace:
   if u['network']==p['id'] and u['oref']==uid and u['scope'] in ['Global','Local'] and u['name']:
    s=(u['name'],u['scope'],u['block'] if u['scope']=='Local' else None)
    if s not in selectors:selectors.append(s)
assert [(s['name'],s['scope'],s['block']) for s in d['signals']]==selectors
for s in d['signals']:
 same=lambda u:canon(u['name'])==canon(s['name']) and u['scope']==s['scope'] and (s['scope']!='Local' or u['block']==s['block'])
 assert s['usages']==[u for u in trace if same(u)] and s['other_scope_usages']==[u for u in trace if canon(u['name'])==canon(s['name']) and not same(u)]
 assert s['symbols']==([x for x in symbols if canon(x['원본 심볼'])==canon(s['name'])] if s['scope']=='Global' else [])
 source_paths.update(u['file'] for u in s['usages']+s['other_scope_usages'])
assert d['sources']=={p:sha(p) for p in sorted(source_paths)}
for f,h in load('registers/simulator-freeze.json')['files'].items():assert sha(f)==h
ht=(ROOT/'encoder-position.html').read_text()
for c in d['channels']:assert 'id="position-'+c['id']+'"' in ht
for p in d['native']:
 for w in p['wires']:assert 'id="wire-'+str(p['id'])+'-'+w['uid']+'"' in ht
for key,id_ in [('P19','MV01'),('P20','MV03'),('P21','MV06')]:assert 'encoder-position.html#position-'+id_ in (ROOT/'repair-guides'/f'{key}.html').read_text()
forms=load('registers/repair-record-forms.json')
for p in forms['profiles']:assert p['evidence_plan']['sources']['registers/encoder-position.json']==sha('registers/encoder-position.json')
for key in ['P19','P20','P21']:assert 'encoder-position.html#position-' in json.dumps(next(p for p in forms['profiles'] if p['key']==key))
result=dict(status='passed',date='2026-10-08',channels=5,native_networks=len(expected),counter_calls=5,conversion_calls=5,calibration_paths=2,symptom_guidance_rows=25,signal_scopes=len(d['signals']),signal_pin_references=sum(len(s['usages']) for s in d['signals']),other_scope_references=sum(len(s['other_scope_usages']) for s in d['signals']),source_hashes_checked=len(d['sources']),encoder_position_sha256=sha('registers/encoder-position.json'),field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun',simulator_files_hashes_unchanged=True,scope='Native LAD counter and position proof, not hardware configuration or PLC execution',**dict(counts))
report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
