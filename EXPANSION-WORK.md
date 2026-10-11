# BATCH02 v1.17.0 실제 게시 완료 · 2026-10-11

HE01(P13) 참고 매뉴얼과 P03/P04/P14 미식별 보고서를 실제 게시했다. 기존17개를 보존한 매뉴얼18개 + 미식별 보고서3건 = 문서범위21/23(91.3%), 기존 제외2개를 뺀21개 문서범위100%. 매뉴얼만18/23(78.3%)이다. 실물 식별·본체 전용 데이터·현장 복구 완료 수가 아니다. HE01 본체 신호/알람/타이머0, 식별3건 PLC 미배정, CC01 전용자료 미확보 유지. 사용자 CC01 안내에 따라 새 근거 전 부재 검색을 반복하지 않는다.

기능 commit cf35b18a37727a21a219078e82b230e0c637f26b, GitHub Release [v1.17.0](https://github.com/esp6662266/gme-plc-manual/releases/tag/v1.17.0), ZIP2819파일/54636330B SHA256 e684ab3f8cd0cb099883b65829d3d527f3f822289d3138dd49998bff0f993a62 / asset630643320 digest 일치. Netlify 6acb7aefd0153e00080a6aff ready 2026-10-11T12:03:13.821Z, 정확 commit_ref 확인. 원격 새clone npm8/BC01/설비18/NETLIFY build/Git변경0. 게시155파일(127해시일치+28HTML URL정규화동등), 실제 HE01/원본13쌍 이미지·PDF·강조/미식별3보고서7영역·미배정/복귀 확인. 공개 기록/초안 null, warn/error0, 운영기록 쓰기0.

로컬 HE01 136화면·26원본쌍·저장/편집/복원/PDF2쪽, 식별3건6화면·저장재열기3건/PDF6쪽과 최종필수14+설비2/npm8/정적build/CSP6해시39정책·ZIP CRC/전체해시 통과. 원본730/추가3·원본sources712·중지5·기존17매뉴얼/23양식 보존. 설비별 저장/PDF 당시 근거 묶음은 그대로 보존하고 최종 HE01 묶음2e798c6b1d4a1ff816e0de8483fd427e63bc8c24aad508c5629e799d5a1db4c6을 별도로 기록했다.

승인된 우선 설비 문서/검증/게시 범위를 complete_with_gaps로 마무리했다. 2차133 후보 로컬 반영0이며 Dots 자체 추가 조사132와 구분한다. TIA 컴파일·현재 CPU·실물 동일성·현장 복구는 미확정/미수행. 시뮬레이터 영구중지·PLC/현장/보호값/SEJIN 변경0. AON 및 고정 ZIP 내부 문서는 생성시점 로컬검증·게시대기 기록을 보존하며, 최신 실제 게시 상태는 이 루트 기록이다. 다른 PC는 최신 main fetch/pull로 소스·원본·초안·검증기록을 받으며 고정 v1.17.0 기능 릴리스와 최신 게시기록 main을 구분한다.

# BATCH02 v1.17.0 — HE01·미확정 식별3 로컬 검증 완료 / 공통 패키지·게시 대기

HE01(P13) 7영역34항목·13참고 원본쌍·1090위치/84해시, 선택 핵심 XML/원본 PDF10쪽 독립 대조 및 화면136/원본쌍26/격리 저장·복원·실제 JSON55030B/비교3/A4 PDF2 passed. 본체 전용 신호/알람/타이머·기록 신호0 유지, TC03/PSH01/PSH03·댐퍼·팬·RD01/BR01 주변 소유를 구분한다. 기존17프로파일/양식/원본712·대장89/중지5·저장키/초안/미지필드 보존. 기록/PDF의 당시 source_bundle은 보존하고 최종 audit/hash는 묶음 검증에 별도 기록한다.

P03/P04/P14 각각7영역 식별 보고서 complete_with_gaps. 고정 초안60/36·외부 첨부3 SHA 대조;12선택 XML·원본 PDF19쪽+변경 없는2쪽 재사용의 독립 검토. 1280/390 6화면·실제 P03 식별 작업지→보고서 연결·기존 관찰양식3개 저장/재열기·각 A4 2쪽/총6쪽 확인. PLC/catalog ID·신호/알람/타이머 배정0·실물 동일성 미확정. 전용 설비 표준 프로파일/4도구 구현으로 세지 않는다. 이전 unresolved JSON과 전체 양식은 보존, HTML 보고서 링크만 추가한다. 재생성은 build-unresolved-identity.py 다음 build-identification-reports.py로 링크를 복원한다. 두 생성기는 시뮬레이터/PLC 실행을 하지 않는다.

문서/프로그램18매뉴얼+식별3보고서가 로컬 검증되었고, 실제 게시 완료는 아직 BATCH01의17매뉴얼이다. 최종 필수14+2·npm8·NETLIFY build·ZIP·GitHub·실제 Netlify를 이번 묶음1회 확인한다. CC01 전용자료 미확보/새자료 전 반복 부재 검색 없음. 2차133 로컬 제외·Dots 연구분모를 편입하지 않음. 운영기록/시뮬레이터/PLC/현장/보호값/SEJIN 변경0·TIA/현재 CPU/현장복구 미수행. 상세 BATCH02-HE01-VERIFICATION.json 및 BATCH02-IDENTIFICATION-VERIFICATION.json.

# BATCH02 v1.17.0 — HE01 및 미확정 식별 조사 진행

실제 게시 완료는 BATCH01까지 17/23개이며 이번 묶음은 아직 게시하지 않았다. v1.16.0 all-in-one 2808파일 전체 백업·SHA 대조를 마쳤다. HE01 본체 자료 미확보와 주변 TC03/PSH01/PSH03·댐퍼·팬·공정 알람 소유를 구분해 원본 선택 핀 및 PDF10쪽을 독립 확인하고 표준 작업실에 연결했다. P03/P04/P14는 PLC 태그를 배정하지 않는 식별 보고서다. P03 전체60/P04 전체36 고정 Git SHA 및 P14 외부 입력3개 원본 첨부를 수신·대조했다. 전체 해시 수는 전체 논리 의미검토 수가 아니다.

기존17·원본·기록키·초안·미지필드·중지5 보존. HE01 UI/기록/PDF와 식별 보고서 독립 확인 후 공통 검증·ZIP·GitHub·Netlify 실제 게시를 묶음1회 수행한다. CC01 자료 미확보 유지·새 자료 전 반복 검색 없음. 2차133 로컬 제외. 시뮬레이터 영구 중지·실제 PLC/현장/보호값/SEJIN 변경0·TIA/현재 CPU/현장복구 미수행.

# BATCH01 v1.16.0 실제 게시 완료 — 2026-10-11

MV06/RD01/BR01/CC01/AB01 문서·정적·UI기록·PDF·최종14+2·npm8·NETLIFY build 검증완료. GitHub ZIP2808파일/54519136B/SHA25680cac514006d4ae67301a5dd456e844f2ecbccbe9fe89320d3f754aba8987473·asset630533977일치. Netlify6acb6e546a59be00083a0b94 ready 2026-10-11T11:09:29.045Z / feature aab32a48f8cfcd5523a0fc43047e7be5627bfa1a. 새clone8/BC01/설비17/NETLIFY build/Git변경0·게시348파일(260exact+88HTML동등)·실제5설비/원본5쌍강조·운영기록/초안null·warnerror0. 원본730/추가3/중지5/기존완료·저장키보존. CC01 전용데이터미확보유지·사용자안내반영·새자료전반복검색안함. AB01 본체후보/주변계측·알람·BR01소유 분리.

게시문서/프로그램 기준17/23=73.9%,기존제외2별도17/21=81.0%. 실제데이터식별·TIA/CPU/실물/현장복구 완료를뜻하지않는다. AON/고정ZIP문서는 생성시점pending기록보존; 최신실제게시상태는이루트기록이다. 설비별저장/PDF해시는당시근거로보존하고최종audit/hash는BATCH01-VERIFICATION.json에별도기록했다. 다음HE01(P13) 독립검토·통합 및P03/P04/P14식별보고서. 2차133로컬제외·전체goalactive. 시뮬레이터영구중지·PLC/현장/보호값/SEJIN/운영기록변경0.

# BATCH01 v1.16.0 — 다섯 설비 검증 완료 / 최종 공통검증·게시 대기

MV06/RD01/BR01/CC01/AB01 설비별 문서·정적·UI기록·PDF 검증 완료. CC01 전용데이터 미확보 유지·새자료전반복검색안함. AB01 본체 후보·TC01/02 기존입력2·기록신호0·주변알람7/타이머6참고·160UI/15쌍/실제JSON42445B/3→4복원/PDF2 확인. 필수14+2·npm test/NETLIFY build·패키지·GitHub·실제게시를 묶음1회 진행한다. 아직 Release/실제게시 없음·실제게시12/23 유지. 다음 HE01/P03/P04/P14·2차133 로컬 제외. [AB01 근거](BATCH01-AB01-VERIFICATION.md). 원본/중지/운영기록 보존·TIA/CPU/현장 미수행·PLC/SEJIN 변경0·전체goal active.

# BATCH01 v1.16.0 — CC01 미확보 경계 검증 완료/AB01 다음

MV06/RD01/BR01/CC01 설비별문서·정적·UI기록·PDF 검증완료. CC01 본체고유데이터와기록신호0 유지·주변참고만연결·새자료전검색반복안함. 공통빈자료/미지항목요약표시 회귀passed. AB01 독립통합→공통회귀/패키지/게시1회. 아직Release/실제게시 없음·실제게시12/23 유지. [CC01 근거](BATCH01-CC01-VERIFICATION.md). 전체goalactive·시뮬레이터/PLC/현장/보호값/SEJIN변경0.

# BATCH01 v1.16.0 설비별 검증 — BR01 완료/CC01 다음

MV06 기준점·RD01·BR01 문서/정적/UI기록/PDF 검증 완료. CC01→AB01 독립통합 후 공통 회귀/패키지/게시1회. v1.16.0 작성중·아직Release/실제게시 없음·실제게시12/23 유지. 원본/기존14/중지5/운영기록 보존·시뮬레이터/PLC/현장/보호값/SEJIN변경0. [BR01 근거](BATCH01-BR01-VERIFICATION.md). 전체goal active.

# BATCH01 v1.16.0 설비별 검증 진행 — RD01 완료/BR01 다음

MV06 검증기준점보존·RD01 문서/정적/224UI/8쌍/실제저장·복원/JSON/PDF3 passed. BR01→CC01→AB01 독립통합후묶음1회패키지/실제게시. v1.16.0 작성중·아직게시/태그/Release없음·실제게시12/23 유지. HE01/미확정식별3다음·2차133로컬제외. 원본/기존13/중지5/운영기록보존·시뮬레이터/PLC/현장/보호값/SEJIN변경0. [RD01 근거](BATCH01-RD01-VERIFICATION.md). 전체goal active.

# 5개 통합 묶음 BATCH01 — 로컬 기준점 보존 · 2026-10-11

묶음은 MV06(P21) → RD01(P06) → BR01(P11) → CC01(P10) → AB01(P12)이다. 설비별 원본·선언·핀·도면·소유 검토와 합성 기록의 저장/재열기 검증은 유지하고, 마지막 공통 회귀·패키지·GitHub·Netlify 실제 게시는 한 번 수행한다. 이후 묶음 크기는 이번 실제 게시 결과로 판단한다. HE01 및 P03/P04/P14는 다음 묶음이며 2차133 로컬 통합·게시는 제외한다.

MV06 v1.15.0은 문서/정적/2472 화면·10원본쌍/격리 기록·복원·충돌·Quota·A4 PDF3쪽 검증을 마친 로컬 기준점이다. 필수14+설비2 검증09:19:10.740539Z, 2801파일 ZIP53581069B SHA256 ab3ba89e8877ca72e76ee971214d779555d6fcb636cbe1212405e497b7372dde, CRC/전체해시/원본730/추가3/중지5 보존·NETLIFY build2830/CSP6/39 passed. 이 버전은 단독 게시하지 않는다. 실제 게시 완료는 여전히 MV03까지12/23=52.2%, 제외2개 별도12/21=57.1%다.

착수 전 전체 all-in-one 2801파일을 ../gme-phase1-before-20261011-v1.15.0에 백업하고 전체 SHA256을 대조했다. 공개 사이트의 실제 저장키 gme-all-in-one-notes-v1 / gme-all-in-one-drafts-v1은 읽기 전용으로 확인했으며 둘 다 null이다. 증거는 /tmp/gme-batch01-qa에 보존하며 운영 기록 변경은0이다.

Dots CC01/AB01/HE01 실제 첨부 본문을 수신·보존했다. 고정abcf31c/v1.12 기준 CC01 핵심34+검색XML695=729해시, AB01 83, HE01 79 전부 Git blob 일치. 현재 CC01 VERSION.json, HE01 all-in-one-data.json만 진행 버전의 기대 차이다. sources 원본은 모두 현재 일치하며 초안 수신은 게시 완료가 아니다. Dots의 추가248 사전 초안은 로컬 대상에 자동 편입하지 않는다.

현재 요청 GPT-6.1 Sol/High를 따르며 로컬 편집·검증·게시는 이 채팅에서 수행한다. 시뮬레이터 영구 중지/TIA·현재CPU·현장복구 미수행/실제PLC·현장·보호값·SEJIN변경0. 다음은 RD01(P06)의 독립 원본 검토·통합이다. 전체 goal active.

# MV06 v1.15.0 통합·검증 진행 — 2026-10-11

MV03 v1.14.0 실제게시완료(12/23=52.2%,제외2별도12/21=57.1%). MV06(P21)7영역·10원본쌍·11직접문서규칙/4중지 원자료 규칙·반전ON/≥5·≤−5/PIW286·20/2초Shot/300ms·150ms응답/엄격±2200동일FAULT·공통인버터同Q상충·HSC2결속21미결속/HMI4FALSE10미해석·START/RESET5–9·LS40/41대34/35·중복FLO4TB2A별개구간을 연결한다. Dots83고정SHA와19XML/선언·실제PDF18쪽 독립대조. 730원본/추가3/기존12/공통기록/중지5보존. UI/기록/PDF/패키지/게시검증중. TIA/CPU/현장not_performed·시뮬레이터/PLC/SEJIN변경0. 다음RD01·BR01수신91/100고정SHA일치;2차133로컬제외.

# MV03 v1.14.0 실제 게시 완료 — 2026-10-11

MV03(P20) 문서·정적·UI기록·패키지·실제게시 검증완료. 7영역55항목/7쌍/782위치85해시·2288화면·합성저장/통합복원3→4/0→1비교/동시성·Quota/A4 PDF3·fresh14+2/ZIP2801/원본730·새clone8/BC01/설비/NETLIFY/Gitclean passed. GitHub v1.14.0 asset630259669 digest ee5e6e7457023ab1e5ab1d2326cd8d48283e85ba500eb55088199f2f2adef28c/53483224B;Netlify6acb4df93484ca00082d7fa4 ready08:51:36.214Z/featureccbb18653eec17524d31b35a5a91ad78e311c7c7. 게시126파일(104exact22HTML)·실제P20/FG38PDF39/Part390강조·통합0/운영키null/warnerror0. 12/23=52.2%,제외2별도12/21=57.1%. AON문서는불변ZIP생성시pending기록보존;최신게시상태는이루트기록이다. 다음MV06(P21)독립검토·통합. RD01/BR01초안수신91/100고정SHA전부일치·VERSION만현재기대차이. Dots CC01 조사중. TIA/liveCPU/field not_performed·시뮬레이터/PLC/현장/보호값/SEJIN변경0·2차133 로컬제외. 전체goal active.

# MV03 v1.14.0 통합·검증 진행 — 2026-10-11

MV01 v1.13.0 실제게시완료(11/23=47.8%,제외2별도). MV03(P20)7영역·7원본쌍·27직접규칙/2opaque·150초방향응답/±3400명령누적 동일FAULT·끝단NOT·상대Q차단접점없음/NC하드웨어·HSC2결속21미결속·HMI4FALSE10미해석·PSH03/PSH02·버너요청상충·M17용량상충을 연결한다. Dots84고정SHA와19고유/공통XML/선언·PDF12쪽 독립대조. 원본730/추가3/기존11프로파일/공통기록/중지5보존. UI/기록/PDF/패키지/게시검증중. TIA/CPU/현장not_performed·시뮬레이터/PLC/SEJIN변경0. 다음MV06수신83SHA고정일치.

# MV01 v1.13.0 실제 게시 완료 — 2026-10-11

MV01(P19) v1.13.0 실제게시완료. 7영역44항목/7쌍/2068화면·격리저장/통합선택복원3→4/0→1비교/동시성·Quota/보고서/A4 PDF3·14+2/ZIP2801/원본730/Node8/새clone passed. GitHub asset630177314 digest7b97a40d.../53363097B;Netlify6acb4468104cd90008fc7de8 ready08:10:47.897Z/feature192d2cbb420bddc2abafda2ed3cec608521537f2·게시111파일(93exact18HTML)·실제P19/Part143/통합0/운영키null. 시뮬레이터/PLC/현장/보호값/SEJIN변경0,TIA/liveCPU/fieldnot_performed. AON문서는불변ZIP생성시pending기록보존. 다음MV03(P20)독립검토·통합;Dots MV06초안중. 2차133은현재로컬goal제외. 전체goal active.

# MV01 v1.13.0 통합·검증 진행 — 2026-10-11

PV02 v1.12.0 실제게시완료. MV01(P19) 7영역·7원본쌍·개폐반대출력/끝단차단·150ms응답/±2000명령누적 공통FAULT·엔코더리셋·HSC4결속/19미결속·CONT_S9미결속·HMI4FALSE/10미해석·ZT02 A/B펄스대시공AI를 연결한다. Dots고정78해시·15고유/공통XML와선언·PDF9쪽 독립대조. 기존10설비/712원본·89대장/미확정/운영기록/중지5보존. UI/기록/PDF/패키지/게시검증진행중. TIA/CPU/현장not_performed·시뮬레이터/PLC/SEJIN변경0. 다음MV03(P20) 수신초안.

# v1.12.0 PV02 — 실제 게시 완료

PV02 v1.12.0 실제게시완료: feature a2c4d601cce2ac02c40a399a5e31a6a2fa5bbde4, GitHub v1.12.0 ZIP53268558bytes/2801파일/SHA8adc5ef8e2bb83c7d0e071c4c50bc8cc5b0a948b848925361fcaa32fc4000582 일치. Netlify6acb3d916af9a700081c73cb ready/동일commit/2026-10-11T07:41:31.900Z. 새clone8테스트/BC01/설비/NETLIFYbuildpassed·Git변경0. 게시61파일40exact+21HTML동등·실제P07 71항목/FG71PDF72/Part724강조/통합기록0/warnerror0. 기존9/원본730/공통기록/중지5보존. 다음MV01 독립검토·통합, Dots MV03조사. TIA/CPU/현장미수행·시뮬레이터/PLC/SEJIN변경0. 전체goal active.

# PV02 v1.12.0 통합·검증 진행 — 2026-10-11

PV01 v1.11.1 정정 실제게시완료. PV02(P07) 7영역·8원본쌍·39직접규칙·MC04 OR허가·300/800ms전이·7초알람4·raw/Inputs/MEM·KF_KT SEC Bool0·Enable 예열Reset/생산Set·RD01/팬요청소유·HMI17미결속을 연결한다. Dots65원본해시 일치 및 핵심XML/선언·PDF9쪽 독립검토. 릴레이부하접점5/9로 정정하고 수신원문보존. 기존9설비/원본/미확정/운영기록/중지5보존. UI/기록/PDF/패키지/게시검증진행중. TIA/CPU/현장not_performed·시뮬레이터/PLC/SEJIN변경0. 다음MV01(P19) Dots조사.

# v1.11.1 PV01 정정 — 실제 게시 완료

PV01 v1.11.1 정정 실제게시완료: feature182ab86fbd067bdf0de898bb666080e2c6fa1c1a, GitHub v1.11.1 ZIP53181725bytes/SHA7bfcbde47deb57774c23d6b6efa90901090a667ccc39fcc75aea58d963d052fb 일치. Netlify6acb38d91fcbcb0007b633a6 ready/동일commit/2026-10-11T07:21:26.626Z. 새clone8테스트/BC01/설비/NETLIFYbuildpassed·Git변경0. 게시33파일32exact+1HTML동등·실제P05 5/9표시/1/9없음/warnerror0. 다음PV02 독립검토·통합, Dots MV01조사. TIA/CPU/현장미수행·시뮬레이터/PLC/SEJIN변경0.

# v1.11.1 PV01 접점 번호 정정 — 게시 확인 중

FG69/PDF70의 EV01/02 부하 경로는 69KA1/2 접점5–9이다. v1.11.0의1–9 설명은 검토 오류이며 v1.11.1에서 정정한다. 도면 하단 접점표에1/5/9가 있으나 실제 그린 부하 경로는5/9다. DC 코일 A1/A2·110Vac 부하·PLC 제어식·원본·기록 기능은 동일하다. v1.11.0 태그/ZIP/저장시점 근거와 Dots 수신 원문은 보존한다.

# v1.11.0 PV01 실제 게시 완료 — 다음 PV02

7영역71항목·8쌍·UI1608·기록보존/복원/동시성/Quota/보고서/A4 PDF3·14+2/원본730/추가3/중지5/ZIP/Node8/새clone/실제게시passed. GitHub+Netlify2041fe8 ready. [검증](V1.11.0-VERIFICATION.md). 다음PV02(P07)65해시초안검토·통합; Dots MV01(P19)자체조사. 현장불확정유지·2차133현재범위제외·전체goal active.

# PV01 v1.11.0 통합·검증 진행 — 2026-10-11

VS01 v1.10.0 실제게시완료. PV01(P05)7영역71항목·8원본쌍·A4/B7초·1초전이·현장/자동/maintenance/OFF·위치기억·IW8→DB13W8·KF_KT/HMI17미결속을연결한다. 초안61해시·고유원본/선언·PDF8쪽검토. 정적/UI/기록/PDF/패키지/게시확인중. 기존8설비/원본/미확정/운영기록/중지5보존. TIA/CPU/현장not_performed.

# VS01 실제 게시 완료 — 2026-10-11

VS01(P09)v1.10.0 41항목/3쌍·1324UI·합성기록·A4 PDF3·14+2/2801파일ZIP/8테스트/새clone·GitHub/Netlify/게시45파일verified. 다음PV01(P05)초안61해시검토·통합; DotsPV02(P07)조사중. 전체목표active.

# MC04 v1.9.1 정정 게시 완료 — 2026-10-11

FG136/PDF137 Rev2 17.03.2025 설명정정·14+2/패키지/8테스트/새clone/게시27파일/실제화면verified. 원본·회로·기록·고정v1.9보존. 다음VS01(P09) 초안51해시와핵심16XML/선언·PDF9쪽검토중; Dots PV01 조사중. 전체목표active.

# MC04 실제 게시 완료 — 2026-10-11

MC04(P08)v1.9 45항목/5쌍·1160UI·합성기록·A4 PDF3·14+2/ZIP/8테스트/새clone·GitHub/Netlify/게시51파일verified. 다음VS01(P09)초안51해시수신·검토/통합; Dots PV01(P05)조사중. 전체목표active.

# FN06 실제 게시 완료 — 2026-10-11

FN06(P18) v1.8.0 7영역32항목·E24입력전달/호출경계·2회로·980항목UI/합성기록/PDF2·14+2/2801파일패키지/8테스트/새clone/실제게시verified. Dots최신43원본해시확인. 다음MC04(P08) 초안수신·핵심검토/통합, Dots는VS01(P09)자체조사. 전체1~4active.

# GME BC01 기반 확장 — 현재 작업과 인계

표준 **GME-STD-1.0.0** · 작업 프로그램 **v1.10.0 / 실제 게시 확인** · 2026-10-11

최신 사용자 승인: 목표모드로 아래1~4번을 설비 한 개씩 진행한다. 원래 Ultra 채팅의 목표는 사용자 명시 요청으로 paused이며 같은 변경의 병행 수정을 중지했다. 기존 이력과 미커밋 FN01을 새 채팅01a12939-4d71-7e12-ab65-5ee9149d00d5로 인계했고, 사용자가 지정한 GPT-6.1 Sol / High에서 남은1~4번 active 목표를 설정했다. FN01/FN02 검증·게시를 완료했고 FN03부터 계속한다. 2차133후보는 이번 목표에 포함하지 않는다.

1. FN01(P15).
2. FN02(P16) → FN03(P17) → FN06(P18) → MC04(P08) → VS01(P09).
3. PV01(P05) → PV02(P07) → MV01(P19) → MV03(P20) → MV06(P21).
4. 킬른/RD01(P06) → BR01(P11) → CC챔버/CC01(P10) → 재연소로/AB01(P12) → 열교환기/HE01(P13), 이어 P03/P04/P14 미확정 식별 조사. 후보와 실물 동일성·제어 소유를 분리한다. 현재 원본은 GitHub main의 all-in-one/이다. 이전 “표준 작성만/미착수” 기록은 gme-std-v1.0.0 태그에 보존했다.

| 작업 | 실제 상태 |
|---|---|
| PREP-01 공통 구조/금지 자동 호출 분리 | 구현·독립 검토·BC01 회귀·v1.4.0 게시 검증 완료 |
| FN04(P02) 시범 | 문서 complete_with_gaps, 정적/UI/기록/PDF passed, v1.4.0 게시 verified |
| FN01(P15) | 47항목 documentation complete_with_gaps · 정적/UI/기록/패키지·v1.5.0 실제 게시 verified |
| FN02(P16) | 42항목 documentation complete_with_gaps · 정적/UI/기록/PDF/패키지/새clone·v1.6.0 실제 게시 verified |
| FN03(P17) | 39항목·정적/UI기록/PDF/2801파일패키지/새clone·v1.7.0 실제게시 verified |
| FN06(P18) | 32항목·정적/UI기록/PDF/패키지/새clone·v1.8.0 실제게시 verified |
| MC04(P08) | 45항목·정적/UI기록/PDF/패키지/새clone·v1.9.1 개정란 정정까지 실제게시 verified |
| VS01(P09) | 41항목·정적/UI기록/PDF/패키지/새clone·v1.10.0 실제게시 verified |
| 나머지 1차 | PV01초안61해시수신·통합대기; Dots PV02조사; 이후미착수 |
| 2차 | 실제 대장133후보, 미착수 |
| TIA 컴파일/현재CPU/현장복구 | 미수행, 완료로 합산하지 않음 |

대장은 전체248 ID, 우선23행/대응18, 기존 제외90, 다른 공정2, 제외 부모 하위 보류7, 2차133후보를 유지한다. 233개를 독립 작업 목록으로 만들지 않는다. preflight는 inventory_matches=true이며 requirements-audit/all-in-one-data의 바이트 변경은 현재 범위 안내/새 프로파일을 추가한 결과다. 집계·대응·제외 관계는 동일하다.

현재 작업 기록은 docs/equipment-standard/work-items/PREP-01.md·FN04.md·FN01.md·FN02.md, FN01 검증은 V1.5.0-VERIFICATION.md/.json이다. 작성 소스 VERSION(root/all-in-one)/package/lock은1.10.0; 마지막 실제 게시는1.10.0이며 과거1.3태그/ZIP·원본을 보존한다. 마지막 실제 게시는 PUBLICATION_STATUS.md를 확인한다.

## 다음 한 작업

PV01(P05) 수신초안61해시와 고유 XML/선언/알람/밸브·도면을 검토·통합한다. Dots는PV02(P07)자체조사/MD초안담당. 유일한로컬편집자01a12963이반영/검증/게시한다.

## 보존 경계

원본730·추가3·중지5, BC01 전체 표준 구조, 기존 FN04/AB01 완료 분석·미확정, note/repair_observation 미지 행/필드·다른 설비·초안·저장 키를 보존한다. 백업은 저장소 밖 ../gme-expansion-before-20261011 및 깨끗한 v1.4 기준 ../gme-phase1-before-20261011-v1.4.0 및 FN02 시작v1.5 기준 ../gme-phase1-before-20261011-v1.5.0이다. 격리127.0.0.1:8874 합성 QA 기록은 시험 후 정리했으며 운영 기록 작성0이다. 시뮬레이터 작성·수정·생성·실행·행동시험0, 실제PLC/현장/보호값·SEJIN 변경/사진·이력 복제0이다. 현재CPU·정상극성·현행모델/단자·실제복구는 추가 자료 확인 전이다.

## 현재 편집자와 분업

01a12963-de06-7e93-bd10-71f025de4730 유일한로컬편집자·High목표1~4active. 이전두창paused. Dots자체조사/첨부초안→본창핵심원본검토/통합/검증/게시. FN03 v1.7/FN06 v1.8실제게시완료. MC04 v1.9.1실제게시완료·VS01 v1.10.0실제게시완료·PV01수신·Dots PV02조사. 새창생성/대리코드편집/시뮬레이터작업없음.
