# MC03 예비 모터 · Dots 원본 조사 초안

- 작성 기준: 2026-10-11 UTC, GME-STD-1.0.0의 7영역 및 WORK-ITEM-TEMPLATE. 작업3 네 번째 묶음의 MC03 한 개에 대한 cloud 읽기 전용 추가 조사다.
- catalog_id: MC03. 이름: 예비 모터 MC03. 유형: motor. 그룹: 원료 이송. 부모: 없음. 별칭: mc03 / mc_03 / spare motor. 우선 P번호 없음. SS09는 대장상 별도 하위 ID이며 이번에 별도 설비 완료로 세지 않는다.
- 고정 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION 1.12.0. 최신 온라인 CPU·준공도·실물 설치 상태를 뜻하지 않는다.
- 범위 선정 근거: `progress/TASK3-BATCH04-SCOPE.json`, INVENTORY catalog index76 / equipment index3. 중복 제외 검토를 유지하며 `phase2/planned/physical_identity_verified:false`다. 로컬 통합 2차133 제외를 변경하지 않는다.
- 작성 결과만 `drafts/MC03-DOTS-DRAFT.md` 및 `extracts/MC03/`에 저장했다. 원본·공통 코드·대장·버전·배포·운영 기록·SEJIN·PLC/현장/보호값 변경 없음. 새 Work/Codex 생성, 재위임, 시뮬레이터 생성·수정·실행·행동시험 없음.
- 실행 모델/추론 수준: 실제 제품 선택값을 독립 관측하지 못함. 문서 표준의 모델 요청을 현재 관측값으로 바꾸지 않았다. 작성자: cloud 조사 담당. 별도 독립 검토: 아직 미수행.
- 표기: D/ = `all-in-one/sources/decoded-original/`, S/ = `all-in-one/sources/`, R/ = `all-in-one/registers/`. P=Part UID, W=Wire UID, O=ORef UID, R=RefId/RID. XML은 대다수 한 줄 선언이므로 파일·RID·NID·UID·핀을 정확 위치로 쓴다.

## 바로 사용할 핵심 결과

1. MC03의 직접 PLC 출력은 `Start Spare Motor %Q0.3`, 요청은 `Flag.M_MC_03 DB2.DBX0.3`이다. MC04의 `%Q0.4`나 MC05의 `%Q0.5`로 대체하지 않는다. D/0246 LAD1940/NID10 P318/W341/O327, D/0602 R61 및 D/0604 R60으로 결속했다. 현재 설치·실제 운전은 미확정이다.
2. 요청 해제는 `ON AND (MC_03_FAULT OR (NOT Inputs.MC04 run AND NOT Flag.STANDBY_ON) OR (MC_03_TORQUE AND NOT UNDER TESTING))`이다. MC04 응답은 타 설비 조건이며 MC03 소유 입력이 아니다. STANDBY와 UNDER TESTING은 서로 다른 분기에만 적용된다.
3. 운전응답 원시 입력은 D/0311에서 `102A7_SPARE5 %I0.5`, 알람용 처리 입력은 `Inputs.MC03 run DB13.DBX0.5`다. D/0397 Word Move가 IW0→DB13.DBW0을 전송한다. FG116/PDF117는 E0.5를 FEEDBACK SPARE MOTOR로 표시한다. 접촉기 보조접점 피드백을 실제 회전 센서로 설명하지 않는다.
4. FAULT와 TORQUE 네트워크는 둘 다 `OFF %M0.1` 접점 아래 있다. FAULT 타이머는 Tag_56 `%T53`, `SdCoil`, 원문 `S5T#2S`다. OFF라는 이름만 보고 항상 FALSE/네트워크 비활성이라고 확정하지 않는다. 반대로 일반 운전 중 정상 보호가 동작한다고 확정하지도 않는다.
5. 요청 DB2.X0.3, FAULT DB3.X0.3, TORQUE DB3.X3.4는 명명 비트 쓰기 외에 startup Word 0쓰기 범위에 포함된다. 0147의 DB2.DBW0, 0148의 DB3.DBW0/DBW2를 직접 대조했다. 전체 DB 초기화나 최종값 0의 증거는 아니다.
6. HMI `spare motor` 호출 D/0360 LAD1181은 존재하지만 8개 실제 피연산자의 MC03 선언 결속은 미완료다. 제공 HMI 태그 CSV에서 MC03/spare 이름 및 요청 DB2,X0.3 대응 행을 확보하지 못했다. MC04 HMI 주소를 복제하지 않는다.
7. 전기 FG23/PDF24는 제목과 모터 M05 모두 SPARE다. 4kW/7.6A 및 23QM1 7–10A는 도면 인쇄값이며 현재 명판·보호 설정이 아니다. 시공 PDF52 row2_5는 텍스트 층에 M05/SPARE가 남지만 실제 렌더는 검은 띠로 덮여 있다. 유효한 현행 케이블 행으로 채택하지 않는다.
8. 운전시간 LAD1021은 MIN에 Add1, MIN≥60이면 HOUR에 Move1이다. HOUR+1 누적이 아니다. LAD1049의 MC03 HOUR 0쓰기 역시 앞선 두 Move의 ENO 연쇄를 거친다. 기록 저장 성공·실제 누적 시간·복구 완료의 증거가 아니다.

## 7영역 적용표

| 영역 | 상태 | 이번 조사 | 남은 경계 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | MC03/예비/M05/SS09 및 MC04·MC05 분리, 고정 자료 시점 | 현재 설치·철거·전용·정상 사용 여부 |
| I/O·HMI | 적용, 일부 미확보 | Q0.3, I0.5/I6.4, DB2/3/9/13/14, Word전송, HMI 호출 | HMI 인스턴스·화면 이벤트·명명 외 writer |
| 제어 구조 | 적용 | 세 Reset 분기, 출력 Coil, 유지보수 쓰기, Main 호출, startup Word | 요청 Set 원천·전체 호출/덮어쓰기·현행 값 |
| 전기 전달 경로 | 적용, 일부 미확보 | FG8/10/23/116/122/136 실제 렌더, 전원·출력·단자·접점·SS09 | 유효 케이블 번호·현행 부품/접점·준공·실물 |
| 알람·복구 | 적용 | OFF, FAULT SD 2초, 토크 Set/Reset, 영향 | OFF 실제값·정상극성·복구/재기동 |
| 증상별 수리 | 적용, 관찰 설계 | 관찰 순서·비교 위치·원인 배제·수집 자료 | 실제 측정·조치·운전시험 미수행 |
| 완료 기준 | 적용 | 부족 자료·독립 검토 포인트·상태 분리·해시 | 통합/UI/기록/게시/TIA/CPU/현장 검증 |

## 1. 식별·자료·설비 소유

### 1.1 대장과 도면의 역할

- INVENTORY의 MC03은 독립 ID, phase2 planned, `existing_detail:baseline`, `bc01_standard_acceptance:not_assessed`다. R/equipment.json의 `status:예비·실물 동일성 확인`은 현장 확인 완료 표시가 아니다. preflight는 inventory_matches=true, 전체248/기존제외90/부모하위보류7/2차133을 확인했다. 이는 문서·현장 완료 수가 아니다.
- R/equipment.json의 MC03 `fgs:[23]`, `pid:false`, 별칭과 Q0.3/SS09 보관 문구를 확인했다. SS09는 `parent:MC03`인 별도 부품 행이다. 이 관계를 MC03 모터의 실물 확인이나 SS09 별도 조사 완료로 확대하지 않는다.
- S/PID_1684n002I.pdf PDF1 전체를 렌더로 검토했다. MC04/M09/SS10과 VS01은 배치되어 있으나 MC03 또는 M05/SS09를 MC03 공정 실물로 결속할 명시 태그를 확인하지 못했다. 문서 내 미확보일 뿐 실물 부재의 증거가 아니다. P&ID와 전기도면의 모터 태그를 이름만으로 치환하지 않는다.
- FG23의 SPARE/M05, Q0.3, E0.5, SS09/E6.4와 PLC spare/MC03 선언이 주소·교차참조로 대응한다. 이것은 백업·도면 사이 정적 대응이며 현재 설치 여부를 확정하지 않는다. 특히 숫자 M05를 MC05로 바꾸면 안 된다.

### 1.2 자료 시점과 상충 보존

- Electrical_Rev2.pdf FG23/116/8/10에는 기본 날짜 27.05.2024가 보이고 별도 REV2 행은 확인되지 않는다. FG122/136에는 REV2 17.03.2025가 있다. 파일명 Rev2를 모든 페이지의 개정으로 일괄 기입하지 않는다.
- FG8 본문은 THREE-PHASE LINE 440V 60Hz, 하단 제목은 400V 60Hz다. FG23 본문은 440V 60Hz다. 인쇄 상충을 그대로 기록하며 현장 정격 전압을 결정하지 않는다.
- 시공 PDF52는 CANDC-CONS-C002-052, 24.11.11 first draft design이다. 준공·승인·현재 적용 근거가 아니다. row2_5의 검은 렌더와 텍스트 잔존은 §4.6에 분리한다.
- S/GME_20250506.zap18 및 PEData.plf는 출처 바이트 보존용 해시만 기록했다. 현재 CPU와 비교·TIA 프로젝트 열기/컴파일은 하지 않았다. 백업 파일명 날짜를 현재 설치 시점으로 사용하지 않는다.

## 2. I/O·내부 메모리·HMI

### 2.1 고유 선언과 주소

| 신호 | 주소·형식 | 고유 선언/호출 위치 | 해석·미확정 |
|---|---|---|---|
| Start Spare Motor | %Q0.3 Bool | D/0602 SimpleAccess R61, SAD Output, SSD AO3; NID10 O327 AK Write. D/0658 R47 NID10 O396는 읽기 | MC03 기동 출력. 옛 CSV 설명 A48.7을 실제 Q주소로 쓰지 않음 |
| 102A7_SPARE5 | %I0.5 Bool | D/0613 R140, SAD Input AO5, NID23 O1288 | 운전시간에 쓰이는 원시 입력. FG116 E0.5의 예비 모터 피드백과 대조 |
| MC03_torque | %I6.4 Bool | D/0556 R240, SAD Input AO52, Monitor NID−2147483648 UID120 | 원시 토크 입력 선언. R/plc-symbols.csv 문서936은 SS-09 설명. 실제 정상극성 미확인 |
| Inputs.MC03 run | DB13.DBX0.5 Bool | D/0657 R272 AO5/BIRID247, NID10 O433/O400. D/0655 R247 TOD DB13 | 원시 I0.5와 영역을 구분하는 처리 입력 |
| Inputs.MC03 torque | DB13.DBX6.4 Bool | D/0657 R273 AO52/BIRID247, NID11 O408/O411 | SS09 원시값의 Word전송 대상 비트. 실물 정상극성 증명 아님 |
| Flag.M_MC_03 | DB2.DBX0.3 Bool | D/0604 R60 AO3/BIRID2, NID10 O325 Write/O326 Read; D/0603 R2 TOD DB2 | 요청·기억, Q와 별개. 명명 Set writer 미확보 |
| Allarm.MC_03_FAULT | DB3.DBX0.3 Bool | D/0657 R50 AO3/BIRID10, NID10 O401 Set/O404 Reset; D/0655 R10 TOD DB3 | 운전 미응답 래치. Q·요청 DB2와 같은 비트번호여도 별개 |
| Allarm.MC_03_TORQUE | DB3.DBX3.4 Bool | D/0657 R52 AO28/BIRID10, NID11 O409 Set/O413 Reset | 토크 래치. MC04/SS10 알람과 별개 |
| Tag_56 | %T53 Timer | D/0658 R48 AO53/SAD Timer, NID10 O398 Write/O399 Read | SD 타이머, S5T#2S. HMI 태그나 디지털 입력이 아님 |
| hours motors.MC_03_MIN | DB9.DBW88 Int | D/0615 R142 AO704/BIRID5; D/0614 R5 TOD DB9; NID23 O1289/O1291/O1292/O1297 | Add/Move 대상. 실제 저장 주기·완료시간 미검증 |
| hours motors.MC_03_HOUR | DB9.DBW90 Int | D/0615 R144 AO720/BIRID5; NID23 O1295, NID51 O2843 Write | Move1 및 Move0. 누적시간 총계라는 해석 금지 |

AO는 위 선언의 bit offset이다. Bool 주소와 Word 시작주소를 형식 및 DB 종속 선언을 통해 변환했다. offset 숫자만으로 다른 DB를 병합하지 않았다.

공통·타 설비 피연산자도 분리한다.

| 신호 | 선언·주소 | MC03에서의 사용 |
|---|---|---|
| ON / OFF | D/0602 R1 AO0 / D/0658 R46 AO1, SAD Memory → %M0.0 / %M0.1 | 모터/알람의 서로 다른 앞단 허가. 이름은 현재 참/거짓의 증거 아님 |
| Inputs.MC04 run | D/0604 R259 AO6/BIRID218→D/0603 Inputs DB13 → DB13.X0.6 | 0246 반전 접점. MC03 피드백과 다른 신호 |
| Flag.STANDBY_ON | D/0604 R11 AO60/BIRID2 → DB2.X7.4 | MC04 미응답 해제 분기의 반전 조건 |
| UNDER TESTING | D/0602 R4 AO45/SAD Memory → %M5.5 | 토크 해제 분기에만 반전으로 사용 |
| Flag.Maintenance_ON | D/0604 R3 AO61/BIRID2 → DB2.X7.5 | 0237에서 UNDER TESTING을 쓰는 공통 입력 |
| Flag.RESET_ALLARM | D/0657 R13 AO48/BIRID12→D/0655 Flag DB2 → DB2.X6.0 | 두 알람 Reset 요청. 실제 HMI 이벤트 결속 미확인 |
| Tag_47 / Tag_48 | D/0613 R1 AO13 / R284 AO17, SAD Timer → T13/T17 | 운전시간 및 시간기록 초기화의 공통 타이머 |

MC03 전용 인버터 속도 지령·아날로그 전류/속도 환산·엔코더 근거는 이번 고유 선언/FG23 경로에서 확보하지 못했다. FG23의 접촉기·보호기·QS·M05 회로를 기준으로 서술하며 MC04의 QW294 속도/전류 경로나 MC05 자료를 복제하지 않는다. 미확보를 현재 현장에 그런 부품이 없다는 결론으로 바꾸지 않는다.

### 2.2 원시 I→Inputs DB13의 Word 경로

D/0397 LAD1070/NID1, HMI Inputs:

| 대상 범위 | in 선언/배선 | Part와 out 배선 | 목적지 및 MC03 비트 |
|---|---|---|---|
| IW0 | D/0627 R3 Tag_178, Word/SAD Input AO0, O25→W23→P22.in | P22 Move, en=W21 rail; out1→W24→O26 | D/0629 R5 Word AO0/BIRID4 → DB13.DBW0. I0.5/MC03 run 및 타설비 I0.6/MC04 run 포함 |
| IW6 | D/0627 R13 Tag_171, Word/Input AO48, O45→W52→P42.in | P42 Move, en=W21 rail; out1→W54→O46 | D/0629 R14 Word AO48/BIRID4 → DB13.DBW6. I6.4/MC03 torque 포함 |

D/0628 DepDBBlock R4는 Inputs, TOD N13/CID638561979615757134다. D/0655 R247 및 D/0603 R218도 같은 DB13/CID이므로 원시 Word/목적지 Word/명명 Bool을 결속했다. 해당 두 Move에는 비트 반전이 없다. 각 Move의 `DisableENO=true`와 옆 Move로 이어지는 ENO는 원문 상태를 보존한다.

D/0030 Main LAD1613/NID19의 호출은 rail W31→Recipes Handler CRef21 →ENO W32→HMI CRef23 →ENO W33→HMI Output CRef25 →ENO W42→반전 Contact37 →W43→HMI Inputs CRef28.en이다. Contact37.operand=W44/O45, D/0692 R140 `Simulation(1)` AO1440/SAD Memory(%M180.0). 호출 블록은 D/0688 R120/124/128/135의 CodeBlock UID22/24/26/29와 D/0694 CRef121/125/129/136의 NID19로 대조했다.

따라서 전송은 상위 ENO와 NOT Simulation(1) 경계를 가진다. 현재 메모리값·온라인 호출·최종 DB13값은 미확정이다. D/0635 R14에는 Inputs.MC03 run의 별도 NID1/UID50 Write 선언도 남아 있어 ‘이 Word만 유일한 writer’라고 하지 않는다. 중지 대상의 해당 실행망을 동작 검증하거나 재개하지 않았다.

### 2.3 Q Word의 HMI 관찰용 복사

D/0401 LAD356/NID1의 P22 Move는 rail W21에 en, `Tag_280` O33/R24→W56.in, out1 W58→O34/R27이다. D/0632 R24는 Word, Output AO0(%QW0); D/0633 R27은 Word AO0/BIRID26; D/0064 R26 DepDBBlock Output는 TOD DB14다. 따라서 Q0.3을 포함하는 QW0→DB14.DBW0 복사가 있다. 이 경로는 Q를 읽고 DB14를 쓰므로 MC03 Q0.3을 덮어쓰는 명령 경로가 아니다. DB14.X0.3을 직접 MC03 HMI 화면·버튼 주소라고 확정할 태그/이벤트 자료는 없다. 현재 복사 시점은 §2.2의 HMI Output 호출/ENO 경계에 따른다.

### 2.4 HMI 명명 호출: 존재와 결속 미완료를 분리

D/0360은 검색 색인상 HMI의 `spare motor`, LAD1181이다. XML의 CRef UID23/RefId638, CodeBlock UID22/RefId1을 읽었다. 0623 FCBlock R1 `HMI Standard Motors`와 0624 BlockInterfaceInfo R638에는 여러 NID 호출이 반복된다. MC03 대상 원본 NID를 유일하게 확정하지 못했으므로 아래 핀을 실제 태그로 확정하지 않았다.

| 함수 핀 | 원본 Wire/ORef/RefId | 직접 확인·경계 |
|---|---|---|
| en | W21 Powerrail→CRef23.en | 직접 연결 |
| Ingresso_run | W24/O25/R711 | 실제 GlobalAccess 선언 결속 미확보 |
| Allarme1 | W28/O29/R59 | 동일 RID의 다른 블록 MC03_TORQUE를 오결속하면 안 됨 |
| Allarme2 | W30/O31/R60 | 실제 피연산자 미결속 |
| Allarme3 | W32/O33/R48 | 0626 FALSE 후보는 있으나 호출 NID 일치 확정 전 |
| Allarme4 | W34/O35/R48 | 위와 같음 |
| Allarme5 | W36/O37/R48 | 위와 같음 |
| Risposta | W42/CRef23→O43/R57 | 실제 Motors.Spare 멤버/DB주소 미결속 |
| Comulativo_allarmi | W46/CRef23→O47/R55 | 실제 목적지/DB주소 미결속 |

색인의 코드 텍스트는 Inputs.MC03 run, MC_03_FAULT, MC_03_TORQUE, FALSE 세 개, Motors.Spare.Risposta/Allarme_comulativo를 나열한다. 이는 탐색 단서이며 XML 선언·NID 일치가 없는 상태에서 ‘정확한 MC03 HMI 경로 검증’으로 승격하지 않는다.

공통 함수 D/0355 LAD331/NID1은 P23 Contact(0621 Local R16 Ingresso_run, O24/W22)→W25→P27 Coil(R17 Risposta, O28/W26), 그리고 Allarme1..5의 P33/P36/P39/P46/P30→OR P41.in1..5(W42/43/44/48/49)→W57→P59 Coil(R22 Comulativo_allarmi,O60/W58)다. Local 선언과 Global 인스턴스를 구분했다. 이 함수 수준 사실을 미결속 MC03 주소에 자동 적용하지 않는다.

S/hmi_plc_tags.csv(782 데이터행) 및 R/equipment-hmi.csv(230 데이터행)를 MC03/mc_03/spare motor/spare 및 DB2,X0.3으로 조회했지만 대응 행은 없었다. 조회 부재는 화면/쓰기 부재의 확정이 아니다. 원본 HMI 프로젝트·dde.cfg·화면 이벤트·태그 내보내기가 필요하다.

## 3. 제어 구조·호출·다른 쓰기

### 3.1 요청 해제와 Q0.3의 별도 Coil

D/0246 LAD1940/NID10의 앞단은 P343 Contact ON, operand W328/O319/D0602 R1, en rail W357이다. P343.out W344가 아래 네 경로로 분기한다.

| 분기 | 정확 배선·피연산자 | 해석·경계 |
|---|---|---|
| 해제1 | P345 Contact W329/O320/D0604 R57 MC_03_FAULT →W346→OR306.in1 | FAULT 참이면 해제 후보. STANDBY/UNDER TESTING으로 우회되는 분기 아님 |
| 해제2 | P347 반전 Contact W330/O321/R259 Inputs.MC04 run →W348→P349 반전 Contact W331/O322/R11 Flag.STANDBY_ON →W350→OR306.in2 | NOT MC04 run AND NOT STANDBY |
| 해제3 | P351 Contact W333/O323/R59 MC_03_TORQUE →W352→P353 반전 Contact W334/O324/D0602 R4 UNDER TESTING →W354→OR306.in3 | TORQUE AND NOT UNDER TESTING |
| 요청 Reset | OR306.out W336→P314 RCoil, operand W338/O325/D0604 R60 | DB2.X0.3 해제. Set 명령이 아님 |
| 출력 | W344→P355 Contact, operand W339/O326/R60 →W356→P318 Coil, operand W341/O327/D0602 R61 | 정적 출력 식 ON AND Flag.M_MC_03 → Q0.3 |

해제와 출력 Coil의 실행상 최신 값/스캔 내 우선순위는 TIA/현재 CPU로 검증하지 않았다. 해제 접점이 Q0.3 직렬에 직접 들어 있지 않다는 사실과, 요청 Reset을 통해 출력에 영향을 줄 수 있다는 사실을 구분한다.

### 3.2 UNDER TESTING과 유지보수는 원문 쓰기로 연결

D/0237 LAD1930/NID1: ON P47 (W42/O38/D0602 R1)→W48→Flag.Maintenance_ON P49 (W43/O39/D0604 R3)→W50→Coil34 및 Coil36. Coil34 operand=W44/O40/D0602 R4 UNDER TESTING(%M5.5), Coil36 operand=W45/O41/D0604 R6 Allarm.Maintenance_ON(DB3.X7.5)이다.

따라서 원문에는 `ON AND Flag.Maintenance_ON`에서 UNDER TESTING을 쓰는 경로가 있다. MC03 0246은 Allarm.Maintenance_ON을 읽는 MC04 망과 달리 UNDER TESTING을 읽는다. 두 변수의 주소·writer와 STANDBY(DB2.X7.4)를 구분한다. 현재 유지보수 허가나 안전 우회를 권고하는 설명이 아니다.

### 3.3 요청 Set 원천과 자동 순서의 미확보

고정 decoded IdentXmlPart 전체 명명 검색에서 Flag.M_MC_03는 D/0604 R60의 Reset/Read, D/0635 R15의 읽기로 발견되었다. MC04의 예열/생산/정지 Set/Reset 단계 값을 MC03에 복제하지 않았다. 이번 확보 원문으로 MC03의 정상 요청 Set 원천을 결속하지 못했다. 제공 HMI 태그 목록에도 요청 주소 대응이 없다.

이것은 ‘MC03는 절대 켜질 수 없음’의 증거가 아니다. 간접/포인터/블록 단위 쓰기, 외부 HMI/통신 쓰기, 원 프로젝트의 미추출 부분·현재 변경본은 별도다. 현재 설치 여부 및 운용 허가를 먼저 확인해야 한다.

### 3.4 명명 비트 외 startup Word 0쓰기

D/0147 LAD402/NID2: rail W210→ON Contact208, operand W184/O167/D0047 R1. out W209→Move138.en. D/0048 R54 `INT#0` O168→W185→Move138.in; Move138.out1→W186→O169. D/0563 R7는 Word AO0/BIRID6, D/0562 R6 Flag/TOD DB2다. 즉 **DB2.DBW0(byte0..1)에 0쓰기**이며 Flag.M_MC_03 DB2.X0.3을 포함한다.

D/0148 LAD403은 map의 NID가 null이다. 상수/목적지 선언들의 CS NID3 및 ON D0047 R1 NID3/O284로 결속했다. D0664의 다른 NID4/UID284 후보를 선택하지 않았다. rail W331→ON Contact329, operand W303/O284, out W330→Move250.en이다.

| 겹치는 명명 비트 | Move와 0입력 | Word 출력·선언 | 의미·경계 |
|---|---|---|---|
| DB3.X0.3 MC_03_FAULT | P250.in W304/O285/D0048 R54 | P250.out1 W305/O286, D0563 R24 Word AO0/BIRID23→D0562 Allarm DB3 | DB3.DBW0 byte0..1의 0쓰기 |
| DB3.X3.4 MC_03_TORQUE | P253.en=P250.eno/W306; in W307/O287/R54 | P253.out1 W308/O288, D0563 R26 Word AO16/BIRID23→DB3 | DB3.DBW2 byte2..3의 0쓰기. 앞 Move ENO 필요 |

0147의 전체 8 Word는 DB2 byte0..15, 0148의 전체9 Word는 DB3 byte0..17이다. 여기에 공통 RESET_ALLARM DB2.X6.0, STANDBY DB2.X7.4, Maintenance DB2.X7.5도 범위상 겹친다. 각 고유 비트의 Set/Reset만 열거하고 다른 쓰기를 빠뜨리면 안 된다.

startup only라는 검색 블록명과 파일 색인 순서만으로 실제 OB 이벤트·호출 시점·Warm/Cold/Retain·항상 실행·최종0을 확정하지 않았다. 이 XML들의 상위 시작 이벤트 결속과 ON 값은 미확정이다. Q0.3 자체를 DB2/DB3 Word가 직접 덮어쓰는 것도 아니다.

### 3.5 Main 호출 경계

| 원본 | 직접 호출 배선 | 의미·미확정 |
|---|---|---|
| D/0031 LAD1619/NID6 | ON Contact282(W280/O271/D0692 R52). out W283→Allarms1 CRef264.en; CodeBlock275/D0688 R58, CRef D0694 R59 | 알람 블록 호출은 ON 아래. 내부 MC03 앞단 OFF도 별도로 만족해야 함. 이름만으로 ON/OFF 상호배타·상수 가정 금지 |
| D/0549 LAD1620/NID7 | ON Contact350(W348/O335/D0692 R52), out W351→Motors1 CRef319.en(CodeBlock337/D0688 R67; D0694 R68) | 모터망 호출 경계. 현재 실제 스캔·최종값 미확인 |
| 같은 0549 | W351→time work motor CRef334.en, CodeBlock347/D0688 R82, D0694 R83 | 시간망 호출 경계. 저장 성공이나 실운전 검증 아님 |
| D/0030 LAD1613/NID19 | §2.2의 Recipes/HMI/HMI Output/HMI Inputs ENO 연쇄 | 입력 복사와 HMI 호출의 허가를 출력망과 구분 |

### 3.6 MC03 운전시간 및 초기화

D/0311 LAD1021/NID23:
- Tag_47 T13 P1316(operand W1299/O1287/D0613 R1)→W1317→102A7_SPARE5 I0.5 P1318(W1300/O1288/R140)→W1319. 그 선이 Add1270.en 및 Ge1277.pre로 분기한다.
- Add1270 Int: W1301/O1289 MC_03_MIN + W1302/O1290 상수1(D0616 R7) →out W1303/O1291 MC_03_MIN. 선언 D0615 R142.
- Ge1277: W1304/O1292 MC_03_MIN >= W1305/O1293 상수60(D0616 R8). out W1306→Move1280.en.
- Move1280: in W1308/O1294=상수1 →out1 W1309/O1295 MC_03_HOUR(D0615 R144). **기존 HOUR에 1을 더하는 Add가 아니다.**
- Move1280.eno W1310→Move1283.en; in W1311/O1296=0(D0616 R12) →out1 W1312/O1297 MC_03_MIN. eno W1313→SCoil1286, operand W1314/O1298 Flag_Aggiorna_DB(%M1.7,D0613 R13).

시간 기반 공통 원문 D/0019 LAD1056/NID58은 반전 Tag_47 Contact3120(W3118/O3115/R1)→W3121→SdCoil3112. value W3117/O3114/D0616 R335 `S5T#1M`, operand W3119/O3116/D0613 R1 T13이다. 정적 주기 의도는 확인되지만 실제 호출주기·기록 정확성을 검증하지 않았다.

D/0336 LAD1049/NID51은 Tag_48(T17) Contact2863 W2848/O2837/D0613 R284 →W2864→Move2822(RD01 HOUR=0). 그 ENO W2851→Move2825(RD01_FAN HOUR=0), 다시 ENO W2854→**Move2828**. MC03 입력은 W2855/O2842/D0616 R12=0, out1 W2856/O2843/D0615 R144→DB9.DBW90이다. MC03 HOUR 0쓰기에 앞선 두 Move ENO 연쇄가 존재한다. 다른 설비 HOUR를 MC03 소유로 세지 않았다.

T17 생성 경계 D/0341 LAD1055/NID57: ON P3147(W3133/O3124/R331)→W3148에서 두 가지. Flag_Aggiorna_DB P3149(W3134/O3125/R13)→W3150→SCoil3110 MEM2_0(W3136/O3126/R332,%M2.0). MEM2_0 P3151(W3137/O3127)→W3152→반전 Flag_Aggiorna_DB P3153(W3139/O3129)→W3154→SdCoil3118, value W3138/O3128/D0616 R334 S5T#5S, operand W3141/O3130/D0613 R284 T17. W3152의 다른 가지는 Tag_48 P3155(W3142/O3131)→W3156→RCoil3123 MEM2_0(W3144/O3132). ‘DB에 기록 후’라는 제목만으로 실제 외부 저장의 성공이나 운영기록 유실 없음은 증명하지 않는다.

## 4. 전기 전달 경로: 실제 PDF 페이지 검토

### 4.1 도면 페이지·개정

실제 렌더를 읽은 페이지는 아래 8쪽이다. FG 번호와 PDF 물리 페이지를 분리한다.

| 파일·FG / PDF | 직접 본 내용 | 개정/시점·제한 |
|---|---|---|
| Electrical_Rev2 FG8 / PDF9 | 8QF1→15KA1→15KA2→8WB1→8.3L1/L2/L3 | 27.05.2024, 별도 REV2 행 미확인. 본문440V/제목400V 상충 |
| 같은 FG10 / PDF11 | 24Vdc 10.7 및 10.9/10.6 공급 | 27.05.2024, 별도 REV2 행 미확인 |
| 같은 FG23 / PDF24 | SPARE M05·23QM1/KM1/QS1, XS7/8, E0.5, SS09/X1 52/53 | 27.05.2024, 별도 REV2 행 미확인 |
| 같은 FG116 / PDF117 | E0.5 FEEDBACK SPARE MOTOR, CPU515/MOD8/pin6 | 27.05.2024, 별도 REV2 행 미확인 |
| 같은 FG122 / PDF123 | E6.4 SS09, CPU515/MOD9/pin25 | REV2 17.03.2025, 기본 27.05.2024 |
| 같은 FG136 / PDF137 | A0.3 SPARE MOTOR COMMAND, CPU515/MOD14/pin4 | REV2 17.03.2025, 기본 27.05.2024 |
| PID_1684n002I / PDF1 | 공정 태그·MC04/VS01 및 MC03 명시 대응 미확보 | Rev.I 도면, 현재 준공·현장 아님 |
| Electrical_Can_Decoating_20241118 / PDF52 | CABLE SCHEDULE(2), row2_5 검은 띠 | 24.11.11 first draft design, 유효 M05케이블 경로 미확보 |

### 4.2 전원에서 M05까지

FG8/PDF9의 6.2L1/L2/L3 공급→8QF1 주접점(1–2/3–4/5–6)→8.1L1/L2/L3→15KA1 주접점→8.2L1/L2/L3→15KA2 주접점→8WB1 20×5 busbar→8.3L1/L2/L3(22/0 교차참조). FG23/PDF24는 22/9에서 이 8.3L1/L2/L3를 받아 26/0으로 이어 보낸다. 공유 공급을 MC03 전용 차단기·전용 안전회로로 분류하지 않는다. FG22의 중간 통과와 15KA1/2 코일 제어는 이번에 완전 추적하지 않았다.

FG23의 분기는 8.3L1/L2/L3→23QM1(1–2/3–4/5–6)→23KM1 주접점(1–2/3–4/5–6)→23U1/23V1/23W1 도체→XM:23U1/23V1/23W1 단자→23QS1(1–2/3–4/5–6)→M05 U/V/W 및 PE다. BLACK FS17 2.5mm² 표기가 있다. 이는 도면의 도체 규격이며 완성 케이블의 검증된 번호·전체 심수·현장 길이가 아니다.

인쇄 M05 4kW/7.6A, 23QM1 7–10A는 참고 도면 수치다. 현행 명판·제조사 형식·열동 설정값·정비 토크·안전한계나 추천 조정값으로 채우지 않는다.

### 4.3 Q0.3에서 접촉기 코일까지

FG136/PDF137: CPU515/MOD14, A0.3 pin4, 교차참조23/4 →FG23/PDF24의 A0.3(136/1) →XS7→23QS1 보조접점→XS8→23QM1 보조접점→23KM1 A1. 23KM1 A2→−0Vdc10.6. FG23의 23QS1/23QM1 보조접점 자체 숫자는 인쇄로 확정하지 못했으므로 일반 접점번호를 만들어 넣지 않았다.

모듈 공급 FG136: +24Vdc10.9(115/9→137/0)→X21 3028/5×20 4A F→선136.1→단자9, 0V10.6→단자10. FG10/PDF11에서10.9는 10GD1→10QF3→10.8→14KA3→10.5→14KA7 이후의 ‘SUPPLY OUTPUTS PLC UNDER EMERGENCY’ 선으로 보인다. 14KA3/7 안전기능/접점 정상상태/현장 등급은 확인하지 않았다.

Q0.3=1이라는 소프트웨어 관찰만으로 QS1/QM1 접점, 모듈 전원, 코일·주접점·모터 회전이 정상이라고 결론내리지 않는다. 현장 조작·활선측정·보호 우회는 이번 작업 범위에 없다.

### 4.4 접촉기 응답 경로

FG23/PDF24 +24Vdc10.7 →23KM1 보조접점13–14→E0.5(116/5). FG116/PDF117 E0.5의23/6 교차참조→CPU515/MOD8/pin6, FEEDBACK SPARE MOTOR. PLC 주소/선언은 §2.1의 I0.5 및 §2.2 Word전송이다.

이 피드백은 도면상 접촉기 보조접점이다. 회전·속도·벨트 움직임·모터 실제 토크를 직접 측정하는 센서로 바꾸지 않는다. 단자·접점 고착이나 실제 결선 여부는 현장 확인이 필요하다.

### 4.5 SS09 토크 경로와 인접 SPARE 오독 방지

FG23/PDF24 +24Vdc10.7→X1:52, 5×20 2A F→선23.2→SS09 접점11–12→X1:53→E6.4(122/5). FG122/PDF123 E6.4(23/7)→CPU515/MOD9/pin25, LIMIT SWITCH SS-09다. 도면의 11–12 접점 심벌을 실제 정상극성·기계 토크 한계값 확인으로 승격하지 않는다.

FG122의 점선 SPARE 박스는 E6.3(SSL01)와 E6.5/E6.6(SS10/SS11)을 둘러싸며 **E6.4/SS09에는 그 박스가 없다**. 그렇더라도 FG23 전체 제목은 SPARE다. ‘SS09 입력 페이지에서 SPARE박스가 없으니 현재 설치 확정’ 또는 ‘MC04/MC05의 SPARE박스를 MC03에 복제’하지 않는다.

### 4.6 시공 케이블 목록의 시각/텍스트 차이

S/can-decoating-page-text.json과 PDF의 텍스트 추출에는 PDF52 row2_5 `CR – M05 SPARE GAC CV 4`가 남아 있다. 실제 PDF52 렌더에서 row2_5는 번호 칸을 제외하고 검은 띠로 덮여 있으며 해당 문자열은 사람이 읽는 도면에 표시되지 않는다. 케이블 번호·FROM 장치 세부·사이즈·경로·길이의 유효한 현행 행을 확보하지 못했다.

따라서 위 텍스트를 채택해 ‘MC03 케이블 CV4/현재 연결’이라고 확정하지 않는다. 검은 처리의 의도가 삭제·취소·가림 중 무엇인지는 개정 승인 자료 없이 판단하지 않는다. 원문과 파생 텍스트 차이를 보존하고 승인 케이블표/양끝 태그 사진을 요청 자료로 남긴다.

## 5. 알람·Reset·복구

### 5.1 MC_03_FAULT: OFF 아래의 2초 운전 미응답 래치

D/0426 LAD1789/NID10:

| 동작 | 직접 Part/Wire/선언 | 정적 식·경계 |
|---|---|---|
| 공통 허가 | rail W431→P419 Contact, operand W405/O395/D0658 R46 OFF | OFF(%M0.1). ON으로 바꿔 읽지 않음 |
| SD 타이머 | P419.out W420→P421 StartSpare(W406/O396/R47)→W422→반전 P432 Inputs.MC03 run(W435/O433/D0657 R272)→W21→P383 SdCoil | OFF AND Q0.3 AND NOT DB13.X0.5 |
| 시간·타이머 | P383.value W407/O397/D0656 R28 S5T#2S, operand W408/O398/D0658 R48 Tag_56 T53 | S5Time 저장 V512, SV S5T_x0023_2S. 값512초로 해석 금지 |
| FAULT Set | W422→P423 Tag_56(W409/O399)→W424→반전 P425 MC03run(W410/O400)→W426→P389 SCoil; operand W412/O401/D0657 R50 | OFF AND Q0.3 AND T53 AND NOT MC03run |
| FAULT Reset | W420→P427 RESET_ALLARM(W414/O402/D0657 R13)→W428→P429 FAULT(W415/O403/R50)→W430→P394 RCoil; operand W417/O404/R50 | OFF AND RESET_ALLARM AND FAULT. 이 Reset 경로에 RUN 정상화 접점 없음 |

Main Allarms1 호출은 §3.5 ON 조건을 갖고, 내부는 OFF 조건이다. 두 값을 현재 CPU에서 확인하지 않았고 해당 이름을 상수로 가정하지 않았다. 타이머 Reset/Retain·호출 중단 시 동작은 TIA 실행으로 확인하지 않았다.

### 5.2 MC_03_TORQUE: 반전 입력 Set, 정극성 입력 Reset

D/0427 LAD1790/NID11:
- rail W434→P424 OFF(Contact operand W414/O407/D0658 R46)→W425.
- Set 가지: 반전 P426 Inputs.MC03 torque(W415/O408/D0657 R273)→W427→P400 SCoil MC_03_TORQUE(W417/O409/R52). 즉 OFF AND NOT torque.
- Reset 가지: P428 RESET_ALLARM(W418/O410/R13)→W429→P430 torque(W419/O411/R273)→W431→P432 MC_03_TORQUE(W420/O412/R52)→W433→P406 RCoil(W422/O413/R52). 즉 OFF AND RESET_ALLARM AND torque AND 기존 TORQUE.
- 이 망에는 MC03 전용 지연 타이머가 없다. 2초 FAULT 타이머를 TORQUE에도 복제하지 않는다. ‘정상은1’이라는 논리 의도를 현재 배선·센서 정상극성의 검증값으로 쓰지 않는다.

### 5.3 영향·HMI·재기동 구분

FAULT는 §3.1의 독립 해제 가지, TORQUE는 NOT UNDER TESTING이 있는 가지로 DB2.X0.3 요청을 Reset한다. 알람 비트 해제는 요청 Set/재기동 허가가 아니다. MC03 Set 원천과 실제 HMI Reset 이벤트는 미결속이다. 0360 HMI 표시 결속도 미완료이므로 실제 경보 문구·색상·누적표시를 만들어 넣지 않는다.

복구 판단에는 원인 정상화, raw/DB13 값, Q/접촉기 피드백, 래치 Reset 후 상태, 재요청 방법·승인 및 실제 기계 결과의 각각의 증거가 필요하다. 이번 초안은 해당 시험을 수행하지 않았다. OFF/UNDER TESTING/STANDBY/보호 접점 강제나 변경을 복구 방법으로 제시하지 않는다.

## 6. 증상별 관찰·수리 초안

다음은 필요한 자료와 비교 순서다. 실제 조치 완료, 활선 측정 허가, 운전·보호 시험 지시가 아니다. 현장 작업은 해당 설비의 승인 절차와 자격을 갖춘 담당자의 안전조치하에 별도로 결정한다.

| 증상 | 먼저 보존할 관찰·위치 | 비교·원인 배제 | 다음 자료·복구 판단 |
|---|---|---|---|
| MC03라는 설비를 찾을 수 없음 | 현장 태그/모터명판/반 위치 및 사진 시각, FG23 M05/SPARE와 PID1 | MC05·MC04와 숫자/이름만으로 동일시하지 않음. PDF52 검은 행은 현행 설치 근거 아님 | 설치/철거/전용 승인 변경서, 단자·케이블 양끝, 현재 도면. 식별 전 운전판정 보류 |
| 요청이 즉시 해제됨 | DB2.X0.3, ON, DB3.X0.3/X3.4, DB13.X0.6, DB2.X7.4, M5.5의 같은 시점 | 0246 OR3개 분기를 각각 비교. STANDBY는 MC04분기, UNDER TESTING은 토크분기에만 영향 | 현재 프로젝트 read-only cross-reference/스캔 관찰. 강제값으로 해제 원인을 덮지 않음 |
| 요청이 있는데 Q0.3이 안 켜짐 | 실제 Set 원천, Motors1 호출, ON, DB2.X0.3 및 startup 이벤트 | 0246 출력 Coil과 0147 DBW0쓰기 경계 비교. HMI 주소만으로 작동 명령 유효 판정 금지 | HMI 이벤트/통신 writer·현재 프로젝트, 호출/최종 writer 증거 |
| Q0.3이 켜졌는데 접촉기/모터 응답 없음 | 승인된 관찰 기록의 모듈표시·QS/QM 상태·전원 상태·I0.5, 도면 위치 | FG136 pin4→XS7/8→QS/QM 보조접점→KM A1/A2; 모터 동력경로와 피드백 별도 | 현행 결선/부품 명판·정비 확인. 안전한 점검 후 실제 회전 결과까지 확인해야 복구 |
| I0.5와 화면/알람이 다름 | raw I0.5, DB13.X0.5, DB14.X0.3, HMI 실제 태그·시간 | 0397 Word복사/0030 호출·ENO·NOT Simulation 경계, 0401 Q관찰복사, 0360 미결속 구분 | HMI 프로젝트·온라인 연결·writer 대조. 화면만으로 센서/PLC 고장 단정 금지 |
| MC03 FAULT가 기대와 다름 | ON/OFF·Q0.3·DB13.X0.5·T53·DB3.X0.3·Reset을 같은 시간축으로 보존 | 0426 OFF 및 2초SD 식, Reset에 원인정상화 접점 없음, startup Word쓰기 비교 | 현재 CPU 프로젝트 동일성·래치/타이머 증거. 해제만으로 정상복구 판정 금지 |
| TORQUE가 해제되지 않거나 표시 없음 | SS09/원시I6.4/DB13.X6.4/DB3.X3.4/Reset/OFF 및 M5.5 | 0427 Set반전/Reset정극성, 0246 출력영향과 HMI미결속을 별도 대조 | SS09 부품/기계상태·승인극성·양끝도면. 안전한 원인해소와 재요청 후 결과 필요 |
| 운전시간이 누적 안 되거나 사라짐 | I0.5,T13,DB9.W88/W90,M1.7,M2.0,T17, 저장 시각 | 0311 HOUR Move1, 0336 선행 ENO 및 Move0, 0341 저장제목/실제저장 증거 구분 | 현행 데이터 기록 구조/확정 저장 로그. 원문을 HOUR+1로 가정해 수리하지 않음 |

관찰 기록 최소 필드: 관찰자·현장 자격/승인·시각과 시간대·태그/위치·실제 값/단위·수집장치·CPU/프로젝트 근거·비교 도면 개정·원인 배제·조치 승인·전후 결과. 미확인 값은 빈칸/미확인으로 보존하고 0으로 채우지 않는다. 실제 운영 기록을 이 조사 저장소에 복제하지 않았다.

## 7. 완료 기준·인계·검증

### 7.1 반드시 남기는 미확정 자료

1. 현재 MC03/M05/SS09의 설치·철거·예비 유지·전용 여부, 실물 태그/명판/단자 양끝 사진 및 승인 변경서.
2. 현행 모터/접촉기/보호기/QS/SS09 모델·설정·정상극성·결선·접점 번호, 유효 케이블 번호/사양/길이. 도면의 4kW/7.6A/7–10A를 설정값으로 복사하지 않음.
3. MC03 요청 Set 원천 및 원본 HMI 프로젝트/dde.cfg/화면 이벤트. 0360의 NID와 8피연산자 실제 GlobalAccess 결속, 표시문구/주소.
4. 현재 CPU와 고정 백업의 동일성, Main 및 startup 상위 이벤트, Retain/Warm/Cold, ON/OFF 실값과 다른 writer·간접쓰기·최종 우선순위.
5. FAULT/TORQUE 실제 발생·원인해소·Reset·재요청·기계 회전의 증거. TIA컴파일/현장검증으로 문서검사 상태를 대체하지 않음.
6. MC03 운전시간의 저장프로그램/확정 저장 로그. `recording the data in the db` 제목은 외부 저장 완료 근거가 아님.

### 7.2 네 기능 적용과 기록 보존

| 기능 | 적용 판단 | 구현·검증 상태 |
|---|---|---|
| 도면·래더 나란히 비교 | FG23/116/122/136와 LAD1940/1789/1790 및 1070의 비교 근거 확보 | 이 초안에서 UI 구현·링크 동작 검증 안 함 |
| 백업 미리보기/선택 복원 | MC03 지원 여부와 저장키 확인 필요 | 실제 사용자 기록/합성 QA 기록 미작성, 저장·재읽기·재열기 미검증 |
| 기록 전후 비교 | 위 관찰 필드와 원본/현재값 분리 필요 | 기능 구현·동시성/Quota/구형JSON/미지필드 보존 미검증 |
| 관찰 보고서/PDF | 자료 시점·미확정·원본 위치를 포함하는 설계 가능 | 보고서 생성·렌더·내용변경 검증 미수행 |

기존 note/repair_observation/다른 설비/초안/미지필드/저장키를 변경하지 않았다. generated_with/saved_with나 이 문서의 해시는 관찰 당시 CPU 상태의 증명이 아니다.

### 7.3 수행과 미수행

- 고정 HEAD/clean 상태 확인, 표준·원본 대장·원본 XML 지정 경로·선언/주소·PDF 실제 렌더 대조를 수행했다.
- 읽기 전용 preflight exit0, inventory_matches=true. source_byte_changes는 기존 requirements-audit.json/all-in-one-data.json 두 파일이며, 이 clone의 VERSION/최신 작업 기록에는 v1.12.0 통합 이력이 있다. 기존 대장 대비 바이트차이와 대장 동일성을 분리하며 이 조사에서 그 파일은 변경하지 않았다.
- 의미 검토 단위: **17개 FlgNet의 아래 지정 경로**. 그중 D/0360은 인터페이스 핀만 확인했고 MC03 실제 피연산자 결속은 미완료다. 부분 경로 검토를 네트워크 전체·전체 프로그램 실행 검증으로 세지 않는다. 8개 PDF페이지의 실제 시각 검토를 별도로 수행했다.
- 원본 해시 개수는 아래 manifest의 바이트 보존 범위다. 해시만 기록한 ZAP/PLF를 의미 검토 완료에 합산하지 않는다. 자동 후보 추출의 전체 선언 수 역시 의미 검토 수가 아니다.
- 별도 독립 검토, BC01/기존완료설비 회귀, 프로그램 정적검사 전체, PC/모바일 UI/기록·패키지·배포 검사는 이번 조사범위에서 미실행이다. 매뉴얼 생성기·시뮬레이터/TIA/현장 실행은 하지 않았다.

| 상태 | 결과 | 경계 |
|---|---|---|
| documentation | draft_ready_with_gaps | MC03 고유 7영역 조사 초안. 통합·문서 최종 승인 아님 |
| static_review | scoped_source_review_done | 지정 XML/선언·Word·PDF 검토. 독립 검토는 pending |
| ui_records | not_run | MC03 화면·저장·복원/보존 기능 미검증 |
| publication | not_published | 배포·버전·공통 코드 변경 없음 |
| tia_compile | not_performed | 프로젝트/TIA 실행 안 함 |
| live_cpu | not_performed | 현재 CPU/값·호출·쓰기순서 미확인 |
| field_recovery | not_performed | 설치·측정·복구·재기동 미수행 |

### 7.4 독립 검토자가 우선 확인할 10곳

1. 0246 OR306의3가지와 P314 Reset/P318 Coil. MC04 run을 MC03로 잘못 치환하지 않았는지.
2. 0426/0427의 OFF 및 상위0031 ON이 동시에 존재하는 사실과 현재값 미확정.
3. T53 SD/S5T#2S, FAULT Reset 경로에 RUN 정상화가 없고 TORQUE Reset에는 입력정극성이 있는 차이.
4. 0397 IW0/IW6→DB13,0030 NOT Simulation 호출 경계와 alternate writer 선언의 한계.
5. 0147 DB2.DBW0,0148 DB3.DBW0/2가 요청·두 알람과 겹치는지. NID3 후보를 다른 블록 RID로 오결속하지 않았는지.
6. 0360 핀8개 미결속 및 HMI CSV 대응0행을 HMI 부재/주소 확정으로 승격하지 않았는지.
7. FG23 SPARE/M05와 FG116 E0.5·FG122 E6.4·FG136 A0.3의 핀6/25/4 및 교차참조.
8. FG122 SPARE 점선이 SS09 아닌 인접 입력을 감싸는지, FG23/116 개정 공란과 FG122/136 Rev2를 구분했는지.
9. 시공PDF52 row2_5 검은 띠와 텍스트층 M05 잔존의 차이, 유효한 케이블 행으로 채택하지 않은 점.
10. 0311 HOUR Move1,0336 MC03 Move0 앞의 두 ENO,0341의 제목과 저장 성공 미검증 구분.

다음 조치: 이 초안의 고유 경로를 독립 대조한 뒤 승인 범위에서 취합한다. 현장 미확정은 그대로 인계한다. MC03를 MC04/MC05에 합치거나 로컬2차133을 재개하는 지시가 아니다.

## 부록 A. 원본 위치·해시·Git blob 대장

모든 상대경로는 고정 source-mv06의 Git 루트 기준이다. SHA-256은 실제 파일 바이트, Git blob은 해당 HEAD의 경로 객체다. `git_blob_matches_bytes`는 Git blob 식별과 파일 바이트가 일치함을 뜻한다. 내용의 해석·실행·현장 적합성은 별도다. 세부 JSON은 `extracts/MC03/source-hashes.json`, 선언과 선 연결은 같은 디렉터리의 지정 trace/refs 파일에 보관한다.

### A.1 의미 검토 범위

| FlgNet | LAD / NID | 검토 범위 |
|---|---|---|
| D/0019 | 1056 / 58 | T13 1분 SD의 접점·상수·타이머 |
| D/0030 | 1613 / 19 | HMI/Output/Inputs 호출 ENO·반전 허가 |
| D/0031 | 1619 / 6 | Allarms1 호출 허가 |
| D/0147 | 402 / 2 | DB2.DBW0 및 전체 Word범위 |
| D/0148 | 403 / 3 (직접 결속) | DB3.DBW0/2 및 전체 Word범위; NID3 재결속 |
| D/0237 | 1930 / 1 | UNDER TESTING writer |
| D/0246 | 1940 / 10 | MC03 Reset OR3개 및 Q Coil |
| D/0311 | 1021 / 23 | MC03 MIN/HOUR Move·Add |
| D/0336 | 1049 / 51 | MC03 HOUR Move0의 선행 ENO |
| D/0341 | 1055 / 57 | T17 생성/기억 Reset |
| D/0355 | 331 / 1 | 공통 HMI Local 입출력·OR |
| D/0360 | 1181 / 미확정 | 호출 핀8개만; 실제MC03 피연산자 미결속 |
| D/0397 | 1070 / 1 | IW0/IW6→DB13의 지정2 Move |
| D/0401 | 356 / 1 | QW0→DB14의 지정1 Move |
| D/0426 | 1789 / 10 | MC03 FAULT SD/Set/Reset |
| D/0427 | 1790 / 11 | MC03 TORQUE Set/Reset |
| D/0549 | 1620 / 7 | Motors1/timework 호출 허가 |

### A.2 바이트 해시 61파일

17개 FlgNet 지정 경로, 선언파일 32개의 관련 선언 조회, 실제 렌더 8쪽과 해시 대상 61파일은 서로 다른 집계다. 0360의 미결속8개는 해결 완료에 합산하지 않는다. ZAP/PLF 2파일은 출처 바이트만 확인했다.

| 원본 경로 | SHA-256 | Git blob | 검토 범위 |
|---|---|---|---|
| `all-in-one/sources/decoded-original/0019-FlgNet.xml` | `a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5` | `f78cfdbf5e717304114660ffbd3bb42cbed6d79d` | scoped XML path |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | scoped XML path |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | `653d27572de6beedcf3eb6c95702bb119a8b567f` | scoped XML path |
| `all-in-one/sources/decoded-original/0147-FlgNet.xml` | `386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c` | `0027890eca158e714dd6260dc920a5d3aa83319b` | scoped XML path |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` | `3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3` | scoped XML path |
| `all-in-one/sources/decoded-original/0237-FlgNet.xml` | `ad3721660c2f357e76c1a351f7898691271f35c341efe775e5780d749b2c4aa0` | `c97f914bb78760dd6fd42a46d3596983beb352f4` | scoped XML path |
| `all-in-one/sources/decoded-original/0246-FlgNet.xml` | `2b1bf0644447f15640214b451281aa3fa5389505936f2a6a1078a9508dfc9f04` | `c21879f1cdca1a8d47938a89ee9ea6a25c4f82bc` | scoped XML path |
| `all-in-one/sources/decoded-original/0311-FlgNet.xml` | `9f5300f71fb94b8f68c9056aa72cbd001a9f472601a8709409bf011e4be72a8f` | `06dc57a339737347f296253d24f683c0aa988064` | scoped XML path |
| `all-in-one/sources/decoded-original/0336-FlgNet.xml` | `1be4f76dba11e6cceea057743c8b15b8a4bea4edfe87c19ef0581d7b65ffe56a` | `3bb3ae34dc100f7a9483cf8bf7702c01e080371d` | scoped XML path |
| `all-in-one/sources/decoded-original/0341-FlgNet.xml` | `e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96` | `45dbda06a692b21380a52207a22094b2e0a9c5a3` | scoped XML path |
| `all-in-one/sources/decoded-original/0355-FlgNet.xml` | `73592d33f8b3a71effeb36f25427c76e931485e7ce31f5c81f144ddae83c4247` | `54f7a267c9b44c325fd5af31ea78736049d8b1ef` | scoped XML path |
| `all-in-one/sources/decoded-original/0360-FlgNet.xml` | `a2297a80a92fe385ff252f001f030a7fbde13510bdffaf156a9a6ed60733f31d` | `0985905a99514ab5b0bf77225735818775201d78` | scoped XML path; incomplete actual operand binding |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | scoped XML path |
| `all-in-one/sources/decoded-original/0401-FlgNet.xml` | `60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae` | `aadefbd35d305dd4a1146bf383b988a903802bf4` | scoped XML path |
| `all-in-one/sources/decoded-original/0426-FlgNet.xml` | `8b03ce9bd6d85c9e0861abd5401f4cb61b199e06a1705fc8ecc9088ed39e5688` | `b2b036e5c9c59ab07c7045dff97a63e7d181615b` | scoped XML path |
| `all-in-one/sources/decoded-original/0427-FlgNet.xml` | `32e92066f26d542098b33dfaa7cc228f373bd3dcc331751ae0ce0ffdd8731816` | `cce340234f9ab69f06d05ec8708335e9be0aee6f` | scoped XML path |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` | `985b5310b43b1015b5dee286aa0e42800564b94b` | scoped XML path |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0064-IdentXmlPart.xml` | `ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d` | `300d74239868f4f4595d4d5bbb848b4b58bbae76` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0555-IdentXmlPart.xml` | `46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6` | `9a915a8b9a260b48402df151c1fe0bbcb2f4ea1c` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0556-IdentXmlPart.xml` | `065d71114e26c93af180265e0e6d59d2a190af1f2f0581c5265e7f4f67d6e23f` | `15ae569ff390ef5c791b0f76d96bd86d5ec6b938` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | `3a92b304baf4dbf6147e944d9778d2da11285cb1` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0613-IdentXmlPart.xml` | `09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb` | `c9d19a48e947098914f4d2de3348c05b4f6d37e8` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0614-IdentXmlPart.xml` | `c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294` | `da0485aa033700f08c8695d30b93ebd2d377d6c7` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0615-IdentXmlPart.xml` | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` | `49eb86fe01feb83de8c0864b21493d305aff8b20` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0616-IdentXmlPart.xml` | `650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d` | `9f7fdd5f93ac149c139a054ebb34f63c632ef7fd` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0621-IdentXmlPart.xml` | `a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee` | `844516839e55f8bf231a18630e010b912190664e` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` | `13b3af0459c8e6069bb9b2f1b16454bf479e08dc` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` | `02511fea47fc47981c101bba49dc40adde1cdcc3` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0626-IdentXmlPart.xml` | `a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b` | `e0fc80d0c20f4db3eea31d35f578a2fa3c09f8e7` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0632-IdentXmlPart.xml` | `fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9` | `600935fa8d394c0d247ea20040d5dfff4f05b500` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0633-IdentXmlPart.xml` | `9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc` | `a1ab5ee12addbc92d04c9950d4437e2b564d6b5c` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | `83b60b9de4541a3ffa6ee0db98205a372b525665` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` | `9bfb9842e55901bab9a71d1ac03158467dfbb1bc` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | `e625f3d8999c7be7d88c50eab0d93107117b58ec` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` | `de9a12a6be87466ef1bf05df71c54580c556a827` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | scoped declaration lookup |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` | scoped declaration lookup |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | PDF visual/text scoped review |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | PDF visual/text scoped review |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | PDF visual/text scoped review |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | catalog or extraction lookup |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | catalog or extraction lookup |
| `all-in-one/registers/plc-symbols.csv` | `a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f` | `cbc576c5d6e47498a3865304a1c23de9b4641d9f` | catalog or extraction lookup |
| `all-in-one/registers/equipment-hmi.csv` | `2cdce600aa0138cc5025022e57d9d61a948afb237f70c70e2d11e8300e73286a` | `aca60d300d26fd2bccd6d3970822c3aed2ecdb87` | catalog or extraction lookup |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | catalog or extraction lookup |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | catalog or extraction lookup |
| `all-in-one/sources/can-decoating-page-text.json` | `d3b4c14945dd00f79c58ebab0cb8991c422dd1670e95e24d10779bd9e9d99bba` | `2bebec2c719fa57ed6c9f8d4e541e8848dc0d732` | catalog or extraction lookup |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` | provenance bytes only; no project execution/review |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` | provenance bytes only; no project execution/review |


## 전달 전 핵심 근거 제한 대조
2026-10-11 원본의 고유 허가/요청쓰기 Part와 선언을 표본 재확인하고 해당 모터 전기도면 실제 렌더의 SPARE·구동·응답·토크 끝점을 재확인했다. 인용 원본 SHA256을 모두 재계산하여 일치했다. 전체 원본 의미 검토, 현재 CPU·설치·현장복구·통합·게시 검증을 뜻하지 않는다. 미결속·미확정은 유지한다.
