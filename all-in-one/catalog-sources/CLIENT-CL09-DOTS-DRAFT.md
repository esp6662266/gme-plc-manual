# CLIENT-CL09 Belt conveyor C 자체 원본 조사 초안

## 핵심 확인·상충·누락

- 조사 ID는 **CLIENT-CL09 한 개**다. Belt conveyor C 외부 연동 채널이며 공압 CYL-CL09와 병합하지 않는다.
- RUN **I13.3**, 경보에 실제 사용되는 FAULT **I15.6**, 유지경보 **DB3.DBX15.1**을 고유 XML 선언·NID·RID·UID·Part/Wire로 독립 확인했다.
- **같은 이름의 별도 입력:** 백업에는 `BELT CONVEYOR C FAULT_doppio!` **I16.6**가 있고 OEM FG95/PDF96, FG132/PDF133에도 BELT CONVEYOR C FAULT가 별도로 그려져 있다. 실제 CL09 래치 0228은 I15.6을 참조한다. 두 입력이 동일 실물·동일 고장이라고 합치지 않는다.
- **Q61.5는 심볼만 확인:** `start client motor 9` 선언이 live_index doc483에 있지만 선택 원본 XML에서 실제 쓰기/호출 핀, OEM의 출력 릴레이·상대 제어반 끝점을 식별하지 못했다. 명령 존재와 실행 쓰기·물리 연결은 별개다.
- 0300 시간계수는 MIN+1 뒤 MIN≥60에서 **HOUR := 1**, MIN := 0이며 0333에서 HOUR := 0의 다른 writer가 있다. HOUR를 누적 ADD로 바꾸지 않는다.
- 실제 렌더 6쪽 모두 해당 회로에 **SPARE** 표시가 있다. 과거 주소 설명, 도면, 백업 논리의 일치가 현장 사용·정상극성·현행 보호값을 증명하지 않는다.
- 공통근거 인덱스: [CLIENT-CL04](CLIENT-CL04-DOTS-DRAFT.md)의 Main/FC2/FC9·Word 미러 구조, [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md)의 저장 핸드셰이크, [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md)의 공통 Reset/집계, [SYS-PLC-IO](SYS-PLC-IO-DOTS-DRAFT.md)·[SYS-HMI](SYS-HMI-DOTS-DRAFT.md)의 상위 호출과 이벤트 미확정 경계를 연결 재사용한다. CL09 고유 선언/래치/시간쓰기/미러/전기 끝점은 이번에 직접 대조했다.

## 1. 설비·자료 기준

대상은 `docs/equipment-standard/INVENTORY.json#/catalog/65`, CLIENT-CL09, Belt conveyor C, kind client, 외부 연동, 부모 없음, phase2다. 외부 모터 채널의 원격 입력 및 내부 경보/계수를 문서화한다. 외부 벨트 본체, 모터·감속기·외부 제어반 내부 프로그램의 실물 동일성은 미확정이다.

기준은 읽기 전용 `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0이다. 최신 로컬 통합·게시 기능의 검증이 아니다. NNNN 약칭은 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 같은 번호 IdentXmlPart.xml이다. 파일번호·document_id·NID는 별개다. live_index/network-map은 탐색 색인이며 핵심 XML이 있는 곳은 원형 선언/핀으로 재확인했다.

- 실제 착수: 2026-10-11 12:23:17 UTC
- 선언/고유 논리 원본 조사: 12:23~12:24 UTC 도구 실행 기록
- 실제 PDF 렌더·시각 검토: 12:24:10~12:24:25 UTC
- 선정 해시/검사 기록: 2026-10-11T12:25:22.355920+00:00
- 실행 모델·추론 런타임 증명: 미확인
- 원본 Git HEAD 일치 및 `git status --short` 공란 확인. 원본/공통코드/대장/운영기록/SEJIN/PLC/보호값 변경 없음. 원본 build/test/generator·시뮬레이터·행동시험 실행 없음.

## 2. I/O·HMI

### 2.1 고유 선언

|대상|선언·문맥·주소|해석과 경계|
|---|---|---|
|BELT CONVEYOR  C RUN|0613 RID56 Global, NID9 UID532, Bool SSD AO107, SAD Input SAM=None → I13.3|원시 입력영상. 벨트 실제 운동의 직접 증명 아님|
|BELT CONVEYOR C FAULT|0599 RID22 Global, NID9 UID197/199, Bool AO126, Input SAM=None → I15.6|0228에서 실제 사용되는 고장 입력|
|BELT CONVEYOR C FAULT_doppio!|live_index `_7ev` doc567, Bool `%i16.6`, comment `e20.0 belt conveyor "c"fault`|별도 심볼/전기회로 존재. 고유 XML 제어 소비자는 미식별. I15.6의 별칭으로 처리 금지|
|start client motor 9|live_index `_7ev` doc483, Bool `%q61.5`, comment `it should be free but it is used`|심볼 선언 수준. 실제 coil/Move/Call writer 및 전기출력 결속 미확보|
|Allarm.motor_client_09_fault|0601 RID23 Global Bool AO121, BAD4→0600 RID4 TOD3; NID9 UID198/201 Write → DB3.DBX15.1|내부 Set/Reset 유지경보|
|Flag.RESET_ALLARM|0601 RID7 Global Bool AO48 BAD6→0600 RID6 TOD2; NID9 UID200 → DB2.DBX6.0|공통 내부 Reset. HMI 버튼 이벤트와 구분|
|ON|0599 RID1 Global Bool AO0 Memory, NID9 UID196 → M0.0|이름만으로 상수 true로 치환하지 않음|
|CLIENT_MOTOR_9_MIN|0615 RID58 Global Int AO256 BAD5→0614 RID5 TOD9; NID9 UID533/535/536/541 → DB9.DBW32|Add+1 및 Move0 쓰기|
|CLIENT_MOTOR_9_HOUR|0615 RID60 Global Int AO272 BAD5; NID9 UID539와 NID48 UID2659 Write → DB9.DBW34|Move1/Move0, 누적 Add 아님|
|Tag_47 / Tag_48|0613 RID1 Timer AO13 / RID284 Timer AO17 → T13/T17|공유 시간계수·저장 처리용 PLC 타이머. HMI 태그/기동감시 타이머 아님|
|Flag_Aggiorna_DB|0613 RID13 Global Bool Memory AO15, NID9 UID542 Write → M1.7|저장 갱신 요청 관련 내부 비트|

고유 선언은 Global, 1·60·0·S5T#1M은 Constant다. Local로 오인하거나 다른 블록의 같은 RID/UID만으로 결속하지 않았다. RUN 백업 doc523의 comment `e 14.0`, FAULT doc541의 `e 18.6`은 실제 Address I13.3/I15.6과 상충하는 과거 설명으로 보존한다.

### 2.2 HMI와 Word 미러

`all-in-one/sources/hmi_plc_tags.csv`의 `BELT_CONVEYOR_C_RUN`, `DB13,X13.3`, Access Name PLC, ID003FD를 확인했다. `Allarmi_122`는 `DB3,X15.1`, ID00113으로 유지경보와 일치한다. 태그 설정은 현재 화면 표시·통신·버튼 이벤트·ACK·스크립트 검증이 아니다. Q61.5 기동 버튼/권한/이벤트 경로와 DB9 직접 HMI 태그는 이번 범위에서 미확보다.

0397 HMI Inputs NID1을 직접 확인했다. 이것은 bit별 Coil이 아니라 **Word 복사**다.

|원시→가공|선언 및 실제 Wire/핀|영향 범위|
|---|---|---|
|IW12→DB13.DBW12|0627 RID19 Tag_183 Word AO96 SAD Input SAM=None, ORef63 W70→Move60.in; rail W21→en; out1 W72→ORef64/0629 RID20 Word AO96 BAD4→0628 TOD13|I13.3을 포함하는 byte12~13. RUN 미러 결속|
|IW14→DB13.DBW14|Move60.eno W71→Move61.en; ORef65/0627 RID21 Tag_274 Word AO112 W73→in; out1 W75→ORef66/0629 RID22 Word AO112|I15.6 포함. 내부 DB3 유지경보와 별도 원시 FAULT 미러|
|IW16→DB13.DBW16|Move61.eno W74→Move62.en; ORef67/0627 RID23 Tag_275 Word AO128 W76→in; out1 W77→ORef68/0629 RID24 Word AO128|I16.6 포함. 별도 이름 입력의 범위 미러이며 0228 경보와 병합 아님|

Move60/61/62의 DisableENO=true 속성과 원문 eno/en 연결을 모두 보존한다. 독립 Bool 직접쓰기나 PIW/Peripherie 접근으로 바꾸지 않는다. 위 Word 범위 결속은 두 fault 입력을 의미적으로 합친다는 뜻이 아니다. FC15 상위 호출·다른 writer·실제 스캔 최종값과 현재 HMI 이벤트는 공통 경계를 유지한다.

## 3. 제어 구조

### 3.1 상위 호출

0549 Main document1620 NID7의 rail W352→Contact350.in, ORef335/RID52 W348→operand(0692의 ON)이며 Contact350.out W351은 CRef331 및 CRef334의 en에 **병렬** 연결된다. CRef331 RefId80 안 CodeBlock345 RefId79는 0688 RID79 `Motor/Alarm Client` TOD9 FC, 0694 RID80 NID7 UID331 TORID79와 결속한다. CRef334 RefId83 안 CodeBlock347 RefId82는 0688 RID82 `time work motor` TOD2 FC, 0694 RID83 NID7 UID334 TORID82와 결속한다. 앞 FC의 ENO 성공을 뒤 FC의 순차 허가로 추정하지 않는다. 실행주기/현재 CPU 실행 증거는 없다.

### 3.2 RUN 기반 고유 시간계수

0300 document1010, FC2 NID9 전체 고유 핀을 확인했다.

1. rail W564→Contact560; T13 ORef531/RID1 W543→operand. 560.out W561→Contact562.in; RUN I13.3 ORef532/RID56 W544→562.operand.
2. 562.out W563은 Add514.en 및 Ge521.pre에 분기한다. Add514는 SrcType Int; MIN ORef533/RID58 W545→in1, Int1 ORef534/RID7 W546→in2, out W547→ORef535/RID58 MIN이다.
3. Ge521 Int는 MIN ORef536 W548→in1, Int60 ORef537/RID8 W549→in2; out W550→Move524.en.
4. Move524.in은 Int1 ORef538/RID7 W552, out1 W553→ORef539/RID60 HOUR다. 즉 HOUR := 1이다.
5. Move524.eno W554→Move527.en; Int0 ORef540/RID12 W555→in, out1 W556→ORef541/RID58 MIN. Move527.eno W557→SCoil530.in; operand W558/ORef542/RID13은 M1.7을 Set한다. ENO 체인을 생략하지 않는다.

0333 document1046 FC2 NID48은 다른 writer다. T17 ORef2651/RID284 W2662→Contact2677.operand, rail W2679→in, out W2678→Move2636.en. Move2636→W2665→Move2639→W2668→Move2642→W2671→Move2645의 eno/en 체인을 거쳐 CL09 HOUR에 쓴다. Move2645.in W2672/ORef2658/RID12=Int0, out1 W2673/ORef2659/RID60=DB9.DBW34이다. 주변 CLIENT 필드에 대한 완료 집계는 하지 않는다.

### 3.3 공유 타이머와 미확정 명령

0019 FC2 NID58의 Contact3120은 operand NOT(T13 ORef3115/RID1/W3118), out W3121→SdCoil3112.in, value W3117/ORef3114/RID335=0616 S5Time `S5T#1M`(V5632), operand W3119/ORef3116=T13이다. **분 계수용 공유 타이머**를 CL09 기동/고장 지연으로 복제하지 않는다. T17/M1.7/M2.0 및 외부 저장 ACK의 상세 경계는 SYS-RUNHOURS 공통 원본을 참조한다. HOUR 0/1만으로 장기누적 저장 성공이나 운전시간 정확도를 판정할 수 없다.

IdentXmlPart 181개에 대한 이름 검색에서 CL09 RUN/FAULT/경보/MIN/HOUR의 5개 선언 항목을 확인했다. `start client motor 9`·`doppio` 명명 선언과 Output AO493(Q61.5)/AO488·480 범위 후보는 미식별이었다. 이는 검색 경계이며 모든 절대/간접쓰기·블록복사 부재의 증명이 아니다. Q61.5가 어떤 모드/허가/기동/정지 회로를 통해 동작하는지, 외부 벨트 전력회로·보호회로와 어떻게 연결되는지는 미확정이다.

## 4. 전기 전달 끝점

원본 `all-in-one/sources/Electrical_Rev2.pdf`를 실제 PDF **90·94·96·130·132·133**쪽으로 렌더하여 시각 확인했다. 각 페이지 footer를 개별 확인했으며 모두 **Rev2 17.03.2025 / DATA 27.05.2024**다. FG와 실제 PDF 번호를 따로 기록한다.

|경로|실제 도면 끝점·근거|미확정 경계|
|---|---|---|
|RUN 외부 접점|FG89/PDF90: +24Vdc10.7 → 5x20 2A F, X1:300 → 선89.4 → 그려진 열린 접점 → X1:301 → E13.3 /129/4|상대 제어반 단자·접점기기번호·케이블번호/규격 없음|
|RUN PLC 입력|FG129/PDF130: E13.3, 역참조89/6 → 입력 단자14, 표기 CPU515 MOD11|현재 CPU·장착모듈·실물 연결 증명 아님|
|래치용 FAULT 외부 접점|FG93/PDF94: +24Vdc10.7 → 5x20 2A F, X1:338 → 선93.3 → 열린 접점 → X1:339 → E15.6 /131/6|I15.6에 해당. 정상극성·외부 고장 종류 미확정|
|래치용 FAULT PLC 입력|FG131/PDF132: E15.6, 역참조93/4 → 입력 단자37, CPU515 MOD11|외부 보호기 설정/복구 회로와 별개|
|이름 중복 FAULT 외부 접점|FG95/PDF96: +24Vdc10.7 → 5x20 2A F, X1:354 → 선95.1 → 열린 접점 → X1:355 → E16.6 /132/6|I16.6, 백업의 fault_doppio! 후보와 주소 일치. 실제 동일 벨트/동일 접점이라고 확정 금지|
|이름 중복 FAULT PLC 입력|FG132/PDF133: E16.6, 역참조95/1 → 입력 단자7, CPU515 MOD12|0228의 I15.6 입력으로 치환 금지|
|보조전원|FG129/PDF130: +24Vdc10.7→X21:3012 5x20 2A IST.→129.1→단자19; -0Vdc10.6→20. FG131/PDF132: X21:3013 2A IST.→131.1→39; -0Vdc10.6→40|그린 도면 정격. 현행 퓨즈/보호설정 추천 아님|
|기동 출력|Q61.5 심볼만 확인. 선택 OEM PDF 텍스트에서 A61.5/Q61.5 출력 연결 미식별|릴레이명·A1/A2·부하접점·출력모듈·단자·외부 모터 전력회로 미확보|

해당 RUN/FAULT 범위에 SPARE 점선이 있다. FG132의 E16.6은 별도 작은 SPARE 점선이며 E16.0~5의 SPARE 묶음과도 구획이 다르다. 열린 접점 그림을 현장 정상극성이나 고장 시 실제 동작의 증명으로 취급하지 않는다. 이 입력 회로에 다른 릴레이의 부하접점5/9 또는 하단 접점표1/5/9 번호를 복제하지 않는다.

`Electrical_Can_Decoating_20241118.pdf`에서도 CL09 이름/출력 텍스트의 별도 결속은 이번 검색에서 없었다. 이 시공 PDF는 이번 실제 렌더 대상이 아니며 전수 의미검토 완료로 쓰지 않는다. 실제 외부 제어반 및 케이블표가 추가되어야 출력→외부기기 끝점을 완성할 수 있다.

## 5. 알람·복구

0228 document418 `motor/alarm client`, FC9 NID9 고유 경로는 다음과 같다.

- rail W219→Contact211.in; ON ORef196/RID1 W202→operand. 211.out W212가 Contact213/215.in으로 분기.
- Set: I15.6 ORef197/RID22 W203→Contact213.operand; out W214→SCoil190.in; operand W205/ORef198/RID23=DB3.DBX15.1. 식은 ON AND I15.6 → 경보 Set.
- Reset: I15.6 ORef199/RID22 W206→Contact215.operand(**Negated**); out W216→Contact217.in. 내부 RESET_ALLARM ORef200/RID7 W207→operand; out W218→RCoil195.in; operand W209/ORef201/RID23=같은 경보. 식은 ON AND NOT I15.6 AND RESET_ALLARM → 경보 Reset.

이 네트워크에 타이머 Part는 없다. RUN I13.3=0이나 별도 I16.6을 직접 원인으로 추가하지 않는다. 원시 고장이 계속 참이면 위 Reset 가지는 성립하지 않는다. I15.6 원인 소멸, PLC 유지경보 해제, HMI ACK, 외부 제어반 자체 Reset, 재기동, 현장 정상복구는 각기 다른 상태다.

Allarmi_122는 내부 비트와 주소가 일치하지만 실제 표시문구·ACK 이벤트·소리·경보이력은 미확정이다. 공통 DB3 경보집계 및 Reset 생성은 SYS-ALARM의 동일 고정입력 근거를 연결한다. 이 한 비트가 외부 벨트를 직접 정지시키는 출력 writer는 확보하지 못했으므로 정지 인과를 발명하지 않는다.

## 6. 증상별 읽기 전용 관찰 기준

현장 조작 순서가 아니라 승인된 담당자가 제공한 자료를 비교할 위치다. 강제출력·바이패스·보호값 변경·활선 점검·Reset 실행을 제안하지 않는다.

|증상|동일 시각 관찰 항목|문서 비교·한계|
|---|---|---|
|기동 표시인데 벨트 정지|현재 프로젝트 식별, Q61.5 값과 writer, 화면 이벤트, 외부 제어반 상태, I13.3|심볼 이름만으로 실제 기동전원 연결을 확정하지 않음|
|현장 RUN인데 화면 미표시|I13.3, IW12, DB13.W12/X13.3, HMI ID003FD|FG89 X1:300/301→FG129 단자14와 0397 Word 미러 분리. 통신/배선/극성을 임의 단정하지 않음|
|FAULT 표시가 서로 다름|I15.6, I16.6, DB13.X15.6/X16.6, DB3.X15.1, 양쪽 단자표|0228은 I15.6만 사용. X1:338/339와354/355를 별개로 기록하고 서로 치환 금지|
|고장 소멸 후 경보 유지|ON, I15.6, DB2.X6.0, DB3.X15.1, HMI Allarmi_122|유지 래치 및 NOT FAULT Reset 조건. 외부 원인 소멸과 내부 해제를 구분|
|Reset 요청에도 경보 지속|HMI 요청/이벤트, 내부 Reset 생성, I15.6 전후와 경보비트|HMI ACK를 PLC Reset이나 외부 Reset과 동일시하지 않음|
|시간값이 1에서 멈추거나 0으로 바뀜|I13.3,T13,T17,DB9.W32/W34,M1.7,외부 저장 로그|0300 Move1·0333 Move0 구조. 실제 장기누적/저장 성공 미확정|
|문구와 주소가 불일치|백업 판본, 현행 도면, 모듈/단자 표찰, 외부회로 사진|과거 e14.0/e18.6/e20.0과 실제 백업 주소를 보존하고 임의 배선수정 금지|

관찰자·실제 시각/시간대·위치·값/단위·장치·프로젝트와 도면 판본·사진/로그 출처·비교결과·배제 결과·승인된 조치와 복구 증거를 별도로 남겨야 한다. 실제 운영/SEJIN 자료를 이번 산출물에 복제하지 않았다.

## 7. 완료·누락·검증 범위

|영역|상태|잔여 증거|
|---|---|---|
|설비·자료 기준|적용, 문서 작성|외부 Belt conveyor C 실물 동일성|
|I/O·HMI|입력·경보·시간 선언과 미러 확인|Q61.5 실행 쓰기, HMI 이벤트, 현재 통신|
|제어|고유 FC9/FC2·상위 호출 선택 검토|기동·정지·수자동·외부 허가/시퀀스|
|전기 끝점|RUN/두 FAULT 실제 렌더6쪽 확인|기동 출력·외부 상대 단자·케이블·현장 적용|
|알람·복구|고유 S/R 및 무타이머 구조 확인|외부 보호 원인·ACK/Reset/현장복구|
|증상 관찰|읽기 전용 비교 기준 작성|실제 관찰값 미취득|
|완료·누락|document complete_with_gaps|BC01 동등 구현·게시·현장 완료 아님|

필요자료: 현재 외부 Belt conveyor C 제어반 회로/프로그램·기동 허가표, Q61.5 간접/절대주소 포함 교차참조, X1:300/301/338/339/354/355 상대 단자 및 케이블표, I15.6와 I16.6의 분리 이유·실제 사용 여부, 현행 HMI 이벤트/스크립트, 명판·회로 개정·RUN/FAULT 정상상태 증거. 새 자료가 없으면 같은 실물 보류를 반복 조사하지 않는다.

네 기능 중 도면·래더 비교용 원본 위치만 준비했다. 이 ID의 백업 미리보기/선택복원, 기록 전후비교, 관찰 보고서/PDF 구현·저장·재읽기·재열기는 실행/검증하지 않았다. 기존 note/repair_observation/미지 필드/초안/저장키는 변경하지 않았다.

최종 상태: documentation `complete_with_gaps`; static_review `selected_original_xml_and_pdf_reviewed`; ui_records `not_run`; publication `not_published`; tia_compile/live_cpu/field_recovery `not_performed`. 부모 독립 검토 및 첨부 대기이며 로컬 통합은 별도 담당 범위다.

### 선정 검증과 검색의 차이

선정 원본34개 byte의 SHA256 및 고정 Git blob 내용 일치 확인은 **34개 전체 의미검토를 뜻하지 않는다**. 직접 의미대조는 0228/0300 고유 전체 핀, 0333 CL09 reset 가지, 0397 IW12/14/16 미러, 0549 호출, 0019 T13 가지 및 선택 선언이다. XML181개 명명/주소 탐색 또한181개 의미검토가 아니다. 실제 PDF6쪽을 시각 검토했다. 외부 제어반, 현장 극성·보호값, 현재 CPU/TIA, UI/게시 및 운전시험은 미수행이다.

검사/해시/원형 추출/렌더는 `../extracts/CLIENT-CL09/verification.json`, `source-hashes.json`, `declaration-search.json`, `extended-search.json` 및 같은 디렉터리에 저장했다. 쓰기 범위는 본 MD와 배정 extracts뿐이다.

### 선정 원본 SHA256 + 고정 Git blob 전체 표

경로는 `source-mv06/` 기준이다. Git 내용 일치는 각 파일 byte와 `git show abcf31c:경로`를 직접 비교했다.

|선정 원본 경로|SHA256|고정 Git blob|내용 일치|
|---|---|---|---|
|`AGENTS.md`|`0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2`|`073164bc6efd5791032d62c71b03b4dab48cb6f8`|일치|
|`.agents/skills/gme-equipment-rollout/SKILL.md`|`fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b`|`9aa820ea6ca15b4e136c9772423b78ed4df6a3d4`|일치|
|`docs/equipment-standard/WORK-STANDARD.md`|`05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99`|`f76a570cc73098632e08759b17934000f7e3a253`|일치|
|`docs/equipment-standard/WORK-ITEM-TEMPLATE.md`|`4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586`|`e546f39535d2b589e80f97db869ac37ce4d05cfd`|일치|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|일치|
|`VERSION.json`|`5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7`|`fffb51663b7705aec91cb119ca80ee943a4ce758`|일치|
|`WORKSPACE-HANDOFF.md`|`215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074`|`dd0b8989d2376c4415bba9bd826fe6754c6b1a12`|일치|
|`PUBLICATION_STATUS.md`|`efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740`|`d76401cf291fc0be681acc51fa898ad3ce46ff78`|일치|
|`all-in-one/ACTIVE-WORK.md`|`eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2`|`6eb947c629b5ddf9c759ef87649451303938864b`|일치|
|`EXPANSION-WORK.md`|`ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2`|`4c42d88ecc2d48269eb23e13a20ebf3721a092a1`|일치|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|일치|
|`all-in-one/sources/Electrical_Can_Decoating_20241118.pdf`|`3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd`|`0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8`|일치|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|일치|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|일치|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|일치|
|`all-in-one/sources/decoded-original/0019-FlgNet.xml`|`a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5`|`f78cfdbf5e717304114660ffbd3bb42cbed6d79d`|일치|
|`all-in-one/sources/decoded-original/0228-FlgNet.xml`|`f3c3162c2e10a73b93375825ab48e31441be2cc0953df905d57b4002d927fbf8`|`60e1e4dc4e1b8f5dbe84ca5f5ab98080d2e714fb`|일치|
|`all-in-one/sources/decoded-original/0300-FlgNet.xml`|`68aed4b55aa84875e10bea79bd05969696019b7d592ffe033b071a7cbdc356ec`|`45724ff286b36dc0ed6825cdd8988e01da0186fb`|일치|
|`all-in-one/sources/decoded-original/0333-FlgNet.xml`|`4031a340e2cf8e008bcf602413e0b71e067891985f0bd3befd7c23ff24cc0483`|`847746715ac2603cc6b84919e3f616073090f332`|일치|
|`all-in-one/sources/decoded-original/0397-FlgNet.xml`|`bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834`|`4ab8370493c4e28fc1eabeeebe2743d27f0c4021`|일치|
|`all-in-one/sources/decoded-original/0549-FlgNet.xml`|`49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1`|`985b5310b43b1015b5dee286aa0e42800564b94b`|일치|
|`all-in-one/sources/decoded-original/0599-IdentXmlPart.xml`|`32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1`|`493de77fc827d8f14192ced05d82df3a062f7965`|일치|
|`all-in-one/sources/decoded-original/0600-IdentXmlPart.xml`|`20c58ee0383d0b6c275bd2d96abd30af7c5d1f3fff59c7d5034cd758936b57d5`|`f22a7ededd0576cf379ee19908da067f08d45412`|일치|
|`all-in-one/sources/decoded-original/0601-IdentXmlPart.xml`|`04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862`|`07bcf656fa58e4a305999456644acd24b3dc6bec`|일치|
|`all-in-one/sources/decoded-original/0613-IdentXmlPart.xml`|`09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb`|`c9d19a48e947098914f4d2de3348c05b4f6d37e8`|일치|
|`all-in-one/sources/decoded-original/0614-IdentXmlPart.xml`|`c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294`|`da0485aa033700f08c8695d30b93ebd2d377d6c7`|일치|
|`all-in-one/sources/decoded-original/0615-IdentXmlPart.xml`|`80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a`|`49eb86fe01feb83de8c0864b21493d305aff8b20`|일치|
|`all-in-one/sources/decoded-original/0616-IdentXmlPart.xml`|`650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d`|`9f7fdd5f93ac149c139a054ebb34f63c632ef7fd`|일치|
|`all-in-one/sources/decoded-original/0627-IdentXmlPart.xml`|`08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb`|`61ebc0abbb2ca160e11e1da400a3f14a397d8bc5`|일치|
|`all-in-one/sources/decoded-original/0628-IdentXmlPart.xml`|`9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd`|`170ca5c72599edc7ea7eefe651c3680ce325e76a`|일치|
|`all-in-one/sources/decoded-original/0629-IdentXmlPart.xml`|`67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972`|`058129bb01e27f7a6a0d0293f332d745e5bab74e`|일치|
|`all-in-one/sources/decoded-original/0688-IdentXmlPart.xml`|`ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda`|`463585759f1ecd94f32362b4fefb000a152f5773`|일치|
|`all-in-one/sources/decoded-original/0692-IdentXmlPart.xml`|`bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037`|`737785d03b5fad43c5b4d451955726d800edb1c0`|일치|
|`all-in-one/sources/decoded-original/0694-IdentXmlPart.xml`|`757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d`|`c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d`|일치|

초안 작성 완료 실제시각: 2026-10-11T12:28:03.090953+00:00
