# VR04 로터리 밸브 원본 조사 초안

VR04는 P&ID에서 BF01 하부 SC10 출구의 로터리 밸브 VR-04/M38로 표시된다. 전기 원본의 명령은 Q4.4, 응답은 I5.5이며 62KM1 접촉기 직접기동 회로다. **I5.5는 62KM1의 13–14 보조접점 응답이다. 축 회전·분진 배출 완료를 직접 검출하는 신호로 확인되지 않았다.**

고유 원본에서 전용 고장 2초, 자동 요청 Set/Reset, SC10 요청 해제, FN04 공유 예고장, BF01 세정 허가와의 연결을 확인했다. BF01 세정용 Forza_Lavaggio에는 타이머 이외 ON의 별도 OR 가지가 있다. 운전시간 HOUR는 Add가 아니라 Move 상수1이며, startup only 원본의 INT#0 Word 덮어쓰기는 VR04 요청·고장 비트도 포함한다.

이 문서는 원본 조사와 후속 독립 검토용이다. 로컬 2차133 통합, 매뉴얼/UI·기록 구현, 게시, TIA 컴파일, 현재 CPU·실물 확인 또는 현장 복구를 완료한 것이 아니다.

## 작업 기준과 보존

- 대상: catalog_id `VR04`, 로터리 밸브, motor, 집진·석회, parent_id 없음, depth0, priority_key 없음. INVENTORY catalog/105, equipment/42. 전기 FG62. 동일 명칭의 VR01~VR06을 이름만으로 병합하지 않는다.
- 작업3 자체 cloud 추가조사 세 번째 묶음 VR04/VR05/VR06/SC10/SC11 중 VR04 한 개. `TASK3-BATCH03-SCOPE.json`의 고유 ID·중복·제외 검토를 확인했다. phase2 후보133 대장은 유지하며 로컬 통합 제외 지시를 유지한다.
- 고정 읽기 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 저장소 `https://github.com/esp6662266/gme-plc-manual`. 이후 main이나 현재 CPU를 이 버전과 같다고 보지 않는다.
- GME-STD-1.0.0, AGENTS, gme-equipment-rollout 스킬·source-map, WORK-STANDARD/WORK-ITEM-TEMPLATE/INVENTORY, START-GPT61, 최신 진행·인계·게시 기록을 읽었다. 기존 VR03 초안은 구조 참고만 사용하고 모든 VR04 값은 고유 원본으로 다시 확인했다.
- 조사일 2026-10-11 UTC. 작성자 VR04 원본 조사 작업자. 실제 모델명·추론 설정의 런타임 증명은 별도 확보하지 않았다.
- 읽기 전용 preflight 종료0, inventory_matches=true. 전체248/우선23/대응18/제외90/제외부모 하위보류7/phase2 133. source_byte_changes의 requirements-audit.json·all-in-one-data.json은 표준 대장 생성 당시와 고정 버전 사이 바이트 차이다. 이번 조사에서 수정·재생성하지 않았다.
- 쓰기 범위는 `drafts/VR04-DOTS-DRAFT.md`, `extracts/VR04/`뿐이다. source 원본·공용 declarations·타 설비 초안·코드·버전·대장·배포·운영기록을 변경하지 않았다.
- 시뮬레이터 작성·수정·생성·실행·행동시험0. 원본의 중지된 다른 Writer 선언은 읽기 전용 존재 확인에 한정했다. 금지 생성기/시험, 실제 PLC·현장·보호값 변경, SEJIN 프로그램·운영자료·사진·이력 복제/통합0.

이하 원본 경로는 고정 저장소 `all-in-one/` 아래다. `0267`은 `sources/decoded-original/0267-FlgNet.xml`, `0604` 선언은 `0604-IdentXmlPart.xml`을 뜻한다. LAD는 원본 문서ID이며, 색인 순서와 NID는 별개다. 파생 network-map/CSV는 탐색에만 쓰고 핵심은 XML의 Part/Wire/ORef와 선언의 UID/RID/NID·형식·주소로 대조했다.

## 7영역 적용표

| 영역 | 적용 상태 | 이 초안의 근거 | 남은 확인 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | VR04/M38, BF01·SC10 관계, 원본·시점 구분 | 현행 실물·명판·배치 동일성 |
| I/O·HMI | 적용, 일부 미확보 | I5.5/Q4.4, DB2/3/9/13, HMI3행, 원시/처리 전달 | HMI4데이터 ORef 결속·DB11 구조·화면 이벤트 |
| 제어 구조 | 적용 | 요청/출력·Set/Reset·Word쓰기, SC10/FN04/BF01 영향, 호출 | 현재 실행 순서·외부 쓰기·기동 조건·현재값 |
| 전기 전달 경로 | 적용 | 전기4쪽·시공2쪽·P&ID1쪽 실제 렌더, 양끝점 | 현장 단자·정상극성·준공·현행 모델/설정 |
| 알람·복구 | 적용 | S5 2초 Set/Reset, 요청 해제·공유 영향 | 표시·원인 제거·재요청·실제 복구 |
| 증상별 수리 | 적용, 관찰 지침 | 요청→Q→접촉기→I→처리→HMI 비교점 | 실제 진단·조치·복구 기록 없음 |
| 완료 기준 | 적용 | 부족자료·미실행·네 기능·검토 경계 | 통합/UI/기록/게시/TIA/CPU/현장 별도 |

## 1. 설비·자료 및 소유 경계

1. equipment.json VR04는 parent가 비어 있다. P&ID p1 실제 렌더에서는 BF-01 하부 분진 스크루 SC-10(M34) 출구에 VR-04(M38)가 있다. 이것은 도면의 공정 관계이며 catalog parent를 BF01로 변경하거나 BF01 세정 기능을 VR04 소유로 바꾸는 근거가 아니다.
2. 전기 FG62/PDF63 제목 `ROTARY VALVE VR-04`, 모터 M38, 0.55kW/1.25A, 상단 THREE-PHASE LINE 440V 60Hz다. P&ID의 M38도 0.55kW/440V다. 현행 명판·전원·정격과의 일치는 별도다.
3. 검토한 직접기동 회로에는 전용 인버터, 속도지령, 전류 아날로그, PID, 위치 엔코더가 없다. 이 직접기동 경로에서는 해당 제어가 비해당이다. 현장에 다른 장치가 전혀 없다는 뜻은 아니다.
4. SC10은 독립 모터 M34, VR04는 M38이다. VR04 Run은 SC10 운전요청 해제의 입력이지만 SC10 고장 자체를 VR04 고장으로 병합하지 않는다. FN04의 90분 타이머도 VR04 전용 2초 타이머와 소유·목적이 다르다.
5. BF01 세정 허가는 Filter 블록의 Local과 Memory에 기록된다. VR04는 그 선행 응답 중 하나다. DP01·공유 문턱값·세정 EV 출력을 VR04 센서/출력·보호값으로 배정하지 않는다.
6. P&ID 도번1684n002 판I, 원작성 06/04/2011, 판I 변경 15/01/2013. 전기 검토 FG62/121/140/254의 기본일자는 27.05.2024이며 하단에 별도 Rev2 날짜를 확인하지 않았다. 파일명 Rev2만으로 모든 시트에 Rev2/17.03.2025를 붙이지 않는다.
7. 시공 PDF47/51에는 `24.11.11 first draft design`, CHECKED/APPROVED 공란이 있다. 문서상의 계획 경로·열값이며 승인 준공도·실제 시공 길이로 확정하지 않는다. PLC·P&ID·전기·시공 자료의 시점 차이를 유지한다.

## 2. I/O·HMI 및 전달

### 2.1 직접 주소와 저장부

| 신호 | 선언 형식·주소 | 원본 결속 | 읽기/쓰기·의미 |
|---|---|---|---|
| VR04_Fbk | Bool, %I5.5 | live_index doc516; 0613 RID260 Input/AO45, NID43 UID2368 | 원시 접촉기 응답. 운전시간 계수에서 읽음 |
| Start VR04 | Bool, %Q4.4 | doc1305; 0602 RID180 Output/AO36, NID37 UID1045 Write; 0658 RID134 NID33 UID1136 | 물리 출력 명령. 주석 `a 53.0`보다 실제 Address·FG62 A4.4를 구분 |
| Flag.M_VR_04 | Bool, DB2.DBX2.6 | 0604 RID179 AO/BO22, BAD2→0603 Flag TOD2; 0577 RID20 | 자동 Set2·정지Reset·고장Reset·기동Word쓰기·HMI 가능 쓰기 |
| Allarm.VR_04_FAULT | Bool, DB3.DBX2.6 | 0657 RID137 AO/BO22 BAD10→0655 Allarm TOD3; NID33 UID1141/1143/1144 | 전용 Set/Reset 유지 고장, startup Word0 포함 |
| Inputs.VR04 Run | Bool, DB13.DBX5.5 | 0604 RID220 AO45, NID32 UID23/NID34 UID996; 0657 RID301 UID1173; 0596 RID318 NID29 UID36; DepDB TOD13 | 원시 I5.5와 별도 처리 응답. SC10/FN04/BF01에 사용 |
| Tag_76 | Timer, %T93 | live_index doc1304; 0658 RID135 Timer/AO93, NID33 UID1138 Write/1139 Read | VR04 2초 감시. HMI 태그가 아님 |
| Flag.RESET_ALLARM | Bool, DB2.DBX6.0 | 0657 RID13 BO48, NID33 UID1142; 0655 Flag TOD2 | 공통 Reset 요청. 재기동·복구 완료와 다름 |
| ON | Bool, %M0.0 | 0602 RID1 Memory/AO0 등 | 원문 공통 접점. 이름만으로 현재 TRUE를 가정하지 않음 |
| UNDER TESTING | Bool, %M5.5 | 0602 RID4 Memory/AO45, NID32 UID924 | SC10 Reset 가지의 부정 접점. 사용·우회 권고 아님 |
| hours motors.VR_04_MIN | Int, DB9.DBW168 | 0615 RID262 BO1344; NID43 UID2369/2371/2372/2377; 0614 TOD9 | +1 및 0 쓰기 |
| hours motors.VR_04_HOUR | Int, DB9.DBW170 | 0615 RID264 BO1360; NID43 UID2375, NID55 UID3091 | 상수1 및 상수0 Move. 누적 Add라고 쓰지 않음 |
| Tag_47 / Tag_48 | Timer, %T13 / %T17 | 0613 RID1 AO13 / RID284 AO17 | 공통 시간계수/기록 후 Reset 관련 |
| Flag_Aggiorna_DB | Bool, %M1.7 | 0613 RID13 AO15, NID43 UID2378 SCoil | 여러 모터 공통 업데이트 요청. 영구저장 완료 신호로 단정 불가 |
| Data.DP_01 / Coeff.DP_01_SOGLIA_1 | Int, DB1.DBW240 / DB4.DBW138 | 0596 RID6 BO1920/RID8 BO1104, NID29 UID37/38; 0595 TOD1/4 | BF01 세정 허가의 비교값. VR04 자체 계측/설정 아님 |
| BF01_RUN | Bool, %M180.3 | 0594 RID341 Memory/AO1443, NID29 UID75 Write | Filter 허가에서 쓰는 내부 비트. 물리 모터 피드백과 구별 |

주소는 SAD·SSD/AO·AOS/BO와 해당 DepDB의 TOD 번호로 환산했다. 현재 CPU 주소, 최적화 DB, 통신 접근, 현재 값·정상극성을 검증한 것이 아니다.

### 2.2 입력 Word 전달과 다른 Writer

- LAD1070 `0397`, hmi inputs 색인1/NID1: Part35 Move.in←ORef36/RID10 Tag_180(W39), out1→ORef37/RID11(W40). `0627` RID10 Word/Input/AO32, `0629` RID11 Word/AO32 BAD4, `0628` Inputs TOD13이므로 **IW4→DB13.DBW4**, 그 워드에 I5.5→DB13.DBX5.5 대응이 포함된다.
- Part22.eno→Part27.en(W34), Part27.eno→Part35.en(W41). 해당 Move에는 DisableENO=true 속성이 있다. 선·속성은 확인했지만 TIA 판본의 실제 ENO 의미와 현재 실행을 시험하지 않았으므로 무조건 매 스캔 복사라고 쓰지 않는다.
- main LAD1613 `0030`, 색인2/NID19: CRef21 Recipes Handler→CRef23 HMI→CRef25 HMI Output의 ENO 연쇄(W31~33), CRef25.eno→Contact37 NOT Simulation(1)(W42/44)→CRef28 HMI Inputs.en(W43). `0688` CodeBlock29/RID135 HMI Inputs, `0692` ORef45/RID140 Simulation(1)을 대조했다.
- `0635`에는 Inputs.VR04 Run RID132 NID4 UID63 AK Write가 있다. 이는 색인상 simulation LAD1085의 중지된 다른 Writer 존재다. 이 선언을 보존했으나 시뮬레이터 실행·행동시험·활성화 판정은 하지 않았다.
- Word/AO 범위도 검색했다. 같은 비트오프셋의 다른 DB를 같은 신호로 합치지 않았다. 처리 응답 Writer를 태그명 검색만으로 하나라고 단정하지 않으며 간접·외부 쓰기 및 현재 프로젝트 교차참조는 미확정이다.

### 2.3 출력 미러와 이름의 주의

LAD356 `0401`, HMI Output NID1은 출력 Word를 DB로 읽어 복사한다. Part24.in←ORef37/RID30 Tag_282(W62), Part24.out1→ORef38/RID51(W63), 앞 Move23.eno→24.en(W60). `0632` Tag_282는 Word/Output/AO32, `0633` RID51 Word/AO32 BAD26, `0064` Output TOD14이므로 QW4→DB14.DBW4다. DB14.DBX4.4에 명령 미러가 포함될 수 있지만 이것은 DB11의 실제 HMI 응답·접촉기 상태와 다르다.

반대로 main LAD1616 `0546`의 `Word_outputs.WORD3`는 이름만으로 QW4라고 읽으면 안 된다. ORef161/RID28 Tag_180은 `0692`에서 **Input/AO32**, Part151.in(W173)이며 out1→ORef162/RID29(W174), `0690/0689`에서 Word_outputs DB101.DBW4다. 즉 해당 원문은 IW4→DB101.DBW4다. 이 미러를 Q4.4의 별도 Writer로 세지 않는다. 현재 원본의 이름·영역 불일치를 임의 수정하지 않았다.

### 2.4 HMI 설정과 미결속 호출

`sources/hmi_plc_tags.csv`의 VR04행은 3개이며 Access Name=PLC, 원문 설명은 `dde.cfg 설정; 온라인 현재값 아님`이다.

| CSV 행 | HMI 태그 | 주소 | ID | 확정 범위 |
|---|---|---|---|---|
| 130 | VR_04\Allarme1 | DB11,X60.1 | 00332 | 설정 존재. PLC DB3 고장과 다른 주소 |
| 418 | VR_04\RispostaA | DB11,X60.0 | 001B9 | 표시 응답 설정. I5.5와 직접 동일 신호라고 확정 못 함 |
| 453 | VR_04\Flag | DB2,X2.6 | 00191 | 요청 주소와 일치. 실제 버튼 이벤트·권한·쓰기 시각은 미확정 |

LAD1207 `0383`, hmi 색인30/제목vr04: CRef22/RID638, CodeBlock23/RID1은 `0623/0624` HMI Standard Motors 호출 선언 후보와 대응한다. 그러나 network-map의 NID는 null이고 데이터 ORef4개는 UID/RID/이름 선언에 결속되지 않았다. 검색 문자열을 직접 선언 확정으로 승격하지 않는다.

| Wire | 원본 핀 | 남은 결속 |
|---|---|---|
| 21 | rail→CRef22.en | 호출 전원선 |
| 37 | ORef24/RID661→Ingresso_run | 검색상 Inputs.VR04 Run 후보, 일치 선언 미확보 |
| 39 | ORef26/RID358→Allarme1 | 검색상 VR_04_FAULT 후보, 일치 선언 미확보 |
| 40/41/42/43 | ORef27/28/29/30, RID48→Allarme2/3/4/5 | 0626 FALSE 선언·호출 기록 존재, 해당 네트워크 NID 결속 별도 |
| 46 | Risposta→ORef33/RID359 | 검색상 Motors.VR04.Risposta 후보, 이름·주소 미결속 |
| 48 | Comulativo_allarmi→ORef35/RID361 | 검색상 Motors.VR04.Allarme_comulativo 후보, 이름·주소 미결속 |

DB3.DBX2.6→DB11.DBX60.1의 실제 갱신·화면 표시를 이 자료만으로 확정하지 않는다. 원 프로젝트의 HMI 함수·DB11 구조, 화면 이벤트 및 온라인 비교가 필요하다.

## 3. 제어 구조·호출·다른 쓰기

### 3.1 VR04 요청 해제와 출력

LAD1967 `0267`, motors1 색인38/NID37. 5 Part/9 Wire를 전부 대조했다.

| 기능 | 원본 연결 | 정적 해석 |
|---|---|---|
| 공통 허가 | rail W1060→ON Contact1054, ORef1041/RID1 W1046 | ON 아래 두 분기 |
| 고장 요청 해제 | 1054.out W1055→fault Contact1056, ORef1042/RID178 W1047; 1056.out W1057→RCoil1036; ORef1043/RID179 W1049 | ON AND VR_04_FAULT→M_VR_04 Reset |
| 출력 | 1054.out W1055→M_VR_04 Contact1058, ORef1044/RID179 W1050; 1058.out W1059→Coil1040; ORef1045/RID180 W1052 | ON AND M_VR_04→Start VR04 |

출력 가지에 NOT fault가 직렬인 형태가 아니다. 별도 요청 Reset과 일반 출력 Coil 구조다. 이 네트워크에서 전용 Local/Auto·Maintenance 접점을 못 찾았다고 전체 설비에 안전조건이 없다고 해석하지 않는다.

### 3.2 자동 Set·전체 정지

`0577` RID20은 NID3 UID599 Set, NID4 UID943 Set, NID5 UID1019 Reset을 담는다. `0604` RID179 고장Reset과 더불어 직접 비트Writer 네 위치를 확인했고, startup Word쓰기·HMI 가능쓰기는 별도다.

| 기능 | 상위 허가·비교 | 대상 쓰기 |
|---|---|---|
| 예열 LAD1843 `0164`, 색인3/NID3 | ON785→NOT Emergency22→Eq400 Tipo=1→Auto_ON1 Contact823. W672→Eq416.pre, ORef596 Tempo와 ORef597/RID18 Int3, W679/680 | Eq416.out W681→SCoil422.in; ORef599/RID20 W683→M_VR_04 |
| 생산 LAD1844 `0165`, 색인4/NID4 | ON1145→NOT Emergency1154→Auto_ON1 1147→Eq737 Tipo=2. W1021→Eq753.pre, ORef940 Tempo와 ORef941/RID18 Int3, W1028/1029 | Eq753.out W1030→SCoil759; ORef943/RID20 W1032 |
| 정지 LAD1847 `0166`, 색인7/NID5 | Auto_ON1 Contact1095→Eq881 Tipo=5. W1031가 Eq957.pre와 Emergency1106.in을 허가. Eq957은 ORef1016 Tempo vs ORef1017/RID102 Int20. W34/35→OR33 | OR33.out W1078→RCoil963; ORef1019/RID20 W1080 |

정지 분기의 식은 Auto_ON1 AND Tipo5 AND (Tempo20 OR Emergency)다. Emergency가 모든 모드에서 이 Reset을 무조건 실행한다는 뜻이 아니다. Tempo=3/20은 Int 비교 원문이고 실제 3초/20초 경과는 상위 갱신·호출 검증 전이다.

`0578`의 RID8 V1/RID78 V2/RID22 V5/RID18 V3/RID102 V20과 해당 UID를 확인했다. `0577/0576`에서 Tipo_preset DB1.DBW98, Tempo_presetting DB1.DBW96, Auto_ON1 DB2.DBX7.3, Emergency_module_fault DB3.DBX16.6이다. 현재값·보호상태·시간성은 미확정이다.

### 3.3 기동 시 Word 단위 덮어쓰기

비트 이름이 없는 GlobalAccess도 범위가 겹치는지 확인했다.

- **요청:** startup only LAD402 `0147`, 색인2/NID2. ON Contact208.out(W209)→Move138.en, Move138.eno(W187)→Move141.en. Move141.in은 ORef170/RID54(W188), out1은 ORef171/RID9(W189). `0048` RID54 Int0, `0563` RID9 Word/AO16 BAD6, `0562` Flag TOD2. 따라서 **DB2.DBW2←0**이며 DB2.DBX2.6 M_VR_04를 포함한다.
- **고장:** startup only LAD403 `0148`, 색인3. ON Contact329.out(W330)→Move250.en, Move250.eno(W306)→Move253.en. Move253.in ORef287/RID54(W307), out1 ORef288/RID26(W308). `0048` RID54 Int0, `0563` RID26 Word/AO16 BAD23, `0562` Allarm TOD3. 따라서 **DB3.DBW2←0**이며 DB3.DBX2.6 VR_04_FAULT를 포함한다.
- LAD403의 파생 inferred_original_nid는 null이지만 `0047` ON/RID1 UID284, `0048` 0/RID54 UID287, `0563` Word/RID26 UID288는 모두 **선언 NID3**으로 대조된다. 파생 결속0과 원본 선언 근거를 구분한다.
- 두 Word쓰기 모두 선행 Move의 ENO 뒤다. startup only라는 블록명은 확보했지만 현재 OB 설정·실제 기동 호출·재시작 시 초기값·다른 쓰기와의 우선순위는 검증하지 않았다. 비트별 Reset 네 위치만으로 전체 쓰기를 다 셌다고 하지 않는다.

### 3.4 SC10·FN04 영향

- **SC10:** LAD1962 `0262`, motors1 색인33/NID32. ON Contact940.out(W941)에서 SC_10_FAULT Contact942→OR911.in1(W943), NOT VR04 Run Contact22→NOT UNDER TESTING Contact946(W24)→OR911.in2(W947). OR911.out(W933)→RCoil916, M_SC_10 ORef925/RID158(W935). 식은 ON AND [SC10_FAULT OR (NOT VR04 처리Run AND NOT UNDER TESTING)]→SC10 요청 Reset이다. ORef23/RID220(W21)이 VR04 처리Run이다.
- **FN04 공유 예고장:** LAD1964 `0264`, 색인35/NID34. ON1020→FN04 Run1022 뒤, SC01/VR03/SC10/VR04/SC11/VR05 여섯 처리응답의 각각 NOT 접점이 OR972로 들어간다. VR04는 ORef996/RID220(W1009)→Contact1030 NOT→OR972.in4(W1031).
- OR972.out(W1012)은 Coil982 Prealarms_FN04, SdCoil985, Tag126 Contact1036을 함께 허가한다. ORef1000/RID112(W1014)는 `0606` S5T#1H_30M V13632, ORef1001/1002와 `0602` RID169는 Tag_126 %T131. Contact1036.out(W1037)→Coil990 Stop_Fan_FN04, ORef1003(W1018).
- `0605` Stop_Fan_FN04 Local RID170은 NID34 UID1003 Write와 NID35 UID1019 Read. LAD1965 `0265`에서 ON1038→Contact1042(W1029)→OR1003.in4(W1043)→RCoil1010(W1031), M_FN_04 ORef1021(W1033) Reset이다. 이는 여러 FAN 정지원인 중 하나다.

90분을 VR04 전용 고장지연으로 표시하거나 2초와 합산하지 않는다. 여섯 응답·FAN 운전·다른 정지원인과 발생 시각을 함께 관찰해야 한다.

### 3.5 BF01 세정 허가와 Forza_Lavaggio

LAD1886 `0219`, Filter 색인5/NID29의 BF01 가지를 원본으로 대조했다.

1. ON Contact21(ORef34/RID52 W48)→SC10 처리Run Contact22(ORef35/RID304 W50), W51→VR04 처리Run Contact23(ORef36/RID318 W52).
2. Contact23.out W53가 Le24.pre와 Forza Contact25.in을 허가한다. Le24는 Int, in1 Data.DP_01 ORef37/RID6(W54), in2 Coeff.DP_01_SOGLIA_1 ORef38/RID8(W55). **비교는 Le(≤)**이며 임의로 ≥로 수정하지 않는다.
3. Le24.out→OR26.in1(W56), Forza_Lavaggio Contact25.out→OR26.in2(W58); OR26.out W59→Coil27 Local Abilita_lavaggio_BF01(ORef40/RID63 W60); Coil27.out W72→Coil74 BF01_RUN(ORef75/RID341 W73).
4. 정적 식은 ON AND SC10 Run AND VR04 Run AND [(DP01≤DP01_SOGLIA1) OR Forza_Lavaggio]다. Forza 가지에도 앞선 SC10·VR04 Run이 필요하다. 문턱이 현재 몇 mbar인지, 비교방향이 운전 의도와 맞는지, 현재값·실제 실행은 별도이며 P&ID의5~10mbar 표기를 현행 PLC 설정으로 대입하지 않는다.
5. `0598`에서 Forza_Lavaggio는 Local Bool RID57 BO34, Abilita_lavaggio_BF01는 Local Bool RID63 BO32. 세정EV·BF01 소유의 Local을 VR04 출력으로 바꾸지 않는다. 인접 BF02 가지도 같은 RID8 DP_01_SOGLIA_1을 읽는 원문을 보존하지만 이 문서에서 BF02 소유·정상성을 확정하지 않는다.

**Forza의 타이머 외 가지:** LAD1885 `0200`, Filter 색인4/NID3.

- ON Contact451→NOT Tag129 Contact453(W452/440)→SdCoil418(W454), value ORef430/RID54(W439)=S5T#2H, operand ORef432/RID55(W442)=Tag130 %T134.
- 같은 ON→Tag130 Contact455(W444)→SdCoil423(W456), value ORef433/RID56(W443)=S5T#10M, operand ORef435/RID53(W446)=Tag129 %T133.
- ON451.out는 Tag130 Contact457과 **별도 ON Contact460**에도 연결된다(W452). Tag130457.out→OR21.in1(W458), ON460.out→OR21.in2(W22). OR21.out(W23)→Coil428, Forza_Lavaggio ORef437/RID57(W449).
- 따라서 원문은 **ON AND (Tag130 OR ON)→Forza_Lavaggio**다. `0594/0597/0598`의 해당 RID/UID/NID를 대조했다. ON의 현재 값은 미확정이며, ‘매2시간 후10분만 강제세정’처럼 타이머 가지만으로 요약하면 잘못이다. 이 해석은 정적 분기 설명이고 제어수정·보호우회 권고가 아니다.

### 3.6 호출 경계

| 원본 | 확인한 허가·호출 | 선언 | 남은 범위 |
|---|---|---|---|
| main LAD1619 `0031`, 색인8/NID6 | ON282.out W283→CRef264 Allarms1.en | 0688 RID58 CodeBlock275 Call | 현재 호출·인터럽트·알람 실행 |
| main LAD1620 `0549`, 색인9/NID7 | ON350.out W351→CRef319 Motors1, CRef322 Filter, CRef334 time work motor | 0688 CodeBlock337/RID67,339/RID70,347/RID82; 0694 인터페이스 | 텍스트 순서와 실제 최종값·현재 스캔은 별도 |
| cyc_int2 ogni1s LAD1723 `0024`, 색인5/NID4 | ON188.out W189→CRef183 Auto start motors.en | 0067 CodeBlock186/RID39; 0068 ON | 이름만으로 실제1초주기 검증 불가 |
| main LAD1613 `0030` | HMI/Output ENO 및 NOT Simulation(1)→Inputs | 0688/0692 | ENO·미러 갱신·현재 호출 유효성 |
| startup only LAD402/403 | ON 및 ENO 뒤 DB2/DB3 Word0 | 0047/0048/0562/0563 | 현재 시작OB·재시작 조건 미확보 |

자동 Set·고장 Reset·기동 Word0·HMI 외부 쓰기의 최종값은 현재 프로젝트 교차참조·호출·실행 검토가 필요하다. 이 조사에서 행동시험하지 않았다.

## 4. 전기 전달 경로

전기 PDF63/122/141/257, 시공 PDF47/51, P&ID p1 총7개의 서로 다른 원본 페이지를 실제 렌더해 확인했다. P&ID 확대2개는 같은 p1의 보조 렌더이며 별도 페이지로 세지 않는다.

| 경로 | 도면·PDF | 확인한 양끝점·배선 | 미확정 |
|---|---|---|---|
| 주회로 | FG62/PDF63 | 8.3L1/L2/L3(61/9→63/0)→62QM1 1/3/5–2/4/6→62KM1 주접점1/3/5–2/4/6→62U1/V1/W1·XM62U1/V1/W1→62QS1 1/3/5–2/4/6→M38 U/V/W, PE | 실제 공급·상순서·회전·명판 |
| PLC 출력 끝점 | FG140/PDF141 | CPU515 MOD15 A4.4 단자5→참조62/4→FG62 A4.4 | 모듈 형번·현행 채널·전압 |
| 출력모듈 전원 | FG140/PDF141 | +24Vdc10.9→X21 3032 4A F 5×20→140.1→단자10; −0Vdc10.6→단자9 | 현장 전원·퓨즈 상태 |
| 코일 제어 | FG62/PDF63 | A4.4(140/1)→XS61→62QS1 보조접점→XS62→선62.1→62QM1 보조접점→62KM1 A1; A2→−0Vdc10.6 | QS/QM 보조접점 숫자단자 명확히 확인 못 함. 정상극성·현장 결속 |
| 원시 응답 | FG62/PDF63, FG121/PDF122 | +24Vdc10.7→62KM1 보조13–14→E5.5(121/5)→CPU515 MOD9 E5.5 단자16, 역참조62/6 | 접촉기 응답이며 실제 회전/분진 흐름은 별도 |
| 입력모듈 전원 | FG121/PDF122 | +24Vdc10.7→X21 3008 2A IST.5×20→121.1→단자20; −0Vdc10.6→단자19 | 현행 퓨즈·전원·접지 |
| 현장 케이블 | 시공PDF47/51 | 1_30 `=DUS+VR04-M38A`, CR→VR-04/M38. p47 DUST ZONE13 Route223RA→Embedded CP No.3 Pipe16→M38 | 실제 양끝 코어단자·준공 변경·길이 |

- FG62의 M38 표기는0.55kW/1.25A, 62QM1 범위1.1–1.6A, 패널 배선 BLACK FS17 1.5mm²다. 문서 정격·범위를 현재 보호설정 또는 변경 지시로 사용하지 않는다.
- FG254/PDF257의 62KM1 본체는 Siemens `3RT2015-1BB41`, CONTACTOR3KW/1L/DC24V/S00 VT, 부속 RC `3RT2916-1CB00`. 62QM1 표기 아래 `3RV2901-1E` 보조접점, `3RA1921-1DA00` 고정구, Whoner `WR32433` 어댑터, Siemens `3RV2011-1AA10` MAGNETOTHERMIC1.1–1.6A가 이어진다. 각 수량1. 첫 62QM1 행이 보조접점이므로 그 행만을 차단기 본체 모델로 읽지 않는다.
- 시공 p51 1_30 열은 Current Type GAC, SPEC CV, CORE4, SIZE1.5, SPARE0, 경로100→200→220→221→223RA→E300, Adjustment8, LEN99다. LEN99를 검증된 실제 설치 길이로 확정하지 않는다. Pipe16은 관로 표기다.
- p47의 DP02·JB01TB6 및 SC10/M34·SC11/M35·VR05/M39는 같은 관로 도면에 나타나지만 VR04 부속센서·출력으로 배정하지 않는다.
- 도면의 Siemens/Whoner를 현재 실물이나 ABB 대체모델로 확정하지 않았다. 현행 모델/단자·토크·정비주기·안전한 보호값은 명판·승인자료·제조사 원문 없이 채우지 않는다.

## 5. 알람·시간·복구

### 5.1 전용 2초 고장

LAD1811 `0445`, allarms1 색인31/NID33, 9 Part/17 Wire를 전체 대조했다.

| 단계 | 원본 Part/Wire/ORef | 정적 해석 |
|---|---|---|
| 허가 | rail W1171→ON Contact1159; ORef1135/RID1 W1145 | ON |
| 명령 | 1159.out W1160→Start Contact1161; ORef1136/RID134 W1146 | 출력명령 감시 |
| 응답부재 | 1161.out W1162→Contact1172 NOT; ORef1173/RID301 W1175; W21→SdCoil1123.in | ON AND Start VR04 AND NOT 처리Run |
| 타이머 | value ORef1137/RID28 W1147, operand ORef1138/RID135 W1148 | 0656 S5Time S5T#2S V512, 0658 Tag76 %T93 |
| 고장Set | 1161.out W1162→Tag76 Contact1163(ORef1139 W1149); W22→SCoil1129; fault ORef1141/RID137 W1152 | ON AND Start AND Tag76→고장Set |
| 고장Reset | ON1159.out→RESET_ALLARM Contact1167(ORef1142 W1154)→fault Contact1169(W1168, ORef1143 W1155)→RCoil1134(W1170), fault ORef1144 W1157 | ON AND RESET_ALLARM AND fault→Reset |

NOT 처리Run은 타이머 입력 가지다. Set 코일의 직렬 접점인 것처럼 식을 새로 만들지 않는다. S5Time V512는 인코딩값이며512ms가 아니다. 타이머 이름·원문시간과 실제 경과·현재값을 구분한다.

### 5.2 Reset과 복구

VR04_FAULT는 LAD1967에서 요청Reset을 일으킨다. 공통Reset으로 fault가 내려가는 것과 M_VR_04가 다시 생성되는 것은 별개다. startup Word0도 명시된 쓰기다. 동시 Set/Reset·HMI요청·전원재시작·스캔순서의 최종값을 추정하지 않는다.

복구 판단은 원인제거, 보호·전원·접촉기·기계 상태, 원시/처리/표시의 일치, 승인된 재요청, 실제 회전·분진 배출과 재발 여부의 근거가 필요하다. 알람해제나 Q=1만으로 복구 완료라 기록하지 않는다. 이 초안은 Reset·재기동·보호우회를 실행하거나 승인하는 문서가 아니다.

### 5.3 운전시간은 HOUR 상수1/0 쓰기

LAD1041 `0328`, time work motor 색인40/NID43, 7 Part/18 Wire를 전체 대조했다.

1. Tag47 Contact2396→**원시 VR04_Fbk** Contact2398(W2397), out W2399가 Add2350.en·Ge2357.pre를 같이 허가한다. 처리Run DB13을 쓰는 경로가 아니다.
2. Add2350 Int: in1 MIN ORef2369/RID262(W2381), in2 상수1 ORef2370/RID7(W2382), out MIN ORef2371(W2383).
3. Ge2357 Int: MIN ORef2372(W2384), 상수60 ORef2373/RID8(W2385). out W2386→Move2360.en.
4. Move2360.in은 **상수1** ORef2374/RID7(W2388), out1 HOUR ORef2375/RID264(W2389). HOUR+1 Add가 아니다.
5. Move2360.eno W2390→Move2363.en, in 상수0 ORef2376/RID12(W2391), out1 MIN ORef2377(W2392), eno W2393→SCoil2366, Flag_Aggiorna_DB ORef2378(W2394).
6. `0616` RID7 V1/RID8 V60/RID12 V0의 NID43 UID를 대조했다. HOUR1·MIN0을 원본 오류로 추정해 바꾸지 않는다.
7. LAD1053 `0340`, 색인52/NID55: Tag48 Contact3111→Move3070(FN04 HOUR0)→ENO Move3073(VR03 HOUR0)→ENO Move3076. Move3076.in 상수0 ORef3090/RID12(W3103), out1 VR04 HOUR ORef3091/RID264(W3104), 앞 ENO W3102. **VR04 HOUR0은 세 번째 Move**이며 단독 첫 Move가 아니다.
8. LAD1056 `0019`, 색인55/NID58: NOT Tag47 Contact3120.out W3121→SdCoil3112.in, value ORef3114/RID335=`S5T#1M`, operand ORef3116 Tag47. 실제 펄스 주기·누락은 미확정이다.
9. LAD1055 `0341`, 색인54/NID57: ON3147 아래 Flag_Aggiorna_DB3149→SCoil3110 MEM2_0. MEM2_0 Contact3151 뒤 NOT Flag_Aggiorna_DB3153→SdCoil3118, value ORef3128/RID334 S5T#5S, operand Tag48. MEM2_0 뒤 Tag48 Contact3155→RCoil3123 MEM2_0. 제목만으로 DB 영구저장 성공 handshake를 확정하지 않는다.

시간계수 Tag47 1분, 기록후 Tag48 5초, 고장 Tag76 2초, FN04 공유 Tag126 90분, Filter Tag130 2시간/Tag129 10분은 각각 소유와 기능이 다르다. HOUR0/1을 총 누적시간·정비기한·가동률로 사용하려면 외부 누계·저장 설계를 확보해야 한다.

## 6. 증상별 관찰·수리 판단

다음은 안전하게 수집할 비교점이다. 라이브 시험·강제출력·활선 측정·보호우회·분해 지시가 아니다. 실제 현장조치는 자격자와 승인절차에 따른다.

| 증상 | 같은 시각에 비교할 대상 | 원인 배제 근거 | 복구 판정의 경계 |
|---|---|---|---|
| HMI 요청은 있는데 출력없음 | HMI DB2,X2.6, 요청, ON, fault, Auto/Tipo/Tempo, Q4.4 | HMI 실제 이벤트, 고장Reset·전체정지·startup Word0·호출 | 버튼 상태가 PLC쓰기·출력 완료를 뜻하지 않음 |
| Q4.4인데 회전없음 | FG140 단자5→XS61/62→QS/QM→KM1 A1/A2, 주회로·M38 | 실물과 도면 결속, 자격자의 승인관찰, 기계 상태 | Q=1·접촉기응답으로 회전/배출을 대신하지 않음 |
| 기동후 FAULT | Start, Tag76, I5.5, DB13.X5.5, KM1 13/14 | 2초 감시·원시/처리 전달·다른Writer·시각 | Reset만으로 원인제거 확정 불가 |
| I5.5와 HMI 응답이 다름 | IW4/DB13W4, DB11,X60.0/60.1, DB14 명령미러 | HMI4 미결속 ORef·DB구조·이벤트·통신/호출 | 표시문제를 곧바로 기계고장으로 단정하지 않음 |
| VR04 문제와 SC10 정지 | VR04 처리Run, SC10 fault/M_SC10, UNDER TESTING, Q4.0 | LAD1962 OR/NOT·시간순서·독립 모터 상태 | 두 설비 고장을 병합하지 않음 |
| FN04 예고장/후속정지 | FN04 Run 및 여섯 응답, Prealarms, Tag126, Stop_Fan, M_FN04 | LAD1964→1965·다른 정지조건·90분 경계 | VR04 하나만으로 FAN 정지원인을 확정 못 함 |
| BF01 세정허가가 예상과 다름 | SC10/VR04 처리Run, DP01/문턱, Forza Local, BF01_RUN | LAD1886의≤/OR·LAD1885의 별도ON 가지, 현재 호출 | 현재 문턱·밸브실동작·세정 완료는 별도 |
| 시간값0/1·누계 이상 | MIN168/HOUR170, 원시Fbk, Tag47/48, 업데이트Flag | Move1·세번째Move0·외부누계·저장 이력 | 총운전시간·정비주기 산출 금지 |

관찰자는 시각/시간대, 장치·프로젝트 버전, 수집방법과 실제위치, 값/단위, 원본대조, 배제근거, 승인조치, 재발·복구증거를 남긴다. 미관찰을 정상으로 채우지 않는다. 사용자 운영기록·사진은 이 공개 소스 조사물로 복제하지 않는다.

## 7. 부족자료·네 기능·완료 기준

### 7.1 필요한 후속 증거

| 자료 | 확보 위치 | 판정 목적 |
|---|---|---|
| 현재 PLC 프로젝트·교차참조·시작OB/주기/DB구조 | 승인된 엔지니어링 백업 | 고정원본 동일성·Word쓰기·호출·동시Set/Reset·실제 최종값 |
| HMI 원프로젝트/DB11/함수·화면이벤트 | HMI·PLC 인터페이스 자료 | 미결속 ORef4와 표시주소·요청쓰기 |
| 원시/처리/HMI 동시관찰 | 승인된 현장기록 | I5.5↔DB13.X5.5↔DB11 차이·시간성 |
| M38·62KM1/QM1/QS1 명판·단자자료 | 현장 담당자·승인 설비기록 | 현재 모델·단자·정격·보호값·극성 |
| BF01/SC10/VR04 배치·기계자료 | 준공도·승인 정비자료 | 도면과 실물동일성·회전/배출 관찰수단 |
| 1_30 케이블 양끝·경로·준공 길이 | 승인 준공도·케이블마킹 | CV4×1.5·LEN99 열과 실제시공 |
| Filter 현행 로직·문턱·세정 관찰 | 승인 PLC/HMI·운영기록 | ≤·Forza ON 가지·현재값·세정 결과, 값변경 권고 아님 |
| 시간누계/영구저장 설계·이력 | 외부 기록부·HMI 설계 | HOUR1/0과 실제누계의 관계 |
| 고장/조치/복구 이력 | 승인 수리기록 | 원인제거·재요청·실제배출·재발 없음 |

### 7.2 네 기능과 기록 보존

| 기능 | 적용 | 이번 상태 |
|---|---|---|
| 도면·래더 나란히 비교 | 적용가능: FG62↔LAD1967/1811, FG121↔원시/처리 전달 | 근거쌍 제안만. UI 구현/실제 링크·강조 미검증 |
| 백업 미리보기·선택복원 | 후속 VR04 지원을 별도 확인 | 구현·저장·재읽기·재열기 실행0 |
| 기록 전후비교 | 관찰항목이 마련되면 적용가능 | 실제기록 생성/편집·동시성·실패 시험0 |
| 관찰보고서/PDF | 후속 관찰기록과 결속 필요 | 보고서 생성/UI 인쇄 검증0. 원본PDF 렌더와 다름 |

후속 구현은 note/repair_observation·미지필드/행·다른설비·초안·저장키와 0/빈칸을 보존해야 한다. generated_with/saved_with는 생성·저장 근거이며 현장CPU 증명이 아니다. 과거기록에 새근거를 소급 적용하지 않는다. 이 조사는 구현/합성QA·사용자운영 기록을 만들지 않았다.

### 7.3 확인·미실행 상태

- 수행: 읽기 전용 preflight, 원본 선언·핀·주소·부정·OR·쓰기범위 정적 추적, PDF7페이지 실제 렌더, 선택 원본 SHA-256 대 Git blob 대조, 중지5 freeze 해시 대조, 시작/종료 Git 상태.
- 완전한 대상 네트워크 의미 검토: `0267` 5Part/9Wire, `0445` 9Part/17Wire, `0328` 7Part/18Wire. 나머지 공동 네트워크는 이 초안에 서술한 관련 분기·호출·Word경로만 검토했다. 그 파일 전체 또는 PLC 전체의 의미검증 완료가 아니다.
- 파생추출의 UID/RID 후보는 이름 충돌·NID·상위 DB를 검토해 사용했다. HMI4데이터 ORef는 미결속으로 남겼다. 해시일치·XML파싱·preflight 수량을 의미검토·현장완료 수량으로 합치지 않는다.
- 미실행: 매뉴얼 생성기·npm test/build·필수14/UI/기록/BC01 회귀·패키지/ZIP/게시검증. 원본 읽기 전용 조사 범위라 실행하지 않았다. TIA 컴파일/CPU/현장·시뮬레이터 시험 미수행.
- 별도 독립검토는 대기다. 이 작업자의 자체 원본 대조와 독립검토를 동일하게 표시하지 않는다.

| 구분 | 상태 | 근거·경계 |
|---|---|---|
| documentation | draft_ready_with_gaps | 7영역 연구초안, 후속검토용 |
| static_review | scoped_source_review_done; independent_review_pending | 대상3네트워크 전체·공동분기·PDF7쪽. 제품회귀검사 미실행 |
| ui_records | not_run | 구현·기록시험·보존회귀 없음 |
| publication | not_published | 초안만, 배포/버전변경 없음 |
| tia_compile | not_performed | TIA 실행0 |
| live_cpu | not_performed | 현재값·프로젝트 대조0 |
| field_recovery | not_performed | 실물/관찰/복구 확인0 |

다음 한 조치는 이 초안의 핵심 원본을 별도 검토하는 것이다. 특히 startup Word덮어쓰기, Filter의≤와 Forza ON별도가지를 놓치지 않아야 한다. 후속 통합은 새 승인범위를 확인한 뒤에만 별도 수행하며 이 문서는 로컬133 통합을 개시하지 않는다.

## 부록 A. 원본 위치 목록과 해시 의미

다음 표는 본 조사에 사용하거나 보존 확인한 선택 파일의 SHA-256이다. Git 고정 커밋 blob과 같은 바이트인지를 확인한 결과이며, 각 파일 전체 의미를 모두 검토했다는 뜻이 아니다. 중지자산은 해시 보존만 검토했다. 파생자료는 탐색용이다.

선택 파일 **89개**가 고정 커밋과 바이트일치, 그중 중지5자산은 freeze 해시도 일치했다. 원본 Git 시작·종료 변경0. 이 숫자는 근거·보존 해시 수이며 의미검토 완료 수가 아니다. 대상 전체검토3네트워크와 공동분기·원본PDF7페이지의 검토범위는 본문에 따로 명시했다.

| 파일 | SHA-256 |
|---|---|
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` |
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
| `all-in-one/sources/decoded-original/0024-FlgNet.xml` | `a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67` |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` |
| `all-in-one/sources/decoded-original/0064-IdentXmlPart.xml` | `ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d` |
| `all-in-one/sources/decoded-original/0067-IdentXmlPart.xml` | `0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628` |
| `all-in-one/sources/decoded-original/0068-IdentXmlPart.xml` | `0a71d492e69760390b99f71a75f02ef684e271554b003d5de8bf64a26c64eeba` |
| `all-in-one/sources/decoded-original/0147-FlgNet.xml` | `386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c` |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` |
| `all-in-one/sources/decoded-original/0164-FlgNet.xml` | `15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491` |
| `all-in-one/sources/decoded-original/0165-FlgNet.xml` | `4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88` |
| `all-in-one/sources/decoded-original/0166-FlgNet.xml` | `0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853` |
| `all-in-one/sources/decoded-original/0200-FlgNet.xml` | `2bd1be34eb905a10d840c59aeb461464a1af418fa0ea3f2b8d0b3f88145eb27e` |
| `all-in-one/sources/decoded-original/0219-FlgNet.xml` | `245409937abf7e28f25a24d4a6d311a801a4b2ee7293148be9b3d266352eb53a` |
| `all-in-one/sources/decoded-original/0262-FlgNet.xml` | `f1f7a0d69692ada132c134fd7c6272eea8e183e77e41fd6ea96742c6abe68c19` |
| `all-in-one/sources/decoded-original/0264-FlgNet.xml` | `9af15015b447731255eff81680aa71321fb4d0ebe2c28904f442146538ff030d` |
| `all-in-one/sources/decoded-original/0265-FlgNet.xml` | `f2471b6ab6169e4c082983ea2080a383cf8b13cba4503a9a07f83d0956fbf08a` |
| `all-in-one/sources/decoded-original/0267-FlgNet.xml` | `a4b23258e13c1e750e587b72a4dab05f2184954d029a24e29efd1b23652c9801` |
| `all-in-one/sources/decoded-original/0328-FlgNet.xml` | `7b05b92a205d7c1b5dc6fb81aaaf92f017a286e1840cc3002d1d2744f9fe9df1` |
| `all-in-one/sources/decoded-original/0340-FlgNet.xml` | `00acb073128337e7d7b95bbedeb50cd0e72c89772d835bdf392da17b3e2d0add` |
| `all-in-one/sources/decoded-original/0341-FlgNet.xml` | `e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96` |
| `all-in-one/sources/decoded-original/0383-FlgNet.xml` | `16aa571742e3ec6538b191b4b830df83680f9fe9b5dc0dc6b4d2daba24bd2347` |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` |
| `all-in-one/sources/decoded-original/0401-FlgNet.xml` | `60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae` |
| `all-in-one/sources/decoded-original/0445-FlgNet.xml` | `14e7d301a96a6acdcf05bc8ff14ba7c8711cb2ae20b4a2352e49c8dfdd7f9b9a` |
| `all-in-one/sources/decoded-original/0546-FlgNet.xml` | `14d5214e135425b0499d8533926bc10b3d8b6e240b1fabc8def41d1cdb163f95` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` |
| `all-in-one/sources/decoded-original/0555-IdentXmlPart.xml` | `46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` |
| `all-in-one/sources/decoded-original/0575-IdentXmlPart.xml` | `40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06` |
| `all-in-one/sources/decoded-original/0576-IdentXmlPart.xml` | `c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe` |
| `all-in-one/sources/decoded-original/0577-IdentXmlPart.xml` | `511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47` |
| `all-in-one/sources/decoded-original/0578-IdentXmlPart.xml` | `0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b` |
| `all-in-one/sources/decoded-original/0594-IdentXmlPart.xml` | `88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd` |
| `all-in-one/sources/decoded-original/0595-IdentXmlPart.xml` | `10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52` |
| `all-in-one/sources/decoded-original/0596-IdentXmlPart.xml` | `a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0` |
| `all-in-one/sources/decoded-original/0597-IdentXmlPart.xml` | `60e292145fe54912a1da7510c8641a4f4c85efe62e1b5206ee3d92794a28de20` |
| `all-in-one/sources/decoded-original/0598-IdentXmlPart.xml` | `dc001c9370a691546c5dea79f5a1252d6d0a5564754703018c47df4bcc2522bb` |
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
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` |
| `all-in-one/sources/decoded-original/0689-IdentXmlPart.xml` | `f0cc6f770c2759b92a9a79f4e289dbfa0ca270d90e0e89496f94a13a8d839d51` |
| `all-in-one/sources/decoded-original/0690-IdentXmlPart.xml` | `fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` |

## 부록 B. 후속 독립 검토의 우선 대조점

1. LAD1967 요청Reset과 출력Coil을 혼동하지 않았는지, DB2/DB3의 startup Word0까지 포함했는지
2. LAD1811의2초·Tag76 T93·NOT처리Run·Set/Reset 선을 그대로 유지했는지
3. LAD1886의Le(≤), SC10/VR04 선행허가, LAD1885 Forza의 별도ON OR가지를 보존했는지
4. LAD1041 HOUR Move1과 LAD1053 세번째Move0·ENO 경계를 보존했는지
5. FG62 Q4.4/XS61·62/A1·A2/13·14/I5.5와 FG121 단자16·FG140 단자5가 원본렌더와 같은지
6. HMI4데이터 ORef미결속, 현행실물·극성·보호값·실제복구 미확정을 완료로 바꾸지 않았는지

검토 입력은 이 초안과 같은 고정 커밋의 원본이다. 별도 검토에서 수정될 수 있는 초안이며 제품/현장 완료를 뜻하지 않는다.


## 전달 전 핵심 근거 제한 대조
2026-10-11 고유 제어 Part/Wire 및 모터 회로의 실제 PDF 렌더를 표본 재확인하고 인용 원본 SHA256을 모두 재계산하여 일치했다. 이는 전체 원본 의미 검토 또는 현재 CPU/현장 검증이 아니다. 사용자 독립 검토 및 미확정 경계를 유지한다.
