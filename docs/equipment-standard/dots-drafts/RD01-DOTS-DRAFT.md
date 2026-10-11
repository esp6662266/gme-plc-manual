# 킬른 후보 RD01(P06) — Dots 독립 원본 조사·문서 초안

- 기준: 공개 esp6662266/gme-plc-manual, all-in-one, 고정 abcf31c5030bc7ef8749ed8e869a857f2387a28a/v1.12.0. 조사일2026-10-11 KST. 이 고정점은 RD01 게시 버전이 아니다.
- 범위: 킬른 후보의 식별과 RD01 구동·냉각팬·윤활·연동 제어. 사용자가 유일한 로컬 코드 편집·검증·게시 담당이며 Dots는 자체 환경에서 직접 조사·초안만 작성한다.
- GME-STD-1.0.0 및 공개 rollout SKILL/WORK-STANDARD/WORK-ITEM-TEMPLATE/INVENTORY를 적용했다. tia-equipment-alarm-trace 로컬 스킬은 확보하지 못했으며 권한 확장 없이 공개 XML·선언·실제 PDF 렌더를 대조했다.
- 공통 코드·버전·대장·배포·운영 기록 변경, 시뮬레이터 작성·수정·생성·실행·행동시험, 실제 PLC·현장·보호값·별도 SEJIN 프로그램 변경은 없다. 원자료와 완료·미확정 내용은 보존한다.
- 현재 CPU·실물·정상 극성·현행 보호 설정·실제 복구는 미확정이다. 문서의 정적 조건은 운전/보호 변경 지시가 아니다.

## 먼저 재확인할 고유 사항

1. **킬른=P06과 RD01은 candidate 관계**다. 이름만으로 본체·구동부를 하나로 확정하지 않는다. M03 주 구동, M04 냉각팬, EV03 윤활은 별도 출력/회로다.
2. 주 구동 fault/INV는 공동5초 감시(Tag54/T49)를 쓰지만 서로 다른 래치다. 팬은2초(Tag55/T52)로 구분한다.
3. 0243의 SET_PERC_FR01=0 요청 해제와0465의 같은 값 최소5/최대100 보정 쓰기를 함께 보존한다. 호출 순서·현재 실행을 확인하지 않고 0정지/최저속도를 확정하지 않는다.
4. EV03 타이머는 데이터 Word를 사용한다. KF_KT 호출의 SEC=0만 보고 작업·대기 시간을 초 단위로 만들어 넣지 않는다.
5. FG20 실제 START 접점21KA1은 **5–9**, RESET17KA1은 **6–10**이다. FG21 윤활21KA2 부하도 **5–9**다. 기존 START1–9 설명은 정정 후보다.
6. FG21의21KA2 코일 A2는0Vac9.9 선에 그려져 있으나 A1은A5.1 출력이다. FG141 A5.1의 반대쪽 참조는66/4로 되어 있어 FG21과 어긋난다. 실제 결선으로 임의 수정하지 않는다.
7. HMI 호출의 미결속과 EV03의 표시 후보를 남긴다. 표시 이름 LS_Open/Close만으로 실제 리미트센서를 추가하지 않는다.
8. 시공 M03 케이블 SIZE16 대25SB 상충(C04)을 보존한다. 실제 케이블·보호 설정을 도면 수치로 결정하지 않는다.

## 1 설비와 자료 기준

### 1.1 식별·본체·하위 설비

INVENTORY.json P06은 이름 킬른, catalog_id RD01, mapping=candidate, identity_verified=false, queue_state=identity_review이며 “킬른 본체와 RD01 구동 설비의 관계를 확인. 동일 설비로 병합하지 않음”이 원문 경계다. 태그 식별 근거와 현장 동일성을 구분한다. [E01]

PID_1684n002I.pdf PDF1에는 CC01과UC01 사이 RD01, M03(30kW440V),M04(0.75kW440V),EV03이 보인다. 인접 PV01/PV02·PV04·SC12를 RD01 소유로 일괄 이전하지 않는다. 전기도면 FG20 M03 ROTATING DRUM 30kW50.1A와FG22 M04 COOLING FAN 0.75kW1.67A는 각각의 인쇄 정격이다. [E02,E17,E19]

### 1.2 기존 자료 보존

RD01의 devices/control-specs/alarm-guides/circuit-guides/signal-guides/construction-guides/procedures 7파일을 읽고 보존했다. 기존5초 감시·본체 후보·윤활/팬 분리·시공C04 공백을 유지한다. 기존 시뮬레이션 항목은 원자료에 존재하더라도 이번에 생성·갱신·실행하지 않았고 완료나 실행 계획으로 승격하지 않는다. [E24]

### 1.3 표기

이하 네 자리 Flg는 all-in-one/sources/decoded-original/NNNN-FlgNet.xml, Ident는 같은 폴더 NNNN-IdentXmlPart.xml이다. LAD는 network-map document_id, NID는 선언 네트워크 식별자다. Part/Wire/ORef UID와 선언RID를 따로 기재한다. PDF·CSV·index는 all-in-one/sources/ 아래이며 부록 해시에서 정확한 경로를 연결한다.

## 2 I/O·HMI·선언

### 2.1 고유 신호와 데이터 층 [E03,E04]

| 대상 | 백업 선언/주소 | 의미·경계 |
| --- | --- | --- |
| Start RD01 | 0602 RID48 Bool Output AO1 = Q0.1 | 0243 C240;FG136 MOD14단자2→FG21 |
| Start fan RD01 | 0602 RID56 Bool Output AO2 = Q0.2 | 0245 C287;FG136단자3→FG22 |
| EV03 | 0602 RID53 Bool Output AO41 = Q5.1 | 0244 C268;FG141 MOD15단자12 |
| RD01_Fbk | 0602 RID276 Input AO2 = I0.2 | 원시운전응답;0238과0309 사용 |
| RD01F_Fbk | 0613 RID134 Input AO4 = I0.4 | 팬원시응답;0310 사용 |
| rd01_all_inv | live_index doc953,I0.3 | 원시 동명SimpleAccess 직접 결속 미확보;처리DB로 대체하지 않음 |
| Inputs.RD01 run | 0657 RID268 AO2,DB13.X0.2 | 알람 처리층;원시태그/현재값과 구분 |
| Inputs.RD01_All_inv | 0657 RID270 AO3,DB13.X0.3 | 인버터 이상 입력 가공층 |
| Inputs.fan RD01 run | 0657 RID271 AO4,DB13.X0.4 | 팬응답;주 구동 요청해제 조건에도 사용 |
| RD01_SP_SPEED | 0664 RID48 Word Output Peripherie AO2320 = PQW290 | 0465 배율 출력;현행 아날로그 구성 미확정 |
| RD01_Current | 0678 RID285 Int Input Peripherie AO2656 = PIW332 | 전류 원시 입력;0627 RID105에도0398참조 |
| Inputs.RD01_ABSORBPTION | 0629 RID107 AO512,DB13.DBW64 | 0398 raw Move,HMI INT64와 대응 |
| Data.Amp_RD01 | 0676 RID288 AO800,DB1.DBW100 | 0519 환산값;위 raw HMI값과 같다고 보지 않음 |
| Coeff.COEFF_DRUM_A_RD01/ ZERO_DRUM_A_RD01 | 0676 RID286/287 AO816/800,DB4.DBW102/100 | 계수/영점의 현재 값은 미확정 |
| Allarm.RD01_Absorbption_OFR | 0676 RID422 AO193,DB3.X24.1 | 환산범위 이상;모터 인버터알람과 별개 |

DB 번호는0603/0655/0674의 DepDBBlock TOD와 BAD 관계를 대조했다. Data=DB1,Flag=DB2,Allarm=DB3,Coeff=DB4,Inputs=DB13이다. 단순히 같은offset을 가진 심볼을 동일 변수로 합치지 않는다.

### 2.2 내부 요청·알람·설정 [E05~E11]

| 변수 | 선언과 백업 주소 | 역할 |
| --- | --- | --- |
| Flag.M_RD_01 | 0604 RID47 AO1,DB2.X0.1 | 운전요청;자동Set/요청해제/HMI쓰기 구분 |
| Flag.M_RD_01_FAN | 0604 RID55 AO2,DB2.X0.2 | 팬 요청 |
| Allarm.RD_01_FAULT | 0657 RID41/0604 RID43 AO1,DB3.X0.1 | 주구동 응답부재 래치 |
| Allarm.RD01_INV | 0657 RID210/0604 RID203 AO153,DB3.X19.1 | 별도 인버터 이상 래치 |
| Allarm.RD_01_FAN_FAULT | 0657 RID45/0604 RID54 AO2,DB3.X0.2 | 팬 응답부재 래치 |
| Data.SET_PERC_FR01 | 0604 RID44/0662 RID43 AO48 Int,DB1.DBW6 | 속도설정·0비교·최소/최대 보정의 같은 대상 |
| Data.EVFR01_Work_time/Wait_time | 0604 RID50/52 AO736/752 Word,DB1.DBW92/94 | S5 timer value 인수;현재 시간 미확정 |
| Data.EV_03_W/EV_03P | 0604 RID237/238 AO2496/2512 Int,DB1.DBW312/314 | KF_KT 입력값;현재설정 미확정 |
| Tag_54 / Tag_55 | 0658 RID39/43 Timer AO49/52 = T49/T52 | 주구동5S/팬2S감시 |
| Tag_115 / Tag_116 | 0602 RID49/51 Timer AO58/59 = T58/T59 | 윤활 대기/작업 순환참조 |
| Disable_Load_RD01 | 0605 RID16 InterfaceAccess AO1 | 블록 인터페이스 값;절대M/I/Q주소로 만들지 않음 |

### 2.3 입력 전달·전류 처리·다른 쓰기 [E04,E12]

0397 LAD1070 NID1 Move22.in W23/ORef25=0627 RID3 Input Word AO0(IW0),out1 W24/ORef26=0629 RID5 Word AO0,BAD4→0628 RID4 Inputs TOD13이다. I0.2/.3/.4가 포함된 Word를DB13.DBW0으로 전달하는 정적 경로다. 현재 별도반전·다른쓰기 전체 완전성은 확정하지 않는다.

0398 LAD1071 NID2는 powerrail→Move144, in W157/ORef148 RD01_Current, out1 W159/ORef149 Inputs.RD01_ABSORBPTION이고 ENO W158은다음Move145로 이어진다. 0519의별도 선형화와 구분한다. main0030의hmi inputs 호출은 ENO와NOT Simulation(1) M180.0 경계가 있으며 항상실행이라고 가정하지 않는다.

원본0635는 Inputs.RD01 run(RID8 UID38 Write),Inputs.fan RD01 run(RID206 UID42 Write)의 기존simulation관련 다른쓰기를 포함한다. 존재만기록하고 활성이라고 추정하지 않는다. 시뮬레이터는 실행하지 않았다. Data.SET_PERC_FR01에는0642 RID92 NID1 UID3840의다른Write도있다. 레시피/HMI/간접쓰기 전체는미확정이다.

### 2.4 HMI 설정과 호출 [E13,E14]

CSV의RD01관련8행은 RD_01 Allarme1 DB11.X2.1(ID00449),RispostaA DB11.X2.0(00327),Flag DB2.X0.1(001B3); RD_01_FAN Allarme1 DB11.X4.1(0044B),RispostaA DB11.X4.0(00326),Flag DB2.X0.2(001B2); Editor_RD01 DB26.INT12(00415); I_RD01_ABSORBPTION DB13.INT64(0002C)이다. AccessName PLC이며현재버튼동작/접근권한/온라인값의증거는아니다.

- 0358 LAD1179 HMI Standard Motors CRef23/CodeBlock22(0624RID638/0623RID1): 비EN8핀 중Alarm3/4/5는0626RID20 false,나머지5핀은미결속이다. Ingresso_run W24/ORef25RID713,Alarm1 W28/29RID32,Alarm2 W30/31RID33,Risposta W42/43RID25,Comulativo W46/47RID27. 다른블록0552의RID25literal0 후보는네트워크범위가달라결속하지않았다. literal호출범위는NID2를지지하지만생성인덱스NID는없음을함께남긴다.
- 0359 LAD1180 CRef22/CodeBlock23 같은함수: run W37/24RID712,Alarm1 W39/26RID44,Risposta W46/33RID37,Comulativo W48/35RID39는미결속. Alarm2 W40/27RID48FALSE,Alarm3/4/5 W41/28,W42/29,W43/30RID20false. NID3후보이나복수호출범위가있어원래NID전체결속은미확정이다.
- EV_03 LS_Open DB11.X86.0(ID00453),LS_Close DB11.X86.1(ID00454)는추가표시2행이다. 0396 LAD1220은EV03직접Contact23→Coil27(W26/ORef28RID790미결속),NOT EV03 Contact29→Coil30(W36/ORef32RID791미결속)이다. 두입력ORef24/34는0063RID789Q5.1로결속된다. 출력미결속을HMI주소로단정하지않으며,LS라는표시명만으로실제센서피드백으로쓰지않는다.

## 3 제어 구조·소유·상충

### 3.1 주 구동 요청 해제와 실제 Q [E05]

0243 LAD1936 NID7:ON Contact270(W252/ORef241)→W271에서다섯해제조건과출력요청가지로분기한다.

- fault Contact272 W253/ORef242 →W24 OR28.in1
- INV Contact22 W21/ORef23 →W29 OR28.in2
- Eq227:SP W254/ORef243 ==0 W255/ORef244 →W31 OR28.in3
- NOT팬응답 Contact26 W25/ORef27 →W32 OR28.in4
- NOT R2_GATE_LOOP_ON Contact278 W260/ORef247 →W279 NOT STANDBY_ON Contact280 W261/ORef248 →W33 NOT UNDER TESTING Contact35 W34/ORef36 →W37 OR28.in5
- OR28.out W30→RCoil236,operand W265/ORef249=Flag.M_RD_01.
- 별도ON분기→Flag.M_RD_01 Contact282 W266/ORef250→W283 Coil240,operand W268/ORef251=Start RD01 Q0.1.

따라서 Reset요청조건은 ON AND(fault OR INV OR SP=0 OR NOT팬응답 OR(NOT R2loop AND NOTStandby AND NOTUnderTesting)),출력가지의정적식은ON AND Flag.M_RD_01이다. RCoil과Coil의실행순서/현재CPU주기에따른결과는미확정이다. UNDER TESTING은원본심볼이며우회조작을권하지않는다.

### 3.2 냉각팬 요청과출력 [E06]

0245 LAD1939 NID9:ON307(W295/ORef288)→fault309(W296/289) OR[NOT R2loop311(W297/290) AND NOTStandby313(W298/291) AND NOTUnderTesting318(W321/319)]→OR278.outW300→R283 Flag팬(W302/292). 별도ON→Flag팬315(W303/293)→W316 Coil287(W305/294)=Q0.2다. 팬요청해제와주구동해제는조건수가다르며복사하지않는다. 팬응답상실이주구동요청해제에영향을주지만팬소유를본체상태전체와동일시하지않는다.

### 3.3 자동 순서의 쓰기 소유 [E07]

0164 LAD1843 NID3 공통은ON785→NOT Emergency_module_fault22→Tipo_preset=1 Eq400→Auto_ON1 Contact823이다. Tempo_presetting 비교값19(Eq466,W711/ORef618와W712/619)→S469 팬요청W715/620;21(Eq472,W716/621와W717/622)→S478 주구동요청W719/623 및Move481 literal25W720/624→SP W721/625다.

0165 LAD1844 NID4의생산순서Tipo_preset=2에서도공통ON/비상모듈fault반전/Auto_ON1을거친다. 단계33 Eq814→S817팬(W1077/ORef971),35 Eq820→S826주구동(W1081/974)와Move82925(W1082/975)→SP(W1083/976)다. 단계숫자를확인없이초로부르지않는다.

0166 LAD1847 NID5는Auto_ON1 Contact1095(W1028/983)→Tipo_preset=5 Eq881이다. 단계15 Eq935(W1060/1006,W1061/1007) OR Emergency_module_fault1118(W1121/1119)→OR42W1062→R939주구동W1063/1008. 단계17 Eq945(W1066/1010,W1067/1011) OR fault1114(W1117/1115)→OR39W41→R948팬W1070/1012다. 이정지네트워크앞단에ON을추가하지않는다.

요청변수의선언0577 RID40(주구동)/36(팬)의NID3·4 Set 및NID5 Reset 참조와대조했다. 자동순서와HMI·0243/0245의다른쓰기를함께보존한다. 현재모드우선순위·종합재시작·전체설비안전조건은확정하지않는다.

### 3.4 속도 출력과0설정 상충 [E08]

0465 LAD1684 NID6:ON455(W438/ORef426)→세가지병렬경로다.

1. Lt406 SP(W439/427)<5(W440/428)→Move409 in5(W443/429)→SP out1(W444/430).
2. Gt414 SP(W445/431)>100(W446/432)→Move417 in100(W449/433)→SP(W450/434).
3. Mul422 in1SP(W451/435),in2 literal272(W452/436),out W453/ORef437 RD01_SP_SPEED(0664RID48 Word Peripherie Output AO2320).

SP는0662RID43와0243의0604RID44가같은Data.SET_PERC_FR01 Int AO48/DB1.DBW6을지시한다. 0설정해제와최소5보정은동일값에대한정적상호작용이다. 이를버그로고쳐쓰거나현재0정지가항상성공/실패한다고단정하지않는다. ×272를×276.48로수정하지않으며현행출력스케일·드라이브AI모드·%→Hz관계도미확정이다.

### 3.5 EV03 윤활 타이머와밸브 [E09]

0244 LAD1938 NID8:ON295(W280/269)→StartRD297(W281/270)→W298.

- NOT Tag115 Contact299(W283/272)→SD257.in,value W282/ORef271 Data.EVFR01_Work_time,operandW285/273 Tag116=T59.
- Tag116 Contact301(W287/275)→SD262.in,valueW286/274 Data.EVFR01_Wait_time,operandW289/276 Tag115=T58.
- NOT Tag116 Contact303(W290/277)→ON305(W291/278)→W306 Coil268,operandW293/279 EV03 Q5.1.

원문출력은ON AND StartRD AND NOT Tag116 AND ON이며밸브actual피드백접점은이가지에없다. 0275 LAD1937 NID45의KF_KT CRef36은powerrail허가, KF W37/ORef38=Data.EV_03_W,SEC W39/40=0,KT W42/43=Work_time;ENO W41→CRef45,KF W46/47=Data.EV_03P,SEC W48/49=0,KT W51/52=Wait_time이다. 0058RID241 FCBlock KF_KT,0059RID248인터페이스와0604/0606 선언을대조했다. 이번network-map에서KF_KT본문을결속하지못했으므로숫자초·시간기반·포화/오류동작을추정하지않는다.

### 3.6 투입 금지와주구동 정지는다른 소유 [E10]

0238 LAD1931 NID2 ON91(W78/ORef67)→OR56 8입력: LOW_TC03_TEMP95(W80/69),Oxigen_Fault97(W81/70),Oxigen_Too_high99(W82/71),STANDBY_ON101(W83/72),MAX_MAX_TC09103(W84/73),HYDROGEN_BOX_FAULT105(W85/74),NOT R1 Gate ON107(W86/75),NOT raw RD01_Fbk22(W21/23). ORoutW88→Coil66,operandW90/77 Disable_Load_RD01(0605RID16 InterfaceAccess)이다.

이인터페이스값은0239 NID3 Contact155(W134/ORef121)→OR97.in6→R109 Flag.M_BWF01(W140/123),0240 NID4 Contact193(W172/159)→OR135.in6→R147 Flag.M_BWF02(W178/161)에쓰인다. 각네트워크에는별도의ON과다른조건도있다. 따라서투입요청해제영향과RD01 Q직접정지를구분한다. 본체전체의안전차단성능이나현재공정허가를이부분만으로판정하지않는다.

### 3.7 전류 환산·운전시간 기록 [E11,E12]

0519 LAD1771 NID38 ON1515(W1509/ORef1502)→W1516 Signal linearization CRef1496.en. IN0W1510/1503=ON;AnalogW1511/1504=RD01_Current;CoeffW1512/1505;ZeroW1513/1506;OutValueW1514/1507=Data.Amp_RD01;OFRW24/23=RD01_Absorbption_OFR. 0291/0014의공통선형화정수계산·범위경계는별도근거이며현재전류A단위·교정값은확정하지않는다.

0309 LAD1019 NID21 Tag47 Contact1208(W1191/1179) AND rawRD01_Fbk1210(W1192/1180)→Add1162(MIN+1 W1193/1181,W1194/1182,outW1195/1183),병렬Ge1169 MIN≥60(W1196/1184,W1197/1185)→Move1172 **literal1** W1200/1186→HOUR W1201/1187,ENO W1202→Move1175zero W1203/1188→MIN W1204/1189,ENO W1205→S1178Flag_Aggiorna_DB W1206/1190다. HOUR+=1로바꾸지않는다. 원본은Move1이며실제누적체계/주기/보존·다른쓰기전체를추가확인해야한다.

0615의RD01_MIN/HOUR AO640/656와팬MIN/HOUR AO672/688는0614 TOD9,즉DB9.DBW80/82와84/86이다. 팬0310·공통0336의다른쓰기참조도보존한다. 시간기록은실제회전량·킬른정상·정비완료증거가아니다.

## 4 전기 전달 경로·도면 끝점

### 4.1 M03 주 구동·START/RESET/STO [E17,E18]

Electrical_Rev2.pdf FG20/PDF21:6.2L1/L2/L3 440V60Hz→20QM1(인쇄54–65A,RATING62A)→20R1/S1/T1→20AS1 ABB ACS580-01-062A-4 30kW U1/V1/W1. U2/V2/W2→20U1/V1/W1,20SCH1차폐→20QS1→M03 RD01 U/V/W/PE. 모터인쇄30kW50.1A,BLACK FS17 16mmq는도면표시이며현재명판/케이블/보호기설정이아니다.

- START부하:인버터단자10 +24V→20.1→**21KA1 5–9**→20.2→단자13 DI1.
- 코일:FG136/PDF137 MOD14 단자2 A0.1→FG21/PDF22 XS3→20QS1보조→XS4→21.1→20QM1보조→21.2→21KA1A1/A2→−0Vdc10.6.
- RESET부하:단자10→**17KA1 6–10**→20.7→단자15 DI3. FG17/PDF18 A7.4(143/1)→17KA1A1/A2→−0Vdc10.6. 현행PLC Reset출력조건과드라이브복구정책은미확정이다.
- STO:단자34 OUT1→14KA1접점3–4→단자37 IN1;단자35 OUT2→14KA5접점3–4→38 IN2. FG14/PDF15의14KA1상류는13.5(13/4),14KA5는13.6(13/5),A2귀로는0Vac9.9다. 원본교차참조끝점까지만대조했으며전체안전체인·현행STO설정·안전등급을확정하지않는다.

접점5–9와6–10은실제부하선을확대한PDF렌더에서각각확인했다. 기존1–9문구와하단접점표를구분한다. 앞선MV06의접점번호를RD01에복제하지않았다.

### 4.2 운전응답·이상·아날로그 [E19]

FG20:+24Vdc10.7→인버터22,24→E0.2→FG116/PDF117 MOD8단자3. +24V→25,27→E0.3→MOD8단자4. RUNNING/ALARM제목은현재드라이브릴레이기능·정상극성의증명이아니다.

속도:+PAW290/−PAW290→인버터2 AI1+/3 AGND−. FG112/PDF113 MOD7의PAW290는단자5 QV1/QI1와단자8 MANA. 도면4–20mA인쇄와원본PQW290계산을대조하되현재AI1모드/Hz스케일은남겨둔다.

전류:인버터8 AO2+ /9 AGND−→+PEW332/−PEW332→FG109/PDF110 MOD4단자30 I6+ /32 U6−·I6−. 20SCH2차폐연결도확인했다. AO2실제기능/전류환산은파라미터·교정근거가필요하다.

### 4.3 M04 냉각팬 [E20]

FG22/PDF23:8.3L1/L2/L3→22QM1(인쇄1.4–2A)→22KM1전력접점→22U1/V1/W1→XM→22QS1→M04 RD01F U/V/W/PE. 모터0.75kW1.67A,전선BLACK FS17 1.5mmq 인쇄다.

제어:FG136 MOD14단자3 A0.2→XS5→22QS1보조→XS6→22.1→22QM1보조→22KM1A1/A2→−0Vdc10.6. 응답:+24Vdc10.7→22KM1보조13/14→E0.4→FG116 MOD8단자5. 접촉기보조응답이팬풍량·냉각정상·주구동회전증명은아니다.

### 4.4 EV03 부하·코일 귀로 상충 [E21]

FG21/PDF22:110Vac9.7→**21KA2 5–9**→21.3→X1/50의2AF퓨즈→21.4→EV03 A1/A2→X1/51→0Vac9.9. 밸브실부하는110Vac도면회로다.

같은페이지21KA2코일은A1=A5.1(141/1),A2가**0Vac9.9**에연결되어그려져있다. 이를−0Vdc라고대체하지않는다. FG141/PDF142는MOD15단자12 A5.1 “EV-03 VALVE COMMAND”이지만신호끝교차참조가66/4다. 실제FG66/PDF67은ER01/66KA1 A5.0회로이며EV03의위치가아니다. 이교차참조상충과코일귀로표기를현행배선오류로단정하지않고원본불일치로남긴다.

### 4.5 시공 경유·케이블상충 [E22]

시공 Electrical_Can_Decoating_20241118.pdf PDF24 ROTARY SIDE01은M03/M04,ROT1TB1→ROT1TB2→EV03과PV02센서/밸브경유를함께그린다. 공유접속함을본체동일성·제어소유증명으로쓰지않는다.

| 페이지·행 | 전체ID/경로 | 인쇄규격·길이 | 경계 |
| --- | --- | --- | --- |
| PDF51 1_5 | =ROT+RD01-M03A,CR→RD01 M03 | DAC/PVC-S4/25SB,spare0,100RC→E100,LEN39 | PDF24동일행SIZE16과상충C04 |
| PDF51 1_6 | =ROT+RD01-M04A,CR→RD01 M04 | GAC/CV4/1.5,spare0,100RC→E200,LEN39 | 주구동과팬을분리 |
| PDF55 5_2 | =ROT+UC01-ROT1TB1B,UC01→ROT1TB1 EV03/04/05 | AC/CVV12G1.0,spare5,100RDD1→E2005,LEN52 | 공유밸브케이블 |
| PDF55 5_3 | =ROT+RD01-ROT1TB2A,UC01 ROT1TB1→RD01 ROT1TB2 EV03 | AC/CVV3G1.0,spare0,RDD1/E110,LEN9 | 경유함·소유구분 |
| PDF55 5_15 | =ROT+RD01-EV03A,RD01 ROT1TB2→RD01 EV03 | AC/CVV3G1.0,spare0,E111,LEN3 | 개별말단;OEM단자와실물대조미완 |

LEN은설계표의값이며실측길이가아니다. SIZE16/25SB중하나를임의선택하지않는다. 시공표의승인·준공·현재일치도미확정이다.

### 4.6 실제 페이지별 개정란

FG17/20/112/136은Rev2 17.03.2025,FG14/21/22/66/109/116/141은개정란공란으로확인했다. PDF파일명Rev2를모든페이지개정란에복제하지않는다. 같은파일의다른페이지를이표만으로판정하지않는다.

## 5 알람·별칭·복구 경계

### 5.1 주 구동 두 래치와공동5초 [E15]

0424 LAD1787 NID8:ON351(W337/ORef327)→StartRD353(W338/328)→W354에서NOT Inputs.RD01 run374(W377/375) 또는Inputs.RD01_All_inv378(W381/379)→OR32.outW34→SD315.in이다. valueW339/ORef329=0656RID175 S5T#5S(V1280),operandW340/330=0658RID39 Tag54=T49.

Start뒤Tag54 Contact355(W341/331)→W21에서두Set으로갈라진다.

- NOT RUN357(W342/332)→W358 S321,operandW344/333=RD_01_FAULT DB3.X0.1.
- INV364(W30/31)→W29 S365,operandW371/367=RD01_INV DB3.X19.1.

동일타이머를공유해도서로다른알람원인·비트다. RD_01 HMI Allarme1이라는단일표시명으로두래치를하나로합치거나HMI미결속을확정하지않는다.

Reset공통ON→RESET_ALLARM359(W346/334)→W22. fault361(W347/335)→R326(W349/336),INV372(W24/25)→R373(W27/28)이다. 각Reset가지에는원인입력정상화접점이별도로없다. 이것만으로즉시재발·래치우선순위·현재Reset성공을확정하지않는다.

### 5.2 팬의별도2초 [E16]

0425 LAD1788 NID9:ON385(W371/361)→Startfan387(W372/362)→NOT팬RUN398(W401/399)→SD349,valueW373/363=S5T#2S,operandW374/364=Tag55 T52. Start뒤Tag55389(W375/365) AND NOT팬RUN391(W376/366)→S355(W378/367)=RD_01_FAN_FAULT DB3.X0.2다. Reset은ON→RESET393(W380/368)→fanFault395(W381/369)→R360(W383/370)이다.

현재팬고장과주구동5초감시를혼동하지않는다. 0243의팬RUN부재요청해제는팬알람2초래치와별도경로다. 따라서“주구동은팬fault2초후에만정지”라고요약하지않는다.

### 5.3 복구 완료로넘기지않을것

원인입력해소,RESET_ALLARM요청,래치해제,운전요청변화,Q출력,인버터/접촉기응답,윤활/냉각/상하류상태,현장복구증거는각기다르다. 현재CPU/현장자료가없으므로복구성공·보호정상·정상극성·권장시간을채우지않는다. 강제출력·접점우회·보호값상향·타이머연장·실제운전시험을이문서에서제안하지않는다.

## 6 증상별 확인 자료

| 증상 | 원본상비교할경로 | 필요근거와미확정 |
| --- | --- | --- |
| 주구동요청유지안됨 | 0243다섯Reset가지/자동순서다른쓰기/SP보정 | 현재호출순서·SP·팬RUN·R2loop·Standby기록;임의우회금지 |
| Q는있지만인버터기동안됨 | Q0.1→FG136/21코일→FG20 21KA1 5–9→DI1 | 현장전압·접점·구성은미측정;PLC만의고장으로단정불가 |
| 주구동fault/INV표시 | 0424공동5초와각원인입력→두별도래치→HMI미결속 | 발생시각/원인입력/표시매핑을각각확인 |
| 팬무응답 | 0245요청→Q0.2→22QS1/22QM1/22KM1→I0.4→0425 2초 | 팬풍량·모터상태는접촉기응답과구분 |
| 속도0지시와결과불일치 | 0243SP=0과0465최소5·자동25·레시피쓰기 | 호출순서/현재계산·PQW290/AI1설정필요 |
| 윤활밸브동작불명 | 0275KF_KT→0244T58/T59→Q5.1→21KA2→EV03 | 시간단위/코일귀로/FG141교차참조미확정;LS표시를센서로오인금지 |
| 전류값차이 | rawPIW332→DB13W64 대선형화→DB1W100 | 현행AO2기능·계수/영점·물리단위·교정자료필요 |
| 원료투입안됨 | 0238Disable_Load_RD01→0239/0240BWF요청Reset | 주구동회전과투입허가분리;전체BWF독립조사대체아님 |
| 운전시간이상 | 0309Move1/HOUR·MIN리셋·Tag47/다른쓰기 | 실제시간기반·누적보존·상위DB갱신미확정 |

관찰을수집할때는관찰자·시각/시간대·장치/프로젝트식별·값/단위·비교원본과최초불일치구간이필요하다. 이초안은실제측정이나운영기록작성결과가아니다.

## 7 완료 범위와통합 인계

| 영역 | 적용범위와남은것 |
| --- | --- |
| 설비·자료기준 | P06candidate/RD01구동·팬·윤활분리;킬른실물동일성미확정 |
| I/O·HMI | 원시·DB·표시층/미결속핀/주소/다른쓰기구분 |
| 제어구조 | 요청해제·최종Q·자동쓰기·속도보정·윤활·투입허가 |
| 전기전달 | 주구동·팬·EV03·응답·아날로그·STO/Reset끝점;상충보존 |
| 알람·복구 | 구동2래치공동5초/팬2초/범위알람분리;현장복구미확정 |
| 증상별수리 | 관찰자료·판단경계만작성,현장조작미수행 |
| 완료기준 | 독립통합검토용초안;UI/기록/게시/TIA/현재CPU/현장완료아님 |

통합자가먼저재확인할것: 0243/0465동일SP의0비교·최소5,0424공동5초와두래치,0425팬2초,0244/0275타이머값/소유,0238투입인터페이스,FG20 5–9/6–10와FG21 5–9,FG21코일귀로와FG141교차참조,시공C04. 이전설비전과정반복대신지정핵심근거부터대조한다.

누락: 현행프로젝트/CPU일치·호출순서/모드우선순위/모든쓰기,킬른본체와구동부관계의현장승인자료,KF_KT본문·현재시간설정,HMI미결속선언/현재화면이벤트,인버터AI/AO/릴레이/STO구성,윤활코일귀로와도면상충해소,케이블C04승인본·명판·보호기현행값,실제복구증거. 모르는항목을현재값으로채우지않는다.

다음자체조사한대상은승인순서의 **BR01(P11)** 이다. P06은자료초안을인계하되본체동일성보류를유지한다. 초안전달을23개게시완료집계에더하지않는다. 본초안작성시사용자확인게시완료는11/23(47.8%),기존제외2개를뺀11/21(52.4%)이다.

## 부록 A 핵심 주장 근거표

Flg/Ident의 전체 경로는§1.3 및부록C를따른다. 고정커밋의원본·핀·선언/페이지와해석/미확정경계를함께읽는다.

| ID | 주장 | 원본 | 위치 | 해석·미확정 |
| --- | --- | --- | --- | --- |
| E01 | P06/킬른 후보 | docs/equipment-standard/INVENTORY.json | P06 mapping=candidate,identity_verified=false | 킬른본체/RD01구동관계미확정 |
| E02 | P&ID 소유 | PID_1684n002I.pdf | PDF1 RD01/M03/M04/EV03,CC01~UC01위치 | 주변게이트/팬/윤활독립;실물미확정 |
| E03 | 신호 선언 | live_index.json;0602/0603/0604/0655/0657/0664/0674/0676/0678 Ident | Q0.1/.2/Q5.1,rawI0.2/.4,PIW332/PQW290;TOD/SSD/SAD | oldE/A주석보다원시선언구분;현행미확정 |
| E04 | 입력 전달 | 0397/0398/0030 Flg;0627/0628/0629/0690/0691/0692 Ident | LAD1070Move22W23/24;1071Move144W157/159;mainNOTSimulation(1) | DB13Word와환산Data구분;호출/쓰기완전성미확정 |
| E05 | 주구동 요청/출력 | 0243 Flg;0602/0603/0604/0606 Ident | LAD1936 NID7 OR28/R236/C240;NOT26/278/280/35 | 5해제가지와출력분리;실행순서미확정 |
| E06 | 팬 요청/출력 | 0245 Flg;0602/0603/0604 Ident | LAD1939 NID9 OR278/R283/C287 | 팬고유조건;주구동과동일조건복제금지 |
| E07 | 자동 쓰기 소유 | 0164/0165/0166 Flg;0575/0576/0577/0578 Ident | 1843S469/S478/Move481;1844S817/S826/Move829;1847R939/R948 | 19/21,33/35,15/17단계·설정25;초단위단정금지 |
| E08 | 속도/0설정상충 | 0465 Flg;0660/0661/0662/0664 Ident;0243 | LAD1684 NID6 Lt406/Move409,Gt414/Move417,Mul422W453/437 | 같은SP최소5/최대100×272;0Reset과현재순서미확정 |
| E09 | 윤활타이머 | 0244/0275 Flg;0058/0059/0602/0603/0604/0606 Ident | LAD1938SD257/262,C268;1937KF_KT36/45 KF/SEC/KT | T58/T59·DB1Word92/94;시간값/단위/본문미확보 |
| E10 | 투입 소유 | 0238/0239/0240 Flg;0602/0604/0605 Ident | 1931OR56/C66InterfaceRID16;0239Contact155→R109;0240Contact193→R147 | BWF요청해제영향;RD01직접정지와구분 |
| E11 | 운전시간 | 0309/0310/0336 Flg;0613/0614/0615/0616 Ident | 1019Add1162/Ge1169/Move1172literal1/Move1175/S1178;DB9 | HOUR+=1로바꾸지않음;실제시간기반/상위갱신미확정 |
| E12 | 전류/다른쓰기 | 0519 Flg;0672/0674/0676/0678/0680/0635/0642 Ident | LAD1771NID38CRef1496 W1511/1514/OFR24;0635InputsWrite;0642SPWrite | rawHMI/환산/기존simulation쓰기분리;현재활성추정금지 |
| E13 | 주구동/팬HMI | 0358/0359 Flg;0623/0624/0626 Ident;hmi_plc_tags.csv | LAD1179 3false5미결속;1180 4false4미결속;CSV관련8행 | 같은RID타블록배제;NID/알람매핑미확정 |
| E14 | EV03 HMI | 0396 Flg;0063 Ident;hmi_plc_tags.csv | LAD1220Contact23/NOT29→Coil27/30;ORef28RID790/32RID791미결속 | 표시LS이름을실물센서로간주금지 |
| E15 | 구동 알람 | 0424 Flg;0655/0656/0657/0658 Ident | LAD1787NID8SD3155S/T49;S321/S365,R326/R373 | 공동타이머2래치;Reset정상화접점없음·현재우선순위미확정 |
| E16 | 팬 알람 | 0425 Flg;0655/0656/0657/0658 Ident | LAD1788NID9SD3492S/T52,S355/R360 | 팬응답상실직접해제와2초fault분리 |
| E17 | 주동력 | Electrical_Rev2.pdf | FG20/PDF21 20QM1/20AS1/20QS1/M03 | 30kW50.1A/54–65A/RATING62A는인쇄값 |
| E18 | START/RESET/STO | Electrical_Rev2.pdf | FG20/21/17/14/136;21KA1 5–9,17KA1 6–10,14KA1/5 3–4 | 접점표와부하구분;현재STO기능/PLCReset소유미확정 |
| E19 | 응답·아날로그 | Electrical_Rev2.pdf | FG20/116/109/112;22→24,25→27;AI1 2/3,AO2 8/9,MOD4 30/32,MOD7 5/8 | 현재릴레이극성/4–20mA설정미확정 |
| E20 | 팬회로 | Electrical_Rev2.pdf | FG22/136/116;M04/22QM1/KM1/QS1/XS5·6/13·14 | 0.75kW1.67A인쇄;풍량/현재보호미확정 |
| E21 | EV03회로/상충 | Electrical_Rev2.pdf | FG21/PDF22 21KA2 5–9/X1 50·51;FG141/PDF142 A5.1→66/4;FG66/PDF67 A5.0 | 코일0Vac귀로/교차참조상충보존;현장결선추정금지 |
| E22 | 시공 경로 | Electrical_Can_Decoating_20241118.pdf | PDF24/51/55;1_5/1_6/5_2/5_3/5_15 | SIZE16대25SB C04·공유함·설계길이;실물미확정 |
| E23 | 공통선형화 | 0291/0014 Flg;0611/0612 Ident | LAD1658/1659범위Gt258/Le161,정수변환/계수/영점/OFR | 실제전류단위·현재교정의증명아님 |
| E24 | 보존/완료경계 | RD01.html7종;AGENTS/SKILL/WORK-STANDARD/TEMPLATE | 기존1–9정정후보·C04보존·7영역 | 초안인계와검증/게시/현장복구분리 |

## 부록 B 원본 HMI 핀 표

EN외핀만표시한다. 미결속은현재단선/0값을뜻하지않는다. 다른블록의같은RID/UID를결속하지않는다.

### 0358 CRef23

| 핀 | Wire/ORef | 선언상태 |
| --- | --- | --- |
| Ingresso_run | W24/ORef25 | RID713 미결속 |
| Allarme1 | W28/ORef29 | RID32 미결속 |
| Allarme2 | W30/ORef31 | RID33 미결속 |
| Allarme3 | W32/ORef33 | 0626RID20 false |
| Allarme4 | W34/ORef35 | 0626RID20 false |
| Allarme5 | W36/ORef37 | 0626RID20 false |
| Risposta | W42/ORef43 | RID25 미결속 |
| Comulativo_allarmi | W46/ORef47 | RID27 미결속 |

### 0359 CRef22

| 핀 | Wire/ORef | 선언상태 |
| --- | --- | --- |
| Ingresso_run | W37/ORef24 | RID712 미결속 |
| Allarme1 | W39/ORef26 | RID44 미결속 |
| Allarme2 | W40/ORef27 | 0626RID48 FALSE |
| Allarme3 | W41/ORef28 | 0626RID20 false |
| Allarme4 | W42/ORef29 | 0626RID20 false |
| Allarme5 | W43/ORef30 | 0626RID20 false |
| Risposta | W46/ORef33 | RID37 미결속 |
| Comulativo_allarmi | W48/ORef35 | RID39 미결속 |

## 부록 C 고정 원본 SHA-256 91개

커밋 abcf31c5030bc7ef8749ed8e869a857f2387a28a의원본을읽어계산했다. 백업ZAP18/PLF는보존기준이며TIA복원/실행·현재CPU일치증거가아니다. 파일해시와기능검증을구분한다.

| 전체원본경로 | SHA-256 |
| --- | --- |
| [AGENTS.md](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/AGENTS.md) | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 |
| [.agents/skills/gme-equipment-rollout/SKILL.md](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/.agents/skills/gme-equipment-rollout/SKILL.md) | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b |
| [docs/equipment-standard/WORK-STANDARD.md](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/docs/equipment-standard/WORK-STANDARD.md) | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 |
| [docs/equipment-standard/WORK-ITEM-TEMPLATE.md](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/docs/equipment-standard/WORK-ITEM-TEMPLATE.md) | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 |
| [docs/equipment-standard/INVENTORY.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/docs/equipment-standard/INVENTORY.json) | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc |
| [VERSION.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/VERSION.json) | 5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7 |
| [all-in-one/sources/Electrical_Rev2.pdf](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/Electrical_Rev2.pdf) | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| [all-in-one/sources/Electrical_Can_Decoating_20241118.pdf](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/Electrical_Can_Decoating_20241118.pdf) | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| [all-in-one/sources/PID_1684n002I.pdf](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/PID_1684n002I.pdf) | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| [all-in-one/sources/GME_20250506.zap18](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/GME_20250506.zap18) | 00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8 |
| [all-in-one/sources/PEData.plf](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/PEData.plf) | 647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a |
| [all-in-one/sources/source-manifest.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/source-manifest.json) | 5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf |
| [all-in-one/sources/live_index.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/live_index.json) | 14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1 |
| [all-in-one/sources/hmi_plc_tags.csv](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/hmi_plc_tags.csv) | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
| [all-in-one/sources/hmi-windows.csv](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/hmi-windows.csv) | 15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e |
| [all-in-one/sources/decoded-original/network-map.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/network-map.json) | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 |
| [all-in-one/sources/decoded-original/0014-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0014-FlgNet.xml) | 2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30 |
| [all-in-one/sources/decoded-original/0030-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0030-FlgNet.xml) | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b |
| [all-in-one/sources/decoded-original/0164-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0164-FlgNet.xml) | 15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491 |
| [all-in-one/sources/decoded-original/0165-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0165-FlgNet.xml) | 4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88 |
| [all-in-one/sources/decoded-original/0166-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0166-FlgNet.xml) | 0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853 |
| [all-in-one/sources/decoded-original/0238-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0238-FlgNet.xml) | 8f6a5537084e092c352552dc469bbe8469b33412971219e51bba211ef607dfa8 |
| [all-in-one/sources/decoded-original/0239-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0239-FlgNet.xml) | dffeeb46b691879c647fefa334674c6e101595c06fab071bc00836fc8f712599 |
| [all-in-one/sources/decoded-original/0240-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0240-FlgNet.xml) | bc1f120c4121b45913d542a0b6dd1ac4801422997fc0cbf3717d50d576932d33 |
| [all-in-one/sources/decoded-original/0243-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0243-FlgNet.xml) | 4b3a77029b4d5901ff40f260d54189748e7697bb6077fca502165fa7cd5ea3b5 |
| [all-in-one/sources/decoded-original/0244-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0244-FlgNet.xml) | 6df4651ea703181e0355fd70339bc3854bd5ef79826eaf3738c6d0acf1d0488f |
| [all-in-one/sources/decoded-original/0245-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0245-FlgNet.xml) | c89543f2a25028652f425fc8979bae3cde56cdcf8022b81beaadd49ab568abb6 |
| [all-in-one/sources/decoded-original/0275-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0275-FlgNet.xml) | 93aa2434583d4cf44f3b69f03db5717f38ac1da8f07b9e4b166c56daca8c3b74 |
| [all-in-one/sources/decoded-original/0291-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0291-FlgNet.xml) | fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550 |
| [all-in-one/sources/decoded-original/0309-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0309-FlgNet.xml) | a7f64a579271b0591d4d5c598221572384dce6eaac4587629447e4ad0f890180 |
| [all-in-one/sources/decoded-original/0310-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0310-FlgNet.xml) | c9f5daacd865ba3757ba2621250c8240659c98dc30d38c012ca72e608b613e5f |
| [all-in-one/sources/decoded-original/0336-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0336-FlgNet.xml) | 1be4f76dba11e6cceea057743c8b15b8a4bea4edfe87c19ef0581d7b65ffe56a |
| [all-in-one/sources/decoded-original/0358-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0358-FlgNet.xml) | 88fe3906653438753a9cefc82b7b1b2751a5d28027ebc778990d81f6a70b4daf |
| [all-in-one/sources/decoded-original/0359-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0359-FlgNet.xml) | eb4aae8bb8ef4e805f42c7ba320ad5f2f1b0a442c1f949a5ef161e4dcc1e1dec |
| [all-in-one/sources/decoded-original/0396-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0396-FlgNet.xml) | d8b31e69c920b6ab31c66318461d49cc227f8149b7f3589f8043664bcfe30142 |
| [all-in-one/sources/decoded-original/0397-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0397-FlgNet.xml) | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 |
| [all-in-one/sources/decoded-original/0398-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0398-FlgNet.xml) | 4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747 |
| [all-in-one/sources/decoded-original/0424-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0424-FlgNet.xml) | 645803f1cc7055adb3996e23788d6648330c992131dc34213c545d2fba184158 |
| [all-in-one/sources/decoded-original/0425-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0425-FlgNet.xml) | 9db302ef56730d0219869c9a9e1a38d0a8d0378a1f84cb94472f0f453ca0401c |
| [all-in-one/sources/decoded-original/0465-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0465-FlgNet.xml) | 6f48f2b9fc031e4dcef47cff8c9b56e2fbe67fd1802aac999b95836dd9a7458a |
| [all-in-one/sources/decoded-original/0519-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0519-FlgNet.xml) | 94c35aac42f54a7b8e4bcb8b8c88d59118e003f483cc49fb447854c682508fa9 |
| [all-in-one/sources/decoded-original/0058-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0058-IdentXmlPart.xml) | 84db55242df6a85df73776bfd23bf16cc10e4da35fedca4942f4a43bc4cd1702 |
| [all-in-one/sources/decoded-original/0059-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0059-IdentXmlPart.xml) | f02ef8f08f1c7ca7625bdbcf90a2c9365f12654d19e2e526fe8e5b0b742263d0 |
| [all-in-one/sources/decoded-original/0063-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0063-IdentXmlPart.xml) | 9dceae18963ead11293cfc3a70c2eac077faa53ebd28e23bb4e84bc3278c5034 |
| [all-in-one/sources/decoded-original/0555-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0555-IdentXmlPart.xml) | 46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6 |
| [all-in-one/sources/decoded-original/0575-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0575-IdentXmlPart.xml) | 40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06 |
| [all-in-one/sources/decoded-original/0576-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0576-IdentXmlPart.xml) | c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe |
| [all-in-one/sources/decoded-original/0577-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0577-IdentXmlPart.xml) | 511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47 |
| [all-in-one/sources/decoded-original/0578-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0578-IdentXmlPart.xml) | 0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b |
| [all-in-one/sources/decoded-original/0602-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0602-IdentXmlPart.xml) | 46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf |
| [all-in-one/sources/decoded-original/0603-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0603-IdentXmlPart.xml) | e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8 |
| [all-in-one/sources/decoded-original/0604-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0604-IdentXmlPart.xml) | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af |
| [all-in-one/sources/decoded-original/0605-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0605-IdentXmlPart.xml) | 0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b |
| [all-in-one/sources/decoded-original/0606-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0606-IdentXmlPart.xml) | 73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740 |
| [all-in-one/sources/decoded-original/0611-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0611-IdentXmlPart.xml) | 0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089 |
| [all-in-one/sources/decoded-original/0612-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0612-IdentXmlPart.xml) | 95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38 |
| [all-in-one/sources/decoded-original/0613-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0613-IdentXmlPart.xml) | 09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb |
| [all-in-one/sources/decoded-original/0614-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0614-IdentXmlPart.xml) | c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294 |
| [all-in-one/sources/decoded-original/0615-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0615-IdentXmlPart.xml) | 80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a |
| [all-in-one/sources/decoded-original/0616-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0616-IdentXmlPart.xml) | 650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d |
| [all-in-one/sources/decoded-original/0623-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0623-IdentXmlPart.xml) | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 |
| [all-in-one/sources/decoded-original/0624-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0624-IdentXmlPart.xml) | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a |
| [all-in-one/sources/decoded-original/0626-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0626-IdentXmlPart.xml) | a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b |
| [all-in-one/sources/decoded-original/0627-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0627-IdentXmlPart.xml) | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| [all-in-one/sources/decoded-original/0628-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0628-IdentXmlPart.xml) | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd |
| [all-in-one/sources/decoded-original/0629-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0629-IdentXmlPart.xml) | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| [all-in-one/sources/decoded-original/0635-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0635-IdentXmlPart.xml) | 1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457 |
| [all-in-one/sources/decoded-original/0642-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0642-IdentXmlPart.xml) | c922483c261c8ddb98c239a7b4dc3d7f73f9a45261dd5b4d669f39d6918a1c21 |
| [all-in-one/sources/decoded-original/0655-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0655-IdentXmlPart.xml) | 38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb |
| [all-in-one/sources/decoded-original/0656-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0656-IdentXmlPart.xml) | 0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592 |
| [all-in-one/sources/decoded-original/0657-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0657-IdentXmlPart.xml) | 0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b |
| [all-in-one/sources/decoded-original/0658-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0658-IdentXmlPart.xml) | 998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831 |
| [all-in-one/sources/decoded-original/0660-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0660-IdentXmlPart.xml) | 0bf4f4c46531f55324602f4f7b1a1e0b9e63df2c6278126f6e5cf1bc9a06509f |
| [all-in-one/sources/decoded-original/0661-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0661-IdentXmlPart.xml) | 90672199fee355011f581d3287046894772f3f3b4cb78bbe0dd0d71bd488ac93 |
| [all-in-one/sources/decoded-original/0662-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0662-IdentXmlPart.xml) | 1838040bfee800fdb3f13b126eaf69a9d178b17cecc0d59ae03e9185216a48a5 |
| [all-in-one/sources/decoded-original/0664-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0664-IdentXmlPart.xml) | 68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed |
| [all-in-one/sources/decoded-original/0672-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0672-IdentXmlPart.xml) | 6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222 |
| [all-in-one/sources/decoded-original/0674-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0674-IdentXmlPart.xml) | 4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84 |
| [all-in-one/sources/decoded-original/0676-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0676-IdentXmlPart.xml) | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 |
| [all-in-one/sources/decoded-original/0678-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0678-IdentXmlPart.xml) | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 |
| [all-in-one/sources/decoded-original/0680-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0680-IdentXmlPart.xml) | fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95 |
| [all-in-one/sources/decoded-original/0690-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0690-IdentXmlPart.xml) | fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541 |
| [all-in-one/sources/decoded-original/0691-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0691-IdentXmlPart.xml) | 17cb7d9734d76b39e729e0daf0c89d9bdf74907aab2130c80453fa04e4cea1da |
| [all-in-one/sources/decoded-original/0692-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0692-IdentXmlPart.xml) | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| [all-in-one/devices/RD01.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/devices/RD01.html) | f3e41c574af35e127a5584ef63e740d79d76f322dd19f902309496ed05a1e1bb |
| [all-in-one/control-specs/RD01.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/control-specs/RD01.html) | 864e9d6ed00c4c05e5ced6ac0a20b74c3c95dac9d536b3a2c68c1cf24ecec050 |
| [all-in-one/alarm-guides/RD01.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/alarm-guides/RD01.html) | d65630ef09c5cbfd073801661f2a9e4570bbfa7c2242aa49be22ebec44606634 |
| [all-in-one/circuit-guides/RD01.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/circuit-guides/RD01.html) | 83f7206c0e8fc30d271b1fe501fffd062abe9788ae925fa804203ff34524b9ea |
| [all-in-one/signal-guides/RD01.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/signal-guides/RD01.html) | 4a713ef1319048926cc168c337501813193c0fcc54f0dba655a1f9d9af6f63da |
| [all-in-one/construction-guides/RD01.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/construction-guides/RD01.html) | 3a3e05e01ae3249d8ced0a191ca8e7df8e2ef257e79a701125cb875bb2fa25d7 |
| [all-in-one/procedures/RD01.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/procedures/RD01.html) | bb919a00de6c3cd4016cc73dc6e29b98c596992cadd1e6eef132ee8d514ba018 |

## 부록 D 수행·보존

공개고정원본읽기,XML정적파싱·선언/Part/Wire/ORef대조,PDF지정페이지렌더·시각확인,자체MD작성과SHA-256계산을수행했다. 원본worktree는읽기전용으로유지하고git status로변경유무를확인한다. 프로젝트생성기·앱시험·시뮬레이터·TIA·실제PLC·현장·보호값·게시작업은수행하지않았다. 현장복구·현재정상극성·설비동일성의빈칸을추정으로채우지않았다.

