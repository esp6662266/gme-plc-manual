# GME 작업 재개 지침

작업 전 VERSION.json, WORKSPACE-HANDOFF.md, PUBLICATION_STATUS.md와 all-in-one/ACTIVE-WORK.md의 최상단 최신 항목을 읽고 pwd/Git 상태를 확인한다. 현재 수정 원본은 all-in-one/이며 dist/와 옛 ZIP/snapshot은 작업 원본으로 사용하지 않는다. 과거 OTHER_PC_HANDOFF.md·시뮬레이션 계획보다 최신 지침을 우선한다.

2026-10-12 사용자가 CC01·TC11·CM01·CM02·UC01의 철거/검토불필요를 확인했다. SCOPE-OVERRIDES.json/preflight의 최신 검토범위를 따르고 해당5개의 추가자료·실물·TIA/CPU·복구 검토를 다시 요청하지 않는다. 원본·기존문서·기록·게시이력은 보존한다.

2026-10-12 사용자 지시로 2번 도면상충 확인(LS34/35↔LS40/41·PV01 A/B·ZT05/06·SS11케이블·LD01A정격)은 당분간 보류한다. 재개 지시 전 반복 조사/자료 요청을 하지 않고 원본·미확정 근거를 보존한다. 이 보류는 철거 제외나 해결 완료가 아니다.

최신 확장 계획은 EXPANSION-WORK.md와 docs/equipment-standard/WORK-STANDARD.md, 저장소 스킬 .agents/skills/gme-equipment-rollout/SKILL.md를 먼저 읽는다. 사용자는 실제 대장 중복 정리·기존 제외 유지로 BC01 기준의 설비 확대를 승인했다. v1.3.0의 BC01 단독 문구는 당시 구현 이력이다. 후속 작업은 PREP-01 공통화·BC01 회귀 → FN04 시범 → 1차 → 2차 후보 순서이며 기존 완료분은 보존한다. 시뮬레이터는 영구 중지: 작성·수정·생성·실행·행동 시험을 하지 않는다. build-program-model.py, verify-virtual-plc.cjs 등을 실행하지 않는다. PREP-01에서 build-control-spec.py의 자동 생성 연쇄를 제거했다. 현재는 독립 정적 생성기이며 실행 전 호출 경로를 재확인한다. 금지 생성기/중지 자산은 계속 실행하지 않는다. 중지5자산과 원본을 해시로 보존한다. 실제 PLC/현장/보호값과 SEJIN 프로그램·운영 자료·사진/이력 복제/통합을 변경하지 않는다.

원본·완료분·미확정 조건과 note/repair_observation 미지 필드·초안·저장 키를 보존한다. static 문서/브라우저 저장 결과와 TIA 컴파일/현재 CPU/실물/현장 복구를 구분한다. 실물·현행 ABB 모델/단자·정상 극성·복구 완료를 추정해 채우지 않는다. 변경 전 백업과 diff를 확인하고 dirty 파일을 강제 reset하지 않는다.

필요한 생성기만 실행한다. 신규 BC01 검사와 필수14검사·원본/중지 해시·ZIP CRC/전체해시를 통과시킨 뒤 npm test/build 및 Netlify CSP 일치를 확인한다. 변경 사항·검증·미확정 범위는 MD와 검증 기록에 갱신한다. GitHub push 뒤 실제 Netlify commit_ref/ready와 게시 파일/UI를 확인해야 게시 완료로 표시한다. 읽기 전용 조사/리뷰는 최대2개로 병행하고 공통 파일·검증 기록은 부모가 순차 통합한다.

작업 완료 때 의미 있는 변경을 버전 이력에 남긴다. VERSION.json(루트/올인원), package.json/package-lock.json, 생성기 표시 버전과 manifest를 일치시키고 RELEASES.md/PUBLICATION_STATUS.md/ACTIVE-WORK.md를 실제 검증 결과로 갱신한다. 최신 작업 main과 고정 배포 tag/Release를 구분한다. 이전 버전 tag나 사용자 자료를 덮어쓰지 않는다. 다른 컴퓨터에서 git fetch/pull과 현재 버전 검사만으로 같은 소스에 도달하도록 필요한 소스·원본·MD·검증 파일을 함께 커밋한다.

all-in-one 밖의 작업표준·스킬만 변경할 때는 표준 버전과 링크·스킬 구조·대장 검증을 갱신한다. 프로그램 버전·기존 매뉴얼 패키지를 문서 변경만으로 재생성하지 않는다. 표준 버전은 docs/equipment-standard/VERSION.json, 실제 설비 진행은 EXPANSION-WORK.md와 work-items 기록으로 인계한다.
