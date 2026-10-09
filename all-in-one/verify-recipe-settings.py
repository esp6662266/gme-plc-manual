"""Independent native XML and exact index-text integrity audit. No execution."""
from pathlib import Path
import csv,hashlib,html,json,xml.etree.ElementTree as ET
from collections import Counter
ROOT=Path(__file__).resolve().parent
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
tag=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s or '').replace('"','').casefold()
report=ROOT/'recipe-settings-verification.json';report.write_text(json.dumps(dict(status='checking',scope='Native and index-text integrity; no execution'))+'\n')
d=load('registers/recipe-settings.json');m=load('registers/program-model.json');ns={n['id']:n for n in m['networks']};decls=load('sources/decoded-original/identifier-declarations.json');mp={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
targets=['Data.SET_PERC_BWF01','Data.SET_PERC_BWF02','Data.SET_PERC_FR01','Data.SET_PERC_VT01','Data.PSH01_SETPOINT','Data.PSH02_SETPOINT','Data.TC03_SETPOINT','Data.TC01_SETPOINT']
trace=load('registers/signal-trace.json')['usages']
writers={u['network'] for u in trace if u['scope']=='Global' and canon(u['name']) in {canon(t) for t in targets} and u['role']=='write' and not u['legacy_simulation_block']}
expected=sorted(writers|{402,403,404,405,1613,1723,1841,1621})
assert d['writer_network_ids']==sorted(writers)
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
import re
readcsv=lambda f:list(csv.DictReader((ROOT/f).open(encoding='utf-8-sig',newline='')))
hmi=readcsv('sources/hmi_plc_tags.csv');priority=readcsv('registers/priority-equipment.csv');blocks=load('sources/block_summary.json');live={(x['segment'],x['i']):x for x in load('sources/live_index.json') if not x['deleted']}
code=live['_7ev',364]['values']['SCL Code']
assert d['recipe_source']==dict(segment='_7ev',id=364,block='recipes handler',text=code,sha256=hashlib.sha256(code.encode()).hexdigest())
assert len(d['claims'])==9 and len({x['key'] for x in d['claims']})==9
for x in d['claims']:
 start,end=x['source_span'];assert code[start:end]==x['excerpt'] and x['status']=='static_index_reading_not_execution'
assert code.count('#differing')==1 and code.index('#differing')<code.index('elsif not #in_range')
assert 'and #in_range' not in d['claims'][7]['excerpt'] and d['claims'][7]['key']=='load'
fields=['bwf01','bwf02','rd01','fn01','psh01','psh02','tc03','tc01'];names=['Editor_BWF01','Editor_BWF02','Editor_RD01','Editor_FN01','Editor_PSH01','Editor_PSH02','Editor_TC03','Editor_TC01']
source_assignments=[m for m in re.finditer(r'"data"\.([a-z0-9_]+) := "recipesdb"\.recipes\[0\]\.([a-z0-9_]+);',code,re.I)]
assert len(source_assignments)==8
for x,f,t,hn,a in zip(d['load_fields'],fields,targets,names,source_assignments):
 assert x['field']==f and x['target']==t and canon('Data.'+a[1])==canon(t) and a[2]==f
 assert x['assignment']==dict(target='Data.'+a[1],field=f,source_span=[a.start(),a.end()],source_text=a.group())
 assert x['hmi']==[r for r in hmi if r['HMI 태그']==hn]
 assert not x['screen_mapping_verified'] and not x['current_write_owner_verified']
 assert x['usages']==[u for u in trace if u['scope']=='Global' and canon(u['name'])==canon(t)]
 assert x['other_scope_usages']==[u for u in trace if u['scope']!='Global' and canon(u['name'])==canon(t)]
 for u in x['usages']+x['other_scope_usages']:assert d['sources'][u['file']]==sha(u['file'])
control_names={'HMI_Index','Editor_Active_Recipe','Editor_Vis_SaveUndo','Editor_Vis_Modify','Editor_Vis_LoadRecipe','Editor_Load_Recipe','Editor_Save_Recipe','Editor_Modify_Recipe','Editor_Undo_Modification'}
assert d['hmi_controls']==[r for r in hmi if r['HMI 태그'] in control_names]
expected_texts=[]
for b in blocks:
 for entry in b['networks']:
  values=live[entry['segment'],entry['doc']]['values']
  for key in ['SCL Code','STL Code']:
   txt=values.get(key)
   if txt and (entry['doc']==401 or re.search(r'"data"\.(?:set_perc_bwf0[12]|set_perc_fr01|set_perc_vt01|psh0[12]_setpoint|tc0[13]_setpoint)\b',txt,re.I)):
    expected_texts.append(dict(block=b['name'],block_properties=b['properties'],segment=entry['segment'],id=entry['doc'],kind=key,text=txt,values=values,sha256=hashlib.sha256(txt.encode()).hexdigest(),status='exact_backup_index_text_not_current_compiled_source'))
assert d['indexed_texts']==expected_texts
assert [x['id'] for x in d['startup']]==list(range(401,406))
for x in d['startup']:assert x['values']==live['_7ev',x['id']]['values'] and x['native_available']==(x['id']!=401)
assert all(r['name'] is None for i in [402,403] for n in ps[i]['nodes'] if n['gate']=='Move' for pin in n['pins'] if pin['pin'] in ['in','out1'] for r in pin['references'])
assert [p['key'] for p in d['profiles']]==[p['key'] for p in priority] and len(d['profiles'])==23
for p,src in zip(d['profiles'],priority):assert p['name']==src['name'] and p['plc_id']==src['plc_id'] and not p['identity_verified']
ht=(ROOT/'recipe-settings.html').read_text()
for p in d['profiles']:assert 'id="profile-'+p['key']+'"' in ht
for p in d['native']:
 for w in p['wires']:assert 'id="wire-'+str(p['id'])+'-'+w['uid']+'"' in ht
for x in d['load_fields']:assert 'id="field-'+x['field']+'"' in ht and html.escape(x['assignment']['source_text']) in ht
for x in d['indexed_texts']:assert html.escape(x['text']) in ht
for f,h in load('registers/simulator-freeze.json')['files'].items():assert sha(f)==h
forms=load('registers/repair-record-forms.json')
for p in forms['profiles']:
 assert p['evidence_plan']['sources']['registers/recipe-settings.json']==sha('registers/recipe-settings.json')
 assert 'recipe-settings.html#profile-'+p['key'] in json.dumps(p)
 assert 'recipe-settings.html#profile-'+p['key'] in (ROOT/'repair-guides'/f"{p['key']}.html").read_text()
expected_counts=dict(recipe_load_fields=8,hmi_control_tags=9,hmi_editor_tags=8,native_networks=20,indexed_text_records=7,recipe_claims=9,symptoms=8,priority_profiles=23)
assert d['counts']==expected_counts
result=dict(status='passed',date='2026-10-08',**expected_counts,writer_networks=len(writers),source_hashes_checked=len(d['sources']),recipe_settings_sha256=sha('registers/recipe-settings.json'),field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun',simulator_files_hashes_unchanged=True,scope='Exact index text, native setting-write and startup source integrity; no SCL/PLC execution',**dict(counts))
report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
