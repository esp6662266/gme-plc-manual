# SYS-COUNTERS 자체 원본 조사 초안

## 핵심 확인·상충·누락

- 한 catalog ID `SYS-COUNTERS`(생산량·가스·유량 계수, software)만 조사했다. BWF01/02·BR01 및 SYS-AUTO/ALARM/HMI의 완료 실적을 포함하지 않는다.
- **세 누적값을 분리한다.** 0524의 BWF 펄스 보고계수는 Int +1, 0170의 HMI 부분/총생산량은 설정 비율·Set_TH로 계산하는 Real 경로, 가스량은 별도 `control_stechio`의 백업 STL 색인 경로다. 실제 중량 계량값 하나로 합치지 않는다.
- **I20.1/I20.2 상충:** XML은 BWF01/02 Pulse, 실제 OEM PDF145/FG144는 MOD16 단자5/6의 E20.1/E20.2 모두 SPARE다. 원본 연결을 인정하되 실물 펄스원·결선·펄스당 톤수는 미확정이다.
- **계산 주기 상충:** 호출 블록명 `cyc_int2 ogni 1s`와 FC30 제목 `this fc is recalled every 1ms`가 다르다. /3600, /36000은 원문 계산상수이며 실제 CPU 주기 보증이 아니다.
- **중복쓰기:** 생산/가스 부분누적은 HMI Reset 외 0193 버너 기동 기억 조건에서도 0으로 쓰인다. 0485 CLIENT_1은 환산값 외 RUN/NOT RUN 계산·0 쓰기가 있고, 0486 대응 가지는 ON 대신 OFF다.
- **누락:** 원형 STL 줄바꿈·주석 경계, 현재 TIA/OB 주기·컴파일 형식변환, HMI 버튼 이벤트·표시배율, BWF 실물동일성, 펄스원과 검교정·누적 보존정책 미확보. 현장 보호·복구·현재값을 확정하지 않는다.
- **공유근거 재사용:** [BF01 초안](BF01-DOTS-DRAFT.md) §4.4의 공통환산0291과 [BR01 초안](BR01-DOTS-DRAFT.md) §4의 FG100/111 가스유량 전기경로를 같은 고정 원본의 참고근거로 연결한다. 이번 독립 대조는 0485/0486/0504 고유 핀과0524/0170/0157/0193, 호출0031/0024/0028, 실제 OEM PDF86/106/145다. 기존 설비 전체를 재조사하지 않았다.

## 1. 설비·자료 기준

기준은 `source-mv06`의 Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0이다. GME-STD-1.0.0/작업표준과 배치11 지시를 적용한다. INVENTORY catalog index37, equipment index246, phase2 software, 부모 없음. 별칭 reset_prod_count/reset_gas_count/conta_prod/conta_gas/count_rep는 검색어이며 같은 메모리·같은 실물을 뜻하지 않는다. BWF01/02를 P03/P04 또는 사용자 실물 설비에 배정하지 않는다.

원본 경로 축약: Flg/Ident는 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` / `NNNN-IdentXmlPart.xml`. 문서번호는 network-map/live_index의 document_id이며 XML 네자리와 다르다. NID/RID/UID를 블록·파일 문맥과 함께 대조한다. AO/BO는 비트 오프셋, TOD는 DB/FC 번호이다. Local 이름은 해당 블록 밖으로 병합하지 않는다.

모델 런타임/추론수준 증명은 미확인. 원본 build/test/generator·시뮬레이터·PLC·현장·보호값·SEJIN을 실행/변경하지 않았다. 이 산출물은 정적 문서 초안이며 배포/운영 기능 구현이 아니다.

## 2. I/O·HMI

|구분|백업 대응·형식|원본 결속·경계|
|---|---|---|
|BWF01/02 Pulse|I20.1/I20.2 Bool|0678 RID309/319 AO161/162, NID43 UID1722/1733; 입력영상 SAM=None. FG144 SPARE와 상충|
|에지기억|M51.0/M51.1 Bool|0678 RID310/320 AO408/409 UID1723/1734 RW; PBox bit, 물리입력 아님|
|보고계수|Data.BWF01_count_rep/02, DB1.DBW270/272 Int|0676 RID318/326 AO2160/2176; 0674 Data TOD1. 0524 NID43의 읽기/쓰기와0157 NID7의 별도0쓰기|
|BWF 유량원시|PIW264/266 Int|0678 RID30/46 AO2112/2128 SAM=Peripherie; 0485/0486 Analog_input. HMI 복사0398은 별도 입력 선언|
|BWF 처리값|Data.CLIENT_1/2 DB1.DBW176/178 Int|0676 RID33/49 AO1408/1424; 동일 네트워크 복수쓰기|
|설정비율·처리량설정|Data.SET_PERC_BWF01/02 DB1.DBW0/2 Int; Data2.Set_TH DB10.DBW0 Int|0577 RID182/189/193, 0576 Data TOD1/Data2 TOD10; 0676에도 별도 문맥 선언|
|생산량 중간값|Prod_h_bwf01/02, Prod_s_bwf01/02 Local Real|0581 RID188/190/200/201; FC30 내부값, HMI주소 아님|
|부분/총생산량|HMI_DB.Counter_PartialProduction/TotalProduction, DB41.DBD8/4 Real|0577 RID203/204 AO64/32; 0576 HMI_DB TOD41|
|부분생산 Reset|HMI_DB.ResetCounter_PartialProduction DB41.DBX50.3 Bool|0577 RID213 AO403; 0170 Contact66, RCoil80|
|가스 유량원시/처리|PIW364 Int → Data.MASSICO_FLOW_GAS DB1.DBW210 Int|0678 RID143 AO2912 Peripherie; 0676 RID146 AO1680; 0504에서 최솟값1 쓰기 별도|
|가스 부분/총량|Stechio.Consumo_GAS / Consumo_GAS_TOTALE DB5.DBD30/34 Real|0591 RID110/139 AO240/272 +0590 Stechio TOD5; 원본 선언과 STL색인을 구분|
|가스 Reset|HMI_DB.ResetCounter_GasConsumption DB41.DBX50.2 Bool|0591 RID137 AO402 NID7 UID26 읽기/37 쓰기; 0590 HMI_DB TOD41|

### HMI CSV 실주소

`all-in-one/sources/hmi_plc_tags.csv` 실제행7~11 및94: RESET_PROD_COUNT `DB41,X50.3` ID00463, RESET_GAS_COUNT `DB41,X50.2` ID00462, Conta_prod `DB41,REAL8` ID00461, Conta_prod_TOT `DB41,REAL4` ID00460, **Conta_gas1 `DB5,REAL30` ID0045F**, Conta_gas_TOT `DB5,REAL34` ID003F2. catalog 파생 control-spec의 HMI 5행은 Conta_gas1을 누락하므로 전체 HMI계수는 CSV로 보완한다. 설정 연결은 확인했지만 클릭/눌림/해제·접근권한·읽기/쓰기 방향과 현재 표시값은 CSV만으로 확정하지 않는다.

행735/737의 I_Flow_rate_BWF02/01은 DB13.INT30/28이며 CLIENT_2/1(DB1)의 처리값과 다르다. 0398 NID2 Move34/41의 ORef35→36,42→43은 원시 BWF01/02_FlowRate→Inputs.Flow_rate_BWF01/02 복사다. 0627/0629 선언으로 원시/DB 영역을 분리한다. 원시입력 전체를 다른 센서 소유로 이관하지 않는다.

## 3. 제어 구조·계산·호출·쓰기

### 3.1 펄스 보고누적: 0524 / 문서1776 / NID43

0678 ON RID1(M0.0) UID1721→Contact1772; W1773은 두 펄스 가지로 분기한다. BWF01 Contact1774의 operand ORef1722/RID309, W1775→PBox1676.in, W1747 ORef1723/RID310→bit, W21→Add1693.en. Int Add 입력 W1754/ORef1730=보고계수, W1755/ORef1731=Int 1(0675 RID147), W1756→ORef1732 같은 보고계수에 쓴다. BWF02는 Contact1776→PBox1700(W1777), bit ORef1734/W1760, Add1717 W22/in1 W1767/in2 W1768/out W1769→ORef1743이다.

PBox의 상승에지·기억핀 구조이며 타이머 누적·고속카운터 명령으로 바꾸지 않는다. 1펄스=1계수는 코드에서 보이나 1톤/펄스는 제목만으로 검증되지 않는다. signed Int 범위·오버플로 시 실제 운전 처리, 펄스폭/스캔 누락·접점 바운스·정상극성은 미확정이다.

### 3.2 보고 종료계수 Reset: 0157 / 문서935 / NID7

ON Contact335→NOT Flag.M_TDPRO_REPORT Contact337(W336/327)→PBox306.in(W338), bit=PLS50_5 M50.5(0567 RID50/AO405, W329). W334가 Move311와316의 en으로 동시에 분기한다. 0566 RID52 Int0→W330/332, out1 W331→Data.BWF01_count_rep, W333→BWF02_count_rep. 0565 RID53/55, UID323/325 Write. **HMI RESET_PROD_COUNT와 별도 경로**다. ON 및 보고 비트의 결합 상승경계이므로 제목의 보고종료만으로 실제 저장완료/한 번 실행을 보증하지 않는다. 보고장치 전송/기록 완료 이벤트는 미확인이다.

### 3.3 생산량 Real 적산: 0170 / 문서1849 / NID13

원문 핀계산은 BWF01 Data.SET_PERC_BWF01→Div22(in1 ORef23, in2 ORef24=100.0, out25=Local Prod_h_bwf01)→Mul38(in1 39=동일Local, in2 40=Data2.Set_TH, out41=동일Local)→Div84(in1 85, in2 86=3600.0, out87=Prod_s_bwf01). W26/34의 eno→en, W88은 다음 BWF02 Div30.en으로 이어진다. BWF02 Div30→Mul46→Div92의 출력95=Prod_s_bwf02도 같은 구조다. 0578 NID13 RID184=Real100.0/RID214=Real3600.0, 0581 Local은 Real. **입력 설정들은 Int 선언인데 Div SrcType=Real와 Mul AutomaticTyped가 함께 존재한다.** 따라서 의도식 `(설정비율/100)×Set_TH/3600`을 적되 숨은 변환·반올림·컴파일 동작을 검증했다고 주장하지 않는다.

누적 허가는 피드백 RUN이 아니라 출력영역 Consent Start BWF01/02(0575 RID198/202 AO50/51=Q6.2/Q6.3)이다.
- BWF01만: Contact61(01)→NOT Contact101(02)→Add126(부분)→eno W50→Add134(총). W128/129/130은 Prod_s01 + 부분→부분, W139/140/141은 Prod_s01 + 총→총.
- BWF02만: Contact72(02)→NOT109(01)→Add142/143. 두 허가 모두: Contact117/118→Add158/159(Card3), Prod_s01+Prod_s02+기존누적.
- 둘 다 거짓이면 이 세 누적 가지는 성립하지 않는다. 모두 참일 때 단독가지의 NOT가 중복 가산을 구분한다.
- Reset Contact66(ORef67=RID213)→Move69(0.0 in W71, 부분 out1 W73)→eno W82→RCoil80(Reset bit ORef96/W83). 총생산량에는 이 Reset의 0쓰기가 없다. Reset과 누적이 같은 호출에서 함께 가능하므로 관찰값이 영구히0이라고 보증하지 않는다.

0170에는 자체 적산 타이머가 없다. 0024/NID4: ON ORef185→Contact188(W187)→W189 CRef183.en, CodeBlock186 RID39; **0067 FCBlock RID39/TOD30**이 Auto start motors임을 원본 결속했다. 호출자 이름/제목의1s와 FC30 제목1ms 상충을 유지한다. 실제 인터럽트 설정·우선순위·지연·누락·현재 ON은 미확인이다.

### 3.4 유량 환산·가공값 복수쓰기

0485/NID5 CRef185(CodeBlock220 RID5) Analog_input=W236/ORef216 PIW264, Coeff=W237/ORef217 DB4.DBW210, Zero=W238/ORef218 DB4.DBW208, OutValue=W239/ORef219 CLIENT_1, Out_of_range=W24/ORef23 Allarm.Flow_rate_BWF01_OFR(DB3.X20.6). 이후 ON Contact260와 BWF01 RUN Contact262 아래 Int Mul198(SET_PERC×Set_TH→Local temp4 Int), eno W246→Div202(/Int100)→CLIENT_1 W249. NOT RUN Contact264→Move209(Int0)→같은 CLIENT_1 W253. 환산 출력과 계산값/0을 같다고 축약하지 않는다.

0486/NID6 CRef260 Analog_input=W311/ORef291 PIW266, Coeff=W312/ORef292 DB4.DBW2, Zero=W313/ORef293 DB4.DBW0, OutValue=W314/ORef294 CLIENT_2, OFR=W24/ORef23(DB3.X20.7). 대응 Mul273/Div277/Move284 가지의 앞 Contact335(W315/ORef296)은 **OFF M0.1**이다. 실제 ON/OFF값·스캔순서·ENO·Int 오버플로를 확인하기 전 '항상 아날로그' 또는 '항상 덮어쓰기'로 단정하지 않는다.

0504/NID24 CRef659(CodeBlock679 RID5): ON Contact697 en과IN0, PIW364→Analog_input W686, Coeff DB4.DBW70 W687, Zero DB4.DBW68 W688, OutValue→DB1.DBW210 W689, OFR→Allarm.Massico_Gas_OFR DB3.X23.1 W24. 비교Lt666는 Int 처리값<1(W690/691)이면 Move669 Int1→동일처리값(W692/694/695). **저값이 처리상1로 바뀔 수 있으므로 실제 무유량·완전영점을 추정하지 않는다.** 공통0291 환산 원문과 −9999/OFR는 BF01 공유근거를 참조하되 각 호출의 고유 핀/후속쓰기는 여기서 직접 대조했다.

### 3.5 가스량: 색인 STL와 원본 선언의 증거등급 분리

`live_index.json` segment `_7ev`, 문서1831/1836의 STL Code가 block_summary의 control_stechio 대응문구와 정확히 일치한다. 이들은 **평탄화된 백업 검색 색인 문자**이고 원형 STL 소스·실행가능 코드로 복원하지 않았다. 원본 LAD 핀을 만들어 넣지 않는다.

1831 문구는 Data.MASSICO_FLOW_GAS Int→ITD→DTR→Local GAS_FLOW Real을 표시한다. 0591 RID69 NID2 UID379는 원 Int 읽기,0589 RID70 NID2 UID384 Write/395 Read, NID7 UID598 Read가 Local GAS_FLOW를 지지한다.

1836 문구는 `AN Inputs.Burner On; JC fine`, GAS_FLOW/36000.0→Portata_al_secondo, 부분 및 총 Consumo_GAS에 +R/T, fine 이후 별도 HMI Reset 검사→부분0→Reset bit R을 표시한다. 이름 Portata_al_secondo와 /36000.0를 /3600으로 고치지 않는다. `azz:` 레이블과 `ju fine`도 남아 있으나 평탄화된 주석·줄바꿈과 분기 도달성은 원형 STL에서 확인해야 한다. 부분0은 총량0과 다르다.

원본 선언0591 NID7 Consumo_GAS RID110 UID617 Read/620·629·34 Write, 총량RID139 UID42 Read/45 Write, Reset RID137 UID26 Read/37 Write를 별도로 대조했다. 0589 Local Portata_al_secondo RID108 UID38 Write/40·615 Read, Real AO272이다. 0590 TOD로 DB5와DB41을 결속했다.

0028/NID13 ON513 operand ORef26, W24→CRef508.en, CodeBlock511 RID109; 0069 FCBlock RID109/TOD13=Control_stechio. 호출자 `cyc_int5 ogni 100ms`와 FC제목100ms는 백업 문자이며 실제 CPU 주기는 미확정이다. m³/h 입력이 실제100ms마다 적산된다는 조건일 때 /36000의 시간환산 취지와 일치하지만 실제 단위·보정·가스 종류·표준상태를 확정하지 않는다.

### 3.6 다른 소유자의 부분값0쓰기·타이머

0193/NID25에서 (Flag.Start_Burner Contact24 OR Flag.AUTO_BURNER25)→O26→NOT memoBurnerON27→Inputs.Burner On28, W69가 SCoil29, Move30/113/119로 분기한다. Move113 W117=Real0.0→W118/ORef115 Stechio.Consumo_GAS, Move119 W123=Real0.0→W124/ORef121 부분생산량이다. 0585 RID260/262 Write와0584 TOD5/41 확인. 생산·가스 공통 Reset 하나로 병합하지 않는다.

같은0193의 memo31→NOT BurnerOn32→NOT PS181_0 Contact78→W91 LRef88.IN, PT W93/ORef95=T#1m(0586 RID254 Time60000), Q W108→PBox109, bit PS181_0 M181.0, W111→Add34가 Counter_StopBurner를 +1한다. 0587 Instruction RID252=TON, EN/ENO=false LRef이며 S5 타이머가 아니다. 이 타이머는 버너 정지계수 소유이며 생산량/가스 적산 주기라고 해석하지 않는다. 상세 버너 내부 안전 순서는 BR01/외부 전용반 범위다.

공통 호출0031/NID6 ON Contact282→CRef261.en, CodeBlock273 RID55;0688 FCBlock RID55/TOD3=Analog input conversion. 동일 main의 다른 알람 호출261/264/267/270 연결과 인터럽트 쓰기 우선순위는 현재CPU 확인 전이다. 모든 코드 경로·간접주소의 전체 쓰기 전수보장은 하지 않는다.

## 4. 전기 전달 경로

SYS-COUNTERS는 software이므로 전용 모터·보호기·독립 단자함 자체는 비해당이다. 관련 계측 끝점은 적용하며 하위 실물 소유로 완료처리하지 않는다.

이번 실제 PDF 렌더3페이지: `Electrical_Rev2.pdf` PDF86=FG85, PDF106=FG105, PDF145=FG144. 각 footer DATE27.05.2024/DESIGN G.G./IEC/총262이며 페이지별 개정란은 공란이다. 파일명 Rev2를 개별페이지 개정2로 옮기지 않았다.

|관련경로|실제 원본 끝점|누락·상충|
|---|---|---|
|BWF01 유량|FG85 X1/252(+)·253(−)·254(85SCH5)→+PEW264/−PEW264→FG105 MOD2 단자22 I4+,24 U4−/I4−|4–20mA 인쇄. 외부계기 모델·케이블번호·원격 끝단 미표기|
|BWF02 유량|X1/255(+)·256(−)·257(85SCH6)→PEW266→MOD2 단자26 I5+,28 U5−/I5−|같은 고정도면, 현재 배선·교정 미확정|
|BWF 레벨 참고|X1/258·259·260→PEW268 MOD2 30/32; X1/261·262·263→PEW270 MOD2 34/36|레벨 경로는 계수와 다른 입력, 이번 본체완료에 포함하지 않음|
|펄스 후보입력|FG144 MOD16 E20.1 단자5, E20.2 단자6, 모두SPARE|외부 전선 없음. I20.1/2 XML 태그만으로 펄스 발생기·단자·톤단위 확정불가|
|가스유량 공유|BR01 초안 원본 FG100/PDF101: 버너반X1/7/1→GME X1/407→+PEW364, X1/7/2→408→−PEW364,409→100SCH3;FG111 MOD5 30 I6+/32 U6−/I6−|FIT2001/4–20mA는 공유문서 근거. 전용반도면010-390 및 현행계기 자료 미확보. 이번 새렌더 대상은아님|

FG105 전원표시는 +24Vdc10.7→X21/3000 500mA F→MOD2 41 L+, −0Vdc10.6→44 M이다. 현재 보호설정/실물 모듈 형식의 증명으로 쓰지 않는다. FG144 encoder MV01 CH0.A/B/N과 SPARE E20.1/2는 다른 단자군이다. 인접 인코더를 BWF 펄스원으로 배정하지 않는다.

## 5. 알람·Reset·복구 경계

- BWF 유량OFR·가스유량OFR는 각 환산 호출 Out_of_range 쓰기다. 표시·공통 Word 알람·경광등·ACK는 SYS-ALARM 공통소유에 연결하며 생산량 오류 전용알람을 발명하지 않는다.
- 보고계수 Reset(0157), 부분생산 Reset(0170), 가스 Reset(색인1836/선언), 버너기억에 의한 부분값0(0193)을 구분한다. 총생산/총가스의 현장 리셋·시작값·전원복귀 보존정책은 미확보다.
- Reset bit의 RCoil 또는 STL R 문자는 물리계기 영점교정·교정승인·복구완료를 의미하지 않는다. 사용자 기록 보존과 PLC 누적 보존은 별도이다.
- ON/OFF는 M0.0/M0.1 실제메모리 선언이다. 이름만으로 상수 True/False로 바꾸지 않는다. 현장 시험·Reset 조작·쓰기·보호값 변경은 이번 범위에서 하지 않았다.

## 6. 증상 관찰·필요 증거

|증상|읽기 전용으로 구분할 관찰|판정 전 필요한 자료|
|---|---|---|
|BWF 보고계수가 멈춤|I20.1/2, PBox M51.0/1, Int보고값, 보고종료비트/PLS50_5의 같은시각 기록|실물 펄스원·폭·정상극성·승인배선;FG144 SPARE 상충해소|
|생산량과 펄스계수가 다름|DB1.DBW270/272 대 DB41.DBD8/4, Q6.2/3 허가, 설정비율·Set_TH|서로 다른 산정방식 승인, 실제중량·단위·주기·변환형식|
|부분값이 갑자기0|HMI Reset bit, memoBurnerON/Start_Burner/AUTO_BURNER/BurnerOn,0193조건|시간순 쓰기추적·현재 호출순서;Reset만 원인이라 단정금지|
|유량표시와 처리값이 다름|PIW264/266, DB13 원시복사, DB1.CLIENT1/2, ON/OFF,RUN,계수/Zero,OFR|Int곱셈/나눗셈 및 후속쓰기, HMI주소/스케일|
|가스량이 정지에서도 변함|BurnerOn 처리비트,PIW364, MASSICO_FLOW_GAS 최솟값1쓰기,부분/총가스,Reset|원형STL·현재이벤트주기·센서영점·스케일/단위|
|Reset 직후 값이 다시생김|Reset요청·RCoil,그후동일호출 누적 허가와다른OB쓰기|현재실행추적·HMI이벤트;즉시0유지약속금지|

관찰 기록에는 시각/시간대·프로젝트/CPU 버전·위치/주소·값/단위·수집장치·관찰자·원본비교·배제결과를 남겨야 한다. 실제 관찰·수리·회복 기록은 이번에 생성하지 않았다. 전기측정·현장조작을 지시하거나 모의시험으로 대신하지 않는다.

## 7. 완료·누락·자체검사

7영역 문서 초안은 complete_with_gaps. 정적 의미검토는 아래 한정범위에 수행했다. UI/기록 저장·재열기·도면래더 비교 기능 구현·백업복원·보고서 기능 검증·게시·TIA compile·live CPU·field recovery는 모두 not_performed/not_published이다. 모델 실행·시뮬레이터 시험도 미수행이며 재개대상이 아니다.

- native 의미검토:0524/0157/0170/0485/0486/0504/0193 7개 전체 핵심가지, 호출0031/0024/0028 3개(0031은아날로그호출중심),0398의BWF유량복사2가지. **11개 XML를 추출했다고0398 전체센서와다른호출까지전수의미검토한것은아니다.**
- STL색인2개(1831/1836)는 별도 문자·선언 대조, 원형STL 명령·주석·줄바꿈 복원/실행 미확인. declaration 원본과 CSV/PDF를 교차확인했다.
- network-map 전체 검색 및 control-spec 연결개수는 탐색 계수다. SYS-COUNTERS에 연결된 모든 온도/압력/산소/MV PID 네트워크는 이 소프트웨어 고유 소유로 일괄완료하지 않았다. 미해석범위는그들 전체계산·알람·현재호출·모든간접쓰기다.
- 3개 PDF 페이지를 실제 렌더/시각대조했다. 공유 BR01 PDF 경로는 이전독립근거를 연결재사용하며 이번 렌더수에 합산하지 않는다.
- 선택된50파일 SHA256·고정Gitblob 내용일치목록은 아래 전부수록. 파일해시는 의미검토수/원본전체검증수와 다르다. 원본상태는 git status clean 확인, 모든 출력은 허용된 SYS-COUNTERS 경로에만 작성했다.
- 다음 필요자료: 원형 STL/현행OB cyclic interrupt 속성·FC30 제목상충 확인, BWF 펄스I20.1/2 승인배선 및 계량 스케일, HMI 버튼이벤트/표시단위, 누적 보존·초기화 규정. 새자료 없이는 실물동일성 보류를 반복조사하지 않는다.

### 수행 시각 (UTC, 실제 도구 관측)

- 2026-10-11 11:44:42 착수·배치지시/범위 읽기.
- 11:46:25.186051 핵심11 XML 및 선언 추출 완료.
- 11:47:00 PDF86/106 렌더 완료, 11:47:07 시각대조. 11:47:20 PDF145 시각대조 및SPARE상충 확인.
- 11:49:19 색인STL1831/1836와 block_summary 일치 대조 및선택50파일 정리.
- 최종 해시/자체검사 완료시각은 부록에실제도구시각으로추가한다. 추정 작업시간을 완료시각으로 쓰지 않았다.


## 부록 A. 전체 선택 원본 해시·고정 Git blob

검사완료 UTC 2026-10-11T11:53:20.239722+00:00; 50파일 모두 고정Git 내용과 byte 일치. source-mv06 git status clean. network-map 검색 426행, catalog 파생연결 54행은 의미검토 완료수와 다르다.

|원본 경로 (source-mv06 기준)|SHA256|고정 Git blob|내용일치|
|---|---|---|---|
|`all-in-one/registers/control-spec.json`|`1e495b32f1f11b910919fbd2945e842a019fce9a27a6a0d7298041a7fab00079`|`c7889fa3271dfd0043057dcaf486f4acae243b16`|yes|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|yes|
|`all-in-one/sources/block_summary.json`|`68253f9366908244a27ed461c66d465da7ec1723571f27deaa9a6f81a542de63`|`15b570a011645023dbfca2d5332a9e0ae3b0a7b6`|yes|
|`all-in-one/sources/decoded-original/0024-FlgNet.xml`|`a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67`|`379ccbabf7692e1df137b99bab1992dea22cc1f0`|yes|
|`all-in-one/sources/decoded-original/0028-FlgNet.xml`|`c369213b6556d0fcecac67ee7f12585fc0aa46845d70fedcbd461eb32b05c62a`|`333f0abc950f871ed0b3f1fce3036979a5762c84`|yes|
|`all-in-one/sources/decoded-original/0031-FlgNet.xml`|`76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65`|`653d27572de6beedcf3eb6c95702bb119a8b567f`|yes|
|`all-in-one/sources/decoded-original/0067-IdentXmlPart.xml`|`0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628`|`455f00638f1618f194b1c83d9c0c2f157663a902`|yes|
|`all-in-one/sources/decoded-original/0069-IdentXmlPart.xml`|`da5203cd92ccadfea2029aafb45a1e6e99443d7edbbcc2fd2f2927482564590d`|`26204ec172cabfadf54c1ad6a74013bfaae06a11`|yes|
|`all-in-one/sources/decoded-original/0157-FlgNet.xml`|`ba7e71fc52ea96bcc2faf598f00a38a7516a1bb0fa7a09b33fbce7ea57611bf7`|`fbbd16ae3a0fbc4ed3574ffa047738d2b12d6b05`|yes|
|`all-in-one/sources/decoded-original/0170-FlgNet.xml`|`68446701a3985b7a8c80b081c891c6490cc4e5cf326e3c609581ea7ece2ad25b`|`cc4789d48f665d451b53a9aa33db5bb8c6462bc3`|yes|
|`all-in-one/sources/decoded-original/0193-FlgNet.xml`|`2aa42ce6e35c90844bc07b302cd12815b20c0008ebf54e9961edf79078c7fd41`|`6662dad6274d5f646041d4fd8585762478710828`|yes|
|`all-in-one/sources/decoded-original/0398-FlgNet.xml`|`4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747`|`67ebb54daa55093487ea7e780f23ae2cf193c397`|yes|
|`all-in-one/sources/decoded-original/0485-FlgNet.xml`|`bb533c3ffb079c544e8072efaba05f720766b474de46cb312853f36cfa47afaf`|`dce83d09a4c1f6dd1dd4429220e9b20600cc2d01`|yes|
|`all-in-one/sources/decoded-original/0486-FlgNet.xml`|`ca0f8ee20a2c6afd8ecb974608d6773bbca6a3fd25248f8cb827a3e4e970d5d8`|`8e675199c9463917db7e0b357c11d9eab480289b`|yes|
|`all-in-one/sources/decoded-original/0504-FlgNet.xml`|`d428b8c440d03f708f397daeb83f622f68b518a018522bed8736aec84c58fbdf`|`d193edb16afbcccf851efb753f8f08838096a484`|yes|
|`all-in-one/sources/decoded-original/0524-FlgNet.xml`|`34dcc9bbe4bfc73ec332d0ca1dc44ea6a12eb11643bf99f7a196a740c2c9e19f`|`a00d18b4fe79f0e394e8423f63ac9f69e8e13a12`|yes|
|`all-in-one/sources/decoded-original/0564-IdentXmlPart.xml`|`2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1`|`c4b1f2cb191970cfce1cce59cb290a9f1f934c37`|yes|
|`all-in-one/sources/decoded-original/0565-IdentXmlPart.xml`|`0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149`|`c2e3e2d57c94c5da864f6e172f0a7a925da942d6`|yes|
|`all-in-one/sources/decoded-original/0566-IdentXmlPart.xml`|`a1914c7ae085acc1f949a649979824bec8b46fcd78a8055318272a1eb5a45265`|`348e6fccf44a8497f58f73e89ec98e892b2df436`|yes|
|`all-in-one/sources/decoded-original/0567-IdentXmlPart.xml`|`5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e`|`48d2fdc3a37b692bfda5234b3cd84c48269552f2`|yes|
|`all-in-one/sources/decoded-original/0575-IdentXmlPart.xml`|`40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06`|`07d5d2548e8f36252a346d0b83341e27c3cb14ba`|yes|
|`all-in-one/sources/decoded-original/0576-IdentXmlPart.xml`|`c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe`|`819b47160eaa6d08c212f71e5b5486ef5b55b6f2`|yes|
|`all-in-one/sources/decoded-original/0577-IdentXmlPart.xml`|`511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47`|`a505ebf7efd05a85850dc29559a4f71242bacae3`|yes|
|`all-in-one/sources/decoded-original/0578-IdentXmlPart.xml`|`0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b`|`070a79fb12139898dd44a17ab2061e795956b9c6`|yes|
|`all-in-one/sources/decoded-original/0580-IdentXmlPart.xml`|`fa748a6c1890f579d694fd5e561b2304f717da79e5352ca32152cc20e877c6ff`|`9bd503f23708fada1a1f871e0e52b0eb75e9aacf`|yes|
|`all-in-one/sources/decoded-original/0581-IdentXmlPart.xml`|`5d1d7372935d984aa2d701aa70bdb4555ee1e98d0b0c23806db7bda1ad9134c5`|`2614704e8c68a43d20f3fbb6b1d300b9f8b7199f`|yes|
|`all-in-one/sources/decoded-original/0582-IdentXmlPart.xml`|`41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951`|`82636dec064876d0f4cc714ef385b07d6e05efe0`|yes|
|`all-in-one/sources/decoded-original/0584-IdentXmlPart.xml`|`3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d`|`0f8dde829be66041bea79e40ccc4586d84ff1da7`|yes|
|`all-in-one/sources/decoded-original/0585-IdentXmlPart.xml`|`e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184`|`16574d37ef3ca61b59ba396c400e269ab1dd3440`|yes|
|`all-in-one/sources/decoded-original/0586-IdentXmlPart.xml`|`f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250`|`266989c590cf52f82e1553f8626a209b8c0b6e0b`|yes|
|`all-in-one/sources/decoded-original/0587-IdentXmlPart.xml`|`bab957ac7c180d9c91b4f904b29e9dbd5812c6ba8f7b9e0c7faf9708605b203e`|`67e84e4b8d43b7c5864ec40fcc2c9fbc2222b436`|yes|
|`all-in-one/sources/decoded-original/0588-IdentXmlPart.xml`|`def5646a0d1eacaae81518f0952c4ba8ada5ea38852463a1d463ff439f3d1905`|`07d012cdc3fb0662f8126f4c274a36288e3bfc9b`|yes|
|`all-in-one/sources/decoded-original/0589-IdentXmlPart.xml`|`846630f3832df93ccdcb0bf86a029546886f8cdba51cd952eed63257ee4540e2`|`5de11972e1fb84f02e4585a53fab478d54e203d0`|yes|
|`all-in-one/sources/decoded-original/0590-IdentXmlPart.xml`|`baff7271b3db646e8953c31d20b72f7b044b1154b689b15ca0fb38ebb44ad81c`|`5816a1fc640da97d27ec68c8c45f255a0bd60730`|yes|
|`all-in-one/sources/decoded-original/0591-IdentXmlPart.xml`|`2e165c44fc9df852ea3729b3ddb33dc0a74e4f8826676f9c5c5626e1dce033f8`|`407456d55041d82dd19e551f904a217a11478289`|yes|
|`all-in-one/sources/decoded-original/0627-IdentXmlPart.xml`|`08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb`|`61ebc0abbb2ca160e11e1da400a3f14a397d8bc5`|yes|
|`all-in-one/sources/decoded-original/0629-IdentXmlPart.xml`|`67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972`|`058129bb01e27f7a6a0d0293f332d745e5bab74e`|yes|
|`all-in-one/sources/decoded-original/0652-IdentXmlPart.xml`|`251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692`|`eee49f8301a6791748de9ab368159af8e8bc1585`|yes|
|`all-in-one/sources/decoded-original/0670-IdentXmlPart.xml`|`e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841`|`b9466007b14e5c4f5d353dca5734401317e2dc03`|yes|
|`all-in-one/sources/decoded-original/0674-IdentXmlPart.xml`|`4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84`|`f210593944547b63eab10c667348711413600aab`|yes|
|`all-in-one/sources/decoded-original/0675-IdentXmlPart.xml`|`b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3`|`d82a33b173c8dc0737fd890eb2a63a88a07d0831`|yes|
|`all-in-one/sources/decoded-original/0676-IdentXmlPart.xml`|`c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59`|`1ed67265f69796a4e659f9438e551068037f33a4`|yes|
|`all-in-one/sources/decoded-original/0677-IdentXmlPart.xml`|`69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3`|`b9437406a7e24f073ef88b8369cacc9ad4ecc5ac`|yes|
|`all-in-one/sources/decoded-original/0678-IdentXmlPart.xml`|`51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382`|`7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc`|yes|
|`all-in-one/sources/decoded-original/0688-IdentXmlPart.xml`|`ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda`|`463585759f1ecd94f32362b4fefb000a152f5773`|yes|
|`all-in-one/sources/decoded-original/0692-IdentXmlPart.xml`|`bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037`|`737785d03b5fad43c5b4d451955726d800edb1c0`|yes|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|yes|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|yes|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|yes|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|yes|

## 부록 B. 재현 자료

- `../extracts/SYS-COUNTERS/core-pin-declarations.md`: 선택 XML Part/Wire/해석 operand와 해당NID/UID 원본선언. 전체추출은 의미전수검토 증명이 아니다.
- `../extracts/SYS-COUNTERS/supplemental-declarations.md`: FC호출/TOD 및 가스Local·Global선언.
- `../extracts/SYS-COUNTERS/indexed-STL.json`: 원형STL이아닌 색인1831/1836와 block_summary 문자일치.
- `../extracts/SYS-COUNTERS/source-hashes.json`, `self-check.json`: 선택해시·검사범위·실제완료시각.
- `../extracts/SYS-COUNTERS/oem-p86.png`, `oem-p106.png`, `oem-p145.png`: 실제PDF 렌더.
- 자체 XML추출/해시검사와 pdftoppm만 실행했다. 원본프로그램 실행/수정·생성기·테스트·시뮬레이터는 실행하지 않았다.
