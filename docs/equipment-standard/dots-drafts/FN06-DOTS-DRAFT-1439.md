# FN06(P18) 조사·문서 초안

- 문서 상태: 원본 대조를 포함한 초안. Codex 핵심 근거 재확인·제품 반영 전.
- 대상: catalog_id FN06, priority_key P18, 대장명 보조 블로어, 우선목록명 FN-06 팬 모터.
- 기준: GME-STD-1.0.0, 공개 저장소 main/all-in-one/.
- 조사 고정 커밋: 341f26f35c99ab8a7e4928f9b981d523a291a8fd (2026-10-11 내려받은 main). 해당 복사본 VERSION은 v1.6.0. FN03 v1.7.0 로컬 초안/검증은 사용자 진술이며 이 문서에서 재조사·수정하지 않았다.
- 조사자: 사용자의 dot, 자체 클라우드 환경에서 직접 조사. 현재 조사 모델/추론 설정은 관측되지 않아 미확인. 후속 검증·반영·배포 담당은 사용자가 지정한 기존 Codex 01a12963-de06-7e93-bd10-71f025de4730(GPT-6.1 Sol / High, 사용자 지정).
- 조사 시작: 2026-10-11 05:17 UTC / 14:17 KST. 초안 작성: 05:29 UTC / 14:29 KST. 자료 확인 시점과 현재 설비 상태를 혼동하지 않는다.
- 이번 산출물은 이 MD 하나다. 원본 저장소 코드·공통 파일·버전·완료대장·운영기록·배포는 변경하지 않았다. 시뮬레이터 작성/수정/생성/실행/행동시험, TIA 컴파일, PLC/현장/보호값 변경은 수행하지 않았다.
- 세진 설비관리 앱 자료·코드·사진·작업이력은 사용하거나 복제하지 않았다. 아래 시공 참고 PDF는 사용자가 지정한 GME 공개 저장소에 이미 포함된 원본이다.

## v1.7.0 후속 기준 확인

2026-10-11 05:30 UTC에 공개 main 10051ddf45f6fd740d057bda51bee3db5a57382e를 가져와 VERSION v1.7.0을 확인했다. 최초 조사 커밋과 비교했을 때 all-in-one/sources/decoded-original/ 전체, 세 원본 PDF, sources/hmi_plc_tags.csv, registers/equipment-hmi.csv, registers/plc-symbols.csv에는 바이트 차이가 없었다. 따라서 본 FN06 원본 근거는 새 main에도 그대로 적용된다. FN03 UI·배포 검증은 이번 dot이 재실행한 것이 아니며 사용자가 완료 사실을 전달했다. 원래 조사 기준과 당시 해시를 지우지 않고 이 확인을 덧붙인다.

## 입력 전달 후속 보강 — 2026-10-11 05:39 UTC / 14:39 KST

MC04의 입력 전달을 대조하는 중 FN06에도 적용되는 **HMI Inputs의 원본 Word 전송**을 확인했다. 최초 E08/G02의 “전송 원본 미확보” 범위를 좁힌다. 기존 원시 입력과 DB 변수를 합치는 것이 아니라, 둘 사이의 백업상 정적 쓰기 경로를 추가로 확인한 것이다. 현행 CPU·호출·최종값은 확인하지 않았다.

- S/0397-FlgNet.xml LAD1070/HMI Inputs, 원본 NID1: Move Part35의 in은 Wire39/ORef36, out1은 Wire40/ORef37이다. en은 앞선 Move27의 eno에서 Wire41로 들어온다. 해당 Move들의 원본 DisableENO="true"와 ENO 연결도 그대로 보존하며 TIA 실행 의미를 임의 단정하지 않는다.
- S/0627-IdentXmlPart.xml RID10/NID1 UID36: Tag_180, Word, SAD Input, SSD AO32. 따라서 백업 입력 Word %IW4를 가리킨다.
- S/0629-IdentXmlPart.xml RID11/NID1 UID37: Word, SSD AO32, BAD BIRID=4. S/0628-IdentXmlPart.xml DepDBBlock RID4는 Inputs, TOD N=13, BT=DB, CID 638561979615757134다. 이름 없는 GlobalAccess이지만 DB 종속 선언까지 연결하면 목적지는 Inputs DB13의 Word4다.
- S/0657-IdentXmlPart.xml RID291/NID24 UID867의 Inputs.FEEDBACKMOTOR FN-06은 BO35/AO35. BIRID247의 선언은 S/0655-IdentXmlPart.xml에서 동일 Inputs/DB13/CID로 확인된다. 이에 따라 Word4가 덮는 bit35, 즉 입력 I4.3에서 DB13의 4.3으로의 정적 전달을 확인한다. 이 연결에는 별도 비트 반전 게이트가 없다. 다른 쓰기나 현행 실행까지 없다고 주장하지 않는다.
- 호출 경계: S/0030-FlgNet.xml Main LAD1613/NID19에서 Recipes Handler CRef21 → ENO Wire32 → HMI CRef23 → ENO Wire33 → HMI Output CRef25 → ENO Wire42 → 반전 Contact37 → Wire43 → HMI Inputs CRef28.en이다. Contact37 operand는 Wire44/ORef45이며 S/0692-IdentXmlPart.xml RID140/NID19 UID45의 Simulation(1) 메모리 %M180.0다. S/0688-IdentXmlPart.xml RID135/NID19 UID29와 S/0694-IdentXmlPart.xml RID136/NID19 UID28/TORID135가 HMI Inputs 호출을 뒷받침한다.
- 따라서 이 백업의 HMI Inputs 호출은 앞선 ENO 연결과 NOT Simulation(1) 조건을 갖는다. 메모리의 현재 값·실제 호출 성공·입력 주기·후속 덮어쓰기는 미확인이다. 시뮬레이터는 여전히 영구 중지이며 관련 블록을 실행·수정·생성하지 않았다.

추가 근거 E24: 위 0397/0627/0628/0629/0655/0657/0030/0688/0692/0694의 경로. Codex는 기존 7영역 전체를 재조사하지 말고 이 Word 전달과 호출 경계만 추가 재확인하면 된다. HMI1198의 표시·알람 인스턴스 미해석과 현장 정상극성은 여전히 별도 미확정이다.

## 접근 및 적용 표준

저장소 .agents/skills/gme-equipment-rollout/SKILL.md, docs/equipment-standard/WORK-STANDARD.md, WORK-ITEM-TEMPLATE.md, INVENTORY.json, 루트 AGENTS와 최신 상태 문서를 읽었다. 표준의 7영역·원본 선언/핀 추적·원본/현행/해석 분리 기준을 적용했다. 표준의 자동 코드 반영·완료대장 갱신·2차133개 확대는 이번 사용자 역할 제한에 따라 실행하지 않았다.

자체 환경의 PDF 읽기·렌더 기능을 사용했다. 별도 tia-equipment-alarm-trace 스킬은 제공된 로컬 스킬 영역에서 찾지 못했으므로 그 스킬을 사용했다고 표시하지 않는다. 권한 확장 요청은 하지 않았다. Mac의 output/gme-netlify-release-20261009/docs/equipment-standard/DOTS-CODEX-HANDOFF-20261011.md는 읽지 못했다. 지정 Codex 창 조회는 연결 도구의 ID 형식 오류로 실패했으며 전달 완료를 주장하지 않는다.

### 읽는 법과 원본 링크

아래 S/는 all-in-one/sources/decoded-original/, R/는 all-in-one/registers/를 뜻한다. LAD 1802 같은 번호는 문서/검색 색인 ID이며, XML 선언의 NID와 다르다. ORef UId와 선언 CS/C UID는 RID와 해당 블록의 NID까지 함께 맞춘다. 다른 파일에 같은 숫자가 나와도 동일 선언으로 취급하지 않는다.

[고정 커밋 원본](https://github.com/esp6662266/gme-plc-manual/tree/341f26f35c99ab8a7e4928f9b981d523a291a8fd/all-in-one)에서 아래 상대 경로를 찾으면 된다. 원본 XML은 한 줄인 파일도 있으므로 임의 줄번호 대신 Part/Wire/ORef/RID/NID를 식별자로 썼다. 마지막에 확인한 원본 SHA-256 목록을 제공한다.

## 요약: 후속 Codex가 우선 재확인할 점

1. FN06은 이 자료에서 **M26 단일 모터의 접촉기 직접 기동 회로**다. FG52/PDF53에 52QM1·52KM1·52QS1이 보이며, 별도 인버터 고장 입력이나 FN03의 소프트스타터/두 35초 타이머를 FN06에 복제하면 안 된다.
2. FN06 자체 감시 타이머는 Tag_67, 선언 주소 %T91, SdCoil Part817의 S5T#2S다. 별칭 알람은 Allarm.MBVA01_FAULT다. 이름만 보고 다른 본체 알람으로 제외하지 말고 LAD1802·1955의 실제 연결로 설명한다.
3. 원시 입력 FN06_Fbk %I4.3과 DB의 Inputs.FEEDBACKMOTOR FN-06은 별개다. 같은 35비트 오프셋/비슷한 이름만으로 연결을 확정하지 않는다. 물리 입력→DB 전달의 현재 실행 근거는 미확보다.
4. 요청 해제는 ON AND (MBVA01_FAULT OR (NOT Inputs.RD01 run AND NOT UNDER TESTING)). UNDER TESTING 반전은 RD01 분기에만 있다. 이를 전체 고장 허가 우회로 해석하면 틀린다.
5. 출력은 같은 네트워크에서 ON AND Flag.M_FN_06 → Start FN06(%Q3.3)이다. 알람 Reset과 운전 요청 재설정은 별도다.
6. HMI 설정 3행은 확보했으나 LAD1198의 FN06 호출의 실제 피연산자 4개는 미해석이다. CRef/CodeBlock 선언 후보는 있으나 해당 호출 NID까지 확정한 연결은 보류한다. DB11,X42.1이 곧 PLC의 MBVA01_FAULT라는 직접 연결은 확정하지 않는다.
7. 운전시간 LAD1032의 FN_06_HOUR는 원본상 **Move 입력 상수1**이다. 일반적인 “시간값에 1 더하기”로 고쳐 설명하지 않는다. 분 값의 Add와 시간값 Move, ENO 연결, 별도 초기화 LAD1051을 각각 보존한다.

## 7영역 적용표

| 영역 | 적용 상태 | 이번 작성 범위 | 미확정 경계 |
| --- | --- | --- | --- |
| 1. 설비·자료 기준 | 적용 | P18/FN06/M26, 원본 시점·공정 관계·경계 | 실제 동일성/현행 모델·설치 상태 |
| 2. I/O·HMI | 적용 + 일부 근거 미확보 | I4.3/Q3.3/T91, Flag/Inputs/알람 분리, HMI 3행·CRef 핀 | 원시 입력→DB의 현행 실행, HMI 실제 인스턴스·이벤트·현재 연결 |
| 3. 제어 구조 | 적용 | 요청 Set/Reset, 최종 출력, 타이머, 버너 준비의 소비 경로, 운전시간 | 현재 호출/스캔 순서·온라인 값·전원복귀 |
| 4. 전기 전달 경로 | 적용 | FG52·120·139 실제 PDF 렌더, 시공참고21·51페이지 | 준공도·현재 단자·보호 설정·실배선 |
| 5. 알람·복구 | 적용 | MBVA01 별칭, 2초 SD, Set/Reset/요청 해제 | HMI 문구 직접 대응, 현장 정상극성·재기동·복구 |
| 6. 증상별 수리 | 적용(관찰·비교 초안) | 증상별 구분과 필요한 자료·복구 증거 | 실제 진단/조치/복구는 미수행 |
| 7. 완료 기준 | 적용 | 근거 재확인 목록·누락·역할별 상태·다음 대상 | 정적 구현검사/UI/게시/CPU/현장 검증 |

# 1. 설비·자료 기준

### 1.1 관리 식별과 물리 관계

INVENTORY.json priority[P18]는 FN06에 태그 대응하지만 identity_verified:false이고 “팬 본체와 모터의 관리 관계 확인”을 남긴다. catalog FN06은 motor, 연소·열회수, parent_id:null이다. 이 상태를 임의로 완료 처리하지 않는다. R/equipment.json의 기능 설명과 P&ID를 탐색 기준으로 삼고 실제 태그·명판·승인도면으로 최종 확인해야 한다.

원본 sources/PID_1684n002I.pdf PDF1의 FN-06/M26 표시는 3kW·440V이며, BR01/FN03 주변의 보조 송풍 경로에 배치되어 있다. 전기 Electrical_Rev2.pdf FG52/PDF53의 M26/FN-06 표기와 맞는다. P&ID의 공정 연결은 PLC 소유나 현장 실물 동일성의 단독 증거가 아니다. 인접한 FN03(M25), RD01, BR01, AB01을 FN06의 모터·알람·타이머로 합치지 않는다.

### 1.2 자료 시점과 충돌

- Electrical_Rev2.pdf FG52 제목 BLOWER FAN FN-06, 도면 일자 27.05.2024. FG120에는 REV2/17.03.2025도 보인다. 페이지별 표제란 상태를 구분한다.
- PLC Ident의 수정시각은 선언마다 다르다. 예: 0602 Start FN06은 2024-07-08, 0658 같은 심볼은 2025-02-13. 이 시각은 현재 CPU 다운로드 일자가 아니다.
- PLC 심볼 색인의 설명은 a 60.3 fn-06 motorcommand, 주소는 %q3.3이다. 원본 SimpleAccess AO27(Output)과 도면 A3.3은 서로 맞지만 설명의 A60.3은 별도 불일치로 남긴다. 현행 배선을 이름으로 바꾸지 않는다.
- 시공 참고 Electrical_Can_Decoating_20241118.pdf 제목란에 first draft design(24.11.11)이 보인다. 승인 준공도라고 취급하지 않는다.

# 2. I/O·HMI

## 2.1 주소·소유·유형

| 신호 | 영역/주소 또는 선언 | 방향·의미 | 원본 근거 | 해석 경계 |
| --- | --- | --- | --- | --- |
| FN06_Fbk | Bool Input, %I4.3 (AO35) | 원시 접촉기 응답. LAD1032 운전시간에서 읽음 | S/0613-IdentXmlPart.xml RID206, NID34/UID1882, SAD Input; S/0320-FlgNet.xml Part1912/Wire1894 | 회전/풍량/기계 정상의 증거 아님 |
| Start FN06 | Bool Output, %Q3.3 (AO27) | 최종 물리 기동 출력 | S/0602-IdentXmlPart.xml RID133,NID26/UID783,Write; 0257 Part776/W794 | 실제 단자 출력전압/접촉기 투입은 미관측 |
| Tag_67 | Timer, %T91 (AO91) | FN06 지연 감시 타이머 | S/0658-IdentXmlPart.xml RID99,NID24 UID832(Write)/833(Read), SAD Timer | HMI 태그가 아님. 현재 누적값 미취득 |
| Flag.M_FN_06 | Global DB member, Bool, BO/AO31 | 기동 요청 기억값. HMI 설정 DB2,X3.7과 비트 위치 대응 후보 | 0577 RID66; 0604 RID132,NID26 UID781/782 | DB 블록 번호/현행 주소를 별도 대조. HMI 쓰기 이벤트까지 입증한 것은 아님 |
| Inputs.FEEDBACKMOTOR FN-06 | Global DB member, Bool, BO/AO35 | 알람과 버너 준비에서 쓰는 처리 응답 | 0657 RID291,NID24 UID867; 0585 RID221,NID4 UID37 | %I4.3과 동일 변수로 합치지 않음. 정적 Word 전송 경로는 아래 후속 보강에서 확인. 현행 실행은 미확인 |
| Allarm.MBVA01_FAULT | Global DB member, Bool, BO/AO31 | FN06 기동응답 감시 알람의 내부 별칭 | 0657 RID101,NID24 UID835/837/838; 0604 RID131,NID26 UID778 | 이름 MBVA01을 실제 별도 자산/모터로 확정하지 않음 |
| Flag.RESET_ALLARM | Global DB member, Bool, AO48 | 공통 알람 해제 요청 | 0657 RID13,NID24 UID836 | 공통 기능이며 FN06 전용 입력 아님 |
| Inputs.RD01 run / UNDER TESTING | Global DB 응답 / Memory Bool | 요청 해제의 RD01 분기 조건 | 0604 RID223,NID26 UID23; 0602 RID4,NID26 UID780 | 정상극성·시험운전 허용 여부/현행 값 미확인. 설정 변경 지시 아님 |

## 2.2 HMI 설정과 원본 호출의 경계

R/equipment-hmi.csv 및 공개된 sources/hmi_plc_tags.csv에서 FN06 설정은 다음 3행이다. 이 CSV는 dde.cfg에서 추출한 설정 자료다. 이번 공개 소스에서 원래 dde.cfg와 실제 버튼 이벤트 스크립트까지는 확보하지 못했다.

| HMI 태그 | 설정 주소 | Access / 내부 ID | 판정 |
| --- | --- | --- | --- |
| FN_06\Allarme1 | DB11,X42.1 | PLC / 00344 | 알람 표시에 쓰는 설정 후보. MBVA01과 직접 동일성 미확정 |
| FN_06\RispostaA | DB11,X42.0 | PLC / 001C2 | 응답 표시 설정. 원시 I4.3과 직접 연결이라고 단정하지 않음 |
| FN_06\Flag | DB2,X3.7 | PLC / 0019A | 요청 위치 설정. 버튼의 Set/Reset/토글/쓰기 이벤트는 미확인 |

S/0375-FlgNet.xml(LAD1198, hmi/fn06)은 CRef22/RID638 및 CodeBlock23/RID1을 호출한다. 실제 연결은 다음과 같다.

| 호출 핀 | Wire | ORef UID / RID | 원본 확인과 남은 것 |
| --- | --- | --- | --- |
| en | 21 | Powerrail | 정적 호출 연결 확인; 현재 CPU 실행은 별도 |
| Ingresso_run | 37 | 24 / 671 | 상대 신호 선언 미해석 |
| Allarme1 | 39 | 26 / 284 | 상대 신호 선언 미해석; MBVA01이라고 채우지 않음 |
| Allarme2/3/4/5 | 40/41/42/43 | 27/28/29/30 / 48 | 기존 해석 FALSE (0626 LiteralConstant RID48 후보). 해당 호출 NID의 확정은 별도; 고장 4개를 새로 만들지 않음 |
| Risposta | 46 | 33 / 287 | 출력 대상 선언 미해석 |
| Comulativo_allarmi | 48 | 35 / 289 | 출력 대상 선언 미해석 |

참고 함수 S/0355-FlgNet.xml(LAD331)의 local Ingresso_run→Risposta 경로와 5입력 OR→Comulativo_allarmi는 보존할 수 있다. 0621-IdentXmlPart.xml Local InterfaceAccess RID16/17/18/22, NID1 UID24/28/34/60에서 입력·출력 선언을 직접 확인했다. 0623의 FCBlock RID1/UID23은 HMI Standard Motors 후보이고 0624의 BlockInterfaceInfo RID638/UID22도 여러 NID에서 재사용되므로, 이 숫자만으로 FN06 호출의 실제 바인딩을 확정하지 않았다. 다만 일반 함수의 동작과 FN06 인스턴스 바인딩은 다른 확인 단계다. FN06 호출의 네 대상 선언과 정확한 바인딩이 미확정인 상태에서 DB11로의 실제 전달을 완료로 쓰면 안 된다.

## 2.3 원시 입력과 처리 응답

확보된 사용처 색인과 원본 대조에서 %I4.3는 운전시간 LAD1032에, DB 처리응답은 LAD1802·1857에 나타난다. 처리응답에 대한 legacy simulation 블록의 쓰기 존재는 현재 물리 입력 전달의 근거로 쓰지 않는다. 해당 블록을 실행·수정·시험하지 않았다. 초기 조사에서는 전송 원본을 미확보로 남겼다. 아래 2026-10-11 05:39 UTC 보강에서 Word 전송 원본을 확인했으며, 현행 호출/다운로드 대조는 여전히 필요하다.

# 3. 제어 구조와 소유

## 3.1 요청 → 출력 → 전기 전달 → 응답

요청은 Flag.M_FN_06, 출력은 Start FN06, 접촉기 전기응답은 FN06_Fbk, 알람에서 읽는 응답은 Inputs.FEEDBACKMOTOR FN-06이다. 네 대상을 분리해 표시한다. 최종 출력 소유는 Motors1의 FN06 네트워크에서 확인되며, 버너 네트워크는 FN06 응답을 소비할 뿐 FN06 출력 소유가 아니다.

S/0257-FlgNet.xml LAD1955:

- Part796(ON)의 out은 Wire797로 고장 경로·RD01 경로·요청 출력 경로에 나뉜다.
- 고장 경로: Part798 MBVA01_FAULT → Wire799 → OR Part767.in1.
- RD01 경로: Part22 NOT Inputs.RD01 run → Wire24 → Part802 NOT UNDER TESTING → Wire803 → Part767.in2.
- OR767.out → Wire789 → RCoil772.in; Wire791/ORef781/RID132는 Flag.M_FN_06.
- 별도 출력 경로: Part804 Flag.M_FN_06 → Wire805 → Coil776; Wire794/ORef783/RID133는 %Q3.3.

정적 조건:

RESET_REQUEST = ON AND (MBVA01_FAULT OR (NOT RD01_RUN AND NOT UNDER_TESTING))

START_OUTPUT = ON AND Flag.M_FN_06

네트워크에서 Reset 코일과 출력 코일이 구분되어 있다는 사실까지 확인했다. 현재 PLC 스캔/다중 쓰기 우선순위·유지값·전원복귀 상태는 실제 프로젝트/TIA·CPU 대조 전이다. ON이 항상 true인지, 시험비트가 어떤 운영 절차로 바뀌는지는 확인하지 않았다.

## 3.2 자동 요청 Set 및 전체정지 Reset

| 경로 | 정적 조건과 동작 | 원본 핀·선언 | 해석 경계 |
| --- | --- | --- | --- |
| 예열 | ON ∧ ¬Emergency_module_fault ∧ Tipo_preset=1 ∧ Auto_ON1 ∧ Tempo_presetting=40 → Set M_FN_06 | 0164 LAD1843: Contact785/22, Eq400, Contact823, Eq548, SCoil554; W761/762(in1/in2),W763(in),W765 operand; ORef655/RID66; 0577 NID3 UID655; 상수40=0578 RID65,NID3 UID653 | 40은 비교 상수. 원본 시간 변수 단위/현재 진행 주기를 확인하지 않고 “40초”로 확정하지 않음 |
| 생산 | ON ∧ ¬Emergency_module_fault ∧ Auto_ON1 ∧ Tipo_preset=2 ∧ Tempo_presetting=60 → Set M_FN_06 | 0165 LAD1844: Contact1145/1154/1147,Eq737,Eq892,SCoil898; W1121/1122/1123/1125; ORef1004/RID66; 0577 NID4; 상수60=0578 RID92,UID1002 | FN02/FN03 조건을 가져오지 않음. 60의 단위/현행 값은 별도 |
| 전체정지 | Auto_ON1 ∧ Tipo_preset=5 ∧ (Tempo_presetting=1 ∨ Emergency_module_fault) → Reset M_FN_06 | 0166 LAD1847: Contact1095,Eq881/887,Contact1134,OR54,RCoil897; W55/56→OR, W1034→Reset, W1038/ORef991/RID66; 0577 NID5 UID991 | OR 두 분기를 보존. 전원차단 또는 안전회로 전체를 뜻하지 않음 |

이 요청에 대한 직접 Set/Reset 4개 네트워크(1843/1844/1847/1955)를 구분한다. HMI 외부 쓰기·현재 호출 조건은 별도이므로 이것만으로 전체 런타임 쓰기 수를 완전 확정하지 않는다.

## 3.3 버너 준비에서의 응답 소비

S/0174-FlgNet.xml LAD1857의 Coil182는 Flag.Burner_ready이다. FN06의 물리 Start 출력을 쓰는 코일이 아니다.

정적 경로는 ON ∧ ¬MAX_MAX_TC09 ∧ ¬BURNER_START_FAULT ∧ ¬BURNER_LDU_FAULT ∧ Inputs.FN01 Run ∧ Inputs.FN04 Run ∧ Inputs.RD01 run ∧ (Inputs.FEEDBACKMOTOR FN-06 ∨ Inputs.Burner On) ∧ Inputs.FN02 Run이다.

FN06 접점 Part36/ORef37(RID221, 0585 NID4)과 Burner On 접점 Part228/ORef229(RID227)이 OR Part38의 서로 다른 입력이다. Wire53/45가 각각 in1/in2, Wire46은 FN02 접점40으로, Wire55는 Coil182로 이어진다. “FN06 응답이 반드시 단독으로 항상 필요하다”라고 OR 가지를 지우지 않는다. 동시에 이 정적 OR가 운전 우회 절차를 허용한다는 뜻도 아니다. 외부 연소제어기 화염·퍼지·점화 안전 로직은 이 원본만으로 알 수 없다.

## 3.4 호출 조건과 현재 실행의 경계

S/0549-FlgNet.xml LAD1620에서는 ON Contact350/Wire351이 Motors1 CRef319/CodeBlock337과 Burner Control CRef328/CodeBlock343, time work motor CRef334/CodeBlock347의 en에 연결된다. S/0688-IdentXmlPart.xml의 RID67/76/82는 NID7의 해당 호출 선언이다. S/0031-FlgNet.xml LAD1619는 ON Contact282/W283를 통해 Allarms1 CRef264/CodeBlock275를 호출하며 0688 RID58/NID6에서 이름을 확인했다.

이는 저장된 원본의 호출 연결 확인이다. 현재 CPU 일치·실제 주기·다른 호출·온라인 값은 검증하지 않았다. 자동시퀀스 호출 전체와 HMI/Inputs의 미해석 ENO 경로를 생략하고 “모든 조건이 매 스캔 그대로 적용됨”이라고 쓰지 않는다.

## 3.5 운전시간은 별도 기능

S/0320-FlgNet.xml LAD1032, NID34:

- Tag47 Contact1910와 원시 FN06_Fbk Contact1912의 직렬 출력 W1913이 Add1864.en 및 Ge1871.pre에 연결된다.
- Add1864는 FN_06_MIN + 상수1 → FN_06_MIN (W1895/1896/1897).
- Ge1871의 입력은 FN_06_MIN와 상수60(W1898/1899).
- Ge.out/W1900 → Move1874.en. **Move 입력은 상수1(ORef1888,RID7,W1902)**이며 out1/W1903은 FN_06_HOUR(ORef1889,RID210)다. Add로 바꾸어 해석하지 않는다.
- 1874.eno/W1904 → Move1877.en; 상수0/W1905 → FN_06_MIN/W1906. 1877.eno/W1907 → SCoil1880 Flag_Aggiorna_DB.
- S/0338-FlgNet.xml LAD1051에는 Tag48 경로의 선행 Move2952.eno/W2981 → Move2955.en, 상수0/W2982 → FN_06_HOUR/W2983가 별도로 있다.

0615-IdentXmlPart.xml RID208(FN_06_MIN),RID210(FN_06_HOUR), NID34/53의 UID를 맞췄다. Tag47 주기/상승엣지, 누적시간 의도, ENO 의미·실행 순서, 현재 값과 초기화 조작은 확인 전이다. 이 문서에서 수정하거나 동작시험하지 않는다.

# 4. 전기 전달 경로

다음은 원본 PDF를 실제 렌더하여 시각 대조한 결과다. 전기 도면 FG 번호와 PDF 페이지를 분리했다.

| 경로 | 양 끝점과 중간 요소 | 원본 위치 | 관찰·제한 |
| --- | --- | --- | --- |
| 주전원→모터 | 3상440V60Hz, 8.3L1/L2/L3 → 52QM1 1/3/5→2/4/6 → 52KM1 주접점 → XM의52U1/52V1/52W1 → 52QS1 → M26 U/V/W, PE | Electrical_Rev2.pdf FG52/PDF53, 좌측 B~E | M26 FN-06, 도면3kW/5.8A. QM1 표기5.5~8A는 도면 범위이며 현행 설정값이 아님 |
| 출력→접촉기 코일 | FG139의 A3.3/채널단자34 → FG52 A3.3 → XS41 → 52QS1 보조접점 → XS42 → 52QM1 보조접점 → 52KM1 A1→A2 → -0Vdc10.6 | FG139/PDF140 ↔ FG52/PDF53 C~E | QS/QM 보조접점의 도면상 직렬 관계. 현장 정상극성·내부 결선/미기재 접점단자 번호는 추정하지 않음 |
| 접촉기→입력 | +24Vdc10.7 → 52KM1 보조접점13→14 → E4.3 → FG120의 입력채널 단자4 | FG52/PDF53 C~D ↔ FG120/PDF121 D~E | FG120 표제에 CPU515/MOD9, E4.3 FEEDBACK MOTOR FN-06. 현재 CPU/모듈 검증 아님 |
| 출력 모듈 급전 참조 | FG139 A3.3은 CPU515/MOD14 도면 칸, 단자34. +24Vdc10.9가 X21(3031), 5×20/4A F를 거쳐 단자39로, 단자40은 -0Vdc10.6 | FG139/PDF140 | 도면값만 기록. 현행 퓨즈·전압·안전정격 변경 지시 없음 |
| 시공 참고 케이블 | CR → FN-06/M26; =ENT+FN06-M26A, 행1_4, GAC/CV/4심/1.5, SPARE0, 경로1=100/RB, 경로2=E100, Adjustment13, LEN43 | Electrical_Can_Decoating_20241118.pdf PDF51, CANDC-CONS-C001-051, 표1_4 | 단위·길이는 표 제목/원문을 유지. 현재 포설값 또는 보호협조 적합으로 확정하지 않음 |
| 배관 경로 참고 | 100RBD1 → EMBEDDED CP No1/Pipe22 → M26; 동일 케이블 식별자와 CV1.5/4심 | 같은 PDF21, CANDC-CONS-E004-021, FN-06/M26행 | 표51의100/RB와 표21의100RBD1은 원문을 각각 보존. 임의 일괄 치환하지 않음 |

다른 팬의 인버터/소프트스타터, 아날로그 속도지령, 브레이크·냉각팬 분기·전류값을 FN06에 추가하지 않았다. 이 확인 범위에서 FN06 전용 속도제어/PID의 실행 근거는 확보되지 않았다. 없는 원본과 비해당을 구분해 “직접기동 원본 확인, 가변속 제어 근거 미확보”로 남긴다.

# 5. 별칭 알람·타이머·복구

## 5.1 LAD1802 원본 경로

S/0437-FlgNet.xml은 block allarms1 / 제목 fn06 / 색인22 / 원본 NID24다.

| 단계 | 원본 경로 | 해석 |
| --- | --- | --- |
| 감시 허가 | ON Part853/ORef829/W839 → W854 → StartFN06 Part855/ORef830/W840 | ON과 실제 출력 심볼이 직렬 조건 |
| 응답 부재 | Part866 Negated PinName=operand, ORef867/RID291/W869; W21→SdCoil817.in | 처리 응답이 false인 경우를 검사. 물리극성 판정 아님 |
| 시간값 | W841/ORef831/RID28→817.value | 0656 LiteralConstant,NID24/UID831, S5Time S5T_x0023_2S, 원시V512. 512ms가 아니라 S5Time 인코딩의2초 |
| 타이머 기록 | W842/ORef832/RID99→817.operand | 0658 Timer Tag67/AO91=%T91 |
| 알람 Set | Part857 Tag67 접점 ORef833/W843 → W22→SCoil823.in; W846/ORef835/RID101 | ON ∧ StartFN06 ∧ Tag67 → MBVA01_FAULT Set |
| 알람 Reset | ON의 W854 분기 → RESET_ALLARM Part861/ORef836/W848 → MBVA01_FAULT Part863/ORef837/W849 → W864→RCoil828; W851/ORef838/RID101 | ON ∧ RESET_ALLARM ∧ MBVA01_FAULT → Reset |

타이머 입력 조건은 ON ∧ StartFN06 ∧ ¬Inputs.FEEDBACKMOTOR FN-06, Gate는 SdCoil이다. 표준 Siemens S5 SD의 지연 기능이라는 해석과 원본 설정2초를 분리하여, 현재 CPU에서 실제2초로 동작 측정했다는 표현은 하지 않는다. 타이머 재시작·전원복귀·스캔 경계·다중 쓰기 확인은 미수행이다.

## 5.2 알람 해제와 설비 복구의 구분

- Reset 가지에 “응답이 정상으로 돌아옴” 접점은 없다. 원인이 그대로인 상태에서 Reset 조건만 성립할 수 있음을 문서에 유지한다.
- Set/Reset 코일은 별개이며 같은 네트워크에 있다. 현재 CPU의 동시 성립·스캔 동작을 측정한 것이 아니다.
- MBVA01_FAULT는 LAD1955에서 요청 M_FN_06을 해제한다. 알람 Reset만으로 요청 재설정 또는 자동재기동을 보장하지 않는다.
- 출력 false, 접촉기 미투입, 기계 미회전, 송풍 부족, HMI 알람 해제는 각각 다른 상태다. 하나를 다른 상태의 확인으로 기록하지 않는다.
- 복구 완료는 원인 조치와 승인된 재기동 절차에 따른 출력/접촉기/실물·공정 응답, 재발 여부를 별도 기록해야 한다. 이번 작업은 그 절차를 수행하지 않았다.

# 6. 증상별 수리·관찰 초안

현장 조작 명령이 아니라 자료 수집·판정 문서다. 전기·기계 점검은 사업장의 작업허가/격리 절차와 자격 범위에서 수행해야 하며, 보호·인터록을 우회해 시험하는 단계를 포함하지 않는다.

| 증상 | 먼저 분리할 관찰값/자료 | 원본 비교 지점 | 배제·확인할 것 | 복구 증거 |
| --- | --- | --- | --- | --- |
| 기동 요청이 유지되지 않음 | M_FN_06, MBVA01_FAULT, RD01 처리응답, UNDER TESTING, ON의 동일 시각 기록 | LAD1955 RCoil772,자동Set/Reset1843/1844/1847 | 알람 해제와 요청 재설정 혼동; 다른 쓰기/모드 | 승인 재요청 후 요청/출력 유지와 원인 조치 기록 |
| 요청은 있는데 접촉기가 안 들어옴 | Q3.3 표시와 실제 출력/XS41·42/코일 상태를 구분한 자격자 점검 기록 | FG139↔FG52, 52QS1/QM1 직렬 경로 | PLC 논리 문제인지 출력 이후 전기 전달 문제인지 | 보호원인 확인, 전달 경로 복구와 접촉기/실물 확인 |
| 기동 후 MBVA01 알람 | StartFN06, DB 처리응답, Tag67, 원시I4.3을 같은 시각으로 수집 | LAD1802,FG52 접점13/14,FG120 | 원시입력 정상인데 DB전달이 다른 경우와 실제 접점 미응답 분리 | 단순 Reset이 아닌 원인·응답·재발 여부 자료 |
| 원시 응답은 있으나 HMI 응답이 다름 | I4.3/DB응답/DB11 설정·통신·화면 이벤트 원본 | 1032/1198, HMI 설정3행 | HMI주소설정·인스턴스 매핑·오래된화면; 회전 정상 단정 금지 | 실제 태그/주소/이벤트 대조 및 표시 정상 증거 |
| 버너 준비가 안 됨 | FN06응답만 보지 말고1857 직렬 조건과 BurnerOn OR 분기 | 0174 Part36/228→OR38→Part40→Coil182 | FN01/FN04/RD01/FN02·온도/버너고장을 FN06단독 고장으로 오판하지 않음 | 해당 제어 소유자의 원인/허가·응답 확인, 외부 안전제어 검증 별도 |
| 응답은 ON이나 송풍이 부족함 | 명판·모터/팬 회전·기계 상태·공정 관측(값/단위/측정위치/시각) | M26/52KM1 보조접점 근거와 P&ID | 보조접점은 풍량센서 아님. 현행 회전방향/성능 기준은 승인자료 필요 | 승인 성능조건에 대한 측정·조치·복구 기록 |
| 운전시간이 기대와 다름 | Tag47/48, FN_06_MIN/HOUR 및 다른쓰기·원본 버전 | 0320 Add1864/Move1874,0338 Move2955 | HOUR를 +1로 오해하지 않음; ENO/초기화/주기 검토 | 원본의도·현행프로그램 대조 후 별도 승인된 검증 결과 |

기록 필드: 관찰자·시간대·설비/신호/주소·프로그램 근거·관찰값/단위·수집방법·원본 비교·배제 사유·조치·복구 증거·남은 미확정. 빈 값과0을 구분하고 기존 note/repair_observation·미지필드·초안·다른 설비 기록을 덮어쓰지 않는다.

# 7. 완료 기준·근거표·인계

## 7.1 핵심 근거표

| 근거ID | 주장 | 원본 경로·위치·선언/핀 | 이번 확인 | 미확정/추가 자료 |
| --- | --- | --- | --- | --- |
| E01 | P18↔FN06 관리 대응 | docs/equipment-standard/INVENTORY.json,priority P18/catalog FN06 | tag 대응,identity_verified:false 보존 | 명판·배치·실물 대응 |
| E02 | M26 FN06과 회로 유형 | sources/Electrical_Rev2.pdf FG52/PDF53 | 렌더로 M26/3kW/5.8A·QM/KM/QS 대조 | 현행 명판·보호설정·준공 변경 |
| E03 | 공정 배치 | sources/PID_1684n002I.pdf PDF1,FN06/M26 | 실제 렌더 확인 | 공정 연결≠PLC소유/실물확정 |
| E04 | 물리입력%I4.3 | S/0613-IdentXmlPart.xml RID206/NID34 UID1882,SSD AO35,SAD Input | 선언/0320 W1894 대조 | 현재 입력·정상극성 |
| E05 | 물리출력%Q3.3 | S/0602-IdentXmlPart.xml RID133/NID26 UID783,AO27/SAD Output;0257 W794 | 선언/Coil776 대조 | 설명A60.3불일치·실배선 |
| E06 | 별칭알람 소유 | S/0657-IdentXmlPart.xml RID101/NID24 UID835/837/838;0437 W846/849/851 | MBVA01_FAULT를FN06지연감시와연결 | HMI문구/자산명칭현재대응 |
| E07 | 2초 SD 자체 근거 | S/0437-FlgNet.xml Part817,W841/842;0656 RID28 UID831,NID24;0658 RID99 UID832/833 | S5T#2S·Timer T91 확인 | 온라인시간/스캔/재시작 |
| E08 | 내부응답과원시입력분리 | S/0657-IdentXmlPart.xml RID291,NID24 UID867,AO35;0613 SAD Input AO35 | 서로다른GlobalDB/Input영역 | 후속 E24로 정적 전송 확인; 현행 호출·다중 쓰기 미확인 |
| E09 | 요청해제OR범위 | S/0257-FlgNet.xml Part22/802,OR767,RCoil772;0604 RID131/132/223,0602 RID4 | 양분기·반전·Wire 대조 | 현행CPU·다중쓰기 |
| E10 | 최종출력 | S/0257-FlgNet.xml 796→804→776,W797/805/794 | ON∧요청→출력 확인 | 실제출력전압/회전 |
| E11 | 예열Set | S/0164-FlgNet.xml 785/22/400/823/548/554,W761~765;0577/0578 NID3 | preset1/비상반전/Auto/40조건 대조 | 시간단위·현재시퀀스 |
| E12 | 생산Set | S/0165-FlgNet.xml 1145/1154/1147/737/892/898,W1121~1125;0577/0578 NID4 | preset2/비상반전/Auto/60조건 대조 | 시간단위·현재시퀀스 |
| E13 | 전체정지Reset | S/0166-FlgNet.xml 1095/881/887/1134/OR54/897,W55/56/1034/1038;0577/0578 NID5 | preset5와(1∨비상)분기 대조 | 현재정지정책/현장안전 |
| E14 | 버너준비응답소비 | S/0174-FlgNet.xml Part36/228/38/40/182,W35/53/45/46/55;0585 NID4 RID221/227/222/34 | FN06응답∨BurnerOn,그후FN02 확인 | 외부버너내부시퀀스 |
| E15 | HMI 설정3행 | sources/hmi_plc_tags.csv, R/equipment-hmi.csv,FN_06 | 설정주소/내부ID 대조 | dde.cfg원본·화면이벤트 |
| E16 | HMI미해석바인딩 | S/0375-FlgNet.xml CRef22/RID638,CodeBlock23/RID1,W37/39/46/48 | 네대상ORef671/284/287/289미확정으로보존 | 해당인스턴스선언/DB레이아웃 |
| E17 | 알람Reset조건 | S/0437-FlgNet.xml Part853/861/863/828,W854/848/862/849/864/851 | 원인해소조건없는Reset가지 확인 | 실제복구/재기동미수행 |
| E18 | 입력회로끝점 | Electrical_Rev2.pdf FG52/PDF53→FG120/PDF121 | KM1 13/14,E4.3,입력단자4 시각확인 | 현행모듈/단자·극성 |
| E19 | 출력회로끝점 | 같은PDF FG139/PDF140→FG52/PDF53 | 출력단자34,A3.3,XS41/42,코일A1/A2 | 현장보조접점미기재번호 |
| E20 | 시공케이블원문 | Electrical_Can_Decoating_20241118.pdf PDF51행1_4/PDF21 FN06행 | 직접렌더·식별자·경로열대조 | 승인준공도/현재케이블 |
| E21 | 운전시간원문 | S/0320-FlgNet.xml Add1864,Ge1871,Move1874/1877,W1902/1903;0615RID208/210 | MIN+1,HOUR Move1,MIN Move0 확인 | 원본의도·Tag47주기·ENO |
| E22 | 별도운전시간초기화 | S/0338-FlgNet.xml Move2955,W2981/2982/2983;0615RID210,NID53UID2969 | 앞Move의eno/상수0/HOUR경로 | 호출·실행·초기화조작 |
| E23 | 호출경계 | S/0549-FlgNet.xml W351,CRef319/328/334;0688RID67/76/82,NID7;0031/0688RID58,NID6 | ON허가와호출대상 대조 | 전체호출순서/현재CPU |

## 7.2 필요한 자료와 수집 위치

| 누락ID | 필요한 자료 | 필요한 이유/판정 기준 | 자료 없이 남길 상태 |
| --- | --- | --- | --- |
| G01 | 현행 PLC 프로젝트/CPU 비교·원본 해시·승인 변경기록 | 백업과 현재프로그램 일치,호출/다중쓰기/전원복귀 | live_cpu 미수행 |
| G02 | 현행 HMI Inputs 호출·ENO·DB13 배치·다중 쓰기 대조 | 정적 Word 전송은 E24로 확인; 현재 실행·최종값은 미확인 | raw/processed별개,정적연결확인 |
| G03 | HMI1198 인스턴스/피연산자선언,DB11/DB2레이아웃,dde.cfg·화면이벤트 | 알람/응답/요청의 실제 읽기·쓰기 연결 | 주소설정만확인 |
| G04 | 현행 M26/FN06 명판·태그사진·승인배치 | 팬본체/모터관리관계와설비동일성 | identity_verified:false |
| G05 | 최신승인 전기도면·단자/케이블표·보호기기명판/설정기록 | QM범위와실설정구분,QS/QM/KM접점·극성·실배선 | 도면상경로만확인 |
| G06 | 운전시간 기능명세·Tag47/48 생성원본·현행값 | Move1/초기화의도와주기·ENO 의미 | 시간누적정상단정금지 |
| G07 | 승인된 현장관찰·원인조치·복구기록 | 알람Reset/전기응답/실제송풍 정상분리 | repairs_completed=0 |
| G08 | 시공참고PDF와준공변경대조 | PDF21/51경로표기의현행적용 | first draft design보존 |

## 7.3 네 기능 적용·기록 보존 제안

| 기능 | FN06 적용 제안 | 이번 구현/시험 상태 |
| --- | --- | --- |
| 도면·래더 비교 | FG52↔LAD1955/1802,FG120↔원시입력·LAD1032,FG139↔Coil776,PID↔식별경계 | 비교근거만초안. UI구현/링크·모바일검증은Codex담당 |
| 백업·선택 복원 | FN06/P18의기존키정책을따르고미지필드/다른설비/초안보존,실데이터복사금지 | 실행안함 |
| 기록 전후 비교 | 요청/출력/원시/처리/HMI를다른관찰항목으로유지,시각·단위·근거버전포함 | 실행안함 |
| 관찰보고서/PDF | 알람해제와복구완료구분,G01~G08와미해석값표시 | 문서구조만제안,프로그램PDF생성/시험안함 |

## 7.4 확인·미실행 상태

| 구분 | 상태 | 근거 |
| --- | --- | --- |
| documentation | draft_with_gaps | 7영역·근거표·누락목록작성 |
| original_source_review | performed_limited | 명시한XML/선언/Wire와PDF페이지정적·시각대조 |
| independent_review | pending | 지정Codex가핵심근거재확인. 자체조사를독립검토로세지않음 |
| static_product_tests | not_run | 코드반영·생성기/완료검사는Codex역할 |
| ui_records | not_run | 저장/재읽기/복원/화면행동시험없음 |
| publication | not_published_by_dot | 이초안을운영프로그램에반영하지않음 |
| tia_compile / live_cpu / field_recovery | not_performed | 문서검토와구분 |
| simulator | permanently_stopped | 작성/수정/생성/실행/행동시험0 |

수행한 것은 공개Git읽기·문서/JSON/CSV/XML읽기·원본구조추출·PDF렌더·해시확인·이MD작성이다. 저장소 생성기나 npm/TIA/시뮬레이터 테스트를 실행하지 않았다. 정적 보조 스크립트는 XML 노드·선언·연결의 읽기 추출만 수행하며, PLC 상태전이·타이머 실행·출력 시뮬레이션을 구현하거나 실행하지 않았다.

## 7.5 Codex 인계: 전 과정 재조사 대신 핵심 재확인

1. FN03 마무리와 충돌하지 않게 현재 main/dirty파일을 보존한다. 이 초안 기준 커밋과 현행 main의 FN06 원본 차이만 먼저 확인한다.
2. E06~E10: 0437/0656/0657/0658의 MBVA01_FAULT·Tag67/T91/2초와0257의RD01분기반전·출력을 재확인한다.
3. E11~E14: FN06 Set/Reset4쓰기와버너준비OR를 확인한다. 40/60을 시간단위추정으로바꾸지 않는다.
4. E15~E16: 미해석HMI바인딩을유지한다. 추가원본이있으면해당4대상과CRef만좁혀확인한다.
5. E18~E20: 도면끝점·모터M26·직접기동·케이블식별자/원문표기를 확인한다. FN03부품/타이머를복제하지 않는다.
6. E21~E22: HOUR Move1/ENO/초기화는원본그대로재검토한다. 문서오해를막되프로그램수정안으로자동승격하지 않는다.
7. 반영시7영역수·알람수·근거수는실제FN06항목에서산출한다. BC01 36이나FN02/FN03수량을맞추지 않는다. 미확정·기존기록은그대로보존한다.
8. 코드반영·공통검사·UI/기록·버전·배포·완료대장은지정Codex만담당한다. 그결과를받기전이초안을게시완료로표시하지않는다.

## 다음 한 대상

이 초안 전달 후 자체 조사 다음 대상은 **MC04(P08)** 이다. FN06 추가 원본/핵심 재확인과 제품 반영은 지정 Codex가 맡으며, dot은 같은 FN06 전체 조사를 반복하지 않는다. 최신 사용자 지시에 따라 후속 대상은 MC04 한 개로 유지하며 VS01로 자동 진행하지 않는다. 2차133후보는 제외한다.

## 부록: 원본 지문

아래 SHA-256은 조사 복사본의 해당 파일 바이트 기준이다. 현재 CPU·현장 일치의 증거가 아니다.

| all-in-one/ 아래 경로 | SHA-256 |
| --- | --- |
| sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
| registers/equipment-hmi.csv | 2cdce600aa0138cc5025022e57d9d61a948afb237f70c70e2d11e8300e73286a |
| registers/plc-symbols.csv | a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f |
| sources/decoded-original/0437-FlgNet.xml | ccf6915ca1b5779245b16ef9790cd042ded33f0a494b6a75660f86e308c76ed7 |
| sources/decoded-original/0257-FlgNet.xml | 43434bcdfb9edb02b979fdc5096fea94636708d316a58dc342719e3b28d194da |
| sources/decoded-original/0164-FlgNet.xml | 15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491 |
| sources/decoded-original/0165-FlgNet.xml | 4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88 |
| sources/decoded-original/0166-FlgNet.xml | 0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853 |
| sources/decoded-original/0174-FlgNet.xml | 23fb073206f95c69abc4373d3080081a369e4dd5021c2bd1a90d63029bb908d5 |
| sources/decoded-original/0320-FlgNet.xml | 4279b69c8bbb37cfcea7b5e389bb66c5d48ef2c45ce7447ee8ba456c48f6d8bd |
| sources/decoded-original/0338-FlgNet.xml | 762ab4b1520aa101efc897ff9e4b72a35f5591ff460a0b654dc87919849077a1 |
| sources/decoded-original/0375-FlgNet.xml | 65964c3f68a169b10a0600fd36847c2fa508cb881794c087e3b77da5d84cba22 |
| sources/decoded-original/0355-FlgNet.xml | 73592d33f8b3a71effeb36f25427c76e931485e7ce31f5c81f144ddae83c4247 |
| sources/decoded-original/0549-FlgNet.xml | 49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1 |
| sources/decoded-original/0031-FlgNet.xml | 76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65 |
| sources/decoded-original/0656-IdentXmlPart.xml | 0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592 |
| sources/decoded-original/0657-IdentXmlPart.xml | 0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b |
| sources/decoded-original/0658-IdentXmlPart.xml | 998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831 |
| sources/decoded-original/0602-IdentXmlPart.xml | 46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf |
| sources/decoded-original/0604-IdentXmlPart.xml | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af |
| sources/decoded-original/0613-IdentXmlPart.xml | 09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb |
| sources/decoded-original/0615-IdentXmlPart.xml | 80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a |
| sources/decoded-original/0575-IdentXmlPart.xml | 40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06 |
| sources/decoded-original/0577-IdentXmlPart.xml | 511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47 |
| sources/decoded-original/0578-IdentXmlPart.xml | 0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b |
| sources/decoded-original/0582-IdentXmlPart.xml | 41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951 |
| sources/decoded-original/0585-IdentXmlPart.xml | e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184 |
| sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda |
| sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| sources/decoded-original/0621-IdentXmlPart.xml | a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee |
| sources/decoded-original/0622-IdentXmlPart.xml | f0b997f1246d76cff71de2160eb617caa936e6987bdf43c73f55cdcf77dccdb6 |

### E24 추가 원본 지문 (v1.7.0 main 기준)

| all-in-one/ 아래 경로 | SHA-256 |
| --- | --- |
| sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 |
| sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd |
| sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| sources/decoded-original/0655-IdentXmlPart.xml | 38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb |
| sources/decoded-original/0030-FlgNet.xml | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b |
| sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda |
| sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| sources/decoded-original/0694-IdentXmlPart.xml | 757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d |
