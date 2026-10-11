# PC02 자체 조사 초안 — 소프트웨어 압력 루프 명칭

고정 입력 `abcf31c5030bc7ef8749ed8e869a857f2387a28a / v1.12.0`, 조사 시작 2026-10-11 10:39:52 UTC. PC02 한 ID의 읽기 전용 문서 조사이다. 제품 통합·게시·TIA 컴파일·현재 CPU·실물·현장 복구 완료를 뜻하지 않는다. 실행 모델/추론 수준의 런타임 증명은 미확인이다.

## 핵심 확인·상충·누락·인계

1. PC02는 INVENTORY catalog[3]의 **software**이며 별칭 `pc_02`이다. 전용 물리 계기/전용 FG가 배정되어 있지 않다. PSH02, PSH03 또는 MV03와 ID를 병합하거나 함께 완료로 세지 않는다.
2. `live_index.json` `_7ex` doc14의 STL 텍스트는 Data.PSH02_SETPOINT와 Data.PSH_02를 ITD→DTR로 바꾸어 Local Real_SPPC02/Real_PC02에 전달한다. `0668/0669-IdentXmlPart.xml` NID11의 Global 읽기/Local 쓰기와 NID12의 Local 읽기가 대응한다. **STL 문장 순서는 추출 색인 근거이고, 별도 STL 실행 본문/온라인 실행을 확보한 것은 아니다.** 선언 대조가 색인의 모든 명령·실행 의미까지 증명하지 않는다.
3. `0479-FlgNet.xml` NID12/doc15의 CONT_S는 DB25 PID_MV03를 인스턴스로 쓰고 Local 두 Real을 SP_INT/PV_IN으로 받는다. OFF는 상수 false가 아닌 **M0.1 Global Bool**이다. 제목 `not used`와 OFF 접점만으로 비실행을 확정하지 않는다.
4. 0479 QLMNUP/QLMNDN과 `0344`의 일반 Coil이 모두 **M14.4/M14.5**에 쓴다. 0344는 PSH03 오차 제어이며 PC02 값과 다른 입력원이다. `0345`는 같은 메모리 비트를 읽어 MV03 자동 출력 가지에 사용한다. 현재 호출·인터럽트 우선순위·쓰기 순서·최종 출력은 미확정이다.
5. 0479 COM_RST는 NOT MV03_Auto OR Open MV03 for washing이고, LMNR_HS/LS는 각각 NOT 처리 Inputs.MV03 open/Close이다. 이는 PID 호출 입력이지 PC02 고유 알람 Reset이나 센서 정상 극성 증명이 아니다.
6. 0479의 9개 ORef는 RefId가 없다. LMNS_ON/LMNUP/LMNDN/PVPER_ON/PV_PER/PV_FAC/PV_OFF/PV/ER의 기본값·미사용 여부·DB 저장값을 보충하지 않았다.
7. 누락: 원시 STL 본문/명령 결속, 실제 OB/DB25·CPU 실행 및 전체 Writer, 현재 HMI 이벤트와 스케일, PSH02/03와 현행 도면의 대응·교정, MV03 실물/안전 복구. 현장 증거 없이 보호값 조정·동작 시험·강제값·복구 지시를 하지 않는다.

### 공유 근거와 이번 독립 검토

- `PSH02-DOTS-DRAFT.md`는 환산0496/0291/0014, HMI 주소, 전기 FG75/107와 P&ID 상충의 인덱스다. 그 고정 원본 해시를 재확인하여 데이터 공급원 문맥만 연결 재사용했다. 센서 초안의 실물 회로를 PC02 고유 회로로 복제하지 않는다.
- `MV03-DOTS-DRAFT.md`는 0344/0345/0479와 출력·전기 경계의 인덱스다. 이번에는 PC02 고유 0479 **전체 Part/Wire/ORef/LRef/Instance**, 0665/0667~0671 선언, NID11 Local 생산/12 소비, 0344 중복 쓰기 및 0345 소비 구간을 독립 재파싱·대조했다.
- 0344 UId296/RID34/NID3의 전역 검색에는 0563의 다른 블록 선언도 충돌한다. Contact334의 operand/Timer 용법, 주변 0617 선언 묶음과 색인 문맥을 대조하여 **0617 Tag_148**만 해당 후보로 채택했다. NID/RID/UID 숫자만 일치하는 전역 결속은 허용하지 않는다. 추출 JSON에는 원 후보를 보존하고 검사 JSON에 이 제외 이유를 남겼다.
- 해시 일치 파일 수는 내용 불변 검사의 범위다. 그 수만큼의 네트워크/설비 의미 검토 완료를 뜻하지 않는다.

## 1. 설비·자료 기준

| 항목 | 확인과 경계 |
|---|---|
| ID·유형 | PC02 / software / 계측 / parent_id=null / depth0 / phase2 planned / priority_key=null |
| 범위 | BATCH06 및 GME-CATALOG-OVERLAP-REVIEW 해당 ID: new_research_scope=true, physical_identity_verified=false, electrical_fgs=[] |
| 기능 소유 | `_7ex` cyc_int5 ogni 100ms의 PC02 명칭 Local 값과 CONT_S 호출. 물리 압력계가 아닌 소프트웨어 데이터/제어 연결 |
| 입력/관련 소유 | PSH02 환산·설정값을 읽는 백업 경로. PSH03 오차 경로와 출력 비트만 공유. MV03는 구동 설비 별도 소유 |
| 자료 시점 | 고정 백업/도면 및 v1.12.0 문서. 선언 MT/SM 날짜는 필드의 저장 정보이며 현재 CPU 증명 아님 |
| 금지/보존 | 원본·코드·대장·버전·운영기록·배포 변경0. 원본 build/test/generator, 시뮬레이터 생성/실행/시험, PLC/현장/보호값/SEJIN 변경0 |

원본 XML의 공통 접두사는 `all-in-one/sources/decoded-original/`이다. `live_index.json`, `hmi_plc_tags.csv` 및 PDF는 `all-in-one/sources/` 아래이다. 문서 doc 번호, XML 파일번호, NID를 혼동하지 않는다. source-mv06의 AGENTS/작업표준/스킬/템플릿/INVENTORY와 최신 버전·인계·게시·작업 기록을 읽었다. 조사 산출만 별도 작성하며 원본 통합 절차를 실행하지 않았다.

## 2. I/O·HMI — 주소·형식·읽기/쓰기

| 대상 | 선언/주소 | 직접 사용 및 경계 |
|---|---|---|
| Data.PSH02_SETPOINT | 0668 Global RID95, Int, SSD AO336, Data DB1.DBW42 | NID11 UID429 OID16 읽기. 고압 한계 DB1.DBW28와 다름 |
| Data.PSH_02 | 0668 Global RID97, Int, AO1568, DB1.DBW196 | NID11 UID441 OID16 읽기. PSH02 raw IW286 자체 아님 |
| Real_SPPC02 | 0669 InterfaceAccess Local RID96, Real32, AO544 | NID11 UID436 AK=Write/OID17 → NID12 UID535 읽기. AO544를 Global DB 주소로 쓰지 않음 |
| Real_PC02 | 0669 Local RID98, Real32, AO576 | NID11 UID448 Write → NID12 UID536 읽기 |
| OFF | 0670 SimpleAccess Global RID53, Memory AO1, Bool=M0.1 | NID12 UID529 → Contact583. literal false와 구분 |
| Flag.MV03_Auto | 0668 Global RID99, AO56, DB2.DBX7.0 | NID12 UID530 → NOT Contact585 → COM_RST 입력 |
| Open MV03 for washing | 0670 Global RID100, Memory AO385=M48.1 | NID12 UID531 → Contact587 → COM_RST 입력 |
| Inputs.MV03 open/Close | 0668 Global RID127/128, AO61/62, DB13.DBX7.5/7.6 | NID12 UID532/533 → NOT Contacts589/591. 처리 DB 입력이며 물리 정상극성으로 치환 금지 |
| PID UP MV03 | 0670 Global RID106, Memory AO116=M14.4 Bool | NID12 UID544 Write/QLMNUP. 0617 RID39 NID3 UID302 Write, NID4 UID420 Read도 존재 |
| PID down MV03 | 0670 Global RID107, Memory AO117=M14.5 Bool | NID12 UID545 Write/QLMNDN. 0617 RID37 NID3 UID299 Write, NID4 UID430 Read도 존재 |
| PID_MV03 | 0665 AufDBBlock Global RID104, TOD N25 BT=DB | NID12 UID546 AK=InstanceDB, CONT_S 유형. 현재 DB25 상태/초기화값 미확인 |
| CONT_S | 0671 Instruction RID113 | NID12 UID507 AK=Call, 0479 LRef507. 별도 PC02 아날로그 출력 Word 없음 |

Global 데이터의 Data/Flag/Inputs 주소는 해당 Block_DB 형식 및 주변 DB 선언 문맥과 대조했다. 별도 범위의 RID를 주소표 전역 키로 사용하지 않았다.

### 2.1 입력 공급원 연결: 공유 사실과 경계

PSH02 초안에서 같은 원본으로 검토된 0496/NID16은 ON Contact475/W476→CRef456.en, IN0 W470/463=ON, Analog_input W471/464=PSH02:P(PIW286, Peripherie), Coeff W472/465=DB4.DBW42, Zero W473/466=DB4.DBW40, OutValue W474/467=DB1.DBW196, Out_of_range W24/23=DB3.DBX22.1이다. 이 연결은 **PC02 이름이 아니라 Data.PSH_02 주소를 공급하는 소프트웨어 근거**다.

공유 환산0291/0014는 Int→DInt 정수 경로, IN0 AND Analog_input>−1382 AND≤32767 범위에서 `(입력+Zero)×Coeff/28000`, 범위 밖 −9999 및 ENO→일반 OFR Coil, NOT IN0에서0 전달로 분석되어 있다. PC02의 ITD/DTR 실수화는 이 앞단 환산과 다르며, 실수화 자체가 mbar 단위/정상값/안전값을 보장하지 않는다. OFR/−9999가 0479 호출을 직접 금지하는 핀 연결은 0479에서 발견하지 못했다. 전체 프로그램의 다른 영향 부재를 선언한 것은 아니다.

HMI용 raw 복사 0398/NID2의 Word Move97는 IW286(Input, SAM=None) → Inputs.PSH_02 DB13.DBW50이며, 환산의 Peripherie PIW286과 접근이 다르다. 앞 Move96.eno→Move97.en(W110) 연결이 있어 독립 상시 복사라고 단정하지 않는다. 이를 PC02의 별도 하드웨어 AI로 세지 않는다.

### 2.2 HMI 주소 대조

`hmi_plc_tags.csv`를 직접 검색했다. 아래는 설정주소이며 화면/쓰기 이벤트/로그/온라인 값 증명이 아니다.

| HMI 태그 | 주소 | 내부 ID | 경계 |
|---|---|---|---|
| data_DB1_DBW42 | DB1,INT42 | 0027C | 제어 설정의 Global 주소 |
| data_DB1_DBW196 | DB1,INT196 | 00292 | 환산 PV Global 주소 |
| Editor_PSH02 | DB26,INT18 | 00410 | 레시피 편집 버퍼; DB1W42 직접 편집과 구분 |
| Allarmi_215 | DB3,X22.1 | 00280 | PSH02 OFR의 관련 주소 |
| Allarmi_67 | DB3,X8.2 | 0014A | PSH02 고압의 관련 주소 |

Access Name는 PLC다. CSV에서 문자열 PC02/PC_02 및 PID_MV03에 직접 대응하는 태그는 찾지 못했다. 이는 전용 화면이 없다는 증명이 아니며, Local Real을 HMI 영속 태그로 만들지 않는다. DB25 현재값/위젯 단위/스케일/편집권한/PLC까지의 commit 이벤트는 근거 미확보다.

## 3. 제어 구조 — 변환·호출·중복 쓰기·소비

### 3.1 Local 값의 상류와 호출 맥락

`live_index.json` `_7ex` doc1: Name=cyc_int5 ogni 100ms, Event class=cyclic interrupt, Language=lad. doc2 인터페이스 이름에 real_sppc02/real_pc02가 있다. doc14 제목은 `control pc02 moduling mv03 - convert values in real`, STL 텍스트는 `L Data.PSH02_SETPOINT; ITD; DTR; T #Real_SPPC02; L Data.PSH_02; ITD; DTR; T #Real_PC02` 순서다. 원문 소문자/주석 포함 추출은 `extracts/PC02/live-index-cycle.json`에 있다.

0668 RID95/97의 NID11 읽기와 0669 RID96/98의 NID11 Write/NID12 Read가 값 결속을 독립 지지한다. 다만 이 NID11은 제공된 FlgNet 대응 목록에서 별도 실행 명령 본문으로 확보하지 못했다. 따라서 변환순서는 **색인 + 선언 교차확인**, 0479 연결은 **실제 XML 핀 확인**으로 신뢰 층위를 구분한다. 명칭의 100ms 및 CYCLE 입력 T#100MS가 현재 CPU OB 주기/지연/우선순위를 증명하지 않는다.

### 3.2 0479/NID12 전체 핵심 핀

LRef507 RefId113=CONT_S, Instance546 RefId104=PID_MV03 DB25. 이 네트워크는 CRef가 아니라 **LRef 라이브러리 호출**이다. 사용하지 않은 CRef 번호를 만들지 않는다.

| 입력/출력 | Part/Wire/ORef | 결속/해석 |
|---|---|---|
| en | W547/ORef529→Contact583; W584→LRef507.en | OFF M0.1이 호출 Enable을 공급 |
| COM_RST | W548/530→NOT Contact585→W586 OR498.in1; W549/531→Contact587→W588 OR498.in2; W550→507.COM_RST | NOT Auto OR Washing. 일반 경보 Reset과 다름 |
| LMNR_HS | W551/532→NOT Contact589; W590→507.LMNR_HS | NOT 처리 Open 입력 |
| LMNR_LS | W552/533→NOT Contact591; W592→507.LMNR_LS | NOT 처리 Close 입력 |
| CYCLE | W561/ORef534, 0667 Constant RID21 | T#100MS |
| SP_INT | W562/ORef535, 0669 Local RID96 | Real_SPPC02 |
| PV_IN | W563/ORef536, 0669 Local RID98 | Real_PC02 |
| GAIN | W566/ORef537, 0667 RID105 | Real −4.0 |
| TI | W567/ORef538, 0667 RID58 | T#10S |
| DEADB_W | W568/ORef539, 0667 RID22 | Real2.0 |
| PULSE_TM | W573/ORef540, 0667 RID25 | T#200MS |
| BREAK_TM | W574/ORef541, 0667 RID27 | T#5S |
| MTR_TM | W575/ORef542, 0667 RID26 | T#3S |
| DISV | W576/ORef543, 0667 RID22 | Real2.0 |
| QLMNUP | W577→ORef544, 0670 RID106 Write | M14.4 Bool 쓰기 |
| QLMNDN | W578→ORef545, 0670 RID107 Write | M14.5 Bool 쓰기 |

W593 Powerrail은 583/585/587/589/591.in에 각각 연결된다. COM_RST와 limit 입력은 en 직렬 접점의 뒤에서 파생되는 동일 조건이라고 축약하지 않는다. 문서의 시간 상수는 호출 인수 원문이며, 현장 권장값/보호설정/측정된 펄스 길이가 아니다. 이 XML에는 CONT_S 내부 구현이나 ENO 소비 경로가 제공되지 않는다.

선언 없는 ORef 9개: LMNS_ON W554/553, LMNUP W556/555, LMNDN W558/557, PVPER_ON W560/559, PV_PER W565/564, PV_FAC W570/569, PV_OFF W572/571, PV W580/579, ER W582/581. RefId 없는 상태를 false/0/미사용 확정으로 채우지 않는다. 현재 DB25와 정확한 라이브러리 판본/호출 초기값을 별도로 확인해야 한다.

### 3.3 0344/NID3의 다른 Writer

0344/doc1705의 ON Contact328(W303/286)→W329는 Sub256.en과 타이머 가지를 병렬 공급한다. Sub256(Int) in1 W304/287=Data.PSH03_SETPOINT, in2 W305/288=Data.PSH03, out W306/289=Local ErrPSH03(0062 RID31 Write)이다. PC02의 PSH02 입력과 별도다.

- NOT Tag_147 Contact330(W308/291)→W331 SdCoil263; W307/290=S5T#4S; W310/292=Tag_148(T139,0617 RID34).
- Tag_148 Contact332(W312/294)→W333 SdCoil268; W311/293=S5T#10S; W314/295=Tag_147(T138,RID32).
- NOT Tag_148 Contact334(W315/296)→W335 두 비교 pre.
- Ge276: ErrPSH03 W316/297 ≥ Int5 W317/298 →W318 일반 Coil279→W320/299=PID down MV03 M14.5(0617 RID37 Write).
- Lt282: ErrPSH03 W321/300 < Int−5 W322/301 →W323 일반 Coil285→W325/302=PID UP MV03 M14.4(RID39 Write).

비교는 `≥5`와 `<−5`이며 대칭 닫힌 deadband라고 바꾸지 않는다. 0479 라이브러리 출력 쓰기와 0344 일반 Coil 쓰기는 같은 주소지만 다른 생성식이다. S/R latch·Word 쓰기와 혼동하지 않는다. 선언검색에서 확인한 직접 명명 Writer는 이 두 경로이나, 간접/주소별칭/통신/강제값까지 전수 배제한 것은 아니다. 실제 마지막 Writer와 스캔/인터럽트 간 선점 여부는 현재 CPU 근거가 필요하다.

### 3.4 0345/NID4 소비 범위와 MV03 출력 경계

같은 블록군 0617 RID39 NID4 UID420, RID37 UID430의 **읽기**를 0345 ORef420/430으로 결속했다. 0670의 NID12 Write를 다른 네트워크 소비 선언으로 재사용하지 않았다.

- 자동 열림: Auto Contact507(W455/419) → UP509(W456/420) → Pulse511/ON513(OR543.in1/2). 출력 전에는 ON489, NOT MV03_FAULT505, 최종 NOT ResetEncoderProcedure44, NOT InputsOpen523이 있다. 일반 Coil390 W470/ORef428=Start open MV03 Q1.7(0617 RID47 Output AO15).
- 자동 닫힘: Auto525→DOWN527(W472/ORef430)→Pulse529/ON531→OR544.in1/2. 세정 차단 NOT Washing539 이후 OR53에는 별도 교정 ResetEncoderProcedure546 가지도 합류한다. 최종 NOT InputsClose541→Coil407 W486/ORef438=Start Close MV03 Q2.0(0617 RID48 Output AO16).
- 수동 열림/닫힘, Open for washing, Close for Burner Startup, 교정 가지는 자동 PID 비트와 별도 요청이다. 따라서 M14.4/14.5가0이어도 모든 출력경로를 차단했다고 판단할 수 없다.

위는 PC02 산출의 **소비 및 출력 경계** 확인이다. MV03 모든 운전 모드·알람·전기 회로·정비 완료를 PC02로 집계하지 않는다. ON=M0.0도 심볼이고, `MV WORK PULSE OR ON`을 펄스 단독 필수 조건으로 축약하지 않는다. 출력 메모리/프로세스 이미지 Q와 실제 접촉기 동작은 별도다.

## 4. 전기 전달 경로 — software의 비해당과 관련 끝점

**PC02 전용 전원/차단기/단자/케이블/센서/접촉기 회로는 비해당**이다. 이는 software 유형·전용 FG 없음에 따른 소유 경계이며, 전체 설비의 회로자료가 없다는 뜻이 아니다. PC02라는 실물 압력전송기를 새로 정의하지 않았다.

관련 경로를 탐색할 때는 다음 기존 검토를 연결한다. 원본 PDF 해시가 동일함을 재확인했으므로 페이지를 새로 렌더해 동일 현장 보류를 반복하지 않았다. 아래 footer/개정 값은 **PSH02 선행 초안의 실제 렌더 검토 재사용**이며 이번 독립 PDF 판독으로 표시하지 않는다.

| 관련 소유 | PDF/실제쪽/FG·개정 | 끝점·사용 경계 |
|---|---|---|
| PSH02 | Electrical_Rev2.pdf 실제76쪽 FG75, 날짜27.05.2024 개정란 공란 | X1:175/176/177 → PEW286/75SCH2. 도면 압력채널의 끝점이며 PC02 계기번호 아님 |
| PSH02 AI | 같은 PDF 실제108쪽 FG107, Rev2 17.03.2025 | MOD3 I7+34 및 U7−/I7−36. 원시 PIW286 공급원 관련 회로 |
| 설치 문맥 | Electrical_Can_Decoating_20241118.pdf 실제58쪽 CANDC-CONS-C008-058, Rev1 24.11.11 first draft design | UC01-PSH02A; 시공/설계 문맥과 현행 설치 확인을 구분 |
| 공정/개정 | PID_1684n002I.pdf 실제1쪽, 1684n002 RevI 15/01/2013 | RevF PSH02 위치변경, RevH MV06 추가/MV03 명령계기 변경. PSH02와 MV06 연결 문맥, PC02 실물 동일성 미확정 |
| MV03 출력 | 0345 Q1.7/Q2.0 끝점 확인; 전기 상세는 MV03 선행 초안 | 실제 접촉기/단자/케이블은 MV03 소유. PC02 전용 릴레이 접점을 만들어 추가하지 않음 |

OEM PSH02 설명 OUTPUT MV03, 현행으로 보이는 0347/0348의 MV06 논리, 위 P&ID 변경기록, PC02 제목 moduling mv03가 서로 시간/소유 문맥이 다르다. 소프트웨어 제목 하나로 어느 도면이 현재 정답인지 확정하지 않는다. FG와 실제 PDF 페이지를 동일시하지 않으며, 다른 설비의 릴레이 하단 접점표1/5/9를 PC02 부하접점으로 사용하지 않는다.

## 5. 알람·Reset·복구 경계

| 항목 | 근거와 결론 |
|---|---|
| PC02 고유 알람 | 0479에 PC02 이름의 알람 출력/발생식/경보 타이머/래치 근거를 확보하지 못했다. PV/ER ORef는 무선언 상태로 HMI 경보라고 할 수 없음 |
| COM_RST | 0479 OR498→W550. NOT MV03_Auto OR Washing가 CONT_S 핀에 전달. 알람 확인/호른 정지/현장 안전 Reset과 다름 |
| PSH02 OFR | 관련 공급원 DB3.DBX22.1 및 −9999. 0479의 en은 OFF이며 OFR 직접 접점 없음. 차단 보장 추정 금지 |
| PSH02 고압 | 공유0537/NID11: Data.PSH_02≥Data.PSH02_MAX_SETPOINT, Tag111 T132 SD S5T#3M 뒤 MAX_PSH_02 Set(DB3.DBX8.2). 해제는 알람 AND PV<(MAX−5)에서 Reset 및 STOP_HORN Set. RESET_ALLARM 접점은 이 네트워크에 없음 |
| MV03 fault 영향 | 0345 NOT Allarm.MV03_FAULT Contact505(W454/418)가 공통 출력 가지를 제한. 이것은 MV03 경보 소유로 PC02 전용 fault로 재명명하지 않음 |
| 실제 복구 | 현재 조건 안정화, 경보 해제, 출력/실제 위치 및 후속 공정 정상 확인 자료 미확보. 소프트웨어 Reset핀이나 HMI 표시만으로 복구 완료 불가 |

고압/범위 오류 값은 선행 PSH02 초안과 고정 원본의 재사용 범위이며, 현재 보호값을 읽거나 변경하지 않았다. 안전 한계의 권고값을 생성하지 않는다. 오류값/강제값을 넣어 관찰하는 행동 시험도 수행하지 않았다.

## 6. 증상별 관찰·원인 배제 인계

아래는 승인된 별도 현장 절차에서 수집할 **관찰 항목**이다. 이번 작업에서 PLC 접속/강제/작동/보호값 변경을 요청하거나 수행한 기록은 없다.

| 증상 | 수집 위치·비교 근거 | 배제 경계·필요 증거 |
|---|---|---|
| PC02 숫자가 기대와 다름 | 같은 시각의 DB1W42/196, PSH02 raw/환산, Local Real 두 값, HMI 태그/단위/스케일 | raw IW/PIW, 정수환산/실수화, 레시피 편집 버퍼를 먼저 분리. 센서 교체 판단 금지 |
| Auto인데 MV03 명령이 없음 | 0479 OFF/en·COM_RST·LMNR, M14.4/5, 0344 PSH03/Err/Timer, 0345 Auto/Fault/처리리미트 | not used 제목으로 종료하지 않음. 호출·스캔/인터럽트·최종 Writer 자료 필요 |
| M14.4/5 값이 예상과 바뀜 | 두 Writer의 호출시점·현재 코드 일치·DB25·간접/통신 쓰기 | 두 경로 동시 존재를 우선 기록. 하나를 제거하거나 OFF 변경하지 않음 |
| PID 비트0인데 출력이 보임 | 0345 수동/Washing/Burner Startup/교정 입력 및 Q1.7/Q2.0 | 비PID 가지 존재와 소유를 분리. 그 자체로 비정상/오작동 확정 불가 |
| HMI 압력 정상인데 알람/동작 불일치 | HMI DB13 raw vs DB1 환산, OFR DB3X22.1, 고압 DB3X8.2, 타임스탬프 | 표시값·범위오류·고압·출력 fault 구분. 경보 해제≠재기동/현장 복구 |
| 방향이 예상과 다름 | Gain−4.0 인수, QLMNUP/DN, 0345 처리리미트와 실제 도면/밸브방향 | 이 백업 인수만으로 Gain 부호/현장배선/정상극성을 변경하지 않음 |

관찰기록에 관찰자, UTC/현장시간대, 장치·프로젝트/CPU 근거, 주소/값/단위/시각, 비교 원본, 원인 배제 결과, 승인된 조치와 독립 복구 증거가 필요하다. 0과 빈칸, 기존 note/repair_observation 미지필드·이전초안·타설비 키를 보존한다. 실제 운영기록/사진은 이 초안에 복제하지 않았다.

## 7. 완료·누락·다음 작업

| 영역 | 판정 | 이유 |
|---|---|---|
| 설비·자료 기준 | 적용, 초안 작성 | software 고유 ID/자료시점/실물 미확정 분리 |
| I/O·HMI | 적용, 일부 근거 미확보 | Local/Global·형식·주소·관련 HMI 확보; 이벤트·현행 스케일 누락 |
| 제어 | 적용, 정적 검토 | 0479 전체 핀·상류 선언·중복 쓰기·0345 소비; STL실행 본문·DB25·실제 호출 미확정 |
| 전기 | PC02 고유는 비해당, 관련자료 연결 | PSH02와 MV03의 회로 소유 보존; 실물 동일성 미확정 |
| 알람·복구 | 관련 영향 적용/직접 전용알람 근거 미확보 | COM_RST/PSH02/MV03 fault를 분리; 실제 복구 미확인 |
| 증상관찰 | 적용, 관찰표 작성 | 관찰을 위한 자료 목록이며 행동 시험 아님 |
| 완료기준 | 적용 | 문서·제품 기능·온라인·현장을 분리 |

### 네 기능과 검증 상태

도면·래더 비교는 관련 소유 링크와 핀표까지만 준비했고 제품 UI 연결은 미수행이다. 백업·선택 복원, 기록 전후 비교, 보고서/PDF 기능의 PC02 적용은 구현·저장·재읽기·재열기 증거가 없다. 이번 MD를 만들었다고 해당 네 기능 완료로 표시하지 않는다. 기존 브라우저 저장/미지필드/타설비 기록을 건드리지 않았다.

- documentation: draft_ready_with_gaps, 부모 독립 검토 대기.
- static_review: 고유 원본 XML 핀/선언·공유 원본 불변 확인, 본문의 범위에 한정. 제품 정적 검사/회귀는 not_run.
- ui_records: not_run. publication: not_published_by_this_task.
- tia_compile/live_cpu/field_recovery: not_performed.
- 원본 생성기·빌드·시뮬레이터·PLC 실행0, 사용자 Mac/새 Work/재위임0.

다음 한 작업은 부모가 PC02의 NID11→12 Local 결속 및 0479/0344 중복 Writer/0345 소비를 독립 대조하는 것이다. 이후 새 권한과 실제 자료가 제공될 때만 현행 OB/DB25·원시 STL·전체 Writer·HMI 이벤트·현장 동일성을 별도 확인한다. 없는 현장 자료를 기다리며 동일 보류를 반복 조사하지 않는다.

### 단계 실제시각과 검증 산출

- 2026-10-11 10:39:52 UTC: 공통 지시·scope·원본 지침 읽기 시작.
- 2026-10-11 10:40:51 UTC: PC02 선언/0479/0344/0345 추출 및 `_7ex` doc14/15 대조 저장.
- 2026-10-11 10:41:07 UTC: 부모에게 상류 데이터 결속 및 중복 쓰기 핵심 보고.
- 나머지 실제 검증/완료 시각은 아래 검사 산출 시각 및 `extracts/PC02/stages.json`에 기록한다. 소요시간을 추정하여 기입하지 않는다.

추출: `0479-refs.json`, `0479-wires.txt`, `0344-refs.json`, `0344-wires.txt`, `0345-refs.json`, `0345-wires.txt`, `declarations-selected.json`, `live-index-cycle.json`. 검사/해시: `static-review.json`, `source-hashes.json`, `shared-source-verification.json`. 검색 전역 후보는 참조 결속 확정본이 아니며, 위 블록문맥/충돌 제외 경계를 함께 읽는다.

검증 실제시각: 2026-10-11T10:46:54.809134+00:00. 원본 연결/자료형/핀 단언 19개 passed. 원본/맥락/보존 76파일은 아래 SHA256와 고정 Git blob 바이트 일치. 중지5자산 freeze 해시 일치, 공유 PSH02 67파일 이전 해시 일치, 원본 Git 변경0. 원본 제품시험은 실행하지 않았다.

## 전체 해시표 — 이 초안의 원본·공유 문맥·보존 파일

각 행의 SHA256는 작업 파일과 고정 Git blob의 SHA256가 모두 같은 값이다. Git blob OID는 SHA256와 다른 Git 객체 식별자다. 중지5자산 및 백업 컨테이너는 보존 검사이며 의미/동작 검토가 아니다.

| 원본 상대경로 | SHA256 (파일=고정 blob) | Git blob OID |
|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | `653d27572de6beedcf3eb6c95702bb119a8b567f` |
| `all-in-one/sources/decoded-original/0032-FlgNet.xml` | `070bb8efa33d03b18add5da81d3f670a47c12b288076b7bfee11ac87fe6fa7e4` | `e31cf9aeecfbfc0c264921ac217cbd15479c1f34` |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` |
| `all-in-one/sources/decoded-original/0062-IdentXmlPart.xml` | `34f188168dc4fad0d6e2c813028045f37b84025636bcebd8aa1c7ffb4cfd9bcd` | `624eed3ba6cd1eb54e7e3f316f8c4c159ca3b4b5` |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` | `3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3` |
| `all-in-one/sources/decoded-original/0151-FlgNet.xml` | `227627d165c6240a4c15b62fd4e4c8d7a621c15f35319cb424601df5cc52c904` | `8e8a9801d1f57180fc3747f6515c0353f38f7dc5` |
| `all-in-one/sources/decoded-original/0152-FlgNet.xml` | `2b6165460f06a52de56afcb4d65ed163d64320e24af1b194e934a4d7c6bfe49f` | `dd8e35b98043d9d0f230351352273eac1d783990` |
| `all-in-one/sources/decoded-original/0153-FlgNet.xml` | `3d3a236a66a7a5c9b8e2d1e15da63cc943ba5cd266949583cbac6ffbb2f88bc6` | `d50223c45f5eb1d1c1d3530b41db1e79ad6c71f3` |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` |
| `all-in-one/sources/decoded-original/0344-FlgNet.xml` | `08eabc412b9457eb615d1cb01b92682987bef170cbeab78070dd4c705ab93576` | `76eef5bbbbee10b7ac3494d736b453b9a8120d42` |
| `all-in-one/sources/decoded-original/0345-FlgNet.xml` | `b278a319d4d8cb8d157f449a2365445ff8f172245ebd2a468aa3ee79dba60f93` | `25656c8d9f39b8eccb67300905545b4cbcec2bfd` |
| `all-in-one/sources/decoded-original/0347-FlgNet.xml` | `092aa32263fce728afde49d5fff0dddb6cc1445c6f71e4fb45956129beda4d6d` | `81a970037cf8bb628c67b61185635e2ae0f574c6` |
| `all-in-one/sources/decoded-original/0348-FlgNet.xml` | `00570dd8c0945f04304c8820b8e3d7294916aa04aaa1158d1c630062961bbedf` | `77338b9dbe0ffd938a992311c55bc07b7f4eaed0` |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` |
| `all-in-one/sources/decoded-original/0479-FlgNet.xml` | `112e55599a4dc705438c8c61b936da9a167c22d9bbd909eda11c45c9dc33e839` | `38df067a2f4f62edfba9c5027002feccb45e5142` |
| `all-in-one/sources/decoded-original/0496-FlgNet.xml` | `9a5c816b27efc2afbe84a170b1f80959c4992829d10eaa55f6bd18f28030808a` | `afe8556ec23887983b4ed5d75e259647374bf1b3` |
| `all-in-one/sources/decoded-original/0537-FlgNet.xml` | `a616e375d6b27b2fe3406838574f75a811357ac0a2a50c949e51201e3d9b5115` | `50169469a1ef3d65bd10c6d2f2a38f522ec7447a` |
| `all-in-one/sources/decoded-original/0554-IdentXmlPart.xml` | `4ae3e7d0bca0f78c9e94617abeb70bdd228d85d74bff2224174fa1bb0076e78c` | `cdb68b35a7287f6b5636c01ea3a01747d3d60e81` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` |
| `all-in-one/sources/decoded-original/0564-IdentXmlPart.xml` | `2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1` | `c4b1f2cb191970cfce1cce59cb290a9f1f934c37` |
| `all-in-one/sources/decoded-original/0565-IdentXmlPart.xml` | `0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149` | `c2e3e2d57c94c5da864f6e172f0a7a925da942d6` |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | `9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e` |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | `11f0502c84a1f319a21459a35c0dc1c6ce8e8f36` |
| `all-in-one/sources/decoded-original/0620-IdentXmlPart.xml` | `da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3` | `dc88b5e87ad3331928f14fcf647673a26fb70b6b` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` |
| `all-in-one/sources/decoded-original/0631-IdentXmlPart.xml` | `8e5072374f8ef098de72fbf93965b2a7bb0965c0f803e397daa68588c0c38555` | `27aa5aef2b126820b4658362e4aad5ca6d709fee` |
| `all-in-one/sources/decoded-original/0642-IdentXmlPart.xml` | `c922483c261c8ddb98c239a7b4dc3d7f73f9a45261dd5b4d669f39d6918a1c21` | `398f73b99c4a792a68387485fcb47048d166b2a1` |
| `all-in-one/sources/decoded-original/0665-IdentXmlPart.xml` | `50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd` | `ea4a8a5013081f648722c5ebbde3bb1366787990` |
| `all-in-one/sources/decoded-original/0666-IdentXmlPart.xml` | `19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6` | `b6130b32498b6fee0d9e4db7a04dc79f785e1fbb` |
| `all-in-one/sources/decoded-original/0667-IdentXmlPart.xml` | `ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3` | `7f2e1798eb9f260d19d038a83369484d0f438856` |
| `all-in-one/sources/decoded-original/0668-IdentXmlPart.xml` | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` | `fe0f30d1eaae37783b0f03cb090353b3a3de3600` |
| `all-in-one/sources/decoded-original/0669-IdentXmlPart.xml` | `754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2` | `f5bf8f3c41d2a07ba9dcfd8f400548be8cf51cd3` |
| `all-in-one/sources/decoded-original/0670-IdentXmlPart.xml` | `e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841` | `b9466007b14e5c4f5d353dca5734401317e2dc03` |
| `all-in-one/sources/decoded-original/0671-IdentXmlPart.xml` | `26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293` | `e38a4e2c93ac8093e2b0b8e082a64688b5d9845e` |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` |
| `all-in-one/sources/decoded-original/0683-IdentXmlPart.xml` | `0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22` | `662acdb9a06c0ba1c0027e7dd215a28f07d3f02b` |
| `all-in-one/sources/decoded-original/0684-IdentXmlPart.xml` | `6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208` | `d67b98b5d5516e0330aae5cfdbee41a3e09206e1` |
| `all-in-one/sources/decoded-original/0685-IdentXmlPart.xml` | `2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448` | `86bda988d9efedba92ba2f3e4877497d9eb5230a` |
| `all-in-one/sources/decoded-original/0686-IdentXmlPart.xml` | `b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4` | `8c152d926692a8e15973c980e08e338d29411814` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |
