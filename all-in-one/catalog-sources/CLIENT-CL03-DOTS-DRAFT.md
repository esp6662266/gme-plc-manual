# CLIENT-CL03 — Impact vibration feeder 자체 조사 초안

고정 기준: abcf31c5030bc7ef8749ed8e869a857f2387a28a / v1.12.0. 조사 대상 1개, CLIENT-CL03. 신규 통합·게시·PLC 시험 결과가 아니다.

## 먼저 확인할 핵심

- 직접 확인: RUN I12.5, FAULT I15.0의 Global 선언, FC9 NID3 경보 S/R, FC2 NID3 시간 처리, DB13 Word 미러와 HMI 태그, 외부 접점·PLC 단자 4쪽 실제 렌더.
- CL03 전용 기동/정지 출력은 아래 한정 명명 검색에서 선언·쓰기·도면 연결을 확보하지 못했다. 이 결과를 ‘외부 설비에는 명령이 없다’고 확대하지 않는다. CL04의 Q61.2나 LIW/BWF 출력은 CL03에 배정하지 않는다.
- 중요 경계: 전기 FG88/92와 FG128/131 해당 채널은 SPARE 점선 표시가 있다. 이름이 남은 예비 설계와 실제 설치·사용 여부는 별도 확인이다.
- 상충/주의: PLC 심볼 설명에는 과거 E13.2 RUN/E18.0 FAULT가 남지만 선언의 실제 주소와 Rev2 도면은 I12.5/I15.0이다. 둘을 임의 통합하지 않는다. 시간 HOUR는 `+1`이 아닌 `Move 1`; 이후 별도 `Move 0` 쓰기가 있다.
- 공통 근거 재사용: [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md)의 FC2 타이머·외부 갱신 경계, [SYS-PLC-IO](SYS-PLC-IO-DOTS-DRAFT.md)의 입력 미러, [SYS-HMI](SYS-HMI-DOTS-DRAFT.md)의 이벤트 미확정, [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md)의 공통 ACK/Reset/Word 보고를 같은 고정 입력에서 연결 재사용했다. 이 문서의 CL03 고유 선언·핀·PDF는 독립 확인했다.
- 누락: 외부 제어반 원도면·접점 장치/단자명·현행 케이블·실제 기동 명령·모터/드라이브 명판·HMI 이벤트·현재 프로젝트/CPU·정상 극성·운전/복구 관찰.

## 1. 설비·자료 기준 — 적용

INVENTORY.json catalog[59]의 ID는 CLIENT-CL03, 이름 Impact vibration feeder, kind client, group 외부 연동, 부모 없음, phase2/planned다. 백업 기호는 `IMPACT VIBRATIONFEEDER RUN/FAULT`, `Allarm.motor_client_03_fault`, `hours motors.CLIENT_MOTOR_3_MIN/HOUR`다. 공압 CYL-CL03이나 아날로그 `Data.client_3`(BWF01 level)와 다른 이름 공간이다. feeder라는 단어만으로 LIW/BWF와 합치지 않는다.

이 문서의 범위는 GME 측 외부 상태 수신·경보 유지·운전시간 데이터와 HMI 전달이다. 외부 모터 내부 기동·보호·진동 설정·안전 인터록은 미확보다. 부모/하위 부품을 함께 완료로 집계하지 않는다.

원본 경로 접두어: XML은 `all-in-one/sources/decoded-original/`; 도면은 `all-in-one/sources/Electrical_Rev2.pdf`; HMI는 `all-in-one/sources/hmi_plc_tags.csv`. 원본 저장소는 읽기 전용으로 유지했다. 실제 실행 모델/추론 런타임 증명은 미확인이다. TIA 추가 접근·사용자 컴퓨터 접근은 수행하지 않았다.

## 2. I/O·HMI — 적용, 화면 이벤트·실물 미확정

### 2.1 주소와 선언 결속

|대상|원본 선언 / NID·RID·UID|주소·형식·소유|
|---|---|---|
|IMPACT VIBRATIONFEEDER RUN|0613 RID20 NID3 UID208, SAD Input AO101 SAM=None|Global Bool I12.5, 입력영상. 실제 움직임 증명과 다름|
|RUN 모니터 참조|0558 RID31 NID -2147483648 UID43 AK Monitor AO101|Global Bool I12.5; 제어 출력 쓰기가 아님|
|IMPACT VIBRATIONFEEDER FAULT|0599 RID10 NID3 UID89/91 AO120|Global Bool I15.0; 전용 고장 원시 입력|
|motor_client_03_fault|0601 RID11 NID3 UID90/93 Write AO115 BAD4, 0600 RID4 TOD3|Global Bool DB3.DBX14.3, Set/Reset 유지 경보|
|RESET_ALLARM|0601 RID7 NID3 UID92 AO48 BAD6, 0600 RID6 TOD2|Global Bool DB2.DBX6.0; 공통 내부 Reset 요청|
|ON|0599 RID1 NID3 UID88 Memory AO0|Global Bool M0.0. 이름만으로 상시1 가정 금지|
|CLIENT_MOTOR_3_MIN|0615 RID22 NID3 UID209/211/212/217 AO64 BAD5, 0614 RID5 TOD9|Global Int DB9.DBW8; Add 및 Move0의 복수 쓰기|
|CLIENT_MOTOR_3_HOUR|0615 RID24 NID3 UID215, NID47 UID2595 AO80 BAD5|Global Int DB9.DBW10; Move1과 Move0|
|Tag_47 / Tag_48|0613 RID1 Timer AO13 / RID284 Timer AO17|T13 / T17; HMI Bool 또는 CL03 고장 지연 타이머가 아님|
|Flag_Aggiorna_DB|0613 RID13 Bool Memory AO15, NID3 UID218 Write|M1.7 공통 갱신요청|

위 핵심 대상은 Global이다. Local 변수·다른 블록의 같은 UID와 합치지 않았다. AO/BO는 bit offset이며 DB 번호는 DepDBBlock.TOD로 확인했다.

### 2.2 입력 Word 미러와 HMI

0397-FlgNet.xml doc1070/NID1: Move60에는 rail W21→en, ORef63/RID19→W70→in, out1→W72→ORef64/RID20. 0627 RID19는 Global Word Input AO96(SAM=None)=IW12, 0629 RID20 Global Word AO96 BAD4 및0628 RID4 TOD13=DB13.DBW12다. 별도 Bool 코일이 아니라 두 byte Word 복사이며 I12.5는 DB13.X12.5와 대응하는 범위다.

같은 망 Move60.eno→W71→Move61.en, ORef65/RID21→W73→in, out1→W75→ORef66/RID22. 0627 RID21 Input Word AO112=IW14, 0629 RID22 Word AO112 BAD4=DB13.DBW14. 이 범위는 I15.0을 포함한다. Move60/61 `DisableENO=true` 표시와 실제 ENO 연결을 모두 보존하며 실행 성공·다른 Writer 부재·현재 최종값을 추정하지 않는다. IW를 PIW 직접주변 접근으로 표기하지 않는다.

HMI CSV 실제행78 `IMPACT_VIBRATIONFEEDER_RUN`, Access PLC, ID00403, `DB13,X12.5`; 실제행573 `Allarmi_116`, ID00119, `DB3,X14.3`. 이는 저장된 dde.cfg 주소 설정이다. RUN 표시와 경보 표시는 원시 입력/유지 bit가 서로 다르다. CSV만으로 위젯, 사용자 쓰기 권한, 알람 메시지 문구, ACK 이벤트, 통신 성공을 확정하지 않는다. DB9 관련 HMI 미결속은 SYS-RUNHOURS의 동일 원본 검색을 연결 재사용한다.

명명 검색 범위: plc-symbols.csv, all-networks.csv, decoded-original의 IdentXmlPart 전체에서 impact vibration, motor_client_03, client_motor_3, start client motor 3/motore 3을 대조했다. 고유 RUN/FAULT/경보/시간 선언은 위와 같고 CL03 전용 start 출력 선언·대응 Coil/Call은 미확보다. 문자열 검색은 간접 주소·전체 제어 부재를 증명하지 않는다.

## 3. 제어 구조 — 적용

### 3.1 실제 호출 경계

0549-FlgNet.xml doc1620/Main NID7: rail W352→Contact350.in, ORef335/RID52(0692 ON M0.0)→W348→operand. Contact350.out의 W351은 CRef319/322/325/328/331/334.en으로 병렬 분기한다.

CL03 경보의 호출 소유는 CRef331 RefId80 / CodeBlock345 RefId79. 0688 FCBlock RID79 NID7 UID345 Call TOD9=`Motor/Alarm Client` FC9, 0694 BlockInterfaceInfo RID80 NID7 UID331 TORID79와 결속된다. 시간은 CRef334 RefId83 / CodeBlock347 RefId82, 0688 TOD2 FC2 `time work motor`, 0694 RID83 TORID82다. 단일 모터 FB 인스턴스를 임의로 만들지 않는다. FC9/FC2 호출은 앞 블록 ENO 직렬 허가가 아니라 ON의 병렬 허가다. 현재 scan 주기/최종 실행 순서는 온라인 미검증이다.

### 3.2 CL03 운전시간 원형: 0294/doc1004/FC2 NID3

1. ORef207/RID1 T13→W219→Contact236. ORef208/RID20 I12.5→W220→Contact238. 두 접점은 W237 직렬, W239가 Add190.en과 Ge197.pre로 분기한다.
2. Add190 SrcType Int: W221 ORef209/RID22(DB9.W8)→in1, W222 ORef210/RID7(Int1)→in2, W223 out→ORef211/RID22(DB9.W8). MIN에 1을 더한다.
3. Ge197 SrcType Int: W224 ORef212/RID22 MIN→in1, W225 ORef213/RID8(Int60)→in2. Ge.out W226→Move200.en.
4. Move200.in W228 ORef214/RID7=Int1; out1 W229→ORef215/RID24 DB9.W10. **HOUR+1 누적 Add가 아니라 1을 쓰는 Move**다.
5. Move200.eno W230→Move203.en; W231 ORef216/RID12=Int0→in; out1 W232→ORef217/RID22 MIN을0으로 쓴다. Move203.eno W233→SCoil206.in; W234 ORef218/RID13 M1.7 갱신요청 Set.

0616 literal RID7/8/12의 원형은 각각 Int1/60/0이며 NID3 UID210/214,213,216과 대조했다. MIN 연산/비교·ENO의 실제 실행/overflow·외부 저장 소비는 관찰하지 않았다.

### 3.3 시간 초기화·공통 타이머 경계

0332/doc1045/FC2 NID47: ORef2589/RID284 T17→W2600→Contact2615, out W2616→Move2574.en. 앞 CLIENT1/2 Move2574/2577의 ENO 체인이 W2603/W2606을 지나 CL03 Move2580.en에 들어온다. W2607 ORef2594/RID12 Int0→2580.in, out1 W2608→ORef2595/RID24 DB9.W10. 따라서 CL03 HOUR는 T17 조건과 앞 Move ENO 체인에 의존하는 별도 0쓰기다. MIN 리셋과 HOUR 초기화를 혼동하지 않는다.

공통 타이머는 SYS-RUNHOURS를 연결 재사용하며 핵심 원형도 대조했다. 0019/doc1056/NID58: NOT Contact3120(T13, W3118)→W3121→SdCoil3112, value W3117/ORef3114 RID335 S5Time S5T#1M, operand W3119/ORef3116 T13. 자기 재허가 구조이며 정확한 실제 60초 샘플링 시험 결과가 아니다.

0341/doc1055/NID57: ON→M1.7 조건은 M2.0을 Set한다. M2.0 및 NOT M1.7 경로 Contact3151/3153→W3154→SdCoil3118; value W3138/RID334 S5T#5S, operand W3141/RID284=T17. T17 Contact3155→W3156→RCoil3123(M2.0). 이 망에는 M1.7 Reset Coil이 없다. 외부 갱신 ACK·영구 누적 writer는 미확보다. T13/T17을 CL03 기동 지연·고장 필터로 전용하지 않는다.

### 3.4 명령·출력 소유

직접 확보한 CL03 경로는 외부 RUN/FAULT 접점→입력/DB 미러→FC9 경보 및 FC2 시간이다. 이 채널 전용 start/stop Coil, 주회로 접촉기·인버터·전용 속도 설정·재기동 sequence는 미확보다. 공통 consent나 주변 BWF/LIW 출력은 외부 연동 전체의 후보 경계일 뿐 CL03 명령으로 확정하지 않았다.

## 4. 전기 전달 경로 — 입력 경로 적용, 외부 구동 경로 미확보

실제 원본 PDF 4쪽을 pdftoppm으로 렌더하여 확인했다. 아래 모든 페이지 footer는 DATA27.05.2024 / Rev2 17.03.2025 / TOT262다. PDF 파일명 Rev2만으로 개정란을 추정하지 않았다.

|실제 PDF / FG|독립 확인한 CL03 경로·끝점|경계|
|---|---|---|
|PDF89 / FG88, DIGITAL INPUT FROM CLIENT MACHINE|+24Vdc10.7(87/9→89/0)→X1:288, 5×20 2A F 표기→선88.3→열린 접점 그림→X1:289→E12.5, 상호참조128/5|IMPACT VIBRATION FEEDER RUN. 전체 외부 접점군 SPARE 점선. 외부 장치 단자·접점번호/릴레이번호 없음|
|PDF129 / FG128, DIGITAL INPUT MODULE|상호참조88/4→E12.5→모듈 단자6, CPU515/MOD11 표기|CL03 끝점은6. 인접 E12.4 단자5를 복제하지 않음. 해당 부분 SPARE 점선|
|PDF93 / FG92, DIGITAL INPUT FROM CLIENT MACHINE|+24Vdc10.7(91/9→93/0)→X1:326, 5×20 2A F→선92.2→열린 접점 그림→X1:327→E15.0, 상호참조131/2|IMPACT VIBRATION FEEDER FAULT. SPARE 점선, 외부 실제 정상 극성 미확인|
|PDF132 / FG131, DIGITAL INPUT MODULE|상호참조92/3→E15.0→모듈 단자31, CPU515/MOD11|SPARE 점선. 같은 페이지 +24V10.7→X21:3013 5×20 2A IST→선131.1→단자39, -0V10.6→40 표기. 설계 module supply와 현재 보호설정 구별|

외부 접점은 그림상 열린 접점이지만 그것이 실제 정상운전·전원차단·단선 상태에서 어떤 값인지는 확정하지 않는다. 이 경로는 릴레이 부하5/9 회로가 아니며 1/5/9 번호를 발명하지 않는다. CL03 자체 출력 릴레이·접점 부하 경로가 확보되지 않았다.

원본 도면에서 양 끝점이 확인되는 범위는 X1 외부 접점 표현↔GME DI module이다. 외부 캐비닛 제조사/실장도·접점 장치 고유번호/정상상태·현행케이블번호·모터 정격·보호기 설정·현장 결선은 이 자료로 확인되지 않는다. 시공본의 동일 실물 대조도 완료로 표기하지 않는다. 모듈의 CPU515 표기는 도면 정보이며 현재 설치 CPU 식별이 아니다.

## 5. 알람·복구 — 적용

0222-FlgNet.xml doc412/FC9 NID3의 원형:

- rail W111→Contact103.in. W94 ORef88/RID1 ON→operand. Contact103.out W104가 Contact105 및 Contact107.in으로 분기한다.
- Set 가지: W95 ORef89/RID10 I15.0→Contact105.operand, Contact105.out W106→SCoil82.in; W97 ORef90/RID11 DB3.X14.3→operand. **ON AND I15.0이면 경보 Set**.
- Reset 가지: W98 ORef91/RID10 I15.0→Contact107.operand, 이 접점은 Negated다. Contact107.out W108→Contact109.in; W99 ORef92/RID7 DB2.X6.0→109.operand; out W110→RCoil87.in, W101 ORef93/RID11 DB3.X14.3→operand. **ON AND NOT I15.0 AND RESET_ALLARM이면 경보 Reset**.
- 이 고유 네트워크에는 Timer Part가 없다. 고장 지연 시간을 다른 모터에서 복제하지 않는다. ON=0이면 이 두 가지는 모두 허가되지 않는다. 외부 원인 소멸과 내부 래치 해제·HMI ACK·기동은 별개다.

HMI `Allarmi_116=DB3.X14.3`은 이 유지 bit와 결속한다. 공통 경보 Word/ACK/Reset 전파는 SYS-ALARM 고정입력 분석을 연결 재사용하며 CL03 고유 비트가 속한 DBW14 범위와 구별한다. 공통 Word/초기화·간접 Writer까지 단일 S/R 두 개만으로 완전히 폐쇄한 것은 아니다. 이 경보가 외부 feeder를 물리적으로 정지시키는 전용 출력 경로는 미확보다.

복구 완료는 이 문서로 판정하지 않는다. 원시 FAULT 상태와 외부 원인, 내부 유지 bit, Reset 실제 전달, 외부 재기동 허가, RUN 및 기계 상태를 현재 프로젝트·승인 절차에서 별도 대조해야 한다. 보호값·우회·강제·재가동 조작은 제시하지 않는다.

## 6. 증상별 관찰 — 적용, 실제 수리·시험 미수행

|증상|같은 시각으로 확보할 관찰|자료 비교와 미확정|
|---|---|---|
|움직이는데 HMI RUN 없음|외부 접점 상태/실제 동작 근거, X1:288/289, I12.5, IW12, DB13.W12/X12.5, HMI00403|FG88→128/6→0397 Move60→CSV 경계 비교. 현장 측정은 승인 자격자·절차 필요; 그림/비트만으로 기계 정상 판정 금지|
|고장 표시가 남음|I15.0, DB3.X14.3, M0.0, DB2.X6.0, HMI00119·이벤트 시각|0222 Reset에는 NOT I15.0와ON이 모두 필요. 외부 고장 미복귀와 Reset 미도달을 분리|
|외부 FAULT 표시와 PLC가 다름|X1:326/327 접점·현재 외부 도면, DI31 I15.0, 원시/DB 미러/래치|극성·설치 여부·통신 미확정. SPARE 표기를 확인 없이 실제 미사용으로 확정하지 않음|
|시간이 증가하지 않거나1→0 반복|T13, I12.5, DB9.W8/W10, M1.7, M2.0, T17, FC2 호출·외부 수집 로그|0294 Move1 및0332 Move0/ENO 확인. HOUR를 장기 누적계라고 가정하면 오판 가능|
|시작 명령을 못 찾음|현재 외부 캐비닛 I/O handshake, 명판·케이블 식별, 승인 원도면/프로젝트|CL03 출력은 현 확보 자료 미결속. CL04 Q61.2 또는 BWF 명령을 대입하지 않음|

관찰 기록에는 관찰자, 시각/시간대, 위치, 값·단위, 수집장치, 프로젝트/도면 판본, 비교 원본, 배제 결과, 실제 조치와 복구 증거를 각각 남긴다. 이 조사에는 실제 관찰값·사용자 운영기록·현장사진이 없다.

## 7. 완료 기준·누락 — 문서 범위 완료, 현장 보류

|영역/상태|판정|
|---|---|
|documentation|complete_with_gaps: CLIENT-CL03 7영역 초안|
|static_review|selected_evidence_reviewed: 고유0222/0294/0332 및 호출0549, 입력0397, 공통0019/0341 핵심과 선언 대조. 전체 PLC 의미 검토 아님|
|전기 자료|PDF89/93/129/132 실제 렌더 확인. 다른 페이지 전체 의미 검토·실물 확인 아님|
|ui_records|not_run; 도면·래더 비교, 선택 백업/복원, 전후기록, 보고서 기능은 이번에 구현·시험하지 않음|
|publication|not_published; 부모 전달용 초안이며 최신 사이트 기능 검증 아님|
|tia_compile / live_cpu / field_recovery|모두 not_performed|

다음 필요한 자료는 외부 feeder 제어반 승인 회로/I/O 목록과 현행 GME–외부 handshake, X1:288/289·326/327의 케이블/상대단자·접점 장치·정상상태, 현행 모터/드라이브 명판, 현재 PLC 프로젝트 및 HMI 이벤트·외부 시간 수집 writer다. 새 자료 없이 현장 보류를 반복 검색하거나 실물 완료로 바꾸지 않는다.

자체 정적 점검은 `extracts/CLIENT-CL03/checks.json`, 선언 발췌는 `declarations-selected.json`, 파생 네트워크 색인은 `network-index.json`, 실제 단계 시각은 `stages.json`에 있다. 검색/선정 파일수는 각 파일 전체의 의미 검토 완료수가 아니다. 시뮬레이터·원본 build/test/generator·PLC·현장·보호값·SEJIN·공통코드 변경/실행은 하지 않았다. 원본 Git working tree 변경 없음.

## 부록 A. 선정 원본 SHA256 및 고정 Git blob 내용 일치

선정 원본 27개. 아래 SHA256은 각 전체 파일 bytes, Git blob은 고정 커밋의 객체 ID다. 일치는 작업 파일 bytes와 git show 고정 blob bytes를 직접 비교한 결과다. 대장/색인은 탐색 근거이며 원형 XML·PDF와 같은 의미검토 수준으로 세지 않는다. 공통 원본730/중지5 전체 보존의 부모 점검과 이 선정표는 별도다.

|원본 경로|SHA256|고정 Git blob|내용 일치|
|---|---|---|---|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|true|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|true|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|true|
|`all-in-one/registers/plc-symbols.csv`|`a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f`|`cbc576c5d6e47498a3865304a1c23de9b4641d9f`|true|
|`all-in-one/registers/all-networks.csv`|`7b6a9fc46f56c1bec7c4c7136792e2fc470fd07c15aa885d4f411c478d5e5f7c`|`cd54feb06ebcbea0c56ccb1226707799be084e16`|true|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|true|
|`all-in-one/sources/decoded-original/0019-FlgNet.xml`|`a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5`|`f78cfdbf5e717304114660ffbd3bb42cbed6d79d`|true|
|`all-in-one/sources/decoded-original/0222-FlgNet.xml`|`710729f55b7b1085f1bd61cd02e4c814f3e79c8754abfb391cea432a4b3e448c`|`09b816d05646159a80b26b220c96889878c3dc97`|true|
|`all-in-one/sources/decoded-original/0294-FlgNet.xml`|`f18d17accd996e443a738b8bb23065f328b0a5548a561f5402178533b583d53b`|`6aae006614d815a4e332717e2b3d55db64a9b0a3`|true|
|`all-in-one/sources/decoded-original/0332-FlgNet.xml`|`c677499004010aba2746412a08e32f3e4206e9212d481fc08ee1c6023326cef7`|`50e3451e01b63fb9311aade1c4bfefa0719d305b`|true|
|`all-in-one/sources/decoded-original/0341-FlgNet.xml`|`e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96`|`45dbda06a692b21380a52207a22094b2e0a9c5a3`|true|
|`all-in-one/sources/decoded-original/0397-FlgNet.xml`|`bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834`|`4ab8370493c4e28fc1eabeeebe2743d27f0c4021`|true|
|`all-in-one/sources/decoded-original/0549-FlgNet.xml`|`49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1`|`985b5310b43b1015b5dee286aa0e42800564b94b`|true|
|`all-in-one/sources/decoded-original/0558-IdentXmlPart.xml`|`45d49d53b6b41312960bb2a329663e87d8803e28d7832308424a6bf5091e6d1b`|`a0b681bd15e9ae15f2e1437576a4486cc732fdf2`|true|
|`all-in-one/sources/decoded-original/0599-IdentXmlPart.xml`|`32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1`|`493de77fc827d8f14192ced05d82df3a062f7965`|true|
|`all-in-one/sources/decoded-original/0600-IdentXmlPart.xml`|`20c58ee0383d0b6c275bd2d96abd30af7c5d1f3fff59c7d5034cd758936b57d5`|`f22a7ededd0576cf379ee19908da067f08d45412`|true|
|`all-in-one/sources/decoded-original/0601-IdentXmlPart.xml`|`04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862`|`07bcf656fa58e4a305999456644acd24b3dc6bec`|true|
|`all-in-one/sources/decoded-original/0613-IdentXmlPart.xml`|`09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb`|`c9d19a48e947098914f4d2de3348c05b4f6d37e8`|true|
|`all-in-one/sources/decoded-original/0614-IdentXmlPart.xml`|`c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294`|`da0485aa033700f08c8695d30b93ebd2d377d6c7`|true|
|`all-in-one/sources/decoded-original/0615-IdentXmlPart.xml`|`80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a`|`49eb86fe01feb83de8c0864b21493d305aff8b20`|true|
|`all-in-one/sources/decoded-original/0616-IdentXmlPart.xml`|`650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d`|`9f7fdd5f93ac149c139a054ebb34f63c632ef7fd`|true|
|`all-in-one/sources/decoded-original/0627-IdentXmlPart.xml`|`08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb`|`61ebc0abbb2ca160e11e1da400a3f14a397d8bc5`|true|
|`all-in-one/sources/decoded-original/0628-IdentXmlPart.xml`|`9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd`|`170ca5c72599edc7ea7eefe651c3680ce325e76a`|true|
|`all-in-one/sources/decoded-original/0629-IdentXmlPart.xml`|`67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972`|`058129bb01e27f7a6a0d0293f332d745e5bab74e`|true|
|`all-in-one/sources/decoded-original/0688-IdentXmlPart.xml`|`ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda`|`463585759f1ecd94f32362b4fefb000a152f5773`|true|
|`all-in-one/sources/decoded-original/0692-IdentXmlPart.xml`|`bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037`|`737785d03b5fad43c5b4d451955726d800edb1c0`|true|
|`all-in-one/sources/decoded-original/0694-IdentXmlPart.xml`|`757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d`|`c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d`|true|
