# LS06 밸브 위치 리미트 스위치 — 고유원본 조사 초안

- 대상: LS06 / PV01 하위 component / phase2 / parent_child_separate. 별칭 ls-06, ls.06. 다른 LS 번호·CYL·CLIENT와 병합하지 않는다.
- 고정 원본: source-mv06, abcf31c5030bc7ef8749ed8e869a857f2387a28a, VERSION 1.12.0. GME-STD-1.0.0. 조사일 2026-10-11 UTC.
- 상태: documentation complete_with_gaps. 한정 원본 정적 검토 완료; 독립 검토 대기. 통합/UI/게시/TIA/현재CPU/실물/현장복구 미검증. 실행 모델·추론 설정은 관측 불가로 미확인.
- 작성 범위: drafts/LS06-DOTS-DRAFT.md와 extracts/LS06만. 원본·코드·PLC·현장·보호값·SEJIN 변경 및 앱빌드/생성기/시뮬레이터 생성·수정·실행·행동시험 없음.

## 1. 설비·자료 기준

[E01] INVENTORY.json catalog[223]와 all-in-one/registers/equipment.json[211]은 LS06의 부모를 PV01로 명시한다. electrical_fgs=[69,70]는 대장 참고 범위이며 센서 실제 회로는 FG70, PLC 입력 끝점은 FG125다. BATCH21 범위와 GME-CATALOG-OVERLAP-REVIEW.json catalog_rows의 parent_child_separate·physical_identity_verified=false를 유지한다. baseline이나 부모 완료 상태는 본 LS의 실물 확인·BC01 동등 기능 완료가 아니다.

[E02] PID_1684n002I.pdf 실제 PDF1 PV-01 Detail의 LS-06 리더선은 EV-02가 구동하는 CL-03 그림의 몸체/피스톤 쪽에 닿으며 LS-05 리더는 그 반대쪽에 표시된다. EV02 계통은 CL03 및 CL04를 함께 그린다. 별도 GATE A/B 기계 형상 그림에는 LS06→특정 실물 위치를 결속하는 선이 없으므로 문자 배치만으로 위/아래 게이트·실린더 행정 방향·실물 설치를 확정하지 않는다. LS06로 CL04의 별도 행정까지 증명하지 않는다.

P&ID 표제: UBC AND SCRAPS DECOATER 10 Ton/h, Drawing 1684n002, Apex I, 기본 06/04/2011, 최종 I 15/01/2013, 설명 REMOVED MC-05, CHANGED POWER OF FN-02. 원본 전체와 회전 확대 렌더로 확인했다. 최신 준공도라는 증거는 없다.

PV01-DOTS-DRAFT 및 CYL-CL03-DOTS-DRAFT는 공통 색인으로 재사용했다. 부모 출력·전체 순서·알람을 반복 조사하거나 LS06 전용 로직으로 복제하지 않았다. 공유 EV 부하 접점은 WORKSPACE-HANDOFF의 v1.11.1 정정 69KA/71KA 5–9를 유지한다. 구 PV01 초안의 1–9는 채택하지 않으며 LS06 접점13/14와 EV 중계 접점5/9는 다른 회로다.

## 2. I/O·HMI

아래 주소는 백업 선언이며 현재 CPU 주소/실물 정상극성의 확정이 아니다. XML 번호는 all-in-one/sources/decoded-original의 같은 번호 파일을 뜻한다.

| 층위 | 직접 원본 선언 | 형식·주소·사용 | 경계 |
|---|---|---|---|
| LS06 원시 입력 | 0607 SimpleAccess RID131 EV02_Close, SAD Input, SSD AO73, CS NID12 UID42/48 | Bool I9.1 read | FG70 LS06, FG125 E9.1과 대응 |
| 부모 B 닫힘 처리 | 0609 GlobalAccess RID133, AO73, BAD BIRID86; 0608 RID86 Inputs TOD13 | Bool DB13.DBX9.1 read | AO 이름 LIMIT SWITCH LS-06GATE B CLOSEDVALVE PV-01; raw와 다른 저장소 |
| 부모 B 닫힘 기억 | 0609 RID134 AO66 BAD5; 0608 RID5 Flag TOD2 | Bool DB2.DBX8.2 S/R | 센서값이 아닌 명령·조건·래치 기억 |
| 부모 B 열림 기억 | 0609 RID11 AO67 BAD5 | Bool DB2.DBX8.3 S/R | LS06에서 직접 열림을 추론하지 않음 |
| 부모 B 명령 | 0607 RID49 PV-01 GATE B EV, Output AO43 | Bool Q5.3 read in 0287 | LS06에 전용 출력이 있는 뜻 아님 |
| HMI 설정 항목 | hmi_plc_tags.csv 662행 PV_01\GateB_Close | DB11,X76.4 / PLC | LS06 raw 입력 주소나 독립 LS06 쓰기 명령이 아님 |

[E03] HMI CSV의 GateB_Open(DB11,X76.3), Selector_GateB(DB11,X76.6), Allarme1(DB11,X76.0)도 부모 PV01 항목이다. CSV는 dde.cfg 설정 색인으로 현재 화면/갱신/버튼 이벤트를 증명하지 않는다. 부모의 0391 HMI PV_2Gate CRef32 실인수17개 미결속 경계는 그대로 남긴다. 이번에 HMI 호출을 해소하지 않았다.

[E04] 0397/LAD1070/NID1 Move43.in은 W55/ORef47→0627 RID15 Tag_181, Word Input AO64(IW8); out1은 W57/ORef48→0629 RID16 Word AO64/BAD4→0628 RID4 Inputs TOD13(DB13.DBW8)이다. Word8 범위에 I9.1→DB13X9.1이 포함된다. Move42.eno→W53→Move43.en, Move43.eno→W56→Move44.en도 보존한다. 이 Move에 LS06 전용 반전은 없다. 다른 MV03 반전부 Part142/150을 LS06 반전으로 옮기지 않는다.

호출은 부모 색인 0030의 HMI Inputs CRef28.en에 NOT Simulation(1) 조건이 있다는 공통 근거를 재사용한다. 현재 호출값·ENO·스캔 순서·CPU·모든 쓰기 소유는 미확정이다. 아래 별도 쓰기 때문에 DB가 항상 raw와 같다는 단정은 특히 금지한다.

## 3. 제어 구조·기억·복수 쓰기

[E05] 0287/LAD1922/NID12에서 LS06 고유 분기와 출력 기억을 직접 대조했다. W53 powerrail→Contact21.in; W54/ORef38→0607 RID1 ON M0.0. W55에서 Contact22/29/31/36으로 분기한다.

- 닫힘 기억 Set: Contact31 operand는 W93/ORef94→RID49 Q5.3이고 Negated다. Contact31.out W72→Contact32.in 및 Contact33.in. raw-close Contact32.operand W73/ORef48→RID131 I9.1, out W74→OR34.in1. 처리close Contact33.operand W75/ORef49→0609 RID133 DB13X9.1, out W76→OR34.in2. OR34.out W77→SCoil35.in, operand W78/ORef50→RID134 DB2X8.2.
- 닫힘 기억 Reset: Contact36 operand W96/ORef97→RID49 Q5.3(비반전), out W95→RCoil37.in, W81/ORef52→RID134.
- 열림 쪽 LS06 분기: Contact22 Q5.3 뒤 W57→Contact24.in. Contact24 operand W60/ORef41→0610 literal RID130 false; out W61→Contact25.in. Contact25 operand W62/ORef42→RID131 I9.1이며 비반전, out W63→OR27.in2. 따라서 false 직렬 분기는 LS06만으로 열림 기억을 Set할 수 없다.
- 열림 다른 경로는 raw-open Contact23 W58/ORef40→RID129와 DB-open Contact26 W64/ORef43→RID132가 OR27.in1/in3(W59/W65)으로 합류한다. OR27.out W66→SCoil28, W67/ORef44→RID11 DB2X8.3. Reset은 Negated Contact29 Q5.3(W91/ORef92)→W90→RCoil30, W70/ORef46→RID11.

정적 식: B_MEM_CLOSE Set = ON AND NOT Q5.3 AND (I9.1 OR DB13X9.1), Reset = ON AND Q5.3. B_MEM_OPEN Set = ON AND Q5.3 AND [I9.0 OR (false AND I9.1) OR DB13X9.0], Reset = ON AND NOT Q5.3. ON은 M0.0 메모리이고 false literal과 다르다. LS06 Contact25/32 자체는 비반전이다. 이것으로 실물 정상 시 접점 전도 여부나 안전 정지를 확정하지 않는다.

[E06] 동일 처리 주소에 별도 백업 쓰기가 존재한다. 원본 0410/LAD1090/NID12(원본 블록명 simulation)의 Contact40은 operand Negated, W50/ORef44→0636 RID210 Output AO43 Q5.3; out W51→Coil41.in; operand W52/ORef45→0635 RID212 AO73 BAD5→0634 RID5 Inputs TOD13, 즉 DB13X9.1 쓰기다. 이는 물리 I9.1 반전이 아니라 명령 기반 별도 DB 쓰기다. 원본 XML 정적 열람으로 쓰기 존재만 확인했으며 이 블록의 현재 실행 여부·활성 조건·최종 우선 쓰기·실행 결과는 확인하지 않았다. 중지 시뮬레이터를 생성/수정/실행하거나 행동시험하지 않았다.

부모 startup 0150에서 B_MEM_CLOSE Set이 있다는 기존 PV01 공통 근거도 남긴다. 그 시작 기억을 LS06이 실제 닫힘을 검출한 증거로 삼지 않는다. 부모 전체 자동순서/출력식/알람 반복 검토는 이번 범위 밖이다.

## 4. 전기 끝점·P&ID·시공 상충

[E07] Electrical_Rev2.pdf의 실제 PDF71/126을 렌더하여 접속점 및 양 끝점을 확인했다.

| 원본 | 페이지별 날짜/개정 | LS06 경로 및 판독 |
|---|---|---|
| FG70 / PDF71, LOAD DRUM CLAPPE VALVE PV-01 | 기본 27.05.2024, 개정란 공란 | +24Vdc10.7 수평선의 접속점→X1/136 퓨즈단자(도면 5×20 2A F)→선70.4→LS06 13/14→X1/137→E9.1 / 125/2 |
| FG125 / PDF126, DIGITAL INPUT MODULE | 기본 27.05.2024, 개정란 공란 | E9.1의 상호참조70/5→CPU515 MOD10 단자12; 표제 LIMIT SWITCH LS-06 GATE “B” CLOSED VALVE PV-01 |
| 같은 FG125 | 동일 | 모듈 전원19는 +24Vdc10.7→X21/3010 퓨즈5×20 2A IST→125.1, 20은 -0Vdc10.6. 이 전원핀을 LS06 접점핀으로 쓰지 않음 |
| PID PDF1 PV01 Detail | Apex I / 15.01.2013 | LS06 리더→CL03 몸체쪽, LS05 반대 리더, EV02 계통 CL03/04 |
| 시공 PDF53, 표제53/64, CANDC-CONS-C003-053 | Rev1 24.11.11 first draft design | 행3_26 =ENT+PV01-LS06A, FROM PV01 ENT2TB3 / PV-01 A GATE, TO PV01 LS-06; DC CVV 2C 1.0, route E222, adjustment3/len3 |

LS06 도면은 13/14 개방 접점 기호다. 이는 도면상 기호 판독이며 실제 센서 방식/정상 위치 극성/명판 접점 구성/작동거리 확인이 아니다. PLC의 CLOSED 명칭과 혼동해 평상시 전도·고장안전 극성을 선언하지 않는다. 도면 퓨즈값은 현행 보호설정/교체 승인값이 아니다.

[E08] 시공 PDF53 행3_10은 ENT2TB1→ENT2TB3 LS05/06/07/08, DC CVV12G1.0, spare3, RBD1/E220을 적고, 행3_26은 LS06 출발 DESCRIPTION을 PV-01 A GATE라고 적는다. OEM FG70/125의 GATE B CLOSE/CLOSED와 명칭이 상충한다. 또한 OEM에는 없는 LS07/08 번호가 시공 묶음에 포함된다. 따라서 시공 표만으로 OEM X1/136·137과 ENT2TB3의 특정 심선/단자 번호를 결속하거나 LS07/08을 추가 PLC 입력으로 만들지 않는다. field wiring/as-built와 게이트 태그 사진이 필요하며 기존 대장·도면을 임의 정정하지 않는다.

## 5. 알람·복구

적용은 부모 PV01 B의 위치감시 참조다. LS06 전용 타이머/알람/복구 명령의 근거는 확보하지 못했다. 부모의 0450/LAD1816/NID43 B NOT_OPEN/NOT_CLOSE 7초 감시를 LS06 독립 알람 수에 복제하지 않는다. 부모색인 근거는 SD1517/S1523/R1528 및 SD1535/S1541/R1546, 0656 RID320 S5T#7S이며 본 조사에서 알람 네트워크 전체를 다시 검토한 것은 아니다. A의4초와 B의7초를 합치지 않는다.

LS06 raw만 1이어도 ON/출력/처리DB/기억/초기화/호출에 따라 부모 표시가 달라질 수 있다. 알람 해제와 실제 접점 정상, 기계 닫힘, CL03/CL04 동시 행정, 재기동 허가는 서로 별도 증거다. 현장복구·안전 절차·리셋 후 실제 상태는 미확정이며 강제입력/점퍼/바이패스/가압/재기동을 지시하지 않는다.

## 6. 증상별 관찰

아래는 이미 확보한 승인 관찰자료를 비교하는 항목이며 시험/현장조작 절차가 아니다. 시각·시간대·관찰자·자산ID·프로젝트/CPU 식별·수집위치·값·사진·비교원본·배제결과·조치·복구증거를 각각 기록한다. 미수집값을 0으로 채우지 않는다.

| 증상 | 비교할 기록 | 원인/미확정 경계 |
|---|---|---|
| 실제 닫힘처럼 보이나 raw I9.1=0 | LS06 태그/설치사진, 기계 위치, 13/14·X1/136/137·MOD10/12 같은 시각 자료 | 센서 위치/접점/전원/배선/주소 중 고장 구간 아직 미확정 |
| I9.1과 DB13X9.1 다름 | 원시/DB 시각, IW8 복사 호출, 프로젝트와 별도 DB쓰기 소유 | 복사 주기·호출·별도 쓰기·현행 백업 차이 배제 필요 |
| DB2X8.2가1인데 raw가0 | Q5.3, ON, raw/DB, startup/래치 관련 기록 | 기억·처리 OR 경로이지 실제 닫힘 보증 아님 |
| HMI CLOSED와 실제가 다름 | DB11X76.4 설정, DB13X9.1, DB2X8.2, HMI 이벤트/갱신근거 | HMI 결속·현재값 미확정; 화면 하나로 LS06 고장 판정 불가 |
| 도면 B인데 현장/시공 A 표기 | OEM FG70/125, 시공3_26, P&ID CL03 리더, 현행 태그/기계배치 | 명칭 충돌 유지; 임의 이름교환/단자 재지정 금지 |
| 부모 B 닫힘 미도달 알람 | 부모7초·명령/기억과 같은 시각 기계상태 | LS06 단독 고장과 EV/공압/기계 문제 분리 필요 |

## 7. 완료·누락·정적검사

| 영역 | 판정 | 미확정 |
|---|---|---|
| 설비·자료 | 적용, 대장/고유 리더 확인 | 실물 동일성·게이트 물리 위치 |
| I/O·HMI | 적용, raw/DB/MEM/부모HMI 분리 | 현재CPU·실제HMI 결속 |
| 제어 | 적용, 0287·0397·0410의 관련 분기만 검토 | 실행순서·전체 쓰기·현재 활성상태 |
| 전기 끝점 | 적용, OEM2쪽+PID1쪽+시공1쪽 렌더 | OEM↔현장 심선 결속·극성·현행 보호값 |
| 알람·복구 | 부모 공통 참조 | LS06 전용 근거·실제복구 없음 |
| 증상관찰 | 적용, 관찰형식 | 실제 관찰기록 없음 |
| 완료기준 | documentation complete_with_gaps | 독립 검토/통합/기능/UI/게시/현장 미완료 |

다음 필요한 자료는 LS06 명판·설치/게이트 태그 사진, 승인 as-built X1↔ENT2TB3 심선표, 센서 형식·작동점/정상극성, 현행 CPU 및 HMI Export다. 동일 보류를 새 자료 없이 반복 확정하지 않는다. 네 기능(도면·래더 비교, 백업·선택복원, 기록 전후비교, 보고서/PDF)은 구현/검증하지 않았다. note/repair_observation·미지 필드·타설비·초안·저장키를 보존한다. UI/게시 not_performed, TIA/live_cpu/field_recovery not_performed. BC01 동등 기능 완료로 집계하지 않는다.

검사: Git HEAD 고정 및 clean 확인, PDF4개 페이지 실제 렌더와 PID 확대2개 판독, XML3개 네트워크의 LS06 관련 경로+선언10개 파일 필요한 RID 검토. 문서 전체13개 XML를 모든 의미에 대해 완주한 수가 아니다. 695 XML 이름탐색은 ID와 AO의 LS-06/EV02_Close만 검색한 탐색이며 3개 선언파일 일치, 검색수를 의미검토수로 합치지 않는다. HMI CSV와 대장2개·network-map은 설정/탐색 보조 검토다. 원본 저장소 생성기/preflight/앱테스트/시뮬레이터는 실행하지 않고 자체 정적 추출/바이트검사만 수행했다.

### 선정 원본 전체 SHA256·고정 Git blob 대조

아래는 선정 원본 26개 각각의 전체 SHA256 및 고정 커밋 Git blob이다. git cat-file blob의 바이트와 로컬 파일을 직접 비교했다. 해시 일치는 현재 CPU나 현장 준공 일치를 뜻하지 않는다. 검사JSON은 extracts/LS06/source-integrity.json에 보관한다. 원본 주소는 https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/ 에 표의 경로를 붙인다.

| 원본 경로 | SHA256 | Git blob | 바이트 일치 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | 일치 |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | 일치 |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | 일치 |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | 일치 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | 일치 |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | 일치 |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | 일치 |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | 일치 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | 일치 |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | 일치 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | 일치 |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | 일치 |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | 일치 |
| `all-in-one/sources/decoded-original/0287-FlgNet.xml` | `885e0619ad4a49a2a873b4f0f069eafc62b350f4a12f060e4def9c020f3fe616` | `7911c5e5d9d9578f60012be454481ca434aaa831` | 일치 |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | 일치 |
| `all-in-one/sources/decoded-original/0410-FlgNet.xml` | `5a72ba5ae71e50ff277c3c52fcf94d4a2e71dff81897bafe72e7f3efc08986cd` | `5314b20676c0f2e4c08041071792232526fc65c4` | 일치 |
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | 일치 |
| `all-in-one/sources/decoded-original/0608-IdentXmlPart.xml` | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | 일치 |
| `all-in-one/sources/decoded-original/0609-IdentXmlPart.xml` | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | 일치 |
| `all-in-one/sources/decoded-original/0610-IdentXmlPart.xml` | `c58d07b1b9707dc8c6c2f06c34ee6142f72238a4cf3f376bee8502d1a9532f9d` | `1497b6bfd7fd9b8afe427b9c910d15e9cf888f9c` | 일치 |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | 일치 |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | 일치 |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | 일치 |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | 일치 |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | 일치 |
| `all-in-one/sources/decoded-original/0636-IdentXmlPart.xml` | `ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca` | `86114327ba1a010b2fcc01dd12b1bf86c01bc02c` | 일치 |

### 공유색인 및 작업지시의 로컬 해시

아래는 고정 Git 원본 검사수에 합산하지 않는다. 부모 초안 전체를 재검토했다는 뜻도 아니다.

| 로컬 자료 | SHA256 |
|---|---|
| `gme-research/drafts/PV01-DOTS-DRAFT.md` | `ed9c8d774ab53ab5c725580f22b076268bc157f09bdccd1a35518e3819670b9e` |
| `gme-research/drafts/CYL-CL03-DOTS-DRAFT.md` | `5bc845b7ad154561ae8fd94a9b957ba23d51ccfc42b0a447504f89a5da5294e6` |
| `gme-research/progress/BATCH21-RESEARCH-INSTRUCTIONS.md` | `7fffd1cb697715bee412f3ca7fd95911e629a497ec747ec2e65d4aff0674a9bb` |
| `gme-research/progress/TASK3-BATCH21-SCOPE.json` | `50819490aee0ecda1ae8ec951e2be3a3dd91c3b28a54ee9043534c6cbb157293` |
| `gme-research/progress/GME-CATALOG-OVERLAP-REVIEW.json` | `027c2d89b034f3681dced7db98146ffd77eecfad116a1a94cac035ccbd598967` |
