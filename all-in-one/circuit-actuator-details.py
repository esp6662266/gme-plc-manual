"""Static actuator/burner interface paths from 24 visually reviewed OEM sheets.

These helpers only assemble explicitly transcribed rows from those sheets.
The encoder channel address remains unresolved; no PLC/simulator is changed.
"""
def path(signal,drawing,backup,fg,nodes,destination,check,**extra):
    return dict(signal=signal,drawing=drawing,backup=backup,fg=fg,nodes=nodes,
                destination=destination,check=check,**extra)

def gate_paths(id,outfg,infg,outputs,limits,selectors):
    paths=[]
    for gate,ev,qa,tag,relay,fuse,ret,pin,net in outputs:
        paths.append(path('게이트 '+gate+' 밸브 명령','A'+qa,'%Q'+qa+' / '+tag,outfg,
            [f'FG141: MOD.15 단자{pin} / A{qa}',f'{relay} 코일A1→A2 / -0Vdc10.6',
             f'110Vac9.7 → {relay} 접점1→9',f'X1:{fuse} / 2A F(5×20) → {ev} 코일A1',f'{ev} A2 → X1:{ret} → 0Vac9.9'],
            f'원본 네트워크 {net}는 현장 선택·자동 요청·maintenance의 출력 경로를 포함합니다. 명령은 열림 밸브 구동이며 닫힘 센서와 다른 신호입니다.',
            '24V PLC 명령·릴레이 코일과110Vac 밸브 전원을 구분합니다. 명령/접점/퓨즈/코일/공압·기계 동작/위치 입력을 순서대로 기록합니다. 출력0을 실제 닫힘 완료로 판단하지 않습니다.'))
    for gate,state,ls,ia,tag,fuse,signal,modfg,pin,net,note in limits:
        paths.append(path('게이트 '+gate+' '+state+' 위치','E'+ia,'%I'+ia+' / '+tag,infg,
            [f'+24Vdc10.7 → X1:{fuse} / 2A F(5×20)',f'{ls} 접점13→14',f'X1:{signal} → E{ia}',f'FG{modfg}: MOD.10 단자{pin}'],
            f'원본 네트워크 {net}는 물리 입력·내부 Inputs와 출력 상태를 이용한 MEM_OPEN/MEM_CLOSE의 Set·Reset을 포함합니다. '+note,
            '원시 센서, 출력 명령, 위치 기억, 처리 입력, 알람을 따로 기록합니다. 도면 접점 형식만으로 설치 상태·정상 위치·입력 반전을 확정하지 않습니다.'))
    for gate,ia,tag,fuse,signal,sb,sa,modfg,pin,net in selectors:
        paths.append(path('현장 게이트 '+gate+' 선택','E'+ia,'%I'+ia+' / '+tag,infg,
            [f'+24Vdc10.7 → X1:{fuse} / 2A F(5×20)',f'{sb} PB 접점13→14 → {sa} 게이트{gate} 선택 접점',f'X1:{signal} → E{ia}',f'FG{modfg}: MOD.10 단자{pin}'],
            f'원본 네트워크 {net}는 해당 선택 입력을 Open EV {gate} 00 요청으로 전달합니다. 최종 밸브 명령은 별도 네트워크입니다.',
            '선택 신호는 위치 센서나 PLC 자동 운전 허가가 아닙니다. PB·선택기·PLC 입력·현장 요청·출력의 전달을 분리합니다.'))
    return paths

actuator_devices=[
 dict(id='PV01',title='드럼 투입 이중 게이트',sheets=[69,70,124,125,141],pages=[70,71,125,126,142],
      equipment='FG69의 EV01/EV02는69KA1/2 릴레이를 거친110Vac 구동입니다. FG70의 LS01/02/05/06과 PB15 현장 선택기는24Vdc 입력입니다. 도면 MOD.10 입력·MOD.15 출력 단자를 함께 추적합니다.',
      distinction='LS02는 FG70 배선·FG124 설명표·백업I8.7에 존재하지만 FG124 배선 선에는 SPARE 점선이 있습니다. 현재 실사용은 미확정입니다. 시공도면 LS01–08을 PLC 위치 입력 여덟 개로 자동 확장하지 않습니다.',
      paths=gate_paths('PV01',69,70,
          [('A','EV-01','5.2','pv-01 gate a','69KA1',126,127,13,1915),('B','EV-02','5.3','pv-01 gate b ev','69KA2',128,129,14,1915)],
          [('A','열림','LS-01','8.6','ev01_open',130,131,124,7,1921,'처리된 A 열림 이름은 Inputs.FC GATE A OPEN입니다. 입력→내부 전달의 전체 호출은 확인 전입니다.'),
           ('A','닫힘','LS-02','8.7','ev01_close',132,133,124,8,1921,'FG124 단자8의 배선에는 SPARE 표시가 있어 기존 PV01-LS02 불일치를 유지합니다.'),
           ('B','열림','LS-05','9.0','ev02_open',134,135,125,11,1922,'원본의 False 접점이 들어간 가지와 실제 입력·처리 입력을 구분합니다.'),
           ('B','닫힘','LS-06','9.1','ev02_close',136,137,125,12,1922,'출력0과 닫힘 응답·기억은 별도 상태입니다.')],
          [('A','9.2','ev01_sel_open',138,139,'70SB1','70SA1',125,13,1914),('B','9.3','ev02_sel_open',138,140,'70SB1','70SA1',125,14,1914)]),
      networks=[405,1815,1816,1911,1913,1914,1915,1921,1922],
      pending=['LS02 실제 설치·사용·예비 처리와 FG124/SPARE 확인','시공도면 ENT2TB2/3의 LS01–08과 OEM 네 센서의 실제 연결 대조','원시·Inputs·MEM·HMI 위치의 전체 전달 및 복수 쓰기 확인','PV01 B 출력의 OFF 가지와 ON 상위 조건, maintenance 명령을 실제 정책과 대조','공압 상실·기계 걸림·출력0 이후 실제 복귀 위치·닫힘 시간은 제작사/현장 근거 필요']),
 dict(id='PV02',title='드럼 배출 이중 게이트',sheets=[71,72,125,126,141],pages=[72,73,126,127,142],
      equipment='FG71의 EV04/EV05는71KA1/2 릴레이를 거친110Vac 구동입니다. FG72의 LS25/26/29/30과 PB16 현장 선택기는24Vdc 입력입니다.',
      distinction='PV02 운전 허가·MC04 응답과 출력 밸브·실제 위치는 별도입니다. 시공도면 ROT1TB1의 EV03/04/05 공유 간선에서 EV03은 RD01 윤활 밸브로 분리합니다.',
      paths=gate_paths('PV02',71,72,
          [('A','EV-04','5.4','pv-02 gate a ev','71KA1',141,142,15,1920),('B','EV-05','5.5','pv-02 gate b ev','71KA2',143,144,16,1920)],
          [('A','열림','LS-25','9.4','ev04_open',145,146,125,15,1923,'물리·Inputs 두 가지를 기억 Set 조건에서 확인합니다.'),
           ('A','닫힘','LS-26','9.5','ev04_close',147,148,125,16,1923,'실제 닫힘과 명령 해제를 구분합니다.'),
           ('B','열림','LS-29','9.6','ev05_open',149,150,125,17,1924,'다음 단계 전환과 B 열림 기억을 함께 기록합니다.'),
           ('B','닫힘','LS-30','9.7','ev05_close',151,152,125,18,1924,'실제 닫힘과 명령 해제를 구분합니다.')],
          [('A','10.0','selector op gate a pv-02',153,154,'72SB1','72SA1',126,21,1919),('B','10.1','selector op gate b pv-02',153,155,'72SB1','72SA1',126,22,1919)]),
      networks=[405,1817,1818,1916,1918,1919,1920,1923,1924],
      pending=['시공도면 LS25–32와 OEM 네 위치 센서, 단자·목록 순번 C06 확인','MC04 피드백·유지보수 신호와 게이트 운전 허가의 전체 전달 확인','A/B 게이트 위치·공압·실린더·기억·원시 입력을 시각순으로 대조','전원 재시작의 닫힘 기억 초기화와 실제 위치를 별도로 확인']),
]

def damper(id,fg,sensefg,motor,qa,qc,qtag_a,qtag_c,ia,ic,itag_a,itag_c,la,lc,ltag_a,ltag_c,ls_a,ls_c,term_a,term_c,xs,enc,enc_terms,enc_lines,supply_lines,tmfg,tm_mod,core):
    km1=f'{fg}KM1';km2=f'{fg}KM2';qm=f'{fg}QM1';qs=f'{fg}QS1'
    paths=[]
    for title,qa,tag,km,opposite in [('열기',qa,qtag_a,km1,km2),('닫기',qc,qtag_c,km2,km1)]:
        paths.append(path(title+' 방향 명령','A'+qa,'%Q'+qa+' / '+tag,fg,
          [f'A{qa} → 반대 방향 {opposite} NC 접점31→32',f'{km} 코일A1→A2',f'공통 반환선 → {qm} 보조접점',f'XS:{xs[0]} → {qs} 보조접점 → XS:{xs[1]} → -0Vdc10.6'],
          f'원본{core[0]}의 모드·반대 출력·리미트·고장·교정 조건과 연결합니다. PLC 조건과 하드웨어 반대 접촉기 인터록을 따로 추적합니다.',
          '출력1인데 접촉기가 붙지 않으면 반대 방향 접점과 공통 반환선을 나눠 확인합니다. 접촉기 동작·전력 전달·모터 회전·밸브 이동·위치 입력을 구분합니다.'))
    for title,ia,tag,km in [('열기',ia,itag_a,km1),('닫기',ic,itag_c,km2)]:
        paths.append(path(title+' 접촉기 응답','E'+ia,'%I'+ia+' / '+tag,fg,
          [f'+24Vdc10.7 → {km} 보조접점13→14',f'E{ia} → 해당 PLC 입력 모듈 참조'],
          '방향 접촉기 보조접점 응답입니다. 실제 개도와 끝단 도달은 별도 리미트·엔코더로 확인합니다.',
          '접촉기 응답이1이어도 커플링·감속기·밸브 이동 또는 끝단 위치가 정상이라는 뜻은 아닙니다.'))
    for title,ia,tag,ls,terms in [('열림',la,ltag_a,ls_a,term_a),('닫힘',lc,ltag_c,ls_c,term_c)]:
        dest='원본1070 Part147/151은 MV03_Open/Close를 NOT 처리해 Inputs.MV03 open/Close로 씁니다. 현재 호출·다른 쓰기는 확인 전입니다.' if id=='MV03' else '원본 제어·고장 네트워크의 내부 리미트와 물리 입력의 전체 전달·반전은 추가 확인합니다.'
        paths.append(path(title+' 끝단 위치','E'+ia,'%I'+ia+' / '+tag,sensefg,
          [f'+24Vdc10.7 → X1:{terms[0]} / 2A F(5×20)',f'{ls} 접점11→12',f'X1:{terms[1]} → E{ia}'],dest,
          '이 도면의 위치 접점11/12와 PV 게이트의13/14를 구분합니다. 정상 상태·단선 반응·내부 반전은 실물과 프로그램을 함께 확인합니다.'))
    paths.append(path('엔코더 위치 채널 · 주소 미확정',enc_lines[0],None,sensefg,
        [f'{enc} B(+24V) → X1:{enc_terms[0]} → {supply_lines[0]} → FG{tmfg} 단자9(24VDC)',
         f'{enc} C(0V) → X1:{enc_terms[1]} → {supply_lines[1]} → FG{tmfg} 단자10(M)',
         f'{enc} D → X1:{enc_terms[2]} → {enc_lines[0]} → FG{tmfg} 단자1 CH0.A',
         f'{enc} E → X1:{enc_terms[3]} → {enc_lines[1]} → FG{tmfg} 단자2 CH0.B',
         f'실드 → X1:{enc_terms[4]} → {sensefg}SCH1 / FG{tmfg} 실드·접지 표시',
         f'FG{tmfg}: MOD.{tm_mod}. CH0.N 단자3 연결은 이 도면에 표시되지 않음'],
        '엔코더 읽기·교정·환산 원본을 연결합니다. 주변 E20/21/22의 SPARE 비트는 카운트값 주소가 아닙니다. 실제 TM 구성·채널 주소·DB 대응은 미확정입니다.',
        '엔코더 A/B 위상·분해능·방향·기계 기준·카운트 스케일을 임의로 정하지 않습니다. 리미트 입력·방향 접촉기 응답·엔코더 원시값·환산 개도를 함께 기록합니다.',backup_verified=False,backup_status='address_unresolved',drawing_labels=enc_lines))
    return paths

actuator_devices.extend([
 dict(id='MV01',title='온도 제어 댐퍼',sheets=[44,45,144],pages=[45,46,145],
      equipment='FG44: M20 MV01(도면2.2kW·4.31A),44KM1/2 정·역 접촉기,44QM1·44QS1. FG45의 LS23/24와 ZT02 엔코더를 구분하고 FG144의 TM 채널까지 추적합니다.',
      distinction='열기·닫기 접촉기 응답 I3.2/3.3, 끝단 I8.1/8.2, 엔코더 위치는 세 종류입니다. 접촉기 상호 인터록과 PLC의 반대 출력 조건도 다른 층의 조건입니다.',
      paths=damper('MV01',44,45,'M20','2.4','2.5','start open mv-01','start close mv-01','3.2','3.3','mv01_fbk_opening','mv01_fbk_closing','8.1','8.2','mv01_open','mv01_close','LS-23','LS-24',(112,113),(114,115),(29,30),'ZT-02',(107,108,109,110,111),['45.1','45.2'],['37.1','37.2'],144,16,[1702]),
      networks=[1226,1702,1703,1713,1714,1756,1762,11],
      pending=['현재 방향별 접점·리미트 정상 극성과 내·외부 인터록 확인','TM16의 실제 모델·주소·채널 구성과 ZT02 A/B 신호 대조','TC03 자동제어·수동·교정·고장 경로의 호출·복수 쓰기 확인','시공도면 ZT02의 AI 표기와 OEM 엔코더/TM 채널 관계를 설치 변경 이력으로 확인']),
 dict(id='MV03',title='압력·버너 연동 댐퍼',sheets=[38,39,146],pages=[39,40,147],
      equipment='FG38: M17 MV03(도면2.2kW·4.31A),38KM1/2·38QM1·38QS1. FG39의 LS19/20, ZT04 엔코더와 FG146 TM 채널을 추적합니다.',
      distinction='물리 끝단 입력은 원본1070에서 NOT 처리됩니다. 버너 세정·기동 요청·수동·압력 제어와 위치 센서·접촉기 응답을 혼용하지 않습니다.',
      paths=damper('MV03',38,39,'M17','1.7','2.0','start open mv03','start close mv03','2.4','2.5','mv03_fbk_opening','mv03_fbk_closing','7.5','7.6','mv03_open','mv03_close','LS-19','LS-20',(90,91),(92,93),(25,26),'ZT-04',(85,86,87,88,89),['39.1','39.2'],['35.1','35.2'],146,17,[1706]),
      networks=[1070,1226,1705,1706,1707,1713,1714,1758,1764,1868,15],
      pending=['원본1070의 입력 반전·현재 호출·다른 쓰기와 실물 끝단을 대조','PSH03 제어 명칭·백업 PSH02 주소·센서 소유를 별도로 확인','버너 세정·기동 닫힘 요청과 수동·자동 제어의 우선순위 확인','TM17 실제 모델·주소·채널·엔코더 분해능·교정 기준 확인']),
])
mv06_paths=[
 path('MV02·MV05·MV06 공통 인버터 기동','A1.0','%Q1.0 / start aux inv',31,
      ['A1.0 → 30QM1 보조접점 → 31KA1 코일A1→A2 / -0Vdc10.6',
       'FG30: 30AS1 단자9(+24V) → 31KA1 접점1→9 → 단자12(DI1 START)',
       '30AS1 출력 U2/V2/W2 → 30U1/30V1/30W1 → 각 댐퍼 분기'],
      '공통 인버터 기동으로 MV06 단독 열기/닫기 명령을 대신하지 않습니다. MV02·MV05도 같은 전원 계통입니다.',
      '공통 인버터 전원·명령·응답·고장과 개별 방향 접촉기·모터를 나눠 확인합니다. MV06 한 장치 이름으로 공통 인버터를 병합하지 않습니다.'),
 path('공통 인버터 응답 · 백업 power_ok','E1.4','%I1.4 / mv02_05_06_power_ok',30,
      ['+24Vdc10.7 → 30AS1 단자17','도면 RUNNING 단자19 → E1.4 → FG117/5'],
      '도면은 RUNNING, 백업은 mv02_05_06_power_ok입니다. 공통 계통의 신호 의미와 내부 전달을 확인합니다.',
      '이 응답을 MV06 개도·방향 접촉기 또는 세 모터의 개별 정상 응답으로 쓰지 않습니다.'),
 path('공통 인버터 이상','E1.5','%I1.5 / mv02_05_06_inv_all',30,
      ['+24Vdc10.7 → 30AS1 단자20','도면 ALARM 단자21 → E1.5 → FG117/5'],
      'MV02·MV05·MV06 공통 이상 신호입니다. 현재 알람 극성·내부 반전·장치별 래치 영향은 추가 확인합니다.',
      '공통 인버터 이상과 개별 접촉기·리미트·엔코더 고장을 구분합니다. 세 장치의 후속 정지·최초 원인을 함께 기록합니다.'),
]+damper('MV06',32,33,'M14','1.1','1.2','open mv06','close mv06','1.6','1.7','mv06_fbk_opening','mv06_fbk_closing','6.7','7.0','mv06_open','mv06_close','LS-40','LS-41',(63,64),(65,66),(19,20),'ZT-06',(58,59,60,61,62),['33.3','33.4'],['33.1','33.2'],148,18,[1711])
actuator_devices.append(dict(id='MV06',title='공통 인버터 구동 댐퍼',sheets=[30,31,32,33,148],pages=[31,32,33,34,149],
    equipment='FG30/31: 공통30AS1 ACS355-03E-04A1-4(도면1.5kW). FG32: M14 MV06(도면0.25kW·0.76A),32KM1/2·32QM1·32QS1. FG33/148: LS40/41와 ZT06 엔코더·TM 채널.',
    distinction='공통 인버터 신호, MV06 개별 방향 접촉기, 끝단 리미트, 엔코더 위치를 네 층으로 나눕니다. 시공도면 LS34/35와 OEM LS40/41, 중복 FLO4TB2A 간선 C01은 미확정 상태를 유지합니다.',
    paths=mv06_paths,networks=[1226,1709,1710,1711,1713,1714,1760,1766],
    pending=['MV02·MV05·MV06 공통 인버터 출력·기동/Reset/STO와 개별 분기 확인','LS34/35와 LS40/41 설치 변경·단자·현재 입력 대응 확인','시공도면 FLO4TB2A 중복 식별자 C01와 실제 간선 대조','원본1711 NOT ON과 실제 호출·다른 방향 출력 쓰기 확인','TM18 실제 모듈·주소·채널 및 위치 교정 기준 확인']))

burner_paths=[]
for title,ia,tag,fg,power,ret,pair,relay,pin in [
 ('버너 ON','17.0','burner on',97,372,373,(2,3),'KA40',11),
 ('버너 LOCKOUT','17.1','brurner lock out',97,374,375,(5,6),'KA41',12),
 ('버너 IN MODULATION','17.2','burner on and ok',97,376,377,(8,9),'KA41',13),
 ('가스 최소 압력 접점','17.3','min pressure gas',97,378,379,(11,12),'KA20',14),
 ('가스 최대 압력 접점','17.4','max pressure gas',97,380,381,(14,15),'KA21',15),
 ('공기 최소 압력 접점','17.5','min pressure air',97,382,383,(17,18),'KA30',16),
 ('공기 최대 압력 접점','17.6','max pressure air',98,384,385,(20,21),'KA31',17),
 ('고화염 가스 밸브 삽입 응답','17.7','high flame gas',98,386,387,(23,24),'KA50',18)]:
    burner_paths.append(path(title,'E'+ia,'%I'+ia+' / '+tag,fg,
        [f'+24Vdc10.7 → X1:{power} / 2A F(5×20)',f'버너 전용반 X/6/{pair[0]} → {relay} 접점 → X/6/{pair[1]}',
         f'X1:{ret} → E{ia} → FG133 MOD.12 단자{pin}'],
        '원본1854·1865·1866·1868 등 버너 제어와 관련 원시/Inputs/알람의 전체 전달을 확인합니다. 도면 접점명과 PLC 이름을 별도로 기록합니다.',
        ('압력 접점은 아날로그 압력값·유량값과 다른 신호입니다. ' if '압력' in title else '버너반의 상태 접점과 GME 내부 처리·기억·명령을 구분합니다. 이 접점만으로 전체 연소 상태·안전 시퀀스 완료를 판단하지 않습니다. ')+'단자·신호의 현재 극성·역할은 버너 전용도면010-390과 대조합니다.'))
for title,qa,tag,relay,term1,term2,ext1,ext2,net in [
 ('원격 START/STOP','6.5','rem. start/stop burner','99KA1',388,389,'X/220V','X/1/7',1866),
 ('최대 필터 온도 인터록','6.6','temperature interlock ok','99KA2',390,391,'X/1/2','X/1/4',1856),
 ('버너 알람 리셋','6.7','rst allarm burner','99KA3',392,393,'X/220V','X/1/10',1854),
 ('고화염 기동 요청','7.0','start high flame','99KA4',394,395,'X/5/11','X/5/13',1862)]:
    burner_paths.append(path(title,'A'+qa,'%Q'+qa+' / '+tag,99,
        [f'A{qa} → {relay} 코일A1→A2 / -0Vdc10.6',f'버너측 {ext1} → X1:{term1} → {relay} 접점1→9 → X1:{term2} → {ext2}'],
        f'원본{net}의 명령·래치·시간 조건과 연결합니다. 릴레이 코일 전원과 버너측 접점 회로의 전원은 별도입니다.',
        'PLC 요청을 전용 연소 제어기 시퀀스 완료 또는 화염 확인으로 해석하지 않습니다. 현재 외부 인터록 기능·전압·허가를 전용도면에서 확인합니다.'))
burner_paths.append(path('강제 점화 전환 접점','A7.1','%Q7.1 / foced spark',99,
    ['A7.1 → 99KA5 코일A1→A2 / -0Vdc10.6','버너 X/5/2 → X1:396 → 99KA5 단자1',
     '버너 X/220V → X1:397 → 99KA5 단자5','99KA5 단자9 → X1:398 (외부 종착 단자는 이 FG에서 식별되지 않음)'],
    '원본1863은 Main flame ON 기억과 Tag141을 사용합니다. 도면 제목에는 전환 중3초라고 표시되지만 현재 타이머·전용기능을 별도로 대조합니다.',
    '전환 접점의 역할과 현재 배선은 버너 전용도면을 확인합니다. 일반 PLC의 요청을 점화·가스 안전 시퀀스 전체로 설명하지 않습니다.'))
for title,label,backup,nodes,net in [
 ('가스 서보 위치 전달','+PEW360','%IW360 / br01_gas',
  ['버너 X1/2/1 → X1:399 → +PEW360 (FG111/1)','버너 X1/2/4 → X1:400 → -100.1 (FG111/0)','실드 X1:402 → 100SCH1'],1752),
 ('가스 서보 설정','+PAW308','%QW308 / br01_gas_sp',
  ['+PAW308 (FG114/1) → X1:401 → 버너 X1/2/3','공통·리턴은 FG111/114와 버너 전용도면에서 대조'],1687),
 ('공기 서보 위치 전달','+PEW362','%IW362 / br01_air',
  ['버너 X1/3/1 → X1:403 → +PEW362 (FG111/2)','버너 X1/3/4 → X1:404 → -100.2 (FG111/1)','실드 X1:406 → 100SCH2'],1753),
 ('공기 서보 설정','+PAW310','%QW310 / br01_air_sp',
  ['+PAW310 (FG114/1) → X1:405 → 버너 X1/3/3','공통·리턴은 FG111/114와 버너 전용도면에서 대조'],1686),
 ('가스 유량 FIT2001','±PEW364','%IW364 / br01_flowmeter_gas',
  ['버너 X1/7/1 → X1:407 → +PEW364 (FG111/4)','버너 X1/7/2 → X1:408 → -PEW364 (FG111/4)','실드 X1:409 → 100SCH3'],1754),
 ('공기 유량 FIT3001','±PEW366','%IW366 / br01_flowmeter_air',
  ['버너 X1/7/3 → X1:410 → +PEW366 (FG111/5)','버너 X1/7/4 → X1:411 → -PEW366 (FG111/5)','실드 X1:412 → 100SCH4'],1755)]:
    burner_paths.append(path(title,label,backup,100,nodes,
        f'FG100은4–20mA 표기입니다. 원본{net}의 변환·설정과 관련 DB/HMI 전달을 대조합니다.',
        '물리 전류 신호·PLC 원시값·변환값·HMI 단위·실제 서보 위치/유량을 구분합니다. 범위·환산·최소 위치·공기/가스 비율은 제작사·현재 파라미터 확인 전입니다.'))
actuator_devices.append(dict(id='BR01',title='가스 버너 · 외부 제어 인터페이스',sheets=[97,98,99,100,133],pages=[98,99,100,101,134],
    equipment='FG97/98의24V clean contact 입력8개, FG99의 릴레이 출력5개, FG100의4–20mA 아날로그6개를 추적합니다. 외부 버너반은 도면010-390 TYPE BP N300을 참조합니다.',
    distinction='이 자료는 GME PLC와 버너반 사이 인터페이스입니다. 내부 화염 감시·점화·퍼지·가스 밸브 보호·안전 시간의 전체 회로가 아닙니다. 시공도면의 BR01 간선 A–F를 개별 핀으로 자동 배정하지 않습니다.',
    paths=burner_paths,networks=[1071,1686,1687,1752,1753,1754,1755,1830,1834,1854,1856,1858,1862,1863,1865,1866,1868,1869],
    pending=['버너 전용010-390 도면과 실제 제어기 모델·개정·현재 기능 확보','FG97 LOCKOUT·IN MODULATION 두 접점 모두 KA41 표기: 제작사 도면/실물 대조 전 이름을 수정하지 않음','압력 입력·서보 최소위치·Lockout·버너 ON·Modulation의 정상 극성·전달 확인','원본1854의 APP M10.2·m491·Tag135/136/137와 리셋 펄스·유지 조건 확인','99KA5/X1:398 외부 종착점, 점화 전환 기능·Tag141 현재 설정 확인','시공도면 BR01F 두 행 C02와 외부반 양단 표찰·핀 대조','서보 설정/위치·가스/공기 유량 환산·단위·전용 안전 제어 경계 확인']))
