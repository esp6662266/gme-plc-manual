# TC09 백 필터 유입 온도 — 고유 원본 조사 7영역 초안

## 핵심 확인·상충·누락

- TC09 한 개의 문서 조사다. `%IW386:P` Int → Signal linearization → `Data.TC_09` DB1.DBW262이며, `TC09_OFR` DB3.DBX20.4는 별도 Bool 출력이다.
- 0539 고유 경보에는 타이머가 없다. Open false air는 TC09_MAX 초과 때 Set, MAX_TC09는 MAX+5 초과 때 Set, 둘의 회복 비교는 MAX−2 미만이다. 다른 TC의 3초를 가져오지 않는다.
- MAX_MAX_TC09는 `Temp>TC09_MAX_MAX OR Temp>200 OR Temp<-60` 래치다. 고온뿐 아니라 저범위도 포함한다. 설정/상수는 현행 안전값이나 조작 권고가 아니다.
- OEM FG171/PDF172의 PEW386·PEW388은 둘 다 TC09라고 적혀 있다. PLC 고유 호출은 IW386:P 하나로 확인했다. 도면은 4–20mA 문구와 U0+/U0−, U1+/U1− 단자 연결이 공존한다. 실제 모듈 모드·변환기·두 채널 관계는 미확정이다.
- 시공 PDF60의 10_6 행은 텍스트 추출에는 있지만 실제 렌더에서 검은 띠로 가려져 있다. 유효 배선으로 채택하지 않는다. 보이는 10_9는 BF01/JB01→PV14/TC09, TC/KX/2S1.0이다.
- MAX_MAX는 BR01 허가/정지, RD01 투입금지, FN04 요청 Reset의 관련 입력이다. Open false air/MAX/MAX_MAX는 PV14 출력의 OR 가지다. 밸브·팬·버너 소유와 실물 복구를 TC09 완료로 합산하지 않는다.

공유 재사용: [BF01](BF01-DOTS-DRAFT.md), [TC03](TC03-DOTS-DRAFT.md)의 같은 고정입력 공통 선형화0291/0014, startup0148 Word 초기화, main0549 호출 설명을 연결 재사용한다. 아래 TC09 호출·경보·각 소비핀과 PDF3쪽은 직접 확인했다. 기존 자료 없는 현행 실물 보류를 재검색으로 해결했다고 하지 않는다.

## 1. 설비·자료 기준

- catalog_id TC09, sensor/계측, parent 없음, depth0, 별칭 tc_09, INVENTORY catalog[19], equipment[83], phase2/planned. 역할은 백 필터 유입 온도. TC01/02/03/04/05/06/07/10/11과 같은 표시명이지만 별도 ID다.
- 범위: BATCH08-RESEARCH-INSTRUCTIONS.md, TASK3-BATCH08-SCOPE.json, GME-CATALOG-OVERLAP-REVIEW.json 해당 행. 실물 동일성 미확인, 신규 자체조사이며 로컬 2차133 통합 제외 유지.
- 원본 `gme-research/source-mv06`, 고정 commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 사용자 보고의 최신 게시·현행 CPU 검증과 별개다.
- root AGENTS, 설비확대 스킬/source-map, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, START-GPT61 및 VERSION/EXPANSION-WORK/WORKSPACE-HANDOFF/PUBLICATION_STATUS/ACTIVE-WORK 상단을 읽었다. 배치의 최신 자체조사 지시를 적용한다.
- 실행 모델 런타임 증명 미확인. 원본/공유코드/대장/버전/배포/운영 기록 편집0, 신규 Work/Codex/재위임0. 시뮬레이터 작성·수정·생성·실행·행동시험0, PLC/현장/보호값/SEJIN 변경0. 원본 build/test/generator 실행0.
- 원본 경로 기본: `source-mv06/all-in-one/sources/decoded-original/`. 0483 등은 FlgNet 파일번호이며 LAD 문서번호/NID와 다르다. RID/UID는 블록 문맥과 선언 NID를 함께 결속한다.

| 영역 | 적용/미확보 | 경계 |
|---|---|---|
| 설비·자료 기준 | 적용 | 백업/실물 동일성 미확인 |
| I/O·HMI | 적용/부분 미확보 | 주소·형식·설정/실제 화면 이벤트 미확인 |
| 제어 구조 | 적용 | 환산·소비·Word 겹침/현재 스캔 미검증 |
| 전기 끝점 | 적용/부분 미확보 | OEM·시공 실제 렌더/모드·변환기·2채널 미확정 |
| 알람·복구 | 적용/복구 미확보 | 직접 S/R·무타이머/현장 복구 미수행 |
| 증상 관찰 | 적용 | 읽기 전용 관찰계획, 조작 지시 아님 |
| 완료·누락 | 적용 | 문서·제품/UI·현장 상태 분리 |

## 2. I/O·HMI·저장값

### 2.1 선언 결속

SSD.AO는 bit offset이며 Int/Word 주소는 AO÷8이다. BAD BIRID는0674/0682의 DepDBBlock TOD와 결속: Coeff DB4, Data DB1, Allarm DB3, Flag DB2. Local 임시변수에 DB주소를 부여하지 않는다.

| 대상 | 형식·백업 주소 | 직접 선언/참조 |
|---|---|---|
| TC09 원시 | Int IW386:P | 0678 SimpleAccess RID19, AO3088, SAD Input SAM=Peripherie, NID3 UID94 |
| ZERO_TC09 / COEFF_TC09 | Int DB4.DBW128/130 | 0676 Global RID21/20 AO1024/1040, NID3 UID96/95 |
| Data.TC_09 | Int DB1.DBW262 | 0676 RID22 AO2096 NID3 UID97 Write;0684 RID103 NID13 UID1102/1108/1114/1120/1122/1124 Read |
| TC09_OFR | Bool DB3.DBX20.4 | 0676 RID359 AO164 NID3 UID23 Write |
| TC09_MAX / TC09_MAX_MAX | Int DB1.DBW54/56 | 0684 RID104/112 AO432/448 NID13 UID1103/1105/1111 및1121 |
| MAX_TC09 / MAX_MAX_TC09 | Bool DB3.DBX8.6/8.7 | 0684 RID108/113 AO70/71 NID13 UID1110·1117 및1126·1129 Write |
| Open false air | Bool M2.1 | 0686 SimpleAccess RID105 AO17, NID13 UID1104 Set/1119 Reset |
| app07 / app03 | Local Int offset160/96bit | 0685 InterfaceAccess RID107/111, NID13 UID1107/1113 Write 및1109/1115 Read |
| RESET_ALLARM / STOP_HORN | Bool DB2.DBX6.0/6.2 | 0684 RID24/16 AO48/50, NID13 UID1127 Read/1118 Set |
| ON | Bool M0.0 | 0678·0686 RID1 AO0, Memory;이름으로 현행 TRUE 단정 안 함 |

별도 IW388의 TC09 전용 환산·HMI 미러는 이 고유 검색에서 확보하지 않았다. FG171의 두 채널을 자동 평균/이중화 또는 TC10 입력으로 바꾸지 않는다. TC09는 다른 TC의 DB13 원시 미러를 복제하지 않는다.

### 2.2 HMI 설정주소 대조

`sources/hmi_plc_tags.csv`에서 이름 TC09 검색은 놓칠 수 있어 주소로 재검색했다. Access Name은 모두 PLC이며 다음8행을 확인했다.

| 태그 | 설정주소 | 내부 ID |
|---|---|---|
| data_DB1_DBW262 | DB1,INT262 | 00289 |
| data_DB1_DBW54 | DB1,INT54 | 00268 |
| data_DB1_DBW56 | DB1,INT56 | 0023E |
| Coeff_DB4_DBW128 | DB4,INT128 | 001F5 |
| Coeff_DB4_DBW130 | DB4,INT130 | 0029F |
| Allarmi_71 | DB3,X8.6 | 00146 |
| Allarmi_72 | DB3,X8.7 | 00145 |
| Allarmi_202 | DB3,X20.4 | 002DA |

CSV는 dde.cfg 백업 설정이다. 현재 화면 위젯, 경보 문장, ACK/쓰기 이벤트, 단위/소수점, 권한, 통신/온라인 값은 증명하지 않는다. 기존 파생 TC09 명세의 “HMI 설정 직접 식별되지 않음”은 이름기반 탐색 결과로 보며, 이번 주소결속으로 보충한다. HMI 전체 구현 완료를 뜻하지 않는다.

### 2.3 백업 저장값과 현행 안전값의 구분

`sources/live_index.json` `_7ev/1604`의 이름/형식/값129개와 `_7ev/1629`의162개 배열 길이가 각각 일치하는 것을 검사한 뒤 위치 대응했다. ZERO_TC09=0, COEFF_TC09=1330, TC09_MAX=180, TC09_MAX_MAX=200, TC_09=61은 **백업 저장값**이다. 61은 현재 측정값이 아니고 180/200은 승인된 안전한계가 아니다. live_index는 보충 추출이며 XML 선언·핀의 대체가 아니다. OEM FG171에서 온도범위 °C 스케일은 확인되지 않아 1330을 현행 °C 풀스케일로 단정하지 않는다.

## 3. 제어 구조·관련 소유

### 3.1 고유 환산 호출

0483 LAD1733 NID3: ON ORef92→W99 Contact105.operand; rail W107→105.in;105.out W106→CRef86.en. ON ORef93→W100 CRef86.IN0. TC09 ORef94 W101→Analog_input, COEFF ORef95 W102→Coeff, ZERO ORef96 W103→Zero. OutValue W104→ORef97(Data.TC_09), Out_of_range W24→ORef23(TC09_OFR). CRef86 RID351는0680 BlockInterfaceInfo, CodeBlock98 RID5는0672 Signal linearization FC 선언과 결속한다.

공통0291/0014는 동일고정근거를 재사용하고 원본 형식/핀을 재확인했다. 유효 raw 범위는 `>-1382 AND <=32767`, Int→DInt Convert164/167/174, Add170/Mul177/Div181의 ENO 연쇄로 `(DInt(raw)+DInt(zero))*DInt(coeff)/28000`, Move185로 Int OutValue. 정수 연산·절삭/오버플로와 ENO 영향은 현재 CPU 미검증이다. 범위외 `raw>32767 OR raw<=-1382`에서 Move193(-9999); Move193.eno W21→Coil23 Out_of_range이므로 단순 비교기 Bool로 치환하지 않는다. 0014 NOT IN0 Contact171→W172 Move162(0)→W170 OutValue. 호출EN=ON이고 IN0=ON이므로 IN0 비활성 공통 경로가 이 호출에서 실제 실행된다고 단정하지 않는다. ON false일 때 유지/갱신은 현재 스캔 확인 대상이다. -9999/0은 코드 대체값이며 안전 대체값이 아니다.

### 3.2 PV14 관련 소유

0216 LAD1903 NID21: ON Contact2035.out W2036이 다섯 OR 가지에 분기한다. M_PV14 Contact2041 W2042→OR2007.in1; Open false air ORef2018/Contact2043 W2044→in2; MAX_TC09 ORef2019/Contact2045 W2046→in3; MAX_MAX_TC09 ORef2020/Contact2047 W2048→in4; Emergency_module_fault ORef23/Contact22 W24→in5. OR2007.out W2031→Coil2012, operand W2033→PV-14 ORef2021. 0594 RID268 AO136 SAD Output SAM=None, NID21 Write이므로 출력 Q17.0이다.

같은망 Fault_PV14 Contact2037 W25→RCoil2004→M_PV14(0596 RID277/UID2016) Reset은 수동 요청 해제다. 이 접점이 온도/비상 OR의 전체 허가 직렬에 있는 것으로 바꾸지 않는다. Q17.0은 PV14 소유 명령이고 개방완료 피드백이 아니다. 밸브 전원·코일·기구 정상/안전위치는 본 조사로 확인하지 않았다.

### 3.3 FN04·RD01·BR01 관련 소유

| 관련 소유 | 고유 소비핀과 의미 | 경계 |
|---|---|---|
| FN04 | 0265 LAD1965 NID35, MAX_MAX ORef1020(0604 RID12)→W1030 Contact1044→W1045 OR1003.in5→W1031 RCoil1010→W1033 M_FN_04 UID1021. 다른 OR는 FN_04_FAULT, FN04_INV, SET_PERC_FN04=0, Local Stop_Fan_FN04. ON 뒤 M_FN_04 Contact1046→W1047 Coil1014→W1036 Start FN04 UID1023 | 0602 RID265 AO137 Output=Q17.1. FN04 명령 Reset과 모터 실물 정지는 다름. FAN 전체 타이머/전기 소유는 기존 FN04 조사 |
| RD01 | 0238 LAD1931 NID2, MAX_MAX ORef73(0604 RID12)→W84 Contact103→W104 OR56.in5;OR56.out W88→Coil66→W90 Local Disable_Load_RD01 UID77(0605 RID16) | 8가지 OR 중 하나. LOW_TC03,산소2종,STANDBY,수소박스,NOT R1 Gate ON,NOT RD01_Fbk와 분리. 실제 투입 차단/복구 확인 아님 |
| BR01 온도 인터록 | 0173 LAD1856 NID3, ON160→NOT MAX_MAX_TC09 Contact162(UID152/W156)→NOT MAX_MAX_TC01 Contact164→W165 Coil150→W159 Temperature Interlock OK UID154 | 0582 RID26 AO54 Output Q6.6. 도면 제목 A56.3을 주소로 채택하지 않음. 버너 외부 안전순서 증명 아님 |
| BR01 준비 | 0174 LAD1857 NID4, NOT MAX_MAX_TC09 Contact209(UID184/W195)가 준비 직렬, 이후 burner faults 반전·FN01/FN04/RD01 Run·(FN06 feedback OR Burner On)·FN02 Run→Coil182 Burner_ready | 각 피드백/허가의 현행 실물 극성 미확인 |
| BR01 정지 | 0175 LAD1858 NID5, MAX_MAX_TC09 UID235 W253→Contact277 W278→OR213.in2→W270 RCoil232→W272 Start_Burner UID250 | 요청 래치 해제이며 연료차단/화염소실/외부 퍼지 실물 검증 아님 |

main0549 LAD1620 NID7은 ON350.out W351의 병렬 호출에 Motors1 CRef319와 Filter CRef322 등이 있다. 0688/0694 결속. ENO 직렬로 실행하는 것으로 바꾸지 않는다. 전체 CPU 호출순서·통신 Writer·현재 프로젝트·물리 응답은 미확인이다.

## 4. 전기 끝점·실제 PDF 확인

실제 원본 PDF3쪽을 렌더하고 이미지로 경로·footer를 확인했다. 이미지: `extracts/TC09/render/`.

| 원본 | 실제 확인 경로·개정 |
|---|---|
| Electrical_Rev2.pdf FG171/PDF172 | TC09 단자3→X3:100→+PEW386→모듈3/U0+;단자4→X3:101→−PEW386→모듈4/U0−/I0−. TC09 단자1→X3:102→+PEW388→모듈7/U1+;단자2→X3:103→−PEW388→모듈8/U1−/I1−. 171SCH1→X3:104→접지. MANA18→−0Vdc152.4(168/9→172/0). CPU515/MOD2 표기 |
| 같은 FG171 footer | ANALOG INPUT MODULE,27.05.2024,FG171/TOT262. 별도 개정 기입 관찰 없음. 두 채널 설명 모두 TC-09 TEMPERATURE CONTROL BF-01 (4–20mA). 인접 PEW390/392는 TC10 SPARE이며 TC09 고유 채널로 편입 안 함 |
| Electrical_Can_Decoating_20241118.pdf PDF35 | DUST ROUTE CONDUIT PIPING(1),CANDC-CONS-E018-035,35/64,D-PAGE18. 211RB 가지3 Pipe16→TC09,LOC PV14,10_9=DUS+PV14-TC09A,KX1.0/2심. DUS1TB1/2를 거치는 ZS/PV14 가지와 TC09 직행 가지를 구분 |
| 같은 시공 PDF60 | CABLE SCHEDULE(9),CANDC-CONS-C010-060,60/64,D-PAGE10. 10_9 =DUS+PV14-TC09A:BF01/JB01→PV14/TC09,Current Type TC,KX,2S,1.0,Spare0. route E500→222RE→222LAP1→212LAP1→211RB→E300,Adjustment25,LEN27. 실제 실측 길이로 표시 안 함 |
| 시공 두쪽 footer | Rev1,24.11.11,first draft design. CHECKED/APPROVED 공란. 현행 승인 준공도라고 하지 않음 |

주의: OEM 4–20mA 설명과 실제 U+ 연결, 시공 KX 열전대선 표기는 원본간 계측 방식·구간의 미확정이다. 정상 형식/센서 타입·냉접점보상·변환기 유무/위치·채널 이중화·현재 모듈 주문번호/구성은 별도 자료가 필요하다. 도면 극성기호는 읽은 사실이며 현장 정상극성 검증이 아니다. OEM와 시공을 자동 연속배선으로 봉합하지 않는다.

시공 PDF60 10_6의 텍스트 레이어는 TC09/NO/NO/2S를 포함하지만 **실제 페이지는 해당 행 전체 검은 띠**다. PDF35에도 DUS1TB1 경유 한 행은 Delete 표기다. 가려진 텍스트를 활성 TC09 루트로 채택하지 않는다. 이번 입력경로에는 릴레이 부하접점이 핵심으로 나타나지 않으므로 타 설비의5/9·하단접점표1/5/9를 복제하지 않는다.

## 5. 고유 알람·복구·Word 겹침

0539 LAD1991 NID13. ON UID1101 W1130→Contact1175,출력 W1176이 아래 비교/산술/리셋 가지를 활성화한다. 모든 비교는 strict Gt/Lt이다. 경계와 같은 값에서 해당 비교는 참이 아니다. 선언은0683 상수/0684 Global/0685 Local/0686 Simple.

| 기능 | 발생·쓰기 | 회복·차이 |
|---|---|---|
| Open false air M2.1 | Gt1046(Temp UID1102 W1131 > MAX UID1103 W1132)→W1133 SCoil1049→W1135 UID1104 | Sub1064(MAX−2) ENO W1148→Lt1068(Temp<app03)→W1151 RCoil1082→W1156 UID1119. MAX 알람이 Set돼 있어야 하는 조건이 이 Reset에는 없음 |
| MAX_TC09 DB3X8.6 | Add1053 Int(MAX UID1105 + constant5 UID1106;W1136/1137)→W1138 Local app07 UID1107. Add.eno W1139→Gt1057(Temp UID1108 > app07 UID1109;W1140/1141)→W1142 SCoil1060→W1144 UID1110 | Sub1064(MAX UID1111−constant2 UID1112;W1145/1146)→W1147 app03 UID1113. ENO W1148→Lt1068→W1151 기존MAX Contact1177(UID1116/W1152)→W1178 RCoil1076/MAX UID1117 및 SCoil1078/STOP_HORN UID1118 |
| MAX_MAX_TC09 DB3X8.7 | Gt1086(Temp>MAX_MAX UID1121),Gt1089(Temp>200 UID1123),Lt1092(Temp<−60 UID1125)→W1160/1163/1166 OR1085.in1/2/3→W1167 SCoil1095→W1169 UID1126 | RESET_ALLARM Contact1179 UID1127/W1170→W1180 기존MAX_MAX Contact1181 UID1128/W1171→W1182 RCoil1100→W1173 UID1129. 이 가지에 온도정상 비교 없음 |
| TC09_OFR DB3X20.4 | 0483 CRef86.Out_of_range→W24 UID23 | 공통0291의 Move193 ENO 코일·0014의 비활성 경로를 구분. MAX/MAX_MAX와 같은 지연·Reset으로 취급 안 함 |

0539에는 SdCoil/TON/TOF/Timer 호출이 없다. “타이머 없음”은 이 고유망의 원본 사실이며 전체 시스템에 처리 지연·샘플링 시간이 없다는 뜻은 아니다. Add/Sub Int ENO를 무시하지 않는다. MAX_MAX Reset은 원인제거 증명이 아니며 원인 지속 때 재Set 가능성/동일 스캔 우선순위는 현재 CPU 미검증이다. STOP_HORN Set은 모든 경보 정상·안전재기동·현장복구가 아니다.

공통 startup0148 LAD403 NID3은 ON329→W330 Move267.en,Int0 UID293 W315→Move267.in, out1 W316→DB3 Word UID294. 0563 RID32 AO64/BAD23 및0562 Allarm DB3 결속으로 DB3.DBW8←0이고 MAX/MAX_MAX DBX8.6/8.7을 함께 덮는다. 이 Word 쓰기는 고유 S/R 외 별도 경로다. TC09_OFR DBX20.4는 이망 W0~16 초기화 범위밖이다. 이 자료만으로 모든 외부/간접 Writer가 없다고 하지 않는다. startup live_index doc401의 ON/OFF STL은0401-FlgNet HMI 출력 미러와 다른 자료다.

## 6. 증상별 읽기 전용 관찰 계획

실제 조작·리셋·센서 탈거·신호 주입·보호값 변경 지시가 아니다. 위험설비 접근은 승인된 현장 절차/자격으로 제한한다.

| 증상 | 같은 시각 확보할 관찰 | 비교·배제·복구 증거 |
|---|---|---|
| 온도 표시 불일치 | IW386:P,DB1W262,ZERO/COEFF,HMI 실제 주소·시각·단위,통신상태 | 원시/환산 구분,정수처리·계수·UI 갱신 검토. IW388를 임의 합산하지 않음 |
| OFR 또는 −9999 | raw,호출EN/IN0,Out_of_range,DB1W262,MAX_MAX | 공통범위외 ENO와 센서/루프/모드/보상선 실제 원인을 분리. 단선이라고 확정하지 않음 |
| false-air 요청만 켜짐 | Temp,MAX,app07/app03,M2.1,MAX/MAX_MAX,PV14 Q17.0 및 피드백 | MAX 초과와MAX+5 초과의 다른 단계,회복MAX−2 비교·다른 OR 원인을 구분 |
| 온도 내려왔는데 MAX_MAX 유지 | Temp,MAX_MAX 설정,경보,RESET_ALLARM | 자동 히스테리시스와 수동요청 Reset 차이. 승인 없는 Reset/재시동 금지 |
| 팬/버너/투입 허가 이상 | MAX_MAX,각 관련 OR/NOT 가지,FN04 요청·출력/피드백,BR01 Q6.6/준비/요청,RD01 금지 | TC09 데이터와 타 설비 고장/전기/기구를 분리. 출력값은 실물 동작 완료가 아님 |
| 두 온도채널/형식 불일치 | TC09 명판·단자1~4·X3 100~104,AI 실제 모듈구성/채널설정,준공도·교정기록 | 4–20mA/U단자/KX 표시 상충을 승인자료로 해소. 지금은 온도센서 형식·극성·범위를 만들지 않음 |

기록 틀: 관찰자·실제시각/시간대·위치·태그/주소·값/단위·신선도·수집장치·프로젝트/CPU ID·비교 원본/개정·원인배제 결과·승인된 조치·별도 복구확인. 운영 기록이나 사진을 새로 작성/공개 복제하지 않았다.

## 7. 완료·검증·누락

| 구분 | 상태 | 근거·경계 |
|---|---|---|
| documentation | complete_with_gaps 초안 | 고유7영역·XML/선언/핀·PDF3쪽·주소HMI·누락 명시 |
| static_review | 자체 문서검사 완료,독립검토 대기 | 검사JSON·선택원본 SHA/고정blob 대조. 프로그램 행동검증 아님 |
| ui_records | not_run | PC/모바일,도면·래더 나란히,저장·재열기·선택복원·전후비교·관찰보고서 미검증 |
| publication | not_published | 기능/코드 통합·버전·게시 수행 안 함 |
| tia_compile | not_performed | 로컬 TIA 접근·추가권한 없음 |
| live_cpu | not_performed | 온라인 프로젝트/CPU/현행보호값 미확인 |
| field_recovery | not_performed | 실물/교정/정상극성/안전복구 미확인 |

네 기능은 TC09에 적용 가능한 목표이나 구현/저장/재읽기/재열기 검증을 한 것이 아니다. 기존 note/repair_observation/미지필드/다른 설비/초안/저장키는 변경하지 않았다. BC01 동등 기능 완료나 현장 정상으로 집계하지 않는다.

남은 자료: TC09 명판/제조사 데이터시트·프로브/변환기 타입·냉접점보상·실제 AI모듈 주문번호/채널모드·IW388 역할, X3/JB1부터 현장까지 승인 준공도·교정 기록, 현행 안전임계/권한승인·HMI 실제 화면 이벤트/경보/통신, 현재 CPU 프로젝트·실제 호출·외부 Writer, PV14/FN04/BR01/RD01 관련 소유의 현장응답. 새 자료 전에는 반복 추정으로 메우지 않는다.

다음 한 작업은 부모의 독립 원본 검토와 순차 초안 전달이다. 사용자의 별도 현장/통합 승인으로 해석하지 않는다. 아래 해시 수는 내용 의미검토 수가 아니며 archive/중지자산은 보존만 확인했다.

### 실제 단계 시각 (UTC)

- 2026-10-11T11:15:19Z — scope_and_instructions_read
- 2026-10-11T11:15:46Z — unique_declarations_extracted
- 2026-10-11T11:16:18Z — OEM172_and_construction60_render_review
- 2026-10-11T11:17:13Z — construction35_render_review_and_consumer_wires
- 2026-10-11T11:17:41Z — backup_value_array_alignment_checked
- 2026-10-11T11:20:31Z — seven_area_draft_written
- 2026-10-11T11:21:29.001795+00:00 — document_assertions_hashes_fixed_blob_checked

### 선정 원본 SHA256·고정 Git blob 전체 대조

67개 선정 원본/맥락/보존 파일 모두 고정 blob 내용일치,중지5자산 freeze일치,원본 Git 변경0. 전체 파일수를 의미검토 완료수로 취급하지 않는다. 검사JSON: extracts/TC09/static-review.json,해시JSON: extracts/TC09/source-hashes.json. 자체검사는 XML 정적문서 검사이며 프로그램/시뮬레이터 실행이 아니다.

| 원본 경로 | SHA256 | 고정 Git blob OID |
|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` |
| `.agents/skills/gme-equipment-rollout/references/source-map.md` | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` | `3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3` |
| `all-in-one/sources/decoded-original/0173-FlgNet.xml` | `b4f2002933f13ad38f8b8bc6daa3f3ef11a9181ea1c2f33f63ef7a3f7305dc07` | `a880d18b10887c0385745539ab80f8fb45e7647b` |
| `all-in-one/sources/decoded-original/0174-FlgNet.xml` | `23fb073206f95c69abc4373d3080081a369e4dd5021c2bd1a90d63029bb908d5` | `8d51310f0ce301bc2d642338e6187e25f472789b` |
| `all-in-one/sources/decoded-original/0175-FlgNet.xml` | `41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97` | `1626da00b3bbcb46f77720271ecf0f50db9dc63b` |
| `all-in-one/sources/decoded-original/0216-FlgNet.xml` | `3a7fa8b0a095f054c543f90d0ffab84a8cd0c60ff1b5ec0101b112dc8f4ff37d` | `97280ef67131ab7a480c8b0030d74de765c14c65` |
| `all-in-one/sources/decoded-original/0238-FlgNet.xml` | `8f6a5537084e092c352552dc469bbe8469b33412971219e51bba211ef607dfa8` | `c1093180555a6a00486d0a7268bb3a059b7cbf9e` |
| `all-in-one/sources/decoded-original/0265-FlgNet.xml` | `f2471b6ab6169e4c082983ea2080a383cf8b13cba4503a9a07f83d0956fbf08a` | `bde7b86a1047ae2eb0508311a6910c0ae2d47a97` |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` |
| `all-in-one/sources/decoded-original/0483-FlgNet.xml` | `b14201384ec26ce89c7e9f132e27034632a567c1058781b5a5ae16f2a40d95d7` | `3b5ea3176612001548095bc0aa46c084508b0a2c` |
| `all-in-one/sources/decoded-original/0539-FlgNet.xml` | `d118d41f5007b112770c77fb33e8c84c2cb0e529e00d781d8837030196a015a5` | `11d48a289d9d3cc74088d9bbdbf230aca456179a` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` | `985b5310b43b1015b5dee286aa0e42800564b94b` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` |
| `all-in-one/sources/decoded-original/0582-IdentXmlPart.xml` | `41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951` | `82636dec064876d0f4cc714ef385b07d6e05efe0` |
| `all-in-one/sources/decoded-original/0583-IdentXmlPart.xml` | `0a34a2b7ad17eba6198dbe53d5c6aa8e87710c7436b832b9d39a075074ab58a8` | `63a23c921a53805f135a0399ba076265907d0eda` |
| `all-in-one/sources/decoded-original/0584-IdentXmlPart.xml` | `3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d` | `0f8dde829be66041bea79e40ccc4586d84ff1da7` |
| `all-in-one/sources/decoded-original/0585-IdentXmlPart.xml` | `e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184` | `16574d37ef3ca61b59ba396c400e269ab1dd3440` |
| `all-in-one/sources/decoded-original/0586-IdentXmlPart.xml` | `f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250` | `266989c590cf52f82e1553f8626a209b8c0b6e0b` |
| `all-in-one/sources/decoded-original/0587-IdentXmlPart.xml` | `bab957ac7c180d9c91b4f904b29e9dbd5812c6ba8f7b9e0c7faf9708605b203e` | `67e84e4b8d43b7c5864ec40fcc2c9fbc2222b436` |
| `all-in-one/sources/decoded-original/0594-IdentXmlPart.xml` | `88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd` | `f38b7d9a52b3d5ae74953da8290f6b417758c1b5` |
| `all-in-one/sources/decoded-original/0595-IdentXmlPart.xml` | `10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52` | `1f24565efac58926dabf5b3fc54ad0e9537410b2` |
| `all-in-one/sources/decoded-original/0596-IdentXmlPart.xml` | `a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0` | `c8b2d1a05727b4ca44e2e4bed9fb58ba2b717576` |
| `all-in-one/sources/decoded-original/0597-IdentXmlPart.xml` | `60e292145fe54912a1da7510c8641a4f4c85efe62e1b5206ee3d92794a28de20` | `2831597d1879bd83f239e838dd4cbe6b3dc64e77` |
| `all-in-one/sources/decoded-original/0598-IdentXmlPart.xml` | `dc001c9370a691546c5dea79f5a1252d6d0a5564754703018c47df4bcc2522bb` | `17a4c24ebc97eb13db483e4c64ac386d6a69125a` |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | `3a92b304baf4dbf6147e944d9778d2da11285cb1` |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` | `30e199288c147aa22d5ce8407178a391b89c6b1b` |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` | `ced032fa747a8544abf17058ee5ebaa78ba9b23b` |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` |
| `all-in-one/sources/decoded-original/0682-IdentXmlPart.xml` | `25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092` | `61182411e912941161eccf4e90c1f174e5379f0a` |
| `all-in-one/sources/decoded-original/0683-IdentXmlPart.xml` | `0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22` | `662acdb9a06c0ba1c0027e7dd215a28f07d3f02b` |
| `all-in-one/sources/decoded-original/0684-IdentXmlPart.xml` | `6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208` | `d67b98b5d5516e0330aae5cfdbee41a3e09206e1` |
| `all-in-one/sources/decoded-original/0685-IdentXmlPart.xml` | `2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448` | `86bda988d9efedba92ba2f3e4877497d9eb5230a` |
| `all-in-one/sources/decoded-original/0686-IdentXmlPart.xml` | `b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4` | `8c152d926692a8e15973c980e08e338d29411814` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |
