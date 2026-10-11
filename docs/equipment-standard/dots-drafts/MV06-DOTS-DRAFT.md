# MV06 P21 고유 제어 근거와 설비 문서 초안

- 산출물: MV06-DOTS-DRAFT.md, 1차 독립 통합 검토용, 2026-10-11 KST.
- Dots 자체 환경에서 직접 조사했다. 대상은 MV06(P21) 한 개이며 사용자가 유일한 로컬 편집·검증·게시 담당이다.
- 공개 저장소 esp6662266/gme-plc-manual의 main/all-in-one 기준. 고정 **abcf31c5030bc7ef8749ed8e869a857f2387a28a / v1.12.0**. MV06 게시 버전이 아니라 조사 원본 고정점이다.
- GME-STD-1.0.0, 저장소 AGENTS·gme-equipment-rollout SKILL·WORK-STANDARD·WORK-ITEM-TEMPLATE·INVENTORY의 7영역/근거 추적/완료 분리를 적용했다. 제공 환경에서 tia-equipment-alarm-trace 스킬은 확보하지 못했다. 권한을 확장하지 않고 공개 표준·원본 XML·PDF 실제 렌더를 사용했다.
- 원본·기존 완료/미확정 자료·이전 초안을 보존했다. 공통 코드·버전·대장·배포·운영 기록은 편집하지 않았다. 새 Work/Codex 생성·재위임, 시뮬레이터 작성·수정·생성·실행·행동시험, 실제 PLC·현장·보호값·별도 SEJIN 프로그램 변경은 없다.
- 현재 CPU·실물·정상 극성·현행 보호 설정·현장 복구는 미확정이다. 이 문서는 정적 원본 검토이며 TIA/UI/기록/배포/현장 검증 완료를 뜻하지 않는다.

## 먼저 확인할 MV06 고유 사항

1. 최종 방향 출력0349의 공통 앞단은 **NOT ON**이다. 수동 요청 Reset 가지에는 NOT ON이 두 번 직렬이다. 반면 압력 제어·Shot 생성·방향 응답/누적 감시는 ON을 읽는다. 같은 M0.0 선언까지 확인했고, 정상 논리로 임의 교정하지 않았다. [E05~E10]
2. 공통 인버터 알람0455에는 **Start Aux INV AND NOT Start Aux INV**가 직렬이다. 같은 Q1.0 선언이며 두 Set 경로 앞에 있다. 정적 동일값 조건의 상충을 보존하고 현재 실행/알람 무효를 단정하지 않는다. [E16]
3. MV06 자체 응답 감시는 **150ms, Tag97=T16**이다. 누적 감시는 **W19>2200 / W20<−2200**이며 같은 MV_06_FAULT를 Set한다. 인접 MV03의150초/3400을 복사하지 않는다. [E09,E10]
4. SETPOINT≠0 경로는 환산 Data.PSH_02의 오차를, SETPOINT=0 경로는 **원시 PSH02:P**와0을 비교한다. 두 입력의 단위·범위를 혼합하지 않는다. [E05,E06,E17]
5. 공통 30AS1 인버터는 MV02/MV05/MV06 공유다. Q1.0,공통 응답/알람과 MV06 Q1.1/Q1.2·M14·방향응답을 분리한다. [E15,E16,E20~E22]
6. FG30/PDF31 실제 START 31KA1 및 RESET 17KA2 부하 접점은 **5–9**다. 기존 설명의1–9는 정정 후보이며 원자료를 보존한다. [E20]
7. P&ID/시공 도면은 LS34/35,OEM FG33은 LS40/41이다. 시공 동일 FLO4TB2A ID 두 행은 신호·시작점·규격이 달라 합치지 않는다. [E02,E23,E25]
8. HSC21핀은 RefId가 없고 HMI10핀은 선언 미결속이다. MV06 전용 HMI 설정은8행이며 별도 RESET_ENC_MV06/교정 네트워크는 이번 검색에서 확인하지 못했다. 앞선 설비의 교정 절차를 추가하지 않는다. [E12,E18]

## 1 설비와 자료 기준

### 1.1 식별·역할·소유

P21→MV06은 태그 대응이며 실물 동일성 미확정으로 유지한다. P&ID PDF1은 Overflow valve MV-06, M14, ZT06, LS34/35,0.25kW440V를 표시한다. OEM FG32의 M14도0.25kW이지만 이 일치만으로 현행 명판·교체 모델·현장 동일성을 완료하지 않는다. [E01,E02]

공통 인버터30AS1은 FG30 제목에 MV-2/MV-5/MV-6가 함께 적혀 있고 출력30U1/V1/W1이 각 분기로 이어진다. 공통 전원·기동·STO·리셋의 소유를 MV06 한 개로 합치지 않는다. 시공 UC01/FLO4TB1과 MV06/FLO4TB2도 위치·배선 경유점이며 이름만으로 본체 소유를 바꾸지 않는다.

### 1.2 기존 자료 보존과 정정 후보

devices/control-specs/alarm-guides/circuit-guides/signal-guides/construction-guides/procedures의 MV06.html을 읽고 원파일을 보존했다. 기존 alarm-guide의 NOT ON·동일 래치·누적값/엔코더 구분을 유지한다. 기존 circuit-guide의31KA1 접점1→9 설명은 실제 FG30 부하선5→9와 대조하여 통합자가 정정할 후보로 남긴다. 기존에 기록된 C01 중복 케이블·C03 ZT05/06 명칭 문제는 삭제하지 않는다. [E26]

### 1.3 근거 표기

네 자리 Flg는 all-in-one/sources/decoded-original/NNNN-FlgNet.xml, Ident는 같은 폴더의 NNNN-IdentXmlPart.xml이다. LAD는 network-map.json document_id, NID는 선언의 원본 네트워크 식별자다. Part/Wire/ORef UID와 선언 RID를 구분한다. 예:0349 ORef22/RID1은0617 NID9 ON의 SimpleAccess이며,다른 HMI 블록의 RID1 함수 후보를 사용하지 않았다. 해시는 부록에서 고정 커밋 경로와 연결한다.

## 2 I/O·내부 변수·HMI

### 2.1 원시 주소와 처리 층

| 항목 | 원시 백업 근거 | 처리 변수·도면 끝점 |
| --- | --- | --- |
| 공통 기동 | Start Aux INV Q1.0;0063 RID776 Output AO8 | 0363 Coil64;FG137 MOD14단자11→FG31 31KA1 |
| 공통 응답 | mv02_05_06_power_ok I1.4;live_index doc494 | Inputs.Aux inverter RUN DB13.X1.4;0657 RID307 AO12;FG117단자15 |
| 공통 이상 | mv02_05_06_inv_all I1.5;doc915 | Inputs.Aux_Inv_All DB13.X1.5;0657 RID308 AO13;FG117단자16 |
| MV06 열림응답 | mv06_fbk_opening I1.6;doc495 | Inputs.MV06 Run_Opening DB13.X1.6;0573 RID69 AO14;FG117단자17 |
| MV06 닫힘응답 | mv06_fbk_closing I1.7;doc496 | Inputs.MV06 Run_Closing DB13.X1.7;0573 RID70 AO15;FG117단자18 |
| 열림 끝단 | mv06_open I6.7;doc657,주석LS.40 | Inputs.MV06_Open DB13.X6.7;0619 RID181 AO55;FG122 MOD9단자28 |
| 닫힘 끝단 | mv06_close I7.0;doc1527;0678 RID260 Input AO56 | Inputs.MV06 Close DB13.X7.0;0619 RID182 AO56;FG123단자31 |
| 열림 명령 | Open MV06 Q1.1;0617 RID98 Output AO9 | 0349 Coil821/ORef857 Write;FG137단자12→32KM1 |
| 닫힘 명령 | Close MV06 Q1.2;0617 RID97 Output AO10 | 0349 Coil837/ORef866 Write;FG137단자13→32KM2 |

raw 공통응답/이상·방향응답·열림끝단5태그는 live_index와 도면을 확인했지만 동명 SimpleAccess를 직접 결속하지 못했다. 처리 DB 선언을 원시 태그 선언이라고 바꿔 쓰지 않는다. 도면 RUNNING과 백업 power_ok는 해석상의 별칭 후보이며,현재 신호 의미/극성은 미확정이다. [E03]

### 2.2 입력 Word 전달·호출

LAD1070 0397 NID1에서 IW0→DB13.DBW0(공통/방향응답 포함),IW6→DB13.DBW6(두 끝단 포함)를 확인했다. [E04]

- Move22.in W23/ORef25=0627 RID3 Tag178 Word Input AO0;out1 W24/ORef26=0629 RID5 Word AO0 BAD4.
- Move42.in W52/ORef45=0627 RID13 Tag171 Word Input AO48;out1 W54/ORef46=0629 RID14 AO48 BAD4.
- 0628 RID4 Inputs TOD13. 이 MV06 Word 복사에는 비트 반전이 없다. 인접 MV03의 개별NOT쓰기를 MV06에 복제하지 않는다.
- main0030 LAD1613 NID19의 ENO 사슬 W32/33/42 뒤 NOT Simulation(1) Contact37(W44/ORef45,0692 RID140 M180.0)→W43 hmi inputs CRef28을 포함한다. 현재 호출·다른쓰기·CPU 값일치는 미확정이다.

### 2.3 고유 내부 변수

| 변수 | 백업 주소·선언 | 구분 |
| --- | --- | --- |
| Flag.MV06_Auto | DB2.X6.5;0619 RID81 AO53 | startup Set,두 압력모드/최종출력 사용 |
| Flag.MV06_Open / Close | DB2.X10.5/X10.6;0619 RID94/93 AO85/86 | 수동요청/PLC Reset |
| MV06 PID UP / DOWN | M13.2/M13.3;0617 RID80/78 AO106/107 | 0347 Coil 출력,CONT_S라고 이름만으로 단정 금지 |
| Shot to close / open | M18.0/M18.1;0617 RID82/83 AO144/145 | 0348 Set/Reset,자동 출력 OR |
| Data.PSH02_SETPOINT | DB1.DBW42;0619 RID71 AO336 | 0/비0 모드 분기 |
| Data.PSH_02 | DB1.DBW196;0619 RID73 AO1568 | 환산 압력,raw PIW286과 구분 |
| ErrPSH02 | local Int;0062 RID74,NID7 UID633 Write | SETPOINT−환산값 |
| Allarm.MV_06_FAULT | DB3.X11.6;0619 RID96/0573 RID36 AO94 | 응답/누적 공통 래치 |
| WorkData.W19/W20 | DB6.DBW38/DBW40;0619 RID140/142 AO304/320 | 방향 명령 누적 |
| Allarm.Aux_Inverter_Fault | DB3.X17.2;0657 RID204 AO138 | 공통 응답 감시 |
| Allarm.Aux_INV | DB3.X20.0;0657 RID238 AO160 | 공통 이상 입력 래치 |
| Data.Pot_MV06 | DB1.DBW136;0676 RID273 AO1088 | 위치 환산값 |
| Allarm.Pot_MV06_OFR | DB3.X25.2;0676 RID440 AO202 | 위치 범위,별도 알람 |
| Allarm.PSH02_OFR | DB3.X22.1;0676 RID387 AO177 | 압력 선형화 범위 |
| Coeff_MV06 / Zero_MV06 | DB4.DBW224/DBW222;0676 RID271/272 AO1792/1776 | 현재 계수/영점 미확정 |
| Encoder_CH04 / CH04_10 | DB8.DBD16/DBW44;0676 RID204/267 AO128/352 | DInt 기억/Int 환산 |
| MV06_Encoder | DB19;0673 RID350 TOD19 | HSC instance,하드웨어매핑 미확정 |

DB 번호는0618/0674/0655 DepDB 계열의 TOD 및 원본 주소 묶음으로 대조한다. symbol 이름이 같거나 DB내 offset이 같다는 이유만으로 다른 DB를 합치지 않는다.

### 2.4 HMI 8행과 호출 미결속

hmi_plc_tags.csv의 MV06 전용 설정은 다음8행이다. 현재 버튼 이벤트/쓰기권한/온라인 값의 증거가 아니다. [E18]

| 태그 | 주소 | ID |
| --- | --- | --- |
| MV_06\Allarme1 | DB11,X28.2 | 0040E |
| MV_06\Flag_CLOSE | DB2,X10.6 | 0040D |
| MV_06\Flag_OPEN | DB2,X10.5 | 0040C |
| MV_06\LimitSwitchClose | DB11,X28.4 | 0040B |
| MV_06\LimitSwitchOpen | DB11,X28.3 | 0040A |
| MV_06\OutputClose | DB11,X28.1 | 00312 |
| MV_06\AutoMan | DB2,X6.5 | 00047 |
| MV_06\OutputOpen | DB11,X28.0 | 00046 |

관련 I_PSH_02=DB13,INT50(ID00055)는 입력 표시층이며 Data.PSH_02 DB1.DBW196과 다르다.

LAD1187 0364 NID10,CRef23/CodeBlock22=HMI Standard Motorized Valve(0624 RID639/0623 RID130). 14실인수중 Allarme2/3/4/5 W30/32/34/36,ORef31/33/35/37은0626 RID20 false. 나머지10개는 선언 미결속이다:

| 핀 | Wire/ORef/RID | 색인 후보,확정 아님 |
| --- | --- | --- |
| Ingresso_run_Opening/Closing | W24/25/705,W26/27/704 | Inputs.MV06 응답 |
| Allarme1 | W28/29/156 | Allarm.MV_06_FAULT |
| Limit_switch_Open/Limiti_Switch_Close | W42/43/703,W44/45/702 | Inputs.MV06 위치 |
| Risposta_Opening/Closing | W50/51/150,W52/53/152 | Motors.MV06 응답 |
| Limit_Switch_Open_HMI/Close_HMI | W54/55/144,W56/57/146 | Motors.MV06 한계 |
| Comulativo_allarmi | W62/63/148 | Motors.MV06 집계 |

DB11 표시를 Q1.1/1.2 또는 DB3.X11.6과 동일주소로 표시하지 않는다. 별도 RESET_ENC_MV06 태그나 전용 HMI 교정 쓰기 사슬은 이번 참조 검색에서 미확보이며,없음을 현재 전체 프로그램에 일반화하지 않는다.

## 3 제어 구조와 소유

### 3.1 SETPOINT≠0:환산 압력 오차 제어

LAD1709 0347 NID7:ON675 W647/ORef628→W676 Ne592(Data.PSH02_SETPOINT W648/ORef629 ≠0 W649/ORef630)→W650. Sub598는SP W651/631−Data.PSH_02 W652/632→local ErrPSH02 W653/633을 쓴다. [E05]

- NOT Tag149677 W655/ORef635→W678 SD605,시간 **300ms** W654/ORef634,대상Tag150 W657/ORef636.
- Tag150679 W659/ORef638→W680 SD610,시간 **4s** W658/ORef637,대상Tag149 W661/ORef639.
- NOT Tag150681 W662/ORef640→W682 Ge618/Le624.pre.
- 오차 **≥5** W663/ORef641,W664/ORef642→W665 Coil621→W667/ORef643 MV06 PID DOWN.
- 오차 **≤−5** W668/ORef644,W669/ORef645→W670 Coil627→W672/ORef646 MV06 PID UP.
- Tag149=T135(0617 RID75),Tag150=T136(RID77). 물리 압력 단위·실제주기·조정의도는 미확정이다. ±5 비교를 인접 MV03의<−5로 복사하지 않는다.

### 3.2 SETPOINT=0:원시 입력 Shot 제어

LAD1710 0348 NID8:ON807→Auto809→Eq693(SP=0 W772/747,W773/748)→NOT ShotClose811→NOT ShotOpen813→W814 두 비교. [E06]

- raw **PSH02:P≤0**:Le701 W777/ORef751,W778/ORef752→W779 SD707 **S5T#20S**(W780/ORef753),Tag151(W781/754)→Contact815→W816 S712 ShotClose(W784/756).
- raw **PSH02:P>0**:Gt715 W786/ORef757,W787/ORef758→W788 SD721 **S5T#2S**(W789/759),Tag152(W790/760)→Contact817→W818 S726 ShotOpen(W793/762).
- ON공통에서ShotClose819 OR ShotOpen821→OR729 W798→SD735 **S5T#300MS**(W799/765),Tag153(W800/766)→Contact823→W824 R741 ShotClose(W802/768) 및R743 ShotOpen(W803/769).
- Tag151=T140(RID88),Tag152=T143(RID90),Tag153=T141(RID91),모두0617 Timer 선언. Reset 타이머 가지에는 Auto/SP=0 직렬조건이 별도로 없다(ON공통에서 분기).

원시PSH02는0617 RID84 Input Peripherie AO2288=PIW286 Int다. 0을0mbar로 확정하지 않는다. Shot의300ms는 내부 요청 해제 인자이며 실제 모터가300ms 움직였다는 결과가 아니다.

### 3.3 최종 출력 앞단 NOT ON과 요청 해제

LAD1711 0349 NID9. Contact915 **Negated operand**,W27/ORef28=0617 RID1 ON(M0.0). 여기서W916으로 요청Reset의NOT ON917 및출력허가NOT Fault931로 분기한다. [E07]

- 요청Open Reset:NOT ON915→NOT ON917(W21/ORef22,같은RID1)→(InputsOpen919 OR FlagClose921 OR Auto923)→OR790→R794 FlagOpen W874/ORef843.
- 요청Close Reset:같은NOT ON두접점→(InputsClose925 OR FlagOpen927 OR Auto929)→OR797→R801 FlagClose W880/ORef847.
- startup0149 LAD404 NID4:ON337→W338→S310 Flag.MV06_Auto W334/ORef322,0563 RID47 AO53. 현재Auto나재기동결과는미확정이다.

A=Auto,U/D=PID UP/DOWN,O/C=수동요청,So/Sc=ShotOpen/Close,P=MV WORK PULSE,F=fault,Lo/Lc=처리한계라고할때정적접속식은:

- Q1.1=NOT ON AND NOT F AND ((A AND (U OR So)) OR (O AND (P OR ON))) AND NOT Q1.2 AND NOT Lo.
- Q1.2=NOT ON AND NOT F AND ((A AND (D OR Sc)) OR (C AND (P OR ON))) AND NOT Q1.1 AND NOT Lc.

핵심배선:NOT F931(W882/ORef848)→W932;열림Auto933→UP935/Shot937→OR965.in1/2,수동939→P941/ON943→in3/4;OR965 W893→NOT Qclose945(W894/855)→NOT Lo947(W895/856)→W948 Coil821(W897/857). 닫힘Auto949→DOWN951/Shot953→OR966.in1/2,수동955→P957/ON959→in3/4;OR966 W908→NOT Qopen961(W909/864)→NOT Lc963(W910/865)→W964 Coil837(W912/866).

**외곽 NOT ON과 내부 ON,압력/Shot생성 및고장감시의ON은같은심볼주소를읽는다.** 이를논리의도대로교정하거나현재설비가절대동작하지않는다고단정하지않는다. 실제호출·기억상태·다른쓰기·현재프로그램이필요하다. 자동가지에는P직렬접점이없고수동가지만P OR ON을포함한다. 앞선MV01출력식을복제하지않았다.

### 3.4 엔코더·기억·환산

LAD1760 0510 NID49:NOT Simulation(1)21 W51/ORef25(0678 RID344 M180.0)→EM_OK22 W53/ORef26(RID173 I19.4)→W54 LRef23 High_Speed_Counter(0679 RID330),Instance24 MV06_Encoder(0673 RID350 DB19). SwGate W55/ORef27=SW_GATE4,CountValue W75/ORef47=ACT_CNTV4. **나머지21핀은RefId없음**이며ErrorAck/EventAck/SetCountValue도포함한다. [E12]

LAD1766 0516 NID35: [E13]

- EM_OK1529 W1503/ORef1480→W1530→NOT **raw MV06_Close**1531 W1504/ORef1481(0678 RID260 I7.0)→W1532 Coil1441 SW_GATE4(W1505/1482)와Add1446.
- Add1446:Encoder_CH04 W1506/1483+ACT_CNTV4 W1507/1484→localCNT_Act_4 W1508/1485;enoW1509→Div1450:local W1510/1486 /100 W1511/1487→CNTV4_100 W1512/1488.
- Div.enoW1513→Move1454 local W1514/1489→Encoder_CH04_10 W1515/1490. DInt→Int저장경계를유지한다.
- EM_OK→NOT SW_GATE4 Contact1533 W1517/1491→W1534:Move1463 0→CH04_10 W1518/1519;Move1468 INT#0→CH04 W1520/1521.
- EM_OK공통→Signal linearization CRef1475/CodeBlock1502(0680 RID351/0672 RID5):IN0 W1523/1497 ON,Analog_input W1524/1498 CH04_10,Coeff W1525/1499,Zero W1526/1500,OutValue W1527/1501 Pot_MV06,OFR W24/ORef23 Pot_MV06_OFR.

LAD1761 0511 NID30의 **NOT EM_OK963**→W964 Move937:localCNT_Act_4 W960/ORef949→Encoder_CH04 W961/ORef950(0676 RID204). 다른쓰기·local값수명·호출순서없이완전위치보존을확정하지않는다. [E14]

Signal linearization0291/0014의원본:입력Int가−1382초과/32767이하일때Int→DInt변환,(입력+Zero)×Coeff/28000정수계산·ENO사슬→Int OutValue. 범위밖이면Move193 −9999→OutValue,eno→일반Coil23 OFR. NOT IN0이면0014 Move162 0→OutValue. 현재계수·센서해상도·개도단위·현장해제는미확정이다. [E19]

### 3.5 공통 인버터 기동 소유와 미결속

LAD1186 0363 NID9의 NOT Contact63(W38/ORef39,RID120 미결속)→W40 Coil64→W41/ORef44 **Start Aux INV Q1.0**(0063 RID776) 쓰기를확인했다. ORef39는색인상Motors.Aux_INV.Allarme_Comulativo후보지만선언미결속이므로“어떤알람이없으면무조건기동”으로확정하지않는다. [E15]

같은0363의HMI Standard Motors CRef23/CodeBlock22:Ingresso_run W24/25/RID706,Allarme1 W28/29/125,Allarme2 W30/31/126,Risposta W42/43/118,Comulativo_allarmi W46/47/120은미결속. Allarme3/4/5 W32/34/36,ORef33/35/37은0626 RID48 FALSE. Q1.0은MV06의방향요청Q1.1/Q1.2가아니며공유기동이다.

### 3.6 공통 인버터 알람의 동일 Q 상충

LAD1821 0455 NID48:ON1816(W1806/ORef1799)→StartAux1837(W1840/ORef1838)→W41→**NOT StartAux22**(W43/ORef44)→W25. 두ORef모두0658 RID236 Output AO8=Q1.0이다. [E16]

- W25→NOT Inputs.Aux inverter RUN1818(W1807/1800)→W1819 TON LRef24.IN. PT W36/ORef37=T#2S(0656 RID311),Instance27 Aux_Inv_run DB31(0654 RID310). Q W38→S1792 Aux_Inverter_Fault W1809/ORef1801. ET W39/ORef40은미결속이다.
- 같은W25→Inputs.Aux_Inv_All1827(W34/ORef35)→W42 S1828 Aux_INV W1834/ORef1830.
- Reset공통:ON1816→RESET_ALLARM1820 W1810/ORef1802→W26. Aux_Inverter_Fault1822 AND Inputs.RUN1824→W1825 R1798 W1814/ORef1805. Aux_INV1835→W30 R1836 W28/ORef29.

Q AND NOT Q의정적상충을보존한다. 이자료만으로현재알람무효·보호우회·리셋정상완료라고판정하지않는다. 공통응답fault와공통INV입력fault는서로다른비트/Reset조건이며MV06자체fault로합치지않는다.

### 3.7 압력 원천·설정 쓰기·다른 쓰기

LAD1746 0496 NID16:ON475→Signal linearization456.en W476,IN0 W470/ORef463 ON,Analog_input W471/464 **PSH02:P**(0678 RID101 Input Peripherie AO2288=PIW286),Coeff W472/465,Zero W473/466,OutValue W474/467 Data.PSH_02(0676 RID104),OFR W24/23 PSH02_OFR(RID387). [E17]

0347은위환산값을사용하지만0348은같은원시PIW286를직접0과비교한다. Data.PSH02_SETPOINT에는0642 RID99,NID1 UID3641 Write선언도있다. 이번FlgNet검색에서상류설정식/조건본문을결속하지못했으므로쓰기값·현재레시피·우선순위는미확정이다. 0668 NID11 지역변환참조도현재제어원천완료로승격하지않는다.

정확한Pot_MV06/Inputs.AuxRUN 심볼에는기존백업simulation블록관련0635의다른쓰기참조도남아있다. 그존재만기록하고현재활성이라고주장하지않는다. 시뮬레이터는작성·변경·실행·행동시험하지않았다. 현재HMI/외부/간접쓰기전체완전성은별도자료가필요하다.

## 4 전기 전달 경로

### 4.1 공통 인버터와 기동·Reset·STO 경계 [E20]

Electrical_Rev2.pdf FG30/PDF31: 6.2 L1/L2/L3(440V60Hz) → 30QM1 → 30R1/S1/T1 → 30AS1 U1/V1/W1. 도면에는 30QM1 범위5.5–8A와 RATING6.9A, 인버터 ACS355-03E-04A1-4·1.5kW가 각각 적혀 있다. 서로 다른 표기이며 현행 설정이나 조합 적정성을 단정하지 않는다. U2/V2/W2 → 30U1/V1/W1 및30SCH1 차폐가 MV06 등 공유 분기로 이어진다.

- START: 단자9(+24V) → 30.1 → **31KA1 접점5–9** → 30.2 → 단자12(DI1 START).
- RESET: 같은+24V → **17KA2 접점5–9** → 30.7 → 단자15(DI4 RESET).
- FG31/PDF32: A1.0 → 30QM1 보조접점 → 31.1 → 31KA1 A1/A2 → −0V10.6. FG137/PDF138 MOD14 단자11이 A1.0 끝점이다.
- FG17/PDF18: A7.5(143/1 참조) → 17KA2 A1/A2 → −0V10.6. Reset 출력의 PLC 조건은 이 회로만으로 결속하지 않는다.
- STO: X1C OUT1(1)–IN1(3)은14KA2 접점1–2, OUT2(2)–IN2(4)는14KA6 접점1–2 경유. FG14/PDF15에서14KA2 코일 상류는13.5(13/4),14KA6는13.6(13/5),A2는0Vac9.9이다. FG13 상류 전체 안전 체인과 현행 안전 기능·인버터 구성은 미확정이다.
- RUNNING: 단자17에+24V10.7 공급,19→E1.4→FG117 MOD8 단자15. ALARM:20에+24V 공급,21→E1.5→MOD8 단자16. 단자22/10GND/11DCOM의−0V 연결도 보존한다. RUNNING/ALARM 글자만으로 정상 극성·고장 시 상태를 확정하지 않는다.

5–9는 실제 부하선을 확대한 렌더에서 추적했다. 하단 접점표의1/5/9 또는 사용하지 않는1번을 실제 부하 접점으로 옮기지 않는다. 이 문서는 기존1–9 문구의 정정 근거를 전달하며 원문이나 공통 코드를 변경하지 않는다.

### 4.2 MV06 고유 모터·방향 접촉기 [E21]

FG32/PDF33: 공유30U1/V1/W1 → 32QM1(인쇄 범위0.7–1A) → 32KM1/32KM2 정·역 전력 접점 → 32U1/V1/W1 → XM → 32QS1 → M14 MV06 U/V/W/PE. 모터 표기는0.25kW·0.76A이다. 보호기 인쇄 범위와 모터 정격은 현행 보호 설정값이 아니다.

- 열림: FG137 MOD14 단자12 A1.1 → 반대32KM2 NC31/32 → 32.1 → 32KM1 A1/A2.
- 닫힘: MOD14 단자13 A1.2 → 반대32KM1 NC31/32 → 32.2 → 32KM2 A1/A2.
- 공통 코일 귀로:32.3 → 32QM1 보조접점 → 32.4 → XS19 → 32QS1 보조접점 → XS20 → −0V10.6.
- 열림 응답:+24V10.7 → 32KM1 보조13/14 → E1.6 → FG117 MOD8 단자17.
- 닫힘 응답:+24V10.7 → 32KM2 보조13/14 → E1.7 → MOD8 단자18.

PLC의 반대 Q 차단과 하드웨어 반대 접촉기 NC를 구분한다. 접촉기 보조 응답은 밸브 이동량·완전 열림 증명이 아니다. 도면만으로 결선·용착·현행 동작을 확인한 것으로 기록하지 않는다.

### 4.3 끝단 스위치와 엔코더 [E22,E23]

FG33/PDF34의 열림: +24V10.7 → X1/63(2AF) → 33.5 → **LS40 NC11/12** → X1/64 → E6.7 → FG122/PDF123 MOD9 단자28. 닫힘: X1/65(2AF) → 33.6 → **LS41 NC11/12** → X1/66 → E7.0 → FG123/PDF124 MOD9 단자31. 접점 기호 NC는 원본 표시이며 현재 정상 극성의 현장 확인을 대신하지 않는다.

ZT06은 FG33에서 B(+24V)→X1/58→33.1→FG148/PDF149 단자9, C(0V)→X1/59→33.2→단자10M, D→X1/60→33.3→단자1 CH0.A, E→X1/61→33.4→단자2 CH0.B, 차폐X1/62→33SCH1이다. FG148은 MOD18 TM1 Timer이며 CH0.N 단자3은 미배선이다. E22.0/.1/.2(단자4/5/6),A10.0/.1(7/8)은 SPARE 표기다. 이를 엔코더 카운트 주소로 임의 사용하지 않는다. 물리 CH0와 소프트웨어 SW_GATE4/ACT_CNTV4의 장치 구성 매핑은 미확정이다.

### 4.4 압력 경로와 소유 상충 [E24]

FG75/PDF76: +24V → X1/175(50mAF) → 75.2 → PSH02 +; 센서− → X1/176 → PEW286; 차폐X1/177→75SCH2. P-BADR 0/10mbar·4–20mA 인쇄값을 보존한다. FG107/PDF108 MOD3 단자34 I7+가 PEW286,단자36 U7−/I7−가 공통−0V,단자44가M이다.

FG75와FG107은 이 채널에 **OUTPUT MV03**이라고 적지만 0347/0348/0496은 MV06 제어에서 PSH02/286을 사용한다. 센서의 물리 위치·공정 소유와 논리 사용처를 구분한다. 현재 계측 범위·환산 계수·영점·교정일·단위를 추정하지 않는다.

### 4.5 시공 자료와 별칭 [E25]

시공 PDF51 행1_14는 =FLB+MV06-M14A, CR→MV06 M14, DAC/PVC-S4/1.5SB,spare0,100→120RB→E900,LEN59이다. 이는 케이블 표의 설계 길이이며 실측이 아니다. PDF33 FLOW_BZONE03 route12는M14,route13은FLO4TB2→LS34/35/ZT06이다.

PDF58의 각 행을 분리하여 보존한다.

| 행 | 식별과 경로 | 규격·인쇄 길이 | 해석 경계 |
| --- | --- | --- | --- |
| 8_6 | =FLB+MV06-FLO4TB2A, CR→MV06 FLO4TB2 ZT06 | TM,CVV-S4S1.0,spare0,LEN63 | 엔코더 케이블 후보 |
| 8_17 | 동일 FLO4TB2A, UC01 FLO4TB1→MV06 FLO4TB2 LS34/35 | DC,CVV7G1.0,spare2,LEN9 | 동일 ID여도8_6과 합치지 않음 |
| 8_19 | MV06-LS34A,FLO4TB2→LS34 | CVV2C1.0,E1310,LEN3 | OEM LS40과 대응 미확정 |
| 8_20 | MV06-LS35A,FLO4TB2→LS35 | CVV2C1.0,E1320,LEN3 | OEM LS41과 대응 미확정 |
| 8_21 | MV06-ZT06A,FLO4TB2→ZT06 | CVV-S4S1.0,E1330,LEN4 | 현재 실물 확인 필요 |
| 8_10 | =FLB+UC01-PSH02A,CR→UC01 PSH02 | AI,CVV-S4S1.0,spare1,LEN55 | MV06 독점 소유로 확정하지 않음 |

PDF56 행6_6은 MV05 FLO1TB2B에 ZT06이라고 적고6_20은 MV05 ZT05다. 기존 명칭 상충을 유지한다. 이 문구만으로 MV06 ZT06을 MV05로 이전하거나 동일 센서라고 확정하지 않는다. PDF58 검게 지운8_5/8_7/8_8은 활성 배선으로 복원하지 않는다.

페이지별 개정란: FG17/30/107/117/122/123/137은 **Rev2 17.03.2025**; FG14/31/32/33/75/148은 **개정란 공란**이다. 파일명이Rev2라고 모든 페이지에Rev2를 붙이지 않는다.

## 5 알람·복구 조건

### 5.1 MV06 자체 fault와 별칭 [E09,E10]

MV_06_FAULT는 DB3.X11.6 하나의 래치다. 0159의 방향 명령 대비 응답 부재150ms와0352의 W19>2200 또는W20<−2200이 같은 비트를 Set한다. 세 조건을 서로 독립된 세 알람 비트로 세지 않는다. 0159 Reset은ON AND RESET_ALLARM AND 현재fault를 거쳐R362에 연결된다. Reset 입력이 들어갔다고 재발 원인이나 설비 복구가 해소되었다고 보지 않는다.

HMI MV06_Allarme1(DB11.X28.2)은 화면용 별도 저장 비트다. 0364 Alarm1/Risposta/Comulativo의10개 미결속 핀 때문에 DB3.X11.6→DB11.X28.2의 전체 전달을 확정하지 않는다. HMI 표시 이름을 근거로 독립 보호·알람 수를 늘리지 않는다.

### 5.2 공통/계측 이상과 구분 [E14,E16,E17]

- Aux_Inverter_Fault DB3.X17.2: 공통 RUN 부재TON2s 경로. Reset에는 RUN 조건이 더 있다.
- Aux_INV DB3.X20.0: 공통 입력 이상 경로. 앞단 동일Q AND NOT Q 상충을 유지한다.
- PSH02_OFR DB3.X22.1: 압력 환산 블록 범위 이상 출력. MV06 방향 fault와 별개다.
- Pot_MV06 OFR DB3.X25.2: 위치 환산 OFR 출력. 엔코더 하드웨어 진단 전부와 같다고 간주하지 않는다.

현재 CPU 래치/발생 이력·현재 보호기·고장 접점 극성·설정 변경·현장 리셋 결과는 없다. 본 초안에는 강제 출력, 접점 우회, 보호 설정 변경, 시뮬레이터 또는 운전 시험 절차를 넣지 않았다.

## 6 증상별 확인 자료와 수리 판단 경계

| 증상 | 정적 비교 순서·필요 기록 | 수리/복구 미확정 경계 |
| --- | --- | --- |
| 방향 명령은 있으나 움직이지 않음 | 0349 NOT ON/fault/반대Q/끝단조건→Q1.1/.2→FG137/32 코일·귀로→공유30AS1 | 현재 측정 자료 없이 PLC/인버터/접촉기 고장 단정 불가 |
| 명령 직후 MV06 fault | 0159 150ms와I1.6/.7 가공층,접촉기 보조응답 및 동일fault 다른Set 확인 | 타이머 연장·fault강제해제 제안 금지 |
| 오래 동작 후 fault | 0351 W19/W20 증감과0352±2200 비교,Reset 및 재Set 시점 | 누적 카운트는 실제 이동시간/엔코더 펄스가 아님 |
| 자동 압력 조절이 이상함 | SP≠0 환산오차±5/300ms·4s와SP=0 원시입력/20s·2s·300ms 구분 | 0원시값을0mbar로 바꾸거나 부호 교정하지 않음 |
| 끝단 표시와 실물 위치 불일치 | LS40/41 원본 NC,LS34/35 시공 별칭,DB13과HMI 미결속 경계 | 정상 극성·센서 교체·배선 역전 추정 금지 |
| 위치값이 멈추거나 튐 | ZT06→FG148 CH0.A/B→HSC 장치구성→0516 누적/환산 | 21개 미결속 HSC핀을 추정 결속하지 않음;교정 절차 미확보 |
| 공통 인버터 경보 또는 타 설비 동시 영향 | MV02/MV05/MV06 공유 경계,0363 기동 소유,0455 상충과RUN/ALL 분리 | MV06 단독 고장/독립 Reset이라고 단정하지 않음 |

필요 관찰 자료는 관찰자·시간대·장치/프로젝트 식별·값과 단위·비교 원본을 갖춰야 한다. 현재 그러한 현장 관찰을 수행하거나 운영 기록에 작성하지 않았다.

## 7 완료 기준·통합 인계

7영역 모두 문서 초안에 적용하되 근거 누락을 완료로 채우지 않는다. 이 산출물의 완료는 조사 문서 인계이며 코드 통합·UI 검증·게시 완료와 다르다.

| 구분 | 상태·조건 |
| --- | --- |
| documentation | 초안, 고유 원본/상충/자료 공백 포함. 통합자 독립 검토 필요 |
| static_review | XML/선언/핀과 실제 PDF 페이지 정적 대조. 현재 CPU 검증 아님 |
| ui_records / publication | 이번 조사에서는 미수행. 사용자/Codex 담당 |
| tia_compile / live_cpu / field_recovery | 미수행·미확정 유지 |

필수 재확인 사항: (1)0349 NOT ON의 NID9 선언과 반전핀, (2)0455 같은RID236의Q AND NOT Q, (3)150MS/T16 및±2200, (4)0348 원시PIW286와 환산값의 차이, (5)FG30 두 부하 접점5–9, (6)HSC21핀/HMI10핀 미결속, (7)LS 별칭·케이블 중복ID·PSH 소유 상충. 전체 MC04/MV01/MV03 조사 반복 대신 이 고유 핵심과 해시를 먼저 대조한다.

누락 자료: 현행 TIA 프로젝트와 CPU 업로드 일치 증거, 블록 호출 순서/실제 활성 쓰기, HSC 기술 객체 및 모듈 매핑, 미결속 HMI 참조 선언, 원시↔가공 입력의 현행 극성, 공유 인버터 파라미터/명판, 보호기 현행 설정과 현장 배선/센서 표찰, LS34/35↔40/41 대응 승인 자료, 압력 계측 범위/교정 증명. 이름·인쇄값만으로 대체하지 않는다.

2026-10-11 추가 승인에 따라 이 초안 이후 **킬른/RD01 식별·제어 조사**를 기존 순서의 다음 한 대상으로 진행한다. 우선23개 중 완료·제외를 빼고 순서대로 조사하며, 이후248개 잔여 대상도 기존 제외와 변경 금지 범위를 보존한다. 공통 대장 변경 없이 별도 조사 진행 기록에서 초안 전달과 실제 게시 완료를 구분한다.

## 부록 A 핵심 주장 근거표

Flg/Ident는 all-in-one/sources/decoded-original/의 네 자리 파일이다. PDF/CSV/index는 all-in-one/sources/다. 정확한 전체 경로와 해시는 부록 C에 연결한다.

| ID | 주장 | 원본 | 핀·선언·페이지 | 미확정 경계 |
| --- | --- | --- | --- | --- |
| E01 | P21 식별 | docs/equipment-standard/INVENTORY.json | mapping=tag,identity_verified=false;댐퍼 본체와 구동모터 관계 확인 | 태그 대응과 실물 동일성 분리 |
| E02 | P&ID | PID_1684n002I.pdf | PDF1 MV06/M14/ZT06/LS34·35/0.25kW440V | OEM LS40·41과 별칭 상충 |
| E03 | I/O·주소 | live_index.json;0617/0618/0619/0573/0063 Ident | doc494/915/495/496/657/1527;Q1.0/.1/.2;Inputs AO12~15/55/56 | 원시·가공·HMI 층 구분;현재극성 미확정 |
| E04 | 입력/호출 | 0397/0030 Flg;0627/0628/0629/0690/0691/0692 Ident | LAD1070 IW0 Move22 W23/24,IW6 Move42 W52/54;LAD1613 ENO/NOT Simulation(1) | DB13 전달·호출 경계;다른쓰기 완전성 미확정 |
| E05 | 압력 오차 | 0347 Flg;0062/0617/0618/0619/0620 Ident | LAD1709 NID7 Sub598;Ge618≥5/Le624≤−5;SD605/610 | 환산오차·300ms/4s;단위/실행주기 미확정 |
| E06 | SP0 Shot | 0348 Flg;0617/0618/0619/0620 Ident | LAD1710 NID8 Eq693/Le701/Gt715,SD707/721/735,S712/726,R741/743 | 원시PIW286≤0/>0;20s/2s/300ms;0mbar 아님 |
| E07 | 최종출력 | 0349 Flg;0617/0619 Ident | LAD1711 NID9 NOT ON915;OR965/966;C821/C837;RID1/97/98 | NOT ON과 상대Q/끝단 차단;원문 임의교정 금지 |
| E08 | 요청Reset/Auto | 0349/0149 Flg;0563/0617/0619 Ident | NOT ON915/917,R794/R801;0149 S310 W334/ORef322 | 기동Auto와 요청해제;알람Reset과 구분 |
| E09 | 응답fault | 0159 Flg;0570/0571/0572/0573 Ident | LAD1226 SD329 W486/487;Tag97T16,150MS;S334 W490,R362 W510 | 동일DB3X11.6;현행CPU/적절성 미확정 |
| E10 | 누적fault | 0351/0352 Flg;0617/0618/0619/0620 Ident | LAD1713 Add1418/Sub1433,W19/W20;LAD1714 Gt1752/Lt1766,S1758/1772 | >2200/<−2200;실제시간/엔코더펄스 아님 |
| E11 | 공유펄스 | 0350/0351 Flg;0617/0618/0620 Ident | SD1225/1230 PBox1235;T118/T119 10MS | 명령누적 에지와 작업P 구분;실제주기 미확정 |
| E12 | HSC | 0510 Flg;0673/0676/0678/0679 Ident | LAD1760 NID49 NOT Simulation21/EM_OK22,LRef23/Instance24,DB19 | 2핀 결속·21핀RefId부재;장치매핑 미확정 |
| E13 | 엔코더처리 | 0516/0511 Flg;0672/0674/0675/0676/0677/0678/0680 Ident | LAD1766 NID35 rawCloseNOT1531,Add1446/Div1450/Move1454/1463/1468;0511 Move937 | rawI7.0와 가공Inputs 구분;DInt/Int/누적 기억 경계 |
| E14 | 위치환산 | 0516/0291/0014 Flg;0611/0612/0676/0680 Ident | CRef1475 AnalogW1524/CoeffW1525/ZeroW1526/OutW1527/OFRW24 | DB1W136/DB3X25.2;현장교정 완료 아님 |
| E15 | 공통기동 소유 | 0363 Flg;0063/0623/0624/0626 Ident | LAD1186 NID9 CRef23,NOT63 W38/ORef39→C64 W41/ORef44RID776 | Q1.0공유;Comulativo RID120 미결속 |
| E16 | 공통알람 상충 | 0455 Flg;0654/0655/0656/0657/0658/0659 Ident | LAD1821 NID48 Q1837 W1840/1838 AND NOTQ22 W43/44,RID236;TON24 PT2s | 두Set경로 정적상충;현재보호무효 단정 금지 |
| E17 | 압력원천/설정쓰기 | 0496 Flg;0642/0668/0672/0674/0676/0678/0680 Ident | LAD1746 NID16 CRef456 AnalogW471/ORef464,PeripherieAO2288;0642RID99UID3641Write | PIW286환산;설정상류식 미결속 |
| E18 | HMI | hmi_plc_tags.csv;0364 Flg;0623/0624/0626 Ident | LAD1187 NID10 CRef23;MV06설정8행;14실인수4FALSE/10미결속 | 표시비트와원인비트 분리;ResetEncoder 미확보 |
| E19 | 선형화 경계 | 0291/0014 Flg;0611/0612 Ident | LAD1658/1659 Gt258/Le161,Convert/Add/Mul/Div/Move185/193/Coil23 | −1382초과/32767이하·−9999/OFR·NOTIN0;물리단위 미확정 |
| E20 | 공통 인버터 | Electrical_Rev2.pdf | FG30/31/14/17 PDF31/32/15/18;31KA1·17KA2 5–9;14KA2/6 1–2 | 부하선·접점표 구분;공유STO/Reset 소유 |
| E21 | 고유 모터 | Electrical_Rev2.pdf | FG32/PDF33,FG137/PDF138,FG117/PDF118;32KM1/2 NC31/32·보조13/14 | M14 0.25kW0.76A;현행보호설정 미확정 |
| E22 | 끝단 | Electrical_Rev2.pdf | FG33/PDF34 X1/63~66,LS40/41NC11/12;FG122/123 단자28/31 | 시공LS34/35와 대응 미확정 |
| E23 | ZT06 | Electrical_Rev2.pdf | FG33 X1/58~62→FG148/PDF149 단자9/10/1/2,CH0.A/B | SW_GATE4와 물리CH0 매핑 미확정 |
| E24 | 압력 회로 | Electrical_Rev2.pdf | FG75/PDF76 X1/175~177 PSH02;FG107/PDF108 MOD3단자34/36/44 | OUTPUT MV03 문구와MV06논리 사용 구분 |
| E25 | 시공 별칭 | Electrical_Can_Decoating_20241118.pdf | PDF33/51/56/58;1_14,8_6/17/19/20/21/10,6_6/20 | 중복FLO4TB2A·ZT05/06상충·가림행 보존 |
| E26 | 기존자료/다른쓰기 | MV06.html7종;0635 Ident;network-map.json | circuit-guide1–9 정정후보;Pot_MV06 및AuxRUN 다른쓰기참조 | 원자료 보존;기존simulation선언을 활성으로 간주하지 않음 |

## 부록 B 원본 호출 핀

### 0510 HSC LRef23

| 핀 | Wire/ORef | RefId 및 결속 |
| --- | --- | --- |
| SwGate | W55/ORef27 | 261 SW_GATE4 |
| CaptureEnable | W56/ORef28 | 원본 RefId 없음 |
| SyncEnable | W57/ORef29 | 원본 RefId 없음 |
| ErrorAck | W58/ORef30 | 원본 RefId 없음 |
| EventAck | W59/ORef31 | 원본 RefId 없음 |
| SetCountValue | W60/ORef32 | 원본 RefId 없음 |
| StatusHW | W61/ORef33 | 원본 RefId 없음 |
| StatusGate | W62/ORef34 | 원본 RefId 없음 |
| StatusUp | W63/ORef35 | 원본 RefId 없음 |
| StatusDown | W64/ORef36 | 원본 RefId 없음 |
| CompResult0 | W65/ORef37 | 원본 RefId 없음 |
| CompResult1 | W66/ORef38 | 원본 RefId 없음 |
| SyncStatus | W67/ORef39 | 원본 RefId 없음 |
| CaptureStatus | W68/ORef40 | 원본 RefId 없음 |
| CapturedValue | W69/ORef41 | 원본 RefId 없음 |
| ZeroStatus | W70/ORef42 | 원본 RefId 없음 |
| PosOverflow | W71/ORef43 | 원본 RefId 없음 |
| NegOverflow | W72/ORef44 | 원본 RefId 없음 |
| Error | W73/ORef45 | 원본 RefId 없음 |
| ErrorID | W74/ORef46 | 원본 RefId 없음 |
| CountValue | W75/ORef47 | 263 ACT_CNTV4 |
| MeasuredValue | W76/ORef48 | 원본 RefId 없음 |
| CompareMeasuredValue | W77/ORef49 | 원본 RefId 없음 |

RefId 부재는 실제 단선·FALSE·기본값이라는 뜻이 아니다. EN은 NOT Simulation(1) 및EM_OK 조건이며 현재 실행 상태는 미확정이다.

### 0364 HMI CRef23

| 핀 | Wire/ORef | 원본RefId·상태 |
| --- | --- | --- |
| Ingresso_run_Opening | W24/ORef25 | RID705 선언 미결속 |
| Ingresso_run_Closing | W26/ORef27 | RID704 선언 미결속 |
| Allarme1 | W28/ORef29 | RID156 선언 미결속 |
| Allarme2 | W30/ORef31 | 0626 RID20 FALSE |
| Allarme3 | W32/ORef33 | 0626 RID20 FALSE |
| Allarme4 | W34/ORef35 | 0626 RID20 FALSE |
| Allarme5 | W36/ORef37 | 0626 RID20 FALSE |
| Limit_switch_Open | W42/ORef43 | RID703 선언 미결속 |
| Limiti_Switch_Close | W44/ORef45 | RID702 선언 미결속 |
| Risposta_Opening | W50/ORef51 | RID150 선언 미결속 |
| Risposta_Closing | W52/ORef53 | RID152 선언 미결속 |
| Limit_Switch_Open_HMI | W54/ORef55 | RID144 선언 미결속 |
| Limit_Switch_Close_HMI | W56/ORef57 | RID146 선언 미결속 |
| Comulativo_allarmi | W62/ORef63 | RID148 선언 미결속 |

### 타이머 적용 구분

| 대상 | 원본 값/주소 | 근거 |
| --- | --- | --- |
| 자체 방향응답 | 150MS/Tag97 T16 | 0159 SD329,0571 RID8 |
| 비영점SP 비교허가 | 300MS/Tag150 T136,4S/Tag149 T135 | 0347 SD605/610 |
| 영점SP 닫힘/열림 Shot | 20S/Tag151 T140,2S/Tag152 T143 | 0348 SD707/721 |
| Shot 해제 | 300MS/Tag153 T141 | 0348 SD735 |
| 공유 누적펄스 | 10MS/Tag156 T118,Tag157 T119 | 0351 SD1225/1230 |
| 공유 인버터 RUN 응답 | TON PT2S,Aux_Inv_run DB31 | 0455 LRef24/Instance27;동일Q 상충 앞단 |

모든 값은 백업 원문이다. 현행 보호 설정·권장값·실제 경과 시간으로 전환하지 않는다.

## 부록 C 고정 원본 SHA-256 83개

커밋 abcf31c5030bc7ef8749ed8e869a857f2387a28a에서 계산했다. ZAP18/PLF는 보존 기준 해시이며 TIA 실행/컴파일을 뜻하지 않는다. 해시 일치는 현재 CPU 일치나 모든 기능 검증을 뜻하지 않는다.

| 전체 원본 경로 | SHA-256 |
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
| [all-in-one/sources/decoded-original/0149-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0149-FlgNet.xml) | bc2519cdad49a7268006b194e8e5e1160744ff221f04b83e710f31f57bc617f9 |
| [all-in-one/sources/decoded-original/0159-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0159-FlgNet.xml) | 5598abbad86ed26fa8dd17fc3eca3e1c0b7941a2798db6ae1e2472a7ca448d2a |
| [all-in-one/sources/decoded-original/0291-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0291-FlgNet.xml) | fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550 |
| [all-in-one/sources/decoded-original/0347-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0347-FlgNet.xml) | 092aa32263fce728afde49d5fff0dddb6cc1445c6f71e4fb45956129beda4d6d |
| [all-in-one/sources/decoded-original/0348-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0348-FlgNet.xml) | 00570dd8c0945f04304c8820b8e3d7294916aa04aaa1158d1c630062961bbedf |
| [all-in-one/sources/decoded-original/0349-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0349-FlgNet.xml) | 2f45af21543189d83f027afbae797532cae5d55935bac1fba3913825d741863b |
| [all-in-one/sources/decoded-original/0350-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0350-FlgNet.xml) | 3f426a4ba9455160b8113df968b1052752a7b72cdfca8e57bdfd466340d691ff |
| [all-in-one/sources/decoded-original/0351-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0351-FlgNet.xml) | 1448cd179747074ae5ac3647c52e47950d18e0d90fa2f1cb155dbb24af50a7f6 |
| [all-in-one/sources/decoded-original/0352-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0352-FlgNet.xml) | 03e2d68dda289fcb7e7738c2f52e675890b252f5b526cab1ec2049323ab30d75 |
| [all-in-one/sources/decoded-original/0363-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0363-FlgNet.xml) | 90fc22646d834bfd3139806680e708b449798516cf0d7c0c65eaf86a2ab80d5a |
| [all-in-one/sources/decoded-original/0364-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0364-FlgNet.xml) | c23a9952251a48105eedd1ed3c185f781b6163d094fb3bb396ac27415587de8a |
| [all-in-one/sources/decoded-original/0397-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0397-FlgNet.xml) | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 |
| [all-in-one/sources/decoded-original/0455-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0455-FlgNet.xml) | 4d49d7acd2ef56ecb47252305453bae589897ab69315fc0cef32e1e156da1325 |
| [all-in-one/sources/decoded-original/0496-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0496-FlgNet.xml) | 9a5c816b27efc2afbe84a170b1f80959c4992829d10eaa55f6bd18f28030808a |
| [all-in-one/sources/decoded-original/0510-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0510-FlgNet.xml) | 0e755f251ab92f2b1904be6812b4995ba04285f99de068b8bc794d31c1cee0dd |
| [all-in-one/sources/decoded-original/0511-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0511-FlgNet.xml) | a4bf314bf817f0f666a0c9fdd26df134cedeed8666819c7a3e8e6438850eace6 |
| [all-in-one/sources/decoded-original/0516-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0516-FlgNet.xml) | 382738875d4fe8ebcf38f878eafd6486047e3cdd6de7a98bebcafc2afd124c8f |
| [all-in-one/sources/decoded-original/0062-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0062-IdentXmlPart.xml) | 34f188168dc4fad0d6e2c813028045f37b84025636bcebd8aa1c7ffb4cfd9bcd |
| [all-in-one/sources/decoded-original/0063-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0063-IdentXmlPart.xml) | 9dceae18963ead11293cfc3a70c2eac077faa53ebd28e23bb4e84bc3278c5034 |
| [all-in-one/sources/decoded-original/0555-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0555-IdentXmlPart.xml) | 46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6 |
| [all-in-one/sources/decoded-original/0563-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0563-IdentXmlPart.xml) | 86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad |
| [all-in-one/sources/decoded-original/0570-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0570-IdentXmlPart.xml) | 9fed133006458c3b43b1d5f2c15107a5a86b4fb7cdbaf3743bf88f0e5a105495 |
| [all-in-one/sources/decoded-original/0571-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0571-IdentXmlPart.xml) | 4a9deeb65a22e497e284fe6d98929e1d201ef5939e4aeca5805b4eb7e007d398 |
| [all-in-one/sources/decoded-original/0572-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0572-IdentXmlPart.xml) | 5ecd18f84e12d702bb46f759b23994dacfa2d97d50fe51e766ca0cf43f75bb4c |
| [all-in-one/sources/decoded-original/0573-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0573-IdentXmlPart.xml) | a22cc24a974e0c792f32e356a14b277a847e2bb204c91bce01c37d1714ddb56c |
| [all-in-one/sources/decoded-original/0611-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0611-IdentXmlPart.xml) | 0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089 |
| [all-in-one/sources/decoded-original/0612-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0612-IdentXmlPart.xml) | 95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38 |
| [all-in-one/sources/decoded-original/0617-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0617-IdentXmlPart.xml) | 10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9 |
| [all-in-one/sources/decoded-original/0618-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0618-IdentXmlPart.xml) | 0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c |
| [all-in-one/sources/decoded-original/0619-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0619-IdentXmlPart.xml) | 85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456 |
| [all-in-one/sources/decoded-original/0620-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0620-IdentXmlPart.xml) | da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3 |
| [all-in-one/sources/decoded-original/0623-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0623-IdentXmlPart.xml) | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 |
| [all-in-one/sources/decoded-original/0624-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0624-IdentXmlPart.xml) | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a |
| [all-in-one/sources/decoded-original/0626-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0626-IdentXmlPart.xml) | a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b |
| [all-in-one/sources/decoded-original/0627-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0627-IdentXmlPart.xml) | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| [all-in-one/sources/decoded-original/0628-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0628-IdentXmlPart.xml) | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd |
| [all-in-one/sources/decoded-original/0629-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0629-IdentXmlPart.xml) | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| [all-in-one/sources/decoded-original/0635-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0635-IdentXmlPart.xml) | 1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457 |
| [all-in-one/sources/decoded-original/0642-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0642-IdentXmlPart.xml) | c922483c261c8ddb98c239a7b4dc3d7f73f9a45261dd5b4d669f39d6918a1c21 |
| [all-in-one/sources/decoded-original/0654-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0654-IdentXmlPart.xml) | b36294f3aad24be72a052bef61c875ca4695d7e101c385cf55bdadec41d5097e |
| [all-in-one/sources/decoded-original/0655-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0655-IdentXmlPart.xml) | 38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb |
| [all-in-one/sources/decoded-original/0656-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0656-IdentXmlPart.xml) | 0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592 |
| [all-in-one/sources/decoded-original/0657-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0657-IdentXmlPart.xml) | 0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b |
| [all-in-one/sources/decoded-original/0658-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0658-IdentXmlPart.xml) | 998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831 |
| [all-in-one/sources/decoded-original/0659-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0659-IdentXmlPart.xml) | ec881805a45730533bccd780e152afb9c9d7c7c45ba7587538b92239f9cbd9d2 |
| [all-in-one/sources/decoded-original/0668-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0668-IdentXmlPart.xml) | 2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed |
| [all-in-one/sources/decoded-original/0672-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0672-IdentXmlPart.xml) | 6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222 |
| [all-in-one/sources/decoded-original/0673-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0673-IdentXmlPart.xml) | 450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58 |
| [all-in-one/sources/decoded-original/0674-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0674-IdentXmlPart.xml) | 4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84 |
| [all-in-one/sources/decoded-original/0675-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0675-IdentXmlPart.xml) | b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3 |
| [all-in-one/sources/decoded-original/0676-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0676-IdentXmlPart.xml) | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 |
| [all-in-one/sources/decoded-original/0677-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0677-IdentXmlPart.xml) | 69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3 |
| [all-in-one/sources/decoded-original/0678-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0678-IdentXmlPart.xml) | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 |
| [all-in-one/sources/decoded-original/0679-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0679-IdentXmlPart.xml) | d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56 |
| [all-in-one/sources/decoded-original/0680-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0680-IdentXmlPart.xml) | fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95 |
| [all-in-one/sources/decoded-original/0690-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0690-IdentXmlPart.xml) | fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541 |
| [all-in-one/sources/decoded-original/0691-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0691-IdentXmlPart.xml) | 17cb7d9734d76b39e729e0daf0c89d9bdf74907aab2130c80453fa04e4cea1da |
| [all-in-one/sources/decoded-original/0692-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0692-IdentXmlPart.xml) | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| [all-in-one/devices/MV06.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/devices/MV06.html) | 204f59cb6903e0985e572a3a5144c835cb0a5721c5c0f0749c9a9e448b1c1726 |
| [all-in-one/control-specs/MV06.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/control-specs/MV06.html) | 74123566109b8d2c2bd6dda0fda541b8d2a0c6bd9ed55264bd31f97aab7ae326 |
| [all-in-one/alarm-guides/MV06.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/alarm-guides/MV06.html) | 97f161b726d427bed039b1fb091028a91b12553da0cbd8d605b362d260298032 |
| [all-in-one/circuit-guides/MV06.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/circuit-guides/MV06.html) | d9d3b1af653adac9c3529a4cbbbf304ee96945749e76d82f74907fc4477325d7 |
| [all-in-one/signal-guides/MV06.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/signal-guides/MV06.html) | 1f442d3e3ab0a2a2fd63d9f2aec5681d45723608c05560b3ba575a408e13858a |
| [all-in-one/construction-guides/MV06.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/construction-guides/MV06.html) | 3a0b089f58658ed39392e3bcbc97dc2da2fb835fdb1983367ed2329967aa91ca |
| [all-in-one/procedures/MV06.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/procedures/MV06.html) | 84a4334dde811d9e0d0456024379de1a0fe39688e3cc1c9c471e6dcfc004ed4e |

## 부록 D 수행·보존 기록

수행 범위는 고정 공개 원본 읽기, XML 정적 파싱 및 선언·Part/Wire/ORef 대조, PDF 지정 페이지 렌더와 시각 확인, 자체 Markdown 작성과 SHA-256 계산이다. 원본 worktree·공통 코드·버전·대장·배포·운영 기록은 수정하지 않았다. 프로젝트 생성기·시뮬레이터·행동시험·TIA·실제PLC·현장·보호값 변경은 수행하지 않았다. 별도 자체 진행 기록은 초안과 사용자/Codex 게시 완료를 분리한다.

