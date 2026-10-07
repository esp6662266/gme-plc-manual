# PLC 통신 장애 확인 기록

확인 시각 2026년 10월 7일 09시 46분부터 09시 48분 UTC

현재 PC 유선 LAN의 물리 링크가 끊긴 상태다. PC의 Ethernet 3 어댑터는 Disconnected, 링크 속도는 0 bps이며 현재 주소는 169.254.121.54다. 어댑터는 비활성화 상태가 아니며 DHCP는 Enabled다. Wi-Fi는 연결되어 있지만 주소는 192.168.0.60으로 PLC용 유선 연결과 다르다.

PLC 통신 설정 대상은 190.168.200.230이다. 해당 주소에 대한 기존 TCP 세션이 없었고 Ping 3회는 모두 시간 초과였다. SIDIR 서비스는 Running이고 SIDIRECT 프로세스와 InTouch WindowViewer는 실행 중이다.

SQL의 dbo.v_AlarmHistory 조회 결과는 다음과 같다.

| 시각 UTC | 태그 | 상태 | 내용 |
|---|---|---|---|
| 2026-10-07 09:40:01.173 | StatusPLC | UNACK_ALM | PLC comunication FAULT |
| 2026-10-07 09:41:09.507 | StatusPLC | ACK_ALM | PLC comunication FAULT |

09:47 HMI 오른쪽 아래에는 노란색 PLC N.C.가 표시됐다. ACK는 알람 확인이며 통신 복구를 의미하지 않는다. 화면에 남아 있는 운전 상태와 온도·전류는 통신 복구 및 갱신 확인 전까지 현재 설비 상태로 판단할 수 없다.

현장에서 먼저 PC 랜선의 체결, PC LAN 포트의 링크 LED, 상대 스위치 전원과 포트 LED를 확인한다. 현재 자료만으로 특정 케이블 불량, 스위치 고장 또는 PLC 전원 문제를 확정할 수는 없다. 연결이 복구되면 유선 어댑터 Up, 정상 PLC 네트워크 주소, PLC 응답, SIDIRECT TCP 102 세션, HMI 통신 표시와 값 갱신, 알람 복귀 기록을 순서대로 확인한다.

이번 점검에서는 PLC/HMI 프로그램, 네트워크 주소, 통신 서비스, CPU 상태, 알람 Reset을 변경하거나 실행하지 않았다.
