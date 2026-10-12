# SYS-RUNHOURS 자체 원본 조사 초안

## 핵심 확인·상충·누락·공유근거

- 한 catalog ID SYS-RUNHOURS만 조사했다. 모터별 운전시간 입력을 참조하지만 해당 모터·팬·CLIENT 장치의 별도 조사완료로 합산하지 않는다.
- **HOUR는 평생 누적시간이 아니다.** 대표 BC01의 MIN은 Int Add 1이고, MIN ≥ 60에서 HOUR에 Int **1을 Move**, MIN에 0을 Move한 다음 공통 갱신 비트를 Set한다. 40개 계수 채널의 원본 구조 추출에서도 같은 HOUR Move 1을 확인했다. 별도 T17 조건의 HOUR 0 쓰기와 함께 해석해야 한다.
- **호출과 분 타이머를 구분한다.** FC2 `time work motor`는 Main의 ON 허가 호출이다. `cyc_int2 ogni 1s`와 묶인 파생 목록만 보고 1초 OB에서 직접 호출한다고 단정하지 않는다. 블록 말미 T13에 S5T#1M을 넣는 자기반전 SdCoil이 있으며, 실제 CPU 호출주기·한 분 정확도·운전시간 정합성은 확인하지 않았다.
- **정비기록 저장 완료는 미확정이다.** M1.7 Flag_Aggiorna_DB를 Set하는 PLC 경로는 확인했으나, 이를 지우는 외부 기록자/수신 ACK는 확보하지 못했다. `reset working hours after recording the data in the db`라는 제목은 저장 성공 증거가 아니다. M2.0 기억, M1.7 반전, T17 S5T#5S를 거쳐 HOUR 필드를 0으로 쓰는 경로를 분리했다.
- **정비기한과 시간계수는 별개다.** Main의 Maint_code 값 전달, 날짜 비교 색인 및 MAINTENANCE_PERIOD_LIMIT Reset은 DB9 계수 경로와 직접 결속되지 않았다. 날짜 상수를 실제 정비기한·서비스 만료일·교체일로 해석하지 않는다. CPU 시계 변경이나 코드/보호값 변경을 제안하지 않는다.
- **HMI 누락:** 782행 CSV에 DB9 주소 또는 해당 시간/갱신 태그의 직접 대응이 없다. `AbilitaMaintenance`는 운전모드 관련 DB2.X7.5이며 운전시간 Reset 버튼으로 치환할 수 없다. 실제 화면/스크립트/외부 누적 DB/정비 이력은 미확보다.
- 공유근거: [SYS-AUTO](SYS-AUTO-DOTS-DRAFT.md)의 유지보수 모드·Main 코드 전달 및 [SYS-COUNTERS](SYS-COUNTERS-DOTS-DRAFT.md)의 호출주기/생산·가스 계수 구분을 같은 고정입력의 공통 근거로 재사용한다. [LD01](LD01-DOTS-DRAFT.md), [MC04](MC04-DOTS-DRAFT.md), [VS01](VS01-DOTS-DRAFT.md) 등의 개별 회로·시간 설명을 색인으로 사용하되, 이번 고유 핵심은 FC2 호출·T13·DB9 Move1/0·M1.7 핸드셰이크를 독립 원본 대조했다. 없는 실물자료를 반복 조사하지 않았다.

## 1. 설비·자료 기준 — 적용

- catalog index44, equipment index245, software/공통 시스템, phase2, 부모 없음. 별칭 `hours motors`, `hours_motor`. `INVENTORY.json` 및 배치12/중복검토의 SYS-RUNHOURS 행을 확인했다.
- 고정 읽기전용 원본: `gme-research/source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 최근 게시판/로컬 최신 기능의 검증이 아니다.
- 축약: `NNNN-FlgNet.xml`, `NNNN-IdentXmlPart.xml`은 모두 `all-in-one/sources/decoded-original/` 아래다. doc는 백업 색인 문서번호이며 XML 네자리·NID와 다르다. RID/UID는 파일 및 블록 문맥 안에서 해석한다. AO/BO는 비트 오프셋, TOD N은 DB/FC 번호다.
- GME-STD-1.0.0의 7영역 적용. 모델 런타임/추론수준 증명은 미확인. 현재 CPU/TIA/현장/실제 누적시간은 미취득이다. 이번 작업은 문서·XML 정적 추출이며 원본 build/test/generator, 시뮬레이터, PLC, 현장, 보호값, SEJIN 변경·실행은 없다.

## 2. I/O·HMI — 적용, 화면 이벤트·실물 대응은 근거 미확보

### 2.1 핵심 선언

|대상|원본 선언·형식|주소·의미 경계|
|---|---|---|
|time work motor|0688 FCBlock RID82, TOD N2, NID7 UID347 Call|FC2, Global; 0549 CRef334/CodeBlock347로 호출|
|hours motors|0614 DepDBBlock RID5, TOD N9, 크기1520bit|DB9, Global; HOUR/MIN은 Int 16bit, 화면·영구저장 DB로 단정 불가|
|Tag_47|0613 RID1, Timer AO13|T13; 물리 입력 또는 HMI Bool이 아님|
|Tag_48|0613 RID284, Timer AO17|T17; 시간계수 HOUR 초기화 조건|
|Flag_Aggiorna_DB|0613 RID13, Bool Memory AO15|M1.7; 공통 갱신요청 Set, 외부 ACK writer 미확보|
|MEM2_0|0613 RID332, Bool Memory AO16|M2.0; 갱신 요청 기억 Set/Reset|
|ON|0613 RID331 / 0692 RID52, Bool Memory AO0|M0.0; 이름만으로 항상 True 가정 금지|
|BC01_Fbk|0613 RID122, Bool Input AO0, SAM=None|I0.0 입력영상; 실제 회전·전력사용·운전시간 증거와 구분|
|BC_01_MIN/HOUR|0615 RID124/126, Int AO608/624|DB9.DBW76/78, 각각 Add/Move0 및 Move1/Move0 여러 쓰기|
|Maint_code_0/1/3|0690 RID103/108/106, Int AO2288/2304/2320; 0689 Data TOD1|DB1.DBW286/288/290; 운전시간 DB9와 별도|
|Tag_189/190|0692 RID104/107, Word AO640/656|MW80/82, Int 설정값을 Word 전달하는 별도 경로|
|MAINTENANCE_PERIOD_LIMIT|0690 RID113 Bool AO62; 0689 Allarm TOD3|DB3.DBX7.6, 날짜 관련 Set·Reset; 시간계수 전용 고장으로 병합 금지|
|RESET_ALLARM|0690 RID115 Bool AO48; 0689 Flag TOD2|DB2.DBX6.0, 내부 리셋이며 HMI 직접 요청과 구분|

### 2.2 HMI 검색 범위와 부재

`all-in-one/sources/hmi_plc_tags.csv`의 782 데이터행에서 설정 주소의 정확한 `DB9,` 접두어와 이름 `hours motors`, `hours_motor`, `Flag_Aggiorna_DB`, `Tag_47`, `Tag_48`, `MEM2_0`를 대조했다. 직접 대응은 0건이다. 따라서 DB9의 미확보 화면을 임의 설계된 기존 HMI 화면이라고 쓰지 않는다. HMI CSV는 주소설정 색인으로 버튼 누름/해제/주기 스크립트·쓰기권한·통신 성공을 증명하지 않는다.

CSV 실제행73 `AbilitaMaintenance`, ID00409, `DB2,X7.5`는 확인된다. 이것은 [SYS-AUTO](SYS-AUTO-DOTS-DRAFT.md)의 유지보수 모드 근거이며 DB9 Reset·정비 완료 ACK·정비기한 해제의 승인 버튼이라는 근거는 없다. `hmi-windows.csv`에서도 시간계수 전용 화면/이벤트를 결속하지 못했다. 현 HMI 프로젝터/외부 데이터 수집 스크립트/태그 통신 맵/실제 화면 캡처가 필요하다.

## 3. 제어 구조 — 적용

### 3.1 호출: 0549 / doc1620 / Main NID7

Powerrail W352→Contact350, ORef335/RID52(0692 ON M0.0)→operand W348. Contact350.out W351는 CRef319·322·325·328·331·334의 en으로 **병렬 분기**한다. CRef334 RefId83 안 CodeBlock347 RefId82가 0688 FC2 선언의 NID7 UID347 Call 및 0694 BlockInterfaceInfo RID83/NID7 UID334와 결속된다. 앞 블록 ENO를 직렬로 통과해야 FC2가 실행되는 구조가 아니다. 다른 NID8의 UID347은 다른 문맥이므로 혼동하지 않는다.

Main은 block_summary의 Event class `program cycle`, Constant name `ob_main`으로 색인된다. 이는 FC2 직접 호출 근거이며 CPU 스캔시간, 인터럽트 우선순위, 온라인 OB 설정 확인이 아니다. SYS-COUNTERS의 1s/1ms 상충을 FC2의 주기로 그대로 복제하지 않는다.

### 3.2 분 간격 후보: 0019 / doc1056 / FC2 NID58

Contact3120은 operand 반전이다. ORef3115/RID1 T13→W3118→Contact3120. Powerrail W3122, Contact3120.out W3121→SdCoil3112.in. ORef3114/RID335→W3117→value이며 0616 literal S5Time `S5T#1M`(V5632)이다. operand W3119/ORef3116도 동일 T13이다.

따라서 `NOT T13 → SD T13(S5T#1M)`의 자기 재허가 구조를 확인한다. FC2의 앞 계수 네트워크는 T13 접점으로 허가되며 끝 NID58이 이 타이머를 다룬다. PBox가 각 계수 네트워크에 있는 것이 아니며, CPU 스캔/호출 중단·재시작·Timer 구현·retention에 따라 실제 샘플링 경계가 달라질 수 있다. 이 정적 문서만으로 정확히 60초마다 단 한 번 누적됨을 시험했다거나 실제 1시간을 계측했다고 하지 않는다.

### 3.3 대표 MIN/HOUR: 0308 / doc1018 / BC01 NID20

- 0613 RID1 T13 UID1125→W1137→Contact1154. RID122 BC01_Fbk UID1126→W1138→Contact1156. 두 Contact는 W1155로 직렬이며 W1157이 Add1108.en과 Ge1115.pre에 분기한다.
- Add1108 SrcType=Int, W1139/ORef1127/RID124(DB9.DBW76)→in1, W1140/ORef1128/RID7(Int1)→in2, W1141→ORef1129/RID124에 MIN을 쓴다.
- Ge1115 SrcType=Int, W1142/ORef1130=동일 MIN, W1143/ORef1131/RID8=Int60. Ge.out W1144→Move1118.en.
- Move1118.in W1146/ORef1132/RID7=Int1, out1 W1147/ORef1133/RID126=DB9.DBW78 HOUR. **HOUR+1 Add가 아니다.**
- Move1118.eno W1148→Move1121.en, in W1149/ORef1134/RID12=Int0, out1 W1150/ORef1135/RID124=MIN. 이어 eno W1151→SCoil1124.in, operand W1152/ORef1136/RID13=M1.7.

MIN 읽기·쓰기·비교는 같은 네트워크에 존재한다. 연결·ENO 체인을 확인했지만 CPU에서 연산과 비교의 런타임 순서·오버플로·실행 성공을 관찰하지 않았다. 장기시간 저장은 이 HOUR를 소비하는 외부 경로가 별도로 있어야 확인할 수 있으며 현재 확보하지 못했다.

### 3.4 HOUR 초기화와 핸드셰이크

0332~0340 및0018은 46개 HOUR 필드에 Int0을 쓰는 10개 네트워크다. 계수 채널은 40개지만 Reset 필드는 46개다. 이는 실제 모터46개 또는 완료46개를 뜻하지 않는다.

대표0332/doc1045/NID47: T17 ORef2589/RID284→W2600→Contact2615, out W2616→Move2574.en. Int0 ORef2590/RID12→W2601, out1 W2602→ORef2591/RID10 CLIENT_MOTOR_1_HOUR. Move2574.eno W2603→Move2577.en 이후 Move2580/2583/2586로 ENO 연쇄하여 CLIENT1~5의 HOUR를 지운다. 첫 Move와 후속 ENO 의존을 구분한다. 0018/doc1054/NID56의 FN05_HOUR는 Contact3085(T17)→W3086→Move3076, in W3083/ORef3080/RID12=0, out W3084/ORef3081/RID282=FN05_HOUR다. 파생 network-map의 이 literal은 누락되어 있으나 원본 RID12 선언으로 보완했다.

0341/doc1055/NID57:
1. ON Contact3147(ORef3124/W3133)→W3148이 두 가지로 분기한다.
2. Flag_Aggiorna_DB Contact3149(ORef3125/W3134)→W3150→SCoil3110; W3136/ORef3126/RID332에 M2.0을 Set한다.
3. M2.0 Contact3151(ORef3127/W3137)→W3152는 NOT Flag_Aggiorna_DB Contact3153와 T17 Contact3155에 분기한다.
4. Contact3153.out W3154→SdCoil3118.in, value W3138/ORef3128/RID334=`S5T#5S`, operand W3141/ORef3130/RID284=T17.
5. Contact3155.out W3156→RCoil3123.in, operand W3144/ORef3132=M2.0을 Reset한다.

즉 ON·갱신요청을 기억한 후 요청이 내려간 상태에서 5초 타이머를 다루며, 그 타이머는 앞 HOUR 0쓰기와 M2.0 Reset 조건에 사용된다. **M1.7을 0으로 쓰는 RCoil은 이 네트워크에 없다.** 모든 IdentXmlPart의 이름 검색에서 Flag_Aggiorna_DB는0613에만 있고 해당 참조는 40 SCoil Write와 NID57 읽기2개다. 이 검색은 외부 HMI/DB/Word·간접 주소 writer가 없다는 증명이 아니다. 비트 이름만으로 전체 writer 폐쇄를 선언하지 않는다.

### 3.5 별도 정비값·날짜·알람 경계

0550/doc1624/Main NID11: ON Contact419.out W420이 Move400/405.en으로 병렬 분기한다. Move400은 W414/ORef409 Data.Maint_code_0(DB1.DBW286 Int)→W415/ORef410 Tag_189(MW80 Word). Move405는 W416/ORef411 Maint_code_3(DB1.DBW290 Int)→W417/ORef412 MW82 Word. Word 전송이며 DB9 시간 누적, 정비 이력 저장, 정비 완료 동작으로 해석하지 않는다. 코드 생성·외부 writer·현재 코드값은 미확보다.

백업 `live_index.json` segment `_7ev` doc1625의 원형 없는 STL 검색문은 Maint_code_1과 상수16972 비교 후 JC M001, RD_SYS_T 및 T_CONV, TodayDate와 `D#2026-01-01` 비교, MAINTENANCE_PERIOD_LIMIT Set를 포함한다. 0690 NID12 RID108 UID396, RID113 UID424(Write), 0691 Local ReadClkRetValue Int RID96·TodayDateTime Date_And_Time RID97·TodayDate Date RID100, 0693 RD_SYS_T RID95와 T_CONV RID116 선언이 해당 문맥을 뒷받침한다. 0071 literal RID109/NID12 UID399는 16972를 DInt로 선언하고, RID141/NID12 UID26는 날짜를 Date로 선언한다. 색인의 ==i/≥i와 실제 선언 형식의 차이는 컴파일·변환 확인이 필요한 경계다. 단일 평탄 문자열은 원형 STL 줄바꿈·분기·컴파일 전체 동작을 대신하지 않으므로 부분 해석이다. 상수16972나 날짜를 서비스 인증·실제 만료/교체기한으로 이름 붙이지 않는다.

0034/doc1623/NID10은 OFF(M0.1) Contact395.out W396이 RD_SYS_T LRef376 및 T_CONV LRef381.en에 병렬 연결된다. W390 RET_VAL→Local RID96, W391 OUT→RID97, W392 RID97→IN, W393 OUT→RID100. RD_SYS_T는 읽기, T_CONV는 변환 선언이며 시계 조정으로 표현하지 않는다. 이 Local 변수는 NID12에서도 쓰이므로 별도의 HMI/DB 날짜 필드로 합치지 않는다. 실제 CPU 시각·시간대·현재 서비스기한은 미확인이다.

### 3.6 채널 범위·빠진 계수와 남아 있는 Reset

40개 계수 XML의 Part/Wire/선언 결속을 구조 추출한 목록은 부록A다. 대표 BC01, 첫 CLIENT, FN04의 선언 차이, 마지막 FN05 및 Reset/타이머를 직접 의미 검토했다. 구조 추출 40건을 40개 모터의 실물 의미·전기·정상극성까지 전수 검토한 것으로 표시하지 않는다.

52개 FC2 XML에는 NID1~10,13~17,19~24,26,28~35,37~46의 40개 계수, NID47~56의10개 Reset, NID57·58이 있다. client11/12/18은 이번 살아 있는 계수 XML에 없고 Reset 대상만 남아 있다. block_summary/live_index는 doc1023 `mc-05 deleted`, doc1025 `sc-12 deleted`, doc1034 `fn-01 fan deleted`의 제목을 보존하며 계수 코드가 없다. 이 항목들을 새 계수나 실제 현장 설비로 부활시키지 않는다. SC12 기존 제외는 유지한다. MC03 계수의 실제 입력 선언은 `102A7_SPARE5` I0.5로, 제목 mc-03만으로 실물 RUN을 확정하지 않는다.

## 4. 전기 전달 경로 — 기능 자체 비해당, 입력 실물 대응은 근거 미확보

SYS-RUNHOURS는 software이며 전원/접점/단자/케이블이 독립 배정된 물리장치가 아니다. 대장 electrical_fgs는 빈 목록이다. FC2가 읽는 각 모터 Fbk/Input는 해당 설비 회로 소유이며 이 기능의 전용 회로로 복제하지 않는다.

이번 조사에서는 PDF 렌더 0쪽이다. 새로운 독립 전기 주장을 하지 않아 고정 원본의 기존 모터 초안 회로 연결을 참고로 유지했다. 실제 FC2 입력이 해당 모터 회전을 대표하는지 확정하려면 각 모터의 승인도면 FG, **실제 PDF 페이지**, 개정란, 피드백 접점-단자-케이블-PLC 채널 양 끝점을 기존 설비별 자료와 현장 사진으로 맞춰야 한다. MC03/SPARE5 및 CLIENT11/12/18·삭제 후보는 특히 신규 결속 자료가 필요하다. 임의로 FG=PDF−1을 적용하지 않는다. 신규 PDF 필요범위는 입력 대응이 쟁점이 되는 해당 모터 페이지이며 전체 전기도를 반복 검토하지 않는다.

## 5. 알람·복구 — 적용 일부, 현장 복구 근거 미확보

- FC2에는 분 계수, HOUR 이벤트값, 갱신요청, Reset 핸드셰이크가 있으며 자체 시간계수 고장/정비완료 경보를 확인하지 못했다. 이를 타 모터 고장 경보에 덧붙이지 않는다.
- 0551/doc1626/NID13: ON Contact451→W452→RESET_ALLARM Contact453→W454→MAINTENANCE_PERIOD_LIMIT Contact455→W456→RCoil441. operand W450/ORef445는 같은 Allarm bit다. 선언0690 RID113는 NID12 Set Write UID424와 NID13 Reset UID445를 함께 보존한다.
- 알람 Reset, DB9 HOUR 0쓰기, M2.0 Reset, MIN 0쓰기는 서로 다른 대상과 조건이다. 어느 것도 정비 작업 완료·부품교체 완료·실제 데이터 기록 성공·재기동 안전의 증거가 아니다.
- 기존 SYS-AUTO/ALARM의 공통 RESET 발생·전달 및 표시 근거를 연결재사용한다. 현장조작 순서, 타이머 강제완료, M1.7 강제0, 날짜/유지보수 코드 변경 방법은 제공하지 않는다.

## 6. 증상별 관찰 — 적용, 조치·복구는 미수행

|증상|읽기 전용 관찰 항목|원본 비교·구분|필요 증거/판정 보류|
|---|---|---|---|
|운전 중 MIN 불변|관찰시각/시간대, FC2 호출허가 ON, T13, 해당 원시 Fbk, DB9 MIN|0549 호출과0019 타이머, 개별 계수 en/pre|현재 프로젝트·CPU 읽기자료 및 입력 실물 대응; 모터 고장으로 단정 금지|
|HOUR가 0 또는1만 보임|해당 HOUR/MIN 전후, M1.7/M2.0/T17, 외부기록 시각|Move1/Move0 구조와 외부 장기 누적값 구분|외부 소비자·저장 내역·ACK 원문 없으면 손실/정상 단정 불가|
|HOUR 초기화 안 됨|M1.7이 내려갔는지, M2.0·T17·ON의 동시점|0341의 NOT 갱신요청과 T17 허가|외부 writer/통신 결과 필요; 강제 Reset 금지|
|여러 모터 HOUR가 함께 0|Reset 대상·T17·ENO 체인·관찰시각|공통 T17 46필드 쓰기와 개별 motor fault 분리|기록 성공/누락 여부는 외부저장 증거로 판단|
|시간이 실운전과 다름|피드백 종류, 호출중단 구간, 정전/재시작, 원시값·계수값 동시 기록|샘플링/retention 미확정, HOUR는 영구 총시간 아님|현행 TIA 설정·변경이력·수집기 DB 스키마 필요|
|정비기한 알람 재발|내부 Reset, alarm bit, 코드/날짜 읽기자료의 출처와 시각|Main NID12/13 복수쓰기, DB9와 별개|원형 STL·승인 정비정책·이력 필요; 날짜조정/코드변경으로 해결 판단 금지|

관찰 양식에는 관찰자, 시각/시간대, 프로젝트/CPU 근거, 위치·주소, 값·단위, 수집방법, 비교원본, 배제한 원인과 미배제 원인을 남긴다. 실제 정비/운전/교체 기록은 이번 문서에서 생성하거나 공개 저장소에 복사하지 않았다.

## 7. 완료·누락 — 적용

|7영역|상태|한계|
|---|---|---|
|설비·자료 기준|적용|고정 백업/대장 한 ID, 실물 동일성 미확인|
|I/O·HMI|적용·근거 미확보|선언/주소 확인, DB9 HMI·이벤트·외부수집 미확보|
|제어 구조|적용|52 FC2 XML 구조 추출·대표 핵심 의미 대조, 런타임 미시험|
|전기 전달 경로|기능 자체 비해당·입력 대응 미확보|전용 FG 없음, 개별 모터 회로 소유 유지|
|알람·복구|일부 적용·미확보|Main 날짜 경보는 별도, 현장 복구 근거 없음|
|증상 관찰|적용|읽기 전용 수집계획이며 실제 조치/시험 아님|
|완료 기준|적용|문서와 현재 CPU·게시·현장 분리|

|네 기능|적용·검증|
|---|---|
|도면·래더 비교|FC2 핵심과 모터별 회로 참조의 비교는 적용 가능; 신규 UI 기능 검증 없음|
|백업·선택복원|관찰기록 보존 요구 적용; 이 기능의 저장/재읽기/복원 실행 없음|
|기록 전후 비교|M1.7·T13/T17·DB9·외부누적의 동시점 구분 필요; 실제 기록 미취득|
|보고서/PDF|이 Markdown 초안만 작성, PDF 렌더/화면 검증 미수행|

- documentation: complete_with_gaps (7영역 자체 문서 초안).
- static_review: scoped_complete (원본 핵심 핀 대조, 구조 추출·해시 확인; 독립 2차 검토는 부모).
- ui_records: not_run. publication: not_published. tia_compile/live_cpu/field_recovery: not_performed.
- 다음 한 작업: 부모의 독립 원본 검토 후 초안 전달. 이후 새 자료가 생기면 외부 기록자 M1.7 ACK·DB9 소비/영구누적 경로와 현행 retention/주기를 확인한다. 자료가 없는 상태에서 실제시간·교체일·정비기한을 보충 추정하지 않는다.

### 실제 조사·검사 시각과 범위

착수 2026-10-11 11:56:54 UTC. 지시/대장/기준 읽기 11:56~11:57 UTC, 핵심 FC2·선언·호출/정비경계 대조 11:57~11:59 UTC, 자체 구조추출 및 고정 Gitblob 일치검사 12:00:16 UTC에 완료했다. 최종 자체검사 시각과 명령 결과는 아래 부록C 및 extracts의 self-check.json에 별도로 기록한다. 과거 작업기간이나 현장 관찰시각으로 재사용하지 않는다.

해시 검사는 선정75파일의 byte 동일성이다. 75개 파일 전체의 모든 의미·도면·HMI 동작을 검토했다는 주장이 아니다. 고유 FC2 구조추출52 XML, Main 고유 대조4 XML, 직접 핵심 의미 검토는 호출0549, 타이머0019, 계수0308와 대표 구조/선언 차이, Reset0332/0018, 핸드셰이크0341, 유지보수0550/0551/0034 및 doc1625 제한적 색인 분석이다. 원본 실행기·시험기·시뮬레이터는 실행하지 않았다.

## 부록A. 계수 채널 정적 결속 전체 목록

0613 입력/0615 DB9 선언과 실제 XML Part/Wire를 결속한 구조추출표다. MIN/HOUR는 Int, HOUR Move 입력은 모든 행에서0616 RID7=1이다. 개별 모터 실물확인·회로/알람 완료 목록이 아니다.

|XML / doc / NID|허가 입력(0613 RID, 주소)|MIN / HOUR (0615 RID, 주소)|Add / HOUR Move / in·out Wire|
|---|---|---|---|
|0292-FlgNet.xml / 1002 / 1|APRON CONVEYOR A RUN RID2 I12.3|CLIENT_MOTOR_1_MIN RID6 DB9.DBW0 / RID10 DB9.DBW2|82 / 92 / W120·W121|
|0293-FlgNet.xml / 1003 / 2|IMPACTOR RUN RID14 I12.4|CLIENT_MOTOR_2_MIN RID16 DB9.DBW4 / RID18 DB9.DBW6|136 / 146 / W174·W175|
|0294-FlgNet.xml / 1004 / 3|IMPACT VIBRATIONFEEDER RUN RID20 I12.5|CLIENT_MOTOR_3_MIN RID22 DB9.DBW8 / RID24 DB9.DBW10|190 / 200 / W228·W229|
|0295-FlgNet.xml / 1005 / 4|BELT CONVEYOR A RUN RID26 I12.6|CLIENT_MOTOR_4_MIN RID28 DB9.DBW12 / RID30 DB9.DBW14|244 / 254 / W282·W283|
|0296-FlgNet.xml / 1006 / 5|AIR KNIFE RUN RID32 I12.7|CLIENT_MOTOR_5_MIN RID34 DB9.DBW16 / RID36 DB9.DBW18|298 / 308 / W336·W337|
|0297-FlgNet.xml / 1007 / 6|BELT CONVEYOR B RUN RID38 I13.0|CLIENT_MOTOR_6_MIN RID40 DB9.DBW20 / RID42 DB9.DBW22|352 / 362 / W390·W391|
|0298-FlgNet.xml / 1008 / 7|SHREDDER 1 RUN RID44 I13.1|CLIENT_MOTOR_7_MIN RID46 DB9.DBW24 / RID48 DB9.DBW26|406 / 416 / W444·W445|
|0299-FlgNet.xml / 1009 / 8|SHREDDER VIBRATIONFEEDER RUN RID50 I13.2|CLIENT_MOTOR_8_MIN RID52 DB9.DBW28 / RID54 DB9.DBW30|460 / 470 / W498·W499|
|0300-FlgNet.xml / 1010 / 9|BELT CONVEYOR  C RUN RID56 I13.3|CLIENT_MOTOR_9_MIN RID58 DB9.DBW32 / RID60 DB9.DBW34|514 / 524 / W552·W553|
|0301-FlgNet.xml / 1011 / 10|ROTEX SCREEN RUN RID62 I13.4|CLIENT_MOTOR_10_MIN RID64 DB9.DBW36 / RID66 DB9.DBW38|568 / 578 / W606·W607|
|0302-FlgNet.xml / 1012 / 13|APRON CONVEYOR B RUN RID80 I13.5|CLIENT_MOTOR_13_MIN RID82 DB9.DBW48 / RID84 DB9.DBW50|730 / 740 / W768·W769|
|0303-FlgNet.xml / 1013 / 14|SHREDDER 2 RUN RID86 I13.6|CLIENT_MOTOR_14_MIN RID88 DB9.DBW52 / RID90 DB9.DBW54|784 / 794 / W822·W823|
|0304-FlgNet.xml / 1014 / 15|BELT CONVEYOR  D RUN RID92 I13.7|CLIENT_MOTOR_15_MIN RID94 DB9.DBW56 / RID96 DB9.DBW58|838 / 848 / W876·W877|
|0305-FlgNet.xml / 1015 / 16|BELT CONVEYOR E RUN RID98 I14.0|CLIENT_MOTOR_16_MIN RID100 DB9.DBW60 / RID102 DB9.DBW62|892 / 902 / W930·W931|
|0306-FlgNet.xml / 1016 / 17|LIW SYSTEMAUTOREADER RID104 I14.1|CLIENT_MOTOR_17_MIN RID106 DB9.DBW64 / RID108 DB9.DBW66|946 / 956 / W984·W985|
|0307-FlgNet.xml / 1017 / 19|PRIMARYSHREDDER RUN RID116 I14.2|CLIENT_MOTOR_19_MIN RID118 DB9.DBW72 / RID120 DB9.DBW74|1054 / 1064 / W1092·W1093|
|0308-FlgNet.xml / 1018 / 20|BC01_Fbk RID122 I0.0|BC_01_MIN RID124 DB9.DBW76 / RID126 DB9.DBW78|1108 / 1118 / W1146·W1147|
|0309-FlgNet.xml / 1019 / 21|RD01_Fbk RID128 I0.2|RD_01_MIN RID130 DB9.DBW80 / RID132 DB9.DBW82|1162 / 1172 / W1200·W1201|
|0310-FlgNet.xml / 1020 / 22|RD01F_Fbk RID134 I0.4|RD_01_FAN_MIN RID136 DB9.DBW84 / RID138 DB9.DBW86|1216 / 1226 / W1254·W1255|
|0311-FlgNet.xml / 1021 / 23|102A7_SPARE5 RID140 I0.5|MC_03_MIN RID142 DB9.DBW88 / RID144 DB9.DBW90|1270 / 1280 / W1308·W1309|
|0312-FlgNet.xml / 1022 / 24|MC04_Fbk RID146 I0.6|MC_04_MIN RID148 DB9.DBW92 / RID150 DB9.DBW94|1324 / 1334 / W1362·W1363|
|0313-FlgNet.xml / 1024 / 26|VS01_Fbk RID158 I1.1|VS_01_MIN RID160 DB9.DBW100 / RID162 DB9.DBW102|1432 / 1442 / W1470·W1471|
|0314-FlgNet.xml / 1026 / 28|FN02_Fbk RID170 I3.0|FN_02_MIN RID172 DB9.DBW108 / RID174 DB9.DBW110|1540 / 1550 / W1578·W1579|
|0315-FlgNet.xml / 1027 / 29|VR01_Fbk RID176 I3.4|VR_01_MIN RID178 DB9.DBW112 / RID180 DB9.DBW114|1594 / 1604 / W1632·W1633|
|0316-FlgNet.xml / 1028 / 30|FN01_Fbk RID182 I3.5|FN_01_MIN RID184 DB9.DBW116 / RID186 DB9.DBW118|1648 / 1658 / W1686·W1687|
|0317-FlgNet.xml / 1029 / 31|VR02_Fbk RID188 I3.7|VR_02_MIN RID190 DB9.DBW120 / RID192 DB9.DBW122|1702 / 1712 / W1740·W1741|
|0318-FlgNet.xml / 1030 / 32|CH01_Fbk RID194 I4.0|CH_01_MIN RID196 DB9.DBW124 / RID198 DB9.DBW126|1756 / 1766 / W1794·W1795|
|0319-FlgNet.xml / 1031 / 33|FN03_Fbk RID200 I4.1|FN_03_MIN RID202 DB9.DBW128 / RID204 DB9.DBW130|1810 / 1820 / W1848·W1849|
|0320-FlgNet.xml / 1032 / 34|FN06_Fbk RID206 I4.3|FN_06_MIN RID208 DB9.DBW132 / RID210 DB9.DBW134|1864 / 1874 / W1902·W1903|
|0321-FlgNet.xml / 1033 / 35|SC01_Fbk RID212 I4.4|SC_01_MIN RID214 DB9.DBW136 / RID216 DB9.DBW138|1918 / 1928 / W1956·W1957|
|0322-FlgNet.xml / 1035 / 37|LD-01_Fbk RID224 I4.6|LD_01_MIN RID226 DB9.DBW144 / RID228 DB9.DBW146|2026 / 2036 / W2064·W2065|
|0323-FlgNet.xml / 1036 / 38|LD-01A_Fbk RID230 I4.7|LD_01_VIB_MIN RID232 DB9.DBW148 / RID234 DB9.DBW150|2080 / 2090 / W2118·W2119|
|0324-FlgNet.xml / 1037 / 39|SC-10_Fbk RID236 I5.0|SC_10_MIN RID238 DB9.DBW152 / RID240 DB9.DBW154|2134 / 2144 / W2172·W2173|
|0325-FlgNet.xml / 1038 / 40|SC-11_Fbk RID242 I5.1|SC_11_MIN RID244 DB9.DBW156 / RID246 DB9.DBW158|2188 / 2198 / W2226·W2227|
|0326-FlgNet.xml / 1039 / 41|FN04_Fbk RID336 I28.2|FN_04_MIN RID250 DB9.DBW160 / RID252 DB9.DBW162|2242 / 2252 / W2280·W2281|
|0327-FlgNet.xml / 1040 / 42|VR03_Fbk RID254 I5.4|VR_03_MIN RID256 DB9.DBW164 / RID258 DB9.DBW166|2296 / 2306 / W2334·W2335|
|0328-FlgNet.xml / 1041 / 43|VR04_Fbk RID260 I5.5|VR_04_MIN RID262 DB9.DBW168 / RID264 DB9.DBW170|2350 / 2360 / W2388·W2389|
|0329-FlgNet.xml / 1042 / 44|VR05_Fbk RID266 I5.6|VR_05_MIN RID268 DB9.DBW172 / RID270 DB9.DBW174|2404 / 2414 / W2442·W2443|
|0330-FlgNet.xml / 1043 / 45|VR06_Fbk RID272 I5.7|VR_06_MIN RID274 DB9.DBW176 / RID276 DB9.DBW178|2458 / 2468 / W2496·W2497|
|0331-FlgNet.xml / 1044 / 46|FN05_Fbk RID278 I6.0|FN_05_MIN RID280 DB9.DBW180 / RID282 DB9.DBW182|2512 / 2522 / W2550·W2551|

## 부록B. 선정 원본 SHA256·고정 Gitblob 전체 목록

선정 75파일 전부 고정 커밋 blob byte와 일치. 아래 경로는 source-mv06 기준이다. SHA 검토와 의미 검토는 별개다.

|원본 경로|SHA256|Git blob|일치|
|---|---|---|---|
|VERSION.json|5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7|fffb51663b7705aec91cb119ca80ee943a4ce758|True|
|all-in-one/sources/block_summary.json|68253f9366908244a27ed461c66d465da7ec1723571f27deaa9a6f81a542de63|15b570a011645023dbfca2d5332a9e0ae3b0a7b6|True|
|all-in-one/sources/decoded-original/0018-FlgNet.xml|7dcd2474e1adda43a4ef2fdd089554ed1506c309c1606772f408bbb69c269344|1ebd993e53a19fd6938ce5c8ba8fb06236ff9c4e|True|
|all-in-one/sources/decoded-original/0019-FlgNet.xml|a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5|f78cfdbf5e717304114660ffbd3bb42cbed6d79d|True|
|all-in-one/sources/decoded-original/0034-FlgNet.xml|ca219edf40a94f23d2f6861b42b3a923f4e24d3a9cf06abf4f8b1a75a6b99dd8|f43dec24fcc62dba0fc24ccf674c758a771b31c7|True|
|all-in-one/sources/decoded-original/0071-IdentXmlPart.xml|49d01eba491fe39ed64cb9b15719f3445f49979ddc73753cb398628075b0d6c3|6f3924a0d75ac7ee3820e83d2873109dd1291b33|True|
|all-in-one/sources/decoded-original/0292-FlgNet.xml|dd1db2302f796dcd00d675f904dc2b23418dcba0530367ef23d343828a1f07fc|c8d9f9026125be35f0a3b92547e82316c848321e|True|
|all-in-one/sources/decoded-original/0293-FlgNet.xml|e63ffe5d62c91b8d9c664fc9935f4f8144f68d598f643e7d00d4127da8f00500|37cd6c09f676682b2ad7589f828d0af8e3c7039e|True|
|all-in-one/sources/decoded-original/0294-FlgNet.xml|f18d17accd996e443a738b8bb23065f328b0a5548a561f5402178533b583d53b|6aae006614d815a4e332717e2b3d55db64a9b0a3|True|
|all-in-one/sources/decoded-original/0295-FlgNet.xml|db68ca1f7e56b71860458ebc5f257a2956933f239736ed3bf31e7b74520918f9|3694d5caf61f77aea3d57f275f89340a1d63248b|True|
|all-in-one/sources/decoded-original/0296-FlgNet.xml|8326d0a6474b89cf31127b1e3cf907b4b1e92cfb76d781045cbadfaaab6ac964|6895ea3252d40326d266003b954529b286005221|True|
|all-in-one/sources/decoded-original/0297-FlgNet.xml|cda29a4baea32238fc7023eda23d278b383078775a63129bd96c528f197676fc|6379510e517f6fe91083a879fcbbf34e757dac11|True|
|all-in-one/sources/decoded-original/0298-FlgNet.xml|4c6e59241d4da79ef0b9cac72a56088d2dfdb5faa9a1dca8b6116a43b8ff0d7d|9ebc17249325ff3f0062c1b7f14cce7e5a14dace|True|
|all-in-one/sources/decoded-original/0299-FlgNet.xml|290c11c2038a3ef43b5480127768643161d18fc3ae973f49308883fb02ef166d|7c1c5146dde6694df2386b85272cd0737519d813|True|
|all-in-one/sources/decoded-original/0300-FlgNet.xml|68aed4b55aa84875e10bea79bd05969696019b7d592ffe033b071a7cbdc356ec|45724ff286b36dc0ed6825cdd8988e01da0186fb|True|
|all-in-one/sources/decoded-original/0301-FlgNet.xml|75bb192b2bf119d9a047203ad2c65595f637377376615a4362d6b8bc0607203f|4ef7775c5eb10ccf2564698b8416dff0ac500b8b|True|
|all-in-one/sources/decoded-original/0302-FlgNet.xml|b5e69b459caae2929f037343ccbdba1da28b523c39371cff1583c7b96b21e6ba|2a35aa4ec31de80589b66119d5269c53c53f4b66|True|
|all-in-one/sources/decoded-original/0303-FlgNet.xml|33ca0f156e3afa2e758203fd1ec594c8f95f34682659cb747acbf8168007d88b|a688d6b81bbb0969fc6ea3973fbc00ee15b9b93d|True|
|all-in-one/sources/decoded-original/0304-FlgNet.xml|fe6cf41278da9b0fa31a16e8db4a8437bf1db30cc29737ba72f0c05746c66b0b|3020b0f271d5d9d08457a0a8bb1daea790d5b7f1|True|
|all-in-one/sources/decoded-original/0305-FlgNet.xml|949ca5dbd42f4084b75f881da1fd530af096a94c11c6f4d9b7e4eed4b3cf3f97|c66451d899d0e545f55ed32fd2beeb74777df222|True|
|all-in-one/sources/decoded-original/0306-FlgNet.xml|a8d53cbb5eca6037686459d44efa3f5dc7d01e0278eec7b004bbdc6c10b89401|13d8edc06c75cd2420621208e410af43585cde18|True|
|all-in-one/sources/decoded-original/0307-FlgNet.xml|7b985a52bf2589306512c69dfd3d222e5341f7d5f7da58dca4a43786380d4446|b15a95a01a7c16b49b5c4385d411b4068ee5f62b|True|
|all-in-one/sources/decoded-original/0308-FlgNet.xml|4594c2942fa2de3937b61830619fbd26c17b59a2617fec33f76d8cefebecab80|f237a1cfe6ec68ba7000c5c6a6a06aae1cd94166|True|
|all-in-one/sources/decoded-original/0309-FlgNet.xml|a7f64a579271b0591d4d5c598221572384dce6eaac4587629447e4ad0f890180|0dc36bdf7a0c03dd13820fa2c665acf6f70d95f5|True|
|all-in-one/sources/decoded-original/0310-FlgNet.xml|c9f5daacd865ba3757ba2621250c8240659c98dc30d38c012ca72e608b613e5f|b66213e3c7ecfe62b52634fdfc99aa8533f6538d|True|
|all-in-one/sources/decoded-original/0311-FlgNet.xml|9f5300f71fb94b8f68c9056aa72cbd001a9f472601a8709409bf011e4be72a8f|06dc57a339737347f296253d24f683c0aa988064|True|
|all-in-one/sources/decoded-original/0312-FlgNet.xml|c871fcc3e52da6fdc937f4891428750ee644e2f545df772f22e2efdbefce9122|fde77f621405b62f624ecc155b5ddd0e8b7383a7|True|
|all-in-one/sources/decoded-original/0313-FlgNet.xml|4a9f084345aa94f2e4e16cc1329f8b2baed2c22266b688000809dfbd7af57d8a|6d3be6f78e64477a4724d39d91b810237c9ab0ec|True|
|all-in-one/sources/decoded-original/0314-FlgNet.xml|ba064c834769a44e67d681925193fc987738302773b44fc91428379725db2db4|b98023eec88e04b79b94ef897414f82c6195b71b|True|
|all-in-one/sources/decoded-original/0315-FlgNet.xml|ee681be380623ee8d2e3d5eb524d8462c61c38f52fd15fe7c1884d65491df5f6|44d1c16c0e924a3f4289faa930a2b29597db1c82|True|
|all-in-one/sources/decoded-original/0316-FlgNet.xml|dcc6b4a27cf8d4e20f877dedd8180bc7a0289b34a37129f068495c143792286c|427ad0e5777e70a83d57f870be0a482cc00b3c55|True|
|all-in-one/sources/decoded-original/0317-FlgNet.xml|e352b630d675157b03dbd97376f60ca65e19b8dedb2ec59d067e58bb02310ce3|9d1dbf50d5a2ce807d4edc8d6bd2ea5674137122|True|
|all-in-one/sources/decoded-original/0318-FlgNet.xml|95cb71fd6c81291ae7e1ff1e36cf7613a7d635615828120b4d595838a1459bb9|d361e9fb6ee443a1d6ea545e344342a8845e08f1|True|
|all-in-one/sources/decoded-original/0319-FlgNet.xml|ddf91f85879fa230f7306959029d4dc13ef6f182a51e32fcabd896cb75ea4af3|de85fa3b8350adfd9f22bec69ab0974777faca94|True|
|all-in-one/sources/decoded-original/0320-FlgNet.xml|4279b69c8bbb37cfcea7b5e389bb66c5d48ef2c45ce7447ee8ba456c48f6d8bd|3062344c783b72c4a413b164a89657058e0ac8f4|True|
|all-in-one/sources/decoded-original/0321-FlgNet.xml|8ebe3a4cfeea89e45286e45d219196561cd426e078d7126ceacb48d8a40f75db|ab21dfe82186e33a1f7a3fc7ec106be52455b797|True|
|all-in-one/sources/decoded-original/0322-FlgNet.xml|2807f177fb91e2aa07e71dc9a608f4fbf5a91b1079dd6b7fca06bc72e098c28a|95ec07605ca3dd6e3fd0e92eba35f868237d048a|True|
|all-in-one/sources/decoded-original/0323-FlgNet.xml|2c71fa2f9c4598d2f0596bc796042d42ab78103e0ddba940c85f06ec595e9a42|43453ad0dab625bb0b4036de8c5b4109c9ddc7cc|True|
|all-in-one/sources/decoded-original/0324-FlgNet.xml|bc65a2bce991e021fcf6643e0ebc01b59d5495763940ec3b489b4608577e9b11|a5b52d825a9ed8ea41a8c5a08860ab66d67dd75c|True|
|all-in-one/sources/decoded-original/0325-FlgNet.xml|f0a2ee6233672a3a6482fe368751677da15768dd24c4bb1147ee0ae9fe2f77c2|717013135bdc3fa7e48aa23318766cb219ebab2e|True|
|all-in-one/sources/decoded-original/0326-FlgNet.xml|b7f4bcae2be6c5542a5fa65406500b70f45bca33055e671306a00510251b70de|def852bc737b2de7ae9b9c012469991bd0b451e9|True|
|all-in-one/sources/decoded-original/0327-FlgNet.xml|ee431cdc1e4e1708d37b58c1c2df1c3e0bba13f45fea4c1c41f35f158df35769|6da6dfd0f68ff5c2e1586cd973c26f89114f8928|True|
|all-in-one/sources/decoded-original/0328-FlgNet.xml|7b05b92a205d7c1b5dc6fb81aaaf92f017a286e1840cc3002d1d2744f9fe9df1|f0f531ee86d6e754f4610bb97976f549b53dabd5|True|
|all-in-one/sources/decoded-original/0329-FlgNet.xml|7aa07b96a1f1d7dee6c875abdd6dca86fa0b02874e2d6b21526f86f1575a164f|812b5464d0d8bea4fbfd4a1515d76298ee61ca7d|True|
|all-in-one/sources/decoded-original/0330-FlgNet.xml|4fa97e4acad5d8c1e67137332a0ee61e88926fd57293a4130fddedcc83dce88c|62f41b3179c4236c71f6d99be974cb4b3662daec|True|
|all-in-one/sources/decoded-original/0331-FlgNet.xml|ddd1ed85b11ff4338bdca0eed85766c5cd890bc84d851fae0463a98034ee0f19|633d409dc80bd3c28b9a811482fcc4dfe6082978|True|
|all-in-one/sources/decoded-original/0332-FlgNet.xml|c677499004010aba2746412a08e32f3e4206e9212d481fc08ee1c6023326cef7|50e3451e01b63fb9311aade1c4bfefa0719d305b|True|
|all-in-one/sources/decoded-original/0333-FlgNet.xml|4031a340e2cf8e008bcf602413e0b71e067891985f0bd3befd7c23ff24cc0483|847746715ac2603cc6b84919e3f616073090f332|True|
|all-in-one/sources/decoded-original/0334-FlgNet.xml|d76007d20f67bcb8f127fef6e7050e0973619a35ef4f5c34c367dc3b3c38932e|7310cc3d9a1324fa17c3c7ea7b8ffe1c62be96fa|True|
|all-in-one/sources/decoded-original/0335-FlgNet.xml|6f0214de436cfaac95750cc25ba3d6f306d33174472618754fac38ad4caf4781|6f065e48bd456e656557f1f94896597028f42c5f|True|
|all-in-one/sources/decoded-original/0336-FlgNet.xml|1be4f76dba11e6cceea057743c8b15b8a4bea4edfe87c19ef0581d7b65ffe56a|3bb3ae34dc100f7a9483cf8bf7702c01e080371d|True|
|all-in-one/sources/decoded-original/0337-FlgNet.xml|403f3a0e9218bbe81fb00cb93fb9f6bd3570af2df157abccd878a3a1f60f2580|3f2586314b90cbe03be441d83dc1a3086fa76053|True|
|all-in-one/sources/decoded-original/0338-FlgNet.xml|762ab4b1520aa101efc897ff9e4b72a35f5591ff460a0b654dc87919849077a1|fb17f25dd9f6614db036e3200fc5e17a77dc2cf7|True|
|all-in-one/sources/decoded-original/0339-FlgNet.xml|ce2c6279b55c8a5ac837a0f7c7a0945636df7dc52b68a1c3d6ec158234b37543|df1b2a3dd9389a264ed6cebee9c4e3a7270fc6fb|True|
|all-in-one/sources/decoded-original/0340-FlgNet.xml|00acb073128337e7d7b95bbedeb50cd0e72c89772d835bdf392da17b3e2d0add|2807ab8484ffd8a35d55bdeb12733a78de525100|True|
|all-in-one/sources/decoded-original/0341-FlgNet.xml|e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96|45dbda06a692b21380a52207a22094b2e0a9c5a3|True|
|all-in-one/sources/decoded-original/0549-FlgNet.xml|49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1|985b5310b43b1015b5dee286aa0e42800564b94b|True|
|all-in-one/sources/decoded-original/0550-FlgNet.xml|ff691b4fa855e6b19bc68f19113a315cbc5da818196b6f2423a47d1650226918|1723621273575e9962b9f2f33f96d0949f617768|True|
|all-in-one/sources/decoded-original/0551-FlgNet.xml|c0a227e0cb72f33fd7149d3718f123d98a36354970e8d515cdf8bf7c95afb375|fb16f0ddb637a734c5adbde8c51c2edc246520f9|True|
|all-in-one/sources/decoded-original/0613-IdentXmlPart.xml|09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb|c9d19a48e947098914f4d2de3348c05b4f6d37e8|True|
|all-in-one/sources/decoded-original/0614-IdentXmlPart.xml|c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294|da0485aa033700f08c8695d30b93ebd2d377d6c7|True|
|all-in-one/sources/decoded-original/0615-IdentXmlPart.xml|80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a|49eb86fe01feb83de8c0864b21493d305aff8b20|True|
|all-in-one/sources/decoded-original/0616-IdentXmlPart.xml|650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d|9f7fdd5f93ac149c139a054ebb34f63c632ef7fd|True|
|all-in-one/sources/decoded-original/0688-IdentXmlPart.xml|ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda|463585759f1ecd94f32362b4fefb000a152f5773|True|
|all-in-one/sources/decoded-original/0689-IdentXmlPart.xml|f0cc6f770c2759b92a9a79f4e289dbfa0ca270d90e0e89496f94a13a8d839d51|8db940bdbab78ea27ffc280acba9375d2a93f587|True|
|all-in-one/sources/decoded-original/0690-IdentXmlPart.xml|fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541|36bd403f48ba8e364126837b19fb0419bbe78941|True|
|all-in-one/sources/decoded-original/0691-IdentXmlPart.xml|17cb7d9734d76b39e729e0daf0c89d9bdf74907aab2130c80453fa04e4cea1da|d38a1a394f3cf9612e2f344142609e376ef47953|True|
|all-in-one/sources/decoded-original/0692-IdentXmlPart.xml|bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037|737785d03b5fad43c5b4d451955726d800edb1c0|True|
|all-in-one/sources/decoded-original/0693-IdentXmlPart.xml|9315ddf43bdfbd7367ab0735a5bbfffcd81ced257d1907c1e2c08ae6b8bfa7ab|6ee2a128582aa9ceac710b82de14e5ec2c96771a|True|
|all-in-one/sources/decoded-original/0694-IdentXmlPart.xml|757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d|c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d|True|
|all-in-one/sources/decoded-original/network-map.json|c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60|424430b6b953e43138e5d0a18ca40c949e21cfa1|True|
|all-in-one/sources/hmi-windows.csv|15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e|8401dcfe5ba3e7e244eea0f501bb84a2e387da39|True|
|all-in-one/sources/hmi_plc_tags.csv|a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404|cf4c0650e7c7baac350dcb89909b808435704880|True|
|all-in-one/sources/live_index.json|14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1|e35ccea1f841349c632666c29954b7bcd4f5839e|True|
|docs/equipment-standard/INVENTORY.json|720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc|587c3748ad9224718f95ba06463fee913dae231d|True|

## 부록C. 최종 자체검사 및 중지자산 보존

실제 검사시각 2026-10-11T12:05:03.110061+00:00. 명령 `python gme-research/extracts/SYS-RUNHOURS/extract.py` 및 `python gme-research/extracts/SYS-RUNHOURS/verify.py`는 이 조사에서 작성한 정적 XML/문서 해시 검사이며 원본 생성기·PLC/시뮬레이터 동작 시험이 아니다. 두 명령 종료코드0. 선정원본75 해시, FC2 XML52·Main XML4, 계수채널40·Reset필드46, HMI782행 직접대응0, 고정원본 Git dirty0을 확인했다.

|검사|결과|
|---|---|
|channel_count_40|True|
|fc2_network_count_52|True|
|all_hour_move_one|True|
|all_min_hour_int|True|
|reset_network_count_10|True|
|reset_write_count_46|True|
|source_hashes_fixed_blob_all|True|
|source_current_unchanged|True|
|hmi_db9_named_targets_zero|True|
|stopped_five_hashes|True|
|source_git_clean|True|

중지5자산은 내용 분석·실행 없이 보존 해시만 비교했다.

|경로|SHA256|동결기준 일치|
|---|---|---|
|all-in-one/registers/program-model.json|6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5|True|
|all-in-one/assets/program-model-data.js|52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f|True|
|all-in-one/assets/virtual-plc.js|5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc|True|
|all-in-one/assets/simulator-workspace.js|3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc|True|
|all-in-one/registers/virtual-plc-test-results.json|a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64|True|

정적 검사 통과는 독립 검토·TIA 컴파일·현재 CPU·HMI 이벤트·기록 복원·실제 게시·현장 복구 완료가 아니다. 종료시각은 이 검사시각 기준이며 이후 부모 검토/전달 시각과 구분한다.
