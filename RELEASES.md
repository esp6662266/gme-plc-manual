# GME 작업 버전

## v1.3.0 — BC01 기록 보존·작업 재개 보완 · 2026-10-11

Python3.10+ 탐지 실행기, 파일 목록 양방향 검사와 승인 파일만 복사, 개별 전체 note JSON 내보내기/구형 호환을 보완했습니다. BC01에 선택 관찰8행을 추가하고 보고서/JSON의 생성 기준 버전·근거 해시, 향후 저장 기준, 단계 제목/자료 위치 변경 비교와 현재BC01/후속21개 표시를 제공합니다. 기존4행·다른22양식·원본·미지 필드/초안과 v1.2.0은 보존합니다.

작업 재개는 [WORKSPACE-HANDOFF.md](WORKSPACE-HANDOFF.md), 기능은 [BC01-PRESERVATION-20261011.md](all-in-one/BC01-PRESERVATION-20261011.md), 실제 검증·게시 결과는 [PUBLICATION_STATUS.md](PUBLICATION_STATUS.md)를 확인합니다. 최신 작업은 main, 고정 배포판은 v1.3.0 태그/Release입니다. 실제PLC/현장/SEJIN 변경0, 시뮬레이터 영구 중지입니다.

## v1.2.0 — BC01 자료·기록 도구 · 2026-10-11

BC01(P01)의 전기도면/원본 래더 비교, 백업 가져오기/선택 복원, 저장 관찰 기록 전후 비교, 관찰 결과 보고서 인쇄/PDF와 전체 JSON 내보내기를 추가했습니다. 기존 원본·완료분·미지 필드·초안과 다른 설비 기록을 보존합니다.

프로그램·생성기·원본·MD·검증 기록을 main의 all-in-one/에 함께 보관합니다. 새 컴퓨터에서는 [WORKSPACE-HANDOFF.md](WORKSPACE-HANDOFF.md), 현재 작업은 [all-in-one/ACTIVE-WORK.md](all-in-one/ACTIVE-WORK.md)를 먼저 읽습니다. 고정 버전은 v1.2.0 태그/Release, 계속되는 최신 작업은 main을 사용합니다.

새 GitHub clone에서 설치/테스트/manifest/CSP 빌드를 확인했고 Netlify 게시 파일과 UI를 대조했습니다. 상세 근거는 [PUBLICATION_STATUS.md](PUBLICATION_STATUS.md), 기능 안내는 [BC01-RECORD-TOOLS-20261011.md](all-in-one/BC01-RECORD-TOOLS-20261011.md)입니다.

브라우저 점검 기록은 JSON 백업으로 별도 이동합니다. 시뮬레이터 영구 중지, 실제 PLC/현장 변경0이며 TIA/현재 CPU/실물/현장 복구 확인과 문서 검증을 구분합니다.
