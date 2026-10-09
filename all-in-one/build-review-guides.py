"""Priority identity worksheets and source-backed improvement review queue."""
from pathlib import Path
import csv,json,html

ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'registers/all-in-one-data.json').read_text())
e=lambda x:html.escape(str(x))
def page(title,body,prefix=''):
    return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+'</title><link rel="stylesheet" href="'+prefix+'assets/all-in-one.css"></head><body><main style="max-width:1240px;margin:auto;padding:24px"><h1>'+e(title)+'</h1>'+body+'</main></body></html>'
def table(headers,rows):
    return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'

guides=ROOT/'priority-guides';guides.mkdir(exist_ok=True)
for p in data['priority']:
    status={'tag':'태그명 일치 / 실물 확인 전','candidate':'공정 역할 대응 후보 / 실물 확인 전','unknown':'PLC 대응 미확정'}[p['match']]
    body='<div class="notice">'+e(status)+' · '+e(p['note'] or '배치도 명칭, 실물 설비 ID, 제어반·입출력·도면의 대응을 확인합니다.')+'</div><p>우선 설비 '+e(p['key'])+' · 배치도: 디코팅 시안 · 확인 기준일 2026-10-07</p>'
    if p['plc_id']:body+='<p>참고 PLC 자료: <strong>'+e(p['plc_id'])+'</strong></p><nav class="inline-actions"><a href="../procedures/'+e(p['plc_id'])+'.html">원본 근거 기반 진단·수리 작업지</a><a href="../control-specs/'+e(p['plc_id'])+'.html">입출력·동작·이상 처리 명세</a></nav>'
    else:body+='<p>현재 GME 자료에서 이 설비와 직접 대응하는 태그를 식별하지 못했습니다. 다른 번호·설비의 프로그램을 대신 연결하지 않습니다.</p>'
    if p['plc_id'] and (ROOT/'circuit-guides'/(p['plc_id']+'.html')).exists():body+='<p><a href="../circuit-guides/'+e(p['plc_id'])+'.html">도면 시각 확인 · 전기 회로 추적</a></p>'
    if p['plc_id'] and (ROOT/'construction-guides'/(p['plc_id']+'.html')).exists():body+='<p><a href="../construction-guides/'+e(p['plc_id'])+'.html">추가 시공도면 · 케이블·접속함·배관 추적</a> · 승인·실물·현재 설치는 확인 전</p>'
    if (ROOT/'common-guides'/(p['key']+'.html')).exists():body+='<p><a href="../common-guides/'+p['key']+'.html">공통 제어·자동 요청·정지·복구 확인</a></p>'
    if (ROOT/'repair-guides'/(p['key']+'.html')).exists():body+='<p><a href="../repair-guides/'+p['key']+'.html">수리 판단·공통 영향 통합 작업지</a></p>'
    body+='<h2>실물과 제어 주체 확인</h2>'+table(['확인 항목','현재 상태','기록할 근거'],[
        ('설비 ID·명판',p['sejin_id'] or '미확인','설비 카드 ID / 명판·관리번호 / 설치 위치'),
        ('본체·구동부 관계','미확인','본체와 모터·감속기·팬·댐퍼를 별도로 확인'),
        ('제어반·PLC·전용 제어기','미확인','반 명칭 / CPU / 전용 제어기 / 통신 또는 접점 연동'),
        ('P&ID의 입출 연결','미확인','투입·배출 / 가스·공기 / 위치·방향 / 도면 태그'),
        ('입출력 주소·단자','미확인','현재 백업 주소 / FG·PDF 페이지 / 현장 단자·배선'),
        ('운전 허가·정지 연동','미확인','상위·하위 설비 / 요청·Ready·Run·Fault / 접점 정상 극성'),
        ('실제 운전·고장 이력','미확인','발생 시각 / 증상 / 조치 / 사진 / 재기동 결과')])
    body+='<h2>증상 조사 순서</h2><ol><li>실물 설비와 제어 주체를 먼저 확인하고 어느 프로그램·도면의 범위인지 표시합니다.</li><li>운전 요청, 준비 허가, 실제 운전 응답과 고장 신호를 구분해 최초 이상을 기록합니다.</li><li>기계적 증상과 PLC의 후속 정지를 분리하고 센서·단자·내부 신호의 전달 구간을 확인합니다.</li><li>원인·조치·리셋·재기동과 주변 공정 영향을 근거 위치와 함께 기록합니다.</li></ol><h2>추가할 자료</h2><p>명판·제어반 사진, 전용 전기도면, 제작사 매뉴얼, 실제 I/O 또는 통신 목록, 정비 이력과 승인된 운전 순서가 필요합니다. 장치 정격·센서 정상 극성·인터록을 임의로 확정하지 않습니다.</p><p><a href="'+e(data['priority_source']['url'])+'" target="_blank" rel="noopener">SEJIN 원본 배치도</a> · <a href="../ACTIVE-WORK.md">현재 작업 범위</a></p>'
    (guides/(p['key']+'.html')).write_text(page(p['key']+' · '+p['name']+' 대응·점검 작업지',body,'../'))

issues=[
 dict(id='IMP-01',equipment='FN03',networks=[1801],observation='Tag_66에 연결한 SD 코일 Part 854·908 두 곳이 있습니다. 같은 RefId 95와 35초 설정, Memo_M25_Running 분기와 PContact를 확인했습니다.',impact='감시 타이머의 실제 시작·리셋·유지와 고장 검출 시점이 단순 모델과 달라질 수 있음',validation='V18 TIA에서 펄스 접점과 두 SD 실행 순서·각 조건·온라인 타이머를 대조',proposal='중복 타이머 구동의 의도가 확인된 뒤 타이머 소유와 운전 모드별 조건을 명시',status='원본 구조 확인 / 활성 동작·수정 필요성 미확정'),
 dict(id='IMP-02',equipment='MV06',networks=[1711],observation='열기·닫기 경로에 ON의 Negated operand가 있으며 정적 조건은 NOT ON으로 시작합니다. 같은 경로의 일부 분기에는 ON도 참조됩니다.',impact='활성·미사용 로직 또는 운전 조건 구분 없이 수동·자동 허가를 설명하면 잘못 판단할 수 있음',validation='ON(M0.0)의 쓰기와 호출, 다른 MV06 출력 쓰기, 현재 활성 네트워크를 확인',proposal='활성 범위·운전 조건을 문서화하고 확인 후 불필요한 경로 정리 여부 검토',status='원본 반전 접점 확인 / 오류 여부 미확정'),
 dict(id='IMP-03',equipment='MC04',networks=[1941],observation='VS01 미운전 시 요청 해제 조건은 Allarm.Maintenance_ON입니다. BC01 등 다른 경로의 Flag.Maintenance_ON과 이름 공간이 다릅니다.',impact='서로 다른 유지보수 신호를 같은 값으로 설명하거나 치환할 위험',validation='DB 선언·주소·읽기·쓰기와 현재 HMI 모드 전달을 대조',proposal='실제 의미가 확인되면 유지보수 모드의 명칭·표시·허가 정책을 일관되게 정리',status='원본 신호 명칭 차이 확인 / 동일성 미확정'),
 dict(id='IMP-04',equipment='FN06',networks=[1802,1955],observation='FN06 관련 요청 해제에 Allarm.MBVA01_FAULT를 참조합니다. 고장 태그 이름이 FN06 이름과 다릅니다.',impact='정비 시 최초 고장·장치 대응을 잘못 찾을 수 있음',validation='알람 Set·Reset, 내부 선언과 HMI 문구, 도면과 실제 팬을 대조',proposal='별칭 또는 과거 장치명 관계를 근거와 함께 표시하고 확인 후 명칭 정리 검토',status='원본 참조 확인 / 태그 의미 미확정'),
 dict(id='IMP-05',equipment='BR01·MV03',networks=[1868],observation='Close MV03 for Burner Startup을 Set하는 한 정적 경로에 Inputs.MV03 Close와 NOT Inputs.MV03 Close가 동시에 나타납니다. 별도 상태 7 경로도 존재합니다.',impact='해당 분기를 실제 동작으로 설명하면 원본의 활성·비활성 경로를 혼동할 수 있음',validation='두 피연산자의 UID/RID·원본 접점과 TIA 표시, 단계·호출 문맥을 확인',proposal='현재 쓰기 경로를 확정한 뒤 미도달 경로의 정리 또는 의도 문서화 검토',status='정적 경로 확인 / TIA에서 재확인 필요'),
 dict(id='IMP-06',equipment='FN04',networks=[1689,1965],observation='1689는 ON일 때 Data.SET_PERC_FN04<5를5, >100을100으로 씁니다(Part831·839). 1965는 같은 설정=0을 요청 해제 조건으로 읽습니다.',impact='한 네트워크에 설정0을 직접 넣은 부분 시험을 전체 프로그램의 설정0 정지 동작으로 오해할 수 있음',validation='아날로그 출력 변환·모터 제어 블록의 호출 조건과 순서, HMI·자동 시퀀스의 동일 설정 쓰기를 확인',proposal='실제 정지 요청과 운전 설정의 역할·최소값 정책을 문서화하고 정지 경로를 일관되게 검토',status='원본 제한 쓰기·정지 읽기 확인 / 전체 실행 도달 조건 미확정')
]
(ROOT/'registers/improvement-review.json').write_text(json.dumps(dict(source='original LAD static review',items=issues,changes_applied=0,field_verified=0),ensure_ascii=False,indent=2)+'\n')
with (ROOT/'registers/improvement-review.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(issues[0]));writer.writeheader();writer.writerows(issues)
body='<div class="notice">원본에서 확인한 구조와 검토 후보입니다. 현재 PLC의 동작 오류 또는 수정 필요성이 확정된 것은 아닙니다. 프로그램 변경 0건, 현장 검증 0건입니다. 기존 자료 불일치 18건의 상태와 별도로 관리합니다.</div>'+table(['ID·설비','원본 관찰','영향','다음 검증','개선 후보·상태'],[[x['id']+' / '+x['equipment'],x['observation'],x['impact'],x['validation'],x['proposal']+' / '+x['status']] for x in issues])
body+='<h2>개별 영향·대안·확인 작업지</h2><p>선택 신호의 전체 원본 읽기·쓰기, Global/Local 범위, 알려진 호출과 후보 핀·반전 배선을 대조합니다. 변경안은 근거 확인을 전제로 한 검토이며 PLC 변경과 시뮬레이터 실행을 수행하지 않습니다.</p><nav class="inline-actions">'+''.join('<a href="improvement-guides/'+x['id']+'.html">'+e(x['id']+' · '+x['equipment']+' 영향·확인')+'</a>' for x in issues)+'</nav>'
body+='<h2>원본 위치</h2><nav class="inline-actions">'+''.join('<a href="networks/network-'+str(n)+'.html">'+e(x['id'])+' · 원본 '+str(n)+'</a>' for x in issues for n in x['networks'])+'</nav><p><a href="registers/improvement-review.json">검토 JSON</a> · <a href="registers/improvement-review.csv">검토 CSV</a> · <a href="registers/improvement-impact.json">영향 근거 JSON</a></p>'
(ROOT/'improvement-review.html').write_text(page('PLC 개선 검토 · 원본 구조 후보 '+str(len(issues))+'건',body))
print(json.dumps(dict(priority_guides=23,improvement_candidates=len(issues),code_changes=0),ensure_ascii=False))
