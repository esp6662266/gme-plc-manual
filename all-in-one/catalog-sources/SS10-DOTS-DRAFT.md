# SS10 이송 장치 감시 스위치 — 독립 조사 초안

## 먼저 확인할 핵심·상충·누락

- SS10은 MC04의 하위 catalog ID다. 부모 완료를 상속하지 않는다. 원시 `MC04_torque` %I6.5, `Inputs."MC04 torque"` DB13.DBX6.5, `Allarm.MC_04_TORQUE` DB3.DBX3.5는 서로 다른 계층이다.
- 0429/NID13은 `OFF AND NOT Inputs."MC04 torque"`로 Set, `OFF AND Flag.RESET_ALLARM AND Inputs."MC04 torque" AND Allarm.MC_04_TORQUE`로 Reset한다. OFF는 상수 FALSE가 아니라 Global %M0.1 선언이다. 현재 값·활성 여부를 추정하지 않는다.
- 고유 네트워크 0429에는 타이머·CRef·환산이 없다. 부모 MC04의 0428/Tag_57/T54/5초는 RUN/INV 감시이며 SS10 지연으로 복제하지 않는다.
- OEM FG25/실제PDF26와 FG122/실제PDF123는 SS10을 SPARE로 표시한다. LAD 색인의 제목은 `mc04 deleted`이나 해당 레코드 deleted=false, XML S/R은 남아 있다. 설치 중/미설치/삭제 완료 어느 쪽도 확정하지 않는다.
- 시공 PDF34의 SS10 LOC MC-05와 PDF59 row9_7의 FROM MC-05 EXI1TB2 → TO MC-04 SS-10을 그대로 구별한다. 접속함 위치와 감시 대상이 다른 표기일 수 있으므로 곧바로 오배선으로 판정하지 않는다.
- 실제 센서 종류·제조사·정상 극성·현재 설치·HMI 전용 표시/이벤트·온라인 호출·최종값·현장 복구는 미확인이다.
- 기존 `MC04-DOTS-DRAFT.md`는 원본 위치 색인으로 재사용했다. 부모 초안 기준은 10051ddf/v1.7.0이고 이번 기준은 abcf31c/v1.12.0이다. 공통 근거는 아래 SHA 일치 표시로 파일 단위 동등성을 확인했으며 SS10 핵심 선언·핀·실제 도면은 다시 읽었다. 부모 전체 논리 재검증을 주장하지 않는다.

## 1. 설비·자료 기준

| 항목 | 확인 내용 | 경계 |
|---|---|---|
| 대장 | INVENTORY.json catalog[111], SS10/sensor/계측/parent MC04/phase2/planned | parent_child_separate; 실물동일성 미확인 |
| 별칭 | plc-symbols.csv 실제 행591: mc04_torque, %i6.5, bool, limit switch ss-10, 문서1097 | 이름 torque는 측정 토크값·센서 원리의 증거가 아님 |
| 공정 | PID_1684n002I.pdf 실제1, MC-04/M09에 SS-10 표시, PV-02 후단과 VS-01 사이 | 회전속도계/트립와이어 종류를 발명하지 않음 |
| P&ID 판본 | 도면1684n002, 기본06/04/2011, Rev.I 15/01/2013; 해당 개정문구 REMOVED MC-05, CHANGED POWER OF FN-02 | 2024/2025 전기도·시공 초안과 세대가 다르며 현재 실물 판정 자료가 아님 |
| 고정 원본 | source-mv06 HEAD abcf31c5030bc7ef8749ed8e869a857f2387a28a / v1.12.0 | 최신 앱/배포/CPU 검증을 뜻하지 않음 |

7영역을 모두 문서에 적용했다. I/O·제어·전기·알람은 확보 범위에 한해 적용, HMI 전용 이벤트와 현장 자료는 근거 미확보다. 제조사/실물 자료 없이 비해당으로 지우지 않는다. 요청된 모델의 실제 런타임 증명은 미확인이다. 원본 생성기·빌드·시험·PLC·현장·보호값·SEJIN 변경 및 시뮬레이터 작성/수정/생성/실행/행동시험은 전혀 수행하지 않았다.

이하 `S/`는 `all-in-one/sources/decoded-original/`이며 네 자리 번호는 실제 XML 파일명이다. NID·RID·UID는 해당 파일/선언 문맥에서만 결속한다.

## 2. I/O·HMI

| 신호 | 영역/주소/형식 | 원본 선언·용도 |
|---|---|---|
| MC04_torque | Global Input %I6.5 Bool | S/0558-IdentXmlPart.xml SimpleAccess RID40, Monitor NID=-2147483648 UID60 LN60; SSD AO53/SAD Input/SAM None |
| Inputs.MC04 torque | Global DB13.DBX6.5 Bool | S/0657 RID276 NID13 UID28/465, AO53 BIRID247; S/0655 DepDB RID247 TOD13 CID638561979615757134 |
| Allarm.MC_04_TORQUE | Global DB3.DBX3.5 Bool | S/0657 RID58 AO29 BIRID10; S/0655 RID10 TOD3. NID13 UID38 Set Write, UID467 Reset Write, UID466 Read |
| Flag.RESET_ALLARM | Global DB2.DBX6.0 Bool | S/0657 RID13 AO48 BIRID12; S/0655 RID12 TOD2; NID13 UID464 |
| OFF | Global Memory %M0.1 Bool | S/0658 RID46 AO1/SAD Memory; NID13 UID35. 이름만으로 현재 FALSE라 단정 금지 |

### Word 전달과 bit 접근

S/0397-FlgNet.xml NID1의 Move Part42는 Wire21 Powerrail→en, Wire52 ORef45→in, Wire54 out1→ORef46이며 DisableENO=true다. 원시 ORef45/RefId13은 S/0627 RID13 Tag_171, Word, Input AO48(%IW6), 목적지 ORef46/RefId14는 S/0629 RID14 Word AO48/BIRID4이다. S/0628 DepDB RID4는 Inputs DB13이며 위 DB 선언과 CID가 같다. 따라서 이 Word 복사의 해당 bit 위치가 I6.5→DB13.DBX6.5다. 해당 Move 데이터 경로에 반전/스케일은 없고, PIW/Peripherie 접근으로 바꾸지 않는다. Word 쓰기와 0429의 Bool 읽기를 따로 표시한다.

Main S/0030 NID19의 HMI Inputs 호출은 CRef28/CodeBlock29, S/0688 RID135 FC15 및 S/0694 RID136/TORID135다. Wire32·33은 선행 호출 ENO 연결, Wire42는 CRef25.eno→반전 Contact37.in, Wire43은 Contact37.out→CRef28.en이다. Wire44/ORef45→S/0692 RID140 `Simulation(1)` %M180.0이다. 즉 원시 입력 복사가 무조건 현재 실행된다고 단정할 수 없다. 이는 백업 호출 경계만 읽은 것이며 중지 기능을 조사·실행·재개하지 않는다.

전체 IdentXmlPart의 `MC04 torque`/`MC_04_TORQUE`/`MC04_torque` 표기 검색에서 S/0635 RID348 NID18 UID28 Write(AO53, Inputs, BIRID5) 선언도 발견했다. 해당 다른 문맥의 실행 동작·호출·최종 쓰기 우선순위는 미해석이며 원시 Word 복사가 유일 writer라고 주장하지 않는다. 새 시뮬레이션 조사로 확대하지 않는다.

### HMI 경계

sources/hmi_plc_tags.csv 실제 행31/138/426의 MC_04\Allarme1=DB11,X8.1, RispostaA=DB11,X8.0, Flag=DB2,X0.4는 부모 MC04 설정이다. 이 셋은 SS10 전용 표시·리셋 주소로 승격하지 않는다. 해당 CSV의 SS10/MC04 torque 전용 태그는 이번 문자열 검색에서 확보되지 않았다. 원본 HMI 화면·이벤트·경보 텍스트·DB3→DB11 집계 바인딩은 미확보이며 MC04 기존 초안의 미결속 상태를 유지한다.

## 3. 제어 구조와 소유

핵심 S/0429-FlgNet.xml(NID13; live_index i1792/LAD1792)의 전체 Parts/Wires를 독립 확인했다.

| 구간 | Part/Wire/ORef 결속 | 해석 |
|---|---|---|
| 공통 허가 | W488 Powerrail→Contact478.in; W34 ORef35(RID46)→478.operand; W479 478.out→480.in 및482.in | 두 분기 모두 OFF 조건 |
| Set 입력 | Contact480은 operand Negated; W27 ORef28(RID276)→480.operand; W36 480.out→SCoil454.in | OFF AND NOT Inputs.MC04 torque |
| Set 목적 | W37 ORef38(RID58)→SCoil454.operand | Allarm.MC_04_TORQUE Set |
| Reset 요청 | W472 ORef464(RID13)→Contact482.operand; W483 482.out→484.in | Flag.RESET_ALLARM |
| Reset 입력 | W473 ORef465(RID276)→Contact484.operand; W485 484.out→486.in | 입력 비반전 조건 |
| Reset 유지 확인 | W474 ORef466(RID58)→Contact486.operand; W487 486.out→RCoil460.in | 기존 자체 알람 참 조건 |
| Reset 목적 | W476 ORef467(RID58)→RCoil460.operand | 자체 알람 Reset |

S/0429에는 CRef, 타이머 Part, 시간 상수, 아날로그 환산이 없다. 입력 0을 무조건 현장 고장/비정상 접점이라고 선언할 수 없다. OFF=0이면 이 네트워크의 S/R 조건이 불성립하더라도 기존 알람이 자동으로 지워진다는 근거는 없다. 래치의 다른 writer·초기화·온라인 호출은 별도 확인 대상이다.

부모의 Q0.4, 속도 QW294, RUN I0.6, inverter I0.7 및 0428의 Tag_57/T54는 SS10 고유 입력/출력이 아니다. 부모 요청 해제 S/0247 ORef 목록은 RID62(MC_04_FAULT),205(MC04_INV),224(VS01),6(Maintenance)와 운전 요청/출력이고 SS10 torque를 이 분기에 직접 연결한 근거는 없다. 이는 0247의 직접 경로 범위이며 공통 전체정지/알람 집계를 배제하는 전수 증거는 아니다.

## 4. 전기 끝점·도면 판본

실제 원본 PDF를 렌더하여 다음 6페이지와 P&ID 표제란 확대를 시각 확인했다. FG와 실제 페이지를 별도로 기록한다.

| 원본·실제페이지 | 표제/개정 | 고유 끝점·독립 확인 |
|---|---|---|
| Electrical_Rev2.pdf p26, FG25 | METALLIC CONVEYOR MC-04, 기본27.05.2024, Rev2/17.03.2025 | +24Vdc 10.7(24/7)→X1:54의 5x20/2A F 표기 퓨즈→선25.3→SS-10 접점11/12→X1:55→E6.5,122/5. 전체 점선 영역 SPARE/LIMIT SWITCH TORQUE CONTROL |
| 같은 PDF p123, FG122 | DIGITAL INPUT MODULE, 기본27.05.2024, Rev2/17.03.2025 | E6.5 상단 역참조25/3→단자26→E6.5/CPU515/MOD9/LIMIT SWITCH SS-10. E6.5·E6.6 주변 SPARE 표시. CPU515는 도면 인쇄 표기이며 현재 CPU 확인 아님 |
| 같은 PDF p25, FG24 | METALLIC CONVEYOR MC-04, 기본27.05.2024, Rev2/17.03.2025 | M09/24AS1 및 +24/0V→25/0 전원 연결. RUN E0.6·ALARM E0.7와 SS10 E6.5를 구별. 부모 25KA1 실제 부하 접점5/9는 MC04 START 경로이며 SS10 접점11/12와 다름 |
| Electrical_Can_Decoating_20241118.pdf p34 | CANDC-CONS-E017-034, D-page17/total34/64, Rev1/24.11.11 first draft design | EXIT ZONE01, EXI1TB1→EXI1TB2→SS-10 그림. 표의 SS-10 LOC MC-05, 케이블9_7=EXI+MC04-SS10A, CVV1.0/2심/pipe16. 실제시공 확정 아님 |
| 같은 PDF p59 | CANDC-CONS-C009-059, D-page9/total59/64, Rev1/24.11.11 first draft design | row9_7 FROM MC-05/EXI1TB2 → TO MC-04/SS-10, DC/CVV/2C/1.0/spare0/routeE351/length3. row9_3은 EXIT/EXI1TB1→MC-05/EXI1TB2(SS10/11) 공통7G1.0 경로. 두 row를 동일 케이블로 합치지 않음 |
| PID_1684n002I.pdf p1 | 1684n002 RevI/15.01.2013 | MC-04/M09 부근 SS-10 공정 위치. 설치·현재 배선·센서 종류 증명과 분리 |

OEM의 X1:54/55와 시공 EXI1TB2 내부 번호의 일대일 준공 대응은 확보되지 않았다. 도면의 2A F는 문서 표기이며 현행 보호값/교체 지시가 아니다. 접점11/12 그림과 PLC NOT 접점을 근거로 실제 정상 때 ON/OFF, NC/NO 동작 상태를 확정하지 않는다. 릴레이 하단1/5/9 접점표와 실제 부모 부하5/9를 구별하며 SS10 회로에 부모 릴레이 접점을 끼워 넣지 않는다.

## 5. 알람·유지·복구

| 항목 | 확인 범위 | 미확정 |
|---|---|---|
| 발생 | OFF AND NOT DB13.DBX6.5 → DB3.DBX3.5 Set | 실제 사용/호출·OFF 값·입력 원인 |
| 지연 | 0429 자체 타이머 없음 | 외부 접점 지연/필터·다른 네트워크 지연·현재 설계는 미확인 |
| 유지 | SCoil/RCoil 구조, OFF 조건이 두 분기 공통 | 전원복귀·DB retain·다중 writer 최종값 |
| 해제 | OFF AND DB2.DBX6.0 AND DB13.DBX6.5 AND DB3.DBX3.5 → Reset | HMI 누름→RESET 요청 경로, 온라인 실행 |
| 영향 | 0429는 알람 비트 쓰기이며 직접 모터 Q 쓰기는 없음 | 공통 알람 집계·운전 전체 영향의 상세 소유는 별도 |
| 표시/ACK | MC04 부모 HMI 설정만 확인 | SS10 전용 경보 텍스트/ACK/시간기록 미확보 |
| 복구 | 입력 원인 회복, 알람 해제, 부모 재요청, 실제 정상 운전은 서로 다른 확인 | 현장 복구·안전 확인·재기동 수행0 |

`mc04 deleted` 제목을 근거로 알람이 완전히 제거되었다고 결론 내리지 않는다. 반대로 잔존 S/R만으로 현장 보호가 유효하다고 주장하지 않는다. 실제 작업은 승인된 절차와 자격을 갖춘 담당자가 판단해야 하며 이 문서는 접점 우회/강제/보호값 변경 지시가 아니다.

## 6. 증상 관찰표

| 증상 | 기록할 관찰 | 비교 근거·판정 경계 |
|---|---|---|
| SS10이 보이지 않음 | 현장 태그·설치 위치·명판·준공도 판본 | SPARE/과거 P&ID/시공초안은 현재 존재 여부를 대신하지 않음 |
| I6.5와 DB13 값이 다름 | 같은 시각 raw·DB·호출조건·프로젝트 판본 | 0397 Word42, 0030 ENO/NOT 조건, 다른 writer 미확정; 강제 시험하지 않음 |
| 입력과 알람이 반대로 보임 | OFF·입력·DB3 알람·RESET의 동시값과 시각 | 0429 Set는 NOT, Reset는 비반전. 이력·래치 상태를 함께 구별 |
| RESET해도 유지 | 요청 도달 여부·OFF·입력·알람·호출 각 값 | 네 조건을 모두 기록; reset 요청 자체가 원인 회복 증거 아님 |
| 모터가 안 돎 | 부모 요청/Q/RUN/INV와 SS10 알람을 별도 관찰 | MC04와 SS10 소유 혼동 방지; 5초 지연을 SS10에 적용 금지 |
| 배선표가 MC05로 보임 | FROM/TO·접속함·케이블 번호·원본 판본 | PDF34와59의 LOC/대상 차이 보존; 준공 증거 전 오배선 확정 금지 |

공통 기록 필드: 관찰자, 시각·시간대, 태그/위치, 자료 판본, 원시 I/DB/HMI 각 값과 단위, 최초 증상, 수집 방법, 비교 근거, 배제 결과, 승인 조치와 별도 복구 증거. 실제 운영 기록·사진은 이번 공개 원본/초안에 복제하지 않았다.

## 7. 완료·누락·인계

| 상태 | 결과 |
|---|---|
| documentation | draft_ready: SS10 한 ID의 7영역 문서 |
| static_review | 고유0429 전핀·선언, Word42·호출경계 및 도면6페이지 독립 확인. 원본 모든 논리 의미검토 아님 |
| ui_records / publication | not_run / not_published_by_dot; 코드·대장·배포 변경0 |
| tia_compile / live_cpu / field_recovery | 모두 not_performed |
| simulator | permanently_stopped; 작성·수정·생성·실행·행동시험0 |

필요 자료와 종료 기준:
1. SS10 실물 태그/명판/제조사 자료와 승인된 준공 결선: 설치·장치종류·정상 접점 방향이 일치할 때만 현장 식별 완료.
2. X1:54/55↔EXI1TB2↔SS10 실제 끝점·케이블 심선표: OEM/시공 차이를 판본과 함께 해결.
3. 현행 PLC 프로젝트/승인 변경내역/온라인 비교: OFF·호출·다른 writer·retain·알람 소비자의 현재 상태 확인. 현재 백업만으로 채우지 않음.
4. 원본 HMI 프로젝트/화면/이벤트·알람 텍스트: SS10 전용 또는 집계 바인딩, ACK와 Reset를 분리 확인.
5. 승인 관찰·원인 조치·재기동/복구 기록: 문서 완료와 현장 수리 완료를 분리.

네 기능 인계: 도면·래더 비교에는 0429↔FG25/122, 백업·선택복원에는 SS10 독립키와 부모/미지 필드 보존, 기록전후비교에는 raw/DB/OFF/알람/RESET 시각, 보고서에는 SPARE·deleted 제목·FROM/TO 판본 차이를 포함할 것을 제안한다. 구현·저장/재읽기/복원·PDF/UI 검증은 수행하지 않았다. 부모 MC04 완료나 다른 SS01/09/11 완료를 상속하지 않는다. 새 자료 없는 실물 보류를 반복 조사하지 않는다.

## 부록 A. 선정 원본 SHA-256·고정 Git blob 전체표

아래는 선정 파일의 바이트 검증이다. 해시 파일 수는 의미 검토 완료 네트워크 수가 아니다. `부모동일`은 MC04 초안 부록의 SHA와 일치함을 뜻하며 부모 문서의 모든 해석을 승인한다는 뜻이 아니다. 모든 행의 Git blob은 고정 commit 경로와 일치했다.

| 원본 상대경로 | SHA-256 | Git blob(SHA-1) | 고정일치 | 부모동일 |
|---|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | 예 | 해당없음 |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | 예 | 예 |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | 예 | 예 |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | 예 | 예 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | 예 | 예 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | 예 | 예 |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | 예 | 예 |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | 예 | 예 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | 예 | 예 |
| `all-in-one/registers/plc-symbols.csv` | `a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f` | `cbc576c5d6e47498a3865304a1c23de9b4641d9f` | 예 | 예 |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` | 예 | 해당없음 |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | 예 | 예 |
| `all-in-one/sources/decoded-original/0247-FlgNet.xml` | `104690938ac2ebe32d668f237255a3e957e0af9930bfc6587b9e6624bedf13a1` | `f7780f7eaaa297cd863fbebea4a56a567b231175` | 예 | 예 |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | 예 | 예 |
| `all-in-one/sources/decoded-original/0428-FlgNet.xml` | `cb7015f543d0deb26fe0bf23d045dc787b7c9cbc3d02c2c5623c0283709fa69a` | `ed486e94e686348871305d802a3575beef176b37` | 예 | 예 |
| `all-in-one/sources/decoded-original/0429-FlgNet.xml` | `092dd3ac8f08d5934b6ffdd27e3b649a06e23c3b95900f70aadb0e1d4f592572` | `822edc1c866917921170b21083f811f38d80da7d` | 예 | 예 |
| `all-in-one/sources/decoded-original/0558-IdentXmlPart.xml` | `45d49d53b6b41312960bb2a329663e87d8803e28d7832308424a6bf5091e6d1b` | `a0b681bd15e9ae15f2e1437576a4486cc732fdf2` | 예 | 예 |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` | 예 | 예 |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` | 예 | 예 |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | 예 | 예 |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | 예 | 예 |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | 예 | 예 |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | 예 | 해당없음 |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | `83b60b9de4541a3ffa6ee0db98205a372b525665` | 예 | 예 |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` | `9bfb9842e55901bab9a71d1ac03158467dfbb1bc` | 예 | 예 |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | `e625f3d8999c7be7d88c50eab0d93107117b58ec` | 예 | 예 |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` | `de9a12a6be87466ef1bf05df71c54580c556a827` | 예 | 예 |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | 예 | 예 |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | 예 | 예 |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` | 예 | 예 |

## 부록 B. 실제 작업 시각·검사 범위

- 배정 수신/조사 시작: 2026-10-11 12:49 UTC(대화 시각).
- 선언 추출·초기 검토 기록: 2026-10-11T12:49:59.555229+00:00
- 원본 해시/정적 검사·초안 저장: 2026-10-11T12:53:49.747581+00:00
- 검사 JSON: `extracts/SS10/checks.json`; 선정 지문 JSON: `extracts/SS10/source-hashes.json`; 독립 선언 추출 및 실제 PDF 렌더를 같은 SS10 폴더에 보존했다.
- 수행: 문서·JSON/CSV/XML 정적 읽기, XML 선언·핀 파싱, 원본 PDF 렌더·시각 확인, SHA/Gitblob 비교, 한국어 MD 작성. 원본 저장소 git status --porcelain은 빈 문자열이었다.
- 전체 원본/중지5자산 보존의 전역 검증은 부모의 별도 기록 범위다. 이 조사자는 선정 파일 검증과 원본 무수정 상태만 확인했으며 전역90/730파일 의미검토를 주장하지 않는다.
