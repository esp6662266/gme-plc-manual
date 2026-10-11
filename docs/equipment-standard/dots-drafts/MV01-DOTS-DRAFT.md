# MV01 P19 고유 제어 근거와 설비 문서 초안

- 산출물: **MV01-DOTS-DRAFT.md / 1차 독립 통합 검토용**, 2026-10-11 KST.
- 조사·작성: Dots 자체 환경에서 직접 수행. 대상은 MV01(P19) 한 개. 사용자가 유일한 로컬 편집·검증·게시 담당이다.
- 기준: 공개 esp6662266/gme-plc-manual의 main/all-in-one. 조사 고정 커밋 **89570f755b3a01cffd80e3e36bea3bf1da403da9**, v1.10.0. 조사 시작 스냅샷이며 MV01 게시 버전이 아니다. 직전 5fac25b 대비 sources 경로 차이는 없었다.
- 적용 표준: GME-STD-1.0.0, 저장소 AGENTS, .agents/skills/gme-equipment-rollout/SKILL.md, WORK-STANDARD.md, WORK-ITEM-TEMPLATE.md, INVENTORY.json의 7영역·근거 추적·완료 분리. 제공 환경에서 tia-equipment-alarm-trace 스킬은 확보하지 못했다. 접근 권한을 확장하지 않고 공개 표준·원본 XML·PDF 실제 렌더를 적용했다.
- 상태: 문서 초안/지정 원본 정적 대조. 현재 CPU·실물·정상 극성·현행 보호 설정·현장 복구는 미확정. TIA 컴파일, UI/저장/복원/동시성/보고서/배포 검증은 수행하지 않았다.
- 보존: 원본·기존 설비 자료·기존 초안 보존. 공통 코드·버전·대장·배포·운영 기록은 편집하지 않았다. 새 Work/Codex 재위임, 시뮬레이터 작성·수정·생성·실행·행동시험, 실제 PLC·현장·보호값 변경은 없다. 별도 세진 프로그램 자료/코드/운영 사진을 가져오지 않았다.

## 먼저 확인할 MV01 고유 사항

1. **150ms 방향 응답 불일치와 W33>2000 / W34<−2000은 같은 Allarm.MV01_FAULT를 Set**한다. 세 원인을 별도 알람 비트 세 개로 만들지 않는다. 타이머는 Tag_92=T4이며 인접 MV03의 150S를 복사하지 않는다. [E09,E11]
2. W33/W34는 Q2.4/Q2.5와 공유 펄스에 따른 명령 누적값이다. ZT02 엔코더 실측값이나 모터 전류가 아니다. ±2000을 초·각도·회전수로 환산할 근거가 없다. [E10,E11]
3. 열림/닫힘 출력의 펄스 가지는 **MV WORK PULSE OR ON**이다. ON을 선언으로 결속했으며, “항상 200ms/2초 간헐 구동”이라고 단정하지 않는다. [E05,E07]
4. ResetEncoderProcedure_MV01은 단순 표시 초기화가 아니다. 정적 논리상 열림을 차단하고 닫힘 요청의 별도 OR 가지에 들어간다. 실제 실행·교정·복구를 안내하거나 수행하지 않는다. [E05,E06]
5. HSC CountValue와 엔코더 처리 경로는 확인했지만 **HSC 실인수 19핀, PID 9핀, HMI 10핀의 선언 결속은 미확보**다. 빈 핀을 FALSE/0/기본값 또는 인접 밸브 값으로 채우지 않는다. [E12,E13,E15,E18]
6. OEM FG45/144는 ZT02 A/B 펄스 엔코더 경로다. 시공 PDF57의 ZT02 케이블 행에는 AI가 적혀 있다. 분류 상충을 보존하고 4–20mA로 임의 해석하지 않는다. [E22,E24]
7. MV01은 M20, LS23/24, ZT02와 연결된다. HE01 인접 배치·공유 단자함은 HE01의 모터 또는 다른 댐퍼와 같은 본체라는 증거가 아니다. [E01,E02,E24]

## 1 설비와 자료 기준

### 1.1 식별·역할·소유

INVENTORY의 P19는 catalog_id=MV01, mapping=tag, **identity_verified=false**다. 모터 구동 밸브, kind=motorvalve, parent_id=null, phase1이다. 태그 대응과 실물 동일성 완료를 구분한다. [E01]

P&ID PID_1684n002I.pdf PDF1 실제 렌더에서 HE01 오른쪽 유로의 MV-01, M20, LS23/LS24, ZT02 및 2.2kW 440V 표기를 확인했다. 제어 네트워크 LAD1702 제목은 mv01 controlled by tc03, PID 입력 지역변수 이름은 Real_SP_TC03xMV01 / Real_TC03xMV01이다. 따라서 자료상 TC03 관련 제어 댐퍼로 설명하되, PID 지역변수의 상류 계산식과 현재 현장 작동 방향은 미확정이다. [E02,E05,E15]

FG44는 M20 MV-01의 3상 정·역 접촉기 회로다. 44KM1/2, 44QM1, 44QS1은 MV01 구동 경로에 배정한다. FN02·MV04·HE01의 다른 구동기를 MV01 부속으로 편입하지 않는다. 시공 도면의 HE01-FLO2TB1은 공유 배선 경유점이지 설비 소유 확정 근거가 아니다. [E20,E24]

### 1.2 기존 자료 보존

devices/MV01.html, control-specs/MV01.html, alarm-guides/MV01.html, circuit-guides/MV01.html, signal-guides/MV01.html, construction-guides/MV01.html, procedures/MV01.html의 기존 완료 분석·미확정·참조를 보존한다. 특히 기존 alarm-guide의 “동일 래치/방향 누적/리셋 분리”는 원본과 일치한다. 공유 control-spec의 인접 MV02/03/05/06 행이나 관련 피연산자 개수를 MV01 전용 항목 수로 복제하지 않는다. [E25]

### 1.3 근거 표기와 해석 경계

본문 네 자리 XML 번호는 all-in-one/sources/decoded-original/NNNN-FlgNet.xml, 선언은 같은 폴더의 NNNN-IdentXmlPart.xml이다. LAD는 network-map.json의 document_id, NID는 원본 선언 네트워크 식별자다. Part/접점/Coil 번호와 ORef UID, 선언 RID를 구분한다. RID·UID가 같은 다른 블록 후보를 이름 순서로 결합하지 않았다. 예: 0342 ORef172는 0617 RID1 ON의 NID1 선언과 연결되며 다른 블록의 같은 번호 DepDB 후보를 배제한다.

해시 부록은 원본 재검토의 기준이다. 복원 XML은 백업에서 추출된 자료이며 현재 다운로드 프로그램·현재 CPU·실물 배선을 입증하지 않는다. 정적 논리식의 ON/OFF는 심볼이고 현재 참/거짓 상수가 아니다.

## 2 I/O와 HMI

### 2.1 원시 I/O와 처리 변수

E/A는 OEM 도면, I/Q는 PLC 표기다. 다음 표는 백업/도면 대응이며 현재 배선·극성·동작 확인이 아니다. [E03,E04,E20~E23]

| 신호 | 원시 주소·근거 | 처리 변수·근거 | 실제 도면 끝점 |
| --- | --- | --- | --- |
| 열림 접촉기 응답 | mv01_fbk_opening I3.2 Bool; live_index _7ev doc885 | Inputs.MV01 Run_Opening DB13.DBX3.2;0573 RID59 AO26 | 44KM1 보조13/14→E3.2→FG119 MOD8 단자33 |
| 닫힘 접촉기 응답 | mv01_fbk_closing I3.3 Bool;doc886 | Inputs.MV01 Run_Closing DB13.DBX3.3;0573 RID60 AO27 | 44KM2 보조13/14→E3.3→FG119 MOD8 단자34 |
| 열림 한계 | mv01_open I8.1 Bool;doc889 | Inputs.MV01 Open DB13.DBX8.1;0619 RID172 AO65 | LS23 11/12→X1/113→E8.1→FG124 MOD10 단자2 |
| 닫힘 한계 | mv01_close I8.2 Bool;doc1528;0678 RID205 SAD Input AO66 | Inputs.MV01 Close DB13.DBX8.2;0619 RID173 AO66 | LS24 11/12→X1/115→E8.2→FG124 MOD10 단자3 |
| 열림 명령 | Start Open MV-01 Q2.4;0617 RID15 SAD Output AO20 | Coil143 0342 NID1 UID175 Write | FG138 MOD14 단자25 A2.4→FG44/4→44KM2 NC31/32→44KM1 coil |
| 닫힘 명령 | Start Close MV-01 Q2.5;0617 RID14 SAD Output AO21 | Coil156 0342 NID1 UID183 Write | FG138 MOD14 단자26 A2.5→FG44/6→44KM1 NC31/32→44KM2 coil |

원시 태그 I3.2/I3.3/I8.1은 live_index 주소·OEM 도면을 확인했으나 동일 이름의 SimpleAccess 선언은 이번 추출 참조에서 직접 결속하지 못했다. 처리 DB 주소를 원시 태그 선언 증거로 바꿔 쓰지 않는다. Q 태그의 과거 A60.1/A60.2 주석은 현재 백업 Q2.4/Q2.5를 대체하지 않는다.

DB 번호는 0618 DepDBBlock Inputs TOD13, Allarm TOD3, Flag TOD2, WorkData TOD6, HMI_DB TOD41로 교차 확인했다. AO는 비트 오프셋이며 Bool과 Word/DInt를 구분한다.

### 2.2 원시 입력 → Inputs 전달 및 호출 경계

LAD1070 0397, NID1에서 다음 두 Word 복사를 원본 Wire·선언으로 확인했다. [E04]

| 포함 신호 | 실제 명령/핀 | 선언 |
| --- | --- | --- |
| I3.2/I3.3 포함 IW2→DB13.DBW2 | Move27.in=W31/ORef28;out1=W32/ORef29;en=W34, 앞 Move22.eno | 0627 RID8 Tag179, Word Input AO16;0629 RID9 Word AO16 BAD4;0628 RID4 TOD13 |
| I8.1/I8.2 포함 IW8→DB13.DBW8 | Move43.in=W55/ORef47;out1=W57/ORef48 | 0627 RID15 Tag181 Word Input AO64;0629 RID16 Word AO64 BAD4;0628 RID4 TOD13 |

복사 경로 자체에는 이 두 Word에 대한 비트 반전이 없다. 그러나 이 사실만으로 현재 모든 쓰기·정상 극성·온라인 값 일치를 확정하지 않는다. main LAD1613 0030 NID19의 recipes handler→hmi→hmi output ENO 사슬 뒤, Contact37의 NOT Simulation(1)을 거쳐 hmi inputs CRef28로 들어가는 경계를 함께 보존한다(W32/33/42/44/43,0692 RID140). 여기서 Simulation(1)은 0692 RID140 SAD Memory AO1440=M180.0이다. 0506의 0678 RID344도 같은 이름·Memory AO1440이므로 두 호출 경계는 백업상 같은 주소를 읽는다. 이름을 임의로 Simulation으로 줄이지 않는다. 원본 호출의 정적 확인일 뿐 시뮬레이터 실행은 하지 않았다.

### 2.3 내부 요청·값·구분

| 항목 | 백업 선언 | 의미·경계 |
| --- | --- | --- |
| Flag.M_MV01_OPEN | DB2.DBX3.3;0619 RID8 AO27 | HMI 열림 요청 후보/PLC Reset 대상;실제 HMI 쓰기 이벤트 미확정 |
| Flag.M_MV01_Close | DB2.DBX3.4;0619 RID6 AO28 | 닫힘 요청;다른 쓰기/우선순위 미확정 |
| Flag.MV01_Auto | DB2.DBX7.2;0619 RID7 AO58 | startup Set, PID COM_RST 반전 입력,모드 선택 |
| HMI_DB.ResetEncoderProcedure_MV01 | DB41.DBX50.5;0619 RID196 AO405 | 출력 요청에도 작용하는 절차 비트 |
| Allarm.MV01_FAULT | DB3.DBX4.7;0619 RID11/0573 RID11 AO39 | 응답/누적 감시 공통 래치 |
| Allarm.Pot_MV01_OFR | DB3.DBX24.6;0676 RID432 AO198 | 위치값 선형화 범위 알람,위 래치와 별개 |
| UP / DOWN MV01 PID | M12.0/M12.1;0617 RID12/16 AO96/97,0670 RID77/78 | CONT_S QLMNUP/QLMNDN 출력 |
| MV WORK PULSE | M10.0;0617 RID13 AO80 | 공유 펄스;MV01 전용 타이머로 분류하지 않음 |
| WorkData.W33 / W34 | DB6.DBW66 / DB6.DBW68 Int;0619 RID109/111 AO528/544 | 방향 명령 누적;엔코더값과 별도 |
| Data.Pot_MV01 | DB1.DBW148 Int;0676 RID220 AO1184,0674 Data TOD1 | 위치 처리값;단위·현재 교정 미확정 |
| ZERO_TRASM_MV01 / COEFF_TRASM_MV01 | DB4.DBW204 / DBW206 Int;0676 RID219/218 AO1632/1648 | 0674 Coeff TOD4;현재값·설정 의도 미확보 |
| Encoder_CH00 / Encoder_CH00_10 | DB8.DBD0 DInt / DB8.DBW36 Int;0676 RID192/214 AO0/288 | 0674 Memory encoder TOD8;이름의 _10과 실제 /100 연산을 혼동 금지 |
| MV01_Encoder instance | DB15;0618/0673 TOD15 | 내부 S/IO offset를 일반 고정 DB 주소로 단정하지 않음 |

### 2.4 HMI 주소와 함수 호출을 분리

hmi_plc_tags.csv의 dde.cfg 설정 9행이다. 온라인 현재값/버튼 이벤트/권한/쓰기 성공을 뜻하지 않는다. [E18]

| HMI 태그 | 설정 주소 | ID |
| --- | --- | --- |
| RESET_ENC_MV01 | DB41,X50.5 | 00464 |
| MV_01\LimitSwitchOpen | DB11,X18.3 | 00316 |
| MV_01\LimitSwitchClose | DB11,X18.4 | 00315 |
| MV_01\Flag_OPEN | DB2,X3.3 | 00314 |
| MV_01\AutoMan | DB2,X7.2 | 00309 |
| MV_01\OutputOpen | DB11,X18.0 | 00308 |
| MV_01\Flag_CLOSE | DB2,X3.4 | 001A7 |
| MV_01\Allarme1 | DB11,X18.2 | 001A6 |
| MV_01\OutputClose | DB11,X18.1 | 001A0 |

LAD1190 0367의 CRef22/CodeBlock23은 HMI Standard Motorized Valve(0624 RID639 interface,0623 RID130)이다. 원본 NID는 단일 확정하지 못했다(공유 호출 후보 NID11/12/13/16). 14 실인수 중 4 FALSE는 선언 후보가 일관되며 10개는 미결속이다. network-map의 이름 순서를 핀의 증명으로 사용하지 않는다.

| 핀 | Wire/ORef/RID | 결속 상태 |
| --- | --- | --- |
| Ingresso_run_Opening | W47/24/693 | 미결속;색인은 Inputs.MV01 Run_Opening 후보 |
| Ingresso_run_Closing | W48/25/692 | 미결속;Inputs.MV01 Run_Closing 후보 |
| Allarme1 | W49/26/423 | 미결속;Allarm.MV01_FAULT 후보 |
| Allarme2 | W50/27/48 | 0626 Literal FALSE |
| Allarme3/4/5 | W51/28/20,W52/29/20,W53/30/20 | 0626 Literal false |
| Limit_switch_Open / Limiti_Switch_Close | W56/33/691,W57/34/690 | 미결속;Inputs 위치 후보 |
| Risposta_Opening / Risposta_Closing | W62/39/428,W63/40/429 | 미결속;Motors.MV01 응답 후보 |
| Limit_Switch_Open_HMI / Limit_Switch_Close_HMI | W64/41/430,W65/42/431 | 미결속;Motors.MV01 한계 후보 |
| Comulativo_allarmi | W68/45/434 | 미결속;Motors.MV01 집계 후보 |

HMI OutputOpen 표시를 물리 Q2.4 자체라고 단정하지 않는다. DB11 표시층과 Q 출력층을 따로 관찰해야 한다. 원본 오류 철자 Limiti_Switch_Close, Comulativo_allarmi를 추적 키에서 임의 변경하지 않는다.

## 3 제어 구조

### 3.1 startup과 수동 요청 해제

LAD404 0149 NID4: ON Contact337(W324/ORef314)→W338→SCoil293, 대상 Flag.MV01_Auto(W325/ORef315). 선언0563 RID42의 UID315 Write와 결속한다. startup 경로 존재는 현재 Auto 값이나 모든 재기동 동작의 증거가 아니다. [E08]

LAD1702 0342 NID1의 요청 해제는 다음과 같다. [E05]

- Open 요청 Reset: ON Contact226→ON228→(Inputs.MV01 Open Contact230 OR Close요청232 OR Auto234)→OR115→W189 RCoil119→W191/ORef162.
- Close 요청 Reset: 같은 ON 두 접점→(Inputs.MV01 Close Contact236 OR Open요청238 OR Auto240)→OR122→W195 RCoil126→W197/ORef166.
- 두 요청의 HMI 생성·외부 쓰기·스캔 우선순위는 이번 원본 사슬로 완료하지 않는다.

### 3.2 최종 열림·닫힘 출력

기호: A=Flag.MV01_Auto, U/D=UP/DOWN MV01 PID, O/C=수동 Open/Close요청, F=MV01_FAULT, LSo/LSc=처리 Inputs Open/Close, R=ResetEncoderProcedure_MV01, P=MV WORK PULSE. 다음은 **정적 접속식**이며 실행 모델/시뮬레이터가 아니다. [E05]

- Q2.4: ON AND NOT F AND ((A AND U) OR O) AND (P OR ON) AND NOT Q2.5 AND NOT LSo AND NOT R.
- Q2.5: ON AND NOT F AND ((((A AND D) OR C) AND (P OR ON)) OR R) AND NOT Q2.4 AND NOT LSc.

| 경로 | Part / Wire / ORef 핵심 |
| --- | --- |
| 공통 허가 | ON226 W184/157→W227→NOT Fault242 W199/167→W243 |
| 열림 자동/수동 | Auto244 W200/168→UP246 W201/169→OR137.in1;Open248 W203/170→in2;OR137.out W204 |
| 열림 펄스 병렬 | Pulse250 W205/171 OR ON252 W206/172→OR138→W207 |
| 열림 최종 차단 | NOT Qclose254 W208/173→W255→NOT LSopen256 W209/174→W257→NOT ResetProc23 W22/24→W25 Coil143→W211/175 |
| 닫힘 자동/수동 | Auto258 W212/176→DOWN260 W213/177→OR150.in1;Close262 W215/178→in2;OR150.out W216 |
| 닫힘 펄스 병렬 | Pulse264 W217/179 OR ON266 W218/180→OR151.in1/2 |
| 별도 닫힘 절차 | 공통 W243→ResetProc273 W276/274→W21 OR151.in3 |
| 닫힘 최종 차단 | OR151 W219→NOT Qopen268 W220/181→W269→NOT LSclose270 W221/182→W271 Coil156→W223/183 |

ON은 M0.0 심볼이다. 외곽 허가에도 ON이 있고 펄스와 병렬인 가지에도 같은 ON 선언이 있다. 따라서 이 네트워크만 보면 P=1만이 출력의 필수조건은 아니다. 두 출력의 소프트웨어 상호 차단과 FG44의 상대 접촉기 NC31/32는 별도 계층이다. 동시 요청 때 실제 우선 출력/접촉기 동작/안전성은 현재 프로그램·호출순서·실물을 확인하기 전 미확정이다.

### 3.3 엔코더 리셋 절차의 구동 영향

LAD1703 0354 NID14: ResetProc Contact21(W35/ORef27)→InputsClose Contact22(W37/ORef28)→W38 Move23.en. Move.in W39/ORef29는 0, out1 W41/ORef30은 **MV01_Encoder.NewCountValue**(0619 RID201). Move.eno W40→NOT SetCountValue Contact24(W42/ORef31)→W43 Coil25 SetCountValue(W44/ORef32), 그 out W45→RCoil26 ResetProc(W46/ORef33). [E06]

NewCountValue(SSD S=S AO320)와 SetCountValue(S=IO AO288)를 이름/순서로 뒤집지 않는다. 0506 HSC의 SetCountValue 실제 입력 핀은 미결속이므로 “이 값이 하드웨어 카운터를 확실히 0으로 완료”라고 쓰지 않는다. 논리상 닫힘 요청에 연결된 절차라는 점과 교정 완료는 별개다. 정상 극성·닫힌 기계 위치·엔코더 기준점·현재 설정을 확인하지 않고 버튼 조작을 권고하지 않는다.

### 3.4 공유 펄스와 명령 누적

LAD1712 0350 NID10: ON846→NOT Tag154 Contact848→SD813 Tag155 **S5T#200MS**(W834/ORef825), Tag155 Contact850→SD818 Tag154 **S5T#2S**(W838/ORef828), NOT Tag155 Contact852→Coil823 MV WORK PULSE(W844/ORef832). Tag154=T78(RID99),Tag155=T79(RID101), 선언0617. 이 공유 생성기의 200ms/2초와 MV01 최종 출력의 P OR ON을 함께 표시한다. [E07]

LAD1713 0351 NID11은 별도의 공유 10ms 타이머 사슬이다. [E10]

- ON1639→NOT Tag156 Contact1641→SD1225 Tag157, S5T#10MS(W1530/ORef1443);Tag1571643→SD1230 Tag156, S5T#10MS(W1534/ORef1446).
- Tag156=T118(0617 RID102),Tag157=T119(RID104). NOT Tag1571645→PBox1235.in W1646. PBox.bit W1540/ORef1450은 PLS 50 7 M50.7(RID105 AO407), 출력 비트가 아니라 에지 기억이다.
- PBox.out W1637→ON1647→Qopen1649: Add1248 W33+1→W33,Move1254 0→W34.
- 같은 공통 펄스→Qclose1651: Sub1263 W34−1→W34,Move1269 0→W33.
- W33 입력/출력 W1543/1545 ORef1453/1455;W34 0 W1546/1547 ORef1456/1457. W34 감산 W1550/1551/1552 ORef1459/1460/1461;W33 0 W1553/1554 ORef1462/1463.

이 사슬은 실제 회전 피드백으로 증분하지 않는다. Q와 펄스 조건에 따른 명령 누적이며, 출력 정지 때 매번 0으로 만드는 가지가 이 MV01 분기에 보이지 않는다. 지속시간·정확한 펄스 주기·누적 단위·retentive 여부는 현재 실행 자료가 필요하다.

### 3.5 엔코더 읽기와 값 처리

LAD1756 0506 NID50: NOT Simulation(1) Contact21(W51/ORef25)→EM_OK Contact22(W53/ORef26)→W54 LRef23.en. 0678 선언의 Simulation(1)은 M180.0, EM_OK는 I19.4(Input AO156)다. LRef23=High_Speed_Counter(0679 RID330),Instance24=MV01_Encoder DB15(0673 RID462). **EM_OK라는 이름으로 모든 안전 허가를 확인한 것으로 간주하지 않는다.** [E12]

확인 핀: SwGate=W55/ORef27→fill_unit1.CONTROL_SIGNALS.SW_GATE0(0676 RID207), ErrorAck=W58/ORef30 및 EventAck=W59/ORef31→Flag.RESET_ALLARM, CountValue=W75/ORef47→fill_unit1.ACT_CNTV0(0676 RID209,DInt). 이외 핀의 결속 공백은 아래 부록 표에 보존한다.

LAD1762 0512 NID31: [E13]

1. EM_OK Contact1113(W1087/ORef1064)→NOT raw MV01_Close Contact1115(W1088/ORef1065)→W1116. Coil1025는 SW_GATE0(W1089/ORef1066)을 쓴다. 처리 Inputs가 아닌 물리 입력 I8.2를 읽는 점을 구분한다.
2. 같은 W1116→Add1030: Memory encoder.Encoder_CH00 DInt(W1090/ORef1067)+fill_unit1.ACT_CNTV0 DInt(W1091/ORef1068)→local CNT_Act_0 DInt(W1092/ORef1069).
3. Add.eno W1093→Div1034: CNT_Act_0(W1094/ORef1070) / **100**(W1095/ORef1071)→local CNTV0_100 DInt(W1096/ORef1072).
4. Div.eno W1097→Move1038: local CNTV0_100(W1098/ORef1073)→Memory encoder.Encoder_CH00_10 **Int**(W1099/ORef1074). DInt→Int 경계·잘림/범위 영향을 임의 보정하지 않는다.
5. EM_OK→NOT SW_GATE0 Contact1117(W1101/ORef1075)→W1118:Move1047 0→Encoder_CH00_10(W1102/1103,ORef1076/1077),Move1052 INT#0→Encoder_CH00(W1104/1105,ORef1078/1079).
6. EM_OK 공통 W1114→Signal linearization CRef1059/CodeBlock1086(0680 RID351 interface/0672 RID5). IN0=W1107/ORef1081 ON;Analog_input=W1108/ORef1082 Encoder_CH00_10;Coeff=W1109/ORef1083 COEFF_TRASM_MV01;Zero=W1110/ORef1084 ZERO_TRASM_MV01;OutValue=W1111/ORef1085 Data.Pot_MV01;Out_of_range=W24/ORef23 Allarm.Pot_MV01_OFR.

LS24의 NC11/12 기호, 원시 I8.2, NOT 접점, SW_GATE0/메모리 0 쓰기는 각각 확인한 자료다. 이들을 근거 없이 “1이면 닫힘 정상”, “닫히면 반드시 카운터 리셋 완료”로 합치지 않는다. 물리 캠 접촉 위치·입력 정상 극성·호출 순서가 필요하다.

### 3.6 위치 선형화와 별칭 OFR

호출 대상 Signal linearization LAD1658 0291 NID1 및 LAD1659 0014 NID2를 별도 읽었다. [E14]

- IN0 Contact255→Analog_input **>−1382**(Gt258 W30/31) AND **≤32767**(Le161 W27/28)일 때 변환·계산 사슬이 열린다.
- Convert164/167로 Analog_input/Zero를 DInt App5/App6으로, Add170으로 합산,Convert174 Coeff→DInt App4, Mul177, Div181의 28000,Move185→OutValue Int. 식의 개략은 (Analog_input + Zero) × Coeff / 28000이지만 실제 Int/DInt 변환·정수 나눗셈·ENO 연쇄를 생략한 실수 비례식으로 시험하지 않는다.
- Analog_input>32767(Gt190 W36/37) OR Analog_input≤−1382(Le259 W38/39)→OR47 W49→Move193 −9999(W252/ORef218)→OutValue(W253/ORef219), Move.eno W21→일반 Coil23 Out_of_range(W22/ORef24).
- 선언0611:Analog_input Int RID3,Zero Int RID8,Coeff Int RID13,OutValue Int RID19,Out_of_range Bool RID26;중간 App3/4/5/6 DInt.0612 RID25=−1382,RID29=32767,RID17 DInt28000,RID21 Int−9999. 따라서 Int 입력의 >32767 가지를 “현실적으로 반드시 발생하는 상한 고장”으로 설명하지 않는다.
- 0014:NOT IN0 Contact171→Move162 0→OutValue(W169/170,ORef166/167). OFR은 별도 S/R 래치가 아니라 위 일반 Coil 경로다. 함수 미호출,ENO 실패,다른 쓰기,출력 복사 동작을 포함한 현장 해제 여부는 미확정이다.

Pot_MV01이라는 이름은 아날로그 포텐셔미터 실물의 증거가 아니다. 이번 OEM 도면은 ZT02 엔코더를 보인다. OFR과 MV01_FAULT의 비트·원인·해제 경로를 분리한다.

### 3.7 TC03 관련 CONT_S PID와 리미트

LAD11 0477 NID8:ON463(W413/ORef388)→W464 LRef366.en. LRef366 CONT_S(0671 RID113),Instance412 PIDMV01(0665 RID71,TOD DB21). NOT Auto465(W414/ORef389)→W466 COM_RST. [E15,E16]

| 핀 | Wire/ORef | 원본 결속값 |
| --- | --- | --- |
| CYCLE | W441/400 | T#100MS;0667 RID21 |
| SP_INT / PV_IN | W442/401,W443/402 | local Real_SP_TC03xMV01 / Real_TC03xMV01;0669 RID62/63,Real |
| GAIN | W446/403 | 3.0;0667 RID72 |
| TI | W447/404 | T#3M;0667 RID73 |
| DEADB_W / DISV | W448/405,W456/409 | 1.0;0667 RID24 |
| PULSE_TM | W453/406 | T#500MS;0667 RID74 |
| BREAK_TM | W454/407 | T#1S;0667 RID75 |
| MTR_TM | W455/408 | T#31S;0667 RID76 |
| QLMNUP / QLMNDN | W457/410,W458/411 | M12.0 / M12.1;0670 RID77/78 |

이는 백업의 호출 인자다. 권장 조정값·실제 모터 전행정 시간·현행 보호 설정이 아니다. 블록 이름의 “ogni100ms” 및 CYCLE100ms만으로 실제 OB 주기/지터를 검증하지 않는다.

SP/PV 두 지역변수의 선언에는 NID7 UID255/271 Write가 있으나 해당 상류 계산 본문은 이번 FlgNet 묶음에서 확보하지 못했다. TC03 관련 명칭과 읽기 핀은 확정하고, 실제 SP/PV 원천·스케일·보정식은 미확정으로 남긴다. [E15]

상한 LMNR_HS(W422)는 (ON AND Inputs.MV01 Open) OR (ON AND OFF AND Pot_MV01≥100)이다. 하한 LMNR_LS(W431)는 (ON AND Inputs.MV01 Close) OR (ON AND OFF AND Pot_MV01≤10)이다. 상한:ON467→Open469→OR348.in1,OFF471→Ge352(Pot W418/ORef393,100 W419/ORef394)→OR348.in2. 하한:ON473→Close475→OR357.in1,OFF477→Le361(Pot W427/ORef398,10 W428/ORef399)→OR357.in2. OFF는 M0.1 심볼이며 현재 false라고 가정하지 않는다. 100/10을 현장 개도% 제한이나 안전 설정으로 확정하지 않는다. [E16]

미결속 PID핀 9개:LMNS_ON W434/ORef433,LMNUP W436/435,LMNDN W438/437,PVPER_ON W440/439,PV_PER W445/444,PV_FAC W450/449,PV_OFF W452/451,PV W460/459,ER W462/461. 내부 인스턴스 기억·기본값·manual mode를 추정으로 채우지 않는다.

### 3.8 제어 소유와 다른 쓰기

- 최종 물리 Q2.4/Q2.5 쓰기:이번 정확한 심볼 참조에서 0342의 Coil143/156. 0555 monitor 참조는 쓰기로 집계하지 않는다.
- Auto 쓰기:startup0149 S293. HMI 태그 설정은 쓰기 가능성의 별도 자료이며 이벤트·현재 권한은 미확정.
- MV01_FAULT 쓰기:0159 S254/R342,0352 S1598/S1612. HMI 집계 후보는 별도 표시층이다.
- 위치값 쓰기:0512 Signal linearization OutValue. **기존 백업**의 0635 RID248에는 simulation 블록 NID2 UID112/147 Write도 남아 있다(network-map LAD1083/0403). 이는 원본에 다른 쓰기 선언이 존재한다는 범위만 기록한다. 해당 블록/시뮬레이터는 작성·변경·실행·행동시험하지 않았고 현재 활성이라고 주장하지 않는다.
- HSC gate·누적 메모리·NewCountValue 쓰기가 서로 다른 네트워크에 있다. 전체 호출 순서와 하드웨어 반영을 현재 CPU 없이 완료할 수 없다. 추출 참조 목록이 HMI·외부·간접 주소 쓰기까지 완전하다고 보장하지 않는다. [E17]

## 4 전기 전달 경로

아래 FG는 Electrical_Rev2.pdf의 인쇄 FG 번호이며 PDF 페이지는 1부터 센 실제 페이지다. 전체 파일명이 Rev2라고 모든 페이지 개정란을 Rev2로 쓰지 않는다. 실제 렌더를 페이지별 확인했다. [E19~E24]

| 원본 | 실제 PDF 페이지 | 개정란 확인 |
| --- | --- | --- |
| FG44 MV01 동력/접촉기 | 45 | 공란;기본 날짜27.05.2024 |
| FG45 ZT02·LS23/24 | 46 | 공란 |
| FG119 입력 모듈 | 120 | 공란 |
| FG124 입력 모듈 | 125 | Rev2 17.03.2025 |
| FG138 출력 모듈 | 139 | Rev2 17.03.2025 |
| FG144 TM1 Timer/encoder | 145 | 공란 |

### 4.1 C1 동력·보호·모터 끝점

FG44/PDF45:3상 440V60Hz 8.3L1/L2/L3→44QM1(도면 범위 **3.5–5A**)→44KM1/44KM2 역상 전력 접점→44U1/44V1/44W1→XM 같은 번호 단자→44QS1 1–2/3–4/5–6→M20 MV-01 U/V/W 및 PE. 도면 모터 표기는 **2.2kW,4.31A**다. [E20]

3.5–5A는 기기 표기 범위이며 현재 트립 설정 4.31A로 읽지 않는다. 모터 실명판·현재 교체 모델·회전방향·정격전류·보호 협조·실부하 전류는 미확정이다. 이 회로에 인버터 속도 파라미터나 공압 솔레노이드 값을 추가하지 않는다.

### 4.2 C2 열림/닫힘 코일과 공통 허가 귀로

FG138/PDF139 MOD14 단자25 A2.4→FG44 열림 가지→상대44KM2 NC31/32→44.1→44KM1 A1/A2. 단자26 A2.5→44KM1 NC31/32→44.2→44KM2 A1/A2. 두 A2 귀로가44.3에서 합류→44QM1 보조접점→44.4→XS29→44QS1 보조접점→XS30→−0Vdc10.6으로 이어진다. [E20,E23]

공통 귀로의 44QM1/44QS1은 코일 구동에도 영향을 주는 도면 경로다. 하단 접점표를 실제 부하선 접점번호로 대신 읽지 않았다. 도면상 코일 양단 및 상대NC31/32와 보조13/14를 구분한다. 보호/격리 접점의 단자 세부 번호가 그림에 없으면 추정하지 않는다. 물리 우회·접점 단락·출력 강제 동작을 제안하지 않는다.

### 4.3 C3 접촉기 응답 끝점

FG44:+24Vdc10.7→44KM1 보조13/14→E3.2(참조119/3)→FG119 MOD8 단자33. 닫힘은44KM2 보조13/14→E3.3(119/4)→단자34. [E21]

이 응답은 도면상 접촉기 보조 상태다. 밸브가 실제 이동했거나 끝 위치에 도달했다는 센서가 아니다. 코일 명령 Q,보조응답 I3.2/I3.3,한계LS,엔코더값을 분리한다.

### 4.4 C4 한계 LS23/24 끝점

FG45/PDF46:+24Vdc10.7→X1/112(5×20 2A F)→45.3→LS23 NC11/12→X1/113→E8.1→FG124/PDF125 MOD10 단자2. 닫힘은X1/114(2A F)→45.4→LS24 NC11/12→X1/115→E8.2→단자3. [E22,E23]

NC 기호와 단자11/12는 도면 사실이다. 현장 캠 위치별 입력전압,단선/정상 상태,raw/Inputs/HMI 위치 의미는 아직 확인하지 않았다. 이번 MV01 단자2/3을 인접 PV01 도면의 SPARE 오독과 혼합하지 않는다.

### 4.5 C5 ZT02 엔코더 끝점

FG45→FG144/PDF145 MOD16 TM1 Timer: [E22,E23]

| ZT02 단자·신호 | 중간 단자/선 | FG144 끝점 |
| --- | --- | --- |
| B +24Vdc | X1/107→37.1 | 단자9 공급 |
| C −0Vdc | X1/108→37.2 | 단자10 M |
| D | X1/109→45.1 | 단자1 CH0.A |
| E | X1/110→45.2 | 단자2 CH0.B |
| shield | X1/111→45SCH1 | 실드 접지 표기 |

CH0.N 단자3에는 이번 ZT02의 현장선이 표시되지 않는다. FG144 단자4/5/6의 E20.0/E20.1/E20.2 SPARE를 엔코더 카운트 주소로 연결하지 않는다. HSC 하드웨어 ID·채널 설정·입력모드·분해능·방향·배율·전기 형식은 현재 구성/실물 근거가 필요하다.

### 4.6 시공 자료와 OEM 상충

Electrical_Can_Decoating_20241118.pdf 실제 PDF51/57은 24.11.11 FIRST DRAFT 시공 설계다. OEM 전기도면과 다른 판본임을 유지한다. 길이는 설계표 값이며 실측이 아니다. [E24]

| PDF/행 | 전체 케이블 ID·FROM→TO | 명시 내용·해석 |
| --- | --- | --- |
| 51 /1_11 | =FLA+MV01-M20A,CR→MV01 M20 | MOTORIZED VALVE,GAC/CV,4 core,1.5,spare0,설계 LEN49 |
| 57 /7_1 | =FLA+HE01-FLO2TB1A→HE01 FLO2TB1 | LS17/18/23/24/21A/22A/21B/22B 공유 DC CVV25G1.0,spare8;전체를MV01전용으로 배정 금지 |
| 57 /7_5 | =FLA+HE01-FLO2TB1E→HE01 FLO2TB1 ZT02 | AI,CVV-S4S1.0,spare0 |
| 57 /7_8 | =FLA+MV01-LS23A,HE01 FLO2TB1→MV01 LS23 | DC,CVV2C1.0,E110,LEN5 |
| 57 /7_9 | =FLA+MV01-LS24A,HE01 FLO2TB1→MV01 LS24 | DC,CVV2C1.0,E120,LEN5 |
| 57 /7_10 | =FLA+MV01-ZT02A,HE01 FLO2TB1→MV01 ZT02 | **AI**,CVV-S4S1.0,E330,LEN6 |

ZT02의 AI 분류와 OEM 펄스 A/B→TM 도면 간 상충을 남긴다. 실물 모델/신호규격,준공 수정도,단자함 배선표,현재 TM 설정 없이는 어느 문서가 현행인지 정하지 않는다. 공유함 HE01 표찰만으로 MV01 본체 소유를 바꾸지 않는다.

## 5 알람·별칭·복구 경계

### 5.1 동일 고장 래치의 세 Set 경로

LAD1226 0159 NID1,Allarm.MV01_FAULT=DB3.DBX4.7. [E09]

- ON513(W425/ORef363)→ON515(W426/ORef364)→두 병렬 가지:Qopen517(W427/ORef365)→NOT Inputs.Run_Opening594(W597/ORef595),Qclose519(W428/ORef366)→NOT Inputs.Run_Closing590(W593/ORef591).
- 각 out W22/W21→OR242;OR.out W522→SD249.in 및Tag92 Contact523.in.
- SD249.value W431/ORef368=**S5T#150mS**,선언0571 RID77. operand W432/ORef369=Tag92,0570 RID9 Timer AO4=T4.
- Contact523 operand W433/ORef370 Tag92;out W524→SCoil254;대상W435/ORef371,0573 RID11 MV01_FAULT.

방향 응답 불일치 두 가지가 하나의 타이머 입력을 공유한다. 한계 도달·ZT02 미변화·과전류 자체를 직접 감시하는 타이머라고 설명하지 않는다. 실검출 지연은 입력갱신/호출/타이머 상태/스캔을 포함하므로150ms와 같다고 보장하지 않는다.

LAD1714 0352 NID12:ON1943(W1845/ORef1778)→ON1945(W1846/ORef1779)에서 두 비교가 열린다. [E11]

| 조건 | Set | 같은 조건의 값 초기화 |
| --- | --- | --- |
| W33 **>2000**:Gt1592,in1W1847/ORef1780,in2W1848/ORef1781 | outW1849→S1598→W1850/ORef1782 MV01_FAULT | Move1601 0 W1851/ORef1783→W1852/ORef1784 W33 |
| W34 **<−2000**:Lt1606,in1W1854/ORef1785,in2W1855/ORef1786 | outW1856→S1612→W1857/ORef1787 MV01_FAULT | Move1615 0 W1858/ORef1788→W1859/ORef1789 W34 |

선언0619 RID109/111 W33/W34,RID11 공통래치;상수는0620 RID145=2000 / RID147=−2000의 NID12 UID1781/1786 선언이다. >/<는 엄격 비교이며≥/≤로 바꾸지 않는다. Move0는 누적값에 대한 쓰기이고 알람 Reset이 아니다.

### 5.2 리셋·재발·재기동

0159의 Reset 경로는 **ON513→Flag.RESET_ALLARM575(W492/ORef412)→MV01_FAULT577(W493/ORef413)→W578 RCoil342→W495/ORef414**이다. Set 경로의 두 번째 ON515와 달리 Reset은 ON513에서 직접 분기한다. 이 Reset 가지에는 응답 정상화 조건이 별도 직렬로 보이지 않는다. [E09]

따라서 “Reset누르면 원인이 사라진다/즉시 정상 재기동된다”라고 쓰지 않는다. 원인 해소,리셋 요청,래치 해제,다른 Set 쓰기,모드/요청,최종 Q,접촉기응답,위치 변화는 별도 확인이다. W33/W34=0 또는 ResetProc 해제는 고장 복구 완료의 증거가 아니다.

### 5.3 알람 별칭·표시층

| 계층 | 확인 이름/주소 | 같은 것으로 볼 수 있는 범위 |
| --- | --- | --- |
| 고장 래치 | Allarm.MV01_FAULT DB3.X4.7 | 응답150ms·W33상한·W34하한의 공통 Set 대상 |
| HMI 호출 후보 | 0367 Allarme1←ORef26/RID423 | 색인은MV01_FAULT이지만 선언 미결속;확정 별칭으로 승격 금지 |
| HMI 집계 후보 | Comulativo_allarmi→ORef45/RID434 | Motors.MV01 집계 후보;핀결속 미확정 |
| HMI 태그 | MV_01\Allarme1 DB11,X18.2 | dde.cfg 설정만 확인;DB3비트와 다른주소 |
| 위치 범위 | Allarm.Pot_MV01_OFR DB3.X24.6 | 선형화 Out_of_range;MV01_FAULT와 별개 |
| HSC 상태 | Error/ErrorID/StatusHW 등 | 실제 실인수 미결속,별도 알람번호/리셋 완료를 만들지 않음 |

알람 코드·인버터 코드·추가 HMI 문구를 설비 이름만으로 생성하지 않는다. 오류 기록에는 최초 시각,정확한 태그/주소/층,방향명령,처리응답,원시값,설정 버전과 미확정을 함께 남겨야 한다.

## 6 증상별 조사·수리 문서 초안

다음은 **관찰 자료와 판단 분기**이며 조작·강제출력·보호값 변경 절차가 아니다. 활선 접근/전력부 점검은 자격 있는 담당자의 현장 안전 절차와 격리 기준을 전제로 별도 승인해야 한다. 이번에는 실행하지 않았다.

| 증상 | 우선 구분할 증거 | 판단 경계·필요 자료 |
| --- | --- | --- |
| 열림/닫힘 모두 명령 안 나옴 | ON,F,Auto,UP/DOWN,수동요청,양쪽한계,ResetProc,Q 상호차단 [E05] | HMI표시만으로 PLC출력불량 판정 금지;현재 호출·다른 쓰기 필요 |
| 한쪽 Q만 안 나옴 | 해당 한계/상대Q/요청 해제,열림의NOT ResetProc,닫힘 별도R가지 | 양방향 조건이 완전히 대칭이라고 설명하지 않음 |
| Q는 있는데 접촉기 응답 없음 | FG44 상대NC31/32,coil,공통44QM1/44QS1귀로,보조13/14→I3.2/3.3 [E20,E21] | Q=전압공급·접촉기흡입 증명 아님;전기적원인 단정/점퍼 제안 금지 |
| 150ms 고장 | Tag92입력,명령Q,raw응답/Inputs응답,Timer 상태,호출 경계 [E04,E09] | 모터막힘/엔코더불량/타이머너무짧음으로 즉시 결론 금지 |
| 일정 누적 뒤 고장 | W33/W34,명령방향,공유PBox,엄격±2000비교와0쓰기 [E10,E11] | 엔코더오차2000/20초보호로 환산 금지 |
| 접촉기는 동작하지만 밸브 안 움직임 | 보조응답과실제기구변위,동력경로·M20명판·기구연결 [E20,E21] | 보조접점은실회전증거 아님;보호설정상향/강제구동 금지 |
| 표시 위치가 고정/−9999 | ZT02 OEM A/B경로,EM_OK/gate/ACT_CNTV0,CH00/100,Int경계,Coeff/Zero,OFR [E12~E14,E22] | AI분류만으로4–20mA고장판정 금지;현재hardwareID필요 |
| 한계 표시 상충 | LS23/24 NC도면,raw/Inputs/DB11층,현재캠위치와원본극성 [E03,E18,E22] | 0/1 정상·두끝위치동시표시의원인을추정하지 않음 |
| ResetEncoder 후 이상 | R이닫힘요청에작용,NewCountValue/SetCountValue사슬,HSC미결속핀 [E06,E12] | 재교정조작권고 금지;실행전상태와승인된복구증거필요 |
| 자동제어만 이상 | COM_RST=NOT Auto,SP/PV지역변수,PID핀/리미트 [E15,E16] | GAIN/TI/MTR_TM변경권고 금지;상류계산·현재인스턴스미확정 |

관찰 기록 필드 초안:설비ID/태그,관찰자,시각·시간대,위치,프로젝트/백업해시,값·단위,수집장치,원시/처리/HMI구분,최초알람·방향요청,비교원본,배제된원인,미확정,승인된조치의근거,복구전후증거. 빈값은미확인으로 남긴다. 실제 운영 기록은 이 공개 초안에 채우지 않는다.

## 7 완료 기준·인계·누락 자료

### 7.1 7영역 적용표

| 영역 | 적용 상태 | 위치 | 미완료·비해당 이유 |
| --- | --- | --- | --- |
| 설비·자료 기준 | 적용 | §1,E01/02/25 | 실물identity=false 유지 |
| I/O·HMI | 적용/부분미결속 | §2,E03/04/18 | HMI10핀,원시태그3개선언결속 미확보 |
| 제어 구조 | 적용/부분미결속 | §3,E05~17 | PID9핀/HSC19핀,상류PID계산·현재호출 미확정 |
| 전기 전달 경로 | 적용 | §4,E19~24 | 실물모델·현행보호·준공변경 미확정 |
| 알람·복구 | 적용 | §5,E09/11/14/18 | 현장리셋/재기동/복구 미실행 |
| 증상별 수리 | 관찰중심초안 | §6 | 조작·시험·현장조치 미수행 |
| 완료 기준 | 적용 | §7 | UI/기록/배포/TIA/CPU/현장완료와분리 |

### 7.2 독립 통합자가 좁혀 확인할 사항

1. 0342의 **ON252/266 병렬 가지**,닫힘 ResetProc OR151.in3,열림 NOT ResetProc를 원본선언·Wire로 재확인한다. 다른댐퍼의출력식으로대체하지 않는다.
2. 0159 Tag92=T4/S5T#150mS와0352의동일래치/엄격비교를 확인한다. 누적값Move0와래치Reset을 분리한다.
3. 0354의NewCountValue/SetCountValue대상을 확인한다. HSC미결속SetCountValue핀을이름만으로이어붙이지 않는다.
4. 0512/0291의 /100,DInt→Int,−1382/32767,−9999,계수/영점순서를확인한다. Pot이름을실물포텐셔미터로단정하지 않는다.
5. 0477의SP/PV지역변수및9미결속핀,100/10비교의OFF가지,호출설정값과현재값경계를 유지한다.
6. FG44/45/119/124/138/144실제페이지·끝점·페이지별개정란 및시공PDF51/57AI상충을 재확인한다. 전체PDF를다시조사할필요없이해당페이지를우선한다.
7. HMI14실인수중4FALSE/10미결속,DB11표시와Q/DB3분리를 유지한다.
8. 기존완료/미확정/알수없는기록필드·초안을보존한뒤사용자범위에서UI·기록·보고서검증을담당한다. 이초안은그검증을대신하지않는다.

### 7.3 누락 자료와 필요한 근거

| 보류 | 이유 | 필요한 근거 |
| --- | --- | --- |
| 현재 CPU 일치/다른쓰기완전성 | 공개백업정적추출만확인 | 승인된프로젝트/온라인비교자료,호출트리·간접쓰기/HMI쓰기목록 |
| MV01 실물 동일성 | 태그/P&ID/케이블문서일치만확인 | 본체·M20·ZT02·단자함명판/표찰/준공도 |
| 정상극성·동작방향 | NC도면과논리NOT만으로확정불가 | 위치별raw/Inputs/HMI와캠/배선대조자료 |
| HMI10핀 | 원본ORef선언복원미결속 | 정확한HMI네트워크NID/인터페이스·실인수Export |
| HSC19핀/하드웨어채널 | 일부ORef미결속,TM구성없음 | DB15인터페이스·호출실인수,hardwareID/채널/분해능/배율자료 |
| PID9핀/SP·PV상류 | 지역변수NID7Write는있으나계산본문미확보 | 해당원본네트워크본문/정식Export·인스턴스설정 |
| 엔코더교정/AI상충 | OEM펄스도면과FIRST DRAFT AI분류상충 | ZT02실규격·최신단자도·채널구성·교정기록 |
| 보호값/모터정격 | 도면범위/설계값뿐 | 실명판·현행44QM1설정과승인근거 |
| 현장복구 | 실행/행동시험없음 | 원인해소·승인된재기동·실응답/위치/알람복구증거 |

### 7.4 네 기능·최종 상태

| 기능/상태 | 이번 결과 |
| --- | --- |
| 도면·래더 비교 | 지정XML/선언/핀·PDF실제페이지정적대조,근거표제공 |
| 백업·선택복원 | 초안에보존요건만기재;구현/시험미수행 |
| 기록 전후 비교 | 관찰필드와원시/처리/HMI구분초안;구현/시험미수행 |
| 보고서/PDF | MD초안첨부대상;앱보고서/A4PDF시험미수행 |
| documentation | draft_ready;통합완료아님 |
| static_review | 지정원본대조완료,미결속/경계보존;현재프로그램전체검증아님 |
| ui_records | not_run |
| publication | not_published_by_Dots |
| tia_compile / live_cpu / field_recovery | not_performed 각각유지 |

완료 산출물은 MV01 한 개의 조사·문서 초안이다. 다음 승인 순서 후보는 **MV03 한 개**이며 이번에 착수하지 않았다. 2차133후보를조사범위에추가하지않았다.

## 부록 A 핵심 주장 근거표

원본 전체 경로와 SHA-256은 부록 C에 연결한다. Flg/Ident 약칭은 §1.3의 decoded-original 경로다. 아래 해석은 지정 백업에 한정한다.

| ID | 주장 | 원본 | 위치·핀·선언 | 해석/미확정 경계 |
| --- | --- | --- | --- | --- |
| E01 | 설비 식별/소유 | docs/equipment-standard/INVENTORY.json;WORK-STANDARD.md;WORK-ITEM-TEMPLATE.md | P19→MV01,identity_verified=false,parent_id=null | 태그 대응/문서 완료와 실물 동일성을 분리 |
| E02 | P&ID 역할 | all-in-one/sources/PID_1684n002I.pdf | PDF1 HE01 우측 MV01/M20/LS23/24/ZT02,2.2kW440V | 유로 인접 관계;HE01 본체 소유/현재 정격은 미확정 |
| E03 | 원시 I/O/처리 주소 | live_index.json;0617/0618/0619/0573/0678 Ident | doc885/886/889/1528;RID15/14 SAD Q AO20/21;Inputs RID59/60 AO26/27,RID172/173 AO65/66 | 원시 3태그는 색인+도면;동명SimpleAccess 직접 미결속 |
| E04 | 입력 복사/호출 | 0397/0030 Flg;0627/0628/0629/0690/0691/0692 Ident | LAD1070 Move27 W31/32 ORef28/29;Move43 W55/57 ORef47/48;LAD1613 W32/33/42/44/43 | IW2/8→DB13W2/8,ENO/NOT Simulation(1) M180.0 경계;다른쓰기/현재CPU 미확정 |
| E05 | 최종 출력·요청 해제 | 0342 Flg;0617/0618/0619 Ident | LAD1702 NID1,C143/C156,R119/R126,OR138/151,Contact252/266 ON,273 ResetProc | §3.1/3.2의 접속식;상호차단·별도닫힘요청;현재 실행 우선순위 미확정 |
| E06 | 리셋 절차 | 0354 Flg;0618/0619/0620 Ident | LAD1703 NID14,Move23 W39/41,Contact24 W42,Coil25 W44,R26 W46;RID201/202 | NewCountValue→SetCountValue→절차Reset;하드웨어0설정완료는 미확정 |
| E07 | 공유 작업 펄스 | 0350 Flg;0617/0620 Ident | LAD1712 NID10,SD813/818,C823;Tag154T78/Tag155T79;200ms/2s | 공유생성기;최종출력은P OR ON이므로필수간헐구동으로일반화금지 |
| E08 | startup Auto | 0149 Flg;0561/0563 Ident | LAD404 NID4,Contact337 W324,RID42/ORef315→S293 W325 | 시작 Set 경로;현재Auto/재기동 결과미확정 |
| E09 | 150ms 공통 fault/Reset | 0159 Flg;0570/0571/0572/0573 Ident | LAD1226 NID1,OR242/SD249/S254/R342;W431/432/433/435/492/493/495 | Tag92=T4 S5T#150mS;두방향불일치공유;Reset에정상화직렬조건없음 |
| E10 | 명령 누적 생성 | 0351 Flg;0617/0618/0619/0620 Ident | LAD1713 NID11,T118/T119 10ms,PBox1235 bitM50.7;Add1248/Sub1263/Move1254/1269 | Q방향명령누적;엔코더실측/실시간초단위아님 |
| E11 | 누적 초과 fault | 0352 Flg;0618/0619/0620 Ident | LAD1714 NID12,Gt1592/S1598/Move1601,Lt1606/S1612/Move1615;RID145/147 | W33>2000,W34<−2000;같은래치 Set과누적0쓰기분리 |
| E12 | HSC 호출·미결속 | 0506 Flg;0673/0674/0676/0678/0679 Ident | LAD1756 NID50,LRef23/Instance24,Contact21 NOT Simulation(1),22 EM_OK,W54;CountValue W75 | DB15/HSC;실인수19핀미결속;현재하드웨어구성미확정 |
| E13 | 엔코더 처리 | 0512 Flg;0672/0674/0675/0676/0677/0678/0680 Ident | LAD1762 NID31,Coil1025/Add1030/Div1034/Move1038/1047/1052,CRef1059 | rawClose NOT,gating,CH00+ACT_CNTV0,/100,DInt→Int,선형화호출 |
| E14 | 선형화/OFR 별도알람 | 0291/0014 Flg;0611/0612 Ident | LAD1658/1659 NID1/2,Gt258/Le161/Convert164/167/Add170/Mul177/Div181/Move185/193/Coil23 | −1382초과·32767이하,정수연산/−9999/일반OFRcoil;설정/현장해제미확정 |
| E15 | PID 호출·인자 | 0477 Flg;0665/0667/0668/0669/0670/0671 Ident | LAD11 NID8,LRef366/Instance412,COM_RST W466,SP/PV W442/443;9미결속핀 | CONT_S DB21,원본시간/GAIN;NID7지역변수상류계산본문미확보 |
| E16 | PID 한계 분기 | 0477 Flg;0667/0668/0670 Ident | OR348/357,Ge352 W418/419,Le361 W427/428,ON467/473,OFF471/477 | Inputs한계 OR ON/OFF/위치비교;100/10을현행개도%로단정금지 |
| E17 | 다른 쓰기/소유 경계 | 0555/0563/0617/0619/0635/0636/0676 Ident;network-map.json | 정확심볼AK검색;Data.Pot_MV01 0635 RID248 NID2 UID112/147 Write | 백업의기존다른쓰기존재만기록;시뮬레이터미실행·현재활성미확정 |
| E18 | HMI 주소/함수 | hmi_plc_tags.csv;0367 Flg;0623/0624/0626 Ident | LAD1190 CRef22/CodeBlock23,14실인수;FALSE4/미결속10;dde.cfg9행 | 표시DB11/요청DB2/절차DB41과물리Q·DB3래치분리 |
| E19 | 페이지 개정란 | Electrical_Rev2.pdf | FG44/45/119/124/138/144 각각PDF45/46/120/125/139/145 | FG124/138만이번6페이지중Rev2;나머지공란 |
| E20 | 동력·코일 경로 | Electrical_Rev2.pdf | FG44/PDF45,44QM1/44KM1/2/44QS1/XM/M20;coil귀로XS29/30 | 2.2kW4.31A도면값,3.5–5A범위;현재보호/실물미확정 |
| E21 | 접촉기 응답 | Electrical_Rev2.pdf | FG44/PDF45 보조13/14→E3.2/3.3;FG119/PDF120 MOD8단자33/34 | 접촉기보조응답이지밸브도달/실회전증거아님 |
| E22 | LS·ZT02 현장 끝점 | Electrical_Rev2.pdf | FG45/PDF46,X1/107~115,LS23/24 NC11/12,ZT02 B/C/D/E | 한계센서·엔코더선분리;정상극성/현재센서모델미확정 |
| E23 | 모듈 끝점 | Electrical_Rev2.pdf | FG124/PDF125 MOD10단자2/3;FG138/PDF139 MOD14단자25/26;FG144/PDF145 MOD16단자1/2/9/10 | I8.1/8.2,Q2.4/2.5,A/B전달;E20.0등SPARE를카운트주소로추정금지 |
| E24 | 시공 케이블/AI상충 | Electrical_Can_Decoating_20241118.pdf | PDF51 row1_11;PDF57 row7_1/5/8/9/10 | M20,LS23/24,ZT02전용/공유분리;AI와OEMpulse상충,설계LEN≠실측 |
| E25 | 기존 자료 보존 | devices/control-specs/alarm-guides/circuit-guides/signal-guides/construction-guides/procedures/MV01.html | 기존MV01자료만읽기,공유네트워크인접행구분 | 원본/완료/미확정유지,다른설비항목수·값복제없음 |

## 부록 B HSC 미결속 핀과 원본 추적

0506 LRef23의 실제 핀 연결이다. ORef가 존재해도 실인수 선언을 결속하지 못하면 실제 값·대상 주소는 미확정이다. 이름으로 DB15 내부 멤버와 연결하지 않는다.

| 핀 | Wire/ORef | 결속/상태 |
| --- | --- | --- |
| SwGate | W55/ORef27 | 0676 RID207 fill_unit1.CONTROL_SIGNALS.SW_GATE0 |
| CaptureEnable | W56/ORef28 | 미결속 |
| SyncEnable | W57/ORef29 | 미결속 |
| ErrorAck | W58/ORef30 | Flag.RESET_ALLARM |
| EventAck | W59/ORef31 | Flag.RESET_ALLARM |
| SetCountValue | W60/ORef32 | 미결속 |
| StatusHW | W61/ORef33 | 미결속 |
| StatusGate | W62/ORef34 | 미결속 |
| StatusUp | W63/ORef35 | 미결속 |
| StatusDown | W64/ORef36 | 미결속 |
| CompResult0 | W65/ORef37 | 미결속 |
| CompResult1 | W66/ORef38 | 미결속 |
| SyncStatus | W67/ORef39 | 미결속 |
| CaptureStatus | W68/ORef40 | 미결속 |
| CapturedValue | W69/ORef41 | 미결속 |
| ZeroStatus | W70/ORef42 | 미결속 |
| PosOverflow | W71/ORef43 | 미결속 |
| NegOverflow | W72/ORef44 | 미결속 |
| Error | W73/ORef45 | 미결속 |
| ErrorID | W74/ORef46 | 미결속 |
| CountValue | W75/ORef47 | 0676 RID209 fill_unit1.ACT_CNTV0 DInt |
| MeasuredValue | W76/ORef48 | 미결속 |
| CompareMeasuredValue | W77/ORef49 | 미결속 |

알람 시간·펄스 시간·PID 시간은 서로 다른 쓰임이다. 이번 대상과 공유 사슬에서 확인한 값만 아래 묶었다.

| 구분 | 원본 값 | 원본 선언/핀 |
| --- | --- | --- |
| 방향응답 감시 | S5T#150mS | 0159 SD249.value W431/ORef368,0571 RID77;Tag92 T4 |
| 공유 작업 펄스 | S5T#200MS / S5T#2S | 0350 SD813/818,0620 시간상수,0617 Timer;Tag155 T79/Tag154 T78 |
| 공유 누적 에지 | S5T#10MS 두 타이머 | 0351 SD1225/1230,0620;Tag157 T119/Tag156 T118 |
| PID CYCLE/TI/PULSE_TM/BREAK_TM/MTR_TM | T#100MS / T#3M / T#500MS / T#1S / T#31S | 0477 W441/447/453/454/455,0667 RID21/73/74/75/76 |

## 부록 C 원본 고정점과 SHA-256 78개

기준 커밋 89570f755b3a01cffd80e3e36bea3bf1da403da9의 파일 바이트를 읽어 계산했다. 원본 보존/재대조용이며 파일 전체를 실행·컴파일·모든 페이지 검증했다는 뜻은 아니다. 특히 ZAP18/PLF는 백업 기준 해시이며 TIA로 열거나 다운로드하지 않았다. 원본 링크는 고정 커밋을 가리킨다.

| 원본 경로 | SHA-256 |
| --- | --- |
| [AGENTS.md](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/AGENTS.md) | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 |
| [.agents/skills/gme-equipment-rollout/SKILL.md](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/.agents/skills/gme-equipment-rollout/SKILL.md) | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b |
| [docs/equipment-standard/WORK-STANDARD.md](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/docs/equipment-standard/WORK-STANDARD.md) | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 |
| [docs/equipment-standard/WORK-ITEM-TEMPLATE.md](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/docs/equipment-standard/WORK-ITEM-TEMPLATE.md) | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 |
| [docs/equipment-standard/INVENTORY.json](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/docs/equipment-standard/INVENTORY.json) | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc |
| [VERSION.json](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/VERSION.json) | 43cf3a23a7294f116a7e366df5929dfb141e88dc3254f8e62e1e11fcd7330691 |
| [all-in-one/sources/Electrical_Rev2.pdf](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/Electrical_Rev2.pdf) | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| [all-in-one/sources/Electrical_Can_Decoating_20241118.pdf](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/Electrical_Can_Decoating_20241118.pdf) | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| [all-in-one/sources/PID_1684n002I.pdf](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/PID_1684n002I.pdf) | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| [all-in-one/sources/GME_20250506.zap18](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/GME_20250506.zap18) | 00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8 |
| [all-in-one/sources/PEData.plf](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/PEData.plf) | 647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a |
| [all-in-one/sources/source-manifest.json](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/source-manifest.json) | 5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf |
| [all-in-one/sources/live_index.json](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/live_index.json) | 14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1 |
| [all-in-one/sources/hmi_plc_tags.csv](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/hmi_plc_tags.csv) | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
| [all-in-one/sources/hmi-windows.csv](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/hmi-windows.csv) | 15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e |
| [all-in-one/sources/decoded-original/network-map.json](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/network-map.json) | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 |
| [all-in-one/sources/decoded-original/0014-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0014-FlgNet.xml) | 2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30 |
| [all-in-one/sources/decoded-original/0030-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0030-FlgNet.xml) | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b |
| [all-in-one/sources/decoded-original/0149-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0149-FlgNet.xml) | bc2519cdad49a7268006b194e8e5e1160744ff221f04b83e710f31f57bc617f9 |
| [all-in-one/sources/decoded-original/0159-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0159-FlgNet.xml) | 5598abbad86ed26fa8dd17fc3eca3e1c0b7941a2798db6ae1e2472a7ca448d2a |
| [all-in-one/sources/decoded-original/0291-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0291-FlgNet.xml) | fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550 |
| [all-in-one/sources/decoded-original/0342-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0342-FlgNet.xml) | 9ef93abad16cc055509ef98c388417c716cb03d23cb02aed6d95888beb43bef8 |
| [all-in-one/sources/decoded-original/0350-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0350-FlgNet.xml) | 3f426a4ba9455160b8113df968b1052752a7b72cdfca8e57bdfd466340d691ff |
| [all-in-one/sources/decoded-original/0351-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0351-FlgNet.xml) | 1448cd179747074ae5ac3647c52e47950d18e0d90fa2f1cb155dbb24af50a7f6 |
| [all-in-one/sources/decoded-original/0352-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0352-FlgNet.xml) | 03e2d68dda289fcb7e7738c2f52e675890b252f5b526cab1ec2049323ab30d75 |
| [all-in-one/sources/decoded-original/0354-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0354-FlgNet.xml) | 626eb4d21b9409ae50ed32436972c8a4284fcc029c10db5c5529463544b2ffbd |
| [all-in-one/sources/decoded-original/0367-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0367-FlgNet.xml) | 7e1a0c6776177463d5ffe7307a991484f97e8e5c5863f00d9597950458482bc5 |
| [all-in-one/sources/decoded-original/0397-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0397-FlgNet.xml) | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 |
| [all-in-one/sources/decoded-original/0477-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0477-FlgNet.xml) | e7b5b0cb95c60d1112081f6129a3127f8413e1b1d2a4c67d0e203d36ea0a711a |
| [all-in-one/sources/decoded-original/0506-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0506-FlgNet.xml) | 71b9ac920eb891ec8965506c40ae3f1d050a2f8a899f79f6afdc81f669717fbe |
| [all-in-one/sources/decoded-original/0512-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0512-FlgNet.xml) | 9437caf0fc524d25925ca5beb3c3bf1a2a0709a478a2981e42e5abe1e4471795 |
| [all-in-one/sources/decoded-original/0555-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0555-IdentXmlPart.xml) | 46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6 |
| [all-in-one/sources/decoded-original/0561-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0561-IdentXmlPart.xml) | ac8a4f7b366a262b9d488b5b78aabe8b2dea768753b58993fe7f846989dac0d7 |
| [all-in-one/sources/decoded-original/0562-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0562-IdentXmlPart.xml) | 85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c |
| [all-in-one/sources/decoded-original/0563-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0563-IdentXmlPart.xml) | 86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad |
| [all-in-one/sources/decoded-original/0570-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0570-IdentXmlPart.xml) | 9fed133006458c3b43b1d5f2c15107a5a86b4fb7cdbaf3743bf88f0e5a105495 |
| [all-in-one/sources/decoded-original/0571-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0571-IdentXmlPart.xml) | 4a9deeb65a22e497e284fe6d98929e1d201ef5939e4aeca5805b4eb7e007d398 |
| [all-in-one/sources/decoded-original/0572-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0572-IdentXmlPart.xml) | 5ecd18f84e12d702bb46f759b23994dacfa2d97d50fe51e766ca0cf43f75bb4c |
| [all-in-one/sources/decoded-original/0573-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0573-IdentXmlPart.xml) | a22cc24a974e0c792f32e356a14b277a847e2bb204c91bce01c37d1714ddb56c |
| [all-in-one/sources/decoded-original/0611-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0611-IdentXmlPart.xml) | 0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089 |
| [all-in-one/sources/decoded-original/0612-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0612-IdentXmlPart.xml) | 95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38 |
| [all-in-one/sources/decoded-original/0617-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0617-IdentXmlPart.xml) | 10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9 |
| [all-in-one/sources/decoded-original/0618-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0618-IdentXmlPart.xml) | 0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c |
| [all-in-one/sources/decoded-original/0619-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0619-IdentXmlPart.xml) | 85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456 |
| [all-in-one/sources/decoded-original/0620-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0620-IdentXmlPart.xml) | da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3 |
| [all-in-one/sources/decoded-original/0623-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0623-IdentXmlPart.xml) | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 |
| [all-in-one/sources/decoded-original/0624-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0624-IdentXmlPart.xml) | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a |
| [all-in-one/sources/decoded-original/0626-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0626-IdentXmlPart.xml) | a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b |
| [all-in-one/sources/decoded-original/0627-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0627-IdentXmlPart.xml) | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| [all-in-one/sources/decoded-original/0628-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0628-IdentXmlPart.xml) | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd |
| [all-in-one/sources/decoded-original/0629-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0629-IdentXmlPart.xml) | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| [all-in-one/sources/decoded-original/0635-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0635-IdentXmlPart.xml) | 1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457 |
| [all-in-one/sources/decoded-original/0636-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0636-IdentXmlPart.xml) | ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca |
| [all-in-one/sources/decoded-original/0665-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0665-IdentXmlPart.xml) | 50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd |
| [all-in-one/sources/decoded-original/0667-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0667-IdentXmlPart.xml) | ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3 |
| [all-in-one/sources/decoded-original/0668-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0668-IdentXmlPart.xml) | 2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed |
| [all-in-one/sources/decoded-original/0669-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0669-IdentXmlPart.xml) | 754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2 |
| [all-in-one/sources/decoded-original/0670-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0670-IdentXmlPart.xml) | e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841 |
| [all-in-one/sources/decoded-original/0671-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0671-IdentXmlPart.xml) | 26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293 |
| [all-in-one/sources/decoded-original/0672-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0672-IdentXmlPart.xml) | 6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222 |
| [all-in-one/sources/decoded-original/0673-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0673-IdentXmlPart.xml) | 450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58 |
| [all-in-one/sources/decoded-original/0674-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0674-IdentXmlPart.xml) | 4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84 |
| [all-in-one/sources/decoded-original/0675-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0675-IdentXmlPart.xml) | b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3 |
| [all-in-one/sources/decoded-original/0676-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0676-IdentXmlPart.xml) | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 |
| [all-in-one/sources/decoded-original/0677-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0677-IdentXmlPart.xml) | 69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3 |
| [all-in-one/sources/decoded-original/0678-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0678-IdentXmlPart.xml) | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 |
| [all-in-one/sources/decoded-original/0679-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0679-IdentXmlPart.xml) | d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56 |
| [all-in-one/sources/decoded-original/0680-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0680-IdentXmlPart.xml) | fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95 |
| [all-in-one/sources/decoded-original/0690-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0690-IdentXmlPart.xml) | fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541 |
| [all-in-one/sources/decoded-original/0691-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0691-IdentXmlPart.xml) | 17cb7d9734d76b39e729e0daf0c89d9bdf74907aab2130c80453fa04e4cea1da |
| [all-in-one/sources/decoded-original/0692-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/sources/decoded-original/0692-IdentXmlPart.xml) | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| [all-in-one/devices/MV01.html](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/devices/MV01.html) | cf6dbf7354bf8fb7c32462374baf18ab2d8ce78f931979bce9ec1e236aba103f |
| [all-in-one/control-specs/MV01.html](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/control-specs/MV01.html) | dfba18f32aafe7f6ccae19cca4240c8d8de5f3fe9fa5a946b6b6446ed590bdc8 |
| [all-in-one/alarm-guides/MV01.html](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/alarm-guides/MV01.html) | c2610e11485bb31577e2f5c467ebaf329531e4e46de6befc78dd9369e4027fa8 |
| [all-in-one/circuit-guides/MV01.html](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/circuit-guides/MV01.html) | dbb677b33b727396e1029893088da7ff833ba142c23d6ae7c49208eefce57966 |
| [all-in-one/signal-guides/MV01.html](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/signal-guides/MV01.html) | 232516fbb4a470f0d15d8cb08817a49a2923cd25a8a78daa3cac8dae09b5f4e0 |
| [all-in-one/construction-guides/MV01.html](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/construction-guides/MV01.html) | 54200da3b8f6811c6c208bec8388aa5f221b5c2dab3882fa35e22a020ebc0183 |
| [all-in-one/procedures/MV01.html](https://github.com/esp6662266/gme-plc-manual/blob/89570f755b3a01cffd80e3e36bea3bf1da403da9/all-in-one/procedures/MV01.html) | 19ddedf0963f341b6bf84ea5ae3f6f608765ed26c49b623cc9addee98d637922 |

## 부록 D 수행 범위와 인계 상태

- 수행: 고정 공개 원본의 파일 읽기, XML 파싱·정적 Part/Wire/선언 대조, PDF 지정 페이지 렌더/시각 확인, SHA-256 계산, 이 MD 작성. 생성·편집 파일은 자체 조사 폴더의 초안/추출 메모/렌더뿐이다.
- 원본 worktree의 git status는 깨끗함을 확인했다. 원본/공통 코드/버전/대장/운영 기록/배포 파일을 수정하지 않았다.
- 실행하지 않음: 프로젝트 생성기/npm검사/시뮬레이터/행동시험/TIA컴파일/실제PLC다운로드·조작/현장시험/보호값변경.
- 사용자의 PV01/PV02 접점 정정(2026-10-11 16:19 KST)은 별도 연구 정정에 기록했고 원첨부를 보존했다. 해당 릴레이 EV 부하 접점은5–9이며 MV01 접촉기31/32·13/14와 혼합하지 않는다. 사용자 단독 로컬 정정·검증·게시 범위를 유지한다.
- 이 초안의 완료는 문서 작성 완료다. MV01 기능 통합·게시·현장 복구 완료가 아니다.

