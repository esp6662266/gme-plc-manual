# LT01 석회 사일로 레벨 — 고정 원본 독립 조사 초안

## 핵심 확인·상충·누락

- 직접 확인: 원시 Bool `LL_LD01 %I28.5` → 처리 Bool `Inputs.LD-01 Minimo DB13.DBX22.5` → IEC TON `Min_LD_01 DB33`, `T#10S` → 유지알람 `Allarm.LD_01_MIN DB3.DBX5.7`. HMI 설정은 `Allarmi_48`, `DB3,X5.7`이다.
- 저레벨 알람의 정상 Reset 가지는 `ON AND RESET_ALLARM AND LD_01_MIN AND NOT Minimo`다. 원조건 해소와 Reset 요청이 별개다. 추가로 startup only에는 DB3.DBW4 전체를 0으로 쓰는 가지가 있으므로 정상운전 S/R을 유일한 Writer라고 표시하지 않는다.
- P&ID의 LT-01, 전기 FG170의 LD-01 LOW LEVEL, 시공 LT-01은 대응 후보다. 문서·PLC 신호 대응과 현재 실물 동일성은 구별한다. LT라는 이름만으로 연속 레벨 트랜스미터·4–20mA·백분율을 만들지 않는다. 확보 PLC 경로는 Bool이다.
- 소유 구분: LT01 레벨관찰/경보와 부모 LD01 피더 요청·Q3.6, LD01A 진동기, VR06 응답을 합치지 않는다. 확인한 LD01 직접 출력식에는 저레벨 입력/알람 접점이 없다. 공통알람·상위허가의 모든 간접영향까지 없다고 단정하지 않는다.
- 상충·누락: 전기 기기전원 110Vac와 시공 DUS2TB1C AC(220V)는 단자별 결속 미확정이다. 전기의 170FC1과 시공의 68FC1도 같은 장치로 확정하지 않는다. 기종·센서 설치 높이·검출원리·정상 접점극성·현행 CPU·실물·복구는 미확정이다.
- 공유 근거: `LD01-DOTS-DRAFT.md`의 소유 경계·색인·공통 호출을 참고했다. 이번에는 LT01 핵심 선언/Part/Wire/핀·타이머·HMI·실제 PDF 끝점을 원본에서 다시 대조했다. 부모 조사완료를 LT01 완료로 상속하지 않았다. 공통 전체알람 경로는 `SYS-ALARM-DOTS-DRAFT.md`를 후속 색인으로 사용할 수 있으나 이 문서가 그 전체를 독립 검증했다는 뜻은 아니다.

## 1. 설비·자료 기준

| 항목 | 기준·범위 |
|---|---|
| 고유 대상 | catalog_id LT01, 석회 사일로 레벨, sensor/계측, parent LD01, depth1, phase2 |
| 대장 | `docs/equipment-standard/INVENTORY.json` catalog[108]; `all-in-one/registers/equipment.json` equipment[103], 별칭 ll_ld01 / low level / lime level, FG170 |
| 원본 | `gme-research/source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0 |
| 표준 | GME-STD-1.0.0, AGENTS·rollout SKILL·WORK-STANDARD·WORK-ITEM-TEMPLATE·INVENTORY 읽기; BATCH16 지시 우선 |
| 조사 범위 | 신규132개 중 LT01 한 ID의 자체 문서조사. 로컬 통합·공용 대장·코드·버전 변경 없음 |
| 작성·검토 | LT01 조사 작업자 자체 정적검토, 독립 승인 대기. 실제 모델/추론 런타임 증명 미확인 |
| 보존 | 원본 읽기 전용. 중지5자산 지정해시 및 선정49파일의 고정Git blob 내용 일치. 원본 Git 시작/종료 변경0 |

이하 `sources/`와 `registers/`는 원본 `all-in-one/` 아래다. `0161`은 `sources/decoded-original/0161-FlgNet.xml`, 선언 번호는 같은 폴더의 `*-IdentXmlPart.xml`이다. 원문 XML 위치는 NID/UID/RID/핀으로 식별하며 pretty XML 줄번호는 원본 행번호가 아니다.

P&ID `PID_1684n002I.pdf` 실제 p1, 도번1684n002 판I에서 LT-01이 LD-01 사일로 측면에 연결된다. M32 피더·M33 진동기·VR-06/M40은 별도 표기다. 도면의 기본일자는06/04/2011이며 작은 개정표의 상세 변경일은 이번 전체 렌더만으로 재확정하지 않는다. 부모 초안의 날짜를 독립확인 없이 그대로 확대하지 않는다.

| 7영역 | 적용 상태 | 이번 확보 / 남은 경계 |
|---|---|---|
| 설비·자료 | 적용 | 고유ID·부모분리 / 현재 실물 미확정 |
| IO/HMI | 적용 | I28.5·DB13X22.5·DB3X5.7·CSV / 이벤트·현재값 미확인 |
| 제어 | 적용 | 개별 bit전달·호출·S/R·Word쓰기 / 전체 간접영향·최종스캔 미확인 |
| 전기끝점 | 적용 | FG170/177 및 시공2쪽 / 현행 단자·기종 미확인 |
| 알람/복구 | 적용 | TON10초·조건해소Reset / 실제복구 없음 |
| 증상관찰 | 적용 | 비교할 지점·자료 정의 / 실측·조작 없음 |
| 완료/누락 | 적용 | 문서·정적범위 / UI·게시·TIA·CPU·현장 별도 |

## 2. I/O·HMI: 원시·처리·경보·제어요청 분리

| 신호 | 형식/주소 | 원본 선언과 참조 | 의미·경계 |
|---|---|---|---|
| LL_LD01 | Global Bool, Input, %I28.5 | 0627 RID142, SAD Input/SAM None, AO229; NID1 UID95 | 원시 디지털 입력. PIW·아날로그가 아님 |
| Inputs.LD-01 Minimo | Global Bool, DB13.DBX22.5 | 0629 RID149 AO181/BAD4; 0628 RID4 TOD13; NID1 UID131 Write | I28.5의 처리 미러. 원시 주소와 다름 |
| 같은 Minimo 알람읽기 | Global Bool DB13X22.5 | 0573 RID82 AO181/BAD58, 0572 RID58 TOD13; NID3 UID30/34 Read | TON 입력과 Reset 부정접점 |
| Allarm.LD_01_MIN | Global Bool DB3.DBX5.7 | 0573 RID42 AO47/BAD10; 0572 RID10 TOD3; NID3 UID291 S/293 Read/295 R | 유지경보 bit, 레벨의 연속값 아님 |
| Flag.RESET_ALLARM | Global Bool DB2.DBX6.0 | 0573 RID38 AO48/BAD37, 0572 RID37 TOD2; NID3 UID292 | 공통 Reset 요청, 보충/재기동 명령 아님 |
| ON | Global Bool %M0.0 | 0570 RID1 AO0 Memory, NID3 UID289 | 명령허가, 항상 TRUE로 가정하지 않음 |
| Min_LD_01 | Global IEC_TIMER DB33 | 0052 AufDBBlock RID79/TOD33, NID3 UID22 InstanceDB | TON 인스턴스, S5 %T 타이머와 다름 |
| T#10S | Constant Time, 10000 | 0571 RID81 NID3 UID24, CB SV=T_x0023_10S/V10000 | 백업 코드의 지연 상수. 현행 설정·안전한계가 아님 |
| Allarmi_48 | HMI PLC 설정 DB3,X5.7 | hmi_plc_tags.csv 실제505행, ID0015D, Access Name PLC | 알람주소 일치만 확인. 메시지문구/ACK/쓰기권한/실제화면 미확인 |

LT01 고유경로에서 Local 변수를 새로 정의하지 않는다. 관련 DB/입력은 위 Global 선언으로 결속했다. `LD_01_MIN` 문자열은 `0615` RID226에도 있으나 그 선언은 `hours motors`의 Int/AO1152, `0614` DB9 → DB9.DBW144인 주모터 분(minute) 카운터다. DB3X5.7 저레벨 알람과 같은 이름으로 합치지 않는다.

CSV 전체를 LT01/LL_LD01/Minimo 및 경보 주소로 검색해도 원시·처리 bit의 독립 화면 이벤트는 확보하지 못했다. HMI 주소파일은 dde.cfg 설정이지 온라인 현재값이 아니다. LT01 전용 HMI 버튼·레벨백분율·단위·로그·알람문구·ACK 동작을 만들지 않는다.

## 3. 제어 구조·호출·Writer 경계

### 3.1 원시 → 처리 bit

`0397` LAD1070, HMI Inputs, index1/NID1:

- rail W21→Contact94.in. ORef95/RID142→Contact94.operand W92.
- Contact94.out→Coil130.in W134. ORef131/RID149→Coil130.operand W133.
- Contact94와 Coil130에는 Negated가 없다. 따라서 이 가지는 I28.5 값을 DB13X22.5에 반전 없이 개별 bit로 전달한다. 전기 접점의 실제 정상극성까지 증명한 것은 아니다.
- 같은 네트워크의 IW4→DB13W4 Move35(원시 모터응답 묶음)는 LT01 신호의 직접 전달이 아니다. LT01을 그 Word의 bit로 설명하지 않는다. 주변 IW/DB Word와 개별 bit전달을 구별한다.

### 3.2 상위 호출의 조건

`0030` LAD1613, main index2/NID19: CRef21→23→25의 W32/W33 ENO 연쇄 후 W42→NOT Contact37, ORef45/RID140 W44→W43 CRef28.en. CodeBlock29/RID135는 `0688` HMI Inputs FC15, NID19 UID29다. `0692` RID140은 Global Simulation(1), Memory AO1440(%M180.0)다. 이는 물리입력 처리 호출의 조건이 있음을 보여 주는 읽기전용 경계이며 해당 정지 기능의 작성/생성/실행/행동시험을 하지 않았다. 현재 활성·주기·최종값은 미확인이다.

`0031` LAD1619, main index8/NID6: rail W284→Contact282(ON ORef271/RID52, W280)→W283으로 CRef267.en 등 병렬 호출. CodeBlock277/RID61은 `0688` Allarms2 FC5, NID6 UID277이다. Allarms2 안의 LT01 알람이 무조건 매스캔 실행된다고 단정하지 않는다.

### 3.3 다른 Writer와 상위 설비 소유

- `0148` LAD403, startup only index3, network-map 추정 NID=null. `0563`의 선택 선언은 NID3 UID290/RID28, Word AO32/BAD23→`0562` Allarm DB3이다. ON Contact329.out W330→Move250.en, eno W306→Move253.en, eno W309→Move256.en. Int0 ORef289/RID54(`0048`, NID3 UID289) W310→Move256.in; W311→ORef290가 DB3.DBW4를 0으로 쓴다. DB3X5.7이 그 Word 범위에 포함된다. startup 의미·실제 실행시점·다른 최종 Writer는 별도이며, 이것을 정상운전 Reset 버튼과 같게 설명하지 않는다. network-map NID null을 임의3으로 수정하지 않았다.
- `0635` GlobalAccess RID366, Inputs.Minimo AO181/BAD5, NID18 UID37 Write가 추가 선언되어 있다. 정지된 기능 자료의 다른 Writer 존재만 확인했다. 현재 CPU에서 실행된다고 추정하지 않았고 해당 기능을 분석확장·실행·시험하지 않았다.
- 부모 `0259` LAD1958/motors1 index29/NID29를 직접 대조했다. ON Contact863→M_LD01 Contact871(ORef847/RID143, W858)→InspectionLS Contact873(ORef848/RID267,W859)→Coil841(W874), Q3.6 ORef849/RID145(W861)다. 선언0604/0603은 요청 DB2X2.0, 도어 DB13X22.6; 0602는 Q3.6이다. 저레벨 입력/알람은 이 출력가지에 없다.
- 같은 부모 네트워크 RCoil836은 ON AND [LD_01_FAULT OR (NOT VR06 Run AND NOT UNDER TESTING)]으로 요청을 Reset한다. 저레벨 알람을 주모터 FAULT(DB3X2.0)와 합치지 않는다. 부모의 모터운전·진동·VR06 제어 전체를 LT01 소유로 옮기지 않는다. 전체 공통알람의 간접 정지영향은 이 좁은 검토로 부정할 수 없다.

## 4. 전기 전달 경로와 실제 PDF 끝점

직접 렌더확인한 원본은 전기2쪽, 시공2쪽, P&ID1쪽으로 총5페이지다. 아래는 FG와 PDF실제쪽을 각각 기록했다. PDF 파일명 Rev2를 모든 시트의 개정값으로 쓰지 않는다.

| 원본/실제 페이지 | 제목·개정란 | 확인 끝점 / 경계 |
|---|---|---|
| Electrical_Rev2.pdf p171 / FG170 | LIME LEVEL INDICATOR LD-01; DATA27.05.2024, 별도 개정행 표시 없음 | 저레벨·도어·셀렉터 별도 회로 |
| 같은 PDF p178 / FG177 | DIGITAL INPUT/OUTPUT MODULE; DATA27.05.2024, 별도 개정행 표시 없음 | CPU515 MOD4 Rack3, E28.5 수신 |
| Electrical_Can_Decoating_20241118.pdf p36/64 | CANDC-CONS-E019-036; DUST ROUTE CONDUIT PIPING(2), Rev1 24.11.11 first draft design | DUS2TB1→LT-01·LD-01·68FC1·PB14 분리. CHECKED/APPROVED 공란 |
| 같은 PDF p60/64 | CANDC-CONS-C010-060; CABLE SCHEDULE(9), Rev1 24.11.11 first draft design | 신호/전원 케이블표. 승인준공·실측으로 승격하지 않음 |
| PID_1684n002I.pdf p1 | 도번1684n002, 판I, P&I | LD-01/LT-01 위치와 관련 구동기 분리. 실물동일성 미확정 |

### 4.1 전원과 신호는 다른 회로

1. 기기전원: FG170 상단 `110Vac152.8`(169/9) → X3:109, 2A F 5×20 → 선170.1 → LD-01 기기전원. 반대측 LD-01→X3:110→`0Vac9.9`(81/9). 내부 기기 단자번호·명판·검출방식은 도면에서 확보하지 못했다.
2. 디지털 응답: `+24Vdc152.5`(168/9) → X3:111, 2A F 5×20 → 선170.2 → LD-01의 별도 접점 → X3:112 → E28.5(177/5).
3. 수신 끝점: FG177 E28.5 상단 역참조170/2 → X22:4008 → CPU515/MOD4/Rack3의 단자6, 설명 LOW LEVEL LD-01. 도면의 E표기와 PLC 선언 I28.5의 대응을 확인했다. 이 CPU515 텍스트만으로 현재 설치CPU 모델/랙상태를 확정하지 않는다.
4. 신호접점 내부 번호·정상 NO/NC·무전원 fail-safe·센서작동레벨을 이름으로 추정하지 않는다. 110Vac 기기전원과 24V 디지털접점을 같은 전압으로 설명하지 않는다.
5. 같은 시트 E28.6은 도어170FC1→X3:114→X22:4009→단자7이며, E28.7은170SA1/PB14→X3:116→X22:4010→단자8이다. LT01과 별도 채널이고 저레벨센서의 보조핀으로 복제하지 않는다.

### 4.2 시공 케이블의 결속 한계

p60 표10_13 `=DUS+LD01-LT01A`: FROM LD-01/DUS2TB1 → TO LD-01/LT-01, DC, CVV, 2C, SIZE1.0, SPARE0, route E420, Adjustment3, LEN3. p36은 DUS2TB1 분기2 LT-01와 대응하는 설계 경로를 그린다. LEN3에 실측·단위를 새로 부여하지 않는다.

표10_16 `=DUS+LD01-LD01A`: DUS2TB1→LD-01, AC, CVV, 3G/1.0, E410, Adjustment3/LEN4다. 케이블 이름의 LD01A만 보고 M33 진동기 케이블이라고 합치지 않는다. p36의 분기1 LD-01와 계장전원 후보로 읽는다. 표10_1은 CR→DUS2TB1의 DC/CVV/16G/1.0/SPARE7, LT01|68FC1|PB14 설명이며, 표10_3은 AC(220V)/CVV/4G/4.0이다.

이 표에는 X3:111/112와 X22:4008까지의 코어/터미널 대응이 없으므로 전기회로와 시공도를 단자대조 완료로 표시하지 않는다. AC(220V) 가지가 FG170의110Vac를 대체한다고 가정할 수 없다. 현행 준공단자표·케이블 코어·센서명판이 필요하다. 시공68FC1과 전기170FC1 차이는 별도 도어관련 식별누락이며 LT01 자체 신호로 병합하지 않는다.

## 5. 저레벨 알람·Reset·복구

`0161` LAD1228, Allarms2 index3/NID3. Part/Wire는 원본 연결을 독립 대조했다.

| 구간 | Part/ORef/Wire | 해석 |
|---|---|---|
| 허가 | rail W316→Contact306, ORef289/RID1 W296 | ON |
| 검출 | Contact306.out W307→Contact308; ORef30/RID82 W29; W27→LRef21.IN | ON AND 처리Minimo. 반전 아님 |
| 지연 | LRef21/RID78 TON, Instance22/RID79 DB33; ORef24/RID81 W23→PT | Time T#10S/V10000. S5Time·모터2초와 다름 |
| Set | TON21.Q W25→SCoil282; W299→ORef291/RID42 | DB3X5.7 유지경보 Set |
| ET | TON21.ET W26→ORef28 | RefId 없음. ET 저장주소·표시경로 미결속 |
| Reset 요청 | ON306.out→Contact310, ORef292/RID38 W300; W311→Contact312, ORef293/RID42 W301 | ON AND RESET_ALLARM AND 현재알람 |
| 조건해소 | W31→Contact314, operand Negated, ORef34/RID82 W33 | NOT 처리Minimo |
| Reset | Contact314.out W32→RCoil288, ORef295/RID42 W304 | 위 조건 만족 시 알람 R |

LRef21의 EN=false/ENO=false 및 `0574` TON 인터페이스 IN Bool/PT Time/Q Bool/ET Time을 구분했다. 독립 en/eno 체인이 없는 IEC 타이머를 다른 S5 지연 코일로 설명하지 않는다. 실제 경과10초·스캔 지연·잔존 상태·현재 프로젝트 동작은 시험하지 않았다.

정상 경보가지에서 Minimo가0으로 바뀌어도 SCoil로 유지된 경보가 자동으로 사라진다고 쓰지 않는다. Reset 요청만 있고 원조건이1이면 해당 R가지가 성립하지 않는다. 다만 startup Word0 및 다른 Writer 가능성이 있으므로 위 설명은 이 정상 S/R 네트워크 범위다. 화면 ACK와 PLC RESET_ALLARM, 알람 bit0과 원인제거, 보충과 재요청, 실제 운전/복구는 서로 다른 단계다.

## 6. 증상별 관찰·자료수집

아래는 승인된 안전절차에 따른 관찰지점 정의이며 활선작업·강제입력·우회·시뮬레이터·설정변경 지시가 아니다.

| 증상 | 함께 기록할 지점 | 대조·미확정 |
|---|---|---|
| 석회부족으로 보이는데 경보 없음 | 관찰된 내용물 상태·센서위치, I28.5, DB13X22.5, ON, TON DB33/Q, DB3X5.7, 시각 | 실제부족/센서동작/접점·전원/전달호출/지연/다른쓰기 구분. 내용물 관찰만으로 센서고장 확정금지 |
| 경보 지속 또는 순간 반복 | 원시와 처리 bit의 같은시각 변화, DB33 Q/ET 접근가능 여부, DB3X5.7 | ET 목적지 미결속 유지. 공정 흔들림/접점/통신을 자료없이 단정하지 않음 |
| Reset 후 그대로 | RESET_ALLARM, Minimo, ON, 경보, 실제 화면 ACK 경로 | NOT Minimo가 필요한 R가지와 실제 원인제거를 구분 |
| HMI만 다름 | Allarmi_48/DB3X5.7, HMI연결·통신시각·화면 이벤트 | CSV 주소일치는 이벤트 확인 아님 |
| 레벨값과 피더운전이 다름 | DB13X22.5/DB3X5.7와 별도 DB2X2.0·DB13X22.6·Q3.6, 상위공통허가 | LT01이 직접 피더출력을 차단한다는 가정부터 배제 |
| 전원/케이블 의심 | FG170 X3:109/110와111/112, FG177 X22:4008/단자6, DUS2TB1/LT01 명판·승인단자표 | 110Vac 전원과24V 신호 분리. 220V표기를 대체전원 지시로 사용금지 |

관찰 기록 필수: 관찰자·시각/시간대·위치·값/단위·수집장치·온라인 프로젝트식별·원본 비교·원인배제·승인조치·재발없음·실물복구 근거. 실제 운영기록이나 사진·SEJIN 자료를 복사하지 않았다.

## 7. 완료·누락·인계

### 자료별 다음 확인

1. LT01/LD01 레벨기기 명판·설치위치·검출원리·승인된 센서 데이터시트와 준공도: P&ID LT01/전기 LD01/시공 LT01의 현재 동일성, 정상극성과 동작기준 결속. 새로운 자료가 없으면 같은 실물보류를 반복조사하지 않는다.
2. X3/X22/DUS2TB1 코어·단자표와 전원계통: 110Vac·24Vdc·시공 AC220V의 서로 다른 가지를 확정. 안전한 현장 접근과 측정은 자격자·승인절차가 필요하다.
3. 현행 TIA/CPU 읽기전용 교차참조와 호출·간접쓰기 자료: 고정백업 이후 주소/Writer/초기화/호출 차이 확인. 이번에는 TIA컴파일·온라인·다운로드·강제·실행시험을 하지 않았다.
4. HMI 프로젝트의 Allarmi_48 메시지·이벤트·ACK/RESET/권한·통신시각: 설정주소와 실제표시 연결. 실제 Reset/보충/재기동/복구 여부는 별도 기록한다.
5. 공통 경보의 상위 운전영향이 필요하면 SYS-ALARM 근거와 현행 프로젝트를 연결해 범위를 한정한다. LT01 직접경로를 넘는 모든 논리를 이번에 의미검토했다고 주장하지 않는다.

| 네 기능 | 적용 방향 | 이번 상태 |
|---|---|---|
| 도면·래더 비교 | FG170/177 ↔ LAD1070/1228, 원시·처리·경보 구분 | Markdown 근거, 제품 UI 미구현/미검증 |
| 백업·선택 복원 | LT01 고유키·부모키·note/repair_observation·미지필드 보존 | 미수행 |
| 기록 전후 비교 | 동일시각 원시/처리/경보/화면/실물 | 관찰 양식 정의, 기능시험 미수행 |
| 보고서/PDF | 이 원본근거/미확정/끝점 전달 | MD 초안만, 제품 PDF출력 미검증 |

| 상태 | 판정 |
|---|---|
| documentation | draft_ready, LT01 한 ID의 자체 조사 초안 |
| static_review | self_review_completed, 6개 LAD의 명시된 부분·5원본 PDF페이지; 독립검토 대기 |
| ui_records | not_run |
| publication | not_published, 이 작업에서 로컬통합/게시 없음 |
| tia_compile / live_cpu / field_recovery | 모두 not_performed |

자가정적 검사24개 통과는 XML 연결/텍스트·해시·보존 단언이다. 기능시험이나 전체 원본 의미검증이 아니다. 기존18불일치/1060확인대기/577설계시험 상태를 변경하지 않았다. 시뮬레이터 작성·수정·생성·실행·행동시험0, 소스 build/test/generator 실행0, PLC/현장/보호값/SEJIN 변경0, 재위임0이다. 완료 커밋은 없으며 쓰기는 이 MD와 `extracts/LT01/`에 한정했다.

### 의미검토 범위

| XML | LAD / index / NID | 독립검토한 부분 |
|---|---|---|
|0397|1070 / 1 / 1|I28.5 개별 전달 Contact94/Coil130, Word와 분리|
|0161|1228 / 3 / 3|LT01 TON·Set·Reset·ET 미결속 전체 핵심|
|0259|1958 / 29 / 29|부모 요청Reset·직접출력, 레벨소유와 구분|
|0030|1613 / 2 / 19|HMI Inputs 호출조건·ENO 연쇄|
|0031|1619 / 8 / 6|Allarms2 공통 ON 호출|
|0148|403 / 3 / null(선택선언3)|startup DB3W4=0 Writer·앞단ENO|

부록의49파일은 바이트 대조수, 위6 LAD는 선택 의미검토수,5페이지는 시각검토수,24는 정적단언수다. 검색한 선언파일 전체를 의미검토완료로 합산하지 않는다. 추출JSON/pretty XML/렌더는 원본 대체물이 아니다.

## 부록 A. 선정 원본 전체 SHA-256·고정 Git blob 내용 일치표

아래 모든 파일의 로컬 SHA-256과 고정커밋 Git blob을 읽어 계산한 SHA-256이 일치한다. Git blob 객체ID와 재계산값은 `extracts/LT01/source-hashes.json`에 함께 기록했다. 중지5자산은 해시보존만 수행했다. 이 표에 포함된 선언/공통자료는 명시한 선택 범위만 의미검토했으며 파일전체 검증이 아니다.

| 원본 상대경로 | SHA-256 | 고정 Git blob 내용 일치 |
|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | 예 |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | 예 |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | 예 |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | 예 |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | 예 |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | 예 |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | 예 |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | 예 |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | 예 |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | 예 |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | 예 |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | 예 |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | 예 |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | 예 |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | 예 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | 예 |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | 예 |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | 예 |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | 예 |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | 예 |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | 예 |
| `all-in-one/sources/decoded-original/0052-IdentXmlPart.xml` | `fbd673549a61f7da169e452e2221da4958b29b3e3c1c3699e9cad3d02577500a` | 예 |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` | 예 |
| `all-in-one/sources/decoded-original/0161-FlgNet.xml` | `3c4804a56f612d0e1884e29c892c21f681698dc1ccb40c6c53ac88fcb0f63a4c` | 예 |
| `all-in-one/sources/decoded-original/0259-FlgNet.xml` | `872a7149ef118f82addce8b038d42418f532c065f2191018d85aed93406dd8b5` | 예 |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | 예 |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | 예 |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | 예 |
| `all-in-one/sources/decoded-original/0570-IdentXmlPart.xml` | `9fed133006458c3b43b1d5f2c15107a5a86b4fb7cdbaf3743bf88f0e5a105495` | 예 |
| `all-in-one/sources/decoded-original/0571-IdentXmlPart.xml` | `4a9deeb65a22e497e284fe6d98929e1d201ef5939e4aeca5805b4eb7e007d398` | 예 |
| `all-in-one/sources/decoded-original/0572-IdentXmlPart.xml` | `5ecd18f84e12d702bb46f759b23994dacfa2d97d50fe51e766ca0cf43f75bb4c` | 예 |
| `all-in-one/sources/decoded-original/0573-IdentXmlPart.xml` | `a22cc24a974e0c792f32e356a14b277a847e2bb204c91bce01c37d1714ddb56c` | 예 |
| `all-in-one/sources/decoded-original/0574-IdentXmlPart.xml` | `0773bc969180298193ed6affe56b485bd2141949f4467dcaf33afbb16ee496cf` | 예 |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | 예 |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | 예 |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | 예 |
| `all-in-one/sources/decoded-original/0614-IdentXmlPart.xml` | `c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294` | 예 |
| `all-in-one/sources/decoded-original/0615-IdentXmlPart.xml` | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` | 예 |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | 예 |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | 예 |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | 예 |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | 예 |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | 예 |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | 예 |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | 예 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | 예 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | 예 |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | 예 |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | 예 |

## 부록 B. 실제 작업 시각(UTC)

- 2026-10-11T12:38:07.333966+00:00: direct_review_started
- 2026-10-11T12:40:13.981007+00:00: direct_XML_PDF_checks_and_hashes_completed
- 2026-10-11T12:43:31.754155+00:00: draft_written

다음 작업은 부모의 독립 검토 및 사용자 전달이다. 실물보류는 새 승인자료가 확보될 때만 재개한다.
