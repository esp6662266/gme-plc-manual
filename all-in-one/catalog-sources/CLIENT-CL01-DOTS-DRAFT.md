# CLIENT-CL01 · Apron conveyor A 자체 원본 조사 초안

## 핵심 확인·상충·누락·공유 근거

- 외부 모터 채널 CLIENT-CL01 한 ID만 다룬다. 공압 CYL-CL01, Apron conveyor B/CLIENT-CL13와 병합하지 않는다.
- 원시 RUN은 **I12.3**, FAULT는 **I14.6**. 선언·원본 핀과 FG88/PDF89, FG91/PDF92의 실제 접점/단자 및 FG128/PDF129, FG130/PDF131 모듈 끝점을 직접 확인했다.
- 두 입력은 실제 도면의 **SPARE 점선 범위** 안에 있다. 회로·PLC 이름이 존재해도 현재 설치/사용·실제 정상극성·모터 회전을 입증하지 않는다. 외부 제어반 회로와 케이블/접점 장치명은 미확보다.
- 전용 기동 출력/명령은 이번 이름·심볼·XML 검색 범위에서 미식별이다. 다른 CLIENT 출력 Q61.2/3/4/5/6을 CL01 출력으로 가져오지 않는다. 출력이 실제로 없다고 단정하지 않는다.
- FAULT는 ON AND FAULT 조건의 래치 Set, ON AND NOT FAULT AND RESET_ALLARM 조건의 Reset이다. 이 네트워크에는 지연 타이머가 없다. RUN과 FAULT는 서로 독립 입력이며 하나를 다른 하나의 반전으로 해석하지 않는다.
- 운전시간 MIN은 Int Add 1, MIN≥60에서 HOUR에 **1을 Move**한다. HOUR 누적 Add가 아니며 별도 T17 조건의 0쓰기도 있다. 실제 누적 DB/기록 완료 ACK는 미확보다.
- HMI RUN은 DB13.X12.3 미러, 알람 주소 대응은 Allarmi_114=DB3.X14.1이다. 이름의 113과 HMI 번호114를 혼동하지 않는다. 화면 문구/버튼 이벤트는 미확보다.
- 공통 근거는 [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md)의 T13/T17·외부 기록 경계, [SYS-PLC-IO](SYS-PLC-IO-DOTS-DRAFT.md)의 HMI 입력 미러 호출/전체 I/O 경계, [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md)의 RESET·알람 Word 표시 경로를 연결 재사용한다. 이 초안의 채널 고유 선언·핀·도면은 독립 대조했다. 기존 CLIENT-CL01 제어명세는 탐색 색인으로만 사용했다.

## 1. 설비·자료 기준 — 적용

- 대장 catalog index57, equipment index59, kind=client, 외부 연동, phase2, 부모 없음. 별칭 motor_client_01/client motor 1/cl01/apron conveyor a. 한 ID 문서초안이며 하위/주변 설비 완료를 함께 집계하지 않는다.
- 고정 원본: gme-research/source-mv06, Git abcf31c5030bc7ef8749ed8e869a857f2387a28a, v1.12.0. 최신 게시·로컬 기능을 검증한 자료가 아니다.
- 아래 네자리 XML 파일명은 all-in-one/sources/decoded-original/ 아래다. doc는 색인 문서번호이며 XML 번호·NID와 다르다. UID/RID는 반드시 해당 파일/블록/NID 문맥에서 결속한다. AO/BO는 비트 오프셋이다.
- 전기도 all-in-one/sources/Electrical_Rev2.pdf. 실제 렌더 4쪽을 의미 검토했다. 원본 표제 DATA 27.05.2024, 각 확인쪽 Rev2 17.03.2025, FG/TOT262를 읽었다. 전체 도면 262장을 전수 검토했다고 주장하지 않는다.
- 작업자 자체 문서 조사, 실행 모델/추론수준의 런타임 증명 미확인. 현재 CPU/TIA/현장/외부 제어반·실운전은 미취득. 원본 build/test/generator·시뮬레이터·PLC/보호값/SEJIN 변경 및 실행 없음.

## 2. I/O·HMI — 적용, 실물·이벤트 미확보

|분류|원본 선언·결속|주소·형식·의미|
|---|---|---|
|원시 RUN|0613 SimpleAccess Global RID2, NID1 UID100, SSD AO99, SAD Input SAM=None|I12.3 Bool. 0292 Contact130 operand W112로 사용. 0558 RID29에도 Monitor UID40 선언이 있으나 이것만으로 외부 프로그램 동작을 확정하지 않음|
|원시 FAULT|0599 SimpleAccess Global RID3, NID1 UID53/55, AO118, Input SAM=None|I14.6 Bool. 0220의 정/반전 접점이 같은 원시 입력을 읽음|
|공통 허가 ON|0599 Global RID1 UID52 AO0 Memory|M0.0 Bool. 명칭 ON을 항상 True 상수로 취급하지 않음|
|래치 알람|0601 GlobalAccess RID5, NID1 UID54/57 Write, AO113; 0600 DepDBBlock RID4 TOD3|Allarm.motor_client_01_fault = DB3.DBX14.1 Bool|
|내부 Reset|0601 Global RID7 NID1 UID56 AO48; 0600 RID6 TOD2|Flag.RESET_ALLARM = DB2.DBX6.0 Bool. HMI 버튼 그 자체와 구분|
|MIN/HOUR|0615 Global RID6/RID10 AO0/16, Int16; 0614 DB TOD9|DB9.DBW0 / DB9.DBW2. MIN UID101/103/104/109, HOUR UID107 및 NID47 UID2591 복수 쓰기|
|계수 타이머·요청|0613 RID1 Timer AO13, RID284 Timer AO17, RID13 Bool Memory AO15|Tag_47=T13, Tag_48=T17, Flag_Aggiorna_DB=M1.7. 물리 입력/HMI Bool로 치환 금지|
|HMI RUN 미러|0627 Global RID19 UID63 Input AO96 Word; 0629 RID20 UID64 Write AO96 BAD4; 0628 DB TOD13|IW12→DB13.DBW12 Word, 그 안 X12.3. 원시 I12.3과 HMI DB13.X12.3은 별도 메모리|
|HMI FAULT 원시범위 미러|0627 RID21 UID65 Input AO112 Word; 0629 RID22 UID66 Write AO112 BAD4|IW14→DB13.DBW14. 해당 Word의 X14.6과 DB3.X14.1 래치 알람은 다름|

hmi_plc_tags.csv 실제행76: APRON_CONVEYOR_A_RUN, DB13,X12.3, PLC, ID00405. 실제행571: Allarmi_114, DB3,X14.1, ID0011B. CSV는 dde.cfg 주소 설정이며 온라인 현재값·화면 애니메이션·알람 메시지 문구·쓰기권한·버튼 이벤트의 증거가 아니다. DB9 전용 HMI 태그 미식별은 공통 SYS-RUNHOURS 검색 근거를 재사용한다.

plc-symbols.csv RUN 설명에는 옛 `e 13.0`, FAULT 설명에는 옛 `e 17.6`이 남아 있으나 실제 선언 AO99/118과 Address I12.3/I14.6 및 도면이 일치한다. 옛 설명을 현재 I/O 주소로 복제하지 않는다. Q61.2는 start client motor 4, Q61.3/4/5/6은 client6/8/9/10으로 명시되어 CL01 근거가 아니다.

## 3. 제어 구조 — 적용, 외부 명령 순서는 미확보

### 3.1 호출·명령 경계

0549/doc1620/Main NID7: Powerrail W352→Contact350.in, ORef335/RID52(0692 ON M0.0)→W348→operand. Contact350.out W351은 CRef319/322/325/328/331/334의 en에 병렬 연결된다. CRef331 Ref80/CodeBlock345 Ref79는 0688 Global FCBlock `Motor/Alarm Client`, TOD9, NID7 UID345 Call. CRef334 Ref83/CodeBlock347 Ref82는 `time work motor`, FC2, NID7 UID347 Call. 0694의 해당 인터페이스 선언과 함께 호출 문맥을 대조했다. 다른 네트워크의 동일 UID와 결합하지 않는다.

따라서 GME FC9의 알람 평가와 FC2의 시간계수는 ON 허가를 공유한다. 이것은 외부 Apron 모터에 START를 보내는 FB 호출이 아니다. 실제 외부 운전요청→허가→접촉기/인버터→응답 순서, Auto/Manual/Local 우선순위, 정지·재기동 및 외부 안전회로는 미확보다. 외부 제어반의 승인도면/프로그램 없이 이를 추정하지 않는다.

### 3.2 RUN→계수: 0292/doc1002/FC2 NID1

- W132 rail→Contact128, W111 ORef99/RID1(T13)→operand, W129→Contact130, W112 ORef100/RID2(I12.3)→operand. Contact130.out W131은 Add82.en과 Ge89.pre에 분기한다.
- Add82 SrcType=Int. W113 ORef101/RID6 MIN→in1, W114 ORef102/RID7 Int1→in2, W115 out→ORef103/RID6 MIN. MIN을 1 증가시키는 산술 쓰기다.
- Ge89 Int: W116 ORef104/RID6 MIN→in1, W117 ORef105/RID8 Int60→in2. out W118→Move92.en.
- Move92.in W120 ORef106/RID7=Int1, out1 W121→ORef107/RID10 HOUR. **HOUR+1 Add가 아니다.**
- Move92.eno W122→Move95.en. W123 ORef108/RID12=Int0→in, W124 out1→ORef109/RID6 MIN. eno W125→SCoil98.in, W126 ORef110/RID13 M1.7→operand.
- literal은 0616 RID7 V1, RID8 V60, RID12 V0로 직접 확인했다. 정적 연결·형식과 실제 CPU 순서/ENO 성공·오버플로·retention은 구분한다. 특정 한 시간에 정확히 1회 전달됐다는 실행 증거는 없다.

### 3.3 HOUR 다른 쓰기·타이머

0332/doc1045/FC2 NID47: ORef2589/RID284 T17→W2600→Contact2615, out W2616→Move2574.en. ORef2590/RID12 Int0→W2601→in, out1 W2602→ORef2591/RID10 CLIENT_MOTOR_1_HOUR. 뒤 채널은 Move2574.eno W2603에 연결되지만 CL01은 첫 Move다. HOUR를 평생 누적계로 설명하지 않는다.

공통 0019/doc1056/NID58은 NOT T13(Contact3120, W3118)→W3121→SdCoil3112, value W3117 ORef3114/RID335=S5T#1M, operand W3119 ORef3116=T13이다. 0341/doc1055/NID57은 ON·M1.7로 M2.0을 Set하고, M2.0·NOT M1.7 조건에서 T17에 S5T#5S를 넣으며 T17로 M2.0 Reset한다. 이 타이머는 계수/기록 핸드셰이크 소유이며 CL01 기동 지연·FAULT 지연이 아니다. 상세 공통 핀은 SYS-RUNHOURS 연결을 재사용한다. 외부 M1.7 Clear·영구 기록 완료는 미확보다.

### 3.4 HMI 미러 Word 전달

0397/doc1070/NID1: W21 rail→Move60.en, W70 ORef63/RID19 IW12→in, W72 out1→ORef64/RID20 DB13.DBW12. Move60 DisableENO=true와 W71 eno→Move61.en이 함께 존재한다. W73 ORef65/RID21 IW14→Move61.in, W75 out1→ORef66/RID22 DB13.DBW14. 비트별 Coil로 읽지 않으며 RUN Bool 자체를 출력으로 쓰는 동작이 아니다. HMI Inputs FC15의 호출경계·다른 비트의 별도 NOT 쓰기 등은 SYS-PLC-IO 참조이며 이번 두 Word 경로를 독립 확인했다. 모든 DB13 비트가 무조건 원시와 동일하다고 일반화하지 않는다.

## 4. 전기 전달 경로 — 적용, 외부 반 내부·케이블 미확보

|경로|실제 렌더 확인|전달 끝점·접점|판정 경계|
|---|---|---|---|
|RUN 외부 접점|FG88 / PDF89, DIGITAL INPUT FROM CLIENT MACHINE, Rev2 17.03.2025|+24Vdc10.7(87/9→89/0)→5x20 2A F 표시 X1:284→선88.1→도면상 열린 접점→X1:285→E12.3, 교차참조128/4|Apron A 채널 포함 전체 점선 SPARE. 외부 접점 장치번호/케이블 번호·설치상태 미확보|
|RUN PLC측|FG128 / PDF129, DIGITAL INPUT MODULE, Rev2 17.03.2025|E12.3, 상부88/1→도면 단자4, CPU515/MOD11 표기|현행 CPU가515라고 확정하지 않음. 해당 입력도 SPARE 범위|
|FAULT 외부 접점|FG91 / PDF92, DIGITAL INPUT FROM CLIENT MACHINE, Rev2 17.03.2025|+24Vdc10.7(90/9→92/0)→5x20 2A F 표시 X1:322→선91.5→도면상 열린 접점→X1:323→E14.6, 교차참조130/6|Apron A FAULT 채널 점선 SPARE. 정상시 신호값·고장접점 논리/배선실물 미확보|
|FAULT PLC측|FG130 / PDF131, DIGITAL INPUT MODULE, Rev2 17.03.2025|E14.6, 상부91/7→도면 단자27, CPU515/MOD11 표기|SPARE 표시. 원시 I14.6 명칭과 도면 대응, 실물 미확인|

2A·5x20은 백업 도면 표기이고 현행 보호설정·교체품 사양의 확인이 아니다. 도면의 열린 접점 그림으로 현장 정상극성이나 fail-safe를 단정하지 않는다. 이 회로에는 CL01 부하용 릴레이의 5/9 접점 또는 하단1/5/9 표가 식별되지 않았다. 타 설비의 릴레이 경로를 복제하지 않는다. 모터 주전원·차단기·접촉기/인버터·과부하·실제 회전검출은 외부 제어반 자료가 필요하다.

자료 탐색상 electrical-page-text의 FG86~95 범위와 Apron 명칭을 확인하되, 본문 의미 확인은 위 4쪽으로 한정했다. 시공도 텍스트에서 Apron 직접 대응은 미식별이며 모든 시공페이지를 시각 검증했다는 뜻은 아니다. PDF83/84/85는 경계 탐색용 렌더만 만들었고 직접 검토 4쪽 실적에 포함하지 않았다.

## 5. 알람·복구 — 적용, 현장 복구 미확보

0220/doc410/FC9 NID1 원본:
- W75 rail→Contact67, ORef52/RID1 ON→W58→operand. Contact67.out W68이 Contact69와 반전 Contact71의 in에 병렬 분기한다.
- ORef53/RID3 FAULT→W59→Contact69.operand; Contact69.out W70→SCoil46.in, ORef54/RID5→W61→operand. 식은 ON AND I14.6 → DB3.X14.1 Set.
- ORef55/RID3 동일 FAULT→W62→Contact71.operand, PinName=operand Negated. W72→Contact73.in; ORef56/RID7 RESET_ALLARM→W63→operand; W74→RCoil51.in, ORef57/RID5→W65→operand. 식은 ON AND NOT I14.6 AND DB2.X6.0 → 동일 알람 Reset.
- FC9 이 고유 네트워크는 Contact/SCoil/RCoil뿐이며 타이머 Part가 없다. ON 불성립 시 이 네트워크의 S/R 조건은 성립하지 않는다. 원시 FAULT가 내려가도 Reset 조건을 따로 만족해야 래치를 지우는 구조다.
- 공통 알람 관리자·ACK·RESET 요청·HMI Word 표시는 SYS-ALARM 연결을 재사용한다. 알람이 모터 출력을 직접 끊는 전체 경로, 현장 E-stop, 외부 모터 재기동 허가와 복구 성공은 이 네트워크만으로 확정할 수 없다.

원시 FAULT, 내부 래치, HMI 주소의 수치, Reset 요청과 실제 외부 고장 해소를 별도로 기록한다. Reset/강제비트/점퍼/퓨즈교체/보호값 변경 절차를 제시하지 않으며, 원인 제거·안전확인·재운전 승인 및 실물 복구는 현장 권한자 증거가 필요하다.

## 6. 증상별 관찰 — 적용, 조치·실행 없음

|증상|읽기 전용 동시 관찰|원본 비교·추가 증거|
|---|---|---|
|Apron A 미운전|외부 반 모드/명령 표시와 시각, I12.3, HMI DB13.X12.3|GME 전용 출력 미식별이므로 외부 기동회로/실물 명판/승인도면부터 필요. RUN=0만으로 모터/센서 고장 확정 금지|
|현장은 운전, RUN 표시 없음|X1:284/285 식별자료·I12.3·DB13.X12.3·드라이버 상태의 동시 기록|SPARE 채널의 실제 사용 여부, 접점/케이블 대응과 미러 호출을 구분. 현장 계측은 별도 승인된 담당자 자료만 사용|
|FAULT 경보 유지|I14.6, M0.0, DB2.X6.0, DB3.X14.1, HMI Allarmi_114와 시각|FAULT 복귀만으로 래치 Reset되지 않는 0220 조건. 정상극성/물리 고장·배선단절은 외부도면 없이 결정 불가|
|HMI RUN만 다른 값|원시 I12.3, DB13.DBW12 및 X12.3, 화면/태그 ID00405, 프로젝트판본|Word 미러와 화면 갱신/통신을 분리. Bool 주소와 옛 e13.0 주석 혼용 여부 확인|
|운전시간 MIN 불변|T13, I12.3, FC2 호출 ON, DB9.DBW0|0292 en/pre와0019 타이머 비교. 실제 샘플링 주기·정전 retention 미확인|
|HOUR가0/1로 반복|DB9.DBW2, MIN, M1.7/M2.0/T17, 외부 기록시각|Move1/Move0 구조. 외부 영구 누적·ACK 없이는 시간 손실/정상 여부 확정 불가|

관찰서 항목: 관찰자, 날짜/시간대, 자료 취득 방법, 프로젝트/CPU 근거, 주소/값/단위, 설비·접점·단자 사진 위치, 비교원본 FG/PDF·XML/NID/핀, 배제/미배제 원인, 승인된 조치와 별도 복구 증거. 이번 작업에 실제 운영/정비 기록을 만들거나 공개 복제하지 않았다.

## 7. 완료·누락 — 문서 초안 complete_with_gaps

|영역|상태|남은 경계|
|---|---|---|
|설비·자료 기준|적용|실제 Apron A 동일성·SPARE 사용 미확인|
|I/O·HMI|적용/일부 미확보|RUN·FAULT·미러·래치·시간 선언 확인, 화면 이벤트/명령 출력 미식별|
|제어|적용/외부 미확보|FC9/FC2 및 고유 핀 확인, 외부 시퀀스/실행순서 미검증|
|전기|적용/외부 미확보|4쪽 실제 렌더, 외부 반 내부·케이블·모터 보호/전력 미확보|
|알람·복구|적용/현장 미확보|Set/Reset 식 확인, 실제 원인 해소·재기동 미확인|
|증상 관찰|적용|수집 계획이며 실제 측정/행동시험 아님|
|완료 기준|적용|부모 독립 검토·전달 후 자료 없는 경계 보류|

- documentation: complete_with_gaps. static_review: scoped_complete(자체 핵심 대조; 부모 독립검토 전). ui_records: not_run. publication: not_published. tia_compile/live_cpu/field_recovery: not_performed.
- 네 기능: 도면·래더 비교는 위 근거로 적용 가능하나 UI 검증 없음. 백업/선택 복원·전후 기록 비교·보고서/PDF 기능은 필요성과 원본·미지필드 보존 요구만 남기며 구현/저장/재읽기/복구 시험을 수행하지 않았다. 전달물은 이 MD 초안이다.
- 다음 한 작업: 부모 독립 검토 후 초안 전달. 신규 자료가 생기면 외부 제어반 승인도면과 단자/케이블/명판으로 SPARE 사용·START 경계·RUN/FAULT 정상극성을 대조한다. 없는 자료를 반복 검색해 현장 완료로 바꾸지 않는다.

### 실제 시각·검사 범위

- 2026-10-11 12:12:16 UTC 착수 지시 수신·범위 읽기 시작.
- 12:12:24 UTC 고정 Git HEAD/dirty 및 원본 시작지침 확인.
- 12:12:46 UTC 고유0220/0292 XML 파싱·핀 확인.
- 12:13:18 UTC 실제 PDF89/92/129/131 렌더·시각 검토.
- 12:14:13 UTC 전용 출력 심볼 경계 확인, 이후 호출·HMI·계수 공통근거/고유핀 대조 및 초안 작성.
- 최종 정적 검사 시각: 2026-10-11T12:17:24.709418+00:00. 검사·해시 JSON은 extracts/CLIENT-CL01에 보관.
- 선정 원본 25파일 SHA256 및 고정 Git blob 내용 일치 확인. 이 수는 전수 의미검토·전체 설비 완료 수가 아니다. 핵심 의미검토는 위 7개 FlgNet의 해당 경로·관련 선언과 도면4쪽, HMI/심볼 선정행이다. 전체 다른 채널 네트워크·외부 제어반은 미해석 경계로 남긴다.

### 선정 원본 SHA256 전체 표

모든 경로는 source-mv06 기준. Git blob 열은 고정 abcf31c의 객체 ID이며 내용일치는 파일 바이트와 git show 결과를 비교했다.

|원본 경로|SHA256|고정 Git blob|내용 일치|
|---|---|---|---|
|docs/equipment-standard/INVENTORY.json|720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc|587c3748ad9224718f95ba06463fee913dae231d|일치|
|all-in-one/sources/Electrical_Rev2.pdf|5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6|f610fd7c7ce14ae951b00cff57b969259bfb389d|일치|
|all-in-one/sources/hmi_plc_tags.csv|a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404|cf4c0650e7c7baac350dcb89909b808435704880|일치|
|all-in-one/registers/plc-symbols.csv|a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f|cbc576c5d6e47498a3865304a1c23de9b4641d9f|일치|
|all-in-one/sources/decoded-original/0220-FlgNet.xml|fd7e4305dcd4fd489fa4fe59ea960e848d38cdb837ae94a6e3ecc690c3d0340b|b237efa898c299cbe730686d036b3f49a229dc8c|일치|
|all-in-one/sources/decoded-original/0292-FlgNet.xml|dd1db2302f796dcd00d675f904dc2b23418dcba0530367ef23d343828a1f07fc|c8d9f9026125be35f0a3b92547e82316c848321e|일치|
|all-in-one/sources/decoded-original/0332-FlgNet.xml|c677499004010aba2746412a08e32f3e4206e9212d481fc08ee1c6023326cef7|50e3451e01b63fb9311aade1c4bfefa0719d305b|일치|
|all-in-one/sources/decoded-original/0397-FlgNet.xml|bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834|4ab8370493c4e28fc1eabeeebe2743d27f0c4021|일치|
|all-in-one/sources/decoded-original/0549-FlgNet.xml|49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1|985b5310b43b1015b5dee286aa0e42800564b94b|일치|
|all-in-one/sources/decoded-original/0019-FlgNet.xml|a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5|f78cfdbf5e717304114660ffbd3bb42cbed6d79d|일치|
|all-in-one/sources/decoded-original/0341-FlgNet.xml|e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96|45dbda06a692b21380a52207a22094b2e0a9c5a3|일치|
|all-in-one/sources/decoded-original/0558-IdentXmlPart.xml|45d49d53b6b41312960bb2a329663e87d8803e28d7832308424a6bf5091e6d1b|a0b681bd15e9ae15f2e1437576a4486cc732fdf2|일치|
|all-in-one/sources/decoded-original/0599-IdentXmlPart.xml|32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1|493de77fc827d8f14192ced05d82df3a062f7965|일치|
|all-in-one/sources/decoded-original/0600-IdentXmlPart.xml|20c58ee0383d0b6c275bd2d96abd30af7c5d1f3fff59c7d5034cd758936b57d5|f22a7ededd0576cf379ee19908da067f08d45412|일치|
|all-in-one/sources/decoded-original/0601-IdentXmlPart.xml|04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862|07bcf656fa58e4a305999456644acd24b3dc6bec|일치|
|all-in-one/sources/decoded-original/0613-IdentXmlPart.xml|09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb|c9d19a48e947098914f4d2de3348c05b4f6d37e8|일치|
|all-in-one/sources/decoded-original/0614-IdentXmlPart.xml|c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294|da0485aa033700f08c8695d30b93ebd2d377d6c7|일치|
|all-in-one/sources/decoded-original/0615-IdentXmlPart.xml|80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a|49eb86fe01feb83de8c0864b21493d305aff8b20|일치|
|all-in-one/sources/decoded-original/0616-IdentXmlPart.xml|650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d|9f7fdd5f93ac149c139a054ebb34f63c632ef7fd|일치|
|all-in-one/sources/decoded-original/0627-IdentXmlPart.xml|08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb|61ebc0abbb2ca160e11e1da400a3f14a397d8bc5|일치|
|all-in-one/sources/decoded-original/0628-IdentXmlPart.xml|9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd|170ca5c72599edc7ea7eefe651c3680ce325e76a|일치|
|all-in-one/sources/decoded-original/0629-IdentXmlPart.xml|67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972|058129bb01e27f7a6a0d0293f332d745e5bab74e|일치|
|all-in-one/sources/decoded-original/0688-IdentXmlPart.xml|ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda|463585759f1ecd94f32362b4fefb000a152f5773|일치|
|all-in-one/sources/decoded-original/0692-IdentXmlPart.xml|bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037|737785d03b5fad43c5b4d451955726d800edb1c0|일치|
|all-in-one/sources/decoded-original/0694-IdentXmlPart.xml|757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d|c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d|일치|
