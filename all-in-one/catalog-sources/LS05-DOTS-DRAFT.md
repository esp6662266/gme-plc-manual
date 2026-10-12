# LS05 고유 원본 조사 초안

- 대상 LS05 밸브 위치 리미트 스위치, PV01 하위 component / phase2 / parent_child_separate. 별칭 ls-05, ls.05.
- 기준 GME-STD-1.0.0, source-mv06 고정 abcf31c5030bc7ef8749ed8e869a857f2387a28a, VERSION 1.12.0. 조사 2026-10-11 UTC. 실제 모델/추론 설정 미확인.
- 자신의 drafts/LS05-DOTS-DRAFT.md 및 extracts/LS05만 작성. 원본·공통코드·PLC·현장·보호값·SEJIN·대장·배포 변경 없음. 생성기·앱빌드·시뮬레이터 작성/수정/생성/실행·행동시험 없음.
- 문서 complete_with_gaps, 한정 정적 조사 완료. 통합·UI·기록·게시·TIA·현행 CPU·실물·복구 확인과 별개다.

## 1. 설비·자료 기준

[E01] INVENTORY.json catalog[222] 및 equipment.json[210]은 LS05→PV01 관계, 별도 catalog ID와 baseline/not_assessed를 기록한다. BATCH21-SCOPE 및 중복 검토도 physical_identity_verified=false다. 부모 PV01 문서의 완료를 본 센서 완료로 상속하지 않는다.

[E02] PID_1684n002I.pdf 실제 PDF1의 PV-01 Detail을 원본 전체 및 확대 렌더로 확인했다. LS-05 리더선은 CL-03 오른쪽 로드 쪽 표시로 내려가며 LS-06 리더는 CL-03의 다른 위치로 간다. EV-02 공압선이 CL-03/CL-04 두 실린더 기호에 분기한다. LS05가 CL04를 독립 검출하는 선은 이 상세도에 없다. 기계 GATE A/B 그림은 별도로 있으며 CL03 번호와 그 형상 위치를 직접 결속하는 리더선은 없다. 따라서 도식의 상하/좌우로 현장 Gate A/B 위치를 추정하지 않는다.

P&ID 표제 UBC AND SCRAPS DECOATER 10 Ton/h, Drawing 1684n002, Apex I, 기본 06/04/2011, 최종 I 15/01/2013, I행 REMOVED MC-05, CHANGED POWER OF FN-02. 전기 도면은 2024/2025 자료이며 서로 시점이 다르다. 최신 준공도나 현재 설치 일치를 의미하지 않는다.

[E03] Electrical_Rev2.pdf FG70/PDF71와 FG125/PDF126은 LS05를 PV-01 GATE B OPEN으로 명시한다. P&ID의 실린더 리더 소유와 전기 신호의 Gate B 소유를 분리한다. LS05와 LS06은 쌍으로 관련되지만 별도 입력이다. LS01/02 또는 CLIENT-CL03과 이름/번호만으로 합치지 않는다.

공유 탐색색인은 PV01-DOTS-DRAFT.md 및 CYL-CL03-DOTS-DRAFT.md다. 부모 전체 순서·출력·알람을 반복 조사하지 않았다. PV01 구초안의 69KA 1–9 표기는 채택하지 않고 고정 WORKSPACE-HANDOFF의 5–9 정정을 유지한다. 71KA도 공유 정정 5–9를 유지하되 LS05 소유 회로로 옮기지 않는다.

## 2. I/O·HMI

아래 XML 축약은 all-in-one/sources/decoded-original/의 해당 번호 파일이다. 주소는 백업 선언이며 온라인 값이 아니다.

| 신호 종류 | 원본 선언·접속 | 주소·형식·역할 | 경계 |
|---|---|---|---|
| LS05 원시 열림 입력 | 0607 RID129 EV02_Open, Global, NID12 UID40, SSD AO72, SAD Input | I9.0 Bool 읽기 | 전기 E9.0 대응; 센서 소프트웨어 별칭 |
| 가공 입력 | 0609 RID132, NID12 UID43, AO72, BAD86; 0608 RID86 Inputs TOD13 | DB13.DBX9.0 Bool 읽기 | 원시 입력과 별도 메모리 경로 |
| 부모 B 출력 | 0607 RID49, AO43, SAD Output; NID12 UID89/92/94/97 | Q5.3 Bool 읽기 | LS05의 출력이나 전원 아님 |
| 부모 B 열림 기억 | 0609 RID11, AO67, BAD5; 0608 RID5 Flag TOD2 | DB2.DBX8.3 Bool Set/Reset | 센서 원시값 아님 |
| 부모 B 닫힘 기억 | 0609 RID134 AO66 BAD5 | DB2.DBX8.2 Bool Set/Reset | LS06/처리닫힘 경로와 관련 |
| LS06 원시·가공 닫힘 | 0607 RID131 AO73; 0609 RID133 AO73 BAD86 | I9.1 / DB13.DBX9.1 Bool | LS05 상태로 치환하지 않음 |
| HMI GateB_Open | hmi_plc_tags.csv 661행 PV_01\GateB_Open | DB11,X76.3 | dde.cfg 설정; LS05 raw 직접주소 아님 |
| HMI GateB_Close | 같은 CSV 662행 | DB11,X76.4 | 센서 쌍/기억과 결속을 이름만으로 확정 금지 |

[E04] 0607 RID129의 CS는 NID12 UID40 읽기다. 0287 Contact23에 Negated가 없으므로 이 사용처의 I9.0은 비반전 접점이다. 이것은 현장 스위치의 정상극성 또는 기계 개방에서 실제 1이 된다는 현장 검증이 아니다. FG70의 13/14 열린 접점 그림, XML 비반전 읽기, 현장 정상 상태를 서로 구분한다.

[E05] 0397-FlgNet LAD1070/NID1 Move43.in W55/ORef47→0627 RID15 Tag_181, Word/Input AO64=IW8. out1 W57/ORef48→0629 RID16 Word AO64 BAD4→0628 RID4 Inputs TOD13=DB13.DBW8. 이 복사 범위는 I9.0에 대응하는 비트를 포함한다. Move42.eno→W53→Move43.en, Move43.eno→W56→Move44.en이므로 무조건/항상 최신이라고 쓰지 않는다. 이 선택 Move 경로에는 비트 반전이 없다. 다른 쓰기·호출 조건·현행 스캔까지 검증하지 않았다.

호출 조건은 부모 PV01 §2.2 공유 근거(0030 LAD1613 NID19 CRef28 HMI Inputs, NOT Simulation(1) 경유)를 참조한다. 이것은 보존된 백업 호출 구조의 설명일 뿐 중지 자산의 실행/복구 요청이 아니다. HMI 실제 이벤트와 0391 CRef32의 17개 실인수 미결속은 부모 조사에서 유지한 미확정이며 이번 LS05 조사로 해소하지 않았다. 독립 LS05 HMI 쓰기 명령/조작 버튼 근거는 미확보다.


### 2.1 처리 DB의 다른 쓰기 경계 보강

[E08] 부모의 좁은 추가 점검 요청으로 보존 원본 0410-FlgNet.xml(LAD1090, 원본 block명 simulation, NID12)의 LS05 관련 핀만 정적으로 확인했다. Powerrail W21→Contact38.in, operand W47/ORef42→0636 RID210 PV-01 GATE B EV, Output AO43=Q5.3. Contact38은 비반전이며 out W48→Coil39.in. Coil39.operand W49/ORef43→0635 RID211, CS NID12 UID43 AK=Write, AO72 BAD5. 0634 RID5 Inputs TOD13과 결속되어 대상은 DB13.DBX9.0이다.

이는 0397 IW8→DB13.DBW8과 별도로 같은 처리 비트를 쓰는 원문 경로가 존재한다는 증거다. DB13X9.0을 언제나 현장 raw LS05와 동일하다고 단정할 수 없다. 중지 블록의 존재만 확인했으며 현행 호출·활성·실행순서·최종값은 미확정이다. 이 정적 핀 확인은 중지 블록이나 시뮬레이터의 작성·수정·생성·실행·행동시험이 아니다. 해당 자료는 실행하지 않았다.

## 3. 제어 구조

적용은 센서→원시/가공→부모 위치기억 구간이다. 독립 센서 구동 출력·PID·행정 제어 시퀀스는 이 센서 유형에 해당하지 않는다. 주변 EV 출력과 부모 타이머를 LS05 독립 기능으로 복제하지 않는다.

[E06] 0287-FlgNet LAD1922/NID12를 선언과 직접 대조했다.

1. Powerrail W53→ON Contact21.in; operand W54/ORef38→0607 RID1 M0.0. out W55→Q Contact22.in 등으로 분기. Contact22 operand W88/ORef89→RID49 Q5.3.
2. Contact22.out W57→Contact23/24/26.in. LS05 Contact23.operand W58/ORef40→RID129 I9.0, out W59→OR27.in1. Contact23는 비반전이다.
3. Contact24.operand W60/ORef41→0610 RID130 literal false; out W61→Contact25.in; operand W62/ORef42→RID131 I9.1; out W63→OR27.in2. false를 OFF 메모리로 바꾸지 않는다.
4. Contact26.operand W64/ORef43→0609 RID132 DB13X9.0; out W65→OR27.in3. Contact26도 비반전이다.
5. OR27.out W66→SCoil28.in; operand W67/ORef44→RID11 B_MEM_OPEN. Reset은 NOT Q Contact29(operand W91/ORef92→RID49).out W90→RCoil30, operand W70/ORef46→RID11.
6. 병행 닫힘은 NOT Q Contact31→raw-close32/DB-close33→OR34→SCoil35(B_MEM_CLOSE), Q Contact36→RCoil37이다. W73/ORef48 raw-close, W75/ORef49 DB-close, W78/ORef50 및 W81/ORef52 닫힘기억을 보존한다.

정적 식: S B_MEM_OPEN = ON AND Q5.3 AND [I9.0 OR (false AND I9.1) OR DB13X9.0]. R B_MEM_OPEN = ON AND NOT Q5.3. 따라서 raw LS05=0이어도 DB 입력 또는 이미 설정된 기억 때문에 열림기억이 1일 수 있다. 반대로 raw=1도 ON/Q 조건이 없으면 그 자체로 열림기억 설정을 보장하지 않는다. 기억비트는 현장 실물 개방의 직접 증거가 아니다. 원시·가공·기억·HMI의 관찰 시각도 맞춰야 한다.

부모 Q5.3 요청 경로와 startup·자동순서는 PV01/CYL-CL03 색인의 공유 근거로 재사용한다. LS05 자체 Enable/Reset/고장 latch를 새로 만들지 않는다. LS05 신호 하나로 CL03와 CL04가 함께 끝 행정에 도달했는지, Gate B가 안전한지는 확정할 수 없다.

## 4. 전기 전달 끝점 및 실제 PDF

[E07] 원본 PDF 3페이지(P&ID1, 전기71/126)를 실제 렌더하고 접속점·접점·단자·개정란을 시각 판독했다. extracts/LS05 PNG가 이번 렌더다.

| 원본 FG / 실제 PDF | 페이지별 개정·날짜 | 고유 끝점 |
|---|---|---|
| FG70 / PDF71 | 개정란 공란, 기본 27.05.2024 | +24Vdc10.7 공통선 접속점→X1/134 퓨즈단자(도면 5×20 2A F)→선70.3→LS-05 단자13/14→X1/135→E9.0 하단 교차참조125/2 |
| FG125 / PDF126 | 개정란 공란, 기본 27.05.2024 | 상단 교차참조70/4 E9.0→CPU515 MOD10 입력 단자11, LS-05 GATE B OPEN VALVE PV-01 명기 |
| 같은 FG125 / PDF126 | 동일 | +24Vdc10.7→X21/3010 퓨즈 5×20 2A IST.→125.1→모듈19; -0Vdc10.6→모듈20. LS05 신호11과 전원19/20을 혼동하지 않음 |
| PID / PDF1 | Apex I 15.01.2013, 기본06/04/2011 | LS05→CL03 로드 쪽 리더; EV02→CL03/04 공압 분기 |

FG70 제목 LOAD DRUM CLAPPE VALVE PV-01, FG125 제목 DIGITAL INPUT MODULE. LS05 접점13/14는 PDF에서 열린 형태로 그려졌지만 현재 장착형식·극성·접촉상태 미확정. 퓨즈값은 도면값일 뿐 현행 보호설정의 승인·교체 지시가 아니다. E(도면)와 I(백업)의 표기 차이는 같은 주소9.0의 대조이지 현장 배선 시험 결과가 아니다.

대장 fgs=[69,70]은 자료색인 범위다. 직접 LS05 입력 끝점은 FG70/125이며 FG69 EV 출력 부하와 구분한다. 69KA/71KA 5–9 정정은 유지하되 LS05에 릴레이 코일을 새로 부여하지 않는다. 현장 단자함·케이블 심선·실제 센서 제조사/형식/명판은 이번 자료로 확정하지 않았다. 현장 X1↔단자함↔LS05 케이블 양 끝점 도면과 사진이 필요하다.

## 5. 알람·복구

적용은 부모 Gate B 감시에 대한 LS05의 간접 영향이다. LS05 독립 알람·전용 지연·전용 Reset은 근거 미확보다.

PV01 §5와 CYL-CL03 §5의 공유 원본 근거는 0450 LAD1816/NID43, B NOT_OPEN/NOT_CLOSE를 MEM_OPEN/CLOSE로 7초 감시한다. SD1517/S1523/R1528, SD1535/S1541/R1546와 0656 RID320 S5T#7S의 부모 타이머다. 이번에 알람 전체 네트워크를 다시 의미검토한 것은 아니며 LS05 자체 7초 필터나 센서 디바운스라고 재분류하지 않는다. A4초를 가져오지 않는다.

raw LS05 단선/고착 여부는 이 알람만으로 단정할 수 없다. 처리 DB OR·기억 래치·출력조건·기계 행정이 영향을 줄 수 있다. 부모 알람 해제나 HMI 표시 변화만으로 센서/게이트 복구 완료를 선언하지 않는다. 승인 안전 절차, 현장 정상극성, 동시각 기록과 실제 행정 증거를 확보해야 한다. 본 문서는 강제출력·점퍼·우회·가압·재기동 시험을 지시하지 않는다.

## 6. 증상별 관찰·원인 구분

실제 시험 없이, 향후 승인 절차로 이미 수집된 기록의 비교 항목만 제시한다. 공통 필드는 관찰자·시각/시간대·현장 자산ID·CPU/프로젝트 식별·수집위치·값·사진/근거·배제결과·조치·복구증거다. 빈칸을 0으로 간주하지 않는다.

| 증상 | 함께 비교할 값·위치 | 아직 배제할 수 없는 범위 |
|---|---|---|
| Gate B 개방으로 보이나 I9.0=0 | LS05 위치/명판 사진, X1/134–135·13/14·MOD10/11 관련 승인 측정기록 | 센서 작동위치·접점·공급·심선·입력모듈·태그 오식별 |
| I9.0=1이나 열림기억0 | 같은 시각 ON(M0.0), Q5.3, DB13X9.0, DB2X8.3 | 설정조건 미성립·Reset·스캔/다른쓰기·현재프로젝트 차이 |
| I9.0=0인데 열림기억/HMI1 | DB13X9.0·DB2X8.3·DB11X76.3 동시기록 | 처리 입력·래치·HMI 미결속/갱신; raw만으로 고장 확정 불가 |
| LS05와 LS06 동시1 | I9.0/9.1, 두 센서 물리위치·접점 및 현행 극성 | 기계 범위 겹침·고착·배선·태그; 정상이라고 추정 금지 |
| 부모 B 미도달 알람 | 부모 명령/MEM·7초 조건과 실제 CL03/04 행정 | 센서 단독 고장 또는 공압/기계 원인인지 미확정 |

## 7. 완료·누락·검사 결과

| 영역 | 적용 상태 | 완료 경계 |
|---|---|---|
| 설비·자료 | 적용 | 별도ID·P&ID 리더·전기 Gate B 소유 확인, 실물 미확인 |
| IO/HMI | 적용/일부 미확보 | I9.0/DB13/DB2/HMI 분리; 이벤트·호출 실인수 미확정 |
| 제어 | 적용 | 0287 입력/OR/SR 및 0397 Word복사 직접 대조 |
| 전기 | 적용 | 원본 전기2쪽·PID1쪽 렌더, 현장 심선 미확인 |
| 알람/복구 | 부모 공통참조 | LS05 독립 알람 근거 없음; 현장 복구 미수행 |
| 증상 관찰 | 적용 | 비교 항목 작성; 운영 기록·시험 생성 없음 |
| 완료 기준 | 적용 | 문서 complete_with_gaps와 구현/현장 별도 |

다음 필요한 자료: (1) LS05/LS06 명판·설치위치와 실제 개방/폐쇄의 승인 관찰기록, (2) X1/134–135부터 센서까지 준공 케이블·심선표, (3) 현행 CPU 프로젝트/현재값·전체 쓰기 교차참조, (4) PV01 HMI CRef32 호출 원본과 화면 이벤트 Export. 새 자료 없이 센서 정상극성·실물동일성·복구를 확정하지 않는다.

네 기능(도면·래더 비교, 백업·선택복원, 전후 기록 비교, 보고서/PDF)은 통합 구현·검증 대기다. UI/저장·재열기/게시 not_performed, TIA/live_cpu/field_recovery not_performed. 기존 note/repair_observation·미지 필드·다른설비·초안·저장키 보존. 독립 검토는 부모 대기이며 BC01 동등 기능완료로 세지 않는다.

선정 원본 30개 SHA256·고정 Gitblob 바이트 30/30 일치. 기술 의미검토는 17파일(equipment1·PDF2·HMI CSV1·XML13)의 선택 내용이다. 정책/분류12파일과 탐색 network-map1파일은 별도다. PDF 의미검토 3페이지, XML은 0287/0397 네트워크 및 0607/0608/0609/0610/0627/0628/0629 선택 선언 7파일에, 다른 쓰기 경계 0410 및 0634/0635/0636의 선택 핀·선언 4파일을 추가했다. 이름 검색으로 전체 XML 의미검토를 주장하지 않는다. 자체 정적 추출·해시와 PDF 렌더만 실행했으며 원본 생성기/시뮬레이터 실행 없음.

## 부록 A. 선정 전체 원본 SHA256·고정 Gitblob

경로 기준 source-mv06. git show 고정커밋 바이트와 로컬 바이트를 직접 비교했다. source-integrity.json, selected-declarations.json, selected-networks.json, 원본 PNG는 ../extracts/LS05에 있다. Gitblob은 Git 객체 식별자이며 SHA256과 다른 값이다.

| 원본 경로 | SHA256 | 고정 Gitblob | 바이트일치 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | 일치 |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | 일치 |
| `.agents/skills/gme-equipment-rollout/references/source-map.md` | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` | 일치 |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | 일치 |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | 일치 |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | 일치 |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | 일치 |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | 일치 |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` | 일치 |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | 일치 |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | 일치 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | 일치 |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | 일치 |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | 일치 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | 일치 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | 일치 |
| `all-in-one/sources/decoded-original/0287-FlgNet.xml` | `885e0619ad4a49a2a873b4f0f069eafc62b350f4a12f060e4def9c020f3fe616` | `7911c5e5d9d9578f60012be454481ca434aaa831` | 일치 |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | 일치 |
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | 일치 |
| `all-in-one/sources/decoded-original/0608-IdentXmlPart.xml` | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | 일치 |
| `all-in-one/sources/decoded-original/0609-IdentXmlPart.xml` | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | 일치 |
| `all-in-one/sources/decoded-original/0610-IdentXmlPart.xml` | `c58d07b1b9707dc8c6c2f06c34ee6142f72238a4cf3f376bee8502d1a9532f9d` | `1497b6bfd7fd9b8afe427b9c910d15e9cf888f9c` | 일치 |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | 일치 |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | 일치 |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | 일치 |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | 일치 |
| `all-in-one/sources/decoded-original/0410-FlgNet.xml` | `5a72ba5ae71e50ff277c3c52fcf94d4a2e71dff81897bafe72e7f3efc08986cd` | `5314b20676c0f2e4c08041071792232526fc65c4` | 일치 |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | 일치 |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | 일치 |
| `all-in-one/sources/decoded-original/0636-IdentXmlPart.xml` | `ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca` | `86114327ba1a010b2fcc01dd12b1bf86c01bc02c` | 일치 |

### 로컬 공유 색인 및 범위 자료

고정 원본 30개에 합산하지 않는다. 경로별 SHA256은 source-integrity.json의 local_indexes에도 보존했다.

| 로컬 경로 | SHA256 |
|---|---|
| `gme-research/drafts/PV01-DOTS-DRAFT.md` | `ed9c8d774ab53ab5c725580f22b076268bc157f09bdccd1a35518e3819670b9e` |
| `gme-research/drafts/CYL-CL03-DOTS-DRAFT.md` | `5bc845b7ad154561ae8fd94a9b957ba23d51ccfc42b0a447504f89a5da5294e6` |
| `gme-research/progress/BATCH21-RESEARCH-INSTRUCTIONS.md` | `7fffd1cb697715bee412f3ca7fd95911e629a497ec747ec2e65d4aff0674a9bb` |
| `gme-research/progress/TASK3-BATCH21-SCOPE.json` | `50819490aee0ecda1ae8ec951e2be3a3dd91c3b28a54ee9043534c6cbb157293` |
| `gme-research/progress/GME-CATALOG-OVERLAP-REVIEW.json` | `027c2d89b034f3681dced7db98146ffd77eecfad116a1a94cac035ccbd598967` |
