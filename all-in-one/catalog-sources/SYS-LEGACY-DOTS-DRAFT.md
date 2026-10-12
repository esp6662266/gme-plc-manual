# SYS-LEGACY — 과거 태그·이름 대응 자체 조사 초안

## 핵심 확인·상충·누락

- 대상은 software catalog ID **SYS-LEGACY 한 개**다. 과거 이름을 현재 장치로 병합하거나 RD01/FN01/BR01/계측기를 같이 완료로 세지 않는다.
- **FR01 → RD01 속도 데이터, VT01 → FN01 속도 데이터**는 원본 선언과 실제 출력 핀으로 확인된다. `Data.SET_PERC_FR01`은 DB1.DBW6, `Data.SET_PERC_VT01`은 DB1.DBW8이며 각각 Peripherie Word 출력 PQW290/PQW292로 이어진다. 이는 백업 프로그램의 데이터 역할 대응이지 역사상의 FR01/VT01과 현재 실물의 동일성 증명은 아니다.
- **Riduce MN01은 %M1.2 Bool 메모리**다. 0180 NID10에는 OFF 접점→Add 두 개 및 ON 접점→비교→S/R가 있다. 제목만 읽고 “항상 TC01+30에서 실제 MN01 감속”이라고 결론내리면 안 된다. Int 덧셈/Local Int 임시값과 Real 비교 형식의 차이, OFF/ON의 현재 값, downstream 소비처가 남아 있다.
- **PC03/PC_03/TR01/MN02/MN03/MN04는 주로 live_index의 오래된 인터페이스 설명**이다. Flag 이름129개에 괄호 설명64개, 계수 DB 이름129개에51개, Data 이름162개에69개여서 배열을 일대일 zip해 이름을 자동 배정할 수 없다. 이 숫자는 토큰/괄호 그룹 계수이며 의미 대응 수가 아니다.
- catalog 역할 문구의 “DB 설명은 block_summary 및 live_index에 보존”은 범위를 좁혀야 한다. 이 고정본에서 PC03/PC_03/TR01/MN02~04 문자열은 **live_index에는 있지만 block_summary 89개 레코드에는 없다**. block_summary는 FR01/VT01/MN01의 네트워크 색인 역할로 재사용한다. 원 대장은 수정하지 않았다.
- 공유 근거: RD01 초안의 0243/0465 동일 SP의 0 비교와 최소5 쓰기, 0244/0275 EV03 시간 경계·FG20/112 대응을 연결 재사용하며 이번에 고유 핀과 PDF를 직접 대조했다. BR01 초안의 0180 파일 목록은 탐색 참고일 뿐, 그 해시가 본 네트워크의 의미 검토 완료를 뜻하지 않는다. PC01/PC02/PSH01 기존 조사와 PC03을 병합하지 않는다.

## 1. 설비·자료 기준 — 적용

- 기준 원본: `gme-research/source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. Git 시작 상태 clean, 기준 HEAD 일치. 현행 게시 v1.16.0이나 현재 CPU를 이번 고정본으로 검증하지 않았다.
- 대장: `docs/equipment-standard/INVENTORY.json#/catalog/39`, phase2/planned, 부모 없음, 실물 동일성 미확인. `progress/TASK3-BATCH11-SCOPE.json` 및 `GME-CATALOG-OVERLAP-REVIEW.json` 해당 행을 읽었다. 기존 제외90/부모 보류7/로컬2차133 통합 제외는 유지한다.
- 목적: 이름·주석·데이터 주소·핀·출력 역할의 서로 다른 증거 수준을 분리한다. 새로운 장치나 명칭 사전을 현장 사실로 만들지 않는다.
- 실행 모델/추론 런타임 증명은 미확인. 로컬 TIA 접근, 사용자 Mac, 새 Work/Codex, 재위임, 외부 장비 접근 없음.
- 원본 build/test/generator 및 시뮬레이터를 실행하지 않았다. 허용된 텍스트 검색, XML 정적 파싱, 해시/Git blob 비교, 원본 PDF 렌더만 수행했다. PLC·현장·보호값·SEJIN·운영 기록·공통 코드·버전·대장·배포 변경 없음.

### 이름 대응의 증거 등급

|과거 문자열|직접 확보 근거|가능한 결론|금지하는 결론/누락|
|---|---|---|---|
|Riduce MN01|0582 RID87/NID10 UID553·556, live_index471, 0180|M1.2 S/R 메모리 이름|실제 MN01 모터 존재, 어느 현재 모터인지, 실제 감속 완료|
|SET_PERC_FR01|0662 RID43→0465 Mul422→0664 RID48|RD01 속도 출력으로 쓰이는 DB1.DBW6|FR01과 RD01의 역사적 실물 동일성|
|SET_PERC_VT01|0662 RID49→0466 Mul473→0664 RID53|FN01 속도 출력으로 쓰이는 DB1.DBW8|VT01과 FN01 실물 동일성 또는 VT02도 같은 장치|
|EVFR01_Work/Wait_time|0604 RID50/52, 0275·0244|RD01 운전 연계 EV03의 시간 인수 Word|FR01 본체 전체, 실제 현재 시간·윤활 정상|
|PC03/PC_03|min_dp_pc03,zero_pc_03,coeff_pc_03,setpoint_pc03,dp_aspir_pc03 등의 live_index1604/1629 설명|과거 설명 잔존|PC01/PC02/PSH01/DP01 등 어느 현재 계측기인지 확정|
|TR01|live_index452의 m_tr01,1629의 set_perc_tr01;1697의 zxtr01_fault000… 부분문자열|설명/잔존 이름이 검색됨|TR01 현재 장치·알람 존재. zxtr01 부분일치도 독립 TR01 선언이 아님|
|MN02/03/04|live_index452 설명 m_mn02/m_mn03/m_mn04|옛 command Word 설명 잔존|현재 Flag 배열 순서로 모터 재명명|

## 2. I/O·HMI — 적용, 이벤트/실물 결속 미확보

원본 XML 경로 접두는 `all-in-one/sources/decoded-original/`이다. AO/BO는 이 선언의 bit offset이며 byte로 환산할 때 형식과 DB/메모리 영역을 함께 확인했다.

|신호|원본 선언/주소|역할과 한계|
|---|---|---|
|Riduce MN01|0582 SimpleAccess Global RID87, Bool OD1, SAD Memory, AO10 → M1.2; NID10 UID553 S Write·556 R Write|물리 출력 아님. live_index471 `%m1.2`와 교차 확인|
|ON/OFF|0582 RID1/RID80, Bool Memory AO0/AO1 → M0.0/M0.1|상수 노드가 아닌 메모리 선언. 이름으로 현재 true/false 단정 금지|
|Data.SET_PERC_FR01|0662 GlobalAccess RID43 AO48 Int16; BAD9→0660 DepDBBlock RID9/TOD DB1|DB1.DBW6; 0604 RID44,0577 RID43,0642 RID92는 다른 문맥의 같은 symbolic field 후보/선언으로 따로 보존|
|Data.SET_PERC_VT01|0662 GlobalAccess RID49 AO64 Int16; 같은 DB1 결속|DB1.DBW8; 0604 RID116,0577 RID60,0642 RID93은 문맥별 식별자|
|RD01_SP_SPEED|0664 SimpleAccess Global RID48/NID6 UID437 Write, Word16, Output AO2320, SAM Peripherie|PQW290 직접 주변장치 접근. 일반 메모리/HMI/물리 피드백과 다름|
|FN01_SP_SPEED|0664 Global RID53/NID7 UID488 Write, Word16, Output AO2336, SAM Peripherie|PQW292. Word 값의 스케일을 실제 Hz로 바꾸려면 드라이브 설정 필요|
|Data.TC01_SETPOINT|0585 RID59 AO528 Int16; BAD58→0584 DB1|DB1.DBW66. 이번 상수30/25는 해당 과거 논리의 원문이며 현장 안전값 아님|
|Manage_TC1_2.PID_Ref_Temp|0585 RID242 AO16 Real32; BAD241→0584 TOD DB39|DB39.DBD2. 원시 TC01 채널과 동일시 금지|
|App02/App03|0583 InterfaceAccess Local RID83/86, Int16 AO32/48|로컬 임시값. Global DB39 Real과 형식이 다름|
|EVFR01_Work_time/Wait_time|0604 RID50/52 Word16 AO736/752; BAD20→0603 DB1|DB1.DBW92/94, S5 타이머 value 인수. 이름에 time이 있어도 SEC Bool과 별개|

`all-in-one/sources/hmi_plc_tags.csv` 782행 중 주소 `DB1,INT6`/`DB1,INT8`/`DB1,INT66`는 각각 `data_DB1_DBW6`(내부ID002C9), `data_DB1_DBW8`(002B8), `data_DB1_DBW66`(00251), Access Name PLC로 확인했다. 이 CSV는 dde.cfg 설정이며 현재값/이벤트 실행/쓰기 권한 증거가 아니다. 이 세 주소와 XML의 byte offset 대응은 확인했으나 화면 객체·버튼·스크립트까지 결속하지 않았다. 검색 문자열이 없는 HMI를 “장치 없음”으로 판정하지 않는다.

### 오래된 DB 설명을 현재 배열에 매핑하지 않는 이유

live_index `_7ev`, i452의 이름 시작은 `m_bc_01 m_rd_01 m_rd_01_fan m_mc_03 …`인데 설명은 `com_w0 bit8 (m_tr01) com_w0 bit9 (m_mn02) …`로 시작한다. 같은 행으로 평탄화된 값은 멤버별 comment 경계를 복원할 수 없는 상태다. i1604에는 `min_dp_pc03`, `zero_pc_03`, `coeff_pc_03`, `setpoint_pc03`; i1629에는 `set_perc_tr01`, `dp_aspir_pc03`가 남아 있지만 이 설명만으로 새 IO 주소를 부여하지 않는다. 원 DB 멤버별 comment export/offset/구판 변경 이력이 추가로 필요하다.

## 3. 제어 구조 — 대표 고유 핵심 원본 직접 검토

### L1. MN01 감소 메모리: 제목과 실제 연결을 분리

live_index i1864 / block_summary `burner control`의 제목은 `reduce speed mn01 se tc01 > 30°c the setpoint`. 대응 `0180-FlgNet.xml`, 원 선언 NID10.

- Wire581 powerrail→Contact577.in; W557 ORef543/RID80 OFF→577.operand.
- W578 **577.out이 Add517.en, Add523.en, Contact579.in에 함께 연결**된다. OFF 조건을 뺀 해석은 원본과 다르다.
- Add517 SrcType Int: W558/UID544 TC01_SETPOINT→in1, W559/545 literal30(0586 RID82)→in2, W560→UID546 Local App02(RID83).
- Add523 SrcType Int: W561/547 TC01_SETPOINT→in1, W562/548 literal25(RID85)→in2, W563→UID549 Local App03(RID86).
- Contact579 operand W564/UID550=ON. W580 579.out→Ge533.pre 및 Lt539.pre.
- Ge533 **Real**: W565/551 PID_Ref_Temp→in1, W566/552 App02→in2; W567→SCoil536.in; W569/553 Riduce MN01→operand.
- Lt539 **Real**: W570/554 PID_Ref_Temp→in1, W571/555 App03→in2; W572→RCoil542.in; W574/556 같은 Riduce MN01→operand.

정적 의도 후보는 +30 이상 Set/+25 미만 Reset의 히스테리시스 구조지만 원본 Add Int/임시 Int와 비교 Real이 다르고 OFF 및 ON이 직렬이다. 이 네트워크에 명시적 Int→Real 변환 Part는 없다. 현재 TIA 형식 해석·컴파일·호출/실행을 확인하지 않았으므로 현재 실효 온도 판정이나 스캔 결과로 확정하지 않는다. 타이머, 실제 속도 출력, 모터 명령 Part도 이 네트워크에는 없다. 검색한 695 XML의 MN01 선언은 0582 한 파일, NID10 두 Write이며 이름으로 확인된 Read/감속 소비처는 미확보다. 간접주소/다른 미추출 코드까지 “없음”으로 일반화하지 않는다.

### L2. FR01 명칭이 RD01 출력으로 이어지는 핀

`0465-FlgNet.xml`, live_index1684, analog output conversion NID6, title rd-01 cylinder.

- Contact455 ON(UID426/RID1), W456→Lt406.pre/Gt414.pre/Mul422.en.
- Lt406 Int: UID427/RID43 SET_PERC_FR01와 UID428/RID44 literal5. W441→Move409.en, W443 UID429=5→in, W444 out1→UID430/RID43 같은 DB1.DBW6 Write.
- Gt414 Int: UID431/RID43와 UID432/RID12 literal100. W447→Move417.en, W449 UID433=100→in, W450 out1→UID434/RID43 Write.
- Mul422 Int: W451 UID435/RID43→in1, W452 UID436/RID16 literal272→in2, **W453 out→UID437/RID48 RD01_SP_SPEED**.
- 선언0661은5/100/272를 Int literal로 확인한다. ENO를 보지 않고 결과 성공을 발명하지 않는다. 원본에 보이는 out 연결까지 검토했다.

### L3. VT01 명칭이 FN01 출력으로 이어지는 별도 핀

`0466-FlgNet.xml`, live_index1685, NID7, title fn-01 ventilator.

- Contact506 ON UID477/RID1, W507→Lt457.pre/Gt465.pre/Mul473.en.
- Lt457 UID478 SET_PERC_VT01와 UID479 literal5→W492 Move460.en; W494 5→in; W495 out1→UID481/RID49 Write.
- Gt465 UID482 SET_PERC_VT01와 UID483 literal100→W498 Move468.en; W500 100→in; W501 out1→UID485/RID49 Write.
- **Mul473 Int W502 UID486/RID49→in1, W503 UID487 literal272→in2, W504 out→UID488/RID53 FN01_SP_SPEED**.

최소5/최대100과 ×272는 백업 논리 사실이며 현행 보호 설정/Hz/정격 범위가 아니다. FR01과 VT01에는 각각 다른 출력 선언이 있다. 두 이름이 과거 방식이라는 이유로 하나의 공통 속도 변수로 합치지 않는다.

### L4. 0 비교와 다른 쓰기: 현재 최종값 미확정

- `0243` motors1 NID7의 Eq227 Int(in1 W254/UID243 SET_PERC_FR01; in2 W255/244 0)→W31 OR28.in3→W30 RCoil236→W265 UID249 Flag.M_RD_01. 정상 요청 Contact282→W283 Coil240→W268 UID251 Start RD01은 별도 가지다. 다른 OR 입력은 RD_01_FAULT, RD01_INV, NOT fan RD01 run 및 NOT R2_GATE_LOOP_ON·NOT STANDBY_ON·NOT UNDER TESTING 직렬 가지다.
- `0253` NID22 Eq678 Int(in1 W702/UID692 SET_PERC_VT01; in2 W703/693 0)→W704 OR676.in3→W709 RCoil685→W711 UID697 Flag.M_FN_01. 별도 Contact726→W727 Coil689→W714 UID699 Start FN01. 다른 입력은 FN_01_FAULT, FN01_INV, Local Stop_Fan_FN01, HYDROGEN_BOX_FAULT AND NOT UNDER TESTING이다.
- 두 0 비교와 0465/0466의 최소5 보정은 **같은 설정 Word의 다른 사용/쓰기**다. 따라서 “0이면 언제나 정지” 또는 “0이 절대 유지되지 않는다”를 실행순서 없이 단정하지 않는다.
- 0577의 FR01 RID43 UID625(NID3)/976(NID4), VT01 RID60 UID644/992 및 NID11 UID87/95/103/109/115가 다른 Write로 선언된다. 0642 NID1 FR01 RID92 UID3840, VT01 RID93 UID3788에도 Write가 있다. 이 모든 큰 네트워크/레시피/주기 순서의 의미 전수 검토는 이번 범위가 아니다.
- block_summary/live_index364 SCL 색인에는 recipe `.rd01`→`data.set_perc_fr01`, `.fn01`→`data.set_perc_vt01`가 있다. 이는 추가 역할 단서이나 직접 SCL 컴파일/실행 증거가 아니다. 이미 직접 확인한 출력 결속의 보조 색인으로만 사용한다.

### L5. EVFR01 시간은 EV03 제어 경계

`0275` NID45의 CRef36/45 RefId248, CodeBlock35/44 RefId241 호출은 색인1937에서 KF_KT로 나타난다. W37 UID38 Data.EV_03_W→36.KF; W39 UID40 literal Bool0(0606 RID249)→36.SEC; W42 36.KT→UID43 Data.EVFR01_Work_time. **W41 36.eno→45.en**으로 이어진다. W46 UID47 Data.EV_03P→45.KF, W48 UID49 Bool0→45.SEC, W51 45.KT→UID52 Wait_time. CRef 숫자만으로 다른 문맥의 KF_KT 호출에 연결하지 않는다. 변환 블록 내부 동작은 RD01/PV 공통 조사 참조이며 이번 재검토는 호출 핀/인수 형식 경계까지다.

`0244` NID8에서 ON295→Start RD01 Contact297→NOT Tag115 Contact299→SD257, value W282/UID271 Work_time, operand W285/UID273 Tag116. Tag116 Contact301→SD262, value W286/UID274 Wait_time, operand W289/UID276 Tag115. NOT Tag116 Contact303→ON305→Coil268 EV03(W293/279)이다. 0602의 Tag115/116은 Timer, EV03은 Output이다. 시간 Word, Timer 상태, EV03 실제 밸브 작동을 각각 구분한다. 현재 인수값/복구 조작은 제공하지 않는다.

## 4. 전기 전달 경로 — 관련 출력만 적용, SYS-LEGACY 독립 실물은 비해당

`Electrical_Rev2.pdf` **PDF21=FG20, PDF48=FG47, PDF113=FG112** 세 장을 실제 렌더했다. 세 footer 모두 원작성 DATA27.05.2024, **Rev2 17.03.2025**, TOT262를 각각 눈으로 확인했다. 전체 PDF가 동일 개정이라고 확장하지 않는다.

- FG112/PDF113 ANALOG OUTPUT MODULE CPU515 MOD7: PAW290 QV1/QI1 **단자5**, MANA **단자8** → +PAW290/−PAW290, 상대참조20/6. FG20/PDF21 RD01의 20AS1 **2 AI1+ /3 AGND−**로 이어진다. 20SCH2 차폐는 FG112에서109/4, FG20에서109/3 표기다. 이 차폐 교차참조 차이는 남기며 임의 정정하지 않는다.
- 같은 FG112 PAW292 QV2/QI2 **단자9**, MANA **단자12** → +PAW292/−PAW292, 상대참조47/6. FG47/PDF48 FN01의 47AS1 **2 AI1+/3 AGND−**. 47SCH2는 FG112109/5, FG47의 차폐 표시는109/4이다. 이 참조 차이도 실물 배선으로 해결하지 않는다.
- 두 회로에 인쇄된4–20mA 및 ABB 모델/모터 표시는 도면 근거다. 현재 드라이브 AI 모드, 현장 케이블, 보호설정, 실제 출력값은 확인하지 않았다. 원본 PQW290/292와 PAW290/292는 주소/역할 대응 근거이며 현재 CPU 하드웨어 일치 증명은 아니다.
- SYS-LEGACY 자체에 별도 전원/보호기/단자/케이블을 만들지 않는다. MN01/PC03/TR01/MN02~04의 고유 전기 끝점은 확보하지 못했다. 전체 RD01/FN01 전력·STO·Reset 회로를 본 catalog의 소유로 복제하지 않는다.
- 참고: 이번 검토는 아날로그 경로이며 릴레이 접점 판정에 사용하지 않았다. RD01 기존 START5/9와 RESET6/10 정정 이력은 그대로 유지한다.

## 5. 알람·복구 — 관련 소유 경계 적용, 전용 현장 복구 미확보

- MN01의 S/R는 `%M1.2` 기억 비트 갱신이다. SCoil/RCoil이라는 이유로 알람 래치/ACK/운전자 Reset이라고 부르지 않는다. 0180에는 알람 Word 쓰기, 사이렌, 독립 타이머 없음.
- FR01/VT01 이름이 쓰이는 0243/0253은 RD01/FN01 운전 요청 Reset 조건에 연결된다. `Flag.M_RD_01`, `Flag.M_FN_01` Reset은 해당 운전 요청 해제이며 모든 알람 지우기/드라이브 복구 완료가 아니다.
- live_index1697의 `zxtr01_fault0000000000`는 TR01 부분 문자열 검색 결과다. 설명의 현재 알람 이름/위치와 확정된 직접 네트워크가 없어 TR01 전용 알람을 신설하지 않는다.
- SYS-ALARM/BR01/RD01/FN01의 기존 알람·복구 문서는 관련 소유로 링크한다. SYS-LEGACY에 동일 알람 완료를 중복 집계하지 않는다. 현장 원인 제거, 리셋, 재기동, 보호값 변경은 수행하지 않았고 권고값도 제시하지 않는다.

## 6. 증상별 관찰 — 수리 실행 없이 기록 설계

|관찰 상황|읽어서 비교할 증거|필요 기록/판정 경계|
|---|---|---|
|과거 FR01 설정을 바꿨는데 RD01 화면이 달라짐|DB1.DBW6/HMI INT6/0465·0243; 독립 승인된 현재 프로젝트|관찰 시각/프로젝트/모드/원시 설정·PQW290·실제속도 따로. 변경 시험 금지|
|VT01 표기와 FN01 속도가 혼재|DB1.DBW8/HMI INT8/0466·0253|레시피/자동쓰기·스캔 순서·AI1설정 확보 전 최종값 원인 단정 금지|
|MN01 감속 이름만 존재|M1.2, M0.0/M0.1, App02/03 타입, PID_Ref_Temp와0180|현재 TIA 선언/컴파일·소비처 cross-reference가 필요. 강제비트/온도 시험 금지|
|PC03를 PC01이나PSH01로 자동 연결하려 함|live_index1604/1629의 설명과 멤버 단위 원본|구판 날짜·도면·변경표·주소·명판 있어야 식별. 이름 일치만으로 수정 금지|
|TR01/MN02~04 알람·버튼을 찾을 수 없음|live_index452의 원 comment와 현재 Flag 선언|옛 comment 존재와 현재 장치 존재 분리. 자료 부족을 고장으로 판정하지 않음|
|EVFR01 시간이 초/밀리초로 오인됨|0275 SEC Bool0·KT Word,0244 SD value|원래 형식/변환 호출·백업값/현재값 구분. 임의 단위변환·운전 시험 금지|

공통 관찰 필드: 관찰자, 실제 시각/시간대, 위치/장치·프로젝트 버전, 읽은 주소/형식/값/단위, 화면/로그 출처, 비교 원본, 불일치와 미확정, 수행 조치(이번에는 없음), 복구 증거(미확보). 사용자 실제 운영 기록을 공개 원본에 넣지 않았다.

## 7. 완료·누락·인계

|영역/상태|결과|
|---|---|
|documentation|complete_with_gaps: 한 catalog의7영역 초안. 원본 고유핵심+역사명칭의 한계 명시|
|static_review|limited_core_review:7개 FlgNet 대표 원본 핀 직접 읽기. 모든 네트워크 의미 전수 검증 아님|
|ui_records|not_run: 화면·저장·재열기·선택복원·비교·보고서 기능 구현/검증 없음|
|publication|not_published: 원본·버전·대장·배포 변경 없음|
|tia_compile / live_cpu / field_recovery|모두 not_performed|
|physical_identity_verified|false 유지|

네 기능(도면/래더 비교, 백업/선택복원, 기록 전후비교, 보고서/PDF)은 이번 조사자료를 후속 구현에 활용할 수 있으나 SYS-LEGACY 카드에 구현/검증했다고 주장하지 않는다. 기존 note/repair_observation·미지 필드·저장키·다른 설비 데이터는 건드리지 않았다.

### 범위와 미해석

- 텍스트 검색: decoded-original XML **695파일**, live_index **2014레코드**, block_summary **89레코드**, HMI CSV **782행**. XML 이름검색 hit5파일/선언노드11개는 고유 장치 수 또는 의미검토 수가 아니다. FlgNet은 이름 대신 RefId가 들어 있어 이름검색만으로 소비처가 완전하다고 볼 수 없다.
- 대표 핀 직접 검토:0180/0465/0466/0243/0253/0275/0244의7개 FlgNet. 초기 자동시퀀스/큰 출력전달/레시피 모든 네트워크, 간접주소쓰기, 현재 HMI 이벤트, 전체 call graph·실행순서, current CPU는 미해석/미수행.
- 전체원본 보존 검사는 공통 UC01 보존목록712파일과 중지5자산의 해시를 현재 고정본에 다시 대조한다. 이는 검색/의미검토 수와 다르다. 선정 근거31파일의 SHA/Git blob 전체 목록은 아래에 별도 수록한다.
- 추가 자료: 멤버별 comment가 보존된 원 TIA DB export, 구판-현행 태그 변경대장, 허가된 현재 프로젝트 cross-reference/compile, HMI 화면/스크립트 export, 날짜가 있는 도면 변경 이력과 명판/배선 확인. 새로운 자료가 없으면 기존 실물 보류를 반복 조사하지 않는다.
- 다음 한 단계: 통합자가0180의 OFF 공통 직렬·Int/Real 경계 및 FR01/VT01의 출력 결속을 독립검토하고 본 초안만 수신 보존한다. 로컬2차133 통합/게시를 자동 시작하지 않는다.

## 실제 작업 시각(UTC)

- 2026-10-11 11:45:14: 배정 착수,11차 지시·범위와 필수 표준 읽기 시작.
- 11:45:31: 기준 HEAD/clean Git 확인, 과거 이름 직접 선언 검색.
- 11:46:26:0180/0465/0466 원본 Part/Wire 직접 읽기.
- 11:47:12: 원본 PDF21/48/113 렌더 생성;11:47:19 실제 이미지/개정란·끝점 시각 확인.
- 11:47:55:0243/0253/0275/0244 관련 핀 검토.
- 11:48:49: 검색범위 JSON과 선정근거 해시/Git blob 대조 저장.
- 최종 자체검사 시각은 아래 자동 부록 및 `extracts/SYS-LEGACY/self-check.json`에 실제 실행 시각으로 기록한다. 대기/추정 시간을 실행 시간으로 기록하지 않는다.

## 선정 원본 SHA256·고정 Git blob 전체 목록

원본 경로는 고정 커밋의 저장소 상대경로다. 모든 행 content_equal=true를 실제 바이트 비교했다. SHA는 파일 동일성 근거이며 의미 전수 검증이 아니다.

|원본 경로|SHA256|Git blob|내용 일치|
|---|---|---|---|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|True|
|`all-in-one/sources/block_summary.json`|`68253f9366908244a27ed461c66d465da7ec1723571f27deaa9a6f81a542de63`|`15b570a011645023dbfca2d5332a9e0ae3b0a7b6`|True|
|`all-in-one/sources/can-decoating-page-text.json`|`d3b4c14945dd00f79c58ebab0cb8991c422dd1670e95e24d10779bd9e9d99bba`|`2bebec2c719fa57ed6c9f8d4e541e8848dc0d732`|True|
|`all-in-one/sources/decoded-original/0180-FlgNet.xml`|`b3141dffaf1a7d0583e3d03ab5bf3b8dcab62e42f3722c45ce0a9d3f8b608e58`|`ee118b4076a8938b74b246c5e99ede30b390d55f`|True|
|`all-in-one/sources/decoded-original/0243-FlgNet.xml`|`4b3a77029b4d5901ff40f260d54189748e7697bb6077fca502165fa7cd5ea3b5`|`53fff711852ac7ea3150a4cb51d83813d640210d`|True|
|`all-in-one/sources/decoded-original/0244-FlgNet.xml`|`6df4651ea703181e0355fd70339bc3854bd5ef79826eaf3738c6d0acf1d0488f`|`b12ba7415747e8a863ec295908e544665339a917`|True|
|`all-in-one/sources/decoded-original/0253-FlgNet.xml`|`2d35470eb44fff79916b93fcf57a597b2b9a03211e8493c2283706dc2c875154`|`6d5dc12df96c7fc47ad7f25eba6ba9a55a6755d0`|True|
|`all-in-one/sources/decoded-original/0275-FlgNet.xml`|`93aa2434583d4cf44f3b69f03db5717f38ac1da8f07b9e4b166c56daca8c3b74`|`fb7ed55da991d0a13c4b19bd75bea5f40cfb4683`|True|
|`all-in-one/sources/decoded-original/0465-FlgNet.xml`|`6f48f2b9fc031e4dcef47cff8c9b56e2fbe67fd1802aac999b95836dd9a7458a`|`36eca861d9668e52c667e4b1a0e3dc552a3310dd`|True|
|`all-in-one/sources/decoded-original/0466-FlgNet.xml`|`4e4461435e68831cab0be6171c58c8f25803a5f3da811001a73ae0bd3fe43e61`|`742543974e8feb350ce0432acd5c09435f02367f`|True|
|`all-in-one/sources/decoded-original/0577-IdentXmlPart.xml`|`511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47`|`a505ebf7efd05a85850dc29559a4f71242bacae3`|True|
|`all-in-one/sources/decoded-original/0582-IdentXmlPart.xml`|`41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951`|`82636dec064876d0f4cc714ef385b07d6e05efe0`|True|
|`all-in-one/sources/decoded-original/0583-IdentXmlPart.xml`|`0a34a2b7ad17eba6198dbe53d5c6aa8e87710c7436b832b9d39a075074ab58a8`|`63a23c921a53805f135a0399ba076265907d0eda`|True|
|`all-in-one/sources/decoded-original/0584-IdentXmlPart.xml`|`3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d`|`0f8dde829be66041bea79e40ccc4586d84ff1da7`|True|
|`all-in-one/sources/decoded-original/0585-IdentXmlPart.xml`|`e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184`|`16574d37ef3ca61b59ba396c400e269ab1dd3440`|True|
|`all-in-one/sources/decoded-original/0586-IdentXmlPart.xml`|`f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250`|`266989c590cf52f82e1553f8626a209b8c0b6e0b`|True|
|`all-in-one/sources/decoded-original/0602-IdentXmlPart.xml`|`46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf`|`bcb12ab1ce8c476ff921baa1608f29d9822f76b4`|True|
|`all-in-one/sources/decoded-original/0603-IdentXmlPart.xml`|`e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8`|`3a92b304baf4dbf6147e944d9778d2da11285cb1`|True|
|`all-in-one/sources/decoded-original/0604-IdentXmlPart.xml`|`b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af`|`bb2c318788b97e7a4924a176275c12d805aa519d`|True|
|`all-in-one/sources/decoded-original/0605-IdentXmlPart.xml`|`0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b`|`30e199288c147aa22d5ce8407178a391b89c6b1b`|True|
|`all-in-one/sources/decoded-original/0606-IdentXmlPart.xml`|`73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740`|`ced032fa747a8544abf17058ee5ebaa78ba9b23b`|True|
|`all-in-one/sources/decoded-original/0642-IdentXmlPart.xml`|`c922483c261c8ddb98c239a7b4dc3d7f73f9a45261dd5b4d669f39d6918a1c21`|`398f73b99c4a792a68387485fcb47048d166b2a1`|True|
|`all-in-one/sources/decoded-original/0660-IdentXmlPart.xml`|`0bf4f4c46531f55324602f4f7b1a1e0b9e63df2c6278126f6e5cf1bc9a06509f`|`915de9b3f968310c45682bef86a91adc1fa06e75`|True|
|`all-in-one/sources/decoded-original/0661-IdentXmlPart.xml`|`90672199fee355011f581d3287046894772f3f3b4cb78bbe0dd0d71bd488ac93`|`cea3653088f8fb5c77afcf715988039cb63e28ac`|True|
|`all-in-one/sources/decoded-original/0662-IdentXmlPart.xml`|`1838040bfee800fdb3f13b126eaf69a9d178b17cecc0d59ae03e9185216a48a5`|`ba624f3460dc05e8ade4956cdfc2ec621edb4f73`|True|
|`all-in-one/sources/decoded-original/0664-IdentXmlPart.xml`|`68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed`|`7ce2f1315d5a21d6b77869a59fc9fcb2f17e90e6`|True|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|True|
|`all-in-one/sources/electrical-page-text.json`|`4b846819aab7e1306aebea617042f9f9ffe0c8aee1930e6f3db035bea3739153`|`1f48073c07b28e668d3d72d5ce49db263a5214e6`|True|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|True|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|True|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|True|

## 최종 자체 검사

- 실제 시각: 2026-10-11T11:52:51.555742+00:00
- 결과: passed; 선정 31 SHA/Git blob 일치, 공통 보존목록712파일·중지5 해시 재대조 일치, 고정원본 Git clean.
- 구조 단언: OFF공통 직렬, S/R Part, FR01/VT01 출력 Wire, KF_KT ENO Wire 통과. 생성기·PLC 행동 시험이 아닌 문서 정적 검사다.
- 원본 PDF3쪽 시각검토,7개 대표 FlgNet 핀검토. XML695파일 검색을695개 의미검증으로 집계하지 않는다.
- 독립 검토는 부모/통합자 대기. UI/기록·게시·TIA/현재CPU·현장 복구 완료는 주장하지 않는다.
