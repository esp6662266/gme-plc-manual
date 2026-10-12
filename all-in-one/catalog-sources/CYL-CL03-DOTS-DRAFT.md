# CYL-CL03 고유원본 조사 초안

- 대상: CYL-CL03 공압 실린더, PV01 하위 구성품. phase2 / parent_child_separate. CLIENT-CL03 외부 연동 채널과 별개다.
- 기준: GME-STD-1.0.0, source-mv06 고정 abcf31c5030bc7ef8749ed8e869a857f2387a28a, 저장소 VERSION 1.12.0. 조사일 2026-10-11 UTC.
- 산출 범위: 이 MD와 extracts/CYL-CL03만 작성. 원본·공통코드·대장·버전·배포·운영·PLC·현장·보호값·SEJIN 변경 없음. 생성기·앱빌드·시뮬레이터 생성/수정/실행·행동시험 없음.
- 상태: 문서 complete_with_gaps, 정적 원본 검토 완료(한정 범위). 통합/UI/게시/TIA/현재CPU/실물/현장복구 미검증. 현재 모델·추론 실행 설정은 미확인.

## 1. 설비·자료 기준

### 1.1 고유 식별과 직접 원본

[E01] INVENTORY.json catalog[203]은 CYL-CL03→PV01, component, depth1, phase2, existing_detail=baseline, bc01_standard_acceptance=not_assessed다. equipment.json[198]도 parent PV01, pid=true, aliases=[], fgs=[]로 분류한다. fgs=[]는 해당 실린더 전용 FG가 대장에 없다는 뜻이지 주변 EV/리미트 회로가 없다는 뜻이 아니다. 중복 검토와 배치 범위는 부모·하위 별도, physical_identity_verified=false를 유지한다.

[E02] PID_1684n002I.pdf 실제 PDF1의 PV-01 Detail을 전체 및 확대 렌더로 확인했다. COMPRESSED AIR 공통 공급은 EV-02 밸브 기호로 들어가고, 그 밸브 쪽 두 선이 CL-03·CL-04 두 실린더 기호로 나뉘어 연결된다. CL-03과 CL-04의 선 연결을 별도로 확인했으므로 단순 이름 검색만의 결론이 아니다. CL-03의 몸체/로드 쪽에 LS-06/LS-05 리더선이 각각 닿는다. 이것은 도면상의 센서 위치 지시이며 현재 설치·정상 극성·CL04의 실제 행정까지 보장하지 않는다.

P&ID 표제는 UBC AND SCRAPS DECOATER 10 Ton/h, Drawing 1684n002, Apex I, 기본 날짜 06/04/2011, 최종 개정 I 15/01/2013이다. I행 설명은 REMOVED MC-05, CHANGED POWER OF FN-02로 판독했다. 파일명만으로 최신 도면이나 현장 준공도를 선언하지 않는다. 별도의 기계 GATE A/B 형상 그림에는 CL03 태그를 직접 붙여 대응시킨 연결선이 없으므로 실물의 상/하·좌/우 게이트 위치는 미확정이다.

[E03] equipment.json[61]의 CLIENT-CL03은 Impact vibration feeder, 외부 연동, aliases motor_client_03/client motor 3/cl03 등이다. 이는 CYL-CL03의 별칭이 아니다. CLIENT용 FG86~95·모터·전류·보호설정을 본 실린더에 적용하지 않는다.

### 1.2 공유자료 재사용과 경계

PV01-DOTS-DRAFT.md를 공통 탐색색인으로 재사용하되 부모 전체 제어를 반복조사하거나 부모 완료를 상속하지 않았다. 특히 구초안의 릴레이 1/9는 채택하지 않는다. 고정 저장소 WORKSPACE-HANDOFF.md의 v1.11.1 정정과 이번 FG69 실제 렌더 모두 EV 부하 접점 5–9를 지지한다. 71KA 부하도 배치 정정 5–9를 유지하되 CYL-CL03의 회로는 69KA2이며 71KA를 조사대상 소유로 옮기지 않았다.

## 2. I/O·HMI

적용: 부모 EV02/B 게이트를 경유하는 신호. 미확보: CYL-CL03 전용 PLC 출력·HMI 명령·독립 완료 신호. 아래 주소는 백업 주소이며 현행 CPU 확인이 아니다. XML 축약번호는 all-in-one/sources/decoded-original 아래 동일 번호 파일이다.

| 구분/소유 | 선언 근거 | 주소·형식/읽기쓰기 | 도면 또는 해석 경계 |
|---|---|---|---|
| PV01 B EV 출력 | 0607 RID49, NID4 UID390 AK Write, SAD Output AO43 | Q5.3 Bool, 0279 Coil377 | CL03와 CL04를 구동하는 EV02 제어, 실린더별 출력 아님 |
| EV02 열림 raw | 0607 RID129, NID12 UID40, Input AO72 | I9.0 Bool read | FG70 LS05 / FG125 E9.0 |
| EV02 닫힘 raw | 0607 RID131, NID12 UID42/48, Input AO73 | I9.1 Bool read | FG70 LS06 / FG125 E9.1 |
| B 현장요청 | 0607 RID45, NID3 UID351, Input AO75 | I9.3 Bool read | 부모 현장 selector, CL03 HMI 버튼 아님 |
| B 현장 00 요청 | 0607 RID46, NID4 UID386, Memory AO161 | M20.1 Bool read | 0279 OR 입력 |
| B 자동 01 요청 | 0607 RID21, NID4 UID387, Memory AO169 | M21.1 Bool read | 0279 OR 입력, 부모 순서 소유 |
| maintenance PV01 | 0607 RID47, NID4 UID388, Memory AO645 | M80.5 Bool read | 부모 공유 경로, 독립 CL03 유지보수 명령 아님 |
| 처리 B open/close | 0609 RID132/133, AO72/73, BAD86; 0608 RID86 Inputs TOD13 | DB13.DBX9.0/9.1 Bool read | raw와 다른 DB 경로 |
| B 위치기억 open/close | 0609 RID11/134 AO67/66 BAD5; 0608 RID5 Flag TOD2 | DB2.DBX8.3/8.2 Bool S/R | 출력과 센서/DB에 의해 만든 기억, 현재 실물 위치 아님 |

[E04] hmi_plc_tags.csv 661~665행에 PV_01\GateB_Open DB11,X76.3, GateB_Close DB11,X76.4, Selector_GateB DB11,X76.6, Allarme1 DB11,X76.0 설정이 있다. CYL-CL03 독립 HMI 태그로 바꾸지 않는다. 부모 색인의 0391 HMI PV_2Gate CRef32 호출 실인수 17개 미결속을 유지하며 이번에 해소했다고 표시하지 않는다. CRef 결속은 본 실린더 독립 소유 근거가 아니다.

이름 점검은 decoded-original의 695 XML에서 ID.N 속성의 CL03/CL-03/CYL-CL03 문자열을 확인했으며 일치 0이었다(name-search.json). 이는 검색범위 내 명시 이름이 없다는 뜻이다. 무명/다른 별칭의 독립 회로까지 존재하지 않는다고 증명하지 않으며 695개 의미검토 완료로 세지 않는다.

## 3. 제어 구조와 소유

### 3.1 출력 고유 경로 직접 대조

[E05] 0279-FlgNet.xml, LAD1915/NID4와 0607 선언을 직접 연결했다.

- Contact410 ON은 W395/ORef385→RID1 M0.0. out W411이 네 B 접점 입력으로 분기한다.
- Contact412 W396/ORef386→RID46 M20.1; out W413→OR372.in1.
- Contact414 W397/ORef387→RID21 M21.1; out W415→OR372.in2.
- Contact416 W398/ORef388→RID47 M80.5; out W417→OR372.in3.
- Contact418 W399/ORef389→RID48 OFF M0.1; out W419→OR372.in4. 비반전 접점이다.
- OR372.out→W400→Coil377.in, Coil377.operand W402/ORef390→RID49 Output AO43(Q5.3).

따라서 해당 백업 정적 식은 Q5.3 = ON AND (OpenB00 OR OpenB01 OR maintenance PV01 OR OFF)다. ON/OFF는 메모리이며 상수가 아니다. Enable=0이 모든 병렬 경로를 차단한다고 쓰지 않는다. CL03 단독 enable/close 출력/시퀀스는 이 원본에서 찾지 못했다. 부모의 자동 허가·단계·공통 복수 쓰기는 PV01 문서의 공유 근거를 유지하며 실린더 자체 로직으로 복제하지 않는다.

### 3.2 위치 기억과 센서 한계

[E06] 0287-FlgNet.xml LAD1922/NID12를 직접 대조했다.

- ON Contact21 W54/ORef38→RID1, Q_B Contact22 W88/ORef89→RID49.
- Q 뒤 W57 병렬: raw-open Contact23 W58/ORef40→RID129→W59→OR27.in1; Contact24 literal false W60/ORef41→0610 RID130→W61→Contact25 raw-close W62/ORef42→RID131→W63→OR27.in2; 처리open Contact26 W64/ORef43→0609 RID132→W65→OR27.in3.
- OR27.out W66→SCoil28; operand W67/ORef44→RID11 B_MEM_OPEN.
- NOT Q Contact29 W91/ORef92→RID49, out W90→RCoil30, operand W70/ORef46→RID11.
- NOT Q Contact31 W93/ORef94→RID49 뒤 raw-close32 W73/ORef48→RID131 및 DB-close33 W75/ORef49→RID133가 OR34.in1/in2(W74/76)로 합쳐진다. W77→SCoil35, W78/ORef50→RID134 B_MEM_CLOSE.
- Q Contact36 W96/ORef97→RID49→W95→RCoil37, W81/ORef52→RID134.

OPEN 기억 Set은 ON·Q·[raw open OR (false AND raw close) OR DB open], Reset은 ON·NOT Q다. CLOSE 기억 Set은 ON·NOT Q·(raw close OR DB close), Reset은 ON·Q다. 0610 RID130은 literal false로 OFF(M0.1)와 다르다. raw/DB/MEM/HMI를 서로 동일한 관찰값으로 취급하지 않는다. P&ID가 CL03에 LS 리더선을 그리더라도 CL04 상태까지 별도 입력으로 확인되는 것은 아니다. 기계 결합·비동기 행정은 현장자료가 필요하다.

## 4. 전기·공압 전달 끝점

[E07] Electrical_Rev2.pdf를 실제 렌더해 아래 다섯 페이지 중 전기 네 페이지를 직접 판독했다. PDF 페이지는 1부터 세며 FG와 혼동하지 않는다.

| 원본 페이지 | 페이지 개정 | 끝점과 접속 확인 |
|---|---|---|
| FG141 / PDF142 | Rev2, 17.03.2025; 기본 27.05.2024 | MOD15 단자14 A5.3 EV-02 VALVE COMMAND→69/6 |
| FG69 / PDF70 | 개정란 공란; 기본 27.05.2024 | A5.3 141/1→69KA2 A1, A2→-0Vdc10.6; PLC측 DC 릴레이 코일 |
| 같은 FG69 | 동일 | 110Vac9.7→69KA2 실제 접점5–9→선69.3→X1/128 퓨즈단자(5×20 2A F 도면기재)→선69.4→EV02 A1; A2→X1/129→0Vac9.9 |
| FG70 / PDF71 | 개정란 공란; 기본 27.05.2024 | +24Vdc10.7→X1/134 퓨즈(5×20 2A F)→70.3→LS05 13/14→X1/135→E9.0 125/2; +24Vdc→X1/136→70.4→LS06 13/14→X1/137→E9.1 125/2 |
| FG125 / PDF126 | 개정란 공란; 기본 27.05.2024 | E9.0 LS05 B OPEN→MOD10 단자11; E9.1 LS06 B CLOSED→MOD10 단자12 |
| PID / PDF1 PV01 detail | Apex I / 15.01.2013 | EV02 공압선→CL03·CL04. CL03 리더 LS05/LS06. 실린더 포트 번호·호스 식별번호는 이 상세도에 제시되지 않음 |

DC PLC 출력→중계 릴레이 코일과 AC EV 부하 전원을 구분한다. CL03 자체에 전기 코일 A1/A2가 있는 것으로 쓰지 않는다. 접점표의 1/5/9 세 숫자와 실제 부하 접점5/9를 구별했다. 퓨즈 표기는 도면값이며 현행 보호설정 승인이나 교체 지시가 아니다. Q=0은 전기 명령 해제이며 실린더 닫힘/잔압 제거/안전 정지 확인이 아니다.

시공 ENT2TB·케이블 관계는 PV01 공유 초안의 참고이며 이번 고유 조사에서는 준공 심선 결속을 추가 확정하지 않았다. OEM X1과 현장 단자함 사이 심선표, EV02 포트→CL03 두 챔버의 호스표, 현행 실린더 명판·형식·행정·보어·부품번호가 필요하다.

## 5. 알람·복구

적용: PV01 B의 공통 감시를 관련 항목으로 참조. 미확보: CL03 독립 알람·독립 복구 신호. 부모의 알람·타이머를 CL03 고유 항목 수에 넣지 않는다.

PV01 공유 근거 §5의 0450 LAD1816/NID43은 B NOT_OPEN/NOT_CLOSE를 7초로 감시하며 MEM_OPEN/CLOSE를 사용한다. 참조 위치는 SD1517/S1523/R1528 및 SD1535/S1541/R1546, 값 W1568/ORef1549와 W1580/ORef1558→0656 RID320 S5T#7S다. 이는 이번에 다시 전 네트워크를 의미검토한 결과가 아니라 부모의 원본 확인 결과를 재사용한 것이다. A 4초와 합치지 않는다. 부모 Reset 조건(ON·RESET_ALLARM·해당 알람), 자동 허가·표시 결속 미확정도 유지한다.

알람 없음·리셋 성공은 CL03·CL04 동시 행정 또는 기계 복구의 증거가 아니다. raw 입력과 처리DB OR 경로·기억 래치 때문에 원시 센서만으로 감시를 설명할 수 없다. 실제 고장 원인, 재요청 조건과 현장 안전 절차는 승인 자료 및 관찰 없이는 단정하지 않는다. 이 초안은 가압·강제출력·바이패스·재기동을 지시하지 않는다.

## 6. 증상별 관찰·원인 구분

관찰 양식은 향후 자격 있는 담당자가 승인 절차에 따라 이미 확보한 기록을 비교하기 위한 것이며 행동시험 절차가 아니다. 시각/시간대, 관찰자, 현장 자산ID/명판, 프로젝트·CPU 식별, 명령/raw/DB/MEM/HMI 각 값·수집 위치, 사진·비교근거·배제결과·조치·복구증거를 분리한다. 값이 없으면 빈칸이며 0으로 채우지 않는다.

| 증상 | 함께 비교할 근거 | 아직 배제할 수 없는 범위 |
|---|---|---|
| 부모 열림 요청, CL03 무동작 | M20.1/M21.1/M80.5/OFF·Q5.3 기록, FG141→69KA2→EV02, EV02→CL03 호스/기계 자료 | PLC명령/릴레이/AC공급/EV/공압/실린더/링크 구간 중 어느 고장인지 미확정 |
| CL03·CL04 움직임 불일치 | 두 실제 행정의 같은 시각 자료, CL03 LS05/06 위치와 게이트 결합도 | 공유 EV 출력·CL03측 리더만으로 CL04 정상 확정 불가 |
| raw와 HMI가 다름 | I9.0/9.1, DB13X9.0/9.1, DB2X8.3/8.2, DB11X76.3/76.4 | 병렬 처리DB·래치·HMI 호출결속/갱신·현장 극성 미확정 |
| B 미도달 알람 | 부모 7초/MEM/출력 조건 및 같은 시각 행정 | CL03 단독 고장 진단 불가, CL04 또는 기계 연결 영향 포함 |
| 출력 해제인데 위치 유지 | Q와 릴레이/EV 관찰, 승인 공압 회로·잔압/스풀/기계 결합 자료 | Q=0을 닫힘·안전·무압으로 간주 불가 |

## 7. 완료·누락·검사 경계

| 7영역 | 상태 | 경계 |
|---|---|---|
| 설비·자료 | 적용 | P&ID CL03 고유구동관계 확인, 실물동일성 미확인 |
| IO/HMI | 적용/전용 근거 미확보 | 부모신호 직접 대조, 독립 신호 추정 금지 |
| 제어 | 적용 | EV02 출력·B 위치기억 직접 대조, 부모순서 공유 |
| 전기 끝점 | 적용 | 전기4쪽+PID1쪽 시각확인, 실물/호스포트 미확인 |
| 알람/복구 | 공통참조/독립 근거 미확보 | 부모 B7초 유지, 현장복구 미확인 |
| 증상관찰 | 적용 | 관찰항목만, 실제 기록·시험 없음 |
| 완료기준 | 적용 | 문서와 통합/현장 별도 |

누락과 다음 수집: (1) CL03 명판·태그 및 전체 게이트 배치 사진, (2) EV02–CL03/04 공압 포트·호스/기계 링크 승인도, (3) LS05/06 설치 위치·정상 극성·작동 범위, (4) OEM X1↔현장 단자함 심선표, (5) 현행 CPU 백업·DB/HMI 이벤트 Export. 새 자료 없이 실물동일성·독립 출력·현장복구를 반복 추정하지 않는다.

네 기능(도면·래더 비교, 백업·선택복원, 기록 전후비교, 보고서/PDF)은 통합 담당의 구현·검증 대상이며 이번에 작성/시험하지 않았다. note/repair_observation·미지 필드·타 설비·초안·저장키를 보존한다. UI/기록/게시 not_performed, TIA/live_cpu/field_recovery not_performed. 독립 검토는 부모 담당 대기이며 문서 작성 완료를 BC01 동등 기능 완료로 세지 않는다.

### 검사 수와 방법

선정 고정 원본 20개를 SHA256 및 git show 고정커밋 원본 바이트와 대조했고 20/20 일치했다. 그 중 고유 기술 의미검토는 10개 파일(equipment 1, PDF2, HMI1, XML6)이다. 정책/기준 9개 및 INVENTORY 1개는 분류·보존 검토이다. PDF 의미검토는 5페이지(전기4/PID1), XML은 6파일 중 선택 선언·네트워크다. 전체695 XML 이름 검색은 의미검토수에 포함하지 않는다. 모든 검사 스크립트는 자체 extracts에 둔 읽기 전용 정적 추출·해시 도구이며 원본 생성기를 실행하지 않았다.

## 부록 A. 선정 전체 원본 SHA256·Gitblob

경로는 source-mv06 기준. 각 행은 고정 커밋에서 읽은 blob 바이트와 로컬 바이트가 완전 일치한다. 전체 재현 검사 JSON은 ../extracts/CYL-CL03/source-integrity.json, 선택 선언/핀은 selected-xml.json, 이름 검색은 name-search.json, 시각자료는 같은 디렉터리의 PNG/TXT다. Git blob 식별자는 SHA256과 다른 Git 객체 식별자다.

| 원본 경로 | SHA256 | 고정 Gitblob | 바이트일치 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | 일치 |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | 일치 |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | 일치 |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | 일치 |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | 일치 |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | 일치 |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | 일치 |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | 일치 |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | 일치 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | 일치 |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | 일치 |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | 일치 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | 일치 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | 일치 |
| `all-in-one/sources/decoded-original/0279-FlgNet.xml` | `4ae9c9ae70987b778a159c896b88fa4e34cf6f597903a0c68e630708b5f1bfd1` | `dfefe5fcd17064a89f61e38f34e9c4d7bb1d01e5` | 일치 |
| `all-in-one/sources/decoded-original/0287-FlgNet.xml` | `885e0619ad4a49a2a873b4f0f069eafc62b350f4a12f060e4def9c020f3fe616` | `7911c5e5d9d9578f60012be454481ca434aaa831` | 일치 |
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | 일치 |
| `all-in-one/sources/decoded-original/0608-IdentXmlPart.xml` | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | 일치 |
| `all-in-one/sources/decoded-original/0609-IdentXmlPart.xml` | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | 일치 |
| `all-in-one/sources/decoded-original/0610-IdentXmlPart.xml` | `c58d07b1b9707dc8c6c2f06c34ee6142f72238a4cf3f376bee8502d1a9532f9d` | `1497b6bfd7fd9b8afe427b9c910d15e9cf888f9c` | 일치 |

### 공유색인·작업범위 보조자료

아래는 고정 Git 원본이 아닌 로컬 색인/지시 자료로, 위20개에 합산하지 않는다.

| 경로 | SHA256 |
|---|---|
| `gme-research/drafts/PV01-DOTS-DRAFT.md` | `ed9c8d774ab53ab5c725580f22b076268bc157f09bdccd1a35518e3819670b9e` |
| `gme-research/progress/BATCH19-RESEARCH-INSTRUCTIONS.md` | `9edbb2bd6c733ecbceff7bcef669cbfaa255514f9d886b6b5730e052c28244a9` |
| `gme-research/progress/TASK3-BATCH19-SCOPE.json` | `3cd12b4cb15ef9543507407a72077785845c8749309b345ed230a10e3abfc5e2` |
| `gme-research/progress/GME-CATALOG-OVERLAP-REVIEW.json` | `027c2d89b034f3681dced7db98146ffd77eecfad116a1a94cac035ccbd598967` |
