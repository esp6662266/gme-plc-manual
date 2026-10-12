# LD01A 석회 사일로 진동기 — 고정 원본 조사 초안

## 핵심 확인·상충·누락·공유 근거

- 고유 채널은 Start Vibrator LD-01 %Q3.7, LD-01A_Fbk %I4.7, 처리응답 DB13.DBX4.7, 요청 DB2.DBX2.1, 유지고장 DB3.DBX2.1이다. FG56의 M33·56KM1과 결속한다. I4.7은 56KM1 보조접점13–14의 응답이며 진동량·축회전 검출의 증거가 아니다.
- 출력에는 요청과 별개인 간헐 Start 가지가 있다. 요청 Reset/요청0을 출력의 무조건 OFF로 설명하지 않는다. T40/T41 가변 간헐시간과 T80의 S5T#2S 고장지연을 구분한다.
- 현장 허가는 PLC의 Local Button(DB13X22.7)이지만 도면은 170SA1/PB14 local selector다. 이름만으로 순간 누름버튼·정상위치·현재 극성을 확정하지 않는다.
- FG56 M33의 0.18kW·0.55A와 56QM1 2.2–3.2A 범위가 다르며 BOM도 같은 범위를 적는다. 오류/현행 적합성/실제 보호설정은 미확정이다. 설정변경을 제안하거나 수행하지 않는다.
- 시공 케이블 10_16의 접미 LD01A는 DUS2TB1→LD01 계장전원 가지다. 진동기 M33 모터케이블1_25와 동일하게 합치지 않는다.
- LD01·LT01 초안은 공통 소유/호출/색인 재사용에만 활용했다. 아래 LD01A 선언·Part/Wire/ORef·타이머·원본 PDF 끝점은 직접 재확인했다. 부모 전체조사·저레벨 전체경로를 반복하지 않았고 부모 완료를 하위 완료로 상속하지 않는다.

## 1. 설비·자료 기준

| 항목 | 확인 및 경계 |
|---|---|
| 대상 | catalog_id LD01A, 석회 사일로 진동기, motor/집진·석회, parent LD01, depth1, phase2 |
| 대장 | INVENTORY catalog[120], equipment[51]; 별칭 ld_01_vib / ld01v / vibrator ld-01 / ld-01a; 전기FG56 |
| 범위 | BATCH18 LD01A 한 개 자체 문서조사. LD01(M32), LT01, VR06(M40)과 별도 소유 |
| 고정 원본 | gme-research/source-mv06, abcf31c5030bc7ef8749ed8e869a857f2387a28a, v1.12.0 |
| 표준 | GME-STD-1.0.0, AGENTS, rollout SKILL, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY 및 최신 인계자료 읽기 |
| 상태 | 문서 초안/선택 근거 자가 정적검토. 실제 모델·추론 런타임 증명 미확인, 독립 승인 대기 |
| 보존 | 원본 읽기 전용. 자신의 draft/extracts/LD01A만 작성. 원본·공통코드·버전·대장·배포·운영·PLC·현장·보호값·SEJIN 변경0 |

이하 sources/registers는 고정 원본 all-in-one 아래다. 0261은 sources/decoded-original/0261-FlgNet.xml, 선언번호는 같은 폴더의 IdentXmlPart.xml이다. XML은 직렬 원문이므로 위치를 NID/UID/RID/핀으로 식별하며 추출 pretty 줄번호를 원본 행번호로 쓰지 않는다.

P&ID PID_1684n002I.pdf 실제p1 도번1684n002 판I에서 LD-01 측면 M33, 하부 M32, LT-01, VR-06/M40을 구별한다. M33은0.18kW/440V 표기다. 상세 개정일은 이번 전체 렌더에서 확대 재확정하지 않았으므로 부모 날짜를 독립확인으로 옮기지 않는다. 현재 실물 동일성은 별도다.

| 7영역 | 적용 상태 | 확보 / 미확정 |
|---|---|---|
| 설비·자료 | 적용 | LD01A/M33/부모 분리 / 현재 실물·명판 |
| IO/HMI | 적용, 일부 미확보 | 고유 Q/I/DB/CSV / HMI 데이터4 ORef·이벤트 |
| 제어 | 적용 | Reset·출력 OR·가변 S5타이머·Word쓰기 / 현재값·전체 최종 Writer |
| 전기끝점 | 적용 | FG56/120/139/170/177/253 및 시공 / 승인준공·극성·보호 |
| 알람/복구 | 적용 | T80 2초·S/R / 실제 원인제거·복구 |
| 증상관찰 | 적용 | 같은시각 비교 지점 / 실측·정비 없음 |
| 완료/누락 | 적용 | 문서·정적범위 / UI·기록·게시·TIA·CPU·현장 별도 |

## 2. I/O·HMI·선언 결속

| 신호 | 형식/주소 | 원본 선언·고유 문맥 | 해석 |
|---|---|---|---|
| Start Vibrator LD-01 | Global Bool %Q3.7 | 0602 RID155 Output AO31, NID31 UID909 Write; 0658 RID114 NID28 UID966 Read | 명령이며 실물진동 아님 |
| LD-01A_Fbk | Global Bool %I4.7 | 0613 RID230 Input AO39, NID38 UID2098 | 접촉기 응답 원시값 |
| FEEDBACKMOTOR-LD-01A | Global Bool DB13X4.7 | 0657 RID295 AO39 BAD247→0655 Inputs/TOD13, NID28 UID1003 | 고장감시에 읽는 처리값 |
| M_LD_01_VIB | Global Bool DB2X2.1 | 0604 RID153 AO17 BAD2→0603 Flag/TOD2, NID31 UID904 Write/905 Read | 요청; 출력과 별도 |
| LD_01_VIB_FAULT | Global Bool DB3X2.1 | 0604 RID152 BAD5→0603 Allarm/TOD3; 0657 RID117 AO17 BAD10→0655 Allarm/TOD3, NID28 UID971 S/973 Read/974 R | 유지고장 |
| Start_LD01Vib | Local Bool interface | 0605 RID151, SSD S=D/AO0, NID30 UID881 Write, NID31 UID907 Read | 전역 M/DB 주소 발명 금지 |
| Tag_124/Tag_125 | Global Timer %T40/%T41 | 0602 RID147/AO40 및 RID149/AO41, NID30 | 간헐 타이머 |
| LD01_W/LD01_P | Global Int DB1W308/W310 | 0604 RID235/AO2464, RID236/AO2480, BAD20→0603 Data/TOD1, NID44 UID38/46 | 변환 입력; 현재값 미확인 |
| LD_01V_WorkTime/PauseTime | Global Word DB1W150/W152 | 0604 RID148/AO1200, RID150/AO1216, NID44 UID43/48 Write 및 NID30 UID874/877 Read | S5타이머 value에 전달하는 Word |
| Tag_71 | Global Timer %T80 | 0658 RID115 AO80, NID28 UID968/969 | 진동기 고장 타이머 |
| 170SA1 / Local Button | Global Bool I28.7 / DB13X22.7 | 0627 RID145 Input AO231 UID115; 0629 RID151 AO183 BAD4→0628 DB13 UID141 Write; 0604 RID268 NID31 UID32 Read | 현장셀렉터 원시/처리 분리 |
| 부모 피더 처리Run | Global Bool DB13X4.6 | 0604 RID229 AO38 BAD218→0603 DB13, NID30 UID24 | LD01 소유 조건, Q3.6이 아님 |
| VR-06 RUN | Global Bool DB13X5.7 | 0604 RID227 AO47 BAD218, NID31 UID23 | VR06 소유 Reset 조건 |
| ON / UNDER TESTING | Global Bool M0.0/M5.5 | 0602 RID1 Memory AO0 / RID4 AO45, NID31 UID901/903 | 항상TRUE·현장허가로 단정 금지 |
| RESET_ALLARM | Global Bool DB2X6.0 | 0657 RID13 AO48 BAD12→0655 Flag/TOD2, NID28 UID972 | 고장Reset 요청, 재기동 아님 |

### 입력·출력 Word 전달

0397 LAD1070/index1/NID1: ORef36/RID10(0627 Tag180 Word/Input AO32=%IW4)→W39 Move35.in; Move35.out1→W40 ORef37/RID11(0629 AO32 BAD4→0628 DB13)=DB13W4. I4.7과 부모 I4.6/VR06 I5.7이 같은 Word에 포함된다. 앞단 Move27.eno→Move35.en W41 및 DisableENO 속성을 유지하며 무조건 매스캔 복사로 단정하지 않는다.

같은0397: rail W21→Contact114, ORef115/RID145→operand W99; Contact114.out→Coil140.in W144, ORef141/RID151→operand W143. 부호반전 없이 I28.7→DB13X22.7로 개별 복사한다. 이 bit는 IW4 묶음과 다르다.

0401 LAD356/index1/NID1: ORef35/RID28(0632 Word Output AO16=%QW2)→Move23.in W59, out1→ORef36/RID50 W61(0633 Word AO16 BAD26→0064 Output/TOD14)=DB14W2. Q3.7을 포함한 출력의 표시 미러 방향이다. DB14에서 Q로 쓰는 경로가 아니다. W57 앞단 ENO 조건을 보존한다.

공통 호출은 LD01 초안 §2.2 및 §3.4를 색인 재사용한다. 현재 CPU 호출·활성·주기·다른 Writer·외부 쓰기를 검증하지 않았다. 부모에서 확인된 정지기능의 처리입력 다른 Writer 존재는 유지하되 이번에는 그 기능을 확대조사·작성·생성·실행·행동시험하지 않았다.

### HMI 세 설정행과 4개 미결속 데이터 ORef

hmi_plc_tags.csv 실제125행 LD_01_VB\Allarme1=DB11,X50.1(ID0033C), 413행 RispostaA=DB11,X50.0(ID001BE),448행 Flag=DB2,X2.1(ID00196). Access Name PLC/dde.cfg 설정이며 온라인 값·실제 클릭 이벤트·쓰기권한의 증거가 아니다. DB11 표시, DB3 유지고장, DB13 처리응답, I4.7 원시응답을 합치지 않는다. LD01_W/P 직접 HMI 설정행은 이 CSV 검색에서 확보하지 못했다.

0378 LAD1202/hmi index25/title ld01 vb, network-map inferred_original_nid=null. CRef22/RID638, CodeBlock23/RID1의 HMI Standard Motors 호출 인터페이스(0624/0623)를 확인했다. W37 ORef24/RID666→Ingresso_run; W39 ORef26/RID323→Allarme1; W46 Risposta→ORef33/RID326; W48 Comulativo_allarmi→ORef35/RID328. 이 4개 비리터럴의 이름·DB11/DB3/DB13 최종 선언 문맥은 미결속으로 유지한다. 같은 RID만 다른 네트워크에 연결하지 않는다. Allarme2~5는 W40~43/ORef27~30/RID48이며 부모의 FALSE literal 색인을 참고하되 실행 결과·화면 메시지는 미확정이다.

## 3. 제어 구조·타이머·복수 Writer

### 3.1 시간 변환 0274 / LAD1959 / index30 / NID44

KF_KT FC109: 0058 RID241/TOD109,0059 RID248 인터페이스 KF=Int,SEC=Bool,KT=Word.

- rail W21→CRef36.en. ORef38/RID235→KF W37(DB1W308), ORef40/RID249→SEC W39(0606 Constant Bool V0). CRef36.KT→ORef43/RID148 W42(DB1W150).
- CRef36.eno→CRef44.en W41. ORef46/RID236→KF W50(DB1W310), ORef47/RID249→SEC W51(Bool0), KT→ORef48/RID150 W52(DB1W152).
- Bool0는 시간0초가 아니라 변환모드 인수다. 부모의 live_index KF_KT 설명 색인은 false=tenths를 설명하지만 이번에는 원문 STL 전체/현재 DB값/실행을 독립검증하지 않았다. 임의 초수·현장 안전상한을 만들지 않는다.

### 3.2 간헐 Start 0260 / LAD1960 / index31 / NID30

ON Contact896(ORef872/RID1, W882)→W26 Contact23(부모 LD01 처리Run ORef24/RID229, W22)→W899로3가지 분기:

| 가지 | 고유 Part/Wire/ORef | 정적 관계 |
|---|---|---|
| 작동시간 | NOT Contact900, operand875/RID147 W885→W901 SdCoil861; value874/RID148 W884, operand876/RID149 W887 | ON·부모처리Run·NOT T40가 T41/WorkTime 입력을 허가 |
| 휴지시간 | Contact902, operand878/RID149 W889→W903 SdCoil866; value877/RID150 W888, operand879/RID147 W891 | ON·부모처리Run·T41이 T40/PauseTime 입력 허가 |
| 지역Start | NOT Contact904, operand880/RID149 W892→W905 Coil871; operand881/RID151 W894 | Start_LD01Vib = ON AND 부모처리Run AND NOT T41 |

실제 첫주기·잔존 타이머·설정0/비정상값·현재 주기 결과는 시험하지 않았다. 고장감시 T80과 간헐 T40/T41을 공유 타이머로 설명하지 않는다.

### 3.3 출력과 요청 Reset 0261 / LAD1961 / index32 / NID31

- rail W939→ON Contact925(ORef901/RID1 W910), out W926 공통분기.
- 고장 Contact927(ORef902/RID152 W911)→OR888.in1 W928. NOT VR06Run Contact22(ORef23/RID227 W21)→W24 NOT UNDER TESTING Contact929(ORef903/RID4 W912)→OR888.in2 W930. OR888.out W913→RCoil891; 요청 ORef904/RID153 W915.
- 요청 Reset 식: ON AND [VIB_FAULT OR (NOT VR06Run AND NOT UNDER TESTING)].
- 출력 첫 가지는 요청 Contact931(ORef905/RID153 W916)→OR894.in1 W932.
- 출력 대체 가지는 NOT fault Contact933(ORef906/RID152 W917)→W934 Start Contact935(ORef907/RID151 W918)→OR894.in2 W936.
- OR894.out→W25 Local Button Contact31(ORef32/RID268 W30)→W26 Coil900; Q3.7 ORef909/RID155 W923.
- 출력 식: ON AND [M_LD_01_VIB OR (NOT VIB_FAULT AND Start_LD01Vib)] AND LocalButton.

VR06 조건은 요청 Reset 가지에 있다. 피더 도어·LT01 저레벨을 이 진동기 출력에 직접 직렬로 삽입하지 않는다. 요청 Reset과 지역Start 병렬가지 때문에 요청0만으로 Q3.7=0을 보장할 수 없다. 현재 스캔의 최종값·동시쓰기·안전등급은 미확정이다.

### 3.4 Startup Word쓰기

0147 LAD402/index2/NID2: 앞단 ON/ENO 연쇄 이후 Move141.in W188의 ORef170/RID54(0048 Int0), out1 W189→ORef171/RID9. 0563 Word AO16 BAD6→0562 Flag DB2이므로 DB2W2 전체0에 요청 DB2X2.1이 포함된다. 0148 LAD403/index3의 추정NID는null이지만 선언0563의 NID3 UID288/RID26(Word AO16 BAD23→0562 Allarm DB3)로 선택 결속한다. Move250.eno W306→Move253.en; ORef287/RID54 Int0 W307→Move253.in; out1 W308→ORef288가 DB3W2를0으로 쓰며 DB3X2.1 포함이다. 정상 고장Reset 버튼과 startup Word초기화는 다르다. 전체 최종 Writer를 전수 확정한 것이 아니다.

## 4. 전기 끝점·도면 실제 페이지·개정

아래10페이지를 원본 PDF에서 렌더해 시각검토했다. 전기표지 파일명 Rev2를 모든 시트의 실제 개정으로 복제하지 않는다.

| 원본 PDF 실제p | 시트·개정 확인 | 고유 확인 범위 |
|---|---|---|
| Electrical_Rev2 p57 | FG56,27.05.2024,별도 Rev 숫자 공란 | M33 동력·Q3.7 코일·I4.7 응답 |
| p121 | FG120,27.05.2024 및 Rev2/17.03.2025 | I4.7 MOD9 단자8 |
| p140 | FG139,27.05.2024,별도 Rev 공란 | Q3.7 MOD14 단자38 |
| p171 | FG170,27.05.2024,별도 Rev 공란 | 170SA1/PB14 접점·X3 |
| p178 | FG177,27.05.2024,별도 Rev 공란 | E28.7/X22 4010/MOD4 Rack3 단자8 |
| p256 | FG253,27.05.2024,별도 Rev 공란 | 56KM1·56QM1 BOM, FG≠p−1 사례 |
| Electrical_Can_Decoating_20241118 p36 | CANDC-CONS-E019-036,24.11.11 first draft design | M33와 DUS2TB1 별도 가지 |
| p51 | CANDC-CONS-C001-051,24.11.11 first draft design | 모터 케이블1_25 |
| p60 | CANDC-CONS-C010-060,24.11.11 first draft design | PB14 10_15와 계장전원10_16 분리 |
| PID_1684n002I p1 | 도번1684n002 판I | M33·M32·LT01·VR06 위치 분리,세부 개정일 재확정 안 함 |

### 동력·명령·응답

1. FG56: 440V/60Hz 3상 8.3L1/L2/L3(55/9에서)→56QM1 주접점1/3/5–2/4/6→56KM1 주접점1/3/5–2/4/6→선56U1/V1/W1(black FS17 1.5mmq)→XM56U1/V1/W1→56QS1 주접점1/3/5–2/4/6→M33 LD-01A U/V/W/PE. 0.18kW·0.55A는 도면표기이며 실측/명판확인 아님.
2. FG139 MOD14 CPU표기515 단자38 A3.7/Q3.7→교차56/4→FG56 XS49→56QS1 보조→XS50→선56.1→56QM1 보조→56KM1 A1, A2→−0Vdc10.6. 주접점·보조접점·코일을 구별한다. CPU515 도면표기는 현재 실제CPU 판정이 아니다.
3. +24Vdc10.7→56KM1 보조13–14→E4.7 교차120/7→FG120 E4.7(56/6)→CPU표기515 MOD9 단자8. 이 피드백에는 진동센서/회전계 끝점이 없다. 접촉기 투입응답을 실물진동으로 승격하지 않는다.
4. Local selector: FG170 +24Vdc152.5→X3 115(2A F 5×20)→선170.4→170SA1/PB14 접점13–14→X3 116→E28.7(177/7). FG177 E28.7(170/5)→X22 4010→MOD4 Rack3 단자8. 원시I28.7→처리LocalButton은 §2의 직접 전달이다. 현재 선택위치·정상극성은 미확정이다.

### BOM·시공 상충 및 별칭 위험

- FG253/실제p256: 56KM1 Siemens 3RT2015-1BB41(3kW/1L/DC24V/S00), RC 3RT2916-1CB00. 56QM1 그룹은 보조3RV2901-1E, 결합3RA1921-1DA00, Whoner WR32433, 본체3RV2011-1DA10(2.2–3.2A) 각각수량1. 보조부품 행을 보호기 본체로 오독하지 않는다. 0.55A와2.2–3.2A 상충 해결은 현행 명판·실물 보호기/설정·승인 검토서가 필요하다.
- 시공p36은212RAD1의2번 Pipe16→LD-01/M33. p51 1_25 =DUS+LD01-M33A는 CR→LD-01/M33 SILO VIBRATOR, GAC/CV/CORE4/SIZE1.5/SPARE0, 경로100→200→210→211→212RAD1→E200, Adjustment6/LEN118이다. 표의 LEN118을 실측값으로 취급하지 않는다.
- 시공p60 10_15 =DUS+LD01-PB14A는 DUS2TB1→PB14, DC/CVV/5G/1.0/SPARE2/E440,Adjustment3/LEN4. 10_16 =DUS+LD01-LD01A는 DUS2TB1→LD-01, AC/CVV/3G/1.0/E410,3/4. 후자 접미A를 LD01A catalog/M33로 오인하지 않는다.
- 시공도 CHECKED/APPROVED 공란이며 승인준공도 아니다. 주변68FC1/170FC1 태그차이·110Vac/220V 가지 결속은 부모LD01·LT01의 기존 보류를 유지한다. 이 주변 센서/전원을 진동기 자체 소유로 옮기지 않는다.

## 5. 알람·복구·시간기록

### 고유 고장 0440 / LAD1806 / allarms1 index26 / NID28

| 단계 | 원본 핀/선언 | 정적 식·제한 |
|---|---|---|
| 공통허가 | ON989(ORef965/RID1,W975)→W990 Start991(ORef966/RID114,W976) | ON·Q3.7 |
| 타이머입력 | Start991.out W992→NOT Run1002(ORef1003/RID295,W1005)→W21 SdCoil953 | ON·Q3.7·NOT DB13X4.7 |
| 설정 | ORef967/RID28 W977→value; ORef968/RID115 W978→operand | 0656 S5Time S5T#2S/V512, T80.512ms가 아님 |
| Set | Start991.out W992→Tag71 Contact993(ORef969/RID115,W979)→W22 SCoil959, fault ORef971/RID117 W982 | ON·Q3.7·T80; NOT Run을 Set에 추가직렬 삽입하지 않음 |
| Reset | ON989.out→RESET Contact997(ORef972/RID13,W984)→W998 fault Contact999(ORef973/RID117,W985)→W1000 RCoil964, ORef974/RID117 W987 | ON·RESET_ALLARM·VIB_FAULT; 원시응답조건 없음 |

원조건을 강제로 바꾸거나 Reset하면 복구된다고 안내하지 않는다. 동시 Set/Reset·최종쓰기·현재 실제지연은 미시험이다. HMI Allarme1 주소는 DB11X50.1이며 DB3X2.1과 별도 표시영역이다. LT01의 IEC TON10초·주모터T75 2초는 다른 소유다.

### 가동시간은 누계확정 아님

0615 RID232 Int AO1184/BAD5→0614 hours motors DB9=DB9W148(VIB_MIN), RID234 Int AO1200=DB9W150(VIB_HOUR). DB1W150 WorkTime과 DB번호가 다르다.

0323 LAD1036/index35/NID38: Tag47 Contact2126→W2127 원시I4.7 Contact2128(ORef2098/RID230,W2110)→W2129 Add2080.en/Ge2087.pre. MIN ORef2099/RID232+Int1 ORef2100/RID7(0616) W2111/2112→MIN2101 W2113. Ge2087은MIN2102와60 ORef2103/RID8(W2114/2115), out W2116→Move2090.en. Move2090.in W2118는Int1 ORef2104/RID7, out1 W2119→HOUR2105/RID234다. HOUR+1 Add로 바꾸어 설명하지 않는다. ENO W2120→Move2093 MIN0(W2121/2122), ENO W2123→SCoil2096 업데이트요청(M1.7,0613 RID13/ORef2108 W2124).

0339 LAD1052/index51/NID54의 공유ENO: Move3011.eno W3040→Move3014.en, Int0 ORef3028/RID12 W3041→in; out1 W3042→VIB_HOUR ORef3029/RID234. 앞단 공통Tag48 허가/외부저장 전체는 부모 §5.3 공통근거를 재사용한다. T13/T17·외부저장 이력을 이번에 다시 전체 분석하지 않았으며 영구 총운전시간·정비주기·실제 저장완료를 확정하지 않는다.

고장Reset, 요청Reset, 간헐상태, 현장셀렉터, 재요청, 실제 원인제거·재발없음은 각각 다른 확인이다. 고장bit0/화면소거를 현장복구로 표시하지 않는다.

## 6. 증상별 관찰·원인배제 계획

실제 관찰·조작·정비 기록을 만든 것이 아니다. 승인된 안전 절차에서 확보할 자료의 위치를 정리한다. 입력강제·활선작업·보호우회·설정변경은 이 초안의 지시가 아니다.

| 증상 | 같은 시각 비교 지점 | 원본에 따른 구분 |
|---|---|---|
| 요청이 사라짐 | DB2X2.1,DB3X2.1,VR06 DB13X5.7,M5.5, startup/HMI쓰기시각 | 0261 RCoil과 DB2W2 초기화, 재요청 분리 |
| 요청0인데 명령있음 | 지역Start,부모 DB13X4.6,T40/T41,DB13X22.7,Q3.7 | 출력 OR 대체가지 존재; 실물진동 별도 |
| 요청/Start 있으나 Q없음 | ON,LocalButton,I28.7,PB14위치·호출/최종Writer | 170SA1 명칭·현장극성 미확정 |
| Q있고 진동없음 | MOD14/38,XS49/50,56QS1/QM1/KM1 코일·주회로,M33 | 명령·전달·접촉기·모터·기계상태 별도; 보호상충 유지 |
| 2초 고장 | Q3.7,T80,I4.7,DB13X4.7,56KM1 13–14,MOD9/8 | 응답접점·Word전달·호출·유지고장 구별 |
| 간헐주기 이상 | DB1W308/W310/W150/W152,T40/T41,부모처리Run | KF_KT Bool0·ENO·타이머상태; 초수 임의수정 금지 |
| HMI/시간기록 불일치 | DB11X50.0/.1,DB2X2.1,원시/처리응답,DB9W148/W150,외부저장시각 | 표시4 ORef 미결속·HOUR Move1·공유0쓰기 |

기록에는 관찰자·시간대·시각·위치/단자·값/단위·수집방법·현재 프로젝트근거·비교 원본·배제결과·승인조치·재요청·재발없음·실물복구 근거가 필요하다. 사용자 운영사진/SEJIN 이력을 복제하지 않았다.

## 7. 완료·누락·인계

- 문서: LD01A 한 ID의 7영역 초안. 부모LD01·LT01·VR06 완료/소유로 확대하지 않음.
- 정적: 아래 명시한11개 LAD 선택범위,10개 실제PDF페이지,선정파일 해시를 구별한다. 전체 원본/모든 로직 의미검토가 아님. 자체검토이며 독립 승인 대기.
- 기능: 도면/래더 나란히 비교·백업/선택복원·기록전후비교·보고서/PDF의 근거는 준비했으나 제품 UI/기록 저장·재읽기·재열기·미지필드 보존·모바일·회귀·보고서 기능시험은 미수행이다. 후속 구현은 LD01A 별도 키와 기존 기록/다른설비를 보존해야 한다.
- 누락: 현재CPU/프로젝트 교차참조와 호출·간접/외부Writer; HMI4 데이터ORef 최종선언·실제이벤트/권한; 현재 KF_KT 설정/시간값; M33/56QM1 명판·승인 보호검토; PB14 위치·정상극성·단자준공도; 실제 진동/원인제거/복구 기록.
- 독립검토 첫조치: 출력OR/요청Reset 분리, T40/T41 핀, 고장T80,56KM1 13–14,보호범위 상충,10_16 이름충돌을 대조한다. 새 실물자료 없이 같은 보류를 반복조사하지 않는다.
- 원본 build/test/generator/preflight 스크립트를 실행하지 않았다. 자체 XML 파싱·문서 렌더·해시·정적 연결검사만 수행했다. 시뮬레이터 작성/수정/생성/실행/행동시험0, PLC/현장/보호값변경0, 커밋/업로드/사용자전송0.

| 상태 | 결과 |
|---|---|
| documentation | draft_ready |
| static_review | self_review_completed, 선택범위만; 독립승인 대기 |
| ui_records | not_run |
| publication | not_published; 로컬 실제 최신 통합/게시 검증 주장 없음 |
| tia_compile / live_cpu / field_recovery | not_performed |

## 부록 A. 직접 의미검토 범위와 실제시각

| XML | LAD / index / NID | 직접 검토 범위 |
|---|---|---|
|0274|1959 /30/44|두 KF_KT 핀·ENO·형식|
|0260|1960 /31/30|T40/T41 및 Local Start|
|0261|1961 /32/31|요청Reset·출력OR·LocalButton|
|0440|1806 /26/28|T80·2초·Set/Reset|
|0378|1202 /25/null|HMI 호출핀·4데이터 미결속|
|0397|1070 /1/1|IW4 Word전달·I28.7 bit전달|
|0401|356 /1/1|QW2→DB14W2 방향|
|0147|402 /2/2|DB2W2 초기화 선택가지|
|0148|403 /3/null|선언NID3의 DB3W2 초기화 선택가지|
|0323|1036 /35/38|원시I4.7·MIN+1·HOUR Move1|
|0339|1052 /51/54|VIB_HOUR Move0 선택가지|

공통 호출/전체저레벨/부모제어/외부LIW/모든설비 시간처리는 LD01·LT01 초안의 색인과 기존 제한을 재사용했으며 위11개 의미검토에 새로 합산하지 않았다. 해시대상파일수는 의미검토수와 다르다.

실제 실행환경 기록(UTC): 추출 시작 2026-10-11T13:06:06.768010+00:00; 고유XML·선언 및PDF 직접검토 후 정적검사/해시 완료 2026-10-11T13:11:31.120824+00:00. 추정 소요시간은 기재하지 않는다.

## 부록 B. 선정 원본 SHA-256 / 고정 Git blob 전체 목록

선정 59파일 모두 작업트리바이트=고정Git blob바이트 및 SHA-256 일치. 중지5자산 지정해시도 일치. 정적 선언/핀/보존 검사 26개 통과. 해시일치는 해당 파일 전체 의미검토나 동작시험이 아니다. 원본 Git 시작·종료 변경0.

| 고정 원본 상대경로 | SHA-256(전체) | Git blob(SHA-1 객체ID) | 바이트대조 |
|---|---|---|---|
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b | 9aa820ea6ca15b4e136c9772423b78ed4df6a3d4 | 일치 |
| AGENTS.md | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 | 073164bc6efd5791032d62c71b03b4dab48cb6f8 | 일치 |
| EXPANSION-WORK.md | ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2 | 4c42d88ecc2d48269eb23e13a20ebf3721a092a1 | 일치 |
| PUBLICATION_STATUS.md | efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740 | d76401cf291fc0be681acc51fa898ad3ce46ff78 | 일치 |
| VERSION.json | 5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7 | fffb51663b7705aec91cb119ca80ee943a4ce758 | 일치 |
| WORKSPACE-HANDOFF.md | 215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074 | dd0b8989d2376c4415bba9bd826fe6754c6b1a12 | 일치 |
| all-in-one/ACTIVE-WORK.md | eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2 | 6eb947c629b5ddf9c759ef87649451303938864b | 일치 |
| all-in-one/assets/program-model-data.js | 52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f | 38f34b0caa380a16ccad6f6f1e234a2fdf23f327 | 일치 |
| all-in-one/assets/simulator-workspace.js | 3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc | 97c2c831c77a9699fff0e0960b3bc1b7d93d45b3 | 일치 |
| all-in-one/assets/virtual-plc.js | 5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc | 0bd9eceb54365a91214a37c5601b5067c39a3f75 | 일치 |
| all-in-one/registers/equipment.json | 7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa | acc42633033398216469064932c4b76987371606 | 일치 |
| all-in-one/registers/program-model.json | 6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5 | 9860b10f008d3a5ae714be50d77b703dfec32f3a | 일치 |
| all-in-one/registers/simulator-freeze.json | bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835 | 808ffac14dbd1b4a7d797fa6cd0d647635d90b47 | 일치 |
| all-in-one/registers/virtual-plc-test-results.json | a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64 | 757dd50e45184568facb8ff62900b39d3ce848d1 | 일치 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd | 0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8 | 일치 |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 | f610fd7c7ce14ae951b00cff57b969259bfb389d | 일치 |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b | 8c83a59fefd5b8b651ec3537ea4236a073f5e109 | 일치 |
| all-in-one/sources/decoded-original/0048-IdentXmlPart.xml | d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d | 64fc5a7f1ad33f3b901b00f0d22d23578ffabff8 | 일치 |
| all-in-one/sources/decoded-original/0058-IdentXmlPart.xml | 84db55242df6a85df73776bfd23bf16cc10e4da35fedca4942f4a43bc4cd1702 | f13bf595dc1b216bb375b7374b8d849dc7db7c95 | 일치 |
| all-in-one/sources/decoded-original/0059-IdentXmlPart.xml | f02ef8f08f1c7ca7625bdbcf90a2c9365f12654d19e2e526fe8e5b0b742263d0 | ccbe8f3e8aadc1c9a052629b674e47805371c84b | 일치 |
| all-in-one/sources/decoded-original/0064-IdentXmlPart.xml | ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d | 300d74239868f4f4595d4d5bbb848b4b58bbae76 | 일치 |
| all-in-one/sources/decoded-original/0147-FlgNet.xml | 386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c | 0027890eca158e714dd6260dc920a5d3aa83319b | 일치 |
| all-in-one/sources/decoded-original/0148-FlgNet.xml | 1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313 | 3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3 | 일치 |
| all-in-one/sources/decoded-original/0260-FlgNet.xml | c0812e84eaac7d42ef9b89f2947ac162a5dd0364424fb51d2a6ccae8297f42ac | 32edefcc37a42cbfadec4de00a78914f773a17ca | 일치 |
| all-in-one/sources/decoded-original/0261-FlgNet.xml | 2cb282a051d3767e256d319453453499c5cc339b725ed78e3e263466f0ef8498 | 85541e116e054e8ad430e22bedf511e5fe51d9cb | 일치 |
| all-in-one/sources/decoded-original/0274-FlgNet.xml | 4cd023464a66193239fe70b782cb1271f7c9d06b97f53dd80e4c81d80014cd66 | f9664e6a84a57b0370d14c2ef76b0dca62c9dac3 | 일치 |
| all-in-one/sources/decoded-original/0323-FlgNet.xml | 2c71fa2f9c4598d2f0596bc796042d42ab78103e0ddba940c85f06ec595e9a42 | 43453ad0dab625bb0b4036de8c5b4109c9ddc7cc | 일치 |
| all-in-one/sources/decoded-original/0339-FlgNet.xml | ce2c6279b55c8a5ac837a0f7c7a0945636df7dc52b68a1c3d6ec158234b37543 | df1b2a3dd9389a264ed6cebee9c4e3a7270fc6fb | 일치 |
| all-in-one/sources/decoded-original/0378-FlgNet.xml | 51c9c18d1029cbf45669702fbdd81061fd7121d49fd3e2f4b2cb558c3365ae3a | 25c2f0e1bbd6ef2fd03f5693ff4d5dba964d5a20 | 일치 |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 | 4ab8370493c4e28fc1eabeeebe2743d27f0c4021 | 일치 |
| all-in-one/sources/decoded-original/0401-FlgNet.xml | 60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae | aadefbd35d305dd4a1146bf383b988a903802bf4 | 일치 |
| all-in-one/sources/decoded-original/0440-FlgNet.xml | a7e71653147751d8e9579dbb9a5be101b531c03612843cd0cb96cf86d6d179d4 | 7cb9552d244068dd454c79e0d02a43ca3522c6fa | 일치 |
| all-in-one/sources/decoded-original/0562-IdentXmlPart.xml | 85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c | 1609802542a3e560baba3f2b73c306be281dfb23 | 일치 |
| all-in-one/sources/decoded-original/0563-IdentXmlPart.xml | 86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad | 6a10fc694f896cda16409804daf2554c91635654 | 일치 |
| all-in-one/sources/decoded-original/0602-IdentXmlPart.xml | 46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf | bcb12ab1ce8c476ff921baa1608f29d9822f76b4 | 일치 |
| all-in-one/sources/decoded-original/0603-IdentXmlPart.xml | e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8 | 3a92b304baf4dbf6147e944d9778d2da11285cb1 | 일치 |
| all-in-one/sources/decoded-original/0604-IdentXmlPart.xml | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af | bb2c318788b97e7a4924a176275c12d805aa519d | 일치 |
| all-in-one/sources/decoded-original/0605-IdentXmlPart.xml | 0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b | 30e199288c147aa22d5ce8407178a391b89c6b1b | 일치 |
| all-in-one/sources/decoded-original/0606-IdentXmlPart.xml | 73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740 | ced032fa747a8544abf17058ee5ebaa78ba9b23b | 일치 |
| all-in-one/sources/decoded-original/0613-IdentXmlPart.xml | 09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb | c9d19a48e947098914f4d2de3348c05b4f6d37e8 | 일치 |
| all-in-one/sources/decoded-original/0614-IdentXmlPart.xml | c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294 | da0485aa033700f08c8695d30b93ebd2d377d6c7 | 일치 |
| all-in-one/sources/decoded-original/0615-IdentXmlPart.xml | 80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a | 49eb86fe01feb83de8c0864b21493d305aff8b20 | 일치 |
| all-in-one/sources/decoded-original/0616-IdentXmlPart.xml | 650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d | 9f7fdd5f93ac149c139a054ebb34f63c632ef7fd | 일치 |
| all-in-one/sources/decoded-original/0623-IdentXmlPart.xml | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 | 13b3af0459c8e6069bb9b2f1b16454bf479e08dc | 일치 |
| all-in-one/sources/decoded-original/0624-IdentXmlPart.xml | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a | 02511fea47fc47981c101bba49dc40adde1cdcc3 | 일치 |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb | 61ebc0abbb2ca160e11e1da400a3f14a397d8bc5 | 일치 |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd | 170ca5c72599edc7ea7eefe651c3680ce325e76a | 일치 |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 | 058129bb01e27f7a6a0d0293f332d745e5bab74e | 일치 |
| all-in-one/sources/decoded-original/0632-IdentXmlPart.xml | fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9 | 600935fa8d394c0d247ea20040d5dfff4f05b500 | 일치 |
| all-in-one/sources/decoded-original/0633-IdentXmlPart.xml | 9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc | a1ab5ee12addbc92d04c9950d4437e2b564d6b5c | 일치 |
| all-in-one/sources/decoded-original/0655-IdentXmlPart.xml | 38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb | 83b60b9de4541a3ffa6ee0db98205a372b525665 | 일치 |
| all-in-one/sources/decoded-original/0656-IdentXmlPart.xml | 0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592 | 9bfb9842e55901bab9a71d1ac03158467dfbb1bc | 일치 |
| all-in-one/sources/decoded-original/0657-IdentXmlPart.xml | 0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b | e625f3d8999c7be7d88c50eab0d93107117b58ec | 일치 |
| all-in-one/sources/decoded-original/0658-IdentXmlPart.xml | 998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831 | de9a12a6be87466ef1bf05df71c54580c556a827 | 일치 |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 | 424430b6b953e43138e5d0a18ca40c949e21cfa1 | 일치 |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 | cf4c0650e7c7baac350dcb89909b808435704880 | 일치 |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc | 587c3748ad9224718f95ba06463fee913dae231d | 일치 |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 | e546f39535d2b589e80f97db869ac37ce4d05cfd | 일치 |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 | f76a570cc73098632e08759b17934000f7e3a253 | 일치 |

후속 담당자는 본 초안과 LD01/LT01 공통색인을 함께 읽고 고유핵심을 독립검토한다. 현장 자료가 새로 없으면 미확정을 유지한다. 이 초안으로 로컬 통합/게시·현재CPU·실물복구 완료를 주장하지 않는다.
