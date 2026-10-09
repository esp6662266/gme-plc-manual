"""Read-only source identification dossiers. Candidates never assign equipment I/O."""
from pathlib import Path
from html import escape as e
import hashlib,json,csv
from importlib.machinery import SourceFileLoader
R=Path(__file__).resolve().parent
inputs={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def source(f):inputs[f]=sha(R/f)
def load(f):source(f);return json.loads((R/f).read_text())
def link(f,t):
 if f!='registers/unresolved-identity.json':assert (R/f.split('#')[0]).is_file(),f
 return '<a href="'+e(f,quote=True)+'">'+e(str(t))+'</a>'
for f in ['build-unresolved-identity.py','body-native-evidence.py','sources/PEData.plf','sources/PID_1684n002I.pdf','sources/Electrical_Rev2.pdf','sources/Electrical_Can_Decoating_20241118.pdf']:source(f)
model=load('registers/program-model.json');nets={n['id']:n for n in model['networks']}
mp={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
proof=SourceFileLoader('identity_native',str(R/'body-native-evidence.py')).load_module().collect(R,nets,mp,load('sources/decoded-original/identifier-declarations.json'),source)
selected=[424,425,1932,1933]
native=[]
for i in selected:
 n=nets[i];source(n['file']);native.append(dict(id=i,file=n['file'],title=n['title'],block=n['block'],evidence=proof(i),candidate_only=True,identity_verified=False))
idx=load('sources/live_index.json');index_ids=[565,566]
index_evidence=[dict(id=i,values=next(x['values'] for x in idx if x['i']==i and 'values' in x and x['values'].get('Address'))) for i in index_ids]
profiles=[
 dict(key='P03',title='웨잉호퍼1',confirmed='배치도 명칭은 호퍼1입니다. 제공 백업에는 명시적으로 WEIGHTING HOPPER 2FAULT 외부 입력과 client17 고장 래치가 있습니다.',excluded='호퍼2 자료를 호퍼1의 직접 입력·알람·계량 로직으로 배정하지 않습니다. 전용 계량기 내부 순서·Reset·재기동은 확보 전입니다.',needed='호퍼 번호/명판·위치 사진, 로드셀·계량 표시기 모델, 계량 제어반/CPU, 투입·배출 전체 경로, 최신 단자/I/O/통신도.',symptom='계량/배출 불능: 실물ID·시각 → 전용 계량기 최초 알람 → 로드셀·게이트·컨베이어 경계 → 확인된 연동의 요청/응답 → 전용 원본 대조.',candidates=['hopper2','bwf']),
 dict(key='P04',title='웨잉호퍼배출컨베이어',confirmed='제공 백업의 HOPPER CONVEYOR 2FAULT는 client18 외부 고장 입력입니다. 별도 BWF01/02 원격기동 허가 출력 자료도 있습니다.',excluded='일반 컨베이어 명칭과 425 제목의 bwf02만으로 CLIENT-CL18=BWF02=P04라고 확정하지 않습니다.',needed='본체·모터·감속기 명판, 기동반/VFD 표시, 케이블번호·양단 단자, 상하류 연결 사진, 외부반 Ready/Run/Fault/허가의 주체·정상 극성.',symptom='미기동: 실물ID → 자기 기동반/VFD 최초 상태 → 명령과 실제 Run 구분 → 상하류 허가/Fault 변화 → 확인된 케이블·단자 비교.',candidates=['hopper2','bwf']),
 dict(key='P14',title='2사이클론',confirmed='P&ID에는 HE01–FN01 사이 CY01/CY03 한 쌍과 별도 CY02/CY04/CY05–SC01 군이 있습니다. 시공31페이지 M21/VR01·M23/VR02와 CY02의 17HL1/6SB03을 구분합니다. 시공58페이지 8_16은 UC01 FLO4TB1→CY02 17HL1의 DC/CVV/3G/1.0 표기입니다.',excluded='숫자2가 장치 번호인지 수량인지 미확정입니다. CY02·CY01+CY03 어느 쪽도 배정하지 않습니다. 주변 램프·버튼·질소박스·VR/SC/FN 구동을 본체의 전용 제어로 합치지 않습니다.',needed='원래 배치도에서 숫자2의 의미, 본체 명판/태그와 입출구·하부 배출 사진, 최신 P&ID/기계도, 주변 구동·센서 목록.',symptom='분리/배출 이상: 실제 본체 식별 → 가스/고형물 유로·발생 위치 → 배출 구동·팬·계측 경계 → 제작사 기준 및 관련 장치 근거 비교.',candidates=['cyclones']),
]
candidates=[
 dict(id='hopper2',title='호퍼2 client17/18 고장 래치',detail='Global 물리 Input AO132/133(색인 I16.4/I16.5). 선택 원본424/425: ON AND 외부 Fault → Set; ON AND NOT 외부 Fault AND Flag.RESET_ALLARM → Reset. 타이머·Ready·Run·기동 출력·계량 내부 제어가 이 두 네트워크에 없습니다. 다른 미확보 실행 경로의 부재를 증명하지 않습니다.',networks=[424,425],paths=['sources/decoded-original/0599-IdentXmlPart.xml','sources/decoded-original/0601-IdentXmlPart.xml']),
 dict(id='bwf',title='별도 BWF01/BWF02 원격기동 인터페이스',detail='선택1932/1933: ON에서 자기 Fault, ControlFault, SET_PERC=Int0, NOT 처리 BWF OK, NOT 처리 BC01 run, motors 1 Local Disable_Load_RD01의 여섯 OR → M_BWF 요청 Reset. 별도 ON AND M_BWF → Consent Start 일반 Coil. Output AO50/51(색인 Q6.2/Q6.3). Local을 같은 이름의 다른 범위와 합치지 않습니다. 요청 해제와 실제 구동 정지·재기동은 다릅니다.',networks=[1932,1933],paths=['sources/decoded-original/0602-IdentXmlPart.xml','sources/decoded-original/0606-IdentXmlPart.xml']),
 dict(id='cyclones',title='서로 다른 사이클론 배치·시공 구역',detail='CY01/CY03–HE01/FN01과 CY02/CY04/CY05–SC01을 구분합니다. 도면의 구역/접속함 표기는 제어 소유 관계가 아닙니다. 시공58페이지의 가려진 행은 복원·채택하지 않습니다.',networks=[],paths=['sources/PID_1684n002I.pdf#page=1','sources/Electrical_Can_Decoating_20241118.pdf#page=31','sources/Electrical_Can_Decoating_20241118.pdf#page=58']),
]
for p in profiles:p.update(plc_id='',match='unknown',identity_verified=False,assigned_signals=[],field_verified=False)
for c in candidates:c.update(assigned_to_priority=[],field_verified=False,identity_verified=False)
freeze=load('registers/simulator-freeze.json')
for f,h in freeze['files'].items():assert sha(R/f)==h
for f in ['sources/hmi_plc_tags.csv','registers/priority-equipment.csv']:source(f)
review_path='registers/unresolved-identity-independent-review.json'
review=load(review_path);assert review['status']=='reviewed' and review['confirmed_errors']==0
for f,h in review['source_hashes'].items():assert sha(R/f)==h,f
record=dict(date='2026-10-09',profiles=profiles,candidates=candidates,native=native,index_evidence=index_evidence,sources=inputs,independent_review=review_path,counts=dict(profiles=3,candidates=len(candidates),native_networks=len(native),assigned_signals=0,identity_verified=0),field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun',source_conflicts_preserved=18)
style='body{margin:0;padding:24px;background:#f2f6f9;color:#183247;font:16px/1.7 system-ui}main{max-width:1200px;margin:auto}section,details{background:white;padding:22px;margin:18px 0;border:1px solid #cddce7;border-radius:12px}a{color:#06678d;margin-right:14px}nav a{display:inline-block;margin-bottom:9px}.notice{background:#fff5db;padding:16px;border-left:5px solid #d7a832}summary{cursor:pointer;font-weight:700}dt{font-weight:700;margin-top:15px}dd{margin:5px 0}code{overflow-wrap:anywhere}@media(max-width:720px){body{padding:10px}section,details{padding:12px}}'
body='<h1>미확정 설비3개 · 식별·외부 제어 경계</h1><div class="notice">자료 후보가 존재해도 이 설비의 직접 I/O·알람으로 배정하지 않습니다. 실물 동일성·현재 CPU·전용 제어기·현장 복구는 확인 전입니다. 시뮬레이터·실제 PLC 변경0건.</div><nav>'+''.join('<a href="#identity-'+p['key']+'">'+e(p['title'])+'</a>' for p in profiles)+'<a href="#candidates">원본 후보3경로</a><a href="#native">원본4네트워크</a></nav>'
for p in profiles:
 body+='<section id="identity-'+p['key']+'"><h2>'+e(p['key']+' · '+p['title'])+'</h2><p>PLC 미배정 · 실물 동일성 미확정</p><dl>'+''.join('<dt>'+label+'</dt><dd>'+e(p[key])+'</dd>' for label,key in [('확인된 자료 범위','confirmed'),('배정하지 않는 근거','excluded'),('필요한 자료','needed'),('증상에서 확인할 순서','symptom')])+'</dl><p>'+''.join('<a href="#candidate-'+i+'">'+e(next(c['title'] for c in candidates if c['id']==i))+'</a>' for i in p['candidates'])+'</p><p>'+link('priority-guides/'+p['key']+'.html','기존 대응 작업지')+link('repair-guides/'+p['key']+'.html','기존 수리 판단')+link('index.html#view=repair-record&equipment='+p['key']+'&scope=priority','자기 관찰·수리 기록')+'</p></section>'
body+='<section id="candidates"><h2>실제 자료 후보 · 설비 연결 미확정</h2><p>자료명·주소·원본 조건은 확인 범위입니다. 원인 해소 → 래치 해제 → 새 요청 → 허가/출력 → 실제 응답을 분리합니다. 외부반 내부 복구·재기동 순서를 새로 정의하지 않습니다.</p>'
for c in candidates:
 body+='<details id="candidate-'+c['id']+'"><summary>'+e(c['title'])+'</summary><p>'+e(c['detail'])+'</p><p>'+''.join(link('networks/network-'+str(n)+'.html','원본 '+str(n)) for n in c['networks'])+''.join(link(f,'자료 '+str(i+1)) for i,f in enumerate(c['paths']))+'</p><p>우선 설비에 배정0건 · 현재 사용/소유 확인 전</p></details>'
body+='</section><section id="native"><h2>원본 핀·배선·선언</h2><p>복원 XML의 Part/Wire/ORef와 정확한 UID/RID/NID 선언을 보존합니다. 참조 목록 순서로 실행 순서를 추정하지 않습니다. 색인 번호와 원래 NID가 다른 경우 JSON에 함께 보존합니다.</p>'+''.join('<p>'+link('networks/network-'+str(n['id'])+'.html',str(n['id'])+' · '+n['title'])+link(n['file'],'원본XML')+'</p>' for n in native)+link('registers/unresolved-identity.json','핀·배선·선언 JSON')+link(review_path,'독립 원본 대조')+'</section><p>'+link('requirements-audit.html','전체 작성 상태')+link('work-progress.html','진행 순서')+link('index.html','올인원')+'</p>'
(R/'registers/unresolved-identity.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
(R/'unresolved-identity.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>미확정 설비 식별 | GME</title><style>'+style+'</style></head><body><main>'+body.replace('미확정','미확정')+'</main></body></html>')
print(json.dumps(record['counts'],ensure_ascii=False))
