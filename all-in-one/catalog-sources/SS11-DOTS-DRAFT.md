# SS11 이송 장치 감시 스위치 — 독립 원본 조사 초안

- 대상: SS11, sensor/계측, 부모 MC05. INVENTORY catalog[112], phase2/planned, baseline/not_assessed 유지. 같은 이름의 SS01·SS09·SS10과 별도 ID이며 부모 완료를 상속하지 않는다.
- 기준: 읽기 전용 `source-mv06`, `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 문서 조사만 완료하며 현재 CPU·실물·현장 복구 검증이 아니다.
- 표준: GME-STD-1.0.0, AGENTS 및 rollout skill, WORK-STANDARD/WORK-ITEM-TEMPLATE/INVENTORY, BATCH17 지시·scope·중복검토의 해당 행 적용. 실제 모델 런타임/추론 설정은 미확인.
- 원본 표기: `D/`=`all-in-one/sources/decoded-original/`, `S/`=`all-in-one/sources/`, `R/`=`all-in-one/registers/`. P=Part, W=Wire, O=ORef, R=RID/RefId. UID는 파일·블록·NID 문맥 안에서만 결속한다.

## 핵심 확인·상충·누락

1. 고유 선언 `D/0556-IdentXmlPart.xml` R243는 Global `MC05_torque`, Bool, Input AO54=%I6.6, SAM=None이다. NID=-2147483648/UID115/AK=Monitor만 있다. 모니터 선언을 실행 Contact나 알람 생성으로 바꾸지 않는다.
2. OEM FG26/실제 PDF27: +24Vdc10.7→X1:56(5×20 2A F)→선26.2→SS-11 접점11–12→X1:57→E6.6, 참조122/6. FG122/실제 PDF123: E6.6→모듈 단자27, CPU515/MOD9, LIMIT SWITCH SS-11, 역참조26/7. 두 쪽은 직접 렌더 확인했다.
3. `LIMIT SWITCH TORQUE CONTROL`은 도면의 기능 명칭이다. 실제 토크스위치/트립와이어/회전센서의 종류, 정상극성, 현재 설치·예비·철거 상태는 미확인이다. 원문 SPARE와 `mc05 deleted` 제목은 현장 철거 증거가 아니다.
4. IW6→DB13.DBW6 Word 사본은 원문 핀으로 확인했다. SS11에 대응하는 DB13.X6.6 포함 범위지만, 이를 사용하는 고유 알람·타이머·S/R·MC05 정지식·HMI 표시 생성은 확보하지 못했다. SS01 ON·SS09 OFF 또는 MC04 타이머를 복제하지 않는다.
5. 시공 참고 PDF34·59의 케이블 이름 `=EXI+MC04-SS11A`와 목적지 MC-05/SS-11이 상충한다. SS11을 MC04 소유로 이관하지 않는다. JB EXI1TB2는 SS10/11 공유 경로다.
6. 부모 MC05 초안 §4.2의 “E6.4/5/6 묶음 SPARE”는 실제 FG122 렌더와 다르다. SS11 조사에서 확인한 우측 SPARE 점선 범위는 E6.5·E6.6이고 E6.4는 그 밖이다. 원초안은 보존하며 이 제한 정정을 인계한다.

### 공유 근거와 이번 독립 확인

`MC05-DOTS-DRAFT.md`는 원본 위치 색인으로 사용했다. 부모의 자동 요청·운전시간·출력 전체 분석은 재작성하지 않는다. 공유 입력 Word/상위 호출은 같은 고정 원본을 직접 다시 확인했고, SS11 선언·전기 양끝점·시공34/59·케이블 상충은 독립 확인했다. 부모의 별도 P&ID 미확보 및 MC05 전체 출력식 공백은 참고 경계일 뿐 SS11 완료 증거가 아니다. P&ID 원본을 이번에 다시 렌더하지 않았으므로 P&ID 실물 대응을 새로 확정하지 않는다.

# 1. 설비·자료 기준 — 적용

SS11의 문서상 관계는 INVENTORY의 부모 MC05, R/equipment.json의 별칭 mc05_torque, OEM MC-05 회로의 SS-11과 E6.6, PLC 선언 I6.6의 일치로 지지된다. 별칭은 문서 연결이며 실물 동일성 검증은 아니다. MC05 모터 M10, 명령 Q0.5, 접촉기 피드백 I1.0은 부모 구동 체인이다. SS11 원시 I6.6와 합쳐 한 센서의 출력/응답으로 표현하지 않는다.

| 자료 | 판본·확인 범위 | 해석 한계 |
|---|---|---|
| Electrical_Rev2.pdf | FG26/PDF27 및 FG122/PDF123, 기본일27.05.2024, Rev2 17.03.2025 각각 footer 시각 확인 | 현행 승인 준공도·현재 배선 확인 아님 |
| Electrical_Can_Decoating_20241118.pdf | PDF34=34/64, D-PAGE17, CANDC-CONS-E017-034; PDF59=59/64, D-PAGE9, CANDC-CONS-C009-059. 두 쪽 모두 Rev1 24.11.11 first draft design | 참고 시공 설계이며 실제 코어/단자 준공 증거 아님 |
| XML 복원 원문 | 0556 고유 선언, 0397/0030/0544 및 해당 선언군 | 복원 범위 밖 간접주소·대체블록·HMI 쓰기까지 완전 검증하지 않음 |
| HMI CSV·네트워크 색인 | MC05 관련 설정3행과 deleted 제목4행 | 검색/설정 자료, 온라인 현재값 및 실행식 아님 |

현재 명판·제조사 매뉴얼·장치 사진·접점표·변경이력은 미확보다. 이 자료 없이 안전등급, 정비주기, 토크 임계값, 정상 ON/OFF를 채우지 않는다.

# 2. I/O·HMI — 적용, 표시 결속 미확보

| 계층 | 직접 근거 | 의미·미확정 |
|---|---|---|
| 원시 SS11 | D/0556 R243 `MC05_torque`, ID S=Global, OD S=1/T=Bool, SSD AO54, SAD Input/SAM=None; C NID=-2147483648 UID115 AK=Monitor | %I6.6 Bool, PIW/아날로그 환산 아님. 실행 Contact UID115로 임의 연결 금지 |
| 입력 Word | D/0627 R13 `Tag_171`, Global Word16, AO48 Input/SAM=None, NID1/O45 | IW6가 I6.6를 포함. 다른 byte 영역 또는 PIW6로 바꾸지 않음 |
| 처리 사본 | D/0629 R14, Global Word16 AO48 BAD BIRID4, NID1/O46 AK=Write → D/0628 R4 Inputs TOD DB13 | DB13.DBW6, byte6..7의 사본. DB13.X6.6의 물리 정상 의미는 부여하지 않음 |
| 별도 Word 사본 | D/0692 R1 Tag_171 IW6 NID1/O82 → D/0690 R3 Word_inputs.word1 AO0/BAD2 → D/0689 R2 TOD DB100 | DB100.DBW0 쓰기, I6.6의 위치는 byte0 bit6에 해당. 후속 소비·알람 연결 미검토 |
| 부모 모터 피드백 | D/0556 R242 MC05_Fbk AO8 Input Bool Monitor UID112 | I1.0. FG26 26KM1 보조접점13–14이며 SS11과 별도 |
| 부모 모터 명령 | D/0556 R241 Start MC05 AO5 Output Bool Monitor UID119 | Q0.5. SS11의 센서 출력으로 소유 변경 금지 |

전용 HMI SS11 문자열/별도 태그는 확보하지 못했다. S/hmi_plc_tags.csv에는 부모 MC_05\Flag=DB2,X0.5(001AF), MC_05\RispostaA=DB11,X10.0(00323), MC_05\Allarme1=DB11,X10.1(0003F), Access PLC가 있다. CSV는 `dde.cfg 설정; 온라인 현재값 아님`으로 명시한다. Allarme1 이름만으로 I6.6 또는 DB13.X6.6가 해당 표시를 구동한다고 단정하지 않는다. 실제 화면·이벤트·주소 writer·권한·통신대상은 원 HMI 프로젝트 필요.

# 3. 제어 구조 — Word 전달 확인, 고유 고장/정지 식 미확보

## 3.1 원시→DB13, D/0397-FlgNet.xml / LAD1070 / NID1

- P42 Gate=Move, DisableENO=true, Cardinality1.
- W21의 Powerrail이 P42.en에 직접 연결. 이전 P22/P27의 ENO 결과가 P42의 직렬 허가인 것은 아니다.
- O45 RefId13(D/0627 IW6)→W52→P42.in.
- P42.out1→W54→O46 RefId14(D/0629 DB13.DBW6), AK=Write.
- P42.eno→W53→P43.en은 다음 Word 사본에 대한 연결이다. ENO 속성/선이 함께 존재하는 원문을 보존하며 실제 실행 성공을 검증한 것으로 표현하지 않는다.

확인 식은 “상위 호출 조건 아래 IW6가 DB13.DBW6로 Move”이다. Bool 알람 Coil·SCoil·RCoil·타이머·상수 환산식이 아니다. DB13.X6.6의 후속 소비자가 확인되지 않아 경보·정지·복구 방향은 열린 경계다.

## 3.2 상위 호출, D/0030 / LAD1613 / NID19

W31 rail→CRef21 Recipes Handler.en→W32(eno)→CRef23 HMI.en→W33(eno)→CRef25 HMI Output.en→W42(eno)→P37 Contact.in. P37은 operand Negated이며 O45/R140(D/0692 Simulation(1), Global Bool Memory AO1440=%M180.0)이 W44로 들어온다. P37.out→W43→CRef28 HMI Inputs.en.

CRef28 RefId136/CodeBlock UID29 RefId135는 D/0694 R136 BIID TORID135 및 D/0688 R135 HMI Inputs TOD FC15와 결속한다. HMI CRef23/CodeBlock24/R124=FC11, HMI Output CRef25/CodeBlock26/R128=FC19도 선언으로 대조했다. 이전 호출 ENO와 반전 접점이 있으므로 DB13을 매번 무조건 실시간 입력이라고 쓰지 않는다. Simulation(1)은 기존 원문에 있는 접점 명칭 인용뿐이며 중지된 시뮬레이터 실행·접근을 승인하지 않는다.

## 3.3 별도 사본, D/0544 / LAD1614 / NID1

W103 rail→P69 Move.en; O82/R1(D/0692 IW6)→W92→P69.in; P69.out1→W93→O83/R3(D/0690 Word_inputs.word1→D/0689 DB100.DBW0). P69.eno/W94는 다음 P73.en으로 이어진다. 이 경로는 입력 읽기/DB Word 쓰기이며 실제 입력 I6.6 또는 출력 Q0.5를 쓰지 않는다. 두 DB 사본의 모든 간접 소비를 전수 해석한 것은 아니다.

## 3.4 고유 로직 미확보의 탐색 범위

181개 IdentXmlPart를 XML 파싱하여 mc05/mc_05/ss11/ss-11 명칭을 검색했다. 결과6개 요소는 Start MC05 모니터2, MC05_Fbk1, MC05_torque1, 부모 요청 M_MC_05 및 MC_05_HOUR 각1이다. 이는 명명 요소 탐색 수이며 181개 전체 의미 검토나 독립신호6개가 아니다.

Input 영역 bit54를 포함하는 SSD AO/OD 크기 검색에서는 MC05_torque Bool 및 두 문맥의 Tag_171 Word가 확인됐다. 정수 AO54만 같은 다른 DB의 MV05_Auto를 SS11로 연결하지 않았다. 복원 선언의 명명·직접주소 탐색으로도 간접 주소나 복원 누락은 배제하지 않는다.

R/all-networks.csv의 mc-05/mc05 행: time work motor/22/doc1023, hmi/6/doc1183, allarms1/13/doc1793, motors1/13/doc1942. 모두 제목에 deleted, 원본 XML 칸 공란이다. 문서1793의 전용 경보 본문과 문서1942의 최종 출력식이 확보되지 않아 SS11 입력→경보→출력 차단 연결은 미확보다. 제목을 코드 전체 부재·현재 비설치로 해석하지 않는다.

# 4. 전기 전달 경로 — 적용, 실제 끝점 미확정

| 직접 렌더 원본 | 경로·핀 | 해석·경계 |
|---|---|---|
| S/Electrical_Rev2.pdf FG26/PDF27 | +24Vdc10.7(좌25/9, 우27/5)→X1:56, 5×20 2A F→26.2→SS-11 접점11–12→X1:57→E6.6/122/6 | LIMIT SWITCH TORQUE CONTROL, MC-05 제목, 전체 SPARE 점선. 퓨즈2A F는 도면 표기이며 현재 설치/보호설정 증명 아님 |
| 같은 PDF FG122/PDF123 | FG26/7→E6.6→단자27, CPU515 MOD9, LIMIT SWITCH SS-11 | 역방향 끝점 일치. 현행 CPU 모델·장착 모듈/주문번호·실제 전압 확인 아님 |
| 시공 PDF59, 9_1 | =EXI+EXIT-EXI1TB1A, CR→EXIT/EXI1TB1, SS10/11\|LS09-12\|PB17, DC/CVV/25G/1.0/spare10, route100/120/121/122RA/E300, adjustment3, LEN74 | CR에서 공유 JB로 가는 계획 케이블. SS11 전용25선이 아님 |
| 시공 PDF59, 9_3 | =EXI+MC05-EXI1TB2A, EXIT/EXI1TB1→MC-05/EXI1TB2, SS10/11, DC/CVV/7G/1.0/spare2, E350, adjustment15, LEN16 | MC05 명칭 JB 공유. SS10/SS11을 동일 실물로 병합하지 않음 |
| 시공 PDF59, 9_8 | =EXI+MC04-SS11A, FROM MC-05/EXI1TB2→TO MC-05/SS-11, DC/CVV/2C/1.0/spare0, E351, adjustment3, LEN3 | 케이블 이름 MC04와 대상 MC05 상충, 원문 유지 |
| 시공 PDF34, 9_8 | EXI1TB2의 가지2→SS-11; 표 DEVICE LOC MC-05/TAG SS-11, EXPOSED CP02 No2/Pipe16, 동일 MC04-SS11A/CVV1.0/2core | 그림 가지번호2는 확정 전기 단자핀2가 아님. PDF59와 같은 명칭 상충 |

OEM X1:56/57과 시공 EXI1TB1/EXI1TB2의 코어색·코어번호·JB 단자번호를 연결하는 완전한 승인 준공표는 없다. 따라서 전기 양끝의 문서 연결을 현장 전 구간 도통 완료로 표시하지 않는다. 릴레이 부하5/9 규칙은 이 SS11 단순 접점 경로에 임의 적용하지 않는다. SS11 도면 접점은11–12이고 부모 26KM1 피드백은13–14로 별개다.

FG122/PDF123의 SPARE 점선은 E6.3 별도와 E6.5/E6.6 묶음이다. E6.4(SS09)는 우측 점선 밖이므로 부모 문서의 묶음 표현을 그대로 복제하지 않았다. SS11 자체 SPARE 상태는 확인되나 현재 사용상태 판정은 남긴다.

# 5. 알람·복구 — 적용, 고유 본문 미확보

| 확인 항목 | 현재 문서 결과 | 필요한 자료 |
|---|---|---|
| 발생 조건·극성 | 토크 기능명/접점11–12/원시 I6.6만 확인. high/low 발생식 미확보 | 실제 장치 접점·작동 원리 및 현재 TIA 교차참조 |
| 지연·유지·S/R | SS11 전용 타이머·설정치·래치/Reset 없음이 증명된 것이 아니라 복원 범위에서 미확보 | doc1793 대체/누락 블록, bit/Word/간접 writer와 타이머 선언 |
| 영향 | 부모 Q0.5 차단·자동정지·허가 차단 결속 미확보 | 현재 Motors1/Allarms1 실제 본문 |
| HMI | MC_05 Allarme1 주소는 있으나 SS11 연결 미확보 | DB11.X10.1 writer와 HMI 화면/이벤트 |
| ACK/Reset·재기동 | 고유 동작 순서 미확보 | 승인 운전/복구 절차, 원인 제거·안전 확인·재요청 조건 |

부모 MC05의 시간 초기화 T17/5초나 MC04 T54/5초를 SS11 지연으로 사용하지 않는다. 이름·접점기호만으로 NC 정상, 단선 시 반드시 trip, fail-safe 또는 안전인증을 주장하지 않는다. 알람 표시 꺼짐·비트0·접촉기 응답은 기계·공정 복구 완료를 뜻하지 않는다. 온라인 강제·우회·보호값 변경·Reset 조작 시험은 수행하지 않았다.

# 6. 증상별 수리·관찰 초안 — 적용, 실제 작업 미수행

| 증상/질문 | 수집할 관찰 | 비교·분리할 경계 |
|---|---|---|
| SS11이 현재 있는가 | 명판·현장 태그·위치·설치/철거 변경이력·준공도 | OEM SPARE와 실제 예비/철거를 분리 |
| 감시장치 작동과 원시 상태가 다름 | 자격 있는 담당자가 승인 절차로 수집한 접점11/12, X1:56/57, 단자27, I6.6의 같은 시각 상태 | 센서 기계작동·공급·케이블·단자·주소 대응을 분리. 통전 조작법 추정 금지 |
| 원시 입력과 DB 사본이 다름 | I6.6, DB13.X6.6 및 HMI Inputs 호출/상위 ENO/반전허가 관찰 | 호출정지·갱신시점·다른 writer·프로젝트 판본 차이; 비트 강제 금지 |
| 토크 이상인데 표시 없음 | 실제 상태, 입력/DB13, DB11.X10.1, 현재 HMI 바인딩·경보식 | CSV 설정 존재와 알람 생성 연결을 분리 |
| 기동이 막히거나 멈춤 | MC05 요청/출력/접촉기 피드백과 SS11 입력을 별도 기록 | SS11 원인으로 단정하지 말고 고유 정지식 확보 후 비교 |
| 케이블 이름은 MC04 | 9_8 양끝 표찰·코어·JB 단자표·최신 승인도 | MC04-SS11A 문자열과 MC05/SS11 목적지 상충 해소 필요 |

관찰 기록은 관찰자·시각/시간대·정확한 위치·값/단위·도구/방법·원 프로젝트 및 도면 판본·비교 원문·원인 배제·승인 조치·복구 증거/확인자를 갖춘다. 이번 문서는 실제 측정값·작업이력·사진을 생성하거나 복제하지 않았다.

# 7. 완료·누락 및 인계 — 문서 범위 한정

## 7.1 검토 결과와 금지 경계

- 3개 FlgNet(0030,0397,0544)의 관련 Part/Wire/ORef/CRef와 9개 IdentXmlPart(0556,0627,0628,0629,0688,0689,0690,0692,0694)의 고유/공유 선언을 의미 대조했다. 해당 파일 전체 타설비 로직을 완료했다는 뜻은 아니다.
- 실제 도면 렌더4쪽: OEM27/123, 시공34/59. 이미지와 페이지별 추출문을 SS11 전용 extracts에 보관했다. 전체 PDF 의미검토 주장 없음.
- 선언181파일은 탐색 범위다. 선택30파일 SHA256/Git blob 검사는 내용일치/보존 검사이며 30개 의미검토 또는 설비30개 완료가 아니다.
- SS11 전용 정적 구조검사15/15 통과. PLC 로직을 실행하거나 시뮬레이터·원본 생성기·build/test를 실행하지 않았다. 원본 Git 변경0 및 고정 HEAD 확인. 중지5자산은 바이트 해시만 비교하여 보존.
- 작성 변경은 이 MD 및 SS11 extracts뿐. 대장/코드/버전/공용추출/다른초안/PLC/현장/보호값/SEJIN 변경 없음. 사용자 추가 통합 승인 여부와 별개로 본 연구자는 문서 조사 권한만 사용.

## 7.2 네 기능의 별도 상태

| 기능 | 이번 산출·상태 |
|---|---|
| 도면·래더 비교 | FG26/122와 입력 사본 네트워크의 연결 위치 제공. UI 구현·링크 시험 미수행 |
| 백업·선택 복원 | 기존 note/repair_observation·미지 필드·저장 키 보존 요구. 접근·저장·복원 미수행 |
| 기록 전후 비교 | 위 관찰 항목 제안만 작성, 실제 UI 검증 미수행 |
| 보고서/PDF | 독립 한국어 MD 초안. 사용자 현장 기록 기반 보고서/PDF 출력 검증 미수행 |

## 7.3 남은 자료와 판정 기준

1. 실제 SS11의 제조사/모델/접점 방식/정상상태/설치 위치·현재 사용 여부를 명판·준공도·승인 변경기록으로 확인.
2. 현재 TIA 원 프로젝트에서 I6.6·DB13.X6.6·DB100 Word 사본의 소비자, doc1793/1942의 누락/대체 블록, DB11.X10.1 writer를 읽기 전용으로 확보. 알람·정지·타이머·S/R이 확인될 때만 해당 항목 작성.
3. 원 HMI 프로젝트의 MC05 Allarme1 실제 화면/이벤트/통신 바인딩 확보. 신호주소 일치만으로 표시 완료 판정 금지.
4. OEM X1:56/57↔EXI1TB1/EXI1TB2↔SS11의 승인 코어/단자표 및 현장 표찰 확보. MC04-SS11A 상충 판정 후 원문 보존.
5. 문서 근거 미확정은 그대로 남기고 새 자료 전에는 동일 실물 보류를 반복 조사하지 않는다. 후속 통합·독립검토·게시·실물 검증은 별도 상태다.

| 상태축 | 결과 |
|---|---|
| documentation | draft_ready, SS11 7영역 범위 한정 |
| static_review | scoped_source_review, 구조15/15·선정30해시 일치 |
| ui_records | not_run |
| publication | not_published |
| tia_compile | not_performed |
| live_cpu | not_performed |
| field_recovery | not_performed |

## 실제 단계 시각 (UTC)

- 2026-10-11 12:49:36: 배정 수신·공통지시/범위 읽기 시작.
- 12:49:54–12:50:27: 고유 선언 검색·Word/호출 원문 추출·도면 렌더.
- 12:50:32–12:50:44: 도면4쪽 시각 대조 및 SPARE 범위 정정 인계.
- 12:51:19–12:52:01: 시공/DB100 결속 확인, 구조검사·해시 계산.
- 최종 작성·재검사 완료시각은 아래 부록 검증시각에 기록한다. 추정 작업시간은 적지 않는다.

# 부록 A. 선정 원본 SHA256 및 고정 Git blob 전체표

아래 표는 source-mv06 상대경로다. Git blob은 고정커밋의 blob과 모든 행에서 일치하며, SHA256은 실제 읽은 바이트 지문이다. 마지막 중지5자산은 보존용 해시만 확인하고 본문 의미분석·실행 대상이 아니다.

| 원본 경로 | SHA256 | Git blob | 고정 일치 |
|---|---|---|---|
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | 예 |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | 예 |
| `all-in-one/sources/decoded-original/0544-FlgNet.xml` | `7eea2ea628a9c9ba7b9df66e20f7bab670da7dc7a155084d80119943ed45e6ca` | `99409858956641861deaf6e727522385febf1b21` | 예 |
| `all-in-one/sources/decoded-original/0556-IdentXmlPart.xml` | `065d71114e26c93af180265e0e6d59d2a190af1f2f0581c5265e7f4f67d6e23f` | `15ae569ff390ef5c791b0f76d96bd86d5ec6b938` | 예 |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | 예 |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | 예 |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | 예 |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | 예 |
| `all-in-one/sources/decoded-original/0689-IdentXmlPart.xml` | `f0cc6f770c2759b92a9a79f4e289dbfa0ca270d90e0e89496f94a13a8d839d51` | `8db940bdbab78ea27ffc280acba9375d2a93f587` | 예 |
| `all-in-one/sources/decoded-original/0690-IdentXmlPart.xml` | `fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541` | `36bd403f48ba8e364126837b19fb0419bbe78941` | 예 |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | 예 |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` | 예 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | 예 |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | 예 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | 예 |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` | 예 |
| `all-in-one/registers/all-networks.csv` | `7b6a9fc46f56c1bec7c4c7136792e2fc470fd07c15aa885d4f411c478d5e5f7c` | `cd54feb06ebcbea0c56ccb1226707799be084e16` | 예 |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | 예 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | 예 |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | 예 |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | 예 |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | 예 |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | 예 |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | 예 |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` | 예 |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` | 예 |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` | 예 |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` | 예 |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` | 예 |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` | 예 |

선정 해시 검사시각: 2026-10-11T12:52:01.705097+00:00.

# 부록 B. 검사·산출 참조

SS11 전용 extracts의 source-hashes.json, scoped-checks.json, named-declarations.json, address-overlaps.json, 원문 포맷 추출과 PDF4쪽 렌더가 재검토 자료다. 검사 스크립트는 XML 구조와 바이트만 검사하며 제어 로직을 실행하지 않는다. 부모 MC05 색인은 재사용했고 원초안은 수정하지 않았다.

최종 문서/해시/구조 재검사 완료: 2026-10-11T12:55:05.500823+00:00; 7영역·해시30행·구조15/15 확인, 원본 Git 변경0.
