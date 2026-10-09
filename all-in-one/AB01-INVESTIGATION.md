# AB01 온도 알람·버너 연결 독립 조사

작성일: 2026-10-09. 원본 XML의 정적 구조를 확인한 결과다. 실제 CPU 실행, TIA 컴파일, 현장 복구, 현재 운전·보호 설정의 승인을 뜻하지 않는다. 시뮬레이터 작성·수정·실행·행동 시험과 실제 PLC/현장 설정 변경은 수행하지 않았다. 공통 대장·빌더·HTML·원본을 수정하지 않았다.

구조화 원본 근거: [registers/ab01-independent-investigation.json](registers/ab01-independent-investigation.json). 원본8개 네트워크의 Part/Negated/TemplateValue/ORef/Wire와 식별 선언 UID/RID/NID, 선언 범위·자료형·LiteralConstant 원문 및 사용 자료24개 SHA-256을 보존했다. 기존 대장은 탐색·비교에 사용했고, 핵심1979/1986·1856/1858·1866은 원본 XML을 직접 읽어 대조했다. 1979의31개 피연산자와1986의20개 피연산자 모두 원본 UID/RID 선언이 연결되며 각각 C.NID=1/8이다.

## 1979 MAX와 MAXMAX는 다른 알람이다

원본: `sources/decoded-original/0527-FlgNet.xml`, 블록 `allarms 3`, 원본 NID=1. 선언은 `0683` LiteralConstant, `0684` GlobalAccess, `0685` Local InterfaceAccess, `0686` SimpleAccess에 있다. 숫자 UID는 아래 배선 위치 식별용이며 실행 순서가 아니다.

| 구분 | 발생·Set의 정적 배선 | Reset의 정적 배선 |
|---|---|---|
| `Global:Allarm.MAX_TC01_TEMP` | ON Contact286 → Real Gt149(`Manage_TC1_2.PID_Ref_Temp`, `Data.TC01_MAX_ALL`) → SD155 `Tag_99`/`S5T#6S`. 같은 비교 출력과 `Tag_99` Contact288 → Set160 | ON과 자기 MAX Contact290 → Int Sub165(`TC01_MAX_ALL`,5) → `Local[allarms 3].app00`. Sub.eno → Real Lt169(선택온도,app00) → Reset173. 같은 Lt.out이 `Flag.STOP_HORN` Set175에도 연결된다. `RESET_ALLARM` 접점은 이 분기에 없다. |
| `Global:Allarm.MAX_MAX_TC01_TEMP` | ON → Int Add179(`TC01_MAX_ALL`,20) → `Local[allarms 3].max_max_tc1`. ON으로 허가된 Real 비교 3개를 OR185: 선택온도 > max_max_tc1 또는 >1250.0 또는 <−60.0 → SD198 `Tag_100`/`S5T#6S`. 같은 OR 출력과 Tag_100 Contact292 → Set203 | ON → `Flag.RESET_ALLARM` Contact294 → 자기 MAXMAX Contact296 → Reset208. 원인해소·온도정상 접점은 이 Reset 분기에 없다. |

MAX Set의 핵심은 Wire241/242의 Gt 입력, Wire243 비교 출력 분기, Wire244의 시간 피연산자, Wire245/246의 타이머 쓰기/읽기, Wire289→Set160, Wire248→ORef215/RID11이다. MAX Reset은 Wire250 자기래치 → Wire291 Sub.en, Wire252/253 입력 → Wire254 Local app00 쓰기, **Wire255 Sub.eno→Lt.pre**, Wire256/257 비교 입력 → Wire258 두 코일 분기, Wire259/260의 MAX Reset/STOP_HORN Set이다.

MAXMAX는 Wire262/263 Add 입력과 Wire264 Local max_max_tc1 출력이다. **Wire287이 Add.en과 세 비교의 pre에 각각 분기되며 Add.eno를 비교 pre에 직렬로 연결하지 않는다.** Wire265~273은 세 비교와 OR185, Wire274는 SD와 타이머 접점으로 분기, Wire275 시간, Wire276/277 타이머 쓰기/읽기, Wire293→Set203, Wire279→ORef236/RID23이다. Reset은 Wire281→RESET_ALLARM, Wire295→자기래치, Wire282→자기래치 피연산자, Wire297→Reset208, Wire284→ORef239/RID23이다. 해당 네트워크의 Contact에는 Negated가 없다.

`PID_Ref_Temp`는 Global Real, `TC01_MAX_ALL`은 Global Int, `app00`과 `max_max_tc1`은 해당 블록 Local Int다. Real 비교와 Int 산술의 원본 형식을 보존하며 현재 컴파일 결과·ENO·범위·오버플로·스캔에서 쓰인 최종값을 이 정적 자료로 확정하지 않는다. 과거 도면850°C와 위 피연산자·상수는 서로 대체하지 않는다.

## 1986 TC01/TC02 비교 알람

원본: `sources/decoded-original/0534-FlgNet.xml`, 블록 `allarms 3`, 원본 NID=8.

1. ON Contact832 → **반전** `TC01-TC02control disable` Contact834. Negated PinName=operand, Wire802/ORef782/RID73, `0686-IdentXmlPart.xml` C.NID=8/UID782를 직접 대조했다.
2. Int Gt745(`Data.Temp_TC01`,400) 또는 Int Gt748(`Data.Temp_TC02`,400)를 OR744로 합친다. 두 온도가 모두400 초과인 AND 조건이 아니다.
3. **Wire809가 Sub754.en과 Lt761/Gt764.pre에 함께 분기한다.** Int Sub754가 `Temp_TC01−Temp_TC02`를 `Local[allarms 3].app02`로 쓰며 Wire812/ORef789/RID77은 `0685` 선언 C.NID=8/UID789/AK=Write다. Sub.eno에서 비교 pre로 이어지는 직렬선은 없다.
4. app02 < −100 또는 app02 >100를 OR760으로 합친다. 정확히±100인 값은 이 두 비교의 범위 밖 조건에 포함되지 않는다. Wire819는 SD770.in과 Tag_108 Contact836.in으로 분기하며 `S5T#1M` 시간 피연산자는 Wire820/ORef794/RID46이다. Tag_108 쓰기/읽기는 Wire821/822이고 Wire837→Set775, Wire824→ORef797/RID81로 `Allarm.TC01_TC02_COMP_FAULT`를 Set한다.
5. Reset780은 ON → RESET_ALLARM Contact838 → 자기래치 Contact840이다. Wire833에서 Set 측 반전 disable 경로와 Reset 측이 분기되므로 Reset은 disable,400 조건,±100 조건,타이머 경로를 거치지 않는다. Wire827/839/828/841/830을 대조했다.

차온·400·±100의 현재 물리 단위, 환산 계수, 비활성 비트의 현재값·쓰기 주체, 산술/실행 순서는 미확정이다. disable 신호를 변경하거나 보호값을 권고하지 않는다.

## 시간은 원본 선언과 분리해 기록한다

| 네트워크·SD | value 배선 | 원본 LiteralConstant 선언 | XML CB 원문 | 해석 가능한 명목 시간 |
|---|---|---|---|---|
| 1979 Part155/Tag_99 | Wire244/ORef212/RID8 | 0683, C.NID1/UID212 | T=S5Time, SV=`S5T_x0023_6S`, V=1536 | `S5T#6S`,6초 |
| 1979 Part198/Tag_100 | Wire275/ORef233/RID8 | 0683, C.NID1/UID233 | T=S5Time, SV=`S5T_x0023_6S`, V=1536 | `S5T#6S`,6초 |
| 1986 Part770/Tag_108 | Wire820/ORef794/RID46 | 0683, C.NID8/UID794 | T=S5Time, SV=`S5T_x0023_1M`, V=5632 | `S5T#1M`,1분 |

두6초와1분은 각각의 원본 SD/value 피연산자다. 명목 시간은 현재 CPU가 그 시간 동안 실제로 실행됐다는 관찰이 아니다. XML 인코딩 값 V를 독립적으로 새 운전 설정값으로 해석하지 않는다. 다른 장치의 `S5T#150S`와 `S5T#150mS`를 이 조사와 섞거나 단위를 통일하지 않는다.

## 버너 정지·요청 해제·최종 출력은 별도 단계다

- **1856** `0173-FlgNet.xml`: ON Contact160 → NOT MAX_MAX_TC09 Contact162 → NOT MAX_MAX_TC01_TEMP Contact164 → `Temperature Interlock OK` ordinary Coil150. TC01 피연산자는 MAX가 아닌 MAXMAX다. Wire155/161/156/163/157/165/159을 대조했다.
- **1858** `0175-FlgNet.xml`: ON Contact273 후 MAXMAX_TC01 Contact293(operand Wire261/ORef243/RID25→Wire294 OR219.in6), TC01_TC02_COMP_FAULT Contact297(Wire263/ORef245/RID40→Wire298 OR219.in8), EmergencyStopTC1_2 Contact22(Wire21/ORef23/RID245→Wire24 OR219.in12)이 연결된다. OR219 → ON Contact305 → OR213.in5 → **Flag.Start_Burner Reset232**이며 끝단 Wire272/ORef250/RID19이다. 정확한 `MAX_TC01_TEMP` 이름은 이 네트워크에 없다.
- **1866** `0182-FlgNet.xml`: Flag.Start_Burner Contact634 AND NOT Lock Burner Contact636 AND Inputs.FN03 Run Contact642 → `Enable start burner(1)` Coil607. 같은 조건에서 `Enable start burner` Contact644를 더 거쳐 `Rem. Start/Stop Burner` Coil611이다. Wire621/635/622/637/627/643/628/629/645/631과 원본 선언을 대조했다. `0582` Memory AO384=M48.0(Enable1), Memory AO386=M48.2(Enable), Output AO53=Q6.5(원격 출력)는 서로 다른 신호다. OFF 접점이 있는 FN03 요청Set 분기는 별도다.
- **1868** `0184-FlgNet.xml`은 세정 상태·Open/Close MV03 요청·Enable·내부 Start Burner를 취급하는 GME 상태 순서다. 이 원본을 기록하되010-390 전용 제어기의 내부 퍼지/점화/화염/가스밸브 보호 순서를 복원한 것으로 취급하지 않는다.

원인 해소 → 알람 래치 해제 → 새 운전 요청 → 두 Enable → 원격 출력 → 전용 제어기 응답 → 실제 화염/연소 상태를 각각 확인해야 한다. Set/Reset 동시 성립의 실제 우선순위, OB/인터럽트 순서, Retain·초기화·외부쓰기, 원시 응답과 Inputs 전달, 전원과 실제 회로는 현재 확인 전이다. 래치Reset이나 요청Reset만으로 안전복구·자동재기동·실제버너정지를 확정하지 않는다.

## 온도 입력·선택 SCL의 근거 경계

1739/1740 원본 `0489/0490-FlgNet.xml`은 Signal linearization 호출을 통해 TC01/TC02와 계수·영점, `Data.Temp_TC01/02`, 각 OFR을 연결한다. 기존 sensor-measurement 대장은 IW272/IW274·OEM FG77/PDF78와 원시 Inputs 복사, 백업의 기존 simulation1092의 다른쓰기를 구분한다. 이번 조사에서는 호출 XML/선언을 읽었고 물리 센서·도면을 새로 시각검증하거나 기존 simulation을 실행하지 않았다.

`Manage_TC1_2.PID_Ref_Temp` 선택은 `sources/live_index.json` segment `_7ev`, i=1719의 SCL 검색색인 문자다. regulation-manual.json의 indexed_texts1719와 문자 그대로 일치했다. 두 Enable/각 OFR에 따라 평균·단일값을 선택하며 둘다 비활성일 때 EmergencyStop true, 뒤에서 `Allarm.EmergencyStopTC1_2`에 대입하는 문자가 있다. 그러나 이 항목의 원형 SCL/컴파일 instruction listing·UID/RID/NID 선언은 이번 원본 LAD에서 확보하지 못했다. process-measurement의 정확한Global LAD쓰기 미확정 상태와 별도 문자근거를 유지한다.

추가 확인 후보: **TC02만 선택하는 색인 분기에서도 `if Allarm.TC01_OFR then EnableTC01 := false`가 표시된다.** 이를 TC02_OFR/EnableTC02로 조용히 정정하지 않는다. 두 Enable에서 동시OFR 처리, 선택값이 대입되지 않는 분기, EmergencyStop/Enable 변경의 실제 반영 순서도 현재 SCL·컴파일·CPU 자료를 확보할 확인 항목이다. 검색색인만으로 현재 PLC 오류나 수정 필요성을 확정하지 않는다.

## body-source-details.py 평가·통합 제안

원본과 모순되는 것으로 확정한 AB01 문장은 없다. 다음은 문서 보강 제안이며 공통 파일은 수정하지 않았다.

| 위치 | 확인 결과 | 제안 |
|---|---|---|
| 33행 AB01 networks |1739/1740 환산과 선택1719를 본문에서 언급하지만 선택 목록에 없으며1856/1858 정지 연결도 빠져 있다.| 원본LAD와 문자색인을 구분해 관련 참조를 보강한다. 본체 전용LAD로 배정하지 않는다. |
| 37행 AB01-D01 비교근거 |1979 온도알람/1986 두온도비교라는 큰 설명은 맞지만 MAX/MAXMAX·Reset 차이·disable 반전·>400 OR·±100·시간이 생략됐다.| 별도 정적근거 표와 원인해소/래치/요청/출력/물리응답 구분을 링크한다. |
| 42행 AB01-D02 비교근거 |1866 기동허가,1868 세정/기동요청은 범위 설명으로 가능하나 여러 요청/허가/출력/상태를 압축한다.|1858 요청Reset→1866 Enable1/Enable/출력과1868 내부 상태를 명시하고010-390 경계를 유지한다. |
| 선택SCL1719 |TC02-only 분기의 TC01_OFR/EnableTC01 원문은 대장과 일치한다.| 원본current SCL/compiled listing을 확보할 확인항목으로 표시한다. 코드나 보호조건을 수정하지 않는다. |

Global/Local의 같은 이름은 합치지 않았다. 특히 app00/max_max_tc1/app02는 `allarms 3` Local이며 Global PID_Ref_Temp·Temp_TC01/02와 별도다. 기존 불일치·확인 완료 상태를 변경하지 않았다.

## 필요한 다음 증거

현재 TIA 프로젝트/CPU 비교본과 OB·인터럽트 호출/순서, 원형SCL1719와 컴파일listing, 현재 DB/HMI 매핑·Retain·초기화/외부쓰기, 온도단위·계수·설정값, disable 및 Enable/OFR 상태, 센서 취출부·교정·출력배선, 전용010-390 제작사 내부안전 자료를 확보한다. 현장 확인은 승인된 절차에서 알람·요청·두Enable·출력·물리응답을 같은시각에 수집하는 별도 업무다. 이 조사 결과만으로 현장 명령이나 설정 변경을 시행하지 않는다.

최종 저장·재열람 정적 검사: 사용자료24개 중 원본/기존대장23개 해시 유지, 원본 Part 145개·Wire 310개·ORef 210개·선언 C 210개 일치, SD 시간3개 원문 유지 확인. body-source-details.py는 조사 후 부모 통합 진행 중 해시가 변경되어 위 제안·행번호는 조사 시점의 스냅샷이다. 두 해시를 JSON에 함께 보존했으며 이 조사 에이전트는 공통파일을 수정하지 않았다. 행동 시험/현재 CPU/현장 검증은 미실행·미확정이다.
