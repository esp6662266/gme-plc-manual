# DP01 백 필터 차압 원본 조사 초안

## 핵심 인계: 먼저 확인할 사항

- **고유 경로 확인:** DP01 센서 → FG169/PDF170 X3:92(+)/93(−) → FG172/PDF173 AI 모듈 30 I6+/32 U6−·I6− → PEW398 → `PR_BF01` Int `%IW398`의 `Peripherie/:P` 접근 → `0521` 환산 호출 → `Data.DP_01` DB1.DBW240. `%IW398`라는 주소 표기만 보고 프로세스 이미지 접근이라고 바꾸지 않는다.
- **환산·범위 오류 구분:** `0291`은 Int 입력을 DInt로 변환한 뒤 `(입력+Zero)×Coeff/28000` 연결을 가진다. DInt 산술·ENO 연쇄·최종 Int OutValue를 보존한다. 범위오류 가지는 −9999 출력과 일반 Coil OFR이며, `0540`의 3분 공통 차압 S/R 경보와 별개다.
- **허가 방향·공유 문턱:** `0219` BF01 허가는 SC10/VR04 처리응답 뒤 `DP01 ≤ DP_01_SOGLIA_1 OR Forza`다. BF02 허가도 같은 DP01 문턱을 읽는다. 이름에 맞춰 비교방향이나 참조를 고치지 않는다. `0200` Forza에는 타이머 외 ON 병렬 가지가 있다.
- **복구 오판 방지:** 공통 차압 경보 Reset은 DP01/DP02 `<2500`만 요구하며 하한 정상복귀 검사가 없다. 알람 소거와 센서 정상화·현장 안전복구는 다르다.
- **상충·누락:** 도면 제목은 SWITCH지만 실제 출력은 4–20mA다. 도면 0/50 mbar, 구 P&ID Setpoint 5÷10mbar, 백업 계수250/문턱50, HMI `mb` 소수점은 서로 다른 자료층이다. 교정/단위/현재 채널설정이 없으므로 하나의 현행 설정으로 합치지 않는다. 실물 동일성·정상극성·현재값·현재 CPU·HMI 쓰기 이벤트·압력 취출배관은 미확정이다.
- **이전 초안과 구분:** [BF01 초안](BF01-DOTS-DRAFT.md) §3·§5의 세정 공통 Word/경적/기동 근거를 같은 고정 원본의 공유 근거로 재사용한다. 이번에는 DP01 고유 `0521`, `0291/0014`, 선언/주소/Writer, DP01 전기·케이블 양 끝점, HMI 주소를 독립 재확인했다. BF01·BF02·DP02·제외 EV의 별도 완료를 늘리지 않는다.

이 문서는 작업3 자체 추가조사의 DP01 한 개 MD 초안이다. 로컬 2차133 통합 제외를 유지한다. 코드/공개 대장/배포/운영기록 반영, TIA 컴파일, 현재 CPU·실물·현장 복구 완료가 아니다.

## 작업 기준·허용 범위

- 대상: `DP01`, 이름 백 필터 차압, kind=sensor, group=계측, parent_id=null, depth=0, phase=phase2, priority_key=null. INVENTORY catalog[0], equipment catalog[95]. 기존 specialist 표시는 이번 완료 판정이 아니다.
- 별칭 `dp_01`, `pr_bf01`. BF01의 `pr_bf01` 별칭 충돌 및 DP02와 같은 이름을 유지한다. 동일 실물·부모/하위로 병합하지 않는다.
- 읽기 전용 기준: `gme-research/source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, `VERSION.json` 1.12.0. 저장소 https://github.com/esp6662266/gme-plc-manual . 현행 main/CPU/현장과의 일치 증명은 아니다.
- 공통 조사 지시, root AGENTS, 저장소 gme-equipment-rollout 스킬/source-map, WORK-STANDARD·WORK-ITEM-TEMPLATE·INVENTORY·START-GPT61, VERSION·WORKSPACE-HANDOFF·PUBLICATION_STATUS·ACTIVE-WORK·EXPANSION-WORK의 최신 머리말을 읽었다. 이번 사용자 승인 범위의 문서 조사만 수행하며 원본의 build/test/generator/preflight 실행은 하지 않았다.
- 범위는 `progress/TASK3-BATCH05-SCOPE.json` 및 `GME-CATALOG-OVERLAP-REVIEW.json`의 DP01 행. 실제 실행 모델/추론 수준의 런타임 증명은 미확인이다.
- 쓰기는 이 MD와 `extracts/DP01/`만. 원본·타 설비 추출·초안·코드·버전·대장·배포·사용자 운영기록을 수정하지 않았다. 새 Work/Codex·재위임·사용자 컴퓨터 접근을 하지 않았다.
- 시뮬레이터 작성/수정/생성/실행/행동시험0. PLC/현장/보호값/SEJIN 변경0. 원본 프로그램 명령을 실행하지 않고 자체 XML 파싱·문서 해시·PDF 렌더만 수행했다. 원본 및 중지5자산의 바이트 보존은 아래 해시 표/검사 JSON으로 구분한다.

이하 원본 경로는 고정 저장소 `all-in-one/` 기준이다. `0521` 등은 `sources/decoded-original/0521-FlgNet.xml`, 선언번호는 해당 `IdentXmlPart.xml`이다. LAD는 파생 document_id이며 NID/UID/RID와 다르다. 검색색인과 이름 일치만으로 원본 선언을 결속하지 않고 블록별 선언·핀·형식을 함께 확인했다.

## 7영역 적용표

| 영역 | 상태 | 확보한 내용 | 남은 범위 |
|---|---|---|---|
|설비·자료 기준|적용|DP01 고유 ID, BF01/DP02와 경계, 고정 판본·실제 PDF|현행 명판/제조사/실물 동일성·취출 위치|
|I/O·HMI|적용·부분 미확보|원시 Peripherie 입력/환산 Int/Bit, HMI 7주소, 저장값|현재값·단위/소수점·화면 이벤트·쓰기권한|
|제어 구조|적용|FC 호출/ENO, DInt 환산, 허가/문턱, 범위·Writer|실제 실행순서/리텐션/간접·외부 Writer|
|전기 전달 경로|적용|전원/4–20mA/차폐/AI 핀/중간 케이블 양 끝점|준공 단자대 매핑·설치 모델·현장 배선|
|알람·복구|적용·부분 미확보|일반 OFR와 공유 S/R·3분·Reset 조건 구분|현재 HMI 알림/경적/안전 복구|
|증상별 관찰|적용|읽기 전용 비교점·원인 배제·필요 증거|실제 측정/정비/운전시험 없음|
|완료·누락|적용|해시·정적 증거·상충/보류·네 기능 구분|독립검토·UI/기록/게시·TIA/CPU/현장|

## 1. 설비·공정·문서 소유 경계

1. `registers/equipment.json` DP01 role은 BF01 차압 감시 및 세정 허가·주기·경보와의 연결이다. 이것은 BF01 본체의 별칭을 독립적인 차압 접점으로 하나 더 만드는 근거가 아니다.
2. `PID_1684n002I.pdf` 실제 p1 BF01 확대에서 DP-01 표기와 필터 전후를 연결하는 계장 선, BF01·SC10·VR04·압축공기/세정 EV군을 구분했다. DP-01의 high/low 포트 번호, 실제 취출관 방향·길이·차단밸브·응축/막힘 대책은 이 자료만으로 완결되지 않는다.
3. P&ID 도번1684n002, 최초06/04/2011, 판I, 개정15/01/2013. DP01 옆 `Setpoint 5÷10mbar`는 구 도면 표기다. 현재 보호 설정·교정값 또는 PLC 단위의 근거로 직접 채택하지 않는다.
4. FG169 제목 DIFFERENTIAL PRESSURE SWITCH BAGS FILTER BF-01과 센서 그림 OUTPUT 4–20mA, 0/50mbar,110Vac가 함께 있다. 이번 확보 신호 경로는 아날로그이며 독립 디지털 스위치 접점은 이 DP01 경로에서 확인하지 못했다. 다른 현장 접점이 없다는 전수검증은 아니다.
5. DP02는 같은 시트에 있지만 PEW400/AI34·36의 별도 경로다. DP02 및 BF01·SC10·VR04·EV11~50를 DP01 문서 완료에 포함하지 않는다. EV 기존 제외 및 로컬2차133 통합 제외 유지.

## 2. I/O·선언·HMI·저장값

### 2.1 원본 선언 및 주소

주소는 SSD.AO/하위AO.BO의 bit offset과 BAD→DepDBBlock.TOD DB번호를 대조했다. 표는 백업 선언이며 현재 CPU 일치 증명이 아니다.

|신호|형식/주소|원본 선언·참조|해석/한계|
|---|---|---|---|
|PR_BF01|Int %IW398, `:P`|0678 RID295, Global SimpleAccess, Input AO3184, SAD.SAM=Peripherie; NID40 UID1544|도면 PEW398과 대응. 일반 입력워드 주소 표기와 직접 주변장치 접근 구분|
|Data.DP_01|Int DB1.DBW240|0676 RID298 AO1920 BAD11→0674 Data TOD1; NID40 UID1547 Write|환산 출력; 실제 mbar·소수점 배율 미확정|
|Coeff.ZERO_DP01|Int DB4.DBW116|0676 RID297 AO928 BAD8→0674 Coeff TOD4; NID40 UID1546 Read|영점 보정 입력, 현행값·변경승인 없음|
|Coeff.COEFF_DP01|Int DB4.DBW118|0676 RID451 AO944 BAD8; NID40 UID1545 Read|환산 계수, 현행값·승인계수 미확정|
|Allarm.BF01_OFR|Bool DB3.DBX24.3|0676 RID426 AO195 BAD354→0674 Allarm TOD3; NID40 UID23 Write|환산의 Out_of_range; HMI 이름 Allarmi_233와 별개 명명층|
|Coeff.DP_01_SOGLIA_1~4|Int DB4.DBW138/140/142/144|0596 RID8/15/19/23, AO1104/1120/1136/1152; BAD 확인|허가/단계 비교. 문턱1은 BF02에서도 읽음|
|DP_01_PAUSA_SOGLIA_1~5|S5Time DB4.DBW146/148/150/152/154|0596 RID10/17/21/25/28|문턱별 휴지 입력; 1은 NID25 UID30 Write 존재|
|DP_01_LAVORO_SOGLIA_1|S5Time DB4.DBW156|0596 RID13; NID25 UID52 Write 및 NID1 다섯 Read|다섯 단계 모두 LAVORO_1을 읽음|
|Data.LAVA_PAUSA / LAVA_LAVORO|Word DB1.DBW236/238|0596 RID11/14|공유 결과 Word, 원본 S5Time 입력과 구분|
|Allarm.MAX_DP_FILTER|Bool DB3.DBX9.5|0684 RID119 AO77 BAD10→0682 Allarm TOD3; NID14 UID1165 Set/1172 Reset|DP01/02 공통 알람, 둘로 복제하지 않음|
|Tag_112|Timer %T114|0686 RID118 AO114; NID14 UID1163/1164|S5T#3M용 PLC 타이머; HMI Tag로 오분류 금지|
|BF01_RUN|Bool %M180.3|0594 RID341 AO1443; NID29 UID75 Write|세정 허가 미러, DP01 측정/실물 세정 피드백 아님|

환산 함수의 `0611`은 Global DB와 별개인 **Local InterfaceAccess**다. IN0 Bool RID1; Analog_input Int RID3; Zero Int RID8; Coeff Int RID13; App5/6/3/4 DInt RID6/9/11/14; OutValue Int RID19; Out_of_range Bool RID26. RID/UID만 전체 파일에서 대조하면 `0291` ORef41/RID25가 다른 블록 `0631` Allarm1과 충돌한다. 여기서는 함수 인터페이스0611 및 인접 상수0612의 NID1 UID33/41, 원문 −1382를 결속했다. 후보 추출의 중복 이름을 최종 논리로 채택하지 않았다.

### 2.2 HMI 설정과 실제 화면의 경계

`sources/hmi_plc_tags.csv`를 주소로 조회한 7행이다. Access Name=PLC, 전 행 근거가 `dde.cfg 설정; 온라인 현재값 아님`이다.

|CSV 실제 행|태그|설정 주소|내부 ID|
|---|---|---|---|
|20|BF01_RUN|MX180.3|00456|
|256|data_DB1_DBW240|DB1,INT240|0028A|
|360|Coeff_DB4_DBW116|DB4,INT116|00206|
|361|Coeff_DB4_DBW138|DB4,INT138|00205|
|382|Coeff_DB4_DBW118|DB4,INT118|001E7|
|535|Allarmi_78|DB3,X9.5|0013F|
|783|Allarmi_233|DB3,X24.3|00025|

- 같은 검색에서 문턱2~4(DB4 INT140/142/144), IW398의 직접 같은 주소 행은 찾지 못했다. 전체 HMI/간접 읽기·쓰기 부재 증명이 아니다.
- 원본 `assets/HMI_DECOATER.png`를 실제 열어 DP-01 0.0mb 표시, BF-01 OUTSIDE, BF-02 INSIDE, 화면 상단2026-10-07을 확인했다. 정지 이미지의 숫자는 현재 온라인 관찰·정상값 증명이 아니다.
- `registers/hmi-window-provenance.json`은 원 WindowsInfo.json·screen events 미확보 및 current_hmi_verified=false를 명시한다. CSV 주소가 있다고 입력 허용·쓰기권한·클릭/Reset 이벤트·알람 priority/색상·소수점 배율을 확정하지 않는다.

### 2.3 백업 저장값은 현재 설정이 아니다

`live_index.json` doc1604 name/type/value 배열 각129개, doc1629 각162개 길이 일치를 확인한 뒤 같은 위치끼리 대응했다. doc1604 ZERO_DP01=0, COEFF_DP01=250, SOGLIA_1=50, SOGLIA_2/3/4=0; PAUSA_1=S5T#4S, PAUSA_2~5=S5T#0MS; LAVORO_1=S5T#200MS, LAVORO_2~5=S5T#0MS. doc1629 DP_01=29, DP_02=140, VALVE_W=2, VALVE_P=40.

이는 검색색인에 보존된 백업 인터페이스 값이고 XML 핀의 보충자료다. 현재 계수/문턱/차압을 읽은 것이 아니며 승인 기본값·현장에 적용할 값이 아니다. 특히 문턱2~4의0을 정상 계단 설정으로 보정하거나 1~4를 단조 증가한다고 가정하지 않는다. 값의 단위/소수점·활성 가지는 보류한다.

## 3. 제어·환산·소비자·복수 쓰기

### 3.1 상위 호출과 DP01 고유 호출

- main `0031` LAD1619 NID6: ON Part282(ORef271/RID52,W280/284).out W283이 Analog input conversion CRef261.en 및 Allarms1/2/3 CRef264/267/270.en에 **병렬** 결선된다. 0688 RID55/CodeBlock273=FC3, RID64/CodeBlock279=FC6; 0694 CRef261/RID56, CRef270/RID65를 대조했다. ENO 직렬 호출이라고 쓰지 않는다.
- `0549` LAD1620 NID7: ON Part350/ORef335.out W351→Filter CRef322.en 등 병렬. 0688 RID70/CodeBlock339=FC8,0694 RID71. `0033` LAD1622 NID9 ON352.out W353→Allarm manager CRef347.en(0688 RID91/CodeBlock350=FC24,0694 RID92).
- 이 연결은 문서상의 호출 허가다. 현재 ON 상태/실제 OB 호출순서·스캔·실시간 갱신·기동 리텐션을 증명하지 않는다. startup live_index doc401의 `set s "on" clr s "off"`를 OFF Reset이나 영구 상수로 바꾸지 않는다. doc401과 `0401-FlgNet.xml` HMI 출력 미러는 다른 자료다.

**DP01 `0521` LAD1773 NID40의 9개 Wire를 직접 확인했다.**

|연결|Part/ORef/CRef·Wire|원본 결속|
|---|---|---|
|호출 허가|rail W1557→Contact1555.in; ON ORef1542/RID1 W1549; Contact.out W1556→CRef1536.en|0678 ON; 0680 CRef RID351|
|IN0|ON ORef1543/RID1 W1550→CRef1536.IN0|호출EN과 같은 ON이지만 별도 핀|
|원시 입력|ORef1544/RID295 W1551→Analog_input|0678 PR_BF01 Int Peripherie|
|계수|ORef1545/RID451 W1552→Coeff|0676 COEFF_DP01|
|영점|ORef1546/RID297 W1553→Zero|0676 ZERO_DP01|
|환산값 Write|CRef1536.OutValue W1554→ORef1547/RID298|0676 Data.DP_01|
|범위오류 Write|CRef1536.Out_of_range W24→ORef23/RID426|0676 BF01_OFR|

CRef1536의 CodeBlock1548/RID5는 0672 `Signal linearization`,0680 BlockInterfaceInfo RID351/TORID5와 Bool/Int 입출력 인터페이스를 확인했다. 함수 내부를 DP01만의 복제된 새 함수로 취급하지 않는다.

### 3.2 정상 범위·DInt 환산의 핀 경로

`0291` LAD1658 NID1은 전체15 Parts/43 Wires를 확인했다.

1. rail W257→IN0 Contact255(ORef196/RID1,W220).out W256이 Gt258.pre 및 오류 비교 Gt190/Le259.pre에 연결된다.
2. Gt258: Analog_input ORef32/RID3 W30, literal−1382 ORef33/RID25 W31. out W25→Le161.pre. Le161: Analog_input ORef29 W27, literal32767 ORef34/RID29 W28. 따라서 유효 산술 가지는 `IN0 AND Analog_input >−1382 AND Analog_input ≤32767`이다.
3. Le161.out W26→Convert164.en; Analog_input ORef199 W225→Convert164.in; Int→DInt out W226→App5 ORef200/RID6. Convert164.eno W227→Convert167.en; Zero ORef201/RID8 W228→Int→DInt→App6 ORef202/RID9 W229.
4. Convert167.eno W230→Add170.en; App5 ORef203 W231와 App6 ORef204 W232를 **DInt Add**하여 App3 ORef205/RID11 W233에 쓴다.
5. Add170.eno W234→Convert174.en; Coeff ORef206/RID13 W235를 Int→DInt로 App4 ORef207/RID14 W236에 쓴다. Convert174.eno W237→Mul177.en; App3 ORef208 W238와 App4 ORef209 W239를 DInt 곱셈, App3 ORef210 W240에 다시 쓴다.
6. Mul177.eno W241→Div181.en; App3 ORef211 W242 / literal28000 ORef212/RID17 W243. DInt 나눗셈 out W244→App3 ORef213. Div181.eno W245→Move185.en; App3 ORef214 W246→OutValue Int ORef215/RID19 W247.

이상은 정적 연결식 `(DInt(Analog_input)+DInt(Zero))*DInt(Coeff)/28000` 뒤 Int OutValue 전달이다. Real 연산·자동 공학단위·반올림/포화처리로 바꾸지 않는다. 마지막 Move의 DInt→Int 폭 축소·오버플로/ENO 상세 CPU 동작·실제 결과는 실행하지 않았다. 28000을 관행적인 다른 아날로그 정규화 상수로 고치지 않는다. 입력이 Int인데도 `>32767` 비교가 구조에 존재한다는 사실을 보존하며 센서 진단의 충분성을 이 식만으로 판단하지 않는다.

### 3.3 오류·비활성 경로와 일반 Coil

- `0291`: Analog_input >32767 Gt190(ORef42/43,W36/37) 또는 ≤−1382 Le259(ORef40/41,W38/39) → OR47(W35/48).out W49→Move193.en. −9999 Int ORef218/RID21 W252→Move193.in; out1 W253→OutValue ORef219/RID19.
- Move193.**eno** W21→일반 Coil23.in, ORef24/RID26 W22=Local Out_of_range. SCoil/RCoil 또는 타이머가 아니다. 이를 독립 래치 알람·안전 정지로 바꾸지 않는다. OUT 비트와 ENO를 같은 의미로 쓰지 않는다.
- `0612` −9999는 Int/SV `_x002D_9999`(V55537),−1382는 Int/SV `_x002D_1382`(V4294965914)다. 내부 V의 unsigned 표현을 양수 경보값으로 읽지 않았다.
- `0014` LAD1659 NID2: NOT IN0 Contact171(operand Negated,ORef165,W168; railW173).out W172→Move162.en; literal Int0 ORef166/RID23 W169→OutValue ORef167/RID19 W170. 이 네트워크는 OFR의 별도 Write가 아니다.
- 함수 안의 비활성0 경로와 호출자 EN을 구분한다. DP01 호출 `0521` 자체가 ON으로 허가되므로 ON이 꺼질 때 함수가 매 스캔 실행되어 DP01을 반드시0으로 쓴다고 단정하지 않는다. 갱신 정지/잔류값·OFR 최종상태는 현재 실행자료가 필요하다.

### 3.4 차압의 세정 허가·주기 소비자

공통 제어의 전체 세정 순서/EV 출력은 BF01 초안 §3을 연결 재사용하고, 아래 DP01 관련 핵심은 원본에서 독립 확인했다.

- `0219` LAD1886 NID29: ON21→SC10 처리22→VR04 처리23 직렬(W47/49/51). 23.out W53이 Le24.pre와 Forza Contact25.in을 같이 허가한다. Le24.in1=DP_01 ORef37/RID6 W54, in2=SOGLIA_1 ORef38/RID8 W55; out W56→OR26.in1. Forza25 ORef39/RID57 W57, out W58→OR26.in2. OR.out W59→Coil27, Local허가 ORef40/RID63 W60; Coil.out W72→Coil74, BF01_RUN ORef75/RID341 W73.
- 즉 `ON AND SC10_processed AND VR04_processed AND ((DP01 ≤ S1) OR Forza)`다. Forza는 SC10/VR04를 우회하지 않는다. 물리 아날로그 입력을 이 허가의 직접 접점으로 대체하지 않는다.
- BF02 쪽 Le30의 ORef44/RID8 W66 역시 **DP_01_SOGLIA_1**이다. DB4W138 설정을 DP01만의 영향으로 취급하면 공유 허가 의존성이 빠진다.
- `0200` LAD1885 NID3의 Forza는 ON451.out W452 아래 Tag130 Contact457.out W458→OR21.in1, 별도 ON Contact460(ORef461/RID52,W463).out W22→OR21.in2. OR.out W23→Coil428(Forza ORef437/RID57,W449). NOT Tag129→SdCoil418 S5T#2H/Tag130, Tag130→SdCoil423 S5T#10M/Tag129도 함께 있다. **2시간 만료만을 기다리는 순수 타이머 허가가 아니다.**

`0198` LAD1883 NID1의 직접 DP01 단계 구조:

|선행조건/구간|Part·주요 Wire|PAUSA 소스→공유 Word|LAVORO 소스→공유 Word|
|---|---|---|---|
|OFF377→Ev_filter_on<51 Lt206|W318~321|다섯 비교 가지에 분기|OFF를 현행 FALSE로 가정하지 않음|
|DP01<S1|Lt213 W322/323|Move216 ORef284→285 W326/327|Move219 ORef286→287 W329/330|
|DP01≥S1 AND <S2|Ge225→Lt228 W331~335|Move231 ORef292→293 W338/339|Move234 ORef294→295 W341/342|
|DP01≥S2 AND <S3|Ge240→Lt243 W343~347|Move246 ORef300→301 W350/351|Move249 ORef302→303 W353/354|
|DP01≥S3 AND <S4|Ge255→Lt258 W355~359|Move261 ORef308→309 W362/363|Move264 ORef310→311 W365/366|
|DP01≥S4|Ge270 W367/368|Move273 ORef314→315 W371/372|Move276 ORef316→317 W374/375|

PAUSA는1~5지만 LAVORO는 다섯 구간 모두 동일 RID13 LAVORO_1이다. 각 LAVORO Move.en은 앞 PAUSA Move.eno(W328/340/352/364/373)다. `0199` DP02 경로와 `0201` ON 아래 고정 시간 Word 쓰기, `0217` KF_KT에 의한 PAUSA_1/LAVORO_1 쓰기는 BF01 §3.3~3.4의 같은 원본 공유 근거를 재사용한다. 따라서 DP01 비교만으로 최종 LAVA_PAUSA/LAVORO나 현행 세정 주기를 확정하지 않는다. 모든 공통 Writer를 이번에 새로 전수 의미검토했다고 세지 않는다.

### 3.5 Writer 범위 검색과 한계

전체 IdentXmlPart를 이름/형식/bit offset으로 파싱했다. DP01 명명 직접 Write는 0676 NID40 UID1547(Data.DP_01) 및 UID23(BF01_OFR), 공유 MAX_DP_FILTER는0684 NID14 UID1165/1172다. Coeff ZERO/COEFF/SOGLIA_1의 명명 PLC Write 선언은 이 검색에서 찾지 못했지만 HMI 주소·외부통신·레시피/간접 복사는 별도다.

이름이 빈 절대 GlobalAccess와 주변 DepDB 후보도 조회했다. `0563` RID32,AO64,size16,BAD23→`0562` Allarm TOD3,NID3 UID294 Write는 **DB3.DBW8**로 MAX_DP_FILTER bit77에 겹친다. `0148` LAD403의 Move267.out1 W316→ORef294이며 Int0 ORef293/RID54 W315가 입력이다. 이 startup Word Write는 BF01 §3.7 공유 근거와 일치한다. DP01 DB1W240 및 OFR DB3X24.3을 덮는 추가 절대 Word 후보는 이 방식에서 찾지 못했다.

이 검색은 정적 명명·근접 선언 범위다. NID가 null인 파생 색인은 원본 선언NID3으로 보완했다. 포인터/블록복사/통신/현재 CPU의 모든 쓰기 부재를 증명한 것이 아니며, 현재 최종값·기동 결과를 결정하지 않는다.

## 4. 전기 끝점·도면 실제 렌더

### 4.1 실제 확인한 페이지와 개정란

|원본|FG/실제PDF|실제 렌더 판독|footer/개정|
|---|---|---|---|
|Electrical_Rev2.pdf|FG152/PDF153|JB1 110Vac·24Vdc 공급 분기|DATA27.05.2024, 별도 Rev2 문구 미확인|
|동일|FG153/PDF154|JB1 IM155/153A1 AI POS2|DATA27.05.2024, 별도 개정 문구 미확인|
|동일|FG169/PDF170|DP01 전원/신호/차폐 및 DP02 경계|DATA27.05.2024, 별도 개정 문구 미확인|
|동일|FG172/PDF173|PEW398 AI핀30/32·모듈전원41/44|DATA27.05.2024, 별도 개정 문구 미확인|
|Electrical_Can_Decoating_20241118.pdf|PDF42|DUST ZONE08 DP01/JB01TB5/JB01 경로|CANDC-CONS-E025-042;24.11.11 first draft design;CHECKED/APPROVED 공란|
|동일|PDF61|DP01 전원/AI의 중간 및 최종 구간4행|CANDC-CONS-C011-061;24.11.11 first draft design;CHECKED/APPROVED 공란|
|PID_1684n002I.pdf|PDF1|BF01 DP01 공정계장/범위 표기·타이틀 확대|1684n002,원작성06/04/2011,판I15/01/2013|

위7개 고유 PDF페이지는 이번에 원본에서 렌더하고 실제 열어 판독했다. 전기154/173쪽은 footer 확대도 확인했다. 렌더 파일 수·해시 수를 의미검토 수로 세지 않는다. 파일명 Rev2와 시트별 개정란을 같다고 추정하지 않으며 다른 FG에도 PDF=FG+1을 자동 적용하지 않는다.

### 4.2 DP01 전원·신호의 양 끝점

1. **센서110Vac 공급:** FG152 X3:3←110Vac9.10(9/4)→152QF4 2A→110Vac152.8, 공통0Vac9.9. FG169에서110Vac152.8→X3:90의5×20 2A F→선169.1→DP01 110Vac 한쪽 전원단자; 다른 쪽→X3:91→0Vac9.9. AC전원 단자를 +/− DC극성으로 부르지 않는다.
2. **센서 출력:** FG169 DP01 OUTPUT4–20mA의+→X3:92→+PEW398(172/4),−→X3:93→−PEW398(172/4). 신호+/−와 위110Vac 전원을 구분한다.
3. **차폐:** DP01 출력 케이블 차폐 표기→X3:94/169SCH1→172/3, 도면 접지 기호. FG172는169SCH1 차폐가59SCH2와 연결되어180A/1로 이어지는 표시다. 차폐를 신호−와 합치거나 현장 단일점 접지 상태를 확정하지 않는다.
4. **AI 채널:** FG172 PEW398,CPU515/MOD2에서 +PEW398→30 I6+,−PEW398→32 U6−/I6−. 29 Uv6/31 U6+는 이 도면에 연결된4–20mA 핀으로 바꾸지 않는다. DP02 PEW400의34/36과 혼합하지 않는다.
5. **AI 전원:** +24Vdc152.5→X22:4000 5×20 500mA F→선172.1→41 L+;−0Vdc152.4→44 M. FG152 별도152QF1 6A→152GD1 AC/DC5A→152QF2 4A→24Vdc계통이다. 센서110Vac 퓨즈와 모듈24Vdc 퓨즈가 다르다.
6. **모듈 문서상 구성:** FG153 153A1 POS2 AI8 표기6ES7531-7KF00-0AB0. 주변153IM155 내부/외부 모델 표기가 서로 다르고(5AA00 vs5AA01),153A3도 내부/외부 문자열 차이가 보인다. DP01의 설치 모델/교체 호환성으로 확정하지 않는다. 모델사진·현재 HW configuration이 필요하다.

이 경로에서 DP01용 출력 릴레이 부하접점·코일 제어는 확인하지 못했다. BF01의 EV릴레이5–9 부하접점/하단1·5·9 접점표는 주변 세정 출력의 소유이며 DP01 아날로그 회로로 복사하지 않는다. 도면의 퓨즈/전압/범위 표기는 현장 측정·현행 설정 확인이나 변경 지시가 아니다.

### 4.3 시공 케이블 구간

|실제PDF61 행|케이블번호|FROM→TO|종류/규격·LEN|
|---|---|---|---|
|11_1|=DUS+BF01-JB01TB5A|BF01 JB01→BF01 JB01TB5 DP-01 POWER|AC,CVV3G1.0,LEN6|
|11_2|=DUS+BF01-JB01TB5B|BF01 JB01→BF01 JB01TB5 DP-01 AI|AI,CVV-S2S1.0,LEN6|
|11_25|=DUS+BF01-DP01A|BF01 JB01TB5→BF01 DP-01 IN POWER|AC,CVV3G1.0,LEN2|
|11_26|=DUS+BF01-DP01B|BF01 JB01TB5→BF01 DP-01 OUTPUT|AI,CVV-S2S1.0,LEN2|

PDF42 DUST ZONE08은222RD→JB01TB5→DP-01과 JB01 분기를 보여 준다. 표에11_1/11_2와 최종 신호11_26이 있고 최종 전원11_25는PDF61에서 확인했다. PDF42 한 도형으로4행을 모두 판독했다고 쓰지 않는다. 표의 LEN을 현장 실측 길이로 바꾸지 않는다.

시공 도면은 `first draft design`, 승인란 공란이며 승인 준공도를 확보하지 못했다. OEM X3:90~94와 시공 JB01TB5의 실제 단자번호 일대일 매핑, 케이블 마킹·차폐·연속성·전압/전류·압력 취출 포트는 미확정이다.

## 5. 알람·Reset·복구 경계

### 5.1 OFR와 공통 MAX_DP_FILTER

- BF01_OFR는 `0521` 호출의 Bool 출력 DB3X24.3이며 `0291` 오류 Move.eno→일반 Coil이다. 3분 타이머나 유지S/R을 OFR에 옮기지 않는다.
- 공통 차압 `0540` LAD1992 NID14: ON1204/ORef1153 W1173, out W1205→Gt1121 DP01>2800(ORef1154/1155,W1174/1175),Gt1124 DP02>2800(W1177/1178),Lt1127 DP01<−100(W1180/1181),Lt1130 DP02<−100(W1183/1184). 비교출력 W1176/1179/1182/1185→OR1120.in1~4.
- OR.out W1186→SdCoil1136.in 및 Tag112 Contact1206.in. value ORef1162/RID96 W1187=0683 S5Time **S5T#3M**(V8576),operand ORef1163/RID118 W1188=T114. Contact1206 ORef1164 W1189,out W1207→SCoil1141;ORef1165/RID119 W1191=MAX_DP_FILTER.
- Reset은 ON→RESET_ALLARM Contact1208(ORef1166/RID24,W1193)→기존MAX_DP_FILTER Contact1210(ORef1167,W1194)→Lt1146 DP01<2500(ORef1168/1169,W1195/1196)→Lt1149 DP02<2500(ORef1170/1171,W1198/1199)→RCoil1152 W1200, 대상ORef1172/RID119 W1202.

발생은 strict `>2800 OR <−100`,Reset은 양쪽 strict `<2500`다. 경계값을 ≥/≤로 바꾸지 않는다. Reset에는 입력≥−100 조건이 없다. 따라서 −9999 같은 오류값도 단순 상한 비교를 만족할 수 있다. 이것은 문서 조건의 비교이며 현장 입력 강제·동작 시험을 한 것이 아니다. 알람해제가 센서 정상화/안전 운전의 증거가 될 수 없고, 실제 동시Set/Reset 우선순위·타이머·현재 호출 결과는 미확정이다.

### 5.2 표시·경적·기동쓰기 공유 근거

BF01 초안 §5.2의 동일 원본 `0151/0152/0153/0158`, 선언0564/0565를 연결 재사용한다. alarm manager는 DB3 W0~16의 Word변화를 WorkData와 비교하고 NEW_ALLARM/RUN_HORN/RESET 경로로 넘긴다. MAX_DP_FILTER의 DB3W8은 이 범위에 있지만 BF01_OFR DB3X24.3은 밖이다. 이 근거로 OFR까지 같은 Word변화 경적 경로를 직접 거친다고 단정하지 않는다. 다른 알림경로가 전혀 없다는 증명도 아니다.

startup `0148` DB3W8←0은 MAX_DP_FILTER와 겹치며 OFR X24.3에는 겹치지 않는다. Reset 요청·ACK·알람 소거·원인 제거·안전 재기동을 구분한다. `Allarmi_233`/`Allarmi_78` HMI 주소설정과 실제 표시 문구·색·소리·기록 동작은 별도다. 이 조사에서는 Reset 버튼/출력/설정 변경을 수행하지 않았다.

## 6. 증상별 관찰·원인 배제 준비

실제 정비나 전기/공압 접근 지시가 아니라 읽기 전용 비교점이다. 통전측정·압력관 접근·교정·정비는 현장 자격자와 승인된 격리/안전절차가 필요하다. 계수·문턱·퓨즈/보호설정·배선을 추정해 변경하지 않는다.

|증상|함께 남길 관찰 위치·값|원인 배제/비교|복구 판정에 필요한 자료|
|---|---|---|---|
|HMI DP01이 고정/0.0|원시IW398:P,DB1W240,ON/FC호출,갱신시각,HMI주소·연결상태|입력·환산·표시 단계 분리;정지 이미지/저장값과 현재값 혼합 금지|현재 프로젝트/채널·HMI스케일 및 동시시각 값|
|DP01이−9999/OFR|센서전원/AI4–20mA,원시Int,함수오류범위,BF01_OFR|X3:90/91 전원과92/93 신호,AI30/32·차폐,취출관·센서·채널 구분|승인 점검측정/교정·현재 HW configuration·범위복귀 기록|
|현장계기와 HMI 값 차이|현장계기 단위·영점,원시값,DB4W116/118,DB1W240,HMI소수점|0/50mbar·구P&ID5÷10·계수250·문턱50을 동일단위로 가정하지 않음|명판/교정성적서·승인환산표·화면 바인딩|
|차압이 낮은데 세정허가 없음|SC10 DB13X5.0,VR04 DB13X5.5,ON,DP01/S1,Forza,BF01_RUN|직렬처리응답과≤조건·Forza를 분리;RUN은 세정완료 아님|현재 호출/원시·처리응답 비교 및 안전허가복귀|
|차압에 따른 세정주기가 예상과 다름|OFF/ON,공유step,LAVA Word236/238,문턱/PAUSA/LAVORO|다섯 LAVORO_1·복수WordWriter·저장문턱0·공유BF02 영향|현재Writer/실행분기·주기기록,별도BF01 자료|
|공통경보가 해제되나 바로 다시 발생|DP01/DP02,T114,MAX_DP_FILTER,RESET,시각|Reset하한미검사·−9999·양쪽기여·startup겹침 구분|양쪽입력 정상화·원인해소·지속회복 및 승인복귀|
|OFR 표시와 경적 반응이 다름|DB3X24.3/9.5,HMI2주소,공통Word경보범위|OFR은W0~16 경적비교범위 밖;표시와음성 분리|현재알람설정/경적·이벤트로그|
|차압 급변/음수이나 전기상 정상|차압취출관 H/L,분진/응축/막힘,운전상태·센서측정|전기정상만으로 공정측 압력차 정상 판정 금지|계장준공도·교정·자격자 점검·동시 운전기록|

관찰기록에는 관찰자,실제 시각/시간대,위치,값/단위,수집장치,프로젝트/CPU근거,비교원본,배제결과,승인조치,복구증거를 별도로 둔다. 이번에는 실제 운영관찰/복구기록을 만들지 않았다.

## 7. 완료 기준·누락·재개

### 7.1 새 자료가 필요한 경계

|필요자료|수집 위치/목적|완료 판정|
|---|---|---|
|DP01명판/제조사매뉴얼/교정성적서|현장 계장 담당;전원·범위·단위·H/L포트|도면과 실물·교정의 일치 또는 차이 기록|
|승인준공도·JB01TB5단자표·케이블표|설계/시공 담당|X3↔TB5↔센서·차폐 양 끝점 확인|
|현재 TIA project/HW configuration|승인된 프로젝트자료|CPU/AI6채널/4–20mA모드·주변장치주소·환산일치|
|현행 HMI 프로젝트/이벤트|화면 소유자|DB1W240 단위/소수점·읽기/쓰기·알람/Reset 확인|
|현재 교차참조/온라인 동시관찰|허가된 PLC 담당|실제호출·계수·Writer·ENO/OutValue 잔류·경보순서 확인|
|정상·이상·복귀 기록|현장운영자 승인 범위|원인해소와 양쪽DP안정·실물복구를 별도로 증명|

이 자료 없이 현재모델·정상극성·안전한 보호값·실물 동일성·복구 완료를 채우지 않는다. 새 자료 없는 실물 보류를 반복 조사하지 않는다.

### 7.2 네 기능과 기록 보존

|기능|적용성|이번 상태|
|---|---|---|
|도면·래더 나란히 보기|FG169/172와0521/0291에 유용|MD 원본연결만;제품UI 구현/검사 미수행|
|백업·선택 복원|DP01 독립키/미지필드 보존 필요|프로그램/사용자기록 변경 및 저장·재열기 없음|
|전후 기록 비교|동시 시각 원시·환산·HMI·교정 비교에 유용|실제 운영기록 생성·비교시험 없음|
|관찰 보고서/PDF|향후 승인관찰 자료에 적용 가능|이번 도면읽기 렌더와 제품보고서/PDF 검증은 다름|

note/repair_observation·미지 필드·타 설비·초안·저장키를 수정하지 않았다. BC01 회귀·제품정적검사·UI1280/390·저장/재읽기/새로고침·ZIP/배포·CSP는 수행하지 않았으며, 이 MD 근거 검사를 그 결과로 대체하지 않는다.

### 7.3 검토 범위·상태

- 독립 직접핵심:0521/0291/0014의 전체 핀·형식,0219 DP01 및 공유S1 허가,0540 전체 발생/Reset,0198 DP01단계·0200 Forza,0031/0033/0549 호출의10네트워크.0148는DB3W8겹침 선택가지만 확인했다.
- 전체 IdentXmlPart의 이름/주소/Writer 검색은 탐색 범위다. 모든파일/모든네트워크 의미검토 완료가 아니다. 공유0199/0201/0217·경적0151~0158 전체 의미는 BF01 초안의 동일원본 근거를 연결 재사용했다.
- 원본PDF7개 고유쪽 실제렌더·footer/선택경로, HMI원본 이미지1개, HMI7주소, 백업2배열의 선택값을 확인했다.
- 단위/교정·실물·현행CPU의 누락을 해결했다고 선언하지 않는다. DP01 밖 설비완료 추가0, 기존제외 재개0.

|구분|최종 상태|경계|
|---|---|---|
|documentation|complete_with_gaps_draft|7영역·핵심원본·상충/누락 작성|
|static_review|selected_source_checked; independent_review_pending|아래 자체 XML단언·원본해시만;전제품검사 아님|
|ui_records|not_run|제품 화면/운영기록 변경 없음|
|publication|not_published|GitHub/배포/공개대장 변경 없음|
|tia_compile|not_performed|로컬TIA추가권한 없음|
|live_cpu|not_performed|현재 프로젝트/CPU 불일치 가능성 미해결|
|field_recovery|not_performed|실물 측정/정비/복구 수행 없음|

다음 한 작업: 부모가 DP01의0521→0291/0014·FG169/172와 Reset하한 경계를 선택 독립검토한 뒤 이 원초안을 전달한다. 전달 후 정정은 별도 보강으로 남기며 원초안을 덮어쓰지 않는다. 실물자료 없는 보류는 유지하고 다음 승인 조사대상은 부모가 배정한다.

## 부록 A. 실제 작업 시각·산출물·검사

아래 시각은 단계가 실제 끝난 때의 UTC이며 예상 소요시간이 아니다. 검사JSON/해시JSON/원본추출·도면렌더는 `extracts/DP01/`에 있다. 도면과 XML 근거의 신규 연구 산출물이며 source 원본 실행 산출물이 아니다.

|실제단계|UTC 완료시각|
|---|---|
|instructions_and_fixed_source_scope_read|2026-10-11T10:28:54.672845+00:00|
|own_original_XML_extraction_and_PDF_render_completed|2026-10-11T10:29:34.374641+00:00|
|original_review_draft_and_22_source_assertions_hash_verification_completed|2026-10-11T10:37:55.564271+00:00|

자체 원본구조 단언 22개 전부 통과. 고정 원본 Git 변경0. 선택 원본/맥락/보존 69파일 SHA-256과 고정 Git blob 바이트 일치, 중지5자산 freeze 일치. 이 파일 수는 원본 의미검토 수와 다르며 관례적인90개 목표에 맞추지 않았다. 파일 무결성 검사로 전체 프로그램·현장 완료를 주장하지 않는다.

### 공유 연구문서 무결성

|이전 문서|SHA-256|재사용범위|
|---|---|---|
|`drafts/BF01-DOTS-DRAFT.md`|`b66269d2df73e6c704e9f98156a6d546f56e1d9fbf1baf9c9210ffb506d48b07`|공통근거/인덱스;원본Git파일 아님|
|`drafts/BF02-DOTS-DRAFT.md`|`ec68e9590e07ba39d40cbfb302114ec1faa1b51f12c31184128d02a0d837d7fa`|공통근거/인덱스;원본Git파일 아님|
|`drafts/TASK3-BATCH04-CORE-HANDOFF.md`|`f846fadac1b99f974303598bda44530aeffcd13777e9d8f197a2f65cc2b3e78a`|공통근거/인덱스;원본Git파일 아님|

## 부록 B. 원본 SHA-256 및 고정 Git blob 전체 목록

모든 행은 SHA-256(현재파일)=SHA-256(고정커밋 blob), 바이트비교 true다. Git blob OID는 내용해시 SHA-256과 별개 표식이다. 상세 role은 source-hashes.json에 있다.

|원본 경로|SHA-256|고정 Git blob OID|일치|
|---|---|---|---|
|`.agents/skills/gme-equipment-rollout/SKILL.md`|`fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b`|`9aa820ea6ca15b4e136c9772423b78ed4df6a3d4`|true|
|`AGENTS.md`|`0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2`|`073164bc6efd5791032d62c71b03b4dab48cb6f8`|true|
|`VERSION.json`|`5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7`|`fffb51663b7705aec91cb119ca80ee943a4ce758`|true|
|`all-in-one/assets/HMI_DECOATER.png`|`b84b888a2df87d23b514aeb790d2fc51f31c3b20486061a365380b28986f49af`|`aa549ca104a1f92975dbf4ec346368423f3f61b7`|true|
|`all-in-one/assets/program-model-data.js`|`52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f`|`38f34b0caa380a16ccad6f6f1e234a2fdf23f327`|true|
|`all-in-one/assets/simulator-workspace.js`|`3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc`|`97c2c831c77a9699fff0e0960b3bc1b7d93d45b3`|true|
|`all-in-one/assets/virtual-plc.js`|`5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc`|`0bd9eceb54365a91214a37c5601b5067c39a3f75`|true|
|`all-in-one/registers/equipment.json`|`7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa`|`acc42633033398216469064932c4b76987371606`|true|
|`all-in-one/registers/hmi-window-provenance.json`|`b0251e377268ec7be83a781fb41e84684a6b187d0132fc7cfa51a6074823a2fa`|`bf258dd76b936da85beebd450ca563aef1b4e9e3`|true|
|`all-in-one/registers/program-model.json`|`6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5`|`9860b10f008d3a5ae714be50d77b703dfec32f3a`|true|
|`all-in-one/registers/simulator-freeze.json`|`bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835`|`808ffac14dbd1b4a7d797fa6cd0d647635d90b47`|true|
|`all-in-one/registers/virtual-plc-test-results.json`|`a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64`|`757dd50e45184568facb8ff62900b39d3ce848d1`|true|
|`all-in-one/sources/Electrical_Can_Decoating_20241118.pdf`|`3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd`|`0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8`|true|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|true|
|`all-in-one/sources/GME_20250506.zap18`|`00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8`|`211c4f604627a32f82a1124c2a9872c2fcf00865`|true|
|`all-in-one/sources/PEData.plf`|`647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a`|`65605ff8910f920109da731604aa5dc8d83fc956`|true|
|`all-in-one/sources/PID_1684n002I.pdf`|`2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b`|`8c83a59fefd5b8b651ec3537ea4236a073f5e109`|true|
|`all-in-one/sources/decoded-original/0014-FlgNet.xml`|`2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30`|`4d164b074fcc13a8f97da9e24382cc169ef29555`|true|
|`all-in-one/sources/decoded-original/0031-FlgNet.xml`|`76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65`|`653d27572de6beedcf3eb6c95702bb119a8b567f`|true|
|`all-in-one/sources/decoded-original/0033-FlgNet.xml`|`e7fc5601889297a84fcc6b5601a3e0acba420b9c9adb8b37c60277a0fb5cb108`|`b8a89efcb38999950739e0462830d03a94d57c08`|true|
|`all-in-one/sources/decoded-original/0047-IdentXmlPart.xml`|`2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e`|`3dc282f149a21fdf76d5521ef1c833be63b578b4`|true|
|`all-in-one/sources/decoded-original/0048-IdentXmlPart.xml`|`d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d`|`64fc5a7f1ad33f3b901b00f0d22d23578ffabff8`|true|
|`all-in-one/sources/decoded-original/0056-IdentXmlPart.xml`|`c5ec45cd232c36d80f80487ec0dd284a876e326ba2286fc722ecc861a400232a`|`1364306d64caf1f1f094c98dc163edf69cdc1afc`|true|
|`all-in-one/sources/decoded-original/0057-IdentXmlPart.xml`|`1124275ab34e188b042b263d3c4b744abf5637ffd229af642b81a27f00a00c6b`|`264d24445f42cf32706bc6942863f9f227eb797e`|true|
|`all-in-one/sources/decoded-original/0148-FlgNet.xml`|`1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313`|`3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3`|true|
|`all-in-one/sources/decoded-original/0151-FlgNet.xml`|`227627d165c6240a4c15b62fd4e4c8d7a621c15f35319cb424601df5cc52c904`|`8e8a9801d1f57180fc3747f6515c0353f38f7dc5`|true|
|`all-in-one/sources/decoded-original/0152-FlgNet.xml`|`2b6165460f06a52de56afcb4d65ed163d64320e24af1b194e934a4d7c6bfe49f`|`dd8e35b98043d9d0f230351352273eac1d783990`|true|
|`all-in-one/sources/decoded-original/0153-FlgNet.xml`|`3d3a236a66a7a5c9b8e2d1e15da63cc943ba5cd266949583cbac6ffbb2f88bc6`|`d50223c45f5eb1d1c1d3530b41db1e79ad6c71f3`|true|
|`all-in-one/sources/decoded-original/0158-FlgNet.xml`|`d3f3adebc3d990b85c5d4c294906ae3bc3dafebb49d25b030bf9cc2ccf905651`|`233ccf8f9d82ffffa498e04cbdcd3de07115c1db`|true|
|`all-in-one/sources/decoded-original/0198-FlgNet.xml`|`95d631a1979b04f148bf6b71eebb8857e580511c523912d533814ed41dda871d`|`965c744c3e216c3625c6ec414236d2db1b6ef6ce`|true|
|`all-in-one/sources/decoded-original/0199-FlgNet.xml`|`005617b53ff1021c24dd11b19cae78c72ff535407999707d4c4636e493888b7c`|`ca1debbcfd0ca0a1555005886450db3e495d9772`|true|
|`all-in-one/sources/decoded-original/0200-FlgNet.xml`|`2bd1be34eb905a10d840c59aeb461464a1af418fa0ea3f2b8d0b3f88145eb27e`|`31eb4f3df5596c004278ef7b3ccf158ae3878079`|true|
|`all-in-one/sources/decoded-original/0201-FlgNet.xml`|`77e7fdcb37e54b3d513aee760f3c142f7259990352dd0ad14a3c9a1a5f61da32`|`0268a83b49e442ee22406139e6bf5062b21bdc6a`|true|
|`all-in-one/sources/decoded-original/0217-FlgNet.xml`|`cbff99bc9f5f8bbde0272c9541be1b26e48808865be58859ff6cef50b8eb9368`|`0a2ce467fd29315818de17b89093cf133e5742d8`|true|
|`all-in-one/sources/decoded-original/0219-FlgNet.xml`|`245409937abf7e28f25a24d4a6d311a801a4b2ee7293148be9b3d266352eb53a`|`d1c9ae9d9fe8a5a1ed605d09a3f9bd26c5632d0a`|true|
|`all-in-one/sources/decoded-original/0291-FlgNet.xml`|`fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550`|`1418fb2ed172c6df694a5eb8bf2dffd0b177653b`|true|
|`all-in-one/sources/decoded-original/0521-FlgNet.xml`|`8966080bc8e628f2604909960f79a060c150cc8fbb401b20f38c59a481cdd4d5`|`7cf0023ec0e3ad2f13d44d6bf91bb96d75b57407`|true|
|`all-in-one/sources/decoded-original/0540-FlgNet.xml`|`c05d5c1db35f1659992cae845cbcad515bbc34f00089169c0722076db9d77735`|`6b9a166d8fdf80bb52c63e90b794d69aaf34a919`|true|
|`all-in-one/sources/decoded-original/0549-FlgNet.xml`|`49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1`|`985b5310b43b1015b5dee286aa0e42800564b94b`|true|
|`all-in-one/sources/decoded-original/0562-IdentXmlPart.xml`|`85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c`|`1609802542a3e560baba3f2b73c306be281dfb23`|true|
|`all-in-one/sources/decoded-original/0563-IdentXmlPart.xml`|`86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad`|`6a10fc694f896cda16409804daf2554c91635654`|true|
|`all-in-one/sources/decoded-original/0564-IdentXmlPart.xml`|`2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1`|`c4b1f2cb191970cfce1cce59cb290a9f1f934c37`|true|
|`all-in-one/sources/decoded-original/0565-IdentXmlPart.xml`|`0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149`|`c2e3e2d57c94c5da864f6e172f0a7a925da942d6`|true|
|`all-in-one/sources/decoded-original/0594-IdentXmlPart.xml`|`88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd`|`f38b7d9a52b3d5ae74953da8290f6b417758c1b5`|true|
|`all-in-one/sources/decoded-original/0595-IdentXmlPart.xml`|`10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52`|`1f24565efac58926dabf5b3fc54ad0e9537410b2`|true|
|`all-in-one/sources/decoded-original/0596-IdentXmlPart.xml`|`a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0`|`c8b2d1a05727b4ca44e2e4bed9fb58ba2b717576`|true|
|`all-in-one/sources/decoded-original/0597-IdentXmlPart.xml`|`60e292145fe54912a1da7510c8641a4f4c85efe62e1b5206ee3d92794a28de20`|`2831597d1879bd83f239e838dd4cbe6b3dc64e77`|true|
|`all-in-one/sources/decoded-original/0598-IdentXmlPart.xml`|`dc001c9370a691546c5dea79f5a1252d6d0a5564754703018c47df4bcc2522bb`|`17a4c24ebc97eb13db483e4c64ac386d6a69125a`|true|
|`all-in-one/sources/decoded-original/0611-IdentXmlPart.xml`|`0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089`|`bad6b16fb32a32d47d882f48754994887457872b`|true|
|`all-in-one/sources/decoded-original/0612-IdentXmlPart.xml`|`95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38`|`7cc782d33d07ef225c2104f3e7c9fbd31f7c7467`|true|
|`all-in-one/sources/decoded-original/0672-IdentXmlPart.xml`|`6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222`|`2f2790dab4bb2357733112220e0acc41edb6feb6`|true|
|`all-in-one/sources/decoded-original/0674-IdentXmlPart.xml`|`4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84`|`f210593944547b63eab10c667348711413600aab`|true|
|`all-in-one/sources/decoded-original/0676-IdentXmlPart.xml`|`c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59`|`1ed67265f69796a4e659f9438e551068037f33a4`|true|
|`all-in-one/sources/decoded-original/0678-IdentXmlPart.xml`|`51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382`|`7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc`|true|
|`all-in-one/sources/decoded-original/0680-IdentXmlPart.xml`|`fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95`|`c9049ced1eaed72c5e251a88601d46ddec8c3e50`|true|
|`all-in-one/sources/decoded-original/0682-IdentXmlPart.xml`|`25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092`|`61182411e912941161eccf4e90c1f174e5379f0a`|true|
|`all-in-one/sources/decoded-original/0683-IdentXmlPart.xml`|`0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22`|`662acdb9a06c0ba1c0027e7dd215a28f07d3f02b`|true|
|`all-in-one/sources/decoded-original/0684-IdentXmlPart.xml`|`6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208`|`d67b98b5d5516e0330aae5cfdbee41a3e09206e1`|true|
|`all-in-one/sources/decoded-original/0686-IdentXmlPart.xml`|`b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4`|`8c152d926692a8e15973c980e08e338d29411814`|true|
|`all-in-one/sources/decoded-original/0688-IdentXmlPart.xml`|`ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda`|`463585759f1ecd94f32362b4fefb000a152f5773`|true|
|`all-in-one/sources/decoded-original/0692-IdentXmlPart.xml`|`bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037`|`737785d03b5fad43c5b4d451955726d800edb1c0`|true|
|`all-in-one/sources/decoded-original/0694-IdentXmlPart.xml`|`757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d`|`c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d`|true|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|true|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|true|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|true|
|`all-in-one/sources/source-manifest.json`|`5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf`|`38cf407491d52dc6128cf94ca8a4bddee350de6d`|true|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|true|
|`docs/equipment-standard/WORK-ITEM-TEMPLATE.md`|`4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586`|`e546f39535d2b589e80f97db869ac37ce4d05cfd`|true|
|`docs/equipment-standard/WORK-STANDARD.md`|`05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99`|`f76a570cc73098632e08759b17934000f7e3a253`|true|
