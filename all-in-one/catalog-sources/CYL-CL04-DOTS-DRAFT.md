# CYL-CL04 — PV01 하위 공압 실린더 고유 조사 초안

- 대상: CYL-CL04 한 개 / 공압 실린더 / component / parent PV01 / phase2 / depth1.
- 기준: GME-STD-1.0.0, source-mv06 고정 커밋 `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, 원본 프로그램 v1.12.0. 문서 기준일 2026-10-11 UTC.
- 범위: 원본 정적 조사와 자체 MD만. 대장·원본·공통 코드·버전·운영 기록·배포·PLC·현장·보호값·SEJIN 무변경. 시뮬레이터 작성·수정·생성·실행·행동시험, 앱 빌드와 원본 생성기 실행 없음.
- 상태: documentation=complete_with_gaps / static_review=targeted_completed / 독립 검토=부모 대기. UI/기록·게시·TIA·현재 CPU·현장 복구 미수행.
- 실행 모델/추론 수준: 도구로 독립 확인하지 못함. 설정이나 실행 증거를 추정하지 않음.

## 핵심 결과

1. P&ID 실제 PDF1의 `PV-01 Detail`에서 **EV-02의 두 공압 가지가 CL-03과 CL-04로 연결**된다. CL-04는 이 쌍의 별도 실린더 기호이며 독립 EV·PLC 출력 기호는 없다. 이것은 설계도 연결 근거이며 현장 실물 동일성 확인이 아니다.
2. **LS-05/06 표시는 CL-03 기호 쪽에 있고 CL-04 쪽에는 별도 리미트가 그려져 있지 않다.** 전기도면은 같은 LS05/06을 PV01 Gate B 열림/닫힘 입력으로 정의한다. 따라서 이를 CL04의 독립 위치 검출이나 두 실린더 모두의 완료 보증으로 전용하지 않는다.
3. 관련 공통 구동은 백업 Q5.3 → FG141 MOD15/14 → 69KA2 A1/A2 → 부하 접점 **5–9** → EV02이다. 부하 접점 1–9는 이전 부모 초안의 오류이며 정정 자료와 실제 렌더를 함께 적용한다.
4. CLIENT-CL04(Belt conveyor A)는 다른 catalog ID다. 숫자 CL04 일치로 모터·인버터·알람을 결합하지 않는다.
5. 전용 CL04 PLC 선언·HMI·알람·타이머·기계 제조사·스트로크·정상극성·현장 복구 근거는 미확보다. 아래 부모 신호는 모두 **공통 관계**로만 기술한다.

## 1. 설비·자료 기준

### 1.1 식별과 소유

`docs/equipment-standard/INVENTORY.json#/catalog/204`와 `all-in-one/registers/equipment.json`의 id=CYL-CL04는 PV01 하위 공압 실린더, 별칭 없음, 전용 electrical_fgs/fgs 빈 배열이다. `TASK3-BATCH19-SCOPE.json`과 `GME-CATALOG-OVERLAP-REVIEW.json`은 parent_child_separate 및 physical_identity_verified=false를 유지한다. 빈 FG 배열은 공통 구동 회로와의 관계가 없다는 뜻이 아니다.

P&ID PDF1(도면1684n002, Apex I, 원도일06/04/2011, 개정I 15/01/2013)의 `PV-01 Detail`을 이번에 직접 렌더·확대하였다. COMPRESSED AIR 공급이 EV02로, EV02 뒤 두 공압 가지가 CL03/04로 이어진다. 두 개 연결선은 기호 접속 사실로만 읽으며 포트 번호, 관경, 호스번호, 배관 길이, 전진/후진 정상방향 또는 스프링 복귀 방식은 표기 확보 없이 채우지 않는다. 인접 기계 그림의 GATE A/B 글자만으로 CL04의 실물 좌우/상하 위치를 확정하지 않는다.

### 1.2 기존 조사 재사용

부모 `gme-research/drafts/PV01-DOTS-DRAFT.md`를 공통 순서·알람·HMI 결속 탐색색인으로 재사용한다. 그 문서는 이전 커밋의 초안이며 이번 고정 원본 검사와 구분한다. `gme-research/extracts/PV01-PV02-contact-correction-20261011.md`의 69KA/71KA 실제 EV부하5–9 정정을 유지한다. 부모 전체 자동/공통 알람을 재조사하거나 CL04 독립 항목으로 복제하지 않았다.

## 2. I/O·HMI — 독립 항목 미확보, 부모 공유 관계 적용

아래 XML 경로의 접두는 `all-in-one/sources/decoded-original/`이다. 선언RID는 파일 내 범위이고 NID는 선언CS의 값이다. 모든 주소는 백업 주소이며 현행 CPU·배선·정상값은 미확정이다.

| 관계 신호 | 백업 주소/형식 | 직접 선언·접속 | CL04 소유 판단 |
|---|---|---|---|
| PV-01 GATE B EV | Q5.3 Bool | 0607 RID49, SAD Output/SSD AO43, NID4 UID390 Write; 0279 Coil377 operand W402/ORef390 | EV02를 통한 CL03/04 공통 구동. CL04 전용Q 아님 |
| EV02_Sel_Open | I9.3 Bool | 0607 RID45, Input AO75, NID3 UID351; 0278 Contact365 operand W357 | Gate B 현장 요청 |
| Open EV B 00 PV-01 | M20.1 Bool | 0607 RID46, Memory AO161, NID3 UID352 Write/NID4 UID386 read | 부모 현장 요청 메모리 |
| Open EV B 01 PV-01 | M21.1 Bool | 0607 RID21, Memory AO169, NID4 UID387 read, NID1/2 쓰기CS | 부모 자동 요청; 세부 순서는 부모 초안 참조 |
| maintenance PV01 | M80.5 Bool | 0607 RID47, Memory AO645, NID4 UID388/393 | A/B 공통 요청, 전용 CL04 아님; 작성 경로 미확정 |
| ON / OFF | M0.0 / M0.1 Bool | 0607 RID1/48, AO0/1, NID4 UID385/389 | 실제 메모리. true/false 상수로 대체 금지 |
| EV02_Open / EV02_Close | I9.0 / I9.1 Bool | 0607 RID129/131, Input AO72/73, NID12 UID40 /42·48 | LS05/06의 Gate B 원시입력. P&ID 센서가 CL03 쪽이므로 CL04 전용 검출 주장 금지 |
| Inputs.PV-01 GATE B OPEN / LS-06 closed | DB13.DBX9.0 /9.1 Bool | 0609 RID132/133 AO72/73, BAD BIRID86; 0608 RID86 TOD13; NID12 UID43/49 | 처리 DB 경로. 원시 I와 구별 |
| Flag.PV_01_GATE_B_MEM_OPEN / MEM_CLOSE | DB2.DBX8.3 /8.2 Bool | 0609 RID11/134 AO67/66, BAD BIRID5; 0608 RID5 TOD2; NID12 UID44/46 및50/52 | 부모 위치 기억, 물리 CL04 직접 위치 아님 |

AO는 bit offset이다. 43=5×8+3, 72=9×8로 주소를 확인했다. DB 이름이 유사해도 Inputs/Flag/raw I를 같은 변수로 병합하지 않는다.

HMI CSV `sources/hmi_plc_tags.csv`와 `PV01-detail/PV01-hmi-map.csv`의 PV_01\GateB_Open=DB11.DBX76.3, GateB_Close=76.4, Selector_GateB=76.6 및 Allarme1=76.0은 부모 PV01 설정 주소다. CL04별 버튼·상태·알람 화면이 아니다. 부모 조사에서 0391의 CRef32 `HMI PV_2Gate` 호출 실인수17개는 미결속 상태다. 본 조사에서 해소하지 않았고 HMI 명령이 직접 Q5.3을 쓴다고 확정하지 않는다. HMI 객체 이벤트·권한·현재 통신은 미확정이다.

`decoded-original/*.xml` 전체에서 정확 문자열 CYL-CL04/CL-04/CL04 검색 일치0을 보관했다. 검색은 탐색 결과일 뿐 전용 신호의 절대 부재나 실물 미설치 증거가 아니다.

## 3. 제어 구조 — EV02 공동 구동 경계

### 3.1 요청에서 출력

0278(LAD1914, 선언NID3): ON Contact361/W353/ORef348 → W362 → 현장입력 Contact365/W357/ORef351 → W366 → Coil347; operand W359/ORef352가 M20.1이다. 즉 부모 현장 B요청은 ON과 I9.3의 정적 직렬 관계다.

0279(LAD1915, NID4): ON Contact410(W395/ORef385) → W411에서 Contact412/414/416/418에 병렬 분기한다. 각 operand는 W396/ORef386(M20.1), W397/ORef387(M21.1), W398/ORef388(M80.5), W399/ORef389(M0.1)이다. W413/415/417/419가 OR372.in1~4, OR372.out W400이 Coil377.in, W402/ORef390이 Q5.3 operand다.

정적 식: Q5.3 = ON AND (OpenB00 OR OpenB01 OR maintenance PV01 OR OFF).

OFF Contact418은 비반전이며 literal false가 아니다. Enable 해제만으로 모든 요청 경로가 차단된다고 쓰지 않는다. 부모 허가·자동순서가 M21.1에 미치는 영향은 별도 경로다. Q5.3=0은 전기 명령 해제이며 CL04 기계 닫힘·안전 정지 확인이 아니다. 실제 호출·스캔·다른 쓰기·값은 검증하지 않았다.

### 3.2 응답과 기억

0287(LAD1922,NID12)에서 부모 B기억은 다음 경로다. CL04 독립 완료 변수로 이름을 바꾸지 않는다.

- OPEN Set: ON21 → Q22(W88/ORef89=RID49) → raw open23(W58/ORef40=RID129) OR [false24(W60/ORef41=0610 RID130) AND raw close25(W62/ORef42)] OR Inputs26(W64/ORef43=RID132) → OR27 → W66 → S28, operandW67/ORef44=RID11.
- OPEN Reset: ON → NOT Q29(W91/ORef92) → W90 → R30, operandW70/ORef46=RID11.
- CLOSE Set: ON → NOT Q31(W93/ORef94) → raw close32(W73/ORef48) OR Inputs close33(W75/ORef49) → OR34/W77 → S35, operandW78/ORef50=RID134.
- CLOSE Reset: ON → Q36(W96/ORef97) → W95 → R37, operandW81/ORef52=RID134.

0610 RID130/NID12 UID41은 Bool literal false다. 이는 M0.1 OFF와 다르다. 부모 startup 닫힘기억 설정·IW8→Inputs DB13 전달·자동 대기 조건은 기존 부모 분석을 재사용하며 이번에 재검토 완료로 중복 계수하지 않는다. MEM과 HMI가 정상이어도 CL04 자체의 기계 위치가 정상이라는 증거는 미확보다.

## 4. 전기·공압 전달 끝점

이번에 원본PDF를 실제 렌더한 페이지는 P&ID1과 Electrical_Rev2 PDF70/71/126/142, 총5쪽이다. 전기도면의 FG 번호와 실제 PDF 페이지를 구분한다.

| 도면/실제PDF/해당쪽개정 | 양 끝점과 직접 관찰 | 해석·경계 |
|---|---|---|
| P&ID1684n002 Apex I /PDF1 /개정I 15/01/2013, 원도06/04/2011 | COMPRESSED AIR → EV02 → 분기된 CL03·CL04 기호; LS05/06은 CL03 쪽 | CL04 구동관계 직접근거. 무번호 포트·호스·현장부품·정상방향 미확정 |
| FG141 /PDF142 /Rev2 17.03.2025, 기본일27.05.2024 | CPU515 MOD15 terminal14 A5.3, EV-02 VALVE COMMAND → 69/6 참조. 모듈공급 +24Vdc10.9 → X21/3033 5×20 4A F → 19, 20은 -0Vdc10.6 | 출력 모듈에서 릴레이 코일로 가는 경로. 현재 퓨즈/보호값 승인 아님 |
| FG69 /PDF70 /개정란 공란, 기본일27.05.2024 | A5.3/141/1 → 69KA2 A1, A2 → -0Vdc10.6. 110Vac9.7 → 69KA2 접점5–9 → wire69.3 → X1/128 5×20 2A F → wire69.4 → EV02 A1; EV02 A2 → X1/129 → 0Vac9.9 | 24Vdc 릴레이코일과110Vac EV부하 분리. 5–9 직접판독. 실린더 자체의 전기코일이 아님 |
| FG70 /PDF71 /개정란 공란, 기본일27.05.2024 | +24Vdc10.7 → X1/134 2A F →70.3→LS05 13/14→X1/135→E9.0(125/2); +24Vdc→X1/136→70.4→LS06 13/14→X1/137→E9.1(125/2) | Gate B 열림/닫힘 회로. CL04 전용 검출로 소유 전환 금지; 정상극성 미확정 |
| FG125 /PDF126 /개정란 공란, 기본일27.05.2024 | LS05 Gate B OPEN E9.0/70/4 → CPU515 MOD10 terminal11; LS06 CLOSED E9.1/70/5 → terminal12. B local E9.3 →terminal14 | 회로 양끝 및 입력 주소 결속. 도면 CPU515는 현행 CPU 증명 아님 |

FG70 요청 경로는 +24Vdc → X1/138 퓨즈 →70.5→70SB1 13/14→70.6→70SA1 Gate B 분기→X1/140→E9.3→FG125 MOD10/14다. 퓨즈 규격은 도면 표기만 기록하며 현장 설치·적정성 또는 변경 지시가 아니다. 상세 개별 케이블/심선과 CL04 배관 port 번호는 이 선정 도면에서 확정하지 못했다.

## 5. 알람·복구 — 부모 경보와 고유 실린더 고장 분리

CL04 독립 알람·타이머·Reset 선언 근거는 확보하지 못했다. 부모 PV01 B의 NOT_OPEN/NOT_CLOSE는 **부모의 명령과 위치기억 감시**이며 CL04 단독 고장 식별이 아니다. 기존 부모 초안 §5/E14·E15의 0450 및0656/0657/0658 추적을 공통근거로 재사용한다. B감시7초와 A감시4초를 CL04 시간값이나 스트로크 허용시간으로 복제하지 않는다. 부모 알람 해제·공통 Reset도 CL04 복구 승인과 다르다.

MEM_OPEN이 서더라도 CL03과CL04의 실제 동기 이동을 입증하지 못한다. 반대로 B알람만으로 CL04 파손을 특정하지 못한다. 공급공압·EV02·릴레이/전원·CL03센서·CL04기계 상태 등 경쟁 원인은 관찰자료가 있어야 분리된다. 자동 복구, 센서 우회, 강제출력, 지연 확대 또는 재가동을 이 초안이 지시하지 않는다.

## 6. 증상별 관찰 계획

실제 수리·동작시험 없이, 승인된 현장 절차에서 수집할 자료를 제시한다. 전기·공압 격리, 잔압·낙하·끼임 위험 통제와 자격자 절차를 선행해야 한다.

| 증상 | 같은 시각에 나눠 기록할 위치/값 | 배제 가능한 범위와 필요한 증거 |
|---|---|---|
| CL03은 움직이나 CL04는 움직이지 않음 | CL03/04 실물ID·위치, Q5.3, EV02 상태, CL04 분기배관·기계결합 상태 | 공통Q 정상만으로 CL04 정상을 판정하지 않음. 배관도/명판/승인된 관찰 필요 |
| 두 실린더 모두 움직이지 않음 | local/auto/maintenance/OFF 요청, Q, 69KA2코일/5–9부하, EV02전원, 공급공압 | 최초 불일치 경계를 찾되 전압/압력 실측은 자격자의 승인절차로 별도 수행 |
| HMI는 B열림인데 CL04 위치가 다름 | I9.0, DB13.DBX9.0, DB2.DBX8.3, HMI DB11.DBX76.3와 두 실린더 실제위치 | 센서의 CL03쪽 배치와 래치 특성, HMI미결속을 구분. HMI로 실린더 복구 보증 금지 |
| 출력해제 뒤 CL04가 닫히지 않음 | Q=0 시점, I9.1/DB13처리값/MEM_CLOSE, 각 로드·게이트 위치 | 무전압=닫힘 아님. 밸브구조/잔압/복귀기구/기계간섭 자료 미확보 |
| 부모 B알람이 리셋 후 다시 발생 | 부모 경보·Q·MEM·원시입력·물리 위치의 시간순 기록 | Reset 성공과 원인제거 분리. CL04만의 고장이라고 단정하지 않음 |

관찰 기록 필드: 관찰자, 일시·시간대, 실물ID, CPU·프로젝트판본, 측정위치, 값·단위, 수집장치, 비교원본·도면개정, 최초차이, 배제결과, 승인조치, 복구증거. 실제 사용자 기록/사진은 이 산출물이나 공개원본에 복제하지 않았다.

## 7. 완료·누락 및 인계

| 영역 | 적용 상태 | 이 초안의 완료/남은 경계 |
|---|---|---|
| 설비·자료 | 적용 | 고유ID·P&ID 분기 직접확인 / 실물 동일성 미확정 |
| I/O·HMI | 공유관계 적용·전용 근거미확보 | EV02 공동신호와 CL03쪽 센서 구분 / 독립CL04 신호·이벤트 미확보 |
| 제어 | 부모 공유 적용 | 최종출력·위치기억 원본핀 대조 / 현행 호출·작성자·CPU 미검증 |
| 전기 | 공유 끝점 적용 | PDF5쪽 및 EV부하5–9 확인 / 현행단자·배관·케이블 미확정 |
| 알람·복구 | 부모 공유 적용 | CL04독립 경보로 복제하지 않음 / 실제 원인·복구 미확보 |
| 증상·관찰 | 계획 적용 | 관찰항목과 구분경계 작성 / 현장수행 없음 |
| 완료·누락 | 적용 | 근거·해시·미확정 인계 / 독립검토·통합·게시 별도 |

네 기능(도면·래더 비교, 백업·선택복원, 전후기록 비교, 보고서/PDF)은 본 MD의 연구범위 밖이다. CL04 지원 구현·저장·재열기·다중탭·모바일UI·보고서 검증을 수행하거나 BC01동등 구현 완료라고 표기하지 않는다. 기존 note/repair_observation·미지필드·저장키를 변경하지 않았다.

필요 자료와 판정 기준:
- CL04 명판·설치 위치·도면 대응표: 독립 실물ID가 확인되어야 physical_identity_verified 판단 가능.
- 승인 공압 회로/배관 포트/밸브 스풀·실린더 모델·스트로크·기계 결합도: 실제 이동방향/복귀방식과 두 실린더 동기 관계 확인.
- 리미트 설치도·I/O as-built: LS05/06이 무엇을 실제 감지하며 CL04 별도센서가 있는지 확인. 단순 태그검색으로 대체 불가.
- 현행 PLC/HMI export 및 시간정렬 관찰: 백업 주소·MEM·HMI 결속과 현재 CPU를 구분.
- 승인된 원인제거/복구 기록: 경보해제와 실물복구를 따로 판정.

### 자체 검사 수와 의미검토 수

선정 고정원본 **22개**의 전체 바이트 SHA256과 고정 Git blob 전체바이트를 비교하여 **22/22 일치**했다. 그중 고유 주장에 대한 지정부분 의미검토 파일은 **13개**이고, 나머지9개는 규칙·재개상태 문맥 확인이다. PDF 의미검토는 전체265쪽 검토가 아닌 실제5쪽 및 P&ID부분확대다. XML전체 정확이름검색0은 의미검토 건수로 합산하지 않는다. 부모의 기존 조사·해시·UI/게시 실적을 이 실린더의 새 검증수로 계수하지 않는다.

검사JSON: `gme-research/extracts/CYL-CL04/source-byte-check.json`. 선언 발췌: `declaration-evidence.json`. 이름검색 범위/결과: `cl04-search.json`. 렌더 PNG와 텍스트는 같은 전용 폴더에 있다. 원본 worktree Git 상태는 착수·완료시 clean 확인한다. 추가 작업은 부모의 독립검토이며 미확정자료 없이 실물조사를 반복하지 않는다.

## 부록. 선정 원본 전체 SHA256·고정 Git blob 바이트대조

경로는 source-mv06 루트 상대경로다. SHA256은 원본 전체파일, Git blob은 고정커밋의 object ID이며 모든 행의 바이트비교는 PASS다. 의미검토와 해시검사는 위에서 분리하였다.

| 선정 원본 경로 | SHA256 | Git blob | 바이트일치 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | PASS |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | PASS |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | PASS |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | PASS |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | PASS |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | PASS |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | PASS |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | PASS |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | PASS |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | PASS |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | PASS |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | PASS |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | PASS |
| `all-in-one/sources/decoded-original/0278-FlgNet.xml` | `ef79acf030d84e4b67e257f43967a31bc362a7a7f3cbb7d120224eb3c475bac9` | `7be1a050b23efc861b6c662c03c9c00b965eada8` | PASS |
| `all-in-one/sources/decoded-original/0279-FlgNet.xml` | `4ae9c9ae70987b778a159c896b88fa4e34cf6f597903a0c68e630708b5f1bfd1` | `dfefe5fcd17064a89f61e38f34e9c4d7bb1d01e5` | PASS |
| `all-in-one/sources/decoded-original/0287-FlgNet.xml` | `885e0619ad4a49a2a873b4f0f069eafc62b350f4a12f060e4def9c020f3fe616` | `7911c5e5d9d9578f60012be454481ca434aaa831` | PASS |
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | PASS |
| `all-in-one/sources/decoded-original/0608-IdentXmlPart.xml` | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | PASS |
| `all-in-one/sources/decoded-original/0609-IdentXmlPart.xml` | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | PASS |
| `all-in-one/sources/decoded-original/0610-IdentXmlPart.xml` | `c58d07b1b9707dc8c6c2f06c34ee6142f72238a4cf3f376bee8502d1a9532f9d` | `1497b6bfd7fd9b8afe427b9c910d15e9cf888f9c` | PASS |
| `all-in-one/PV01-detail/PV01-hmi-map.csv` | `741dc6046067c027d1aec9c7fc44faa2876bb81d458e6c56acfc66004d83efd1` | `645a8357c4b7fd1f6a6a98a7532db6ca28439d7f` | PASS |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | PASS |
