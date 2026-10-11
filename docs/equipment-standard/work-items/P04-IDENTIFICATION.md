# v1.17.0 실제 게시 확인

P04-IDENTIFICATION 문서 게시 확인. feature cf35b18a37727a21a219078e82b230e0c637f26b / Netlify 6acb7aefd0153e00080a6aff ready 2026-10-11T12:03:13.821Z. 미확정/당시 저장·PDF 근거를 아래에 보존한다. 루트 BATCH02-VERIFICATION.json 참고.

# P03/P04/P14 식별 보고서 로컬 검증 · 실제 게시 대기

각7영역의 식별 보고서를 작성하고 기존 식별 작업지에 연결했다. P03 호퍼1과 호퍼2 외부고장, P04 CLIENT-CL18과 BWF02/BC01, P14 숫자2와 서로 다른 CY군·VR/SC/경보/질소 소유를 구분한다. PLC/catalog ID 배정0, 본체 신호/알람/타이머0·실물 동일성 미확정. 후보 parent/원 대장/신호0 양식·미지필드·기존 제외 보존. 2차133 로컬 편입0.

Dots P03 전체60/P04 전체36 고정 Git SHA와 P14 외부 첨부3 SHA 일치. 외부 중복보고서/SC01 초안은 참고이며 원본 자료 또는 현행 실물 증거가 아니다. 독립 의미검토는12선택 XML의 Part/Wire·동일 UID/RID/NID 선언, 원본 PDF19쪽 및 변경 없는 P&ID1/시공3 재사용에 한정한다. 전체 파일 해시 수를 전체 논리검토 수로 세지 않는다.

1280/390 실제6화면·P03 실제 식별버튼→보고서 연결·모든 로컬 링크/anchors 검사 passed. 기존 관찰양식3개 실제 저장/재열기·다른설비 기존기록 보존, 직접 신호0/identity/field false/복구0 유지. 새 설비 표준 프로파일을 만들지 않았으므로 전용4도구 동등 구현으로 합산하지 않는다. 각 A4 PDF2쪽/총6쪽 모두 시각 확인·SHA JSON 보존. 격리 QA3개 제거 후 기록/초안 null. 운영기록 변경0.

정적 문서 complete_with_gaps, TIA/현재 CPU/현장복구 미수행·시뮬레이터/PLC/SEJIN 변경0. 필요한 새 실물/전용 자료가 오면 식별을 재개한다. 실제 게시는 BATCH02 최종 패키지 후 별도 확인한다.

# P04 · 웨잉호퍼배출컨베이어 식별 조사

문서 complete_with_gaps · PLC 미배정 · 실물 동일성 미확정 · 전용 신호/알람/타이머0.

## 식별과 제공 자료

일반 명칭과 LAD425의 bwf02 제목만으로 CLIENT-CL18=BWF02=P04라고 확정하지 않는다. BC01은 기존 P01/SS01 경로로 유지한다. CLIENT-CL17은 인접 외부 입력이다. 부모/자식 관계 및 PLC 태그를 새로 배정하지 않는다.

## 별도 물리 입력·처리응답

0235/NID18의 0599 RID40 UID359/361, HOPPER CONVEYOR 2FAULT, SAD Input AO133=I16.5. 0601 RID41 UID360/363는 Allarm.motor_client_18_fault AO130 쓰기다. BWF02의 처리 RUN/Fault DB, Q6.3 Consent Start와 다른 채널이다. 현행 정상 극성·외부반 Ready/Run/Fault의 주체는 미확정.

## 요청·허가·실제 Run

BWF02 LAD1933 OR135→Wire176→R147 M_BWF02; 별도 ON183→접점197→Wire198→Coil151 Q6.3. 여섯 요청 해제 조건에 Local Disable_Load_RD01과 NOT 처리 BC01 run이 포함된다. P04 기동 출력으로 배정하지 않는다. 외부반 내부 Reset→요청→허가→실제 Run의 순서와 다른 쓰기는 미확보.

## 고장 입력과 시공의 한계

FG94/PDF95: +24Vdc10.7→X1:352(2A F)→외부 접점→353→E16.5. FG132/PDF133 MOD12 단자6 HOPPER CONVEYOR 2FAULT. 외부 모터/인버터/접점/케이블 양끝은 미확보다. 시공21/51 BC01 M02를 P04 회로로 복제하지 않는다. PDF50 CANDC-CONS-G002-050 표기법과 예시, PDF51 실제 목록을 구분한다. PDF53의3_5 검은 가림은 활성 배선으로 복원하지 않는다.

## CLIENT와 BWF 고장 소유

LAD425: ON373 AND Fault375→S352; ON373 AND NOT Fault377 AND RESET379→R357. 타이머·기동 출력은 이 네트워크에 없다. 별도 BWF02 LAD1783: ON193→Consent195→NOT 처리RUN210→SD147 Tag50 S5T#10S; 허가+타이머+NOT RUN 또는 허가+처리Fault가 고장 Set156. Reset162는 ON/RESET/자기래치/NOT 처리Fault다. Tag50의 Timer AO121과 상수 저장4352는10초이며 P04 보호값으로 배정하지 않는다.

## 식별에 필요한 자료

본체·모터·감속기 명판, 전용 기동반/VFD 표시, 케이블번호·양단 단자, 상하류 경로 사진, Ready/Run/Fault/허가의 소유·정상 극성이 필요하다. 자료명 일치만으로 현재 사용·실물 대응·안전 재기동을 확정하지 않는다.

## 증상에서 관찰할 순서

미기동: 실물 ID→자기 기동반/VFD 최초 상태→명령과 실제 Run 구분→상하류 허가/Fault 변화→확인된 케이블/단자 비교. 운전 중 강제출력이나 보호값 조정을 제안하지 않는다. 기존 신호0 관찰 양식과 미지 필드를 유지한다.

검토는 위 선택 원본/핀과 PDF에 한정한다. Dots 전체 첨부 해시 수를 전체 의미검토 수로 세지 않는다. 원본/기존 완료/관찰양식/미지필드/중지5 보존. UI/PDF/공통 패키지/실제 게시 확인은 별도 기록한다.
