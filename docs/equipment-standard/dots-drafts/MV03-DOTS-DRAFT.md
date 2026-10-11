# MV03 P20 고유 제어 근거와 설비 문서 초안

- 산출물: **MV03-DOTS-DRAFT.md / 1차 독립 통합 검토용**, 2026-10-11 KST.
- Dots 자체 환경에서 직접 조사·작성했다. MV03(P20) 한 개가 대상이며, 사용자가 유일한 로컬 편집·검증·게시 담당이다.
- 기준: 공개 esp6662266/gme-plc-manual main/all-in-one, 고정 **c14bfd125a06e5d90bc1732c1cef5cd19ff1895b / v1.11.1**. 조사 시작점이며 MV03 게시 버전이 아니다. 직전89570f7 대비 sources 바이트 변경은 없었다.
- GME-STD-1.0.0, 저장소 AGENTS·gme-equipment-rollout SKILL·WORK-STANDARD·WORK-ITEM-TEMPLATE·INVENTORY의 7영역/근거 추적/완료 분리를 적용했다. 제공 환경에서 tia-equipment-alarm-trace 로컬 스킬은 확보하지 못했다. 권한을 확장하지 않고 공개 표준, XML 원본, PDF 실제 페이지 렌더를 대조했다.
- 원본·기존 완료 자료·미확정·이전 초안을 보존했다. 공통 코드·버전·대장·배포·운영 기록은 편집하지 않았다. 새 Work/Codex 작업 생성·조사 재위임, 시뮬레이터 작성·수정·생성·실행·행동시험, 실제 PLC·현장·보호값·별도 SEJIN 프로그램 변경은 없다.
- 현재 CPU·실물·정상 극성·현행 보호 설정·현장 복구는 미확정이다. 문서 정적 대조와 UI/기록/배포/TIA/현장 검증을 구분한다.

## 핵심 검토 요약

1. **MV03 응답 감시는 S5T#150S, Tag94=T3**다. 150ms가 아니다. 현재 CPU 설정·의도·적절성은 미확정이며 인접 밸브 값으로 고치지 않는다. [E09]
2. 명령 누적은 **W29/W30, >3400 / <−3400**이다. 엔코더 실측·각도·시간이 아니며 같은 MV03_FAULT를 Set한다. [E10,E11]
3. I7.5/I7.6은 Word 복사와 별도로 **NOT 연산 후 Inputs.DB13 X7.5/X7.6에 쓴다**. 처리 Inputs를 raw 값과 같은 극성으로 설명하면 안 된다. [E03,E04]
4. 최종 출력0345에는 반대 Q를 읽는 소프트웨어 차단 접점이 보이지 않는다. FG38의 상대 접촉기 NC31/32는 확인되지만 이를 XML에 있다고 쓰지 않는다. [E06,E21]
5. PSH03 오차 제어0344와 “not used” 제목의 CONT_S0479가 **같은 M14.4/M14.5에 쓰는 선언**을 갖는다. OFF 접점·현재 호출·실행 순서를 확인하지 않고 한쪽만 유일 제어자로 확정하지 않는다. [E05,E15]
6. 세정 열림과 버너 기동 닫힘은 별도 소유 블록의 요청이다. 버너0184에는 동일 처리 Close의 NOT/정접점 직렬 가지, State5의 Close OR ON이 실제로 있다. 이를 정상 순서로 임의 교정하지 않는다. [E16]
7. **P&ID M17=0.25kW 440V, FG38 M17=2.2kW 4.31A**로 상충한다. 명판 없이 현재 모터/보호값을 확정하지 않는다. [E02,E20]
8. OEM FG75는 “OUTPUT MV-03” 아래 PSH02/PEW286, PLC0344/0497은 PSH03/PIW320을 사용한다. 센서 태그·물리 소유·제어 원천의 문서 상충을 보존한다. [E17,E24]

## 1 설비와 자료 기준

### 1.1 식별과 소유

P20→MV03은 태그 대응이며 identity_verified=false다. 모터 구동 밸브/motorvalve, parent_id=null, phase1이다. 실물 동일성 완료를 뜻하지 않는다. 대장 주석도 “댐퍼 본체와 구동모터 관계 확인”으로 남아 있다. [E01]

P&ID PDF1에서 MV-03은 Overflow valve로 표시되고 M17, LS19/20, ZT04가 연결된다. 버너/HE01 관련 유로와 인접하지만 해당 공정의 모든 센서·모터·세정 장치를 MV03 소유로 묶지 않는다. 시공 FLO1TB1은 LS15/16/19/20 등이 경유하는 공유함이다. [E02,E25]

### 1.2 보존할 기존 자료와 정정 후보

기존 devices/control-specs/alarm-guides/circuit-guides/signal-guides/construction-guides/procedures의 MV03.html을 보존한다. 기존 circuit-guide의 “원본1706 모드·반대 출력·리미트…”라는 서술은 **0345 실제 XML에 반대 Q 접점이 없다는 이번 확인과 구분하여 통합자가 검토할 정정 후보**다. 파일 자체는 수정하지 않았다. 기존 압력명·백업주소·센서소유 미확정은 유지한다. [E06,E26]

공유 allarms2·valve control loop 네트워크에 다른 댐퍼가 포함돼도 MV03 항목/타이머/용량으로 복제하지 않는다. 문서의 항목 수를 앞선 MV01 등에 맞추지 않는다.

### 1.3 근거 읽는 법

네 자리 Flg 번호는 all-in-one/sources/decoded-original/NNNN-FlgNet.xml, Ident는 같은 폴더의 NNNN-IdentXmlPart.xml이다. LAD는 network-map.json document_id, NID는 원본 선언 네트워크 식별자다. Part UID, Wire UID, ORef UID, 선언 RID를 서로 바꿔 쓰지 않는다. 같은 RID/UID라도 블록·NID·자료형·주소·핀 연결이 다르면 다른 후보다. 예:0344 ORef296은0617 RID34 Tag148의NID3 접점이며 다른 블록의 GlobalAccess 후보를 배제했다.

## 2 태그·I/O·HMI

### 2.1 물리 주소와 처리 층

| 항목 | 백업 근거 | 처리 층/도면 끝점 |
| --- | --- | --- |
| 열림 명령 Q1.7 | 0617 RID47 Start open MV03,Output AO15;0345 ORef428 Write | FG137 MOD14단자18 A1.7→FG38 38KM1 coil |
| 닫힘 명령 Q2.0 | 0617 RID48 Start Close MV03,Output AO16;0345 ORef438 Write | FG138 MOD14단자21 A2.0→38KM2 coil |
| 열림 접촉기 응답 I2.4 | live_index _7ev doc883 mv03_fbk_opening Bool | 0573 RID63 Inputs.MV03 Run_Opening AO20=DB13.X2.4;FG118 MOD8단자25 |
| 닫힘 접촉기 응답 I2.5 | live_index doc884 mv03_fbk_closing Bool | 0573 RID64 Inputs.MV03 Run_Closing AO21=DB13.X2.5;FG118단자26 |
| 열림 끝단 I7.5 | 0627 RID152 MV03_Open,Input AO61 | 0629 RID153 Inputs.MV03 open AO61=DB13.X7.5;**NOT 쓰기**;LS19→FG123단자36 |
| 닫힘 끝단 I7.6 | 0627 RID154 MV03_Close,Input AO62 | 0629 RID155 Inputs.MV03 Close AO62=DB13.X7.6;**NOT 쓰기**;LS20→FG123단자37 |

접촉기 응답 원시 태그 두 개는 색인·도면을 확인했으나 동일 이름 SimpleAccess 선언은 이번 참조에서 직접 결속하지 못했다. 처리 DB 선언을 원시 심볼 선언인 것처럼 표시하지 않는다. 주소는 백업/도면 기준이며 현재 배선·정상극성·CPU일치가 아니다. [E03]

### 2.2 raw→Inputs 복사·반전과 호출

LAD1070 0397 NID1: [E04]

- IW2→DB13.DBW2:Move27.in W31/ORef28(0627 RID8 Tag179 Input Word AO16),out1 W32/ORef29(0629 RID9 AO16 BAD4).0628 RID4 Inputs TOD13. 이 Word에 I2.4/I2.5가 포함된다.
- **열림 반전**:Contact127 raw MV03_Open,operand W122/ORef132→W137 Not142.in→W145 Coil147→W146/ORef148 Inputs.MV03 open.
- **닫힘 반전**:Contact149 raw MV03_Close,operand W155/ORef152→W156 Not150.in→W157 Coil151→W158/ORef153 Inputs.MV03 Close.
- Word 복사에 같은 바이트가 포함되더라도 위 개별 쓰기를 누락하면 안 된다. 전체 현재 호출/쓰기가 동일한지는 미확정이다.
- main LAD1613 0030 NID19:recipes handler→hmi→hmi output의 ENO(W32/33/42) 뒤 NOT Simulation(1) Contact37(W44/ORef45)→W43 hmi inputs CRef28.0692 RID140 Memory AO1440=M180.0. 이 호출 경계를 포함한 정적 사실만 확인했고 가상 실행은 하지 않았다.

NC 센서 도면과 소프트웨어 NOT는 각각의 증거다. 현장 캠·배선·위치별 값 없이 “정상은 무조건0/1”이라고 정하지 않는다.

### 2.3 주요 내부 변수

DB 번호는0618/0674의 DepDBBlock TOD로 확인한다:Flag2,Allarm3,Data1,WorkData6,HMI_DB41,Inputs13,Coeff4,Memory encoder8,fill_unit1 91.

| 이름 | 주소/선언 | 용도·경계 |
| --- | --- | --- |
| Flag.M_MV03_OPEN / CLOSE | DB2.X9.7 / X10.0;0619 RID43/41 AO79/80 | 수동 요청;HMI 실제 쓰기 이벤트 미확정 |
| Flag.MV03_Auto | DB2.X7.0;0619 RID42 AO56 | startup Set,자동 분기,CONT_S reset |
| Allarm.MV03_FAULT | DB3.X4.3;0619 RID45/0573 RID21 AO35 | 응답/명령누적 공통 래치 |
| Open MV03 for washing | M48.1;0617 RID46/0582 RID101 AO385 | 버너 블록 소유 Set/Reset 요청 |
| Close MV03 for Burner Startup | M180.5;0617 RID187/0582 RID238 AO1445 | 버너 Set,밸브 제어 Reset |
| PID UP / down MV03 | M14.4/M14.5;0617 RID39/37 AO116/117;0670 RID106/107 | 두 제어 경로의 쓰기 대상 |
| ResetEncoderProcedure_MV03 | DB41.X50.6;0619 RID191 AO406 | 구동 요청에도 영향 |
| WorkData.W29 / W30 | DB6.DBW58/DBW60;0619 RID121/123 AO464/480 | 방향 명령 누적,엔코더와 별도 |
| Data.PSH03_SETPOINT / PSH03 | DB1.DBW40/DBW24;0619 RID29/30 AO320/192 | 압력 비교 입력;현재값/단위 미확정 |
| ErrPSH03 | local Int;0062 RID31,NID3 UID289 Write | SETPOINT−PSH03 결과;전역 주소를 만들지 않음 |
| Data.Pot_MV03 | DB1.DBW144 Int;0676 RID234 AO1152 | 엔코더 환산값,현행 교정 미확정 |
| Allarm.Pot_MV03_OFR | DB3.X25.0;0676 RID436 AO200 | 위치 선형화 범위 알람 |
| Allarm.PSH03_OFR | DB3.X22.2;0676 RID389 AO178 | 압력 선형화 범위 알람;MV03 자체고장과 별개 |
| ZERO_TRASM_MV03 / COEFF_TRASM_MV03 | DB4.DBW200/202;0676 RID233/232 AO1600/1616 | 현재값·설정 의도 미확정 |
| Encoder_CH02 / Encoder_CH02_10 | DB8.DBD8/DBW40;0676 RID198/242 AO64/320 | DInt 누적/Int 환산,이름과실제/100연산 구분 |
| MV03_Encoder | DB17;0618 RID192/0673 RID340 TOD17 | HSC instance;내부 S/IO offset를고정절대주소로단정금지 |

### 2.4 HMI 주소와 미결속 호출

hmi_plc_tags.csv의 MV03 전용9행은 dde.cfg 설정이며 온라인현재값이 아니다. [E18]

| 태그 | 설정주소 | ID |
| --- | --- | --- |
| RESET_ENC_MV03 | DB41,X50.6 | 00465 |
| MV_03\LimitSwitchClose | DB11,X22.4 | 0031B |
| MV_03\Flag_OPEN | DB2,X9.7 | 0031A |
| MV_03\Flag_CLOSE | DB2,X10.0 | 00319 |
| MV_03\Allarme1 | DB11,X22.2 | 00318 |
| MV_03\AutoMan | DB2,X7.0 | 0030D |
| MV_03\OutputOpen | DB11,X22.0 | 0030C |
| MV_03\OutputClose | DB11,X22.1 | 001A2 |
| MV_03\LimitSwitchOpen | DB11,X22.3 | 00043 |

연관 I_PSH_03=DB13,INT52(ID00056)는 별도 입력 표시 태그이며 Data.PSH03 DB1.DBW24와 구분한다.

LAD1191 0369 CRef22/CodeBlock23=HMI Standard Motorized Valve(0624 RID639/0623 RID130). NID는복수후보11/12/13/16에서단일확정못했다. Allarme2/3/4/5는 W50~53/ORef27~30,0626 RID48(FALSE)/20(false)로 일관되지만,아래10개는선언미결속이다.

| 핀 | Wire/ORef/RID | 색인 후보,확정 아님 |
| --- | --- | --- |
| Ingresso_run_Opening / Closing | W47/24/681,W48/25/688 | Inputs.MV03 Run_Opening/Closing |
| Allarme1 | W49/26/444 | Allarm.MV03_FAULT |
| Limit_switch_Open / Limiti_Switch_Close | W56/33/687,W57/34/686 | Inputs.MV03 위치 |
| Risposta_Opening / Closing | W62/39/449,W63/40/450 | Motors.MV03 응답 |
| Limit_Switch_Open_HMI / Close_HMI | W64/41/451,W65/42/452 | Motors.MV03 한계 |
| Comulativo_allarmi | W68/45/455 | Motors.MV03 집계 |

DB11 HMI OutputOpen을 Q1.7 자체로,DB11 Allarme1을 DB3 fault와 같은주소로 표시하지 않는다. 원본 핀 철자는 추적용으로 유지한다.

## 3 고유 제어·구동·소유

### 3.1 PSH03 오차 제어

LAD1705 0344 NID3:ON328(W303/ORef286)→W329에서 Sub256과 타이머 가지로 분기한다. Sub.in1 W304/ORef287=Data.PSH03_SETPOINT,in2 W305/ORef288=Data.PSH03,out W306/ORef289=local ErrPSH03 Int. [E05]

- NOT Tag147 Contact330(W308/ORef291)→W331 SD263 Tag148(W310/ORef292),value W307/ORef290=**S5T#4S**(0620 RID33).
- Tag148 Contact332(W312/ORef294)→W333 SD268 Tag147(W314/ORef295),value W311/ORef293=**S5T#10S**(0620 RID35).
- NOT Tag148 Contact334(W315/ORef296)→W335 두 비교의pre.
- ErrPSH03 **≥5**:Ge276 W316/ORef297, W317/ORef298(0620 RID185)→W318 Coil279→W320/ORef299 PID down MV03 M14.5.
- ErrPSH03 **<−5**:Lt282 W321/ORef300,W322/ORef301(0620 RID186)→W323 Coil285→W325/ORef302 PID UP MV03 M14.4.
- Tag147=T138(0617 RID32),Tag148=T139(RID34). 정확한 비교는≥5와<−5로 비대칭이며 ±5의 닫힌 deadband라고 바꿔 쓰지 않는다.

이름PID인 두 비트를 만드는 실제 경로는 위 오차·타이머·비교 사슬이다. 현재 압력단위,4초/10초의 실제 구동시간,스캔/호출주기를 단정하지 않는다.

### 3.2 최종 출력: 자동·수동·세정·기동·교정

LAD1706 0345 NID4. 기호 A=Auto,U/D=PID UP/down,O/C=수동열림/닫힘,W=Open for washing,B=Close for Burner Startup,R=ResetEncoderProcedure,P=MV WORK PULSE,F=MV03_FAULT,Lo/Lc=처리 Inputs 위치. [E06]

- 열림 Q1.7: ON AND NOT F AND (((A AND U) AND (P OR ON)) OR (O AND (P OR ON)) OR W) AND NOT R AND NOT Lo.
- 닫힘 Q2.0: ON AND NOT F AND (((((A AND D) AND (P OR ON)) OR (C AND (P OR ON)) OR B) AND NOT W) OR R) AND NOT Lc.

| 분기 | 실제 Part/Wire/ORef |
| --- | --- |
| 공통 | ON489 W439/408→W490→NOT F505 W454/418→W506 |
| 열림 자동 | Auto507 W455/419→UP509 W456/420→Pulse511 W457/421 OR ON513 W458/422→OR543.in1/2 |
| 열림 수동 | Open515 W461/423→Pulse517 W462/424 OR ON519 W463/425→OR543.in3/4 |
| 세정 열림 | Washing521 W466/426→W522 OR543.in5 |
| 열림 최종 | OR543 W27→NOT R44 W39/45→W47→NOT Lo523 W29/30→W28 Coil390→W470/428 |
| 닫힘 자동/수동 | Auto525→Down527→Pulse529/ON531→OR544.in1/2;Close533→Pulse535/ON537→in3/4 |
| 기동 닫힘 | B36 W35/37→W38 OR544.in5 |
| 세정 차단/교정 | OR544 W482→NOT W539 W483/436→W31 OR53.in1;R546 W51/52→W54 OR53.in2 |
| 닫힘 최종 | OR53 W55→NOT Lc541 W33/34→W32 Coil407→W486/438 |

**이XML 최종경로에는 NOT 상대Q 접점이 없다.** FG38 상대접촉기NC 인터록과구분한다. 출력요청동시성·실제접촉기우선순위/안전은 현재프로그램·현장검증없이완료하지않는다. R닫힘가지는NOT W 이후의OR에합류하므로 교정요청이있으면세정닫힘차단을그가지에는적용하지않는구조다. 이것은조작권고가아니다.

ON은심볼M0.0,OFF는M0.1이다. P OR ON 때문에공유펄스만이출력의필수허가라고할수없다. 공유작업펄스0350은Tag155 T79=200ms/Tag154 T78=2s 사슬이지만 MV03의필수운전주기로복제하지않는다.

### 3.3 요청 Reset와 startup

0345의 ON489→ON491 아래:

- Lo493 OR Close495 OR Auto497→OR358→R362 Open요청(W446/ORef413).
- Lc499 OR Open501 OR Auto503→OR365→R369 Close요청(W452/ORef417).
- Lc42(W41/ORef43)→W48 R46→W49/ORef50 기동닫힘B를Reset.
이들은알람Reset과다르다. 수동요청생성·외부쓰기·스캔우선순위는미확정이다.

startup LAD404 0149 NID4의ON337→W338→SCoil300,대상Flag.MV03_Auto W329/ORef318(0563 RID44 AO56). 현재Auto나전원복구후실제동작은확인하지않았다. [E07]

### 3.4 엔코더 교정 요청

LAD1707 0353 NID13:ResetProc22(W25/ORef23)→InputsClose26(W29/ORef30)→W33 Move32.en;in W34/ORef36=0,out1 W35/ORef37=MV03_Encoder.NewCountValue(0619 RID193). eno W38→NOT SetCountValue40(W39/ORef41)→W42 Coil44(W43/ORef45,0619 RID195)→W50 R48 ResetProc(W51/ORef52). [E08]

DB17 내부NewCountValue(S=S AO320)·SetCountValue(S=IO AO288)는별도멤버다. HSC 호출의SetCountValue 핀에는RefId가없으므로이멤버와실제핀을이름만으로결속하지않는다. 구동영향·요청해제·하드웨어제로설정·현장기준점완료는서로다르다.

### 3.5 엔코더 읽기·누적·환산·다른쓰기

LAD1758 0508 NID47:NOT Simulation(1)75(W74/ORef76,0678 RID344 M180.0)→W77 EM_OK21(W49/ORef24,RID173 I19.4)→W50 LRef22 High_Speed_Counter(0679 RID330),Instance23 MV03_Encoder(0673 RID340 DB17). [E12]

SwGate W51/ORef25=fill_unit1.CONTROL_SIGNALS.SW_GATE2(0676 RID236);CountValue W71/ORef45=fill_unit1.ACT_CNTV2(RID238,DInt). **나머지21핀은ORef에RefId가없다.** ErrorAck/EventAck도미결속이며공통Reset에연결됐다고앞설비에서복사하지않는다. 부록핀표참조.

LAD1764 0514 NID32:EM_OK1217(W1191/ORef1168)→W1218에서다음으로분기한다. [E13]

- NOT **처리 Inputs.MV03 Close** Contact1219(W21/ORef22,0676 RID446)→W1220 Coil1129 SW_GATE2(W1193/ORef1170)와Add1134.en. raw I7.6가아니라이미반전된DB13비트다.
- Add1134:Encoder_CH02(W1194/ORef1171)+ACT_CNTV2(W1195/ORef1172)→local CNT_Act_2(W1196/ORef1173). eno W1197→Div1138:local W1198/ORef1174 /100 W1199/ORef1175→CNTV2_100 W1200/ORef1176.
- Div.eno W1201→Move1142:local W1202/ORef1177→Encoder_CH02_10 W1203/ORef1178. DInt계산값에서Int저장으로가는자료형경계를보존한다.
- NOT SW_GATE2 Contact1221(W1205/ORef1179)→W1222:Move1151 0→Encoder_CH02_10(W1206/1207),Move1156 INT#0→Encoder_CH02(W1208/1209).
- EM_OK공통→Signal linearization CRef1163:IN0 W1211/ORef1185=ON;Analog_input W1212/1186=CH02_10;Coeff W1213/1187,Zero W1214/1188;OutValue W1215/1189=Data.Pot_MV03;Out_of_range W24/23=Allarm.Pot_MV03_OFR.

추가쓰기 LAD1761 0511 NID30:NOT EM_OK Contact963(W951/ORef940)→W964 Move927.en;in W956/ORef945=local CNT_Act_2(0677 RID197),out W957/ORef946=Encoder_CH02(0676 RID198). 즉 EM_OK조건이반대인기억경로도있다. 로컬값수명·초기화·실행순서없이 “전원차단시정확한위치보존”으로확정하지않는다. [E14]

Signal linearization 본문0291/0014의확인범위:IN0 AND Analog_input>−1382 AND≤32767에서 Int→DInt 변환 후 (입력+Zero)×Coeff/28000,Int OutValue로전달한다. 범위밖이면Move193 −9999→OutValue,eno→일반Coil23 Out_of_range. NOT IN0는0014 Move162 0→OutValue. 0611/0612의자료형·정수연산·ENO사슬을보존하며실수비례식/실제센서규격으로일반화하지않는다. 위치OFR은별도S/R래치가아니다. [E19]

### 3.6 같은 UP/DOWN을 쓰는 CONT_S 경로

LAD15 0479 NID12 제목은 control pc02 moduling mv03 - not used다. 그러나LRef507 CONT_S(0671 RID113),Instance546 PID_MV03(0665 RID104 DB25)와M14.4/M14.5 출력선언은존재한다. [E15]

- en:OFF583 W547/ORef529→W584. OFF심볼이현재0이라는실행증거는없다.
- COM_RST:NOT Auto585 W548/530 OR Washing587 W549/531→OR498 W550.
- LMNR_HS=NOT InputsOpen589 W551/532→W590;LMNR_LS=NOT InputsClose591 W552/533→W592.
- CYCLE T#100MS W561/534;SP_INT localReal_SPPC02 W562/535;PV_IN localReal_PC02 W563/536.
- GAIN **−4.0** W566/537;TI **T#10S** W567/538;DEADB_W **2.0** W568/539;PULSE_TM **T#200MS** W573/540;BREAK_TM **T#5S** W574/541;MTR_TM **T#3S** W575/542;DISV **2.0** W576/543. 0667 RID105/58/22/25/27/26의 원본 값이다.
- QLMNUP W577/ORef544→M14.4,QLMNDN W578/ORef545→M14.5(0670 RID106/107 Write). 0344의Coil과같은주소다.
- 9핀은RefId없음:LMNS_ON W554/553,LMNUP W556/555,LMNDN W558/557,PVPER_ON W560/559,PV_PER W565/564,PV_FAC W570/569,PV_OFF W572/571,PV W580/579,ER W582/581.

“not used”제목은현재실행불가의증명도,코드삭제허가도아니다. SP/PV지역변수상류계산·현재DB25·OFF값·두블록호출순서·다른쓰기자료가필요하다. 여기에적힌설정은조정권고/현행보호값이아니다.

### 3.7 버너 세정·기동 요청의 소유와 상충

LAD1868 0184 NID14는 **burner control 소유**다. MV03출력의W/B요청과연결되는범위만추적했으며BR01전체설비초안을대신작성하지않았다. Enable start burner(1)=M48.0(0582 RID92),W=M48.1(RID101),B=M180.5(RID238);WorkData.BR01_State는RID100 AO176=DB6.DBW22,CleanTime은RID97 AO192=DB6.DBW24다. [E16]

| 경로 | 원본 Part/Wire | 해석·경계 |
| --- | --- | --- |
| 비허가 초기화 | ON1634→NOT Enable1636→W1637:Move1122 State0,R1127 W해제,R1130 Enable start burner해제 | 이름이비슷한Enable두변수구분;현재호출미확정 |
| 상충하는 B Set 가지 | 같은W1637→**NOT Close28**(W37/ORef38)→W29→**Close1670**(W33/ORef34)→W30 S1669 B(W25/ORef26) | 두접점모두0585 RID233 AO62=같은InputsClose. 정적동일값모델에서충족불가;임의수정/정상가지로서술금지 |
| State0 분기 | Eq1137→PID_Ref_Temp≥500.0이면Move1146 State7,<500.0이면Move1154 State1;Move1159 CleanTime0 | 관련버너설정,현재온도/안전허가아님 |
| State1 | Eq1164→S1176 W(W1509/ORef1390),Move1179 State2 | 세정열림요청발생 |
| State2 | Eq1184→**NOT InputsOpen1642** W23/ORef24→Move1188 State3 | “열림응답1을기다린다”라고역으로쓰지않음 |
| State3 | Eq1193→SD1199 Tag143 **S5T#4M**;Tag1431650→Move1220 State4 | T31;별도Tag142 T32 S5T#1S/증분CleanTime가지도존재. MV03응답타이머아님 |
| State4 | Eq1225→R1237 W(W1548/ORef1418),Move1240 State5 | W해제 |
| State5 | Eq1245→InputsClose1654 **OR ON1656**→OR1248→Move1251 State6 | Close하나가항상필수라고설명할수없음 |
| State6 | Eq1256→SD1262 Tag144 **S5T#1S**→Move1267 State7 | T37,관련순서타이머 |
| State7 | Eq1294→S1300 Enable,R1303 W(W1591/ORef1447),S1306 B(W1592/ORef1448),Move1309 State8 | B의유효한별도Set경로존재;앞상충가지가있어도B절대불발로단정금지 |
| 이후 관련 대기 | State8 BurnerOn후State9;SD1329 Tag145 **S5T#30S**후State10 | T38,버너순서소유. MV03보호시간으로복제금지 |

상태여러가지가같은네트워크에병렬로배치돼있다. 스캔내연쇄전이·호출순서를미검증한상태에서단계당한스캔/실시간순서를확정하지않는다. 버너승인·가스·연소보호의실제완전성은이번문서범위밖이다.

또한 정확한 Data.Pot_MV03 선언 검색에서 기존 백업의0635 RID314의 NID2 UID509/517 Write 참조가 존재한다. 이는 network-map LAD1083의 기존 simulation 블록 관련 다른 쓰기 후보이며 활성·실행으로 간주하지 않는다. 해당 원본 블록 또는 시뮬레이터를 작성·수정·실행·행동시험하지 않았다. 현재 프로그램의 간접주소/HMI/외부쓰기까지 완전한 목록이라고 주장하지 않는다.

### 3.8 압력 원천과 도면 상충

LAD1747 0497 NID17:ON495→W496 Signal linearization CRef476.en;IN0 W490/ORef483 ON,Analog_input W491/ORef484 **PSH03:P**(0678 RID106,SAD Input Peripherie AO2560=PIW320),Coeff W492/485(0676 RID449 AO1760),Zero W493/486(RID448 AO1744),OutValue W494/487 Data.PSH03(RID109),OFR W24/23 Allarm.PSH03_OFR(RID389). [E17]

즉0344의Data.PSH03는이원본경로와결속된다. 기존설명중PSH02/PIW286과섞이는부분은그대로확정하지않는다. PSH02는0678 RID101 AO2288=PIW286의별도입력이며FG75 “OUTPUT MV-03”라벨아래에그려져있다. FG75 오른쪽PSH03/PEW320가지에는다시“PRESSURE CONTROL PSH-02”제목이있다. 도면텍스트자체의불일치를기록하고어느센서가현재MV03압력을제어하는지명판/준공도/현재프로젝트없이는정하지않는다. Data.PSH03_SETPOINT 쓰기/현재값도미확보다.

## 4 전기도면 실제 페이지·끝점·판본

### 4.1 페이지별 개정란

Electrical_Rev2.pdf의인쇄FG/실제PDF(1부터)는다음과같다. 실제렌더에서확인했으며파일명Rev2를일괄적용하지않았다. [E20~E24]

| FG / PDF | 개정란 |
| --- | --- |
| 38/39,39/40,75/76,146/147 | 공란;기본날짜27.05.2024 |
| 108/109,118/119,123/124,137/138,138/139 | Rev2 17.03.2025 |

### 4.2 C1 동력/보호와 모터 상충

FG38/PDF39:440V60Hz 8.3L1/L2/L3→38QM1(인쇄범위3.5–5A)→38KM1/2 정역전력접점→38U1/38V1/38W1→XM동일단자→38QS1 1–2/3–4/5–6→M17 MV-03 U/V/W/PE. 도면모터표기는2.2kW4.31A다. [E20]

P&ID PDF1실제M17표기는0.25kW440V다. 어느하나를현재실물정격으로채택하지않는다. 3.5–5A를현행설정이나4.31A설정으로추정하지않고,실명판·현재보호설정·교체이력·승인근거를요구한다. 이번회로에인버터모델/속도파라미터를가져오지않는다.

### 4.3 C2 출력/코일과 하드웨어 상호 차단

- FG137/PDF138 MOD14단자18 A1.7→FG38/4→상대38KM2 NC31/32→38.1→38KM1 A1/A2.
- FG138/PDF139 MOD14단자21 A2.0→FG38/6→상대38KM1 NC31/32→38.2→38KM2 A1/A2.
- 두A2귀로38.3→38QM1보조접점→38.4→XS25→38QS1보조접점→XS26→−0Vdc10.6.
- 출력모듈공급은FG137 X21/3029 4AF 및FG138 X21/3030 4AF의각도면가지에표시된다. 실제퓨즈상태/현행교체규격은확인하지않았다.

NC31/32,응답보조13/14,코일A1/A2,하단접점표는서로구분한다. 하드웨어인터록확인을소프트웨어상대Q접점존재로전환하지않는다. 점퍼·강제출력·보호우회는제안하지않는다. [E21]

### 4.4 C3 접촉기 응답

FG38:+24Vdc10.7→38KM1 보조13/14→E2.4→FG118/PDF119 MOD8단자25. 닫힘은38KM2 보조13/14→E2.5→단자26. [E22]

이응답은접촉기상태이지모터실회전·밸브이동·한계도달증명이아니다. I2.4/2.5와LS19/20·ZT04를구분한다.

### 4.5 C4 한계센서

FG39/PDF40:+24Vdc10.7→X1/90 5×20 2AF→39.3→LS19 NC11/12→X1/91→E7.5→FG123/PDF124 MOD9단자36. 닫힘은X1/92 2AF→39.4→LS20 NC11/12→X1/93→E7.6→단자37. [E22]

PLC0397의별도NOT쓰기를같이참조한다. NC도면만으로현재단선반응/정상극성을확정하지않는다.

### 4.6 C5 ZT04 엔코더

FG39→FG146/PDF147 MOD17 TM1 TIMER:

| ZT04 | 중간 단자/선 | 끝점 |
| --- | --- | --- |
| B +24V | X1/85→35.1 | 단자9 24VDC |
| C 0V | X1/86→35.2 | 단자10 M |
| D | X1/87→39.1 | 단자1 CH0.A |
| E | X1/88→39.2 | 단자2 CH0.B |
| shield | X1/89→39SCH1 | 실드접지표시 |

CH0.N단자3의현장선은표시되지않았다. E21.0/21.1/21.2와A9.0/9.1 SPARE를카운트주소로추정하지않는다. **도면CH0와프로그램SW_GATE2/ACT_CNTV2의숫자가다르다고단순불일치판정하거나동일하드웨어채널로확정하지않는다.** 모듈별로컬채널명과소프트웨어자료구조의매핑설정이필요하다. [E23]

### 4.7 C6 압력 입력과 문서 소유 경계

FG75/PDF76 PSH03:+24Vdc10.7→X1/178 50mAF→75.3→PSH03 +;PSH03 −→X1/179→+PEW320→FG108/PDF109 MOD4단자2 I0+. X1/180→75SCH3실드. FG108단자4 U0−/I0−와18 MANA는−0V귀로표시다. 도면기기P-BADR,0/10mbar,4–20mA는설계표기이며현재계기범위/교정확인이아니다. [E24]

같은FG75의중앙PSH02는X1/175/176/177→PEW286,상단제목OUTPUT MV-03이다. PLC0344/0497 PSH03/PIW320과다르므로전선번호·센서명판·압력취출점·준공개정으로확인해야한다. 이름MV03만으로PSH02/03를동일센서또는MV03본체소유로확정하지않는다.

### 4.8 시공 도면

Electrical_Can_Decoating_20241118.pdf는24.11.11 FIRST DRAFT 시공설계다. 공개GME원본내자료를읽었으며별도SEJIN프로그램자료를복제하지않았다. [E25]

| 실제PDF/행 | 전체ID·FROM→TO | 표기 |
| --- | --- | --- |
| 51/1_9 | =FLA+MV03-M17A CR→MV03 M17 | GAC/CV4×1.5,spare0,100 LCD1→E100,LEN46 |
| 56/6_1 | =FLA+MV03-FLO1TB1A→MV03 FLO1TB1 | LS15/16/19/20 공유DC CVV12G1.0,spare3,LEN44 |
| 56/6_3 | =FLA+MV03-FLO1TB1C→ZT04 | TM CVV-S4S1.0,LEN42 |
| 56/6_11 | =FLA+HE01-PSH03A CR→HE01 PSH03 | AI CVV-S4S1.0,spare1,LEN48;태그HE01소유표기와제어사용구분 |
| 56/6_15 | =FLA+MV03-LS19A FLO1TB1→MV03 LS19 | DC CVV2C1.0,E1200,LEN5 |
| 56/6_16 | =FLA+MV03-LS20A FLO1TB1→MV03 LS20 | DC CVV2C1.0,E1300,LEN5 |
| 56/6_17 | =FLA+MV03-ZT04A FLO1TB1→MV03 ZT04 | TM CVV-S4S1.0,E1400,LEN6 |

LEN은설계길이,TM/AI는원문분류다. 가려진행6_7~6_10은배선근거에서제외했다. 공유함다른센서·다른밸브를MV03목록에추가하지않는다.

## 5 알람·타이머·별칭·복구

### 5.1 방향응답 감시:150초

LAD1226 0159 NID1:ON513→ON535(W448/ORef380)→두가지로분기. Qopen537(W449/ORef381)→NOT Inputs.RunOpening541(W452/ORef383)→W37 OR36.in1;Qclose539(W450/ORef382)→NOT Inputs.RunClosing34(W33/ORef35)→W38 OR36.in2. [E09]

OR36.out W542→SD281.in와Timer Contact543.in. SD281.value W453/ORef384=**S5T#150S**,0571 RID83의원본단위다. operand W454/ORef385=Tag94,0570 RID20 Timer AO3=T3. Contact543 operand W455/ORef386→W544 S286→W457/ORef387 Allarm.MV03_FAULT(0573 RID21 DB3.X4.3).

0571 LiteralConstant의 TD=S5Time,CB SV=S5T_x0023_150S,V=8528(0x2150)도 함께 보존한다. 원본설정은150초다. 실제검출시간·현행CPU·설정의도·안전적절성은판정하지않았다. 인접150MS에맞춰교정하거나타이머단축/보호값변경을권고하지않는다.

### 5.2 방향 명령 누적과 같은 래치

LAD1713 0351 NID11의공유Tag156 T118/Tag157 T119 S5T#10MS사슬→NOT Tag157→PBox1235(bit M50.7)→ON1659에서MV03분기. [E10]

- Qopen1661(W1574/ORef1478)→W1662 Add1316:W29 W1575/ORef1479 +1 W1576/ORef1480→W29 W1577/ORef1481;Move1322 0→W30 W1578/1579.
- Qclose1663(W1581/ORef1484)→W1664 Sub1331:W30 W1582/ORef1485 −1 W1583/ORef1486→W30 W1584/ORef1487;Move1337 0→W29 W1585/1586.
- 타이머를실제10ms주기보증·누적초환산으로사용하지않는다. 현재둘다Q가없을때매번누적0으로지운다는가지도이분기에서는확인하지못했다.

LAD1714 0352 NID12:ON1943→ON1949(W1878/ORef1801)→W1950 두비교. [E11]

| 비교 | 같은 MV03_FAULT Set | 누적값 Move0 |
| --- | --- | --- |
| W29>3400:Gt1656 W1879/1880,ORef1802/1803 | W1881→S1662→W1882/ORef1804 | Move1665 W1883/1884,ORef1805/1806 |
| W30<−3400:Lt1670 W1886/1887,ORef1807/1808 | W1888→S1676→W1889/ORef1809 | Move1679 W1890/1891,ORef1810/1811 |

0619 RID121/123 W29/W30,RID45는 같은 fault,0620 RID153=3400/RID155=−3400이다. 엄격 비교 >/<를 유지한다. 누적0은알람Reset·엔코더영점·기구복구완료가아니다.

### 5.3 Reset와 별도 알람층

0159:ON513→RESET_ALLARM575(W492/ORef412)→MV03_FAULT581(W499/ORef417)→W582 R350→W501/ORef418. 이Reset가지에는원인응답정상화직렬접점이별도로보이지않는다. Set/Reset의현재호출·다른쓰기·재발·재기동결과는미확정이다. [E09]

| 계층 | 이름/주소 | 해석 |
| --- | --- | --- |
| 공통고장래치 | MV03_FAULT DB3.X4.3 | 150초방향응답불일치,양방향누적초과가같은Set대상 |
| 위치범위 | Pot_MV03_OFR DB3.X25.0 | 0514 선형화출력;별도일반coil경로 |
| 압력범위 | PSH03_OFR DB3.X22.2 | 0497 선형화출력;사용센서연관알람이지MV03동력고장비트와같지않음 |
| HMI알람 | MV_03\Allarme1 DB11,X22.2 | 표시집계설정;Allarme1호출실인수선언미결속 |
| HSC진단 | Error/ErrorID 등 | RefId없는핀,가상의진단주소/알람번호를만들지않음 |

HMI DB11.X22.2와 PSH03_OFR DB3.X22.2는바이트/비트숫자가같아도**서로다른DB**다. 동일알람별칭으로합치지않는다. 오류최초시각·정확한DB/태그·명령방향·raw/Inputs/HMI층을구분해기록한다.

## 6 증상별 조사·수리 문서 초안

다음은관찰·근거대조용이다. 조작·강제출력·점퍼·보호설정변경·교정실행은포함하지않는다. 전기/구동부현장점검은자격있는담당자의승인된격리·안전절차를전제로한다.

| 증상 | 필요한 비교 증거 | 판단 경계 |
| --- | --- | --- |
| 자동만동작안함 | 0344 오차/Tag147·148,Auto,M14.4/14.5,0479 OFF/동일주소쓰기 | PSH명칭만으로센서소유/활성PID를정하지않음 |
| 한쪽요청만안됨 | 처리한계,세정W/기동B/교정R,요청Reset경로 | 열림/닫힘은완전대칭아님;상대Q접점을임의추가설명금지 |
| 양방향명령상충 | 두Q·두요청·W/B/R·현재쓰기,FG38상대NC | 하드웨어인터록만으로안전검증완료선언금지 |
| Q있고접촉기응답없음 | 상대NC31/32,coil,38QM1/38QS1공통귀로,보조13/14→I2.4/2.5 | Q=현장전압/접촉기흡입/실회전아님 |
| 150초고장 | Tag94입력·현재Q·raw응답/Inputs·호출 | 150ms로오독하거나원인없이시간변경금지 |
| 누적초과고장 | W29/W30,Q방향,공유PBox,엄격±3400비교/Move0 | 엔코더오차3400·34초등으로환산금지 |
| 한계표시반대 | LS19/20 NC와0397 NOT쓰기,DB11표시 | 정상극성/단선반응/캠위치확인전기구불량단정금지 |
| 개도고정/−9999 | ZT04 A/B,DB17/ACT_CNTV2,gating,CH02,/100,Int변환,계수/OFR | TM하드웨어채널과SW_GATE2숫자만으로매핑확정금지 |
| 교정후이상 | R의열림차단·닫힘OR,NewCountValue/SetCountValue,미결속HSC핀 | 재교정버튼실행권고금지 |
| 버너순서중MV03요청이상 | 0184 W/B Set/Reset,NOT Close AND Close상충,State2NOTOpen,State5Close OR ON | BR01전체보호/정상순서를추정으로완성하지않음 |
| 모터용량/보호판단필요 | M17명판,FG38와P&ID상충,준공변경 | 0.25/2.2kW중임의채택·전류설정상향금지 |

관찰필드초안:설비/태그·정확한DB주소,관찰자,시각/시간대,위치,원본해시/프로젝트,값/단위,수집장치,raw/Inputs/HMI층,최초불일치,비교원본,배제근거,미확정,승인된조치,복구전후증거. 빈칸을정상/완료로채우지않고실제운영기록은공개문서에추가하지않는다.

## 7 완료 기준·미확정·인계

| 7영역 | 적용 | 미완료 경계 |
| --- | --- | --- |
| 설비·자료 기준 | §1,E01/02/26 | 실물identity=false |
| I/O·HMI | §2,E03/04/18 | 원시응답2태그선언/HMI10핀미결속 |
| 제어 구조 | §3,E05~08/12~19 | HSC21핀/PID9핀RefId없음;현재호출·다른쓰기미확정 |
| 전기 전달 경로 | §4,E20~25 | 실물/정상극성/준공도/현행보호미확정 |
| 알람·복구 | §5,E09~11/19 | 현장해제/재기동/복구미실행 |
| 증상별 수리 | §6 | 관찰자료중심초안,현장조치미수행 |
| 완료 기준 | §7 | 문서/정적/UI/게시/TIA/CPU/현장분리 |

### 독립 통합자가 먼저 확인할 핵심

1. 0159 S5T#150S/T3,0352 W29>3400/W30<−3400,동일DB3.X4.3을확인한다.
2. 0397 raw끝단NOT쓰기와0514의**처리Close NOT**사용을결속한다.
3. 0345에상대Q접점이없음,세정/기동/교정OR위치,하드웨어NC인터록을구분한다.
4. 0344와0479의M14.4/M14.5중복쓰기,OFF=심볼,not-used제목의한계를유지한다.
5. 0184 NOT Close28 AND Close1670의동일0585 RID233,State2NOTOpen,State5Close OR ON,State7B Set을재확인한다. 의도추정으로원본을교정하지않는다.
6. FG38/P&ID모터상충,FG75/0497압력태그상충,FG146 CH0와SW_GATE2매핑미확정을반영한다.
7. HSC21핀은RefId없음이며ErrorAck/EventAck도포함한다. MV01의Reset결속을복사하지않는다.
8. 지정원본/페이지와핵심주장부터재확인하고전체설비를중복조사할필요없이미확정자료확보여부를분리한다. 기존완료/미확정/미지기록필드는보존한다.

### 누락 자료

- 현재CPU/프로젝트일치·호출순서·간접/HMI쓰기·OFF현재값:공개백업만으로완료불가.
- M17/구동기명판·38QM1현행설정·교체/준공이력:P&ID/전기도면상충해결에필요.
- PSH02/03센서명판·압력취출점·양단배선·준공개정:제어원천과물리소유확정에필요.
- HMI호출정식Export/NID/실인수:10핀미결속해결에필요.
- DB17 HSC인스턴스·hardwareID/모듈/채널/분해능/방향·RefId없는21핀의정식표현:카운트/교정/진단연결에필요.
- 0479 지역Real_SPPC02/Real_PC02상류식·DB25설정·현재호출:PC02경로의현행성확정에필요.
- 위치별raw/Inputs/HMI·기계캠기준·ZT04교정자료:정상극성/영점/개도단위확정에필요.
- 현장원인해소/승인된재기동/실응답·알람해제증거:복구완료는문서검토로대체불가.

### 네 기능과 최종 상태

| 항목 | 이번 상태 |
| --- | --- |
| 도면·래더 비교 | 지정원본XML/선언/핀/PDF정적대조와근거표 |
| 백업·선택복원 | 보존요건초안만,구현/시험미수행 |
| 기록 전후 비교 | 관찰필드초안,구현/시험미수행 |
| 보고서/PDF | MD산출물;앱보고서/A4PDF검증미수행 |
| documentation | draft_ready,통합완료아님 |
| static_review | 지정범위대조완료;전체현재프로그램검증아님 |
| ui_records / publication | not_run / not_published_by_Dots |
| tia_compile / live_cpu / field_recovery | 각각not_performed |

이번완료산출물은MV03한개의문서초안이다. 다음승인순서후보는**MV06한개**이며이번에착수하지않았다. 2차133후보는제외했다.

## 부록 A 핵심 주장 근거표

Flg/Ident는§1.3의decoded-original 경로다. 전체원본경로·고정커밋링크·해시는부록C에있다.

| ID | 주장 | 원본 | Part/Wire/핀/선언·페이지 | 해석과미확정 |
| --- | --- | --- | --- | --- |
| E01 | P20/MV03 본체 식별 | INVENTORY.json;WORK-STANDARD/WORK-ITEM-TEMPLATE | mapping=tag,identity_verified=false,parent=null,phase1 | 본체/구동모터 관계 확인 주석;현재 실물 미확정 |
| E02 | P&ID 역할·용량 상충 | PID_1684n002I.pdf | PDF1 Overflow valve MV03/M17/LS19/20/ZT04,0.25kW440V | FG38 2.2kW와 상충;실명판으로 해결 필요 |
| E03 | 고유 I/O·처리 주소 | live_index.json;0617/0618/0619/0573/0627/0629 Ident | doc883/884;Q AO15/16;raw LS AO61/62;Inputs 응답 AO20/21 | 응답2태그 원시 SimpleAccess 미확보;백업주소와현행구분 |
| E04 | 입력 전달·반전·호출 | 0397/0030 Flg;0627/0628/0629/0690/0691/0692 Ident | LAD1070 Move27 W31/32;Not142→Coil147,Not150→Coil151;LAD1613 ENO/NOT Simulation(1) | 처리끝단 NOT 쓰기;현재CPU·외부쓰기미확정 |
| E05 | PSH03 오차/타이머 | 0344 Flg;0062/0617/0618/0619/0620 Ident | LAD1705 NID3,Sub256,Gt가아닌Ge276≥5,Lt282<−5,SD263/268 | T1394초/T13810초;실제주기·물리단위미확정 |
| E06 | 최종 출력·우선 가지 | 0345 Flg;0617/0618/0619 Ident | LAD1706 NID4,C390/C407,OR543/544/53,NOT W539,Reset546 | 상대Q차단접점없음;세정/기동/교정분리;실제안전성미검증 |
| E07 | 요청 해제/startup | 0345/0149 Flg;0563/0617/0619 Ident | R362/R369/R46,0149 S300 W329/ORef318 RID44 | 알람Reset아님;현재Auto/다른쓰기미확정 |
| E08 | 교정 절차 | 0353 Flg;0618/0619/0620 Ident | LAD1707 NID13,Move32,C44,R48,NewCount RID193/SetCount RID195 | DB17내부멤버;HSC실핀결속·영점완료미확정 |
| E09 | 150초 응답 fault/Reset | 0159 Flg;0570/0571/0572/0573 Ident | LAD1226 NID1,SD281 W453/454,S286 W457,R350 W501;Tag94T3 | S5T#150S,V8528;현재CPU/실제지연/적절성미확정 |
| E10 | 명령 누적 생성 | 0351 Flg;0617/0618/0619/0620 Ident | LAD1713 NID11,PBox1235,Q1661/1663,Add1316/Sub1331,Move1322/1337 | W29/W30,공유10ms에지;엔코더실측/초환산아님 |
| E11 | 누적 초과 동일래치 | 0352 Flg;0618/0619/0620 Ident | LAD1714 NID12,Gt1656/S1662/Move1665,Lt1670/S1676/Move1679 | >3400/<−3400;누적0과faultReset분리 |
| E12 | HSC 호출 | 0508 Flg;0673/0676/0678/0679 Ident | LAD1758 NID47,LRef22/Instance23,NOT Simulation75,EM_OK21,SwGateW51,CountW71 | DB17;21핀RefId없음;진단/Reset연결추정금지 |
| E13 | 엔코더 환산 | 0514 Flg;0672/0674/0675/0676/0677/0678/0680 Ident | LAD1764 NID32,처리CloseNOT1219,C1129,Add1134/Div1138/Move1142/1151/1156,CRef1163 | SW_GATE2,CH02,/100,DInt→Int,계수/OFR;현재교정미확정 |
| E14 | 엔코더 기억 다른쓰기 | 0511 Flg;0676/0677/0678 Ident | LAD1761 NID30,NOT EM_OK963→Move927 W956/957;RID197/198 | localCNT_Act_2→CH02;실행순서/로컬값수명미확정 |
| E15 | CONT_S 중복 쓰기 | 0479 Flg;0665/0667/0668/0669/0670/0671 Ident | LAD15 NID12,OFF583→LRef507,DB25,QLMNUP/DN W577/578→M14.4/14.5 | not-used제목≠실행불가증명;9핀RefId없음 |
| E16 | 버너 소유 요청/상충 | 0184 Flg;0582/0583/0584/0585 Ident | LAD1868 NID14,NOTClose28 AND Close1670(RID233),S1176/R1237/R1303/S1306,State5 OR1248 | 동일값직렬상충·Close OR ON보존;BR01전체안전/현행순서미확정 |
| E17 | PSH03 압력원천 | 0497 Flg;0672/0674/0676/0678/0680 Ident | LAD1747 NID17,CRef476 AnalogW491/ORef484,RID106 PeripherieAO2560 | PIW320→DataPSH03;PSH02/PEW286도면라벨과구분 |
| E18 | HMI 설정/호출 | hmi_plc_tags.csv;0369 Flg;0623/0624/0626 Ident | LAD1191,14실인수중4FALSE/10미결속,MV03 dde.cfg9행 | DB11표시/DB2요청/DB41절차/DB3알람구분 |
| E19 | 선형화/OFR | 0291/0014 Flg;0611/0612 Ident | LAD1658/1659,Gt258/Le161,Convert/Add/Mul/Div/Move185/193/Coil23 | −1382초과/32767이하,정수계산/−9999,일반coil;현장해제미확정 |
| E20 | 동력·보호·정격 | Electrical_Rev2.pdf | FG38/PDF39,38QM1/38KM1/2/38QS1/XM/M17 | 2.2kW4.31A,3.5–5A설계표기;P&ID상충·현재보호미확정 |
| E21 | 코일/인터록/출력모듈 | Electrical_Rev2.pdf | FG38/PDF39;FG137/PDF138단자18;FG138/PDF139단자21;XS25/26 | 상대NC31/32는하드웨어;0345상대Q접점으로대체금지 |
| E22 | 응답·한계센서 | Electrical_Rev2.pdf | FG38/39/118/123,PDF39/40/119/124;보조13/14,LS19/20 NC11/12 | I2.4/2.5는보조응답;LS반전/정상극성별도 |
| E23 | ZT04/TM 끝점 | Electrical_Rev2.pdf | FG39/PDF40 X1/85~89→FG146/PDF147 MOD17단자1/2/9/10 | CH0.A/B와SW_GATE2매핑미확정;SPARE카운트주소추정금지 |
| E24 | 압력 회로/태그 상충 | Electrical_Rev2.pdf | FG75/PDF76 PSH02/286 OUTPUT MV03 vsPSH03/320;FG108/PDF109단자2/4/18 | 4–20mA/0~10mbar도면;현행계기·취출점·소유미확정 |
| E25 | 시공 케이블/공유함 | Electrical_Can_Decoating_20241118.pdf | PDF51row1_9;PDF56row6_1/3/11/15/16/17 | FIRST DRAFT,LS15/16공유·HE01PSH03소유표기;가림행제외 |
| E26 | 기존 자료/다른쓰기보존 | MV03.html 7종;0635 Ident;network-map.json | 기존circuit-guide반대출력문구정정후보,Data.Pot_MV03 NID2 UID509/517 Write | 원파일미수정;기존simulation선언만읽기,실행없음 |

## 부록 B HSC 실제 핀과 RefId 부재

0508 LRef22의 en 이외23개핀을원본Wire에서읽었다. 2개만RefId가있고21개는원본ORef에RefId속성자체가없다. 이부재를FALSE/0/기본값/빈배선의현장상태로단정하지않는다.

| 핀 | Wire/ORef | 원본RefId/결속 |
| --- | --- | --- |
| SwGate | W51/ORef25 | 236 SW_GATE2 |
| CaptureEnable | W52/ORef26 | RefId 없음 |
| SyncEnable | W53/ORef27 | RefId 없음 |
| ErrorAck | W54/ORef28 | RefId 없음 |
| EventAck | W55/ORef29 | RefId 없음 |
| SetCountValue | W56/ORef30 | RefId 없음 |
| StatusHW | W57/ORef31 | RefId 없음 |
| StatusGate | W58/ORef32 | RefId 없음 |
| StatusUp | W59/ORef33 | RefId 없음 |
| StatusDown | W60/ORef34 | RefId 없음 |
| CompResult0 | W61/ORef35 | RefId 없음 |
| CompResult1 | W62/ORef36 | RefId 없음 |
| SyncStatus | W63/ORef37 | RefId 없음 |
| CaptureStatus | W64/ORef38 | RefId 없음 |
| CapturedValue | W65/ORef39 | RefId 없음 |
| ZeroStatus | W66/ORef40 | RefId 없음 |
| PosOverflow | W67/ORef41 | RefId 없음 |
| NegOverflow | W68/ORef42 | RefId 없음 |
| Error | W69/ORef43 | RefId 없음 |
| ErrorID | W70/ORef44 | RefId 없음 |
| CountValue | W71/ORef45 | 238 ACT_CNTV2 |
| MeasuredValue | W72/ORef46 | RefId 없음 |
| CompareMeasuredValue | W73/ORef47 | RefId 없음 |

### 이번에 확인한 타이머 구분

| 용도 | 원본설정·주소 | 위치 |
| --- | --- | --- |
| MV03응답감시 | 150S/Tag94 T3 | 0159 SD281,0571 RID83 |
| MV03압력비교허가 | 4S/Tag148 T139,10S/Tag147 T138 | 0344 SD263/268,0617 RID34/32 |
| 공유작업펄스 | 200MS/Tag155 T79,2S/Tag154 T78 | 0350 SD813/818;최종출력P OR ON과분리 |
| 공유명령누적에지 | 10MS/Tag157 T119와Tag156 T118 | 0351 SD1225/1230/PBox1235 |
| 버너세정/순서소유 | 4M/Tag143 T31,1S/Tag142 T32,1S/Tag144 T37,30S/Tag145 T38 | 0184 SD1199/1215/1262/1329;MV03동력보호시간아님 |
| 별도CONT_S호출인자 | CYCLE100MS,TI10S,PULSE200MS,BREAK5S,MTR3S | 0479;현재활성/실행주기/권장튜닝아님 |

## 부록 C 고정 원본 SHA-256 84개

고정커밋 c14bfd125a06e5d90bc1732c1cef5cd19ff1895b에서읽어계산했다. ZAP18/PLF는백업보존기준해시이며TIA로열기/컴파일/다운로드하지않았다. 해시일치는현재CPU일치나파일전체모든기능검증을뜻하지않는다.

| 원본경로 | SHA-256 |
| --- | --- |
| [AGENTS.md](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/AGENTS.md) | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 |
| [.agents/skills/gme-equipment-rollout/SKILL.md](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/.agents/skills/gme-equipment-rollout/SKILL.md) | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b |
| [docs/equipment-standard/WORK-STANDARD.md](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/docs/equipment-standard/WORK-STANDARD.md) | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 |
| [docs/equipment-standard/WORK-ITEM-TEMPLATE.md](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/docs/equipment-standard/WORK-ITEM-TEMPLATE.md) | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 |
| [docs/equipment-standard/INVENTORY.json](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/docs/equipment-standard/INVENTORY.json) | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc |
| [VERSION.json](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/VERSION.json) | 0dc1b8435a18e5d2820300b8ec6778c90c660dd81b51abfe19c6fb922d7d27e5 |
| [all-in-one/sources/Electrical_Rev2.pdf](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/Electrical_Rev2.pdf) | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| [all-in-one/sources/Electrical_Can_Decoating_20241118.pdf](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/Electrical_Can_Decoating_20241118.pdf) | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| [all-in-one/sources/PID_1684n002I.pdf](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/PID_1684n002I.pdf) | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| [all-in-one/sources/GME_20250506.zap18](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/GME_20250506.zap18) | 00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8 |
| [all-in-one/sources/PEData.plf](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/PEData.plf) | 647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a |
| [all-in-one/sources/source-manifest.json](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/source-manifest.json) | 5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf |
| [all-in-one/sources/live_index.json](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/live_index.json) | 14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1 |
| [all-in-one/sources/hmi_plc_tags.csv](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/hmi_plc_tags.csv) | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
| [all-in-one/sources/hmi-windows.csv](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/hmi-windows.csv) | 15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e |
| [all-in-one/sources/decoded-original/network-map.json](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/network-map.json) | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 |
| [all-in-one/sources/decoded-original/0014-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0014-FlgNet.xml) | 2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30 |
| [all-in-one/sources/decoded-original/0030-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0030-FlgNet.xml) | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b |
| [all-in-one/sources/decoded-original/0149-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0149-FlgNet.xml) | bc2519cdad49a7268006b194e8e5e1160744ff221f04b83e710f31f57bc617f9 |
| [all-in-one/sources/decoded-original/0159-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0159-FlgNet.xml) | 5598abbad86ed26fa8dd17fc3eca3e1c0b7941a2798db6ae1e2472a7ca448d2a |
| [all-in-one/sources/decoded-original/0184-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0184-FlgNet.xml) | a0a59597c73eb68e1cbdb2f41d640eabccfd05655c4e9c08624be6027974caf3 |
| [all-in-one/sources/decoded-original/0291-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0291-FlgNet.xml) | fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550 |
| [all-in-one/sources/decoded-original/0344-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0344-FlgNet.xml) | 08eabc412b9457eb615d1cb01b92682987bef170cbeab78070dd4c705ab93576 |
| [all-in-one/sources/decoded-original/0345-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0345-FlgNet.xml) | b278a319d4d8cb8d157f449a2365445ff8f172245ebd2a468aa3ee79dba60f93 |
| [all-in-one/sources/decoded-original/0350-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0350-FlgNet.xml) | 3f426a4ba9455160b8113df968b1052752a7b72cdfca8e57bdfd466340d691ff |
| [all-in-one/sources/decoded-original/0351-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0351-FlgNet.xml) | 1448cd179747074ae5ac3647c52e47950d18e0d90fa2f1cb155dbb24af50a7f6 |
| [all-in-one/sources/decoded-original/0352-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0352-FlgNet.xml) | 03e2d68dda289fcb7e7738c2f52e675890b252f5b526cab1ec2049323ab30d75 |
| [all-in-one/sources/decoded-original/0353-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0353-FlgNet.xml) | 062854b25c5afacb34e53ce0ee7cd8c660cd9a0f5b79a02d8a5fbed89c794766 |
| [all-in-one/sources/decoded-original/0369-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0369-FlgNet.xml) | f64e35330b3816e761ce72575977878d5cad6317191297c2a64107629a611806 |
| [all-in-one/sources/decoded-original/0397-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0397-FlgNet.xml) | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 |
| [all-in-one/sources/decoded-original/0479-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0479-FlgNet.xml) | 112e55599a4dc705438c8c61b936da9a167c22d9bbd909eda11c45c9dc33e839 |
| [all-in-one/sources/decoded-original/0497-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0497-FlgNet.xml) | 334a065d6dc7aac9e9652a1f705a31fdadea6a5d4760dd6aa2ed3283a8e4b665 |
| [all-in-one/sources/decoded-original/0508-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0508-FlgNet.xml) | 21f461aced38216c15a873f61b461c962662aa11367309835c7203508f804bb4 |
| [all-in-one/sources/decoded-original/0511-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0511-FlgNet.xml) | a4bf314bf817f0f666a0c9fdd26df134cedeed8666819c7a3e8e6438850eace6 |
| [all-in-one/sources/decoded-original/0514-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0514-FlgNet.xml) | 3826044da205b26e31f400232a55aa240eef8a4933e532d0bf9a3bccee2d19c5 |
| [all-in-one/sources/decoded-original/0062-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0062-IdentXmlPart.xml) | 34f188168dc4fad0d6e2c813028045f37b84025636bcebd8aa1c7ffb4cfd9bcd |
| [all-in-one/sources/decoded-original/0555-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0555-IdentXmlPart.xml) | 46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6 |
| [all-in-one/sources/decoded-original/0563-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0563-IdentXmlPart.xml) | 86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad |
| [all-in-one/sources/decoded-original/0570-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0570-IdentXmlPart.xml) | 9fed133006458c3b43b1d5f2c15107a5a86b4fb7cdbaf3743bf88f0e5a105495 |
| [all-in-one/sources/decoded-original/0571-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0571-IdentXmlPart.xml) | 4a9deeb65a22e497e284fe6d98929e1d201ef5939e4aeca5805b4eb7e007d398 |
| [all-in-one/sources/decoded-original/0572-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0572-IdentXmlPart.xml) | 5ecd18f84e12d702bb46f759b23994dacfa2d97d50fe51e766ca0cf43f75bb4c |
| [all-in-one/sources/decoded-original/0573-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0573-IdentXmlPart.xml) | a22cc24a974e0c792f32e356a14b277a847e2bb204c91bce01c37d1714ddb56c |
| [all-in-one/sources/decoded-original/0582-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0582-IdentXmlPart.xml) | 41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951 |
| [all-in-one/sources/decoded-original/0583-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0583-IdentXmlPart.xml) | 0a34a2b7ad17eba6198dbe53d5c6aa8e87710c7436b832b9d39a075074ab58a8 |
| [all-in-one/sources/decoded-original/0584-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0584-IdentXmlPart.xml) | 3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d |
| [all-in-one/sources/decoded-original/0585-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0585-IdentXmlPart.xml) | e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184 |
| [all-in-one/sources/decoded-original/0611-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0611-IdentXmlPart.xml) | 0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089 |
| [all-in-one/sources/decoded-original/0612-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0612-IdentXmlPart.xml) | 95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38 |
| [all-in-one/sources/decoded-original/0617-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0617-IdentXmlPart.xml) | 10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9 |
| [all-in-one/sources/decoded-original/0618-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0618-IdentXmlPart.xml) | 0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c |
| [all-in-one/sources/decoded-original/0619-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0619-IdentXmlPart.xml) | 85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456 |
| [all-in-one/sources/decoded-original/0620-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0620-IdentXmlPart.xml) | da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3 |
| [all-in-one/sources/decoded-original/0623-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0623-IdentXmlPart.xml) | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 |
| [all-in-one/sources/decoded-original/0624-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0624-IdentXmlPart.xml) | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a |
| [all-in-one/sources/decoded-original/0626-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0626-IdentXmlPart.xml) | a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b |
| [all-in-one/sources/decoded-original/0627-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0627-IdentXmlPart.xml) | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| [all-in-one/sources/decoded-original/0628-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0628-IdentXmlPart.xml) | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd |
| [all-in-one/sources/decoded-original/0629-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0629-IdentXmlPart.xml) | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| [all-in-one/sources/decoded-original/0635-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0635-IdentXmlPart.xml) | 1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457 |
| [all-in-one/sources/decoded-original/0665-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0665-IdentXmlPart.xml) | 50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd |
| [all-in-one/sources/decoded-original/0667-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0667-IdentXmlPart.xml) | ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3 |
| [all-in-one/sources/decoded-original/0668-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0668-IdentXmlPart.xml) | 2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed |
| [all-in-one/sources/decoded-original/0669-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0669-IdentXmlPart.xml) | 754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2 |
| [all-in-one/sources/decoded-original/0670-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0670-IdentXmlPart.xml) | e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841 |
| [all-in-one/sources/decoded-original/0671-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0671-IdentXmlPart.xml) | 26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293 |
| [all-in-one/sources/decoded-original/0672-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0672-IdentXmlPart.xml) | 6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222 |
| [all-in-one/sources/decoded-original/0673-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0673-IdentXmlPart.xml) | 450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58 |
| [all-in-one/sources/decoded-original/0674-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0674-IdentXmlPart.xml) | 4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84 |
| [all-in-one/sources/decoded-original/0675-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0675-IdentXmlPart.xml) | b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3 |
| [all-in-one/sources/decoded-original/0676-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0676-IdentXmlPart.xml) | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 |
| [all-in-one/sources/decoded-original/0677-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0677-IdentXmlPart.xml) | 69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3 |
| [all-in-one/sources/decoded-original/0678-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0678-IdentXmlPart.xml) | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 |
| [all-in-one/sources/decoded-original/0679-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0679-IdentXmlPart.xml) | d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56 |
| [all-in-one/sources/decoded-original/0680-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0680-IdentXmlPart.xml) | fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95 |
| [all-in-one/sources/decoded-original/0690-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0690-IdentXmlPart.xml) | fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541 |
| [all-in-one/sources/decoded-original/0691-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0691-IdentXmlPart.xml) | 17cb7d9734d76b39e729e0daf0c89d9bdf74907aab2130c80453fa04e4cea1da |
| [all-in-one/sources/decoded-original/0692-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/sources/decoded-original/0692-IdentXmlPart.xml) | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| [all-in-one/devices/MV03.html](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/devices/MV03.html) | 2e3f06f11e6f89d468360fbf85790dbc7d5265fec741d087b7f7652579ccc421 |
| [all-in-one/control-specs/MV03.html](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/control-specs/MV03.html) | db5b70ebec268b651f78ab798ec9d6faf7c52951f622238a99b0e1f9ab242106 |
| [all-in-one/alarm-guides/MV03.html](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/alarm-guides/MV03.html) | 63bbf8dab5ace721598611aeec9dd572e644b793ce337055f84e9211a6c257ec |
| [all-in-one/circuit-guides/MV03.html](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/circuit-guides/MV03.html) | 3b3998a8006d0a8fa3d36eea124dcf2bc795d42f7f53216914d37c3faf8a5041 |
| [all-in-one/signal-guides/MV03.html](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/signal-guides/MV03.html) | b268991bcb453466573cca92a0b0dff75d388be4be46377f3b7fff5a5919c4de |
| [all-in-one/construction-guides/MV03.html](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/construction-guides/MV03.html) | e302f01e0184d8778bcdc7e564cead8f16d7c8a2750a319795c53d3832105e23 |
| [all-in-one/procedures/MV03.html](https://github.com/esp6662266/gme-plc-manual/blob/c14bfd125a06e5d90bc1732c1cef5cd19ff1895b/all-in-one/procedures/MV03.html) | 269252a648109688055bd12e5eb45e0d10d188d49b9475cda4c232ed6b420fbc |

## 부록 D 수행·보존 기록

- 수행: 공개고정원본읽기,XML정적파싱·Part/Wire/ORef/선언대조,지정PDF페이지실제렌더/시각확인,SHA-256계산,자체MD초안작성.
- 자체작성파일은조사폴더의초안·추출메모·렌더이며원본worktree는편집하지않았다. 종료시git status로확인한다.
- 미실행:프로젝트생성기/npm검사/UI·기록·PDF행동시험/시뮬레이터/TIA컴파일/PLC·현장조작/보호설정변경/게시.
- 사용자에게받은PV01/PV02접점5–9정정및원초안보존원칙을유지한다. MV03접촉기의31/32·13/14와혼합하지않았다.
- 이파일은독립통합자가지정핵심근거부터재확인하도록제공하는초안이며,기능통합·게시·현장복구완료표시가아니다.

