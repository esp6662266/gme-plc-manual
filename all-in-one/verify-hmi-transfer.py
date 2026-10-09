"""Independent native XML and exact index-text integrity audit. No execution."""
from pathlib import Path
import csv,hashlib,html,json,xml.etree.ElementTree as ET
from collections import Counter
ROOT=Path(__file__).resolve().parent
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
tag=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s or '').replace('"','').casefold()
report=ROOT/'hmi-transfer-verification.json';report.write_text(json.dumps(dict(status='checking',scope='Native and index-text integrity; no execution'))+'\n')
d=load('registers/hmi-transfer.json');m=load('registers/program-model.json');ns={n['id']:n for n in m['networks']};decls=load('sources/decoded-original/identifier-declarations.json');mp={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
groups=['hmi','hmi inputs','hmi output','hmi standard motors','hmi standard motorized valve','hmi pv_1gate','hmi pv_2gate']
expected=sorted(n['id'] for n in m['networks'] if n['block'] in groups)
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
import re,zipfile
from collections import defaultdict
readcsv=lambda f:list(csv.DictReader((ROOT/f).open(encoding='utf-8-sig',newline='')))
tags=readcsv('sources/hmi_plc_tags.csv');windows=readcsv('sources/hmi-windows.csv');assigned=readcsv('registers/equipment-hmi.csv');symbols=readcsv('registers/plc-symbols.csv');priority=readcsv('registers/priority-equipment.csv');equipment_networks=readcsv('registers/equipment-networks.csv');trace=load('registers/signal-trace.json')['usages']
assert len(tags)==782 and len(windows)==17 and len(expected)==47 and len(priority)==23
assert [a['source'] for a in d['tags']]==tags and d['windows']==windows
assert [a['index'] for a in d['tags']]==list(range(782))
assert len({a['anchor'] for a in d['tags']})==782
def hmi_span(s):
 # Independent notation parser; no DB member alignment or current settings assumed.
 if s.startswith('DB'):
  head,tail=s.split(',');area='DB'+str(int(head[2:]));kind=next(k for k in ['INT','REAL','X','W','D'] if tail.startswith(k));num=tail[len(kind):]
  if kind=='X':
   byte,bit=map(int,num.split('.'));assert 0<=bit<8;return area,byte*8+bit,byte*8+bit+1,'db',kind
  width=16 if kind in ['INT','W'] else 32;start=int(num)*8;return area,start,start+width,'db',kind
 if s.startswith(('EB','EW','AB','AW')):
  start=int(s[2:])*8;return ('I' if s[0]=='E' else 'Q'),start,start+(8 if s[1]=='B' else 16),'physical',s[:2]
 if s.startswith('MX'):
  byte,bit=map(int,s[2:].split('.'));assert 0<=bit<8;return 'M',byte*8+bit,byte*8+bit+1,'memory','MX'
 assert s=='$SYS$Status';return None
def symbol_span(s):
 match=re.fullmatch(r'%([IQM])(?:(\d+)\.([0-7])|([BWD])(\d+))',s.upper())
 if not match:return None
 area,byte,bit,kind,offset=match.groups()
 if byte is not None:start=int(byte)*8+int(bit);return area,start,start+1
 start=int(offset)*8;return area,start,start+{'B':8,'W':16,'D':32}[kind]
def crosses(a,b):return a[0]==b[0] and a[1]<b[2] and b[1]<a[2]
source_paths={'registers/program-model.json','registers/signal-trace.json','sources/live_index.json','sources/block_summary.json','sources/decoded-original/network-map.json','sources/decoded-original/identifier-declarations.json','registers/plc-symbols.csv','registers/equipment-hmi.csv','sources/hmi_plc_tags.csv','sources/hmi-windows.csv','registers/hmi-window-provenance.json','registers/equipment-networks.csv','registers/priority-equipment.csv'}
for a,row in zip(d['tags'],tags):
 assert a['anchor']=='tag-'+row['태그 내부 ID'] and not a['current_mapping_verified'] and not a['screen_read_write_verified']
 span=hmi_span(row['설정 주소']);parsed=a['parsed']
 if span:
  assert (parsed['area'],parsed['start_bit'],parsed['end_bit'],parsed['kind'],parsed['notation'])==span
  assert parsed['width_bits']==span[2]-span[1] and parsed['access']==row['Access Name']
  if span[3]=='db':assert parsed['plc_member_offset_verified'] is False
 else:assert parsed['kind']=='driver_status'
 expected_eq=[x['설비 ID'] for x in assigned if (x['HMI 태그'],x['설정 주소'],x['Access Name'],x['내부 ID'])==(row['HMI 태그'],row['설정 주소'],row['Access Name'],row['태그 내부 ID'])]
 assert a['existing_equipment_references']==expected_eq
 sy=[]
 if span and span[3] in ['physical','memory']:
  for s in symbols:
   sp=symbol_span(s['백업 주소'])
   if sp and crosses(span,sp):
    uses=[u for u in trace if u['scope']=='Global' and canon(u['name'])==canon(s['원본 심볼'])]
    sy.append(dict(symbol=s,relation='same_span_candidate' if span[:3]==sp else 'overlapping_span_candidate',usages=uses));source_paths.update(u['file'] for u in uses)
 assert a['physical_symbol_candidates']==sy
same=defaultdict(list)
for i,row in enumerate(tags):same[row['Access Name'],row['설정 주소']].append(i)
assert d['shared_addresses']==[dict(access=k[0],address=k[1],tag_indices=v,status='shared_configuration_address_not_confirmed_error') for k,v in same.items() if len(v)>1]
assert [(g['address'],[tags[i]['HMI 태그'] for i in g['tag_indices']]) for g in d['shared_addresses']]==[('DB14,W20',['I_W20','O_W20']),('DB14,W22',['I_W22','O_W22'])]
pairs=[]
for i,a in enumerate(tags):
 sa=hmi_span(a['설정 주소'])
 if not sa:continue
 for j,b in enumerate(tags[i+1:],i+1):
  sb=hmi_span(b['설정 주소'])
  if sb and a['Access Name']==b['Access Name'] and crosses(sa,sb):pairs.append(dict(a=i,b=j,relation='same_span' if sa[:3]==sb[:3] else 'overlapping_span',status='configuration_range_comparison_not_confirmed_error'))
assert d['address_overlaps']==pairs and len(pairs)==17
assert [p['key'] for p in d['profiles']]==[p['key'] for p in priority]
for p,original in zip(d['profiles'],priority):
 assert p['name']==original['name'] and p['plc_id']==original['plc_id'] and p['identity_verified'] is False and p['field_verified'] is False
 assert p['tag_indices']==[a['index'] for a in d['tags'] if p['plc_id'] and p['plc_id'] in a['existing_equipment_references']]
 assert p['existing_native_reference_rows']==([x for x in equipment_networks if x['설비 ID']==p['plc_id'] and int(x['문서 ID']) in expected] if p['plc_id'] else [])
 if not p['plc_id']:assert p['tag_indices']==[] and p['existing_native_reference_rows']==[]
blocks=load('sources/block_summary.json');live={(x['segment'],x['i']):x for x in load('sources/live_index.json') if not x['deleted']}
expected_titles=[dict(segment=n['segment'],id=n['doc'],values=live[n['segment'],n['doc']]['values'],status='index_title_only_no_native_LAD') for b in blocks if b['name']=='hmi' for n in b['networks'] if n['doc'] not in expected]
assert d['title_only_networks']==expected_titles and [x['id'] for x in expected_titles]==[1183,1185,1200]
selectors=[]
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
 same_scope=lambda u:canon(u['name'])==canon(s['name']) and u['scope']==s['scope'] and (s['scope']!='Local' or u['block']==s['block'])
 assert s['usages']==[u for u in trace if same_scope(u)] and s['other_scope_usages']==[u for u in trace if canon(u['name'])==canon(s['name']) and not same_scope(u)]
 source_paths.update(u['file'] for u in s['usages']+s['other_scope_usages'])
assert d['sources']=={p:sha(p) for p in sorted(source_paths)}
prov=load('registers/hmi-window-provenance.json');assert d['window_provenance']==prov and prov['window_csv_sha256']==sha('sources/hmi-windows.csv') and prov['tag_csv_sha256']==sha('sources/hmi_plc_tags.csv') and prov['tag_csv_matches_preserved_source'] and not prov['current_hmi_verified']
# The original, previously retrieved archive is available on this authoring host.
archive=Path('/private/tmp/gme-upload-review-20261007.zip');archive_rechecked=False
if archive.exists():
 assert hashlib.sha256(archive.read_bytes()).hexdigest()==prov['export_archive_sha256']
 with zipfile.ZipFile(archive) as z:
  assert z.read(prov['window_archive_entry'])==(ROOT/'sources/hmi-windows.csv').read_bytes()
  assert z.read(prov['tag_archive_entry'])==(ROOT/'sources/hmi_plc_tags.csv').read_bytes()
 archive_rechecked=True
expected_counts=dict(tags=782,windows=17,native_networks=47,priority_profiles=23,shared_address_groups=2,overlapping_tag_pairs=17,address_kinds={'db':678,'memory':2,'physical':101,'driver_status':1},symbol_candidate_tags=100,same_span_candidate_tags=58,title_only_networks=3)
assert d['counts']==expected_counts
for f,h in load('registers/simulator-freeze.json')['files'].items():assert sha(f)==h
ht=(ROOT/'hmi-transfer.html').read_text()
for a in d['tags']:assert 'id="'+a['anchor']+'"' in ht and html.escape(a['source']['HMI 태그']) in ht
for p in d['profiles']:assert 'id="profile-'+p['key']+'"' in ht
for p in d['native']:
 for w in p['wires']:assert 'id="wire-'+str(p['id'])+'-'+w['uid']+'"' in ht
forms=load('registers/repair-record-forms.json')
for p in forms['profiles']:
 assert p['evidence_plan']['sources']['registers/hmi-transfer.json']==sha('registers/hmi-transfer.json')
 assert 'hmi-transfer.html#profile-'+p['key'] in json.dumps(p)
 assert 'hmi-transfer.html#profile-'+p['key'] in (ROOT/'repair-guides'/f"{p['key']}.html").read_text()
result=dict(status='passed',date='2026-10-08',**expected_counts,native_calls=sum(n['kind'] in ['LRef','CRef'] for p in d['native'] for n in p['nodes']),signal_scopes=len(d['signals']),signal_pin_references=sum(len(s['usages']) for s in d['signals']),other_scope_references=sum(len(s['other_scope_usages']) for s in d['signals']),source_hashes_checked=len(d['sources']),hmi_transfer_sha256=sha('registers/hmi-transfer.json'),export_archive_rechecked=archive_rechecked,field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun',simulator_files_hashes_unchanged=True,scope='CSV metadata, notation range candidates and native interface evidence; not current screen events or DB member layout',**dict(counts))
report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
