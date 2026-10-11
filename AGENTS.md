# GME 작업 재개 지침

작업 전 VERSION.json, WORKSPACE-HANDOFF.md, PUBLICATION_STATUS.md와 all-in-one/ACTIVE-WORK.md의 최상단 최신 항목을 읽고 pwd/Git 상태를 확인한다. 현재 수정 원본은 all-in-one/이며 dist/와 옛 ZIP/snapshot은 작업 원본으로 사용하지 않는다. 과거 OTHER_PC_HANDOFF.md·시뮬레이션 계획보다 최신 지침을 우선한다.

현재 고도화 범위는 BC01(P01) 단독이다. 다른 설비 확대·기존 완료 자료 변경은 사용자 범위에 맞춰 판단한다. 시뮬레이터는 영구 중지: 작성·수정·생성·실행·행동 시험을 하지 않는다. build-program-model.py, verify-virtual-plc.cjs 등을 실행하지 않는다. 중지5자산과 원본을 해시로 보존한다. 실제 PLC/현장/보호값과 SEJIN 프로그램·운영 자료·사진/이력 복제/통합을 변경하지 않는다.

원본·완료분·미확정 조건과 note/repair_observation 미지 필드·초안·저장 키를 보존한다. static 문서/브라우저 저장 결과와 TIA 컴파일/현재 CPU/실물/현장 복구를 구분한다. 실물·현행 ABB 모델/단자·정상 극성·복구 완료를 추정해 채우지 않는다. 변경 전 백업과 diff를 확인하고 dirty 파일을 강제 reset하지 않는다.

필요한 생성기만 실행한다. 신규 BC01 검사와 필수14검사·원본/중지 해시·ZIP CRC/전체해시를 통과시킨 뒤 npm test/build 및 Netlify CSP 일치를 확인한다. 변경 사항·검증·미확정 범위는 MD와 검증 기록에 갱신한다. GitHub push 뒤 실제 Netlify commit_ref/ready와 게시 파일/UI를 확인해야 게시 완료로 표시한다. 읽기 전용 조사/리뷰는 최대2개로 병행하고 공통 파일·검증 기록은 부모가 순차 통합한다.
