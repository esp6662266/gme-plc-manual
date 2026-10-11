# BF01 백 필터 본체·세정 공통 제어 원본 조사 초안

BF01의 `BF01_RUN`은 세정 허가에서 쓰는 내부 비트 `%M180.3`이다. 물리적인 필터 운전접점이나 세정 밸브의 실제 동작 확인 신호로 확인된 것이 아니다. 허가 원문은 SC10·VR04 처리응답을 직렬로 요구하고, 그 뒤에서 `DP_01 <= DP_01_SOGLIA_1 OR Forza_Lavaggio`를 검사한다. Forza에는 2시간/10분 타이머 이외의 **별도 ON OR 가지**가 있다.

세정 공통 Word는 BF01/BF02가 공유하며 OFF 조건의 분기 쓰기 외에 ON 조건의 시간·범위 쓰기가 있다. 따라서 이름이나 한 네트워크만으로 현재 활성 모드·최종 Word·세정 간격을 결정하지 않는다. DP 범위고장과 두 필터 공통 차압 경보, HMI 설정 주소, JB1 전원·대표 펄스 출력·DP01 입력의 양 끝점을 추적했다.

이 문서는 작업3 자체 cloud 추가조사의 BF01 한 개 초안이다. SC10·VR04·DP01·TC09·PV14·FN04의 별도 완료를 선언하지 않으며, BF01 하위 EV11~EV50 40개는 기존 작성 제외 상태를 유지한다. 로컬 2차133 통합, UI/기록 기능, 게시, TIA 컴파일, 현재 CPU·실물·현장 복구 완료가 아니다.

## 작업 기준과 보존

- 표준: GME-STD-1.0.0. 대상 catalog_id BF01, filter, 집진·석회, parent 없음, depth0, priority_key 없음. INVENTORY catalog[88], equipment[48]. 문서상 phase2 후보이며 완료 실적이 아니다.
- 범위: `progress/TASK3-BATCH04-SCOPE.json`의 네 번째 묶음 MC03/MC05/LD01/BF01/BF02 중 BF01. 고유 ID·별칭 충돌·기존 제외를 대조했다. 로컬의 2차133 제외는 유지한다.
- 고정 읽기 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION 1.12.0. 저장소 `https://github.com/esp6662266/gme-plc-manual`. 현재 main/현재 CPU/현행 시공과의 동일성은 미확인이다.
- AGENTS, EXPANSION-WORK, VERSION/WORKSPACE-HANDOFF/PUBLICATION_STATUS/ACTIVE-WORK 최신 머리말, `gme-equipment-rollout/SKILL.md`와 source-map, WORK-STANDARD/WORK-ITEM-TEMPLATE/INVENTORY/START-GPT61을 읽었다. 기존 SC10/VR04 초안은 탐색용으로만 사용하고 본문 핵심은 고정 원본으로 재대조했다.
- 읽기 전용 preflight 종료0, inventory_matches=true. 전체248/우선23/우선대응18/기존 제외90/제외 부모 하위 보류7/phase2 후보133. requirements-audit.json·all-in-one-data.json의 source_byte_changes는 대장 생성 시점과 고정 버전의 바이트 차이이며 이번 조사에서 갱신하지 않았다.
- 조사일 2026-10-11 UTC. 작성자 BF01 원본 조사 작업자. 실제 모델명·추론 설정의 런타임 증명은 미확보다.
- 쓰기는 `drafts/BF01-DOTS-DRAFT.md`와 `extracts/BF01/`뿐이다. source 원본·공용 declarations·타 설비 초안·공통 코드/버전/대장/배포/운영 기록 변경0. 시뮬레이터 작성·수정·생성·실행·행동시험0, 실제 PLC·현장·보호값 및 SEJIN 자료 변경0.

이하 경로는 고정 저장소의 `all-in-one/` 아래다. 4자리 XML 약칭은 `sources/decoded-original/<번호>-FlgNet.xml` 또는 명시된 `<번호>-IdentXmlPart.xml`이다. LAD는 document_id, NID는 원본 네트워크 번호로 서로 다르다. 파생 색인·CSV·검색 원문은 탐색/보충으로 구분하며 XML Part/Wire/ORef/CRef와 선언 RID/NID/UID·형식·주소를 핵심 근거로 삼았다.

## 7영역 적용표

| 영역 | 적용 상태 | 이번 확보 범위 | 남은 확인 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | 고유 BF01, 별칭 충돌, 독립 설비·제외 EV·공유 JB1의 경계, 판본 | 현행 본체·백/케이지 사양·실물 동일성 |
| I/O·HMI | 적용, 일부 미확보 | M180.3, DB1/3/4/13, IW398:P, 세정 타이머, HMI10주소 | 현재값·HMI 이벤트/단위 스케일·쓰기 권한 |
| 제어 구조 | 적용 | 허가·Forza·공유 시간/범위/카운터·호출·Word 쓰기 | 현재 호출 순서·ENO/리텐션·간접/외부 Writer |
| 전기 전달 경로 | 적용 | 전기12쪽, 시공3쪽, P&ID1쪽 실제 렌더; 전원/대표 펄스/DP 양 끝점 | 모든 제외 EV별 회로 완료는 아님; 준공/현장 단자 |
| 알람·복구 | 적용, 경계 분리 | DP01 OFR, 두 필터 공통 3분 차압 경보, Word 경보전달 | 실제 표시·소리·원인 제거·안전 재요청·복구 |
| 증상별 수리 | 적용, 관찰 지침 | 상태→비교점→원인 배제→필요 증거 | 실제 점검·조치·운전시험 없음 |
| 완료 기준 | 적용 | 누락자료·네 기능·정적/현장 상태 분리 | 독립 검토·제품통합/UI/게시·TIA/CPU/현장 |

## 1. 본체와 소유 경계

1. `registers/equipment.json` BF01 별칭은 pr_bf01/pr_br01/bf_01/filter 1이다. DP01에도 pr_bf01 별칭이 있다. 따라서 PR_BF01이라는 PLC 변수명을 BF01 본체의 독립적인 물리 입력으로 이중 집계하지 않는다. BF02와 이름이 같아도 서로 다른 catalog ID다.
2. P&ID `PID_1684n002I.pdf` p1의 BF01 확대에서 본체 하부 SC10/M34, 출구 VR04/M38, DP01, 상부 EV11~18/19~26/27~34/35~42/43~50, 공통 배출측 FN04→CM01을 구분했다. SC10·VR04는 catalog parent가 비어 있는 독립 모터다. 도면의 공정 연결을 catalog 부모나 완료 상속으로 바꾸지 않는다.
3. EV11~EV50은 INVENTORY에서 parent_id=BF01, phase=excluded, 사용자 제공 작성 제외인 40개다. 아래 출력 인터페이스의 구조 확인은 BF01 공통 제어 설명용이며 개별 EV 매뉴얼·수리·현장 확인 40건 완료가 아니다. EV08/09/10을 만들지 않는다.
4. DP01/TC09/PV14/LD01/FN04도 독립 catalog ID다. BF01의 넓은 FG152~180B 묶음에는 DP02, LD01, PV14, FN04, ER01, 예비 채널까지 들어 있다. FG 범위 전체를 BF01 전용 제어 소유로 해석하지 않는다.
5. P&ID 도번1684n002, 원작성06/04/2011, 판I 변경15/01/2013이다. 상부 AIR 6–8 Bar, DP01 표기 Setpoint 5÷10 mbar, 유입 Max180°C·TC09 Open170°C/Close160°C는 **그 도면 시점의 표기**다. 현행 안전 한계·PLC 계수·현장 압축공기 설정으로 채우거나 적용하지 않는다.
6. 백 재질·수량·길이/면적, 케이지/씰/교체품, 차압계 현행 제조사/모델/교정, 분진 특성·방폭·화재 대응·안전정비 주기는 확보하지 않았다. 주변 모터의 명판이나 타 필터 수치를 복제하지 않는다.

## 2. I/O·저장부·HMI

### 2.1 직접 선언과 주소

주소는 선언 SSD.AO/AOS.BO와 SAD 영역, BAD→DepDBBlock.TOD로 대조했다. 현재 CPU 주소·초기화·최적화 DB·통신과의 일치까지 확인한 것은 아니다.

| 신호 | 형식·주소 | 선언 위치와 직접 용도 | 경계 |
|---|---|---|---|
| BF01_RUN | Bool %M180.3 | 0594 RID341 AO1443, NID29 UID75 Write; live_index doc902 | 세정 허가 미러, 물리 응답 아님 |
| Forza_Lavaggio | Local Bool BO34 | 0598 RID57, NID3 UID437 Write/NID29 UID39 Read | FC Filter Local, HMI 물리 입력 아님 |
| Abilita_lavaggio_BF01 | Local Bool BO32 | 0598 RID63, NID29 UID40 Write, NID4 UID23 및 NID10~17 Read | 세정 허가, 실제 공기 분사 증거 아님 |
| SC10 처리응답 | Bool DB13.DBX5.0 | 0596 RID304 AO40 BAD303→0595 Inputs TOD13; NID29 UID35 | 원시 I5.0과 별도 저장부 |
| VR04 처리 Run | Bool DB13.DBX5.5 | 0596 RID318 AO45, NID29 UID36 | 접촉기 응답 전달, 실제 분진 배출 아님 |
| SC-10_Fbk/SC-11_Fbk | Bool %I5.0/%I5.1 | 0594 RID62/64 Input AO40/41; NID6 UID572/578,575/579 | Data.LAVA 쓰기는 처리 비트 대신 원시 입력 사용 |
| PR_BF01 | Int %IW398, 원문 :P | 0678 RID295 Input AO3184, SAD.SAM=Peripherie; NID40 UID1544, doc1523 | DP01 아날로그 원시값, BF01 별칭과 구분 |
| Data.DP_01 | Int DB1.DBW240 | 0676 RID298 BO1920 BAD11→0674 Data TOD1, NID40 UID1547 Write; 0596 RID6/0684 RID114 Read | 환산 결과. 승인 단위·현재값 미확인 |
| Coeff.ZERO_DP01 / COEFF_DP01 | Int DB4.DBW116 / 118 | 0676 RID297/451 BO928/944, BAD8→0674 Coeff TOD4, NID40 UID1546/1545 | 계수/제로는 보호값 변경 대상 아님 |
| DP_01_SOGLIA_1~4 | Int DB4.DBW138/140/142/144 | 0596 RID8/15/19/23, BO1104/1120/1136/1152 | 1은 BF02 허가에서도 읽힘 |
| DP_01_PAUSA_SOGLIA_1~5 | S5Time DB4.DBW146/148/150/152/154 | 0596 RID10/17/21/25/28, BO1168~1232 | 1은 KF_KT KT가 다시 씀 |
| DP_01_LAVORO_SOGLIA_1 | S5Time DB4.DBW156 | 0596 RID13 BO1248, NID25 UID52 Write | 0198의 5단계 모두 이 동일 LAVORO_1을 읽음 |
| Data.VALVE_W / VALVE_P | Int DB1.DBW318 / 320 | 0596 RID291/290 BO2544/2560, NID25 UID34/25 | KF_KT 입력. HMI 설정 있음 |
| Data.LAVA | Int DB1.DBW230 | 0596 RID68 BO1840; NID6 UID571/574/577/581 Write | OFF 아래 네 Move, 출력명령 자체가 아님 |
| LAVA_START / LAVA_END | Int DB1.DBW232 / 234 | 0596 RID76/78 BO1856/1872; NID7 네 쓰기씩 + NID8 별도 쓰기 | 공유 카운터 범위, 최종값 순서 주의 |
| LAVA_PAUSA / LAVA_LAVORO | Word DB1.DBW236 / 238 | 0596 RID11/14 BO1888/1904; NID1·2·4 복수 Write | 시간 형태는 S5Time 입력과 구분; raw Word를 ms로 오독 금지 |
| Ev_filter_on | Int DB1.DBW170 | 0596 RID3 BO1360; NID27 UID34/38/42 Write | 공유 단계 번호, EV 태그 번호와 다름 |
| Tag_129 / Tag_130 | Timer %T133 / %T134 | 0594 RID53/55, NID3 | 10분/2시간 회로. Tag명이 HMI 태그라는 뜻 아님 |
| Tag_131 / Tag_132 | Timer %T1 / %T2 | 0594 RID60/61, NID4 | 작업/휴지 시간 공통 회로 |
| PLS 50 3 | Bool %M50.3 | 0594 RID89 Memory AO403, NID27 UID31 RW | PBox 경계 저장비트 |
| ON / OFF | Bool %M0.0 / %M0.1 | 0594 RID52/1 Memory AO0/1 | 문자열만으로 현행 상수 TRUE/FALSE로 취급하지 않음 |
| BF01_OFR | Bool DB3.DBX24.3 | 0676 RID426 AO195 BAD354→0674 Allarm TOD3, NID40 UID23 Write | DP01 환산 함수의 Out_of_range 연결 |
| MAX_DP_FILTER | Bool DB3.DBX9.5 | 0684 RID119 AO77 BAD10→0682 Allarm TOD3, NID14 UID1165 Set/1172 Reset | DP01/DP02 공유 알람 |
| Tag_112 | Timer %T114 | 0686 RID118 AO114, NID14 UID1163 Write/1164 Read | MAX_DP_FILTER의 S5T#3M |

### 2.2 원시 입력과 Word 전달

- LAD1070 `0397`, NID1: Move35의 in←ORef36/RID10(W39), out1→ORef37/RID11(W40). 0627의 Tag_180=Word Input AO32와 0629 RID11 Word AO32/BAD4, 0628 Inputs TOD13을 대조하면 **IW4→DB13.DBW4**다. SC10 I5.0, VR04 I5.5가 그 워드 범위에 포함된다.
- Move35.en은 앞 Move27.eno(W41) 뒤며 DisableENO 속성도 있다. 선·속성 확인과 현재 매 스캔 실행 보증은 다르다.
- main LAD1613 `0030` NID19의 Recipes Handler→HMI→HMI Output ENO 연쇄(W31~33) 뒤에 NOT Simulation(1) 접점37(W42/44), 그 out→HMI Inputs CRef28.en(W43)이 있다. 호출 식과 현재 활성 여부를 분리한다.
- 0635에는 SC10 처리응답 RID124/NID4 UID42 Write, VR04 처리응답 RID132/NID4 UID63 Write가 추가로 있다. 이는 중지된 simulation 블록의 Writer 선언 존재 확인에 한정했다. 해당 프로그램 실행·활성화·행동시험을 하지 않았다.
- HMI Output LAD356 `0401`, NID1은 Move28의 in←ORef45/RID38 Tag_286(W72), out1→ORef46/RID55(W74), rail→en(W21)이다. 0632의 Word/Output AO96, 0633의 Word AO96/BAD26, 0064 Output TOD14에 따라 QW12→DB14.DBW12로 명령을 읽어 미러링한다. 물리 출력의 독립 Writer 또는 실제 밸브 피드백으로 세지 않는다. BF01 본체를 별도의 Q 한 점으로 만들지 않는다.

### 2.3 HMI 주소·화면과 미확정 이벤트

`sources/hmi_plc_tags.csv`에서 이름 검색에만 의존하지 않고 위 주소를 대조하여 10행을 확인했다. Access Name은 모두 PLC, 근거 문구는 `dde.cfg 설정; 온라인 현재값 아님`이다.

| CSV행 | HMI 태그 | 설정 주소 | 내부 ID | 연결/한계 |
|---|---|---|---|---|
|20|BF01_RUN|MX180.3|00456|허가 메모리 주소 일치, 실물 운전증거 아님|
|218|data_DB1_DBW170|DB1,INT170|002BF|공유 active step 후보 주소|
|256|data_DB1_DBW240|DB1,INT240|0028A|DP01 환산값 주소|
|297|data_DB1_DBW318|DB1,INT318|00255|VALVE_W 입력 가능 주소|
|315|data_DB1_DBW320|DB1,INT320|00242|VALVE_P 입력 가능 주소|
|360|Coeff_DB4_DBW116|DB4,INT116|00206|ZERO_DP01 주소|
|361|Coeff_DB4_DBW138|DB4,INT138|00205|DP01 문턱1 주소|
|382|Coeff_DB4_DBW118|DB4,INT118|001E7|COEFF_DP01 주소|
|535|Allarmi_78|DB3,X9.5|0013F|공유 MAX_DP_FILTER 주소|
|783|Allarmi_233|DB3,X24.3|00025|BF01_OFR 주소|

- `assets/HMI_DECOATER.png` 실제 정지 이미지는 상단 2026-10-07, 오른쪽 BF-01 OUTSIDE/BF-02 INSIDE, DP-01/02 단위 mb, ACTIVE STEP CLEANING FILTER 32, SC10/VR04 등을 표시한다. 이 이미지의 0.0/32 값은 그 화면 캡처에 있는 숫자이며 현재값이나 새 온라인 관찰이 아니다.
- 32라는 단계는 아래 공통 인터페이스에서 BF02 측 출력과 연결되는 번호다. `active step 32=BF01 EV32`라고 읽을 수 없다. 화면 표시가 실제로 어느 태그에 바인딩됐는지와 색상/클릭/권한/단위 소수점 스케일/쓰기 이벤트는 원 프로젝트 자료가 없다.
- `registers/hmi-window-provenance.json`도 원 WindowsInfo.json·screen events가 이 작업공간에 없고 current_hmi_verified=false라고 명시한다. 태그 CSV·정지 화면으로 실제 버튼의 Write 또는 알람 문구·우선순위·음성 동작을 완료 처리하지 않는다.
- 이 CSV에서 LAVA DB1W230~238, Coeff 시간 Word146/156의 직접 동일주소 행은 찾지 못했다. 다른 화면·간접 접근이 없다는 뜻은 아니다.

## 3. 세정 공통 제어

### 3.1 타이머 이외 ON 가지가 있는 Forza

LAD1885 `0200`, NID3, 0594/0597/0598 선언:

1. ON Contact451, ORef429/RID52, W438/459; out W452에서 네 가지가 갈라진다.
2. NOT Tag_129 Contact453, ORef431/RID53(W440), out W454→SdCoil418.in. value ORef430/RID54(W439), `0597` S5Time 원문 S5T#2H(SV=S5T_x0023_2H,V14112); operand ORef432/RID55(W442)=%T134 Tag_130.
3. Tag_130 Contact455, ORef434/RID55(W444), out W456→SdCoil423.in. value ORef433/RID56(W443), S5T#10M(SV=S5T_x0023_10M,V9728); operand ORef435/RID53(W446)=%T133 Tag_129.
4. Tag_130 Contact457, ORef436(W447), out W458→OR21.in1. 별도의 ON Contact460, ORef461/RID52(W463), out **W22→OR21.in2**.
5. OR21.out W23→Coil428.in; ORef437/RID57(W449)=Local Forza_Lavaggio.

정적 분기식은 ON 아래 `(Tag_130 OR ON)`이다. ‘2시간 만료에만 Forza가 켜진다’는 설명은 두 번째 OR 가지를 누락한다. 타이머의 현재값·기동 리텐션·FC호출·스캔 간 상태와 실제 시간을 시험하지 않았으며 V14112/9728을 ms로 읽지 않는다.

### 3.2 세정 허가, ≤ 방향 및 직렬 응답

LAD1886 `0219`, NID29:

- ON21(ORef34/RID52,W48)→SC10 처리접점22(ORef35/RID304,W50)→VR04 처리접점23(ORef36/RID318,W52), 전원 W47/49/51.
- 23.out W53이 Le24.pre와 Forza Contact25.in을 같이 허가한다. Le24.in1=DP_01 ORef37/RID6(W54), in2=DP_01_SOGLIA_1 ORef38/RID8(W55).
- Le24.out W56→OR26.in1; Forza25(ORef39/RID57,W57).out W58→OR26.in2.
- OR26.out W59→Coil27, ORef40/RID63(W60)=Abilita_lavaggio_BF01. 그 Coil.out W72→Coil74, ORef75/RID341(W73)=BF01_RUN.

따라서 `ON AND SC10_processed AND VR04_processed AND ((DP_01 <= SOGLIA_1) OR Forza)`다. 비교를 관행에 맞춰 ≥로 바꾸지 않는다. Forza가 SC10/VR04의 선행 응답을 우회하는 것도 아니다. BF02 병렬 가지는 SC11·VR05·DP02를 쓰되 비교의 Coeff는 동일 **DP_01_SOGLIA_1**(ORef44/RID8,W66)이다. 공유 의존성은 기록하되 BF02 완료로 집계하지 않는다.

### 3.3 KF_KT 호출·고정 시간 쓰기와 공통 타이머

- LAD1882 `0217`, NID25: FC109 KF_KT 선언 0056 RID299, 0057 BlockInterfaceInfo RID300의 KF:Int, SEC:Bool, KT:Word를 확인했다. CRef23/CodeBlock22는 KF←Data.VALVE_P ORef25/RID290(W24), SEC←ORef27/RID302(W26), KT→Coeff.DP_01_PAUSA_SOGLIA_1 ORef30/RID10(W29). CRef23.eno W28→CRef32.en; 두 번째 KF←VALVE_W ORef34/RID291(W33), SEC←ORef49/RID302(W35), KT→LAVORO_SOGLIA_1 ORef52/RID13(W51)이다.
- 0597 RID302/NID25 UID27·49는 **Bool literal0**다. ‘0초’로 읽지 않는다. live_index doc458의 인터페이스 주석은 SEC true=seconds/false=tenths이고 doc457 제목은 max9990seconds이나, 이 초안에서 FC109 STL 본체의 모든 분기·범위 처리를 독립 해석하지 않았다.
- LAD1887 `0201`, NID4: ON Contact500.out W501→Move457/462.en. Coeff.PAUSA_1 ORef476/RID10→LAVA_PAUSA ORef477/RID11(W487/488), Coeff.LAVORO_1 ORef478/RID13→LAVA_LAVORO ORef479/RID14(W489/490)를 **허가 비트와 별도 가지에서** 쓴다.
- 같은 ON 아래 BF01허가 Contact22(ORef23/RID63,W21)와 BF02허가 Contact507(ORef508/RID65,W510)가 OR25(W24/26)로 합류한다. OR25.out W27→NOT Tag_131 Contact502→SdCoil468.in(W503); value=LAVA_PAUSA ORef480(W491), operand=Tag_132 ORef482(W494).
- ON의 다른 가지→Tag_132 Contact504(ORef484,W496).out W505→SdCoil473.in; value=LAVA_LAVORO ORef483(W495), operand=Tag_131 ORef485(W498). 두 필터가 타이머 T1/T2와 시간 Word를 공유한다. 개별 BF01 타이머 두 벌로 복제하지 않는다.

보충 snapshot: live_index doc1604는 name/type/value 배열 각각129개, doc1629는 각각162개가 맞는다. 저장값 ZERO_DP01=0, COEFF_DP01=250, SOGLIA_1=50, PAUSA_1=S5T#4S, LAVORO_1=S5T#200MS, VALVE_W=2, VALVE_P=40을 대응시켰다. 이는 XML 핀 의미의 보충값이며 현재 운전값·승인 기본값·설정 지시가 아니다. Word16#0400/16#0020을 단순 정수 ms로 바꾸지 않는다.

### 3.4 DP 단계형 시간 가지와 복수 Word 쓰기

LAD1883 `0198`, NID1, OFF377→Lt206(Ev_filter_on ORef280/RID3 < literal51 ORef281/RID4), W318~321 이후:

| 비교 구간(원문) | 비교 Part·주요 입력 Wire | PAUSA Move→대상 ORef | LAVORO Move→대상 ORef |
|---|---|---|---|
|DP01 < S1|Lt213 W322/323|216, PAUSA_1 ORef284→285 W326/327|219, LAVORO_1 ORef286→287 W329/330|
|DP01 ≥ S1 AND < S2|Ge225→Lt228, W331~335|231, PAUSA_2 ORef292→293 W338/339|234, LAVORO_1 ORef294→295 W341/342|
|DP01 ≥ S2 AND < S3|Ge240→Lt243, W343~347|246, PAUSA_3 ORef300→301 W350/351|249, LAVORO_1 ORef302→303 W353/354|
|DP01 ≥ S3 AND < S4|Ge255→Lt258, W355~359|261, PAUSA_4 ORef308→309 W362/363|264, LAVORO_1 ORef310→311 W365/366|
|DP01 ≥ S4|Ge270 W367/368|273, PAUSA_5 ORef314→315 W371/372|276, LAVORO_1 ORef316→317 W374/375|

각 LAVORO Move.en은 앞 PAUSA Move.eno(W328/340/352/364/373)다. 다섯 구간의 LAVORO 소스는 모두 0596 RID13 `DP_01_LAVORO_SOGLIA_1`이며 번호2~5로 바꿔 쓰지 않는다.

LAD1884 `0199`, NID2는 OFF559→Gt388(Ev_filter_on >50, W500~503) 뒤 DP02의 같은 형태 5구간이 **동일 DB1W236/238**에 쓰는 별도 경로다. 해당 Write UID는 PAUSA467/475/483/491/497, LAVORO469/477/485/493/499(0596 RID11/14)다. LAD1887의 ON 쓰기 UID477/479는 다른 NID4이므로 UID 숫자가 같아도 별개다.

여기서 51 미만/50 초과는 공통 step 번호이며 아래 출력 인터페이스의 BF01/BF02 교차 순서와 단순한 필터별50개 분할로 일치하지 않는다. OFF의 현행 상태·현재 실행순서·상위 호출·간접/외부쓰기가 확인되지 않아 ‘DP별 주기가 현재 적용됨’ 또는 ‘OFF라 영구 사문화됨’ 어느 쪽도 확정하지 않는다.

### 3.5 OFF 아래 Data.LAVA와 범위, ON의 별도 범위 쓰기

LAD1888 `0202`, NID6의 OFF Contact599/ORef569/RID1(W582/609), out W600은 네 가지로 분기한다.

| 조건 | Move·상수 | 동일 Data.LAVA 대상 |
|---|---|---|
|OFF|547, ORef570/RID67 Int0(W583)|ORef571/RID68 W584|
|OFF AND SC10 원시601|553, ORef573/RID70 Int1(W587)|ORef574/RID68 W588|
|OFF AND SC11 원시603|559, ORef576/RID72 Int2(W591)|ORef577/RID68 W592|
|OFF AND SC10 원시605 AND SC11 원시607|566, ORef580/RID74 Int3(W596)|ORef581/RID68 W597|

LAD1889 `0203`, NID7 OFF780(W742/782) 아래 Eq672/684/696/708은 LAVA=0/1/2/3을 비교하여 START/END를 각각 0/0,11/50,51/90,11/90으로 쓴다. 첫 Move675/687/699/711의 ENO가 다음 Move678/690/702/714를 허가(W749/758/767/776)한다. 대상 START ORef721/727/733/739 RID76, END ORef723/729/735/741 RID78이다.

그러나 LAD1890 `0204`, NID8 ON714/ORef703/RID52(W708/716) 아래 W715가 Move695/700.en을 직접 허가한다. Int11 ORef704/RID80→START ORef705/RID76(W709/710), Int90 ORef706/RID84→END ORef707/RID78(W711/712)의 **별도 쓰기**가 있다. OFF분기 결과만 보고 최종 범위를 확정할 수 없다.

### 3.6 단계 증가·경계 보정과 제외 EV 인터페이스

LAD1899 `0218`, NID27: ON21→Tag_132 Contact22(W43/44/67/46)→PBox23.in(W45), bit=PLS50 3 ORef31/RID89(W48). PBox.out W49가 Add24.en와 Lt25.pre/Gt27.pre를 병렬 허가한다.

- Add24: Int1 ORef32/RID70(W50)+Ev_filter_on ORef33/RID3(W51)→동일 카운터 ORef34(W52).
- Lt25: 카운터 ORef35 < LAVA_START ORef36(W53/54)→Move26(W55), START ORef37→카운터 ORef38(W56/57).
- Gt27: 카운터 ORef39 > LAVA_END ORef40(W58/59)→Move28(W60), START ORef41→카운터 ORef42(W61/62).

같은 Word에 Add와 두 Move가 있다. 경계 비교가 Add.eno 연쇄가 아니라 동일 PBox.out에 붙어 있는 구조를 보존한다. 실제 스캔 최종값·펄스 폭·활성 타이머 전이를 시험하지 않았다.

출력 경계 원본 `0205`~`0212` NID10~17을 구조 추출하여 공통 ON→Tag_132→Eq(step)→해당 필터허가→Coil의 연결을 대조했다. BF01 허가를 읽는 40개 가지는 **step11,13,…,89→EV11,12,…,50**, 출력 %Q12.0~%Q16.7이다. BF02는 그 사이 짝수 step이다. 이는 본체 공통 제어의 출력 경계 목록이며 제외40설비의 전체 의미/수리/전기도면 검토 완료가 아니다.

- 첫 BF01 경계: LAD1891 `0205` NID10 ON1060→T2접점1062(W1061/998/1063), Eq887(step11, ORef958/RID80,W999/1000), 허가1064(ORef959/RID63,W1001/1002), Coil891(W1065), EV11 ORef960/RID93(W1004), 0594 Output AO96=%Q12.0.
- 마지막 BF01 경계: LAD1898 `0212` NID17 Eq1895(step89), 허가2032, Coil1899→EV50 ORef1944/RID247, 0594 Output AO135=%Q16.7. 전체 40가지의 고유 Part/ORef/Wire·주소는 별도 pulse-interface-map.json에 보존했다.
- P&ID의 EV11~50과 본체 출력 경계는 대응하지만 도면 번호/전선/현행 설치를 모든 하위 EV에 자동 전개하지 않는다. 대표 EV11의 전기 전달만 §4에서 확인했다.

### 3.7 호출·Word 겹침·주석과 현행 실행의 경계

- main LAD1619 `0031`, NID6: ON282/ORef271 W280/284, out W283이 Analog input conversion CRef261, Allarms1/2/3 CRef264/267/270.en을 각각 허가한다. 0688은 Analog conversion RID55/CodeBlock273=FC3, Allarms3 RID64/CodeBlock279=FC6. 이를 직렬 ENO 호출로 설명하지 않는다.
- main LAD1620 `0549`, NID7: ON350/ORef335(W348/352), out **W351**이 Motors1 CRef319, Filter CRef322 등으로 분기한다. 0688 RID70/CodeBlock339, 0694 RID71/CRef322가 **Filter FC8**이다. motors1.eno→Filter.en의 직렬 Wire가 아니다.
- main LAD1622 `0033`, NID9: ON352/ORef349 W351/354→CRef347.en(W353); CodeBlock350/RID91=Allarm manager FC24.
- startup only LAD403 `0148`: ON329/ORef284→W330→Move267.en. Int0 ORef293/RID54(W315)→DB3 Word ORef294/RID32(W316). 0047/0048·0563의 선언은 NID3이고 0563 AO64/BAD23→0562 Allarm DB3이므로 **DB3.DBW8←0**, 그 범위에 MAX_DP_FILTER DBX9.5가 포함된다. 파생 network-map의 NID=null과 원본 선언 NID3을 구분했다. BF01_OFR DBX24.3은 이 startup의 W0~16 범위에 포함되지 않는다.
- startup only LAD402 `0147`의 DB2W2←0은 SC10/VR04 요청 비트를 포함하지만 그 모터별 제어 소유는 독립이다. BF01 허가 Local·M180.3을 그 Word로 Reset한다고 쓰지 않는다.
- 전체 IdentXmlPart 선언을 이름과 주소 범위로 검색했다. BF01_RUN M180.3에 겹치는 Memory Word/DWord 직접 Write 선언은 이번 추출에서 찾지 못했으며, Data의 관련 명명 Writer는 위 네트워크의 다중쓰기를 따로 세었다. 이름이 비어 있는 GlobalAccess 직접 Write도 주소 범위를 검색했고, 그 검색에서 해당 DB1 구간을 덮는 추가 절대 Word 선언은 찾지 못했다. 이것은 간접 포인터/블록복사/통신/현재 CPU의 모든 Writer가 없다는 증명이 아니다.
- startup doc401 검색 원문은 `set s "on" clr s "off"`이며 0047 ON RID1/NID1 UID24와 OFF RID2/NID1 UID27 모두 OID7 Write다. **CLR 다음 S를 R(Reset)로 바꿔 읽지 않는다.** 현재 OFF=False 초기화, ON=True 고정, 기동호출·리텐션은 미확정이다.
- live_index doc1904의 EV OR→BF01_RUN/BF02_RUN SCL 검색 텍스트는 전체 `(* … *)` 주석으로 감싸져 있다. 활성 Writer 근거로 채택하지 않았다. 직접 XML 근거의 M180.3 Writer는 §3.2 허가 Coil이다. 검색 문자열의 존재와 활성 코드는 다르다.

## 4. 전기·계측·실제 도면 확인

### 4.1 개별 시트·페이지·footer

`Electrical_Rev2.pdf`의 파일명 Rev2를 시트별 개정 날짜로 복제하지 않았다. 아래 12개 시트는 각각 실제 전체 렌더의 해당 내용과 footer를 확인했다. 공통 기본일자 표기가 같아도 개별로 대조했다. 모두 footer DATA=27.05.2024, 해당 시트에 별도 Rev2/17.03.2025 문구를 확인하지 못했다.

| FG | 실제 PDF쪽 | 확인한 내용 | footer 개정/날짜 판독 | 범위 |
|---|---:|---|---|---|
|152|153|JB1 전원·보호·110Vac/24Vdc 분기|27.05.2024; 별도 개정 문구 미확인|핵심 경로|
|153|154|JB1 IM·I/O 구성과 전원단자|27.05.2024; 별도 개정 문구 미확인|핵심 경로|
|154|155|대표 EV11 명령·릴레이·110Vac부하|27.05.2024; 별도 개정 문구 미확인|대표 출력 경계|
|168|169|PV14 출력·열림/닫힘 입력|27.05.2024; 별도 개정 문구 미확인|독립 PV14 소유 경계|
|169|170|DP01/02 전원·4–20mA·단자|27.05.2024; 별도 개정 문구 미확인|DP01 핵심 경로|
|170|171|LD01 저레벨/점검문/셀렉터|27.05.2024; 별도 개정 문구 미확인|독립 LD01 소유 경계|
|171|172|TC09 두 채널, 예비TC10|27.05.2024; 별도 개정 문구 미확인|독립 TC09 소유 경계|
|172|173|DP01 PEW398 모듈핀·전원|27.05.2024; 별도 개정 문구 미확인|DP01 핵심 경로|
|173|174|EV11 Q12.0 모듈핀·공급|27.05.2024; 별도 개정 문구 미확인|대표 출력 경계|
|177|178|PV14/FN04/ER01/LD01 입력|27.05.2024; 별도 개정 문구 미확인|혼합 소유 경계|
|180A|182|FN04 PAW336 아날로그출력|27.05.2024; 별도 개정 문구 미확인|FN04 소유 경계|
|180B|183|PAW344/346/348/350 SPARE|27.05.2024; 별도 개정 문구 미확인|예비 채널 경계|

FG155~167/174~176/178~180 등 catalog 범위 나머지 시트는 색인/텍스트 탐색 범위다. 개별 EV 전선·접점·footer를 전부 의미검토했다고 세지 않는다. 별도 렌더만 만들어도 실제 판독 완료로 계산하지 않는다.

### 4.2 JB1 공통 전원

FG152/PDF153:

- 110Vac9.11(60/6)→X3:1, 0Vac9.9(9/5)→X3:2→152QF1 6A 두 극→152.1/152.2→152GD1 AC/DC 5A. +출력152.3→152QF2 4A→+24Vdc152.5, −출력→−0Vdc152.4. 표기 배선 RED/BLUE FAS17 1.5mm².
- 별도 110Vac9.10(9/4)→X3:3→152QF4 2A→110Vac152.8, 공통0Vac9.9와 함께154/0으로 간다. DC제어 공급과 EV의110Vac 부하 공급을 구분한다.
- QF3 1A→152TM1 L:5, N:7, 출력3→152EV1 제어반 냉각 가지가 별도로 그려져 있다. 이를 필터세정 EV11로 혼동하지 않는다.
- 24Vdc 선은59/9·60/9 교차참조도 있다. BF01만의 완전히 독립된 전원/격리회로라는 결론을 내리지 않는다.

FG153/PDF154에서 153IM155의 1L+/2L+,1M/2M 전원, Profinet X1P1/X1P2와 POS2 AI 153A1, POS3 DQ 153A2, POS4 DI/DQ153A3, POS5 AQ153A4를 확인했다. **그림 내부 형식과 외부 문자열이 일부 다르다**(IM 6ES7155-5AA00-0AB0 대 외부6ES7155-5AA01-0AB0; DI/DQ 내부6ES7523-1BL00-0AA0 대 외부6ES7523-1BL01-0AB0). 153A1은6ES7531-7KF00-0AB0,153A2는6ES7522-1BL01-0AB0,153A4는6ES7532-5HF00-0AB0 표기다. 도면의 모델 표기이며 실제 설치 모델·호환성·교체품 추천으로 확정하지 않는다.

### 4.3 대표 세정 출력의 양 끝점

제외 EV11의 개별 매뉴얼을 재개하는 것이 아니라 BF01 공통 제어가 현장 출력으로 전달되는 대표 경계다.

1. PLC XML EV11 %Q12.0(§3.6)↔FG173/PDF174 `A12.0`, CPU515/MOD3 채널핀1→FG154/3.
2. FG154/PDF155 A12.0→154KA1 코일 **A1**, A2→−0Vdc152.4. DC 코일과110Vac 부하를 구분한다.
3. 부하측110Vac152.8→154KA1 **접점5–9**→선154.1→X3:4의5×20 2A F→선154.2→EV11 A1→EV11 A2→X3:5→0Vac9.9. 하단 접점표의1/5/9 중 실제 그린 부하 경로는5/9다.
4. FG173의24V 공통은X22:4001 5×20 4A F→공급핀9,0V→핀10이다. 현행 회로·코일 전압·퓨즈 설치/설정·접점 상태는 현장 미확인이다.
5. 원본에 이 대표 출력의 실제 밸브 이동/공기압 분사 피드백 경로는 확인하지 못했다. Q=1 또는릴레이 동작만으로 세정 완료·차압회복을 선언하지 않는다.

### 4.4 DP01 센서부터 PLC 환산까지

- FG169/PDF170 DP01은 제목 DIFFERENTIAL PRESSURE SWITCH이나 도형의 출력은 **4–20mA**, 범위0/50 mbar다. 센서 측110Vac152.8→X3:90(5×20 2A F)→DP01 전원+,0Vac9.9→X3:91→전원−. 신호 DP01+→X3:92→+PEW398(172/4),−→X3:93→−PEW398(172/4); 차폐169SCH1→X3:94와 접지 표기→172/3을 구분했다.
- FG172/PDF173 `PEW398`, CPU515/MOD2, +→**30 I6+**, −→**32 U6−/I6−**. 29Uv6/31U6+는 이4–20mA 경로의 실제 연결핀으로 바꾸지 않는다. 모듈 공통 +24Vdc→X22:4000 500mA F→41L+, −0Vdc→44M. DP02는 PEW400,34/36핀의 별도 채널이다.
- LAD1773 `0521`, NID40: ON1555/ORef1542 RID1(W1549/1557), out W1556→CRef1536.en. 0672 CodeBlock1548/RID5=Signal linearization, 0680 BlockInterfaceInfo RID351. IN0←ON ORef1543(W1550), Analog_input←PR_BF01 ORef1544/RID295(W1551), Coeff←COEFF_DP01 ORef1545/RID451(W1552), Zero←ZERO_DP01 ORef1546/RID297(W1553), OutValue→DP_01 ORef1547/RID298(W1554), Out_of_range→BF01_OFR ORef23/RID426(W24).
- 공유 환산 함수 LAD1658 `0291` NID1은 IN0 아래 `Analog_input > -1382 AND <=32767`일 때 Convert164/167→Add170(원시값+Zero)→Convert174(Coeff)→Mul177→Div181(/28000)→Move185 OutValue의 ENO 연쇄다. App3/4/5/6는0611에 DInt, OutValue는Int로 선언돼 있다. 계수·제로를 실제 스케일 승인값으로 단정하지 않는다.
- 입력 >32767 또는 <=−1382는 Gt190/Le259→OR47(W35/48/49)→Move193의 literal−9999 ORef218/RID21(0612,W252)→OutValue ORef219(W253); Move193.eno W21→Coil23 Out_of_range ORef24/RID26(W22)이다. 일반 Coil과 Move의 ENO 경계를 임의로 래치 알람으로 바꾸지 않는다. ORef41/RID25의−1382는0612 선언으로 결속했으며 다른 블록0631의 동숫자 Allarm1과 혼합하지 않았다.
- LAD1659 `0014`, NID2는 NOT IN0 Contact171→Move162(W172), Int0 ORef166→OutValue ORef167(W169/170)이다. 함수 내부의 비활성0경로가 있어도1773 호출 자체가 ON 조건이므로 **ON이 꺼질 때 반드시 매 스캔0을 쓴다**고 확정할 수 없다.

도면0/50 mbar·P&ID set5÷10mbar·PLC Int계수/문턱·HMI의mb 소수점 표시는 서로 다른 층이다. 원 프로젝트의 채널설정·교정·환산단위/화면스케일을 확보하기 전 소수점 위치·정상범위·보호한계로 합치지 않는다.

### 4.5 시공 케이블·승인상태

`Electrical_Can_Decoating_20241118.pdf` 실제 PDF42/60/61을 확인했다. 각각 도번 CANDC-CONS-E025-042/C010-060/C011-061, footer24.11.11 `first draft design`, CHECKED/APPROVED 공란이다. 승인 준공도나 현행 케이블 길이로 확정하지 않는다.

| 실제 PDF/행 | 양 끝점 | 케이블 번호·표기 | 경계 |
|---|---|---|---|
|60/10_23|CR→BF01 JB01 POWER(110V/110V/0V)|=DUS+BF01-JB01A, CVV4G4.0, LEN104|110Vac 공통 공급 계획|
|60/10_24|BF02 JB02→BF01 JB01 IM|=DUS+BF01-JB01B, Profinet, LEN11|통신 연결 계획; 현행 온라인/토폴로지 미검증|
|60/10_25|BF01 JB01→JB01TB1 EV11~20|=DUS+BF01-JB01TB1A, CVV25G1.0, spare4,LEN24|대표 출력 군 연결; EV별 완료 아님|
|61/11_1|BF01 JB01→JB01TB5 DP01 POWER|=DUS+BF01-JB01TB5A, CVV3G1.0,LEN6|중간접속점이 있는 전원경로|
|61/11_2|BF01 JB01→JB01TB5 DP01 AI|=DUS+BF01-JB01TB5B, CVV-S2S1.0,LEN6|중간접속점이 있는 신호경로|
|61/11_25|JB01TB5→DP01 IN POWER|=DUS+BF01-DP01A, CVV3G1.0,LEN2|최종 전원 구간|
|61/11_26|JB01TB5→DP01 OUTPUT|=DUS+BF01-DP01B, CVV-S2S1.0,LEN2|최종 아날로그 구간|

PDF42 DUST ZONE08 도형은222RD→JB01TB5→DP01과 JB01 분기를 보여 준다. 표의11_1/11_2 중간구간 및11_26 신호구간을 확인했다. PDF61의 최종 전원11_25까지 PDF42 표 한 줄로 모두 판독했다고 확장하지 않는다. 전기X3:90~94와 시공JB01TB5의 실제 단자번호 대응표·현장케이블 식별은 미확보다.

## 5. 알람·복구와 인접 보호의 소유

### 5.1 두 필터 공통 차압 경보

LAD1992 `0540`, NID14, 0682/0683/0684/0686:

- ON1204/ORef1153(RID1,W1173) 아래 W1205→Gt1121(DP01 ORef1154 > Int2800 ORef1155), Gt1124(DP02 ORef1156 >2800 ORef1157), Lt1127(DP01 ORef1158 <−100 ORef1159), Lt1130(DP02 ORef1160 <−100 ORef1161).
- 각 out W1176/1179/1182/1185→OR1120.in1~4. OR.out W1186이 SdCoil1136.in과 Tag_112 Contact1206.in을 같이 허가한다.
- value ORef1162/RID96(W1187)=**S5T#3M**, 0683의 S5Time SV=S5T_x0023_3M,V8576 원문. operand ORef1163/RID118(W1188)=Tag112 **T114**. Contact1206 ORef1164(W1189).out W1207→SCoil1141; ORef1165/RID119(W1191)=MAX_DP_FILTER.
- Reset 가지는 ON→RESET_ALLARM1208(ORef1166/RID24,W1193)→기존 MAX_DP_FILTER1210(ORef1167,W1194)→Lt1146(DP01 ORef1168 <Int2500 ORef1169,W1195/1196)→Lt1149(DP02 ORef1170 <2500 ORef1171,W1198/1199)→RCoil1152(W1200), 대상ORef1172/RID119(W1202).

발생의 비교는 strict >2800 또는 strict <−100이고 Reset의 두 비교도 strict <2500이다. Reset에는 −100 이상 복귀 조건이 없다. 예를 들어 센서 이상값−9999가 단지2500보다 작다는 이유로 Reset 비교를 만족할 수 있어, 알람해제는 센서 정상화·원인 제거·안전 운전의 증거가 아니다. 실제 동시 Set/Reset 우선순위·타이머 만료·호출·화면 재표시는 현재 CPU에서 미확인이다. 이 공유 알람을 BF01 전용·BF02 전용 두 독립알람으로 만들지 않는다.

### 5.2 Word 경보 전달·startup 초기화의 차이

- 공통 allarm manager LAD927 `0151` NID1은 RESET_ALLARM/ RUN_HORN/STOP_HORN의 OR121.out W212 아래 DB3 W0,2,4,6,8,10,12,14,16을 WorkData로 복사한다. MAX_DP_FILTER가 포함된 DB3W8은 ORef181/RID21→Move147.in W202, out→WorkData.W4 ORef182/RID22 W203;0565와0564 Allarm TOD3/WorkData TOD6로 대조했다.
- LAD928 `0152` NID2에서 Ne203의 DB3W8 ORef228/RID21(W252) 대 WorkData.W4 ORef229/RID22(W253)→OR190.in5(W254). 다른 8개Word 변화와 OR한 뒤 NOT STOP_HORN271(ORef238,W268)→Coil219 NEW_ALLARM ORef239/RID35(W270/272).
- LAD929 `0153` NID3는 NEW_ALLARM219→NOT RESET_ALLARM221→NOT STOP_HORN223(W220/222) 뒤 W224에서 RUN_HORN Set204, NEW_ALLARM Reset206을 갈라 쓴다. 실제 경적 출력·스피커·HMI 경보표시까지 완료 검증한 것은 아니다.
- **BF01_OFR DB3.X24.3은 위 W0~16 복사/비교 범위 밖**이다. 이 근거로 해당 OFR이 이 Word변화경로를 직접 거친다고 할 수 없다. HMI Allarmi_233 설정 존재와 구별하며 전체 시스템에 다른 알림경로가 전혀 없다고 단정하지 않는다.
- MAX_DP_FILTER는 startup DB3W8←0의 겹침 쓰기가 있다(§3.7). BF01_OFR은 해당 범위 밖이다. 같은 DB의 모든 알람이 같은 방식으로 초기화·경보화된다는 가정을 하지 않는다.
- LAD930 `0158`, NID9: Inputs.Reset_allarmi Contact23 또는 Flag.Reset_Allarms_HMI26→OR28.out W38→SCoil33 RESET_ALLARM(ORef37)와RCoil40 Reset_Allarms_HMI(ORef43). 별도 Reset 요청·ACK/소거·원인 제거·재기동을 한 동작으로 합치지 않는다. 버튼을 작동하거나 현장 Reset을 수행하지 않았다.

### 5.3 PV14·온도 및 모터 경계

- Filter LAD1902 `0215` NID20의 PV14 불일치식은 `ON AND [(PV14명령 AND NOT OPEN응답) OR (NOT PV14명령 AND NOT CLOSE응답)]`→SdCoil1986(원문 S5T#20S)→Fault_PV14 Set1991이며 RESET_ALLARM과 기존 Fault로Reset1996한다. 소유는 독립 PV14이고 BF01 세정 밸브의 20초 고장으로 복제하지 않는다.
- LAD1903 `0216`, NID21: ON2035 아래 Fault_PV14 Contact2037→RCoil2004 `Flag.M_PV14` Reset. 별도로 M_PV14 Contact2041, Open false air2043, MAX_TC09 2045, MAX_MAX_TC09 2047, Emergency_module_fault22의 **5개 OR2007**→Coil2012 `PV-14` 출력이다. 따라서 요청Reset이 모든 출력OR를 차단한다고 설명하지 않는다. 0596 RID277=DB2.X13.1, MAX_TC09/MAX_MAX_TC09=DB3.X8.6/8.7,Emergency=DB3.X16.6;0594 PV14 RID268 Output AO136=%Q17.0.
- FG168/177의 PV14 I28.0/I28.1 응답, TC09 FG171의 두4–20mA 채널, FN04·ER01·LD01은 공유시트의 다른 소유다. 이번 BF01 문서로 TC09의 전체 알람 발생조건·FN04 정지·PV14의 모든 Writer·현장 정상극성까지 완료하지 않았다.
- SC10/VR04 전용 고장 2초·모터 출력/기동·FN04 공유 예고장 90분 등은 별도 조사 초안에 있다. BF01의 타이머·알람 수에 복사해서 더하지 않는다. 이번 본체 핵심 식에는 그 처리응답이 입력으로 쓰인다는 점만 직접 결속했다.

## 6. 증상별 관찰·수리 준비

아래는 읽기 전용 비교점과 승인된 점검을 준비하기 위한 지침이다. 실제 강제출력·보호값/타이머 변경·우회·운전시험·정비 실행은 하지 않았으며, 전기/기계/공압 접근은 현장 절차·전원/압력 격리·담당자 승인 이후에만 한다.

| 증상 | 동시에 남길 관찰 위치/값 | 비교와 원인 배제 | 완료에 필요한 증거 |
|---|---|---|---|
|BF01_RUN이 안 켜짐|ON,SC10 I5.0/DB13.X5.0,VR04 I5.5/DB13.X5.5,DP01/S1,Forza·Local허가|원시/처리 불일치와 직렬 응답을 우선 구분;≤와Forza 별도ON가지를 원문대로 대조|현재 호출/통신·응답 정상 및 안전한 허가 복귀|
|RUN 표시가 있으나 세정 안 됨|M180.3,허가Local,T1/T2,DB1W170/232/234/236/238,대표Q12.0|허가 미러와 실제 펄스·공기분사를 구분;카운터번호≠EV번호|명령→접점5/9→코일·공기분사 및 차압회복 확인|
|HMI 작업/휴지 설정과 간격 다름|HMI W318/W320,Coeff W146/W156,DataW236/W238,OFF,실제읽기시각|KF_KT SEC Bool0·ENO,DP별 쓰기와ON 고정쓰기를 분리|현행FC109·현재WordWriter 교차참조와 주기 로그|
|한쪽 필터만 순서가 맞지 않음|공유step/양쪽허가/START-END|홀수BF01·짝수BF02 경계,OFF의11~50/51~90와ON의11~90,카운터다중쓰기|실제양쪽순서·출력·호출확인;제외EV 개별완료와분리|
|DP 표시가 비정상/−9999|DP01전원·4–20mA,PEW398/DP01 Int,제로/계수,OFR|센서→X3:92/93→AI30/32→환산ENO·범위 비교;소수점단위추정금지|교정·채널설정·명판·현재환산표와값일치|
|공유 차압알람이 계속 발생/해제만 됨|DP01·DP02, T114,MAX_DP_FILTER,RESET,발생/해제시각|BF02기여·3분조건·Reset하한미검사·startup W8쓰기를구분|양쪽입력 정상범위·원인해소·지속복귀·안전 재요청|
|OFR은 화면에 보이나 공통경적 반응 불명|DB3.X24.3,HMI Allarmi_233,Word경보범위,실제 알림시각|W0~16경로 바깥인 점 확인;주소설정≠이벤트|현행알람설정/함수·소리/기록까지실제확인|
|JB1 여러 기능이 동시에 이상|110Vac X3:1/2/3,24V공통,모듈진단,Profinet경로|공유전원/통신과BF01전용고장을분리;하위PLC태그만으로실물단정금지|승인준공도·현행설치/단자·통신정상증거|
|차압은 돌아와도 분진 배출 불량|SC10·VR04 기계경로·호퍼/백/압축공기|접촉기응답과회전/배출/백정상구분|격리 후 실물점검·제조사기준·승인복귀기록|

관찰은 관찰자·시각/시간대·위치·값/단위·수집장치·프로젝트/CPU근거·비교원본·원인배제·조치·복구증거를 따로 기록한다. 이 초안에는 실제 운영관찰·복구기록을 생성하지 않았다.

## 7. 완료 기준·네 기능·남은 자료

### 7.1 확보해야 할 자료와 판정

1. 현행 PLC 프로젝트/CPU 비교와 교차참조: FC8·FC109·FC3/6/24의 실제 호출/네트워크 순서, ON/OFF·Local·타이머 리텐션, DB1/4 쓰기·간접/통신Writer. 최종Word·활성주기·동시Set/Reset이 설명과 맞는지를 별도로 판정한다.
2. 현행 HMI 원 프로젝트: BF01_RUN 표시·active step·DP 소수점·VALVE_W/P 입력/권한·알람Allarmi_78/233·Reset/ACK 이벤트. 현재화면·실제Write/Read 증거가 있어야 HMI 전달 완료다.
3. 승인 전기·시공도와 실물 명판: JB1의 내부/외부 모델표기 충돌, 모듈/슬롯/주소, X3↔JB01TB5 단자대, DP014–20mA 채널·교정·차폐,Profinet선. 도면파일명이나 예정 LEN으로 설치를 확정하지 않는다.
4. BF01 기계·공압 제조사자료: 백/케이지/씰·노즐/배관·압축공기·정비안전/방폭·허용온도/차압·교체 기준. 과거P&ID 숫자를 현재보호값으로 쓰지 않는다.
5. 세정 출력의 실물/공기/차압효과와 분진배출 관찰:Q·릴레이·모터접촉기 응답만으로 본체 복구를 완료하지 않는다. 독립SC10/VR04/DP01/PV14 작업의 완료를 별도 판단한다.
6. 제외EV11~50·다른독립ID 범위는 사용자 지시 없이 재개/완료처리하지 않는다. 자료없는 항목을 추정으로 메우지 않는다.

### 7.2 네 기능과 기록 보존

| 기능 | BF01 적용 판단 | 이번 결과 |
|---|---|---|
|도면·래더 비교|§3허가/시간/카운터·§4전원/DP/대표출력 연결 가능|원본 대조 초안만 확보; 제품UI 미구현/미검증|
|백업·선택 복원|BF01 지원 여부·저장키·타설비/미지필드 보존 필요|실제내보내기/충돌선택/저장/재읽기/재열기 미수행|
|기록 전후 비교|정상화/설정시점·호출·단위근거를 분리해 비교해야 함|운영기록 작성·수정0; 실제비교 미수행|
|보고서/PDF|7영역·근거/부족자료를 담을 수 있음|이Markdown 조사초안만 작성; 제품보고서/PDF 생성/검증 미수행|

### 7.3 검증과 집계 경계

- 수행: 고정커밋/버전·시작/종료Git상태, 읽기전용 preflight, XML 파싱·직접핀/선/주소 대조, Word/이름Writer 검색, HMI주소10행, 선택 원본PDF16개 고유 페이지 실제판독, 정지HMI이미지1개. 아래 부록의 SHA/Git blob 대조는 바이트보존 검사다.
- 의미검토의 핵심전체 네트워크: 공통세정 `0198/0199/0200/0201/0202/0203/0204/0217/0218/0219` 10개, DP변환경계 `0521` 및 공통환산 `0291/0014` 3개, 공유차압경보 `0540` 1개, 합계14개. 같은공통네트워크를BF01/BF02 두설비의 독립완료 수로 합산하지 않는다.
- 0205~0212의80출력분기 중 BF01허가40가지 구조추출은 출력경계확인이다. 실제 EV별도면·기계·알람·복구 의미검토40건으로 세지 않는다. 호출·입력Word·startup·공통경보·PV14는 본문에 적은 관련분기 범위이며 전체프로그램 의미검토가 아니다.
- PDF16쪽=전기12+시공3+P&ID1. 전기6쪽은핵심전달경로, 나머지6쪽은소유경계 판독. 사진/렌더의 수 또는PDF전체해시1개와 의미검토쪽수를 섞지 않는다.
- 미실행: 시뮬레이터/PLC실행·TIA·현재CPU·현장복구·생성기/npm/build·BC01제품회귀·PC/모바일UI·저장/복원·게시/패키지 검사. 원본조사만 허용된 범위이고 제품변경이 없으므로 이를검사통과로 표시하지 않는다.
- 수행 명령은 읽기 전용 preflight.py, 본 조사폴더의 extract.py·inspect_pulse_interfaces.py·verify_and_hash.py 및 PyMuPDF의 PDF 읽기/렌더다. 모두 종료0을 확인했다. 원본 프로그램 생성기나 PLC 동작시험을 호출하지 않는다. 구조 추출·해시 대조·직접핀 assertion 로그는 extracts/BF01/에 보존한다.
- 독립 검토는 부모가 별도로 수행해야 한다. 자체 XML 정적 assertion은 PLC 동작시험도 독립 검토도 아니다.

| 상태 | 결과 | 경계 |
|---|---|---|
|documentation|draft_ready_with_gaps|BF01 본체·세정 공통 핵심과 미확정 작성; 별도 검토 전|
|static_review|scoped_source_review_done; independent_review_pending|원본 핵심14네트워크·선택 PDF16쪽/관련분기; 제품 전체검사 아님|
|ui_records|not_run|BF01 통합·실제 저장/재열기 없음|
|publication|not_published|이번 조사 게시/코드 릴리스 없음|
|tia_compile|not_performed|TIA 컴파일 없음|
|live_cpu|not_performed|현재 프로젝트/CPU/온라인 관찰 없음|
|field_recovery|not_performed|실물·교정·정비·복구 확인 없음|

다음 한 작업: 부모가 이 초안의 Forza 별도 ON 가지, DP≤허가/선행응답, 공유 Word 다중쓰기와 OFF 해석, 3분 알람 Reset 하한 미검사, DP01 양 끝점·개별 footer를 고정 원본으로 독립 대조한다. 새 증거 없이 현장/하위 설비 완료로 올리지 않는다.

## 부록 A. 원본 바이트 보존

아래 해시는 선택한 근거·맥락·보존 파일의 SHA-256이다. source-hashes.json에는 고정 커밋 Git blob OID와 동일 내용 SHA-256도 함께 보존한다. 해시 일치 파일 수와 14개 핵심 의미검토·PDF16쪽 판독 수는 별개다. 압축백업·PLF·중지 자산은 보존 해시만 확인했으며 전체 파일의 의미검토/실행을 뜻하지 않는다.

선택한 원본/맥락/보존 파일 **96개**는 고정 커밋 Git blob과 바이트가 일치했다. 중지 5자산은 freeze 해시도 일치했다. 시작·종료 원본 Git 변경0. 문서의 의미검토 범위는 §7.3이며 이 숫자로 대체하지 않는다.

| 파일 | SHA-256 | 고정 커밋 Git blob OID |
|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` |
| `all-in-one/assets/HMI_DECOATER.png` | `b84b888a2df87d23b514aeb790d2fc51f31c3b20486061a365380b28986f49af` | `aa549ca104a1f92975dbf4ec346368423f3f61b7` |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` |
| `all-in-one/registers/hmi-window-provenance.json` | `b0251e377268ec7be83a781fb41e84684a6b187d0132fc7cfa51a6074823a2fa` | `bf258dd76b936da85beebd450ca563aef1b4e9e3` |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | `653d27572de6beedcf3eb6c95702bb119a8b567f` |
| `all-in-one/sources/decoded-original/0033-FlgNet.xml` | `e7fc5601889297a84fcc6b5601a3e0acba420b9c9adb8b37c60277a0fb5cb108` | `b8a89efcb38999950739e0462830d03a94d57c08` |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` |
| `all-in-one/sources/decoded-original/0056-IdentXmlPart.xml` | `c5ec45cd232c36d80f80487ec0dd284a876e326ba2286fc722ecc861a400232a` | `1364306d64caf1f1f094c98dc163edf69cdc1afc` |
| `all-in-one/sources/decoded-original/0057-IdentXmlPart.xml` | `1124275ab34e188b042b263d3c4b744abf5637ffd229af642b81a27f00a00c6b` | `264d24445f42cf32706bc6942863f9f227eb797e` |
| `all-in-one/sources/decoded-original/0064-IdentXmlPart.xml` | `ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d` | `300d74239868f4f4595d4d5bbb848b4b58bbae76` |
| `all-in-one/sources/decoded-original/0147-FlgNet.xml` | `386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c` | `0027890eca158e714dd6260dc920a5d3aa83319b` |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` | `3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3` |
| `all-in-one/sources/decoded-original/0151-FlgNet.xml` | `227627d165c6240a4c15b62fd4e4c8d7a621c15f35319cb424601df5cc52c904` | `8e8a9801d1f57180fc3747f6515c0353f38f7dc5` |
| `all-in-one/sources/decoded-original/0152-FlgNet.xml` | `2b6165460f06a52de56afcb4d65ed163d64320e24af1b194e934a4d7c6bfe49f` | `dd8e35b98043d9d0f230351352273eac1d783990` |
| `all-in-one/sources/decoded-original/0153-FlgNet.xml` | `3d3a236a66a7a5c9b8e2d1e15da63cc943ba5cd266949583cbac6ffbb2f88bc6` | `d50223c45f5eb1d1c1d3530b41db1e79ad6c71f3` |
| `all-in-one/sources/decoded-original/0158-FlgNet.xml` | `d3f3adebc3d990b85c5d4c294906ae3bc3dafebb49d25b030bf9cc2ccf905651` | `233ccf8f9d82ffffa498e04cbdcd3de07115c1db` |
| `all-in-one/sources/decoded-original/0198-FlgNet.xml` | `95d631a1979b04f148bf6b71eebb8857e580511c523912d533814ed41dda871d` | `965c744c3e216c3625c6ec414236d2db1b6ef6ce` |
| `all-in-one/sources/decoded-original/0199-FlgNet.xml` | `005617b53ff1021c24dd11b19cae78c72ff535407999707d4c4636e493888b7c` | `ca1debbcfd0ca0a1555005886450db3e495d9772` |
| `all-in-one/sources/decoded-original/0200-FlgNet.xml` | `2bd1be34eb905a10d840c59aeb461464a1af418fa0ea3f2b8d0b3f88145eb27e` | `31eb4f3df5596c004278ef7b3ccf158ae3878079` |
| `all-in-one/sources/decoded-original/0201-FlgNet.xml` | `77e7fdcb37e54b3d513aee760f3c142f7259990352dd0ad14a3c9a1a5f61da32` | `0268a83b49e442ee22406139e6bf5062b21bdc6a` |
| `all-in-one/sources/decoded-original/0202-FlgNet.xml` | `8caa0c15a086ffb64f7857fb656b3baba3090a32948b9942ccecff6c730186bb` | `c8f6ed33f01b9c3cd126545969cd054ff298e086` |
| `all-in-one/sources/decoded-original/0203-FlgNet.xml` | `85510fca2cc0450d123d825e2c61e63d4d8c4ccbd354f58ee73d045e6967e7c9` | `c8d01a1c97029d8bfc9f0be3513c34a94b398370` |
| `all-in-one/sources/decoded-original/0204-FlgNet.xml` | `d34dd80c437e1ae8351dfbee61ce0db8f6c85ee3625ad2c09fa55d3aa64edc40` | `0f34353c5dc02e1e0f6bea231cd3e68e0b1e7165` |
| `all-in-one/sources/decoded-original/0205-FlgNet.xml` | `8003cb41dd3e68d51e5a91e1dee0726d98fd4ea3270a5ea93a4bfb871db67574` | `81ba42433699b834ab219990f172cf545d6f9aa6` |
| `all-in-one/sources/decoded-original/0206-FlgNet.xml` | `7eb7f0c937530eb553cb63ee40932230fda4222ef6678d34f0be3d47412bb603` | `0ed597ebe8e5e2c0e45f27cbde92dc93239d2d87` |
| `all-in-one/sources/decoded-original/0207-FlgNet.xml` | `cfbf5535ee20794aaa138dd21a1c80fb3d246e0bf3303449d1eff49d3dca1377` | `f847e614f1afd2c9226c94c7a5520fd4de0a16d3` |
| `all-in-one/sources/decoded-original/0208-FlgNet.xml` | `b0c8b09146738898af5821fce9c80c9cf8af4c8728259b60577b54ae55a54d3d` | `056e943ce5e82deb216c4b88ee67623c110e7f86` |
| `all-in-one/sources/decoded-original/0209-FlgNet.xml` | `a120b9ed2abe7e65c896cf097dd4d85eb7fdc6726c5c4f5dff38ebafbf8c6801` | `ee80c872f76ab1f333d1be6f0c231eec302448aa` |
| `all-in-one/sources/decoded-original/0210-FlgNet.xml` | `80bf954b84e90fbec9a8c682a4f4097c47da3635e940008c88fc3df43463b677` | `50c08b684e06171ffafdfb4c213a3e433aa7cf15` |
| `all-in-one/sources/decoded-original/0211-FlgNet.xml` | `d2d66556f622fc4f0264c638b22ed6a8add9bf3a55da6ecbfa344739703c1757` | `a50f6d427472d8aacb2d0ec69a4735f25c6e6a37` |
| `all-in-one/sources/decoded-original/0212-FlgNet.xml` | `f3dab4c2d6143637144daeecff0484ec546ab85e0c2ccab278ddcab8d72a1fc2` | `a2a587f24d8f09ff0f63c760204fc10d4e048b22` |
| `all-in-one/sources/decoded-original/0215-FlgNet.xml` | `723789a5daf72bba1d49751963bc6517739761ae3a4122b875b8a66ea0de3a14` | `096f3482463759a7a506433e7b3266e3f13d3f14` |
| `all-in-one/sources/decoded-original/0216-FlgNet.xml` | `3a7fa8b0a095f054c543f90d0ffab84a8cd0c60ff1b5ec0101b112dc8f4ff37d` | `97280ef67131ab7a480c8b0030d74de765c14c65` |
| `all-in-one/sources/decoded-original/0217-FlgNet.xml` | `cbff99bc9f5f8bbde0272c9541be1b26e48808865be58859ff6cef50b8eb9368` | `0a2ce467fd29315818de17b89093cf133e5742d8` |
| `all-in-one/sources/decoded-original/0218-FlgNet.xml` | `1cfcecebc32b8f69d30d2ea3946f13554acd79e3470e7d7b6358ac4f5e9e0481` | `dc5271460b37bd944592574704ffde29b7ee1a7b` |
| `all-in-one/sources/decoded-original/0219-FlgNet.xml` | `245409937abf7e28f25a24d4a6d311a801a4b2ee7293148be9b3d266352eb53a` | `d1c9ae9d9fe8a5a1ed605d09a3f9bd26c5632d0a` |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` |
| `all-in-one/sources/decoded-original/0401-FlgNet.xml` | `60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae` | `aadefbd35d305dd4a1146bf383b988a903802bf4` |
| `all-in-one/sources/decoded-original/0521-FlgNet.xml` | `8966080bc8e628f2604909960f79a060c150cc8fbb401b20f38c59a481cdd4d5` | `7cf0023ec0e3ad2f13d44d6bf91bb96d75b57407` |
| `all-in-one/sources/decoded-original/0540-FlgNet.xml` | `c05d5c1db35f1659992cae845cbcad515bbc34f00089169c0722076db9d77735` | `6b9a166d8fdf80bb52c63e90b794d69aaf34a919` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` | `985b5310b43b1015b5dee286aa0e42800564b94b` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` |
| `all-in-one/sources/decoded-original/0564-IdentXmlPart.xml` | `2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1` | `c4b1f2cb191970cfce1cce59cb290a9f1f934c37` |
| `all-in-one/sources/decoded-original/0565-IdentXmlPart.xml` | `0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149` | `c2e3e2d57c94c5da864f6e172f0a7a925da942d6` |
| `all-in-one/sources/decoded-original/0594-IdentXmlPart.xml` | `88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd` | `f38b7d9a52b3d5ae74953da8290f6b417758c1b5` |
| `all-in-one/sources/decoded-original/0595-IdentXmlPart.xml` | `10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52` | `1f24565efac58926dabf5b3fc54ad0e9537410b2` |
| `all-in-one/sources/decoded-original/0596-IdentXmlPart.xml` | `a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0` | `c8b2d1a05727b4ca44e2e4bed9fb58ba2b717576` |
| `all-in-one/sources/decoded-original/0597-IdentXmlPart.xml` | `60e292145fe54912a1da7510c8641a4f4c85efe62e1b5206ee3d92794a28de20` | `2831597d1879bd83f239e838dd4cbe6b3dc64e77` |
| `all-in-one/sources/decoded-original/0598-IdentXmlPart.xml` | `dc001c9370a691546c5dea79f5a1252d6d0a5564754703018c47df4bcc2522bb` | `17a4c24ebc97eb13db483e4c64ac386d6a69125a` |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` |
| `all-in-one/sources/decoded-original/0631-IdentXmlPart.xml` | `8e5072374f8ef098de72fbf93965b2a7bb0965c0f803e397daa68588c0c38555` | `27aa5aef2b126820b4658362e4aad5ca6d709fee` |
| `all-in-one/sources/decoded-original/0632-IdentXmlPart.xml` | `fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9` | `600935fa8d394c0d247ea20040d5dfff4f05b500` |
| `all-in-one/sources/decoded-original/0633-IdentXmlPart.xml` | `9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc` | `a1ab5ee12addbc92d04c9950d4437e2b564d6b5c` |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` |
| `all-in-one/sources/decoded-original/0682-IdentXmlPart.xml` | `25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092` | `61182411e912941161eccf4e90c1f174e5379f0a` |
| `all-in-one/sources/decoded-original/0683-IdentXmlPart.xml` | `0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22` | `662acdb9a06c0ba1c0027e7dd215a28f07d3f02b` |
| `all-in-one/sources/decoded-original/0684-IdentXmlPart.xml` | `6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208` | `d67b98b5d5516e0330aae5cfdbee41a3e09206e1` |
| `all-in-one/sources/decoded-original/0686-IdentXmlPart.xml` | `b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4` | `8c152d926692a8e15973c980e08e338d29411814` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` |
| `all-in-one/sources/hmi-windows.csv` | `15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e` | `8401dcfe5ba3e7e244eea0f501bb84a2e387da39` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |
