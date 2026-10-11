# VR06 로터리 밸브 원본 조사 초안

VR06은 P&ID의 LD-01 출구에 있는 VR-06/M40이며, FN-05·ER-01의 공기 경로와 만나는 위치에 표시된다. 전기 원본은 64KM1 직접기동 회로, PLC 출력은 Q4.6, 원시 응답은 I5.7이다. **I5.7은 64KM1의 13–14 보조접점 응답이다. 축 회전·석회 투입량 또는 배출 완료 검출로 확인된 신호가 아니다.**

VR06 고유 제어는 고장 외에 `NOT Start ER-01 AND NOT UNDER TESTING`으로 운전 요청을 Reset한다. ER01의 명령을 읽는 조건을 ER01 실제 가열·온도 정상 확인으로 바꾸면 안 된다. VR06 처리Run은 LD01 및 LD01 진동기 요청 해제에도 쓰인다. 전용 고장 타이머는 Tag_78/%T95, S5T#2S다. 운전시간 HOUR에는 누적 Add 대신 Move 상수1과 공통 Move0이 있으므로 총 가동시간으로 단정하지 않는다.

이 산출물은 작업3 자체 cloud 원본 조사 초안이다. 로컬 2차133 통합·게시, 기능 구현, TIA 컴파일, 현재 CPU, 실물·현장 복구 완료를 뜻하지 않는다.

## 작업 기준과 보존

- 대상: catalog_id `VR06`, kind `motor`, group `집진·석회`, parent_id 없음, depth0, priority_key 없음. INVENTORY catalog 배열107 및 equipment 배열44에 대응한다. 같은 이름의 VR01~VR05와 고유 ID를 유지한다.
- 세 번째 5개 묶음 VR04/VR05/VR06/SC10/SC11 중 VR06 한 개다. `progress/TASK3-BATCH03-SCOPE.json`의 제외·중복 검토 결과는 new_research_scope=true, alias_duplicate=false, physical_identity_verified=false다. phase2 후보133은 계획 분모이며 조사·통합 완료 수가 아니다.
- 고정 읽기 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 원본 저장소: https://github.com/esp6662266/gme-plc-manual . 이후 main 또는 현재 현장과 동일하다고 가정하지 않는다.
- GME-STD-1.0.0, AGENTS, gme-equipment-rollout/SKILL, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, 최신 고정 진행자료를 읽었다. 기존 VR03 초안은 구조를 참고했으며 VR06 수치·주소·제어·도면은 각 원본에서 다시 확인했다.
- 읽기 전용 preflight 종료0, inventory_matches=true. 대장248, 우선23, 대응18, 제외90, 제외부모 하위보류7, phase2 133이 일치한다. 기존 requirements-audit.json/all-in-one-data.json의 source_byte_changes 두 항목은 표준 생성 당시 대비 차이이며 이번 작업의 변경이 아니다.
- 조사일: 2026-10-11 UTC. 작성자: VR06 원본 조사 작업자. 실제 실행 모델명·추론 설정의 런타임 증명은 확보하지 않았다.
- 쓰기 범위: 본 초안과 `extracts/VR06/`만. 원본·공용 declarations·다른 설비·코드·버전·대장·배포·운영기록 변경0. 시뮬레이터 작성·수정·생성·실행·행동 시험0. 실제 PLC·현장·보호값과 SEJIN 운영자료·사진·이력 변경/통합0.
- 해시 일치는 원본 바이트 보존 검사다. 원본 의미검토, 기능 시험, TIA/CPU/현장 확인과 별도다. 파일별 결과와 범위는 부록에 기록한다.

이하 경로는 원본의 `all-in-one/` 아래다. `0269`는 `sources/decoded-original/0269-FlgNet.xml`, 선언 `0604`는 `0604-IdentXmlPart.xml`을 뜻한다. LAD는 문서 ID, 색인은 block 내 index_order, NID는 선언의 네트워크 식별자로 구분한다.

## 7영역 적용표

| 영역 | 적용 상태 | 확보 근거 | 남은 범위 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | VR06/M40, LD01/FN05/ER01 관계, 고정 원본·판본 | 현행 실물·명판·배치 일치 |
| I/O·HMI | 적용, 일부 근거 미확보 | Q4.6/I5.7, DB2/3/9/13, HMI3 설정행 | HMI4 데이터 ORef 결속, 화면 이벤트·온라인 |
| 제어 구조 | 적용 | ER01 명령 조건, 요청Reset/출력, LD01 영향, 전체Word 쓰기, 호출 | 재시작·최종값·실제 주기·외부Write |
| 전기 전달 경로 | 적용 | FG64/121/140/254, 시공36/51, P&ID1 시각 확인 | 실제 단자·정상 극성·보호 설정·준공 |
| 알람·복구 | 적용 | 2초 감시, Set/Reset, 요청 해제 | 실제 표시·원인 제거·재요청·복구 |
| 증상별 수리 | 적용, 관찰 지점만 | 요청→Q→접촉기→I→DB→HMI 비교 | 실제 고장진단·조치·관찰 기록 없음 |
| 완료 기준 | 적용 | 검사와 미검사 분리, 부족 자료·재개 경계 | 통합/UI/기록/게시/TIA/CPU/현장 별도 |

## 1. 설비와 자료의 소유 경계

1. `registers/equipment.json` VR06행은 motor/FG64, parent 빈값, 별칭 빈 배열이다. P&ID에서 LD01와 붙어 있더라도 catalog parent를 LD01로 바꾸거나 M32/M33·LT01를 VR06 소유로 배정하지 않는다.
2. `PID_1684n002I.pdf` p1을 실제 렌더했다. LD-01 하부 M32 출구 아래 VR-06/M40이 있고, FN-05/M41→ER-01 공기 경로가 그 하부 유로에 접속한다. M40은 0.25kW/440V, M32/M33은 각각0.18kW/440V다. 이웃 기기 용량을 VR06에 복제하지 않는다.
3. `Electrical_Rev2.pdf` FG64/PDF65 제목은 ROTARY VALVE VR-06, M40은0.25kW/0.76A다. 64QM1→64KM1→64QS1→M40 직접기동 경로다. 이 직접 경로에서 인버터 속도지령·아날로그 전류/PID·엔코더는 비해당이다. 현장에 추가 장치가 없다는 뜻은 아니다.
4. VR06이 ER01 출력 명령을 읽고 LD01 요청에 영향을 주는 PLC 의존성과 실제 물질·공기 전달 관계는 구별한다. ER01 내부 온도·안전제어, FN05 실제 송풍, LD01 실제 투입량은 본 문서가 확인한 VR06 신호만으로 보증되지 않는다.
5. P&ID 도번1684n002는 원 작성일06/04/2011, 판I 변경일15/01/2013이다. 개정E(12/11/2011)에 M15/17/40/41 모터출력 변경이 기재되어 있다. 현행 명판 증거가 아니다.
6. 전기 검토 시트 FG64/121/140/254는 하단 기본 날짜27.05.2024가 보인다. 파일명 Rev2만으로 모든 시트에 같은 Rev2 날짜를 부여하지 않는다. 시공 PDF36/51은24.11.11 first draft design, CHECKED/APPROVED 공란이다. 승인 준공도·실측 길이로 승격하지 않는다.

## 2. I/O 및 HMI

### 2.1 직접 신호·메모리·시간부

| 신호 | 형식·주소 | 원본 선언과 위치 | 의미·경계 |
|---|---|---|---|
| VR06_Fbk | Bool, %I5.7 | live_index doc514; `0613` RID272, Input/AO47, NID45 UID2476 | 64KM1 보조접점 원시 응답 |
| Start VR06 | Bool, %Q4.6 | doc1301; `0602` RID187, Output/AO38, NID39 UID1090 Write; `0658` RID142 | 명령 출력. doc 주석 a53.6과 Address를 혼동하지 않음 |
| Flag.M_VR_06 | Bool, DB2.DBX3.0 | `0604` RID186/AO24/BO24, BAD2→`0603` Flag DB2; NID39 UID1088 Reset·1089 Read | 운전 요청. 실물 운전과 별도 |
| Allarm.VR_06_FAULT | Bool, DB3.DBX3.0 | `0604` RID184; `0657` RID145/AO24, BAD10→`0655` DB3; NID35 UID1209/1211/1212 | Set/Reset 유지 고장 |
| Inputs.VR-06 RUN | Bool, DB13.DBX5.7 | `0604` RID227/AO47, NID29/31 UID23; `0657` RID303 NID35 UID1241; DepDB DB13 | 처리 응답. 원시 I5.7과 별도 |
| Tag_78 | Timer, %T95 | doc1300; `0658` RID143 Timer/AO95, NID35 UID1206 Write/1207 Read | VR06 전용 S5 고장 타이머. HMI 태그 아님 |
| Flag.RESET_ALLARM | Bool, DB2.DBX6.0 | `0657` RID13/AO48, NID35 UID1210; `0655` Flag DB2 | 공통 Reset 요청. 재기동과 별도 |
| ON | Bool, %M0.0 | `0602` RID1, NID39 UID1084; `0658` RID1 UID1203 | 이름만으로 항상 TRUE 가정 금지 |
| Start ER-01 | Bool, %Q5.0 | doc1279; `0602` RID185 Output/AO40, NID39 UID1086 Read/NID41 UID1136 Write | VR06 Reset 조건이 읽는 ER01 출력 명령. 실제 가열 피드백 아님 |
| UNDER TESTING | Bool, %M5.5 | `0602` RID4 Memory/AO45, NID39 UID1087; NID1 UID40 Write | 유지보수 조건이 쓰는 내부 비트. 우회 사용 권고 아님 |
| hours motors.VR_06_MIN | Int, DB9.DBW176 | `0615` RID274/AO1408, NID45 UID2477/2479/2480/2485; `0614` DB9 | Add1·Move0 대상 |
| hours motors.VR_06_HOUR | Int, DB9.DBW178 | `0615` RID276/AO1424, NID45 UID2483/NID55 UID3095 Write | Move1·공통 Move0 대상. 총누계 확정 금지 |
| Tag_47 / Tag_48 | Timer, %T13 / %T17 | `0613` RID1/AO13, RID284/AO17 | 공통 분 타이밍·시간 기록 후Reset 관련 |
| Flag_Aggiorna_DB | Bool, %M1.7 | `0613` RID13 Memory/AO15, NID45 UID2486 | 공유 업데이트 요청. 영구 저장 완료 신호로 확정하지 않음 |

주소는 SAD 영역, SSD/AO·멤버 BO 비트오프셋, DepDBBlock TOD의 DB번호를 대조했다. 현재 프로젝트 최적화 DB·온라인 주소·실제 값은 미확인이다.

### 2.2 원시 입력→처리 응답과 다른 Writer

- LAD1070 `0397`, hmi inputs 색인1/NID1: Move35의 `in`에 ORef36/RID10 Tag_180이 W39로 연결되고, `out1`은 ORef37/RID11에 W40으로 연결된다. `0627` RID10 Word/Input/AO32=`IW4`, `0629` RID11 Word/AO32/BAD4와 `0628` Inputs DB13을 결속하면 IW4→DB13.DBW4다. I5.7/DB13.DBX5.7은 이 16비트 전달에 포함된다.
- Move22.eno→Move27.en(W34), Move27.eno→Move35.en(W41)의 앞단 허가가 있다. 해당 Move들의 DisableENO=true 속성·선은 확인했으나 실제 TIA 판본의 ENO 의미 및 현재 호출을 시험하지 않았다. 무조건 매 스캔 복사라고 쓰지 않는다.
- main LAD1613 `0030`, 색인2/NID19: Recipes Handler CRef21→HMI CRef23→HMI Output CRef25 ENO 연쇄(W31/32/33), CRef25.eno→NOT Simulation(1) Contact37(W42/44)→HMI Inputs CRef28.en(W43). CodeBlock29/RID135는 `0688` HMI Inputs, ORef45/RID140은 `0692` 선언이다.
- `0635` RID136/AO47에는 Inputs.VR-06 RUN의 NID4 UID84 Write가 남아 있다. 색인의 simulation LAD1085/0405에 대응하는 **정지된 자료 안의 다른 Writer 존재**만 기록한다. 시뮬레이터를 작성·수정·실행·시험하지 않았고 현재 활성 여부를 판단하지 않는다.
- 원시/처리 응답의 이름만 검색해 유일한 Writer라고 판정하지 않는다. 전체Word 전송, 정지 자료의 선언, 호출 조건, 외부 HMI/CPU 변경은 서로 다른 확인 대상이다.

### 2.3 HMI 주소 설정과 미결속

`sources/hmi_plc_tags.csv`는 dde.cfg 설정이며 온라인 현재값이 아니라고 명시한다. 직접 설정3행의 Access Name은 PLC다.

| 행 | HMI 태그 | 설정 주소 | 내부 ID | 경계 |
|---|---|---|---|---|
| 132 | VR_06\Allarme1 | DB11,X64.1 | 0032E | DB3.DBX3.0과 같은 주소가 아님 |
| 420 | VR_06\RispostaA | DB11,X64.0 | 001B7 | I5.7/DB13.DBX5.7과 별도 상태영역 |
| 455 | VR_06\Flag | DB2,X3.0 | 0018F | M_VR_06 주소와 일치. 버튼/권한/실제Write는 미확인 |

LAD1209 `0385`는 hmi 색인32/제목vr06이다. CRef22/RID638, 내부 CodeBlock23/RID1은 `0623` HMI Standard Motors와 `0624` 호출 인터페이스에 대응한다. network-map inferred_original_nid=null이며 다음4개 데이터 ORef를 이름 선언과 UID/RID/NID 일치로 결속하지 못했다.

| Wire | 원본 실제 핀 | 확보한 의미와 한계 |
|---|---|---|
| W21 | rail→CRef22.en | 호출 허가 연결 |
| W37 | ORef24/RID659→Ingresso_run | index_code는 Inputs.VR-06 RUN 후보. 이름 선언 결속 미확보 |
| W39 | ORef26/RID376→Allarme1 | index_code는 Allarm.VR_06_FAULT 후보. 결속 미확보 |
| W40/41/42/43 | ORef27/28/29/30, RID48→Allarme2/3/4/5 | `0626` FALSE literal·UID 호출 기록 존재. 최종NID 결속 별도 |
| W46 | CRef22.Risposta→ORef33/RID383 | Motors.VR06.Risposta 후보. 선언·주소 결속 미확보 |
| W48 | CRef22.Comulativo_allarmi→ORef35/RID385 | Motors.VR06.Allarme_comulativo 후보. 결속 미확보 |

HMI 설정행, 함수 호출핀, DB11 구조/함수 내부, 화면 이벤트는 별도 단계다. DB3 고장이 DB11,X64.1로 실제 갱신되었다거나 버튼이 운전요청을 썼다고 이 자료만으로 확정하지 않는다.

## 3. 고유 제어·호출·다른 쓰기

### 3.1 직접 운전 요청 해제와 출력

LAD1969 `0269`, motors1 색인40/NID39. Part8/Wire14를 VR06 원본과 대조했다.

| 기능 | 원본 Part/Wire/ORef | 정적 해석 |
|---|---|---|
| 허가 | rail W1113→ON Contact1103; ORef1084/RID1 W1091 | ON이 고장·ER01·출력 분기를 허가 |
| 고장 분기 | ORef1085/RID184→Contact1105(W1092), out→OR1074.in1(W1106) | VR_06_FAULT |
| ER01 분기 | ORef1086/RID185→NOT Contact1107(W1093); out→NOT Contact1109(W1108), ORef1087/RID4(W1094); out→OR1074.in2(W1110) | NOT Start ER-01 AND NOT UNDER TESTING |
| 요청 Reset | OR1074.out W1096→RCoil1079; ORef1088/RID186 W1098→operand | ON AND [FAULT OR (NOT ER01명령 AND NOT UNDER TESTING)]→M_VR_06 Reset |
| 출력 | ON1103.out W1104→Contact1111, ORef1089/RID186 W1099; out W1112→Coil1083, ORef1090/RID187 W1101 | ON AND M_VR_06→Start VR06 |

출력 분기에 ER01·NOT fault를 모두 직렬로 넣은 구조가 아니다. 별도 Reset이 요청에 영향을 준다. 선의 연결과 같은 스캔의 최종 출력·응답 시점은 구별한다.

### 3.2 ER01 조건과 유지보수의 소유

- VR06은 ER01의 Q5.0 명령을 읽는다. ER01 원시 피드백이나 히터 온도값을 직접 읽는 VR06 조건은 아니다.
- 명령 Writer는 LAD1971 `0271`, motors1 색인42/NID41: ON Contact1149→M_ER01 Contact1157(W1150/1145)→Inputs.177T1_OK Contact30(W1158/29)→Coil1129(W32), ORef1136/RID185(W1147)다. ER01 전용 허가·보호의 기능 소유는 ER01에 남긴다. `177T1_OK`의 이름/논리접점을 실제 정상극성·안전 온도 한계의 증거로 바꾸지 않는다.
- LAD1971에는 OFF, ER01_run, NOT FN-05 RUN AND NOT UNDER TESTING의 OR1120→RCoil1125 M_ER01도 있다. VR06에서 ER01명령이 꺼진 이유를 조사할 때 참조할 의존 경계다. FN05/ER01의 고장·타이머를 VR06 전용 규칙으로 합산하지 않는다.
- LAD1930 `0237`, 색인1/NID1: ON Contact47→Maintenance_ON Contact49(W48), W50→Coil34 UNDER TESTING 및 Coil36 Allarm.Maintenance_ON. ORef39/RID3=`Flag.Maintenance_ON` DB2.DBX7.5, ORef40/RID4=%M5.5다. 이 원문은 조건 설명이며 보호·시험 우회를 사용하라는 제안이 아니다.
- 원본 색인상 VR06 네트워크40은 ER01 네트워크42보다 앞선다. 같은 주기 ER01 계산 전 값 참조 가능성은 실행순서 검토 대상이다. 이것만으로 한 스캔 지연·최종 우선권을 확정하지 않는다.

### 3.3 VR06 응답이 다른 설비에 미치는 영향

| 대상 | 고유 원본 경로 | 판단 경계 |
|---|---|---|
| LD01 요청 | LAD1958 `0259`, 색인29/NID29. ON863 뒤 LD_01_FAULT Contact865→OR831.in1(W866); ORef23/RID227→NOT VR06 Run Contact22(W21), W24→NOT UNDER TESTING869→OR831.in2(W870); W855→RCoil836, ORef846/RID143 M_LD_01(W857) | ON AND [LD01고장 OR (NOT VR06 처리Run AND NOT UNDER TESTING)]→M_LD_01 Reset |
| LD01 진동기 요청 | LAD1961 `0261`, 색인32/NID31. ON925 뒤 LD_01_VIB_FAULT927→OR888.in1(W928); NOT VR06 Run22→NOT UNDER TESTING929(W24)→OR888.in2(W930); W913→RCoil891, ORef904/RID153(W915) | 같은 VR06 응답부재가 M_LD_01_VIB Reset 원인 중 하나 |

LD01 주출력에는 Inspection LS Contact873가 별도다. 진동기 출력은 M_LD_01_VIB 가지와 NOT 진동기고장933→Start_LD01Vib935의 병렬 OR894, 이어 Local Button Contact31(W25/30)→Coil900(W26)이다. **M_LD_01_VIB Reset을 진동기 출력의 무조건 OFF와 동의어로 쓰면 안 된다.** 내부 Local Start_LD01Vib 및 현장 버튼 경로는 LD01 소유이며 별도 검토가 필요하다.

### 3.4 다른 쓰기와 재시작 Word 덮어쓰기

VR06 직접 이름 선언13행을 전체 IdentXmlPart에서 추출했다. 그 중 M_VR_06의 명명된 LAD Write는 `0604` NID39 UID1088 Reset으로 확인됐다. 자동시동 블록의 VR06 명명 Set은 이번 선언 검색에서 확인되지 않았다. 이를 수동전용 확정, HMI 유일Writer, 또는 자동 시동 불가능의 증거로 사용하지 않는다.

| 저장부 | 추가 쓰기 원본 | 영향·제한 |
|---|---|---|
| DB2.DBX3.0 요청 | startup only LAD402 `0147`, 색인2/NID2. ON208→Move138.en(W209), Move138.eno→Move141.en(W187). ORef170/RID54 INT#0→141.in(W188), 141.out1→ORef171/RID9(W189) | `0563` RID9 Word/AO16/BAD6→`0562` Flag DB2 = DB2.DBW2. byte2~3 전체0은 VR06 요청bit3.0을 포함 |
| DB3.DBX3.0 고장 | startup only LAD403 `0148`, 색인3. ON329→Move250.en(W330), 250.eno→Move253.en(W306). ORef287/RID54 INT#0→253.in(W307), 253.out1→ORef288/RID26(W308) | `0563` RID26 Word/AO16/BAD23→`0562` Allarm DB3 = DB3.DBW2. byte2~3 전체0은 고장bit3.0을 포함 |
| DB13.DBX5.7 처리Run | LAD1070 `0397` IW4→DB13.DBW4 | byte4~5 전체 덮어쓰기. 독립된 BOOL 한 개 복사로 축소하지 않음 |
| DB13.DBX5.7 처리Run | 정지 자료 `0635` RID136 NID4 UID84 Write | Writer 존재만. 실행/활성/재현 미수행 |
| DB2.DBX3.0 요청 | HMI 설정455행 | 외부Write 가능 경계. 실제 이벤트·권한·활성Write 불명 |
| DB9.DBW178 HOUR | LAD1043 Move1 및 LAD1053 Move0 | 시간부 절 참조. 직접 알람·운전 요청과 별도 |

LAD403의 network-map NID는 null이다. 이번 대상 Word 경로는 `0047` ON UID284/RID1, `0048` INT#0 UID287/RID54, `0563` UID288/RID26가 모두 NID3인 선언과 BAD23/DB3를 대조하여 결속했다. 다른 블록의 동일 RID·UID 후보는 제외했다. startup only라는 블록 이름을 실제 전원 재시작 수행·현재 OB 설정의 증거로 쓰지 않는다. 호출·재시작 조건은 원 프로젝트/TIA에서 별도 확인해야 한다.

### 3.5 상위 호출의 경계

| 위치 | 원본 허가·호출 | 미확정 |
|---|---|---|
| main LAD1619 `0031`, 색인8/NID6 | ON Contact282.out W283→CRef264.en, 내부 CodeBlock275/RID58=`0688` Allarms1 | 실제 CPU에서 호출·중단/인터럽트 |
| main LAD1620 `0549`, 색인9/NID7 | ON350.out W351→CRef319 Motors1.en 및 CRef334 time work motor.en; CodeBlock337/RID67,347/RID82 | 원본 순서와 현재 실행·최종값 |
| main LAD1613 `0030` | Recipes/HMI/HMI Output ENO→NOT Simulation(1)→HMI Inputs | 전송 유효성·ENO·HMI 결속 |

이 조사에서는 런타임 실행·강제 출력·타이머 진행 시험을 하지 않았다. 명령·응답·Reset의 우선순위, 외부 쓰기, 재시작 후 잔존/초기 상태는 미확정이다.

## 4. 전기 전달 경로와 시공 자료

전기 PDF65/122/141/257, 시공 PDF36/51, P&ID p1의 서로 다른7페이지를 실제 렌더해 보았다. PDF번호와 FG를 구별한다.

| 경로 | FG/PDF | 원본 양 끝점·중간 경로 | 남은 경계 |
|---|---|---|---|
| 3상 주회로 | FG64/PDF65 | 8.3L1/L2/L3(63/9)→64QM1 1/3/5–2/4/6→64KM1 1/3/5–2/4/6→64U1/V1/W1 및 XM64U1/V1/W1→64QS1 1/3/5–2/4/6→M40 U/V/W, PE | 실전원·상순서·회전·모터/감속기 명판 |
| 출력 모듈 | FG140/PDF141 | CPU515 MOD15 A4.6 단자7→참조64/4→FG64 A4.6 | 실제 모듈형번·주소·출력전압 |
| 출력측 전원 | FG140/PDF141 | +24Vdc10.9→X21 3032 4A F 5×20→140.1→단자10; −0Vdc10.6→단자9 | 현행 퓨즈·전압·단자 |
| 접촉기 제어 | FG64/PDF65 | A4.6(140/1)→XS65→64QS1 보조접점→XS66→선64.1→64QM1 보조접점→64KM1 A1; A2→−0Vdc10.6 | QS/QM 보조 숫자단자는 명확히 확인되지 않음. 실물 극성·접점정상 여부 |
| 피드백 | FG64/PDF65 + FG121/PDF122 | +24Vdc10.7→64KM1 보조13–14→E5.7(121/7)→CPU515 MOD9 E5.7 단자18, 역참조64/6 | 접촉기 보조응답. 회전·배출·투입량과 다름 |
| 입력 모듈 전원 | FG121/PDF122 | +24Vdc10.7→X21 3008 2A IST.5×20→121.1→단자20; −0Vdc10.6→단자19 | 실제 전원·퓨즈·접속 |
| 모터 케이블 | 시공 PDF36/51 | 1_26 `=DUS+VR06-M40A`, CR→VR-06/M40. p36 DUST ZONE02, Route212RAD1의3번 Pipe16→M40. p51 경로100→200→210→211→212RAD1→E300 | 승인 준공·실제 길이·코어별 단자 결속 |

### 4.1 도면 정격·BOM 표기의 제한

- FG64의 M40은0.25kW/0.76A, 64QM1 범위0.7–1A, 패널 배선 BLACK FS17 1.5mm²다. 0.76A를 실제 보호기 설정이라고 단정하거나 설정변경을 지시하지 않는다.
- FG254/PDF257에서 64KM1은 Siemens `3RT2015-1BB41`, CONTACTOR3KW/1L/DC24V/S00, 부속 RC `3RT2916-1CB00`다. 이어 64QM1 행의 `3RV2901-1E`는 보조접점, `3RA1921-1DA00`은 결합부품, `WR32433`은 Whoner 어댑터, `3RV2011-0JA10`은 MAGNETOTHERMIC0.7–1A다. 각 수량1 표기다. 첫64QM1 행만 보고 보조접점 형번을 보호기 본체로 읽지 않는다.
- 원본은 현행 설치 Siemens/Whoner 제품 확인이나 ABB 대체품 승인서가 아니다. 제조사 매뉴얼·명판·승인자료 없이 모델대체·토크·정비주기·보호 한계를 채우지 않는다.
- 시공p51 케이블1_26은 Current Type GAC/CV/CORE4/SIZE1.5/SPARE0/Adjustment6/LEN118이다. LEN118은 문서 열값이며 실측길이·길이단위를 추가로 확정하지 않았다. p36 Pipe16은 관로 표기다.
- 시공p36에서 M32/M33·ER01·DUS2TB1·LT01·68FC1·PB14가 이웃한다. 같은 관로구역을 VR06 센서·부품 소유의 근거로 바꾸지 않는다.

### 4.2 단자와 상태를 합치지 않기

A4.6 명령, 코일 A1/A2, 주접점1/2·3/4·5/6, 보조13/14, I5.7 처리 응답은 각기 다르다. 출력1은 코일여자·접촉기닫힘·회전의 관찰 증거가 아니다. 입력1도 투입물 흐름/축회전을 보증하지 않는다. 도면상 접점 모양만으로 현행 정상극성·고장원인을 확정하지 않는다.

## 5. 알람·복구·시간 기록

### 5.1 VR06 전용 고장

LAD1813 `0447`, allarms1 색인33/NID35. Part9/Wire17을 원본 선언과 대조했다.

| 단계 | 원본 연결 | 정적 의미 |
|---|---|---|
| 허가 | rail W1239→ON Contact1227, ORef1203/RID1 W1213 | ON 공통허가 |
| 감시 | ON1227.out W1228→Start Contact1229, ORef1204/RID142 W1214; Start.out W1230→NOT Run1240, ORef1241/RID303 W1243; W21→SdCoil1191.in | ON AND Start VR06 AND NOT 처리Run |
| 지연 | ORef1205/RID28 W1215→1191.value; ORef1206/RID143 W1216→operand | `0656` S5Time S5T#2S, V512; `0658` Tag_78/%T95 |
| Set | Start1229.out W1230→Tag78 Contact1231, ORef1207 W1217; W22→SCoil1197; ORef1209/RID145 W1220 | ON AND Start VR06 AND Tag78 접점→VR_06_FAULT Set |
| Reset | ON1227.out→Reset Contact1235, ORef1210/RID13 W1222; W1236→fault Contact1237, ORef1211/RID145 W1223; W1238→RCoil1202, ORef1212/RID145 W1225 | ON AND RESET_ALLARM AND 고장→동일고장 Reset |

NOT 처리Run은 타이머 입력 가지에 있으며 Set 코일에 다시 직렬로 들어 있지 않다. S5Time V512는 원문 인코딩으로512ms가 아니다. TON T#2S와 임의로 같은 블록이라고 바꾸지 않는다.

### 5.2 Reset과 재기동·복구 구분

고장으로 M_VR_06이 Reset될 수 있다. RESET_ALLARM으로 고장만 내려가는 것과 운전요청 재생성은 별개다. ER01명령 조건·HMIWrite·재시작Word초기화·상위 실행순서를 같이 확인해야 한다. 같은 네트워크의 Set/Reset 동시조건 최종값은 이번 정적 조사만으로 확정하지 않는다.

복구 기록은 원인 제거, 현장 보호·전원·접촉기·기계상태, 명령/응답/표시 일치, 승인된 절차의 재요청·재발 없음 근거를 포함해야 한다. 알람창 소거 또는 bit Reset만으로 field_recovery를 완료로 표시하지 않는다. 본 작업은 Reset/재기동을 수행하거나 승인하지 않았다.

### 5.3 시간 기록의 Move1와 공통Reset

- LAD1043 `0330`, time work motor 색인42/NID45: Tag47 Contact2504→원시 VR06_Fbk Contact2506(W2505), out W2507가 Add2458.en과 Ge2465.pre를 허가한다. 처리 DB13이 아닌 I5.7을 읽는다.
- Add2458은 Int, ORef2477/RID274 MIN→in1(W2489), ORef2478/RID7 Int1→in2(W2490), out→ORef2479/RID274 MIN(W2491). `0616` RID7/V1과 대조했다.
- Ge2465는 MIN ORef2480/RID274(W2492)과60 ORef2481/RID8(W2493)를 비교, W2494→Move2468.en이다.
- Move2468.in은 ORef2482/RID7 **상수1**(W2496), out1→ORef2483/RID276 HOUR(W2497). HOUR+1 Add가 아니다.
- Move2468.eno W2498→Move2471.en, ORef2484/RID12 Int0(W2499)→in, out1→ORef2485 MIN(W2500), eno W2501→SCoil2474 Flag_Aggiorna_DB, ORef2486/RID13(W2502)다.
- LAD1053 `0340` 색인52/NID55: Tag48 Contact3111→Move3070 FN04 HOUR0→Move3073 VR03 HOUR0→Move3076 VR04 HOUR0→Move3079 VR05 HOUR0→Move3082 VR06 HOUR0의 ENO 연쇄다. VR06 앞단 W3108, Int0 ORef3094/RID12 W3109, out1→ORef3095/RID276 W3110을 확인했다. VR06만의 단독Reset 허가로 축소하지 않는다.
- LAD1056 `0019`, NID58: NOT Tag47 Contact3120.out W3121→SdCoil3112, value ORef3114/RID335=`0616` S5T#1M(W3117), operand ORef3116/RID1(W3119)다. 이름·시간상수는 확인됐으나 실제 펄스 주기·누락·영구 누계는 미확인이다.
- LAD1055 `0341`, NID57: ON3147→Flag_Aggiorna_DB3149→SCoil3110 MEM2_0; MEM2_0 Contact3151→NOT Flag_Aggiorna_DB3153→SdCoil3118, value ORef3128/RID334 S5T#5S, operand Tag48. MEM2_0 뒤 Tag48 Contact3155→RCoil3123 MEM2_0. 제목의 ‘DB 기록 후Reset’을 실제 저장완료 handshake로 간주하지 않는다.

HOUR0/1·MIN값만으로 총가동시간·정비주기를 계산하거나 Move1을 오타로 보고 PLC를 바꾸지 않는다. 외부 누적처리/기록이력·실행순서가 추가 자료다.

## 6. 증상별 관찰·수리 판단

아래는 자료 비교 지점이며 실제 현장작업 지시·보호우회·활선 측정·강제출력 시험이 아니다. 현장 확인은 자격자와 승인 안전절차로 한다.

| 증상 | 비교할 관찰점 | 원인 배제 근거 | 복구 판정 경계 |
|---|---|---|---|
| 요청을 줘도 곧 사라짐 | DB2.DBX3.0, VR_06_FAULT, ER01 Q5.0, UNDER TESTING, startup DB2.DBW2 | LAD1969 Reset의 두 분기, HMI실제Write/재시작 시각 | ER01명령과 실제 온도·가열 정상 구분 |
| 요청은 있는데 Q4.6이 없음 | ON, 현재 호출, 요청Write/Reset 순서, LAD1969 Coil | 현재 프로젝트 교차참조·동일시각 값 | 화면 표시만으로 출력 확정 금지 |
| Q4.6인데 모터가 안 돎 | MOD15 단자7, XS65/66, 64QS1/QM1, KM1 A1/A2, 주회로/M40 | 원본과 실물 결속·보호/전원/기계 상태 | 명령1이 회전 증거 아님 |
| 기동 후 VR06 고장 | Start, Tag78, I5.7, DB13.DBX5.7, 64KM1 13/14 | 2초 타이머 입력·Reset·Word전송/다른Writer 시각 | 알람해제와 원인제거·재기동 분리 |
| 원시입력과 HMI응답이 다름 | IW4→DB13.DBW4, 호출ENO, DB11,X64.0/64.1 | 미결속4 ORef, DB11구조, 통신·화면이벤트 | 표시 문제를 즉시 기계고장으로 단정 금지 |
| LD01/진동기 요청이 해제됨 | VR06 처리Run, UNDER TESTING, 각 LD01 고장·LocalStart/버튼 | LAD1958/1961의 각각 분기·대체 출력경로 | 진동기요청Reset을 무조건출력OFF로 쓰지 않음 |
| 가동시간이 비정상 | I5.7, T13/T17, DB9W176/W178, M1.7, 공유ENO | Move1/Move0, 외부저장/누적·값변경 이력 | 총시간·정비주기/설정 변경 추정 금지 |

실제 기록은 관찰자, 시각/시간대, 물리위치·온라인프로젝트 근거, 값/단위, 수집장치, 원본비교, 배제결과, 조치, 재요청·복구 근거가 필요하다. 운영기록·사진·SEJIN 자료를 이 조사물이나 공개저장소에 복사하지 않았다.

## 7. 네 기능·검증·완료 기준

### 7.1 네 기능과 기록 보존

| 기능 | 적용 방향 | 이번 검증 |
|---|---|---|
| 도면·래더 나란히 보기 | FG64 ↔ LAD1969/1813, FG121/140 ↔ 원시/처리Word전달 | 후보 근거 확보만. 제품 UI 구현·강조·왕복링크 미검증 |
| 백업·선택 복원 | VR06 고유키, note/repair_observation/미지필드·타설비 보존 | 미구현/미시험. 기존 지원을 추정하지 않음 |
| 기록 전후 비교 | 명령/응답·알람·시각/프로젝트 근거 분리 | 실제 저장·재읽기·재열기 미시험 |
| 관찰보고서/PDF | 작성시점 근거와 실제관찰시점 구별 | 원본PDF 읽기 렌더만 수행. 보고서생성 기능 검증 아님 |

0/빈칸, generated_with/saved_with와 실제 CPU/현장시점은 서로 다르다. 과거 기록에 새 근거를 소급 적용하지 않는다.

### 7.2 수행한 정적 조사

- 고정Git HEAD·VERSION·시작/종료Git상태 확인.
- preflight 읽기전용 종료0, 대장일치.
- XML 파싱, Global/Simple/Local 선언검색, Part/Wire/ORef·UID/RID/NID와 주소/상수 대조.
- 43개 명시적 XML/선언 정적 단언 통과. `extracts/VR06/static-review.json`에 항목별 결과가 있다. 시뮬레이션·행동시험·PLC실행 결과가 아니다.
- 직접 출력/고장/연동/시간부와 관련 호출·Word초기화의 서로 다른17개 LAD 네트워크 의미를 검토했다. HMI 데이터4 ORef는 미결속으로 유지한다. 전체프로그램 완전해석을 뜻하지 않는다.
- 실제PDF 시각검토7페이지. P&ID는 LD01/VR06구역과 개정란을 확대 재확인했다. 텍스트 추출만으로 접점/단자를 확정하지 않았다.
- 원본 파일 SHA-256과 고정커밋 Git blob 비교, 중지5자산 freeze 해시 비교는 별도로 부록에 기록한다.

금지 생성기, build-program-model.py/verify-virtual-plc.cjs, simulator 실행·시험, verify:manual/패키지재생성, npm test/build, UI·운영기록 조작은 실행하지 않았다. 문서조사 범위 밖이므로 미실행을 통과로 바꾸지 않는다.

### 7.3 미확정과 필요한 자료

1. 현행 VR06/M40 명판·모터/감속기·배치·부품 모델, 정비이력·준공도.
2. HMI4 데이터 ORef의 원프로젝트 선언 및 DB11 구조, HMI Standard Motors 내부/화면이벤트·쓰기권한/통신 매핑.
3. startup only 블록의 실제 OB호출/재시작 조건, ON·외부Write·ER01 선후 실행, 현재 CPU와 백업 비교.
4. 코일/보조접점·QS/QM·모듈단자·현장케이블 끝점과 정상극성의 실물 증거. 도면상0.7–1A와 실제 보호설정 구분.
5. 처리Run의 전체Word/다른Writer 유효성, 원시응답과 실제회전·물질흐름의 관계.
6. 시간 HOUR의 외부누적/영구저장·Reset handshake, 실제시간 단위/누락 및 정비기준.
7. 후속 문서 독립검토, UI/기록/보고서 구현·검증, 실제게시 및 별도 TIA/CPU/현장 확인. 이번 연구가 로컬2차133 통합승인은 아니다.

### 7.4 최종 상태

| 구분 | 상태 | 근거·한계 |
|---|---|---|
| documentation | draft_complete_with_gaps | 7영역, 고유 원본 근거·미확정 포함 |
| static_review | scoped_pass_with_unresolved_hmi | 43정적단언,17LAD 의미검토,7PDF페이지. 독립검토는 별도 |
| ui_records | not_run | 기능·저장·복원·UI 미시험 |
| publication | not_published | 초안 산출물만 |
| tia_compile | not_performed | Windows/TIA 미실행 |
| live_cpu | not_performed | 현재CPU/온라인 미확인 |
| field_recovery | not_performed | 실제관찰·복구없음 |

다음 작업은 부모가 이 초안의 고유 논리·Word덮어쓰기·전기끝점을 독립 대조하는 것이다. 미확정자료가 없다는 이유로 값을 채우거나 이미 검토한 보류를 반복 조사하지 않는다. 새 통합·배포는 별도 승인 범위에서 결정한다.

## 부록 A. 핵심 원본 위치

| 내용 | 원본 | LAD/색인/NID | 핵심 포인트 |
|---|---|---|---|
| VR06 직접제어 | 0269-FlgNet.xml + 0602/0603/0604 | 1969/40/39 | Part1079 Reset,1083 Coil; ER01명령 부정분기 |
| VR06 고장 | 0447-FlgNet.xml + 0655~0658 | 1813/33/35 | Sd1191,Set1197,Reset1202;2초/T95 |
| LD01영향 | 0259-FlgNet.xml + 0602~0604 | 1958/29/29 | VR06 Run22→NOT UNDER TESTING869→OR831 |
| LD01진동영향 | 0261-FlgNet.xml + 0602~0605 | 1961/32/31 | Run22→NOT929→OR888,출력대체가지별도 |
| ER01명령원 | 0271-FlgNet.xml + 0602~0604 | 1971/42/41 | M_ER01→177T1_OK→Q5.0 |
| 유지보수 | 0237-FlgNet.xml + 0602/0604 | 1930/1/1 | Maintenance_ON→UNDER TESTING |
| 시간부 | 0330-FlgNet.xml + 0613~0616 | 1043/42/45 | HOUR Move1 |
| 시간Reset | 0340-FlgNet.xml + 0613/0615/0616 | 1053/52/55 | Move3082 HOUR0,앞단ENO |
| 공통시간허가 | 0019/0341-FlgNet.xml + 0613/0616 | 1056/55/58;1055/54/57 | S5T#1M,기록요청/5초Reset경계 |
| HMI호출 | 0385-FlgNet.xml + 0623/0624/0626 | 1209/32/미확정 | 4데이터ORef 미결속 |
| 원시전달 | 0397-FlgNet.xml + 0627~0629 | 1070/1/1 | IW4→DB13W4 |
| 요청Word초기화 | 0147-FlgNet.xml + 0047/0048/0562/0563 | 402/2/2 | DB2W2←0 |
| 고장Word초기화 | 0148-FlgNet.xml + 0047/0048/0562/0563 | 403/3/선택선언NID3 | DB3W2←0,색인NID null보존 |
| 상위호출 | 0030/0031/0549-FlgNet.xml + 0688/0692/0694 | 1613/2/19;1619/8/6;1620/9/7 | ENO/Simulation접점/ON 허가 |

`extracts/VR06/`에는 자기설비용 선언검색 결과·직접네트워크/관련네트워크 Wire추출·PDF렌더·정적단언 결과가 있다. 추출파일은 원본을 대신하지 않는다.

## 부록 B. 원본 바이트 보존 해시

대상 70파일의 작업 사본 SHA-256과 고정커밋 Git blob SHA-256이 모두 일치한다. 중지5자산은 freeze 지정해시에도 모두 일치한다. 시작·종료 원본 Git 변경0. 이 수는 바이트 보존 대상 수이며 의미 검토한 네트워크 수나 완료 설비 수가 아니다. 별도로 17LAD 범위의 정적 의미검토, 43개 XML/선언 단언, 7개 원본PDF페이지 시각검토를 수행했다.

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
| `all-in-one/sources/decoded-original/0147-FlgNet.xml` | `386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c` |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` |
| `all-in-one/sources/decoded-original/0237-FlgNet.xml` | `ad3721660c2f357e76c1a351f7898691271f35c341efe775e5780d749b2c4aa0` |
| `all-in-one/sources/decoded-original/0259-FlgNet.xml` | `872a7149ef118f82addce8b038d42418f532c065f2191018d85aed93406dd8b5` |
| `all-in-one/sources/decoded-original/0261-FlgNet.xml` | `2cb282a051d3767e256d319453453499c5cc339b725ed78e3e263466f0ef8498` |
| `all-in-one/sources/decoded-original/0269-FlgNet.xml` | `e9aad7857b267d425d4e23a03e2e7e2ebdbdebb558fef2e08e5be4c2c96c0d37` |
| `all-in-one/sources/decoded-original/0271-FlgNet.xml` | `7f913249a7879930d8443291b542374887e8cbbe89b55993a51233446008521b` |
| `all-in-one/sources/decoded-original/0330-FlgNet.xml` | `4fa97e4acad5d8c1e67137332a0ee61e88926fd57293a4130fddedcc83dce88c` |
| `all-in-one/sources/decoded-original/0340-FlgNet.xml` | `00acb073128337e7d7b95bbedeb50cd0e72c89772d835bdf392da17b3e2d0add` |
| `all-in-one/sources/decoded-original/0341-FlgNet.xml` | `e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96` |
| `all-in-one/sources/decoded-original/0385-FlgNet.xml` | `00ebc92b12b57c2015eb0142f2e40f989e65958d4adf0875f1242beb3c7ad878` |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` |
| `all-in-one/sources/decoded-original/0447-FlgNet.xml` | `ab9a755ce0fe76d8890626f5101bd0ca4c13ff25a3cdee3e506fd4bc510f9f1e` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` |
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
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` |
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


## 전달 전 핵심 근거 제한 대조
2026-10-11 고유 제어 Part/Wire 및 모터 회로의 실제 PDF 렌더를 표본 재확인하고 인용 원본 SHA256을 모두 재계산하여 일치했다. 이는 전체 원본 의미 검토 또는 현재 CPU/현장 검증이 아니다. 사용자 독립 검토 및 미확정 경계를 유지한다.
