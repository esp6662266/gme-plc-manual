# MV05 FG123 개정란 정정 보강 — 원초안 보존

2026-10-11 UTC. LS15 고유 회로 조사 중 원본 PDF를 직접 렌더하여 확인한 좁힌 정정이다.

## 기존 문장과 정정

- 기존 `drafts/MV05-DOTS-DRAFT.md` §4.3: “FG35/PDF36,FG123/PDF124,FG39/PDF40,FG146/PDF147,FG147/PDF148의 개정란은 각 렌더에서 공란이다.”
- 이 중 **Electrical_Rev2.pdf 실제 PDF124 / FG123 하단 개정란은 Rev. 2, 17.03.2025**이다. “FG123 개정란 공란”을 이 값으로 정정해야 한다.
- 본 보강은 FG123 한 페이지만 독립 재검토했다. 위 문장의 다른 페이지 개정란까지 이 결과로 바꾸지 않는다.
- 해당 페이지에는 E7.1 / LS-15 / CPU515 / MOD9 / 단자32와 35/5 상호참조가 표시된다. FG35/PDF36의 LS15 11–12→X1/73→E7.1과 연결되는 페이지다.

## 원본·렌더 근거

- 고정 원본: `source-mv06/all-in-one/sources/Electrical_Rev2.pdf`
- 고정 Git commit: `abcf31c5030bc7ef8749ed8e869a857f2387a28a`
- SHA256: `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`
- Git blob: `f610fd7c7ce14ae951b00cff57b969259bfb389d`
- 고정 Git blob 바이트 동일: `True`
- 전체 페이지 직접 렌더: `extracts/LS15/Electrical_Rev2.pdf-p124.png`
- 개정란 확대 직접 렌더: `extracts/LS15/FG123-revision-detail.png`
- 텍스트 보조: `extracts/LS15/Electrical_Rev2.pdf-p124.txt`

## 영향·경계

문서의 페이지별 개정 표시 정정만이다. 원본 PDF, MV05 원초안, PLC 논리·주소·핀·타이머·보호값·운영/배포/현장 상태는 변경하지 않았다. 도면 Rev2 확인은 현재 CPU·실물·정상극성·현장복구의 증명이 아니다. 시뮬레이터 작성·수정·생성·실행·행동시험 없음.
