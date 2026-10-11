# VR02 로터리 밸브 — 자체 클라우드 조사초안

작성일: 2026-10-11 UTC · 기준: GME-STD-1.0.0 · 작업3 두 번째 5개 묶음 중 VR02 단일 ID

## 먼저 확인할 결론

1. **VR02는 M23 로터리 밸브 모터의 접촉기 직접기동 회로**다. 고정 백업의 출력 `Start VR02=%Q3.0`, 원시 접촉기 피드백 `VR02_Fbk=%I3.7`, 처리 입력 `Inputs.VR02 Run=DB13.DBX3.7`, 요청 `Flag.M_VR_02=DB2.DBX1.3`은 서로 다른 신호다.
2. `0254/LAD1952`는 `ON` 아래에서 고장일 때 요청을 Reset하고, 별도 요청 접점으로 Q3.0을 쓴다. `0434/LAD1799`는 **Q3.0 요청이 있는데 처리 피드백이 없는 상태**를 `Tag_64=%T67`, `S5T#2S`로 검출해 `Allarm.VR_02_FAULT=DB3.DBX1.3`을 Set한다. 리셋과 재요청은 별도다.
3. 예열 요청은 `Tipo_preset=1, Tempo_presetting=28`, 생산 요청은 `Tipo_preset=2, Tempo_presetting=46`에서 Set된다. 완전정지 순서5에서는 `Tempo_presetting=11 OR Emergency_module_fault`에서 Reset된다. 각 식의 상위 허가와 정확한 핀은 아래에 따로 기록했다.
4. **VR02 피드백 미성립은 FN01 사전경보의 한 분기**다. FN01 운전 중 `NOT Inputs.VR02 Run`이 다른 사전경보 조건과 OR되고, FN01 소유 `Tag_122=%T130/S5T#1H_30M` 경로에 들어간다. 이 90분 타이머를 VR02 고장 지연으로 가져오지 않는다.
5. P&ID `1684n002`, apex I, PDF1은 **CY-03 하부에 VR-02/M23**을 그린다. 2024 시공안 PDF31의 동일 FLOW_B 구간에 CY-02 램프/버튼이 있어도 VR02의 부모를 CY02로 확정하지 않는다. 대장상 VR02는 부모 없는 독립 ID이고 사용자 ‘2사이클론’과의 동일성은 미확정이다.
6. HMI 설정 3행과 PLC의 HMI 표준모터 호출 핀은 확인했지만, **0372의 핵심 ORef 24/26/33/35는 해당 선언과 완전히 결속되지 않았다.** 검색문자열만으로 연결을 확정하지 않는다.
7. 문서 조사는 가능 범위에서 완료했지만 현재 CPU·현장·HMI 실제 이벤트·시공 완료·복구는 검증하지 않았다. 로컬 2차133 통합·게시 제외와 시뮬레이터 영구중지는 그대로 유지한다.

## 0. 작업·보존 기준

- 대상: `catalog_id=VR02`, 이름 로터리 밸브, `kind=motor`, 대장 그룹 집진·석회, `parent_id=null`, `priority_key=null`, 기존 phase2/planned/baseline. P키를 새로 배정하지 않는다.
- 원본 저장소: `source-mv06`, 고정 `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, 프로그램 v1.12.0. 최신 운영본을 의미하지 않는다.
- 전체248에서 중복·기존 제외·부모보류·시뮬레이터 중지를 별도 overlay로 차감한 작업3 조사분모132를 적용한다. 원본 INVENTORY의 phase2 133은 수정하지 않았다. VR02 한 개만 이번 산출물이며 다른 VR/CY의 완료를 상속하지 않는다.
- 승인된 산출물: 이 초안과 `extracts/VR02/` 아래 읽기 전용 원본 추출·렌더·해시 증거. 공통 `declarations.json`과 공용 코드·대장·버전·배포는 변경하지 않았다.
- 실행 모델/추론 설정: 이 조사환경에서 실제 모델 선택·설정의 독립 증거를 확보하지 못했으므로 미확인. 문서상 권장 모델을 실행 사실로 적지 않는다.
- 백업 이름 `GME_20250506.zap18`과 내부 프로젝트/보관 날짜는 같은 날짜라고 단정할 수 없다. XML은 PEData.plf에서 복원한 원본 조각이며 TIA 재수출/컴파일 결과가 아니다.
- 읽기전용 preflight 통과: `inventory_matches=true`. requirements-audit.json/all-in-one-data.json의 과거 저장해시 대비 바이트 차이는 존재하지만 ID·메타데이터·대응·제외·수량은 일치했다. 이것은 현장 인수검사가 아니다.

### 7영역 적용표

| 영역 | 적용 상태 | 이 문서 위치 | 남은 경계 |
|---|---|---|---|
| 설비·자료 기준 | 적용 + 현재실물 근거 미확보 | 0, 1 | VR02/M23 현장명판, CY 연결, 최신 승인도 |
| I/O·HMI | 적용 + 이벤트/핵심 HMI 결속 미확보 | 2 | raw/DB/HMI 현재값·쓰기 이벤트 |
| 제어 구조 | 적용 + 현재 호출·간접쓰기 미확정 | 3 | OB 실제 주기/우선순위, 초기화/retentivity |
| 전기 전달 경로 | 적용 + 시공/실측 미확인 | 4 | 전원·QM/QS/KM·모터 양 끝점 현장대조 |
| 알람·복구 | 적용 + 실제 복구 미수행 | 5 | 원인 제거와 새 요청, 재발 여부 |
| 증상별 수리 | 적용, 관찰·자료수집 절차 | 6 | 작업자 승인/차단 절차와 실제 관찰 |
| 완료 기준 | 적용 | 7 | 문서·UI·게시·TIA·CPU·현장 별도 상태 |

## 1. 설비·소유·자료 시점

### 1.1 확인한 관계와 확인하지 못한 관계

- 대장 `equipment.json`의 VR02 행은 FG49와 `pid=true`를 연결하지만 부모는 공란이다. ‘집진·석회’ 그룹은 문서 분류이며 실물 설치구역 또는 CY02의 소유 증명이 아니다.
- P&ID PDF1의 CY-03 하부 배출 기호에 `VR-02 / M23 / 0.55 kW 440V`가 직접 붙어 있다. 도면 전체와 해당 영역을 실제 렌더로 확인했다. 제목 UBC AND SCRAPS DECOATER 10 Ton/h, 도번1684n002/apex I, 기본일자06/04/2011, 마지막 보이는 개정행15/01/2013. 이를 현재 준공 상태로 승격하지 않는다.
- 전기도면 FG49/PDF50은 `ROTARY VALVE VR-02`, M23, 0.55kW/1.25A와 440V 60Hz를 표기한다. 그려진 회로에는 가변속 인버터나 정역 두 출력이 없다. 따라서 **이 도면 범위의 구동은 접촉기 직접기동**으로 설명하되 현행 장착·개조 유무는 별도다.
- 시공안 PDF31의 VR02/M23 케이블 행과 CY02/17HL1·6SB03 행은 별개다. 같은 배관구간/페이지에 있다는 이유로 장치 소유를 합치지 않는다. P&ID의 CY03 연결과 시공안의 CY02 주변표기는 판본·기능 경계의 추가 현장 확인 사유다.
- 로터, 감속기, 씰, 베어링, 구동축, 실제 배출량/에어록 성능의 모델·치수·정비주기·토크는 근거 미확보다. PLC 접촉기 응답을 로터 정상회전/분진 배출/기밀성의 증거로 대체하지 않는다.

### 1.2 자료의 용도

| 자료 | 확인한 용도 | 한계 |
|---|---|---|
| decoded-original XML/IdentXmlPart | Part/Wire/ORef/RID/NID/UID·Global/Local·상수·주소/DB 관계 | 복원 조각, 현재 CPU와 일치 미확인 |
| network-map.json/검색 색인 | LAD 문서ID·블록·원본조각·후보 선언 탐색 | 제어식 자체의 최종 근거가 아님 |
| hmi_plc_tags.csv | dde.cfg에서 추출된 Access/설정주소/내부ID | 원본 화면 이벤트·실제 연결·현재값 미확인 |
| Electrical_Rev2.pdf | 회로·단자·명목값·자재표 | 각 페이지 개정란은 별도로 판독, 현행 실장 아님 |
| PID_1684n002I.pdf | VR02의 도면상 공정 연결 | 2013까지의 도면, 현장 동일성 미확인 |
| Electrical_Can_Decoating_20241118.pdf | FLOW_B 배관/케이블 후보 | first draft design, 승인·준공도 아님 |

## 2. I/O·HMI와 값의 경계

### 2.1 주소와 선언

XML SSD의 AO/BO는 비트 오프셋이므로 Bool 31→3.7, Word 16→byte2로 환산한다. `TOD N`으로 DB 번호를 별도 확인했다. 각 행의 현재값은 미확보다.

| 역할 | 심볼/주소/형식 | 원본 선언·참조 | 해석과 미확정 |
|---|---|---|---|
| 원시 피드백 | VR02_Fbk, %I3.7 Bool | 0613 RID188, SAD Input/AO31, NID31 UID1720; plc-symbols.csv doc503 | 49KM1 보조접점 신호 경로. 로터 회전 센서 아님 |
| 출력 | Start VR02, %Q3.0 Bool | 0602 RID121, Output/AO24; 0254 ORef702→Coil697 operand Wire709 | PLC 논리 출력, 접촉기 코일 전압/회전과 별도 |
| 요청/기억 | Flag.M_VR_02, DB2.DBX1.3 Bool | 0604 RID120/AO11, BAD2→0603 DepDB Flag TOD2; NID23 UID700/701 | RCoil/요청 접점, HMI 주소와 같은 bit이지만 이벤트는 미확인 |
| 처리 피드백 | Inputs.VR02 Run, DB13.DBX3.7 Bool | 0657 RID287/AO31 BAD247→0655 Inputs TOD13; NID21 UID765 | 알람/FN01 분기가 읽는 DB bit, 원시I와 분리 |
| 전용 고장 | Allarm.VR_02_FAULT, DB3.DBX1.3 Bool | 0657 RID88/AO11 BAD10→0655 Allarm TOD3; UID733/735/736 | Set/Reset 래치. DB2.X1.3 요청과 주소 혼동 금지 |
| 전용 타이머 | Tag_64, %T67 Timer | 0658 RID86, SAD Timer/AO67; UID730 write/731 read | PLC S5 타이머, HMI 태그 아님 |
| 공통 허가 | ON, %M0.0 Bool | 0602 RID1 Memory/AO0; 0254 ORef698 | 이름만으로 항상True 또는 안전회로 증명 불가 |
| 공통 리셋 | Flag.RESET_ALLARM, DB2.DBX6.0 Bool | 0657 RID13/AO48, 0655 Flag TOD2; ORef734 | 고장 bit 해제 요청, 재기동 명령 아님 |
| 자동 진행 | Auto_ON1=DB2.DBX7.3; Tempo_presetting=DB1.DBW96 Int; Tipo_preset=DB1.DBW98 Int | 0577 RID4/AO59, RID7/AO768, RID12/AO784; 0576 TOD2/1 | 자동 순서 소유, VR02 전용 타이머가 아님 |
| 시간 분 버퍼 | hours motors.VR_02_MIN=DB9.DBW120 Int | 0615 RID190/AO960 BAD5→0614 TOD9 | 더하기/60비교/0쓰기 |
| 시간 hour 버퍼 | hours motors.VR_02_HOUR=DB9.DBW122 Int | 0615 RID192/AO976; UID1727/2963 write | 원문은 Move1/Move0, 누적시간 +1과 다름 |

### 2.2 원시 I3.7 → 처리 DB13.X3.7

`0397/LAD1070`, HMI Inputs NID1:

- `0627 RID8 Tag_179`은 Input/Word/AO16, 즉 `%IW2`다. ORef28→Move27.in은 Wire31.
- Move27.out1→ORef29는 Wire32. `0629 RID9`는 Word/AO16, BAD4이고 `0628 RID4 Inputs TOD13`이므로 목적지는 `%DB13.DBW2`다. I3.7이 포함된 두 바이트를 같은 DB 두 바이트로 복사하는 구조다.
- 이 Move의 EN은 전원레일 직접이 아니라 **Move22.eno→Move27.en, Wire34**이다. Move22/27에는 `DisableENO=true`가 함께 있다. 와이어 연결과 속성을 보존하며 실제 ENO 동작을 별도 실행으로 확정하지 않는다.
- 상위 `0030/LAD1613`은 Recipes Handler(21)→HMI(23)→HMI Output(25)의 ENO 연쇄 뒤, `NOT Simulation(1)` 접점37을 거쳐 HMI Inputs CRef28.en을 허가한다(Wire31/32/33/42/44/43). Simulation(1)은 0692 RID140 Memory AO1440=%M180.0. **이것은 과거 백업의 읽기 경계 조사이며 시뮬레이터의 생성·수정·실행 승인이 아니다.**
- 0635 선언에 Inputs.VR02 Run의 과거 다른 쓰기(RID98, NID3 UID50 AK Write)가 남아 있다. 중지 자산의 이력을 숨기지 않고, 원시I와 처리DB가 언제나 같다는 주장을 하지 않는다. 해당 동작을 실행하거나 검증하지 않았다.
- 따라서 원시 I3.7, DB13.X3.7, HMI 응답의 같은 시각 비교가 필요하다. 입력이 맞고 화면이 다르다는 이유만으로 센서를 교체할 근거가 되지 않는다.

### 2.3 HMI 설정과 미결속 호출

`all-in-one/sources/hmi_plc_tags.csv` 헤더 포함 행28~30, Access Name=PLC:

| HMI 태그 | 설정주소 | 내부ID | 현재 확인 범위 |
|---|---|---|---|
| VR_02\RispostaA | DB11,X36.0 | 00440 | 처리 응답 설정주소, 실제 표시 이벤트 미확인 |
| VR_02\Flag | DB2,X1.3 | 0043F | 요청 주소와 일치, 클릭·토글·쓰기 권한/시점 미확인 |
| VR_02\Allarme1 | DB11,X36.1 | 0043E | HMI 모터 집계 알람 설정, DB3 전용 고장과 별도 |

`0372/LAD1195 hmi vr02`의 실제 핀:

- CRef22/RID638→CodeBlock23/RID1. 0623 FCBlock RID1은 HMI Standard Motors/TOD FC1이고 0624 인터페이스 참조가 있다.
- Wire21 powerrail→22.en. Wire37 ORef24/RID674→Ingresso_run, Wire39 ORef26/RID252→Allarme1.
- Wire40/41/42/43 ORef27/28/29/30(RID48)→Allarme2/3/4/5. FALSE 후보 선언이 있지만 VR02 호출의 NID/UID 완전 결속을 전체가 동일하게 충족하지 못하므로 **네 외부 입력을 모두 확정 FALSE로 기술하지 않는다.**
- Wire46 Risposta→ORef33/RID255, Wire48 Comulativo_allarmi→ORef35/RID257.
- 검색문자열에는 Inputs.VR02 Run/Allarm.VR_02_FAULT/Motors.VR02.Risposta·Allarme_comulativo가 나타나지만 핵심4개 ORef와 일치하는 호출 선언은 이 복원본에서 미확보다. 전체 다른 선언의 같은 RID/UID 후보(예: unrelated Allarm.Simulation enabled)를 대입하지 않는다.
- 공통 FC 내부 `0355/LAD331`과 **Local** 선언0621은 Ingresso_run→Risposta(Contact23/Coil27, Wire22/25/26), Allarme1..5→OR41→Comulativo_allarmi(Coil59, Wire42/43/44/48/49/57/58)를 보인다. 이 Local 처리 구조를 VR02의 미결속 외부 주소에 강제로 연결하지 않는다.
- 추가 필요: 현재 HMI 프로젝트의 dde.cfg 원문·VR02 화면객체·버튼 press/release/스크립트 이벤트·PLC DB11 구조 및 TIA 정식 cross-reference. 세 태그의 물리/논리 연결을 독립적으로 대조해야 한다.

## 3. 제어 구조와 모든 알려진 쓰기

### 3.1 요청 Reset과 출력은 두 가지 쓰기

`0254/LAD1952`, motors1 NID23:

- Wire717 rail→Contact711, ORef698/RID1 ON→711.operand(Wire703).
- ON.out에서 고장 Contact713과 요청 Contact715로 병렬 분기(Wire712).
- ORef699/Allarm.VR_02_FAULT→713.operand(Wire704), 713.out→RCoil693.in(Wire714), ORef700/Flag.M_VR_02→693.operand(Wire706). **ON AND FAULT이면 M_VR_02 Reset**이다.
- ORef701/같은 M_VR_02→715.operand(Wire707), 715.out→Coil697.in(Wire716), ORef702/Start VR02→697.operand(Wire709). **이 출력 rung 자체는 ON AND M_VR_02**이다.
- 이 네트워크에서 Maintenance_ON·VR02 로컬선택 입력·속도설정·역방향·엔코더 조건을 찾지 못했다. 다른 모터의 허가식을 추가하지 않는다. QM/QS의 하드웨어 접점은 4절에서 별도로 설명한다.
- Reset 후 출력 평가의 스캔 효과, ON으로 상위 FC 호출이 생략될 때 이전 Q 보존 여부, 인터럽트가 같은 요청을 다시 쓰는 순서는 현재 TIA/CPU 미확정이다. 단순 Boolean 식만으로 모든 최종 스캔값을 보장하지 않는다.

### 3.2 자동 요청 세 곳

상수 선언0578, 전역 선언0577, DB 소유0576을 같이 읽었다. 식의 숫자는 VR02 원본값이며 다른 VR의 숫자를 복제하지 않았다.

| 경로 | 정확한 핀·선언 | 확인한 조건/쓰기 | 경계 |
|---|---|---|---|
| 예열1843 / 0164 NID3 | ON Contact785(ORef588), NOT Emergency Contact22(ORef23/RID108), Tipo Eq400(in1 ORef590/RID12, in2 ORef591/RID8=1), Auto Contact823(ORef824/RID4), Tempo Eq509(in1 ORef635/RID7, in2 ORef636/RID52=28), Wire738→SCoil515; Wire740 ORef638/RID54 | ON AND NOT Emergency AND Tipo=1 AND Auto_ON1 AND Tempo=28 → Set M_VR_02 | Eq509의 pre가 Wire672 공통 허가에 연결. 독립 28초 TON 아님 |
| 생산1844 / 0165 NID4 | ON1145/ORef932, NOT Emergency1154/ORef1155, Auto1147/ORef933, Tipo Eq737/ORef934·935(RID78=2), Tempo Eq846/ORef983·984(RID85=46), Wire1097→SCoil852; Wire1099 ORef986/RID54 | ON AND NOT Emergency AND Auto_ON1 AND Tipo=2 AND Tempo=46 → Set M_VR_02 | Tempo=46 비교, 별도 피드백 대기시간 아님 |
| 완전정지1847 / 0166 NID5 | Auto1095/ORef983, Tipo Eq881/ORef984·985(RID22=5), Tempo Eq913/ORef997·998(RID99=11)→OR48.in1 Wire49; Emergency Contact1126/ORef1127→OR48.in2 Wire50; Wire1049→RCoil919; Wire1051 ORef1000/RID54 | Auto_ON1 AND Tipo=5 AND (Tempo=11 OR Emergency) → Reset M_VR_02 | Eq881.out Wire1031이 양쪽 분기를 허가. Emergency 단독 무조건Reset으로 축약 금지 |

- 자동 블록 호출: `0024/LAD1723`, cyc_int2 ogni1s, Contact188/ON(ORef185,0652 RID36)→Wire189→CRef183.en, CodeBlock186/0067 RID39 Auto start motors. 블록명과 호출색인은 1초 계통을 가리키지만 현재 OB 설정·주기·우선순위는 검증하지 않았다.
- `0162/LAD1841`: ON Contact88 아래 Auto_ON1 Contact90→Add59(Data.Tempo_presetting+1, out ORef73), NOT Auto_ON1 Contact92→Move66(0,out ORef76). Wires77~86/89/91/93. 이 카운터가 호출마다 증감/초기화되어 단계 숫자의 의미를 만든다. 실제 벽시계와 정확히 일치한다고 보장하지 않는다.
- `0168/LAD1846 emergency stop`: PContact21, operand ORef52 Emergency_module_fault, bit ORef51 Tag_292=%M90.5, Wire48→Move22(0→Tempo), ENO Wire35→Move23(5→Tipo), ENO Wire38→SCoil24(Auto_ON1). 정지순서로 전환하는 별도 공통 기능이다. safety-rated 정지시간 또는 모든 실제 출력의 즉시차단을 이 식으로 인증하지 않는다.

### 3.3 호출·다른 쓰기·소유 경계

- `0031/LAD1619`: ON Contact282/ORef271→Wire283에서 Analog conversion/Allarms1/Allarms2/Allarms3 CRef EN이 공통 분기. Allarms1은 CRef264→CodeBlock275(0688 RID58).
- `0549/LAD1620`: ON Contact350/ORef335→Wire351로 Motors1 CRef319(CodeBlock337/RID67)과 time work motor CRef334(CodeBlock347/RID82) 등이 허가된다. 같은 와이어로 연결됐다는 사실만으로 동시실행 의미를 부여하지 않는다.
- 복원 색인은 main에서 HMI 처리1613, 알람1619, 구동1620, 알람관리1622 순서를 보여준다. 원본 NID는 편집 이력 식별값이므로 NID 숫자만 정렬해 실행순서로 바꾸지 않는다. 현재 프로젝트 정식 호출계층 확인 필요.
- 이름 있는 선언에서 확인한 M_VR_02 쓰기: 예열 Set638, 생산 Set986, 정지 Reset1000(0577 RID54), 고장 Reset700(0604 RID120). HMI DB2.X1.3은 외부 쓰기 후보다. 이 목록을 모든 간접/Word/외부 쓰기의 완전성 증명으로 사용하지 않는다.
- Start VR02/Q3.0 명시적 이름 쓰기는 0602 RID121 UID702 한 곳, 전용 T67 쓰기는 0658 RID86 UID730 한 곳을 확인했다. 기존 Watch Monitor 참조는 쓰기로 세지 않았다. 현재 온라인 강제값/간접쓰기 유무는 미확인.

### 3.4 FN01에 주는 영향은 FN01 소유

`0252/LAD1950`, NID21:

- ON Contact691(ORef662) 아래 Inputs.FN01 Run Contact699(ORef666)→Wire700→**NOT** VR02 Run Contact703(ORef668,0604 RID252)→Wire704→OR707.in5.
- 다른 OR 분기는 MAX_TC04, MAX_TC05, ZT01 vibration, FN01 Run AND NOT VR01 Run이다. VR02 분기만 따로 떼면 `ON AND FN01Run AND NOT VR02Run`이며 전체는 OR5다.
- OR707.out Wire683→Coil653(Allarm.Prealarms_FN01, ORef669/Wire684), SdCoil656(Tag_122=%T130, ORef671/Wire686, S5T#1H_30M ORef670/Wire685), Contact705(T130 ORef672/Wire687)→Coil661(Local Stop_Fan_FN01 ORef673/Wire689).
- 다음 `0253/LAD1951`에서는 Local Stop_Fan_FN01 ORef694/0605 RID114→Contact720.operand(Wire705), Contact720.out→OR676.in4(Wire721), OR676.out→RCoil685.in(Wire709), ORef697/Flag.M_FN_01→operand(Wire711). 즉 FN01 요청 Reset 경로로 이어지는 자료가 있다.
- 이것은 VR02 고장 bit의 직접상위 차단이 아니라 **처리 피드백 미성립에서 출발하는 FN01 사전경보**다. 현재 지연값, 최종 FAN 정지/공정 영향은 CPU·현장에서 미검증이다.

### 3.5 운전시간의 원문을 그대로 보존

`0317/LAD1029`, NID31:

- Contact1748 Tag_47=%T13(0613 RID1/ORef1719) AND Contact1750 **원시 VR02_Fbk**(RID188/ORef1720) → Add1702.en 및 Ge1709.pre(Wire1751).
- Add1702: in1 VR_02_MIN ORef1721, in2 정수1 ORef1722, out→같은 MIN ORef1723(Wires1733/1734/1735).
- Ge1709: MIN ORef1724 >= 정수60 ORef1725(Wires1736/1737). out→Move1712.en(Wire1738).
- **Move1712.in=정수1(ORef1726/Wire1740), out1=VR_02_HOUR(ORef1727/Wire1741)**. HOUR+1 ADD가 아니다. Move1712.eno→Move1715.en(Wire1742), Move1715.in=0/ORef1728, out1=MIN/ORef1729(Wires1743/1744), eno→SCoil1718(Flag_Aggiorna_DB=%M1.7/ORef1730, Wires1745/1746).
- `0019/LAD1056`에서 NOT T13 Contact3120→SD3112, 값 S5T#1M(ORef3114/Wire3117), timer operand ORef3116/Wire3119. 호출조건·스캔과 별도로 1분 설정을 확인했다.
- `0338/LAD1051`에서는 T17/Tag_48 Contact2987→Move2946.en(Wire2988), 정수0/ORef2962→in(Wire2973), VR_02_HOUR/ORef2963→out1(Wire2974). 이 행은 해당 공통 묶음의 **첫 Move**라 앞 장치 Move의 ENO를 기다리는 경로가 아니다. 뒤 장치들과 ENO 연쇄가 이어진다.
- `0341/LAD1055`: ON AND Flag_Aggiorna_DB→Set MEM2_0(%M2.0); ON AND MEM2_0 AND NOT Flag_Aggiorna_DB→SD Tag_48=%T17/S5T#5S(Part3118); T17 접점3155→Reset MEM2_0 Part3123. Wires3133~3144/3148/3150/3152/3154/3156.
- 따라서 HOUR는 외부 DB 기록용 펄스/버퍼일 가능성이 있으나 외부 저장 성공은 확인하지 않았다. **현장 누적 운전시간·보전주기 실적**으로 확정하지 않으며 값/로직을 수정하지 않는다.

## 4. 전기 전달 경로: 실제 원본 렌더 확인

전기도면 PDF 페이지와 인쇄 FG 번호는 다르다. 특히 자재표 **PDF255는 실제 FG252**이며 +1 규칙을 기계적으로 적용하지 않았다. 모두 날짜27.05.2024가 보이고, FG139에는 추가로 Rev2/17.03.2025가 있다. FG49·119·252에서 별도 개정번호는 확인되지 않았다.

### 4.1 동력 경로 — FG49/PDF50

- 상단 `THREE-PHASE LINE 440V 60Hz`, 8.3L1/L2/L3가 전페이지46/9에서 들어와 다음50/0으로 이어진다.
- 해당 세 상→49QM1의1/3/5–2/4/6→49KM1 주접점1/3/5–2/4/6→49U1/49V1/49W1→XM의 동명 단자→49QS1의1/3/5–2/4/6→M23/VR-02 U/V/W. PE 접지기호가 별도 있다.
- 도면 내부선 BLACK/FS17 1.5mm², 모터 명목0.55kW/1.25A, 49QM1 범위1.1–1.6A. 이 범위는 현재 설정값·권장 조정값이 아니다. 명판/보호계산 없이 조정하지 않는다.
- 회전방향·기계전달·실제 모터/감속기 명판·출력축 동작은 이 회로만으로 확정되지 않는다.

### 4.2 명령의 양 끝점 — FG139/PDF140 ↔ FG49/PDF50

- FG139의 VR-02 MOTOR COMMAND: CPU515, MOD14, **A3.0/단자31**, 49/4 상호참조.
- FG49의 A3.0(139/1)→**XS35→49QS1 보조접점→XS36→선49.1→49QM1 보조접점→49KM1 코일A1**, A2→-0Vdc10.6. 보조접점의 정확한 단자번호는 도면에 판독 가능한 숫자가 없어 임의95/96 등을 붙이지 않는다.
- FG139 출력군 전원: +24Vdc10.9→X21/3031 퓨즈5×20 4A F→139.1→단자39, 단자40→-0Vdc10.6. 이 공통 퓨즈를 VR02 전용 장치로 분류하지 않는다.
- Q3.0=1은 이 모든 접점·전원·모듈·배선·코일이 정상이라는 뜻이 아니다. 도면상 QS/QM 접점이 코일경로를 끊을 수 있다.

### 4.3 피드백의 양 끝점 — FG49/PDF50 ↔ FG119/PDF120

- +24Vdc10.7→**49KM1 보조접점13–14**→E3.7(119/7).
- FG119에서 E3.7/49/6 상호참조→**CPU515 MOD8 단자38**, FEEDBACK MOTOR VR-02.
- 해당 입력 모듈의 공통전원은 +24Vdc10.7→X21/3007 퓨즈5×20 2A IST→119.1→단자39, 단자40→-0Vdc10.6.
- 그려진 것은 접촉기 보조접점 상태다. 명령/Q, 보조접점/I, 실제 모터전류/회전/배출은 따로 관찰해야 한다. 실물 극성·접점 용착·가공된 DB 입력 일치는 아직 검증하지 않았다.

### 4.4 자재표와 시공안

- FG252/PDF255의 49KM1: Siemens `3RT2015-1BB41`, 설명 CONTACTOR 3KW,1L,DC24V,S00 VT; RC 소자 `3RT2916-1CB00`(AC24–48V/DC24–70V).
- 49QM1 그룹: `3RV2901-1E`, `3RA1921-1DA00`, `WR32433`, `3RV2011-1AA10`(1.1–1.6A). 표의49KM1/49QM1과 FG49의 동일 태그를 연결한 **자료상 BOM**이다. 실제 장착품·제조사 승인 대체품은 미확정이며 부품 구매/교체 지시가 아니다.
- 시공안 PDF31/TOTAL-PAGE31/64, D-PAGE14, 도번 `CANDC-CONS-E014-031`, FLOW B ROUTE/CONDUIT PIPING(1), Rev1 `24.11.11 first draft design`, 승인란 공란. `100 LDD1`, Flexible16/No.2, M23, VR-02, `1_17=FLB+VR02-M23A`, CV/1.5/4core를 확인했다.
- 시공안 PDF51/TOTAL-PAGE51/64, CABLE SCHEDULE(1), 도번 `CANDC-CONS-C001-051`, 행1_17: **FROM CR → TO VR-02/M23**, `=FLB+VR02-M23A`, GAC, CV, 4core, size1.5, spare0, route100LDD1→E200, Adjustment12, LEN59. 두 수치의 단위·현장실측 의미가 해당 행에 명시되지 않았으므로 임의의 실제 길이로 확정하지 않는다.
- 시공안은 끝점 장치/케이블을 연결하지만 전기 FG49의 XM 단자와 현장 심선번호의 확정 대응을 제공하지 않는다. 최종 케이블라벨·단자대·QS 위치·준공표가 필요하다. 운영 SEJIN 자료·사진은 읽거나 수정하지 않았다.

## 5. 알람·복구

### 5.1 전용 VR02 고장

`0434/LAD1799`, NID21, 선언0656/0657/0658:

| 단계 | 원본 핀 | 해석 |
|---|---|---|
| 감시허가 | ON751/ORef727 Wire737, Start753/ORef728 Wire738; Wire752/754 | ON AND 실제 출력 Start VR02 |
| 불일치검출 | Contact764에 Negated operand, ORef765/RID287 Inputs.VR02 Run/Wire767; out Wire21→SD715.in | 출력 있고 처리 피드백이 없을 때 SD 시작 |
| 타이머값·소유 | ORef729/RID28 S5T#2S→715.value Wire739; ORef730/RID86 Tag_64/T67→operand Wire740 | 2초 지연. IEC TON/TIME 또는 FN01 90분과 혼동 금지 |
| 고장Set | Start753.out→Contact755.in(Wire754), T67 ORef731→755.operand(Wire741), 755.out→SCoil721(Wire22), ORef733/FAULT→operand(Wire744) | ON AND Start AND T67 접점이면 FAULT Set |
| 고장Reset | ON751.out→Contact759 RESET_ALLARM(ORef734/Wire746)→Contact761 FAULT(ORef735/Wire747)→RCoil726(Wires760/762); ORef736→operand Wire749 | ON AND RESET_ALLARM AND FAULT이면 FAULT Reset |

- Reset 분기에 `피드백 회복`을 확인하는 조건은 없다. 따라서 Reset으로 원인이 제거됐다고 판정하면 안 된다.
- 고장은 motors1의 M_VR_02 Reset을 통해 요청을 지운다. 고장해제만으로 그 요청을 Set하는 VR02 전용 코일은 이 알람망에 없다. HMI 새 요청·자동 순서 쓰기와 충돌/재시도 여부는 따로 확인한다.
- Set721/Reset726이 같은 네트워크에 있고 자동인터럽트/HMI도 요청을 쓸 수 있으므로 동시조건·반복요청·전원재시작의 최종값은 현재 실행검증 없이 단정하지 않는다.

### 5.2 공통 Reset 입력 경계

- `0158/LAD930`: Inputs.Reset_allarmi ORef24(0565 RID57/AO159=DB13.X19.7) Contact23와 Flag.Reset_Allarms_HMI ORef27(RID61/AO108=DB2.X13.4) Contact26를 OR28로 묶는다(Wires22/25/29/30). OR.out Wire38→SCoil33, operand ORef37/RID2 RESET_ALLARM(Wire36). 같은 분기에 HMI reset-request Reset과 별도 TOF 경로가 있으나 VR02 접촉기 회로 자체를 인버터 reset 소유로 바꾸지 않는다.
- HMI CSV 행188 `ResetAlarms`, DB2,X13.4, 내부ID002E1은 위 HMI 요청 설정과 일치한다. 실제 클릭 이벤트/권한은 미확인.
- `0154/LAD931`: RESET_ALLARM OR STOP_HORN(OR224)→SD229, Tag_160=%T47/S5T#1S. T47 Contact263→RCoil235가 RESET_ALLARM을 해제한다(Wires251/252/253/264/254). 공통 reset pulse 정리 경로이며 VR02 고장검출 지연2초와 별개다.
- 원시 `%I19.7` 이름 Reset_Allarm과 처리 DB13.X19.7, 공통 DB2.X6.0, HMI DB2.X13.4는 구별한다. 이번 VR02 범위에서는 이 공통 입력의 전기 양 끝점·현재배선을 완전 재조사하지 않았다.

## 6. 증상별 관찰·원인 배제 초안

다음은 자료 수집/비교 계획이다. 실제 설비 조작·활선 측정·보호값 변경·우회·시험운전을 수행하거나 승인한 것이 아니다. 전기/기계 정비는 자격 있는 담당자의 현장 승인과 차단·잠금 절차가 선행되어야 한다.

| 증상 | 같은 시각 모을 관찰 | 비교·원인배제 순서 | 복구 판정 자료 |
|---|---|---|---|
| HMI 기동요청 후 Q3.0 없음 | HMI Flag 이벤트/DB2.X1.3, ON M0.0, FAULT DB3.X1.3, Q3.0, 자동Tipo/Tempo/Auto_ON1 | 실제 요청쓰기→고장Reset→0254 허가→상위FC 호출; 화면 DB11 응답을 Q로 대체하지 않음 | 승인된 새 요청과 출력/응답의 시간기록 |
| Q3.0은 있으나 KM/모터 미동작 | FG139 단자31·공통전원 상태, XS35/36·QS/QM 접점·49KM1 A1/A2 점검기록 | 논리출력→모듈/퓨즈→QS/QM→코일→주접점→M23를 나눔; 무단접점 우회 금지 | 자격자 전기점검 및 실제 모터/축 확인 |
| 시작 후 약2초 고장 | Q3.0, 원시 I3.7, DB13.X3.7, T67, DB3.X1.3 추세 | 접촉기13–14/FG119단자38와 입력전달0397/0030을 분리 비교 | 원인 제거 후 요청·피드백·알람의 일관된 추세, 재발유무 |
| KM 응답은 있으나 분진 배출 불량 | 원시 피드백, 승인된 모터전류/축회전·막힘·로터/감속기 점검보고 | KM 보조접점이 실제회전·유량·기밀성 증명이 아님을 먼저 확인 | 현장 기능확인·기계점검 기록. 모델/토크 임의작성 금지 |
| VR02 문제 뒤 FN01 경보/정지 | DB13.X3.7, FN01Run, Prealarms_FN01, T130, Local Stop_Fan_FN01, M_FN_01 | 0252의 VR02분기와 TC04/TC05/진동/VR01 다른 OR분기를 구분 | 어느 분기가 지속됐는지 및 FN01 소유 복구기록 |
| 운전시간이 1/0 반복·누적과 다름 | I3.7, T13, DB9.W120/W122, M1.7, M2.0, T17, 외부DB 기록 | 0317 Move1·0338 Move0와 외부기록 성공 여부 비교, 임의ADD로 수정 금지 | 실제 외부저장/집계의 별도 확인. PLC 버퍼=누적시간 오인 해소 |
| Reset 후 바로 재발/재기동 안 됨 | RESET_ALLARM, FAULT, M_VR_02, HMI/자동쓰기, I/DB/Q의 시각 | 원인 미제거·동시Set/Reset·재요청 부재를 구분 | 고장해제와 새 기동의 각각 독립 증거 |

관찰기록 최소필드: 관찰자, 시각/시간대, 물리위치, 태그/주소, 값·단위, 수집장치/방법, 프로젝트 커밋·CPU 온라인비교 여부, 비교원본/FG·PDF·LAD·핀, 배제한 원인, 승인된 조치, 복구증거, 미확정 사항. 운영 사진·개인정보·사용자 기록을 공개 Git에 복제하지 않는다.

## 7. 완료·누락·인계

### 7.1 네 기능 적용과 기록보존

| 기능 | 적용 판단 | 실제 상태 |
|---|---|---|
| 도면·래더 나란히 보기 | 0254↔FG49/139,0434↔FG49/119,0317↔원시I,0372↔HMI설정이 비교쌍 후보 | 원본 렌더·정적조사만. UI 통합/링크 상호동작 검증 안 함 |
| 백업·선택복원 | VR02 고유키와 기존/미지 필드 보존 필요 | 구현·저장·재읽기·재열기 시험 안 함 |
| 기록 전후 비교 | 요청/Q/raw/DB/FAULT/호출/전기점검의 시각별 비교 | 실제 사용자 기록 없음, 합성 QA도 이번 범위에서 안 함 |
| 보고서/PDF | 위 관찰필드와 원본판본·해시 포함 가능 | 새 보고서/PDF 제작·검증 안 함. 원본 PDF 렌더와 구별 |

### 7.2 누락 자료와 수용 기준

| 자료 | 필요한 위치/제공물 | 통과 기준 |
|---|---|---|
| 현행 VR02 식별 | M23/VR02 명판·현장 위치도·축/배출연결 사진·승인 P&ID | CY03 도면 연결과 현재 실물, 사용자 ‘2사이클론’의 의미를 별도로 대조 |
| PLC 원본·현재CPU | 정식 TIA 프로젝트/DB 구조/호출계층/교차참조/온라인비교 | ORef 결속, 간접·Word·HMI쓰기, 초기화·보존·OB주기를 확인 |
| HMI 이벤트 | VR02 화면객체, dde.cfg, press/release/스크립트·권한 | DB2 요청과 DB11 응답/알람, 실제 read/write 경로 확정 |
| 전기 현재배선 | 최신 준공 FG49/119/139, 단자/케이블라벨, QM/QS/KM 명판 | 양 끝점·실제 보호기/설정·모듈주소·49KM1 접점 확인 |
| 기계/제조사 | 승인 모터·감속기·로터 도면/설명서 | 현재 모델/방향/윤활·토크·정비 기준 확정 |
| 운전시간 저장 | 외부DB/HMI 기록 체계의 승인 설명·read-only 결과 | Move1/Move0 버퍼와 실제 누적/저장성공의 관계 확인 |
| 복구 | 승인된 조치 및 추세·현장 관찰 | 고장원인 제거, 새 요청, 출력/응답/실물 기능의 독립 증거 |

### 7.3 수행한 검토와 수행하지 않은 검토

- AGENTS/스킬/WORK-STANDARD/WORK-ITEM-TEMPLATE/INVENTORY 및 overlap 검토를 읽었다. 읽기전용 preflight 종료0.
- VR02와 직접 연관 공통부의 원본 XML/선언을 직접 파싱해 Part·Wire·ORef·RID·NID·UID·Global/Local·상수·쓰기 위치를 비교했다. 자체 추출 파일은 후보목록을 포함하며 **후보가 여러 개일 때 초안의 선택·미결속 판정이 우선**이다. 도면은 원본 PDF를 렌더해 확인했다.
- `extracts/VR02/source-sha256.json`의 **87개 파일 모두 로컬 SHA256과 고정 git blob 바이트/SHA256이 일치**했다. 자세한 파일목록은 부록에 있다. 원본 repository 상태는 조사 시작과 종료에 clean으로 확인했다.
- 이번 검토는 자체 원본조사다. 독립 검토자는 아직 없다. XML 파싱/본문·해시 정적확인은 PLC 실행시험이 아니다.
- UI/모바일·저장/재열기·복원·BC01 회귀·패키지·배포·TIA compile·CPU·현장복구는 이번 조사초안 범위 밖이라 미수행이다.
- 시뮬레이터 작성/수정/생성/실행/행동시험0. 실제 PLC·현장·보호값·SEJIN 운영자료·공통코드·버전·대장·배포 변경0. 중지 이력과 미확정 필드를 지우지 않았다. 기존18불일치/1060확인대기/577설계시험을 해결·실행완료로 갱신하지 않는다.

| 상태축 | 이번 상태 | 근거/한계 |
|---|---|---|
| documentation | draft_complete_with_gaps | 7영역 초안, 원본 연결·누락 명시 |
| static_review | source_checked, independent_review_pending | XML/선언·도면렌더·87해시 자체대조 |
| ui_records | not_run | 통합/기록기능 검증 제외 |
| publication | not_published | 로컬2차133 통합·게시 제외 유지 |
| tia_compile | not_performed | 정식 프로젝트 검증 미수행 |
| live_cpu | not_performed | 현재 CPU·강제값·호출 미확인 |
| field_recovery | not_performed | 명판·준공·조치·복구 미확인 |

핵심 핀·도면·미결속의 제한 검토를 마쳤으며 다음 첫 조치는 사용자 독립 검토다. 현장자료가 없다는 이유로 CY02/P14 식별을 확정하거나 로컬 통합·게시를 자동 재개하지 않는다.

## 부록 A. 근거 파일의 읽는 방법

- XML 경로 접두사: `all-in-one/sources/decoded-original/`. 예를 들어 `0254`는 `0254-FlgNet.xml`, 선언 `0604`는 `0604-IdentXmlPart.xml`이다.
- LAD 번호는 문서색인 ID이며 원본 네트워크 NID와 다르다. 원본 조각이 한 줄이어도 `Part UId`, `Wire UId`, `ORef UId/RefId`, 선언의 `RID`와 `C NID/UID/AK`로 위치를 재현할 수 있다.
- Git 고정 링크의 기준은 `https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/`이다. 다음 표의 경로를 이어붙이면 같은 원본을 확인할 수 있다.
- 자체 렌더: FG49-PDF50, FG119-PDF120, FG139-PDF140, FG252-PDF255, CON-PDF31/51, PID-PDF1 및 VR02/제목 영역. 이 렌더는 편집한 설계도가 아니라 읽기 확인용이다.

## 부록 B. 고정 원본 SHA256 / git blob 대조

아래 모든 행은 bytes equality=true다. 원본 해시 일치가 현재설비 또는 런타임 검증을 뜻하지 않는다.

| 원본 파일 | SHA256 |
|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` |
| `all-in-one/registers/all-in-one-data.json` | `63a46b36b6454bf1246d093300dbee11f2fcc287ad94991405369bf9f939a8fe` |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` |
| `all-in-one/registers/plc-symbols.csv` | `a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` |
| `all-in-one/sources/decoded-original/0019-FlgNet.xml` | `a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5` |
| `all-in-one/sources/decoded-original/0024-FlgNet.xml` | `a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67` |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` |
| `all-in-one/sources/decoded-original/0040-IdentXmlPart.xml` | `4aa4f09101f827918ca2af003544aa0de8a70410cc4d69e738f2d6220669f182` |
| `all-in-one/sources/decoded-original/0067-IdentXmlPart.xml` | `0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628` |
| `all-in-one/sources/decoded-original/0068-IdentXmlPart.xml` | `0a71d492e69760390b99f71a75f02ef684e271554b003d5de8bf64a26c64eeba` |
| `all-in-one/sources/decoded-original/0154-FlgNet.xml` | `b0a163ffa382b722eaa34df4bdc4c3dd06039b296b791d26d68639a7b0502746` |
| `all-in-one/sources/decoded-original/0158-FlgNet.xml` | `d3f3adebc3d990b85c5d4c294906ae3bc3dafebb49d25b030bf9cc2ccf905651` |
| `all-in-one/sources/decoded-original/0162-FlgNet.xml` | `892eab96a4f5c87cfafd35f8a2e2a04982a93ca23c777312101882e408b11deb` |
| `all-in-one/sources/decoded-original/0164-FlgNet.xml` | `15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491` |
| `all-in-one/sources/decoded-original/0165-FlgNet.xml` | `4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88` |
| `all-in-one/sources/decoded-original/0166-FlgNet.xml` | `0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853` |
| `all-in-one/sources/decoded-original/0168-FlgNet.xml` | `6e69605abd053c1d85f668b8e29bf98975e7e6b9ec1903b017af2048602d4847` |
| `all-in-one/sources/decoded-original/0252-FlgNet.xml` | `66b8bf7c1e033f2e6710ab6959e1f5ec2cf27bd6e90c8780eb1bd6daebf76749` |
| `all-in-one/sources/decoded-original/0253-FlgNet.xml` | `2d35470eb44fff79916b93fcf57a597b2b9a03211e8493c2283706dc2c875154` |
| `all-in-one/sources/decoded-original/0254-FlgNet.xml` | `568a4cfb029a4f1a8babf2e3ad2c515d9ca52655890bf65446cca2f796859258` |
| `all-in-one/sources/decoded-original/0317-FlgNet.xml` | `e352b630d675157b03dbd97376f60ca65e19b8dedb2ec59d067e58bb02310ce3` |
| `all-in-one/sources/decoded-original/0338-FlgNet.xml` | `762ab4b1520aa101efc897ff9e4b72a35f5591ff460a0b654dc87919849077a1` |
| `all-in-one/sources/decoded-original/0341-FlgNet.xml` | `e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96` |
| `all-in-one/sources/decoded-original/0355-FlgNet.xml` | `73592d33f8b3a71effeb36f25427c76e931485e7ce31f5c81f144ddae83c4247` |
| `all-in-one/sources/decoded-original/0372-FlgNet.xml` | `badb107b5654fdf3ac04a3a8d5a67913f3b88c6b6b03b2682311720ba584e484` |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` |
| `all-in-one/sources/decoded-original/0434-FlgNet.xml` | `31c8de50439465d356d0735765fa0ab0983585e0f1fbfab6bf614b054566f3f9` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` |
| `all-in-one/sources/decoded-original/0553-IdentXmlPart.xml` | `4bf2f2c613e81ee6bd92ac0f21252ea0ce4a1135818fcc404740a914aaae1317` |
| `all-in-one/sources/decoded-original/0555-IdentXmlPart.xml` | `46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6` |
| `all-in-one/sources/decoded-original/0559-IdentXmlPart.xml` | `ec5c6d3f18cbedc2bf695fb1318c1d3a8d2a71c77fbd4ab30d286e2399a289d1` |
| `all-in-one/sources/decoded-original/0564-IdentXmlPart.xml` | `2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1` |
| `all-in-one/sources/decoded-original/0565-IdentXmlPart.xml` | `0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149` |
| `all-in-one/sources/decoded-original/0566-IdentXmlPart.xml` | `a1914c7ae085acc1f949a649979824bec8b46fcd78a8055318272a1eb5a45265` |
| `all-in-one/sources/decoded-original/0567-IdentXmlPart.xml` | `5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e` |
| `all-in-one/sources/decoded-original/0575-IdentXmlPart.xml` | `40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06` |
| `all-in-one/sources/decoded-original/0576-IdentXmlPart.xml` | `c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe` |
| `all-in-one/sources/decoded-original/0577-IdentXmlPart.xml` | `511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47` |
| `all-in-one/sources/decoded-original/0578-IdentXmlPart.xml` | `0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b` |
| `all-in-one/sources/decoded-original/0584-IdentXmlPart.xml` | `3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d` |
| `all-in-one/sources/decoded-original/0586-IdentXmlPart.xml` | `f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250` |
| `all-in-one/sources/decoded-original/0590-IdentXmlPart.xml` | `baff7271b3db646e8953c31d20b72f7b044b1154b689b15ca0fb38ebb44ad81c` |
| `all-in-one/sources/decoded-original/0595-IdentXmlPart.xml` | `10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52` |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` |
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` |
| `all-in-one/sources/decoded-original/0613-IdentXmlPart.xml` | `09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb` |
| `all-in-one/sources/decoded-original/0614-IdentXmlPart.xml` | `c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294` |
| `all-in-one/sources/decoded-original/0615-IdentXmlPart.xml` | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` |
| `all-in-one/sources/decoded-original/0616-IdentXmlPart.xml` | `650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d` |
| `all-in-one/sources/decoded-original/0621-IdentXmlPart.xml` | `a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee` |
| `all-in-one/sources/decoded-original/0622-IdentXmlPart.xml` | `f0b997f1246d76cff71de2160eb617caa936e6987bdf43c73f55cdcf77dccdb6` |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` |
| `all-in-one/sources/decoded-original/0625-IdentXmlPart.xml` | `17a9f9bd540bf0a54e9973391fa258d81e567248fd201ae4ff32c367359e69f9` |
| `all-in-one/sources/decoded-original/0626-IdentXmlPart.xml` | `a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` |
| `all-in-one/sources/decoded-original/0652-IdentXmlPart.xml` | `251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692` |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` |
| `all-in-one/sources/decoded-original/0661-IdentXmlPart.xml` | `90672199fee355011f581d3287046894772f3f3b4cb78bbe0dd0d71bd488ac93` |
| `all-in-one/sources/decoded-original/0682-IdentXmlPart.xml` | `25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` |


## 전달 전 핵심 근거 제한 검토

2026-10-11 조사 초안 취합 단계에서 핵심 출력/타이머/운전시간 또는 요청쓰기의 원본 Part/Wire를 표본 재대조하고, 도면 전달 끝점을 실제 렌더로 재확인했다. 인용 원본 SHA256도 전부 재계산하여 일치했다. 전체 원본의 의미 검토나 현재 CPU/현장/통합/게시 검증을 뜻하지 않는다. 사용자 독립 검토용 초안이며 미확정 경계는 유지한다.
