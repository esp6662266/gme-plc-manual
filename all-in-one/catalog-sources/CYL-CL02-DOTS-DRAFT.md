# CYL-CL02 공압 실린더 고유 원본 조사 초안

- 대상: CYL-CL02 한 개, parent PV01, component, phase2. 기준 GME-STD-1.0.0.
- 작성: 2026-10-11 UTC. 고정 원본 source-mv06 커밋 abcf31c5030bc7ef8749ed8e869a857f2387a28a, VERSION v1.12.0. 현행 배포·CPU라는 뜻은 아니다.
- 분류: INVENTORY catalog[202], batch19 및 overlap catalog_rows 모두 parent_child_separate. CLIENT-CL02 외부 모터와 별개이며 독립 실물 동일성은 확인 전이다.
- 범위: 정적 원본·도면 조사와 자체 초안만. 원본/공통코드/대장/버전/배포/PLC/현장/보호값/운영·SEJIN 변경 0. 시뮬레이터/원본 생성기/앱 빌드/행동시험 실행 0. 새 Work/Codex/재위임/업로드 없음.
- 실행 모델·추론 수준은 이 작업에서 독립 관측하지 못했으므로 미확인.

## 핵심 결과

1. P&ID PDF1 PV-01 Detail에 고유 CL-02가 있고, EV-01 이후 두 공압선이 CL-01와 CL-02로 분기한다. CL02는 EV02/CL03·04 계통과 구별된다. 각 실린더의 포트 번호·호스 번호는 원본에 제시되지 않는다.
2. LS01/LS02 라벨은 CL01 그림 쪽에 표시되며 CL02에는 별도 LS 라벨이 보이지 않는다. 이를 CL02 전용 센서나 LS03/LS04로 보충하지 않는다. 전기도면은 부모 GATE A의 위치 신호다.
3. Q5.2→69KA1→EV01 경로는 부모 공통 구동 관계이며 CL02 전용 PLC 출력이 아니다. EV01 부하 접점은 정정된 **5–9**다. 이전 PV01 초안의 1–9를 재사용하지 않는다.
4. P&ID의 GATE A/B 형상 문자와 전기도면 A/B를 위치만으로 결속하지 않는다. CL02의 실제 설치 위치, 운동 방향, 기계 링크, 독립 끝단 감시·복구는 미확정이다.

## 1. 설비·자료 기준 — 적용

[E1] docs/equipment-standard/INVENTORY.json#/catalog/202는 공압 실린더 CYL-CL02, parent_id PV01, depth1, existing_detail baseline, bc01_standard_acceptance not_assessed다. 부모 완료를 상속하지 않는다. progress/TASK3-BATCH19-SCOPE.json 및 GME-CATALOG-OVERLAP-REVIEW.json의 해당 행에서 이름 충돌 경계와 별도 조사 범위를 확인했다.

[E2] all-in-one/sources/PID_1684n002I.pdf 실제 PDF1, PV-01 Detail. 도면번호1684n002, 기본 날짜06/04/2011, Apex I, 최종 표제 개정행 I/15/01/2013 “REMOVED MC-05, CHANGED POWER OF FN-02”. 페이지 전체와 Detail/표제를 실제 렌더해 보았다. 오래된 P&ID 판본은 2024/2025 전기 백업과 동일 시점 자료로 취급하지 않는다. 장착 사진·승인 조립도 없이는 physical_identity_verified로 바꾸지 않는다.

고유 공압 끝점: COMPRESSED AIR 분기→EV-01→두 평행선→CL-01 및 CL-02 실린더 기호의 두 연결점. 실제 배관의 포트 A/B, 전진/후진, 무전원 복귀 방향, fail-safe 구조, 단동/복동의 실제 사양은 확인 전이다. 도면상 두 연결선만으로 제조사 모델·보어·스트로크·공급 설정을 채우지 않는다. 인접 GATE 형상으로 기계 결속을 확정하지 않는다.

부모 PV01-DOTS-DRAFT.md는 탐색색인 및 공통 순서/알람 근거로 재사용했다. 고유 조사에서는 P&ID CL02, 0279 출력부, 0607 관련 선언, 전기도면 끝점과 HMI 설정 범위만 재확인했다. 부모 전 프로그램을 다시 조사하거나 CL02 문서로 복제하지 않았다.

## 2. I/O·HMI — 부모 관계 적용, 독립 신호 근거 미확보

[E3] all-in-one/sources/decoded-original/0607-IdentXmlPart.xml의 SimpleAccess에서 ID, SSD.AO, SAD.R, CS.NID/UID를 함께 확인했다. 모두 Bool이다.

| 신호 | 선언/주소 | CL02에 대한 의미와 소유 |
|---|---|---|
| PV-01 Gate a | RID50, Output AO42=Q5.2, NID4 UID394 Write | EV01 공통 구동 출력. CL02 전용 출력 아님 |
| EV01_Open | RID124, Input AO70=I8.6, NID11 UID38 | 부모 A 열림 피드백. CL02 독립 위치 증명 아님 |
| EV01_Close | RID126, Input AO71=I8.7, NID11 UID44 | 부모 A 닫힘 피드백. LS02 SPARE 상충 보존 |
| ON | RID1, Memory AO0=M0.0, NID4 UID385 | 메모리 신호이며 상수 TRUE 아님 |
| Open EV A 00 PV-01 | RID44, Memory AO160=M20.0, NID4 UID391 | 부모 현장 요청 경로 |
| Open EV A 01  PV-01 | RID20, Memory AO171=M21.3, NID4 UID392 | 부모 자동 요청 경로 |
| maintenance PV01 | RID47, Memory AO645=M80.5, NID4 UID393 | 부모 유지보수 분기; CL02 개별 수동버튼 아님 |

[E4] all-in-one/sources/hmi_plc_tags.csv에서 PV_01의 Flag DB2,X5.0, Allarme1 DB11,X76.0, GateA_Open/Close DB11,X76.1/.2, GateB_Open/Close .3/.4, Selector_GateA/B .5/.6을 읽었다. 설정 CSV의 8개 부모 태그이며 현재값·객체 이벤트·쓰기 권한·실제 PLC 결속을 증명하지 않는다. CL02 독립 HMI 태그는 이번 검색에 없었다. PV01 공통 MEM/DB 처리·HMI 이벤트 미확정은 부모 자료를 참조하며 CL02 소유로 바꾸지 않는다.

검색 경계: decoded-original의 XML695파일에서 (?i)(?<![A-Z0-9])(?:CYL[-_ ]?)?CL[-_ ]?0?2(?![0-9]) 단순검색 0건. 이는 **어휘 검색**이며 695파일 의미검토 완료나 독립 기능 부재의 절대 증명이 아니다. 무명주소·별칭·누락 백업·현행 CPU의 CL02 기능은 배제하지 못한다. identity-search.json에 범위를 남겼다. CLIENT-CL02와 병합하지 않는다.

## 3. 제어 구조 — 공통 구동 결속 적용

[E5] all-in-one/sources/decoded-original/0279-FlgNet.xml, 0607 NID4의 A 출력 가지를 독립 확인했다.

- Powerrail W426→Contact410.in. ORef385 RefId1→W395→410.operand = ON.
- 410.out→W411→Contact420/422/424.in. 각각 operand는 W403/ORef391/RID44, W404/ORef392/RID20, W405/ORef393/RID47.
- 420.out→W421→OR Part380.in1, 422.out→W423→380.in2, 424.out→W425→380.in3.
- Part380.out→W406→Coil384.in, Coil384.operand←W408←ORef394 RefId50, 즉 PV-01 Gate a Q5.2.
- 이 가지의 접점들에는 Negated 표기가 없다. 정적 식은 ON AND (Open EV A 00 OR Open EV A 01 OR maintenance PV01)이다. 현재 스캔·다른 네트워크 쓰기·명령 허가·출력 우선순위를 이 한 네트워크만으로 확정하지 않는다. 이 출력부에 CRef 호출은 없다.

전달 구분: 부모 요청→Q5.2→69KA1 DC 코일→별도 AC 접점→EV01→공압 공통선→CL01/CL02→기계 움직임→부모 LS01/LS02. 최종 두 단계의 각 실린더 실물 운동/기계결속은 미확정이다. Enable, 자동 상태0~5, 위치 MEM, 부모 타이머·알람 전체는 기존 PV01 근거를 참조한다. 부모 순서를 CL02 독립 상태기계로 만들지 않는다. Q5.2=1만으로 CL02 전진·열림 완료를 판정할 수 없다.

## 4. 전기 전달 경로 — EV01 부모 끝점 적용, CL02 전기단자 미확보

[E6] all-in-one/sources/Electrical_Rev2.pdf를 직접 렌더했다. FG 번호와 실제 PDF 페이지, 개정란은 다음과 같다.

| FG / 실제 PDF | 해당 페이지 개정 | 직접 확인 범위 |
|---|---|---|
|69 / 70|개정란 공란, 기본 DATE27.05.2024|69KA1 코일·5/9 부하 접점·EV01 A1/A2·X1/126,127|
|70 / 71|개정란 공란, 기본 DATE27.05.2024|LS01/02 접점13/14·X1/130~133·E8.6/8.7|
|124 / 125|Rev2 17.03.2025|MOD10 단자7 E8.6, 단자8 E8.7와 SPARE 점선|
|141 / 142|Rev2 17.03.2025|MOD15 단자13 A5.2 EV01 VALVE COMMAND, FG69/3 교차참조|

제어측: FG141 MOD15/13 A5.2→FG69/3 69KA1.A1, A2→-0Vdc10.6. MOD15 공급 도면은 +24Vdc10.9, X21/3033(5×20 4A F 표기)와 141.1이 보이지만 현행 보호값으로 확정하지 않는다.

부하측: 110Vac9.7→69KA1 접점5–9→wire69.1→X1/126(5×20 2A F 도면표기)→wire69.2→EV01.A1. EV01.A2→X1/127→0Vac9.9. 접점 하단 표에1/5/9가 있다고 부하를1–9로 읽지 않는다. PLC 24Vdc와 EV01 110Vac 부하를 분리한다. EV01에서 CL02까지는 P&ID의 공압 연결이며 전기도면에서 CL02 코일·전기단자를 새로 만들지 않는다.

위치측: +24Vdc10.7→X1/130(2A F)→wire70.1→LS01.13/14→X1/131→E8.6→FG124 MOD10/7. 닫힘은 X1/132→wire70.2→LS02.13/14→X1/133→E8.7→MOD10/8. 도면상 GATE A OPEN/CLOSE이며 실린더 CL02 전용 센서라고 표시되지 않는다. 접점 심벌에서 현장 정상극성0/1을 추정하지 않는다.

소유·상충: FG70 LS02 회로와 0607 EV01_Close 선언은 존재하지만 FG124에는 SPARE 점선이 병기된다. 삭제·미설치·사용안함으로 해결하지 않는다. 원본 P&ID에는 CL02의 독립 케이블/단자/리미트·포트 번호가 없어 소유 결속을 보류한다. 부모 시공도 색인의 LS03/04 표기를 CL02에 번호순으로 배정하지 않는다. 시공 케이블표/실린더 명판/호스 라우팅/최신 승인도 추가 필요.

## 5. 알람·복구 — 부모 영향 적용, 독립 항목 미확보

CL02 자체 선언 알람·타이머·리셋 입력을 이번 범위에서 확보하지 못했다. PV01의 A/B 위치 기억 감시·지연·유지·공통 Reset은 부모 소유다. 기존 PV01 초안의 A4초/B7초를 CL02 독립 타이머로 복제하지 않는다. 이번 원본 의미검토는 해당 알람식을 재검토한 작업이 아니며 상세 발생식·Set/Reset은 부모 문서의 근거표를 사용한다.

부모 A 위치 불일치가 CL02 문제와 동반될 수 있으나 공압 공급·EV01·CL01·기계부·LS 배선 중 어느 하나인지 알람만으로 특정할 수 없다. 부모 알람 해제, MEM 변경, Q 명령 해제와 실린더 복구를 구분한다. 실제 복구·재요청·부하 운전 증거가 없으며 자동 재기동을 제안하지 않는다.

## 6. 증상별 관찰 — 적용, 현장 수행 없음

아래는 추가 증거의 수집 설계다. 강제출력·밸브 수동조작·배관 탈거·가압·보호변경·동작시험 지시가 아니다. 안전한 정지·에너지격리·잔압관리 및 현장 승인 절차는 담당자가 수립해야 한다.

| 증상 | 비교할 관찰 및 근거 | 해석 경계/추가 자료 |
|---|---|---|
|CL01과 CL02 움직임이 다름|동시각 두 실린더 위치, EV01 공통 명령, 외부 누기·연결상태 기록; P&ID 분기 비교|공통 Q 정상만으로 CL02 정상 아님. CL02 호스/기계링크/명판 필요|
|둘 다 움직임 없음|기존 관찰 가능한 Q5.2·69KA1/EV01 상태·공압 공급 표시를 같은 시각에 기록|전기와 공압 어느 쪽 결함인지 미결정. 실측은 자격자 절차 필요|
|부모 OPEN 표시인데 CL02 상태 불명|LS01 원시/부모 처리/표시와 CL02 실제 위치를 각각 기록|LS01이 CL02 독립 완주를 보증하지 않음. 센서 장착도 필요|
|부모 CLOSE 불일치|LS02 도면·I8.7·SPARE 상충과 현재 센서·단자 식별 대조|입력 극성·SPARE 의미·실린더 위치를 추정하지 않음|
|알람 해제 후 재발|부모 알람/요청/위치·시각 및 CL02 위치 변화의 기록 비교|알람 리셋을 복구 증거로 사용하지 않음|

관찰 필드: 관찰자, 시각/시간대, 설비 ID, 현장 표찰·위치, 프로젝트/CPU 근거, 원시/처리/표시 구분, 값·단위, 사진·도면 위치, 조치 전후, 배제한 원인, 복구 판단자. 실제 운영 사진·개인정보는 이 초안이나 공개 원본에 복사하지 않았다.

## 7. 완료·누락과 인계

| 영역 | 상태 | 완료 범위/누락 |
|---|---|---|
|설비·자료 기준|적용|CL02 고유 도면 및 EV01 분기 확인; 실물 동일성 미확정|
|I/O·HMI|부모 관계 적용/독립 근거 미확보|부모 Q/I 선언 확인; CL02 전용 태그·HMI 미확보|
|제어 구조|공통 관계 적용|0279 A 출력 핀 추적; CL02 독립 상태기계 없음으로 단정하지 않음|
|전기 전달|부모 EV01 적용/CL02 전기끝점 미확보|4 OEM 페이지 및 P&ID 확인; 공압 포트/호스·실물 미확정|
|알람·복구|부모 영향 적용/독립 근거 미확보|부모 항목 복제 안 함; 실제 복구 미수행|
|증상 관찰|적용|5개 관찰 시나리오; 현장 관찰 없음|
|완료 기준|적용|문서와 해시·정적 범위, UI·게시·CPU·현장 분리|

우선 추가자료: CL02 명판/표찰·장착 사진과 승인 조립도, EV01→CL02 포트/호스 식별, LS01/LS02 장착 소유와 최신 SPARE 설명, 현행 CPU·IO/HMI 이벤트 Export, 안전하게 수집한 동일시각 위치·상태 기록. 이 자료 없이 정상극성·모델·보호설정·구동방향·현장복구를 완료하지 않는다.

네 기능: 도면/래더 비교용 원본 위치와 소유 경계는 제공. 백업/선택복원·전후비교·보고서/PDF는 CL02 독립 구현 및 실제 검증하지 않았다. 기존 note/repair_observation·미지 필드/키·다른 설비/초안·운영기록을 보존한다.

상태: documentation=complete_with_gaps(조사초안), static_review=bounded_source_review_complete, independent_review=parent_pending, ui_records=not_run, publication=not_published, tia_compile/live_cpu/field_recovery=not_performed. BC01 동등 기능 완료나 전체 프로그램 검증을 뜻하지 않는다.

검사: 선정 원본15파일 SHA256 및 고정 Git blob 바이트일치15/15. 의미검토는 6개 자료(INVENTORY, PDF2종, XML2개, HMI CSV), PDF는 실제5페이지(P&ID1+OEM4). XML695개는 어휘검색만 했다. 파일 수/페이지 수/의미검토/검색수를 합산해 완료수로 만들지 않는다. source-verification.json 및 identity-search.json, 렌더 이미지와 선언 발췌가 자신의 extracts/CYL-CL02에 있다. 원본 Git status 공란 확인. preflight/생성기/시뮬레이션·UI·앱검사는 범위 밖이므로 실행하지 않았다.

## 부록 A. 선정 전체 원본 SHA256 / 고정 Git blob

경로는 source-mv06 기준. 다음 모든 파일은 commit abcf31c5030bc7ef8749ed8e869a857f2387a28a의 git cat-file blob 바이트와 직접 비교했다. 해시는 전파일 바이트이고 PDF 의미검토는 명시된 페이지만이다.

| 원본 경로 | SHA256 | Git blob | 바이트일치 |
|---|---|---|---|
| AGENTS.md | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | yes |
| .agents/skills/gme-equipment-rollout/SKILL.md | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | yes |
| docs/equipment-standard/WORK-STANDARD.md | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | yes |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | yes |
| docs/equipment-standard/INVENTORY.json | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | yes |
| VERSION.json | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | yes |
| WORKSPACE-HANDOFF.md | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | yes |
| PUBLICATION_STATUS.md | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | yes |
| EXPANSION-WORK.md | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | yes |
| all-in-one/ACTIVE-WORK.md | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | yes |
| all-in-one/sources/PID_1684n002I.pdf | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | yes |
| all-in-one/sources/Electrical_Rev2.pdf | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | yes |
| all-in-one/sources/decoded-original/0279-FlgNet.xml | `4ae9c9ae70987b778a159c896b88fa4e34cf6f597903a0c68e630708b5f1bfd1` | `dfefe5fcd17064a89f61e38f34e9c4d7bb1d01e5` | yes |
| all-in-one/sources/decoded-original/0607-IdentXmlPart.xml | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | yes |
| all-in-one/sources/hmi_plc_tags.csv | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | yes |

## 부록 B. 외부 조사색인 재사용 경계

- gme-research/progress/BATCH19-RESEARCH-INSTRUCTIONS.md: SHA256 `9edbb2bd6c733ecbceff7bcef669cbfaa255514f9d886b6b5730e052c28244a9`. 조사 지침/분류/탐색색인이며 고정 원본 Git blob 검사15건에 포함하지 않음.
- gme-research/progress/TASK3-BATCH19-SCOPE.json: SHA256 `3cd12b4cb15ef9543507407a72077785845c8749309b345ed230a10e3abfc5e2`. 조사 지침/분류/탐색색인이며 고정 원본 Git blob 검사15건에 포함하지 않음.
- gme-research/progress/GME-CATALOG-OVERLAP-REVIEW.json: SHA256 `027c2d89b034f3681dced7db98146ffd77eecfad116a1a94cac035ccbd598967`. 조사 지침/분류/탐색색인이며 고정 원본 Git blob 검사15건에 포함하지 않음.
- gme-research/drafts/PV01-DOTS-DRAFT.md: SHA256 `ed9c8d774ab53ab5c725580f22b076268bc157f09bdccd1a35518e3819670b9e`. 조사 지침/분류/탐색색인이며 고정 원본 Git blob 검사15건에 포함하지 않음.

부모 초안의 초기1–9 오류는 원문을 보존하되 이 문서에는5–9 정정만 사용했다. 부모의 현행게시나 CPU 검증 상태를 CL02로 상속하지 않는다. 다음 조치는 이 초안을 독립 검토하고 누락 현장자료를 별도 확보하는 것이다.
