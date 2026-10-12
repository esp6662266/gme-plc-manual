# TC01 온도 계측 — 원본 조사 7영역 초안

## 핵심 확인·인계

- 고유 catalog TC01 한 개의 문서 조사. TC02·TC03·AB01·BR01을 함께 완료로 세지 않는다. 현행 CPU·설치·정상 극성·보호 설정·현장 복구는 미확정이다.
- TC01 원시 입력은 Int `%IW272`. 0489 환산 호출은 `SAM=Peripherie` (`%IW272:P`), 0398 HMI 미러는 `SAM=None`. `Inputs.TC_01` DB13.DBW36, `Data.Temp_TC01` DB1.DBW110, `Manage_TC1_2.PID_Ref_Temp` DB39.DBD2는 서로 다른 관찰점이다.
- 0489 호출 EN과 IN0는 모두 ON `%M0.0`이다. 실제 ON 값·호출 실행은 미확인. 공통 선형화는 Int→DInt 후 `(raw+zero)*coeff/28000`; Real 온도계산으로 바꾸지 않는다. OFR은 -9999 Move의 ENO 출력이다.
- **이름 MAX_TC01_TEMP/MAX_MAX_TC01_TEMP여도 0527 실제 비교 입력은 DB39의 선택된 PID_Ref_Temp(Real)**다. TC01 직접값만 비교한다고 설명하지 않는다. 6초 SdCoil, MAX 해제의 -5 및 MAXMAX의 +20/1250.0/-60.0는 백업 상수이며 현장 안전값이 아니다.
- TC01/02 비교 고장은 별도 0534: ON·NOT disable·(TC01>400 OR TC02>400)·차이<-100 OR >100·S5T#1M 경로. disable는 `%M80.2`; TC01 OFR DB3.DBX21.2와 비교 고장 DB3.DBX9.1을 혼동하지 않는다.
- 원본의 0412/LAD1092에는 DB1.DBW110의 별도 Writer가 있다. 기존 simulation 블록의 **읽기 전용 정적 원본 조사**만 했다. 생성·수정·실행·행동시험 0. 활성 여부·실제 최종값은 미확정.
- 선택기 SCL 검색 색인 doc1719는 두 채널 평균/한 채널 선택을 서술하지만, TC02-only 가지에도 `TC01_OFR → EnableTC01 := false`가 적혀 있다. 임의로 TC02로 고치지 않는다. 선언 0650 NID9와 구분하고 실제 SCL 원본·컴파일·CPU에서 검증할 누락으로 남긴다.

### 상충·누락·공유근거

|구분|내용|처리|
|---|---|---|
|도면 상충|OEM FG77/106 TC01 설명은 AB-01 챔버, 시공 p56 6_23 목적지는 HE-01 TC-01|같은 실물로 확정하거나 위치를 수정하지 않음|
|신호방식 경계|OEM 송신기 출력 4–20mA·0/1300°C, 시공 케이블은 TC/KX 2S|KX 표기로 실제 프로브 타입·송신기 위치·보상방식 확정 금지|
|선택기 의문|doc1719 TC02-only 가지의 TC01_OFR/EnableTC01 표기|색인 그대로 보존, 원본 SCL·현재 프로젝트 추가자료 필요|
|자료형 경계|0527 비교 SrcType=Real인데 설정 TC01_MAX_ALL 및 지역 app00/max_max_tc1은 Int|암묵 변환/실행 결과를 정적 연결만으로 확정하지 않음|
|공유 재사용|BF01/RO01/AB01의 공통 0291/0014 선형화와 AB01의 온도 경보 색인|같은 고정 입력의 탐색 인덱스로 재사용; TC01 호출·선언·경보 고유 핀 독립 재확인|
|누락|현재 계수/제로/한계/Enable/disable/호출 상태·교정·명판·준공도·HMI 이벤트/쓰기권한|새 자료 없이 재조사 반복·현장 완료 표시 안 함|

## 1. 설비·자료 기준

- catalog_id TC01, 별칭 tc_01, 계측/sensor, parent 없음/depth0, phase2/planned, priority_key 없음, INVENTORY catalog[12], 설비 색인[76]. 역할 AB01 챔버 온도. TC02 안전 온도 채널과 별개 ID.
- 범위: `progress/TASK3-BATCH07-SCOPE.json`, `GME-CATALOG-OVERLAP-REVIEW.json` TC01 행. 로컬2차133 통합 제외 유지. 부모/별칭/같은 이름만으로 실물 병합하지 않는다.
- 읽기 전용 기준 `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. https://github.com/esp6662266/gme-plc-manual . 이 고정 백업은 현행 CPU의 증명이 아니다.
- AGENTS, 스킬/source-map, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, START-GPT61, VERSION/WORKSPACE-HANDOFF/PUBLICATION_STATUS/EXPANSION-WORK/ACTIVE-WORK를 읽었다. 최신 배치 지시에 따라 원본 preflight/build/test/generator 실행 없이 자체 파서·해시·PDF렌더만 수행.
- 쓰기 범위 `drafts/TC01-DOTS-DRAFT.md`, `extracts/TC01/`만. 원본/코드/대장/버전/배포/운영 기록/SEJIN 변경0. PLC/현장/보호값 변경0. 새 Work/Codex/재위임/사용자 Mac 접근0. 로컬 TIA 추가 접근권한 없음. 실제 모델·추론 수준 런타임 증명 미확인.

이하 원본 경로는 `source-mv06/all-in-one/` 기준. `0489`는 `sources/decoded-original/0489-FlgNet.xml`, 선언 `0676`는 `0676-IdentXmlPart.xml`. LAD 문서번호와 XML NID를 구분한다. 추출 refs의 동명 후보는 자동 의미확정이 아니며 아래 핵심은 선언 그룹·핀을 직접 대조했다.

|7영역|상태|확보/누락|
|---|---|---|
|설비·자료|적용|고유 ID·고정 판본·AB01/HE01 위치 상충, 실물 미확정|
|IO/HMI|적용/일부 미확보|IW272/DB1/3/4/13/39, HMI 주소; 화면 이벤트·현재값 미확보|
|제어|적용/일부 미확보|환산·선택기 경계·복수쓰기; 실제 실행순서 미확인|
|전기끝점|적용|FG77/106·시공p56; 실제 배선·명판·교정 미확인|
|알람/복구|적용/복구 미확보|OFR/MAX/MAXMAX/비교 S/R·버너 영향; 승인 복구절차 미확보|
|증상관찰|적용|읽기 전용 관찰안; 실제 측정·조치 미수행|
|완료/누락|적용|문서 조사와 통합/UI/TIA/현장 분리|

## 2. I/O·HMI

### 2.1 선언과 주소

DB 결속: 0674 DepDBBlock RID8=Coeff DB4, RID11=Data DB1, RID354=Allarm DB3; 0682 RID3=DB1, RID10=DB3, RID15=Flag DB2, RID168=Manage_TC1_2 DB39; 0628 Inputs=DB13. SSD.AO는 bit offset. Timer AO는 T 번호이며 byte offset으로 나누지 않는다.

|신호|형식/주소|직접 선언·핀|
|---|---|---|
|TC01 원시|Int IW272:P|0678 RID66 AO2176 SAM=Peripherie, NID9 UID324; 0489 W331→CRef316.Analog_input|
|TC01 원시 미러 읽기|Int IW272|0627 RID61 AO2176 SAM=None NID2 UID56; 0398 W67→Move50.in|
|Inputs.TC_01|Int DB13.DBW36|0629 RID64 AO288 NID2 UID57 Write; 0398 W69 Move50.out1|
|Coeff.ZERO_TC01|Int DB4.DBW12|0676 RID68 AO96 NID9 UID326; 0489 W333→Zero|
|Coeff.COEFF_TC01|Int DB4.DBW14|0676 RID67 AO112 NID9 UID325; W332→Coeff|
|Data.Temp_TC01|Int DB1.DBW110|0676 RID69 AO880 NID9 UID327 Write; W334 OutValue|
|Allarm.TC01_OFR|Bool DB3.DBX21.2|0676 RID373 AO170 NID9 UID23 Write; W24 Out_of_range|
|Data.TC01_SETPOINT|Int DB1.DBW66|0650 RID2 AO528, 0585 RID59 및 0577 RID71에 복수쓰기 선언|
|Data.TC01_MAX_ALL|Int DB1.DBW68|0684 RID5 AO544 NID1 UID211/217/224|
|Manage_TC1_2.PID_Ref_Temp|Real DB39.DBD2|0684 RID169 AO16, 0650 RID91 NID9 UID4019/3796/3709 Write|
|Manage_TC1_2.EnableTC01|Bool DB39.DBX0.0|0650 RID75 AO0, NID9 UID3880/3750/3661 Write|
|Allarm.MAX_TC01_TEMP|Bool DB3.DBX8.0|0684 RID11 AO64 UID215 Set/222 Reset|
|Allarm.MAX_MAX_TC01_TEMP|Bool DB3.DBX8.1|0684 RID23 AO65 UID236 Set/239 Reset|
|Allarm.TC01_TC02_COMP_FAULT|Bool DB3.DBX9.1|0684 RID81 AO73 UID797 Set/800 Reset|
|TC01-TC02control disable|Bool M80.2|0686 RID73 AO642 NID8 UID782; Contact834 negated|
|Tag_99/Tag_100/Tag_108|Timer T85/T86/T116|0686 RID9/22/80, AO85/86/116; PLC 타이머, HMI 태그 아님|

### 2.2 HMI 설정 주소 확인

`sources/hmi_plc_tags.csv`의 dde.cfg 추출 설정이며 현재 화면 이벤트·실제 Write·로그인 권한·화면 알람 문구를 증명하지 않는다. `extracts/TC01/hmi-address-matches.json` 전체13행.

- I_TC_01 `DB13,INT36`, ID00060: 원시 미러.
- data_DB1_DBW110 `DB1,INT110`, ID00275: 환산값.
- data_DB1_DBW66 `DB1,INT66`, ID00251; data_DB1_DBW68 `DB1,INT68`, ID0022A: 운전 설정/알람 기준 구분.
- Coeff_DB4_DBW12/14 `DB4,INT12/14`, ID001E3/002CD: 계수/제로, 현행값 미확정.
- EnableTC01 `DB39,X0.0`, ID00211; TC_PID_REF `DB39,REAL2`, ID001C0: 채널 enable과 선택온도.
- Allarmi_208 `DB3,X21.2`, ID00254; Allarmi_65 `DB3,X8.0`, ID0014C; Allarmi_66 `DB3,X8.1`, ID0014B; Allarmi_74 `DB3,X9.1`, ID00143.
- Editor_TC01 `DB26,INT22`, ID00412는 위 DB1 설정주소와 다르다. RecipesDB 선언/전달 경로 확인 없이 직접 TC01_SETPOINT Writer로 단정하지 않는다.

0398/LAD1071 NID2: Move49.eno→W65→Move50.en; ORef56/RID61→W67→50.in; 50.out1→W69→ORef57/RID64. 앞 Move ENO의 연쇄이며 독립 상시 갱신이라고 보장하지 않는다. 환산 0489는 peripheral 읽기, 미러는 input 읽기로 분리되어 시점·일치 보장이 없다.

## 3. 제어 구조

### 3.1 TC01 환산 고유 결속

0489/LAD1739 NID9의 CRef316 RID351, CodeBlock328 RID5는 공통 변환 인터페이스에 연결된다(0680 BlockInterfaceInfo351, 0672 FCBlock RID5/TOD FC63 Signal linearization). Contact335는 ORef322/RID1 ON: W329 operand, W336 out→316.en. ORef323/RID1 ON→W330→316.IN0. ON 이름을 현재 TRUE로 간주하지 않는다.

W331 TC01→Analog_input, W332 COEFF_TC01→Coeff, W333 ZERO_TC01→Zero, W334 OutValue→Temp_TC01, W24 Out_of_range→TC01_OFR. 고유 호출의 peripheral 주소·입출력 선언을 직접 검토했다. 이 식에 단독 물리 출력은 없다.

공유 함수 0291/LAD1658 NID1, 선언0611/0612 및 0014/LAD1659 NID2:

1. Local IN0 Contact255→W256. Gt258(raw>-1382) 다음 Le161(raw<=32767); 경계 -1382는 제외된다.
2. Convert164 raw Int→DInt App5, Convert167 Zero Int→DInt App6, Add170, Convert174 Coeff Int→DInt App4, Mul177, Div181 DInt 28000, Move185→Local OutValue(Int). 산술 사이 ENO 연쇄 W227/230/234/237/241/245 보존. 정수 나눗셈·형변환 경계를 Real 공식으로 단순화하지 않는다.
3. Gt190(raw>32767) OR Le259(raw<=-1382)→O47→Move193 -9999→OutValue. **W21 Move193.eno→Coil23.in**, W22→Out_of_range. OFR을 비교식 접점과 직접 동일시하지 않는다.
4. 0014 Contact171 NOT IN0→Move162 0→OutValue. 이는 백업 코드값이며 안전 대체온도·센서 정상 판단 기준이 아니다.

도면은 송신기 범위 0/1300°C를 제공하지만 저장 계수값·소수점·교정 상태를 확인하지 못했다. 따라서 내부 -5/+20/±100를 임의의 현장 °C 보호편차로 승인하지 않는다.

### 3.2 선택기와 관련 제어 소유

0650 GlobalAccess RID72=Temp_TC01, RID90=Temp_TC02, RID75/76=EnableTC01/02, RID80/81=TC01/02_OFR, RID91=PID_Ref_Temp, RID95=EmergencyStop 등의 NID9 읽기/쓰기 선언은 확인했다. 해당 SCL 실행 원본/동일 NID의 FlgNet 본문은 이 추출에서 확보하지 못했다.

보충 근거 `sources/live_index.json` 문서 i1719, `values.SCL Code` (별도 `selector-index1719.json` 보존)의 검색 문자열은 다음과 같다. **색인 수준 근거**이고 실제 CPU 실행 증명·원본 핀 대체가 아니다.

- 두 Enable가 참이고 두 OFR이 거짓: `(Temp_TC01 + Temp_TC02) / 2`를 PID_Ref_Temp에 대입.
- 두 Enable 참일 때 TC01_OFR이면 EnableTC01 false, elsif TC02_OFR이면 EnableTC02 false; 그 가지에서 EmergencyStop false.
- TC01-only: PID_Ref_Temp=Temp_TC01, EmergencyStop=false, TC01_OFR이면 EnableTC01=false.
- TC02-only: PID_Ref_Temp=Temp_TC02, EmergencyStop=false, **원문은 TC01_OFR이면 EnableTC01=false**. TC02_OFR로 정정하거나 안전 채널 자동전환을 보장하지 않는다.
- 어느 Enable도 없으면 EmergencyStop=true, 이후 Allarm.EmergencyStopTC1_2에 대입.

원문에는 enable 변경 후 동일 scan의 재평가·최종 PID값 유지·산술 형식 변환이 확정되어 있지 않다. 선택기는 TC01 전용 경보가 아니라 TC01/TC02 공동 기능이다.

### 3.3 복수쓰기·원본의 중지 경계

- 0412/LAD1092 NID14의 원본 블록명 simulation에 Temp_TC01 Writer 존재. 0635 RID287 NID14 UID60/66/73 Write: W91 Add42.out, W99 Sub45.out, W109 Sub49.out. W112 Add50.out는 Temp_TC02로 간다. 이 기존 XML의 정적 관찰만 했으며 시뮬레이터 실행·생성·시험을 하지 않았다. 현재 호출/활성 확인 전 환산값만이 최종값이라고 말하지 않는다.
- TC01_SETPOINT는 0577 NID3 UID660/NID4 UID1009, 0585 NID21/22/23의 다수 Write, 0642 NID1 UID3505가 선언되어 있다. 자동기동 0164/0165, 버너 0190~0192는 후보 인덱스/핀 추출까지이며 전체 설정 우선순위 검토 완료가 아니다. 설정값850 등 과거 상수를 현재 보호 설정으로 옮기지 않는다.
- BR01은 관련 소비 소유자. 0173/LAD1856 NID3: ON Contact160→NOT MAX_MAX_TC09 Contact162→NOT MAX_MAX_TC01_TEMP Contact164→Coil150 `Temperature Interlock OK` (W157/163/165/159). TC01 전용 센서 출력으로 바꾸지 않는다.
- 0175/LAD1858 NID5: MAX_MAX_TC01 Contact293→W294→OR219.in6, TC01_TC02_COMP_FAULT Contact297→W298→OR219.in8. OR219.out W267→Contact305(0582 SimpleAccess RID1, NID5 UID249 ON, %M0.0; 동명 Data 후보는 다른 선언 그룹으로 배제)→W306→OR213.in5, OR213.out W270→RCoil232 Flag.Start_Burner. 앞 ON 및 다른 버너/팬/산소/공동 EmergencyStop 조건을 생략한 단독정지식으로 만들지 않는다. 외부 버너 화염·퍼지·가스 차단 안전 내부 순서는 본 조사 범위 밖이다.

## 4. 전기 전달 끝점

### 4.1 OEM 실제 PDF 렌더

`Electrical_Rev2.pdf` 실제 p78=FG77, p107=FG106. 페이지별 PNG와 FG106 footer 별도 렌더를 직접 확인했다. 두 footer DATA 27.05.2024, DISEGN G.G., NORMA IEC, TOT262. 보이는 개정 기입란은 공란이다. 파일명 Rev2를 이 두 쪽의 개정란 Rev2라고 적지 않는다.

TC01 경로(FG77 왼쪽, TC02 중앙과 분리):

- +24Vdc 10.7 연속선 76/9→78/0에서 분기→5×20 50mA F 표기의 X1:186→선77.1→TC-01 송신기 +5.
- TC-01 -6→X1:187→`+PEW272` 교차참조106/2→FG106 모듈 단자2 `I0+` (PEW272).
- 실드/접지 표기→X1:188→`77SCH1` 교차참조106/2→FG106 차폐 연결. 실드를 센서 전류 반환선으로 혼동하지 않는다.
- FG106 단자4 `U0-/I0-`는 공통 반환선 및 단자8/12/16/18 MANA와 연결되고 위쪽 `-0Vdc 10.6` 연속선105/9→107/0으로 간다. TC01의 1=Uv0/3=U0+에는 TC01 전류선이 그려져 있지 않다.
- FG106 라벨 CPU515/MOD3, 입력 PEW272, `TEMPERATURE CONTROL CHAMBER AB-01 (TC-01) (4–20mA)`. CPU515는 도면 문자이며 실제 CPU 모델/슬롯 확인을 대신하지 않는다.
- FG77 송신기 OUTPUT4–20mA, 0/1300°C. 실제 제조사·프로브 열전대 타입·냉접점 보상·번아웃 방향·전송기 모델·현재 범위·교정성적서 미확보.

이 경로에는 TC01 전용 릴레이 부하 접점을 식별하지 않았다. 다른 설비의 5/9 또는 하단접점표1/5/9를 온도회로에 복제하지 않는다.

### 4.2 시공 케이블 별도 판본

`Electrical_Can_Decoating_20241118.pdf` 실제 p56, DWG CANDC-CONS-C006-056, D-PAGE6, TOTAL56/64, CABLE SCHEDULE(5). 하단 개정1/24.11.11/first draft design; 승인칸 공란. 승인 준공도로 부르지 않는다.

행6_23: `=FLA+HE01-TC01A`, FROM CR(태그 공란)→TO HE-01 / TC-01, Current Type TC, SPEC KX, CORE2S, SIZE1.0, SPARE0, ROUTE100 LCD1→E500, Adjustment10, LEN50. 단위가 명시되지 않은 길이50을 추정 단위로 고치지 않는다. 이 표만으로 OEM X1:186/187/188 전선 각심과 결속하지 못했다. 현장 열전대 케이블과 송신기 4–20mA 케이블 경계·위치 차이를 도면 상충으로 남긴다. SEJIN 운영기록의 복제/수정이 아니라 허용된 고정 원본 도면 읽기만 했다.

## 5. 알람·복구

### 5.1 TC01 고유 범위고장

0489 Out_of_range→Allarm.TC01_OFR DB3.DBX21.2. 0291의 범위 비교 및 Move193 ENO를 거친 Coil이며 SCoil latch와 다르다. HMI Allarmi_208 주소와 연결되나 실제 표시문구·Acknowledgement·팝업 동작은 미확보. 단선/역극성/센서불량이라는 단일 원인으로 확정할 수 없다.

### 5.2 선택온도 고온 경보 0527/LAD1979 NID1

공통 선행 Contact286 ON→W287. 모든 수치는 고정 백업 논리 설명이다.

|경보|발생·기억|해제·부수효과|핵심 선언/핀|
|---|---|---|---|
|MAX_TC01_TEMP|Gt149 PID_Ref_Temp > TC01_MAX_ALL→SdCoil155 S5T#6S/Tag_99 T85 및 Contact288→SCoil160|현재 경보 Contact290→Sub165(설정-5)→**ENO W255**→Lt169(PID_Ref_Temp<지역app00)→RCoil173 및 STOP_HORN SCoil175|0684 RID169/5/11, 0685 Local RID14 Int app00; W241/242/243/244/245/248/255/258/259/260|
|MAX_MAX_TC01_TEMP|Add179 설정+20→Local max_max_tc1; OR185[(Gt186 PID>max_max_tc1),(Gt189 PID>1250.0),(Lt192 PID<-60.0)]→SdCoil198 S5T#6S/Tag_100 T86, Contact292→SCoil203|ON→RESET_ALLARM Contact294→현재경보 Contact296→RCoil208. 값이 정상으로 돌아왔다는 조건을 이 reset 가지에 추가하지 않음|0683 RID18=20,171=1250.0,172=-60.0,8=S5T#6S; 0685 Local RID19 Int; W262~279/281~284/295/297|

MAX는 엄격 `>`/`<`, MAXMAX의 범위 조건도 엄격 `>`/`<`. 설정/지역변수는 Int, 비교 Part의 SrcType=Real. 이 형식 경계·실행 변환은 CPU/TIA 미검증이며 안전한계 설정으로 제안하지 않는다. RESET은 오류 원인 제거·재기동 승인·외부 버너 재가동을 의미하지 않는다.

### 5.3 공동 비교 고장 0534/LAD1986 NID8

- ON Contact832→NOT disable Contact834(`M80.2`)→W835→Gt745 TC01>400, Gt748 TC02>400. 두 비교는 OR744이며 AND가 아니다.
- OR744.out W809가 Sub754.en 및 Lt761.pre/Gt764.pre를 **병렬**로 공급한다. Sub754(TC01−TC02)→W812 Local app02(0685 RID77 Int). 비교 pre가 Sub ENO에서 온 것으로 바꾸지 않는다.
- app02<-100 또는 app02>100→OR760→W819→SdCoil770(S5T#1M, Tag_108 T116) 및 Contact836→W837→SCoil775 DB3.DBX9.1.
- ON W833→RESET_ALLARM Contact838→현재경보 Contact840→RCoil780. Reset 가지는 disable NOT의 뒤가 아니라 ON에서 갈라진다.
- ±100 및400은 원문 Int 상수. 실제 오차 허용치/설비 안전요구조건으로 승인하지 않는다. TC01 고장·TC02 고장·온도차를 구분해야 하며 BR01 요청 reset 영향은 관련 소유로 별도다.

## 6. 증상별 관찰안

조작·보호값 변경·reset·재기동을 지시하지 않는 읽기 전용 관찰안이다. 실제 관찰값은 없다.

|증상|관찰 위치/비교|배제와 남길 기록|
|---|---|---|
|HMI 온도 고정/서로 다름|IW272:P, IW272 process-image, DB13W36, DB1W110, DB39D2 및 각 수집 시각|원시 미러/환산/선택값 구분; 0398 ENO·0489 호출·계수/제로·별도 Writer 활성 확인 필요|
|OFR 경보|원시 Int 부호값, DB3X21.2, TC02 OFR, 송신기 루프/채널 진단 자료|범위조건·단선·전원·교정 구분. -9999/0으로 실제 온도를 판정하지 않음|
|TC01 표시가 낮아도 MAX|DB39D2, EnableTC01/02, TC01/02 값, TC01_MAX_ALL, T85/T86|직접TC01 대신 선택값 비교임을 확인; 선택기 원본 결손·Real/Int 경계 유지|
|TC01/02 비교고장|M80.2, 두 온도, 차이 app02, T116, DB3X9.1, Reset 요청 시각|OR>400 및 ±100 조건과1분 경로를 구분; disable/reset 변경하지 않음|
|고장이 없어져도 버너 정지|DB3X8.1/9.1, 공동 EmergencyStopTC1_2, Temperature Interlock OK, Start_Burner|BR01 요청/인터록/외부 응답을 별도 검토; TC01 수리만으로 재기동 완료 아님|
|도면 위치와 설치가 다름|센서/송신기 명판, 실제 설치장소, 단자번호·케이블 식별표, 승인준공도|AB01/HE01 상충 및 KX/4–20mA 구간 결속 확인. 무전압/작업허가 등 승인 정비절차는 별도 담당|

관찰 기록 필수: 관찰자·실제시각/시간대·설비/프로브 위치·프로젝트/CPU 근거·값/자료형/단위·수집장치·비교 원본·원인배제·승인조치·복구증거. 없는 값을 정상/0으로 채우지 않는다. 사용자 운영기록·사진은 공개 원본에 복사하지 않는다.

## 7. 완료·누락·검증

- 문서: complete_with_gaps. TC01 고유 IO·환산·전기끝점·경보·관찰안과 공유 기능/상충 정리.
- 자체 정적 검토: 고유19항목 assertion 모두 true, 전체18개 네트워크 핀 추출. 이 중 고유 핵심0489/0527/0534 및 공유0291/0014 의미검토, 0173/0175/0398 경계검토, 0412 별도쓰기 정적검토. 기타9개 추출은 전체 의미검토 완료로 세지 않음.
- 원본 선언181개 검색/파싱과 해시226개는 각각 검색·무결성 범위이며226개 의미검토 완료가 아니다. 공통90파일 같은 과거 집계도 해시와 의미검토를 혼동하지 않는다.
- 원본226/226 SHA256 및 고정 Git blob 바이트 일치, 중지5자산 freeze 해시 일치. Git status clean. `extracts/TC01/source-hashes.json`, `assertion-check.json`, `static-review.json` 참조.
- 독립 검토 pending. 부모 검토에서 원본 핀/선택기 경계/도면 끝점 확인 필요. 이 자체19검사를 독립 검토로 부르지 않는다.
- UI/기록 not_run; publication not_published; TIA compile/live CPU/field recovery 모두 not_performed. 프로그램 통합·버전/대장 갱신·게시 작업 미수행.
- 네 기능: 도면↔래더 비교 적용 후보(본 근거표 확보), 백업/선택복원·전후비교·관찰보고서/PDF는 설비 UI의 실제 저장/재읽기/재열기 미검증. 이번 PDF는 원본 도면 렌더로 보고서 생성 완료가 아니다. note/repair_observation/미지필드/기존 기록 수정0.

### 필요한 다음 자료

1. 현행 승인 준공도 및 TC01 실물/송신기 명판·배선 식별·교정 성적: AB01/HE01·KX/4–20mA 구간 확인.
2. 승인된 읽기 전용 현재 프로젝트/실제 SCL 본문 및 채널/DB 선언·호출 구조: 선택기 doc1719 의문, 복수쓰기·자료형 변환·최종값 확인. 추가 TIA 접근권한 없이 진행하지 않음.
3. HMI 화면/이벤트 원본과 현재 역할권한: raw/환산/선택값 표시, Editor_TC01 전달, 알람 표시/acknowledgement 결속.
4. 실제 계측/안전 설정 승인자료와 시각있는 관찰기록. 본 초안의 수치로 보호값 변경·센서 우회·reset·재기동하지 않음.

### 실제 작업 단계 시각(UTC)

- 2026-10-11 10:52:02: 부모 배정 및 지시/범위 읽기 시작(대화 도구 시각).
- 10:52:07–10:52:51: 원본 지침·고유 선언·공통 색인·환산/경보 XML 읽기(각 도구 응답 실제시각).
- 10:53:13: FG77/PDF78 및 FG106/PDF107 렌더 시각확인.
- 10:53:38: 자체 선언/네트워크 추출 완료 도구 응답. 정밀시각은 stages.json.
- 10:54:26: 시공p56 렌더·페이지/케이블 행 확인.
- 10:55:40.207460+00:00: 자체19검사·226해시/Git blob 검증 완료.
- 10:55:48–10:55:55: 선택기 색인doc1719 및 FG106 footer 재확인.

## 부록 A. 원본 SHA256·고정 Git blob 전체 목록

모든 행의 파일 SHA256과 git blob SHA256이 같고 바이트 동일함을 확인했다. 별도의 git blob object ID도 아래 보존한다. 기준 commit은 위 고정값. `IdentXmlPart`181개는 검색 corpus이며 선택된 선언 외 전체 의미검토를 뜻하지 않는다. 중지5파일은 해시보존용으로만 읽고 실행하지 않았다.

|원본 경로(source-mv06 기준)|SHA256 = 고정blob SHA256|Git blob OID|
|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` |
| `.agents/skills/gme-equipment-rollout/references/source-map.md` | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` |
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
| `all-in-one/sources/decoded-original/0035-IdentXmlPart.xml` | `3a1e3c8c96b30b843c6d75fc7d961972864571095dd972afa94a6b5c8c463b8b` | `c37a386e485291ed7b4387320b6eb5bfc8826183` |
| `all-in-one/sources/decoded-original/0036-IdentXmlPart.xml` | `d1b7556a1edcf20ecbe76769cd446f7960a5c50c1f464004f07acfe47c856091` | `0d48db4c91725bd3a13cf90bb6bd79144b0ed764` |
| `all-in-one/sources/decoded-original/0037-IdentXmlPart.xml` | `e92ae321d16be03fa669dc70d4703eb6dcdac4153427518e40cd7514c7bab06e` | `6070cd95a24ee9a635ef58d047310b89b57b740b` |
| `all-in-one/sources/decoded-original/0038-IdentXmlPart.xml` | `4c0347349822cbc9ac56fa868355893073215fc8fbefa094d1c7a37f236628b7` | `02dcccd2e0cdde35615e718f5ba2a53ec767f6d2` |
| `all-in-one/sources/decoded-original/0039-IdentXmlPart.xml` | `3ae955e5079c7e2f14f98035cffec43763714a9aa62d3b1defe86164aeb43486` | `00d088df9d43e85d53c2d4feab5b0364399642ae` |
| `all-in-one/sources/decoded-original/0040-IdentXmlPart.xml` | `4aa4f09101f827918ca2af003544aa0de8a70410cc4d69e738f2d6220669f182` | `dde9014e48da7a32dbb0cf9523dbdb6afcfd0bb3` |
| `all-in-one/sources/decoded-original/0041-IdentXmlPart.xml` | `f6879784dcb83569b01753a2986e4db4ddb411f64580d1e72c22c114dcdaae15` | `80b12f3b9be6cb015dacff8fc852ee4476768c0c` |
| `all-in-one/sources/decoded-original/0042-IdentXmlPart.xml` | `39a10a59ac8afcda3d1729f6b07dccea38c00227605c43cac46853fdc3e1b5e2` | `62cfa50ff1c308189542b805e9797f2294097407` |
| `all-in-one/sources/decoded-original/0043-IdentXmlPart.xml` | `c71c75f0b13763a806cc984f933fd0ec785f77a0fe6915267ebf7648189ddb33` | `f20ba4e4479e42f8496e637a0e755814fe1dac56` |
| `all-in-one/sources/decoded-original/0044-IdentXmlPart.xml` | `80ed7b8be0e4988ac52ac84cbc7e68a29a15755c821d9b0452247d9f362638c2` | `eb44635cb72b77f04dea4319e47d96ee68c09a58` |
| `all-in-one/sources/decoded-original/0045-IdentXmlPart.xml` | `334d3c31a4dc1084cd9e6d870058e32f5e96c17ece69e5fc52038965416a1c79` | `d455986215307b725280a4ff3beea011d8d37e25` |
| `all-in-one/sources/decoded-original/0046-IdentXmlPart.xml` | `1df29e9d0382743dcf42b287223f63f9880740616318769d8e23fdb8a68a97b1` | `8c7426049cdd9f9f00d96c6298af443d5a336e38` |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` |
| `all-in-one/sources/decoded-original/0049-IdentXmlPart.xml` | `d4c49fa00735537ee8cce4baba526b0027e4fe25343074e83de5719cafd1bacc` | `50478b19d7a3d4af551c914f181fb25b6f809331` |
| `all-in-one/sources/decoded-original/0050-IdentXmlPart.xml` | `f7ceb0408380d3fad2df3bbf5c663c393b57d1ce156af7a587e14c6b1eb701e3` | `9a94a69077a225b05da86a8118b5ec1622dcc629` |
| `all-in-one/sources/decoded-original/0051-IdentXmlPart.xml` | `b43718d933537099d8ab3fac88b2012d088d46b69ca1d31ac1570bae4a62cd6c` | `2c7597408597e1cce84deca2d0a01c2465b72eb7` |
| `all-in-one/sources/decoded-original/0052-IdentXmlPart.xml` | `fbd673549a61f7da169e452e2221da4958b29b3e3c1c3699e9cad3d02577500a` | `9304a3d08ead7483362605eca3169e15518fa6b9` |
| `all-in-one/sources/decoded-original/0053-IdentXmlPart.xml` | `1d386f98f7bc842e474cf9448dbe37ff3f86775797644252b56d7407e1936c80` | `27c0527904f201efbdd33c50d1e94c08a3f4ecf4` |
| `all-in-one/sources/decoded-original/0054-IdentXmlPart.xml` | `32d9ad8334dc4c115b04e24702a02051de3155e007de26fba4e32b2d43a1e87f` | `ae93a5d3b602ba2e35990bcf904571009388757f` |
| `all-in-one/sources/decoded-original/0055-IdentXmlPart.xml` | `9baf3104be3c8a3457c3eea021f23fbd6a60c665e81a293bd7f2cae52c64be29` | `85d87193fda164b5c7282f6e40ec5f49b3383309` |
| `all-in-one/sources/decoded-original/0056-IdentXmlPart.xml` | `c5ec45cd232c36d80f80487ec0dd284a876e326ba2286fc722ecc861a400232a` | `1364306d64caf1f1f094c98dc163edf69cdc1afc` |
| `all-in-one/sources/decoded-original/0057-IdentXmlPart.xml` | `1124275ab34e188b042b263d3c4b744abf5637ffd229af642b81a27f00a00c6b` | `264d24445f42cf32706bc6942863f9f227eb797e` |
| `all-in-one/sources/decoded-original/0058-IdentXmlPart.xml` | `84db55242df6a85df73776bfd23bf16cc10e4da35fedca4942f4a43bc4cd1702` | `f13bf595dc1b216bb375b7374b8d849dc7db7c95` |
| `all-in-one/sources/decoded-original/0059-IdentXmlPart.xml` | `f02ef8f08f1c7ca7625bdbcf90a2c9365f12654d19e2e526fe8e5b0b742263d0` | `ccbe8f3e8aadc1c9a052629b674e47805371c84b` |
| `all-in-one/sources/decoded-original/0060-IdentXmlPart.xml` | `d61344a049baa2ce8a97335cd94e6c1753f8f8b7180d3def74d8631ff2cf21b9` | `8751e6aab7045a8f0a6f9d515197aeb5c81ba6dd` |
| `all-in-one/sources/decoded-original/0061-IdentXmlPart.xml` | `0861f9e3686b911262b7b7e108c51fc9fed9cb7080c72bcc4b3aae60750af1c7` | `736313f3bebebf3ba6ee674b058a43185520d391` |
| `all-in-one/sources/decoded-original/0062-IdentXmlPart.xml` | `34f188168dc4fad0d6e2c813028045f37b84025636bcebd8aa1c7ffb4cfd9bcd` | `624eed3ba6cd1eb54e7e3f316f8c4c159ca3b4b5` |
| `all-in-one/sources/decoded-original/0063-IdentXmlPart.xml` | `9dceae18963ead11293cfc3a70c2eac077faa53ebd28e23bb4e84bc3278c5034` | `9de78fc3f67460e61214d2bed3ec5b6e4e82bd92` |
| `all-in-one/sources/decoded-original/0064-IdentXmlPart.xml` | `ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d` | `300d74239868f4f4595d4d5bbb848b4b58bbae76` |
| `all-in-one/sources/decoded-original/0065-IdentXmlPart.xml` | `c99a9960a364084a8e9f007803db72ebaf0ac0ea9126c1b0692da1e5337b33be` | `a427905d03fe4cf63cf6b9d0315a1be8d1bcd04d` |
| `all-in-one/sources/decoded-original/0066-IdentXmlPart.xml` | `13ff943033934043bb50d38d95e46706443a12b1eef70471cb0f35d3b0ade402` | `55adec8d054eb4d3b186c6498616457ad254c22f` |
| `all-in-one/sources/decoded-original/0067-IdentXmlPart.xml` | `0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628` | `455f00638f1618f194b1c83d9c0c2f157663a902` |
| `all-in-one/sources/decoded-original/0068-IdentXmlPart.xml` | `0a71d492e69760390b99f71a75f02ef684e271554b003d5de8bf64a26c64eeba` | `abf1e8cf672afee026f7945219fcee8ad62c9787` |
| `all-in-one/sources/decoded-original/0069-IdentXmlPart.xml` | `da5203cd92ccadfea2029aafb45a1e6e99443d7edbbcc2fd2f2927482564590d` | `26204ec172cabfadf54c1ad6a74013bfaae06a11` |
| `all-in-one/sources/decoded-original/0070-IdentXmlPart.xml` | `bac2852c85f039a342a0066b3c38df60c572d89b3358fb889b104126d530a447` | `061988f3b48be1073ca3fac3dbf335fc9e79b0fb` |
| `all-in-one/sources/decoded-original/0071-IdentXmlPart.xml` | `49d01eba491fe39ed64cb9b15719f3445f49979ddc73753cb398628075b0d6c3` | `6f3924a0d75ac7ee3820e83d2873109dd1291b33` |
| `all-in-one/sources/decoded-original/0072-IdentXmlPart.xml` | `4528729656e87a902d9be2ab85d2b890b2cb3c68df619b881781eff985eede27` | `7c5a73659e4eba679dd85c8774cc9cf6ce770b3b` |
| `all-in-one/sources/decoded-original/0164-FlgNet.xml` | `15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491` | `1035a51ee3100d524da1b7b204ba142b6b509ac5` |
| `all-in-one/sources/decoded-original/0165-FlgNet.xml` | `4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88` | `8d636eb535060037ccf00ebdfb328b8775225fe4` |
| `all-in-one/sources/decoded-original/0173-FlgNet.xml` | `b4f2002933f13ad38f8b8bc6daa3f3ef11a9181ea1c2f33f63ef7a3f7305dc07` | `a880d18b10887c0385745539ab80f8fb45e7647b` |
| `all-in-one/sources/decoded-original/0175-FlgNet.xml` | `41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97` | `1626da00b3bbcb46f77720271ecf0f50db9dc63b` |
| `all-in-one/sources/decoded-original/0178-FlgNet.xml` | `36752e04a38e486ad4a0857d6baa8119d9b757678300358bcc95881f23e266c9` | `5831f5a312f2fbc2738b5e18de1aba6016bd8c36` |
| `all-in-one/sources/decoded-original/0180-FlgNet.xml` | `b3141dffaf1a7d0583e3d03ab5bf3b8dcab62e42f3722c45ce0a9d3f8b608e58` | `ee118b4076a8938b74b246c5e99ede30b390d55f` |
| `all-in-one/sources/decoded-original/0181-FlgNet.xml` | `98e839ee13a05db05768503e768e9238d892c4788dc7b6c9d3017fc86d3b722b` | `ff48f9494436c2557ad1d3d45edd4197f3e622fe` |
| `all-in-one/sources/decoded-original/0186-FlgNet.xml` | `932f8756ee0e4385553944bd166109c45684766a136bfddd68cdf08552a83883` | `744ced99611f666064f30aae4ac32c5d38622d9e` |
| `all-in-one/sources/decoded-original/0190-FlgNet.xml` | `46722388ab7f69c14436e64051b0bb0c720ba1878b9652c4b859fdb4ddb0bf25` | `851ee4680f7a05c41c79f841a8429560bb361f5a` |
| `all-in-one/sources/decoded-original/0191-FlgNet.xml` | `28f087b14ff3a0a0f5bcb20e212c41357ad36caf3c8308f8019f4b78d60eb7bd` | `df4dce76c1db53fe0e9cd2979044397f4fa56d10` |
| `all-in-one/sources/decoded-original/0192-FlgNet.xml` | `874a8e7d6208c568027f4b03fb0e5e085be7e79b914db9dbef30a43d200ee1d2` | `405a401e2162d732b6cb9f81f2fb411557419b47` |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` |
| `all-in-one/sources/decoded-original/0412-FlgNet.xml` | `701771c268542416a0c75c9505f90f6d98dda0de15dd8953e66798fae6617377` | `f9f1d22e54a072b2f5cdce922e302cfcefa1bd72` |
| `all-in-one/sources/decoded-original/0489-FlgNet.xml` | `942f08041c83fbac9a870743e71135d5e4251f28468be2271bab86ba61873b2b` | `759d6f447b0abd4b4d2e04942a7d3f95227d4910` |
| `all-in-one/sources/decoded-original/0527-FlgNet.xml` | `a91f3876643dbdb796d24833a5d67301ff72a3e41365e52f12ec4509b0f41196` | `ad2aadea551d949ce36aeadcd2ff2cfc0317e4f2` |
| `all-in-one/sources/decoded-original/0534-FlgNet.xml` | `f46e2d9c9dbe465d1068ecf0cc52909e0f8a2691347b533028a908937461a611` | `625186661512560db08e09d8d41ae2455cde59dc` |
| `all-in-one/sources/decoded-original/0552-IdentXmlPart.xml` | `d6cb81b6330e182c430061b494463a73065bd9a0945f39e9a15bb8de8d81703d` | `3b5cfce8d91f75b4d1a8130b79e031d6ab54fb8c` |
| `all-in-one/sources/decoded-original/0553-IdentXmlPart.xml` | `4bf2f2c613e81ee6bd92ac0f21252ea0ce4a1135818fcc404740a914aaae1317` | `ec2344a9d25560ef4d6e53951804ceaf21326c1d` |
| `all-in-one/sources/decoded-original/0554-IdentXmlPart.xml` | `4ae3e7d0bca0f78c9e94617abeb70bdd228d85d74bff2224174fa1bb0076e78c` | `cdb68b35a7287f6b5636c01ea3a01747d3d60e81` |
| `all-in-one/sources/decoded-original/0555-IdentXmlPart.xml` | `46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6` | `9a915a8b9a260b48402df151c1fe0bbcb2f4ea1c` |
| `all-in-one/sources/decoded-original/0556-IdentXmlPart.xml` | `065d71114e26c93af180265e0e6d59d2a190af1f2f0581c5265e7f4f67d6e23f` | `15ae569ff390ef5c791b0f76d96bd86d5ec6b938` |
| `all-in-one/sources/decoded-original/0557-IdentXmlPart.xml` | `536563da118493838d346a6b34b4367bed4185edbe150d79eb2b2042c3950bf0` | `f627dd27d001a8af1770fd43a5dc04ceb572d4e6` |
| `all-in-one/sources/decoded-original/0558-IdentXmlPart.xml` | `45d49d53b6b41312960bb2a329663e87d8803e28d7832308424a6bf5091e6d1b` | `a0b681bd15e9ae15f2e1437576a4486cc732fdf2` |
| `all-in-one/sources/decoded-original/0559-IdentXmlPart.xml` | `ec5c6d3f18cbedc2bf695fb1318c1d3a8d2a71c77fbd4ab30d286e2399a289d1` | `9431d19cf594838e7a451404e1116e4daa822f81` |
| `all-in-one/sources/decoded-original/0560-IdentXmlPart.xml` | `847792a7620ed331f784353ef8037be10ba1618b02c8693cd297585d2357089c` | `54cdd99a46efddab91d2724bae1e596239290968` |
| `all-in-one/sources/decoded-original/0561-IdentXmlPart.xml` | `ac8a4f7b366a262b9d488b5b78aabe8b2dea768753b58993fe7f846989dac0d7` | `0f8308086219f23c888dcb4ead96dd954842ed68` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` |
| `all-in-one/sources/decoded-original/0564-IdentXmlPart.xml` | `2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1` | `c4b1f2cb191970cfce1cce59cb290a9f1f934c37` |
| `all-in-one/sources/decoded-original/0565-IdentXmlPart.xml` | `0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149` | `c2e3e2d57c94c5da864f6e172f0a7a925da942d6` |
| `all-in-one/sources/decoded-original/0566-IdentXmlPart.xml` | `a1914c7ae085acc1f949a649979824bec8b46fcd78a8055318272a1eb5a45265` | `348e6fccf44a8497f58f73e89ec98e892b2df436` |
| `all-in-one/sources/decoded-original/0567-IdentXmlPart.xml` | `5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e` | `48d2fdc3a37b692bfda5234b3cd84c48269552f2` |
| `all-in-one/sources/decoded-original/0568-IdentXmlPart.xml` | `4ea2540c76f86ab5b17a30c7c9182cc0026bc6b05e605eddcd4af6fc3b919f89` | `c3b9bb052c2200805c3d0af5237d41ebaafaaad5` |
| `all-in-one/sources/decoded-original/0569-IdentXmlPart.xml` | `2e77bb83cf9a7aecd228dac33fe1c897e1149f2063786f4f4e54c66be618a2c7` | `d58446112989460d247fc9f2e1b39bb7e4ada67d` |
| `all-in-one/sources/decoded-original/0570-IdentXmlPart.xml` | `9fed133006458c3b43b1d5f2c15107a5a86b4fb7cdbaf3743bf88f0e5a105495` | `15e6452f424d6ef5f0fa2407ae4e4121dbca3044` |
| `all-in-one/sources/decoded-original/0571-IdentXmlPart.xml` | `4a9deeb65a22e497e284fe6d98929e1d201ef5939e4aeca5805b4eb7e007d398` | `1c37da5dfd669fc2606d5d8316dbb7df4978ab19` |
| `all-in-one/sources/decoded-original/0572-IdentXmlPart.xml` | `5ecd18f84e12d702bb46f759b23994dacfa2d97d50fe51e766ca0cf43f75bb4c` | `67fbbd3e804418687c2ceaaea357fbc3016d38b9` |
| `all-in-one/sources/decoded-original/0573-IdentXmlPart.xml` | `a22cc24a974e0c792f32e356a14b277a847e2bb204c91bce01c37d1714ddb56c` | `97541d25722c43abf428aa8e2197b1973149bde2` |
| `all-in-one/sources/decoded-original/0574-IdentXmlPart.xml` | `0773bc969180298193ed6affe56b485bd2141949f4467dcaf33afbb16ee496cf` | `49305a0a06bfcf6957d93ca1188676def23cb2b1` |
| `all-in-one/sources/decoded-original/0575-IdentXmlPart.xml` | `40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06` | `07d5d2548e8f36252a346d0b83341e27c3cb14ba` |
| `all-in-one/sources/decoded-original/0576-IdentXmlPart.xml` | `c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe` | `819b47160eaa6d08c212f71e5b5486ef5b55b6f2` |
| `all-in-one/sources/decoded-original/0577-IdentXmlPart.xml` | `511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47` | `a505ebf7efd05a85850dc29559a4f71242bacae3` |
| `all-in-one/sources/decoded-original/0578-IdentXmlPart.xml` | `0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b` | `070a79fb12139898dd44a17ab2061e795956b9c6` |
| `all-in-one/sources/decoded-original/0579-IdentXmlPart.xml` | `ee35cf525388f2b38399787caef57a978b0bb17216a90e1a90ac4391e0e799fe` | `19d1039319ffeb150767d96fc36205326483b1c4` |
| `all-in-one/sources/decoded-original/0580-IdentXmlPart.xml` | `fa748a6c1890f579d694fd5e561b2304f717da79e5352ca32152cc20e877c6ff` | `9bd503f23708fada1a1f871e0e52b0eb75e9aacf` |
| `all-in-one/sources/decoded-original/0581-IdentXmlPart.xml` | `5d1d7372935d984aa2d701aa70bdb4555ee1e98d0b0c23806db7bda1ad9134c5` | `2614704e8c68a43d20f3fbb6b1d300b9f8b7199f` |
| `all-in-one/sources/decoded-original/0582-IdentXmlPart.xml` | `41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951` | `82636dec064876d0f4cc714ef385b07d6e05efe0` |
| `all-in-one/sources/decoded-original/0583-IdentXmlPart.xml` | `0a34a2b7ad17eba6198dbe53d5c6aa8e87710c7436b832b9d39a075074ab58a8` | `63a23c921a53805f135a0399ba076265907d0eda` |
| `all-in-one/sources/decoded-original/0584-IdentXmlPart.xml` | `3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d` | `0f8dde829be66041bea79e40ccc4586d84ff1da7` |
| `all-in-one/sources/decoded-original/0585-IdentXmlPart.xml` | `e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184` | `16574d37ef3ca61b59ba396c400e269ab1dd3440` |
| `all-in-one/sources/decoded-original/0586-IdentXmlPart.xml` | `f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250` | `266989c590cf52f82e1553f8626a209b8c0b6e0b` |
| `all-in-one/sources/decoded-original/0587-IdentXmlPart.xml` | `bab957ac7c180d9c91b4f904b29e9dbd5812c6ba8f7b9e0c7faf9708605b203e` | `67e84e4b8d43b7c5864ec40fcc2c9fbc2222b436` |
| `all-in-one/sources/decoded-original/0588-IdentXmlPart.xml` | `def5646a0d1eacaae81518f0952c4ba8ada5ea38852463a1d463ff439f3d1905` | `07d012cdc3fb0662f8126f4c274a36288e3bfc9b` |
| `all-in-one/sources/decoded-original/0589-IdentXmlPart.xml` | `846630f3832df93ccdcb0bf86a029546886f8cdba51cd952eed63257ee4540e2` | `5de11972e1fb84f02e4585a53fab478d54e203d0` |
| `all-in-one/sources/decoded-original/0590-IdentXmlPart.xml` | `baff7271b3db646e8953c31d20b72f7b044b1154b689b15ca0fb38ebb44ad81c` | `5816a1fc640da97d27ec68c8c45f255a0bd60730` |
| `all-in-one/sources/decoded-original/0591-IdentXmlPart.xml` | `2e165c44fc9df852ea3729b3ddb33dc0a74e4f8826676f9c5c5626e1dce033f8` | `407456d55041d82dd19e551f904a217a11478289` |
| `all-in-one/sources/decoded-original/0592-IdentXmlPart.xml` | `d157e3d92df9e4a6ce46567b8611a51b0a10abf4dd7f9c4e613087b2df9583a8` | `09bbf459f42d75a973dad70dcfa6871c668b0851` |
| `all-in-one/sources/decoded-original/0593-IdentXmlPart.xml` | `504568b5b50bb25a6880e9da724f79438fbb07e7a311a9391681143d713499e9` | `f2447d339be5de33caf49e1dd56d970eecfd23a2` |
| `all-in-one/sources/decoded-original/0594-IdentXmlPart.xml` | `88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd` | `f38b7d9a52b3d5ae74953da8290f6b417758c1b5` |
| `all-in-one/sources/decoded-original/0595-IdentXmlPart.xml` | `10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52` | `1f24565efac58926dabf5b3fc54ad0e9537410b2` |
| `all-in-one/sources/decoded-original/0596-IdentXmlPart.xml` | `a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0` | `c8b2d1a05727b4ca44e2e4bed9fb58ba2b717576` |
| `all-in-one/sources/decoded-original/0597-IdentXmlPart.xml` | `60e292145fe54912a1da7510c8641a4f4c85efe62e1b5206ee3d92794a28de20` | `2831597d1879bd83f239e838dd4cbe6b3dc64e77` |
| `all-in-one/sources/decoded-original/0598-IdentXmlPart.xml` | `dc001c9370a691546c5dea79f5a1252d6d0a5564754703018c47df4bcc2522bb` | `17a4c24ebc97eb13db483e4c64ac386d6a69125a` |
| `all-in-one/sources/decoded-original/0599-IdentXmlPart.xml` | `32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1` | `493de77fc827d8f14192ced05d82df3a062f7965` |
| `all-in-one/sources/decoded-original/0600-IdentXmlPart.xml` | `20c58ee0383d0b6c275bd2d96abd30af7c5d1f3fff59c7d5034cd758936b57d5` | `f22a7ededd0576cf379ee19908da067f08d45412` |
| `all-in-one/sources/decoded-original/0601-IdentXmlPart.xml` | `04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862` | `07bcf656fa58e4a305999456644acd24b3dc6bec` |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | `3a92b304baf4dbf6147e944d9778d2da11285cb1` |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` | `30e199288c147aa22d5ce8407178a391b89c6b1b` |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` | `ced032fa747a8544abf17058ee5ebaa78ba9b23b` |
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` |
| `all-in-one/sources/decoded-original/0608-IdentXmlPart.xml` | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` |
| `all-in-one/sources/decoded-original/0609-IdentXmlPart.xml` | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` |
| `all-in-one/sources/decoded-original/0610-IdentXmlPart.xml` | `c58d07b1b9707dc8c6c2f06c34ee6142f72238a4cf3f376bee8502d1a9532f9d` | `1497b6bfd7fd9b8afe427b9c910d15e9cf888f9c` |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` |
| `all-in-one/sources/decoded-original/0613-IdentXmlPart.xml` | `09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb` | `c9d19a48e947098914f4d2de3348c05b4f6d37e8` |
| `all-in-one/sources/decoded-original/0614-IdentXmlPart.xml` | `c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294` | `da0485aa033700f08c8695d30b93ebd2d377d6c7` |
| `all-in-one/sources/decoded-original/0615-IdentXmlPart.xml` | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` | `49eb86fe01feb83de8c0864b21493d305aff8b20` |
| `all-in-one/sources/decoded-original/0616-IdentXmlPart.xml` | `650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d` | `9f7fdd5f93ac149c139a054ebb34f63c632ef7fd` |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | `9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e` |
| `all-in-one/sources/decoded-original/0618-IdentXmlPart.xml` | `0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c` | `9eec0dbd8abde4aa7295f77b63ad473f895f274b` |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | `11f0502c84a1f319a21459a35c0dc1c6ce8e8f36` |
| `all-in-one/sources/decoded-original/0620-IdentXmlPart.xml` | `da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3` | `dc88b5e87ad3331928f14fcf647673a26fb70b6b` |
| `all-in-one/sources/decoded-original/0621-IdentXmlPart.xml` | `a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee` | `844516839e55f8bf231a18630e010b912190664e` |
| `all-in-one/sources/decoded-original/0622-IdentXmlPart.xml` | `f0b997f1246d76cff71de2160eb617caa936e6987bdf43c73f55cdcf77dccdb6` | `3b1ae1987950d0754aec37282960b314e9913cd3` |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` | `13b3af0459c8e6069bb9b2f1b16454bf479e08dc` |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` | `02511fea47fc47981c101bba49dc40adde1cdcc3` |
| `all-in-one/sources/decoded-original/0625-IdentXmlPart.xml` | `17a9f9bd540bf0a54e9973391fa258d81e567248fd201ae4ff32c367359e69f9` | `047b29b8c09a15a666553bf04eb4fb00f00e1bf8` |
| `all-in-one/sources/decoded-original/0626-IdentXmlPart.xml` | `a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b` | `e0fc80d0c20f4db3eea31d35f578a2fa3c09f8e7` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` |
| `all-in-one/sources/decoded-original/0630-IdentXmlPart.xml` | `1526a89b425470fa6e874bb4a9b6c7bc8e58b740f80d018b9106b6916f402372` | `2d2963f05fe262504f7b8f72454b9f7bc6266a7d` |
| `all-in-one/sources/decoded-original/0631-IdentXmlPart.xml` | `8e5072374f8ef098de72fbf93965b2a7bb0965c0f803e397daa68588c0c38555` | `27aa5aef2b126820b4658362e4aad5ca6d709fee` |
| `all-in-one/sources/decoded-original/0632-IdentXmlPart.xml` | `fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9` | `600935fa8d394c0d247ea20040d5dfff4f05b500` |
| `all-in-one/sources/decoded-original/0633-IdentXmlPart.xml` | `9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc` | `a1ab5ee12addbc92d04c9950d4437e2b564d6b5c` |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` |
| `all-in-one/sources/decoded-original/0636-IdentXmlPart.xml` | `ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca` | `86114327ba1a010b2fcc01dd12b1bf86c01bc02c` |
| `all-in-one/sources/decoded-original/0637-IdentXmlPart.xml` | `3fb68f57dbe2a877c4ad5aa1b3316810cf84958f2d13b5b1d7d321e0915271c7` | `cb1d7fb76aa2afd96eb46984cc1e71b77f36395c` |
| `all-in-one/sources/decoded-original/0638-IdentXmlPart.xml` | `878e7b33a4adb054e172843a7519157e39a5e779a1984fc9ec88cc5c465d5d33` | `c5820897c6028dac5ac9955738be074b528c554b` |
| `all-in-one/sources/decoded-original/0639-IdentXmlPart.xml` | `ae39316c2b618c0783fc1b3889f47d12d8b2a53198c9a7e7b3c40070338c9539` | `c7e224166db0c7ce33275a788633ac549ade6781` |
| `all-in-one/sources/decoded-original/0640-IdentXmlPart.xml` | `2873e2c70eb4ce97c104b00b675c8f800a3ab9621f9d382718428d2d82025379` | `5b899bd63cac30e700a26932a3ffe889ecad8769` |
| `all-in-one/sources/decoded-original/0641-IdentXmlPart.xml` | `75c1f81d659331b8b62578f766e2f0336276caaf086201fdc383e61c195d01df` | `341bca78929061ab73560dd85fef3f4000127782` |
| `all-in-one/sources/decoded-original/0642-IdentXmlPart.xml` | `c922483c261c8ddb98c239a7b4dc3d7f73f9a45261dd5b4d669f39d6918a1c21` | `398f73b99c4a792a68387485fcb47048d166b2a1` |
| `all-in-one/sources/decoded-original/0643-IdentXmlPart.xml` | `ce7ff35daa71ee1728f4e7b5ac3234d0a31a3c71e953021e9c1f9a953783b6cb` | `84b3cfa219e1e1650664f02a67403b8b0e52654e` |
| `all-in-one/sources/decoded-original/0644-IdentXmlPart.xml` | `02ab863d23ad70420950737d07cf960a2c27bca1c7c011d18930f5bd2045e272` | `1b693ba6815fd9533c22684d0acd9d48becf069f` |
| `all-in-one/sources/decoded-original/0645-IdentXmlPart.xml` | `bd0d052cc926d4a9a66ffe9d12de4e5f064231d10a86bd0d3c6e97fd82c4e1d3` | `7280de0c33d0756d250fdb80f15435ecd876b4d1` |
| `all-in-one/sources/decoded-original/0646-IdentXmlPart.xml` | `46f5a677301ad9b0d20a2d9543a2042081ed6db8f0a8fd8d84f25c342c67a8b0` | `db0b2e38d819b6ea29ac980d84b410e864821c26` |
| `all-in-one/sources/decoded-original/0647-IdentXmlPart.xml` | `ffa253c00b62ccdd999f272d95f613caae3a68792ee5ea9d208253dad53e64be` | `d2cf63bd5fe432b0085690496566c9dbcc989352` |
| `all-in-one/sources/decoded-original/0648-IdentXmlPart.xml` | `afaa47ae737d9333fe831ffac2b1d1388f108bb6a2b23d03554fa862f7edb454` | `3dd5101419fbe16bbce7814398209efd6508db82` |
| `all-in-one/sources/decoded-original/0649-IdentXmlPart.xml` | `38f59e654ecfbc2066fa1f8beeb9ced952adc405f8a4fcf3ef233e9d5d026576` | `039bf2e14a610674a8c01d807805d2db9b4a4956` |
| `all-in-one/sources/decoded-original/0650-IdentXmlPart.xml` | `86f53657eb7afb0798da0e215ba226721076c2ab1b25b74eb83e7b3c4b2d8a2d` | `a3d80a76ef5b0d00009c0fc9a1fdeb1471d0b67b` |
| `all-in-one/sources/decoded-original/0651-IdentXmlPart.xml` | `549c09fb14ce6e9734a2ba604c78868647451f24d224ead0d17d209f66428111` | `08d5828b2ed490605da88f6fbb695db5427b6972` |
| `all-in-one/sources/decoded-original/0652-IdentXmlPart.xml` | `251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692` | `eee49f8301a6791748de9ab368159af8e8bc1585` |
| `all-in-one/sources/decoded-original/0653-IdentXmlPart.xml` | `2df91e2095f16613332cfc59d4c51f8a587183e5e75295a119431b61805c92a6` | `4f93c87d6f199d9f8ad16db16fd4df2192ee6d19` |
| `all-in-one/sources/decoded-original/0654-IdentXmlPart.xml` | `b36294f3aad24be72a052bef61c875ca4695d7e101c385cf55bdadec41d5097e` | `118bc3d5610beabdb92a541e19bf4de3ec148b41` |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | `83b60b9de4541a3ffa6ee0db98205a372b525665` |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` | `9bfb9842e55901bab9a71d1ac03158467dfbb1bc` |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | `e625f3d8999c7be7d88c50eab0d93107117b58ec` |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` | `de9a12a6be87466ef1bf05df71c54580c556a827` |
| `all-in-one/sources/decoded-original/0659-IdentXmlPart.xml` | `ec881805a45730533bccd780e152afb9c9d7c7c45ba7587538b92239f9cbd9d2` | `44d88b18c6b3e5cd5765463ab433ac2ba01d317a` |
| `all-in-one/sources/decoded-original/0660-IdentXmlPart.xml` | `0bf4f4c46531f55324602f4f7b1a1e0b9e63df2c6278126f6e5cf1bc9a06509f` | `915de9b3f968310c45682bef86a91adc1fa06e75` |
| `all-in-one/sources/decoded-original/0661-IdentXmlPart.xml` | `90672199fee355011f581d3287046894772f3f3b4cb78bbe0dd0d71bd488ac93` | `cea3653088f8fb5c77afcf715988039cb63e28ac` |
| `all-in-one/sources/decoded-original/0662-IdentXmlPart.xml` | `1838040bfee800fdb3f13b126eaf69a9d178b17cecc0d59ae03e9185216a48a5` | `ba624f3460dc05e8ade4956cdfc2ec621edb4f73` |
| `all-in-one/sources/decoded-original/0663-IdentXmlPart.xml` | `d3980b88d3cd3e49854439d0778c58ed131bae46a6bc3e65ab70e81f766ac03d` | `3051de9b670457991223a08c03f785747e687414` |
| `all-in-one/sources/decoded-original/0664-IdentXmlPart.xml` | `68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed` | `7ce2f1315d5a21d6b77869a59fc9fcb2f17e90e6` |
| `all-in-one/sources/decoded-original/0665-IdentXmlPart.xml` | `50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd` | `ea4a8a5013081f648722c5ebbde3bb1366787990` |
| `all-in-one/sources/decoded-original/0666-IdentXmlPart.xml` | `19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6` | `b6130b32498b6fee0d9e4db7a04dc79f785e1fbb` |
| `all-in-one/sources/decoded-original/0667-IdentXmlPart.xml` | `ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3` | `7f2e1798eb9f260d19d038a83369484d0f438856` |
| `all-in-one/sources/decoded-original/0668-IdentXmlPart.xml` | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` | `fe0f30d1eaae37783b0f03cb090353b3a3de3600` |
| `all-in-one/sources/decoded-original/0669-IdentXmlPart.xml` | `754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2` | `f5bf8f3c41d2a07ba9dcfd8f400548be8cf51cd3` |
| `all-in-one/sources/decoded-original/0670-IdentXmlPart.xml` | `e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841` | `b9466007b14e5c4f5d353dca5734401317e2dc03` |
| `all-in-one/sources/decoded-original/0671-IdentXmlPart.xml` | `26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293` | `e38a4e2c93ac8093e2b0b8e082a64688b5d9845e` |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` |
| `all-in-one/sources/decoded-original/0673-IdentXmlPart.xml` | `450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58` | `1957bff7dd1beffcb6e2a40d6a541c1751753548` |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` |
| `all-in-one/sources/decoded-original/0675-IdentXmlPart.xml` | `b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3` | `d82a33b173c8dc0737fd890eb2a63a88a07d0831` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` |
| `all-in-one/sources/decoded-original/0677-IdentXmlPart.xml` | `69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3` | `b9437406a7e24f073ef88b8369cacc9ad4ecc5ac` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` |
| `all-in-one/sources/decoded-original/0679-IdentXmlPart.xml` | `d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56` | `e8d8a014609871082bf5cfca0f9ab9b78136e920` |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` |
| `all-in-one/sources/decoded-original/0681-IdentXmlPart.xml` | `318e0cf7cd23caadbd3d72d304358dcf978c4b207c04f58fb5b6ce3f31e344e3` | `371ff45e605de3ab1fefc98583d35ca0235d7ca5` |
| `all-in-one/sources/decoded-original/0682-IdentXmlPart.xml` | `25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092` | `61182411e912941161eccf4e90c1f174e5379f0a` |
| `all-in-one/sources/decoded-original/0683-IdentXmlPart.xml` | `0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22` | `662acdb9a06c0ba1c0027e7dd215a28f07d3f02b` |
| `all-in-one/sources/decoded-original/0684-IdentXmlPart.xml` | `6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208` | `d67b98b5d5516e0330aae5cfdbee41a3e09206e1` |
| `all-in-one/sources/decoded-original/0685-IdentXmlPart.xml` | `2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448` | `86bda988d9efedba92ba2f3e4877497d9eb5230a` |
| `all-in-one/sources/decoded-original/0686-IdentXmlPart.xml` | `b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4` | `8c152d926692a8e15973c980e08e338d29411814` |
| `all-in-one/sources/decoded-original/0687-IdentXmlPart.xml` | `fa50e7e0262c5d51eeca60e914fce4616fa39a05a3466aa14ec93ba375b04cb1` | `5f2b010c4bcc6e752c1952a7a65bf48dcd8e275c` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` |
| `all-in-one/sources/decoded-original/0689-IdentXmlPart.xml` | `f0cc6f770c2759b92a9a79f4e289dbfa0ca270d90e0e89496f94a13a8d839d51` | `8db940bdbab78ea27ffc280acba9375d2a93f587` |
| `all-in-one/sources/decoded-original/0690-IdentXmlPart.xml` | `fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541` | `36bd403f48ba8e364126837b19fb0419bbe78941` |
| `all-in-one/sources/decoded-original/0691-IdentXmlPart.xml` | `17cb7d9734d76b39e729e0daf0c89d9bdf74907aab2130c80453fa04e4cea1da` | `d38a1a394f3cf9612e2f344142609e376ef47953` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` |
| `all-in-one/sources/decoded-original/0693-IdentXmlPart.xml` | `9315ddf43bdfbd7367ab0735a5bbfffcd81ced257d1907c1e2c08ae6b8bfa7ab` | `6ee2a128582aa9ceac710b82de14e5ec2c96771a` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |

초안 저장 시각(UTC): 2026-10-11T11:00:09.067107+00:00
