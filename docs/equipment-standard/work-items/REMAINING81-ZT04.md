# 작업 기록 — ZT04

- 표준/배치: GME-STD-1.0.0 / phase2 / REMAINING81
- 대상·이름·유형: ZT04 / P&ID 밸브 위치 계측 / sensor
- 부모·소유: MV03; ZT04 전용 물리 I/O·HMI·LAD 태그는 식별하지 못했습니다. OEM·시공 엔코더 이름과 부모 MV03의 TM/카운터 근거만으로 현재 실물 엔코더와 채널 동일성을 확정하지 않습니다.
- 시작 커밋/버전: 93fa00c447229202bbffc4096c2fe004f12a83ae / v1.22.0 → v1.23.0
- 작업자/검토: 부모 단독 통합 + 최대2개 읽기전용 원본 조사/PDF 시각검토. 조사 요청 모델 GPT-6.1 Sol/Ultra; 부모 실행 모델/추론 런타임은 미확인.
- 작업 시각: 2026-10-12 Asia/Seoul. 최종 검사·게시 시각은 공통 검증 대장 참조.
- 백업: 기준 Git + 고정 v1.22 ZIP SHA0829195396edfcda4909faf407b65ad93dd7ab7341d5889f528142f0f5834729; 원본712/중지5 보존.
- 변경: catalog-profiles/ZT04.json, catalog-sources/ZT04-CODEX-REVIEW.md, catalog-guides/ZT04.html, 선택 native HTML anchor/도면 이미지와 공통 정적 자료.

## 7영역 적용표

| 영역 | 상태 | 작성 위치 · all-in-one 기준 | 경계 |
|---|---|---|---|
| 설비·자료 기준 | 원문/누락 명시 | catalog-guides/ZT04.html#overview | 고유·관련 소유와 미확정 구분 |
| I/O·HMI | 원문/누락 명시 | catalog-guides/ZT04.html#io | 고유·관련 소유와 미확정 구분 |
| 제어 구조 | 원문/누락 명시 | catalog-guides/ZT04.html#control | 고유·관련 소유와 미확정 구분 |
| 전기 전달 경로 | 원문/누락 명시 | catalog-guides/ZT04.html#circuits | 고유·관련 소유와 미확정 구분 |
| 알람·복구 | 원문/누락 명시 | catalog-guides/ZT04.html#alarms | 고유·관련 소유와 미확정 구분 |
| 증상별 수리 | 원문/누락 명시 | catalog-guides/ZT04.html#repair | 고유·관련 소유와 미확정 구분 |
| 완료 기준 | 원문/누락 명시 | catalog-guides/ZT04.html#completion | 고유·관련 소유와 미확정 구분 |

## 핵심 근거

검토 초안 SHA 53475fe4ceace2d87ef411e77783f0d052607dc43fd6a685bd6392db0a303639. UI/PDF 확인 당시 자료 묶음 SHA 7ed70f3cfd0d0a030bd217c9f22706309893b829d012a862ede11fb5c108f51c. 최종 ACTIVE 감사 해시 갱신은 공통 보존 기록에서 비교합니다. 원본 위치0참조, 관찰4항목/증상3항목, 도면8참조/경로0입니다. 해당 고유 원문과 관련 소유 범위로 검토했고 다른 설비의 주소를 배정하지 않았습니다.

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

- ZT04 전용 I/O·HMI·직접 제어 미확보 범위를 유지합니다. 명판·태그·배선·연결 사진 없이 새 대응 주소를 넣지 않습니다.
- 현재 엔코더 모델·전원·신호 방식·TM/카운터 채널·Zero/Max 교정 절차와 실제 밸브 위치의 대응 증거가 필요합니다.
- ZT04 전용 물리 I/O·HMI·LAD 태그는 식별하지 못했습니다. OEM·시공 엔코더 이름과 부모 MV03의 TM/카운터 근거만으로 현재 실물 엔코더와 채널 동일성을 확정하지 않습니다.
- 이번 범위는 원본 정적 문서 검토입니다. TIA에서 현재 프로젝트·호출·복수 쓰기·컴파일을 확인하는 작업, 현재 CPU 비교, 실제 현장 시험·복구는 미수행·미확정입니다.
- 시뮬레이터는 영구 중지입니다. 이전 대장의 오프라인 실행·시험 설계 문구를 시뮬레이터 생성·실행 재개 지시로 사용하지 않습니다. 실제 PLC·현장·보호값 변경은 수행하지 않았습니다.

명령/종료코드·Netlify/Release/freshclone/ZIP/CSP·정리는 공통 REMAINING81-VERIFICATION.md를 확인합니다. 다음 작업은 새 증거에 따른 현재 프로젝트/TIA·실물·현장 대조이며 시뮬레이터 개발/실행은 영구중지입니다.
