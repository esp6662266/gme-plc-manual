# SYS-RECIPES — 레시피·설정값 관리 자체 원본 조사 초안

## 핵심 확인·상충·누락

- 한 catalog ID SYS-RECIPES만 조사했다. 편집 버퍼, 저장 레시피, 운전 Data 설정, 현재 물리 출력은 별개다. Save는 버퍼→저장본, Load는 버퍼→Data 8개 필드 경로다.
- **기존 파생 매뉴얼의 미확정 일부를 원본 선언으로 좁혔다.** 0641/0642에서 RecipesDB=DB26, Recipes 배열 `0..101`, 요소176bit, HMI 인덱스/표시/요청의 주소를 확인했다. 색인에서 선택 허용범위는1…100이다. 배열 범위와 선택 정책은 같지 않다. 현재 CPU DB의 배치·Retain 검증은 아니다.
- 0553/0554의 별도 Monitor 문맥에서 편집 요소 8개 Int와 Spare/Spare_1/Spare_2 Word3개를 확인했다. 전체 Recipe 구조 비교를 화면의 8개 숫자 비교로 축약하지 않는다.
- SCL364는 주석·줄바꿈이 평탄화된 백업 색인이다. 아래 분기 해석은 색인과 선언의 정적 대조이며 실행 가능한 원형 SCL이나 TIA 컴파일 결과가 아니다. 범위 분기 전에 동적 배열 참조, Load 조건에 직접 In_Range 부재가 있다. 잘못된 번호를 실제 입력하거나 시험하지 않았다.
- FC21 Recipes Handler는 Main의 0030 CRef21에 결속되고 뒤 HMI/Output은 ENO 체인이다. 뒤쪽 부정 접점 Simulation(1)을 레시피 호출의 허가로 거꾸로 붙이지 않는다.
- 레시피 적용 뒤에도 출력변환 클램프·자동 단계·예열·건조가 같은 Global Data를 쓴다. active_recipe 번호만으로 현재 운전값이 저장본과 같다고 판단할 수 없다.
- 공유근거: [SYS-HMI](SYS-HMI-DOTS-DRAFT.md)의 HMI 이벤트/주소 한계, [SYS-AUTO](SYS-AUTO-DOTS-DRAFT.md)의 FC30 단계·주기상충, [SYS-COUNTERS](SYS-COUNTERS-DOTS-DRAFT.md)의 설정비율·생산량 의미, [FN01 고정판본 작업기록](../source-mv06/docs/equipment-standard/work-items/FN01.md)·[RD01](RD01-DOTS-DRAFT.md)·[TC01](TC01-DOTS-DRAFT.md)·[TC03](TC03-DOTS-DRAFT.md)·[PSH01](PSH01-DOTS-DRAFT.md)·[PSH02](PSH02-DOTS-DRAFT.md)의 최종 출력/계측 경계를 연결 재사용한다. 고유 DB26 선언·17 HMI 태그·호출 및 대표 Writer/알람 핀은 이번에 독립 대조했다.

## 1. 설비·자료 기준

고정 원본 `gme-research/source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. INVENTORY catalog43/equipment243, software/공통 시스템, 부모 없음, phase2. 별칭 recipe/recipes/editor_는 검색어이며 실물 장치명이 아니다. 로컬2차133 통합 제외를 유지한다. 사용자 후속 게시판본과 이 고정 조사판본을 혼합하지 않는다.

이하 네자리 XML은 `all-in-one/sources/decoded-original/` 기준. 문서ID는 `network-map.json`/`live_index.json`의 번호이며 XML 파일번호가 아니다. UID/RID/NID가 같은 다른 블록 선언을 병합하지 않는다. AO/BO는 bit offset이다. 코드 블록의 TOD 번호와 DB의 TOD 번호를 구별한다.

모델·추론수준 런타임 증명 미확인. Windows/TIA·CPU 접속·사용자 컴퓨터·새 Work/Codex·재위임 없음. 실제 레시피 수정/적용/시험, 보호값·현장·SEJIN 변경 없음. 원본 build/test/generator와 시뮬레이터는 실행하지 않았다. 작성 범위는 본 MD와 `extracts/SYS-RECIPES/`뿐이다.

|7영역|적용 판정|이 문서 범위/누락|
|---|---|---|
|설비·자료 기준|적용|소프트웨어 ID/고정판본/개별 완료 경계|
|I/O·HMI|적용+누락|DB26/DB1 선언과 CSV17행; 실제 화면 이벤트·권한·현행 배치 미확보|
|제어 구조|적용+누락|선택/편집/저장/취소/적용, FC21 호출·대표 복수쓰기; 원형 SCL/전체 실행순서 미확보|
|전기 전달 경로|직접 끝점 비해당|소프트웨어 DB 전달에는 코일/단자/케이블 없음. 연결 모터·센서 끝점은 각 설비 문서 소유|
|알람·복구|적용+누락|Formula_Fault의 독립 관련 경로; 레시피 전용 통신·범위알람/현장복구 미확보|
|증상별 관찰|적용|수동 수집할 관찰항목만 제시, 변경/강제입력/시험 절차 없음|
|완료 기준|적용|문서/정적/실행/현장 별도 상태|

## 2. I/O·HMI: 편집 영역과 적용 영역

### 2.1 DB26 제어 멤버와 HMI 설정

0641 `DepDBBlock RecipesDB RID15/TOD26`, 0642 GlobalAccess의 BAD15를 결속했다. 아래 RID와 대표 UID는 0642의 NID1 문맥이다. 요청비트의 0 대입은 SCL 정수상수 표기이며 LAD의 RCoil이라고 부르지 않는다.

|멤버|형식/백업 주소|RID, 대표 UID|HMI 태그 / 실제 CSV행|
|---|---|---|---|
|HMI_Index|Int DB26.DBW0|16; 4991 read/4693 Write|HMI_Index, DB26,INT0 /57|
|OldHmi_Idx|Int DB26.DBW2|18;4876 read/3345 Write|이번17행에 없음|
|Vis_SaveUndo|Bool DB26.DBX4.0|40;4488 read/4773 Write|Editor_Vis_SaveUndo /50|
|Vis_Modify|Bool DB26.DBX4.1|50;4747 Write|Editor_Vis_Modify /51|
|Vis_LoadRecipe|Bool DB26.DBX4.2|63;4000 read/4726 Write|Editor_Vis_LoadRecipe /52|
|Load_Recipe|Bool DB26.DBX4.3|65;3984 read/3384 Write|Editor_Load_Recipe /53|
|Save_Recipe|Bool DB26.DBX4.4|52;4479 read/4341 Write|Editor_Save_Recipe /54|
|Modify_Recipe|Bool DB26.DBX4.5|36;4566 read/4794 Write|Editor_Modify_Recipe /55|
|Undo_Modification|Bool DB26.DBX4.6|60;4274 read/4150 Write|Editor_Undo_Modification /56|
|Active_Recipe|Int DB26.DBW6|107;3433 Write|Editor_Active_Recipe, DB26,INT6 /58|

CSV 원본은 `all-in-one/sources/hmi_plc_tags.csv`, Access Name 모두 PLC, 원본 설명은 dde.cfg 설정/온라인 현재값 아님. 데이터 주소 대응은 확보했으나 버튼 Down/Up 이벤트, 쓰기권한, 값 범위, 데이터 품질, 통신 설정, 현재 화면 배치까지 증명하지 않는다. 위 CSV행은 헤더 포함 물리행이며 내부ID와 다르다.

### 2.2 Recipe 구조·8필드 적용

0642 RID24의 형식은 Array[0..101] of Recipe, 배열 BO64/BS17952bit; RID26은 요소 BO64/BS176bit. 102×176=17952bit와 일치한다. 0643 Expression RID25, ED CV0는 RID26/78/89/91/95/98/100/102/104의 인덱스0 문맥을 보강한다. 0553 RecipesDB RID2/TOD26와 0554 Monitor NID=-2147483648의 별도 절대 AO를 함께 대조했다. Monitor는 실행 Writer가 아니다.

|레시피 필드|Editor 태그/CSV행, DB26 주소|0642 읽기 RID/UID|Data 적용 멤버·DB1 주소|0642 쓰기 RID/UID|
|---|---|---|---|---|
|BWF01|Editor_BWF01 /59, INT8|78/3929|SET_PERC_BWF01 DBW0|81/3966|
|BWF02|Editor_BWF02 /60, INT10|89/3872|SET_PERC_BWF02 DBW2|82/3902|
|RD01|Editor_RD01 /61, INT12|91/3814|SET_PERC_FR01 DBW6|92/3840|
|FN01|Editor_FN01 /62, INT14|95/3757|SET_PERC_VT01 DBW8|93/3788|
|PSH01|Editor_PSH01 /65, INT16|98/3685|PSH01_SETPOINT DBW32|96/3722|
|PSH02|Editor_PSH02 /66, INT18|100/3607|PSH02_SETPOINT DBW42|99/3641|
|TC03|Editor_TC03 /63, INT20|102/3536|TC03_SETPOINT DBW50|101/3571|
|TC01|Editor_TC01 /64, INT22|104/3467|TC01_SETPOINT DBW66|103/3505|

위 8개는 모두 Int(16bit). Data 대상은 0641 Data RID80/TOD1 +0642 BAD80이며 동일 NID1에서 AK=Write를 확인했다. RD01→FR01, FN01→VT01은 코드상의 이름 대응이며 설비 실물동일성 판정이 아니다. 단위·HMI 표시소수점·현행 허용범위는 Int 타입만으로 정하지 않는다.

0554 RID26…33은 편집 요소8개 AO64,80,96,112,128,144,160,176bit이며 위 DB26 INT8…22와 맞는다. RID34/35/36은 Spare/Spare_1/Spare_2, Word, AO192/208/224bit(DBW24/26/28)다. 따라서 전체 Recipe 동등비교를 ‘8개 숫자가 화면에서 같음’으로 대체할 수 없다. 이 셋의 실제 운용 의미·HMI 노출은 미확정이다. 같은0554의 AO11856 등 다른 Monitor 요소를 편집버퍼 시작주소로 오인하지 않는다.

Local `In_Range`와 `Differing`은0066 InterfaceAccess, RID47/62, Bool, NID1 UID5007/4956 Write이다. Data 또는 DB26의 Global 멤버로 병합하지 않는다. Differing은 그 선언에서 Write 참조만 있고 색인에서도 뒤 사용이 없다. 컴파일 최적화로 동적 참조가 제거된다고 단정하지 않는다.

## 3. 제어 구조

### 3.1 선택·편집·저장·취소·적용의 정적 경로

근거: `sources/live_index.json` segment `_7ev`, i364, deleted=false, values['SCL Code']; `block_summary.json` recipes handler Language=scl/Version0.1/filter103. recipesdb filter104는 DB번호104가 아니다. 색인 SHA256은 `748103b381c8a669a16a2e506ccb81f426c5e93a472d9cf54a0939cd2fa3139f`. 원문은 `extracts/SYS-RECIPES/index364.json`에 그대로 보존했다. 형식/주소/Write 선언은 §2의 원본으로 독립 대조했다. SCL 몸체에 LAD Part/Wire를 발명하지 않는다.

1. In_Range는 hmi_index>=1 AND <=100. 그 다음 Differing 대입에서 recipes[0]과 recipes[hmi_index]를 참조한다. 범위보정 if보다 앞이다. 배열0…101 존재와 별개로 음수/102이상의 실제 예외·CPU 반응은 미확정이다.
2. 번호가 oldhmi_idx와 다르고 범위 안이면 선택 저장본→recipes[0]. Modify/SaveUndo=0, Vis_Modify/Vis_LoadRecipe=1. 편집중 번호변경을 UI가 허용하는지는 미확정이다.
3. 범위 밖이면 hmi_index=1. 이 호출 안에서 In_Range 재계산문은 없다. 번호를 고쳤다는 이유로 같은 호출의 버퍼복사·Load가 안전하게 완료된다고 단정하지 않는다.
4. 범위 안이고 번호가 이전과 같으며 버퍼≠저장본 AND Modify_Recipe일 때 SaveUndo=1, Vis_Modify/Vis_LoadRecipe=0. 표시비트가 곧 접근권한/안전인터록인 것은 아니다.
5. Vis_SaveUndo AND Save_Recipe이면 버퍼→선택저장본. SaveUndo=0, Vis_Modify=1, Modify=0, Save=0, Vis_LoadRecipe=1. **여기서는 Data8개에 쓰지 않는다.**
6. 별도의 다음 if에서 Vis_SaveUndo AND Undo_Modification이면 저장본→버퍼, 표시/Modify/Undo를 갱신한다. Save/Undo는 else-if 한 쌍이 아니다. 선행 Save가 SaveUndo를0으로 바꾸므로 동시 요청을 무조건 두 동작 완료라고 설명하지 않는다.
7. 버퍼=선택저장본 AND Vis_LoadRecipe AND Load_Recipe이면 §2.2의 Data8개를 대입하고 Active_Recipe=hmi_index, Load_Recipe=0. 이 조건문에는 In_Range가 직접 없다. 저장 직후 별도 Load 요청이 남아있을 때 같은 호출에 적용될 가능성도 원형 소스/이벤트 확인 없이 배제하지 않는다.
8. 마지막 oldhmi_idx=hmi_index. 전원 재기동 유지·저장매체 영속성·Retain의 증명이 아니다. 번호변경 분기에 Save/Undo/Load 요청을 모두 일괄 0으로 지우는 구문도 보이지 않는다.

### 3.2 FC21 호출과 ENO

0030-FlgNet.xml 문서1613/Main/NID19:
- Wire31 Powerrail→CRef21.en. CRef21 RID121/CodeBlock UID22 RID120;0688 FCBlock Recipes Handler TOD21 +0694 호출선언.
- Wire32 CRef21.eno→CRef23.en(HMI FC11), Wire33 CRef23.eno→CRef25.en(HMI Output FC19).
- Wire42 CRef25.eno→Contact37.in, Wire44 ORef45/RID140=Simulation(1)(0692 AO1440 Memory Bool, M180.0)→37.operand, 명시 Negated. Wire43 37.out→CRef28.en(HMI Inputs FC15).

이 부정접점은 레시피 호출 뒤 HMI Inputs 가지에 있다. 미실행 시뮬레이션 블록을 조사·수정·시험한 것이 아니라 허가 오독 방지를 위해 해당 접점만 정적 확인했다. ENO는 Data8개 적용 완료 ACK로 정의되어 있지 않다. FC21 내부 반환/예외 동작과 현재 호출주기는 미확정이다.

0032/문서1621/NID8은 ON Contact352.out의 Wire353가 Valve Control loop CRef341.en과 Analog output conversion CRef344.en에 병렬 연결된다. 후자0688 RID88/CodeBlock349/TOD18이다. 둘을 직렬 ENO 체인이라고 만들지 않는다. 0024/문서1723은 ON ORef185→188.operand, Wire189→CRef183.en/CodeBlock186 RID39(0067 Auto start motors FC30). 서로 다른 OB의 전체 실행/인터럽트 우선순위는 이 연결만으로 확정하지 않는다.

### 3.3 대표 복수 Writer·형식·범위

공통문맥:0460/0461/0463/0465/0466은 FC18, 선언0662 Global Data,0663 Local Prod_h/tmp,0664 ON/출력,0661 상수. RID는 이 블록 문맥으로만 사용한다.

|원본|독립 대조한 핵심 핀|해석·경계|
|---|---|---|
|0461 문서1680 NID2|ON Contact171→W172 Lt118/Gt126.pre. W155 Lt118.out→Move121.en, W158 121.out1→ORef143 RID10. W161 Gt126.out→Move129.en, W164→ORef147 RID10|SET_PERC_BWF01 Int를 <0일 때0, >100일 때100으로 직접 덮어쓴다. 0661 RID5=0/RID12=100. 레시피 저장본을 수정하는 것은 아님|
|0463 문서1682 NID4|ON316→W317 비교263/271.pre. Move266 W303→ORef288 RID30, Move274 W309→ORef292 RID30|BWF02에도0/100 쓰기. OFF Contact318은 별도 Mul280 경로에 있으며 클램프 전체의 허가가 아님|
|0465 문서1684 NID6|ON455→W456 비교406/414 및 Mul422. W441→Move409, W444→ORef430 RID43; W447→Move417, W450→ORef434 RID43|SET_PERC_FR01 Int <5→5, >100→100. RID44=5. Mul422 W451 입력 FR01/W452 상수272/W453→RD01_SP_SPEED Word(0664 RID48 AO2320)|
|0466 문서1685 NID7|ON506→W507 비교457/465 및 Mul473. W492→Move460/W495→ORef481 RID49; W498→Move468/W501→ORef485 RID49|SET_PERC_VT01 Int <5→5, >100→100. Mul473 W502/W503=VT01×272, W504→FN01_SP_SPEED Word(0664 RID53 AO2336). 현재 drive 스케일 보증 아님|
|0480 문서8 NID16|Powerrail W21→Lt22.pre, W27 ORef29 RID45 TC03_SETPOINT→in1, W28 ORef30 RID137 200→in2. W33→Move32.en, W34=200, W35→ORef37 RID45|TC03_SETPOINT Int<200이면200 직접쓰기; Move32 DisableENO=true. 원문상수이며 현행 보호설정/권장값 아님|
|0460 문서1679 NID1|Div21 W22 BWF01/100→W24 Local Prod_h; W30 21.eno→Mul29.en, Mul29.out W33→Prod_h. 비교108→W37 Mul159.en; W40 159.eno→Div39.en; W43 39.out→ORef46 RID10 BWF01|Local Prod_h Real을 Data2.Set_TH와 연산하고 처리량 제한 경로에서 비율 자체를 다시 쓴다. 자동형식 Div/Mul, Int 입력/Real 임시/LReal literal100.0 혼합을 고정 정수식으로 축약하지 않는다|
|0460 동일|Move107 W126→BWF01; Move169 W193→BWF02; Mul171.eno W199→Div172.en; W203 172.out→BWF02|음수 계산시0 및 처리량상한 기반 재계산 후보. DisableENO=true여도 배선 ENO는 존재하므로 삭제해 해석하지 않는다. 분모0/형변환·overflow의 실제 진단은 미확정|

0460의 BWF01 분모 Div39.in2는 W42의 Data2.Set_MAX_TH(RID7), BWF02 Div172.in2는 W202의 같은 멤버다. 분자 계산의 Set_MAX_TH1/2와 구별한다. Local Prod_h/tmp는 동일 FC 안에서 재사용된다. 이름이 같다는 이유로 다른 블록 Local과 결합하지 않았다.

**자동 단계·예열·건조 공유근거와 이번 대조:**
- 0164/문서1843 NID3: Eq472 Tempo_presetting=21의 W718→Move481, W720=25/W721→FR01. Eq521=30의 W745→Move530, W747=35/W748→VT01.
- 0165/문서1844 NID4: Eq820=35의 W1080→Move829 FR01=25(W1082/1083), Eq858=49의 W1104→Move867 VT01=35(W1106/1107). 단계허가 전체는 SYS-AUTO를 공유 참조하며 단순 무조건 쓰기로 설명하지 않는다.
- TC01=850/TC03=500 쌍의 Move568/573(0164 W771…774),912/917(0165 W1131…1134)도 존재하지만 바로 앞 Contact791/1151의 operand는 **비반전 OFF**다(W770/1130). ‘항상 초기850/500’이라고 쓰지 않는다. ON/OFF는 현재값 증명 없는 메모리 선언이다.
- 0169/문서1845 NID11의 Move60/65/70/74는 각각 timer58/63/68/72.Q로 enable(W126/137/148/156), HMI_DB의1~4단계 speed→Data.SET_PERC_VT01. Move78은 timer76.Q W164 뒤 상수15(W166)→VT01(W167). 선택 온도/예열조건 전체는 FN01/SYS-AUTO 공통근거 재사용이며 실제 타이머 경과시험 없음.
- 0190/0191/0192(문서1875…1877) 건조 TC01_SETPOINT 다중쓰기 네트워크도 원본 핀 추출에 보존했다. 이 셋의 모든 분기·조건은 이번 의미검토 범위가 아니다. BR01/TC01 공통근거 연결 후 현재 원형 소스로 최종 Writer 순서를 추가 확인해야 한다.
- 파생 recipe-settings의 LAD Writer 목록은 BWF01 4핀, BWF02 4핀, FR01 4핀, VT01 9핀, TC03 3핀, TC01 23핀이며 PSH01/02는 그 목록에서0이다. 이는 전체 SCL/HMI/온라인 Writer가0이라는 뜻이 아니다. 색인 SCL364는 이 LAD계수 밖의8개 쓰기다.

## 4. 전기 끝점·실제 PDF 범위

SYS-RECIPES 직접 기능은 DB26→DB1의 소프트웨어 전달이다. 전용 전원·릴레이·코일·터미널·케이블·물리접점 FG는 대장에서도 지정되지 않았다. 따라서 직접 끝점은 **기능경계상 비해당**, 주변 모터/센서 회로와 현재 실물 연결은 **별도 설비 근거/미확정**이다.

이번 고유 주장에 필요한 실제 PDF 렌더 페이지는0쪽이며 실제 열람도0쪽이다. 검토하지 않은 PDF의 footer/개정란을 본 것처럼 쓰지 않는다. 저장/적용 알고리즘과 DB 배치를 증명하는 자료는 XML/SCL원형/HMI프로젝트이지 임의 전기도면 페이지가 아니다. RD01/FN01 출력 후 전기 끝점, PSH01/02 및 TC01/03 센서/최종 제어요소는 각 고정판본 초안의 확인 페이지·개정란을 참조하고 SYS-RECIPES 완료로 중복 집계하지 않는다. 향후 물리 출력까지 사용자 요구가 확대되면 그 설비의 정확한 OEM/시공 PDF 페이지를 별도 지정하여 재확인한다.

## 5. 알람·복구

레시피 편집 오류 전용 알람·저장 실패코드·통신품질 경고·인덱스 예외처리는 이번 원형자료에서 미확보다. 표시비트 Vis_*를 알람 비트로 바꾸지 않는다.

관련되는 공급비율 알람은 독립 확인했다. 0541-FlgNet.xml/문서1993/NID15:
- ON Contact1227→W1228→BWF01 RUN Contact22→W24→BWF02 RUN Contact26→W28→Add1174.en.
- W1209 ORef1196(Data.SET_PERC_BWF01 RID122)와 W1210 ORef1197(BWF02 RID123) Int Add, W1211→Local Somma_Perc_alim(RID124,0685).
- Add1174.eno W1212→Ne1178.pre, W1213 합계/W1214 Int100(RID125,0683); Ne.out W1215→SdCoil1184 및 timer접점1229.
- W1216 상수RID175 `S5T#5S`, W1217 Tag_113 RID127 Timer AO50(0686, T50). 접점1229.out W1230→SCoil1189; W1220→Allarm.Formula_Fault RID128(0684 AO103, DB3.DBX12.7).
- 별도 ON 분기→Contact1231(Flag.RESET_ALLARM)→W1232→Contact1233(Formula_Fault)→W1234→RCoil1194, W1225→같은 Formula_Fault. 원인 소멸만으로 래치가 자동해제된다고 해석하지 않는다. 동일 네트워크 S/R 동시조건의 현행 스캔 결과·ACK 표시·최종 정지 영향은 SYS-ALARM/관련 모터에 연결하고 여기서 현장 복구를 확정하지 않는다.

이 알람은 RUN조건·현재 Data 비율 합계에 관한 경로다. ‘어떤 저장 레시피의 합계가100이 아니면 언제나 경보’ 또는 ‘레시피 Load 성공/실패’ 알람으로 바꾸지 않는다. 합계를 맞추기 위한 실제 설정 변경·리셋시험은 하지 않았다.

## 6. 증상별 관찰: 변경 없이 확보할 자료

|증상|관찰할 기존 자료/같은 시각 항목|구분 기준·추가 자료|
|---|---|---|
|저장했지만 운전값 그대로|HMI Save/Load 이벤트 로그, hmi_index/active_recipe, recipes[0]/선택 저장본, Data8개|Save 분기는 archive만 갱신. 버튼이 Load까지 요청하는지 현재 HMI 이벤트 필요|
|화면8개는 같은데 Load 안 됨|전체176bit Recipe 구조와 Spare3Word, Vis_LoadRecipe/Load_Recipe|8개 숫자 일치만으로 전체 동등비교 성공을 단정하지 않음|
|편집중 내용 바뀜|hmi_index/oldhmi_idx 변경시각, modify/표시비트, 편집버퍼 이전자료|선택변경 복사/Undo/외부Writer를 구분. 신규 번호·값 주입시험 금지|
|활성번호는 맞지만 값이 다름|Load 시각과 FC18 clamp/FC30 단계/FN01예열/BR건조 흔적, 현재Data|active_recipe는 연속 동등성 보증이 아님. 스캔/OB 우선순위와 온라인 추적은 별도 허가/자료 필요|
|범위밖 번호/CPU진단 기록|이미 남은 오류로그, 원형SCL, 배열선언, HMI 입력제한|범위검사 이전 참조·Load의 별도조건을 검토. 잘못된 번호를 넣어 재현하지 않음|
|저장/취소 요청이 남음|요청 Down/Up/펄스 정책, 번호변경, Vis_SaveUndo, 처리시각|조건이 만족될 때만0으로 소비하는 경로를 확인. 강제비트조작 금지|
|전원복귀 뒤 값이 달라짐|승인된 DB 시작값/Retain 설정/프로젝트 버전·기존 추세|백업 저장값과 당시 운전값·현행 보호값을 분리. 임의 전원사이클/재시작 금지|
|Formula_Fault 발생|BWF1/2 RUN 처리비트, Data 두비율, 합계, T50, RESET_ALLARM|SCL저장본/실제 설정/펄스실물 구별. 알람해제와 공정안전·재기동은 별도|

관찰기록은 관찰자·실제시각/시간대·프로젝트 식별·위치·값/단위·품질·버퍼/저장/적용/출력 구분·관련로그·복구증거를 보존한다. 여기는 수집 계획이며 실제 관찰·수리실적이 아니다. 운영기록/사진/SEJIN 데이터 복사 없음.

## 7. 완료·누락·자체검사

### 7.1 상태와 다음 필요한 자료

- documentation: complete_with_gaps, 한 ID의 자체 조사 초안. BC01 동등 UI구현·현장완료 아님.
- static_review: selected_source_crosscheck. SCL364/DB26·DB1 선언,17 HMI행,호출·대표Writer·Formula_Fault 핵심 대조. 16 XML 네트워크 추출은16개 전체 의미검토를 뜻하지 않는다.
- ui_records/not_run, publication/not_published, tia_compile/not_performed, live_cpu/not_performed, field_recovery/not_performed.
- 우선 필요: 줄바꿈/주석이 보존된 FC21 원형 SCL, 현행 DB26/Recipe UDT 전체 export·시작값/Retain, HMI recipe 화면 이벤트/권한/범위, 정확한 현재 OB호출/우선순위·타Writer 목록. 새자료 없이 보류 범위를 반복 조사하지 않는다.
- 현재CPU/프로젝트 동일성·컴파일·예외·보호한계·물리복구는 추가 자료 또는 별도 승인된 현장 검증이 필요하며 이 정적문서로 대체하지 않는다.

### 7.2 네 기능 및 기록보존

|기능|적용/검증 상태|
|---|---|
|도면·래더 비교|소프트웨어 선언/호출/SCL 대조는 적용. 전용 전기도면 페어 비해당, 현재 UI 구현/링크검증 미수행|
|백업·선택 복원|문서 관찰기록용 기능은 향후 적용 가능. 실제 PLC 레시피 복원과 별개, 저장/복원 실행 없음|
|전후 기록 비교|편집·저장·적용을 나눈 기록 형식에 적용 가능. 실제 기록 작성/전후검증 없음|
|보고서/PDF|이 MD가 전달자료. 사용자 보고서/PDF 생성·렌더 미수행|

기존 note/repair_observation·미지필드·타설비·초안·저장키를 변경하지 않았다. 자체추출 Python은 XML/CSV 읽기·근거해시·문서검사만 하며 원본 생성기를 실행하지 않는다.

### 7.3 작업 실제시각 및 검사 기록

- 2026-10-11 11:56:38 UTC 착수, 배치 지시/범위 읽기 시작.
- 11:56:46 UTC Git HEAD/원본 상태·표준/대장/현황 및 고정판본 확인.
- 11:57:22 UTC DB26 배열/주소 선언 발견, 11:57:33 UTC 선언 추출 저장.
- 11:58:35 UTC 16개 XML 핀/17개 HMI 태그 자체추출. 이후 UID/NID/RID만 맞는 타블록 후보가 섞이는 위험을 발견해 선언 블록 문맥 필터를 추가하고 재추출했다. 잘못된 후보를 의미근거로 채택하지 않았다.
- 12:00:12 UTC 호출·클램프·OFF 조건·Formula_Fault·배열구조 독립대조 및 57개 선정파일 Gitblob 비교 완료. 최종검사 시각/결과는 아래 부록과 self-check.json에 기록한다.

## 부록 A. 선정 원본 SHA256 / 고정 Git blob 전체 목록

다음은 이번에 선택한 원본/파생색인/작업표준 파일의 바이트 보존 목록이다. **파일 수는 의미검토 수가 아니다.** 원본 XML의 핵심검토 범위는 본문에 한정했고, 파생 recipe-settings는 탐색용이며 실행증거로 쓰지 않았다. 각 경로는 고정 원본 저장소 상대경로. 모든 행은 현재파일과 고정커밋 Git blob 내용이 같음을 확인했다.

|원본 상대경로|SHA256|고정 Git blob|내용 일치|
|---|---|---|---|
|.agents/skills/gme-equipment-rollout/SKILL.md|fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b|9aa820ea6ca15b4e136c9772423b78ed4df6a3d4|yes|
|AGENTS.md|0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2|073164bc6efd5791032d62c71b03b4dab48cb6f8|yes|
|all-in-one/registers/recipe-settings.json|ff920bfff996cd4fe9eaff4789593cbd30f2a9252c88bf1cb48a148a96a4d81c|e708735df32342e89fad3ce8e5d17bd08371a409|yes|
|all-in-one/sources/block_summary.json|68253f9366908244a27ed461c66d465da7ec1723571f27deaa9a6f81a542de63|15b570a011645023dbfca2d5332a9e0ae3b0a7b6|yes|
|all-in-one/sources/decoded-original/0024-FlgNet.xml|a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67|379ccbabf7692e1df137b99bab1992dea22cc1f0|yes|
|all-in-one/sources/decoded-original/0030-FlgNet.xml|9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b|e74c70b751acdcdbc7a8b3b0c98aa773c2107cab|yes|
|all-in-one/sources/decoded-original/0032-FlgNet.xml|070bb8efa33d03b18add5da81d3f670a47c12b288076b7bfee11ac87fe6fa7e4|e31cf9aeecfbfc0c264921ac217cbd15479c1f34|yes|
|all-in-one/sources/decoded-original/0066-IdentXmlPart.xml|13ff943033934043bb50d38d95e46706443a12b1eef70471cb0f35d3b0ade402|55adec8d054eb4d3b186c6498616457ad254c22f|yes|
|all-in-one/sources/decoded-original/0067-IdentXmlPart.xml|0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628|455f00638f1618f194b1c83d9c0c2f157663a902|yes|
|all-in-one/sources/decoded-original/0164-FlgNet.xml|15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491|1035a51ee3100d524da1b7b204ba142b6b509ac5|yes|
|all-in-one/sources/decoded-original/0165-FlgNet.xml|4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88|8d636eb535060037ccf00ebdfb328b8775225fe4|yes|
|all-in-one/sources/decoded-original/0169-FlgNet.xml|c11893dfee800efa2649b14cd4bab9c94e018ce690168f060526c3249f50da10|9b3d8e50d69f96265e573fa1d4a124b7e59884be|yes|
|all-in-one/sources/decoded-original/0190-FlgNet.xml|46722388ab7f69c14436e64051b0bb0c720ba1878b9652c4b859fdb4ddb0bf25|851ee4680f7a05c41c79f841a8429560bb361f5a|yes|
|all-in-one/sources/decoded-original/0191-FlgNet.xml|28f087b14ff3a0a0f5bcb20e212c41357ad36caf3c8308f8019f4b78d60eb7bd|df4dce76c1db53fe0e9cd2979044397f4fa56d10|yes|
|all-in-one/sources/decoded-original/0192-FlgNet.xml|874a8e7d6208c568027f4b03fb0e5e085be7e79b914db9dbef30a43d200ee1d2|405a401e2162d732b6cb9f81f2fb411557419b47|yes|
|all-in-one/sources/decoded-original/0460-FlgNet.xml|3e8655935bad9105b42565da363af4f405b0f5b0ff9876d068bd1098b5efae47|886be3bb0396826a8b5960ab3703f840034c240b|yes|
|all-in-one/sources/decoded-original/0461-FlgNet.xml|50bdf21c978cb87d2b9048aaeb427dee393365d2dc0ec2661dc6e0c57f91b95c|7b5fe95f86385113020b473cbca14f42626f4678|yes|
|all-in-one/sources/decoded-original/0463-FlgNet.xml|ed64a900253f8548cd9e9b41db84bdb323f87f61ff1a03da31e48523dba18b56|f6fc1f4fb19d8744e476ee2b863750bfcf794a9a|yes|
|all-in-one/sources/decoded-original/0465-FlgNet.xml|6f48f2b9fc031e4dcef47cff8c9b56e2fbe67fd1802aac999b95836dd9a7458a|36eca861d9668e52c667e4b1a0e3dc552a3310dd|yes|
|all-in-one/sources/decoded-original/0466-FlgNet.xml|4e4461435e68831cab0be6171c58c8f25803a5f3da811001a73ae0bd3fe43e61|742543974e8feb350ce0432acd5c09435f02367f|yes|
|all-in-one/sources/decoded-original/0480-FlgNet.xml|c14d2fee14b38b7c597edb46626676f0cf550b5831668884cb2fac341b559273|d17dfbf4a5e25e09c25b13721d6a81636ad62ad9|yes|
|all-in-one/sources/decoded-original/0541-FlgNet.xml|12c952b45816909fab975cdac62939d8aa4c20682f3499c450e88050458f7dfb|b13b96c06e49205babdc608d7c52515172eb9929|yes|
|all-in-one/sources/decoded-original/0553-IdentXmlPart.xml|4bf2f2c613e81ee6bd92ac0f21252ea0ce4a1135818fcc404740a914aaae1317|ec2344a9d25560ef4d6e53951804ceaf21326c1d|yes|
|all-in-one/sources/decoded-original/0554-IdentXmlPart.xml|4ae3e7d0bca0f78c9e94617abeb70bdd228d85d74bff2224174fa1bb0076e78c|cdb68b35a7287f6b5636c01ea3a01747d3d60e81|yes|
|all-in-one/sources/decoded-original/0575-IdentXmlPart.xml|40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06|07d5d2548e8f36252a346d0b83341e27c3cb14ba|yes|
|all-in-one/sources/decoded-original/0576-IdentXmlPart.xml|c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe|819b47160eaa6d08c212f71e5b5486ef5b55b6f2|yes|
|all-in-one/sources/decoded-original/0577-IdentXmlPart.xml|511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47|a505ebf7efd05a85850dc29559a4f71242bacae3|yes|
|all-in-one/sources/decoded-original/0578-IdentXmlPart.xml|0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b|070a79fb12139898dd44a17ab2061e795956b9c6|yes|
|all-in-one/sources/decoded-original/0579-IdentXmlPart.xml|ee35cf525388f2b38399787caef57a978b0bb17216a90e1a90ac4391e0e799fe|19d1039319ffeb150767d96fc36205326483b1c4|yes|
|all-in-one/sources/decoded-original/0580-IdentXmlPart.xml|fa748a6c1890f579d694fd5e561b2304f717da79e5352ca32152cc20e877c6ff|9bd503f23708fada1a1f871e0e52b0eb75e9aacf|yes|
|all-in-one/sources/decoded-original/0582-IdentXmlPart.xml|41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951|82636dec064876d0f4cc714ef385b07d6e05efe0|yes|
|all-in-one/sources/decoded-original/0585-IdentXmlPart.xml|e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184|16574d37ef3ca61b59ba396c400e269ab1dd3440|yes|
|all-in-one/sources/decoded-original/0586-IdentXmlPart.xml|f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250|266989c590cf52f82e1553f8626a209b8c0b6e0b|yes|
|all-in-one/sources/decoded-original/0640-IdentXmlPart.xml|2873e2c70eb4ce97c104b00b675c8f800a3ab9621f9d382718428d2d82025379|5b899bd63cac30e700a26932a3ffe889ecad8769|yes|
|all-in-one/sources/decoded-original/0641-IdentXmlPart.xml|75c1f81d659331b8b62578f766e2f0336276caaf086201fdc383e61c195d01df|341bca78929061ab73560dd85fef3f4000127782|yes|
|all-in-one/sources/decoded-original/0642-IdentXmlPart.xml|c922483c261c8ddb98c239a7b4dc3d7f73f9a45261dd5b4d669f39d6918a1c21|398f73b99c4a792a68387485fcb47048d166b2a1|yes|
|all-in-one/sources/decoded-original/0643-IdentXmlPart.xml|ce7ff35daa71ee1728f4e7b5ac3234d0a31a3c71e953021e9c1f9a953783b6cb|84b3cfa219e1e1650664f02a67403b8b0e52654e|yes|
|all-in-one/sources/decoded-original/0652-IdentXmlPart.xml|251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692|eee49f8301a6791748de9ab368159af8e8bc1585|yes|
|all-in-one/sources/decoded-original/0660-IdentXmlPart.xml|0bf4f4c46531f55324602f4f7b1a1e0b9e63df2c6278126f6e5cf1bc9a06509f|915de9b3f968310c45682bef86a91adc1fa06e75|yes|
|all-in-one/sources/decoded-original/0661-IdentXmlPart.xml|90672199fee355011f581d3287046894772f3f3b4cb78bbe0dd0d71bd488ac93|cea3653088f8fb5c77afcf715988039cb63e28ac|yes|
|all-in-one/sources/decoded-original/0662-IdentXmlPart.xml|1838040bfee800fdb3f13b126eaf69a9d178b17cecc0d59ae03e9185216a48a5|ba624f3460dc05e8ade4956cdfc2ec621edb4f73|yes|
|all-in-one/sources/decoded-original/0663-IdentXmlPart.xml|d3980b88d3cd3e49854439d0778c58ed131bae46a6bc3e65ab70e81f766ac03d|3051de9b670457991223a08c03f785747e687414|yes|
|all-in-one/sources/decoded-original/0664-IdentXmlPart.xml|68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed|7ce2f1315d5a21d6b77869a59fc9fcb2f17e90e6|yes|
|all-in-one/sources/decoded-original/0666-IdentXmlPart.xml|19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6|b6130b32498b6fee0d9e4db7a04dc79f785e1fbb|yes|
|all-in-one/sources/decoded-original/0667-IdentXmlPart.xml|ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3|7f2e1798eb9f260d19d038a83369484d0f438856|yes|
|all-in-one/sources/decoded-original/0668-IdentXmlPart.xml|2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed|fe0f30d1eaae37783b0f03cb090353b3a3de3600|yes|
|all-in-one/sources/decoded-original/0682-IdentXmlPart.xml|25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092|61182411e912941161eccf4e90c1f174e5379f0a|yes|
|all-in-one/sources/decoded-original/0683-IdentXmlPart.xml|0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22|662acdb9a06c0ba1c0027e7dd215a28f07d3f02b|yes|
|all-in-one/sources/decoded-original/0684-IdentXmlPart.xml|6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208|d67b98b5d5516e0330aae5cfdbee41a3e09206e1|yes|
|all-in-one/sources/decoded-original/0685-IdentXmlPart.xml|2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448|86bda988d9efedba92ba2f3e4877497d9eb5230a|yes|
|all-in-one/sources/decoded-original/0686-IdentXmlPart.xml|b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4|8c152d926692a8e15973c980e08e338d29411814|yes|
|all-in-one/sources/decoded-original/0688-IdentXmlPart.xml|ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda|463585759f1ecd94f32362b4fefb000a152f5773|yes|
|all-in-one/sources/decoded-original/0692-IdentXmlPart.xml|bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037|737785d03b5fad43c5b4d451955726d800edb1c0|yes|
|all-in-one/sources/decoded-original/0694-IdentXmlPart.xml|757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d|c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d|yes|
|all-in-one/sources/decoded-original/network-map.json|c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60|424430b6b953e43138e5d0a18ca40c949e21cfa1|yes|
|all-in-one/sources/hmi-windows.csv|15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e|8401dcfe5ba3e7e244eea0f501bb84a2e387da39|yes|
|all-in-one/sources/hmi_plc_tags.csv|a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404|cf4c0650e7c7baac350dcb89909b808435704880|yes|
|all-in-one/sources/live_index.json|14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1|e35ccea1f841349c632666c29954b7bcd4f5839e|yes|
|docs/equipment-standard/INVENTORY.json|720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc|587c3748ad9224718f95ba06463fee913dae231d|yes|
|docs/equipment-standard/WORK-ITEM-TEMPLATE.md|4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586|e546f39535d2b589e80f97db869ac37ce4d05cfd|yes|
|docs/equipment-standard/WORK-STANDARD.md|05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99|f76a570cc73098632e08759b17934000f7e3a253|yes|
|docs/equipment-standard/work-items/FN01.md|9839f61918970377ce55ad12238fd7efaa99d1507a17f593ce0aeb6a696a69cd|0f0b5ac077a1e39f5eb2551cc6584b5ba0f31378|yes|

## 부록 B. 최종 자체검사

- 실제 완료시각: 2026-10-11T12:05:45.044260+00:00 UTC.
- 선정62파일 SHA256 재확인·고정 Git blob62/62 내용일치·고정 HEAD·원본 Git clean 확인.
- 자체 문서검사13항목 모두 통과: 7영역·공유링크·17 HMI태그·16 XML추출·SCL원문해시·8개Data대입·배열/Local선언·MD62해시행 검산.
- 처음 링크 검사에서 FN01 초안 링크가 없음을 확인하고, 실제 존재하며 같은 고정판본인 FN01 작업기록으로 정정·읽기·재검사했다. 선언 UID 문맥 후보 혼합도 필터 후 재추출했다. 실패 기록을 숨기지 않고 해당 수정사항을 self-check.json에 남겼다.
- 검사 JSON: `extracts/SYS-RECIPES/self-check.json`; 해시 JSON: `extracts/SYS-RECIPES/source-hashes.json`. 전수 프로그램 의미검토·TIA컴파일·현재CPU·UI/기록·배포·실제레시피/현장복구 검사가 아니다.
- 후속 단계는 원형 FC21/DB26/HMI 이벤트 자료 확보 후 미확정 범위만 대조. 현재 승인범위에서 추가 변경이나 시험 없음.
