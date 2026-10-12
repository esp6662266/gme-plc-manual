# RD01-FAN · 현재 보존 원본 검토

## 1. 설비·자료 기준

RD01-FAN(드럼 모터 냉각팬)는 실제 대장에서 보조 구동장치으로 분류합니다. 담당 부모는 RD01입니다.

RD01 구동 모터 냉각 보조장치.

OEM FG22/PDF23은 M04 냉각팬, 22QM1 도면 정격1.4-2A, 22KM1·22QS1, A0.2 명령과 E0.4 피드백을 표시합니다. 도면 정격을 현재 보호 설정으로 사용하지 않습니다.

접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다.

Dots 원초안은 abcf31c/v1.12.0 당시 연구 자료이며 원문 바이트를 보존했습니다. 아래는 현재 원본과 독립 대조한 검토본입니다.

## 2. I/O·HMI

RD01-FAN 대장에는 입력·출력·내부 신호 2행과 HMI 설정 3행이 연결됩니다.

- rd01f_fbk — %i0.4 / bool / 원본 문서954; 원본 XML의 SAD/SSD·자료형 및 백업 주소 대응 확인; 같은 이름 LAD 핀 1곳. 원문 설명: feedback motor rd-01f
- start fan rd01 — %q0.2 / bool / 원본 문서1339; 원본 XML의 SAD/SSD·자료형 및 백업 주소 대응 확인; 같은 이름 LAD 핀 2곳. 원문 설명: a 48.6 rd-01f motorcommand
- RD_01_FAN\Allarme1 — DB11,X4.1 / Access Name PLC / 내부 ID 0044B; HMI 설정 주소와 물리 I/O를 구분
- RD_01_FAN\RispostaA — DB11,X4.0 / Access Name PLC / 내부 ID 00326; HMI 설정 주소와 물리 I/O를 구분
- RD_01_FAN\Flag — DB2,X0.2 / Access Name PLC / 내부 ID 001B2; HMI 설정 주소와 물리 I/O를 구분

| 원문 신호 | 백업 주소 | 형식 | 주소 증거 |
| --- | --- | --- | --- |
| rd01f_fbk | %i0.4 | bool | native 선언 일치 |
| start fan rd01 | %q0.2 | bool | native 선언 일치 |

## 3. 제어 구조

접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다.

1939:287은 ON AND Flag.M_RD_01_FAN에서 Start fan RD01을 기록합니다. 1939:283은 전용 고장 또는 R2_GATE_LOOP_ON/STANDBY_ON 허가 부재 및 NOT UNDER TESTING 경로에서 Flag.M_RD_01_FAN 요청을 Reset합니다. 정확한 AND/OR/NOT 묶음을 원본 표로 보존합니다.

1788 SdCoil349 입력은 ON·Start fan RD01·NOT Inputs.fan RD01 run입니다. Tag_55는 ORef364/RID43, S5T#2S는 ORef363/RID28입니다. IEC 호출로 바꾸어 설명하지 않습니다.

- 원시 이름의 핀 참조를 확인한 네트워크: 1020, 1788, 1939. 읽기·쓰기·호출은 원본 Part/Wire/ORef 표로 구분합니다.
- 관련 처리·부모 신호: Flag.M_RD_01_FAN, Inputs.fan RD01 run, Allarm.RD_01_FAN_FAULT, hours motors.RD_01_FAN_HOUR, hours motors.RD_01_FAN_MIN. 관련 신호를 새로운 구성품 전용 제어로 복제하지 않습니다.
- 원본 정적 조건 1939:287 / Coil / Start fan RD01: (ON AND Flag.M_RD_01_FAN); 현재 호출·실행·최종값 확인 전
- 원본 정적 조건 1939:283 / RCoil / Flag.M_RD_01_FAN: ((ON AND Allarm.RD_01_FAN_FAULT) OR (((ON AND NOT [Flag.R2_GATE_LOOP_ON]) AND NOT [Flag.STANDBY_ON]) AND NOT [UNDER TESTING])); 현재 호출·실행·최종값 확인 전

| 고유/관련 원문 이름 | 원본 네트워크 | 명령 UID·Gate·Pin | Wire·ORef | 소유 경계 |
| --- | --- | --- | --- | --- |
| RD01F_Fbk | 1020 | 1264 Contact.operand | 1246 / 1234 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| Start fan RD01 | 1788 | 387 Contact.operand | 372 / 362 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| Start fan RD01 | 1939 | 287 Coil.operand | 305 / 294 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| hours motors.RD_01_FAN_MIN | 1020 | 1216 Add.in1 | 1247 / 1235 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| hours motors.RD_01_FAN_MIN | 1020 | 1216 Add.out | 1249 / 1237 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| hours motors.RD_01_FAN_MIN | 1020 | 1223 Ge.in1 | 1250 / 1238 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| hours motors.RD_01_FAN_HOUR | 1020 | 1226 Move.out1 | 1255 / 1241 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| hours motors.RD_01_FAN_MIN | 1020 | 1229 Move.out1 | 1258 / 1243 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| hours motors.RD_01_FAN_HOUR | 1049 | 2825 Move.out1 | 2853 / 2841 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| Allarm.RD_01_FAN_FAULT | 1788 | 355 SCoil.operand | 378 / 367 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| Allarm.RD_01_FAN_FAULT | 1788 | 395 Contact.operand | 381 / 369 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| Allarm.RD_01_FAN_FAULT | 1788 | 360 RCoil.operand | 383 / 370 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| Flag.M_RD_01_FAN | 1843 | 469 SCoil.operand | 715 / 620 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| Flag.M_RD_01_FAN | 1844 | 817 SCoil.operand | 1077 / 971 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| Flag.M_RD_01_FAN | 1847 | 948 RCoil.operand | 1070 / 1012 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| Allarm.RD_01_FAN_FAULT | 1939 | 309 Contact.operand | 296 / 289 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| Flag.M_RD_01_FAN | 1939 | 283 RCoil.operand | 302 / 292 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |
| Flag.M_RD_01_FAN | 1939 | 315 Contact.operand | 303 / 293 | 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다. |

| 원본 | 명령 UID·동작 | 대상 | 정적 Wire 조건 · 현재 실행 별도 |
| --- | --- | --- | --- |
| 1939 | 287 Coil | Start fan RD01 | (ON AND Flag.M_RD_01_FAN) |

## 4. 전기 전달 경로

선택한 OEM 원본 위치는 FG22/PDF23입니다. 도면 FG와 PDF 페이지를 별도 필드로 유지합니다.

- OEM FG22/PDF23은 M04 냉각팬, 22QM1 도면 정격1.4-2A, 22KM1·22QS1, A0.2 명령과 E0.4 피드백을 표시합니다. 도면 정격을 현재 보호 설정으로 사용하지 않습니다.

## 5. 알람·복구

1788 SdCoil349 입력은 ON·Start fan RD01·NOT Inputs.fan RD01 run입니다. Tag_55는 ORef364/RID43, S5T#2S는 ORef363/RID28입니다. IEC 호출로 바꾸어 설명하지 않습니다.

1788:360 Reset은 RESET_ALLARM과 기존 Allarm.RD_01_FAN_FAULT를 사용합니다. 래치 해제가 실제 팬 복구를 증명하지 않습니다.

접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다.

## 6. 증상별 관찰

RD01-FAN의 원인은 아래 관찰을 실제로 수집한 뒤 원본과 비교합니다. 빈 관찰 양식을 현재 값이나 복구 완료 증거로 채우지 않습니다.

- Q0.2→XS5/6→22QS1/22QM1→22KM1과 I0.4의22KM1 보조 접점
- 원시 RD01F_Fbk·가공 Inputs.fan RD01 run·Allarm.RD_01_FAN_FAULT의 값·시간
- M04의 실제 회전·열 상태는 접촉기 피드백과 별도로 관찰

## 7. 완료·누락·검증

RD01-FAN의 문서·정적 검토 결과와 다음에 필요한 증거를 구분하여 인계합니다.

- 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다.
- 이번 범위는 원본 정적 문서 검토입니다. TIA에서 현재 프로젝트·호출·복수 쓰기·컴파일을 확인하는 작업, 현재 CPU 비교, 실제 현장 시험·복구는 미수행·미확정입니다.
- 시뮬레이터는 영구 중지입니다. 이전 대장의 오프라인 실행·시험 설계 문구를 시뮬레이터 생성·실행 재개 지시로 사용하지 않습니다. 실제 PLC·현장·보호값 변경은 수행하지 않았습니다.

현재 CPU·호출/최종쓰기·실물·정상 극성·현재 승인 설정·TIA 컴파일·현장 복구는 확인 전입니다.

- 접촉기 피드백은 전기 접점 경로이며 모터 회전 증거가 아닙니다. 원시 RD01F_Fbk에서 Inputs.fan RD01 run으로의 직접 전달은 해석되지 않았고1082 가공값 쓰기는 보존된 과거 Simulation 블록의 정적 참조입니다. 해당 블록을 실행하지 않았습니다.
- 이번 범위는 원본 정적 문서 검토입니다. TIA에서 현재 프로젝트·호출·복수 쓰기·컴파일을 확인하는 작업, 현재 CPU 비교, 실제 현장 시험·복구는 미수행·미확정입니다.
- 시뮬레이터는 영구 중지입니다. 이전 대장의 오프라인 실행·시험 설계 문구를 시뮬레이터 생성·실행 재개 지시로 사용하지 않습니다. 실제 PLC·현장·보호값 변경은 수행하지 않았습니다.
