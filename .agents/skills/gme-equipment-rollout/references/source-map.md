# 현재 원본과 실행 경계

경로는 Git 루트 기준. 아래 위치는 v1.3.0 조사 기준이므로 수정 전에 실제 내용을 확인한다.

| 확인할 내용 | 원본/구현 |
|---|---|
| 실제 설비/우선 목록 | all-in-one/registers/equipment.json, priority-equipment.csv |
| 작성 수준/범위 | registers/requirements-audit.json, registers/all-in-one-data.json의 equipment_status_notes/excluded_priority |
| BC01 기준 | registers/all-in-one-data.json의 bc01_standard |
| 원본 선언·핀 | all-in-one/sources/decoded-original/*.xml, networks/network-*.html |
| 파생 제어/알람 | registers/control-spec.json, alarm-recovery.json, program-model.json |
| 유형별 근거 | registers/burner-interface.json, sensor-measurement.json, process-measurement.json, encoder-position.json, regulation-manual.json |
| 수리/기록 | build-repair-records.py, assets/repair-records.js, assets/bc01-tools.js |
| 화면/검색/URL | assets/all-in-one.js, build-all-in-one.py |
| 기존 검사 | verify-all-in-one.py, verify-bc01-tools.cjs, verify-package.py, build-package.py |
| 원본/패키지 보존 | scripts/verify-all-in-one.mjs, scripts/package-inventory.mjs |
| 기록 호환 기준 | all-in-one/BC01-PRESERVATION-20261011.md, BC01-RECORD-TOOLS-20261011.md |

표에서 registers/·assets/·build-·verify-로 시작한 경로는 all-in-one/ 아래다.

## 우선 분리해야 하는 BC01 고정 부분

- build-all-in-one.py: BC01/P01 표준, facility=3, 관계/매체/ABB 대응, 근거 묶음.
- all-in-one.js: P01 표준 화면·검색·URL 선택·저장 버전·복원 대상.
- bc01-tools.js: P01 복원·비교·보고서·근거·도면 비교.
- build-repair-records.py: BC01만 선택 관찰8행 추가.
- verify-all-in-one.py/verify-package.py/verify-bc01-tools.cjs: BC01 수량/원본 위치 단언.

고정 부분은 설비별 데이터와 공통 기능을 분리하되 기존 BC01 검사도 유지한다. v1.3.0에서 타 설비에 네 도구가 이미 지원된다고 가정하지 않는다.

## 실행 전에 반드시 확인

v1.3.0의 build-control-spec.py는 build-program-model.py를 runpy로 자동 호출했다. PREP-01(v1.4.0)에서 전체 자동 연쇄를 제거했다. 현재는 독립 정적 생성기이며 실행 전에 변경된 호출 경로가 없는지 확인한다. build-all-in-one.py는 데이터뿐 아니라 네트워크 HTML의 앵커/스타일도 쓴다. build-package.py는 필수14정적 검사와 패키지/검증 기록을 생성한다. 파일명에 verify가 있어도 출력 파일이 생길 수 있으므로 실행 본문을 확인한다.

## BC01에만 적용하는 회귀 사례

1843:102의 선행 out/ENO, 1843:828 전체 NOT, 1935:198의 FC 분기에만 있는 UNDER TESTING 반전, 1935:202의 OR 허가3개, FAULT/INV의 Tag_51 공유, FC의 직접 Start/타이머 접점 부재를 유지한다. 이는 BC01 검토 결과이며 다른 설비에 복제할 공통 논리가 아니다.

원본 위치56과 참고 LAD1018을 포함한 검사57, 직접 근거 해시32는 기준 개수다. 새 근거가 정당하게 추가되면 근거·변경 이유·기존 보존 대조를 함께 기록한다.
