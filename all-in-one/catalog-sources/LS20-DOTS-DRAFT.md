# LS20 — MV03 닫힘 리미트 고유 원본 조사 초안

- 작업: phase2 / catalog_id LS20, component, 부모 MV03, priority_key 없음. 부모와 별도 ID이며 부모 완료를 상속하지 않는다.
- 기준: GME-STD-1.0.0, source-mv06 고정 Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 조사일 2026-10-11 UTC. 실행 모델/추론 설정 런타임 증명 미확인.
- 허용 산출물: 이 MD와 extracts/LS20만. 원본·공통 파일·PLC·현장·보호값·SEJIN 변경 없음. 시뮬레이터 생성·수정·실행·행동시험 없음. 0403은 보존 원문의 다른 쓰기를 정적으로 읽은 것뿐이다.
- MV03/ZT04 초안은 탐색 색인·공통 근거 연결로 사용했고 부모 전체 제어·모터·압력·알람을 반복 조사하지 않았다. 고유 판단은 아래 원본으로 다시 대조했다.

## 핵심 결과

1. FG39/실제 PDF40은 LS-20을 LIMIT SWITCH VALVE CLOSING, NC11/12로 그리고 X1/92→39.4→LS20→X1/93→E7.6로 연결한다. FG123/실제 PDF124는 E7.6을 MOD9 단자37, LIMIT SWITCH LS-20으로 확인한다. P&ID의 MV03/M17/LS19/LS20/ZT04 묶음과 부합한다.
2. PLC 원시는 MV03_Close I7.6, 가공값은 Inputs.MV03 Close DB13.X7.6이다. 0397은 raw를 NOT하여 가공값에 쓴다. NC 접점 그림·원시값·가공값·실제 닫힘 정상극성을 하나로 동일시하지 않는다.
3. DB13.X7.6에는 0397 Word6 복사, 0397 개별 반전 Coil, 보존 0403의 다른 Coil 쓰기가 있다. 가공값의 유일 작성자가 하드웨어 입력이라는 단정은 불가하다.
4. 닫힘 가공값은 부모 Q2.0 차단, 수동 닫힘 및 버너기동 닫힘 요청 해제, 교정 조건, 엔코더 gate, 별도 CONT_S LMNR_LS 반전에 관여한다. 어느 것도 LS20 독립 구동출력이나 독립 알람이 아니다.
5. HMI MV_03\\LimitSwitchClose는 DB11.X22.4이며 raw/가공주소와 다르다. 0369 호출의 해당 입력·출력 ORef는 이번 선언 탐색에서 미결속이므로 실제 표시까지 완결된 경로라고 하지 않는다.

## 1. 설비·자료 기준 — 적용, 현장 식별 미확정

대장 INVENTORY.json catalog[231]은 LS20/밸브 위치 리미트 스위치/component/MV03/depth1/phase2/planned/baseline/not_assessed다. TASK3-BATCH23-SCOPE 및 겹침 검토는 parent_child_separate, alias ls-20/ls.20, physical_identity_verified=false로 분류한다. 같은 이름의 다른 LS와 병합하지 않는다.

| 원본 | 실제 위치·판본 | 고유 판단·경계 |
|---|---|---|
| all-in-one/sources/PID_1684n002I.pdf | PDF1, 도면1684n002, Apex I, 기본06/04/2011; I 15/01/2013, H 01/08/2012 | MV03 Overflow valve의 M17과 LS19/20, ZT04를 실제 렌더 확인. H의 MV03 COMMAND INSTRUMENT 변경은 현 설치상태 증명이 아님 |
| all-in-one/sources/Electrical_Rev2.pdf | FG39/PDF40, MOTORIZED VALVE MV-03, 27.05.2024, 개정란 공란 | LS20 닫힘 센서의 직접 단자·입력 식별. 파일명 Rev2를 모든 쪽에 복사하지 않음 |
| 같은 PDF | FG123/PDF124, DIGITAL INPUT MODULE, 기본27.05.2024, **Rev2 17.03.2025** | MOD9/단자37/E7.6/LS20, 페이지 개정 독립 확인 |
| Electrical_Can_Decoating_20241118.pdf | PDF56/64, CANDC-CONS-C006-056, D-PAGE6; Rev1 24.11.11 first draft design | 공유함 trunk와 LS20 branch는 설계 케이블표. 준공·실물 검사 아님 |

LS19는 열림 종단, LS20은 닫힘 종단, ZT04는 엔코더 위치 측정이다. I2.5 접촉기 닫힘 응답, Q2.0 닫힘 명령, M17 모터, LS20 종단 접점은 서로 다른 소유/의미다. 제조사·모델·설치 캠·기계 동작점·현행 교체 부품은 미확정이다. 부모 모터 정격 상충 및 압력센서 상충은 MV03 초안을 참조하며 LS20 규격으로 복사하지 않는다.

## 2. I/O·HMI — 적용, 원시·가공·기억/요청 분리

이하 NNNN은 all-in-one/sources/decoded-original/NNNN-FlgNet.xml, 선언 파일은 NNNN-IdentXmlPart.xml이다. 주소는 SSD AO 비트 오프셋과 관련 DepDBBlock TOD를 결속한 고정 백업 주소이며 현재 CPU 검증이 아니다.

| 층 | 원문 선언·주소 | 고유 의미 |
|---|---|---|
| 실제 입력 | 0627 SimpleAccess RID154, NID1 UID152, Bool SAD Input AO62 = I7.6, MV03_Close | 0397 Contact149 operand ORef152/W155 |
| 가공 입력 | 0629 Global RID155, NID1 UID153 Write, Bool AO62 BAD4; 0628 DepDBBlock RID4 Inputs TOD13 = DB13.X7.6 | 0397 Not150 뒤 Coil151의 쓰기. raw와 반대 |
| 부모 소비 선언 | 0619 Global RID176, NID4 UID26/34/43 및 NID13 UID30, BAD168; 0618 RID168 Inputs TOD13 | 동일 DB13.X7.6, 문맥별 사용은 아래 표 |
| 엔코더 소비 | 0676 Global RID446 NID32 UID22, BAD445; 0674 RID445 Inputs TOD13 | 0514의 NOT 가공 Close, ZT04 측정값과 다른 Bool |
| PID 소비 | 0668 Global RID128 NID12 UID533 AO62 BAD118 | 0479 NOT Contact591→CONT_S LMNR_LS |
| 다른 쓰기 | 0635 Global RID238 NID2 UID523 Write AO62 BAD5; 0634 RID5 Inputs TOD13 | 0403 별도 Coil501, 보존 원문만 정적 대조 |
| 수동 요청 | 0619 RID41 Flag.M_MV03_CLOSE AO80 = DB2.X10.0 | LS20 기억값이 아닌 부모 수동 명령 요청, RCoil369에서 해제 가능 |
| 버너 요청 | 0617 SimpleAccess RID187 Close MV03 for Burner Startup Memory AO1445 = M180.5 | LS20 센서 래치가 아닌 다른 기능의 요청, RCoil46에서 해제 |
| HMI 표시 설정 | hmi_plc_tags.csv MV_03\\LimitSwitchClose, DB11,X22.4, ID0031B | dde.cfg 설정; DB13.X7.6/I7.6과 별도 주소 |

LS20 전용 MEM_CLOSE 또는 독립 retentive 위치 기억 선언은 이번 정확명/관련 MV03 선언 검색에서 확보하지 못했다. 부모 요청 비트나 DB11 HMI 표시를 LS20의 물리 접점 또는 독립 기억으로 바꾸지 않는다.

### HMI 미결속 경계

0369/LAD1191 hmi mv03 CRef22의 Limiti_Switch_Close는 W57/ORef34/RID686, Limit_Switch_Close_HMI는 W65/ORef42/RID452다. 원본 철자를 보존한다. 동일 RID+UID 선언이 확인되지 않아 NID/주소 결속을 완료하지 못했다. DB11.X22.4 설정의 존재만으로 ORef42와 연결하거나 HMI 버튼/스크립트 쓰기가 있다고 단정하지 않는다. 입력과 출력 핀의 정확 연결, 현재 HMI 프로젝트·이벤트/갱신자료가 필요하다.

XML 695개에서 경계식 LS[ _.-]?20 정확명 검색 0개, HMI CSV 같은 검색 0개다. 소프트웨어는 MV03_Close/Inputs.MV03 Close 이름을 사용한다. 정확명 0건은 실물/간접주소가 없다는 뜻이 아니다. 검색 범위와 직접 쓰기 선언 목록은 extracts/LS20/search.json에 기록했다.

## 3. 제어 구조 — 적용, 고유 위치 가지와 다른 쓰기

### 3.1 raw 수집과 호출 경계

0397/LAD1070 hmi inputs NID1:

- W21 powerrail→Contact149.in, operand W155/ORef152/RID154=raw I7.6.
- Contact149.out W156→**Not150.in**, Not150.out W157→일반 Coil151.in, operand W158/ORef153/RID155=DB13.X7.6. S/R 기억 Coil이 아니다.
- 같은 네트워크 Move42.en도 W21. in W52/ORef45, 0627 RID13 Tag_171 Input Word AO48=IW6. out1 W54/ORef46, 0629 RID14 Word AO48 BAD4→0628 RID4 DB13.DBW6. 이 Word는 DB13 byte6/7을 포함하여 X7.6과 겹친다. Move42 DisableENO=true와 W53 eno 연결은 그대로 보존한다. 개별 반전과 Word복사를 구분하며 현재 실행·최종값 우선순위는 추정하지 않는다.
- 0030/LAD1613 main NID19 Contact37는 operand Negated, W44/ORef45=0692 RID140 Simulation(1), Memory AO1440=M180.0. W42는 선행 CRef25.eno에서 들어오고 W43은 hmi inputs CRef28.en으로 간다. 부모 색인에서 재사용한 호출 명칭의 현재 프로젝트 실행 여부는 미확정이다. 어떤 모드도 실행하거나 변경하지 않았다.

### 3.2 LS20 가공 Close의 소비 위치

| 네트워크·소유 | 선언/Part/Wire/ORef/핀 | 고유 영향·해석 경계 |
|---|---|---|
| 0345/LAD1706 NID4, MV03 출력 | 0619 RID176 ORef34/W33→NOT Contact541. OR53.out W55→541.in, out W32→Coil407, operand W486/ORef438=0617 RID48 Output AO16 Q2.0 | 부모 닫힘 명령의 마지막 위치 차단. 전체 모드·요청 식은 MV03 초안 공유. LS20 출력은 없음 |
| 같은 네트워크, 수동 요청 해제 | ORef26/W25→정접점499, W24→OR365.in1; Open요청/Auto의 다른 OR 입력도 존재; W40→RCoil369; W452/ORef417=0619 RID41 | ON489/491 조건 아래 Close OR 수동Open OR Auto로 수동Close 요청 해제. 센서가 자체 래치를 Reset하는 구조 아님 |
| 같은 네트워크, 버너기동 요청 해제 | ORef43/W41→정접점42; W48→RCoil46; W49/ORef50=0617 RID187 M180.5 | ON489/491 조건 아래 기동닫힘 요청 Reset. LS20 전용 알람 Reset이 아님 |
| 0353/LAD1707 NID13, 교정 | 0619 RID176 ORef30/W29→Contact26, W28 선행 Reset 요청 Contact22; W33→Move32.en | 요청과 처리Close의 조건. Move32 DisableENO=true와 후속 ENO, NewCountValue/SetCountValue 경계는 ZT04 초안 참조; 현장 교정 성공 증명 아님 |
| 0514/LAD1764 NID32, 엔코더 관리 | 0676 RID446 ORef22/W21→NOT Contact1219; EM_OK1217.out W1218→1219.in; W1220→SW_GATE2 Coil1129.in 및 Add1134.en | NOT 처리Close를 엔코더 gate/산술 허가에 사용. EM_OK·후속 산술·다른 저장은 ZT04 공통근거 참조 |
| 0479/LAD15 NID12, 별도 CONT_S | 0668 RID128 ORef533/W552→NOT Contact591; W592→LRef507.LMNR_LS; 0671 Instruction RID113 CONT_S | PID 핀은 가공값에 다시 NOT. 원시 반전과 소비 반전을 혼합하지 않음. 제목 not used와 OFF Contact583(0670 RID53 M0.1) EN 조건 존재, 현재 호출/활성 여부 미확정 |
| 0184/LAD1868 NID14, burner control | 0585 RID233 ORef38/W37→NOT Contact28; W29→정접점1670, operand ORef34/W33도 같은 RID233; W30→SCoil1669 M180.5 | 같은 가공Close의 NOT/정접점 직렬 원문을 보존. 임의로 정상 순서로 수정하거나 현장 실행 결과를 단정하지 않음 |
| 같은 버너 네트워크 | ORef1423/W1555→정접점1654; W1655→OR1248.in1 | 다른 버너 단계의 위치 조건. 다른 OR입력·부모 단계는 MV03 초안으로 연결하며 LS20 제어기 소유로 변경하지 않음 |

### 3.3 보존 원문에 있는 다른 쓰기

0403/LAD1083, block simulation, NID2의 정적 원문만 확인했다. Part500 Gt Int in1 W65/ORef73=0635 RID314 Data.Pot_MV03 AO1152(DB1.DBW144), in2 W71/ORef74=0637 RID254 Int **2**. powerrail W21→Gt500.pre, out W64→일반 Coil501.in, W554/ORef523=0635 RID238 Inputs.MV03 Close DB13.X7.6 Write. 즉 이 별도 보존 블록은 위치값 **>2**의 비교 결과를 같은 DB 비트에 쓴다. 이 식을 실제 센서의 물리 닫힘 조건으로 적용하지 않는다.

해당 보존 블록을 작성·생성·수정·실행·행동시험하지 않았다. 현재 호출/활성/온라인 쓰기 및 간접/겹침 쓰기 전체 목록은 미확정이다. 이름이 같은 모든 RID를 다른 문맥에 재사용하지 않았고, 위 쓰기는 선언 NID2/UID523와 Coil 연결을 확인했다. 이번 문서의 핵심은 다른 writer의 존재이지 실행 주장이나 재개 권고가 아니다.

## 4. 전기 전달 경로 — 적용, 실제 PDF 끝점 확인

실제 렌더: PID1, OEM PDF40/124, 시공 PDF56 총4쪽. 확대 캡처는 동일 페이지의 보조 이미지로 페이지 수를 늘리지 않았다.

| 구간 | 확인 끝점·선·접점 | 원본 위치/미확정 |
|---|---|---|
| 공급 | +24Vdc 10.7 상단 버스 분기점 → X1/92, 5×20 2A F → 선39.4 | FG39/PDF40 오른쪽 LS20 가지. 표기 정격은 설계 자료이며 현행 보호값 확정/변경 아님 |
| 센서 | 39.4 → LS-20 **NC11/12** → X1/93 | 같은 페이지 LIMIT SWITCH VALVE CLOSING. 닫힘 기계위치/캠과 접점 실제 전환시점은 미확정 |
| PLC 입력 | X1/93 → E7.6, 계속참조123/6 → FG123/PDF124 E7.6 → **MOD9 단자37**, LIMIT SWITCH LS-20 | FG123 상단 유입 참조39/7도 원문 보존. CPU515/MOD9는 설계표기, 현재 CPU/슬롯 확인 아님 |
| 공통 공급/귀로 경계 | FG123 단자39는 123.1(+24Vdc, X21/3009 5×20 2A IST), 단자40은 −0Vdc10.6 | 이는 모듈 공급측 표기. LS20 신호선을 단자39/40에 직접 연결했다고 해석하지 않음 |
| 공유 trunk | 시공PDF56 row6_1 =FLA+MV03-FLO1TB1A, CR→MV-03 FLO1TB1, LS15/16/19/20 | DC/CVV/12G/1.0/spare3, 100 LBD1→E100, Adjustment7 LEN44. LS15/16 공유 때문에 같은 센서·같은 소유라는 결론 금지 |
| LS20 branch | row6_16 =FLA+MV03-LS20A, MV-03 FLO1TB1→MV-03 LS-20 | DC/CVV/2C/1.0/spare0, LAD1 E300→LAD1→E1300, Adjustment5 LEN5 |

OEM X1/92~93과 시공 FLO1TB1 내부 단자/심선의 연결 세부는 확보되지 않았다. 두 문서의 끝점을 확인한 것과 완전한 준공 연속성 검증을 구분한다. 실측 전압/도통/절연, 실제 극성, 단선 시 거동은 취득하지 않았다. NC 그림과 PLC NOT가 있어도 안전기능 인증이나 fail-safe 보장은 성립하지 않는다. EV 69KA/71KA 부하5–9 정정은 별도 공통근거로 유지하며 이 NC11/12와 혼합하지 않는다.

## 5. 알람·복구 — 부분 적용, 부모 알람 소유 유지

LS20 정확명 독립 고장 비트·독립 타이머·독립 HMI 알람은 이번 검색과 고유 경로에서 확보하지 못했다. 따라서 없는 전용 알람을 만들거나 부모 MV03_FAULT를 LS20 고장으로 복제하지 않는다.

부모 MV03 초안의 DB3.X4.3 응답/명령누적 고장과 S5T#150S는 접촉기 응답·부모 명령 경로다. 이를 LS20 응답 허용시간으로 쓰지 않는다. ZT04 위치 OFR도 별도 위치 환산 경로다. 이 공통사항은 이번 LS20 고유 의미검토 수에 포함하지 않는다.

LS20 처리값은 Q2.0 명령 억제·수동/기동 요청 해제에 관여하지만, 화면 닫힘 표시 변화, 요청 비트 Reset, 부모 fault 해제, 기계 닫힘, 안전한 재기동/실제 복구는 서로 다르다. 실제 복구 판정에는 승인된 현장 상태기록, 시각 일치한 raw/가공/출력/기계위치 자료 및 현재 프로젝트 식별이 필요하다. 강제입력·접점 우회·교정/리셋 실행·보호값 조정 절차는 작성하지 않는다.

## 6. 증상별 관찰 — 문서 적용, 현장 조작 없음

| 증상 | 확보할 읽기 전용 관찰·대조 | 배제할 단정 |
|---|---|---|
| 닫힘 표시가 실물과 다름 | 같은 시각의 물리 위치/캠 사진, I7.6, DB13.X7.6, DB11.X22.4, 현재 HMI 매핑 | 세 주소를 같은 신호/같은 극성으로 간주하지 않음 |
| raw와 가공이 반대 | 0397 Not150, Word42 중첩, 호출조건과 현재 프로젝트 | NOT 자체를 오배선으로 판정하지 않음 |
| 가공값이 위치와 무관하게 바뀜 | 현재 호출/쓰기 교차참조, Word6, 보존0403 다른 쓰기의 존재·현재 비활성 증거 | 현재0403 실행을 추정하거나 실행시험하지 않음 |
| 닫힘 명령이 나오지 않음 | Q2.0·처리Close, 부모 허가/고장/모드/요청의 같은 시각 기록 | LS20만 단독 원인으로 지목하지 않음 |
| 닫힘 후 수동/버너기동 요청이 사라짐 | 0345 R369/R46, DB2.X10.0/M180.5, 부모 다른 Set/Reset | 알람 Reset 또는 기계복구 성공과 동일시하지 않음 |
| 엔코더가 멈추거나 0으로 보임 | 처리Close, EM_OK, SW_GATE2, ZT04 값·교정요청·기술객체 매핑 | LS20와 엔코더를 같은 부품으로 병합하지 않음 |
| 입력이 고정됨 | 승인된 기존 점검기록에서 X1/92~93, LS20 NC11/12, MOD9/37 및 준공함 매핑 | 전용 알람 부재만으로 정상 판정하지 않음 |

관찰기록 필드: 관찰자·시각/시간대·설비 위치·값/형식/단위·프로젝트 식별·취득장치·비교원본·배제결과·승인된 조치·후속 복구근거. 현장 관찰값을 지어 채우지 않으며 기존 note/repair_observation·미지필드·기록키·다른 설비 기록을 변경하지 않았다.

## 7. 완료·누락·인계

| 영역 | 상태 | 경계 |
|---|---|---|
| 설비·자료 기준 | 적용/초안 | LS20-MV03 직접 문서 식별, 실제 실물동일성 보류 |
| IO/HMI | 부분 적용 | raw/가공/다른쓰기/설정 구분, HMI 호출 출력 미결속 |
| 제어 | 부분 적용 | 고유소비·반전·요청Reset·겹침쓰기 정적확인, 현재 호출/최종값 미확정 |
| 전기 끝점 | 부분 적용 | 실제 PDF4쪽 끝점·개정확인, FLO1TB1 내부 준공연결 누락 |
| 알람/복구 | 부분 적용 | 독립항목 미확보 및 부모소유 분리, 실제복구 미확인 |
| 증상 관찰 | 적용/문서 | 관찰표 작성, 현장값/시험 없음 |
| 완료/누락 | complete_with_gaps 문서초안 | 기능통합·게시·TIA·현장완료 아님 |

필요 자료/수집 위치/통과 기준:
1. 현 LS20 명판·MV03 장착/캠 사진과 승인 준공 P&ID: 태그/실물/닫힘 검출 방향 일치 판정.
2. 준공 결선표/단자함 상세: X1/92~93↔FLO1TB1↔센서11/12↔MOD9/37의 심선/단자별 연속 대응.
3. 현재 TIA 프로젝트/온라인 비교와 교차참조: I7.6·DB13.X7.6·Word6·별도쓰기·호출순서 및 실제 활성상태 확인. 현장 변경 없이 승인된 자료로 비교.
4. 현재 HMI 소스/태그·이벤트: 0369 ORef34/RID686, ORef42/RID452와 DB11.X22.4의 실제 결속·표시갱신을 확인.
5. 승인된 위치별 관찰기록: 기계위치/raw/가공/HMI/출력·접촉기 응답의 동시 자료로 정상극성과 복구 판정. 본 초안의 정적 해시검사는 이를 대체하지 않음.

네 기능(도면·래더 비교/선택복원/전후비교/보고서PDF)은 LS20 지원 구현·저장·재열기·UI 검증을 하지 않았으므로 모두 not_run/미확인이다. documentation=complete_with_gaps(draft), static_review=selected_sources_reviewed, ui_records=not_run, publication=not_published, tia_compile/live_cpu/field_recovery=not_performed. BC01 회귀·빌드·생성기·패키징은 문서조사 범위를 넘어 미실행. 부모에게 통합 검토용으로 인계하며 현장 미확정을 완료로 올리지 않는다.

## 부록 A. 검사 범위와 원본 바이트 일치

아래 표의 모든 SHA256은 전체 파일 바이트에 대해 계산했고 Gitblob은 고정 커밋의 `git rev-parse COMMIT:path` 및 `git show COMMIT:path` 바이트와 비교했다. 해시검사와 의미검토는 별도다. 네트워크 의미검토는 문서에 기재한 LS20 관련 가지에 한하며 파일 전체의 모든 부모 논리를 검토했다는 뜻이 아니다. XML695개 명칭검색도 695개 의미검토로 세지 않는다.

- 선정 원본 해시검사 **32파일**, Gitblob 바이트일치 **32/32**. 원문 의미검토 **31파일의 지정 범위**(XML network 9·선언 17·PDF3·HMI CSV1·대장1); 별도 network-map1은 탐색색인이다. PDF 의미검토4쪽, 동일쪽 확대 이미지 별도 집계 없음.
- 원본 Git status: clean. 전체 저장소/전체 원본 보존 검사를 대신하는 수치는 아니며, 선정 파일의 고정 커밋 바이트일치를 확인했다.
- 검사 JSON: `extracts/LS20/source-hashes.json`, 명칭·writer 검색: `extracts/LS20/search.json`. 자체 정적 파서/추출은 해당 폴더에만 작성했다. 0403 첫 Part ID 탐색 오류는 실제 Coil501 확인 후 재추출했으며 실행 의미를 시험하지 않았다.

| 선정 원본 | 전체 SHA256 | 고정 Gitblob | 바이트일치 / 검토범위 |
|---|---|---|---|
| docs/equipment-standard/INVENTORY.json | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | 일치 / 대상행 의미검토 |
| all-in-one/sources/hmi_plc_tags.csv | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | 일치 / 해당 태그 의미검토 |
| all-in-one/sources/Electrical_Rev2.pdf | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | 일치 / 실제 PDF 지정쪽 의미검토 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | 일치 / 실제 PDF 지정쪽 의미검토 |
| all-in-one/sources/PID_1684n002I.pdf | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | 일치 / 실제 PDF 지정쪽 의미검토 |
| all-in-one/sources/decoded-original/network-map.json | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | 일치 / 탐색색인, 원문대조 보조 |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | 일치 / 지정 가지 의미검토 |
| all-in-one/sources/decoded-original/0184-FlgNet.xml | `a0a59597c73eb68e1cbdb2f41d640eabccfd05655c4e9c08624be6027974caf3` | `da94babe74df340b11b37560e94e04acfad1212a` | 일치 / 지정 가지 의미검토 |
| all-in-one/sources/decoded-original/0345-FlgNet.xml | `b278a319d4d8cb8d157f449a2365445ff8f172245ebd2a468aa3ee79dba60f93` | `25656c8d9f39b8eccb67300905545b4cbcec2bfd` | 일치 / 지정 가지 의미검토 |
| all-in-one/sources/decoded-original/0353-FlgNet.xml | `062854b25c5afacb34e53ce0ee7cd8c660cd9a0f5b79a02d8a5fbed89c794766` | `19b9493c88c95031ee327dc9e567bc7780fd4839` | 일치 / 지정 가지 의미검토 |
| all-in-one/sources/decoded-original/0369-FlgNet.xml | `f64e35330b3816e761ce72575977878d5cad6317191297c2a64107629a611806` | `487c75b5e66b32d1f7dda78eb750abea855f365a` | 일치 / 지정 가지 의미검토 |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | 일치 / 지정 가지 의미검토 |
| all-in-one/sources/decoded-original/0403-FlgNet.xml | `77b03e38aa857ac8dd404f2f66a56256939b4e7924b41334a7981b86089c1e6b` | `4c806e31eb65f00cbb7870c72896ac26a8bc3dd3` | 일치 / 지정 가지 의미검토 |
| all-in-one/sources/decoded-original/0479-FlgNet.xml | `112e55599a4dc705438c8c61b936da9a167c22d9bbd909eda11c45c9dc33e839` | `38df067a2f4f62edfba9c5027002feccb45e5142` | 일치 / 지정 가지 의미검토 |
| all-in-one/sources/decoded-original/0514-FlgNet.xml | `3826044da205b26e31f400232a55aa240eef8a4933e532d0bf9a3bccee2d19c5` | `efecda3b942fba7ce4ab9cd8c773136a6a021f83` | 일치 / 지정 가지 의미검토 |
| all-in-one/sources/decoded-original/0585-IdentXmlPart.xml | `e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184` | `16574d37ef3ca61b59ba396c400e269ab1dd3440` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0617-IdentXmlPart.xml | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | `9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0618-IdentXmlPart.xml | `0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c` | `9eec0dbd8abde4aa7295f77b63ad473f895f274b` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0619-IdentXmlPart.xml | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | `11f0502c84a1f319a21459a35c0dc1c6ce8e8f36` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0634-IdentXmlPart.xml | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0635-IdentXmlPart.xml | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0637-IdentXmlPart.xml | `3fb68f57dbe2a877c4ad5aa1b3316810cf84958f2d13b5b1d7d321e0915271c7` | `cb1d7fb76aa2afd96eb46984cc1e71b77f36395c` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0668-IdentXmlPart.xml | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` | `fe0f30d1eaae37783b0f03cb090353b3a3de3600` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0670-IdentXmlPart.xml | `e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841` | `b9466007b14e5c4f5d353dca5734401317e2dc03` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0671-IdentXmlPart.xml | `26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293` | `e38a4e2c93ac8093e2b0b8e082a64688b5d9845e` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0674-IdentXmlPart.xml | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0676-IdentXmlPart.xml | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | 일치 / 지정 선언 의미검토 |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` | 일치 / 지정 선언 의미검토 |

## 부록 B. 인계 및 금지 경계

- 부모 검토자는 0397 중첩 Word와 NOT 쓰기, 0345 Close 소비3곳, 0403 다른 writer, FG39/123 실제 PDF 끝점·개정부터 독립 대조한다.
- 다음 한 작업: 위 고유 근거의 독립 통합 검토. 새 현장자료 없이 정상극성·HMI 결속·준공배선을 임의 확정하지 않는다.
- 자체 산출물 외 변경 없음. 업로드·새 Work/Codex·재위임·원본 생성기·앱 빌드·시뮬레이터/행동시험·TIA·PLC/현장 조작·보호값/SEJIN 변경·게시 모두 미수행.
