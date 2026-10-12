# TC06 온도 계측 — 고유 원본 조사 7영역 초안

## 핵심 확인·상충·공유 근거

- TC06 고유 경로는 `%IW278:P` → 0492 CRef376 `Signal linearization` → `Data.Temp_T6` DB1.DBW120과 `Allarm.TC06_OFR` DB3.DBX21.5다. HMI 원시 미러 `Inputs.TC_06` DB13.DBW42는 별도다.
- OEM FG78/PDF79의 기능은 `TEMPERATURE CONTROL OUTPUT AB-01`, 4–20mA, 0/1300°C다. FG106/PDF107의 PEW278, CPU515 MOD3 I3+14까지 양 끝점을 재확인했다. FG78은 Rev2/17.03.2025이며 FG106은 별도 개정 기입이 관찰되지 않는다.
- 시공 PDF23/53은 TC06 위치를 CC01로 기재한다. OEM의 AB01 출구 역할과 위치 표기를 그대로 병기한다. TC06을 CC01 본체 소유로 배정하지 않으며 **CC01 본체 전용 근거 미확보는 유지**한다. CC01 전체 재검색은 하지 않았다.
- 고유 명명 선언·FlgNet 검색에서 TC06 온도 HIGH/LOW/MAXMAX·지연 타이머·S/R 래치·버너 차단 직접 소비는 확보하지 못했다. TC01/02/03의 3초/6초나 인접 TC04/05의 경보를 복제하지 않는다. OFR의 생성은 공통 함수의 Move ENO 코일이며 단순 비교 비트와 구분한다.
- `live_index.json` `_7ex/10`의 `// l "data".temp_t6`는 주석이다. 실제 MV01 PV 소비로 세지 않는다. Data 인터페이스 설명의 과거 `t5_t6_max_all` 명칭만으로 TC06 고온경보를 발명하지 않는다.
- 공유 재사용: AB01 초안의 TC06/전기 인덱스, TC03·BF01의 0291/0014 선형화 설명을 재사용했다. TC06 호출/선언/핀/HMI 5행/실제 PDF 4쪽은 독립 확인했다. 새 자료 없는 본체·실물 보류 반복조사는 하지 않았다.
- 미확정: 현행 센서·송신기 형식/위치·열전대 보상선 구간·정상 극성·교정, 현재 계수와 제로, CPU/실제 호출순서·HMI 이벤트·현재 경보와 복구. 인쇄 0/1300°C는 승인 보호설정이 아니다.

## 1. 설비·자료 기준

TC06, sensor/계측, parent 없음, depth0, priority_key 없음, 별칭 tc_06. INVENTORY catalog[17], equipment[81], phase2/planned. 역할은 AB01 출구 온도다. 동일 이름 TC01~TC11이나 AB01/CC01과 동일 실물·완료 항목으로 병합하지 않는다. TASK3-BATCH08-SCOPE.json 및 GME-CATALOG-OVERLAP-REVIEW.json의 해당 행을 확인했다. 로컬 2차133 통합 제외를 유지한다.

원본은 `gme-research/source-mv06`, 고정 commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0이다. 사용자 진술의 최신 v1.16.0 게시와 이 고정 입력의 의미검토는 별개다. 런타임 모델·추론 설정의 실제 증명은 미확인이다.

AGENTS, 저장소 스킬/source-map, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, START-GPT61과 VERSION/EXPANSION-WORK/WORKSPACE-HANDOFF/PUBLICATION_STATUS/ACTIVE-WORK 최신 항목을 읽었다. 최신 배치 지시가 과거 병렬수·제품통합 지시보다 우선한다. 새 Work/Codex/재위임/사용자 Mac/TIA 추가 접근 없음. 원본 build/test/generator 실행 없음. 시뮬레이터 작성·수정·생성·실행·행동시험, PLC/현장/보호값/SEJIN/운영기록 변경0. 쓰기는 이 MD와 extracts/TC06뿐이다.

아래 원본 경로는 별도 표기가 없으면 `source-mv06/all-in-one/sources/decoded-original/`의 `NNNN-FlgNet.xml` 또는 `NNNN-IdentXmlPart.xml`을 뜻한다. LAD 문서 번호, NID, RID, UID는 서로 다르며 같은 UID를 다른 블록으로 연결하지 않았다.

| 7영역 | 적용·확보 수준 | 미확정 경계 |
|---|---|---|
| 설비·자료 | 적용 | 실물 동일성·현행 자료 |
| IO/HMI | 적용 | 실제 화면·쓰기권한·통신 |
| 제어 | 적용, 환산과 미러 확인 | 전체 간접 Writer/CPU 최종값 |
| 전기끝점 | 적용, OEM·시공 4쪽 | 시공-변환기 연결 구간 |
| 알람·복구 | OFR 적용, 고유 고온/타이머 근거 미확보 | 실제 경보/복구 |
| 증상관찰 | 읽기 전용 계획 적용 | 현장 관찰 미수행 |
| 완료·누락 | 문서초안 적용 | 통합·UI·게시·현장 별도 |

## 2. IO·HMI

### 2.1 선언과 저장부

| 신호 | 원본 선언·NID/UID | 형식/주소·쓰기 |
|---|---|---|
| TC06 환산입력 | 0678 RID81, NID12 UID384, SimpleAccess Global, AO2224, SAD Input SAM=Peripherie | Int, IW278:P/PIW278 읽기 |
| TC06 미러입력 | 0627 RID70, NID2 UID78, SimpleAccess Global, AO2224, SAM=None | Int, IW278 읽기. 위 Peripherie와 구별 |
| Inputs.TC_06 | 0629 RID72, NID2 UID79 AK=Write, AO336; BAD4→0628 TOD13 | Word DB13.DBW42 쓰기 |
| Coeff.COEFF_TC06 | 0676 RID82 NID12 UID385 AO208; BAD8→0674 TOD4 | Int DB4.DBW26 읽기 |
| Coeff.ZERO_TC06 | 0676 RID83 NID12 UID386 AO192; BAD8→0674 TOD4 | Int DB4.DBW24 읽기 |
| Data.Temp_T6 | 0676 RID84 NID12 UID387 AK=Write AO960; BAD11→0674 TOD1 | Int DB1.DBW120 쓰기 |
| Allarm.TC06_OFR | 0676 RID379 NID12 UID23 AK=Write AO173; BAD354→0674 TOD3 | Bool DB3.DBX21.5 쓰기 |

0674 DepDBBlock의 TOD로 DB 번호를 결속했다. AO는 비트 단위이므로 Word 바이트 오프셋과 직접 혼동하지 않는다. 이 온도 계측에 전용 DO/접점 출력은 확보하지 못했다. TC06 자체 전동기 기동·정역·인버터 구성은 기능상 비해당이며, 주변 버너/밸브의 출력을 TC06 것으로 복제하지 않는다.

### 2.2 원시 미러와 HMI

0398 LAD1071 NID2의 Move73(`DisableENO=true`)는 W88 ORef78→73.in, W90 73.out1→ORef79를 연결한다. W86은 선행 Move72.eno→73.en, W89는73.eno→Move74.en이다. 따라서 독립 무조건 쓰기라 단정하지 않으며 원시 미러는 환산 결과가 아니다. SAM=None와 Peripherie가 다르므로 두 원시값이 모든 시각에 같다고 보장하지 않는다.

`sources/hmi_plc_tags.csv`의 설정주소·Access Name PLC 5행:

| 태그 | 주소 | 내부 ID |
|---|---|---|
| I_TC_06 | DB13,INT42 | 00064 |
| data_DB1_DBW120 | DB1,INT120 | 00286 |
| Coeff_DB4_DBW24 | DB4,INT24 | 002D7 |
| Coeff_DB4_DBW26 | DB4,INT26 | 002C1 |
| Allarmi_211 | DB3,X21.5 | 002B4 |

HMI Int 원시 표기와 PLC Word 저장을 보존한다. CSV는 dde.cfg 설정 추출이며 실제 위젯·표시 단위·소수점·버튼·ACK·쓰기 이벤트나 온라인 값의 증거가 아니다. 비트 OFR와 Word/블록 단위 간접 접근은 구분하며 외부 Writer·전체 DB전달을 이 명명 태그 검색만으로 배제하지 않는다.

## 3. 제어·환산·소유

### 3.1 TC06 고유 호출

0492 LAD1742 NID12:

- ON ORef382(0678 RID1) W389→Contact395.operand, rail W397→395.in. 395.out W396→CRef376.en.
- ON ORef383 W390→376.IN0. EN과 IN0가 모두 ON이지만 현재 TRUE를 뜻하지 않는다.
- ORef384 TC06 W391→376.Analog_input;385 계수 W392→Coeff;386 제로 W393→Zero.
- 376.OutValue W394→387 Temp_T6, 376.Out_of_range W24→23 TC06_OFR.
- CRef376 RID351은 0680 BlockInterfaceInfo, 내부 CodeBlock388 RID5는0672 `Signal linearization`이다. Local 함수 인터페이스와 Global TC06 저장부를 섞지 않는다.

### 3.2 공유 함수 핵심 재대조

0291 NID1 및0014 NID2, 0611 Local InterfaceAccess·0612 상수 선언을 확인했다. 0611 RID1 IN0 Bool, RID3 Analog_input Int, RID8 Zero Int, RID13 Coeff Int, RID19 OutValue Int, RID26 Out_of_range Bool이며 App5/App6/App3/App4는 Local DInt다.

0291 Contact255(IN0)→W256에서 유효 `raw>-1382 AND raw<=32767`를 Gt258/Le161로 검사한다. Convert164/167/174는 Int→DInt, Add170/Mul177/Div181의 계산은 `(DInt(raw)+DInt(zero))*DInt(coeff)/28000`, Move185→OutValue다. ENO 연쇄 W227/230/234/237/241/245를 생략하지 않는다. Real 계산이나 임의 °C 배율을 넣지 않는다. 정수 오버플로·절삭과 비활성 호출시 값 유지/초기화의 실제 결과는 CPU 미검증이다.

범위 이탈 raw>32767(Gt190) OR raw<=-1382(Le259)→OR47 W49→Move193.en; -9999 ORef218 W252→193.in;193.out1 W253→OutValue. **193.eno W21→Coil23.in**, ORef24 W22→Coil23.operand=Local Out_of_range다. 범위 비교 결과와 ENO 코일을 같다고 치환하지 않는다. Int 상한 초과 가지의 정적 존재와 실제 도달성도 별개다.

0014 NOT IN0 Contact171→W172→Move162(0)→W170 OutValue. TC06 호출 EN도 ON으로 묶이므로 IN0가 OFF일 때 0014가 반드시 실제 실행한다고 단정할 수 없다. 0/-9999는 원본 대체값이며 안전 대체값·현행 보호값을 뜻하지 않는다.

### 3.3 소비·별칭의 경계

고유 명명 선언 검색과 network-map 연결은 TC06에 대해0398/0492를 식별한다. live_index `_7ev/1543`은 IW278/int/temperature control outputab-01, `_7ev/1742`는 위 환산호출을 보충한다. `_7ex/10` STL의 Temp_T6 로드는 `//` 주석이고 활성 값은 Temp_TC03다. 이를 TC06→MV01 PID로 세지 않는다. `_7ev/1629`의 인터페이스 주석에는 t5_t6_max_all 같은 오래된 이름이 있으나 TC06 고유 선언·핀·타이머 결속은 확보되지 않았다. 전체 간접 주소·외부 Writer의 부재 증명으로 확대하지 않는다.

AB01은 OEM 측정 역할의 관련 설비이고 CC01은 시공 위치다. 어느 쪽도 TC06 조사 한 건으로 본체 완료가 되지 않는다. CC01 본체 전용 자료 미확보를 유지하고 추가 전체 검색은 하지 않는다.

## 4. 전기 끝점·실제 PDF 판독

4쪽 모두 실제 원본 PDF를 렌더하고 이미지로 확인했다. FG와 PDF 페이지는 아래처럼 개별 대조했으며 일반식으로 가정하지 않았다.

| 자료·실제 페이지 | 양 끝점·판본 |
|---|---|
| Electrical_Rev2.pdf FG78/PDF79 | +24Vdc10.7→X1:195의5×20 50mA F→78.1→TC06 +5. TC06 -6→X1:196→+PEW278/106.6. 차폐→X1:197→78SCH1/106.6. 4–20mA,0/1300°C. 제목 THERMOCOUPLE,DATE27.05.2024,REV2/17.03.2025,FG78/TOT262 |
| 같은 PDF FG106/PDF107 | +PEW278→단자14 I3+, 채널 U3-/I3- 단자16→공통12/8/4 및18 MANA/-0Vdc10.6. 78SCH1은 차폐접지. CPU515/MOD3, TEMPERATURE CONTROL OUTPUT AB-01(TC-06),4–20mA. DATE27.05.2024,개별 개정란 기입 관찰 없음 |
| Electrical_Can_Decoating_20241118.pdf PDF23 | CANDC-CONS-E006-023,ENTRY ROUTE CONDUIT PIPING(3),TOTAL23/64,D-PAGE6. 행10 Pipe16 TC06,LOC CC01,TAG TC06,케이블3_14=ENT+CC01-TC06A,KX1.0/2심. REV1/24.11.11 first draft design,CHECKED/APPROVED 공란 |
| 같은 시공 PDF53 | CANDC-CONS-C003-053,CABLE SCHEDULE(2),TOTAL53/64,D-PAGE3. 행3_14=ENT+CC01-TC06A,FROM CR→TO CC01/TC06,Current Type TC,SPEC KX,CORE2S,SIZE1.0,SPARE0,ROUTE100RBD1→E1000,Adjustment11,LEN41. REV1/24.11.11 first draft design,CHECKED/APPROVED 공란 |

시공 PDF53의3_5는 검은 마스킹이다. 숨겨진 추출문자를 해석·복원하거나 근거로 쓰지 않는다. OEM 출력4–20mA와 시공 TC/KX를 자동으로 동일 배선구간으로 합치지 않는다. 프로브→송신기→PLC의 구간 분할, 열전대 실제 타입·냉접점 보상·연장/보상선 실제 접속, 송신기 위치·모델·교정이 필요하다. 도면의 +5/-6는 인쇄 극성이며 현재 정상극성 검증이 아니다. 이 TC06 입력회로에 릴레이 부하접점은 확인되지 않아 다른 설비의 부하5/9나 하단접점표1/5/9를 가져오지 않는다. LEN41도 현행 실측값이 아니다.

## 5. 고유 경보·타이머·복구

확보한 TC06 직접 경보는 `TC06_OFR` 한 개다. 0492 Out_of_range→DB3.X21.5 Bool 쓰기와 HMI Allarmi_211 주소를 연결했다. 생성 원리는0291 Move193 ENO→Coil23이며 SCoil/RCoil이 아니다. 고유 지연 타이머는 이 호출/함수에 없다. TC06 고온/저온 타이머의 전역 부재를 주장하는 것이 아니라, 고유 원본에서 확인되지 않은 상태다.

공통 HMI Reset 요청 전달(AB01 초안의0158/0154)과 TC06 OFR의 자체 생성은 별개다. 그 공유 설명을 TC06 전용 Reset 허가로 바꾸지 않는다. 본 호출/함수에는 RESET_ALLARM 입력이나 TC06용 수동 Reset 가지가 확인되지 않는다. 실제 ACK·혼/램프·전체 Word 쓰기·경보 표시·재발·안전정지 효과는 미확정이다. OFR 꺼짐, HMI ACK, 입력값 정상, 기계 복구 완료를 서로 대신하지 않는다.

현재 값·계수·제로·온도 안전설정·원인해소를 확인하지 않은 상태에서 Reset/강제값/시험신호/재시동을 권고하지 않는다. 실제 복구 판정에는 승인된 현장 원인확인·조치와 별도 운전 승인/관찰 증거가 필요하다.

## 6. 증상별 읽기 전용 관찰 계획

| 증상 | 같은 시각의 관찰 | 비교·배제 및 미확정 |
|---|---|---|
| HMI 온도와 기대가 다름 | IW278:P,IW278,DB13W42,DB1W120,HMI 주소·값·시간 | 원시/환산 혼동,접근·갱신주기,Int/Word 표시,제로/계수·단위를 대조 |
| -9999 또는 OFR 표시 | 호출EN/IN0,raw,DB4W24/W26,DB3X21.5,MoveENO | 범위·연산·비활성호출과 실제 단선/전원/보상 문제를 분리; 원인 단정 금지 |
| 값0/고정값 | ON/호출상태,원시/환산 추세,통신 신선도 | IN0=OFF 경로와 호출EN=OFF를 구별; 값0만으로 실제0°C 판정 금지 |
| 고온인데 경보 없음 | 실제 표시주소,온도·OFR·관련 설비 알람과 시각 | TC01/02/03 알람을 TC06 것으로 기대하지 않음; 승인 보호계통 자료 필요 |
| TC06 위치가 도면마다 다름 | 명판·태그·변환기 위치·케이블3_14·X1:195~197 | AB01 기능/CC01 위치·KX/4–20mA 구간 확인; 본체 소유 배정 금지 |
| ACK 후에도 표시 유지 | raw/환산/OFR,실제 HMI ACK 이벤트 및 공통요청 | OFR 직접 재계산과 래치 Reset을 혼동하지 않음; 현장 복구는 별도 |

관찰 기록은 관찰자·시각/시간대·설비 위치·태그/주소·수치/단위/신선도·수집장치·CPU/프로젝트 식별·비교 원본/개정·원인배제·승인조치·복구확인을 분리한다. 이 표는 관찰 계획이며 전기 접근·센서 탈거·신호주입·보호값 수정·리셋·재시동 지시가 아니다. 실제 운영 기록을 생성/복제하지 않았다.

## 7. 완료·검증·누락

| 구분 | 상태 |
|---|---|
| documentation | draft_complete_with_gaps,TC06 한 개 7영역 |
| static_review | 고유 핀·선언·PDF 대조 완료,부모 독립검토 대기 |
| ui_records | not_run |
| publication | not_published,제품통합 없음 |
| tia_compile/live_cpu/field_recovery | not_performed |

도면·래더 비교는 문서상 원본 위치까지 준비했으나 실제 앱 링크/UI는 미검증이다. 백업·선택 복원,기록 전후 비교,관찰보고서/PDF의 TC06 지원·저장/재읽기/재열기·실패/동시성 검사는 하지 않았다. 기존 note/repair_observation/미지필드·타설비·초안·저장키는 보존했다. 원본 PDF 렌더는 현장보고서 출력시험이 아니다.

직접 의미검토는0492 전체 고유 환산호출,0398의TC06 Move73 경계,0291/0014 공통함수 핵심,고유 명명 선언·HMI5행·PDF4쪽이다. 기타 추출/해시파일 전체를 의미검토 완료로 세지 않는다. core source에 고유 timer/SR가 없다는 확인과 모든 간접 경로의 부재 증명은 구분한다. 검사는 자체 XML파싱·문서검사·원본 SHA/Git blob·중지자산 보존에 한정하며 원본 test/build/generator는 실행하지 않았다.

필요 자료: 승인 준공도와 실제 TC06/송신기/보상선 구간,허가된 현재 프로젝트/CPU 주소·전체 호출/Writer 대조,현행 계수/제로/교정·승인 보호계통,실제 HMI 화면·ACK·통신·권한,승인 현장관찰·조치·복구 결과. 새 자료가 없으면 CC01 본체 또는 실물보류를 반복 조사하지 않는다. 다음은 부모의 고유 핀/상충 독립검토다. 이 초안은 제품통합이나 현장 변경을 승인하지 않는다.

### 실제 작업 단계 시각 (UTC)

- 2026-10-11T11:14:52Z — instructions_and_scope_read
- 2026-10-11T11:16:07.685059+00:00 — xml_extraction
- 2026-10-11T11:16:21Z — four_actual_pdf_renders_visually_reviewed
- 2026-10-11T11:19:26.195054+00:00 — seven_area_draft_written
- 2026-10-11T11:20:17.265451+00:00 — static_assertions_and_fixed_blob_hashes_verified

### 선택 원본·중지 자산 해시 전체 목록

선택 원본·맥락·보존 47파일의 SHA-256와 고정 Git blob 내용이 모두 일치했다. 중지5자산 freeze 해시 일치,원본 Git 변경0. 파일 수는 의미검토 수가 아니며 임의로90개를 채우지 않았다. 검사JSON은 extracts/TC06/static-review.json,해시JSON은 extracts/TC06/source-hashes.json이다. 전체 목록의 각 행은 fixed commit과 내용 동일(true)이며 OID는 git rev-parse,내용은 git show로 대조했다.

| 원본 경로 | SHA-256 | 고정 Git blob OID |
|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` |
| `.agents/skills/gme-equipment-rollout/references/source-map.md` | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` |
| `all-in-one/sources/decoded-original/0492-FlgNet.xml` | `f97288e870de4e6d3528ebc194428d0fb961b9893d661ed875ad8170fa90653b` | `a161757eb8c94525c2211d354e2ca2cfec21b97c` |
| `all-in-one/sources/decoded-original/0548-FlgNet.xml` | `cc21a5b04a0d17b1d0ce7dceca752b6570ccd9d961c0ec3c6c5c734f648ae83e` | `149b184192970060f32956ec81a8408c7f7a30b1` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` | `985b5310b43b1015b5dee286aa0e42800564b94b` |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` |
| `all-in-one/sources/decoded-original/0690-IdentXmlPart.xml` | `fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541` | `36bd403f48ba8e364126837b19fb0419bbe78941` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |
