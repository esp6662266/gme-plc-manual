"""Build a source-backed, offline equipment handbook and evidence registers."""
from pathlib import Path
import collections, csv, hashlib, html, json, re, runpy, shutil, zipfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
BASE=Path('/private/tmp/gme-pv01-analysis-20261007')
DECODE=ROOT/'sources/decoded-original'
BACKUP=Path('/private/tmp/gme-original-project-review-20261007')
PV=ROOT.parent/'gme-pv01-manual-20261007'
for folder in ('assets','devices','networks','sources','registers'):
    (ROOT/folder).mkdir(exist_ok=True,parents=True)

def dump(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def esc(s): return html.escape(str(s),quote=True)
def csvfile(name,headers,rows):
    with (ROOT/'registers'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(rows)
def table(headers,rows):
    return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+esc(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def mtable(headers,rows):
    def clean(x):return str(x).replace('|',' / ').replace('\n',' ')
    return '| '+' | '.join(map(clean,headers))+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(clean,row))+' |\n' for row in rows)
def page(title,body,prefix='../',nav=''):
    return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title><link rel="stylesheet" href="'+prefix+'assets/manual.css"></head><body><header><a href="'+prefix+'index.html">GME 전체 설비 매뉴얼</a><a href="'+prefix+'index.html#purpose">프로젝트 목적·작업 순서</a><span>v0.2 · 2026-10-07 · 자료 검토본</span></header><div class="layout">'+nav+'<main><h1>'+esc(title)+'</h1>'+body+'</main></div><footer>원본 백업과 도면에 근거한 오프라인 검토본 · 현장 현재값 및 TIA 실행 결과와 구분</footer></body></html>'

purpose='''<section aria-labelledby="purpose"><h2 id="purpose">프로젝트 목적과 작업 우선순위</h2><p>이 프로젝트의 목적은 <strong>전체 설비 매뉴얼 작성, 고장 진단과 수리 지원, PLC 프로그램 구조 파악, 근거에 따른 개선 검토</strong>다. 2026-10-07 사용자가 확정한 목적을 기준으로 다음 작업을 진행한다.</p><ul><li><strong>매뉴얼:</strong> 설비 역할·운전 조건·점검 방법을 도면, I/O, HMI, 원본 래더와 연결한다.</li><li><strong>진단·수리:</strong> 증상 → 확인 신호 → 관련 래더 → 도면·단자 → 조치 → 복구 검증의 순서로 안내한다.</li><li><strong>프로그램 구조:</strong> OB·FC·FB·DB의 역할, 호출 조건, 읽기·쓰기 위치, 인터록, 타이머, 초기화 및 공통 기능을 분석한다.</li><li><strong>개선 검토:</strong> 문제 후보별 근거, 현재 동작, 변경안, 영향 범위, 검증 방법과 복원 방법을 기록한다.</li></ul><p><strong>다음 작업은 프로그램 구조도와 설비별 고장 진단표 작성이다.</strong> 전체 설비를 대상으로 분석하고, BC01 등 개별 장치에서 신호 추적 방식의 상세도를 확인한다. HMI는 자료 탐색과 진단의 진입점으로 사용하며, 시뮬레이터는 동작 이해·고장 재현·개선안 비교 검증을 지원한다.</p><p>현재 자료는 설비별 참조 목록과 정적 래더 조건을 제공한다. 블록 호출 관계, 신호를 쓰는 위치의 실행 우선순위, 단자별 진단 및 개선안 검증은 후속 작업으로 구분한다. <a href="PROJECT-PURPOSE.md">목적·산출물·작업 순서 상세 문서</a></p></section>'''
purpose=purpose.replace('다음 작업은 프로그램 구조도와 설비별 고장 진단표 작성이다.', '먼저 전체 설비 제어 명세를 작성하고, 프로그램 구조도와 고장 진단표를 연결한다.')

CSS='''
:root{font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;color:#172635;background:#f3f6f8;line-height:1.7;font-size:16px}*{box-sizing:border-box}body{margin:0}header{position:sticky;top:0;z-index:4;display:flex;gap:24px;justify-content:space-between;align-items:center;background:#142f42;color:white;padding:14px 30px;border-bottom:3px solid #22ac9c}header a{color:white;font-weight:700;text-decoration:none}header span{font-size:13px;color:#c3d7e1}.layout{display:flex;max-width:1700px;margin:auto}main{padding:28px 36px;background:white;min-width:0;flex:1}h1{font-size:29px;line-height:1.4;margin:4px 0 20px}h2{font-size:22px;border-top:1px solid #d8e1e6;margin-top:34px;padding-top:20px;scroll-margin-top:90px}h3{font-size:18px}a{color:#12687d}p{max-width:1000px}.table-wrap{overflow:auto;margin:16px 0;border:1px solid #d7e2e6;border-radius:5px}table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:10px 12px;border-bottom:1px solid #dce5e9;text-align:left;vertical-align:top}th{background:#eaf1f4;font-weight:700;white-space:nowrap}td code{white-space:nowrap}tbody tr:nth-child(even){background:#f9fbfc}code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px}pre{white-space:pre-wrap;word-break:break-word;background:#f0f4f6;border:1px solid #d9e2e7;padding:16px;overflow:auto}ul,ol{padding-left:24px;max-width:1050px}li{margin-bottom:8px}.note{background:#fff6dd;border-left:4px solid #b98216;padding:14px 18px;margin:18px 0}.source{background:#eaf5f2;border-left:4px solid #248578;padding:14px 18px;margin:18px 0}.badge{display:inline-block;border-radius:4px;padding:1px 8px;background:#e5eef2;font-size:12px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:20px 0}.card{padding:18px;border:1px solid #d9e4e8;border-radius:6px;background:#f8fbfc}.card strong{font-size:25px;color:#154e66}.controls{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0}input,select,button{font:inherit;border:1px solid #9fb5c1;border-radius:5px;padding:10px;background:white;color:#173344}input{flex:1;min-width:240px}button{cursor:pointer}figure{margin:20px 0}img{max-width:100%;height:auto}figcaption{font-size:13px;color:#506778}.diagram{overflow:auto;border:1px solid #d9e2e7;background:white;margin:18px 0}.diagram img{max-width:none}.toc{width:245px;flex-shrink:0;position:sticky;align-self:flex-start;top:76px;max-height:calc(100vh - 92px);overflow:auto;padding:20px;background:#edf3f6;font-size:14px}.toc a{display:block;padding:7px 0}.muted{color:#607785;font-size:13px}details{margin:18px 0}summary{cursor:pointer;font-weight:700}footer{text-align:center;font-size:12px;padding:25px;color:#607785}@media(max-width:800px){main{padding:20px 16px}.toc{display:none}header{padding:12px 16px}header span{display:none}h1{font-size:24px}}@media print{header{position:static}.toc,.controls{display:none}body,main{background:white}main{padding:0}h2{break-after:avoid}.table-wrap{overflow:visible}tr{break-inside:avoid}a{color:inherit}footer{display:none}}
'''
CSS+='\ntd code.condition{white-space:normal;overflow-wrap:anywhere;display:block;min-width:230px;max-width:620px}\n'
(ROOT/'assets/manual.css').write_text(CSS)

live=json.loads((BASE/'live_index.json').read_text())
blocks=json.loads((BASE/'block_summary.json').read_text())
nets=json.loads((DECODE/'network-map.json').read_text())
decode_stats=json.loads((DECODE/'decode-summary.json').read_text())
hmi=list(csv.DictReader((BASE/'hmi_plc_tags.csv').open(encoding='utf-8-sig')))
symbols=[dict(x['values'],segment=x['segment'],document_id=x['i']) for x in live if not x['deleted'] and x['values'].get('Address')]
pages=json.loads(Path('/private/tmp/gme-electrical-review-20261007/text-pages.json').read_text())
pageby={p['page']:p['text'] for p in pages}

def pdfpage(fg):
    fg=str(fg)
    if fg=='5A':return 6
    if fg=='180A':return 182
    if fg=='180B':return 183
    n=int(fg)
    return n+(n>5)+(2 if n>180 else 0)
def fg_links(fgs,prefix='../'):
    return ', '.join('<a href="'+prefix+'sources/Electrical_Rev2.pdf#page='+str(pdfpage(f))+'">FG '+str(f)+' / PDF '+str(pdfpage(f))+'</a>' for f in fgs) or '직접 전기 회로 식별 근거 없음'
def plainfg(fgs):return ', '.join('FG '+str(f)+' / PDF '+str(pdfpage(f)) for f in fgs) or '직접 회로 식별 근거 없음'

devices=[]
def add(id,name,kind,group,fgs=(),role='',parent='',status='자료에서 확인',aliases=(),pid=True,note=''):
    devices.append(dict(id=id,name=name,kind=kind,group=group,fgs=list(fgs),role=role,parent=parent,status=status,aliases=list(aliases),pid=pid,note=note))

# Curated identities avoid promoting HMI graphic names (AB0 etc.) into equipment.
add('BC01','드럼 투입 컨베이어','motor','원료 이송',[18,19],'원료를 PV01 투입 게이트까지 이송한다.',aliases=['belt conveyor bc01'])
add('RD01','회전 드럼','motor','원료 이송',[20,21],'원료의 회전·체류를 담당한다. 투입·배출 게이트와 함께 운전 조건을 검토한다.')
add('RD01-FAN','드럼 모터 냉각팬','motor','원료 이송',[22],'RD01 구동 모터 냉각 보조장치.',parent='RD01',aliases=['fan rd01','rd01f','rd_01_fan'])
add('MC03','예비 모터 MC03','motor','원료 이송',[23],'PLC의 예비 모터 및 토크 감시 항목.',status='예비·실물 동일성 확인',aliases=['mc03','mc_03','spare motor'],pid=False,note='P&ID에서 주설비 태그로 확인되지 않는다. Q0.3과 MC03/SS09 참조를 별도 예비 장치로 보관한다.')
add('MC04','금속 컨베이어','motor','원료 이송',[24,25],'PV02 배출 원료를 VS01 방향으로 이송한다.')
add('MC05','금속 컨베이어 MC05','motor','원료 이송',[26],'전기도면과 PLC 입출력에는 남아 있는 이송 장치.',status='삭제 제목·예비 여부 확인',pid=False,note='Motors 1에는 mc05 deleted 제목이 있다. 입출력과 도면의 잔존만으로 현재 설치·사용 상태를 결정하지 않는다.')
add('VS01','진동 스크린','motor','원료 이송',[27,28],'배출 원료를 선별한다. VS01/VS01A 공통 피드백을 분리 검토한다.',aliases=['vs01a','vs_01a'])
add('SC12','드럼 배출실 스크루','motor','원료 이송',[29],'드럼 배출실 측 원료 배출 스크루.',status='SPARE·삭제 제목',note='P&ID에 존재하지만 전기 회로 SPARE와 sc12 deleted 제목이 확인됐다. 설치 상태와 유지되는 배선을 확인한다.')
add('CC01','드럼 투입실','passive','공정 본체',role='PV01과 RD01 입구 사이의 투입 챔버. 기밀·퇴적·게이트 간섭을 점검한다.')
add('UC01','드럼 배출실','passive','공정 본체',role='RD01 출구, PV02 및 배출 경로를 구성하는 챔버.')
add('AB01','연소 챔버','passive','연소·열회수',role='BR01의 연소와 TC01/02 온도 감시가 연결되는 공정 챔버.')
add('BR01','가스 버너','burner','연소·열회수',[97,98,99,100],'연소 상태·락아웃·가스/공기 조건·변조 값을 외부 버너 시스템과 교환한다.',aliases=['burner','brurner','br01','br_01'],note='버너 전용 상세 도면 및 제조사 연소 제어 절차는 별도 문서가 필요하다. 이 매뉴얼의 일반 PLC 해석을 버너 안전 시퀀스로 대체하지 않는다.')
add('HE01','열교환기','passive','연소·열회수',role='P&ID의 열교환 본체. MV01/MV04와 FN02의 연결 경로를 함께 검토한다.')
for i,fg,name,role in [(1,[47,48],'순환 블로어','TC04/TC05 베어링 온도, ZT01 및 전류 감시와 연결된다.'),(2,[42,43],'열회수 블로어','열회수 경로의 송풍과 아날로그 속도 설정을 담당한다.'),(3,[51],'연소 공기 블로어','BR01 측 연소 공기 공급 경로.'),(4,[59,60],'집진 배기팬','CY·BF 집진 경로의 흡인 및 압력 제어와 연결된다.'),(5,[65],'석회 계통 송풍기','LD01/ER01 석회 계통 송풍 경로.'),(6,[52],'보조 블로어','P&ID의 AB01 하부 보조 송풍 경로.')]:
    add(f'FN{i:02}',name,'motor','연소·열회수' if i in (1,2,3,6) else '집진·석회',fg,role)
add('FN01-FAN','FN01 모터 냉각팬','motor','연소·열회수',[54],'FN01 구동부 냉각 보조장치.',parent='FN01',status='SPARE·삭제 제목',aliases=['star fan fn01','fn01f','fn_01_fan'],note='Q3.5/I4.5 잔존과 SPARE 표기를 따로 기록한다.')
add('CH01','냉각기','motor','연소·열회수',[50],'FN01 측 냉각 계통. PLC 내부 시작 요청과 별도 원격 기동 출력 경로를 구분한다.',aliases=['chiller'])
for i in range(1,7):
    fgs={1:[44,45],2:[30,31,36,37],3:[38,39],4:[40,41],5:[30,31,34,35],6:[30,31,32,33]}[i]
    role={1:'TC03 관련 열회수 경로 제어.',2:'PSH01 관련 배기/압력 경로 제어.',3:'PSH03 관련 오버플로 경로 제어.',4:'FN02/HE01 경로의 모터 밸브. M18A/M18B 두 구동부를 구분한다.',5:'RO01 관련 산소 제어 경로.',6:'PSH02 관련 오버플로 경로 제어.'}[i]
    add(f'MV{i:02}','모터 구동 밸브','motorvalve','제어 밸브',fgs,role,note='공통 전원 MV02/05/06은 개별 구동 피드백과 분리한다.' if i in (2,5,6) else '')
for i in range(1,5):
    fgs={1:[69,70],2:[71,72],3:[73],4:[74]}[i]
    roles={1:'드럼 투입 A/B 게이트. EV01/02, CL01~04 및 위치 센서와 연결된다.',2:'드럼 배출 A/B 게이트. EV04/05, CL05~08 및 위치 센서와 연결된다.',3:'스크린 배출 분기 밸브. EV06, CL09/10에 연결된다.',4:'드럼 배출실 밸브. EV07, CL11에 연결된다.'}
    aliases={1:['ev01','ev02'],2:['ev04','ev05'],3:['ev06'],4:['ev07','button open pv-0000','74sb1']}[i]
    add(f'PV{i:02}','공압 게이트/분기 밸브','gate','공압 밸브',fgs,roles[i],aliases=aliases,status='예비 표기·삭제 제목' if i==4 else '자료에서 확인',note='회로 및 출력 SPARE와 pv04 deleted 제목을 확인해야 한다.' if i==4 else '')
for i in (5,6):add(f'PV{i:02}','질소 주입 밸브','nitrogen','공압 밸브',[96],'질소 비상 주입 계통. 탱크 준비 입력과 공통 주입 요청 출력을 함께 검토한다.',aliases=['nitrogen'],note='두 밸브의 개별 PLC 출력으로 단정하지 않는다. 외부 릴레이·타이머 박스 회로가 포함된다.')
add('PV14','필터 냉풍 유입 밸브','gate','공압 밸브',[168],'집진 필터 냉풍 유입. 열림/닫힘 입력과 필터 과온 대응을 검토한다.',aliases=['false air','cold air'])
for i in range(1,6):add(f'CY{i:02}','사이클론','passive','집진·석회',role='P&ID의 분진 분리 본체. 배출 로터리 밸브 또는 SC01 경로와 연결해 점검한다.')
for i in range(1,7):
    fg={1:46,2:49,3:61,4:62,5:63,6:64}[i]
    add(f'VR{i:02}','로터리 밸브','motor','집진·석회',[fg],'사이클론·필터·석회 경로에서 배출 및 공기 차단을 담당한다.')
for id,name,fg in [('SC01','사이클론 분진 스크루',53),('SC10','BF01 분진 스크루',57),('SC11','BF02 분진 스크루',58)]:
    add(id,name,'motor','집진·석회',[fg],'분진을 해당 로터리 밸브로 이송한다.',aliases=['sc-1'] if id=='SC01' else [])
for i,fg in [(1,list(range(152,181))+['180A','180B']),(2,list(range(181,205)))]:
    add(f'BF{i:02}','백 필터','filter','집진·석회',fg,'DP 차압 감시, 분진 스크루·로터리 밸브, 펄스 세정 밸브가 연결되는 집진 장치.',aliases=[f'pr_bf{i:02}',f'pr_br{i:02}',f'bf_{i:02}',f'filter {i}'])
add('LD01','석회 마이크로피더','motor','집진·석회',[55,170],'석회 투입 장치. VR06 운전, 점검 도어, 저레벨 및 현장 셀렉터를 함께 점검한다.')
add('LD01A','석회 사일로 진동기','motor','집진·석회',[56],'LD01의 간헐 운전/정지 타이머와 현장 요청에 연결되는 진동기.',parent='LD01',aliases=['ld_01_vib','ld01v','vibrator ld-01','ld-01a'])
add('ER01','전기 히터','heater','집진·석회',[66],'FN05와 석회 투입 공기 가열 경로. 온도 허용 및 피드백을 함께 검토한다.')
for id,name,role in [('CM01','집진 배기 스택','FN04 후단의 대기 배출 경로.'),('CM02','상부 배기 스택','MV02 측 대기 배출 경로.'),('CR01','운전 제어반','P&ID의 운전 캐비닛. 전기 계통·보조전원·운전 표시와 연결된다.')]:add(id,name,'passive','공정 본체',role=role)
for i in (1,2):add(f'BWF{i:02}','고객 설비 계량 피더','client','외부 연동',list(range(85,96)), '외부 피더의 준비·운전·고장·레벨·유량과 원격 운전 허가를 교환한다.',pid=False,aliases=[f'bwf {i:02}',f'bwf{i}',f'bwf_{i:02}'])
add('LIW','외부 LIW 피더','client','외부 연동',list(range(85,96)),'고객 피더 시스템 원격 시작과 속도 설정. BWF 계통 및 배출 분기 상태와 교차 검토한다.',pid=False,aliases=['liw','autoreader'])
clients={1:'Apron conveyor A',2:'Impactor',3:'Impact vibration feeder',4:'Belt conveyor A',5:'Air knife',6:'Belt conveyor B',7:'Shredder 1',8:'Shredder vibration feeder',9:'Belt conveyor C',10:'Rotex screen',13:'Apron conveyor B',14:'Shredder 2',15:'Belt conveyor D',16:'Belt conveyor E',17:'Weighing hopper 2',18:'Hopper conveyor 2',19:'Primary shredder'}
for i,name in clients.items():
    spell={'Impact vibration feeder':'impact vibrationfeeder','Shredder vibration feeder':'shredder vibrationfeeder','Weighing hopper 2':'weighting hopper 2fault','Primary shredder':'primaryshredder','Hopper conveyor 2':'hopper conveyor 2fault','Belt conveyor D':'belt coveyor d'}.get(name,name.lower())
    add(f'CLIENT-CL{i:02}',name,'client','외부 연동',list(range(86,96)),f'PLC 외부 모터/설비 채널 {i:02}. 원격 신호와 실제 외부 제어반 상태를 대조한다.',pid=False,aliases=[f'motor_client_{i:02}',f'client motor {i}',f'cl{i:02}',spell],note='P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.')

for i in (1,2,3,4,5,6,7,9,10,11):
    fg={1:[77],2:[77],3:[77],4:[79],5:[79],6:[78],7:[78],9:[171],10:[171],11:[]}[i]
    role={1:'AB01 챔버 온도.',2:'AB01 안전 온도 채널.',3:'배출 가스 온도·MV01 관련 제어 값.',4:'FN01 베어링 PT100 온도.',5:'FN01 다른 베어링 PT100 온도.',6:'AB01 출구 온도.',7:'유입 가스 온도. 도면 SPARE 표기 확인.',9:'백 필터 유입 온도.',10:'백업에 예비 온도 입력으로 남아 있는 채널.',11:'P&ID ER01 계통의 로컬 온도 표시. PLC 대응은 식별되지 않았다.'}[i]
    add(f'TC{i:02}','온도 계측','sensor','계측',fg,role,aliases=[f'tc_{i:02}'],status='P&ID 로컬 계측' if i==11 else '예비·운영 상태 확인' if i in (7,10) else '자료에서 확인',pid=i!=10)
for i in range(1,5):add(f'RO{i:02}','산소 분석 채널','sensor','계측',[80] if i<3 else [81],'연소·순환 가스 산소 분석. 데이터 변환과 대체값/시험 조건을 함께 검토한다.',aliases=[f'r0-0{i}',f'r00{i}',f'r0_0{i}'])
for i in range(1,4):add(f'PSH{i:02}','압력 측정 채널','sensor','계측',[75], 'P&ID의 압력 제어 위치와 관련 MV 제어 루프를 함께 검토한다.',aliases=[f'psh_{i:02}'])
add('PC01','집진 흡인 압력','sensor','계측',[76],'PC01 4~20mA 입력과 FN04 압력 제어 경로.',aliases=['pc_01'])
add('PC02','소프트웨어 압력 루프 명칭','software','계측',role='백업의 PC02 관련 데이터 명칭. PSH02와 물리 센서 동일성은 별도 검증한다.',pid=False,aliases=['pc_02'],status='소프트웨어 명칭·물리 태그 확인')
for i in (1,2):add(f'DP{i:02}','백 필터 차압','sensor','계측',[169],'BF'+f'{i:02}'+'의 차압 감시. 세정 허가·주기·경보 기준과 연결된다.',aliases=[f'dp_{i:02}', 'pr_bf01' if i==1 else 'pr_br02'])
add('ZT01','FN01 진동 계측','sensor','계측',[82],'FN01 진동 채널. 전기 회로 SPARE와 변환 네트워크 시험 조건을 확인한다.',status='SPARE·활성 조건 확인')
for i,parent in [(2,'MV01'),(3,'MV02'),(4,'MV03'),(5,'MV05'),(6,'MV06')]:add(f'ZT{i:02}','P&ID 밸브 위치 계측','sensor','계측',role=f'P&ID {parent} 위치 계측 태그. 현재 엔코더/TM 채널과 동일성은 확인 항목으로 남긴다.',parent=parent,status='P&ID·현재 엔코더 동일성 확인')
add('LT01','석회 사일로 레벨','sensor','계측',[170],'LD01 사일로의 P&ID 레벨 태그. PLC 저레벨 입력과 현장 센서 동일성을 확인한다.',parent='LD01',aliases=['ll_ld01','low level','lime level'])
for i,parent in [(1,'BC01'),(9,'MC03'),(10,'MC04'),(11,'MC05')]:add(f'SS{i:02}','이송 장치 감시 스위치','sensor','계측',[18,19] if i==1 else [23] if i==9 else [24,25] if i==10 else [26], '트립와이어·회전 또는 토크 감시의 실제 장치 종류와 접점 방향을 확인한다.',parent=parent,aliases=['bc01_tripwire','bc01_prox','ssl-01'] if i==1 else [parent.lower()+'_torque'])
add('PSL05','압축공기 저압 스위치','sensor','계측',[76],'공압 계통의 저압 입력. 게이트 구동 가능 여부와 알람을 대조한다.',aliases=['low pressure air','psl-05'])

# Components are separately addressable; their parent retains the operating chapter.
for i,parent,fg in [(1,'PV01',69),(2,'PV01',69),(3,'RD01',20),(4,'PV02',71),(5,'PV02',71),(6,'PV03',73),(7,'PV04',74)]:
    add(f'EV{i:02}','공압 솔레노이드' if i!=3 else '드럼 윤활 솔레노이드','component','하위 구성품',[fg],'상위 장치 요청·중간 릴레이·현장 코일을 연결해 점검한다.',parent=parent,aliases=[f'ev{i:02}'])
for i in range(11,91):
    parent='BF01' if i<=50 else 'BF02'
    circuit_range=list(range(154,168)) if i<=50 else list(range(183,197))
    # PDF extraction joins the two-digit EV tag to its terminal number (EV-1410X3).
    # Within the known EV11..90 circuit range, preserve that joined label match.
    exact=[fg for fg in circuit_range if re.search(r'EV[- ]'+str(i),pageby[pdfpage(fg)],re.I)]
    add(f'EV{i:02}','필터 펄스 세정 밸브','pulse','필터 세정 밸브',exact or circuit_range, '개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.',parent=parent,pid=True)
for i in range(1,13):
    parent='PV01' if i<=4 else 'PV02' if i<=8 else 'PV03' if i<=10 else 'PV04' if i==11 else 'PV14'
    add(f'CYL-CL{i:02}','공압 실린더','component','하위 구성품',role='P&ID의 실린더. 독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검한다.',parent=parent,aliases=[],note='외부 모터 CLIENT-CL'+f'{i:02}'+'과 별개다.')
lsparents={'01':'PV01','02':'PV01','05':'PV01','06':'PV01','09':'PV03','10':'PV03','15':'MV05','16':'MV05','17':'MV02','18':'MV02','19':'MV03','20':'MV03','21A':'MV04','21B':'MV04','22A':'MV04','22B':'MV04','23':'MV01','24':'MV01','25':'PV02','26':'PV02','29':'PV02','30':'PV02','32':'PV04','33':'PV04','34':'MV06','35':'MV06','40':'MV06','41':'MV06'}
for k,parent in lsparents.items():
    parent_fgs=next(d['fgs'] for d in devices if d['id']==parent)
    add('LS'+k,'밸브 위치 리미트 스위치','component','하위 구성품',parent_fgs,role='개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.',parent=parent,aliases=['ls-'+k.lower(),'ls.'+k.lower()],status='P&ID/전기/백업 번호 대조',pid=k not in ('40','41'),note='MV06은 P&ID LS34/35와 백업 LS40/41 표기가 다르다.' if parent=='MV06' else '')

SYSTEM_BLOCKS={
 'SYS-POWER':[],
 'SYS-SAFETY':['main','startup only'],
 'SYS-PLC-IO':['main','hmi inputs','hmi output','analog input conversion','analog output conversion','signal linearization','i/o_flt1','mod_err','prog_err','rack_flt'],
 'SYS-HMI':['hmi','hmi inputs','hmi output'],
 'SYS-ALARM':['allarm manager','allarms 1','allarms 2','allarms 3','motor/alarm client'],
 'SYS-AUTO':['auto start motors','main','startup only'],
 'SYS-PID':['cyc_int2 ogni 1s','cyc_int5 ogni 100ms','valve control loop','burner control','control_stechio'],
 'SYS-RECIPES':['recipes handler'],
 'SYS-SIMULATION':['simulation','cyc_int4 ogni 200ms'],
 'SYS-RUNHOURS':['time work motor','cyc_int2 ogni 1s'],
 'SYS-COUNTERS':['analog input conversion','cyc_int5 ogni 100ms'],
 'SYS-LEGACY':[],
}
for id,name,fgs,role,aliases in [
 ('SYS-POWER','주전원·보조전원·제어반',list(range(6,12))+[16,84],'주전원·110Vac·24Vdc·제어반 냉각과 서비스 릴레이를 관리한다. 표지 전압과 회로 제목의 차이를 확인한다.',['presence 110v','presence voltage']),
 ('SYS-SAFETY','비상정지·일반 안전 회로',list(range(12,16))+[99,236],'비상정지와 일반 허가, 온도 허가 회로의 물리·논리 경로를 검토한다. CPU 형식이나 일반 PLC 접점만으로 안전 인증을 판단하지 않는다.',['em_ok','em_ok','emergency','temperature interlock','177t1_ok']),
 ('SYS-PLC-IO','CPU·분산 I/O·신호 변환',list(range(102,150))+[153,182],'CPU·I/O 구성, 원시 입력/출력, 단위 환산, 엔코더/TM 및 진단 상태를 관리한다.',['mod_err','prog_err','rack_flt']),
 ('SYS-HMI','HMI·통신·가공 상태',[],'기본 HMI의 화면·태그·PLC 주소·상태 가공과 운전 요청 경로를 관리한다. 전체 782개 설정 대장을 제공한다.',['hmi_db']),
 ('SYS-ALARM','알람·경광등·사이렌·Reset',[17],'원인·유지·확인·Reset·통합 알람 및 출력 표시를 연결한다. HMI Reset 요청과 내부 Reset 비트를 별도 신호로 추적한다.',['resetalarms','reset_allarm','acknowledg','siren','blinking ligh']),
 ('SYS-AUTO','자동 기동·정지·유지보수',[],'운전 허가·기동 단계·대기·유지보수 모드의 호출 및 출력 관계를 관리한다.',['abilitaauto','abilitamaintenance','standby','maintenance']),
 ('SYS-PID','온도·압력·산소·비율 제어',[],'주기 OB의 PID 호출, 채널 선택, 수동/자동, 제한과 밸브·버너 출력 경로를 관리한다.',['tc_pid_ref','stechiometro']),
 ('SYS-RECIPES','레시피·설정값 관리',[],'레시피 선택·편집·적용값·현재 설정 DB를 추적한다. 화면 편집 값과 실제 적용 값의 전달 경로를 구분한다.',['recipe','recipes','editor_']),
 ('SYS-SIMULATION','기존 시험·시뮬레이션 블록',[],'백업에 남은 Simulation 블록과 시험 비트가 실제 입력 대체·자동 조건에 미치는 영향을 검토한다.',['simulation','under testing']),
 ('SYS-RUNHOURS','모터 운전시간·정비 이력',[],'Time work motor 관련 카운트·유지보수 값·Reset 경로를 관리한다.',['hours motors','hours_motor']),
 ('SYS-COUNTERS','생산량·가스·유량 계수',[],'BWF 펄스·생산량·가스/유량·Reset·스케일과 누적값을 관리한다.',['reset_prod_count','reset_gas_count','conta_prod','conta_gas','count_rep']),
 ('SYS-LEGACY','과거 태그·이름 대응',[],'MN01 속도 감소 참조와 PC03/TR01/FR01/VT01 등 과거 이름을 현재 설비와 대조한다. 이름만으로 장치를 병합하지 않는다. DB 인터페이스 설명 원문은 block_summary.json 및 live_index.json에 보존했다.',['mn01','pc03','pc_03','tr01','fr01','vt01','mn02','mn03','mn04'])
]:add(id,name,'software','공통 시스템',fgs,role,aliases=aliases,pid=False)

def pattern(tag):
    m=re.fullmatch(r'([A-Z]+)(\d{2})([AB]?)',tag)
    if not m:return re.compile(r'(?<![a-z0-9])'+re.escape(tag)+r'(?![a-z0-9])',re.I)
    family,num,suffix=m.groups()
    return re.compile(r'(?<![a-z0-9])'+family+r'[-_ ]?0?'+str(int(num))+suffix+r'(?![a-z0-9])',re.I)
def match(d,text):
    # CL identities are intentionally namespaced. Cylinders are P&ID-only here.
    if d['id'].startswith('CYL-'):return False
    if d['id'].startswith('LS'):
        k=d['id'][2:]
        number=re.match(r'(\d+)([AB]?)',k)
        suffix=number[2]
        return bool(re.search(r'ls[-_ .]?0?'+str(int(number[1]))+suffix+r'(?![0-9ab])',text,re.I))
    if d['id'].startswith('CLIENT-'):tags=d['aliases']
    else:tags=[d['id']]+d['aliases']
    return any(pattern(t.upper()).search(text) for t in tags)
def symbolmatch(d,s):return match(d,s.get('Name','')+' '+s.get('Comment',''))

for d in devices:
    d['symbols']=[s for s in symbols if symbolmatch(d,s)]
    d['hmi']=[s for s in hmi if not re.fullmatch(r'AB\d+',s['HMI 태그']) and match(d,s['HMI 태그'])]
    if d['id']=='PV01':
        d['hmi'] += [s for s in hmi if s['HMI 태그'] in ('ResetAlarms','AbilitaMaintenance')]
    d['networks']=[n for n in nets if match(d,n['title']+' '+n['index_code'])]
    if d['id'] in SYSTEM_BLOCKS:
        d['networks']=[n for n in nets if n['block'] in SYSTEM_BLOCKS[d['id']] or match(d,n['title']+' '+n['index_code'])]
    if d['id']=='EV03':d['networks']=[n for n in nets if re.search(r'ev[-_ ]?0?3(?!\d)|evfr01',n['index_code'],re.I)]
    d['physical']=[s for s in d['symbols'] if re.match(r'%[iq]',s['Address'],re.I)]
    d['internal']=[s for s in d['symbols'] if s not in d['physical']]
    d['alarms']=[n for n in d['networks'] if n['block'].startswith('allarm') or n['block']=='motor/alarm client']
    d['own']=[n for n in d['networks'] if match(d,n['title'])]

# The catalog counts related references, not exclusive channel ownership.

byid={d['id']:d for d in devices}
RELATED={
 'CC01':['BC01','PV01','RD01'], 'UC01':['RD01','PV02','PV04','SC12'],
 'AB01':['BR01','FN03','FN06','TC01','TC02','TC06','RO01','RO02'],
 'HE01':['MV01','MV04','FN02'], 'CY01':['VR01','FN01'],
 'CY03':['VR02','FN01'], 'CY02':['SC01','VR03'], 'CY04':['SC01','VR03'],
 'CY05':['SC01','VR03'], 'CM01':['FN04'], 'CM02':['MV02','PSH01'],
 'CR01':['SYS-POWER','SYS-SAFETY','SYS-PLC-IO','SYS-HMI'],
 'BF01':['DP01','SC10','VR04','TC09','PV14','FN04'],
 'BF02':['DP02','SC11','VR05','TC09','PV14','FN04'],
 'LD01':['LD01A','LT01','VR06','FN05','ER01'],
 'PC02':['PSH02','MV06'], 'TC11':['ER01','FN05'],
 'SYS-SAFETY':['SYS-POWER','BR01','SYS-ALARM'],
 'SYS-PID':['MV01','MV02','MV03','MV05','MV06','BR01','FN04'],
}

# Offline diagnosis procedures are proposals, explicitly separated from decoded logic.
PROCEDURES={
'motor':[
('운전 요청이 없을 때','HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.'),
('요청은 있으나 출력이 없을 때','위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.'),
('출력은 있으나 피드백이 없을 때','Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.'),
('운전 중 고장 또는 과전류','기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.'),
('복귀','원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.')],
'motorvalve':[
('공통 전원/구동 준비','공통 인버터 전원 허가와 개별 열림/닫힘 구동 피드백을 따로 기록한다.'),
('수동·자동 요청','HMI 개방/폐쇄 요청, 자동 플래그, 관련 PID 또는 펄스 요청, 양 끝 리미트와 원본 접점의 극성을 대조한다.'),
('반대 방향 동시 요청','개방·폐쇄 두 출력의 상호 배제 조건을 Wires에서 추적한다. 현재 신호가 동시에 발생하는 경우 원인을 찾은 뒤 시험한다.'),
('위치 값·엔코더','리미트 입력, 실제 밸브 위치, 엔코더 카운트, 환산 위치, 저장/전원 복귀 값을 같은 시각에 기록한다. 캘리브레이션 네트워크의 조건과 완료 신호를 확인한다.'),
('동작 지연·고장','구동 출력 → 모터/인버터 → 기구부 → 리미트/엔코더 → 타이머/횟수 고장을 대조한다. 타이머 값은 원본과 설정 DB를 근거로 확정한다.')],
'gate':[
('공압·현장 요청','공기 공급과 저압 스위치, 현장 선택 스위치, 솔레노이드 전원 및 구동 릴레이를 확인한다.'),
('위치 상태','열림만 1, 닫힘만 1, 둘 다 0, 둘 다 1을 구분하고 원시 I, 내부 기억 비트, HMI 가공 상태를 동시에 기록한다.'),
('출력 경로','HMI 요청 → 상태/기억 비트 → 물리 Q → 중간 릴레이 → 솔레노이드 → 실린더 → 위치 센서 순서로 확인한다.'),
('게이트 순서','A/B 두 게이트 장치는 상태 값, 각 단계 진입 조건, Set/Reset 출력, 시간 조건과 다음 상태 Move를 원본 XML로 대조한다.'),
('복귀·전원 재시작','닫힘 상태, 잔존 요청과 기억 비트, 공기 복귀 상태, 초기화 네트워크의 조건을 기록한 후 정상 순서 시험을 설계한다.')],
'sensor':[
('측정 경로','현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.'),
('단위·범위','도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.'),
('값이 고정·비정상','단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.'),
('알람·제어 경계','경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.'),
('교정 기록','기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.')],
'burner':[
('외부 버너 상태','버너 자체 제어반의 준비·운전·락아웃과 PLC 입력을 일대일 대조한다. 외부 버너 상세 시퀀스의 제조사 기준을 함께 적용한다.'),
('요청/허가','원격 시작, 가스/공기 압력, 온도 허가, 블로어와 관련 알람 접점의 실제 연결을 확인한다.'),
('변조 경로','온도 선택 → PID 호출 → 가스/공기 비율 및 제한 → 아날로그 출력 → 실제 서보/유량 피드백을 같은 시각에 기록한다.'),
('정지·락아웃','락아웃 원인·신호 방향·Reset 출력과 외부 버너 응답을 기록한다. 원인 제거와 Reset, 재시작을 서로 다른 사건으로 시험한다.')],
'filter':[
('필터 운전 허가','분진 스크루·로터리 밸브·BF_RUN 표시·차압 기준 및 강제 세정 조건을 원본 Filter 네트워크로 검토한다.'),
('세정 순서','EV11~50과 EV51~90을 구분하고 실제 순서 변수의 값 → 비교기 → 개별 출력 주소를 추적한다. 번호 범위만 보고 순서를 정하지 않는다.'),
('펄스/휴지 시간','작업 시간·휴지 시간·차압 단계별 계수 및 시험 ON/OFF 조건을 기록한다.'),
('세정 불량','출력 펄스 → 릴레이 → 전원/퓨즈 → 코일 → 압축공기 → 밸브 → 차압 변화 순으로 점검한다.'),
('온도·분진 배출','TC09/PV14, SC/VR 피드백과 필터 과온·차압 경보를 연결해 점검한다.')],
'client':[
('인터페이스 의미','외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.'),
('주소·번호','전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.'),
('시간·Handshake','허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.'),
('아날로그 값','유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.'),
('복귀','외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.')],
'nitrogen':[
('외부 박스 회로','탱크 준비 입력, 현장 비상 요청, PLC 공통 주입 출력, 중간 릴레이·타이머, PV05/PV06 배선을 추적한다.'),
('개별 밸브 확인','두 밸브의 현장 코일과 실제 개방 경로를 따로 기록한다. 공통 요청을 개별 위치 피드백으로 사용하지 않는다.'),
('복귀·가스 공급','압력·공급 준비·타이머·요청 해제와 잔존 상태를 도면과 현장에서 대조한다.')],
'heater':[
('운전 허가','FN05 피드백, 온도 허용, ER01 요청/알람, ON/OFF 접점과 실제 출력 경로를 대조한다.'),
('출력 및 온도','Q→릴레이/접촉기→히터 전원과 전류, 온도 센서, 외부 온도 제어기의 허용 신호를 기록한다.'),
('과온·복귀','과온 발생 시 허가 해제·전원 차단·온도 하강·Reset·재가열 결과를 별도로 기록한다.')],
'passive':[
('기계·공정 상태','본체의 누설·기밀·퇴적·마모·부식, 입출구 막힘, 점검구와 연결 배관 상태를 기록한다.'),
('연관 장치','주변 모터·밸브·온도/압력/레벨 계측의 운전 상태와 본체 공정 상태를 연결해 검토한다.'),
('도면 동일성','P&ID의 위치와 실제 본체·배관·전기도면 장치의 태그를 대조하고 변경 사항을 기록한다.')],
'software':[
('논리 명칭 확인','이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.'),
('데이터 추적','원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.')],
'component':[
('상위 장치 대조','상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.'),
('입출력 및 단자','전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.'),
('상태 검증','상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.')],
'pulse':[
('출력 식별','아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.'),
('순서 변수 식별','관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.'),
('펄스 품질','작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.')]
}

SPECIAL={
'PV01':'PV01의 8개 물리 I/O와 HMI 10개 설정은 기존 세부 매뉴얼에서 배선과 대조했다. 이번에는 R1 scraps gate 2의 원본 연결 구조를 추가했다. A/B 게이트 실제 명칭은 P&ID 상세도와 전기 입력·출력 회로를 함께 확인한다.',
'PV02':'PV02는 PV01과 다른 상태 변수·센서·출력을 가진다. A 개방/폐쇄 I9.4/I9.5, B 개방/폐쇄 I9.6/I9.7, EV04/05 출력 Q5.4/Q5.5를 백업 심볼과 대조한다. PV01의 시간값이나 순서식을 복사하지 않는다.',
'MV04':'M18A/M18B 위치 입력 IW324/IW326과 개방/폐쇄 출력 Q2.1/Q2.2가 남아 있다. Analog input conversion에는 MV04 관련 입력을 MC04 전류로 사용하는 참조도 있어, 회로 라벨과 현재 프로그램 목적을 별도 확인해야 한다.',
'MV06':'P&ID의 LS34/LS35와 백업의 LS40/LS41을 서로 다른 출처 표기로 기록한다. 원본 루프에는 PSH02 기반 펄스·범위 조건과 별도 short-range 동작 네트워크가 있다.',
'FN04':'백업에는 Q17.1 start fn04와 Q4.2 spare_0(FN04 관련 옛 주석)가 공존한다. 전기 회로와 출력 사용처로 현재 실구동 채널을 확정해야 한다. 네트워크 제목 fn-02 aspirator와 실제 FN04 전류 입력도 충돌한다.',
'FN01':'베어링 TC04/TC05와 진동 ZT01의 고장·예경보 참조가 있다. preallarm 네트워크의 s5t#1h_30m은 지연 의미와 실행 조건을 원본에서 확인해야 하며, 보호 설정 권장값으로 사용하지 않는다.',
'TC05':'백업 TC05 설명에 TC04 및 -30...250°C가 섞인 문구가 있고 reserved tc05에는 다른 범위 문구가 남아 있다. 전기 FG79 센서 채널 및 현재 전송기 설정을 기준으로 대조한다.',
'RO03':'Analog input conversion 원본에는 RO03 입력 외에도 RO02에 11을 더하는 대체 계산 참조가 존재한다. 어떤 분기가 실제 실행되는지 ON/OFF 값과 원본 연결 구조로 확인한다.',
'BF01':'병렬 필터 세정 원본 네트워크에 11~90 범위를 설정하는 참조와 두 필터 허가에 따라 출력을 교대시키는 비교기가 있다. EV 번호가 순서 변수 값과 항상 같다고 가정하지 않는다.',
'BF02':'BF02 허가 네트워크에 DP02 값과 DP01 임계값 명칭이 함께 등장한다. 공용 계수인지 오기인지 현재 설정과 원본 연결을 확인해야 한다.',
'BR01':'현재 자료는 외부 버너의 PLC 인터페이스와 일반 제어 블록을 제공한다. 상세 안전 회로 및 버너 자체 제어 시퀀스의 실제 내용은 제조사 버너 도면으로 확정한다.',
'CLIENT-CL19':'원본에는 Primary shredder run 입력을 motor_client_19_fault와 연결하는 네트워크가 있다. 명칭만으로 고장 입력의 방향을 결정하지 말고 접점 극성과 외부 신호 계약을 확인한다.',
'SC12':'전기 FG29는 SPARE이며 PLC Motors 1에는 sc12 deleted 제목과 잔존 I1.3/Q0.7이 있다. 이는 삭제된 네트워크라는 제목을 뜻하며, 검색 문서 자체가 삭제 상태라는 뜻과 구분한다.',
'PV04':'I10.5/I10.6, Q5.7 및 현장 입력 I10.7은 잔존한다. 전기 SPARE 및 pv04 deleted 제목 때문에 현재 자동 운전 대상이라고 확정할 수 없다.'
}

test_specs={
'motor':[('정상 기동','준비·피드백 조건 정상, 운전 요청 ON','관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인'),('기동 피드백 없음','기동 요청 후 피드백 미발생','백업의 고장 검출 경로·시간·출력 결과와 대조'),('운전 중 인버터/피드백 고장','운전 중 고장 입력 또는 피드백 변경','정지/알람/상위 영향은 해당 원본 네트워크로 판정'),('유지보수·상위 허가 없음','허가 입력 하나씩 해제','허가 조건에 따른 요청과 실제 출력의 관계 확인'),('복귀·전원 재시작','고장 해제, Reset, 재시작','잔존 요청·기억·초기화 처리 확인')],
'motorvalve':[('개방·폐쇄','각 방향 요청을 분리 주입','출력 방향·끝 리미트 조건·반대 출력 상태 대조'),('동시 요청','열림/닫힘 요청 동시 ON','원본 상호 배제 동작 검증'),('중간 위치','양 끝 리미트 0, 엔코더 중간 값','위치 환산·허용 방향·고장 시간 검증'),('리미트 모순','열림/닫힘 리미트 동시 1','경보·출력 반응을 원본으로 검증'),('자동/수동 전환','자동 제어 중 수동 요청 변경','요청 우선순위와 잔존 출력 검증'),('전원 복귀·교정','카운트 저장·재시작·교정 요청','원점 설정과 저장값 사용 경로 확인')],
'gate':[('정상 위치 전환','닫힘→중간→열림','I/기억 비트/HMI 상태/Q 경로 확인'),('위치 모순','열림·닫힘 모두 1','원본 경보·진행 조건 확인'),('도달 실패','출력 요청 후 위치 입력 미도달','타이머·알람·다음 단계 차단 확인'),('공기/현장 요청','저압·현장 셀렉터 상태 변경','공통 허가·현장 우선순위 대조'),('전원 복귀','초기/중간 위치로 재시작','기억과 요청의 초기화 및 재순서 확인')],
'sensor':[('정상값','여러 원시값/스위치 상태','환산값·단위·HMI 대응 확인'),('단선·범위 초과','최소·최대·이탈 원시값','OFR/고장/대체값 처리 확인'),('경보 경계','각 경계 앞/같음/뒤 값','비교기·지연·히스테리시스 확인'),('시험/선택 조건','시험 입력과 선택 채널 변경','실제 입력과 대체값의 우선순위 확인')],
'filter':[('세정 허가','SC/VR·차압·BF_RUN 변경','두 필터 허가를 각각 확인'),('전체 펄스 순서','순서 변수 전 범위','80개 EV 출력과 비교기 상수 매핑 확인'),('펄스/휴지','작업/휴지 설정 변경','단계·주기·중복 출력 검증'),('차압 경계','DP 임계값 전후','허가·시간 계수의 실제 분기 확인'),('온도/배출 고장','온도와 SC/VR 고장 입력 변경','PV14·정지/경보 경로 확인')],
'client':[('Handshake 정상','준비→허가→운전 응답','번호·I/O 방향·지연 확인'),('외부 고장','정상 상태에서 외부 신호 변경','접점 극성·알람 유지·재허가 확인'),('신호 누락','준비·피드백·통신 상태 누락','고장 검출 및 HMI 표시 확인'),('복귀','고장 해제·Reset·요청 유지/해제','재기동 조건과 잔존 요청 확인')],
'burner':[('정상 인터페이스','버너 준비·허가·운전 응답','외부 상태와 PLC 신호 계약 대조'),('락아웃','버너 락아웃 입력','원격 출력·알람·Reset 경로 확인'),('온도 선택','TC01/TC02 선택 및 고장','PID 측정값과 선택 조건 확인'),('변조/제한','가스·공기 요구값과 한계 변경','비율·출력 범위·피드백 확인'),('압력/허가 누락','압력·블로어·온도 허가 변경','원본 출력 차단 경로 대조')],
'nitrogen':[('요청·준비','탱크 준비/주입 요청 변경','공통 Q와 외부 릴레이/타이머 동작 대조'),('복귀','요청 해제·준비 해제','개별 밸브 결과는 외부 회로 모델과 대조')],
'heater':[('허가 정상/상실','FN05·온도 허용·요청 변경','Q 출력과 피드백/고장 대조'),('과온·복귀','과온·Reset 조건 변경','허가 해제와 재가열 조건 확인')],
'software':[('데이터 추적','원시값 및 선택 조건 변경','논리 명칭의 입력/출력 관계 확인')],
'passive':[('공정 이상 모델','막힘·누설·퇴적을 연관 신호로 모델링','본체 직접 I/O가 없으면 연관 장치 영향으로 판정')],
'component':[('정상/고장','상위 요청과 구성품 응답 변경','독립 또는 공통 I/O 경로와 상위 조건 확인')],
'pulse':[('개별 펄스','해당 비교기 조건 주입','실제 Q 주소·펄스 폭·이웃 채널 오동작 확인')]
}

all_tests=[];checks=[]
for d in devices:
    d['tests']=[]
    for j,(name,stimulus,expected) in enumerate(test_specs[d['kind']],1):
        t=dict(id=f"{d['id']}-SIM-{j:02}",device=d['id'],name=name,stimulus=stimulus,expected=expected,status='설계·미실행',model='원본 PLC 논리 대조가 필요한 시험안')
        d['tests'].append(t);all_tests.append(t)
    fields=[('식별/실물','도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정'),('제어/데이터','원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조'),('시뮬레이션','위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록')]
    if d['physical']:fields.append(('전기 배선','현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증'))
    if d['hmi']:fields.append(('HMI/통신','HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증'))
    if d['note']:fields.append(('불일치/특이점',d['note']))
    for j,(topic,work) in enumerate(fields,1):checks.append(dict(id=f"{d['id']}-V-{j:02}",device=d['id'],topic=topic,work=work,status='확인 대기',evidence=''))

# Archive source provenance; originals remain unchanged.
for src,dst in [(PV/'sources/PID_1684n002I.pdf',ROOT/'sources/PID_1684n002I.pdf'),(PV/'sources/Electrical_Rev2.pdf',ROOT/'sources/Electrical_Rev2.pdf'),(BASE/'hmi_plc_tags.csv',ROOT/'sources/hmi_plc_tags.csv'),(BASE/'live_index.json',ROOT/'sources/live_index.json'),(BASE/'block_summary.json',ROOT/'sources/block_summary.json'),(BASE/'manual-manual.md',ROOT/'sources/existing-website-manual.md'),(BACKUP/'GME_20250506.zap18',ROOT/'sources/GME_20250506.zap18'),(BACKUP/'GME_20250605/System/PEData.plf',ROOT/'sources/PEData.plf'),(PV/'assets/HMI_DECOATER.png',ROOT/'assets/HMI_DECOATER.png'),(Path('/private/tmp/gme-pid-review-20261007/landscape.png'),ROOT/'assets/PID-landscape.png')]:
    if src!=dst:shutil.copy2(src,dst)
dump(ROOT/'sources/electrical-page-text.json',pages)
source_manifest=[dict(file=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted((ROOT/'sources').glob('*')) if p.is_file() and p.name!='source-manifest.json']
dump(ROOT/'sources/source-manifest.json',source_manifest)

def lname(e):return e.tag.rsplit('}',1)[-1]
identifier_declarations=json.loads((DECODE/'identifier-declarations.json').read_text())
id_lookup=collections.defaultdict(list)
for ident in identifier_declarations:id_lookup[(ident['uid'],ident['rid'])].append(ident)
def block_name(p,n):
    code=n['index_code'].replace('"','').casefold()
    nodes=[p]+list(p)
    names=set()
    for node in nodes:
        uid,rid=node.get('UId'),node.get('RefId')
        for candidate in id_lookup[(uid,rid)]:
            if candidate['nid']==n.get('inferred_original_nid') and candidate['name'].casefold() in code:
                names.add(candidate['name'])
    return next(iter(names)) if len(names)==1 else 'RefId '+str(p.get('RefId','?'))

def action_conditions(parts,wires,refnames):
    """Static path expansion for contacts, OR/AND, comparators and actions.

    Unknown calls/edges remain explicit opaque terms. This is a reading aid,
    not a compiler, timing model or proof of complete program behaviour.
    """
    pmap={p.get('UId'):p for p in parts}; pinmap=collections.defaultdict(list)
    for w in wires:
        for e in w:
            if lname(e)=='PCon':pinmap[(e.get('UId'),e.get('PinName'))].append(w)
    def combine(op,values):
        values=list(dict.fromkeys(values))
        if op=='AND':values=[x for x in values if x!='POWER']
        if not values:return 'POWER' if op=='AND' else '미연결'
        return values[0] if len(values)==1 else '('+(' '+op+' ').join(values)+')'
    def pin(uid,name,visited):
        values=[]
        for w in pinmap[(uid,name)]:
            if any(lname(e)=='Powerrail' for e in w):values.append('POWER')
            for e in w:
                if lname(e)=='OCon':values.append(refnames.get(e.get('UId'),'ORef UID '+e.get('UId')))
                if lname(e)=='PCon' and (e.get('UId'),e.get('PinName'))!=(uid,name) and re.fullmatch(r'out\d*|eno|q',e.get('PinName',''),re.I):
                    values.append(out(e.get('UId'),e.get('PinName'),visited))
        return combine('OR',values) if values else '미해석 핀 '+uid+'.'+name
    def out(uid,name,visited):
        if uid in visited:return '순환 참조 UID '+uid
        if uid not in pmap:return '미해석 Part '+uid+'.'+name
        p=pmap[uid];gate=p.get('Gate') or lname(p);v=visited|{uid}
        if gate=='Contact':
            operand=pin(uid,'operand',v)
            if any(lname(e)=='Negated' and e.get('PinName')=='operand' for e in p):operand='NOT ['+operand+']'
            return combine('AND',[pin(uid,'in',v),operand])
        if gate in ('O','A'):
            names=sorted({key[1] for key in pinmap if key[0]==uid and re.fullmatch(r'in\d*',key[1])})
            return combine('OR' if gate=='O' else 'AND',[pin(uid,x,v) for x in names])
        if gate in ('Eq','Ne','Gt','Ge','Lt','Le'):
            op={'Eq':'=','Ne':'!=','Gt':'>','Ge':'>=','Lt':'<','Le':'<='}[gate]
            expr='['+pin(uid,'in1',v)+' '+op+' '+pin(uid,'in2',v)+']'
            return combine('AND',[pin(uid,'pre',v),expr]) if (uid,'pre') in pinmap else expr
        if gate=='Not':return 'NOT ['+pin(uid,'in',v)+']'
        return gate+' UID '+uid+'.'+name+' (블록 동작 확인)'
    rows=[]
    for p in parts:
        uid=p.get('UId');gate=p.get('Gate') or lname(p)
        if gate in ('Coil','SCoil','RCoil','SdCoil'):
            condition=pin(uid,'in',set())
            target=pin(uid,'operand',set())
            behavior={'Coil':'조건에 따른 Coil 기록','SCoil':'조건 성립 시 Set','RCoil':'조건 성립 시 Reset','SdCoil':'시간 동작 SdCoil; 타이머 의미 추가 확인'}[gate]
            negated=[e.get('PinName','') for e in p if lname(e)=='Negated']
            if negated:behavior+=' / Negated 핀 '+', '.join(negated)+'의 출력 극성 확인'
            parameter=pin(uid,'value',set()) if gate=='SdCoil' else ''
            rows.append([uid,gate,target,condition,behavior+(' / 시간 인자 '+parameter if parameter else '')])
        elif gate=='Move':
            target_pins=sorted(key[1] for key in pinmap if key[0]==uid and re.fullmatch(r'out\d+',key[1]))
            targets=', '.join(pin(uid,key,set()) for key in target_pins)
            rows.append([uid,gate,targets,pin(uid,'en',set()),'Move 입력 '+pin(uid,'in',set())])
    return rows

def network_diagram(n,parts,wires,refnames):
    # Connectivity diagram, deliberately labelled as a redraw rather than a TIA screenshot.
    pmap={p.get('UId'):p for p in parts}
    bindings=collections.defaultdict(list); edges=[]
    for w in wires:
        pins=[e for e in w if lname(e)=='PCon']; ops=[e for e in w if lname(e)=='OCon']
        for pin in pins:
            for op in ops:bindings[pin.get('UId')].append(pin.get('PinName')+': '+refnames.get(op.get('UId'),'Ref@'+op.get('UId','?')))
        if any(lname(e)=='Powerrail' for e in w):
            edges.extend(('POWER',p.get('UId'),w.get('UId')) for p in pins)
        ins=[p for p in pins if re.fullmatch(r'in\d*|en|pre',p.get('PinName',''),re.I)]
        outs=[p for p in pins if re.fullmatch(r'out\d*|eno|q',p.get('PinName',''),re.I)]
        edges.extend((a.get('UId'),b.get('UId'),w.get('UId')) for a in outs for b in ins if a.get('UId')!=b.get('UId'))
    depth={k:0 for k in pmap};depth['POWER']=-1
    for _ in range(min(len(pmap),30)):
        changed=False
        for a,b,w in edges:
            if b in depth and a in depth and depth[a]+1>depth[b] and depth[a]<20:
                depth[b]=depth[a]+1;changed=True
        if not changed:break
    cols=collections.defaultdict(list)
    for uid in pmap:cols[depth[uid]].append(uid)
    coords={};width=(max(cols,default=0)+2)*285; height=max(180,max((len(v) for v in cols.values()),default=1)*95+60)
    for col,values in cols.items():
        for row,uid in enumerate(values):coords[uid]=(70+col*285,50+row*95)
    lines=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="white"/><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#718a98"/></marker></defs>']
    for a,b,w in edges:
        if b not in coords:continue
        x2,y2=coords[b]
        if a=='POWER':x1,y1=10,y2+25
        elif a in coords:x1,y1=coords[a];x1+=240;y1+=25
        else:continue
        lines.append(f'<path d="M{x1} {y1} C{x1+30} {y1} {x2-30} {y2+25} {x2} {y2+25}" stroke="#97aeb9" stroke-width="1.4" fill="none" marker-end="url(#arrow)"><title>Wire {esc(w)}</title></path>')
    for uid,(x,y) in coords.items():
        p=pmap[uid];gate=p.get('Gate') or lname(p); neg=any(lname(e)=='Negated' for e in p)
        color='#e3f3ee' if 'Coil' in gate else '#fff3d8' if gate=='Contact' else '#eaf0f8'
        label=('NOT ' if neg else '')+gate+' · UID '+uid
        bind='; '.join(bindings.get(uid,[]))
        short=bind[:34]+('…' if len(bind)>34 else '')
        lines.append(f'<g><rect x="{x}" y="{y}" width="240" height="66" rx="5" fill="{color}" stroke="#8fa8b5"/><text x="{x+10}" y="{y+23}" font-family="sans-serif" font-size="13">{esc(label)}</text><text x="{x+10}" y="{y+47}" font-family="sans-serif" font-size="11">{esc(short)}</text><title>{esc(bind)}</title></g>')
    lines.append('</svg>');return ''.join(lines)

all_part_rows=[];all_wire_rows=[];all_action_rows=[]
for n in nets:
    xml=ET.parse(DECODE/n['xml_file']).getroot()
    container=next(e for e in xml if lname(e)=='Parts')
    parts=[e for e in container if lname(e) in ('Part','CRef','LRef')];wires=[e for e in xml.iter() if lname(e)=='Wire']
    n['parts']=len(parts)
    rnames={uid:v['name'] for uid,v in n['resolved_operands'].items()}
    refs={e.get('UId'):e.get('RefId') or '(RefId 없음)' for e in xml.iter() if lname(e)=='ORef'}
    partrows=[];wirerows=[];operandrows=[]
    for p in parts:
        pinrefs=[]
        for w in wires:
            pin=[e for e in w if lname(e)=='PCon' and e.get('UId')==p.get('UId')]
            for pinx in pin:
                for op in w:
                    if lname(op)=='OCon':
                        uid=op.get('UId');rid=refs.get(uid,'?');pinrefs.append(pinx.get('PinName')+' = '+rnames.get(uid,'RefId '+rid+' / ORef UID '+uid))
        neg=', '.join(e.get('PinName','') for e in p if lname(e)=='Negated')
        gate=p.get('Gate') or lname(p)
        if lname(p) in ('CRef','LRef'):pinrefs.insert(0,'호출 참조: '+block_name(p,n))
        row=[n['block'],n['document_id'],p.get('UId'),gate,neg,'; '.join(pinrefs)]
        all_part_rows.append(row);partrows.append([esc(x) for x in row[2:]])
    for w in wires:
        ends=[]
        for e in w:
            kind=lname(e)
            if kind=='PCon':ends.append('Part '+e.get('UId')+'.'+e.get('PinName'))
            elif kind=='OCon':ends.append('ORef '+e.get('UId')+' ('+rnames.get(e.get('UId'),'RefId '+refs.get(e.get('UId'),'?'))+')')
            else:ends.append(kind+' '+str(e.attrib))
        row=[n['block'],n['document_id'],w.get('UId'),' ↔ '.join(ends)]
        all_wire_rows.append(row);wirerows.append([esc(x) for x in row[2:]])
    for uid,rid in refs.items():
        resolved=n['resolved_operands'].get(uid)
        operandrows.append([esc(uid),esc(rid),esc(resolved['name']) if resolved else '<span class="badge">미해석 RefId</span>',esc(', '.join(resolved['identifier_files'])) if resolved else '식별 선언 원본 참조'])
    actions=action_conditions(parts,wires,rnames)
    n['actions']=actions
    all_action_rows.extend([n['block'],n['document_id']]+a for a in actions)
    filename=f"network-{n['document_id']}.html"
    svg=f"network-{n['document_id']}.svg"
    (ROOT/'networks'/svg).write_text(network_diagram(n,parts,wires,rnames))
    body='<p>'+esc(n['block'])+' · 검색 색인 순서 '+str(n['index_order'])+' · 원본 내부 NID 추정 '+esc(n.get('inferred_original_nid'))+'</p>'
    body+='<div class="source">백업 PLF 원본의 '+str(n['source_offset'])+' 바이트 위치에서 복원한 XML. 검색 문서 '+str(n['document_id'])+'의 객체 키 '+esc(n['object_key_hex'])+'와 연결했다. 이름 해석 '+str(n['resolved_operand_count'])+'/'+str(n['operand_count'])+'개. 남은 RefId는 상수 또는 미해석 참조다.</div>'
    body+='<p><a href="../sources/decoded-original/'+n['xml_file']+'">원본 연결 XML</a> · <a href="../registers/lad-parts.csv">전체 부품표</a> · <a href="../registers/lad-wires.csv">전체 연결표</a></p>'
    body+='<h2>연결 구조 다시 그리기</h2><p class="muted">원본 Part/PCon/Wire를 이용한 연결도다. TIA 화면의 래더 배치 또는 실행 결과를 재현한 그림은 아니다. 핀 연결은 아래 표와 원본 XML을 기준으로 읽는다. 노드 위에 마우스를 두면 피연산자 이름을 볼 수 있다.</p><div class="diagram"><img src="'+svg+'" alt="원본 연결 구조"></div>'
    body+='<h2>접점·코일·블록과 피연산자</h2>'+table(['Part UID','Gate','Negated 핀','연결 피연산자'],partrows)
    body+='<h2>접점 경로를 펼친 조건식</h2><p class="muted">Contact·O/A·비교기의 원본 연결을 읽기 쉽게 펼친 보조 해석이다. POWER는 전원 레일 시작을 뜻한다. 호출 블록·에지·타이머의 내부 동작과 다중 쓰기 순서는 이 표로 실행 검증하지 않았다. 미해석 핀과 RefId는 원문 연결표에서 확인한다.</p>'+table(['UID','동작','대상','원본 접점 경로','내용'],[[esc(x) for x in a] for a in actions])
    body+='<h2>원본 배선 연결</h2>'+table(['Wire UID','동일 Wire 연결 끝점'],wirerows)
    operandrows=[row+[esc(n['resolved_operands'].get(uid,{}).get('status','미해석'))] for uid,row in zip(refs,operandrows)]
    body+='<details><summary>식별자 해석 근거 '+str(len(refs))+'개</summary>'+table(['ORef UID','RefId','이름','IdentXmlPart 파일','해석 방법'],operandrows)+'</details>'
    body+='<h2>검색 코드 보조 자료</h2><p>참조 명칭을 찾기 위한 자료이며 실행 순서나 AND/OR 관계는 위 연결표로 확인한다.</p><pre>'+esc(n['index_code'])+'</pre>'
    (ROOT/'networks'/filename).write_text(page(n['title'] or n['block'],body))

csvfile('lad-parts.csv',['블록','네트워크 문서','Part UID','Gate','Negated 핀','피연산자 연결'],all_part_rows)
csvfile('lad-wires.csv',['블록','네트워크 문서','Wire UID','연결 끝점'],all_wire_rows)
csvfile('lad-conditions.csv',['블록','네트워크 문서','Part UID','동작','대상','정적 조건식','내용'],all_action_rows)

def devicebody(d):
    title=d['id']+' · '+d['name']
    b='<div class="source"><strong>'+esc(d['group'])+'</strong> · '+esc(d['status'])+'<br>'+esc(d['role'])+'</div>'
    if d['parent']:b+='<p>상위 설비: <a href="'+d['parent']+'.html">'+esc(d['parent'])+'</a></p>'
    if d['id'] in RELATED:
        b+='<p>공정/기능 연관 장치: '+', '.join('<a href="'+r+'.html">'+r+'</a>' for r in RELATED[d['id']])+'. 배관 또는 기능 관계이며 모든 장치 간 자동 인터록을 뜻하지 않는다.</p>'
    b+='<h2 id="source">도면·식별과 현재 확인 범위</h2><p>'+('P&ID '+ '<a href="../sources/PID_1684n002I.pdf#page=1">1684n002 Rev.I / 1페이지</a>. ' if d['pid'] else 'PLC·전기 자료 기준 항목. ')+fg_links(d['fgs'])+'</p>'
    if d['note'] or d['id'] in SPECIAL:b+='<div class="note">'+esc(SPECIAL.get(d['id'],''))+' '+esc(d['note'])+'</div>'
    b+='<p>관련 물리 I/O '+str(len(d['physical']))+'개, 내부 심볼 '+str(len(d['internal']))+'개, HMI 설정 '+str(len(d['hmi']))+'개, 관련 래더 '+str(len(d['networks']))+'개. 목록은 태그 참조를 연결한 자료이며 공유 신호·상위/하위 설비 참조도 포함한다. 채널의 독점 소유나 독립 설비 전용 블록 수를 뜻하지 않는다.</p>'
    b+='<h2 id="io">물리 I/O와 내부 심볼</h2>'
    if d['symbols']:
        b+=table(['구분','현재 백업 주소','원본 심볼','자료형','원본 설명 / 과거 주소','색인 근거'],[[esc('물리 I/O' if re.match(r'%[iq]',s['Address'],re.I) else '내부'),'<code>'+esc(s['Address'].upper())+'</code>',esc(s.get('Name','')),esc(s.get('Datatype','')),esc(s.get('Comment','')),esc(s['segment']+' / '+str(s['document_id']))] for s in d['symbols']])
    else:b+='<p>이 태그에 직접 연결되는 심볼 주소는 식별되지 않았다. 상위/연관 설비와 공정 조건으로 관리한다.</p>'
    b+='<p class="muted">위 주소는 백업 심볼의 Address 값이다. 옛 I/O 주소가 설명에 남아 있어 설명 문자열을 현재 주소로 사용하지 않는다. 단자·퓨즈·릴레이·모듈 배선 확정은 아래 전기 원문에서 별도로 수행한다.</p>'
    b+='<h2 id="hmi">HMI 설정 주소와 표시 의미</h2>'
    if d['hmi']:b+=table(['HMI 태그','설정 주소','Access Name','내부 ID'],[[esc(s['HMI 태그']),'<code>'+esc(s['설정 주소'])+'</code>',esc(s['Access Name']),esc(s['태그 내부 ID'])] for s in d['hmi']])
    else:b+='<p>직접 태그 이름으로 일치하는 HMI 설정은 없다. 가공·통합 상태 또는 상위 설비 화면 참조를 별도 확인한다.</p>'
    b+='<p class="muted">HMI 주소는 dde.cfg 설정값이며 PLC 물리 I/Q와 다를 수 있다. 표시색·입력값·알람 팝업은 화면 스크립트 및 온라인 값으로 추가 검증한다.</p>'
    b+='<h2 id="logic">관련 PLC 원본 래더</h2>'
    if d['networks']:
        b+=table(['블록 / 색인 순서','제목','원본 구조','태그 이름 해석','연결 자료'],[[esc(n['block'])+' / '+str(n['index_order']),esc(n['title'] or '(제목 없음)'),str(n['parts'])+' Parts / '+str(n['wires'])+' Wires',str(n['resolved_operand_count'])+'/'+str(n['operand_count']),'<a href="../networks/network-'+str(n['document_id'])+'.html">원본 연결 보기 #'+str(n['document_id'])+'</a>'] for n in d['networks']])
    else:b+='<p>직접 참조하는 래더 네트워크는 식별되지 않았다. 이 항목의 현재 제어 역할 또는 로컬 계측 여부를 확인한다.</p>'
    own_actions=[(n,a) for n in d['own'] for a in n.get('actions',[])]
    if d['kind']=='pulse':own_actions=[(n,a) for n in d['networks'] for a in n.get('actions',[]) if match(d,a[2])]
    if own_actions:
        b+='<details><summary>설비 제목이 일치하는 네트워크의 접점 조건 펼치기</summary><p class="muted">정적 읽기 보조 자료. 타이머·호출 블록·다중 쓰기 및 실제 실행 조건은 원본 연결과 TIA로 검증한다.</p>'+table(['네트워크','동작','대상','조건식','내용'],[['<a href="../networks/network-'+str(n['document_id'])+'.html">#'+str(n['document_id'])+'</a>']+[esc(x) for x in (a[1],a[2],a[3],a[4])] for n,a in own_actions])+'</details>'
    b+='<h2 id="alarm">알람·설정값 추적</h2>'
    if d['alarms']:b+=table(['블록','제목','검토 자료'],[[esc(n['block']),esc(n['title']),'<a href="../networks/network-'+str(n['document_id'])+'.html">접점 극성·Set/Reset·시간 조건</a>'] for n in d['alarms']])
    else:b+='<p>설비 이름으로 일치한 알람 전용 네트워크가 없다. 상위 설비 고장 및 일반 진단 블록의 참조를 확인한다.</p>'
    code=' '.join(n['index_code'] for n in d['networks'])
    timers=sorted(set(re.findall(r's5t#[0-9a-z_]+',code,re.I)))
    b+='<p>관련 검색 코드의 시간 상수 후보: '+esc(', '.join(timers) or '직접 상수 없음 / 설정 DB 및 타이머 인스턴스 확인')+'. 여러 설비를 포함한 공유 네트워크의 상수도 포함된다. 실제 적용 대상·접점 경로·설정 DB 값은 원본에서 확정한다.</p>'
    b+='<h2 id="work">운전 확인과 고장 진단 절차</h2><p>아래는 설비 유형에 맞춘 점검 절차안이다. 원본에서 확정한 제어 논리와 현장 절차를 대조해 승인용 문서로 발전시킨다.</p><ol>'
    for title,text in PROCEDURES[d['kind']]:b+='<li><strong>'+esc(title)+'</strong> — '+esc(text)+'</li>'
    b+='</ol>'
    if d['id']=='PV01':b+='<p><a href="../PV01-detail/PV01-manual.html">PV01 기존 배선·단자·18개 시험 세부편</a>. 해당 세부편의 검색 색인 해석 한계는 이번 원본 래더 연결 페이지와 함께 읽는다.</p>'
    children=[x for x in devices if x['parent']==d['id']]
    if children:b+='<h2>하위 구성품</h2>'+table(['ID','이름','자료 상태'],[['<a href="'+c['id']+'.html">'+c['id']+'</a>',esc(c['name']),esc(c['status'])] for c in children])
    b+='<h2 id="sim">시뮬레이터 모델과 시험 설계</h2><p>시뮬레이터는 운전 요청, 허가, 출력, 지연 응답, 고장, Reset, 초기값을 각각 저장한다. 물리 입력과 내부/HMI 상태를 분리하며, 임의로 넣은 지연·관성·공정 계수는 교육용 가정으로 표시한다. 아래 시험은 아직 실행하지 않았다.</p>'
    b+=table(['시험 ID','상황','주입 조건','확인할 결과','실행 상태'],[[esc(t['id']),esc(t['name']),esc(t['stimulus']),esc(t['expected']),esc(t['status'])] for t in d['tests']])
    b+='<h2 id="verify">확인 대장과 작업 기록</h2>'+table(['ID','항목','확인 작업','상태'],[[esc(c['id']),esc(c['topic']),esc(c['work']),esc(c['status'])] for c in checks if c['device']==d['id']])
    b+='<p>작업 기록에는 장치 ID, 도면 FG/PDF 페이지, 원본 네트워크 문서 ID, 전/후 값, 실제 단자·코일·센서 확인, 증거 사진, 조치와 검증자·일시를 함께 남긴다.</p>'
    if d['fgs']:
        b+='<details><summary>관련 전기 회로의 추출 원문</summary><p class="muted">PDF 텍스트 추출은 위치 순서가 바뀔 수 있다. 배선·교차참조는 원본 PDF 시각 확인을 기준으로 한다.</p>'
        for fg in d['fgs']:
            b+='<h3>FG '+str(fg)+' / PDF '+str(pdfpage(fg))+'</h3><pre>'+esc(pageby[pdfpage(fg)])+'</pre>'
        b+='</details>'
    return b

toc='<aside class="toc">'+''.join('<a href="#'+id+'">'+name+'</a>' for id,name in [('source','도면·확인 범위'),('io','I/O·내부 심볼'),('hmi','HMI 설정'),('logic','원본 래더'),('alarm','알람·설정'),('work','운전·진단 절차'),('sim','시뮬레이터 시험'),('verify','확인 대장')])+'</aside>'
for d in devices:(ROOT/'devices'/f"{d['id']}.html").write_text(page(d['id']+' · '+d['name'],devicebody(d),nav=toc))

# Preserve the detailed PV01 work, with a visible note pointing to new evidence.
if (ROOT/'PV01-detail').exists():shutil.rmtree(ROOT/'PV01-detail')
shutil.copytree(PV,ROOT/'PV01-detail',ignore=shutil.ignore_patterns('sources','bundle-manifest.json','verification-result.json','build-review.py'))
(ROOT/'PV01-detail/sources').mkdir()
for f in ('PID_1684n002I.pdf','Electrical_Rev2.pdf'):
    shutil.copy2(ROOT/'sources'/f,ROOT/'PV01-detail/sources'/f)
for f in ('pv01-evidence.json','hmi_plc_tags.csv','existing-manual.md','source-manifest.json'):
    if (PV/'sources'/f).exists():shutil.copy2(PV/'sources'/f,ROOT/'PV01-detail/sources'/f)
p=ROOT/'PV01-detail/PV01-manual.html'
t=p.read_text();t=t.replace('<body>','<body><div style="background:#eaf5f2;padding:18px"><strong>2026-10-07 원본 래더 추가:</strong> 이 문서는 기존 배선 세부편입니다. <a href="../devices/PV01.html">426개 원본 래더 연결을 반영한 전체 설비 PV01 장</a>을 함께 읽으세요.</div>',1);p.write_text(t)

equipment_rows=[[d['id'],d['name'],d['group'],d['kind'],d['parent'],d['status'],plainfg(d['fgs']),len(d['physical']),len(d['internal']),len(d['hmi']),len(d['networks']),d['role'],d['note']] for d in devices]
csvfile('equipment.csv',['ID','설비명','영역','유형','상위 설비','자료 상태','전기 회로','물리 I/O','내부 심볼','HMI 태그','관련 래더','역할','특이점'],equipment_rows)
csvfile('plc-symbols.csv',['원본 심볼','백업 주소','자료형','설명','색인 세그먼트','문서 ID'],[[s.get('Name',''),s['Address'],s.get('Datatype',''),s.get('Comment',''),s['segment'],s['document_id']] for s in symbols])
csvfile('equipment-io.csv',['설비 ID','원본 심볼','백업 주소','자료형','설명','문서 ID'],[[d['id'],s.get('Name',''),s['Address'],s.get('Datatype',''),s.get('Comment',''),s['document_id']] for d in devices for s in d['symbols']])
csvfile('equipment-hmi.csv',['설비 ID','HMI 태그','설정 주소','Access Name','내부 ID'],[[d['id'],s['HMI 태그'],s['설정 주소'],s['Access Name'],s['태그 내부 ID']] for d in devices for s in d['hmi']])
csvfile('equipment-networks.csv',['설비 ID','블록','색인 순서','제목','문서 ID','원본 XML','PLF 위치','Parts','Wires','해석 피연산자','전체 피연산자'],[[d['id'],n['block'],n['index_order'],n['title'],n['document_id'],n['xml_file'],n['source_offset'],n['parts'],n['wires'],n['resolved_operand_count'],n['operand_count']] for d in devices for n in d['networks']])
csvfile('simulation-tests.csv',['시험 ID','설비 ID','상황','주입 조건','확인할 결과','상태'],[[t['id'],t['device'],t['name'],t['stimulus'],t['expected'],t['status']] for t in all_tests])
csvfile('verification.csv',['확인 ID','설비 ID','항목','확인 작업','상태','증거'],[[c['id'],c['device'],c['topic'],c['work'],c['status'],c['evidence']] for c in checks])
all_network_rows=[]
for block in blocks:
    for i,n in enumerate(block['networks'],1):
        mapped=next((x for x in nets if x['segment']==n['segment'] and x['document_id']==n['doc']),None)
        title=n.get('title',n.get('Network title',''))
        lang='LAD' if mapped else '색인/빈 네트워크/기타 언어'
        code=n.get('LADFBD Code',n.get('SCL Code',n.get('STL Code','')))
        all_network_rows.append([block['name'],i,title,n['doc'],lang,mapped['xml_file'] if mapped else '',code])
csvfile('all-networks.csv',['블록','색인 순서','제목','문서 ID','구분','원본 XML','검색 코드'],all_network_rows)
csvfile('electrical-pages.csv',['FG','PDF 페이지','회로 제목'],[[fg,pdfpage(fg),pageby[pdfpage(fg)].splitlines()[0]] for fg in list(map(str,range(1,263)))+['5A','180A','180B']])

unassigned_s=[s for s in symbols if not any(s in d['symbols'] for d in devices)]
unassigned_h=[h for h in hmi if not any(h in d['hmi'] for d in devices)]
csvfile('unassigned-plc-symbols.csv',['심볼','주소','자료형','설명','검토 상태'],[[s.get('Name',''),s['Address'],s.get('Datatype',''),s.get('Comment',''),'공통/예비/설비 미지정 참조 검토'] for s in unassigned_s])
csvfile('unassigned-hmi.csv',['HMI 태그','주소','검토 상태'],[[h['HMI 태그'],h['설정 주소'],'공통/화면 요소/설비 미지정 참조 검토'] for h in unassigned_h])
dump(ROOT/'registers/equipment.json',[{k:v for k,v in d.items() if k not in ('symbols','hmi','networks','own','alarms','physical','internal','tests')} for d in devices])

CONFLICTS=[
('BASELINE','백업 파일명과 내부 프로젝트 날짜','GME_20250506.zap18 내부 GME_20250605.ap18; 2026-10-01은 보관 일자','온라인 PLC 및 현재 엔지니어링 프로젝트와 비교'),
('POWER','설치 전력·도면 세대','2013 P&ID 355kW / 2024~2025 전기 463kW','설치·개조 내역과 명판 기준 확정'),
('VOLTAGE','주전원 표기','전기 표지 440Vac / 일부 인덱스 제목 400V','현장 공급 및 실제 회로/명판 확인'),
('PV01-LS02','닫힘 센서 예비 표기','FG70에 LS02, PLC I8.7, FG124 SPARE 표기','단자와 현재 입력 채널 실제 사용 확인'),
('ADDRESS','현재 주소와 과거 주석','심볼 Address와 설명에 남은 옛 E/A 주소가 다름','Address 및 실제 모듈/배선으로 대조'),
('MC05-SC12-PV04','삭제/예비 및 잔존 I/O','도면/심볼에는 존재, Motors 1 일부 deleted 제목','실물·현재 네트워크·사용 상태 확정'),
('FN01-FAN','냉각팬 삭제/예비','FG54 SPARE, I4.5/Q3.5 잔존','현재 연결 및 필요성 확인'),
('MV04-MC04','아날로그 입력 목적 충돌','MV04 위치 M18A/IW324를 MC04 전류 변환에서 참조','현장 배선·모듈 채널·사용 프로그램 목적 확인'),
('FN04','실구동 출력 및 제목','Q17.1 start fn04 / Q4.2 옛 FN04 주석; 변환 제목 FN02','사용처와 전기도면 기준 현재 채널 확인'),
('MV06-LS','리미트 번호 변경','P&ID LS34/35 / 백업 LS40/41','변경 이력과 실제 센서/단자 확인'),
('CL-NAMESPACE','같은 CL 번호의 다른 장치','P&ID 실린더 CL01~12 / 외부 모터 CL01~19 일부 채널','CYL-CL / CLIENT-CL ID 유지'),
('TC05','베어링 채널·범위 문구','TC04/TC05·범위 설명 혼재','전송기 범위와 AI 채널/환산 계수 확인'),
('RO03','산소 대체 계산','실제 입력 외 RO02+11 참조','원본 분기·시험 비트·현재 값 확인'),
('BF02-DP','차압 계수 이름','DP02와 DP01 임계값 참조 혼재','공용 설정 의도와 실제 적용 확인'),
('CLIENT19','고장/운전 신호 의미','Primaryshredder run을 fault 알람에 연결','외부 신호 정상 극성과 원본 접점 확인'),
('BR01','버너 상세 도면 경계','P&ID에서 버너 별도 DWG 참조','제조사 버너 도면/안전 제어 순서 확보'),
('SOURCE-XML','복원 해석과 TIA 결과','426 LAD 원본 XML 복원; 상수/일부 참조 이름 미해석','TIA에서 프로젝트 복원·블록 비교·컴파일·오프라인 실행 검증'),
('PID-TM','과거 위치 계측과 현재 엔코더','P&ID ZT02~06 / TM·엔코더 카운트 사용','실제 위치 계측 방식/보정 절차 확인'),
]
csvfile('source-conflicts.csv',['ID','확인 항목','자료 내용','다음 검증'],CONFLICTS)

scope_counts=collections.Counter(d['group'] for d in devices)
parents=sum(d['kind'] not in ('component','pulse') for d in devices)
components=len(devices)-parents
stats=dict(equipment_items=len(devices),main_chapters=parents,component_chapters=components,
    categories=dict(scope_counts),plc_symbols=len(symbols),physical_symbols=sum(bool(re.match(r'%[iq]',s['Address'],re.I)) for s in symbols),
    hmi_settings=len(hmi),indexed_blocks=len(blocks),indexed_networks=len(all_network_rows),
    original_lad_networks=len(nets),lad_parts=len(all_part_rows),lad_wires=len(all_wire_rows),static_action_paths=len(all_action_rows),
    simulation_test_designs=len(all_tests),simulation_tests_executed=0,verification_rows=len(checks),
    source_conflicts=len(CONFLICTS),unassigned_plc_symbols=len(unassigned_s),unassigned_hmi_settings=len(unassigned_h),
    decoded=decode_stats)
dump(ROOT/'registers/coverage.json',stats)

common='''<h2 id="scope">자료와 적용 범위</h2><p>사용자가 제공한 P&ID·전기도면과 GitHub 프로젝트의 PLC 백업·기존 홈페이지 자료를 함께 정리한 전체 설비 검토본이다. 물리 설비, 외부 연동, 계측, 예비 장치 및 하위 구성품을 모두 목록에 포함했다. 자료에서 식별한 항목의 범위를 말하며 현장 전체 실물의 최종 인수 목록은 아니다.</p><p>P&ID: 1684n002 Rev.I, 2013년. 전기: IMPIANTO COREA DEFINITIVO REVISIONE 2, 265페이지. PLC: GME_20250506.zap18 내부 GME_20250605.ap18, V18.0.1.0. GitHub 분석 기준: 2ebff1273f586f3355a2ba8fb91d701ac94e4a5e. HMI: InTouch dde.cfg 782개 설정 및 DECOATER 화면.</p><h2 id="method">백업 원본 래더를 읽은 방법</h2><p>ZAP18에서 원본 PEData.plf를 읽고 압축된 XML 조각과 분할 스트림을 복원했다. 살아 있는 검색 색인의 객체 키를 PLF와 대조하여 426개 LAD 네트워크를 각각 다른 원본 FlgNet XML에 연결했다. 접점·Negated 핀·Coil/SCoil/RCoil/SdCoil·블록·Wire 구조를 읽을 수 있다.</p><p>검색 코드에 나타나는 이름과 원본 식별 선언의 UID/RID 및 내부 NID가 일치하는 참조만 이름을 붙였다. 미해석 RefId와 상수는 원본 선언 파일에 보존했다. 연결도는 XML 구조를 다시 그린 것이다. TIA 프로젝트 복원·컴파일·PLC 현재 프로그램 비교 또는 실제 제어 실행은 아직 수행하지 않았다.</p><h2 id="read">설비별 매뉴얼을 읽는 순서</h2><ol><li>설비 ID와 도면·자료 상태를 확인한다. 동일 CL 번호의 실린더와 외부 모터는 다른 ID를 사용한다.</li><li>물리 I/O와 HMI 주소를 분리해 읽고 현재 Address와 옛 주석 주소를 비교한다.</li><li>관련 원본 래더의 부품표와 Wire 표에서 접점 극성·분기·Set/Reset·시간/상수 연결을 확인한다.</li><li>알람·설정값과 설비 유형별 진단 절차를 검토한다.</li><li>시뮬레이터 시험 설계를 원본 동작과 대조해 기대 결과를 확정하고 확인 대장에 실행 증거를 남긴다.</li></ol><h2 id="workflow">공통 운전·작업 기록</h2><p>자동 기동·정지 순서는 Auto start motors, Main, Motors 1, Burner control, Filter, R1 scraps gate 2, Valve control loop 및 주기 OB를 함께 읽는다. 검색 목록의 줄 순서를 실제 운전 순서로 사용하지 않는다. 같은 신호가 여러 네트워크에서 갱신될 때 호출 조건·주기·쓰기 순서를 확인한다.</p><p>작업 전에는 장치 ID·현재 운전 모드·활성 요청·알람·상위/하위 설비·해당 전기 회로·사용 프로젝트를 기록한다. 물리 배선 또는 기계 점검은 현장 작업 절차에 따라 에너지를 격리하고 잔류 공압·열·회전 상태를 확인한 뒤 수행한다. 복귀는 배선/기구 상태 확인, 전원·공기 복구, 알람 원인 해소, Reset, 요청 상태 확인, 제한 운전 검증을 각각 기록한다.</p><p>이력은 설비 ID, 시각, 도면 FG/PDF 페이지, 네트워크 ID, 요청/허가/출력/피드백/알람의 전후 값, 실제 단자·계측 결과, 증거 사진, 조치와 검증자로 구성한다. 백업에는 프로젝트·자료 해시와 변경 이유를 남겨 원본과 개정본을 함께 추적한다.</p><h2 id="program">PLC 관리 프로그램과 HMI 시뮬레이터의 구현 기준</h2><p>이번 결과물은 매뉴얼·원본 탐색기·CSV/JSON 대장이다. 운전 시뮬레이터 실행 엔진이나 실제 PLC 통신 제어 기능은 아직 구현하지 않았다. 다음 구현은 설비 ID를 중심으로 원본 도면, I/O, HMI, 알람, 작업 이력과 시험 결과를 연결한다.</p><ol><li>자료 계층: 원본 파일 해시, 개정, 전기 FG/PDF 매핑, 네트워크 객체 키, 확인 상태를 보존한다.</li><li>장치 계층: 물리 입력·명령 출력·내부 기억·가공 HMI·설정·알람을 별도 필드로 저장한다.</li><li>시뮬레이터 계층: 스캔마다 입력 샘플링, 원본 조건 평가, 내부 상태·타이머 갱신, 출력 갱신, 장치 응답 모델, HMI 상태를 순서대로 기록한다. 주기 OB·Set/Reset·중복 쓰기와 재시작 초기화도 모델링한다.</li><li>HMI 계층: 기존 DECOATER 배치를 참조하고 설비 클릭 시 주소·원본 로직·알람 원인·도면·점검 기록을 연결한다. 교육용 공정 가정과 원본 PLC 동작의 검증 상태를 표시한다.</li><li>시험 계층: 각 시험의 입력·시간·기대 결과·관찰 결과·근거 네트워크·모델 버전을 저장한다. 결과가 미실행인 경우 합격으로 표시하지 않는다.</li><li>현장 연동: 주소·자료형·실제 CPU 프로그램과 통신 계약을 검증한 뒤 읽기 화면 및 제어 기능을 단계별로 검토한다.</li></ol>'''
common=common.replace('미해석 RefId와 상수는 원본 선언 파일에 보존했다.', '상수는 UID/RID/NID와 인접 선언·검색 값이 일치하면 후보 이름을 붙이고 해석 방법을 별도 표시했다. 미해석 RefId는 원본 선언 파일에 보존했다. Contact·O/A·비교기 경로를 펼친 조건식은 정적 읽기 보조 자료이며 실행 엔진으로 사용하지 않는다.')
common=common.replace('PLC 관리 프로그램과 HMI 시뮬레이터의 구현 기준', '매뉴얼·수리·프로그램 분석과 개선을 위한 구현 기준')

def network_index_html():
    rows=[]
    for b,o,title,doc,lang,xml,code in all_network_rows:
        rows.append([esc(b),str(o),esc(title),str(doc),'<a href="networks/network-'+str(doc)+'.html">원본 LAD</a>' if xml else esc(lang)])
    return '<h2>PLC 네트워크 전체 목록</h2><p>426개 원본 LAD 및 빈 네트워크/기타 언어의 검색 문서를 함께 제공한다. 빈 제목도 제외하지 않았다.</p>'+table(['블록','색인 순서','제목','문서 ID','자료'],rows)
(ROOT/'plc-networks.html').write_text(page('PLC 전체 네트워크',network_index_html(),prefix=''))

def reference_page(title,headers,rows,rawfile):
    body='<p>원본 설정 또는 검색 색인 자료다. 온라인 현재 값은 별도 검증한다. <a href="'+rawfile+'">전체 대장 다운로드</a></p><div class="controls"><input id="ref-search" aria-label="태그·주소 검색" placeholder="태그 또는 주소 검색"></div><p id="ref-count" class="muted"></p><div class="table-wrap"><table><thead><tr>'+''.join('<th>'+esc(h)+'</th>' for h in headers)+'</tr></thead><tbody>'
    body+=''.join('<tr class="ref-row" data-search="'+esc(' '.join(map(str,row)).lower())+'">'+''.join('<td>'+esc(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
    body+='''<script>const input=document.getElementById('ref-search'),rows=[...document.querySelectorAll('.ref-row')];function filter(){let q=input.value.trim().toLowerCase(),n=0;for(let r of rows){let ok=!q||r.dataset.search.includes(q);r.hidden=!ok;if(ok)n++}document.getElementById('ref-count').textContent=n+' / '+rows.length+'개'}input.addEventListener('input',filter);filter();</script>'''
    return page(title,body,prefix='')
(ROOT/'hmi-tags.html').write_text(reference_page('HMI 전체 설정 782개',['HMI 태그','설정 주소','Access Name','내부 ID'],[[h['HMI 태그'],h['설정 주소'],h['Access Name'],h['태그 내부 ID']] for h in hmi],'sources/hmi_plc_tags.csv'))
(ROOT/'plc-symbols.html').write_text(reference_page('PLC 전체 심볼 789개',['심볼','백업 주소','자료형','원본 설명','문서 ID'],[[s.get('Name',''),s['Address'],s.get('Datatype',''),s.get('Comment',''),s['document_id']] for s in symbols],'registers/plc-symbols.csv'))

rowhtml=''
for d in devices:
    search=' '.join([d['id'],d['name'],d['group'],d['parent'],d['status'],d['role']]+[s.get('Name','')+' '+s['Address'] for s in d['symbols']]+[h['HMI 태그'] for h in d['hmi']]).lower()
    rowhtml+='<tr data-search="'+esc(search)+'" data-group="'+esc(d['group'])+'"><td><a href="devices/'+d['id']+'.html"><strong>'+d['id']+'</strong></a></td><td>'+esc(d['name'])+'</td><td>'+esc(d['group'])+'</td><td>'+esc(d['parent'] or '—')+'</td><td>'+esc(d['status'])+'</td><td>'+str(len(d['physical']))+'</td><td>'+str(len(d['hmi']))+'</td><td>'+str(len(d['networks']))+'</td></tr>'
catalog='<h2 id="equipment">전체 설비 목록</h2><div class="controls"><input id="search" aria-label="설비·심볼·주소 검색" placeholder="PV01, FN04, EV61, Q19.2, TC05…"><select id="group" aria-label="설비 영역"><option value="">전체 영역</option>'+''.join('<option>'+esc(g)+'</option>' for g in scope_counts)+'</select><button id="clear">초기화</button></div><p id="count" class="muted" aria-live="polite">전체 '+str(len(devices))+'개 항목</p><div class="table-wrap"><table id="equipment-table"><thead><tr>'+''.join('<th>'+esc(x)+'</th>' for x in ['ID','설비명','영역','상위','자료 상태','I/O','HMI','LAD'])+'</tr></thead><tbody>'+rowhtml+'</tbody></table></div>'
summary='<div class="grid">'+''.join('<div class="card"><strong>'+str(v)+'</strong><br>'+esc(k)+'</div>' for k,v in [('주설비·계측·외부 연동·공통 기능 장',parents),('하위 구성품·펄스 밸브 장',components),('원본 래더 네트워크',len(nets)),('시뮬레이터 시험 설계',len(all_tests))])+'</div>'
links='<p><a href="control-spec.html">전체 설비 제어 명세</a> · <a href="ALL-EQUIPMENT-MANUAL.md">통합 Markdown 매뉴얼</a> · <a href="plc-networks.html">PLC 전체 네트워크</a> · <a href="plc-symbols.html">PLC 전체 심볼</a> · <a href="hmi-tags.html">HMI 전체 설정</a> · <a href="registers/equipment.csv">설비 대장 CSV</a> · <a href="registers/verification.csv">확인 대장</a> · <a href="registers/simulation-tests.csv">시험 설계</a> · <a href="registers/source-conflicts.csv">자료 불일치 대장</a></p>'
conflict_html='<h2 id="conflicts">자료 불일치와 현장 확인 항목</h2>'+table(['ID','항목','자료 내용','다음 검증'],[[esc(x) for x in row] for row in CONFLICTS])
images='<h2 id="drawing">기본 HMI와 공정 배치</h2><figure><a href="assets/HMI_DECOATER.png"><img src="assets/HMI_DECOATER.png" alt="기존 DECOATER HMI" loading="lazy"></a><figcaption>제공된 기존 HMI 화면. 값은 촬영 당시 표시이며 현재 현장 값이 아니다.</figcaption></figure><figure><a href="assets/PID-landscape.png"><img src="assets/PID-landscape.png" alt="P&ID 전체 배치" loading="lazy"></a><figcaption>1684n002 Rev.I. 원본 PDF의 태그·개정과 함께 읽는다.</figcaption></figure>'
nav='<aside class="toc">'+''.join('<a href="#'+id+'">'+name+'</a>' for id,name in [('purpose','목적·작업 우선순위'),('equipment','전체 설비 찾기'),('scope','자료·범위'),('method','원본 래더 복원'),('read','읽는 순서'),('workflow','운전·작업 기록'),('program','관리 프로그램 기준'),('conflicts','불일치·검증'),('drawing','HMI·P&ID')])+'</aside>'
script='''<script>const s=document.getElementById('search'),g=document.getElementById('group'),rows=[...document.querySelectorAll('#equipment-table tbody tr')];function filter(){let q=s.value.trim().toLowerCase(),v=g.value,n=0;for(let r of rows){let ok=(!q||r.dataset.search.includes(q))&&(!v||r.dataset.group===v);r.hidden=!ok;if(ok)n++}document.getElementById('count').textContent=n+' / '+rows.length+'개 항목'}s.addEventListener('input',filter);g.addEventListener('change',filter);document.getElementById('clear').addEventListener('click',()=>{s.value='';g.value='';filter();s.focus()});</script>'''
(ROOT/'manual-catalog.html').write_text(page('전체 설비 통합 매뉴얼 · 원본 래더 탐색기',purpose+summary+links+catalog+common+conflict_html+images+script,prefix='',nav=nav))

# Portable Markdown contains every device, actual signal/HMI tables and direct logic locators.
md='# GME 전체 설비 통합 매뉴얼 v0.2\n\n작성일 2026-10-07. 제공자료 기준 검토본.\n\n'
md+='프로젝트 목적: 전체 설비 매뉴얼 작성, 고장 진단과 수리, PLC 프로그램 구조 파악 및 개선 검토. 전체 설비 제어 명세를 공통 기준으로 작성하고, HMI와 시뮬레이터는 탐색·진단·고장 재현·개선안 검증에 활용한다. [목적과 작업 기준](PROJECT-PURPOSE.md) · [전체 설비 제어 명세](control-spec.html)\n\n'
md+=f'총 {len(devices)}개 관리 항목: 주설비·계측·외부 연동·공통 기능 {parents}개, 하위 구성품·펄스 밸브 {components}개. 원본 LAD 네트워크 426개를 복원·연결했다. 시뮬레이션 시험안 {len(all_tests)}개는 미실행이다.\n\n'
md+='## 적용 기준과 자료\n\nP&ID 1684n002 Rev.I(2013), 전기 Rev.2(265페이지), GME_20250506.zap18 내부 GME_20250605.ap18(V18.0.1.0), GitHub 2ebff1273f586f3355a2ba8fb91d701ac94e4a5e 및 기존 HMI 설정을 기준으로 한다. 현장 현재 설치·프로그램·온라인 값을 확정한 문서는 아니다.\n\n'
md+='원본 PEData.plf에서 압축/분할 XML을 복원하고 검색 객체 키로 426개 LAD를 각각 연결했다. 접점·코일·Negated 핀·Wire 구조를 원본 자료로 제공한다. 이름은 UID/RID·NID·검색 이름 일치 시 해석했고 미해석 RefId는 보존했다. TIA 복원·컴파일·실행 검증은 별도 단계다.\n\n'
md+='## 작업 기록과 시뮬레이터 기준\n\n물리 입력, 내부 기억, HMI 가공 상태, 명령 출력, 설정값, 알람은 별도 신호로 관리한다. 설비 ID·FG/PDF 페이지·네트워크 ID·전후 값·단자/계측 결과·조치·증거·검증자·일시를 기록한다. 자동 순서와 정지는 실제 블록 호출·접점 분기·주기 OB·중복 쓰기 순서로 확인한다.\n\n시뮬레이터 모델은 입력 샘플링 → 원본 조건 평가 → 상태/타이머 갱신 → 출력 → 장치 응답 → HMI의 각 단계를 기록한다. 공정 계수·관성·응답시간을 가정한 경우 교육용 가정으로 표시한다. 시험 기대 결과는 원본 실행 결과와 대조해 확정한다. 이번 결과물에 PLC 통신 제어나 시뮬레이터 실행 엔진은 구현하지 않았다.\n\n'
md+='## 자료 불일치\n\n'+mtable(['ID','항목','자료 내용','다음 검증'],CONFLICTS)+'\n'
md+='## 전체 설비 대장\n\n'+mtable(['ID','설비명','영역','상위','자료 상태'],[[d['id'],d['name'],d['group'],d['parent'],d['status']] for d in devices])+'\n'
for d in devices:
    md+='## '+d['id']+' · '+d['name']+'\n\n'+d['role']+'\n\n자료 상태: '+d['status']+'. 상위: '+(d['parent'] or '해당 없음')+'. 전기: '+plainfg(d['fgs'])+'.\n\n'
    if d['note'] or d['id'] in SPECIAL:md+='확인할 특이점: '+SPECIAL.get(d['id'],'')+' '+d['note']+'\n\n'
    md+='### PLC 신호\n\n'
    md+=mtable(['주소','심볼','자료형','원본 설명','문서 ID'],[[s['Address'].upper(),s.get('Name',''),s.get('Datatype',''),s.get('Comment',''),s['document_id']] for s in d['symbols']]) if d['symbols'] else '직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.\n'
    md+='\n### HMI 설정\n\n'
    md+=mtable(['HMI 태그','주소','Access Name','내부 ID'],[[h['HMI 태그'],h['설정 주소'],h['Access Name'],h['태그 내부 ID']] for h in d['hmi']]) if d['hmi'] else '직접 이름으로 일치한 HMI 태그 미식별.\n'
    md+='\n### 원본 래더 참조\n\n'
    md+=mtable(['블록','색인 순서','제목','원본 연결','Parts/Wires'],[[n['block'],n['index_order'],n['title'],'[네트워크 '+str(n['document_id'])+'](networks/network-'+str(n['document_id'])+'.html)',str(n['parts'])+'/'+str(n['wires'])] for n in d['networks']]) if d['networks'] else '직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.\n'
    selected=[(n,a) for n in d['own'] for a in n.get('actions',[])]
    if d['kind']=='pulse':selected=[(n,a) for n in d['networks'] for a in n.get('actions',[]) if match(d,a[2])]
    if selected:
        md+='\n### 원본 접점 조건식\n\n원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.\n\n'
        md+=mtable(['네트워크','동작','대상','정적 조건식','내용'],[[n['document_id'],a[1],a[2],a[3],a[4]] for n,a in selected])+'\n'
    md+='\n### 점검·진단 절차안\n\n'
    for j,(title,text) in enumerate(PROCEDURES[d['kind']],1):md+=str(j)+'. '+title+': '+text+'\n'
    md+='\n### 시뮬레이터 시험 설계\n\n'+mtable(['ID','상황','주입 조건','확인할 결과','상태'],[[t['id'],t['name'],t['stimulus'],t['expected'],t['status']] for t in d['tests']])+'\n'
    md+='### 확인 대장\n\n'+mtable(['ID','항목','작업','상태'],[[c['id'],c['topic'],c['work'],c['status']] for c in checks if c['device']==d['id']])+'\n'
(ROOT/'ALL-EQUIPMENT-MANUAL.md').write_text(md)

readme=f'''# GME 전체 설비 매뉴얼 검토본

목적은 전체 설비 매뉴얼, 고장 진단·수리, PLC 프로그램 구조 파악 및 개선 검토입니다. [프로젝트 목적과 작업 기준](PROJECT-PURPOSE.md)에 산출물과 우선순위를 기록했습니다. [전체 설비 제어 명세](control-spec.html)는 이 작업과 후속 HMI·시뮬레이터 검증의 공통 기준으로 사용합니다.

index.html은 올인원 프로그램의 단일 시작 화면입니다. 설비 선택을 유지하며 매뉴얼·진단·I/O·제어 명세·래더·도면·시험·확인 대장·개선 메모를 사용합니다. 기존 검색 가능한 전체 매뉴얼은 manual-catalog.html에 보존합니다. 자세한 사용법은 ALL-IN-ONE.md에 기록합니다.

- 관리 항목 {len(devices)}개 (주설비·계측·외부 연동·공통 기능 {parents}, 하위 구성품 {components})
- 원본 LAD 네트워크 426개 / 전체 검색 네트워크 {len(all_network_rows)}개
- PLC 심볼 {len(symbols)}개 / HMI 설정 {len(hmi)}개
- 시험 설계 {len(all_tests)}개, 실행 0개 / 확인 대장 {len(checks)}건
- 자료 불일치 {len(CONFLICTS)}건

기존 PV01 세부편은 PV01-detail에 보존했고 새 원본 연결 자료는 devices/PV01.html에 추가했습니다.

sources에는 원본 PDF·ZAP18·PEData.plf·검색 자료와 복원 XML을 보존했습니다. 원본 파일 해시 및 복원 위치는 source-manifest.json과 decoded-original/network-map.json에서 확인합니다.

실행 엔진·현장 PLC 통신·현재 프로그램 일치·TIA 컴파일·시험 실행은 완료된 범위가 아닙니다. 미해석 참조·공통/예비·설비 미지정 항목은 대장에 남겼습니다.

decode-backup.py와 build-manual.py는 이번 로컬 검토 작업의 재현 스크립트입니다. 원본 자료 scratch 경로는 스크립트 상단에 지정되어 있습니다.
'''
(ROOT/'README.md').write_text(readme)
runpy.run_path(str(ROOT/'build-control-spec.py'),run_name='__main__')
print(json.dumps(stats,ensure_ascii=False,indent=2))
