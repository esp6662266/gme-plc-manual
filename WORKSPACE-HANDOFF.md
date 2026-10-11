# 다른 컴퓨터에서 최신 GME 작업 재개 — v1.9.1

모든 설비 통합 백업·복원은 선택 설비와 관계없이 이 브라우저에 저장한 전체 메모·수리 기록을 JSON 한 파일로 내보냅니다. 메뉴의 “모든 설비 통합 백업·복원”을 열어 다운로드하거나 기존 전체/개별 JSON을 가져옵니다. 복원 미리보기는 설비·새 기록/충돌별 필터와50건 단위 페이지를 제공하며, 필터로 숨긴 선택도 전체 저장 건수에 포함합니다. 같은 설비·같은 ID는 기존 유지/가져온 값 복원/새 ID 복사, 다른 설비·같은 ID는 기존 유지/새 ID 복사를 선택합니다. 새 기록은 기본 추가, 충돌은 기본 기존 유지입니다. 기존에만 있는 기록·초안·미지 필드/행은 유지합니다. 가져온 저장 근거는 그대로 사용하고 이전 저장 근거는 backup_restore_history에 보존합니다. 통합 파일은64MiB/50,000건까지 지원하며 한계를 넘으면 잘라 내지 않고 차단합니다. 다운로드 문자열과 최종 병합 결과도 같은 검사로 확인합니다. P02와 FN04 같은 키를 명칭으로 합치지 않습니다.

**2026-10-11 후속 작업표준:** [GME-STD-1.0.0](docs/equipment-standard/WORK-STANDARD.md)과 [EXPANSION-WORK.md](EXPANSION-WORK.md)를 먼저 읽습니다. 저장소에 공유 스킬과 23행/248 ID 대장, GPT-6.1 Sol / Ultra 재개 문장을 추가했습니다. 현재 프로그램 소스는 v1.9.1입니다. PREP-01 공통 구조·FN04 시범을 완료하고 FN01/FN02/FN03/FN06를 추가·게시 확인하고 MC04도v1.9.1실제게시확인했으며 게시/완료 여부와 다음 작업은 EXPANSION-WORK.md와 PUBLICATION_STATUS.md의 최신 항목을 확인합니다.

최신 작업 원본은 이 저장소 main의 all-in-one/입니다. 버전명은 VERSION.json, 고정 배포판은 게시 확인된 버전 태그, 게시 확인은 PUBLICATION_STATUS.md입니다. 예전 ZIP·OTHER_PC_HANDOFF.md·시뮬레이션 계획은 과거 자료이며 이 문서와 AGENTS.md, all-in-one/ACTIVE-WORK.md를 우선합니다.

## 처음 내려받기

Windows/macOS/Linux에서 Git과 Node.js 24를 준비합니다. 기존 원본의 줄바꿈과 해시를 유지하도록 다음 명령을 사용합니다.

```sh
git -c core.autocrlf=false clone https://github.com/esp6662266/gme-plc-manual.git
cd gme-plc-manual
git config core.autocrlf false
git status --short
git log -1 --oneline
npm ci
npm test
npm run build
```

npm build는 저장소의 실제 파일 목록과 manifest를 양방향 대조하고 원본·중지 자산 해시를 검사한 뒤 승인된 파일만 dist/에 복사합니다. 복사 후 해시도 확인하며 누락·추가 파일·심볼릭 링크는 차단합니다. 별도 Mac 폴더·/private/tmp·옛 ZIP 해제가 필요하지 않습니다. 현재 정적 웹 빌드를 새 clone에서 확인했으며 Windows 실제 장비에서의 TIA/PLC 실행 검증은 별도입니다.

## 기존 컴퓨터에서 최신 작업 받기

```sh
git status --short
git fetch origin --tags
git switch main
git pull --ff-only origin main
git log -1 --oneline
```

수정 파일이 있으면 먼저 diff와 백업/커밋을 확인합니다. 미완료 작업을 강제로 reset하거나 덮어쓰지 않습니다. 최신 main은 이후 작업을 포함할 수 있으며 특정 배포판을 확인하려면 확인하려는 버전 태그의 별도 복사본을 사용합니다.

## 작업 위치와 검증

| 경로 | 역할 |
|---|---|
| all-in-one/ | 현재 BC01/FN04/FN01/FN02/FN03/FN06/MC04 매뉴얼·소스·생성기·원본·검증 문서 |
| all-in-one/ACTIVE-WORK.md | 가장 최근 목표·범위·완료/미확정 상태 |
| all-in-one/BC01-RECORD-TOOLS-20261011.md | 새 네 기능과 기록 이동·검증 결과 |
| all-in-one/BC01-PRESERVATION-20261011.md | v1.3 선택 관찰·전체 note 내보내기·근거 버전 안내 |
| scripts/ | Python 실행기·파일 목록/해시 검증·정적 웹 복사·CSP 생성 |
| manual/,src/,netlify/ | 기존22장 홈페이지·자료실·인증/저장 구성 |

Python 3.10 이상이 있으면 다음 명령으로 BC01 검사와 필수14검사·ZIP 검증을 재실행합니다. Python 작업은 UTF-8 모드로 실행합니다. Windows에서 전체 문서 재생성이 필요하면 WSL 환경을 사용하며 native Windows 생성기의 전체 호환성은 별도 검증 대상입니다.

```sh
npm run check:python
npm run verify:bc01
npm run verify:equipment
npm run verify:manual
npm run serve:manual
```

check:python은 Python 준비 확인입니다. 실행기는 Windows py -3, python3, python을 탐지하고 3.10 이상을 요구합니다. 특정 실행 파일은 GME_PYTHON에 경로 하나를 지정합니다(인자를 포함하지 않음). verify:manual은 단순 읽기 검사가 아니라 필수14검사 및 설비2검사와 manifest·GME-All-In-One-v1.9.1.zip 및 검증 보고서를 재생성합니다. Python 최적화로 검사가 생략되는 실행은 거부합니다. npm build 자체는 Python 없이 저장된 검증 패키지로 실행할 수 있습니다.

패키지에 새 파일을 넣을 때는 diff·내용을 검토한 뒤 GME_NEW_PACKAGE_FILES에 새 상대경로의 JSON 목록(예: ["새안내.md"])을 해당 실행에만 지정합니다. 새 파일 집합과 정확히 같아야 하며 성공 후 환경변수를 해제합니다. 기존 파일 삭제·미검토 개인 기록의 자동 포함은 허용하지 않습니다. ZIP은 버전별 Release 자산으로 올리고 예전 태그·ZIP은 덮어쓰지 않습니다.

로컬 주소는 http://127.0.0.1:8770/ 입니다. 내용 변경 후에는 필요한 생성기만 실행하고, 필수 검사 → manifest/ZIP → npm build → NETLIFY 환경의 CSP 일치 확인 → Git commit/push 순서로 진행합니다. npm build가 바꾼 netlify.toml도 커밋합니다. 원본 초기 가져오기용 build-manual.py/decode-backup.py와 시뮬레이터 생성/행동 시험을 일반 재개 명령으로 실행하지 않습니다.

## 브라우저 점검 기록 옮기기

프로그램·문서 최신본은 GitHub에서 받습니다. 브라우저의 모든 설비 통합 백업·복원에서 전체 메모·수리 기록을 JSON 한 파일로 옮깁니다. 모든 유효 대장/우선 키의 기록을 미리보고 충돌을 선택해 저장·재읽기·재열기로 확인합니다. 선택 설비 도구의 전후 비교/보고서는 실제 등록 프로파일을 따르며 현재 BC01/FN04/FN01/FN02/FN03/FN06를 지원합니다. P02와 FN04처럼 키가 다른 문맥을 합치지 않습니다. 초안·미지 항목을 보존하며 서버 자동 동기화와 실제 기록/인증 자료의 Git 업로드는 제공하지 않습니다.

## 다음 채팅 재개 문장

> 이 저장소의 .agents/skills/gme-equipment-rollout/SKILL.md, AGENTS.md, EXPANSION-WORK.md, docs/equipment-standard/WORK-STANDARD.md와 START-GPT61.md를 읽고 최신 Git 상태를 확인해 줘. GPT-6.1 Sol / High로 BC01 기준 확장을 최신 작업 기록의 다음 한 단계부터 진행해. 기존 제외·완료분·원본·미확정·브라우저 기록을 보존하고 문서/화면/현장 확인을 구분해. 시뮬레이터와 실제 PLC/현장/보호값 및 SEJIN 변경은 하지 마. 필요한 검증과 GitHub 인계 기록을 남겨 줘.

## Sparse checkout에서 커밋할 때

현재 작업 체크아웃의 sparse 규칙은 일부 변경/신규 파일의 일반 git add를 제외할 수 있습니다. 적용 중이면 git add --sparse로 검토한 경로를 추가하고 git diff --cached --stat 및 manifest와 Git 추적 파일을 대조한 뒤 커밋합니다. 새 GitHub clone에서 테스트/빌드로 누락을 확인합니다. v1.4.0의 첫 staging 누락은 후속 완전 소스 커밋으로 수정했습니다.
