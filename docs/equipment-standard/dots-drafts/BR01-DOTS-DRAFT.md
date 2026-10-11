# BR01(P11) 외부 버너 인터페이스 — Dots 원본 조사·문서 초안

- 조사 기준: esp6662266/gme-plc-manual, main/all-in-one, 고정 abcf31c5030bc7ef8749ed8e869a857f2387a28a/v1.12.0. 2026-10-11 KST. BR01 게시 버전이나 현재 CPU 기준이라는 뜻은 아니다.
- Dots 자체 환경에서 직접 조사·작성했다. 사용자가 유일한 로컬 코드 편집·검증·게시 담당이다. 이번 산출물은 설비 문서와 근거 인계용이다.
- 공개 GME-STD-1.0.0, rollout SKILL, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY를 적용했다. tia-equipment-alarm-trace 스킬은 확보하지 못했으며 권한을 확장하지 않았다. 원본 XML/선언/핀과 실제 PDF 렌더를 대조했다.
- 원자료·기존 완료·미확정을 보존했다. 공통 코드·버전·대장·배포·운영 기록, 시뮬레이터 작성/수정/생성/실행/행동시험, 실제 PLC·현장·보호값·별도 SEJIN 변경은 없다.

## 핵심 경계와 발견 사항

1. **이 자료는 GME PLC와 외부 버너반 사이 인터페이스다.** FG97/100이 요구하는 전용 도면010-390 TYPE BP N300의 내부 점화·화염 감시·가스 밸브 안전 회로는 확보하지 못했다. 일반 PLC 순서를 제조사 연소 안전 시퀀스로 대체하지 않는다.
2. Inputs.FC GAS Chiuso(DB13.X17.3)와 FC Aria chiusa(DB13.X17.5)는 논리에서 닫힘처럼 사용되지만, 대응 원시 I17.3/I17.5의 FG97 표시는 **가스/공기 최소 압력**이다. Word 복사 경로와 다른 쓰기를 함께 보존하고 실제 의미를 확정하지 않는다.
3. 원격 Q6.5,고화염 Q7.0,점화 전환 Q7.1,PLC 내부 Start Burner/Enable/Flag는 다른 변수다. 이름만으로 화염 확인·안전 허가·실물 상태를 동일시하지 않는다.
4. 세정0184에는 **NOT MV03 Close AND MV03 Close**, State5에는 **MV03 Close OR ON**, State77 별도 가지가 있다. 원문을 정상적인 순서로 교정하지 않는다.
5. 0183과0184가 같은 Tag142/T32 및 BR01_CleanTime을 쓴다. 실제 시간·현재 호출 순서가 확인되기 전에는 화면 숫자를 검증된 세정 시간이라고 부르지 않는다.
6. FG99/143 점화 전환 제목은3초,0179 원본 타이머는4초다. 22/24시간 가지0177은OFF(M0.1) 앞단을 가진다. 현재 보호 동작·권장값을 추정하지 않는다.
7. FG99의99KA1~4 부하 접점은 **5–9**다. 99KA5는1/5/9가 모두 사용하는 전환 회로이므로 같은 방식으로 단순화하지 않는다.
8. Air 출력배율272와Gas285가 다르며 가스 출력 읽기에는 Peripherie/일반 Output 접근 차이가 있다. 숫자를 통일하거나 보호·비율 설정을 변경하지 않는다.
9. HMI0395의4개 ORef가 미결속이다. 시공 BR01F 두 행도 중복 여부 미확정으로 보존한다.

## 1 설비와 자료 기준

### 1.1 식별·본체·제어 소유 [E01,E02]

INVENTORY P11의 BR01은 tag 대응이며 identity_verified=false다. P&ID PDF1은 BR01을 AB01 쪽 버너로 표시하고 “FEED BURNER SEE DWG N°35602201_00”를 참조한다. OEM Electrical_Rev2.pdf FG97/100은 외부 버너 전용반010-390 TYPE BP N300을 참조한다. 서로 다른 문서 번호를 같은 판본으로 합치지 않는다. 실제 제작 모델·제어기 형식·현장 동일성은 미확정이다.

시공 자료의 CR→CC01/BR01 표기는 케이블 도착 위치 자료다. 이를 AB01과CC01 본체의 동일성이나 버너 소유 변경의 근거로 삼지 않는다. 외부 버너반, GME PLC 인터페이스, 주변 FN01/FN02/FN03/FN04/FN06/RD01/MV03의 연동을 분리한다.

### 1.2 보존한 기존 자료와 누락

BR01 devices/control-specs/circuit-guides/signal-guides/construction-guides/procedures 6개 HTML 및 registers/burner-interface.json의 기존 내용은 보존했다. 이 고정점에는 alarm-guides/BR01.html이 없다. 기존 생성 요약은 위치를 찾는 색인으로 활용하고 핵심 주장은 decoded-original로 확인했다. 기존 시뮬레이션 페이지/원본이 있더라도 실행·수정·생성하지 않았다. [E26]

### 1.3 근거 표기

Flg/Ident 네 자리 번호는 all-in-one/sources/decoded-original/NNNN-FlgNet.xml 또는 NNNN-IdentXmlPart.xml이다. LAD는 network-map document_id, NID는 선언 네트워크 식별자다. UID(Part/Wire/ORef)와 RID(선언)를 구분한다. PDF/CSV/index는 all-in-one/sources/다. 부록의 전체 경로·고정 링크·해시와 함께 읽는다. UID/RID만 같아도 다른 블록 선언이면 결속하지 않았다.

## 2 I/O·HMI·선언

### 2.1 디지털 상태·명령 [E03,E04]

| 대상 | 백업 주소·근거 | 해석 경계 |
| --- | --- | --- |
| Brurner Lock Out | 0582 RID3 Input AO137=I17.1 | 0171이 직접 원시 입력 사용 |
| Burner ON and OK | 0582 RID65 Input AO138=I17.2 | 0178에서 원시/가공 입력을 각각 사용 |
| Burner ON | live_index doc906 I17.0;처리0585 RID227 AO136=DB13.X17.0 | 동명 raw SimpleAccess 결속 미확보 |
| Inputs.FC GAS Chiuso | 0585 RID223 AO139=DB13.X17.3 | 도면 I17.3 최소 가스 압력과 명칭 상충 |
| Inputs.FC Aria chiusa | 0585 RID224 AO141=DB13.X17.5 | 도면 I17.5 최소 공기 압력과 명칭 상충 |
| Inputs.Burner ON and OK | 0585 RID232 AO138=DB13.X17.2 | 가공 상태;현재 극성 미확정 |
| Inputs.High Flame Gas | 0585 RID229 AO143=DB13.X17.7 | 외부 고화염 밸브 상태 접점;실제 화염 검출과 동일하지 않음 |
| Rem. Start/Stop Burner | 0582 RID94 Output AO53=Q6.5 | 0182 Coil611→99KA1 |
| Temperature Interlock OK | 0582 RID26 Output AO54=Q6.6 | 0173 Coil150→99KA2 |
| Rst allarm Burner | 0582 RID16 Output AO55=Q6.7 | 0171 Coil149→99KA3 |
| Start High Flame | 0582 RID66 Output AO56=Q7.0 | 0178 Set/Reset→99KA4 |
| Foced Spark | 0582 RID79 Output AO57=Q7.1 | 0179 Coil477→99KA5 전환 |

FG97/98의8개입력은I17.0~I17.7이며 도면 기능과끝점은§4에 따로 적는다. 백업 주석의옛E44/A56 주소는 현재백업Address 대신 사용하지 않는다.

### 2.2 내부 명칭을 합치지 않기 [E05]

| 심볼 | 원본 선언과 주소 | 구분 |
| --- | --- | --- |
| ON / OFF | 0582 RID1/80 Memory AO0/1=M0.0/M0.1 | 이름이지 참/거짓 상수가 아님 |
| Flag.Start_Burner | 0585 RID19 AO42=DB2.X5.2 | 운전 요청 |
| Start Burner | 0582 RID144 AO387=M48.3 | 세정 순서의 후단 상태 Coil |
| Enable start burner(1) | 0582 RID92 AO384=M48.0 | FN03 응답 경유 준비 |
| Enable start burner | 0582 RID93 AO386=M48.2 | 0184 순서에서 Set/Reset |
| Lock Burner | 0582 RID89 AO224=M28.0 | 별도 래치 |
| Flag.AUTO_BURNER | 0585 RID147 AO35=DB2.X4.3 | 자동 요청 |
| Flag AutoBurner | 0582 RID149 AO120=M15.0 | PID 결과 전달 허가 |
| Main flame ON | 0582 RID76 AO200=M25.0 | 점화 전환 기억;실제 화염 증거 아님 |
| Programmed stop burner | 0582 RID54 AO9=M1.1 | OFF 앞단 1440 비교 결과 |
| m491 | 0582 RID9 Memory AO81=**M10.1** | 이름 m491을M49.1로 해석하지 않음 |
| APP M10.2 | 0582 RID4 AO82=M10.2 | Reset 뒤 억제 기억 |
| Open MV03 for washing / Close MV03 for Burner Startup | 0582 RID101/238 AO385/1445=M48.1/M180.5 | MV03 방향요청과제어소유 연계 |
| Flag.Burner_ready | 0585 RID34 AO41=DB2.X5.1 | GME 연동 준비 조건;외부 안전완료가 아님 |
| BR01_State / BR01_CleanTime | 0585 RID100/97 AO176/192=DB6.DBW22/24 | 순서/표시 시간 누적 |
| WorkData.W5 / Burner_PID_Result | 0585 RID48/152 AO80/96=DB6.DBW10/12 | 운전분누적/PID 전달값 |
| Data.Burner_Panel_SetPoint | 0585 RID71 AO176=DB1.DBW22 | 여러 네트워크가 쓰는 요청값 |

0584의DepDB TOD에서Allarm=3,Flag=2,WorkData=6,Data=1,Stechio=5,Inputs=13을 확인했다. 같은 이름·offset을 다른DB와 합치지 않았다.

### 2.3 입력 전달·별칭 상충 [E04]

0397 LAD1070 NID1의Move62.in W76/ORef67은0627 RID23 Tag275 Input Word AO128=IW16, out1 W77/ORef68은0629 RID24 Word AO128/BAD4,0628 RID4 Inputs TOD13→DB13.DBW16이다. 이Word에I17.3/.5가포함된다. 도면최소압력과논리닫힘표현사이의상충을숨기지않는다.

0635 NID14에는Inputs.FC Aria chiusa RID224 UID28 Write,FC GAS Chiuso RID225 UID32 Write의기존simulation관련참조가있다. 현재활성/극성을추정하지않는다. main0030의ENO 및NOT Simulation(1) M180.0 호출경계를보존하고다른쓰기완전성은미확정으로남긴다.

### 2.4 아날로그와HMI 층 [E06,E07]

원시서보위치BR01_GAS PIW360/BR01_AIR PIW362,가스/공기유량 PIW364/366과,최종가스/공기설정 PQW308/310을구분한다. 0502~0505는별도계수·영점으로Data.GAS_BR_01/AIR_BR_01/MASSICO_FLOW_GAS/MASSICO_FLOW_AIR을생성한다. 현재물리단위/실제위치/질량유량범위·교정은미확정이다.

0398 LAD1071은raw Move170(W187/ORef176→W189/177)로DB13.INT76 가스재전송,Move171(W190/178→W191/179)로INT78 공기재전송,Move84(W132/180→W156/192)로INT80 가스유량,Move194(W196/198→W197/199)로INT82 공기유량을쓴다. 환산Data값과HMI원시값은같은층이아니다.

HMI CSV의BR01관련설정은10행이다: RESET_BURNER_COUNT DB41.X50.1,BR_01 HighFlame DB11.X84.0,BurnerON DB11.X84.1,Flag DB2.X5.2,Auto DB2.X4.3,Burner_ready DB2.X5.1,재전송GAS/AIR DB13.INT76/78,질량유량GAS/AIR DB13.INT80/82. 실제권한·버튼이벤트·온라인표시는확정하지않는다.

0395 LAD1219 hmi BR01은Contact23 operand W22/ORef24RID781→Coil27 W26/ORef28RID783,Contact30 W29/ORef31RID784→Coil34 W33/ORef35RID785의두가지다. **4개ORef 모두해당선언미결속**이다. 생성색인의표시명만으로네개의원본변수를확정하지않는다.

## 3 제어 구조·요청 소유·상충

### 3.1 GME 준비·정지·최종 원격 출력 [E08,E09]

0174 LAD1857 NID4:ON207(W194/ORef183)→NOT MAX_MAX_TC09209(W195/184)→NOT BURNER_START_FAULT211(W196/185)→NOT BURNER_LDU_FAULT213(W197/186)→FN01 Run23(W22/24)→FN04 Run27(W26/29)→RD01 run32(W31/33)→[FN06 feedback36(W35/37) OR Burner On228(W231/229)]→OR38.outW46→FN02 Run40(W39/41)→Coil182 W206/ORef193 Flag.Burner_ready다. 준비조건에들어간각처리응답과물리정상은구분한다. 이네트워크를버너내부가스/화염안전허가전체로부르지않는다.

0175 LAD1858 NID5:ON273(W251/233) 아래 OR213의조건은NOT Ready275,MAX_MAX_TC09277,START_FAULT279,LDU_FAULT281,그리고12개알람OR219→ON305(W268/249)이다. OR219는FN03_FAULT,SERVOMOTOR_MIN_POS_ALL,MAX_TC04_TEMP,MAX_TC05_TEMP,MAX_MAX_TC03_TEMP,MAX_MAX_TC01_TEMP,RO01_Signal_Fault,TC01_TC02_COMP_FAULT,Low_Aspiration,PSL_AIR_LOW,HYDROGEN_BOX_FAULT,EmergencyStopTC1_2다. OR213.outW270→R232,operandW272/ORef250 Flag.Start_Burner. ON305를Data라는동일RID타블록후보로오결속하지않았다.

0182 LAD1866 NID12는**Flag.Start_Burner634 AND NOT Lock Burner636**으로시작한다. 여기앞에ON을임의추가하지않는다. 분기1은NOT FN03요청638 AND OFF640→S600 FN03요청(W626/616). 분기2는FN03 Run642(W627/617)→Coil607 Enable start burner(1)(W628/618),그리고Enable start burner644(W629/619)→Coil611 Q6.5(W631/620)다. FN03요청·응답·두Enable과Q6.5의제어소유를분리한다.

### 3.2 Lock Burner의정적Set/Reset [E10]

0181 LAD1865 NID11:ON630→[(OFF632 AND(MAX_TC01_TEMP634 ORMAX_TC03_TEMP636)) OR Programmed stop burner638]→[(Data.GAS_BR_01≤30 Le573) OR(FC GAS640 AND FC Aria642)]→S579 Lock(W620/ORef598).

별도Reset가지:ON630→[(NOT MAX_TC01_TEMP644 AND NOT MAX_TC03_TEMP646) OR **ON648**]→NOT Programmed stop burner650→R588 Lock(W628/603). ON병렬가지를삭제하지않는다. 같은래치Set/Reset의현재호출·실행우선순위·현장정지상태는미확정이다. FC닫힘이라는내부명칭은§2.3의최소압력도면과상충한다.

### 3.3 세정·MV03 제어 소유 [E11]

0184 LAD1868 NID14의공통ON1634(W1476/ORef1366),Enable1분기와State조건을확인했다. WorkData.BR01_State는0585RID100 DB6W22다. 다음은원본정적전이이며제조사퍼지절차·안전시간으로해석하지않는다.

| 가지/State | 원본 명령·핀 | 해석·미확정 |
| --- | --- | --- |
| NOT Enable1 | Contact1636→Move1122 State0 W1479/1369;R1127 Open W1480/1370;R1130 Enable W1481/1371 | 상태초기화와방향요청분리 |
| 같은NOT Enable1가지 | NOT Close Contact28 W37/ORef38 AND Close1670 W33/ORef34→S1669 Close W25/26 | 두Close는0585RID233 동일DB13X7.6. 상충을보존 |
| 0 | Eq1137;PID_Ref_Temp≥500.0 Ge1143→Move1146 State7;<500.0 Lt1151→Move1154 State1;Move1159 CleanTime0 | 백업비교값이며현장허용온도아님 |
| 1 | Eq1164→OFF1640경유Move1171 Max_PRC_BR1→PanelSP;S1176 Open;Move1179 State2 | OFF앞단을현재불능으로단정하지않음 |
| 2 | Eq1184→**NOT** Inputs.MV03 open1642→Move1188 State3 | 반전을원문대로유지 |
| 3 | Eq1193→SD1199 4M Tag143/T31;Tag142경유Add1208 CleanTime+1;NOT Tag142→SD1215 1S T32;Tag143→Move1220 State4 | 세정표시와실제안전퍼지분리 |
| 4 | Eq1225→OFF1652경유Move1232 PanelSP0;R1237 Open;Move1240 State5 | 각명령의조건경계를유지 |
| 5 | Eq1245→Close1654 **OR ON1656**→OR1248→Move1251 State6 | 닫힘확인만기다리는가지로고쳐쓰지않음 |
| 6 | Eq1256→SD1262 1S Tag144/T37→Move1267 State7 | 현재경과시간미확정 |
| 77 | Eq1272 **literal77**→Oxigen_RO01≥60 Ge1278이면State7,<60 Lt1286이면State0 | 7과77구분;진입쓰기/현재단위미확정 |
| 7 | Eq1294→S1300 Enable,R1303 Open,S1306 Close,Move1309 State8 | MV03구동부와버너순서소유연계 |
| 8 | Eq1314 AND BurnerOn1660→Move1318 State9 | 외부상태접점과화염안전완료구분 |
| 9 | Eq1323→SD1329 30S Tag145/T38→Move1334 State10 | 현재안전시간으로승격하지않음 |
| 10 | Eq1339→Move1342 State11 | 정적순서 |
| 11 | Eq1347 AND BurnerOn1664→Coil1354 Start Burner M48.3;NOT BurnerOn1666→Move1358 State0;Move1363 CleanTime0 | PLC기억값과실제화염구분 |

NOT Close와Close 직렬은논리상동일값상충이다. 현재CPU·다른쓰기·실행상태검증없이보호가무효라고단정하거나제거하지않는다. MV03최종방향Q는해당설비의별도제어가지에서확인해야한다.

0183 LAD1867 NID13도ON653→Tag142655→Add625 CleanTime+1(W645/636,W646/637,W647/638),NOT Tag142657→SD632 1S(W648/639),operandW651/641 Tag142를쓴다. **T32와CleanTime의다른쓰기**가0184와겹친다. 실제누적시간/호출순서·활성블록을확인하기전한네트워크만으로실제세정시간을산출하지않는다.

### 3.4 고화염과점화 전환 [E12,E13]

0178 LAD1862 NID8,ON549 아래Add409 TC01_SETPOINT+20→App00,Add415 SETPOINT+15→App01이다. NOT처리Inputs.Burner ON and OK551→R422 Q7.0. 별도의**raw I17.2** Contact553 아래현재HighFlame555가있고,[(ON557 AND PID_Ref_Temp≥App00 Ge432) ORMAX_TC01559 ORMAX_TC03561]이면Move441 PanelSP0,FCgas563 ANDFCair565→SD448 **50MS** Tag139/T29,Tag139567→R453 Q7.0다.

raw I17.2 아래NOT HighFlame569 AND PID_Ref_Temp<App01 Lt457 AND NOT MAX_TC01571 AND NOT MAX_TC03573→SD465 **8S** Tag140/T12,Tag140575→S470 Q7.0다. 두온도오프셋·원시/가공입력·타이머·Set/Reset을따로남긴다. 이값을현장튜닝권고로사용하지않는다.

0179 LAD1863 NID9:ON521 AND Inputs.Burner On523 AND HighFlame525→S464 Main flame ON M25.0. 같은BurnerOn아래NOT HighFlame527 AND Main flame529→SD472 **S5T#4S**(W507/ORef492),Tag141/T122(W508/493). NOT Tag141531→Coil477 Q7.1(W511/495),Tag141533→R481 Main flame. NOT BurnerOn535→R485 Main flame다. FG99/143 제목의3초와원본4초를병기하고숫자를맞추지않는다. 이M25.0은화염검출기신호로대체할수없다.

### 3.5 자동변조·요청 제한·복수쓰기 [E14,E15]

0186 LAD1870 NID16의제목에는FB41 PID가있지만본문은허가/0쓰기다. ON1218 AND AUTO_BURNER1220 AND NOT MAX_TC011222 AND NOT MAX_TC031224 AND NOT ProgrammedStop1226 AND StartBurner1228 AND Inputs.HighFlame1230→Coil1172 Flag AutoBurner M15.0. 병렬OR1175는NOT Enable1,MAX_TC01,MAX_TC03,ProgrammedStop,NOT HighFlame이며Move1181로PanelSP0을쓴다.

0187 LAD1871 NID17 FlagAutoBurner1188→Add1176 WorkData.Burner_PID_Result+0→PanelSP(W1187/ORef1183). 실제PID원천은다른쓰기와결속해야한다. 0416 LAD1721은**OFF**앞단에서Manual에따라Move165 I_FFWD 또는Add171 I_Outvalue+0를WorkPIDResult에쓴다. 0023 LAD1722는ON186→Add174 I_Outvalue+0→같은WorkPIDResult다. 두원천의활성·주기·실행우선순위를미확정으로유지한다.

0188 LAD1872 NID18 ON1350 아래 (a)BurnerOn1352 AND PanelSP>Max_PRC_BR1→Move1265 Max값,(b)PanelSP>100→Move1273 100,(c)RemoteQ6.5 AND PanelSP<0→Move1282 0,(d)[(NOT RemoteQ6.5 AND PanelSP**≤0**) OR NOT Enable1]→Move1294 0이다. 원격OFF라는이유만으로항상0출력이라고요약하지않는다.

0417 LAD1724 NID5 ON273에서PanelSP>AirOut이면Add233 AirOut+1,PanelSP<AirOut이면Add242 AirOut−1이다. 블록이름“ogni1s”만으로현행1초당변화율을확정하지않는다.

### 3.6 아날로그배율·가스보정 경계 [E16,E17]

0467 LAD1686 NID8 ON582:AirOut<0 Lt520→Move5230,>100 Gt528→Move531100,병렬Mul536 AirOut×**272**→local Calcolo_Aria,ON584→Move543→BR01_AIR_SP W580/ORef560(0664RID61 Output Peripherie AO2480=PQW310).

0468 LAD1687 NID9 ON626:GasOut<0 Lt573→Move5760,>100 Gt581→Move584100,ON628→Mul590 GasOut×**285**→BR01_GAS_SP W624/ORef606(0664RID67 Output Peripherie AO2464=PQW308). ENO W23→Move22는BR01_GAS_SP W24/ORef26(0664RID109 **SAM=None**,같은AO2464)를읽어test_out W25/ORef27(0663RID110 InterfaceAccess AO208)에쓴다. 주변장치직접쓰기와일반Output읽기를같은현재값이라고단정하지않는다. test_out은별도물리Q라고만들지않는다.

0502~0505의선형화는각채널고유계수/영점을사용한다. 0504가스유량은환산뒤별도Lt666<1이면Move669로1을Data.MASSICO_FLOW_GAS에쓴다. 0505공기유량에같은보정을복제하지않는다. 하한1표시는실제최소유량이나OFR정상화를증명하지않는다.

0194 LAD1830은AirOut의구간비교에따라Stechio.Gas_crv*를Portata_Presunta_GAS에쓰는이론곡선참조다. 실제곡선값·가스종류·공기/가스비율·버너최소위치는미확정이다. 0195 LAD1832 CONT_C(LRef663,0593RID112;Instance664/0055RID86 PID_Stechio)는LMN을Correzione_Stechio에쓴다. CYCLE100MS,TM_LAG1M,DEADB_W0.1과계수/한계변수가원문인수이며튜닝권고가아니다. **12핀은원본RefId자체가없다**(부록B). 현재호출주기·PID안전성·전체실행결과는확정하지않는다.

0196은GasOut에0/100보정을다시쓰는별도네트워크다. 0197은Correzione_Stechio≤Limite_min이면Sign_lim_min,≥Limite_MAX이면Sign_lim_MAX를Coil로쓴다. 전체비율변환·곡선·간접쓰기완전성은추가원본이필요하며단일PID식으로대체하지않는다.

## 4 전기 전달 경로·실제 도면 끝점

### 4.1 외부 상태8회로 [E18]

FG97/PDF98 및FG98/PDF99는외부버너반clean contact회로다. 각채널은+24Vdc10.7→X1의2AF퓨즈→버너반송출단자→표시릴레이접점→회수단자→X1→E17.x→FG133/PDF134 MOD12입력단자로이어진다.

| E주소/표시 | 퓨즈X1→버너측송출 | 원본접점명 | 버너측회수→X1 | MOD12단자 |
| --- | --- | --- | --- | --- |
| E17.0 BURNER ON | 372→X/6/2 | KA40 | X/6/3→373 | 11 |
| E17.1 LOCKOUT | 374→X/6/5 | KA41 | X/6/6→375 | 12 |
| E17.2 IN MODULATION | 376→X/6/8 | KA41 | X/6/9→377 | 13 |
| E17.3 MIN GAS PRESSURE | 378→X/6/11 | KA20 | X/6/12→379 | 14 |
| E17.4 MAX GAS PRESSURE | 380→X/6/14 | KA21 | X/6/15→381 | 15 |
| E17.5 MIN AIR PRESSURE | 382→X/6/17 | KA30 | X/6/18→383 | 16 |
| E17.6 MAX AIR PRESSURE | 384→X/6/20 | KA31 | X/6/21→385 | 17 |
| E17.7 HIGH FLAME GAS VALVE INSERTED | 386→X/6/23 | KA50 | X/6/24→387 | 18 |

LOCKOUT과MODULATION에KA41이반복되는표기,최소압력의S3/최대압력의S4표기를원문대로보존한다. 같은릴레이실물·정상접점극성·실제화염감시로확정하지않는다. 버너전용010-390이없으므로위외부단자가근거끝점이다.

### 4.2 출력 릴레이와부하접점 [E19]

FG99/PDF100:Q6.5/.6/.7/Q7.0/.1은각각99KA1/2/3/4/5 코일A1, A2는−0Vdc10.6이다. FG142/PDF143 MOD15단자26/27/28과FG143/PDF144단자31/32가대응한다. PLC코일전원과버너측접점회로전원을혼합하지않는다.

| 릴레이·요청 | 실제 부하 경로 | 근거 경계 |
| --- | --- | --- |
| 99KA1 원격START/STOP | 버너X/220V→X1/388→99.1→**5–9**→99.2→X1/389→X/1/7 | 기존1–9설명은정정후보 |
| 99KA2 최대필터온도인터록 | X/1/2→X1/390→99.3→**5–9**→99.4→391→X/1/4 | PLC조건은TC09와TC01두고온래치반전 |
| 99KA3 버너RESET | X/220V→392→99.5→**5–9**→99.6→393→X/1/10 | 외부복구정책은미확정 |
| 99KA4 고화염요청 | X/5/11→394→99.7→**5–9**→99.8→395→X/5/13 | 고화염실제성립과구분 |
| 99KA5 점화전환 | X/5/2→396→99.9→단자1;X/220V→397→99.10→단자5;공통9→99.11→398 | X1/398외부종착단자는FG99에이름없음;전용도면필요 |

99KA5에는1과5모두실제선이들어온다. 이전환접점을앞네개와같이한쌍으로만기록하지않는다. 99KA1~4의미사용1번/접점표와실부하5–9를구분했다. X/220V는도면표시이며현재전압측정이아니다.

### 4.3 아날로그6경로 [E20]

FG100/PDF101은다음4–20mA회로를표시한다. 신호명·인쇄전류범위는현재파라미터/서보위치/질량유량범위의확정이아니다.

| 채널 | 버너전용반↔X1↔GME경로 | PLC모듈 끝점 |
| --- | --- | --- |
| 가스위치재전송 | X1/2/1→X1/399→+PEW360;X1/2/4→400→−100.1;차폐402→100SCH1 | FG111 MOD5단자22 I4+,24 U4−/I4− |
| 가스변조설정 | +PAW308→X1/401→버너X1/2/3;귀로−100.1 공유 | FG114 MOD8단자9 QV2/QI2,12 MANA |
| 공기위치재전송 | X1/3/1→403→+PEW362;X1/3/4→404→−100.2;차폐406→100SCH2 | FG111 MOD5단자26 I5+,28 U5−/I5− |
| 공기변조설정 | +PAW310→405→X1/3/3;귀로−100.2 공유 | FG114 MOD8단자13 QV3/QI3,16 MANA |
| 가스유량 FIT2001 | X1/7/1→407→+PEW364;X1/7/2→408→−PEW364;차폐409→100SCH3 | FG111 MOD5단자30 I6+,32 U6−/I6− |
| 공기유량 FIT3001 | X1/7/3→410→+PEW366;X1/7/4→411→−PEW366;차폐412→100SCH4 | FG111 MOD5단자34 I7+,36 U7−/I7− |

위버너측“X1/2/1”과GME측“X1/399”는서로다른기기의표기이며하나의단자대로합치지않는다. 서보최소위치/압력접점/질량유량을아날로그하나로대체하지않는다.

### 4.4 시공 케이블·중복표기 [E21]

Electrical_Can_Decoating_20241118.pdf PDF64의14_12~18은모두CR→CC01/BR01간선이다.

| 행·전체ID | 종류/규격·spare | 경로·LEN 인쇄 |
| --- | --- | --- |
| 14_12 =ENT+CC01-BR01A | DC/CVV25G1.0,8 | 100RA,LEN36 |
| 14_13 =ENT+CC01-BR01B | AC/CVV4G4.0,3 | 100RA/E400,LEN36 |
| 14_14 =ENT+CC01-BR01C | AC/CVV16G1.0,15 | 100RA/E400,LEN36 |
| 14_15 =ENT+CC01-BR01D | AIO/CVV-S4S1.0,3 | 100RA/E500,LEN36 |
| 14_16 =ENT+CC01-BR01E | AIO/CVV-S4S1.0,3 | 100RA/E500,LEN36 |
| 14_17 =ENT+CC01-BR01F | AI/CVV-S4S1.0,3 | 100RA/E600,LEN36 |
| 14_18 =ENT+CC01-BR01F | AI/CVV-S4S1.0,3 | 100RA/E600,LEN36 |

F가두행에반복되는C02를보존한다. 동일케이블중복기재인지별도두간선인지미확정이므로자동중복제거하지않는다. 개별I/O핀으로A~F를배정하지않는다. LEN은실측이아니며현재승인/준공/설치도미확정이다.

페이지별개정란:FG97/98/99/100/111/114/133/142는공란,FG143은Rev2 17.03.2025다. 파일명Rev2를전체페이지개정란에복제하지않는다.

## 5 알람·타이머·복구 경계

### 5.1 LDU 외부LOCKOUT과Reset 억제·출력 [E22]

0171 LAD1854 NID1:ON219(W188/ORef165) AND raw Lockout221(W189/166) AND NOT APP M10.2 Contact223(W190/167)→S117 LDU fault(W192/168). LDU fault는0585RID6 AO60=DB3.X7.4다.

ON→RESET_ALLARM225(W193/169) AND LDU227(W194/170)→S123 m491/M10.1(W195/171),S125 APP M10.2(W196/172). APP M10.2 Contact229→SD133 **6S**(0586RID12,W199/174) Tag135/T26(W200/175),Tag135231→R138 APP M10.2(W203/177).

m491 Contact233(W205/178)→SD145 **2S**(0586RID14,W206/179),Tag136/T27(W207/180);같은가지Coil149→Q6.7(W208/181). Tag136235(W209/182)→R156 LDU(W210/183),SD159 **2S** Tag137/T28(W212/185);Tag137237→R164 m491(W215/187). 타이머분기와Reset출력을“버너정상화완료”로해석하지않는다. rawLockout정상화접점이Reset시작가지에없는것과현행복구정책은구분한다.

### 5.2 최소위치 알람·시작실패·비율한계 [E23]

0172 LAD1855:ON32→Flag.Start_Burner238(W260/ORef249)→PBox239 bit PLS M50.0(W262/250)→[NOT FC GAS240(W264/251) OR NOT FC AIR242(W268/253)]→OR244→S245 SERVOMOTOR_MIN_POS_ALL(W273/255,0585RID23 DB3.X7.0). Reset은ON AND RESET246 ANDfault247→R248다. 내부닫힘이름과도면최소압력의상충때문에이를검증된서보최소위치보호라고확정하지않는다.

0185 LAD1869의 BURNER_START_FAULT(0585RID27 DB3.X6.7)는RESET1130 ANDfault1132→R1122(W1129/ORef1125)이다. 이번정확한Global참조조사에서해당래치의Set원천을확보하지못했다. 임의기동타임아웃·실패조건을생성하지않는다.

0189 LAD1874:ON1359 AND(Sign_lim_min1361 OR Sign_lim_MAX1363)→SD1317 **20S**(0586RID162,W1346/1333) Tag146/T90,Tag1461365→S1322 Sechio_Limits(W1350/1336,0585RID164 DB3.X7.2). Reset은ON AND RESET1367 ANDfault1369 AND NOT min1371 AND NOT max1373→R1329(W1357/1341). 원인비율한계의현재값·가스/공기비율적정성은미확정이다.

### 5.3 운전시간과22/24시간 가지 [E24]

0176 LAD1859:ON317 AND Inputs.BurnerOn319 AND Tag138321→PBox268(M51.5)→Add270 WorkData.W5+1;NOT Tag138323→SD277 **1M** Tag138/T30. ON AND NOT BurnerOn325→Move282 W5=0.

0177 LAD1861은**OFF318**(0582RID80 M0.1,W23/ORef24)→Ge289 W5≥1440→Coil292 Programmed stop burner M1.1,병렬Ge295 W5≥1320→Coil298 BURNER_TIME_LIMIT_22H(0585RID56 DB3.X7.7)다. 명칭24h/22h와비교숫자는백업근거지만현재자동정지보호가실제활성이라고단정하지않는다. OFF를False상수로확정하거나가지삭제를권하지않는다.

0193 LAD1860의 HMI Counter_StopBurner/ResetCounter_StopBurner는별도계수기이며W5와다르다. RESET_BURNER_COUNT DB41.X50.1이위22/24시간가지나외부버너LOCKOUT을해제한다고설명하지않는다. dryout ramp관련0190~0192는별도설정/쓰기참조로보존하며현행건조가열레시피·승인운전절차를이초안으로재구성하지않는다.

### 5.4 알람명·표시·현재 보호를분리

LDU,START_FAULT,SERVO_MIN,TIME22H,Sechio_Limits는각각다른원인/쓰기다. 아날로그BR01_Gas_OFR(DB3.X22.7),BR01_Air_OFR(DB3.X23.0) 및질량유량OFR도별도선형화출력이다. HMI4핀미결속상태에서표시색/팝업/“Allarme”별칭을같은래치라고단정하지않는다.

현재안전시간·최소공기량·밸브닫힘·점화성공·화염검출·가스차단·실제Reset완료는전용제조사자료와현재CPU/현장증거가필요하다. 이초안은보호값변경,연소비조정,강제출력,안전접점우회,반복리셋운전의근거가아니다.

## 6 증상별 자료 확인과수리 판단 경계

| 증상 | 비교할정적근거 | 막힌자료·판단경계 |
| --- | --- | --- |
| Ready가성립하지않음 | 0174 FN01/FN04/RD01/(FN06 ORBurnerOn)/FN02와3fault반전 | 각응답의현재신호·외부안전허가별도;강제Ready금지 |
| Start요청이해제됨 | 0175요청Reset/0181Lock/0182Enable와FN03 | 현재호출·다른쓰기·모드우선순위필요 |
| 외부LOCKOUT·Reset반복 | I17.1→0171래치/억제6S/출력2S가지→Q6.7/99KA3 | 외부010-390과제어기진단/복구절차미확보;자동재시도권고안함 |
| 최소위치알람 | 0172상승에지/FC닫힘이름↔I17.3/.5최소압력표기 | 전용센서/단자·현재쓰기/정상극성으로식별필요 |
| 세정상태가멈춤/예상과다름 | 0184State/NOTCloseANDClose/State5CloseORON/77가지 | 현재CPU를보지않고접점삭제·순서수정하지않음 |
| 세정표시시간이상 | 0183/0184같은T32와CleanTime복수쓰기 | 화면표시와실제퍼지안전시간은별도 |
| 고화염/점화전환이상 | 0178raw/processedI17.2,50MS/8S;01794S;FG99/1433초제목 | 현재제조사안전시퀀스·화염검출자료필요 |
| 가스/공기출력불일치 | PanelSP복수쓰기→Air±1→곡선/PID→272대285→아날로그끝점 | 설정비율·AI/AO스케일·교정·실제연소판단미확정 |
| 유량표시가0이안됨 | 0504GasFlow<1→Move1,원시HMI/환산/OFR분리 | 최소실제유량으로오인하지않음 |
| 22/24시간표시·정지불일치 | 0176W5와0177OFF조건,0193별도HMIcounter | 현행활성/실행주기/외부보호와별도 |

관찰자료는관찰자·시각/시간대·원본프로젝트/장치·값/단위·출처를갖춰야한다. 이번에현장관찰·운영기록·실제복구를수행하지않았다.

## 7 완료·누락·통합 인계

7영역은식별/소유·I/O/HMI·제어·전달회로·알람/복구·증상·완료경계로작성했다. 문서상태는독립통합검토용초안이다. 정적XML/PDF대조와UI/기록/게시·TIA컴파일·현재CPU·현장복구는각각별도상태며뒤항목은이번조사에서미수행이다.

통합시먼저대조할핵심: FC닫힘↔최소압력별칭,두Enable과Start/Flag구분,m491의M10.1선언,NOTCloseANDClose/CloseORON/State77,T32복수쓰기,기동실패Set미확보,OFF앞단22/24시간,3초대4초,272대285및Peripherie대일반Output읽기,99KA1~4 5–9/KA5전환,HMI4핀미결속,BR01F중복간선. 전체이전설비를재조사하지않고이원본경계부터확인한다.

누락자료는외부버너010-390 TYPE BP N300 및P&ID참조35602201_00의현행판,버너/연소제어기명판·승인안전시퀀스·화염감시/가스밸브/퍼지근거,현재CPU와백업일치·호출/다른쓰기·HMI이벤트,최소압력/최소위치태그대응,아날로그교정/제조사범위·현행비율/보호설정,케이블F두행의실물표찰,현재복구증거다. 없는내용은추정해서채우지않는다.

다음대상은승인순서의 **CC/CC01(P10)** 한개다. BR01초안전달을게시완료수에넣지않는다. 이초안작성시사용자확인게시완료는11/23(47.8%),기존제외2개를뺀11/21(52.4%)이다.

## 부록 A 핵심 주장 근거표

Flg/Ident는§1.3의decoded-original이다. 전체경로·고정커밋·해시는부록C에연결했다.

| ID | 주장 | 원본 | 핀·선언·페이지 | 해석·미확정 |
| --- | --- | --- | --- | --- |
| E01 | P11/소유 | docs/equipment-standard/INVENTORY.json | BR01 tag/identity_verified=false | 버너실물·본체/제어기일치미확정 |
| E02 | 전용도면경계 | PID_1684n002I.pdf;Electrical_Rev2.pdf | PID PDF1 DWG35602201_00;FG97/100 010-390 TYPE BP N300 | 전용안전회로자료없음;일반PLC로대체금지 |
| E03 | 디지털I/O | 0582/0584/0585 Ident;live_index.json | RID3/65I17.1/.2;RID94/26/16/66/79Q6.5~7.1;SAD/SSD | oldE/A주석과현재백업주소분리 |
| E04 | 입력·별칭 | 0397/0030 Flg;0627/0628/0629/0635/0690/0691/0692 Ident;FG97 | Move62W76/ORef67InputAO128→W77/ORef68DB13W16;FC닫힘AO139/141 | 최소압력도면vs닫힘논리;현재극성/다른쓰기미확정 |
| E05 | 내부식별 | 0582/0584/0585 Ident | Start/Enable/Flag/Lock/M10.1/M10.2/M15.0/TOD DB1/2/3/5/6/13 | 유사명·블록범위·RID오결속배제 |
| E06 | 아날로그선언 | 0502/0503/0504/0505 Flg;0672/0674/0676/0678/0680 Ident | PIW360/362/364/366;Data/Coef/Zero/OFR핀 | 실제단위/교정/위치·유량미확정 |
| E07 | HMI | 0395/0398 Flg;0627/0628/0629 Ident;hmi_plc_tags.csv | 1219ORef24/28/31/35전부미결속;1071Move170/171/84/194;10CSV행 | 표시·원시·환산·실물층구분 |
| E08 | Ready/요청해제 | 0174/0175 Flg;0582/0584/0585 Ident | 1857C182;1858OR213/OR219/R232 | FN01/04/RD01/(FN06ORBurnerOn)/FN02;외부안전완료아님 |
| E09 | 원격출력소유 | 0182 Flg;0582/0585 Ident | 1866NID12Contact634/636/642/644,C607/C611 | Flag/Lock/FN03응답/Enable두개분리;ON임의추가금지 |
| E10 | Lock상충 | 0181 Flg;0582/0583/0585/0586 Ident | 1865S579/R588;OFF/ProgramStop,FC닫힘,Reset OR ON648 | 현재래치우선순위/물리닫힘미확정 |
| E11 | MV03세정순서 | 0183/0184 Flg;0582/0584/0585/0586 Ident | 1867SD632/Add625와1868SD1215/Add1208,T32중복;NOTClose28ANDClose1670 | 동일RID233·CloseORON·State77·4M/1S/30S;안전퍼지로확정금지 |
| E12 | 고화염 | 0178 Flg;0582/0583/0585/0586 Ident | 1862Add409/415,SD44850MS/4658S,R422/R453/S470 | rawI17.2와처리DB13X17.2;현행튜닝미확정 |
| E13 | 점화전환상충 | 0179 Flg;0582/0585/0586 Ident;Electrical_Rev2.pdf | 1863SD472literalRID2374S/T122;FG99/143제목3sec | MainflameM25.0은화염검출아님;시간정정안함 |
| E14 | PID허가/전달 | 0186/0187/0416/0023 Flg;0582/0585/0648/0649/0650/0651/0652 Ident | 1870C1172/Move1181;1871Add1176;1721/1722WorkPIDResult다른쓰기 | 제목PID와실제본문구분;현재원천/주기미확정 |
| E15 | 요청제한/지연 | 0188/0417 Flg;0582/0585/0586/0650/0651 Ident | 1872Move1265/1273/1282/1294;1724Add233/+1,Add242/−1 | NOTremoteANDSP≤0원문보존;실제1초주기미확정 |
| E16 | 출력배율/접근방식 | 0467/0468 Flg;0660/0661/0662/0663/0664 Ident | AirMul536×272/PQW310;GasMul590×285/PQW308;Move22QW308→test_out | Peripherie쓰기대SAMNone읽기;test_out은인터페이스 |
| E17 | 곡선·비율PID | 0194/0195/0196/0197 Flg;0055/0590/0591/0592/0593/0594 Ident | 1832CONT_C663/Instance664;12ORefRefId부재;1834보정/1835한계 | 계수현재값/전체비율변환/실제튜닝미확정 |
| E18 | 디지털입력끝점 | Electrical_Rev2.pdf | FG97/98/133 PDF98/99/134 X1/372~387→E17.0~7→MOD12 11~18 | KA41중복표기·최소압력라벨;정상극성미확정 |
| E19 | 릴레이출력끝점 | Electrical_Rev2.pdf | FG99/142/143 PDF100/143/144;KA1~4 5–9,KA5 1/5/9 | 버너외부전원·코일전원분리;X1/398종착미확보 |
| E20 | 아날로그끝점 | Electrical_Rev2.pdf | FG100/111/114 PDF101/112/115;X1/399~412;MOD5/8단자 | 버너반X1과GME X1구분;현행4–20mA구성미확정 |
| E21 | 시공간선 | Electrical_Can_Decoating_20241118.pdf | PDF64 14_12~18 A/B/C/D/E/F/F,LEN36 | C02중복F보존;개별핀자동배정금지 |
| E22 | LDU/Reset | 0171 Flg;0582/0584/0585/0586 Ident | 1854S117,S123/125,SD1336S/1452S/1592S,C149Q6.7,R156/R164 | M10.1/M10.2·T26/27/28;외부복구완료아님 |
| E23 | 알람별Set/Reset | 0172/0185/0189 Flg;0582/0585/0586 Ident | 1855PBox239/S245/R248;1869R1122만확보;1874SD131720S/S1322/R1329 | START_FAULT Set미확보;비율알람Reset두한계정상조건 |
| E24 | 운전시간/카운터 | 0176/0177/0193 Flg;0582/0584/0585/0586 Ident | 1859SD2771M/P268/Add270/Move282;1861OFF318→1440/1320;1860별도HMIcounter | 현행22/24h보호단정금지;ResetCounter별도 |
| E25 | 미완료경계 | 0190/0191/0192 Flg;0582/0585/0586 Ident | dryout ramp기존참조/설정소유 | 현행레시피·전용가열절차재구성안함 |
| E26 | 보존·표준 | BR01.html6종;burner-interface.json;WORK-STANDARD/TEMPLATE/SKILL | alarm-guides/BR01.html없음;기존C02·접점설명정정후보 | 초안과게시·TIA·현재CPU·현장복구분리 |

## 부록 B CONT_C 원본 RefId 부재와고유타이머

0195 LRef663 CONT_C의원본ORef에RefId가없는핀만열거한다. 미결속은FALSE/0/기본값/실제단선이라는뜻이아니다. 실제Instance664는0055RID86 PID_Stechio이고호출은0593RID112 CONT_C다.

| 핀 | Wire/ORef | 상태 |
| --- | --- | --- |
| INT_HOLD | W735/ORef680 | 원본RefId없음 |
| I_ITL_ON | W736/ORef681 | 원본RefId없음 |
| PV_PER | W741/ORef686 | 원본RefId없음 |
| I_ITLVAL | W754/ORef699 | 원본RefId없음 |
| LMN_PER | W757/ORef702 | 원본RefId없음 |
| QLMN_HLM | W758/ORef703 | 원본RefId없음 |
| QLMN_LLM | W759/ORef704 | 원본RefId없음 |
| LMN_P | W760/ORef705 | 원본RefId없음 |
| LMN_I | W761/ORef706 | 원본RefId없음 |
| LMN_D | W762/ORef707 | 원본RefId없음 |
| PV | W763/ORef708 | 원본RefId없음 |
| ER | W764/ORef709 | 원본RefId없음 |

| 용도 | 백업설정·타이머 | 원본 |
| --- | --- | --- |
| LDU Reset억제 | 6S/T26(Tag135) | 0171 SD133;0586RID12 |
| Reset시퀀스 | 2S/T27(Tag136),2S/T28(Tag137) | 0171 SD145/159;0586RID14 |
| 운전분누적 | 1M/T30(Tag138) | 0176 SD277 |
| 고화염해제/진입 | 50MS/T29(Tag139),8S/T12(Tag140) | 0178 SD448/465;0586RID72/74 |
| 점화전환 | 4S/T122(Tag141) | 0179 SD472;0586RID237;도면3sec와상충 |
| 세정표시공유 | 1S/T32(Tag142) | 0183 SD632와0184 SD1215 |
| 세정상태 | 4M/T31(Tag143),1S/T37(Tag144),30S/T38(Tag145) | 0184 SD1199/1262/1329;0586RID114/98/138 |
| 비율한계 | 20S/T90(Tag146) | 0189 SD1317;0586RID162 |

값은원본기록이며현행안전시간·권장튜닝·실제경과시간의검증값이아니다.

## 부록 C 고정 원본 SHA-256 100개

고정커밋 abcf31c5030bc7ef8749ed8e869a857f2387a28a에서읽어계산했다. ZAP18/PLF는백업보존기준이며실행/컴파일/현재CPU일치나파일전체기능검증을뜻하지않는다.

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
| [all-in-one/registers/burner-interface.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/registers/burner-interface.json) | f27c14a85d745fdb864b31864f6744ac58dac1d34b45c951042249c5f210fdfd |
| [all-in-one/sources/decoded-original/0014-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0014-FlgNet.xml) | 2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30 |
| [all-in-one/sources/decoded-original/0030-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0030-FlgNet.xml) | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b |
| [all-in-one/sources/decoded-original/0171-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0171-FlgNet.xml) | e3790f570398abfc8422245fe44bef6563b4c9144ba5debdaad3ce3fe752a4af |
| [all-in-one/sources/decoded-original/0172-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0172-FlgNet.xml) | 42dc8e20b3a4a819be3b750235ffe5b037b2b9915229af86999474ca82bc0609 |
| [all-in-one/sources/decoded-original/0173-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0173-FlgNet.xml) | b4f2002933f13ad38f8b8bc6daa3f3ef11a9181ea1c2f33f63ef7a3f7305dc07 |
| [all-in-one/sources/decoded-original/0174-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0174-FlgNet.xml) | 23fb073206f95c69abc4373d3080081a369e4dd5021c2bd1a90d63029bb908d5 |
| [all-in-one/sources/decoded-original/0175-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0175-FlgNet.xml) | 41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97 |
| [all-in-one/sources/decoded-original/0176-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0176-FlgNet.xml) | 80a479c10365b5d5af6a592e09eda6fdbab66433658d69b0219043ac90a3be78 |
| [all-in-one/sources/decoded-original/0177-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0177-FlgNet.xml) | 6661adf80ebeb53185a94c177c09880d0d473fe4c3f883ad8aea642e6c0c3c1f |
| [all-in-one/sources/decoded-original/0178-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0178-FlgNet.xml) | 36752e04a38e486ad4a0857d6baa8119d9b757678300358bcc95881f23e266c9 |
| [all-in-one/sources/decoded-original/0179-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0179-FlgNet.xml) | ee88a6ae9661830d363fcbada7542a9bf829daa7c8515b2335806020ee0b5279 |
| [all-in-one/sources/decoded-original/0180-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0180-FlgNet.xml) | b3141dffaf1a7d0583e3d03ab5bf3b8dcab62e42f3722c45ce0a9d3f8b608e58 |
| [all-in-one/sources/decoded-original/0181-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0181-FlgNet.xml) | 98e839ee13a05db05768503e768e9238d892c4788dc7b6c9d3017fc86d3b722b |
| [all-in-one/sources/decoded-original/0182-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0182-FlgNet.xml) | f11326ea7f915ce3d9347f72a4b314635e0943fc251db9a67694aedd3795dd0b |
| [all-in-one/sources/decoded-original/0183-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0183-FlgNet.xml) | 7f609f32b756215f62c2d9311d8471ecb4e44f7358d2cefcccff8c9fc5930e18 |
| [all-in-one/sources/decoded-original/0184-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0184-FlgNet.xml) | a0a59597c73eb68e1cbdb2f41d640eabccfd05655c4e9c08624be6027974caf3 |
| [all-in-one/sources/decoded-original/0185-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0185-FlgNet.xml) | 2532fbe9602e3effc1f3992aaeb6749e93841072f0e4d797c4b7a369a849ab61 |
| [all-in-one/sources/decoded-original/0186-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0186-FlgNet.xml) | 932f8756ee0e4385553944bd166109c45684766a136bfddd68cdf08552a83883 |
| [all-in-one/sources/decoded-original/0187-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0187-FlgNet.xml) | 0d4e4dd53c729f48c4ad275eba51d89fab582958032f9eae6f722daff808e027 |
| [all-in-one/sources/decoded-original/0188-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0188-FlgNet.xml) | 8a7aa3d5d5d26de589c1c386f20e1d28cb83244bbc78c5cee17671964bc1ac08 |
| [all-in-one/sources/decoded-original/0189-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0189-FlgNet.xml) | db78061a0a5a5568ea188ed6de4e7568c503411afbe811a5afea024a6f74dbbe |
| [all-in-one/sources/decoded-original/0190-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0190-FlgNet.xml) | 46722388ab7f69c14436e64051b0bb0c720ba1878b9652c4b859fdb4ddb0bf25 |
| [all-in-one/sources/decoded-original/0191-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0191-FlgNet.xml) | 28f087b14ff3a0a0f5bcb20e212c41357ad36caf3c8308f8019f4b78d60eb7bd |
| [all-in-one/sources/decoded-original/0192-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0192-FlgNet.xml) | 874a8e7d6208c568027f4b03fb0e5e085be7e79b914db9dbef30a43d200ee1d2 |
| [all-in-one/sources/decoded-original/0193-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0193-FlgNet.xml) | 2aa42ce6e35c90844bc07b302cd12815b20c0008ebf54e9961edf79078c7fd41 |
| [all-in-one/sources/decoded-original/0194-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0194-FlgNet.xml) | 489de0d7673d1551b77ddf892ea74eee784ac6e5f5ea9860bd2fcaeb9b0c2851 |
| [all-in-one/sources/decoded-original/0195-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0195-FlgNet.xml) | fc40707c4c248625ff2a5ec39a7451e02ee2cd9670d41e0354021027d3cc5ea7 |
| [all-in-one/sources/decoded-original/0196-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0196-FlgNet.xml) | 8dfab60a56115bbf67249db39505dc288e4da875314579c66f7e2f5f1702a274 |
| [all-in-one/sources/decoded-original/0197-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0197-FlgNet.xml) | 61aedd67b7ec771ea30fe601d5e715c68e6fe5981060da8de7ce4719e5c66e4d |
| [all-in-one/sources/decoded-original/0291-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0291-FlgNet.xml) | fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550 |
| [all-in-one/sources/decoded-original/0395-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0395-FlgNet.xml) | 0572d7856681cd5c9fdd87562f1bcc1f04e5234f2505338c4a85a162a3de7fc1 |
| [all-in-one/sources/decoded-original/0397-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0397-FlgNet.xml) | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 |
| [all-in-one/sources/decoded-original/0398-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0398-FlgNet.xml) | 4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747 |
| [all-in-one/sources/decoded-original/0416-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0416-FlgNet.xml) | 1838d3c52dbc3319af0d7aabbb6477af9e862075b12a990412e6bd69a1d1cd0d |
| [all-in-one/sources/decoded-original/0023-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0023-FlgNet.xml) | 868f9cce5f0759fac0fb4a1a23599fa166ffa29978b430c84d1b8cf03bb3d347 |
| [all-in-one/sources/decoded-original/0417-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0417-FlgNet.xml) | 1b9c7e4adf52f72f896b3c93753c76869a5aa0f85a9b40c9b7d168f1ef14b7f8 |
| [all-in-one/sources/decoded-original/0467-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0467-FlgNet.xml) | 126749547e09ee8f0584da5892a8c4025d85555c21bba40a4a5ad25e2a7591a8 |
| [all-in-one/sources/decoded-original/0468-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0468-FlgNet.xml) | 4e29e6dd5cb60e64a7116f3f66bf51d8f476aa6cff6de3542689a50996c2015b |
| [all-in-one/sources/decoded-original/0502-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0502-FlgNet.xml) | 240607a037e36658b634c4df475d8819bd0211c75ad2dfc6b5d0fefde9042eda |
| [all-in-one/sources/decoded-original/0503-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0503-FlgNet.xml) | 449f8c0476e01ba5db80814f58301cce4d77d0e14be0f6e641b7edf3434626e2 |
| [all-in-one/sources/decoded-original/0504-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0504-FlgNet.xml) | d428b8c440d03f708f397daeb83f622f68b518a018522bed8736aec84c58fbdf |
| [all-in-one/sources/decoded-original/0505-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0505-FlgNet.xml) | 3cedabf3574cc158919501c3bd81afb9b6e00387dbb7e7d28abe3d0bad185c26 |
| [all-in-one/sources/decoded-original/0055-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0055-IdentXmlPart.xml) | 9baf3104be3c8a3457c3eea021f23fbd6a60c665e81a293bd7f2cae52c64be29 |
| [all-in-one/sources/decoded-original/0582-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0582-IdentXmlPart.xml) | 41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951 |
| [all-in-one/sources/decoded-original/0583-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0583-IdentXmlPart.xml) | 0a34a2b7ad17eba6198dbe53d5c6aa8e87710c7436b832b9d39a075074ab58a8 |
| [all-in-one/sources/decoded-original/0584-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0584-IdentXmlPart.xml) | 3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d |
| [all-in-one/sources/decoded-original/0585-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0585-IdentXmlPart.xml) | e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184 |
| [all-in-one/sources/decoded-original/0586-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0586-IdentXmlPart.xml) | f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250 |
| [all-in-one/sources/decoded-original/0590-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0590-IdentXmlPart.xml) | baff7271b3db646e8953c31d20b72f7b044b1154b689b15ca0fb38ebb44ad81c |
| [all-in-one/sources/decoded-original/0591-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0591-IdentXmlPart.xml) | 2e165c44fc9df852ea3729b3ddb33dc0a74e4f8826676f9c5c5626e1dce033f8 |
| [all-in-one/sources/decoded-original/0592-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0592-IdentXmlPart.xml) | d157e3d92df9e4a6ce46567b8611a51b0a10abf4dd7f9c4e613087b2df9583a8 |
| [all-in-one/sources/decoded-original/0593-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0593-IdentXmlPart.xml) | 504568b5b50bb25a6880e9da724f79438fbb07e7a311a9391681143d713499e9 |
| [all-in-one/sources/decoded-original/0594-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0594-IdentXmlPart.xml) | 88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd |
| [all-in-one/sources/decoded-original/0611-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0611-IdentXmlPart.xml) | 0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089 |
| [all-in-one/sources/decoded-original/0612-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0612-IdentXmlPart.xml) | 95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38 |
| [all-in-one/sources/decoded-original/0627-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0627-IdentXmlPart.xml) | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| [all-in-one/sources/decoded-original/0628-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0628-IdentXmlPart.xml) | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd |
| [all-in-one/sources/decoded-original/0629-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0629-IdentXmlPart.xml) | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| [all-in-one/sources/decoded-original/0635-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0635-IdentXmlPart.xml) | 1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457 |
| [all-in-one/sources/decoded-original/0648-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0648-IdentXmlPart.xml) | afaa47ae737d9333fe831ffac2b1d1388f108bb6a2b23d03554fa862f7edb454 |
| [all-in-one/sources/decoded-original/0649-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0649-IdentXmlPart.xml) | 38f59e654ecfbc2066fa1f8beeb9ced952adc405f8a4fcf3ef233e9d5d026576 |
| [all-in-one/sources/decoded-original/0650-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0650-IdentXmlPart.xml) | 86f53657eb7afb0798da0e215ba226721076c2ab1b25b74eb83e7b3c4b2d8a2d |
| [all-in-one/sources/decoded-original/0651-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0651-IdentXmlPart.xml) | 549c09fb14ce6e9734a2ba604c78868647451f24d224ead0d17d209f66428111 |
| [all-in-one/sources/decoded-original/0652-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0652-IdentXmlPart.xml) | 251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692 |
| [all-in-one/sources/decoded-original/0660-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0660-IdentXmlPart.xml) | 0bf4f4c46531f55324602f4f7b1a1e0b9e63df2c6278126f6e5cf1bc9a06509f |
| [all-in-one/sources/decoded-original/0661-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0661-IdentXmlPart.xml) | 90672199fee355011f581d3287046894772f3f3b4cb78bbe0dd0d71bd488ac93 |
| [all-in-one/sources/decoded-original/0662-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0662-IdentXmlPart.xml) | 1838040bfee800fdb3f13b126eaf69a9d178b17cecc0d59ae03e9185216a48a5 |
| [all-in-one/sources/decoded-original/0663-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0663-IdentXmlPart.xml) | d3980b88d3cd3e49854439d0778c58ed131bae46a6bc3e65ab70e81f766ac03d |
| [all-in-one/sources/decoded-original/0664-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0664-IdentXmlPart.xml) | 68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed |
| [all-in-one/sources/decoded-original/0672-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0672-IdentXmlPart.xml) | 6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222 |
| [all-in-one/sources/decoded-original/0674-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0674-IdentXmlPart.xml) | 4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84 |
| [all-in-one/sources/decoded-original/0676-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0676-IdentXmlPart.xml) | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 |
| [all-in-one/sources/decoded-original/0678-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0678-IdentXmlPart.xml) | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 |
| [all-in-one/sources/decoded-original/0680-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0680-IdentXmlPart.xml) | fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95 |
| [all-in-one/sources/decoded-original/0690-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0690-IdentXmlPart.xml) | fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541 |
| [all-in-one/sources/decoded-original/0691-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0691-IdentXmlPart.xml) | 17cb7d9734d76b39e729e0daf0c89d9bdf74907aab2130c80453fa04e4cea1da |
| [all-in-one/sources/decoded-original/0692-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0692-IdentXmlPart.xml) | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| [all-in-one/devices/BR01.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/devices/BR01.html) | b1e5bbe3e3d79990e8a90d2d7e608ed0e8c65f4ebd68a5d3f0feffbba833d030 |
| [all-in-one/control-specs/BR01.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/control-specs/BR01.html) | dc8d4f2614958e29b20cc73f00ede0edaa90e3d95bba190e02eb22c277c2d8f6 |
| [all-in-one/circuit-guides/BR01.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/circuit-guides/BR01.html) | d15417b414a8b64519c1095b345253bb2e890255654ab2c2cd50b3ec7f618e70 |
| [all-in-one/signal-guides/BR01.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/signal-guides/BR01.html) | 79bfd648f1a91a4b1729f13624c995f71833c5a0dc4062f7ae835fdb9d337787 |
| [all-in-one/construction-guides/BR01.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/construction-guides/BR01.html) | 1b1cba9a30e7e307ddd7a100de9d299c464b44d0b86f8efcd365b83f012fd43f |
| [all-in-one/procedures/BR01.html](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/procedures/BR01.html) | 0e1cca72ec88365abdd402b3bafe5db95066b15e9e95880d26e6e4bc936ab402 |

## 부록 D 수행·보존기록

수행은공개고정원본읽기,XML정적파싱·선언/Part/Wire/ORef대조,지정PDF실제렌더/시각확인,자체MD작성과SHA-256계산이다. 원본worktree변경유무는git status로확인한다. 공통코드·버전·대장·배포·운영기록을편집하지않았다. 프로젝트생성기·시뮬레이터·행동시험·TIA·실제PLC·현장·보호값·게시작업은하지않았다. 전용버너문서의공백을일반PLC·태그명·인접설비자료로메우지않았다.

