# HE01 독립 원본 검토·통합 근거

2026-10-11, 로컬 기준 98f3f3d / v1.16.0. Dots 고정 abcf31c 조사 초안을 보존하고 핵심 원본을 독립 대조했다. 본체 전용 PLC 자료는 미확보이며 아래 TC03·PSH01·PSH03·댐퍼·팬·공정 알람은 주변 참고다. 전용 신호·설비 소유·현장 상태를 새로 배정하지 않았다.

독립 검토: 0491/0495/0497 환산 호출과 0528 TC03 경보의 Part/Wire/NID/RID/선언 및 HMI raw 전달. 공유 FC63·MV01·MV03·FN02·RD01·BR01은 동일 해시의 선행 검토를 재사용하고 HE01 관련 핀을 대조했다. 22개 XML의 선택 핀 범위를 검토했으며 모든 블록의 전체 의미 검토를 주장하지 않는다. PSH01 출력은 Data.Press_PC01 DB1W134, PSH03 Coeff/Zero는 DB4W220/W218이다. 이름만으로 별도 PC01 센서와 합치지 않는다.

원본 PDF10쪽을 실제 렌더 확인했다: OEM PDF76/78/107/108/109, 시공3/6/56/57, PID1. 시공57 7_1–7_10과 CANDC-CONS-C007-057, PSH03 제목 불일치, 가림6_7–6_10, HE01 구역 대 AB01 기능, MV04 철거 제외를 유지한다. 계수·단위·현행 설정·실물 동일성·현재 유로·복구는 미확정이다.

TC03 LOW/MAX는 자동 히스테리시스 해제이고 MAXMAX는 RESET_ALLARM 자기래치 해제다. LOW의 BWF RUN 발생 조건과 Reset 가지 차이, Add/Sub ENO 직렬, MAXMAX Add/비교 pre 병렬을 보존했다. 원문 200/5/50/750/−60·3초를 현재 보호값이나 권고값으로 채택하지 않는다.

UI/저장·재열기/PDF·패키지·게시 검증은 아래 조사 초안의 과거 미수행 상태와 별도 기록한다. TIA/현재 CPU/현장 복구는 수행하지 않았다.

---

# HE01(P13) 열교환기 — 원본 조사·표준화 인계 초안

> 검토용 조사 초안. HE01 본체 전용 PLC I/O·HMI·LAD·알람·타이머는 확보하지 못했다. 주변 TC03·PSH01·PSH03·MV01·MV02·MV03·FN02의 연결 근거를 본체 고유 제어로 합치지 않는다. P13↔HE01은 역할 후보이며 실물 동일성·현장 배선·현재 CPU·복구는 미확인이다.


## 0. 작업 기준과 보존 범위

- 표준: GME-STD-1.0.0, phase1 P13 / catalog_id HE01, passive / 연소·열회수 / 부모 없음.
- 조사 원본: 고정 커밋 abcf31c5030bc7ef8749ed8e869a857f2387a28a, 프로그램 v1.12.0의 all-in-one/. 조사 시점 2026-10-11 UTC. 최신 사용자 컴퓨터의 프로그램 버전·게시 상태를 대신하지 않는다.
- 공개 저장소 .agents/skills/gme-equipment-rollout/SKILL.md, WORK-STANDARD.md, WORK-ITEM-TEMPLATE.md, INVENTORY.json 및 공개 원본만 사용했다. 비공개/개인 스킬 사용을 주장하지 않는다. 모델·추론 수준은 이 조사에서 사용자 앱 설정을 직접 관측하지 못했으므로 미확인이다.
- 원본 저장소·공통 코드·버전·대장·배포·운영 기록은 편집하지 않았다. 자체 extracts/HE01/와 본 초안만 작성했다. 유일한 로컬 편집자가 검토 후 통합·검증·게시한다.
- 시뮬레이터 작성/수정/생성/실행/행동 시험, 실제 PLC/현장/보호값, SEJIN 운영 자료 변경은 수행하지 않았다. 원본 시공 PDF는 기존 공개 참고자료로만 읽었다.
- preflight: inventory_matches=true. 전체248 ID, 우선23행, 대응18, 제외90, 다른 공정2, 제외 부모 하위 보류7, phase2 133을 유지한다. phase2는 이번 로컬 목표 범위 제외다. requirements-audit/all-in-one-data의 과거 기준 대비 바이트 변경2개는 확인했으며, 대장 구조/집계 불일치는 없었다. 원본 진행 문서의 v1.12.0 프로파일 추가 이력과 구분한다.
- 본문에서 “원본 XML 확인”은 복원된 XML의 선언·핀·연결을 정적으로 읽었다는 뜻이다. TIA 복원/컴파일·온라인 CPU 비교·실제 실행 결과를 뜻하지 않는다.


## 1. 7영역 적용표


| 영역 | 판정 | 이 초안의 적용 | 남은 경계 |
| --- | --- | --- | --- |
| 설비·자료 기준 | 적용 | P13/HE01 후보, passive 본체, 역사 P&ID 두 유로, 시공 구역/장치 소유 분리 | 명판·현재 P&ID·철거 이후 배관/연결 미확인 |
| I/O·HMI | 본체 근거 미확보 / 주변 참고 적용 | TC03/PSH01/PSH03 원시입력·환산·HMI raw 전달과 Editor 참조 분리 | HE01 전용 태그·화면 이벤트 없음; HMI 표시 환산·쓰기 이벤트 미결속 |
| 제어 구조 | 본체 근거 미확보 / 주변 참고 적용 | 센서 환산→관련 조절/방향요청, TC03 공정 알람, FN02와 우회 경계 | 주변 루프의 최종 실행·호출·복수쓰기·현행 사용 여부 |
| 전기 전달 경로 | 본체 전용 동력회로 비해당 / 주변 참고 적용 | 수동 열교환 본체에 모터·접촉기 체인을 만들지 않음; 관련 계측 FG/PDF 양 끝점과 시공 구역 확인 | “passive”만으로 보조전원/현장 장치 전체가 없다고 단정하지 않음 |
| 알람·복구 | 본체 고유 근거 미확보 / 주변 참고 적용 | TC03 LOW/MAX/MAXMAX와 센서 OFR, RD01/BR01 영향 분리 | HE01 고유 알람 0건 발견은 알람 부재의 현장 증명이 아님 |
| 증상별 수리 | 적용 | 열교환 저하/압력 불일치/우회 불일치/동시 채널 이상별 관찰·배제·자료 수집 | 세정·내부 개방·보호값 변경 및 실제 수리 미수행 |
| 완료 기준 | 적용 | 자료·UI/기록·게시·TIA·CPU·현장 상태 별도 | 초안 작성만으로 BC01 동등 기능 완료 처리 금지 |


## 2. 본체 식별·공정 유로·소유 경계


### 2.1 실제 대장과 발견 범위

INVENTORY.json P13은 name=열교환기, catalog_id=HE01, mapping=candidate, identity_verified=false, queue_state=identity_review다. equipment.json HE01은 passive·전용 FG 목록 공란이다. control-spec.json의 HE01 inputs/outputs/internal/hmi/networks/direct_rules/timers는 모두 빈 목록이다.

추가로 복원 선언 원본181개 파일에서 HE01/HE-01/exchanger/exchange/scambi 이름 검색은 0건이었다. equipment-io 498행, equipment-hmi 230행, equipment-networks 1281행에서도 HE01 직접 배정은 0행이었다. 이는 조사한 백업/파생대장의 발견 결과이며 다른 이름으로 제어하거나 현재 추가된 설비까지 없다는 증명이 아니다. 통신 장치나 미등록 보조 구동기가 실물에 있는지는 별도 확인한다.

주변 참조는 TC03·PSH01·PSH03의 센서 대장, MV01·MV02·MV03의 제어, FN02 팬이며 HE01 자식으로 재분류하지 않는다. 시공 PDF의 HE-01 LOC TAG 역시 위치/구역을 나타내므로 본체 신호 소유 근거로 바꾸지 않는다.


### 2.2 P&ID 원본 렌더 확인

원본 PID_1684n002I.pdf PDF1, 도면1684n002, Apex I. title block 작성일06/04/2011, 마지막 표시 개정 I=15/01/2013(REMOVED MC-05, CHANGED POWER OF FN-02)을 렌더와 확대하여 확인했다. 이 과거 자료의 출력·온도·압력 표기를 현재 설정/보호 한계로 채택하지 않는다.

- 배기가스측: AB01 출구에서 HE01 하부 헤더로 들어가는 오른쪽 화살표, 열교환 통로 상향 화살표, 상부 헤더에서 CY01/CY03측 오른쪽 화살표가 있다.
- MV01은 HE01 하부 헤더 오른쪽과 상부 출구 관로 사이의 우회 연결이다. FN02의 공기측 바이패스와 합치지 않는다.
- 공기측: FN02→MV04→HE01 좌상 입력 화살표, HE01 좌하 출력의 왼쪽 화살표가 AB01측으로 이어진다. MV04의 하향 우회 분기는 이 좌하 관로에 합류한다.
- MV02는 ATM/CM02측 분기, MV03는 Overflow valve 분기다. TC03는 아래쪽 회송 관로에 표기되어 있으며 HE01 바로 앞/뒤 두 온도계 한 쌍을 증명하지 않는다.
- 그림의 T2 550–610°C, PSH01 +2÷+5mBar, PSH03 +0.1mBar는 역사 도면 표기다. 정상 운전 범위나 조치 임계값으로 사용하지 않는다.
- MV04는 기존 사용자 진술 기반 철거 제외(2026-10-09, field_verified=false)다. 원본 그림의 M18A/M18B·리미트를 역사 참고로 보존하되 상세 분석을 재개하거나 현행 유로로 간주하지 않는다. 철거 이후 FN02–HE01–AB01 실제 연결이 가장 먼저 필요한 현장 자료다.


## 3. I/O·환산·HMI 전달


### 3.1 관련 센서와 세 값의 분리


| 관련 센서 | 백업 심볼 표 주소 / 형식 | 환산 출력 | HMI 설정 참조 | 근거·주의 |
| --- | --- | --- | --- | --- |
| TC03 | %IW276 / Int | Data.Temp_TC03 / Int | I_TC_03=DB13,INT40; Editor_TC03=DB26,INT20 | live_index _7ev:1544, LAD1741; “temperature control outputsmoke” |
| PSH01 | %IW284 / Int | Data.Press_PC01 / Int | I_PSH_01=DB13,INT48; Editor_PSH01=DB26,INT16 | live_index _7ev:1540, LAD1745; Pressure control output MV-02 |
| PSH03 | %IW320 / Int | Data.PSH03 / Int | I_PSH_03=DB13,INT52 | live_index _7ev:1538, LAD1747; Editor_PSH03는 이 설정 목록에서 미발견 |

접근 방식도 분리한다. 위 %IW276/284/320은 live_index의 심볼 주소 표기다. 환산 호출 LAD1741/1745/1747의 원본 0678-IdentXmlPart.xml은 TC03(NID11/UID364/RID76), PSH01(NID15/UID444/RID96), PSH03(NID17/UID484/RID106) 모두 SAD R="Input" SAM="Peripherie"이며 SSD AO는 각각2208/2272/2560bit다. 즉 이 환산 입력은 해당 바이트의 직접 주변입력 PIW276/PIW284/PIW320 접근으로 구분한다. 반면 HMI raw 전송 LAD1071의 0627-IdentXmlPart.xml은 동일 센서의 NID2/UID76·100·104/RID67·79·88, 동일 AO에서 SAM="None"이므로 IW276/IW284/IW320 일반 입력 접근으로 구분한다. 동일 이름·바이트 주소라는 이유로 환산에 읽힌 주변입력과 HMI로 복사된 raw 값이 같은 시점의 동일 샘플이라고 보장하지 않는다. 현재 CPU의 프로세스이미지 배치·업데이트 시점·호출 순서는 미확인이다.

물리 raw Int, PLC 환산 Int, HMI 표시/입력 설정은 별도다. Data.Press_PC01이라는 출력명은 PSH01 %IW284에서 나온다. 별도 PC01 %IW322/Data.PC_01과 이름만으로 합치지 않는다. 공학 단위·소수점·현재 Coeff/Zero는 실물/현행 프로젝트 확인 전이다.


### 3.2 원본 CRef·선언 결속

- TC03 LAD1741=0491-FlgNet.xml, NID11: Contact375(ON)→Wire376→CRef356.en. Wire371/ORef364(RID76)=TC03→Analog_input; Wire372/ORef365=Coeff.COEFF_TC03; Wire373/ORef366=Coeff.ZERO_TC03; Wire374/ORef367=Data.Temp_TC03; Wire24/ORef23=Allarm.TC03_OFR.
- PSH01 LAD1745=0495-FlgNet.xml, NID15: Contact455(ON)→Wire456→CRef436.en. Wire451/ORef444(RID96)=PSH01; Wire452/ORef445=Coeff.COEFF_PSH01; Wire453/ORef446=Coeff.ZERO_PSH01; Wire454/ORef447=Data.Press_PC01; Wire24/ORef23=Allarm.PSH01_OFR.
- PSH03 LAD1747=0497-FlgNet.xml, NID17: Contact495(ON)→Wire496→CRef476.en. Wire491/ORef484(RID106)=PSH03; Wire492/ORef485=Coeff.Coeff_PSH03; Wire493/ORef486=Coeff.Zero_PSH03; Wire494/ORef487=Data.PSH03; Wire24/ORef23=Allarm.PSH03_OFR.
- 세 호출의 CodeBlock은 UID368/448/488·RID5의 Signal linearization 참조다. IN0에도 ON을 연결한다. 단순 “상시”라고 바꾸지 않는다.
- 0676-IdentXmlPart.xml의 GlobalAccess 선언에서 환산 출력/OFR 출력 occurrence AK=Write와 해당 NID·UID·RID를 대조했다. 원시 SimpleAccess와 ON은 0678-IdentXmlPart.xml, CodeBlock의 Signal linearization 이름은 0672-IdentXmlPart.xml, 호출 인터페이스는 0680-IdentXmlPart.xml에서 대조했다. UID/RID만 전역 키로 쓰지 않고 NID·이름·선언 파일 문맥을 대조해야 한다.


### 3.3 공통 환산 원본과 호출 경계

LAD1658=0291-FlgNet.xml, NID1, 선언 0611/0612-IdentXmlPart.xml:

- Local IN0 Contact255가 비교를 활성화한다. Analog_input > −1382(Gt258)와 ≤32767(Le161)의 직렬 경로다.
- Convert164(Int→DInt) Analog_input→App5, Convert167 Zero→App6, Add170 App5+App6→App3, Convert174 Coeff→App4, Mul177 App3×App4→App3, Div181 App3÷28000→App3, Move185→OutValue다. Wire227/230/234/237/241/245의 eno 직렬 연결을 보존한다.
- 이 경로의 수학적 개요는 ((raw + Zero) × Coeff) / 28000이다. 원본은 DInt 연산과 최종 Move이므로 실수 나눗셈이나 소수점 정밀도·오버플로/절삭 규칙을 임의 확정하지 않는다. 다른 장비의27648 환산을 복제하지 않는다.
- 범위외는 Analog_input >32767 또는 ≤−1382, O47→Move193(−9999)→OutValue다. Out_of_range Coil23은 Move193.eno→Wire21에 연결된다. 이 경로에 전용 래치나 타이머는 없다. Int 비교의 원문 경계를 그대로 남긴다.
- LAD1659=0014-FlgNet.xml, NID2는 NOT IN0(Contact171)→Move162(0)→OutValue다. 그러나 세 호출은 en과 IN0가 모두 ON이므로 호출 자체가 건너뛰어질 때 이 내부0쓰기 분기가 실행된다고 보장하지 않는다. 호출되지 않음·0·−9999·빈값을 구분해야 한다.


### 3.4 HMI는 raw 전송 경로와 표시 이벤트를 구분

LAD1071=0398-FlgNet.xml, NID2, 0627/0629-IdentXmlPart.xml:

- Powerrail→Move72.en, TC03 ORef76→Wire85→in, out1→Wire87→ORef77 Inputs.TC_03. Word 선언 BO320bit=40byte가 I_TC_03 DB13,INT40과 대응한다.
- Powerrail→Move96.en, PSH01 ORef100→Wire109→in, out1→Wire111→ORef101 Inputs.PSH_01. Word BO384bit=48byte.
- PSH03는 Move96.eno→Wire110→Move97(PSH02).en→eno/Wire113→Move98.en이다. PSH03 ORef104/Wire115→in, out1/Wire117→ORef105 Inputs.PSH_03. Word BO416bit=52byte. 이 세 번째 경로를 독립 무조건 Move로 요약하지 않는다.
- sources/hmi_plc_tags.csv는 dde.cfg에서 정리한 설정 참조이며 실제 dde.cfg/화면 객체 이벤트/현행 온라인 값 자체는 이번 자료에 없다. Editor 이름만으로 쓰기 가능·버튼 동작·승인·Data 설정까지의 전달을 확정하지 않는다. raw Word를 HMI INT로 해석하는 경계와 HMI의 자체 환산/표시식을 추가 확인한다.
- HE01 전용 HMI 화면·고유 요청/상태·고유 Alarm Ack는 미식별이다. 위5개 태그는 관련 센서 설정 참조이며 HE01 직접 HMI5개로 집계하지 않는다.


## 4. 주변 제어 구조와 고유 소유 구분


### 4.1 TC03→MV01 우회 제어

- live_index _7ex:10은 Data.TC03_SETPOINT/Temp_TC03의 ITD/DTR→Local Real_SP_TC03xMV01/Real_TC03xMV01 전송을 보여주는 평탄화 STL 검색 텍스트다. 주석 // l Data.Temp_T6가 섞여 있으므로 네이티브 명령/컴파일로 확인된 실행 코드라고 쓰지 않는다.
- LAD11=0477-FlgNet.xml, NID8, LRef366 CONT_S, Instance412 PIDMV01. Wire442/ORef401 SP_INT=Local Real_SP_TC03xMV01, Wire443/ORef402 PV_IN=Local Real_TC03xMV01, Wire457/ORef410 QLMNUP=Global UP MV01 PID, Wire458/ORef411 QLMNDN=Global DOWN MV01 PID다. 0665/0667/0668/0669/0670/0671 선언을 함께 확인한다.
- 확인한 백업 상수: CYCLE T#100MS, GAIN3.0, TI T#3M, DEADB_W1.0, PULSE_TM T#500MS, BREAK_TM T#1S, MTR_TM T#31S. 이는 MV01 CONT_S 파라미터이며 HE01 타이머/보호값이 아니다. 현재 튜닝·전환·리미트·미해석 파라미터를 확정하지 않는다.
- LAD1702=0342-FlgNet.xml, NID1은 고장 반전, Auto+PID 요청 또는 수동 요청, 반대방향/리미트, 엔코더 리셋 경계를 지나 Start Open MV-01/Start Close MV-01을 쓴다. 열림 Coil143→Wire211/ORef175, 닫힘 Coil156→Wire223/ORef183. 본체 열교환 실행 명령으로 바꾸지 않는다. 세부 MV01 문서와 동일 원본 링크로 연결하고 HE01에 중복 제어 프로파일을 만들지 않는다.


### 4.2 PSH01→MV02와 PSH03→MV03는 별도 루프

- PSH01 환산의 Press_PC01명과 _7ex:6 제목의 PC01은 별도 PC01 물리센서의 증명이 아니다. 실제 평탄화 STL은 PSH01_SETPOINT/Press_PC01→Local Real_SPPC01/Real_PC01을 표시한다. LAD7=0476-FlgNet.xml, NID4, CONT_S LRef172/PID_MV-02 Instance210→PID MV02 UP/Down이고, 최종 LAD1704=0343-FlgNet.xml에 ON 반전 접점도 있으므로 현행 출력 활성 상태는 확인 전이다.
- PSH03 직접 비교는 LAD1705=0344-FlgNet.xml, NID3: ON Contact328→Int Sub256, Wire304/ORef287 Data.PSH03_SETPOINT − Wire305/ORef288 Data.PSH03→Wire306/ORef289 Local ErrPSH03. Sub.eno를 비교 전제와 직렬 연결한 것으로 만들지 않는다.
- 같은 ON 분기에서 NOT Tag_147 Contact330→SD263(Tag_148,S5T#4S), Tag_148 Contact332→SD268(Tag_147,S5T#10S). NOT Tag_148 Contact334→Ge276(ErrPSH03≥5)→Coil279 PID down MV03, Lt282(ErrPSH03<−5)→Coil285 PID UP MV03다. %T138/139와4초/10초는 MV03 조절 경로 소유다. <−5와 ≥5의 비대칭 경계를 보존한다.
- 별도 _7ex:14는 PSH02_SETPOINT/PSH_02를 사용한다. LAD15=0479-FlgNet.xml, NID12는 제목 not used, OFF 접점 뒤 CONT_S LRef507/PID_MV03 Instance546가 같은 PID UP/down에 쓴다. 이름/제목만으로 삭제·현재미사용·최종쓰기 우선순위를 확정하지 않는다.
- LAD1706=0345-FlgNet.xml 최종 방향 요청은 세정 열림·버너 기동 닫힘·엔코더 리셋도 참조한다. HE01 압력만의 자율제어로 요약하지 않는다.


### 4.3 FN02 팬과 본체 유량은 별도

LAD1688=0469-FlgNet.xml, NID10에서 ON 조건 아래 Set_Perc_VT02<5이면5, >100이면100을 쓰고 Int Mul640×272→FN02_SP(ORef655/Wire671)다. LAD1948=0250-FlgNet.xml, NID19는 FN_02_FAULT 또는 FN02_INV 또는 Set_Perc_VT02=0을 OR587→RCoil592 Flag.M_FN_02로 연결하고 Flag.M_FN_02→Coil596 Start FN02를 쓴다. 서로 다른 네트워크의 제한/0요청/실제 호출 순서는 현행 프로젝트에서 확인할 사항이다. 팬 기동 명령이나 설정값만으로 HE01 실제 통과 유량·팬 회전·댐퍼 실제 위치를 확정하지 않는다.


## 5. 전기 전달 경로·시공 케이블


### 5.1 직접 렌더한 OEM 회로와 모듈 끝점

모든 아래 회로는 Electrical_Rev2.pdf 실제 페이지를 렌더하여 단자 양 끝점을 확인했다. FG는 도면 번호이며 PDF 페이지와 다르다. title block 기본일자는27.05.2024이다. FG107/PDF108은 별도 Rev2=17.03.2025가 보이고, FG75/77/106/108의 해당 렌더에서는 같은 개정란이 보이지 않는다. 파일명 Rev2를 모든 페이지의 개정값으로 주입하지 않는다.


| 경로 | 현장측 FG / PDF | 양 끝점 | 모듈측 FG / PDF | 소유·미확정 |
| --- | --- | --- | --- | --- |
| TC03 | FG77/PDF78, TEMPERATURE CONTROL OUTPUT SMOKE | +24Vdc10.7→X1:192(5×20,50mA F)→TC03 +5; TC03 −6→X1:193→+PEW276; X1:194/77SCH3 shield | FG106/PDF107, CPU515/MOD3, PEW276 I2+ pin10; U2−/I2− pin12→0V; MANA18 | 표기4–20mA,0/750°C. 실물 변환기·영점·극성·현재범위 미확인 |
| PSH01 | FG75/PDF76, PRESSURE CONTROL OUTPUT MV-02 | +24Vdc10.7→X1:172(50mA F)→PSH01 +; PSH01 −→X1:173→+PEW284; X1:174/75SCH1 shield | FG107/PDF108, CPU515/MOD3, PEW284 I6+ pin30; U6−/I6− pin32→0V | P-BADR,4–20mA,0/10mbar 원문. 실제 취출위치/현행 모델 미확인 |
| PSH03 | FG75/PDF76, 상단 제목 PRESSURE CONTROL PSH-02 / 하단 장치 PSH-03 | +24Vdc10.7→X1:178(50mA F)→PSH03 +; PSH03 −→X1:179→+PEW320; X1:180/75SCH3 shield | FG108/PDF109, CPU515/MOD4, PEW320 I0+ pin2; U0−/I0− pin4→0V, 채널 제목PSH-03 | 제목PSH-02/장치PSH-03 상충을 보존. P-BADR,4–20mA,0/10mbar |

센서 전원 퓨즈 표기50mA F는 도면에 적힌 값이다. 적합성 판단·현장 교체 지시·현재 보호값으로 사용하지 않는다. Electrical_Rev2.pdf가 HE01 본체 전용 회로를 제공한 것은 아니다.


### 5.2 시공 구역과 공유 접속함

Electrical_Can_Decoating_20241118.pdf P3/P6/P56/P57을 직접 렌더했다. 표제부 Rev1=24.11.11 first draft design, P56=CANDC-CONS-C006-056, D-PAGE6/TOTAL56/64; P57=CANDC-CONS-C007-057, D-PAGE7/TOTAL57/64다. 파일명의20241118과 표시 개정일24.11.11을 구분하며 승인/준공 도면으로 주장하지 않는다.

- P3은 FLOW_A의 HE01 구역, P6은 HE01 FLO1TB4/FLO2TB1 접속함 표기를 보여 준다. 본체 전용 PLC 인터록을 뜻하지 않는다.
- P56의6_7–6_10은 검게 가려져 있다. 텍스트 추출에 내용이 남더라도 이 행을 배선 증거로 복원하지 않는다.


| PDF/행 | 원본 CABLE NO. | FROM→TO와 DESCRIPTION | 원문 케이블·신호 | 해석 경계 |
| --- | --- | --- | --- | --- |
| 56/6_11 | =FLA+HE01-PSH03A | CR→HE-01 PSH-03 | AI / CVV-S4S | HE01 구역 위치 참조; PSH03 실제 취출/본체 소유 미확인 |
| 56/6_21 | =FLA+HE01-RO01A | MV-03 81RO-01→HE-01 RO-1 | AI / CVV-S4S | 센서와 변환기/반 구간을 분리 |
| 56/6_22 | =FLA+HE01-RO02A | MV-03 81RO-02→HE-01 RO-2 | AI / CVV-S4S | RO02 본체 소유를 임의 확정하지 않음 |
| 56/6_23 | =FLA+HE01-TC01A | CR→HE-01 TC-01 | TC / KX2S | OEM FG77은 AB01 chamber라고 표기; 위치코드/기능소유 상충 보존 |
| 56/6_24 | =FLA+HE01-TC02A | CR→HE-01 TC-02 | TC / KX2S | OEM FG77은 safety temperature control chamber AB01; 가림6_8을 대체증거로 사용하지 않음 |
| 57/7_1 | =FLA+HE01-FLO2TB1A | CR→HE-01 FLO2TB1, LS17/18/23/24/21A/22A/21B/22B | DC / CVV25G | MV02/MV01/MV04의 공유 간선 |
| 57/7_2 | =FLA+HE01-FLO2TB1B | CR→HE-01 FLO2TB1, ACTUATORS(MV04) | AC / CVV5G | 철거 MV04의 과거 경로; 추가 분석 제외 |
| 57/7_3,7_4 | =FLA+HE01-FLO2TB1C / …1D | CR→HE-01 FLO2TB1, M18A / M18B | AO / CVV-S2S 각각 | 두 구동기를 하나로 합치지 않음; 현행 철거 이후 배선 미확인 |
| 57/7_5,7_6 | =FLA+HE01-FLO2TB1E / …1F | CR→HE-01 FLO2TB1, ZT02 / ZT03 | AI / CVV-S4S 각각 | AI 표기만으로 encoder 소프트웨어 채널/인터페이스 확정 금지 |
| 57/7_7 | =FLA+HE01-PSH01A | CR→HE-01 PSH-01 | AI / CVV-S4S | OEM PSH01 회로와 현재 양단 대조 필요 |
| 57/7_8 | =FLA+MV01-LS23A | HE-01 FLO2TB1→MV-01 LS-23 | DC / CVV2C | MV01 별도 리미트 |
| 57/7_9 | =FLA+MV01-LS24A | HE-01 FLO2TB1→MV-01 LS-24 | DC / CVV2C | LS23과 별도 |
| 57/7_10 | =FLA+MV01-ZT02A | HE-01 FLO2TB1→MV-01 ZT-02 | AI / CVV-S4S | 기계위치/변환기/PLC 입력 대응 미확인 |

TC01/02 시공의 TC/KX2S와 OEM FG77의 +24V·4–20mA는 같은 구간이라고 단정하지 않는다. 센서 소자→변환기→간선→입력모듈의 실제 양 끝점과 위치를 확보해야 연결할 수 있다. 원본 케이블 행을 현재 승인 심선표 대신 쓰지 않는다.


## 6. 주변 알람·복구 경계


### 6.1 HE01 고유 알람·타이머는 미확보

관련 TC03 온도 알람을 HE01 고유 알람3개로 세지 않는다. PSH01/PSH03/TC03 OFR는 위 환산 호출의 별도 출력이며, HE01의 막힘/누설/열교환 효율 진단 비트라는 근거가 없다. OFR만으로 기계고장을 확정하거나 센서 이상만으로 본체를 수리하지 않는다.


### 6.2 TC03 원본 고유 알람 식

모두 LAD1980=0528-FlgNet.xml, NID2, 선언 0683/0684/0685/0686-IdentXmlPart.xml이다. ON 조건·래치·타이머·복구 경로를 구분한다.


| 센서 소유 알람 | Set 경로 | Reset 경로 | 시간·소유 |
| --- | --- | --- | --- |
| Allarm.LOW_TC03_TEMP | ON Contact543→BWF01 RUN Contact545 또는 BWF02 RUN Contact547(OR333)→Int Lt336(Temp_TC03<TC03_MIN_ALL)→SD342 및 Tag_101 Contact549→Set347 | ON AND 자기래치 Contact551→Int Add352(TC03_MIN_ALL+5)→Local app00; Add.eno Wire491→Gt356(Temp_TC03>app00)→Reset360 및 Set362 STOP_HORN | Tag_101 %T87 / S5T#3S. LOW Reset 분기에 BWF RUN·RESET_ALLARM 접점 없음 |
| Allarm.MAX_TC03_TEMP | ON→Int Gt366(Temp_TC03>TC03_MAX_ALL)→SD372 및 Tag_102 Contact553→Set377 | ON AND 자기래치 Contact555→Int Sub382(TC03_MAX_ALL−5)→Local app00; Sub.eno Wire512→Lt386(Temp_TC03<app00)→Reset390 및 Set392 STOP_HORN | Tag_102 %T88 / S5T#3S. MAX Reset 분기에 RESET_ALLARM 접점 없음 |
| Allarm.MAX_MAX_TC03_TEMP | ON→Int Add396(TC03_MAX_ALL+50)→Local max_max_tc3; Gt403(Temp_TC03>max_max_tc3) 또는 Gt406(>750) 또는 Lt409(<−60), OR402→SD415 및 Tag_103 Contact557→Set420 | ON→RESET_ALLARM Contact559→자기래치 Contact561→Reset425 | Tag_103 %T89 / S5T#3S. Reset 분기에 온도 정상/원인해소 조건 없음 |

- LOW/MIN 보정은 같은 LAD1980의 ON→Lt21(TC03_MIN_ALL<200)→Move27(200)→TC03_MIN_ALL이다. 현장 설정이 항상200 이상이라고 단정하지 않고 복수쓰기와 네트워크 실행 순서를 확인한다.
- MAXMAX는 Add396.eno가 비교를 enable하는 구조가 아니다. Wire544가 Add396.en과 Gt403/Gt406/Lt409.pre를 별도로 분기 공급한다. Local 값 계산과 비교의 실제 실행 순서는 TIA 확인 사항이다.
- 상수200/5/50/750/−60은 백업 비교/산술 값이다. 현장 보호값 변경 권고가 아니며 센서 단위/실제 스케일도 별도 확인한다.
- timer 주소는 live_index _7ev:1578/1577/1576과 Timer 선언 AO87/88/89를 대조했다. HMI 태그로 분류하지 않는다.


### 6.3 공정 영향과 재기동

- LOW: LAD1931=0238-FlgNet.xml, NID2, Wire80/ORef69→Contact95→OR56.in1, OR56→Coil66→Local Disable_Load_RD01(0605 선언)이다. 이는 RD01 적재금지 경로의 한 원인이며 HE01 고유 출력이 아니다. LOW 해제로 다른 적재 허가까지 모두 충족되지는 않는다.
- MAXMAX: LAD1858=0175-FlgNet.xml, NID5, Wire260/ORef242→Contact291→OR219.in5→ON Contact305→OR213.in5→RCoil232→Flag.Start_Burner(ORef250/Wire272). GME 버너 시작요청 Reset 근거이며 외부 연소제어기의 내부 안전 차단 순서/인증을 증명하지 않는다.
- MAX: LAD1862/1865/1870에 추가 참조가 있다. 특히 LAD1865=0181-FlgNet.xml의 MAX_TC03→Contact636은 앞에 OFF Contact632가 있고, Lock Burner의 Reset에도 ON을 통한 OR586 병렬분기가 있다. “MAX면 즉시 본체/버너 잠김”이라는 단순 문장을 만들지 않는다. 세부 버너 제어는 BR01 자료와 현재 프로젝트로 대조한다.
- RESET_ALLARM 조작·알람 비트 해제·STOP_HORN·GME 기동요청·외부 버너 정상응답·현장 복구는 서로 다른 상태다. 본 조사에서는 리셋/재기동/현장 시험을 수행하지 않았다.


## 7. 증상별 관찰·원인 배제·복구 증거

기존 HE01-D01~D04의 증상 분류를 보존하되 다음과 같이 관찰 위치를 명확히 한다. 작업자의 안전절차/승인 없이 본체 개방, 세정, 센서분리, 활선측정, 강제출력 또는 보호값 변경을 지시하지 않는다.


| 증상 | 먼저 기록할 사실 | 비교·원인 배제 | 다음 자료/복구 판정 |
| --- | --- | --- | --- |
| HE01-D01 가열·열교환 효과 부족/흔들림 | 같은 시각·같은 운전조건의 매체/유량, 측정 위치, 입출구 온도, FN02 실제응답, MV01 실제위치 | TC03 한 점·팬요청·명령개도를 효율로 바꾸지 않음. raw→환산→표시와 MV01 우회/FN02 공기측을 분리 | 현재 입출구 계측 위치·제작사 성능표·명판·현행 유로. 승인 조치 전후 동조건의 실제 열수지/측정 증거 |
| HE01-D02 압력·배출/순환 불일치 | PSH01/03 취출위치·단위·raw/환산/설정·MV02/03 모드·실제방향/위치 | PSH01/Press_PC01와 PC01을 구분. PSH03 직접비교와 PSH02 별도 PID를 구분. OFR·전원·변환기 문제를 본체 막힘과 분리 | 현재 취출 배관/변환기·허용압력·승인 설정/루프 확인. 원인별 관찰과 후속알람 |
| HE01-D03 팬 운전 표시 중인데 우회/교환 경로가 불일치 | FN02 요청/출력/실제회전·상태시각, MV01 요청/출력/리미트/실물위치, 철거 후 배관 | 팬 상태 하나로 유동/전열 확정 금지. 과거 MV04/M18A/B·공유간선을 현행 장치로 복원 금지 | 철거 이후 승인 P&ID·도면·양단 사진. 실제 유로·팬응답·댐퍼위치 일치 증거 |
| HE01-D04 여러 채널/리미트 동시 이상 또는 소유 불일치 | FLO1TB4/FLO2TB1 표찰, 전원/채널/시각, 변경이력, 회로별 양단 | 공유간선과 개별소자를 분리. 가림6_7–6_10 배선 추정 금지. KX와4–20mA 구간 혼합 금지 | 준공도·심선표·케이블 번호·센서/변환기 위치·양단 사진; 각 독립 채널의 정상화 증거 |

관찰기록에는 actual_equipment_id, 관찰자·시각/시간대·운전모드·측정위치·값/단위·수집기기·프로젝트 근거·원시/처리 구분·비교 원본·배제 결과·승인 조치·복구 증거를 남긴다. 현재 repair-observation-P13.json은 actual_equipment_id=null, observations/recovery_evidence 빈 배열, status=미작성, field_verified=false다. 실제 관찰이나 복구 자료로 바꾸지 않았다.


## 8. 핵심 주장 근거표

아래 해시는 부록의 원본 경로로 결속한다. 파생 문서는 탐색·기존 내용 보존에 사용했고 핵심 식/접점/단자는 직접 원본을 대조했다.


| 주장 | 원본 파일·위치 | 선언/핀·해석 | 불확실성 |
| --- | --- | --- | --- |
| P13=HE01 역할 후보/passive | INVENTORY priority P13/catalog HE01; equipment HE01 | candidate/identity_verified=false, passive | 실물 매칭 미완료 |
| 두 열교환 유로/우회 분리 | PID1684n002I PDF1 HE01 구역 및 title block | AB01→하부→상부→CY, 별도 FN02/MV04 공기측 | 현행 유로·효율 미확인 |
| 본체 직접 PLC 발견0 | 선언181파일 이름 검색; HE01 control-spec와 I/O/HMI/network csv | HE01 고유 선언/배정/알람/타이머 미발견 | 다른 이름·현행 추가 가능성 |
| TC03 raw→환산 | 0491 NID11 + 0676/0678 | CRef356, W371/374/24, O364/367/23 | 현재 계수/단위·호출 미확인 |
| PSH01 raw→Press_PC01 | 0495 NID15 + 0676/0678 | CRef436, W451/454/24, O444/447/23 | 별도 PC01과 소유 혼동 금지 |
| PSH03 raw→Data.PSH03 | 0497 NID17 + 0676/0678 | CRef476, W491/494/24, O484/487/23 | 도면 상단PSH02/하단PSH03 불일치 |
| 환산28000·OFR·호출경계 | 0291 NID1/0014 NID2 + 0611/0612 | Part164→167→170→174→177→181→185; OFR Move193.eno→Coil23 | Int/DInt·최종Move·미호출 보존값 미검증 |
| raw HMI 전달·PSH03 ENO 선행 | 0398 NID2 + 0627/0629; hmi_plc_tags.csv | Move72/96/97/98, W85/87/109/111/113/115/117 | 실제 화면 이벤트/환산 미확인 |
| TC03→MV01 조절소유 | 0477 NID8 + 0665/0667–0671; 0342 NID1 | LRef366 W442/443/457/458, Coil143/156 | STL10은 색인; 현재 튜닝·리미트 미확인 |
| PSH03 비교·4/10초 | 0344 NID3 + 0062/0617/0619/0620 | Sub256/Ge276/Lt282/SD263/268, T138/139 | MV03 별도PID 복수쓰기·호출 미확인 |
| TC03 LOW/MAX/MAXMAX | 0528 NID2 + 0683–0686 | Part336/342/347/352/356;366/372/377/382/386;396/402/415/420/425 | HE01 고유 알람 아님; 현장보호값 아님 |
| LOW→RD01 적재금지 | 0238 NID2 + 0602/0604/0605 | Contact95→OR56→Coil66 Local Disable_Load_RD01 | 적재 재허가 전체 조건 아님 |
| MAXMAX→GME 버너요청 Reset | 0175 NID5 + 0582/0585 | C291→OR219.in5→C305→OR213→R232 | 외부 버너 내부 안전순서 미증명 |
| 센서 회로 양 끝점 | Electrical_Rev2 FG75/77/106/107/108 = PDF76/78/107/108/109 | X1/PEW/모듈핀 표 참조 | 현재 설치/정상극성/모델 미확인 |
| HE01 구역/공유함과 가림행 | 시공 PDF3/6/56/57,6_11/21–24,7_1–10 | LOC TAG와 실제 센서/장치를 분리 | 승인/준공 미확인; 가림행 채택불가 |
| TC01/02 소유·케이블 상충 | 시공 PDF56/6_23–24 대 OEM FG77/PDF78 | HE01 위치코드/AB01 기능표기, KX2S/4–20mA 구간 | 실제 소자·변환기·양단 확인 필요 |


## 9. 네 기능 적용 및 기록 보존 인계


| 기능 | HE01 적용 제안 | 고정 v1.12.0에서 확인한 상태 | 완료 조건 |
| --- | --- | --- | --- |
| 도면·래더 나란히 보기 | 본체 P&ID와 관련 TC03/PSH 회로·환산/알람을 “주변 참고”로 비교. 본체 전용 LAD 없음을 상시 표기 | 본 조사에서 기능 구현/화면검증 없음; 기존 body-manual/관련 문서는 존재 | 아래 원본쌍 링크·FG/PDF·UID 강조·왕복·새로고침 실검증 |
| 백업 미리보기/선택 복원 | P13·HE01·실물ID 분리와 후보 표시 유지 | equipment_standards 프로파일10개에 HE01/P13 없음. 전체백업 기능 존재가 HE01 전용 표준 도구 지원 증명은 아님 | 격리 합성 QA로 미리보기→충돌 선택→저장→재읽기→재열기, 타설비/미지필드/초안 보존 |
| 기록 전후 비교 | 동일 계측위치·조건·시각 기준으로 raw/환산/실물 분리 | HE01 지원·실제 검증 미수행 | 0/빈값/−9999/미호출을 구분하고 원인·조치·복구 증거 비교 |
| 보고서/PDF | 후보 대응·주변소유·자료판본·미확정·실제관찰 구분 | HE01 보고서 렌더·PDF 검증 미수행 | 생성/저장 근거와 관찰 당시CPU 증거 구분, A4 렌더와 페이지/링크 확인 |

권장 원본쌍: (1) PID PDF1↔본체 식별/유로 설명, (2) OEM FG77/PDF78·FG106/PDF107↔TC03 LAD1741/1658/1980, (3) FG75/PDF76·FG107/PDF108↔PSH01 LAD1745/1704, (4) FG75/PDF76·FG108/PDF109↔PSH03 LAD1747/1705, (5) 시공 PDF56/57↔장치 소유/공유함 경계. 순수 본체에는 직접 래더 없음 표시를 유지한다.

기존 note/repair_observation, 미지 필드/행, 다른 설비, 초안, 저장 키와 과거 generated_with/saved_with를 보존한다. P13과 HE01이라는 이름이 같다는 이유로 기존 기록 키를 합치지 않는다. 새 근거를 과거 관찰 당시CPU/현장 상태로 소급 적용하지 않는다.


## 10. 검증·미실행·다음 조치

수행: 공개 작업표준 읽기, 고정 commit/Git clean 확인, 읽기 전용 preflight 종료0, 관련22개 네트워크 원본/선언 정적 추출, PDF 원본10페이지 렌더 및 PID 확대2개/가로 렌더, 고유 source SHA256 계산, 중지5자산 해시 일치 확인. 자체 추출은 논리 실행/시뮬레이션이 아니라 XML 구조와 문서의 읽기/전사다.

미수행: 원본repo 편집/생성기, npm/매뉴얼/BC01 회귀, UI/저장/복원/동시성/Quota/PDF 보고서, 패키지/ZIP/CSP/게시, TIA/CPU/현장/실물/복구. 이유는 읽기 전용 조사초안 역할이며 유일한 로컬 편집자 범위와 실제 현장 접근을 침범하지 않기 위해서다. 추가 독립 검토자는 아직 확인 전이다.


| 상태 | 이번 결과 | 설명 |
| --- | --- | --- |
| documentation | draft_complete_with_gaps | 7영역·핵심근거·원본해시·누락을 작성, 통합 전 |
| static_review | source_checked_pending_independent_review | 원본 선언/핀/도면 자체대조; 앱 정적/회귀검사 아님 |
| ui_records | not_run | HE01 프로파일/UI/기록 기능 검증 전 |
| publication | not_published | 이 초안 반영·버전·GitHub/게시 확인 없음 |
| tia_compile | not_performed | 복원/컴파일 미수행 |
| live_cpu | not_performed | 현행 프로젝트·CPU 비교 미수행 |
| field_recovery | not_performed | 실물·운전관찰·수리·복구 미확인 |

다음 한 작업: 로컬 편집자가 이 초안의 TC03 LAD1980 및 원본 P&ID/회로/시공 공유함 경계를 독립 검토한 뒤, 기존 body-manual의 HE01-D01~D04와 연계하는 HE01/P13 표준 프로파일을 통합한다. 본체 직접 PLC 항목을 만들지 않고 “미확보/주변참고”를 데이터와 UI에서 구분한다.

추가 필수 자료: (1) HE01 명판·실물 위치와 P13 대응, (2) MV04 철거 후 현행 P&ID/배관, (3) HE01 제작사 형식·매체·성능/허용압력/정비 기준, (4) TC03/PSH01/03 실제 취출·센서/변환기·모듈/심선 양단과 단위, (5) 승인/준공도·현재 PLC 호출/설정/중복쓰기와 HMI 이벤트, (6) 동일 조건 입출구 측정 및 승인 조치 후 실제 복구 기록. 없는 값은 공란/미확정으로 유지한다.


## 부록 A. 직접 조사 파일 SHA256

해시는 고정 조사 원본의 바이트 식별자이며 현재CPU·현장 동일성을 증명하지 않는다. 아래 경로는 저장소 루트 기준이다. 자체 추출/렌더는 원본이 아니며 이 원본해시와 구분하여 보관한다.


| 파일 | SHA256 |
| --- | --- |
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b |
| all-in-one/registers/all-in-one-data.json | 63a46b36b6454bf1246d093300dbee11f2fcc287ad94991405369bf9f939a8fe |
| all-in-one/registers/body-manual.json | 0e8071196565fdffb29ae81fa3d24e567c95fd254355e5d71e887bc24ac189a4 |
| all-in-one/registers/control-spec.json | 1e495b32f1f11b910919fbd2945e842a019fce9a27a6a0d7298041a7fab00079 |
| all-in-one/registers/equipment-hmi.csv | 2cdce600aa0138cc5025022e57d9d61a948afb237f70c70e2d11e8300e73286a |
| all-in-one/registers/equipment-io.csv | a7a1f27dc453af25b2b729074cac5266d6dd53c0945a6a1a4afe2dd1e9153b6a |
| all-in-one/registers/equipment-networks.csv | 0dcd161bafe7fbc5fd31dd00ed031da3b01e4e46f1154b4c80698bdd766568e0 |
| all-in-one/registers/equipment.json | 7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa |
| all-in-one/registers/regulation-manual.json | 3b5309ec06f35610ab57e6ef85bd7eb6f7c83ec7db149db1b881b9b65bce91fe |
| all-in-one/registers/repair-observation-P13.json | bc1d2ea52439070afcbff093ed418d9c58b998c83a98e9d764b360fedb14b4ff |
| all-in-one/registers/sensor-measurement.json | 4b8c357c803e7b429766d54a87bf49bb5dd25343a9797b44b5702df93440c7a3 |
| all-in-one/registers/simulator-freeze.json | bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| all-in-one/sources/GME_20250506.zap18 | 00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8 |
| all-in-one/sources/PEData.plf | 647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| all-in-one/sources/decoded-original/0014-FlgNet.xml | 2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30 |
| all-in-one/sources/decoded-original/0062-IdentXmlPart.xml | 34f188168dc4fad0d6e2c813028045f37b84025636bcebd8aa1c7ffb4cfd9bcd |
| all-in-one/sources/decoded-original/0175-FlgNet.xml | 41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97 |
| all-in-one/sources/decoded-original/0178-FlgNet.xml | 36752e04a38e486ad4a0857d6baa8119d9b757678300358bcc95881f23e266c9 |
| all-in-one/sources/decoded-original/0181-FlgNet.xml | 98e839ee13a05db05768503e768e9238d892c4788dc7b6c9d3017fc86d3b722b |
| all-in-one/sources/decoded-original/0186-FlgNet.xml | 932f8756ee0e4385553944bd166109c45684766a136bfddd68cdf08552a83883 |
| all-in-one/sources/decoded-original/0238-FlgNet.xml | 8f6a5537084e092c352552dc469bbe8469b33412971219e51bba211ef607dfa8 |
| all-in-one/sources/decoded-original/0250-FlgNet.xml | e54a35e34540c3ccb59af900e18d9f1e6b14fc3175a663fe2e60a4a41b563ae5 |
| all-in-one/sources/decoded-original/0291-FlgNet.xml | fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550 |
| all-in-one/sources/decoded-original/0342-FlgNet.xml | 9ef93abad16cc055509ef98c388417c716cb03d23cb02aed6d95888beb43bef8 |
| all-in-one/sources/decoded-original/0343-FlgNet.xml | a2f41d7cce7c4d944f0cebdcacc964a1298962198a20f9471558902b39685d68 |
| all-in-one/sources/decoded-original/0344-FlgNet.xml | 08eabc412b9457eb615d1cb01b92682987bef170cbeab78070dd4c705ab93576 |
| all-in-one/sources/decoded-original/0345-FlgNet.xml | b278a319d4d8cb8d157f449a2365445ff8f172245ebd2a468aa3ee79dba60f93 |
| all-in-one/sources/decoded-original/0398-FlgNet.xml | 4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747 |
| all-in-one/sources/decoded-original/0469-FlgNet.xml | 65a7cba8a18b5e9d79cbade58ef0a5ffad80329550996ee7225e5026c36af696 |
| all-in-one/sources/decoded-original/0476-FlgNet.xml | 0f9c48dddf61987d61094de9368ab534b56ec6c30e898dc2e4d81b64e86fa55a |
| all-in-one/sources/decoded-original/0477-FlgNet.xml | e7b5b0cb95c60d1112081f6129a3127f8413e1b1d2a4c67d0e203d36ea0a711a |
| all-in-one/sources/decoded-original/0479-FlgNet.xml | 112e55599a4dc705438c8c61b936da9a167c22d9bbd909eda11c45c9dc33e839 |
| all-in-one/sources/decoded-original/0480-FlgNet.xml | c14d2fee14b38b7c597edb46626676f0cf550b5831668884cb2fac341b559273 |
| all-in-one/sources/decoded-original/0491-FlgNet.xml | f7395b1dc4f33553114a108c61691cb24b830d2152b31e6e9cd9f7718ecc9b1d |
| all-in-one/sources/decoded-original/0495-FlgNet.xml | 0ff8eb8cf4b147a9077e5bcd88620216cea558cdf2cbb2c336c07b91014abfa4 |
| all-in-one/sources/decoded-original/0497-FlgNet.xml | 334a065d6dc7aac9e9652a1f705a31fdadea6a5d4760dd6aa2ed3283a8e4b665 |
| all-in-one/sources/decoded-original/0528-FlgNet.xml | cc856c9e70accae5f3f3ff16cb1d4f6d3c00ab7f5b538ff9d58cdf97b23845d0 |
| all-in-one/sources/decoded-original/0564-IdentXmlPart.xml | 2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1 |
| all-in-one/sources/decoded-original/0582-IdentXmlPart.xml | 41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951 |
| all-in-one/sources/decoded-original/0583-IdentXmlPart.xml | 0a34a2b7ad17eba6198dbe53d5c6aa8e87710c7436b832b9d39a075074ab58a8 |
| all-in-one/sources/decoded-original/0585-IdentXmlPart.xml | e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184 |
| all-in-one/sources/decoded-original/0586-IdentXmlPart.xml | f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250 |
| all-in-one/sources/decoded-original/0602-IdentXmlPart.xml | 46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf |
| all-in-one/sources/decoded-original/0604-IdentXmlPart.xml | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af |
| all-in-one/sources/decoded-original/0605-IdentXmlPart.xml | 0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b |
| all-in-one/sources/decoded-original/0606-IdentXmlPart.xml | 73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740 |
| all-in-one/sources/decoded-original/0611-IdentXmlPart.xml | 0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089 |
| all-in-one/sources/decoded-original/0612-IdentXmlPart.xml | 95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38 |
| all-in-one/sources/decoded-original/0617-IdentXmlPart.xml | 10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9 |
| all-in-one/sources/decoded-original/0619-IdentXmlPart.xml | 85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456 |
| all-in-one/sources/decoded-original/0620-IdentXmlPart.xml | da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3 |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| all-in-one/sources/decoded-original/0661-IdentXmlPart.xml | 90672199fee355011f581d3287046894772f3f3b4cb78bbe0dd0d71bd488ac93 |
| all-in-one/sources/decoded-original/0662-IdentXmlPart.xml | 1838040bfee800fdb3f13b126eaf69a9d178b17cecc0d59ae03e9185216a48a5 |
| all-in-one/sources/decoded-original/0664-IdentXmlPart.xml | 68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed |
| all-in-one/sources/decoded-original/0665-IdentXmlPart.xml | 50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd |
| all-in-one/sources/decoded-original/0667-IdentXmlPart.xml | ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3 |
| all-in-one/sources/decoded-original/0668-IdentXmlPart.xml | 2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed |
| all-in-one/sources/decoded-original/0669-IdentXmlPart.xml | 754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2 |
| all-in-one/sources/decoded-original/0670-IdentXmlPart.xml | e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841 |
| all-in-one/sources/decoded-original/0671-IdentXmlPart.xml | 26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293 |
| all-in-one/sources/decoded-original/0672-IdentXmlPart.xml | 6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222 |
| all-in-one/sources/decoded-original/0676-IdentXmlPart.xml | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 |
| all-in-one/sources/decoded-original/0678-IdentXmlPart.xml | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 |
| all-in-one/sources/decoded-original/0680-IdentXmlPart.xml | fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95 |
| all-in-one/sources/decoded-original/0683-IdentXmlPart.xml | 0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22 |
| all-in-one/sources/decoded-original/0684-IdentXmlPart.xml | 6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208 |
| all-in-one/sources/decoded-original/0685-IdentXmlPart.xml | 2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448 |
| all-in-one/sources/decoded-original/0686-IdentXmlPart.xml | b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4 |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
| all-in-one/sources/live_index.json | 14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1 |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 |

총 79개 조사/근거 파일 해시. XML·원본PDF/백업과 파생 색인·대장은 위 경로로 구분한다. 원본별 SHA256 검증 목록은 자체 source-sha256.json에도 동일하게 보관한다.
