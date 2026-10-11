# PSH01 압력 측정 채널 — 원본 조사 초안

## 핵심 확인·상충·인계

- PSH01은 원본 전기 FG75/PDF76의 **4–20mA 아날로그 계기**다. 이름 PSH만으로 고압 디지털 스위치·안전기능으로 규정하지 않는다. 원시 입력은 `%IW284`; 환산 호출은 `:P / SAM=Peripherie`, HMI 원시값 미러는 `SAM=None`이다.
- 환산 목적지는 `Data.Press_PC01` **DB1.DBW134**, HMI 원시 미러는 `Inputs.PSH_01` **DB13.DBW48/Word**다. `PC01 %IW322 → Data.PC_01`이나 레시피 `PSH01_SETPOINT`와 동일 값이 아니다.
- **파생 색인 누락 발견:** sensor-measurement.json의 PSH01 value_reads=[]와 달리 원본 `0668 NID3 UID112/RID32`에 Press_PC01 참조, `0669 NID3 UID119→NID4 UID200`에 Local Real_PC01 쓰기/읽기, `0476 W225`에 CONT_S.PV_IN 연결이 있다. 따라서 사용처가 없다고 쓰면 안 된다. STL 명령 순서 자체는 live_index `_7ex/doc6` 보충 근거이며 별도 복원 STL XML은 확보하지 못했다.
- 관련 CONT_S는 `PID_MV-02 DB23`, 출력은 `M14.0/14.1`이다. 이 메모리와 Q1.5/Q1.6을 구분한다. 하류 `0343`의 선두 **NOT ON Part310**과 추가 NOT ON312를 보존한다. 현행 활성·CPU 호출·물리 밸브 동작을 단정하지 않는다.
- 시공 케이블 `7_7 =FLA+HE01-PSH01A`: PDF30 관로표 **2심**, PDF57 케이블표 **4S/예비1**로 상충한다. 준공도/실물 확인 전 한쪽으로 정리하지 않는다.
- OEM FG75 footer는 27.05.2024, 별도 개정 표기 미관찰. FG107/PDF108은 같은 기본일자와 **Rev2 17.03.2025**를 직접 판독했다. P&ID 판I 15/01/2013의 PSH01 `+2÷+5 mBar`는 당시 표기이며 현행 설정이 아니다.
- 독립 재확인: PSH01 원시/환산/알람 선언, 0495·0398·0476·0343 핵심 핀, 전기2쪽·시공2쪽·P&ID1쪽 실제 렌더. 공유 재사용: BF01 초안 §3/§5의 0291·0014 공통 환산, 0030 HMI 호출 경계. 공유 소스는 같은 고정 커밋으로 확인했고 PSH01 결속은 따로 대조했다.
- 남은 우선 확인: 원본 STL 명령 재복원 또는 승인된 TIA 읽기 결과, 현재 호출/모드·HMI 이벤트, 현행 계기/채널·스케일/극성/단자, 케이블 심수 충돌. 새 현장 자료 없는 보류를 반복 조사하지 않는다.

## 작업 기준·범위

- GME-STD-1.0.0, catalog PSH01, sensor/계측, parent 없음, depth0, priority 없음. INVENTORY catalog[4], equipment[90], 별칭 psh_01. 같은 이름 PSH02/03을 병합하지 않는다. HE01 및 MV02는 관련 위치/루프이며 catalog 부모 또는 이번 완료 대상이 아니다.
- 배정: TASK3-BATCH05-SCOPE.json, GME-CATALOG-OVERLAP-REVIEW.json의 PSH01. 신규132 자체조사 중 한 개 문서 초안이며 로컬 2차133 통합 제외 유지.
- 고정 원본 `gme-research/source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION 1.12.0. 시작 Git status 빈 출력. 현재 main·CPU·실물과 동일함을 뜻하지 않는다.
- AGENTS, 스킬, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, EXPANSION-WORK, VERSION, WORKSPACE-HANDOFF, PUBLICATION_STATUS, ACTIVE-WORK 최신 항목, START-GPT61, source-map 읽음. 배정 지시의 병렬·문서전용 제한을 따른다. 원본 스크립트/preflight/build/test/generator 실행 없이 자체 XML 파싱·해시·PDF 렌더만 수행했다.
- 실제 모델명/추론수준의 런타임 증명 미확인. 로컬 TIA 추가접근권한 없음. Windows/TIA/PLC/시뮬레이터 사용 없음.
- 쓰기 범위: `drafts/PSH01-DOTS-DRAFT.md`, `extracts/PSH01/`만. 원본·타 초안·공용 추출·코드·버전·대장·배포·운영기록·SEJIN 변경 없음. 원본 및 중지5자산 해시 보존. 재위임 및 Work/Codex 생성 없음.
- 아래 경로는 달리 명시하지 않으면 고정 원본의 `all-in-one/` 아래. 4자리 번호는 `sources/decoded-original/####-FlgNet.xml` 또는 IdentXmlPart.xml. document_id와 원본 NID를 구분한다.

## 7영역 적용표

| 영역 | 상태 | 확보 | 미확정 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | 독립 ID, MV02/HE01 관계, 도면 판본 | 현행 실물 동일성 |
| I/O·HMI | 적용/일부 미확보 | IW284:P/일반 IW, DB13 Word, DB1/4/3 주소, HMI7행 | 이벤트·표시 단위·권한·현재값 |
| 제어 구조 | 적용/일부 미확보 | 환산→Local Real→CONT_S→M14.0/1→하류 Q경계 | STL 원문 전체·현재 호출·복수 Writer 최종값 |
| 전기 전달 | 적용 | PSH01 ±, X1, PEW284, MOD3, 케이블7_7 | 현재 모듈·실제 배선·심수상충 |
| 알람·복구 | 적용/일부 미확보 | OFR bit, 범위 판정·ENO·0/−9999 경계 | 화면 경보·공통 Word 영향·실제 복구 |
| 증상별 관찰 | 적용 | 관찰 항목/비교 근거/원인 배제 | 실제 측정·조치·재기동 없음 |
| 완료·누락 | 적용 | 해시/정적 확인과 운영 검증 분리 | 통합/UI/게시/TIA/CPU/현장 |

## 1. 설비·공정·자료 시점

P&ID `sources/PID_1684n002I.pdf` p1 실제 전체 및 PSH01 확대 렌더에서 AB01 출구측 MV05/TC07 경로와 CM02/MV02 분기, PSH01 계기 표기를 확인했다. MV02에는 M16/LS17/LS18/ZT03이 따로 그려져 있다. PSH01 표기와 MV02의 위치관계는 자료 사실이지만 센서 압력탭·밸브·구동기 실물 일치의 증명은 아니다. HE01이라는 시공 LOC와 PLC 변수 Press_PC01이라는 소프트웨어 명칭도 서로 다른 분류다.

P&ID footer: 도번1684n002, 원작성06/04/2011, 판I 변경15/01/2013. PSH01의 SetPoint `+2÷+5 mBar`, 전기도의 계기범위 `0/10 mbar`, 소프트웨어 Int 값은 각 자료층을 따로 보관한다. PLC 정수에 배율이 있다고 가정해 20=2mbar 등으로 환산하거나 운전·보호값을 추천하지 않는다.

전기도의 `P-BADR` 표기를 기록하되 현행 제조사·정확한 모델·압력방식(게이지/차압/절대)·내압·접액재료·교정범위로 확대하지 않는다. 최신 명판과 제조사 매뉴얼, 승인된 계기목록 및 교정성적서는 미확보다.

## 2. I/O·HMI·형식 구분

### 2.1 직접 선언

| 항목 | 선언 주소/형식 | 원본 결속 | 해석·경계 |
|---|---|---|---|
| PSH01 환산 입력 | Input Int %IW284, Peripherie | 0678 RID96 SSD.AO2272, NID15 UID444, SAD.SAM=Peripherie | :P 접근; HMI 입력복사와 동일 시점 보장 없음 |
| PSH01 HMI 원시 입력 | Input Int %IW284, SAM=None | 0627 RID79 AO2272 NID2 UID100 | 프로세스 이미지 접근 선언, :P로 바꾸지 않음 |
| Inputs.PSH_01 | Word DB13.DBW48 | 0629 RID81 AO384/BO384 BAD4→0628 Inputs TOD13, NID2 UID101 AK=Write | Word16비트 복사, Bool/환산압력 아님 |
| Coeff.COEFF_PSH01 | Int DB4.DBW38 | 0676 RID97 BO304 BAD8→0674 Coeff TOD4, NID15 UID445 | 보정계수, 현행 설정 미확인 |
| Coeff.ZERO_PSH01 | Int DB4.DBW36 | 0676 RID98 BO288 BAD8, NID15 UID446 | 영점, 단위/승인값 미확인 |
| Data.Press_PC01 | Int DB1.DBW134 | 0676 RID99 BO1072 BAD11→0674 Data TOD1, NID15 UID447 Write | PSH01 환산 출력; 별도 PC01 입력의 Data.PC_01 아님 |
| Allarm.PSH01_OFR | Bool DB3.DBX22.0 | 0676 RID385 AO176 BAD354→0674 Allarm TOD3, NID15 UID23 Write | 환산 범위오류 bit, 공정 고압 trip 의미로 확대 금지 |
| Data.PSH01_SETPOINT | Int DB1.DBW32 | 0642 RID96 BO256 BAD80, NID1 UID3722 Write; 0668 RID30 BAD1→0666 Data TOD1, NID3 UID100 read | 레시피·HMI 설정 경로와 센서 실측 구분 |
| Real_SPPC01 | Local Real, BO160 | 0669 RID31 NID3 UID107 Write / NID4 UID199 read | SP_INT 입력, 별도 물리 주소 없음 |
| Real_PC01 | Local Real, BO192 | 0669 RID33 NID3 UID119 Write / NID4 UID200 read | PV_IN 입력, Global PC01과 동일성 혼동 금지 |
| PID MV02 UP / Down | Bool M14.0 / M14.1 | 0670 RID43/44 AO112/113, NID4 UID208/209 Write | 내부 PID 요청; 물리 출력 및 실제 방향 아님 |
| Open MV02 / Close MV02 | Bool Q1.5 / Q1.6 | 0617 RID25/24 AO13/14, NID2 UID259/267 Write | PSH01 관련 하류 경계로만 확인; MV02 완료 아님 |
| Flag.MV02_Auto | Bool DB2.DBX6.7 | 0668 RID34 AO55 BAD6→0666 Flag TOD2, NID4 UID195 | NOT 접점으로 CONT_S.COM_RST에 연결 |
| Inputs.MV02 Open/Close | Bool DB13.DBX7.3/7.4 | 0668 RID121/122 AO59/60 BAD118→0666 Inputs TOD13 | NOT로 LMNR_HS/LS에 연결, 정상 실물 극성 미확인 |

Global/Local/Constant는 이름만으로 결정하지 않고 ID.S, SSD, SAD, BAD와 DepDBBlock.TOD를 대조했다. 추출기의 NID/UID/RID 후보 충돌은 자동 확정하지 않았다. 예: 0476 ORef208에 무관한 0690 Word_outputs 후보도 나오지만 이 블록 소유 선언0670과 원문 색인에 따라 PID MV02 UP으로 결속한다. 0343 ORef249의 무관한0585 Start_Burner 후보도 사용하지 않는다.

### 2.2 원시 미러와 호출 경계

`0398` document1071/NID2: Powerrail W21→Move96.en, ORef100/RID79→in W109, out1 W111→ORef101/RID81. **IW284 Int→DB13.DBW48 Word**이며 스케일 계산은 이 Move에 없다. Move96 DisableENO=true, eno W110→Move97.en도 존재한다. Move96은 앞 Move의 ENO 뒤가 아니라 rail 병렬 가지다.

상위 HMI 호출 `0030` document1613/NID19는 Recipes Handler→HMI→HMI Output의 ENO W32/33 뒤, Part37의 NOT Simulation(1) W42/44/43을 거쳐 HMI Inputs 호출로 연결된다. BF01 초안의 동일 고정 원본 호출 경계를 재사용했고 원본 연결도 확인했다. 호출이 구성되어 있다는 사실과 현재 활성/매 스캔 갱신은 다르다. 중지 simulation 코드의 실행·시험은 하지 않았다.

### 2.3 HMI 주소 일치 7행

`sources/hmi_plc_tags.csv`는 모두 Access Name PLC, 근거 문구 `dde.cfg 설정; 온라인 현재값 아님`이다.

| CSV행 | HMI 태그 | 설정 주소 | ID | 역할 |
|---|---|---|---|---|
|65|Editor_PSH01|DB26,INT16|00411|레시피 편집 버퍼 후보, 직접 실측 아님|
|205|Coeff_DB4_DBW36|DB4,INT36|002CC|영점 주소|
|223|Coeff_DB4_DBW38|DB4,INT38|002B9|계수 주소|
|279|Allarmi_214|DB3,X22.0|0026C|OFR bit 주소|
|282|data_DB1_DBW32|DB1,INT32|00269|운전 setpoint 저장부 주소|
|310|data_DB1_DBW134|DB1,INT134|00247|환산 압력 주소|
|743|I_PSH_01|DB13,INT48|00054|PLC Word 저장부를 HMI INT로 참조|

INT48 HMI 표현과 PLC Word 선언 차이를 보존한다. 태그 CSV만으로 화면 입력/출력 방향·버튼 이벤트·쓰기 권한·통신품질·소수점·mb 배율·경보 표시문을 확정하지 않는다.

`0554` RID30은 RecipesDB.Recipes 배열 요소의 PSH01을 Monitor로 참조하며 AO128(16byte)다. `0642` RID98은 Recipes[0].PSH01 읽기, RID96은 PSH01_SETPOINT 쓰기 선언이다. `live_index _7ev/doc364` SCL 색인에는 `(Recipes[0]=Recipes[HMI_index]) AND vis_loadrecipe AND load_recipe` 아래 `Data.PSH01_SETPOINT := RecipesDB.Recipes[0].PSH01`이 있다. 이는 저장/선택 레시피 조건의 보충 근거이며 CSV 태그 쓰기만으로 바로 센서값이나 현재 PID SP가 바뀐다는 뜻이 아니다. 원본 SCL 전체·HMI 이벤트 결속은 추가 확인 대상이다.

## 3. 제어·환산·루프 경계

### 3.1 PSH01 고유 환산 호출

`0495` document1745/NID15를 독립 대조했다. Part455 Contact operand←ON ORef442/RID1 W449, rail W457, out W456→CRef436.en. 별도 IN0←ON ORef443 W450. ON=%M0.0 선언이며 이름만으로 상시 TRUE를 가정하지 않는다.

CRef436 RefId351, CodeBlock448 RefId5. `0672 FCBlock RID5` TOD63=Signal linearization/FC63, `0680 BlockInterfaceInfo RID351`에서 방향/형식을 확인했다.

| CRef436 핀 | Wire | ORef/RID | 결속/방향 |
|---|---|---|---|
|Analog_input|451|444/96|PSH01 Int Input :P|
|Coeff|452|445/97|COEFF_PSH01 Int Input|
|Zero|453|446/98|ZERO_PSH01 Int Input|
|OutValue|454|447/99|Data.Press_PC01 Int Output/Write|
|Out_of_range|24|23/385|PSH01_OFR Bool Output/Write|

별도 timer/S/R는 이 네트워크에 없다. EN/IN0를 둘 다 ON에 묶은 구조와 호출 함수 내부 동작을 구분한다.

### 3.2 공통 FC63 환산 재사용 및 직접 확인

BF01 초안의 공통 `0291` document1658/NID1와 `0014` document1659/NID2를 연결 재사용하되 PSH01 핀 결속은 위 표로 독립 확인했다. 아래 원본 형식/경계도 정적 대조했다.

- `0291` IN0 아래 Int 비교 `Analog_input > -1382 AND <=32767`: Gt258/Le161. Int→DInt Convert164(입력), Convert167(Zero), Add170, Convert174(Coeff), Mul177, Div181(`/28000`), Move185→OutValue의 ENO 연쇄 W227/230/234/237/241/245이다.
- 산술 요약은 `(DInt(raw)+DInt(Zero))*DInt(Coeff)/28000`, 이후 Int OutValue로 쓰기다. 이것은 원본 수식 요약이지 실수 연산·현재 스케일·mbar 변환 검증이나 overflow/절삭 동작시험이 아니다.
- 범위 밖은 Gt190 `>32767` 또는 Le259 `<=−1382`, OR47 W35/48/49→Move193. ORef218/RID21(0612 literal−9999) W252→in, out1 W253→OutValue ORef219. Move193.eno W21→일반 Coil23, operand W22→Local Out_of_range RID26(0611)이다.
- OFR를 S/R 래치·지연타이머로 오독하지 않는다. ENO에 연결된 일반 Coil이라는 범위까지만 확정한다. Int 상한32767과 비교식 `>32767`도 원문 그대로 보존하며 무조건 발생 가능한 독립 fault로 바꾸지 않는다.
- `0014` NOT IN0 Part171(W168)→Move162.en W172, literal0 ORef166/RID23(0612) W169→in, OutValue ORef167/RID19(0611) W170→out1. **0값은 정상 압력의 독립 증거가 아니며 IN0 해제 경계 쓰기일 수 있다.** 이 네트워크는 Out_of_range를 직접 쓰지 않는다.
- ON 때문에 외부 en이 꺼지면 내부 NOT IN0 분기를 반드시 수행한다고 가정할 수 없다. 호출되지 않았을 때 잔류값/현재 실행 의미는 TIA/CPU 검증 미수행이다.

### 3.3 Press_PC01 → Local Real → PID_MV-02

1. `0668 GlobalAccess RID32`: Data.Press_PC01 BO1072, NID3 UID112. `0669 InterfaceAccess RID33`: Real_PC01 Local Real BO192, NID3 UID119 AK=Write, NID4 UID200 read. SP는 0668 RID30 PSH01_SETPOINT UID100→0669 RID31 Real_SPPC01 UID107 Write/199 read다.
2. `live_index _7ex/doc6` 제목 “controll pc01 moduling mv02 - converts values into real”의 STL 색인은 `L Data.PSH01_SETPOINT; ITD; DTR; T #Real_SPPC01; L Data.Press_PC01; ITD; DTR; T #Real_PC01`을 표시한다. **명령순서의 출처는 검색 색인**이며 직접 선언만으로 ITD/DTR 전체 실행이나 CPU 주기를 검증했다고 하지 않는다.
3. `0476` document `_7ex/7`, NID4, LRef172/RID113 CONT_S(0671) 및 Instance210/RID38(0665 PID_MV-02, TOD23). W224 ORef199/RID31→SP_INT, W225 ORef200/RID33→PV_IN. Local 값을 PID 호출에 넣는 핀 연결은 직접 XML 근거다.
4. en은 Part245 ON(ORef194/RID17 W211/246). COM_RST는 Part247 **NOT Flag.MV02_Auto**(ORef195/RID34 W212/248). LMNR_HS는 Part249 **NOT Inputs.MV02 Open**(ORef196/RID121 W213/250), LMNR_LS는 Part251 **NOT Inputs.MV02 Close**(ORef197/RID122 W214/252). NOT을 제거하거나 실제 리미트 정상극성으로 해석하지 않는다.
5. QLMNUP W239→ORef208/RID43 M14.0, QLMNDN W240→ORef209/RID44 M14.1. PID.MV02의 출력은 아직 물리 Q가 아니다.
6. `0667` 상수와 핀을 직접 결속한 **백업 호출 상수**: CYCLE100ms RID21/W223; GAIN−0.22 RID39/W228; TI2s RID40/W229; DEADB_W Real2.0 RID22/W230; PULSE_TM200ms RID25/W235; BREAK_TM2s500ms RID41/W236; MTR_TM18s RID42/W237; DISV Real1.0 RID24/W238. 현행 tuning/보호설정/승인주기로 전환하지 않는다. 시간들은 Time이며 S5Time과 구분한다.
7. RefId 없는 ORef215/217/219/221/226/231/233/241/243가 LMNS_ON/LMNUP/LMNDN/PVPER_ON/PV_PER/PV_FAC/PV_OFF/PV/ER에 연결돼 있다. 빈 참조를 임의 FALSE/0/1·현재값으로 채우지 않는다. 라이브러리 내부 CONT_S 알고리즘·실행 조건 및 실제100ms 태스크 설정은 추가 검증 대상이다.

**색인 상충의 결론:** sensor-measurement.json은 LAD FlgNet만 중심으로 value_reads를 수집한 결과로 보이나 원인을 확정하지 않는다. 원본 Global/Local 참조와 CONT_S 핀 증거가 있으므로 value_reads=[]를 “읽는 곳 없음/미사용 채널”로 인용할 수 없다. 파생 파일은 수정하지 않았다.

### 3.4 하류 방향명령 경계

`0343` document1704, 지도 index_order3이지만 원본 **NID2**다. 블록 valve control loop 제목 “mv02 controlled by psh-01”. Part310 **NOT ON** ORef28/RID1(W27), rail W356→310.in, out W311→Part326 및 Part312. Part326은 **NOT MV02_FAULT**(ORef251/RID22 W283)이다. 이 선두 조건을 없애고 PID가 항상 Q를 구동한다고 설명하지 않는다.

- OPEN 가지: `(MV02_Auto AND PID MV02 UP) OR M_MV02_OPEN`를 OR221(Part328/330/332, W329/331/333)로 묶고, 이어 `(MV WORK PULSE OR ON)` OR222(334/336, W335/337), NOT Close MV02 Part338(W292), Inputs.MV02 Open Part340(W293), Coil227→Open MV02 ORef259/RID25 W295. Q1.5 쓰기다.
- CLOSE 가지: `(MV02_Auto AND PID MV02 Down) OR M_MV02_CLOSE` OR234(342/344/346 W343/345/347), `(MV WORK PULSE OR ON)` OR235(348/350 W349/351), NOT Open MV02 Part352(W304), Inputs.MV02 Close Part354(W305), Coil240→Close MV02 ORef267/RID24 W307. Q1.6 쓰기다.
- 수동기억 리셋 쪽은 별도 Part312 **NOT ON**까지 직렬이며, OR199→RCoil203 M_MV02_OPEN, OR206→RCoil210 M_MV02_CLOSE가 있다. 일반 출력 Coil과 수동기억 RCoil을 구분한다.
- 이 문서는 원본의 해당 방향 쓰기 경계를 확인한 것이며 MV02 전체 Writer/전기 구동/현행 동작 검증이나 복구 지침 완료가 아니다. 두 NOT ON을 근거로 현재 비활성이라고도 단정하지 않는다. ON의 현재값·상위 호출·다른 Writer가 미확인이다.

## 4. 전기·단자·케이블 양 끝점

### 4.1 OEM 전기도 직접 렌더

`sources/Electrical_Rev2.pdf` PDF76=FG75, 제목 PRESSURE CONTROL, footer27.05.2024, 별도 개정 표시 미관찰.

- PSH-01 상자: OUTPUT4–20mA, P-BADR, 0/10mbar. 제목 “PRESSURE CONTROL OUTPUT MV-02”의 OUTPUT은 계기/공정 설명이며 PLC 아날로그 출력으로 분류하면 안 된다.
- 공급: +24Vdc10.7(74/9→76/0)→X1:172, 5×20 **50mA F** 표기→PSH01 `+`. 신호: PSH01 `−`→X1:173→+PEW284(107/4). 실드: X1:174→75SCH1(107/3), 접지기호/차폐를 신호 음극과 동일 회로로 합치지 않는다.
- PDF108=FG107 ANALOG INPUT MODULE. footer27.05.2024와 Rev2 17.03.2025를 실제 판독. PSH01은 CPU515/MOD3/PEW284, **I6+ terminal30**, U6−/I6− terminal32와 공통−0Vdc10.6 경로. Uv6=29, U6+=31 표기도 따로 있다. 75SCH1은 실드 경로다.
- 모듈 공통 공급은 +24Vdc10.7→X21:3001 5×20 **500mA F**→L+ terminal41/42, M43/44. 계기50mA와 모듈500mA를 섞지 않는다. 도면 표시의 CPU515/MOD3가 현장 CPU/모듈의 현행 모델 증명은 아니다.
- FG75의 PEW284 참조107/4, 75SCH1 참조107/3과 FG107의 75/2 역참조를 보존한다. FG와 실제 PDF쪽은 이번 두 쪽에서만 대응 확인했으며 전체 PDF-1 규칙으로 일반화하지 않는다.

### 4.2 시공도·케이블 상충

`sources/Electrical_Can_Decoating_20241118.pdf` 두 페이지를 실제 렌더했다.

| PDF | 도번/페이지 | 직접 표기 | 판본/경계 |
|---|---|---|---|
|30|CANDC-CONS-E013-030, D-PAGE13, 30/64|FLOW_A ZONE05, device9 PSH01, HE01, Flexible16, 7_7=FLA+HE01-PSH01A, CVV-S1.0, core2|Rev1 24.11.11 first draft design, checked/approved 공란|
|57|CANDC-CONS-C007-057, D-PAGE7, 57/64|7_7 CR→HE01 PSH01, AI, CVV-S4S1.0, spare1, route100/110LAD1/E900, Adjustment7/LEN52|Rev1 24.11.11 first draft design, checked/approved 공란|

2심과4S 표기는 문서 간 상충이다. 설계계획/시공자료라는 범위를 유지하며 52를 실측 케이블 길이로 확정하지 않는다. p57의 다른 FLO2TB1 회로를 PSH01 중간단자로 추가하지 않는다. OEM X1:172/173/174와 시공7_7의 연결은 태그·기능 수준 대응이며 심선색/접속마킹의 직접 일치는 미확보다.

계기 극성 `+ / −` 및 입력단자 표기는 도면상의 전기 끝점이다. 정상 압력 방향, 안전 fail state, 현장 접점 정상극성 또는 분리/단락 시험 허가는 아니다. 회로를 연결·단락·강제하거나 보호퓨즈/스케일을 바꾸지 않았다.

## 5. 알람·영향·복구 경계

직접 확인된 전용 알람은 PSH01_OFR(DB3.DBX22.0) 환산 범위출력이다. 0495 output pin과 0676 AK=Write, 공통0291의 일반 Coil/ENO가 근거다. 전용 지연·S/R·고압 trip은 해당 PSH01 환산 네트워크에서 확인되지 않았다. **전용 회로에서 미발견**을 시스템 전체 경보·정지 영향 없음으로 확대하지 않는다. 공통 알람 Word 읽기, HMI 표시·ACK·siren 및 외부 장치 영향은 별도 검증이 필요하다.

−9999는 범위오류 분기 저장값이며 압력 실측이 아니다. 0 역시 NOT IN0 분기와 구분해야 한다. OFR 해제 또는 표시 숫자 정상화만으로 센서 교정·단자 복구·밸브 구동·공정 안정·안전 재기동 완료를 선언할 수 없다.

복구 확인은 승인된 절차와 자격 있는 담당자가 계기·전원·루프·배선·채널·프로젝트 일치 자료를 확보한 뒤 판단해야 한다. 여기서는 운전 조작·계수수정·강제출력·리셋·현장시험을 수행/지시하지 않는다. ON/IN0/호출·raw/환산/OFR·Local Real/PID 요청·Q명령을 같은 시각 증거로 구분해 모으는 것이 다음 문서 조사 단계다.

## 6. 증상별 관찰 기록안

실제 운영 관찰을 새로 만들지 않았다. 각 기록은 관찰자, 실제시각/시간대, 위치, 장치/프로젝트판본, 원시값/형식/단위, 비교근거, 배제결과, 승인조치, 이후복구증거를 별도로 남긴다.

| 증상 | 읽기 전용 관찰·비교 위치 | 섞지 않을 것/원인 배제 | 필요 증거 |
|---|---|---|---|
| HMI 원시값과 환산압력 다름 | IW284 일반/:P, DB13W48, DB1W134, DB4W36/38, 0398/0495 | 접근시점·Word/INT 표현·계수·호출 차이를 먼저 분리 | 승인된 동시각 trace, 스케일/단위 설정 |
| −9999/OFR 표시 | DB3X22.0, DB1W134, FC63 enable, raw범위, 0291 | 수치만으로 단선/계기고장/고압을 확정하지 않음 | 채널진단·교정/명판·승인된 루프 측정기록 |
| 값이0 또는 고정 | ON/en/IN0, 0014, HMI 통신시각 | NOT IN0의0쓰기·미호출 잔류·실제0압력 구분 | 호출/업데이트 상태 및 독립 기준계 |
| 압력은 변하나 MV02 응답 다름 | Real_PC01/SPPC01, CONT_S COM_RST/HS/LS, M14.0/1, 0343의 NOT ON/FAULT/리미트/반대명령, Q1.5/1.6 | PID 요청=Q명령=실제개도 아님, Q만으로 기계 원인 판정 금지 | 현재 프로그램/모드·MV02 현장 응답 별도자료 |
| 레시피 변경 후 SP 다름 | Editor_PSH01 DB26W16, load/vis 조건, DB1W32 | 편집버퍼와 적용setpoint·센서실측 구분 | 승인 HMI 이벤트/레시피 적용시점 |
| 도면·현장 채널 다름 | X1:172/173/174, PEW284 I6+30, 케이블7_7 | p30 core2와 p57 4S 상충 임의 해소 금지 | 최신 준공단자표·케이블표·명판/식별사진 |

## 7. 완료 상태·누락·다음 한 작업

- 문서: `draft_ready_with_gaps`. 본문의 7영역, 고유 핵심·공유근거·상충·미확정 포함.
- 정적 검토: 자체 원본 XML/선언·핀 확인, PDF 실제5쪽 및 확대 판독, SHA256/Git blob 내용 비교. 외부 독립검토는 부모 단계로 남긴다. 해시 일치 개수는 의미검토 개수가 아니다.
- 핵심 고유 의미검토: 0495 전체, 0398 PSH01 Move96 가지, 0476 PID_MV02 호출 핀, 0343 관련 방향/조건. 공유 의미 재확인: 0291/0014 환산 경계, 0030 호출, 0031 호출구조 참고. 8개 추출 XML이 각각 설비 전체 의미완료를 뜻하지 않는다.
- UI/기록·네 기능: 도면/래더 비교는 문서 대응만, 백업/선택복원·기록전후비교·관찰 보고서/PDF는 PSH01 제품통합/저장/재읽기/재열기 **not_run**. 추출 PNG는 조사증거이며 제품 보고서 기능 검증이 아니다. 기존 note/repair_observation·미지필드·타설비·저장키를 변경하지 않았다.
- publication `not_published`, tia_compile/live_cpu/field_recovery `not_performed`. 기존18불일치/1060확인대기/577설계시험을 완료나 실행으로 바꾸지 않는다.
- 미실행: 원본 build/test/generator, 시뮬레이터 작성/수정/실행/행동시험, PLC/현장/보호값/SEJIN변경, 운영기록입력, 배포 및 로컬 통합 모두0.
- 다음 한 작업: 부모 독립 검토에서 **0668/0669→0476 결속과0343 NOT ON**을 우선 대조하고 파생 value_reads 누락을 인계한다. 실물 보류는 최신 STL/준공/계기/HMI자료가 생길 때만 재개한다. 원초안 전달 후 보강 필요 시 별도 보강본으로 보존한다.

## 실제 작업 단계 시각 (UTC)

| 시각 | 실제 수행 |
|---|---|
|2026-10-11 10:28:43|배정 지시 읽기·착수|
|10:28:50–10:29:00|표준/범위/고정Git·최신 인계 읽기|
|10:29:25–10:29:54|원본 선언 파싱, Press_PC01 읽기 누락 발견·추가 루프 탐색|
|10:30:02–10:30:48|PID 호출 핀 및 전기·시공·P&ID5쪽/확대 실제렌더 판독|
|10:31:12–10:32:56|환산/하류 방향/상수/시공 상충 대조, 추출·초안 정리|

## 근거 파일 SHA256 및 고정 Git blob 일치 목록

아래 목록은 선택한 원본·파생탐색·맥락·보존 파일이다. 압축백업/PLF/중지5자산은 해시만 확인하며 실행하거나 전체 의미검토한 것이 아니다. `extracts/PSH01/source-hashes.json`에 크기·역할·Git blob의 SHA256·바이트일치 여부를 보관한다. `network-evidence.json`의 단순 UID/RID 후보는 본문 블록소유 대조와 함께 사용한다.

최종 자체 정적검사 실제시각: 2026-10-11T10:37:51.286277+00:00. 선택 파일 57개 SHA256/Git blob 내용 일치, 중지5자산 freeze일치, 원본 Git 변경0, 정적단언 13/13.

| 파일 | SHA256 | 고정 Git blob OID |
|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` |
| `all-in-one/registers/sensor-measurement.json` | `4b8c357c803e7b429766d54a87bf49bb5dd25343a9797b44b5702df93440c7a3` | `e032d23b1f3163dcf95390589c93e2e9dcda474e` |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | `653d27572de6beedcf3eb6c95702bb119a8b567f` |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` |
| `all-in-one/sources/decoded-original/0343-FlgNet.xml` | `a2f41d7cce7c4d944f0cebdcacc964a1298962198a20f9471558902b39685d68` | `a882a5b83ff68c500114dd48e15397a35ee8c454` |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` |
| `all-in-one/sources/decoded-original/0476-FlgNet.xml` | `0f9c48dddf61987d61094de9368ab534b56ec6c30e898dc2e4d81b64e86fa55a` | `6201c68a4d81417c8aa970bdcc7de6dea3899260` |
| `all-in-one/sources/decoded-original/0495-FlgNet.xml` | `0ff8eb8cf4b147a9077e5bcd88620216cea558cdf2cbb2c336c07b91014abfa4` | `5d6b0e2317f783bd7c8b077f524235b893e446d6` |
| `all-in-one/sources/decoded-original/0554-IdentXmlPart.xml` | `4ae3e7d0bca0f78c9e94617abeb70bdd228d85d74bff2224174fa1bb0076e78c` | `cdb68b35a7287f6b5636c01ea3a01747d3d60e81` |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | `9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e` |
| `all-in-one/sources/decoded-original/0618-IdentXmlPart.xml` | `0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c` | `9eec0dbd8abde4aa7295f77b63ad473f895f274b` |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | `11f0502c84a1f319a21459a35c0dc1c6ce8e8f36` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` |
| `all-in-one/sources/decoded-original/0640-IdentXmlPart.xml` | `2873e2c70eb4ce97c104b00b675c8f800a3ab9621f9d382718428d2d82025379` | `5b899bd63cac30e700a26932a3ffe889ecad8769` |
| `all-in-one/sources/decoded-original/0641-IdentXmlPart.xml` | `75c1f81d659331b8b62578f766e2f0336276caaf086201fdc383e61c195d01df` | `341bca78929061ab73560dd85fef3f4000127782` |
| `all-in-one/sources/decoded-original/0642-IdentXmlPart.xml` | `c922483c261c8ddb98c239a7b4dc3d7f73f9a45261dd5b4d669f39d6918a1c21` | `398f73b99c4a792a68387485fcb47048d166b2a1` |
| `all-in-one/sources/decoded-original/0665-IdentXmlPart.xml` | `50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd` | `ea4a8a5013081f648722c5ebbde3bb1366787990` |
| `all-in-one/sources/decoded-original/0666-IdentXmlPart.xml` | `19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6` | `b6130b32498b6fee0d9e4db7a04dc79f785e1fbb` |
| `all-in-one/sources/decoded-original/0667-IdentXmlPart.xml` | `ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3` | `7f2e1798eb9f260d19d038a83369484d0f438856` |
| `all-in-one/sources/decoded-original/0668-IdentXmlPart.xml` | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` | `fe0f30d1eaae37783b0f03cb090353b3a3de3600` |
| `all-in-one/sources/decoded-original/0669-IdentXmlPart.xml` | `754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2` | `f5bf8f3c41d2a07ba9dcfd8f400548be8cf51cd3` |
| `all-in-one/sources/decoded-original/0670-IdentXmlPart.xml` | `e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841` | `b9466007b14e5c4f5d353dca5734401317e2dc03` |
| `all-in-one/sources/decoded-original/0671-IdentXmlPart.xml` | `26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293` | `e38a4e2c93ac8093e2b0b8e082a64688b5d9845e` |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |
