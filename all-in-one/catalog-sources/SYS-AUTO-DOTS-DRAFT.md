# SYS-AUTO — 자동 기동·정지·유지보수 자체 조사 초안

## 먼저 확인할 핵심
- SYS-AUTO 한 catalog ID의 소프트웨어 기능 조사다. 실제 모터·밸브·버너 또는 그 하위부품 완료를 포함하지 않는다.
- FC30 Auto start motors는 0024-FlgNet.xml의 ON 접점으로 호출된다. 호출자 제목 `cyc_int2 ogni 1s`/`cyclic interrupt 1 second`와 FC 제목 `this fc is recalled every 1ms`가 상충한다. 호출마다 +1 하는 Int 카운터를 현행 실시간 초 단위로 확정하지 않는다.
- Auto_ON1, STANDBY_ON, Maintenance_ON은 각각 DB2.DBX7.3/.4/.5. HMI AbilitaAuto/AbilitaMaintenance는 .3/.5 설정 주소와 대응하지만 버튼 이벤트·운영 권한·현재값은 미확인이다.
- 예열/생산은 단계별 S/R 요청 쓰기다. 시작 요청이 곧 전기 출력 또는 운전 응답은 아니다. 대표 RD01/MC04 하위 Reset 조건을 직접 대조했다.
- D37 표시는 Auto_ON1=0에서 Tipo_preset, =1에서 -1이다. 검색 문자열 순서만 보면 반대로 오독할 수 있다.
- 예열의 STANDBY Set, 생산의 STANDBY Reset, 유지보수의 UNDER TESTING/Allarm.Maintenance_ON 전달을 구분한다. 유지보수를 안전 정지 모드로 설명하지 않는다.
- 고유 검토: 0024, 0162~0169, 0237/0238/0243/0247, 0550/0551. 공유 참조: BF01 초안의 startup Word 초기화·ON/OFF 한계, 기존 RD01/MC04/PV01/PV02/BR01/FN01 초안의 최종 출력·회로 경계. 공유 도면을 다시 전체 조사하지 않았다.

## 1. 설비·자료 기준

- catalog: `docs/equipment-standard/INVENTORY.json#/catalog/36`, software/공통 시스템, 부모 없음, phase2. 별칭 abilitaauto/abilitamaintenance/standby/maintenance는 식별어이며 물리 장치 네 개가 아니다.
- 고정 원본: `gme-research/source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 이후 게시판본·현행 CPU 검증으로 확대하지 않는다.
- 아래 XML 경로 약칭은 `all-in-one/sources/decoded-original/` 기준. LAD 번호는 network-map/live_index 문서 ID이며 XML 파일번호와 다르다.
- 7영역 중 1/2/3/5/6/7 적용, 4는 소프트웨어 직접 물리 단자 비해당 + 연결 대상의 현장 끝점 미확정. 불명확한 직접 회로를 만들어 채우지 않는다.
- 요청 모델/추론 수준의 런타임 증명은 미확인. Windows/TIA 추가 접근, 현재 CPU 접속, 새 환경, 시뮬레이터 실행, PLC/현장/보호값/SEJIN 변경은 수행하지 않았다.

## 2. I/O·HMI 및 선언

0576 DepDBBlock의 Flag RID3/TOD2, Data RID6/TOD1과 0577 GlobalAccess의 BAD를 결속했다. AO는 bit offset이다.

|신호|원본 선언|주소·형식|역할과 한계|
|---|---|---|---|
|Flag.Auto_ON1|0577 RID4, AO59, BAD3; NID1 UID70/74, NID10 UID30 Write|DB2.DBX7.3 Bool|시퀀스 동작 비트. 일반 안전 허가와 동일하지 않음|
|Flag.STANDBY_ON|0577 RID29 AO60/BAD3, NID3 UID611 S, NID4 UID968 R|DB2.DBX7.4 Bool|예열·생산·정지·no sequence에서 다르게 쓰임|
|Flag.Maintenance_ON|0577 RID17 AO61/BAD3, NID3 UID595/NID4 UID939 R|DB2.DBX7.5 Bool|시퀀스 첫 단계 Reset, 외부 HMI 요청 별도|
|Flag.RESET_ALLARM|0577 RID16 AO48/BAD3|DB2.DBX6.0 Bool|시퀀스 SCoil이 쓰는 내부 Reset. HMI Reset 요청과 별개|
|Data.Tempo_presetting|0577 RID7 AO768/BAD6, Int|DB1.DBW96|호출마다 증가하는 정수 단계 카운트. timer type 아님|
|Data.Tipo_preset|0577 RID12 AO784/BAD6, Int|DB1.DBW98|1 예열, 2 생산, 5 정지, 6 no sequence 분기|
|Data.D37|0577 RID13 AO720/BAD6, Int|DB1.DBW90|0163 가공 표시값, 카운터/물리 응답 아님|
|UNDER TESTING|0602 SimpleAccess RID4, AO45 Memory, NID1 UID40 Write|M5.5 Bool|0237에서 유지보수 상태를 전달. 시험을 실행했다는 뜻 아님|
|Allarm.Maintenance_ON|0604 RID6 AO61/BAD5; 0603 Allarm TOD3|DB3.DBX7.5 Bool|별도의 상태/알람 영역. DB2.DBX7.5와 동일 저장소 아님|
|MemoCMD_PV1_Startup / BC01_Startup|0575 RID110/115 AO1446/1447 Memory|M180.6/.7 Bool|요청 기억, 실제 게이트/벨트 응답 아님|
|Tag_292|0575 RID109 AO725 Memory, NID10 UID51 RW|M90.5 Bool|0168 PContact 에지 기억|

HMI `hmi_plc_tags.csv` 실제 행73 AbilitaMaintenance DB2,X7.5/ID00409, 행632 AbilitaAuto DB2,X7.3/ID000DB; 행203/255/284 data_DB1_DBW90/96/98는 각각 DB1,INT90/96/98. CSV는 dde.cfg 설정 추출이며 현재값이나 사용자 조작 이벤트를 증명하지 않는다. DB2,X7.4 정확 주소의 행은 이번 CSV 검색에서 발견하지 못했다. 이름의 부재를 HMI 화면·PLC 쓰기 전체 부재로 확대하지 않는다. 원본 dde.cfg 독립 파일과 버튼 OnPress/OnRelease/스크립트·권한·쓰기 방향의 직접 결속은 추가 필요하다.

Local 구분: 0238의 Disable_Load_RD01은 Local InterfaceAccess이며 물리 Q나 전역 운전허가로 바꾸지 않는다. 0162~0169 핵심 모드·단계 신호는 GlobalAccess다. 선언 파일 간 UID/RID/NID가 같아도 다른 블록 문맥일 수 있다. 추출의 복수 후보는 보존했고 0162 UID74는 0577 Flag.Auto_ON1을 이 FC의 문맥으로 선택했다.

## 3. 제어 구조 및 고유 원본 핀

### 3.1 호출·시간·표시
- 0024 / LAD1723 / NID4: W190 rail→Contact188.in, ORef185/RID36(0652 ON)→W187→188.operand; 188.out→W189→CRef183.en. CRef183/RID40 안 CodeBlock186/RID39는 0067 FCBlock Auto start motors/TOD30/NID4 UID186 Call이다. 다른 Main 모터 호출과 별도 cyclic interrupt 경로다.
- `live_index.json` i1716 Name `cyc_int2 ogni 1s`, Title `cyclic interrupt 1 second`; i1838 Auto start motors Title `this fc is recalled every 1ms` 상충. 블록 제목은 스케줄 하드웨어 설정 증명이 아니다. 현재 OB 주기/우선순위·실제 다운로드 프로젝트가 필요하다.
- 0162 / LAD1841 / NID1: ON Contact88 후 Auto_ON1 Contact90→W91→Add59.en. ORef71/RID7→W80→in1, 상수1 ORef72/RID8→W81→in2, W82 out→ORef73/RID7. 병렬 NOT Contact92(Auto_ON1 ORef74)→W93→Move66.en, 0 ORef75→W85→in, W86 out1→ORef76/RID7. 따라서 허가된 호출에서 Auto=1이면 +1, Auto=0이면 0이다. 카운트 건너뜀/오버플로·실제 초 환산은 검증하지 않았다.
- 0163 / LAD1842 / NID2: NOT Contact115(Auto ORef97)→W116→Move87; Tipo ORef98→W106→in, D37 ORef99←W107 out1. 정상 Contact117(Auto ORef100)→W118→Move93; -1 ORef101→W110→in, D37 ORef102←W111. 즉 진행 중 -1 표시, 비진행 중 preset 값이다.

### 3.2 예열·생산 단계 요청

숫자는 Tempo_presetting의 Int **Eq** 비교값이다. 1초 경과시간 확정값 또는 운전절차 지시가 아니다. S=Set, R=Reset, M=Move. Flag 접두어를 생략했다. 하위 설비의 자체 인터록·복수 쓰기가 최종 요청을 바꿀 수 있다.

예열 0164 / LAD1843 / NID3: ON Contact785→NOT Emergency Contact22→Eq400(Tipo=1)→Contact823(Auto_ON1)→W672 단계 비교들의 pre. 선언 0575~0580/0577.

|카운트|직접 쓰기|대표 Part/Wire|
|---|---|---|
|1|S RESET_ALLARM, R Maintenance_ON|Eq406 W675→S410/R412; W676/677|
|3 / 5 / 8|S VR03/04/05; S SC01/10/11; S FN04|Eq416/428/440, W681/688/695|
|15|S STANDBY_ON|Eq446→W700→S449, ORef611 W702|
|17|R VS01/MC05/MC04/Enable_R2_GATE|Eq452→W705→R456/458/460/462, W706~709|
|19 / 21|S RD01_FAN; S RD01 및 M SET_PERC_FR01=25|Eq466/472 W713/718, Move481 W720/721|
|24|S BC01 및 MemoCMD_BC01_Startup, M Set_Perc_VT02=75, S FN02|Eq486 W725; S492→W104→S102; Move495 W727/728; S500|
|26|S Enable_R1_GATE 및 MemoCMD_PV1_Startup|Eq503 W27→S506→W36→S34; ORef29/38 W28/37|
|28 / 30|S VR01/02와 R CH01; S FN01, M SET_PERC_VT01=35|Eq509 W738; Eq521 W745, Move530 W747/748|
|33 / 36|OFF 조건을 거친 R FN02; S FN03|Eq535→W30→Contact794(OFF)→W31→R539; Eq542 W758|
|40|S RESET_ALLARM/FN06|Eq548 W763→S552/S554|
|45|S Start_Burner/AUTO_BURNER; 별도 OFF 분기에서 TC01=850/TC03=500 Move|Eq558 W769; OFF Contact791→W792→Move568/573; S578/581는 OFF 후단 아님|
|50|R Auto_ON1|Eq584 W781→R587, ORef667 W783|

예열 부가 기억: Eq400.out→W33→Not827→W831→R828(MemoCMD_BC01_Startup/ORef829 W832). 이는 Auto 접점823의 NOT로 임의 바꾸지 않는다. 타입=1/상위허가 결과의 Not 분기다. 실제 실행·retention 효과는 미검증.

예열 PV1 TON: 0164 LRef835/RID116(EN=false/ENO=false), Instance836/RID117→0580 `T_Reset_Startup_PV1` DB38; 0579 Instruction RID116 TON/NID3 UID835 문맥. Eq400 상위 결과 후 Enable_R1_GATE Contact833와 MemoCMD Contact834 직렬→W849→IN, ORef841/RID118 `T#1M`→W850→PT. Q→W851→R837(Enable_R1_GATE)→W854→R838(MemoCMD). ET는 W852 ORef842의 미결속 수신처이며 동작 결론에 사용하지 않았다. 별도의 1분 IEC TON을 정수 단계 카운트와 섞지 않는다.

생산 0165 / LAD1844 / NID4: ON1145→NOT Emergency1154→Auto1147→Eq737(Tipo=2)→W1021 각 Eq.pre.

|카운트|직접 쓰기|대표 Part/Wire|
|---|---|---|
|1 / 3 / 6 / 10|S RESET_ALLARM+R Maintenance; S VR03/04/05; S SC01/10/11; S FN04|Eq743 W1024; Eq753 W1030; Eq765 W1037; Eq777 W1044|
|18 / 21 / 24|S VS01; OFF Contact1149 후 S MC05; S MC04|Eq783 W1049; Eq789 W1054→1149→W1150→S793; Eq796 W1060|
|27 / 30 / 33|S Enable_R2_GATE; R STANDBY; S RD01_FAN|Eq802 W1065; Eq808 W1070→R811; Eq814 W1075|
|35 / 40 / 43|S RD01+M FR01=25; S Enable_R1_GATE; S BC01|Eq820 W1080; Eq834 W1087→S1158; Eq840 W23→S1162|
|46 / 49 / 52|S VR01/02/CH01; S FN01+M VT01=35; S FN02+M VT02=80|Eq846 W1097; Eq858 W1104; Eq872 W1111|
|56 / 60|S FN03; S RESET_ALLARM/FN06|Eq886 W1118; Eq892 W1123|
|62 / 65|S Start_Burner/AUTO_BURNER, OFF 조건으로 TC01=850/TC03=500 Move; R Auto_ON1|Eq902 W1129, OFF1151 W1152→Move912/917, S922/925 별도; Eq928 W1141→R931|

상수25/35/75/80/850/500은 백업 코드의 쓰기값이다. 안전·정상·현행 보호 설정으로 권장하지 않는다. OFF는 명명만으로 항상 false라고 확정하지 않는다. BF01 공유검토의 startup doc401 원문 `set s "on" clr s "off"`에서 CLR 다음 S를 R로 바꿔 읽지 않으며 retention/실제 초기값은 미확정이다. doc401과 0401 HMI Output XML은 별개다.

### 3.3 정지·비상 전환·대기
- 0168 / LAD1846 / NID10: Emergency ORef52→W50→PContact21.operand, Tag_292 ORef51→W49→bit. 상승 에지 out→W48→Move22.en, 0→W34→in, out1 W36→Tempo. Move22.eno→W35→Move23.en, 5→W37→in, out1 W39→Tipo. Move23.eno→W38→S24(Auto ORef30 W40). ENO 연쇄이므로 모든 상황 무조건 세 쓰기라고 표현하지 않는다. 비상 해제만으로 재기동 허가를 확인할 수 없다.
- 0166 / LAD1847 / NID5: Auto Contact1095→W26→Eq881(Tipo=5)→W1031 각 분기. 각 단계 Eq와 Emergency 접점은 O(2) 병렬. 따라서 이 **공통 상위 조건 아래** Emergency가 참이면 단계값을 기다리지 않는 Reset 분기가 있다. 안전릴레이와 같은 물리 기능이라고 주장하지 않는다.
- 정지 요청: 카운트1 FN03/FN02/FN06 R(Eq887·O54 W1034), 5 CH01/FN01_FAN/FN01 R(Eq901·O51 W1042), 11 VR01/02 R(Eq913·O48 W1049), 13 BC01/FN04/ER01 R(Eq923·O45 W1055), 15 RD01/Enable_R1_GATE R(Eq935·O42 W1062), 17 RD01_FAN R(Eq945·O39 W41), 19 MC04 R(Eq951·O36 W38), 20 VR03/04/05 R(Eq957·O33 W1078), 21 STANDBY/VS01 R(Eq969·O30 W1085), 25 Auto R(Eq979·O27 W29). 원본 제목 “complete engine stop”은 전체 Q/에너지 차단 증명이 아니다. 표에 없는 SC 출력이나 버너 내부 정지를 추가하지 않는다.
- 0167 / LAD1848 / NID6: Auto954→Eq914(Tipo=6); Tempo=1 Eq920→W945→S923(STANDBY ORef935 W947); Tempo=25 Eq926→W950→R929(Auto ORef938 W952). no sequence라는 제목만으로 아무 쓰기 없다고 설명하지 않는다.

### 3.4 유지보수·대기의 실제 하위 영향과 출력 경계
- 0237 / LAD1930 / NID1: ON47→Maintenance49→W50→Coil34와36 병렬. W44 ORef40=UNDER TESTING(M5.5), W45 ORef41=Allarm.Maintenance_ON(DB3.DBX7.5). 단순 Coil이며 S/R 래치 아님.
- 0238 / LAD1931 / NID2: ON91에서 O56의 8개 입력으로 LOW_TC03_TEMP, Oxigen_Fault, Oxigen_Too_high, STANDBY_ON, MAX_MAX_TC09, HYDROGEN_BOX_FAULT, NOT R1 Gate ON, NOT RD01_Fbk. STANDBY Contact101 ORef72/RID11 W83→W102→O56.in4. O56.out W88→Coil66; ORef77 W90은 Local Disable_Load_RD01. 이 로컬 부하 억제와 RD01 주모터 전체 정지는 다르다.
- 대표 RD01 0243/NID7: ON 아래 Reset O28.in5는 NOT R2_GATE_LOOP_ON(Contact278) AND NOT STANDBY(Contact280) AND NOT UNDER TESTING(Contact35), W279/33/37. 이 OR의 다른 분기는 RD fault, INV, SET_PERC_FR01=0, NOT fan run. O28 W30→R236(M_RD01 ORef249 W265); M_RD01 Contact282→W283→Coil240(Start RD01 ORef251 W268). 따라서 대기/유지보수는 이 의존조건 분기에 영향을 주며 모든 고장을 우회하는 조건이 아니다.
- 대표 MC04 0247/NID11: NOT VS01 run Contact26→W28→NOT Allarm.Maintenance_ON Contact380→W29→O333.in3; 다른 OR 입력은 MC04_FAULT/INV. O333.out W360→R340(M_MC04). M_MC04 Contact377→W378→Coil344(Start MC04 ORef352 W365). 유지보수를 모든 장치 정지 허가로 읽을 수 없다.
- Main0549의 모터·필터·게이트·버너 호출 및 하위 Start→Q/Word 전달은 기존 설비별 원본 연결을 재사용한다. 이번 조사로 SYS-AUTO 고유 Q주소 또는 독립 전기단자를 발명하지 않는다.

### 3.5 자동 진행 후에도 영향을 주는 별도 쓰기·초기화
- 0169 / LAD1845 / NID11은 ON22→NOT Emergency23→Tipo=1 또는2(O29)→PreheatingControl_Enabled Contact55. **Auto_ON1 접점이 없는 별도 온도별 속도 갱신 분기**다. Real Ge/Lt 온도 구간→TON 58/63/68/72/76의 PT=T#10s→Q→Move60/65/70/74/78; SET_PERC_VT01에 각 HMI 속도 또는 최하 구간 15를 쓴다(W129/140/151/159/167). 0164/0165의 Move35와 복수 쓰기 관계. 실제 우선순위/현재 HMI 설정은 미확정. 모든 FN01 온도제어 기능을 새로 완료 처리하지 않는다.
- 0147 / startup LAD402/NID2의 DB2.DBW0/2/4/6/8/10/12/14←Int0 중 DBW6은 Auto/STANDBY/Maintenance 세 bit와 범위가 겹친다. bit Writer 목록만으로 모드가 보존된다고 결론내리지 않는다. 0048 Int0, 0562/0563 DB/Global absolute Word 선언, 0147 Move/Wire 참조. 전체 startup 호출/retention/현행 초기화는 미확정.
- 0149 startup auto flags와 0150 gate MEM defaults는 별도 설비 초기값 영역. 전체 하위 장치를 SYS-AUTO 완료로 합산하지 않는다.
- 0550 / Main NID11: ON419→W420→Move400/405.en. Data.Maint_code_0 ORef409 W414→in, out1 W415→Tag_189; Maint_code_3 ORef411 W416→in, out1 W417→Tag_190. 0692 Word Memory AO640/656=MW80/MW82. 모드 Bool과 유지보수 코드 Word가 다르다. 코드 bit 의미·코드 생성 논리 전체는 미해석이다.

## 4. 전기 전달 경로

SYS-AUTO는 software이므로 직접 명판·전원·릴레이·단자·케이블/FG가 비해당이다(INVENTORY 고유 electrical_fgs 없음). 경계는 DB/M 요청→개별 모터·게이트·버너 제어→개별 Q/Word 출력→그 설비 회로→피드백이다. 이 문서의 독립 검토는 대표 RD01/MC04의 요청/Reset 논리까지다.

기존 MC04 초안의 FG136/PDF137 Rev2 17.03.2025, PV01/02 초안의 출력·게이트 회로 및 BF01의 Word 전달은 연결 인덱스다. 이번에 그 PDF를 렌더·시각 검토했다고 주장하지 않으며 새 전기 끝점 사실을 추가하지 않았다. 하위 승인 시공도·실물 단자·케이블·현행 PLC와의 대응은 해당 설비 범위에 남긴다. 공유 도면 재검토가 없으므로 PDF 페이지/개정 신규 확정 건수는 0이다.

## 5. 알람·복구

- Emergency_module_fault는 자동 블록의 입력 조건이다. 그 발생 회로·물리 안전등급은 이 블록으로 입증되지 않는다. 0168 상승 에지→정지 타입5/Auto Set, 0166 OR Reset, 0164/65/69 NOT 억제를 각각 구분한다.
- 예열1/40 및 생산1/60에서 내부 RESET_ALLARM Set 요청. 모든 경보를 실제 해제하거나 안전하게 재기동했다는 증거가 아니다. ACK/원인 유지·개별 알람 재설정은 SYS-ALARM/설비 소유다.
- 0551 / LAD1626 / Main NID13은 ON451→RESET_ALLARM453→MAINTENANCE_PERIOD_LIMIT455→W456→R441(같은 Allarm ORef445 W450). 이는 해당 알람 Reset 경로만 증명한다. 발생 Set·유지보수 기한 산정·정비 완료 기록·현장 복구는 미확보다.
- Maintenance_ON 상태 Coil과 MAINTENANCE_PERIOD_LIMIT 경보를 합치지 않는다. 실제 정비/차단·재투입 권한/재기동 확인을 문서상 Reset으로 대체하지 않는다.

## 6. 증상별 관찰 계획

아래는 자료 수집·정적 비교 항목이며 현장 시험·강제 쓰기·보호값 변경 지시가 아니다. 실제 시각/시간대·프로젝트/CPU 식별·관찰자·원시/가공 주소·단위·동시 값이 필요하다.

|증상|관찰할 값·근거|먼저 구별할 것|복구 판단에 필요한 증거|
|---|---|---|---|
|자동 요청했으나 순서 시작 안 됨|HMI 이벤트 기록, DB2X7.3, DB1W98/96, ON, Emergency, 0024 호출|HMI 쓰기 미실행/호출 안 됨/상위 억제/초기화 덮어쓰기|승인된 요청 수신과 실제 하위 응답을 각각 확인|
|단계가 너무 빠르거나 정체|Tempo 연속 timestamp, OB 주기 설정·호출 횟수|1ms 제목과1s 호출자 상충; Int Eq 단계 건너뜀 가능성과 계측 주기|실측 호출 주기/프로젝트 일치 및 요청·응답 순서 기록|
|D37=-1 또는 preset 숫자|DB1W90, Tipo, Auto의 동시 기록|0163 NOT 분기; 표시값은 실제 운전피드백 아님|가공식과 화면 표시 이벤트의 결속|
|자동 종료 후 FN01 설정 변함|Tipo, PreheatingControl_Enabled, PID_Ref_Temp, 5개 TON.Q, VT01|0169에는 Auto 접점 없음; 단계 Move와 온도 Move 복수 쓰기|승인 설정자료·실제 쓰기 출처와 출력 피드백 비교|
|대기인데 RD01이 계속 요청됨|STANDBY, R2_GATE_LOOP_ON, M5.5, RD fault/INV/fan, M_RD01/Start|대기 부하 억제와 모터 정지는 다른 식|하위 회로·정지 기준·응답을 설비 담당 자료로 확인|
|유지보수에서 종속모터 반응 다름|DB2X7.5→M5.5/DB3X7.5, MC04의 VS01 run 등|유지보수는 특정 의존성 Reset을 바꾼다; 전체 fault bypass 아님|안전 차단·권한/하위 허가 기준과 현장 기록|
|비상 후 Auto가 다시 켜짐|Emergency 상승 에지, M90.5, Tipo=5, Tempo, Auto|0168의 정지 시퀀스용 Auto Set과 생산 재기동을 혼동하지 않음|물리 안전장치 복구·원인 해소·승인 재요청 별도|
|기한 경보 Reset 후 재발|MAINTENANCE_PERIOD_LIMIT, 내부 RESET, 코드MW80/82|Reset 경로만 확인, 발생·기한산정 미해석|정비 이력과 발생 소유 논리·재발원인 자료|

## 7. 완료·누락·검사 경계

- documentation: complete_with_gaps(배정 ID 원본 기반 7영역 초안). static_review: scoped_source_review. 원본 XML 정적 읽기·파싱·선언/핀 대조 및 선정 해시 검사만 수행했다.
- ui_records: not_run; publication: not_published; tia_compile/live_cpu/field_recovery: not_performed. 복원·전후비교·나란히보기·사용자 보고서/PDF 기능의 실제 저장/재열기/화면 동등성은 검증하지 않았다.
- 핵심 의미검토: 0024, 0162~0169, 0237, 0238, 0243, 0247, 0550, 0551의 본문 분기. 0147은 DBW6 겹침, 0149/0150/0549는 공유 경계만 확인했다. 이 19개 XML 추출 수는 19개 전체 제어 기능/모든 설비 의미검토 수가 아니다.
- 검색: decoded-original identifier XML의 이름/UID/RID/NID를 정적 파싱하고 network-map 및 HMI CSV를 검색했다. 식별자 파싱·검색 결과 수는 의미검토 건수가 아니다. 전체 프로그램·전체 모터/게이트·모든 쓰기·모든 호출의 완전한 실행 순서 분석은 수행하지 않았다.
- 미해석/필요자료: 현재 cyclic OB 설정(1s/1ms 충돌 해결), 실제 HMI 이벤트 및 보안/쓰기 권한, startup 호출·retention, 선택 타입3/4의 전체 사용/외부 쓰기 유무, 모든 Auto/HMI/Word writer 및 인터럽트 실행 우선순위, maintenance 코드 생성·기한 발생 로직, 타이머 ET 미결속 수신처, 현행 CPU·실물 대응·안전 재기동 기준.
- 명령/스크립트는 이 extracts 폴더의 자체 XML 추출·해시·문서검사용만 실행. 원본 build/test/generator, 시뮬레이터, PLC, 현장, 보호 설정, SEJIN 변경 0. 선정 source와 중지5자산은 고정 blob/기존 보존해시와 비교한다. 전체 원본 보존기록은 같은 고정입력의 UC01 preservation을 참조하며 전체를 의미검토했다고 주장하지 않는다.
- 다음 작업은 통합 담당의 고유핀 독립 검토 후 초안 전달이다. 현장 확인이 필요한 항목은 새 자료 확보 전 보류하며 같은 검색을 반복하지 않는다.

## 실제 작업 시각

- 시작/범위 확인: 2026-10-11 11:44:29 UTC
- XML 재추출 완료: 2026-10-11 11:46:57.779965 UTC (자체 단계 로그)
- 호출 주기 상충 및 표시 분기 부모 보고: 2026-10-11 11:46:12 UTC
- 본문 작성·해시·문서 검사 완료 시각은 아래 자동 기록에 기재한다. 추정 소요시간은 쓰지 않는다.

## 선정 원본 SHA256·Git blob 전체 목록

경로는 source-mv06 기준. 아래는 직접 선정된 원본/탐색자료/표준의 내용 일치 목록이며 파일 전체 의미검토 목록이 아니다.

|원본 상대경로|SHA256|고정 Git blob|내용 일치|
|---|---|---|---|
|`.agents/skills/gme-equipment-rollout/SKILL.md`|`fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b`|`9aa820ea6ca15b4e136c9772423b78ed4df6a3d4`|True|
|`AGENTS.md`|`0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2`|`073164bc6efd5791032d62c71b03b4dab48cb6f8`|True|
|`VERSION.json`|`5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7`|`fffb51663b7705aec91cb119ca80ee943a4ce758`|True|
|`all-in-one/sources/decoded-original/0024-FlgNet.xml`|`a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67`|`379ccbabf7692e1df137b99bab1992dea22cc1f0`|True|
|`all-in-one/sources/decoded-original/0040-IdentXmlPart.xml`|`4aa4f09101f827918ca2af003544aa0de8a70410cc4d69e738f2d6220669f182`|`dde9014e48da7a32dbb0cf9523dbdb6afcfd0bb3`|True|
|`all-in-one/sources/decoded-original/0047-IdentXmlPart.xml`|`2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e`|`3dc282f149a21fdf76d5521ef1c833be63b578b4`|True|
|`all-in-one/sources/decoded-original/0048-IdentXmlPart.xml`|`d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d`|`64fc5a7f1ad33f3b901b00f0d22d23578ffabff8`|True|
|`all-in-one/sources/decoded-original/0067-IdentXmlPart.xml`|`0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628`|`455f00638f1618f194b1c83d9c0c2f157663a902`|True|
|`all-in-one/sources/decoded-original/0068-IdentXmlPart.xml`|`0a71d492e69760390b99f71a75f02ef684e271554b003d5de8bf64a26c64eeba`|`abf1e8cf672afee026f7945219fcee8ad62c9787`|True|
|`all-in-one/sources/decoded-original/0147-FlgNet.xml`|`386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c`|`0027890eca158e714dd6260dc920a5d3aa83319b`|True|
|`all-in-one/sources/decoded-original/0149-FlgNet.xml`|`bc2519cdad49a7268006b194e8e5e1160744ff221f04b83e710f31f57bc617f9`|`836f61a06b35842d1bc00b4e60eeedafade43dcc`|True|
|`all-in-one/sources/decoded-original/0150-FlgNet.xml`|`829ca4aa3bd2bb6ee406f7f204add2987ec6159ef0fd6dd3dfc075592664a98e`|`b8130ae4a433018f7513d24bd8f0cf79a7897238`|True|
|`all-in-one/sources/decoded-original/0162-FlgNet.xml`|`892eab96a4f5c87cfafd35f8a2e2a04982a93ca23c777312101882e408b11deb`|`8b3887811075409309a0428bd49842dd9b6c1486`|True|
|`all-in-one/sources/decoded-original/0163-FlgNet.xml`|`b927f8c0bf35eb549a28a480bfc34d675e0bde20d3a00600ae700b2d310a1d34`|`edddc7af570335c9efc3ddf4182f9d4b0a286cf6`|True|
|`all-in-one/sources/decoded-original/0164-FlgNet.xml`|`15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491`|`1035a51ee3100d524da1b7b204ba142b6b509ac5`|True|
|`all-in-one/sources/decoded-original/0165-FlgNet.xml`|`4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88`|`8d636eb535060037ccf00ebdfb328b8775225fe4`|True|
|`all-in-one/sources/decoded-original/0166-FlgNet.xml`|`0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853`|`6b3062ae9ac2bc6ad8c2509d3fc4c15609a4b892`|True|
|`all-in-one/sources/decoded-original/0167-FlgNet.xml`|`112140ab4aee3509c9a1e887b97a9c5b00276809e0775c0d00d70ebacbb9160e`|`4b4d871ca7c57e13cea72543ce50cd9fb090d193`|True|
|`all-in-one/sources/decoded-original/0168-FlgNet.xml`|`6e69605abd053c1d85f668b8e29bf98975e7e6b9ec1903b017af2048602d4847`|`13262ff07cb094ffd38d9c00a5281c68f4c9ca2b`|True|
|`all-in-one/sources/decoded-original/0169-FlgNet.xml`|`c11893dfee800efa2649b14cd4bab9c94e018ce690168f060526c3249f50da10`|`9b3d8e50d69f96265e573fa1d4a124b7e59884be`|True|
|`all-in-one/sources/decoded-original/0237-FlgNet.xml`|`ad3721660c2f357e76c1a351f7898691271f35c341efe775e5780d749b2c4aa0`|`c97f914bb78760dd6fd42a46d3596983beb352f4`|True|
|`all-in-one/sources/decoded-original/0238-FlgNet.xml`|`8f6a5537084e092c352552dc469bbe8469b33412971219e51bba211ef607dfa8`|`c1093180555a6a00486d0a7268bb3a059b7cbf9e`|True|
|`all-in-one/sources/decoded-original/0243-FlgNet.xml`|`4b3a77029b4d5901ff40f260d54189748e7697bb6077fca502165fa7cd5ea3b5`|`53fff711852ac7ea3150a4cb51d83813d640210d`|True|
|`all-in-one/sources/decoded-original/0247-FlgNet.xml`|`104690938ac2ebe32d668f237255a3e957e0af9930bfc6587b9e6624bedf13a1`|`f7780f7eaaa297cd863fbebea4a56a567b231175`|True|
|`all-in-one/sources/decoded-original/0549-FlgNet.xml`|`49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1`|`985b5310b43b1015b5dee286aa0e42800564b94b`|True|
|`all-in-one/sources/decoded-original/0550-FlgNet.xml`|`ff691b4fa855e6b19bc68f19113a315cbc5da818196b6f2423a47d1650226918`|`1723621273575e9962b9f2f33f96d0949f617768`|True|
|`all-in-one/sources/decoded-original/0551-FlgNet.xml`|`c0a227e0cb72f33fd7149d3718f123d98a36354970e8d515cdf8bf7c95afb375`|`fb16f0ddb637a734c5adbde8c51c2edc246520f9`|True|
|`all-in-one/sources/decoded-original/0562-IdentXmlPart.xml`|`85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c`|`1609802542a3e560baba3f2b73c306be281dfb23`|True|
|`all-in-one/sources/decoded-original/0563-IdentXmlPart.xml`|`86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad`|`6a10fc694f896cda16409804daf2554c91635654`|True|
|`all-in-one/sources/decoded-original/0575-IdentXmlPart.xml`|`40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06`|`07d5d2548e8f36252a346d0b83341e27c3cb14ba`|True|
|`all-in-one/sources/decoded-original/0576-IdentXmlPart.xml`|`c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe`|`819b47160eaa6d08c212f71e5b5486ef5b55b6f2`|True|
|`all-in-one/sources/decoded-original/0577-IdentXmlPart.xml`|`511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47`|`a505ebf7efd05a85850dc29559a4f71242bacae3`|True|
|`all-in-one/sources/decoded-original/0578-IdentXmlPart.xml`|`0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b`|`070a79fb12139898dd44a17ab2061e795956b9c6`|True|
|`all-in-one/sources/decoded-original/0579-IdentXmlPart.xml`|`ee35cf525388f2b38399787caef57a978b0bb17216a90e1a90ac4391e0e799fe`|`19d1039319ffeb150767d96fc36205326483b1c4`|True|
|`all-in-one/sources/decoded-original/0580-IdentXmlPart.xml`|`fa748a6c1890f579d694fd5e561b2304f717da79e5352ca32152cc20e877c6ff`|`9bd503f23708fada1a1f871e0e52b0eb75e9aacf`|True|
|`all-in-one/sources/decoded-original/0602-IdentXmlPart.xml`|`46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf`|`bcb12ab1ce8c476ff921baa1608f29d9822f76b4`|True|
|`all-in-one/sources/decoded-original/0603-IdentXmlPart.xml`|`e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8`|`3a92b304baf4dbf6147e944d9778d2da11285cb1`|True|
|`all-in-one/sources/decoded-original/0604-IdentXmlPart.xml`|`b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af`|`bb2c318788b97e7a4924a176275c12d805aa519d`|True|
|`all-in-one/sources/decoded-original/0605-IdentXmlPart.xml`|`0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b`|`30e199288c147aa22d5ce8407178a391b89c6b1b`|True|
|`all-in-one/sources/decoded-original/0606-IdentXmlPart.xml`|`73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740`|`ced032fa747a8544abf17058ee5ebaa78ba9b23b`|True|
|`all-in-one/sources/decoded-original/0652-IdentXmlPart.xml`|`251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692`|`eee49f8301a6791748de9ab368159af8e8bc1585`|True|
|`all-in-one/sources/decoded-original/0688-IdentXmlPart.xml`|`ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda`|`463585759f1ecd94f32362b4fefb000a152f5773`|True|
|`all-in-one/sources/decoded-original/0690-IdentXmlPart.xml`|`fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541`|`36bd403f48ba8e364126837b19fb0419bbe78941`|True|
|`all-in-one/sources/decoded-original/0692-IdentXmlPart.xml`|`bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037`|`737785d03b5fad43c5b4d451955726d800edb1c0`|True|
|`all-in-one/sources/decoded-original/0694-IdentXmlPart.xml`|`757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d`|`c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d`|True|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|True|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|True|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|True|
|`docs/equipment-standard/WORK-ITEM-TEMPLATE.md`|`4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586`|`e546f39535d2b589e80f97db869ac37ce4d05cfd`|True|
|`docs/equipment-standard/WORK-STANDARD.md`|`05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99`|`f76a570cc73098632e08759b17934000f7e3a253`|True|
|`hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|True|

선정 파일 51개 전부 고정 blob 내용 일치. 별도 중지5자산 SHA256 기존 보존값 일치(실행하지 않음).

- 본문·선정 해시·자체 정적 문서검사: 2026-10-11T11:51:50.095838+00:00
