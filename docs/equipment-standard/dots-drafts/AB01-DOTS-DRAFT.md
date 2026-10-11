# AB01(P12) 재연소로 후보 — Dots 원본 조사·문서 초안

- 기준: esp6662266/gme-plc-manual, 고정 커밋 abcf31c5030bc7ef8749ed8e869a857f2387a28a, 프로그램 v1.12.0, 조사일 2026-10-11. 이 버전은 조사 자료의 기준이며 AB01 신규 게시나 현재 CPU 버전의 확인을 뜻하지 않는다.
- 대상: catalog_id AB01, priority_key P12, 우선 목록 이름 재연소로, 대장 이름 연소 챔버, 유형 passive. mapping=candidate, identity_verified=false, queue_state=identity_review를 유지한다.
- 범위: 공유 조사 환경에서 원본 읽기, 실제 PDF 렌더 대조, 이 독립 초안 작성. 사용자 Codex가 유일한 로컬 반영·검증·배포 담당이다. 새 Work/Codex를 만들지 않았다.
- 보존: 원본, 기존 AB01 완료 분석, 다른 설비, 공통 코드·버전·대장·배포·운영 기록을 편집하지 않았다. 시뮬레이터 작성/수정/생성/실행/행동시험, 실제 PLC·현장·보호값·SEJIN 변경은 수행하지 않았다.
- 작업표준: GME-STD-1.0.0, rollout SKILL, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY. 실행 모델·추론 수준의 제품 화면상 선택은 미확인이다. 아래는 정적 문서 조사 결과이며 실물·컴파일·안전성 판정이 아니다.


## 먼저 유지해야 할 경계

- AB01 본체, BR01 버너, 외부 버너반, 주변 온도·산소 계측과 댐퍼는 별도 소유다. 기존 직접 명세는 입력 참조 2, 출력 0, HMI 0, 직접 네트워크/규칙 0이다. 관련 30개 네트워크를 본체 직접 제어 30개로 바꾸지 않는다.
- TC01/TC02의 OEM 명칭은 AB01 챔버 온도지만, 시공 PDF3/56은 HE01 구역으로 묶는다. 시공 구역·케이블 도착 위치와 센서 실제 취출 위치·본체 identity를 합치지 않는다.
- MAX와 MAXMAX는 각각 6초지만 조건·Reset·버너 영향이 다르다. MAX는 선택온도 < (설정−5)의 자동 Reset, MAXMAX는 RESET_ALLARM와 자기 래치에 의한 Reset이다. 후자 Reset 가지에는 원인해소 접점이 없다.
- TC01/02 차온 알람은 NOT disable, 두 채널 중 하나 >400, 차이 <−100 또는 >100, 1분이다. AND나 ≥±100으로 바꾸지 않는다. 산술 ENO의 직렬 유무도 보존한다.
- TC07, RO01, RO02 환산 호출의 외부 허가 접점은 OFF다. 호출 내부 IN0는 ON이다. 이름을 상수로 바꾸거나 현재 미사용/사용으로 확정하지 않는다.
- HMI ResetAlarms DB2.X13.4와 PLC RESET_ALLARM DB2.X6.0은 별도다. 원본 공통 알람 관리에서 요청을 전달·자기 해제한다. Reset을 온도 정상화나 버너 재기동 허가로 취급하지 않는다.
- 선택 SCL1719 본문은 백업 검색색인 문자 근거다. 관련 네이티브 선언은 추가 확인했지만 원형 SCL 본문·컴파일 listing·현재 CPU는 여전히 없다. TC02-only 분기의 TC01_OFR/EnableTC01 문자를 임의 정정하지 않는다.
- P&ID의 850°C·O₂=±4% 및 원본 비교·시간 수치는 과거 자료다. 현재 운전·안전 설정 권고값으로 사용하지 않는다.


## 1. 설비·자료 기준


### 1.1 식별과 공정 관계 [E01–E03]

P&ID PID_1684n002I.pdf 실제 1쪽을 회전 렌더하여 확인했다. AB01 세로 본체 하부 쪽에 BR01과 FEED BURNER 참조 35602201_00, 본체 측 TC01/TC02, 출구 쪽 RO01/RO02와 PSH03, 상부 유입 쪽 MV05와 TC07이 표시된다. AB01 출구 관로의 화살표는 HE01 하부 쪽으로 향한다. 이 공정도에서 기능 관계를 읽을 수 있지만 실제 현장 명판·설치 위치가 P12 재연소로와 동일하다는 증명은 아니다.

OEM Electrical_Rev2의 FG97/PDF98은 별도 010-390 ELECTRIC PANEL BURNER COMMAND TYPE BP N300을 참조한다. P&ID의 35602201_00과 같은 도면·판본이라고 합치지 않는다. 외부 제어기의 퍼지, 점화, 화염 감시, 연료 차단, 재기동 안전 순서는 미확보다.

시공 PDF3은 ENTRY/AB01에 6SB2, FLOW_A/AB01에 TC07, FLOW_A/HE01에 TC01–02/RO01–02/PSH01/PSH03을 표시한다. PDF6도 ENTRY AB01/6SB2를 표시한다. 동일 AB01 문자열이 다른 구역 행에 있는 사실을 보존한다. CC01행에 BR01이 있는 것은 시공 배치/간선 자료이며 버너나 본체의 제어 소유를 바꾸는 근거가 아니다.


### 1.2 기존 자료 보존 [E04]

기존 AB01-INVESTIGATION.md, registers/ab01-independent-investigation.json, body-manual.json, devices/AB01.html, control-specs/AB01.html, construction-guides/AB01.html, procedures/AB01.html의 기존 분석·미확정을 읽기 참조했다. 이번 초안은 기존 MAX/MAXMAX·차온·BR01 경계를 재검토하고 실제 회로·HMI 전달·호출/계측 경계를 보강한다. 기존 완료를 재초기화하거나 기존18불일치/1060확인 대기/577설계시험을 새 완료로 변경하지 않는다.


### 1.3 표기와 증거 수준

- NNNN은 all-in-one/sources/decoded-original/NNNN-FlgNet.xml 또는 NNNN-IdentXmlPart.xml이다. LAD는 network-map의 document_id이며 NID는 선언 네트워크 식별자다.
- Part, Wire, ORef/CRef/CodeBlock의 UID와 선언 RID 및 C.NID/UID를 별도로 결속했다. UID/RID 숫자가 같은 다른 블록의 선언을 혼합하지 않는다.
- AO는 선언 비트 오프셋이다. DB 번호는 BAD/BIRID와 DepDBBlock의 TOD N으로 별도 확인했다. Timer AO는 타이머 번호로 읽으며 바이트 주소처럼 나누지 않는다.
- 원본 XML/도면, 백업 색인·HMI 설정 CSV, 파생 대장, 현장 관찰은 서로 다른 증거다. 이번에 현장 관찰은 없다.


## 2. I/O·HMI와 계측 전달


### 2.1 관련 원시 입력과 환산 데이터 [E05–E08]

아래 채널은 AB01 주변 계측 참조다. 모든 채널을 본체 직접 I/O로 편입하지 않는다. XML Input/SAM=Peripherie를 보존하여 원시 PIW와 HMI DB 복사, 환산 Data를 구분한다.


| 채널 | 원시 선언·주소 | 환산 결과와 OFR | 호출 허가·별도 계수/영점 |
| --- | --- | --- | --- |
| TC01 | 0678 RID66 AO2176, PIW272 Int | 0676 RID69 Data.Temp_TC01 DB1.DBW110; RID373 TC01_OFR DB3.X21.2 | 0489 LAD1739 NID9 Contact335 ON→CRef316; Coeff DB4.DBW14/Zero DB4.DBW12 |
| TC02 | 0678 RID71 AO2192, PIW274 Int | 0676 RID74 Temp_TC02 DB1.DBW108; RID375 TC02_OFR DB3.X21.3 | 0490 LAD1740 NID10 Contact355 ON→CRef336; Coeff DB4.DBW18/Zero DB4.DBW16 |
| TC06 | 0678 RID81 AO2224, PIW278 Int | 0676 RID84 Temp_T6 DB1.DBW120; RID379 TC06_OFR DB3.X21.5 | 0492 LAD1742 NID12 Contact395 ON→CRef376; Coeff DB4.DBW26/Zero DB4.DBW24 |
| TC07 | 0678 RID86 AO2240, PIW280 Int | 0676 RID89 TC_07 DB1.DBW190; RID381 TC07_OFR DB3.X21.6 | 0493 LAD1743 NID13 Contact415 **OFF**→CRef396; Coeff DB4.DBW30/Zero DB4.DBW28 |
| RO01(원문 R001) | 0678 RID111 AO2816, PIW352 Int | 0676 RID114 Oxigen_RO01 DB1.DBW130; RID393 Ro01_OFR DB3.X22.3 | 0498 LAD1748 NID18 Contact515 **OFF**→CRef496; Coeff DB4.DBW46/Zero DB4.DBW44 |
| RO02(원문 R002) | 0678 RID116 AO2832, PIW354 Int | 0676 RID119 Oxigen_RO02 DB1.DBW128; RID395 RO02_OFR DB3.X22.4 | 0499 LAD1749 NID19 Contact535 **OFF**→CRef516; Coeff DB4.DBW50/Zero DB4.DBW48 |

0674 DepDBBlock의 Coeff TOD4, Data TOD1, Allarm TOD3를 확인했다. 계수·영점의 주소를 확인했을 뿐 현재 수치/단위/교정을 확보한 것은 아니다. TC06는 OEM OUTPUT AB01, 시공은 CC01 구역이라는 별도 위치 경계를 가진다.

TC01: Wire329/ORef322(RID1) Contact335 operand; W336 CRef316.en; W330/O323 IN0=ON, W331/O324 Analog_input=TC01, W332/O325 Coeff, W333/O326 Zero, W334/O327 OutValue, W24/O23 Out_of_range. TC02 대응은 Contact355, CRef336, W349~354와 W24, O342~347와 O23이다. 각 CRef의 CodeBlock UID328/348→0672 RID5 Signal linearization, CRef RefId351→0680 호출 선언을 대조했다.

TC07/RO01/RO02는 en에 OFF(M0.1), IN0에 ON(M0.0)이 연결된다. OFF 앞단이 있다는 이유만으로 원시값·HMI 복사·다른 쓰기도 사라진다고 해석하지 않는다.


### 2.2 공통 Signal linearization 원본 경계 [E09]

0291 LAD1658 NID1, Local IN0 Contact255(W220/O196) 아래 Analog_input >−1382 Part258(W30/O32,W31/O33)와 ≤32767 Part161(W27/O29,W28/O34)의 직렬 비교를 지난다. Int→DInt 변환164/167, DInt Add170(raw+Zero), Coeff 변환174, Mul177, Div181(/28000), Move185→Local OutValue 순서다. W227/230/234/237/241/245는 ENO 연쇄를 보존한다.

범위 외 가지는 Analog_input >32767 Part190 또는 ≤−1382 Part259→OR47→Move193 −9999를 OutValue에 쓰며, **W21 Move193.eno→Coil23 Out_of_range**, W22/O24(RID26)이다. OFR를 단순 비교 직결로 축약하지 않는다. 0014 LAD1659 NID2의 NOT IN0 Contact171→Move162 0은 OutValue를 별도로 쓴다. 0611 Local OutValue 자료형은 Int, 연산 중간은 DInt다. 현재 변환/오버플로/ENO 결과와 최종값은 미확정이다.

수학적으로 (raw+Zero)×Coeff/28000 경로지만 위 허가·정수연산·범위 외 값·다른 쓰기를 생략한 실측 온도 공식으로 사용하지 않는다. −1382/32767/−9999/28000은 원본 숫자이며 교정·현장 경계 권고가 아니다. ORef41/RID25의 전역 단순 검색은 다른 블록 Allarm1과 충돌하므로 해당 signal linearization의 0612 LiteralConstant 선언을 사용했다.


### 2.3 원시 Inputs 복사와 HMI 설정 [E10–E12]

0398 LAD1071 NID2는 raw를 DB13에 복사한다. TC01 Move50.in W67/O56(0627 RID61)→out1 W69/O57(0629 RID64 AO288); TC02 Move51.in W70/O58 RID62→out1 W71/O59 RID66 AO304. 0628 DepDBBlock RID4 TOD13과 결속했다. TC06 Move73→DB13W42, TC07 Move74→DB13W44, RO01 Move146→DB13W68, RO02 Move147→DB13W70도 원본 주소를 확인했다. 이들은 Data 환산값이 아니다.

TC01 Move50 앞에는 Move48/49의 ENO 경로 W62/65가 있고 TC02 Move51.en은 Move50.eno W68이다. 공유 HMI Inputs 전체 호출과 ENO를 무조건 실행으로 바꾸지 않는다. main0030 LAD1613은 Recipes Handler→HMI→HMI Output의 ENO 연쇄 뒤 NOT Simulation(1)(Contact37,W44/O45;0692 선언 M180.0)를 거쳐 HMI Inputs를 호출한다. 기존 simulation 자산은 읽기 경계 확인만 했으며 생성·실행하지 않았다.


| CSV 실제 행(머리행 포함) | HMI 태그 | 설정 주소/내부 ID | 해석 |
| --- | --- | --- | --- |
| 64 | Editor_TC01 | DB26,INT22 /00412 | 편집 DB 태그. Data.TC01_MAX_ALL이나 현재 설정으로 직접 결속하지 않음 |
| 321 /351 | EnableTC02 /EnableTC01 | DB39,X0.1 /00239; DB39,X0.0 /00211 | 선택 요청/상태 설정. 실제 버튼 이벤트·권한·외부쓰기 미확인 |
| 411 | TC_PID_REF | DB39,REAL2 /001C0 | Manage_TC1_2.PID_Ref_Temp 선언과 주소 대응 |
| 730 /732 /734 /745 | I_TC_06 /I_TC_02 /I_TC_01 /I_TC_07 | DB13,INT42/38/36/44;00064/00062/00060/00052 | raw DB 복사층 |
| 773 /774 | I_RO_02 /I_RO_01 | DB13,INT70/68;0002F/0002E | raw DB 복사층. 산소 % 환산표시와 동일시하지 않음 |
| 188 | ResetAlarms | DB2,X13.4 /002E1 | Flag.Reset_Allarms_HMI, PLC RESET_ALLARM과 별도 |

모두 Access Name=PLC, 근거는 dde.cfg 설정이며 온라인 값이 아니다. hmi-windows.csv의 ALARM/ALARM_HIST/ALARM_RECENT 및 CONFIG3(Burner configuration page) 목록만으로 해당 버튼/표시 이벤트를 증명할 수 없다. 실제 화면 요소→태그→쓰기 방식→PLC 수신 확인은 미확정이다.


### 2.4 HMI Reset 실제 PLC 전달 [E13]

0158 LAD930 NID9: Inputs.Reset_allarmi Contact23(W22/O24) **OR** Flag.Reset_Allarms_HMI Contact26(W25/O27)→OR28→W38→S33 Flag.RESET_ALLARM(W36/O37) 및 R40 HMI 요청(W42/O43). 0565 RID61 AO108와0564 Flag TOD2는 DB2.X13.4; RID2 AO48는 DB2.X6.0이다. Inputs.Reset_allarmi는 AO159/TOD13=DB13.X19.7이다.

0154 LAD931 NID4: RESET_ALLARM Contact259 OR STOP_HORN Contact261→SD229 Tag_160/T47, S5T#1S(W251/O243,0566 RID37)→접점263→R235 RESET_ALLARM, R237 STOP_HORN, R239 Blinking Ligh. HMI 클릭이 현재 이 요청에 도달함은 별도 확인 대상이다. 공통 요청의 자동 해제와 개별 온도/산소 알람의 Reset 허가는 서로 다르다.


## 3. 제어 구조·본체와 버너 소유


### 3.1 호출과 복수쓰기 [E14]

main0031 LAD1619의 ON Contact282(W280/O271)→W283은 Analog input conversion CRef261, Allarms1 CRef264, Allarms2 CRef267, Allarms3 CRef270의 en에 **각각 분기**된다. 앞 호출의 ENO 직렬 통과로 재구성하지 않는다. main0549 LAD1620 ON Contact350→W351에는 Burner Control CRef328가 다른 호출들과 분기된다. main0032 LAD1621 ON→Valve Control loop와 Analog output conversion 호출을 구분한다. 현재 OB/인터럽트 주기·실행 우선순위·Retain·온라인 상태·외부쓰기는 미확정이다.

백업0635 선언에는 기존 simulation NID14의 Data.Temp_TC01/Temp_TC02 쓰기 참조가 존재한다. 실제 활성 여부를 추정하지 않고 다른 쓰기 가능성을 보존한다. 중지 자산의 동작을 시험하지 않았다.


### 3.2 선택온도와 SCL1719의 증거 한계 [E15]

0684 RID169 AO16/BAD168,0682 DepDBBlock RID168 TOD39에 따라 PID_Ref_Temp는 DB39.DBD2 Real이다. 0650에서 EnableTC01 RID75 AO0, EnableTC02 RID76 AO1, PID_Ref_Temp RID91 AO16, EmergencyStop RID95 AO48의 GlobalAccess 선언 및 NID9 읽기/쓰기 C를 확인했다. Manage_TC1_2 DB 번호는0648의 DepDBBlock RID74/TOD39로 다시 대조한다.

live_index.json segment _7ev, i1719의 SCL Code 문자는 다음을 나타낸다.

- 두 Enable이고 OFR가 둘 다 없으면 두 온도 평균을 대입한다. OFR가 있으면 해당 Enable을 false로 쓰는 elsif가 있으며 그 분기에는 PID_Ref_Temp 대입이 없다.
- TC01만 선택이면 Temp_TC01을 대입하고 TC01_OFR이면 EnableTC01을 false로 쓴다.
- TC02만 선택이면 Temp_TC02를 대입하지만 후속 문자는 **TC01_OFR이면 EnableTC01 := false**다. 원문을 TC02로 고치지 않는다.
- 둘 다 비활성이면 EmergencyStop := true, 마지막에 Allarm.EmergencyStopTC1_2 := Manage_TC1_2.EmergencyStop이다.

관련 native 선언이 있다는 사실은 검색색인 본문의 완전성·실행순서·현재 적용을 증명하지 않는다. native SCL 본문과 컴파일 listing을 확보하기 전 현재 PLC 오류·중복 고장 처리 완료·선택값 갱신을 확정하지 않는다. 기존 조사에서 남긴 SCL 본문 미확정은 유지한다.


### 3.3 온도 알람에서 외부 버너까지 [E16–E19]

- 0173 LAD1856 NID3: ON160→NOT MAX_MAX_TC09 Contact162→NOT MAX_MAX_TC01_TEMP Contact164→Coil150 Temperature Interlock OK. W155/161/156/163/157/165/159, ORef151~154를 대조했다. 0582 RID26 Output AO54=Q6.6. **MAX가 아닌 MAXMAX**가 입력이다.
- 0175 LAD1858 NID5: MAXMAX_TC01 Contact293→OR219.in6, RO01_Signal_Fault Contact295→in7, TC01_TC02_COMP_FAULT Contact297→in8, EmergencyStopTC1_2 Contact22→in12가 다른 정지 조건과 합쳐진다. OR219.out W267→ON305→OR213.in5→R232 Flag.Start_Burner(W272/O250). 조건은 ON273 앞단을 가지며 정확한 MAX_TC01_TEMP 이름은 이 네트워크에 없다. ON305의 ORef249/RID1을 타블록 Data 선언과 오결속하지 않는다.
- 0182 LAD1866 NID12: Flag.Start_Burner634 AND NOT Lock Burner636 AND Inputs.FN03 Run642→Coil607 Enable start burner(1); 여기에 Enable start burner644를 더 거쳐 Coil611 Q6.5다. W621/635/622/637/627/643/628/629/645/631. Flag 요청 DB2.X5.2, Lock M28.0, Enable1 M48.0, Enable M48.2, Q6.5는 별도다. 다른 분기의 NOT FN03요청 AND OFF→FN03 요청Set도 그대로 둔다.
- 0184 LAD1868 NID14는 WorkData.BR01_State, 세정 시간, Open/Close MV03 요청, Enable, 내부 Start Burner를 쓰는 **BR01의 GME 순서**다. AB01 본체 시퀀스로 재배정하지 않는다. 기존 조사에서 확인한 State5의 Close OR ON, 별도 State77, NOT Close AND Close 가지, 공유 T32/CleanTime 다른 쓰기는 보존 대상이다. 외부010-390 내부 안전 시퀀스를 대체하지 않는다.

알람 래치 해제→운전 요청→두 Enable→GME 출력→외부반 응답→실제 연소 상태는 별도 확인 단계다. 현장 복구나 자동 재기동을 보증하지 않는다.


### 3.4 MAX의 변조 영향과 주변 댐퍼 [E20]

0186 LAD1870에서 ON1218 AND AUTO_BURNER1220 AND NOT MAX_TC01_TEMP1222 AND NOT MAX_TC03_TEMP1224 AND NOT ProgrammedStop1226 AND StartBurner1228 AND Inputs.HighFlame1230→Coil1172 Flag AutoBurner(M15.0)다. 별도 OR1175의 NOT Enable1/MAX_TC01/MAX_TC03/ProgrammedStop/NOT HighFlame→Move1181 PanelSP0 쓰기가 있다.

0187 LAD1871 FlagAutoBurner1188→Add1176 WorkData.Burner_PID_Result+0→Data.Burner_Panel_SetPoint. 0416 LAD1721은 OFF 앞단에서 Manuale에 따라 I_FFWD 또는 I_Outvalue+0를 WorkPIDResult에 쓰고,0023 LAD1722는 ON→I_Outvalue+0를 같은 결과에 쓴다. 이름 cyc_int2 ogni1s만으로 실제 갱신주기를 확정하지 않는다. MAX/MAXMAX의 영향 차이만 기록하며 버너 출력·가스/공기 비율을 AB01 소유로 복제하지 않는다.

0346 LAD1708은 MV05 자동/수동 요청, 실제 방향 출력, 위치 응답, Oxigen_Fault와 UNDER TESTING 등이 있는 별도 댐퍼 제어다. AB01에서 RO01·상부 유로와의 연관을 연결할 수 있지만 전체 댐퍼 규칙이나 PID 조정을 본체에 포함하지 않는다. MV03/PSH03도 해당 설비의 기존 조사 범위다.


## 4. 전기 전달 경로·PDF 실페이지


### 4.1 TC01/TC02/TC06/TC07 [E21,E22]

OEM Electrical_Rev2 실제 렌더 FG77/PDF78, FG78/PDF79, FG106/PDF107, FG107/PDF108을 대조했다. TC 표기는 센서/변환기 도면 표기이며 현재 제조사·소자 종류·교정 증명이 아니다.


| 신호·도면 기능 | 전원/신호/차폐 양 끝점 | PLC 모듈 끝점 | 자료 경계 |
| --- | --- | --- | --- |
| TC01 CHAMBER AB01 | +24Vdc10.7→X1/186의5×20 50mA F→77.1→TC01 +5; TC01 −6→X1/187→+PEW272; 차폐 X1/188→77SCH1 | FG106 CPU515 MOD3, I0+ 단자2, U0−/I0− 단자4; 귀로 −0Vdc10.6/MANA18 | OUTPUT4–20mA,0/1300°C 인쇄. 현재 계수/설정과 구분 |
| TC02 SAFETY TEMPERATURE CHAMBER AB01 | +24Vdc→X1/189 50mA F→77.2→+5; −6→X1/190→+PEW274; 차폐 X1/191→77SCH2 | FG106 MOD3, I1+6, U1−/I1−8, 공통귀로 | 4–20mA,0/1300°C. SAFETY 명칭은 안전등급 증명이 아님 |
| TC06 TEMPERATURE OUTPUT AB01 | +24Vdc→X1/195 50mA F→78.1→+5; −6→196→+PEW278; 차폐197→78SCH1 | FG106 MOD3, I3+14,U3−/I3−16 | 4–20mA,0/1300°C. 시공 CC01 위치와 구분 |
| TC07 SAFETY TEMPERATURE INPUT SMOKE | +24Vdc→X1/198 50mA F→78.2→+5; −6→199→+PEW280; 차폐200→78SCH2 | FG107 MOD3, I4+22,U4−/I4−24 | 4–20mA,0/750°C. FG78·107 모두 SPARE 영역; 현재 설치/사용 미확인 |

FG77·106 개정란은 공란이다. FG78·107은 **Rev2 /17.03.2025**가 있다. 공통 타이틀 DATE27.05.2024 및 파일명 Rev2와 개별 개정란을 구분한다. 현재 본체 온도나 보호값을 위 인쇄 범위에서 채워 넣지 않는다.


### 4.2 RO01/RO02 산소 계측 [E23]

FG80/PDF81은 RO01 SMOKE DETECTOR OXIGEN OUTLET AB01, RO02 SMOKE SAFETY DETECT OXIGEN OUTLET AB01을 표시하며 각 80RO01/02 TRANSMITTER MOD.H705를 그린다. 현행 설치모델/제조사·안전등급·정상 출력 범위는 별도 확인 전이다.


| 구간 | RO01 | RO02 |
| --- | --- | --- |
| 센서→변환기 | 소자 +S/−S/−T/+T→H705 단자1+/2−/3−/4+, 차폐80SCH2 | 같은 표시 단자1+/2−/3−/4+, 차폐80SCH4 |
| 변환기 전원 | 110Vac9.8→X1/209 2A F→15;0Vac9.9→X1/210→16;GND17 | X1/214 2A F→15;X1/215→16;GND17 |
| 4–20mA 신호 | 7+→X1/211→+PEW352;8−→212→−PEW352;차폐213/80SCH1 | 7+→216→+PEW354;8−→217→−PEW354;차폐218/80SCH3 |
| FG110/PDF111 모듈 | CPU515 MOD5 I0+2,U0−/I0−4 | MOD5 I1+6,U1−/I1−8 |

FG80·110 개정란은 공란이다. 소자선·변환기 전원·아날로그 신호선과 차폐를 서로 대신 쓰지 않는다. 인쇄4–20mA에서 현재 산소 % 단위나0.1% 배율을 임의 확정하지 않는다.


### 4.3 시공 케이블·위치 상충 [E24]

Electrical_Can_Decoating_20241118.pdf PDF56, 도면 CANDC-CONS-C006-056, CABLE SCHEDULE(5)의 해당 행을 시각 확인했다. 검은 마스킹 영역6_7~6_10은 해석·복원하지 않았다.


| 행/전체 케이블 ID | FROM→TO | 종류·규격·SPARE | 경로/인쇄 LEN |
| --- | --- | --- | --- |
| 6_4 =FLA+MV03-81RO01A | CR→MV03/81RO01 PEW352 | AI,CVV-S2S1.0,0 | 100 LBD1/E500;47 |
| 6_5 =FLA+MV03-81RO02A | CR→MV03/81RO02 PEW354 | AI,CVV-S2S1.0,0 | 100 LBD1/E800;47 |
| 6_21 =FLA+HE01-RO01A | MV03/81RO01→HE01/RO01 | AI,CVV-S4S1.0,0 | LAD1 E700→100 LAD1→100 LCD1→E700;16 |
| 6_22 =FLA+HE01-RO02A | MV03/81RO02→HE01/RO02 | AI,CVV-S4S1.0,0 | LAD1 E1000→100 LAD1→100 LCD1→E800;16 |
| 6_23 =FLA+HE01-TC01A | CR→HE01/TC01 | TC,**KX2S1.0**,0 | 100 LCD1/E500;50 |
| 6_24 =FLA+HE01-TC02A | CR→HE01/TC02 | TC,**KX2S1.0**,0 | 100 LCD1/E600;50 |
| 6_25 =FLA+MV02-TC07A | CR→**FLA/TC07** | TC,KX2S1.0,0 | 100→110 LAD1→E1700;60 |

케이블 ID의 MV02와 도착 LOC의 FLA는 원문대로 남긴다. OEM TC변환기 출력4–20mA와 시공 TC/KX 표기를 자동 동일 구간으로 합치지 않는다. 변환기 실제 위치·접속점·구간 분할 자료가 필요하다. LEN은 도면 표기이며 실측 길이가 아니다.

시공 PDF64 CANDC-CONS-C014-064/CABLE SCHEDULE(13)의 14_3 =ENT+AB01-6SB2A는 UC01/NVBOX→AB01/6SB2, DC CVV2C0.75 SPARE0, E400→120 RAD1→100→100 RBD1,LEN50이다. 14_4 =ENT+AB01-6SB2B는 CR→AB01/6SB2, 같은 규격, CR→100 RBD1,LEN40이다. 이 케이블 표만으로 6SB2 접점 극성·전체 비상정지 회로·안전등급·PLC 특정 비트를 확정하지 않는다.

같은 PDF64의14_12~14_18은 CC01/BR01 간선이다. AB01 본체 케이블로 재배정하지 않는다. 기존 BR01F 두 행 반복도 그대로 둔다. 시공 PDF3/6/56/64 타이틀에는 최초안 24.11.11 first draft design이 있으며 승인·준공·실제 설치 상태는 확인 전이다.


### 4.4 버너 전기 경계 [E25]

FG99/PDF100의 Temperature Interlock는 Q6.6→99KA2 코일 A1, A2→−0Vdc10.6과, 버너 X/1/2→X1/390→99.3→**부하접점5–9**→99.4→X1/391→버너 X/1/4를 분리한다. 원격 Q6.5→99KA1도 코일 회로와 X/220V→X1/388→99.1→5–9→99.2→X1/389→X/1/7 부하 경로다. 전기적 외부 종착점은 여기까지이며010-390 내부는 미확보다. 도면 릴레이 회로가 있다는 사실과 현재 실제 연료 차단은 별도다.


## 5. 알람·타이머·복구


### 5.1 주소와 범위 [E26]


| 변수 | 원본 선언 | 백업 주소·형식 |
| --- | --- | --- |
| Manage_TC1_2.PID_Ref_Temp | 0684 RID169 AO16/BAD168→0682 TOD39 | DB39.DBD2 Real |
| Data.TC01_MAX_ALL | 0684 RID5 AO544/BAD3→TOD1 | DB1.DBW68 Int |
| Allarm.MAX_TC01_TEMP /MAX_MAX_TC01_TEMP | 0684 RID11/23 AO64/65/BAD10→TOD3 | DB3.X8.0/X8.1 Bool |
| Allarm.TC01_TC02_COMP_FAULT | 0684 RID81 AO73 | DB3.X9.1 Bool |
| TC01-TC02control disable | 0686 RID73 Memory AO642 | M80.2 Bool |
| Flag.RESET_ALLARM /STOP_HORN | 0684 RID24/16 AO48/50,BAD15→TOD2 | DB2.X6.0/X6.2 Bool |
| Tag_99 /Tag_100 /Tag_108 | 0686 RID9/22/80,Timer AO85/86/116 | T85/T86/T116 |
| Allarm.EmergencyStopTC1_2 | 0585 RID245 AO140,BAD5→0584 TOD3 | DB3.X17.4 Bool |

Local app00/max_max_tc1/app02는0685의 allarms3 지역 Int다. Global 온도·다른 블록 동일 지역명과 합치지 않는다. 현재 래치 값·타이머 경과값·HMI 접근 권한은 미확정이다.


### 5.2 MAX_TC01_TEMP [E27]

0527 LAD1979 NID1:

- ON Contact286(W240/O209)→Real Gt149(PID_Ref_Temp W241/O210, TC01_MAX_ALL W242/O211).
- Gt.out W243은 SD155.in과 Tag_99 Contact288.in에 분기한다. SD value W244/O212→0683 RID8 CB T=S5Time, SV=S5T_x0023_6S,V1536. operand W245/O213→T85; Contact operand W246/O214도T85다. Contact.out W289→S160, W248/O215→MAX 래치.
- Reset은 ON→자기 MAX Contact290(W250/O216)→Sub165.en(W291). Int TC01_MAX_ALL−5(W252/O217,W253/O218)→Local app00(W254/O219). **W255 Sub.eno→Real Lt169.pre**, 입력 W256/O220 선택온도, W257/O221 app00. Lt.out W258→R173 MAX(W259/O222) 및 S175 STOP_HORN(W260/O223).
- 이 Reset에 RESET_ALLARM 접점은 없다. 온도 하강 조건·ENO·현재 값이 확인돼야 하며 HMI Reset을 누르는 것과 같은 의미가 아니다.


### 5.3 MAX_MAX_TC01_TEMP [E28]

같은0527:

- ON 아래 Int Add179 TC01_MAX_ALL+20(W262/O224,W263/O225)→Local max_max_tc1(W264/O226).
- Real Gt186(selected>max_max), Gt189(selected>1250.0), Lt192(selected<−60.0)→OR185. 비교 입력은 W265~272, OR 입력W267/270/273이다.
- **W287이 Add.en과 세 비교.pre에 각각 분기**된다. Add.eno→비교 직렬선은 없다.
- OR.out W274→SD198.in 및 Tag_100 Contact292.in. 시간W275/O233은 같은0683 RID8 S5T#6S; T86 operand W276/O234와W277/O235. Contact.out W293→S203, W279/O236→MAXMAX.
- Reset은 ON→RESET_ALLARM294(W281/O237)→자기 MAXMAX296(W282/O238)→R208(W284/O239), 연결W295/297이다. **이 가지 자체에는 원인해소·온도정상 접점이 없다.** 지속 원인·동시 Set/Reset·스캔 순서가 미확정이므로 Reset 성공을 안전 복구로 표시하지 않는다.


### 5.4 TC01/TC02 비교 알람 [E29]

0534 LAD1986 NID8:

- ON832(W801/O781)→**NOT** TC01-TC02control disable834(W802/O782,RID73;Negated PinName=operand).
- Int Temp_TC01>400 Gt745 또는 Temp_TC02>400 Gt748→OR744. 입력W803/804/806/807, 합류W805/808.
- **W809**는 Int Sub754.en과 Lt761/Gt764.pre에 분기한다. Sub754 Temp_TC01−Temp_TC02(W810/O787,W811/O788)→Local app02 W812/O789. Sub.eno를 비교.pre로 연결한 직렬선은 없다.
- app02<−100 Lt761 또는 >100 Gt764→OR760(W813~818). 정확히−100/+100은 이 범위 밖 조건에 포함되지 않는다.
- W819→SD770.in 및 Tag_108 Contact836.in. W820/O794→0683 RID46 S5T_x0023_1M,T=S5Time,V5632. T116 쓰기/읽기W821/O795,W822/O796; Contact.out W837→S775,W824/O797→COMP_FAULT.
- Reset은 ON에서 별도 분기W833→RESET_ALLARM838(W827/O798)→자기 래치840(W828/O799)→R780(W830/O800), 연결W839/841. disable·>400·차이·타이머 가지를 통과하지 않는다.

400/±100의 현재 환산 단위·비활성 비트 값·설정 주체를 임의 채우지 않는다. 두 센서 중 하나를 대신 사용하거나 보호를 우회하는 작업은 범위 밖이다.


### 5.5 주변 RO01/RO02 알람: 별도 소유와 사용 여부 [E30]

다음은 AB01 출구 연관 계측의 원본 정적 조건이다. 본체 신규 알람으로 생성하지 않으며 % 단위를 덧붙이지 않는다. 0682 Allarm TOD3와0684 선언을 결속했다.


| 네트워크/래치 | Set와 Reset 정적 조건 | 원본 Part/Wire·경계 |
| --- | --- | --- |
| 0530/LAD1982 Oxigen_Fault DB3.X9.6 | ON AND (Oxigen_RO01≤0 OR ≥200) AND **ServiceBit**→Set. 자기래치 AND ≥5 AND ≤195→Reset 및 STOP_HORN Set | ON539,OR483,ServiceBit22(W21/O23;0686 RID161,M1000.0),S490/R501/S503. 지연 SD 없음. 단순 OFR와 별도 |
| 0531/LAD1983 Oxigen_Too_high DB3.X9.7 | 설정 RO01_MAX_SETPOINT>100이면 별도 Move32 100쓰기. ON AND O₂값≥설정→Set. 자기래치 아래 설정−10을app05에 쓰고 값<app05→Reset/STOP_HORN | Gt663→Move32,Ge627→S628,Sub630·Lt631은W654 병렬 허가로 ENO직렬 아님;R632/S633. 현재 설정 권고 아님 |
| 0532/LAD1984 Oxigen_LOW DB3.X9.4 | **OFF** AND PID_Ref_Temp>650.0 AND O₂값≤5→SD599 1분 T68→Set. OFF AND RESET_ALLARM AND 자기래치 AND (O₂값≥20 OR 선택온도≤650.0)→Reset | OFF658,SD599 valueW640/O622 S5T#1M,RID46;Tag_106=0686RID63 Timer68;S604/R616. OFF를 삭제하지 않음 |
| 0533/LAD1985 RO01_Signal_Fault DB3.X4.4 | ON AND NOT RO01-RO02control disable AND 선택온도>650.0, RO01−RO02<-20 OR >20→SD6851분 T117→Set. ON AND RESET_ALLARM AND 자기래치→Reset | disable743 W715/O697,0686RID65 M80.1;Sub669·비교는W718 병렬허가;SD W729/O707;S690/R695. 지연 Tag_107 T117 |

ServiceBit(M1000.0), disable(M80.1), OFF(M0.1)의 현재 상태는 미확정이다. RO01/02 환산 호출도 OFF 앞단이므로 고장 조건표만으로 현재 연소 보호가 작동한다고 확정하지 않는다. RO01_Signal_Fault는1858의 버너 요청 Reset 입력이지만 Oxigen_Fault/Too_high/LOW를 모두 같은 정지 효과로 일반화하지 않는다.


### 5.6 복구 상태를 기록하는 방식

원인 관찰, 원시 입력, 환산/OFR, 선택온도/Enable, 개별 래치, 공통 Reset요청, 버너 요청/Enable/출력, 외부 제어기 최초 알람, 실제 물리 반응을 같은 시각 기준으로 구분한다. 시간은 원문 SD 명목값이며 경과 관찰값이 아니다. 원인 지속/재발, Reset 요청 소실, 신규 기동 요청 여부는 별도 기록한다. 현재 승인 복구 절차·제작사 안전 자료가 없는 상태에서 Reset·재기동·설정 변경을 지시하지 않는다.


## 6. 증상별 관찰·원인 구간 분리

아래는 수리 완료나 즉시 현장 조작 절차가 아니라 필요한 관찰·자료 수집 초안이다. 전기·고온·연소 설비 접근은 현장 승인 절차와 자격을 갖춘 담당자가 수행해야 한다. 보호값·disable·Enable·원격 출력 변경이나 센서 대체를 제안하지 않는다.


| 증상 | 동시에 남길 관찰 | 원본 비교·원인 배제 | 다음 자료와 복구 증거 |
| --- | --- | --- | --- |
| TC01/02가 다르거나 차온 알람 반복 | raw PIW272/274,DB13W36/38,DataW110/108,OFR,Enable1/2,PID_REF,M80.2,T116,DB3.X9.1,시각 | 센서→변환기→회로→원시→환산→선택→차온 래치 순서. OEM AB01/시공 HE01 위치와400 OR·±100 밖을 대조 | 실제 취출부/명판/교정·현재 계수/단위·native SCL/CPU. 동일 시각 비교와 승인 절차 후 원인/래치/외부 응답 각각 확인 |
| MAX 또는 MAXMAX 반복·Reset 직후 재발 | 선택온도,DB1W68,DB3X8.0/8.1,T85/86,HMI요청DB2X13.4,RESETDB2X6.0 | MAX 자동히스테리시스와MAXMAX 요청Reset 차이. 선택값/OFR/다른 쓰기와 원인 지속을 분리 | 현재 설정/승인 기준·Reset 이벤트. 한 래치가 내려갔다는 사실만으로 과열 해소/재기동 완료 처리하지 않음 |
| 버너 시작 불가·Lock Out | 최초 외부반 알람,Flag.Start_Burner,Lock,Enable1/Enable,FN03 응답,Q6.5/Q6.6,외부 응답,시각 | 1858 요청Reset→1866 두Enable/출력→FG99 릴레이→전용010-390을 구간 분리 | 외부반 제조사 원도면/안전·복구 절차,현행 신호 극성. 실제 화염/연소 결과까지 승인된 별도 확인 필요 |
| HMI는 온도가 보이나 선택온도/OFR와 다름 | HMI raw 태그,환산Data,TC_PID_REF,Enable,표시 단위·갱신시각 | 0398 raw DB 복사와0489/90 환산·SCL선택을 구분. HMI 설정만으로 화면 scale을 추정하지 않음 | HMI 프로젝트 화면요소/이벤트/배율과현재DB. 표시값·계산값·센서실측의 동시 비교 |
| RO01/02 산소 표시/차이가 이상 | PIW352/354,DB13W68/70,DataW130/128,OFR,OFF,M80.1,ServiceBit,관련 래치 | OFF-gated 호출·H705전원/출력·단위·시공센서/변환기 위치를 구분.두 산소채널을 서로 대체하지 않음 | 교정·출력범위·현재사용여부/호출·계수·nativePID·현장설치. 실제 연소 상태는 별도 증거 |
| TC07 표시나 외관/출구 온도와 맞지 않음 | TC07 raw/환산/표시,사용상태,외관의 정확한 위치·시각 | SPARE도면과OFF호출,시공TC07 FLA표기,TC06 OUTPUT AB01을 구분 | 현행 설치·기계/내화재/씰 도면·제작사점검기준. 단순 외관관찰로 내부손상·복구 완료 판정하지 않음 |
| 비상정지/6SB2 관련 보고 | 어느 구역·장치인지,최초상태·시각,승인된현장회로자료 | 시공14_3/14_4는간선이므로 접점·안전등급·GME비트로 바로 배정하지 않음 | 전체안전회로·접점/단자양끝·현장시험기록. 케이블표 확인과안전기능검증을 분리 |

관찰 기록 필수값: 관찰자, 시각/시간대, 장치·위치, 값과 단위/빈칸 여부, 수집 장치, 프로젝트/CPU 근거, 비교한 원본 파일·페이지/네트워크·해시, 배제한 원인과 근거, 수행 승인·조치, 복구 증거 및 미확정. 사용자 운영 기록·사진은 이 공개 자료나 원본 저장소에 복제하지 않는다.


## 7. 적용표·검증·인계


### 7.1 7영역 적용


| 영역 | 상태 | 이 초안 위치 | 미확정/비해당 경계 |
| --- | --- | --- | --- |
| 설비·자료 기준 | 적용, identity 근거 미확보 | §1 | P12↔AB01은역할후보,현장명판·본체/버너관계확정 전 |
| I/O·HMI | 관련계측·공통요청 적용;본체전용HMI 근거 미확보 | §2 | raw/환산/선택/설정CSV분리,버튼이벤트·현행화면미확인 |
| 제어 구조 | 관련호출·정지영향 적용;본체전용출력 근거 미확보 | §3 | BR01·MV03/MV05제어소유 유지,전용연소안전내부 미확보 |
| 전기 전달 경로 | 계측·인터페이스 적용;본체구동회로 근거 미확보 | §4 | OEM/시공구역상충,현재모듈·극성·준공상태 미확인 |
| 알람·복구 | 관련온도·산소원본 적용;실제복구 미확인 | §5 | MAX/MAXMAX/차온/산소/OFR/공통Reset분리 |
| 증상별 수리 | 관찰·원인배제·자료요구 초안 적용 | §6 | 실제조치·복구없음,보호값/우회/현장명령 없음 |
| 완료 기준 | 적용 | §7 | 문서·정적·UI/기록·게시·TIA·CPU·현장을 각각 기록 |

본체 내화재·씰·구조부에 신규 PLC 알람을 만드는 것은 비해당이다. 제작사 기계도·점검 기준이 없는 상태는 비해당이 아니라 근거 미확보다. 본체 passive라는 대장 유형만으로 전용 안전기능이 없다고 단정하지 않는다.


### 7.2 네 기능 반영 제안, 실제 구현은 미수행


| 기능 | AB01에 필요한 연결 | 현재 상태 |
| --- | --- | --- |
| 도면·래더 비교 | FG77/PDF78↔1739/1740↔1979/1986;FG99/PDF100↔1856/1858/1866;시공56/64↔identity 경계 | 문서근거 준비;UI 구현/왕복·강조 검증 미수행 |
| 백업·선택 복원 | P12/AB01기록키·기존note/repair_observation·미지행/필드·다른설비·초안보존 | 기존기능을AB01지원완료로 추정하지 않음;격리검증 필요 |
| 전후 기록 비교 | raw/환산/선택/래치/요청/응답과시각,기록생성·저장근거 구분 | 새기록작성 없음;실제저장·재열기·동시성검증 미수행 |
| 보고서/PDF | candidate 표시·원본출처·미확정과실제조치 분리 | 설계제안만;생성기/UI/PDF출력검증 미수행 |

0과빈칸을 구분하고 기존 saved_with/generated_with·이전근거·사용자편집을 보존한다. 과거기록에 이번해시·해석을 소급적용하지 않는다.


### 7.3 원본 검토와 추가 필요 자료

- 현재 TIA 프로젝트/CPU 비교·OB/인터럽트 호출·native SCL1719/컴파일 listing·현재 DB/Retain/초기화·외부쓰기
- TC01/02/06/07,RO01/02의 실물위치·명판·교정·현재단위/계수,센서와변환기구간 연결도
- P12 재연소로↔AB01 본체 identity,BR01 및010-390/35602201_00 판본·제조사 연소보호 자료
- HMI화면·버튼이벤트·설정/표시배율·사용자권한·Reset전달·Enable변경이력
- 6SB2 전체회로와현장승인 안전검증,시공표의승인/준공상태,TC/KX와4–20mA구간대응
- 기계/내화재/씰/체결점검기준과승인복구절차. 현행모델·토크·정비주기·보호설정은 임의작성하지 않는다.


### 7.4 최종 상태


| 구분 | 이 작업의 상태 | 근거 |
| --- | --- | --- |
| documentation | draft_complete_with_gaps | 7영역·근거표·관련원본·시각확인13쪽·미확정명시;후속독립검토/통합 필요 |
| static_review | 원본읽기·정적대조 수행 | 아래 재열람/해시검사 기록;정식설비검사/BC01회귀를 대체하지 않음 |
| ui_records | not_run | UI·기록기능 편집/시험 안 함 |
| publication | not_published_by_this_work | 버전·GitHub·Netlify 변경/확인 안 함 |
| tia_compile | not_performed | 컴파일/현재타입실행 검증없음 |
| live_cpu | not_performed | 현재CPU·동작·주기 미검증 |
| field_recovery | not_performed | 실제 현장조치/복구 미수행 |

다음 한 작업은 사용자 Codex의 AB01 원본핵심 독립검토와 기존완료분을 보존한 통합이다. 새자료가 필요한 identity·안전·현장보류를 억지로 완료하지 않고, 독립된 다음 우선설비 조사와 구분한다.


## 부록 A. 핵심 주장 근거표

판본은 모두 상단 고정 커밋이다. 원본경로와 SHA256은 부록B, 해석과 미확정은 각 본문절을 함께 사용한다. 아래 LAD는 조회용 식별자이며 현재 실행순서가 아니다.


| ID | 핵심 주장 | 원본 파일·페이지/네트워크·핀 | 해석/미확정 경계 |
| --- | --- | --- | --- |
| E01 | P12 AB01 역할후보 유지 | docs/equipment-standard/INVENTORY.json priority P12/catalog AB01 | identity_verified=false,BR01은별도P11 |
| E02 | AB01본체와BR01·센서·유로구분 | sources/PID_1684n002I.pdf p1,AB01/BR01/TC01/02/MV05/RO01/02/PSH03 | 실제렌더확인,850°C/O₂±4%현재권고아님 |
| E03 | 시공구역과본체 identity구분 | Electrical_Can_Decoating_20241118.pdf p3/6 ENTRY AB01/6SB2,FLOW_A AB01/TC07,HE01계측행 | 센서실제취출부·동일성 미확인 |
| E04 | 기존AB01분석보존 | AB01-INVESTIGATION.md;registers/ab01-independent-investigation.json;body-manual.json profiles AB01 | 탐색·기존분석자료,새현장완료아님 |
| E05 | TC01/TC02환산호출 | 0489/0490 LAD1739/1740 NID9/10,CRef316/336,W331/351→W334/354;0672/0674/0676/0678/0680 | 원시Peripherie·Data·OFR·계수분리 |
| E06 | TC06출구계측 | 0492 LAD1742,CRef376,0676RID84 AO960,0678RID81 AO2224 | OEM/시공위치별도 |
| E07 | TC07 OFF-gated 호출 | 0493 LAD1743 Contact415 W409/O402 OFF,CRef396 W416.en/IN0 ON | SPARE/현재사용여부추정금지 |
| E08 | RO01/RO02 OFF-gated 호출 | 0498/0499 LAD1748/49 Contact515/535 W509/529;0676/0678 | 원시/HMI/환산·현재단위분리 |
| E09 | 공통환산·OFR·ENO | 0291/0014 LAD1658/59;0611/0612 Local/상수;Gt258/Le161,Convert164/167/174,Add170,Mul177,Div181,Move185/193,Coil23 | 정수형·범위외−9999·ENO·NOTIN0쓰기보존 |
| E10 | raw Inputs DB복사 | 0398 LAD1071 Move50/51 W67/69/70/71,0627/0628/0629 | Data온도와HMIraw가다른층 |
| E11 | HMI설정주소 | sources/hmi_plc_tags.csv 행64,188,321,351,411,730,732,734,745,773,774 | dde.cfg설정,현재값/화면이벤트아님 |
| E12 | HMI호출경계 | 0030 LAD1613,CRef21→23→25 ENO,Contact37 NOT Simulation(1)→CRef28;0688/0692/0694 | 현재활성·외부쓰기·원시전달미확인 |
| E13 | HMIReset과PLC공통Reset분리 | 0158 LAD930 NID9 OR28 W38→S33/R40;0154 LAD931 SD2291S/T47→R235;0564/65/66/67 | DB2X13.4→DB2X6.0,온도정상/재기동아님 |
| E14 | 공통호출병렬en·다른쓰기 | 0031 LAD1619 W283,0549 LAD1620 W351,0032 LAD1621 W353;0635 Data.Temp_TC01/02 NID14 쓰기 | ENO직렬로재구성안함,현재OB/CPU미확인 |
| E15 | 선택SCL색인과선언 | sources/live_index.json _7ev/i1719/SCL Code;0648 RID74 TOD39;0650RID75/76/91/95,NID9 | 원형SCL/컴파일미확인,TC02-only TC01문자보존 |
| E16 | MAXMAX가Q6.6인터록입력 | 0173 LAD1856 Contact160/162/164→Coil150,W159/O154;0582/0585 | MAX와구분,외부안전전체아님 |
| E17 | 온도·산소알람이BR01요청Reset | 0175 LAD1858 OR219.in6/7/8/12→ON305→OR213→R232 | 요청해제와최종출력/화염정지분리 |
| E18 | BR01요청/두Enable/Q6.5 | 0182 LAD1866 Contact634/636/642/644,Coil607/611;0582/0584/0585 | AB01전용출력으로재배정금지 |
| E19 | 세정순서는BR01소유 | 0184 LAD1868 NID14,State/MV03요청/Enable/StartBurner | 010-390내부안전과구분,기존상충보존 |
| E20 | MAX변조억제·결과복수쓰기·MV05경계 | 0186/0187 LAD1870/71;0416/0023 LAD1721/22;0346 LAD1708 | 본체전용PID/출력으로복제금지 |
| E21 | TC01/02전원·신호·모듈 | Electrical_Rev2 FG77/PDF78,FG106/PDF107 X1/186~191,MOD3핀2/4/6/8 | 50mAF·4–20mA·0/1300°C도면범위 |
| E22 | TC06/07위치·SPARE·개정 | 동PDF FG78/PDF79,FG106/107 PDF107/108 X1/195~200 | TC07SPARE,FG78/107Rev2 17.03.2025 |
| E23 | RO01/02소자·H705·AI | 동PDF FG80/PDF81,FG110/PDF111 X1/209~218,MOD5핀2/4/6/8 | 변환기전원/소자/아날로그/차폐분리 |
| E24 | 시공케이블과불일치 | 시공PDF56행6_4/5/21~25,PDF64행14_3/4 | HE01/AB01구역·KX/4–20mA·6SB2안전기능미확정 |
| E25 | 버너외부전기끝점 | Electrical_Rev2 FG97/PDF98,FG99/PDF100 99KA1/2부하5–9 | 010-390미확보,코일/부하전원구분 |
| E26 | 온도래치·타이머주소 | 0682 TOD,0684 AO/BAD,0685 Local,0686 Timer/Memory;0584/0585EmergencyStop | T85/86/116은PLC타이머,HMI태그아님 |
| E27 | MAX Set6S/자동Reset | 0527 LAD1979 Gt149→SD155→S160,Sub165.eno W255→Lt169→R173/S175 | RESET_ALLARM접점없음 |
| E28 | MAXMAX범위/6S/요청Reset | 0527 Add179,OR185,SD198,S203,R208;W287병렬허가 | 원인해소접점없는Reset,현재실행미확인 |
| E29 | 차온NOTdisable·OR400·±100밖·1M | 0534 LAD1986 Contact834 Negated,OR744,W809,Sub754,OR760,SD770,S775/R780 | 단위/disable현재값추정안함 |
| E30 | 산소4알람의각조건 | 0530/31/32/33 LAD1982~85;0683/84/85/86 ServiceBit/OFF/disable/SD | 환산OFR와별도,본체소유로신설안함 |


## 부록 B. 원본·참조 SHA256과 재열람 결과

아래 전체 SHA256은 고정 커밋의 실제 파일을 읽어 계산했다. sources/ 경로는 원본/원본해독자료이고 registers/·기존 조사 MD는 파생/참고다. 링크는 해당 고정 커밋의 파일로 연결한다. 네이티브 XML과 PDF를 수정하지 않았다.


| 파일(저장소 상대경로·고정 링크) | SHA256 |
| --- | --- |
| [all-in-one/AB01-INVESTIGATION.md](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/AB01-INVESTIGATION.md) | 513252fe525bbfbae5fe75ca8f23df67be9860f4d2b907b9431fff5ed1d1c7bb |
| [all-in-one/registers/ab01-independent-investigation.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/registers/ab01-independent-investigation.json) | f52b160f5a56cb8b2077b30e541aca2fef9dbd750b19b3862c20bc6e9f511e98 |
| [all-in-one/registers/body-manual.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/registers/body-manual.json) | 0e8071196565fdffb29ae81fa3d24e567c95fd254355e5d71e887bc24ac189a4 |
| [all-in-one/registers/equipment.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/registers/equipment.json) | 7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa |
| [all-in-one/registers/priority-equipment.csv](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/registers/priority-equipment.csv) | 953c2c4df5b3a6e40d926d1f0f08f91900b7d6565e4dcd64191b548e438edeba |
| [all-in-one/registers/regulation-manual.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/registers/regulation-manual.json) | 3b5309ec06f35610ab57e6ef85bd7eb6f7c83ec7db149db1b881b9b65bce91fe |
| [all-in-one/registers/sensor-measurement.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/registers/sensor-measurement.json) | 4b8c357c803e7b429766d54a87bf49bb5dd25343a9797b44b5702df93440c7a3 |
| [all-in-one/sources/Electrical_Can_Decoating_20241118.pdf](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/Electrical_Can_Decoating_20241118.pdf) | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| [all-in-one/sources/Electrical_Rev2.pdf](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/Electrical_Rev2.pdf) | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| [all-in-one/sources/GME_20250506.zap18](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/GME_20250506.zap18) | 00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8 |
| [all-in-one/sources/PEData.plf](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/PEData.plf) | 647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a |
| [all-in-one/sources/PID_1684n002I.pdf](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/PID_1684n002I.pdf) | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| [all-in-one/sources/decoded-original/0014-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0014-FlgNet.xml) | 2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30 |
| [all-in-one/sources/decoded-original/0023-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0023-FlgNet.xml) | 868f9cce5f0759fac0fb4a1a23599fa166ffa29978b430c84d1b8cf03bb3d347 |
| [all-in-one/sources/decoded-original/0030-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0030-FlgNet.xml) | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b |
| [all-in-one/sources/decoded-original/0031-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0031-FlgNet.xml) | 76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65 |
| [all-in-one/sources/decoded-original/0032-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0032-FlgNet.xml) | 070bb8efa33d03b18add5da81d3f670a47c12b288076b7bfee11ac87fe6fa7e4 |
| [all-in-one/sources/decoded-original/0154-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0154-FlgNet.xml) | b0a163ffa382b722eaa34df4bdc4c3dd06039b296b791d26d68639a7b0502746 |
| [all-in-one/sources/decoded-original/0158-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0158-FlgNet.xml) | d3f3adebc3d990b85c5d4c294906ae3bc3dafebb49d25b030bf9cc2ccf905651 |
| [all-in-one/sources/decoded-original/0173-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0173-FlgNet.xml) | b4f2002933f13ad38f8b8bc6daa3f3ef11a9181ea1c2f33f63ef7a3f7305dc07 |
| [all-in-one/sources/decoded-original/0175-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0175-FlgNet.xml) | 41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97 |
| [all-in-one/sources/decoded-original/0182-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0182-FlgNet.xml) | f11326ea7f915ce3d9347f72a4b314635e0943fc251db9a67694aedd3795dd0b |
| [all-in-one/sources/decoded-original/0184-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0184-FlgNet.xml) | a0a59597c73eb68e1cbdb2f41d640eabccfd05655c4e9c08624be6027974caf3 |
| [all-in-one/sources/decoded-original/0186-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0186-FlgNet.xml) | 932f8756ee0e4385553944bd166109c45684766a136bfddd68cdf08552a83883 |
| [all-in-one/sources/decoded-original/0187-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0187-FlgNet.xml) | 0d4e4dd53c729f48c4ad275eba51d89fab582958032f9eae6f722daff808e027 |
| [all-in-one/sources/decoded-original/0291-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0291-FlgNet.xml) | fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550 |
| [all-in-one/sources/decoded-original/0346-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0346-FlgNet.xml) | 7c782d799751476d88794a5d3d993e91878e03a39147d3b13233193dd3f6ce09 |
| [all-in-one/sources/decoded-original/0398-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0398-FlgNet.xml) | 4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747 |
| [all-in-one/sources/decoded-original/0416-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0416-FlgNet.xml) | 1838d3c52dbc3319af0d7aabbb6477af9e862075b12a990412e6bd69a1d1cd0d |
| [all-in-one/sources/decoded-original/0489-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0489-FlgNet.xml) | 942f08041c83fbac9a870743e71135d5e4251f28468be2271bab86ba61873b2b |
| [all-in-one/sources/decoded-original/0490-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0490-FlgNet.xml) | 8c3423f973afdf6356c1fdf0d303203c9561ddc197b3566da5e6cbc25b737655 |
| [all-in-one/sources/decoded-original/0492-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0492-FlgNet.xml) | f97288e870de4e6d3528ebc194428d0fb961b9893d661ed875ad8170fa90653b |
| [all-in-one/sources/decoded-original/0493-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0493-FlgNet.xml) | 991673aed363870b817d18e14865ffb8c89a955e3780331e5a3b25dfe8595a38 |
| [all-in-one/sources/decoded-original/0498-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0498-FlgNet.xml) | 88d25f691eb2199794f0013d98a91cd42bf6a9dec98d64b290014b72e7ab8fcd |
| [all-in-one/sources/decoded-original/0499-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0499-FlgNet.xml) | 6526c8da7b45f38e72d8ebd8c177889a58f7e2db7265d1572db5a8c7dd6e0467 |
| [all-in-one/sources/decoded-original/0527-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0527-FlgNet.xml) | a91f3876643dbdb796d24833a5d67301ff72a3e41365e52f12ec4509b0f41196 |
| [all-in-one/sources/decoded-original/0530-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0530-FlgNet.xml) | 9f20c55030b3127abfedce38de08e50d494885cdf61d75c85a2715b0d380eac5 |
| [all-in-one/sources/decoded-original/0531-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0531-FlgNet.xml) | d53b8ca1482c4365251a3b1d0f108ed32fa4e5b8f78848e2ceb48648f2d7095e |
| [all-in-one/sources/decoded-original/0532-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0532-FlgNet.xml) | 63b649820f729a693a38203c57eb79c1a25fbd4374e3e3aa79609b47f1c3c980 |
| [all-in-one/sources/decoded-original/0533-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0533-FlgNet.xml) | 3fd228af5f1eeb7c88b48cef59b9faa2e601cbe318498a26c8c339957fc01d58 |
| [all-in-one/sources/decoded-original/0534-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0534-FlgNet.xml) | f46e2d9c9dbe465d1068ecf0cc52909e0f8a2691347b533028a908937461a611 |
| [all-in-one/sources/decoded-original/0549-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0549-FlgNet.xml) | 49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1 |
| [all-in-one/sources/decoded-original/0564-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0564-IdentXmlPart.xml) | 2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1 |
| [all-in-one/sources/decoded-original/0565-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0565-IdentXmlPart.xml) | 0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149 |
| [all-in-one/sources/decoded-original/0566-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0566-IdentXmlPart.xml) | a1914c7ae085acc1f949a649979824bec8b46fcd78a8055318272a1eb5a45265 |
| [all-in-one/sources/decoded-original/0567-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0567-IdentXmlPart.xml) | 5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e |
| [all-in-one/sources/decoded-original/0582-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0582-IdentXmlPart.xml) | 41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951 |
| [all-in-one/sources/decoded-original/0584-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0584-IdentXmlPart.xml) | 3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d |
| [all-in-one/sources/decoded-original/0585-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0585-IdentXmlPart.xml) | e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184 |
| [all-in-one/sources/decoded-original/0586-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0586-IdentXmlPart.xml) | f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250 |
| [all-in-one/sources/decoded-original/0611-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0611-IdentXmlPart.xml) | 0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089 |
| [all-in-one/sources/decoded-original/0612-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0612-IdentXmlPart.xml) | 95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38 |
| [all-in-one/sources/decoded-original/0617-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0617-IdentXmlPart.xml) | 10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9 |
| [all-in-one/sources/decoded-original/0619-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0619-IdentXmlPart.xml) | 85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456 |
| [all-in-one/sources/decoded-original/0627-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0627-IdentXmlPart.xml) | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| [all-in-one/sources/decoded-original/0628-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0628-IdentXmlPart.xml) | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd |
| [all-in-one/sources/decoded-original/0629-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0629-IdentXmlPart.xml) | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| [all-in-one/sources/decoded-original/0631-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0631-IdentXmlPart.xml) | 8e5072374f8ef098de72fbf93965b2a7bb0965c0f803e397daa68588c0c38555 |
| [all-in-one/sources/decoded-original/0634-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0634-IdentXmlPart.xml) | af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d |
| [all-in-one/sources/decoded-original/0635-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0635-IdentXmlPart.xml) | 1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457 |
| [all-in-one/sources/decoded-original/0648-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0648-IdentXmlPart.xml) | afaa47ae737d9333fe831ffac2b1d1388f108bb6a2b23d03554fa862f7edb454 |
| [all-in-one/sources/decoded-original/0649-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0649-IdentXmlPart.xml) | 38f59e654ecfbc2066fa1f8beeb9ced952adc405f8a4fcf3ef233e9d5d026576 |
| [all-in-one/sources/decoded-original/0650-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0650-IdentXmlPart.xml) | 86f53657eb7afb0798da0e215ba226721076c2ab1b25b74eb83e7b3c4b2d8a2d |
| [all-in-one/sources/decoded-original/0651-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0651-IdentXmlPart.xml) | 549c09fb14ce6e9734a2ba604c78868647451f24d224ead0d17d209f66428111 |
| [all-in-one/sources/decoded-original/0652-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0652-IdentXmlPart.xml) | 251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692 |
| [all-in-one/sources/decoded-original/0672-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0672-IdentXmlPart.xml) | 6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222 |
| [all-in-one/sources/decoded-original/0674-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0674-IdentXmlPart.xml) | 4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84 |
| [all-in-one/sources/decoded-original/0676-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0676-IdentXmlPart.xml) | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 |
| [all-in-one/sources/decoded-original/0678-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0678-IdentXmlPart.xml) | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 |
| [all-in-one/sources/decoded-original/0680-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0680-IdentXmlPart.xml) | fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95 |
| [all-in-one/sources/decoded-original/0682-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0682-IdentXmlPart.xml) | 25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092 |
| [all-in-one/sources/decoded-original/0683-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0683-IdentXmlPart.xml) | 0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22 |
| [all-in-one/sources/decoded-original/0684-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0684-IdentXmlPart.xml) | 6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208 |
| [all-in-one/sources/decoded-original/0685-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0685-IdentXmlPart.xml) | 2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448 |
| [all-in-one/sources/decoded-original/0686-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0686-IdentXmlPart.xml) | b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4 |
| [all-in-one/sources/decoded-original/0688-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0688-IdentXmlPart.xml) | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda |
| [all-in-one/sources/decoded-original/0692-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0692-IdentXmlPart.xml) | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| [all-in-one/sources/decoded-original/0694-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0694-IdentXmlPart.xml) | 757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d |
| [all-in-one/sources/decoded-original/network-map.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/network-map.json) | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 |
| [all-in-one/sources/hmi-windows.csv](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/hmi-windows.csv) | 15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e |
| [all-in-one/sources/hmi_plc_tags.csv](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/hmi_plc_tags.csv) | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
| [all-in-one/sources/live_index.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/live_index.json) | 14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1 |
| [docs/equipment-standard/INVENTORY.json](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/docs/equipment-standard/INVENTORY.json) | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc |


### 이번 읽기 전용 검사 결과

- 조사자료 해시 83개를 계산·저장 후 다시 읽어 일치 확인했다. 위 고정 저장소 Git 상태는 착수/완료 모두 변경0이다.
- sources/source-manifest.json: 9파일 해시 확인, 불일치0. 중지 자산은 바이트 해시만 읽었으며 import/생성/실행하지 않았다.
- registers/additional-source-manifest.json: 3파일 해시 확인, 불일치0. 중지 자산은 바이트 해시만 읽었으며 import/생성/실행하지 않았다.
- registers/simulator-freeze.json: 5파일 해시 확인, 불일치0. 중지 자산은 바이트 해시만 읽었으며 import/생성/실행하지 않았다.
- 정적 원본 재열람: 30네트워크, Parts 컨테이너 원소820개(Part/CRef/ORef 포함), Wire735개, ORef476개를 원본과 대조했다. 시뮬레이터나 논리 평가기를 사용하지 않았다.
- 핵심1979의31개 ORef,1986의20개 ORef는 모두 동일 원본 RID/UID/NID 선언과 연결된다. 0158의TOF ET 두 ORef71/76은 원본 RefId 자체가 없어 미결속으로 유지한다. 공통Reset 전달주장의 피연산자로 사용하지 않았다.
- 전역숫자 검색에서0291 ORef41/RID25,0175 ORef249/RID1,0346 ORef24/RID1 등의 타블록 후보가 중복된다. 블록·종류·핀·선언파일 경계를 보존했으며 첫 검색결과로 자동 확정하지 않았다.
- SCL1719 검색색인 문자는 기존 독립조사와 정확히 일치한다. 문자 SHA256 bd2a1cf95892d12834cbabd34735484c1131add722144ccabc753de13e647c7a. 추가 native 선언을 확인했지만 native 본문/컴파일/현재실행 상태는 미확정이다.
- PDF 원본13쪽을 직접 렌더·시각확인했다: OEM78/79/81/98/100/107/108/111,시공3/6/56/64,P&ID1. 페이지별 개정란·원시회로와 시공구역 상충을 유지했다.
- preflight.py 기본 읽기전용 실행 종료0: inventory_matches=true. 원본248/우선23/기존제외90/부모하위보류7/2차133을 유지한다. source_byte_changes의requirements-audit/all-in-one-data 두 파일은 고정판의 기존 확장내용 차이이며 이번 작업에서 편집하지 않았다.
- 미실행: 모든 생성기·정식설비/BC01회귀·UI/기록·패키지/배포·TIA/CPU·현장 복구검증. 문서조사만으로 이 상태를 passed 또는 완료로 바꾸지 않는다.
