# CR01 운전 제어반 — 고정 원본 7영역 조사 초안

문서 범위 완료·누락 포함. 실물 동일성, 현재 CPU, 현장 복구 및 실제 게시 완료를 뜻하지 않는다.

## 핵심 확인·상충·누락·공유 근거

- 직접 확인: P&ID 실제 PDF1에 OPERATING CAB, CR-01, AC440V-60Hz/AC110V-60Hz가 표시된다. 운전 캐비닛이라는 문서 식별은 확보했다.
- 관련 공통 근거: OEM FG9/10 보조전원, FG16 전원 표시, FG17 알람 조작, FG135 입력을 직접 렌더 대조했다. 이는 공통 전기 계통이며 모든 PLC·알람을 CR01 고유 소유로 전환하는 근거가 아니다.
- 소유 혼동 주의: OEM FG235/PDF238의 JB01 CONTROL CABINET은 FN04 운전·알람·속도·피드백 단자다. CR01=JB01이라고 병합하지 않는다. FG237/PDF240 CONTROL BOARD 외형도 CR01 표기가 없어 대응 후보에 그친다.
- 미확보: CR01 전용 XML 선언·HMI·래더·고유 입출력, CR01↔QG/JB01/운전반 실물 결속, 현행 회로·보호설정·정상극성·복구 증거. 검색 불발은 실물 부재가 아니다.
- 공유 원본 재사용: [BF01](BF01-DOTS-DRAFT.md), [LD01](LD01-DOTS-DRAFT.md)의 0397/0627/0628/0629 공통 Word 전달 구조를 색인으로 활용했다. 이번에는 CR01 연관 110V 공통 입력인 IW18→DB13.DBW18 분기를 직접 확인했다. BF01/LD01 고유 로직·알람은 복제하지 않는다. 0457 110V 공통 알람은 별도 직접 확인했다.
- 기존 CR01 baseline의 passive 공정본체 점검 문구와 시뮬레이션 설계 항목은 CR01 제어반 고유 검증이 아니다. 원문은 수정하지 않고, 이 초안은 전원·표시·제어 경계로 관찰 항목을 제한한다. 시뮬레이터 작성·수정·생성·실행·행동 시험은 하지 않았다.

## 1. 설비·자료 기준

- catalog_id CR01, 운전 제어반, kind passive, group 공정 본체, parent_id null, phase2. 고정 INVENTORY catalog33(0-based), equipment index55. 부모나 하위를 같이 완료로 세지 않는다.
- 고정 원본: `gme-research/source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 이후 로컬 기능·실제 게시 상태는 검증하지 않았다. 로컬2차133 통합 제외 유지; 자체 조사 초안만 작성.
- P&ID: `all-in-one/sources/PID_1684n002I.pdf`, PDF1, 도면1684n002, Apex I, 작성06/04/2011, 개정 I 15/01/2013 “REMOVED MC-05, CHANGED POWER OF FN-02”. 하단의 별도 OPERATING CAB 상자 안 CR-01을 시각 확인. 이는 현행 전압 측정이나 승인 시공 실물 검증이 아니다.
- OEM: `all-in-one/sources/Electrical_Rev2.pdf`. 실제 footer별 FG/PDF를 아래에서 분리한다. 앞쪽 FG9는PDF10, 뒤쪽 FG235는PDF238이므로 PDF-1 일괄 환산 금지.
- 시공도 `Electrical_Can_Decoating_20241118.pdf` 64페이지 텍스트에서 CR01 및 RUNNING CABINET 명시적 표기는 확보하지 못했다. 이미지 전체 의미검토를 했다는 뜻이 아니며, 해당 부재를 확정하지 않는다.
- root AGENTS, 저장소 스킬, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY 및 배치 범위·중복 검토를 읽었다. 요청 모델·추론 설정 런타임 증명은 미확인. 로컬 TIA 추가접근, 새 Work/Codex, 사용자 컴퓨터 접근 및 재위임 없음.

## 2. I/O·HMI

### 2.1 CR01 고유 검색

`all-in-one/sources/decoded-original/*.xml` 695개를 대소문자 무시 `(?<![A-Za-z0-9])CR[ _-]?0?1(?![0-9])`로 검색한 일치 파일0. 같은 식으로 `live_index.json`, `hmi_plc_tags.csv`, `hmi-windows.csv` 각각0. 695는 문자열 검색 수이며 의미검토695 또는 전체 백업 분석 수가 아니다. 원본 선택23파일 해시 확인도 의미검토23과 다르다.

CR01 직접 HMI 화면명·태그·버튼 이벤트·설정 쓰기·주소는 근거 미확보. 공통 전원 램프를 HMI 태그로 바꾸지 않는다. 바이너리·다른 별칭·현행 CPU의 부재를 주장하지 않는다.

### 2.2 공통 보조전원 연관 채널: CR01 독점 소유 아님

|구분|직접 선언·위치|해석·경계|
|---|---|---|
|도면 입력 E19.5|FG16/PDF17의9QF2 보조접점 → FG135/PDF136 CPU515 MOD12 단자36|PRESENCE VOLTAGE110Vac AUXILIARY. 실물 현재 정상극성 미확인|
|원시 Word|0627 SimpleAccess RID25/UID81 NID1, Tag_276, Word, AO144, SAD Input SAM=None|%IW18 프로세스이미지 Word. PIW 직접주변 접근이라고 쓰지 않음|
|내부 Word 쓰기|0629 GlobalAccess RID26/UID82 NID1 AK=Write, Word AO144, BAD4;0628 Inputs RID4 TOD13|DB13.DBW18, 내부 저장. I19.5 범위 포함과 같은 바이트/비트 위치의 DB13.DBX19.5를 연결|
|전압존재 처리비트|0657 Global RID248, NID50 UID24, Bool AO157, Inputs.Presenza_110V;0655 Inputs RID247 TOD13|DB13.DBX19.5. 원시 전압 자체 측정값이나 현장110V 확인과 다름|
|공통 전압고장|0657 Global RID252, NID50 UID39(read),40/48(write), Bool AO92;0655 Allarm RID10 TOD3|DB3.DBX11.4 Allarm.110V_Fault. CR01 이름의 고유 알람이 아님|
|공통 리셋|0657 Global RID13, NID50 UID38, Bool AO48;0655 Flag RID12 TOD2|DB2.DBX6.0 Flag.RESET_ALLARM. 버튼→이비트 전체 결속은 미확정|

공통 선언 0635에는 RID354/NID18 UID46 AK=Write로 동일 Inputs.Presenza_110V AO157 별도 쓰기 참조가 있다. network-map은 해당 블록을 simulation으로 색인한다. 이는 추가 쓰기 후보 존재를 보존하기 위한 읽기 전용 선언 확인이며, 그 블록 실행·현행 호출·시험을 수행하거나 정상 운전 조건으로 채택하지 않았다.

## 3. 제어 구조

### 3.1 CR01 본체 제어 경계

CR01 전용 요청→허가→출력→응답이나 자동/수동 전이, 타이머·PID·환산은 근거 미확보이다. 운전반이 제어 기능을 담을 수 있다는 사실만으로 전체 공정 PLC를 CR01 소유로 만들지 않는다. 전기 보조전원 및 공통 알람 연결까지만 조사한다.

### 3.2 공통 Word 입력 전달 직접 확인

`0397-FlgNet.xml`(색인 LAD1070/NID1)의 Move Part78, DisableENO=true, Cardinality1:

- W21 Powerrail→P78.en
- W88 ORef81/RID25→P78.in, 선언0627의 IW18 Word
- W90 P78.out1→ORef82/RID26, 선언0629의 Inputs DB13.DBW18 Write
- W89 P78.eno→P79.en 연결은 남아 있다. DisableENO와 eno 존재를 구별하며 ENO 전파만으로 현재 실행·후속 최종값을 확정하지 않는다.

이것은 Word 복사이며 직접 Bool 코일 쓰기가 아니다. E19.5→DB13.DBX19.5는 해당 Word 범위와 선언을 대조한 해석이다. 호출 순서·다른 쓰기·현행 프로그램은 추가 확인 필요. 해당 분기 CRef 호출 핀은 없으며 ORef/PCon을 사용한다.

## 4. 전기 전달 경로

모든 회로는 OEM 문서상 연관 공통 경로이다. CR01 독점 하드웨어 소유 및 현장 설치 모델을 확정하지 않는다. 아래 전압·정격은 도면 원문이며 현행 보호설정 권고가 아니다.

|FG / 실제PDF / footer|양 끝점 및 중간 회로|구별·미확정|
|---|---|---|
|FG9/PDF10,27.05.2024, 개정란 공란|6.2L1/L2(8/9)→9QF1→9T1 440/110V 3600VA→9QF2→110Vac9.8 및0Vac9.9. 별도14KA4/14KA8 직렬접점→110Vac9.7(21/0)|직접전원과 비상조건 아래전원을 혼동 금지. 그림 상단440V와 추출텍스트400V 차이는 실제렌더440V 채택|
|FG9/PDF10 동일|9QF3→X1:413 110Vac9.10 VALVES(152/0),9QF4→X1:414 110Vac9.11 FAN+PLC(60/4),X1:415 0Vac9.9; JB2쪽9QF5→X1:416,9QF6→X1:417,X1:418 0Vac9.9(181/0)|JB1/JB2 공급은 연결된 공통 끝점이며 CR01=JB1/JB2 아님. 후단 모든장치 재조사하지 않음|
|FG10/PDF11,27.05.2024, 개정란 공란|UPS CLIENT 3상440V60Hz XL:1/2/3→10QF1→10GD1 20A AC/DC→10QF2→+24Vdc10.7 INPUTS PLC; 음극→-0Vdc10.6|UPS 고객경계와 PLC입력전원 경계 분리|
|FG10/PDF11 동일|10QF3→+24Vdc10.8 DIRECT OUTPUTS;14KA3/14KA7 직렬→+24Vdc10.9 OUTPUTS UNDER EMERGENCY;10QF4→+24Vdc10.10 CPU|10.7/10.8/10.9/10.10 네전원을 하나로 합치지 않음|
|FG16/PDF17,27.05.2024, 개정란 공란|110Vac9.8→X20:2010→16HL1(WHITE) X1/X2→X20:2011→0Vac9.9; CPU+24Vdc10.10→X20:2012→16HL2(WHITE)→-0Vdc10.6|전원존재 표시이며 공정 운전완료 램프 아님. 두램프 전원독립|
|FG16/PDF17→FG135/PDF136,27.05.2024, 각개정란공란|+24Vdc10.7→9QF2 보조접점(9/1 참조)→E19.5(135/5)→CPU515 MOD12 단자36|9QF2 상태접점 입력을 정밀110V 계측으로 설명하지 않음|
|FG17/PDF18, Rev2 17.03.2025, 기본27.05.2024|+24Vdc10.7→X20:2013→17SB1(13/14,YELLOW)→X20:2014→E19.6;17SB2(13/14,BLUE)→X20:2015→E19.7; FG135 단자37/38|SILENTLY ALARMS와RESET ALARMS FAULT 기능분리. 자동재기동이나현장복구승인아님|
|FG17/PDF18 동일|A7.6→X1:41(퓨즈)→17HL2→X1:43→0V;A7.7→X1:42(퓨즈)→17HL1→동일귀로;A7.4/7.5→17KA1/2 A1, A2→0V|출력 상대참조143/1만확보. FG143 실물·출력선언 전체는 범위외. 하단접점표를부하핀으로오독하지 않음|
|FG235/PDF238,27.05.2024, 개정란공란|QG-X5:7 E28.2 RUNNING FN04, :8 E28.3 ALARM FN04, :10/11 ±PAW336 속도, :12/13 ±PEW394 피드백, :17 110Vac9.11, :18 0Vac9.9|JB01 CONTROL CABINET TERMINAL BOARD는FN04 관련별도반. CR01 고유실물대응미확정|
|FG237/PDF240,27.05.2024, 개정란공란|CONTROL BOARD,6000폭/10DOORS 외형 및 SIDE VIEW|CR01 태그없음. P&ID 소형스케치와크기를같다고단정하지 않음|

참고 렌더 FG234/PDF237 PLC BOX JB2 TERMINAL BOARD, FG240/PDF243 CUT OUT DOORS도 별도 타이틀을 확인했다. 처음 선택한 PDF 번호가 목표 FG와 같지 않음을 발견하여 FG235/PDF238 및 FG237/PDF240으로 바로잡았다. 해당 주변 판넬 도면을 CR01 소유로 병합하지 않았다.

## 5. 알람·복구

`0457-FlgNet.xml` 색인 LAD1823, allarms1, index43, NID50, title presence110v. `0657` Global 선언과 `0655` DB번호를 독립 대조했다.

|기능|Part/Wire/ORef/선언|정적 해석|
|---|---|---|
|Set|P23 Contact operand Negated, W22←ORef24/RID248;W41 P23.out→P27 SCoil.in;W47 ORef48/RID252→P27.operand|NOT Inputs.Presenza_110V가 공통110V_Fault Set 분기에 연결|
|Reset|P35 Contact W42←ORef38/RID13;W43→P36 Contact W44←ORef39/RID252;W45→P37 RCoil;W46 ORef40/RID252|RESET_ALLARM AND 110V_Fault가 Reset 분기에 연결|
|급전|W21 Powerrail→P23.in 및P35.in|두갈래의 Set/Reset. 이네트워크에는타이머없음|

단순 조합 Fault=NOT Presence로 축약하지 않는다. Set/Reset이 모두 있는 기억 상태이고, 전압 미복귀 중 Reset이 동시에 참일 때 스캔 최종우선·다른쓰기·호출순서는 현재검증하지 않았다. Reset 분기에 Presence 복귀 접점이 그려져 있다고 발명하지 않는다. 공통 리셋 비트가 현장17SB2 및 HMI 이벤트로 작성되는 전체경로는 미확정. 이 알람이 공정 전체에 끼치는 정지/재요청 영향은 범위 밖이며 추가 자료 없이 CR01 전용 안전기능으로 배정하지 않는다.

운영자의 리셋 입력, 표시 소거, 전원 복귀, 공정 재기동, 안전복구는 각각 다른 증거가 필요하다. 보조전원 재투입·보호값 조정·활선 측정·인터록 우회는 이 초안의 작업지시가 아니다.

## 6. 증상별 관찰·원인 분리

현장 관찰은 수행하지 않았다. 승인된 담당자가 제공할 관찰기록의 항목만 정의한다. 시각/시간대·관찰자·설비명판·현재프로젝트근거·위치·값/단위·비교원본·조치와복구증거를 따로 보관한다.

|증상|관찰/비교근거|단정금지·필요증거|
|---|---|---|
|화면/운전반 전체꺼짐|16HL1 110V와16HL2 CPU24V의각표시, UPS고객공급 및10QF4 경로의기존점검기록|화면꺼짐만으로PLC고장·CR01전체전원상실단정금지|
|110V알람남음|9QF2상태접점/E19.5/DB13.DBX19.5/DB3.DBX11.4의동시관찰시각비교|접점·Word전달·기억알람을구별, 원시전압계측으로대체하지 않음|
|리셋눌러도알람남음|17SB2→E19.7, Flag.RESET_ALLARM, 0457 S/R분기 각각기록|Reset요청과복구완료혼동금지, 재발원인/다른쓰기확인전해결표시금지|
|램프만꺼짐|16HL1/2 전원표시와17HL1/2 공통알람표시를태그로구분|램프회로와공정상태서로대신증명불가|
|운전반명칭불일치|P&ID CR-01, QG 명판, JB01 FN04반 명판·배치도·단자대사진대조|유사명칭/같은전원만으로캐비닛병합금지|

## 7. 완료·누락·검증

|영역|문서 적용 판정|
|---|---|
|설비·자료기준|직접P&ID표기확보, 실물동일성보류|
|I/O·HMI|CR01고유근거미확보; 공통입력Word/Bool분리확보; HMI미결속|
|제어구조|본체고유제어미확보; 공통Word분기만직접검토|
|전기전달|보조전원·표시·공통입력과캐비닛소유경계확보;실물끝점미확인|
|알람·복구|공통110V S/R직접검토, CR01고유알람미확보;현장복구미수행|
|증상관찰|기록항목작성,현장값/정비조치없음|
|완료기준|문서complete_with_gaps,통합/화면/게시/TIA/CPU/현장별도미수행|

네 기능: 도면·래더 비교는 문서 원본 연결 후보만 작성. 백업/선택복원, 전후기록비교, 보고서/PDF 기능 구현·사용자UI·기록저장·재열기 검증은 미수행. 원본PDF 렌더 검토를 제품 보고서PDF 기능 검증과 혼동하지 않는다. BC01 동등 표준화완료·게시완료·현장완료로 집계하지 않는다.

추가 필요자료:
1. CR01/QG/JB01 대응을 확정하는 승인 배치도·명판·반내부 단자대사진 및 도면변경대장.
2. 현행 승인 회로와 현재 PLC 프로젝트의 I/O교차참조·호출순서·HMI 이벤트 및 전압/알람 관찰 기록.
3. 전문 담당자의 전원공급·보호기기 상태·실제 복구기록. 원본 도면의정격과현재설정은별개.

새 자료가 오기 전 동일실물보류를 반복검색하지 않는다. 다음 단계는 부모의 초안독립검토·전달이며, 운영/대장/배포 통합은 이번 조사 범위가 아니다.

### 실제 작업 시각 (UTC)

- 2026-10-11 11:35:27 착수·배치지시/범위 읽기 시작.
- 11:35:34 표준/인벤토리/원본상태 읽기, 이후 고정자료탐색.
- 11:35:57 원본PDF 텍스트선별완료. 11:36:10 P&ID 및 XML695 변형검색결과확인.
- 11:36:20~11:36:59 OEM 실제렌더열람·footer/회로대조; PDF/FG번호보정.
- 11:37:06~11:37:34 공통110V 선언/0457 핀/Word전달 대조.
- 11:38:00 P&ID CR01·개정란 확대렌더확인.
- 11:38:37 선정23파일 SHA256/Gitblob 내용일치, 중지5 해시일치 확인. 이후 초안작성·자체검사시각은 검사JSON 참조.

### 검증 범위와 보존

자체 XML파싱/원본문서해시/PDF렌더만 수행했다. 원본 build/test/generator, 시뮬레이터·PLC·현장·보호값·SEJIN 변경/실행0. 원본 Git clean 대조와 선정파일 고정blob 대조를 수행하며 원본 및 중지5자산을 수정하지 않았다. 독립검토는 부모 대기. 선택파일23 중 중지5는 해시전용이고, 탐색색인과선언·도면 의미검토를분리한다. 검사JSON·검색JSON·파싱원문·렌더PNG는 `../extracts/CR01/`에 보관.

### 전체 선정 원본 SHA256 / 고정 Git blob 목록

아래는 이번 선정23파일 전부다. 표기된 Gitblob 내용과 로컬SHA256이 일치한다. 중지5는 읽기해시만 하며 코드실행이나의미시험을 하지 않았다.

|원본 상대경로|SHA256|고정 Git blob|내용 비교|
|---|---|---|---|
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` | 일치 |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` | 일치 |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` | 일치 |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | 일치 |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` | 일치 |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` | 일치 |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` | 일치 |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | 일치 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | 일치 |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | 일치 |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | 일치 |
| `all-in-one/sources/decoded-original/0457-FlgNet.xml` | `498e0618c56b6a898373d4fa4745e749d0654da17b1f1cd148e9d9617dccb86d` | `dcba3137465522e263742251b0e00159b2be090d` | 일치 |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | 일치 |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | 일치 |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | 일치 |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | 일치 |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | `83b60b9de4541a3ffa6ee0db98205a372b525665` | 일치 |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | `e625f3d8999c7be7d88c50eab0d93107117b58ec` | 일치 |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | 일치 |
| `all-in-one/sources/hmi-windows.csv` | `15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e` | `8401dcfe5ba3e7e244eea0f501bb84a2e387da39` | 일치 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | 일치 |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` | 일치 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | 일치 |