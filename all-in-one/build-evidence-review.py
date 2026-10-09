"""Read-only review hub: keep source queues distinct and link repair evidence.

Relationships indicate review/reference scope, never installed-device identity.
User annotations live separately in the browser, not in these source registers.
"""
from pathlib import Path
from collections import Counter
import csv, hashlib, html, json

ROOT=Path(__file__).resolve().parent
app=json.loads((ROOT/'registers/all-in-one-data.json').read_text())
repair=json.loads((ROOT/'registers/repair-decision.json').read_text())
common=json.loads((ROOT/'registers/common-control.json').read_text())
construction=json.loads((ROOT/'registers/construction-review.json').read_text())
improvement=json.loads((ROOT/'registers/improvement-review.json').read_text())
conflicts=list(csv.DictReader((ROOT/'registers/source-conflict-review.csv').open(encoding='utf-8-sig')))
model=json.loads((ROOT/'registers/program-model.json').read_text())
signal=json.loads((ROOT/'registers/signal-trace.json').read_text())
global_refs={(r['network'],r['oref']) for r in signal['usages'] if r['scope']=='Global'}
nets={n['id']:n for n in model['networks']}
ids={d['id'] for d in app['equipment']}
priority=app['priority']
source_files=['registers/source-conflict-review.csv','registers/construction-review.json',
              'registers/common-control.json','registers/improvement-review.json',
              'registers/repair-decision.json','registers/priority-equipment.csv','registers/signal-trace.json']
e=lambda x:html.escape(str(x))
canon=lambda s:str(s).replace('"','').casefold()
rows=[]

def make(kind, source_id, title, observation, next_check, equipment, source, raw,
         source_status, networks=(), links=(), global_scope=False, priority_key=None):
    declared=list(dict.fromkeys(equipment))
    mapped=[x for x in declared if x in ids]
    network_list=list(dict.fromkeys(networks))
    # A named reference in a native network establishes a review relationship,
    # not ownership of that signal or identity of an installed unit.
    related=[]
    matches=[]
    for r in repair['records']:
        if not r['plc_id'] or r['plc_id'] in mapped:continue
        names={canon(b['name']) for b in r['bindings']}
        hit=[dict(network=n,oref=u,name=v['name']) for n in network_list
             for u,v in nets[n]['refs'].items() if (n,u) in global_refs and v.get('name') and canon(v['name']) in names]
        if hit:
            related.append(r['plc_id'])
            matches.append(dict(equipment=r['plc_id'],basis='exact native name reference',refs=hit))
    review_keys=[p['key'] for p in priority if p['plc_id'] and p['plc_id'] in mapped+related]
    if priority_key:review_keys=list(dict.fromkeys([priority_key]+review_keys))
    sources=[dict(label=label,path=path) for label,path in links]
    sources += [dict(label='원본 '+str(n),path='networks/network-'+str(n)+'.html') for n in network_list]
    rows.append(dict(id=kind+':'+source_id,kind=kind,source_id=source_id,title=title,
        observation=observation,next_check=next_check,equipment_ids=mapped,declared_scope=declared,
        unmapped_scope=[x for x in declared if x not in ids],related_equipment_ids=related,
        relationship_evidence=matches,priority_keys=review_keys,global_scope=global_scope,
        source_file=source,source_status=source_status,raw=raw,networks=network_list,links=sources,
        identity_verified=False,field_verified=False,resolved=False))

for r in conflicts:
    make('source',r['ID'],r['항목'],r['자료 내용'],r['다음 검증'],
         [] if r['관련 범위']=='전체 공통' else [x.strip() for x in r['관련 범위'].split(',')],
         'registers/source-conflict-review.csv',r,r['해소 상태'],
         links=[('원본 불일치 대장','registers/source-conflict-review.csv')],
         global_scope=r['관련 범위']=='전체 공통')
for r in construction['items']:
    make('construction',r['id'],'시공 자료 '+r['id'],r['observation'],r['validation'],r['equipment'],
         'registers/construction-review.json',r,r['status'],
         links=[('시공 참조 작업지','construction-guide.html')]+
               [('추가 시공도면 PDF '+str(p),construction['source']+'#page='+str(p)) for p in r['pages']])
common_equipment={'COM-08':['BC01'],'COM-09':['BR01','FN03','MV03'],
                  'COM-10':['FN02','FN03','MC05','BR01']}
for r in common['checks']:
    make('common',r['id'],r['title'],r['work'],r['work'],common_equipment.get(r['id'],[]),
         'registers/common-control.json',r,r['status'],networks=r['networks'],
         links=[('공통 확인 목록','common-control.html#checks')],global_scope=r['id'] not in common_equipment)
for r in improvement['items']:
    make('improvement',r['id'],r['equipment']+' · 원본 구조 개선 검토',r['observation'],r['validation'],
         r['equipment'].split('·'),'registers/improvement-review.json',r,r['status'],
         networks=r['networks'],links=[('개선 후보 전체 목록','improvement-review.html'),('개별 영향·대안·확인','improvement-guides/'+r['id']+'.html')])
for p in priority:
    status={'tag':'태그명 일치 / 실물 확인 전','candidate':'공정 역할 대응 후보 / 실물 확인 전','unknown':'PLC 대응 미확정'}[p['match']]
    make('identity',p['key'],p['name']+' · 동일성·제어 경계',
         status+(' · '+p['note'] if p['note'] else ''),
         '명판·실물 설비ID·위치·본체/구동부·제어반/전용 제어기·P&ID 연결과 현재 I/O를 대조합니다. 태그 일치나 역할 후보만으로 실물 동일성을 확정하지 않습니다.',
         [p['plc_id']] if p['plc_id'] else [],'registers/priority-equipment.csv',p,status,
         links=[('실물 대응 작업지','priority-guides/'+p['key']+'.html'),
                ('수리 판단 작업지','repair-guides/'+p['key']+'.html')],priority_key=p['key'])

counts=dict(Counter(r['kind'] for r in rows))
assert counts==dict(source=18,construction=7,common=10,improvement=6,identity=23)
assert len({r['id'] for r in rows})==64
record=dict(date='2026-10-08',scope='source review and repair navigation; browser annotations separate',
    counts=counts,items=rows,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source_files},
    original_pending_register_count=1060,design_tests_preserved=577,field_verified=0,
    plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun')
(ROOT/'registers/evidence-review.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
with (ROOT/'registers/evidence-review.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=['id','kind','source_id','title','source_status','equipment_ids','related_equipment_ids','priority_keys','global_scope','observation','next_check','source_file'])
    writer.writeheader();writer.writerows({k:(' / '.join(v) if isinstance(v,list) else v) for k,v in r.items() if k in writer.fieldnames} for r in rows)
labels={'source':'원본 불일치','construction':'시공 검토','common':'공통 확인','improvement':'개선 후보','identity':'설비 동일성'}
body='<h1>근거 검토·확인 통합 목록</h1><div class="notice">원본 불일치18·시공 검토7·공통 확인10·개선 후보6·설비 동일성23개를 종류별로 유지합니다. 원본 확인 대장1060건과 시험 설계577건은 별도 대장입니다. 실물·현장 확인·원인 해소·PLC 변경을 완료로 확정한 항목은 없습니다. 시뮬레이터 작성·시험 중지.</div><p>올인원에서는 종류·선택 설비·검색으로 찾고 근거와 수리 작업지로 이동하며 항목별 메모를 기록할 수 있습니다. 신호 참조 연관은 실제 설비 동일성·전용 소유를 뜻하지 않습니다.</p>'
body+='<div class="table-wrap"><table><thead><tr><th>종류·ID</th><th>관찰·자료 내용</th><th>다음 확인</th><th>범위·근거</th></tr></thead><tbody>'
for r in rows:
    scope=('전체 공통 자료' if r['global_scope'] else ' / '.join(r['declared_scope']) or '설비 식별 전')
    refs='<br>'.join('<a href="'+e(x['path'])+'">'+e(x['label'])+'</a>' for x in r['links'])
    repairs='<br>'.join('<a href="repair-guides/'+p+'.html">'+e(p)+' 수리 판단</a>' for p in r['priority_keys'])
    body+='<tr id="review-'+e(r['kind']+'-'+r['source_id'])+'"><td>'+e(labels[r['kind']]+' / '+r['source_id'])+'<br>'+e(r['source_status'])+'</td><td><strong>'+e(r['title'])+'</strong><br>'+e(r['observation'])+'</td><td>'+e(r['next_check'])+'</td><td>'+e(scope)+('<br>신호 참조 연관: '+e(' / '.join(r['related_equipment_ids'])) if r['related_equipment_ids'] else '')+'<br>'+refs+'<br>'+repairs+'</td></tr>'
body+='</tbody></table></div><p><a href="registers/evidence-review.json">통합 검토 JSON</a> · <a href="registers/evidence-review.csv">통합 검토 CSV</a></p>'
page='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>근거 검토·확인 통합 목록</title><link rel="stylesheet" href="assets/all-in-one.css"><style>td{overflow-wrap:anywhere}td:last-child{min-width:180px}</style></head><body><main style="max-width:1240px;margin:auto;padding:24px">'+body+'</main></body></html>'
(ROOT/'evidence-review.html').write_text(page)
print(json.dumps(dict(review_items=len(rows),counts=counts,source_registers_unchanged=True,field_verified=0),ensure_ascii=False))
