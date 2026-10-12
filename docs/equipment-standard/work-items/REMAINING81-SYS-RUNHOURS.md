# 작업 기록 — SYS-RUNHOURS

- 표준/배치: GME-STD-1.0.0 / phase2 / REMAINING81
- 대상·이름·유형: SYS-RUNHOURS / 모터 운전시간·정비 이력 / software
- 부모·소유: 공통/외부/본체; 보존 백업의 문서·정적 참조입니다. 현재 호출·최종 Writer·HMI 이벤트·실물·정상 극성·TIA 컴파일·현장 복구는 확인 전입니다.
- 시작 커밋/버전: 93fa00c447229202bbffc4096c2fe004f12a83ae / v1.22.0 → v1.23.0
- 작업자/검토: 부모 단독 통합 + 최대2개 읽기전용 원본 조사/PDF 시각검토. 조사 요청 모델 GPT-6.1 Sol/Ultra; 부모 실행 모델/추론 런타임은 미확인.
- 작업 시각: 2026-10-12 Asia/Seoul. 최종 검사·게시 시각은 공통 검증 대장 참조.
- 백업: 기준 Git + 고정 v1.22 ZIP SHA0829195396edfcda4909faf407b65ad93dd7ab7341d5889f528142f0f5834729; 원본712/중지5 보존.
- 변경: catalog-profiles/SYS-RUNHOURS.json, catalog-sources/SYS-RUNHOURS-DOTS-DRAFT.md, catalog-guides/SYS-RUNHOURS.html, 선택 native HTML anchor/도면 이미지와 공통 정적 자료.

## 7영역 적용표

| 영역 | 상태 | 작성 위치 · all-in-one 기준 | 경계 |
|---|---|---|---|
| 설비·자료 기준 | 원문/누락 명시 | catalog-guides/SYS-RUNHOURS.html#overview | 고유·관련 소유와 미확정 구분 |
| I/O·HMI | 원문/누락 명시 | catalog-guides/SYS-RUNHOURS.html#io | 고유·관련 소유와 미확정 구분 |
| 제어 구조 | 원문/누락 명시 | catalog-guides/SYS-RUNHOURS.html#control | 고유·관련 소유와 미확정 구분 |
| 전기 전달 경로 | 원문/누락 명시 | catalog-guides/SYS-RUNHOURS.html#circuits | 고유·관련 소유와 미확정 구분 |
| 알람·복구 | 원문/누락 명시 | catalog-guides/SYS-RUNHOURS.html#alarms | 고유·관련 소유와 미확정 구분 |
| 증상별 수리 | 원문/누락 명시 | catalog-guides/SYS-RUNHOURS.html#repair | 고유·관련 소유와 미확정 구분 |
| 완료 기준 | 원문/누락 명시 | catalog-guides/SYS-RUNHOURS.html#completion | 고유·관련 소유와 미확정 구분 |

## 핵심 근거

검토 초안 SHA aa3a248f04d888378aef3bb484ad58dbec7596a79e17c73143e60470ad0025ea. UI/PDF 확인 당시 자료 묶음 SHA 7c162da140f348c1f3d05bf362278bb8a01100363c684c030642a9893002d223. 최종 ACTIVE 감사 해시 갱신은 공통 보존 기록에서 비교합니다. 원본 위치55참조, 관찰7항목/증상2항목, 도면0참조/경로0입니다. 해당 고유 원문과 관련 소유 범위로 검토했고 다른 설비의 주소를 배정하지 않았습니다.

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

- 외부 기록·갱신 사용 주체와 절차, 성공적인 저장 완료 응답 및 Flag_Aggiorna_DB 해제는 미확인입니다.
- HOUR의 Move 1 토큰 의미와 누적 시간은 구분합니다. MIN의 0 Reset이나 다른 모터 HOUR Reset만으로 전체 수명 이력 삭제를 증명하지 않습니다.
- Time work motor의 현재 호출, 실제 타이머 주기, Retain·전원 복귀, 오버플로와 현재 피드백의 실제 상태는 미확인입니다.
- 782개 태그의 원본 CSV 검색에서 HMI 운전시간 쓰기 위치나 정비 Reset 태그를 확인하지 못했습니다. AbilitaMaintenance 모드는 별도입니다.
- 모터별 피드백 대응은 해당 원본 분기로 확인해야 합니다. BC01 예시를 모든 모터에 배정하지 않습니다.

명령/종료코드·Netlify/Release/freshclone/ZIP/CSP·정리는 공통 REMAINING81-VERIFICATION.md를 확인합니다. 다음 작업은 새 증거에 따른 현재 프로젝트/TIA·실물·현장 대조이며 시뮬레이터 개발/실행은 영구중지입니다.
