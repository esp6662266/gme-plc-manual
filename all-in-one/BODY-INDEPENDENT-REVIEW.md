# CC01·HE01 독립 정적 검토 — 2026-10-09

검토 대상은 body-source-details.py, build-body-manual.py, 현재 body-manual.html과 원본 P&ID·OEM·추가 시공도면입니다. 공통 파일을 수정하지 않았습니다. 확정 전사 오류는 1건이며 그 외는 표현/확인 경계 보강입니다. 부모가 순차 통합합니다.

## P2 · BODY-IND-01 · PB15/18을 PB15–18 범위로 확대함

분류: confirmed_source_transcription_error / 필수 수정: 예

위치: body-source-details.py:85, body-source-details.py:96, body-manual.html

원본 근거: 원본 시공 PDF53의 DESCRIPTION은 LS01-08|LS32/33|PB15/18. P03/P06도 PV01 PB15·PV04 PB18을 별도 표기하며 PB16은 PV02, PB17은 PV03.

영향: PB16·PB17을 CC01 ENT2TB1 공유 간선에 포함한 것으로 읽힌다.

문구/구조 수정안: LS01–08 / LS32/33 / PB15 / PB18

## P2 · BODY-IND-02 · HE01 MV01 우회 유로와 FN02/MV04측을 방향으로 분리

분류: process_direction_omission / 필수 수정: 아니오, 권고

위치: body-source-details.py:58, body-source-details.py:62

원본 근거: P&ID 화살표: AB01 출구→HE01 하부 header; 하부에서 열교환 통로 상향→상부 header→CY01/CY03. MV01은 하부 header 우측과 상부 출구 사이 관로. FN02→MV04→좌상 입력, 좌하 출력은 왼쪽 AB01측으로 향하며 MV04 하향 분기도 여기에 합류.

영향: 현재 문장은 명백한 방향 오기는 아니지만 MV01을 공기측으로 묶어 읽을 여지가 있고 header bypass가 설명되지 않는다.

문구/구조 수정안: P&ID 화살표상 AB01 출구측은 HE01 하부 header로 들어가 열교환 통로를 따라 상부 header·CY01/CY03측으로 이어집니다. MV01은 하부 header 우측과 상부 출구 관로 사이 우회 경로입니다. FN02–MV04측은 HE01 좌상 입력·좌하 출력과 MV04 하향 분기를 별도로 보며, 좌하 관로의 화살표는 AB01측을 향합니다. 이는 도면 연결·방향 설명이며 현재 매체·유량·실물 연결은 확인 전입니다.

## P3 · BODY-IND-03 · TC 계측의 KX 케이블과 OEM 4–20mA 표기를 별도 확인사항으로 보강

분류: interface_boundary_clarification / 필수 수정: 아니오, 권고

위치: body-source-details.py:118, body-source-details.py:120

원본 근거: 시공53/3_14 및56/6_23·24는 TC/KX2S. OEM FG77·78은 TC01/02/06 +24V와 출력4–20mA 회로.

영향: 위치 차이뿐 아니라 센서/변환기/제어반 구간 경계가 불명확하다. KX와4–20mA가 같은 구간인지 다른 구간인지 현재 자료로 단정할 수 없다.

문구/구조 수정안: 시공 TC/KX2S 구간과 OEM +24V·4–20mA 입력 구간을 자동으로 같은 케이블로 연결하지 않습니다. 센서 소자–변환기 위치–케이블 양단–제어반 입력을 현재 승인 도면/표찰로 확인합니다.

## P3 · BODY-IND-04 · BR01F는 기능 설명이 아니라 케이블 번호의 말미

분류: table_field_clarification / 필수 수정: 아니오, 권고

위치: body-source-details.py:115, body-source-details.py:116

원본 근거: 시공64/14_17·18: CABLE NO. =ENT+CC01-BR01F, TAG BR-01, DESCRIPTION 공란. 양 행 동일 번호와 AI/CVV-S4S 표기.

영향: description=BR01F를 원본 DESCRIPTION의 전사로 오해할 수 있다. 원본 전체 번호와 해당 필드 의미를 함께 보여주면 더 정확하다.

문구/구조 수정안: description 공란을 보존하고 note 또는 cable_number에 =ENT+CC01-BR01F(두 원본 행 동일 번호)를 기록합니다.

## 확인한 경계

- 32 selected rows; no masked 53/3_5 or56/6_7–10 in selected data
- 53/3_3 and3_30 remain separate 25G/12G rows
- 53/3_6 PEW358 AI separated from3_7 AC110V power
- TC06 P&ID/CC01 construction location versus FG78 OUTPUT AB01 description retained
- RO04 CC01 construction location versus FG81 OUTLET FN01 retained
- TC01/02 andRO01/02 HE01 construction zone versus OEM AB01 process description retained
- MV04 M18A/M18B and LS21A/22A/21B/22B remain separate; current mapping unresolved
- 14_17/14_18 repeat cable rows preserved as existing C02; no deduplication
- Current approval/as-built, body ownership, live PLC, TIA compilation, field repair remain unverified

## 그림 재현 및 시각 판독

P&ID 원본 page1을 scale3200으로 새 렌더 후 반시계90도 회전한 RGB 픽셀은 assets/PID-landscape.png와 전부 일치했습니다. CC01·AB01·HE01 세 crop도 기록된 원본 영역과 픽셀 일치합니다. P&ID 전체와 CC01/HE01 crop을 시각 확인했습니다.

OEM FG77/78/80/81(PDF78/79/81/82)은 scale2800의 새 원본 렌더와 각각 픽셀 일치했고 전체 페이지를 시각 확인했습니다.

시공 P03/P06/P21/P53/P56/P57/P64의 전체 PNG를 시각 확인했습니다. 동일 scale2800의 원본 새 Poppler 렌더와 크기는 같지만 픽셀은 일치하지 않습니다. 이를 자료 변경/위변조로 판정하지 않습니다. 새 원본 PDF P53/P56/P57의 선택행 쪽 crop도 화면에서 확인했으나 표시용 저화질 crop이며 상세 텍스트/규격 판독은 전체 PNG를 함께 사용했습니다. P03/P06/P21/P64의 새 렌더 자체는 픽셀/수치 비교만 했으며 별도 시각 판독 완료라고 주장하지 않습니다.

|PDF page|Asset SHA256|Fresh PNG SHA256|Mean absolute RGB delta|
|---|---|---|---|
|3|1ce09c5bb895d2201f84a0896fd695fe62d22bdb0683ba822b7b3811f8bf91b6|1d0d9c128277ca5aded7c3744833016a4a5a2b52d48f85e447883e2c141ae641|6.612892/255|
|6|551b7955a499045b98740c5b68378b58eafa537665e2fa8636422da517a8739f|e14e48007c0a191bfe4974f306eb4c6fcff0dc51a6d4fc48fd556dd684999265|5.348599/255|
|21|05d16b4f74394da376384aa23334340620fc44d3648ea684466042e507fb05ad|b8087b451e861d3a6c4ffb2713862eda82ed011f0165d97d599ae793f8515b2a|4.868335/255|
|53|6c4c596ffa178ac409b2288a1785b8b61e9855d825f1eb487b53cb3581fa18b1|0d64bd9df20117e88e08f1569ef2f2e6f45eac6f8cc2cf49720056a1b626cc7d|6.603739/255|
|56|1196c4620b56115c87124221061cdc0278ed44999a9f55d4c92c7a6cb1e265c5|00e232d6aaf7af4ee66c7289bfa56879503bb45092eba36c5675a06d7adcd1a2|5.748804/255|
|57|d2a399e63cc2588c0775755f2c6138812472e24ffcc2a18babf5c645d5f5a449|c0fd58504c33fcc82accba9e4c69b6abcaaaccba07ad52920ce44ebb8891e7a7|5.924939/255|
|64|14943205d46e3a44101064074e0b90b87ba2f727db7ffebc314c12deea4e697c|831f59faaaf1f0dce3362ee9b5928f4e741036fdeeed8dfceddfa095ad823c6f|5.755838/255|

## 원본 PLC 대조 범위

색인/모델은 파일 탐색에만 사용했습니다. 선택 원본 FlgNet의 ORef·RefId·Wire·Part/CRef 핀과 원본 IdentXmlPart의 UID/RID/NID 선언을 대조했습니다. 핵심 목격값은 아래와 같고 전체 실행순서/현재값을 확정하지 않습니다.

- 1742 · sources/decoded-original/0492-FlgNet.xml · TC06 ORef384/RID81→Wire391→CRef376.Analog_input; Data.Temp_T6 ORef387/RID84←Wire394←OutValue. Ident0678/0676 NID12 matches.
- 1751 · sources/decoded-original/0501-FlgNet.xml · R004 ORef583/RID128→Wire590→CRef575.Analog_input; Data.RO04 ORef586/RID131←Wire593←OutValue. Ident0678/0676 NID21 matches. OFF contact en andON IN0 are separate; not proof of execution.
- 1931 · sources/decoded-original/0238-FlgNet.xml · Disable_Load_RD01 ORef77/RID16←Wire90←Part66 Coil; Ident0605 NID2/UID77.
- 1911 · sources/decoded-original/0276-FlgNet.xml · R1 Gate ON ORef150/RID12←Wire174←Part115 Coil; Ident0607 NID1/UID150.
- 1935 · sources/decoded-original/0242-FlgNet.xml · Start BC01 ORef211/RID42←Wire225←Part202 Coil; Ident0602 NID6/UID211.
- 1936 · sources/decoded-original/0243-FlgNet.xml · Start RD01 ORef251/RID48←Wire268←Part240 Coil; Ident0602 NID7/UID251.
- 1745 · sources/decoded-original/0495-FlgNet.xml · Data.Press_PC01 ORef447/RID99←Wire454←CRef436.OutValue; Ident0676 NID15/UID447.
- 1747 · sources/decoded-original/0497-FlgNet.xml · PSH03 ORef484/RID106→Wire491→CRef476.Analog_input; Data.PSH03 ORef487/RID109←Wire494←OutValue; Ident0678/0676 NID17.
- 1705 · sources/decoded-original/0344-FlgNet.xml · Data.PSH03_SETPOINT ORef287/RID29→Sub256.in1; Data.PSH03 ORef288/RID30→Sub256.in2; ErrPSH03 ORef289/RID31←Sub256.out. Ident0619/0062 NID3, Local retained.
- 1769 · sources/decoded-original/0526-FlgNet.xml · MV04_M18A ORef26/RID472→Wire35→CRef22.Analog_input; HMI_DB.Amp_MC04 ORef29/RID473←Wire38←OutValue; Ident0678/0676 NID52. MV04_M18A raw Input AO2592 bits corresponds IW324. Existing discrepancy retained, not diagnosed or corrected.

## 수행하지 않은 검증

- Only named source references and selected critical native wires/declarations were inspected; no complete logic equivalence claim
- Fresh original construction previews were cropped/lossy for display on53/56/57; detail reading also used full2800 PNG assets
- Construction assets do not pixel-match fresh Poppler render; full-page semantic equivalence was not established solely from hash or mean pixel differences
- Network map and program-model used for locating XML only; not treated as execution verification
- No simulator authoring/modification/execution; no real PLC/site/field write; no shared source or HTML modification

## 검토 시점 파일 해시

- body-source-details.py · bcb4f882e45ec175ccc4d4d0c93c41735aa8357f43b580b38d64939615c42258 · 보고서 작성 시 동일: False
- build-body-manual.py · b47ea4a233e11583a2691bf91d6d88a49cf56c98845652af088b06e20fe4ba96 · 보고서 작성 시 동일: False
- body-manual.html · 76e1d8cdd939dc6a46f45db3c3e13640b9ce6d3843483a1a305f1d9ed9ca2448 · 보고서 작성 시 동일: False

원본 PDF 해시 및 상세 체크는 registers/body-independent-review.json에 보존했습니다. 최종 통합 후 부모가 수정된 본문/JSON과 링크를 다시 확인해야 합니다.

## 부모 통합 · 2026-10-09

필수 전사 오류와 세 권고를 본문에 반영했습니다. 기존 검토 시점 해시는 역사로 보존하며 최종 HTML/JSON 해시는 body-manual-verification.json에서 다시 확인합니다. 별도 reviewer는 AB011979/1986/1856/1858/1866의 Part·Wire·UID/RID/NID와 타이머3개, 1719 검색색인 원문을 읽기 전용 대조했고 확정 오류0건입니다. 원본 SCL·현재 실행·현장 복구는 미확인입니다. 상세 결과는 기존 JSON의 ab01_original_review와 parent_integration에 부모가 기록했습니다.
