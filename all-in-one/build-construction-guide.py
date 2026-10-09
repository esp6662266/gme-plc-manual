"""Complement OEM functional circuits with a reviewed construction reference.
No original PLC, source PDF, simulator, or source-conflict records are modified.
"""
from pathlib import Path
import csv, hashlib, html, json, re, runpy, shutil
ROOT=Path(__file__).resolve().parent
detail=runpy.run_path(str(ROOT/'construction-source-details.py'))
SOURCE=detail['SOURCE'];POWER=detail['POWER'];CONTROL=detail['CONTROL']
REVIEWS=detail['REVIEWS'];MASKED=detail['MASKED'];PROFILES=detail['PROFILES']
assert hashlib.sha256((ROOT/SOURCE).read_bytes()).hexdigest()==detail['SHA256']
texts=json.loads((ROOT/'sources/can-decoating-page-text.json').read_text())
assert len(texts)==64
data=json.loads((ROOT/'registers/all-in-one-data.json').read_text())
specs={s['id']:s for s in data['equipment']}
assert all(id in specs for id in PROFILES)
out=ROOT/'construction-guides';out.mkdir(exist_ok=True)
images=ROOT/'assets/construction';images.mkdir(exist_ok=True)
for pg in [3,6,21,24,48,51,52,53,55,56,57,58,59,64]:
    image=ROOT.parent.parent/'tmp/pdfs/gme-construction'/f'P{pg:02}.png'
    if image.exists():shutil.copy2(image,images/f'P{pg:02}.png')
e=lambda v:html.escape(str(v))
def dump(path,v):path.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def link(pg,prefix=''):
    return '<a href="'+prefix+SOURCE+'#page='+str(pg)+'">새 시공도면 · PDF '+str(pg)+'</a>'
def table(headers,rows):
    return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+v+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def page(title,body,prefix=''):
    return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+'</title><link rel="stylesheet" href="'+prefix+'assets/all-in-one.css"></head><body><main style="max-width:1240px;margin:auto;padding:24px"><h1>'+e(title)+'</h1>'+body+'</main></body></html>'
def source_notice():
    return '<div class="notice info">64페이지 전기 시공도면을 기존 OEM Rev.2 회로도·PLC 백업의 보완 근거로 사용합니다. 표지 FOR APPROVAL, 개정란 24.11.11 first draft design. 승인·준공·실제 설치·현재 배선은 확인 전입니다. PLC 주소와 실제 단자 핀은 이 자료만으로 확정하지 않습니다.</div>'
def row_table(rows,prefix=''):
    return table(['근거·행','케이블 식별자','FROM → TO','종류·규격 원문','경로·LEN 원문 / 검토'],[[link(r['page'],prefix)+'<br>'+e(r['row']),'<code>'+e(r['cable'])+'</code>',e(r['from_']+' → '+r['to']),e(' / '.join([r['current_type'],r['spec'],r['core'],r['size']]))+('<br>SPARE '+e(r['spare']) if r['spare'] is not None else ''),e(' → '.join(r.get('route',[])))+(' · LEN '+e(r['len_original']) if 'len_original' in r else '')+'<p>'+e(r['note'])+'</p>'] for r in rows])
def review_table(items,prefix=''):
    return table(['검토·근거','도면 관찰','영향','확인 작업·상태'],[[e(r['id']+' / '+', '.join(r['equipment']))+'<br>'+ ' · '.join(link(p,prefix) for p in r['pages'])+'<br>'+e(', '.join(r['rows'])),e(r['observation']),e(r['impact']),e(r['validation'])+'<br><strong>확인 대기 · 현장 미확인</strong>'] for r in items])
def previews(pages,prefix=''):
    return ''.join('<details><summary>시공도면 PDF '+str(p)+' · 원본 페이지 보기</summary><a href="'+prefix+SOURCE+'#page='+str(p)+'"><img class="source-image" src="'+prefix+'assets/construction/P'+str(p).zfill(2)+'.png" alt="Can-Decoating 시공도면 원본 PDF '+str(p)+'페이지" loading="lazy"></a></details>' for p in pages if (images/f'P{p:02}.png').exists())

sections=[(1,2,'표지·목차'),(3,6,'구역·모터·센서·접속함 배치'),(7,17,'공통 및 공정별 케이블 경로'),(18,20,'배관도 읽기·트레이 단면'),(21,23,'ENTRY 배관'),(24,25,'ROTARY 배관'),(26,30,'FLOW A 배관'),(31,33,'FLOW B 배관'),(34,34,'EXIT 배관'),(35,48,'DUST 배관'),(49,50,'케이블 목록 읽기'),(51,64,'케이블 목록 · D-PAGE 1–14')]
page_index=[]
for t in texts:
    pg=t['page'];match=re.search(r'CANDC-CONS-[A-Z]\d{3}-\d{3}',t['text'])
    title=re.findall(r'Can-Decoating ([^\r\n]+)',t['text'])
    page_index.append(dict(page=pg,drawing_code=match.group(0) if match else '',title_original=title[-1] if title else '',section=next(s for a,b,s in sections if a<=pg<=b),visual_review=pg in detail['VISUAL_PAGES'],example_only=pg in [19,50],masked_rows=MASKED.get(pg,[])))
profiles=[]
for id,(pages,boundary) in PROFILES.items():
    powers=[r for r in POWER if r['equipment']==id];controls=[r for r in CONTROL if r['equipment']==id];reviews=[r for r in REVIEWS if id in r['equipment']]
    body=source_notice()+'<p><strong>추적 경계:</strong> '+e(boundary)+'</p><nav class="inline-actions"><a href="../construction-guide.html">시공도면 전체 색인·검토</a><a href="../procedures/'+e(id)+'.html">진단·수리 작업지</a><a href="../control-specs/'+e(id)+'.html">PLC 제어 명세</a>'
    if (ROOT/'circuit-guides'/(id+'.html')).exists():body+='<a href="../circuit-guides/'+e(id)+'.html">OEM 단자·릴레이 경로</a>'
    body+='</nav><h2>1. 관련 원본 페이지</h2><p>'+' · '.join(link(p,'../') for p in pages)+'</p><p>아래 자료는 시각 확인한 선택 행입니다. 전체 케이블·단자·I/O 목록의 완성이나 현장 수리 완료를 뜻하지 않습니다.</p>'
    body+='<h2>2. 모터 동력 간선 · 선택 행</h2>'+(row_table(powers,'../') if powers else '<p>이 항목의 동력 케이블은 선택 기록에 없습니다. 본체·센서·공유 접속함을 모터로 대신 지정하지 않습니다.</p>')
    body+='<h2>3. 접속함·센서·밸브 · 선택 행</h2>'+(row_table(controls,'../') if controls else '<p>제어 케이블의 개별 행·단자 경로는 추가 검토가 필요합니다. 관련 PDF와 OEM 회로도를 함께 확인합니다.</p>')
    if reviews:body+='<h2>4. 새 시공도면의 확인 대기</h2>'+review_table(reviews,'../')
    body+='<h2>현장 수리 기록 순서</h2><ol><li>현재 승인 도면·설비 명판·양단 케이블 표찰·접속함 ID를 대조합니다.</li><li>도면별 페이지·행·전체 식별자·FROM/TO를 기록합니다. No. 또는 이름만으로 연결하지 않습니다.</li><li>기존 OEM 회로에서 반·단자·접점·릴레이·장치 핀·PLC 주소를 찾아 구간별 전달을 확인합니다.</li><li>PLC 원본의 입력 전달·출력 조건·알람·Reset·복수 쓰기를 수리 작업지와 함께 확인합니다.</li><li>관찰값·최초 불일치 구간·조치·복구·주변 공정 영향을 기록하고 승인된 절차로 확인합니다.</li></ol><p>케이블 종류·심수·SIZE·SPARE·LEN은 도면 원문입니다. LEN을 실측 거리로, G/C/S/SB를 검증된 배선 사양으로 환산하지 않습니다. 가려진 행은 배선 근거에서 제외합니다.</p>'
    body+='<h2>원본 페이지 시각 확인</h2>'+previews([p for p in pages if p>=21],'../')
    (out/(id+'.html')).write_text(page(id+' · 시공 배선·케이블 참조',body,'../'))
    profiles.append(dict(id=id,pages=pages,boundary=boundary,power_rows=len(powers),control_rows=len(controls),review_ids=[r['id'] for r in reviews],guide='construction-guides/'+id+'.html',field_verified=False))

priority_rows=[]
for p in data['priority']:
    id=p['plc_id'];profile=next((x for x in profiles if x['id']==id),None)
    priority_rows.append(dict(key=p['key'],name=p['name'],plc_id=id,match=p['match'],identity_verified=False,guide=profile['guide'] if profile else '',pages=profile['pages'] if profile else [],status='태그 기준 참고 · 실물 대응 미확인' if p['match']=='tag' else '본체 대응 후보 · 실물 미확인' if p['match']=='candidate' else 'PLC 대응 미확정 · 자동 연결 없음'))
record=dict(source=SOURCE,source_name='Can-Decoating_20241118.pdf',sha256=detail['SHA256'],bytes=(ROOT/SOURCE).stat().st_size,pages=64,source_role='construction layout/conduit/cable schedule complement to OEM functional circuits',filename_date='2024-11-18',titleblock_revision='24.11.11 first draft design',cover_status='FOR APPROVAL',pdf_metadata_date='2024-11-19 18:00:21 +09:00',approved_as_built_verified=False,field_verified=0,plc_changes=0,simulator_changes=0,visually_reviewed_pages=detail['VISUAL_PAGES'],power_rows=len(POWER),control_rows=len(CONTROL),equipment_guides=len(profiles),new_review_items=len(REVIEWS),original_conflicts_preserved=18,masked_rows=[dict(page=p,rows=rows,status='visually masked; excluded from operative cable records') for p,rows in MASKED.items()],masked_rows_known=sum(len(rows) for rows in MASKED.values()),masked_review_complete=False,profiles=profiles,priority=priority_rows)
dump(ROOT/'registers/construction-reference.json',record)
dump(ROOT/'registers/construction-page-index.json',page_index)
dump(ROOT/'registers/construction-power-cables.json',POWER)
dump(ROOT/'registers/construction-control-cables.json',CONTROL)
dump(ROOT/'registers/construction-review.json',dict(source=SOURCE,items=REVIEWS,resolved=0,field_verified=0,original_conflicts_preserved=18))
with (ROOT/'registers/construction-cables.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['구분','설비','PDF페이지','행','케이블 식별자','FROM','TO','CURRENT TYPE 원문','SPEC 원문','CORE 원문','SIZE 원문','SPARE 원문','경로 원문','LEN 원문','검토','상태'])
    for kind,rows in [('power',POWER),('control',CONTROL)]:
        for r in rows:w.writerow([kind,r['equipment'],r['page'],r['row'],r['cable'],r['from_'],r['to'],r['current_type'],r['spec'],r['core'],r['size'],r['spare'],' → '.join(r.get('route',[])),r.get('len_original',''),r['note'],'도면 선택 행 시각 확인 / 현장 미확인'])

body=source_notice()+'<nav class="inline-actions"><a href="'+SOURCE+'#page=1">새 전기 시공도면 원본 · 64페이지</a><a href="sources/Electrical_Rev2.pdf#page=1">기존 OEM Rev.2 회로도 · 265페이지</a><a href="electrical-trace.html">OEM 단자·릴레이 회로 추적</a><a href="registers/construction-cables.csv">선택 케이블 CSV</a><a href="registers/construction-reference.json">참조·승인 상태 JSON</a></nav>'
body+='<h2>자료의 역할과 확인 범위</h2><p>새 시공도면은 설비 위치 → 접속함 → 배관·트레이 → 케이블 양단·규격의 추적에 사용합니다. 기존 OEM 회로도는 장치 핀·접점·릴레이·PLC 주소를, 백업 LAD는 운전 조건·타이머·알람·리셋을 확인하는 근거입니다. 서로 다른 개정과 자료 범위이므로 어느 하나를 현재 현장 전체의 확정본으로 대체하지 않습니다.</p><p>원본 64페이지 중 '+str(len(detail['VISUAL_PAGES']))+'페이지를 시각 확인했습니다. 선택 동력 '+str(len(POWER))+'행·제어 '+str(len(CONTROL))+'행, '+str(len(profiles))+'개 참조 작업지를 연결했습니다. 승인·준공·실물 대응·배선·정상 극성은 미확인입니다.</p><p>파일명의 20241118, 개정란의 24.11.11, PDF 메타데이터의 2024-11-19는 각각 보존합니다. 작성일만으로 기존 Rev.2보다 유효한 최종 도면이라고 판단하지 않습니다.</p>'
body+='<h2>우선 23개 · 현재 대응 상태 유지</h2>'+table(['우선·배치도','PLC 참고','시공도면 작업지','상태'],[[e(p['key']+' · '+p['name']),e(p['plc_id'] or '미확정'),'<a href="'+p['guide']+'">케이블·배관 추적</a>' if p['guide'] else '대응 미확정 · 추가 식별 필요',e(p['status'])] for p in priority_rows])
body+='<h2>보조 설비를 별도로 추적</h2><nav class="inline-actions">'+''.join('<a href="construction-guides/'+id+'.html">'+e(id)+'</a>' for id in ['RD01-FAN','FN01-FAN','EV03','SC01'])+'</nav><h2>새 시공도면 확인 대기 · '+str(len(REVIEWS))+'건</h2><p>아래 목록은 이번 시공도면의 별도 검토 항목입니다. 기존 18개 불일치의 상태를 해소하거나 덮어쓰지 않습니다.</p>'+review_table(REVIEWS)
body+='<h2>가려진 행 · 배선 근거에서 제외</h2><p>시각 확인한 페이지에서 검은 가림 '+str(record['masked_rows_known'])+'행을 확인했습니다. 텍스트 추출에는 해당 행이 남아 있어도 사용 케이블로 채택하지 않습니다. 이 수치는 확인한 페이지 범위의 발견 수이며 모든 행의 가림 검토 완료를 뜻하지 않습니다.</p>'+table(['원본 페이지','가림 행','처리'],[[link(p),e(', '.join(rows)),'선택 배선·동작 모델·I/O 근거에서 제외'] for p,rows in MASKED.items()])
body+='<h2>읽는 방법</h2><ol><li>PDF19·50은 설명 예시입니다. 예시 케이블의 LEN·장치 표기를 실제 목록 값으로 쓰지 않습니다.</li><li>51–64페이지의 D-PAGE는 1–14입니다. No. 1_1은 PDF1페이지를 의미하지 않습니다.</li><li>전체 케이블 식별자 =INS+LOC-TAG, FROM/TO, CURRENT TYPE, SPEC/CORE/SIZE/SPARE, 경로 열1–7, LEN을 함께 봅니다.</li><li>케이블 식별자가 중복될 수 있습니다. PDF페이지+행을 기록 키로 사용하며 실물·접속함·단자를 확인하기 전 자동 병합하지 않습니다.</li><li>삭제 표기·가림·SPARE·공유 접속함을 실제 운전 조건이나 설치 확정으로 해석하지 않습니다.</li></ol>'+link(19)+' · '+link(50)
body+='<h2>64페이지 전체 색인</h2>'+table(['PDF','도면번호 원문','구역·종류','시각 확인·주의'],[[link(x['page']),'<code>'+e(x['drawing_code'])+'</code>',e(x['section']),e(('시각 확인' if x['visual_review'] else '텍스트 색인 · 세부 시각 확인 전')+(' / 설명 예시' if x['example_only'] else '')+(' / 가림 행 제외: '+', '.join(x['masked_rows']) if x['masked_rows'] else ''))] for x in page_index])
body+='<h2>주요 원본 페이지 보기</h2>'+previews([3,6,51,52,53,55])
(ROOT/'construction-guide.html').write_text(page('시공도면 참조 · 배치·접속함·케이블 추적',body))
print(json.dumps({k:record[k] for k in ['pages','power_rows','control_rows','equipment_guides','new_review_items','masked_rows_known','field_verified','simulator_changes']},ensure_ascii=False))
