# SC10 BF01 분진 스크루 원본 조사 초안

SC10은 문서상 BF01 하부의 분진을 VR04로 이송하는 스크루다. 고정 PLC 백업에는 운전요청 `Flag.M_SC_10`, 출력 `%Q4.0`, 원시 피드백 `%I5.0`, 처리 응답 `DB13.DBX5.0`, 고장 `DB3.DBX2.2`가 구분되어 있다. 고장감시는 `Tag_72=%T81`, 원문 `S5T#2S`다. **접촉기 응답은 실제 스크루 회전·분진 이송 완료의 증거가 아니다.**

본 문서는 작업3 추가조사의 세 번째 5개 묶음 중 SC10 한 설비의 cloud 조사 초안이다. 로컬 2차133 통합·게시, UI/기록 지원 완료, TIA 컴파일, 현재 CPU·현장 복구를 뜻하지 않는다. 실제 PLC·보호 설정·SEJIN 운영자료를 변경하지 않았고, 시뮬레이터 작성·수정·생성·실행·행동 시험을 하지 않았다.

## 작업 기준·범위·보존

- 표준: GME-STD-1.0.0. 저장소 AGENTS, gme-equipment-rollout 스킬, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY와 최신 인계 파일을 읽었다.
- 고정 읽기 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 조사 시작 Git 변경 0.
- 대상: catalog SC10, motor, 집진·석회, parent 빈값, depth0, aliases 빈목록, priority_key 없음. 원본 INVENTORY catalog[100], equipment[46]. BF01이라는 이름을 근거로 catalog parent를 변경하지 않는다.
- 범위 검토: TASK3-BATCH03-SCOPE에서 `other_research_target`, 중복·기존 제외·부모보류 해당 없음, 현재 실물 동일성 미확인. 우선18/제외90/보류7/phase2 후보133의 집계는 변경하지 않는다.
- 읽기 전용 preflight: `--repo source-mv06` 종료0, inventory_matches=true (`--emit-json` 파생 대장 출력은 별도로 보관). `requirements-audit.json`, `all-in-one-data.json`의 기준 대비 바이트 변경만 표시되며 대장 대응은 일치한다. 처음 `--root` 잘못된 인자를 사용한 호출은 종료2였고 올바른 읽기 전용 인자로 재실행했다.
- 쓰기 허용 범위: 본 `drafts/SC10-DOTS-DRAFT.md`와 `extracts/SC10/`만. 공유 선언·helper·원본·버전·대장·배포·운영기록 편집 없음.
- 조사일: 2026-10-11 UTC. 작성자: SC10 원본 조사자. 실제 모델명/추론 수준을 확인하는 런타임 근거는 미확인. 자체 원본 대조 후 부모의 별도 검토 대기.
- 아래 경로는 별도 표기가 없으면 고정 저장소의 `all-in-one/sources/decoded-original/` 기준이다. `network-map.json`, `live_index.json`, `control-spec.json`은 탐색용 파생 자료로 구분하고 핵심식은 XML/선언/핀을 다시 대조했다.

## 7영역 적용표

| 영역 | 상태 | 확보 근거 | 남은 범위 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | BF01–SC10/M34–VR04/M38, catalog 독립 ID, 자료 판본 | 현장 배치·명판·현재 설치 동일성 |
| I/O·HMI | 적용, 일부 근거 미확보 | I5.0/Q4.0, DB2/3/13, HMI3행·고유 호출핀 | HMI 데이터 ORef4개 결속·실제 버튼 이벤트 |
| 제어 구조 | 적용 | LAD1962/1807/1843/1844, startup Word덮어쓰기, 입력·출력 Word전달 | 현재 TIA 호출/스캔/유지속성·전체 교차참조 |
| 전기 전달 경로 | 적용 | FG57/121/140/253, 시공47/51, P&ID 렌더 | 현행 배선·단자·정상극성·보호 설정 |
| 알람·복구 | 적용 | SC10 2초 Set/Reset, VR04 허가, FN04 공유90분 | 실제 원인해소·재요청·복구 기록 |
| 증상별 수리 | 적용, 관찰계획 | 원시·처리·명령·접촉기·실제 이송 비교 | 실제 현장 관찰/수리/시험 없음 |
| 완료 기준 | 적용 | 기능/상태표·미확정 목록·인계 | 통합/UI/기록/게시/TIA/CPU/현장 별도 |

## 1. 설비와 소유 경계

1. equipment.json은 SC10을 `BF01 분진 스크루`, FG57, parent 빈값으로 기록한다. P&ID `PID_1684n002I.pdf` p1 실제 렌더에서 BF-01 하부 SC-10/M34(3 kW 440 V)와 출구 VR-04/M38(0.55 kW 440 V)을 구분했다. 기계적 관계와 catalog 부모 관계는 별도다.
2. `Electrical_Rev2.pdf` FG57/PDF58의 M34 SC-10은 `FILTER DUST SCREW`, 3 kW/5.8 A, 440 V 60 Hz 삼상 전력 경로다. 57QM1–57KM1–57QS1의 직접기동 회로이며, 해당 직접 회로에 전용 VFD·속도 설정·PID·엔코더·아날로그 전류 경로는 식별되지 않았다. 이 회로 설명에서 해당 기능은 비해당이며, 현장 장비의 부재까지 단정하지 않는다.
3. VR04 처리 Run은 SC10 요청 Reset 조건에 참여한다. VR04 자체 출력·모터·고장·보호값을 SC10에 병합하지 않는다. BF01 본체·DP01·세척 EV군·공기계통도 SC10 전용 소유가 아니다.
4. SC10 처리응답은 BF01 세척허가와 FN04 공유 예고장에 기여한다. 이것은 SC10이 BF01의 모든 세척 기능 또는 FN04의 90분 타이머를 소유한다는 뜻이 아니다.
5. 원본의 문서 시점: 전기 FG57/121/140/253 기본 날짜27.05.2024, 해당 검토 시트에 개별 Rev2 표시는 보이지 않았다. 파일명 Rev2를 모든 시트의 개정으로 확대하지 않는다. P&ID는 1684n002 판 I, 기본 날짜06/04/2011, I개정15/01/2013(`REMOVED MC-05, CHANGED POWER OF FN-02`)의 과거 설계 자료다. 시공도는 24.11.11 `first draft design`, CHECKED/APPROVED 공란이다. 승인 준공도·현재 설치를 증명하지 않는다.

## 2. I/O·내부 메모리·HMI

### 2.1 신호 대응

| 신호 | 형식·정적 주소 | 원본 위치·선언 | 해석·한계 |
|---|---|---|---|
| SC-10_Fbk | Bool %I5.0 | live_index doc511; `0613` SimpleAccess RID236 NID39 UID2152, Input AO40; `0594` RID62 NID6 UID572/578 | 57KM1 보조접점의 원시 응답. 실제 축/이송 센서가 아님 |
| Start SC10 | Bool %Q4.0 | doc1312; `0602` RID159 NID32 UID927 AK Write, Output AO32; `0658` RID118 UID1000 | 직접 출력 Coil. doc1312 주석의 `a 52.2`는 현재 Address Q4.0 및 FG57/140과 별도인 과거 설명 |
| Flag.M_SC_10 | Bool DB2.DBX2.2 | `0604` RID158 AO/BO18 NID32 UID925 Write/926 Read; `0577` RID24 UID604/948 Write; `0603` Flag TOD N2 | 요청 비트. 출력·피드백과 분리, startup Word 쓰기와 겹침 |
| Allarm.SC_10_FAULT | Bool DB3.DBX2.2 | `0657` RID121 AO/BO18 NID29 UID1005/1008 Write, UID1007 Read; `0603` Allarm TOD N3 | 유지 고장. HMI DB11 표시주소와 다름, startup DB3W2와 겹침 |
| Inputs.FEEDBACKMOTOR SC-10 | Bool DB13.DBX5.0 | `0657` RID296 AO/BO40 NID29 UID1037; `0604` RID254; `0628` Inputs TOD N13 | 처리 응답. 원시 I5.0와 주소영역/Writer가 다름 |
| Inputs.VR04 Run | Bool DB13.DBX5.5 | `0604` RID220 AO/BO45 NID32 UID23, NID34 UID996 | 별도 VR04 처리 응답, SC10 Reset 조건 |
| Tag_72 | Timer %T81 | doc1311; `0658` RID119 Timer AO81 NID29 UID1002 Write/1003 Read | SC10 2초 S5 타이머, HMI 태그 아님 |
| ON / OFF | Bool %M0.0 / %M0.1 | docs1556/1552; `0602` RID1/33, `0594` RID52/1 | 이름으로 항상1/0이나 실제 운전모드를 가정하지 않음 |
| UNDER TESTING | Bool %M5.5 | doc1906; `0602` RID4 AO45 NID32 UID924 | VR04 Run 부재 Reset 분기의 부정 접점. 변경·우회 지시 아님 |
| SC_10_MIN / SC_10_HOUR | Int DB9.DBW152 / DB9.DBW154 | `0615` RID238 BO1216 / RID240 BO1232; `0614` hours motors TOD N9 | 시간 관련 저장부. HOUR는 Add가 아닌 Move1 경로 존재 |
| BF01_RUN | Bool %M180.3 | doc902; `0594` RID341 AO1443 NID29 UID75 | BF01 세척허가에서 파생하는 메모리, SC10 실물 운전센서 아님 |

주소는 선언의 SAD 영역, SSD/AO·BO 비트 오프셋, DepDBBlock TOD N을 대조한 정적 대응이다. 현재 CPU의 최적화·주소 유지·값은 확인하지 않았다.

### 2.2 원시→처리 입력 Word 경로

LAD1070 `0397-FlgNet.xml`, NID1의 Part35 Move는 `Tag_180` ORef36/RID10 → ORef37/RID11로 전달한다. W39=in, W40=out1. `0627` RID10 Word/Input AO32는 %IW4이며, `0629` RID11 Word AO32/BAD BIRID4와 `0628` Inputs DB13 선언은 DB13.DBW4다. 따라서 I4.0~I5.7 전체 Word에 속하는 **I5.0→DB13.DBX5.0** 대응이며, SC10만을 위한 단독 Bool Move가 아니다.

Part35.en은 Part27.eno/W41에서, Part27.en은 Part22.eno/W34에서 온다. 모두 DisableENO=true 속성을 포함한다. 호출과 선행 ENO가 유효하다는 가정 없이 ‘항상 복사’라고 쓰지 않는다. main LAD1613 `0030`은 Recipes Handler CRef21 → HMI CRef23 → HMI Output CRef25의 ENO 연쇄 후, Part37 `NOT Simulation(1)`을 통해 HMI Inputs CRef28.en/W43을 허가한다. CodeBlock UID24/29, `0688` RID124/135, `0692` RID140 NID19 UID45를 대조했다.

기존 원본 simulation 블록 LAD1085 `0405`에는 처리응답의 다른 Writer Part41 Coil/ORef42 RID124가 남아 있다(`0635`, NID4, AK Write). 요청 ORef38/RID138을 읽는다. **기존 백업에 다른 Writer가 있다는 읽기 전용 확인만 했으며 작성·수정·생성·실행·행동 시험은 하지 않았다.** 해당 Writer의 현재 활성 여부는 미확정이다.

### 2.3 출력 Word 미러 경로

LAD356 `0401-FlgNet.xml` NID1은 물리 출력 Word를 DB14에 미러한다. SC10 Q4.0을 포함하는 `Tag_282=%QW4`는 `0632` RID30 Output AO32, ORef37이다. Part24.in/W62→Part24.out1/W63→ORef38/RID51(`0633`, Word AO32, BAD26)→DB14.DBW4(`0064` DepDBBlock Output RID26/TOD N14)이다. Part24.en은 Part23.eno/W60이며 DisableENO=true이다.

이 경로는 Q4.0의 추가 Writer가 아니라 **QW4를 읽어 DB14W4를 쓰는 출력 미러**다. DB14의 관찰값·HMI DB11 표시값·Q4.0 현재값을 같은 순간의 동일 증거로 간주하지 않는다. 실제 호출·갱신시각은 별도 확인해야 한다.

### 2.4 HMI3행과 미결속 핀

`hmi_plc_tags.csv`에는 Access Name PLC, `dde.cfg 설정; 온라인 현재값 아님`인 SC10 직접3행이 있다.

| CSV 행 | HMI 이름 | 설정 주소 | 내부 ID |
|---|---|---|---|
| 126 | SC_10\Allarme1 | DB11,X52.1 | 0033A |
| 414 | SC_10\RispostaA | DB11,X52.0 | 001BD |
| 449 | SC_10\Flag | DB2,X2.2 | 00195 |

LAD1203 `0379-FlgNet.xml`은 CRef22/RID638, CodeBlock23/RID1의 HMI Standard Motors 호출이다. `0623/0624` 호출 선언 및 원본 핀을 대조했지만 원 네트워크 NID는 미확정이며 파생색인도 데이터 피연산자 0/8 해석 상태다.

| Wire | 원본 핀 | 원본 ORef/RID | 결속 상태 |
|---|---|---|---|
|21|Powerrail→CRef22.en|해당 없음|연결 확인|
|37|Ingresso_run|24/665|doc1203 검색문자열은 Inputs.FEEDBACKMOTOR SC-10 후보, 선언 결속 미확보|
|39|Allarme1|26/331|Allarm.SC_10_FAULT 후보, 선언 결속 미확보|
|40~43|Allarme2/3/4/5|27/28/29/30, RID48|0626 FALSE 선언과 관련 NID호출군 존재, SC10 원 NID 확정은 별도|
|46|Risposta|33/334|Motors.sc10.risposta 후보, 선언 결속 미확보|
|48|Comulativo_allarmi|35/336|Motors.sc10.allarme_comulativo 후보, 선언 결속 미확보|

RID 또는 UID만 같은 다른 블록 선언을 결속하지 않았다. HMI 요청주소 DB2,X2.2는 요청 Bool 주소와 맞지만 버튼의 누름/놓음·토글·직접쓰기·권한을 증명하지 않는다. DB11,X52.1을 DB3.DBX2.2의 직접 주소로 바꾸지 않는다. HMI 원 프로젝트, 실제 창/스크립트·알람 목록·통신 상태가 필요하다.

## 3. 제어 구조·호출·다른 쓰기

### 3.1 SC10 요청 Reset과 출력

LAD1962 `0262-FlgNet.xml`, NID32:

- ON Part940→FAULT Part942→OR911.in1(W943).
- ON Part940→NOT VR04_Run Part22→NOT UNDER_TESTING Part946→OR911.in2(W24/947).
- OR911.out/W933→RCoil916.in, operand W935→ORef925/RID158 M_SC_10.
- ON Part940→M_SC_10 Part948→Coil920.in/W949, operand W938→ORef927/RID159 Start SC10.
- 공통 분기 W941, 요청 접점 operand W936; 선언 `0602` ON ORef921/RID1, UNDER TESTING924/RID4, Start927/RID159; `0604` FAULT922/RID156, VR04 Run23/RID220, 요청925/926 RID158.

정적식은 `Reset M_SC_10 = (ON AND SC_10_FAULT) OR (ON AND NOT VR04_Run AND NOT UNDER_TESTING)`, `Start_SC10 Coil = ON AND M_SC_10`이다. VR04 조건을 출력 앞의 직접 직렬 접점으로 바꾸면 원본 Reset/출력 구조가 달라진다. UNDER TESTING은 자체 SC10 고장 Reset을 면제하지 않는다. 실제 스캔 결과·동시 쓰기 우선순위·안전회로 전체를 이 네트워크만으로 확정하지 않는다.

### 3.2 자동 Set 두 경로와 비교 카운트

| 원본 | SC10 고유 대상 | 핀으로 확인한 조건 |
|---|---|---|
| LAD1843 `0164`, NID3 | SCoil434→ORef604/RID24 M_SC_10, operand W690 | ON785 AND NOT Emergency_module_fault22 AND Tipo_preset=1(Eq400) AND Auto_ON1_823 AND Tempo_presetting=5(Eq428) |
| LAD1844 `0165`, NID4 | SCoil771→ORef948/RID24 M_SC_10, operand W1039 | ON1145 AND NOT Emergency_module_fault1154 AND Auto_ON1_1147 AND Tipo_preset=2(Eq737) AND Tempo_presetting=6(Eq765) |

1843의 Eq428 입력은 ORef601/Data.Tempo_presetting W686, ORef602/RID22/상수5 W687이다. W688이 SC01/SC10/SC11 세 Set 입력으로 분기한다. 1844는 ORef945/Tempo W1035와 ORef946/RID79/상수6 W1036, 공통 W1037이다. `0577` RID24는 NID3 UID604와 NID4 UID948를 모두 AK Write로 명시한다. 같은 공유 네트워크에서도 SC10 대상 핀을 따로 추적했다.

LAD1841 `0162`의 Tempo_presetting Add1/NOT Auto_ON1 Move0, LAD1723 `0024` ON Part188→CRef183.en/CodeBlock186 RID39 Auto start motors(`0067`)를 확인했다. 블록 제목은 cyclic interrupt 1 second다. 5/6은 원문의 비교 카운트이며 현재 CPU에서 실제 5초/6초 경과를 측정한 결과가 아니다.

### 3.3 startup Word 덮어쓰기

SC10의 요청·고장 이름만 검색하면 아래 다른 쓰기가 빠진다.

| 원본 | 명령·Wire | 선언·겹침 |
|---|---|---|
| LAD402 `0147`, NID2 | ON208→Move138.en/W209→Move138.eno/W187→Move141.en. INT#0 ORef170/RID54→Move141.in/W188; Move141.out1/W189→ORef171/RID9 | `0048` 상수 Int V0, `0563` RID9 Word AO16/BAD6, `0562` RID6 Flag TOD N2. DB2.DBW2=0이 DB2.DBX2.2 M_SC_10을 포함 |
| LAD403 `0148`, 선언 NID3 | ON329→Move250.en/W330→Move250.eno/W306→Move253.en. INT#0 ORef287/RID54→Move253.in/W307; Move253.out1/W308→ORef288/RID26 | `0048` NID3 UID287, `0563` RID26 Word AO16/BAD23, `0562` RID23 Allarm TOD N3. DB3.DBW2=0이 DB3.DBX2.2 SC_10_FAULT를 포함 |

DBW2는 byte2~3의16비트다. 두 Word 쓰기는 SC10 전용 Reset이 아니며 다른 설비 비트도 함께 포함한다. LAD403 파생 network-map은 NID 투표 충돌로 inferred_original_nid=null이다. 여기서 NID3은 블록 문맥과 `0047` ON UID284, `0048` 상수 UID285/287, `0563` 쓰기 UID286/288 등 선언들의 일치로 추적한 것으로, 다른 블록 NID4/UID284를 가져오지 않았다.

live_index doc302는 ob_startup=100, doc398은 `startup only`, event startup, `power up - start up`으로 기록한다. 이는 백업의 OB 분류이며 현재 CPU 기동·재시작·호출 활성·유지성은 확인하지 않았다. ‘전원 복귀 때 반드시 현재 SC10 상태가 이 값’이라고 결론 내리지 않는다.

### 3.4 호출과 Writer 정리

- main LAD1619 `0031`: ON 아래 Allarms1 CRef264/CodeBlock275/RID58 호출(`0688`, NID6).
- main LAD1620 `0549`: ON Part350.out/W351이 Motors1 CRef319, Filter CRef322, time work motor CRef334.en 등에 분기한다. CodeBlock337/RID67,339/RID70,347/RID82(`0688`, NID7).
- SC10 요청의 확인된 Writer: 자동 Set2개, LAD1962 RCoil1개, startup DB2W2 덮어쓰기. HMI DB2X2.2 설정주소도 별도로 존재하나 실제 이벤트 미확보.
- SC10 고장 Writer: LAD1807 S/R 두 개와 startup DB3W2 덮어쓰기. 처리피드백 Writer: IW4→DB13W4 및 기존 simulation 원본의 Bool Writer. HOUR Writer: LAD1037 Move1와 LAD1052 Move0.
- Q4.0 직접 Coil과 QW4→DB14W4 읽기 미러를 혼동하지 않는다. 이 조사 범위 밖의 간접 DB/포인터/외부 통신 쓰기를 모두 배제했다는 뜻은 아니다.
- main 정적 나열, cyclic interrupt, startup, HMI의 서로 다른 문맥을 한 연속 실행으로 간주하지 않는다. 전체 Writer 우선순위와 ENO·리텐션은 현행 TIA 교차참조가 필요하다.

### 3.5 운전시간의 원문 특이점

LAD1037 `0324`, NID39: Tag_47 Part2180 AND 원시 SC-10_Fbk Part2182→W2183에서 Add2134.en 및 Ge2141.pre로 분기한다. Add 입력 MIN ORef2153/RID238, 상수1 ORef2154/RID7, 결과 MIN ORef2155(W2165/2166/2167). Ge2141은 MIN ORef2156>=60 ORef2157/RID8(W2168/2169).

Ge.out/W2170→Move2144는 상수1 ORef2158/RID7(`0616`, V1)을 HOUR ORef2159/RID240에 쓴다(W2172/2173). **HOUR+=1이 아니다.** 이어 eno/W2174→Move2147가 상수0 ORef2160을 MIN ORef2161로 쓰고(W2175/2176), eno/W2177→SCoil2150 Flag_Aggiorna_DB ORef2162(W2178)이다.

LAD1052 `0339`, NID54: Tag_48 Part3049→Move3008→3011→3014의 ENO연쇄(W3050/3037/3040) 뒤 W3043→Move3017.en, 상수0 ORef3030/RID12(W3044)→HOUR ORef3031/RID240(W3045). `0613` Tag_47=%T13, Tag_48=%T17, `0616` 상수형식을 확인했다. LAD1056 `0019`에는 Tag_47 S5T#1M 생성 경로가 있다. Move1을 오류라고 수정하지 않았으며 누적 수신부·초기화 정책·리텐션을 확인하기 전 실제 총 운전시간으로 확정하지 않는다.

## 4. 전기 전달 경로·실제 PDF 확인

### 4.1 페이지와 판본

| 원본 | 실제 PDF 페이지 | 렌더에서 확인한 내용 |
|---|---:|---|
| Electrical_Rev2 FG57 |58|M34/57QM1/KM1/QS1, A4.0/E5.0, 전력·코일·응답 |
| Electrical_Rev2 FG121 |122|E5.0 CPU515/MOD9/단자11, 57/6 참조 |
| Electrical_Rev2 FG140 |141|A4.0 CPU515/MOD15/단자1, 57/4 참조 |
| Electrical_Rev2 FG253 |256|57KM1·57QM1 BOM, 전기 시트와 별도 FG/PDF 오프셋 |
| Can Decoating CANDC-CONS-E030-047 |47/64|DUST ZONE13, 223 RA 경로, M34 Pipe16, 1_29 케이블 |
| Can Decoating CANDC-CONS-C001-051 |51/64|CR→SC-10/M34 전력케이블 1_29 행 |
| P&ID 1684n002 판 I |1|BF01 하부 SC10/M34→VR04/M38; 별도 확대 렌더 |

전기4쪽·시공2쪽·P&ID1쪽의 **7개 원본 페이지를 실제 렌더로 확인**했다. 확대 렌더는 페이지 수에 추가하지 않는다. 전기 4쪽 모두 기본 날짜27.05.2024이고 검토 부분에 개별 Rev2 표시는 없다. P&ID/시공도와 전기 원본은 시점이 다른 문서이며 승인 준공 상태는 미확인이다.

### 4.2 전력·보호·케이블 양끝

FG57: 8.3L1/L2/L3(이전56/9, 다음58/0, 440V60Hz)→57QM1 주접점1–2/3–4/5–6→57KM1 주접점1–2/3–4/5–6→57U1/V1/W1→XM의 같은 선명→57QS1 주접점1–2/3–4/5–6→M34 U/V/W 및 PE→SC10.

- 패널 내부 배선 표기는 BLACK FS17 1.5 mm²다. M34 3 kW/5.8 A와 57QM1 5.5–8 A는 원본 표기다. 5.5–8 A는 보호기 범위이며 현재 트립 설정이 아니다.
- 시공 PDF51의 행1_29: `=DUS+SC10-M34A`, FROM CR, TO SC-10/M34, FILTER DUST SCREW, GAC, CV4심×1.5, spare0. 경로100→200→220→221→223 RA→E200, Adjustment8, LEN99. 표의 LEN을 현장 실측이나 확인된 단위로 바꾸지 않는다.
- 시공 PDF47: DUST ZONE13, 223 RA의 EMBEDDED CP No.2/Pipe16→M34, 케이블1_29= DUS+SC10-M34A, CV1.5/4. 인접 No.3/M38은 VR04이며 SC10 배선에 합치지 않는다.
- CV 외부 케이블과 FS17 내부선을 같은 케이블로 합치지 않는다. CR 단자대와 M34 현장 단자까지의 심선별 준공표는 미확보다.

### 4.3 명령 전달·접촉기

LAD1962 Coil920→%Q4.0→FG140 CPU515 MOD15 단자1/A4.0→FG57 참조140/1→XS51→57QS1 보조접점→XS52→선57.1→57QM1 보조접점→57KM1 코일 A1, A2→-0Vdc10.6.

57QS1/QM1 보조접점의 현장 단자번호는 이 시트에서 확정하지 못했다. 그림에 없는 접점번호를 채우지 않는다. FG140의 +24Vdc10.9→X21/3032 퓨즈5×20,4A F→선140.1/단자9 공급과 단자10/-0Vdc10.6을 별도 기록한다. 4A를 모터 과부하 설정으로 쓰지 않는다. Q4.0=1만으로 접점 상태·코일 전압·실제 흡입을 확정하지 않는다.

### 4.4 피드백 전달

FG57 +24Vdc10.7→57KM1 보조접점13–14→E5.0(참조121/2)→FG121 E5.0 CPU515 MOD9 단자11(참조57/6)→%I5.0→LAD1070 IW4→DB13W4→DB13.DBX5.0 처리 응답→SC10 고장감시/공유 기능.

도면의 접점 기호가 현재 실물 정상극성·접점 상태를 확인한 증거는 아니다. 현재 배선 NO/NC·입력 정상값은 명판·현행 도면·승인된 현장 관찰이 필요하다.

### 4.5 BOM 원문과 현재 실물 구분

FG253/PDF256의 57KM1은 Siemens `3RT2015-1BB41`(3 kW,1L,DC24V,S00 VT), RC element `3RT2916-1CB00`이다. 57QM1은 Siemens `3RV2901-1E` 보조접점, `3RA1921-1DA00` 결합부, Whoner 표기의 `WR32433` 어댑터, Siemens `3RV2011-1HA10`(MAGNETOTHERMIC S00,5.5–8A,VT)이다.

원본 BOM 기록일 뿐 현행 설치모델·교체품 호환성·보호 설정·토크·정비 주기는 미확인이다. SC01 등 다른 설비 BOM 값을 이름만 바꿔 작성하지 않았다. 외부 제조사 최신 사양을 조사해 현장 모델로 단정하는 작업은 하지 않았다.

## 5. 알람·복구 및 공유 기능

### 5.1 SC10 고장 Set/Reset

LAD1807 `0441`, NID29:

| 동작 | 고유 Part·피연산자 | 정적 조건·Wire |
|---|---|---|
| 2초 감시 | SdCoil987, Tag_72 ORef1002/RID119 | ON1023 AND Start1025 AND NOT 처리응답1036. W1024/1026 분기, 반전 operand W1039, timer.in W21, value W1011, timer operand W1012 |
| 고장 Set | SCoil993, FAULT ORef1005/RID121 | ON1023 AND Start1025 AND Tag_72 접점1027. operand W1013, Set.in W22, Set operand W1016 |
| 고장 Reset | RCoil998, FAULT ORef1008/RID121 | ON1023 AND RESET_ALLARM1031 AND FAULT1033. W1018/1032/1019/1034/1021 |

`0656` LiteralConstant RID28 NID29 UID1001은 S5Time, `SV=S5T_x0023_2S`, V512다. **원문 S5T#2S를 보존하며 512ms로 해석하지 않는다.** `0658` Timer AO81과 doc1311이 %T81이다.

고장 Set은 LAD1962의 요청 Reset으로 연결된다. 고장 Reset 식에는 처리피드백 정상 확인 접점이 없으므로 알람해제만으로 원인해소·허가복귀·재기동을 선언하지 않는다. 실제 만료시간·반복호출·리텐션·다른 Reset 우선순위는 현재 CPU에서 미확인이다.

### 5.2 FN04 공유 예고장·90분 정지 경계

LAD1964 `0264`, NID34: ON1020 AND Inputs.FN04 Run1022 아래, SC01_응답1024/VR03_Run1026/**SC10_응답1028**/VR04_Run1030/SC11_응답1032/VR05_Run1034가 각각 부정 접점인6분기 OR972로 합쳐진다. SC10의 ORef995/RID254(`0604`)가 Part1028.operand다.

OR972.out/W1012는 Coil982 Allarm.Prealarms_FN04(ORef999), SdCoil985 Tag_126(ORef1001), Tag_126 접점1036의 입력으로 갈라진다. `0606` RID112 NID34 UID1000, S5Time SV=S5T#1H_30M/V13632; `0602` RID169 Timer AO131이 %T131이다. 접점1036→Coil990 local Stop_Fan_FN04 ORef1003/RID170(`0605` Local BO3). 다음 LAD1965 `0265`는 그 local 비트를 Part1042/ORef1019로 읽어 OR1003→RCoil1010→M_FN_04 ORef1021로 연결한다.

90분은 FN04 공유 경로이며 SC10 고장지연2초와 구분한다. 다른5분기 중 하나가 원인일 수 있으므로 FN04 예고장만으로 SC10 불량이라고 판정하지 않는다.

### 5.3 BF01 세척허가의 고유 연결

LAD1886 `0219`, NID29:

- ON21→SC10 처리응답22→VR04 처리Run23, W49/51. ORef34/RID52(`0594`),35/RID304와36/RID318(`0596`)이다.
- W53이 Le24.pre와 Forza_Lavaggio 접점25.in으로 분기한다. Le24.in1/W54=Data.DP_01 ORef37/RID6, in2/W55=Coeff.DP_01_SOGLIA_1 ORef38/RID8.
- Le24.out/W56→OR26.in1; local Forza_Lavaggio25.out/W58→OR26.in2. OR26.out/W59→Coil27 Abilita_lavaggio_BF01 ORef40/RID63(W60), Coil27.out/W72→Coil74 BF01_RUN ORef75/RID341(W73).
- 따라서 원문 조건은 `ON AND SC10_processed AND VR04_processed AND ((DP_01 <= DP_01_SOGLIA_1) OR Forza_Lavaggio)`다. 통상 예상으로 비교 방향을 >=로 바꾸지 않는다. 강제세척 접점도 앞의 SC10/VR04 조건을 우회하는 구조가 아니다.
- `0598`은 Forza_Lavaggio를 Local InterfaceAccess BO34, Abilita_lavaggio_BF01을 BO32로 기록한다. Data.DP_01(Int,BO1920)과 Coeff.DP_01_SOGLIA_1(Int,BO1104)은 BF01 관련 비교 입력이며 SC10의 보호 설정으로 전환하지 않는다. 현재값/단위환산/승인 안전한계는 미검증이다.
- BF01_RUN은 메모리이며 원시 스크루 회전증거가 아니다. P&ID의 DP·압력·온도 표기를 현재 PLC 설정값으로 채우지 않는다. BF01의 EV 개별 순서·보호 로직 전체는 이번 SC10 범위가 아니다.

### 5.4 원시 SC10/SC11과 Data.LAVA 복수쓰기

LAD1888 `0202`, NID6은 **OFF** Part599 아래 W600이 네 분기로 갈라진다. `0594` RID1/UID569는 %M0.1이므로 이름만 보고 비활성이라고 생략하지 않는다.

| 조건 | 원본 명령 | 대상 |
|---|---|---|
| OFF | Move547, 상수0 ORef570/RID67, W583/584 | ORef571 Data.LAVA |
| OFF AND 원시 SC10_Fbk601 | Move553, 상수1 ORef573/RID70, W587/588 | ORef574 Data.LAVA |
| OFF AND 원시 SC11_Fbk603 | Move559, 상수2 ORef576/RID72, W591/592 | ORef577 Data.LAVA |
| OFF AND 원시 SC10_Fbk605 AND 원시 SC11_Fbk607 | Move566, 상수3 ORef580/RID74, W596/597 | ORef581 Data.LAVA |

네 대상은 모두 `0596` RID68 Int BO1840/BAD2 Data이다. `0595` Data DB1 선언에 따라 DB1.DBW230이며 SC10 출력이 아니다. 처리 피드백을 사용하는 1886과 달리 여기에는 %I5.0/%I5.1 원시 입력이 사용된다. 동일 대상에 여러 조건부 Move가 있어 코드3의 실제 최종 채택·호출·다른 Writer까지 현재 CPU 결과로 확정하지 않는다.

## 6. 증상별 관찰·수리 판단 계획

다음은 향후 승인된 진단에서 남길 관찰계획이며 이번에 수행한 현장 조치가 아니다. 전기·기계 검측은 자격 있는 담당자가 현장 안전절차, 잠금/표찰, 잔류에너지 확인 하에 수행해야 한다. 강제출력·안전우회·보호값 변경을 허용하지 않는다.

| 증상 | 같은 시각의 관찰 지점 | 원문 비교·원인 배제 | 복구 자료 |
|---|---|---|---|
| 자동에서 요청이 안 켜짐 | ON/Auto_ON1/Tipo/Tempo/Emergency/M_SC_10 | 1843의1/5와1844의2/6, VR04 부재 Reset, startup DB2W2 구분 | 현재 호출·Writer 추세, 원인 해소 |
| 요청이 바로 꺼짐 | SC_10_FAULT, VR04 처리Run, UNDER TESTING | 1962 두 Reset분기 구분; UNDER TESTING 변경으로 해결하지 않음 | 허가 복귀·재요청·출력 기록 |
| Q4.0=1인데 접촉기 무응답 | FG140 단자1, XS51/52, 57QS1/QM1, KM1 A1/A2 | 명령·공급·접점·코일 단계 분리 | 승인 검측·현행 배선/명판 |
| 접촉기 흡입 뒤2초 고장 | 57KM1 13–14, E5.0/I5.0, DB13X5.0, T81 | 원시/처리 차이, IW4전달/ENO/호출/다른Writer | 동시 시각 추세·배선·처리 경로 정상화 |
| HMI와 PLC가 다름 | DB11X52.0/.1, DB3X2.2, DB13X5.0, DB14W4 | 1203 미결속, 356 출력미러 갱신, HMI 이벤트 | 원 프로젝트 결속·통신·시각 근거 |
| 접촉기 응답은 정상, 분진 배출 없음 | M34 축/감속기/커플링/스크루/BF01 출구/VR04 | 접촉기 피드백은 기계 회전·흐름 증거가 아님 | 안전정지 기계점검 및 승인 이송복귀 |
| SC10은 돌아가나 BF01 세척 불가 | 처리 SC10/VR04, DP01 비교, Local 허가 | 1886의 <= 방향과 공통 선행 조건, 원시/처리 구분 | BF01 담당 범위의 허가·DP경로 확인 |
| FN04 예고장 | 여섯 처리응답·T131·Prealarms_FN04 | SC10 단독 원인으로 단정하지 않음 | 분기별 추세·공유 정지 연결 |
| 시간표시1 반복/0복귀 | MIN/HOUR/T13/T17/Flag_Aggiorna_DB | 1037 Move1와1052 Move0, 누적 수신부·초기화 | 시간 수집정책·리텐션 증거 |
| 재시작 후 요청/고장 변화 | OB startup 문맥·DB2W2·DB3W2·HMI | Word쓰기와 Bool쓰기 중 어느 경로인지 분리 | 현행 OB/유지속성/기동기록 |

각 관찰은 관찰자·시각/시간대·위치·값/단위·수집 도구·프로젝트/CPU 근거·비교 원본·원인배제·승인된 조치·전후 복구 증거를 기록해야 한다. 미관찰을0/정상으로 채우지 않으며 실제 운영기록·사진·SEJIN 자료를 복사하지 않았다.

## 7. 기능 적용·검증·완료 경계

### 네 기능과 기록 보존

| 기능 | 후속 적용 근거 | 이번 상태 |
|---|---|---|
| 도면·래더 비교 | FG57↔1962/1807, FG121↔1070, P&ID↔1886 소유경계 | 대응 초안만, UI/강조/링크 시험 없음 |
| 백업 미리보기·선택 복원 | SC10 고유 키, 타설비·미지 필드·초안 보존 | 구현/저장/복원 미수행 |
| 전후 기록 비교 | 요청/출력/원시/처리/접촉기/실제이송 비교 | 미수행 |
| 관찰 보고서/PDF | 관찰필드·판본·해시·미확정 포함 | 사용자 보고서 생성 미수행. 원본PDF 렌더와 별도 |

BC01의 항목 수·알람 수·기록 지원 완료를 복제하지 않는다. 후속 구현 시 기존 note/repair_observation, 미지 행/필드, 타설비·초안·저장키를 보존하며0과 빈칸을 구분해야 한다. PC1280/모바일390·큰글자·검색/링크·저장/재읽기/재열기·복원/동시성·패키지/배포 시험은 이번 범위 밖이다.

### 미확정과 필요한 자료

1. 현재 PLC 프로젝트/CPU 비교, TIA 전체 교차참조: 요청/고장 Word덮어쓰기, cyclic/startup/main/HMI 호출, ENO/DisableENO, 재시작/리텐션과 간접 Writer.
2. HMI 원 프로젝트: LAD1203 미결속4개 데이터 참조와 실제 DB11 결속, DB2X2.2 이벤트/권한·알람 표시 목록.
3. 현행 명판·승인도: M34/57QM1/KM1/QS1, I5.0/Q4.0 모듈/단자, 케이블1_29 양끝 심선, 보호 설정·정상극성. 원본 범위를 현장 설정으로 지시하지 않는다.
4. BF01 제어자료: DP01의 현행 환산/단위/허가와 Local 데이터 유지·호출, Data.LAVA의 모든 Writer/활성. SC10 소유로 확장하지 않는다.
5. 실제 복구: 원인해소→고장해제→허가→재요청→출력→접촉기→실제회전·이송을 분리한 시각 있는 증거.

### 검증 상태

- 수행: 읽기 전용 Git/대장/preflight, SC10 고유 원본 XML/선언/Part·Wire·핀·상수 대조, startup Word/입출력 Word경로, 원본PDF7페이지 실제 렌더 및 P&ID 확대.
- 자체 추출은 읽기 전용 XML 참조/핀 기록과 PDF 렌더다. PLC 실행 모델 또는 시뮬레이터를 만들지 않는다. 원본의 기존 simulation 항목은 다른 Writer 존재만 문서화했다.
- 해시 일치는 파일바이트 보존 검사이며 전체 내용의 의미 검토 완료와 다르다. 의미 검토는 본문의 지정 SC10 경로·선언·도면 부분에 한정된다. 기존18불일치/1060확인대기/577설계시험 상태는 변경하지 않는다.
- 미수행: 매뉴얼 생성기, npm/build, BC01/UI/기록/배포 회귀, TIA/현재CPU/현장 행동시험. 문서 조사만이므로 완료로 주장하지 않는다.

| 상태 | 결과 | 해석 |
|---|---|---|
| documentation | draft_complete_with_gaps | 7영역 조사초안, HMI·현장 공백 명시 |
| static_review | self_source_reviewed_bounded_spot_review_done | 지정핵심 원본 대조, 별도 검토 대기 |
| ui_records | not_run | 미구현·미시험 |
| publication | not_published | 통합·게시 범위 밖 |
| tia_compile | not_performed | 수행 안 함 |
| live_cpu | not_performed | 수행 안 함 |
| field_recovery | not_performed | 수행 안 함 |

## 다음 검토

부모가 SC10 초안의 (1) 고유 T81/VR04 Reset과2초감시, (2) DB2W2/DB3W2 겹침, (3) HMI4개 미결속, (4) BF01 <= 세척허가와 OFF/Data.LAVA 복수쓰기, (5) 전기 FG57/121/140/253·시공1_29를 별도로 대조한다. 새 현장자료 없이 공백을 추정으로 메우지 않는다. 초안 승인 자체가 로컬133 통합·배포 또는 PLC/현장 변경 승인은 아니다.

## 부록: 원본 SHA-256

기계판독 목록은 `extracts/SC10/source-sha256.json`에 있으며 아래는 같은 목록이다. 원본 해시 재대조 수량과 의미검토 범위를 구분한다.

해시 대조: **75개 경로가 고정 Git blob과 모두 일치**. 이는 75개 파일 전체의 의미 검토 완료 수가 아니다. 본문에 명시한 SC10 핵심 경로·관련 Writer와7개 렌더 페이지의 검토를 구분한다.

| 원본 경로 | SHA256 |
|---|---|
| `all-in-one/sources/decoded-original/0262-FlgNet.xml` | `f1f7a0d69692ada132c134fd7c6272eea8e183e77e41fd6ea96742c6abe68c19` |
| `all-in-one/sources/decoded-original/0441-FlgNet.xml` | `120be8e7e1340f860083c1bf3f5d2cad5bee5464a46beadc886a45fb61242369` |
| `all-in-one/sources/decoded-original/0164-FlgNet.xml` | `15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491` |
| `all-in-one/sources/decoded-original/0165-FlgNet.xml` | `4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88` |
| `all-in-one/sources/decoded-original/0324-FlgNet.xml` | `bc65a2bce991e021fcf6643e0ebc01b59d5495763940ec3b489b4608577e9b11` |
| `all-in-one/sources/decoded-original/0339-FlgNet.xml` | `ce2c6279b55c8a5ac837a0f7c7a0945636df7dc52b68a1c3d6ec158234b37543` |
| `all-in-one/sources/decoded-original/0379-FlgNet.xml` | `0b0c99ad4a16586dd1be7db3b440cea99f07b38cf0cac83409e9243d48e0db49` |
| `all-in-one/sources/decoded-original/0264-FlgNet.xml` | `9af15015b447731255eff81680aa71321fb4d0ebe2c28904f442146538ff030d` |
| `all-in-one/sources/decoded-original/0265-FlgNet.xml` | `f2471b6ab6169e4c082983ea2080a383cf8b13cba4503a9a07f83d0956fbf08a` |
| `all-in-one/sources/decoded-original/0219-FlgNet.xml` | `245409937abf7e28f25a24d4a6d311a801a4b2ee7293148be9b3d266352eb53a` |
| `all-in-one/sources/decoded-original/0202-FlgNet.xml` | `8caa0c15a086ffb64f7857fb656b3baba3090a32948b9942ccecff6c730186bb` |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` |
| `all-in-one/sources/decoded-original/0405-FlgNet.xml` | `4290734017e68a9ded2a54a34c55d65cc7b2336296cb8d2d397e64f381b7947d` |
| `all-in-one/sources/decoded-original/0024-FlgNet.xml` | `a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67` |
| `all-in-one/sources/decoded-original/0019-FlgNet.xml` | `a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5` |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` |
| `all-in-one/sources/decoded-original/0147-FlgNet.xml` | `386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c` |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` |
| `all-in-one/sources/decoded-original/0401-FlgNet.xml` | `60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae` |
| `all-in-one/sources/decoded-original/0162-FlgNet.xml` | `892eab96a4f5c87cfafd35f8a2e2a04982a93ca23c777312101882e408b11deb` |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` |
| `all-in-one/sources/decoded-original/0064-IdentXmlPart.xml` | `ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d` |
| `all-in-one/sources/decoded-original/0067-IdentXmlPart.xml` | `0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628` |
| `all-in-one/sources/decoded-original/0555-IdentXmlPart.xml` | `46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` |
| `all-in-one/sources/decoded-original/0575-IdentXmlPart.xml` | `40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06` |
| `all-in-one/sources/decoded-original/0577-IdentXmlPart.xml` | `511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47` |
| `all-in-one/sources/decoded-original/0578-IdentXmlPart.xml` | `0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b` |
| `all-in-one/sources/decoded-original/0594-IdentXmlPart.xml` | `88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd` |
| `all-in-one/sources/decoded-original/0595-IdentXmlPart.xml` | `10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52` |
| `all-in-one/sources/decoded-original/0596-IdentXmlPart.xml` | `a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0` |
| `all-in-one/sources/decoded-original/0597-IdentXmlPart.xml` | `60e292145fe54912a1da7510c8641a4f4c85efe62e1b5206ee3d92794a28de20` |
| `all-in-one/sources/decoded-original/0598-IdentXmlPart.xml` | `dc001c9370a691546c5dea79f5a1252d6d0a5564754703018c47df4bcc2522bb` |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` |
| `all-in-one/sources/decoded-original/0613-IdentXmlPart.xml` | `09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb` |
| `all-in-one/sources/decoded-original/0614-IdentXmlPart.xml` | `c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294` |
| `all-in-one/sources/decoded-original/0615-IdentXmlPart.xml` | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` |
| `all-in-one/sources/decoded-original/0616-IdentXmlPart.xml` | `650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d` |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` |
| `all-in-one/sources/decoded-original/0626-IdentXmlPart.xml` | `a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` |
| `all-in-one/sources/decoded-original/0632-IdentXmlPart.xml` | `fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9` |
| `all-in-one/sources/decoded-original/0633-IdentXmlPart.xml` | `9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc` |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` |
| `all-in-one/registers/control-spec.json` | `1e495b32f1f11b910919fbd2945e842a019fce9a27a6a0d7298041a7fab00079` |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` |


## 전달 전 핵심 근거 제한 대조
2026-10-11 고유 출력/요청 Reset의 원본 Part/Wire와 해당 모터 회로 실제 PDF 렌더를 표본 재확인하고 인용 원본 SHA256을 모두 재계산하여 일치했다. 전체 원본 의미 검토 또는 현재 CPU/현장/게시 검증으로 확대하지 않는다. 사용자 독립 검토와 미확정 경계는 유지한다.
