# RD01·PV03 초안 정정 보강 — 2026-10-11

## 적용·보존 범위

원본 저장소 고정 커밋 `abcf31c5030bc7ef8749ed8e869a857f2387a28a` / v1.12.0을 기준으로 한 문서 정정이다. 앞서 전달한 RD01-DOTS-DRAFT.md·PV03-DOTS-DRAFT.md는 수신 원문으로 보존한다. 아래 정정이 해당 문장의 기존 해석에 우선하며 원본 XML/PDF, 공통 코드, 버전, 대장, 게시 및 운영기록을 수정하지 않는다. 현재 CPU·실물·정상극성·현행 보호설정·현장복구는 미확정이다.

사용자 독립 검토 보고(2026-10-11 18:35 KST)의 RD01 정정을 받은 뒤 원본 도면 두 쪽과 전류 입력 선언을 조사 쪽에서도 제한 재대조했다. 같은 도면을 인용한 PV03에서 추가 오독 한 건을 찾아 함께 정정한다.

## 1. RD01 21KA2 코일 리턴과 EV03 부하 리턴

- 출처: `all-in-one/sources/Electrical_Rev2.pdf`, FG21/PDF22.
- 정확한 코일 경로: `A5.1 → 21KA2 A1 → 코일 → A2 → −0Vdc10.6`.
- 정확한 EV03 부하 경로: `110Vac9.7 → 21KA2 접점5–9 → 21.3 → X1/50(2A F) → 21.4 → EV03 → X1/51 → 0Vac9.9`.
- 코일 A2의 수직선은 0Vac9.9 수평선을 지나지만 그 교차에 접속점이 없다. 아래 −0Vdc10.6 수평선에는 접속점이 있다. 공간적으로 가까운 교차와 실제 접속을 구분한다.
- 철회: 기존 초안 요약6·전기회로 설명·E21의 ‘21KA2 코일 A2가 0Vac9.9에 연결’, 그로 인한 원본 코일 귀로 상충 주장.
- 미확정: 실제 배선·릴레이 명판·현행 전압 및 접점 동작은 별도 현장 자료가 필요하다. 이 정정은 원본 도면 판독 정정이며 현장 결선 변경 지시가 아니다.

## 2. RD01 A5.1 교차참조

- 출처: 같은 PDF FG141/PDF142, CPU515/MOD15 도면.
- `A5.1 / EV-03 VALVE COMMAND / 단자12 → 교차참조21/5`.
- 인접 `A5.0 / ER-01 ELECTRICAL RESISTANCE COMMAND / 단자11 → 66/4`는 ER01 소유다.
- 철회: 기존 RD01 초안의 A5.1→66/4 서술과 그에 따른 FG21/FG66 교차참조 상충 주장.
- 정확한 해석: A5.1은 RD01 윤활밸브 EV03, A5.0은 ER01 히터 명령으로 분리한다. 도면 표기만으로 현재 CPU 모델/현장 배선을 확정하지 않는다.

## 3. FG141 개정란: RD01·PV03 공통 정정

- 실제 footer: **Rev2 / 17.03.2025**, 기본 도면 날짜 **27.05.2024**와 구분한다.
- RD01: 기존 개정 목록에서 FG141을 공란으로 분류한 문장을 철회한다. 다른 페이지의 개정 판정은 이번 정정만으로 바꾸지 않는다.
- PV03: §4의 FG141/PDF142 설명 중 ‘이 시트 개정란은 공란’을 **‘이 시트는 Rev2 17.03.2025이며 기본 도면 날짜는27.05.2024’**로 정정한다.
- PV03 A5.6/EV06 단자17→73/3의 명령 끝점과 FG73의 실제 EV 부하 접점5–9는 이 정정으로 바뀌지 않는다. FG73의 개정란 판정도 FG141과 별개다.
- 해석 경계: PDF 파일명 Rev2를 모든 페이지에 일괄 적용하지 않으며, 반대로 인접 페이지 공란을 FG141로 복제하지 않는다.

## 4. RD01 IW332와 PIW332 접근 방식 분리

| 원본 경로 | 선언·핀 | 정확한 접근·전달 |
|---|---|---|
| `0398-FlgNet.xml`, LAD1071/NID2 | Move144.in W157/ORef148; `0627-IdentXmlPart.xml` SimpleAccess RID105, NID2/UID148, RD01_Current, Int, Input AO2656, **SAM=None** | **IW332**를 읽어 Move144.out1 W159/ORef149 → Inputs.RD01_ABSORBPTION(DB13.DBW64) |
| `0519-FlgNet.xml`, LAD1771/NID38 | Signal linearization CRef1496.Analog_input W1511/ORef1504; `0678-IdentXmlPart.xml` SimpleAccess RID285, NID38/UID1504, RD01_Current, Int, Input AO2656, **SAM=Peripherie** | **PIW332**를 직접 읽는 별도 선형화 경로 → OutValue W1514/ORef1507 Data.Amp_RD01(DB1.DBW100) |

두 선언의 비트 오프셋은 모두2656(바이트332)이나 접근 모드가 다르다. 기존 초안의 ‘rawPIW332→DB13W64’ 요약은 **IW332→DB13W64**로 정정하고, PIW332→선형화→DB1W100과 분리한다. 같은 태그 문자열·바이트주소 때문에 읽기 시점과 값까지 항상 같다고 보장하지 않는다. 현재 프로세스 이미지 갱신 설정·실행 시점·계수/영점·인버터 AO2 기능·전류 단위/교정은 추가 자료가 필요하다.

## 5. 검토 결과와 적용 순서

1. 앞서 받은 두 원초안과 원본 파일을 보존한다.
2. RD01 핵심요약·전기회로·E21·증상표·개정표·전류 신호표의 해당 설명을 이 보강에 맞춰 정정한다.
3. PV03의 FG141 개정란 한 문장을 정정한다. 동일 시트를 참조하는 새 ER01 초안에는 Rev2와 A5.0→66/4를 이미 반영했다.
4. 로컬 담당자의 독립 검토·통합·게시 경계는 유지한다. 이 보강은 게시 완료나 실제 현장 검증 수를 늘리지 않는다.
5. 원본의 의미 불명/미결속과 단순 판독 오독을 구분한다. 철회한 오독을 향후 ‘원본 상충’으로 다시 인용하지 않는다.

## 6. 원본 SHA256

경로는 고정 저장소 루트 기준. 아래 해시는 바이트 무결성 증거이며 파일 전체 의미 검토 완료를 뜻하지 않는다.

| 경로 | SHA256 |
|---|---|
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` |
| `all-in-one/sources/decoded-original/0519-FlgNet.xml` | `94c35aac42f54a7b8e4bcb8b8c88d59118e003f483cc49fb447854c682508fa9` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` |
