# GME 작업 버전

## v1.2.0 — BC01 자료·기록 도구 · 2026-10-11

BC01(P01)의 전기도면/원본 래더 비교, 백업 가져오기/선택 복원, 저장 관찰 기록 전후 비교, 관찰 결과 보고서 인쇄/PDF와 전체 JSON 내보내기를 추가했습니다. 기존 원본·완료분·미지 필드·초안과 다른 설비 기록을 보존합니다.

프로그램·생성기·원본·MD·검증 기록을 main의 all-in-one/에 함께 보관합니다. 새 컴퓨터에서는 [WORKSPACE-HANDOFF.md](WORKSPACE-HANDOFF.md), 현재 작업은 [all-in-one/ACTIVE-WORK.md](all-in-one/ACTIVE-WORK.md)를 먼저 읽습니다. 고정 버전은 v1.2.0 태그/Release, 계속되는 최신 작업은 main을 사용합니다.

새 GitHub clone에서 설치/테스트/manifest/CSP 빌드를 확인했고 Netlify 게시 파일과 UI를 대조했습니다. 상세 근거는 [PUBLICATION_STATUS.md](PUBLICATION_STATUS.md), 기능 안내는 [BC01-RECORD-TOOLS-20261011.md](all-in-one/BC01-RECORD-TOOLS-20261011.md)입니다.

브라우저 점검 기록은 JSON 백업으로 별도 이동합니다. 시뮬레이터 영구 중지, 실제 PLC/현장 변경0이며 TIA/현재 CPU/실물/현장 복구 확인과 문서 검증을 구분합니다.
