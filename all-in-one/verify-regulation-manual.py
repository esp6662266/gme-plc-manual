"""Independent native XML and exact index-text integrity audit. No execution."""
from pathlib import Path
import csv,hashlib,html,json,xml.etree.ElementTree as ET
from collections import Counter
ROOT=Path(__file__).resolve().parent
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
tag=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s or '').replace('"','').casefold()
report=ROOT/'regulation-manual-verification.json';report.write_text(json.dumps(dict(status='checking',scope='Native and index-text integrity; no execution'))+'\n')
d=load('registers/regulation-manual.json');m=load('registers/program-model.json');ns={n['id']:n for n in m['networks']};decls=load('sources/decoded-original/identifier-declarations.json');mp={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
expected=[5,7,8,11,12,15,16,1686,1687,1688,1689,1702,1704,1705,1706,1708,1709,1710,1711,1712,1713,1714,1721,1722,1724,1830,1832,1834,1835,1870,1871,1900,1901]
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
assert pid==[(5,'109','CONT_S','PID_MV05'),(7,'172','CONT_S','PID_MV-02'),(11,'366','CONT_S','PIDMV01'),(15,'507','CONT_S','PID_MV03'),(1832,'663','CONT_C','PID_Stechio')]
def node(i,uid):return next(n for n in ps[i]['nodes'] if n['uid']==uid)
def values(i,uid,pin):return [r['name'] for p in node(i,uid)['pins'] if p['pin']==pin for r in p['references']]
def peers(i,uid,pin):return [q for p in node(i,uid)['pins'] if p['pin']==pin for q in p['peers']]
# Native control directions/thresholds and writer overlap are critical repair boundaries.
for uid,gate,a,b in [('1935','Sub','Data.PC_01','Coeff.SET_PC01'),('1945','Ge','App02','5'),('1948','Lt','Data.FN_04_ASPIRATOR','250'),('1957','Le','App02','-1'),('1960','Gt','Data.SET_PERC_FN04','20'),('1951','Add','1','Data.SET_PERC_FN04'),('1963','Add','-1','Data.SET_PERC_FN04')]:
    assert node(1901,uid)['gate']==gate and values(1901,uid,'in1')==[a] and values(1901,uid,'in2')==[b]
assert values(1901,'1970','value')==['S5T#4S']
assert values(1689,'844','in1')==['Data.SET_PERC_FN04'] and values(1689,'844','in2')==['272'] and values(1689,'844','out')==['FN04_SP']
assert values(1688,'640','in1')==['Data.Set_Perc_VT02'] and values(1688,'640','in2')==['272'] and values(1688,'640','out')==['FN02_SP']
assert values(1705,'256','in1')==['Data.PSH03_SETPOINT'] and values(1705,'256','in2')==['Data.PSH03']
assert values(1705,'279','operand')==['PID down MV03'] and values(1705,'285','operand')==['PID UP MV03']
assert values(15,'507','QLMNUP')==['PID UP MV03'] and values(15,'507','QLMNDN')==['PID down MV03']
# en wire must actually come from the OFF contact; UID is independent of ORef UID.
off_src=next(q for q in peers(15,'507','en') if q['kind']=='PCon' and q['pin']=='out')
assert values(15,off_src['uid'],'operand')==['OFF']
for i,uid,sp,pv in [(5,'109','Real_SPO2','Real_O2'),(7,'172','Real_SPPC01','Real_PC01'),(11,'366','Real_SP_TC03xMV01','Real_TC03xMV01'),(15,'507','Real_SPPC02','Real_PC02'),(1832,'663','SetPoint_Stechio','Stechio_attuale')]:
    assert values(i,uid,'SP_INT')==[sp] and values(i,uid,'PV_IN')==[pv] and values(i,uid,'CYCLE')==['T#100MS']
    # No RefId is retained as unknown; it must not be replaced with a default.
    assert any(r['ref_id'] is None and r['name'] is None for p in node(i,uid)['pins'] for r in p['references'])
assert values(11,'366','GAIN')==['3.0'] and values(7,'172','GAIN')==['-0.22']
assert values(1710,'701','in1')==['PSH02'] and values(1710,'715','in1')==['PSH02']
assert values(1709,'598','in1')==['Data.PSH02_SETPOINT'] and values(1709,'598','in2')==['Data.PSH_02']
live={(r['segment'],r['i']):r for r in load('sources/live_index.json') if not r['deleted']}
assert [(t['segment'],t['id']) for t in d['indexed_texts']]==[('_7ex',4),('_7ex',6),('_7ex',9),('_7ex',10),('_7ex',13),('_7ex',14),('_7ev',1719),('_7ev',1720),('_7ev',1831),('_7ev',1833)]
blocks=load('sources/block_summary.json')
for t in d['indexed_texts']:
    row=live[t['segment'],t['id']];assert row['values'][t['language']]==t['text']
    assert hashlib.sha256(t['text'].encode()).hexdigest()==t['text_sha256']
    b=next(b for b in blocks if b['name']==t['block']);n=next(n for n in b['networks'] if n['segment']==t['segment'] and n['doc']==t['id'])
    assert n[t['language']]==t['text'] and t['evidence']=='backup_search_index_text_not_compiled_or_native_instruction_listing'
textmap={t['id']:t['text'] for t in d['indexed_texts']}
assert 'l -15 //meno 30°c' in textmap[9] and '// l "data".temp_t6' in textmap[10]
assert 'l "data".press_pc01' in textmap[6] and 't #real_pc01' in textmap[6]
assert '"allarm".emergencystoptc1_2 := "manage_tc1_2".emergencystop;' in textmap[1719]
assert 'call cont_c , "pid-burner"' in textmap[1720] and 'lmn_llm :=5.0' in textmap[1720]
trace=load('registers/signal-trace.json')['usages'];pins=0;others=0
expected_selectors=[]
for p in d['native']:
    for uid in p['refs']:
        for u in trace:
            if u['network']==p['id'] and u['oref']==uid and u['scope'] in ['Global','Local'] and u['name']:
                identity=(u['name'],u['scope'],u['block'] if u['scope']=='Local' else None)
                if identity not in expected_selectors:expected_selectors.append(identity)
assert [(s['name'],s['scope'],s['block']) for s in d['signals']]==expected_selectors
for s in d['signals']:
    same=lambda u:canon(u['name'])==canon(s['name']) and u['scope']==s['scope'] and (s['scope']!='Local' or u['block']==s['block'])
    assert s['usages']==[u for u in trace if same(u)]
    assert s['other_scope_usages']==[u for u in trace if canon(u['name'])==canon(s['name']) and not same(u)]
    pins+=len(s['usages']);others+=len(s['other_scope_usages'])
assert [l['id'] for l in d['loops']]==['FN04','MV01','MV02','MV03','MV05','MV06','VT02','BR01','STECHIO']
hmi=list(csv.DictReader((ROOT/'registers/equipment-hmi.csv').open(encoding='utf-8-sig')))
for l in d['loops']:
    assert not l['field_verified'] and l['plc_changes']==0 and len(l['repair'])==4 and len(l['pending'])==3
    assert l['text_refs']==[t for t in d['indexed_texts'] if t['id'] in l['texts']]
    assert l['hmi_reference_rows']==[r for r in hmi if r['설비 ID'] in l['equipment']]
    if l['controller']:
        i,uid=l['controller'];assert l['controller_evidence']==dict(network=i,**node(i,uid))
htmltext=(ROOT/'regulation-manual.html').read_text()
for l in d['loops']:assert 'id="loop-'+l['id']+'"' in htmltext
for t in d['indexed_texts']:assert html.escape(t['text']) in htmltext
for p in d['native']:
    for w in p['wires']:assert 'id="wire-'+str(p['id'])+'-'+w['uid']+'"' in htmltext
for f,h in load('registers/simulator-freeze.json')['files'].items():assert sha(f)==h
# These references must be present in generated integration files.
for key,id_ in [('P02','FN04'),('P19','MV01'),('P20','MV03'),('P21','MV06'),('P16','VT02'),('P11','BR01')]:
    assert 'regulation-manual.html#loop-'+id_ in (ROOT/'repair-guides'/f'{key}.html').read_text()
forms=load('registers/repair-record-forms.json')
for p in forms['profiles']:
    assert p['evidence_plan']['sources']['registers/regulation-manual.json']==sha('registers/regulation-manual.json')
for key in ['P02','P19','P20','P21','P16','P11']:
    assert 'regulation-manual.html#loop-' in json.dumps(next(p for p in forms['profiles'] if p['key']==key))
result=dict(status='passed',date='2026-10-08',loops=9,native_networks=33,indexed_text_records=10,native_pid_calls=5,symptom_guidance_rows=36,signal_scopes=len(d['signals']),signal_pin_references=pins,other_scope_references=others,source_hashes_checked=len(d['sources']),regulation_manual_sha256=sha('registers/regulation-manual.json'),field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun',simulator_files_hashes_unchanged=True,scope='Native LAD and exact backup index text, not current TIA compilation or PLC execution',**dict(counts))
report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
