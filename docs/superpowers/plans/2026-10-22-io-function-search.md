# GME I/O Function Search Implementation Plan

> **Execution:** Follow the project instructions and existing user authorization. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** I/O 주소·태그·기능으로 검색하여 원본 설명, 설비 참조, 도면·LAD 근거를 바로 연다.

**Architecture:** 보존된 PLC 심볼 전체 원장·HMI 설정·기존 회로/신호 추적에서 작은 검색 색인을 생성한다. 기존 GME 라우터에 전용 검색 화면을 추가하고 색인은 화면 진입 시 지연 로딩한다.

**Tech Stack:** Vanilla JavaScript, Node.js, existing Python static packager.

**Spec:** 2026-10-22 사용자 요청: GME /all-in-one/에도 방금 electrical-drawings에 구현한 I/O 기능 검색을 추가.

## Global Constraints

- 기존 원본·운영 저장키·초안·미지 필드 보존.
- 시뮬레이터 작성·수정·생성·실행·행동 시험 금지.
- PLC/현장/보호값·SEJIN 운영 자료 변경 금지.
- 철거5개 검토 제외·도면상충 보류 유지; 검색 결과는 과거 정적 참조임을 표시.

## Review Focus

- 주소 경계: I0.0/I10.0, IW2/IW20를 구분한다.
- 표기: 선택 %, 전각, 공백, DB bit 표기를 검색용으로만 정규화한다.
- 공유/미배정 심볼과 HMI 주소를 현재 장치 대응으로 확정하지 않는다.
- URL 재열기·필터·0건·로딩 실패/재시도를 검사한다.
- HTML 특수문자·모바일 줄바꿈·원본 근거 링크를 검사한다.

### Task 1: 검색 자료와 화면

**Files:** scripts/build-io-search-index.mjs, all-in-one/registers/io-search-index.json, all-in-one/assets/io-search-model.js, io-search.js, io-search.css; existing all-in-one.js and build-all-in-one.py.

**Interfaces:** 색인 records[].{id,kind,title,text,address,symbol,equipment,links,status}; GMEIOSearch.attach(host,{data}); GMEIOSearchModel.search(records,query,{equipment,kind}).

- [x] 정규화·정확 주소·미배정 전체원장·HMI·XSS에 대한 tests/io-search.test.mjs 작성 및 실행.
- [x] 원장/회로/신호/HMI 색인, 검색 모듈, 기존 메뉴/라우팅·생성기 통합.
- [x] 로컬 브라우저에서 주소·기능·필터·URL·근거 링크·390px 확인.

### Task 2: 버전·검증·게시

**Files:** VERSION.json (root/manual), package.json/lock, generated index/data/package manifest, RELEASES.md, PUBLICATION_STATUS.md, ACTIVE-WORK.md, WORKSPACE-HANDOFF.md, docs/io-search/verification.json.

- [x] v1.24.0 버전 일치와 원본/중지자산 보존 확인.
- [x] 필수14+2 패키지 검사·ZIP CRC/전체해시·npm test/build·Netlify CSP 일치 확인.
- [x] GitHub main 게시 후 실제 Netlify commit_ref/ready·공개 자산 해시·검색 UI 확인.
- [x] 식별 가능한 기존 Dots 연결로 종료 상담 시도, 미연결이면 실제 상태를 기록.
