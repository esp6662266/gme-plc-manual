# 작업 기록 — SYS-ALARM

- 표준/배치: GME-STD-1.0.0 / phase2 / REMAINING81
- 대상·이름·유형: SYS-ALARM / 알람·경광등·사이렌·Reset / software
- 부모·소유: 공통/외부/본체; 보존 백업의 문서·정적 참조입니다. 현재 호출·최종 Writer·HMI 이벤트·실물·정상 극성·TIA 컴파일·현장 복구는 확인 전입니다.
- 시작 커밋/버전: 93fa00c447229202bbffc4096c2fe004f12a83ae / v1.22.0 → v1.23.0
- 작업자/검토: 부모 단독 통합 + 최대2개 읽기전용 원본 조사/PDF 시각검토. 조사 요청 모델 GPT-6.1 Sol/Ultra; 부모 실행 모델/추론 런타임은 미확인.
- 작업 시각: 2026-10-12 Asia/Seoul. 최종 검사·게시 시각은 공통 검증 대장 참조.
- 백업: 기준 Git + 고정 v1.22 ZIP SHA0829195396edfcda4909faf407b65ad93dd7ab7341d5889f528142f0f5834729; 원본712/중지5 보존.
- 변경: catalog-profiles/SYS-ALARM.json, catalog-sources/SYS-ALARM-DOTS-DRAFT.md, catalog-guides/SYS-ALARM.html, 선택 native HTML anchor/도면 이미지와 공통 정적 자료.

## 7영역 적용표

| 영역 | 상태 | 작성 위치 · all-in-one 기준 | 경계 |
|---|---|---|---|
| 설비·자료 기준 | 원문/누락 명시 | catalog-guides/SYS-ALARM.html#overview | 고유·관련 소유와 미확정 구분 |
| I/O·HMI | 원문/누락 명시 | catalog-guides/SYS-ALARM.html#io | 고유·관련 소유와 미확정 구분 |
| 제어 구조 | 원문/누락 명시 | catalog-guides/SYS-ALARM.html#control | 고유·관련 소유와 미확정 구분 |
| 전기 전달 경로 | 원문/누락 명시 | catalog-guides/SYS-ALARM.html#circuits | 고유·관련 소유와 미확정 구분 |
| 알람·복구 | 원문/누락 명시 | catalog-guides/SYS-ALARM.html#alarms | 고유·관련 소유와 미확정 구분 |
| 증상별 수리 | 원문/누락 명시 | catalog-guides/SYS-ALARM.html#repair | 고유·관련 소유와 미확정 구분 |
| 완료 기준 | 원문/누락 명시 | catalog-guides/SYS-ALARM.html#completion | 고유·관련 소유와 미확정 구분 |

## 핵심 근거

검토 초안 SHA 601bb47c72bb87274b6278739fd094d11a0946e1f95cbefbf2b7c24b11f1035f. UI/PDF 확인 당시 자료 묶음 SHA c61ce172c7d436e8988c80f2ffb47a78f4a108b5ad02ae29bcce50522cb094ac. 최종 ACTIVE 감사 해시 갱신은 공통 보존 기록에서 비교합니다. 원본 위치67참조, 관찰10항목/증상2항목, 도면1참조/경로1입니다. 해당 고유 원문과 관련 소유 범위로 검토했고 다른 설비의 주소를 배정하지 않았습니다.

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

- 927/928의 절대 DB3 워드 참조는 원본 0565 GlobalAccess + 0564 부모 TOD3으로 확인했습니다. AOS가 비어 있어 검색 색인의 이름은 UNRESOLVED로 남아 있습니다. 부모의 판단 없이 기존 색인 표기를 바꾸지 않으며, 현재 HMI 알람 대응은 미확인입니다.
- 원본 HMI ResetAlarms DB2,X13.4는 같은 백업 배치의 참고입니다. 실제 화면의 누름·해제·알람 확인 이벤트는 확보하지 못했습니다.
- 현재 Allarm manager와 설비별 Set/Reset의 실행 순서, 외부 쓰기, Retain 및 현재 타이머 동작은 미확인입니다.
- OEM의 lampalarm2 심볼과 PLC의 Siren 이름을 대조해야 합니다. 현재 실물·접점·케이블은 미확인입니다.
- 알람 확인은 원인 제거나 검증된 재기동 완료를 뜻하지 않습니다.

명령/종료코드·Netlify/Release/freshclone/ZIP/CSP·정리는 공통 REMAINING81-VERIFICATION.md를 확인합니다. 다음 작업은 새 증거에 따른 현재 프로젝트/TIA·실물·현장 대조이며 시뮬레이터 개발/실행은 영구중지입니다.

최종: v1.23.0 실제게시·공개UI·freshclone·합성테스트파일 정리 완료. 자료 공백·TIA·현재CPU·실물·현장 복구는 계속 미확정입니다.
