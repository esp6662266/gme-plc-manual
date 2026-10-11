# ER01 전기 히터 7영역 원본 조사 초안

- 표준: GME-STD-1.0.0 / WORK-ITEM-TEMPLATE 구조 적용.
- 대상: catalog_id `ER01`, 전기 히터, kind `heater`, group `집진·석회`, parent_id 없음, priority_key 없음.
- 작업 구분: 사용자 작업3의 두 번째 묶음에 속한 클라우드 조사 초안. 신규 연구분모132의 독립 ID이며, FN05 초안과 소유 경계만 대조했다. FN05의 값·타이머·고장식을 복제하지 않았다.
- 기준: 읽기 전용 `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION.json `1.12.0`. 현재 게시물/온라인 CPU를 나타내지 않는다. 로컬 목표의 **2차133 통합·게시 제외는 유지**한다.
- 착수: 2026-10-11 09:25 UTC. 종료 시각·무결성 검사는 부록에 기록한다. 실행 모델/추론 수준은 이 조사 과정에서 독립 관측 불가하여 미확인.
- 수정 범위: `drafts/ER01-DOTS-DRAFT.md`와 `extracts/ER01/`만. 원본, 공통 코드, 버전, 대장, 배포, 현장/PLC/보호값, SEJIN 프로그램·운영자료 변경 없음. 공유 declarations.json 덮어쓰기 없음.
- 문서 상태: `draft_complete_with_gaps`, 자체 원본 정적 대조 수행, 핵심 근거 제한 대조 완료; 사용자 독립 검토 대기. UI/기록 구현·통합·게시·TIA·현재 CPU·현장 복구는 미수행.
- 시뮬레이터 작성·수정·생성·실행·행동시험을 하지 않았다. 중지 원본의 선언상 다른 쓰기는 존재만 기록하며 활성화/동작 근거로 쓰지 않는다.

## 먼저 확인할 결론

1. ER01의 PLC 출력은 `Start ER-01 %Q5.0`, 피드백 원시 입력은 `%I6.1`, 처리 피드백은 `Inputs.Feedback_ER01 DB13.DBX6.1`이다. FG66의 피드백은 66KA1 보조접점13–14이므로 실제 히터 발열·공기온도·풍량을 직접 입증하지 않는다.
2. LAD1971 출력 접점은 `ON AND Flag.M_ER01 AND Inputs.177T1_OK`다. 온도허가 입력은 **%I28.4 → DB13.DBX22.4로 개별 비트 재매핑**된다. 같은 byte 번호의 Word 복사로 추정한 연결이 아니다.
3. 요청 Reset은 `ON AND (OFF OR Allarm.ER01_run OR ((NOT Inputs.FN-05 RUN) AND (NOT UNDER TESTING)))`다. FN05의 처리 Run은 ER01 요청 유지 조건에 관여하지만 FN05 자체 고장과 ER01 고장은 별도 소유다. OFF는 메모리 비트이며 문자 이름만으로 0 상수로 치환하지 않는다.
4. 고유 고장은 LAD1822의 **IEC TON / Er_01_Run_Rit DB32 / T#2S(2000 ms)**다. `ON AND Q5.0 AND NOT DB13.DBX6.1`을 감시해 `Allarm.ER01_run DB3.DBX20.1`을 Set한다. FN05의 SD/%T96/S5T#2S와는 다른 타이머다.
5. 온도허가 상실은 출력 직렬 접점을 끊지만 LAD1971의 요청 Reset 분기에는 없다. 요청이 유지되는 경우 온도허가 회복에 따라 출력이 다시 평가될 수 있는 정적 구조다. **실제 재통전 여부·시점은 미검증이며, 허가 회복·고장 해제·운전 요청·현장 복구를 별도 확인해야 한다.**
6. HMI 설정은 DB2.X5.4/DB11.X68.0/DB11.X68.1 세 개가 확인된다. 실제 HMI 호출의 ORef24/26/33/35 선언 결속과 화면 이벤트는 미확정이다. P&ID의 로컬 TC11과 전기도면 177T1을 같은 실물로 단정하지 않는다.

## 7영역 적용표

| 영역 | 판정 | 작성 위치 | 남은 경계 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | 1 | 현행 히터·온도조절기 명판/현장 대응 미확인 |
| I/O·HMI | 적용, 일부 근거 미확보 | 2 | HMI 실제 이벤트·4개 호출 ORef 결속 부족 |
| 제어 구조 | 적용 | 3 | 접점/핀/호출/쓰기 정적 확인, 온라인 실행순서 미검증 |
| 전기 전달 경로 | 적용 | 4 | FG/PDF 실제 렌더 확인, 승인 시공/현재 부품 미확인 |
| 알람·복구 | 적용 | 5 | 고유 TON·Set/Reset 확보, 실복구·재통전 확인 없음 |
| 증상별 수리 | 적용, 관찰 설계 | 6 | 관찰·원인 배제 설계이며 실제 수리/시험 아님 |
| 완료 기준 | 적용 | 7 | 문서·UI·게시·TIA·CPU·현장 상태 분리 |

## 근거 읽는 법

`D/`는 고정 repo의 `all-in-one/sources/decoded-original/`이다. LAD는 검색 document_id이며 내부 NID와 다르다. XML이 한 줄이거나 재정렬될 수 있어 핵심 위치는 **파일 + Part/Wire UID + ORef/RefId + 선언 RID/NID**로 제시한다. PDF 페이지는 1기준이며 FG는 도면 인쇄번호다. FG254는 PDF257이므로 일괄 FG+1 계산을 사용하지 않는다.

네트워크 색인·equipment CSV·live_index는 탐색/추출 근거다. 주요 논리는 원본 FlgNet와 IdentXmlPart 선언의 Global/Local, SSD/SAD/BAD/TOD, 상수, 핀과 함께 대조했다. 일치하지 않는 HMI 선언은 추출 이름만으로 확정하지 않았다. 원본 SHA256과 고정 커밋 git blob 바이트 대조 결과는 부록에 있다.

## 1 설비와 자료 기준

### 1.1 ID와 소유 경계

- `docs/equipment-standard/INVENTORY.json`의 ER01은 `phase2/planned/baseline/not_assessed`, 부모/우선키/제외사유/보류부모 없음이다. `registers/equipment.json`은 FG66 및 FN05와 석회 투입 공기 가열 경로를 가리킨다.
- 읽기 전용 preflight 결과 `inventory_matches=true`: 전체248, root108/child140, 우선23/대응18, 제외90, 부모보류7, phase2 133 유지. 과거 저장 해시와 다른 `requirements-audit.json`·`all-in-one-data.json` 2개는 이미 있는 바이트 차이이며 이번 ER01 변경 또는 설비 완료로 계산하지 않는다.
- 신규 연구132는 별도의 범위 overlay다. 전체248에서 우선 대응18·제외90·부모보류7·SYS-SIMULATION1을 차감한 값이다. 원본 대장의 phase2 133은 수정하지 않는다. ER01은 첫5 FN05/SC01/PV03/MV02/MV05와 중복되지 않는다.
- FN05는 공기 송풍 구동, ER01은 전기 히터, VR06은 로터리 밸브, LD01은 피더 본체다. FN05 처리 Run을 ER01이 읽고 ER01 출력 상태를 VR06이 읽어도 소유자와 ID를 합치지 않는다.
- P&ID PDF1 상세에는 FN05/M41 → ER01(6 kW 440V) → VR06/LD01 투입 연결부 및 공정 배관 방향이 보인다. ER01 근처 TC11은 별도 로컬 온도 표시이며 catalog TC11도 PLC 대응 미식별로 남아 있다. TC11=177T1 또는 ER01 전용 PLC 아날로그 온도채널로 확정하지 않는다.

### 1.2 판본과 자료 한계

| 자료 | 실제 표시 | 해석 경계 |
|---|---|---|
| GME_20250506.zap18 / PEData.plf / decoded XML | 백업 파일·추출 XML, 고정 커밋 보존 | 파일명 날짜를 현재 CPU 백업 일시로 보증하지 않음 |
| Electrical_Rev2.pdf FG66/PDF67 | ELECTRICAL RESISTANCE ER-01, DATA 27.05.2024 | 3상440V60Hz, 6kW/13.6A는 도면 표기. 현행 정격/실측 아님 |
| FG122/PDF123 | Rev2 17.03.2025, DATA 27.05.2024 | 입력 E6.1 매핑 설계. 현행 CPU/모듈 일치 미검증 |
| FG141/PDF142 | Rev2 17.03.2025, DATA 27.05.2024 | 출력 모듈 회로. 고해상도 개정란 재확인 |
| FG177/PDF178 | DATA 27.05.2024, 별도 개정값 미표시 | 온도접점 회로 설계 |
| FG254/PDF257 | MATERIAL LIST, DATA 27.05.2024 | 부품 후보. 설치부품/교체 승인 근거 아님 |
| PID_1684n002I.pdf PDF1 | 도면1684n002, 원도06/04/2011, Rev I 15/01/2013 | 공정 연결과6kW440V 표기. 현행 배관/온도허가 설정 미확인 |
| Electrical_Can_Decoating_20241118.pdf PDF36/51 | `24.11.11 first draft design`, 승인칸 공란 | 참고 경로·케이블 설계. 승인 시공·실제 길이로 확정하지 않음 |

P&ID의 ER01 6kW440V와 FG66의 6kW 표기는 같은 설계값을 제시한다. 이것만으로 13.6A가 현행 실측 전류이거나 해당 전압·결선에서 검증된 정격이라고 계산/보증하지 않는다. 재료표의 접촉기7.5kW 설명도 ER01 히터가7.5kW라는 뜻이 아니다.

### 1.3 비해당과 근거 미확보

- 확보된 ER01 출력은 접촉기 on/off 경로다. 이 경로에 팬 인버터 주파수·모터 rpm 환산을 적용하는 것은 비해당이다.
- 전용 PLC PID 루프, ER01 아날로그 온도 환산, 전류센서, 히터 운전시간 카운터, 독립 풍량 확인은 이번 직접 원본에서 확보되지 않았다. 현장에 없다고 단정하지 않는다.
- 177T1의 설정온도·히스테리시스·수동/자동 리셋 종류·안전 등급, TC11과의 실물 관계, 히터 발열체 구성/절연 기준/정비주기/제조사/현행 품번은 근거 미확보다. 다른 계통 온도값이나 일반적인 권장값으로 채우지 않는다.

## 2 I/O와 HMI

### 2.1 물리 신호와 DB 주소

SSD.AO는 bit offset이며 byte.bit로 변환했다. GlobalAccess는 BAD.BIRID와 해당 DepDBBlock.TOD DB 번호를 함께 확인했다. 아래 주소는 백업 기준이며 현재 온라인 주소/값은 미확인이다.

| 신호 | 주소·형식 | 직접 선언 근거 | 역할 |
|---|---|---|---|
| Start ER-01 | %Q5.0 Bool | D/0602 RID185 SAD Output/AO40; NID41 UID1136 Write. D/0658 RID243 NID49 UID34 Read | 물리 출력 이미지. live_index doc1279 주석의 `a 60.4`를 주소로 쓰지 않음 |
| er01_fbk | %I6.1 Bool | sources/live_index.json `_7ev` doc519 Address/Datatype/Name; FG66/122의 E6.1, 아래 %IW6 복사 | 원시 접촉기 응답. 개별 이름의 SimpleAccess 선언은 이번 추출에서 미확보 |
| Inputs.Feedback_ER01 | DB13.DBX6.1 Bool | D/0657 RID313 AO49/BAD247; D/0655 RID247 TOD13, NID49 UID35 | 처리 피드백. 원시 입력·HMI 표시와 분리 |
| Flag.M_ER01 | DB2.DBX5.4 Bool | D/0604 RID192 AO44/BAD2; D/0603 RID2 TOD2, NID41 UID1134 Write/1135 Read | 운전 요청 메모리 |
| Allarm.ER01_run | DB3.DBX20.1 Bool | D/0604 RID217 AO161/BAD5→D/0603 RID5 TOD3; D/0657 RID246/BAD10→D/0655 RID10 TOD3 | 피드백 불일치 래치 고장. 이름 run을 정상 Run으로 해석하지 않음 |
| 177T1_OK | %I28.4 Bool | D/0627 RID141 SAD Input/AO228, NID1 UID87 | 온도접점 원시 입력 |
| Inputs.177T1_OK | DB13.DBX22.4 Bool | D/0629 RID148 AO180/BAD4→D/0628 RID4 TOD13; D/0604 RID266/BAD218→D/0603 RID218 TOD13 | ER01 출력 직렬 허가. 원시 I28.4와 byte 번호가 다름 |
| Inputs.FN-05 RUN | DB13.DBX6.0 Bool | D/0604 RID225 AO48/BAD218→D/0603 RID218 TOD13 | 다른 설비 FN05 처리 응답, ER01 요청 Reset에서 읽음 |
| ON / OFF | %M0.0 / %M0.1 Bool | D/0602 RID1 AO0 / RID33 AO1, SAD Memory | 공통 허가/Reset 분기의 메모리. 1/0 상수 가정 금지 |
| UNDER TESTING | %M5.5 Bool | D/0602 RID4 SAD Memory/AO45 | FN05 미응답 Reset 분기의 반전 접점 |
| Flag.Maintenance_ON | DB2.DBX7.5 Bool | D/0604 RID3 AO61/BAD2→DB2 | UNDER TESTING의 작성 경로에서 읽음 |
| Flag.RESET_ALLARM | DB2.DBX6.0 Bool | D/0657 RID13 AO48/BAD12→D/0655 RID12 TOD2 | 고장 Reset 요청, ER01 기동 요청이 아님 |
| Er_01_Run_Rit | DB32 IEC_TIMER | D/0654 AufDBBlock RID312, TOD32; D/0456 Instance29/NID49 | PLC TON 인스턴스. %T 타이머/HMI 태그 아님 |

### 2.2 원시 I6.1에서 처리 피드백으로 가는 Word 복사

LAD1070 / `D/0397-FlgNet.xml`, 내부 NID1:

- Part42 Move의 Wire21은 Powerrail→42.en이다.
- Wire52: ORef45/RID13→42.in. D/0627 RID13 `Tag_171`, Word, SAD Input/AO48 = `%IW6`.
- Wire54: 42.out1→ORef46/RID14. D/0629 RID14 GlobalAccess Word/AO48/BAD4, D/0628 RID4 Inputs/TOD13 = `DB13.DBW6`.
- 따라서 백업의 Word 복사 `%IW6 → DB13.DBW6`가 I6.1과 DB13.DBX6.1을 연결한다. FN05 I6.0은 같은 Word의 다른 bit이며 독립 소유다.
- Part42 `DisableENO=true`와 후행 Wire53 `42.eno→43.en`은 그대로 보존한다. 직접 out1 연결과 무관한 ENO 이후의 실행 의미를 확대하지 않는다.
- ORef46 UID/RID가 D/0625의 Allarm 후보와도 검색되지만 그 호출은 NID39다. 이 네트워크의 NID1·GlobalAccess/BAD4·핀을 맞춘 D/0629를 사용했다. UID/RID만으로 다른 블록의 선언을 결속하지 않는다.

### 2.3 177T1의 개별 비트 재매핑

같은 LAD1070이지만 177T1은 Word 복사가 아니라 별도 Contact→Coil 경로다.

| 구간 | 정확한 위치 | 확인한 의미 |
|---|---|---|
| 원시 입력 | D/0627 RID141 `177T1_OK`, Input AO228=%I28.4, NID1 UID87 | 물리 입력 선언 |
| Contact | D/0397 Wire21 Powerrail→Part86.in; Wire85 ORef87→86.operand | 반전 표시 없는 접점 |
| 전달 | Wire129 Part86.out→Part125.in | 단일 비트 논리 전달 |
| 처리 Coil | Wire128 ORef126/RID148→Part125.operand | 쓰기 끝점 |
| DB 결속 | D/0629 RID148 AO180/BAD4; D/0628 RID4 TOD13, NID1 UID126 AK=Write | DB13.DBX22.4 |
| 소비 | D/0271 ORef31/RID266→Wire29 Part30.operand | ER01 출력에 직렬인 처리허가 |

현재 raw/DB 두 값이 같다는 온라인 증거는 없다. 갱신은 아래 호출 조건에 의존한다. 주소 번호 차이를 오류로 고치거나 %IW28→DB13.DBW28로 만들어 설명하지 않는다.

### 2.4 입력 호출과 값의 시점

LAD1613 / D/0030, 내부 NID19: Recipes Handler CRef21 → Wire32 ENO → HMI CRef23 → Wire33 ENO → HMI Output CRef25 → Wire42 → Part37의 반전 `Simulation(1)` 접점 → Wire43 → HMI Inputs CRef28.en.

- CodeBlock22/24/26/29는 D/0688 RID120/124/128/135의 FC 이름, CRef21/23/25/28는 D/0694 RID121/125/129/136, ORef45/RID140는 D/0692 SimpleAccess로 대조했다.
- 따라서 입력 DB를 무조건 매 스캔 갱신된다고 쓰지 않는다. ENO 연쇄와 반전 접점의 정적 연결만 확인했다. 이 설명은 중지 경로를 실행하거나 허용한 것이 아니다.
- 다른 쓰기 조사에서 DB13.DBX22.4의 명명 Write는 D/0629 NID1 UID126 하나를 확인했다. DB13의 확보된 anonymous Word Move 범위는 DBW0..20이고 DBX22.4를 덮는 Word22/28 쓰기를 찾지 못했다. 미추출·간접주소·HMI 외부 쓰기까지 배제한 결과는 아니다.

### 2.5 HMI 세 태그와 미결속 호출

`sources/hmi_plc_tags.csv`의 헤더 포함 행134/422/457:

| HMI 태그 | 설정 주소 | ID | 확인 수준 |
|---|---|---|---|
| ER_01\Allarme1 | DB11,X68.1 | 0032A | dde.cfg 설정 추출. 표시/쓰기 이벤트 미확인 |
| ER_01\RispostaA | DB11,X68.0 | 001B5 | 응답 표시 후보. I6.1 자체 아님 |
| ER_01\Flag | DB2,X5.4 | 0018D | 요청 메모리 주소와 일치. 버튼 Set/Reset/Toggle 미확인 |

LAD1211 / D/0387의 배선은 다음과 같다. 네트워크 색인 NID는 null이며 핵심4개 선언 결속이 부족하다.

| Wire | 호출 핀 | ORef/RefId | 직접 확인 상태 |
|---|---|---|---|
|21|CRef22.en|Powerrail|호출 en 연결|
|37|Ingresso_run|24/657|이 호출에 맞는 선언 결속 미확보|
|39|Allarme1|26/401|이 호출에 맞는 선언 결속 미확보|
|40/41/42/43|Allarme2/3/4/5|27/28/29/30 모두 RID48|D/0626 FALSE 후보. 반복 UID와 NID 때문에 적용 대상 확정 주의|
|46|Risposta 출력|33/404|쓰기 대상 선언 결속 미확보|
|48|Comulativo_allarmi 출력|35/406|쓰기 대상 선언 결속 미확보|

CodeBlock23/RID1는 D/0623 `HMI Standard Motors` 호출군, CRef22/RID638은 D/0624의 인터페이스군으로 대응한다. 검색 색인의 `Inputs.Feedback_ER01`, `Allarm.ER01_run`, `Motors.ER01.Risposta/Allarme_comulativo`는 유력 후보지만 누락된4개 선언의 대체 증거로 사용하지 않는다.

공통 함수 LAD331 / D/0355 및 D/0621 Local 선언에서는 Ingresso_run ORef24/RID16→Part23→Wire25 Part27 Coil→Wire26 Risposta ORef28/RID17, Allarme1..5→Part41 O(5입력)→Wire57 Part59 Coil→Wire58 Comulativo_allarmi ORef60/RID22이다. 공통 Local 함수 구조를 ER01의 DB11 주소 결속 증명으로 확대하지 않는다.

실제 HMI dde.cfg 원문/화면 객체/로그인 권한/이벤트/현재 통신 상태가 추가로 필요하다. HMI 종합표시가 꺼졌다는 사실만으로 고유 DB3 고장·접촉기 피드백·열 상태가 모두 정상이라고 판정하지 않는다.

## 3 제어 구조

### 3.1 호출자와 실행순서

- LAD1619 / D/0031: Part282 ON→Wire283→Allarms1 CRef264.en. D/0688 CodeBlock275/RID58, D/0694 CRef264/RID59, 내부 NID6으로 대조.
- LAD1620 / D/0549: Part350 ON→Wire351→Motors1 CRef319.en. D/0688 CodeBlock337/RID67, D/0694 CRef319/RID68, 내부 NID7. 같은 Wire에 다른 FC들도 병렬 연결되어 있다.
- LAD1723 / D/0024, 색인 `cyc_int2 ogni 1s`: Wire190 Powerrail→Part188 ON, Wire187 ORef185/RID36, Wire189 Part188.out→CRef183.en. D/0067 CodeBlock186/RID39=`Auto start motors`, D/0068 CRef183/RID40, D/0652 ON/NID4.
- `ogni 1s`라는 블록 명칭은 백업의 주기 의도를 가리킨다. 현재 OB 주기/중단 우선순위/실행순서를 현장 설정으로 검증하지 않았으므로 `Tempo_presetting=13`을 무조건13초라고 바꾸지 않는다.
- ON이 거짓이거나 호출되지 않을 때의 출력/DB 보존, 물리 출력 갱신 시점, 통신 지연, 다른 OB의 간접 쓰기는 현재 CPU와 TIA 전체 프로젝트로 추가 검증해야 한다.

### 3.2 ER01 요청 Reset과 출력

LAD1971 / D/0271, 내부 NID41의 정적 접점식을 펼치면 다음과 같다.

- 요청 Reset: `ON AND (OFF OR Allarm.ER01_run OR ((NOT Inputs.FN-05 RUN) AND (NOT UNDER TESTING)))` → RCoil `Flag.M_ER01`.
- 출력 Coil: `ON AND Flag.M_ER01 AND Inputs.177T1_OK` → `Start ER-01`.

| 부분 | Part/Wire/ORef 근거 | 해석과 경계 |
|---|---|---|
| ON 공통 | Wire1159 Powerrail→Part1149; Wire1137 ORef1130/RID1→operand; Wire1150 분기 | ON 이후 Reset3분기와 출력요청 분기 |
| OFF Reset | Part1151, Wire1138 ORef1131/RID33; Wire1152→O1120.in1 | OFF는 %M0.1. 이름만으로 무효 분기 처리 금지 |
| 고유 고장 Reset | Part22, Wire21 ORef23/RID217; Wire24→O1120.in2 | Allarm.ER01_run을 읽음 |
| FN05 미응답 | Part26 operand Negated, Wire25 ORef27/RID225; Wire28→Part1155 operand Negated; Wire1140 ORef1133/RID4; Wire1156→O1120.in3 | FN05처리Run과 UNDER TESTING의 반전 AND |
| 요청 Reset 끝점 | O1120 Card3→Wire1142 Part1125 RCoil; Wire1144 ORef1134/RID192 | D/0604 NID41 UID1134 AK=Write |
| 요청 접점 | Part1157, Wire1145 ORef1135/RID192; Wire1158→Part30 | 요청은 출력과 별도 메모리 |
| 온도허가 | Part30, Wire29 ORef31/RID266; Wire32→Part1129 Coil | Inputs.177T1_OK가 직렬. 반전 없음 |
| 출력 끝점 | Part1129, Wire1147 ORef1136/RID185 | D/0602 NID41 UID1136 AK=Write, Q5.0 |

이 구조에서 177T1_OK가 거짓이면 해당 출력 Coil의 직렬 경로가 끊긴다. 그러나 그것만으로 M_ER01을 Reset하는 경로는 이 네트워크에 없다. M_ER01이 계속 참이고 다른 조건도 유지된다면 허가 회복 시 출력 경로가 다시 참이 될 수 있다. 이것은 원본 정적 해석이며 실제 자동 재통전을 시험하거나 복구 안전성을 보증한 결과가 아니다.

고장 Set/요청 Reset/출력 Coil의 같은 스캔 최종 상태는 호출과 실행순서에 영향을 받는다. 식을 단순 논리값으로 계산한 결과를 현재 운전 상태로 제시하지 않는다.

### 3.3 유지보수 비트의 작성 경로

LAD1930 / D/0237, NID1: Part47 ON→Wire48 Part49 `Flag.Maintenance_ON`→Wire50에서 Part34 `UNDER TESTING` 및 Part36 `Allarm.Maintenance_ON` Coil로 병렬 분기한다.

- ORef38/RID1→Wire42, ORef39/RID3→Wire43, ORef40/RID4→Wire44, ORef41/RID6→Wire45.
- D/0602 RID1/4 및 D/0604 RID3/6의 NID1 호출로 결속했다.
- ER01의 UNDER TESTING은 FN05 미응답 Reset 분기에만 들어간다. 고유 고장·OFF Reset·177T1 출력허가 전체를 우회한다고 쓰지 않는다. 이 비트를 켜거나 강제하라는 운전/수리 지침은 제공하지 않는다.

### 3.4 다른 쓰기와 정지 경로

명명 선언뿐 아니라 같은 주소를 포함하는 Word 쓰기도 검색했다. 범위는 고정 원본 IdentXmlPart 전부 및 해당 FlgNet이며 현재 HMI/간접주소/누락 원본까지 모두 배제한 검사는 아니다.

| 대상 | 확보된 다른 쓰기 | 영향과 한계 |
|---|---|---|
| M_ER01 DB2.X5.4 | LAD1847 D/0166 NID5 Part931 RCoil/ORef1005 RID101; D/0577 | 자동정지에서도 요청을 지움 |
| M_ER01 포함 DB2.DBW4 | LAD402 D/0147 NID2 Part144 Move out1→Wire192 ORef173/RID11; D/0563 AO32 Word/BAD6→D/0562 Flag DB2 | INT#0 Word쓰기 범위가 byte4..5이므로 X5.4 포함. named-only 검색으로 놓치면 안 됨 |
| Q5.0 | D/0602 NID41 UID1136 직접 Write를 확인. 확보된 Output address-span Write에서 추가 겹침 미발견 | 이름뿐 아니라 %Q 영역폭도 검사. 외부강제/간접쓰기·현재 온라인은 별도 |
| DB13.X6.1 | 정상경로 D/0397의 DB13.DBW6 Word쓰기. 중지 원본 D/0635 RID148 NID5 UID42 Write도 선언에 남음 | 중지 원본을 실행/활성 확인하지 않음. 현재값 기원으로 채택하지 않음 |
| DB13.X22.4 | D/0629 RID148 NID1 UID126 Write | I28.4에서 개별 재매핑. 추가 겹치는 DB13 Word쓰기 미발견 |
| DB3.X20.1 | D/0657 RID246 NID49 UID36 Set / UID44 Reset | D/0148 startup의 확보된 DB3.DBW0..16 초기화 범위와 다름. 전체 알람을 초기화한다는 제목만으로 ER01까지 초기화된다고 하지 않음 |

LAD402 Word 초기화의 공급은 Part208 ON→Wire209 Part138.en, Part138.eno→Wire187 Part141.en, Part141.eno→Wire190 Part144.en이다. Wire191 ORef172/RID54→Part144.in은 D/0048 `INT#0`이며 Wire192가 DB2.DBW4에 쓴다. startup 호출 발생/유지값/현행 리텐션 설정은 미검증이다.

LAD1847의 ER01 정지 분기는 아래와 같이 직접 대조했다.

- Part1095 `Flag.Auto_ON1`(ORef983/RID4, Wire1028), Part881 Eq(Int) `Data.Tipo_preset`(ORef984/RID12, Wire1029) = 상수5(ORef985/RID22, Wire1030).
- Wire1031이 Part923 Eq.pre와 Part1122 Contact.in 양쪽으로 분기.
- Part923 `Data.Tempo_presetting`(ORef1001/RID7, Wire1053) = 상수13(ORef1002/RID100, Wire1054)→Wire46 O45.in1.
- Part1122 `Allarm.Emergency_module_fault`(ORef1123/RID108, Wire1125)→Wire47 O45.in2.
- O45.out→Wire1055 Part931 RCoil→Wire1058 ORef1005/RID101 `Flag.M_ER01`.
- 해석: `Auto_ON1 AND Tipo_preset=5 AND (Tempo_presetting=13 OR Emergency_module_fault)`에서 요청 Reset. 비상모듈 분기도 선행 Auto_ON1/Tipo_preset=5의 허가를 공유한다. ER01 고유 비상입력 또는 무조건 전역 차단이라고 바꾸지 않는다.
- 주소: D/0577 RID4 Auto_ON1 AO59→DB2.X7.3; RID12 Tipo_preset AO784→DB1.DBW98; RID7 Tempo_presetting AO768→DB1.DBW96; RID108 Emergency_module_fault AO134→DB3.X16.6. D/0576 RID3/6/107의 TOD2/1/3으로 대조.

현재 확보된 ER01 명명 PLC 쓰기에서는 요청 Set Coil을 찾지 못했다. HMI Flag 설정은 요청 진입의 후보지만 실제 버튼 이벤트를 확보하지 못했으므로 “HMI 버튼이 반드시 Set한다” 또는 “자동 기동한다”로 확정하지 않는다.

### 3.5 VR06이 읽는 ER01 출력

LAD1969 / D/0269, NID39는 VR06 소유 네트워크다.

- Part1103 ON→Wire1104 분기. Part1105 VR_06_FAULT→Wire1106 O1074.in1.
- Part1107(operand Negated) ORef1086/RID185=`Start ER-01`→Wire1108 Part1109(operand Negated) ORef1087/RID4=`UNDER TESTING`→Wire1110 O1074.in2.
- O1074→Wire1096 Part1079 RCoil, Wire1098 ORef1088/RID186=`Flag.M_VR_06`.
- 따라서 VR06의 해당 요청 Reset 조건은 `ON AND (VR_06_FAULT OR (NOT Q5.0 AND NOT UNDER TESTING))`다. **ER01 실제 피드백 DB13.X6.1이 아니라 출력 Q5.0을 읽는다.**

ER01 출력 상실이 이 경로에서 VR06 요청에 영향을 줄 수 있지만 VR06의 최종 운전/재기동·LD01 영향 전체는 그 설비 조사 범위다. ER01 알람으로 VR06 자체 고장을 새로 만든다고 쓰지 않는다.

## 4 전기 전달 경로

아래 회로는 원본 PDF를 직접 렌더하여 글자·접점·단자 양 끝점을 확인했다. 현장 작업 허가나 충전부 측정 지침은 아니다. 실물 점검은 승인 절차와 자격을 갖춘 담당자가 전원·잔열 등 위험을 통제한 상태에서 수행해야 한다.

### 4.1 주전력 경로

`Electrical_Rev2.pdf` FG66/PDF67:

1. 상단 THREE-PHASE LINE 440V 60Hz, 앞 FG65/9에서 오는 `8.3L1/8.3L2/8.3L3`.
2. `66FU1`, 도면 표시 `25A GL 10x38`, 각 상 단자1–2/3–4/5–6.
3. `66KA1` 주접점1–2/3–4/5–6, 코일 참조66/4.
4. 전선표기 `BLACK FS17 4 mmq`, 식별66U1/66V1/66W1.
5. 단자 `XM 66U1 / XM 66V1 / XM 66W1` → ER01 L1/L2/L3 발열체. 도면은 `6 kW A 13,6` 표기.

확보된 회로에는 별도 인버터/아날로그 전력제어기가 그려져 있지 않다. PE 경로·실제 발열체 결선·상별 전류·단선·절연상태는 이 도면만으로 완료 판정하지 않는다. 25A는 도면 부품 표기이며 보호값 변경 권고가 아니다.

### 4.2 출력에서 접촉기 코일까지

- FG141/PDF142: CPU515/MOD15 출력 A5.0, 단자11, “ER-01 ELECTRICAL RESISTANCE COMMAND”, 참조66/4. 개정란 Rev2 17.03.2025를 확대 렌더로 재확인했다. 옆 A5.1/단자12의21/5는 EV03 경로이며 ER01로 가져오지 않는다.
- 같은 페이지의 출력군 전원은 `+24Vdc10.9 → X21 3033 5x20 4A F → 선141.1 → 모듈 단자19`; 단자20은 `-0Vdc10.6`으로 연결된다. A5.0 한 채널만의 별도 보호기라고 해석하지 않는다.
- FG66/PDF67: A5.0/141/1 → 66KA1 코일A1; A2 → `-0Vdc10.6`. 코일 병렬의 억제소자 표기를 확인했다.
- 따라서 Q5.0 논리 참, 모듈 출력 전압, 코일 여자, 주접점 도통, 발열은 각각 별도 관찰 지점이다. Q5.0만으로 후단 모두를 정상 처리하지 않는다.

### 4.3 보조접점 피드백에서 PLC까지

- FG66/PDF67: `+24Vdc10.7`(65/7에서 공급) → `66KA1 보조접점13–14` → `E6.1`, 참조122/2.
- FG122/PDF123: E6.1/66/6 → CPU515/MOD9 입력 단자22, “FEEDBACK ER-01 ELECTRICAL RESISTANCE”.
- 이 경로는 접촉기 보조접점 응답이며 히터 전류·주접점3극 모두·열 도달·풍량을 독립 측정하지 않는다. 접점 도면기호와 정상 운전 시 실제 극성/배선상태는 구분한다.

### 4.4 온도접점에서 출력허가까지

- FG177/PDF178: `+24Vdc152.5`(176/9) → X3:117의 `5x20 2A F` → 선177.1 → `177T1 접점11–12` → X3:118 → X22:4007 → E28.4 → CPU515/MOD4/Rack3 입력 단자5.
- 기능명은 THERMOSTAT ELECTRICAL RESISTANCE ER-01. 접점의 t> 기호와11–12를 렌더 확인했다.
- PLC 연결은 D/0397의 `%I28.4 → DB13.X22.4` 개별 비트 경로, 그 처리허가는 D/0271 Part30을 거쳐 Q5.0 출력에 직렬이다.
- 이 도면/PLC 범위에서 177T1을 66KA1 코일의 직접 하드와이어 직렬접점으로 그리면 오류다. 확보된 그림은 PLC 입력으로 들어가며 소프트웨어 허가에 사용된다. 별도 안전회로 존재·등급·안전 기능 적합성은 확인하지 않았다.
- 설정온도/자동복귀 여부/트립시험/현재극성은 미확정이다. P&ID TC11과의 물리 동일성도 부족하다.

### 4.5 재료표와 시공 참고

FG254/PDF257에서 ER01 관련 행을 실제 렌더 대조했다.

| 항목 | 표기 품번·설명 | 소유/한계 |
|---|---|---|
|66FU1|Siemens 3NW60101, FUSIBLE25A GL/GG500Vac10x38, 수량3|도면 설계 부품 후보|
|66FU1 하위|WOHNER31954, FUSE BASE32A10.3x38 3P, 수량1|퓨즈 정격과 베이스 정격을 혼동하지 않음|
|66KA1|Siemens3RT2916-1CB00, RC ELEMENT AC24–48V/DC24–70V, 수량1|억제소자 후보|
|66KA1 하위|Siemens3RT2018-1BB41, CONTACTOR7.5kW/IL/DC24V, 수량1|현행 설치/교체 확정 아님. 히터 출력7.5kW라는 뜻 아님|

`Electrical_Can_Decoating_20241118.pdf`:

- PDF36 / 인쇄36/64 / D-PAGE19, DUST ROUTE CONDUIT PIPING(2), 도면번호CANDC-CONS-E019-036: ER01 배관 분기4, Pipe16; 표의 LOC=FN-05, TAG=ER01, 케이블 `1_28=DUS+FN05-ER01`, CV, SIZE4, CORE4.
- PDF51 / 인쇄51/64 / D-PAGE1, CABLE SCHEDULE(1), CANDC-CONS-C001-051: No.1_28, FROM CR → TO LOC FN-05/TAG ER01, ELECTRICAL RESISTANCE, GAC, CV4core/size4, SPARE0, route100→200→210→211→212LB, Adjustment3, LEN115.
- 같은 초안의 PDF36은 ER01 분기를212RAD1 쪽 표에 배치하고 PDF51은 route212LB를 적는다. 두 페이지의 경로 표기를 하나로 합쳐 승인 경로로 확정하지 않는다. 최종 시공도·케이블 양 끝 식별·실제 경로·길이 단위와 실측이 필요하다.
- FN05/M41의 케이블1_27과 ER01의1_28은 별도다. LOC FN-05 표기가 ER01을 팬 모터와 같은 ID로 만드는 근거는 아니다. 승인칸이 비어 있는 first draft를 현장 완료증거로 쓰지 않는다.

## 5 알람과 복구

### 5.1 고유 피드백 감시

LAD1822 / D/0456, 내부 NID49:

| 기능 | 원본 핀·선언 | 해석 |
|---|---|---|
|허가|Wire45 Powerrail→Part21; Wire46 ORef33/RID1→21.operand; Wire47 분기|ON, D/0658 NID49로 결속. 같은 UID33의 타 NID 선언 제외|
|명령|Part22, Wire48 ORef34/RID243; Wire25→Part23|Q5.0 Start ER-01이 참인 경우|
|피드백 불일치|Part23 operand Negated, Wire50 ORef35/RID313; Wire51→LRef28.IN|NOT Inputs.Feedback_ER01|
|타이머|LRef28/RID309 TON, Instance29/RID312; D/0659/0654 NID49|Er_01_Run_Rit DB32, IEC_TIMER|
|시간|Wire30 ORef37/RID311→28.PT; D/0656 LiteralConstant Time32, SV=T_x0023_2S, V=2000|T#2S. S5Time 또는 현장 권장값으로 바꾸지 않음|
|Set|28.Q→Wire38 Part24 SCoil; Wire52 ORef36/RID246|Allarm.ER01_run DB3.X20.1 Set|
|ET|28.ET→Wire40 ORef41, RefId 없음|미결속 끝점. 임의 관찰 DB/시간변수 생성 금지|
|Reset|ON 이후 Part27, Wire56 ORef39/RID13 RESET_ALLARM; Wire26→Part31, Wire63 ORef43/RID246; Wire64→Part32 RCoil, Wire65 ORef44/RID246|ON AND RESET_ALLARM AND ER01_run에서 Reset|

정적 요약: TON.IN=`ON AND Q5.0 AND NOT Feedback_ER01`; PT=T#2S; TON.Q는 고장을 Set한다. ER01이 충분히 가열됐는지 또는 온도허가가 정상인지 별도로 비교하는 알람이 아니다.

### 5.2 유지와 해제의 경계

- 피드백이 돌아와 TON 입력이 거짓이 되어도 고유 고장은 SCoil/RCoil 구조이므로 별도 Reset 경로가 있다. PLC 타이머 정상화와 고장 래치 해제를 같은 사건으로 쓰지 않는다.
- Reset 식에는 `NOT Q5.0` 또는 `Feedback_ER01 정상` 조건이 없다. 원인이 지속될 때 재발하거나 같은 스캔에 Set/Reset이 겹치는 경우의 최종 상태를 이 조사에서 시험하지 않았다.
- ER01_run은 LAD1971에서 M_ER01을 Reset한다. 고장 Reset이 운전요청을 자동 복원한다는 경로는 이번 원본에서 확인하지 못했다.
- 온도허가가 거짓이면 Q5.0 자체가 차단될 수 있어 명령이 참일 때만 작동하는 이 피드백 알람이 발생하지 않을 수 있다. “ER01 알람 없음=온도허가/발열 정상”은 성립하지 않는다.
- 중지한 뒤 보조접점이 계속 참인 상황은 이 고유 식의 직접 감시 범위가 아니다. 다른 알람의 존재는 별도 검토가 필요하며, 접촉기 용착 검출이 완비됐다고 주장하지 않는다.
- HMI 종합표시·알람문구·타임스탬프·경보음 경로까지 직접 결속은 미완료다. Allarm.ER01_run을 현장 정상 Run 비트로 잘못 읽지 않도록 표시 명칭 검토가 필요하다.

### 5.3 복구 완료를 판단할 자료

승인된 조치 후 요청·허가·Q5.0·모듈 출력·66KA1·I6.1·DB13.X6.1·TON·DB3.X20.1·HMI를 같은 시각/프로젝트 기준으로 기록해야 한다. 추가로 발열·공기온도·송풍 조건을 해당 설비의 승인 판정 기준과 대조해야 한다. 현재 자료에는 실제 조치/복구 기록이 없다. 보호설정 변경·인터록 우회·강제출력·재기동 시험을 수행하지 않았다.

## 6 증상별 관찰과 원인 배제 초안

다음은 읽기 전용 관찰을 설계한 항목이다. 실제 조치 지시나 현장 시험 완료 기록이 아니다. 원인 후보는 관찰로 배제하기 전 확정하지 않는다.

| 증상 | 같은 시각에 기록할 위치 | 비교·원인 배제 | 추가 자료/복구 판정 |
|---|---|---|---|
| HMI 요청을 넣어도 가열되지 않음 | HMI Flag 이벤트, DB2.X5.4, M0.0/M0.1, FN05 처리Run, DB3.X20.1, DB13.X22.4, Q5.0 | 요청 미기록/즉시Reset/온도허가차단/출력전달을 나누어 LAD1971과 비교 | HMI 원문 이벤트·CPU 동일성·열 관찰. 버튼 조작을 이번에 시험하지 않음 |
| M_ER01이 바로 사라짐 | LAD1971 Reset3분기, Auto_ON1/Tipo_preset/Tempo_presetting/비상모듈고장, startup 발생 | 직접 Reset·자동정지·DB2.DBW4 초기화를 분리. 이름만으로 HMI 고장 단정 금지 | 호출 시각/OB·CPU 재시작 이력. 원인 해소 전 요청 반복 금지 |
| 요청은1인데 Q5.0은0 | ON, Inputs.177T1_OK, rawI28.4, DB13.X22.4, 호출 조건 | Part30 허가와 I28.4→DB13.X22.4 갱신을 비교. 단순 주소오류로 결론 내리지 않음 | 177T1 모델/설정/트립 상태와 현행 회로 |
| rawI28.4와 처리X22.4가 다름 | I28.4, DB13.X22.4, D/0030 호출·갱신시각 | D/0397 Contact86→Coil125 직접 재매핑 기준. stale·호출차단·외부쓰기 후보 분리 | 현재 프로젝트 전체 cross-reference/온라인 수집. Word28 가정 금지 |
| Q5.0은1인데 I6.1이0 | 출력군24V, 단자11, 66KA1 A1/A2,13–14, E6.1단자22, raw/DB | 출력 논리→코일→보조접점→입력 전달을 분리; TON 지연2초와 비교 | 안전한 계측은 자격자/승인절차 필요. 보호기/코일 임의 교체 금지 |
| ER01_run이 반복 발생 | Q5.0, rawI6.1, 처리X6.1, DB32 상태, Reset 요청/시각 | 실제 응답지연·접점·입력갱신·재Set 조건 분리. 2초를 늘려 증상을 숨기지 않음 | 원본과 현재 DB32 대조·관찰시간 확보 |
| 피드백1·알람0인데 가열 안 됨 | 승인된 열/전류 관찰,3상전력경로,66FU1/주접점/발열체 | 보조접점1은 발열 보증이 아님. 전력·열·송풍을 별도 배제 | 명판/실측/승인 온도·풍량 기준. 본 조사에서 충전부 계측 없음 |
| 온도허가가 회복되자 상태가 바뀜 | rawI28.4/DB13.X22.4, 유지 M_ER01, Q5.0, 출력실물시각 | 허가차단과 요청Reset이 다른 구조임을 비교 | 자동복귀·재통전 실제 시퀀스/안전 절차 확인. 동작을 유도하지 않음 |
| ER01 정지 뒤 VR06 요청도 사라짐 | Q5.0, M5.5, VR06 고장/M_VR_06 | LAD1969는 ER01 출력명령을 읽음. ER01 피드백으로 잘못 대조하지 않음 | VR06 별도 조사·현재 호출순서 |
| HMI와 PLC 관찰이 다름 | HMI DB11.X68.0/68.1, PLC 고유 X6.1/X20.1, 통신시각 | 설정태그/함수Local/실제 호출 미결속 구간을 구별 | 해당 HMI 호출 선언4개·화면객체·통신로그 확보 |

관찰 기록은 관찰자·시각/시간대·설비/위치·값/단위·수집장치·프로젝트/CPU 식별·비교원본·배제결과·승인조치·복구증거를 포함한다. 미측정과0을 구분하고 실제 사용자 기록·사진은 공개 소스에 붙이지 않는다.

## 7 완료 기준과 다음 자료

### 7.1 우선 부족 자료

1. 현재 TIA 전체 프로젝트/CPU와 고정 백업의 동일성, OB 주기·호출순서·간접 쓰기·강제값·리텐션 설정. 자료 수집만으로 운전/변경 권한을 확대하지 않는다.
2. HMI ER01 화면 객체와 dde.cfg 원문, ORef24/657·26/401·33/404·35/406 결속 선언, Flag Set/Reset 이벤트 및 권한/통신시각.
3. ER01 명판, 66FU1/66KA1 실제 품번·배선, 주접점/보조접점·단자22/출력11 대조, 승인 시공도. 재료표만으로 교체부품을 확정하지 않는다.
4. 177T1 명판/설정/히스테리시스/복귀 방식/안전문서, rawI28.4·처리DB13.X22.4 관찰; TC11과177T1의 실제 관계.
5. 승인된 히터 온도/송풍/전력 판정 기준 및 복구 기록. 발열 확인을 접촉기 피드백으로 대신하지 않는다.
6. 시공 초안 PDF36과51의212RAD1/212LB 경로 차이, 케이블1_28 실제 양 끝·경로·길이. 임의 통합하지 않는다.

### 7.2 네 기능의 적용과 기록 보존

| 기능 | ER01 적용 계획 | 이번 상태 |
|---|---|---|
| 도면·래더 나란히 보기 | FG66/122/141/177과 LAD1971/1822/1070/1969를 소유 구분해 연결 | 원본 포인터만 준비. UI 구현/왕복/강조 미검증 |
| 백업 미리보기·선택 복원 | ER01 catalog 키 유지, 타 설비·미지필드·초안 보존 | 구현·실제 저장·재읽기·재열기 미수행 |
| 기록 전후 비교 | 요청/허가/raw/DB/고장/물리열 상태·시각을 분리 | 관찰 설계만 작성, 실제 기록 없음 |
| 관찰 보고서/PDF | 원본버전/해시·관찰시각·미확정을 함께 표시 | 보고서 기능/UI/PDF 출력 미시험 |

통합 시 기존 `note`·`repair_observation`·미지 행/필드·다른 설비·초안·저장 키를 보존해야 한다. `generated_with`와 `saved_with`는 생성/저장 근거이며 현재 CPU·현장 상태의 증명으로 쓰지 않는다. 이번 조사에서는 운영 기록을 만들거나 가져오지 않았다.

### 7.3 검증과 상태

| 항목 | 상태 | 근거/한계 |
|---|---|---|
|documentation|draft_complete_with_gaps|7영역·핵심핀·전기끝점·미확정 작성. 핵심 근거 제한 대조 완료; 사용자 독립 검토 대기|
|static_review|source_crosscheck_performed|원본XML/선언·UID/RefId/NID·Word범위·PDF렌더·SHA/git blob 대조. 설비 통합 검사 아님|
|ui_records|not_run|범위 밖, 미구현/저장 검증을 완료로 표시하지 않음|
|publication|not_published|작업3 조사초안. 통합·릴리스·게시 없음|
|tia_compile|not_performed|TIA 실행 없음|
|live_cpu|not_performed|CPU 접근/비교/운전 없음|
|field_recovery|not_performed|실물확인·보호설정·수리·복구 확인 없음|

수행한 것은 읽기 전용 preflight, XML 선언/핀 검색, 주소범위 대조, PDF 텍스트 추출·원본 렌더 확인, 고정 커밋 파일 무결성 대조다. 매뉴얼 생성기, npm/BC01 회귀, UI/저장/패키지/Netlify, PLC·시뮬레이터 시험은 실행하지 않았다. 문서만 작성한 작업에 현장 검증 완료를 붙이지 않는다.

### 7.4 인계

- 자체검토 정정: FG141/PDF142 개정란은 공란이 아니라 Rev2 17.03.2025다. 확대 렌더에서 이를 확인하여 판본표와 출력경로 설명을 정정했다. A5.0→66/4와 인접 A5.1→21/5의 소유 경계도 분리했다.
- 다음 한 작업: 독립 검토자가 D/0271(요청Reset/177T1 출력허가), D/0456(TON/Set/Reset), D/0397(I28.4→DB13.X22.4), D/0147(DB2.DBW4 초기화)와 FG66/141/177 끝점을 먼저 대조한다.
- HMI4개 미결속·온도허가 복귀/재통전·현행 부품/TC11 대응은 자료 확보 전 미확정으로 유지한다.
- 로컬 2차133 통합/게시 제외, 원본/완료분/중지자산 보존, 실제 PLC·현장·보호값·SEJIN 변경금지 경계를 유지한다. 이 초안을 게시 완료 또는 BC01 동등 기능 완료로 합산하지 않는다.

## 부록 원본 위치와 무결성

아래 해시는 고정 커밋의 바이트 기준이다. 파생 조사 파일과 원본 저장소 파일을 구분한다. 조사 추출은 `extracts/ER01/` 안에만 저장했다. 파일명과 SHA256 전문은 다음 표에 덧붙인다.

- 최종 무결성 대조: 2026-10-11T09:37:33.060451+00:00 UTC. 211개 파일의 작업사본 SHA256과 고정 커밋 git blob SHA256이 모두 같고 바이트도 일치했다.
- 종료시 원본 repo git status --short는 빈 문자열이었다. 원본·버전·대장 변경 없음.
- 전체 IdentXmlPart 선언2938건을 명명/주소범위 탐색에 사용했다. 선언 스캔은 전체 실행코드 완전성 또는 현재 CPU 상태 검증이 아니다.
- 원본 PDF 실제 렌더 검토: Electrical PDF67/123/142/178/257, P&ID PDF1 및 ER01/개정란 확대, 시공참고 PDF36/51. FG141 개정란은 추가 확대 재확인했다.

| 원본 경로 | SHA256 | git blob 바이트 대조 |
|---|---|---|
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | 일치 |
| `all-in-one/registers/equipment-hmi.csv` | `2cdce600aa0138cc5025022e57d9d61a948afb237f70c70e2d11e8300e73286a` | 일치 |
| `all-in-one/registers/equipment-io.csv` | `a7a1f27dc453af25b2b729074cac5266d6dd53c0945a6a1a4afe2dd1e9153b6a` | 일치 |
| `all-in-one/registers/equipment-networks.csv` | `0dcd161bafe7fbc5fd31dd00ed031da3b01e4e46f1154b4c80698bdd766568e0` | 일치 |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | 일치 |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | 일치 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | 일치 |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | 일치 |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | 일치 |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | 일치 |
| `all-in-one/sources/decoded-original/0024-FlgNet.xml` | `a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67` | 일치 |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | 일치 |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | 일치 |
| `all-in-one/sources/decoded-original/0035-IdentXmlPart.xml` | `3a1e3c8c96b30b843c6d75fc7d961972864571095dd972afa94a6b5c8c463b8b` | 일치 |
| `all-in-one/sources/decoded-original/0036-IdentXmlPart.xml` | `d1b7556a1edcf20ecbe76769cd446f7960a5c50c1f464004f07acfe47c856091` | 일치 |
| `all-in-one/sources/decoded-original/0037-IdentXmlPart.xml` | `e92ae321d16be03fa669dc70d4703eb6dcdac4153427518e40cd7514c7bab06e` | 일치 |
| `all-in-one/sources/decoded-original/0038-IdentXmlPart.xml` | `4c0347349822cbc9ac56fa868355893073215fc8fbefa094d1c7a37f236628b7` | 일치 |
| `all-in-one/sources/decoded-original/0039-IdentXmlPart.xml` | `3ae955e5079c7e2f14f98035cffec43763714a9aa62d3b1defe86164aeb43486` | 일치 |
| `all-in-one/sources/decoded-original/0040-IdentXmlPart.xml` | `4aa4f09101f827918ca2af003544aa0de8a70410cc4d69e738f2d6220669f182` | 일치 |
| `all-in-one/sources/decoded-original/0041-IdentXmlPart.xml` | `f6879784dcb83569b01753a2986e4db4ddb411f64580d1e72c22c114dcdaae15` | 일치 |
| `all-in-one/sources/decoded-original/0042-IdentXmlPart.xml` | `39a10a59ac8afcda3d1729f6b07dccea38c00227605c43cac46853fdc3e1b5e2` | 일치 |
| `all-in-one/sources/decoded-original/0043-IdentXmlPart.xml` | `c71c75f0b13763a806cc984f933fd0ec785f77a0fe6915267ebf7648189ddb33` | 일치 |
| `all-in-one/sources/decoded-original/0044-IdentXmlPart.xml` | `80ed7b8be0e4988ac52ac84cbc7e68a29a15755c821d9b0452247d9f362638c2` | 일치 |
| `all-in-one/sources/decoded-original/0045-IdentXmlPart.xml` | `334d3c31a4dc1084cd9e6d870058e32f5e96c17ece69e5fc52038965416a1c79` | 일치 |
| `all-in-one/sources/decoded-original/0046-IdentXmlPart.xml` | `1df29e9d0382743dcf42b287223f63f9880740616318769d8e23fdb8a68a97b1` | 일치 |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | 일치 |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | 일치 |
| `all-in-one/sources/decoded-original/0049-IdentXmlPart.xml` | `d4c49fa00735537ee8cce4baba526b0027e4fe25343074e83de5719cafd1bacc` | 일치 |
| `all-in-one/sources/decoded-original/0050-IdentXmlPart.xml` | `f7ceb0408380d3fad2df3bbf5c663c393b57d1ce156af7a587e14c6b1eb701e3` | 일치 |
| `all-in-one/sources/decoded-original/0051-IdentXmlPart.xml` | `b43718d933537099d8ab3fac88b2012d088d46b69ca1d31ac1570bae4a62cd6c` | 일치 |
| `all-in-one/sources/decoded-original/0052-IdentXmlPart.xml` | `fbd673549a61f7da169e452e2221da4958b29b3e3c1c3699e9cad3d02577500a` | 일치 |
| `all-in-one/sources/decoded-original/0053-IdentXmlPart.xml` | `1d386f98f7bc842e474cf9448dbe37ff3f86775797644252b56d7407e1936c80` | 일치 |
| `all-in-one/sources/decoded-original/0054-IdentXmlPart.xml` | `32d9ad8334dc4c115b04e24702a02051de3155e007de26fba4e32b2d43a1e87f` | 일치 |
| `all-in-one/sources/decoded-original/0055-IdentXmlPart.xml` | `9baf3104be3c8a3457c3eea021f23fbd6a60c665e81a293bd7f2cae52c64be29` | 일치 |
| `all-in-one/sources/decoded-original/0056-IdentXmlPart.xml` | `c5ec45cd232c36d80f80487ec0dd284a876e326ba2286fc722ecc861a400232a` | 일치 |
| `all-in-one/sources/decoded-original/0057-IdentXmlPart.xml` | `1124275ab34e188b042b263d3c4b744abf5637ffd229af642b81a27f00a00c6b` | 일치 |
| `all-in-one/sources/decoded-original/0058-IdentXmlPart.xml` | `84db55242df6a85df73776bfd23bf16cc10e4da35fedca4942f4a43bc4cd1702` | 일치 |
| `all-in-one/sources/decoded-original/0059-IdentXmlPart.xml` | `f02ef8f08f1c7ca7625bdbcf90a2c9365f12654d19e2e526fe8e5b0b742263d0` | 일치 |
| `all-in-one/sources/decoded-original/0060-IdentXmlPart.xml` | `d61344a049baa2ce8a97335cd94e6c1753f8f8b7180d3def74d8631ff2cf21b9` | 일치 |
| `all-in-one/sources/decoded-original/0061-IdentXmlPart.xml` | `0861f9e3686b911262b7b7e108c51fc9fed9cb7080c72bcc4b3aae60750af1c7` | 일치 |
| `all-in-one/sources/decoded-original/0062-IdentXmlPart.xml` | `34f188168dc4fad0d6e2c813028045f37b84025636bcebd8aa1c7ffb4cfd9bcd` | 일치 |
| `all-in-one/sources/decoded-original/0063-IdentXmlPart.xml` | `9dceae18963ead11293cfc3a70c2eac077faa53ebd28e23bb4e84bc3278c5034` | 일치 |
| `all-in-one/sources/decoded-original/0064-IdentXmlPart.xml` | `ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d` | 일치 |
| `all-in-one/sources/decoded-original/0065-IdentXmlPart.xml` | `c99a9960a364084a8e9f007803db72ebaf0ac0ea9126c1b0692da1e5337b33be` | 일치 |
| `all-in-one/sources/decoded-original/0066-IdentXmlPart.xml` | `13ff943033934043bb50d38d95e46706443a12b1eef70471cb0f35d3b0ade402` | 일치 |
| `all-in-one/sources/decoded-original/0067-IdentXmlPart.xml` | `0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628` | 일치 |
| `all-in-one/sources/decoded-original/0068-IdentXmlPart.xml` | `0a71d492e69760390b99f71a75f02ef684e271554b003d5de8bf64a26c64eeba` | 일치 |
| `all-in-one/sources/decoded-original/0069-IdentXmlPart.xml` | `da5203cd92ccadfea2029aafb45a1e6e99443d7edbbcc2fd2f2927482564590d` | 일치 |
| `all-in-one/sources/decoded-original/0070-IdentXmlPart.xml` | `bac2852c85f039a342a0066b3c38df60c572d89b3358fb889b104126d530a447` | 일치 |
| `all-in-one/sources/decoded-original/0071-IdentXmlPart.xml` | `49d01eba491fe39ed64cb9b15719f3445f49979ddc73753cb398628075b0d6c3` | 일치 |
| `all-in-one/sources/decoded-original/0072-IdentXmlPart.xml` | `4528729656e87a902d9be2ab85d2b890b2cb3c68df619b881781eff985eede27` | 일치 |
| `all-in-one/sources/decoded-original/0147-FlgNet.xml` | `386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c` | 일치 |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` | 일치 |
| `all-in-one/sources/decoded-original/0166-FlgNet.xml` | `0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853` | 일치 |
| `all-in-one/sources/decoded-original/0237-FlgNet.xml` | `ad3721660c2f357e76c1a351f7898691271f35c341efe775e5780d749b2c4aa0` | 일치 |
| `all-in-one/sources/decoded-original/0269-FlgNet.xml` | `e9aad7857b267d425d4e23a03e2e7e2ebdbdebb558fef2e08e5be4c2c96c0d37` | 일치 |
| `all-in-one/sources/decoded-original/0271-FlgNet.xml` | `7f913249a7879930d8443291b542374887e8cbbe89b55993a51233446008521b` | 일치 |
| `all-in-one/sources/decoded-original/0355-FlgNet.xml` | `73592d33f8b3a71effeb36f25427c76e931485e7ce31f5c81f144ddae83c4247` | 일치 |
| `all-in-one/sources/decoded-original/0387-FlgNet.xml` | `6d644e7ce02054374d95b3667120dc660795a3af2f02048d7a1ee6a8c9d182fa` | 일치 |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | 일치 |
| `all-in-one/sources/decoded-original/0456-FlgNet.xml` | `6c1e503d84f8806cfc607f67a9a3960ff3bd5d4bc52d6770f1815ff357162077` | 일치 |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` | 일치 |
| `all-in-one/sources/decoded-original/0552-IdentXmlPart.xml` | `d6cb81b6330e182c430061b494463a73065bd9a0945f39e9a15bb8de8d81703d` | 일치 |
| `all-in-one/sources/decoded-original/0553-IdentXmlPart.xml` | `4bf2f2c613e81ee6bd92ac0f21252ea0ce4a1135818fcc404740a914aaae1317` | 일치 |
| `all-in-one/sources/decoded-original/0554-IdentXmlPart.xml` | `4ae3e7d0bca0f78c9e94617abeb70bdd228d85d74bff2224174fa1bb0076e78c` | 일치 |
| `all-in-one/sources/decoded-original/0555-IdentXmlPart.xml` | `46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6` | 일치 |
| `all-in-one/sources/decoded-original/0556-IdentXmlPart.xml` | `065d71114e26c93af180265e0e6d59d2a190af1f2f0581c5265e7f4f67d6e23f` | 일치 |
| `all-in-one/sources/decoded-original/0557-IdentXmlPart.xml` | `536563da118493838d346a6b34b4367bed4185edbe150d79eb2b2042c3950bf0` | 일치 |
| `all-in-one/sources/decoded-original/0558-IdentXmlPart.xml` | `45d49d53b6b41312960bb2a329663e87d8803e28d7832308424a6bf5091e6d1b` | 일치 |
| `all-in-one/sources/decoded-original/0559-IdentXmlPart.xml` | `ec5c6d3f18cbedc2bf695fb1318c1d3a8d2a71c77fbd4ab30d286e2399a289d1` | 일치 |
| `all-in-one/sources/decoded-original/0560-IdentXmlPart.xml` | `847792a7620ed331f784353ef8037be10ba1618b02c8693cd297585d2357089c` | 일치 |
| `all-in-one/sources/decoded-original/0561-IdentXmlPart.xml` | `ac8a4f7b366a262b9d488b5b78aabe8b2dea768753b58993fe7f846989dac0d7` | 일치 |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | 일치 |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | 일치 |
| `all-in-one/sources/decoded-original/0564-IdentXmlPart.xml` | `2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1` | 일치 |
| `all-in-one/sources/decoded-original/0565-IdentXmlPart.xml` | `0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149` | 일치 |
| `all-in-one/sources/decoded-original/0566-IdentXmlPart.xml` | `a1914c7ae085acc1f949a649979824bec8b46fcd78a8055318272a1eb5a45265` | 일치 |
| `all-in-one/sources/decoded-original/0567-IdentXmlPart.xml` | `5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e` | 일치 |
| `all-in-one/sources/decoded-original/0568-IdentXmlPart.xml` | `4ea2540c76f86ab5b17a30c7c9182cc0026bc6b05e605eddcd4af6fc3b919f89` | 일치 |
| `all-in-one/sources/decoded-original/0569-IdentXmlPart.xml` | `2e77bb83cf9a7aecd228dac33fe1c897e1149f2063786f4f4e54c66be618a2c7` | 일치 |
| `all-in-one/sources/decoded-original/0570-IdentXmlPart.xml` | `9fed133006458c3b43b1d5f2c15107a5a86b4fb7cdbaf3743bf88f0e5a105495` | 일치 |
| `all-in-one/sources/decoded-original/0571-IdentXmlPart.xml` | `4a9deeb65a22e497e284fe6d98929e1d201ef5939e4aeca5805b4eb7e007d398` | 일치 |
| `all-in-one/sources/decoded-original/0572-IdentXmlPart.xml` | `5ecd18f84e12d702bb46f759b23994dacfa2d97d50fe51e766ca0cf43f75bb4c` | 일치 |
| `all-in-one/sources/decoded-original/0573-IdentXmlPart.xml` | `a22cc24a974e0c792f32e356a14b277a847e2bb204c91bce01c37d1714ddb56c` | 일치 |
| `all-in-one/sources/decoded-original/0574-IdentXmlPart.xml` | `0773bc969180298193ed6affe56b485bd2141949f4467dcaf33afbb16ee496cf` | 일치 |
| `all-in-one/sources/decoded-original/0575-IdentXmlPart.xml` | `40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06` | 일치 |
| `all-in-one/sources/decoded-original/0576-IdentXmlPart.xml` | `c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe` | 일치 |
| `all-in-one/sources/decoded-original/0577-IdentXmlPart.xml` | `511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47` | 일치 |
| `all-in-one/sources/decoded-original/0578-IdentXmlPart.xml` | `0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b` | 일치 |
| `all-in-one/sources/decoded-original/0579-IdentXmlPart.xml` | `ee35cf525388f2b38399787caef57a978b0bb17216a90e1a90ac4391e0e799fe` | 일치 |
| `all-in-one/sources/decoded-original/0580-IdentXmlPart.xml` | `fa748a6c1890f579d694fd5e561b2304f717da79e5352ca32152cc20e877c6ff` | 일치 |
| `all-in-one/sources/decoded-original/0581-IdentXmlPart.xml` | `5d1d7372935d984aa2d701aa70bdb4555ee1e98d0b0c23806db7bda1ad9134c5` | 일치 |
| `all-in-one/sources/decoded-original/0582-IdentXmlPart.xml` | `41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951` | 일치 |
| `all-in-one/sources/decoded-original/0583-IdentXmlPart.xml` | `0a34a2b7ad17eba6198dbe53d5c6aa8e87710c7436b832b9d39a075074ab58a8` | 일치 |
| `all-in-one/sources/decoded-original/0584-IdentXmlPart.xml` | `3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d` | 일치 |
| `all-in-one/sources/decoded-original/0585-IdentXmlPart.xml` | `e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184` | 일치 |
| `all-in-one/sources/decoded-original/0586-IdentXmlPart.xml` | `f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250` | 일치 |
| `all-in-one/sources/decoded-original/0587-IdentXmlPart.xml` | `bab957ac7c180d9c91b4f904b29e9dbd5812c6ba8f7b9e0c7faf9708605b203e` | 일치 |
| `all-in-one/sources/decoded-original/0588-IdentXmlPart.xml` | `def5646a0d1eacaae81518f0952c4ba8ada5ea38852463a1d463ff439f3d1905` | 일치 |
| `all-in-one/sources/decoded-original/0589-IdentXmlPart.xml` | `846630f3832df93ccdcb0bf86a029546886f8cdba51cd952eed63257ee4540e2` | 일치 |
| `all-in-one/sources/decoded-original/0590-IdentXmlPart.xml` | `baff7271b3db646e8953c31d20b72f7b044b1154b689b15ca0fb38ebb44ad81c` | 일치 |
| `all-in-one/sources/decoded-original/0591-IdentXmlPart.xml` | `2e165c44fc9df852ea3729b3ddb33dc0a74e4f8826676f9c5c5626e1dce033f8` | 일치 |
| `all-in-one/sources/decoded-original/0592-IdentXmlPart.xml` | `d157e3d92df9e4a6ce46567b8611a51b0a10abf4dd7f9c4e613087b2df9583a8` | 일치 |
| `all-in-one/sources/decoded-original/0593-IdentXmlPart.xml` | `504568b5b50bb25a6880e9da724f79438fbb07e7a311a9391681143d713499e9` | 일치 |
| `all-in-one/sources/decoded-original/0594-IdentXmlPart.xml` | `88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd` | 일치 |
| `all-in-one/sources/decoded-original/0595-IdentXmlPart.xml` | `10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52` | 일치 |
| `all-in-one/sources/decoded-original/0596-IdentXmlPart.xml` | `a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0` | 일치 |
| `all-in-one/sources/decoded-original/0597-IdentXmlPart.xml` | `60e292145fe54912a1da7510c8641a4f4c85efe62e1b5206ee3d92794a28de20` | 일치 |
| `all-in-one/sources/decoded-original/0598-IdentXmlPart.xml` | `dc001c9370a691546c5dea79f5a1252d6d0a5564754703018c47df4bcc2522bb` | 일치 |
| `all-in-one/sources/decoded-original/0599-IdentXmlPart.xml` | `32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1` | 일치 |
| `all-in-one/sources/decoded-original/0600-IdentXmlPart.xml` | `20c58ee0383d0b6c275bd2d96abd30af7c5d1f3fff59c7d5034cd758936b57d5` | 일치 |
| `all-in-one/sources/decoded-original/0601-IdentXmlPart.xml` | `04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862` | 일치 |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | 일치 |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | 일치 |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | 일치 |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` | 일치 |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` | 일치 |
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | 일치 |
| `all-in-one/sources/decoded-original/0608-IdentXmlPart.xml` | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | 일치 |
| `all-in-one/sources/decoded-original/0609-IdentXmlPart.xml` | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | 일치 |
| `all-in-one/sources/decoded-original/0610-IdentXmlPart.xml` | `c58d07b1b9707dc8c6c2f06c34ee6142f72238a4cf3f376bee8502d1a9532f9d` | 일치 |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | 일치 |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | 일치 |
| `all-in-one/sources/decoded-original/0613-IdentXmlPart.xml` | `09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb` | 일치 |
| `all-in-one/sources/decoded-original/0614-IdentXmlPart.xml` | `c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294` | 일치 |
| `all-in-one/sources/decoded-original/0615-IdentXmlPart.xml` | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` | 일치 |
| `all-in-one/sources/decoded-original/0616-IdentXmlPart.xml` | `650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d` | 일치 |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | 일치 |
| `all-in-one/sources/decoded-original/0618-IdentXmlPart.xml` | `0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c` | 일치 |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | 일치 |
| `all-in-one/sources/decoded-original/0620-IdentXmlPart.xml` | `da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3` | 일치 |
| `all-in-one/sources/decoded-original/0621-IdentXmlPart.xml` | `a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee` | 일치 |
| `all-in-one/sources/decoded-original/0622-IdentXmlPart.xml` | `f0b997f1246d76cff71de2160eb617caa936e6987bdf43c73f55cdcf77dccdb6` | 일치 |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` | 일치 |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` | 일치 |
| `all-in-one/sources/decoded-original/0625-IdentXmlPart.xml` | `17a9f9bd540bf0a54e9973391fa258d81e567248fd201ae4ff32c367359e69f9` | 일치 |
| `all-in-one/sources/decoded-original/0626-IdentXmlPart.xml` | `a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b` | 일치 |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | 일치 |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | 일치 |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | 일치 |
| `all-in-one/sources/decoded-original/0630-IdentXmlPart.xml` | `1526a89b425470fa6e874bb4a9b6c7bc8e58b740f80d018b9106b6916f402372` | 일치 |
| `all-in-one/sources/decoded-original/0631-IdentXmlPart.xml` | `8e5072374f8ef098de72fbf93965b2a7bb0965c0f803e397daa68588c0c38555` | 일치 |
| `all-in-one/sources/decoded-original/0632-IdentXmlPart.xml` | `fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9` | 일치 |
| `all-in-one/sources/decoded-original/0633-IdentXmlPart.xml` | `9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc` | 일치 |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | 일치 |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | 일치 |
| `all-in-one/sources/decoded-original/0636-IdentXmlPart.xml` | `ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca` | 일치 |
| `all-in-one/sources/decoded-original/0637-IdentXmlPart.xml` | `3fb68f57dbe2a877c4ad5aa1b3316810cf84958f2d13b5b1d7d321e0915271c7` | 일치 |
| `all-in-one/sources/decoded-original/0638-IdentXmlPart.xml` | `878e7b33a4adb054e172843a7519157e39a5e779a1984fc9ec88cc5c465d5d33` | 일치 |
| `all-in-one/sources/decoded-original/0639-IdentXmlPart.xml` | `ae39316c2b618c0783fc1b3889f47d12d8b2a53198c9a7e7b3c40070338c9539` | 일치 |
| `all-in-one/sources/decoded-original/0640-IdentXmlPart.xml` | `2873e2c70eb4ce97c104b00b675c8f800a3ab9621f9d382718428d2d82025379` | 일치 |
| `all-in-one/sources/decoded-original/0641-IdentXmlPart.xml` | `75c1f81d659331b8b62578f766e2f0336276caaf086201fdc383e61c195d01df` | 일치 |
| `all-in-one/sources/decoded-original/0642-IdentXmlPart.xml` | `c922483c261c8ddb98c239a7b4dc3d7f73f9a45261dd5b4d669f39d6918a1c21` | 일치 |
| `all-in-one/sources/decoded-original/0643-IdentXmlPart.xml` | `ce7ff35daa71ee1728f4e7b5ac3234d0a31a3c71e953021e9c1f9a953783b6cb` | 일치 |
| `all-in-one/sources/decoded-original/0644-IdentXmlPart.xml` | `02ab863d23ad70420950737d07cf960a2c27bca1c7c011d18930f5bd2045e272` | 일치 |
| `all-in-one/sources/decoded-original/0645-IdentXmlPart.xml` | `bd0d052cc926d4a9a66ffe9d12de4e5f064231d10a86bd0d3c6e97fd82c4e1d3` | 일치 |
| `all-in-one/sources/decoded-original/0646-IdentXmlPart.xml` | `46f5a677301ad9b0d20a2d9543a2042081ed6db8f0a8fd8d84f25c342c67a8b0` | 일치 |
| `all-in-one/sources/decoded-original/0647-IdentXmlPart.xml` | `ffa253c00b62ccdd999f272d95f613caae3a68792ee5ea9d208253dad53e64be` | 일치 |
| `all-in-one/sources/decoded-original/0648-IdentXmlPart.xml` | `afaa47ae737d9333fe831ffac2b1d1388f108bb6a2b23d03554fa862f7edb454` | 일치 |
| `all-in-one/sources/decoded-original/0649-IdentXmlPart.xml` | `38f59e654ecfbc2066fa1f8beeb9ced952adc405f8a4fcf3ef233e9d5d026576` | 일치 |
| `all-in-one/sources/decoded-original/0650-IdentXmlPart.xml` | `86f53657eb7afb0798da0e215ba226721076c2ab1b25b74eb83e7b3c4b2d8a2d` | 일치 |
| `all-in-one/sources/decoded-original/0651-IdentXmlPart.xml` | `549c09fb14ce6e9734a2ba604c78868647451f24d224ead0d17d209f66428111` | 일치 |
| `all-in-one/sources/decoded-original/0652-IdentXmlPart.xml` | `251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692` | 일치 |
| `all-in-one/sources/decoded-original/0653-IdentXmlPart.xml` | `2df91e2095f16613332cfc59d4c51f8a587183e5e75295a119431b61805c92a6` | 일치 |
| `all-in-one/sources/decoded-original/0654-IdentXmlPart.xml` | `b36294f3aad24be72a052bef61c875ca4695d7e101c385cf55bdadec41d5097e` | 일치 |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | 일치 |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` | 일치 |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | 일치 |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` | 일치 |
| `all-in-one/sources/decoded-original/0659-IdentXmlPart.xml` | `ec881805a45730533bccd780e152afb9c9d7c7c45ba7587538b92239f9cbd9d2` | 일치 |
| `all-in-one/sources/decoded-original/0660-IdentXmlPart.xml` | `0bf4f4c46531f55324602f4f7b1a1e0b9e63df2c6278126f6e5cf1bc9a06509f` | 일치 |
| `all-in-one/sources/decoded-original/0661-IdentXmlPart.xml` | `90672199fee355011f581d3287046894772f3f3b4cb78bbe0dd0d71bd488ac93` | 일치 |
| `all-in-one/sources/decoded-original/0662-IdentXmlPart.xml` | `1838040bfee800fdb3f13b126eaf69a9d178b17cecc0d59ae03e9185216a48a5` | 일치 |
| `all-in-one/sources/decoded-original/0663-IdentXmlPart.xml` | `d3980b88d3cd3e49854439d0778c58ed131bae46a6bc3e65ab70e81f766ac03d` | 일치 |
| `all-in-one/sources/decoded-original/0664-IdentXmlPart.xml` | `68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed` | 일치 |
| `all-in-one/sources/decoded-original/0665-IdentXmlPart.xml` | `50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd` | 일치 |
| `all-in-one/sources/decoded-original/0666-IdentXmlPart.xml` | `19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6` | 일치 |
| `all-in-one/sources/decoded-original/0667-IdentXmlPart.xml` | `ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3` | 일치 |
| `all-in-one/sources/decoded-original/0668-IdentXmlPart.xml` | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` | 일치 |
| `all-in-one/sources/decoded-original/0669-IdentXmlPart.xml` | `754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2` | 일치 |
| `all-in-one/sources/decoded-original/0670-IdentXmlPart.xml` | `e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841` | 일치 |
| `all-in-one/sources/decoded-original/0671-IdentXmlPart.xml` | `26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293` | 일치 |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | 일치 |
| `all-in-one/sources/decoded-original/0673-IdentXmlPart.xml` | `450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58` | 일치 |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | 일치 |
| `all-in-one/sources/decoded-original/0675-IdentXmlPart.xml` | `b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3` | 일치 |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | 일치 |
| `all-in-one/sources/decoded-original/0677-IdentXmlPart.xml` | `69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3` | 일치 |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | 일치 |
| `all-in-one/sources/decoded-original/0679-IdentXmlPart.xml` | `d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56` | 일치 |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | 일치 |
| `all-in-one/sources/decoded-original/0681-IdentXmlPart.xml` | `318e0cf7cd23caadbd3d72d304358dcf978c4b207c04f58fb5b6ce3f31e344e3` | 일치 |
| `all-in-one/sources/decoded-original/0682-IdentXmlPart.xml` | `25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092` | 일치 |
| `all-in-one/sources/decoded-original/0683-IdentXmlPart.xml` | `0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22` | 일치 |
| `all-in-one/sources/decoded-original/0684-IdentXmlPart.xml` | `6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208` | 일치 |
| `all-in-one/sources/decoded-original/0685-IdentXmlPart.xml` | `2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448` | 일치 |
| `all-in-one/sources/decoded-original/0686-IdentXmlPart.xml` | `b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4` | 일치 |
| `all-in-one/sources/decoded-original/0687-IdentXmlPart.xml` | `fa50e7e0262c5d51eeca60e914fce4616fa39a05a3466aa14ec93ba375b04cb1` | 일치 |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | 일치 |
| `all-in-one/sources/decoded-original/0689-IdentXmlPart.xml` | `f0cc6f770c2759b92a9a79f4e289dbfa0ca270d90e0e89496f94a13a8d839d51` | 일치 |
| `all-in-one/sources/decoded-original/0690-IdentXmlPart.xml` | `fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541` | 일치 |
| `all-in-one/sources/decoded-original/0691-IdentXmlPart.xml` | `17cb7d9734d76b39e729e0daf0c89d9bdf74907aab2130c80453fa04e4cea1da` | 일치 |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | 일치 |
| `all-in-one/sources/decoded-original/0693-IdentXmlPart.xml` | `9315ddf43bdfbd7367ab0735a5bbfffcd81ced257d1907c1e2c08ae6b8bfa7ab` | 일치 |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | 일치 |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | 일치 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | 일치 |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | 일치 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | 일치 |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | 일치 |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | 일치 |

자체 정적 확인: XML 핀·선언·주소/상수·문서 구조 26개 검사 통과. 이는 읽기 전용 원문 확인이며 PLC 동작시험/시뮬레이터 실행이 아니다. 독립 검토는 대기한다.


## 전달 전 핵심 근거 제한 대조
2026-10-11 원본0271·0456·0397의 Part/Wire와 FG66/PDF67, FG141/PDF142, FG177/PDF178 실제 렌더를 표본 재확인했다. 인용·검색 대상211파일의 SHA256 재계산도 일치했다. 211은 파일 무결성 범위이며 211개 모든 파일의 의미 검토 완료 수가 아니다. 현재 CPU/현장/통합/게시 검증은 수행하지 않았다.
