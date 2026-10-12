# LS02 고유 구성품 원본 조사 초안

- 대상: LS02, 밸브 위치 리미트 스위치, PV01 하위 component, phase2. 별칭 ls-02 / ls.02. 부모·하위 별도이며 실물 동일성 확인은 아니다.
- 고정 원본: source-mv06, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION v1.12.0. 조사일 2026-10-11 UTC. 시작 Git clean, 원본 읽기 전용.
- 기준: GME-STD-1.0.0, BATCH21-RESEARCH-INSTRUCTIONS, TASK3-BATCH21-SCOPE. 원본 AGENTS/스킬/표준/작업템플릿/대장과 시작 문서의 최신 항목 확인. 실제 모델/추론 설정은 독립 관측 자료 미확보.
- 이번 결과: LS02는 도면 Gate A CLOSED, 원시 I8.7, 처리 DB13.DBX8.7, 상위 MEM_CLOSE를 구분해야 한다. FG124의 SPARE와 회로/PLC 사용 상충을 보존한다. **FG70 LS02의 교차참조는 124/7**이다.
- 쓰기 범위: 이 MD와 extracts/LS02/만. 원본·공통코드·버전·대장·배포·운영·PLC·현장·보호값·SEJIN 변경 없음. 시뮬레이터 작성/수정/생성/실행/행동시험, 원본 생성기 및 앱 빌드 실행 없음. XML/PDF 정적 분석만 수행.

## 1. 설비·자료 기준

INVENTORY.json catalog[221]은 LS02 parent_id=PV01, depth=1, phase2, queue_state=planned, existing_detail=baseline, bc01_standard_acceptance=not_assessed다. equipment.json의 LS02 행은 fgs=[69,70], pid=true 및 위 별칭을 선언한다. GME-CATALOG-OVERLAP-REVIEW와 배정 JSON의 parent_child_separate, physical_identity_verified=false를 유지한다. 부모 문서 완료나 동일한 센서 이름을 실물 동일성으로 상속하지 않는다.

원본 P&ID `all-in-one/sources/PID_1684n002I.pdf` 실제 PDF1, 1684n002, Apex I, 기본 06/04/2011, 개정 I 15/01/2013, FG ‘–’의 PV-01 Detail을 직접 렌더했다. EV01 공압 분기는 CL01/CL02로 이어지며 LS02 리더는 CL01 기호의 몸체 쪽, LS01은 로드 쪽이다. 이는 도면 리더 관계이며 실제 장착 위치·작동점·정상극성의 확인서가 아니다. Gate A/B 기계 형상 글자를 실린더 분기와 연결하는 명시 선이 없어 상하 실물 위치를 추정하지 않는다.

`drafts/PV01-DOTS-DRAFT.md`와 `CYL-CL01-DOTS-DRAFT.md`는 탐색색인/공통근거로 재사용하고 전체 반복조사하지 않았다. 부모 알람·요청·EV 구동 전체는 부모에 남긴다. LS02는 CYL-CL01 자체나 EV01 코일과 동일 물체가 아니다. 69KA/71KA EV 부하접점 5–9 정정을 유지하며 LS 센서 회로에 그 AC 접점을 삽입하지 않는다.

## 2. I/O·HMI

이하 XML 원본 경로 접두사는 `all-in-one/sources/decoded-original/`이다. 주소는 고정 백업 선언으로 현재 CPU 주소/값이 아니다.

| 구분 | 원본 선언/참조 | 주소·자료 의미 | 미확정 경계 |
|---|---|---|---|
| 물리 원시 입력 | 0607-IdentXmlPart.xml SimpleAccess RID126 EV01_Close, SAD Input, SSD AO71, Bool; NID11 UID44 | I8.7; 전기 E8.7과 대조 | 설치/배선/정상값 미확정 |
| 처리 입력 | 0609 GlobalAccess RID127, AO71, BAD BIRID86; 0608 DepDBBlock RID86 Inputs TOD13; NID11 UID45 | DB13.DBX8.7, 이름 LIMIT SWITCH LS-02GATE A CLOSEDVALVE PV-01 | raw와 별도 저장/쓰기 대상 |
| 상위 위치 기억 | 0609 RID128 AO64 BAD5; 0608 RID5 Flag TOD2; NID11 UID46 Set / UID48 Reset | DB2.DBX8.0 PV_01_GATE_A_MEM_CLOSE | LS02 순간값·실물 위치와 같지 않음 |
| 부모 출력 조건 | 0607 RID50 PV-01 Gate a, Output AO42; NID11 UID43/47 | Q5.2, EV01 구동 조건 | LS02 출력이 아님 |
| 논리 허가 | 0607 RID1 ON, Memory AO0; NID11 UID36 | M0.0 | 이름을 상수 true로 치환하지 않음 |
| HMI 부모 닫힘 표시 | hmi_plc_tags.csv PV_01\GateA_Close | DB11,X76.2 | DB13X8.7/MEM_CLOSE와 동일 주소 아님 |
| HMI 부모 공통 알람 | 같은 CSV PV_01\Allarme1 | DB11,X76.0 | LS02 독립 알람으로 재명명 금지 |

AO71=8×8+7, AO64=8×8을 계산하고 SAD/BAD/TOD까지 대조했다. 동일 RID 숫자를 파일/블록 경계 없이 합치지 않는다. HMI CSV는 설정 주소 근거이며 표시 객체·실제 이벤트·권한·CRef32의 부모 17개 실인수 결속을 해결하지 않는다. LS02 전용 HMI 버튼/리셋 객체는 선정 자료에서 미확보다.

## 3. 제어 구조

### 3.1 raw/DB→부모 위치 기억: 0286-FlgNet.xml, LAD1921, NID11

| 단계 | 직접 Part/Wire/ORef/선언 결속 | 정적 해석 |
|---|---|---|
| 허가 | Powerrail W49→Contact21.in; W50/ORef36 RID1→21.operand; 21.out→W51 | ON을 공통으로 읽음 |
| 닫힘 방향 | W51→Contact29.in, Negated operand; W63/ORef43 RID50→29.operand; 29.out→W64 | NOT Q5.2, LS02 신호 반전 아님 |
| 원시 닫힘 | W64→Contact30.in; W65/ORef44 RID126→30.operand; 30.out→W66→OR32.in1 | I8.7은 이 경로에서 비반전 |
| 처리 닫힘 | W64→Contact31.in; W67/ORef45 RID127→31.operand; 31.out→W68→OR32.in2 | DB13X8.7 병렬 경로 |
| 기억 Set | OR32.out→W69→SCoil33.in; W70/ORef46 RID128→33.operand | S MEM_CLOSE = ON AND NOT Q5.2 AND (I8.7 OR DB13X8.7) |
| 기억 Reset | W51→Contact34.in; W71/ORef47 RID50→34.operand; 34.out→W72→RCoil35.in; W73/ORef48 RID128 | R MEM_CLOSE = ON AND Q5.2 |

닫힘 기억 Set 경로의 I8.7/DB 비트는 비반전이다. Q 출력 반전과 센서의 물리 정상극성을 혼동하지 않는다. 입력이 잠깐 없어져도 이 S/R 조각만으로 즉시 기억이 지워진다고 할 수 없으며 다른 쓰기·호출·스캔 순서는 별도 경계다. 이 LS02 가지에는 고유 타이머나 CRef 호출이 없다.

### 3.2 처리 입력의 다른 쓰기와 호출 경계

- `0397-FlgNet.xml` LAD1070/NID1 Move43: W55/ORef47→0627 RID15 Tag_181 Word/Input AO64=IW8가 in, out1 W57/ORef48→0629 RID16 Word AO64 BAD4, 0628 RID4 Inputs TOD13=DB13.DBW8이다. Move42.eno→W53→Move43.en, Move43.eno→W56→Move44.en. LS02 비트가 포함된 Word 전달로, 센서 전용 독립 코일은 아니다.
- `0030-FlgNet.xml` LAD1613/NID19: CRef25 HMI Output.eno→W42→NOT Contact37→W43→CRef28 HMI Inputs.en. Contact37 operand W44/ORef45→0692 RID140 Simulation(1), M180.0. 호출 선언 0688 RID128 FC19 / RID135 FC15, CRef25 Ref129/CodeBlock26 RID128 및 CRef28 Ref136/CodeBlock29 RID135. 백업 조건만 확인했고 현재 M180.0, ENO, CPU 실행 여부는 미확정이다.
- 어휘 검색에서 추가 LS02 쓰기 선언 `0635 RID209` NID12 UID37 Write, AO71 BAD5와 `0634 RID5 Inputs TOD13`을 확인했다. 보존 백업 `0410-FlgNet.xml`(색인 LAD1090, simulation 블록)의 Part30 NOT operand는 W32/ORef33→0636 RID207 PV-01 Gate a Q5.2다. W21 Powerrail→30.in; 30.out→W34→Coil36.in; W35/ORef37→0635 RID209=DB13X8.7. 즉 이 보존 조각에는 NOT Q5.2를 DB 처리 비트에 쓰는 경로가 있다. **센서 I8.7의 입력 반전이나 실제 닫힘 측정이 아니다.** 중지된 simulation 자료의 정적 읽기만 했으며 작성·수정·생성·실행·행동시험은 전혀 하지 않았다. 해당 보존 블록 호출/현행 CPU 최종값은 확인하지 않았다.

따라서 처리 DB 값·MEM·HMI 표시 하나만으로 LS02 실물 접점 닫힘이나 게이트 이동 완료를 증명할 수 없다. 이름이 같다고 원시와 가공값을 병합하지 않는다.

## 4. 전기 끝점

### 4.1 렌더·시각 확인한 실제 페이지

| 파일 | 실제 PDF | 표제/FG 또는 도번 | 해당 페이지 개정 |
|---|---:|---|---|
| PID_1684n002I.pdf | 1 | P&I, 1684n002, FG ‘–’ | Apex I 15/01/2013, 기본06/04/2011 |
| Electrical_Rev2.pdf | 71 | LOAD DRUM CLAPPE VALVE PV-01, FG70 | 개정란 공란, 기본27.05.2024 |
| 같은 파일 | 125 | DIGITAL INPUT MODULE, FG124 | Rev2 17.03.2025, 기본27.05.2024 |
| Electrical_Can_Decoating_20241118.pdf | 21 | ENTRY ROUTE CONDUIT PIPING (1), CANDO-CONS-E004-021, D-PAGE4 | 24.11.11 first draft design |
| 같은 파일 | 53 | CABLE SCHEDULE (2), CANDO-CONS-C003-053, D-PAGE3 | 이 페이지 개정란 공란; PDF21의 first draft를 승인 준공으로 승격하지 않음 |

각 페이지와 P&ID 상세/표제 확대는 extracts/LS02/*.png에 있다. PDF 파일명 Rev2를 모든 쪽의 개정으로 적용하지 않는다.

### 4.2 OEM 회로의 두 끝점

FG70/PDF71 두 번째 가지:

1. +24Vdc 10.7 공통선의 접속점→X1/132, 도면 5×20 2A F 표기→선70.2→LS-02 접점13.
2. LS-02 접점14→X1/133→E8.7 하향 교차참조 **124/7**.
3. FG124/PDF125 E8.7 상단 **70/3** 역참조→MOD10/CPU515 표기 입력 단자 **8**. 하단 LIMIT SWITCH LS-02 GATE “A” CLOSED VALVE PV-01.
4. E8.7 상단에 점선 SPARE가 함께 있다. FG70 회로/하단 설명/0607 RID126 사용과 상충하므로 미설치·삭제·항상0으로 결론내리지 않는다.

13/14의 열린 접점 도식은 자료의 접점 표현이다. 현재 게이트 위치별 0/1, NO/NC 실제 설치·작동, 현행 퓨즈 형식/정격/보호값을 확정하지 않는다. 전원 가지와 교차참조를 도면 관찰로 기록했으며 현장 측정/통전/강제입력은 수행하지 않았다.

### 4.3 참고 시공 케이블 경계

공개 원본 PDF21은 ENT2TB1→ENT2TB2→LS02를 그리며 LS02 끝점은 flexible16 가지2, 표의 케이블 `3_21=ENT+PV01-LS02A`, CVV, 1.0, 2심이다. PDF53 행3_21은 FROM PV-01 ENT2TB2, 설명 PV-01 A GATE → TO PV-01 LS-02, DC CVV 2C 1.0 SPARE0, 경로 E212, LEN3을 기록한다. 행3_8은 ENT2TB1→ENT2TB2 묶음(LS01/02/03/04), DC CVV12G1.0 SPARE3, RBD1/E210이다. 이것은 설계 케이블 식별 정보이며 현행 포설 길이/심선 결속 확인이 아니다.

OEM X1/132·133과 ENT2TB2의 개별 단자/케이블 심선 대응표는 미확보. LS03/04 표기를 독립 PLC 입력 추가로 해석하지 않는다. 외부 SEJIN 프로그램·운영 자료/사진은 취급하지 않았고 고정 저장소 공개 PDF만 정적 열람했다.

## 5. 알람·복구

선정 LS02 선언/직접 사용 경로에 LS02 고유 타이머·전용 알람·독립 reset을 확보하지 못했다. 부모 PV01 Gate A NOT_CLOSE/NOT_OPEN 및 부모 지연·유지·해제는 PV01 공통 조사에 남기며 LS02 소유 알람으로 복제하지 않는다. 부모 알람 하나로 LS02 센서 고장을 확정할 수 없다. Q5.2, EV01, 공압/CL01·CL02, 기계 위치, raw/DB/MEM과 표시를 분리해야 한다.

알람 해제=센서 복구나 기계 닫힘 완료가 아니다. 현장 복구·리셋·출력 강제·접점 우회·보호값 조정은 미수행. 검증된 시점의 원시 입력과 실제 접점/설치·현행 CPU 자료를 확보하기 전 현재 정상값을 기재하지 않는다.

## 6. 증상별 관찰

아래는 이미 승인된 관찰에서 모을 증거 필드이며 현장 조작·통전 측정·수리 지시가 아니다.

| 증상 | 구분해 기록할 위치/값 | 비교 근거·원인 배제 경계 | 필요한 자료 |
|---|---|---|---|
| 닫힘인데 I8.7 없음 | 실제 게이트/CL01 위치, LS02 표찰·접점 상태, X1/132·133 및 MOD10 채널 기록 시각 | FG70→FG124, 센서·전원·배선·입력채널 구분 | 승인 현행 배선/센서 설치·정상극성 |
| I8.7와 DB13X8.7 다름 | raw, DB Word8, 호출조건·프로젝트 근거를 동시 기록 | 0397 전달과 별도 DB 쓰기; raw=DB 가정 금지 | 현재 CPU 비교·호출/쓰기 증거 |
| 센서 변해도 MEM_CLOSE 유지 | Q5.2, ON, I8.7, DB13X8.7, DB2X8.0 | 0286 S/R, 순간 비트와 기억 구분 | 같은 시각 원시·기억·기계 위치 |
| HMI만 닫힘/닫힘표시 없음 | DB11X76.2, DB13X8.7, MEM_CLOSE 및 통신상태 | CSV 주소만으로 데이터 결속 완결 안 됨 | HMI 실제 이벤트/실인수·온라인 읽기 근거 |
| SPARE라고 표시된 채널의 고장 보고 | 현물 E8.7/센서/단자대 표찰과 승인 도면 개정 | SPARE·LS02 사용 상충 보존 | 변경 이력·준공도·현행 I/O 리스트 |

공통 기록: 관찰자·시각/시간대·장치/위치·값/단위·CPU/프로젝트 식별·비교 문서와 개정·배제 사실·승인된 조치·전후 복구 증거. 미관측 값은 공란이며 0으로 대체하지 않는다. 센서 제조사·모델·작동거리·토크·정비주기는 자료 미확보로 작성하지 않는다.

## 7. 완료·누락

| 영역 | 판정 | 확인/누락 |
|---|---|---|
| 설비·자료 기준 | 적용 | P&ID 리더/대장 부모 관계; 실물 동일성 미확정 |
| I/O·HMI | 적용 | I8.7/DB13X8.7/MEM/HMI 주소 분리; 표시 결속 미확정 |
| 제어 | 적용 | 닫힘 S/R·Word 전달·DB 다른 쓰기 정적 확인; 온라인 순서 미확정 |
| 전기 끝점 | 적용 | LS02 13/14→X1→MOD10 단자8, 124/7 정정; 심선/현행 보호 미확정 |
| 알람·복구 | 부모 연계 적용, 독립 근거 미확보 | 부모 항목 미복제; 현장 복구 미수행 |
| 증상 관찰 | 적용 | 원인 분리 필드; 실제 진단/수리 미수행 |
| 완료·누락 | 적용 | 문서와 UI/CPU/현장 분리 |

- 선정 원본/기준자료 **31개** 전체 SHA256·고정 Git blob 바이트 **31/31 일치**. 검사 JSON은 `extracts/LS02/source-verification.json`. 저장소 전체 검증 수가 아니다.
- 의미 검토: 실제 PDF **5페이지**(추가 확대2개는 별도 페이지로 중복 집계하지 않음), XML **4개 네트워크의 LS02 관련 가지/호출**, 선언 XML **11개 해당 선언**, 대장2행과 HMI CSV의 PV01 해당 주소. 기준문서/색인 해시 검사수를 PLC 의미 검토수로 합산하지 않는다.
- 695개 decoded XML의 LS[-_. ]*0?2(?!\d) 검색은 어휘 검색이며 의미 검토695개가 아니다. 일치 파일0609/0635와 검색 범위는 signal-search.json. 다른 명칭 신호 부재를 증명하지 않는다.
- 독립 검토 pending. 원본 저장소 Git clean 보존 확인. PDF 렌더·XML 파싱·해시/Git 바이트 검사를 수행했으며 앱/PLC 동작 검사가 아니다.
- 도면·래더 비교 링크용 근거 제공, 백업/선택복원·전후비교·보고서/PDF 기능은 구현/실행 미검증. 사용자 기록·미지 필드·저장키에 접근/변경하지 않았다.

| 최종 상태 | 결과 |
|---|---|
| documentation | draft_complete_with_gaps |
| static_review | self_review_complete; independent_review_pending |
| ui_records | not_run |
| publication | not_published_by_this_task |
| tia_compile | not_performed |
| live_cpu | not_performed |
| field_recovery | not_performed |

다음 한 확인은 승인 현행 LS02 설치/단자/심선/I/O 리스트로 FG124 SPARE 상충을 해소하는 것이다. 새 자료 없이 반복 조사하거나 현재 CPU·실물·정상극성·보호설정·현장복구를 완료로 바꾸지 않는다.

## 부록 A. 선정 전체 SHA256 / Git blob

경로는 source-mv06 기준. 고정 커밋은 `abcf31c5030bc7ef8749ed8e869a857f2387a28a`. Git blob 전체 바이트의 SHA256도 JSON에 별도 보관하며 모두 로컬 SHA와 같다. 부모 초안/배정 JSON은 탐색·배정 자료이며 아래 고정 원본 검사수에 포함하지 않았다.

| 상대경로 | 전체 SHA256 | Git blob | 바이트 일치 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | PASS |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | PASS |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | PASS |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | PASS |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | PASS |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | PASS |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | PASS |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | PASS |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | PASS |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | PASS |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | PASS |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | PASS |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | PASS |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | PASS |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | PASS |
| `all-in-one/sources/decoded-original/0286-FlgNet.xml` | `dca38f0104a47f95095b88a86400e379d653dd26b0e2fc88e1b3d17612268828` | `756366ed44352d07dd0b7af823d5493d84e920b8` | PASS |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | PASS |
| `all-in-one/sources/decoded-original/0410-FlgNet.xml` | `5a72ba5ae71e50ff277c3c52fcf94d4a2e71dff81897bafe72e7f3efc08986cd` | `5314b20676c0f2e4c08041071792232526fc65c4` | PASS |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | PASS |
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | PASS |
| `all-in-one/sources/decoded-original/0608-IdentXmlPart.xml` | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | PASS |
| `all-in-one/sources/decoded-original/0609-IdentXmlPart.xml` | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | PASS |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | PASS |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | PASS |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | PASS |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | PASS |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | PASS |
| `all-in-one/sources/decoded-original/0636-IdentXmlPart.xml` | `ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca` | `86114327ba1a010b2fcc01dd12b1bf86c01bc02c` | PASS |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | PASS |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | PASS |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | PASS |
