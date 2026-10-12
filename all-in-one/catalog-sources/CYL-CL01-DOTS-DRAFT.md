# CYL-CL01 고유 구성품 원본 조사 초안

- 대상: CYL-CL01, 공압 실린더, PV01 하위 component, phase2. CLIENT-CL01 외부 모터와 별개다.
- 고정 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION v1.12.0. 작성 2026-10-11 UTC.
- 기준: GME-STD-1.0.0; BATCH19-RESEARCH-INSTRUCTIONS 및 TASK3-BATCH19-SCOPE의 CYL-CL01 한 개만 조사했다. 다른 설비의 완료를 상속하지 않는다.
- 결과: P&ID의 EV01→CL01/CL02 공압 분기와 CL01 쪽 LS01/LS02 리더를 확인했다. PLC와 전기도면 신호 소유는 PV01 Gate A/EV01이다. CL01 고유 전용 출력·코일·알람·HMI 객체를 확인한 것으로 표시하지 않는다.
- 작성 범위: 자신의 `drafts/CYL-CL01-DOTS-DRAFT.md`와 `extracts/CYL-CL01/`만 변경. 원본, 공통 코드, 버전, 대장, 배포, 운영/SEJIN, PLC·현장·보호값은 변경하지 않았다. 시뮬레이터·원본 생성기·앱 빌드·행동시험은 실행하지 않았다.
- 원본 표준·시작 문서와 최신 원본 상태를 읽었으며 시작 Git status는 clean이었다. 실제 실행 모델/추론 설정은 독립 관측 자료가 없어 미확인이다.

## 1. 설비·자료 기준

### 1.1 분류와 독립성

`docs/equipment-standard/INVENTORY.json#/catalog/201`은 CYL-CL01의 parent_id=PV01, depth=1, phase2, planned, existing_detail=baseline, bc01_standard_acceptance=not_assessed를 기록한다. `all-in-one/registers/equipment.json`의 id=CYL-CL01 행은 aliases=[], fgs=[], pid=true, parent=PV01이며 “독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검”하는 역할과 CLIENT-CL01 구분을 명시한다. 이 두 행은 분류 근거이지 실물 확인서가 아니다.

`progress/GME-CATALOG-OVERLAP-REVIEW.json` 해당 행의 parent_child_separate, physical_identity_verified=false, confirmed_alias_duplicate=false를 유지한다. PV01과 하위 구성품을 별도 문서화하되 부모의 단일 출력이 CL01 전용 출력으로 바뀌지 않는다. LS01과 번호가 같다는 이유로 실린더와 센서를 동일 물체로 병합하지 않는다.

### 1.2 고유 P&ID 관찰

원본 `all-in-one/sources/PID_1684n002I.pdf`, 실제 PDF1, 표제 UBC AND SCRAPS DECOATER 10 Ton/h / P&I, 도번 1684n002, Apex I. 기본 날짜 06/04/2011, 개정 I 15/01/2013. FG 칸은 ‘–’다. 확대 렌더 `pid-detail.png`, `pid-title.png`로 다음을 독립 확인했다.

- PV-01 Detail의 COMPRESSED AIR 공통선에서 EV-01 분기가 나와 CL-01과 CL-02 두 실린더 기호로 이어진다. EV-02→CL-03/04는 다른 분기다.
- CL-01은 위쪽 EV-01 실린더 기호다. LS-02 리더는 그 기호의 몸체 쪽, LS-01 리더는 로드 쪽으로 연결된다. 이 페이지의 CL-02 기호에는 별도 LS-03/04 리더가 표시되지 않는다.
- 이는 P&ID의 명명·도식 연결 관찰이다. 실제 센서가 CL01 어디에 설치되었는지, 동작점·정상극성·행정·보어·스풀 포트·공압 호스번호·실물 제조사/모델은 확인되지 않았다.
- 같은 박스 오른쪽 기계 형상의 GATE “A”/“B” 문자가 각 EV 분기와 일대일로 연결되는 선은 없다. 그 글자 위치로 CL01의 실물 상/하 게이트 위치를 확정하지 않는다.
- P&ID 계장 표기와 2024/2025 전기도면 사이에는 시점 차이가 있다. 최신 승인 준공자료로 자동 승격하지 않는다.

### 1.3 재사용한 부모 조사와 제한

`drafts/PV01-DOTS-DRAFT.md`를 공통 제어·알람·HMI 탐색색인으로 재사용했다. 부모 초안 전체를 다시 조사하지 않았다. 특히 부모 초안의 69KA1 접점 1/9 서술은 고정 원본 `WORKSPACE-HANDOFF.md`와 `PUBLICATION_STATUS.md`의 v1.11.1 정정 및 이번 FG69 렌더를 따라 **실제 EV01 부하 경로 5–9**로 읽는다. 기존 수신 초안은 수정하지 않았다. 71KA 계열 5–9 정정도 보존 원칙이며 이번 CL01 회로에는 71KA를 붙이지 않는다.

## 2. I/O·HMI와 소유

아래 주소는 고정 PLC 백업 선언이며 현재 CPU 주소/값으로 검증한 것이 아니다. 원본 XML 경로 접두사는 `all-in-one/sources/decoded-original/`이다.

| 항목 | 원본 선언·참조 | 백업 주소/의미 | CYL-CL01 경계 |
|---|---|---|---|
| PV-01 Gate a | 0607-IdentXmlPart.xml RID50, SSD AO42, SAD Output; NID4 UID394 Write | Q5.2 Bool, EV01 출력 | CL01/CL02 공통 상위 구동; CL01 전용 출력 아님 |
| EV01_Open | 0607 RID124, AO70 Input, NID11 UID38 | I8.6 Bool, LS01/Gate A open | P&ID CL01 쪽 리더와 관계 있음; PLC 이름은 게이트 응답 |
| EV01_Close | 0607 RID126, AO71 Input, NID11 UID44 | I8.7 Bool, LS02/Gate A close | FG124 SPARE 상충 유지 |
| Inputs.FC GATE A OPEN | 0609 RID125 AO70, BAD BIRID86; 0608 RID86 Inputs TOD13 | DB13.DBX8.6 | 원시 I8.6과 별도 경로 |
| Inputs.LIMIT SWITCH LS-02GATE A CLOSEDVALVE PV-01 | 0609 RID127 AO71, BAD86 | DB13.DBX8.7 | 원시 I8.7과 별도 경로 |
| Flag.PV_01_GATE_A_MEM_OPEN/CLOSE | 0609 RID10 AO65 / RID128 AO64, BAD5; 0608 RID5 Flag TOD2 | DB2.DBX8.1 / DB2.DBX8.0 | 게이트 위치 기억. 실린더 독립 센서나 현물 위치 아님 |
| ON | 0607 RID1 Memory AO0, NID4 UID385 / NID11 UID36 | M0.0 Bool | 참 상수로 치환 금지 |
| Open EV A 00 PV-01 / Open EV A 01 PV-01 | 0607 RID44 AO160 / RID20 AO171; NID4 UID391/392 | M20.0 / M21.3 | 현장·자동의 상위 요청 |
| maintenance PV01 | 0607 RID47 Memory AO645, NID4 UID393 | M80.5 | 부모 공통 유지보수 경로; CL01 독립 명령 아님 |

AO는 비트 오프셋으로 42=5×8+2, 70=8×8+6을 대조했다. DB 멤버는 BAD와 DepDBBlock TOD까지 결속했다. 동일 RID 숫자를 다른 파일·블록의 동일 변수로 합치지 않았다.

### HMI

`all-in-one/sources/hmi_plc_tags.csv` 행658/659/660/665에서 PV_01\GateA_Open=DB11,X76.1, Flag=DB2,X5.0, GateA_Close=DB11,X76.2, Allarme1=DB11,X76.0 설정을 확인했다. 이는 PV01 화면 자료이며 CL01 전용 표시·버튼의 증거가 아니다. 실제 버튼 이벤트/권한/실인수 결속은 이 CSV로 알 수 없다. 부모 초안의 HMI PV_2Gate 호출 CRef32와 17개 미결속 실인수는 이번에 해결하지 않았으며 CRef를 CL01 호출로 재명명하지 않는다.

원본 decoded-original/*.xml 695개와 위 HMI CSV에서 `(?:CYL[-_ ]*)?CL[-_ ]*0?1(?!\d)` 대소문자 무시 검색 결과 직접 일치 파일/행은 0이다. 검색 범위·패턴·결과는 `signal-search.json`. **695개는 어휘 검색수이며 의미 검토수나 고유 신호 부재의 증명수가 아니다.** 다른 이름/외부 장치/미제공 도면의 존재는 배제하지 않는다.

## 3. 제어 구조

### 3.1 상위 요청→Q5.2

독립 대조한 `0279-FlgNet.xml` (부모 색인 LAD1915, 선언 NID4):

- Contact410 ON은 W395/ORef385→0607 RID1이다. 410.out→W411이 A 분기의 Contact420/422/424.in으로 공급된다.
- Contact420.operand는 W403/ORef391/RID44, 420.out→W421→OR380.in1.
- Contact422.operand는 W404/ORef392/RID20, 422.out→W423→OR380.in2.
- Contact424.operand는 W405/ORef393/RID47, 424.out→W425→OR380.in3.
- OR380.out→W406→Coil384.in, Coil384.operand W408/ORef394→RID50 Q5.2.
- 정적 식은 Q5.2 = ON AND (OpenA00 OR OpenA01 OR maintenance PV01). 이 네트워크의 A 분기에는 전용 CL01 접점·코일·CRef 호출이 없다. 실행·스캔·온라인 최종값은 검사하지 않았다.

상위 자동 허용/알람이 모든 경로에 직접 직렬 삽입된 것으로 쓰지 않는다. CL01 단독 정지/단독 열기 명령을 새로 만들지 않는다. PLC Q=0은 전기 명령 해제일 뿐 실린더 수축이나 게이트 닫힘 확인이 아니다.

### 3.2 원시 입력→상위 위치 기억

독립 대조한 `0286-FlgNet.xml` (부모 색인 LAD1921, NID11):

| 처리 | Part/Wire/ORef 직접 결속 | 정적 의미 |
|---|---|---|
| A MEM_OPEN Set | ON21→W51→Q22→W53→23(raw)/24(DB)→W55/W57→OR25→W58→S26; 대상 W59/ORef40 RID10 | ON AND Q5.2 AND (I8.6 OR DB13X8.6) |
| A MEM_OPEN Reset | W51→NOT27→W61→R28; Q operand W60/ORef41 RID50; 대상 W62/ORef42 RID10 | ON AND NOT Q5.2 |
| A MEM_CLOSE Set | W51→NOT29→W64→30(raw)/31(DB)→W66/W68→OR32→W69→S33; 대상 W70/ORef46 RID128 | ON AND NOT Q5.2 AND (I8.7 OR DB13X8.7) |
| A MEM_CLOSE Reset | W51→34→W72→R35; Q operand W71/ORef47 RID50; 대상 W73/ORef48 RID128 | ON AND Q5.2 |

원시 open23 W54/ORef38→RID124, DBopen24 W56/ORef39→RID125; rawclose30 W65/ORef44→RID126, DBclose31 W67/ORef45→RID127로 결속했다. 위치 기억에 원시/DB 병렬 경로가 있으므로 HMI 표시나 MEM만 보고 CL01 물리 이동 완료를 판정할 수 없다. 부모 startup/Inputs 전달/다른 쓰기·호출 조건은 부모 공통 조사에 남기며 이 문서에서 단독 소유를 주장하지 않는다.

## 4. 전기 끝점과 공압 경계

### 4.1 실제 렌더와 페이지별 개정

| 원본 | 실제 PDF 페이지 | FG/표제 | 페이지별 개정 |
|---|---:|---|---|
| PID_1684n002I.pdf | 1 | 1684n002, PV-01 Detail; FG ‘–’ | Apex I, 15/01/2013; 기본 06/04/2011 |
| Electrical_Rev2.pdf | 70 | FG69 LOAD DRUM CLAPPE VALVE PV-01 | 개정란 공란; 기본 27.05.2024 |
| 같은 파일 | 71 | FG70 같은 표제 | 개정란 공란; 기본 27.05.2024 |
| 같은 파일 | 125 | FG124 DIGITAL INPUT MODULE | Rev2 17.03.2025; 기본 27.05.2024 |
| 같은 파일 | 142 | FG141 DIGITAL OUTPUT MODULE | Rev2 17.03.2025; 기본 27.05.2024 |

총 실제 PDF 5페이지를 렌더·시각검토했다. PDF명 Rev2를 전체 페이지의 개정 번호로 쓰지 않는다.

### 4.2 EV01 구동과 CL01

1. DC 제어측: FG141/PDF142 MOD15 단자13, A5.2→69/3 교차참조→FG69/PDF70 69KA1 A1; 코일 A2→−0Vdc 10.6. FG141 전원은 +24Vdc 10.9→X21/3033 도면 5×20 4A F→선141.1→모듈 공급단자, 20→−0Vdc 10.6로 표시된다. 실물 보호값을 확인한 것은 아니다.
2. AC 부하측: 110Vac 9.7→69KA1 **접점5–9**→선69.1→X1/126 (5×20 2A F 표기)→선69.2→EV01 A1. EV01 A2→X1/127→0Vac 9.9. 접점표의 1/5/9 전체를 실제 부하선 1–9로 잘못 옮기지 않는다.
3. 기계/공압측: P&ID PDF1의 EV01 분기→CL01과 CL02. 전기 끝점은 EV01 코일이며 CL01에 AC 배선이 직접 들어간다는 근거가 아니다. 솔레노이드 코일과 공압 실린더를 분리한다.
4. EV01 출구 포트/튜브 번호→CL01 양 포트, 실물 69KA1 접점 상태, 현재 코일 명판, 잔압/복귀 방식은 미확정이다. 도면에서 미확보된 케이블/호스 번호를 생성하지 않는다.

### 4.3 LS01/LS02 피드백의 두 끝점

- LS01: FG70/PDF71 +24Vdc 10.7→X1/130(5×20 2A F 표기)→선70.1→LS01 접점13→14→X1/131→E8.6 교차참조124/6→FG124/PDF125 MOD10 단자7 E8.6(I8.6). PLC 이름은 EV01_Open이다.
- LS02: 같은 +24Vdc→X1/132(2A F 표기)→선70.2→LS02 접점13→14→X1/133→E8.7 교차참조124/6→FG124 MOD10 단자8 E8.7(I8.7). PLC 이름은 EV01_Close다.
- FG124 E8.7 위쪽에는 SPARE 점선 표기가 있으나 하단 설명은 LIMIT SWITCH LS-02 GATE “A” CLOSED VALVE PV-01이다. FG70 실회로와 PLC 선언/사용도 존재한다. 삭제·미설치·항상0으로 정리하지 않는다.
- P&ID의 CL01 리더 연결은 센서와 구동 묶음을 좁히는 근거다. 전기도면은 LS01/02를 Gate A 센서로 명명하므로 CL01 독립 고장진단/정상극성은 미확정이다. 접점13/14 도식만으로 현재 물리 위치별 0/1을 확정하지 않는다.

## 5. 알람·복구

- 이번 CL01 직접 이름 검색과 선택 XML에서는 CL01 전용 알람 RID, 고유 타이머, 독립 리셋 또는 HMI 알람 객체를 확보하지 못했다. 물리적으로 존재하지 않는다는 결론은 아니다.
- 부모 PV01 A/B NOT_OPEN/NOT_CLOSE 및 A 4초/B 7초 감시는 부모 공통 조사 사항이다. 이 초안은 그 원본 타이머/알람 전체를 재조사하지 않았으며 **CL01_NOT_OPEN** 같은 별도 항목으로 복제하지 않는다.
- 부모 위치 기억과 원시 입력/DB 경로, EV01/공압/두 실린더가 연결되므로 부모 알람 하나로 CL01만 고장났다고 판단할 수 없다. CL02, EV01, 공압 공통선, LS01/02, 입력 전달, 링크/기계 저항을 구분할 자료가 필요하다.
- 알람 해제와 재요청, Q 출력, 실제 이동, 센서 응답은 각각 기록한다. 리셋 성공=실린더 복구 완료가 아니다. 현장 리셋·강제출력·우회·설정변경 또는 움직임 시험은 이번에 수행하지 않았다.

## 6. 증상별 관찰·수리 근거

아래는 이미 허용된 관찰에서 모을 증거 목록이다. 현장 조작·통전 측정·임의 수리 지시가 아니다. 값이 없으면 빈칸으로 남기며 0으로 채우지 않는다.

| 증상 | 분리해 기록할 관찰 | 비교 근거/배제 경계 | 필요한 후속 자료 |
|---|---|---|---|
| CL01/CL02가 함께 움직이지 않음 | 요청/M20.0/M21.3/M80.5, Q5.2, EV01 명판·상태, 공압 공급의 관측 시각 | 0279 상위 명령과 FG141→69KA1→EV01, P&ID 공통 분기; 바로 실린더 불량 단정 금지 | 승인 계측기록/배선·공압 포트 추적 |
| CL02는 움직이고 CL01만 반응 없음 | 두 실린더 명판/장착 위치와 같은 시각의 이동·링크 관찰 | 공통 EV01 출력만으로 개별 행정/부하를 알 수 없음 | 실제 호스·피팅·실린더·링크 조립도 |
| 실물 이동과 open 표시 불일치 | CL01 위치, LS01 상태, I8.6, DB13X8.6, MEM_OPEN, HMI 표시를 따로 기록 | 0286 raw/DB OR 및 S/R; 하나의 표시로 물리 이동 판정 금지 | 센서 설치사진, 정상극성, HMI 실제 이벤트/결속 |
| 닫힘 표시 누락/항상 표시 | LS02, I8.7, DB13X8.7, MEM_CLOSE 및 CPU 근거 | FG124 SPARE와 FG70/PLC 사용 상충 | 승인 현행 I/O 리스트·단자대·센서 추적 |
| 부모 위치 알람 반복 | 알람 이름/발생·해제 시각, 요청/Q/raw/DB/MEM 및 두 실린더 동작 자료 | 부모 알람을 CL01 소유로 변경하지 않음 | 부모 원본 알람과 동일 시점 온라인/현장 관찰 |

관찰 기록 공통 필드: 관찰자, 시각/시간대, 장치와 위치, 프로젝트/CPU 식별 근거, 값/단위, 비교 원본·개정, 배제 사실, 승인된 조치, 조치 전후 자료와 복구 증거. 현재 데이터가 없으므로 원인·조치·복구완료를 채우지 않았다. 제조사 행정·압력·씰·토크·윤활 주기 등은 명판/공식 모델 자료 확보 전 공란이다.

## 7. 완료·누락과 검증

### 7.1 7영역 적용 판정

| 영역 | 판정 | 확보/누락 |
|---|---|---|
| 설비·자료 기준 | 적용 | CYL-CL01 고유 P&ID와 PV01 부모 관계; 실물 동일성 미확정 |
| I/O·HMI | 상위 연계 적용, 전용 근거 미확보 | Gate A/EV01 선언과 CSV; CL01 전용 객체 없음으로 단정하지 않음 |
| 제어 구조 | 상위 구동·응답 적용 | 0279/0286 원본 결속; 개별 실린더 PLC 소유 미확보 |
| 전기 전달 경로 | 상위 전기→공압 경계 적용 | 릴레이·EV·센서 두 끝점; 실제 호스/케이블 심선·현행 부품 미확정 |
| 알람·복구 | 상위 연계, 고유 근거 미확보 | 부모 알람을 독립 항목으로 복제하지 않음; 현장 복구 미수행 |
| 증상 관찰 | 적용 | 공동/개별 원인 분리 자료 목록; 실제 진단·수리 미수행 |
| 완료·누락 | 적용 | 문서 정적 상태와 UI/게시/CPU/현장 분리 |

### 7.2 검사수와 의미검토수

- 선정 원본 **14개**의 전체 SHA256 및 고정 Git blob 바이트를 비교: **14/14 일치**. 부록 표와 `source-verification.json`에 전체 값 보관.
- 의미 검토: 고유 P&ID 실제1페이지, 연계 전기 실제4페이지, FlgNet 원본2개(0279/0286), 선언 XML3개(0607/0608/0609)의 해당 선언·DB·핀, HMI CSV의 PV01 8행과 대장2행. 나머지 XML의 695개 어휘 검색을 의미검토 695개로 보고하지 않는다.
- JSON/XML 파싱, 파일 바이트 SHA256/Git show 비교 및 PDF 렌더만 수행. 실행 모델/PLC 동작 시험이 아니다. 선택 원본의 14개 검사와 원본 저장소 전체 해시 검증을 구분한다.
- 독립 검토는 부모의 후속 검토 대상으로 남긴다. 자체 확인만으로 독립 검토 완료라고 하지 않는다.

### 7.3 네 기능과 최종 상태

| 기능 | 이 초안에서의 상태 |
|---|---|
| 도면·래더 나란히 보기 | 연결할 원본·페이지·핀 제공; CYL-CL01 UI 구현/링크 검증 미실행 |
| 백업 미리보기·선택 복원 | 저장 스키마/키/미지 필드 변경 없음; CYL-CL01 적용 검증 미실행 |
| 전후 기록 비교 | 관찰 항목만 정의; 구현·저장·재열기 검증 미실행 |
| 관찰 보고서/PDF | 보고서 앱 생성·출력 검증 미실행; 원본 PDF 렌더와 별개 |

| 상태 | 결과 |
|---|---|
| documentation | draft_complete_with_gaps: 고유 하위 구성품 근거/소유/누락 작성 |
| static_review | self_review_complete; independent_review_pending |
| ui_records | not_run |
| publication | not_published_by_this_task |
| tia_compile | not_performed |
| live_cpu | not_performed |
| field_recovery | not_performed |

다음 좁은 확인: CL01 명판·두 공압 포트/호스와 LS01/LS02 실제 설치 위치를 하나의 승인된 현행 도면/사진 세트로 확인하고 FG124 SPARE 충돌을 해소한다. 자료 없이 반복 조사하거나 CL01을 CLIENT-CL01로 합치지 않는다. 현재 CPU, 실물 동일성, 정상극성, 보호값, 현장 복구는 미확정으로 유지한다.

## 부록 A. 선정 전체 원본 SHA256 / Git blob

경로는 고정 `source-mv06/` 기준이다. Git commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`. Git blob ID와 해당 blob 바이트의 SHA256을 각각 계산했고, 로컬 전체 바이트와 정확히 같음을 확인했다. 부모 초안·작업 범위 JSON은 탐색/배정 자료로 사용했으며 PLC 원본 검증수에 포함하지 않았다.

| 고정 원본 상대경로 | SHA-256 (전체 파일) | Git blob | 바이트 일치 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | PASS |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | PASS |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | PASS |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | PASS |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | PASS |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | PASS |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | PASS |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | PASS |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | PASS |
| `all-in-one/sources/decoded-original/0279-FlgNet.xml` | `4ae9c9ae70987b778a159c896b88fa4e34cf6f597903a0c68e630708b5f1bfd1` | `dfefe5fcd17064a89f61e38f34e9c4d7bb1d01e5` | PASS |
| `all-in-one/sources/decoded-original/0286-FlgNet.xml` | `dca38f0104a47f95095b88a86400e379d653dd26b0e2fc88e1b3d17612268828` | `756366ed44352d07dd0b7af823d5493d84e920b8` | PASS |
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | PASS |
| `all-in-one/sources/decoded-original/0608-IdentXmlPart.xml` | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | PASS |
| `all-in-one/sources/decoded-original/0609-IdentXmlPart.xml` | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | PASS |

## 부록 B. 자체 증거 산출물

- `extracts/CYL-CL01/source-verification.json`: 14개 전체 해시·Git blob·바이트 일치 및 검사 범위.
- `extracts/CYL-CL01/xml-evidence.json`: 지정 FlgNet 두 원문 및 RID 선택 선언, Flag/Inputs DB 결속.
- `extracts/CYL-CL01/signal-search.json`: 695 XML 어휘 검색과 HMI PV01 8행; 검색의 음성 결과 범위.
- `extracts/CYL-CL01/catalog-row.json`: CYL-CL01 장비 행.
- `extracts/CYL-CL01/pid-full.png`, `pid-detail.png`, `pid-title.png`: 실제 PDF1 전체/고유 상세/개정란.
- `extracts/CYL-CL01/electrical-p70.png`, `electrical-p71.png`, `electrical-p125.png`, `electrical-p142.png`: 실제 전기 PDF 네 페이지 렌더.

고유 선언/핀을 찾지 못한 곳에는 N/A 또는 근거 미확보를 썼다. CL01 실린더 자체의 RID·NID·Part·Wire·ORef·CRef를 부모 신호 번호로 새로 만들지 않았다.
