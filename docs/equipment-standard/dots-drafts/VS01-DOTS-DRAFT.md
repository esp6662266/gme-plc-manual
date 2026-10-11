# VS01(P09) 조사·문서 1차 초안

- 문서 상태: 원본 대조를 포함한 초안. 코드 반영·독립 검증·게시 전. 실제 설비 진단·수리 완료 문서가 아니다.
- 대상: catalog_id VS01, priority_key P09, 진동 스크린, motor/원료 이송. VS01/VS01A·M06/M07·공통 구동기·스크린 본체의 관계를 구분한다.
- 기준: GME-STD-1.0.0, 공개 저장소 main/all-in-one/.
- 고정 조사 커밋: 10051ddf45f6fd740d057bda51bee3db5a57382e, VERSION v1.7.0. 2026-10-11 05:53 UTC 공개 main도 이 커밋임을 확인했다. FN06 v1.8.0 검증 완료·게시 전 패키지 확인은 사용자가 전달한 별도 진행 상태이며, 이 조사에서 배포를 실행하거나 게시 완료를 주장하지 않는다.
- 조사자: 사용자의 dot, 자체 환경에서 직접 조사·작성. 실행 모델/추론 수준의 관측값은 미확인. 사용자/지정 Codex가 코드 통합·검증·게시를 담당한다.
- 시작: 2026-10-11 05:53 UTC / 14:53 KST. 저장 시각은 부록에 기록한다.
- 산출물: 이 MD 하나. 공통 코드·버전·완료대장·배포·운영기록은 편집하지 않았다. 실제 PLC·현장·보호값 변경과 시뮬레이터 작성/수정/생성/실행/행동시험은 수행하지 않았다.
- 새 Work/Codex 작업을 만들거나 이 조사·초안을 재위임하지 않았다. MC04 원본 전체를 반복 조사하지 않았다. 세진 설비관리 프로그램에는 변경하지 않았고 그 데이터·코드·사진·작업이력을 가져오지 않았다.

## 적용 표준과 접근 제한

공개 저장소의 .agents/skills/gme-equipment-rollout/SKILL.md, docs/equipment-standard/WORK-STANDARD.md, WORK-ITEM-TEMPLATE.md, INVENTORY.json의 7영역·원본 선언/핀 추적·원본/해석/현행 분리 기준을 적용한다. 최신 사용자 역할 제한이 우선이며 자동 코드 반영·대장 갱신·2차133개 확대는 수행하지 않는다.

자체 환경의 PDF 읽기·렌더 기능을 사용했다. 별도 tia-equipment-alarm-trace 스킬은 제공된 로컬 스킬 영역에서 찾지 못해 사용했다고 표시하지 않는다. 로컬 권한은 확장하지 않았다. Mac 인계 파일은 읽지 못했지만 공개 원본으로 조사했다. 사용자 지시에 따라 직접 Codex 창 연계를 재시도하지 않고 이 대화에 파일을 첨부한다.

### 원본 경로 표기

- S/ = all-in-one/sources/decoded-original/.
- R/ = all-in-one/registers/.
- 네 자리 XML 번호는 S/ 아래 파일을 뜻한다. 예: 0430은 0430-FlgNet.xml, 선언 0658은 0658-IdentXmlPart.xml.
- LAD 숫자는 문서/검색 ID, NID는 원본 선언의 네트워크 ID다. 같다고 가정하지 않는다.
- Part/Wire/ORef/CRef의 UID와 선언의 RID·CS/C NID/UID를 함께 맞췄다. 동일 RID/UID가 다른 선언 파일에 나타나도 자동 연결하지 않았다.
- [고정 커밋 원본](https://github.com/esp6662266/gme-plc-manual/tree/10051ddf45f6fd740d057bda51bee3db5a57382e/all-in-one). 끝에 실제 파일 SHA-256을 제공한다.

## 먼저 재확인할 핵심

1. 도면상 **공통 27AS1 인버터 하나가 M06 VS-01과 M07 VS-01A 두 모터를 구동**한다. 각 모터는 8.3kW·14.6A 표기이며 두 분기 QM/QS/케이블을 별도로 가진다. 공통 RUN I1.1은 두 모터 각각의 회전·진동 정상 증명이 아니다.
2. VS01 운전 감시는 Tag_59 %T60, SD S5T#2S, LAD1794 Part545다. FAULT와 INV가 이 타이머를 공유한다. 다른 설비의 Tag57/T54/5초나 팬 태그를 복제하지 않는다.
3. 운전 요청 해제는 ON AND (VS_01_FAULT OR VS01_INV). 최종 StartVS01은 ON AND Flag.M_VS_01이다. MC04의 VS01/유지보수 분기를 VS01 자체 기동 조건으로 가져오지 않는다.
4. 원시 I1.1/I1.2는 IW0→Inputs DB13 Word0의 정적 전송을 통해 DB13 1.1/1.2에 연결된다. 호출 ENO/NOT Simulation(1), 현재 CPU·다른 쓰기·정상극성은 별도 경계다.
5. 브레이크 요청 Start VS01 BRAKE는 메모리 %M11.0, 물리 출력 Braking VS01은 %Q49.5다. 이름의 Start를 보고 Q로 분류하지 않는다.
6. 브레이크에는 별도 Tag_117 %T69, SD S5T#2S가 있다. 운전 고장 감시와 같은 2초여도 서로 다른 타이머다. 이 회로는 OFF 조건, 제목 (off), 출력 주석 it's no longer there를 함께 보존한다. 현장 사용·삭제 완료 어느 쪽도 단정하지 않는다.
7. 브레이크 Set 식에는 NOT FAULT가 있지만 NOT INV는 없다. Reset에는 INV가 포함된다. 두 쓰기 조건이 겹칠 수 있는 원본 형태를 보존하며 실제 스캔 우선순위를 추정하지 않는다. SD와 그 접점의 조합을 “2초 제동 펄스”로 바꾸지 않는다.
8. 자동 요청 단계는 예열17 Reset, 생산18 Set, 정지21 또는 Emergency Reset이다. 다른 설비의 생산24/정지19와 다르다. 숫자를 초 단위로 임의 변환하지 않는다.
9. HMI 설정 3행은 확인했으나 LAD1184 실제 바인딩 8개는 미해석이다. DB11,X12.1을 FAULT 또는 INV 단독 표시로 확정하지 않는다.
10. VS01 운전시간의 HOUR는 원본 Move 상수1이다. MIN Add1과 구분한다. HOUR 초기화 LAD1050의 VS01 Move는 해당 네트워크의 첫 Move라 Tag48 접점에서 직접 en으로 들어간다.

## 7영역 적용표

| 영역 | 상태 | 작성 범위 | 미확정 경계 |
| --- | --- | --- | --- |
| 설비·자료 기준 | 적용 | P09/VS01, 본체·두 모터·공통 인버터, 공정·자료 시점 | 실제 자산 관계·명판·현행 설치 |
| I/O·HMI | 적용, 일부 미확보 | I1.1/I1.2/Q0.6, M11.0/Q49.5, 두 타이머, DB 전송, HMI 설정/핀 | HMI 이벤트·인스턴스, 실제 브레이크 회로 |
| 제어 구조 | 적용 | 자체 요청/출력·자동 단계·브레이크·MC04 소비 경계·시간 기록 | 호출/다른 쓰기·현재 값·전원복귀 |
| 전기 전달 경로 | 적용 | FG27/28/117/136, Reset/STO FG17/14, 시공34/51 실제 페이지 | 준공·극성·보호설정·브레이크 출력 끝점 |
| 알람·복구 | 적용 | FAULT/INV 공유2초·Reset·영향, 브레이크 타이머 분리 | 실제 고장코드·원인회복·재기동 |
| 증상별 수리 | 적용, 관찰 초안 | 공통응답/개별모터·기동전달·브레이크·HMI·시간 증상 구분 | 실제 측정·조치·복구 미수행 |
| 완료 기준 | 적용 | 근거표·누락 목록·Codex 핵심 확인·상태 분리 | 코드/UI/게시·TIA·CPU·현장 검증 |

# 1. 설비·자료 기준

## 1.1 관리 식별과 실제 관계

INVENTORY priority P09는 VS01 태그 대응이지만 identity_verified:false, catalog parent_id:null, existing_detail:symptom, bc01_standard_acceptance:not_assessed다. 이 상태를 이번 문서만으로 완료로 바꾸지 않는다.

원본 sources/PID_1684n002I.pdf PDF1 Rev.I의 VS-01은 MC-04 배출 뒤에 있고 M06/M07, 8.3+8.3kW·440V로 표시된다. Electrical_Rev2.pdf FG27/PDF28은 M06 VS-01과 M07 VS-01A로 나누어 그린다. 시공 참고 PDF51은 두 행 모두 VS-01로 쓰면서 M06/M07·케이블을 구분한다. VS-01A라는 전기 표기, VS01 단일 catalog, 본체와 두 구동 모터의 관리 관계를 각각 보존한다. 별도 catalog를 이름만으로 만들거나 두 모터를 하나의 실물로 합치지 않는다.

27AS1은 공통 구동기, M06/M07은 각각 모터 분기, 스크린은 공정 본체다. 근처 MC04·PV03·다른 컨베이어의 알람이나 Q를 VS01 소유로 전환하지 않는다. 기계 진동 방향·편심 추·베어링·체결·회전 관계는 이 PLC 백업만으로 확정하지 않는다.

## 1.2 자료 시점·기존 내용 보존

- FG27/28/117/136 표제란: 기본 일자27.05.2024, 해당 페이지 REV2/17.03.2025. FG14의 개정 표시는 별도로 읽고 임의 보충하지 않는다.
- Electrical_Can_Decoating_20241118.pdf는 24.11.11 first draft design 시공 참고다. 고객명이 표제란에 있어도 이번에는 GME 공개 저장소에 이미 있는 원본으로만 사용했다. 세진 관리 앱 데이터가 아니다.
- procedures/VS01.html, devices/VS01.html의 기존 증상·브레이크 OFF/폐지 주석·현장 미확정 및 관련 제어/알람/전기/신호 파생 자료를 읽었다. 파생 문서는 원본 위치를 찾는 색인으로 사용하고 핵심 조건은 XML/선언/실제 도면과 대조했다.
- 기존 백업 파일명과 내부 프로젝트 날짜 차이, P&ID/전기 세대 차이, 주석 옛 주소, SOURCE-XML 해석 경계는 해결 처리하지 않는다.
- 기존 시뮬레이터 링크·과거 시험 설계·확인 대장은 보존 자료이며 이번 실행 근거가 아니다. 새 시험 설계·모델·동작 검증을 만들지 않았다.

# 2. I/O·HMI·주소·전달

## 2.1 영역별 신호

| 대상 | 백업 주소/형식 | 원본 위치 | 해석·경계 |
| --- | --- | --- | --- |
| VS01_Fbk | %I1.1 Bool | 0613 RID158/NID26 UID1450, SAD Input/AO9; R/plc-symbols.csv 문서493 | 공통 드라이브 RUN. 개별 모터 정상 보증 아님 |
| vs01_all_inv | %I1.2 Bool | R/plc-symbols.csv 문서917; FG27 ALARM→FG117 E1.2; Word 전달 | 원시 심볼의 단독 선언 참조는 이번에 미확보. 주소·도면·Word 경로 구분 |
| Start VS01 | %Q0.6 Bool | 0602 RID73/NID13 UID386, SAD Output/AO6; 0248 W393 | 공통 기동 출력. 주석의 옛 A49.0과 구분 |
| Flag.M_VS_01 | DB member Bool AO6 | 0604 RID72/NID13 UID384/385; 0577 RID31/NID3/4/5 | 요청/기억. 출력 Q와 다른 영역 |
| Inputs.VS01 run | Inputs DB13 bit9(1.1) | 0657 RID279/NID16 UID605/562, BIRID247; 0655 Inputs DB13 | 알람·브레이크·MC04에서 쓰는 DB 응답 |
| Inputs.VS01_All_Inv | Inputs DB13 bit10(1.2) | 0657 RID280/NID16 UID609/31 | 알람 DB 입력. 원시 I와 분리 |
| Allarm.VS_01_FAULT | Allarm member Bool AO6 | 0657 RID68/NID16 UID563/565/566 | 원문 밑줄 유지. HMI 단독 표시 대응은 미확정 |
| Allarm.VS01_INV | Allarm member Bool AO155 | 0657 RID218/NID16 UID597/25/28 | 철자 VS01_INV 유지. FAULT와 타이머 공유 |
| Tag_59 | %T60 Timer | 0658 RID66/NID16 UID560/561, SAD Timer/AO60 | 운전 FAULT/INV 감시, SD 2초 |
| Start VS01 BRAKE | %M11.0 Bool | 0602 RID74/NID14 UID449/452/454, SAD Memory/AO88 | 브레이크 요청 래치. 물리 Q 아님 |
| Tag_117 | %T69 Timer | 0602 RID77/NID14 UID456/457, SAD Timer/AO69 | 브레이크 경로의 별도 SD 2초 |
| Braking VS01 | %Q49.5 Bool | 0602 RID78/NID14 UID458, SAD Output/AO397; CSV 문서461 | 주석 it's no longer there. 실제 회로 끝점 미확보 |
| OFF | %M0.1 Bool | 0602 RID33/NID14 UID445, SAD Memory/AO1 | Bool 메모리다. 이름만으로 상수FALSE·현재0을 확정하지 않음 |

주소는 선언 영역·자료형과 함께 읽는다. Flag/Allarm의 AO6과 Q0.6은 같은 값이거나 같은 저장 위치라는 뜻이 아니다. 타이머 주소는 Timer 영역 번호이며 HMI 태그/물리 I/O로 세지 않는다.

## 2.2 원시 I1.1/I1.2 → Inputs DB13의 정적 전송

0397-FlgNet.xml HMI Inputs/LAD1070/NID1:

1. Powerrail Wire21→Move22.en. 입력 Wire23/ORef25→0627 RID3/NID1 UID25 Tag_178, Word, SAD Input/AO0, 즉 IW0.
2. Move22.out1 Wire24/ORef26→0629 GlobalAccess RID5/NID1 UID26, Word AO0, BAD BIRID4.
3. BIRID4는 0628 DepDBBlock RID4 Inputs, TOD N13/DB, CID638561979615757134다. 따라서 목적지는 Inputs DB13 Word0.
4. 0657 RID279/280은 VS01 run/all_inv의 BO9/10이며 BIRID247을 가진다. 0655 RID247도 같은 Inputs/DB13/CID다. IW0가 포함하는 I1.1/I1.2는 DB13 1.1/1.2로 연결된다.
5. 이 Word Move 자체에는 비트 반전이 없다. 원본 DisableENO="true" 및 주변 ENO 연결을 보존한다. 이 확인은 원본 정적 경로이며 현재 물리 신호·최종 DB값을 읽은 것이 아니다.

호출은 Main 0030 LAD1613/NID19에서 Recipes Handler CRef21→ENO W32→HMI CRef23→ENO W33→HMI Output CRef25→ENO W42→반전 Contact37→W43→HMI Inputs CRef28.en이다. Contact37.operand=W44/ORef45, 0692 RID140 Simulation(1) %M180.0. 0688 RID135/NID19 UID29와 0694 RID136/TORID135가 HMI Inputs 호출을 확인한다.

따라서 앞선 ENO와 NOT Simulation(1) 조건이 호출 경계다. 현재 메모리값·CPU 실행·호출 주기·다른 쓰기의 최종 영향은 미확정이다. legacy simulation의 Inputs.VS01 run 쓰기 존재는 물리 응답 증거가 아니며 해당 블록을 실행/수정/생성하지 않았다.

## 2.3 HMI 설정과 VS01 호출

sources/hmi_plc_tags.csv, R/equipment-hmi.csv에서 확인한 설정:

| 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| VS_01\RispostaA | DB11,X12.0 | PLC | 00322 |
| VS_01\Flag | DB2,X0.6 | PLC | 001AE |
| VS_01\Allarme1 | DB11,X12.1 | PLC | 0003D |

설정 행은 실제 화면 이벤트·현재 통신·PLC 바인딩 완료 증거가 아니다. 원본 호출은 0362-FlgNet.xml LAD1184, CRef23/RID638 안의 CodeBlock22/RID1이다.

| 핀 | Wire | ORef UID / RefId | 확인 상태 |
| --- | --- | --- | --- |
| en | 21 | Powerrail | 정적 직접 연결 |
| Ingresso_run | 24 | 25 / 708 | 실제 대상 선언/NID 미해석 |
| Allarme1 | 28 | 29 / 101 | 미해석 |
| Allarme2 | 30 | 31 / 102 | 미해석 |
| Allarme3 | 32 | 33 / 48 | FALSE 선언 후보, 해당 호출 NID 확정 전 보류 |
| Allarme4 | 34 | 35 / 48 | 같은 경계 |
| Allarme5 | 36 | 37 / 48 | 같은 경계 |
| Risposta | 42 | 43 / 95 | 미해석 |
| Comulativo_allarmi | 46 | 47 / 97 | 미해석 |

0623 FCBlock RID1의 HMI Standard Motors, 0624 BlockInterfaceInfo RID638은 후보지만 숫자만으로 VS01 인스턴스를 확정하지 않는다. 같은 UID/RID 검색에서 다른 파일의 Start BC01/ON도 후보로 나올 수 있으므로 블록/NID 없이 채택하지 않는다.

공통 함수 0355/0621 Local 선언의 Ingresso_run→Risposta, 5개 알람 OR→Comulativo_allarmi와 VS01의 실제 바인딩은 별도다. FAULT/INV가 어느 인수로 들어가고 DB11로 어떻게 연결되는지는 원본 HMI 프로젝트·해당 NID 선언·DB11/DB2 레이아웃·이벤트가 필요하다. HMI Allarme1을 VS01_FAULT 하나의 별칭으로 확정하지 않는다.

## 2.4 속도·전류·개별 진동 신호의 경계

이번 VS01 태그·원본 연결·FG27/28에서는 MC04의 QW294/10~100/272 변환이나 전류 IW324 같은 경로를 VS01 소유로 확인하지 않았다. FG27에 외부 속도 지령의 AI 배선이 그려지지 않았다는 사실만으로 현행 고정속도·설정 Hz를 추정하지 않는다. 드라이브 현재 파라미터와 승인된 설계가 필요하다.

개별 M06/M07 회전·진동·전류·과부하별 PLC 알람을 새로 만들지 않는다. 두 분기 보호접점은 아래 공통 명령 전달에 직렬로 포함되지만, 각각 독립된 PLC 상태 입력이나 개별 고장 코드라는 근거는 아니다.

# 3. 제어 구조·소유·복수 쓰기

## 3.1 공통 기동 출력의 직접 소유

LAD1943 0248-FlgNet.xml, NID13:

ON AND (Allarm.VS_01_FAULT OR Allarm.VS01_INV) → RCoil377 Flag.M_VS_01

- ON Contact395.operand W387/ORef382→0602 RID1. out W396은 FAULT Contact397, INV Contact22, 요청 Contact399로 분기한다.
- FAULT Contact397.operand W388/ORef383→0604 RID71. out W398→OR24.in1.
- INV Contact22.operand W21/ORef23→0604 RID207. out W25→OR24.in2.
- OR24.out W26→RCoil377.in, operand W390/ORef384→0604 RID72 Flag.M_VS_01/Write.

ON AND Flag.M_VS_01 → Coil381 Start VS01

- 요청 Contact399.operand W391/ORef385→0604 RID72.
- Contact399.out W400→Coil381.in, operand W393/ORef386→0602 RID73/Q0.6.

고장 두 분기가 요청을 해제하고 별도 Coil이 Q를 쓴다. 이 네트워크에는 MC04의 VS01 미응답·유지보수 분기를 추가하지 않는다. 현재 CPU의 실행/다중쓰기 최종값·동시 Set/Reset 우선순위는 별도 확인 대상이다.

## 3.2 자동 요청의 VS01 고유 단계

| 네트워크 | 동작 | 정적 조건 | 대상 핀·선언 |
| --- | --- | --- | --- |
| 0164 LAD1843/NID3 | RCoil456 | ON AND NOT Emergency_module_fault AND Tipo_preset=1 AND Auto_ON1 AND Tempo_presetting=17 | W706/ORef614→0577 RID31 Flag.M_VS_01; 비교17=0578 RID30/UID613 |
| 0165 LAD1844/NID4 | SCoil786 | ON AND NOT Emergency_module_fault AND Auto_ON1 AND Tipo_preset=2 AND Tempo_presetting=18 | W1051/ORef955→0577 RID31; Eq783 W1047/1048,18=0578 RID81/UID954 |
| 0166 LAD1847/NID5 | RCoil975 | Auto_ON1 AND Tipo_preset=5 AND (Tempo_presetting=21 OR Emergency_module_fault) | W1087/ORef1024→0577 RID31; Eq969 W1083/1084,21=0578 RID37/UID1022; Emergency Contact1102/W1105 |
| 0248 LAD1943/NID13 | RCoil377 | ON AND (FAULT OR INV) | W390/ORef384→0604 RID72 |

0577 RID4=Auto_ON1, RID12=Tipo_preset, RID7=Tempo_presetting, RID108=Emergency_module_fault를 각 NID/UID로 대조했다.

상수17/18/21은 비교 숫자다. Tempo 이름만으로 초 단위를 확정하지 않는다. 정지 네트워크0166에는 별도 ON 직렬 접점을 임의 추가하지 않는다. HMI Flag 설정 주소는 있어도 실제 이벤트 writer는 미해석이므로 위 네 위치가 모든 쓰기의 완전한 목록이라고 주장하지 않는다.

## 3.3 브레이크는 별도 OFF 조건 경로

LAD1944 0249-FlgNet.xml, NID14, 제목 vs01 brake (off):

### A. 요청 Set

OFF AND NOT Flag.M_VS_01 AND NOT Inputs.VS01 run AND NOT Allarm.VS_01_FAULT → SCoil425 Start VS01 BRAKE

- OFF Contact479/W459 ORef445→0602 RID33.
- out W480→NOT 요청 Contact481(W460/ORef446/0604 RID72)→W482→NOT run Contact483(W461/ORef447/0604 RID224)→W484→NOT FAULT Contact485(W462/ORef448/0604 RID71)→W486→SCoil425.
- operand W464/ORef449→0602 RID74 Memory AO88=%M11.0.

### B. 요청 Reset

OFF AND (Flag.M_VS_01 OR Allarm.VS_01_FAULT OR Allarm.VS01_INV) → RCoil431 Start VS01 BRAKE

- OFF 후 Contact487(요청) W488, Contact489(FAULT) W490, Contact22(INV) W24가 OR428.in1/in2/in3로 합쳐진다.
- OR428.out W467→RCoil431.in, operand W469/ORef452→0602 RID74.
- Set 식에 NOT INV는 없고 Reset에 INV가 있다는 비대칭을 보존한다. 조건이 겹치는 경우의 현재 결과는 실행 순서·타이머·호출을 검증하지 않고 단정하지 않는다.

### C. 타이머와 출력

OFF AND NOT Inputs.VS01 run AND Start VS01 BRAKE → SdCoil439 Tag_117, S5T#2S

- OFF 후 NOT run Contact491(W470/ORef453)→W492→요청 Contact493(W471/ORef454)→W494가 SD439.in과 timer접점495.in으로 분기한다.
- SD439.value W472/ORef455→0606 RID76/NID14 UID455 S5T#2S, stored V512.
- SD439.operand W473/ORef456→0602 RID77/NID14 UID456 Timer AO69=%T69.
- Contact495.operand W474/ORef457은 같은 Tag117. out W496→Coil444, operand W476/ORef458→0602 RID78 Output AO397=%Q49.5.

따라서 출력 식은 OFF AND NOT run AND BrakeRequest AND Tag117이다. SD 지연과 접점 경로이지 “2초만 브레이크를 켜는 펄스”라고 확인한 것이 아니다. 브레이크 타이머를 FAULT/INV 감시 Tag59와 합치지 않는다.

OFF는 메모리 M0.1이므로 이름만으로 현재false로 대체하지 않는다. 반대로 원본에 회로가 남았다는 이유로 현장 브레이크가 사용 중이라고도 말하지 않는다. 원본 제목·주석·Q49.5·실제 회로 미확보를 함께 남긴다. 시뮬레이터로 이 경로를 시험하거나 OFF를 바꾸지 않았다.

## 3.4 MC04 등 주변 소비 경계

VS01 공통 응답은 MC04의 기동 요청 해제 분기에서도 읽힌다. 그 좁은 연결은 0247 LAD1941의 NOT Inputs.VS01 run Contact26/W25/ORef27→0604 RID224, 뒤에 NOT Allarm.Maintenance_ON Contact380이 직렬인 경로다. 이는 **MC04 출력 소유 쪽에서 VS01 응답을 소비하는 관계**다. VS01의 Q0.6 writer는0248이며 MC04 Q0.4를 VS01 소유로 합치지 않는다. MC04 전체 분석·아날로그 변환·코드 반영은 반복하지 않았다.

VS01 공통응답 상실이 MC04 요청에 영향을 줄 수 있다는 정적 연결과 실제 현장 정지 전파·시각 순서는 구분한다. 실제 시간 순서·보호 동작·재기동은 미확인이다.

## 3.5 호출과 운전시간

Main 0031 LAD1619/NID6의 ON 후 CRef264/CodeBlock275는 Allarms1, 0549 LAD1620/NID7의 ON 후 CRef319/CodeBlock337은 Motors1, CRef334/CodeBlock347은 time work motor다. 블록 선언은0688 RID58/67/82이며 해당 NID·UID와 연결한다. 정적 호출 연결을 현재 CPU에서 매 스캔 실행됐다는 증거로 바꾸지 않는다.

Auto start motors 호출 선언은0067 RID39/NID4 UID186에 있으나 상위 실행 조건·레시피 현재 값·다른 쓰기 순서는 추가 확인 대상이다. HMI/입력 전달은2.2의ENO 경계도 유지한다.

### 운전시간 LAD1024

0313-FlgNet.xml, NID26:

- Tag47 Contact1478→W1479→VS01_Fbk Contact1480→W1481로 Add1432.en 및 Ge1439.pre.
- MIN Add1: W1463/ORef1451(MIN), W1464/ORef1452(상수1), out W1465/ORef1453(MIN).
- MIN>=60: Ge1439 W1466/ORef1454(MIN), W1467/ORef1455(60), out W1468→Move1442.en.
- HOUR 쓰기: Move1442.in W1470/ORef1456=상수1, out1 W1471/ORef1457=VS_01_HOUR. **HOUR Add가 아니라 Move1이다.**
- Move1442.eno W1472→Move1445.en. in W1473/ORef1458=0, out1 W1474/ORef1459=MIN. eno W1475→SCoil1448 Flag_Aggiorna_DB/W1476/ORef1460.
- 선언0613 RID158=raw VS01_Fbk,0615 RID160=MIN/RID162=HOUR,0616 RID7=1/RID8=60/RID12=0, NID26 UID 일치 확인.

### 초기화 LAD1050

0337-FlgNet.xml, NID52: Tag48 Contact2925.operand W2910/ORef2899→0613 RID284. Contact2925.out W2926→Move2884.en, in W2911/ORef2900=0, out1 W2912/ORef2901→0615 RID162 VS_01_HOUR. 이 네트워크에서 VS01은 **첫 Move**다. 다른 설비의 후단 ENO 초기화 경로를 복제하지 않는다. Tag47/48 실제 생성 주기·현재 누적값·전원복귀·HOUR Move1의 기능 의도는 미확인이다.

# 4. 전기 전달 경로 — FG·실제 PDF 끝점

아래 FG27/PDF28,FG28/PDF29,FG117/PDF118,FG136/PDF137과 보조 FG14/PDF15·FG17/PDF18을 실제 PDF 렌더로 보았다. 도면 CPU:515/MOD 번호는 해당 판본의 표기이며 현행 CPU·모듈 식별 확인이 아니다.

## 4.1 공통 전원·인버터와 두 모터 분기

FG27/PDF28:

- 전원: 3상440V60Hz,6.2L1/L2/L3→27QM1 주접점→27R1/S1/T1→27AS1 U1/V1/W1. 선종 BLACK FS17 16mmq 표기를 그대로 유지한다.
- 27AS1 표기: ACS355-03E-38A0-4,18.5kW.
- 공통 출력 U2/V2/W2→27U1/V1/W1에서 두 분기로 나뉜다.
- M06 분기: 27QM2→27U2/V2/W2→XM의 해당 선번 단자→27QS1→M06 VS-01 U/V/W,PE. 8.3kW·14.6A.
- M07 분기: 27QM3→27U3/V3/W3→XM의 해당 선번 단자→27QS2→M07 VS-01A U/V/W,PE. 8.3kW·14.6A.
- 두 출력 분기의 실드/접지와27SCH1 표기는 도면대로 보존한다. XM 단자에 임의의 숫자 번호를 새로 붙이지 않는다.

27QM1은54–65A/RATING62A,27QM2/27QM3는각10–16A 표기다. **범위·RATING·모터정격은 현행 보호 설정·적정 조정값·실측이 아니다.** 현재 명판/승인 회로/보호기 설정 기록 없이 수치를 변경하거나 적정성을 판정하지 않는다.

공통 인버터 운전응답이 존재해도 한 분기의 개폐기·모터·기계가 정상이라는 직접 증거가 되지는 않는다. 실제 개별 회전·진동 관계는 현장 승인 관찰 및 제조사/설계 자료가 필요하다.

## 4.2 Q0.6 → 직렬 보조접점 → 28KA1 → DI1

1. FG136/PDF137 MOD14 단자7=A0.6 VS-01/VS-01A MOTOR COMMAND→FG28/2.
2. FG28/PDF29: A0.6→XS13→27QS1 보조접점→XS14→선28.1→XS15→27QS2 보조접점→XS16→선28.2→27QM1 보조접점→선28.3→27QM2 보조접점→선28.4→27QM3 보조접점→선28.5→28KA1 A1/A2→-0Vdc10.6.
3. FG27/PDF28: 27AS1 단자9 +24V→28KA1 접점1/9→단자12 DI1 START(선27.2).

두 QS와 세 QM의 보조접점이 공통 명령 릴레이 경로에 직렬로 들어간다. 어느 한 접점의 전달이 끊겨도 DI1 전달이 달라질 수 있다는 회로 해석이다. 실제 접점 정상 상태·단자 측정·고장 원인은 확인하지 않았다. Q0.6 ON=28KA1 여자=두 모터 정상이라는 등식을 만들지 않는다.

## 4.3 공통 RUN/ALARM → 입력 모듈

- RUN: FG27 +24Vdc10.7→27AS1 단자17 RUNNING, 단자19→E1.1→FG117/2. FG117/PDF118 MOD8 단자12=E1.1 FEEDBACK MOTOR VS-01/VS-01A.
- ALARM: FG27 +24Vdc10.7→단자20 ALARM, 단자21→E1.2→FG117/3. FG117 MOD8 단자13=E1.2 ALARM MOTOR VS-01/VS-01A.
- FG27 단자22/GND10/DCOM11의-0Vdc10.6 공통 연결도 보존한다.

공통 출력의 기능 설정·실제 NO/NC 정상극성·단선 시 입력값·내부 처리의 현재 실행은 별도다. 원본 알람 식에서 run은 반전,all_inv는비반전으로 읽힌다는 사실과 실제 전기 정상 상태를 혼동하지 않는다. 각각의 모터가 아닌27AS1의 공통 신호라는 한계를 화면/보고서에 표시해야 한다.

## 4.4 Reset·STO는 브레이크 출력과 다른 경로

- 드라이브 Reset: FG27 단자9 +24V→17KA1 접점4/12→단자15 DI4 RESET,선27.7. FG17/PDF18에서17KA1 코일A1은A7.4, A2는-0Vdc10.6. 17SB2 RESET ALARMS는E19.7 입력이다.
- PLC Flag.RESET_ALLARM→A7.4의 실제 writer 전달을 이번에 끝까지 확인하지 않았으므로 버튼·PLC래치Reset·드라이브DI4를 하나의 신호로 합치지 않는다.
- STO: FG27 X1C OUT1(1)→14KA2 접점5/6→IN1(3),OUT2(2)→14KA6 접점5/6→IN2(4).
- FG14/PDF15에서14KA2는13.5계통,14KA6은13.6계통에 연결된 코일이며 A2측은0Vac9.9이다. 교차참조27/7·27/8이 보인다. 이는 하위 끝점 대조이며 상위 비상회로 전체의 안전성/성능등급·현장 동작을 검증한 것이 아니다.

DI4 Reset·STO·기동DI1은 서로 다른 기능 경로다. 이를Q49.5 브레이크의 실제 회로로 간주하지 않는다. 우회·점퍼·출력강제·보호값 조정 지시를 만들지 않는다.

## 4.5 브레이크 Q49.5의 누락 끝점

백업에서는 Q49.5가 선언되고0249에Coil이 있으나 FG27/28에는 그 출력의 실제 릴레이/브레이크 장치를 식별하지 못했다. 전체 전기 PDF의 추출 텍스트에서49.5/brak/fren 검색도 추가 연결을 제공하지 않았다. 텍스트 검색 실패는 도면 전체에 브레이크가 절대 없다는 증명이 아니다.

현재 브레이크의 실제 존재·철거/미사용 승인 기록·개정 전/후 도면·Q49.5 모듈/단자·장치명판·배선 끝점이 필요하다. 자료가 없으므로 인버터 내장 제동이나 별도 기계 브레이크 어느 쪽으로도 자동 매핑하지 않는다. 이 누락 때문에 다른 확인 가능한VS01 경로의 초안 작성을 멈추지 않았다.

## 4.6 시공 참고의 두 케이블·배관

Electrical_Can_Decoating_20241118.pdf 실제 PDF34/51:

| 위치 | M06 | M07 | 해석·경계 |
| --- | --- | --- | --- |
| PDF34 EXIT ZONE01,CONDUIT D-page17/도면034 | EXI1TB1 분기3→Pipe28→M06; cable1_20=EXI+VS01-M06A,CV6/4core | EXI1TB1 분기4→Pipe28→M07; cable1_21=EXI+VS01-M07A,CV6/4core | 공통구동기여도 현장모터 경로는 두 개 |
| PDF51 row1_20/1_21 | CR→VS-01/M06,VIBRATING SCREEN,DAC,PVC-S,4core,6SB,SPARE0 | CR→VS-01/M07,동일 케이블 사양 표기 | VS01A 대신VS-01로 쓰는 표기 차이 보존 |
| PDF51 route | 100→120→121→122→EXI1TB1→E300 | 100→120→121→122→EXI1TB1→E400 | 끝점E300/E400 별도 |
| PDF51 길이 관련 | Adjustment16,LEN88 | Adjustment16,LEN88 | 표 값이며 실측/준공 길이·단위 임의 확정 안 함 |

PDF34의CV6과PDF51의PVC-S/6SB 표기는 원문대로 남긴다. 참고 설계의 케이블 두 행을 actual 설치 완료로 바꾸지 않는다. 승인 준공도·현장 선번·모터 표지·접속함 대조가 필요하다.

# 5. 알람·타이머·Reset·복구

## 5.1 자체 FAULT/INV 공유 감시

LAD1794 0430-FlgNet.xml, NID16:

ON AND Start VS01 AND (NOT Inputs.VS01 run OR Inputs.VS01_All_Inv) → SdCoil545 Tag_59, S5T#2S

- ON Contact581/W567/ORef557→0658 RID1→W582→Start Contact583/W568/ORef558→0658 RID65.
- Start.out W584→NOT run Contact604(W607/ORef605→0657 RID279)와all_inv Contact608(W611/ORef609→0657 RID280).
- W23/W33→OR32.in1/in2→W34→SD545.in.
- value W569/ORef559→0656 RID28/NID16 UID559,S5Time 원문S5T#2S,storedV512. 같은UID/RID의0592/NID1 상수35 후보는 이 네트워크의 선언이 아니다.
- operand W570/ORef560→0658 RID66/NID16 UID560,Tag59/SAD Timer AO60(%T60). 타이머 접점 Contact585는W571/ORef561로 같은 선언을 읽는다.

V512를512ms로 읽거나 검색의다른상수35를감시시간으로채택하지않는다. 타이머명·주소·종류·상수는VS01 자체선언으로확인했다. 타이머의 현행 동작·리셋/보존·스캔 지연은시험하지않았다.

## 5.2 Set/Reset과 영향

| 대상 | 발생 Set | 해제 Reset | 원본 근거 |
| --- | --- | --- | --- |
| Allarm.VS_01_FAULT | ON AND Start AND Tag59 AND NOT Inputs.VS01 run | ON AND Flag.RESET_ALLARM AND own_FAULT | SCoil551.in W588/operand W574 ORef563; RCoil556.in W592/operand W579 ORef566;0657 RID68 |
| Allarm.VS01_INV | ON AND Start AND Tag59 AND Inputs.VS01_All_Inv | ON AND Flag.RESET_ALLARM AND own_INV | SCoil595.in W29/operand W601 ORef597; RCoil603.in W26/operand W27 ORef28;0657 RID218 |

RESET는Contact589.operand W576/ORef564→0657 RID13/Flag.RESET_ALLARM이다. FAULT/INV Set 분기는Start 및Tag59 뒤에서 나뉘지만Reset 분기는ON 뒤에서별도로RESET를읽는다. Reset 식에 원인 입력 정상·Start=0 같은 조건을 임의 삽입하지 않는다.

두 알람은0248에서운전요청Flag를Reset한다. 알람표시의해제,기동요청의재설정,드라이브자체오류해제,두모터의실제운전회복은다른판정이다. 원인이 남은 상태에서Reset되거나재발하는현재시간순서는관찰이필요하다. 모든현장드라이브고장이이두알람으로완전히설명된다고주장하지않는다.

별칭/표기 보존: VS_01_FAULT, VS01_INV, Inputs.VS01_All_Inv, VS_01\Allarme1은 역할이 다르다. 밑줄·대소문자가다르다고자동으로새알람을추가하거나,이름이비슷하다고한신호로합치지않는다. HMI 합산 바인딩은2.3미확정이다.

## 5.3 두 2초 타이머를 구분

| 항목 | 운전 고장 감시 | OFF 브레이크 경로 |
| --- | --- | --- |
| 원본 | 0430/LAD1794/NID16 | 0249/LAD1944/NID14 |
| Timer | Tag59/%T60 | Tag117/%T69 |
| Part | SD545 | SD439 |
| 상수선언 | 0656RID28/UID559 | 0606RID76/UID455 |
| 조건 | ON&Start&(!run OR inv) | OFF&!run&BrakeRequest |
| 결과 소비 | FAULT/INV Set 분기 | Coil444 BrakingVS01 Q49.5 |
| 경계 | 공통응답·현재극성·실행미확인 | 현장존재/활성·실제끝점·우선순위미확인 |

둘 다S5T#2S/SD라는이유로같은타이머나같은기능으로합치지않는다. 브레이크는운전알람의추가한개가아니며모터각각의타이머로복제하지않는다.

## 5.4 복구 완료 판정

실제복구판정에는최초드라이브상태·원인해소·원시입력/DB전달·알람Reset·요청재설정·개별M06/M07회전/진동·상류연동의같은시각증거가필요하다. 공통HMI녹색/알람없음만으로두모터정상완료를선언하지않는다. 이번실측·조치·복구는없으며repairs_completed=0이다.

# 6. 증상별 수리·관찰 초안

현장 작업 지시나 활선 측정·강제 출력·보호 조정 제안이 아니라, 승인된 절차로 확보할 증거를 구분하는 틀이다. 현장 담당자는 정지·전원 격리·작업 승인 절차를 우선한다.

| 증상 | 필요한 관찰·자료 | 비교 원본 | 구분할 원인/경계 | 복구 증거 |
| --- | --- | --- | --- | --- |
| 기동 요청이 사라짐 | Flag,FAULT,INV,모드/단계·최초시각 | 0248,0164~0166 | 자체고장Reset/예열·정지단계/HMI요청쓰기 | 원인·재요청·Q·응답의시각별기록 |
| Q0.6은 있으나 두 모터 정지 | Q,각QS/QM전달,28KA1,DI1,드라이브상태/STO표시 | FG136→28→27,FG14 | PLC명령과직렬보조접점·드라이브허가분리 | 승인점검·조치후명령전달/모터응답 |
| 공통 RUN은 있는데 한쪽이 이상 | M06/M07각각의식별·회전/진동·분기상태,공통RUN | FG27,시공34/51 | 공통응답≠개별회전/진동정상 | 양쪽각각의확인·근거자료 |
| 2초 감시 뒤 FAULT/INV | Start,Tag59,rawI1.1/I1.2,DB1.1/1.2,최초드라이브코드 | 0430/0397,FG27/117 | 실제구동미응답/인버터고장/입력전달/최초·후속알람 | 원인회복과Reset·재기동분리 |
| 브레이크 표시/출력이 예상과 다름 | M11.0,Q49.5,OFF,run,FAULT/INV,Tag117,실물·철거기록 | 0249,CSV폐지주석 | 메모리요청/Q/SD/현장존재·활성구분 | 먼저설치·사용근거확보;현재복구단정금지 |
| HMI만 운전/알람 상태 불일치 | DB11/DB2,화면이벤트,raw/DBrun,통신시각 | 0362/0355,CSV,0397 | 미해석인스턴스·합산표시·다른쓰기 | 실제바인딩·통신·원시/표시대조 |
| 시간 기록이 누적되지 않음 | MIN/HOUR,Tag47/48,초기화/전원복귀이력 | 0313/0337 | HOUR Move1과MIN Add,첫Move초기화·주기 | 기능명세·현재값·승인조사결과 |
| VS01과 MC04가 함께 멈춤 | 두설비최초알람/응답·요청시각,VS01공통응답 | 0248/0430,0247좁은소비경로 | VS01→MC04응답연동과실제정지순서분리 | 원인설비와후속정지·각각복구증거 |

관찰 기록 필드: 관찰자 / 날짜·시간·시간대 / 스크린·M06·M07·27AS1 각각의 위치·명판 / 프로젝트·도면 판본 / 모드·단계 / 원시I·DB·HMI·Q·드라이브 상태 각각의 값·단위 / 최초·후속 알람 / 수집 장치·방법 / 비교 근거 / 배제한 원인 / 승인된 조치 / 복구 증거. 실제 운영 기록을 공개 Git에 복사하지 않는다.

# 7. 근거표·누락·완료 기준·인계

## 7.1 핵심 근거표

| ID | 주장/항목 | 원본 경로·FG/PDF·선언/핀 | 해석 | 미확정 경계 |
| --- | --- | --- | --- | --- |
| E01 | P09 관리 대응 | INVENTORY priority P09/catalog VS01 | tag, identity_verified:false 보존 | 본체·모터 실물 관계 |
| E02 | 두 모터·공통 구동 | Electrical FG27/PDF28; PID PDF1 | 27AS1→M06/M07, 각 8.3kW·14.6A | 현행 명판·회전·진동 |
| E03 | 공통 Q·원시 응답 | 0602 RID73/NID13 UID386; 0613 RID158/NID26 UID1450; CSV493/917/1333 | Q0.6/I1.1/I1.2 | 원시 INV 단독 선언·옛 주소 주석 |
| E04 | IW0→Inputs DB13 | 0397 Part22/W23/24; 0627 RID3; 0629 RID5/BIRID4; 0628 RID4; 0655 RID247; 0657 RID279/280 | Word0에 포함된 bit9/10의 전달 | 현재 실행·다른 쓰기 |
| E05 | 입력 호출 경계 | 0030 CRef21/23/25/28, Contact37/W44; 0688 RID135, 0692 RID140, 0694 RID136 | ENO 및 NOT Simulation(1) | 현재 CPU·최종 DB값 |
| E06 | HMI 설정 3행 | sources/hmi_plc_tags.csv, R/equipment-hmi.csv | DB11X12.0/12.1, DB2X0.6 | 화면 이벤트·통신 |
| E07 | VS01 HMI 호출 | 0362 CRef23/CodeBlock22, W24/28/30/32/34/36/42/46 | 실제 피연산자 8개 미해석 | NID·선언·인스턴스 |
| E08 | 운전 2초 SD | 0430 Part545/W569/570; 0656 RID28/NID16 UID559; 0658 RID66 | Tag59/T60, S5T2S | 현행 타이머·스캔 |
| E09 | FAULT/INV Set | 0430 Part551/595, W574/601; 0657 RID68/218 | !run과 inv의 분기 구분 | 실제 극성·전체 알람 완전성 |
| E10 | 알람 Reset | 0430 Part556/603, W579/27; 0657 RID13/68/218 | ON&RESET&own | 원인 복구·재기동 별도 |
| E11 | 요청 Reset | 0248 OR24/Part377, W26/390; 0604 RID71/207/72 | FAULT OR INV | 동시 쓰기·현행 순서 |
| E12 | 최종 Q 소유 | 0248 Part381/W400/393; 0602 RID73 | ON&Flag→StartVS01 | 전기 전달·실물 운전 |
| E13 | 자동 단계 | 0164 Part456, 0165 Part786, 0166 Part975; 0577 RID31; 0578 RID30/81/37 | 17 Reset/18 Set/21 또는 Emergency Reset | 단위·레시피·다른 쓰기 |
| E14 | 브레이크 요청 메모리 | 0249 Part425/431, W464/469; 0602 RID74/NID14 | M11.0 Set/Reset | OFF 현재 값·동시 조건 |
| E15 | 브레이크 별도 SD·Q | 0249 Part439/444, W472/473/476; 0606 RID76; 0602 RID77/78 | Tag117/T69/2S, Q49.5 | 현장 브레이크·끝점 누락 |
| E16 | OFF·폐지 주석 경계 | 0602 RID33; 0249 제목; CSV 문서461 | M0.1, off, it's no longer there | 현행 활성·철거 확정 금지 |
| E17 | MC04 소비 경계 | 0247 Contact26/380, W25/ORef27; 0604 RID224 | VS01 run을 읽는 소비자 | MC04 전체 재조사 범위 아님 |
| E18 | HOUR Move1 | 0313 Part1432/1442/1445, W1470/1471/1472; 0615 RID160/162, 0616 RID7/8/12 | MIN Add/HOUR Move 구분 | 실제 주기·의도 |
| E19 | HOUR 초기화 | 0337 Part2925/2884, W2926/2911/2912; 0613 RID284, 0615 RID162 | Tag48에서 첫 Move0 | 현재 초기화·전원복귀 |
| E20 | 상위 호출 | 0031/0549; 0688 RID58/67/82 | Allarms1/Motors1/time work의 ON 호출 | 현재 CPU 실행·순서 |
| E21 | Q→DI1 끝점 | FG136/PDF137 단자7→FG28/PDF29 XS13~16/QS/QM/28KA1→FG27 DI1 단자12 | 공통 명령·두 분기 허가 직렬 | 실배선·접점 상태 |
| E22 | RUN/ALARM 끝점 | FG27 단자17/19 및20/21→FG117/PDF118 단자12/13 | 공통 I1.1/I1.2 | 개별 모터 정상 증명 아님 |
| E23 | Reset/STO 구분 | FG27/PDF28, FG17/PDF18, FG14/PDF15 | 17KA1 4/12→DI4, 14KA2/6→STO | 상위 안전회로·Flag Reset 전달 |
| E24 | 두 시공 케이블 | construction PDF34/51 row1_20/1_21 | M06 E300/M07 E400, 각 LEN88 | first draft·준공·현행 |

## 7.2 누락 자료와 필요한 판정 근거

| 누락 | 필요한 자료/위치 | 필요한 이유 | 현재 상태 |
| --- | --- | --- | --- |
| G01 | 현행PLC프로젝트·CPU비교·승인변경기록 | 호출·다중쓰기·메모리/타이머·전원복귀 | 현재CPU미수행 |
| G02 | 스크린/M06/M07/27AS1명판·배치·관리관계 | 공통구동/두모터·VS01A표기의실물동일성 | identity_verified:false |
| G03 | 준공전기·각QS/QM/단자·드라이브기능/보호설정기록 | 공통Q/RUN/ALARM정상극성·현행허가·분기보호 | 도면상경로만확인 |
| G04 | Q49.5모듈/끝점·브레이크실물·철거/미사용승인·개정도면 | off/폐지주석/잔존코드의현행의미 | 현장존재·활성미확정 |
| G05 | HMI원본·dde.cfg·화면이벤트·1184의NID/선언·DB11/DB2배치 | 미해석8피연산자·누적알람·요청writer | 설정행/핀만확인 |
| G06 | Tag47/48주기·시간기능명세·현재MIN/HOUR | Move1과초기화의도·실누적 | 누적정상성미확정 |
| G07 | 승인된각모터관찰·최초고장·원인조치·복구기록 | 공통응답과두모터실제정상구분 | repairs_completed=0 |
| G08 | 현행안전회로승인자료·FlagRESET→A7.4전달 | STO상위회로·PLC/드라이브Reset구분 | 부분끝점만대조 |

## 7.3 네 기능 반영 제안과 기존 기록 보존

| 기능 | VS01에 필요한 내용 | 이번 수행 |
| --- | --- | --- |
| 도면·래더 비교 | 0248/0430↔FG27/28/117/136,0249브레이크누락,두모터분기 | 문서근거만작성 |
| 백업·선택 복원 | VS01/P09기존키·미지필드·다른설비·과거/미확정기록보존 | 실제복원시험안함 |
| 기록 전후 비교 | 공통Q/응답/알람과M06/M07각각의관찰분리,시각·단위·판본 | 필드제안만 |
| 보고서/PDF | 공통응답한계·브레이크경계·두타이머·누락/복구미완료표시 | 앱PDF생성/시험안함 |

기존 완료 설비·불일치·확인 대기·과거 설계시험의 집계/상태를 이번 초안으로 바꾸지 않는다. 실운영 기록·세진 데이터는 공개 원본/코드에 복제하지 않는다.

## 7.4 상태와 미실행 검사

| 구분 | 상태 | 근거·범위 |
| --- | --- | --- |
| documentation | draft_ready | 이MD의7영역·24근거행 |
| static_review | original_sources_reviewed_partial | 핵심XML/선언/핀·실제PDF대조,독립Codex재확인전 |
| ui_records | not_run | 앱화면/저장/복원/동시성/PDF검증미수행 |
| publication | not_published_by_dot | 코드·버전·배포담당아님 |
| tia_compile / live_cpu | not_performed | TIA·현재CPU접속/쓰기안함 |
| field_recovery | not_performed | 실측·조치·복구안함 |
| simulator | permanently_stopped | 작성/수정/생성/실행/행동시험0 |

수행한 것은 공개Git읽기,문서/CSV/JSON/XML정적읽기·노드/선언/핀추출,PDF렌더·시각대조,해시확인,이MD작성이다. 정적 보조 스크립트는 XML 연결을 출력하며 PLC 상태전이·타이머 실행·출력 시뮬레이션을 구현하지 않는다. 저장소 생성기/npm/TIA/시뮬레이터 검사를 실행하지 않았다.

## 7.5 Codex 인계 — 핵심 재확인만 좁혀 수행

1. 실제 반영 시 현재 main과 이 고정 커밋의 VS01 원본 차이만 먼저 확인한다. FN06/MC04 전체를 재조사하지 않는다.
2. E08~E12: Tag59/T60/S5T2S·FAULT/INV공유·Reset과0248출력/요청해제를 재확인한다.
3. E14~E16: M11.0/Q49.5/Tag117T69의역할·OFF·Set/Reset비대칭·SD를펄스로오해하지않는지·현장끝점미확보를확인한다.
4. E02/E21~E24: 한인버터/두모터/공통응답의경계와각QS/QM·케이블끝점을 실제PDF에서재확인한다. 현행극성·보호설정·개별모터정상을추정하지않는다.
5. E04~E07: IW0→DB13의bit9/10및호출ENO/NOTSimulation(1)을확인한다. HMI1184실제바인딩은미확정그대로남긴다.
6. E13/E18~E20: 자동17/18/21·HOURMove1·첫Move초기화·호출경계를확인한다. 다른설비값/항목수를복제하지않는다.
7. VS01고유내용으로7영역/검색/기록키/선택복원/비교/PDF를반영·검증하되코드·공통검사·버전·완료대장·배포는사용자/지정Codex만담당한다. dot초안을게시완료로표시하지않는다.

## 다음 대상·범위

이번 승인된 한 대상은 VS01(P09)이다. 이 초안을 이 대화에 첨부한 뒤 다른 설비로 자동 확대하지 않는다. 처음 승인한 순서에서 다음 후보는 PV01이지만 이번 문서에서 조사·작성하지 않았다. 사용자 검토 중 새 근거/질문이 오면 VS01의 해당 부분만 보강한다. 2차133후보는 제외한다.

## 부록: 고정 원본 지문

SHA-256은 조사 커밋의 파일 바이트 기준이며 현재CPU/실물동일성의증거가아니다.

| 경로 | SHA-256 |
| --- | --- |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 |
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
| all-in-one/registers/equipment-hmi.csv | 2cdce600aa0138cc5025022e57d9d61a948afb237f70c70e2d11e8300e73286a |
| all-in-one/registers/plc-symbols.csv | a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f |
| all-in-one/procedures/VS01.html | 415a2f3f8bae49e34fe3a3cd38738a541919a84eef8b933a72c615634c017830 |
| all-in-one/devices/VS01.html | 05f520cc52537958e04753c21e826c099c0988f1b071e706d9d364ef750245b5 |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b |
| all-in-one/sources/decoded-original/0031-FlgNet.xml | 76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65 |
| all-in-one/sources/decoded-original/0164-FlgNet.xml | 15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491 |
| all-in-one/sources/decoded-original/0165-FlgNet.xml | 4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88 |
| all-in-one/sources/decoded-original/0166-FlgNet.xml | 0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853 |
| all-in-one/sources/decoded-original/0247-FlgNet.xml | 104690938ac2ebe32d668f237255a3e957e0af9930bfc6587b9e6624bedf13a1 |
| all-in-one/sources/decoded-original/0248-FlgNet.xml | 5625b16670c9c66da8d8387851ba511f3f139cca97e0a45d307c1e17bdabf2b7 |
| all-in-one/sources/decoded-original/0249-FlgNet.xml | 795b5d96b7cb6ba8f4a8c0d94276c3cc52195c39fb0f3948607354dfbf041971 |
| all-in-one/sources/decoded-original/0313-FlgNet.xml | 4a9f084345aa94f2e4e16cc1329f8b2baed2c22266b688000809dfbd7af57d8a |
| all-in-one/sources/decoded-original/0337-FlgNet.xml | 403f3a0e9218bbe81fb00cb93fb9f6bd3570af2df157abccd878a3a1f60f2580 |
| all-in-one/sources/decoded-original/0355-FlgNet.xml | 73592d33f8b3a71effeb36f25427c76e931485e7ce31f5c81f144ddae83c4247 |
| all-in-one/sources/decoded-original/0362-FlgNet.xml | e5882d4714fd03d63b3b0226419273caeb8cf835e0b03fdedbea1b12430d1162 |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 |
| all-in-one/sources/decoded-original/0430-FlgNet.xml | d058073f512bcdc1d392d281d9df7932583a15ae90bfd81d903b940e9e2d6599 |
| all-in-one/sources/decoded-original/0549-FlgNet.xml | 49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1 |
| all-in-one/sources/decoded-original/0067-IdentXmlPart.xml | 0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628 |
| all-in-one/sources/decoded-original/0575-IdentXmlPart.xml | 40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06 |
| all-in-one/sources/decoded-original/0577-IdentXmlPart.xml | 511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47 |
| all-in-one/sources/decoded-original/0578-IdentXmlPart.xml | 0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b |
| all-in-one/sources/decoded-original/0602-IdentXmlPart.xml | 46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf |
| all-in-one/sources/decoded-original/0604-IdentXmlPart.xml | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af |
| all-in-one/sources/decoded-original/0606-IdentXmlPart.xml | 73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740 |
| all-in-one/sources/decoded-original/0613-IdentXmlPart.xml | 09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb |
| all-in-one/sources/decoded-original/0615-IdentXmlPart.xml | 80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a |
| all-in-one/sources/decoded-original/0616-IdentXmlPart.xml | 650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d |
| all-in-one/sources/decoded-original/0621-IdentXmlPart.xml | a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee |
| all-in-one/sources/decoded-original/0623-IdentXmlPart.xml | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 |
| all-in-one/sources/decoded-original/0624-IdentXmlPart.xml | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a |
| all-in-one/sources/decoded-original/0626-IdentXmlPart.xml | a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| all-in-one/sources/decoded-original/0655-IdentXmlPart.xml | 38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb |
| all-in-one/sources/decoded-original/0656-IdentXmlPart.xml | 0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592 |
| all-in-one/sources/decoded-original/0657-IdentXmlPart.xml | 0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b |
| all-in-one/sources/decoded-original/0658-IdentXmlPart.xml | 998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831 |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | 757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d |

초안 저장: 2026-10-11T06:03:21.368867+00:00 (UTC).
