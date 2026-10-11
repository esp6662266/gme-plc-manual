# MC05 금속 컨베이어: 작업3 자체 추가조사 초안

- 상태: `documentation=draft_ready`, `static_review=scoped_source_review`; 코드 통합·화면·배포·TIA·현재 CPU·현장 복구 완료가 아니다.
- 대상: `catalog_id=MC05`, 금속 컨베이어 MC05, motor / 원료 이송. `priority_key=null`, `parent_id=null`, 대장 `phase2/planned`, `baseline/not_assessed`를 유지한다. 사용자 승인 작업3의 네 번째 최대5개 묶음 중 한 개이며, 로컬 구현 작업의 2차133 제외를 변경하지 않는다.
- 고정 기준: `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION `1.12.0`. [고정 원본](https://github.com/esp6662266/gme-plc-manual/tree/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one).
- 적용 표준: GME-STD-1.0.0. 저장소 `.agents/skills/gme-equipment-rollout/SKILL.md`, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY 및 시작·실행 경계를 읽고 적용했다.
- 조사일: 2026-10-11 UTC. 실제 모델/추론 UI 선택은 관측하지 않았으므로 미확인이다.
- 수정 범위: 이 MC05 초안과 MC05 전용 추출·검토 자료. 원본·기존 완료분·공통 코드·버전·대장·운영기록·배포를 변경하지 않았다. PLC/현장/보호값/SEJIN 프로그램·운영 자료·사진·작업이력은 변경·복제·통합하지 않았다. 시뮬레이터 작성·생성·실행·행동시험은 하지 않았다.
- 출처 표기: `S/`는 `all-in-one/sources/`, `D/`는 `S/decoded-original/`, `R/`는 `all-in-one/registers/`. XML 번호는 D/의 실제 파일 번호다. P=Part UID, W=Wire UID, O=ORef UID, R=선언 RID/RefId. LAD 문서 ID와 XML NID를 구분한다.

## 먼저 확인할 결론

1. `mc05 deleted`는 모터·알람·HMI·운전시간 네 곳의 **색인 제목**이다. 이 네 행에는 대응 FlgNet XML이 연결되지 않는다. 검색 인덱스의 별도 `deleted` 필드는 오히려 false다. 제목을 실제 철거·현재 비설치·전체 코드 삭제의 증거로 쓰지 않는다.
2. 전기 FG26/PDF27에는 M10, 1.5kW·3.03A, 26QM1 2.8–4A 범위, 26KM1/26QS1의 접촉기 회로가 남고 전체 회로가 SPARE로 둘러싸여 있다. FG117/122/136에서도 MC05의 I1.0/I6.6/Q0.5가 SPARE 표시다. 보호기 범위는 실제 설정값이 아니다.
3. MC05 요청은 DB2.X0.5다. 예열 0164/LAD1843의 값17 분기는 **RCoil P458**, 생산 0165/LAD1844의 값21 분기는 추가 **OFF 접점 P1149를 거친 SCoil P793**다. MC04나 VS01의 조건으로 대체하지 않는다.
4. `startup only` 0147의 DB2.DBW0에 대한 INT#0 쓰기는 X0.5를 포함한다. 명명된 Set/Reset만 목록화하면 이 쓰기를 놓친다. HMI 설정도 같은 DB2.X0.5를 가리키지만 실제 HMI 쓰기 이벤트·현재 최종값은 미확인이다.
5. Start MC05 Q0.5는 모니터용 선언이 남아 있으나, 이번 복원 XML에서 **MC05 명명 최종 출력 Coil·전용 피드백/토크 알람·전용 모터 타이머를 확보하지 못했다**. MC04의 Tag_57/T54/5초, MC03의 토크 알람을 가져오지 않는다.
6. HMI 3행은 DB2.X0.5 / DB11.X10.0 / DB11.X10.1 설정이다. DB11 표시와 원시 I1.0/I6.6, 처리 DB13, 출력 사본 DB14는 서로 다르다. HMI deleted 제목과 실제 바인딩 부재를 남긴다.
7. 운전시간의 잔존 쓰기는 MC_05_HOUR에 **0을 Move**하는 0336 P2834다. 이를 MC05 운전시간 누적으로 설명하지 않는다. 공유 초기화 T17의 S5T#5S는 모터 고장 지연시간이 아니다.
8. 시공 참고 PDF59의 SS11 케이블 이름은 `=EXI+MC04-SS11A`지만 수신 태그는 MC-05/SS-11이다. 케이블 문자열만 보고 SS11을 MC04로 이관하거나 두 컨베이어를 합치지 않는다.

## 7영역 적용표

| 영역 | 판정 | 이번 결과 | 미확정 경계 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | MC05/M10/SS11의 문서상 관계, deleted/SPARE/설계 잔존 분리 | 현재 본체·설치·사용·철거 여부 |
| I/O·HMI | 적용·일부 근거 미확보 | 3 물리 신호, 요청 Bool, 시간 Int, HMI 3행, Word 전달 | HMI 실제 화면 이벤트·DB11 생성핀·현재 I/O 할당 |
| 제어 구조 | 적용·핵심 출력 근거 미확보 | 예열 Reset/생산 OFF-Set, Startup Word, 호출, 시간0쓰기 | 요청→최종 Q 제어 연결, CPU 실행·복수 쓰기 우선순위 |
| 전기 전달 경로 | 적용 | FG26/117/122/136 실제 페이지와 명령·접점·단자 양 끝 | 현재 결선·명판·보호설정·안전 성능 |
| 알람·복구 | 적용·전용 로직 근거 미확보 | 전용 알람 부재 경계, HMI 이름 한계, 공통 시간초기화 구분 | 실제 고장식·지연·유지·Reset·재기동 영향 |
| 증상별 수리 | 적용, 관찰 초안 | 설치 식별부터 원시/요청/회로/표시의 비교 지점 | 현장 측정·조치·복구 수행 없음 |
| 완료 기준 | 적용 | 원본 위치·충돌·누락·해시·다음 확인 목록 | 구현/UI/배포/TIA/CPU/현장 모두 별도 |

# 1. 설비·자료 기준과 소유

## 1.1 대장 및 자료별 정체성

INVENTORY `catalog[78]`의 MC05는 독립 루트다. 하위 SS11은 별도 catalog ID, `parent_id=MC05`, sensor로 남는다. 부모 조사에 SS11 경로를 다루는 것은 하위 설비 문서가 완료됐다는 뜻이 아니다. MC04(M09), MC03 예비 모터(Q0.3), VS01(M06/M07)은 별개다.

S/Electrical_Rev2.pdf FG26/PDF27 제목은 METALLIC CONVEYOR MC-05이며 모터 M10과 SS-11이 같은 회로에 있다. S/Electrical_Can_Decoating_20241118.pdf PDF34·51·59는 EXIT 영역 MC05/M10/SS11 연결을 담지만 `24.11.11 first draft design` 자료다. 이 자료의 고객 표제란과 별개로 공개 저장소에 이미 포함된 참고 원본만 읽었으며 SEJIN 운영 프로그램 자료를 이용하지 않았다.

S/PID_1684n002I.pdf PDF1을 렌더로 보았다. 해당 출구 영역에 MC04/M09·VS01·PV03는 표시되나 MC05/M10 본체 대응은 확보되지 않았다. R/equipment.json의 MC05 `pid=false`와 맞는 범위다. MC05의 공정상 정확한 설치 위치·투입/배출 역할을 인접 MC04나 VS01에서 복제하지 않는다. SS11의 기존 `pid=true` 속성 역시 본문에서 MC05 설치 근거로 승격하지 않는다.

## 1.2 deleted 제목의 정확한 증거 수준

| 블록·색인 순서 | 문서 ID | S/live_index.json `_7ev`, i 및 제목 | R/all-networks.csv의 원본 XML | 해석·한계 |
|---|---:|---|---|---|
| time work motor / 22 | 1023 | i1023, `mc-05 deleted` | 공란 | MC05 누적 네트워크의 실행 식 미확보 |
| hmi / 6 | 1183 | i1183, `mc05 deleted` | 공란 | MC05 HMI 함수핀/대상 바인딩 미확보 |
| allarms 1 / 13 | 1793 | i1793, `mc05 deleted` | 공란 | 전용 알람 네트워크·타이머 미확보 |
| motors 1 / 13 | 1942 | i1942, `mc05 deleted` | 공란 | 요청→Q0.5 최종식 미확보 |

네 색인 행의 객체 `deleted=false`와 사람이 붙인 제목 `deleted`는 다른 필드다. 네 행은 색인/빈 네트워크/기타 언어 분류이며, 이 조사에서 FlgNet 원문이 없으므로 실제 TIA에서 비어 있는지, 삭제 이력인지, 다른 언어/대체 블록이 있는지는 확정하지 않는다. 복원 범위 밖까지 포함한 “프로그램에 MC05 제어가 전혀 없다”는 주장도 하지 않는다.

## 1.3 판본·기존 충돌

- 전기 FG26/PDF27, FG117/PDF118, FG122/PDF123, FG136/PDF137은 시각 확인상 기본 날짜 27.05.2024, Rev2 / 17.03.2025다. FG와 PDF 페이지를 서로 바꿔 적지 않는다.
- P&ID PDF1의 문서 번호 1684n002 I와 이후 전기/시공 도면은 세대가 다르다. 최신 설치는 별도 준공·개조 기록이 필요하다.
- 백업 파일명 GME_20250506.zap18과 내부 GME_20250605.ap18의 기존 시점 차이, 주전원 표지/인덱스의 440/400V 표기 차이를 해결 완료로 바꾸지 않는다. 본 회로의 실제 표기는 440V 60Hz다.
- `start mc05` 설명의 과거 `a 49.2`와 선언/현 전기도면 Q0.5/A0.5를 구분한다. A49.2를 현재 주소로 채택하지 않는다.
- 기존 devices/MC05.html·control-spec의 일반 모터/인버터 점검 문구와 과거 시뮬레이터 항목은 MC05 인버터 설치·현재 보호 기능·시험 수행 증거가 아니다. 본 초안은 실제 FG26 접촉기 회로와 확보된 로직만 사용한다.

# 2. I/O·HMI·Word 전달

## 2.1 고유 선언과 주소

| 항목 | 주소/형식 | 직접 선언 및 참조 | 해석 / 미확정 |
|---|---|---|---|
| Start MC05 | %Q0.5 Bool | D/0556 R241, NID=-2147483648 UID119 AK=Monitor, SAD Output AO5. D/0555 R6 UID32에도 Monitor | 물리 출력 주소 선언. 최종 Coil 쓰기 증거가 아님 |
| MC05_Fbk | %I1.0 Bool | D/0556 R242, 같은 Monitor NID UID112, SAD Input AO8 | FG26의 26KM1 보조접점 피드백. 회전 검출기로 단정 불가 |
| MC05_torque | %I6.6 Bool | D/0556 R243, 같은 Monitor NID UID115, SAD Input AO54 | FG26 SS11. 실제 장치 종류·정상극성·전용 알람 처리 미확인 |
| Flag.M_MC_05 | DB2.DBX0.5 Bool | D/0577 R32, AO5, BAD BIRID3→D/0576 Flag R3 TOD DB2; NID3/O615 Write, NID4/O959 Write | 운전 요청 기억. 물리 Q0.5와 다른 영역 |
| hours motors.MC_05_HOUR | DB9.DBW98 Int | D/0615 R156 AO784/16bit, BAD5→D/0614 R5 TOD DB9; NID51/O2847 Write | 잔존 시간 필드. 확보된 쓰기는 0 Move이며 누적 미확보 |
| ON / OFF | %M0.0 / %M0.1 Bool | D/0575 R1/R62, SAD Memory AO0/1 | 논리 이름을 현재 TRUE/FALSE로 가정하지 않음 |
| Flag.Auto_ON1 | DB2.DBX7.3 Bool | D/0577 R4 AO59, BAD3→DB2 | 자동 요청 공통 비트 |
| Data.Tipo_preset / Tempo_presetting | DB1.DBW98 / DBW96 Int | D/0577 R12 AO784 / R7 AO768; BAD6→D/0576 Data R6 TOD DB1 | 값1/2와17/21 비교. 타이머 단위로 자동 환산하지 않음 |
| Allarm.Emergency_module_fault | DB3.DBX16.6 Bool | D/0577 R108 AO134; BAD107→D/0576 Allarm R107 TOD DB3 | 공통 자동 허가 접점. MC05 고유 고장으로 소유 변경 금지 |

AO는 여기서 bit offset으로 해석했으며 DB/영역·자료형을 함께 확인했다. DB1.DBW98와 DB9.DBW98는 서로 다른 필드다. 모니터 NID의 음수 예약값을 실행 LAD 네트워크 번호로 읽지 않는다.

## 2.2 원시 입력 → DB13 처리 사본

D/0397-FlgNet.xml, LAD1070, HMI Inputs NID1의 실제 Move 두 개를 D/0627·0628·0629 선언과 연결했다.

| 범위 | 입력 선언·핀 | Part/Wire | 출력 선언·주소 | MC05 중첩·한계 |
|---|---|---|---|---|
| IW0→DB13.DBW0 | D/0627 R3 Tag_178, Word Input AO0, O25 | W23→P22.in; rail W21→P22.en; P22.out1/W24→O26 | D/0629 R5 Word AO0 BAD4; D/0628 Inputs R4 TOD13 | I1.0 포함. DB13.X1.0의 Word 사본 경로까지 확인; MC05 명명 소비자/DB11 표시는 미확보 |
| IW6→DB13.DBW6 | D/0627 R13 Tag_171, Word Input AO48, O45 | W52→P42.in; rail W21→P42.en; P42.out1/W54→O46 | D/0629 R14 Word AO48 BAD4→DB13 | I6.6 포함. DB13.X6.6의 사본 경로까지 확인; 토크 고장 판단식은 미확보 |

이 두 Move는 en이 각기 W21 rail에 연결된다. 앞선 Move의 ENO에 종속되는 다른 Word를 이 두 개의 조건으로 복제하지 않았다. 상위 호출은 §3.4의 HMI Output ENO 및 NOT Simulation(1) 조건을 갖는다. 여기서 NOT Simulation(1)은 **기존 XML의 접점 인용**일 뿐 시뮬레이터 접근·생성·실행을 하지 않았다.

D/0544 Main LAD1614/NID1에는 IW6(Tag_171 D/0692 R1/O82)→P69.in/W92, P69.out1/W93→D/0690 R3/O83 Word_inputs.word1(AO0)의 다른 사본도 있다. D/0546 Main LAD1616/NID3 제목은 `word output`이지만, P144.in/W167/O157의 Tag_178은 D/0692 R21에서 **Input AO0 Word**다. P144.out1/W168/O158→D/0690 R23 Word_outputs.WORD1로 전달한다. 이름만으로 QW0 쓰기 또는 MC05 출력제어라고 판단하지 않는다. 이들 Word 컨테이너의 모든 소비 경로는 미추적이다.

## 2.3 Q0.5를 포함한 출력 Word 읽기와 DB 사본

D/0401, HMI Output LAD356/NID1의 P22는 다음과 같다.

- D/0632 R24 `Tag_280`, SAD Output, AO0, Word, O33 → W56 → P22.in.
- W21 rail → P22.en. P22.out1 → W58 → O34/R27.
- D/0633 R27는 Word AO0, BAD BIRID26. D/0064의 Output DepDBBlock R26, TOD DB14와 결속한다.
- 따라서 QW0→DB14.DBW0 **읽기 사본**이며 Q0.5도 범위에 든다. 이 Move는 Q0.5를 쓰는 출력 명령이 아니다. DB14.X0.5를 DB11.X10.0에 직접 등치시키지 않는다.

명명 Bool 외 Word 쓰기 검토에서 확인된 MC05 요청 덮어쓰기는 §3.3의 DB2.DBW0다. 출력 범위와 겹치는 QW0 선언은 위 사본의 입력측이다. 이것은 모든 간접주소·BLKMOV·복원되지 않은 원문·외부 HMI 쓰기까지 배제한 전역 Writer 완전성 선언이 아니다.

## 2.4 HMI 설정과 미결속 경계

S/hmi_plc_tags.csv와 R/equipment-hmi.csv의 MC05 세 행은 아래와 같다. CSV 자체가 `dde.cfg 설정; 온라인 현재값 아님`이라고 한정한다. 원본 dde.cfg/화면 프로젝트는 이번 고정 작업트리에서 별도로 확보하지 못했다.

| HMI 태그 | 설정 주소 | Access / 내부 ID | 확인 가능한 의미·남은 경계 |
|---|---|---|---|
| MC_05\Flag | DB2,X0.5 | PLC / 001AF | PLC Flag.M_MC_05 주소와 일치. 버튼·이벤트·양방향 쓰기·접근권·현재값 미확인 |
| MC_05\RispostaA | DB11,X10.0 | PLC / 00323 | 표시용 설정 이름. I1.0/DB13.X1.0/Q0.5 중 어느 피연산자를 받는지 미결속 |
| MC_05\Allarme1 | DB11,X10.1 | PLC / 0003F | 표시용 설정 이름. MC05 전용 FAULT 또는 토크 알람 생성의 증거 아님 |

HMI LAD1183의 deleted 제목에는 대응 XML이 없으므로 MC04의 hmi standard motors 호출핀이나 알람 묶음을 복사하지 않는다. DB11 byte10에는 여기서 임의 신규 태그나 알람을 배정하지 않는다. HMI 버튼을 눌러 확인하거나 PLC/HMI 값을 바꾸는 시험은 하지 않았다.

# 3. 제어 구조·복수 쓰기·호출

## 3.1 예열은 Reset: D/0164 / LAD1843 / NID3

MC05 관련 분기 식은 다음의 정적 연결이다.

`ON AND NOT Allarm.Emergency_module_fault AND (Data.Tipo_preset = 1) AND Flag.Auto_ON1 AND (Data.Tempo_presetting = 17) → Reset Flag.M_MC_05`

| 경로 | 실제 원본 위치·선언 | 해석 / 미확정 |
|---|---|---|
| 선행 허가 | rail W793→P785 Contact; O588/R1 ON/W668. P785.out/W786→P22 Contact, operand Negated, O23/R108/W21 | ON과 공통 비상모듈 고장 반전 직렬 |
| 예열 모드 | P22.out/W32→P400 Eq.pre; O590/R12/W670→in1, O591/R8/W671→in2 | Data.Tipo_preset=1. 상수는 D/0578 R8 NID3/O591 |
| 자동 요청 | P400.out/W33→P823 Contact; O824/R4/W826→operand; P823.out/W672→P452 Eq.pre | Flag.Auto_ON1 허가 |
| 값17 비교 | O612/R7/W703→P452.in1; O613/R30/W704→in2 | 상수17은 D/0578 R30 NID3/O613 |
| MC05 Reset | P452.out/W705→P458 **RCoil**. O615/R32/W707→operand | 요청 Reset. 같은 W705의 MC04/VS01/Enable_R2_GATE RCoil은 각각 별개 대상 |

NID3/O615의 D/0577 AK=Write만으로 Set/Reset을 구분할 수 없고 반드시 P458의 Gate=RCoil을 함께 읽는다. 값17을 “MC05를 17초 뒤 기동”으로 표현하면 틀린다.

## 3.2 생산은 추가 OFF가 있는 Set: D/0165 / LAD1844 / NID4

`ON AND NOT Allarm.Emergency_module_fault AND Flag.Auto_ON1 AND (Data.Tipo_preset = 2) AND (Data.Tempo_presetting = 21) AND OFF → Set Flag.M_MC_05`

- rail W1153→P1145 ON Contact(O932/R1/W1017)→W1146→P1154 반전 Emergency 접점(O1155/R108/W1157).
- P1154.out/W21→P1147 Auto_ON1 Contact(O933/R4/W1018)→W1148→P737 Eq.pre.
- P737.in1/W1019/O934/R12=Tipo_preset, in2/W1020/O935/R78=상수2(D/0578).
- P737.out/W1021→P789 Eq.pre. in1/W1052/O956/R7=Tempo_presetting, in2/W1053/O957/R37=상수21(D/0578).
- P789.out/W1054→**P1149 Contact**; operand W1055/O958/R62=OFF(%M0.1), 반전 표시 없음.
- P1149.out/W1150→P793 **SCoil**; operand W1057/O959/R32=Flag.M_MC_05, D/0577 NID4 AK Write.

OFF 이름만으로 현재 FALSE라거나 이 분기가 영구 불능이라고 확정하지 않는다. 반대로 OFF를 제거한 정상 자동 기동식으로 표시해서도 안 된다. 인접 MC04는 값24의 별도 분기이므로 MC05의 예열/생산 상수를 MC04/VS01과 혼합하지 않는다.

D/0166/LAD1847의 complete engine stop 네트워크도 MC05 소유 경계 확인용으로 읽었다. MC04·VS01 등 다른 대상의 RCoil은 있으나 이번 MC05 명명 선언 R32의 NID5 사용은 없다. 이를 MC05 Reset으로 옮기지 않는다. CPU 전체의 정지 수단 부재를 증명하는 결과는 아니다.

## 3.3 이름 없는 Word 덮어쓰기: D/0147 / LAD402 / NID2

`startup only`의 DB2.DBW0 쓰기는 다음과 같이 M_MC_05(DB2.X0.5)와 중첩한다.

- W210 rail→P208 Contact.in. D/0047 R1, NID2/O167, ON(%M0.0)→W184→operand.
- P208.out/W209→P138 Move.en.
- D/0048 LiteralConstant R54, Int16, `INT#0`(원문 SV=INT_x0023_0, V=0), NID2/O168→W185→P138.in.
- P138.out1/W186→O169/R7. D/0563 R7는 16bit Word, AO0, BAD BIRID6→D/0562 Flag DepDB R6 TOD DB2.
- DB2.DBW0의 byte0..1 범위가 X0.5를 포함하므로 이 쓰기가 실행되면 요청 비트도 0쓰기 대상이다. 이는 명명 RCoil과 별도 Writer다.

이 XML의 제목/색인만으로 실제 시작 OB, Warm/Cold/Retain 동작, 현재 호출 횟수·순서나 최종값을 확정하지 않았다. 뒤의 자동 Set/Reset과 HMI 이벤트, 간접 쓰기의 우선순위도 별도다. DB3 초기화 Word가 있다고 MC05 전용 알람 주소를 만들어 중첩표에 넣지 않는다. DB11 표시 비트도 DB2/DB3 초기화와 다른 영역이다.

## 3.4 상위 호출과 실행 경계

| 호출 | 원본 핀·선언 | 확인 / 미확정 |
|---|---|---|
| Auto start motors | D/0024 LAD1723/NID4, rail W190→P188 ON Contact(O185 D/0652 R36/W187), out W189→호출 인터페이스 CRef183.en. D/0068 R40, D/0067 FCBlock R39 CodeBlock UID186, TOD FC30 | 블록명 `cyc_int2 ogni 1s` 안 ON 허가 호출. 이름만으로 현재 CPU 주기1초·할당 OB·활성 확정하지 않음 |
| Motors 1와 time work motor | D/0549 LAD1620/NID7, rail W352→P350 ON(O335 D/0692 R52/W348); P350.out W351은 CRef319(Motors1).en과 CRef334(time work motor).en 등으로 병렬 연결. D/0694 R68/R83, D/0688 FC7 R67 UID337 / FC2 R82 UID347 | 두 호출을 직렬 ENO 연쇄로 설명하지 않음. Motors1 호출 존재가 deleted MC05 출력식을 복원하지는 않음 |
| HMI→출력사본→입력사본 | D/0030 LAD1613/NID19: rail W31→Recipes Handler CRef21.en; W32→HMI CRef23.en; W33→HMI Output CRef25.en; W42→P37 반전 Simulation(1) Contact(O45 D/0692 R140/W44); W43→HMI Inputs CRef28.en. D/0688 HMI FC11 R124/UID24, HMI Output R128/UID26, HMI Inputs FC15 R135/UID29; D/0694 대응 인터페이스 | 전 단계 ENO와 반전접점 존재. 실제 호출/온라인값은 미검증. HMI FC가 호출돼도 MC05용 네트워크 결속은 미확보 |
| Startup Word | D/0147 자체의 ON/Move 허가 | 상위 시작 OB·재시작 이벤트 연결은 이번 자료에서 미확보 |

같은 문서의 index_order, NID 숫자, 파일 번호는 다른 블록을 가로지르는 CPU 실행순서 증거가 아니다. 요청→허가→최종 출력→접촉기→실물→피드백→표시 중 **요청→최종 Q**와 **처리 피드백→MC05 표시·알람**의 PLC 연결은 열린 경계다.

## 3.5 운전시간 잔존0쓰기와 공유 타이머

D/0336, LAD1049/NID51은 Tag_48 접점 뒤 다섯 Move가 ENO로 직렬 연결된다.

- Tag_48: D/0613 R284, Timer/SAD Timer AO17 = %T17. O2837/W2848→P2863 Contact. rail W2865→P2863.in, out W2864→P2822.en.
- P2822(RD01)→W2851→P2825(RD01 FAN)→W2854→P2828(MC03)→W2857→P2831(MC04)→**W2860→P2834.en**.
- MC05 경로: D/0616 LiteralConstant R12, V=0, NID51/O2846→W2861→P2834.in; P2834.out1/W2862→O2847/R156→D/0615 MC_05_HOUR(DB9.DBW98, Int).
- 앞 네 Move의 성공/ENO는 현재 실행 결과로 검증하지 않았다. P2834의 정적 동작은 **0 Move**, MC05 MIN 증가·HOUR 누적·현재 누적시간의 정상성은 미확보다.

T17 생성·해제의 공통 원문 D/0341 LAD1055/NID57도 구분했다.

| 공통 경로 | 원본 | 해석·한계 |
|---|---|---|
| 기억 Set | ON P3147.out/W3148→Flag_Aggiorna_DB P3149→W3150→SCoil P3110, operand O3126/W3136 | D/0613 R13 Flag_Aggiorna_DB %M1.7, R332 MEM2_0 %M2.0. 기록 갱신 공통 경로 |
| 공유 지연 | ON→MEM2_0 P3151→W3152→NOT Flag_Aggiorna_DB P3153→W3154→SdCoil P3118; value O3128/R334/W3138=D/0616 S5T#5S; operand O3130/R284/W3141=T17 | 공유 시간초기화 타이머. MC05 고장·토크·피드백 알람의 5초 지연이 아님 |
| 기억 Reset | P3151.out/W3152→T17 Contact P3155(O3131/W3142)→W3156→RCoil P3123(O3132/R332/W3144) | MEM2_0 해제. MC05 요청 또는 알람 Reset과 구분 |

# 4. 전기 전달 경로: 실제 PDF 페이지

## 4.1 FG26/PDF27, SPARE 접촉기 회로

페이지 전체 SPARE 점선 안에 전원·모터·명령·피드백·SS11이 같이 있다. 그림의 보존은 현재 접속/가동 증거가 아니다.

| 경로 | 도면 양 끝점과 기기·선 | 해석 / 미확정 |
|---|---|---|
| 3상 주회로 | 8.3L1/L2/L3(좌 FG23/9, 우 FG29/0)→26QM1 1–2/3–4/5–6→26KM1 1–2/3–4/5–6→26U1/26V1/26W1→XM 26U1/26V1/26W1→26QS1 1–2/3–4/5–6→M10 U/V/W, PE | 도면 440V60Hz, M10=MC-05, 1.5kW·3.03A. 모터/컨베이어 실물 동일성·정격은 명판 확인 전 |
| 보호/도체 | 26QM1 옆 `2,8-4A`, `BLACK FS17 1,5 mmq` | 보호기 조정 범위와 도면 도체 규격. 현행 모델·실제 세팅·차단능력·배선 적합성 확정 아님 |
| 명령 코일 | FG136/1 A0.5→XS11→26QS1 보조접점→XS12→26QM1 보조접점→26KM1 A1; A2→-0Vdc 10.6 | Q 출력만으로 코일 여자 보장 안 됨. QS/QM 보조접점 상세 번호는 이 그림에서 별도 판독하지 못했으므로 추정 번호를 넣지 않음 |
| 피드백 | +24Vdc 10.7→26KM1 보조접점 13–14→E1.0→FG117/2 | 접촉기 보조접점 응답. 모터 실제 회전·체인 이송·토크 정상의 직접 센서 아님 |
| SS11 | +24Vdc 10.7→X1:56, 5×20 2A F→선26.2→SS-11 접점11–12→X1:57→E6.6→FG122/6 | 도면 LIMIT SWITCH TORQUE CONTROL. 접점 기호/번호를 물리 정상극성·안전 등급·PLC 트립 논리로 승격하지 않음 |

+24Vdc10.7 / -0Vdc10.6의 페이지 연결은 좌FG25/9, 우FG27/5다. 26KM1 코일은 A1/A2가 24Vdc 제어망에 연결된다. 실제 전압 측정이나 통전 조작은 수행하지 않았다.

## 4.2 PLC 쪽 끝점

| FG/PDF | 실제 표시 | MC05 끝점·경계 |
|---|---|---|
| FG136/PDF137 | DIGITAL OUTPUT MODULE, CPU515 MOD14 | A0.5 단자6→FG26/4. MC-05 MOTOR COMMAND이며 이 선이 SPARE 점선 안에 있음. 모듈 급전은 +24Vdc10.9→X21:3028 5×20 4A F→단자9, 단자10→0V10.6 |
| FG117/PDF118 | DIGITAL INPUT MODULE, CPU515 MOD8 | E1.0 단자11←FG26/6, FEEDBACK MOTOR MC-05. 해당 입력 SPARE 표시. 전원 +24Vdc10.7→X21:3006 5×20 2A IST.→단자19, 0V10.6→단자20 |
| FG122/PDF123 | DIGITAL INPUT MODULE, CPU515 MOD9 | E6.6 단자27←FG26/7, LIMIT SWITCH SS-11. E6.4/5/6 묶음이 SPARE. SS09/SS10을 SS11 소유로 합치지 않음 |

위 단자 번호는 원본 도면의 모듈 그림 표기이며 현재 장착 모듈의 주문번호/실물 커넥터 확인이 아니다. 현장 교차참조·안전전원 차단의 전체 성능까지 판정하지 않았다.

## 4.3 시공 참고 케이블·소유 상충

원본 S/Electrical_Can_Decoating_20241118.pdf의 PDF34·51·59를 실제 렌더로 대조했다. 모두 24.11.11 first draft design이며 승인 준공 자료로 대체하지 않는다.

| 페이지 / 행 | 원문 연결 | 해석과 보존할 문제 |
|---|---|---|
| PDF51, 1_19 | `=EXI+MC05-M10A`, FROM CR→TO MC-05/M10, METALLIC CONVEYOR, GAC, CV 4core 1.5, SPARE0, route100/120/121/122/EXI1TB1/E200, adjustment15, LEN87 | 도면의 길이표기87은 현장 실측 아님. MC04의 DAC/PVC-S4×16SB 행1_18과 다른 행 |
| PDF34, 1_19 | EXI1TB1 경로, EXPOSED CP01 No.2 Pipe22, M10, CV1.5/4core | 표와 스케치의 설계 대응. 정확한 현장 단자핀은 전기 FG26과 별도 |
| PDF59, 9_3 | `=EXI+MC05-EXI1TB2A`, EXIT/EXI1TB1→MC-05/EXI1TB2, SS10/11, DC CVV7G1.0, spare2, E350, adjustment15, LEN16 | MC05 명칭의 JB가 MC04 SS10·MC05 SS11 둘 다 전달. JB 이름은 두 센서의 단독 PLC 소유 증거가 아님 |
| PDF59, 9_8 | `=EXI+MC04-SS11A`, FROM MC-05/EXI1TB2→TO MC-05/SS-11, DC CVV2C1.0, spare0, E351, adjustment3, LEN3 | 케이블 이름의 MC04와 목적지 MC05/SS11 상충을 그대로 보존 |
| PDF34, 9_8 | MC-05 SS-11, 동일 `=EXI+MC04-SS11A`, CVV1.0/2core | PDF59와 같은 이름 상충. SS11을 MC04로 재분류하지 않음 |

S/Electrical_Rev2.pdf의 X1:56/57과 시공 PDF59의 EXI1TB2 사이에 실제 코어 번호·JB 단자핀을 연결하는 완전 준공표는 미확보다. 계획 케이블과 전기 접점 양 끝점이 존재한다고 현장 전 경로 연결 확인 완료로 세지 않는다.

# 5. 알람·정지·복구의 확인 범위

## 5.1 확보하지 못한 전용 보호 로직

MC05 이름 검색 결과, 복원 선언과 연결 네트워크에서 MC05 전용 FAULT/INV/토크 알람 대상·전용 모터 타이머·고유 Reset 식을 확보하지 못했다. allarms1 문서1793은 deleted 제목이고 XML이 연결되지 않는다. 원시 MC05_torque I6.6 및 HMI Allarme1 DB11.X10.1의 존재만으로 아래를 작성하면 안 된다.

- “요청 후 피드백이 없으면 5초 뒤 FAULT”: MC05 근거 없음
- “SS11 작동은 요청 Reset 및 상위 MC04 정지”: MC05 근거 없음
- “Reset_ALLARM 누르면 MC05가 자동 재기동”: MC05 근거 없음
- “인버터 고장을 리셋하면 복구”: FG26은 접촉기 회로이며 MC05 인버터 선언/회로 미확보

공통 Emergency_module_fault는 자동 요청 분기 허가에 실제 연결된다(§3.1·3.2). 이 사실을 MC05 전용 안전기능 인증·전원차단 성능·고유 고장으로 확장하지 않는다. 기계보호/전기보호/PLC 알람/HMI 표시는 각각 별도다.

## 5.2 복구 판단

이번 결과는 복구 절차 승인서가 아니다. 현장 운전 승인 없이 요청·Reset·OFF·보호 설정을 바꾸거나 출력 강제하지 않는다. 복구를 표시하려면 설비 설치 여부, 실제 M10/SS11·QS/QM/KM, 현재 PLC 프로젝트/최종 출력식, HMI 이벤트, 고장 원인과 승인된 조치, 재시작 조건 및 운전 결과를 담당자가 확인해야 한다. 단순 문서 정적 대조나 DB bit 해제만으로 기계·공정 복구를 판정하지 않는다.

# 6. 증상별 수리·관찰 초안

| 증상/질문 | 수집할 관찰과 비교 근거 | 구분할 원인·미확정 | 완료 증거 |
|---|---|---|---|
| MC05가 실제 있는가 | MC05/M10 명판·설치위치·철거/예비 표식, 최신 승인 준공도; FG26 SPARE 및 시공34/51 대조 | deleted/SPARE가 자료상의 비사용인지 실제 철거인지 | 현장 식별·변경이력, 담당자와 시각 |
| HMI 요청은 켜지지만 기동 안 됨 | DB2.X0.5·HMI 설정/이벤트, Tipo/Tempo·OFF 관찰, 현재 Q0.5 작성 블록 | 예열 RCoil·생산 OFF 조건·Startup DBW0·HMI 쓰기 충돌과 최종 출력식 부재를 분리 | 현재 프로젝트의 읽기 전용 교차참조와 시각동기 관찰 |
| Q0.5와 접촉기 응답이 다름 | FG136 단자6, FG26 XS11/12·QS/QM 보조접점·KM A1/A2; 자격 있는 담당자의 승인된 측정 | 출력 주소/단자/전원/중간접점/코일 상태 각각 | 안전하게 수집한 실제 끝점/전압/상태·조치 기록 |
| 접촉기는 켜졌으나 실제 이송 안 됨 | KM13–14 피드백 I1.0와 실제 M10/체인 상태를 별도 관찰 | 보조접점은 회전·이송 센서 아님 | 명판/회전·이송 관찰과 승인 정비 기록 |
| 토크 이상인데 HMI 알람이 없음 | SS11 장치/접점 상태·X1:56/57·I6.6·DB13.X6.6·DB11.X10.1 | 원시 접점 단선/극성, 소비 로직 부재, HMI 바인딩 부재 | 현재 프로젝트의 입력→알람→표시 결속 자료 |
| 운전시간이 0 또는 불연속 | DB9.DBW98, T17/MEM2_0/Flag_Aggiorna_DB와 기록 시각 | 0336의0쓰기와 deleted 누적네트워크를 구분. 누적값 임의 복구 금지 | 원본 시간기록과 현재 writer·호출 증거 |
| SS11 케이블에 MC04라고 적힘 | 9_8 케이블 양 끝, EXI1TB2·현장 태그; 시공59와 전기FG26 | 명칭 상충·JB 공유를 실물 소유로 자동 치환하지 않음 | 최신 승인 케이블/단자표와 실제 표찰 사진 |

기록 항목은 관찰자, 날짜·시각·시간대, 정확한 대상/위치, 값·단위, 수집 도구·방법, 프로그램/도면 판본, 비교 원문, 배제한 원인, 승인된 조치, 복구 확인자·증거다. 여기서는 실제 운영 기록·사진을 만들거나 공개 저장소에 복사하지 않았다.

# 7. 검토·완료 기준과 인계

## 7.1 네 기능 및 보존

| 기능 | 이번 범위 | 실제 상태 |
|---|---|---|
| 도면·래더 나란히 비교 | MC05 원본쌍 후보: FG26/117/122/136와 예열/생산/Word 전달. 삭제 제목은 XML 없음 표시 필요 | UI 구현·링크 시험 미수행 |
| 백업·선택 복원 | 기존 note/repair_observation·unknown field·타설비·초안·저장 키 보존 | 브라우저 기록 접근·저장·복원 미수행 |
| 기록 전후 비교 | 관찰 항목·판본·시각의 분리 요구만 작성 | 실제 비교 UI 미수행 |
| 보고서/PDF | 이 MD는 문서 초안 | 사용자 기록 기반 보고서 생성·PDF 출력 검증 미수행 |

## 7.2 실제 수행과 의미 검토 수

- Git HEAD 및 상태 확인: 지정 고정커밋, 조사 전 변경 없음. 종료 때도 이 읽기 전용 소스의 상태·Git blob 대조를 확인한다.
- 저장소 preflight.py를 읽고 읽기 전용 기본 검사만 수행했다. 종료0, inventory_matches=true, catalog248/제외90/부모보류7/phase2후보133. source_byte_changes는 requirements-audit.json, all-in-one-data.json 두 경로이며 고정v1.12.0에 이미 있는 기존 표준 스냅샷 대비 바이트 차이다. MC05대장을 변경하거나 이를 MC05 완료로 해석하지 않았다.
- 선택 XML Part/Wire/ORef/CRef와 선언 NID/RID/UID/AO/BAD/TOD 대조를 수행했다. 대상 식과 전달 방향을 텍스트 구조로만 점검했고 제어 실행/모의 모델은 작성·실행하지 않았다.
- **의미 검토:** FlgNet 13개에서 본문에 쓰인 MC05 및 공통 경계만 확인했다(0164,0165,0166,0336,0341,0147,0397,0401,0024,0030,0549,0544,0546). IdentXmlPart 27개에서 관련 선언·상수·블록을 확인했다. 이 40 XML의 다른 설비 전체 로직을 검토했다는 뜻은 아니다.
- **도면 의미 검토:** 전기4쪽, 시공3쪽, P&ID1쪽 = 실제 렌더8쪽. 페이지 수와 새 설비 완료 수를 합산하지 않는다.
- 전체 181 IdentXmlPart 검색은 MC05 명명 선언 탐색용이다. 검색 범위·해시 수는 의미 검토 수가 아니다. 네트워크 색인426개와 원본730개 전체를 의미 검토 완료했다고 하지 않는다.
- 이번에 포착한 주요 함정: 예열은 Reset, 생산에는 OFF 직렬접점, 시간은0쓰기, QW0는 DB사본 입력, `word output` 제목의 입력이 IW0, HMI Allarme1은 전용 알람 증거 아님, SPARE와 현재 비설치 구분, MC04 문자열 SS11 케이블의 소유 상충.

## 7.3 다음 검토자가 확인할 자료

1. MC05/M10/SS11이 현재 설치·예비·철거 중 무엇인지, 최신 준공 및 변경 기록으로 결정한다. 문서 제목만으로 제외/병합하지 않는다.
2. 원 TIA 프로젝트의 Motors1 문서1942·Allarms1 1793·HMI1183·Time1023의 실제 블록 상태를 읽기 전용으로 대조한다. 요청→Q0.5·피드백/토크→알람→DB11의 대체/간접 경로가 있는지 확인한다.
3. 생산 OFF 접점의 현재 의도·M0.1 writer 및 동작 경계, Startup/자동/HMI 쓰기·Retain/재시작·호출 우선순위를 원 프로젝트에서 확인한다. 원문 근거 없이 OFF 접점을 제거하거나 0/1 값을 가정하지 않는다.
4. 실제 HMI dde.cfg·화면 이벤트·통신 대상 및 DB11 MC05 구조 결속을 확보한다. DB2/DB11/DB13/DB14의 주소/역할을 분리한다.
5. 26QM1/QS1 보조접점 번호, 설치 M10 명판·보호기 모델/현행 설정, SS11 종류/접점·정상극성, X1↔EXI1TB2 코어/단자표를 승인 자료로 확인한다.
6. 시공59 9_8의 `MC04-SS11A`와 MC05 목적지 상충을 현장 표찰·최신 도면으로 판정하고 기존 원문을 보존한다.
7. 코드/UI/대장 반영은 사용자 지정 통합 작업의 별도 승인 범위에서만 한다. 이번 문서로 로컬2차133 제외나 완료집계를 바꾸지 않는다.

## 7.4 상태 분리

| 상태 축 | 결과 |
|---|---|
| documentation | MC05 7영역 조사 초안 작성, 소유/충돌/미확정 포함 |
| static_review | 선택 XML·선언·실제 PDF의 범위 한정 대조. 독립 통합 검토는 후속 |
| ui_records | not_run |
| publication | not_published, 코드 통합 없음 |
| tia_compile | not_performed |
| live_cpu | not_performed |
| field_recovery | not_performed |

# 부록 A. 원본·참고 파일 바이트 지문

아래 SHA-256/Git blob은 **기준 파일의 바이트와 고정커밋 일치**를 뜻한다. 해시 파일 수를 원본 의미 검토·타이머 검증·설비 완료 수로 세지 않는다. PDF의 의미 검토는 위 지정8쪽뿐이며 ZAP/PLF는 보존 지문만 검사했다. HMI CSV·검색 색인·파생 제어 명세는 해당 성격을 유지한다.

총 65개 파일의 SHA-256과 Git blob을 계산하여 모두 고정 HEAD와 일치했다. 이 중 중지5자산은 바이트 해시만 검사하여 보존 기준과도 일치했으며 실행하지 않았다. 관련 의미검토는 선택 XML40개·PDF8쪽으로 별도다.

| 파일 | SHA-256 | Git blob |
|---|---|---|
| `all-in-one/sources/decoded-original/0164-FlgNet.xml` | `15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491` | `1035a51ee3100d524da1b7b204ba142b6b509ac5` |
| `all-in-one/sources/decoded-original/0165-FlgNet.xml` | `4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88` | `8d636eb535060037ccf00ebdfb328b8775225fe4` |
| `all-in-one/sources/decoded-original/0166-FlgNet.xml` | `0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853` | `6b3062ae9ac2bc6ad8c2509d3fc4c15609a4b892` |
| `all-in-one/sources/decoded-original/0336-FlgNet.xml` | `1be4f76dba11e6cceea057743c8b15b8a4bea4edfe87c19ef0581d7b65ffe56a` | `3bb3ae34dc100f7a9483cf8bf7702c01e080371d` |
| `all-in-one/sources/decoded-original/0341-FlgNet.xml` | `e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96` | `45dbda06a692b21380a52207a22094b2e0a9c5a3` |
| `all-in-one/sources/decoded-original/0147-FlgNet.xml` | `386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c` | `0027890eca158e714dd6260dc920a5d3aa83319b` |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` |
| `all-in-one/sources/decoded-original/0401-FlgNet.xml` | `60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae` | `aadefbd35d305dd4a1146bf383b988a903802bf4` |
| `all-in-one/sources/decoded-original/0024-FlgNet.xml` | `a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67` | `379ccbabf7692e1df137b99bab1992dea22cc1f0` |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` | `985b5310b43b1015b5dee286aa0e42800564b94b` |
| `all-in-one/sources/decoded-original/0544-FlgNet.xml` | `7eea2ea628a9c9ba7b9df66e20f7bab670da7dc7a155084d80119943ed45e6ca` | `99409858956641861deaf6e727522385febf1b21` |
| `all-in-one/sources/decoded-original/0546-FlgNet.xml` | `14d5214e135425b0499d8533926bc10b3d8b6e240b1fabc8def41d1cdb163f95` | `6ae5bca8179c9c6a9d9ed4f1104ddbd65055bbce` |
| `all-in-one/sources/decoded-original/0555-IdentXmlPart.xml` | `46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6` | `9a915a8b9a260b48402df151c1fe0bbcb2f4ea1c` |
| `all-in-one/sources/decoded-original/0556-IdentXmlPart.xml` | `065d71114e26c93af180265e0e6d59d2a190af1f2f0581c5265e7f4f67d6e23f` | `15ae569ff390ef5c791b0f76d96bd86d5ec6b938` |
| `all-in-one/sources/decoded-original/0575-IdentXmlPart.xml` | `40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06` | `07d5d2548e8f36252a346d0b83341e27c3cb14ba` |
| `all-in-one/sources/decoded-original/0576-IdentXmlPart.xml` | `c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe` | `819b47160eaa6d08c212f71e5b5486ef5b55b6f2` |
| `all-in-one/sources/decoded-original/0577-IdentXmlPart.xml` | `511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47` | `a505ebf7efd05a85850dc29559a4f71242bacae3` |
| `all-in-one/sources/decoded-original/0578-IdentXmlPart.xml` | `0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b` | `070a79fb12139898dd44a17ab2061e795956b9c6` |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` |
| `all-in-one/sources/decoded-original/0613-IdentXmlPart.xml` | `09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb` | `c9d19a48e947098914f4d2de3348c05b4f6d37e8` |
| `all-in-one/sources/decoded-original/0614-IdentXmlPart.xml` | `c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294` | `da0485aa033700f08c8695d30b93ebd2d377d6c7` |
| `all-in-one/sources/decoded-original/0615-IdentXmlPart.xml` | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` | `49eb86fe01feb83de8c0864b21493d305aff8b20` |
| `all-in-one/sources/decoded-original/0616-IdentXmlPart.xml` | `650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d` | `9f7fdd5f93ac149c139a054ebb34f63c632ef7fd` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` |
| `all-in-one/sources/decoded-original/0064-IdentXmlPart.xml` | `ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d` | `300d74239868f4f4595d4d5bbb848b4b58bbae76` |
| `all-in-one/sources/decoded-original/0632-IdentXmlPart.xml` | `fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9` | `600935fa8d394c0d247ea20040d5dfff4f05b500` |
| `all-in-one/sources/decoded-original/0633-IdentXmlPart.xml` | `9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc` | `a1ab5ee12addbc92d04c9950d4437e2b564d6b5c` |
| `all-in-one/sources/decoded-original/0067-IdentXmlPart.xml` | `0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628` | `455f00638f1618f194b1c83d9c0c2f157663a902` |
| `all-in-one/sources/decoded-original/0068-IdentXmlPart.xml` | `0a71d492e69760390b99f71a75f02ef684e271554b003d5de8bf64a26c64eeba` | `abf1e8cf672afee026f7945219fcee8ad62c9787` |
| `all-in-one/sources/decoded-original/0652-IdentXmlPart.xml` | `251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692` | `eee49f8301a6791748de9ab368159af8e8bc1585` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` |
| `all-in-one/sources/decoded-original/0690-IdentXmlPart.xml` | `fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541` | `36bd403f48ba8e364126837b19fb0419bbe78941` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `all-in-one/registers/all-networks.csv` | `7b6a9fc46f56c1bec7c4c7136792e2fc470fd07c15aa885d4f411c478d5e5f7c` | `cd54feb06ebcbea0c56ccb1226707799be084e16` |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` |
| `all-in-one/registers/equipment-io.csv` | `a7a1f27dc453af25b2b729074cac5266d6dd53c0945a6a1a4afe2dd1e9153b6a` | `d042a15edd5f2550dbbef40203f927da3360fe32` |
| `all-in-one/registers/equipment-hmi.csv` | `2cdce600aa0138cc5025022e57d9d61a948afb237f70c70e2d11e8300e73286a` | `aca60d300d26fd2bccd6d3970822c3aed2ecdb87` |
| `all-in-one/registers/plc-symbols.csv` | `a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f` | `cbc576c5d6e47498a3865304a1c23de9b4641d9f` |
| `all-in-one/registers/control-spec.json` | `1e495b32f1f11b910919fbd2945e842a019fce9a27a6a0d7298041a7fab00079` | `c7889fa3271dfd0043057dcaf486f4acae243b16` |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` |

## 부록 B. 정적 구조 검사와 종료 경계

선택 원본에서 20개 구조 단언(예열 RCoil, 생산 OFF+SCoil, DB2 Word중첩, 시간0쓰기, 공유 SdCoil5초, 입출력 Word 전달방향, 호출핀)을 대조해 통과했다. 이것은 XML 문서 구조 검사이며 PLC 논리 실행·시뮬레이터·현장시험이 아니다. 선언181파일 탐색에서 MC05 명명 요소는 6개(동일 Start MC05의 모니터 선언2개 포함)였다. 6을 독립 신호6개나 설비 완료6개로 세지 않는다.

원본 Git 상태 변경0, 고정 HEAD 동일. 문서 작성만 완료했으며 배포 커밋·현장 복구 결과는 없다.


## 전달 전 핵심 근거 제한 대조
2026-10-11 원본의 고유 허가/요청쓰기 Part와 선언을 표본 재확인하고 해당 모터 전기도면 실제 렌더의 SPARE·구동·응답·토크 끝점을 재확인했다. 인용 원본 SHA256을 모두 재계산하여 일치했다. 전체 원본 의미 검토, 현재 CPU·설치·현장복구·통합·게시 검증을 뜻하지 않는다. 미결속·미확정은 유지한다.
