# MV05 — 산소 조절 경로 모터밸브 원본 조사 초안

> 원본 고정 기준 1차 조사 초안. 작업3번 첫 묶음의 독립 조사. 현재 CPU·실물·정상극성·보호설정·복구 확인을 대신하지 않는다.

## 1. 설비·자료 기준

- catalog MV05, 우선23 대응18과 중복되지 않는 별도 대상이다. 전체248 중복·제외 대조 후 자체 연구범위에 배정했다. 기존 로컬 phase2 133 통합·게시 제외 상태는 유지한다.
- 고정 원본: `esp6662266/gme-plc-manual`, 커밋 `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0, `all-in-one/`. 이후 사용자가 게시한 v1.14.0과 조사 기준을 분리한다.
- 공개 rollout SKILL, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY의 근거 추적·7영역·완료 상태 분리를 적용했다. 접근하지 않은 로컬 전용 스킬 사용을 주장하지 않는다.
- 기존 devices/control-specs/procedures/MV05.html은 보존했다. 고정 기준에서 MV05 전용 circuit-guides/signal-guides/construction-guides/alarm-guides 파일은 없다. 이를 회로·신호·알람 부재로 해석하지 않는다.
- P&ID의 M15/MV05 0.25 kW 440 V, LS15/16, ZT05와 OEM FG34/35가 문서상 연결된다. 물리 동일성·현재 설치 상태·명판은 미확정이다. RO01 산소 제어와 관련되지만 RO01 계측 전체, AB01/HE01 본체, 공유 인버터를 MV05 소유로 합치지 않는다.
- 실제 수행은 원본 정적 읽기·XML 선언/핀 대조·PDF 실제 렌더·해시 계산·이 초안 작성이다. 코드·버전·대장·배포·운영기록 및 시뮬레이터/실제 PLC/현장/보호값/SEJIN 변경은 하지 않았다.

## 2. I/O·HMI

### 2.1 물리·처리·요청의 분리

|층|원본 신호·주소|근거와 경계|
|---|---|---|
|공유 전원 응답|I1.4 mv02_05_06_power_ok|FG30 inverter RUN 17–19→E1.4. MV02/05/06 공유, 개별 M15 회전 증명이 아님|
|공유 인버터 알람|I1.5 mv02_05_06_inv_all|FG30 20–21→E1.5. 현재 접점 설정·정상극성 미확정|
|개별 접촉기 응답|I2.0 mv05_fbk_opening / I2.1 mv05_fbk_closing|FG34 KM1/KM2 13–14→FG118 MOD8 단자21/22. 실제 축·밸브 위치와 분리|
|끝 리미트|I7.1 MV05_open / I7.2 MV05_Close|LS15/16, FG35/123. NC 도면과 현재 극성은 별도|
|출력|Q1.3 Open MV05 / Q1.4 Close MV05|0617 RID69/68 SSD AO11/12 Output; FG137 A1.3/A1.4→FG34|
|처리 응답|Inputs.MV05 RUN_Opening / RUN_Closing|0573 RID67/68 AO16/17, DB13.X2.0/X2.1|
|처리 리미트|Inputs.MV05 open / Close|0619 RID179/180 AO57/58, DB13.X7.1/X7.2|
|수동 요청|Flag.M_MV05_OPEN / CLOSE|0619 RID62/60 AO76/75, DB2.X9.4/X9.3|
|자동 선택|Flag.MV05_Auto|0619 RID61 AO54, DB2.X6.6|
|PID 방향|PID UP MV05 / PID DOWN MV05|0617 RID65/70 또는0670 RID28/29 AO104/105, M13.0/M13.1|
|출력 수동 펄스|MV WORK PULSE|0617 RID13 AO80, M10.0. 고정 주기·실제 출력 주파수 미확정|
|구동 고장|Allarm.MV_05_FAULT|0573 RID31/0619 RID64 AO93, DB3.X11.5|

DB 번호는 0618 DepDBBlock Flag/TOD2,Allarm/TOD3,Inputs/TOD13을 대조했다. 같은 RID 숫자를 다른 블록의 동명/유사명과 혼합하지 않았다. AO는 비트 오프셋이며 Timer AO는 타이머 번호다.

물리 입력을 처리 DB로 복사하는 `0397-FlgNet.xml` LAD1070은 raw Word 묶음 Move를 사용한다. 예를 들어 0627 Tag_179 RID8 AO16=IW2 → Move27, 0629 RID9 AO16 및 Inputs DB13 선언의 Word2로 전달한다. I2.0/.1과 DB13.X2.0/.1은 별도 공간이다. raw 복사 외에 처리 값의 다른 쓰기 가능성·실제 호출 순서는 미확정이며 같아 보이는 비트 주소만으로 현재 값 일치를 보장하지 않는다.

### 2.2 HMI 8개 설정과 미결속 호출

`hmi_plc_tags.csv`의 Access Name PLC, dde.cfg 설정 참조:

|태그 MV_05\\|설정 주소|내부 ID|
|---|---|---|
|LimitSwitchOpen|DB11,X26.3|0040F|
|Flag_CLOSE|DB2,X9.3|0031F|
|Allarme1|DB11,X26.2|0031E|
|AutoMan|DB2,X6.6|00311|
|OutputOpen|DB11,X26.0|00310|
|OutputClose|DB11,X26.1|001A4|
|Flag_OPEN|DB2,X9.4|00045|
|LimitSwitchClose|DB11,X26.4|00044|

`0365-FlgNet.xml` LAD1188은 CRef22/RID639, CodeBlock23/RID130을 호출하고 아래 14개 데이터 ORef를 가진다. RefId는 존재하나 해당 선언 결속을 확보하지 못했다. CSV와 핀명만으로 값을 끼워 넣지 않는다.

입력 W47/O24 Ingresso_run_Opening, W48/O25 Ingresso_run_Closing, W49~53/O26~30 Allarme1~5, W56/O33 Limit_switch_Open, W57/O34 Limiti_Switch_Close. 출력 W62/O39 Risposta_Opening,W63/O40 Risposta_Closing,W64/O41 Limit_Switch_Open_HMI,W65/O42 Limit_Switch_Close_HMI,W68/O45 Comulativo_allarmi.

따라서 HMI의 OutputOpen/Close라는 이름이 직접 Q 출력인지 가공 응답인지, 버튼 이벤트가 쓰는 방식, 실제 LimitSwitch 표시극성은 미확정이다. DB2 요청,DB11 표시,Q출력,raw입력,처리입력을 따로 기록한다.

## 3. 제어 구조·호출·소유

### 3.1 main 호출과 NOT ON 내부 경계

main `0032-FlgNet.xml` LAD1621/NID8: Powerrail W354→Contact352.in, ORef345/RID52 ON→W350→operand; Contact352.out W353→CRef341.en(또한 CRef344.en). CodeBlock347/RID85는 0688 FCBlock Valve Control loop/TOD N14다. ON은0692 RID52 Memory AO0=M0.0.

반면 아래 `0346-FlgNet.xml` LAD1708/NID6은 **NOT ON** Contact652로 시작한다. 0617 SimpleAccess RID1/UID24,NID6도 Memory AO0=M0.0이다. main의 ON 정접점과 내부의 동일 주소 반전을 원문 그대로 보존한다. 이를 ON으로 교정하거나 현재 실제 운전 가능/불가능으로 확정하지 않는다. 다른 호출·온라인 값·스캔 중 쓰기·현재 프로그램이 필요하다.

### 3.2 수동 요청 Reset과 방향 출력

0346의 고유 핀/선언:

- 공통 Contact652 NOT ON: W23/ORef24, outW653.
- 요청 Reset 앞 Contact654도 NOT ON: W21/ORef22, outW655.
- 수동 OPEN Reset: NOT Inputs.MV05 open(Contact656/W608/O579) OR Flag.M_MV05_CLOSE(658/W609/O580) OR MV05_Auto(660/W610/O581)→OR531→W611→RCoil535 M_MV05_OPEN(W613/O582).
- 수동 CLOSE Reset: NOT Inputs.MV05 Close(662/W614/O583) OR M_MV05_OPEN(664/W615/O584) OR MV05_Auto(666/W616/O585)→OR538→W617→RCoil542 M_MV05_CLOSE(W619/O586).
- 방향 출력 공통은 NOT ON652 다음 NOT MV_05_FAULT668(W621/O587),outW669다.

열림 출력:

`[(Auto670 AND PID_UP672) OR (수동OPEN674 AND MV_WORK_PULSE676)] AND [NOT Oxigen_Fault678 OR UNDER_TESTING680] AND NOT Close_MV05(682) AND Inputs.MV05_open684 → Coil561 Open_MV05`.

OR552 W628→알람/테스트 OR556 W631→반대출력 NC W632/O594→리미트 W633/O595→W685→Coil561,출력 operandW635/O596. 산소 알람과 테스트 조건을 누락한 단순 PID 제어로 요약하지 않는다.

닫힘 출력:

`[(Auto686 AND PID_DOWN688) OR (수동CLOSE690 AND MV_WORK_PULSE692) OR (Oxigen_Fault694 AND NOT UNDER_TESTING696)] AND NOT Open_MV05(698) AND Inputs.MV05_Close700 → Coil576 Close_MV05`.

OR567 W645→반대출력 W646/O603→리미트 W647/O604→W701→Coil576,출력 W649/O605. 이 식은 PLC 정적 연결이며 현장 Fail Close의 안전 성능·정상극성·응답시간 인증이 아니다.

### 3.2a 수동 요청의 공통 동작 펄스

`0350-FlgNet.xml` LAD1712/NID10:ON Contact846→NOT Tag_154 Contact848→SdCoil813,시간W834/O825 S5T#200MS,대상W837/O827 Tag_155. ON→Tag_155 Contact850→SdCoil818,시간W838/O828 S5T#2S,대상W841/O830 Tag_154. ON→NOT Tag_155 Contact852→W853→Coil823 MV WORK PULSE(M10.0,W844/O832). 선언0617/0620과 결속했다. 이 출력은0346의 수동 요청 가지에서 읽으며 PID의 PULSE_TM/BREAK_TM과 다른 경로다. 실제 펄스 주기·스캔 효과·고장 응답시간은 원본 시간값만으로 보증하지 않는다.

### 3.3 산소 PID: CONT_S·개별 상수·미결속9개

`0475-FlgNet.xml` LAD5,cyc_int5 NID2: ON Contact188/W150/O131→W189→LRef109.en. 0671 Instruction RID113=CONT_S,Instance149/RID20=0665 PID_MV05 DB22다.

|핀|Wire/ORef|원본 값/변수|
|---|---|---|
|COM_RST|W155/OR98|NOT MV05_Auto190 OR (Oxigen_Fault192 AND NOT UNDER_TESTING194)|
|LMNR_HS|W197/Contact196|NOT Inputs.MV05 open|
|LMNR_LS|W199/Contact198|NOT Inputs.MV05 Close|
|CYCLE|W166/O137|T#100MS|
|SP_INT|W167/O138|Local Real_SPO2|
|PV_IN|W168/O139|Local Real_O2|
|GAIN|W171/O140|Real2.0|
|TI|W172/O141|T#1M|
|DEADB_W|W173/O142|Real1.0|
|PULSE_TM|W178/O143|T#200MS|
|BREAK_TM|W179/O144|T#3S|
|MTR_TM|W180/O145|T#5S|
|DISV|W181/O146|Real1.0|
|QLMNUP|W182/O147|PID UP MV05 M13.0|
|QLMNDN|W183/O148|PID DOWN MV05 M13.1|

0667 상수 RID21~27의 Time/Real 선언과 SV를 확인했다. 현재 튜닝값·권장 설정이 아니다. Real_SPO2/Real_O2는0669 로컬 TEMP Real이다. live_index의 _7ex:4 평탄화 STL 검색 문자는 Data.RO01_SETPOINT→ITD→DTR→Real_SPO2, Data.Oxigen_RO01→ITD→DTR→Real_O2를 나타낸다. 0668 NID15 RID2/UID27 AO160(DB1.DBW20) 및 RID4/UID39 AO1040(DB1.DBW130),0669 RID3/UID34와RID5/UID46 쓰기 선언과 대응한다. 그러나 원형 STL 본문·컴파일 listing·현재 실행 순서는 미확보이다. 검색 문자를 원형 실행 코드로 승격하거나 현재 단위·주기를 확정하지 않는다.

원본 ORef에 RefId 자체가 없는9개: LMNS_ON O158/W159,LMNUP O160/W161,LMNDN O162/W163,PVPER_ON O164/W165,PV_PER O169/W170,PV_FAC O174/W175,PV_OFF O176/W177,PV O184/W185,ER O186/W187. 미결속은 FALSE/0/기본값/물리 단선이라는 뜻이 아니다.

### 3.4 엔코더 취득: MV05 고유 CH03

`0509-FlgNet.xml` LAD1759/NID48: NOT Simulation(1) Contact21(W51/O25)→EM_OK22(W53/O26)→W54→LRef23.en. Simulation(1)은0678RID344 M180.0,EM_OK는RID173 I19.4. 중지된 시뮬레이터를 실행·변경하지 않고 원본 호출 경계만 읽었다.

LRef23/RID330=0679 High_Speed_Counter,Instance24/RID347=0673 MV05_Encoder DB18. SwGate W55/O27=fill_unit1.CONTROL_SIGNALS.SW_GATE3(DB91.X23.3),CountValue W75/O47=fill_unit1.ACT_CNTV3(DB91.DBD172) Write. 0674 fill_unit1 TOD91,0676 RID345/346의 AO187/1376과 대조했다.

CaptureEnable 등 O28~46 및 O48/49,총21개 ORef에는 RefId가 없다. 실제 HSC 채널 구성·Capture/Sync/Reset·상태값·오버플로 대응은 미확정이다. 도면 MOD17 CH1과 프로그램 CH03 문자열을 이름만으로 같은 하드웨어 채널이라고 확정하지 않는다.

### 3.5 엔코더 누적·0쓰기·환산

`0515-FlgNet.xml` LAD1765/NID33:

1. EM_OK Contact1321→NOT raw MV05_Close1323(I7.2)→Coil1233 SW_GATE3와 Add1238.en.
2. Add1238: Memory encoder.Encoder_CH03(DB8.DBD12,DInt) + fill_unit1.ACT_CNTV3(DB91.DBD172)→Local CNT_Act_3. ENO W1301→Div1242 `/100`→Local CNTV3_100,ENO W1305→Move1246→Encoder_CH03_10(DB8.DBW42,Int).
3. 별도 EM_OK AND NOT SW_GATE3 Contact1325→Move1255 literal0→DB8.DBW42 및 Move1260 INT0→DB8.DBD12. rawClose와 처리Close의 사용처를 혼합하지 않는다.
4. EM_OK 분기 W1322→CRef1267.en Signal linearization. IN0W1315/O1289 ON;AnalogW1316/O1290 DB8.DBW42;CoeffW1317/O1291 DB4.DBW78;ZeroW1318/O1292 DB4.DBW76;OutW1319/O1293 Data.Pot_MV05 DB1.DBW140;OFRW24/O23 Allarm.Pot_MV05_OFR DB3.X25.1.

0674 Memory encoder TOD8,0676 RID201/349/155/156/157/438과 타입을 확인했다. 저장값의 현재 유효성·Retain·전원복귀 일치·실제 위치 %는 미확정이다. 공통 FC63 0291/0014는 범위내 `(입력+Zero)×Coeff/28000`의 정수 환산,범위밖−9999/OFR,NOT IN0시0쓰기 경로다. EN 호출 경계·다른 쓰기를 포함한 실제 실행 결과는 별도다.

## 4. 전기 전달 경로·실제 페이지

### 4.1 공유 인버터와 개별 모터 분리

Electrical_Rev2.pdf FG30/PDF31은 **Rev2 17.03.2025**,FG31/PDF32는 개정란 공란이다.

- 3상440V60Hz 6.2L1/2/3→30QM1→ACS355-03E-04A1-4 1.5kW U1/V1/W1. 출력U2/V2/W2→30U1/30V1/30W1 공통 간선으로 MV02/05/06에 분배한다.
- 30QM1 표기범위5.5–8A,도면 RATING6.9A는 현재 설정 확인값이나 조정 권고가 아니다.
- 단자9(+24V)→31KA1 **실부하5–9**→단자12DI1START. 단자9→17KA2 **실부하5–9**→15DI4RESET. 하단 접점표1/5/9를 부하 경로로 오독하지 않는다.
- FG31 A1.0→30QM1 보조→31.1→31KA1A1;A2→0V10.6. FG137 MOD14단자11=A1.0. 이 공통 출력은 MV05 전용 기동이 아니다.
- RUN17/19→E1.4,ALARM20/21→E1.5. STO14KA2/14KA6 경로와 PLC 일반 구동 명령을 같은 안전 기능으로 간주하지 않는다.

### 4.2 M15 정역 전력·코일·피드백

FG34/PDF35 개정란 공란, MOTORlZED VALVE MV-05:

`30U1/V1/W1 → 34QM1(1/3/5→2/4/6) → 34KM1/34KM2 정역접점 → 34U1/V1/W1 → XM → 34QS1(1/3/5→2/4/6) → M15 U/V/W`.

M15 0.25kW/0.76A,34QM1 범위0.7–1A를 원문으로 남긴다. 현장 명판·보호값·회전방향은 미확정이다.

- Open:FG137 MOD14단자14 A1.3→상대34KM2 NC31–32→34.1→34KM1A1.
- Close:MOD14단자15 A1.4→상대34KM1 NC31–32→34.2→34KM2A1.
- 두 A2공통34.3→34QM1 보조접점→34.4→XS21→34QS1 보조→XS22→0V10.6. 보조접점 번호가 렌더에서 명확하지 않은 부분은 임의 배정하지 않는다.
- 피드백:+24V10.7→34KM1 NO13–14→E2.0→FG118 MOD8단자21;KM2 NO13–14→E2.1→단자22. 접촉기 응답이며 모터 축/밸브 끝단 도달을 증명하지 않는다.
- FG118/PDF119는 Rev2 17.03.2025,FG137/PDF138은 공란이다. CPU515/MOD 표기는 도면 기준이며 현재 CPU를 확인한 것이 아니다.

### 4.3 리미트·엔코더 끝점

FG35/PDF36,FG123/PDF124,FG39/PDF40,FG146/PDF147,FG147/PDF148의 개정란은 각 렌더에서 공란이다.

- LS15:+24V→X1/72(2AF)→35.5→LS15 11–12→X1/73→E7.1→FG123 MOD9단자32.
- LS16:+24V→X1/74(2AF)→35.6→LS16 11–12→X1/75→E7.2→MOD9단자33.
- ZT05 B+24→X1/67→35.1;C0V→X1/68→35.2. 이 선은FG39를 경유하여FG146 MOD17단자9(24VDC)/10M에 연결되며 다른 ZT04 공급과 공유한다.
- ZT05 D→X1/69→35.3→FG147 MOD17 CH1.A단자11;E→X1/70→35.4→CH1.B단자12;ShieldX1/71→35SCH1→접지. CH1.N단자13에는 해당 신호가 그려지지 않았다.
- MOD17 별도 공급:+24V10.7→X21/3041(2AIST)→147.1→41L+,44M→0V10.6. 센서 공급/모듈 공급/신호 쌍을 구분한다.

### 4.4 시공도와 ZT05/ZT06 상충

Electrical_Can_Decoating_20241118.pdf 실제 PDF26/51/56,첫안24.11.11. 승인·준공 도면으로 단정하지 않는다.

|행|원문 경로·표기|미확정 경계|
|---|---|---|
|51/1_7|=FLO+MV05-M15A,CR→MV05M15,DAC PVC-S4core1.5SB,100LA/E100,LEN41|도면 길이·규격이며 실측 아님|
|56/6_6|=FLA+MV05-FLO1TB2B,CR→MV05FLO1TB2,설명 **ZT-06**,TM CVV-S4S1.0,LEN42|다른 행ZT05와 상충|
|56/6_12|=FLA+MV05-FLO1TB2A,MV03FLO1TB1→MV05FLO1TB2,LS15/16,DC7G1.0,LEN19|접속함 공유와 장치 소유 구분|
|56/6_18,19|FLO1TB2→LS15/16,DC CVV2C1.0,LEN각3|양단 개별 센서 식별 필요|
|56/6_20|=FLA+MV05-**ZT05A**,FLO1TB2→ZT05,TM CVV-S4S1.0,LEN4|PDF26 장치ZT05행의 케이블은 **ZT06A**|

PDF26 장치ZT05·케이블ZT06A,PDF56 incoming6_6설명ZT06·outgoing6_20ZT05A와 OEMZT05를 함께 보존한다. 이름을 하나로 정정하지 않는다. PDF56의6_7~10 검은 가림 행은 텍스트 추출 내용으로 복구하지 않는다.

## 5. 알람·타이머·복구

### 5.1 MV05 전용 응답 고장

`0159-FlgNet.xml` LAD1226/NID1은 제목이 mv-01 fault여도 공유 네트워크다. MV05 가지를 별도 추적했다.

`ON555 AND [(Open557 AND NOT Inputs.RUN_Opening561) OR (Close559 AND NOT Inputs.RUN_Closing58)] → OR60 → SdCoil313 S5T#150MS/Tag_96(T15)`.

시간 W475/O400=0571RID8,Timer W476/O401=0570RID30 AO15. 같은 조건 아래 Tag_96 Contact563(W477/O402)→W564→S318 Allarm.MV_05_FAULT(W479/O403). 리셋은 RESET_ALLARM Contact575 AND 자기고장585→W586→R358(W507/O422). 실제 극성·피드백 갱신·Set/Reset 순서는 미확정이다. 이 150ms를 MV03의150초나 MV06 다른 타이머로 바꾸지 않는다.

### 5.2 방향 누적 고장: ±700은 시간 단위가 아님

`0351` LAD1713/NID11:ON1671 AND Open1673→Add1384 WorkData.W31+1/Move1390 W32=0. ON1671 AND Close1675→Sub1399 W32−1/Move1405 W31=0. 0619 RID134/136 AO496/512 및0618 WorkData TOD6에 따라 DB6.DBW62/W64이다.

`0352` LAD1714/NID12:ON1953→Gt1720 `W31>700`→S1726 MV_05_FAULT와Move1729 W31=0. Lt1734 `W32<−700`→S1740 같은고장과Move1743 W32=0. 0620 RID157/159의700/−700을 확인한다. 출력 누적 계수이며 호출 빈도/정지 조건을 확인하지 않고 초·각도·회전수로 바꾸지 않는다.

### 5.3 공유 인버터 고장과 상충

`0455` LAD1821/NID48은 ON1816→StartAuxINV1837→**NOT 같은 StartAuxINV22**를 직렬 연결한다. 두 ORef1838/44는0658 RID236,OutputAO8=Q1.0이다. 이 모순처럼 보이는 원본을 수정하지 않는다.

그 뒤 NOT Inputs.Aux inverter RUN1818→TON24(PT2S)→S1792 Aux_Inverter_Fault,별도 Inputs.Aux_Inv_All1827→S1828 Aux_INV가 있다. Reset은 RESET_ALLARM1820 AND 해당 고장,Aux_Inverter_Fault 쪽은 Run1824도 요구한다. MV05 고유150ms/±700과 공통 인버터 고장을 합치지 않는다. 실제 보호 기능이 동작한다고 보증하지 않는다.

공유 출력의 별도 쓰기도 확인했다. `0363-FlgNet.xml` LAD1186/NID9에서 CRef23.Comulativo_allarmi→W46/O47(RID120), 같은 RID120의 O39→W38→NOT Contact63.operand, Contact63.out→W40→Coil64.in, W41/O44(RID776)→Coil64.operand다. `0063-IdentXmlPart.xml` RID776 Start Aux INV는 NID9/UID44/AK=Write, Output AO8=Q1.0으로 직접 선언된다. 반면 RID120의 직접 선언은 이번 결속에서 확보되지 않았다. 색인의 Motors.aux_inv.allarme_comulativo 명칭은 후보 해석으로만 남긴다. Q1.0의 쓰기 위치는 확인했지만 그 입력 고장 신호의 실주소·현행 실행·다른 쓰기 우선순위는 미확정이며, 공유 출력을 MV05 전용 운전 명령으로 배정하지 않는다.

### 5.4 산소 고장의 방향 영향과 자동 해제

`0530` LAD1982/NID4:ON539 아래 Data.Oxigen_RO01(DB1.DBW130)≤0(Le484) OR ≥200(Ge487)→OR483→**ServiceBit22**→S490 Allarm.Oxigen_Fault(DB3.X9.6). ServiceBit는0686 RID161 MemoryAO8000=M1000.0이다.

Reset은ON AND자기고장541→RO01≥5(Ge494)→RO01≤195(Le497)→R501고장 및S503STOP_HORN. 이 경로에는 RESET_ALLARM 접점이 없다. 0/200/5/195를 현재 산소%·안전한계로 임의 환산하지 않는다. ServiceBit의 현재 값과 RO01 환산 호출의 사용 여부·다른 쓰기는 미확정이다.

이 고장은0346에서 열림 억제/닫힘요청 및0475 COM_RST에 영향을 주지만 UNDER_TESTING 분기와 NOTON 호출 경계가 있다. 고장 해제·방향 출력·실제 밸브 이동·공정 정상·현장 복구를 구분한다.

## 6. 증상별 확인·수리 문서 경계

|증상|문서상 구분할 경로|필요한 추가 근거|
|---|---|---|
|자동에서 움직이지 않음|main ON 호출/내부 NOTON,Auto/PID/고장/리미트/반대출력|현재 승인 프로젝트·호출·관찰값, 임의 논리 수정 금지|
|출력은 있는데 응답 없음|Q→NC상대접점→KM코일→QM/QS공통귀환→KM13–14→I→DB|실제 결선/접촉기/모터 기계부 상태, 현재 극성|
|끝위치에서 반대 표시|LS15/16회로/처리DB/HMI미결속14개|현장 끝단사진·HMI이벤트·표시극성|
|150ms고장·누적고장|T15 응답감시 대 DB6 W31/W32±700|최초원인·스캔·피드백 지연·실제 기구 상태|
|위치값 이상|HSCDB18/CH03,rawClose 게이트,누적/0쓰기/FC63|채널구성·현재Count/보존값·실제위치,강제0쓰기금지|
|산소 고장 후 닫힘|ServiceBit·RO01범위·UNDER_TESTING·방향식|실제산소계/스케일/안전조건,현장안전평가|
|공유 인버터 이상|MV02/05/06공유응답/개별QM·KM·M15|다른모터영향과M15자체고장구분|

관찰은 사용자 승인된 현장 절차의 영역이다. 이 문서는 가동·시험·보호값 조정·강제출력·인터록 우회·시뮬레이터 시험을 제안하거나 수행하지 않는다.

## 7. 완료 기준·통합 인계

7영역은 본문의1~7에 대응한다. 설비·자료/I/O·HMI/제어/전기/알람/증상/완료를 모두 작성하되 미결속·소유·현재실물 경계를 유지한다.

- documentation: 초안 작성 및 핵심 원본 재검토. 사용자 독립검토·통합은 별도.
- static_review: 원본 XML/PDF 정적 대조 수행,실행검증 아님.
- ui_records/publication: 미수행,사용자/Codex 전담. 신규 작업3 자료의 로컬 통합·게시 제외 유지.
- tia_compile/live_cpu/field_recovery: 미수행.
- 원본 대조 기능에는 본문 핀·선언·실제 PDF페이지를 연결한다. 기록 백업/복원·변경 비교·보고서/PDF는 후속 구현영역이며 이번 조사에서 완료로 세지 않는다.
- 현재 보호값·모터/엔코더 실물·정상극성·HMI 실제쓰기·원형 STL 공급본문·HSC21개/CONT_S9개/HMI14개 미결속이 남는다.
- 다른 MV의 출력·타이머·누적한계·계수·항목 수를 복제하지 않았다. ±700,150ms,DB18/CH03,CONT_S 상수는 MV05 원본에서 확인한 값이다.

## 부록 A 핵심 주장 근거표

Flg/Ident는 all-in-one/sources/decoded-original/ 원본이다. ID와 페이지는 문서 위치이며 실제 프로그램 실행을 뜻하지 않는다.

|ID|주장|원본|핀·선언·페이지|경계|
|---|---|---|---|---|
|E01|설비/소유|INVENTORY;equipment.json;PID PDF1;FG34/35|M15/LS15/16/ZT05|공유인버터와RO01본체별도|
|E02|요청/출력/처리|0617/0618/0619 Ident;0397/0627/0628/0629|Q1.3/1.4,DB2X9.3/.4,DB13X2.0/.1,X7.1/.2|현재값/다른쓰기미확정|
|E03|HMI미결속|0365Flg;hmi_plc_tags.csv|14 ORef/8CSV태그|CSV만으로호출핀배정금지|
|E04|호출상충|0032/0346Flg;0688/0692/0694/0617|main352ON→CRef341 vs 내부652NOTON,같은M0.0|원문수정/현재활성추정금지|
|E05|수동요청Reset|0346Flg;0619|R535/R542;NOTON654;OR531/538|처리리미트정상극성미확정|
|E06|방향식/산소영향|0346Flg;0617/0619|Coil561/576;OR552/556/567;UNDERTESTING|실제FailClose안전성아님|
|E07|CONT_S개별상수|0475Flg;0665/0666/0667/0668/0669/0670/0671|LRef109/Instance149DB22,9개RefId없음|실제튜닝/평탄화STL공급근거/원형실행본문미확정|
|E08|HSC취득|0509Flg;0673/0674/0676/0678/0679|DB18/CH03,NOTSimulation21/EM_OK22,CountW75|21RefId없음,실하드웨어채널미확정|
|E09|누적/0쓰기/환산|0515Flg;0674/0676/0677/0678|Add1238/Div1242/Move1246/1255/1260/FC1267|DB8/91/Data/Coeff구분,Retain미확정|
|E10|공통환산|0291/0014Flg;0611/0612/0672|28000/−9999/NOTIN0|단위/현재계수미확정|
|E11|전용응답고장|0159Flg;0570/0571/0573|SD313150MS/T15,S318/R358|MV03/MV06타이머복제안함|
|E12|방향누적고장|0351/0352Flg;0617/0618/0619/0620|W31/W32±700,S1726/1740|호출횟수vs시간구분|
|E13|공유인버터고장|0455Flg;0655/0657/0658|StartAuxINV ANDNOT동일RID236,TON24/PT2S|공유소유/실제실행미확정|
|E14|산소알람|0530Flg;0682/0683/0684/0686|ServiceBitM1000.0,<=0OR>=200,reset5~195|산소%임의환산금지|
|E15|동력/코일|Electrical_Rev2.pdf|FG30/31/34/137,31KA1/17KA25–9,KMNC31–32|현재보호설정/실물미확정|
|E16|피드백/리미트|Electrical_Rev2.pdf|FG34/35/118/123,13–14,LS11–12|현재극성/회전/끝도달구분|
|E17|엔코더끝점|Electrical_Rev2.pdf|FG35/39/146/147,X1/67~71,CH1.A11/B12|전원공유와채널명의동일성구분|
|E18|시공상충|Electrical_Can_Decoating_20241118.pdf|PDF26/51/56,ZT05/06,1_7/6_6/6_12/6_18~20|가림행복원금지;길이실측아님|

## 부록 B 원본 SHA-256 71개

고정 커밋 abcf31c5030bc7ef8749ed8e869a857f2387a28a. 전체경로를 저장소 기준으로 표시했다. 해시가 맞아도 현재 CPU·설치·보호값이 맞다는 뜻이 아니다. 백업 원형 ZAP/PLF는 보존 기준이며 실행하지 않았다.

|원본 경로|SHA-256|
|---|---|
|.agents/skills/gme-equipment-rollout/SKILL.md|`fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b`|
|docs/equipment-standard/WORK-STANDARD.md|`05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99`|
|docs/equipment-standard/WORK-ITEM-TEMPLATE.md|`4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586`|
|docs/equipment-standard/INVENTORY.json|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|
|VERSION.json|`5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7`|
|all-in-one/sources/Electrical_Rev2.pdf|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|
|all-in-one/sources/Electrical_Can_Decoating_20241118.pdf|`3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd`|
|all-in-one/sources/PID_1684n002I.pdf|`2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b`|
|all-in-one/sources/GME_20250506.zap18|`00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8`|
|all-in-one/sources/PEData.plf|`647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a`|
|all-in-one/sources/source-manifest.json|`5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf`|
|all-in-one/sources/live_index.json|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|
|all-in-one/sources/hmi_plc_tags.csv|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|
|all-in-one/sources/hmi-windows.csv|`15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e`|
|all-in-one/registers/equipment.json|`7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa`|
|all-in-one/sources/decoded-original/network-map.json|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|
|all-in-one/sources/decoded-original/0014-FlgNet.xml|`2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30`|
|all-in-one/sources/decoded-original/0032-FlgNet.xml|`070bb8efa33d03b18add5da81d3f670a47c12b288076b7bfee11ac87fe6fa7e4`|
|all-in-one/sources/decoded-original/0149-FlgNet.xml|`bc2519cdad49a7268006b194e8e5e1160744ff221f04b83e710f31f57bc617f9`|
|all-in-one/sources/decoded-original/0159-FlgNet.xml|`5598abbad86ed26fa8dd17fc3eca3e1c0b7941a2798db6ae1e2472a7ca448d2a`|
|all-in-one/sources/decoded-original/0291-FlgNet.xml|`fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550`|
|all-in-one/sources/decoded-original/0346-FlgNet.xml|`7c782d799751476d88794a5d3d993e91878e03a39147d3b13233193dd3f6ce09`|
|all-in-one/sources/decoded-original/0351-FlgNet.xml|`1448cd179747074ae5ac3647c52e47950d18e0d90fa2f1cb155dbb24af50a7f6`|
|all-in-one/sources/decoded-original/0352-FlgNet.xml|`03e2d68dda289fcb7e7738c2f52e675890b252f5b526cab1ec2049323ab30d75`|
|all-in-one/sources/decoded-original/0365-FlgNet.xml|`99285443609a94429b3310720f3ebdcea63f3273ab0fc8ac9d4ae2bd1dd0377a`|
|all-in-one/sources/decoded-original/0397-FlgNet.xml|`bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834`|
|all-in-one/sources/decoded-original/0455-FlgNet.xml|`4d49d7acd2ef56ecb47252305453bae589897ab69315fc0cef32e1e156da1325`|
|all-in-one/sources/decoded-original/0475-FlgNet.xml|`ca3a5bf5bce9189b7c63dd27057b6b759e74a7793d34d2d050fe7e69951ae2b3`|
|all-in-one/sources/decoded-original/0509-FlgNet.xml|`e1e870a86edd1878f8ba3963e984e67718be1b39255a3e3d5fc17dd61b90a5a8`|
|all-in-one/sources/decoded-original/0515-FlgNet.xml|`504f68cf91ee6b33d6b29ab8549a013fed0d11b46212ad58f0aa377f33816ccf`|
|all-in-one/sources/decoded-original/0530-FlgNet.xml|`9f20c55030b3127abfedce38de08e50d494885cdf61d75c85a2715b0d380eac5`|
|all-in-one/sources/decoded-original/0570-IdentXmlPart.xml|`9fed133006458c3b43b1d5f2c15107a5a86b4fb7cdbaf3743bf88f0e5a105495`|
|all-in-one/sources/decoded-original/0571-IdentXmlPart.xml|`4a9deeb65a22e497e284fe6d98929e1d201ef5939e4aeca5805b4eb7e007d398`|
|all-in-one/sources/decoded-original/0573-IdentXmlPart.xml|`a22cc24a974e0c792f32e356a14b277a847e2bb204c91bce01c37d1714ddb56c`|
|all-in-one/sources/decoded-original/0611-IdentXmlPart.xml|`0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089`|
|all-in-one/sources/decoded-original/0612-IdentXmlPart.xml|`95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38`|
|all-in-one/sources/decoded-original/0617-IdentXmlPart.xml|`10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9`|
|all-in-one/sources/decoded-original/0618-IdentXmlPart.xml|`0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c`|
|all-in-one/sources/decoded-original/0619-IdentXmlPart.xml|`85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456`|
|all-in-one/sources/decoded-original/0620-IdentXmlPart.xml|`da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3`|
|all-in-one/sources/decoded-original/0627-IdentXmlPart.xml|`08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb`|
|all-in-one/sources/decoded-original/0628-IdentXmlPart.xml|`9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd`|
|all-in-one/sources/decoded-original/0629-IdentXmlPart.xml|`67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972`|
|all-in-one/sources/decoded-original/0655-IdentXmlPart.xml|`38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb`|
|all-in-one/sources/decoded-original/0657-IdentXmlPart.xml|`0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b`|
|all-in-one/sources/decoded-original/0658-IdentXmlPart.xml|`998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831`|
|all-in-one/sources/decoded-original/0665-IdentXmlPart.xml|`50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd`|
|all-in-one/sources/decoded-original/0666-IdentXmlPart.xml|`19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6`|
|all-in-one/sources/decoded-original/0667-IdentXmlPart.xml|`ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3`|
|all-in-one/sources/decoded-original/0668-IdentXmlPart.xml|`2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed`|
|all-in-one/sources/decoded-original/0669-IdentXmlPart.xml|`754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2`|
|all-in-one/sources/decoded-original/0670-IdentXmlPart.xml|`e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841`|
|all-in-one/sources/decoded-original/0671-IdentXmlPart.xml|`26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293`|
|all-in-one/sources/decoded-original/0672-IdentXmlPart.xml|`6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222`|
|all-in-one/sources/decoded-original/0673-IdentXmlPart.xml|`450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58`|
|all-in-one/sources/decoded-original/0674-IdentXmlPart.xml|`4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84`|
|all-in-one/sources/decoded-original/0676-IdentXmlPart.xml|`c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59`|
|all-in-one/sources/decoded-original/0677-IdentXmlPart.xml|`69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3`|
|all-in-one/sources/decoded-original/0678-IdentXmlPart.xml|`51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382`|
|all-in-one/sources/decoded-original/0679-IdentXmlPart.xml|`d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56`|
|all-in-one/sources/decoded-original/0682-IdentXmlPart.xml|`25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092`|
|all-in-one/sources/decoded-original/0683-IdentXmlPart.xml|`0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22`|
|all-in-one/sources/decoded-original/0684-IdentXmlPart.xml|`6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208`|
|all-in-one/sources/decoded-original/0686-IdentXmlPart.xml|`b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4`|
|all-in-one/sources/decoded-original/0688-IdentXmlPart.xml|`ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda`|
|all-in-one/sources/decoded-original/0692-IdentXmlPart.xml|`bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037`|
|all-in-one/sources/decoded-original/0694-IdentXmlPart.xml|`757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d`|
|all-in-one/devices/MV05.html|`1edd7f92176d74ba6fc80f63345f62f88670037d8dd371a0881b4cc68fe7f919`|
|all-in-one/control-specs/MV05.html|`a7dba5c0e3a90c669df5306502fc4b309e7ca7e2e1fa4fc242a37a139a042375`|
|all-in-one/procedures/MV05.html|`ada79f4276ceedb31257c40f90e70f9cabc443984f4871915ebfcda3489a91f1`|
|all-in-one/sources/decoded-original/0350-FlgNet.xml|`3f426a4ba9455160b8113df968b1052752a7b72cdfca8e57bdfd466340d691ff`|
|all-in-one/sources/decoded-original/0363-FlgNet.xml|`90fc22646d834bfd3139806680e708b449798516cf0d7c0c65eaf86a2ab80d5a`|
|all-in-one/sources/decoded-original/0063-IdentXmlPart.xml|`9dceae18963ead11293cfc3a70c2eac077faa53ebd28e23bb4e84bc3278c5034`|
