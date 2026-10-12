# 작업 기록 — SYS-COUNTERS

- 표준/배치: GME-STD-1.0.0 / phase2 / REMAINING81
- 대상·이름·유형: SYS-COUNTERS / 생산량·가스·유량 계수 / software
- 부모·소유: 공통/외부/본체; 보존 백업의 문서·정적 참조입니다. 현재 호출·최종 Writer·HMI 이벤트·실물·정상 극성·TIA 컴파일·현장 복구는 확인 전입니다.
- 시작 커밋/버전: 93fa00c447229202bbffc4096c2fe004f12a83ae / v1.22.0 → v1.23.0
- 작업자/검토: 부모 단독 통합 + 최대2개 읽기전용 원본 조사/PDF 시각검토. 조사 요청 모델 GPT-6.1 Sol/Ultra; 부모 실행 모델/추론 런타임은 미확인.
- 작업 시각: 2026-10-12 Asia/Seoul. 최종 검사·게시 시각은 공통 검증 대장 참조.
- 백업: 기준 Git + 고정 v1.22 ZIP SHA0829195396edfcda4909faf407b65ad93dd7ab7341d5889f528142f0f5834729; 원본712/중지5 보존.
- 변경: catalog-profiles/SYS-COUNTERS.json, catalog-sources/SYS-COUNTERS-DOTS-DRAFT.md, catalog-guides/SYS-COUNTERS.html, 선택 native HTML anchor/도면 이미지와 공통 정적 자료.

## 7영역 적용표

| 영역 | 상태 | 작성 위치 · all-in-one 기준 | 경계 |
|---|---|---|---|
| 설비·자료 기준 | 원문/누락 명시 | catalog-guides/SYS-COUNTERS.html#overview | 고유·관련 소유와 미확정 구분 |
| I/O·HMI | 원문/누락 명시 | catalog-guides/SYS-COUNTERS.html#io | 고유·관련 소유와 미확정 구분 |
| 제어 구조 | 원문/누락 명시 | catalog-guides/SYS-COUNTERS.html#control | 고유·관련 소유와 미확정 구분 |
| 전기 전달 경로 | 원문/누락 명시 | catalog-guides/SYS-COUNTERS.html#circuits | 고유·관련 소유와 미확정 구분 |
| 알람·복구 | 원문/누락 명시 | catalog-guides/SYS-COUNTERS.html#alarms | 고유·관련 소유와 미확정 구분 |
| 증상별 수리 | 원문/누락 명시 | catalog-guides/SYS-COUNTERS.html#repair | 고유·관련 소유와 미확정 구분 |
| 완료 기준 | 원문/누락 명시 | catalog-guides/SYS-COUNTERS.html#completion | 고유·관련 소유와 미확정 구분 |

## 핵심 근거

검토 초안 SHA ca2aa1e637287fca278b27dc2a3d9090ce1f8fd13161fa7871f9f38e198c21a0. UI/PDF 확인 당시 자료 묶음 SHA 1578c2001e4192bf24e992f08ea15e5f5c7b9c8a1fb2ef0c32e730013bf04c0a. 최종 ACTIVE 감사 해시 갱신은 공통 보존 기록에서 비교합니다. 원본 위치52참조, 관찰6항목/증상2항목, 도면0참조/경로0입니다. 해당 고유 원문과 관련 소유 범위로 검토했고 다른 설비의 주소를 배정하지 않았습니다.

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
| publication | verified v1.23.0 | exact feature commit abaac928 / Netlify ready / 공개81 / freshclone; PUBLICATION_STATUS 최신 증거 참조 |
| tia_compile | not_performed | 현재 TIA 환경·프로젝트 필요 |
| live_cpu | not_performed | 온라인 PLC 읽기/쓰기 미수행 |
| field_recovery | not_performed | 실제 관찰·조치·복구 자료 필요 |

## 누락·다음 작업

- 원본 CSV의 HMI RESET_PROD_COUNT/GAS/BURNER_COUNT 요청은 선택한 원본 쓰기 위치나 Reset 회로에 대응시키지 못했습니다.
- Conta_prod/Conta_prod_TOT의 DB41 REAL과 Conta_gas1/TOT의 DB5 REAL이 보고 Int 계수에서 전달된다는 근거는 없습니다.
- 실제 펄스 단위·배율, 가스 적산 알고리즘, 오버플로, 전원 복귀 후 보존과 보고 기록 완료 응답은 미확인입니다.
- 현재 채널과 BWF 펄스 원본의 old-address 주석에 대한 확인이 필요합니다.
- 전기 회로나 카운터 Reset에 대한 실제 조작은 수행하지 않았습니다.

명령/종료코드·Netlify/Release/freshclone/ZIP/CSP·정리는 공통 REMAINING81-VERIFICATION.md를 확인합니다. 다음 작업은 새 증거에 따른 현재 프로젝트/TIA·실물·현장 대조이며 시뮬레이터 개발/실행은 영구중지입니다.

최종: v1.23.0 실제게시·공개UI·freshclone·합성테스트파일 정리 완료. 자료 공백·TIA·현재CPU·실물·현장 복구는 계속 미확정입니다.
