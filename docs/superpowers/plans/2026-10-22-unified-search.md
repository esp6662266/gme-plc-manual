# GME Unified Drawing Search Implementation Plan

> **Execution:** Follow the project instructions and existing user authorization. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 사진에 보이는 부품 태그와 선번을 입력하여 쓰임새·원본 페이지를 찾는다.

**Architecture:** 기존 PLC/HMI 검색에 원본3PDF 전체 페이지, 공개 HTML 매뉴얼 본문, 원본 시각대조6행을 추가한다. 추출 본문과 기능 해설을 구분하고 텍스트층에서 빠지는 번호는 검증된 전사로 보강한다. 압축된 재현용 문서 색인을 보관하고 통합색인은 화면 진입 시 지연 로딩한다.

**Tech Stack:** Existing JavaScript UI/Node build; Python HTMLParser and pypdf for offline extraction.

**Spec:** 사용자 사진의14KA6·14KA8·14KA10·8.9·8.10·13.6이 검색되지 않아 도면/매뉴얼 통합검색으로 확장해 달라는 후속 요청.

## Global Constraints

- 원본·중지5자산·운영기록·저장키 보존. PLC/현장/SEJIN 쓰기·시뮬레이터 실행 금지.
- 도면 대조 설명/본문 문맥/사진과 현장 대응 미확정을 구분한다.
- 기존 철거5개 제외·도면상충 보류 유지.
- localStorage·운영메모·초안 MD는 색인에서 제외한다.

## Review Focus

- 14KA6과14KA8,14KA10을 서로 바꾸지 않는다.
- 도면번호8.9/8.10을 실제이미지에서 확인하며 추출0건을 부재로 단정하지 않는다.
- 정확 태그/선번의 기능을 단순 본문언급보다 먼저 표시한다.
- 문서 본문은 검색 문맥만 표시하고 현재값·확정 기능으로 표현하지 않는다.
- 390px·URL/필터 복원·원본 PDF페이지와 문서 링크를 검증한다.

### Task 1: 보존 문서 색인과 기능 해설

**Files:** scripts/build-document-search.py, scripts/build-io-search-index.mjs, registers/document-search-data.json.gz, registers/io-search-reference-notes.json, UI/model and tests/io-search.test.mjs.

- [x] 원본 시각대조6행과 PDF/HTML 추출을 추가한다.
- [x] 통합검색 메뉴·7종 필터·문맥 snippet·정확 태그 순위를 구현한다.
- [x] 실제 태그/선번·원본 페이지·본문·필터·모바일을 검사한다.

### Task 2: v1.25.0 검증과 게시

**Files:** versions/package, generated UI/data, package manifest, RELEASES/PUBLICATION_STATUS/WORKSPACE-HANDOFF/ACTIVE-WORK, docs/io-search verification.

- [x] 필수14+2·원본/중지해시·ZIP CRC/전체해시·npm test/build·CSP를 확인한다.
- [x] 모든 수정/추가 파일을 sparse 체크아웃 설정까지 고려해 커밋한다.
- [x] 실제 Netlify commit_ref/ready·공개 검색/자산 해시를 확인해 기록한다.
