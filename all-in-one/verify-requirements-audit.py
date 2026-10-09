"""Independently check coverage against preserved specs and actual document sections."""
from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
import csv,hashlib,json
from functools import cache
ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
@cache
def load(p):return json.loads((ROOT/p).read_text())
a=load('registers/requirements-audit.json')
assert a['overall_completion_proven'] is False
assert a['field_verified'] is False and a['tia_verified'] is False
assert a['simulator_development']=='stopped_by_user' and a['simulator_behavior_tests']=='not_rerun'
for p,h in a['inputs'].items():assert sha(ROOT/p)==h,p
assert not any(p in a['inputs'] for p in ['index.html','registers/all-in-one-data.json','requirements-audit.html','operator-guide.html','all-in-one-verification.json'])
for p,h in load('registers/simulator-freeze.json')['files'].items():assert sha(ROOT/p)==h,p
spec={s['id']:s for s in load('registers/control-spec.json')['specifications']}
rows={r['id']:r for r in a['equipment']}
assert len(rows)==248 and set(rows)==set(spec)
class Tags(HTMLParser):
    def __init__(self):super().__init__();self.ids=set()
    def handle_starttag(self,t,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.add(d['id'])
@cache
def ids(p):
    parser=Tags();parser.feed((ROOT/p).read_text());return parser.ids
symptoms=set()
for ident,r in rows.items():
    s=spec[ident]
    assert (r['name'],r['kind'],r['parent'],r['group'])==(s['name'],s['kind'],s['parent'],s['group'])
    for field in ['inputs','outputs','hmi','networks','pending']:assert r[field]==len(s[field]),(ident,field)
    assert r['direct_paths']==len(s['direct_rules'])
    assert r['field_verified'] is False and r['tia_verified'] is False
    assert r['next_task']
    for d in r['base_documents']+r['specialist']:
        parts=d['path'].split('#');assert (ROOT/parts[0]).is_file(),d
        if len(parts)==2:assert parts[1] in ids(parts[0]),d
    if '3. 원본에서 확인한 핵심 동작' in (ROOT/'procedures'/f'{ident}.html').read_text():symptoms.add(ident)
    assert r['detail_level']==('symptom' if r['symptom_detail'] else 'specialist' if r['specialist'] else 'baseline')
assert symptoms=={r['id'] for r in rows.values() if r['symptom_detail']}==set(load('registers/diagnostic-coverage.json')['detailed_devices'])
# Check explicit specialist membership independently, including every documented regulation relation.
for ident,r in rows.items():
    expected=[]
    if ident in {c['id'] for c in load('registers/sensor-measurement.json')['channels']}:expected.append('sensor-measurement.html#sensor-'+ident)
    if ident in {c['id'] for c in load('registers/encoder-position.json')['channels']}:expected.append('encoder-position.html#position-'+ident)
    expected+=['regulation-manual.html#loop-'+l['id'] for l in load('registers/regulation-manual.json')['loops'] if ident in l['equipment']]
    if ident in {p['id'] for p in load('registers/alarm-recovery.json')['profiles']}:expected.append('alarm-guides/'+ident+'.html')
    if ident in {d['id'] for d in load('registers/electrical-trace.json')['devices']}:expected.append('circuit-guides/'+ident+'.html')
    if ident in {p['id'] for p in load('registers/body-manual.json')['profiles']}:expected.append('body-manual.html#body-'+ident)
    assert [d['path'] for d in r['specialist']]==expected,ident
with (ROOT/'registers/priority-equipment.csv').open(encoding='utf-8-sig') as f:priority=list(csv.DictReader(f))
assert len(a['priority'])==len(priority)==23
for original,current in zip(priority,a['priority']):
    for field in ['key','name','plc_id','match','sejin_id']:assert original[field]==current[field]
    assert current['identity_verified'] is False
    assert current['detail_level']==(rows[current['plc_id']]['detail_level'] if current['plc_id'] else 'identity_unresolved')
assert Counter(p['match'] for p in priority)=={'tag':14,'candidate':4,'unknown':5}
c=a['counts'];levels=Counter(r['detail_level'] for r in rows.values())
assert [c[k] for k in ['equipment','base_manuals','base_specs','base_procedures']]==[248]*4
assert (c['representative_symptom_devices'],c['specialist_only_devices'],c['baseline_only_devices'])==(levels['symptom'],levels['specialist'],levels['baseline'])==(15,28,205)
assert c['current_priority']==21 and c['other_process_excluded']==2 and c['retired_equipment_excluded']==1 and c['absent_equipment_excluded']==1
assert c['manual_deferred_equipment_excluded']==87 and c['current_equipment_detail_scope']==21 and c['eligible_history_equipment']==158
assert c['eligible_history_baseline_devices']==sum(r['detail_level']=='baseline' and not r['lifecycle_note'] for r in rows.values())
for i in range(1,91):
    ident='EV'+str(i).zfill(2)
    if ident in rows:assert rows[ident]['lifecycle_note']['status']=='manual_deferred_user_reported' and rows[ident]['lifecycle_note']['resume_requires_user_request']
assert c['not_planned_equipment_excluded']==1
assert rows['PV04']['lifecycle_note']['exclude_from_current_detailed_analysis'] and rows['PV04']['lifecycle_note']['status']=='not_planned_user_reported'
assert rows['SC12']['lifecycle_note']['exclude_from_current_detailed_analysis'] and not rows['SC12']['field_verified']
assert rows['MV04']['lifecycle_note']['exclude_from_current_detailed_analysis'] and not rows['MV04']['field_verified']
assert (c['body_source_devices'],c['body_symptom_cases'])==(3,12)
assert (c['with_io'],c['with_hmi'],c['with_direct_paths'])==(207,65,148)
assert [c[k] for k in ['priority','priority_referenced_equipment','priority_unknown','tests_designed','tests_executed','pending_checks','source_conflicts','review_items','field_verified','tia_verified']]==[23,18,5,577,0,1060,18,64,0,0]
with (ROOT/'registers/requirements-audit.csv').open(encoding='utf-8-sig') as f:csvrows=list(csv.DictReader(f))
assert len(csvrows)==248
for cr,r in zip(csvrows,a['equipment']):
    for k,v in cr.items():assert v==str(r[k]),(r['id'],k)
anchors=ids('requirements-audit.html')
work=a['priority_open_work']
assert [r['key'] for r in work]==['P'+str(i).zfill(2) for i in range(1,22)]
assert Counter(r['lane'] for r in work)=={'BC01 단독 표준화':1,'현행 자료·관찰 보강':13,'식별 자료 우선':3,'본체·계측·제작사 자료':3,'전용 버너 자료·현행 연동':1}
assert work[0]['lane']=='BC01 단독 표준화' and 'BC01 표준 매뉴얼' in work[0]['document_work']
assert all('다른 설비 확대 보류' in r['document_work'] for r in work[1:])
assert {'priority-open-work'}|{'open-'+r['key'] for r in work}<=anchors
identity={r['key']:r for r in load('registers/unresolved-identity.json')['profiles']}
alarms={r['id']:r for r in load('registers/alarm-recovery.json')['profiles']}
checks={r['id']:r for r in load('registers/body-manual.json')['checks']}
reviews={r['id']:r for r in load('registers/evidence-review.json')['items']}
for r,p in zip(work,a['priority'][:21]):
    assert (r['key'],r['name'],r['plc_id'],r['match'])==(p['key'],p['name'],p['plc_id'],p['match'])
    assert not r['identity_verified'] and not r['field_verified'] and not r['tia_verified'] and r['repairs_completed']==0
    assert all(r[k] for k in ['document_work','additional_materials','field_work','completion_criterion'])
    assert r['existing_pending']==(spec[r['plc_id']]['pending'] if r['plc_id'] else [])
    for d in r['existing_documents']:
        path,_,anchor=d['path'].partition('#')
        assert (ROOT/path).is_file()
        if anchor:assert anchor in ids(path),(r['key'],d)
    for ref in r['evidence_references']:assert ref['path'] in a['inputs']
    if not r['plc_id']:
        assert r['additional_materials']==identity[r['key']]['needed']
        assert r['boundary']==identity[r['key']]['excluded']
        assert not identity[r['key']]['assigned_signals']
    if r['plc_id'] in alarms:assert alarms[r['plc_id']]['note'] in r['existing_notes']
    expected_checks={k for k,v in checks.items() if r['plc_id'] in v['equipment'] and not v['excluded_from_current_analysis']}
    assert {v['id'] for v in r['body_checks']}==expected_checks
    for v in r['body_checks']:assert v==checks[v['id']] and v['id']!='BODY-07' and not v['resolved']
    for v in r['existing_review']:
        assert all(value==reviews[v['id']][field] for field,value in v.items()) and r['key'] in v['priority_keys'] and not v['resolved']
        assert not any(ex in v['title']+' '+v['source_id'] for ex in ['MV04','SC12','PV04'])
        assert 'review-'+v['id'].replace(':','-') in ids('evidence-review.html')
assert '완료한 AB01' in next(r for r in work if r['plc_id']=='AB01')['document_work']
assert {'equipment-'+i for i in rows}|{'priority-'+p['key'] for p in priority}|{'R'+str(i).zfill(2) for i in range(1,15)}<=anchors
assert {'bc01-standard','start','repair','structure','records','pending','limits','install'}<=ids('operator-guide.html')
for text in ['가져오기·병합·서버 동기화는 없습니다','프로그램 ZIP에 브라우저 기록이 자동 포함되지 않습니다','577개 시험은 설계·미실행']:
    assert text in (ROOT/'operator-guide.html').read_text(),text
result=dict(status='passed',requirements_audit_sha256=sha(ROOT/'registers/requirements-audit.json'),audit_html_sha256=sha(ROOT/'requirements-audit.html'),operator_guide_sha256=sha(ROOT/'operator-guide.html'),source_hashes_checked=len(a['inputs']),equipment_checked=248,priority_checked=23,detail_depth=c,simulator_files_unchanged=True,simulator_behavior_tests='not_rerun',field_verified=False,tia_verified=False,scope='static document coverage; browser observations separate')
result['current_priority_open_work_checked']=len(work)
(ROOT/'requirements-audit-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='detail_depth'},ensure_ascii=False))
