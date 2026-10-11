# BATCH01 v1.16.0 — 다섯 설비 검증 완료 / 최종 공통검증·게시 대기

MV06/RD01/BR01/CC01/AB01 설비별 문서·정적·UI기록·PDF 검증 완료. CC01 전용데이터 미확보 유지·새자료전반복검색안함. AB01 본체 후보·TC01/02 기존입력2·기록신호0·주변알람7/타이머6참고·160UI/15쌍/실제JSON42445B/3→4복원/PDF2 확인. 필수14+2·npm test/NETLIFY build·패키지·GitHub·실제게시를 묶음1회 진행한다. 아직 Release/실제게시 없음·실제게시12/23 유지. 다음 HE01/P03/P04/P14·2차133 로컬 제외. [AB01 근거](BATCH01-AB01-VERIFICATION.md). 원본/중지/운영기록 보존·TIA/CPU/현장 미수행·PLC/SEJIN 변경0·전체goal active.

# BATCH01 v1.16.0 — CC01 미확보 경계 검증 완료/AB01 다음

MV06/RD01/BR01/CC01 설비별문서·정적·UI기록·PDF 검증완료. CC01 본체고유데이터와기록신호0 유지·주변참고만연결·새자료전검색반복안함. 공통빈자료/미지항목요약표시 회귀passed. AB01 독립통합→공통회귀/패키지/게시1회. 아직Release/실제게시 없음·실제게시12/23 유지. [CC01 근거](BATCH01-CC01-VERIFICATION.md). 전체goalactive·시뮬레이터/PLC/현장/보호값/SEJIN변경0.

# BATCH01 v1.16.0 설비별 검증 — BR01 완료/CC01 다음

MV06 기준점·RD01·BR01 문서/정적/UI기록/PDF 검증 완료. CC01→AB01 독립통합 후 공통 회귀/패키지/게시1회. v1.16.0 작성중·아직Release/실제게시 없음·실제게시12/23 유지. 원본/기존14/중지5/운영기록 보존·시뮬레이터/PLC/현장/보호값/SEJIN변경0. [BR01 근거](BATCH01-BR01-VERIFICATION.md). 전체goal active.

# BATCH01 v1.16.0 설비별 검증 진행 — RD01 완료/BR01 다음

MV06 검증기준점보존·RD01 문서/정적/224UI/8쌍/실제저장·복원/JSON/PDF3 passed. BR01→CC01→AB01 독립통합후묶음1회패키지/실제게시. v1.16.0 작성중·아직게시/태그/Release없음·실제게시12/23 유지. HE01/미확정식별3다음·2차133로컬제외. 원본/기존13/중지5/운영기록보존·시뮬레이터/PLC/현장/보호값/SEJIN변경0. [RD01 근거](BATCH01-RD01-VERIFICATION.md). 전체goal active.

# 5개 통합 묶음 BATCH01 — 로컬 기준점 보존 · 2026-10-11

묶음은 MV06(P21) → RD01(P06) → BR01(P11) → CC01(P10) → AB01(P12)이다. 설비별 원본·선언·핀·도면·소유 검토와 합성 기록의 저장/재열기 검증은 유지하고, 마지막 공통 회귀·패키지·GitHub·Netlify 실제 게시는 한 번 수행한다. 이후 묶음 크기는 이번 실제 게시 결과로 판단한다. HE01 및 P03/P04/P14는 다음 묶음이며 2차133 로컬 통합·게시는 제외한다.

MV06 v1.15.0은 문서/정적/2472 화면·10원본쌍/격리 기록·복원·충돌·Quota·A4 PDF3쪽 검증을 마친 로컬 기준점이다. 필수14+설비2 검증09:19:10.740539Z, 2801파일 ZIP53581069B SHA256 ab3ba89e8877ca72e76ee971214d779555d6fcb636cbe1212405e497b7372dde, CRC/전체해시/원본730/추가3/중지5 보존·NETLIFY build2830/CSP6/39 passed. 이 버전은 단독 게시하지 않는다. 실제 게시 완료는 여전히 MV03까지12/23=52.2%, 제외2개 별도12/21=57.1%다.

착수 전 전체 all-in-one 2801파일을 ../gme-phase1-before-20261011-v1.15.0에 백업하고 전체 SHA256을 대조했다. 공개 사이트의 실제 저장키 gme-all-in-one-notes-v1 / gme-all-in-one-drafts-v1은 읽기 전용으로 확인했으며 둘 다 null이다. 증거는 /tmp/gme-batch01-qa에 보존하며 운영 기록 변경은0이다.

Dots CC01/AB01/HE01 실제 첨부 본문을 수신·보존했다. 고정abcf31c/v1.12 기준 CC01 핵심34+검색XML695=729해시, AB01 83, HE01 79 전부 Git blob 일치. 현재 CC01 VERSION.json, HE01 all-in-one-data.json만 진행 버전의 기대 차이다. sources 원본은 모두 현재 일치하며 초안 수신은 게시 완료가 아니다. Dots의 추가248 사전 초안은 로컬 대상에 자동 편입하지 않는다.

현재 요청 GPT-6.1 Sol/High를 따르며 로컬 편집·검증·게시는 이 채팅에서 수행한다. 시뮬레이터 영구 중지/TIA·현재CPU·현장복구 미수행/실제PLC·현장·보호값·SEJIN변경0. 다음은 RD01(P06)의 독립 원본 검토·통합이다. 전체 goal active.

# MV06 v1.15.0 통합·검증 진행 — 2026-10-11

MV03 v1.14.0 실제게시완료(12/23=52.2%,제외2별도12/21=57.1%). MV06(P21)7영역·10원본쌍·11직접문서규칙/4중지 원자료 규칙·반전ON/≥5·≤−5/PIW286·20/2초Shot/300ms·150ms응답/엄격±2200동일FAULT·공통인버터同Q상충·HSC2결속21미결속/HMI4FALSE10미해석·START/RESET5–9·LS40/41대34/35·중복FLO4TB2A별개구간을 연결한다. Dots83고정SHA와19XML/선언·실제PDF18쪽 독립대조. 730원본/추가3/기존12/공통기록/중지5보존. UI/기록/PDF/패키지/게시검증중. TIA/CPU/현장not_performed·시뮬레이터/PLC/SEJIN변경0. 다음RD01·BR01수신91/100고정SHA일치;2차133로컬제외.

# MV03 v1.14.0 실제 게시 완료 — 2026-10-11

MV03(P20) 문서·정적·UI기록·패키지·실제게시 검증완료. 7영역55항목/7쌍/782위치85해시·2288화면·합성저장/통합복원3→4/0→1비교/동시성·Quota/A4 PDF3·fresh14+2/ZIP2801/원본730·새clone8/BC01/설비/NETLIFY/Gitclean passed. GitHub v1.14.0 asset630259669 digest ee5e6e7457023ab1e5ab1d2326cd8d48283e85ba500eb55088199f2f2adef28c/53483224B;Netlify6acb4df93484ca00082d7fa4 ready08:51:36.214Z/featureccbb18653eec17524d31b35a5a91ad78e311c7c7. 게시126파일(104exact22HTML)·실제P20/FG38PDF39/Part390강조·통합0/운영키null/warnerror0. 12/23=52.2%,제외2별도12/21=57.1%. AON문서는불변ZIP생성시pending기록보존;최신게시상태는이루트기록이다. 다음MV06(P21)독립검토·통합. RD01/BR01초안수신91/100고정SHA전부일치·VERSION만현재기대차이. Dots CC01 조사중. TIA/liveCPU/field not_performed·시뮬레이터/PLC/현장/보호값/SEJIN변경0·2차133 로컬제외. 전체goal active.

# MV03 v1.14.0 통합·검증 진행 — 2026-10-11

MV01 v1.13.0 실제게시완료(11/23=47.8%,제외2별도). MV03(P20)7영역·7원본쌍·27직접규칙/2opaque·150초방향응답/±3400명령누적 동일FAULT·끝단NOT·상대Q차단접점없음/NC하드웨어·HSC2결속21미결속·HMI4FALSE10미해석·PSH03/PSH02·버너요청상충·M17용량상충을 연결한다. Dots84고정SHA와19고유/공통XML/선언·PDF12쪽 독립대조. 원본730/추가3/기존11프로파일/공통기록/중지5보존. UI/기록/PDF/패키지/게시검증중. TIA/CPU/현장not_performed·시뮬레이터/PLC/SEJIN변경0. 다음MV06수신83SHA고정일치.

# MV01 v1.13.0 실제 게시 완료 — 2026-10-11

MV01(P19) v1.13.0 실제게시완료. 7영역44항목/7쌍/2068화면·격리저장/통합선택복원3→4/0→1비교/동시성·Quota/보고서/A4 PDF3·14+2/ZIP2801/원본730/Node8/새clone passed. GitHub asset630177314 digest7b97a40d.../53363097B;Netlify6acb4468104cd90008fc7de8 ready08:10:47.897Z/feature192d2cbb420bddc2abafda2ed3cec608521537f2·게시111파일(93exact18HTML)·실제P19/Part143/통합0/운영키null. 시뮬레이터/PLC/현장/보호값/SEJIN변경0,TIA/liveCPU/fieldnot_performed. AON문서는불변ZIP생성시pending기록보존. 다음MV03(P20)독립검토·통합;Dots MV06초안중. 2차133은현재로컬goal제외. 전체goal active.

# MV01 v1.13.0 통합·검증 진행 — 2026-10-11

PV02 v1.12.0 실제게시완료. MV01(P19) 7영역·7원본쌍·개폐반대출력/끝단차단·150ms응답/±2000명령누적 공통FAULT·엔코더리셋·HSC4결속/19미결속·CONT_S9미결속·HMI4FALSE/10미해석·ZT02 A/B펄스대시공AI를 연결한다. Dots고정78해시·15고유/공통XML와선언·PDF9쪽 독립대조. 기존10설비/712원본·89대장/미확정/운영기록/중지5보존. UI/기록/PDF/패키지/게시검증진행중. TIA/CPU/현장not_performed·시뮬레이터/PLC/SEJIN변경0. 다음MV03(P20) 수신초안.

# v1.12.0 PV02 — 실제 게시 완료

PV02 v1.12.0 실제게시완료: feature a2c4d601cce2ac02c40a399a5e31a6a2fa5bbde4, GitHub v1.12.0 ZIP53268558bytes/2801파일/SHA8adc5ef8e2bb83c7d0e071c4c50bc8cc5b0a948b848925361fcaa32fc4000582 일치. Netlify6acb3d916af9a700081c73cb ready/동일commit/2026-10-11T07:41:31.900Z. 새clone8테스트/BC01/설비/NETLIFYbuildpassed·Git변경0. 게시61파일40exact+21HTML동등·실제P07 71항목/FG71PDF72/Part724강조/통합기록0/warnerror0. 기존9/원본730/공통기록/중지5보존. 다음MV01 독립검토·통합, Dots MV03조사. TIA/CPU/현장미수행·시뮬레이터/PLC/SEJIN변경0. 전체goal active.

# PV02 v1.12.0 통합·검증 진행 — 2026-10-11

PV01 v1.11.1 정정 실제게시완료. PV02(P07) 7영역·8원본쌍·39직접규칙·MC04 OR허가·300/800ms전이·7초알람4·raw/Inputs/MEM·KF_KT SEC Bool0·Enable 예열Reset/생산Set·RD01/팬요청소유·HMI17미결속을 연결한다. Dots65원본해시 일치 및 핵심XML/선언·PDF9쪽 독립검토. 릴레이부하접점5/9로 정정하고 수신원문보존. 기존9설비/원본/미확정/운영기록/중지5보존. UI/기록/PDF/패키지/게시검증진행중. TIA/CPU/현장not_performed·시뮬레이터/PLC/SEJIN변경0. 다음MV01(P19) Dots조사.

# v1.11.1 PV01 정정 — 실제 게시 완료

PV01 v1.11.1 정정 실제게시완료: feature182ab86fbd067bdf0de898bb666080e2c6fa1c1a, GitHub v1.11.1 ZIP53181725bytes/SHA7bfcbde47deb57774c23d6b6efa90901090a667ccc39fcc75aea58d963d052fb 일치. Netlify6acb38d91fcbcb0007b633a6 ready/동일commit/2026-10-11T07:21:26.626Z. 새clone8테스트/BC01/설비/NETLIFYbuildpassed·Git변경0. 게시33파일32exact+1HTML동등·실제P05 5/9표시/1/9없음/warnerror0. 다음PV02 독립검토·통합, Dots MV01조사. TIA/CPU/현장미수행·시뮬레이터/PLC/SEJIN변경0.

# v1.11.1 PV01 접점 번호 정정 — 게시 확인 중

FG69/PDF70의 EV01/02 부하 경로는 69KA1/2 접점5–9이다. v1.11.0의1–9 설명은 검토 오류이며 v1.11.1에서 정정한다. 도면 하단 접점표에1/5/9가 있으나 실제 그린 부하 경로는5/9다. DC 코일 A1/A2·110Vac 부하·PLC 제어식·원본·기록 기능은 동일하다. v1.11.0 태그/ZIP/저장시점 근거와 Dots 수신 원문은 보존한다.

# v1.11.0 PV01 실제 게시 완료 — 다음 PV02

현재GitHub v1.11.0/Netlify동일2041fe8 ready. 문서71·372위치77해시·UI1608/8쌍/합성기록/A4 PDF3/14+2/ZIP/Node8/새clone/게시57파일passed. [검증](V1.11.0-VERIFICATION.md). PV02(P07)초안65원본해시일치수신·독립검토미완료; Dots다음MV01(P19)조사. 원본/기존8내용/미지필드·신호·타설비·초안/미확정보존. 시뮬레이터영구중지·PLC/현장/보호값/SEJIN변경0. 전체goal active.

# v1.11.0 PV01 통합·게시 진행

PV01(P05)7영역71항목·372위치77해시·8쌍·UI1608/합성기록/A4 PDF3/필수14+2/ZIP/Node8/NETLIFY빌드passed. GitHub/Netlify/새clone확인진행. 마지막실제게시는아래v1.10.0. 다음PV02(P07)초안65해시일치수신; Dots자체다음MV01(P19)조사. 시뮬레이터영구중지/실제PLC·현장·보호값·SEJIN변경0/2차133제외. 전체goal active. [검증](V1.11.0-VERIFICATION.md).

# 다른 컴퓨터에서 최신 GME 작업 재개 — v1.10.0

모든 설비 통합 백업·복원은 선택 설비와 관계없이 이 브라우저에 저장한 전체 메모·수리 기록을 JSON 한 파일로 내보냅니다. 메뉴의 “모든 설비 통합 백업·복원”을 열어 다운로드하거나 기존 전체/개별 JSON을 가져옵니다. 복원 미리보기는 설비·새 기록/충돌별 필터와50건 단위 페이지를 제공하며, 필터로 숨긴 선택도 전체 저장 건수에 포함합니다. 같은 설비·같은 ID는 기존 유지/가져온 값 복원/새 ID 복사, 다른 설비·같은 ID는 기존 유지/새 ID 복사를 선택합니다. 새 기록은 기본 추가, 충돌은 기본 기존 유지입니다. 기존에만 있는 기록·초안·미지 필드/행은 유지합니다. 가져온 저장 근거는 그대로 사용하고 이전 저장 근거는 backup_restore_history에 보존합니다. 통합 파일은64MiB/50,000건까지 지원하며 한계를 넘으면 잘라 내지 않고 차단합니다. 다운로드 문자열과 최종 병합 결과도 같은 검사로 확인합니다. P02와 FN04 같은 키를 명칭으로 합치지 않습니다.

**2026-10-11 후속 작업표준:** [GME-STD-1.0.0](docs/equipment-standard/WORK-STANDARD.md)과 [EXPANSION-WORK.md](EXPANSION-WORK.md)를 먼저 읽습니다. 저장소에 공유 스킬과 23행/248 ID 대장, GPT-6.1 Sol / Ultra 재개 문장을 추가했습니다. 현재 프로그램 소스는 v1.10.0입니다. PREP-01 공통 구조·FN04 시범을 완료하고 FN01/FN02/FN03/FN06를 추가·게시 확인하고 MC04도v1.9.1실제게시확인했고 VS01도v1.10.0실제게시확인했으며 게시/완료 여부와 다음 작업은 EXPANSION-WORK.md와 PUBLICATION_STATUS.md의 최신 항목을 확인합니다.

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
| all-in-one/ | 현재 BC01/FN04/FN01/FN02/FN03/FN06/MC04/VS01 매뉴얼·소스·생성기·원본·검증 문서 |
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

check:python은 Python 준비 확인입니다. 실행기는 Windows py -3, python3, python을 탐지하고 3.10 이상을 요구합니다. 특정 실행 파일은 GME_PYTHON에 경로 하나를 지정합니다(인자를 포함하지 않음). verify:manual은 단순 읽기 검사가 아니라 필수14검사 및 설비2검사와 manifest·GME-All-In-One-v1.10.0.zip 및 검증 보고서를 재생성합니다. Python 최적화로 검사가 생략되는 실행은 거부합니다. npm build 자체는 Python 없이 저장된 검증 패키지로 실행할 수 있습니다.

패키지에 새 파일을 넣을 때는 diff·내용을 검토한 뒤 GME_NEW_PACKAGE_FILES에 새 상대경로의 JSON 목록(예: ["새안내.md"])을 해당 실행에만 지정합니다. 새 파일 집합과 정확히 같아야 하며 성공 후 환경변수를 해제합니다. 기존 파일 삭제·미검토 개인 기록의 자동 포함은 허용하지 않습니다. ZIP은 버전별 Release 자산으로 올리고 예전 태그·ZIP은 덮어쓰지 않습니다.

로컬 주소는 http://127.0.0.1:8770/ 입니다. 내용 변경 후에는 필요한 생성기만 실행하고, 필수 검사 → manifest/ZIP → npm build → NETLIFY 환경의 CSP 일치 확인 → Git commit/push 순서로 진행합니다. npm build가 바꾼 netlify.toml도 커밋합니다. 원본 초기 가져오기용 build-manual.py/decode-backup.py와 시뮬레이터 생성/행동 시험을 일반 재개 명령으로 실행하지 않습니다.

## 브라우저 점검 기록 옮기기

프로그램·문서 최신본은 GitHub에서 받습니다. 브라우저의 모든 설비 통합 백업·복원에서 전체 메모·수리 기록을 JSON 한 파일로 옮깁니다. 모든 유효 대장/우선 키의 기록을 미리보고 충돌을 선택해 저장·재읽기·재열기로 확인합니다. 선택 설비 도구의 전후 비교/보고서는 실제 등록 프로파일을 따르며 현재 BC01/FN04/FN01/FN02/FN03/FN06를 지원합니다. P02와 FN04처럼 키가 다른 문맥을 합치지 않습니다. 초안·미지 항목을 보존하며 서버 자동 동기화와 실제 기록/인증 자료의 Git 업로드는 제공하지 않습니다.

## 다음 채팅 재개 문장

> 이 저장소의 .agents/skills/gme-equipment-rollout/SKILL.md, AGENTS.md, EXPANSION-WORK.md, docs/equipment-standard/WORK-STANDARD.md와 START-GPT61.md를 읽고 최신 Git 상태를 확인해 줘. GPT-6.1 Sol / High로 BC01 기준 확장을 최신 작업 기록의 다음 한 단계부터 진행해. 기존 제외·완료분·원본·미확정·브라우저 기록을 보존하고 문서/화면/현장 확인을 구분해. 시뮬레이터와 실제 PLC/현장/보호값 및 SEJIN 변경은 하지 마. 필요한 검증과 GitHub 인계 기록을 남겨 줘.

## Sparse checkout에서 커밋할 때

현재 작업 체크아웃의 sparse 규칙은 일부 변경/신규 파일의 일반 git add를 제외할 수 있습니다. 적용 중이면 git add --sparse로 검토한 경로를 추가하고 git diff --cached --stat 및 manifest와 Git 추적 파일을 대조한 뒤 커밋합니다. 새 GitHub clone에서 테스트/빌드로 누락을 확인합니다. v1.4.0의 첫 staging 누락은 후속 완전 소스 커밋으로 수정했습니다.
