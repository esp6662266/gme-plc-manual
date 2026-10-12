# TC02 안전 온도 계측 원본 조사 초안

## 핵심 인계·상충·누락

- TC02는 TC01과 별도 ID다. OEM FG77/PDF78의 AB01 챔버 안전 온도 채널, +24Vdc / 4–20mA / 0–1300°C 표기는 확인했다. “SAFETY”라는 도면 제목만으로 안전등급·독립 안전차단기·현행 보호한계를 확정하지 않는다.
- 고유 환산은 0490(LAD1740,NID10): **PIW274 → FC63 → DB1.DBW108 Int**, 계수 DB4.DBW18, 영점 DB4.DBW16, 범위 출력 DB3.DBX21.3이다. HMI raw는 별도 **IW274 → DB13.DBW38 Word**이며 PIW와 IW, raw와 온도값을 합치지 않는다.
- TC01/TC02 비교 경보는 두 Int 온도와 공통 비교회로 소유다. ON·NOT M80.2·둘 중 하나 >400·차(TC01−TC02)가 −100 미만 또는100 초과·T116의 S5T#1M 경로를 갖는다. 400/100/1분은 고정 백업 명령이며 현장 안전 권장값이 아니다.
- MAX_TC01_TEMP / MAX_MAX_TC01_TEMP는 명칭만 보고 TC01 직접값으로 설명하면 안 된다. 0527 원본 비교 입력은 **DB39.DBD2 PID_Ref_Temp Real**이다. TC02가 선택/평균에 영향을 줄 수 있지만 TC02 전용 MAX 알람으로 복제하지 않는다.
- SCL 검색색인1719의 TC02-only 분기는 Temp_TC02를 선택하면서 후속 고장 처리에 **TC01_OFR → EnableTC01=false**라고 적혀 있다. 기존 AB01 조사와 같은 미확정 사항이며 신규 현장 오류로 단정하거나 TC02 문구로 고치지 않는다. 네이티브 SCL 본문·컴파일 listing 미확보.
- 전기 OEM X1:189/190/191과 시공p56의 HE01 구역 KX 케이블6_24를 무리하게 한 선로로 잇지 않는다. 변환기 위치·열전대형식·냉접점보상·현재 설치·승인 준공 대조가 누락됐다. 시공p56의6_7~6_10은 실제 렌더에서 검은 영역이며 숨은 텍스트를 유효 배선으로 되살리지 않았다.
- 공유 재사용: AB01 초안의 공통 호출·SCL 근거한계·버너 소유·공통 리셋, BF01/BF02의 FC63·startup Word쓰기 해석을 탐색 인덱스로 이용했다. TC02 고유 PIW/IW·CRef 핀·선언·비교경보·전기3쪽은 이번에 직접 재대조했다. 다른 TC 값/알람을 이름 치환하지 않았다.

작업3 자체 문서조사이며 로컬2차133 통합 제외를 유지한다. 현장 복구·TIA·현재 CPU·UI·기록·게시 완료가 아니다. 이 문서로 AB01/TC01/BR01/열전대 소자나 다른 하위 ID를 같이 완료로 집계하지 않는다.

## 1. 설비·자료 기준

- catalog TC02, sensor, 계측, parent 없음, depth0, phase2, priority 없음. INVENTORY.json catalog[13], 범위표 equipment[77], 별칭 tc_02. same-name TC01/03/04/05/06/07/09/10/11은 별개 ID다.
- 고정 읽기 원본 gme-research/source-mv06, Git abcf31c5030bc7ef8749ed8e869a857f2387a28a / v1.12.0. 원본 백업 GME_20250506.zap18; 백업·도면·시공자료 시점은 서로 다르다.
- root AGENTS, repository skill와source-map, WORK-STANDARD / WORK-ITEM-TEMPLATE / INVENTORY 및 버전·인계·게시·진행 최상단, BATCH07 지시·범위를 읽었다. 최신 부모 지시의5개 병렬 직접 조사 범위를 따르되 이 작업은 TC02만 담당했다.
- 실행 모델/추론 수준은 런타임 증명을 별도로 확보하지 못했다. 사용자 컴퓨터·로컬TIA 추가접근 없음. 새 Work/Codex/재위임 없음.
- 쓰기 범위는 drafts/TC02-DOTS-DRAFT.md와 extracts/TC02/뿐. 원본/코드/대장/버전/게시/운영기록 변경0, 시뮬레이터 작성·수정·생성·실행·행동시험0, PLC/현장/보호값/SEJIN 변경0. 저장소 generator/test/build 미실행.

### 7영역 적용

|영역|상태|근거와 경계|
|---|---|---|
|설비·자료 기준|적용|고유 TC02와 자료시점 확인, 실물 동일성 미확정|
|IO/HMI|적용·일부 미확보|PIW/IW/DB/형식/CSV 결속, 실제 이벤트·권한·온라인값 미확인|
|제어|적용·일부 미확보|TC02 환산/공통 선택/비교·호출, SCL 원형/스캔/간접쓰기 미확정|
|전기끝점|적용·일부 미확보|OEM 양끝과 시공KX 독립 확인, 현행 장치·보상·변환기 위치 누락|
|알람/복구|적용·일부 미확보|OFR와 비교 S/R·공통 선택온도/버너 경계, 실제 복구 미확인|
|증상관찰|적용·관찰설계|기록 항목·비교 위치 제안, 관찰·조치 수행 없음|
|완료/누락|적용|정적 자체대조와 미완료 영역 분리|

아래 네 자리 XML 번호는 all-in-one/sources/decoded-original/ 접두어다. 선언 번호는 -IdentXmlPart.xml, 회로 번호는 -FlgNet.xml을 뜻한다. LAD/document_id·NID·UID는 별개 식별자다. BO/AO는 bit offset이며 주소는 고정 백업 해석이다.

## 2. IO/HMI와 정확한 선언

|신호|선언·위치|형식/주소·방향|
|---|---|---|
|TC02 환산입력|0678 RID71 AO2192, SAD Input SAM=Peripherie; NID10 UID344|Global Int PIW274, 읽기|
|TC02 HMI raw|0627 RID62 AO2192, SAD Input SAM=None; NID2 UID58|Global Int IW274, 읽기|
|Inputs.TC_02|0629 RID66 BO304 BAD4;0628 DepDBBlock RID4 TOD13; NID2 UID59 Write|Global Word DB13.DBW38, raw 복사 쓰기|
|Data.Temp_TC02|0676 RID74 BO864 BAD11;0674 Data TOD1; NID10 UID347 Write|Global Int DB1.DBW108, 환산값|
|Coeff.COEFF_TC02 / ZERO_TC02|0676 RID72 BO144 /RID73 BO128, BAD8;0674 Coeff TOD4; UID345/346|Global Int DB4.DBW18 /16, 환산 시 읽기|
|Allarm.TC02_OFR|0676 RID375 BO171 BAD354;0674 Allarm TOD3; UID23 Write|Global Bool DB3.DBX21.3, FC 출력|
|Manage_TC1_2.EnableTC02|0650 RID76 AO1/BAD74;0648 DepDBBlock RID74 TOD39; NID9 UID3857 Write 및4127/3805/3728 Read|Global Bool DB39.DBX0.1; 선택상태/외부쓰기 미확정|
|Manage_TC1_2.PID_Ref_Temp|0650 RID91 /0684 RID169 AO16;0648/0682 TOD39|Global Real DB39.DBD2; 선택온도, raw Int와 다름|
|TC01-TC02control disable|0686 RID73 AO642, SAD Memory; NID8 UID782|Global Bool M80.2; 비교회로 반전접점|
|Allarm.TC01_TC02_COMP_FAULT|0684 RID81 AO73/BAD10;0682 Allarm TOD3; NID8 UID797/800 Write,799 Read|Global Bool DB3.DBX9.1; 비교 공동 래치|
|app02|0685 RID77 Local, AO32, NID8 UID789 Write /790/792 Read|Local Int 차 계산 임시값; 물리 입력 아님|
|Tag_108|0686 RID80 SAD Timer AO116 NID8 UID795 Write/796 Read|T116 PLC S5 Timer; HMI 태그가 아님|
|Flag.RESET_ALLARM|0684 RID24 AO48/BAD15;0682 Flag TOD2; UID798|Global Bool DB2.DBX6.0; 공통 요청|

### HMI 백업주소와 실제 표시의 경계

sources/hmi_plc_tags.csv는 dde.cfg에서 나온 주소설정이며 현재값/쓰기 이벤트 증명이 아니다. line은 헤더 포함 실제 CSV행이다.

|CSV행·태그/내부ID|주소|성격|
|---|---|---|
|200 data_DB1_DBW108 /002D3|DB1,INT108|TC02 환산 Int|
|222 Coeff_DB4_DBW16 /002BA|DB4,INT16|TC02 Zero|
|236 Coeff_DB4_DBW18 /002A5|DB4,INT18|TC02 Coeff|
|265 Allarmi_209 /0027F|DB3,X21.3|TC02_OFR와 동일주소|
|321 EnableTC02 /00239|DB39,X0.1|선택 비트|
|351 EnableTC01 /00211|DB39,X0.0|공유 선택 상대; TC02 고유 태그 아님|
|411 TC_PID_REF /001C0|DB39,REAL2|선택/평균 Real|
|531 Allarmi_74 /00143|DB3,X9.1|비교 공동 알람|
|732 I_TC_02 /00062|DB13,INT38|PLC 선언은 Word인 raw미러를 HMI가 INT로 설정|

명칭·주소 일치로 실제 화면 버튼/입력창·권한·쓰기 트리거·현재 단위·경보문구를 확정하지 않는다. 이 조사에서 HMI 실행·화면/기록 기능 검증은 하지 않았다.

## 3. 제어 구조와 다중쓰기

### 3.1 TC02 환산 고유 결속

0490 LAD1740 NID10 Contact355는 W349/ORef342(0678 RID1 ON)을 읽는다. W357 rail→355.in, W356 355.out→CRef336.en. CRef336 RefId351→0680 BlockInterfaceInfo RID351, CodeBlock348 RefId5→0672 FCBlock RID5/TOD63 Signal linearization을 직접 확인했다.

- W350 O343(ON)→336.IN0 Bool
- W351 O344(TC02 PIW274)→336.Analog_input Int
- W352 O345(COEFF_TC02)→336.Coeff Int
- W353 O346(ZERO_TC02)→336.Zero Int
- W354 336.OutValue→O347(Data.Temp_TC02 Int)
- W24 336.Out_of_range→O23(Allarm.TC02_OFR Bool)

ON은 M0.0의 이름이며 현재 참을 가정하지 않는다. EN과 IN0는 별도 핀이다. FC 호출 안 됨과 IN0 false는 같은 동작으로 처리하지 않는다.

FC63 공통본0291 LAD1658 NID1과0014 LAD1659 NID2는 공유 근거를 이용하고 원본 타입·고유 호출 결속을 재대조했다. 0291은 IN0 Contact255 하에서 Analog_input >−1382(Gt258) AND <=32767(Le161)일 때 Int→DInt Convert164/167, DInt Add170(Analog+Zero), Convert174(Coeff), DInt Mul177, DInt Div181(/28000), Move185→OutValue 순서다. W227/230/234/237/241/245는 ENO 연쇄다. Real 계산·일반 반올림·0–1300 단순비례로 바꾸지 않는다.

범위 가지 Gt190 >32767 OR Le259 <=−1382→OR47→Move193(−9999)→OutValue. **OFR Coil23은 Move193.eno(W21)**를 받으며 값(out1 W253)과 다르다. 오류상수와 단선/모든 하드웨어진단/TC소자 고장을 등치하지 않는다. Int에서 >32767 조건의 실제 도달성·변환 overflow·온라인 진단은 미확정이다.0014 NOT IN0(Contact171)→Move162 상수0→OutValue. 이 가지에서 OFR를 별도 Reset한다고 덧붙이지 않는다. 공통 선언0611/0612의 Local/상수/입출력형식을 참고하며 추출표의 RID만 같은 타블록 후보를 자동 채택하지 않는다.

### 3.2 raw HMI 미러와 호출

0398 LAD1071 NID2 Move51.in은 W70/O58→IW274, out1은 W71/O59→DB13.DBW38이다. Move51.en은 W68의 Move50.eno를 받는다. 전 단계 TC01의 ENO와 raw복사 형식 때문에 이 값을 환산 온도로 표시하거나 독립 무조건 주기 갱신으로 쓰지 않는다.

main0030 LAD1613: Recipes Handler→HMI→HMI Output ENO연쇄 뒤 NOT Simulation(1) Contact37/W44/O45→CRef28 HMI Inputs.en(W43). main0031 LAD1619 NID6: ON Contact282/W280 O271→W283에서 CRef261 Analog input conversion과264/267/270 Allarms1/2/3에 각각 en 분기. 앞 호출의 ENO 연쇄로 만들지 않는다. 0549 LAD1620의 ON350→W351은 Burner control CRef328에도 분기된다. 이 호출·주소 근거는0692/0694 선언과 공통 AB01 근거에 연결한다. 실제 스캔주기·OB우선순위·현재 CPU 일치는 미확정이다.

0635 RID292에는 Data.Temp_TC02의 기존 simulation NID14 UID76 Write가 별도로 있다. 이번에는 선언만 읽어 다른 쓰기 가능성을 보존했으며 해당 자산 실행/행동시험은 하지 않았다. 환산 출력이 항상 최종값이라 단정하지 않는다. HMI/통신·간접쓰기까지 전수 증명한 것은 아니다.

### 3.3 공통 선택온도, TC02-only 원문 이상과 한계

live_index.json segment _7ev i1719의 SCL Code는 검색색인 문자 근거다. 0650·0648 네이티브 선언이 관련 읽기/쓰기를 뒷받침하지만 SCL 원형 전체·연산 승격·실행순서·현행 적용을 증명하지 않는다.

- 두 Enable이 참이고 두 OFR가 거짓이면 PID_Ref_Temp := (Temp_TC01+Temp_TC02)/2라는 문자다.
- 두 Enable 안의 OFR분기는 TC01_OFR 우선 elsif 뒤 TC02_OFR이며 해당 Enable을 false로 쓴다. 그 분기에는 PID_Ref_Temp 대입이 없다. 두 OFR 동시 상태의 검증을 발명하지 않는다.
- TC02만 선택이면 PID_Ref_Temp := Temp_TC02, EmergencyStop := false지만 후속 문자는 if TC01_OFR then EnableTC01 := false다. 원문 그대로 남긴다.
- 아무 채널도 선택되지 않으면 EmergencyStop := true, 마지막에 Allarm.EmergencyStopTC1_2로 전달한다.

1274의 true/true/0.0/false는 백업 인터페이스 저장값이며 현재 Enable·보호설정을 나타내지 않는다. TC02 선택 버튼을 조작하거나 계수·선택·보호값 변경을 제안하지 않는다.

## 4. 전기 전달 경로와 실제 PDF

세 페이지는 이번 TC02 작업에서 실제 렌더하여 시각 검토했다. FG와 PDF를 각각 적었으며 렌더는 extracts/TC02/render에 있다.

### 4.1 OEM Electrical_Rev2.pdf FG77 / 실제PDF78

제목 THERMOCOUPLE, TC02 부분 SAFETY TEMPERATURE CONTROL CHAMBER AB-01. footer DATA27.05.2024 / FG77 / TOT262 / 별도 개정란 공란이다. 파일명 Rev2를 모든 시트 개정으로 대신하지 않는다.

전원 +24Vdc10.7(좌76/9→우78/0)→X1:189의 5×20 50mA F→선77.2→TC02 +5. TC02 −6→X1:190→+PEW274 /106/3. 차폐 X1:191→77SCH2 /106/3. 센서 도형은 OUTPUT4–20mA, 0/1300°C라고 적혀 있다. 이 +5/−6은 출력루프 단자 표기이며 열전대 소자 자체의 보상케이블 단자와 합치지 않는다. 차폐를 신호−나 전원0V로 임의 배선하지 않는다.

### 4.2 OEM FG106 / 실제PDF107

제목 ANALOG INPUT MODULE, footer DATA27.05.2024 / FG106 / TOT262 / 개정란 공란. CPU515 MOD3 표기이고 TC02 PEW274는 채널1 **I1+ 단자6**, 귀로 **U1−/I1− 단자8**, 공통 −0Vdc10.6 및 MANA18이 도면상 연결된다. 77SCH2는 차폐 도형, +PEW274는 단자6으로 내려오며 두 참조는77/5다. FG77의106/3와 상호참조 위치를 그대로 보존한다.

모듈의 정확한 현행 주문번호/설정·채널 진단·활선상태는 미확인이다. 도면 CPU515 표기를 현재 CPU 모델 증명으로 사용하지 않는다.

### 4.3 시공 Electrical_Can_Decoating_20241118.pdf 실제PDF56

도번 CANDC-CONS-C006-056, 제목 CABLE SCHEDULE(5), D-PAGE6 / TOTAL56/64. footer Rev1 /24.11.11 /first draft design, CHECKED·APPROVED 공란을 실제 렌더로 확인했다.

가시적인6_24 행: =FLA+HE01-TC02A, FROM CR→TO HE-01 / TC-02, current type TC, KX /2S /1.0 /spare0, route100 LCD1→E600, Adjustment10 /LEN50. 단위를 새로 붙이지 않는다. OEM의 AB01 기능명과 시공 HE01 구역을 동일실물 위치 또는 부모 변경 근거로 단정하지 않는다. KX 문자만으로 현행 센서 Type K·보상/접속·극성/허용온도를 확정하지 않는다.

6_7~6_10은 렌더에서 검게 가려져 있다. 텍스트층에 나온6_8 등의 문자열을 현행 유효 케이블 근거로 채택하지 않았다. OEM4–20mA 출력루프와 시공KX 열전대 구간 사이의 실제 변환기/접속함 위치·단자 연결은 확보 전이다.

## 5. 알람·복구·직접제어 소유

### 5.1 TC02_OFR

0490 CRef336.Out_of_range→DB3.X21.3는 TC02 고유 출력이다. 공유 FC63의 ENO/−9999 및 IN0 경계를 §3.1대로 적용한다. TC02_OFR 자체를 비교경보 DB3.X9.1 또는 MAX_TC01/MAXMAX와 혼동하지 않는다. 본 검토의 TC02_OFR 쓰기는0676 NID10 UID23이다. 선언/범위검색에서 확인한 결과이며 온라인 외부쓰기 배제 증명은 아니다.

### 5.2 TC01/TC02 비교경보 0534 LAD1986 NID8

- Contact832=ON(W801/O781), Contact834=**NOT** M80.2(W802/O782), W835→Gt745/748.pre.
- Gt745 TC01>400(W803/804), Gt748 TC02>400(W806/807)→OR744.in1/2(W805/808). “둘 다400 초과”가 아니다.
- W809 OR744.out은 Sub754.en과 Lt761/Gt764.pre로 분기. W810 TC01−W811 TC02→W812 Local app02.
- Lt761 app02<−100(W813/814), Gt764 app02>100(W816/817)→OR760(W815/818). ±100과 정확히 같은 경계는 이 두 비교의 참 조건이 아니다.
- W819 OR760.out→SdCoil770.in와Contact836.in, W820 상수 S5T#1M→770.value, W821 Tag_108 T116→770.operand; Contact836가 T116을 읽고 W837→SCoil775, W824/O797→DB3.X9.1 Set.
- 별도 ON후 Contact838 RESET_ALLARM(W827/O798)→Contact840 같은 래치(W828/O799)→W841 RCoil780, W830/O800 Reset. 온도차 정상화 허가가 이 Reset 가지에 추가되어 있지 않다. 원인 지속이면 조건에 따라 재발 가능하며 자동 현장복구·버너재시작을 보증하지 않는다.

0683 상수 RID74=400 Int, RID140=−100 Int(원문 SV와 부호 보존), RID125=100 Int, RID46=S5T#1M;0685 RID77 Local Int;0686 RID80 T116을 각 NID8/UID로 대조했다. 온도값의 실제°C 교정/현재 설정은 도면과 별도이다.

0148 startup의 DB3.DBW8 쓰기(0563 RID32 AO64 Word/BAD23,0562 Allarm TOD3; NID3 UID294, Move267.out1/W316)는 DB3.X9.1을 포함한다. 공통 startup의 Word zero 경로를 BF01/BF02의 같은 고정원본 근거와 연결하며, 비교 S/R만 유일한 쓰기라고 표시하지 않는다. OFR byte21.3을 이 Word8 범위에 넣지 않는다. 0148의 map NID 미추론은 선언 NID3과 구별한다.

### 5.3 선택온도 알람과 버너는 관련 소유

0527 LAD1979 NID1은 0684 RID169 DB39.DBD2 Real을 O210/220/227/229/231로 읽는다. Gt149/W241 입력, Lt169/W256 입력, Gt186/W265·Gt189/W268·Lt192/W271 입력 모두 선택온도다. MAX/MAXMAX의 타이머/상수/설정은 이 공통 회로 소유이며 본 초안에 TC02 전용 설정으로 복제하지 않는다.

0175 LAD1858 NID5에서 비교경보 O245/RID40→Contact297(W263)→OR219.in8(W298), EmergencyStopTC1_2 O23→Contact22→OR219.in12; OR219.out W267→ON305→OR213.in5→RCoil232 Flag.Start_Burner(W272/O250)라는 GME 버너 요청 해제 경로를 확인했다. 비교경보가 곧 가스 밸브/화염/현장안전 차단기의 직접 출력은 아니다. 실제 Q6.5와 외부010-390 전용반, 가스/공기·점화·퍼지·내부 복구는 BR01 조사 소유로 연결하며 TC02 소유로 편입하지 않는다.

공통 HMI reset 요청0158과 자동해제0154는 기존 AB01 원본 조사 연결을 재사용한다. 이 작업에서는 실제 HMI 이벤트·버너반 리셋·현재 보호회로를 시험하지 않았다. 래치해제, 선택온도 정상화, 새 요청, PLC출력, 외부 응답, 실제 공정복구는 각각 확인해야 한다.

## 6. 증상별 관찰 설계

관찰은 승인된 안전절차와 적격 작업자가 수행할 후속 기록이다. 이 조사에서 실제 계측/조작/조치/복구는 없었다. 기록은 관찰자·시각/시간대·프로젝트/CPU 식별·위치·값/단위·근거·배제결과·조치·복구증거로 구분한다. 계수변경·강제입출력·보호우회·반복리셋은 제안하지 않는다.

|증상|같은 시각에 기록할 항목|비교 및 미확정|
|---|---|---|
|TC02 표시가 −9999/고정값|PIW274, ON/FC호출, ZERO/COEFF, DB1W108, OFR, 채널진단|0490/0291 ENO·범위·다른쓰기와 비교; 표시만으로 센서교체 판정 금지|
|raw와 온도 표시가 다름|IW274/PIW274, DB13W38, DB1W108, HMI 주소/갱신시각|서로 다른 접근·raw/환산·Word/INT이므로 수치 동일 기대 금지|
|두 온도 차가 큰데 비교경보 없음|M0.0/M80.2, 두 Temp, app02, T116, X9.1, RESET|0534 >400 OR와 엄격부등호·지연·현재 Reset 조건을 확인; 고장입력 OFR와 별개|
|Reset 뒤 경보 재발/버너요청 꺼짐|X9.1, Reset, T116, Enable1/2, PIDref, EmergencyStop, Flag.Start_Burner|래치 해제와 원인 해소/버너 직접출력 소유 분리|
|TC02-only 선택온도가 예상과 다름|EnableTC01/02, 두 OFR, 두 Temp, PIDref와 현재 프로그램 원형|SCL1719 TC01_OFR 문구 그대로 비교; 현장 프로그램 오류·자동변경 단정 금지|
|센서배선/위치 확인 불가|명판·변환기·접속함·X1 189/190/191·MOD3 6/8·케이블6_24 사진/승인도|OEM4–20mA와KX 구간 접속 증거 확보 전 임의연결/단자 대체 금지|

## 7. 완료·누락·다음 인계

|상태|결과|
|---|---|
|documentation|complete_with_gaps /TC02 자체 초안|
|static_review|고유 원본 자체 핀/선언/PDF 및 해시대조; 독립 검토 대기|
|ui_records|not_run; 도면/래더 비교·선택복원·전후기록·보고서/PDF 네 기능 구현/실행 미검증|
|publication|not_published; 원본/버전/대장/게시 변경 없음|
|tia_compile /live_cpu /field_recovery|모두 not_performed|

원본 UI/기록키·note/repair_observation·미지필드·기존초안·0/빈칸·운영사진을 수정/복제하지 않았다. BC01 동등 기능구현 완료라고 세지 않는다. 해시 파일수는 의미검토수와 다르며 §2~5에 명시한 경로만 검토했다. 0398/0527/0175 등은 TC02 관련 경계만 검토했고 전체 설비 기능 검토 수로 세지 않는다.

미확보: 현행센서/변환기 제조사·모델·열전대형식·보상/교정, 승인준공 도면·KX↔4–20mA 인터페이스, 네이티브 SCL원형/compile listing·TC02-only 실제로직, 현재 CPU·설정·보호값·정상극성, HMI실제이벤트·화면단위·권한·갱신, 안전회로/버너전용반/현장복구. 새 현장자료 없이 같은 보류를 반복조사하지 않는다.

다음 한 작업: 부모 독립 검토자가0490 고유핀·0534 비교/Reset·SCL1719 증거수준·FG77/106 및 시공56 상충을 원본과 대조하고, 문서 수용 여부만 판정한다. 로컬통합/게시/TIA/현장작업 권한은 이 인계에서 추가하지 않는다.

## 부록 A. 추출·검사와 실제 단계시각

extracts/TC02에는 선언 스냅샷, TC02고유 선언, 선택XML의 refs/wires/network-evidence, HMI행, 선택SCL색인, 겹치는알람쓰기, PDF렌더, source-hashes/static-review/stage-times JSON이 있다. 선언 전수 탐색은 의미검토 전수완료가 아니다. 자체파서는 원본을 읽기만 했다. 저장소 preflight/generator/test/build는 실행하지 않았다. 자체검사 첫 실행은 버너 OR입력 선을 W263으로 잘못 지정한 검사 작성 오류를 검출했다. 원본에서 W263은 Contact297.operand이고 실제 OR219.in8 연결은 W298임을 재대조하여 검사만 수정한 후 재실행했다. 원본/알람 논리는 변경하지 않았다.

- 착수/배정 수신:2026-10-11 10:52:41 UTC.
- FG77 실제 렌더 확인:10:53:42 UTC까지 완료.
- FG106·시공56 실제 렌더 확인:10:54:43 UTC까지 완료.
- 이후 검증·초안 완료 시각은 아래 검사 스크립트가 실제 시계로 추가한다. 소요시간을 추정해 만들지 않는다.

## 부록 B. 원본 SHA256와 고정 Git blob 바이트 일치


실제 자체검증 종료:2026-10-11T11:01:20.032671+00:00. 선택 원본/맥락/보존 71개 SHA256와 고정 Git blob 바이트가 모두 일치했다. 중지5자산은 해시보존만 확인했다. 시작·종료 원본 Git 변경0. 위11개XML은 추출 수이며 의미검토 전수완료 수가 아니다.

|원본 경로|SHA256|고정Git blob OID|바이트일치|
|---|---|---|---|
|`.agents/skills/gme-equipment-rollout/SKILL.md`|`fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b`|`9aa820ea6ca15b4e136c9772423b78ed4df6a3d4`|true|
|`.agents/skills/gme-equipment-rollout/references/source-map.md`|`40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc`|`49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3`|true|
|`AGENTS.md`|`0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2`|`073164bc6efd5791032d62c71b03b4dab48cb6f8`|true|
|`EXPANSION-WORK.md`|`ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2`|`4c42d88ecc2d48269eb23e13a20ebf3721a092a1`|true|
|`PUBLICATION_STATUS.md`|`efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740`|`d76401cf291fc0be681acc51fa898ad3ce46ff78`|true|
|`VERSION.json`|`5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7`|`fffb51663b7705aec91cb119ca80ee943a4ce758`|true|
|`WORKSPACE-HANDOFF.md`|`215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074`|`dd0b8989d2376c4415bba9bd826fe6754c6b1a12`|true|
|`all-in-one/ACTIVE-WORK.md`|`eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2`|`6eb947c629b5ddf9c759ef87649451303938864b`|true|
|`all-in-one/assets/program-model-data.js`|`52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f`|`38f34b0caa380a16ccad6f6f1e234a2fdf23f327`|true|
|`all-in-one/assets/simulator-workspace.js`|`3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc`|`97c2c831c77a9699fff0e0960b3bc1b7d93d45b3`|true|
|`all-in-one/assets/virtual-plc.js`|`5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc`|`0bd9eceb54365a91214a37c5601b5067c39a3f75`|true|
|`all-in-one/registers/equipment.json`|`7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa`|`acc42633033398216469064932c4b76987371606`|true|
|`all-in-one/registers/program-model.json`|`6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5`|`9860b10f008d3a5ae714be50d77b703dfec32f3a`|true|
|`all-in-one/registers/simulator-freeze.json`|`bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835`|`808ffac14dbd1b4a7d797fa6cd0d647635d90b47`|true|
|`all-in-one/registers/virtual-plc-test-results.json`|`a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64`|`757dd50e45184568facb8ff62900b39d3ce848d1`|true|
|`all-in-one/sources/Electrical_Can_Decoating_20241118.pdf`|`3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd`|`0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8`|true|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|true|
|`all-in-one/sources/GME_20250506.zap18`|`00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8`|`211c4f604627a32f82a1124c2a9872c2fcf00865`|true|
|`all-in-one/sources/PEData.plf`|`647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a`|`65605ff8910f920109da731604aa5dc8d83fc956`|true|
|`all-in-one/sources/decoded-original/0014-FlgNet.xml`|`2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30`|`4d164b074fcc13a8f97da9e24382cc169ef29555`|true|
|`all-in-one/sources/decoded-original/0030-FlgNet.xml`|`9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b`|`e74c70b751acdcdbc7a8b3b0c98aa773c2107cab`|true|
|`all-in-one/sources/decoded-original/0031-FlgNet.xml`|`76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65`|`653d27572de6beedcf3eb6c95702bb119a8b567f`|true|
|`all-in-one/sources/decoded-original/0047-IdentXmlPart.xml`|`2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e`|`3dc282f149a21fdf76d5521ef1c833be63b578b4`|true|
|`all-in-one/sources/decoded-original/0048-IdentXmlPart.xml`|`d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d`|`64fc5a7f1ad33f3b901b00f0d22d23578ffabff8`|true|
|`all-in-one/sources/decoded-original/0056-IdentXmlPart.xml`|`c5ec45cd232c36d80f80487ec0dd284a876e326ba2286fc722ecc861a400232a`|`1364306d64caf1f1f094c98dc163edf69cdc1afc`|true|
|`all-in-one/sources/decoded-original/0057-IdentXmlPart.xml`|`1124275ab34e188b042b263d3c4b744abf5637ffd229af642b81a27f00a00c6b`|`264d24445f42cf32706bc6942863f9f227eb797e`|true|
|`all-in-one/sources/decoded-original/0064-IdentXmlPart.xml`|`ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d`|`300d74239868f4f4595d4d5bbb848b4b58bbae76`|true|
|`all-in-one/sources/decoded-original/0148-FlgNet.xml`|`1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313`|`3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3`|true|
|`all-in-one/sources/decoded-original/0154-FlgNet.xml`|`b0a163ffa382b722eaa34df4bdc4c3dd06039b296b791d26d68639a7b0502746`|`ce5ea87daabd1c234cd5b94dd1a3465d878f658b`|true|
|`all-in-one/sources/decoded-original/0158-FlgNet.xml`|`d3f3adebc3d990b85c5d4c294906ae3bc3dafebb49d25b030bf9cc2ccf905651`|`233ccf8f9d82ffffa498e04cbdcd3de07115c1db`|true|
|`all-in-one/sources/decoded-original/0175-FlgNet.xml`|`41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97`|`1626da00b3bbcb46f77720271ecf0f50db9dc63b`|true|
|`all-in-one/sources/decoded-original/0291-FlgNet.xml`|`fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550`|`1418fb2ed172c6df694a5eb8bf2dffd0b177653b`|true|
|`all-in-one/sources/decoded-original/0398-FlgNet.xml`|`4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747`|`67ebb54daa55093487ea7e780f23ae2cf193c397`|true|
|`all-in-one/sources/decoded-original/0490-FlgNet.xml`|`8c3423f973afdf6356c1fdf0d303203c9561ddc197b3566da5e6cbc25b737655`|`cdbb733e28e1e2f244ff53292290d14008f0bb00`|true|
|`all-in-one/sources/decoded-original/0527-FlgNet.xml`|`a91f3876643dbdb796d24833a5d67301ff72a3e41365e52f12ec4509b0f41196`|`ad2aadea551d949ce36aeadcd2ff2cfc0317e4f2`|true|
|`all-in-one/sources/decoded-original/0534-FlgNet.xml`|`f46e2d9c9dbe465d1068ecf0cc52909e0f8a2691347b533028a908937461a611`|`625186661512560db08e09d8d41ae2455cde59dc`|true|
|`all-in-one/sources/decoded-original/0549-FlgNet.xml`|`49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1`|`985b5310b43b1015b5dee286aa0e42800564b94b`|true|
|`all-in-one/sources/decoded-original/0562-IdentXmlPart.xml`|`85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c`|`1609802542a3e560baba3f2b73c306be281dfb23`|true|
|`all-in-one/sources/decoded-original/0563-IdentXmlPart.xml`|`86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad`|`6a10fc694f896cda16409804daf2554c91635654`|true|
|`all-in-one/sources/decoded-original/0564-IdentXmlPart.xml`|`2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1`|`c4b1f2cb191970cfce1cce59cb290a9f1f934c37`|true|
|`all-in-one/sources/decoded-original/0565-IdentXmlPart.xml`|`0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149`|`c2e3e2d57c94c5da864f6e172f0a7a925da942d6`|true|
|`all-in-one/sources/decoded-original/0566-IdentXmlPart.xml`|`a1914c7ae085acc1f949a649979824bec8b46fcd78a8055318272a1eb5a45265`|`348e6fccf44a8497f58f73e89ec98e892b2df436`|true|
|`all-in-one/sources/decoded-original/0582-IdentXmlPart.xml`|`41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951`|`82636dec064876d0f4cc714ef385b07d6e05efe0`|true|
|`all-in-one/sources/decoded-original/0585-IdentXmlPart.xml`|`e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184`|`16574d37ef3ca61b59ba396c400e269ab1dd3440`|true|
|`all-in-one/sources/decoded-original/0611-IdentXmlPart.xml`|`0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089`|`bad6b16fb32a32d47d882f48754994887457872b`|true|
|`all-in-one/sources/decoded-original/0612-IdentXmlPart.xml`|`95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38`|`7cc782d33d07ef225c2104f3e7c9fbd31f7c7467`|true|
|`all-in-one/sources/decoded-original/0627-IdentXmlPart.xml`|`08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb`|`61ebc0abbb2ca160e11e1da400a3f14a397d8bc5`|true|
|`all-in-one/sources/decoded-original/0628-IdentXmlPart.xml`|`9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd`|`170ca5c72599edc7ea7eefe651c3680ce325e76a`|true|
|`all-in-one/sources/decoded-original/0629-IdentXmlPart.xml`|`67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972`|`058129bb01e27f7a6a0d0293f332d745e5bab74e`|true|
|`all-in-one/sources/decoded-original/0635-IdentXmlPart.xml`|`1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457`|`95bfcad59cfb0c12b573e9e8face4262d1e94622`|true|
|`all-in-one/sources/decoded-original/0648-IdentXmlPart.xml`|`afaa47ae737d9333fe831ffac2b1d1388f108bb6a2b23d03554fa862f7edb454`|`3dd5101419fbe16bbce7814398209efd6508db82`|true|
|`all-in-one/sources/decoded-original/0650-IdentXmlPart.xml`|`86f53657eb7afb0798da0e215ba226721076c2ab1b25b74eb83e7b3c4b2d8a2d`|`a3d80a76ef5b0d00009c0fc9a1fdeb1471d0b67b`|true|
|`all-in-one/sources/decoded-original/0672-IdentXmlPart.xml`|`6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222`|`2f2790dab4bb2357733112220e0acc41edb6feb6`|true|
|`all-in-one/sources/decoded-original/0674-IdentXmlPart.xml`|`4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84`|`f210593944547b63eab10c667348711413600aab`|true|
|`all-in-one/sources/decoded-original/0676-IdentXmlPart.xml`|`c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59`|`1ed67265f69796a4e659f9438e551068037f33a4`|true|
|`all-in-one/sources/decoded-original/0678-IdentXmlPart.xml`|`51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382`|`7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc`|true|
|`all-in-one/sources/decoded-original/0680-IdentXmlPart.xml`|`fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95`|`c9049ced1eaed72c5e251a88601d46ddec8c3e50`|true|
|`all-in-one/sources/decoded-original/0682-IdentXmlPart.xml`|`25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092`|`61182411e912941161eccf4e90c1f174e5379f0a`|true|
|`all-in-one/sources/decoded-original/0683-IdentXmlPart.xml`|`0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22`|`662acdb9a06c0ba1c0027e7dd215a28f07d3f02b`|true|
|`all-in-one/sources/decoded-original/0684-IdentXmlPart.xml`|`6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208`|`d67b98b5d5516e0330aae5cfdbee41a3e09206e1`|true|
|`all-in-one/sources/decoded-original/0685-IdentXmlPart.xml`|`2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448`|`86bda988d9efedba92ba2f3e4877497d9eb5230a`|true|
|`all-in-one/sources/decoded-original/0686-IdentXmlPart.xml`|`b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4`|`8c152d926692a8e15973c980e08e338d29411814`|true|
|`all-in-one/sources/decoded-original/0692-IdentXmlPart.xml`|`bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037`|`737785d03b5fad43c5b4d451955726d800edb1c0`|true|
|`all-in-one/sources/decoded-original/0694-IdentXmlPart.xml`|`757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d`|`c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d`|true|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|true|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|true|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|true|
|`all-in-one/sources/source-manifest.json`|`5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf`|`38cf407491d52dc6128cf94ca8a4bddee350de6d`|true|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|true|
|`docs/equipment-standard/WORK-ITEM-TEMPLATE.md`|`4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586`|`e546f39535d2b589e80f97db869ac37ce4d05cfd`|true|
|`docs/equipment-standard/WORK-STANDARD.md`|`05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99`|`f76a570cc73098632e08759b17934000f7e3a253`|true|
