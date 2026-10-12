# LS23 — MV01 개방측 리미트 고유 원본 조사

- 기준: GME-STD-1.0.0, 2026-10-11 UTC. 고정 원본 `source-mv06` commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 독립 검토 전 초안, documentation=complete_with_gaps.
- 대상은 LS23 한 개, parent MV01. `INVENTORY.json#/catalog/236`, TASK3-BATCH23-SCOPE와 GME-CATALOG-OVERLAP-REVIEW의 LS23행을 대조했다. component/하위 구성품/depth1/phase2/planned/baseline/not_assessed, parent_child_separate, physical_identity_verified=false. 부모 및 LS24/ZT02 완료를 상속하지 않는다.
- 원본 AGENTS, 저장소 skill, WORK-STANDARD, WORK-ITEM-TEMPLATE, 최신 인계 상단·VERSION·ACTIVE-WORK를 읽었다. 이전 배치의 PV/실린더 언급보다 이번 scope를 우선한다. 모델/추론 UI 설정은 미확인.
- 변경은 본 MD와 `extracts/LS23/`뿐. 원본·공통 코드·버전·대장·배포·PLC·현장·보호값·SEJIN 변경 없음. 시뮬레이터 작성·수정·생성·실행·행동시험, 앱 빌드/원본 생성기 실행, 업로드/새 Work/재위임 없음.
- 부모 MV01 및 ZT02 초안은 탐색색인/공통근거로 재사용했다. 부모 전체를 반복 의미검토하지 않았다. 아래 원본 XML/선언·4개 PDF 페이지의 LS23 고유 부분을 직접 대조했다.

## 1. 설비·자료 기준 — 적용

핵심 대응은 **LS23 → MV01 개방측 위치 리미트 → E8.1/I8.1 → Inputs.MV01 Open DB13.DBX8.1**이다. 이름만으로 정한 소유가 아니다. P&ID PDF1의 MV-01/M20·LS-23/LS-24·ZT-02 인접 리더와 OEM FG45의 MOTORIZED VALVE MV-01/LIMIT SWITCH VALVE OPEN/LS-23, FG124의 LS-23/E8.1을 함께 확인했다. HE01 부근 배치와 공유 단자함은 부모를 HE01로 바꿀 근거가 아니다.

| 직접 시각 검토 원본 | 실제 페이지·개정 | 확인·한계 |
|---|---|---|
| `all-in-one/sources/PID_1684n002I.pdf` | PDF1, 1684n002 Apex I, 기본06/04/2011, I행15/01/2013 REMOVED MC-05, CHANGED POWER OF FN-02 | MV01/M20·LS23/24·ZT02 배치. PLC주소·정상극성 없음 |
| `all-in-one/sources/Electrical_Rev2.pdf` | FG45/PDF46, 27.05.2024, 개정란 공란 | LS23 개방측, NC기호 11/12, X1/112·113, E8.1 |
| 같은 OEM 원본 | FG124/PDF125, 기본27.05.2024, **Rev2 17.03.2025** | DIGITAL INPUT MODULE, CPU515 MOD10 단자2 E8.1 LS-23 |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | PDF57, CANDC-CONS-C007-057, D-PAGE7/TOTAL57/64, Rev1 24.11.11 first draft design | 케이블7_1 공통·7_8 전용. 준공·실측으로 승격하지 않음 |

파일명의 Rev2를 FG45의 페이지 개정으로 덮어쓰지 않는다. NC 도면 기호, 기계 개방 위치, 입력전압, raw Bool, PLC 접점 반전은 서로 다르다. 현재 실물 캠/모델·정상극성은 미확정.

이하 네 자리 원본은 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 `NNNN-IdentXmlPart.xml`이다. LAD는 탐색색인의 문서번호이며, NID/UID/RID는 원본 선언 문맥이다. 서로 다른 파일의 같은 RID를 임의 결속하지 않는다.

## 2. I/O·HMI·기억값 — 적용 / 일부 미결속

| 계층 | 주소·정체 | 원본 근거·경계 |
|---|---|---|
| 원시 센서 | I8.1 Bool, mv01_open | `all-in-one/registers/plc-symbols.csv` doc889/_7ev, comment limit switch ls-23; FG45→FG124. 같은 이름의 SimpleAccess 개별 Bool 선언은 이번 검색에서 미확보. CSV를 선언 XML로 바꿔 말하지 않음 |
| 원시 word | IW8, Tag_181 Word | 0627 SimpleAccess RID15/NID1 UID47, SAD Input AO64 |
| 처리 word | DB13.DBW8 | 0629 GlobalAccess RID16/NID1 UID48 AK Write, Word AO64/BAD4;0628 DepDBBlock RID4 Inputs TOD13 |
| 처리 리미트 | DB13.DBX8.1 Inputs.MV01 Open Bool | 0619 RID172 AO65 BAD168, NID1 UID159/174;0618 Inputs RID168 TOD13 |
| PID 문맥 | 같은 DB13.DBX8.1 | 0668 RID125 AO65 BAD118 NID8 UID391;0666 Inputs RID118 TOD13. 위 RID172와 동일 번호로 취급하지 않음 |
| HMI 설정 | MV_01\LimitSwitchOpen → DB11,X18.3, ID00316 | `sources/hmi_plc_tags.csv`, Access PLC. 통신·쓰기·화면 이벤트·현재값 확인 아님 |
| 다른 처리값 쓰기 | DB13.DBX8.1 | 0635 RID234 AO65 BAD5, NID2 UID152 AK Write;0634 Inputs RID5 TOD13. §3.4 |

LS23 고유 S/R 위치기억 선언은 지정 범위 검색에서 확보하지 않았다. DB13 처리 메모리·DB11 HMI 표시층·DB2 수동 요청은 별도 역할이다. PV계 MEM_OPEN/CLOSE나 ZT02 DB8 카운트 저장을 LS23 위치기억으로 복제하지 않는다. 전체 PLC에서 기억값이 전혀 없다는 부재 증명도 아니다.

### HMI 핀의 미확정 유지

0367 LAD1190: CRef22/RID639, CodeBlock23/RID130는 HMI Standard Motorized Valve 호출(0624/0623). W56 ORef33/RID691→CRef22.Limit_switch_Open, W64 CRef22.Limit_Switch_Open_HMI→ORef41/RID430를 직접 확인했다. 그러나 NID 및 RID691/430의 동일 문맥 Global 선언 결속은 확보하지 못했다. 따라서 DB13.X8.1→DB11.X18.3의 완전 연결을 주장하지 않는다. 부모의 10핀 미결속은 유지하며 이름/순서로 보완하지 않는다.

## 3. 제어 구조 — 적용 / 정적 확인 한정

### 3.1 원시 입력 word 전달·호출 경계

0397 LAD1070 hmi inputs/NID1: Move43.in은 W55/ORef47/RID15(IW8), out1은 W57/ORef48/RID16(DB13.DBW8). en은 W53 Move42.eno이다. Move43 원문은 **DisableENO=true**이며 W56은 Move43.eno→Move44.en으로 그려져 있다. 접속 사실과 실행 ENO 의미를 구분한다. 이 word 복사 자체에는 비트 반전이 없지만 DB13 최종값의 유일한 writer는 아니다.

0030 LAD1613/main NID19: HMI Output CRef25.eno→W42→Contact37.in, Contact37은 Negated operand(W44/ORef45/RID140), W43→HMI Inputs CRef28.en. 0692 RID140 Simulation(1) SAD Memory AO1440=M180.0. 선행 Recipes/HMI/HMI Output ENO 사슬은 부모 공통 색인 참조. 호출조건과 다른 쓰기가 있으므로 raw/DB13 값을 무조건 동일시하지 않는다. 이 원문을 정적으로만 읽었고 중지 기능을 실행하지 않았다.

### 3.2 개방 요청 해제와 개방 출력의 반대 극성

0342 LAD1702 Valve Control loop/NID1:

- 정접점: W186 ORef159/RID172→Contact230.operand. ON226→ON228의 W229 공통 다음 Contact230.out W231→OR115.in1; OR115.out W189→RCoil119, operand W191/ORef162/RID8. 0619 RID8 Bool AO27/BAD5 + 0618 Flag TOD2이므로 **M_MV01_OPEN DB2.DBX3.3** 요청을 Reset한다. 다른 OR 가지 Close요청232/Auto234도 있으므로 LS23만이 해제 원인이라고 하지 않는다.
- 반전접점: W209 ORef174/RID172→**NOT Contact256.operand**. NOT 반대방향Q Contact254.out W255→Contact256.in; Contact256.out W257→NOT ResetProc Contact23→W25→Coil143. Coil143 operand W211/ORef175/RID15;0617 RID15 SAD Output AO20로 **Q2.4 Start Open MV-01**이다.
- 따라서 처리 리미트는 요청해제에서 정접점, 최종 개방 차단에서 반전접점이다. 원문 조건 전체는 부모 공통근거의 ON·NOT FAULT·Auto/PID 또는 수동요청·(PULSE OR ON)·NOT Q2.5·NOT InputsOpen·NOT ResetProc를 유지한다. 리미트 하나로 기계 작동/정지 성공을 단정하지 않는다.
- 0032 LAD1621/main NID8: Contact352(ON, W350/ORef345/RID52)→W353 CRef341.en. 0692 RID52 Memory AO0=M0.0;0688 RID85 FC Valve Control loop/TOD14. ON 심볼을 현재 TRUE 상수로 간주하지 않는다.

### 3.3 PID 상한 입력: 이 LS23 접점에는 반전이 없음

0477 LAD11/NID8: W415 ORef390→ON Contact467; W468→Contact469.in. **W416/ORef391/RID125→Contact469.operand는 정접점**이다. Contact469.out W470→OR348.in1. OR348.out W422→LRef366.CONT_S의 **LMNR_HS**. 별도 OR 입력은 ON→OFF Contact471→Ge352(Data.Pot_MV01≥100)의 W420이며 LS23와 다른 경로다. LRef366 RID113(0671), Instance412 PIDMV01 DB21(0665 RID71).

상한 입력은 `(ON AND Inputs.MV01 Open) OR (ON AND OFF AND Pot_MV01≥100)`이라는 정적 연결이다. COM_RST의 NOT Auto와 LS 접점의 반전을 혼동하지 않는다. OFF는 M0.1 심볼이며 현재 FALSE 보장이나 숫자100의 현장 개도%/보호설정 근거가 아니다. 부모 PID 9핀 미결속·현재 인스턴스·스캔 및 모드 미확정은 그대로 둔다. 인접 MV02의 반전 리미트 식을 복사하지 않는다.

### 3.4 다른 쓰기 — 중지 원문 보존용 정적 검사만

0403의 NID2에서 Powerrail W21→**Ge342.pre**. W346/ORef343/RID248(0635 Data.Pot_MV01 Int AO1184, BAD247;0634 Data TOD1)→Ge342.in1; W347/ORef344/RID253(0637 Int **98**)→in2. Ge342.out W149→일반 Coil151, W150/ORef152/RID234→Inputs.MV01 Open(DB13.X8.1).

즉 보존된 simulation 블록 원문에는 위치 처리값 비교로 같은 DB13 비트를 쓰는 경로가 존재한다. 이는 실제 LS23 접점 입력도 아니고 현장 리미트 설정98도 아니다. 실행·모델 작성·수정·생성·행동시험은 전혀 하지 않았다. 존재 확인은 해당 블록이 현재 CPU에서 호출되거나 최종값을 덮는다는 증명이 아니다. 현재 호출순서/외부 HMI/간접주소 및 모든 writer의 전수 검증은 미완료다.

## 4. 전기 양 끝점 — 적용

FG45/PDF46과 FG124/PDF125를 직접 렌더 확인:

| 시작→끝 | 원문 식별자·교차참조 | 판정 |
|---|---|---|
| +24Vdc10.7→X1/112 | 상부44/9에서 들어와46/3으로 계속, X1/112에5×20 2A F | 도면상의 공급/퓨즈. 현행 보호값으로 승인하지 않음 |
| X1/112→LS23 | 선45.3→LS-23 접점11/12, NC기호 | LIMIT SWITCH VALVE OPEN. 캠의 실제 위치·정상극성 미확정 |
| LS23→PLC | X1/113→E8.1, FG124/2;반대쪽FG124는45/5 | CPU515 MOD10 단자2, E8.1 LS-23 직접 끝점 |
| 인접 구분 | LS24=X1/114·115/E8.2 단자3;ZT02=X1/107~111 | LS23에 닫힘 리미트·엔코더 회로를 합치지 않음 |

시공 PDF57 Rev1의 두 경로:

| 행·케이블 | FROM→TO | 원문 설계값 |
|---|---|---|
|7_1 `=FLA+HE01-FLO2TB1A`|CR→HE-01 FLO2TB1|LS17/18/23/24/21A/22A/21B/22B 공통, DC/CVV/25G/1.0/spare8, route100·110 LAD1·E100, adjustment5,LEN50|
|7_8 `=FLA+MV01-LS23A`|HE-01 FLO2TB1→MV-01 LS-23|DC/CVV/2C/1.0/spare0, routeE110, adjustment5,LEN5|

공통 케이블의 여러 LS 표기를 단일 실물로 병합하지 않는다. 2C는 실측 도체/단자 배정 증거가 아니며 OEM X1과 현장 FLO2TB1의 개별 단자 대응은 이 표에 없다. 준공판·양끝 표찰/단자표가 필요하다. OEM/시공 설계본의 일치와 현재 설치 확인은 다르다. EV69KA/71KA 부하5–9 정정은 보존하되 관련 없는 EV 회로를 LS23에 만들지 않는다.

## 5. 알람·복구 — 부모 경계 적용 / 고유 검출 근거 미확보

LS23 전용 단선/불일치/장시간 알람, 타이머, S/R 유지 래치를 고유 신호로 확보하지 않았다. ‘알람이 전혀 없다’는 전체프로그램 부재 주장도 아니다.

MV01 초안의 Allarm.MV01_FAULT DB3.DBX4.7은 부모 Q/접촉기응답 불일치 T4 S5T#150mS와 방향명령 누적 W33>2000/W34<−2000이 공유하는 래치다. 이를 LS23 전용 검출·전행정 시간·센서 응답시간으로 복제하지 않는다. 이번에 그 알람 네트워크 전체를 다시 검증하지 않았으며 부모 설명은 공통 색인 참조다. ZT02 위치 OFR도 LS23 소유로 바꾸지 않는다.

리미트 변화, 요청 Reset, Q출력 해제, 알람 Reset, 물리 정지/복구는 별도 증거다. 정상극성·현장 복구는 미확정이며 ResetEncoderProcedure는 구동 영향을 갖는 부모 절차이므로 센서 확인용 리셋으로 안내하지 않는다.

## 6. 증상별 관찰 — 적용 / 현장 실행 아님

아래는 이미 승인된 안전 관찰 자료를 받기 위한 기록 항목이다. 활선 측정·점퍼·강제출력·캠조절·재기동·교정을 수행하거나 권고하지 않는다.

| 증상 | 비교할 위치·값·시각 | 원인 배제·판정 경계 |
|---|---|---|
| 개방 위치인데 표시가 다름 | LS23 표찰/캠 위치 사진, X1/112·113 및 MOD10단자2 식별, raw I8.1,DB13.X8.1,DB11.X18.3 동시각 | 도면 NC=개방1로 단정 금지. 배선/극성/처리 writer/표시층을 분리 |
| raw와 처리값 불일치 | IW8→DB13.W8 복사 호출, M180.0 조건, 0403 쓰기 존재, CPU프로젝트/스캔 정보 | 현장 리미트 불량으로 바로 단정하지 않음;모드/다른쓰기 증거 필요 |
| 개방 요청이 사라짐 | DB2.X3.3 요청, InputsOpen 정접점230, Close요청/Auto OR 가지와 시각 | 요청 해제=센서 정상/기계 끝점 도달 아님 |
| 개방 출력이 안 나옴 | NOT Contact256 처리입력,반대Q·Fault·ResetProc·모드·요청·공유허가 | 리미트만 원인으로 단정하지 않고 부모 허가/출력 사슬과 비교 |
| 자동 상한 제한만 이상 | InputsOpen,ON/OFF,Pot_MV01 비교가지,LMNR_HS·현재PID 상태 | PID경로에는 LS 반전 없음. 100/98 설정 변경 금지 |
| 부모 Fault만 표시됨 | 접촉기응답/부모누적/리미트/엔코더 각 시계열·발생시각 | Fault를 LS23 고장코드로 오인하지 않음 |

관찰기록 필수: 관찰자·시각/시간대·수집장치·프로젝트 판본·위치·값/단위·비교근거·배제결과·승인된 조치·별도 복구확인. 운영기록/사진을 공개 저장소에 복제하지 않는다.

## 7. 완료·누락·인계 — 적용

| 구분 | 현재 상태·필요 자료 |
|---|---|
|문서|complete_with_gaps, 7영역 고유 초안 작성. 독립검토 전 |
|정적 의미검토|7 FlgNet의 지정 경로, 선택 선언 문맥, 4개 실제 PDF 페이지 직접 확인. 전체부모/전체PLC 전수검토 아님 |
|보존 해시|선정32원본 SHA256·고정Gitblob 바이트일치32/32. 해시32는 의미검토32 또는 전체원본 보존검사 수가 아님 |
|HMI·기억|HMI RID691/430 동일문맥 미결속, LS23 고유 기억태그 미확보. 정식 export/화면이벤트·교차참조 필요 |
|현장/CPU|실물 LS23 형번·캠/정상극성·준공단자·현재CPU/프로젝트·모든writer/호출순서 미확정 |
|ui_records|not_run: 화면·저장·재열기·선택복원·보고서 검증 없음 |
|publication|not_published: 앱반영/배포하지 않음 |
|tia_compile/live_cpu/field_recovery|모두 not_performed |

네 기능(도면·래더 비교/백업 선택복원/기록 전후비교/보고서PDF)은 LS23 전용 구현·검증 미수행이며 본 문서·PNG가 기능완료 증거가 아니다. note/repair_observation·미지필드·타설비 기록·초안·저장키를 변경하지 않았다.

읽기 전용 preflight는 inventory_matches=true, 대장248/phase2 133. requirements-audit.json 및 all-in-one-data.json 두 source_byte_changes가 표시되었으나 대장 일치와 별도인 기존 바이트 차이이며 고정원본을 수정하지 않았다. 큐검사 통과를 문서/현장 완료로 세지 않는다.

다음 한 작업: 부모가 본문·선정해시·검사JSON을 독립검토하고, 신규 현장 증거가 없으면 정상극성/HMI 결속을 미확정으로 유지해 인계한다. 다른 설비 자료를 대신 반복 조사하지 않는다.

## 부록 A. 선정 원본 SHA256 / 고정 Gitblob 전체 표

| 원본 경로(source-mv06 기준) | SHA256 | Gitblob SHA1 | 바이트 일치 |
|---|---|---|---|
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc | 587c3748ad9224718f95ba06463fee913dae231d | True |
| all-in-one/registers/plc-symbols.csv | a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f | cbc576c5d6e47498a3865304a1c23de9b4641d9f | True |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 | cf4c0650e7c7baac350dcb89909b808435704880 | True |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b | 8c83a59fefd5b8b651ec3537ea4236a073f5e109 | True |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 | f610fd7c7ce14ae951b00cff57b969259bfb389d | True |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd | 0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8 | True |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b | e74c70b751acdcdbc7a8b3b0c98aa773c2107cab | True |
| all-in-one/sources/decoded-original/0032-FlgNet.xml | 070bb8efa33d03b18add5da81d3f670a47c12b288076b7bfee11ac87fe6fa7e4 | e31cf9aeecfbfc0c264921ac217cbd15479c1f34 | True |
| all-in-one/sources/decoded-original/0342-FlgNet.xml | 9ef93abad16cc055509ef98c388417c716cb03d23cb02aed6d95888beb43bef8 | a9b1841964216331887d18f91c014c0534cc9df1 | True |
| all-in-one/sources/decoded-original/0367-FlgNet.xml | 7e1a0c6776177463d5ffe7307a991484f97e8e5c5863f00d9597950458482bc5 | fc6017ddea1f08526c317d5f76b3ae3ca98c02e4 | True |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 | 4ab8370493c4e28fc1eabeeebe2743d27f0c4021 | True |
| all-in-one/sources/decoded-original/0403-FlgNet.xml | 77b03e38aa857ac8dd404f2f66a56256939b4e7924b41334a7981b86089c1e6b | 4c806e31eb65f00cbb7870c72896ac26a8bc3dd3 | True |
| all-in-one/sources/decoded-original/0477-FlgNet.xml | e7b5b0cb95c60d1112081f6129a3127f8413e1b1d2a4c67d0e203d36ea0a711a | 8bc2088bf4bb5eb8d51e0d9186879fc61d2c27df | True |
| all-in-one/sources/decoded-original/0617-IdentXmlPart.xml | 10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9 | 9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e | True |
| all-in-one/sources/decoded-original/0618-IdentXmlPart.xml | 0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c | 9eec0dbd8abde4aa7295f77b63ad473f895f274b | True |
| all-in-one/sources/decoded-original/0619-IdentXmlPart.xml | 85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456 | 11f0502c84a1f319a21459a35c0dc1c6ce8e8f36 | True |
| all-in-one/sources/decoded-original/0623-IdentXmlPart.xml | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 | 13b3af0459c8e6069bb9b2f1b16454bf479e08dc | True |
| all-in-one/sources/decoded-original/0624-IdentXmlPart.xml | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a | 02511fea47fc47981c101bba49dc40adde1cdcc3 | True |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb | 61ebc0abbb2ca160e11e1da400a3f14a397d8bc5 | True |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd | 170ca5c72599edc7ea7eefe651c3680ce325e76a | True |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 | 058129bb01e27f7a6a0d0293f332d745e5bab74e | True |
| all-in-one/sources/decoded-original/0634-IdentXmlPart.xml | af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d | 877d9e0734dc7f3e5a8cea789eeb58a208501f48 | True |
| all-in-one/sources/decoded-original/0635-IdentXmlPart.xml | 1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457 | 95bfcad59cfb0c12b573e9e8face4262d1e94622 | True |
| all-in-one/sources/decoded-original/0637-IdentXmlPart.xml | 3fb68f57dbe2a877c4ad5aa1b3316810cf84958f2d13b5b1d7d321e0915271c7 | cb1d7fb76aa2afd96eb46984cc1e71b77f36395c | True |
| all-in-one/sources/decoded-original/0665-IdentXmlPart.xml | 50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd | ea4a8a5013081f648722c5ebbde3bb1366787990 | True |
| all-in-one/sources/decoded-original/0666-IdentXmlPart.xml | 19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6 | b6130b32498b6fee0d9e4db7a04dc79f785e1fbb | True |
| all-in-one/sources/decoded-original/0667-IdentXmlPart.xml | ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3 | 7f2e1798eb9f260d19d038a83369484d0f438856 | True |
| all-in-one/sources/decoded-original/0668-IdentXmlPart.xml | 2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed | fe0f30d1eaae37783b0f03cb090353b3a3de3600 | True |
| all-in-one/sources/decoded-original/0670-IdentXmlPart.xml | e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841 | b9466007b14e5c4f5d353dca5734401317e2dc03 | True |
| all-in-one/sources/decoded-original/0671-IdentXmlPart.xml | 26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293 | e38a4e2c93ac8093e2b0b8e082a64688b5d9845e | True |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda | 463585759f1ecd94f32362b4fefb000a152f5773 | True |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 | 737785d03b5fad43c5b4d451955726d800edb1c0 | True |

## 부록 B. 검사·원본 보존 기록

- 검사시각 2026-10-11T13:49:42.869103+00:00 UTC, `extracts/LS23/VALIDATION.json`: 정적 단언15/15 통과, 원본 Git status 깨끗함.
- `SOURCE-SHA256.json`: 선정32원본의 SHA256·Gitblob·바이트 수와 일치결과. 저장소 전수 해시검사나 전체 의미검토라고 표시하지 않는다.
- 실제 렌더4쪽과 P&ID 제목 확대, 지정 FlgNet7개의 정적 trace, 선언 검색·선정 subtree가 `extracts/LS23/`에 있다. 초기 선언검색에서 XML namespace 때문에 빈 결과가 나왔고, namespace를 정규화해 다시 검색하여 선언을 확보했다. 원본을 바꾸지 않았다.
- `preflight.json`은 대장만의 읽기 전용 검사다. 검사와 PDF/XML 추출은 로컬 보조 분석이며 PLC 프로그램·원본 생성기·시뮬레이터·앱을 실행하지 않았다.
