# GME 설비 문서 — Dots 조사·초안 / Codex 반영·검증·게시 인계

2026-10-11. 사용자 요청: 자료 정리·문서 초안은 Dots가 직접, 코드 반영·검증·배포는 GPT-6.1 Sol / High에서 진행하며 새 창으로 옮긴다. 현재 채팅 01a12939-4d71-7e12-ab65-5ee9149d00d5의 목표는 사용자 명시 요청으로 paused. 원래 Ultra 채팅 01a128fa-707d-7c12-b804-aaa053591b66도 paused다. 부모는 새 설비 편집을 중단하고 인계만 한다.

## 현재 권위 있는 상태

- 저장소: /Users/kimbumjoo/Downloads/_Gemini - Google AI를 활용하는 방법_files/무제 폴더/output/gme-netlify-release-20261009
- Git main 마지막 커밋 341f26f35c99ab8a7e4928f9b981d523a291a8fd. 마지막 실제 게시 v1.6.0 FN02이며 PUBLICATION_STATUS.md에 근거가 있다.
- FN03(P17) v1.7.0은 미커밋 작성 상태. 기존 dirty를 보존하고 reset/덮어쓰기를 하지 않는다. 배포 완료로 세지 않는다.
- FN03 자체 프로파일: 7영역39항목(3/4/15/3/4/5/5), 소프트스타터 기동/TOR/FAULT3원본쌍, 원본 위치77/근거 해시43. type=motor_softstarter, 전용 아날로그/조절 루프 미확보.
- 독립 조사 완료: fn02_native_review 및 fn02_drawing_review가 FN03 원본/XML·도면을 읽기 전용으로 검토. 중요 오류 한 곳 수정: 표시용 Memo_M25_Running/FP_M25_Run declarations.kind는 원본0658의 SimpleAccess이며 GlobalAccess가 아니다. scope Global, M180.1/M180.2와 5핀은 원본 일치. access_kind Write/null/RW도 원본에 맞췄다.
- 수정 후 build-all-in-one.py 재생성 exit0, Node24 verify:equipment passed. 원본 SimpleAccess/UID/AK와 비교하는 회귀 단언 추가.
- requirements-audit verifier passed(수정 전 같은 감사 데이터): source hashes880/설비248/우선23, 시뮬레이터 불변/행동시험 미수행. preflight inventory_matches=true, source byte changes는 새 프로파일·안내 반영이다.
- 실제 FN03 로컬 초기 화면만 확인: http://127.0.0.1:8876/#view=manual&equipment=P17&scope=priority 에 v1.7.0, 39항목, M25/PSE·TOR/RUN 경계 표시. 화면 전체·기록·복원·비교·PDF·패키지·새clone·게시 검증은 아직 미수행.
- 로컬 QA 탭은 닫고 viewport override를 reset했다. 이번 FN03 합성 운영기록은 아직 만들지 않았다. 사용자 기존 브라우저 탭/SEJIN 운영기록은 수정하지 않았다.
- 로그 /tmp/gme-fn03-qa/equipment.log, /tmp/gme-fn03-data.log, /tmp/gme-fn03-audit.log. 임시 로그를 유일한 인계 근거로 삼지 말고 검사를 실제 재확인한다.
- package-lock.json의 기존 CRLF 보존 때문에 git diff --check가 변경 두 줄의 CR을 trailing whitespace로 보고한다. 버전 외 의존성/파일 전체 줄바꿈 변경은 하지 않았다. LF로 전체 변환하지 않는다.
- 백업 ../gme-phase1-before-20261011-v1.6.0 (all-in-one2801+루트6=2807); 이전 v1.4/v1.5 백업과 원본/불변태그/ZIP 보존.

## 분업과 사용량 원칙

Dots는 자체 클라우드 환경/브라우저에서 공개 GitHub 원본을 읽고 다음 설비 FN06(P18)의 자료 정리·7영역 초안·근거표·누락 목록을 작성한다. 이 초안 작업을 Work/Codex에 재위임하거나 새 Codex 작업을 만들지 않는다. 연결된 Mac 접근이 없다면 공개 소스에서 가능한 범위만 조사하고 로컬 상태가 필요한 곳은 미확인으로 남긴다. 연결 권한을 자동 확장하지 않는다.

Codex 새 창은 유일한 저장소 편집자다. 이미 작성된 FN03를 먼저 검증·게시 마무리하면서 Dots FN06 초안을 기다린다. 이후 Dots 산출물을 원본 근거와 대조하고 프로파일/생성기에 통합한다. 초안을 전부 다시 조사하지 않고 핵심 논리·소유/상충/미해석을 확인한다. Dots 초안이 없거나 접근이 막혔다면 이를 명시하고 기존 FN03 등 독립 검증을 진행한다. 자동 절감률/무료 무제한을 주장하지 않는다.

Dots 초안 산출물은 설비당 하나: FN06-DOTS-DRAFT.md 같은 첨부 문서. 7영역, 원본 파일/FG/PDF/Part/Wire/ORef/선언·주소·읽기쓰기·해석·미확정 경계, 핵심 논리/별칭 알람/본체·구동부 관계, 4기록 도구에 필요한 자체 원본쌍과 관찰 항목을 포함한다. Dots는 공통 코드/버전/완료대장/배포/운영기록을 변경하지 않는다. 다음 설비를 중복 처리하지 않도록 완료 초안과 다음 대상 한 개를 명시한다.

## 새 Codex 창의 실행 지침

1. 이 인계, AGENTS.md, EXPANSION-WORK.md, VERSION.json, WORKSPACE-HANDOFF.md, PUBLICATION_STATUS.md, all-in-one/ACTIVE-WORK.md 최상단을 읽고 Git 상태를 실제 확인한다.
2. 저장소 스킬 .agents/skills/gme-equipment-rollout/SKILL.md 및 WORK-STANDARD.md·FN03.md를 적용한다. 사용자 최신 GPT-6.1 Sol / High 지정이 과거 Ultra 기본보다 우선한다. TIA 원본 조사에는 tia-equipment-alarm-trace, PDF에는 pdf, 릴리스에는 release-artifact-review를 필요 범위로 사용한다.
3. FN03 검증 상태를 실제 결과로 갱신한다. 생성기 변경이 있으므로 BC01 및 기존 FN04/FN01/FN02와 FN03 전체 적용 항목 PC1280/모바일390·기본/큰 글자, 링크·검색·잘못된 URL·왕복·새로고침·원본쌍을 검증한다.
4. 격리 localhost 합성자료로 저장0/빈칸·재읽기/재열기, 복원 미리보기/선택/충돌, 미지행/필드·타설비·초안·키 보존, 실패/동시변경, 전후 비교, 보고서 변경차단, 실제 A4 PDF 렌더를 확인 후 QA 자료/패치를 정리한다.
5. 필요한 정적검사·14+설비2 검사/manifest/ZIP·원본730/추가3/중지5·Node24 npm test/build/NETLIFY CSP·fresh clone·GitHub tag/Release asset digest·실제 Netlify ready/commit_ref/게시 파일·UI를 확인한다. git add --sparse로 검토한 경로만 추가한다. 과거 태그/ZIP을 덮어쓰지 않는다.
6. FN03 완료 후 FN06 Dots 초안을 받아 다음 순서를 유지한다. 작업마다 상태/검증/다음 한 개를 남긴다.

Node PATH=/Users/kimbumjoo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin:$PATH (v24.19)
Python=/Users/kimbumjoo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
all-in-one이 원본이며 dist/옛ZIP에서 편집하지 않는다. build-control-spec.py는 정적 호출 경로 재확인 후에만. build-program-model.py/verify-virtual-plc.cjs 등 영구중지 자산을 작성·변경·생성·실행·행동시험하지 않는다.

## 목표 전체 — 줄이거나 완료 범위를 바꾸지 않음

사용자가 승인한1~4번 목표를 새 창에서 계속한다. FN01/FN02 완료분 보존, 현재 FN03 마무리 → FN06(P18) → MC04(P08) → VS01(P09); PV01(P05) → PV02(P07) → MV01(P19) → MV03(P20) → MV06(P21); 킬른/RD01(P06) → BR01(P11) → CC챔버/CC01(P10) → 재연소로/AB01(P12) → 열교환기/HE01(P13), 이어 P03/P04/P14 미확정 식별 조사. 본체 후보와 실물/제어 소유를 분리한다. 대장248/23/18/제외90/다른공정2/부모보류7/2차133 불변, 2차133은 이번 목표에서 제외.

원본·완료/미확정 분석·운영 기록·미지필드/다른설비/초안/저장키 보존. 실제 PLC/현장/보호값·SEJIN 데이터/사진/이력을 변경하거나 복제하지 않는다. field_verified=false, TIA/현재CPU/현장복구 not_performed를 유지하며 문서/UI/게시 결과로 현장 완료를 대신하지 않는다.

## Dots 전달 현황

새 Codex 작업 생성 확인: 01a12963-de06-7e93-bd10-71f025de4730 / local / create_thread model=gpt-6.1-sol, thinking=high. 2026-10-11 오후2:16 Dots '속슬이' 웹 대화에 FN06 자체 조사·초안 요청을 실제 발송했고 읽음·답변을 확인했다. 답변: FN06(P18)부터 자체 환경에서 조사·초안을 시작, 새 코딩 작업을 만들지 않음, 공개 GitHub 표준/원본 확인, Mac 인계 파일·로컬 스킬 접근 미확인. 초안 산출물은 아직 대기다. /tmp/gme-fn03-qa/dots-handoff.png 수신 화면 저장. 새 Codex thread active/인계 문서 및 스킬 읽기/전체목표 설정 메시지를 확인했고 navigate_to_codex_page(navigated=true)로 새 작업을 열었다. 현재 부모 목표 paused 확인 완료. 새 창이 전체 승인 범위를 계속한다.

Chrome에 사용자 Dots '속슬이' 대화 https://chatgpt.com/dots/home 가 열려 있다. 이 대화는 별도의 SEJIN 작업도 수행 중이므로 GME를 별도 조사 책임으로 추가하고 SEJIN 중단/범위변경을 지시하지 않는다. Dots 직접 API/플러그인은 발견되지 않았고, 사용자 명시 요청에 따라 브라우저 메시지로 GME 분업을 전달한다. 메시지 발송·응답/작업 시작은 UI 관측 후에만 확인한다. Codex 신규 창은 create_thread(model=gpt-6.1-sol,thinking=high)로 만든다.
