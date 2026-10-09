# GME 전체 설비 통합 매뉴얼 v0.2

작성일 2026-10-07. 제공자료 기준 검토본.

프로젝트 목적: 전체 설비 매뉴얼 작성, 고장 진단과 수리, PLC 프로그램 구조 파악 및 개선 검토. 전체 설비 제어 명세를 공통 기준으로 작성하고, HMI와 시뮬레이터는 탐색·진단·고장 재현·개선안 검증에 활용한다. [목적과 작업 기준](PROJECT-PURPOSE.md) · [전체 설비 제어 명세](control-spec.html)

총 248개 관리 항목: 주설비·계측·외부 연동·공통 기능 121개, 하위 구성품·펄스 밸브 127개. 원본 LAD 네트워크 426개를 복원·연결했다. 시뮬레이션 시험안 577개는 미실행이다.

## 적용 기준과 자료

P&ID 1684n002 Rev.I(2013), 전기 Rev.2(265페이지), GME_20250506.zap18 내부 GME_20250605.ap18(V18.0.1.0), GitHub 2ebff1273f586f3355a2ba8fb91d701ac94e4a5e 및 기존 HMI 설정을 기준으로 한다. 현장 현재 설치·프로그램·온라인 값을 확정한 문서는 아니다.

원본 PEData.plf에서 압축/분할 XML을 복원하고 검색 객체 키로 426개 LAD를 각각 연결했다. 접점·코일·Negated 핀·Wire 구조를 원본 자료로 제공한다. 이름은 UID/RID·NID·검색 이름 일치 시 해석했고 미해석 RefId는 보존했다. TIA 복원·컴파일·실행 검증은 별도 단계다.

## 작업 기록과 시뮬레이터 기준

물리 입력, 내부 기억, HMI 가공 상태, 명령 출력, 설정값, 알람은 별도 신호로 관리한다. 설비 ID·FG/PDF 페이지·네트워크 ID·전후 값·단자/계측 결과·조치·증거·검증자·일시를 기록한다. 자동 순서와 정지는 실제 블록 호출·접점 분기·주기 OB·중복 쓰기 순서로 확인한다.

시뮬레이터 모델은 입력 샘플링 → 원본 조건 평가 → 상태/타이머 갱신 → 출력 → 장치 응답 → HMI의 각 단계를 기록한다. 공정 계수·관성·응답시간을 가정한 경우 교육용 가정으로 표시한다. 시험 기대 결과는 원본 실행 결과와 대조해 확정한다. 이번 결과물에 PLC 통신 제어나 시뮬레이터 실행 엔진은 구현하지 않았다.

## 자료 불일치

| ID | 항목 | 자료 내용 | 다음 검증 |
| --- | --- | --- | --- |
| BASELINE | 백업 파일명과 내부 프로젝트 날짜 | GME_20250506.zap18 내부 GME_20250605.ap18; 2026-10-01은 보관 일자 | 온라인 PLC 및 현재 엔지니어링 프로젝트와 비교 |
| POWER | 설치 전력·도면 세대 | 2013 P&ID 355kW / 2024~2025 전기 463kW | 설치·개조 내역과 명판 기준 확정 |
| VOLTAGE | 주전원 표기 | 전기 표지 440Vac / 일부 인덱스 제목 400V | 현장 공급 및 실제 회로/명판 확인 |
| PV01-LS02 | 닫힘 센서 예비 표기 | FG70에 LS02, PLC I8.7, FG124 SPARE 표기 | 단자와 현재 입력 채널 실제 사용 확인 |
| ADDRESS | 현재 주소와 과거 주석 | 심볼 Address와 설명에 남은 옛 E/A 주소가 다름 | Address 및 실제 모듈/배선으로 대조 |
| MC05-SC12-PV04 | 삭제/예비 및 잔존 I/O | 도면/심볼에는 존재, Motors 1 일부 deleted 제목 | 실물·현재 네트워크·사용 상태 확정 |
| FN01-FAN | 냉각팬 삭제/예비 | FG54 SPARE, I4.5/Q3.5 잔존 | 현재 연결 및 필요성 확인 |
| MV04-MC04 | 아날로그 입력 목적 충돌 | MV04 위치 M18A/IW324를 MC04 전류 변환에서 참조 | 현장 배선·모듈 채널·사용 프로그램 목적 확인 |
| FN04 | 실구동 출력 및 제목 | Q17.1 start fn04 / Q4.2 옛 FN04 주석; 변환 제목 FN02 | 사용처와 전기도면 기준 현재 채널 확인 |
| MV06-LS | 리미트 번호 변경 | P&ID LS34/35 / 백업 LS40/41 | 변경 이력과 실제 센서/단자 확인 |
| CL-NAMESPACE | 같은 CL 번호의 다른 장치 | P&ID 실린더 CL01~12 / 외부 모터 CL01~19 일부 채널 | CYL-CL / CLIENT-CL ID 유지 |
| TC05 | 베어링 채널·범위 문구 | TC04/TC05·범위 설명 혼재 | 전송기 범위와 AI 채널/환산 계수 확인 |
| RO03 | 산소 대체 계산 | 실제 입력 외 RO02+11 참조 | 원본 분기·시험 비트·현재 값 확인 |
| BF02-DP | 차압 계수 이름 | DP02와 DP01 임계값 참조 혼재 | 공용 설정 의도와 실제 적용 확인 |
| CLIENT19 | 고장/운전 신호 의미 | Primaryshredder run을 fault 알람에 연결 | 외부 신호 정상 극성과 원본 접점 확인 |
| BR01 | 버너 상세 도면 경계 | P&ID에서 버너 별도 DWG 참조 | 제조사 버너 도면/안전 제어 순서 확보 |
| SOURCE-XML | 복원 해석과 TIA 결과 | 426 LAD 원본 XML 복원; 상수/일부 참조 이름 미해석 | TIA에서 프로젝트 복원·블록 비교·컴파일·오프라인 실행 검증 |
| PID-TM | 과거 위치 계측과 현재 엔코더 | P&ID ZT02~06 / TM·엔코더 카운트 사용 | 실제 위치 계측 방식/보정 절차 확인 |

## 전체 설비 대장

| ID | 설비명 | 영역 | 상위 | 자료 상태 |
| --- | --- | --- | --- | --- |
| BC01 | 드럼 투입 컨베이어 | 원료 이송 |  | 자료에서 확인 |
| RD01 | 회전 드럼 | 원료 이송 |  | 자료에서 확인 |
| RD01-FAN | 드럼 모터 냉각팬 | 원료 이송 | RD01 | 자료에서 확인 |
| MC03 | 예비 모터 MC03 | 원료 이송 |  | 예비·실물 동일성 확인 |
| MC04 | 금속 컨베이어 | 원료 이송 |  | 자료에서 확인 |
| MC05 | 금속 컨베이어 MC05 | 원료 이송 |  | 삭제 제목·예비 여부 확인 |
| VS01 | 진동 스크린 | 원료 이송 |  | 자료에서 확인 |
| SC12 | 드럼 배출실 스크루 | 원료 이송 |  | SPARE·삭제 제목 |
| CC01 | 드럼 투입실 | 공정 본체 |  | 자료에서 확인 |
| UC01 | 드럼 배출실 | 공정 본체 |  | 자료에서 확인 |
| AB01 | 연소 챔버 | 연소·열회수 |  | 자료에서 확인 |
| BR01 | 가스 버너 | 연소·열회수 |  | 자료에서 확인 |
| HE01 | 열교환기 | 연소·열회수 |  | 자료에서 확인 |
| FN01 | 순환 블로어 | 연소·열회수 |  | 자료에서 확인 |
| FN02 | 열회수 블로어 | 연소·열회수 |  | 자료에서 확인 |
| FN03 | 연소 공기 블로어 | 연소·열회수 |  | 자료에서 확인 |
| FN04 | 집진 배기팬 | 집진·석회 |  | 자료에서 확인 |
| FN05 | 석회 계통 송풍기 | 집진·석회 |  | 자료에서 확인 |
| FN06 | 보조 블로어 | 연소·열회수 |  | 자료에서 확인 |
| FN01-FAN | FN01 모터 냉각팬 | 연소·열회수 | FN01 | SPARE·삭제 제목 |
| CH01 | 냉각기 | 연소·열회수 |  | 자료에서 확인 |
| MV01 | 모터 구동 밸브 | 제어 밸브 |  | 자료에서 확인 |
| MV02 | 모터 구동 밸브 | 제어 밸브 |  | 자료에서 확인 |
| MV03 | 모터 구동 밸브 | 제어 밸브 |  | 자료에서 확인 |
| MV04 | 모터 구동 밸브 | 제어 밸브 |  | 자료에서 확인 |
| MV05 | 모터 구동 밸브 | 제어 밸브 |  | 자료에서 확인 |
| MV06 | 모터 구동 밸브 | 제어 밸브 |  | 자료에서 확인 |
| PV01 | 공압 게이트/분기 밸브 | 공압 밸브 |  | 자료에서 확인 |
| PV02 | 공압 게이트/분기 밸브 | 공압 밸브 |  | 자료에서 확인 |
| PV03 | 공압 게이트/분기 밸브 | 공압 밸브 |  | 자료에서 확인 |
| PV04 | 공압 게이트/분기 밸브 | 공압 밸브 |  | 예비 표기·삭제 제목 |
| PV05 | 질소 주입 밸브 | 공압 밸브 |  | 자료에서 확인 |
| PV06 | 질소 주입 밸브 | 공압 밸브 |  | 자료에서 확인 |
| PV14 | 필터 냉풍 유입 밸브 | 공압 밸브 |  | 자료에서 확인 |
| CY01 | 사이클론 | 집진·석회 |  | 자료에서 확인 |
| CY02 | 사이클론 | 집진·석회 |  | 자료에서 확인 |
| CY03 | 사이클론 | 집진·석회 |  | 자료에서 확인 |
| CY04 | 사이클론 | 집진·석회 |  | 자료에서 확인 |
| CY05 | 사이클론 | 집진·석회 |  | 자료에서 확인 |
| VR01 | 로터리 밸브 | 집진·석회 |  | 자료에서 확인 |
| VR02 | 로터리 밸브 | 집진·석회 |  | 자료에서 확인 |
| VR03 | 로터리 밸브 | 집진·석회 |  | 자료에서 확인 |
| VR04 | 로터리 밸브 | 집진·석회 |  | 자료에서 확인 |
| VR05 | 로터리 밸브 | 집진·석회 |  | 자료에서 확인 |
| VR06 | 로터리 밸브 | 집진·석회 |  | 자료에서 확인 |
| SC01 | 사이클론 분진 스크루 | 집진·석회 |  | 자료에서 확인 |
| SC10 | BF01 분진 스크루 | 집진·석회 |  | 자료에서 확인 |
| SC11 | BF02 분진 스크루 | 집진·석회 |  | 자료에서 확인 |
| BF01 | 백 필터 | 집진·석회 |  | 자료에서 확인 |
| BF02 | 백 필터 | 집진·석회 |  | 자료에서 확인 |
| LD01 | 석회 마이크로피더 | 집진·석회 |  | 자료에서 확인 |
| LD01A | 석회 사일로 진동기 | 집진·석회 | LD01 | 자료에서 확인 |
| ER01 | 전기 히터 | 집진·석회 |  | 자료에서 확인 |
| CM01 | 집진 배기 스택 | 공정 본체 |  | 자료에서 확인 |
| CM02 | 상부 배기 스택 | 공정 본체 |  | 자료에서 확인 |
| CR01 | 운전 제어반 | 공정 본체 |  | 자료에서 확인 |
| BWF01 | 고객 설비 계량 피더 | 외부 연동 |  | 자료에서 확인 |
| BWF02 | 고객 설비 계량 피더 | 외부 연동 |  | 자료에서 확인 |
| LIW | 외부 LIW 피더 | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL01 | Apron conveyor A | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL02 | Impactor | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL03 | Impact vibration feeder | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL04 | Belt conveyor A | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL05 | Air knife | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL06 | Belt conveyor B | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL07 | Shredder 1 | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL08 | Shredder vibration feeder | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL09 | Belt conveyor C | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL10 | Rotex screen | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL13 | Apron conveyor B | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL14 | Shredder 2 | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL15 | Belt conveyor D | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL16 | Belt conveyor E | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL17 | Weighing hopper 2 | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL18 | Hopper conveyor 2 | 외부 연동 |  | 자료에서 확인 |
| CLIENT-CL19 | Primary shredder | 외부 연동 |  | 자료에서 확인 |
| TC01 | 온도 계측 | 계측 |  | 자료에서 확인 |
| TC02 | 온도 계측 | 계측 |  | 자료에서 확인 |
| TC03 | 온도 계측 | 계측 |  | 자료에서 확인 |
| TC04 | 온도 계측 | 계측 |  | 자료에서 확인 |
| TC05 | 온도 계측 | 계측 |  | 자료에서 확인 |
| TC06 | 온도 계측 | 계측 |  | 자료에서 확인 |
| TC07 | 온도 계측 | 계측 |  | 예비·운영 상태 확인 |
| TC09 | 온도 계측 | 계측 |  | 자료에서 확인 |
| TC10 | 온도 계측 | 계측 |  | 예비·운영 상태 확인 |
| TC11 | 온도 계측 | 계측 |  | P&ID 로컬 계측 |
| RO01 | 산소 분석 채널 | 계측 |  | 자료에서 확인 |
| RO02 | 산소 분석 채널 | 계측 |  | 자료에서 확인 |
| RO03 | 산소 분석 채널 | 계측 |  | 자료에서 확인 |
| RO04 | 산소 분석 채널 | 계측 |  | 자료에서 확인 |
| PSH01 | 압력 측정 채널 | 계측 |  | 자료에서 확인 |
| PSH02 | 압력 측정 채널 | 계측 |  | 자료에서 확인 |
| PSH03 | 압력 측정 채널 | 계측 |  | 자료에서 확인 |
| PC01 | 집진 흡인 압력 | 계측 |  | 자료에서 확인 |
| PC02 | 소프트웨어 압력 루프 명칭 | 계측 |  | 소프트웨어 명칭·물리 태그 확인 |
| DP01 | 백 필터 차압 | 계측 |  | 자료에서 확인 |
| DP02 | 백 필터 차압 | 계측 |  | 자료에서 확인 |
| ZT01 | FN01 진동 계측 | 계측 |  | SPARE·활성 조건 확인 |
| ZT02 | P&ID 밸브 위치 계측 | 계측 | MV01 | P&ID·현재 엔코더 동일성 확인 |
| ZT03 | P&ID 밸브 위치 계측 | 계측 | MV02 | P&ID·현재 엔코더 동일성 확인 |
| ZT04 | P&ID 밸브 위치 계측 | 계측 | MV03 | P&ID·현재 엔코더 동일성 확인 |
| ZT05 | P&ID 밸브 위치 계측 | 계측 | MV05 | P&ID·현재 엔코더 동일성 확인 |
| ZT06 | P&ID 밸브 위치 계측 | 계측 | MV06 | P&ID·현재 엔코더 동일성 확인 |
| LT01 | 석회 사일로 레벨 | 계측 | LD01 | 자료에서 확인 |
| SS01 | 이송 장치 감시 스위치 | 계측 | BC01 | 자료에서 확인 |
| SS09 | 이송 장치 감시 스위치 | 계측 | MC03 | 자료에서 확인 |
| SS10 | 이송 장치 감시 스위치 | 계측 | MC04 | 자료에서 확인 |
| SS11 | 이송 장치 감시 스위치 | 계측 | MC05 | 자료에서 확인 |
| PSL05 | 압축공기 저압 스위치 | 계측 |  | 자료에서 확인 |
| EV01 | 공압 솔레노이드 | 하위 구성품 | PV01 | 자료에서 확인 |
| EV02 | 공압 솔레노이드 | 하위 구성품 | PV01 | 자료에서 확인 |
| EV03 | 드럼 윤활 솔레노이드 | 하위 구성품 | RD01 | 자료에서 확인 |
| EV04 | 공압 솔레노이드 | 하위 구성품 | PV02 | 자료에서 확인 |
| EV05 | 공압 솔레노이드 | 하위 구성품 | PV02 | 자료에서 확인 |
| EV06 | 공압 솔레노이드 | 하위 구성품 | PV03 | 자료에서 확인 |
| EV07 | 공압 솔레노이드 | 하위 구성품 | PV04 | 자료에서 확인 |
| EV11 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV12 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV13 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV14 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV15 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV16 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV17 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV18 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV19 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV20 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV21 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV22 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV23 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV24 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV25 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV26 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV27 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV28 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV29 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV30 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV31 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV32 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV33 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV34 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV35 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV36 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV37 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV38 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV39 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV40 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV41 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV42 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV43 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV44 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV45 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV46 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV47 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV48 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV49 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV50 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF01 | 자료에서 확인 |
| EV51 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV52 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV53 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV54 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV55 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV56 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV57 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV58 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV59 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV60 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV61 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV62 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV63 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV64 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV65 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV66 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV67 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV68 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV69 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV70 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV71 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV72 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV73 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV74 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV75 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV76 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV77 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV78 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV79 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV80 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV81 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV82 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV83 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV84 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV85 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV86 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV87 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV88 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV89 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| EV90 | 필터 펄스 세정 밸브 | 필터 세정 밸브 | BF02 | 자료에서 확인 |
| CYL-CL01 | 공압 실린더 | 하위 구성품 | PV01 | 자료에서 확인 |
| CYL-CL02 | 공압 실린더 | 하위 구성품 | PV01 | 자료에서 확인 |
| CYL-CL03 | 공압 실린더 | 하위 구성품 | PV01 | 자료에서 확인 |
| CYL-CL04 | 공압 실린더 | 하위 구성품 | PV01 | 자료에서 확인 |
| CYL-CL05 | 공압 실린더 | 하위 구성품 | PV02 | 자료에서 확인 |
| CYL-CL06 | 공압 실린더 | 하위 구성품 | PV02 | 자료에서 확인 |
| CYL-CL07 | 공압 실린더 | 하위 구성품 | PV02 | 자료에서 확인 |
| CYL-CL08 | 공압 실린더 | 하위 구성품 | PV02 | 자료에서 확인 |
| CYL-CL09 | 공압 실린더 | 하위 구성품 | PV03 | 자료에서 확인 |
| CYL-CL10 | 공압 실린더 | 하위 구성품 | PV03 | 자료에서 확인 |
| CYL-CL11 | 공압 실린더 | 하위 구성품 | PV04 | 자료에서 확인 |
| CYL-CL12 | 공압 실린더 | 하위 구성품 | PV14 | 자료에서 확인 |
| LS01 | 밸브 위치 리미트 스위치 | 하위 구성품 | PV01 | P&ID/전기/백업 번호 대조 |
| LS02 | 밸브 위치 리미트 스위치 | 하위 구성품 | PV01 | P&ID/전기/백업 번호 대조 |
| LS05 | 밸브 위치 리미트 스위치 | 하위 구성품 | PV01 | P&ID/전기/백업 번호 대조 |
| LS06 | 밸브 위치 리미트 스위치 | 하위 구성품 | PV01 | P&ID/전기/백업 번호 대조 |
| LS09 | 밸브 위치 리미트 스위치 | 하위 구성품 | PV03 | P&ID/전기/백업 번호 대조 |
| LS10 | 밸브 위치 리미트 스위치 | 하위 구성품 | PV03 | P&ID/전기/백업 번호 대조 |
| LS15 | 밸브 위치 리미트 스위치 | 하위 구성품 | MV05 | P&ID/전기/백업 번호 대조 |
| LS16 | 밸브 위치 리미트 스위치 | 하위 구성품 | MV05 | P&ID/전기/백업 번호 대조 |
| LS17 | 밸브 위치 리미트 스위치 | 하위 구성품 | MV02 | P&ID/전기/백업 번호 대조 |
| LS18 | 밸브 위치 리미트 스위치 | 하위 구성품 | MV02 | P&ID/전기/백업 번호 대조 |
| LS19 | 밸브 위치 리미트 스위치 | 하위 구성품 | MV03 | P&ID/전기/백업 번호 대조 |
| LS20 | 밸브 위치 리미트 스위치 | 하위 구성품 | MV03 | P&ID/전기/백업 번호 대조 |
| LS21A | 밸브 위치 리미트 스위치 | 하위 구성품 | MV04 | P&ID/전기/백업 번호 대조 |
| LS21B | 밸브 위치 리미트 스위치 | 하위 구성품 | MV04 | P&ID/전기/백업 번호 대조 |
| LS22A | 밸브 위치 리미트 스위치 | 하위 구성품 | MV04 | P&ID/전기/백업 번호 대조 |
| LS22B | 밸브 위치 리미트 스위치 | 하위 구성품 | MV04 | P&ID/전기/백업 번호 대조 |
| LS23 | 밸브 위치 리미트 스위치 | 하위 구성품 | MV01 | P&ID/전기/백업 번호 대조 |
| LS24 | 밸브 위치 리미트 스위치 | 하위 구성품 | MV01 | P&ID/전기/백업 번호 대조 |
| LS25 | 밸브 위치 리미트 스위치 | 하위 구성품 | PV02 | P&ID/전기/백업 번호 대조 |
| LS26 | 밸브 위치 리미트 스위치 | 하위 구성품 | PV02 | P&ID/전기/백업 번호 대조 |
| LS29 | 밸브 위치 리미트 스위치 | 하위 구성품 | PV02 | P&ID/전기/백업 번호 대조 |
| LS30 | 밸브 위치 리미트 스위치 | 하위 구성품 | PV02 | P&ID/전기/백업 번호 대조 |
| LS32 | 밸브 위치 리미트 스위치 | 하위 구성품 | PV04 | P&ID/전기/백업 번호 대조 |
| LS33 | 밸브 위치 리미트 스위치 | 하위 구성품 | PV04 | P&ID/전기/백업 번호 대조 |
| LS34 | 밸브 위치 리미트 스위치 | 하위 구성품 | MV06 | P&ID/전기/백업 번호 대조 |
| LS35 | 밸브 위치 리미트 스위치 | 하위 구성품 | MV06 | P&ID/전기/백업 번호 대조 |
| LS40 | 밸브 위치 리미트 스위치 | 하위 구성품 | MV06 | P&ID/전기/백업 번호 대조 |
| LS41 | 밸브 위치 리미트 스위치 | 하위 구성품 | MV06 | P&ID/전기/백업 번호 대조 |
| SYS-POWER | 주전원·보조전원·제어반 | 공통 시스템 |  | 자료에서 확인 |
| SYS-SAFETY | 비상정지·일반 안전 회로 | 공통 시스템 |  | 자료에서 확인 |
| SYS-PLC-IO | CPU·분산 I/O·신호 변환 | 공통 시스템 |  | 자료에서 확인 |
| SYS-HMI | HMI·통신·가공 상태 | 공통 시스템 |  | 자료에서 확인 |
| SYS-ALARM | 알람·경광등·사이렌·Reset | 공통 시스템 |  | 자료에서 확인 |
| SYS-AUTO | 자동 기동·정지·유지보수 | 공통 시스템 |  | 자료에서 확인 |
| SYS-PID | 온도·압력·산소·비율 제어 | 공통 시스템 |  | 자료에서 확인 |
| SYS-RECIPES | 레시피·설정값 관리 | 공통 시스템 |  | 자료에서 확인 |
| SYS-SIMULATION | 기존 시험·시뮬레이션 블록 | 공통 시스템 |  | 자료에서 확인 |
| SYS-RUNHOURS | 모터 운전시간·정비 이력 | 공통 시스템 |  | 자료에서 확인 |
| SYS-COUNTERS | 생산량·가스·유량 계수 | 공통 시스템 |  | 자료에서 확인 |
| SYS-LEGACY | 과거 태그·이름 대응 | 공통 시스템 |  | 자료에서 확인 |

## BC01 · 드럼 투입 컨베이어

원료를 PV01 투입 게이트까지 이송한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 18 / PDF 19, FG 19 / PDF 20.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I0.1 | bc01_all_inv | bool | alarm motor bc-01 | 950 |
| %I0.0 | bc01_fbk | bool | feedback motor bc-01 | 951 |
| %I6.2 | bc01_tripwire | bool | limit switch ss-01 | 952 |
| %I6.3 | bc01_prox | bool | limit switch ssl-01 | 973 |
| %M180.7 | memocmd_bc01_startup | bool |  | 1173 |
| %Q0.0 | start bc01 | bool | a 48.1 bc-01 motorcommand | 1343 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| BC_01\RispostaA | DB11,X0.0 | PLC | 00328 |
| BC_01\Flag | DB2,X0.0 | PLC | 001B4 |
| BC_01\Allarme1 | DB11,X0.1 | PLC | 00038 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 17 | bc-01 | [네트워크 1018](networks/network-1018.html) | 7/18 |
| time work motor | 47 |  | [네트워크 1048](networks/network-1048.html) | 6/17 |
| simulation | 4 | motors simulated | [네트워크 1082](networks/network-1082.html) | 14/22 |
| hmi | 1 | bc01 | [네트워크 1178](networks/network-1178.html) | 1/9 |
| analog output conversion | 14 | bc01 | [네트워크 1692](networks/network-1692.html) | 6/16 |
| analog input conversion | 38 | bc-01 | [네트워크 1768](networks/network-1768.html) | 2/9 |
| allarms 1 | 5 | bc01 | [네트워크 1785](networks/network-1785.html) | 16/28 |
| allarms 1 | 6 | bc01 | [네트워크 1786](networks/network-1786.html) | 7/13 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| motors 1 | 3 | bwf01 | [네트워크 1932](networks/network-1932.html) | 11/21 |
| motors 1 | 4 | bwf02 | [네트워크 1933](networks/network-1933.html) | 11/21 |
| motors 1 | 5 | bwf01/02 | [네트워크 1934](networks/network-1934.html) | 17/29 |
| motors 1 | 6 | bc01 | [네트워크 1935](networks/network-1935.html) | 13/23 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1018 | Move | hours motors.BC_01_HOUR | ((Tag_47 AND BC01_Fbk) AND [hours motors.BC_01_MIN >= 60]) | Move 입력 1 |
| 1018 | Move | hours motors.BC_01_MIN | Move UID 1118.eno (블록 동작 확인) | Move 입력 0 |
| 1018 | SCoil | Flag_Aggiorna_DB | Move UID 1121.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1692 | Move | HMI_DB.SET_PERC_BC01 | (ON AND [HMI_DB.SET_PERC_BC01 < 10]) | Move 입력 10 |
| 1692 | Move | HMI_DB.SET_PERC_BC01 | (ON AND [HMI_DB.SET_PERC_BC01 > 100]) | Move 입력 100 |
| 1785 | SdCoil | Tag_51 | (((ON AND Start BC01) AND NOT [Inputs.BC01 run]) OR ((ON AND Start BC01) AND Inputs.BC01_All_inv)) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1785 | SCoil | Allarm.BC_01_FAULT | (((ON AND Start BC01) AND Tag_51) AND NOT [Inputs.BC01 run]) | 조건 성립 시 Set |
| 1785 | SCoil | Allarm.BC01_INV | (((ON AND Start BC01) AND Tag_51) AND Inputs.BC01_All_inv) | 조건 성립 시 Set |
| 1785 | RCoil | Allarm.BC_01_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.BC_01_FAULT) | 조건 성립 시 Reset |
| 1785 | RCoil | Allarm.BC01_INV | ((ON AND Flag.RESET_ALLARM) AND Allarm.BC01_INV) | 조건 성립 시 Reset |
| 1786 | SCoil | Allarm.BC_01_FC | (ON AND Inputs.BC01 trip wire) | 조건 성립 시 Set |
| 1786 | RCoil | Allarm.BC_01_FC | (((ON AND Flag.RESET_ALLARM) AND NOT [Inputs.BC01 trip wire]) AND Allarm.BC_01_FC) | 조건 성립 시 Reset |
| 1935 | RCoil | Flag.M_BC_01 | ((ON AND Allarm.BC_01_FAULT) OR (ON AND Allarm.BC01_INV) OR ((ON AND Allarm.BC_01_FC) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1935 | Coil | Start BC01 | (((ON AND Flag.M_BC_01) AND Flag.R1_GATE_LOOP_ON) OR ((ON AND Flag.M_BC_01) AND MemoCMD_BC01_Startup) OR ((ON AND Flag.M_BC_01) AND Flag.Maintenance_ON)) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| BC01-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| BC01-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| BC01-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| BC01-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| BC01-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| BC01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| BC01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| BC01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| BC01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| BC01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## RD01 · 회전 드럼

원료의 회전·체류를 담당한다. 투입·배출 게이트와 함께 운전 조건을 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 20 / PDF 21, FG 21 / PDF 22.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I0.3 | rd01_all_inv | bool | alarm motor rd-01 | 953 |
| %Q0.2 | start fan rd01 | bool | a 48.6 rd-01f motorcommand | 1339 |
| %Q0.1 | start rd01 | bool | a 48.5 rd-01 motorcommand | 1341 |
| %QW290 | rd01_sp_speed | word | rotating drum rd-01 | 1354 |
| %IW332 | rd01_current | int | rotating drum current | 1525 |
| %I0.2 | rd01_fbk | bool | feedback motor rd-01 | 1653 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| RD_01_FAN\Allarme1 | DB11,X4.1 | PLC | 0044B |
| RD_01\Allarme1 | DB11,X2.1 | PLC | 00449 |
| Editor_RD01 | DB26,INT12 | PLC | 00415 |
| RD_01\RispostaA | DB11,X2.0 | PLC | 00327 |
| RD_01_FAN\RispostaA | DB11,X4.0 | PLC | 00326 |
| RD_01\Flag | DB2,X0.1 | PLC | 001B3 |
| RD_01_FAN\Flag | DB2,X0.2 | PLC | 001B2 |
| I_RD01_ABSORBPTION | DB13,INT64 | PLC | 0002C |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 18 | rd-01 | [네트워크 1019](networks/network-1019.html) | 7/18 |
| time work motor | 19 | rd-01 fan | [네트워크 1020](networks/network-1020.html) | 7/18 |
| time work motor | 48 |  | [네트워크 1049](networks/network-1049.html) | 6/17 |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| simulation | 4 | motors simulated | [네트워크 1082](networks/network-1082.html) | 14/22 |
| hmi | 2 | rd01 | [네트워크 1179](networks/network-1179.html) | 1/9 |
| hmi | 3 | rd01 fan | [네트워크 1180](networks/network-1180.html) | 1/9 |
| analog output conversion | 6 | rd-01 cylinder | [네트워크 1684](networks/network-1684.html) | 6/16 |
| analog input conversion | 41 | rd-01 | [네트워크 1771](networks/network-1771.html) | 2/9 |
| allarms 1 | 7 | rd01 | [네트워크 1787](networks/network-1787.html) | 16/28 |
| allarms 1 | 8 | fan rd01 | [네트워크 1788](networks/network-1788.html) | 10/19 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| burner control | 4 | start gas test | [네트워크 1857](networks/network-1857.html) | 12/23 |
| motors 1 | 2 | block load | [네트워크 1931](networks/network-1931.html) | 11/21 |
| motors 1 | 3 | bwf01 | [네트워크 1932](networks/network-1932.html) | 11/21 |
| motors 1 | 4 | bwf02 | [네트워크 1933](networks/network-1933.html) | 11/21 |
| motors 1 | 5 | bwf01/02 | [네트워크 1934](networks/network-1934.html) | 17/29 |
| motors 1 | 7 | rd01 | [네트워크 1936](networks/network-1936.html) | 12/23 |
| motors 1 | 9 | rd01 | [네트워크 1938](networks/network-1938.html) | 9/18 |
| motors 1 | 10 | rd01 fan | [네트워크 1939](networks/network-1939.html) | 9/16 |
| motors 1 | 26 | fn06 | [네트워크 1955](networks/network-1955.html) | 8/14 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1019 | Move | hours motors.RD_01_HOUR | ((Tag_47 AND RD01_Fbk) AND [hours motors.RD_01_MIN >= 60]) | Move 입력 1 |
| 1019 | Move | hours motors.RD_01_MIN | Move UID 1172.eno (블록 동작 확인) | Move 입력 0 |
| 1019 | SCoil | Flag_Aggiorna_DB | Move UID 1175.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1020 | Move | hours motors.RD_01_FAN_HOUR | ((Tag_47 AND RD01F_Fbk) AND [hours motors.RD_01_FAN_MIN >= 60]) | Move 입력 1 |
| 1020 | Move | hours motors.RD_01_FAN_MIN | Move UID 1226.eno (블록 동작 확인) | Move 입력 0 |
| 1020 | SCoil | Flag_Aggiorna_DB | Move UID 1229.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1684 | Move | Data.SET_PERC_FR01 | (ON AND [Data.SET_PERC_FR01 < 5]) | Move 입력 5 |
| 1684 | Move | Data.SET_PERC_FR01 | (ON AND [Data.SET_PERC_FR01 > 100]) | Move 입력 100 |
| 1787 | SdCoil | Tag_54 | (((ON AND Start RD01) AND NOT [Inputs.RD01 run]) OR ((ON AND Start RD01) AND Inputs.RD01_All_inv)) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#5S |
| 1787 | SCoil | Allarm.RD_01_FAULT | (((ON AND Start RD01) AND Tag_54) AND NOT [Inputs.RD01 run]) | 조건 성립 시 Set |
| 1787 | SCoil | Allarm.RD01_INV | (((ON AND Start RD01) AND Tag_54) AND Inputs.RD01_All_inv) | 조건 성립 시 Set |
| 1787 | RCoil | Allarm.RD_01_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.RD_01_FAULT) | 조건 성립 시 Reset |
| 1787 | RCoil | Allarm.RD01_INV | ((ON AND Flag.RESET_ALLARM) AND Allarm.RD01_INV) | 조건 성립 시 Reset |
| 1788 | SdCoil | Tag_55 | ((ON AND Start fan RD01) AND NOT [Inputs.fan RD01 run]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1788 | SCoil | Allarm.RD_01_FAN_FAULT | (((ON AND Start fan RD01) AND Tag_55) AND NOT [Inputs.fan RD01 run]) | 조건 성립 시 Set |
| 1788 | RCoil | Allarm.RD_01_FAN_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.RD_01_FAN_FAULT) | 조건 성립 시 Reset |
| 1936 | RCoil | Flag.M_RD_01 | ((ON AND Allarm.RD_01_FAULT) OR (ON AND Allarm.RD01_INV) OR (ON AND [Data.SET_PERC_FR01 = 0]) OR (ON AND NOT [Inputs.fan RD01 run]) OR (((ON AND NOT [Flag.R2_GATE_LOOP_ON]) AND NOT [Flag.STANDBY_ON]) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1936 | Coil | Start RD01 | (ON AND Flag.M_RD_01) | 조건에 따른 Coil 기록 |
| 1938 | SdCoil | Tag_116 | ((ON AND Start RD01) AND NOT [Tag_115]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 Data.EVFR01_Work_time |
| 1938 | SdCoil | Tag_115 | ((ON AND Start RD01) AND Tag_116) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 Data.EVFR01_Wait_time |
| 1938 | Coil | EV03 | (((ON AND Start RD01) AND NOT [Tag_116]) AND ON) | 조건에 따른 Coil 기록 |
| 1939 | RCoil | Flag.M_RD_01_FAN | ((ON AND Allarm.RD_01_FAN_FAULT) OR (((ON AND NOT [Flag.R2_GATE_LOOP_ON]) AND NOT [Flag.STANDBY_ON]) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1939 | Coil | Start fan RD01 | (ON AND Flag.M_RD_01_FAN) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| RD01-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| RD01-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| RD01-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| RD01-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| RD01-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| RD01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| RD01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| RD01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| RD01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| RD01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## RD01-FAN · 드럼 모터 냉각팬

RD01 구동 모터 냉각 보조장치.

자료 상태: 자료에서 확인. 상위: RD01. 전기: FG 22 / PDF 23.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I0.4 | rd01f_fbk | bool | feedback motor rd-01f | 954 |
| %Q0.2 | start fan rd01 | bool | a 48.6 rd-01f motorcommand | 1339 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| RD_01_FAN\Allarme1 | DB11,X4.1 | PLC | 0044B |
| RD_01_FAN\RispostaA | DB11,X4.0 | PLC | 00326 |
| RD_01_FAN\Flag | DB2,X0.2 | PLC | 001B2 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 19 | rd-01 fan | [네트워크 1020](networks/network-1020.html) | 7/18 |
| time work motor | 48 |  | [네트워크 1049](networks/network-1049.html) | 6/17 |
| simulation | 4 | motors simulated | [네트워크 1082](networks/network-1082.html) | 14/22 |
| hmi | 3 | rd01 fan | [네트워크 1180](networks/network-1180.html) | 1/9 |
| allarms 1 | 8 | fan rd01 | [네트워크 1788](networks/network-1788.html) | 10/19 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| motors 1 | 7 | rd01 | [네트워크 1936](networks/network-1936.html) | 12/23 |
| motors 1 | 10 | rd01 fan | [네트워크 1939](networks/network-1939.html) | 9/16 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1788 | SdCoil | Tag_55 | ((ON AND Start fan RD01) AND NOT [Inputs.fan RD01 run]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1788 | SCoil | Allarm.RD_01_FAN_FAULT | (((ON AND Start fan RD01) AND Tag_55) AND NOT [Inputs.fan RD01 run]) | 조건 성립 시 Set |
| 1788 | RCoil | Allarm.RD_01_FAN_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.RD_01_FAN_FAULT) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| RD01-FAN-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| RD01-FAN-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| RD01-FAN-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| RD01-FAN-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| RD01-FAN-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| RD01-FAN-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| RD01-FAN-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| RD01-FAN-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| RD01-FAN-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| RD01-FAN-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## MC03 · 예비 모터 MC03

PLC의 예비 모터 및 토크 감시 항목.

자료 상태: 예비·실물 동일성 확인. 상위: 해당 없음. 전기: FG 23 / PDF 24.

확인할 특이점:  P&ID에서 주설비 태그로 확인되지 않는다. Q0.3과 MC03/SS09 참조를 별도 예비 장치로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I6.4 | mc03_torque | bool | limit switch ss-09 | 936 |
| %Q0.3 | start spare motor | bool | a 48.7 spare motorcommand | 1337 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 20 | mc-03 | [네트워크 1021](networks/network-1021.html) | 7/18 |
| time work motor | 48 |  | [네트워크 1049](networks/network-1049.html) | 6/17 |
| simulation | 4 | motors simulated | [네트워크 1082](networks/network-1082.html) | 14/22 |
| hmi | 4 | spare motor | [네트워크 1181](networks/network-1181.html) | 1/9 |
| allarms 1 | 9 | spare motor | [네트워크 1789](networks/network-1789.html) | 10/19 |
| allarms 1 | 10 | spare motor | [네트워크 1790](networks/network-1790.html) | 7/13 |
| motors 1 | 11 | mc03 spare motor | [네트워크 1940](networks/network-1940.html) | 10/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1021 | Move | hours motors.MC_03_HOUR | ((Tag_47 AND 102A7_SPARE5) AND [hours motors.MC_03_MIN >= 60]) | Move 입력 1 |
| 1021 | Move | hours motors.MC_03_MIN | Move UID 1280.eno (블록 동작 확인) | Move 입력 0 |
| 1021 | SCoil | Flag_Aggiorna_DB | Move UID 1283.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1789 | SdCoil | Tag_56 | ((OFF AND Start Spare Motor) AND NOT [Inputs.MC03 run]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1789 | SCoil | Allarm.MC_03_FAULT | (((OFF AND Start Spare Motor) AND Tag_56) AND NOT [Inputs.MC03 run]) | 조건 성립 시 Set |
| 1789 | RCoil | Allarm.MC_03_FAULT | ((OFF AND Flag.RESET_ALLARM) AND Allarm.MC_03_FAULT) | 조건 성립 시 Reset |
| 1790 | SCoil | Allarm.MC_03_TORQUE | (OFF AND NOT [Inputs.MC03 torque]) | 조건 성립 시 Set |
| 1790 | RCoil | Allarm.MC_03_TORQUE | (((OFF AND Flag.RESET_ALLARM) AND Inputs.MC03 torque) AND Allarm.MC_03_TORQUE) | 조건 성립 시 Reset |
| 1940 | RCoil | Flag.M_MC_03 | ((ON AND Allarm.MC_03_FAULT) OR ((ON AND NOT [Inputs.MC04 run]) AND NOT [Flag.STANDBY_ON]) OR ((ON AND Allarm.MC_03_TORQUE) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1940 | Coil | Start Spare Motor | (ON AND Flag.M_MC_03) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| MC03-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| MC03-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| MC03-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| MC03-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| MC03-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| MC03-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| MC03-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| MC03-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| MC03-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| MC03-V-05 | 불일치/특이점 | P&ID에서 주설비 태그로 확인되지 않는다. Q0.3과 MC03/SS09 참조를 별도 예비 장치로 보관한다. | 확인 대기 |

## MC04 · 금속 컨베이어

PV02 배출 원료를 VS01 방향으로 이송한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 24 / PDF 25, FG 25 / PDF 26.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I0.7 | mc04_all_inv | bool | feedback motor mc-04 | 916 |
| %I0.6 | mc04_fbk | bool | feedback motor mc-04 | 958 |
| %I6.5 | mc04_torque | bool | limit switch ss-10 | 1097 |
| %Q0.4 | start mc04 | bool | a 49.1 mc-04 motorcommand | 1335 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| MC_04\Allarme1 | DB11,X8.1 | PLC | 0043A |
| MC_04\RispostaA | DB11,X8.0 | PLC | 00324 |
| MC_04\Flag | DB2,X0.4 | PLC | 001B0 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 21 | mc-04 | [네트워크 1022](networks/network-1022.html) | 7/18 |
| time work motor | 48 |  | [네트워크 1049](networks/network-1049.html) | 6/17 |
| simulation | 2 |  | [네트워크 1080](networks/network-1080.html) | 7/9 |
| simulation | 4 | motors simulated | [네트워크 1082](networks/network-1082.html) | 14/22 |
| hmi | 5 | mc04 | [네트워크 1182](networks/network-1182.html) | 1/9 |
| analog output conversion | 15 | mc04 | [네트워크 1693](networks/network-1693.html) | 6/16 |
| analog input conversion | 39 | mc04 | [네트워크 1769](networks/network-1769.html) | 2/9 |
| allarms 1 | 11 | mc04 | [네트워크 1791](networks/network-1791.html) | 16/28 |
| allarms 1 | 12 | mc04 deleted | [네트워크 1792](networks/network-1792.html) | 7/13 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| r1 scraps gate 2 | 6 | pv-02 rotary drum discharge valve | [네트워크 1916](networks/network-1916.html) | 20/33 |
| motors 1 | 11 | mc03 spare motor | [네트워크 1940](networks/network-1940.html) | 10/18 |
| motors 1 | 12 | mc04 | [네트워크 1941](networks/network-1941.html) | 9/16 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1022 | Move | hours motors.MC_04_HOUR | ((Tag_47 AND MC04_Fbk) AND [hours motors.MC_04_MIN >= 60]) | Move 입력 1 |
| 1022 | Move | hours motors.MC_04_MIN | Move UID 1334.eno (블록 동작 확인) | Move 입력 0 |
| 1022 | SCoil | Flag_Aggiorna_DB | Move UID 1337.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1693 | Move | HMI_DB.SET_PERC_MC04 | (ON AND [HMI_DB.SET_PERC_MC04 < 10]) | Move 입력 10 |
| 1693 | Move | HMI_DB.SET_PERC_MC04 | (ON AND [HMI_DB.SET_PERC_MC04 > 100]) | Move 입력 100 |
| 1791 | SdCoil | Tag_57 | (((ON AND Start MC04) AND Inputs.MC04_All_inv) OR ((ON AND Start MC04) AND NOT [Inputs.MC04 run])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#5S |
| 1791 | SCoil | Allarm.MC_04_FAULT | (((ON AND Start MC04) AND Tag_57) AND NOT [Inputs.MC04 run]) | 조건 성립 시 Set |
| 1791 | SCoil | Allarm.MC04_INV | (((ON AND Start MC04) AND Tag_57) AND Inputs.MC04_All_inv) | 조건 성립 시 Set |
| 1791 | RCoil | Allarm.MC_04_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.MC_04_FAULT) | 조건 성립 시 Reset |
| 1791 | RCoil | Allarm.MC04_INV | ((ON AND Flag.RESET_ALLARM) AND Allarm.MC04_INV) | 조건 성립 시 Reset |
| 1792 | SCoil | Allarm.MC_04_TORQUE | (OFF AND NOT [Inputs.MC04 torque]) | 조건 성립 시 Set |
| 1792 | RCoil | Allarm.MC_04_TORQUE | (((OFF AND Flag.RESET_ALLARM) AND Inputs.MC04 torque) AND Allarm.MC_04_TORQUE) | 조건 성립 시 Reset |
| 1941 | RCoil | Flag.M_MC_04 | ((ON AND Allarm.MC_04_FAULT) OR (ON AND Allarm.MC04_INV) OR ((ON AND NOT [Inputs.VS01 run]) AND NOT [Allarm.Maintenance_ON])) | 조건 성립 시 Reset |
| 1941 | Coil | Start MC04 | (ON AND Flag.M_MC_04) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| MC04-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| MC04-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| MC04-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| MC04-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| MC04-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| MC04-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| MC04-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| MC04-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| MC04-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| MC04-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## MC05 · 금속 컨베이어 MC05

전기도면과 PLC 입출력에는 남아 있는 이송 장치.

자료 상태: 삭제 제목·예비 여부 확인. 상위: 해당 없음. 전기: FG 26 / PDF 27.

확인할 특이점:  Motors 1에는 mc05 deleted 제목이 있다. 입출력과 도면의 잔존만으로 현재 설치·사용 상태를 결정하지 않는다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I6.6 | mc05_torque | bool | limit switch ss-11 | 937 |
| %Q0.5 | start mc05 | bool | a 49.2 mc-05 motorcommand | 975 |
| %I1.0 | mc05_fbk | bool | feedback motor mc-05 | 976 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| MC_05\RispostaA | DB11,X10.0 | PLC | 00323 |
| MC_05\Flag | DB2,X0.5 | PLC | 001AF |
| MC_05\Allarme1 | DB11,X10.1 | PLC | 0003F |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 48 |  | [네트워크 1049](networks/network-1049.html) | 6/17 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |

### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| MC05-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| MC05-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| MC05-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| MC05-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| MC05-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| MC05-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| MC05-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| MC05-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| MC05-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| MC05-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |
| MC05-V-06 | 불일치/특이점 | Motors 1에는 mc05 deleted 제목이 있다. 입출력과 도면의 잔존만으로 현재 설치·사용 상태를 결정하지 않는다. | 확인 대기 |

## VS01 · 진동 스크린

배출 원료를 선별한다. VS01/VS01A 공통 피드백을 분리 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 27 / PDF 28, FG 28 / PDF 29.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M11.0 | start vs01 brake | bool |  | 58 |
| %Q49.5 | braking vs01 | bool | it's no longer there | 461 |
| %I1.1 | vs01_fbk | bool | feedback motor vs-01/vs-01a | 493 |
| %I1.2 | vs01_all_inv | bool | alarm motor vs-01/vs-01a | 917 |
| %Q0.6 | start vs01 | bool | a 49.0 vs-01/vs-01amotor command | 1333 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| VS_01\RispostaA | DB11,X12.0 | PLC | 00322 |
| VS_01\Flag | DB2,X0.6 | PLC | 001AE |
| VS_01\Allarme1 | DB11,X12.1 | PLC | 0003D |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 23 | vs-01 | [네트워크 1024](networks/network-1024.html) | 7/18 |
| time work motor | 49 |  | [네트워크 1050](networks/network-1050.html) | 6/17 |
| simulation | 4 | motors simulated | [네트워크 1082](networks/network-1082.html) | 14/22 |
| hmi | 7 | vs01 | [네트워크 1184](networks/network-1184.html) | 1/9 |
| allarms 1 | 14 | vs01 | [네트워크 1794](networks/network-1794.html) | 16/28 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| motors 1 | 12 | mc04 | [네트워크 1941](networks/network-1941.html) | 9/16 |
| motors 1 | 14 | vs01 | [네트워크 1943](networks/network-1943.html) | 7/12 |
| motors 1 | 15 | vs01 brake (off) | [네트워크 1944](networks/network-1944.html) | 15/27 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1024 | Move | hours motors.VS_01_HOUR | ((Tag_47 AND VS01_Fbk) AND [hours motors.VS_01_MIN >= 60]) | Move 입력 1 |
| 1024 | Move | hours motors.VS_01_MIN | Move UID 1442.eno (블록 동작 확인) | Move 입력 0 |
| 1024 | SCoil | Flag_Aggiorna_DB | Move UID 1445.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1794 | SdCoil | Tag_59 | (((ON AND Start VS01) AND NOT [Inputs.VS01 run]) OR ((ON AND Start VS01) AND Inputs.VS01_All_Inv)) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1794 | SCoil | Allarm.VS_01_FAULT | (((ON AND Start VS01) AND Tag_59) AND NOT [Inputs.VS01 run]) | 조건 성립 시 Set |
| 1794 | SCoil | Allarm.VS01_INV | (((ON AND Start VS01) AND Tag_59) AND Inputs.VS01_All_Inv) | 조건 성립 시 Set |
| 1794 | RCoil | Allarm.VS_01_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.VS_01_FAULT) | 조건 성립 시 Reset |
| 1794 | RCoil | Allarm.VS01_INV | ((ON AND Flag.RESET_ALLARM) AND Allarm.VS01_INV) | 조건 성립 시 Reset |
| 1943 | RCoil | Flag.M_VS_01 | ((ON AND Allarm.VS_01_FAULT) OR (ON AND Allarm.VS01_INV)) | 조건 성립 시 Reset |
| 1943 | Coil | Start VS01 | (ON AND Flag.M_VS_01) | 조건에 따른 Coil 기록 |
| 1944 | SCoil | Start VS01 BRAKE | (((OFF AND NOT [Flag.M_VS_01]) AND NOT [Inputs.VS01 run]) AND NOT [Allarm.VS_01_FAULT]) | 조건 성립 시 Set |
| 1944 | RCoil | Start VS01 BRAKE | ((OFF AND Flag.M_VS_01) OR (OFF AND Allarm.VS_01_FAULT) OR (OFF AND Allarm.VS01_INV)) | 조건 성립 시 Reset |
| 1944 | SdCoil | Tag_117 | ((OFF AND NOT [Inputs.VS01 run]) AND Start VS01 BRAKE) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1944 | Coil | Braking VS01 | (((OFF AND NOT [Inputs.VS01 run]) AND Start VS01 BRAKE) AND Tag_117) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| VS01-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| VS01-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| VS01-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| VS01-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| VS01-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| VS01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| VS01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| VS01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| VS01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| VS01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## SC12 · 드럼 배출실 스크루

드럼 배출실 측 원료 배출 스크루.

자료 상태: SPARE·삭제 제목. 상위: 해당 없음. 전기: FG 29 / PDF 30.

확인할 특이점: 전기 FG29는 SPARE이며 PLC Motors 1에는 sc12 deleted 제목과 잔존 I1.3/Q0.7이 있다. 이는 삭제된 네트워크라는 제목을 뜻하며, 검색 문서 자체가 삭제 상태라는 뜻과 구분한다. P&ID에 존재하지만 전기 회로 SPARE와 sc12 deleted 제목이 확인됐다. 설치 상태와 유지되는 배선을 확인한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I1.3 | sc12_fbk | bool | feedback motor sc-12 | 979 |
| %Q0.7 | start sc12 | bool | a 48.0 sc-12 motorcommand | 980 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| SC_12\RispostaA | DB11,X14.0 | PLC | 00321 |
| SC_12\Flag | DB2,X0.7 | PLC | 001AD |
| SC_12\Allarme1 | DB11,X14.1 | PLC | 0003B |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 49 |  | [네트워크 1050](networks/network-1050.html) | 6/17 |

### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SC12-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| SC12-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| SC12-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| SC12-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| SC12-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SC12-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SC12-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SC12-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SC12-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| SC12-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |
| SC12-V-06 | 불일치/특이점 | P&ID에 존재하지만 전기 회로 SPARE와 sc12 deleted 제목이 확인됐다. 설치 상태와 유지되는 배선을 확인한다. | 확인 대기 |

## CC01 · 드럼 투입실

PV01과 RD01 입구 사이의 투입 챔버. 기밀·퇴적·게이트 간섭을 점검한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 기계·공정 상태: 본체의 누설·기밀·퇴적·마모·부식, 입출구 막힘, 점검구와 연결 배관 상태를 기록한다.
2. 연관 장치: 주변 모터·밸브·온도/압력/레벨 계측의 운전 상태와 본체 공정 상태를 연결해 검토한다.
3. 도면 동일성: P&ID의 위치와 실제 본체·배관·전기도면 장치의 태그를 대조하고 변경 사항을 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CC01-SIM-01 | 공정 이상 모델 | 막힘·누설·퇴적을 연관 신호로 모델링 | 본체 직접 I/O가 없으면 연관 장치 영향으로 판정 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CC01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CC01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CC01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## UC01 · 드럼 배출실

RD01 출구, PV02 및 배출 경로를 구성하는 챔버.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 기계·공정 상태: 본체의 누설·기밀·퇴적·마모·부식, 입출구 막힘, 점검구와 연결 배관 상태를 기록한다.
2. 연관 장치: 주변 모터·밸브·온도/압력/레벨 계측의 운전 상태와 본체 공정 상태를 연결해 검토한다.
3. 도면 동일성: P&ID의 위치와 실제 본체·배관·전기도면 장치의 태그를 대조하고 변경 사항을 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| UC01-SIM-01 | 공정 이상 모델 | 막힘·누설·퇴적을 연관 신호로 모델링 | 본체 직접 I/O가 없으면 연관 장치 영향으로 판정 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| UC01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| UC01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| UC01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## AB01 · 연소 챔버

BR01의 연소와 TC01/02 온도 감시가 연결되는 공정 챔버.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW274 | tc02 | int | safety temperature chamber ab-01 | 1545 |
| %IW272 | tc01 | int | temperature chamber ab-01 | 1546 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 기계·공정 상태: 본체의 누설·기밀·퇴적·마모·부식, 입출구 막힘, 점검구와 연결 배관 상태를 기록한다.
2. 연관 장치: 주변 모터·밸브·온도/압력/레벨 계측의 운전 상태와 본체 공정 상태를 연결해 검토한다.
3. 도면 동일성: P&ID의 위치와 실제 본체·배관·전기도면 장치의 태그를 대조하고 변경 사항을 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| AB01-SIM-01 | 공정 이상 모델 | 막힘·누설·퇴적을 연관 신호로 모델링 | 본체 직접 I/O가 없으면 연관 장치 영향으로 판정 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| AB01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| AB01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| AB01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| AB01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## BR01 · 가스 버너

연소 상태·락아웃·가스/공기 조건·변조 값을 외부 버너 시스템과 교환한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 97 / PDF 98, FG 98 / PDF 99, FG 99 / PDF 100, FG 100 / PDF 101.

확인할 특이점: 현재 자료는 외부 버너의 PLC 인터페이스와 일반 제어 블록을 제공한다. 상세 안전 회로 및 버너 자체 제어 시퀀스의 실제 내용은 제조사 버너 도면으로 확정한다. 버너 전용 상세 도면 및 제조사 연소 제어 절차는 별도 문서가 필요하다. 이 매뉴얼의 일반 PLC 해석을 버너 안전 시퀀스로 대체하지 않는다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M48.3 | start burner | bool |  | 472 |
| %M1.1 | programmed stop burner | bool |  | 477 |
| %I17.0 | burner on | bool | e 44.7 burner on | 906 |
| %I17.1 | brurner lock out | bool | e 44.6 burner lockout | 907 |
| %I17.2 | burner on and ok | bool | e 44.1 burner inmodulation | 908 |
| %Q6.7 | rst allarm burner | bool | a 56.2 reset alarmburner | 911 |
| %M28.0 | lock burner | bool |  | 1060 |
| %M48.2 | enable start burner | bool |  | 1061 |
| %Q6.5 | rem. start/stop burner | bool | a 56.1 remote start/stopburner | 1062 |
| %M180.5 | close mv03 for burner startup | bool |  | 1096 |
| %M48.0 | enable start burner(1) | bool |  | 1275 |
| %QW308 | br01_gas_sp | word | flame modulation gas floating motor br-01(4-20ma) | 1351 |
| %QW310 | br01_air_sp | word | flame modulation air floating motor br-01(4-20ma) | 1352 |
| %IW366 | br01_flowmeter_air | int | air outlet br-01 | 1530 |
| %IW364 | br01_flowmeter_gas | int | gas outlet br-01 | 1531 |
| %IW362 | br01_air | int | air servo-motor br-01 | 1532 |
| %IW360 | br01_gas | int | gas servo-motor br-01 | 1533 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| RESET_BURNER_COUNT | DB41,X50.1 | PLC | 00466 |
| BR_01\HighFlame | DB11,X84.0 | PLC | 00389 |
| BR_01\BurnerON | DB11,X84.1 | PLC | 00387 |
| BR_01\Flag | DB2,X5.2 | PLC | 00386 |
| BR_01\Auto | DB2,X4.3 | PLC | 00385 |
| Burner_ready | DB2,X5.1 | PLC | 00375 |
| I_BR_01_RETRANSMISSION_AIR | DB13,INT78 | PLC | 00035 |
| I_BR_01_RETRANSMISSION_GAS | DB13,INT76 | PLC | 00034 |
| I_BR_01_MASSFLOWMETER_GAS | DB13,INT80 | PLC | 00027 |
| I_BR_01_MASSFLOWMETER_AIR | DB13,INT82 | PLC | 00026 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| simulation | 14 |  | [네트워크 1092](networks/network-1092.html) | 18/42 |
| hmi | 42 | br-01 | [네트워크 1219](networks/network-1219.html) | 4/7 |
| main | 9 | motors valve and burner | [네트워크 1620](networks/network-1620.html) | 7/3 |
| analog output conversion | 8 | br01 burner | [네트워크 1686](networks/network-1686.html) | 8/20 |
| analog output conversion | 9 | br01 burner - gas | [네트워크 1687](networks/network-1687.html) | 8/21 |
| valve control loop | 5 | mv03 controlled by psh03 | [네트워크 1706](networks/network-1706.html) | 41/73 |
| cyc_int2 ogni 1s | 3 |  | [네트워크 1721](networks/network-1721.html) | 5/12 |
| cyc_int2 ogni 1s | 4 |  | [네트워크 1722](networks/network-1722.html) | 2/6 |
| cyc_int2 ogni 1s | 6 | delayed burner flow rate variation | [네트워크 1724](networks/network-1724.html) | 5/15 |
| analog input conversion | 22 | gas br-01 - position | [네트워크 1752](networks/network-1752.html) | 2/9 |
| analog input conversion | 23 | air br-01 - position | [네트워크 1753](networks/network-1753.html) | 2/9 |
| analog input conversion | 24 | max flow gas - flowmeter | [네트워크 1754](networks/network-1754.html) | 4/14 |
| analog input conversion | 25 | max flow air - flowmeter | [네트워크 1755](networks/network-1755.html) | 2/9 |
| control_stechio | 1 | calculate the gas flow rate based on the theoretical ramp | [네트워크 1830](networks/network-1830.html) | 41/103 |
| control_stechio | 5 | verify range sent by gas | [네트워크 1834](networks/network-1834.html) | 5/13 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| burner control | 1 | burner control box fault | [네트워크 1854](networks/network-1854.html) | 20/34 |
| burner control | 2 | burner servomotor not in minimal position | [네트워크 1855](networks/network-1855.html) | 10/18 |
| burner control | 4 | start gas test | [네트워크 1857](networks/network-1857.html) | 12/23 |
| burner control | 5 | burner stop | [네트워크 1858](networks/network-1858.html) | 21/40 |
| burner control | 6 | counter minutes of burner work | [네트워크 1859](networks/network-1859.html) | 9/20 |
| burner control | 7 | counter burner off during preheating or production | [네트워크 1860](networks/network-1860.html) | 21/44 |
| burner control | 8 | programmed burner shutdown every 24 hours | [네트워크 1861](networks/network-1861.html) | 5/11 |
| burner control | 9 | a 56.6 start high flameburner | [네트워크 1862](networks/network-1862.html) | 25/51 |
| burner control | 10 | enable relay forceed spark | [네트워크 1863](networks/network-1863.html) | 13/23 |
| burner control | 12 | burner lock | [네트워크 1865](networks/network-1865.html) | 17/31 |
| burner control | 13 | burner start sequence | [네트워크 1866](networks/network-1866.html) | 9/16 |
| burner control | 14 | for viewing washing time in supervisor | [네트워크 1867](networks/network-1867.html) | 5/12 |
| burner control | 15 | enable burner cleaning sequence | [네트워크 1868](networks/network-1868.html) | 71/151 |
| burner control | 16 | burner start fault reset | [네트워크 1869](networks/network-1869.html) | 3/6 |
| burner control | 17 | burner servomotor control fb41 pid mode | [네트워크 1870](networks/network-1870.html) | 15/29 |
| burner control | 18 | if on auto send pid result to the module | [네트워크 1871](networks/network-1871.html) | 2/6 |
| burner control | 19 | burner air range limits | [네트워크 1872](networks/network-1872.html) | 14/32 |
| burner control | 20 | simulation | [네트워크 1873](networks/network-1873.html) | 2/5 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1219 | Coil | ORef UID 28 | ORef UID 24 | 조건에 따른 Coil 기록 |
| 1219 | Coil | ORef UID 35 | ORef UID 31 | 조건에 따른 Coil 기록 |
| 1686 | Move | Data.Burner_Air_Out | (ON AND [Data.Burner_Air_Out < 0]) | Move 입력 0 |
| 1686 | Move | Data.Burner_Air_Out | (ON AND [Data.Burner_Air_Out > 100]) | Move 입력 100 |
| 1686 | Move | BR01_AIR_SP | ON | Move 입력 Calcolo_Aria |
| 1687 | Move | Data.Burner_Gas_Out | (ON AND [Data.Burner_Gas_Out < 0]) | Move 입력 0 |
| 1687 | Move | Data.Burner_Gas_Out | (ON AND [Data.Burner_Gas_Out > 100]) | Move 입력 100 |
| 1687 | Move | test_out | Mul UID 590.eno (블록 동작 확인) | Move 입력 BR01_GAS_SP |
| 1854 | SCoil | Allarm.BURNER_LDU_FAULT | ((ON AND Brurner Lock Out) AND NOT [APP M10.2]) | 조건 성립 시 Set |
| 1854 | SCoil | m491 | ((ON AND Flag.RESET_ALLARM) AND Allarm.BURNER_LDU_FAULT) | 조건 성립 시 Set |
| 1854 | SCoil | APP M10.2 | ((ON AND Flag.RESET_ALLARM) AND Allarm.BURNER_LDU_FAULT) | 조건 성립 시 Set |
| 1854 | SdCoil | Tag_135 | (ON AND APP M10.2) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#6S |
| 1854 | RCoil | APP M10.2 | ((ON AND APP M10.2) AND Tag_135) | 조건 성립 시 Reset |
| 1854 | SdCoil | Tag_136 | (ON AND m491) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1854 | Coil | Rst allarm Burner | (ON AND m491) | 조건에 따른 Coil 기록 |
| 1854 | RCoil | Allarm.BURNER_LDU_FAULT | ((ON AND m491) AND Tag_136) | 조건 성립 시 Reset |
| 1854 | SdCoil | Tag_137 | ((ON AND m491) AND Tag_136) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1854 | RCoil | m491 | (((ON AND m491) AND Tag_136) AND Tag_137) | 조건 성립 시 Reset |
| 1855 | SCoil | Allarm.SERVOMOTOR_MIN_POS_ALL | ((PBox UID 239.out (블록 동작 확인) AND NOT [Inputs.FC GAS Chiuso]) OR (PBox UID 239.out (블록 동작 확인) AND NOT [Inputs.FC Aria chiusa])) | 조건 성립 시 Set |
| 1855 | RCoil | Allarm.SERVOMOTOR_MIN_POS_ALL | ((ON AND Flag.RESET_ALLARM) AND Allarm.SERVOMOTOR_MIN_POS_ALL) | 조건 성립 시 Reset |
| 1858 | RCoil | Flag.Start_Burner | ((ON AND NOT [Flag.Burner_ready]) OR (ON AND Allarm.MAX_MAX_TC09) OR (ON AND Allarm.BURNER_START_FAULT) OR (ON AND Allarm.BURNER_LDU_FAULT) OR (((ON AND Allarm.FN_03_FAULT) OR (ON AND Allarm.PSL_AIR_LOW) OR (ON AND Allarm.HYDROGEN_BOX_FAULT) OR (ON AND Allarm.EmergencyStopTC1_2) OR (ON AND Allarm.SERVOMOTOR_MIN_POS_ALL) OR (ON AND Allarm.MAX_TC04_TEMP) OR (ON AND Allarm.MAX_TC05_TEMP) OR (ON AND Allarm.MAX_MAX_TC03_TEMP) OR (ON AND Allarm.MAX_MAX_TC01_TEMP) OR (ON AND Allarm.RO01_Signal_Fault) OR (ON AND Allarm.TC01_TC02_COMP_FAULT) OR (ON AND Allarm.Low_Aspiration)) AND ON)) | 조건 성립 시 Reset |
| 1859 | SdCoil | Tag_138 | ((ON AND Inputs.Burner On) AND NOT [Tag_138]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1M |
| 1859 | Move | WorkData.W5 | (ON AND NOT [Inputs.Burner On]) | Move 입력 0 |
| 1860 | RCoil | HMI_DB.memoBurnerON | ([Data.Tipo_preset != 1] AND [Data.Tipo_preset != 2]) | 조건 성립 시 Reset |
| 1860 | SCoil | HMI_DB.memoBurnerON | (((Flag.Start_Burner OR Flag.AUTO_BURNER) AND NOT [HMI_DB.memoBurnerON]) AND Inputs.Burner On) | 조건 성립 시 Set |
| 1860 | Move | HMI_DB.Counter_StopBurner | (((Flag.Start_Burner OR Flag.AUTO_BURNER) AND NOT [HMI_DB.memoBurnerON]) AND Inputs.Burner On) | Move 입력 0 |
| 1860 | Move | Stechio.Consumo_GAS | (((Flag.Start_Burner OR Flag.AUTO_BURNER) AND NOT [HMI_DB.memoBurnerON]) AND Inputs.Burner On) | Move 입력 0.0 |
| 1860 | Move | HMI_DB.Counter_PartialProduction | (((Flag.Start_Burner OR Flag.AUTO_BURNER) AND NOT [HMI_DB.memoBurnerON]) AND Inputs.Burner On) | Move 입력 0.0 |
| 1860 | Move | HMI_DB.Counter_StopBurner | HMI_DB.ResetCounter_StopBurner | Move 입력 0 |
| 1860 | RCoil | HMI_DB.ResetCounter_StopBurner | Move UID 90.eno (블록 동작 확인) | 조건 성립 시 Reset |
| 1861 | Coil | Programmed stop burner | (OFF AND [WorkData.W5 >= 1440]) | 조건에 따른 Coil 기록 |
| 1861 | Coil | Allarm.BURNER_TIME_LIMIT_22H | (OFF AND [WorkData.W5 >= 1320]) | 조건에 따른 Coil 기록 |
| 1865 | SCoil | Lock Burner | (((((ON AND OFF) AND Allarm.MAX_TC01_TEMP) OR ((ON AND OFF) AND Allarm.MAX_TC03_TEMP) OR (ON AND Programmed stop burner)) AND [Data.GAS_BR_01 <= 30]) OR (((((ON AND OFF) AND Allarm.MAX_TC01_TEMP) OR ((ON AND OFF) AND Allarm.MAX_TC03_TEMP) OR (ON AND Programmed stop burner)) AND Inputs.FC GAS Chiuso) AND Inputs.FC Aria chiusa)) | 조건 성립 시 Set |
| 1865 | RCoil | Lock Burner | ((((ON AND NOT [Allarm.MAX_TC01_TEMP]) AND NOT [Allarm.MAX_TC03_TEMP]) OR ON) AND NOT [Programmed stop burner]) | 조건 성립 시 Reset |
| 1866 | SCoil | Flag.M_FN_03 | (((Flag.Start_Burner AND NOT [Lock Burner]) AND NOT [Flag.M_FN_03]) AND OFF) | 조건 성립 시 Set |
| 1866 | Coil | Enable start burner(1) | ((Flag.Start_Burner AND NOT [Lock Burner]) AND Inputs.FN03 Run) | 조건에 따른 Coil 기록 |
| 1866 | Coil | Rem. Start/Stop Burner | (((Flag.Start_Burner AND NOT [Lock Burner]) AND Inputs.FN03 Run) AND Enable start burner) | 조건에 따른 Coil 기록 |
| 1868 | Move | WorkData.BR01_State | (ON AND NOT [Enable start burner(1)]) | Move 입력 0 |
| 1868 | RCoil | Open MV03 for washing | (ON AND NOT [Enable start burner(1)]) | 조건 성립 시 Reset |
| 1868 | SCoil | Close MV03 for Burner Startup | (((ON AND NOT [Enable start burner(1)]) AND NOT [Inputs.MV03 Close]) AND Inputs.MV03 Close) | 조건 성립 시 Set |
| 1868 | RCoil | Enable start burner | (ON AND NOT [Enable start burner(1)]) | 조건 성립 시 Reset |
| 1868 | Move | WorkData.BR01_State | (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 0]) AND [Manage_TC1_2.PID_Ref_Temp >= 500.0]) | Move 입력 7 |
| 1868 | Move | WorkData.BR01_State | (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 0]) AND [Manage_TC1_2.PID_Ref_Temp < 500.0]) | Move 입력 1 |
| 1868 | Move | WorkData.BR01_CleanTime | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 0]) | Move 입력 0 |
| 1868 | Move | Data.Burner_Panel_SetPoint | (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 1]) AND OFF) | Move 입력 Data.Max_PRC_BR1 |
| 1868 | SCoil | Open MV03 for washing | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 1]) | 조건 성립 시 Set |
| 1868 | Move | WorkData.BR01_State | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 1]) | Move 입력 2 |
| 1868 | Move | WorkData.BR01_State | (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 2]) AND NOT [Inputs.MV03 open]) | Move 입력 3 |
| 1868 | SdCoil | Tag_143 | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 3]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#4M |
| 1868 | SdCoil | Tag_142 | ((((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 3]) AND ON) AND NOT [Tag_142]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1S |
| 1868 | Move | WorkData.BR01_State | (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 3]) AND Tag_143) | Move 입력 4 |
| 1868 | Move | Data.Burner_Panel_SetPoint | (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 4]) AND OFF) | Move 입력 0 |
| 1868 | RCoil | Open MV03 for washing | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 4]) | 조건 성립 시 Reset |
| 1868 | Move | WorkData.BR01_State | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 4]) | Move 입력 5 |
| 1868 | Move | WorkData.BR01_State | ((((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 5]) AND Inputs.MV03 Close) OR (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 5]) AND ON)) | Move 입력 6 |
| 1868 | SdCoil | Tag_144 | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 6]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1S |
| 1868 | Move | WorkData.BR01_State | (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 6]) AND Tag_144) | Move 입력 7 |
| 1868 | Move | WorkData.BR01_State | (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 77]) AND [Data.Oxigen_RO01 >= 60]) | Move 입력 7 |
| 1868 | Move | WorkData.BR01_State | (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 77]) AND [Data.Oxigen_RO01 < 60]) | Move 입력 0 |
| 1868 | SCoil | Enable start burner | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 7]) | 조건 성립 시 Set |
| 1868 | RCoil | Open MV03 for washing | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 7]) | 조건 성립 시 Reset |
| 1868 | SCoil | Close MV03 for Burner Startup | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 7]) | 조건 성립 시 Set |
| 1868 | Move | WorkData.BR01_State | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 7]) | Move 입력 8 |
| 1868 | Move | WorkData.BR01_State | (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 8]) AND Inputs.Burner On) | Move 입력 9 |
| 1868 | SdCoil | Tag_145 | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 9]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#30S |
| 1868 | Move | WorkData.BR01_State | (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 9]) AND Tag_145) | Move 입력 10 |
| 1868 | Move | WorkData.BR01_State | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 10]) | Move 입력 11 |
| 1868 | Coil | Start Burner | (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 11]) AND Inputs.Burner On) | 조건에 따른 Coil 기록 |
| 1868 | Move | WorkData.BR01_State | (((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 11]) AND NOT [Inputs.Burner On]) | Move 입력 0 |
| 1868 | Move | WorkData.BR01_CleanTime | ((ON AND Enable start burner(1)) AND [WorkData.BR01_State = 11]) | Move 입력 0 |
| 1869 | RCoil | Allarm.BURNER_START_FAULT | (Flag.RESET_ALLARM AND Allarm.BURNER_START_FAULT) | 조건 성립 시 Reset |
| 1870 | Coil | Flag AutoBurner | ((((((ON AND Flag.AUTO_BURNER) AND NOT [Allarm.MAX_TC01_TEMP]) AND NOT [Allarm.MAX_TC03_TEMP]) AND NOT [Programmed stop burner]) AND Start Burner) AND Inputs.High Flame Gas) | 조건에 따른 Coil 기록 |
| 1870 | Move | Data.Burner_Panel_SetPoint | ((ON AND NOT [Enable start burner(1)]) OR (ON AND Allarm.MAX_TC01_TEMP) OR (ON AND Allarm.MAX_TC03_TEMP) OR (ON AND Programmed stop burner) OR (ON AND NOT [Inputs.High Flame Gas])) | Move 입력 0 |
| 1872 | Move | Data.Burner_Panel_SetPoint | ((ON AND Inputs.Burner On) AND [Data.Burner_Panel_SetPoint > Data.Max_PRC_BR1]) | Move 입력 Data.Max_PRC_BR1 |
| 1872 | Move | Data.Burner_Panel_SetPoint | (ON AND [Data.Burner_Panel_SetPoint > 100]) | Move 입력 100 |
| 1872 | Move | Data.Burner_Panel_SetPoint | ((ON AND Rem. Start/Stop Burner) AND [Data.Burner_Panel_SetPoint < 0]) | Move 입력 0 |
| 1872 | Move | Data.Burner_Panel_SetPoint | (((ON AND NOT [Rem. Start/Stop Burner]) AND [Data.Burner_Panel_SetPoint <= 0]) OR (ON AND NOT [Enable start burner(1)])) | Move 입력 0 |


### 점검·진단 절차안

1. 외부 버너 상태: 버너 자체 제어반의 준비·운전·락아웃과 PLC 입력을 일대일 대조한다. 외부 버너 상세 시퀀스의 제조사 기준을 함께 적용한다.
2. 요청/허가: 원격 시작, 가스/공기 압력, 온도 허가, 블로어와 관련 알람 접점의 실제 연결을 확인한다.
3. 변조 경로: 온도 선택 → PID 호출 → 가스/공기 비율 및 제한 → 아날로그 출력 → 실제 서보/유량 피드백을 같은 시각에 기록한다.
4. 정지·락아웃: 락아웃 원인·신호 방향·Reset 출력과 외부 버너 응답을 기록한다. 원인 제거와 Reset, 재시작을 서로 다른 사건으로 시험한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| BR01-SIM-01 | 정상 인터페이스 | 버너 준비·허가·운전 응답 | 외부 상태와 PLC 신호 계약 대조 | 설계·미실행 |
| BR01-SIM-02 | 락아웃 | 버너 락아웃 입력 | 원격 출력·알람·Reset 경로 확인 | 설계·미실행 |
| BR01-SIM-03 | 온도 선택 | TC01/TC02 선택 및 고장 | PID 측정값과 선택 조건 확인 | 설계·미실행 |
| BR01-SIM-04 | 변조/제한 | 가스·공기 요구값과 한계 변경 | 비율·출력 범위·피드백 확인 | 설계·미실행 |
| BR01-SIM-05 | 압력/허가 누락 | 압력·블로어·온도 허가 변경 | 원본 출력 차단 경로 대조 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| BR01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| BR01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| BR01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| BR01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| BR01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |
| BR01-V-06 | 불일치/특이점 | 버너 전용 상세 도면 및 제조사 연소 제어 절차는 별도 문서가 필요하다. 이 매뉴얼의 일반 PLC 해석을 버너 안전 시퀀스로 대체하지 않는다. | 확인 대기 |

## HE01 · 열교환기

P&ID의 열교환 본체. MV01/MV04와 FN02의 연결 경로를 함께 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 기계·공정 상태: 본체의 누설·기밀·퇴적·마모·부식, 입출구 막힘, 점검구와 연결 배관 상태를 기록한다.
2. 연관 장치: 주변 모터·밸브·온도/압력/레벨 계측의 운전 상태와 본체 공정 상태를 연결해 검토한다.
3. 도면 동일성: P&ID의 위치와 실제 본체·배관·전기도면 장치의 태그를 대조하고 변경 사항을 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| HE01-SIM-01 | 공정 이상 모델 | 막힘·누설·퇴적을 연관 신호로 모델링 | 본체 직접 I/O가 없으면 연관 장치 영향으로 판정 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| HE01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| HE01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| HE01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## FN01 · 순환 블로어

TC04/TC05 베어링 온도, ZT01 및 전류 감시와 연결된다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 47 / PDF 48, FG 48 / PDF 49.

확인할 특이점: 베어링 TC04/TC05와 진동 ZT01의 고장·예경보 참조가 있다. preallarm 네트워크의 s5t#1h_30m은 지연 의미와 실행 조건을 원본에서 확인해야 하며, 보호 설정 권장값으로 사용하지 않는다. 

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I3.5 | fn01_fbk | bool | feedbackmotor fn-01 | 502 |
| %IW262 | reserved tc05 | int | probe sensor pt100 bearing fn-01 (tc-05) -30...350°c | 897 |
| %I3.6 | fn01_all_inv | bool | alarm motor fn-01 | 919 |
| %Q3.5 | star fan fn01 | bool | a 53.5 fn-01 motorcommand cooling fan | 997 |
| %I4.5 | fn01f_fbk | bool | feedback cooling fan motor fn-01 | 1057 |
| %Q2.7 | start fn01 | bool | a 49.6 fn-01 motorcommand | 1328 |
| %QW292 | fn01_sp_speed | word | sp speed blower fan fn-01 | 1353 |
| %IW260 | tc05 | int | probe sensor pt100 bearing fn-01 (tc-04) -30...250°c | 1511 |
| %IW334 | fn01_current | int | blower fan current fn-01 | 1524 |
| %IW282 | zt01 | int | vibration trasmitter blower fn-01 | 1541 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| FN01_Preathing_enable | DB41,X50.0 | PLC | 00467 |
| Editor_FN01 | DB26,INT14 | PLC | 00414 |
| FN_01\Allarme1 | DB11,X34.1 | PLC | 0034A |
| FN_01\RispostaA | DB11,X34.0 | PLC | 00305 |
| FN_01\Flag | DB2,X1.2 | PLC | 0019D |
| I_FN01_ABSORPTION | DB13,INT66 | PLC | 0002D |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 27 | fn-01 | [네트워크 1028](networks/network-1028.html) | 7/18 |
| time work motor | 49 |  | [네트워크 1050](networks/network-1050.html) | 6/17 |
| time work motor | 51 |  | [네트워크 1052](networks/network-1052.html) | 6/17 |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| simulation | 6 | motors simulated | [네트워크 1084](networks/network-1084.html) | 16/25 |
| hmi | 17 | fn01 | [네트워크 1194](networks/network-1194.html) | 1/9 |
| analog output conversion | 7 | fn-01 ventilator | [네트워크 1685](networks/network-1685.html) | 6/16 |
| analog input conversion | 42 | fn-01 | [네트워크 1772](networks/network-1772.html) | 2/9 |
| allarms 1 | 18 | fn01 | [네트워크 1798](networks/network-1798.html) | 16/28 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 5 | set points fn01 | [네트워크 1845](networks/network-1845.html) | 24/63 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| burner control | 4 | start gas test | [네트워크 1857](networks/network-1857.html) | 12/23 |
| motors 1 | 21 | preallarm fn01 | [네트워크 1950](networks/network-1950.html) | 12/22 |
| motors 1 | 22 | fn01 | [네트워크 1951](networks/network-1951.html) | 11/21 |
| allarms 3 | 9 | pc-01 low depressure | [네트워크 1987](networks/network-1987.html) | 13/27 |
| allarms 3 | 10 | high vibrations fn-01 | [네트워크 1988](networks/network-1988.html) | 10/21 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1028 | Move | hours motors.FN_01_HOUR | ((Tag_47 AND FN01_Fbk) AND [hours motors.FN_01_MIN >= 60]) | Move 입력 1 |
| 1028 | Move | hours motors.FN_01_MIN | Move UID 1658.eno (블록 동작 확인) | Move 입력 0 |
| 1028 | SCoil | Flag_Aggiorna_DB | Move UID 1661.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1685 | Move | Data.SET_PERC_VT01 | (ON AND [Data.SET_PERC_VT01 < 5]) | Move 입력 5 |
| 1685 | Move | Data.SET_PERC_VT01 | (ON AND [Data.SET_PERC_VT01 > 100]) | Move 입력 100 |
| 1798 | SdCoil | Tag_63 | (((ON AND Start FN01) AND NOT [Inputs.FN01 Run]) OR ((ON AND Start FN01) AND Inputs.FN01_All_Inv)) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1798 | SCoil | Allarm.FN_01_FAULT | (((ON AND Start FN01) AND Tag_63) AND NOT [Inputs.FN01 Run]) | 조건 성립 시 Set |
| 1798 | SCoil | Allarm.FN01_INV | (((ON AND Start FN01) AND Tag_63) AND Inputs.FN01_All_Inv) | 조건 성립 시 Set |
| 1798 | RCoil | Allarm.FN_01_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.FN_01_FAULT) | 조건 성립 시 Reset |
| 1798 | RCoil | Allarm.FN01_INV | ((ON AND Flag.RESET_ALLARM) AND Allarm.FN01_INV) | 조건 성립 시 Reset |
| 1845 | Move | Data.SET_PERC_VT01 | LRef UID 58.Q (블록 동작 확인) | Move 입력 HMI_DB.FN01_Preheating_1st_step_speed |
| 1845 | Move | Data.SET_PERC_VT01 | LRef UID 63.Q (블록 동작 확인) | Move 입력 HMI_DB.FN01_Preheating_2nd_step_speed |
| 1845 | Move | Data.SET_PERC_VT01 | LRef UID 68.Q (블록 동작 확인) | Move 입력 HMI_DB.FN01_Preheating_3rd_step_speed |
| 1845 | Move | Data.SET_PERC_VT01 | LRef UID 72.Q (블록 동작 확인) | Move 입력 HMI_DB.FN01_Preheating_4th_step_speed |
| 1845 | Move | Data.SET_PERC_VT01 | LRef UID 76.Q (블록 동작 확인) | Move 입력 15 |
| 1950 | Coil | Allarm.Prealarms_FN01 | ((ON AND Allarm.MAX_TC04_TEMP) OR (ON AND Allarm.MAX_TC05_TEMP) OR (ON AND Allarm.ZT01_FN01_Vibration) OR ((ON AND Inputs.FN01 Run) AND NOT [Inputs.VR-01 RUN]) OR ((ON AND Inputs.FN01 Run) AND NOT [Inputs.VR02 Run])) | 조건에 따른 Coil 기록 |
| 1950 | SdCoil | Tag_122 | ((ON AND Allarm.MAX_TC04_TEMP) OR (ON AND Allarm.MAX_TC05_TEMP) OR (ON AND Allarm.ZT01_FN01_Vibration) OR ((ON AND Inputs.FN01 Run) AND NOT [Inputs.VR-01 RUN]) OR ((ON AND Inputs.FN01 Run) AND NOT [Inputs.VR02 Run])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1H_30M |
| 1950 | Coil | Stop_Fan_FN01 | (((ON AND Allarm.MAX_TC04_TEMP) OR (ON AND Allarm.MAX_TC05_TEMP) OR (ON AND Allarm.ZT01_FN01_Vibration) OR ((ON AND Inputs.FN01 Run) AND NOT [Inputs.VR-01 RUN]) OR ((ON AND Inputs.FN01 Run) AND NOT [Inputs.VR02 Run])) AND Tag_122) | 조건에 따른 Coil 기록 |
| 1951 | RCoil | Flag.M_FN_01 | ((ON AND Allarm.FN_01_FAULT) OR (ON AND Allarm.FN01_INV) OR (ON AND [Data.SET_PERC_VT01 = 0]) OR (ON AND Stop_Fan_FN01) OR ((ON AND Allarm.HYDROGEN_BOX_FAULT) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1951 | Coil | Start FN01 | (ON AND Flag.M_FN_01) | 조건에 따른 Coil 기록 |
| 1988 | SdCoil | Tag_110 | ((OFF AND [Data.ZT_01 > 400]) OR (OFF AND [Data.ZT_01 < -800])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#10S |
| 1988 | SCoil | Allarm.ZT01_FN01_Vibration | (((OFF AND [Data.ZT_01 > 400]) OR (OFF AND [Data.ZT_01 < -800])) AND Tag_110) | 조건 성립 시 Set |
| 1988 | RCoil | Allarm.ZT01_FN01_Vibration | ((OFF AND Allarm.ZT01_FN01_Vibration) AND [Data.ZT_01 < 380]) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| FN01-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| FN01-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| FN01-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| FN01-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| FN01-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| FN01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| FN01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| FN01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| FN01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| FN01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## FN02 · 열회수 블로어

열회수 경로의 송풍과 아날로그 속도 설정을 담당한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 42 / PDF 43, FG 43 / PDF 44.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I3.0 | fn02_fbk | bool | feedback motor fn-02 | 500 |
| %I3.1 | fn02_all_inv | bool | alarm motor fn-02 | 918 |
| %QW306 | fn02_sp | word | blower fan fn-02(4-20ma) | 1350 |
| %Q2.3 | start fn02 | bool | a 52.0 fn-02 motorcommand | 1360 |
| %IW328 | fn02_current | int | blower fan current | 1526 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| FN_02\Allarme1 | DB11,X30.1 | PLC | 0034E |
| FN_02\RispostaA | DB11,X30.0 | PLC | 00307 |
| Gain_FN02 | DB150,INT4 | PLC | 001D4 |
| TI_FN02 | DB150,D0 | PLC | 001CF |
| FN_02\Flag | DB2,X1.0 | PLC | 0019F |
| I_FN02_ABSORPTION | DB13,INT60 | PLC | 0002A |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 25 | fn-02 | [네트워크 1026](networks/network-1026.html) | 7/18 |
| time work motor | 49 |  | [네트워크 1050](networks/network-1050.html) | 6/17 |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| simulation | 6 | motors simulated | [네트워크 1084](networks/network-1084.html) | 16/25 |
| hmi | 15 | fn02 | [네트워크 1192](networks/network-1192.html) | 1/9 |
| analog output conversion | 10 | fn02 ventilation of secondary air | [네트워크 1688](networks/network-1688.html) | 6/16 |
| analog input conversion | 37 | fn-02 fan | [네트워크 1767](networks/network-1767.html) | 2/9 |
| analog input conversion | 40 | fn-02 aspirator | [네트워크 1770](networks/network-1770.html) | 2/9 |
| allarms 1 | 16 | fn02 | [네트워크 1796](networks/network-1796.html) | 16/28 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| burner control | 4 | start gas test | [네트워크 1857](networks/network-1857.html) | 12/23 |
| motors 1 | 19 | fn02 | [네트워크 1948](networks/network-1948.html) | 8/15 |
| cyc_int5 ogni 100ms | 9 | disable pid control on vt02 | [네트워크 12](networks/network-12.html) | 6/11 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1026 | Move | hours motors.FN_02_HOUR | ((Tag_47 AND FN02_Fbk) AND [hours motors.FN_02_MIN >= 60]) | Move 입력 1 |
| 1026 | Move | hours motors.FN_02_MIN | Move UID 1550.eno (블록 동작 확인) | Move 입력 0 |
| 1026 | SCoil | Flag_Aggiorna_DB | Move UID 1553.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1688 | Move | Data.Set_Perc_VT02 | (ON AND [Data.Set_Perc_VT02 < 5]) | Move 입력 5 |
| 1688 | Move | Data.Set_Perc_VT02 | (ON AND [Data.Set_Perc_VT02 > 100]) | Move 입력 100 |
| 1796 | SdCoil | Tag_61 | (((ON AND Start FN02) AND NOT [Inputs.FN02 Run]) OR ((ON AND Start FN02) AND Inputs.FN02_All_Inv)) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1796 | SCoil | Allarm.FN_02_FAULT | (((ON AND Start FN02) AND Tag_61) AND NOT [Inputs.FN02 Run]) | 조건 성립 시 Set |
| 1796 | SCoil | Allarm.FN02_INV | (((ON AND Start FN02) AND Tag_61) AND Inputs.FN02_All_Inv) | 조건 성립 시 Set |
| 1796 | RCoil | Allarm.FN_02_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.FN_02_FAULT) | 조건 성립 시 Reset |
| 1796 | RCoil | Allarm.FN02_INV | ((ON AND Flag.RESET_ALLARM) AND Allarm.FN02_INV) | 조건 성립 시 Reset |
| 1948 | RCoil | Flag.M_FN_02 | ((ON AND Allarm.FN_02_FAULT) OR (ON AND Allarm.FN02_INV) OR (ON AND [Data.Set_Perc_VT02 = 0])) | 조건 성립 시 Reset |
| 1948 | Coil | Start FN02 | (ON AND Flag.M_FN_02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| FN02-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| FN02-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| FN02-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| FN02-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| FN02-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| FN02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| FN02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| FN02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| FN02-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| FN02-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## FN03 · 연소 공기 블로어

BR01 측 연소 공기 공급 경로.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 51 / PDF 52.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I4.1 | fn03_fbk | bool | feedback motor fn-03 | 505 |
| %I4.2 | fn03_all_softstarter | bool | alarm motor fn-03 | 506 |
| %Q3.2 | start fn03 | bool | a 56.0 fn-03 motorcommand | 1322 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| FN_03\Allarme1 | DB11,X40.1 | PLC | 00346 |
| FN_03\RispostaA | DB11,X40.0 | PLC | 001C3 |
| FN_03\Flag | DB2,X1.5 | PLC | 0019B |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 30 | fn-03 | [네트워크 1031](networks/network-1031.html) | 7/18 |
| time work motor | 50 |  | [네트워크 1051](networks/network-1051.html) | 6/17 |
| simulation | 6 | motors simulated | [네트워크 1084](networks/network-1084.html) | 16/25 |
| hmi | 20 | fn03 | [네트워크 1197](networks/network-1197.html) | 1/9 |
| allarms 1 | 21 | fn03 | [네트워크 1801](networks/network-1801.html) | 24/43 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| burner control | 5 | burner stop | [네트워크 1858](networks/network-1858.html) | 21/40 |
| burner control | 13 | burner start sequence | [네트워크 1866](networks/network-1866.html) | 9/16 |
| motors 1 | 25 | fn03 | [네트워크 1954](networks/network-1954.html) | 7/12 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1031 | Move | hours motors.FN_03_HOUR | ((Tag_47 AND FN03_Fbk) AND [hours motors.FN_03_MIN >= 60]) | Move 입력 1 |
| 1031 | Move | hours motors.FN_03_MIN | Move UID 1820.eno (블록 동작 확인) | Move 입력 0 |
| 1031 | SCoil | Flag_Aggiorna_DB | Move UID 1823.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1801 | SCoil | Memo_M25_Running | PContact UID 905.out (블록 동작 확인) | 조건 성립 시 Set |
| 1801 | RCoil | Memo_M25_Running | (NOT [Start FN03] OR NOT [Inputs.FN03 Run]) | 조건 성립 시 Reset |
| 1801 | SdCoil | Tag_66 | (((ON AND Start FN03) AND NOT [Inputs.FN03 Run]) AND NOT [Memo_M25_Running]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#35S |
| 1801 | SdCoil | Tag_66 | (((ON AND Start FN03) AND NOT [Inputs.FN03 Run]) AND Memo_M25_Running) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#35S |
| 1801 | SCoil | Allarm.FN03_INV | ((ON AND Start FN03) AND NOT [Inputs.FN03_All_SoftStarter]) | 조건 성립 시 Set |
| 1801 | SCoil | Allarm.FN_03_FAULT | (((ON AND Start FN03) AND Tag_66) AND NOT [Inputs.FN03 Run]) | 조건 성립 시 Set |
| 1801 | RCoil | Allarm.FN_03_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.FN_03_FAULT) | 조건 성립 시 Reset |
| 1801 | RCoil | Allarm.FN03_INV | ((ON AND Flag.RESET_ALLARM) AND Allarm.FN03_INV) | 조건 성립 시 Reset |
| 1954 | RCoil | Flag.M_FN_03 | ((ON AND Allarm.FN_03_FAULT) OR (ON AND Allarm.FN03_INV)) | 조건 성립 시 Reset |
| 1954 | Coil | Start FN03 | (ON AND Flag.M_FN_03) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| FN03-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| FN03-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| FN03-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| FN03-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| FN03-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| FN03-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| FN03-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| FN03-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| FN03-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| FN03-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## FN04 · 집진 배기팬

CY·BF 집진 경로의 흡인 및 압력 제어와 연결된다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 59 / PDF 60, FG 60 / PDF 61.

확인할 특이점: 백업에는 Q17.1 start fn04와 Q4.2 spare_0(FN04 관련 옛 주석)가 공존한다. 전기 회로와 출력 사용처로 현재 실구동 채널을 확정해야 한다. 네트워크 제목 fn-02 aspirator와 실제 FN04 전류 입력도 충돌한다. 

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I28.3 | fn04_all_inv | bool |  | 955 |
| %I28.2 | fn04_fbk | bool |  | 956 |
| %Q4.2 | spare_0 | bool | a 52.4 fn-04/fn-04a motorcommand | 957 |
| %Q17.1 | start fn04 | bool | fn-04/fn-04a motor | 1278 |
| %QW336 | fn04_sp | word | aspiration fan fn-04 speed | 1349 |
| %IW394 | fn04_current | int | main aspirator absorption current fn-04(4-20ma) | 1515 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| FN_04\Allarme1 | DB11,X56.1 | PLC | 00336 |
| FN_04\AutoON | DB2,X9.2 | PLC | 001D7 |
| FN_04\RispostaA | DB11,X56.0 | PLC | 001BB |
| FN_04\Flag | DB2,X2.4 | PLC | 00193 |
| I_FN04_ABSORPTION | DB13,INT62 | PLC | 0002B |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| startup only | 4 | plants defaults | [네트워크 404](networks/network-404.html) | 10/14 |
| time work motor | 38 | fn-04 | [네트워크 1039](networks/network-1039.html) | 7/18 |
| time work motor | 52 |  | [네트워크 1053](networks/network-1053.html) | 6/17 |
| hmi inputs | 1 |  | [네트워크 1070](networks/network-1070.html) | 33/62 |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| simulation | 7 | motors simulated | [네트워크 1085](networks/network-1085.html) | 19/29 |
| hmi | 28 | fn04 ???? | [네트워크 1205](networks/network-1205.html) | 1/9 |
| analog output conversion | 11 | module aspirator fn-04 | [네트워크 1689](networks/network-1689.html) | 6/16 |
| analog input conversion | 40 | fn-02 aspirator | [네트워크 1770](networks/network-1770.html) | 2/9 |
| allarms 1 | 29 | fn04 | [네트워크 1809](networks/network-1809.html) | 16/28 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| burner control | 4 | start gas test | [네트워크 1857](networks/network-1857.html) | 12/23 |
| filter | 19 | speed fn-04 at start | [네트워크 1900](networks/network-1900.html) | 3/7 |
| filter | 20 | dp-01 control loop | [네트워크 1901](networks/network-1901.html) | 11/30 |
| motors 1 | 35 | preallarm fn04 | [네트워크 1964](networks/network-1964.html) | 13/24 |
| motors 1 | 36 | fn04 | [네트워크 1965](networks/network-1965.html) | 10/19 |
| motors 1 | 41 | fn05 | [네트워크 1970](networks/network-1970.html) | 8/14 |
| allarms 3 | 9 | pc-01 low depressure | [네트워크 1987](networks/network-1987.html) | 13/27 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1039 | Move | hours motors.FN_04_HOUR | ((Tag_47 AND FN04_Fbk) AND [hours motors.FN_04_MIN >= 60]) | Move 입력 1 |
| 1039 | Move | hours motors.FN_04_MIN | Move UID 2252.eno (블록 동작 확인) | Move 입력 0 |
| 1039 | SCoil | Flag_Aggiorna_DB | Move UID 2255.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1689 | Move | Data.SET_PERC_FN04 | (ON AND [Data.SET_PERC_FN04 < 5]) | Move 입력 5 |
| 1689 | Move | Data.SET_PERC_FN04 | (ON AND [Data.SET_PERC_FN04 > 100]) | Move 입력 100 |
| 1809 | SdCoil | Tag_74 | (((ON AND Start FN04) AND NOT [Inputs.FN04 Run]) OR ((ON AND Start FN04) AND Inputs.FN04_All_inv)) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#17S |
| 1809 | SCoil | Allarm.FN_04_FAULT | (((ON AND Start FN04) AND Tag_74) AND NOT [Inputs.FN04 Run]) | 조건 성립 시 Set |
| 1809 | SCoil | Allarm.FN04_INV | (((ON AND Start FN04) AND Tag_74) AND Inputs.FN04_All_inv) | 조건 성립 시 Set |
| 1809 | RCoil | Allarm.FN_04_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.FN_04_FAULT) | 조건 성립 시 Reset |
| 1809 | RCoil | Allarm.FN04_INV | ((ON AND Flag.RESET_ALLARM) AND Allarm.FN04_INV) | 조건 성립 시 Reset |
| 1900 | Move | Data.SET_PERC_FN04 | PBox UID 1847.out (블록 동작 확인) | Move 입력 20 |
| 1964 | Coil | Allarm.Prealarms_FN04 | (((ON AND Inputs.FN04 Run) AND NOT [Inputs.FEEDBACKMOTOR SC-01]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.VR03 Run]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.FEEDBACKMOTOR SC-10]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.VR04 Run]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.FEEDBACKMOTOR SC-11]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.VR05 Run])) | 조건에 따른 Coil 기록 |
| 1964 | SdCoil | Tag_126 | (((ON AND Inputs.FN04 Run) AND NOT [Inputs.FEEDBACKMOTOR SC-01]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.VR03 Run]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.FEEDBACKMOTOR SC-10]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.VR04 Run]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.FEEDBACKMOTOR SC-11]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.VR05 Run])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1H_30M |
| 1964 | Coil | Stop_Fan_FN04 | ((((ON AND Inputs.FN04 Run) AND NOT [Inputs.FEEDBACKMOTOR SC-01]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.VR03 Run]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.FEEDBACKMOTOR SC-10]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.VR04 Run]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.FEEDBACKMOTOR SC-11]) OR ((ON AND Inputs.FN04 Run) AND NOT [Inputs.VR05 Run])) AND Tag_126) | 조건에 따른 Coil 기록 |
| 1965 | RCoil | Flag.M_FN_04 | ((ON AND Allarm.FN_04_FAULT) OR (ON AND Allarm.FN04_INV) OR (ON AND [Data.SET_PERC_FN04 = 0]) OR (ON AND Stop_Fan_FN04) OR (ON AND Allarm.MAX_MAX_TC09)) | 조건 성립 시 Reset |
| 1965 | Coil | Start FN04 | (ON AND Flag.M_FN_04) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| FN04-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| FN04-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| FN04-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| FN04-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| FN04-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| FN04-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| FN04-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| FN04-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| FN04-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| FN04-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## FN05 · 석회 계통 송풍기

LD01/ER01 석회 계통 송풍 경로.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 65 / PDF 66.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I6.0 | fn05_fbk | bool | feedback motor fn-05 | 518 |
| %Q4.7 | start fn05 | bool | a 60.0 fn-05 motorcommand | 1299 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| FN_05\Allarme1 | DB11,X66.1 | PLC | 0032C |
| FN_05\RispostaA | DB11,X66.0 | PLC | 001B6 |
| FN_05\Flag | DB2,X3.1 | PLC | 0018E |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 43 | fn-05 | [네트워크 1044](networks/network-1044.html) | 7/18 |
| time work motor | 53 |  | [네트워크 1054](networks/network-1054.html) | 2/5 |
| simulation | 8 | motors simulated | [네트워크 1086](networks/network-1086.html) | 10/15 |
| hmi | 33 | fn05 | [네트워크 1210](networks/network-1210.html) | 1/9 |
| allarms 1 | 34 | fn05 | [네트워크 1814](networks/network-1814.html) | 9/17 |
| motors 1 | 41 | fn05 | [네트워크 1970](networks/network-1970.html) | 8/14 |
| motors 1 | 42 | er01 | [네트워크 1971](networks/network-1971.html) | 10/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1044 | Move | hours motors.FN_05_HOUR | ((Tag_47 AND FN05_Fbk) AND [hours motors.FN_05_MIN >= 60]) | Move 입력 1 |
| 1044 | Move | hours motors.FN_05_MIN | Move UID 2522.eno (블록 동작 확인) | Move 입력 0 |
| 1044 | SCoil | Flag_Aggiorna_DB | Move UID 2525.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1814 | SdCoil | Tag_79 | ((ON AND Start FN05) AND NOT [Inputs.FN-05 RUN]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1814 | SCoil | Allarm.FN_05_FAULT | ((ON AND Start FN05) AND Tag_79) | 조건 성립 시 Set |
| 1814 | RCoil | Allarm.FN_05_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.FN_05_FAULT) | 조건 성립 시 Reset |
| 1970 | RCoil | Flag.M_FN_05 | ((ON AND Allarm.FN_05_FAULT) OR ((ON AND NOT [Inputs.FN04 Run]) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1970 | Coil | Start FN05 | (ON AND Flag.M_FN_05) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| FN05-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| FN05-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| FN05-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| FN05-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| FN05-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| FN05-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| FN05-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| FN05-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| FN05-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| FN05-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## FN06 · 보조 블로어

P&ID의 AB01 하부 보조 송풍 경로.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 52 / PDF 53.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I4.3 | fn06_fbk | bool | feedback motor fn-06 | 507 |
| %Q3.3 | start fn06 | bool | a 60.3 fn-06 motorcommand | 1320 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| FN_06\Allarme1 | DB11,X42.1 | PLC | 00344 |
| FN_06\RispostaA | DB11,X42.0 | PLC | 001C2 |
| FN_06\Flag | DB2,X3.7 | PLC | 0019A |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 31 | fn-06 | [네트워크 1032](networks/network-1032.html) | 7/18 |
| time work motor | 50 |  | [네트워크 1051](networks/network-1051.html) | 6/17 |
| simulation | 6 | motors simulated | [네트워크 1084](networks/network-1084.html) | 16/25 |
| hmi | 21 | fn06 | [네트워크 1198](networks/network-1198.html) | 1/9 |
| allarms 1 | 22 | fn06 | [네트워크 1802](networks/network-1802.html) | 9/17 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| burner control | 4 | start gas test | [네트워크 1857](networks/network-1857.html) | 12/23 |
| motors 1 | 26 | fn06 | [네트워크 1955](networks/network-1955.html) | 8/14 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1032 | Move | hours motors.FN_06_HOUR | ((Tag_47 AND FN06_Fbk) AND [hours motors.FN_06_MIN >= 60]) | Move 입력 1 |
| 1032 | Move | hours motors.FN_06_MIN | Move UID 1874.eno (블록 동작 확인) | Move 입력 0 |
| 1032 | SCoil | Flag_Aggiorna_DB | Move UID 1877.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1802 | SdCoil | Tag_67 | ((ON AND Start FN06) AND NOT [Inputs.FEEDBACKMOTOR FN-06]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1802 | SCoil | Allarm.MBVA01_FAULT | ((ON AND Start FN06) AND Tag_67) | 조건 성립 시 Set |
| 1802 | RCoil | Allarm.MBVA01_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.MBVA01_FAULT) | 조건 성립 시 Reset |
| 1955 | RCoil | Flag.M_FN_06 | ((ON AND Allarm.MBVA01_FAULT) OR ((ON AND NOT [Inputs.RD01 run]) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1955 | Coil | Start FN06 | (ON AND Flag.M_FN_06) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| FN06-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| FN06-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| FN06-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| FN06-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| FN06-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| FN06-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| FN06-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| FN06-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| FN06-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| FN06-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## FN01-FAN · FN01 모터 냉각팬

FN01 구동부 냉각 보조장치.

자료 상태: SPARE·삭제 제목. 상위: FN01. 전기: FG 54 / PDF 55.

확인할 특이점:  Q3.5/I4.5 잔존과 SPARE 표기를 따로 기록한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q3.5 | star fan fn01 | bool | a 53.5 fn-01 motorcommand cooling fan | 997 |
| %I4.5 | fn01f_fbk | bool | feedback cooling fan motor fn-01 | 1057 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 51 |  | [네트워크 1052](networks/network-1052.html) | 6/17 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |

### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| FN01-FAN-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| FN01-FAN-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| FN01-FAN-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| FN01-FAN-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| FN01-FAN-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| FN01-FAN-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| FN01-FAN-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| FN01-FAN-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| FN01-FAN-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| FN01-FAN-V-05 | 불일치/특이점 | Q3.5/I4.5 잔존과 SPARE 표기를 따로 기록한다. | 확인 대기 |

## CH01 · 냉각기

FN01 측 냉각 계통. PLC 내부 시작 요청과 별도 원격 기동 출력 경로를 구분한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 50 / PDF 51.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q6.0 | enable start chiller | bool | a 61.0 chiller remotestart | 678 |
| %I4.0 | ch01_fbk | bool | feedback motor ch-01 | 942 |
| %Q3.1 | start ch01 | bool | a 53.4 ch-01 motorcommand | 1324 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| CH_01\Allarme1 | DB11,X38.1 | PLC | 00348 |
| CH_01\RispostaA | DB11,X38.0 | PLC | 00304 |
| CH_01\Flag | DB2,X1.4 | PLC | 0019C |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 29 | ch-01 | [네트워크 1030](networks/network-1030.html) | 7/18 |
| time work motor | 50 |  | [네트워크 1051](networks/network-1051.html) | 6/17 |
| simulation | 6 | motors simulated | [네트워크 1084](networks/network-1084.html) | 16/25 |
| hmi | 19 | ch01 | [네트워크 1196](networks/network-1196.html) | 1/9 |
| analog input conversion | 31 | store current position value at power-off | [네트워크 1761](networks/network-1761.html) | 6/13 |
| analog input conversion | 33 | data management mv02 | [네트워크 1763](networks/network-1763.html) | 10/28 |
| allarms 1 | 20 | ch01 | [네트워크 1800](networks/network-1800.html) | 9/17 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| motors 1 | 24 | ch01 | [네트워크 1953](networks/network-1953.html) | 9/16 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1030 | Move | hours motors.CH_01_HOUR | ((Tag_47 AND CH01_Fbk) AND [hours motors.CH_01_MIN >= 60]) | Move 입력 1 |
| 1030 | Move | hours motors.CH_01_MIN | Move UID 1766.eno (블록 동작 확인) | Move 입력 0 |
| 1030 | SCoil | Flag_Aggiorna_DB | Move UID 1769.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1800 | SdCoil | Tag_65 | ((ON AND Start CH01) AND NOT [Inputs.CH01 Run]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1800 | SCoil | Allarm.CH_01_FAULT | ((ON AND Start CH01) AND Tag_65) | 조건 성립 시 Set |
| 1800 | RCoil | Allarm.CH_01_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.CH_01_FAULT) | 조건 성립 시 Reset |
| 1953 | RCoil | Flag.M_CH_01 | ((ON AND ServiceBit) AND Allarm.CH_01_FAULT) | 조건 성립 시 Reset |
| 1953 | Coil | Start CH01 | ((ON AND ServiceBit) AND Flag.M_CH_01) | 조건에 따른 Coil 기록 |
| 1953 | SdCoil | Tag_123 | ((ON AND ServiceBit) AND Flag.M_CH_01) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#10S |
| 1953 | Coil | Enable start chiller | (((ON AND ServiceBit) AND Flag.M_CH_01) AND Tag_123) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CH01-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| CH01-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| CH01-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| CH01-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| CH01-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CH01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CH01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CH01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CH01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CH01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## MV01 · 모터 구동 밸브

TC03 관련 열회수 경로 제어.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 44 / PDF 45, FG 45 / PDF 46.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q2.4 | start open mv-01 | bool | a 60.1 mv-01 openingmotor command | 676 |
| %Q2.5 | start close mv-01 | bool | a 60.2 mv-01 closingmotor command | 677 |
| %I3.2 | mv01_fbk_opening | bool | feedback openingmotor mv-01 | 885 |
| %I3.3 | mv01_fbk_closing | bool | feedback closingmotor mv-01 | 886 |
| %I8.1 | mv01_open | bool | limit switch ls-23 | 889 |
| %M12.1 | down mv01 pid | bool |  | 1361 |
| %M12.0 | up mv01 pid | bool |  | 1362 |
| %I8.2 | mv01_close | bool | limit switch ls-24 | 1528 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| RESET_ENC_MV01 | DB41,X50.5 | PLC | 00464 |
| MV_01\LimitSwitchOpen | DB11,X18.3 | PLC | 00316 |
| MV_01\LimitSwitchClose | DB11,X18.4 | PLC | 00315 |
| MV_01\Flag_OPEN | DB2,X3.3 | PLC | 00314 |
| MV_01\AutoMan | DB2,X7.2 | PLC | 00309 |
| MV_01\OutputOpen | DB11,X18.0 | PLC | 00308 |
| MV_01\Flag_CLOSE | DB2,X3.4 | PLC | 001A7 |
| MV_01\Allarme1 | DB11,X18.2 | PLC | 001A6 |
| MV_01\OutputClose | DB11,X18.1 | PLC | 001A0 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| startup only | 4 | plants defaults | [네트워크 404](networks/network-404.html) | 10/14 |
| simulation | 5 | mv | [네트워크 1083](networks/network-1083.html) | 70/151 |
| hmi | 13 | mv01 | [네트워크 1190](networks/network-1190.html) | 1/15 |
| allarms 2 | 1 | mv-01 motorized valve fault | [네트워크 1226](networks/network-1226.html) | 59/103 |
| valve control loop | 1 | mv01 controlled by tc03 | [네트워크 1702](networks/network-1702.html) | 35/61 |
| valve control loop | 2 | calibration encoder mv01 | [네트워크 1703](networks/network-1703.html) | 6/13 |
| valve control loop | 12 | motorized valve pulse generator for rotation control | [네트워크 1713](networks/network-1713.html) | 42/95 |
| valve control loop | 13 | motorized valve fault | [네트워크 1714](networks/network-1714.html) | 43/87 |
| analog input conversion | 26 | reading encoder mv01 | [네트워크 1756](networks/network-1756.html) | 3/28 |
| analog input conversion | 32 | data management mv01 | [네트워크 1762](networks/network-1762.html) | 10/28 |
| cyc_int5 ogni 100ms | 8 | controll tc03 moduling mv01 | [네트워크 11](networks/network-11.html) | 13/46 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1226 | SdCoil | Tag_92 | (((ON AND Start Open MV-01) AND NOT [Inputs.MV01 Run_Opening]) OR ((ON AND Start Close MV-01) AND NOT [Inputs.MV01 Run_Closing])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#150mS |
| 1226 | SCoil | Allarm.MV01_FAULT | ((((ON AND Start Open MV-01) AND NOT [Inputs.MV01 Run_Opening]) OR ((ON AND Start Close MV-01) AND NOT [Inputs.MV01 Run_Closing])) AND Tag_92) | 조건 성립 시 Set |
| 1226 | SdCoil | Tag_93 | (((ON AND Open MV02) AND NOT [Inputs.MV02 RUN_Opening]) OR ((ON AND Close MV02) AND NOT [Inputs.MV02 RUN_Closing])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#150MS |
| 1226 | SCoil | Allarm.MV02_FAULT | ((((ON AND Open MV02) AND NOT [Inputs.MV02 RUN_Opening]) OR ((ON AND Close MV02) AND NOT [Inputs.MV02 RUN_Closing])) AND Tag_93) | 조건 성립 시 Set |
| 1226 | SdCoil | Tag_94 | (((ON AND Start open MV03) AND NOT [Inputs.MV03 Run_Opening]) OR ((ON AND Start Close MV03) AND NOT [Inputs.MV03 Run_Closing])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#150S |
| 1226 | SCoil | Allarm.MV03_FAULT | ((((ON AND Start open MV03) AND NOT [Inputs.MV03 Run_Opening]) OR ((ON AND Start Close MV03) AND NOT [Inputs.MV03 Run_Closing])) AND Tag_94) | 조건 성립 시 Set |
| 1226 | SdCoil | Tag_96 | (((ON AND Open MV05) AND NOT [Inputs.MV05 RUN_Opening]) OR ((ON AND Close MV05) AND NOT [Inputs.MV05 RUN_Closing])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#150MS |
| 1226 | SCoil | Allarm.MV_05_FAULT | ((((ON AND Open MV05) AND NOT [Inputs.MV05 RUN_Opening]) OR ((ON AND Close MV05) AND NOT [Inputs.MV05 RUN_Closing])) AND Tag_96) | 조건 성립 시 Set |
| 1226 | SdCoil | Tag_97 | (((ON AND Open MV06) AND NOT [Inputs.MV06 Run_Opening]) OR ((ON AND Close MV06) AND NOT [Inputs.MV06 Run_Closing])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#150MS |
| 1226 | SCoil | Allarm.MV_06_FAULT | ((((ON AND Open MV06) AND NOT [Inputs.MV06 Run_Opening]) OR ((ON AND Close MV06) AND NOT [Inputs.MV06 Run_Closing])) AND Tag_97) | 조건 성립 시 Set |
| 1226 | RCoil | Allarm.MV01_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.MV01_FAULT) | 조건 성립 시 Reset |
| 1226 | RCoil | Allarm.MV02_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.MV02_FAULT) | 조건 성립 시 Reset |
| 1226 | RCoil | Allarm.MV03_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.MV03_FAULT) | 조건 성립 시 Reset |
| 1226 | RCoil | Allarm.MV04_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.MV04_FAULT) | 조건 성립 시 Reset |
| 1226 | RCoil | Allarm.MV_05_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.MV_05_FAULT) | 조건 성립 시 Reset |
| 1226 | RCoil | Allarm.MV_06_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.MV_06_FAULT) | 조건 성립 시 Reset |
| 1702 | RCoil | Flag.M_MV01_OPEN | ((ON AND Inputs.MV01 Open) OR (ON AND Flag.M_MV01_Close) OR (ON AND Flag.MV01_Auto)) | 조건 성립 시 Reset |
| 1702 | RCoil | Flag.M_MV01_Close | ((ON AND Inputs.MV01 Close) OR (ON AND Flag.M_MV01_OPEN) OR (ON AND Flag.MV01_Auto)) | 조건 성립 시 Reset |
| 1702 | Coil | Start Open MV-01 | (((((((((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.MV01_Auto) AND UP MV01 PID) OR ((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.M_MV01_OPEN)) AND MV WORK PULSE) OR (((((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.MV01_Auto) AND UP MV01 PID) OR ((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.M_MV01_OPEN)) AND ORef UID 172)) AND NOT [Start Close MV-01]) AND NOT [Inputs.MV01 Open]) AND NOT [HMI_DB.ResetEncoderProcedure_MV01]) | 조건에 따른 Coil 기록 |
| 1702 | Coil | Start Close MV-01 | ((((((((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.MV01_Auto) AND DOWN MV01 PID) OR ((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.M_MV01_Close)) AND MV WORK PULSE) OR (((((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.MV01_Auto) AND DOWN MV01 PID) OR ((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.M_MV01_Close)) AND ON) OR ((ON AND NOT [Allarm.MV01_FAULT]) AND HMI_DB.ResetEncoderProcedure_MV01)) AND NOT [Start Open MV-01]) AND NOT [Inputs.MV01 Close]) | 조건에 따른 Coil 기록 |
| 1703 | Move | MV01_Encoder.NewCountValue | (HMI_DB.ResetEncoderProcedure_MV01 AND Inputs.MV01 Close) | Move 입력 0 |
| 1703 | Coil | MV01_Encoder.SetCountValue | (Move UID 23.eno (블록 동작 확인) AND NOT [MV01_Encoder.SetCountValue]) | 조건에 따른 Coil 기록 |
| 1703 | RCoil | HMI_DB.ResetEncoderProcedure_MV01 | Coil UID 25.out (블록 동작 확인) | 조건 성립 시 Reset |
| 1762 | Coil | fill_unit1.CONTROL_SIGNALS.SW_GATE0 | (EM_OK AND NOT [MV01_Close]) | 조건에 따른 Coil 기록 |
| 1762 | Move | Memory encoder.Encoder_CH00_10 | Div UID 1034.eno (블록 동작 확인) | Move 입력 CNTV0_100 |
| 1762 | Move | Memory encoder.Encoder_CH00_10 | (EM_OK AND NOT [fill_unit1.CONTROL_SIGNALS.SW_GATE0]) | Move 입력 0 |
| 1762 | Move | Memory encoder.Encoder_CH00 | (EM_OK AND NOT [fill_unit1.CONTROL_SIGNALS.SW_GATE0]) | Move 입력 INT#0 |


### 점검·진단 절차안

1. 공통 전원/구동 준비: 공통 인버터 전원 허가와 개별 열림/닫힘 구동 피드백을 따로 기록한다.
2. 수동·자동 요청: HMI 개방/폐쇄 요청, 자동 플래그, 관련 PID 또는 펄스 요청, 양 끝 리미트와 원본 접점의 극성을 대조한다.
3. 반대 방향 동시 요청: 개방·폐쇄 두 출력의 상호 배제 조건을 Wires에서 추적한다. 현재 신호가 동시에 발생하는 경우 원인을 찾은 뒤 시험한다.
4. 위치 값·엔코더: 리미트 입력, 실제 밸브 위치, 엔코더 카운트, 환산 위치, 저장/전원 복귀 값을 같은 시각에 기록한다. 캘리브레이션 네트워크의 조건과 완료 신호를 확인한다.
5. 동작 지연·고장: 구동 출력 → 모터/인버터 → 기구부 → 리미트/엔코더 → 타이머/횟수 고장을 대조한다. 타이머 값은 원본과 설정 DB를 근거로 확정한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| MV01-SIM-01 | 개방·폐쇄 | 각 방향 요청을 분리 주입 | 출력 방향·끝 리미트 조건·반대 출력 상태 대조 | 설계·미실행 |
| MV01-SIM-02 | 동시 요청 | 열림/닫힘 요청 동시 ON | 원본 상호 배제 동작 검증 | 설계·미실행 |
| MV01-SIM-03 | 중간 위치 | 양 끝 리미트 0, 엔코더 중간 값 | 위치 환산·허용 방향·고장 시간 검증 | 설계·미실행 |
| MV01-SIM-04 | 리미트 모순 | 열림/닫힘 리미트 동시 1 | 경보·출력 반응을 원본으로 검증 | 설계·미실행 |
| MV01-SIM-05 | 자동/수동 전환 | 자동 제어 중 수동 요청 변경 | 요청 우선순위와 잔존 출력 검증 | 설계·미실행 |
| MV01-SIM-06 | 전원 복귀·교정 | 카운트 저장·재시작·교정 요청 | 원점 설정과 저장값 사용 경로 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| MV01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| MV01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| MV01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| MV01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| MV01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## MV02 · 모터 구동 밸브

PSH01 관련 배기/압력 경로 제어.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 30 / PDF 31, FG 31 / PDF 32, FG 36 / PDF 37, FG 37 / PDF 38.

확인할 특이점:  공통 전원 MV02/05/06은 개별 구동 피드백과 분리한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M11.7 | close mv02 pid | bool |  | 54 |
| %M11.6 | open mv02 pid | bool |  | 62 |
| %I1.4 | mv02_05_06_power_ok | bool | feedback inverter supply motors mv-02/mv-05/mv-06 | 494 |
| %I2.2 | mv02_fbk_opening | bool | feedback opening motor mv-02 | 499 |
| %I7.3 | mv02_open | bool | limit switch ls-17 | 659 |
| %Q1.5 | open mv02 | bool | a 57.2 mv-02 openingmotor command | 672 |
| %Q1.6 | close mv02 | bool | a 57.3 mv-02 closingmotor command | 673 |
| %I2.3 | mv02_fbk_closing | bool | feedback closing motor mv-02 | 882 |
| %I1.5 | mv02_05_06_inv_all | bool | alarm inverter supply motors mv-02/mv-05/mv-06 | 915 |
| %Q1.0 | start aux inv | bool | start inverter for valve motorized mv02-05-06 | 1280 |
| %M14.1 | pid mv02 down | bool |  | 1363 |
| %M14.0 | pid mv02 up | bool |  | 1364 |
| %I7.4 | mv02_close | bool | limit switch ls-18 | 1514 |
| %IW284 | psh01 | int | pressure control output mv-02 | 1540 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| MV_02\OutputOpen | DB11,X20.0 | PLC | 00350 |
| MV_02\AutoMan | DB2,X6.7 | PLC | 0034F |
| MV_02\Allarme1 | DB11,X20.2 | PLC | 00317 |
| MV_02\OutputClose | DB11,X20.1 | PLC | 0030A |
| MV_02\LimitSwitchOpen | DB11,X20.3 | PLC | 001A9 |
| MV_02\LimitSwitchClose | DB11,X20.4 | PLC | 001A8 |
| MV_02\Flag_CLOSE | DB2,X9.5 | PLC | 00041 |
| MV_02\Flag_OPEN | DB2,X9.6 | PLC | 00040 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| cyc_int4 ogni 200ms | 1 | for test trends | [네트워크 396](networks/network-396.html) | 4/11 |
| startup only | 4 | plants defaults | [네트워크 404](networks/network-404.html) | 10/14 |
| simulation | 5 | mv | [네트워크 1083](networks/network-1083.html) | 70/151 |
| hmi | 12 | mv02 | [네트워크 1189](networks/network-1189.html) | 1/15 |
| allarms 2 | 1 | mv-01 motorized valve fault | [네트워크 1226](networks/network-1226.html) | 59/103 |
| valve control loop | 3 | mv02 controlled by psh-01 | [네트워크 1704](networks/network-1704.html) | 33/57 |
| valve control loop | 12 | motorized valve pulse generator for rotation control | [네트워크 1713](networks/network-1713.html) | 42/95 |
| valve control loop | 13 | motorized valve fault | [네트워크 1714](networks/network-1714.html) | 43/87 |
| analog input conversion | 27 | reading encoder mv02 | [네트워크 1757](networks/network-1757.html) | 3/28 |
| analog input conversion | 33 | data management mv02 | [네트워크 1763](networks/network-1763.html) | 10/28 |
| cyc_int5 ogni 100ms | 4 | controll pc01 moduling mv02 | [네트워크 7](networks/network-7.html) | 5/30 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1704 | RCoil | Flag.M_MV02_OPEN | ((NOT [ON] AND NOT [Inputs.MV02 Open]) OR (NOT [ON] AND Flag.M_MV02_CLOSE) OR (NOT [ON] AND Flag.MV02_Auto)) | 조건 성립 시 Reset |
| 1704 | RCoil | Flag.M_MV02_CLOSE | ((NOT [ON] AND NOT [Inputs.MV02 Close]) OR (NOT [ON] AND Flag.M_MV02_OPEN) OR (NOT [ON] AND Flag.MV02_Auto)) | 조건 성립 시 Reset |
| 1704 | Coil | Open MV02 | ((((((((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.MV02_Auto) AND PID MV02 UP) OR ((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.M_MV02_OPEN)) AND MV WORK PULSE) OR (((((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.MV02_Auto) AND PID MV02 UP) OR ((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.M_MV02_OPEN)) AND ON)) AND NOT [Close MV02]) AND Inputs.MV02 Open) | 조건에 따른 Coil 기록 |
| 1704 | Coil | Close MV02 | ((((((((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.MV02_Auto) AND PID MV02 Down) OR ((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.M_MV02_CLOSE)) AND MV WORK PULSE) OR (((((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.MV02_Auto) AND PID MV02 Down) OR ((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.M_MV02_CLOSE)) AND ON)) AND NOT [Open MV02]) AND Inputs.MV02 Close) | 조건에 따른 Coil 기록 |
| 1763 | Coil | fill_unit1.CONTROL_SIGNALS.SW_GATE1 | (EM_OK AND NOT [MV02_Close]) | 조건에 따른 Coil 기록 |
| 1763 | Move | Memory encoder.Encoder_CH01_10 | Div UID 25.eno (블록 동작 확인) | Move 입력 CNTV1_100 |
| 1763 | Move | Memory encoder.Encoder_CH01_10 | (EM_OK AND NOT [fill_unit1.CONTROL_SIGNALS.SW_GATE1]) | Move 입력 0 |
| 1763 | Move | Memory encoder.Encoder_CH01 | (EM_OK AND NOT [fill_unit1.CONTROL_SIGNALS.SW_GATE1]) | Move 입력 INT#0 |


### 점검·진단 절차안

1. 공통 전원/구동 준비: 공통 인버터 전원 허가와 개별 열림/닫힘 구동 피드백을 따로 기록한다.
2. 수동·자동 요청: HMI 개방/폐쇄 요청, 자동 플래그, 관련 PID 또는 펄스 요청, 양 끝 리미트와 원본 접점의 극성을 대조한다.
3. 반대 방향 동시 요청: 개방·폐쇄 두 출력의 상호 배제 조건을 Wires에서 추적한다. 현재 신호가 동시에 발생하는 경우 원인을 찾은 뒤 시험한다.
4. 위치 값·엔코더: 리미트 입력, 실제 밸브 위치, 엔코더 카운트, 환산 위치, 저장/전원 복귀 값을 같은 시각에 기록한다. 캘리브레이션 네트워크의 조건과 완료 신호를 확인한다.
5. 동작 지연·고장: 구동 출력 → 모터/인버터 → 기구부 → 리미트/엔코더 → 타이머/횟수 고장을 대조한다. 타이머 값은 원본과 설정 DB를 근거로 확정한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| MV02-SIM-01 | 개방·폐쇄 | 각 방향 요청을 분리 주입 | 출력 방향·끝 리미트 조건·반대 출력 상태 대조 | 설계·미실행 |
| MV02-SIM-02 | 동시 요청 | 열림/닫힘 요청 동시 ON | 원본 상호 배제 동작 검증 | 설계·미실행 |
| MV02-SIM-03 | 중간 위치 | 양 끝 리미트 0, 엔코더 중간 값 | 위치 환산·허용 방향·고장 시간 검증 | 설계·미실행 |
| MV02-SIM-04 | 리미트 모순 | 열림/닫힘 리미트 동시 1 | 경보·출력 반응을 원본으로 검증 | 설계·미실행 |
| MV02-SIM-05 | 자동/수동 전환 | 자동 제어 중 수동 요청 변경 | 요청 우선순위와 잔존 출력 검증 | 설계·미실행 |
| MV02-SIM-06 | 전원 복귀·교정 | 카운트 저장·재시작·교정 요청 | 원점 설정과 저장값 사용 경로 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| MV02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| MV02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| MV02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| MV02-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| MV02-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |
| MV02-V-06 | 불일치/특이점 | 공통 전원 MV02/05/06은 개별 구동 피드백과 분리한다. | 확인 대기 |

## MV03 · 모터 구동 밸브

PSH03 관련 오버플로 경로 제어.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 38 / PDF 39, FG 39 / PDF 40.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q1.7 | start open mv03 | bool | a 52.5 mv-03 openingmotor command | 674 |
| %Q2.0 | start close mv03 | bool | a 52.6 mv-03 closingmotor command | 675 |
| %I2.4 | mv03_fbk_opening | bool | feedback opening motor mv-03 | 883 |
| %I2.5 | mv03_fbk_closing | bool | feedback closing motor mv-03 | 884 |
| %I7.5 | mv03_open | bool | limit switch ls-19 | 887 |
| %I7.6 | mv03_close | bool | limit switch ls-20 | 888 |
| %M180.5 | close mv03 for burner startup | bool |  | 1096 |
| %M14.5 | pid down mv03 | bool |  | 1357 |
| %M14.4 | pid up mv03 | bool |  | 1358 |
| %M48.1 | open mv03 for washing | bool |  | 1359 |
| %IW286 | psh02 | int | pressure control output mv-03 | 1539 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| RESET_ENC_MV03 | DB41,X50.6 | PLC | 00465 |
| MV_03\LimitSwitchClose | DB11,X22.4 | PLC | 0031B |
| MV_03\Flag_OPEN | DB2,X9.7 | PLC | 0031A |
| MV_03\Flag_CLOSE | DB2,X10.0 | PLC | 00319 |
| MV_03\Allarme1 | DB11,X22.2 | PLC | 00318 |
| MV_03\AutoMan | DB2,X7.0 | PLC | 0030D |
| MV_03\OutputOpen | DB11,X22.0 | PLC | 0030C |
| MV_03\OutputClose | DB11,X22.1 | PLC | 001A2 |
| MV_03\LimitSwitchOpen | DB11,X22.3 | PLC | 00043 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| startup only | 4 | plants defaults | [네트워크 404](networks/network-404.html) | 10/14 |
| hmi inputs | 1 |  | [네트워크 1070](networks/network-1070.html) | 33/62 |
| simulation | 5 | mv | [네트워크 1083](networks/network-1083.html) | 70/151 |
| hmi | 14 | mv03 | [네트워크 1191](networks/network-1191.html) | 1/15 |
| allarms 2 | 1 | mv-01 motorized valve fault | [네트워크 1226](networks/network-1226.html) | 59/103 |
| valve control loop | 4 | mv03 controlled by psh03 | [네트워크 1705](networks/network-1705.html) | 11/24 |
| valve control loop | 5 | mv03 controlled by psh03 | [네트워크 1706](networks/network-1706.html) | 41/73 |
| valve control loop | 6 | calibration encoder mv03 | [네트워크 1707](networks/network-1707.html) | 6/13 |
| valve control loop | 12 | motorized valve pulse generator for rotation control | [네트워크 1713](networks/network-1713.html) | 42/95 |
| valve control loop | 13 | motorized valve fault | [네트워크 1714](networks/network-1714.html) | 43/87 |
| analog input conversion | 28 | reading encoder mv03 | [네트워크 1758](networks/network-1758.html) | 3/28 |
| analog input conversion | 34 | mv03 data management | [네트워크 1764](networks/network-1764.html) | 10/28 |
| burner control | 15 | enable burner cleaning sequence | [네트워크 1868](networks/network-1868.html) | 71/151 |
| cyc_int5 ogni 100ms | 12 | control pc02 moduling mv03 - not used | [네트워크 15](networks/network-15.html) | 7/33 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1705 | SdCoil | Tag_148 | (ON AND NOT [Tag_147]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#4S |
| 1705 | SdCoil | Tag_147 | (ON AND Tag_148) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#10S |
| 1705 | Coil | PID down MV03 | ((ON AND NOT [Tag_148]) AND [ErrPSH03 >= 5]) | 조건에 따른 Coil 기록 |
| 1705 | Coil | PID UP MV03 | ((ON AND NOT [Tag_148]) AND [ErrPSH03 < -5]) | 조건에 따른 Coil 기록 |
| 1706 | RCoil | Flag.M_MV03_OPEN | ((ON AND Inputs.MV03 open) OR (ON AND Flag.M_MV03_CLOSE) OR (ON AND Flag.MV03_Auto)) | 조건 성립 시 Reset |
| 1706 | RCoil | Flag.M_MV03_CLOSE | ((ON AND Inputs.MV03 Close) OR (ON AND Flag.M_MV03_OPEN) OR (ON AND Flag.MV03_Auto)) | 조건 성립 시 Reset |
| 1706 | RCoil | Close MV03 for Burner Startup | (ON AND Inputs.MV03 Close) | 조건 성립 시 Reset |
| 1706 | Coil | Start open MV03 | (((((((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.MV03_Auto) AND PID UP MV03) AND MV WORK PULSE) OR ((((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.MV03_Auto) AND PID UP MV03) AND ON) OR (((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.M_MV03_OPEN) AND MV WORK PULSE) OR (((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.M_MV03_OPEN) AND ON) OR ((ON AND NOT [Allarm.MV03_FAULT]) AND Open MV03 for washing)) AND NOT [HMI_DB.ResetEncoderProcedure_MV03]) AND NOT [Inputs.MV03 open]) | 조건에 따른 Coil 기록 |
| 1706 | Coil | Start Close MV03 | ((((((((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.MV03_Auto) AND PID down MV03) AND MV WORK PULSE) OR ((((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.MV03_Auto) AND PID down MV03) AND ON) OR (((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.M_MV03_CLOSE) AND MV WORK PULSE) OR (((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.M_MV03_CLOSE) AND ON) OR ((ON AND NOT [Allarm.MV03_FAULT]) AND Close MV03 for Burner Startup)) AND NOT [Open MV03 for washing]) OR ((ON AND NOT [Allarm.MV03_FAULT]) AND HMI_DB.ResetEncoderProcedure_MV03)) AND NOT [Inputs.MV03 Close]) | 조건에 따른 Coil 기록 |
| 1707 | Move | MV03_Encoder.NewCountValue | (HMI_DB.ResetEncoderProcedure_MV03 AND Inputs.MV03 Close) | Move 입력 0 |
| 1707 | Coil | MV03_Encoder.SetCountValue | (Move UID 32.eno (블록 동작 확인) AND NOT [MV03_Encoder.SetCountValue]) | 조건에 따른 Coil 기록 |
| 1707 | RCoil | HMI_DB.ResetEncoderProcedure_MV03 | Coil UID 44.out (블록 동작 확인) | 조건 성립 시 Reset |
| 1764 | Coil | fill_unit1.CONTROL_SIGNALS.SW_GATE2 | (EM_OK AND NOT [Inputs.MV03 Close]) | 조건에 따른 Coil 기록 |
| 1764 | Move | Memory encoder.Encoder_CH02_10 | Div UID 1138.eno (블록 동작 확인) | Move 입력 CNTV2_100 |
| 1764 | Move | Memory encoder.Encoder_CH02_10 | (EM_OK AND NOT [fill_unit1.CONTROL_SIGNALS.SW_GATE2]) | Move 입력 0 |
| 1764 | Move | Memory encoder.Encoder_CH02 | (EM_OK AND NOT [fill_unit1.CONTROL_SIGNALS.SW_GATE2]) | Move 입력 INT#0 |


### 점검·진단 절차안

1. 공통 전원/구동 준비: 공통 인버터 전원 허가와 개별 열림/닫힘 구동 피드백을 따로 기록한다.
2. 수동·자동 요청: HMI 개방/폐쇄 요청, 자동 플래그, 관련 PID 또는 펄스 요청, 양 끝 리미트와 원본 접점의 극성을 대조한다.
3. 반대 방향 동시 요청: 개방·폐쇄 두 출력의 상호 배제 조건을 Wires에서 추적한다. 현재 신호가 동시에 발생하는 경우 원인을 찾은 뒤 시험한다.
4. 위치 값·엔코더: 리미트 입력, 실제 밸브 위치, 엔코더 카운트, 환산 위치, 저장/전원 복귀 값을 같은 시각에 기록한다. 캘리브레이션 네트워크의 조건과 완료 신호를 확인한다.
5. 동작 지연·고장: 구동 출력 → 모터/인버터 → 기구부 → 리미트/엔코더 → 타이머/횟수 고장을 대조한다. 타이머 값은 원본과 설정 DB를 근거로 확정한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| MV03-SIM-01 | 개방·폐쇄 | 각 방향 요청을 분리 주입 | 출력 방향·끝 리미트 조건·반대 출력 상태 대조 | 설계·미실행 |
| MV03-SIM-02 | 동시 요청 | 열림/닫힘 요청 동시 ON | 원본 상호 배제 동작 검증 | 설계·미실행 |
| MV03-SIM-03 | 중간 위치 | 양 끝 리미트 0, 엔코더 중간 값 | 위치 환산·허용 방향·고장 시간 검증 | 설계·미실행 |
| MV03-SIM-04 | 리미트 모순 | 열림/닫힘 리미트 동시 1 | 경보·출력 반응을 원본으로 검증 | 설계·미실행 |
| MV03-SIM-05 | 자동/수동 전환 | 자동 제어 중 수동 요청 변경 | 요청 우선순위와 잔존 출력 검증 | 설계·미실행 |
| MV03-SIM-06 | 전원 복귀·교정 | 카운트 저장·재시작·교정 요청 | 원점 설정과 저장값 사용 경로 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| MV03-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| MV03-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| MV03-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| MV03-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| MV03-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## MV04 · 모터 구동 밸브

FN02/HE01 경로의 모터 밸브. M18A/M18B 두 구동부를 구분한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 40 / PDF 41, FG 41 / PDF 42.

확인할 특이점: M18A/M18B 위치 입력 IW324/IW326과 개방/폐쇄 출력 Q2.1/Q2.2가 남아 있다. Analog input conversion에는 MV04 관련 입력을 MC04 전류로 사용하는 참조도 있어, 회로 라벨과 현재 프로그램 목적을 별도 확인해야 한다. 

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M11.2 | up mv04 pid | bool |  | 96 |
| %M11.3 | down mv04 pid | bool |  | 105 |
| %M11.1 | down tc03 pid mv04 | bool |  | 106 |
| %I2.6 | mv04_fbk_opening | bool | feedback opening motor mv-04 | 938 |
| %I2.7 | mv04_fbk_closing | bool | feedback closing motor mv-04 | 939 |
| %I7.7 | mv04_open | bool | limit switch ls21a/ls21b | 940 |
| %I8.0 | mv04_close | bool | limit switch ls-22a/ls-22b | 941 |
| %Q2.2 | close mv04 | bool | a 57.5 mv-04 closingmotor command | 982 |
| %Q2.1 | open mv04 | bool | a 57.4 mv-04 openingmotor command | 983 |
| %IW326 | mv04_m18b | int | mv-04 position m18b | 984 |
| %M14.3 | pid down mv04 | bool |  | 985 |
| %M14.2 | pid up mv04 | bool |  | 986 |
| %IW324 | mv04_m18a | int | mv-04 position m18a | 1726 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| I_MV_04_MV18B | DB13,INT58 | PLC | 00029 |
| I_MV_04_M18A | DB13,INT56 | PLC | 00028 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| startup only | 4 | plants defaults | [네트워크 404](networks/network-404.html) | 10/14 |
| allarms 2 | 1 | mv-01 motorized valve fault | [네트워크 1226](networks/network-1226.html) | 59/103 |
| valve control loop | 13 | motorized valve fault | [네트워크 1714](networks/network-1714.html) | 43/87 |
| analog input conversion | 39 | mc04 | [네트워크 1769](networks/network-1769.html) | 2/9 |
| cyc_int5 ogni 100ms | 9 | disable pid control on vt02 | [네트워크 12](networks/network-12.html) | 6/11 |

### 점검·진단 절차안

1. 공통 전원/구동 준비: 공통 인버터 전원 허가와 개별 열림/닫힘 구동 피드백을 따로 기록한다.
2. 수동·자동 요청: HMI 개방/폐쇄 요청, 자동 플래그, 관련 PID 또는 펄스 요청, 양 끝 리미트와 원본 접점의 극성을 대조한다.
3. 반대 방향 동시 요청: 개방·폐쇄 두 출력의 상호 배제 조건을 Wires에서 추적한다. 현재 신호가 동시에 발생하는 경우 원인을 찾은 뒤 시험한다.
4. 위치 값·엔코더: 리미트 입력, 실제 밸브 위치, 엔코더 카운트, 환산 위치, 저장/전원 복귀 값을 같은 시각에 기록한다. 캘리브레이션 네트워크의 조건과 완료 신호를 확인한다.
5. 동작 지연·고장: 구동 출력 → 모터/인버터 → 기구부 → 리미트/엔코더 → 타이머/횟수 고장을 대조한다. 타이머 값은 원본과 설정 DB를 근거로 확정한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| MV04-SIM-01 | 개방·폐쇄 | 각 방향 요청을 분리 주입 | 출력 방향·끝 리미트 조건·반대 출력 상태 대조 | 설계·미실행 |
| MV04-SIM-02 | 동시 요청 | 열림/닫힘 요청 동시 ON | 원본 상호 배제 동작 검증 | 설계·미실행 |
| MV04-SIM-03 | 중간 위치 | 양 끝 리미트 0, 엔코더 중간 값 | 위치 환산·허용 방향·고장 시간 검증 | 설계·미실행 |
| MV04-SIM-04 | 리미트 모순 | 열림/닫힘 리미트 동시 1 | 경보·출력 반응을 원본으로 검증 | 설계·미실행 |
| MV04-SIM-05 | 자동/수동 전환 | 자동 제어 중 수동 요청 변경 | 요청 우선순위와 잔존 출력 검증 | 설계·미실행 |
| MV04-SIM-06 | 전원 복귀·교정 | 카운트 저장·재시작·교정 요청 | 원점 설정과 저장값 사용 경로 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| MV04-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| MV04-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| MV04-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| MV04-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| MV04-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## MV05 · 모터 구동 밸브

RO01 관련 산소 제어 경로.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 30 / PDF 31, FG 31 / PDF 32, FG 34 / PDF 35, FG 35 / PDF 36.

확인할 특이점:  공통 전원 MV02/05/06은 개별 구동 피드백과 분리한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M11.4 | open mv05 pid | bool |  | 38 |
| %M11.5 | close mv05 pid | bool |  | 73 |
| %I1.4 | mv02_05_06_power_ok | bool | feedback inverter supply motors mv-02/mv-05/mv-06 | 494 |
| %I2.0 | mv05_fbk_opening | bool | feedback opening motor mv-05 | 497 |
| %I2.1 | mv05_fbk_closing | bool | feedback closing motor mv-05 | 498 |
| %I7.1 | mv05_open | bool | limit switch ls-15 | 658 |
| %Q1.3 | open mv05 | bool | a 48.2 mv-05 openingmotor command | 670 |
| %Q1.4 | close mv05 | bool | a 48.3 mv-05 closingmotor command | 671 |
| %I1.5 | mv02_05_06_inv_all | bool | alarm inverter supply motors mv-02/mv-05/mv-06 | 915 |
| %M13.1 | pid down mv05 | bool |  | 1365 |
| %M13.0 | pid up mv05 | bool |  | 1366 |
| %I7.2 | mv05_close | bool | limit switch ls-16 | 1513 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| MV_05\LimitSwitchOpen | DB11,X26.3 | PLC | 0040F |
| MV_05\Flag_CLOSE | DB2,X9.3 | PLC | 0031F |
| MV_05\Allarme1 | DB11,X26.2 | PLC | 0031E |
| MV_05\AutoMan | DB2,X6.6 | PLC | 00311 |
| MV_05\OutputOpen | DB11,X26.0 | PLC | 00310 |
| MV_05\OutputClose | DB11,X26.1 | PLC | 001A4 |
| MV_05\Flag_OPEN | DB2,X9.4 | PLC | 00045 |
| MV_05\LimitSwitchClose | DB11,X26.4 | PLC | 00044 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| startup only | 4 | plants defaults | [네트워크 404](networks/network-404.html) | 10/14 |
| simulation | 5 | mv | [네트워크 1083](networks/network-1083.html) | 70/151 |
| hmi | 11 | mv05 | [네트워크 1188](networks/network-1188.html) | 1/15 |
| allarms 2 | 1 | mv-01 motorized valve fault | [네트워크 1226](networks/network-1226.html) | 59/103 |
| valve control loop | 7 | mv05 controlled by ro-01 | [네트워크 1708](networks/network-1708.html) | 34/60 |
| valve control loop | 12 | motorized valve pulse generator for rotation control | [네트워크 1713](networks/network-1713.html) | 42/95 |
| valve control loop | 13 | motorized valve fault | [네트워크 1714](networks/network-1714.html) | 43/87 |
| analog input conversion | 29 | reading encoder mv05 | [네트워크 1759](networks/network-1759.html) | 3/28 |
| analog input conversion | 35 | mv05 data management | [네트워크 1765](networks/network-1765.html) | 10/28 |
| cyc_int5 ogni 100ms | 2 | controll ro01 moduling mv05 - pid | [네트워크 5](networks/network-5.html) | 8/35 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1708 | RCoil | Flag.M_MV05_OPEN | (((NOT [ORef UID 24] AND NOT [ON]) AND NOT [Inputs.MV05 open]) OR ((NOT [ORef UID 24] AND NOT [ON]) AND Flag.M_MV05_CLOSE) OR ((NOT [ORef UID 24] AND NOT [ON]) AND Flag.MV05_Auto)) | 조건 성립 시 Reset |
| 1708 | RCoil | Flag.M_MV05_CLOSE | (((NOT [ORef UID 24] AND NOT [ON]) AND NOT [Inputs.MV05 Close]) OR ((NOT [ORef UID 24] AND NOT [ON]) AND Flag.M_MV05_OPEN) OR ((NOT [ORef UID 24] AND NOT [ON]) AND Flag.MV05_Auto)) | 조건 성립 시 Reset |
| 1708 | Coil | Open MV05 | ((((((((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Flag.MV05_Auto) AND PID UP MV05) OR (((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Flag.M_MV05_OPEN) AND MV WORK PULSE)) AND NOT [Allarm.Oxigen_Fault]) OR (((((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Flag.MV05_Auto) AND PID UP MV05) OR (((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Flag.M_MV05_OPEN) AND MV WORK PULSE)) AND UNDER TESTING)) AND NOT [Close MV05]) AND Inputs.MV05 open) | 조건에 따른 Coil 기록 |
| 1708 | Coil | Close MV05 | ((((((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Flag.MV05_Auto) AND PID DOWN MV05) OR (((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Flag.M_MV05_CLOSE) AND MV WORK PULSE) OR (((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Allarm.Oxigen_Fault) AND NOT [UNDER TESTING])) AND NOT [Open MV05]) AND Inputs.MV05 Close) | 조건에 따른 Coil 기록 |
| 1765 | Coil | fill_unit1.CONTROL_SIGNALS.SW_GATE3 | (EM_OK AND NOT [MV05_Close]) | 조건에 따른 Coil 기록 |
| 1765 | Move | Memory encoder.Encoder_CH03_10 | Div UID 1242.eno (블록 동작 확인) | Move 입력 CNTV3_100 |
| 1765 | Move | Memory encoder.Encoder_CH03_10 | (EM_OK AND NOT [fill_unit1.CONTROL_SIGNALS.SW_GATE3]) | Move 입력 0 |
| 1765 | Move | Memory encoder.Encoder_CH03 | (EM_OK AND NOT [fill_unit1.CONTROL_SIGNALS.SW_GATE3]) | Move 입력 INT#0 |


### 점검·진단 절차안

1. 공통 전원/구동 준비: 공통 인버터 전원 허가와 개별 열림/닫힘 구동 피드백을 따로 기록한다.
2. 수동·자동 요청: HMI 개방/폐쇄 요청, 자동 플래그, 관련 PID 또는 펄스 요청, 양 끝 리미트와 원본 접점의 극성을 대조한다.
3. 반대 방향 동시 요청: 개방·폐쇄 두 출력의 상호 배제 조건을 Wires에서 추적한다. 현재 신호가 동시에 발생하는 경우 원인을 찾은 뒤 시험한다.
4. 위치 값·엔코더: 리미트 입력, 실제 밸브 위치, 엔코더 카운트, 환산 위치, 저장/전원 복귀 값을 같은 시각에 기록한다. 캘리브레이션 네트워크의 조건과 완료 신호를 확인한다.
5. 동작 지연·고장: 구동 출력 → 모터/인버터 → 기구부 → 리미트/엔코더 → 타이머/횟수 고장을 대조한다. 타이머 값은 원본과 설정 DB를 근거로 확정한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| MV05-SIM-01 | 개방·폐쇄 | 각 방향 요청을 분리 주입 | 출력 방향·끝 리미트 조건·반대 출력 상태 대조 | 설계·미실행 |
| MV05-SIM-02 | 동시 요청 | 열림/닫힘 요청 동시 ON | 원본 상호 배제 동작 검증 | 설계·미실행 |
| MV05-SIM-03 | 중간 위치 | 양 끝 리미트 0, 엔코더 중간 값 | 위치 환산·허용 방향·고장 시간 검증 | 설계·미실행 |
| MV05-SIM-04 | 리미트 모순 | 열림/닫힘 리미트 동시 1 | 경보·출력 반응을 원본으로 검증 | 설계·미실행 |
| MV05-SIM-05 | 자동/수동 전환 | 자동 제어 중 수동 요청 변경 | 요청 우선순위와 잔존 출력 검증 | 설계·미실행 |
| MV05-SIM-06 | 전원 복귀·교정 | 카운트 저장·재시작·교정 요청 | 원점 설정과 저장값 사용 경로 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| MV05-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| MV05-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| MV05-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| MV05-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| MV05-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |
| MV05-V-06 | 불일치/특이점 | 공통 전원 MV02/05/06은 개별 구동 피드백과 분리한다. | 확인 대기 |

## MV06 · 모터 구동 밸브

PSH02 관련 오버플로 경로 제어.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 30 / PDF 31, FG 31 / PDF 32, FG 32 / PDF 33, FG 33 / PDF 34.

확인할 특이점: P&ID의 LS34/LS35와 백업의 LS40/LS41을 서로 다른 출처 표기로 기록한다. 원본 루프에는 PSH02 기반 펄스·범위 조건과 별도 short-range 동작 네트워크가 있다. 공통 전원 MV02/05/06은 개별 구동 피드백과 분리한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M13.3 | mv06 pid down | bool |  | 82 |
| %M13.2 | mv06 pid up | bool |  | 83 |
| %I1.4 | mv02_05_06_power_ok | bool | feedback inverter supply motors mv-02/mv-05/mv-06 | 494 |
| %I1.6 | mv06_fbk_opening | bool | feedback opening motor mv-06 | 495 |
| %I1.7 | mv06_fbk_closing | bool | feedback closing motor mv-06 | 496 |
| %I6.7 | mv06_open | bool | limit switch ls.40 | 657 |
| %Q1.1 | open mv06 | bool | a 60.6 mv-06 openingmotor command | 668 |
| %Q1.2 | close mv06 | bool | a 60.7 mv-06 closingmotor command | 669 |
| %I1.5 | mv02_05_06_inv_all | bool | alarm inverter supply motors mv-02/mv-05/mv-06 | 915 |
| %I7.0 | mv06_close | bool | limit switch ls-41 | 1527 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| MV_06\Allarme1 | DB11,X28.2 | PLC | 0040E |
| MV_06\Flag_CLOSE | DB2,X10.6 | PLC | 0040D |
| MV_06\Flag_OPEN | DB2,X10.5 | PLC | 0040C |
| MV_06\LimitSwitchClose | DB11,X28.4 | PLC | 0040B |
| MV_06\LimitSwitchOpen | DB11,X28.3 | PLC | 0040A |
| MV_06\OutputClose | DB11,X28.1 | PLC | 00312 |
| MV_06\AutoMan | DB2,X6.5 | PLC | 00047 |
| MV_06\OutputOpen | DB11,X28.0 | PLC | 00046 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| startup only | 4 | plants defaults | [네트워크 404](networks/network-404.html) | 10/14 |
| simulation | 5 | mv | [네트워크 1083](networks/network-1083.html) | 70/151 |
| hmi | 10 | mv06 | [네트워크 1187](networks/network-1187.html) | 1/15 |
| allarms 2 | 1 | mv-01 motorized valve fault | [네트워크 1226](networks/network-1226.html) | 59/103 |
| valve control loop | 8 | mv06 controlled by psh02 | [네트워크 1709](networks/network-1709.html) | 12/27 |
| valve control loop | 9 | the working tool has a low range | [네트워크 1710](networks/network-1710.html) | 20/39 |
| valve control loop | 10 | mv06 controlled by psh02 | [네트워크 1711](networks/network-1711.html) | 33/59 |
| valve control loop | 12 | motorized valve pulse generator for rotation control | [네트워크 1713](networks/network-1713.html) | 42/95 |
| valve control loop | 13 | motorized valve fault | [네트워크 1714](networks/network-1714.html) | 43/87 |
| analog input conversion | 30 | reading encoder mv06 | [네트워크 1760](networks/network-1760.html) | 3/28 |
| analog input conversion | 36 | mv06 data management | [네트워크 1766](networks/network-1766.html) | 10/28 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1709 | SdCoil | Tag_150 | ((ON AND [Data.PSH02_SETPOINT != 0]) AND NOT [Tag_149]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#300MS |
| 1709 | SdCoil | Tag_149 | ((ON AND [Data.PSH02_SETPOINT != 0]) AND Tag_150) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#4S |
| 1709 | Coil | MV06 PID DOWN | (((ON AND [Data.PSH02_SETPOINT != 0]) AND NOT [Tag_150]) AND [ErrPSH02 >= 5]) | 조건에 따른 Coil 기록 |
| 1709 | Coil | MV06 PID UP | (((ON AND [Data.PSH02_SETPOINT != 0]) AND NOT [Tag_150]) AND [ErrPSH02 <= -5]) | 조건에 따른 Coil 기록 |
| 1711 | RCoil | Flag.MV06_Open | ((NOT [ON] AND Inputs.MV06_Open) OR (NOT [ON] AND Flag.MV06_Close) OR (NOT [ON] AND Flag.MV06_Auto)) | 조건 성립 시 Reset |
| 1711 | RCoil | Flag.MV06_Close | ((NOT [ON] AND Inputs.MV06 Close) OR (NOT [ON] AND Flag.MV06_Open) OR (NOT [ON] AND Flag.MV06_Auto)) | 조건 성립 시 Reset |
| 1711 | Coil | Open MV06 | ((((((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Auto) AND MV06 PID UP) OR (((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Auto) AND Shot to open) OR (((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Open) AND MV WORK PULSE) OR (((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Open) AND ON)) AND NOT [Close MV06]) AND NOT [Inputs.MV06_Open]) | 조건에 따른 Coil 기록 |
| 1711 | Coil | Close MV06 | ((((((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Auto) AND MV06 PID DOWN) OR (((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Auto) AND Shot to close) OR (((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Close) AND MV WORK PULSE) OR (((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Close) AND ON)) AND NOT [Open MV06]) AND NOT [Inputs.MV06 Close]) | 조건에 따른 Coil 기록 |
| 1766 | Coil | fill_unit1.CONTROL_SIGNALS.SW_GATE4 | (EM_OK AND NOT [MV06_Close]) | 조건에 따른 Coil 기록 |
| 1766 | Move | Memory encoder.Encoder_CH04_10 | Div UID 1450.eno (블록 동작 확인) | Move 입력 CNTV4_100 |
| 1766 | Move | Memory encoder.Encoder_CH04_10 | (EM_OK AND NOT [fill_unit1.CONTROL_SIGNALS.SW_GATE4]) | Move 입력 0 |
| 1766 | Move | Memory encoder.Encoder_CH04 | (EM_OK AND NOT [fill_unit1.CONTROL_SIGNALS.SW_GATE4]) | Move 입력 INT#0 |


### 점검·진단 절차안

1. 공통 전원/구동 준비: 공통 인버터 전원 허가와 개별 열림/닫힘 구동 피드백을 따로 기록한다.
2. 수동·자동 요청: HMI 개방/폐쇄 요청, 자동 플래그, 관련 PID 또는 펄스 요청, 양 끝 리미트와 원본 접점의 극성을 대조한다.
3. 반대 방향 동시 요청: 개방·폐쇄 두 출력의 상호 배제 조건을 Wires에서 추적한다. 현재 신호가 동시에 발생하는 경우 원인을 찾은 뒤 시험한다.
4. 위치 값·엔코더: 리미트 입력, 실제 밸브 위치, 엔코더 카운트, 환산 위치, 저장/전원 복귀 값을 같은 시각에 기록한다. 캘리브레이션 네트워크의 조건과 완료 신호를 확인한다.
5. 동작 지연·고장: 구동 출력 → 모터/인버터 → 기구부 → 리미트/엔코더 → 타이머/횟수 고장을 대조한다. 타이머 값은 원본과 설정 DB를 근거로 확정한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| MV06-SIM-01 | 개방·폐쇄 | 각 방향 요청을 분리 주입 | 출력 방향·끝 리미트 조건·반대 출력 상태 대조 | 설계·미실행 |
| MV06-SIM-02 | 동시 요청 | 열림/닫힘 요청 동시 ON | 원본 상호 배제 동작 검증 | 설계·미실행 |
| MV06-SIM-03 | 중간 위치 | 양 끝 리미트 0, 엔코더 중간 값 | 위치 환산·허용 방향·고장 시간 검증 | 설계·미실행 |
| MV06-SIM-04 | 리미트 모순 | 열림/닫힘 리미트 동시 1 | 경보·출력 반응을 원본으로 검증 | 설계·미실행 |
| MV06-SIM-05 | 자동/수동 전환 | 자동 제어 중 수동 요청 변경 | 요청 우선순위와 잔존 출력 검증 | 설계·미실행 |
| MV06-SIM-06 | 전원 복귀·교정 | 카운트 저장·재시작·교정 요청 | 원점 설정과 저장값 사용 경로 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| MV06-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| MV06-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| MV06-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| MV06-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| MV06-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |
| MV06-V-06 | 불일치/특이점 | 공통 전원 MV02/05/06은 개별 구동 피드백과 분리한다. | 확인 대기 |

## PV01 · 공압 게이트/분기 밸브

드럼 투입 A/B 게이트. EV01/02, CL01~04 및 위치 센서와 연결된다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 69 / PDF 70, FG 70 / PDF 71.

확인할 특이점: PV01의 8개 물리 I/O와 HMI 10개 설정은 기존 세부 매뉴얼에서 배선과 대조했다. 이번에는 R1 scraps gate 2의 원본 연결 구조를 추가했다. A/B 게이트 실제 명칭은 P&ID 상세도와 전기 입력·출력 회로를 함께 확인한다. 

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M20.0 | open ev a 00 pv-01 | bool |  | 39 |
| %M21.3 | open ev a 01 pv-01 | bool |  | 41 |
| %M20.2 | close ev a 00 pv-01 | bool |  | 46 |
| %M21.0 | close ev a 01 pv-01 | bool |  | 47 |
| %M22.3 | close ev a 02 pv-01 | bool |  | 49 |
| %M20.3 | close ev b 00 pv-01 | bool |  | 50 |
| %M21.2 | close ev b 01 pv-01 | bool |  | 51 |
| %M22.1 | close ev b 02 pv-01 | bool |  | 53 |
| %M21.1 | open ev b 01 pv-01 | bool |  | 59 |
| %M22.2 | open ev b 02 pv-01 | bool |  | 61 |
| %M10.7 | mem gate a open pv-01 | bool |  | 84 |
| %M10.6 | mem gate b open pv-01 | bool |  | 86 |
| %M22.0 | open ev a 02 pv-01 | bool |  | 99 |
| %M20.1 | open ev b 00 pv-01 | bool |  | 100 |
| %M80.5 | maintenance pv01 | bool |  | 474 |
| %I8.6 | ev01_open | bool | limit switch ls-01 gate "a" open | 662 |
| %I8.7 | ev01_close | bool | limit switch ls-02 gate "a" closed | 663 |
| %I9.0 | ev02_open | bool | limit switch ls-05 gate "b" open | 664 |
| %I9.1 | ev02_close | bool | limit switch ls-06 gate "b" closed | 665 |
| %I9.2 | ev01_sel_open | bool | opening gate "a"local selector | 877 |
| %I9.3 | ev02_sel_open | bool | opening gate "b"local selector | 878 |
| %M180.6 | memocmd_pv1_startup | bool |  | 1169 |
| %Q5.3 | pv-01 gate b ev | bool | a 48.4 ev-02 valvecommand | 1296 |
| %Q5.2 | pv-01 gate a | bool | a 57.0 ev-01 valvecommand | 1297 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| PV_01\GateA_Open | DB11,X76.1 | PLC | 000B1 |
| PV_01\Flag | DB2,X5.0 | PLC | 000B0 |
| PV_01\GateA_Close | DB11,X76.2 | PLC | 000AF |
| PV_01\GateB_Open | DB11,X76.3 | PLC | 000AE |
| PV_01\GateB_Close | DB11,X76.4 | PLC | 000AD |
| PV_01\Selector_GateA | DB11,X76.5 | PLC | 000AC |
| PV_01\Selector_GateB | DB11,X76.6 | PLC | 000AB |
| PV_01\Allarme1 | DB11,X76.0 | PLC | 000A9 |
| AbilitaMaintenance | DB2,X7.5 | PLC | 00409 |
| ResetAlarms | DB2,X13.4 | PLC | 002E1 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| startup only | 5 | default | [네트워크 405](networks/network-405.html) | 6/8 |
| simulation | 12 | pv01 | [네트워크 1090](networks/network-1090.html) | 8/13 |
| hmi | 38 | pv01 | [네트워크 1215](networks/network-1215.html) | 1/21 |
| allarms 1 | 35 | pv01 | [네트워크 1815](networks/network-1815.html) | 17/31 |
| allarms 1 | 36 | pv01 | [네트워크 1816](networks/network-1816.html) | 17/31 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| r1 scraps gate 2 | 1 | pv-01 | [네트워크 1911](networks/network-1911.html) | 19/31 |
| r1 scraps gate 2 | 3 | r1 gate loop pv-01 | [네트워크 1913](networks/network-1913.html) | 33/65 |
| r1 scraps gate 2 | 4 | evr4 scraps discharge door and gates selector pv-01 | [네트워크 1914](networks/network-1914.html) | 5/9 |
| r1 scraps gate 2 | 5 | a 48.4 ev-02 valvecommand | [네트워크 1915](networks/network-1915.html) | 12/21 |
| r1 scraps gate 2 | 11 | pv01 | [네트워크 1921](networks/network-1921.html) | 15/25 |
| r1 scraps gate 2 | 12 | pv01 | [네트워크 1922](networks/network-1922.html) | 17/29 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1090 | Coil | Inputs.FC GATE A OPEN | PV-01 Gate a | 조건에 따른 Coil 기록 |
| 1090 | Coil | Inputs.LIMIT SWITCH LS-02GATE A CLOSEDVALVE PV-01 | NOT [PV-01 Gate a] | 조건에 따른 Coil 기록 |
| 1090 | Coil | Inputs.PV-01 GATE B OPEN | PV-01 GATE B EV | 조건에 따른 Coil 기록 |
| 1090 | Coil | Inputs.LIMIT SWITCH LS-06GATE B CLOSEDVALVE PV-01 | NOT [PV-01 GATE B EV] | 조건에 따른 Coil 기록 |
| 1815 | SdCoil | Tag_80 | ((ON AND PV-01 Gate a) AND NOT [Flag.PV_01_GATE_A_MEM_OPEN]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#4S |
| 1815 | SCoil | Allarm.PV_01_GATE_A_NOT_OPEN | ((ON AND PV-01 Gate a) AND Tag_80) | 조건 성립 시 Set |
| 1815 | RCoil | Allarm.PV_01_GATE_A_NOT_OPEN | ((ON AND Flag.RESET_ALLARM) AND Allarm.PV_01_GATE_A_NOT_OPEN) | 조건 성립 시 Reset |
| 1815 | SdCoil | Tag_81 | ((ON AND NOT [PV-01 Gate a]) AND NOT [Flag.PV_01_GATE_A_MEM_CLOSE]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#4S |
| 1815 | SCoil | Allarm.PV_01_GATE_A_NOT_CLOSE | ((ON AND NOT [PV-01 Gate a]) AND Tag_81) | 조건 성립 시 Set |
| 1815 | RCoil | Allarm.PV_01_GATE_A_NOT_CLOSE | ((ON AND Flag.RESET_ALLARM) AND Allarm.PV_01_GATE_A_NOT_CLOSE) | 조건 성립 시 Reset |
| 1816 | SdCoil | Tag_82 | ((ON AND PV-01 GATE B EV) AND NOT [Flag.PV_01_GATE_B_MEM_OPEN]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#7S |
| 1816 | SCoil | Allarm.PV_01_GATE_B_NOT_OPEN | ((ON AND PV-01 GATE B EV) AND Tag_82) | 조건 성립 시 Set |
| 1816 | RCoil | Allarm.PV_01_GATE_B_NOT_OPEN | ((ON AND Flag.RESET_ALLARM) AND Allarm.PV_01_GATE_B_NOT_OPEN) | 조건 성립 시 Reset |
| 1816 | SdCoil | Tag_83 | ((ON AND NOT [PV-01 GATE B EV]) AND NOT [Flag.PV_01_GATE_B_MEM_CLOSE]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#7S |
| 1816 | SCoil | Allarm.PV_01_GATE_B_NOT_CLOSE | ((ON AND NOT [PV-01 GATE B EV]) AND Tag_83) | 조건 성립 시 Set |
| 1816 | RCoil | Allarm.PV_01_GATE_B_NOT_CLOSE | ((ON AND Flag.RESET_ALLARM) AND Allarm.PV_01_GATE_B_NOT_CLOSE) | 조건 성립 시 Reset |
| 1911 | Coil | R1 Gate ON | (((((ON OR (ON AND UNDER TESTING)) AND Flag.Enable_R1_GATE) AND NOT [Allarm.PV_01_GATE_A_NOT_OPEN]) AND NOT [Allarm.PV_01_GATE_B_NOT_OPEN]) OR ((((ON OR (ON AND UNDER TESTING)) AND NOT [Flag.Enable_R1_GATE]) AND Flag.PV_01_GATE_A_MEM_OPEN) AND Flag.PV_01_GATE_B_MEM_OPEN)) | 조건에 따른 Coil 기록 |
| 1911 | Coil | Flag.R1_GATE_LOOP_ON | (((((ON OR (ON AND UNDER TESTING)) AND Flag.Enable_R1_GATE) AND NOT [Allarm.PV_01_GATE_A_NOT_OPEN]) AND NOT [Allarm.PV_01_GATE_B_NOT_OPEN]) OR ((((ON OR (ON AND UNDER TESTING)) AND NOT [Flag.Enable_R1_GATE]) AND Flag.PV_01_GATE_A_MEM_OPEN) AND Flag.PV_01_GATE_B_MEM_OPEN)) | 조건에 따른 Coil 기록 |
| 1911 | Move | WorkData.R1State | (ON AND NOT [R1 Gate ON]) | Move 입력 0 |
| 1911 | RCoil | Open EV A 01  PV-01 | (ON AND NOT [R1 Gate ON]) | 조건 성립 시 Reset |
| 1911 | RCoil | Open EV B 01  PV-01 | (ON AND NOT [R1 Gate ON]) | 조건 성립 시 Reset |
| 1911 | RCoil | Close EV A 01  PV-01 | (ON AND NOT [R1 Gate ON]) | 조건 성립 시 Reset |
| 1911 | RCoil | Close EV B 01  PV-01 | (ON AND NOT [R1 Gate ON]) | 조건 성립 시 Reset |
| 1913 | SCoil | Close EV A 01  PV-01 | (((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 0]) | 조건 성립 시 Set |
| 1913 | RCoil | Open EV A 01  PV-01 | (((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 0]) | 조건 성립 시 Reset |
| 1913 | SdCoil | Tag_163 | (((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 0]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1S |
| 1913 | Move | WorkData.R1State | ((((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 0]) AND Tag_163) | Move 입력 1 |
| 1913 | SCoil | Open EV B 01  PV-01 | (((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 1]) | 조건 성립 시 Set |
| 1913 | RCoil | Close EV B 01  PV-01 | (((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 1]) | 조건 성립 시 Reset |
| 1913 | Move | WorkData.R1State | ((((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 1]) AND Flag.PV_01_GATE_B_MEM_OPEN) | Move 입력 2 |
| 1913 | SdCoil | Tag_164 | (((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 2]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 Data.SET_EVR1B_Open_time |
| 1913 | Move | WorkData.R1State | ((((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 2]) AND Tag_164) | Move 입력 3 |
| 1913 | SCoil | Close EV B 01  PV-01 | (((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 3]) | 조건 성립 시 Set |
| 1913 | RCoil | Open EV B 01  PV-01 | (((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 3]) | 조건 성립 시 Reset |
| 1913 | SdCoil | Tag_165 | (((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 3]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1S |
| 1913 | Move | WorkData.R1State | ((((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 3]) AND Tag_165) | Move 입력 4 |
| 1913 | SCoil | Open EV A 01  PV-01 | (((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 4]) | 조건 성립 시 Set |
| 1913 | RCoil | Close EV A 01  PV-01 | (((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 4]) | 조건 성립 시 Reset |
| 1913 | Move | WorkData.R1State | ((((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 4]) AND Flag.PV_01_GATE_A_MEM_OPEN) | Move 입력 5 |
| 1913 | SdCoil | Tag_166 | (((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 5]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 Data.SET_EVR1A_Open_time |
| 1913 | Move | WorkData.R1State | ((((ON AND Flag.Enable_R1_GATE) AND R1 Gate ON) AND [WorkData.R1State = 5]) AND Tag_166) | Move 입력 0 |
| 1914 | Coil | Open EV A 00 PV-01 | (ON AND EV01_Sel_Open) | 조건에 따른 Coil 기록 |
| 1914 | Coil | Open EV B 00  PV-01 | (ON AND EV02_Sel_Open) | 조건에 따른 Coil 기록 |
| 1915 | Coil | PV-01 GATE B EV | ((ON AND Open EV B 00  PV-01) OR (ON AND Open EV B 01  PV-01) OR (ON AND maintenance PV01) OR (ON AND OFF)) | 조건에 따른 Coil 기록 |
| 1915 | Coil | PV-01 Gate a | ((ON AND Open EV A 00 PV-01) OR (ON AND Open EV A 01  PV-01) OR (ON AND maintenance PV01)) | 조건에 따른 Coil 기록 |
| 1921 | SCoil | Flag.PV_01_GATE_A_MEM_OPEN | (((ON AND PV-01 Gate a) AND EV01_Open) OR ((ON AND PV-01 Gate a) AND Inputs.FC GATE A OPEN)) | 조건 성립 시 Set |
| 1921 | RCoil | Flag.PV_01_GATE_A_MEM_OPEN | (ON AND NOT [PV-01 Gate a]) | 조건 성립 시 Reset |
| 1921 | SCoil | Flag.PV_01_GATE_A_MEM_CLOSE | (((ON AND NOT [PV-01 Gate a]) AND EV01_Close) OR ((ON AND NOT [PV-01 Gate a]) AND Inputs.LIMIT SWITCH LS-02GATE A CLOSEDVALVE PV-01)) | 조건 성립 시 Set |
| 1921 | RCoil | Flag.PV_01_GATE_A_MEM_CLOSE | (ON AND PV-01 Gate a) | 조건 성립 시 Reset |
| 1922 | SCoil | Flag.PV_01_GATE_B_MEM_OPEN | (((ON AND PV-01 GATE B EV) AND EV02_Open) OR (((ON AND PV-01 GATE B EV) AND false) AND EV02_Close) OR ((ON AND PV-01 GATE B EV) AND Inputs.PV-01 GATE B OPEN)) | 조건 성립 시 Set |
| 1922 | RCoil | Flag.PV_01_GATE_B_MEM_OPEN | (ON AND NOT [PV-01 GATE B EV]) | 조건 성립 시 Reset |
| 1922 | SCoil | Flag.PV_01_GATE_B_MEM_CLOSE | (((ON AND NOT [PV-01 GATE B EV]) AND EV02_Close) OR ((ON AND NOT [PV-01 GATE B EV]) AND Inputs.LIMIT SWITCH LS-06GATE B CLOSEDVALVE PV-01)) | 조건 성립 시 Set |
| 1922 | RCoil | Flag.PV_01_GATE_B_MEM_CLOSE | (ON AND PV-01 GATE B EV) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 공압·현장 요청: 공기 공급과 저압 스위치, 현장 선택 스위치, 솔레노이드 전원 및 구동 릴레이를 확인한다.
2. 위치 상태: 열림만 1, 닫힘만 1, 둘 다 0, 둘 다 1을 구분하고 원시 I, 내부 기억 비트, HMI 가공 상태를 동시에 기록한다.
3. 출력 경로: HMI 요청 → 상태/기억 비트 → 물리 Q → 중간 릴레이 → 솔레노이드 → 실린더 → 위치 센서 순서로 확인한다.
4. 게이트 순서: A/B 두 게이트 장치는 상태 값, 각 단계 진입 조건, Set/Reset 출력, 시간 조건과 다음 상태 Move를 원본 XML로 대조한다.
5. 복귀·전원 재시작: 닫힘 상태, 잔존 요청과 기억 비트, 공기 복귀 상태, 초기화 네트워크의 조건을 기록한 후 정상 순서 시험을 설계한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| PV01-SIM-01 | 정상 위치 전환 | 닫힘→중간→열림 | I/기억 비트/HMI 상태/Q 경로 확인 | 설계·미실행 |
| PV01-SIM-02 | 위치 모순 | 열림·닫힘 모두 1 | 원본 경보·진행 조건 확인 | 설계·미실행 |
| PV01-SIM-03 | 도달 실패 | 출력 요청 후 위치 입력 미도달 | 타이머·알람·다음 단계 차단 확인 | 설계·미실행 |
| PV01-SIM-04 | 공기/현장 요청 | 저압·현장 셀렉터 상태 변경 | 공통 허가·현장 우선순위 대조 | 설계·미실행 |
| PV01-SIM-05 | 전원 복귀 | 초기/중간 위치로 재시작 | 기억과 요청의 초기화 및 재순서 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| PV01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| PV01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| PV01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| PV01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| PV01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## PV02 · 공압 게이트/분기 밸브

드럼 배출 A/B 게이트. EV04/05, CL05~08 및 위치 센서와 연결된다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 71 / PDF 72, FG 72 / PDF 73.

확인할 특이점: PV02는 PV01과 다른 상태 변수·센서·출력을 가진다. A 개방/폐쇄 I9.4/I9.5, B 개방/폐쇄 I9.6/I9.7, EV04/05 출력 Q5.4/Q5.5를 백업 심볼과 대조한다. PV01의 시간값이나 순서식을 복사하지 않는다. 

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M30.4 | open ev a 00 pv-02 | bool |  | 40 |
| %M12.2 | pv-02 gate on | bool |  | 45 |
| %M30.0 | close ev a 01 pv-02 | bool |  | 48 |
| %M30.2 | close ev b 01 pv-02 | bool |  | 52 |
| %M30.1 | open ev b 01 pv-02 | bool |  | 60 |
| %M12.4 | mem gate a open pv-02 | bool |  | 85 |
| %M12.3 | mem gate b open pv-02 | bool |  | 87 |
| %M30.3 | open ev a 01 pv-02 | bool |  | 98 |
| %M80.6 | maintenance pv02 | bool |  | 475 |
| %I9.5 | ev04_close | bool | e29.7 limit switch ls-26gate "a" closed | 666 |
| %I9.7 | ev05_close | bool | e29.3 limit switch ls-30gate "b" closed | 667 |
| %M30.5 | open ev b 00 pv-02 | bool |  | 785 |
| %I10.0 | selector op gate a pv-02 | bool | e45.4 opening gate "a"local selector | 875 |
| %I10.1 | selector op gate b pv-02 | bool | e45.5 opening gate "b"local selector | 876 |
| %I9.4 | ev04_open | bool | e29.6 limit switch ls-25gate "a" open | 1166 |
| %I9.6 | ev05_open | bool | e29.2 limit switch ls-29gate "b" open | 1167 |
| %Q5.5 | pv-02 gate b ev | bool | a 56.4 ev-05 valvecommand | 1294 |
| %Q5.4 | pv-02 gate a ev | bool | a 53.7 ev-04 valvecommand | 1295 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| PV_02\Flag | DB2,X10.3 | PLC | 000A8 |
| PV_02\GateA_Open | DB11,X78.1 | PLC | 000A6 |
| PV_02\GateA_Close | DB11,X78.2 | PLC | 000A5 |
| PV_02\GateB_Open | DB11,X78.3 | PLC | 00077 |
| PV_02\GateB_Close | DB11,X78.4 | PLC | 00076 |
| PV_02\Selector_GateA | DB11,X78.5 | PLC | 00075 |
| PV_02\Selector_GateB | DB11,X78.6 | PLC | 00074 |
| PV_02\Allarme1 | DB11,X78.0 | PLC | 00073 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| startup only | 5 | default | [네트워크 405](networks/network-405.html) | 6/8 |
| simulation | 13 | pv02 | [네트워크 1091](networks/network-1091.html) | 8/13 |
| hmi | 39 | pv02 | [네트워크 1216](networks/network-1216.html) | 1/21 |
| allarms 1 | 37 | pv02 | [네트워크 1817](networks/network-1817.html) | 17/31 |
| allarms 1 | 38 | pv02 | [네트워크 1818](networks/network-1818.html) | 17/31 |
| r1 scraps gate 2 | 6 | pv-02 rotary drum discharge valve | [네트워크 1916](networks/network-1916.html) | 20/33 |
| r1 scraps gate 2 | 8 | r1 gate loop pv-02 | [네트워크 1918](networks/network-1918.html) | 33/65 |
| r1 scraps gate 2 | 9 | evr4 scraps discharge door and gates selector pv-02 | [네트워크 1919](networks/network-1919.html) | 5/9 |
| r1 scraps gate 2 | 10 | a 56.4 ev-05 valvecommand | [네트워크 1920](networks/network-1920.html) | 11/19 |
| r1 scraps gate 2 | 13 | pv02 | [네트워크 1923](networks/network-1923.html) | 15/25 |
| r1 scraps gate 2 | 14 | pv02 | [네트워크 1924](networks/network-1924.html) | 15/25 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1091 | Coil | Inputs.PV-02 EV A OPEN | PV-02 GATE A EV | 조건에 따른 Coil 기록 |
| 1091 | Coil | Inputs.PV-02 EV A CLOSE | NOT [PV-02 GATE A EV] | 조건에 따른 Coil 기록 |
| 1091 | Coil | Inputs.PV-02 GATE B OPEN | PV-02 GATE B EV | 조건에 따른 Coil 기록 |
| 1091 | Coil | Inputs.PV-02 GATE B CLOSE | NOT [PV-02 GATE B EV] | 조건에 따른 Coil 기록 |
| 1817 | SdCoil | Tag_84 | ((ON AND PV-02 GATE A EV) AND NOT [Flag.PV_02_GATE_A_MEM_OPEN]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#7S |
| 1817 | SCoil | Allarm.PV_02_GATE_A_NOT_OPEN | ((ON AND PV-02 GATE A EV) AND Tag_84) | 조건 성립 시 Set |
| 1817 | RCoil | Allarm.PV_02_GATE_A_NOT_OPEN | ((ON AND Flag.RESET_ALLARM) AND Allarm.PV_02_GATE_A_NOT_OPEN) | 조건 성립 시 Reset |
| 1817 | SdCoil | Tag_85 | ((ON AND NOT [PV-02 GATE A EV]) AND NOT [Flag.PV_02_GATE_A_MEM_CLOSE]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#7S |
| 1817 | SCoil | Allarm.PV_02_GATE_A_NOT_CLOSE | ((ON AND NOT [PV-02 GATE A EV]) AND Tag_85) | 조건 성립 시 Set |
| 1817 | RCoil | Allarm.PV_02_GATE_A_NOT_CLOSE | ((ON AND Flag.RESET_ALLARM) AND Allarm.PV_02_GATE_A_NOT_CLOSE) | 조건 성립 시 Reset |
| 1818 | SdCoil | Tag_86 | ((ON AND PV-02 GATE B EV) AND NOT [Flag.PV_02_GATE_B_MEM_OPEN]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#7S |
| 1818 | SCoil | Allarm.PV_02_GATE_B_NOT_OPEN | ((ON AND PV-02 GATE B EV) AND Tag_86) | 조건 성립 시 Set |
| 1818 | RCoil | Allarm.PV_02_GATE_B_NOT_OPEN | ((ON AND Flag.RESET_ALLARM) AND Allarm.PV_02_GATE_B_NOT_OPEN) | 조건 성립 시 Reset |
| 1818 | SdCoil | Tag_87 | ((ON AND NOT [PV-02 GATE B EV]) AND NOT [Flag.PV_02_GATE_B_MEM_CLOSE]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#7S |
| 1818 | SCoil | Allarm.PV_02_GATE_B_NOT_CLOSE | ((ON AND NOT [PV-02 GATE B EV]) AND Tag_87) | 조건 성립 시 Set |
| 1818 | RCoil | Allarm.PV_02_GATE_B_NOT_CLOSE | ((ON AND Flag.RESET_ALLARM) AND Allarm.PV_02_GATE_B_NOT_CLOSE) | 조건 성립 시 Reset |
| 1916 | Coil | PV-02 Gate ON | ((((((ON AND MC04_Fbk) OR (ON AND Inputs.MC04 run) OR (ON AND Allarm.Maintenance_ON)) AND Flag.Enable_R2_GATE) AND NOT [Allarm.PV_02_GATE_A_NOT_OPEN]) AND NOT [Allarm.PV_02_GATE_B_NOT_OPEN]) OR (((((ON AND MC04_Fbk) OR (ON AND Inputs.MC04 run) OR (ON AND Allarm.Maintenance_ON)) AND NOT [Flag.Enable_R2_GATE]) AND Flag.PV_02_GATE_A_MEM_OPEN) AND Flag.PV_02_GATE_B_MEM_OPEN)) | 조건에 따른 Coil 기록 |
| 1916 | Coil | Flag.R2_GATE_LOOP_ON | ((((((ON AND MC04_Fbk) OR (ON AND Inputs.MC04 run) OR (ON AND Allarm.Maintenance_ON)) AND Flag.Enable_R2_GATE) AND NOT [Allarm.PV_02_GATE_A_NOT_OPEN]) AND NOT [Allarm.PV_02_GATE_B_NOT_OPEN]) OR (((((ON AND MC04_Fbk) OR (ON AND Inputs.MC04 run) OR (ON AND Allarm.Maintenance_ON)) AND NOT [Flag.Enable_R2_GATE]) AND Flag.PV_02_GATE_A_MEM_OPEN) AND Flag.PV_02_GATE_B_MEM_OPEN)) | 조건에 따른 Coil 기록 |
| 1916 | Move | WorkData.W7 | (ON AND NOT [PV-02 Gate ON]) | Move 입력 0 |
| 1916 | RCoil | Open EV A 01  PV-02 | (ON AND NOT [PV-02 Gate ON]) | 조건 성립 시 Reset |
| 1916 | RCoil | Open EV B 01  PV-02 | (ON AND NOT [PV-02 Gate ON]) | 조건 성립 시 Reset |
| 1916 | RCoil | Close EV A 01  PV-02 | (ON AND NOT [PV-02 Gate ON]) | 조건 성립 시 Reset |
| 1916 | RCoil | Close EV B 01  PV-02 | (ON AND NOT [PV-02 Gate ON]) | 조건 성립 시 Reset |
| 1918 | SCoil | Close EV A 01  PV-02 | (((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 0]) | 조건 성립 시 Set |
| 1918 | RCoil | Open EV A 01  PV-02 | (((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 0]) | 조건 성립 시 Reset |
| 1918 | SdCoil | Tag_167 | (((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 0]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#300MS |
| 1918 | Move | WorkData.W7 | ((((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 0]) AND Tag_167) | Move 입력 1 |
| 1918 | SCoil | Open EV B 01  PV-02 | (((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 1]) | 조건 성립 시 Set |
| 1918 | RCoil | Close EV B 01  PV-02 | (((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 1]) | 조건 성립 시 Reset |
| 1918 | Move | WorkData.W7 | ((((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 1]) AND Flag.PV_02_GATE_B_MEM_OPEN) | Move 입력 2 |
| 1918 | SdCoil | Tag_168 | (((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 2]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 Data.SET_PV02B_Open_time |
| 1918 | Move | WorkData.W7 | ((((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 2]) AND Tag_168) | Move 입력 3 |
| 1918 | SCoil | Close EV B 01  PV-02 | (((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 3]) | 조건 성립 시 Set |
| 1918 | RCoil | Open EV B 01  PV-02 | (((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 3]) | 조건 성립 시 Reset |
| 1918 | SdCoil | Tag_169 | (((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 3]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#800MS |
| 1918 | Move | WorkData.W7 | ((((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 3]) AND Tag_169) | Move 입력 4 |
| 1918 | SCoil | Open EV A 01  PV-02 | (((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 4]) | 조건 성립 시 Set |
| 1918 | RCoil | Close EV A 01  PV-02 | (((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 4]) | 조건 성립 시 Reset |
| 1918 | Move | WorkData.W7 | ((((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 4]) AND Flag.PV_02_GATE_A_MEM_OPEN) | Move 입력 5 |
| 1918 | SdCoil | Tag_170 | (((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 5]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 Data.SET_PV02A_Open_time |
| 1918 | Move | WorkData.W7 | ((((ON AND Flag.Enable_R2_GATE) AND PV-02 Gate ON) AND [WorkData.W7 = 5]) AND Tag_170) | Move 입력 0 |
| 1919 | Coil | Open EV A 00 PV-02 | (ON AND Selector Op Gate A PV-02) | 조건에 따른 Coil 기록 |
| 1919 | Coil | Open EV B 00  PV-02 | (ON AND Selector Op Gate B PV-02) | 조건에 따른 Coil 기록 |
| 1920 | Coil | PV-02 GATE B EV | ((ON AND Open EV B 00  PV-02) OR (ON AND Open EV B 01  PV-02) OR (ON AND maintenance PV02)) | 조건에 따른 Coil 기록 |
| 1920 | Coil | PV-02 GATE A EV | ((ON AND Open EV A 00 PV-02) OR (ON AND Open EV A 01  PV-02) OR (ON AND maintenance PV02)) | 조건에 따른 Coil 기록 |
| 1923 | SCoil | Flag.PV_02_GATE_A_MEM_OPEN | (((ON AND PV-02 GATE A EV) AND EV04_Open) OR ((ON AND PV-02 GATE A EV) AND Inputs.PV-02 EV A OPEN)) | 조건 성립 시 Set |
| 1923 | RCoil | Flag.PV_02_GATE_A_MEM_OPEN | (ON AND NOT [PV-02 GATE A EV]) | 조건 성립 시 Reset |
| 1923 | SCoil | Flag.PV_02_GATE_A_MEM_CLOSE | (((ON AND NOT [PV-02 GATE A EV]) AND EV04_Close) OR ((ON AND NOT [PV-02 GATE A EV]) AND Inputs.PV-02 EV A CLOSE)) | 조건 성립 시 Set |
| 1923 | RCoil | Flag.PV_02_GATE_A_MEM_CLOSE | (ON AND PV-02 GATE A EV) | 조건 성립 시 Reset |
| 1924 | SCoil | Flag.PV_02_GATE_B_MEM_OPEN | (((ON AND PV-02 GATE B EV) AND EV05_Open) OR ((ON AND PV-02 GATE B EV) AND Inputs.PV-02 GATE B OPEN)) | 조건 성립 시 Set |
| 1924 | RCoil | Flag.PV_02_GATE_B_MEM_OPEN | (ON AND NOT [PV-02 GATE B EV]) | 조건 성립 시 Reset |
| 1924 | SCoil | Flag.PV_02_GATE_B_MEM_CLOSE | (((ON AND NOT [PV-02 GATE B EV]) AND EV05_Close) OR ((ON AND NOT [PV-02 GATE B EV]) AND Inputs.PV-02 GATE B CLOSE)) | 조건 성립 시 Set |
| 1924 | RCoil | Flag.PV_02_GATE_B_MEM_CLOSE | (ON AND PV-02 GATE B EV) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 공압·현장 요청: 공기 공급과 저압 스위치, 현장 선택 스위치, 솔레노이드 전원 및 구동 릴레이를 확인한다.
2. 위치 상태: 열림만 1, 닫힘만 1, 둘 다 0, 둘 다 1을 구분하고 원시 I, 내부 기억 비트, HMI 가공 상태를 동시에 기록한다.
3. 출력 경로: HMI 요청 → 상태/기억 비트 → 물리 Q → 중간 릴레이 → 솔레노이드 → 실린더 → 위치 센서 순서로 확인한다.
4. 게이트 순서: A/B 두 게이트 장치는 상태 값, 각 단계 진입 조건, Set/Reset 출력, 시간 조건과 다음 상태 Move를 원본 XML로 대조한다.
5. 복귀·전원 재시작: 닫힘 상태, 잔존 요청과 기억 비트, 공기 복귀 상태, 초기화 네트워크의 조건을 기록한 후 정상 순서 시험을 설계한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| PV02-SIM-01 | 정상 위치 전환 | 닫힘→중간→열림 | I/기억 비트/HMI 상태/Q 경로 확인 | 설계·미실행 |
| PV02-SIM-02 | 위치 모순 | 열림·닫힘 모두 1 | 원본 경보·진행 조건 확인 | 설계·미실행 |
| PV02-SIM-03 | 도달 실패 | 출력 요청 후 위치 입력 미도달 | 타이머·알람·다음 단계 차단 확인 | 설계·미실행 |
| PV02-SIM-04 | 공기/현장 요청 | 저압·현장 셀렉터 상태 변경 | 공통 허가·현장 우선순위 대조 | 설계·미실행 |
| PV02-SIM-05 | 전원 복귀 | 초기/중간 위치로 재시작 | 기억과 요청의 초기화 및 재순서 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| PV02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| PV02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| PV02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| PV02-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| PV02-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## PV03 · 공압 게이트/분기 밸브

스크린 배출 분기 밸브. EV06, CL09/10에 연결된다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 73 / PDF 74.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I10.2 | deviator open pv-03 | bool | e29.4 limit switchls-09 | 879 |
| %I10.3 | deviator close pv-03 | bool | e29.5 limit switchls-10 | 880 |
| %I10.4 | pv03 local selector | bool | e65.7 73sa1 deviatorev-06 selector | 881 |
| %Q5.6 | pv-03 gate ev | bool | a 56.5 ev-06 valvecommand | 1293 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| PV_03\Flag | DB2,X11.2 | PLC | 00072 |
| PV_03\LS_Open | DB11,X80.0 | PLC | 00070 |
| PV_03\LS_Close | DB11,X80.1 | PLC | 0006F |
| PV_03\Allarme1 | DB11,X80.3 | PLC | 0006E |
| PV_03\Selector | DB11,X80.2 | PLC | 0006D |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| startup only | 5 | default | [네트워크 405](networks/network-405.html) | 6/8 |
| simulation | 9 | pv03 | [네트워크 1087](networks/network-1087.html) | 4/7 |
| hmi | 40 | pv03 | [네트워크 1217](networks/network-1217.html) | 1/13 |
| allarms 1 | 39 | pv03 | [네트워크 1819](networks/network-1819.html) | 17/31 |
| r1 scraps gate 2 | 15 | pv03 | [네트워크 1925](networks/network-1925.html) | 17/29 |
| motors 1 | 43 | pv03 | [네트워크 1972](networks/network-1972.html) | 7/12 |
| motors 1 | 44 | liw feeder | [네트워크 1973](networks/network-1973.html) | 13/24 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1087 | Coil | Inputs.Deviator Open PV-03 | Flag.M_PV03 | 조건에 따른 Coil 기록 |
| 1087 | Coil | Inputs.Deviator Close PV-03 | NOT [Flag.M_PV03] | 조건에 따른 Coil 기록 |
| 1819 | SdCoil | Tag_88 | ((ON AND PV-03 GATE EV) AND NOT [Flag.PV_03_GATE_MEM_OPEN]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#5S |
| 1819 | SCoil | Allarm.PV_03_GATE_NOT_OPEN1 | ((ON AND PV-03 GATE EV) AND Tag_88) | 조건 성립 시 Set |
| 1819 | RCoil | Allarm.PV_03_GATE_NOT_OPEN1 | ((ON AND Flag.RESET_ALLARM) AND Allarm.PV_03_GATE_NOT_OPEN1) | 조건 성립 시 Reset |
| 1819 | SdCoil | Tag_89 | ((ON AND NOT [PV-03 GATE EV]) AND NOT [Flag.PV_03_GATE_MEM_CLOSE]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#5S |
| 1819 | SCoil | Allarm.PV_03_GATE_NOT_CLOSE1 | ((ON AND NOT [PV-03 GATE EV]) AND Tag_89) | 조건 성립 시 Set |
| 1819 | RCoil | Allarm.PV_03_GATE_NOT_CLOSE1 | ((ON AND Flag.RESET_ALLARM) AND Allarm.PV_03_GATE_NOT_CLOSE1) | 조건 성립 시 Reset |
| 1925 | SCoil | Flag.PV_03_GATE_MEM_OPEN | (((ON AND PV-03 GATE EV) AND Deviator Open PV-03) OR ((ON AND PV-03 GATE EV) AND Inputs.Deviator Open PV-03) OR ((ON AND PV-03 GATE EV) AND Flag.M_PV03)) | 조건 성립 시 Set |
| 1925 | RCoil | Flag.PV_03_GATE_MEM_OPEN | (ON AND NOT [PV-03 GATE EV]) | 조건 성립 시 Reset |
| 1925 | SCoil | Flag.PV_03_GATE_MEM_CLOSE | (((ON AND NOT [PV-03 GATE EV]) AND Deviator Close PV-03) OR ((ON AND NOT [PV-03 GATE EV]) AND Inputs.Deviator Close PV-03) OR ((ON AND NOT [PV-03 GATE EV]) AND NOT [Flag.M_PV03])) | 조건 성립 시 Set |
| 1925 | RCoil | Flag.PV_03_GATE_MEM_CLOSE | (ON AND PV-03 GATE EV) | 조건 성립 시 Reset |
| 1972 | RCoil | Flag.M_PV03 | (ON AND OFF) | 조건 성립 시 Reset |
| 1972 | Coil | PV-03 GATE EV | ((ON AND Flag.M_PV03) OR (ON AND Inputs.PV03 Local Selector)) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 공압·현장 요청: 공기 공급과 저압 스위치, 현장 선택 스위치, 솔레노이드 전원 및 구동 릴레이를 확인한다.
2. 위치 상태: 열림만 1, 닫힘만 1, 둘 다 0, 둘 다 1을 구분하고 원시 I, 내부 기억 비트, HMI 가공 상태를 동시에 기록한다.
3. 출력 경로: HMI 요청 → 상태/기억 비트 → 물리 Q → 중간 릴레이 → 솔레노이드 → 실린더 → 위치 센서 순서로 확인한다.
4. 게이트 순서: A/B 두 게이트 장치는 상태 값, 각 단계 진입 조건, Set/Reset 출력, 시간 조건과 다음 상태 Move를 원본 XML로 대조한다.
5. 복귀·전원 재시작: 닫힘 상태, 잔존 요청과 기억 비트, 공기 복귀 상태, 초기화 네트워크의 조건을 기록한 후 정상 순서 시험을 설계한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| PV03-SIM-01 | 정상 위치 전환 | 닫힘→중간→열림 | I/기억 비트/HMI 상태/Q 경로 확인 | 설계·미실행 |
| PV03-SIM-02 | 위치 모순 | 열림·닫힘 모두 1 | 원본 경보·진행 조건 확인 | 설계·미실행 |
| PV03-SIM-03 | 도달 실패 | 출력 요청 후 위치 입력 미도달 | 타이머·알람·다음 단계 차단 확인 | 설계·미실행 |
| PV03-SIM-04 | 공기/현장 요청 | 저압·현장 셀렉터 상태 변경 | 공통 허가·현장 우선순위 대조 | 설계·미실행 |
| PV03-SIM-05 | 전원 복귀 | 초기/중간 위치로 재시작 | 기억과 요청의 초기화 및 재순서 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| PV03-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| PV03-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| PV03-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| PV03-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| PV03-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## PV04 · 공압 게이트/분기 밸브

드럼 배출실 밸브. EV07, CL11에 연결된다.

자료 상태: 예비 표기·삭제 제목. 상위: 해당 없음. 전기: FG 74 / PDF 75.

확인할 특이점: I10.5/I10.6, Q5.7 및 현장 입력 I10.7은 잔존한다. 전기 SPARE 및 pv04 deleted 제목 때문에 현재 자동 운전 대상이라고 확정할 수 없다. 회로 및 출력 SPARE와 pv04 deleted 제목을 확인해야 한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I10.5 | pv04 open | bool | e 45.0 pv 04 ls33 open | 943 |
| %I10.6 | pv04 close | bool | e36.6 limit switchls-32 | 944 |
| %Q5.7 | pv-04 | bool | a 57.1 ev-07 valvecommand | 988 |
| %I10.7 | button open pv-0000 | bool | e 37.6 74sb1 diverterv-07 selector | 989 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| PV_04\Flag | DB2,X4.1 | PLC | 0006B |
| PV_04\LS_Open | DB11,X82.0 | PLC | 00069 |
| PV_04\LS_Close | DB11,X82.1 | PLC | 00068 |
| PV_04\Push_Button | DB11,X82.2 | PLC | 00067 |
| PV_04\Allarme1 | DB11,X82.3 | PLC | 00066 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| simulation | 10 | pv04 | [네트워크 1088](networks/network-1088.html) | 4/7 |
| hmi | 41 | pv04 | [네트워크 1218](networks/network-1218.html) | 1/13 |
| motors 1 | 18 |  | [네트워크 1947](networks/network-1947.html) | 1/4 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1088 | Coil | Inputs.PV04 Open | Flag.M_PV04 | 조건에 따른 Coil 기록 |
| 1088 | Coil | Inputs.PV04 Close | NOT [Flag.M_PV04] | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 공압·현장 요청: 공기 공급과 저압 스위치, 현장 선택 스위치, 솔레노이드 전원 및 구동 릴레이를 확인한다.
2. 위치 상태: 열림만 1, 닫힘만 1, 둘 다 0, 둘 다 1을 구분하고 원시 I, 내부 기억 비트, HMI 가공 상태를 동시에 기록한다.
3. 출력 경로: HMI 요청 → 상태/기억 비트 → 물리 Q → 중간 릴레이 → 솔레노이드 → 실린더 → 위치 센서 순서로 확인한다.
4. 게이트 순서: A/B 두 게이트 장치는 상태 값, 각 단계 진입 조건, Set/Reset 출력, 시간 조건과 다음 상태 Move를 원본 XML로 대조한다.
5. 복귀·전원 재시작: 닫힘 상태, 잔존 요청과 기억 비트, 공기 복귀 상태, 초기화 네트워크의 조건을 기록한 후 정상 순서 시험을 설계한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| PV04-SIM-01 | 정상 위치 전환 | 닫힘→중간→열림 | I/기억 비트/HMI 상태/Q 경로 확인 | 설계·미실행 |
| PV04-SIM-02 | 위치 모순 | 열림·닫힘 모두 1 | 원본 경보·진행 조건 확인 | 설계·미실행 |
| PV04-SIM-03 | 도달 실패 | 출력 요청 후 위치 입력 미도달 | 타이머·알람·다음 단계 차단 확인 | 설계·미실행 |
| PV04-SIM-04 | 공기/현장 요청 | 저압·현장 셀렉터 상태 변경 | 공통 허가·현장 우선순위 대조 | 설계·미실행 |
| PV04-SIM-05 | 전원 복귀 | 초기/중간 위치로 재시작 | 기억과 요청의 초기화 및 재순서 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| PV04-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| PV04-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| PV04-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| PV04-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| PV04-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |
| PV04-V-06 | 불일치/특이점 | 회로 및 출력 SPARE와 pv04 deleted 제목을 확인해야 한다. | 확인 대기 |

## PV05 · 질소 주입 밸브

질소 비상 주입 계통. 탱크 준비 입력과 공통 주입 요청 출력을 함께 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 96 / PDF 97.

확인할 특이점:  두 밸브의 개별 PLC 출력으로 단정하지 않는다. 외부 릴레이·타이머 박스 회로가 포함된다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q6.4 | start nitrogen | bool | a 60.5 automatic immissionmotor command | 1059 |
| %I16.7 | nitrogen tank ready | bool | e 45.7 nitrogen tankready | 1074 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| simulation | 2 |  | [네트워크 1080](networks/network-1080.html) | 7/9 |
| allarms 3 | 12 | hydrogen box not ready | [네트워크 1990](networks/network-1990.html) | 10/18 |

### 점검·진단 절차안

1. 외부 박스 회로: 탱크 준비 입력, 현장 비상 요청, PLC 공통 주입 출력, 중간 릴레이·타이머, PV05/PV06 배선을 추적한다.
2. 개별 밸브 확인: 두 밸브의 현장 코일과 실제 개방 경로를 따로 기록한다. 공통 요청을 개별 위치 피드백으로 사용하지 않는다.
3. 복귀·가스 공급: 압력·공급 준비·타이머·요청 해제와 잔존 상태를 도면과 현장에서 대조한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| PV05-SIM-01 | 요청·준비 | 탱크 준비/주입 요청 변경 | 공통 Q와 외부 릴레이/타이머 동작 대조 | 설계·미실행 |
| PV05-SIM-02 | 복귀 | 요청 해제·준비 해제 | 개별 밸브 결과는 외부 회로 모델과 대조 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| PV05-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| PV05-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| PV05-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| PV05-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| PV05-V-05 | 불일치/특이점 | 두 밸브의 개별 PLC 출력으로 단정하지 않는다. 외부 릴레이·타이머 박스 회로가 포함된다. | 확인 대기 |

## PV06 · 질소 주입 밸브

질소 비상 주입 계통. 탱크 준비 입력과 공통 주입 요청 출력을 함께 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 96 / PDF 97.

확인할 특이점:  두 밸브의 개별 PLC 출력으로 단정하지 않는다. 외부 릴레이·타이머 박스 회로가 포함된다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q6.4 | start nitrogen | bool | a 60.5 automatic immissionmotor command | 1059 |
| %I16.7 | nitrogen tank ready | bool | e 45.7 nitrogen tankready | 1074 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| simulation | 2 |  | [네트워크 1080](networks/network-1080.html) | 7/9 |
| allarms 3 | 12 | hydrogen box not ready | [네트워크 1990](networks/network-1990.html) | 10/18 |

### 점검·진단 절차안

1. 외부 박스 회로: 탱크 준비 입력, 현장 비상 요청, PLC 공통 주입 출력, 중간 릴레이·타이머, PV05/PV06 배선을 추적한다.
2. 개별 밸브 확인: 두 밸브의 현장 코일과 실제 개방 경로를 따로 기록한다. 공통 요청을 개별 위치 피드백으로 사용하지 않는다.
3. 복귀·가스 공급: 압력·공급 준비·타이머·요청 해제와 잔존 상태를 도면과 현장에서 대조한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| PV06-SIM-01 | 요청·준비 | 탱크 준비/주입 요청 변경 | 공통 Q와 외부 릴레이/타이머 동작 대조 | 설계·미실행 |
| PV06-SIM-02 | 복귀 | 요청 해제·준비 해제 | 개별 밸브 결과는 외부 회로 모델과 대조 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| PV06-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| PV06-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| PV06-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| PV06-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| PV06-V-05 | 불일치/특이점 | 두 밸브의 개별 PLC 출력으로 단정하지 않는다. 외부 릴레이·타이머 박스 회로가 포함된다. | 확인 대기 |

## PV14 · 필터 냉풍 유입 밸브

집진 필터 냉풍 유입. 열림/닫힘 입력과 필터 과온 대응을 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 168 / PDF 169.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q17.0 | pv-14 | bool | a 5.0 inlet fresh airfilters valve | 830 |
| %I28.0 | pv-14 open | bool | %i6.0 | 873 |
| %I28.1 | pv-14 close | bool | %i6.1 | 874 |
| %M2.1 | open false air | bool |  | 1565 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| PV_14\Flag | DB2,X13.1 | PLC | 000B5 |
| PV_14\LS_Open | DB11,X74.0 | PLC | 000B3 |
| PV_14\LS_Close | DB11,X74.1 | PLC | 000B2 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 1 |  | [네트워크 1070](networks/network-1070.html) | 33/62 |
| simulation | 11 | pv14 | [네트워크 1089](networks/network-1089.html) | 4/7 |
| hmi | 35 | pv14 | [네트워크 1212](networks/network-1212.html) | 4/7 |
| filter | 21 | pv-14 cold air filter fault | [네트워크 1902](networks/network-1902.html) | 12/22 |
| filter | 22 | valve air false pv-14 | [네트워크 1903](networks/network-1903.html) | 10/18 |
| allarms 3 | 13 | tc-09 filter inlet temperature | [네트워크 1991](networks/network-1991.html) | 20/43 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1089 | Coil | Inputs.PV-14 OPEN | PV-14 | 조건에 따른 Coil 기록 |
| 1089 | Coil | Inputs.PV-14 CLOSE | NOT [PV-14] | 조건에 따른 Coil 기록 |
| 1212 | Coil | ORef UID 38 | ORef UID 27 | 조건에 따른 Coil 기록 |
| 1212 | Coil | ORef UID 42 | ORef UID 30 | 조건에 따른 Coil 기록 |
| 1902 | SdCoil | Tag_134 | (((ON AND PV-14) AND NOT [Inputs.PV-14 OPEN]) OR ((ON AND NOT [PV-14]) AND NOT [Inputs.PV-14 CLOSE])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#20S |
| 1902 | SCoil | Allarm.Fault_PV14 | ((((ON AND PV-14) AND NOT [Inputs.PV-14 OPEN]) OR ((ON AND NOT [PV-14]) AND NOT [Inputs.PV-14 CLOSE])) AND Tag_134) | 조건 성립 시 Set |
| 1902 | RCoil | Allarm.Fault_PV14 | ((ON AND Flag.RESET_ALLARM) AND Allarm.Fault_PV14) | 조건 성립 시 Reset |
| 1903 | RCoil | Flag.M_PV14 | (ON AND Allarm.Fault_PV14) | 조건 성립 시 Reset |
| 1903 | Coil | PV-14 | ((ON AND Flag.M_PV14) OR (ON AND Open false air) OR (ON AND Allarm.MAX_TC09) OR (ON AND Allarm.MAX_MAX_TC09) OR (ON AND Allarm.Emergency_module_fault)) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 공압·현장 요청: 공기 공급과 저압 스위치, 현장 선택 스위치, 솔레노이드 전원 및 구동 릴레이를 확인한다.
2. 위치 상태: 열림만 1, 닫힘만 1, 둘 다 0, 둘 다 1을 구분하고 원시 I, 내부 기억 비트, HMI 가공 상태를 동시에 기록한다.
3. 출력 경로: HMI 요청 → 상태/기억 비트 → 물리 Q → 중간 릴레이 → 솔레노이드 → 실린더 → 위치 센서 순서로 확인한다.
4. 게이트 순서: A/B 두 게이트 장치는 상태 값, 각 단계 진입 조건, Set/Reset 출력, 시간 조건과 다음 상태 Move를 원본 XML로 대조한다.
5. 복귀·전원 재시작: 닫힘 상태, 잔존 요청과 기억 비트, 공기 복귀 상태, 초기화 네트워크의 조건을 기록한 후 정상 순서 시험을 설계한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| PV14-SIM-01 | 정상 위치 전환 | 닫힘→중간→열림 | I/기억 비트/HMI 상태/Q 경로 확인 | 설계·미실행 |
| PV14-SIM-02 | 위치 모순 | 열림·닫힘 모두 1 | 원본 경보·진행 조건 확인 | 설계·미실행 |
| PV14-SIM-03 | 도달 실패 | 출력 요청 후 위치 입력 미도달 | 타이머·알람·다음 단계 차단 확인 | 설계·미실행 |
| PV14-SIM-04 | 공기/현장 요청 | 저압·현장 셀렉터 상태 변경 | 공통 허가·현장 우선순위 대조 | 설계·미실행 |
| PV14-SIM-05 | 전원 복귀 | 초기/중간 위치로 재시작 | 기억과 요청의 초기화 및 재순서 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| PV14-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| PV14-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| PV14-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| PV14-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| PV14-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## CY01 · 사이클론

P&ID의 분진 분리 본체. 배출 로터리 밸브 또는 SC01 경로와 연결해 점검한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 기계·공정 상태: 본체의 누설·기밀·퇴적·마모·부식, 입출구 막힘, 점검구와 연결 배관 상태를 기록한다.
2. 연관 장치: 주변 모터·밸브·온도/압력/레벨 계측의 운전 상태와 본체 공정 상태를 연결해 검토한다.
3. 도면 동일성: P&ID의 위치와 실제 본체·배관·전기도면 장치의 태그를 대조하고 변경 사항을 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CY01-SIM-01 | 공정 이상 모델 | 막힘·누설·퇴적을 연관 신호로 모델링 | 본체 직접 I/O가 없으면 연관 장치 영향으로 판정 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CY01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CY01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CY01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## CY02 · 사이클론

P&ID의 분진 분리 본체. 배출 로터리 밸브 또는 SC01 경로와 연결해 점검한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 기계·공정 상태: 본체의 누설·기밀·퇴적·마모·부식, 입출구 막힘, 점검구와 연결 배관 상태를 기록한다.
2. 연관 장치: 주변 모터·밸브·온도/압력/레벨 계측의 운전 상태와 본체 공정 상태를 연결해 검토한다.
3. 도면 동일성: P&ID의 위치와 실제 본체·배관·전기도면 장치의 태그를 대조하고 변경 사항을 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CY02-SIM-01 | 공정 이상 모델 | 막힘·누설·퇴적을 연관 신호로 모델링 | 본체 직접 I/O가 없으면 연관 장치 영향으로 판정 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CY02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CY02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CY02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## CY03 · 사이클론

P&ID의 분진 분리 본체. 배출 로터리 밸브 또는 SC01 경로와 연결해 점검한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 기계·공정 상태: 본체의 누설·기밀·퇴적·마모·부식, 입출구 막힘, 점검구와 연결 배관 상태를 기록한다.
2. 연관 장치: 주변 모터·밸브·온도/압력/레벨 계측의 운전 상태와 본체 공정 상태를 연결해 검토한다.
3. 도면 동일성: P&ID의 위치와 실제 본체·배관·전기도면 장치의 태그를 대조하고 변경 사항을 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CY03-SIM-01 | 공정 이상 모델 | 막힘·누설·퇴적을 연관 신호로 모델링 | 본체 직접 I/O가 없으면 연관 장치 영향으로 판정 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CY03-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CY03-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CY03-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## CY04 · 사이클론

P&ID의 분진 분리 본체. 배출 로터리 밸브 또는 SC01 경로와 연결해 점검한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 기계·공정 상태: 본체의 누설·기밀·퇴적·마모·부식, 입출구 막힘, 점검구와 연결 배관 상태를 기록한다.
2. 연관 장치: 주변 모터·밸브·온도/압력/레벨 계측의 운전 상태와 본체 공정 상태를 연결해 검토한다.
3. 도면 동일성: P&ID의 위치와 실제 본체·배관·전기도면 장치의 태그를 대조하고 변경 사항을 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CY04-SIM-01 | 공정 이상 모델 | 막힘·누설·퇴적을 연관 신호로 모델링 | 본체 직접 I/O가 없으면 연관 장치 영향으로 판정 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CY04-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CY04-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CY04-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## CY05 · 사이클론

P&ID의 분진 분리 본체. 배출 로터리 밸브 또는 SC01 경로와 연결해 점검한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 기계·공정 상태: 본체의 누설·기밀·퇴적·마모·부식, 입출구 막힘, 점검구와 연결 배관 상태를 기록한다.
2. 연관 장치: 주변 모터·밸브·온도/압력/레벨 계측의 운전 상태와 본체 공정 상태를 연결해 검토한다.
3. 도면 동일성: P&ID의 위치와 실제 본체·배관·전기도면 장치의 태그를 대조하고 변경 사항을 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CY05-SIM-01 | 공정 이상 모델 | 막힘·누설·퇴적을 연관 신호로 모델링 | 본체 직접 I/O가 없으면 연관 장치 영향으로 판정 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CY05-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CY05-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CY05-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## VR01 · 로터리 밸브

사이클론·필터·석회 경로에서 배출 및 공기 차단을 담당한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 46 / PDF 47.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I3.4 | vr01_fbk | bool | feedbackmotor vr-01 | 501 |
| %Q2.6 | start vr01 | bool | a 53.2 vr-01 motorcommand | 1330 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| VR_01\Allarme1 | DB11,X32.1 | PLC | 0034C |
| VR_01\RispostaA | DB11,X32.0 | PLC | 00306 |
| VR_01\Flag | DB2,X1.1 | PLC | 0019E |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 26 | vr-01 | [네트워크 1027](networks/network-1027.html) | 7/18 |
| time work motor | 49 |  | [네트워크 1050](networks/network-1050.html) | 6/17 |
| simulation | 6 | motors simulated | [네트워크 1084](networks/network-1084.html) | 16/25 |
| hmi | 16 | vr01 | [네트워크 1193](networks/network-1193.html) | 1/9 |
| allarms 1 | 17 | vr01 | [네트워크 1797](networks/network-1797.html) | 9/17 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| motors 1 | 20 | vr01 | [네트워크 1949](networks/network-1949.html) | 5/9 |
| motors 1 | 21 | preallarm fn01 | [네트워크 1950](networks/network-1950.html) | 12/22 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1027 | Move | hours motors.VR_01_HOUR | ((Tag_47 AND VR01_Fbk) AND [hours motors.VR_01_MIN >= 60]) | Move 입력 1 |
| 1027 | Move | hours motors.VR_01_MIN | Move UID 1604.eno (블록 동작 확인) | Move 입력 0 |
| 1027 | SCoil | Flag_Aggiorna_DB | Move UID 1607.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1797 | SdCoil | Tag_62 | ((ON AND Start VR01) AND NOT [Inputs.VR-01 RUN]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1797 | SCoil | Allarm.VR_01_FAULT | ((ON AND Start VR01) AND Tag_62) | 조건 성립 시 Set |
| 1797 | RCoil | Allarm.VR_01_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.VR_01_FAULT) | 조건 성립 시 Reset |
| 1949 | RCoil | Flag.M_VR_01 | (ON AND Allarm.VR_01_FAULT) | 조건 성립 시 Reset |
| 1949 | Coil | Start VR01 | (ON AND Flag.M_VR_01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| VR01-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| VR01-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| VR01-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| VR01-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| VR01-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| VR01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| VR01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| VR01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| VR01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| VR01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## VR02 · 로터리 밸브

사이클론·필터·석회 경로에서 배출 및 공기 차단을 담당한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 49 / PDF 50.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I3.7 | vr02_fbk | bool | feedbackmotor vr-02 | 503 |
| %Q3.0 | start vr02 | bool | a 49.7 vr-02 motorcommand | 1326 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| VR_02\RispostaA | DB11,X36.0 | PLC | 00440 |
| VR_02\Flag | DB2,X1.3 | PLC | 0043F |
| VR_02\Allarme1 | DB11,X36.1 | PLC | 0043E |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 28 | vr-02 | [네트워크 1029](networks/network-1029.html) | 7/18 |
| time work motor | 50 |  | [네트워크 1051](networks/network-1051.html) | 6/17 |
| simulation | 6 | motors simulated | [네트워크 1084](networks/network-1084.html) | 16/25 |
| hmi | 18 | vr02 | [네트워크 1195](networks/network-1195.html) | 1/9 |
| allarms 1 | 19 | vr02 | [네트워크 1799](networks/network-1799.html) | 9/17 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| motors 1 | 21 | preallarm fn01 | [네트워크 1950](networks/network-1950.html) | 12/22 |
| motors 1 | 23 | vr02 | [네트워크 1952](networks/network-1952.html) | 5/9 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1029 | Move | hours motors.VR_02_HOUR | ((Tag_47 AND VR02_Fbk) AND [hours motors.VR_02_MIN >= 60]) | Move 입력 1 |
| 1029 | Move | hours motors.VR_02_MIN | Move UID 1712.eno (블록 동작 확인) | Move 입력 0 |
| 1029 | SCoil | Flag_Aggiorna_DB | Move UID 1715.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1799 | SdCoil | Tag_64 | ((ON AND Start VR02) AND NOT [Inputs.VR02 Run]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1799 | SCoil | Allarm.VR_02_FAULT | ((ON AND Start VR02) AND Tag_64) | 조건 성립 시 Set |
| 1799 | RCoil | Allarm.VR_02_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.VR_02_FAULT) | 조건 성립 시 Reset |
| 1952 | RCoil | Flag.M_VR_02 | (ON AND Allarm.VR_02_FAULT) | 조건 성립 시 Reset |
| 1952 | Coil | Start VR02 | (ON AND Flag.M_VR_02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| VR02-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| VR02-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| VR02-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| VR02-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| VR02-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| VR02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| VR02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| VR02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| VR02-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| VR02-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## VR03 · 로터리 밸브

사이클론·필터·석회 경로에서 배출 및 공기 차단을 담당한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 61 / PDF 62.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I5.4 | vr03_fbk | bool | feedback motor vr-03 | 517 |
| %Q4.3 | start vr03 | bool | a 52.7 vr-03 motorcommand | 1307 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| VR_03\Allarme1 | DB11,X58.1 | PLC | 00334 |
| VR_03\RispostaA | DB11,X58.0 | PLC | 001BA |
| VR_03\Flag | DB2,X2.5 | PLC | 00192 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 39 | vr-03 | [네트워크 1040](networks/network-1040.html) | 7/18 |
| time work motor | 52 |  | [네트워크 1053](networks/network-1053.html) | 6/17 |
| simulation | 7 | motors simulated | [네트워크 1085](networks/network-1085.html) | 19/29 |
| hmi | 29 | vr03 | [네트워크 1206](networks/network-1206.html) | 1/9 |
| allarms 1 | 30 | vr03 | [네트워크 1810](networks/network-1810.html) | 9/17 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| motors 1 | 27 | sc01 | [네트워크 1956](networks/network-1956.html) | 8/14 |
| motors 1 | 35 | preallarm fn04 | [네트워크 1964](networks/network-1964.html) | 13/24 |
| motors 1 | 37 | vr03 | [네트워크 1966](networks/network-1966.html) | 5/9 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1040 | Move | hours motors.VR_03_HOUR | ((Tag_47 AND VR03_Fbk) AND [hours motors.VR_03_MIN >= 60]) | Move 입력 1 |
| 1040 | Move | hours motors.VR_03_MIN | Move UID 2306.eno (블록 동작 확인) | Move 입력 0 |
| 1040 | SCoil | Flag_Aggiorna_DB | Move UID 2309.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1810 | SdCoil | Tag_75 | ((ON AND Start VR03) AND NOT [Inputs.VR03 Run]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1810 | SCoil | Allarm.VR_03_FAULT | ((ON AND Start VR03) AND Tag_75) | 조건 성립 시 Set |
| 1810 | RCoil | Allarm.VR_03_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.VR_03_FAULT) | 조건 성립 시 Reset |
| 1966 | RCoil | Flag.M_VR_03 | (ON AND Allarm.VR_03_FAULT) | 조건 성립 시 Reset |
| 1966 | Coil | Start VR03 | (ON AND Flag.M_VR_03) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| VR03-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| VR03-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| VR03-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| VR03-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| VR03-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| VR03-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| VR03-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| VR03-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| VR03-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| VR03-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## VR04 · 로터리 밸브

사이클론·필터·석회 경로에서 배출 및 공기 차단을 담당한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 62 / PDF 63.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I5.5 | vr04_fbk | bool | feedback motor vr-04 | 516 |
| %Q4.4 | start vr04 | bool | a 53.0 vr-04 motorcommand | 1305 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| VR_04\Allarme1 | DB11,X60.1 | PLC | 00332 |
| VR_04\RispostaA | DB11,X60.0 | PLC | 001B9 |
| VR_04\Flag | DB2,X2.6 | PLC | 00191 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 40 | vr-04 | [네트워크 1041](networks/network-1041.html) | 7/18 |
| time work motor | 52 |  | [네트워크 1053](networks/network-1053.html) | 6/17 |
| simulation | 7 | motors simulated | [네트워크 1085](networks/network-1085.html) | 19/29 |
| hmi | 30 | vr04 | [네트워크 1207](networks/network-1207.html) | 1/9 |
| allarms 1 | 31 | vr04 | [네트워크 1811](networks/network-1811.html) | 9/17 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| filter | 5 | enabling sleeve washing | [네트워크 1886](networks/network-1886.html) | 15/29 |
| motors 1 | 33 | sc10 | [네트워크 1962](networks/network-1962.html) | 8/14 |
| motors 1 | 35 | preallarm fn04 | [네트워크 1964](networks/network-1964.html) | 13/24 |
| motors 1 | 38 | vr04 | [네트워크 1967](networks/network-1967.html) | 5/9 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1041 | Move | hours motors.VR_04_HOUR | ((Tag_47 AND VR04_Fbk) AND [hours motors.VR_04_MIN >= 60]) | Move 입력 1 |
| 1041 | Move | hours motors.VR_04_MIN | Move UID 2360.eno (블록 동작 확인) | Move 입력 0 |
| 1041 | SCoil | Flag_Aggiorna_DB | Move UID 2363.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1811 | SdCoil | Tag_76 | ((ON AND Start VR04) AND NOT [Inputs.VR04 Run]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1811 | SCoil | Allarm.VR_04_FAULT | ((ON AND Start VR04) AND Tag_76) | 조건 성립 시 Set |
| 1811 | RCoil | Allarm.VR_04_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.VR_04_FAULT) | 조건 성립 시 Reset |
| 1967 | RCoil | Flag.M_VR_04 | (ON AND Allarm.VR_04_FAULT) | 조건 성립 시 Reset |
| 1967 | Coil | Start VR04 | (ON AND Flag.M_VR_04) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| VR04-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| VR04-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| VR04-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| VR04-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| VR04-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| VR04-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| VR04-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| VR04-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| VR04-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| VR04-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## VR05 · 로터리 밸브

사이클론·필터·석회 경로에서 배출 및 공기 차단을 담당한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 63 / PDF 64.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I5.6 | vr05_fbk | bool | feedback motor vr-05 | 515 |
| %Q4.5 | start vr05 | bool | a 53.3 vr-05 motorcommand | 1303 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| VR_05\Allarme1 | DB11,X62.1 | PLC | 00330 |
| VR_05\RispostaA | DB11,X62.0 | PLC | 001B8 |
| VR_05\Flag | DB2,X2.7 | PLC | 00190 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 41 | vr-05 | [네트워크 1042](networks/network-1042.html) | 7/18 |
| time work motor | 52 |  | [네트워크 1053](networks/network-1053.html) | 6/17 |
| simulation | 7 | motors simulated | [네트워크 1085](networks/network-1085.html) | 19/29 |
| hmi | 31 | vr05 | [네트워크 1208](networks/network-1208.html) | 1/9 |
| allarms 1 | 32 | vr05 | [네트워크 1812](networks/network-1812.html) | 9/17 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| filter | 5 | enabling sleeve washing | [네트워크 1886](networks/network-1886.html) | 15/29 |
| motors 1 | 34 | sc11 | [네트워크 1963](networks/network-1963.html) | 8/14 |
| motors 1 | 35 | preallarm fn04 | [네트워크 1964](networks/network-1964.html) | 13/24 |
| motors 1 | 39 | vr05 | [네트워크 1968](networks/network-1968.html) | 5/9 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1042 | Move | hours motors.VR_05_HOUR | ((Tag_47 AND VR05_Fbk) AND [hours motors.VR_05_MIN >= 60]) | Move 입력 1 |
| 1042 | Move | hours motors.VR_05_MIN | Move UID 2414.eno (블록 동작 확인) | Move 입력 0 |
| 1042 | SCoil | Flag_Aggiorna_DB | Move UID 2417.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1812 | SdCoil | Tag_77 | ((ON AND Start VR05) AND NOT [Inputs.VR05 Run]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1812 | SCoil | Allarm.VR_05_FAULT | ((ON AND Start VR05) AND Tag_77) | 조건 성립 시 Set |
| 1812 | RCoil | Allarm.VR_05_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.VR_05_FAULT) | 조건 성립 시 Reset |
| 1968 | RCoil | Flag.M_VR_05 | (ON AND Allarm.VR_05_FAULT) | 조건 성립 시 Reset |
| 1968 | Coil | Start VR05 | (ON AND Flag.M_VR_05) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| VR05-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| VR05-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| VR05-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| VR05-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| VR05-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| VR05-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| VR05-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| VR05-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| VR05-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| VR05-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## VR06 · 로터리 밸브

사이클론·필터·석회 경로에서 배출 및 공기 차단을 담당한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 64 / PDF 65.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I5.7 | vr06_fbk | bool | feedback motor vr-06 | 514 |
| %Q4.6 | start vr06 | bool | a 53.6 vr-06 motorcommand | 1301 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| VR_06\Allarme1 | DB11,X64.1 | PLC | 0032E |
| VR_06\RispostaA | DB11,X64.0 | PLC | 001B7 |
| VR_06\Flag | DB2,X3.0 | PLC | 0018F |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 42 | vr-06 | [네트워크 1043](networks/network-1043.html) | 7/18 |
| time work motor | 52 |  | [네트워크 1053](networks/network-1053.html) | 6/17 |
| simulation | 7 | motors simulated | [네트워크 1085](networks/network-1085.html) | 19/29 |
| hmi | 32 | vr06 | [네트워크 1209](networks/network-1209.html) | 1/9 |
| allarms 1 | 33 | vr06 | [네트워크 1813](networks/network-1813.html) | 9/17 |
| motors 1 | 29 | ld01 | [네트워크 1958](networks/network-1958.html) | 9/16 |
| motors 1 | 32 | ld01 | [네트워크 1961](networks/network-1961.html) | 12/21 |
| motors 1 | 40 | vr06 | [네트워크 1969](networks/network-1969.html) | 8/14 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1043 | Move | hours motors.VR_06_HOUR | ((Tag_47 AND VR06_Fbk) AND [hours motors.VR_06_MIN >= 60]) | Move 입력 1 |
| 1043 | Move | hours motors.VR_06_MIN | Move UID 2468.eno (블록 동작 확인) | Move 입력 0 |
| 1043 | SCoil | Flag_Aggiorna_DB | Move UID 2471.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1813 | SdCoil | Tag_78 | ((ON AND Start VR06) AND NOT [Inputs.VR-06 RUN]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1813 | SCoil | Allarm.VR_06_FAULT | ((ON AND Start VR06) AND Tag_78) | 조건 성립 시 Set |
| 1813 | RCoil | Allarm.VR_06_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.VR_06_FAULT) | 조건 성립 시 Reset |
| 1969 | RCoil | Flag.M_VR_06 | ((ON AND Allarm.VR_06_FAULT) OR ((ON AND NOT [Start ER-01]) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1969 | Coil | Start VR06 | (ON AND Flag.M_VR_06) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| VR06-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| VR06-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| VR06-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| VR06-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| VR06-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| VR06-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| VR06-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| VR06-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| VR06-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| VR06-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## SC01 · 사이클론 분진 스크루

분진을 해당 로터리 밸브로 이송한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 53 / PDF 54.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I4.4 | sc01_fbk | bool | feedback motor sc-01 | 508 |
| %Q3.4 | start sc01 | bool | a 49.3 sc-01 motorcommand | 1318 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| SC_01\Allarme1 | DB11,X44.1 | PLC | 00342 |
| SC_01\RispostaA | DB11,X44.0 | PLC | 001C1 |
| SC_01\Flag | DB2,X1.6 | PLC | 00199 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 32 | sc-01 | [네트워크 1033](networks/network-1033.html) | 7/18 |
| time work motor | 50 |  | [네트워크 1051](networks/network-1051.html) | 6/17 |
| simulation | 6 | motors simulated | [네트워크 1084](networks/network-1084.html) | 16/25 |
| hmi | 22 | sc1 | [네트워크 1199](networks/network-1199.html) | 1/9 |
| allarms 1 | 23 | sc01 | [네트워크 1803](networks/network-1803.html) | 9/17 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| motors 1 | 27 | sc01 | [네트워크 1956](networks/network-1956.html) | 8/14 |
| motors 1 | 35 | preallarm fn04 | [네트워크 1964](networks/network-1964.html) | 13/24 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1033 | Move | hours motors.SC_01_HOUR | ((Tag_47 AND SC01_Fbk) AND [hours motors.SC_01_MIN >= 60]) | Move 입력 1 |
| 1033 | Move | hours motors.SC_01_MIN | Move UID 1928.eno (블록 동작 확인) | Move 입력 0 |
| 1033 | SCoil | Flag_Aggiorna_DB | Move UID 1931.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1803 | SdCoil | Tag_68 | ((ON AND Start SC01) AND NOT [Inputs.FEEDBACKMOTOR SC-01]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1803 | SCoil | Allarm.SC_01_FAULT | ((ON AND Start SC01) AND Tag_68) | 조건 성립 시 Set |
| 1803 | RCoil | Allarm.SC_01_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.SC_01_FAULT) | 조건 성립 시 Reset |
| 1956 | RCoil | Flag.M_SC_01 | ((ON AND Allarm.SC_01_FAULT) OR ((ON AND NOT [Inputs.VR03 Run]) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1956 | Coil | Start SC01 | (ON AND Flag.M_SC_01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SC01-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| SC01-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| SC01-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| SC01-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| SC01-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SC01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SC01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SC01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SC01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| SC01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## SC10 · BF01 분진 스크루

분진을 해당 로터리 밸브로 이송한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 57 / PDF 58.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I5.0 | sc-10_fbk | bool | feedback motor sc-10 | 511 |
| %Q4.0 | start sc10 | bool | a 52.2 sc-10 motorcommand | 1312 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| SC_10\Allarme1 | DB11,X52.1 | PLC | 0033A |
| SC_10\RispostaA | DB11,X52.0 | PLC | 001BD |
| SC_10\Flag | DB2,X2.2 | PLC | 00195 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 36 | sc-10 | [네트워크 1037](networks/network-1037.html) | 7/18 |
| time work motor | 51 |  | [네트워크 1052](networks/network-1052.html) | 6/17 |
| simulation | 7 | motors simulated | [네트워크 1085](networks/network-1085.html) | 19/29 |
| hmi | 26 | sc10 | [네트워크 1203](networks/network-1203.html) | 1/9 |
| allarms 1 | 27 | sc10 | [네트워크 1807](networks/network-1807.html) | 9/17 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| filter | 5 | enabling sleeve washing | [네트워크 1886](networks/network-1886.html) | 15/29 |
| filter | 7 | filter work | [네트워크 1888](networks/network-1888.html) | 9/19 |
| motors 1 | 33 | sc10 | [네트워크 1962](networks/network-1962.html) | 8/14 |
| motors 1 | 35 | preallarm fn04 | [네트워크 1964](networks/network-1964.html) | 13/24 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1037 | Move | hours motors.SC_10_HOUR | ((Tag_47 AND SC-10_Fbk) AND [hours motors.SC_10_MIN >= 60]) | Move 입력 1 |
| 1037 | Move | hours motors.SC_10_MIN | Move UID 2144.eno (블록 동작 확인) | Move 입력 0 |
| 1037 | SCoil | Flag_Aggiorna_DB | Move UID 2147.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1807 | SdCoil | Tag_72 | ((ON AND Start SC10) AND NOT [Inputs.FEEDBACKMOTOR SC-10]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1807 | SCoil | Allarm.SC_10_FAULT | ((ON AND Start SC10) AND Tag_72) | 조건 성립 시 Set |
| 1807 | RCoil | Allarm.SC_10_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.SC_10_FAULT) | 조건 성립 시 Reset |
| 1962 | RCoil | Flag.M_SC_10 | ((ON AND Allarm.SC_10_FAULT) OR ((ON AND NOT [Inputs.VR04 Run]) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1962 | Coil | Start SC10 | (ON AND Flag.M_SC_10) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SC10-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| SC10-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| SC10-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| SC10-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| SC10-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SC10-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SC10-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SC10-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SC10-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| SC10-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## SC11 · BF02 분진 스크루

분진을 해당 로터리 밸브로 이송한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 58 / PDF 59.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I5.1 | sc-11_fbk | bool | feedback motor sc-11 | 512 |
| %Q4.1 | start sc11 | bool | a 52.3 sc-11 motorcommand | 1310 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| SC_11\Allarme1 | DB11,X54.1 | PLC | 00338 |
| SC_11\RispostaA | DB11,X54.0 | PLC | 001BC |
| SC_11\Flag | DB2,X2.3 | PLC | 00194 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 37 | sc-11 | [네트워크 1038](networks/network-1038.html) | 7/18 |
| time work motor | 51 |  | [네트워크 1052](networks/network-1052.html) | 6/17 |
| simulation | 7 | motors simulated | [네트워크 1085](networks/network-1085.html) | 19/29 |
| hmi | 27 | sc11 | [네트워크 1204](networks/network-1204.html) | 1/9 |
| allarms 1 | 28 | sc11 | [네트워크 1808](networks/network-1808.html) | 9/17 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| filter | 5 | enabling sleeve washing | [네트워크 1886](networks/network-1886.html) | 15/29 |
| filter | 7 | filter work | [네트워크 1888](networks/network-1888.html) | 9/19 |
| motors 1 | 34 | sc11 | [네트워크 1963](networks/network-1963.html) | 8/14 |
| motors 1 | 35 | preallarm fn04 | [네트워크 1964](networks/network-1964.html) | 13/24 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1038 | Move | hours motors.SC_11_HOUR | ((Tag_47 AND SC-11_Fbk) AND [hours motors.SC_11_MIN >= 60]) | Move 입력 1 |
| 1038 | Move | hours motors.SC_11_MIN | Move UID 2198.eno (블록 동작 확인) | Move 입력 0 |
| 1038 | SCoil | Flag_Aggiorna_DB | Move UID 2201.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1808 | SdCoil | Tag_73 | ((ON AND Start SC11) AND NOT [Inputs.FEEDBACKMOTOR SC-11]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1808 | SCoil | Allarm.SC_11_FAULT | ((ON AND Start SC11) AND Tag_73) | 조건 성립 시 Set |
| 1808 | RCoil | Allarm.SC_11_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.SC_11_FAULT) | 조건 성립 시 Reset |
| 1963 | RCoil | Flag.M_SC_11 | ((ON AND Allarm.SC_11_FAULT) OR ((ON AND NOT [Inputs.VR05 Run]) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1963 | Coil | Start SC11 | (ON AND Flag.M_SC_11) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SC11-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| SC11-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| SC11-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| SC11-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| SC11-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SC11-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SC11-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SC11-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SC11-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| SC11-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## BF01 · 백 필터

DP 차압 감시, 분진 스크루·로터리 밸브, 펄스 세정 밸브가 연결되는 집진 장치.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 152 / PDF 153, FG 153 / PDF 154, FG 154 / PDF 155, FG 155 / PDF 156, FG 156 / PDF 157, FG 157 / PDF 158, FG 158 / PDF 159, FG 159 / PDF 160, FG 160 / PDF 161, FG 161 / PDF 162, FG 162 / PDF 163, FG 163 / PDF 164, FG 164 / PDF 165, FG 165 / PDF 166, FG 166 / PDF 167, FG 167 / PDF 168, FG 168 / PDF 169, FG 169 / PDF 170, FG 170 / PDF 171, FG 171 / PDF 172, FG 172 / PDF 173, FG 173 / PDF 174, FG 174 / PDF 175, FG 175 / PDF 176, FG 176 / PDF 177, FG 177 / PDF 178, FG 178 / PDF 179, FG 179 / PDF 180, FG 180 / PDF 181, FG 180A / PDF 182, FG 180B / PDF 183.

확인할 특이점: 병렬 필터 세정 원본 네트워크에 11~90 범위를 설정하는 참조와 두 필터 허가에 따라 출력을 교대시키는 비교기가 있다. EV 번호가 순서 변수 값과 항상 같다고 가정하지 않는다. 

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q12.0 | ev-11 | bool | a0.0 filter 1 valve bf01first sector | 791 |
| %Q13.0 | ev-19 | bool | a1.0 filter 1 valve bf01second sector | 799 |
| %Q14.0 | ev-27 | bool | a2.0 filter 1 valve bf01third sector | 806 |
| %Q15.0 | ev-35 | bool | a3.0 filter 1 valve bf01fourth sector | 814 |
| %Q16.0 | ev-43 | bool | a4.0 filter 1 valve bf01fifth sector | 822 |
| %Q19.0 | ev-59 | bool | a9.0 filter 1 valve bf02second sector | 843 |
| %Q20.0 | ev-67 | bool | a10.0 filter 1 valve bf02third sector | 850 |
| %Q21.0 | ev-75 | bool | a11.0 filter 1 valve bf02fourth sector | 858 |
| %Q22.0 | ev-83 | bool | a12.0 filter 1 valve bf02fifth sector | 866 |
| %Q18.0 | ev-51 | bool | a8.0 filter 1 valve bf02first sector | 890 |
| %M180.3 | bf01_run | bool |  | 902 |
| %IW398 | pr_bf01 | int | differential pressure switchbags filter bf-01(4-20ma) | 1523 |
| %IW386 | tc09 | int | temperature bf-01 | 1555 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| BF01_RUN | MX180.3 | PLC | 00456 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| analog input conversion | 43 | dp-01 | [네트워크 1773](networks/network-1773.html) | 2/9 |
| filter | 5 | enabling sleeve washing | [네트워크 1886](networks/network-1886.html) | 15/29 |
| filter | 6 | work pause times for filter valves | [네트워크 1887](networks/network-1887.html) | 10/20 |
| filter | 10 | a0.0 filter 1 valve bf01first sector | [네트워크 1891](networks/network-1891.html) | 32/65 |
| filter | 11 | wash filter | [네트워크 1892](networks/network-1892.html) | 32/65 |
| filter | 12 | wash filter | [네트워크 1893](networks/network-1893.html) | 32/65 |
| filter | 13 | wash filter | [네트워크 1894](networks/network-1894.html) | 32/65 |
| filter | 14 | wash filter | [네트워크 1895](networks/network-1895.html) | 32/65 |
| filter | 15 | wash filter | [네트워크 1896](networks/network-1896.html) | 32/65 |
| filter | 16 | wash filter | [네트워크 1897](networks/network-1897.html) | 32/65 |
| filter | 17 | wash filter | [네트워크 1898](networks/network-1898.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1891 | Coil | EV-11 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 11]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |
| 1891 | Coil | EV-51 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 12]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |
| 1891 | Coil | EV-12 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 13]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |
| 1891 | Coil | EV-52 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 14]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |
| 1891 | Coil | EV-13 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 15]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |
| 1891 | Coil | EV-53 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 16]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |
| 1891 | Coil | EV-14 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 17]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |
| 1891 | Coil | EV-54 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 18]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |
| 1891 | Coil | EV-15 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 19]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |
| 1891 | Coil | EV-55 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 20]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 필터 운전 허가: 분진 스크루·로터리 밸브·BF_RUN 표시·차압 기준 및 강제 세정 조건을 원본 Filter 네트워크로 검토한다.
2. 세정 순서: EV11~50과 EV51~90을 구분하고 실제 순서 변수의 값 → 비교기 → 개별 출력 주소를 추적한다. 번호 범위만 보고 순서를 정하지 않는다.
3. 펄스/휴지 시간: 작업 시간·휴지 시간·차압 단계별 계수 및 시험 ON/OFF 조건을 기록한다.
4. 세정 불량: 출력 펄스 → 릴레이 → 전원/퓨즈 → 코일 → 압축공기 → 밸브 → 차압 변화 순으로 점검한다.
5. 온도·분진 배출: TC09/PV14, SC/VR 피드백과 필터 과온·차압 경보를 연결해 점검한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| BF01-SIM-01 | 세정 허가 | SC/VR·차압·BF_RUN 변경 | 두 필터 허가를 각각 확인 | 설계·미실행 |
| BF01-SIM-02 | 전체 펄스 순서 | 순서 변수 전 범위 | 80개 EV 출력과 비교기 상수 매핑 확인 | 설계·미실행 |
| BF01-SIM-03 | 펄스/휴지 | 작업/휴지 설정 변경 | 단계·주기·중복 출력 검증 | 설계·미실행 |
| BF01-SIM-04 | 차압 경계 | DP 임계값 전후 | 허가·시간 계수의 실제 분기 확인 | 설계·미실행 |
| BF01-SIM-05 | 온도/배출 고장 | 온도와 SC/VR 고장 입력 변경 | PV14·정지/경보 경로 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| BF01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| BF01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| BF01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| BF01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| BF01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## BF02 · 백 필터

DP 차압 감시, 분진 스크루·로터리 밸브, 펄스 세정 밸브가 연결되는 집진 장치.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 181 / PDF 184, FG 182 / PDF 185, FG 183 / PDF 186, FG 184 / PDF 187, FG 185 / PDF 188, FG 186 / PDF 189, FG 187 / PDF 190, FG 188 / PDF 191, FG 189 / PDF 192, FG 190 / PDF 193, FG 191 / PDF 194, FG 192 / PDF 195, FG 193 / PDF 196, FG 194 / PDF 197, FG 195 / PDF 198, FG 196 / PDF 199, FG 197 / PDF 200, FG 198 / PDF 201, FG 199 / PDF 202, FG 200 / PDF 203, FG 201 / PDF 204, FG 202 / PDF 205, FG 203 / PDF 206, FG 204 / PDF 207.

확인할 특이점: BF02 허가 네트워크에 DP02 값과 DP01 임계값 명칭이 함께 등장한다. 공용 계수인지 오기인지 현재 설정과 원본 연결을 확인해야 한다. 

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q12.1 | ev-12 | bool | a0.1 filter 2 valve bf01first sector | 792 |
| %Q13.1 | ev-20 | bool | a1.1 filter 2 valve bf01second sector | 800 |
| %Q14.1 | ev-28 | bool | a2.1 filter 2 valve bf01third sector | 807 |
| %Q15.1 | ev-36 | bool | a3.1 filter 2 valve bf01fourth sector | 815 |
| %Q16.1 | ev-44 | bool | a4.1 filter 2 valve bf01fifth sector | 823 |
| %Q19.1 | ev-60 | bool | a9.1 filter 2 valve bf02second sector | 844 |
| %Q20.1 | ev-68 | bool | a10.1 filter 2 valve bf02third sector | 851 |
| %Q21.1 | ev-76 | bool | a11.1 filter 2 valve bf02fourth sector | 859 |
| %Q22.1 | ev-84 | bool | a12.1 filter 2 valve bf02fifth sector | 867 |
| %Q18.1 | ev-52 | bool | a8.1 filter 2 valve bf02first sector | 891 |
| %M180.4 | bf02_run | bool |  | 903 |
| %IW400 | pr_br02 | int | differential pressure switchbags filter bf-02(4-20ma) | 1522 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| BF02_RUN | MX180.4 | PLC | 00457 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| analog input conversion | 44 | dp-02 | [네트워크 1774](networks/network-1774.html) | 2/9 |
| filter | 5 | enabling sleeve washing | [네트워크 1886](networks/network-1886.html) | 15/29 |
| filter | 6 | work pause times for filter valves | [네트워크 1887](networks/network-1887.html) | 10/20 |
| filter | 10 | a0.0 filter 1 valve bf01first sector | [네트워크 1891](networks/network-1891.html) | 32/65 |
| filter | 11 | wash filter | [네트워크 1892](networks/network-1892.html) | 32/65 |
| filter | 12 | wash filter | [네트워크 1893](networks/network-1893.html) | 32/65 |
| filter | 13 | wash filter | [네트워크 1894](networks/network-1894.html) | 32/65 |
| filter | 14 | wash filter | [네트워크 1895](networks/network-1895.html) | 32/65 |
| filter | 15 | wash filter | [네트워크 1896](networks/network-1896.html) | 32/65 |
| filter | 16 | wash filter | [네트워크 1897](networks/network-1897.html) | 32/65 |
| filter | 17 | wash filter | [네트워크 1898](networks/network-1898.html) | 32/65 |

### 점검·진단 절차안

1. 필터 운전 허가: 분진 스크루·로터리 밸브·BF_RUN 표시·차압 기준 및 강제 세정 조건을 원본 Filter 네트워크로 검토한다.
2. 세정 순서: EV11~50과 EV51~90을 구분하고 실제 순서 변수의 값 → 비교기 → 개별 출력 주소를 추적한다. 번호 범위만 보고 순서를 정하지 않는다.
3. 펄스/휴지 시간: 작업 시간·휴지 시간·차압 단계별 계수 및 시험 ON/OFF 조건을 기록한다.
4. 세정 불량: 출력 펄스 → 릴레이 → 전원/퓨즈 → 코일 → 압축공기 → 밸브 → 차압 변화 순으로 점검한다.
5. 온도·분진 배출: TC09/PV14, SC/VR 피드백과 필터 과온·차압 경보를 연결해 점검한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| BF02-SIM-01 | 세정 허가 | SC/VR·차압·BF_RUN 변경 | 두 필터 허가를 각각 확인 | 설계·미실행 |
| BF02-SIM-02 | 전체 펄스 순서 | 순서 변수 전 범위 | 80개 EV 출력과 비교기 상수 매핑 확인 | 설계·미실행 |
| BF02-SIM-03 | 펄스/휴지 | 작업/휴지 설정 변경 | 단계·주기·중복 출력 검증 | 설계·미실행 |
| BF02-SIM-04 | 차압 경계 | DP 임계값 전후 | 허가·시간 계수의 실제 분기 확인 | 설계·미실행 |
| BF02-SIM-05 | 온도/배출 고장 | 온도와 SC/VR 고장 입력 변경 | PV14·정지/경보 경로 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| BF02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| BF02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| BF02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| BF02-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| BF02-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## LD01 · 석회 마이크로피더

석회 투입 장치. VR06 운전, 점검 도어, 저레벨 및 현장 셀렉터를 함께 점검한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 55 / PDF 56, FG 170 / PDF 171.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I4.6 | ld-01_fbk | bool | feedback motor ld-01 | 509 |
| %I28.5 | ll_ld01 | bool |  | 947 |
| %Q3.7 | start vibrator ld-01 | bool | a 52.1 ld-01a motorcommand | 1314 |
| %Q3.6 | start ld01 | bool | a 49.4 ld-01 motorcommand | 1316 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| LD_01_MF\Allarme1 | DB11,X48.1 | PLC | 0033E |
| LD_01_VB\Allarme1 | DB11,X50.1 | PLC | 0033C |
| LD_01_MF\RispostaA | DB11,X48.0 | PLC | 001BF |
| LD_01_VB\RispostaA | DB11,X50.0 | PLC | 001BE |
| LD_01_MF\Flag | DB2,X2.0 | PLC | 00197 |
| LD_01_VB\Flag | DB2,X2.1 | PLC | 00196 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 34 | ld-01 | [네트워크 1035](networks/network-1035.html) | 7/18 |
| time work motor | 35 | ld-01 vib | [네트워크 1036](networks/network-1036.html) | 7/18 |
| time work motor | 51 |  | [네트워크 1052](networks/network-1052.html) | 6/17 |
| hmi inputs | 1 |  | [네트워크 1070](networks/network-1070.html) | 33/62 |
| simulation | 2 |  | [네트워크 1080](networks/network-1080.html) | 7/9 |
| simulation | 7 | motors simulated | [네트워크 1085](networks/network-1085.html) | 19/29 |
| hmi | 24 | ld01 mf | [네트워크 1201](networks/network-1201.html) | 1/9 |
| hmi | 25 | ld01 vb | [네트워크 1202](networks/network-1202.html) | 1/9 |
| allarms 2 | 3 | ld-01 low lime level | [네트워크 1228](networks/network-1228.html) | 8/16 |
| allarms 1 | 25 | ld01 | [네트워크 1805](networks/network-1805.html) | 9/17 |
| allarms 1 | 26 | ld01 vibrator | [네트워크 1806](networks/network-1806.html) | 9/17 |
| motors 1 | 29 | ld01 | [네트워크 1958](networks/network-1958.html) | 9/16 |
| motors 1 | 30 |  | [네트워크 1959](networks/network-1959.html) | 2/8 |
| motors 1 | 31 | ld01 | [네트워크 1960](networks/network-1960.html) | 8/16 |
| motors 1 | 32 | ld01 | [네트워크 1961](networks/network-1961.html) | 12/21 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1035 | Move | hours motors.LD_01_HOUR | ((Tag_47 AND LD-01_Fbk) AND [hours motors.LD_01_MIN >= 60]) | Move 입력 1 |
| 1035 | Move | hours motors.LD_01_MIN | Move UID 2036.eno (블록 동작 확인) | Move 입력 0 |
| 1035 | SCoil | Flag_Aggiorna_DB | Move UID 2039.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1036 | Move | hours motors.LD_01_VIB_HOUR | ((Tag_47 AND LD-01A_Fbk) AND [hours motors.LD_01_VIB_MIN >= 60]) | Move 입력 1 |
| 1036 | Move | hours motors.LD_01_VIB_MIN | Move UID 2090.eno (블록 동작 확인) | Move 입력 0 |
| 1036 | SCoil | Flag_Aggiorna_DB | Move UID 2093.eno (블록 동작 확인) | 조건 성립 시 Set |
| 1228 | SCoil | Allarm.LD_01_MIN | LRef UID 21.Q (블록 동작 확인) | 조건 성립 시 Set |
| 1228 | RCoil | Allarm.LD_01_MIN | (((ON AND Flag.RESET_ALLARM) AND Allarm.LD_01_MIN) AND NOT [Inputs.LD-01 Minimo]) | 조건 성립 시 Reset |
| 1805 | SdCoil | Tag_70 | ((ON AND Start LD01) AND NOT [Inputs.FEEDBACKMOTOR LD-01]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1805 | SCoil | Allarm.LD_01_FAULT | ((ON AND Start LD01) AND Tag_70) | 조건 성립 시 Set |
| 1805 | RCoil | Allarm.LD_01_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.LD_01_FAULT) | 조건 성립 시 Reset |
| 1806 | SdCoil | Tag_71 | ((ON AND Start Vibrator LD-01) AND NOT [Inputs.FEEDBACKMOTOR-LD-01A]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#2S |
| 1806 | SCoil | Allarm.LD_01_VIB_FAULT | ((ON AND Start Vibrator LD-01) AND Tag_71) | 조건 성립 시 Set |
| 1806 | RCoil | Allarm.LD_01_VIB_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.LD_01_VIB_FAULT) | 조건 성립 시 Reset |
| 1958 | RCoil | Flag.M_LD_01 | ((ON AND Allarm.LD_01_FAULT) OR ((ON AND NOT [Inputs.VR-06 RUN]) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1958 | Coil | Start LD01 | ((ON AND Flag.M_LD_01) AND Inputs.LD-01 Inspection LS) | 조건에 따른 Coil 기록 |
| 1960 | SdCoil | Tag_125 | ((ON AND Inputs.FEEDBACKMOTOR LD-01) AND NOT [Tag_124]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 Data.LD_01V_WorkTime |
| 1960 | SdCoil | Tag_124 | ((ON AND Inputs.FEEDBACKMOTOR LD-01) AND Tag_125) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 Data.LD_01V_PauseTime |
| 1960 | Coil | Start_LD01Vib | ((ON AND Inputs.FEEDBACKMOTOR LD-01) AND NOT [Tag_125]) | 조건에 따른 Coil 기록 |
| 1961 | RCoil | Flag.M_LD_01_VIB | ((ON AND Allarm.LD_01_VIB_FAULT) OR ((ON AND NOT [Inputs.VR-06 RUN]) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1961 | Coil | Start Vibrator LD-01 | (((ON AND Flag.M_LD_01_VIB) OR ((ON AND NOT [Allarm.LD_01_VIB_FAULT]) AND Start_LD01Vib)) AND Inputs.LD-01 Local Button) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LD01-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| LD01-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| LD01-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| LD01-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| LD01-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LD01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LD01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LD01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LD01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| LD01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## LD01A · 석회 사일로 진동기

LD01의 간헐 운전/정지 타이머와 현장 요청에 연결되는 진동기.

자료 상태: 자료에서 확인. 상위: LD01. 전기: FG 56 / PDF 57.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I4.7 | ld-01a_fbk | bool | feedback motor-ld-01a | 510 |
| %Q3.7 | start vibrator ld-01 | bool | a 52.1 ld-01a motorcommand | 1314 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 35 | ld-01 vib | [네트워크 1036](networks/network-1036.html) | 7/18 |
| time work motor | 51 |  | [네트워크 1052](networks/network-1052.html) | 6/17 |
| simulation | 7 | motors simulated | [네트워크 1085](networks/network-1085.html) | 19/29 |
| hmi | 25 | ld01 vb | [네트워크 1202](networks/network-1202.html) | 1/9 |
| allarms 1 | 26 | ld01 vibrator | [네트워크 1806](networks/network-1806.html) | 9/17 |
| motors 1 | 32 | ld01 | [네트워크 1961](networks/network-1961.html) | 12/21 |

### 점검·진단 절차안

1. 운전 요청이 없을 때: HMI 요청 태그 → 내부 운전 허가 → 관련 Motors 1 원본 네트워크의 접점과 분기 → 물리 Q 출력 순서로 확인한다. 연결 구조에 있는 정지·알람·상위 허가를 하나씩 기록한다.
2. 요청은 있으나 출력이 없을 때: 위치·하위 설비 운전·인버터 알람·유지보수 조건을 원본 연결표와 대조한다. AND/OR 관계를 검색 코드의 나열 순서만으로 판단하지 않는다.
3. 출력은 있으나 피드백이 없을 때: Q 채널 상태, 중간 릴레이, 접촉기/인버터, 현장 전원, 실제 회전, I 피드백 순으로 추적한다. 피드백 접점이 운전과 전원 허가 중 무엇을 의미하는지 확인한다.
4. 운전 중 고장 또는 과전류: 기계 걸림·공급전압·인버터 고장 코드·센서 원시값을 수집하고 PLC 알람 원인과 결과를 구분한다. 해당 장치와 후속 설비의 정지 순서는 연결 네트워크로 검증한다.
5. 복귀: 원인 해소 → 피드백 정상 → 알람 Reset 전달 → 운전 요청 잔존 확인 → 재기동 결과 기록 순으로 점검한다. Reset을 자동 재기동으로 가정하지 않는다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LD01A-SIM-01 | 정상 기동 | 준비·피드백 조건 정상, 운전 요청 ON | 관련 원본 접점 조건이 충족될 때 해당 Q 요청과 I 피드백 전달을 확인 | 설계·미실행 |
| LD01A-SIM-02 | 기동 피드백 없음 | 기동 요청 후 피드백 미발생 | 백업의 고장 검출 경로·시간·출력 결과와 대조 | 설계·미실행 |
| LD01A-SIM-03 | 운전 중 인버터/피드백 고장 | 운전 중 고장 입력 또는 피드백 변경 | 정지/알람/상위 영향은 해당 원본 네트워크로 판정 | 설계·미실행 |
| LD01A-SIM-04 | 유지보수·상위 허가 없음 | 허가 입력 하나씩 해제 | 허가 조건에 따른 요청과 실제 출력의 관계 확인 | 설계·미실행 |
| LD01A-SIM-05 | 복귀·전원 재시작 | 고장 해제, Reset, 재시작 | 잔존 요청·기억·초기화 처리 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LD01A-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LD01A-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LD01A-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LD01A-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## ER01 · 전기 히터

FN05와 석회 투입 공기 가열 경로. 온도 허용 및 피드백을 함께 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 66 / PDF 67.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I6.1 | er01_fbk | bool | feedback er-01 electrical resistance | 519 |
| %Q5.0 | start er-01 | bool | a 60.4 er-01 electricalresistance command | 1279 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| ER_01\Allarme1 | DB11,X68.1 | PLC | 0032A |
| ER_01\RispostaA | DB11,X68.0 | PLC | 001B5 |
| ER_01\Flag | DB2,X5.4 | PLC | 0018D |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| simulation | 8 | motors simulated | [네트워크 1086](networks/network-1086.html) | 10/15 |
| hmi | 34 | er01 | [네트워크 1211](networks/network-1211.html) | 1/9 |
| allarms 1 | 42 | er01 | [네트워크 1822](networks/network-1822.html) | 8/16 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| motors 1 | 40 | vr06 | [네트워크 1969](networks/network-1969.html) | 8/14 |
| motors 1 | 42 | er01 | [네트워크 1971](networks/network-1971.html) | 10/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1822 | SCoil | Allarm.ER01_run | LRef UID 28.Q (블록 동작 확인) | 조건 성립 시 Set |
| 1822 | RCoil | Allarm.ER01_run | ((ON AND Flag.RESET_ALLARM) AND Allarm.ER01_run) | 조건 성립 시 Reset |
| 1971 | RCoil | Flag.M_ER01 | ((ON AND OFF) OR (ON AND Allarm.ER01_run) OR ((ON AND NOT [Inputs.FN-05 RUN]) AND NOT [UNDER TESTING])) | 조건 성립 시 Reset |
| 1971 | Coil | Start ER-01 | ((ON AND Flag.M_ER01) AND Inputs.177T1_OK) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 운전 허가: FN05 피드백, 온도 허용, ER01 요청/알람, ON/OFF 접점과 실제 출력 경로를 대조한다.
2. 출력 및 온도: Q→릴레이/접촉기→히터 전원과 전류, 온도 센서, 외부 온도 제어기의 허용 신호를 기록한다.
3. 과온·복귀: 과온 발생 시 허가 해제·전원 차단·온도 하강·Reset·재가열 결과를 별도로 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| ER01-SIM-01 | 허가 정상/상실 | FN05·온도 허용·요청 변경 | Q 출력과 피드백/고장 대조 | 설계·미실행 |
| ER01-SIM-02 | 과온·복귀 | 과온·Reset 조건 변경 | 허가 해제와 재가열 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| ER01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| ER01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| ER01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| ER01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| ER01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## CM01 · 집진 배기 스택

FN04 후단의 대기 배출 경로.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 기계·공정 상태: 본체의 누설·기밀·퇴적·마모·부식, 입출구 막힘, 점검구와 연결 배관 상태를 기록한다.
2. 연관 장치: 주변 모터·밸브·온도/압력/레벨 계측의 운전 상태와 본체 공정 상태를 연결해 검토한다.
3. 도면 동일성: P&ID의 위치와 실제 본체·배관·전기도면 장치의 태그를 대조하고 변경 사항을 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CM01-SIM-01 | 공정 이상 모델 | 막힘·누설·퇴적을 연관 신호로 모델링 | 본체 직접 I/O가 없으면 연관 장치 영향으로 판정 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CM01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CM01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CM01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## CM02 · 상부 배기 스택

MV02 측 대기 배출 경로.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 기계·공정 상태: 본체의 누설·기밀·퇴적·마모·부식, 입출구 막힘, 점검구와 연결 배관 상태를 기록한다.
2. 연관 장치: 주변 모터·밸브·온도/압력/레벨 계측의 운전 상태와 본체 공정 상태를 연결해 검토한다.
3. 도면 동일성: P&ID의 위치와 실제 본체·배관·전기도면 장치의 태그를 대조하고 변경 사항을 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CM02-SIM-01 | 공정 이상 모델 | 막힘·누설·퇴적을 연관 신호로 모델링 | 본체 직접 I/O가 없으면 연관 장치 영향으로 판정 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CM02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CM02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CM02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## CR01 · 운전 제어반

P&ID의 운전 캐비닛. 전기 계통·보조전원·운전 표시와 연결된다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 기계·공정 상태: 본체의 누설·기밀·퇴적·마모·부식, 입출구 막힘, 점검구와 연결 배관 상태를 기록한다.
2. 연관 장치: 주변 모터·밸브·온도/압력/레벨 계측의 운전 상태와 본체 공정 상태를 연결해 검토한다.
3. 도면 동일성: P&ID의 위치와 실제 본체·배관·전기도면 장치의 태그를 대조하고 변경 사항을 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CR01-SIM-01 | 공정 이상 모델 | 막힘·누설·퇴적을 연관 신호로 모델링 | 본체 직접 I/O가 없으면 연관 장치 영향으로 판정 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CR01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CR01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CR01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## BWF01 · 고객 설비 계량 피더

외부 피더의 준비·운전·고장·레벨·유량과 원격 운전 허가를 교환한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 85 / PDF 86, FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I14.4 | bwf1_inverter_high_speed | bool | e 17.0 bwf1_inverter_high_speed | 531 |
| %I11.1 | bwf01 ok | bool | e 64.0 bwf 01 manu status | 959 |
| %I11.3 | bwf01 fault | bool | e 64.2 bwf 01 fault | 960 |
| %I11.4 | min lev bwf01 | bool | e 64.3 bwf 01 minimum level | 961 |
| %I11.5 | max lev bwf01 | bool | e 64.4 bwf 01maximum level | 962 |
| %QW298 | bwf01_sp_flowrate | word | flow rate speed set bwf 01(client machine)(4-20ma) | 1356 |
| %I20.1 | bwf01 pulse | bool | old address | 1520 |
| %IW268 | bwf01_level | int | level bwf 01 (client machine) | 1548 |
| %I11.2 | bwf 01 run | bool | e 64.1 bwf 01 run | 1551 |
| %IW264 | bwf01_flowrate | int | flow rate bwf 01(client machine) | 1553 |
| %Q6.2 | consent start bwf01 | bool | a 61.7 bwf 01 remotestart | 1666 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| Editor_BWF01 | DB26,INT8 | PLC | 00417 |
| BWF01\Risposta | DB11,X70.1 | PLC | 000EC |
| BWF01\StatusOK | DB11,X70.0 | PLC | 000EA |
| BWF01\Allarme1 | DB11,X70.2 | PLC | 000E9 |
| BWF01\Flag | DB2,X12.0 | PLC | 000E8 |
| I_Level_BWF01 | DB13,INT32 | PLC | 0005D |
| I_Flow_rate_BWF01 | DB13,INT28 | PLC | 0005C |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| allarm manager | 9 | clear values of report at the end of the recording | [네트워크 935](networks/network-935.html) | 5/11 |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| simulation | 8 | motors simulated | [네트워크 1086](networks/network-1086.html) | 10/15 |
| hmi | 36 | bwf01 | [네트워크 1213](networks/network-1213.html) | 10/17 |
| analog output conversion | 1 | plant limits | [네트워크 1679](networks/network-1679.html) | 21/61 |
| analog output conversion | 2 | bwf01 client feeder | [네트워크 1680](networks/network-1680.html) | 5/13 |
| analog output conversion | 3 | bwf01 speed calculation | [네트워크 1681](networks/network-1681.html) | 13/39 |
| analog input conversion | 5 | client 1 bwf01 flow rate | [네트워크 1735](networks/network-1735.html) | 9/26 |
| analog input conversion | 7 | client 3 level indicator bwf01 | [네트워크 1737](networks/network-1737.html) | 2/9 |
| analog input conversion | 46 | contactor ton passed in bwf | [네트워크 1776](networks/network-1776.html) | 7/17 |
| allarms 1 | 1 | bwf01 | [네트워크 1781](networks/network-1781.html) | 13/24 |
| allarms 1 | 2 | bwf01 | [네트워크 1782](networks/network-1782.html) | 11/19 |
| allarms 1 | 40 | bwf01/bwf02 | [네트워크 1820](networks/network-1820.html) | 16/29 |
| auto start motors | 9 | production counters | [네트워크 1849](networks/network-1849.html) | 21/65 |
| motors 1 | 3 | bwf01 | [네트워크 1932](networks/network-1932.html) | 11/21 |
| motors 1 | 5 | bwf01/02 | [네트워크 1934](networks/network-1934.html) | 17/29 |
| motors 1 | 44 | liw feeder | [네트워크 1973](networks/network-1973.html) | 13/24 |
| allarms 3 | 2 | low tc03 temperature | [네트워크 1980](networks/network-1980.html) | 35/74 |
| allarms 3 | 15 | incorrect scraps feeder formula | [네트워크 1993](networks/network-1993.html) | 11/24 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1213 | Coil | ORef UID 52 | ORef UID 24 | 조건에 따른 Coil 기록 |
| 1213 | Coil | ORef UID 56 | ORef UID 27 | 조건에 따른 Coil 기록 |
| 1213 | Coil | ORef UID 48 | (ORef UID 30 OR ORef UID 33 OR ORef UID 36 OR ORef UID 43) | 조건에 따른 Coil 기록 |
| 1680 | Move | Data.SET_PERC_BWF01 | (ON AND [Data.SET_PERC_BWF01 < 0]) | Move 입력 0 |
| 1680 | Move | Data.SET_PERC_BWF01 | (ON AND [Data.SET_PERC_BWF01 > 100]) | Move 입력 100 |
| 1681 | Move | App00 | ON | Move 입력 Data.SET_PERC_BWF01 |
| 1681 | Move | App01 | ON | Move 입력 Data2.Set_TH |
| 1681 | Move | App03 | ON | Move 입력 Data2.Set_MAX_TH1 |
| 1681 | Move | BWF01_SP_FlowRate | Div UID 236.eno (블록 동작 확인) | Move 입력 App03 |
| 1681 | Move | BWF01_SP_FlowRate | Div UID 356.eno (블록 동작 확인) | Move 입력 App03 |
| 1735 | Move | Data.CLIENT_1 | (ON AND NOT [BWF 01 RUN]) | Move 입력 0 |
| 1781 | SdCoil | Tag_49 | ((ON AND Consent Start BWF01) AND NOT [Inputs.BWF 01 RUN]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#10S |
| 1781 | SCoil | Allarm.BWF01_FAULT | ((((ON AND Consent Start BWF01) AND Tag_49) AND NOT [Inputs.BWF 01 RUN]) OR ((ON AND Consent Start BWF01) AND Inputs.BWF01 FAULT)) | 조건 성립 시 Set |
| 1781 | RCoil | Allarm.BWF01_FAULT | (((ON AND Flag.RESET_ALLARM) AND Allarm.BWF01_FAULT) AND NOT [Inputs.BWF01 FAULT]) | 조건 성립 시 Reset |
| 1782 | SCoil | Allarm.BWF01_min_LEVEL | ((ON AND Consent Start BWF01) AND Inputs.min LEV BWF01) | 조건 성립 시 Set |
| 1782 | SCoil | Allarm.BWF01_MAX_LEVEL | (ON AND Inputs.MAX LEV BWF01) | 조건 성립 시 Set |
| 1782 | RCoil | Allarm.BWF01_min_LEVEL | ((ON AND Flag.RESET_ALLARM) AND NOT [Inputs.min LEV BWF01]) | 조건 성립 시 Reset |
| 1782 | RCoil | Allarm.BWF01_MAX_LEVEL | ((ON AND Flag.RESET_ALLARM) AND NOT [Inputs.MAX LEV BWF01]) | 조건 성립 시 Reset |
| 1820 | SdCoil | Tag_90 | (OFF AND NOT [Inputs.BWF1_INVERTER_HIGH_SPEED]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#30S |
| 1820 | SCoil | Allarm.BWF01_Fault_Control | ((OFF AND NOT [Inputs.BWF1_INVERTER_HIGH_SPEED]) AND Tag_90) | 조건 성립 시 Set |
| 1820 | SdCoil | Tag_91 | (OFF AND NOT [Inputs.BWF2_INVERTER_HIGH_SPEED]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#30S |
| 1820 | SCoil | Allarm.BWF02_Fault_Control | ((OFF AND NOT [Inputs.BWF2_INVERTER_HIGH_SPEED]) AND Tag_91) | 조건 성립 시 Set |
| 1820 | RCoil | Allarm.BWF01_Fault_Control | (((OFF AND Flag.RESET_ALLARM) AND Allarm.BWF01_Fault_Control) AND Inputs.BWF1_INVERTER_HIGH_SPEED) | 조건 성립 시 Reset |
| 1820 | RCoil | Allarm.BWF02_Fault_Control | (((OFF AND Flag.RESET_ALLARM) AND Allarm.BWF02_Fault_Control) AND Inputs.BWF2_INVERTER_HIGH_SPEED) | 조건 성립 시 Reset |
| 1932 | RCoil | Flag.M_BWF01 | ((ON AND Allarm.BWF01_FAULT) OR (ON AND Allarm.BWF01_Fault_Control) OR (ON AND [Data.SET_PERC_BWF01 = 0]) OR (ON AND NOT [Inputs.BWF01 OK]) OR (ON AND NOT [Inputs.BC01 run]) OR (ON AND Disable_Load_RD01)) | 조건 성립 시 Reset |
| 1932 | Coil | Consent Start BWF01 | (ON AND Flag.M_BWF01) | 조건에 따른 Coil 기록 |
| 1934 | SdCoil | Tag_114 | ((OFF AND Flag.M_BWF01) OR (OFF AND Flag.M_BWF02)) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#6M |
| 1934 | RCoil | Flag.M_BWF01 | (((OFF AND Flag.M_BWF01) OR (OFF AND Flag.M_BWF02)) AND Tag_114) | 조건 성립 시 Reset |
| 1934 | RCoil | Flag.M_BWF02 | (((OFF AND Flag.M_BWF01) OR (OFF AND Flag.M_BWF02)) AND Tag_114) | 조건 성립 시 Reset |
| 1934 | RCoil | Flag.M_BWF02 | ((((ON AND Flag.M_BWF01) OR (ON AND Flag.M_BWF02)) AND NOT [Inputs.RD01 run]) OR (((ON AND Flag.M_BWF01) OR (ON AND Flag.M_BWF02)) AND NOT [Inputs.BC01 run])) | 조건 성립 시 Reset |
| 1934 | RCoil | Flag.M_BWF01 | RCoil UID 228.out (블록 동작 확인) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| BWF01-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| BWF01-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| BWF01-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| BWF01-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| BWF01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| BWF01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| BWF01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| BWF01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| BWF01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## BWF02 · 고객 설비 계량 피더

외부 피더의 준비·운전·고장·레벨·유량과 원격 운전 허가를 교환한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 85 / PDF 86, FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I14.5 | bwf2_inverter_high_speed | bool | e 17.1 bwf2_inverter_high_speed | 532 |
| %I11.6 | bwf02 ok | bool | e 64.5 bwf 02 manu status | 963 |
| %I12.0 | bwf02 fault | bool | e 64.7 bwf 02 fault | 964 |
| %I12.1 | min lev bwf02 | bool | e 65.0 bwf 02minimum level | 965 |
| %I12.2 | max lev bwf02 | bool | e 65.1 bwf 02maximum level | 966 |
| %QW300 | bwf02_sp_flowrate | word | flow rate speed set bwf 02(client machine)(4-20ma) | 1355 |
| %I20.2 | bwf02 pulse | bool | old address | 1518 |
| %IW270 | bwf02_level | int | level bwf 02 (client machine) | 1547 |
| %I11.7 | bwf 02 run | bool | e 64.6 bwf 02 run | 1549 |
| %IW266 | bwf02_flowrate | int | flow rate bwf 02 (client machine) | 1550 |
| %Q6.3 | consent start bwf02 | bool | a 68.3 bwf 02 remotestart | 1667 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| Editor_BWF02 | DB26,INT10 | PLC | 00416 |
| BWF02\Risposta | DB11,X72.1 | PLC | 000BA |
| BWF02\StatusOK | DB11,X72.0 | PLC | 000B8 |
| BWF02\Allarme1 | DB11,X72.2 | PLC | 000B7 |
| BWF02\Flag | DB2,X12.5 | PLC | 000B6 |
| I_Level_BWF02 | DB13,INT34 | PLC | 00061 |
| I_Flow_rate_BWF02 | DB13,INT30 | PLC | 0005E |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 16 | client motor 18 allarm bwf02--------------- | [네트워크 425](networks/network-425.html) | 6/11 |
| allarm manager | 9 | clear values of report at the end of the recording | [네트워크 935](networks/network-935.html) | 5/11 |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| simulation | 8 | motors simulated | [네트워크 1086](networks/network-1086.html) | 10/15 |
| hmi | 37 | bwf02 | [네트워크 1214](networks/network-1214.html) | 10/17 |
| analog output conversion | 1 | plant limits | [네트워크 1679](networks/network-1679.html) | 21/61 |
| analog output conversion | 4 | bwf02 client feeder | [네트워크 1682](networks/network-1682.html) | 7/18 |
| analog output conversion | 5 | bwf02 speed calculation | [네트워크 1683](networks/network-1683.html) | 8/23 |
| analog input conversion | 6 | client 2 bwf02 flow rate | [네트워크 1736](networks/network-1736.html) | 9/26 |
| analog input conversion | 8 | client 4 level indicator bwf02 | [네트워크 1738](networks/network-1738.html) | 2/9 |
| analog input conversion | 46 | contactor ton passed in bwf | [네트워크 1776](networks/network-1776.html) | 7/17 |
| allarms 1 | 3 | bwf02 | [네트워크 1783](networks/network-1783.html) | 13/24 |
| allarms 1 | 4 | bwf02 | [네트워크 1784](networks/network-1784.html) | 11/19 |
| allarms 1 | 40 | bwf01/bwf02 | [네트워크 1820](networks/network-1820.html) | 16/29 |
| auto start motors | 9 | production counters | [네트워크 1849](networks/network-1849.html) | 21/65 |
| motors 1 | 4 | bwf02 | [네트워크 1933](networks/network-1933.html) | 11/21 |
| motors 1 | 5 | bwf01/02 | [네트워크 1934](networks/network-1934.html) | 17/29 |
| motors 1 | 44 | liw feeder | [네트워크 1973](networks/network-1973.html) | 13/24 |
| allarms 3 | 2 | low tc03 temperature | [네트워크 1980](networks/network-1980.html) | 35/74 |
| allarms 3 | 15 | incorrect scraps feeder formula | [네트워크 1993](networks/network-1993.html) | 11/24 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 425 | SCoil | Allarm.motor_client_18_fault | (ON AND HOPPER CONVEYOR 2FAULT) | 조건 성립 시 Set |
| 425 | RCoil | Allarm.motor_client_18_fault | ((ON AND NOT [HOPPER CONVEYOR 2FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1214 | Coil | ORef UID 33 | ORef UID 32 | 조건에 따른 Coil 기록 |
| 1214 | Coil | ORef UID 35 | ORef UID 34 | 조건에 따른 Coil 기록 |
| 1214 | Coil | ORef UID 40 | (ORef UID 36 OR ORef UID 37 OR ORef UID 38 OR ORef UID 39) | 조건에 따른 Coil 기록 |
| 1682 | Move | Data.SET_PERC_BWF02 | (ON AND [Data.SET_PERC_BWF02 < 0]) | Move 입력 0 |
| 1682 | Move | Data.SET_PERC_BWF02 | (ON AND [Data.SET_PERC_BWF02 > 100]) | Move 입력 100 |
| 1683 | Move | App00 | ON | Move 입력 Data.SET_PERC_BWF02 |
| 1683 | Move | App01 | ON | Move 입력 Data2.Set_TH |
| 1683 | Move | App03 | ON | Move 입력 Data2.Set_MAX_TH2 |
| 1683 | Move | BWF02_SP_FlowRate | Div UID 381.eno (블록 동작 확인) | Move 입력 App03 |
| 1736 | Move | Data.CLIENT_2 | ((ON AND OFF) AND NOT [BWF 02 RUN]) | Move 입력 0 |
| 1783 | SdCoil | Tag_50 | ((ON AND Consent Start BWF02) AND NOT [Inputs.BWF 02 RUN]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#10S |
| 1783 | SCoil | Allarm.BWF02_FAULT | ((((ON AND Consent Start BWF02) AND Tag_50) AND NOT [Inputs.BWF 02 RUN]) OR ((ON AND Consent Start BWF02) AND Inputs.BWF02 FAULT)) | 조건 성립 시 Set |
| 1783 | RCoil | Allarm.BWF02_FAULT | (((ON AND Flag.RESET_ALLARM) AND Allarm.BWF02_FAULT) AND NOT [Inputs.BWF02 FAULT]) | 조건 성립 시 Reset |
| 1784 | SCoil | Allarm.BWF02_min_LEVEL | ((ON AND Consent Start BWF02) AND Inputs.min LEV BWF02) | 조건 성립 시 Set |
| 1784 | SCoil | Allarm.BWF02_MAX_LEVEL | (ON AND Inputs.MAX LEV BWF02) | 조건 성립 시 Set |
| 1784 | RCoil | Allarm.BWF02_min_LEVEL | ((ON AND Flag.RESET_ALLARM) AND NOT [Inputs.min LEV BWF02]) | 조건 성립 시 Reset |
| 1784 | RCoil | Allarm.BWF02_MAX_LEVEL | ((ON AND Flag.RESET_ALLARM) AND NOT [Inputs.MAX LEV BWF02]) | 조건 성립 시 Reset |
| 1820 | SdCoil | Tag_90 | (OFF AND NOT [Inputs.BWF1_INVERTER_HIGH_SPEED]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#30S |
| 1820 | SCoil | Allarm.BWF01_Fault_Control | ((OFF AND NOT [Inputs.BWF1_INVERTER_HIGH_SPEED]) AND Tag_90) | 조건 성립 시 Set |
| 1820 | SdCoil | Tag_91 | (OFF AND NOT [Inputs.BWF2_INVERTER_HIGH_SPEED]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#30S |
| 1820 | SCoil | Allarm.BWF02_Fault_Control | ((OFF AND NOT [Inputs.BWF2_INVERTER_HIGH_SPEED]) AND Tag_91) | 조건 성립 시 Set |
| 1820 | RCoil | Allarm.BWF01_Fault_Control | (((OFF AND Flag.RESET_ALLARM) AND Allarm.BWF01_Fault_Control) AND Inputs.BWF1_INVERTER_HIGH_SPEED) | 조건 성립 시 Reset |
| 1820 | RCoil | Allarm.BWF02_Fault_Control | (((OFF AND Flag.RESET_ALLARM) AND Allarm.BWF02_Fault_Control) AND Inputs.BWF2_INVERTER_HIGH_SPEED) | 조건 성립 시 Reset |
| 1933 | RCoil | Flag.M_BWF02 | ((ON AND Allarm.BWF02_FAULT) OR (ON AND Allarm.BWF02_Fault_Control) OR (ON AND [Data.SET_PERC_BWF02 = 0]) OR (ON AND NOT [Inputs.BWF02 OK]) OR (ON AND NOT [Inputs.BC01 run]) OR (ON AND Disable_Load_RD01)) | 조건 성립 시 Reset |
| 1933 | Coil | Consent Start BWF02 | (ON AND Flag.M_BWF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| BWF02-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| BWF02-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| BWF02-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| BWF02-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| BWF02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| BWF02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| BWF02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| BWF02-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| BWF02-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## LIW · 외부 LIW 피더

고객 피더 시스템 원격 시작과 속도 설정. BWF 계통 및 배출 분기 상태와 교차 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 85 / PDF 86, FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I14.1 | liw systemautoreader | bool | e 15.0 liw systemautoreader | 529 |
| %Q6.1 | start liw feeder | bool | a 61.1 liw feederremote start | 679 |
| %QW302 | liw_sp_speed | word | speed set liw system(client machine)(4-20ma) | 1346 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 15 | client motor 17 | [네트워크 1016](networks/network-1016.html) | 7/18 |
| analog output conversion | 13 | send output to perifery | [네트워크 1691](networks/network-1691.html) | 4/11 |
| motors 1 | 44 | liw feeder | [네트워크 1973](networks/network-1973.html) | 13/24 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1973 | SdCoil | Tag_127 | ((ON AND Inputs.BWF 01 RUN) OR (ON AND Inputs.BWF 02 RUN)) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#15M |
| 1973 | SCoil | START LIW FEEDER | (((ON AND Inputs.BWF 01 RUN) OR (ON AND Inputs.BWF 02 RUN)) AND PV-03 GATE EV) | 조건 성립 시 Set |
| 1973 | SdCoil | Tag_128 | (((ON AND START LIW FEEDER) AND NOT [Inputs.BWF 01 RUN]) AND NOT [Inputs.BWF 02 RUN]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#15M |
| 1973 | RCoil | START LIW FEEDER | ((ON AND START LIW FEEDER) AND Tag_128) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LIW-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| LIW-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| LIW-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| LIW-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LIW-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LIW-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LIW-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LIW-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## CLIENT-CL01 · Apron conveyor A

PLC 외부 모터/설비 채널 01. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I14.6 | apron conveyor a fault | bool | e 17.6 apron conveyor "a"fault | 533 |
| %I12.3 | apron conveyor a run | bool | e 13.0 apron conveyor "a"run | 967 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 1 | apron conveyor fault (cl01) | [네트워크 410](networks/network-410.html) | 6/11 |
| time work motor | 1 | client motor 1 | [네트워크 1002](networks/network-1002.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 410 | SCoil | Allarm.motor_client_01_fault | (ON AND APRON CONVEYOR A FAULT) | 조건 성립 시 Set |
| 410 | RCoil | Allarm.motor_client_01_fault | ((ON AND NOT [APRON CONVEYOR A FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1002 | Move | hours motors.CLIENT_MOTOR_1_HOUR | ((Tag_47 AND APRON CONVEYOR A RUN) AND [hours motors.CLIENT_MOTOR_1_MIN >= 60]) | Move 입력 1 |
| 1002 | Move | hours motors.CLIENT_MOTOR_1_MIN | Move UID 92.eno (블록 동작 확인) | Move 입력 0 |
| 1002 | SCoil | Flag_Aggiorna_DB | Move UID 95.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL01-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL01-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL01-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL01-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL01-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL02 · Impactor

PLC 외부 모터/설비 채널 02. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I14.7 | impactor fault | bool | e 17.7 impactor fault | 534 |
| %I12.4 | impactor run | bool | e 13.1 impactor run | 968 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| IMPACTOR_RUN | DB13,X12.4 | PLC | 00404 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 2 | client motor 2 allarm | [네트워크 411](networks/network-411.html) | 6/11 |
| time work motor | 2 | client motor 2 | [네트워크 1003](networks/network-1003.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 411 | SCoil | Allarm.motor_client_02_fault | (ON AND IMPACTOR FAULT) | 조건 성립 시 Set |
| 411 | RCoil | Allarm.motor_client_02_fault | ((ON AND NOT [IMPACTOR FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1003 | Move | hours motors.CLIENT_MOTOR_2_HOUR | ((Tag_47 AND IMPACTOR RUN) AND [hours motors.CLIENT_MOTOR_2_MIN >= 60]) | Move 입력 1 |
| 1003 | Move | hours motors.CLIENT_MOTOR_2_MIN | Move UID 146.eno (블록 동작 확인) | Move 입력 0 |
| 1003 | SCoil | Flag_Aggiorna_DB | Move UID 149.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL02-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL02-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL02-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL02-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL02-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL02-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |
| CLIENT-CL02-V-06 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL03 · Impact vibration feeder

PLC 외부 모터/설비 채널 03. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I15.0 | impact vibrationfeeder fault | bool | e 18.0 impact vibrationfeeder fault | 535 |
| %I12.5 | impact vibrationfeeder run | bool | e 13.2 impact vibrationfeeder run | 969 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 3 | client motor 3 allarm | [네트워크 412](networks/network-412.html) | 6/11 |
| time work motor | 3 | client motor 3 | [네트워크 1004](networks/network-1004.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 412 | SCoil | Allarm.motor_client_03_fault | (ON AND IMPACT VIBRATIONFEEDER FAULT) | 조건 성립 시 Set |
| 412 | RCoil | Allarm.motor_client_03_fault | ((ON AND NOT [IMPACT VIBRATIONFEEDER FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1004 | Move | hours motors.CLIENT_MOTOR_3_HOUR | ((Tag_47 AND IMPACT VIBRATIONFEEDER RUN) AND [hours motors.CLIENT_MOTOR_3_MIN >= 60]) | Move 입력 1 |
| 1004 | Move | hours motors.CLIENT_MOTOR_3_MIN | Move UID 200.eno (블록 동작 확인) | Move 입력 0 |
| 1004 | SCoil | Flag_Aggiorna_DB | Move UID 203.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL03-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL03-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL03-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL03-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL03-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL03-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL03-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL03-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL03-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL04 · Belt conveyor A

PLC 외부 모터/설비 채널 04. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q61.2 | start client motor 4 | bool | it should be free but it is used | 480 |
| %I15.1 | belt conveyor a fault | bool | e 18.1 belt conveyor "a"fault | 536 |
| %I12.6 | belt conveyor a run | bool | e 13.3 belt conveyor "a"run | 970 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 4 | client motor 4 allarm | [네트워크 413](networks/network-413.html) | 6/11 |
| time work motor | 4 | client motor 4 | [네트워크 1005](networks/network-1005.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 413 | SCoil | Allarm.motor_client_04_fault | (ON AND BELT CONVEYOR  A FAULT) | 조건 성립 시 Set |
| 413 | RCoil | Allarm.motor_client_04_fault | ((ON AND NOT [BELT CONVEYOR  A FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1005 | Move | hours motors.CLIENT_MOTOR_4_HOUR | ((Tag_47 AND BELT CONVEYOR A RUN) AND [hours motors.CLIENT_MOTOR_4_MIN >= 60]) | Move 입력 1 |
| 1005 | Move | hours motors.CLIENT_MOTOR_4_MIN | Move UID 254.eno (블록 동작 확인) | Move 입력 0 |
| 1005 | SCoil | Flag_Aggiorna_DB | Move UID 257.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL04-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL04-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL04-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL04-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL04-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL04-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL04-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL04-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL04-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL05 · Air knife

PLC 외부 모터/설비 채널 05. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I15.2 | air knife fault | bool | e 18.2 air knife fault | 537 |
| %I12.7 | air knife run | bool | e 13.4 air knife run | 978 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 5 | client motor 5 allarm | [네트워크 414](networks/network-414.html) | 6/11 |
| time work motor | 5 | client motor 5 | [네트워크 1006](networks/network-1006.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 414 | SCoil | Allarm.motor_client_05_fault | (ON AND AIR KNIFE FAULT) | 조건 성립 시 Set |
| 414 | RCoil | Allarm.motor_client_05_fault | ((ON AND NOT [AIR KNIFE FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1006 | Move | hours motors.CLIENT_MOTOR_5_HOUR | ((Tag_47 AND AIR KNIFE RUN) AND [hours motors.CLIENT_MOTOR_5_MIN >= 60]) | Move 입력 1 |
| 1006 | Move | hours motors.CLIENT_MOTOR_5_MIN | Move UID 308.eno (블록 동작 확인) | Move 입력 0 |
| 1006 | SCoil | Flag_Aggiorna_DB | Move UID 311.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL05-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL05-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL05-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL05-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL05-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL05-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL05-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL05-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL05-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL06 · Belt conveyor B

PLC 외부 모터/설비 채널 06. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q61.3 | start client motor 6 | bool | it should be free but it is used | 481 |
| %I13.0 | belt conveyor b run | bool | e 13.5 belt conveyor "b"run | 520 |
| %I15.3 | belt conveyor b fault | bool | e 18.3 belt conveyor "b"fault | 538 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 6 | client motor 6 allarm | [네트워크 415](networks/network-415.html) | 6/11 |
| time work motor | 6 | client motor 6 | [네트워크 1007](networks/network-1007.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 415 | SCoil | Allarm.motor_client_06_fault | (ON AND BELT CONVEYOR B FAULT) | 조건 성립 시 Set |
| 415 | RCoil | Allarm.motor_client_06_fault | ((ON AND NOT [BELT CONVEYOR B FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1007 | Move | hours motors.CLIENT_MOTOR_6_HOUR | ((Tag_47 AND BELT CONVEYOR B RUN) AND [hours motors.CLIENT_MOTOR_6_MIN >= 60]) | Move 입력 1 |
| 1007 | Move | hours motors.CLIENT_MOTOR_6_MIN | Move UID 362.eno (블록 동작 확인) | Move 입력 0 |
| 1007 | SCoil | Flag_Aggiorna_DB | Move UID 365.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL06-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL06-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL06-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL06-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL06-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL06-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL06-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL06-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL06-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL07 · Shredder 1

PLC 외부 모터/설비 채널 07. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I13.1 | shredder 1 run | bool | e 13.6 shredder 1 run | 521 |
| %I15.4 | shredder 1 fault | bool | e 18.4 shredder 1 fault | 539 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 7 | client motor 7 allarm | [네트워크 416](networks/network-416.html) | 6/11 |
| time work motor | 7 | client motor 7 | [네트워크 1008](networks/network-1008.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 416 | SCoil | Allarm.motor_client_07_fault | (ON AND SHREDDER 1 FAULT) | 조건 성립 시 Set |
| 416 | RCoil | Allarm.motor_client_07_fault | ((ON AND NOT [SHREDDER 1 FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1008 | Move | hours motors.CLIENT_MOTOR_7_HOUR | ((Tag_47 AND SHREDDER 1 RUN) AND [hours motors.CLIENT_MOTOR_7_MIN >= 60]) | Move 입력 1 |
| 1008 | Move | hours motors.CLIENT_MOTOR_7_MIN | Move UID 416.eno (블록 동작 확인) | Move 입력 0 |
| 1008 | SCoil | Flag_Aggiorna_DB | Move UID 419.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL07-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL07-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL07-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL07-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL07-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL07-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL07-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL07-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL07-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL08 · Shredder vibration feeder

PLC 외부 모터/설비 채널 08. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q61.4 | start client motor 8 | bool | it should be free but it is used | 482 |
| %I13.2 | shredder vibrationfeeder run | bool | e 13.7 shredder vibrationfeeder run | 522 |
| %I15.5 | shredder vibrationfeeder fault | bool | e 18.5 shredder vibrationfeeder fault | 540 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 8 | client motor 8 allarm | [네트워크 417](networks/network-417.html) | 6/11 |
| time work motor | 8 | client motor 8 | [네트워크 1009](networks/network-1009.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 417 | SCoil | Allarm.motor_client_08_fault | (ON AND SHREDDER VIBRATIONFEEDER FAULT) | 조건 성립 시 Set |
| 417 | RCoil | Allarm.motor_client_08_fault | ((ON AND NOT [SHREDDER VIBRATIONFEEDER FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1009 | Move | hours motors.CLIENT_MOTOR_8_HOUR | ((Tag_47 AND SHREDDER VIBRATIONFEEDER RUN) AND [hours motors.CLIENT_MOTOR_8_MIN >= 60]) | Move 입력 1 |
| 1009 | Move | hours motors.CLIENT_MOTOR_8_MIN | Move UID 470.eno (블록 동작 확인) | Move 입력 0 |
| 1009 | SCoil | Flag_Aggiorna_DB | Move UID 473.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL08-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL08-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL08-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL08-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL08-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL08-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL08-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL08-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL08-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL09 · Belt conveyor C

PLC 외부 모터/설비 채널 09. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q61.5 | start client motor 9 | bool | it should be free but it is used | 483 |
| %I13.3 | belt conveyor c run | bool | e 14.0 belt conveyor "c"run | 523 |
| %I15.6 | belt conveyor c fault | bool | e 18.6 belt conveyor "c"fault | 541 |
| %I16.6 | belt conveyor c fault_doppio! | bool | e20.0 belt conveyor "c"fault | 567 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 9 | client motor 9 allarm | [네트워크 418](networks/network-418.html) | 6/11 |
| time work motor | 9 | client motor 9 | [네트워크 1010](networks/network-1010.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 418 | SCoil | Allarm.motor_client_09_fault | (ON AND BELT CONVEYOR C FAULT) | 조건 성립 시 Set |
| 418 | RCoil | Allarm.motor_client_09_fault | ((ON AND NOT [BELT CONVEYOR C FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1010 | Move | hours motors.CLIENT_MOTOR_9_HOUR | ((Tag_47 AND BELT CONVEYOR  C RUN) AND [hours motors.CLIENT_MOTOR_9_MIN >= 60]) | Move 입력 1 |
| 1010 | Move | hours motors.CLIENT_MOTOR_9_MIN | Move UID 524.eno (블록 동작 확인) | Move 입력 0 |
| 1010 | SCoil | Flag_Aggiorna_DB | Move UID 527.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL09-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL09-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL09-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL09-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL09-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL09-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL09-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL09-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL09-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL10 · Rotex screen

PLC 외부 모터/설비 채널 10. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I13.4 | rotex screen run | bool | e 14.1 rotex screen run | 524 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 10 | client motor 10 allarm | [네트워크 419](networks/network-419.html) | 6/11 |
| time work motor | 10 | client motor 10 | [네트워크 1011](networks/network-1011.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 419 | SCoil | Allarm.motor_client_10_fault | (ON AND ROTEX SCREENFAULT) | 조건 성립 시 Set |
| 419 | RCoil | Allarm.motor_client_10_fault | ((ON AND NOT [ROTEX SCREENFAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1011 | Move | hours motors.CLIENT_MOTOR_10_HOUR | ((Tag_47 AND ROTEX SCREEN RUN) AND [hours motors.CLIENT_MOTOR_10_MIN >= 60]) | Move 입력 1 |
| 1011 | Move | hours motors.CLIENT_MOTOR_10_MIN | Move UID 578.eno (블록 동작 확인) | Move 입력 0 |
| 1011 | SCoil | Flag_Aggiorna_DB | Move UID 581.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL10-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL10-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL10-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL10-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL10-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL10-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL10-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL10-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL10-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL13 · Apron conveyor B

PLC 외부 모터/설비 채널 13. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I13.5 | apron conveyor b run | bool | e 14.4 apron conveyor "b"run | 525 |
| %I16.0 | apron conveyor b fault | bool | e19.2 apron conveyor "b"fault | 561 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 11 | client motor 13 allarm | [네트워크 420](networks/network-420.html) | 6/11 |
| time work motor | 11 | client motor 13 | [네트워크 1012](networks/network-1012.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 420 | SCoil | Allarm.motor_client_13_fault | (ON AND APRON CONVEYOR B FAULT) | 조건 성립 시 Set |
| 420 | RCoil | Allarm.motor_client_13_fault | ((ON AND NOT [APRON CONVEYOR B FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1012 | Move | hours motors.CLIENT_MOTOR_13_HOUR | ((Tag_47 AND APRON CONVEYOR B RUN) AND [hours motors.CLIENT_MOTOR_13_MIN >= 60]) | Move 입력 1 |
| 1012 | Move | hours motors.CLIENT_MOTOR_13_MIN | Move UID 740.eno (블록 동작 확인) | Move 입력 0 |
| 1012 | SCoil | Flag_Aggiorna_DB | Move UID 743.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL13-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL13-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL13-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL13-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL13-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL13-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL13-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL13-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL13-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL14 · Shredder 2

PLC 외부 모터/설비 채널 14. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I13.6 | shredder 2 run | bool | e 14.5 shredder 2 run | 526 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 12 | client motor 14 allarm | [네트워크 421](networks/network-421.html) | 6/11 |
| time work motor | 12 | client motor 14 | [네트워크 1013](networks/network-1013.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 421 | SCoil | Allarm.motor_client_14_fault | (ON AND SHREDDER 2FAULT) | 조건 성립 시 Set |
| 421 | RCoil | Allarm.motor_client_14_fault | ((ON AND NOT [SHREDDER 2FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1013 | Move | hours motors.CLIENT_MOTOR_14_HOUR | ((Tag_47 AND SHREDDER 2 RUN) AND [hours motors.CLIENT_MOTOR_14_MIN >= 60]) | Move 입력 1 |
| 1013 | Move | hours motors.CLIENT_MOTOR_14_MIN | Move UID 794.eno (블록 동작 확인) | Move 입력 0 |
| 1013 | SCoil | Flag_Aggiorna_DB | Move UID 797.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL14-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL14-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL14-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL14-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL14-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL14-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL14-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL14-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL14-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL15 · Belt conveyor D

PLC 외부 모터/설비 채널 15. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I16.2 | belt coveyor d fault | bool | e19.4 belt coveyor "d"fault | 563 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 13 | client motor 15 allarm | [네트워크 422](networks/network-422.html) | 6/11 |
| time work motor | 13 | client motor 15 | [네트워크 1014](networks/network-1014.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 422 | SCoil | Allarm.motor_client_15_fault | (ON AND BELT COVEYOR  D FAULT) | 조건 성립 시 Set |
| 422 | RCoil | Allarm.motor_client_15_fault | ((ON AND NOT [BELT COVEYOR  D FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1014 | Move | hours motors.CLIENT_MOTOR_15_HOUR | ((Tag_47 AND BELT CONVEYOR  D RUN) AND [hours motors.CLIENT_MOTOR_15_MIN >= 60]) | Move 입력 1 |
| 1014 | Move | hours motors.CLIENT_MOTOR_15_MIN | Move UID 848.eno (블록 동작 확인) | Move 입력 0 |
| 1014 | SCoil | Flag_Aggiorna_DB | Move UID 851.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL15-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL15-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL15-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL15-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL15-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL15-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL15-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL15-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL15-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL16 · Belt conveyor E

PLC 외부 모터/설비 채널 16. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I14.0 | belt conveyor e run | bool | e 14.7 belt conveyor "e"run | 528 |
| %I16.3 | belt conveyor e fault | bool | e19.5 belt conveyor "e"fault | 564 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 14 | client motor 16 allarm | [네트워크 423](networks/network-423.html) | 6/11 |
| time work motor | 14 | client motor 16 | [네트워크 1015](networks/network-1015.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 423 | SCoil | Allarm.motor_client_16_fault | (ON AND BELT CONVEYOR  E FAULT) | 조건 성립 시 Set |
| 423 | RCoil | Allarm.motor_client_16_fault | ((ON AND NOT [BELT CONVEYOR  E FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1015 | Move | hours motors.CLIENT_MOTOR_16_HOUR | ((Tag_47 AND BELT CONVEYOR E RUN) AND [hours motors.CLIENT_MOTOR_16_MIN >= 60]) | Move 입력 1 |
| 1015 | Move | hours motors.CLIENT_MOTOR_16_MIN | Move UID 902.eno (블록 동작 확인) | Move 입력 0 |
| 1015 | SCoil | Flag_Aggiorna_DB | Move UID 905.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL16-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL16-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL16-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL16-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL16-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL16-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL16-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL16-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL16-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL17 · Weighing hopper 2

PLC 외부 모터/설비 채널 17. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I16.4 | weighting hopper 2fault | bool | e19.6 weighting hopper 2fault | 565 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 15 | client motor 17 allarm | [네트워크 424](networks/network-424.html) | 6/11 |
| time work motor | 15 | client motor 17 | [네트워크 1016](networks/network-1016.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 424 | SCoil | Allarm.motor_client_17_fault | (ON AND WEIGHTING HOPPER 2FAULT) | 조건 성립 시 Set |
| 424 | RCoil | Allarm.motor_client_17_fault | ((ON AND NOT [WEIGHTING HOPPER 2FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1016 | Move | hours motors.CLIENT_MOTOR_17_HOUR | ((Tag_47 AND LIW SYSTEMAUTOREADER) AND [hours motors.CLIENT_MOTOR_17_MIN >= 60]) | Move 입력 1 |
| 1016 | Move | hours motors.CLIENT_MOTOR_17_MIN | Move UID 956.eno (블록 동작 확인) | Move 입력 0 |
| 1016 | SCoil | Flag_Aggiorna_DB | Move UID 959.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL17-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL17-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL17-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL17-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL17-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL17-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL17-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL17-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL17-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL18 · Hopper conveyor 2

PLC 외부 모터/설비 채널 18. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점:  P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I16.5 | hopper conveyor 2fault | bool | e19.7 hopper conveyor 2fault | 566 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 16 | client motor 18 allarm bwf02--------------- | [네트워크 425](networks/network-425.html) | 6/11 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 425 | SCoil | Allarm.motor_client_18_fault | (ON AND HOPPER CONVEYOR 2FAULT) | 조건 성립 시 Set |
| 425 | RCoil | Allarm.motor_client_18_fault | ((ON AND NOT [HOPPER CONVEYOR 2FAULT]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL18-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL18-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL18-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL18-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL18-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL18-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL18-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL18-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL18-V-05 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## CLIENT-CL19 · Primary shredder

PLC 외부 모터/설비 채널 19. 원격 신호와 실제 외부 제어반 상태를 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 86 / PDF 87, FG 87 / PDF 88, FG 88 / PDF 89, FG 89 / PDF 90, FG 90 / PDF 91, FG 91 / PDF 92, FG 92 / PDF 93, FG 93 / PDF 94, FG 94 / PDF 95, FG 95 / PDF 96.

확인할 특이점: 원본에는 Primary shredder run 입력을 motor_client_19_fault와 연결하는 네트워크가 있다. 명칭만으로 고장 입력의 방향을 결정하지 말고 접점 극성과 외부 신호 계약을 확인한다. P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I14.2 | primaryshredder run | bool | e 15.2 primaryshredder run | 530 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| PRIMARYSHREDDER_RUN | DB13,X14.2 | PLC | 003F7 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 17 | primary shradder fault (cl19) | [네트워크 426](networks/network-426.html) | 6/11 |
| time work motor | 16 | client motor 19 | [네트워크 1017](networks/network-1017.html) | 7/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 426 | SCoil | Allarm.motor_client_19_fault | (ON AND PRIMARYSHREDDER RUN) | 조건 성립 시 Set |
| 426 | RCoil | Allarm.motor_client_19_fault | ((ON AND NOT [PRIMARYSHREDDER RUN]) AND Flag.RESET_ALLARM) | 조건 성립 시 Reset |
| 1017 | Move | hours motors.CLIENT_MOTOR_19_HOUR | ((Tag_47 AND PRIMARYSHREDDER RUN) AND [hours motors.CLIENT_MOTOR_19_MIN >= 60]) | Move 입력 1 |
| 1017 | Move | hours motors.CLIENT_MOTOR_19_MIN | Move UID 1064.eno (블록 동작 확인) | Move 입력 0 |
| 1017 | SCoil | Flag_Aggiorna_DB | Move UID 1067.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 인터페이스 의미: 외부 제어반의 준비/운전/고장 신호가 정상일 때 1인지 0인지와 원격 요청의 펄스/유지 방식을 확인한다.
2. 주소·번호: 전기도면 단자, 현재 PLC I/Q, 과거 주소 주석과 CLIENT-CL 번호를 대조한다.
3. 시간·Handshake: 허가 요청, 외부 준비, 실제 운전 피드백, 고장과 해제 응답의 시간을 각각 기록한다.
4. 아날로그 값: 유량/레벨/속도 설정이 있는 계통은 범위·단위·원시값·환산값·통신 상태를 함께 기록한다.
5. 복귀: 외부 고장 해소·신호 복귀·PLC 알람 Reset·재허가를 구분해 검증한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CLIENT-CL19-SIM-01 | Handshake 정상 | 준비→허가→운전 응답 | 번호·I/O 방향·지연 확인 | 설계·미실행 |
| CLIENT-CL19-SIM-02 | 외부 고장 | 정상 상태에서 외부 신호 변경 | 접점 극성·알람 유지·재허가 확인 | 설계·미실행 |
| CLIENT-CL19-SIM-03 | 신호 누락 | 준비·피드백·통신 상태 누락 | 고장 검출 및 HMI 표시 확인 | 설계·미실행 |
| CLIENT-CL19-SIM-04 | 복귀 | 고장 해제·Reset·요청 유지/해제 | 재기동 조건과 잔존 요청 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CLIENT-CL19-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CLIENT-CL19-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CLIENT-CL19-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CLIENT-CL19-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| CLIENT-CL19-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |
| CLIENT-CL19-V-06 | 불일치/특이점 | P&ID의 공압 실린더 CL 번호와 다른 이름 공간으로 보관한다. | 확인 대기 |

## TC01 · 온도 계측

AB01 챔버 온도.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 77 / PDF 78.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW272 | tc01 | int | temperature chamber ab-01 | 1546 |
| %M80.2 | tc01-tc02control disable | bool |  | 1570 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| Editor_TC01 | DB26,INT22 | PLC | 00412 |
| I_TC_01 | DB13,INT36 | PLC | 00060 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| simulation | 14 |  | [네트워크 1092](networks/network-1092.html) | 18/42 |
| analog input conversion | 9 | tc-01 | [네트워크 1739](networks/network-1739.html) | 2/9 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 5 | set points fn01 | [네트워크 1845](networks/network-1845.html) | 24/63 |
| burner control | 3 | a 56.3 max.temperaturefilter | [네트워크 1856](networks/network-1856.html) | 4/8 |
| burner control | 5 | burner stop | [네트워크 1858](networks/network-1858.html) | 21/40 |
| burner control | 9 | a 56.6 start high flameburner | [네트워크 1862](networks/network-1862.html) | 25/51 |
| burner control | 11 | reduce speed mn01 se tc01 > 30°c the setpoint | [네트워크 1864](networks/network-1864.html) | 8/19 |
| burner control | 12 | burner lock | [네트워크 1865](networks/network-1865.html) | 17/31 |
| burner control | 15 | enable burner cleaning sequence | [네트워크 1868](networks/network-1868.html) | 71/151 |
| burner control | 17 | burner servomotor control fb41 pid mode | [네트워크 1870](networks/network-1870.html) | 15/29 |
| burner control | 22 | dryout warm first ramp | [네트워크 1875](networks/network-1875.html) | 23/58 |
| burner control | 23 | dryout warm second ramp | [네트워크 1876](networks/network-1876.html) | 9/23 |
| burner control | 24 | dryout warm third ramp | [네트워크 1877](networks/network-1877.html) | 13/33 |
| allarms 3 | 1 | max tc01 temperature | [네트워크 1979](networks/network-1979.html) | 21/45 |
| allarms 3 | 6 | ro01 oxigen low limit | [네트워크 1984](networks/network-1984.html) | 12/26 |
| allarms 3 | 7 | ro01-ro02 signal compare fault | [네트워크 1985](networks/network-1985.html) | 13/28 |
| allarms 3 | 8 | tc01/tc02 signal compare fault | [네트워크 1986](networks/network-1986.html) | 15/32 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1864 | SCoil | Riduce MN01 | ((OFF AND ON) AND [Manage_TC1_2.PID_Ref_Temp >= App02]) | 조건 성립 시 Set |
| 1864 | RCoil | Riduce MN01 | ((OFF AND ON) AND [Manage_TC1_2.PID_Ref_Temp < App03]) | 조건 성립 시 Reset |
| 1979 | SdCoil | Tag_99 | (ON AND [Manage_TC1_2.PID_Ref_Temp > Data.TC01_MAX_ALL]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#6S |
| 1979 | SCoil | Allarm.MAX_TC01_TEMP | ((ON AND [Manage_TC1_2.PID_Ref_Temp > Data.TC01_MAX_ALL]) AND Tag_99) | 조건 성립 시 Set |
| 1979 | RCoil | Allarm.MAX_TC01_TEMP | (Sub UID 165.eno (블록 동작 확인) AND [Manage_TC1_2.PID_Ref_Temp < app00]) | 조건 성립 시 Reset |
| 1979 | SCoil | Flag.STOP_HORN | (Sub UID 165.eno (블록 동작 확인) AND [Manage_TC1_2.PID_Ref_Temp < app00]) | 조건 성립 시 Set |
| 1979 | SdCoil | Tag_100 | ((ON AND [Manage_TC1_2.PID_Ref_Temp > max_max_tc1]) OR (ON AND [Manage_TC1_2.PID_Ref_Temp > 1250.0]) OR (ON AND [Manage_TC1_2.PID_Ref_Temp < -60.0])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#6S |
| 1979 | SCoil | Allarm.MAX_MAX_TC01_TEMP | (((ON AND [Manage_TC1_2.PID_Ref_Temp > max_max_tc1]) OR (ON AND [Manage_TC1_2.PID_Ref_Temp > 1250.0]) OR (ON AND [Manage_TC1_2.PID_Ref_Temp < -60.0])) AND Tag_100) | 조건 성립 시 Set |
| 1979 | RCoil | Allarm.MAX_MAX_TC01_TEMP | ((ON AND Flag.RESET_ALLARM) AND Allarm.MAX_MAX_TC01_TEMP) | 조건 성립 시 Reset |
| 1986 | SdCoil | Tag_108 | (((((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC01 > 400]) OR ((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC02 > 400])) AND [app02 < -100]) OR ((((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC01 > 400]) OR ((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC02 > 400])) AND [app02 > 100])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1M |
| 1986 | SCoil | Allarm.TC01_TC02_COMP_FAULT | ((((((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC01 > 400]) OR ((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC02 > 400])) AND [app02 < -100]) OR ((((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC01 > 400]) OR ((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC02 > 400])) AND [app02 > 100])) AND Tag_108) | 조건 성립 시 Set |
| 1986 | RCoil | Allarm.TC01_TC02_COMP_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.TC01_TC02_COMP_FAULT) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| TC01-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| TC01-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| TC01-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| TC01-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| TC01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| TC01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| TC01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| TC01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| TC01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## TC02 · 온도 계측

AB01 안전 온도 채널.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 77 / PDF 78.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW274 | tc02 | int | safety temperature chamber ab-01 | 1545 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| I_TC_02 | DB13,INT38 | PLC | 00062 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| simulation | 14 |  | [네트워크 1092](networks/network-1092.html) | 18/42 |
| analog input conversion | 10 | tc-02 | [네트워크 1740](networks/network-1740.html) | 2/9 |
| burner control | 5 | burner stop | [네트워크 1858](networks/network-1858.html) | 21/40 |
| allarms 3 | 8 | tc01/tc02 signal compare fault | [네트워크 1986](networks/network-1986.html) | 15/32 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1986 | SdCoil | Tag_108 | (((((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC01 > 400]) OR ((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC02 > 400])) AND [app02 < -100]) OR ((((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC01 > 400]) OR ((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC02 > 400])) AND [app02 > 100])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1M |
| 1986 | SCoil | Allarm.TC01_TC02_COMP_FAULT | ((((((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC01 > 400]) OR ((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC02 > 400])) AND [app02 < -100]) OR ((((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC01 > 400]) OR ((ON AND NOT [TC01-TC02control disable]) AND [Data.Temp_TC02 > 400])) AND [app02 > 100])) AND Tag_108) | 조건 성립 시 Set |
| 1986 | RCoil | Allarm.TC01_TC02_COMP_FAULT | ((ON AND Flag.RESET_ALLARM) AND Allarm.TC01_TC02_COMP_FAULT) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| TC02-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| TC02-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| TC02-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| TC02-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| TC02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| TC02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| TC02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| TC02-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| TC02-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## TC03 · 온도 계측

배출 가스 온도·MV01 관련 제어 값.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 77 / PDF 78.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M40.7 | tc03 close | bool |  | 34 |
| %M41.1 | tc03 close2 | bool |  | 35 |
| %M40.6 | tc03 open | bool |  | 36 |
| %M41.0 | tc03 open2 | bool |  | 37 |
| %M11.1 | down tc03 pid mv04 | bool |  | 106 |
| %IW276 | tc03 | int | temperature control outputsmoke | 1544 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| Editor_TC03 | DB26,INT20 | PLC | 00413 |
| I_TC_03 | DB13,INT40 | PLC | 00063 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| valve control loop | 1 | mv01 controlled by tc03 | [네트워크 1702](networks/network-1702.html) | 35/61 |
| analog input conversion | 11 | tc-03 | [네트워크 1741](networks/network-1741.html) | 2/9 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| burner control | 5 | burner stop | [네트워크 1858](networks/network-1858.html) | 21/40 |
| burner control | 9 | a 56.6 start high flameburner | [네트워크 1862](networks/network-1862.html) | 25/51 |
| burner control | 12 | burner lock | [네트워크 1865](networks/network-1865.html) | 17/31 |
| burner control | 17 | burner servomotor control fb41 pid mode | [네트워크 1870](networks/network-1870.html) | 15/29 |
| motors 1 | 2 | block load | [네트워크 1931](networks/network-1931.html) | 11/21 |
| allarms 3 | 2 | low tc03 temperature | [네트워크 1980](networks/network-1980.html) | 35/74 |
| cyc_int5 ogni 100ms | 5 |  | [네트워크 8](networks/network-8.html) | 2/6 |
| cyc_int5 ogni 100ms | 8 | controll tc03 moduling mv01 | [네트워크 11](networks/network-11.html) | 13/46 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1702 | RCoil | Flag.M_MV01_OPEN | ((ON AND Inputs.MV01 Open) OR (ON AND Flag.M_MV01_Close) OR (ON AND Flag.MV01_Auto)) | 조건 성립 시 Reset |
| 1702 | RCoil | Flag.M_MV01_Close | ((ON AND Inputs.MV01 Close) OR (ON AND Flag.M_MV01_OPEN) OR (ON AND Flag.MV01_Auto)) | 조건 성립 시 Reset |
| 1702 | Coil | Start Open MV-01 | (((((((((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.MV01_Auto) AND UP MV01 PID) OR ((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.M_MV01_OPEN)) AND MV WORK PULSE) OR (((((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.MV01_Auto) AND UP MV01 PID) OR ((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.M_MV01_OPEN)) AND ORef UID 172)) AND NOT [Start Close MV-01]) AND NOT [Inputs.MV01 Open]) AND NOT [HMI_DB.ResetEncoderProcedure_MV01]) | 조건에 따른 Coil 기록 |
| 1702 | Coil | Start Close MV-01 | ((((((((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.MV01_Auto) AND DOWN MV01 PID) OR ((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.M_MV01_Close)) AND MV WORK PULSE) OR (((((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.MV01_Auto) AND DOWN MV01 PID) OR ((ON AND NOT [Allarm.MV01_FAULT]) AND Flag.M_MV01_Close)) AND ON) OR ((ON AND NOT [Allarm.MV01_FAULT]) AND HMI_DB.ResetEncoderProcedure_MV01)) AND NOT [Start Open MV-01]) AND NOT [Inputs.MV01 Close]) | 조건에 따른 Coil 기록 |
| 1980 | SdCoil | Tag_101 | (((ON AND Inputs.BWF 01 RUN) OR (ON AND Inputs.BWF 02 RUN)) AND [Data.Temp_TC03 < Data.TC03_MIN_ALL]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#3S |
| 1980 | SCoil | Allarm.LOW_TC03_TEMP | ((((ON AND Inputs.BWF 01 RUN) OR (ON AND Inputs.BWF 02 RUN)) AND [Data.Temp_TC03 < Data.TC03_MIN_ALL]) AND Tag_101) | 조건 성립 시 Set |
| 1980 | Move | Data.TC03_MIN_ALL | (ON AND [Data.TC03_MIN_ALL < 200]) | Move 입력 200 |
| 1980 | RCoil | Allarm.LOW_TC03_TEMP | (Add UID 352.eno (블록 동작 확인) AND [Data.Temp_TC03 > app00]) | 조건 성립 시 Reset |
| 1980 | SCoil | Flag.STOP_HORN | (Add UID 352.eno (블록 동작 확인) AND [Data.Temp_TC03 > app00]) | 조건 성립 시 Set |
| 1980 | SdCoil | Tag_102 | (ON AND [Data.Temp_TC03 > Data.TC03_MAX_ALL]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#3S |
| 1980 | SCoil | Allarm.MAX_TC03_TEMP | ((ON AND [Data.Temp_TC03 > Data.TC03_MAX_ALL]) AND Tag_102) | 조건 성립 시 Set |
| 1980 | RCoil | Allarm.MAX_TC03_TEMP | (Sub UID 382.eno (블록 동작 확인) AND [Data.Temp_TC03 < app00]) | 조건 성립 시 Reset |
| 1980 | SCoil | Flag.STOP_HORN | (Sub UID 382.eno (블록 동작 확인) AND [Data.Temp_TC03 < app00]) | 조건 성립 시 Set |
| 1980 | SdCoil | Tag_103 | ((ON AND [Data.Temp_TC03 > max_max_tc3]) OR (ON AND [Data.Temp_TC03 > 750]) OR (ON AND [Data.Temp_TC03 < -60])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#3S |
| 1980 | SCoil | Allarm.MAX_MAX_TC03_TEMP | (((ON AND [Data.Temp_TC03 > max_max_tc3]) OR (ON AND [Data.Temp_TC03 > 750]) OR (ON AND [Data.Temp_TC03 < -60])) AND Tag_103) | 조건 성립 시 Set |
| 1980 | RCoil | Allarm.MAX_MAX_TC03_TEMP | ((ON AND Flag.RESET_ALLARM) AND Allarm.MAX_MAX_TC03_TEMP) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| TC03-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| TC03-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| TC03-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| TC03-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| TC03-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| TC03-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| TC03-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| TC03-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| TC03-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## TC04 · 온도 계측

FN01 베어링 PT100 온도.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 79 / PDF 80.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW258 | reserved tc04 | int |  | 896 |
| %IW260 | tc05 | int | probe sensor pt100 bearing fn-01 (tc-04) -30...250°c | 1511 |
| %IW256 | tc04 | int |  | 1512 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| I_TC_04 | DB13,INT24 | PLC | 00065 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| analog input conversion | 1 | tc04 | [네트워크 1731](networks/network-1731.html) | 2/9 |
| burner control | 5 | burner stop | [네트워크 1858](networks/network-1858.html) | 21/40 |
| motors 1 | 21 | preallarm fn01 | [네트워크 1950](networks/network-1950.html) | 12/22 |
| allarms 3 | 3 | max tc04 temperature | [네트워크 1981](networks/network-1981.html) | 21/43 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1981 | SdCoil | Tag_104 | ((ON AND [Data.Temp_TC04 > Data.TC04_TC05_MAX_ALL]) OR (ON AND [Data.Temp_TC04 > 120]) OR (ON AND [Data.Temp_TC04 < -60])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1M |
| 1981 | SCoil | Allarm.MAX_TC04_TEMP | (((ON AND [Data.Temp_TC04 > Data.TC04_TC05_MAX_ALL]) OR (ON AND [Data.Temp_TC04 > 120]) OR (ON AND [Data.Temp_TC04 < -60])) AND Tag_104) | 조건 성립 시 Set |
| 1981 | SdCoil | Tag_105 | ((ON AND [Data.Temp_TC05 > Data.TC04_TC05_MAX_ALL]) OR (ON AND [Data.Temp_TC05 > 120]) OR (ON AND [Data.Temp_TC05 < -60])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1M |
| 1981 | SCoil | Allarm.MAX_TC05_TEMP | ((((ON AND [Data.Temp_TC05 > Data.TC04_TC05_MAX_ALL]) OR (ON AND [Data.Temp_TC05 > 120]) OR (ON AND [Data.Temp_TC05 < -60])) AND Tag_105) AND ServiceBit) | 조건 성립 시 Set |
| 1981 | RCoil | Allarm.MAX_TC04_TEMP | ((ON AND Flag.RESET_ALLARM) AND Allarm.MAX_TC04_TEMP) | 조건 성립 시 Reset |
| 1981 | RCoil | Allarm.MAX_TC05_TEMP | ((ON AND Flag.RESET_ALLARM) AND Allarm.MAX_TC05_TEMP) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| TC04-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| TC04-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| TC04-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| TC04-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| TC04-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| TC04-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| TC04-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| TC04-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| TC04-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## TC05 · 온도 계측

FN01 다른 베어링 PT100 온도.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 79 / PDF 80.

확인할 특이점: 백업 TC05 설명에 TC04 및 -30...250°C가 섞인 문구가 있고 reserved tc05에는 다른 범위 문구가 남아 있다. 전기 FG79 센서 채널 및 현재 전송기 설정을 기준으로 대조한다. 

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW262 | reserved tc05 | int | probe sensor pt100 bearing fn-01 (tc-05) -30...350°c | 897 |
| %IW260 | tc05 | int | probe sensor pt100 bearing fn-01 (tc-04) -30...250°c | 1511 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| I_TC_05 | DB13,INT26 | PLC | 0005B |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| analog input conversion | 2 | tc-05 | [네트워크 1732](networks/network-1732.html) | 2/9 |
| burner control | 5 | burner stop | [네트워크 1858](networks/network-1858.html) | 21/40 |
| motors 1 | 21 | preallarm fn01 | [네트워크 1950](networks/network-1950.html) | 12/22 |
| allarms 3 | 3 | max tc04 temperature | [네트워크 1981](networks/network-1981.html) | 21/43 |

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| TC05-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| TC05-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| TC05-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| TC05-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| TC05-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| TC05-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| TC05-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| TC05-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| TC05-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## TC06 · 온도 계측

AB01 출구 온도.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 78 / PDF 79.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW278 | tc06 | int | temperature control outputab-01 | 1543 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| I_TC_06 | DB13,INT42 | PLC | 00064 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| analog input conversion | 12 | tc-06 | [네트워크 1742](networks/network-1742.html) | 2/9 |

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| TC06-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| TC06-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| TC06-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| TC06-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| TC06-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| TC06-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| TC06-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| TC06-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| TC06-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## TC07 · 온도 계측

유입 가스 온도. 도면 SPARE 표기 확인.

자료 상태: 예비·운영 상태 확인. 상위: 해당 없음. 전기: FG 78 / PDF 79.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW280 | tc07 | int | temperature control inputsmoke | 1542 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| I_TC_07 | DB13,INT44 | PLC | 00052 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| analog input conversion | 13 | tc-07 | [네트워크 1743](networks/network-1743.html) | 2/9 |

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| TC07-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| TC07-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| TC07-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| TC07-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| TC07-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| TC07-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| TC07-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| TC07-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| TC07-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## TC09 · 온도 계측

백 필터 유입 온도.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 171 / PDF 172.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW386 | tc09 | int | temperature bf-01 | 1555 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| analog input conversion | 3 | tc-09 | [네트워크 1733](networks/network-1733.html) | 2/9 |
| burner control | 3 | a 56.3 max.temperaturefilter | [네트워크 1856](networks/network-1856.html) | 4/8 |
| burner control | 4 | start gas test | [네트워크 1857](networks/network-1857.html) | 12/23 |
| burner control | 5 | burner stop | [네트워크 1858](networks/network-1858.html) | 21/40 |
| filter | 22 | valve air false pv-14 | [네트워크 1903](networks/network-1903.html) | 10/18 |
| motors 1 | 2 | block load | [네트워크 1931](networks/network-1931.html) | 11/21 |
| motors 1 | 36 | fn04 | [네트워크 1965](networks/network-1965.html) | 10/19 |
| allarms 3 | 13 | tc-09 filter inlet temperature | [네트워크 1991](networks/network-1991.html) | 20/43 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1991 | SCoil | Open false air | (ON AND [Data.TC_09 > Data.TC09_MAX]) | 조건 성립 시 Set |
| 1991 | SCoil | Allarm.MAX_TC09 | (Add UID 1053.eno (블록 동작 확인) AND [Data.TC_09 > app07]) | 조건 성립 시 Set |
| 1991 | RCoil | Allarm.MAX_TC09 | ((Sub UID 1064.eno (블록 동작 확인) AND [Data.TC_09 < app03]) AND Allarm.MAX_TC09) | 조건 성립 시 Reset |
| 1991 | SCoil | Flag.STOP_HORN | ((Sub UID 1064.eno (블록 동작 확인) AND [Data.TC_09 < app03]) AND Allarm.MAX_TC09) | 조건 성립 시 Set |
| 1991 | RCoil | Open false air | (Sub UID 1064.eno (블록 동작 확인) AND [Data.TC_09 < app03]) | 조건 성립 시 Reset |
| 1991 | SCoil | Allarm.MAX_MAX_TC09 | ((ON AND [Data.TC_09 > Data.TC09_MAX_MAX]) OR (ON AND [Data.TC_09 > 200]) OR (ON AND [Data.TC_09 < -60])) | 조건 성립 시 Set |
| 1991 | RCoil | Allarm.MAX_MAX_TC09 | ((ON AND Flag.RESET_ALLARM) AND Allarm.MAX_MAX_TC09) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| TC09-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| TC09-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| TC09-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| TC09-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| TC09-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| TC09-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| TC09-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| TC09-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## TC10 · 온도 계측

백업에 예비 온도 입력으로 남아 있는 채널.

자료 상태: 예비·운영 상태 확인. 상위: 해당 없음. 전기: FG 171 / PDF 172.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW390 | tc-10 | int | spare temperature | 1554 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| analog input conversion | 4 | tc-10 | [네트워크 1734](networks/network-1734.html) | 2/9 |

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| TC10-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| TC10-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| TC10-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| TC10-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| TC10-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| TC10-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| TC10-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| TC10-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## TC11 · 온도 계측

P&ID ER01 계통의 로컬 온도 표시. PLC 대응은 식별되지 않았다.

자료 상태: P&ID 로컬 계측. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| TC11-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| TC11-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| TC11-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| TC11-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| TC11-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| TC11-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| TC11-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## RO01 · 산소 분석 채널

연소·순환 가스 산소 분석. 데이터 변환과 대체값/시험 조건을 함께 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 80 / PDF 81.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M40.1 | ro01 close | bool |  | 88 |
| %M40.0 | ro01 open | bool |  | 89 |
| %M41.3 | ro01_close | bool |  | 90 |
| %M41.2 | ro01_open | bool |  | 91 |
| %IW352 | r001 | int | oxigen control | 1537 |
| %M80.1 | ro01-ro02control disable | bool |  | 1572 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| I_RO_01 | DB13,INT68 | PLC | 0002E |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| valve control loop | 7 | mv05 controlled by ro-01 | [네트워크 1708](networks/network-1708.html) | 34/60 |
| analog input conversion | 18 | r0-01 | [네트워크 1748](networks/network-1748.html) | 2/9 |
| burner control | 5 | burner stop | [네트워크 1858](networks/network-1858.html) | 21/40 |
| burner control | 15 | enable burner cleaning sequence | [네트워크 1868](networks/network-1868.html) | 71/151 |
| allarms 3 | 4 | oxigen analyzer out of range | [네트워크 1982](networks/network-1982.html) | 11/23 |
| allarms 3 | 5 | oxigen too high | [네트워크 1983](networks/network-1983.html) | 10/22 |
| allarms 3 | 6 | ro01 oxigen low limit | [네트워크 1984](networks/network-1984.html) | 12/26 |
| allarms 3 | 7 | ro01-ro02 signal compare fault | [네트워크 1985](networks/network-1985.html) | 13/28 |
| cyc_int5 ogni 100ms | 2 | controll ro01 moduling mv05 - pid | [네트워크 5](networks/network-5.html) | 8/35 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1708 | RCoil | Flag.M_MV05_OPEN | (((NOT [ORef UID 24] AND NOT [ON]) AND NOT [Inputs.MV05 open]) OR ((NOT [ORef UID 24] AND NOT [ON]) AND Flag.M_MV05_CLOSE) OR ((NOT [ORef UID 24] AND NOT [ON]) AND Flag.MV05_Auto)) | 조건 성립 시 Reset |
| 1708 | RCoil | Flag.M_MV05_CLOSE | (((NOT [ORef UID 24] AND NOT [ON]) AND NOT [Inputs.MV05 Close]) OR ((NOT [ORef UID 24] AND NOT [ON]) AND Flag.M_MV05_OPEN) OR ((NOT [ORef UID 24] AND NOT [ON]) AND Flag.MV05_Auto)) | 조건 성립 시 Reset |
| 1708 | Coil | Open MV05 | ((((((((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Flag.MV05_Auto) AND PID UP MV05) OR (((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Flag.M_MV05_OPEN) AND MV WORK PULSE)) AND NOT [Allarm.Oxigen_Fault]) OR (((((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Flag.MV05_Auto) AND PID UP MV05) OR (((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Flag.M_MV05_OPEN) AND MV WORK PULSE)) AND UNDER TESTING)) AND NOT [Close MV05]) AND Inputs.MV05 open) | 조건에 따른 Coil 기록 |
| 1708 | Coil | Close MV05 | ((((((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Flag.MV05_Auto) AND PID DOWN MV05) OR (((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Flag.M_MV05_CLOSE) AND MV WORK PULSE) OR (((NOT [ORef UID 24] AND NOT [Allarm.MV_05_FAULT]) AND Allarm.Oxigen_Fault) AND NOT [UNDER TESTING])) AND NOT [Open MV05]) AND Inputs.MV05 Close) | 조건에 따른 Coil 기록 |
| 1984 | SdCoil | Tag_106 | ((OFF AND [Manage_TC1_2.PID_Ref_Temp > 650.0]) AND [Data.Oxigen_RO01 <= 5]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1M |
| 1984 | SCoil | Allarm.Oxigen_LOW | (((OFF AND [Manage_TC1_2.PID_Ref_Temp > 650.0]) AND [Data.Oxigen_RO01 <= 5]) AND Tag_106) | 조건 성립 시 Set |
| 1984 | RCoil | Allarm.Oxigen_LOW | ((((OFF AND Flag.RESET_ALLARM) AND Allarm.Oxigen_LOW) AND [Data.Oxigen_RO01 >= 20]) OR (((OFF AND Flag.RESET_ALLARM) AND Allarm.Oxigen_LOW) AND [Manage_TC1_2.PID_Ref_Temp <= 650.0])) | 조건 성립 시 Reset |
| 1985 | SdCoil | Tag_107 | ((((ON AND NOT [RO01-RO02control disable]) AND [Manage_TC1_2.PID_Ref_Temp > 650.0]) AND [app01 < -20]) OR (((ON AND NOT [RO01-RO02control disable]) AND [Manage_TC1_2.PID_Ref_Temp > 650.0]) AND [app01 > 20])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1M |
| 1985 | SCoil | Allarm.RO01_Signal_Fault | (((((ON AND NOT [RO01-RO02control disable]) AND [Manage_TC1_2.PID_Ref_Temp > 650.0]) AND [app01 < -20]) OR (((ON AND NOT [RO01-RO02control disable]) AND [Manage_TC1_2.PID_Ref_Temp > 650.0]) AND [app01 > 20])) AND Tag_107) | 조건 성립 시 Set |
| 1985 | RCoil | Allarm.RO01_Signal_Fault | ((ON AND Flag.RESET_ALLARM) AND Allarm.RO01_Signal_Fault) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| RO01-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| RO01-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| RO01-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| RO01-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| RO01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| RO01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| RO01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| RO01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| RO01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## RO02 · 산소 분석 채널

연소·순환 가스 산소 분석. 데이터 변환과 대체값/시험 조건을 함께 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 80 / PDF 81.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW354 | r002 | int | oxigen control | 1536 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| I_RO_02 | DB13,INT70 | PLC | 0002F |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| analog input conversion | 19 | r0-02 | [네트워크 1749](networks/network-1749.html) | 2/9 |
| analog input conversion | 20 | r0-03 | [네트워크 1750](networks/network-1750.html) | 4/14 |
| allarms 3 | 7 | ro01-ro02 signal compare fault | [네트워크 1985](networks/network-1985.html) | 13/28 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1985 | SdCoil | Tag_107 | ((((ON AND NOT [RO01-RO02control disable]) AND [Manage_TC1_2.PID_Ref_Temp > 650.0]) AND [app01 < -20]) OR (((ON AND NOT [RO01-RO02control disable]) AND [Manage_TC1_2.PID_Ref_Temp > 650.0]) AND [app01 > 20])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1M |
| 1985 | SCoil | Allarm.RO01_Signal_Fault | (((((ON AND NOT [RO01-RO02control disable]) AND [Manage_TC1_2.PID_Ref_Temp > 650.0]) AND [app01 < -20]) OR (((ON AND NOT [RO01-RO02control disable]) AND [Manage_TC1_2.PID_Ref_Temp > 650.0]) AND [app01 > 20])) AND Tag_107) | 조건 성립 시 Set |
| 1985 | RCoil | Allarm.RO01_Signal_Fault | ((ON AND Flag.RESET_ALLARM) AND Allarm.RO01_Signal_Fault) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| RO02-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| RO02-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| RO02-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| RO02-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| RO02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| RO02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| RO02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| RO02-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| RO02-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## RO03 · 산소 분석 채널

연소·순환 가스 산소 분석. 데이터 변환과 대체값/시험 조건을 함께 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 81 / PDF 82.

확인할 특이점: Analog input conversion 원본에는 RO03 입력 외에도 RO02에 11을 더하는 대체 계산 참조가 존재한다. 어떤 분기가 실제 실행되는지 ON/OFF 값과 원본 연결 구조로 확인한다. 

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW356 | r003 | int | oxigen control | 1535 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| I_RO_03 | DB13,INT72 | PLC | 00032 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| analog input conversion | 20 | r0-03 | [네트워크 1750](networks/network-1750.html) | 4/14 |
| allarms 3 | 17 | ro03 | [네트워크 1995](networks/network-1995.html) | 13/27 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1995 | SCoil | Allarm.RO03_Min | LRef UID 31.Q (블록 동작 확인) | 조건 성립 시 Set |
| 1995 | SCoil | Allarm.RO03_Max | LRef UID 68.Q (블록 동작 확인) | 조건 성립 시 Set |
| 1995 | RCoil | Allarm.RO03_Min | (Flag.RESET_ALLARM AND Allarm.RO03_Min) | 조건 성립 시 Reset |
| 1995 | RCoil | Allarm.RO03_Max | (Flag.RESET_ALLARM AND Allarm.RO03_Max) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| RO03-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| RO03-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| RO03-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| RO03-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| RO03-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| RO03-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| RO03-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| RO03-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| RO03-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## RO04 · 산소 분석 채널

연소·순환 가스 산소 분석. 데이터 변환과 대체값/시험 조건을 함께 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 81 / PDF 82.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW358 | r004 | int | oxigen control | 1534 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| I_RO_04 | DB13,INT74 | PLC | 00033 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| analog input conversion | 21 | r0-04 | [네트워크 1751](networks/network-1751.html) | 2/9 |

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| RO04-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| RO04-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| RO04-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| RO04-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| RO04-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| RO04-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| RO04-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| RO04-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| RO04-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## PSH01 · 압력 측정 채널

P&ID의 압력 제어 위치와 관련 MV 제어 루프를 함께 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 75 / PDF 76.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW284 | psh01 | int | pressure control output mv-02 | 1540 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| Editor_PSH01 | DB26,INT16 | PLC | 00411 |
| I_PSH_01 | DB13,INT48 | PLC | 00054 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| valve control loop | 3 | mv02 controlled by psh-01 | [네트워크 1704](networks/network-1704.html) | 33/57 |
| analog input conversion | 15 | psh-01 | [네트워크 1745](networks/network-1745.html) | 2/9 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1704 | RCoil | Flag.M_MV02_OPEN | ((NOT [ON] AND NOT [Inputs.MV02 Open]) OR (NOT [ON] AND Flag.M_MV02_CLOSE) OR (NOT [ON] AND Flag.MV02_Auto)) | 조건 성립 시 Reset |
| 1704 | RCoil | Flag.M_MV02_CLOSE | ((NOT [ON] AND NOT [Inputs.MV02 Close]) OR (NOT [ON] AND Flag.M_MV02_OPEN) OR (NOT [ON] AND Flag.MV02_Auto)) | 조건 성립 시 Reset |
| 1704 | Coil | Open MV02 | ((((((((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.MV02_Auto) AND PID MV02 UP) OR ((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.M_MV02_OPEN)) AND MV WORK PULSE) OR (((((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.MV02_Auto) AND PID MV02 UP) OR ((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.M_MV02_OPEN)) AND ON)) AND NOT [Close MV02]) AND Inputs.MV02 Open) | 조건에 따른 Coil 기록 |
| 1704 | Coil | Close MV02 | ((((((((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.MV02_Auto) AND PID MV02 Down) OR ((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.M_MV02_CLOSE)) AND MV WORK PULSE) OR (((((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.MV02_Auto) AND PID MV02 Down) OR ((NOT [ON] AND NOT [Allarm.MV02_FAULT]) AND Flag.M_MV02_CLOSE)) AND ON)) AND NOT [Open MV02]) AND Inputs.MV02 Close) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| PSH01-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| PSH01-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| PSH01-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| PSH01-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| PSH01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| PSH01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| PSH01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| PSH01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| PSH01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## PSH02 · 압력 측정 채널

P&ID의 압력 제어 위치와 관련 MV 제어 루프를 함께 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 75 / PDF 76.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW286 | psh02 | int | pressure control output mv-03 | 1539 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| Editor_PSH02 | DB26,INT18 | PLC | 00410 |
| I_PSH_02 | DB13,INT50 | PLC | 00055 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| valve control loop | 8 | mv06 controlled by psh02 | [네트워크 1709](networks/network-1709.html) | 12/27 |
| valve control loop | 9 | the working tool has a low range | [네트워크 1710](networks/network-1710.html) | 20/39 |
| valve control loop | 10 | mv06 controlled by psh02 | [네트워크 1711](networks/network-1711.html) | 33/59 |
| analog input conversion | 16 | psh-02 | [네트워크 1746](networks/network-1746.html) | 2/9 |
| allarms 3 | 11 | max pressure psh-02 | [네트워크 1989](networks/network-1989.html) | 10/21 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1709 | SdCoil | Tag_150 | ((ON AND [Data.PSH02_SETPOINT != 0]) AND NOT [Tag_149]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#300MS |
| 1709 | SdCoil | Tag_149 | ((ON AND [Data.PSH02_SETPOINT != 0]) AND Tag_150) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#4S |
| 1709 | Coil | MV06 PID DOWN | (((ON AND [Data.PSH02_SETPOINT != 0]) AND NOT [Tag_150]) AND [ErrPSH02 >= 5]) | 조건에 따른 Coil 기록 |
| 1709 | Coil | MV06 PID UP | (((ON AND [Data.PSH02_SETPOINT != 0]) AND NOT [Tag_150]) AND [ErrPSH02 <= -5]) | 조건에 따른 Coil 기록 |
| 1711 | RCoil | Flag.MV06_Open | ((NOT [ON] AND Inputs.MV06_Open) OR (NOT [ON] AND Flag.MV06_Close) OR (NOT [ON] AND Flag.MV06_Auto)) | 조건 성립 시 Reset |
| 1711 | RCoil | Flag.MV06_Close | ((NOT [ON] AND Inputs.MV06 Close) OR (NOT [ON] AND Flag.MV06_Open) OR (NOT [ON] AND Flag.MV06_Auto)) | 조건 성립 시 Reset |
| 1711 | Coil | Open MV06 | ((((((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Auto) AND MV06 PID UP) OR (((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Auto) AND Shot to open) OR (((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Open) AND MV WORK PULSE) OR (((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Open) AND ON)) AND NOT [Close MV06]) AND NOT [Inputs.MV06_Open]) | 조건에 따른 Coil 기록 |
| 1711 | Coil | Close MV06 | ((((((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Auto) AND MV06 PID DOWN) OR (((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Auto) AND Shot to close) OR (((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Close) AND MV WORK PULSE) OR (((NOT [ON] AND NOT [Allarm.MV_06_FAULT]) AND Flag.MV06_Close) AND ON)) AND NOT [Open MV06]) AND NOT [Inputs.MV06 Close]) | 조건에 따른 Coil 기록 |
| 1989 | SdCoil | Tag_111 | (ON AND [Data.PSH_02 >= Data.PSH02_MAX_SETPOINT]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#3M |
| 1989 | SCoil | Allarm.MAX_PSH_02 | ((ON AND [Data.PSH_02 >= Data.PSH02_MAX_SETPOINT]) AND Tag_111) | 조건 성립 시 Set |
| 1989 | RCoil | Allarm.MAX_PSH_02 | ((ON AND Allarm.MAX_PSH_02) AND [Data.PSH_02 < app06]) | 조건 성립 시 Reset |
| 1989 | SCoil | Flag.STOP_HORN | ((ON AND Allarm.MAX_PSH_02) AND [Data.PSH_02 < app06]) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| PSH02-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| PSH02-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| PSH02-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| PSH02-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| PSH02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| PSH02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| PSH02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| PSH02-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| PSH02-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## PSH03 · 압력 측정 채널

P&ID의 압력 제어 위치와 관련 MV 제어 루프를 함께 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 75 / PDF 76.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW320 | psh03 | int | pressure control | 1538 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| I_PSH_03 | DB13,INT52 | PLC | 00056 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| valve control loop | 4 | mv03 controlled by psh03 | [네트워크 1705](networks/network-1705.html) | 11/24 |
| valve control loop | 5 | mv03 controlled by psh03 | [네트워크 1706](networks/network-1706.html) | 41/73 |
| analog input conversion | 17 | psh-03 | [네트워크 1747](networks/network-1747.html) | 2/9 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1705 | SdCoil | Tag_148 | (ON AND NOT [Tag_147]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#4S |
| 1705 | SdCoil | Tag_147 | (ON AND Tag_148) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#10S |
| 1705 | Coil | PID down MV03 | ((ON AND NOT [Tag_148]) AND [ErrPSH03 >= 5]) | 조건에 따른 Coil 기록 |
| 1705 | Coil | PID UP MV03 | ((ON AND NOT [Tag_148]) AND [ErrPSH03 < -5]) | 조건에 따른 Coil 기록 |
| 1706 | RCoil | Flag.M_MV03_OPEN | ((ON AND Inputs.MV03 open) OR (ON AND Flag.M_MV03_CLOSE) OR (ON AND Flag.MV03_Auto)) | 조건 성립 시 Reset |
| 1706 | RCoil | Flag.M_MV03_CLOSE | ((ON AND Inputs.MV03 Close) OR (ON AND Flag.M_MV03_OPEN) OR (ON AND Flag.MV03_Auto)) | 조건 성립 시 Reset |
| 1706 | RCoil | Close MV03 for Burner Startup | (ON AND Inputs.MV03 Close) | 조건 성립 시 Reset |
| 1706 | Coil | Start open MV03 | (((((((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.MV03_Auto) AND PID UP MV03) AND MV WORK PULSE) OR ((((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.MV03_Auto) AND PID UP MV03) AND ON) OR (((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.M_MV03_OPEN) AND MV WORK PULSE) OR (((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.M_MV03_OPEN) AND ON) OR ((ON AND NOT [Allarm.MV03_FAULT]) AND Open MV03 for washing)) AND NOT [HMI_DB.ResetEncoderProcedure_MV03]) AND NOT [Inputs.MV03 open]) | 조건에 따른 Coil 기록 |
| 1706 | Coil | Start Close MV03 | ((((((((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.MV03_Auto) AND PID down MV03) AND MV WORK PULSE) OR ((((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.MV03_Auto) AND PID down MV03) AND ON) OR (((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.M_MV03_CLOSE) AND MV WORK PULSE) OR (((ON AND NOT [Allarm.MV03_FAULT]) AND Flag.M_MV03_CLOSE) AND ON) OR ((ON AND NOT [Allarm.MV03_FAULT]) AND Close MV03 for Burner Startup)) AND NOT [Open MV03 for washing]) OR ((ON AND NOT [Allarm.MV03_FAULT]) AND HMI_DB.ResetEncoderProcedure_MV03)) AND NOT [Inputs.MV03 Close]) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| PSH03-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| PSH03-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| PSH03-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| PSH03-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| PSH03-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| PSH03-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| PSH03-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| PSH03-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| PSH03-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## PC01 · 집진 흡인 압력

PC01 4~20mA 입력과 FN04 압력 제어 경로.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 76 / PDF 77.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M40.2 | pc01 close | bool |  | 63 |
| %M40.3 | pc01 open | bool |  | 64 |
| %IW322 | pc01 | int | pressure control | 1521 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| I_PC_01 | DB13,INT54 | PLC | 00057 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| analog input conversion | 15 | psh-01 | [네트워크 1745](networks/network-1745.html) | 2/9 |
| analog input conversion | 45 | pc-01 | [네트워크 1775](networks/network-1775.html) | 2/9 |
| filter | 20 | dp-01 control loop | [네트워크 1901](networks/network-1901.html) | 11/30 |
| allarms 3 | 9 | pc-01 low depressure | [네트워크 1987](networks/network-1987.html) | 13/27 |
| cyc_int5 ogni 100ms | 4 | controll pc01 moduling mv02 | [네트워크 7](networks/network-7.html) | 5/30 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1987 | SdCoil | Tag_109 | ((((ON AND Inputs.FN01 Run) AND Inputs.FN04 Run) AND [Data.PC_01 > -10]) OR (((ON AND Inputs.FN01 Run) AND Inputs.FN04 Run) AND [Data.PC_01 > Data.Min_Pressure_PC_01]) OR (((ON AND Inputs.FN01 Run) AND Inputs.FN04 Run) AND [Data.PC_01 < -800])) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#30S |
| 1987 | SCoil | Allarm.Low_Aspiration | (((((ON AND Inputs.FN01 Run) AND Inputs.FN04 Run) AND [Data.PC_01 > -10]) OR (((ON AND Inputs.FN01 Run) AND Inputs.FN04 Run) AND [Data.PC_01 > Data.Min_Pressure_PC_01]) OR (((ON AND Inputs.FN01 Run) AND Inputs.FN04 Run) AND [Data.PC_01 < -800])) AND Tag_109) | 조건 성립 시 Set |
| 1987 | RCoil | Allarm.Low_Aspiration | ((((ON AND Inputs.FN01 Run) AND Inputs.FN04 Run) AND Flag.RESET_ALLARM) AND Allarm.Low_Aspiration) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| PC01-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| PC01-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| PC01-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| PC01-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| PC01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| PC01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| PC01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| PC01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| PC01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## PC02 · 소프트웨어 압력 루프 명칭

백업의 PC02 관련 데이터 명칭. PSH02와 물리 센서 동일성은 별도 검증한다.

자료 상태: 소프트웨어 명칭·물리 태그 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M40.4 | pc02 close | bool |  | 65 |
| %M40.5 | pc02 open | bool |  | 66 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| cyc_int5 ogni 100ms | 12 | control pc02 moduling mv03 - not used | [네트워크 15](networks/network-15.html) | 7/33 |

### 점검·진단 절차안

1. 논리 명칭 확인: 이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.
2. 데이터 추적: 원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| PC02-SIM-01 | 데이터 추적 | 원시값 및 선택 조건 변경 | 논리 명칭의 입력/출력 관계 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| PC02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| PC02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| PC02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## DP01 · 백 필터 차압

BF01의 차압 감시. 세정 허가·주기·경보 기준과 연결된다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 169 / PDF 170.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW398 | pr_bf01 | int | differential pressure switchbags filter bf-01(4-20ma) | 1523 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| analog input conversion | 43 | dp-01 | [네트워크 1773](networks/network-1773.html) | 2/9 |
| filter | 1 |  | [네트워크 1882](networks/network-1882.html) | 2/8 |
| filter | 2 | time work/pause by dp01 | [네트워크 1883](networks/network-1883.html) | 20/55 |
| filter | 5 | enabling sleeve washing | [네트워크 1886](networks/network-1886.html) | 15/29 |
| filter | 6 | work pause times for filter valves | [네트워크 1887](networks/network-1887.html) | 10/20 |
| filter | 20 | dp-01 control loop | [네트워크 1901](networks/network-1901.html) | 11/30 |
| allarms 3 | 14 | max filter depressure | [네트워크 1992](networks/network-1992.html) | 14/32 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1883 | Move | Data.LAVA_PAUSA | ((OFF AND [Data.Ev_filter_on < 51]) AND [Data.DP_01 < Coeff.DP_01_SOGLIA_1]) | Move 입력 Coeff.DP_01_PAUSA_SOGLIA_1 |
| 1883 | Move | Data.LAVA_LAVORO | Move UID 216.eno (블록 동작 확인) | Move 입력 Coeff.DP_01_LAVORO_SOGLIA_1 |
| 1883 | Move | Data.LAVA_PAUSA | (((OFF AND [Data.Ev_filter_on < 51]) AND [Data.DP_01 >= Coeff.DP_01_SOGLIA_1]) AND [Data.DP_01 < Coeff.DP_01_SOGLIA_2]) | Move 입력 Coeff.DP_01_PAUSA_SOGLIA_2 |
| 1883 | Move | Data.LAVA_LAVORO | Move UID 231.eno (블록 동작 확인) | Move 입력 Coeff.DP_01_LAVORO_SOGLIA_1 |
| 1883 | Move | Data.LAVA_PAUSA | (((OFF AND [Data.Ev_filter_on < 51]) AND [Data.DP_01 >= Coeff.DP_01_SOGLIA_2]) AND [Data.DP_01 < Coeff.DP_01_SOGLIA_3]) | Move 입력 Coeff.DP_01_PAUSA_SOGLIA_3 |
| 1883 | Move | Data.LAVA_LAVORO | Move UID 246.eno (블록 동작 확인) | Move 입력 Coeff.DP_01_LAVORO_SOGLIA_1 |
| 1883 | Move | Data.LAVA_PAUSA | (((OFF AND [Data.Ev_filter_on < 51]) AND [Data.DP_01 >= Coeff.DP_01_SOGLIA_3]) AND [Data.DP_01 < Coeff.DP_01_SOGLIA_4]) | Move 입력 Coeff.DP_01_PAUSA_SOGLIA_4 |
| 1883 | Move | Data.LAVA_LAVORO | Move UID 261.eno (블록 동작 확인) | Move 입력 Coeff.DP_01_LAVORO_SOGLIA_1 |
| 1883 | Move | Data.LAVA_PAUSA | ((OFF AND [Data.Ev_filter_on < 51]) AND [Data.DP_01 >= Coeff.DP_01_SOGLIA_4]) | Move 입력 Coeff.DP_01_PAUSA_SOGLIA_5 |
| 1883 | Move | Data.LAVA_LAVORO | Move UID 273.eno (블록 동작 확인) | Move 입력 Coeff.DP_01_LAVORO_SOGLIA_1 |
| 1901 | SdCoil | Tag_133 | (Flag.FN_04_AUTO AND NOT [Tag_133]) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#4S |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| DP01-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| DP01-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| DP01-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| DP01-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| DP01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| DP01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| DP01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| DP01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## DP02 · 백 필터 차압

BF02의 차압 감시. 세정 허가·주기·경보 기준과 연결된다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 169 / PDF 170.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW400 | pr_br02 | int | differential pressure switchbags filter bf-02(4-20ma) | 1522 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| analog input conversion | 44 | dp-02 | [네트워크 1774](networks/network-1774.html) | 2/9 |
| filter | 3 | time work/pause by dp02 | [네트워크 1884](networks/network-1884.html) | 20/55 |
| filter | 5 | enabling sleeve washing | [네트워크 1886](networks/network-1886.html) | 15/29 |
| allarms 3 | 14 | max filter depressure | [네트워크 1992](networks/network-1992.html) | 14/32 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1884 | Move | Data.LAVA_PAUSA | ((OFF AND [ORef UID 462 > 50]) AND [Data.DP_02 < Coeff.DP_02_SOGLIA_1]) | Move 입력 Coeff.DP_02_PAUSA_SOGLIA_1 |
| 1884 | Move | Data.LAVA_LAVORO | Move UID 398.eno (블록 동작 확인) | Move 입력 Coeff.DP_02_LAVORO_SOGLIA_1 |
| 1884 | Move | Data.LAVA_PAUSA | (((OFF AND [ORef UID 462 > 50]) AND [Data.DP_02 >= Coeff.DP_02_SOGLIA_1]) AND [Data.DP_02 < Coeff.DP_02_SOGLIA_2]) | Move 입력 Coeff.DP_02_PAUSA_SOGLIA_2 |
| 1884 | Move | Data.LAVA_LAVORO | Move UID 413.eno (블록 동작 확인) | Move 입력 Coeff.DP_02_LAVORO_SOGLIA_1 |
| 1884 | Move | Data.LAVA_PAUSA | (((OFF AND [ORef UID 462 > 50]) AND [Data.DP_02 >= Coeff.DP_02_SOGLIA_2]) AND [Data.DP_02 < Coeff.DP_02_SOGLIA_3]) | Move 입력 Coeff.DP_02_PAUSA_SOGLIA_3 |
| 1884 | Move | Data.LAVA_LAVORO | Move UID 428.eno (블록 동작 확인) | Move 입력 Coeff.DP_02_LAVORO_SOGLIA_1 |
| 1884 | Move | Data.LAVA_PAUSA | (((OFF AND [ORef UID 462 > 50]) AND [Data.DP_02 >= Coeff.DP_02_SOGLIA_3]) AND [Data.DP_02 < Coeff.DP_02_SOGLIA_4]) | Move 입력 Coeff.DP_02_PAUSA_SOGLIA_4 |
| 1884 | Move | Data.LAVA_LAVORO | Move UID 443.eno (블록 동작 확인) | Move 입력 Coeff.DP_02_LAVORO_SOGLIA_1 |
| 1884 | Move | Data.LAVA_PAUSA | ((OFF AND [ORef UID 462 > 50]) AND [Data.DP_02 >= Coeff.DP_02_SOGLIA_4]) | Move 입력 Coeff.DP_02_PAUSA_SOGLIA_5 |
| 1884 | Move | Data.LAVA_LAVORO | Move UID 455.eno (블록 동작 확인) | Move 입력 Coeff.DP_02_LAVORO_SOGLIA_1 |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| DP02-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| DP02-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| DP02-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| DP02-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| DP02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| DP02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| DP02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| DP02-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## ZT01 · FN01 진동 계측

FN01 진동 채널. 전기 회로 SPARE와 변환 네트워크 시험 조건을 확인한다.

자료 상태: SPARE·활성 조건 확인. 상위: 해당 없음. 전기: FG 82 / PDF 83.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %IW282 | zt01 | int | vibration trasmitter blower fn-01 | 1541 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| I_ZT_01 | DB13,INT46 | PLC | 00053 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| analog input conversion | 14 | zt-01 | [네트워크 1744](networks/network-1744.html) | 2/9 |
| motors 1 | 21 | preallarm fn01 | [네트워크 1950](networks/network-1950.html) | 12/22 |
| allarms 3 | 10 | high vibrations fn-01 | [네트워크 1988](networks/network-1988.html) | 10/21 |

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| ZT01-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| ZT01-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| ZT01-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| ZT01-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| ZT01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| ZT01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| ZT01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| ZT01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| ZT01-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## ZT02 · P&ID 밸브 위치 계측

P&ID MV01 위치 계측 태그. 현재 엔코더/TM 채널과 동일성은 확인 항목으로 남긴다.

자료 상태: P&ID·현재 엔코더 동일성 확인. 상위: MV01. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| ZT02-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| ZT02-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| ZT02-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| ZT02-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| ZT02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| ZT02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| ZT02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## ZT03 · P&ID 밸브 위치 계측

P&ID MV02 위치 계측 태그. 현재 엔코더/TM 채널과 동일성은 확인 항목으로 남긴다.

자료 상태: P&ID·현재 엔코더 동일성 확인. 상위: MV02. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| ZT03-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| ZT03-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| ZT03-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| ZT03-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| ZT03-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| ZT03-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| ZT03-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## ZT04 · P&ID 밸브 위치 계측

P&ID MV03 위치 계측 태그. 현재 엔코더/TM 채널과 동일성은 확인 항목으로 남긴다.

자료 상태: P&ID·현재 엔코더 동일성 확인. 상위: MV03. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| ZT04-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| ZT04-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| ZT04-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| ZT04-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| ZT04-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| ZT04-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| ZT04-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## ZT05 · P&ID 밸브 위치 계측

P&ID MV05 위치 계측 태그. 현재 엔코더/TM 채널과 동일성은 확인 항목으로 남긴다.

자료 상태: P&ID·현재 엔코더 동일성 확인. 상위: MV05. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| ZT05-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| ZT05-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| ZT05-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| ZT05-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| ZT05-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| ZT05-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| ZT05-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## ZT06 · P&ID 밸브 위치 계측

P&ID MV06 위치 계측 태그. 현재 엔코더/TM 채널과 동일성은 확인 항목으로 남긴다.

자료 상태: P&ID·현재 엔코더 동일성 확인. 상위: MV06. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| ZT06-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| ZT06-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| ZT06-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| ZT06-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| ZT06-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| ZT06-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| ZT06-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## LT01 · 석회 사일로 레벨

LD01 사일로의 P&ID 레벨 태그. PLC 저레벨 입력과 현장 센서 동일성을 확인한다.

자료 상태: 자료에서 확인. 상위: LD01. 전기: FG 170 / PDF 171.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I28.5 | ll_ld01 | bool |  | 947 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi inputs | 1 |  | [네트워크 1070](networks/network-1070.html) | 33/62 |
| allarms 2 | 3 | ld-01 low lime level | [네트워크 1228](networks/network-1228.html) | 8/16 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1228 | SCoil | Allarm.LD_01_MIN | LRef UID 21.Q (블록 동작 확인) | 조건 성립 시 Set |
| 1228 | RCoil | Allarm.LD_01_MIN | (((ON AND Flag.RESET_ALLARM) AND Allarm.LD_01_MIN) AND NOT [Inputs.LD-01 Minimo]) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LT01-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| LT01-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| LT01-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| LT01-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LT01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LT01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LT01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LT01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## SS01 · 이송 장치 감시 스위치

트립와이어·회전 또는 토크 감시의 실제 장치 종류와 접점 방향을 확인한다.

자료 상태: 자료에서 확인. 상위: BC01. 전기: FG 18 / PDF 19, FG 19 / PDF 20.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I6.2 | bc01_tripwire | bool | limit switch ss-01 | 952 |
| %I6.3 | bc01_prox | bool | limit switch ssl-01 | 973 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SS01-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| SS01-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| SS01-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| SS01-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SS01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SS01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SS01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SS01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## SS09 · 이송 장치 감시 스위치

트립와이어·회전 또는 토크 감시의 실제 장치 종류와 접점 방향을 확인한다.

자료 상태: 자료에서 확인. 상위: MC03. 전기: FG 23 / PDF 24.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I6.4 | mc03_torque | bool | limit switch ss-09 | 936 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SS09-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| SS09-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| SS09-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| SS09-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SS09-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SS09-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SS09-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SS09-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## SS10 · 이송 장치 감시 스위치

트립와이어·회전 또는 토크 감시의 실제 장치 종류와 접점 방향을 확인한다.

자료 상태: 자료에서 확인. 상위: MC04. 전기: FG 24 / PDF 25, FG 25 / PDF 26.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I6.5 | mc04_torque | bool | limit switch ss-10 | 1097 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SS10-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| SS10-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| SS10-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| SS10-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SS10-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SS10-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SS10-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SS10-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## SS11 · 이송 장치 감시 스위치

트립와이어·회전 또는 토크 감시의 실제 장치 종류와 접점 방향을 확인한다.

자료 상태: 자료에서 확인. 상위: MC05. 전기: FG 26 / PDF 27.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I6.6 | mc05_torque | bool | limit switch ss-11 | 937 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SS11-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| SS11-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| SS11-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| SS11-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SS11-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SS11-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SS11-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SS11-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## PSL05 · 압축공기 저압 스위치

공압 계통의 저압 입력. 게이트 구동 가능 여부와 알람을 대조한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 76 / PDF 77.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I11.0 | low pressure air | bool | e 41.4 psl-05 low airpressure switch | 945 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| simulation | 2 |  | [네트워크 1080](networks/network-1080.html) | 7/9 |
| allarms 2 | 2 | psl-04 low air pressure | [네트워크 1227](networks/network-1227.html) | 7/13 |

### 점검·진단 절차안

1. 측정 경로: 현장 센서 → 전원/퓨즈 → 전송기 → 아날로그/디지털 I → 환산 데이터 → HMI 주소를 대조한다.
2. 단위·범위: 도면의 센서 범위와 신호 종류, 원시값의 자료형, PLC 계수/영점, HMI 공학 단위를 각각 기록한다. 4~20mA라는 이유만으로 동일 환산식을 적용하지 않는다.
3. 값이 고정·비정상: 단선/초과 범위 비트, 시험 조건, OFF/ON 접점, 대체값·상수 Move, 선택된 PID 측정 채널을 원본에서 확인한다.
4. 알람·제어 경계: 경보/정지/복귀의 각 기준, 히스테리시스·지연시간·Reset 조건을 DB 설정값과 연결한다.
5. 교정 기록: 기준 계기와 여러 점의 측정값, 원시값·환산값·HMI값, 오차, 교정 전후 계수와 일시를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| PSL05-SIM-01 | 정상값 | 여러 원시값/스위치 상태 | 환산값·단위·HMI 대응 확인 | 설계·미실행 |
| PSL05-SIM-02 | 단선·범위 초과 | 최소·최대·이탈 원시값 | OFR/고장/대체값 처리 확인 | 설계·미실행 |
| PSL05-SIM-03 | 경보 경계 | 각 경계 앞/같음/뒤 값 | 비교기·지연·히스테리시스 확인 | 설계·미실행 |
| PSL05-SIM-04 | 시험/선택 조건 | 시험 입력과 선택 채널 변경 | 실제 입력과 대체값의 우선순위 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| PSL05-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| PSL05-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| PSL05-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| PSL05-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV01 · 공압 솔레노이드

상위 장치 요청·중간 릴레이·현장 코일을 연결해 점검한다.

자료 상태: 자료에서 확인. 상위: PV01. 전기: FG 69 / PDF 70.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I8.6 | ev01_open | bool | limit switch ls-01 gate "a" open | 662 |
| %I8.7 | ev01_close | bool | limit switch ls-02 gate "a" closed | 663 |
| %I9.2 | ev01_sel_open | bool | opening gate "a"local selector | 877 |
| %Q5.2 | pv-01 gate a | bool | a 57.0 ev-01 valvecommand | 1297 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| r1 scraps gate 2 | 4 | evr4 scraps discharge door and gates selector pv-01 | [네트워크 1914](networks/network-1914.html) | 5/9 |
| r1 scraps gate 2 | 11 | pv01 | [네트워크 1921](networks/network-1921.html) | 15/25 |

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV01-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV02 · 공압 솔레노이드

상위 장치 요청·중간 릴레이·현장 코일을 연결해 점검한다.

자료 상태: 자료에서 확인. 상위: PV01. 전기: FG 69 / PDF 70.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I9.0 | ev02_open | bool | limit switch ls-05 gate "b" open | 664 |
| %I9.1 | ev02_close | bool | limit switch ls-06 gate "b" closed | 665 |
| %I9.3 | ev02_sel_open | bool | opening gate "b"local selector | 878 |
| %Q5.3 | pv-01 gate b ev | bool | a 48.4 ev-02 valvecommand | 1296 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| r1 scraps gate 2 | 4 | evr4 scraps discharge door and gates selector pv-01 | [네트워크 1914](networks/network-1914.html) | 5/9 |
| r1 scraps gate 2 | 5 | a 48.4 ev-02 valvecommand | [네트워크 1915](networks/network-1915.html) | 12/21 |
| r1 scraps gate 2 | 12 | pv01 | [네트워크 1922](networks/network-1922.html) | 17/29 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1915 | Coil | PV-01 GATE B EV | ((ON AND Open EV B 00  PV-01) OR (ON AND Open EV B 01  PV-01) OR (ON AND maintenance PV01) OR (ON AND OFF)) | 조건에 따른 Coil 기록 |
| 1915 | Coil | PV-01 Gate a | ((ON AND Open EV A 00 PV-01) OR (ON AND Open EV A 01  PV-01) OR (ON AND maintenance PV01)) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV02-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV02-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV03 · 드럼 윤활 솔레노이드

상위 장치 요청·중간 릴레이·현장 코일을 연결해 점검한다.

자료 상태: 자료에서 확인. 상위: RD01. 전기: FG 20 / PDF 21.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q5.1 | ev03 | bool | a 53.1 ev-03 valvecommand | 901 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| EV_03\LS_Close | DB11,X86.1 | PLC | 00454 |
| EV_03\LS_Open | DB11,X86.0 | PLC | 00453 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi | 43 | ev03 | [네트워크 1220](networks/network-1220.html) | 4/7 |
| motors 1 | 8 |  | [네트워크 1937](networks/network-1937.html) | 2/8 |
| motors 1 | 9 | rd01 | [네트워크 1938](networks/network-1938.html) | 9/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1220 | Coil | ORef UID 28 | EV03 | 조건에 따른 Coil 기록 |
| 1220 | Coil | ORef UID 32 | NOT [EV03] | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV03-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV03-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV03-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV03-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV03-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| EV03-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## EV04 · 공압 솔레노이드

상위 장치 요청·중간 릴레이·현장 코일을 연결해 점검한다.

자료 상태: 자료에서 확인. 상위: PV02. 전기: FG 71 / PDF 72.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I9.5 | ev04_close | bool | e29.7 limit switch ls-26gate "a" closed | 666 |
| %I9.4 | ev04_open | bool | e29.6 limit switch ls-25gate "a" open | 1166 |
| %Q5.4 | pv-02 gate a ev | bool | a 53.7 ev-04 valvecommand | 1295 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| r1 scraps gate 2 | 13 | pv02 | [네트워크 1923](networks/network-1923.html) | 15/25 |

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV04-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV04-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV04-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV04-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV04-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV05 · 공압 솔레노이드

상위 장치 요청·중간 릴레이·현장 코일을 연결해 점검한다.

자료 상태: 자료에서 확인. 상위: PV02. 전기: FG 71 / PDF 72.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I9.7 | ev05_close | bool | e29.3 limit switch ls-30gate "b" closed | 667 |
| %I9.6 | ev05_open | bool | e29.2 limit switch ls-29gate "b" open | 1167 |
| %Q5.5 | pv-02 gate b ev | bool | a 56.4 ev-05 valvecommand | 1294 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| r1 scraps gate 2 | 10 | a 56.4 ev-05 valvecommand | [네트워크 1920](networks/network-1920.html) | 11/19 |
| r1 scraps gate 2 | 14 | pv02 | [네트워크 1924](networks/network-1924.html) | 15/25 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1920 | Coil | PV-02 GATE B EV | ((ON AND Open EV B 00  PV-02) OR (ON AND Open EV B 01  PV-02) OR (ON AND maintenance PV02)) | 조건에 따른 Coil 기록 |
| 1920 | Coil | PV-02 GATE A EV | ((ON AND Open EV A 00 PV-02) OR (ON AND Open EV A 01  PV-02) OR (ON AND maintenance PV02)) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV05-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV05-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV05-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV05-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV05-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV06 · 공압 솔레노이드

상위 장치 요청·중간 릴레이·현장 코일을 연결해 점검한다.

자료 상태: 자료에서 확인. 상위: PV03. 전기: FG 73 / PDF 74.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q5.6 | pv-03 gate ev | bool | a 56.5 ev-06 valvecommand | 1293 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV06-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV06-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV06-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV06-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV06-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV07 · 공압 솔레노이드

상위 장치 요청·중간 릴레이·현장 코일을 연결해 점검한다.

자료 상태: 자료에서 확인. 상위: PV04. 전기: FG 74 / PDF 75.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q5.7 | pv-04 | bool | a 57.1 ev-07 valvecommand | 988 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV07-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV07-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV07-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV07-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV07-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV11 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 154 / PDF 155.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q12.0 | ev-11 | bool | a0.0 filter 1 valve bf01first sector | 791 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 10 | a0.0 filter 1 valve bf01first sector | [네트워크 1891](networks/network-1891.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1891 | Coil | EV-11 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 11]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV11-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV11-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV11-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV11-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV11-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV12 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 154 / PDF 155.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q12.1 | ev-12 | bool | a0.1 filter 2 valve bf01first sector | 792 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 10 | a0.0 filter 1 valve bf01first sector | [네트워크 1891](networks/network-1891.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1891 | Coil | EV-12 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 13]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV12-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV12-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV12-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV12-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV12-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV13 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 154 / PDF 155.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q12.2 | ev-13 | bool | a0.2 filter 3 valve bf01first sector | 793 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 10 | a0.0 filter 1 valve bf01first sector | [네트워크 1891](networks/network-1891.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1891 | Coil | EV-13 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 15]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV13-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV13-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV13-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV13-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV13-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV14 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 155 / PDF 156.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q12.3 | ev-14 | bool | a0.3 filter 4 valve bf01first sector | 794 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 10 | a0.0 filter 1 valve bf01first sector | [네트워크 1891](networks/network-1891.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1891 | Coil | EV-14 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 17]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV14-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV14-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV14-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV14-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV14-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV15 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 155 / PDF 156.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q12.4 | ev-15 | bool | a0.4 filter 5 valve bf01first sector | 795 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 10 | a0.0 filter 1 valve bf01first sector | [네트워크 1891](networks/network-1891.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1891 | Coil | EV-15 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 19]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV15-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV15-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV15-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV15-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV15-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV16 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 155 / PDF 156.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q12.5 | ev-16 | bool | a0.5 filter 6 valve bf01first sector | 796 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 11 | wash filter | [네트워크 1892](networks/network-1892.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1892 | Coil | EV-16 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 21]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV16-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV16-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV16-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV16-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV16-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV17 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 156 / PDF 157.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q12.6 | ev-17 | bool | a0.6 filter 7 valve bf01first sector | 797 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 11 | wash filter | [네트워크 1892](networks/network-1892.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1892 | Coil | EV-17 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 23]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV17-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV17-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV17-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV17-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV17-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV18 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 156 / PDF 157.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q12.7 | ev-18 | bool | a0.7 filter 8 valve bf01first sector | 798 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 11 | wash filter | [네트워크 1892](networks/network-1892.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1892 | Coil | EV-18 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 25]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV18-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV18-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV18-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV18-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV18-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV19 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 156 / PDF 157.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q13.0 | ev-19 | bool | a1.0 filter 1 valve bf01second sector | 799 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 11 | wash filter | [네트워크 1892](networks/network-1892.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1892 | Coil | EV-19 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 27]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV19-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV19-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV19-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV19-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV19-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV20 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 157 / PDF 158.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q13.1 | ev-20 | bool | a1.1 filter 2 valve bf01second sector | 800 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 11 | wash filter | [네트워크 1892](networks/network-1892.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1892 | Coil | EV-20 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 29]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV20-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV20-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV20-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV20-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV20-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV21 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 157 / PDF 158.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q13.2 | ev-21 | bool | a1.2 filter 3 valve bf01second sector | 801 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 12 | wash filter | [네트워크 1893](networks/network-1893.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1893 | Coil | EV-21 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 31]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV21-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV21-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV21-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV21-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV21-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV22 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 157 / PDF 158.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q13.3 | ev-22 | bool | a1.3 filter 4 valve bf01second sector | 802 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 12 | wash filter | [네트워크 1893](networks/network-1893.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1893 | Coil | EV-22 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 33]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV22-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV22-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV22-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV22-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV22-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV23 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 158 / PDF 159.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q13.4 | ev-23 | bool | a1.4 filter 5 valve bf01second sector | 803 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 12 | wash filter | [네트워크 1893](networks/network-1893.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1893 | Coil | EV-23 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 35]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV23-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV23-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV23-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV23-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV23-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV24 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 158 / PDF 159.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q13.5 | ev-24 | bool | a1.5 filter 6 valve bf01second sector | 831 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 12 | wash filter | [네트워크 1893](networks/network-1893.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1893 | Coil | EV-24 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 37]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV24-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV24-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV24-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV24-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV24-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV25 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 158 / PDF 159.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q13.6 | ev-25 | bool | a1.6 filter 7 valve bf01second sector | 804 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 12 | wash filter | [네트워크 1893](networks/network-1893.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1893 | Coil | EV-25 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 39]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV25-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV25-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV25-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV25-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV25-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV26 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 159 / PDF 160.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q13.7 | ev-26 | bool | a1.7 filter 8 valve bf01second sector | 805 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 13 | wash filter | [네트워크 1894](networks/network-1894.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1894 | Coil | EV-26 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 41]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV26-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV26-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV26-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV26-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV26-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV27 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 159 / PDF 160.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q14.0 | ev-27 | bool | a2.0 filter 1 valve bf01third sector | 806 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 13 | wash filter | [네트워크 1894](networks/network-1894.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1894 | Coil | EV-27 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 43]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV27-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV27-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV27-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV27-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV27-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV28 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 159 / PDF 160.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q14.1 | ev-28 | bool | a2.1 filter 2 valve bf01third sector | 807 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 13 | wash filter | [네트워크 1894](networks/network-1894.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1894 | Coil | EV-28 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 45]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV28-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV28-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV28-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV28-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV28-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV29 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 160 / PDF 161.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q14.2 | ev-29 | bool | a2.2 filter 3 valve bf01third sector | 808 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 13 | wash filter | [네트워크 1894](networks/network-1894.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1894 | Coil | EV-29 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 47]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV29-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV29-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV29-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV29-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV29-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV30 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 160 / PDF 161.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q14.3 | ev-30 | bool | a2.3 filter 4 valve bf01third sector | 809 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 13 | wash filter | [네트워크 1894](networks/network-1894.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1894 | Coil | EV-30 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 49]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV30-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV30-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV30-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV30-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV30-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV31 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 160 / PDF 161.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q14.4 | ev-31 | bool | a2.4 filter 5 valve bf01third sector | 810 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 14 | wash filter | [네트워크 1895](networks/network-1895.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1895 | Coil | EV-31 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 51]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV31-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV31-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV31-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV31-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV31-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV32 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 161 / PDF 162.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q14.5 | ev-32 | bool | a2.5 filter 6 valve bf01third sector | 811 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 14 | wash filter | [네트워크 1895](networks/network-1895.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1895 | Coil | EV-32 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 53]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV32-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV32-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV32-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV32-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV32-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV33 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 161 / PDF 162.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q14.6 | ev-33 | bool | a2.6 filter 7 valve bf01third sector | 812 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 14 | wash filter | [네트워크 1895](networks/network-1895.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1895 | Coil | EV-33 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 55]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV33-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV33-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV33-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV33-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV33-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV34 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 161 / PDF 162.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q14.7 | ev-34 | bool | a2.7 filter 8 valve bf01third sector | 813 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 14 | wash filter | [네트워크 1895](networks/network-1895.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1895 | Coil | EV-34 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 57]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV34-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV34-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV34-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV34-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV34-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV35 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 162 / PDF 163.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q15.0 | ev-35 | bool | a3.0 filter 1 valve bf01fourth sector | 814 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 14 | wash filter | [네트워크 1895](networks/network-1895.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1895 | Coil | EV-35 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 59]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV35-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV35-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV35-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV35-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV35-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV36 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 162 / PDF 163.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q15.1 | ev-36 | bool | a3.1 filter 2 valve bf01fourth sector | 815 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 15 | wash filter | [네트워크 1896](networks/network-1896.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1896 | Coil | EV-36 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 61]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV36-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV36-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV36-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV36-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV36-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV37 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 162 / PDF 163.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q15.2 | ev-37 | bool | a3.2 filter 3 valve bf01fourth sector | 816 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 15 | wash filter | [네트워크 1896](networks/network-1896.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1896 | Coil | EV-37 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 63]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV37-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV37-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV37-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV37-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV37-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV38 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 163 / PDF 164.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q15.3 | ev-38 | bool | a3.3 filter 4 valve bf01fourth sector | 817 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 15 | wash filter | [네트워크 1896](networks/network-1896.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1896 | Coil | EV-38 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 65]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV38-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV38-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV38-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV38-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV38-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV39 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 163 / PDF 164.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q15.4 | ev-39 | bool | a3.4 filter 5 valve bf01fourth sector | 818 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 15 | wash filter | [네트워크 1896](networks/network-1896.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1896 | Coil | EV-39 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 67]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV39-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV39-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV39-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV39-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV39-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV40 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 163 / PDF 164.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q15.5 | ev-40 | bool | a3.5 filter 6 valve bf01fourth sector | 819 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 15 | wash filter | [네트워크 1896](networks/network-1896.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1896 | Coil | EV-40 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 69]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV40-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV40-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV40-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV40-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV40-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV41 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 164 / PDF 165.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q15.6 | ev-41 | bool | a3.6 filter 7 valve bf01fourth sector | 820 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 16 | wash filter | [네트워크 1897](networks/network-1897.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1897 | Coil | EV-41 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 71]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV41-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV41-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV41-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV41-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV41-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV42 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 164 / PDF 165.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q15.7 | ev-42 | bool | a3.7 filter 8 valve bf01fourth sector | 821 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 16 | wash filter | [네트워크 1897](networks/network-1897.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1897 | Coil | EV-42 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 73]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV42-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV42-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV42-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV42-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV42-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV43 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 164 / PDF 165.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q16.0 | ev-43 | bool | a4.0 filter 1 valve bf01fifth sector | 822 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 16 | wash filter | [네트워크 1897](networks/network-1897.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1897 | Coil | EV-43 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 75]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV43-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV43-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV43-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV43-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV43-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV44 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 165 / PDF 166.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q16.1 | ev-44 | bool | a4.1 filter 2 valve bf01fifth sector | 823 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 16 | wash filter | [네트워크 1897](networks/network-1897.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1897 | Coil | EV-44 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 77]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV44-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV44-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV44-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV44-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV44-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV45 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 165 / PDF 166.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q16.2 | ev-45 | bool | a4.2 filter 3 valve bf01fifth sector | 824 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 16 | wash filter | [네트워크 1897](networks/network-1897.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1897 | Coil | EV-45 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 79]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV45-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV45-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV45-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV45-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV45-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV46 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 165 / PDF 166.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q16.3 | ev-46 | bool | a4.3 filter 4 valve bf01fifth sector | 825 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 17 | wash filter | [네트워크 1898](networks/network-1898.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1898 | Coil | EV-46 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 81]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV46-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV46-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV46-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV46-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV46-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV47 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 166 / PDF 167.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q16.4 | ev-47 | bool | a4.4 filter 5 valve bf01fifth sector | 826 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 17 | wash filter | [네트워크 1898](networks/network-1898.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1898 | Coil | EV-47 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 83]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV47-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV47-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV47-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV47-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV47-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV48 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 166 / PDF 167.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q16.5 | ev-48 | bool | a4.5 filter 6 valve bf01fifth sector | 827 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 17 | wash filter | [네트워크 1898](networks/network-1898.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1898 | Coil | EV-48 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 85]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV48-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV48-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV48-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV48-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV48-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV49 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 166 / PDF 167.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q16.6 | ev-49 | bool | a4.6 filter 7 valve bf01fifth sector | 828 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 17 | wash filter | [네트워크 1898](networks/network-1898.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1898 | Coil | EV-49 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 87]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV49-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV49-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV49-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV49-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV49-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV50 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF01. 전기: FG 167 / PDF 168.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q16.7 | ev-50 | bool | a4.7 filter 8 valve bf01fifth sector | 829 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 17 | wash filter | [네트워크 1898](networks/network-1898.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1898 | Coil | EV-50 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 89]) AND Abilita_lavaggio_BF01) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV50-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV50-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV50-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV50-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV50-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV51 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 183 / PDF 186.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q18.0 | ev-51 | bool | a8.0 filter 1 valve bf02first sector | 890 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 10 | a0.0 filter 1 valve bf01first sector | [네트워크 1891](networks/network-1891.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1891 | Coil | EV-51 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 12]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV51-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV51-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV51-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV51-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV51-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV52 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 183 / PDF 186.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q18.1 | ev-52 | bool | a8.1 filter 2 valve bf02first sector | 891 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 10 | a0.0 filter 1 valve bf01first sector | [네트워크 1891](networks/network-1891.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1891 | Coil | EV-52 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 14]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV52-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV52-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV52-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV52-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV52-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV53 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 183 / PDF 186.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q18.2 | ev-53 | bool | a8.2 filter 3 valve bf02first sector | 892 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 10 | a0.0 filter 1 valve bf01first sector | [네트워크 1891](networks/network-1891.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1891 | Coil | EV-53 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 16]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV53-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV53-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV53-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV53-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV53-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV54 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 184 / PDF 187.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q18.3 | ev-54 | bool | a8.3 filter 4 valve bf02first sector | 893 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 10 | a0.0 filter 1 valve bf01first sector | [네트워크 1891](networks/network-1891.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1891 | Coil | EV-54 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 18]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV54-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV54-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV54-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV54-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV54-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV55 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 184 / PDF 187.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q18.4 | ev-55 | bool | a8.4 filter 5 valve bf02first sector | 894 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 10 | a0.0 filter 1 valve bf01first sector | [네트워크 1891](networks/network-1891.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1891 | Coil | EV-55 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 20]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV55-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV55-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV55-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV55-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV55-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV56 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 184 / PDF 187.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q18.5 | ev-56 | bool | a8.5 filter 6 valve bf02first sector | 895 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 11 | wash filter | [네트워크 1892](networks/network-1892.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1892 | Coil | EV-56 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 22]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV56-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV56-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV56-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV56-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV56-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV57 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 185 / PDF 188.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q18.6 | ev-57 | bool | a8.6 filter 7 valve bf02first sector | 841 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 11 | wash filter | [네트워크 1892](networks/network-1892.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1892 | Coil | EV-57 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 24]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV57-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV57-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV57-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV57-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV57-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV58 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 185 / PDF 188.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q18.7 | ev-58 | bool | a8.7 filter 8 valve bf02first sector | 842 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 11 | wash filter | [네트워크 1892](networks/network-1892.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1892 | Coil | EV-58 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 26]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV58-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV58-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV58-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV58-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV58-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV59 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 185 / PDF 188.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q19.0 | ev-59 | bool | a9.0 filter 1 valve bf02second sector | 843 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 11 | wash filter | [네트워크 1892](networks/network-1892.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1892 | Coil | EV-59 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 28]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV59-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV59-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV59-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV59-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV59-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV60 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 186 / PDF 189.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q19.1 | ev-60 | bool | a9.1 filter 2 valve bf02second sector | 844 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 11 | wash filter | [네트워크 1892](networks/network-1892.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1892 | Coil | EV-60 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 30]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV60-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV60-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV60-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV60-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV60-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV61 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 186 / PDF 189.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q19.2 | ev-61 | bool | a9.2 filter 3 valve bf02second sector | 904 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 12 | wash filter | [네트워크 1893](networks/network-1893.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1893 | Coil | EV-61 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 32]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV61-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV61-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV61-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV61-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV61-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV62 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 186 / PDF 189.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q19.3 | ev-62 | bool | a9.3 filter 4 valve bf02second sector | 845 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 12 | wash filter | [네트워크 1893](networks/network-1893.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1893 | Coil | EV-62 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 34]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV62-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV62-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV62-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV62-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV62-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV63 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 187 / PDF 190.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q19.4 | ev-63 | bool | a9.4 filter 5 valve bf02second sector | 846 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 12 | wash filter | [네트워크 1893](networks/network-1893.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1893 | Coil | EV-63 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 36]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV63-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV63-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV63-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV63-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV63-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV64 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 187 / PDF 190.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q19.5 | ev-64 | bool | a9.5 filter 6 valve bf02second sector | 847 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 12 | wash filter | [네트워크 1893](networks/network-1893.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1893 | Coil | EV-64 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 38]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV64-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV64-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV64-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV64-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV64-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV65 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 187 / PDF 190.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q19.6 | ev-65 | bool | a9.6 filter 7 valve bf02second sector | 848 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 12 | wash filter | [네트워크 1893](networks/network-1893.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1893 | Coil | EV-65 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 40]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV65-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV65-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV65-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV65-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV65-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV66 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 188 / PDF 191.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q19.7 | ev-66 | bool | a9.7 filter 8 valve bf02second sector | 849 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 13 | wash filter | [네트워크 1894](networks/network-1894.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1894 | Coil | EV-66 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 42]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV66-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV66-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV66-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV66-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV66-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV67 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 188 / PDF 191.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q20.0 | ev-67 | bool | a10.0 filter 1 valve bf02third sector | 850 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 13 | wash filter | [네트워크 1894](networks/network-1894.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1894 | Coil | EV-67 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 44]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV67-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV67-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV67-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV67-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV67-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV68 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 188 / PDF 191.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q20.1 | ev-68 | bool | a10.1 filter 2 valve bf02third sector | 851 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 13 | wash filter | [네트워크 1894](networks/network-1894.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1894 | Coil | EV-68 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 46]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV68-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV68-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV68-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV68-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV68-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV69 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 189 / PDF 192.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q20.2 | ev-69 | bool | a10.2 filter 3 valve bf02third sector | 852 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 13 | wash filter | [네트워크 1894](networks/network-1894.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1894 | Coil | EV-69 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 48]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV69-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV69-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV69-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV69-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV69-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV70 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 189 / PDF 192.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q20.3 | ev-70 | bool | a10.3 filter 4 valve bf02third sector | 853 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 13 | wash filter | [네트워크 1894](networks/network-1894.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1894 | Coil | EV-70 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 50]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV70-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV70-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV70-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV70-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV70-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV71 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 189 / PDF 192.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q20.4 | ev-71 | bool | a10.4 filter 5 valve bf02third sector | 854 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 14 | wash filter | [네트워크 1895](networks/network-1895.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1895 | Coil | EV-71 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 52]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV71-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV71-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV71-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV71-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV71-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV72 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 190 / PDF 193.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q20.5 | ev-72 | bool | a10.5 filter 6 valve bf02third sector | 855 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 14 | wash filter | [네트워크 1895](networks/network-1895.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1895 | Coil | EV-72 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 54]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV72-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV72-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV72-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV72-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV72-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV73 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 190 / PDF 193.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q20.6 | ev-73 | bool | a10.6 filter 7 valve bf02third sector | 856 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 14 | wash filter | [네트워크 1895](networks/network-1895.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1895 | Coil | EV-73 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 56]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV73-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV73-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV73-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV73-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV73-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV74 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 190 / PDF 193.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q20.7 | ev-74 | bool | a10.7 filter 8 valve bf02third sector | 857 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 14 | wash filter | [네트워크 1895](networks/network-1895.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1895 | Coil | EV-74 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 58]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV74-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV74-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV74-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV74-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV74-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV75 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 191 / PDF 194.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q21.0 | ev-75 | bool | a11.0 filter 1 valve bf02fourth sector | 858 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 14 | wash filter | [네트워크 1895](networks/network-1895.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1895 | Coil | EV-75 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 60]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV75-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV75-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV75-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV75-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV75-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV76 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 191 / PDF 194.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q21.1 | ev-76 | bool | a11.1 filter 2 valve bf02fourth sector | 859 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 15 | wash filter | [네트워크 1896](networks/network-1896.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1896 | Coil | EV-76 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 62]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV76-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV76-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV76-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV76-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV76-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV77 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 191 / PDF 194.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q21.2 | ev-77 | bool | a11.2 filter 3 valve bf02fourth sector | 860 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 15 | wash filter | [네트워크 1896](networks/network-1896.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1896 | Coil | EV-77 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 64]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV77-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV77-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV77-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV77-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV77-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV78 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 192 / PDF 195.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q21.3 | ev-78 | bool | a11.3 filter 4 valve bf02fourth sector | 861 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 15 | wash filter | [네트워크 1896](networks/network-1896.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1896 | Coil | EV-78 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 66]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV78-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV78-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV78-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV78-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV78-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV79 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 192 / PDF 195.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q21.4 | ev-79 | bool | a11.4 filter 5 valve bf02fourth sector | 862 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 15 | wash filter | [네트워크 1896](networks/network-1896.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1896 | Coil | EV-79 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 68]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV79-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV79-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV79-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV79-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV79-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV80 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 192 / PDF 195.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q21.5 | ev-80 | bool | a11.5 filter 6 valve bf02fourth sector | 863 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 15 | wash filter | [네트워크 1896](networks/network-1896.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1896 | Coil | EV-80 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 70]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV80-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV80-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV80-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV80-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV80-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV81 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 193 / PDF 196.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q21.6 | ev-81 | bool | a11.6 filter 7 valve bf02fourth sector | 864 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 16 | wash filter | [네트워크 1897](networks/network-1897.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1897 | Coil | EV-81 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 72]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV81-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV81-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV81-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV81-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV81-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV82 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 193 / PDF 196.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q21.7 | ev-82 | bool | a11.7 filter 8 valve bf02fourth sector | 865 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 16 | wash filter | [네트워크 1897](networks/network-1897.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1897 | Coil | EV-82 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 74]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV82-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV82-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV82-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV82-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV82-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV83 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 193 / PDF 196.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q22.0 | ev-83 | bool | a12.0 filter 1 valve bf02fifth sector | 866 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 16 | wash filter | [네트워크 1897](networks/network-1897.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1897 | Coil | EV-83 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 76]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV83-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV83-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV83-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV83-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV83-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV84 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 194 / PDF 197.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q22.1 | ev-84 | bool | a12.1 filter 2 valve bf02fifth sector | 867 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 16 | wash filter | [네트워크 1897](networks/network-1897.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1897 | Coil | EV-84 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 78]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV84-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV84-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV84-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV84-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV84-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV85 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 194 / PDF 197.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q22.2 | ev-85 | bool | a12.2 filter 3 valve bf02fifth sector | 868 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 16 | wash filter | [네트워크 1897](networks/network-1897.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1897 | Coil | EV-85 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 80]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV85-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV85-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV85-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV85-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV85-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV86 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 194 / PDF 197.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q22.3 | ev-86 | bool | a12.3 filter 4 valve bf02fifth sector | 905 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 17 | wash filter | [네트워크 1898](networks/network-1898.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1898 | Coil | EV-86 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 82]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV86-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV86-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV86-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV86-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV86-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV87 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 195 / PDF 198.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q22.4 | ev-87 | bool | a12.4 filter 5 valve bf02fifth sector | 869 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 17 | wash filter | [네트워크 1898](networks/network-1898.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1898 | Coil | EV-87 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 84]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV87-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV87-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV87-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV87-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV87-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV88 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 195 / PDF 198.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q22.5 | ev-88 | bool | a12.5 filter 6 valve bf02fifth sector | 870 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 17 | wash filter | [네트워크 1898](networks/network-1898.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1898 | Coil | EV-88 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 86]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV88-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV88-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV88-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV88-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV88-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV89 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 195 / PDF 198.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q22.6 | ev-89 | bool | a12.6 filter 7 valve bf02fifth sector | 871 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 17 | wash filter | [네트워크 1898](networks/network-1898.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1898 | Coil | EV-89 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 88]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV89-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV89-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV89-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV89-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV89-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## EV90 · 필터 펄스 세정 밸브

개별 세정 펄스 출력 채널. 순서 번호를 출력 주소와 별도로 기록한다.

자료 상태: 자료에서 확인. 상위: BF02. 전기: FG 196 / PDF 199.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %Q22.7 | ev-90 | bool | a12.7 filter 8 valve bf02fifth sector | 872 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| filter | 17 | wash filter | [네트워크 1898](networks/network-1898.html) | 32/65 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1898 | Coil | EV-90 | (((ON AND Tag_132) AND [Data.Ev_filter_on = 90]) AND Abilita_lavaggio_BF02) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 출력 식별: 아래 원본 심볼의 Q 주소와 전기 JB1/JB2 회로를 대조한다.
2. 순서 변수 식별: 관련 Filter 네트워크의 Eq 비교기 입력·상수 RefId·출력 코일 연결을 확인해 세정 순서 값을 확정한다.
3. 펄스 품질: 작동·휴지 시간, 코일 전원, 공기압, 밸브 응답 및 차압 변화를 기록한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| EV90-SIM-01 | 개별 펄스 | 해당 비교기 조건 주입 | 실제 Q 주소·펄스 폭·이웃 채널 오동작 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| EV90-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| EV90-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| EV90-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| EV90-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## CYL-CL01 · 공압 실린더

P&ID의 실린더. 독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검한다.

자료 상태: 자료에서 확인. 상위: PV01. 전기: 직접 회로 식별 근거 없음.

확인할 특이점:  외부 모터 CLIENT-CL01과 별개다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CYL-CL01-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CYL-CL01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CYL-CL01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CYL-CL01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CYL-CL01-V-04 | 불일치/특이점 | 외부 모터 CLIENT-CL01과 별개다. | 확인 대기 |

## CYL-CL02 · 공압 실린더

P&ID의 실린더. 독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검한다.

자료 상태: 자료에서 확인. 상위: PV01. 전기: 직접 회로 식별 근거 없음.

확인할 특이점:  외부 모터 CLIENT-CL02과 별개다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CYL-CL02-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CYL-CL02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CYL-CL02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CYL-CL02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CYL-CL02-V-04 | 불일치/특이점 | 외부 모터 CLIENT-CL02과 별개다. | 확인 대기 |

## CYL-CL03 · 공압 실린더

P&ID의 실린더. 독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검한다.

자료 상태: 자료에서 확인. 상위: PV01. 전기: 직접 회로 식별 근거 없음.

확인할 특이점:  외부 모터 CLIENT-CL03과 별개다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CYL-CL03-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CYL-CL03-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CYL-CL03-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CYL-CL03-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CYL-CL03-V-04 | 불일치/특이점 | 외부 모터 CLIENT-CL03과 별개다. | 확인 대기 |

## CYL-CL04 · 공압 실린더

P&ID의 실린더. 독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검한다.

자료 상태: 자료에서 확인. 상위: PV01. 전기: 직접 회로 식별 근거 없음.

확인할 특이점:  외부 모터 CLIENT-CL04과 별개다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CYL-CL04-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CYL-CL04-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CYL-CL04-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CYL-CL04-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CYL-CL04-V-04 | 불일치/특이점 | 외부 모터 CLIENT-CL04과 별개다. | 확인 대기 |

## CYL-CL05 · 공압 실린더

P&ID의 실린더. 독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검한다.

자료 상태: 자료에서 확인. 상위: PV02. 전기: 직접 회로 식별 근거 없음.

확인할 특이점:  외부 모터 CLIENT-CL05과 별개다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CYL-CL05-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CYL-CL05-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CYL-CL05-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CYL-CL05-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CYL-CL05-V-04 | 불일치/특이점 | 외부 모터 CLIENT-CL05과 별개다. | 확인 대기 |

## CYL-CL06 · 공압 실린더

P&ID의 실린더. 독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검한다.

자료 상태: 자료에서 확인. 상위: PV02. 전기: 직접 회로 식별 근거 없음.

확인할 특이점:  외부 모터 CLIENT-CL06과 별개다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CYL-CL06-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CYL-CL06-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CYL-CL06-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CYL-CL06-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CYL-CL06-V-04 | 불일치/특이점 | 외부 모터 CLIENT-CL06과 별개다. | 확인 대기 |

## CYL-CL07 · 공압 실린더

P&ID의 실린더. 독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검한다.

자료 상태: 자료에서 확인. 상위: PV02. 전기: 직접 회로 식별 근거 없음.

확인할 특이점:  외부 모터 CLIENT-CL07과 별개다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CYL-CL07-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CYL-CL07-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CYL-CL07-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CYL-CL07-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CYL-CL07-V-04 | 불일치/특이점 | 외부 모터 CLIENT-CL07과 별개다. | 확인 대기 |

## CYL-CL08 · 공압 실린더

P&ID의 실린더. 독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검한다.

자료 상태: 자료에서 확인. 상위: PV02. 전기: 직접 회로 식별 근거 없음.

확인할 특이점:  외부 모터 CLIENT-CL08과 별개다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CYL-CL08-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CYL-CL08-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CYL-CL08-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CYL-CL08-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CYL-CL08-V-04 | 불일치/특이점 | 외부 모터 CLIENT-CL08과 별개다. | 확인 대기 |

## CYL-CL09 · 공압 실린더

P&ID의 실린더. 독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검한다.

자료 상태: 자료에서 확인. 상위: PV03. 전기: 직접 회로 식별 근거 없음.

확인할 특이점:  외부 모터 CLIENT-CL09과 별개다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CYL-CL09-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CYL-CL09-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CYL-CL09-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CYL-CL09-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CYL-CL09-V-04 | 불일치/특이점 | 외부 모터 CLIENT-CL09과 별개다. | 확인 대기 |

## CYL-CL10 · 공압 실린더

P&ID의 실린더. 독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검한다.

자료 상태: 자료에서 확인. 상위: PV03. 전기: 직접 회로 식별 근거 없음.

확인할 특이점:  외부 모터 CLIENT-CL10과 별개다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CYL-CL10-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CYL-CL10-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CYL-CL10-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CYL-CL10-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CYL-CL10-V-04 | 불일치/특이점 | 외부 모터 CLIENT-CL10과 별개다. | 확인 대기 |

## CYL-CL11 · 공압 실린더

P&ID의 실린더. 독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검한다.

자료 상태: 자료에서 확인. 상위: PV04. 전기: 직접 회로 식별 근거 없음.

확인할 특이점:  외부 모터 CLIENT-CL11과 별개다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CYL-CL11-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CYL-CL11-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CYL-CL11-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CYL-CL11-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CYL-CL11-V-04 | 불일치/특이점 | 외부 모터 CLIENT-CL11과 별개다. | 확인 대기 |

## CYL-CL12 · 공압 실린더

P&ID의 실린더. 독립 PLC 출력으로 단정하지 않고 상위 밸브 구동 관계를 점검한다.

자료 상태: 자료에서 확인. 상위: PV14. 전기: 직접 회로 식별 근거 없음.

확인할 특이점:  외부 모터 CLIENT-CL12과 별개다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| CYL-CL12-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| CYL-CL12-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| CYL-CL12-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| CYL-CL12-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| CYL-CL12-V-04 | 불일치/특이점 | 외부 모터 CLIENT-CL12과 별개다. | 확인 대기 |

## LS01 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: PV01. 전기: FG 69 / PDF 70, FG 70 / PDF 71.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I8.6 | ev01_open | bool | limit switch ls-01 gate "a" open | 662 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS01-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS01-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS01-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS01-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS01-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS02 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: PV01. 전기: FG 69 / PDF 70, FG 70 / PDF 71.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I8.7 | ev01_close | bool | limit switch ls-02 gate "a" closed | 663 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| simulation | 12 | pv01 | [네트워크 1090](networks/network-1090.html) | 8/13 |
| hmi | 38 | pv01 | [네트워크 1215](networks/network-1215.html) | 1/21 |
| r1 scraps gate 2 | 11 | pv01 | [네트워크 1921](networks/network-1921.html) | 15/25 |

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS02-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS02-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS02-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS02-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS02-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS05 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: PV01. 전기: FG 69 / PDF 70, FG 70 / PDF 71.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I9.0 | ev02_open | bool | limit switch ls-05 gate "b" open | 664 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS05-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS05-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS05-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS05-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS05-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS06 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: PV01. 전기: FG 69 / PDF 70, FG 70 / PDF 71.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I9.1 | ev02_close | bool | limit switch ls-06 gate "b" closed | 665 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| simulation | 12 | pv01 | [네트워크 1090](networks/network-1090.html) | 8/13 |
| hmi | 38 | pv01 | [네트워크 1215](networks/network-1215.html) | 1/21 |
| r1 scraps gate 2 | 12 | pv01 | [네트워크 1922](networks/network-1922.html) | 17/29 |

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS06-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS06-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS06-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS06-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS06-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS09 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: PV03. 전기: FG 73 / PDF 74.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I10.2 | deviator open pv-03 | bool | e29.4 limit switchls-09 | 879 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS09-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS09-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS09-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS09-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS09-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS10 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: PV03. 전기: FG 73 / PDF 74.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I10.3 | deviator close pv-03 | bool | e29.5 limit switchls-10 | 880 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS10-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS10-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS10-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS10-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS10-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS15 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV05. 전기: FG 30 / PDF 31, FG 31 / PDF 32, FG 34 / PDF 35, FG 35 / PDF 36.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I7.1 | mv05_open | bool | limit switch ls-15 | 658 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS15-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS15-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS15-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS15-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS15-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS16 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV05. 전기: FG 30 / PDF 31, FG 31 / PDF 32, FG 34 / PDF 35, FG 35 / PDF 36.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I7.2 | mv05_close | bool | limit switch ls-16 | 1513 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS16-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS16-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS16-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS16-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS16-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS17 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV02. 전기: FG 30 / PDF 31, FG 31 / PDF 32, FG 36 / PDF 37, FG 37 / PDF 38.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I7.3 | mv02_open | bool | limit switch ls-17 | 659 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS17-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS17-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS17-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS17-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS17-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS18 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV02. 전기: FG 30 / PDF 31, FG 31 / PDF 32, FG 36 / PDF 37, FG 37 / PDF 38.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I7.4 | mv02_close | bool | limit switch ls-18 | 1514 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS18-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS18-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS18-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS18-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS18-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS19 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV03. 전기: FG 38 / PDF 39, FG 39 / PDF 40.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I7.5 | mv03_open | bool | limit switch ls-19 | 887 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS19-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS19-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS19-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS19-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS19-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS20 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV03. 전기: FG 38 / PDF 39, FG 39 / PDF 40.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I7.6 | mv03_close | bool | limit switch ls-20 | 888 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS20-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS20-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS20-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS20-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS20-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS21A · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV04. 전기: FG 40 / PDF 41, FG 41 / PDF 42.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I7.7 | mv04_open | bool | limit switch ls21a/ls21b | 940 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS21A-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS21A-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS21A-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS21A-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS21A-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS21B · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV04. 전기: FG 40 / PDF 41, FG 41 / PDF 42.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I7.7 | mv04_open | bool | limit switch ls21a/ls21b | 940 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS21B-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS21B-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS21B-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS21B-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS21B-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS22A · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV04. 전기: FG 40 / PDF 41, FG 41 / PDF 42.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I8.0 | mv04_close | bool | limit switch ls-22a/ls-22b | 941 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS22A-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS22A-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS22A-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS22A-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS22A-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS22B · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV04. 전기: FG 40 / PDF 41, FG 41 / PDF 42.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I8.0 | mv04_close | bool | limit switch ls-22a/ls-22b | 941 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS22B-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS22B-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS22B-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS22B-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS22B-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS23 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV01. 전기: FG 44 / PDF 45, FG 45 / PDF 46.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I8.1 | mv01_open | bool | limit switch ls-23 | 889 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS23-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS23-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS23-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS23-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS23-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS24 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV01. 전기: FG 44 / PDF 45, FG 45 / PDF 46.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I8.2 | mv01_close | bool | limit switch ls-24 | 1528 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS24-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS24-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS24-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS24-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS24-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS25 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: PV02. 전기: FG 71 / PDF 72, FG 72 / PDF 73.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I9.4 | ev04_open | bool | e29.6 limit switch ls-25gate "a" open | 1166 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS25-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS25-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS25-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS25-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS25-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS26 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: PV02. 전기: FG 71 / PDF 72, FG 72 / PDF 73.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I9.5 | ev04_close | bool | e29.7 limit switch ls-26gate "a" closed | 666 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS26-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS26-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS26-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS26-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS26-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS29 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: PV02. 전기: FG 71 / PDF 72, FG 72 / PDF 73.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I9.6 | ev05_open | bool | e29.2 limit switch ls-29gate "b" open | 1167 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS29-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS29-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS29-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS29-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS29-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS30 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: PV02. 전기: FG 71 / PDF 72, FG 72 / PDF 73.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I9.7 | ev05_close | bool | e29.3 limit switch ls-30gate "b" closed | 667 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS30-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS30-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS30-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS30-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS30-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS32 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: PV04. 전기: FG 74 / PDF 75.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I10.6 | pv04 close | bool | e36.6 limit switchls-32 | 944 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS32-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS32-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS32-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS32-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS32-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS33 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: PV04. 전기: FG 74 / PDF 75.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I10.5 | pv04 open | bool | e 45.0 pv 04 ls33 open | 943 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS33-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS33-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS33-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS33-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS33-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## LS34 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV06. 전기: FG 30 / PDF 31, FG 31 / PDF 32, FG 32 / PDF 33, FG 33 / PDF 34.

확인할 특이점:  MV06은 P&ID LS34/35와 백업 LS40/41 표기가 다르다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS34-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS34-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS34-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS34-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS34-V-04 | 불일치/특이점 | MV06은 P&ID LS34/35와 백업 LS40/41 표기가 다르다. | 확인 대기 |

## LS35 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV06. 전기: FG 30 / PDF 31, FG 31 / PDF 32, FG 32 / PDF 33, FG 33 / PDF 34.

확인할 특이점:  MV06은 P&ID LS34/35와 백업 LS40/41 표기가 다르다.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS35-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS35-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS35-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS35-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS35-V-04 | 불일치/특이점 | MV06은 P&ID LS34/35와 백업 LS40/41 표기가 다르다. | 확인 대기 |

## LS40 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV06. 전기: FG 30 / PDF 31, FG 31 / PDF 32, FG 32 / PDF 33, FG 33 / PDF 34.

확인할 특이점:  MV06은 P&ID LS34/35와 백업 LS40/41 표기가 다르다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I6.7 | mv06_open | bool | limit switch ls.40 | 657 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS40-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS40-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS40-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS40-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS40-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| LS40-V-05 | 불일치/특이점 | MV06은 P&ID LS34/35와 백업 LS40/41 표기가 다르다. | 확인 대기 |

## LS41 · 밸브 위치 리미트 스위치

개방/폐쇄 위치 센서. 번호·방향·단자·PLC 입력을 상위 장치와 대조한다.

자료 상태: P&ID/전기/백업 번호 대조. 상위: MV06. 전기: FG 30 / PDF 31, FG 31 / PDF 32, FG 32 / PDF 33, FG 33 / PDF 34.

확인할 특이점:  MV06은 P&ID LS34/35와 백업 LS40/41 표기가 다르다.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I7.0 | mv06_close | bool | limit switch ls-41 | 1527 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

직접 래더 참조 미식별. 로컬 계측/상위 제어 여부 확인.

### 점검·진단 절차안

1. 상위 장치 대조: 상위 설비 장의 운전·알람 조건을 먼저 확인하고 이 구성품의 물리 위치와 도면 번호를 대조한다.
2. 입출력 및 단자: 전원·중간 릴레이·센서·PLC 채널의 신호 방향과 단자를 한 경로씩 기록한다.
3. 상태 검증: 상위 설비의 정상 동작과 고장 상태에서 해당 구성품의 요청/피드백을 따로 수집한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| LS41-SIM-01 | 정상/고장 | 상위 요청과 구성품 응답 변경 | 독립 또는 공통 I/O 경로와 상위 조건 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| LS41-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| LS41-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| LS41-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| LS41-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| LS41-V-05 | 불일치/특이점 | MV06은 P&ID LS34/35와 백업 LS40/41 표기가 다르다. | 확인 대기 |

## SYS-POWER · 주전원·보조전원·제어반

주전원·110Vac·24Vdc·제어반 냉각과 서비스 릴레이를 관리한다. 표지 전압과 회로 제목의 차이를 확인한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 6 / PDF 7, FG 7 / PDF 8, FG 8 / PDF 9, FG 9 / PDF 10, FG 10 / PDF 11, FG 11 / PDF 12, FG 16 / PDF 17, FG 84 / PDF 85.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I19.5 | presence 110v | bool |  | 568 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| allarms 1 | 43 | presence 110v | [네트워크 1823](networks/network-1823.html) | 5/9 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1823 | SCoil | Allarm.110V_Fault | NOT [Inputs.Presenza_110V] | 조건 성립 시 Set |
| 1823 | RCoil | Allarm.110V_Fault | (Flag.RESET_ALLARM AND Allarm.110V_Fault) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 논리 명칭 확인: 이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.
2. 데이터 추적: 원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SYS-POWER-SIM-01 | 데이터 추적 | 원시값 및 선택 조건 변경 | 논리 명칭의 입력/출력 관계 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SYS-POWER-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SYS-POWER-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SYS-POWER-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SYS-POWER-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## SYS-SAFETY · 비상정지·일반 안전 회로

비상정지와 일반 허가, 온도 허가 회로의 물리·논리 경로를 검토한다. CPU 형식이나 일반 PLC 접점만으로 안전 인증을 판단하지 않는다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 12 / PDF 13, FG 13 / PDF 14, FG 14 / PDF 15, FG 15 / PDF 16, FG 99 / PDF 100, FG 236 / PDF 239.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I28.4 | 177t1_ok | bool |  | 946 |
| %Q6.6 | temperature interlock ok | bool | a 56.3 max.temperaturefilter | 1058 |
| %I19.4 | em_ok | bool |  | 1529 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| startup only | 2 | reset all flag start motors | [네트워크 402](networks/network-402.html) | 9/25 |
| startup only | 3 | reset all flag allarms | [네트워크 403](networks/network-403.html) | 10/27 |
| startup only | 4 | plants defaults | [네트워크 404](networks/network-404.html) | 10/14 |
| startup only | 5 | default | [네트워크 405](networks/network-405.html) | 6/8 |
| hmi inputs | 1 |  | [네트워크 1070](networks/network-1070.html) | 33/62 |
| simulation | 2 |  | [네트워크 1080](networks/network-1080.html) | 7/9 |
| main | 1 | simulation | [네트워크 1612](networks/network-1612.html) | 2/3 |
| main | 2 |  | [네트워크 1613](networks/network-1613.html) | 5/6 |
| main | 3 | word input | [네트워크 1614](networks/network-1614.html) | 4/12 |
| main | 4 |  | [네트워크 1615](networks/network-1615.html) | 3/9 |
| main | 5 | word output | [네트워크 1616](networks/network-1616.html) | 4/12 |
| main | 6 |  | [네트워크 1617](networks/network-1617.html) | 4/12 |
| main | 7 |  | [네트워크 1618](networks/network-1618.html) | 3/9 |
| main | 8 | analog conversion and allarms | [네트워크 1619](networks/network-1619.html) | 5/3 |
| main | 9 | motors valve and burner | [네트워크 1620](networks/network-1620.html) | 7/3 |
| main | 10 | motorized valve | [네트워크 1621](networks/network-1621.html) | 3/3 |
| main | 11 | allarm manager and siren | [네트워크 1622](networks/network-1622.html) | 2/3 |
| main | 12 | cpu clock | [네트워크 1623](networks/network-1623.html) | 3/7 |
| main | 13 | trasfering bit of maintenance | [네트워크 1624](networks/network-1624.html) | 3/7 |
| main | 15 | maintenance period limits | [네트워크 1626](networks/network-1626.html) | 4/8 |
| analog input conversion | 26 | reading encoder mv01 | [네트워크 1756](networks/network-1756.html) | 3/28 |
| analog input conversion | 27 | reading encoder mv02 | [네트워크 1757](networks/network-1757.html) | 3/28 |
| analog input conversion | 28 | reading encoder mv03 | [네트워크 1758](networks/network-1758.html) | 3/28 |
| analog input conversion | 29 | reading encoder mv05 | [네트워크 1759](networks/network-1759.html) | 3/28 |
| analog input conversion | 30 | reading encoder mv06 | [네트워크 1760](networks/network-1760.html) | 3/28 |
| analog input conversion | 31 | store current position value at power-off | [네트워크 1761](networks/network-1761.html) | 6/13 |
| analog input conversion | 32 | data management mv01 | [네트워크 1762](networks/network-1762.html) | 10/28 |
| analog input conversion | 33 | data management mv02 | [네트워크 1763](networks/network-1763.html) | 10/28 |
| analog input conversion | 34 | mv03 data management | [네트워크 1764](networks/network-1764.html) | 10/28 |
| analog input conversion | 35 | mv05 data management | [네트워크 1765](networks/network-1765.html) | 10/28 |
| analog input conversion | 36 | mv06 data management | [네트워크 1766](networks/network-1766.html) | 10/28 |
| allarms 1 | 44 | module emergenzy ok | [네트워크 1824](networks/network-1824.html) | 5/9 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 5 | set points fn01 | [네트워크 1845](networks/network-1845.html) | 24/63 |
| auto start motors | 6 | emergency stop | [네트워크 1846](networks/network-1846.html) | 4/11 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| burner control | 3 | a 56.3 max.temperaturefilter | [네트워크 1856](networks/network-1856.html) | 4/8 |
| filter | 22 | valve air false pv-14 | [네트워크 1903](networks/network-1903.html) | 10/18 |
| motors 1 | 42 | er01 | [네트워크 1971](networks/network-1971.html) | 10/18 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1846 | Move | Data.Tempo_presetting | PContact UID 21.out (블록 동작 확인) | Move 입력 0 |
| 1846 | Move | Data.Tipo_preset | Move UID 22.eno (블록 동작 확인) | Move 입력 5 |
| 1846 | SCoil | Flag.Auto_ON1 | Move UID 23.eno (블록 동작 확인) | 조건 성립 시 Set |


### 점검·진단 절차안

1. 논리 명칭 확인: 이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.
2. 데이터 추적: 원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SYS-SAFETY-SIM-01 | 데이터 추적 | 원시값 및 선택 조건 변경 | 논리 명칭의 입력/출력 관계 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SYS-SAFETY-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SYS-SAFETY-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SYS-SAFETY-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SYS-SAFETY-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |

## SYS-PLC-IO · CPU·분산 I/O·신호 변환

CPU·I/O 구성, 원시 입력/출력, 단위 환산, 엔코더/TM 및 진단 상태를 관리한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 102 / PDF 103, FG 103 / PDF 104, FG 104 / PDF 105, FG 105 / PDF 106, FG 106 / PDF 107, FG 107 / PDF 108, FG 108 / PDF 109, FG 109 / PDF 110, FG 110 / PDF 111, FG 111 / PDF 112, FG 112 / PDF 113, FG 113 / PDF 114, FG 114 / PDF 115, FG 115 / PDF 116, FG 116 / PDF 117, FG 117 / PDF 118, FG 118 / PDF 119, FG 119 / PDF 120, FG 120 / PDF 121, FG 121 / PDF 122, FG 122 / PDF 123, FG 123 / PDF 124, FG 124 / PDF 125, FG 125 / PDF 126, FG 126 / PDF 127, FG 127 / PDF 128, FG 128 / PDF 129, FG 129 / PDF 130, FG 130 / PDF 131, FG 131 / PDF 132, FG 132 / PDF 133, FG 133 / PDF 134, FG 134 / PDF 135, FG 135 / PDF 136, FG 136 / PDF 137, FG 137 / PDF 138, FG 138 / PDF 139, FG 139 / PDF 140, FG 140 / PDF 141, FG 141 / PDF 142, FG 142 / PDF 143, FG 143 / PDF 144, FG 144 / PDF 145, FG 145 / PDF 146, FG 146 / PDF 147, FG 147 / PDF 148, FG 148 / PDF 149, FG 149 / PDF 150, FG 153 / PDF 154, FG 182 / PDF 185.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi output | 1 |  | [네트워크 356](networks/network-356.html) | 12/33 |
| i/o_flt1 | 1 |  | [네트워크 434](networks/network-434.html) | 2/4 |
| mod_err | 1 |  | [네트워크 439](networks/network-439.html) | 2/4 |
| prog_err | 1 |  | [네트워크 444](networks/network-444.html) | 2/4 |
| rack_flt | 1 |  | [네트워크 765](networks/network-765.html) | 2/4 |
| hmi inputs | 1 |  | [네트워크 1070](networks/network-1070.html) | 33/62 |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| main | 1 | simulation | [네트워크 1612](networks/network-1612.html) | 2/3 |
| main | 2 |  | [네트워크 1613](networks/network-1613.html) | 5/6 |
| main | 3 | word input | [네트워크 1614](networks/network-1614.html) | 4/12 |
| main | 4 |  | [네트워크 1615](networks/network-1615.html) | 3/9 |
| main | 5 | word output | [네트워크 1616](networks/network-1616.html) | 4/12 |
| main | 6 |  | [네트워크 1617](networks/network-1617.html) | 4/12 |
| main | 7 |  | [네트워크 1618](networks/network-1618.html) | 3/9 |
| main | 8 | analog conversion and allarms | [네트워크 1619](networks/network-1619.html) | 5/3 |
| main | 9 | motors valve and burner | [네트워크 1620](networks/network-1620.html) | 7/3 |
| main | 10 | motorized valve | [네트워크 1621](networks/network-1621.html) | 3/3 |
| main | 11 | allarm manager and siren | [네트워크 1622](networks/network-1622.html) | 2/3 |
| main | 12 | cpu clock | [네트워크 1623](networks/network-1623.html) | 3/7 |
| main | 13 | trasfering bit of maintenance | [네트워크 1624](networks/network-1624.html) | 3/7 |
| main | 15 | maintenance period limits | [네트워크 1626](networks/network-1626.html) | 4/8 |
| signal linearization | 1 |  | [네트워크 1658](networks/network-1658.html) | 15/43 |
| signal linearization | 2 |  | [네트워크 1659](networks/network-1659.html) | 2/5 |
| analog output conversion | 1 | plant limits | [네트워크 1679](networks/network-1679.html) | 21/61 |
| analog output conversion | 2 | bwf01 client feeder | [네트워크 1680](networks/network-1680.html) | 5/13 |
| analog output conversion | 3 | bwf01 speed calculation | [네트워크 1681](networks/network-1681.html) | 13/39 |
| analog output conversion | 4 | bwf02 client feeder | [네트워크 1682](networks/network-1682.html) | 7/18 |
| analog output conversion | 5 | bwf02 speed calculation | [네트워크 1683](networks/network-1683.html) | 8/23 |
| analog output conversion | 6 | rd-01 cylinder | [네트워크 1684](networks/network-1684.html) | 6/16 |
| analog output conversion | 7 | fn-01 ventilator | [네트워크 1685](networks/network-1685.html) | 6/16 |
| analog output conversion | 8 | br01 burner | [네트워크 1686](networks/network-1686.html) | 8/20 |
| analog output conversion | 9 | br01 burner - gas | [네트워크 1687](networks/network-1687.html) | 8/21 |
| analog output conversion | 10 | fn02 ventilation of secondary air | [네트워크 1688](networks/network-1688.html) | 6/16 |
| analog output conversion | 11 | module aspirator fn-04 | [네트워크 1689](networks/network-1689.html) | 6/16 |
| analog output conversion | 12 | salt system | [네트워크 1690](networks/network-1690.html) | 5/12 |
| analog output conversion | 13 | send output to perifery | [네트워크 1691](networks/network-1691.html) | 4/11 |
| analog output conversion | 14 | bc01 | [네트워크 1692](networks/network-1692.html) | 6/16 |
| analog output conversion | 15 | mc04 | [네트워크 1693](networks/network-1693.html) | 6/16 |
| analog input conversion | 1 | tc04 | [네트워크 1731](networks/network-1731.html) | 2/9 |
| analog input conversion | 2 | tc-05 | [네트워크 1732](networks/network-1732.html) | 2/9 |
| analog input conversion | 3 | tc-09 | [네트워크 1733](networks/network-1733.html) | 2/9 |
| analog input conversion | 4 | tc-10 | [네트워크 1734](networks/network-1734.html) | 2/9 |
| analog input conversion | 5 | client 1 bwf01 flow rate | [네트워크 1735](networks/network-1735.html) | 9/26 |
| analog input conversion | 6 | client 2 bwf02 flow rate | [네트워크 1736](networks/network-1736.html) | 9/26 |
| analog input conversion | 7 | client 3 level indicator bwf01 | [네트워크 1737](networks/network-1737.html) | 2/9 |
| analog input conversion | 8 | client 4 level indicator bwf02 | [네트워크 1738](networks/network-1738.html) | 2/9 |
| analog input conversion | 9 | tc-01 | [네트워크 1739](networks/network-1739.html) | 2/9 |
| analog input conversion | 10 | tc-02 | [네트워크 1740](networks/network-1740.html) | 2/9 |
| analog input conversion | 11 | tc-03 | [네트워크 1741](networks/network-1741.html) | 2/9 |
| analog input conversion | 12 | tc-06 | [네트워크 1742](networks/network-1742.html) | 2/9 |
| analog input conversion | 13 | tc-07 | [네트워크 1743](networks/network-1743.html) | 2/9 |
| analog input conversion | 14 | zt-01 | [네트워크 1744](networks/network-1744.html) | 2/9 |
| analog input conversion | 15 | psh-01 | [네트워크 1745](networks/network-1745.html) | 2/9 |
| analog input conversion | 16 | psh-02 | [네트워크 1746](networks/network-1746.html) | 2/9 |
| analog input conversion | 17 | psh-03 | [네트워크 1747](networks/network-1747.html) | 2/9 |
| analog input conversion | 18 | r0-01 | [네트워크 1748](networks/network-1748.html) | 2/9 |
| analog input conversion | 19 | r0-02 | [네트워크 1749](networks/network-1749.html) | 2/9 |
| analog input conversion | 20 | r0-03 | [네트워크 1750](networks/network-1750.html) | 4/14 |
| analog input conversion | 21 | r0-04 | [네트워크 1751](networks/network-1751.html) | 2/9 |
| analog input conversion | 22 | gas br-01 - position | [네트워크 1752](networks/network-1752.html) | 2/9 |
| analog input conversion | 23 | air br-01 - position | [네트워크 1753](networks/network-1753.html) | 2/9 |
| analog input conversion | 24 | max flow gas - flowmeter | [네트워크 1754](networks/network-1754.html) | 4/14 |
| analog input conversion | 25 | max flow air - flowmeter | [네트워크 1755](networks/network-1755.html) | 2/9 |
| analog input conversion | 26 | reading encoder mv01 | [네트워크 1756](networks/network-1756.html) | 3/28 |
| analog input conversion | 27 | reading encoder mv02 | [네트워크 1757](networks/network-1757.html) | 3/28 |
| analog input conversion | 28 | reading encoder mv03 | [네트워크 1758](networks/network-1758.html) | 3/28 |
| analog input conversion | 29 | reading encoder mv05 | [네트워크 1759](networks/network-1759.html) | 3/28 |
| analog input conversion | 30 | reading encoder mv06 | [네트워크 1760](networks/network-1760.html) | 3/28 |
| analog input conversion | 31 | store current position value at power-off | [네트워크 1761](networks/network-1761.html) | 6/13 |
| analog input conversion | 32 | data management mv01 | [네트워크 1762](networks/network-1762.html) | 10/28 |
| analog input conversion | 33 | data management mv02 | [네트워크 1763](networks/network-1763.html) | 10/28 |
| analog input conversion | 34 | mv03 data management | [네트워크 1764](networks/network-1764.html) | 10/28 |
| analog input conversion | 35 | mv05 data management | [네트워크 1765](networks/network-1765.html) | 10/28 |
| analog input conversion | 36 | mv06 data management | [네트워크 1766](networks/network-1766.html) | 10/28 |
| analog input conversion | 37 | fn-02 fan | [네트워크 1767](networks/network-1767.html) | 2/9 |
| analog input conversion | 38 | bc-01 | [네트워크 1768](networks/network-1768.html) | 2/9 |
| analog input conversion | 39 | mc04 | [네트워크 1769](networks/network-1769.html) | 2/9 |
| analog input conversion | 40 | fn-02 aspirator | [네트워크 1770](networks/network-1770.html) | 2/9 |
| analog input conversion | 41 | rd-01 | [네트워크 1771](networks/network-1771.html) | 2/9 |
| analog input conversion | 42 | fn-01 | [네트워크 1772](networks/network-1772.html) | 2/9 |
| analog input conversion | 43 | dp-01 | [네트워크 1773](networks/network-1773.html) | 2/9 |
| analog input conversion | 44 | dp-02 | [네트워크 1774](networks/network-1774.html) | 2/9 |
| analog input conversion | 45 | pc-01 | [네트워크 1775](networks/network-1775.html) | 2/9 |
| analog input conversion | 46 | contactor ton passed in bwf | [네트워크 1776](networks/network-1776.html) | 7/17 |

### 점검·진단 절차안

1. 논리 명칭 확인: 이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.
2. 데이터 추적: 원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SYS-PLC-IO-SIM-01 | 데이터 추적 | 원시값 및 선택 조건 변경 | 논리 명칭의 입력/출력 관계 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SYS-PLC-IO-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SYS-PLC-IO-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SYS-PLC-IO-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## SYS-HMI · HMI·통신·가공 상태

기본 HMI의 화면·태그·PLC 주소·상태 가공과 운전 요청 경로를 관리한다. 전체 782개 설정 대장을 제공한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| hmi output | 1 |  | [네트워크 356](networks/network-356.html) | 12/33 |
| hmi inputs | 1 |  | [네트워크 1070](networks/network-1070.html) | 33/62 |
| hmi inputs | 2 | analog | [네트워크 1071](networks/network-1071.html) | 28/78 |
| hmi | 1 | bc01 | [네트워크 1178](networks/network-1178.html) | 1/9 |
| hmi | 2 | rd01 | [네트워크 1179](networks/network-1179.html) | 1/9 |
| hmi | 3 | rd01 fan | [네트워크 1180](networks/network-1180.html) | 1/9 |
| hmi | 4 | spare motor | [네트워크 1181](networks/network-1181.html) | 1/9 |
| hmi | 5 | mc04 | [네트워크 1182](networks/network-1182.html) | 1/9 |
| hmi | 7 | vs01 | [네트워크 1184](networks/network-1184.html) | 1/9 |
| hmi | 9 | auxiliary inverter | [네트워크 1186](networks/network-1186.html) | 3/12 |
| hmi | 10 | mv06 | [네트워크 1187](networks/network-1187.html) | 1/15 |
| hmi | 11 | mv05 | [네트워크 1188](networks/network-1188.html) | 1/15 |
| hmi | 12 | mv02 | [네트워크 1189](networks/network-1189.html) | 1/15 |
| hmi | 13 | mv01 | [네트워크 1190](networks/network-1190.html) | 1/15 |
| hmi | 14 | mv03 | [네트워크 1191](networks/network-1191.html) | 1/15 |
| hmi | 15 | fn02 | [네트워크 1192](networks/network-1192.html) | 1/9 |
| hmi | 16 | vr01 | [네트워크 1193](networks/network-1193.html) | 1/9 |
| hmi | 17 | fn01 | [네트워크 1194](networks/network-1194.html) | 1/9 |
| hmi | 18 | vr02 | [네트워크 1195](networks/network-1195.html) | 1/9 |
| hmi | 19 | ch01 | [네트워크 1196](networks/network-1196.html) | 1/9 |
| hmi | 20 | fn03 | [네트워크 1197](networks/network-1197.html) | 1/9 |
| hmi | 21 | fn06 | [네트워크 1198](networks/network-1198.html) | 1/9 |
| hmi | 22 | sc1 | [네트워크 1199](networks/network-1199.html) | 1/9 |
| hmi | 24 | ld01 mf | [네트워크 1201](networks/network-1201.html) | 1/9 |
| hmi | 25 | ld01 vb | [네트워크 1202](networks/network-1202.html) | 1/9 |
| hmi | 26 | sc10 | [네트워크 1203](networks/network-1203.html) | 1/9 |
| hmi | 27 | sc11 | [네트워크 1204](networks/network-1204.html) | 1/9 |
| hmi | 28 | fn04 ???? | [네트워크 1205](networks/network-1205.html) | 1/9 |
| hmi | 29 | vr03 | [네트워크 1206](networks/network-1206.html) | 1/9 |
| hmi | 30 | vr04 | [네트워크 1207](networks/network-1207.html) | 1/9 |
| hmi | 31 | vr05 | [네트워크 1208](networks/network-1208.html) | 1/9 |
| hmi | 32 | vr06 | [네트워크 1209](networks/network-1209.html) | 1/9 |
| hmi | 33 | fn05 | [네트워크 1210](networks/network-1210.html) | 1/9 |
| hmi | 34 | er01 | [네트워크 1211](networks/network-1211.html) | 1/9 |
| hmi | 35 | pv14 | [네트워크 1212](networks/network-1212.html) | 4/7 |
| hmi | 36 | bwf01 | [네트워크 1213](networks/network-1213.html) | 10/17 |
| hmi | 37 | bwf02 | [네트워크 1214](networks/network-1214.html) | 10/17 |
| hmi | 38 | pv01 | [네트워크 1215](networks/network-1215.html) | 1/21 |
| hmi | 39 | pv02 | [네트워크 1216](networks/network-1216.html) | 1/21 |
| hmi | 40 | pv03 | [네트워크 1217](networks/network-1217.html) | 1/13 |
| hmi | 41 | pv04 | [네트워크 1218](networks/network-1218.html) | 1/13 |
| hmi | 42 | br-01 | [네트워크 1219](networks/network-1219.html) | 4/7 |
| hmi | 43 | ev03 | [네트워크 1220](networks/network-1220.html) | 4/7 |
| analog output conversion | 14 | bc01 | [네트워크 1692](networks/network-1692.html) | 6/16 |
| analog output conversion | 15 | mc04 | [네트워크 1693](networks/network-1693.html) | 6/16 |
| valve control loop | 1 | mv01 controlled by tc03 | [네트워크 1702](networks/network-1702.html) | 35/61 |
| valve control loop | 2 | calibration encoder mv01 | [네트워크 1703](networks/network-1703.html) | 6/13 |
| valve control loop | 5 | mv03 controlled by psh03 | [네트워크 1706](networks/network-1706.html) | 41/73 |
| valve control loop | 6 | calibration encoder mv03 | [네트워크 1707](networks/network-1707.html) | 6/13 |
| analog input conversion | 38 | bc-01 | [네트워크 1768](networks/network-1768.html) | 2/9 |
| analog input conversion | 39 | mc04 | [네트워크 1769](networks/network-1769.html) | 2/9 |
| auto start motors | 5 | set points fn01 | [네트워크 1845](networks/network-1845.html) | 24/63 |
| auto start motors | 9 | production counters | [네트워크 1849](networks/network-1849.html) | 21/65 |
| burner control | 7 | counter burner off during preheating or production | [네트워크 1860](networks/network-1860.html) | 21/44 |

### 점검·진단 절차안

1. 논리 명칭 확인: 이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.
2. 데이터 추적: 원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SYS-HMI-SIM-01 | 데이터 추적 | 원시값 및 선택 조건 변경 | 논리 명칭의 입력/출력 관계 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SYS-HMI-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SYS-HMI-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SYS-HMI-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## SYS-ALARM · 알람·경광등·사이렌·Reset

원인·유지·확인·Reset·통합 알람 및 출력 표시를 연결한다. HMI Reset 요청과 내부 Reset 비트를 별도 신호로 추적한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: FG 17 / PDF 18.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %I19.6 | acknowledg | bool |  | 569 |
| %I19.7 | reset_allarm | bool |  | 570 |
| %Q7.6 | siren | bool | a 57.6 siren alarms | 783 |
| %Q7.7 | blinking ligh | bool | a 57.7 lampalarm | 784 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| ResetAlarms | DB2,X13.4 | PLC | 002E1 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| motor/alarm client | 1 | apron conveyor fault (cl01) | [네트워크 410](networks/network-410.html) | 6/11 |
| motor/alarm client | 2 | client motor 2 allarm | [네트워크 411](networks/network-411.html) | 6/11 |
| motor/alarm client | 3 | client motor 3 allarm | [네트워크 412](networks/network-412.html) | 6/11 |
| motor/alarm client | 4 | client motor 4 allarm | [네트워크 413](networks/network-413.html) | 6/11 |
| motor/alarm client | 5 | client motor 5 allarm | [네트워크 414](networks/network-414.html) | 6/11 |
| motor/alarm client | 6 | client motor 6 allarm | [네트워크 415](networks/network-415.html) | 6/11 |
| motor/alarm client | 7 | client motor 7 allarm | [네트워크 416](networks/network-416.html) | 6/11 |
| motor/alarm client | 8 | client motor 8 allarm | [네트워크 417](networks/network-417.html) | 6/11 |
| motor/alarm client | 9 | client motor 9 allarm | [네트워크 418](networks/network-418.html) | 6/11 |
| motor/alarm client | 10 | client motor 10 allarm | [네트워크 419](networks/network-419.html) | 6/11 |
| motor/alarm client | 11 | client motor 13 allarm | [네트워크 420](networks/network-420.html) | 6/11 |
| motor/alarm client | 12 | client motor 14 allarm | [네트워크 421](networks/network-421.html) | 6/11 |
| motor/alarm client | 13 | client motor 15 allarm | [네트워크 422](networks/network-422.html) | 6/11 |
| motor/alarm client | 14 | client motor 16 allarm | [네트워크 423](networks/network-423.html) | 6/11 |
| motor/alarm client | 15 | client motor 17 allarm | [네트워크 424](networks/network-424.html) | 6/11 |
| motor/alarm client | 16 | client motor 18 allarm bwf02--------------- | [네트워크 425](networks/network-425.html) | 6/11 |
| motor/alarm client | 17 | primary shradder fault (cl19) | [네트워크 426](networks/network-426.html) | 6/11 |
| allarm manager | 1 |  | [네트워크 927](networks/network-927.html) | 13/26 |
| allarm manager | 2 | com_w3 bit11 (new_allarm) | [네트워크 928](networks/network-928.html) | 12/32 |
| allarm manager | 3 | com_w3 bit9 (run_horn) | [네트워크 929](networks/network-929.html) | 5/9 |
| allarm manager | 4 | com_w3 bit8 (reset_allarm) | [네트워크 930](networks/network-930.html) | 14/23 |
| allarm manager | 5 | com_w3 bit8 (reset_allarm) | [네트워크 931](networks/network-931.html) | 8/13 |
| allarm manager | 6 |  | [네트워크 932](networks/network-932.html) | 1/4 |
| allarm manager | 7 | a 57.6 siren alarms | [네트워크 933](networks/network-933.html) | 9/15 |
| allarm manager | 8 | send report every 10 minutes | [네트워크 934](networks/network-934.html) | 6/12 |
| allarm manager | 9 | clear values of report at the end of the recording | [네트워크 935](networks/network-935.html) | 5/11 |
| allarms 2 | 1 | mv-01 motorized valve fault | [네트워크 1226](networks/network-1226.html) | 59/103 |
| allarms 2 | 2 | psl-04 low air pressure | [네트워크 1227](networks/network-1227.html) | 7/13 |
| allarms 2 | 3 | ld-01 low lime level | [네트워크 1228](networks/network-1228.html) | 8/16 |
| main | 11 | allarm manager and siren | [네트워크 1622](networks/network-1622.html) | 2/3 |
| main | 15 | maintenance period limits | [네트워크 1626](networks/network-1626.html) | 4/8 |
| analog input conversion | 26 | reading encoder mv01 | [네트워크 1756](networks/network-1756.html) | 3/28 |
| allarms 1 | 1 | bwf01 | [네트워크 1781](networks/network-1781.html) | 13/24 |
| allarms 1 | 2 | bwf01 | [네트워크 1782](networks/network-1782.html) | 11/19 |
| allarms 1 | 3 | bwf02 | [네트워크 1783](networks/network-1783.html) | 13/24 |
| allarms 1 | 4 | bwf02 | [네트워크 1784](networks/network-1784.html) | 11/19 |
| allarms 1 | 5 | bc01 | [네트워크 1785](networks/network-1785.html) | 16/28 |
| allarms 1 | 6 | bc01 | [네트워크 1786](networks/network-1786.html) | 7/13 |
| allarms 1 | 7 | rd01 | [네트워크 1787](networks/network-1787.html) | 16/28 |
| allarms 1 | 8 | fan rd01 | [네트워크 1788](networks/network-1788.html) | 10/19 |
| allarms 1 | 9 | spare motor | [네트워크 1789](networks/network-1789.html) | 10/19 |
| allarms 1 | 10 | spare motor | [네트워크 1790](networks/network-1790.html) | 7/13 |
| allarms 1 | 11 | mc04 | [네트워크 1791](networks/network-1791.html) | 16/28 |
| allarms 1 | 12 | mc04 deleted | [네트워크 1792](networks/network-1792.html) | 7/13 |
| allarms 1 | 14 | vs01 | [네트워크 1794](networks/network-1794.html) | 16/28 |
| allarms 1 | 16 | fn02 | [네트워크 1796](networks/network-1796.html) | 16/28 |
| allarms 1 | 17 | vr01 | [네트워크 1797](networks/network-1797.html) | 9/17 |
| allarms 1 | 18 | fn01 | [네트워크 1798](networks/network-1798.html) | 16/28 |
| allarms 1 | 19 | vr02 | [네트워크 1799](networks/network-1799.html) | 9/17 |
| allarms 1 | 20 | ch01 | [네트워크 1800](networks/network-1800.html) | 9/17 |
| allarms 1 | 21 | fn03 | [네트워크 1801](networks/network-1801.html) | 24/43 |
| allarms 1 | 22 | fn06 | [네트워크 1802](networks/network-1802.html) | 9/17 |
| allarms 1 | 23 | sc01 | [네트워크 1803](networks/network-1803.html) | 9/17 |
| allarms 1 | 25 | ld01 | [네트워크 1805](networks/network-1805.html) | 9/17 |
| allarms 1 | 26 | ld01 vibrator | [네트워크 1806](networks/network-1806.html) | 9/17 |
| allarms 1 | 27 | sc10 | [네트워크 1807](networks/network-1807.html) | 9/17 |
| allarms 1 | 28 | sc11 | [네트워크 1808](networks/network-1808.html) | 9/17 |
| allarms 1 | 29 | fn04 | [네트워크 1809](networks/network-1809.html) | 16/28 |
| allarms 1 | 30 | vr03 | [네트워크 1810](networks/network-1810.html) | 9/17 |
| allarms 1 | 31 | vr04 | [네트워크 1811](networks/network-1811.html) | 9/17 |
| allarms 1 | 32 | vr05 | [네트워크 1812](networks/network-1812.html) | 9/17 |
| allarms 1 | 33 | vr06 | [네트워크 1813](networks/network-1813.html) | 9/17 |
| allarms 1 | 34 | fn05 | [네트워크 1814](networks/network-1814.html) | 9/17 |
| allarms 1 | 35 | pv01 | [네트워크 1815](networks/network-1815.html) | 17/31 |
| allarms 1 | 36 | pv01 | [네트워크 1816](networks/network-1816.html) | 17/31 |
| allarms 1 | 37 | pv02 | [네트워크 1817](networks/network-1817.html) | 17/31 |
| allarms 1 | 38 | pv02 | [네트워크 1818](networks/network-1818.html) | 17/31 |
| allarms 1 | 39 | pv03 | [네트워크 1819](networks/network-1819.html) | 17/31 |
| allarms 1 | 40 | bwf01/bwf02 | [네트워크 1820](networks/network-1820.html) | 16/29 |
| allarms 1 | 41 | auxiliary inverter | [네트워크 1821](networks/network-1821.html) | 14/26 |
| allarms 1 | 42 | er01 | [네트워크 1822](networks/network-1822.html) | 8/16 |
| allarms 1 | 43 | presence 110v | [네트워크 1823](networks/network-1823.html) | 5/9 |
| allarms 1 | 44 | module emergenzy ok | [네트워크 1824](networks/network-1824.html) | 5/9 |
| allarms 1 | 45 | simulation enabled | [네트워크 1825](networks/network-1825.html) | 5/9 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| burner control | 1 | burner control box fault | [네트워크 1854](networks/network-1854.html) | 20/34 |
| burner control | 2 | burner servomotor not in minimal position | [네트워크 1855](networks/network-1855.html) | 10/18 |
| burner control | 16 | burner start fault reset | [네트워크 1869](networks/network-1869.html) | 3/6 |
| burner control | 21 | stoichiometry out of range | [네트워크 1874](networks/network-1874.html) | 12/22 |
| filter | 21 | pv-14 cold air filter fault | [네트워크 1902](networks/network-1902.html) | 12/22 |
| allarms 3 | 1 | max tc01 temperature | [네트워크 1979](networks/network-1979.html) | 21/45 |
| allarms 3 | 2 | low tc03 temperature | [네트워크 1980](networks/network-1980.html) | 35/74 |
| allarms 3 | 3 | max tc04 temperature | [네트워크 1981](networks/network-1981.html) | 21/43 |
| allarms 3 | 4 | oxigen analyzer out of range | [네트워크 1982](networks/network-1982.html) | 11/23 |
| allarms 3 | 5 | oxigen too high | [네트워크 1983](networks/network-1983.html) | 10/22 |
| allarms 3 | 6 | ro01 oxigen low limit | [네트워크 1984](networks/network-1984.html) | 12/26 |
| allarms 3 | 7 | ro01-ro02 signal compare fault | [네트워크 1985](networks/network-1985.html) | 13/28 |
| allarms 3 | 8 | tc01/tc02 signal compare fault | [네트워크 1986](networks/network-1986.html) | 15/32 |
| allarms 3 | 9 | pc-01 low depressure | [네트워크 1987](networks/network-1987.html) | 13/27 |
| allarms 3 | 10 | high vibrations fn-01 | [네트워크 1988](networks/network-1988.html) | 10/21 |
| allarms 3 | 11 | max pressure psh-02 | [네트워크 1989](networks/network-1989.html) | 10/21 |
| allarms 3 | 12 | hydrogen box not ready | [네트워크 1990](networks/network-1990.html) | 10/18 |
| allarms 3 | 13 | tc-09 filter inlet temperature | [네트워크 1991](networks/network-1991.html) | 20/43 |
| allarms 3 | 14 | max filter depressure | [네트워크 1992](networks/network-1992.html) | 14/32 |
| allarms 3 | 15 | incorrect scraps feeder formula | [네트워크 1993](networks/network-1993.html) | 11/24 |
| allarms 3 | 16 | plc hardware diagnostic fault fault | [네트워크 1994](networks/network-1994.html) | 16/25 |
| allarms 3 | 17 | ro03 | [네트워크 1995](networks/network-1995.html) | 13/27 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 930 | SCoil | Flag.RESET_ALLARM | (Inputs.Reset_allarmi OR Flag.Reset_Allarms_HMI) | 조건 성립 시 Set |
| 930 | RCoil | Flag.Reset_Allarms_HMI | (Inputs.Reset_allarmi OR Flag.Reset_Allarms_HMI) | 조건 성립 시 Reset |
| 930 | Coil | 103A7 | LRef UID 64.Q (블록 동작 확인) | 조건에 따른 Coil 기록 |
| 930 | Coil | Reset_Inverter | LRef UID 73.Q (블록 동작 확인) | 조건에 따른 Coil 기록 |
| 930 | SCoil | Flag.STOP_HORN | (Inputs.Tacitazione OR Flag.Stop_horn_HMI) | 조건 성립 시 Set |
| 930 | RCoil | Flag.Stop_horn_HMI | (Inputs.Tacitazione OR Flag.Stop_horn_HMI) | 조건 성립 시 Reset |
| 931 | SdCoil | Tag_160 | (Flag.RESET_ALLARM OR Flag.STOP_HORN) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 S5T#1S |
| 931 | RCoil | Flag.RESET_ALLARM | ((Flag.RESET_ALLARM OR Flag.STOP_HORN) AND Tag_160) | 조건 성립 시 Reset |
| 931 | RCoil | Flag.STOP_HORN | ((Flag.RESET_ALLARM OR Flag.STOP_HORN) AND Tag_160) | 조건 성립 시 Reset |
| 931 | RCoil | Blinking Ligh | ((Flag.RESET_ALLARM OR Flag.STOP_HORN) AND Tag_160) | 조건 성립 시 Reset |
| 933 | SdCoil | Tag_161 | (Flag.RUN_HORN OR Flag.M_HORN) | 시간 동작 SdCoil; 타이머 의미 추가 확인 / 시간 인자 Data.SIREN_WORK_TIME |
| 933 | Coil | Siren | (Flag.RUN_HORN OR Flag.M_HORN) | 조건에 따른 Coil 기록 |
| 933 | SCoil | Blinking Ligh | PBox UID 268.out (블록 동작 확인) | 조건 성립 시 Set |
| 933 | RCoil | Flag.RUN_HORN | ((Flag.RUN_HORN OR Flag.M_HORN) AND Tag_161) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 논리 명칭 확인: 이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.
2. 데이터 추적: 원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SYS-ALARM-SIM-01 | 데이터 추적 | 원시값 및 선택 조건 변경 | 논리 명칭의 입력/출력 관계 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SYS-ALARM-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SYS-ALARM-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SYS-ALARM-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SYS-ALARM-V-04 | 전기 배선 | 현재 I/Q 주소·모듈·단자·전원·중간 릴레이를 현장 배선으로 검증 | 확인 대기 |
| SYS-ALARM-V-05 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## SYS-AUTO · 자동 기동·정지·유지보수

운전 허가·기동 단계·대기·유지보수 모드의 호출 및 출력 관계를 관리한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M80.5 | maintenance pv01 | bool |  | 474 |
| %M80.6 | maintenance pv02 | bool |  | 475 |

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| AbilitaMaintenance | DB2,X7.5 | PLC | 00409 |
| AbilitaAuto | DB2,X7.3 | PLC | 000DB |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| startup only | 2 | reset all flag start motors | [네트워크 402](networks/network-402.html) | 9/25 |
| startup only | 3 | reset all flag allarms | [네트워크 403](networks/network-403.html) | 10/27 |
| startup only | 4 | plants defaults | [네트워크 404](networks/network-404.html) | 10/14 |
| startup only | 5 | default | [네트워크 405](networks/network-405.html) | 6/8 |
| main | 1 | simulation | [네트워크 1612](networks/network-1612.html) | 2/3 |
| main | 2 |  | [네트워크 1613](networks/network-1613.html) | 5/6 |
| main | 3 | word input | [네트워크 1614](networks/network-1614.html) | 4/12 |
| main | 4 |  | [네트워크 1615](networks/network-1615.html) | 3/9 |
| main | 5 | word output | [네트워크 1616](networks/network-1616.html) | 4/12 |
| main | 6 |  | [네트워크 1617](networks/network-1617.html) | 4/12 |
| main | 7 |  | [네트워크 1618](networks/network-1618.html) | 3/9 |
| main | 8 | analog conversion and allarms | [네트워크 1619](networks/network-1619.html) | 5/3 |
| main | 9 | motors valve and burner | [네트워크 1620](networks/network-1620.html) | 7/3 |
| main | 10 | motorized valve | [네트워크 1621](networks/network-1621.html) | 3/3 |
| main | 11 | allarm manager and siren | [네트워크 1622](networks/network-1622.html) | 2/3 |
| main | 12 | cpu clock | [네트워크 1623](networks/network-1623.html) | 3/7 |
| main | 13 | trasfering bit of maintenance | [네트워크 1624](networks/network-1624.html) | 3/7 |
| main | 15 | maintenance period limits | [네트워크 1626](networks/network-1626.html) | 4/8 |
| auto start motors | 1 | increment seconds count | [네트워크 1841](networks/network-1841.html) | 5/12 |
| auto start motors | 2 | status display in supervisor | [네트워크 1842](networks/network-1842.html) | 5/11 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 5 | set points fn01 | [네트워크 1845](networks/network-1845.html) | 24/63 |
| auto start motors | 6 | emergency stop | [네트워크 1846](networks/network-1846.html) | 4/11 |
| auto start motors | 7 | presetting sequence 5: complete engine stop | [네트워크 1847](networks/network-1847.html) | 53/87 |
| auto start motors | 8 | presetting sequence 6: no sequence | [네트워크 1848](networks/network-1848.html) | 6/14 |
| auto start motors | 9 | production counters | [네트워크 1849](networks/network-1849.html) | 21/65 |
| r1 scraps gate 2 | 5 | a 48.4 ev-02 valvecommand | [네트워크 1915](networks/network-1915.html) | 12/21 |
| r1 scraps gate 2 | 6 | pv-02 rotary drum discharge valve | [네트워크 1916](networks/network-1916.html) | 20/33 |
| r1 scraps gate 2 | 10 | a 56.4 ev-05 valvecommand | [네트워크 1920](networks/network-1920.html) | 11/19 |
| motors 1 | 1 | maintenance | [네트워크 1930](networks/network-1930.html) | 4/7 |
| motors 1 | 2 | block load | [네트워크 1931](networks/network-1931.html) | 11/21 |
| motors 1 | 6 | bc01 | [네트워크 1935](networks/network-1935.html) | 13/23 |
| motors 1 | 7 | rd01 | [네트워크 1936](networks/network-1936.html) | 12/23 |
| motors 1 | 10 | rd01 fan | [네트워크 1939](networks/network-1939.html) | 9/16 |
| motors 1 | 11 | mc03 spare motor | [네트워크 1940](networks/network-1940.html) | 10/18 |
| motors 1 | 12 | mc04 | [네트워크 1941](networks/network-1941.html) | 9/16 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1624 | Move | Tag_189 | ON | Move 입력 Data.Maint_code_0 |
| 1624 | Move | Tag_190 | ON | Move 입력 Data.Maint_code_3 |
| 1626 | RCoil | Allarm.MAINTENANCE_PERIOD_LIMIT | ((ON AND Flag.RESET_ALLARM) AND Allarm.MAINTENANCE_PERIOD_LIMIT) | 조건 성립 시 Reset |
| 1930 | Coil | UNDER TESTING | (ON AND Flag.Maintenance_ON) | 조건에 따른 Coil 기록 |
| 1930 | Coil | Allarm.Maintenance_ON | (ON AND Flag.Maintenance_ON) | 조건에 따른 Coil 기록 |


### 점검·진단 절차안

1. 논리 명칭 확인: 이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.
2. 데이터 추적: 원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SYS-AUTO-SIM-01 | 데이터 추적 | 원시값 및 선택 조건 변경 | 논리 명칭의 입력/출력 관계 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SYS-AUTO-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SYS-AUTO-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SYS-AUTO-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SYS-AUTO-V-04 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## SYS-PID · 온도·압력·산소·비율 제어

주기 OB의 PID 호출, 채널 선택, 수동/자동, 제한과 밸브·버너 출력 경로를 관리한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| Stechiometro | DB5,REAL4 | PLC | 00421 |
| TC_PID_REF | DB39,REAL2 | PLC | 001C0 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| valve control loop | 1 | mv01 controlled by tc03 | [네트워크 1702](networks/network-1702.html) | 35/61 |
| valve control loop | 2 | calibration encoder mv01 | [네트워크 1703](networks/network-1703.html) | 6/13 |
| valve control loop | 3 | mv02 controlled by psh-01 | [네트워크 1704](networks/network-1704.html) | 33/57 |
| valve control loop | 4 | mv03 controlled by psh03 | [네트워크 1705](networks/network-1705.html) | 11/24 |
| valve control loop | 5 | mv03 controlled by psh03 | [네트워크 1706](networks/network-1706.html) | 41/73 |
| valve control loop | 6 | calibration encoder mv03 | [네트워크 1707](networks/network-1707.html) | 6/13 |
| valve control loop | 7 | mv05 controlled by ro-01 | [네트워크 1708](networks/network-1708.html) | 34/60 |
| valve control loop | 8 | mv06 controlled by psh02 | [네트워크 1709](networks/network-1709.html) | 12/27 |
| valve control loop | 9 | the working tool has a low range | [네트워크 1710](networks/network-1710.html) | 20/39 |
| valve control loop | 10 | mv06 controlled by psh02 | [네트워크 1711](networks/network-1711.html) | 33/59 |
| valve control loop | 11 | motorized valve work time pulse generator | [네트워크 1712](networks/network-1712.html) | 7/14 |
| valve control loop | 12 | motorized valve pulse generator for rotation control | [네트워크 1713](networks/network-1713.html) | 42/95 |
| valve control loop | 13 | motorized valve fault | [네트워크 1714](networks/network-1714.html) | 43/87 |
| cyc_int2 ogni 1s | 3 |  | [네트워크 1721](networks/network-1721.html) | 5/12 |
| cyc_int2 ogni 1s | 4 |  | [네트워크 1722](networks/network-1722.html) | 2/6 |
| cyc_int2 ogni 1s | 5 | auto start/stop motors and presetting | [네트워크 1723](networks/network-1723.html) | 2/3 |
| cyc_int2 ogni 1s | 6 | delayed burner flow rate variation | [네트워크 1724](networks/network-1724.html) | 5/15 |
| control_stechio | 1 | calculate the gas flow rate based on the theoretical ramp | [네트워크 1830](networks/network-1830.html) | 41/103 |
| control_stechio | 3 | run pid block | [네트워크 1832](networks/network-1832.html) | 7/45 |
| control_stechio | 5 | verify range sent by gas | [네트워크 1834](networks/network-1834.html) | 5/13 |
| control_stechio | 6 | check stoichiometric ratio correction range | [네트워크 1835](networks/network-1835.html) | 5/11 |
| burner control | 1 | burner control box fault | [네트워크 1854](networks/network-1854.html) | 20/34 |
| burner control | 2 | burner servomotor not in minimal position | [네트워크 1855](networks/network-1855.html) | 10/18 |
| burner control | 3 | a 56.3 max.temperaturefilter | [네트워크 1856](networks/network-1856.html) | 4/8 |
| burner control | 4 | start gas test | [네트워크 1857](networks/network-1857.html) | 12/23 |
| burner control | 5 | burner stop | [네트워크 1858](networks/network-1858.html) | 21/40 |
| burner control | 6 | counter minutes of burner work | [네트워크 1859](networks/network-1859.html) | 9/20 |
| burner control | 7 | counter burner off during preheating or production | [네트워크 1860](networks/network-1860.html) | 21/44 |
| burner control | 8 | programmed burner shutdown every 24 hours | [네트워크 1861](networks/network-1861.html) | 5/11 |
| burner control | 9 | a 56.6 start high flameburner | [네트워크 1862](networks/network-1862.html) | 25/51 |
| burner control | 10 | enable relay forceed spark | [네트워크 1863](networks/network-1863.html) | 13/23 |
| burner control | 11 | reduce speed mn01 se tc01 > 30°c the setpoint | [네트워크 1864](networks/network-1864.html) | 8/19 |
| burner control | 12 | burner lock | [네트워크 1865](networks/network-1865.html) | 17/31 |
| burner control | 13 | burner start sequence | [네트워크 1866](networks/network-1866.html) | 9/16 |
| burner control | 14 | for viewing washing time in supervisor | [네트워크 1867](networks/network-1867.html) | 5/12 |
| burner control | 15 | enable burner cleaning sequence | [네트워크 1868](networks/network-1868.html) | 71/151 |
| burner control | 16 | burner start fault reset | [네트워크 1869](networks/network-1869.html) | 3/6 |
| burner control | 17 | burner servomotor control fb41 pid mode | [네트워크 1870](networks/network-1870.html) | 15/29 |
| burner control | 18 | if on auto send pid result to the module | [네트워크 1871](networks/network-1871.html) | 2/6 |
| burner control | 19 | burner air range limits | [네트워크 1872](networks/network-1872.html) | 14/32 |
| burner control | 20 | simulation | [네트워크 1873](networks/network-1873.html) | 2/5 |
| burner control | 21 | stoichiometry out of range | [네트워크 1874](networks/network-1874.html) | 12/22 |
| burner control | 22 | dryout warm first ramp | [네트워크 1875](networks/network-1875.html) | 23/58 |
| burner control | 23 | dryout warm second ramp | [네트워크 1876](networks/network-1876.html) | 9/23 |
| burner control | 24 | dryout warm third ramp | [네트워크 1877](networks/network-1877.html) | 13/33 |
| cyc_int5 ogni 100ms | 2 | controll ro01 moduling mv05 - pid | [네트워크 5](networks/network-5.html) | 8/35 |
| cyc_int5 ogni 100ms | 4 | controll pc01 moduling mv02 | [네트워크 7](networks/network-7.html) | 5/30 |
| cyc_int5 ogni 100ms | 5 |  | [네트워크 8](networks/network-8.html) | 2/6 |
| cyc_int5 ogni 100ms | 8 | controll tc03 moduling mv01 | [네트워크 11](networks/network-11.html) | 13/46 |
| cyc_int5 ogni 100ms | 9 | disable pid control on vt02 | [네트워크 12](networks/network-12.html) | 6/11 |
| cyc_int5 ogni 100ms | 12 | control pc02 moduling mv03 - not used | [네트워크 15](networks/network-15.html) | 7/33 |
| cyc_int5 ogni 100ms | 13 | executes gas flow calculation block | [네트워크 16](networks/network-16.html) | 2/3 |

### 점검·진단 절차안

1. 논리 명칭 확인: 이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.
2. 데이터 추적: 원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SYS-PID-SIM-01 | 데이터 추적 | 원시값 및 선택 조건 변경 | 논리 명칭의 입력/출력 관계 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SYS-PID-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SYS-PID-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SYS-PID-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SYS-PID-V-04 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## SYS-RECIPES · 레시피·설정값 관리

레시피 선택·편집·적용값·현재 설정 DB를 추적한다. 화면 편집 값과 실제 적용 값의 전달 경로를 구분한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| Editor_Load_Recipe | DB26,X4.3 | PLC | 0041D |
| Editor_Save_Recipe | DB26,X4.4 | PLC | 0041C |
| Editor_Modify_Recipe | DB26,X4.5 | PLC | 0041B |
| Editor_Active_Recipe | DB26,INT6 | PLC | 00418 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| main | 2 |  | [네트워크 1613](networks/network-1613.html) | 5/6 |

### 점검·진단 절차안

1. 논리 명칭 확인: 이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.
2. 데이터 추적: 원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SYS-RECIPES-SIM-01 | 데이터 추적 | 원시값 및 선택 조건 변경 | 논리 명칭의 입력/출력 관계 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SYS-RECIPES-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SYS-RECIPES-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SYS-RECIPES-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SYS-RECIPES-V-04 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## SYS-SIMULATION · 기존 시험·시뮬레이션 블록

백업에 남은 Simulation 블록과 시험 비트가 실제 입력 대체·자동 조건에 미치는 영향을 검토한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M180.0 | simulation(1) | bool |  | 1516 |
| %M5.5 | under testing | bool |  | 1906 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| cyc_int4 ogni 200ms | 1 | for test trends | [네트워크 396](networks/network-396.html) | 4/11 |
| simulation | 1 |  | [네트워크 1079](networks/network-1079.html) | 3/7 |
| simulation | 2 |  | [네트워크 1080](networks/network-1080.html) | 7/9 |
| simulation | 3 |  | [네트워크 1081](networks/network-1081.html) | 3/7 |
| simulation | 4 | motors simulated | [네트워크 1082](networks/network-1082.html) | 14/22 |
| simulation | 5 | mv | [네트워크 1083](networks/network-1083.html) | 70/151 |
| simulation | 6 | motors simulated | [네트워크 1084](networks/network-1084.html) | 16/25 |
| simulation | 7 | motors simulated | [네트워크 1085](networks/network-1085.html) | 19/29 |
| simulation | 8 | motors simulated | [네트워크 1086](networks/network-1086.html) | 10/15 |
| simulation | 9 | pv03 | [네트워크 1087](networks/network-1087.html) | 4/7 |
| simulation | 10 | pv04 | [네트워크 1088](networks/network-1088.html) | 4/7 |
| simulation | 11 | pv14 | [네트워크 1089](networks/network-1089.html) | 4/7 |
| simulation | 12 | pv01 | [네트워크 1090](networks/network-1090.html) | 8/13 |
| simulation | 13 | pv02 | [네트워크 1091](networks/network-1091.html) | 8/13 |
| simulation | 14 |  | [네트워크 1092](networks/network-1092.html) | 18/42 |
| main | 1 | simulation | [네트워크 1612](networks/network-1612.html) | 2/3 |
| main | 2 |  | [네트워크 1613](networks/network-1613.html) | 5/6 |
| valve control loop | 7 | mv05 controlled by ro-01 | [네트워크 1708](networks/network-1708.html) | 34/60 |
| analog input conversion | 26 | reading encoder mv01 | [네트워크 1756](networks/network-1756.html) | 3/28 |
| analog input conversion | 27 | reading encoder mv02 | [네트워크 1757](networks/network-1757.html) | 3/28 |
| analog input conversion | 28 | reading encoder mv03 | [네트워크 1758](networks/network-1758.html) | 3/28 |
| analog input conversion | 29 | reading encoder mv05 | [네트워크 1759](networks/network-1759.html) | 3/28 |
| analog input conversion | 30 | reading encoder mv06 | [네트워크 1760](networks/network-1760.html) | 3/28 |
| allarms 1 | 45 | simulation enabled | [네트워크 1825](networks/network-1825.html) | 5/9 |
| burner control | 20 | simulation | [네트워크 1873](networks/network-1873.html) | 2/5 |
| r1 scraps gate 2 | 1 | pv-01 | [네트워크 1911](networks/network-1911.html) | 19/31 |
| motors 1 | 1 | maintenance | [네트워크 1930](networks/network-1930.html) | 4/7 |
| motors 1 | 6 | bc01 | [네트워크 1935](networks/network-1935.html) | 13/23 |
| motors 1 | 7 | rd01 | [네트워크 1936](networks/network-1936.html) | 12/23 |
| motors 1 | 10 | rd01 fan | [네트워크 1939](networks/network-1939.html) | 9/16 |
| motors 1 | 11 | mc03 spare motor | [네트워크 1940](networks/network-1940.html) | 10/18 |
| motors 1 | 22 | fn01 | [네트워크 1951](networks/network-1951.html) | 11/21 |
| motors 1 | 26 | fn06 | [네트워크 1955](networks/network-1955.html) | 8/14 |
| motors 1 | 27 | sc01 | [네트워크 1956](networks/network-1956.html) | 8/14 |
| motors 1 | 29 | ld01 | [네트워크 1958](networks/network-1958.html) | 9/16 |
| motors 1 | 32 | ld01 | [네트워크 1961](networks/network-1961.html) | 12/21 |
| motors 1 | 33 | sc10 | [네트워크 1962](networks/network-1962.html) | 8/14 |
| motors 1 | 34 | sc11 | [네트워크 1963](networks/network-1963.html) | 8/14 |
| motors 1 | 40 | vr06 | [네트워크 1969](networks/network-1969.html) | 8/14 |
| motors 1 | 41 | fn05 | [네트워크 1970](networks/network-1970.html) | 8/14 |
| motors 1 | 42 | er01 | [네트워크 1971](networks/network-1971.html) | 10/18 |
| cyc_int5 ogni 100ms | 2 | controll ro01 moduling mv05 - pid | [네트워크 5](networks/network-5.html) | 8/35 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1825 | Coil | Allarm.Simulation enabled | Simulation(1) | 조건에 따른 Coil 기록 |
| 1825 | RCoil | Allarm.Simulation enabled | (Flag.RESET_ALLARM AND Allarm.Simulation enabled) | 조건 성립 시 Reset |
| 1873 | Move | Data.Burner_Panel_SetPoint | OFF | Move 입력 ORef UID 1272 |


### 점검·진단 절차안

1. 논리 명칭 확인: 이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.
2. 데이터 추적: 원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SYS-SIMULATION-SIM-01 | 데이터 추적 | 원시값 및 선택 조건 변경 | 논리 명칭의 입력/출력 관계 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SYS-SIMULATION-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SYS-SIMULATION-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SYS-SIMULATION-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## SYS-RUNHOURS · 모터 운전시간·정비 이력

Time work motor 관련 카운트·유지보수 값·Reset 경로를 관리한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| time work motor | 1 | client motor 1 | [네트워크 1002](networks/network-1002.html) | 7/18 |
| time work motor | 2 | client motor 2 | [네트워크 1003](networks/network-1003.html) | 7/18 |
| time work motor | 3 | client motor 3 | [네트워크 1004](networks/network-1004.html) | 7/18 |
| time work motor | 4 | client motor 4 | [네트워크 1005](networks/network-1005.html) | 7/18 |
| time work motor | 5 | client motor 5 | [네트워크 1006](networks/network-1006.html) | 7/18 |
| time work motor | 6 | client motor 6 | [네트워크 1007](networks/network-1007.html) | 7/18 |
| time work motor | 7 | client motor 7 | [네트워크 1008](networks/network-1008.html) | 7/18 |
| time work motor | 8 | client motor 8 | [네트워크 1009](networks/network-1009.html) | 7/18 |
| time work motor | 9 | client motor 9 | [네트워크 1010](networks/network-1010.html) | 7/18 |
| time work motor | 10 | client motor 10 | [네트워크 1011](networks/network-1011.html) | 7/18 |
| time work motor | 11 | client motor 13 | [네트워크 1012](networks/network-1012.html) | 7/18 |
| time work motor | 12 | client motor 14 | [네트워크 1013](networks/network-1013.html) | 7/18 |
| time work motor | 13 | client motor 15 | [네트워크 1014](networks/network-1014.html) | 7/18 |
| time work motor | 14 | client motor 16 | [네트워크 1015](networks/network-1015.html) | 7/18 |
| time work motor | 15 | client motor 17 | [네트워크 1016](networks/network-1016.html) | 7/18 |
| time work motor | 16 | client motor 19 | [네트워크 1017](networks/network-1017.html) | 7/18 |
| time work motor | 17 | bc-01 | [네트워크 1018](networks/network-1018.html) | 7/18 |
| time work motor | 18 | rd-01 | [네트워크 1019](networks/network-1019.html) | 7/18 |
| time work motor | 19 | rd-01 fan | [네트워크 1020](networks/network-1020.html) | 7/18 |
| time work motor | 20 | mc-03 | [네트워크 1021](networks/network-1021.html) | 7/18 |
| time work motor | 21 | mc-04 | [네트워크 1022](networks/network-1022.html) | 7/18 |
| time work motor | 23 | vs-01 | [네트워크 1024](networks/network-1024.html) | 7/18 |
| time work motor | 25 | fn-02 | [네트워크 1026](networks/network-1026.html) | 7/18 |
| time work motor | 26 | vr-01 | [네트워크 1027](networks/network-1027.html) | 7/18 |
| time work motor | 27 | fn-01 | [네트워크 1028](networks/network-1028.html) | 7/18 |
| time work motor | 28 | vr-02 | [네트워크 1029](networks/network-1029.html) | 7/18 |
| time work motor | 29 | ch-01 | [네트워크 1030](networks/network-1030.html) | 7/18 |
| time work motor | 30 | fn-03 | [네트워크 1031](networks/network-1031.html) | 7/18 |
| time work motor | 31 | fn-06 | [네트워크 1032](networks/network-1032.html) | 7/18 |
| time work motor | 32 | sc-01 | [네트워크 1033](networks/network-1033.html) | 7/18 |
| time work motor | 34 | ld-01 | [네트워크 1035](networks/network-1035.html) | 7/18 |
| time work motor | 35 | ld-01 vib | [네트워크 1036](networks/network-1036.html) | 7/18 |
| time work motor | 36 | sc-10 | [네트워크 1037](networks/network-1037.html) | 7/18 |
| time work motor | 37 | sc-11 | [네트워크 1038](networks/network-1038.html) | 7/18 |
| time work motor | 38 | fn-04 | [네트워크 1039](networks/network-1039.html) | 7/18 |
| time work motor | 39 | vr-03 | [네트워크 1040](networks/network-1040.html) | 7/18 |
| time work motor | 40 | vr-04 | [네트워크 1041](networks/network-1041.html) | 7/18 |
| time work motor | 41 | vr-05 | [네트워크 1042](networks/network-1042.html) | 7/18 |
| time work motor | 42 | vr-06 | [네트워크 1043](networks/network-1043.html) | 7/18 |
| time work motor | 43 | fn-05 | [네트워크 1044](networks/network-1044.html) | 7/18 |
| time work motor | 44 |  | [네트워크 1045](networks/network-1045.html) | 6/17 |
| time work motor | 45 |  | [네트워크 1046](networks/network-1046.html) | 6/17 |
| time work motor | 46 |  | [네트워크 1047](networks/network-1047.html) | 6/17 |
| time work motor | 47 |  | [네트워크 1048](networks/network-1048.html) | 6/17 |
| time work motor | 48 |  | [네트워크 1049](networks/network-1049.html) | 6/17 |
| time work motor | 49 |  | [네트워크 1050](networks/network-1050.html) | 6/17 |
| time work motor | 50 |  | [네트워크 1051](networks/network-1051.html) | 6/17 |
| time work motor | 51 |  | [네트워크 1052](networks/network-1052.html) | 6/17 |
| time work motor | 52 |  | [네트워크 1053](networks/network-1053.html) | 6/17 |
| time work motor | 53 |  | [네트워크 1054](networks/network-1054.html) | 2/5 |
| time work motor | 54 | reset working hours after recording the data in the db | [네트워크 1055](networks/network-1055.html) | 8/15 |
| time work motor | 55 | every 1 minutes | [네트워크 1056](networks/network-1056.html) | 2/5 |
| cyc_int2 ogni 1s | 3 |  | [네트워크 1721](networks/network-1721.html) | 5/12 |
| cyc_int2 ogni 1s | 4 |  | [네트워크 1722](networks/network-1722.html) | 2/6 |
| cyc_int2 ogni 1s | 5 | auto start/stop motors and presetting | [네트워크 1723](networks/network-1723.html) | 2/3 |
| cyc_int2 ogni 1s | 6 | delayed burner flow rate variation | [네트워크 1724](networks/network-1724.html) | 5/15 |

### 점검·진단 절차안

1. 논리 명칭 확인: 이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.
2. 데이터 추적: 원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SYS-RUNHOURS-SIM-01 | 데이터 추적 | 원시값 및 선택 조건 변경 | 논리 명칭의 입력/출력 관계 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SYS-RUNHOURS-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SYS-RUNHOURS-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SYS-RUNHOURS-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

## SYS-COUNTERS · 생산량·가스·유량 계수

BWF 펄스·생산량·가스/유량·Reset·스케일과 누적값을 관리한다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

직접 심볼 주소 미식별. 상위/연관 설비 기준으로 관리한다.

### HMI 설정

| HMI 태그 | 주소 | Access Name | 내부 ID |
| --- | --- | --- | --- |
| RESET_PROD_COUNT | DB41,X50.3 | PLC | 00463 |
| RESET_GAS_COUNT | DB41,X50.2 | PLC | 00462 |
| Conta_prod | DB41,REAL8 | PLC | 00461 |
| Conta_prod_TOT | DB41,REAL4 | PLC | 00460 |
| Conta_gas_TOT | DB5,REAL34 | PLC | 003F2 |

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| allarm manager | 9 | clear values of report at the end of the recording | [네트워크 935](networks/network-935.html) | 5/11 |
| analog input conversion | 1 | tc04 | [네트워크 1731](networks/network-1731.html) | 2/9 |
| analog input conversion | 2 | tc-05 | [네트워크 1732](networks/network-1732.html) | 2/9 |
| analog input conversion | 3 | tc-09 | [네트워크 1733](networks/network-1733.html) | 2/9 |
| analog input conversion | 4 | tc-10 | [네트워크 1734](networks/network-1734.html) | 2/9 |
| analog input conversion | 5 | client 1 bwf01 flow rate | [네트워크 1735](networks/network-1735.html) | 9/26 |
| analog input conversion | 6 | client 2 bwf02 flow rate | [네트워크 1736](networks/network-1736.html) | 9/26 |
| analog input conversion | 7 | client 3 level indicator bwf01 | [네트워크 1737](networks/network-1737.html) | 2/9 |
| analog input conversion | 8 | client 4 level indicator bwf02 | [네트워크 1738](networks/network-1738.html) | 2/9 |
| analog input conversion | 9 | tc-01 | [네트워크 1739](networks/network-1739.html) | 2/9 |
| analog input conversion | 10 | tc-02 | [네트워크 1740](networks/network-1740.html) | 2/9 |
| analog input conversion | 11 | tc-03 | [네트워크 1741](networks/network-1741.html) | 2/9 |
| analog input conversion | 12 | tc-06 | [네트워크 1742](networks/network-1742.html) | 2/9 |
| analog input conversion | 13 | tc-07 | [네트워크 1743](networks/network-1743.html) | 2/9 |
| analog input conversion | 14 | zt-01 | [네트워크 1744](networks/network-1744.html) | 2/9 |
| analog input conversion | 15 | psh-01 | [네트워크 1745](networks/network-1745.html) | 2/9 |
| analog input conversion | 16 | psh-02 | [네트워크 1746](networks/network-1746.html) | 2/9 |
| analog input conversion | 17 | psh-03 | [네트워크 1747](networks/network-1747.html) | 2/9 |
| analog input conversion | 18 | r0-01 | [네트워크 1748](networks/network-1748.html) | 2/9 |
| analog input conversion | 19 | r0-02 | [네트워크 1749](networks/network-1749.html) | 2/9 |
| analog input conversion | 20 | r0-03 | [네트워크 1750](networks/network-1750.html) | 4/14 |
| analog input conversion | 21 | r0-04 | [네트워크 1751](networks/network-1751.html) | 2/9 |
| analog input conversion | 22 | gas br-01 - position | [네트워크 1752](networks/network-1752.html) | 2/9 |
| analog input conversion | 23 | air br-01 - position | [네트워크 1753](networks/network-1753.html) | 2/9 |
| analog input conversion | 24 | max flow gas - flowmeter | [네트워크 1754](networks/network-1754.html) | 4/14 |
| analog input conversion | 25 | max flow air - flowmeter | [네트워크 1755](networks/network-1755.html) | 2/9 |
| analog input conversion | 26 | reading encoder mv01 | [네트워크 1756](networks/network-1756.html) | 3/28 |
| analog input conversion | 27 | reading encoder mv02 | [네트워크 1757](networks/network-1757.html) | 3/28 |
| analog input conversion | 28 | reading encoder mv03 | [네트워크 1758](networks/network-1758.html) | 3/28 |
| analog input conversion | 29 | reading encoder mv05 | [네트워크 1759](networks/network-1759.html) | 3/28 |
| analog input conversion | 30 | reading encoder mv06 | [네트워크 1760](networks/network-1760.html) | 3/28 |
| analog input conversion | 31 | store current position value at power-off | [네트워크 1761](networks/network-1761.html) | 6/13 |
| analog input conversion | 32 | data management mv01 | [네트워크 1762](networks/network-1762.html) | 10/28 |
| analog input conversion | 33 | data management mv02 | [네트워크 1763](networks/network-1763.html) | 10/28 |
| analog input conversion | 34 | mv03 data management | [네트워크 1764](networks/network-1764.html) | 10/28 |
| analog input conversion | 35 | mv05 data management | [네트워크 1765](networks/network-1765.html) | 10/28 |
| analog input conversion | 36 | mv06 data management | [네트워크 1766](networks/network-1766.html) | 10/28 |
| analog input conversion | 37 | fn-02 fan | [네트워크 1767](networks/network-1767.html) | 2/9 |
| analog input conversion | 38 | bc-01 | [네트워크 1768](networks/network-1768.html) | 2/9 |
| analog input conversion | 39 | mc04 | [네트워크 1769](networks/network-1769.html) | 2/9 |
| analog input conversion | 40 | fn-02 aspirator | [네트워크 1770](networks/network-1770.html) | 2/9 |
| analog input conversion | 41 | rd-01 | [네트워크 1771](networks/network-1771.html) | 2/9 |
| analog input conversion | 42 | fn-01 | [네트워크 1772](networks/network-1772.html) | 2/9 |
| analog input conversion | 43 | dp-01 | [네트워크 1773](networks/network-1773.html) | 2/9 |
| analog input conversion | 44 | dp-02 | [네트워크 1774](networks/network-1774.html) | 2/9 |
| analog input conversion | 45 | pc-01 | [네트워크 1775](networks/network-1775.html) | 2/9 |
| analog input conversion | 46 | contactor ton passed in bwf | [네트워크 1776](networks/network-1776.html) | 7/17 |
| cyc_int5 ogni 100ms | 2 | controll ro01 moduling mv05 - pid | [네트워크 5](networks/network-5.html) | 8/35 |
| cyc_int5 ogni 100ms | 4 | controll pc01 moduling mv02 | [네트워크 7](networks/network-7.html) | 5/30 |
| cyc_int5 ogni 100ms | 5 |  | [네트워크 8](networks/network-8.html) | 2/6 |
| cyc_int5 ogni 100ms | 8 | controll tc03 moduling mv01 | [네트워크 11](networks/network-11.html) | 13/46 |
| cyc_int5 ogni 100ms | 9 | disable pid control on vt02 | [네트워크 12](networks/network-12.html) | 6/11 |
| cyc_int5 ogni 100ms | 12 | control pc02 moduling mv03 - not used | [네트워크 15](networks/network-15.html) | 7/33 |
| cyc_int5 ogni 100ms | 13 | executes gas flow calculation block | [네트워크 16](networks/network-16.html) | 2/3 |

### 점검·진단 절차안

1. 논리 명칭 확인: 이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.
2. 데이터 추적: 원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SYS-COUNTERS-SIM-01 | 데이터 추적 | 원시값 및 선택 조건 변경 | 논리 명칭의 입력/출력 관계 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SYS-COUNTERS-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SYS-COUNTERS-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SYS-COUNTERS-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |
| SYS-COUNTERS-V-04 | HMI/통신 | HMI 설정 주소·자료형·가공 상태를 온라인 PLC 값으로 검증 | 확인 대기 |

## SYS-LEGACY · 과거 태그·이름 대응

MN01 속도 감소 참조와 PC03/TR01/FR01/VT01 등 과거 이름을 현재 설비와 대조한다. 이름만으로 장치를 병합하지 않는다. DB 인터페이스 설명 원문은 block_summary.json 및 live_index.json에 보존했다.

자료 상태: 자료에서 확인. 상위: 해당 없음. 전기: 직접 회로 식별 근거 없음.

### PLC 신호

| 주소 | 심볼 | 자료형 | 원본 설명 | 문서 ID |
| --- | --- | --- | --- | --- |
| %M1.2 | riduce mn01 | bool |  | 471 |

### HMI 설정

직접 이름으로 일치한 HMI 태그 미식별.

### 원본 래더 참조

| 블록 | 색인 순서 | 제목 | 원본 연결 | Parts/Wires |
| --- | --- | --- | --- | --- |
| analog output conversion | 6 | rd-01 cylinder | [네트워크 1684](networks/network-1684.html) | 6/16 |
| analog output conversion | 7 | fn-01 ventilator | [네트워크 1685](networks/network-1685.html) | 6/16 |
| auto start motors | 3 | preheating | [네트워크 1843](networks/network-1843.html) | 67/121 |
| auto start motors | 4 | production | [네트워크 1844](networks/network-1844.html) | 60/113 |
| auto start motors | 5 | set points fn01 | [네트워크 1845](networks/network-1845.html) | 24/63 |
| burner control | 11 | reduce speed mn01 se tc01 > 30°c the setpoint | [네트워크 1864](networks/network-1864.html) | 8/19 |
| motors 1 | 7 | rd01 | [네트워크 1936](networks/network-1936.html) | 12/23 |
| motors 1 | 22 | fn01 | [네트워크 1951](networks/network-1951.html) | 11/21 |

### 원본 접점 조건식

원본 접점 경로를 펼친 정적 보조 해석이다. 호출 블록·타이머·에지·다중 쓰기 및 실행 순서는 추가 검증한다.

| 네트워크 | 동작 | 대상 | 정적 조건식 | 내용 |
| --- | --- | --- | --- | --- |
| 1864 | SCoil | Riduce MN01 | ((OFF AND ON) AND [Manage_TC1_2.PID_Ref_Temp >= App02]) | 조건 성립 시 Set |
| 1864 | RCoil | Riduce MN01 | ((OFF AND ON) AND [Manage_TC1_2.PID_Ref_Temp < App03]) | 조건 성립 시 Reset |


### 점검·진단 절차안

1. 논리 명칭 확인: 이 항목이 물리 계기인지 PLC 내부 공학값/루프 이름인지 확인한다.
2. 데이터 추적: 원시 입력→선택/환산→제어 루프→HMI 값을 네트워크와 DB 주소로 연결한다.

### 시뮬레이터 시험 설계

| ID | 상황 | 주입 조건 | 확인할 결과 | 상태 |
| --- | --- | --- | --- | --- |
| SYS-LEGACY-SIM-01 | 데이터 추적 | 원시값 및 선택 조건 변경 | 논리 명칭의 입력/출력 관계 확인 | 설계·미실행 |

### 확인 대장

| ID | 항목 | 작업 | 상태 |
| --- | --- | --- | --- |
| SYS-LEGACY-V-01 | 식별/실물 | 도면 태그·물리 위치·명판을 대조하고 현재 설치/사용 상태 확정 | 확인 대기 |
| SYS-LEGACY-V-02 | 제어/데이터 | 원본 네트워크와 관련 설정·접점 극성·주소를 현재 프로젝트로 대조 | 확인 대기 |
| SYS-LEGACY-V-03 | 시뮬레이션 | 위 시험안의 기대 결과를 원본 실행 결과로 확정하고 실행 증거 기록 | 확인 대기 |

