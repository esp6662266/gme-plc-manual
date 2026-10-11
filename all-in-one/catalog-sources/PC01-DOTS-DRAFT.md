# PC01 집진 흡인 압력 — 7영역 원본 조사 초안

## 핵심 확인·상충·인계

- PC01은 OEM FG76/PDF77의 **4–20mA, −/+200 mbar 표기 계기**다. 원시 입력 `%IW322:P` → FC63 → `Data.PC_01 DB1.DBW244` → FN04 단계조절 경로를 원본 선언·핀으로 확인했다. **PSH01 %IW284 → Press_PC01 DB1.DBW134 → MV02 CONT_S**와 서로 다른 데이터 경로다. PC02 소프트웨어 명칭과도 병합하지 않는다.
- FN04 관련 `0214`의 제목은 `dp-01 control loop`이지만 실제 연산 in1은 **Data.PC_01**이다. 압력 오차 Local Int를 이용한 +1/−1 단계조절이며, PSH01 쪽의 Real/CONT_S를 이 PC01에 복제하면 안 된다.
- Low_Aspiration(DB3.X4.5)은 **ON AND FN01 처리 Run AND FN04 처리 Run** 아래 압력 비교 3개 OR → **S5T#30S / T115** → Set다. Reset도 같은 두 팬 선행조건 아래에 있으며 **압력이 정상으로 돌아왔는지 확인하는 비교가 없다**. 알람 해제와 압력 정상·안전 재기동을 구분한다.
- PC01_OFR(DB3.X24.4)은 FC63의 일반 Coil/ENO 출력이고 Low_Aspiration S/R과 다르다. −9999 sentinel은 Low_Aspiration의 `<−800` 조건에도 들어갈 수 있다. 이 문서로 현행 경보·안전값을 제안하거나 변경하지 않는다.
- OEM FG76/PDF77 footer 기본일자는 27.05.2024, 별도 개정 표기는 관찰되지 않았다. FG108/PDF109는 기본일자 27.05.2024, **Rev2 17.03.2025**를 실제 렌더에서 판독했다. 서로 다른 페이지의 개정란을 일괄 적용하지 않는다.
- 공유 근거: BF01/PSH01 초안을 탐색 인덱스로 사용한 FC63·HMI 호출·공통 알람 Word 구조. 원본 Git blob 일치를 먼저 확인하고 PC01의 실제 결속·범위만 독립 대조했다. 고유 핵심: 0523, 0214, 0535, 0213, 0470 및 PC01 선언·전기 2쪽. BF01 세정/차압 경보는 PC01 고유 경보로 가져오지 않았다.
- 주요 누락: 현행 계기명판/압력취출 위치·센서/AI 설정·교정표·HMI 화면 이벤트·현재 CPU 실행순서/스캔·승인 복구 절차. 시공/P&ID 문자 검색에서 PC01 결속을 얻지 못했으며, 이를 물리 미설치 증거로 쓰지 않는다. 새 현장자료 없이 실물 보류를 반복 조사하지 않는다.

## 작업 기준과 경계

- catalog PC01, sensor/계측, 부모 없음, depth0, phase2, priority 없음. INVENTORY catalog[2], 배정 TASK3-BATCH06-SCOPE.json 및 GME-CATALOG-OVERLAP-REVIEW.json 해당행, 별칭 pc_01. 전체 신규132 자체문서 조사 중 한 ID이며 로컬 2차133 통합 제외 유지. FN04·PSH01·PC02·PSL05를 함께 완료로 세지 않는다.
- 고정 원본 `gme-research/source-mv06`, 커밋 `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION v1.12.0. AGENTS, 저장소 스킬/source-map, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, START-GPT61, VERSION/WORKSPACE-HANDOFF/PUBLICATION_STATUS/EXPANSION-WORK/ACTIVE-WORK 최신 항목 읽음.
- 배정의 문서전용·병렬 승인 범위가 작업방법을 정한다. 원본 preflight/build/test/generator 실행 없음. 자체 XML 파싱·문서 해시·PDF 렌더만 수행. 실제 모델명/추론수준의 런타임 증명 미확인. 로컬 TIA 추가접근권한 없음.
- 쓰기는 `drafts/PC01-DOTS-DRAFT.md`, `extracts/PC01/`만. 원본·코드·대장·다른 초안/공용추출·버전·배포·운영기록·SEJIN 변경 없음. 시뮬레이터 작성/수정/생성/실행/행동시험, PLC/현장/보호값 변경 없음. 재위임·새 Work/Codex 생성 없음.
- 아래 상대경로는 원본 `all-in-one/` 기준. 4자리 XML 번호는 `sources/decoded-original/####-FlgNet.xml` 또는 IdentXmlPart.xml. 파생 document ID와 원본 선언 NID를 구분한다. 파일 해시는 전체 의미검토 완료 수가 아니다.

## 7영역 적용표

| 영역 | 상태 | 확보한 근거 | 미확정 경계 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | 고유 ID, IW322, 도면 판본, PSH01/PC02와 분리 | 현행 실물/공정 압력탭 |
| I/O·HMI | 적용/일부 미확보 | Int 원시/환산, Word 원시미러, Bool 경보, 주소11행 | 화면 이벤트·쓰기권한·단위/배율·현재값 |
| 제어 | 적용/일부 미확보 | FC63, FN04 단계조절, 다른 Writer/제한/출력 | 현재 호출·스캔 최종값·통신 Writer |
| 전기 끝점 | 적용/일부 미확보 | +24V→X1→PC01→AI MOD4 PEW322 | 준공 케이블/명판·현행 채널·실배선 |
| 알람·복구 | 적용/일부 미확보 | OFR/Low_Aspiration 분리, 30초 S/R, 버너 경계/Word 겹침 | 현장 복구·경보 UI·안전 검증 |
| 증상 관찰 | 적용 | 비교할 값·지점·원인배제·증거 항목 | 실제 관찰/조치 없음 |
| 완료·누락 | 적용 | 해시·정적단언과 운영검증 분리 | 독립검토/통합/UI/게시/TIA/CPU/현장 |

## 1. 설비·자료 기준

PC01 전기도는 `PRESSURE CONTROL PC-01`, 출력4–20mA, 범위 `-/+200 mbar`를 기재한다. PLC 심볼 설명 pressure control, 대장 집진 흡인 압력, FC filter의 PC_01 사용은 문서상 연결이다. 흡입압의 기준압(게이지/절대/차압), 실제 취출 위치, 설치형식·제조사/모델·교정범위는 이 자료만으로 확정하지 않는다.

PC01이라는 글자가 포함된 모든 변수를 동일 계기로 취급하지 않는다. `0676` RID99 Press_PC01(AO1072)은 PSH01 환산 결과, RID308 PC_01(AO1952)은 이 PC01 결과다. `0668/0669`의 Local Real_PC01/Real_SPPC01과 `0476` CONT_S는 PSH01/MV02 관련 별도 조사 범위다. `live_index`의 과거 comment pc01/pc02와 현재 member 명칭이 다를 수 있으므로 comment를 현행 물리 태그로 승격하지 않는다.

시공 `Electrical_Can_Decoating_20241118.pdf`의 파생 page-text 및 P&ID 텍스트에서 PC01 결속을 얻지 못했다. 검색 음성 결과는 계기 부재·시공 누락·미연결 증명이 아니다. 이번 전기 직접 검토는 OEM 2쪽이며 시공도/P&ID의 전체 페이지 의미검토를 주장하지 않는다.

## 2. I/O·HMI

### 2.1 고유 선언과 주소

| 항목 | 형식/주소 | 원본 선언·참조 | 의미/경계 |
|---|---|---|---|
| PC01 환산 원시 | Global Int, Input %IW322, SAM=Peripherie | 0678 RID305 AO2576, NID42 UID1584 | `:P` 주변장치 접근 |
| PC01 HMI 원시 | Global Int, Input %IW322, SAM=None | 0627 RID90 AO2576, NID2 UID106 | 프로세스 이미지 접근, 위와 동일 시점 보장 없음 |
| Inputs.PC_01 | Global Word DB13.DBW54 | 0629 RID92 AO432 BAD4→0628 Inputs TOD13, NID2 UID107 Write | 원시 16비트 미러, 환산압력 아님 |
| Coeff.ZERO_PC01 | Global Int DB4.DBW124 | 0676 RID307 AO992 BAD8→0674 Coeff TOD4, NID42 UID1586 | 환산 영점 입력 |
| Coeff.COEFF_PC01 | Global Int DB4.DBW126 | 0676 RID306 AO1008 BAD8, NID42 UID1585 | 환산 계수 입력 |
| Data.PC_01 | Global Int DB1.DBW244 | 0676 RID308 AO1952 BAD11→0674 Data TOD1, NID42 UID1587 Write; 0596 RID256,0684 RID82 Read | 환산 결과 |
| Allarm.PC01_OFR | Global Bool DB3.DBX24.4 | 0676 RID428 AO196 BAD354→0674 Allarm TOD3, NID42 UID23 Write | 범위오류 출력 |
| Coeff.SET_PC01 | Global Int DB4.DBW198 | 0596 RID257 AO1584 BAD7→0595 Coeff TOD4, NID19 UID1974 | FN04 조절 목표, 현재/승인값 아님 |
| Flag.FN_04_AUTO | Global Bool DB2.DBX9.2 | 0596 RID254 AO74 BAD253→0595 Flag TOD2, NID19 UID1972 | 단계조절 허가 |
| App02 | Local Int, AO16 | 0598 RID258 NID19 UID1975 Write, UID24/29 Read | PC_01−SET_PC01의 임시값. 다른 블록 App02와 분리 |
| Data.SET_PERC_FN04 | Global Int DB1.DBW10 | 0596 RID252 AO80 BAD2→0595 Data TOD1 | 증가/감소·기동·출력제한 다중 Writer |
| Data.FN_04_ASPIRATOR | Global Int DB1.DBW224 | 0596 RID262 AO1792 BAD2 | FN04 전류환산 경계. 압력값 또는 실제 속도가 아님 |
| Tag_133 | Global Timer %T5 | 0594 RID259 AO5, NID19 UID1993 Write | HMI 태그 아님, S5T#4S SD |
| Data.Min_Pressure_PC_01 | Global Int DB1.DBW80 | 0684 RID84 AO640 BAD3→0682 Data TOD1, NID9 UID824 | 저흡인 비교문턱 저장부 |
| Inputs.FN01 Run / FN04 Run | Global Bool DB13.X3.5 / DB13.X22.2 | 0684 RID162 AO29, RID163 AO178 BAD135→0682 Inputs TOD13 | 처리 응답, 실물 운전 판정과 분리 |
| Allarm.Low_Aspiration | Global Bool DB3.DBX4.5 | 0684 RID88 AO37 BAD10→0682 Allarm TOD3 | NID9 UID830 Set,833 Reset |
| Flag.RESET_ALLARM | Global Bool DB2.DBX6.0 | 0684 RID24 AO48 BAD15→0682 Flag TOD2 | 복구 완료가 아닌 Reset 요청 |
| Tag_109 | Global Timer %T115 | 0686 RID87 AO115, NID9 UID828 Write/829 Read | S5T#30S SD |
| FN04_SP | Global Word %QW336, SAM=Peripherie | 0664 RID105 AO2688 NID14 UID859 Write | :P 출력 워드, 실제 팬 속도/회전 피드백 아님 |

Global/Local은 ID.S와 SSD·BAD·TOD로 구분했다. 파싱에서 같은 RID/NID/UID를 가진 무관한 다른 블록 후보가 나와도 자동 병합하지 않는다. 예: 공통0291 ORef41/RID25는0612 상수−1382이며0631 Allarm1이 아니다. 0175 ORef249/RID1은0582 ON이며0648 Data 후보는 배제한다.

### 2.2 원시 HMI 전달

`0398` document1071/NID2의 Move99: ORef106/RID90→in W118, out1 W119→ORef107/RID92. 앞 PSH03 Move98.eno가 **W116→Move99.en**으로 들어간다. PC01은 rail 독립 Move라고 쓰면 안 된다. Move의 DisableENO 속성 및 선 연결과 현재 매스캔 실행은 별도다. Int 원시값을 Word 저장부로 복사하며 이 네트워크에 압력환산은 없다.

공유 상위 `0030` document1613/NID19는 Recipes Handler→HMI→HMI Output ENO 연쇄 뒤 NOT Simulation(1) Part37를 거쳐 HMI Inputs CRef28.en으로 이어진다(W31~33,42~44). 원본 고정 blob을 대조한 공유 근거다. 중지된 코드·시뮬레이터는 실행하지 않았고 Simulation 플래그의 현재 상태를 가정하지 않는다.

### 2.3 HMI 태그 설정 11행

`sources/hmi_plc_tags.csv`, 모두 Access Name PLC, 근거 문구 `dde.cfg 설정; 온라인 현재값 아님`.

| CSV 행 | HMI 태그 | 설정 주소 | 내부 ID |
|---|---|---|---|
|18|Allarmi_234|DB3,X24.4|00458|
|213|data_DB1_DBW80|DB1,INT80|002C4|
|266|Coeff_DB4_DBW198|DB4,INT198|0027E|
|281|data_DB1_DBW10|DB1,INT10|0026A|
|314|Coeff_DB4_DBW124|DB4,INT124|00243|
|320|data_DB1_DBW244|DB1,INT244|0023A|
|347|Coeff_DB4_DBW126|DB4,INT126|0021A|
|350|data_DB1_DBW224|DB1,INT224|00213|
|392|FN_04\AutoON|DB2,X9.2|001D7|
|495|Allarmi_38|DB3,X4.5|00167|
|740|I_PC_01|DB13,INT54|00057|

PLC Inputs.PC_01의 Word와 HMI INT54 해석 차이를 보존한다. CSV가 존재한다는 사실은 화면 버튼의 쓰기 이벤트·입력허용범위·권한·로그인·소수점/단위·알람문구·현재 통신품질을 증명하지 않는다. ZERO/COEFF/SET/MIN 값의 현재값을 추정하거나 안전값으로 권하지 않는다.

## 3. 제어 구조

### 3.1 PC01 고유 FC63 결속

`0523` document1775/NID42. ON Contact1595의 rail W1597, operand ORef1582/RID1 W1589, out W1596→CRef1576.en. ON은 %M0.0이며 이름만으로 항상TRUE라고 가정하지 않는다. CRef1576 RefId351/CodeBlock1588 RefId5는0672 FCBlock RID5 TOD63,0680 BlockInterfaceInfo RID351로 FC63 Signal linearization에 결속된다.

| 핀 | Wire | ORef/RID | 방향·형식 |
|---|---|---|---|
|IN0|1590|1583/1 ON|Input Bool|
|Analog_input|1591|1584/305 PC01|Input Int %IW322:P|
|Coeff|1592|1585/306 COEFF_PC01|Input Int|
|Zero|1593|1586/307 ZERO_PC01|Input Int|
|OutValue|1594|1587/308 Data.PC_01|Output Int|
|Out_of_range|24|23/428 PC01_OFR|Output Bool|

### 3.2 공유 환산 함수의 형식과 ENO 경계

BF01/PSH01에서 확인한 같은 고정 원본 `0291` document1658/NID1 및 `0014` document1659/NID2를 공유한다. PC01 고유 호출은 위와 같이 별도 확인했다.

- IN0 Contact255 아래 원시 Int `>−1382 AND <=32767`(Gt258/Le161). Convert164/167(Int→DInt) → Add170(원시+Zero) → Convert174(Coeff Int→DInt) → Mul177 → Div181(DInt 상수28000) → Move185(OutValue Int)의 ENO 연쇄다. App3/4/5/6는0611의 Local DInt. 정수 연산/형변환이므로 실수식과 정밀도·overflow·최종 Int 변환을 동일하게 취급하지 않는다.
- 식의 요약은 `((raw + Zero) × Coeff) / 28000`이나, 실제 연산은 위 원본 형식·ENO를 따른다. 범위조건과 실행권한을 생략한 연속 수학모델로 대체하지 않는다.
- 원시 `>32767 OR <=−1382`: Gt190/Le259→OR47(W35/48/49)→Move193.en, 상수−9999 ORef218/RID21 W252→OutValue ORef219 W253. Move193.eno **W21→일반 Coil23**, Out_of_range ORef24/RID26 W22. OFR을 S/R 래치로 바꾸지 않는다.
- `0014`의 **NOT IN0 Contact171**→Move162.en W172; Int0 ORef166/RID23 W169→OutValue ORef167 W170. 이 경로는 FC가 실행되고 IN0=false일 때의 함수 내부 쓰기다. PC01 호출 en도 ON이고 IN0도 ON이므로 ON=false라는 사실만으로 해당 네트워크가 실행되어 PC01이0으로 갱신된다고 단정할 수 없다.
- 도면±200mbar, 원시 숫자, Coeff/Zero, HMI INT 표시는 다른 층이다. 최종 PLC 정수의 mbar 배율·현재 채널구성·교정은 미확인이다.

### 3.3 FN04 압력 단계조절

`0214` document1901/NID19, title `dp-01 control loop`를 보존하되 실제 변수 PC_01을 우선한다. 원본0594/0596/0597/0598 선언.

1. Flag.FN_04_AUTO Contact2025/ORef1972 RID254(W1994), rail W2031. out **W2026**은 Sub1935.en, T5 Contact2027.in, NOT T5 Contact2029.in을 병렬로 허가한다.
2. Sub1935 Int: PC_01 ORef1973/RID256 W1995 − SET_PC01 ORef1974/RID257 W1996 → Local App02 ORef1975/RID258 W1997.
3. T5 Contact2027/ORef1976 RID259 W1998의 out W2028이 두 조절가지의 비교 pre를 허가한다.
4. 증가: Ge1945 App02≥Int5(ORef24/25,W22/23) → Lt1948 `Data.FN_04_ASPIRATOR <250`(ORef1979/1980,W2002/2003) → Add1951 Int1+SET_PERC_FN04(W2006/2007) → 같은 DB1W10 ORef1983 W2008.
5. 감소: Le1957 App02≤Int−1(ORef29/30,W27/28) → Gt1960 `SET_PERC_FN04 >20`(ORef1986/1987,W2012/2013) → Add1963 Int−1+SET_PERC_FN04(W2016/2017) → 같은 DB1W10 ORef1990 W2018.
6. NOT T5 Contact2029/ORef1992 W2021의 out W2030→SdCoil1970.in; S5T#4S ORef1991/RID267 W2020, operand T5 ORef1993 W2023. S5Time 저장 V1024를1024ms로 바꾸지 않는다.

증가측은 속도<250이 아니라 **전류환산 저장부 DB1W224**의 비교다. 감소측은 설정값>20. 오차−1/5 문턱의 비대칭을 임의의 ±5 데드밴드로 고치지 않는다. T5 자기접점 SD 구조를 관찰했을 뿐 실제 정확한4초 주기·현재 응답·스캔 최종값을 행동시험하지 않았다. Sub의 ENO 뒤에 조절가지가 직렬로 붙은 것도 아니므로 그 연산성공을 자동 허가로 설명하지 않는다.

### 3.4 다른 Writer·출력 변환과 FN04 소유

- `0213` document1900/NID18: Start FN04(Q17.1,0594 RID316) Contact1861→PBox1847(W1862), PLS50 4(M50.4,RID250) edge memory W1857, out W1858→Move1849. Int20 ORef1854/RID110 W1859→SET_PERC_FN04 ORef1855/RID252 W1860. 기동 edge의 별도 저장값 Writer다.
- `0470` document1689/NID14: ON877.out **W878**이 Lt828.pre, Gt836.pre, Mul844.en에 병렬로 연결. 설정<5이면 Move831가5를 DB1W10에(W865/866), 설정>100이면 Move839가100을 같은 주소에(W871/872) 쓴다. Mul844 Int는 설정 ORef857 W873 ×272 ORef858 W874 → FN04_SP Word %QW336:P ORef859 W875. 제한 Move들의 ENO가 Mul.en을 직렬 허가하는 구조가 아니다.
- 조절설정0을 단순 정지명령이라 단정하지 않는다. FN04 모터 소유 `0265` document1965/NID35의 Eq1005(SET_PERC_FN04=0, W1026/1027)는 다른4조건과 OR1003→RCoil1010 Flag.M_FN_04(W1031/1033)의 한 조건이고, 같은 설정에 위5하한 Writer가 존재한다. ON1038의 다른 가지1046→Coil1014 Start FN04는 요청비트 전달 경계다. 실제 스캔순서/최종값/현재 활성은 미검증이다.
- 이 초안은 PC01→FN04 설정 영향과 출력 워드까지의 자료 흐름을 작성한다. FN04 두 모터·인버터/접촉기·보호/실제 속도의 전체 수리문서를 다시 완료했다고 표시하지 않는다.

### 3.5 상위 호출

`0031` document1619/NID6 ON282.out W283→Analog input conversion CRef261 및 Allarms1/2/3 CRef264/267/270.en의 병렬 가지. `0549` document1620/NID7 ON350.out W351→Motors1/Filter 등.en; Filter CRef322/CodeBlock339는0688 RID70 TOD8(FC8),0694 RID71 인터페이스. `0032` document1621/NID8 ON352.out W353은 Valve control loop CRef341과 Analog output conversion CRef344.en을 병렬 허가한다(0688 RID88/0694 RID89). ENO 직렬 순서를 만들어 쓰지 않는다. 현재 CPU의 OB 호출/스캔 순서/통신 쓰기까지 증명하지 않는다.

## 4. 전기 끝점과 원본 렌더

### 4.1 OEM FG76 / 실제 PDF77

원본 `sources/Electrical_Rev2.pdf`, 렌더 `extracts/PC01/oem-p77.png`, 제목 PRESSURE CONTROL. footer DATA27.05.2024, DISEGN.G.G., NORMA IEC, FG76/TOT262; 별도 Rev 표기 미관찰.

1. +24Vdc 10.7이75/9에서 들어와77/0으로 이어진다.
2. PC01 가지: **X1:181의5×20,50mA F** 표기 보호 → 전선76.1 → 계기 `+`.
3. 계기 `−` → **X1:182 → +PEW322 /108/3**.
4. 차폐/드레인 경계 **X1:183 →76SCH1 /108/3**를 별도 보존한다. 이를 압력 신호−단자와 합치지 않는다.
5. 옆 PSL05는 X1:184의2A F·X1:185·E11.0 경로인 별도 접점이다. PC01의50mA F 보호나4–20mA 회로와 합치지 않는다.

이는 도면상 보호표기이며 현행 퓨즈를 같은 값으로 교체하라는 지시가 아니다. 안전 정비·실측은 승인된 절차와 적격 작업자 범위다. 케이블의 현행 외부 ID·심수·종단 라벨·압력튜브 경로는 이 OEM 페이지에 완결되어 있지 않다.

### 4.2 OEM FG108 / 실제 PDF109

원본 같은 PDF, 렌더 `oem-p109.png`. 제목 ANALOG INPUT MODULE, footer 기본일자27.05.2024, **Rev2 17.03.2025**, FG108/TOT262를 직접 확인.

- PC01 채널은 CPU:515 / MOD:4, **PEW322**. 76/2에서 온 +PEW322가 **I1+ pin6**으로 들어간다. **U1−/I1− pin8**은 공통−0Vdc10.6 선에 연결된다.
- 76SCH1 차폐는 입력선 옆 점선 shield와 묶이며 신호입력 pin6와 분리한다. 좌측 PSH03 PEW320(pin2/4), 우측 PEW324/326 SPARE MV04 표기는 별도 채널이다.
- 도면 CPU515/MOD4가 현재 설치 Siemens 주문번호·펌웨어/채널 측정방식·AI 설정·보호구성이 확인됐다는 뜻은 아니다. 단자번호/편극/전원/차폐의 현행 상태는 사진·명판·준공도·승인된 채널설정으로 대조해야 한다.

## 5. 알람·복구

### 5.1 Low_Aspiration 고유 발생·유지·Reset

`0535` document1987/NID9, title pc-01 low depressure. 세 가지 비교는 모두 Int이며 선언상 상수−10은0683 RID142,−800은RID85, 지연은RID86 S5Time S5T#30S(V4864)다.

- 선행: railW864→ON Contact856(ORef820 W834) →W21→FN01 Run Contact23(ORef24/RID162 W22) →W25→FN04 Run Contact27(ORef28/RID163 W26). Contact27.out **W857**이 비교3개와 Reset Contact860.in에 모두 연결된다.
- 발생OR: Gt797 `PC_01 >−10`(ORef821/822,W835/836) →OR796.in1 W837; Gt800 `PC_01 > Min_Pressure_PC_01`(ORef823/824,W838/839) →in2 W840; Lt803 `PC_01 <−800`(ORef825/826,W841/842) →in3 W843.
- OR796.out **W844**→SdCoil809.in과T115 Contact858.in. SdCoil value W845←ORef827/RID86 S5T#30S; operand W846←ORef828/RID87 T115. Contact858 operand ORef829 W847, out W859→SCoil814, 대상Low_Aspiration ORef830/RID88 W849.
- Reset: 같은 W857 아래 RESET_ALLARM Contact860(ORef831/RID24 W851) →W861→기존 Low_Aspiration Contact862(ORef832/RID88 W852) →W863→RCoil819, 대상ORef833 W854. **압력 정상범위 비교는 이 Reset 경로에 없다.** 두 팬 처리 Run가 false이면 이 네트워크의 Reset 경로도 선행조건을 통과하지 못한다.

직렬두팬·30초·래치·Reset조건을 그대로 보존한다. 현재 동시 Set/Reset 우선순위와 실제 스캔 표시, 팬 응답의 정상극성은 현장 미확인이다. 값−9999가 발생 비교 `<−800`에 포함되더라도 전기 OFR과 공정 저흡인 원인을 자동으로 같다고 판단하지 않는다. 원인 제거·센서정상·정상압력·버너재요청·현장복구는 별도 증거가 필요하다.

### 5.2 PC01_OFR과 공통 Word 경계

PC01_OFR DB3.X24.4는 FC63의 Out_of_range 일반 Coil/ENO 출력이며 별도 시간 S/R을 이 호출에 추가하지 않는다. 고유 직접 이름검색에서 이 비트의 추가 명명 Read는 확인하지 못했지만 간접/통신·HMI 전체 사용처 부재의 증명은 아니다.

공유 alarm manager `0151/0152`의 DB3W0,2,…16 복사/변화비교 범위에는 Low_Aspiration DB3X4.5가 포함되고 **PC01_OFR DB3X24.4는 포함되지 않는다**. `0151` NID1 DB3W4 ORef177/RID15→Move137.in W198, out W199→WorkData.W2 ORef178/RID16. `0152` NID2 Ne197의 in1/in2는 ORef224/225 W246/247. 선언0565 AO32 BAD와0564 Allarm TOD3,WorkData TOD6로 결속했다. 다른8Word와 OR→NOT STOP_HORN→NEW_ALLARM; `0153`의 NEW_ALLARM→NOT RESET_ALLARM→NOT STOP_HORN 뒤 RUN_HORN Set/NEW_ALLARM Reset은 공유 경적관리 경계다. 실제 경적 출력·HMI 표시검증은 별도다.

startup `0148` document403은 network-map NID가 null이지만 선언0563 RID28 **NID3 UID290 Write, Word AO32 BAD23→0562 Allarm TOD3**가 DB3W4를 지정한다. Move256.out1 W311→ORef290, 값0(0048 RID54)이므로 Low_Aspiration에 겹치는 startup Word0 쓰기다. PC01_OFR는 이 startup W0~16 범위 밖이다. Startup 수행·현재 리텐션·CPU 값은 미확정이다. 별도 startup live_index doc401과 HMI output `0401-FlgNet.xml`을 혼동하지 않는다.

### 5.3 버너·FN04 영향과 재기동 경계

`0175` document1858/NID5에서 Low_Aspiration은0585 RID41 AO37(BAD Allarm) ORef246→Contact299 operand W264, out W300→12입력OR219.in9. OR219.out W267→ON Contact305(ORef249/0582RID1 W268)→W306→OR213.in5→W270→RCoil232 `Flag.Start_Burner`(ORef250/RID19 W272). 즉 GME 버너 시작요청 Reset에 영향을 주는 경로이며 외부 연소안전기의 내부 퍼지·화염·점화·트립을 이 문서에서 확정하지 않는다.

0265의 FN04 요청Reset 조건에는 PC01_OFR/Low_Aspiration이 직접 이름으로 나열돼 있지 않다. 이것만으로 팬이 어떤 조건에서도 계속 돈다거나 모든 간접영향이 없다고 할 수 없다. 위 압력 조절과 다른 설비의 정지/보호 소유를 구분한다.

공유 `0158` NID9의 물리 Reset 입력 또는 HMI Reset 요청→RESET_ALLARM Set/HMI요청 Reset 경로는 요청전달이다. 버튼조작·현장Reset·재기동은 수행하지 않았다.

## 6. 증상별 관찰·수리 준비

아래는 실행된 시험·운영기록이 아닌 관찰 설계다. 작업자/시각·시간대/프로젝트·장치/측정점/값·단위/비교원본/배제결과/승인조치/복구증거를 함께 기록한다. 제어값 강제·시험신호 주입·퓨즈교체·보호값 조정은 이번 범위가 아니다.

| 증상 | 먼저 관찰할 값·위치 | 비교·원인 배제 | 복구 확인에 필요한 증거 |
|---|---|---|---|
| PC01 HMI가 멈추거나 원시/환산이 다름 | IW322:P와일반IW322, DB13W54,DB1W244, 호출/통신품질 | 0398 Move99 ENO·0030 호출,0523 FC63, 읽기시각/형식 | 동일시각 원시·전류·환산·화면과채널/교정표 일치 |
| −9999/OFR 표시 | X1:181/182/183,4–20mA계기,MOD4 pin6/8,PC01_OFR | 센서전원/퓨즈/차폐/입력범위와Zero/Coeff,FC63 ENO | 승인된측정으로전원·전류·원시·환산및OFR정상 확인 |
| 압력방향/단위가 이상함 | 실제압력 기준·교정,도면±200mbar,DB4W124/126 | PSH01 Press_PC01/PC02와혼동,배율·부호·영점오인 | 명판/교정표/화면스케일/PLC채널설정 대응 |
| FN04 설정이 증가하지 않음 | FN_04_AUTO,T5,App02,DB1W224,DB1W10 | 오차≥5와전류환산<250,4초SD·다중Writer·현재호출 | 정상운전승인절차 안에서 요청→출력워드→실응답 관찰 |
| 설정이 감소하지 않거나20주변 | App02≤−1,SET_PERC>20,기동edge·출력5/100 제한 | 0214/0213/0470 Writer를순서·시각으로 비교 | 선택모드·스캔·통신Write 및 실팬응답 근거 |
| Low_Aspiration이 안 생김 | 두팬처리Run,ON,세압력비교,T115,지연시각 | 직렬팬허가가 없거나30초미충족·호출누락·Reset겹침 | 원시센서와 처리응답,현재프로젝트 및경보이력 |
| Reset이 안 되거나 해제후재발 | RESET_ALLARM,두팬Run,DB3X4.5,압력/OFR | Reset도두팬선행조건,정상압력비교없음,조건잔류/Word초기화 | 원인제거·정상압력·센서정상·경보재발없음 별도 확인 |
| 버너시작요청이 사라짐 | Low_Aspiration과0175 다른OR입력,Start_Burner | GME요청Reset과외부연소제어상태 분리 | 관련책임자의승인복구절차·현재안전상태·재요청증거 |

증상만으로 센서고장·현장극성·팬/버너안전 상태를 확정하지 않는다. 모든 실물·현장 조치는 별도 권한/승인자료가 필요하다.

## 7. 완료·누락·다음 단계

### 7.1 검토 깊이와 중복 절감

- 고유 핵심 네트워크 전체 구조 검토5개: 0523(환산호출),0214(단계조절),0535(저흡인S/R),0213(기동Writer),0470(제한/출력).
- 공유/경계 선택검토14개: 0398,0291,0014,0030,0031,0032,0549,0175,0265,0148,0151,0152,0153,0158. 해당 설비결속/선행조건·참조만 확인하며 네트워크에 함께 있는 모든 설비의 완료는 아니다.
- 탐색구조추출만3개: 0200,0219,0540. BF01 공통세정·차압 영역이 PC01 고유제어가 아님을 분리하기 위한 색인. 이3개 전체를 PC01의 추가 의미검토로 집계하지 않는다.
- XML추출22개, 핵심5개, 해시99파일, 실제PDF2쪽은 각각 다른 수치다. 전부 동일 의미의 완료 개수가 아니다. source archive zap18/PEData와중지5자산은 해시보존만 하며 실행·컴파일하지 않았다.

### 7.2 네 기능·운영 상태

| 항목 | 이번 결과 |
|---|---|
| 도면·래더 비교 | 원본쌍/핀/렌더를 초안에 정리,프로그램 UI 통합·왕복링크 미검증 |
| 백업·선택복원 | 운영기록/저장키 변경없음, PC01 저장·재읽기·재열기 시험 미수행 |
| 전후기록 비교 | 관찰항목 설계만, 실기록 없음 |
| 보고서/PDF | 원본PDF2쪽 렌더 검토, 앱보고서/PDF출력 구현·시험 안함 |
| documentation | complete_with_gaps / 초안, 독립검토 대기 |
| static_review | 자체선택원본 검토·19단언 통과, 전체앱 회귀 아님 |
| ui_records | not_run |
| publication | not_published / 이번초안에 대한 상태 |
| tia_compile / live_cpu / field_recovery | 모두 not_performed |

### 7.3 추가 자료와 수집 위치

1. 현장 계기명판·PC01압력취출/튜빙·단자라벨·준공케이블표: FG76계기/X1,FG108 MOD4 대응. 현재 모델·4–20mA·압력범위·극성을 확인할 자료.
2. 승인된 TIA 읽기결과·하드웨어채널설정·현재 프로젝트 대조: IW322:P/프로세스이미지, FC63/FC8/출력변환 호출·실제순서, T5/T115, 외부HMI쓰기를 확인할 자료. 이번에 추가접근권한을 부여받지 않았음.
3. 계기교정성적서·스케일명세·운전기준: ±200mbar와PLC Int/HMI표시배율, ZERO/COEFF/SET/MIN의현재·승인값을 별도로 확인. 백업저장값을 현행값으로 채우지 않는다.
4. HMI원화면/이벤트/통신·알람설정: CSV주소11행의실제표시·입력·권한·기록. CSV만으로입출력방향완료 불가.
5. 책임자승인복구절차/관찰기록: 원인제거·압력/센서정상·두팬응답·버너외부제어상태·재기동승인을 분리.

다음 작업 한 개: 부모가 PC01 초안의 고유5네트워크·전기2쪽·Reset선행조건을 독립 검토하고 전달한다. 새 현장 자료가 없으면 미확정 상태를 유지하며 다음 배정설비로 진행한다. 원본초안 전달 후 보강은 별도 파일로 관리한다.

### 7.4 실제 작업 시각(UTC)

- 2026-10-11 10:39:40: 배정 수신, 범위/공통지시 읽기 시작.
- 10:40:31: 자체 XML 첫 추출 11네트워크, 고유환산·조절·알람 구조 확인.
- 10:41:03: OEM PDF77/109 실제 렌더와 footer/끝점 판독 완료.
- 10:41:28: 부모에게 핵심 Low_Aspiration Reset 경계 보고.
- 10:42:48: 호출·다중Writer·Word겹침으로 확장한 XML22네트워크 추출 완료.
- 10:44:00: SHA256/Git blob 99파일 일치,중지5보존,자체19단언 검사 완료.
- 초안 완성/최종재검 시각은 아래 최종 검사에 기록한다. 위 시각은 도구 실행/메시지의 실제 시각이며 예상 소요시간이 아니다.

## 부록 A. 원본 파일 전체 SHA256·고정 Git blob 대조

아래99개는 선택근거/문맥·해시보존 대상 전체다. 모든 행의 파일내용이 고정 커밋 Git blob과 같음. SHA256는 작업트리파일에 계산했고, 같은 blob bytes에 별도 계산해 확인했다. Git blob OID는 SHA256가 아닌 Git객체 ID다. 원본 전체저장소의 모든파일 의미검토를 뜻하지 않는다. 상세 JSON은 `extracts/PC01/source-hashes.json`, 검사판정은 `static-review.json`.

| 원본 상대경로 | SHA256 | 고정 Git blob OID | 내용일치 |
|---|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | yes |
| `.agents/skills/gme-equipment-rollout/references/source-map.md` | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` | yes |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | yes |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | yes |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | yes |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | yes |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | yes |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | yes |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` | yes |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` | yes |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` | yes |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` | yes |
| `all-in-one/registers/sensor-measurement.json` | `4b8c357c803e7b429766d54a87bf49bb5dd25343a9797b44b5702df93440c7a3` | `e032d23b1f3163dcf95390589c93e2e9dcda474e` | yes |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` | yes |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` | yes |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | yes |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | yes |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` | yes |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` | yes |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | yes |
| `all-in-one/sources/can-decoating-page-text.json` | `d3b4c14945dd00f79c58ebab0cb8991c422dd1670e95e24d10779bd9e9d99bba` | `2bebec2c719fa57ed6c9f8d4e541e8848dc0d732` | yes |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` | yes |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | yes |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | `653d27572de6beedcf3eb6c95702bb119a8b567f` | yes |
| `all-in-one/sources/decoded-original/0032-FlgNet.xml` | `070bb8efa33d03b18add5da81d3f670a47c12b288076b7bfee11ac87fe6fa7e4` | `e31cf9aeecfbfc0c264921ac217cbd15479c1f34` | yes |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` | yes |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` | yes |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` | `3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3` | yes |
| `all-in-one/sources/decoded-original/0151-FlgNet.xml` | `227627d165c6240a4c15b62fd4e4c8d7a621c15f35319cb424601df5cc52c904` | `8e8a9801d1f57180fc3747f6515c0353f38f7dc5` | yes |
| `all-in-one/sources/decoded-original/0152-FlgNet.xml` | `2b6165460f06a52de56afcb4d65ed163d64320e24af1b194e934a4d7c6bfe49f` | `dd8e35b98043d9d0f230351352273eac1d783990` | yes |
| `all-in-one/sources/decoded-original/0153-FlgNet.xml` | `3d3a236a66a7a5c9b8e2d1e15da63cc943ba5cd266949583cbac6ffbb2f88bc6` | `d50223c45f5eb1d1c1d3530b41db1e79ad6c71f3` | yes |
| `all-in-one/sources/decoded-original/0158-FlgNet.xml` | `d3f3adebc3d990b85c5d4c294906ae3bc3dafebb49d25b030bf9cc2ccf905651` | `233ccf8f9d82ffffa498e04cbdcd3de07115c1db` | yes |
| `all-in-one/sources/decoded-original/0175-FlgNet.xml` | `41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97` | `1626da00b3bbcb46f77720271ecf0f50db9dc63b` | yes |
| `all-in-one/sources/decoded-original/0200-FlgNet.xml` | `2bd1be34eb905a10d840c59aeb461464a1af418fa0ea3f2b8d0b3f88145eb27e` | `31eb4f3df5596c004278ef7b3ccf158ae3878079` | yes |
| `all-in-one/sources/decoded-original/0213-FlgNet.xml` | `1abacae20327c184c4a94d8c37283c7b5bdd5c8663d5ae35866cb0e29081e82d` | `1cb5485a3dbf7c6d2827857d220720161248db40` | yes |
| `all-in-one/sources/decoded-original/0214-FlgNet.xml` | `2d1487d9260e976cef67975583353b10acab2dbff8da535f8391b422d330e8fa` | `812c34c104d4f6bee2bc1061c302a26e2771d806` | yes |
| `all-in-one/sources/decoded-original/0219-FlgNet.xml` | `245409937abf7e28f25a24d4a6d311a801a4b2ee7293148be9b3d266352eb53a` | `d1c9ae9d9fe8a5a1ed605d09a3f9bd26c5632d0a` | yes |
| `all-in-one/sources/decoded-original/0265-FlgNet.xml` | `f2471b6ab6169e4c082983ea2080a383cf8b13cba4503a9a07f83d0956fbf08a` | `bde7b86a1047ae2eb0508311a6910c0ae2d47a97` | yes |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` | yes |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` | yes |
| `all-in-one/sources/decoded-original/0470-FlgNet.xml` | `4f1003dd1f030ae86992225fbd485e669e64fc9d401beb28e9138fc9f012591b` | `36e79fd3e7debedc0274e577282709bc13a131c2` | yes |
| `all-in-one/sources/decoded-original/0523-FlgNet.xml` | `4da713a99dd583d5c9833d1104daf666eb026acaf056d8d184bd07e25c885b7f` | `82827a212392935ad9343a2a93a9751c02cae9af` | yes |
| `all-in-one/sources/decoded-original/0535-FlgNet.xml` | `91bc05af3aa1c071a2eb84edd9031f555a0d339708360decc1ac18dc89cf4316` | `5207b7719ef8aed12a20d678a67cd6db8016e368` | yes |
| `all-in-one/sources/decoded-original/0540-FlgNet.xml` | `c05d5c1db35f1659992cae845cbcad515bbc34f00089169c0722076db9d77735` | `6b9a166d8fdf80bb52c63e90b794d69aaf34a919` | yes |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` | `985b5310b43b1015b5dee286aa0e42800564b94b` | yes |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` | yes |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` | yes |
| `all-in-one/sources/decoded-original/0564-IdentXmlPart.xml` | `2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1` | `c4b1f2cb191970cfce1cce59cb290a9f1f934c37` | yes |
| `all-in-one/sources/decoded-original/0565-IdentXmlPart.xml` | `0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149` | `c2e3e2d57c94c5da864f6e172f0a7a925da942d6` | yes |
| `all-in-one/sources/decoded-original/0566-IdentXmlPart.xml` | `a1914c7ae085acc1f949a649979824bec8b46fcd78a8055318272a1eb5a45265` | `348e6fccf44a8497f58f73e89ec98e892b2df436` | yes |
| `all-in-one/sources/decoded-original/0567-IdentXmlPart.xml` | `5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e` | `48d2fdc3a37b692bfda5234b3cd84c48269552f2` | yes |
| `all-in-one/sources/decoded-original/0568-IdentXmlPart.xml` | `4ea2540c76f86ab5b17a30c7c9182cc0026bc6b05e605eddcd4af6fc3b919f89` | `c3b9bb052c2200805c3d0af5237d41ebaafaaad5` | yes |
| `all-in-one/sources/decoded-original/0582-IdentXmlPart.xml` | `41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951` | `82636dec064876d0f4cc714ef385b07d6e05efe0` | yes |
| `all-in-one/sources/decoded-original/0584-IdentXmlPart.xml` | `3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d` | `0f8dde829be66041bea79e40ccc4586d84ff1da7` | yes |
| `all-in-one/sources/decoded-original/0585-IdentXmlPart.xml` | `e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184` | `16574d37ef3ca61b59ba396c400e269ab1dd3440` | yes |
| `all-in-one/sources/decoded-original/0594-IdentXmlPart.xml` | `88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd` | `f38b7d9a52b3d5ae74953da8290f6b417758c1b5` | yes |
| `all-in-one/sources/decoded-original/0595-IdentXmlPart.xml` | `10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52` | `1f24565efac58926dabf5b3fc54ad0e9537410b2` | yes |
| `all-in-one/sources/decoded-original/0596-IdentXmlPart.xml` | `a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0` | `c8b2d1a05727b4ca44e2e4bed9fb58ba2b717576` | yes |
| `all-in-one/sources/decoded-original/0597-IdentXmlPart.xml` | `60e292145fe54912a1da7510c8641a4f4c85efe62e1b5206ee3d92794a28de20` | `2831597d1879bd83f239e838dd4cbe6b3dc64e77` | yes |
| `all-in-one/sources/decoded-original/0598-IdentXmlPart.xml` | `dc001c9370a691546c5dea79f5a1252d6d0a5564754703018c47df4bcc2522bb` | `17a4c24ebc97eb13db483e4c64ac386d6a69125a` | yes |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` | yes |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` | yes |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` | `30e199288c147aa22d5ce8407178a391b89c6b1b` | yes |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` | `ced032fa747a8544abf17058ee5ebaa78ba9b23b` | yes |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` | yes |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` | yes |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | `9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e` | yes |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | yes |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | yes |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | yes |
| `all-in-one/sources/decoded-original/0631-IdentXmlPart.xml` | `8e5072374f8ef098de72fbf93965b2a7bb0965c0f803e397daa68588c0c38555` | `27aa5aef2b126820b4658362e4aad5ca6d709fee` | yes |
| `all-in-one/sources/decoded-original/0648-IdentXmlPart.xml` | `afaa47ae737d9333fe831ffac2b1d1388f108bb6a2b23d03554fa862f7edb454` | `3dd5101419fbe16bbce7814398209efd6508db82` | yes |
| `all-in-one/sources/decoded-original/0660-IdentXmlPart.xml` | `0bf4f4c46531f55324602f4f7b1a1e0b9e63df2c6278126f6e5cf1bc9a06509f` | `915de9b3f968310c45682bef86a91adc1fa06e75` | yes |
| `all-in-one/sources/decoded-original/0661-IdentXmlPart.xml` | `90672199fee355011f581d3287046894772f3f3b4cb78bbe0dd0d71bd488ac93` | `cea3653088f8fb5c77afcf715988039cb63e28ac` | yes |
| `all-in-one/sources/decoded-original/0662-IdentXmlPart.xml` | `1838040bfee800fdb3f13b126eaf69a9d178b17cecc0d59ae03e9185216a48a5` | `ba624f3460dc05e8ade4956cdfc2ec621edb4f73` | yes |
| `all-in-one/sources/decoded-original/0664-IdentXmlPart.xml` | `68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed` | `7ce2f1315d5a21d6b77869a59fc9fcb2f17e90e6` | yes |
| `all-in-one/sources/decoded-original/0668-IdentXmlPart.xml` | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` | `fe0f30d1eaae37783b0f03cb090353b3a3de3600` | yes |
| `all-in-one/sources/decoded-original/0669-IdentXmlPart.xml` | `754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2` | `f5bf8f3c41d2a07ba9dcfd8f400548be8cf51cd3` | yes |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` | yes |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` | yes |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` | yes |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` | yes |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` | yes |
| `all-in-one/sources/decoded-original/0682-IdentXmlPart.xml` | `25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092` | `61182411e912941161eccf4e90c1f174e5379f0a` | yes |
| `all-in-one/sources/decoded-original/0683-IdentXmlPart.xml` | `0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22` | `662acdb9a06c0ba1c0027e7dd215a28f07d3f02b` | yes |
| `all-in-one/sources/decoded-original/0684-IdentXmlPart.xml` | `6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208` | `d67b98b5d5516e0330aae5cfdbee41a3e09206e1` | yes |
| `all-in-one/sources/decoded-original/0686-IdentXmlPart.xml` | `b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4` | `8c152d926692a8e15973c980e08e338d29411814` | yes |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | yes |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | yes |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` | yes |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | yes |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | yes |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` | yes |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` | yes |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | yes |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` | yes |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | yes |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | yes |
| `docs/equipment-standard/work-items/FN04.md` | `7d053bfa3dbbeda11112fc9a08935f1bdf147461ca6c915c2349d83e615b8191` | `03aa880f4d5c958f89dd123f4901f8f92d13306c` | yes |

## 최종 자체 확인

실제 최종 시각: 2026-10-11T10:49:17.979102+00:00. 원본 선택99파일 SHA256·고정 Git blob 내용 일치, 중지5자산 freeze 해시 일치, 원본 Git status 변경0. 자체19단언 통과. XML22추출/고유핵심5전체/공유·경계14선택/탐색3을 구분했으며 PDF2쪽 실제렌더 확인. 원본/다른초안/운영기록·PLC·SEJIN 변경0, 시뮬레이터 행동0. 초안 독립검토·현장확인은 별도 미완료다.
