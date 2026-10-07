# 다른 컴퓨터에서 이어서 작업하기

## 준비된 파일

GitHub 계정: esp6662266. 대상 저장소: https://github.com/esp6662266/gme-plc-manual

GME_PROJECT_SOURCE_20261007.zip, GME_PLC_BACKUPS_20261007.zip, GME_TIA_PROJECT_FOLDERS_20261007.zip을 같은 폴더에 풀면 project 폴더에 합쳐진다. 원본 ZIP과 zap18, 2월 전체 프로젝트 폴더 ZIP은 backups에 있다. PACKAGE_MANIFEST.json의 SHA-256으로 내려받은 파일을 검증한다.

```powershell
git clone https://github.com/esp6662266/gme-plc-manual.git
cd gme-plc-manual
Expand-Archive -LiteralPath .\GME_PROJECT_SOURCE_20261007.zip -DestinationPath .\handoff
Expand-Archive -LiteralPath .\GME_PLC_BACKUPS_20261007.zip -DestinationPath .\handoff
Expand-Archive -LiteralPath .\GME_TIA_PROJECT_FOLDERS_20261007.zip -DestinationPath .\handoff
python .\handoff\project\scripts\verify-package.py .\handoff\project
```

Git을 쓰지 않으면 GitHub Code → Download ZIP으로 받을 수 있다. Python이 없어도 MD·HTML·PDF와 원본 백업은 열람·복사할 수 있다.

## 매뉴얼 편집

project/manual/manual.md가 수정 원본이다. 현재 PDF와 HTML은 그 원본의 2026-10-07 버전이다. 그림은 assets의 SVG를 편집하고 참조 CSV는 references에서 관리한다. source 폴더 경로와 무관하게 매뉴얼의 상대 링크를 유지한다.

```powershell
python -m pip install reportlab pypdf pillow
python .\handoff\project\scripts\rebuild-manual.py
```

이 명령은 기존 참조 CSV와 그림을 그대로 사용해 PDF를 갱신한다. HTML 갱신은 scripts 폴더에서 npm install marked 후 npm run html로 수행한다. HTML 이식용 스크립트는 본문·표·장 링크를 갱신하며 기존 시작 화면과 CSS를 보존한다. 원래 제작 스크립트는 scripts/original에 보관돼 있으나 현장 HMI 경로와 해당 PC의 라이브러리 경로에 의존한다. 이식용 스크립트는 그 경로에 의존하지 않는다. 한국어 PDF를 만들 때 Windows 맑은 고딕 또는 GME_FONT/GME_FONT_BOLD 환경 변수로 지정한 한국어 글꼴이 필요하다.

## 홈페이지 이어가기

완료된 Sites 구현은 project/sites/chatgpt-sites에 있다. Node.js 22.13 이상과 npm을 준비한다.

```powershell
cd .\handoff\project\sites\chatgpt-sites
npm ci
node scripts/sync-manual.mjs ../../manual
npm run build
```

이 ZIP에 보관한 Sites 소스는 호스팅 한도 때문에 배포하지 못한 버전이다. 다른 채팅에서 진행 중인 GitHub+Netlify 전환이 완료되면 저장소 루트의 Netlify 소스·설정과 최신 PUBLICATION_STATUS.md를 먼저 확인한다. 진행 중 Netlify 소스의 보관 시점 스냅샷은 project/sites/netlify-snapshot에 있으며 완료된 배포판 여부는 별도 확인한다. 진행 중 Netlify 소스의 보관 시점 스냅샷은 project/sites/netlify-snapshot에 있으며 완료된 배포판 여부는 별도 확인한다. 기존 Sites용 D1/R2 코드를 Netlify에 그대로 배포하지 않는다. 사이트 운영 데이터와 인증 상태는 소스 묶음에 들어 있지 않다.

## PLC 백업 열기

TIA Portal V18에서 backups의 원본 10월 1일 ZIP을 풀고 zap18을 Restore한다. 2월 프로젝트 폴더 ZIP은 전체 폴더를 풀고 그 안의 ap18을 연다. 원본은 보존하고 검토용 별도 복사본을 사용한다. TIA에서 프로젝트가 열리고 컴파일되는지와 현재 PLC 일치 여부는 이번 파일 검증의 범위 밖이다.

## 시뮬레이션 시작점

PROGRAM_STRUCTURE.md와 SIMULATION_PLAN.md를 읽고 PV01부터 독립 모델을 만든다. HMI 스크린샷은 화면 기준, CSV는 매핑 기준, 백업은 확인 가능한 로직의 근거다. 이미 구현된 시뮬레이터로 오해하지 않는다.

## 다음 채팅에 전달할 문장

> 이 저장소의 PROJECT_OVERVIEW.md, PROJECT_HISTORY.md, OTHER_PC_HANDOFF.md, PROGRAM_STRUCTURE.md, SIMULATION_PLAN.md와 PUBLICATION_STATUS.md를 먼저 읽어줘. GME DECOATER는 Siemens PLC/TIA V18과 AVEVA InTouch HMI를 사용해. 기준 자료와 미확인 조건을 유지하면서 매뉴얼·홈페이지·향후 시뮬레이션 작업을 이어가줘. 실제 PLC와 HMI는 문서 개발과 별도 대상이야.

## 변경 기록

수정 후 PROJECT_HISTORY.md와 매뉴얼 CHANGELOG.md에 근거·대상·검증 결과를 적고 Git 커밋을 남긴다. 백업 파일을 교체하면 파일명과 SHA-256, 프로젝트 버전과 출처도 갱신한다.
