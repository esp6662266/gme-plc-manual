# LS01 고유 구성품 원본 조사 초안

- 대상: LS01(별칭 ls-01, ls.01), 밸브 위치 리미트 스위치, PV01 하위 component / phase2.
- 기준: GME-STD-1.0.0; 고정 `source-mv06` Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION v1.12.0. 조사일 2026-10-11 UTC.
- 결과: LS01의 OEM Gate A OPEN 명칭, P&ID CL01 쪽 리더, X1/130–131→I8.6 및 raw/Inputs/위치 기억의 구분을 확인했다. 물리 정상극성·현재 CPU·실물 동일성·현장 복구는 미확정이다.
- 범위: `drafts/LS01-DOTS-DRAFT.md` 및 `extracts/LS01/`만 작성. 원본/대장/공통 코드/배포/PLC/현장/보호값/SEJIN 변경 없음. 시뮬레이터 작성·수정·생성·실행·행동시험, 원본 생성기 및 앱 빌드는 수행하지 않았다.
- 시작 시 원본 Git 상태 clean, HEAD 고정값 일치. AGENTS/스킬/표준/템플릿/대장 및 최신 시작 문서를 읽었다. 실행 모델·추론 설정은 별도 관측자료가 없어 미확인. 독립 검토는 부모 후속 작업이다.

## 1. 설비·자료 기준

### 분류와 소유

`docs/equipment-standard/INVENTORY.json#/catalog/220`은 LS01의 parent_id=PV01, depth=1, phase2, planned, existing_detail=baseline, bc01_standard_acceptance=not_assessed를 기록한다. `all-in-one/registers/equipment.json`의 LS01 행은 parent=PV01, fgs=[69,70], pid=true, 별칭 ls-01/ls.01이다. FG69는 부모 구동 연계이고 LS01 접점 자체는 FG70에 그려져 있다.

`progress/TASK3-BATCH21-SCOPE.json` 및 `GME-CATALOG-OVERLAP-REVIEW.json`의 parent_child_separate, physical_identity_verified=false, confirmed_alias_duplicate=false를 유지한다. 부모 문서의 완료를 상속하지 않으며 LS01·CYL-CL01·CLIENT-CL01은 서로 다른 이름 공간/구성품이다.

`drafts/PV01-DOTS-DRAFT.md`, `drafts/CYL-CL01-DOTS-DRAFT.md`는 공통 제어·알람·전기 탐색색인으로 재사용했다. 부모 전체 제어를 반복조사하지 않았다. 부모 초안의 과거 69KA 접점1–9 서술은 원본 WORKSPACE-HANDOFF/PUBLICATION_STATUS의 v1.11.1 정정에 따라 **5–9**로 유지한다. 71KA 계열 정정도 보존하며 LS01 회로에 71KA를 새로 붙이지 않는다.

### 고유 P&ID 관찰

`all-in-one/sources/PID_1684n002I.pdf` 실제 PDF1, PV-01 Detail에서 LS-01 리더가 CL-01 기호의 로드 쪽으로 내려가고 LS-02는 몸체 쪽으로 내려간다. EV-01 공압 분기는 CL-01과 CL-02에 함께 연결된다. LS01은 EV01 코일이나 CL01 자체가 아니다. 이 기호 배치로 실제 설치면·동작점·행정 방향·현장 0/1을 확정하지 않는다.

같은 Detail의 기계 그림 GATE “A”/“B” 문자와 각 EV/실린더를 일대일로 묶는 연결선은 없다. OEM 전기도면과 PLC는 LS01을 Gate A open 응답으로 명명하지만, 도식상의 상하 위치와 실물 게이트 위치까지 자동 동일시하지 않는다. P&ID는 2013 개정, OEM은 2024 기본/2025 일부 개정, 시공 참고자료는 2024 초안이므로 모두 현행 준공도라고 부르지 않는다.

## 2. I/O·HMI

XML 경로 접두사는 `all-in-one/sources/decoded-original/`. 아래는 백업 선언이며 현재 CPU 주소/값을 확인한 결과가 아니다.

| 층위 | 원본 선언·참조 | 주소·해석 | 미확정 경계 |
|---|---|---|---|
| 물리 위치 입력 | 0607-IdentXmlPart.xml RID124 EV01_Open, SAD Input, SSD AO70 Bool, NID11 UID38 | I8.6, OEM LS01 Gate A OPEN | 현재 정상극성/접점 상태 미확정 |
| 처리 입력 DB | 0609 RID125 Inputs.FC GATE A OPEN, AO70 Bool, BAD BIRID86; 0608 RID86 Inputs TOD13; NID11 UID39 | DB13.DBX8.6 | raw와 별도 변수, 갱신/타 쓰기/호출 영향 |
| 게이트 위치 기억 | 0609 RID10 Flag.PV_01_GATE_A_MEM_OPEN, AO65 Bool BAD5; 0608 RID5 Flag TOD2; NID11 UID40/42 Write | DB2.DBX8.1, S/R 기억 | LS01 자체 값 또는 실물 위치와 동일하지 않음 |
| 상위 출력 | 0607 RID50 PV-01 Gate a, SAD Output AO42 Bool; NID11 UID37/41 | Q5.2, EV01 상위 명령 | LS01 출력 아님. CL01/02 구동과 관계 |
| 공통 접점 | 0607 RID1 ON, Memory AO0 Bool; NID11 UID36 | M0.0 | 이름만으로 항상 참 상수화 금지 |
| Word 전달 원천 | 0627 RID15 Tag_181, Input AO64 Word, NID1 UID47 | IW8 | Word8이 I8.6을 포함 |
| Word 전달 목적지 | 0629 RID16 AO64 Word BAD4; 0628 RID4 Inputs TOD13, NID1 UID48 Write | DB13.DBW8 | 전달될 때 해당 bit도 복사되지만 현재 항상 일치 보장 아님 |

AO는 비트 오프셋으로 70=8×8+6, 65=8×8+1, 42=5×8+2이다. 동일 RID 숫자는 파일/블록 범위 없이 병합하지 않았다.

### HMI 경계

`all-in-one/sources/hmi_plc_tags.csv` 행658 PV_01\GateA_Open은 DB11,X76.1 설정이다. 행660 GateA_Close=DB11,X76.2, 행665 Allarme1=DB11,X76.0 및 행659 Flag=DB2,X5.0 등 PV01 8행을 확인했다. GateA_Open 표시는 I8.6 직접 화면 객체로 결속된 증거가 아니며 LS01 전용 버튼/알람으로 바꾸지 않는다.

부모 색인의 0391 HMI PV_2Gate CRef32 호출 실인수 중 17개 미결속은 그대로 남긴다. 이번 LS01 조사에서 HMI 객체 이벤트·쓰기권한·DB11 결과 결속을 새로 해결하지 않았다. CSV 설정·raw 입력·Inputs DB·MEM·HMI 표시를 다섯 층위로 구분한다.

## 3. 제어 구조

### 3.1 LS01 raw와 처리값 → Gate A OPEN 기억

`0286-FlgNet.xml`, 부모 탐색색인 LAD1921, 선언 NID11을 직접 대조했다. CRef는 이 네트워크에 없다. 아래는 정적 핀 연결 설명이며 동작 실행이나 CPU 최종값 검사가 아니다.

| 단계 | Part / Wire / ORef / 선언 | 해석 |
|---|---|---|
| 허용 | rail W49→Contact21.in, operand W50/ORef36→0607 RID1; 21.out→W51→Contact22.in | ON 접점 뒤 Q5.2 경로 |
| Q 조건 | Contact22.operand W52/ORef37→0607 RID50; 22.out W53→Contact23/24.in | Q5.2가 두 응답 분기를 공급 |
| LS01 raw | Contact23.operand W54/ORef38→0607 RID124; 23.out W55→OR25.in1 | I8.6 비반전 접점 |
| 처리 DB | Contact24.operand W56/ORef39→0609 RID125; 24.out W57→OR25.in2 | DB13X8.6 비반전 접점 |
| 기억 설정 | OR25.out W58→SCoil26.in; operand W59/ORef40→0609 RID10 | ON AND Q5.2 AND (I8.6 OR DB13X8.6)로 OPEN 기억 Set |
| 기억 해제 | W51→Contact27.in; Negated operand W60/ORef41→RID50; 27.out W61→RCoil28.in; operand W62/ORef42→RID10 | ON AND NOT Q5.2로 OPEN 기억 Reset |

**반전은 Q5.2를 읽는 Contact27에 있으며 LS01 입력 Contact23 또는 처리 Contact24에는 없다.** 따라서 LS02/타 센서의 닫힘이나 다른 네트워크의 NOT를 LS01에 복제하지 않는다. LS01 raw가 0이어도 별도 DB 경로로 기억 설정이 가능하며, 이미 설정된 S/R 기억의 값이 raw와 계속 같다는 보장도 없다. 이러한 정적 구분은 센서의 실제 normally-open/closed 설정이나 정상극성을 판정한 것이 아니다.

### 3.2 Word 전달 및 호출 경계

`0397-FlgNet.xml` LAD1070/선언 NID1에서 Move42.eno→W53→Move43.en, Move43.in W55/ORef47→0627 RID15 IW8, Move43.out1 W57/ORef48→0629 RID16 DB13.DBW8, Move43.eno W56→Move44.en을 확인했다. LS01 비트를 포함한 Word 직접 전달이며 이 Move43 경로에 NOT는 없다. 같은 XML의 MV03 Not142/150은 별도 주소의 처리로 LS01 반전 근거가 아니다(0627 RID152/154 및 0629 RID153/155는 AO61/62).

`0030-FlgNet.xml` LAD1613/선언 NID19: Recipes Handler CRef21.eno→W32→HMI CRef23.en→W33→HMI Output CRef25.en; 25.eno→W42→반전 Contact37.in→W43→HMI Inputs CRef28.en. Contact37.operand W44/ORef45는 0692 RID140 Simulation(1), Memory AO1440=M180.0. CodeBlock29는 0688 RID135 HMI Inputs, CRef28 인터페이스는 0694 RID136/TORID135로 결속한다. 앞 호출은 0688 RID120/124/128이다. 이 호출 조건과 ENO를 생략하고 항상 복사된다고 하지 않는다.

다른 쓰기 선언도 있다: `0635-IdentXmlPart.xml` RID208, NID12 UID28 AK=Write, Inputs.FC GATE A OPEN AO70 BAD5 및 `0634` RID5 TOD13. 탐색색인 network-map은 관련 네트워크를 simulation/LAD1090으로 분류한다. 여기서는 **추가 작성 선언의 존재만 정적으로 확인**했고 해당 논리를 제작·수정·실행·행동시험하지 않았다. 현행 활성 여부나 CPU 최종값은 미확정이다. 이 사실은 DB 표시를 실물 센서 단독 증거로 쓰지 말아야 할 추가 경계다.

### 3.3 구동 소유

PV01 부모의 요청→Q5.2→69KA1→EV01→CL01/02→LS01 관계는 부모/CYL-CL01 색인을 재사용한다. 이 문서의 LS01은 응답 센서이며 독립 출력·밸브코일·실린더 제어 소유자가 아니다. 부모 자동 순서·유지보수 병렬·알람 타이머 전체를 여기 다시 복제하지 않았다. Q=0 또는 MEM=1만으로 실물 닫힘/열림 완료를 선언하지 않는다.

## 4. 전기 끝점과 실제 PDF

### 4.1 직접 렌더 확인한 페이지

| 원본 `all-in-one/sources/` | 실제 PDF 페이지 | 도면 FG/문서 번호·표제 | 해당 페이지의 개정 |
|---|---:|---|---|
| PID_1684n002I.pdf | 1 | 1684n002, PV-01 Detail / P&I, FG ‘–’ | Apex I 15/01/2013; 기본 06/04/2011 |
| Electrical_Rev2.pdf | 71 | FG70 LOAD DRUM CLAPPE VALVE PV-01 | 개정란 공란; 기본 27.05.2024 |
| Electrical_Rev2.pdf | 125 | FG124 DIGITAL INPUT MODULE | Rev2 17.03.2025; 기본 27.05.2024 |
| Electrical_Can_Decoating_20241118.pdf | 21 | CANDC-CONS-E004-021, ENTRY ROUTE CONDUIT PIPING(1), 인쇄21/64, SECTION CONDUIT/ENTRY 4 | Rev1 24.11.11 first draft design |
| 같은 파일 | 53 | CANDC-CONS-C003-053, CABLE SCHEDULE(2), 인쇄53/76, SCHEDULE3 | Rev1 24.11.11 first draft design |

실제 5페이지를 이번에 렌더해 접점/끝점/표제를 시각 확인했다. 추출 PNG/TXT는 `extracts/LS01/`에 있다. 시공 페이지 인쇄 총쪽수64/76 차이는 그대로 기록하고 실제 PDF 인덱스와 혼동하지 않는다. 문서명 Rev2나 파일명 날짜로 모든 페이지 개정을 치환하지 않는다.

### 4.2 OEM LS01 경로

FG70/PDF71의 왼쪽 분기는 LIMIT SWITCH GATE “A” OPEN이다.

1. +24Vdc 10.7 공급선에서 연결점 → X1/130(5×20 2A F 도면 표기) → 선70.1 → LS-01 접점13.
2. LS-01 접점14 → X1/131 → E8.6, 교차참조124/6.
3. FG124/PDF125 E8.6 유입 교차참조70/1 → MOD10 단자7, CPU 515 도면 표기, 하단 LIMIT SWITCH LS-01 GATE “A” OPEN VALVE PV-01.
4. E8.6과 0607 RID124의 I8.6을 대조했다. X1/130–131은 별개의 공급/귀환 끝점이다. LS01에 0V 귀환선을 임의 추가하거나 단자7을 센서 단자로 혼동하지 않는다.

13/14 접점은 도면상 벌어진 접점으로 그려져 있다. 이는 도식 관찰이지 실제 장착 상태/접점 작동 시점/정상 위치별 0/1 증명은 아니다. 2A F는 도면값이며 현장 보호기 명판/현행 설정 확인이나 변경 권고가 아니다. 전선70.1 외 개별 케이블 심선번호는 OEM 페이지에서 확보하지 못했다.

인접 E8.7에만 SPARE 점선 표시가 있고 LS02 하단 설명과 상충한다. **LS01 E8.6은 그 점선 밖에 있으며 LS02 상충을 LS01의 SPARE 근거로 옮기지 않는다.** 부모 상충 자체는 보존한다.

### 4.3 시공 참고자료와 남는 연결 틈

PDF21 도식은 ENT2TB1→ENT2TB2→LS01/LS02/EV01 분기를 그리며 표의 LS01은 3_20, =ENT+PV01-LS01A, Flexible16, CVV 1.0, 2 core다. PDF53:

- 3_8 =ENT+PV01-ENT2TB2A: FROM CC-01 ENT2TB1 ENTRY joint box → PV-01 ENT2TB2 LS01/02/03/04; DC CVV 12G, SIZE1.0, SPARE3, route RBD1/E210.
- 3_20 =ENT+PV01-LS01A: FROM PV-01 ENT2TB2 / PV-01 A GATE → PV-01 LS-01; DC CVV 2C, SIZE1.0, SPARE0, route E211, Adjustment3/LEN3 (단위는 이 행에서 명시되지 않아 단위 추가 안 함).

이것은 설치 경로/케이블 일정의 설계 근거다. OEM X1/130–131↔ENT2TB2의 실제 개별 단자·심선 매핑은 미확보다. 3_8의 LS03/04 표기를 LS01과 합치거나 새로운 PLC 채널로 만들지 않는다. 시공자료의 A GATE 명칭은 참고 근거이며 P&ID 기계 형상과 실물 동일성은 추가 자료가 필요하다. 저장소에 이미 있는 원본만 읽었고 별도 SEJIN 운영자료를 복제하지 않았다.

## 5. 알람·복구

- LS01의 원시 입력과 위치 기억은 부모 PV01 Gate A 위치 감시에 영향을 줄 수 있으나 부모 알람의 소유는 PV01이다. 부모 색인의 A NOT_OPEN/NOT_CLOSE 및 4초 감시를 LS01 전용 알람/타이머로 복제하지 않았다. 이 문서에서는 그 타이머 전체 의미검토를 수행했다고 집계하지 않는다.
- 선정 LS01 원본 경로에서 독립 LS01 고장 알람·전용 reset·센서 진단 코드를 확보하지 못했다. 전 프로젝트에 없다는 전면 부재 판정은 아니다.
- Parent 알람이 발생해도 LS01 고장만 단정할 수 없다. EV01 명령/공압/CL01·CL02 기계 응답/배선/입력 갱신/기억/HMI를 분리해야 한다.
- 오류 해제·재요청·출력·실제 위치·raw/DB·기억·화면을 각각 다른 시점 증거로 기록한다. 알람 reset 성공이나 MEM_OPEN=1은 현장 복구 완료가 아니다. 실제 reset, force, 우회, 보호값 변경, 통전/행동시험은 수행하지 않았다.

## 6. 증상별 관찰·수리 근거

다음은 허용된 관찰의 자료 수집 목록이며 현장 조작·통전측정·수리 실행 지시가 아니다. 미수집 값은 빈칸으로 두며 0으로 대체하지 않는다.

| 증상 | 분리할 관찰 | 비교 근거·원인 배제 경계 | 추가 자료 |
|---|---|---|---|
| 게이트가 열린 듯하나 LS01 raw=0 | 실제 위치/센서 장착·명판/관찰시각, X1/130·131 식별자료, I8.6 | FG70→124 및 P&ID 리더; 배선/동작점/기계 연동 중 단정 금지 | 승인 현행 결선·정상극성·설치사진 |
| raw=0인데 OPEN 기억/화면=1 | 같은 시각 Q5.2, I8.6, DB13X8.6, DB2X8.1, DB11X76.1 | 0286 OR 및 S/R, 0397 호출과 타 쓰기, HMI 미결속 | 현재 프로젝트/CPU 식별, 승인 온라인 추적 |
| raw=1인데 기억이 설정되지 않음 | ON M0.0, Q5.2, 실제 호출·관찰시각, raw/DB/MEM | 0286은 ON/Q 조건 포함; 값 하나로 로직 불량 단정 금지 | 동일 스캔/호출 조건·다른 작성자 검토자료 |
| 표시 깜박임/위치 알람 반복 | 실제 움직임·접점 관찰·raw/DB/MEM/알람 발생해제시각 | 접점 흔들림·기계 행정·DB 갱신을 분리, 전용 지연 임의 생성 금지 | 센서 모델/동작점·승인 이력 |
| LS01과 LS02 명칭/배선 혼동 | 센서 번호사진, 두 케이블·단자 추적, 최신 도면판본 | LS01=Gate A OPEN/I8.6; LS02 SPARE 상충을 전이시키지 않음 | OEM↔시공 개별 심선표 |

공통 기록: 관찰자·시각/시간대·위치·값/단위·수집 장치·CPU/프로젝트 근거·비교 원본/개정·배제 사실·승인 조치와 전후 복구 증거. 실제 관찰값/원인/조치/복구완료를 지어내지 않았다. 제조사 모델·접점 정격·정비주기·체결토크는 명판/공식 모델 자료 전까지 미확정이다.

## 7. 완료·누락과 검증

| 영역 | 적용 판정 | 확보 및 남은 부분 |
|---|---|---|
| 설비·자료 기준 | 적용 | LS01 고유 리더/parent PV01; 실물 동일성 미확정 |
| I/O·HMI | 적용, HMI 직접 결속 미확보 | raw/DB/MEM/화면 분리; 이벤트·실인수 미결속 |
| 제어 구조 | 응답 센서로 적용 | 0286 비반전/OR/SR, Word 갱신과 호출 경계; CPU 상태 미확정 |
| 전기 전달 경로 | 적용 | 접점 양단→MOD10/7 및 참고 케이블; OEM↔시공 심선 연결 미확보 |
| 알람·복구 | 부모 연계 적용, 고유 알람 근거 미확보 | 부모 소유 유지; 실제 복구 미수행 |
| 증상 관찰 | 적용 | 원인 분리 목록 제공; 현장값 없음 |
| 완료 기준 | 적용 | 문서/정적/UI/게시/CPU/현장 상태 분리 |

### 검사 범위와 결과

- 선정 원본 **32개 전체 SHA256와 고정 Git blob 바이트 비교: 32/32 일치**. 아래 부록 및 `extracts/LS01/source-verification.json` 참조. 이는 전체 원본 저장소 해시 검사가 아니다.
- 의미 검토는 FlgNet 3파일의 LS01 관련 분기·호출(0286/0397/0030), 선언 XML 11파일의 해당 RID/DB/핀, 실제 PDF5페이지, HMI CSV의 PV01 8행, 대장2행이다. 해시32개를 전부 PLC 의미 검토32개로 세지 않는다. network-map은 탐색용 파생색인이다.
- 정적 Python XML/JSON 파싱·해시/Git show 바이트 비교·PDF 렌더를 수행했다. 자체 추출 스크립트 `extracts/LS01/prepare_evidence.py` 종료0, all_byte_equal=true. XML 구조/선언 추출은 `xml-evidence.json`에 보관한다. 원본 생성기/앱/시뮬레이터는 실행하지 않았다.
- 원본 기준문서 preflight가 일반 실행 안내에 있지만 이번 own 정적분석 범위에 따라 원본 스크립트는 실행하지 않았다. 대상 두 대장행과 고정 바이트를 직접 정적 대조했다.
- 부모 전체 자동 순서·알람·HMI 실인수 재조사, TIA compile, CPU/현장, UI/저장/복원/동시성/앱 PDF/패키지/배포 검사는 수행하지 않았다.

| 네 기능 | 현재 상태 |
|---|---|
| 도면·래더 나란히 보기 | 원본 페이지·핀 제공; LS01 UI 구현/링크 동작 검증 미실행 |
| 백업 미리보기·선택 복원 | 기존 스키마/키/미지 필드 변경 없음; LS01 기능 검증 미실행 |
| 전후 기록 비교 | 관찰 필드 제시; 저장·재읽기·재열기 검증 미실행 |
| 관찰 보고서/PDF | 앱 생성/출력 미실행; 원본 도면 렌더와 구분 |

| 구분 | 상태 |
|---|---|
| documentation | draft_complete_with_gaps |
| static_review | self_review_complete; independent_review_pending |
| ui_records | not_run |
| publication | not_published_by_this_task |
| tia_compile | not_performed |
| live_cpu | not_performed |
| field_recovery | not_performed |

다음 좁은 확인: LS01 명판·설치사진과 OEM X1/130–131↔ENT2TB2↔LS01 개별 심선표를 받아 정상극성/실물 동일성 및 HMI DB11 결속을 확인한다. 자료 없이 같은 경계를 반복 조사하거나 부모 전체 완료를 상속하지 않는다. 현장 보호값·현재 CPU·복구는 미확정으로 유지한다.

## 부록 A. 선정 전체 원본 SHA256 / 고정 Git blob

경로는 `source-mv06/` 기준이다. Git commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`. 각 로컬 파일 전체 바이트와 고정 blob 전체 바이트를 비교했으며 blob SHA256도 검사 JSON에 보관한다. 배정 JSON·부모 초안은 작업/탐색 근거로 원본32개 수에 포함하지 않는다.

| 고정 원본 상대경로 | 전체 SHA-256 | Git blob | 바이트 일치 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | PASS |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | PASS |
| `.agents/skills/gme-equipment-rollout/references/source-map.md` | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` | PASS |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | PASS |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | PASS |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | PASS |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | PASS |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | PASS |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | PASS |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | PASS |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` | PASS |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | PASS |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | PASS |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | PASS |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | PASS |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | PASS |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | PASS |
| `all-in-one/sources/decoded-original/0286-FlgNet.xml` | `dca38f0104a47f95095b88a86400e379d653dd26b0e2fc88e1b3d17612268828` | `756366ed44352d07dd0b7af823d5493d84e920b8` | PASS |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | PASS |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | PASS |
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | PASS |
| `all-in-one/sources/decoded-original/0608-IdentXmlPart.xml` | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | PASS |
| `all-in-one/sources/decoded-original/0609-IdentXmlPart.xml` | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | PASS |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | PASS |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | PASS |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | PASS |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | PASS |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | PASS |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | PASS |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | PASS |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` | PASS |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | PASS |
