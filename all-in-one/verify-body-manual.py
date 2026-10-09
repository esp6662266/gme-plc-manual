"""Compare body evidence and critical alarms with preserved native files; never evaluate PLC logic."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote,parse_qs
from functools import cache
from collections import Counter
import csv,hashlib,json,re,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent
sha=lambda f:hashlib.sha256((R/f).read_bytes()).hexdigest()
load=lambda f:json.loads((R/f).read_text())
tag=lambda x:x.tag.rsplit('}',1)[-1]
decode=lambda s:re.sub(r'_x([0-9a-fA-F]{4})_',lambda m:chr(int(m[1],16)),str(s))
report=R/'body-manual-verification.json';report.write_text(json.dumps(dict(status='checking',scope='Original static evidence; no execution'))+'\n')
b=load('registers/body-manual.json');counts=b['counts'];total=Counter()
for f,h in b['sources'].items():assert sha(f)==h,f
for f,h in load('registers/simulator-freeze.json')['files'].items():assert sha(f)==h,f
assert not b['field_verified'] and not b['tia_verified'] and b['plc_changes']==b['current_values_written']==b['direct_io_assignments']==0
assert b['simulator_development']=='stopped_by_user' and b['simulator_behavior_tests']=='not_rerun'
assert [p['id'] for p in b['profiles']]==['CC01','AB01','HE01']
specs={s['id']:s for s in load('registers/control-spec.json')['specifications']}
for p in b['profiles']:
    assert not p['identity_verified'] and not p['field_verified'] and not p['tia_verified']
    assert p['direct_spec_counts']=={k:len(specs[p['id']][k]) for k in ['inputs','outputs','hmi','networks','direct_rules']}
    assert specs[p['id']]['kind']=='passive' and not specs[p['id']]['outputs'] and not specs[p['id']]['networks']
    assert len(p['symptoms'])==4 and all(not s['field_verified'] and not s['repair_completed'] for s in p['symptoms'])
    assert all(not s['ownership_verified'] for s in p['sensor_references'])
assert [p['direct_spec_counts']['inputs'] for p in b['profiles']]==[0,2,0]
assert [n['id'] for n in b['native']]==sorted({i for p in b['profiles'] for i in p['network_ids']})
@cache
def xml(f):return ET.parse(R/f).getroot()
proof={}
for n in b['native']:
    assert sha(n['file'])==n['sha256'] and n['reference_only'] and not n['ownership_verified']
    root=xml(n['file']);v=n['evidence'];proof[n['id']]=v
    parts=[dict(uid=x.get('UId'),gate=x.get('Gate'),attributes=dict(x.attrib),negated=[dict(c.attrib) for c in x if tag(c)=='Negated'],templates=[dict(attributes=dict(c.attrib),value=c.text) for c in x if tag(c)=='TemplateValue']) for x in root.iter() if tag(x)=='Part']
    wires=[dict(uid=x.get('UId'),endpoints=[dict(kind=tag(c),attributes=dict(c.attrib)) for c in x]) for x in root.iter() if tag(x)=='Wire']
    assert v['parts']==parts and v['wires']==wires
    def tree(x):return dict(tag=tag(x),attributes=dict(x.attrib),text=x.text,children=[tree(c) for c in x])
    assert v['call_nodes']==[tree(x) for x in root.iter() if tag(x) in ['CRef','LRef']]
    actualrefs={x.get('UId'):x for x in root.iter() if tag(x)=='ORef'}
    assert set(v['references'])==set(actualrefs)
    for uid,r in v['references'].items():
        assert r['uid']==uid and r['rid']==actualrefs[uid].get('RefId') and r['nid']==v['inferred_nid']
        for d in r['declarations']:
            matches=[]
            for entry in xml('sources/decoded-original/'+d['file']):
                ident=next((x for x in entry if tag(x)=='ID'),None)
                if ident is None or ident.get('RID')!=r['rid']:continue
                occurrences=[x for x in ident.iter() if tag(x)=='C' and x.get('UID')==uid and x.get('NID')==r['nid']]
                if not occurrences:continue
                constants=[dict(x.attrib) for x in entry.iter() if tag(x)=='CB']
                name=decode(ident.get('N','')) or '.'.join(decode(x.get('N')) for x in entry.iter() if tag(x)=='AO' and x.get('N'))
                if not name and constants:name=decode(constants[0].get('SV',constants[0].get('V','')))
                matches.append((name,ident.get('S'),dict(occurrences[0].attrib),[dict(x.attrib) for x in entry.iter() if tag(x)=='TD'],constants))
            assert (r['name'],d['scope'],d['occurrence'],d['types'],d['constants']) in matches,(n['id'],uid,d)
        assert r['unresolved']==(r['name'] is None or not r['declarations'])
        total['native_declarations']+=len(r['declarations']);total['unresolved_refs']+=r['unresolved']
    assert (n['native_parts'],n['native_wires'],n['native_orefs'])==(len(parts),len(wires),len(actualrefs))
    total.update(native_parts=len(parts),native_wires=len(wires),native_orefs=len(actualrefs))
# Critical AB01 pins are checked against the native wires and the independently matched declarations above.
def pin(i,uid,pin):
    return [proof[i]['references'][e['attributes']['UId']]['name'] for w in proof[i]['wires'] if any(e['kind']=='PCon' and e['attributes'].get('UId')==uid and e['attributes'].get('PinName')==pin for e in w['endpoints']) for e in w['endpoints'] if e['kind']=='OCon']
def node(i,uid):return next(p for p in proof[i]['parts'] if p['uid']==uid)
def connected(i,wire,*endpoints):
    w=next(w for w in proof[i]['wires'] if w['uid']==wire)
    got={(e['kind'],e['attributes'].get('UId'),e['attributes'].get('PinName')) for e in w['endpoints']}
    assert set(endpoints)<=got,(i,wire,got)
assert pin(1979,'149','in1')==['Manage_TC1_2.PID_Ref_Temp'] and pin(1979,'149','in2')==['Data.TC01_MAX_ALL']
assert pin(1979,'165','in1')==['Data.TC01_MAX_ALL'] and pin(1979,'165','in2')==['5']
assert pin(1979,'179','in2')==['20']
assert pin(1979,'189','in2')==['1250.0'] and pin(1979,'192','in2')==['-60.0']
connected(1979,'255',('PCon','165','eno'),('PCon','169','pre'))
connected(1979,'287',('PCon','179','en'),('PCon','186','pre'),('PCon','189','pre'),('PCon','192','pre'))
assert node(1986,'834')['negated']==[{'PinName':'operand'}]
assert pin(1986,'745','in2')==pin(1986,'748','in2')==['400']
assert pin(1986,'761','in2')==['-100'] and pin(1986,'764','in2')==['100']
connected(1986,'809',('PCon','754','en'),('PCon','761','pre'),('PCon','764','pre'))
for i,part,value in [(1979,'155','S5T#6S'),(1979,'198','S5T#6S'),(1986,'770','S5T#1M')]:
    assert node(i,part)['gate']=='SdCoil' and pin(i,part,'value')==[value]
    uid=next(e['attributes']['UId'] for w in proof[i]['wires'] if any(e['kind']=='PCon' and e['attributes'].get('UId')==part and e['attributes'].get('PinName')=='value' for e in w['endpoints']) for e in w['endpoints'] if e['kind']=='OCon')
    assert any(c.get('T')=='S5Time' and decode(c.get('SV'))==value for d in proof[i]['references'][uid]['declarations'] for c in d['constants'])
assert node(1856,'162')['negated']==node(1856,'164')['negated']==[{'PinName':'operand'}]
assert node(1866,'636')['negated']==[{'PinName':'operand'}]
assert pin(1866,'611','operand')==['Rem. Start/Stop Burner']
assert len(b['alarm_paths'])==3 and [a['id'] for a in b['alarm_paths']]==['AB01-AL01','AB01-AL02','AB01-AL03']
# Analyst source snapshots are preserved; edited draft snapshots are intentionally historical.
analyst=load(b['alarm_investigation'])
for s in analyst['sources']:
    if s['file'].startswith('sources/'):assert sha(s['file'])==s['sha256']
for fact in analyst['core_facts']:
    if fact['network'] not in proof:continue
    for key in ['set_parts','parts']:
        for uid in fact.get(key,[]):assert uid in {x['uid'] for x in proof[fact['network']]['parts']}
    for key in ['set_wires','reset_wires','wires']:
        for uid in fact.get(key,[]):assert uid in {x['uid'] for x in proof[fact['network']]['wires']}
assert analyst['static_verification']['scl_1719_exact_register_match']
assert 'tc01_ofr' in next(f for f in analyst['core_facts'] if f['id']=='AB01-SCL01')['exact_text']
# No masked construction rows, no automatic source conflict resolution, no observation values.
selected={(r['page'],r['id']) for r in b['cable_rows']};masked={(r['page'],r['id']) for r in b['masked_cable_rows_excluded']}
assert len(selected)==32 and not selected&masked
byrow={r['id']:r for r in b['cable_rows']}
assert byrow['3_3']['description']==byrow['3_30']['description']=='LS01–08 / LS32/33 / PB15 / PB18'
assert (byrow['3_3']['cable'],byrow['3_30']['cable'])==('CVV 25G','CVV 12G')
assert byrow['14_17']['description']==byrow['14_18']['description']==''
assert all('=ENT+CC01-BR01F' in byrow[x]['note'] for x in ['14_17','14_18'])
assert all(not r['current_wiring_verified'] for r in b['cable_rows'])
assert b['counts']['body_checks_pending']==7 and b['counts']['body_checks_excluded']==1
assert [c['id'] for c in b['checks'] if c['excluded_from_current_analysis']]==['BODY-07']
assert {n['id'] for n in b['equipment_status_notes']}==({'MV04','SC12','PV04','P22','P23'} | ({'EV'+str(i).zfill(2) for i in range(1,91)} & {v['id'] for v in json.loads((R/'registers/control-spec.json').read_text())['specifications']}))
assert all(n['exclude_from_current_detailed_analysis'] and n['source_kind']=='user_statement' and not n['field_verified'] and n['historical_sources_preserved'] for n in b['equipment_status_notes'])
assert b['equipment_status_notes'][0]['id']=='MV04' and b['equipment_status_notes'][0]['status']=='removed_user_reported' and b['equipment_status_notes'][0]['exclude_from_current_detailed_analysis'] and not b['equipment_status_notes'][0]['field_verified']
assert len(b['checks'])==8 and all(not r['resolved'] and not r['field_verified'] for r in b['checks'])
with (R/'registers/simulation-tests.csv').open(encoding='utf-8-sig') as f:tests=list(csv.DictReader(f))
with (R/'registers/verification.csv').open(encoding='utf-8-sig') as f:checks=list(csv.DictReader(f))
assert len(tests)==577 and all(t['상태']=='설계·미실행' for t in tests) and len(checks)==1060
assert load('registers/evidence-review.json')['counts']['source']==18
crop=load('registers/body-pid-render-verification.json');assert crop['status']=='passed'
assert crop['all_pixels_equal_fresh_pdf_render'] and crop['pdf_sha256']==sha(crop['pdf']) and crop['reference_sha256']==sha(crop['reference'])
assert {c['id'] for c in crop['crops']}=={'CC01','AB01','HE01'}
for c in crop['crops']:assert c['pixels_equal_source_region'] and c['sha256']==sha(c['file'])
review=load(b['independent_review'])
assert review['ab01_original_review']['confirmed_errors']==0 and review['ab01_original_review']['original_xml_and_uid_rid_nid_matched']
assert len(review['parent_integration']['fixes'])==4 and review['parent_integration']['original_conflicts_closed']==0
for f,h in review['source_hashes'].items():assert sha(f)==h
# Link and anchor checks, including supported app routes returning to the same priority equipment.
class Tags(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.refs=[]
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if t in ['a','link'] and 'href' in a:self.refs.append(a['href'])
        if t in ['img','script'] and 'src' in a:self.refs.append(a['src'])
@cache
def html(f):
    p=Tags();p.feed((R/f).read_text());return p
page=html('body-manual.html')
assert {'cables','checks','native','alarms-AB01','selection-AB01'}|{q+p['id'] for p in b['profiles'] for q in ['body-','flow-','symptoms-']}|{s['id'] for p in b['profiles'] for s in p['symptoms']}|{c['id'] for c in b['checks']}<=page.ids
for path in page.refs:
    u=urlsplit(path);f=unquote(u.path) or 'body-manual.html';assert (R/f).is_file(),path
    if u.fragment and f.endswith('.html'):
        if f=='index.html' and '=' in u.fragment:
            q=parse_qs(u.fragment);assert q['view']==['repair-record'] and q['equipment'][0] in ['P10','P12','P13']
        else:assert unquote(u.fragment) in html(f).ids,path
text=(R/'body-manual.html').read_text()
assert 'PB15–18' not in text and 'TC02 단독 분기에서도 원문은 TC01_OFR' in text and 'Sub.eno → Real Lt' in text
for p in b['profiles']:
    for f in ['procedures/'+p['id']+'.html','repair-guides/'+p['priority']+'.html']:
        assert 'body-manual.html#body-'+p['id'] in (R/f).read_text()
    form=next(x for x in load('registers/repair-record-forms.json')['profiles'] if x['key']==p['priority'])
    assert not form['signals'] and not form['identity_confirmed'] and not form['field_verified']
    assert form['evidence_plan']['sources']['registers/body-manual.json']==sha('registers/body-manual.json')
    links=[r['path'] for s in form['evidence_plan']['steps'] for r in s['source_links'] if r['path'].startswith('body-manual.html')]
    assert links==['body-manual.html#flow-'+p['id'],'body-manual.html#symptoms-'+p['id'],'body-manual.html#body-'+p['id']]
for k in ['native_parts','native_wires','native_orefs','native_declarations']:assert counts[k]==total[k]
assert (counts['profiles'],counts['symptom_cases'],counts['native_networks'],counts['selected_visible_cable_rows'])==(3,12,34,32)
result=dict(status='passed',date='2026-10-09',body_manual_sha256=sha('registers/body-manual.json'),html_sha256=sha('body-manual.html'),source_hashes_checked=len(b['sources']),local_links_checked=len(page.refs),native_networks=34,**dict(total),critical_ab01_native_pins_checked=True,body_form_links_checked=9,counts=counts,field_verified=False,tia_verified=False,plc_changes=0,simulator_files_unchanged=True,simulator_behavior_tests='not_rerun',scope='Static originals and documentation; reviewer snapshots and browser observations are separately recorded')
report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
