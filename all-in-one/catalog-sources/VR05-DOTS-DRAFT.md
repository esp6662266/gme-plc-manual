# VR05 로터리 밸브 원본 조사 초안

VR05는 P&ID의 BF02 하부 SC11 출구에 그려진 로터리 밸브 VR-05/M39다. 전기 원본은 63KM1 접촉기 직접기동, PLC 출력 Q4.5, 원시 입력 I5.6을 연결한다. **I5.6은 63KM1 보조접점 13–14의 응답이며, 밸브 축 회전이나 분진 배출 완료를 직접 검출한다고 확인한 신호는 아니다.**

원본의 전용 고장 감시는 Tag_77(%T94), S5T#2S다. 처리 Run은 SC11 정지조건, BF02 세정허가, FN04 공유 예고장에도 쓰인다. BF02 분기의 차압 비교 상대는 원문 그대로 DP_01_SOGLIA_1이다. 운전시간 HOUR에는 누적 Add 대신 Move 상수1이 있고, 요청·알람에는 startup의 Word0 덮어쓰기가 있다.

이 문서는 고정 원본 조사와 후속 독립 검토용이다. 매뉴얼 통합·UI/기록 구현·게시·TIA 컴파일·현재 CPU·현장 복구의 완료 기록이 아니다.

## 작업 기준과 범위

- catalog_id VR05, 로터리 밸브, motor, 집진·석회, parent_id 없음, depth0, priority_key 없음, 별칭 없음. INVENTORY catalog[106], equipment[43]을 고유 ID로 확인했다. BF02와의 도면 관계로 catalog 부모를 새로 정하지 않았다.
- 작업3 자체 추가조사의 세 번째 5개 묶음 중 VR05 한 개다. 착수 전 TASK3-BATCH03-SCOPE.json의 중복·제외·부모보류 검토를 확인했다. 같은 이름인 VR01~VR06을 중복 ID로 합치지 않았다. 원래 phase2 후보133 및 로컬 2차133 통합 제외를 유지한다.
- 고정 읽기 원본: source-mv06, Git abcf31c5030bc7ef8749ed8e869a857f2387a28a, 프로그램 v1.12.0. 저장소 https://github.com/esp6662266/gme-plc-manual. 이후 main이나 현재 현장과 동일하다고 전제하지 않는다.
- GME-STD-1.0.0, AGENTS.md, gme-equipment-rollout 스킬, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, 최신 인계·버전·작업 기록을 읽었다. 읽기 전용 preflight 종료0, inventory_matches=true. 전체248·우선23·대응18·제외90·제외부모 하위보류7·phase2 133이 일치한다. 이것은 대장 일치이며 문서 완료 수가 아니다.
- preflight의 source_byte_changes는 requirements-audit.json과 all-in-one-data.json이다. 표준 생성 시점과 이 고정 버전 사이의 바이트 차이를 보존했고 이번 조사에서 갱신하지 않았다.
- 조사일 2026-10-11 UTC. 작성자는 VR05 원본 조사 작업자다. 실제 모델명/추론 설정을 증명하는 런타임 자료는 별도 미확보다.
- 작성 파일은 이 MD와 extracts/VR05/ 아래 정적 추출·렌더·검토자료뿐이다. 공용 declarations, 다른 초안, 원본, 공통 코드·버전·대장·배포·운영 기록을 수정하지 않았다. 기존 VR03 초안은 구성 참고만 하고 신호·핀·타이머·회로는 VR05 원본에서 확인했다.
- 보존 검사97파일의 SHA-256이 고정 커밋 Git blob SHA-256과 모두 일치했다. 이 중 중지5자산은 freeze 명세와도 모두 일치한다. 착수·종료 원본 Git 변경0이다. 97은 바이트 동일성 검사 수이며 의미 검토 완료 수가 아니다. 파일별 해시는 부록 B에 있다.
- 시뮬레이터 작성·수정·생성·실행·행동 시험, 실제 PLC·현장·보호값 변경, SEJIN 프로그램/운영자료/사진·이력 복제·통합은 수행하지 않았다. 금지 생성기와 행동 시험을 실행하지 않았다.

이하 파일 경로는 별도 언급 없으면 all-in-one/ 기준이다. 0268은 sources/decoded-original/0268-FlgNet.xml, 0604는 같은 폴더의 0604-IdentXmlPart.xml이다. LAD는 문서 ID, index_order는 색인 순서, NID는 선언의 네트워크 식별자다. 숫자가 같다고 같은 의미로 혼용하지 않는다.

## 7영역 적용표

| 영역 | 적용 상태 | 확보 근거 | 남은 경계 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | VR05/M39, BF02·SC11 도면 관계, 버전·대장 | 현행 실물·명판·준공 대응 |
| I/O·HMI | 적용, 일부 근거 미확보 | I5.6/Q4.5·DB2/3/9/13/14, HMI3행 | HMI 데이터 ORef4개·이벤트·현재 주소 |
| 제어 구조 | 적용 | 요청/출력, 자동 Set/Reset, startup Word0, SC11/BF02/FN04 의존 | 실제 호출·스캔·주기·외부 쓰기·현재 최종값 |
| 전기 전달 경로 | 적용 | FG63/121/140/254, 시공 p47/52, P&ID p1 렌더 | 실제 단자·극성·보호설정·시공 변경 |
| 알람·복구 | 적용 | Tag77 2초, Set/Reset·요청 Reset·공유 지연 구분 | 현장 원인 제거·재요청·복구 증거 |
| 증상별 수리 | 적용, 관찰 초안 | 요청→출력→접촉기→원시→처리→표시 관찰점 | 실제 관찰·조치 기록 없음 |
| 완료 기준 | 적용 | 정적 조사·부족자료·미수행 상태 분리 | 통합/UI/기록/게시/TIA/CPU/현장 별도 |

## 1 설비와 자료 소유

1. registers/equipment.json과 INVENTORY에서 VR05는 독립 catalog 항목이다. P&ID PID_1684n002I.pdf p1의 BF02 하부에 SC-11/M35가 있고 출구에 VR-05/M39, 0.55kW 440V가 표시된다. SC11·BF02와 VR05는 서로 다른 본체/구동/제어 소유를 가진 항목으로 유지한다.
2. Electrical_Rev2.pdf FG63/PDF64 제목은 ROTARY VALVE VR-05다. M39, 0.55kW/1.25A, THREE-PHASE LINE 440V 60Hz, 63QM1/63KM1/63QS1 회로가 있다. 검토한 직접기동 경로에는 전용 인버터·속도지령·엔코더·PID가 없어 그 경로에는 비해당이다. 추가 현장 장치가 전혀 없다는 뜻은 아니다.
3. BF02 차압 DP02, 압축공기, 세정 EV51~90은 필터측 자료다. 같은 도면에 있다는 이유로 VR05의 센서·알람·구동 출력으로 편입하지 않는다. 세정허가가 VR05 Run을 읽는 조건만 직접 연결 근거로 기록한다.
4. FN04 예고장과 Tag126 90분은 여섯 응답을 공유하는 FN04 조건이다. VR05 전용2초와 소유·목적이 다르다. FN04 인버터·속도·보호 정격을 VR05에 복제하지 않는다.
5. P&ID 도번1684n002, 원 작성일06/04/2011, 판 I 15/01/2013을 실제 타이틀 렌더에서 확인했다. 전기 FG63/121/140/254 하단은 기본 날짜27.05.2024다. 이 시트에 별도 Rev2 날짜는 확인되지 않았다. 파일명 Rev2만으로 모든 시트에 Rev2 17.03.2025를 부여하지 않는다.
6. 시공도 Electrical_Can_Decoating_20241118.pdf p47/52는 24.11.11 first draft design이며 CHECKED/APPROVED가 공란이다. 케이블 경로의 문서 근거로 쓰되 승인 준공·현재 길이·실물 배선으로 확정하지 않는다. PLC 백업·P&ID·전기·시공 자료의 시점을 구분한다.

## 2 I/O와 HMI

### 2.1 직접·내부·처리 신호

| 신호 | 원본 주소·형식 | 선언과 위치 | 해석·경계 |
|---|---|---|---|
| VR05_Fbk | Bool %I5.6 | live_index doc515; 0613 RID266, Input/AO46, NID44 UID2422 | 63KM1 보조접점 응답. 축회전·분진량 신호 아님 |
| Start VR05 | Bool %Q4.5 | doc1303; 0602 RID183, Output/AO37, NID38 UID1061 Write; 0658 RID138 UID1170 Read | PLC 출력명령. doc1303 주석 a53.3은 실제 Address Q4.5 및 도면 A4.5와 구분 |
| Flag.M_VR_05 | Bool DB2.DBX2.7 | 0604 RID182 BO/AO23, BAD2→0603 Flag/TOD N2; 0577 RID21 | 운전 요청·기억 비트. 출력·실물과 별도 |
| Allarm.VR_05_FAULT | Bool DB3.DBX2.7 | 0604 RID181; 0657 RID141 BO23, NID34 UID1175 Set/1178 Reset; 0655 Allarm/TOD N3 | 유지 고장. HMI DB11 표시주소와 같지 않음 |
| Inputs.VR05 Run | Bool DB13.DBX5.6 | 0604 RID221 BO46, NID33 UID23/NID34 UID998; 0657 RID302 UID1207; 0596 RID319 UID42; DB13은 0603/0655/0595 | 원시 입력에서 Word 전달되는 처리값. 별도 Writer 존재 |
| Tag_77 | Timer %T94 | doc1302; 0658 RID139, Timer/AO94, NID34 UID1172 Write/1173 Read | VR05 고장 S5 타이머이며 HMI 태그가 아님 |
| Flag.RESET_ALLARM | Bool DB2.DBX6.0 | 0657 RID13 BO48, NID34 UID1176; 0655 Flag/TOD N2 | 공통 Reset 요청. 복구·재기동 완료가 아님 |
| ON | Bool %M0.0 | 0602 RID1 UID1057, 0658 RID1 UID1169 | 공통 허가 접점. 이름만으로 항상 TRUE라 가정하지 않음 |
| hours motors.VR_05_MIN | Int DB9.DBW172 | 0615 RID268 BO1376, NID44 UID2423/2425/2426/2431; 0614 RID5/TOD9 | Add1·Move0 대상. 현재 누계·단위 운용 미확인 |
| hours motors.VR_05_HOUR | Int DB9.DBW174 | 0615 RID270 BO1392, NID44 UID2429 및 NID55 UID3093 Write | Move1·공통 Move0. 누적 Add로 설명 금지 |
| Tag_47 / Tag_48 | Timer %T13 / %T17 | 0613 RID1/AO13, RID284/AO17 | 공통 시간·기록후 초기화 타이머 |
| Flag_Aggiorna_DB | Bool %M1.7 | 0613 RID13 Memory/AO15, NID44 UID2432 | 공통 데이터 갱신 요청. 영구 저장완료를 보증하지 않음 |

SAD 영역·OD 타입/크기·SSD AO·멤버 BO·BAD→DepDBBlock TOD를 대조한 원본 주소다. 현재 CPU 프로젝트, 최적화 DB 구조, 온라인 값은 별도 확인한다.

### 2.2 Word 전달과 다른 쓰기

- LAD1070/0397 hmi inputs index1/NID1: Part35 Move.in은 ORef36/RID10 Tag_180(W39), out1은 ORef37/RID11(W40). 0627의 Tag_180은 Word/Input/AO32=%IW4, 0629 RID11은 Word/AO32/BAD4, 0628 RID4 Inputs/TOD13이다. 따라서 IW4→DB13.DBW4이며 I5.6과 DB13.DBX5.6이 같은 바이트/비트 위치로 대응한다.
- Part22.eno→27.en(W34), 27.eno→35.en(W41)의 연쇄와 DisableENO=true를 보존한다. 실제 TIA 판본에서의 ENO 유효성·매 스캔 실행은 확인하지 않았다.
- main LAD1613/0030 index2/NID19: CRef21 Recipes Handler→23 HMI→25 HMI Output의 W31/32/33 연쇄 뒤 CRef25.eno→Contact37 NOT Simulation(1)(W42/44)→CRef28 HMI Inputs.en(W43). 0688 RID135/UID29가 HMI Inputs, 0692 RID140/UID45가 Simulation(1)이다.
- 0635 RID134는 Inputs.VR05 Run에 NID4 UID65 AK Write를 가진다. 고정 원본 simulation LAD1085/0405에 다른 Writer가 존재한다는 사실만 보존한다. 정지 자산의 활성 여부·행동을 시험하거나 수정하지 않았다. 따라서 처리 Run의 Writer가 Word Move 하나뿐이라고 결론내리지 않는다.
- LAD356/0401 hmi output은 **출력 읽기**다. Part24.in ORef37/RID30 Tag_282=%QW4(W62), out1 ORef38/RID51(W63); 0632의 Output/AO32 Word와 0633의 BAD26·AO32 Word 및 0064의 Output/TOD14를 대조하면 QW4→DB14.DBW4다. Q4.5를 덮어쓰는 Move로 오독하지 않는다. Part22→23→24 ENO 연쇄(W57/60) 역시 호출과 분리한다.
- main LAD1616/0546에는 IW4 읽기 ORef161/RID28→Move151.in(W173), out1 ORef162/RID29(W174) Word_outputs.WORD3 경로가 있다. 이름 Word_outputs만으로 Q영역에 쓰는 경로라고 설명하지 않는다. 그 저장부와 VR05 처리 Run DB13은 별도다.
- 요청과 고장의 Word0 덮어쓰기는 §3.3에 별도 기록한다. 이름 없는 절대주소 접근을 비트명 검색에서 누락하지 않는다. 외부 HMI·통신·간접주소·현재 CPU 쓰기까지 유일 Writer임을 증명한 것은 아니다.

### 2.3 HMI 설정, 호출, 미결속

sources/hmi_plc_tags.csv의 표기는 dde.cfg 설정이며 온라인 현재값이 아니다. 직접 VR05 행은3개, Access Name=PLC다.

| 행 | 태그 | 설정주소 | 내부 ID | 확정 범위 |
|---|---|---|---|---|
| 131 | VR_05\Allarme1 | DB11,X62.1 | 00330 | 고장 표시주소 설정 존재 |
| 419 | VR_05\RispostaA | DB11,X62.0 | 001B8 | 응답 표시주소 설정 존재 |
| 454 | VR_05\Flag | DB2,X2.7 | 00190 | M_VR_05 원본 주소와 일치. 버튼 이벤트·쓰기 권한·시점 별도 |

LAD1208/0384 hmi index31, 제목 vr05. CRef22/RID638의 내부 CodeBlock23/RID1은 0623의 HMI Standard Motors와 맞고 호출 인터페이스는 0624다. network-map의 inferred_original_nid는 null이다. UID/RID와 해당 NID의 이름 선언을 결속하지 못한 데이터 ORef4개는 다음과 같이 남긴다.

| Wire | 원본 핀 | 선언/해석 상태 |
|---|---|---|
| W21 | rail→CRef22.en | 호출 허가선 |
| W37 | ORef24/RID660→Ingresso_run | 검색문자열 Inputs.VR05 Run 후보, 대응 선언 미결속 |
| W39 | ORef26/RID366→Allarme1 | Allarm.VR_05_FAULT 후보, 대응 선언 미결속 |
| W40/41/42/43 | ORef27/28/29/30, 모두 RID48→Allarme2/3/4/5 | 0626 FALSE 선언·UID 기록은 존재, 최종 NID 결속 별도 |
| W46 | CRef22.Risposta→ORef33/RID367 | Motors.VR05.Risposta 후보, 이름·주소 미결속 |
| W48 | CRef22.Comulativo_allarmi→ORef35/RID369 | Motors.VR05.Allarme_comulativo 후보, 이름·주소 미결속 |

함수 자체 LAD331/0355 NID1과 0621 Local 선언에서는 Ingresso_run Contact23→Risposta Coil27(W22/25/26), Allarme1~5의 Contact33/36/39/46/30→OR41→Comulativo_allarmi Coil59(W32/35/38/45/29, W42~49, W57/58)를 확인했다. 함수 동작 구조가 있다고 0384의 미결속 네 데이터를 자동 확정할 수는 없다. HMI CSV, 호출 ORef, DB11 레이아웃, 화면 이벤트의 네 단계를 분리하며 DB3.DBX2.7이 DB11.DBX62.1에 실제 전달되는지 미확정으로 둔다.

## 3 제어 구조와 소유 영향

### 3.1 직접 요청 Reset과 출력

LAD1968/0268 motors1 index39/NID38의 5Part/9Wire를 원본 선언과 대조했다.

| 단계 | Part·Wire·ORef | 정적 해석 |
|---|---|---|
| 공통 허가 | W1076 rail→Contact1070.in, W1062 ORef1057/RID1 ON→operand | ON 뒤 두 분기 |
| 고장에 의한 요청 해제 | W1071→Contact1072.in, W1063 ORef1058/RID181 fault→operand, W1073→RCoil1052.in, W1065 ORef1059/RID182 M_VR_05→operand | ON AND fault→운전요청 Reset |
| 출력 | W1071→Contact1074.in, W1066 ORef1060/RID182 M_VR_05→operand, W1075→Coil1056.in, W1068 ORef1061/RID183 Start VR05→operand | ON AND 요청→Q4.5 일반 Coil |

출력 분기 자체에 NOT fault가 직렬로 있는 형태가 아니다. 고장으로 요청을 Reset하는 별도 분기다. 같은 스캔의 Set·다른 Word/HMI 쓰기와 최종값 우선순위는 별도 검토 대상이다. 이 네트워크에 전용 Local/Auto·Maintenance·회전검출 접점이 없다고 전체 안전조건이 없다고 결론내리지 않는다.

### 3.2 자동 Set·전체정지 Reset

0577 RID21 M_VR_05의 Write 선언은 NID3 UID600, NID4 UID944, NID5 UID1020이다. 아래 고유 핀과 원본 상수를 확인했다.

| 기능 | 원본 상위 조건·비교 | VR05 쓰기 |
|---|---|---|
| 예열 | LAD1843/0164 index3/NID3. ON Contact785→NOT Emergency22→Eq400(Tipo_preset=1)→Auto_ON1 Contact823. W672→Eq416.pre, ORef596 Tempo 및 ORef597/RID18 Int3 비교(W679/680) | Eq416.out W681→SCoil424.in, W684 ORef600/RID21→operand |
| 생산 | LAD1844/0165 index4/NID4. ON1145→NOT Emergency1154→Auto_ON1 1147→Eq737(Tipo_preset=2). W1021→Eq753.pre, ORef940 Tempo/ORef941 RID18 Int3(W1028/1029) | Eq753.out W1030→SCoil761.in, W1033 ORef944/RID21→operand |
| 전체정지 | LAD1847/0166 index7/NID5. Auto_ON1 Contact1095→Eq881(Tipo_preset=5). W1031이 Eq957.pre 및 Emergency1106.in 허가. ORef1016 Tempo/ORef1017 RID102 Int20 비교(W1076/1077). Eq957.out W34와 Emergency1106.out W35→OR33 | W1078 OR33.out→RCoil965.in, W1081 ORef1020/RID21→operand |

전체정지의 해당 분기는 Auto_ON1 AND Tipo5 AND (Tempo20 OR Emergency)다. Emergency가 모든 모드에서 무조건 이 Reset을 수행하는 식으로 확대하지 않는다. Tempo3/20은 원문 비교값이며 실제3초/20초라고 이름만으로 단정하지 않는다.

0578의 Tipo상수 RID8/UID591 V1, RID78/UID935 V2, RID22/UID985 V5와 Tempo상수 RID18/UID597·941 V3, RID102/UID1017 V20을 대조했다. 0577의 Tipo_preset는 RID12 Int/BO784=DB1.DBW98, Tempo_presetting는 RID7 Int/BO768=DB1.DBW96, Auto_ON1은 RID4 Bool/BO59=DB2.DBX7.3, Emergency_module_fault는 RID108 Bool/BO134=DB3.DBX16.6이다. DB번호는 0576의 Data/Flag/Allarm TOD로 확인했다. 현재 값·주기·변경 경로를 재설정하는 작업은 아니다.

### 3.3 비트명 밖의 startup Word 덮어쓰기

요청의 비트 Set/Reset4위치에 더해 **DB2.DBW2 전체0 Write**가, 알람 Set/Reset에 더해 **DB3.DBW2 전체0 Write**가 각각 겹친다.

| 대상 | 원본 경로 | 선언 대조와 겹침 |
|---|---|---|
| 요청 DB2.DBX2.7 | startup only LAD402/0147 index2/NID2. ON Contact208.out W209→Move138.en, Move138.eno W187→Move141.en. ORef170/RID54 INT#0 W188→Move141.in, W189 out1→ORef171/RID9 | 0048 RID54 V0, 0563 RID9 Word/AO16/BAD6, 0562 RID6 Flag/TOD2. DB2.DBW2가 바이트2/3 전체를 쓰므로 M_VR_05 포함 |
| 알람 DB3.DBX2.7 | startup only LAD403/0148 index3. ON Contact329.out W330→Move250.en, Move250.eno W306→Move253.en. ORef287/RID54 INT#0 W307→Move253.in, W308 out1→ORef288/RID26 | 0047 ON UID284 NID3, 0048 V0 UID287 NID3, 0563 RID26 Word/AO16/BAD23 NID3 UID288 Write, 0562 RID23 Allarm/TOD3. DB3.DBW2가 fault 포함 |

0148의 탐색 색인은 inferred NID=null이지만 이 경로의 ON/상수/Word 목적지 선언은 모두 NID3·해당 UID/RID로 대조됐다. 그 차이를 숨기거나 전체 HMI 미결속을 함께 해결된 것으로 세지 않는다. block_summary의 startup only 속성 Event class=startup, Title=power up - start up은 탐색 보조 근거다. 현재 CPU의 startup 구성·실제 실행·재시작 후 값은 검증하지 않았다. 재시작을 복구 수단으로 권고하는 문서가 아니다.

### 3.4 SC11 요청에 미치는 영향

LAD1963/0263 motors1 index34/NID33. ON Contact963 뒤 fault Contact965.out→OR934.in1(W966), NOT Inputs.VR05 Run Contact22.out→NOT UNDER TESTING Contact969.in(W24)→OR934.in2(W970), OR934.out W956→RCoil939.in, W958 ORef948/RID162 M_SC_11(DB2.DBX2.3)→operand다.

식은 ON AND [SC_11_FAULT OR (NOT VR05 처리Run AND NOT UNDER TESTING)]→SC11 요청 Reset이다. ORef23/RID221(W21)가 VR05 처리Run, ORef947/RID4(W954)가 UNDER TESTING이다. 후자는 원문 경계이며 임의 우회 지시가 아니다. 별도 M_SC_11 Contact971→Start SC11 Coil943(W972/961)가 있으므로 VR05 자체 출력회로와 SC11 출력회로를 합치지 않는다.

### 3.5 BF02 세정허가의 고유 분기

LAD1886/0219 filter index5/NID29의 BF02 분기:

1. ON Contact21.out(W49)→SC11 처리응답 Contact28, W61 ORef41/RID305. Contact28.out W62→VR05 처리Run Contact29, W63 ORef42/RID319.
2. Contact29.out W64는 Int 비교 Le Part30.pre와 Forza_Lavaggio Contact31.in에 함께 연결된다.
3. W65 ORef43/RID31 Data.DP_02→Le30.in1; W66 ORef44/RID8 Coeff.DP_01_SOGLIA_1→Le30.in2. 비교는 **DP_02 <= DP_01_SOGLIA_1**이다. 이름을 DP_02_SOGLIA_1로 고치거나 부등호를 반대로 해석하지 않았다.
4. Le30.out W67→OR32.in1, Forza_Lavaggio Contact31.out W69→OR32.in2. Forza operand는 ORef45/RID57(W68)다. 두 가지 모두 상위 ON·SC11 Run·VR05 Run 뒤에 있으므로 Forza가 VR05 Run 조건을 건너뛰는 식이 아니다.
5. OR32.out W70→Coil33 Abilita_lavaggio_BF02, W71 ORef46/RID65. Coil33.out W76→Coil78 BF02_RUN, W77 ORef79/RID344.
6. 0596/0595의 DP02는 Int DB1.DBW242(BO1936), DP_01_SOGLIA_1은 Int DB4.DBW138(BO1104)이다. SC11 처리응답은 DB13.DBX5.1, VR05는 DB13.DBX5.6. 0598의 Abilita_lavaggio_BF02·Forza_Lavaggio는 Local InterfaceAccess이며 현장 출력주소로 만들지 않는다. 0594 BF02_RUN은 Bool Memory/AO1444=%M180.4다.

요약식은 ON AND SC11 처리Run AND VR05 처리Run AND [(DP02 <= DP_01_SOGLIA_1) OR Forza_Lavaggio]의 허가다. DP 정규화·단위·현재 임계값·Forza 생성·필터 세정출력 전체 순서와 실제 압축공기 상태는 이번 VR05 경계 밖이다. 원문 차압값을 안전 설정치나 보호값으로 추천하지 않는다.

### 3.6 FN04 공유 예고장과 정지

- LAD1964/0264 index35/NID34에서 ON1020→Inputs.FN04 Run1022 뒤 SC01/VR03/SC10/VR04/SC11/VR05 처리응답의 각각 부정 접점1024/1026/1028/1030/1032/1034가 OR972.in1~6으로 들어간다. VR05는 ORef998/RID221(W1011)→NOT Contact1034→OR.in6(W1035).
- OR972.out W1012가 Coil982 Prealarms_FN04, SdCoil985, Tag126 Contact1036을 함께 허가한다. value ORef1000/RID112 W1014는 0606의 S5T#1H_30M(V13632), operand ORef1001 W1015 및 접점 ORef1002 W1016은 0602 RID169 Timer/AO131=%T131이다. Contact1036.out W1037→Coil990, W1018 ORef1003/RID170 Stop_Fan_FN04.
- 0605의 Local Stop_Fan_FN04는 NID34 UID1003 Write, NID35 UID1019 Read. LAD1965/0265에서 ON1038 뒤 Contact1042 operand(W1029)로 읽고 W1043→OR1003.in4→W1031 RCoil1010→W1033 Flag.M_FN_04 요청 Reset으로 연결된다.
- 공유 예고장·90분 지연은 VR05만의 전용 알람이 아니다. FN04 Run, 다른 다섯 응답, 다른 FN04 정지 원인과 함께 비교해야 한다. 현재 발생시각·타이머 누적·정지 원인을 실행 검증한 것은 아니다.

### 3.7 호출·실행 순서의 경계

| 원본 | 확인한 연결 | 미확정 |
|---|---|---|
| main LAD1619/0031 index8/NID6 | ON282.out W283→CRef264.en Allarms1, 내부 CodeBlock275/RID58, 0688 선언 | 실제 알람 스캔·현재 CPU·인터럽트 |
| main LAD1620/0549 index9/NID7 | ON350.out W351→CRef319 Motors1, CRef322 Filter, CRef334 time work motor. 0688의 RID67 UID337, RID70 UID339, RID82 UID347 | 색인 순서와 실제 실행순서·동시 writer의 최종값 구분 |
| cyc_int2 ogni1s LAD1723/0024 index5/NID4 | ON188.out W189→CRef183.en, CodeBlock186/RID39 Auto start motors(0067) | 블록명만으로 현재 인터럽트1초를 확정하지 않음 |
| main LAD1613/0030 | Recipes/HMI/HMI Output ENO 뒤 NOT Simulation(1)→HMI Inputs | 입력 전달·HMI 표시의 실제 시간 경계 |
| startup only LAD402/403 | 요청/알람 Word0 경로 존재 | 현재 startup 설정·전원 재시작·보존값 검증 없음 |

## 4 전기 전달 경로

전기 PDF64/122/141/257, 시공 PDF47/52, P&ID p1의 **7개 고유 원본 페이지를 실제 렌더·시각 확인**했다. P&ID 상세 크롭은 같은 p1이며 추가 페이지로 세지 않는다. FG와 PDF 번호를 구분한다.

| 경로 | 원본 | 확인한 양 끝점·중간 접점 | 남은 경계 |
|---|---|---|---|
| 3상 주회로 | FG63/PDF64 | 8.3L1/L2/L3(62/9)→63QM1 1/3/5–2/4/6→63KM1 1/3/5–2/4/6→63U1/V1/W1→XM63U1/V1/W1→63QS1 1/3/5–2/4/6→M39 U/V/W 및 PE | 공급·상순서·회전·명판·기계부 현황 |
| PLC 출력 끝점 | FG140/PDF141 | CPU515/MOD15 A4.5 단자6→63/4→FG63 A4.5. +24Vdc10.9→X21 3032 4A F 5×20→140.1→단자10, 0Vdc10.6→단자9 | 실제 모듈 형번·전원·출력전압 |
| 접촉기 제어 | FG63/PDF64 | A4.5(140/1)→XS63→63QS1 보조접점→XS64→63.1→63QM1 보조접점→63KM1 A1; A2→−0Vdc10.6 | QS/QM 보조접점 숫자단자 명확한 근거 미확보. 현장 극성·손상 여부 미확인 |
| 원시 피드백 | FG63/PDF64와 FG121/PDF122 | +24Vdc10.7→63KM1 13–14→E5.6(121/6)→FG121 E5.6, CPU515/MOD9 단자17, 역참조63/6 | 접촉기 보조응답이며 실회전/분진 배출 보장 안 함 |
| 입력 모듈 전원 | FG121/PDF122 | +24Vdc10.7→X21 3008 2A IST.5×20→121.1→단자20; −0Vdc10.6→단자19 | 실제 전원·퓨즈·배선 상태 |
| 현장 모터 케이블 | 시공 p47/52 | 2_2 =DUS+VR05-M39A, CR→VR-05/M39. p47 Route223 RA→Pipe16 분기5→M39; p52 경로100→200→220→221→223 RA→E400 | 현장 마킹·케이블 양끝 코어/단자·승인 준공·실제 길이 |

### 정격·BOM·시공 수치의 경계

- FG63은 M39 0.55kW/1.25A, 63QM1 범위1.1–1.6A, 패널 BLACK FS17 1.5mm²를 적고 있다. 도면의 정격과 범위일 뿐 현재 보호설정이나 안전한 설정 추천값이 아니다.
- FG254/PDF257의 63KM1 행은 3RT2015-1BB41 CONTACTOR3KW/1L/DC24V/S00 및 3RT2916-1CB00 RC 부속이다. 63QM1 묶음은 첫 줄3RV2901-1E 보조접점, 3RA1921-1DA00 고정구, WR32433 어댑터, 3RV2011-1AA10 MAGNETOTHERMIC1.1–1.6A를 포함한다. 수량은 각1이다. 첫63QM1 행을 차단기 본체 형번으로 잘못 읽지 않는다.
- BOM 제조사 표기는 Siemens, 어댑터 Whoner다. 현재 설치 모델·ABB 대체품·토크·정비주기·안전 한계는 명판과 승인자료 및 필요한 제조사 원문 없이 채우지 않았다.
- 시공 p52 2_2행은 GAC/CV/CORE4/SIZE1.5/SPARE0/Adjustment3/LEN94다. LEN94를 확인된 실측 미터로 확대하지 않는다. p47 Pipe16은 관로 표기이며 전선 단면적이나 접점단자가 아니다.
- 63KM1 주접점1/2·3/4·5/6, 코일A1/A2, 보조13/14를 구분한다. +24Vdc10.7은 피드백 공급, A4.5는 출력명령으로 같은 관찰점이 아니다. 같은 DUST ZONE13의 DP02/JB01TB6 또는 M34/M38/M35를 VR05 소유로 편입하지 않는다.

## 5 알람·복구·운전시간

### 5.1 VR05 전용2초 고장

LAD1812/0446 allarms1 index32/NID34, 9Part/17Wire.

| 단계 | 원본 핀·선 | 정적 해석 |
|---|---|---|
| 공통 허가 | rail W1205→ON Contact1193, W1179 ORef1169/RID1→operand | ON 뒤 감시/Reset 가지 |
| 출력 감시 | W1194→Start Contact1195, W1180 ORef1170/RID138 | Start VR05 명령을 읽음 |
| 응답부재 타이머 | Start1195.out W1196→NOT 처리Run Contact1206, W1209 ORef1207/RID302→operand; W21→SdCoil1157.in | ON AND Start AND NOT 처리Run |
| 시간/타이머 | W1181 ORef1171/RID28→value, W1182 ORef1172/RID139→operand | 0656 S5Time S5T#2S/V512, 0658 Tag77/%T94 |
| 고장 Set | Start1195.out W1196→Tag77 Contact1197, W1183 ORef1173/RID139; W22→SCoil1163.in, W1186 ORef1175/RID141 | ON AND Start AND Tag77 접점 결과→fault Set |
| 고장 Reset | ON1193.out W1194→RESET_ALLARM Contact1201, W1188 ORef1176/RID13; W1202→fault Contact1203, W1189 ORef1177/RID141; W1204→RCoil1168, W1191 ORef1178/RID141 | ON AND Reset AND fault→동일 fault Reset |

NOT 처리Run은 타이머 입력 가지이며 Set코일 경로에 직접 직렬 배치된 접점은 아니다. S5Time V512는 원문 인코딩값으로 512ms라 해석하지 않는다. 현재 타이머 진행·동시 Set/Reset 결과는 실행 검증하지 않았다. startup Word0 쓰기도 별개로 존재한다.

### 5.2 복구 판단

VR05 fault는 §3.1에서 M_VR_05 요청을 Reset한다. 알람 Reset으로 고장 비트가 내려가도 요청이 자동 복구됐거나 기계 원인이 제거됐다는 증거는 아니다. 자동 Set, HMI 요청쓰기, startup 및 실제 호출순서와 같은 시각의 값을 대조해야 한다. 현장 자격자와 승인 절차에 따라 보호·전원·접촉기·모터/밸브·실제 배출 상태와 원인 제거를 확인하고 재요청 및 재발 여부의 증거를 남긴다. 이 초안은 Reset·재기동·강제출력·보호우회를 수행하거나 승인하지 않는다.

VR05 고장2초, BF02 세정허가, SC11 요청해제, FN04 예고장90분은 각각 다른 조건과 소유를 갖는다. 하나의 ‘VR05 알람’으로 합치지 않는다.

### 5.3 운전시간 Move1과 공통 Reset

LAD1042/0329 time work motor index41/NID44:

1. Tag47 Contact2450(W2433)→원시 VR05_Fbk Contact2452(W2434), W2453이 Add2404.en과 Ge2411.pre를 함께 허가한다. 처리Run이 아닌 원시 I5.6을 읽는다.
2. Int Add2404는 MIN ORef2423/RID268(in1 W2435) + 상수1 ORef2424/RID7(in2 W2436)을 MIN ORef2425(RID268, out W2437)에 쓴다.
3. Ge2411은 MIN ORef2426(W2438)와 상수60 ORef2427/RID8(W2439)을 비교해 W2440→Move2414.en을 허가한다.
4. Move2414.in은 ORef2428/RID7 **상수1**(W2442), out1은 ORef2429/RID270 HOUR(W2443)다. HOUR+1 Add가 아니다.
5. Move2414.eno W2444→Move2417.en, 상수0 ORef2430/RID12 W2445→in, MIN ORef2431 W2446←out1, eno W2447→SCoil2420, W2448 ORef2432 Flag_Aggiorna_DB.
6. 0616의 RID7 V1, RID8 V60, RID12 V0 및 NID44 UID2424/2427/2428/2430을 대조했다. MIN172/HOUR174의 현재 누계·overflow·저장주기·외부 누적 의미는 미확정이다.
7. LAD1053/0340 index52/NID55에서 Tag48 Contact3111→Move3070 FN04_HOUR0→Move3073 VR03_HOUR0→Move3076 VR04_HOUR0의 ENO 후 W3105→Move3079.en이 온다. ORef3092/RID12 상수0(W3106)→Move3079.in, out1 W3107→ORef3093/RID270 VR05_HOUR. 앞 Move의 ENO를 무시한 독립 초기화로 설명하지 않는다.
8. LAD1056/0019 index55/NID58은 NOT Tag47 Contact3120.out W3121→SdCoil3112, value ORef3114/RID335 S5T#1M(W3117), operand ORef3116 Tag47(W3119)이다. 이름만으로 실제 정확한1분 펄스나 현재 누적시간의 정확성을 보증하지 않는다.
9. LAD1055/0341 index54/NID57은 ON3147 뒤 Flag_Aggiorna_DB3149→MEM2_0 SCoil3110, MEM2_0 Contact3151 뒤 NOT Flag_Aggiorna_DB3153→SdCoil3118(value ORef3128/RID334 S5T#5S, operand Tag48), 같은 MEM2_0 뒤 Tag48 Contact3155→MEM2_0 RCoil3123이다. 제목의 ‘DB 기록 후 Reset’만으로 실제 영구저장 handshake 완료를 확인할 수 없다.

HOUR의0/1을 실제 누적시간·가동률·정비주기로 바로 사용하지 않는다. Move1을 오타라고 가정해 Add로 고치지 않았다.

## 6 증상별 관찰·원인 배제 초안

아래는 읽기·관찰 지점이다. 실제 고장 진단이나 활선 전기작업·라이브 시험 지시가 아니다. 현장 자격자와 승인된 안전 절차로 수집한다.

| 증상 | 먼저 비교할 관찰점 | 배제에 필요한 근거 | 복구 경계 |
|---|---|---|---|
| HMI 요청은 있으나 출력 없음 | DB2X2.7·ON·fault·Q4.5, 자동 Tipo/Tempo, startup | HMI 실제 Write, LAD1968 Reset, 자동 전체정지, Word0와 시각 | 화면버튼만으로 요청/출력 확정 금지 |
| Q4.5는 켜지나 밸브가 돌지 않음 | FG140 단자6, XS63/64, QS/QM, KM A1/A2·주회로, M39 상태 | 실물단자·명판·안전한 측정 및 기계 점검 | Q=1은 코일 여자·정상회전의 증거가 아님 |
| 기동 뒤 VR05 fault | Start·Tag77·I5.6·DB13X5.6·63KM1 13/14 | 명령/응답 타임라인,2초 조건, raw/Word/다른 Writer | 알람 Reset만으로 원인제거 완료 금지 |
| I5.6과 HMI 응답이 다름 | IW4→DB13W4, HMI Inputs 호출, DB11X62.0 | 실제 DB11·미결속 ORef4개·화면 이벤트·통신 | 표시 차이를 기계 고장으로 즉단하지 않음 |
| VR05 이상과 SC11 정지 동반 | VR05 처리Run, SC11 fault·M_SC_11, UNDER TESTING | LAD1963 두 Reset 원인·발생순서·실제 두 모터 | SC11 고장과 VR05 고장을 병합하지 않음 |
| BF02 세정허가가 없음 | SC11/VR05 처리Run·DP02·DP_01_SOGLIA_1·Forza·Local 허가·M180.4 | LAD1886의 직렬·OR·<=, 현재 단위/계수·필터측 자료 | Forza가 운전응답을 우회한다고 가정 금지 |
| FN04 예고장·후속 정지 | FN04 Run, 여섯 응답, Prealarms·Tag126·Stop_Fan_FN04 | LAD1964→1965,90분 및 다른 정지원인 | VR05만으로 FAN 정지원인 확정 금지 |
| 운전시간0/1·누계 이상 | I5.6·Tag47·MIN172/HOUR174·Tag48·업데이트 요청 | Move1/Move0, 외부 누계·영구저장·관찰시각 | 숫자를 실제 정비시간으로 환산 금지 |

관찰 기록에는 시각·시간대, 관찰자, 프로젝트/장치 버전, 실제 위치, 값/단위, 안전한 수집방법, 비교 원본, 배제 근거, 승인 조치, 재발 여부·복구 증거를 남긴다. 미관찰 칸을 정상값으로 채우지 않고 운영기록·사진을 공개 소스 초안에 복제하지 않는다.

## 7 부족자료와 완료 기준

| 필요한 자료 | 수집 위치 | 판정 목적 |
|---|---|---|
| 현재 PLC 백업·교차참조·DB 및 호출 설정 | 승인 TIA 프로젝트 | 고정원본 동일성, startup/주기·간접/외부 Writer·최종값 |
| HMI 원프로젝트·DB11 레이아웃·스크립트 | HMI/PLC 인터페이스 담당 | 0384 데이터 ORef4개·표시·DB2 요청쓰기 결속 |
| raw/처리/표시 동시 관찰 | 현장 승인 관찰 | I5.6→DB13X5.6→DB11/HMI의 시간차 |
| M39·63QM1/KM1/QS1 명판·단자 사진 | 현장 설비 승인자료 | 모델·정격·보호설정·극성·현재 결선 |
| 케이블2_2 준공 경로·코어별 양끝 | 승인 준공도/단자대 | CV4×1.5·LEN94 열값과 실물 대응 |
| BF02·SC11 배치·차압/세정 자료 | 승인 P&ID·필터 담당 | 도면 관계·실제 배출·세정허가 단위·Forza 생성 |
| 운전시간 저장·누계 설계 및 이력 | HMI/외부 기록부 | HOUR Move1·공통Reset의 실제 누계 의미 |
| 고장·조치·재요청·복구 이력 | 승인 수리관찰 기록 | 원인제거·정상회전/배출·재발 여부 |

### 네 기능과 기록 보존

| 기능 | 적용 판단 | 이번 상태 |
|---|---|---|
| 도면·래더 비교 | Q4.5→63KM1→I5.6→처리Run과 LAD1968/1812 연결에 적용 가능 | 근거만 준비, 기능/UI 구현·검증 안 함 |
| 백업·선택 복원 | 후속 VR05 지원 구현 시 요청/관찰기록을 분리할 필요 | 구현·저장·재읽기·재열기 미수행 |
| 기록 전후 비교 | raw/처리/명령/표시·시각 비교에 적용 가능 | 실제 사용자 기록 접근/변경 없음 |
| 보고서/PDF | 후속 관찰보고서에 해당 근거·미확정 포함 가능 | 원본 PDF만 읽기·렌더, 사용자 보고서 생성 없음 |

note/repair_observation, 미지 필드·다른 설비·초안·저장키 보존을 변경하지 않았다. generated_with/saved_with 정보가 관찰 당시 CPU 상태를 증명한다는 해석도 하지 않는다.

### 검증 범위와 최종 상태

- 원본 source-mv06의 착수 Git HEAD/상태를 확인했다. 읽기 전용 preflight, XML 파싱·UID/RID/NID/Part/Wire·주소/Word 중첩 검색, 원본 PDF 렌더·시각 검토, 원본/고정 Git blob 해시 대조를 수행했다.
- 해시 일치는 바이트 보존 검사다. 해당 파일의 모든 논리를 의미 검토했다거나 현재 PLC/현장을 검증했다는 수량으로 세지 않는다. 의미 검토 범위는 §2~5의 특정 경로·선언·핀과 아래 근거 색인이다.
- 독립 검토자는 아직 배정/완료되지 않았다. 공통 코드·BC01 회귀, UI/기록 보존, 링크/검색·PC/모바일·큰 글자, 저장·재읽기·재열기·동시성/실패, 패키지/ZIP/CSP/배포 검사는 수행하지 않았다. 조사 범위 밖이며 통합을 변경하지 않았기 때문이다.
- TIA 컴파일, 현재 CPU·현장 보호값·전기/기계 복구는 미수행. 시뮬레이터 및 관련 생성·행동 시험은 금지 범위로 미수행.

| 상태 축 | 결과 | 근거 |
|---|---|---|
| documentation | draft_ready | VR05 고유 원본 조사 초안 |
| static_review | author_source_review_done / bounded_spot_review_done | 아래 검토대상 및 해시 보존, 독립검토 별도 |
| ui_records | not_run | 구현/저장검증 범위 제외 |
| publication | not_published | 로컬2차133 통합·배포 범위 제외 |
| tia_compile | not_performed | 현재 프로젝트 실행검증 없음 |
| live_cpu | not_performed | 온라인 확인 없음 |
| field_recovery | not_performed | 실물 관찰·수리·복구 없음 |

다음 단계는 부모 검토자가 VR05의 주소·2초고장·BF02 <=/DP_01 임계값·startup Word0·HOUR Move1·PDF 끝점·미결속 HMI4개를 독립 대조하는 것이다. catalog 부모나 실물 동일성을 새로 확정하거나 로컬2차133 통합을 시작하는 승인으로 사용하지 않는다. 완료 커밋은 없다. 원본과 프로그램 변경이 없는 외부 조사 초안이다.

## 부록 A 의미 검토 범위 색인

| 원본 | 검토 범위 | 해석 한계 |
|---|---|---|
| 0268/LAD1968 | VR05 출력·고장 요청Reset 전체5Part/9Wire | 실제 최종값/전압 별도 |
| 0446/LAD1812 | 전용 고장 전체9Part/17Wire·Tag77 상수 | 현재 타이머/동시쓰기 별도 |
| 0164/0165/0166 | VR05 자동Set/Reset과 상위 허가·관련 상수 | 해당 블록의 다른 모터 전체 의미검토 수량 아님 |
| 0147/0148 | DB2W2/DB3W2의0 Write·앞 ENO·startup 선언 | 다른 Word의 모든 효과·실CPU startup 별도 |
| 0263/0264/0265 | SC11 Reset, FN04 공유예고장·Local 정지 연결 | 상대 설비 전체검증 아님 |
| 0219 | SC11/VR05 직렬·BF02 비교/Forza·허가/표시 Coil | 차압 환산·세정 순서 전체검증 아님 |
| 0329/0340/0341/0019 | VR05 시간계수·Move1/0·공통 타이밍/handshake | 외부누계·영구저장 별도 |
| 0397/0401/0546/0030 | IW4 처리전달, QW4 읽기, 별도Word 저장, 호출허가 | 블록 내 나머지 주소의 전체검증 아님 |
| 0384/0355 | HMI 호출 핀/상수와 함수 구조 | 데이터 ORef4개 미결속 유지 |
| 0031/0549/0024 | 알람/모터/필터/시간/자동 호출선·선언 | 현재 스캔·주기 별도 |
| 0405/0635 | 중지 자료 안 다른 처리Run Writer 존재 확인 | 실행·행동 검토/시험 아님 |
| 원본 PDF7페이지 | FG·단자 양끝·BOM·케이블·P&ID·판본 렌더 | 현재 실물·승인 준공·정상극성 별도 |

## 부록 B 원본 해시와 재현 자료

고정 커밋의 Git blob과 작업 사본을 SHA-256으로 각각 계산해 아래97파일 전부 일치했다. 원본 백업·PDF·선언·탐색자료·표준·중지자산을 포함하는 보존 검사 수다. 핵심 의미 검토 범위는 부록 A이며 파일 개수를 같은 뜻으로 사용하지 않는다. 중지5자산은 보존해시만 확인했으며 실행하지 않았다.

| 원본 경로 | SHA-256 | 고정 Git blob |
|---|---|---|
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b | 일치 |
| .agents/skills/gme-equipment-rollout/scripts/preflight.py | 395067d6da20af3e1d82a43b7936907a87a44d8d2e11e4ebc61b1fc441e2adb6 | 일치 |
| AGENTS.md | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 | 일치 |
| EXPANSION-WORK.md | ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2 | 일치 |
| PUBLICATION_STATUS.md | efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740 | 일치 |
| VERSION.json | 5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7 | 일치 |
| WORKSPACE-HANDOFF.md | 215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074 | 일치 |
| all-in-one/ACTIVE-WORK.md | eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2 | 일치 |
| all-in-one/assets/program-model-data.js | 52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f | 일치 |
| all-in-one/assets/simulator-workspace.js | 3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc | 일치 |
| all-in-one/assets/virtual-plc.js | 5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc | 일치 |
| all-in-one/registers/all-in-one-data.json | 63a46b36b6454bf1246d093300dbee11f2fcc287ad94991405369bf9f939a8fe | 일치 |
| all-in-one/registers/equipment.json | 7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa | 일치 |
| all-in-one/registers/program-model.json | 6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5 | 일치 |
| all-in-one/registers/requirements-audit.json | a10b773ff96e9b1c7a27cf409644c68d3eb59aedc5bcb5ca00199d602e63facb | 일치 |
| all-in-one/registers/simulator-freeze.json | bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835 | 일치 |
| all-in-one/registers/virtual-plc-test-results.json | a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64 | 일치 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd | 일치 |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 | 일치 |
| all-in-one/sources/GME_20250506.zap18 | 00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8 | 일치 |
| all-in-one/sources/PEData.plf | 647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a | 일치 |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b | 일치 |
| all-in-one/sources/block_summary.json | 68253f9366908244a27ed461c66d465da7ec1723571f27deaa9a6f81a542de63 | 일치 |
| all-in-one/sources/decoded-original/0019-FlgNet.xml | a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5 | 일치 |
| all-in-one/sources/decoded-original/0024-FlgNet.xml | a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67 | 일치 |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b | 일치 |
| all-in-one/sources/decoded-original/0031-FlgNet.xml | 76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65 | 일치 |
| all-in-one/sources/decoded-original/0047-IdentXmlPart.xml | 2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e | 일치 |
| all-in-one/sources/decoded-original/0048-IdentXmlPart.xml | d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d | 일치 |
| all-in-one/sources/decoded-original/0064-IdentXmlPart.xml | ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d | 일치 |
| all-in-one/sources/decoded-original/0067-IdentXmlPart.xml | 0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628 | 일치 |
| all-in-one/sources/decoded-original/0068-IdentXmlPart.xml | 0a71d492e69760390b99f71a75f02ef684e271554b003d5de8bf64a26c64eeba | 일치 |
| all-in-one/sources/decoded-original/0147-FlgNet.xml | 386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c | 일치 |
| all-in-one/sources/decoded-original/0148-FlgNet.xml | 1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313 | 일치 |
| all-in-one/sources/decoded-original/0164-FlgNet.xml | 15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491 | 일치 |
| all-in-one/sources/decoded-original/0165-FlgNet.xml | 4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88 | 일치 |
| all-in-one/sources/decoded-original/0166-FlgNet.xml | 0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853 | 일치 |
| all-in-one/sources/decoded-original/0219-FlgNet.xml | 245409937abf7e28f25a24d4a6d311a801a4b2ee7293148be9b3d266352eb53a | 일치 |
| all-in-one/sources/decoded-original/0263-FlgNet.xml | de5cef96279de6a92a6e9eb746a13f23c8889c0ba1701a18e74838c6c6dc3d34 | 일치 |
| all-in-one/sources/decoded-original/0264-FlgNet.xml | 9af15015b447731255eff81680aa71321fb4d0ebe2c28904f442146538ff030d | 일치 |
| all-in-one/sources/decoded-original/0265-FlgNet.xml | f2471b6ab6169e4c082983ea2080a383cf8b13cba4503a9a07f83d0956fbf08a | 일치 |
| all-in-one/sources/decoded-original/0268-FlgNet.xml | c6e891269b0fd733bd8eae5efefa573d9dc529b4135156f32cf54602d20e947a | 일치 |
| all-in-one/sources/decoded-original/0329-FlgNet.xml | 7aa07b96a1f1d7dee6c875abdd6dca86fa0b02874e2d6b21526f86f1575a164f | 일치 |
| all-in-one/sources/decoded-original/0340-FlgNet.xml | 00acb073128337e7d7b95bbedeb50cd0e72c89772d835bdf392da17b3e2d0add | 일치 |
| all-in-one/sources/decoded-original/0341-FlgNet.xml | e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96 | 일치 |
| all-in-one/sources/decoded-original/0355-FlgNet.xml | 73592d33f8b3a71effeb36f25427c76e931485e7ce31f5c81f144ddae83c4247 | 일치 |
| all-in-one/sources/decoded-original/0384-FlgNet.xml | add5f5694ea81f223395c3e3c9a7bbf0871c29596e6f66e576af49545d491dc5 | 일치 |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 | 일치 |
| all-in-one/sources/decoded-original/0401-FlgNet.xml | 60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae | 일치 |
| all-in-one/sources/decoded-original/0405-FlgNet.xml | 4290734017e68a9ded2a54a34c55d65cc7b2336296cb8d2d397e64f381b7947d | 일치 |
| all-in-one/sources/decoded-original/0446-FlgNet.xml | b6e1e5efb4ce5c59774e2d554e353e660e2c7d3fdf58f907294d759b8913190d | 일치 |
| all-in-one/sources/decoded-original/0546-FlgNet.xml | 14d5214e135425b0499d8533926bc10b3d8b6e240b1fabc8def41d1cdb163f95 | 일치 |
| all-in-one/sources/decoded-original/0549-FlgNet.xml | 49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1 | 일치 |
| all-in-one/sources/decoded-original/0562-IdentXmlPart.xml | 85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c | 일치 |
| all-in-one/sources/decoded-original/0563-IdentXmlPart.xml | 86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad | 일치 |
| all-in-one/sources/decoded-original/0575-IdentXmlPart.xml | 40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06 | 일치 |
| all-in-one/sources/decoded-original/0576-IdentXmlPart.xml | c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe | 일치 |
| all-in-one/sources/decoded-original/0577-IdentXmlPart.xml | 511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47 | 일치 |
| all-in-one/sources/decoded-original/0578-IdentXmlPart.xml | 0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b | 일치 |
| all-in-one/sources/decoded-original/0594-IdentXmlPart.xml | 88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd | 일치 |
| all-in-one/sources/decoded-original/0595-IdentXmlPart.xml | 10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52 | 일치 |
| all-in-one/sources/decoded-original/0596-IdentXmlPart.xml | a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0 | 일치 |
| all-in-one/sources/decoded-original/0598-IdentXmlPart.xml | dc001c9370a691546c5dea79f5a1252d6d0a5564754703018c47df4bcc2522bb | 일치 |
| all-in-one/sources/decoded-original/0602-IdentXmlPart.xml | 46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf | 일치 |
| all-in-one/sources/decoded-original/0603-IdentXmlPart.xml | e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8 | 일치 |
| all-in-one/sources/decoded-original/0604-IdentXmlPart.xml | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af | 일치 |
| all-in-one/sources/decoded-original/0605-IdentXmlPart.xml | 0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b | 일치 |
| all-in-one/sources/decoded-original/0606-IdentXmlPart.xml | 73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740 | 일치 |
| all-in-one/sources/decoded-original/0613-IdentXmlPart.xml | 09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb | 일치 |
| all-in-one/sources/decoded-original/0614-IdentXmlPart.xml | c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294 | 일치 |
| all-in-one/sources/decoded-original/0615-IdentXmlPart.xml | 80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a | 일치 |
| all-in-one/sources/decoded-original/0616-IdentXmlPart.xml | 650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d | 일치 |
| all-in-one/sources/decoded-original/0621-IdentXmlPart.xml | a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee | 일치 |
| all-in-one/sources/decoded-original/0623-IdentXmlPart.xml | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 | 일치 |
| all-in-one/sources/decoded-original/0624-IdentXmlPart.xml | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a | 일치 |
| all-in-one/sources/decoded-original/0626-IdentXmlPart.xml | a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b | 일치 |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb | 일치 |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd | 일치 |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 | 일치 |
| all-in-one/sources/decoded-original/0632-IdentXmlPart.xml | fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9 | 일치 |
| all-in-one/sources/decoded-original/0633-IdentXmlPart.xml | 9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc | 일치 |
| all-in-one/sources/decoded-original/0635-IdentXmlPart.xml | 1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457 | 일치 |
| all-in-one/sources/decoded-original/0655-IdentXmlPart.xml | 38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb | 일치 |
| all-in-one/sources/decoded-original/0656-IdentXmlPart.xml | 0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592 | 일치 |
| all-in-one/sources/decoded-original/0657-IdentXmlPart.xml | 0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b | 일치 |
| all-in-one/sources/decoded-original/0658-IdentXmlPart.xml | 998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831 | 일치 |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda | 일치 |
| all-in-one/sources/decoded-original/0689-IdentXmlPart.xml | f0cc6f770c2759b92a9a79f4e289dbfa0ca270d90e0e89496f94a13a8d839d51 | 일치 |
| all-in-one/sources/decoded-original/0690-IdentXmlPart.xml | fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541 | 일치 |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 | 일치 |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 | 일치 |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 | 일치 |
| all-in-one/sources/live_index.json | 14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1 | 일치 |
| all-in-one/sources/source-manifest.json | 5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf | 일치 |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc | 일치 |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 | 일치 |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 | 일치 |

검토 재현자료는 extracts/VR05/에 분리되어 있다. declarations.json·vr05-declarations.json은 이 조사 전용 추출이며 공용 파일이 아니다. 각 *-refs.json/*-wires.txt, overlapping-word-accesses.json, network-evidence.json, 원본 페이지 렌더, source-hashes.json, static-review.json, preflight.txt가 있다. extract.py/verify.py는 XML·해시·핀을 읽는 정적 조사 스크립트이며 시뮬레이터나 PLC 동작 모델이 아니다. verify.py 종료0의165개 단언은 XML/주소 구조61, 대장1, 파일해시97, freeze5, 원본 Git상태1로 구분된다. 전 설비·현재 CPU·현장 시험165개를 수행했다는 뜻이 아니다.


## 전달 전 핵심 근거 제한 대조
2026-10-11 고유 출력/요청 Reset의 원본 Part/Wire와 해당 모터 회로 실제 PDF 렌더를 표본 재확인하고 인용 원본 SHA256을 모두 재계산하여 일치했다. 전체 원본 의미 검토 또는 현재 CPU/현장/게시 검증으로 확대하지 않는다. 사용자 독립 검토와 미확정 경계는 유지한다.
