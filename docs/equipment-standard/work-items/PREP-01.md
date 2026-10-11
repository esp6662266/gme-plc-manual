# 작업 기록 — PREP-01

- 표준: GME-STD-1.0.0
- 대상: BC01(P01) 회귀와 설비별 공통 구조
- 기준 커밋: 3899f0254af596aa56b6deb8f513c5c042565fbf / v1.3.0
- 실행 모델: 부모 실제 UI 선택은 미관측. 읽기 전용 조사2개는 gpt-6.1-sol / ultra로 도구 지정 확인.
- 시작: 2026-10-11 Asia/Seoul
- Git: 최신 origin/main과 일치, 시작 시 dirty 없음.
- 백업: 저장소 밖 ../gme-expansion-before-20261011. baseline.json에 원본/중지5자산 해시와 BC01 표준 구조 해시 보존.
- preflight: 전체248 / 우선23 / 대응18 / 제외90 / 부모 보류7 / 2차133 일치, source_byte_changes 없음.

## 이번 목표와 영향 범위

BC01 자료를 그대로 보존하면서 설비별 프로파일, 기능 적용, 원본 비교 연결과 안정된 기록 키를 받는 공통 계층을 추가한다. build-control-spec.py의 금지 생성기 자동 호출을 정적으로 제거한다. 중지5자산의 수정·생성·실행·행동시험은 하지 않는다.

예정 파일: all-in-one/build-control-spec.py, build-all-in-one.py, assets/equipment-standard.js, assets/bc01-tools.js, assets/all-in-one.js, 관련 정적 검사와 생성 출력, 버전/진행/게시 문서. 기존 BC01 36항목/19조건/3알람/5회로/32근거/57검사 위치와 FN04·AB01 완료 분석, 저장 키·미지필드·초안·다른 설비 기록 보존.

## 현재 상태

공통 구조와 금지 자동 호출 분리 완료. BC01 근거 데이터 동일, 원본730·중지5 해시 동일. 기존 BC01 검사19종/57위치·verify-all-in-one·공통 격리 검사 통과. 실제 PC1280에서 기존36항목과 도면 비교, 합성 JSON 미리보기→선택 저장→재읽기→목록 재열기 확인. 미지 행·필드와 0/빈칸 보존 검사 통과.

독립 GPT-6.1 Sol / Ultra 리뷰 지적: 개별/전체 export의 P01 기본 메타데이터, passed 기록 뒤 단언, 잠금 대기 중 닫힌 미리보기 저장을 수정했다. 기존 저장 키·초안 키·기록 설비 ID는 그대로 유지한다. BC01 고유 데이터/36항목/19조건/3알람/5회로/32근거를 다른 설비로 복제하지 않는다. UI 실패/동시성/모바일/PDF 전체 영향 검사와 게시는 FN04 시범을 포함한 공통 기능 릴리스 검증에서 수행하며 그 전 게시 완료로 표시하지 않는다.

| 상태 | 결과 |
|---|---|
| documentation | complete_with_gaps — 공통 구조·금지 경로 분리 |
| static_review | passed — BC01/공통 격리 검사, 보존 대조 |
| ui_records | BC0136항목·복원 저장/재읽기/재열기 통과, 전체 영향 검사 진행 |
| publication | not_published — 시범 릴리스와 함께 확인 예정 |
| tia_compile/live_cpu/field_recovery | not_performed |

## 다음 한 작업

FN04(P02) 기존 분석을 설비별 7영역·네 기능과 연결하고 전체 영향 검사/게시를 마친다.

## v1.4.0 최종 로컬 검증

문서 complete_with_gaps, 정적 검토 passed, ui_records passed. BC01144/FN04196화면·선택격리/검색·저장/복원/재열기·0/빈칸·미지필드/다른설비/초안·실패/동시탭/닫힌대기복원·PDF A4 2쪽 렌더 통과. 현재 기준과 검증 상세는 루트 V1.4.0-VERIFICATION.md/.json. 게시 확인은 진행 중이며 TIA/현재CPU/현장복구 미수행. 다음 한 작업은 v1.4.0 최종 패키지·GitHub/Netlify 게시 검증, 이후FN01(P15)이다.
