# SC11 BF02 분진 스크루 원본 조사 초안

SC11은 원본 P&ID의 BF02 하부 분진 스크루 M35와 대응하며, 배출부에는 별도 VR05/M39가 그려져 있다. 전기 도면은 58KM1 직접기동·Q4.1 명령·I5.1 접촉기 응답을 보인다. PLC는 SC11 고장 또는 VR05 처리 운전응답 부재로 요청을 Reset하며, 출력 명령 후 SC11 처리 응답이 없으면 Tag_73(%T82)의 S5T#2S 감시로 고장을 Set한다. SC11 응답은 BF02 세정허가·공유 FN04 예고장에도 사용되지만, 이 기능들의 소유를 SC11로 병합하지 않는다.

이 문서는 작업3번 세 번째 5개 묶음의 SC11 자체 cloud 조사 초안이다. 로컬 2차133 통합, 매뉴얼 구현·게시, 현재 CPU나 실물·복구의 완료 증명이 아니다. 시뮬레이터 작성·수정·생성·실행·행동 시험, PLC·보호값·SEJIN 운영자료 변경을 하지 않았다.

## 작업 기준과 보존

- 표준: GME-STD-1.0.0. 저장소 AGENTS.md, gme-equipment-rollout 스킬, WORK-STANDARD.md 및 WORK-ITEM-TEMPLATE.md 적용.
- catalog_id SC11, 이름 BF02 분진 스크루, motor, 집진·석회, parent_id 없음, depth0, 별칭 없음, priority_key 없음. BF02와의 공정 관계는 부모 대장 필드가 아니다.
- 고정 읽기 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, 프로그램 v1.12.0. 착수 시 Git 변경 없음.
- 대장: INVENTORY.json catalog[101] 및 equipment.json[47]. phase2/planned, 기존 baseline, 별도 원본 조사 전 완료로 세지 않는다. TASK3-BATCH03-SCOPE.json에서 우선18 중복·제외90·부모범위 보류7에 속하지 않는 신규 조사대상으로 확인되었다.
- 읽기 전용 preflight 종료0, inventory_matches=true. 248 ID·우선23·우선대응18·제외90·하위보류7·phase2 133은 그대로 유지한다. source_byte_changes는 requirements-audit.json 및 all-in-one-data.json의 기존 스냅샷 대비 바이트 차이이며 대장 필드 불일치는 아니다. 대장을 고치지 않았다.
- SC01 초안은 구조 참고만 사용했다. 아래 주소·UID·RID·상수·단자·PDF 페이지·개정은 SC11 고유 원본에서 재대조했다.
- 작성일: 2026-10-11 UTC. 작성자 SC11 조사 작업자. 실제 실행 모델·추론 수준의 런타임 관측 근거는 미확인. 핵심 근거 제한 대조 완료; 사용자 독립 검토 대기.
- 작성 범위: `drafts/SC11-DOTS-DRAFT.md`, `extracts/SC11/`만. 공용 선언 파일, 공통 코드·버전·대장·배포·운영기록 및 고정 원본을 수정하지 않았다.
- 아래 원본 경로는 달리 쓰지 않으면 고정 저장소 `all-in-one/` 기준이다. 해시 목록은 부록 및 `extracts/SC11/source-sha256.json`에 있다. 해시 일치 개수와 의미 검토 범위는 별도로 기록한다.

## 7영역 적용표

| 영역 | 상태 | 조사 근거 | 남은 경계 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | SC11/M35, BF02 및 VR05/M39, 대장·P&ID·자료 판본 | 현재 명판·설치 동일성·준공 개정 |
| I/O·HMI | 적용, 일부 근거 미확보 | I5.1/Q4.1, DB2/3/9/13, HMI3행, Word 전달 | HMI4개 이름 결속·버튼 이벤트·현행 주소 |
| 제어 구조 | 적용 | 요청 Reset/자동 Set, startup Word 덮어쓰기, 원시/처리/출력 전달, BF02·FN04 경계 | 현재 호출·스캔·다른 외부 Writer·DB 유지 |
| 전기 전달 경로 | 적용 | FG58/121/140/253, 실제 PDF59/122/141/256, 시공47/52 | 현장 단자·심선·정상극성·장치 실물·보호 설정 |
| 알람·복구 | 적용 | SC_11_FAULT 2초 Set/Reset, 공유 FN04 90분 | 실제 표시·원인 제거·재요청·복구 이력 |
| 증상별 수리 | 적용, 관찰 계획 | 요청/출력/접촉기/원시/처리/HMI 및 세정 경계별 비교 | 현장 관찰·조치·복구 수행 없음 |
| 완료 기준 | 적용 | 출처·누락·검토 상태·후속 수집 목록 | UI/기록/게시/TIA/CPU/현장 별도 |

## 1 설비와 소유 경계

1. equipment.json SC11행은 `BF02 분진 스크루`, FG58, parent 빈값이다. P&ID `1684n002` 판I p1에서 BF-02 하부 SC-11/M35, 배출부 VR-05/M39가 별개로 그려져 있다. SC11은 3 kW 440 V, VR05는 0.55 kW 440 V 표기다. 이는 설계 자료의 표기이며 현재 설치전력·공급전압 측정값이 아니다.
2. Electrical_Rev2.pdf FG58/PDF59에는 `FILTER DUST SCREW SC-11`, M35, 3 kW/5.8 A 및 3상 440 V 60 Hz가 있다. 확인한 직접 회로·태그에서는 SC11 전용 인버터, 속도설정, 엔코더, 아날로그 전류를 식별하지 못했다. 이 직접기동 문서 경로에는 가변속/PID가 비해당이지만 현장에 추가 장치가 전혀 없다고 단정하지 않는다.
3. VR05 처리응답은 SC11 요청 Reset의 조건이다. VR05 출력·모터·자체 고장을 SC11 소유로 바꾸지 않는다. BF02의 세정·DP02, FN04 공유 예고장도 연관 기능으로 분리한다.
4. P&ID 판I의 최종 표시 개정은 15/01/2013, 최초 날짜는 06/04/2011이다. 전기 시트의 기본 날짜27.05.2024와 시공도 24.11.11 `first draft design`은 다른 자료 시점이다. 현재 준공·현재 CPU 동일성은 확인되지 않았다.
5. 시공 PDF47/52에는 CHECKED·APPROVED가 공란이다. 이 문서를 승인 준공도나 현장 설치 완료의 근거로 쓰지 않는다.

## 2 I/O와 HMI

### 2.1 주소·형식·읽기/쓰기

DB 주소는 원본 DepDBBlock의 TOD N과 SSD/AO 또는 구성원 BO를 대조한 정적 주소다. 실제 CPU 현재값, 유지속성, 온라인 접근 가능성을 확인한 결과가 아니다.

| 신호 | 형식·주소 | 원본 선언·위치 | 의미와 소유 |
|---|---|---|---|
| SC-11_Fbk | Bool, %I5.1 | live_index doc512; 0613 RID242, NID40 UID2206, Input AO41; 0594 RID64 NID6 UID575/579 | 원시 물리 입력. 58KM1 보조접점 응답이며 축 회전/실제 분진 이송 센서는 아님 |
| Start SC11 | Bool, %Q4.1 | doc1310; 0602 RID163 NID33 UID950 Write, Output AO33; 0658 RID122 NID30 UID1034 | 출력 Coil. doc의 `a 52.3` 주석과 실제 Address를 혼동하지 않음 |
| Flag.M_SC_11 | Bool, DB2.DBX2.3 | 0604 RID162 NID33 UID948 Write/949 Read, AO19; 0603 Flag TOD N2; 0577 RID25 | 운전 요청. 자동 Set·자체 Reset·startup Word 쓰기·HMI 설정주소와 만남 |
| Allarm.SC_11_FAULT | Bool, DB3.DBX2.3 | 0657 RID125 NID30 UID1039/1042 Write, UID1041 Read, AO19; 0655 Allarm TOD N3 | 유지 고장. DB11의 HMI 주소와 다른 메모리 |
| Inputs.FEEDBACKMOTOR SC-11 | Bool, DB13.DBX5.1 | 0657 RID297 NID30 UID1071 AO41; 0604 RID255 NID34 UID997; 0596 RID305 NID29 UID41 | 처리 응답. 원시 I5.1과 Word 복사·다른 쓰기 경계를 분리 |
| Inputs.VR05 Run | Bool, DB13.DBX5.6 | 0604 RID221 NID33 UID23/NID34 UID998 AO46; 0603 Inputs TOD N13 | 별도 VR05 처리 응답. SC11 Reset 및 공유 조건에 사용 |
| Tag_73 | Timer, %T82 | doc1309; 0658 RID123, NID30 UID1036 Write/1037 Read, Timer AO82 | SC11 전용 2초 고장 감시. HMI 태그로 분류하지 않음 |
| ON / OFF | Bool, %M0.0 / %M0.1 | 0602 RID1/33, 0594 RID52/1 | 논리 접점. 이름만으로 상시 TRUE/FALSE라고 전제하지 않음 |
| UNDER TESTING | Bool, %M5.5 | 0602 RID4, NID33 UID947 AO45 | VR05 부재 Reset 분기에만 부정 접점. 변경·우회 지시 없음 |
| Flag.RESET_ALLARM | Bool, DB2.DBX6.0 | 0657 RID13, NID30 UID1040 AO48, DepDB Flag N2 | 공통 Reset 요청. SC11 운전 요청 재설정과 다름 |
| hours motors.SC_11_MIN/HOUR | Int, DB9.DBW156/158 | 0615 RID244/246, BO1248/1264; 0614 DB9 | HOUR에 Move1·별도 Move0이 있어 단순 누적시간으로 확정하지 않음 |
| BF02_RUN | Bool, %M180.4 | doc903; 0594 RID344, NID29 UID79 Write, Memory AO1444 | 필터 로직의 결과 메모리. SC11 원시 운전 피드백이 아님 |
| Data.DP_02 / Coeff.DP_01_SOGLIA_1 | Int, DB1.DBW242 / DB4.DBW138 | 0596 RID31 AO1936 / RID8 AO1104; 0595 DB1/DB4 | BF02 세정 비교 피연산자. 문서의 P&ID 단위를 이 Int에 임의 배정하지 않음 |
| Data.LAVA | Int, DB1.DBW230 | 0596 RID68 AO1840; 0595 Data TOD N1 | 필터 공유 선택값. SC10/SC11 원시 응답을 읽는 다중 Move 대상 |

### 2.2 원시 입력 Word 전달과 출력 상태 읽기

LAD1070 `0397-FlgNet.xml`, NID1:

- Part35 Move의 in은 ORef36/RID10 Tag_180. `0627`은 Word/Input AO32, live_index doc1591은 %IW4를 기록한다.
- out1은 ORef37/RID11. `0629`의 Word AO32/BAD BIRID4와 `0628` Inputs TOD N13을 대조하면 DB13.DBW4다. 따라서 해당 Word의 I5.1→DB13.DBX5.1 및 I5.6→DB13.DBX5.6 대응을 확인한다.
- Wire39=in, Wire40=out1, Wire41=Part27.eno→Part35.en, Wire34=Part22.eno→Part27.en. Part22/27/35에는 DisableENO=true가 있다. 선행 ENO·호출·TIA 해석이 유효한지 확인하지 않고 매 스캔 항상 복사된다고 쓰지 않는다.
- main LAD1613 `0030-FlgNet.xml`에서 Recipes Handler→HMI→HMI Output ENO 연쇄 후 Part37 `NOT Simulation(1)`을 거쳐 HMI Inputs CRef28.en을 호출한다. Wire31/32/33/42/44/43, CodeBlock29/RID135, 0688 및 0692 NID19 UID45가 근거다. Simulation(1)은 %M180.0이며 이름·기록만으로 현행 활성 여부를 판정하지 않는다.

출력 상태 경로는 별도다. LAD356 `0401-FlgNet.xml` NID1의 Part24 Move는 ORef37/RID30 `Tag_282`를 in(Wire62)으로 읽고 ORef38/RID51을 out1(Wire63)으로 쓴다. 0632의 Output/Word AO32는 QW4, 0633의 Word AO32/BAD26 및 0064의 Output TOD N14는 DB14.DBW4다. 이 방향은 **QW4→DB14.DBW4**이며 Q4.1의 또 다른 출력 Writer가 아니다. Wire60의 Part23.eno 허가도 보존한다. DB14는 DB11의 SC_11 HMI 응답주소와 별개다.

처리 응답에는 기존 simulation 자료의 다른 Writer 선언도 있다. 0635 RID126, NID4 UID49 AK Write가 DB13.DBX5.1에 해당한다. 이는 기존 정적 선언의 존재만 기록한 것이며, 시뮬레이터를 작성·수정·실행하거나 그 동작·현재 호출을 시험한 것이 아니다. 현재 프로젝트 교차참조로 활성 경계와 다른 Writer를 별도 확인해야 한다.

### 2.3 HMI 설정과 미결속 호출핀

`sources/hmi_plc_tags.csv`의 SC11 직접 설정행은3개다. Access Name은 PLC, 근거 열은 `dde.cfg 설정; 온라인 현재값 아님`이다.

| CSV 행 | HMI 이름 | 설정 주소 | 내부 ID |
|---|---|---|---|
| 127 | SC_11\Allarme1 | DB11,X54.1 | 00338 |
| 415 | SC_11\RispostaA | DB11,X54.0 | 001BC |
| 450 | SC_11\Flag | DB2,X2.3 | 00194 |

LAD1204 `0380-FlgNet.xml` 제목 sc11은 CRef22/RID638→CodeBlock23/RID1이다. 0623에는 HMI Standard Motors, 0624에는 호출 인터페이스가 있으나 원 네트워크 NID는 파생 map에서 null이다. 같은 UID/RID가 여러 호출 NID에 반복되므로 문자열 순서나 타 설비의 NID를 이용해 이름 결속을 만들어내지 않는다.

| Wire | 실제 XML 연결 | 이름 결속 상태 |
|---|---|---|
| 21 | Powerrail→CRef22.en | 연결 확인 |
| 37 | ORef24/RID664→Ingresso_run | SC11 처리응답은 검색문자열상 후보; UID/RID/NID 명명 선언 미확보 |
| 39 | ORef26/RID339→Allarme1 | SC_11_FAULT 후보; 명명 선언 미확보 |
| 40/41/42/43 | ORef27/28/29/30 RID48→Allarme2/3/4/5 | 0626 FALSE 선언·복수 호출기록 존재. 이 원 네트워크 NID 결속은 미확정 |
| 46 | Risposta→ORef33/RID340 | Motors.sc11.risposta 후보; 명명 선언 미확보 |
| 48 | Comulativo_allarmi→ORef35/RID342 | Motors.sc11.allarme_comulativo 후보; 명명 선언 미확보 |

미결속4개는 실제 데이터 ORef24/26/33/35다. 4라는 수를 모든 HMI 의미가 검증되었다는 뜻으로 사용하지 않는다. DB2 주소 일치도 버튼의 누름/놓음·토글·권한·실제 쓰기 이벤트를 증명하지 않는다. DB11,X54.1을 DB3.DBX2.3 직접주소로 대체하지 않는다. 현재 HMI 프로젝트, 창 객체·스크립트·알람 표시 설정이 추가로 필요하다.

## 3 고유 제어 구조

### 3.1 SC11 요청 Reset과 실제 출력

LAD1963 `0263-FlgNet.xml`, NID33:

- ON Part963→SC_11_FAULT Part965→OR934.in1.
- ON Part963→NOT VR05 Run Part22→NOT UNDER TESTING Part969→OR934.in2.
- OR934.out→RCoil939.in→ORef948/RID162 Flag.M_SC_11.
- ON Part963→M_SC_11 Part971→Coil943→ORef950/RID163 Start SC11.

정적 조건식은 요청 Reset=`ON ∧ (SC_11_FAULT ∨ (¬VR05_Run ∧ ¬UNDER_TESTING))`, 출력 Coil=`ON ∧ M_SC_11`이다.

Wire964는 공통 분기, 966/24/970은 OR 입력 경로, 956/958은 Reset 입력·대상, 959/972/961은 요청접점·출력입력·출력대상이다. 선언은 0602 ON RID1 UID944, UNDER TESTING RID4 UID947, 출력 RID163 UID950 및 0604 고장 RID160 UID945, VR05 RID221 UID23, 요청 RID162 UID948/949를 고유 NID33으로 대조했다.

UNDER TESTING은 자체 고장 분기를 면제하지 않는다. VR05 Run을 출력 Coil 앞의 독립 직렬접점처럼 바꿔 그리지 않는다. 같은 요청에 대한 다른 Set/Word 쓰기와 실제 스캔 순서를 대조하기 전, Reset과 출력의 최종값을 선 연결만으로 완결하지 않는다.

### 3.2 자동 Set2개와 계수의 의미

| 원본 | SC11 고유 대상 | 정적 조건 |
|---|---|---|
| LAD1843 /0164, NID3 | SCoil436, ORef605/RID25; 0577 AK Write | ON(785) ∧ NOT Emergency_module_fault(22) ∧ Tipo_preset=1(Eq400) ∧ Auto_ON1(823) ∧ Tempo_presetting=5(Eq428) |
| LAD1844 /0165, NID4 | SCoil773, ORef949/RID25; 0577 AK Write | ON(1145) ∧ NOT Emergency_module_fault(1154) ∧ Auto_ON1(1147) ∧ Tipo_preset=2(Eq737) ∧ Tempo_presetting=6(Eq765) |

- 1843 Wire686/687은 Tempo/5 비교, Wire688은 SC01·SC10·SC11 병렬 Set 허가, Wire691은 SC11 고유 대상. 상수는 0578 RID22, NID3 UID602, Int5다.
- 1844 Wire1035/1036은 Tempo/6 비교, Wire1037은 병렬 Set 허가, Wire1040은 SC11 대상. 상수는 0578 RID79, NID4 UID946, Int6다.
- 같은 네트워크에 있어도 다른 설비의 Set를 SC11 규칙으로 세지 않는다.
- LAD1841 `0162` NID1은 ON∧Auto_ON1에서 Add59로 Tempo_presetting+1, ON∧NOT Auto_ON1에서 Move66으로0을 쓴다. DB1.DBW96(Tempo), DB1.DBW98(Tipo), DB2.DBX7.3(Auto_ON1)는 0576/0577 선언을 대조한 주소다.
- LAD1723 `0024`는 ON Part188→Auto start motors CRef183.en(CodeBlock186/RID39, 0067/0068)을 호출하며 cyclic interrupt 블록의 검색 제목은 1 second다. 5/6은 비교 카운트다. 실제 현재 CPU에서 5초/6초 지연을 계측한 것으로 쓰지 않는다.

### 3.3 startup Word 덮어쓰기와 호출 경계

심볼명 M_SC_11/SC_11_FAULT만 검색하면 놓치는 Word 쓰기가 있다.

| 대상 포함범위 | 원본 선언·핀 | 실제 Word 쓰기 |
|---|---|---|
| DB2.DBX2.3 요청 | LAD402 `0147`, NID2; Part141 out1→ORef171/RID9, Wire189. 0563 Word AO16/BAD6, 0562 Flag TOD N2 | DB2.DBW2=INT#0. 입력 ORef170/RID54, Wire188; 0048 V0. Part138.eno→Part141.en Wire187 |
| DB3.DBX2.3 고장 | LAD403 `0148`, NID3; Part253 out1→ORef288/RID26, Wire308. 0563 Word AO16/BAD23, 0562 Allarm TOD N3 | DB3.DBW2=INT#0. 입력 ORef287/RID54, Wire307; 0048 V0. Part250.eno→Part253.en Wire306 |

두 Word는 byte2와3을 덮어쓰므로 SC11의 bit2.3이 포함된다. LAD402의 ON Part208은 Wire209로 첫 Move138/155를 허가하며, LAD403의 ON Part329는 Wire330으로 첫 Move250/267/281을 허가한다.

0148의 파생 network-map NID는 null이다. 여기의 NID3은 0047 ON UID284/RID1, 0048 INT0 UID287/RID54, 0563 UID288/RID26의 같은 선언군 결속 및 0562 DB3 근거로 직접 검토한 것이다. 파생 map을 수정하지 않았다. RID/UID만 같은 다른 블록의 선언을 섞지 않는다.

live_index doc398은 `startup only`, Event class startup, Title `power up - start up`을 기록한다. 이것은 해당 Word 쓰기의 프로그램 자료상 문맥이며, 현재 기동 이벤트 실행·현재 활성·전원복귀 상태·DB 유지정책 검증은 아니다. 현재 CPU를 재기동하거나 값을 시험하지 않았다.

main LAD1619 `0031`은 ON Part282/Wire283 아래 Allarms1 CRef264(CodeBlock275/RID58)를, LAD1620 `0549`는 ON Part350/Wire351 아래 Motors1 CRef319(CodeBlock337/RID67), Filter CRef322(CodeBlock339/RID70), time work motor CRef334(CodeBlock347/RID82)를 호출한다. 0688/0694 NID6/7이 근거다. HMI/입력전달→알람→모터·필터·시간의 정적 목록과 별도 cyclic interrupt/스타트업/외부 HMI 요청 쓰기를 구분한다. 실제 최종 쓰기 우선순위·인터럽트·재기동 결과는 미검증이다.

### 3.4 BF02 세정허가와 공유 Data.LAVA

LAD1886 `0219-FlgNet.xml`, Filter/NID29는 SC11 처리응답을 별도 필터 기능에 사용한다.

- ON Part21→SC11 처리응답 Part28(ORef41/RID305)→VR05 처리응답 Part29(ORef42/RID319).
- Wire64가 위 직렬 결과를 Le30.pre와 Forza_Lavaggio Part31.in으로 분기한다.
- Le30의 in1=Data.DP_02(ORef43/RID31, Wire65), in2=**Coeff.DP_01_SOGLIA_1**(ORef44/RID8, Wire66). 원문은 Le, 즉 이하 비교다. BF02라는 이유로 DP_02_SOGLIA_1로 고치거나 비교 방향을 바꾸지 않는다.
- Le30.out(Wire67) 또는 Forza_Lavaggio Part31.out(Wire69)이 OR32를 거쳐 Coil33의 `#Abilita_lavaggio_BF02`(ORef46/RID65, Wire70/71)를 쓴다.
- Coil33.out→Coil78.in은 Wire76, Coil78의 대상 BF02_RUN(ORef79/RID344)은 Wire77이다. 앞 Coil의 out 전달을 그대로 보존한다.
- 정적 경로: `ON ∧ SC11_processed ∧ VR05_processed ∧ ((DP02 ≤ DP01_SOGLIA1) ∨ Forza_Lavaggio)`가 세정허가 경로다. Forza_Lavaggio 분기도 두 처리응답을 우회하지 않는다.

0596은 처리응답/DP/계수 Global 선언, 0598은 Forza_Lavaggio(RID57)·Abilita_lavaggio_BF02(RID65)의 Local/InterfaceAccess, 0594는 BF02_RUN Memory 선언이다. 로컬 허가를 전역 실물 센서로 바꾸지 않는다. 실제 밸브별 세정순서·DP02 환산·정상차압/보호 한계는 이 SC11 조사로 확정하지 않는다.

LAD1888 `0202-FlgNet.xml`, NID6은 원시 응답을 읽으며 처리응답 경로와 다르다.

| Part | in→out1 | 허가 경로 |
|---|---|---|
| Move547 | Int0 ORef570→LAVA ORef571 | OFF Part599의 out, Wire600/583/584 |
| Move553 | Int1 ORef573→LAVA ORef574 | OFF∧SC-10_Fbk Part601, Wire602/587/588 |
| Move559 | Int2 ORef576→LAVA ORef577 | OFF∧SC-11_Fbk Part603, Wire604/591/592 |
| Move566 | Int3 ORef580→LAVA ORef581 | OFF∧SC-10_Fbk Part605∧SC-11_Fbk Part607, Wire608/596/597 |

0594 SC11 RID64 UID575/579, 0596 LAVA RID68, 0597 Int0/1/2/3의 RID67/70/72/74와 NID6을 대조했다. 공통 OFF 접점은 원문에 있다. OFF를 없애거나 이름만으로 FALSE라고 단정하지 않는다. 여러 Move가 같은 DB1.DBW230을 쓰므로 단순 상호배타 선택문으로 재작성하거나 최종 값3을 무조건 보장하지 않는다. 별도 Filter 공유 기능이며 SC11 운전 요청의 다른 Writer는 아니다.

### 3.5 운전시간의 Move1과 초기화

LAD1038 `0325-FlgNet.xml`, NID40:

1. Tag_47 Part2234와 **원시 SC-11_Fbk Part2236**가 직렬이며 Wire2237이 Add2188.en과 Ge2195.pre로 분기한다.
2. Add2188은 SC_11_MIN(ORef2207/RID244)+Int1(ORef2208/RID7)→MIN(ORef2209), Wire2219/2220/2221.
3. Ge2195는 MIN(ORef2210)>=Int60(ORef2211/RID8), Wire2222/2223; out/Wire2224→Move2198.en.
4. Move2198의 in은 **Int1**(ORef2212/RID7, 0616 CB V1)이며 out1은 SC_11_HOUR(ORef2213/RID246), Wire2226/2227. HOUR+=1 연산이 아니다.
5. Wire2228의 ENO→Move2201로 MIN=0(ORef2214/RID12→2215/RID244, Wire2229/2230), Wire2231의 ENO→SCoil2204가 Flag_Aggiorna_DB를 Set한다.
6. LAD1052 `0339`, NID54는 Tag_48 Part3049→Move3008→3011→3014→3017의 ENO 연쇄 후 Move3020에 Int0(ORef3032/RID12)을 넣어 SC_11_HOUR(ORef3033/RID246)를 쓴다. Wire3046/3047/3048. 인접 SC10 등의 초기화를 SC11 고유 출력으로 세지 않는다.
7. Tag_47=%T13, Tag_48=%T17는 live_index doc107/108. LAD1056 `0019`, NID58의 NOT Tag_47 Part3120→SdCoil3112, ORef3114/RID335 S5T#1M(0616), ORef3116 타이머가 시간 관련 근거다. 타이머의 현재 주기·이벤트·외부 누적 수신부는 미검증이다.

이상하게 보이는 Move1을 Add1로 수정하지 않았다. 이 값만으로 실제 누적 운전시간·정비주기를 산정하지 않는다.

## 4 전기 전달 경로와 실제 페이지

### 4.1 렌더 확인 목록·판본

| 자료 | 실제 PDF 페이지 | FG/도면번호와 확인 범위 |
|---|---:|---|
| Electrical_Rev2.pdf | 59 | FG58, FILTER DUST SCREW SC-11, 전력·명령·응답 |
| 같은 PDF | 122 | FG121, DIGITAL INPUT MODULE, E5.1/단자12 |
| 같은 PDF | 141 | FG140, DIGITAL OUTPUT MODULE, A4.1/단자2 |
| 같은 PDF | 256 | FG253, MATERIAL LIST, 58KM1·58QM1 |
| Electrical_Can_Decoating_20241118.pdf | 47/64 | CANDC-CONS-E030-047, DUST ZONE13, M35/케이블2_1 |
| 같은 PDF | 52/64 | CANDC-CONS-C002-052, CABLE SCHEDULE(2), CR→SC11/M35 |
| PID_1684n002I.pdf | 1 | 1684n002 판I, BF02→SC11/M35→VR05/M39 |

원본 PDF7쪽을 실제 렌더하여 확인했다. crop 두 개는 같은 P&ID p1의 확대이며 추가 페이지로 세지 않는다. 전기4시트에는 기본 날짜27.05.2024가 보이고 별도 Rev2 날짜 표시는 확인되지 않는다. 파일명 Rev2를 시트별 개정완료로 대체하지 않으며, 인접 FG120/139의 17.03.2025 표기를 FG121/140에 복제하지 않는다. FG253=PDF256인 만큼 일괄 +1 오프셋을 적용하지 않는다.

### 4.2 전력 양끝점

FG58/PDF59:

`8.3L1/L2/L3(이전57/9, 다음61/0) → 58QM1 주접점1-2/3-4/5-6 → 58KM1 주접점1-2/3-4/5-6 → 58U1/V1/W1 → XM(동일 선명) → 58QS1 주접점1-2/3-4/5-6 → M35 U/V/W 및 PE → SC11`.

- 패널 배선은 BLACK FS17 1.5 mm² 표기다.
- 58QM1의 5.5-8 A는 도면상 보호기 범위이며 M35의 5.8 A 표기는 모터 자료값이다. 두 값을 실제 설정치나 조정 지시로 쓰지 않는다.
- 시공 PDF52 행2_1: 케이블 `=DUS+SC11-M35A`, FROM CR, TO SC-11/M35, FILTER DUST SCREW, GAC, CV4심/1.5, spare0, 경로100→200→220→221→223 RA→E400, Adjustment3, LEN94.
- 시공 PDF47: DUST ZONE13, route223 RA, **4/Pipe16**, M35, SC-11, 2_1, CV1.5/4와 대응한다. 외부 CV 케이블과 패널 내부 FS17을 같은 케이블 규격으로 합치지 않는다. LEN94의 현장 실측·단위 및 CR 측 실제 단자·케이블심선-단자 매핑은 추가자료가 필요하다.

### 4.3 출력 명령 양끝점

`PLC Q4.1 ↔ FG140/PDF141 A4.1, CPU515/MOD15/출력단자2 → FG58의 140/1 참조 → XS53 → 58QS1 보조접점 → XS54 → 선58.1 → 58QM1 보조접점 → 58KM1 코일 A1; A2→-0Vdc10.6`.

58QS1·58QM1의 명령경로 보조접점에는 이 렌더에서 개별 단자번호가 표시되지 않는다. 임의로13/14를 넣지 않는다. FG140은 +24Vdc10.9→X21 3032(5×20 4A F)→선140.1→모듈 공급단자9, 0V단자10을 보인다. 모듈 공급퓨즈4A를 SC11 모터 과부하 설정값으로 사용하지 않는다.

Q4.1이1인 것과 코일 흡입, 모터 전력전달·회전은 다른 관찰 지점이다. 도면상 직렬 QS/QM 경로·코일 전원 문제가 있으면 출력논리만으로 접촉기 흡입을 보장할 수 없다. 이는 정적 경로 설명이며 현장 이상을 진단한 결과가 아니다.

### 4.4 피드백 양끝점

`FG58 +24Vdc10.7 → 58KM1 보조접점13-14 → E5.1(121/2 참조) → FG121/PDF122 E5.1, CPU515/MOD9/입력단자12 → PLC I5.1 → LAD1070 IW4→DB13.DBW4 → Inputs.FEEDBACKMOTOR SC-11 → LAD1808 고장감시·LAD1886 세정허가·LAD1964 공유예고장`.

FG121의 모듈 공급은 X21 3008(5×20 2A IST.) 및 단자19/20의 별도 경로다. 도면에 표시된 개방 접점과13-14를 현재 실물 정상극성·실제 NO/NC 배선 판정으로 확대하지 않는다. 58KM1 응답이 있더라도 감속기·커플링·스크루·실제 분진흐름 정상은 별도 확인이 필요하다.

### 4.5 BOM와 설치 실물 구분

FG253/PDF256의 원본 BOM:

- 58KM1: Siemens 3RT2015-1BB41, CONTACTOR3 kW/1L/DC24V/S00 VT. RC element 3RT2916-1CB00.
- 58QM1: Siemens 3RV2901-1E 보조접점, 3RA1921-1DA00 결합부, Wohner WR32433 어댑터, Siemens 3RV2011-1HA10 MAGNETOTHERMIC S00 5.5-8A.

이는 BOM의 모델과 설명이다. 현재 설치 모델·교체품 호환·안전등급·토크·정비주기·보호설정은 명판·승인자료·현재 제조사 원문 없이 채우지 않는다. 인접 FN04의 인버터를 SC11 장치로 가져오지 않는다.

## 5 알람·복구

### 5.1 SC11 자체 고장

LAD1808 `0442-FlgNet.xml`, NID30:

- ON Part1057→Start SC11 Part1059→NOT SC11 처리응답 Part1070→SdCoil1021.in(Wire21).
- 타이머 value ORef1035/RID28, 0656의 S5Time `S5T_x0023_2S`, Wire1045. operand ORef1036/RID123 Tag_73, Wire1046. 이는 2초 원문이며 512라는 인코딩값을 512ms로 바꾸지 않는다.
- ON∧StartSC11 후 Tag_73 접점 Part1061→SCoil1027→SC_11_FAULT ORef1039/RID125, Wire1047/22/1050.
- ON→RESET_ALLARM Part1065→SC_11_FAULT Part1067→RCoil1032→같은 고장 ORef1042, Wire1052/1066/1053/1068/1055.

정적식은 timer input=`ON∧StartSC11∧¬SC11_processed`, Set=`ON∧StartSC11∧Tag_73`, Reset=`ON∧RESET_ALLARM∧SC_11_FAULT`다. 고장 타이머 입력과 Set 접점은 서로 다른 분기다. 명령이 없어지거나 응답이 돌아왔다고 유지 고장이 자동 Reset된다고 쓰지 않는다. startup DB3.DBW2=0도 별도 고장 쓰기다.

Set/Reset이 같은 실행주기에 동시에 성립하는 경우의 실제 우선순위·재기동·다른 Writer는 TIA와 현재 프로젝트 확인 전 미확정이다. Reset은 원인 제거·응답 정상·M_SC_11 재요청의 증명이 아니며 자동 재기동 보장도 아니다.

### 5.2 FN04 공유 예고장과90분 경계

LAD1964 `0264-FlgNet.xml`, NID34의 공통 조건은 `ON∧Inputs.FN04 Run∧(¬SC01_processed∨¬VR03_Run∨¬SC10_processed∨¬VR04_Run∨¬SC11_processed∨¬VR05_Run)`이다.

SC11은 Part1032 부정접점/ORef997(RID255), Wire1010/1033→OR972.in5, VR05는 Part1034/ORef998(RID221), Wire1011/1035→OR.in6이다. Wire1012는 OR.out을 Coil982 `Allarm.Prealarms_FN04`와 SdCoil985 및 타이머접점 Part1036으로 분기한다.

Tag_126=%T131, 0602 RID169 NID34 UID1001/1002. value ORef1000/RID112는 0606의 S5T#1H_30M이며90분이다. 타이머접점 뒤 Coil990이 Local `Stop_Fan_FN04`(0605 RID170, UID1003)를 쓴다. LAD1965 `0265` NID35의 해당 Local 접점 Part1042/ORef1019→OR1003.in4→RCoil1010이 FN04 요청을 Reset한다.

SC11의 독립 2초 고장과 FN04 공유90분 기능을 분리한다.90분을 SC11 안전 정지 지연으로 설명하거나 SC11만의 문제로 진단하지 않는다. SC11이 원인이 아니어도 다른5개 처리응답으로 같은 공유 조건이 성립할 수 있다. FN04 자체고장·인버터·설정·TC09 등 다른 정지경로 전체 검증은 이 초안 범위 밖이다.

### 5.3 복구 확인에 필요한 증거

고장 표시 해제, 원인 제거, 전기전달 회복, 원시/처리응답 일치, 별도 운전요청 재발행, 실제 스크루·분진흐름 정상은 각각 기록해야 한다. 승인된 안전절차와 자격 있는 현장 담당자의 관찰로 시각·상태를 확보한다. 이 문서는 통전 작업, 가드 해제, 신호강제, 보호설정 변경이나 고장 상태 재기동을 지시하지 않는다.

## 6 증상별 관찰·수리 인계

실제 관찰값은 아직 없다. 다음은 원인 확정이나 실행한 수리가 아니라 비교 지점과 필요한 자료다.

| 증상 | 순서대로 확보할 관찰 | 원본 비교·원인 배제 | 조치·복구 판정의 경계 |
|---|---|---|---|
| 요청을 넣어도 유지되지 않음 | HMI 이벤트/DB2.X2.3, DB3.X2.3, VR05 DB13.X5.6, ON, UNDER TESTING, startup 시각 | LAD1963 Reset·자동 Set2개·Word 초기화·외부 HMI 쓰기를 분리 | VR05 응답 실제원인과 요청경로를 먼저 확인. 값강제·시험모드 변경 금지 |
| Q4.1은 켜지는데 응답 없음 | 승인 안전절차로 출력단자2, XS53/54, 58QS1/QM1 경로, 코일 A1/A2, KM 상태, I5.1 | FG140/58/121 연결 및2초감시를 대조 | 논리명령·전기전달·기계 상태를 각각 분리. 현장 조치/재가동 별도 승인 |
| 접촉기 응답은 있는데 고장 발생 | 같은 시각의 I5.1, DB13.X5.1, 호출/Word전달, StartSC11, T82, 고장 Set/Reset | 원시입력 정상만으로 처리응답 전달·타이머 스캔을 배제하지 않음 | 현재 프로젝트 교차참조·시계동기 자료 필요 |
| 모터/접촉기는 운전인데 분진이 안 나옴 | 스크루·감속기·커플링·막힘 관찰 및 VR05 실제 상태 | KM 보조접점은 회전·이송 센서가 아님 | 현장 안전격리 후 자격자 점검자료와 실제 흐름 증거로 판정 |
| SC11 운전인데 BF02 세정이 안 됨 | DB13.X5.1/X5.6, DP02 Int값/환산, DP01_SOGLIA1, Local Forza/Abilita, BF02_RUN | LAD1886은 처리응답 직렬, 이하비교 OR 강제세정. SC11 운전 하나로 허가되지 않음 | 세정 밸브/DP기능은 별도 담당. 설정값·비교방향을 임의 변경하지 않음 |
| FN04가 늦게 정지하거나 공유예고장 발생 | FN04 처리응답,6개 분진경로 처리응답의 동시 타임라인, T131, Prealarms, Local Stop | LAD1964의 OR6개와90분, LAD1965의 다른 정지분기 비교 | SC11에 단독 원인 배정 금지; 직접2초고장과 구분 |
| 운전시간이1 또는0으로 보임 | DB9.DBW156/158, T13/T17, Flag_Aggiorna_DB, 수집처·리셋시각 | LAD1038 Move1와 LAD1052 Move0 | 누적시간으로 추정해 정비주기 산출 금지 |
| HMI 표시가 PLC와 다름 | CSV설정 버전, DB11.X54.0/1, DB2.X2.3, 실제 이벤트·통신상태 | 미결속 ORef4개, DB11/DB13/DB3/DB14 영역 분리 | 현재 HMI 원본 확보 전 표시/알람의 완전 결속 미확정 |

관찰 기록에는 설비ID·관찰자·날짜/시간대·신호/물리위치·값과 단위·수집장치·프로젝트/CPU 근거·비교 원본·배제 결과·조치·복구 증거를 넣는다. 미확인 값은 빈칸/미확인으로 남기고0을 대신 쓰지 않는다. 운영사진·사용자 기록을 이 자료 묶음이나 공개 Git에 복제하지 않는다.

## 7 네 기능 적용과 기록 보존

| 기능 | 적용 근거·향후 범위 | 실제 구현·검증 |
|---|---|---|
| 도면·래더 나란히 보기 | FG58/121/140와 LAD1963/1808/1070; BF02·FN04는 연관링크 | 구현하지 않음. 정적 원본 렌더/논리 대조만 수행 |
| 백업 미리보기·선택 복원 | SC11 지원 여부·키 격리를 확인한 후 연결 | 저장·재읽기·재열기 미수행 |
| 전후 기록 비교 | 요청/출력/원시/처리/알람을 같은 시간축으로 비교 | 실제 또는 합성 기록 시험 미수행 |
| 관찰 보고서/PDF | 위 관찰항목·미확정·자료버전을 포함 | 사용자 보고서 생성/기능검증 미수행. 원본 PDF 열람과 구분 |

다른 설비 기록·미지 필드·초안·저장키·0과 빈칸을 보존해야 한다. generated_with/saved_with는 자료생성·저장근거이며 관찰 당시 CPU의 증명이 아니다. 현재 SC11 baseline 화면이나 범용 저장기능이 있다는 사실만으로 BC01 동등4기능을 완료로 선언하지 않는다.

## 8 검증·독립 검토·최종 상태

- 수행: 고정 commit/버전/Git 상태 확인, 읽기 전용 preflight, SC11 대장·원본 선언/핀·Word 범위·CSV 대조, 원본 PDF7쪽 렌더 및 직접 시각 확인.
- 정적 의미 검토:21개 네트워크의 SC11 관련 구간과 선언군을 대조했다. 이것은 모든 네트워크의 모든 분기·실행·현장 의미를 검증한 수가 아니다. HMI4개 데이터 ORef의 이름 결속 및 HMI 네트워크 NID는 미확정으로 남겼다.
- 원본 해시:76개 근거 파일의 SHA-256 목록과 고정 commit 바이트 대조를 별도 보관한다.76개 일치는 바이트 동일성만 뜻하며 의미 검토76개, 완료설비76개, 현장 검증을 뜻하지 않는다.
- 독립 검토: 핵심 근거 제한 대조 완료; 사용자 독립 검토 대기. 필요 정정이 생기면 원본·수신초안·수정 사유를 보존한다.
- 실행하지 않음: 매뉴얼 생성기, npm test/build, BC01 회귀, UI/모바일/기록 QA, 패키지·게시, TIA 컴파일, 현재CPU 비교, 현장 관찰/수리. 원본조사 초안만 작성하므로 이 실행들을 통과했다고 표시하지 않는다.
- 시뮬레이터 관련은 기존 선언의 다른 Writer 존재만 확인했다. 작성·수정·생성·실행·행동시험은0이다.

| 상태 | 이번 결과 | 근거·제한 |
|---|---|---|
| documentation | draft_complete_with_gaps | 7영역 조사 초안; 독립 검토·실제매뉴얼 통합 전 |
| static_review | source_review_partial | 원본 관련구간·7PDF쪽 직접검토; 의미 미확정 보존·독립검토 대기 |
| ui_records | not_run | 구현·저장·재열기·PDF 기능시험 없음 |
| publication | not_published | 공통버전·대장·배포 변경 없음 |
| tia_compile | not_performed | TIA 환경 작업 없음 |
| live_cpu | not_performed | 현재CPU/프로젝트 동일성 없음 |
| field_recovery | not_performed | 실물·원인제거·복구 확인 없음 |

## 9 다음 검토와 자료 요청

첫 후속 작업은 SC11 초안의 고유 선언·Word 덮어쓰기·BF02 세정허가·도면 양끝점 독립 검토다. 통합·UI 구현·게시·로컬2차133 진행은 이 산출물로 자동 승인되거나 착수되지 않는다.

필요자료:

1. 현재 PLC 프로젝트의 SC11/DB2.DBW2/DB3.DBW2/IW4/DB13.DBW4 교차참조, startup/인터럽트/일반스캔 호출, 유지 속성과 CPU 비교.
2. 현재 HMI 프로젝트의 SC_11 버튼·표시·알람 객체, 미결속 ORef24/26/33/35가 포함된 원본 호출 선언.
3. M35·58KM1/QM1/QS1 명판, 승인 준공도·단자대/케이블심선표, 실제 공급·현장 정상극성 자료. 설치모델·설정값은 원본 BOM과 구분.
4. BF02의 DP02 센서/환산·세정 회로, 공유계수 DP_01_SOGLIA_1의 승인 설명. P&ID5-10mbar 표기를 현재 PLC 정상값/보호값으로 옮기지 않음.
5. 고장 발생부터 원인 제거·Reset·재요청·실제 스크루/분진흐름 회복까지 시간대가 있는 관찰기록. 운전시간 Move1/Move0의 설계 의도와 수집처.

완료 커밋 없음. 고정 원본은 그대로이며 재개 시 이 초안, SC11 추출물, 고정 source-mv06의 원본을 함께 대조한다.

## 부록 A 원본 위치 요약

| LAD | XML | NID | 이번 검토 구간 |
|---:|---|---|---|
| 1963 | 0263-FlgNet.xml | 33 | SC11 요청 Reset·Q4.1 Coil |
| 1808 | 0442-FlgNet.xml | 30 | T82 2초·FAULT Set/Reset |
| 1843/1844 | 0164/0165-FlgNet.xml | 3/4 | SC11 자동Set 및5/6 비교 |
| 1841/1723 | 0162/0024-FlgNet.xml | 1/4 | 자동계수·호출 |
| 402/403 | 0147/0148-FlgNet.xml | 2/3 | DB2/3 Word2 초기화;403은 선언에서 직접 결속 |
| 1070/356 | 0397/0401-FlgNet.xml | 1/1 | IW4→DB13.W4;QW4→DB14.W4 |
| 1204 | 0380-FlgNet.xml | 미확정 | HMI 호출핀·4개 데이터 이름 미결속 |
| 1886/1888 | 0219/0202-FlgNet.xml | 29/6 | BF02 세정허가·LAVA 복수 쓰기 |
| 1964/1965 | 0264/0265-FlgNet.xml | 34/35 | FN04 공유90분·Local Stop 소비 |
| 1038/1052/1056 | 0325/0339/0019-FlgNet.xml | 40/54/58 | 운전시간 Move1·초기화·T13 |
| 1613/1619/1620 | 0030/0031/0549-FlgNet.xml | 19/6/7 | HMI·입력·알람·모터·필터·시간 호출 |

추출 JSON/trace는 탐색·재검토 보조물이다. 자동 UID/RID/NID 결합 결과에 다른 블록 동번호 후보가 함께 나타날 수 있다. 핵심 주장은 본문에 적은 선언군·DB 소유·핀으로 직접 확인하며, 추출물의 이름열 하나만으로 결속을 확정하지 않는다.

## 부록 B SHA-256

다음은 조사근거 파일의 고정 버전 바이트 해시다. 전체76개이며 해시일치와 의미검토의 구분은8절과 같다.

| 고정 원본 상대경로 | SHA-256 |
|---|---|
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
| `all-in-one/sources/decoded-original/0162-FlgNet.xml` | `892eab96a4f5c87cfafd35f8a2e2a04982a93ca23c777312101882e408b11deb` |
| `all-in-one/sources/decoded-original/0164-FlgNet.xml` | `15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491` |
| `all-in-one/sources/decoded-original/0165-FlgNet.xml` | `4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88` |
| `all-in-one/sources/decoded-original/0202-FlgNet.xml` | `8caa0c15a086ffb64f7857fb656b3baba3090a32948b9942ccecff6c730186bb` |
| `all-in-one/sources/decoded-original/0219-FlgNet.xml` | `245409937abf7e28f25a24d4a6d311a801a4b2ee7293148be9b3d266352eb53a` |
| `all-in-one/sources/decoded-original/0263-FlgNet.xml` | `de5cef96279de6a92a6e9eb746a13f23c8889c0ba1701a18e74838c6c6dc3d34` |
| `all-in-one/sources/decoded-original/0264-FlgNet.xml` | `9af15015b447731255eff81680aa71321fb4d0ebe2c28904f442146538ff030d` |
| `all-in-one/sources/decoded-original/0265-FlgNet.xml` | `f2471b6ab6169e4c082983ea2080a383cf8b13cba4503a9a07f83d0956fbf08a` |
| `all-in-one/sources/decoded-original/0325-FlgNet.xml` | `f0a2ee6233672a3a6482fe368751677da15768dd24c4bb1147ee0ae9fe2f77c2` |
| `all-in-one/sources/decoded-original/0339-FlgNet.xml` | `ce2c6279b55c8a5ac837a0f7c7a0945636df7dc52b68a1c3d6ec158234b37543` |
| `all-in-one/sources/decoded-original/0380-FlgNet.xml` | `84b6be27e4d63bbfdd8fa5c0f48ada9ccb14f2061fd691f5a8e547241159ebae` |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` |
| `all-in-one/sources/decoded-original/0401-FlgNet.xml` | `60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae` |
| `all-in-one/sources/decoded-original/0442-FlgNet.xml` | `46243969afe61a8ca0051fa012008219bad84eae00670e5c960aa5f153eac41e` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` |
| `all-in-one/sources/decoded-original/0555-IdentXmlPart.xml` | `46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` |
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
| `all-in-one/sources/decoded-original/0652-IdentXmlPart.xml` | `251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692` |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` |
| `all-in-one/registers/control-spec.json` | `1e495b32f1f11b910919fbd2945e842a019fce9a27a6a0d7298041a7fab00079` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` |


## 전달 전 핵심 근거 제한 대조
2026-10-11 고유 출력/요청 Reset의 원본 Part/Wire와 해당 모터 회로 실제 PDF 렌더를 표본 재확인하고 인용 원본 SHA256을 모두 재계산하여 일치했다. 전체 원본 의미 검토 또는 현재 CPU/현장/게시 검증으로 확대하지 않는다. 사용자 독립 검토와 미확정 경계는 유지한다.
