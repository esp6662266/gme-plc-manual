# LD01 석회 마이크로피더 원본 조사 초안

LD01은 M32 미세피더이고 LD01A/M33 사일로 진동기, LT01 레벨 계기, VR06/M40 로터리 밸브는 별도 소유 대상으로 유지한다. LD01 명령 Q3.6과 원시 응답 I4.6은 접촉기 직접기동 회로에 연결된다. **I4.6은 55KM1의 13–14 보조접점이며 축 회전·석회 투입량을 직접 검출한 증거가 아니다.**

LD01 및 LD01A 요청에는 VR06 처리Run 부재에 따른 Reset 가지가 있다. 그러나 진동기에는 요청과 별개인 간헐Start 가지가 병렬로 있으므로 **요청 Reset을 진동기 출력의 무조건 OFF로 바꾸면 안 된다.** 미세피더 점검도어와 진동기 현장셀렉터는 서로 다른 허가다. 저레벨 TON 10초, 피더 S5 고장2초, 진동기 S5 고장2초, 가변 간헐운전 타이머를 구별한다.

도면 FG55/56의 M32/M33은 각각0.18kW·0.55A이지만 55QM1/56QM1 범위는2.2–3.2A이고 BOM에도 같은 범위다. 현행 보호기/명판/설정의 적합성 또는 도면 오류 여부는 미확정이다. 이 조사로 보호값 변경을 제안하거나 수행하지 않는다.

이 산출물은 작업3 자체 cloud 원본 조사 초안이다. 로컬 2차133 통합·기능구현·게시·TIA 컴파일·현재 CPU·현장 복구 완료가 아니다.

## 작업 기준과 보존

- 대상: catalog_id `LD01`, 이름 석회 마이크로피더, motor, 집진·석회, parent_id 없음, depth0, priority_key 없음. INVENTORY catalog 배열98, equipment 배열50(모두0부터 센 위치)다.
- 네 번째 5개 묶음 MC03/MC05/LD01/BF01/BF02 중 LD01 한 개다. `progress/TASK3-BATCH04-SCOPE.json`에서 고유 ID·new_research_scope=true·confirmed_alias_duplicate=false·physical_identity_verified=false를 확인했다. 부모 자료 확인을 LD01A/LT01의 별도 조사 완료로 합산하지 않는다.
- 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, 프로그램v1.12.0. 저장소 https://github.com/esp6662266/gme-plc-manual . 최신 main·현재 CPU·현행 시공과 동일하다고 가정하지 않는다.
- GME-STD-1.0.0, AGENTS, gme-equipment-rollout/SKILL, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY와 고정판 최신 진행자료를 읽었다. VR06 초안은 구성만 참고했고 아래 LD01 선언·핀·수치·도면은 고유 원본에서 대조했다.
- 읽기 전용 preflight 종료0, inventory_matches=true. 대장248/우선23/대응18/제외90/제외부모하위보류7/phase2후보133 일치. requirements-audit.json 및 all-in-one-data.json의 source_byte_changes는 표준 스냅샷 대비 기존 차이이며 이번 원본 변경이 아니다.
- 조사일: 2026-10-11 UTC. 작성: LD01 원본 조사 작업자. 실제 실행 모델/추론 수준의 런타임 증명은 미확인이다.
- 쓰기 범위: 이 초안과 `extracts/LD01/`만. 공용 선언파일, 다른 초안, 코드·버전·대장·배포·운영기록 변경0. 원본·중지 자산 변경0. 시뮬레이터 작성/수정/생성/실행/행동 시험0. PLC·현장·보호값·SEJIN 운영자료/사진/이력 변경·복제·통합0.
- 해시 검사는 바이트 보존 검사이며 원본 의미 검토·기능 시험·현장 검증 수와 별도다. 최종 수량과 원본별 SHA-256/Git blob 검사는 부록에 적는다.

이하 원본 경로는 `all-in-one/` 아래다. `0259`는 `sources/decoded-original/0259-FlgNet.xml`, `0604` 선언은 `0604-IdentXmlPart.xml`이다. XML은 원본1행 직렬 파일이므로 위치는 LAD 문서ID, 블록 내 색인(index_order), NID, Part/Wire/ORef/CRef/UID/RID로 제시한다. 추출용 pretty XML의 줄번호를 원본 행번호로 사용하지 않는다.

## 7영역 적용표

| 영역 | 상태 | 확보 근거 | 미확정 경계 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | LD01/M32, LD01A/M33·LT01·VR06 분리, 고정판 | 실물 명판·현재 프로젝트·현행 동일성 |
| I/O·HMI | 적용, 일부 근거 미확보 | Q3.6/I4.6·관련Q3.7/I4.7, DB2/3/9/13/14, HMI설정7행 | 모터HMI 8데이터 ORef 미결속, 이벤트/쓰기권한 |
| 제어 구조 | 적용 | 요청Reset·도어허가·진동 대체가지·KF_KT·Word·호출 | 실제 주기/최종 우선순위·현재 설정/외부Writer |
| 전기 전달 경로 | 적용 | 전기8페이지·시공3페이지·P&ID1페이지 시각검토 | 0.55A/2.2–3.2A 차이,68FC1/170FC1,실제극성·단자 |
| 알람·복구 | 적용 | 주모터/진동기2초, 저레벨TON10초, 요청해제/Reset | 현재표시·원인제거·승인재요청·현장복구 |
| 증상별 수리 | 적용, 관찰 지점만 | 요청→명령→접촉기→원시→처리→표시 | 실제 진단·정비·관찰 기록 없음 |
| 완료 기준 | 적용 | 정적검토/자료 부족/기능/현장을 분리 | 통합·UI/기록·게시·TIA/CPU/현장 별도 |

## 1. 설비·계통·소유 범위

1. `registers/equipment.json` LD01행은 FG55/170이며, LD01A행(배열51)은 parent LD01·FG56이다. LT01행(배열103)은 parent LD01·FG170, VR06은 독립 ID다. 부모와 관련 부품을 이 초안에서 함께 읽었지만 ID를 합치거나 하위조사 완료로 세지 않는다.
2. `PID_1684n002I.pdf` p1은 LD-01 사일로, 하부 M32 미세피더, 측면 M33 진동기, LT-01, 출구 VR-06/M40 및 FN-05/M41→ER-01 공기계통을 표시한다. M32/M33은0.18kW/440V, M40은0.25kW/440V로 보인다. 물질 흐름과 PLC의 조건 의존성은 각각 확인한다. P&ID LT01과 전기 저레벨기기의 현행 동일성은 확정하지 않는다.
3. P&ID 도번1684n002, 판I, 기본 작성일06/04/2011, 판I 변경일15/01/2013이다. 전기 FG55/56/120/121/139/170/177/253의 기본 날짜는27.05.2024이며 **FG120/PDF121에는 Rev2/17.03.2025가 추가로 보인다.** 나머지 검토 시트에 파일명만으로 그 개정일을 일괄 부여하지 않는다.
4. 전기 직접 경로는 QM→KM→QS→M32다. 이 경로에서 LD01 자체 인버터 속도지령·PID·아날로그 전류/유량·엔코더는 비해당이다. 현행 추가 장치가 없다는 뜻은 아니다. 외부 LIW FEEDER의 아날로그 지령을 LD01의 속도지령으로 가져오지 않는다.
5. 시공 p36/51/60은24.11.11 first draft design, CHECKED/APPROVED 공란이다. 설계·케이블표를 승인 준공·실측 길이·현장 정상상태로 승격하지 않는다.

### 1.1 외부 LIW와 구별

- LD01 직접명령은 `0602` RID145 Output/AO30=%Q3.6, NID29 UID849이고, 별도 `START LIW FEEDER`는 같은 선언 RID198 Output/AO49=%Q6.1, NID43 UID1222 Set/1229 Reset이다. 이름에 FEEDER가 있다고 동일 설비로 합치지 않는다.
- LAD1973 `0273`, motors1 색인44/NID43: ON1251 뒤 BWF01 Contact1253/BWF02 Contact1255의 OR1190(W1233)와 PV03 GATE EV Contact1257(W1236/W1258)가 SCoil1201(Q6.1)에 연결된다. Tag127/S5T#15M 타이머 가지가 병렬로 있으나 그 접점이 이 Set 가지에 직렬인 것은 아니다. Q6.1 Contact1259 뒤 NOT BWF01/NOT BWF02→SdCoil1210 Tag128, Q6.1+Tag128 접점1265→RCoil1215가 별도다. 이 시간/게이트 조건은 LD01 요청Reset 조건에 합산하지 않는다.
- LAD1691 `0472`, analog output conversion 색인13/NID16: ORef919/RID104는 `0664` LIW_SP_SPEED, Word Output/AO2416/SAM=Peripherie, 즉%QW302:P다. Move909.out1 W928의 목적지다. 이는 Q3.6과 형식·주소·주인이 다르다는 경계 근거다. 181배산술, 유량 단위/환산/현재 설정의 LD01 적용은 하지 않는다.
- `registers/equipment.json`의 외부 CLIENT-CL17 등과 물리 LIW의 동일성은 이 작업에서 배정하지 않는다. 외부 LIW 내부 제어/안전·소유자·현행 배선은 별도 조사 대상이다.

## 2. I/O·HMI·주소의 결속

### 2.1 주신호 및 관련 신호

주소는 선언 TD/SAD·SSD AO(비트오프셋), 멤버 BO, BAD BIRID와 DepDB TOD의 DB번호를 대조했다. 현재 최적화 DB·온라인 주소·값은 미확인이다.

| 신호 | 형식/주소 | 원본 선언·위치 | 해석/경계 |
|---|---|---|---|
| Start LD01 | Bool %Q3.6 | `0602` RID145 AO30, NID29 UID849 Write; live_index doc1316 | 명령. 주석 a49.4를 실제 주소로 쓰지 않음 |
| LD-01_Fbk | Bool %I4.6 | `0613` RID224 AO38, NID37 UID2044; doc509 | 55KM1 보조응답, 물질유량 아님 |
| Flag.M_LD_01 | Bool DB2.DBX2.0 | `0604` RID143 AO16/BAD2→`0603` Flag DB2; NID29 UID846 Write/847 Read | 운전요청 Reset 대상 |
| Allarm.LD_01_FAULT | Bool DB3.DBX2.0 | `0604` RID141; `0657` RID113 AO16/BAD10→`0655` DB3; NID27 UID937/939/940 | 주모터 유지 고장 |
| Inputs.FEEDBACKMOTOR LD-01 | Bool DB13.DBX4.6 | `0604` RID229 AO38/BAD218→`0603` DB13; NID30 UID24; `0657` RID294/NID27 UID969 | 처리응답 |
| Start Vibrator LD-01 | Bool %Q3.7 | `0602` RID155 AO31 NID31 UID909 Write; doc1314 | LD01A 별도 명령 |
| LD-01A_Fbk | Bool %I4.7 | `0613` RID230 AO39 NID38 UID2098; doc510 | 56KM1 보조응답 |
| Flag.M_LD_01_VIB | Bool DB2.DBX2.1 | `0604` RID153 AO17, NID31 UID904 Write/905 Read | 진동기 요청, 출력과 별도 |
| Allarm.LD_01_VIB_FAULT | Bool DB3.DBX2.1 | `0604` RID152; `0657` RID117 AO17 NID28 UID971/973/974 | 진동기 유지 고장 |
| Inputs.FEEDBACKMOTOR-LD-01A | Bool DB13.DBX4.7 | `0657` RID295 AO39 NID28 UID1003 | 진동기 처리응답 |
| Inputs.VR-06 RUN | Bool DB13.DBX5.7 | `0604` RID227 AO47/BAD218, NID29/31 UID23 | 두 요청Reset의 의존 입력, VR06 소유 |
| LL_LD01 | Bool %I28.5 | `0627` RID142 AO229 NID1 UID95; doc947 | 전기 저레벨 원시입력 |
| Inputs.LD-01 Minimo | Bool DB13.DBX22.5 | `0629` RID149 AO181/BAD4→`0628` DB13, NID1 UID131 Write; `0573` RID82 | 물리I28.5와 주소가 다름 |
| 170FC1 | Bool %I28.6 | `0627` RID144 AO230 NID1 UID98; doc948 | 점검도어 원시입력 |
| Inputs.LD-01 Inspection LS | Bool DB13.DBX22.6 | `0629` RID150 AO182 NID1 UID136 Write; `0604` RID267 NID29 UID848 | 주모터 출력 허가 |
| 170SA1 | Bool %I28.7 | `0627` RID145 AO231 NID1 UID115; doc949 | 전기 PB14 현장셀렉터 |
| Inputs.LD-01 Local Button | Bool DB13.DBX22.7 | `0629` RID151 AO183 NID1 UID141 Write; `0604` RID268 NID31 UID32 | 이름 Button과 도면 Selector 차이 보존 |
| Allarm.LD_01_MIN | Bool DB3.DBX5.7 | `0573` RID42 AO47/BAD10→`0572` Allarm DB3; NID3 UID291/293/295 | 저레벨 알람. HMI Allarmi_48 |
| Tag_70 / Tag_71 | Timer %T75 / %T80 | `0658` RID111 AO75 NID27 UID934/935; RID115 AO80 NID28 UID968/969 | 모터별 S5 고장타이머, HMI태그 아님 |
| Tag_124 / Tag_125 | Timer %T40 / %T41 | `0602` RID147 AO40 NID30 UID875/879; RID149 AO41 UID876/878/880 | 간헐 휴지/작동 상호의존 |
| Start_LD01Vib | Local Bool, interface | `0605` RID151 S=Local, SSD S=D AO0, NID30 UID881 Write/NID31 UID907 Read | 내부 지역값. M/DB 고정전역 주소로 발명하지 않음 |
| ON / UNDER TESTING | Bool %M0.0 / %M5.5 | `0602` RID1 AO0 / RID4 AO45 | 공통허가/유지보수 조건, 항상TRUE·현장허가로 추정 금지 |
| Flag.RESET_ALLARM | Bool DB2.DBX6.0 | `0657` RID13 AO48 및 `0573` RID38, DepDB Flag DB2 | 공통고장Reset, 재요청 아님 |

### 2.2 원시 입력 전달과 Word 전체쓰기

- LAD1070 `0397`, HMI Inputs 색인1/NID1. ORef36/RID10 Tag180=`0627` Word/Input/AO32=%IW4가 W39→Move35.in, Move35.out1 W40→ORef37/RID11=`0629` Word/AO32/BAD4→`0628` Inputs DB13, 즉 DB13.DBW4로 전달된다. I4.6, I4.7, I5.7이 같은16비트 전송 안에 포함된다.
- Move22.eno→Move27.en(W34), Move27.eno→Move35.en(W41) 앞단 연쇄와 DisableENO=true 속성을 보존한다. 실제 TIA 버전의 ENO 처리·현재 호출을 확인하지 않았으므로 매스캔 무조건복사로 확정하지 않는다.
- 같은 LAD1070의 센서3개는 이 Word와 다르다. rail W21→Contact94/97/114, 각각 ORef95/RID142 LL_LD01(W92), ORef98/RID144 170FC1(W96), ORef115/RID145 170SA1(W99)를 읽는다. 출력 W134/139/144→Coil130/135/140, operand W133/138/143→ORef131/136/141다. 부호반전 없는 개별 Contact→Coil 전달로 I28.5/.6/.7→DB13X22.5/.6/.7을 결속했다. 물리 정상극성을 여기서 확정하지 않는다.
- main LAD1613 `0030`, 색인2/NID19: Recipes CRef21→HMI CRef23→HMI Output CRef25 ENO연쇄(W32/W33) 후, W42→NOT Simulation(1) Contact37→W43 HMI Inputs CRef28.en. CodeBlock29/RID135=`0688` HMI Inputs; ORef45/RID140=`0692` Simulation(1). 활성값·온라인 실행은 미확인이다.
- 정지 자료 선언 `0635`에 FEEDBACKMOTOR LD01 NID4 UID28, LD01A NID4 UID35, Local Button NID4 UID87, Minimo NID18 UID37의 Write가 있다. **정지자료에 다른 Writer가 존재함만 기록**하며 해당 자료를 실행·생성·시험하거나 현재 활성이라고 판단하지 않았다.

### 2.3 출력의 표시용 Word 전달

LAD356 `0401`, HMI Output 색인1/NID1: ORef35/RID28=`0632` Tag281, Word Output/AO16=%QW2가 W59→Move23.in; W61 Move23.out1→ORef36/RID50=`0633` Word/AO16/BAD26, `0064` Output DB14로 DB14.DBW2에 복사된다. Q3.6/.7이 이 범위에 포함된다. 앞단 Move22.eno→Move23.en(W57)을 확인했다. 방향은 **QW2를 읽어 DB14W2에 쓰는 것**이며 DB14가 Q3.6/.7을 쓰는 경로가 아니다. 실제 HMI가 이 영역을 읽는 화면 이벤트/표시는 별도 미확인이다.

### 2.4 HMI 설정과 미결속

`sources/hmi_plc_tags.csv`의 다음7행은 Access Name PLC, dde.cfg 설정이며 온라인 현재값이 아니다.

| 행 | HMI태그 | 주소 | 내부ID | 경계 |
|---|---|---|---|---|
|124|LD_01_MF\Allarme1|DB11,X48.1|0033E|DB3X2.0과 별도 표시영역|
|125|LD_01_VB\Allarme1|DB11,X50.1|0033C|DB3X2.1과 별도|
|412|LD_01_MF\RispostaA|DB11,X48.0|001BF|I4.6/DB13X4.6과 별도|
|413|LD_01_VB\RispostaA|DB11,X50.0|001BE|I4.7/DB13X4.7과 별도|
|447|LD_01_MF\Flag|DB2,X2.0|00197|요청주소 일치, 버튼/권한/실제Write 미확인|
|448|LD_01_VB\Flag|DB2,X2.1|00196|진동기 요청주소, 출력보장 아님|
|505|Allarmi_48|DB3,X5.7|0015D|저레벨 알람주소 일치, 메시지문구/확인동작 미확인|

LAD1201 `0377` hmi 색인24/title ld01 mf, LAD1202 `0378` 색인25/title ld01 vb는 원본 CRef22/RID638와 CodeBlock23/RID1이 `0624` 인터페이스와 `0623` HMI Standard Motors에 대응한다. network-map의 inferred_original_nid는 두 네트워크 모두 null이다. 이를 색인24/25로 임의 채우지 않는다.

| 핀/Wire | LD01 MF ORef/RID | LD01 VB ORef/RID | 색인상 후보와 확보 한계 |
|---|---|---|---|
|Ingresso_run / W37|24/667|24/666|LD01/LD01A 처리응답 후보. 이름선언 UID/RID/NID 결속 미확보|
|Allarme1 / W39|26/315|26/323|LD01_FAULT/LD01_VIB_FAULT 후보. 미결속|
|Allarme2~5 / W40~43|27~30/48|27~30/48|`0626` FALSE literal의 UID호출기록은 있으나 네트워크 최종NID 결속별도|
|Risposta / W46|33/318|33/326|Motors.LD01_MF/VB.Risposta 후보. 미결속|
|Comulativo_allarmi / W48|35/320|35/328|각 Motors 누적알람 후보. 미결속|

8개 비리터럴 데이터 ORef의 미결속을 보존한다. HMI설정행, 호출핀, DB11 구조, 함수 내부, 실제 화면 이벤트를 한 단계로 합쳐 “HMI 동작확인”이라고 쓰지 않는다. LD01_W/P의 현재 입력값·HMI쓰기 경로는 이 CSV 직접검색에서 확보하지 못했다.

## 3. 고유 제어 구조·다른 쓰기

### 3.1 LD01 요청Reset과 출력

LAD1958 `0259`, motors1 색인29/NID29, Part9/Wire16.

| 기능 | 원본 연결 | 정적 해석 |
|---|---|---|
|허가|rail W875→ON Contact863, operand ORef842/RID1(W850)|ON 공통허가|
|고장가지|ON863.out W864→Contact865, ORef843/RID141(W851); W866→OR831.in1|LD_01_FAULT|
|VR06가지|ON863.out→NOT Contact22, ORef23/RID227(W21); W24→NOT Contact869, ORef845/RID4(W853); W870→OR831.in2|NOT VR06처리Run AND NOT UNDER TESTING|
|요청Reset|OR831.out W855→RCoil836, ORef846/RID143(W857)|ON AND [고장 OR (NOT VR06Run AND NOT UNDER TESTING)]→M_LD_01 Reset|
|명령|ON863.out→M_LD01 Contact871(W858), W872→InspectionLS Contact873(W859), W874→Coil841, ORef849/RID145(W861)|ON AND M_LD01 AND 점검도어처리입력→Q3.6|

저레벨/현장셀렉터/NOT fault/VR06 Run을 모두 출력에 직렬로 넣은 회로가 아니다. 원문에는 요청Reset과 출력 가지가 따로 있다. 도어 입력0이면 위 출력 가지가 성립하지 않지만, 도어에 대한 별도 S/R 고장이나 안전등급 인터록을 발명하지 않는다. 같은 스캔 최종값·외부쓰기 순서는 미확정이다.

### 3.2 간헐진동 시간 변환과 내부Start

LAD1959 `0274`, motors1 색인30/NID44는 `KF_KT` FC109를 두 번 호출한다. `0058` RID241, `0059` RID248의 KF=Int/SEC=Bool/KT=Word 인터페이스를 대조했다.

| 경로 | 원본 | 주소·형식과 제한 |
|---|---|---|
|작동입력|ORef38/RID235→CRef36.KF(W37)|Data.LD01_W Int, `0604` AO2464/BAD20→`0603` DB1, DB1.DBW308|
|작동모드|ORef40/RID249→CRef36.SEC(W39)|`0606` Bool V0. 숫자0초 설정이 아님|
|변환결과|CRef36.KT→ORef43/RID148(W42)|Data.LD_01V_WorkTime Word/AO1200=DB1.DBW150|
|휴지입력|ORef46/RID236→CRef44.KF(W50)|Data.LD01_P Int/AO2480=DB1.DBW310|
|휴지모드|ORef47/RID249→SEC(W51)|동일 Bool0|
|휴지결과|CRef44.KT→ORef48/RID150(W52)|Data.LD_01V_PauseTime Word/AO1216=DB1.DBW152|
|호출연쇄|rail W21→CRef36.en, CRef36.eno W41→CRef44.en|두 번째 호출 앞단 ENO 영향 보존|

live_index doc457/458/460의 KF_KT 설명/검색용 STL은 SEC true=seconds, false=tenths, S5T 인코딩 변환이라고 설명한다. 이는 호출의 Bool0를0초로 읽지 않게 하는 보조자료다. 본 조사에서 원문 STL 명령 전체 복호화·컴파일·현재값은 확인하지 않았다. 따라서 작동/휴지시간을 임의 초수로 채우거나 설계 상한을 현장 안전 한계로 승격하지 않는다.

LAD1960 `0260`, 색인31/NID30, Part8/Wire16:

- ON Contact896→처리 피더응답 Contact23(W26), ORef24/RID229(W22). **주모터 명령 Q3.6이 아니라 DB13X4.6 처리응답을 공통허가로 읽는다.**
- W899→NOT Tag124 Contact900, W901→SdCoil861. WorkTime ORef874/RID148 W884→value; Tag125 ORef876/RID149 W887→operand. 즉 ON·처리Run·NOT T40가 T41 작동타이머 입력을 허가한다.
- 같은 W899→Tag125 Contact902, W903→SdCoil866. PauseTime ORef877/RID150 W888→value; Tag124 ORef879/RID147 W891→operand. T41 접점이 T40 휴지타이머 입력을 허가한다.
- 같은 W899→NOT Tag125 Contact904, W905→Coil871; ORef881/RID151 W894→Start_LD01Vib. 정적 식은 ON AND 처리Run AND NOT T41다.
- 이름·핀은 확인했으나 실제 주기·첫 주기의 잔존상태·타이머 재설정·설정0/비정상값의 결과는 미시험이다. 다른 설비의 간헐주기를 복제하지 않는다.

### 3.3 진동기 요청Reset과 대체 출력가지

LAD1961 `0261`, 색인32/NID31, Part12/Wire21. LD01A 소유의 관련 경로이며 본체 완료로 통합하지 않는다.

- ON925.out W926→VIB_FAULT Contact927(W911)→OR888.in1(W928), 그리고 NOT VR06Run Contact22(W21)→NOT UNDER TESTING Contact929(W24/W912)→OR888.in2(W930). OR888.out W913→RCoil891, ORef904/RID153 W915가 M_LD01_VIB를 Reset한다.
- 출력첫가지: ON925.out→M_LD01_VIB Contact931, operand ORef905/RID153(W916), W932→OR894.in1.
- 출력둘째가지: ON925.out→NOT VIB_FAULT Contact933, operand ORef906/RID152(W917), W934→Start_LD01Vib Contact935, operand ORef907/RID151(W918), W936→OR894.in2.
- OR894.out W25→Local Button Contact31, operand ORef32/RID268(W30), W26→Coil900, ORef909/RID155(W923). 따라서 검토 원문의 출력식은 ON AND [M_LD01_VIB OR (NOT VIB_FAULT AND Start_LD01Vib)] AND LocalButton이다.

VR06 처리Run 부재는 요청Reset 가지에 있다. 내부Start는 LD01 처리응답/타이머를 읽으며 직접 VR06을 읽지 않는다. 이 차이 때문에 요청Reset만 보고 즉시·무조건 진동정지라고 쓰지 않는다. 반대로 이 정적 식이 실제 진동을 계속시키거나 보호를 우회하라는 뜻도 아니다. 현재 호출·값·현장보호·실물·최종출력을 별도 확인한다.

### 3.4 상위호출과 공통 유지보수

- LAD1930 `0237` 색인1/NID1: ON47→Flag.Maintenance_ON49(W48), W50→Coil34 UNDER TESTING 및 Coil36 Allarm.Maintenance_ON. `0604` RID3 AO61=DB2X7.5, `0602` RID4 AO45=%M5.5다. 이 조건의 설명은 시험모드 사용·보호우회 승인/권고가 아니다.
- main LAD1619 `0031` 색인8/NID6: ON282.out W283→Allarms1 CRef264.en 및 Allarms2 CRef267.en. CodeBlock275/RID58,277/RID61은 `0688` 선언이다. 주/진동 고장과 저레벨은 서로 다른 블록에서 처리된다.
- main LAD1620 `0549` 색인9/NID7: ON350.out W351→Motors1 CRef319.en 및 time work motor CRef334.en. CodeBlock337/RID67,347/RID82은 `0688` 선언이다. 공통허가는 `0694` 인터페이스와 대조했다.
- 원본 motors1의 순서는 LD01요청/출력(29)→시간변환(30)→간헐Start(31)→진동기출력(32)다. main 색인상의 HMI/입력전달(2)·알람(8)·모터(9) 순서와 현재CPU 주기/중단/외부쓰기를 구분한다. 인용 순서만으로 온라인 최종값·즉시성/지연을 확정하지 않는다.

### 3.5 명명 비트검색을 넘는 다른 Writer

전체 IdentXmlPart 선언의 이름검색에서 M_LD01/ M_LD01_VIB의 명명 Write는 각각 NID29 UID846 Reset, NID31 UID904 Reset이다. 자동시동 명명 Set은 이 검색에서 찾지 못했다. **수동전용·HMI유일Writer·자동불가능의 증거가 아니다.** 전체Word·HMI·정지자료·간접 접근·현재CPU의 다른 코드를 같이 구분해야 한다.

| 대상 | 원본·핀 | 해석과 미확정 |
|---|---|---|
|DB2X2.0/.1 요청|startup only LAD402 `0147` 색인2/NID2: ON208→Move138(W209), eno W187→Move141; Int0 ORef170/RID54 W188→in, out1 W189→ORef171/RID9|`0563` RID9 Word/AO16/BAD6→`0562` Flag DB2, DB2W2 전체0. 두 요청 포함|
|DB3X2.0/.1 고장|LAD403 `0148`: ON329→Move250(W330), eno W306→Move253; Int0 ORef287/RID54 W307, out1 W308→ORef288/RID26|`0563` RID26 Word/AO16/BAD23→DB3W2 전체0. 두 모터고장 포함|
|DB3X5.7 저레벨고장|같은LAD403 Move253.eno W309→Move256.en, Int0 ORef289/RID54 W310, out1 W311→ORef290/RID28|`0563` RID28 Word/AO32/BAD23→DB3W4 전체0. byte4~5의 저레벨 포함|
|DB13X4.6/.7/5.7 처리응답|LAD1070 Move35, IW4→DB13W4|원시범위16비트 전송; 독립BOOL만의Writer로 축소 금지|
|DB13X22.5/.6/.7 센서처리|LAD1070 개별Coil130/135/140|I28원시와 주소 다름. Word22 복사라고 가정 금지|
|처리응답·저레벨·셀렉터|`0635` NID4/18 선언의 관련 Write|정지자료 참조, 실행/활성 미판정|
|요청2개|HMI CSV447/448|주소 설정은 외부Write 가능 경계, 실제Write 증거 아님|
|시간설정Word|LAD1959 `0274` KT→DB1W150/W152|외부 입력/변환/초기값·설정시각은 별도|
|가동시간Word|LAD1035/1036 Move1, LAD1052 Move0|§5.3. 영구 총시간으로 간주 금지|

LAD403 network-map NID=null은 보존한다. 여기 인용한 ON UID284/RID1(`0047`), 상수UID287/289 RID54(`0048`), 목적지UID288/290 RID26/28(`0563`)가 모두 선언NID3인 것과 DB결속을 대조해 선택경로만 결속했다. 블록이름 startup only를 실제 전원재시작·현재 OB설정·초기화 수행증거로 쓰지 않는다.

## 4. 전기 전달 경로·자료 상충

전기 PDF56/57/121/122/140/171/178/256, 시공 PDF36/51/60, P&ID p1의 서로 다른12페이지를 실제 렌더해 시각검토했다. P&ID 회전렌더는 같은1페이지를 다시 본 것이며 페이지수를 늘리지 않았다.

### 4.1 LD01/M32 주회로와 명령·응답

| 경로 | 실제 위치 | 확인한 양 끝점·중간경로 | 경계 |
|---|---|---|---|
|주전원|FG55/PDF56|440V/60Hz 표기 8.3L1/L2/L3(54/9)→55QM1 1/3/5–2/4/6→55KM1 1/3/5–2/4/6→55U1/V1/W1→XM55U1/V1/W1→55QS1 1/3/5–2/4/6→M32 U/V/W, PE|실전압·상순서·회전·명판 미확인|
|출력모듈|FG139/PDF140|CPU515 MOD14 A3.6 단자37→참조55/4→FG55 A3.6(139/1)|현행모듈형번·단자·출력전압 미확인|
|모듈전원|FG139/PDF140|+24Vdc10.9→X21 3031 4A F 5×20→139.1→단자39; −0Vdc10.6→단자40|퓨즈/실전압·부하 미확인|
|접촉기제어|FG55/PDF56|A3.6→XS47→55QS1 보조→XS48→선55.1→55QM1 보조→55KM1 A1; A2→−0Vdc10.6|QS/QM 보조접점 숫자단자는 원문에서 명확히 확보 못함|
|원시응답|FG55/PDF56+FG120/PDF121|+24Vdc10.7→55KM1 보조13–14→E4.6(120/6)→CPU515 MOD9 E4.6 단자7(역참조55/6)|접촉기응답이며 축/유량센서 아님|
|입력모듈전원|FG121/PDF122|같은MOD9의 +24Vdc10.7→X21 3008 2A IST.5×20→121.1→단자20; −0Vdc10.6→단자19|FG120에는 전원단자 별도 미표시, 인접MOD9 시트와 결속|

주접점1/2·3/4·5/6, 코일A1/A2, 보조13/14는 다른 경로다. Q3.6=1이 코일여자·접촉기폐로·기계회전·정량 투입의 증거가 되는 것은 아니다. 문서상의 접점기호와 실제 정상극성을 분리한다.

### 4.2 관련 진동기 회로의 별도 소유

FG56/PDF57은 LD01A/M33: 8.3L1/L2/L3(55/9)→56QM1→56KM1→56U1/V1/W1·XM56U1/V1/W1→56QS1→M33 U/V/W/PE다. 각3상장치의 주접점은1/3/5–2/4/6이다. Q3.7은 FG139 MOD14 단자38→A3.7(56/4)→XS49→56QS1 보조→XS50→선56.1→56QM1 보조→56KM1 A1/A2(−0Vdc10.6)로 연결된다. +24Vdc10.7→56KM1 보조13–14→E4.7(120/7)→FG120 MOD9 단자8이다. 이 경로를 M32 주모터 경로에 합치지 않는다.

### 4.3 저레벨·점검도어·현장셀렉터

FG170/PDF171과 FG177/PDF178의 실제 끝점을 대조했다.

| 경로 | FG170 원본 | FG177 수신 끝점 | 미확정 |
|---|---|---|---|
|저레벨기기 전원|110Vac152.8→X3 109(2A F 5×20)→170.1→LD-01; 반대전원→X3 110→0Vac9.9|전원과24V접점 회로를 분리|명판전압·내부단자·현행기종|
|저레벨응답|+24Vdc152.5→X3 111(2A F)→170.2→LD-01 접점→X3 112→E28.5(177/5)|E28.5(170/2)→X22 4008→CPU515 MOD4 Rack3 단자6|P&ID LT01과 실물 센서 동일성/정상극성|
|점검도어|+24Vdc152.5→X3 113(2A F)→170.3→170FC1 11–12→X3 114→E28.6(177/6)|E28.6(170/3)→X22 4009→MOD4 Rack3 단자7|문열림/닫힘 실제극성·안전등급|
|현장셀렉터|+24Vdc152.5→X3 115(2A F)→170.4→170SA1/PB14 13–14→X3 116→E28.7(177/7)|E28.7(170/5)→X22 4010→MOD4 Rack3 단자8|셀렉터위치·Button명칭 차이·실제배선|

전기 도어접점11–12와 PLC 부호반전 없는 복사/출력접점을 확인했어도 어떤 물리 위치가“정상1”인지 단정하지 않는다. 입력강제·보호 회로 우회·활선작업을 이 초안에서 요청하지 않는다.

### 4.4 BOM·케이블·개정 상충

- FG253/PDF256: 55KM1/56KM1은 Siemens 3RT2015-1BB41(CONTACTOR3KW/1L/DC24V/S00), RC부속3RT2916-1CB00이다. 각각QM 그룹은 보조3RV2901-1E, 결합부품3RA1921-1DA00, Whoner WR32433 어댑터, 보호기본체 Siemens3RV2011-1DA10(MAGNETOTHERMIC2.2–3.2A)로 여러 행이다. 각 수량1. 첫QM행의 보조접점 형번을 보호기본체로 읽지 않는다.
- FG55/56의 모터표기0.18kW·0.55A와 QM범위2.2–3.2A 차이가 BOM에도 존재한다. 오타·기존설계·실물오장착 중 어느 것인지 이 자료만으로 결정하지 않는다. 보호기 실제품번/다이얼·모터명판·승인변경자료를 대조해야 한다. ABB현행모델·대체형번·토크·안전 한계·정비주기를 추정해 채우지 않는다.
- 시공p36(DWG CANDC-CONS-E019-036)은 DUST ZONE02/212RAD1의1번 Pipe16→LD01/M32,2번 Pipe16→LD01/M33으로 그린다. p51(CANDC-CONS-C001-051)의 모터케이블1_24 `=DUS+LD01-M32A`,1_25 `=DUS+LD01-M33A`는 CR→M32/M33, GAC/CV/CORE4/SIZE1.5/SPARE0, 경로100→200→210→211→212RAD1→각E100/E200, Adjustment6/LEN118이다. LEN118은 표의값이며 실측 길이·길이단위를 추가 확정하지 않았다.
- 시공p36/p60(CANDC-CONS-C010-060)은 DUS2TB1에서 LT01·68FC1·PB14·LD01로 분기한다. p60 케이블10_13 `=DUS+LD01-LT01A`(DC/CVV/2C/1.0/E420, Adjustment3/LEN3),10_14 `=DUS+LD01-68FC1A`(DC/CVV/2C/1.0/E430,3/3),10_15 `=DUS+LD01-PB14A`(DC/CVV/5G/1.0/SPARE2/E440,3/4),10_16 `=DUS+LD01-LD01A`(AC/CVV/3G/1.0/E410,3/4)가 있다. 접미 LD01A인10_16은 이 표에서 FROM DUS2TB1→LD01 계장전원 가지이므로 M33 진동기 케이블1_25와 합치지 않는다.
- **시공 도어관련 태그68FC1과 전기/PLC170FC1의 번호 차이**를 보존한다. 양자가 같은 현장 도어라는 확정 단자 대조가 없다. P&ID LT01, 전기의 LD-01 LOW LEVEL, 시공 LT01과 LD01 전원가지 역시 별도 확인이 필요하다.
- 시공p60의10_3 DUS2TB1C에는 AC(220V) 표기가 있고 전기FG170의 저레벨기기전원은110Vac다. p60의10_2/10_16과10_3을 동일회로로 임의 묶지 않는다. 서로다른 전원 용도일 수 있으나 정확한 공급·코어·단자 결속은 미확정이며 임의전압대체 금지다.

## 5. 알람·복구·시간 기록

### 5.1 모터별 고장2초

| 항목 | LD01 주모터 | 관련 LD01A 진동기 |
|---|---|---|
|위치|LAD1805 `0439`, allarms1 색인25/NID27|LAD1806 `0440`, 색인26/NID28|
|타이머입력|ON955→Start957(W956), Start.out W958→NOT Run968(W971), W21→SdCoil919|ON989→Start991(W990), Start.out W992→NOT Run1002(W1005), W21→SdCoil953|
|설정/타이머|value ORef933/RID28 W943, operand ORef934/RID111 W944|value ORef967/RID28 W977, operand ORef968/RID115 W978|
|타입/주소|`0656` S5Time S5T#2S V512, Tag70/%T75|동일형식 원문2초, Tag71/%T80 별도|
|Set|Start957.out→Tag70 Contact959(W945), W22→SCoil925; ORef937/RID113(W948)|Start991.out→Tag71 Contact993(W979), W22→SCoil959; ORef971/RID117(W982)|
|Reset|ON955→RESET Contact963(W950)→fault Contact965(W964/W951)→RCoil930(W966); ORef940(W953)|ON989→RESET Contact997(W984)→fault Contact999(W998/W985)→RCoil964(W1000); ORef974(W987)|

타이머입력은 ON AND 명령 AND NOT 처리Run이고, Set 가지는 ON AND 명령 AND 타이머접점이다. NOT Run은 Set 코일에 다시 직렬로 들어 있지 않다. V512는 S5Time 원문 인코딩이며512ms가 아니다. 주모터·진동기 타이머를 공유한다고 쓰지 않는다. 실제 지연·현재값·동시Set/Reset 우선·재발은 미시험이다.

### 5.2 저레벨 TON10초와 해제 조건

LAD1228 `0161`, allarms2 색인3/NID3, `0574` RID78는 TON 명령, LRef21/Instance22 RID79는 `0052` Min_LD_01/DB33(IEC_TIMER)다. `0571` RID81의 Time T#10S/V10000이 ORef24→PT(W23)에 연결된다. 모터 S5타이머와 타입/소유가 다르다.

- ON Contact306.out W307→Minimo Contact308, ORef30/RID82(W29); W27→TON21.IN. 반전 접점이 아니다.
- TON21.Q W25→SCoil282; ORef291/RID42 W299→Allarm.LD_01_MIN=DB3X5.7. ET W26→ORef28은 RefId가 없으므로 목적지 미결속으로 남긴다.
- Reset은 ON306.out→RESET Contact310(W300), W311→고장Contact312(W301), W31→NOT Minimo Contact314(W33), W32→RCoil288, ORef295/RID42(W304)다. **ON AND RESET_ALLARM AND 저레벨고장 AND NOT 처리Minimo**를 요구한다. 저레벨조건이 남아 있는 상태의 Reset을 복구로 쓰지 않는다.
- LAD1958 주모터 직접식에서 LD_01_MIN 고장접점을 찾지 못했다. 따라서 이 네트워크의 직접운전차단이라고 쓰지 않는다. 전체 공통알람·상위허가의 간접영향까지 없다고 확정한 것은 아니다.
- HMI Allarmi_48 주소일치는 표시설정의 근거다. 알람번호48을 현장장치/타이머번호로 바꾸거나 화면메시지·acknowledge 이벤트를 추정하지 않는다.

### 5.3 가동시간의 Move1과 공통Move0

`0615`와 `0614` DB9 결속: LD_01_MIN AO1152=DB9.DBW144, LD_01_HOUR AO1168=DB9.DBW146, LD_01_VIB_MIN AO1184=DB9.DBW148, LD_01_VIB_HOUR AO1200=DB9.DBW150(모두Int). DB1.DBW150의 WorkTime과 DB번호가 다르다.

- LAD1035 `0322`, time work motor 색인34/NID37: Tag47 Contact2072→**원시 I4.6** Contact2074(W2073/W2056), W2075→Add2026.en/Ge2033.pre. Add는 MIN ORef2045/RID226+상수1 ORef2046/RID7→동일MIN2047(W2057~2059). Ge는 MIN2048와60 ORef2049/RID8(W2060/2061), W2062→Move2036.en. Move2036.in은 **상수1** ORef2050/RID7(W2064), out1 W2065→HOUR ORef2051/RID228다. HOUR+1 Add가 아니다. eno W2066→Move2039 MIN0(W2067/2068), eno W2069→SCoil2042 Flag_Aggiorna_DB(W2070).
- LAD1036 `0323`, 색인35/NID38도 별도 원시I4.7 Contact2128를 읽는다. Add2080 MIN+1(W2111~2113), Ge2087 MIN≥60(W2114/2115), Move2090 **상수1** ORef2104/RID7(W2118)→VIB_HOUR ORef2105/RID234(W2119), Move2093 MIN0(W2121/2122)→SCoil2096 업데이트요청이다. 두모터의 원시·처리Run 용도를 혼동하지 않는다.
- LAD1052 `0339`, 색인51/NID54: Tag48 Contact3049(W3034)→Move3008 FN01_FAN_HOUR0, eno W3037→Move3011 LD01_HOUR0(ORef3026/RID12 W3038, out1→3027/RID228 W3039), eno W3040→Move3014 VIB_HOUR0(ORef3028/RID12 W3041, out1→3029/RID234 W3042). 이후SC10/SC11로 계속되는 공유ENO 연쇄다. LD01만의 독립Reset허가로 축소하지 않는다.
- Tag47=%T13, Tag48=%T17은 `0613` RID1/AO13, RID284/AO17이며 Flag_Aggiorna_DB는 RID13/AO15=%M1.7이다. LAD1056 `0019` NID58 NOT Tag47 Contact3120→SdCoil3112, S5T#1M ORef3114/RID335(W3117), 타이머operand3116/RID1(W3119)를 확인했다.
- LAD1055 `0341` NID57: ON3147→Flag_Aggiorna_DB3149→SCoil3110 MEM2_0; MEM2_0 Contact3151→NOT Flag_Aggiorna_DB3153→SdCoil3118(S5T#5S, ORef3128/RID334, Tag48). Tag48 Contact3155→RCoil3123 MEM2_0. 제목의“DB기록후Reset”을 실제 영구저장완료 handshake 증거로 쓰지 않는다.

시간/업데이트요청을 총누계·정비주기·실제영구저장 완료로 단정하지 않는다. HOUR Move1을 오타로 판단해 PLC를 고치지 않는다. 실제 외부 누적·저장/초기화 이력이 추가증거다.

### 5.4 Reset·재요청·현장복구 분리

주/진동 고장Reset은 요청을 새로 만들지 않는다. 요청Reset, 고장Reset, 타이머상태, 도어·현장셀렉터·VR06응답, 간헐 대체가지·Word초기화, HMI쓰기 시각을 같이 보아야 한다. 저레벨은 원조건 해소가 논리Reset에도 필요하다. 알람창소거·DBbit0을 원인제거·재기동·정량 투입·현장복구로 표시하지 않는다. 실제 조치/재요청은 자격자·승인안전 절차·원인제거/재발없음 기록이 필요하며 본 조사에서는 수행하지 않았다.

## 6. 증상별 관찰·수리 판단

아래는 정적 원본과 비교할 관찰 지점이다. 현장작업·활선측정·입력강제·보호우회·설정변경 지시가 아니다.

| 증상 | 관찰 위치/같은시각 값 | 비교·원인배제 근거 | 복구판정의 경계 |
|---|---|---|---|
|피더요청이 바로 사라짐|DB2X2.0, DB3X2.0, VR06 DB13X5.7, M5.5, DB2W2 초기화/HMI쓰기시각|LAD1958 Reset 두가지·재시작Word·명명Writer검색|요청보유와 출력/회전 별도|
|피더요청은 있으나 Q3.6 없음|ON, DB13X22.6, 원시I28.6, 현재 호출·최종쓰기|LAD1958 Contact871/873, LAD1070 도어전달|도어정상극성·시공태그 동일성 미확정|
|Q3.6인데 회전없음|MOD14/37, XS47/48,55QS1/QM1,KM1 A1/A2·주회로,M32|FG55/139·실물명판·보호범위차이·전원/기계상태|화면bit1과 물리회전/투입량 분리|
|기동 후 주모터고장|Q3.6,T75,I4.6,DB13X4.6,55KM1 13/14|LAD1805 S5T2초·IW4전달·다른Writer·응답배선|고장해제와 원인제거/재요청 분리|
|진동기요청 껐는데 진동명령있음|DB2X2.1,Start_LD01Vib,T40/T41,DB13X4.6,DB3X2.1,DB13X22.7|LAD1960/1961 병렬대체가지·현장셀렉터|요청0=출력0 오판금지,실물진동 확인별도|
|진동이 시작안됨/주기이상|I4.6/DB13X4.6,DB1W308/W310,W150/W152,T40/T41,LocalButton|KF_KT Bool0·ENO·작동/휴지순서·현재값|설정값/안전범위 미확정,임의 초수수정금지|
|진동기고장|Q3.7,T80,I4.7,DB13X4.7,56KM1 13/14|LAD1806 별도S5타이머·FG56/120/139|주모터T75/55KM1에 합치지 않음|
|저레벨알람 지속/Reset안됨|I28.5,DB13X22.5,DB33 TON,DB3X5.7,RESET_ALLARM|LAD1228 10초·NOT Minimo Reset·110Vac전원/24V접점 분리|센서고장과 실제석회부족 구분,원조건 해소|
|HMI응답/고장과 원시값 다름|I4.6/.7→DB13W4,DB11X48/50,HMI호출·통신시각|8미결속ORef·실제이벤트·표시주소·QW2→DB14W2|화면문제를 즉시 기계고장으로 확정금지|
|가동시간값 이상|I4.6/.7,T13/T17,DB9W144~150,M1.7,외부저장시각|Move1/Move0·공유ENO·원시입력허가|영구총시간/정비주기 추정금지|

관찰 기록에는 관찰자, 시각/시간대, 설비/단자/화면 위치, 값/단위, 수집장치, 온라인 프로젝트 근거, 비교 원본, 배제결과, 조치, 재요청·재발없음·실물복구 증거가 필요하다. 사용자 운영기록·사진·SEJIN 자료를 이 초안이나 공개저장소로 복사하지 않았다.

## 7. 기능·검증·완료 경계

### 7.1 네 기능과 기록 보존

| 기능 | 적용 방향 | 이번 상태 |
|---|---|---|
|도면·래더 나란히 비교|FG55↔LAD1958/1805; FG170↔LAD1070/1228; 관련FG56↔LAD1960/1961/1806|원본근거 후보확보,제품UI·강조·왕복링크 미구현/미검증|
|백업·선택복원|LD01 고유 ID, LD01A/LT01별도 키, note/repair_observation/미지필드·타설비 보존|구현/저장·재읽기·재열기·복원시험 미수행|
|기록 전후비교|명령/원시/처리/표시·프로젝트·시각·단자 대조 분리|합성/운영기록 작성·비교시험 미수행|
|보고서/PDF|주소/소유/FG-PDF/시공상충·미확정·복구기준 전달|Markdown 조사초안만,제품보고서·PDF출력 미검증|

### 7.2 자료 부족과 판정 기준

1. 현재 TIA 프로젝트/CPU 교차참조·OB/블록호출·간접/외부 Writer 자료: 원본 고정판과 현재 실행·주소·초기값·최종값을 결속한다. 이번에는 컴파일/다운로드/온라인/강제시험을 하지 않았다.
2. HMI 원본 DB11/이벤트·태그쓰기/권한·통신시각: MF/VB의8개 데이터 ORef를 UID/RID/NID·선언/DB11주소로 결속하고7개 설정행의 실제 용도를 확인한다. 주소 설정만으로 UI완료 처리하지 않는다.
3. LD01/LD01A 모터·QM/KM/QS 명판/승인전기변경표·보호 검토서: 0.55A와2.2–3.2A의 문서 차이를 해소한다. 사진/운영이력의 공개복제 없이 승인수집 범위에서확인한다.
4. 170FC1/68FC1, LT01/LD01 레벨기기, PB14, DUS2TB1 코어·단자·전원 구분과 승인준공도: 양 끝점이 동일한지,110Vac·220Vac 가지가 어떤 장치인지 대조한다. 도면번호/설계표만으로 같은 회로라고 표시하지 않는다.
5. KF_KT 원문 STL/현재 DB값·설정이력: Bool0와 작동/휴지시간 단위를 결속하고 현재 작동/휴지값을 관찰한다. 안전 한계/설정변경은 이번 범위가 아니다.
6. 원인제거·안전 절차·재요청·같은시각전기/논리/실물관찰 및재발없음: 실제 복구 근거. 문서/정적검사만으로field_recovery를 완료하지 않는다.

### 7.3 수행과 미수행

- 수행: 고정Git/상태확인, 읽기전용 preflight, 고유XML선언/핀/호출/Word·다른Writer 정적검토, 원본PDF12페이지 시각검토, 원본파일 SHA-256/Git blob 대조, 정적 선언/연결 단언163개 통과(스크립트 종료0).
- 미수행: 제품코드/대장/버전/운영기록 수정, 통합, npm/build/패키지·ZIP 재생성, PC/모바일UI·글자크기·검색/선택복원, 저장/재열기·동시성/실패/구형미지필드 기능시험, BC01실행회귀, GitHub/Netlify게시, TIA컴파일/현재CPU/현장복구.
- 중지5자산은 해시로만 보존검사했다. 시뮬레이터·금지생성기·행동시험 실행0. 해시일치는시뮬레이터의 동작검증이 아니다.
- 기존18불일치/1060확인대기/577설계시험을 새로운해결·실행완료로 변경하지 않았다.
- 독립검토는 부모/후속검토자가 별도 수행해야 한다. 이 초안의 자가정적검토를 독립승인으로 표시하지 않는다.

| 상태분류 | 결과 | 제한 |
|---|---|---|
|documentation|draft_ready|LD01 고유 조사초안, 하위/외부완료 아님|
|static_review|self_review_completed|선택근거 범위,독립 검토 대기|
|ui_records|not_run|기능구현/기록기능시험 없음|
|publication|not_published|로컬2차133 통합제외 유지|
|tia_compile|not_performed|현재 프로젝트 컴파일 없음|
|live_cpu|not_performed|다운로드/온라인/강제/실행시험 없음|
|field_recovery|not_performed|현장정비/설정/안전 한계 변경 없음|

## 부록 A. 의미검토 위치 목록

| 원본XML | LAD / 색인 / NID | 검토 범위 |
|---|---|---|
|0259|1958 / 29 / 29|LD01 Reset·점검도어 출력|
|0274|1959 / 30 / 44|KF_KT 2호출·Bool0·DB1Word|
|0260|1960 / 31 / 30|작동/휴지 타이머·지역Start|
|0261|1961 / 32 / 31|진동기 Reset·병렬대체출력|
|0439|1805 / 25 / 27|LD01 S5고장2초·Set/Reset|
|0440|1806 / 26 / 28|LD01A S5고장2초·Set/Reset|
|0161|1228 / 3 / 3|저레벨TON DB33·10초·원조건 해소Reset|
|0397|1070 / 1 / 1|IW4→DB13W4 및I28.5/.6/.7개별전달|
|0401|356 / 1 / 1|QW2→DB14W2 표시용전달|
|0377|1201 / 24 / null|HMI MF 호출핀·4데이터 ORef 미결속|
|0378|1202 / 25 / null|HMI VB 호출핀·4데이터 ORef 미결속|
|0147|402 / 2 / 2|DB2W2←0|
|0148|403 / 3 / null, 선택선언3|DB3W2/W4←0|
|0237|1930 / 1 / 1|유지보수조건→UNDER TESTING|
|0322|1035 / 34 / 37|원시I4.6·MIN·HOUR Move1|
|0323|1036 / 35 / 38|원시I4.7·VIB MIN·HOUR Move1|
|0339|1052 / 51 / 54|공유시간Reset Move0·ENO|
|0019|1056 / 55 / 58|Tag47 S5T1분|
|0341|1055 / 54 / 57|시간업데이트/5초Reset 조건경계|
|0030|1613 / 2 / 19|HMI/Output/Input ENO·Simulation조건|
|0031|1619 / 8 / 6|Allarms1/2 ON호출|
|0549|1620 / 9 / 7|Motors1/time work motor ON호출|
|0273|1973 / 44 / 43|외부LIW Q6.1 별도소유·Set/Reset경계|
|0472|1691 / 13 / 16|외부LIW %QW302:P 목적지경계만|

위24개 LAD는 전부의 프로그램을 의미검증했다는 뜻이 아니다. 일부 공유 네트워크는 명시한 선택 가지·목적지만 검토했다. `extracts/LD01/`의 선언/refs/wires/렌더·검사 파일은 추출 증거이며 원본을 대신하지 않는다. 해시 대상 수,24개 LAD 범위,12개 원본 페이지 수,정적 단언 수를 별도로 집계한다.

## 부록 B. 원본 바이트 보존

아래 파일별 SHA-256은 고정커밋의 Git blob 내용으로 다시 계산한 SHA-256과 대조했다. Git blob 객체ID(SHA-1)는 별도 manifest에 기록했다. 동일하다는 표시는 바이트 보존이며 파일 전체의 의미검토가 아니다.

바이트 보존 대상 **90파일** 모두 고정 Git blob 내용과 SHA-256 일치, 중지 **5자산**의 지정해시도 일치했다. 시작·종료 원본 Git 변경0이다. 별도 의미검토는 **24개 LAD의 명시된 범위**, 시각검토는 **12개 원본 PDF페이지**, 정적 텍스트·연결·선언 단언은 **163개 통과**다. 이 수들을 완료 설비 수 또는 TIA/현장 검증 수로 합산하지 않는다.

| 원본 상대경로 | SHA-256 |
|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` |
| `.agents/skills/gme-equipment-rollout/scripts/preflight.py` | `395067d6da20af3e1d82a43b7936907a87a44d8d2e11e4ebc61b1fc441e2adb6` |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` |
| `all-in-one/sources/decoded-original/0019-FlgNet.xml` | `a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5` |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` |
| `all-in-one/sources/decoded-original/0052-IdentXmlPart.xml` | `fbd673549a61f7da169e452e2221da4958b29b3e3c1c3699e9cad3d02577500a` |
| `all-in-one/sources/decoded-original/0058-IdentXmlPart.xml` | `84db55242df6a85df73776bfd23bf16cc10e4da35fedca4942f4a43bc4cd1702` |
| `all-in-one/sources/decoded-original/0059-IdentXmlPart.xml` | `f02ef8f08f1c7ca7625bdbcf90a2c9365f12654d19e2e526fe8e5b0b742263d0` |
| `all-in-one/sources/decoded-original/0064-IdentXmlPart.xml` | `ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d` |
| `all-in-one/sources/decoded-original/0147-FlgNet.xml` | `386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c` |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` |
| `all-in-one/sources/decoded-original/0161-FlgNet.xml` | `3c4804a56f612d0e1884e29c892c21f681698dc1ccb40c6c53ac88fcb0f63a4c` |
| `all-in-one/sources/decoded-original/0237-FlgNet.xml` | `ad3721660c2f357e76c1a351f7898691271f35c341efe775e5780d749b2c4aa0` |
| `all-in-one/sources/decoded-original/0259-FlgNet.xml` | `872a7149ef118f82addce8b038d42418f532c065f2191018d85aed93406dd8b5` |
| `all-in-one/sources/decoded-original/0260-FlgNet.xml` | `c0812e84eaac7d42ef9b89f2947ac162a5dd0364424fb51d2a6ccae8297f42ac` |
| `all-in-one/sources/decoded-original/0261-FlgNet.xml` | `2cb282a051d3767e256d319453453499c5cc339b725ed78e3e263466f0ef8498` |
| `all-in-one/sources/decoded-original/0273-FlgNet.xml` | `48cc05ab4fb2778e2878b53993f10a31250dfeadd8b56024af4647a1e1da7f31` |
| `all-in-one/sources/decoded-original/0274-FlgNet.xml` | `4cd023464a66193239fe70b782cb1271f7c9d06b97f53dd80e4c81d80014cd66` |
| `all-in-one/sources/decoded-original/0322-FlgNet.xml` | `2807f177fb91e2aa07e71dc9a608f4fbf5a91b1079dd6b7fca06bc72e098c28a` |
| `all-in-one/sources/decoded-original/0323-FlgNet.xml` | `2c71fa2f9c4598d2f0596bc796042d42ab78103e0ddba940c85f06ec595e9a42` |
| `all-in-one/sources/decoded-original/0339-FlgNet.xml` | `ce2c6279b55c8a5ac837a0f7c7a0945636df7dc52b68a1c3d6ec158234b37543` |
| `all-in-one/sources/decoded-original/0341-FlgNet.xml` | `e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96` |
| `all-in-one/sources/decoded-original/0377-FlgNet.xml` | `a157e2098e1e76c30823c47e734a447e299334cc30765e8307df6fc2a9ecded2` |
| `all-in-one/sources/decoded-original/0378-FlgNet.xml` | `51c9c18d1029cbf45669702fbdd81061fd7121d49fd3e2f4b2cb558c3365ae3a` |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` |
| `all-in-one/sources/decoded-original/0401-FlgNet.xml` | `60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae` |
| `all-in-one/sources/decoded-original/0439-FlgNet.xml` | `8d2dd5a867874dd0e079047c3cf73aa9cbb3fb43b02046820565d39ac2fea6ac` |
| `all-in-one/sources/decoded-original/0440-FlgNet.xml` | `a7e71653147751d8e9579dbb9a5be101b531c03612843cd0cb96cf86d6d179d4` |
| `all-in-one/sources/decoded-original/0472-FlgNet.xml` | `903cd4c143ad8020796f3bd2e309d7aee9c537aab9be7ac7a20cc00fdb2ac413` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` |
| `all-in-one/sources/decoded-original/0570-IdentXmlPart.xml` | `9fed133006458c3b43b1d5f2c15107a5a86b4fb7cdbaf3743bf88f0e5a105495` |
| `all-in-one/sources/decoded-original/0571-IdentXmlPart.xml` | `4a9deeb65a22e497e284fe6d98929e1d201ef5939e4aeca5805b4eb7e007d398` |
| `all-in-one/sources/decoded-original/0572-IdentXmlPart.xml` | `5ecd18f84e12d702bb46f759b23994dacfa2d97d50fe51e766ca0cf43f75bb4c` |
| `all-in-one/sources/decoded-original/0573-IdentXmlPart.xml` | `a22cc24a974e0c792f32e356a14b277a847e2bb204c91bce01c37d1714ddb56c` |
| `all-in-one/sources/decoded-original/0574-IdentXmlPart.xml` | `0773bc969180298193ed6affe56b485bd2141949f4467dcaf33afbb16ee496cf` |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` |
| `all-in-one/sources/decoded-original/0613-IdentXmlPart.xml` | `09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb` |
| `all-in-one/sources/decoded-original/0614-IdentXmlPart.xml` | `c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294` |
| `all-in-one/sources/decoded-original/0615-IdentXmlPart.xml` | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` |
| `all-in-one/sources/decoded-original/0616-IdentXmlPart.xml` | `650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d` |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` |
| `all-in-one/sources/decoded-original/0626-IdentXmlPart.xml` | `a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` |
| `all-in-one/sources/decoded-original/0632-IdentXmlPart.xml` | `fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9` |
| `all-in-one/sources/decoded-original/0633-IdentXmlPart.xml` | `9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc` |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` |
| `all-in-one/sources/decoded-original/0664-IdentXmlPart.xml` | `68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` |

## 다음 작업

- 완료 커밋: 없음. 조사초안과 자기 추출 경로만 작성했으며 고정 원본은 읽기 전용이다.
- 첫 후속조치: LD01 고유 핀/주소·출력대체가지·저레벨TON·FG55/170 실제끝점·BOM/시공상충을 독립 재검토한다. 추가 현장 자료가 없으면 미확정을 유지한 채 독립된 다음 조사로 넘긴다.
- 로컬2차133 통합제외는 계속 유지한다. LD01A·LT01·VR06·외부LIW의 주체/완료수·운영기록을 이 부모초안으로 바꾸지 않는다.
