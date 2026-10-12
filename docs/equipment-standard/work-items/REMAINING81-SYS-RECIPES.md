# 작업 기록 — SYS-RECIPES

- 표준/배치: GME-STD-1.0.0 / phase2 / REMAINING81
- 대상·이름·유형: SYS-RECIPES / 레시피·설정값 관리 / software
- 부모·소유: 공통/외부/본체; 보존 백업의 문서·정적 참조입니다. 현재 호출·최종 Writer·HMI 이벤트·실물·정상 극성·TIA 컴파일·현장 복구는 확인 전입니다.
- 시작 커밋/버전: 93fa00c447229202bbffc4096c2fe004f12a83ae / v1.22.0 → v1.23.0
- 작업자/검토: 부모 단독 통합 + 최대2개 읽기전용 원본 조사/PDF 시각검토. 조사 요청 모델 GPT-6.1 Sol/Ultra; 부모 실행 모델/추론 런타임은 미확인.
- 작업 시각: 2026-10-12 Asia/Seoul. 최종 검사·게시 시각은 공통 검증 대장 참조.
- 백업: 기준 Git + 고정 v1.22 ZIP SHA0829195396edfcda4909faf407b65ad93dd7ab7341d5889f528142f0f5834729; 원본712/중지5 보존.
- 변경: catalog-profiles/SYS-RECIPES.json, catalog-sources/SYS-RECIPES-DOTS-DRAFT.md, catalog-guides/SYS-RECIPES.html, 선택 native HTML anchor/도면 이미지와 공통 정적 자료.

## 7영역 적용표

| 영역 | 상태 | 작성 위치 · all-in-one 기준 | 경계 |
|---|---|---|---|
| 설비·자료 기준 | 원문/누락 명시 | catalog-guides/SYS-RECIPES.html#overview | 고유·관련 소유와 미확정 구분 |
| I/O·HMI | 원문/누락 명시 | catalog-guides/SYS-RECIPES.html#io | 고유·관련 소유와 미확정 구분 |
| 제어 구조 | 원문/누락 명시 | catalog-guides/SYS-RECIPES.html#control | 고유·관련 소유와 미확정 구분 |
| 전기 전달 경로 | 원문/누락 명시 | catalog-guides/SYS-RECIPES.html#circuits | 고유·관련 소유와 미확정 구분 |
| 알람·복구 | 원문/누락 명시 | catalog-guides/SYS-RECIPES.html#alarms | 고유·관련 소유와 미확정 구분 |
| 증상별 수리 | 원문/누락 명시 | catalog-guides/SYS-RECIPES.html#repair | 고유·관련 소유와 미확정 구분 |
| 완료 기준 | 원문/누락 명시 | catalog-guides/SYS-RECIPES.html#completion | 고유·관련 소유와 미확정 구분 |

## 핵심 근거

검토 초안 SHA 2506273efe61e4ab78ee9fbf9d4a356478e255c957437a0196a945495e573ff7. UI/PDF 확인 당시 자료 묶음 SHA f5f7fcffcceeb1bff21904705fd8c2366ff9e0625918fbff359a16ef8495f9f5. 최종 ACTIVE 감사 해시 갱신은 공통 보존 기록에서 비교합니다. 원본 위치15참조, 관찰5항목/증상2항목, 도면0참조/경로0입니다. 해당 고유 원문과 관련 소유 범위로 검토했고 다른 설비의 주소를 배정하지 않았습니다.

## 네 기능과 기록 보존

- 도면·원본 비교: 확보한 관련 도면·native 위치의 실제 UI 확인, 전용 대응 미확보는 숨김/경계 명시.
- 백업·복원: 묶음 공통1회235합성기록, 기존73/0/빈값/미지false 보존, 새 프로필 최종 재열기 일치. 개별 백업 반복 안 함.
- 전후 비교: 해당 양식의 고유 신호·증상 항목과 0→빈값 차이를 실제 화면에서 확인.
- 보고서/PDF: 저장값·주소·원본·생성 기준 hash, A4/12mm 여백과 전 페이지 시각검토. 운영 기록이 아닌 합성 자료.

## 최종 상태

| 구분 | 상태 | 근거 |
|---|---|---|
| documentation | complete_with_gaps | 원본·7영역·누락/비해당·소유 명시 |
| static_review | passed; unavailable refs explicit | 원본 critical/설비/catalog 및 최종14검사 공통 로그 |
| ui_records | passed | validation/remaining81/headless-verification.json |
| publication | pending | 실제 ready/commit/공개 검증 전; PUBLICATION_STATUS 최신 증거 참조 |
| tia_compile | not_performed | 현재 TIA 환경·프로젝트 필요 |
| live_cpu | not_performed | 온라인 PLC 읽기/쓰기 미수행 |
| field_recovery | not_performed | 실제 관찰·조치·복구 자료 필요 |

## 누락·다음 작업

- 원래 줄바꿈·주석 경계를 보존한 컴파일 소스, recipesdb 배열의 실제 상·하한·형식·Retain과 DB 멤버 절대 주소는 미확인입니다.
- HMI 선택·편집 제어 요청 이벤트, 권한, 펄스·래치와 실제 Data 운전 쓰기 주체는 미확인입니다.
- 원본 DB 선언 없이 HMI DB26 절대 주소 범위를 이름만으로 recipesdb 멤버에 대응시키지 않습니다.
- 동시에 들어온 save/undo/load 요청의 순서와 end_if 경계의 불명확성은 현재 TIA에서 확인해야 합니다.
- 현재 OB 실행 일정과 외부 쓰기는 미확인입니다. active_recipe가 설정값의 지속적인 일치를 보장하지 않습니다.

명령/종료코드·Netlify/Release/freshclone/ZIP/CSP·정리는 공통 REMAINING81-VERIFICATION.md를 확인합니다. 다음 작업은 새 증거에 따른 현재 프로젝트/TIA·실물·현장 대조이며 시뮬레이터 개발/실행은 영구중지입니다.
