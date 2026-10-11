# Startup Word 0쓰기와 기존 10초안의 주소 중첩 보강 검토

- 작성: 2026-10-11 UTC. 읽기 전용 기준: `gme-research/source-mv06/all-in-one/sources/decoded-original/`.
- 대상: 이미 작성된 FN05·SC01·PV03·MV02·MV05·ER01·CH01·VR01·VR02·VR03 초안의 DB2 요청/기억·DB3 알람 주소표. 신규 설비 조사나 전체 Writer 재조사가 아니다.
- 이 문서에서 `Word 0쓰기`는 **Word 값에 INT#0을 공급하는 쓰기**를 뜻한다. 시작주소 DBW0 한 워드만을 뜻하지 않는다.
- 결과 파일만 `extracts/startup-boundary-review/`에 작성했다. 기존 초안과 원본·공통코드·버전·대장·운영기록·배포·PLC/현장/보호값·SEJIN은 변경하지 않았다. 시뮬레이터 작성/실행/행동시험, TIA 컴파일, CPU/현장 실행은 하지 않았다.

## 1. 바로 사용할 결론

1. `0147-FlgNet.xml`의 8개 Move는 DB2.DBW0,2,4,6,8,10,12,14에 INT#0을 공급한다. 전체 byte 범위는 **DB2 byte0..15**다.
2. `0148-FlgNet.xml`의 9개 Move는 DB3.DBW0,2,4,6,8,10,12,14,16에 INT#0을 공급한다. 전체 byte 범위는 **DB3 byte0..17**다. 제목 `reset all flag allarms`를 DB3 전체 초기화의 증거로 쓰면 안 된다.
3. 10초안에서 추린 설비 고유 요청/기억·알람 28개 비트 중 **26개가 중첩**한다. 범위 밖 2개는 `Allarm.ER01_run DB3.DBX20.1`, `Allarm.Pot_MV02_OFR DB3.DBX24.7`이다. 공통 제어비트 4개는 별도로 구분했다.
4. FN05·SC01·CH01·VR01·VR02·VR03는 요청과 전용 FAULT가 모두 중첩한다. PV03은 요청·열림/닫힘 기억 및 두 알람, MV02/MV05는 자동·수동 요청과 구동 FAULT가 중첩한다. ER01은 요청만 중첩하며 이는 ER01 초안에 이미 기록되어 있다.
5. `0149`에는 MV02/MV05 Auto의 SCoil, `0150`에는 PV03 MEM_CLOSE의 SCoil이 존재한다. 따라서 0147의 0쓰기만 보고 **startup 후 해당 비트의 최종값은 0**이라고 정리하면 안 된다. 파일/네트워크 색인 순서는 현재 CPU의 호출 시점이나 최종값을 입증하지 않는다.
6. 정확한 허가 경로는 ON 접점과 각 Move의 en/eno 연결이다. 이 제한 검토로 상위 OB 결속, 실제 시작 이벤트, Warm/Cold/Retain 설정, 현재 활성/현재값, 다른 쓰기의 실행 우선순위를 확정하지 않았다.

## 2. 근거 등급과 NID 결속

경로 접두사 `D/`는 위 decoded-original이다. W=Wire UID, P=Part UID, O=ORef UID, R=RefId/RID다.

- **직접 의미 검토:** D/0147·0148의 Part/Wire/ORef를 D/0047·0048·0562·0563 선언에 연결했다. D/0149·0150은 이 중첩비트의 별도 Set과 최종값 경계만 확인했다.
- **기존 초안 주소 입력:** 10개 `drafts/*-DOTS-DRAFT.md`의 명명 주소표를 읽어 중첩을 계산했다. 설비별 명명 Bool 선언의 출처 RID/AO를 표에 재기재했지만, 그 설비의 전체 원본·알람/자동/전기/도면 조사를 다시 수행한 것은 아니다.
- **검색용 색인:** network-map.json은 `startup only`, LAD402/403/404/405, 색인2/3/4/5, 해당 XML을 찾는 용도다. 색인 문자열이나 해시 일치만으로 의미 검토 완료라고 하지 않는다. identifier-declarations.json의 정확한 `startup only` 이름 검색에서 호출 선언을 확보하지 못했으나 이것은 프로그램 전체에 호출이 없다는 증거가 아니다.
- **바이트 보존:** input-hashes-before.json과 input-hashes-after.json은 입력 20개 파일의 바이트 동일성을 검사한다. 파일 해시의 존재/일치는 Word 주소·호출·비트 의미를 증명하지 않는다.

### 2.1 공통 선언

| 항목 | 직접 선언 | 확인 내용 |
|---|---|---|
| ON | D/0047 SimpleAccess R1, Bool, SSD AO0, SAD Memory | %M0.0. NID2/O167, NID3/O284. 이름만으로 항상 TRUE라는 가정 금지 |
| 0 상수 | D/0048 LiteralConstant R54, OD S16, TD Int, CD/CB `SV=INT_x0023_0`, `V=0` | 0147의 O168/170/172/174/176/178/180/182, 0148의 O285/287/289/291/293/295/297/299/301과 일치 |
| DB2 | D/0562 DepDBBlock Flag R6, TOD `BT=DB, N=2` | D/0563 Word 출력 선언의 BAD BIRID6을 DB2로 결속 |
| DB3 | D/0562 DepDBBlock Allarm R23, TOD `BT=DB, N=3` | D/0563 Word 출력 선언의 BAD BIRID23을 DB3로 결속 |
| Word 범위 | D/0563 해당 GlobalAccess OD S16, TD Word, SSD AO 및 BAD | AO는 bit offset. Word 하나는 시작 byte와 그 다음 byte를 포함. 이름이 없는 절대 Word쓰기도 명명 Bool에 중첩 가능 |

### 2.2 0148의 검색 모호성 해소

network-map의 0148 `inferred_original_nid`는 null이며 ON 검색후보에 D/0047과 D/0664가 함께 있다. 이번 검토는 그 후보 목록을 그대로 확정하지 않았다. D/0048의 입력상수 9개 UID, D/0563의 출력 Word 9개 UID, D/0562의 DB 쓰기 UID가 모두 **NID3**로 일치하며 D/0047의 NID3/O284도 맞는다. 따라서 이 0148 배선은 startup LAD403/NID3으로 결속한다. 0147은 같은 방법으로 NID2에 결속한다. D/0664의 다른 ON 후보는 이 결속에 사용하지 않았다.

## 3. 0147 / LAD402 / NID2: DB2 Word쓰기

- W210 Powerrail→P208.in; W184 O167/R1→P208.operand. P208은 정극성 Contact, 반전 표기 없음.
- W209 P208.out→P138.en 및 P155.en. 두 별도 en 가지가 존재한다.
- 가지A: P138.eno→W187→P141.en→(P141.eno/W190)→P144.en→(P144.eno/W193)→P147.en.
- 가지B: P155.eno→W198→P158.en→(P158.eno/W201)→P161.en→(P161.eno/W204)→P164.en.
- 아래 `in`은 모두 D/0048 R54 INT#0이다. 모든 출력은 D/0563 Word, BAD6→D/0562 Flag DB2, NID2 AK=Write다. `en`은 선 연결을 그대로 기재한 것이며 전체가 현재 실행된다는 선언이 아니다.

| DB2 대상 | 포함 byte | Move / en Wire | 0 입력 연결 | Word 출력 연결 | D/0563 RID / AO |
|---|---|---|---|---|---|
| DBW0 | 0..1 | P138 / W209 | O168/R54→W185→P138.in | P138.out1→W186→O169 | R7 / AO0 |
| DBW2 | 2..3 | P141 / W187 | O170/R54→W188→P141.in | P141.out1→W189→O171 | R9 / AO16 |
| DBW4 | 4..5 | P144 / W190 | O172/R54→W191→P144.in | P144.out1→W192→O173 | R11 / AO32 |
| DBW6 | 6..7 | P147 / W193 | O174/R54→W194→P147.in | P147.out1→W195→O175 | R13 / AO48 |
| DBW8 | 8..9 | P155 / W209 | O176/R54→W196→P155.in | P155.out1→W197→O177 | R15 / AO64 |
| DBW10 | 10..11 | P158 / W198 | O178/R54→W199→P158.in | P158.out1→W200→O179 | R17 / AO80 |
| DBW12 | 12..13 | P161 / W201 | O180/R54→W202→P161.in | P161.out1→W203→O181 | R19 / AO96 |
| DBW14 | 14..15 | P164 / W204 | O182/R54→W205→P164.in | P164.out1→W206→O183 | R21 / AO112 |

## 4. 0148 / LAD403 / NID3: DB3 Word쓰기

- W331 Powerrail→P329.in; W303 O284/R1→P329.operand. P329는 정극성 ON Contact, 반전 표기 없음.
- W330 P329.out→P250.en, P267.en, P281.en. 세 별도 en 가지가 존재한다.
- 가지A: P250.eno→W306→P253.en→(P253.eno/W309)→P256.en→(P256.eno/W312)→P259.en.
- 가지B: P267.eno→W317→P270.en→(P270.eno/W320)→P273.en→(P273.eno/W323)→P276.en.
- 가지C: W330→P281.en.
- 모든 입력은 D/0048 R54 INT#0, 출력은 D/0563 Word, BAD23→D/0562 Allarm DB3, NID3 AK=Write다.

| DB3 대상 | 포함 byte | Move / en Wire | 0 입력 연결 | Word 출력 연결 | D/0563 RID / AO |
|---|---|---|---|---|---|
| DBW0 | 0..1 | P250 / W330 | O285/R54→W304→P250.in | P250.out1→W305→O286 | R24 / AO0 |
| DBW2 | 2..3 | P253 / W306 | O287/R54→W307→P253.in | P253.out1→W308→O288 | R26 / AO16 |
| DBW4 | 4..5 | P256 / W309 | O289/R54→W310→P256.in | P256.out1→W311→O290 | R28 / AO32 |
| DBW6 | 6..7 | P259 / W312 | O291/R54→W313→P259.in | P259.out1→W314→O292 | R30 / AO48 |
| DBW8 | 8..9 | P267 / W330 | O293/R54→W315→P267.in | P267.out1→W316→O294 | R32 / AO64 |
| DBW10 | 10..11 | P270 / W317 | O295/R54→W318→P270.in | P270.out1→W319→O296 | R34 / AO80 |
| DBW12 | 12..13 | P273 / W320 | O297/R54→W321→P273.in | P273.out1→W322→O298 | R36 / AO96 |
| DBW14 | 14..15 | P276 / W323 | O299/R54→W324→P276.in | P276.out1→W325→O300 | R38 / AO112 |
| DBW16 | 16..17 | P281 / W330 | O301/R54→W326→P281.in | P281.out1→W327→O302 | R40 / AO128 |

## 5. 10초안별 명명 비트 중첩

아래 명명비트의 주소·RID/AO는 **기존 각 초안 주소표에서 가져온 입력**이다. 오른쪽 startup 핀/Word 선언은 이번 원문 검토다. DB2/DB3가 다르면 byte.bit가 같더라도 별개 비트다. 물리 Q/I와 HMI DB11 주소는 이번 Word쓰기 대상에 포함하지 않았다.

| 초안/주소표 행 | 명명 DB2 요청·기억 | 0147 중첩 / 정확한 출력 | 명명 DB3 알람 | 0148 중첩 / 정확한 출력 |
|---|---|---|---|---|
| FN05 L78–79 | Flag.M_FN_05 X3.1; 0604 R189/AO25 | DBW2: P141.out1/W189/O171/R9 | Allarm.FN_05_FAULT X3.1; 0604 R188,0657 R149/AO25 | DBW2: P253.out1/W308/O288/R26 |
| SC01 L48–49 | Flag.M_SC_01 X1.6; 0604 R136/AO14 | DBW0: P138.out1/W186/O169/R7 | Allarm.SC_01_FAULT X1.6; 0657 R105/AO14 | DBW0: P250.out1/W305/O286/R24 |
| PV03 L64–66,70–71 | Flag.M_PV03 X11.2; 0604 R193/0609 R153 AO90 | DBW10: P158.out1/W200/O179/R17 | Allarm.PV_03_GATE_NOT_OPEN1 X11.1; 0657 R193/AO89; NOT_CLOSE1 X11.2; R195/AO90 | 두 비트 모두 DBW10: P270.out1/W319/O296/R34 |
| PV03 동일 표 | Flag.PV_03_GATE_MEM_CLOSE X9.0;0609 R149/AO72; MEM_OPEN X9.1;R147/AO73 | 두 비트 모두 DBW8: P155.out1/W197/O177/R15 | 위 두 고장과 별개 기억 비트 | 0150 MEM_CLOSE Set은 §6 참조 |
| MV02 L70–71,78,80 | Flag.MV02_Auto X6.7;0619 R19/AO55 | DBW6: P147.out1/W195/O175/R13 | Allarm.MV02_FAULT X4.0;0573 R16/0619 R22 AO32 | DBW4: P256.out1/W311/O290/R28 |
| MV02 동일 표 | Flag.M_MV02_CLOSE X9.5 / OPEN X9.6;0619 R18/20 AO77/78 | 두 비트 모두 DBW8: P155.out1/W197/O177/R15 | Allarm.Pot_MV02_OFR X24.7;0676 R434/AO199 | **범위 밖**. DB3 byte0..17 쓰기로 이 비트 초기화는 증명 안 됨 |
| MV05 L27–31 | Flag.MV05_Auto X6.6;0619 R61/AO54 | DBW6: P147.out1/W195/O175/R13 | Allarm.MV_05_FAULT X11.5;0573 R31/0619 R64 AO93 | DBW10: P270.out1/W319/O296/R34 |
| MV05 동일 표 | Flag.M_MV05_OPEN X9.4 / CLOSE X9.3;0619 R62/60 AO76/75 | 두 비트 모두 DBW8: P155.out1/W197/O177/R15 | 구동 FAULT는 위 행 | 0149 Auto Set은 §6 참조 |
| ER01 L81–82 | Flag.M_ER01 X5.4;0604 R192/AO44 | DBW4: P144.out1/W192/O173/R11. **기존 ER01 L200/206에 이미 있음** | Allarm.ER01_run X20.1;0604 R217/0657 R246 AO161 | **범위 밖**. 기존 ER01 L204의 경계와 일치 |
| CH01 L52,57 | Flag.M_CH_01 X1.4;0604 R123/AO12 | DBW0: P138.out1/W186/O169/R7 | Allarm.CH_01_FAULT X1.4;0657 R92/AO12 | DBW0: P250.out1/W305/O286/R24 |
| VR01 L56–57 | Flag.M_VR_01 X1.1;0604 R103/AO9 | DBW0: P138.out1/W186/O169/R7 | Allarm.VR_01_FAULT X1.1;0657 R80/AO9 | DBW0: P250.out1/W305/O286/R24 |
| VR02 L68,70 | Flag.M_VR_02 X1.3;0604 R120/AO11 | DBW0: P138.out1/W186/O169/R7 | Allarm.VR_02_FAULT X1.3;0657 R88/AO11 | DBW0: P250.out1/W305/O286/R24 |
| VR03 L52–53 | Flag.M_VR_03 X2.5;0604 R176/AO21 | DBW2: P141.out1/W189/O171/R9 | Allarm.VR_03_FAULT X2.5;0604 R175/0657 R133 AO21 | DBW2: P253.out1/W308/O288/R26 |

이 표는 16개 설비 고유 DB2 비트와 10개 중첩 DB3 비트, 2개 비중첩 DB3 비트를 담는다. 부모에게 전달받은 VR04 X2.6의 검토는 범위 선정 계기일 뿐이며, 이 문서는 VR04의 명명 선언·초안을 재검토하지 않았다.

### 5.1 공통 비트의 별도 중첩

아래는 초안 주소표에 등장하는 공통 요청이다. 각 설비의 고유 요청/알람 개수로 중복 계산하지 않는다.

| 공통 비트 | 기존 초안 주소 근거 | 0147 중첩 |
|---|---|---|
| Flag.RESET_ALLARM DB2.X6.0 | FN05 L84, PV03 L73, MV02 L77, ER01 L89, VR01 L58, VR02 L73, VR03 L56; 대표0657 R13/AO48 | DBW6 P147.out1/W195/O175/R13, byte6..7 |
| Flag.Auto_ON1 DB2.X7.3 | VR01 L62, VR02 L74;0577 R4/AO59 | 같은 DBW6 |
| Flag.Maintenance_ON DB2.X7.5 | ER01 L88;0604 R3/AO61 | 같은 DBW6 |
| Flag.Reset_Allarms_HMI DB2.X13.4 | PV03 L74;0565 R61/AO108 | DBW12 P161.out1/W203/O181/R19, byte12..13 |

DB2.DBW14 및 DB3.DBW6/8/12/14/16에도 원문 쓰기는 존재하지만 위 10초안의 이번 명명 후보 중 별도 고유 비트가 배정되지 않았다. 이 사실을 그 워드가 미사용이라는 의미로 확대하지 않는다.

## 6. 같은 startup 묶음의 Set과 호출 경계

### 6.1 대상 중첩비트의 추가 Set

0쓰기 이후의 **현재 최종값**을 가정하지 않기 위한 인접 원문 대조다. 모든 아래 명명선언은 D/0563, BAD6→D/0562 Flag DB2다. 색인의 0149=순서4,0150=순서5라는 정보와 실제 OB 실행순서를 구분한다.

| 대상 | 직접 원본 Set 배선 | 선언 | 의미/한계 |
|---|---|---|---|
| MV02_Auto DB2.X6.7 | 0149 NID4: W343 rail→ON P337.in; O314/R1→W324→337.operand; P337.out→W338→ON P339.in; O316/R1→W326→339.operand; P339.out→W340→SCoil P297.in; O317/R43→W328→297.operand | 0563 R43, Bool AO55, NID4 UID317 AK Write | 0147 DBW6 0쓰기와 같은 비트에 ON 직렬접점을 거치는 Set이 별도로 있음. 결과값·호출시각 확정 금지 |
| MV05_Auto DB2.X6.6 | 0149 NID4: 위 P337.out→W338→SCoil P307.in; O321/R46→W333→307.operand | 0563 R46, Bool AO54, NID4 UID321 AK Write | 0147 DBW6와 중첩. MV02의 추가 P339 접점을 MV05에 복제하지 않음 |
| PV_03_GATE_MEM_CLOSE DB2.X9.0 | 0150 NID5: W328 rail→ON P326.in; O313/R1→W319→326.operand; P326.out→W327→SCoil P311.in; O318/R53→W324→311.operand | 0563 R53, Bool AO72, NID5 UID318 AK Write | 0147 DBW8와 중첩. LS 입력이나 실제 밸브 닫힘 명령을 검증하는 Set이 아님. 기존 PV03 §3.3과 일치 |

0149/0150의 이 Set이 발견되었다는 사실만으로 다른 23개 중첩 설비비트가 이후에 다시 쓰이지 않는다고 결론내리지 않는다. 이번 작업은 전체 Writer·전체 OB·현재 HMI 이벤트를 조사하지 않았다.

### 6.2 확정되는 호출 경계

- 0147/0148 자체는 Contact와 Move를 담은 FlgNet이며, 두 XML 안에 상위 호출을 식별할 CRef/LRef 또는 CPU 시작 이벤트의 설정이 없다. **그 네트워크가 현재 어떤 OB에서 언제 실행되는지는 이 배선만으로 결속되지 않는다.**
- 0147과 0148의 입력 허가는 각각 ON P208/P329, 내부 연쇄는 §3/§4에 기재한 en/eno이다. `ON`의 이름, INT#0 상수, `startup only` 검색 블록명, 검색 index_order만으로 ‘OB 시작 때 항상 실행’, ‘매 스캔 실행’, ‘현재 0’, ‘재시작 후 모두 Reset’을 주장하지 않는다.
- D/0047에는 ON의 NID1/UID24 AK Write도 존재한다. 이번에는 그 작성 네트워크 및 상위 이벤트 결속을 확보하지 않았다. 그러므로 NID2/3을 읽을 때 ON이 이미 TRUE일 것이라는 전제를 세우지 않는다.
- 실제 상위 블록 종류/번호, 시작·재시작 이벤트, Warm/Cold 차이, Retain 속성, 현재 CPU와 백업의 일치, 실행/인터럽트 순서, 이후 Set/Reset/HMI 쓰기 및 최종값은 추가 원 프로젝트·온라인 근거가 필요하다. 이것은 허가된 읽기 전용 문서 보강의 한계이며 실행시험 요청이 아니다.

## 7. 각 초안에 보강할 수 있는 최소 문구

공통 틀: “명명비트 Set/Reset 외에 startup only LAD402/403의 INT#0 Word쓰기 범위가 [주소]를 포함한다. 원본 Part/Wire/ORef와 Word 선언으로 주소 중첩을 확인했으며 실제 startup 호출·ON/en/eno 유효성·재시작/Retain·현재값·최종 Writer 우선순위는 미확정이다.”

- FN05·SC01·CH01·VR01~03: §5의 요청과 전용 FAULT 양쪽 Word 경로를 추가.
- PV03: 기존 0150 MEM_CLOSE Set 설명에 0147 DBW8의 두 MEM 비트 및 DBW10의 M_PV03, 0148 DBW10의 두 알람을 병기. Word 0쓰기와 MEM_CLOSE Set의 공존을 유지.
- MV02: DBW6 Auto, DBW8 수동2비트, DB3.DBW4 FAULT를 보강. Auto Set 0149 및 Pot_MV02_OFR 범위 밖을 분리.
- MV05: DBW6 Auto, DBW8 수동2비트, DB3.DBW10 FAULT를 보강. 0149의 Auto Set을 병기.
- ER01: 이미 있는 DB2.DBW4/X5.4와 DB3.X20.1 범위 밖 설명은 반복 신규발견으로 계산하지 않는다. 이번 표는 기존 근거를 재결속한 보강이다.

## 8. 검사와 남은 한계

- `extract_scoped_map.py`: 지정 XML만 읽어 17 Move의 in/out/en 핀, 0 LiteralConstant R54, NID, Word 크기/오프셋, DB 종속 선언을 교차검사한다. XML 텍스트 정적 구조 검사이며 제어 흐름의 실행·시뮬레이션이 아니다.
- `startup-word-map.json`: 그 17개 쓰기의 재현 가능한 핀/선언 결과. 해석을 대신하는 실행모델이 아니다.
- 10초안 명명 주소는 입력으로 재사용했다. 모든 설비의 고유 명명 선언을 새로 독립검증했다거나 전체 다른 쓰기를 망라했다고 주장하지 않는다.
- 현장 정상극성·정격·보호값·알람 실제발생·고장 해소·재기동·복구완료는 이 검토로 판단하지 않는다.
- 입력 20파일의 전후 SHA-256 검사는 별도 JSON에 기록한다. 산출물 SHA-256은 SHA256SUMS.txt에 기록한다.


## 전달 범위
이 보강은 기존 10개 초안의 알려진 다른 쓰기 목록을 보완한다. 기존 전달 초안은 보존하며 새로운 설비 완료 수를 추가하지 않는다. 현재 startup 실행과 값/복구 동작은 미검증이다. 조사 취합 단계에서 0147의 Move8개·0148의 Move9개 및 대상 선언 일부를 제한 재대조했다.
