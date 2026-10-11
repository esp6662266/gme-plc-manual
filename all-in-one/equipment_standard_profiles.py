"""Equipment-specific display profiles over preserved static evidence, no simulation."""
from pathlib import Path
import json,hashlib
import xml.etree.ElementTree as ET

def build_static_profile(root,data,source_rows,config):
    catalog_id=config["catalog_id"]
    key=config.get("selection_key") or config["priority_key"]
    prefix="gme-"+catalog_id.lower()
    def read(file):return json.loads((root/file).read_text(encoding='utf-8'))
    spec=next(p for p in read('registers/control-spec.json')['specifications'] if p['id']==catalog_id)
    alarm=config.get('alarm_reference')
    if alarm is None:alarm=next(p for p in read('registers/alarm-recovery.json')['profiles'] if p['id']==catalog_id)
    regulation=next((p for p in read('registers/regulation-manual.json')['loops'] if p['id']==catalog_id),None)
    control_reference=config.get('control_reference',regulation)
    assert control_reference is not None,(catalog_id,'reviewed control reference required')
    completion=config.get('completion')
    if completion is None:completion=next(p for p in read('registers/requirements-audit.json')['priority_open_work'] if p['key']==key)
    repair=config.get('repair')
    if repair is None:repair=next(p for p in read('registers/repair-decision.json')['records'] if p['key']==key)
    form=next(p for p in data['repair_record_forms']['profiles'] if p['key']==key)
    drawing=next(p for p in data['drawing_workspace']['profiles'] if p['key']==key)
    signal_trace=config.get('signal_reference')
    if signal_trace is None:signal_trace=next(p for p in read('registers/signal-trace.json')['devices'] if p['id']==catalog_id)
    networks={p['document_id']:p for p in read('sources/decoded-original/network-map.json')}
    allowed={}
    def add(network,kind,uid):allowed.setdefault(int(network),set()).add((kind,str(uid)))
    for rule in spec['direct_rules']:
        if not config.get('reviewed_native_only'):add(rule['네트워크 문서'],'part',rule['Part UID'])
    for entry in alarm['timers']+[a for group in alarm['alarms'] for a in group['actions']]:
        add(entry['network'],entry.get('location_kind','part'),entry['uid'])
        for part in entry.get('native_upstream',{}).get('parts',[]):add(entry['network'],'part',part)
        for ref in entry.get('native_upstream',{}).get('reference_pins',[]):add(entry['network'],'wire',ref['wire'])
    for network,kind,uid in config.get('extra_locations',[]):add(network,kind,uid)
    for pair in config['source_pairs']:add(pair['network'],pair.get('kind','part'),pair['uid'])
    for signal in signal_trace['signals']:
        if signal['name'].startswith(('Inputs.','Flag.','Stop_')) or signal['name'] in config['internal_names']:
            for use in signal['usages']:add(use['network'],'wire',use['wire'])
    sources=['registers/control-spec.json','registers/alarm-recovery.json','registers/regulation-manual.json',
             'registers/electrical-trace.json','registers/construction-reference.json','registers/construction-review.json',
             'registers/repair-decision.json','registers/repair-record-forms.json','registers/requirements-audit.json',
             'registers/signal-trace.json','registers/hmi-transfer.json','registers/vendor-reference-review.json',
             'registers/plc-symbols.csv','sources/hmi_plc_tags.csv','sources/Electrical_Rev2.pdf',
             'sources/Electrical_Can_Decoating_20241118.pdf','sources/PID_1684n002I.pdf','sources/decoded-original/network-map.json']
    sources.extend(config.get('extra_sources',[]))
    # Hash original XML and all declarations in the reviewed network scope.
    native_ids=set(allowed)|set(control_reference['native'])
    if not config.get('reviewed_native_only'):native_ids.update(int(n['문서 ID']) for n in spec['networks'])
    for number in sorted(native_ids):
        n=networks[number];sources.append('sources/decoded-original/'+n['xml_file'])
        for operand in n['resolved_operands'].values():sources.extend('sources/decoded-original/'+f for f in operand.get('identifier_files',[]))
    locations=[]
    ns={'s':'http://www.siemens.com/automation/Openness/SW/NetworkSource/FlgNet/v1'}
    # Resolve the namespace from the original; no PLC/model evaluation.
    for number,rows in sorted(allowed.items()):
        n=networks[number];file='sources/decoded-original/'+n['xml_file'];xml=ET.parse(root/file).getroot();ns={'s':xml.tag.split('}')[0][1:]}
        for kind,uid in rows:
            assert any(p.get('UId')==uid for p in xml.findall('s:Parts/s:Part' if kind=='part' else 's:Wires/s:Wire',ns)),(number,kind,uid)
        path=root/f'networks/network-{number}.html';text=path.read_text(encoding='utf-8');parser=source_rows(text,rows,prefix=prefix);parser.feed(text)
        assert parser.found==rows,(number,rows-parser.found)
        for pos,length,value in sorted(parser.edits,reverse=True):text=text[:pos]+value+text[pos+length:]
        style='<style id="'+prefix+'-source-locations">tr[id^="'+prefix+'-"]{scroll-margin-top:65px}tr[id^="'+prefix+'-"]:target td{background:#e0f2e9!important;outline:1px solid #167769}</style>'
        if 'id="'+prefix+'-source-locations"' not in text:text=text.replace('</head>',style+'</head>',1)
        if text!=path.read_text(encoding='utf-8'):path.write_text(text,encoding='utf-8')
        locations.extend(dict(network=number,kind=kind,uid=uid,path=f'networks/network-{number}.html#{parser.anchors[(kind,uid)]}',xml=file) for kind,uid in sorted(rows))
    pairs=config["source_pairs"]
    for pair in pairs:
        match=next((s for s in locations if s['network']==pair['network'] and s['kind']==pair.get('kind','part') and s['uid']==pair['uid']),None)
        pair['path']=match['path'] if match else f"networks/network-{pair['network']}.html"
    hashes={file:hashlib.sha256((root/file).read_bytes()).hexdigest() for file in sorted(set(sources))}
    profile=dict(priority_key=config['priority_key'],catalog_id=catalog_id,type=config['type'],version=1,
        scope='preserved '+catalog_id+' analysis linked to seven areas; no new PLC execution or field claims',
        tools=dict(sources=True,restore=True,compare=True,report=True),sections=['overview','io','control','circuits','alarms','repair','completion'],
        specification=spec,signal_trace=signal_trace,alarm=alarm,regulation=regulation,control_reference=control_reference,completion=completion,repair=repair,
        presentation=config['presentation'],internal_names=config['internal_names'],
        source_pairs=pairs,source_locations=locations,source_hashes=hashes,
        source_bundle_sha256=hashlib.sha256(json.dumps(hashes,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        field_verified=False,tia_verified=False,repairs_completed=0,
        related_alarm_boundary=config['related_alarm_boundary'])
    if config.get('selection_key'):profile['selection_key']=key
    if config.get('reviewed_sections'):profile['reviewed_sections']=config['reviewed_sections']
    return profile


def build_fn04_profile(root,data,source_rows):
    pairs=[
      dict(signal='기동 명령',network=1965,uid='1014',label='최종 출력 · Start FN04',boundary='ON·요청 → Q17.1과 공통 인버터·두 모터 회로를 비교합니다. 출력1만으로 두 모터 운전을 확정하지 않습니다.'),
      dict(signal='운전 응답',network=1809,uid='1114',label='처리 응답 · Inputs.FN04 Run',boundary='I28.2 원시 응답과 Inputs.FN04 Run의 전달·정상 극성·현재 CPU 대응은 확인 전입니다.'),
      dict(signal='인버터 이상',network=1809,uid='1118',label='처리 입력 · Inputs.FN04_All_inv',boundary='I28.3 원시 입력과 처리 신호를 구분합니다. 공동 인버터 RO·현재 극성은 확인 전입니다.'),
      dict(signal='속도 설정',network=1689,kind='wire',uid='875',label='속도 출력 · FN04_SP',boundary='5/100 제한·×272 출력과 QW336→AI1 전달을 비교합니다. 실제 환산·현재 인버터 파라미터·복수쓰기 최종값은 확인 전입니다.'),
      dict(signal='전류 전달',network=1770,kind='wire',uid='1491',label='전류 입력 · 별도 범위 오류',boundary='IW394→환산/범위 오류와 AO2 전달을 비교합니다. 공동 인버터 전류를 각 모터 개별 전류로 적용하지 않습니다.')]
    return build_static_profile(root,data,source_rows,dict(
        catalog_id='FN04',priority_key='P02',type='motor_fan',source_pairs=pairs,
        extra_locations=[(1689,'wire','875'),(1770,'wire','1491'),(1770,'wire','24')],
        internal_names=['Stop_Fan_FN04','Data.SET_PERC_FN04','Data.FN_04_ASPIRATOR'],
        related_alarm_boundary='직접 FAULT/INV2개와 공유17초 감시를 구분합니다. 1964의 Prealarms_FN04/90분 Local 정지와1770 전류 범위 오류는 별도 근거입니다. 설정0 요청 해제와5/100 제한을 현재 실행 오류로 단정하지 않습니다.',
        presentation=dict(identity_title='팬·공동 구동부와 설비 식별',identity_pending='명판·위치·두 모터/설비 카드 관계 확인 전',
            oem_baseline='Electrical_Rev2.pdf · FG59/60 = PDF60/61 · 원본 개정/현재 승인 자료 대조',
            construction_baseline='Electrical_Can_Decoating_20241118.pdf · FOR APPROVAL / first draft design · C05 미해소',
            control_title='PC01 비교·속도 설정과 복수 쓰기',control_links=[['조절 루프 근거','regulation-manual.html#loop-FN04'],['설정·전원 복귀','recipe-settings.html#profile-P02']],
            timer_title='공유 Tag_74 · S5T#17S 감시',related_title='별도 예비알람·90분 정지·범위 오류',
            related_links=[['별도1964 근거','networks/network-1964.html'],['별도1770 근거','networks/network-1770.html'],['관련 명세','control-specs/FN04.html#fault']],
            field_title='실물·두 모터 분기와 정상 극성',alarm_recovery='Set/Reset 연결은 현재 호출 순서·알람 해제·모터 운전의 증명이 아닙니다. 최초 알람 시각과 원인, 요청 Reset/새 요청·출력·두 모터 응답을 같은 시각에 대조합니다.',
            search_examples='Q17.1, Tag_74, S5T#17S, PC01')))

def build_fn01_profile(root,data,source_rows):
    read=lambda file:json.loads((root/file).read_text(encoding='utf-8'))
    spec=next(p for p in read('registers/control-spec.json')['specifications'] if p['id']=='FN01')
    writes=[r for r in spec['scoped_rules'] if r['네트워크 문서']=='1845' and r['대상']=='Data.SET_PERC_VT01']
    assert [r['Part UID'] for r in writes]==['60','65','70','74','78']
    control=dict(applicability='own regulation loop not identified; reviewed recipe/output paths apply',
        chain=['FN01 전용 조절 루프는 보존 regulation-manual 대장에 없습니다. FN04의 PC01 압력 조절을 복제하지 않습니다.',
            '1845: Move60/65/70/74는 HMI 1~4단계 속도, Move78은 원문15를 Data.SET_PERC_VT01에 씁니다. enable은 LRef58/63/68/72/76.Q로 미해석입니다.',
            '1685: 하한5·상한100 쓰기와 ×272→FN01_SP_SPEED(%QW292) 경로를 구분합니다. 호출 순서·복수쓰기 최종값·전기 환산은 현재 자료 확인 전입니다.',
            '1951: 설정0은 요청 Reset 분기입니다. NOT UNDER TESTING은 HYDROGEN_BOX_FAULT 분기에만 적용하며 다른4분기를 포함한 전체 반전으로 해석하지 않습니다.'],
        repair=['설정 요청·제한 쓰기·원시 출력·인버터 입력/표시를 같은 시각에 비교합니다.',
            'Simulation1084의 요청→처리 응답은 보존 원본의 정적 참조입니다. 물리 입력 전달·현장 응답의 증거로 사용하지 않으며 실행하지 않습니다.'],
        pending=['1845 LRef.Q 호출/타이머 인스턴스·HMI 이벤트 및 전체 쓰기 순서',
            '실제 인버터 AI1 모드·현재 스케일·정상 극성·전기 측정·주팬/냉각팬 식별',
            'TC04 %IW256 / TC05 %IW260 / reserved tc05 %IW262 및 범위 문구 상충'],
        native=[1845,1685,1951],native_refs=writes)
    pairs=[
        dict(signal='기동 명령',network=1951,uid='689',label='최종 출력 · Start FN01',boundary='ON·Flag.M_FN_01→Q2.7·48KA1·47AS1 DI1을 비교합니다. M22 주팬과 별도 M29 냉각팬을 구분합니다.'),
        dict(signal='운전 응답',network=1798,uid='740',label='처리 응답 · Inputs.FN01 Run',boundary='I3.5 원시 응답과 처리 Inputs를 구분합니다. Simulation1084는 물리 전달 증명이 아니며 현재 CPU·정상 극성 확인 전입니다.'),
        dict(signal='인버터 이상',network=1798,uid='744',label='처리 입력 · Inputs.FN01_All_Inv',boundary='I3.6 원시 입력과 내부 감시를 구분합니다. 도면 RO·현재 극성·원시→처리 전달 확인 전입니다.'),
        dict(signal='속도 설정',network=1685,kind='wire',uid='504',label='속도 출력 · FN01_SP_SPEED',boundary='SET_PERC_VT01의5/100 제한·×272→QW292 경로를 보존합니다. 실제 환산·AI1 모드·복수쓰기 최종값은 확인 전입니다.'),
        dict(signal='전류 전달',network=1772,kind='wire',uid='1531',label='전류 환산 · 별도 범위 오류',boundary='IW334→Data.Amp_FN01 환산/Absorbption_OFR와1071 Inputs.FN01_ABSORPTION 전달을 분리합니다. AO2 기능·단위·현재 파라미터는 확인 전입니다.')]
    extra=[(1772,'wire','24'),(1950,'part','656'),(1988,'part','857')]+[(1845,'part',r['Part UID']) for r in writes]
    extra += [(1845,'wire',uid) for uid in ['129','140','151','159','167']]
    return build_static_profile(root,data,source_rows,dict(catalog_id='FN01',priority_key='P15',type='motor_fan',source_pairs=pairs,extra_locations=extra,
        internal_names=['Stop_Fan_FN01','Data.SET_PERC_VT01','Data.Amp_FN01'],control_reference=control,
        related_alarm_boundary='直接 FAULT/INV2개는 공유Tag_63 S5T#2S 감시입니다. 1950의 TC04/TC05·ZT01·VR01/VR02 예경보와Tag_122 S5T#1H_30M/Local Stop_Fan_FN01,1988의 OFF·진동Tag_110 S5T#10S,1772 전류 범위 오류는 별도 근거입니다. 시간 설정을 현재 실제 정지·정상 극성·수리 완료로 확정하지 않습니다.'.replace('直接','직접'),
        presentation=dict(identity_title='주팬·별도 냉각팬과 설비 식별',identity_pending='명판·위치·M22 주팬과 M29 냉각팬 SPARE/설비 카드 관계 확인 전',
            oem_baseline='Electrical_Rev2.pdf · 주팬 FG47/48 = PDF48/49, 냉각팬 SPARE FG54 = PDF55, TC05 FG79/104 = PDF80/105',
            construction_baseline='Electrical_Can_Decoating_20241118.pdf · FOR APPROVAL / first draft design · PDF4/5/6/33/51/58 · M22/M29·TC04/05와 가려진 단자 상충 유지',
            control_title='속도 레시피·제한·미해석5쓰기와 제어 경계',control_links=[['설정·전원 복귀','recipe-settings.html#profile-P15'],['원본 설정1845','networks/network-1845.html']],
            timer_title='공유 Tag_63 · S5T#2S 기동 감시',related_title='별도90분 정지·OFF 진동·전류 범위 오류',
            related_links=[['예경보/Local 정지1950','networks/network-1950.html'],['진동/OFF1988','networks/network-1988.html'],['전류1772','networks/network-1772.html'],['관련 명세','control-specs/FN01.html#fault']],
            field_title='실물·주팬/냉각팬SPARE·TC05와 정상 극성',alarm_recovery='Set/Reset 연결은 현재 호출 순서·알람 해제·모터 운전의 증명이 아닙니다. 2초 기동 감시와90분 Local 정지·설정0·수소박스 분기를 구분하고 요청·출력·주팬 응답을 같은 시각에 대조합니다.',
            search_examples='Q2.7, Tag_63, S5T#2S, SET_PERC_VT01, TC05')))

def build_fn02_profile(root,data,source_rows):
    read=lambda file:json.loads((root/file).read_text(encoding='utf-8'))
    spec=next(p for p in read('registers/control-spec.json')['specifications'] if p['id']=='FN02')
    vt02=next(p for p in read('registers/regulation-manual.json')['loops'] if p['id']=='VT02')
    assert vt02['priority']=='P16' and vt02['controller_evidence'] is None
    writes=[r for r in spec['scoped_rules'] if r['대상']=='Data.Set_Perc_VT02' and r['네트워크 문서'] in ['1843','1844','1688']]
    assert {r['rule_id'] for r in writes}=={'1843:495','1844:881','1688:627','1688:635'}
    control=dict(vt02)
    control.update(applicability='preserved VT02/FN02 loop; indexed PID text, native controller evidence absent',
        chain=['VT02/TC03→FN02 출력의 보존 조절 자료입니다. PID는 검색색인 텍스트이며 원본 제어기 실행명령 근거는 미확보입니다. 현재 제어기·빈핀 기본값·실행 결과를 확정하지 않습니다.']+vt02['chain']+[
            '원본8은 TC03_SETPOINT<200이면200을 씁니다. 검색색인9의 실제 -15와30°C 주석은 상충하며 원본 실행명령으로 단정하지 않습니다.',
            '1843 예열 종류1/카운터24의 Move495는75,1844 생산 종류2/카운터52의 Move881은80을 Set_Perc_VT02에 씁니다. 단계 수치는 실제 초가 아닙니다.',
            '1843 카운터33의 FN02 요청 Reset539에는 추가 OFF 접점794가 있습니다. 현재 OFF 값·호출·다른 쓰기 없이 의도나 실행 결과를 확정하지 않습니다.',
            '1948 설정0은 Flag.M_FN_02 요청 해제 분기입니다. 1688의5/100 제한·PID 하한35·예열75/생산80은 서로 다른 쓰기·단계입니다.',
            '1767은 FN02_Current→Data.FN_02_FAN 환산과 FN02_Absorbption_OFR입니다. 1071은 원시 FN02_Current→Inputs.FN02_ABSORPTION 전달로 환산값 전달과 구분합니다.',
            '1770 제목 fn-02 aspirator는 실제 FN04_Current·FN04 계수/출력/OFR을 사용합니다. 이름만으로 FN02 전류 환산에 배정하지 않습니다.'],
        repair=vt02['repair']+['설정값 전체 쓰기·QW306·AI1 전기 신호·인버터 표시와 요청 해제 시각을 비교합니다.',
            'Simulation1084의 Flag.M_FN_02→Inputs.FN02 Run은 보존 원본 정적 참조이며 물리 입력 전달의 증명이 아닙니다. 실행하지 않습니다.'],
        pending=vt02['pending']+['원시 I3.0/I3.1→처리 Inputs의 전달·정상 극성·현재 CPU/HMI 이벤트',
            '예열/생산/제한/PID/HMI 전체 쓰기 순서·최종값·단위·인버터 AI1/AO2 파라미터',
            '기동 심볼의 과거 a52.0 주석은 도면 A2.3/Q2.3 주소와 구분; HMI1192 피연산자8개 미해석 유지',
            'FG42의17KA2 DI3 RESET·14KA2/14KA6 STO 경로는 보존 도면; 현재 PLC 주소·안전 기능 검증 전'],
        native=sorted(set(vt02['native']+[1843,1844,1767,1770])),native_refs=vt02['native_refs']+writes)
    pairs=[
        dict(signal='기동 명령',network=1948,uid='596',label='최종 출력 · Start FN02',boundary='ON·Flag.M_FN_02→Q2.3·43KA1·42AS1 DI1을 비교합니다. Set_Perc_VT02=0 요청 해제와 전기 전달을 구분합니다.'),
        dict(signal='운전 응답',network=1796,uid='655',label='처리 응답 · Inputs.FN02 Run',boundary='I3.0 원시 응답과 처리 Inputs의 반전 감시 접점을 구분합니다. Simulation1084는 물리 전달 증명이 아니며 현재 CPU·극성 확인 전입니다.'),
        dict(signal='인버터 이상',network=1796,uid='662',label='처리 입력 · Inputs.FN02_All_Inv',boundary='I3.1 원시 입력과 내부 감시를 구분합니다. 도면 ALARM/RO·현재 극성·원시→처리 전달 확인 전입니다.'),
        dict(signal='속도 설정',network=1688,kind='wire',uid='671',label='속도 출력 · FN02_SP',boundary='Set_Perc_VT02의5/100 제한·×272→QW306을 보존합니다. PID 하한35·예열75/생산80·설정0 해제와 최종 쓰기를 구분합니다.'),
        dict(signal='전류 전달',network=1767,kind='wire',uid='1471',label='FN02 전류 환산 · 별도 원시 전달',boundary='IW328→Data.FN_02_FAN/OFR과1071 원시→Inputs 전달은 별도입니다. 제목 FN02인1770의 실제 FN04 전류를 혼입하지 않습니다.')]
    extra=[(1767,'wire','24'),(1767,'wire','1474'),(1770,'wire','1491'),(12,'part','362'),(12,'wire','372'),(8,'part','32'),(1843,'part','794'),(1843,'wire','31')]
    extra.extend((int(r['네트워크 문서']),'part',r['Part UID']) for r in writes)
    return build_static_profile(root,data,source_rows,dict(catalog_id='FN02',priority_key='P16',type='motor_fan',source_pairs=pairs,extra_locations=extra,
        extra_sources=['sources/live_index.json'],internal_names=['Data.Set_Perc_VT02','Data.FN_02_FAN'],control_reference=control,
        related_alarm_boundary='직접 FAULT/INV2개는 공유Tag_61 S5T#2S 감시입니다. 1767 전류 범위 오류·1071 원시 전달,설정0 요청 해제·예열 추가OFF·VT02 색인 PID/수동 조건은 별도입니다. 1770은 제목 FN02이나 실제 FN04 신호이며 현재 실행·복구·정상 극성을 확정하지 않습니다.',
        presentation=dict(identity_title='열회수 블로어·단일 모터와 설비 식별',identity_pending='명판·위치·M19 블로어와 설비 카드 관리 관계 확인 전',
            oem_baseline='Electrical_Rev2.pdf · FG42/43 = PDF43/44 · Rev.2 17.03.2025 · M19 75kW·123A / 42AS1 ACS580-01-145A-4 / 42QM1 160A와 RATING145A 구분 · 당시 도면값',
            construction_baseline='Electrical_Can_Decoating_20241118.pdf · FOR APPROVAL / first draft design · PDF4/6/51 · 현재 승인·현행 배선 확인 전',
            control_title='VT02/TC03 조절·단계 설정·제한과 전류 불일치',control_links=[['VT02 조절 근거','regulation-manual.html#loop-VT02'],['설정·전원 복귀','recipe-settings.html#profile-P16'],['전류 제목 불일치1770','networks/network-1770.html']],
            timer_title='공유 Tag_61 · S5T#2S 기동 감시',related_title='추가 OFF·설정0 해제·전류/제목 불일치',
            related_links=[['추가 OFF/예열1843','networks/network-1843.html'],['FN02 전류1767','networks/network-1767.html'],['VT02 수동12','networks/network-12.html'],['관련 명세','control-specs/FN02.html#fault']],
            field_title='실물·単일 블로어·신호 전달과 정상 극성'.replace('単','단'),alarm_recovery='Set/Reset 연결은 현재 호출 순서·알람 해제·모터 운전의 증명이 아닙니다. 2초 감시·설정0·예열 추가OFF·VT02 설정 쓰기를 나누어 요청·출력·원시/처리 응답을 같은 시각에 비교합니다.',
            search_examples='Q2.3, Tag_61, S5T#2S, Set_Perc_VT02, TC03, VT02')))

def build_fn03_profile(root,data,source_rows):
    read=lambda file:json.loads((root/file).read_text(encoding='utf-8'))
    spec=next(p for p in read('registers/control-spec.json')['specifications'] if p['id']=='FN03')
    related=[r for r in spec['scoped_rules'] if r['rule_id'] in ['1801:73','1801:66','1801:854','1801:908','1866:607','1866:611']]
    assert {r['rule_id'] for r in related}=={'1801:73','1801:66','1801:854','1801:908','1866:607','1866:611'}
    control=dict(applicability='softstarter discrete control; own analog speed/current or regulation loop not identified',
        chain=['FN03은 보존 FG51의 단독 M25와 PSE72 소프트스타터입니다. 전용 아날로그 속도·전류 채널과 PID 조절 루프는 현재 대장에 확인되지 않습니다. 다른 팬의 QW/IW·AI1/AO2 경로를 배정하지 않습니다.',
            '1954:749 ON·Flag.M_FN_03→Start FN03(%Q3.2). 745는 FN_03_FAULT 또는 FN03_INV일 때 요청을 Reset합니다. 현재 출력·실물 운전은 별도입니다.',
            '1801:854/908은 같은 Tag_66에 각각 S5T#35S를 씁니다. ON·Start·NOT 처리 Run 뒤 Memo_M25_Running의 반전/비반전 분기로 갈립니다. 두 타이머를70초로 합산하거나 독립 타이머로 해석하지 않습니다.',
            '1801:73의 Memo Set은 PContact905.out 뒤이며 FP_M25_Run 펄스 문맥의 현재 동작은 미확정입니다. 66은 NOT Start 또는 NOT 처리 Run일 때 Memo Reset입니다. 기억 비트는 실물 TOR 입력이 아닙니다.',
            'INV Set856은 ON·Start·NOT Inputs.FN03_All_SoftStarter이며 Tag_66 접점이 없습니다. FAULT Set859는 Tag_66·NOT 처리 Run을 거칩니다. 알람 이름 INV를 인버터 설치 근거로 바꾸지 않습니다.',
            '1843/1844의 예열·생산 요청 Set은 단계36/56,1847의 정지 Reset은 종류5 단계1/비상 분기입니다. 단계 번호를 초로 바꾸지 않습니다.',
            '1866:600의 버너 관련 요청 Set에는 추가 OFF Contact640이 있습니다. 607/611은 처리 Run과 버너 허가·원격기동 경로이며1858의 FN03 FAULT 버너정지 영향과 구분합니다. OFF 현재값·외부 버너 내부 안전순서는 미확정입니다.'],
        repair=['Q3.2/FG139 MOD14 단자33→51KA1→PSE START8/9와110Vac 제어전원1/2를 분리해 관찰합니다. 51FU1 6A GG10×38·단자1/2의100–250Vac 표시와24V PLC 명령릴레이를 구분합니다.',
            'E4.1은 TOR5→FG120 MOD9 단자2, E4.2는FAULT6→MOD9 단자3입니다. RUN4는 입력 연결 표시가 없습니다. 원시 TOR·처리 Inputs.Run·Memo·Tag66·알람·버너 허가를 같은 시각에 비교합니다.',
            '보존 Simulation1084의 요청→처리 Run은 물리 입력 전달 증명이 아니며 실행하지 않습니다.'],
        pending=['현재 PSE 모델·명판·TOR/RUN/FAULT 접점 및 램프 시간·정상 극성·원시→처리 전달; 물리 I4.2 심볼의 원본 LAD 직접 참조는 미확보',
            '두 SdCoil의 같은 Tag66 쓰기 순서·PContact/FP_M25_Run 펄스·메모리·OB 호출·TIA/현재 CPU',
            '기동 심볼의 과거 a56.0 주석과 현재 Q3.2/도면 A3.2 구분·HMI1197 피연산자8개 미해석',
            '기존 버너 외부 제어·실제 연소 공기·허가·정지·복구 관찰·현재 승인 시공자료'],
        native=[1801,1843,1844,1847,1858,1866,1954],native_refs=related)
    pairs=[
        dict(signal='소프트스타터 기동',network=1954,uid='749',label='최종 출력 · Start FN03',boundary='ON·요청→Q3.2·51KA1·PSE START8/9. 110Vac 제어전원과24V 명령릴레이를 분리합니다.'),
        dict(signal='피드백으로 쓰는 TOR',network=1801,uid='858',label='처리 응답 · Inputs.FN03 Run',boundary='도면 TOR5→I4.1과 내부 Run 감시를 비교합니다. RUN4와TOR5는 별도이며 원시→처리 전달·현재 기능·정상극성은 확인 전입니다.'),
        dict(signal='소프트스타터 이상',network=1801,uid='855',label='처리 이상 · NOT Inputs.FN03_All_SoftStarter',boundary='도면 FAULT6→I4.2와 처리 입력의 반전 접점을 구분합니다. INV Set은 Tag66 접점 없이 요청/처리입력을 읽으며 정상극성·복구는 확인 전입니다.')]
    extra=[(1801,'part',uid) for uid in ['44','906','59','905','73','66']]+[(1801,'wire',uid) for uid in ['43','51','52','53','56','58','68','69','78','79','92','95','887','888','915','916']]
    extra += [(1031,'part','1858'),(1866,'part','640'),(1866,'part','607'),(1866,'part','611'),(1858,'part','283')]
    profile=build_static_profile(root,data,source_rows,dict(catalog_id='FN03',priority_key='P17',type='motor_softstarter',source_pairs=pairs,extra_locations=extra,
        internal_names=['Memo_M25_Running','FP_M25_Run'],control_reference=control,
        related_alarm_boundary='FN03 직접 FAULT/INV2개에서 FAULT만 Tag66 접점을 거칩니다. 두 SdCoil854/908이 같은 Tag66에35초를 쓰며 Memo/펄스 의미·현재 쓰기 순서는 미확정입니다. 1858의 버너정지 영향과1866 추가OFF·버너 허가/원격기동은 별도입니다. 현재 실물·정상극성·연소공기·복구는 확인 전입니다.',
        presentation=dict(identity_title='소프트스타터·단독 M25와 설비 식별',identity_pending='명판·위치·M25 연소 공기 블로어와 설비 카드 관리 관계 확인 전',
            oem_baseline='Electrical_Rev2.pdf · FG51 = PDF52 · 작성27.05.2024/개정행 공란; FG120/139 Rev.2 17.03.2025 · M25 37kW·61.9A / ABB PSE72-600-70 / 51QM1 62–73A와RATING68A / 440V60Hz · 보존 도면값',
            construction_baseline='Electrical_Can_Decoating_20241118.pdf · FOR APPROVAL/24.11.11 first draft/승인란 공란 · PDF4/6/21/51 · 1_3 =ENT+FN03-M25A CR→M25 · DAC/PVC-S/CORE4/SIZE25SB/SPARE0 · 100/RA→E200 Adjustment7/LEN36는 실측·현행 규격 증명 아님',
            control_title='두35초·메모리/펄스·TOR·버너 허가와 제어 경계',control_links=[['FN03 원본1801','networks/network-1801.html'],['버너 기동1866','networks/network-1866.html'],['설정·전원 복귀','recipe-settings.html#profile-P17']],
            timer_title='같은 Tag_66 · 두 SdCoil의 S5T#35S',related_title='TOR/RUN·메모리/펄스·버너정지/추가OFF',
            related_links=[['버너정지1858','networks/network-1858.html'],['버너기동/추가OFF1866','networks/network-1866.html'],['관련 명세','control-specs/FN03.html#fault']],
            field_title='실물·소프트스타터·TOR/FAULT와 정상 극성',alarm_recovery='Set/Reset과 두35초는 현재 호출·램프 완료·소프트스타터 고장 해제·버너 허가·실제 운전의 증명이 아닙니다. 원시 TOR/FAULT·처리입력·Memo·Tag66·요청·출력과 알람을 같은 시각에 관찰합니다.',
            search_examples='Q3.2, I4.1, Tag_66, S5T#35S, Memo_M25_Running, TOR')))
    # These two shared memory names do not contain FN03 and are absent from its
    # preserved name-based trace. Add reviewed display references without editing it.
    trace=dict(profile['signal_trace']);trace['signals']=list(trace['signals'])
    def usage(wire,oref,part,gate,pin,role):
        return dict(network=1801,block='allarms 1',title='fn03',file='sources/decoded-original/0436-FlgNet.xml',wire=wire,oref=oref,part=part,gate=gate,pin=pin,scope='Global',role=role,role_basis='원본 핀 및 선언 AK; 현재 펄스·호출 미검증',declarations=[dict(kind='SimpleAccess',scope='Global',access_kind={'write':'Write','read':None,'read/write':'RW'}[role],file='sources/decoded-original/0658-IdentXmlPart.xml')])
    trace['signals'].extend([
        dict(name='Memo_M25_Running',addresses=['%M180.1'],usages=[usage('79','80','73','SCoil','operand','write'),usage('69','70','66','RCoil','operand','write'),usage('92','93','87','Contact','operand','read'),usage('95','96','907','Contact','operand','read')],boundary='관련 기억 비트; 실물 TOR/운전 확인 아님'),
        dict(name='FP_M25_Run',addresses=['%M180.2'],usages=[usage('52','54','905','PContact','bit','read/write')],boundary='펄스 메모리 AK=RW; 현재 실행·펄스 시점 미검증')])
    profile['signal_trace']=trace
    return profile

def build_fn06_profile(root,data,source_rows):
    read=lambda file:json.loads((root/file).read_text(encoding='utf-8'))
    spec=next(p for p in read('registers/control-spec.json')['specifications'] if p['id']=='FN06')
    request=[r for r in spec['direct_rules'] if r['대상']=='Flag.M_FN_06']
    assert {r['rule_id'] for r in request}=={'1843:554','1844:898','1847:897','1955:772'}
    control=dict(applicability='contactor direct starting; own analog speed/current or regulation loop not identified',
        chain=['FN06은 FG52/PDF53의 단독 M26 접촉기 직접기동 회로입니다. 52QM1·52KM1·52QS1을 구분하며 전용 가변속/PID·아날로그 속도/전류 근거는 미확보입니다.',
            '1955: ON AND (MBVA01_FAULT OR (NOT Inputs.RD01 run AND NOT UNDER TESTING))→Flag.M_FN_06 Reset772. NOT UNDER TESTING은 RD01 가지에만 있습니다. 같은 네트워크의 ON·요청→Start FN06(%Q3.3) Coil776과 구분합니다.',
            '1802: ON·Start FN06·NOT Inputs.FEEDBACKMOTOR FN-06→SdCoil817, Tag_67(%T91), S5T#2S. ON·Start·Tag_67→MBVA01_FAULT Set823. ON·RESET_ALLARM·알람→Reset828이며 원인 해소 접점은 없습니다.',
            'MBVA01_FAULT는 원본상 FN06 감시와 요청 해제에 연결됩니다. 별칭 이름의 현재 자산 의미·HMI 문구·실물 동일성은 확인 전이며 다른 모터의 알람으로 재배정하지 않습니다.',
            '1843 예열 preset1/Tempo40 Set554,1844 생산 preset2/Tempo60 Set898,1847 preset5·(Tempo1 OR 비상) Reset897과1955 Reset772는 네 요청 쓰기입니다. 40/60은 비교 상수이며 초 단위로 추정하지 않습니다.',
            '1857: FN06 처리응답과 Inputs.Burner On은 OR38의 서로 다른 가지입니다. 이 OR 뒤 FN02 응답과 다른 직렬 조건→Flag.Burner_ready Coil182입니다. 버너 준비는 응답 소비이며 FN06 출력 소유가 아닙니다.',
            '1032: Tag47·원시 FN06_Fbk(%I4.3), MIN Add1/Ge60 뒤 HOUR Move1(W1902/1903)이며 시간값+1이 아닙니다. Move1874.eno→MIN Move0→Flag_Aggiorna_DB와1051 HOUR Move0을 별도로 보존합니다.',
            '1070 HMI Inputs/0397의 Move35: Tag_180 Word %IW4(RID10/Input AO32)→Inputs DB13 Word4(RID11/GlobalAccess AO32/BIRID4). 0628/0655의 같은 DB13/CID638561979615757134와 처리응답 BO35를 대조해 I4.3→DB13 bit4.3의 백업상 정적 복사를 확인했습니다. W39/40/41·DisableENO=true를 보존하며 같은 변수로 합치지 않습니다.',
            '1613/0030: Recipes Handler→ENO W32→HMI→ENO W33→HMI Output→ENO W42→NOT Simulation(1) Contact37→W43→HMI Inputs CRef28.en. 0692 RID140/NID19 UID45는 %M180.0, 0688 RID135/0694 RID136이 호출대상을 뒷받침합니다. 현재 값·호출 성공·주기·다른 쓰기는 확인 전이며 시뮬레이터를 실행하지 않습니다.',
            '1198 HMI 호출의 Ingresso_run/Allarme1/Risposta/Comulativo_allarmi 네 대상 선언은 미해석입니다. 일반 함수331의 Local 전달과 실제 FN06 인스턴스/DB11 주소를 합치지 않습니다.'],
        repair=['Q3.3/FG139 MOD14 단자34→A3.3→XS41→QS1 보조접점→XS42→QM1 보조접점→KM1 A1/A2→0Vdc10.6을 도면·관찰과 대조합니다. 단자번호가 없는 보조접점은 채우지 않습니다.',
            '24Vdc10.7→KM1 보조접점13/14→E4.3→FG120 MOD9 단자4입니다. 접촉기 보조응답은 회전·풍량 증명이 아닙니다. 원시I4.3와 DB 처리응답·요청·출력·Tag67·HMI를 같은 시각으로 분리합니다.',
            '보존 simulation1084의 요청→처리응답은 현재 물리 입력 전달 증명이 아니며 실행하지 않습니다. 1619/1620 ON 호출 연결도 현재 CPU의 전체 호출·실행 검증과 별도입니다.'],
        pending=['백업Word전달과분리해 원시I4.3/DB13 bit4.3의 현재 호출·ENO/주기·다른쓰기·현장정상극성',
            '1198의 네 미해석 HMI 대상·호출NID/인스턴스·DB11/DB2 레이아웃·DDE 원본과 버튼 이벤트',
            '기동 설명 a60.3과 원본Output AO27/Q3.3·도면A3.3의 불일치; 현행 명판/보호값·회로·케이블 승인자료',
            'Tag47/48 주기·HOUR Move1의 의도·ENO·다중쓰기·전원복귀·전체 OB/현재 CPU',
            'MBVA01 별칭의 현재 실물/HMI 대응·외부 버너 내부 안전순서·승인된 관찰과 복구 자료'],
        native=[331,1032,1051,1070,1198,1613,1619,1620,1802,1843,1844,1847,1857,1955],native_refs=request)
    pairs=[dict(signal='기동 명령',network=1955,uid='776',label='최종 출력 · Start FN06',boundary='ON·요청→Q3.3·A3.3/XS41/42·QS/QM·KM1 코일을 비교합니다. 실제 전압·접촉기·송풍은 별도 관찰입니다.'),
        dict(signal='접촉기 응답',network=1802,uid='866',label='처리 응답 · NOT Inputs.FEEDBACKMOTOR FN-06',boundary='KM1 13/14→I4.3와1070의IW4→DB13 Word4 정적 복사를 분리해 비교합니다. 현재 전달·극성과 반전 감시 접점·Tag67·별칭 알람은 별도입니다.')]
    extra=[(1032,'part',u) for u in ['1912','1864','1871','1874','1877','1880']]
    extra += [(1032,'wire',u) for u in ['1894','1895','1896','1897','1898','1899','1900','1902','1903','1904','1905','1906','1907','1913']]
    extra += [(1051,'wire',u) for u in ['2981','2982','2983']]
    extra += [(1955,'part',u) for u in ['22','798','802','767','804']]+[(1955,'wire',u) for u in ['797','799','24','803','789','791','805','794']]
    extra += [(1857,'part',u) for u in ['36','228','38','40','182']]+[(1857,'wire',u) for u in ['53','45','46','55']]
    extra += [(1198,'wire',u) for u in ['21','37','39','40','41','42','43','46','48']]+[(1620,'wire','351'),(1619,'wire','283')]
    extra += [(1070,'part','35')]+[(1070,'wire',u) for u in ['39','40','41']]+[(1613,'part','37')]+[(1613,'wire',u) for u in ['32','33','42','43','44']]
    return build_static_profile(root,data,source_rows,dict(catalog_id='FN06',priority_key='P18',type='motor_directstarter',source_pairs=pairs,extra_locations=extra,
        extra_sources=['sources/decoded-original/0621-IdentXmlPart.xml','sources/decoded-original/0623-IdentXmlPart.xml','sources/decoded-original/0624-IdentXmlPart.xml','sources/decoded-original/0627-IdentXmlPart.xml','sources/decoded-original/0628-IdentXmlPart.xml','sources/decoded-original/0629-IdentXmlPart.xml','sources/decoded-original/0655-IdentXmlPart.xml','sources/decoded-original/0688-IdentXmlPart.xml','sources/decoded-original/0694-IdentXmlPart.xml'],
        internal_names=['Allarm.MBVA01_FAULT','hours motors.FN_06_MIN','hours motors.FN_06_HOUR'],control_reference=control,
        related_alarm_boundary='FN06 자체 감시1개: MBVA01_FAULT·Tag67/T91·2초SD. RD01/UNDER TESTING 요청해제 가지, 네 요청쓰기, 버너준비의FN06応答 OR BurnerOn, HOUR Move1/ENO·초기화와 미해석HMI는 별도입니다. 현재 실물·정상극성·복구는 확인 전입니다.'.replace('応答','응답'),
        presentation=dict(identity_title='접촉기 직접기동·단독 M26와 설비 식별',identity_pending='명판·위치·M26 보조 블로어와 설비 카드 관리 관계 확인 전',
            oem_baseline='Electrical_Rev2.pdf · FG52/PDF53 작성27.05.2024·FG120/139 Rev.2 17.03.2025 · M26 3kW/5.8A·440V60Hz·52QM1 5.5–8A 도면범위·52KM1/52QS1 · 현행 설정값 아님',
            construction_baseline='Electrical_Can_Decoating_20241118.pdf · FOR APPROVAL/24.11.11 first draft/승인란 공란 · PDF21/51 · 1_4 =ENT+FN06-M26A CR→M26 · GAC/CV/4심/1.5/SPARE0 · 100/RB→E100 Adjustment13/LEN43; PDF21 100RBD1/CP No1/Pipe22 원문은 별도 보존',
            control_title='RD01 분기·별칭2초·버너준비OR·HOUR Move1과 제어 경계',control_links=[['요청·출력1955','networks/network-1955.html'],['별칭 알람1802','networks/network-1802.html'],['버너준비1857','networks/network-1857.html'],['HMI1198','networks/network-1198.html'],['입력Word전달1070','networks/network-1070.html'],['호출경계1613','networks/network-1613.html']],
            timer_title='Tag_67 / T91 · S5T#2S 감시',related_title='RD01 분기·버너준비·HMI/운전시간 경계',
            related_links=[['요청 해제1955','networks/network-1955.html'],['버너준비1857','networks/network-1857.html'],['운전시간1032','networks/network-1032.html'],['별도 초기화1051','networks/network-1051.html']],
            field_title='실물·접촉기 보조응답·전기전달과 정상 극성',alarm_recovery='알람 Reset·요청 재설정·출력·접촉기·실제 송풍과 복구는 별개입니다. 원시/처리응답과RD01분기·별칭 알람·Tag67을 같은 시각에 비교하고 원인 조치·승인 재기동과 재발 여부를 따로 기록합니다.',
            search_examples='Q3.3, I4.3, MBVA01_FAULT, Tag_67, S5T#2S, FN_06_HOUR')))

def build_mc04_profile(root,data,source_rows):
    read=lambda file:json.loads((root/file).read_text(encoding='utf-8'))
    spec=next(p for p in read('registers/control-spec.json')['specifications'] if p['id']=='MC04')
    request=[r for r in spec['direct_rules'] if r['대상']=='Flag.M_MC_04']
    assert {r['rule_id'] for r in request}=={'1843:460','1844:799','1847:954','1941:340'}
    control=dict(applicability='MC04 inverter speed output; MV04/current conflict and OFF torque preserved; no own PID identified',
        chain=['MC04/P08은 FG24/PDF25의 단독 M09 금속 컨베이어입니다. 모터11kW·19.3A와24AS1 ACS355 15kW,24QM1 도면49–59A/RATING52A를 서로 구분합니다. 실제 명판·보호 설정·실물 동일성은 확인 전입니다.',
            '1941: ON AND (MC_04_FAULT OR MC04_INV OR (NOT Inputs.VS01 run AND NOT Allarm.Maintenance_ON))→Flag.M_MC_04 Reset340. 유지보수 조건은 VS01 가지에만 있으며 같은 네트워크 ON·Flag→Start MC04(%Q0.4) Coil344와 구분합니다.',
            '1930: ON Contact47→Flag.Maintenance_ON Contact49→Coil36 Allarm.Maintenance_ON. 같은 AO61이어도 Flag와Allarm은 별개 DB이며 읽기/쓰기·현재 호출시점을 하나로 합치지 않습니다.',
            '1791: ON·Start·(Inputs.MC04_All_inv OR NOT Inputs.MC04 run)→SdCoil437 Tag_57(%T54)/S5T#5S. 같은 타이머 뒤 NOT run→FAULT Set443,비반전inv→INV Set487입니다. ON·RESET·own알람 Reset448/495에는 원인 정상 접점을 추가하지 않습니다.',
            '1792 mc04 deleted: OFF·NOT Inputs.MC04 torque→TORQUE Set454; OFF·RESET·torque·own알람→Reset460. 도면SS10 SPARE와 현재OFF값/설치/활성을 구분합니다.1941 요청해제식에 TORQUE는 직접 포함되지 않습니다.',
            '1843 preset1/Tempo17 Reset460,1844 preset2/Tempo24 Set799,1847 Auto_ON1·preset5·(Tempo19 OR 비상) Reset954와1941 Reset340의 네 요청쓰기를 보존합니다.1847에 없는ON 접점을 넣지 않고17/24/19를 초 단위로 추정하지 않습니다.',
            '1070/0397: Move22(W23/24) Tag178 Word IW0→Inputs DB13 Word0,Move42(W52/54) Tag171 Word IW6→DB13 Word6.0627/0629 AO0/48·0628/0655 같은DB13/CID638561979615757134·0657 bit6/7/53로 I0.6/0.7/6.5 정적복사를 확인했습니다. raw와DB는 다른변수이며 DisableENO=true·현재다른쓰기/극성은별도입니다.',
            '1613/0030: Recipes Handler ENO W32→HMI ENO W33→HMI Output ENO W42→NOT Simulation(1) Contact37→W43 HMI Inputs.en.0692 RID140/NID19UID45=%M180.0,0688/0694 호출선언.1619/1620/1621의ON·아날로그/알람/모터/시간 호출도정적범위이며 현재CPU실행과분리합니다. 시뮬레이터를실행하지않습니다.',
            '1693: ON·SET_PERC_MC04 <10→Move24 10, >100→Move26 100. Mul27(Int)에서 SET_PERC_MC04×272→102A5_SPARE3 Word %QW294.0474 W53/54/55·0661 RID16=272·0664 RID145/AO2352를 보존합니다. SPARE이름과FG112 PAW294 MC04 4–20mA→FG24 AI1 경로를구분하고 현장Hz/단위/순서·출력범위보증은확인전입니다.',
            '1769/0526 Signal linearization: ON en/IN0, MV04_M18A peripheral Int %IW324→Analog_input, Coeff100/Zero0→Amp_MC04·MC04_Absorbption_OFR. 입력은MV04위치 이름이고출력은MC04전류 이름입니다. 센서/채널/단위를추측해치환하지않습니다.',
            '1658/0291 및1659/0014: IN0·Analog_input>-1382·<=32767→형변환/ENO·(input+Zero)×Coeff/28000→Int OutValue. 범위분기→Move193 -9999·ENO→Out_of_range Coil23; 반전IN0→Move162 0. 1769의en도ON에매여ON=0에서호출/초기화를보장하지않습니다. 정수나눗셈/오버플로실행과물리범위는미검증입니다.',
            '1916 PV02 gate 앞단: ON·(원시MC04_Fbk OR Inputs.MC04 run OR Allarm.Maintenance_ON), OR443 W527/24/31입니다. MC03 spare1940도MC04 run을소비하지만 Start Spare Motor를씁니다. 두경로는MC04 출력소유가아닙니다.',
            '1022: Tag47·MC04_Fbk·MIN Add1/Ge60 뒤 HOUR Move1334 상수1(W1362/1363)이며 HOUR+1이아닙니다. ENO→MIN Move0→Flag_Aggiorna_DB와1049 HOUR Move0을분리합니다. 주기/의도/누적정상은확인전입니다.',
            '1182 HMI 호출8대상과 실제NID/인스턴스바인딩은미해석입니다. HMI설정DB11 X8.1/X8.0,DB2 X0.4와일반함수331의Local연결을합쳐 특정알람표시나버튼writer를확정하지않습니다.'],
        repair=['FG136 MOD14단자5/Q0.4→FG25 XS9/QS보조/XS10/QM보조→25KA1 A1/A2→0V10.6. FG24 드라이브9 +24V→25KA1 1/9→12 DI1 START입니다. PLC출력·릴레이·DI1·실제회전은각각관찰합니다.',
            'FG24 RUN17/19→I0.6 FG116 MOD8단자7,ALARM20/21→I0.7 단자8. FG112 QV3/QI3단자13/MANA16→PAW294→FG24 AI1 2/GND3·4–20mA. 현재극성/파라미터/실측환산은확인전입니다.',
            'FG25 SS10 SPARE X1 54/55·11/12→I6.5 FG122단자26. FG17 A7.4→17KA1/FG24 DI4 15와PLC Flag.RESET_ALLARM writer는별도입니다. FG14/24의14KA1/5와STO끝점은부분도면이며상위안전성·실행·현장복구증명이아닙니다.'],
        pending=['현행PLC/OB·호출ENO·온라인일치·다중쓰기/최종값·실제극성과원시/DB전달',
            'HMI1182 실제8바인딩·NID/DB11레이아웃·원본프로젝트/dde.cfg/화면이벤트',
            'M09/24AS1 명판·DI/RUN/ALARM/AI1설정·준공회로·보호값·PAW294단위',
            'IW324 MV04위치→MC04전류표시/OFR 상충의센서·채널·승인변경근거',
            'SS10 SPARE/삭제제목/OFF 및MC05접속함/LOC·MC04케이블/TO의설치·소유',
            'Tag47/48·HOUR Move1/초기화기능명세·PLCReset/DI4Reset/승인된실복구'],
        native=[331,1022,1049,1070,1182,1613,1619,1620,1621,1658,1659,1693,1769,1791,1792,1843,1844,1847,1916,1930,1940,1941],native_refs=request)
    pairs=[dict(signal='기동 명령',network=1941,uid='344',label='최종 출력 · Start MC04',boundary='Q0.4→QS/QM보조→25KA1→DI1과 VS01 요청해제 가지를분리합니다. 실제운전은별도입니다.'),
        dict(signal='운전 응답',network=1791,uid='500',label='처리 응답 · NOT Inputs.MC04 run',boundary='I0.6·IW0→DB13 0.6 정적복사와NOT run/공유5초감시를구분합니다. 현재극성/실행미확정입니다.'),
        dict(signal='인버터 이상',network=1791,uid='496',label='처리 입력 · Inputs.MC04_All_inv',boundary='I0.7·DB13 0.7·비반전감시와드라이브최초고장코드/정상극성을분리합니다.'),
        dict(signal='토크 감시 예비',network=1792,uid='480',label='OFF 조건 · NOT Inputs.MC04 torque',boundary='SS10 SPARE·I6.5·DB13 6.5·OFF·deleted 제목을분리하며현재활성을확정하지않습니다.'),
        dict(signal='속도 회로 주소 대조',network=1693,kind='wire',uid='55',label='속도 출력 · 102A5_SPARE3 / QW294',boundary='SPARE별칭과MC04 PAW294→AI1 경로·10/100제한·×272를비교합니다. 현행단위/드라이브설정은확인전입니다.')]
    extra=[]
    locations={1022:('1324 1331 1334 1337 1340','1362 1363 1364 1365 1366 1367'),1049:('2831','2857 2858 2859'),1070:('22 42','21 23 24 52 54'),1613:('37','32 33 42 43 44'),1693:('22 23 24 25 26 27','42 43 44 45 46 47 48 49 50 51 52 53 54 55'),1769:('21','32 33 34 35 36 37 38 39'),1792:('478 480 482 484 486 454 460','36 37 476 487'),1916:('443 524 526 22 29','525 527 24 31'),1930:('47 49 36','43 45 48 50'),1941:('26 380 333 340 344 377','28 29 24 360 362 365 378'),1182:('', '21 24 28 30 32 34 36 42 46'),1658:('258 161 190 259 193 23','21 22 49 252 253')}
    for n,(parts,wires) in locations.items():extra.extend((n,'part',u) for u in parts.split());extra.extend((n,'wire',u) for u in wires.split())
    return build_static_profile(root,data,source_rows,dict(catalog_id='MC04',priority_key='P08',type='motor_conveyor_inverter',source_pairs=pairs,extra_locations=extra,
        extra_sources=['sources/decoded-original/'+f+'-IdentXmlPart.xml' for f in ['0558','0621','0623','0624','0627','0628','0629','0655','0688','0692','0694']],
        internal_names=['Allarm.MC_04_TORQUE','Allarm.Maintenance_ON','Flag.Maintenance_ON','102A5_SPARE3','MV04_M18A','HMI_DB.SET_PERC_MC04','HMI_DB.Amp_MC04','Allarm.MC04_Absorbption_OFR','hours motors.MC_04_MIN','hours motors.MC_04_HOUR'],control_reference=control,
        related_alarm_boundary='자체FAULT/INV 두래치·공유Tag57/T54/5초와 별도OFF조건토크·MV04입력의MC04 OFR을구분합니다. VS01/유지보수는요청해제의한가지이며총현장알람개수나현재복구를확정하지않습니다.',
        presentation=dict(identity_title='M09 인버터 금속 컨베이어와 설비 식별',identity_pending='명판·위치·본체/M09와설비카드의관리관계확인전',
            oem_baseline='Electrical_Rev2.pdf · FG24/25=PDF25/26,M09 11kW19.3A·ACS355 15kW·440V60Hz·QM49–59A/RATING52A 도면값. FG24/25/112/122/136/17은Rev2 17.03.2025,FG116/14 개정란공란·작성27.05.2024. 현재설정/승인값아님',
            construction_baseline='Electrical_Can_Decoating_20241118.pdf ·24.11.11 first draft/승인공란·PDF34/51row1_18 EXI+MC04-M09A/4core/CV16 vs PVC-S16SB·SPARE0·100→120→121→122→EXI1TB1→E100/Adjustment15/LEN87. SS10 PDF34 LOC MC05와PDF59row9_7 FROM MC05/EXI1TB2→TO MC04/SS10·CVV2C1.0/E351/Adjustment3/LEN3 상충보존',
            control_title='VS01·유지보수·5초감시·OFF토크·속도/전류 상충과 제어 경계',control_links=[['요청·출력1941','networks/network-1941.html'],['유지보수1930','networks/network-1930.html'],['속도1693','networks/network-1693.html'],['전류상충1769','networks/network-1769.html'],['입력전달1070','networks/network-1070.html']],
            timer_title='공유 Tag_57 / T54 · S5T#5S 감시',related_title='OFF 토크·MV04 전류 상충·VS01/유지보수와 시간',related_links=[['OFF토크1792','networks/network-1792.html'],['전류상충1769','networks/network-1769.html'],['변환1658','networks/network-1658.html'],['HMI1182','networks/network-1182.html'],['시간1022','networks/network-1022.html']],
            field_title='실물·인버터·원시/DB입력·SPARE/상충과 정상극성',alarm_recovery='PLC알람Reset·드라이브DI4 Reset·요청재설정·Q/DI1·실제회전/응답과현장복구를구분합니다. 최초드라이브코드·FAULT/INV/Tag57·VS01/유지보수·원시/DB를같은시각에기록하고OFF토크/전류상충을추측해정상화하지않습니다.',
            search_examples='Q0.4, I0.6, I6.5, Tag_57, S5T#5S, QW294, 102A5_SPARE3, MV04_M18A')))

def build_vs01_profile(root,data,source_rows):
    spec=next(p for p in json.loads((root/'registers/control-spec.json').read_text())['specifications'] if p['id']=='VS01')
    request=[r for r in spec['direct_rules'] if r['대상']=='Flag.M_VS_01']
    assert {r['rule_id'] for r in request}=={'1843:456','1844:786','1847:975','1943:377'}
    control=dict(applicability='VS01 common inverter and two motor branches; separate OFF brake path; no own speed/current/PID confirmed',
        chain=['FG27/PDF28: 共通27AS1 ACS355-03E-38A0-4 18.5kW→M06 VS-01/M07 VS-01A 각8.3kW14.6A·440V60Hz. 공통RUN만으로 두모터 각각의회전/진동정상을확정하지않습니다.'.replace('共通','공통'),
            '1943/0248: ON·(Allarm.VS_01_FAULT OR Allarm.VS01_INV)→Flag.M_VS_01 Reset377, ON·Flag→Start VS01 Q0.6 Coil381입니다. MC04의VS01/유지보수분기를VS01 자체식으로복제하지않습니다.',
            '1794/0430: ON·Start·(NOT Inputs.VS01 run OR Inputs.VS01_All_Inv)→SD545 Tag_59 T60/S5T#2S. NOT run→FAULT Set551,비반전inv→INV Set595;ON·RESET·own→Reset556/603.0656 RID28/NID16UID559 V512는512ms가아닙니다.',
            '1944/0249 vs01 brake (off): OFF·NOT Flag·NOT run·NOT FAULT→SCoil425 Start VS01 BRAKE M11.0. OFF·(Flag OR FAULT OR INV)→Reset431. Set에는NOT INV가없고Reset에는INV가있습니다. 조건중첩/쓰기순서/현재OFF값은미확정입니다.',
            '1944: OFF·NOT run·BrakeRequest→SD439 Tag_117 T69/S5T#2S;같은접점495 뒤Coil444 Braking VS01 Q49.5입니다. T60과별도타이머이며2초 제동펄스로해석하지않습니다. 0602 RID74 Memory AO88/M11.0, RID77 Timer AO69, RID78 Output AO397/Q49.5·폐지주석과실제회로끝점누락을구분합니다.',
            '1843 예열preset1/Tempo17 Reset456,1844 생산preset2/Tempo18 Set786,1847 Auto_ON1·preset5·(Tempo21 OR Emergency) Reset975입니다. 정지식에ON을추가하지않고17/18/21을초단위로가정하지않습니다. 현재전체writer·스캔우선순위는별도입니다.',
            '1070/0397 Move22 W23/24: Tag178 Word IW0→Inputs DB13 Word0.0627 RID3/AO0·0629 RID5/AO0/BIRID4·0628/0655 같은DB13/CID·0657 RID279/280 bit9/10으로I1.1/I1.2 정적전달을확인했습니다. raw와DB는다른변수이고현재값/다른쓰기/극성미확정입니다.',
            '1613/0030: Recipes Handler ENO W32→HMI ENO W33→HMI Output ENO W42→NOT Simulation(1) Contact37→W43 HMI Inputs.en.0692 RID140/NID19UID45 M180.0과0688/0694 호출선언·1619/1620/1621 ON호출은정적경계입니다. 중지시뮬레이터를실행하지않습니다.',
            '1941/0247 NOT Inputs.VS01 run Contact26 뒤NOT Allarm.Maintenance_ON Contact380은MC04의요청해제소유경로입니다. VS01 응답소비관계이며VS01 출력writer로합치지않습니다.',
            '1024/0313: Tag47·raw VS01_Fbk→MIN Add1432 1/Ge1439 60→HOUR Move1442 상수1 W1470/1471;ENO W1472→MIN Move1445 0→Flag_Aggiorna_DB Set1448. HOUR+1이아닙니다.1050/0337 첫Move2884 0은Tag48 Contact2925.out W2926에서직접en으로들어갑니다.',
            '1184/0362 HMI CodeBlock22 CRef23/RID638의8바인딩은미해석입니다. CSV DB11 X12.0/X12.1·DB2 X0.6과일반331 Local함수만으로FAULT/INV 특정표시·버튼writer를확정하지않습니다.',
            'VS01 전용속도/전류/PID경로는확보하지못했습니다. FG27 AI배선미표기만으로현행고정속도/Hz를확정하거나MC04 QW294/IW324 경로를복제하지않습니다. 개별모터진동/전류/고장입력도추정하지않습니다.'],
        repair=['FG136 MOD14단자7/Q0.6→FG28 XS13/QS1/XS14→XS15/QS2/XS16→QM1/QM2/QM3 보조직렬→28KA1 A1/A2→0V10.6. FG27 9 +24V→28KA1 1/9→12 DI1. 출력/허가전달/공통인버터/각모터관찰을분리합니다.',
            'FG27 RUN17/19→I1.1 FG117 MOD8단자12,ALARM20/21→I1.2 단자13. 공통접점/드라이브파라미터/극성과각모터회전은별도입니다.',
            'FG17 A7.4→17KA1 4/12→FG27 DI4단자15;17SB2 E19.7·FlagRESET writer는별도. FG14 14KA2/6 5/6→FG27 X1C STO 끝점은부분근거이며상위안전성/현장동작검증이아닙니다. Q49.5브레이크로매핑하지않습니다.'],
        pending=['현행PLC/호출ENO/다중쓰기/타이머·OFF현재값/극성·온라인원시/DB전달',
            '스크린본체·M06/M07·VS01A표기·27AS1 관리동일성/명판·각모터회전/진동관찰',
            '준공QS/QM/DI/RUN/ALARM/STO·드라이브모델/보호설정·PLCReset→DI4 writer',
            'M11.0/Q49.5 브레이크끝점/모듈·실물·폐지/철거승인·Set/Reset우선순위',
            'HMI1184 8대상·NID/인스턴스/DB11·DB2/원본이벤트/통신',
            'Tag47/48주기·HOUR Move1/첫Move 초기화기능명세·실제복구'],
        native=[331,1024,1050,1070,1184,1613,1619,1620,1621,1794,1843,1844,1847,1941,1943,1944],native_refs=request)
    pairs=[dict(signal='공통 기동 명령',network=1943,uid='381',label='최종 공통 출력 · Start VS01',boundary='Q0.6·두QS/세QM·28KA1→DI1과각모터회전을구분합니다. 공통응답은두모터정상보증이아닙니다.'),
        dict(signal='운전 응답',network=1794,uid='604',label='처리 공통 응답 · NOT Inputs.VS01 run',boundary='I1.1·IW0→DB13 1.1 정적전달과반전감시를비교합니다. 정상극성/현재실행미확정입니다.'),
        dict(signal='인버터 이상',network=1794,uid='608',label='처리 입력 · Inputs.VS01_All_Inv',boundary='I1.2·DB13 1.2·공유T60감시와최초드라이브고장코드를구분합니다. 개별모터고장입력이아닙니다.')]
    extra=[]
    locations={1024:('1478 1480 1432 1439 1442 1445 1448','1479 1481 1463 1464 1465 1466 1467 1468 1470 1471 1472 1473 1474 1475 1476'),1050:('2925 2884','2910 2926 2911 2912'),1070:('22','21 23 24'),1613:('37','32 33 42 43 44'),1941:('26 380','25 28 29'),1943:('395 397 22 24 377 399 381','387 388 398 21 25 26 390 391 400 393'),1944:('479 481 483 485 425 487 489 22 428 431 491 493 439 495 444','459 460 461 462 486 464 488 490 24 467 469 470 471 492 494 472 473 474 496 476'),1184:('','21 24 28 30 32 34 36 42 46')}
    for n,(parts,wires) in locations.items():extra.extend((n,'part',u) for u in parts.split());extra.extend((n,'wire',u) for u in wires.split())
    return build_static_profile(root,data,source_rows,dict(catalog_id='VS01',priority_key='P09',type='motor_vibrating_screen',source_pairs=pairs,extra_locations=extra,
        extra_sources=['sources/decoded-original/'+f+'-IdentXmlPart.xml' for f in ['0606','0621','0623','0624','0627','0628','0629','0655','0688','0692','0694']],
        internal_names=['Start VS01 BRAKE','Braking VS01','Tag_117','OFF','hours motors.VS_01_MIN','hours motors.VS_01_HOUR'],control_reference=control,
        related_alarm_boundary='두자체알람FAULT/INV는공유T60/2초입니다. OFF브레이크T69/2초·M11.0/Q49.5는별도회로이며추가모터알람이나두초펄스로합치지않습니다. 공통응답/각모터/MC04소비와현장복구는별도입니다.',
        presentation=dict(identity_title='공통 인버터·M06/M07 두 모터와 스크린 식별',identity_pending='본체·VS01/VS01A·M06/M07·27AS1 명판/관리관계확인전',
            oem_baseline='Electrical_Rev2.pdf · FG27/PDF28 공통ACS355 18.5kW·두모터각8.3kW14.6A·440V60Hz·QM1 54–65A/RATING62A·QM2/3 10–16A 도면값. FG27/117/136/17 Rev2 17.03.2025,FG28/14 개정란공란·작성27.05.2024. 현행보호값아님',
            construction_baseline='Electrical_Can_Decoating_20241118.pdf ·24.11.11 first draft·PDF34/51 row1_20/1_21 EXI+VS01-M06A/M07A·CV6/4core vs PVC-S/6SB·SPARE0·100→120→121→122→EXI1TB1→E300/E400·Adjustment16/LEN88. 두행VS-01과전기VS-01A차이·준공미확정보존',
            control_title='공통기동·공유T60·별도OFF브레이크T69와 제어 경계',control_links=[['공통출력1943','networks/network-1943.html'],['브레이크1944','networks/network-1944.html'],['감시1794','networks/network-1794.html'],['입력1070','networks/network-1070.html']],
            timer_title='공유 Tag_59 / T60 · S5T#2S 운전 감시',related_title='별도OFF브레이크·두모터·MC04소비·시간',related_links=[['OFF브레이크1944','networks/network-1944.html'],['MC04소비1941','networks/network-1941.html'],['시간1024','networks/network-1024.html'],['첫Move초기화1050','networks/network-1050.html'],['미해석HMI1184','networks/network-1184.html']],
            field_title='스크린·공통인버터·각모터·브레이크 존재와 정상극성',alarm_recovery='드라이브원인회복·PLC래치Reset·DI4Reset·새요청·공통Q/RUN/ALARM·두모터각각의회전/진동·상류MC04복구를같은시각근거로구분합니다. 브레이크활성/철거와현재OFF값을추정하지않습니다.',
            search_examples='Q0.6, I1.1, I1.2, Tag_59, T60, Tag_117, T69, M11.0, Q49.5, VS01A')))

def build_pv01_profile(root,data,source_rows):
    spec=next(p for p in json.loads((root/'registers/control-spec.json').read_text())['specifications'] if p['id']=='PV01')
    control=dict(applicability='PV01 pneumatic two-gate valve command, memory and six-state sequence; no motor/PID ownership',
        chain=[
            'P05/PV01는 드럼투입 A/B 공압게이트 후보입니다. OEM EV01/EV02·P&ID compressed air→CL01/02,CL03/04와 기계 GATE A/B 상하형상은 실물대응확인전입니다. 인버터/모터/유압설정을복제하지않습니다.',
            '1911/0276: ON AND (ON OR UNDER TESTING) AND [(Enable AND !A_NOT_OPEN AND !B_NOT_OPEN) OR (!Enable AND A_MEM_OPEN AND B_MEM_OPEN)]→Coil115 R1GateON M10.5/Coil117 LOOP_ON DB2X4.7. 두NOT_CLOSE를자동허용부에추가하지않고중복ON을삭제하지않습니다.',
            '1911 ON·NOT R1GateON Contact206 W207→State0 Move125와 OpenA01/OpenB01/CloseA01/CloseB01 Reset130/133/136/139. local00·maintenance writer를초기화하는조건으로확대하지않습니다.',
            '1914/0278: ON·EV01_Sel_Open I9.2→Coil343 OpenA00 M20.0, ON·EV02_Sel_Open I9.3→Coil347 OpenB00 M20.1. PB15 공통70SB1와70SA1 A/B선택·HMI버튼을구분합니다.',
            '1915/0279 최종Q5.2 Coil384 = ON AND (OpenA00 OR OpenA01 OR maintenance PV01 M80.5), Q5.3 Coil377 = ON AND (OpenB00 OR OpenB01 OR maintenance PV01 OR OFF M0.1). OFF Contact418은비반전/메모리읽기이며false상수가아닙니다. Enable해제만으로모든출력차단을확정하지않습니다.',
            '1913/0277 pre ON555→Enable557→R1GateON559 W560. State0:CloseA Set334/OpenA Reset337→SD340 Tag163/T100 S5T#1S→Contact561 W562→Move345 State1. A닫힘기억직렬접점은없습니다.',
            'State1:OpenB Set356/CloseB Reset359→B_MEM_OPEN Contact563 W564→Move363 State2. State2 SD374 Tag164/T56 value SET_EVR1B_Open_time DB1W44→Contact565 W566→Move379 State3. 체류단위/현재값미확정입니다.',
            'State3:CloseB Set390/OpenB Reset393→SD396 Tag165/T102 S5T#1S→Contact567 W568→Move401 State4. B닫힘기억직렬접점은없습니다. State4 OpenA Set412/CloseA Reset415→A_MEM_OPEN569→Move419 State5. State5 SD430 Tag166/T57 DB1W16→Contact571→Move435 State0. 한스캔전이/안전성/실제시간검증이아닙니다.',
            '1912/0285 KF_KT CRef35:Data.PV_01B Int DB1W302→KF,W39 SEC literal0(Bool),KT W41→DB1W44 Word. ENO W45→CRef44.en,Data.PV-01a Int DB1W300→KF,SEC0→KT DB1W16. 0061 RID122 SEC은Bool이며함수몸체/단위/변환범위미확정입니다.',
            '1921/0286 A MEM:ON·Q_A·(I8.6 OR Inputs DB13X8.6)→S26 OPEN DB2X8.1;ON·!Q_A→R28. ON·!Q_A·(I8.7 OR DB13X8.7)→S33 CLOSE DB2X8.0;ON·Q_A→R35. raw/DB/순간위치/래치를합치지않습니다.',
            '1922/0287 B MEM:ON·Q_B·[I9.0 OR (false AND I9.1) OR DB13X9.0]→S28 OPEN DB2X8.3;ON·!Q_B→R30. ON·!Q_B·(I9.1 OR DB13X9.1)→S35 CLOSE DB2X8.2;ON·Q_B→R37.0610 RID130 NID12UID41 literalfalse와OFF는별개입니다.405/0150 ON326 W327→S307/309 초기CLOSE기억은물리닫힘증거가아닙니다.',
            '1070/0397 Move43 W55/ORef47 Tag181 Word IW8→W57/ORef48 Inputs DB13 Word8.0627 RID15 Input AO64·0629 RID16 BAD4 AO64/Word·0628 RID4 TOD13와0608 RID86 같은DB13/CID를대조했습니다. I8.6/8.7/9.0/9.1 raw와DB의현재값/극성/다른쓰기는미확정입니다.',
            '1613/0030 Recipes ENO W32→HMI ENO W33→HMI Output ENO W42→NOT Simulation(1)37 W43→HMI Inputs CRef28.en·0692 RID140 M180.0는정적호출경계입니다. 시뮬레이터를실행하지않고현재CPU/ENO를확정하지않습니다.',
            '1815/0449 A SD1453/1471 Tag80/T103·Tag81/T104 S5T#4S(0656 RID322 NID42UID1485/1494).1816/0450 B SD1517/1535 Tag82/T105·Tag83/T106 S5T#7S(RID320 NID43UID1549/1558). 열림ON·Q·!MEM_OPEN/닫힘ON·!Q·!MEM_CLOSE 감시이며S코일은별도ON·Q방향·timer접점입니다. 원시센서직접감시나모든게이트같은시간이아닙니다.',
            'A 알람DB3X10.1/10.2 Set1459/1477 Reset1464/1482, B DB3X10.3/10.4 Set1523/1541 Reset1528/1546. 각Reset ON·Flag.RESET_ALLARM·ownAlarm.930/0158 OR Inputs.Reset_allarmi/Flag.Reset_Allarms_HMI→S33 RESET/R40 HMI요청해제. 3초TOF를PV감시/복구시간으로복제하지않습니다.',
            '1843/0164 예열preset1·Auto_ON1·Tempo26→Enable S506/MemoStartup S34;예열상위W33 별도가지 Enable833·Memo834→TON835 PT0578RID118 T#1M→R837/838.1844 생산preset2/Tempo40 Set1158,1847 Auto_ON1·preset5·(Tempo15 OR Emergency) Reset941. 공통Enable DB2X5.0과HMI쓰기우선순위·M180.6작성/현재값미확정;26/40/15를초로가정하지않습니다.',
            '1935/0242 BC01소유 ON·Flag.M_BC_01·(R1_GATE_LOOP_ON OR MemoCMD_BC01_Startup OR Maintenance_ON)→Start BC01 Coil202. PV01 루프응답소비와BC01출력소유를분리하며PV01만으로BC01전체가항상운전/정지한다고확대하지않습니다.',
            '1215/0391 HMI PV_2Gate CodeBlock31/CRef32 0623/0624 NID39 RID715/716·20핀. Allarm5/6/7 ORef54/56/58→0626 RID48 FALSE만결속,나머지17바인딩은미해석.347/0400 공통Local함수와CSV DB11X76.0~76.6·DB2X5.0를실인수/현재이벤트로확정하지않습니다.'
        ],
        repair=['FG141 MOD15 단자13/Q5.2→FG69 69KA1 DC코일;110Vac9.7→69KA1 접점5/9→X1 126(5x20/2A F)→EV01 A1/A2→127/0Vac9.9. B 단자14/Q5.3→69KA2 DC코일·접점5/9→128/EV02→129/0Vac. 출력/접점/밸브/공압·기계/위치단계를구분합니다.',
            'FG70 LS01/02/05/06 13/14·X1 130~137→FG124 MOD10단자7/8 I8.6/8.7·FG125단자11/12 I9.0/9.1. LS02는FG124 SPARE와FG70배선/원본I8.7모두보존하며삭제/극성/실사용을추정하지않습니다.',
            'PB15 +24V→X1 138→70SB1→70SA1 A/B→139/I9.2·140/I9.3. 시공ENT2TB2/3·LS01~08 추가/ENT2TB3 A GATE반복설명·OEM↔심선미확정. 현장반/게이트위치를이름만으로확정하지않습니다.'],
        pending=['현행CPU/프로젝트·ON/OFF/UNDER TESTING/ENO·raw/DB·모든writer·스캔우선순위',
            'LS02 SPARE 실물/극성/배선·OEM X1↔ENT2TB 개별심선·LS03/04/07/08관계',
            'EV01/EV02 모델·110Vac정격·공압손실/정전복귀·CL01~04/기계A/B 실물동일성',
            'KF_KT 본체/SEC 단위·범위·현재DB1 체류값·고정1초전이설계검토',
            'HMI1215 미결속17실인수/DB11 멤버·객체이벤트·Maintenance공통과M80.5소유',
            '현재4/7초설정·실제원인/조치·MEM/센서/출력·복구/상류BC01증거'],
        native=[347,405,930,1070,1215,1613,1843,1844,1847,1815,1816,1911,1912,1913,1914,1915,1921,1922,1935],native_refs=spec['direct_rules'])
    pairs=[]
    for signal,n,u,label in [('게이트 A 밸브 명령',1915,'384','A 최종출력 Q5.2'),('게이트 B 밸브 명령',1915,'377','B 최종출력 Q5.3·OFF 병렬'),('게이트 A 열림 위치',1921,'23','A raw EV01_Open'),('게이트 A 닫힘 위치',1921,'30','A raw EV01_Close·SPARE상충'),('게이트 B 열림 위치',1922,'23','B raw EV02_Open'),('게이트 B 닫힘 위치',1922,'32','B raw EV02_Close'),('현장 게이트 A 선택',1914,'343','I9.2→A local00 요청'),('현장 게이트 B 선택',1914,'347','I9.3→B local00 요청')]:
        pairs.append(dict(signal=signal,network=n,uid=u,label=label,boundary='원시입력/DB처리/위치기억/자동·현장·유지보수·OFF출력/EV·공압기계응답을구분합니다. 현재극성/배선·실물·CPU/복구미확정입니다.'))
    extra=[]
    selected={1911:('186 188 192 104 194 196 198 200 202 204 109 115 117 206 125','159 160 163 164 165 166 167 169 170 171 173 174 175 177 207 178 179'),1913:('555 557 559 328 350 368 384 406 424 340 561 345 563 363 374 565 379 396 567 401 569 419 430 571 435','487 488 489 560 492 495 496 497 562 504 507 564 514 515 516 517 566 524 527 528 529 568 536 539 570 546 547 548 549 572'),1912:('','37 39 41 45 46 48 50'),1915:('410 412 414 416 418 372 377 420 422 424 380 384','395 411 396 397 398 399 400 402 403 405 406 408'),1921:('21 22 23 24 25 26 27 28 29 30 31 32 33 34 35','49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73'),1922:('21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37','53 54 55 57 58 59 60 61 62 63 64 65 66 67 70 72 73 74 75 76 77 78 81 88 90 91 93 95 96'),1070:('43','53 55 56 57'),1613:('37','32 33 42 43 44'),1215:('','33 35 37 39 41 43 45 47 49 51 53 55 57 59 61 63 65 67 69 71'),1843:('506 34 833 834 837 838','28 33 849 850 851 854'),1844:('1158','1087 1161'),1847:('941','1062 1064'),1935:('242 41 26 43 202','36 45')}
    for n,(parts,wires) in selected.items():extra.extend((n,'part',u)for u in parts.split());extra.extend((n,'wire',u)for u in wires.split())
    return build_static_profile(root,data,source_rows,dict(catalog_id='PV01',priority_key='P05',type='pneumatic_double_gate',control_reference=control,source_pairs=pairs,extra_locations=extra,
        extra_sources=['sources/decoded-original/'+f+'-IdentXmlPart.xml' for f in ['0060','0061','0563','0565','0575','0577','0578','0580','0607','0608','0609','0610','0623','0624','0626','0627','0628','0629','0631','0655','0688','0692','0694']]+['PV01-detail/PV01-manual.md','PV01-detail/PV01-io-map.csv','PV01-detail/PV01-hmi-map.csv','PV01-detail/PV01-internal-tags.csv','PV01-detail/PV01-verification.csv','PV01-detail/sources/pv01-evidence.json'],
        internal_names=['R1 Gate ON','Open EV A 00 PV-01','Open EV B 00  PV-01','Open EV A 01  PV-01','Open EV B 01  PV-01','Close EV A 01  PV-01','Close EV B 01  PV-01','maintenance PV01','ON','OFF','UNDER TESTING','WorkData.R1State','Data.PV-01a','Data.PV_01B','Data.SET_EVR1A_Open_time','Data.SET_EVR1B_Open_time'],
        related_alarm_boundary='4개位置감시 알람은A4초/B7초로서원시센서와MEM래치를구분합니다. 공통비상/Enable복수쓰기·BC01소비·Reset/HMI통합표시는별도. startupCLOSE기억·Q0·래치Reset이물리복구완료가아닙니다.'.replace('位置','위치'),
        presentation=dict(identity_title='드럼 투입 A/B 공압게이트·밸브와 실물 식별',identity_pending='PV01 본체/기계A/B 상하·EV01/02·CL01~04·PB15/ENT2TB2/3 현행대응미확정',
            oem_baseline='Electrical_Rev2.pdf:FG69/PDF70·FG70/PDF71·FG125/PDF126 개정란공란·기본DATE27.05.2024;FG124/PDF125·FG141/PDF142 Rev2 17.03.2025. EV110Vac/PLC릴레이DC·LS/PB15 24Vdc. 2A퓨즈는도면값·현행설정아님',
            construction_baseline='Electrical_Can_Decoating_20241118.pdf PDF21/53·24.11.11firstdraft. row3_8/9 ENT2TB2 DC CVV12G1.0 SPARE3/AC CVV3G1.0;3_10/11 ENT2TB3·LS05~08/EV02 E220/E320. LS01/02 E211/212 EV01 E213 LS05/06 E221/222 EV02 E323·A GATE반복설명·OEM개별심선미확정',
            control_title='자동 0~5 순서·현장/유지보수·위치기억과 제어 소유',control_links=[['최종출력1915','networks/network-1915.html'],['순서1913','networks/network-1913.html'],['A기억1921','networks/network-1921.html'],['B기억1922','networks/network-1922.html']],
            timer_title='A Tag80/81 T103/104 4초 · B Tag82/83 T105/106 7초',related_title='초기 닫힘기억·공통 Enable/Reset·BC01·HMI 미해석',related_links=[['startup405','networks/network-405.html'],['Reset930','networks/network-930.html'],['자동예열1843','networks/network-1843.html'],['HMI1215','networks/network-1215.html']],
            field_title='EV·공압·실린더·A/B 위치와 LS02 SPARE 실물 경계',alarm_recovery='알람Reset·요청/최종Q·원시센서/Inputs DB·위치MEM·실제EV/게이트회복·Enable/BC01연동을같은시각증거로구분합니다. Q0이나startupCLOSE기억만으로복구를확정하지않습니다.',
            search_examples='Q5.2, Q5.3, I8.7, LS02, SPARE, M80.5, OFF, T103, T105, KF_KT, R1State')))

def build_pv02_profile(root,data,source_rows):
    spec=next(p for p in json.loads((root/'registers/control-spec.json').read_text())['specifications'] if p['id']=='PV02')
    control=dict(applicability='PV02 pneumatic two-gate command, memory and six-state sequence; no motor/PID ownership',
        chain=[
            'P07/PV02는 드럼 배출측 A/B 공압게이트 후보입니다. P&ID EV04→CL05/06,EV05→CL07/08과 기계 A/B 상하형상은 실물 대응 확인 전입니다. OEM FG71/72 제목 LOAD DRUM_CLAPPE VALVE PV-02는 원문 그대로 보존합니다.',
            '1916/0280 ON524→[raw MC04_Fbk I0.6 Contact526 OR Inputs.MC04 run DB13X0.6 Contact22 OR Allarm.Maintenance_ON DB3X7.5 Contact29]→OR443. raw MC04 하나만 필수인 조건이 아닙니다.',
            '그 응답허가 AND [(Enable_R2_GATE DB2X10.3 Contact530 AND !A_NOT_OPEN532 AND !B_NOT_OPEN534) OR (!Enable536 AND A_MEM_OPEN538 AND B_MEM_OPEN540)]→OR450→Coil456 PV-02 GateON M12.2·Coil458 R2_GATE_LOOP_ON DB2X10.4. 두 NOT_CLOSE를 허가 조건에 추가하지 않습니다.',
            '1916 ON·NOT GateON Contact542 W543→Move466 W7=0 DB6W14와 Reset471/474/477/480 auto01. local00·maintenance M80.6까지 초기화하는 조건으로 확대하지 않습니다.',
            '1919/0282 ON704→I10.0 EV04_Sel_Open706→Coil686 OpenA00 M30.4; I10.1 EV05_Sel_Open708→Coil690 OpenB00 M30.5. PB16 현장 선택과 HMI 버튼·위치센서는 별개입니다.',
            '1920/0283 ON748 W749→A OR720(localA00,autoA01,maintenance PV02 M80.6)→Coil724 Q5.4; B OR713(localB00,autoB01,M80.6)→Coil717 Q5.5. 양쪽 OR Cardinality3이며 OFF 가지는 없습니다. Enable 해제만으로 모든 출력을 차단한다고 확정하지 않습니다.',
            '1918/0281 pre ON898→Enable900→GateON902 W903→WorkData.W7 Eq671/693/711/727/749/767의 State0~5. 현재 호출/스캔 순서와 실제 기계 시간은 확인 전입니다.',
            'State0 CloseA S677/OpenA R680→SD683 Tag167 T8 S5T#300MS(0610 RID65 NID6 UID788)→Contact904 W905 Move688 State1. State3 CloseB S733/OpenB R736→SD739 Tag169 T10 S5T#800MS(RID72 UID811)→Contact910 W911 Move744 State4. 닫힘 MEM 직렬 접점은 두 전이 모두 없습니다.',
            'State1 OpenB S699/CloseB R702→B_MEM_OPEN906 W907 Move706 State2. State4 OpenA S755/CloseA R758→A_MEM_OPEN912 W913 Move762 State5. 위치 기억은 raw 센서 순간값과 구분합니다.',
            'State2 SD717 Tag168 T9 value SET_PV02B_Open_time DB1W154→Contact908 W909 Move722 State3. State5 SD773 Tag170 T11 DB1W156→Contact914 W915 Move778 State0. 고정300/800ms와 가변체류 값·단위를 합치지 않습니다.',
            '1917/0284 KF_KT CRef23/CodeBlock22: Data.PV_02B Int DB1W306→KF W25, SEC W27 literal0 Bool→KT W29 DB1W154 Word. ENO W33→CRef32/CodeBlock31, Data.PV_02A Int DB1W304 W34→KF, SEC0 W36→KT W38 DB1W156. 0061 RID122 SEC은Bool, KF Int, KT Word이며 함수 몸체/시간단위/현재값 미확정입니다.',
            '1923/0288 A MEM: ON·Q5.4·(I9.4 OR Inputs DB13X9.4)→S26 OPEN DB2X8.5; ON·!Q5.4→R28. ON·!Q5.4·(I9.5 OR DB13X9.5)→S33 CLOSE DB2X8.4; ON·Q5.4→R35. raw23/30과 DB24/31 및 래치 출력을 구분합니다.',
            '1924/0289 B MEM: ON·Q5.5·(I9.6 OR Inputs DB13X9.6)→S26 OPEN DB2X8.7; ON·!Q5.5→R28. ON·!Q5.5·(I9.7 OR DB13X9.7)→S33 CLOSE DB2X8.6; ON·Q5.5→R35. PV01의 false AND close 추가 가지를 복제하지 않습니다.',
            '405/0150 ON326 W327→S303/S305 CLOSE 초기기억(0563 RID49/50 AO68/70,Flag DB2). startup CLOSE 기억은 물리적 닫힘 확인이 아닙니다.',
            '1817/0451 A SD1581/1599 Tag84/85 T107/108,1818/0452 B SD1645/1663 Tag86/87 T109/110 모두 S5T#7S(0656 RID320 NID44/45). 열림 ON·Q·!MEM_OPEN,닫힘 ON·!Q·!MEM_CLOSE 감시입니다. 알람Set은 별도 ON·Q방향·timer 접점이며 raw 직접감시로 확대하지 않습니다.',
            'A 알람 DB3X10.5/10.6 S1587/1605 R1592/1610;B DB3X10.7/11.0 S1651/1669 R1656/1674. 마지막 주소는 바이트 경계11.0입니다. Reset 각ON·Flag.RESET_ALLARM·자기알람. 930/0158의 공통 OR→S33 RESET/R40 HMI요청 해제와 현장복구 완료를 구분합니다.',
            '1930/0237 ON47·Flag.Maintenance_ON49 DB2X7.5→W50 Coil34 UNDER TESTING M5.5·Coil36 Allarm.Maintenance_ON DB3X7.5. Enable허가의 Allarm유지보수·Flag원본·최종출력의 M80.6은 서로 다른 변수이며 M80.6 작성자는 미확보입니다.',
            '1843/0164 예열 preset1·Auto_ON1·Tempo17 Eq452 W705→Enable_R2_GATE R462 W709/ORef617.1844/0165 생산 preset2·Auto_ON1·Tempo27 Eq802 W1065→S805 W1067/ORef965.0577 RID34/0578 RID30=17,RID82=27. 단계 수치를 초로 읽거나 전체 writer 우선순위를 확정하지 않습니다.',
            '1936/0243 RD01 요청 Reset236의 OR28.in5는 !R2_GATE_LOOP_ON278 AND !STANDBY_ON280 AND !UNDER TESTING35 W37.1939/0245 팬 요청 Reset283의 OR278.in2도 NOT311/313/318 W22의 같은 세 변수입니다. 해당 요청 소유를 구분하며 PV02만으로 전체 설비가 항상 정지/재기동한다고 확대하지 않습니다.',
            '1070/0397 Move22 W23/24 IW0→Inputs DB13W0,Move43 W55/57 IW8→DB13W8,Move44 W58/59 IW10→DB13W10.0627 RID3/15/17 AO0/64/80 및0629 RID5/16/18 BAD4,0628 TOD13/CID대조. rawMC04/위치/선택과 처리값의 현재 극성·다른쓰기는 확인 전입니다.',
            '1613/0030 Recipes ENO W32→HMI ENO W33→HMI Output ENO W42→NOT Simulation37 M180.0 W43→HMI Inputs CRef28.en은 정적 호출 경계입니다. 시뮬레이터 실행과 현재CPU/ENO 검증을 수행하지 않습니다.',
            '1216/0392 HMI PV_2Gate CRef22/CodeBlock23(0624 RID716/0623 RID715 NID40)20핀. Allarm5/6/7 ORef34/35/36→0626 RID48 FALSE만 결속,17실인수 미해석. CSV Enable DB2X10.3+DB11X78.0~78.6과347 공통Local함수를 현재 이벤트/실인수로 확정하지 않습니다.'
        ],
        repair=[
            'FG141 MOD15 단자15/Q5.4→FG71 71KA1 DC코일 A1/A2→-0Vdc10.6. 부하110Vac9.7→71KA1 접점5/9→선71.1→X1/141 5x20/2A F→71.2/EV04 A1,EV04 A2→142/0Vac9.9. B 단자16/Q5.5→71KA2 DC코일·접점5/9→143/EV05→144/0Vac. 원초안1/9 판독은 정정했으며 실제 모델/정격/폐로/복귀는 미확정입니다.',
            'FG72 LS25/26/29/30 접점13/14와 X1/145~152→FG125 MOD10 단자15~18/I9.4~9.7. PB16 +24V→X1/153→72SB1 GREEN13/14→72SA1 WHITE A/B→154/I10.0·155/I10.1→FG126 단자21/22. 접점심벌만으로 정상극성/현재배선을 확정하지 않습니다.',
            '시공 PDF24 LS25/26 No.5_3/5_4,PDF55 No.5_4/5_5이나 전체ID=ROT+PV02-LS25A/LS26A를 유지합니다. ROT1TB1A CORE26 대 CVV25G1.0 SPARE5·ROT1TB1B AC CVV12G1.0 SPARE5 및 추가LS27/28/31/32·OEM↔심선은 미확정입니다.',
            '공유ROT1TB1 분기 EV03은 FG21/PDF22 ROTATING DRUM RD-01 LUBRIFICATION VALVE, A5.1/21KA2/X1 50~51로 PV02 EV04/05와 별도입니다. 공유 케이블만으로 PV02 세 번째 밸브로 추가하지 않습니다.'
        ],
        pending=['현행CPU·ON/Enable/maintenance/ENO·raw/DB값·모든writer·스캔순서',
            '300/800ms 고정전이·7초감시 현재설정·실제기계/센서/래치 동작',
            'KF_KT 본체·SEC Bool 의미/단위·현재DB1W154/156 체류값',
            'EV04/05 명판·110Vac 정격·공압손실/정전복귀·CL05~08/기계 A/B 대응',
            'LS25/26 No.상충·CORE26대25·개별심선/OEM X1↔ROT단자·추가LS·준공판본',
            'HMI1216 미결속17핀/DB11실멤버·이벤트·M80.6 writer·RD01/팬 연동복구'],
        native=[347,405,930,1070,1216,1613,1817,1818,1843,1844,1916,1917,1918,1919,1920,1923,1924,1930,1936,1939],native_refs=spec['direct_rules'])
    pairs=[]
    for signal,n,u,label in [('게이트 A 밸브 명령',1920,'724','A 최종출력 Q5.4'),('게이트 B 밸브 명령',1920,'717','B 최종출력 Q5.5'),('게이트 A 열림 위치',1923,'23','A raw EV04_Open'),('게이트 A 닫힘 위치',1923,'30','A raw EV04_Close'),('게이트 B 열림 위치',1924,'23','B raw EV05_Open'),('게이트 B 닫힘 위치',1924,'30','B raw EV05_Close'),('현장 게이트 A 선택',1919,'686','I10.0→A local00 요청'),('현장 게이트 B 선택',1919,'690','I10.1→B local00 요청')]:
        pairs.append(dict(signal=signal,network=n,uid=u,label=label,boundary='raw/Inputs DB/위치MEM·자동/현장/유지보수 요청·최종출력·EV/공압기계를 구분합니다. 현재CPU/극성/배선/실물/복구 미확정입니다.'))
    extra=[]
    for n in [1916,1917,1918,1919,1920,1923,1924,1817,1818,1930,1936,1939,1216]:
        mapping=next(x for x in json.loads((root/'sources/decoded-original/network-map.json').read_text()) if x['document_id']==n)
        xml=ET.parse(root/'sources/decoded-original'/mapping['xml_file']).getroot();ns={'s':xml.tag.split('}')[0][1:]}
        extra.extend((n,'part',p.get('UId')) for p in xml.findall('s:Parts/s:Part',ns));extra.extend((n,'wire',w.get('UId')) for w in xml.findall('s:Wires/s:Wire',ns))
    for n,parts,wires in [(405,'303 305 326','319 320 321 327 328'),(1843,'452 462','672 703 704 705 709'),(1844,'802 805','1021 1063 1064 1065 1067'),(1070,'22 43 44','21 23 24 53 55 56 57 58 59'),(1613,'37','32 33 42 43 44'),(930,'28 33 40','29 30 36 38 42')]:
        extra.extend((n,'part',p)for p in parts.split());extra.extend((n,'wire',w)for w in wires.split())
    return build_static_profile(root,data,source_rows,dict(catalog_id='PV02',priority_key='P07',type='pneumatic_double_gate',control_reference=control,source_pairs=pairs,extra_locations=extra,
        extra_sources=['sources/decoded-original/'+f+'-IdentXmlPart.xml' for f in ['0060','0061','0563','0565','0577','0578','0602','0603','0604','0607','0608','0609','0610','0623','0624','0626','0627','0628','0629','0631','0655','0656','0657','0658','0692']],
        internal_names=['PV-02 Gate ON','Open EV A 00 PV-02','Open EV B 00  PV-02','Open EV A 01  PV-02','Open EV B 01  PV-02','Close EV A 01  PV-02','Close EV B 01  PV-02','maintenance PV02','ON','UNDER TESTING','WorkData.W7','Data.PV_02A','Data.PV_02B','Data.SET_PV02A_Open_time','Data.SET_PV02B_Open_time'],
        related_alarm_boundary='네 위치MEM 감시 모두7초이며 마지막B NOT_CLOSE 주소DB3X11.0을 유지합니다. startup닫힘기억·예열Reset/생산Set·MC04 raw/처리/유지보수 OR·RD01/팬 요청Reset·HMI미결속은 각각 별도 근거입니다. 알람Reset/출력0을 현장복구로 확정하지 않습니다.',
        presentation=dict(identity_title='드럼 배출 A/B 공압게이트·밸브와 실물 식별',identity_pending='PV02 본체·기계A/B·EV04/05·CL05~08·PB16/ROT단자 현행 대응 미확정',
            oem_baseline='Electrical_Rev2.pdf FG71/PDF72·FG72/PDF73·FG125/PDF126 개정란공란/DATE27.05.2024;FG126/PDF127·FG141/PDF142 Rev2 17.03.2025. EV부하110Vac/릴레이DC·LS/PB16 24Vdc·퓨즈2A는 도면값. EV03 FG21/PDF22 RD01소유',
            construction_baseline='Electrical_Can_Decoating_20241118.pdf PDF24/55·24.11.11firstdraft. LS25/26 No.5_3/5_4 대5_4/5_5·전체ID보존·ROT1TB1A CORE26대CVV25G1.0 SPARE5;AC CVV12G1.0 SPARE5·LS27/28/31/32추가·심선/승인준공미확정',
            control_title='MC04 허가·300/800ms 순서·위치MEM·현장/유지보수 소유',control_links=[['허가1916','networks/network-1916.html'],['순서1918','networks/network-1918.html'],['최종출력1920','networks/network-1920.html'],['A/B 기억','networks/network-1923.html']],
            timer_title='Tag84/85/86/87 T107~110 · 네 위치MEM 감시7초',related_title='startup·Enable Reset/Set·RD01/팬·HMI 미해석',related_links=[['startup405','networks/network-405.html'],['Enable1843/1844','networks/network-1843.html'],['RD01 Reset1936','networks/network-1936.html'],['HMI1216','networks/network-1216.html']],
            field_title='EV·공압·A/B 위치·LS 번호/케이블 상충과 현장 경계',alarm_recovery='원인 raw/Inputs DB·위치MEM·요청/최종Q·EV/실제게이트·알람Reset·MC04/RD01/팬연동을 같은 시각 증거로 구분합니다. 출력0/초기닫힘기억만으로 물리복구를 확정하지 않습니다.',
            search_examples='Q5.4, Q5.5, I9.4, I10.0, LS25, CORE26, M80.6, S5T#300MS, S5T#800MS, S5T#7S, KF_KT, W7')))

def build_mv01_profile(root,data,source_rows):
    spec=next(p for p in json.loads((root/'registers/control-spec.json').read_text())['specifications'] if p['id']=='MV01')
    regulation=next(p for p in json.loads((root/'registers/regulation-manual.json').read_text())['loops'] if p['id']=='MV01')
    control=json.loads(json.dumps(regulation))
    control['chain'] += [
        'P19/MV01은 HE01 계통 온도제어 댐퍼 후보·M20·LS23/24·ZT02로 연결합니다. P&ID 2.2kW440V와 OEM M20 2.2kW4.31A는 도면값이며 실물 동일성·밸브/감속기/커플링 소유는 확인 전입니다.',
        '1702/0342 ON226의 요청Reset 가지와 ON·!FAULT242의 출력 가지를 구분합니다. Open요청 R119는 Open230 OR Close232 OR Auto234,Close요청 R126은 Inputs.Close236 OR Open238 OR Auto240입니다. 현재 요청 writer/호출순서는 미확정입니다.',
        'Q2.4 Coil143: ON·!FAULT→[(Auto244 AND UP_PID246) OR Open248]→(MV WORK PULSE250 OR ON252)→!Q2.5 Contact254→!Inputs.Open256→!RESET_ENC23. 0617 RID1/NID1 UID172·180은 실제 ON M0.0 선언이며 원시 direct_rule의 불투명 표기는 보존합니다.',
        'Q2.5 Coil156: ON·!FAULT→[(((Auto258 AND DOWN_PID260) OR Close262) AND (Pulse264 OR ON266)) OR RESET_ENC273(W276)]→!Q2.4 Contact268→!Inputs.Close270. 리셋은 닫힘요청 병렬가지이며 실제 닫힘/원점완료가 아닙니다. Pulse OR ON을 항상 필수 펄스조건으로 해석하지 않습니다.',
        '1703/0354 RESET_ENC21·Inputs.Close22→Move23(en W38,IN DInt0 W39,out W41)→Memory_encoder.MV01.NewCountValue. ENO W40→!SetCountValue Contact24 W42→Coil25 W44→R26 RESET_ENC W46. S=S NewCount와 S=IO SetCount 선언을 임의 DB주소로 환산하거나 미해석 ENO를 실행결과로 확정하지 않습니다.',
        '1712/0350 ON·!Tag154→SD813 Tag155 T79 S5T#200MS,Tag155→SD818 Tag154 T78 S5T#2S,!Tag155→Coil823 MV WORK PULSE M10.0. PID PULSE_TM500MS/BREAK_TM1S와 이 공통 주기를 합치지 않습니다.',
        '1713/0351 Tag157 T119/Tag156 T118의10ms SD1225/1230→!Tag1571645→PBox1235 M50.7→ON1647→Q2.4 Add1248 WorkData.W33 DB6W66+1 및Move1254 W34=0;Q2.5 Sub1263 W34 DB6W68−1 및Move1269 W33=0. 명령 누적과 실제 ZT02카운트는 다른 값이며 실제 시간/스캔을 추정하지 않습니다.',
        '1714/0352 ON1943·ON1945→Gt1592 W33>2000→S1598 Allarm.MV01_FAULT DB3X4.7·Move1601 W33=0. Lt1606 W34<−2000→S1612 같은FAULT·Move1615 W34=0. 엄격비교 두 원인이 하나의 래치에 합쳐지며 카운트0 기록은 고장Reset이 아닙니다.',
        '1226/0159 ON513·ON515→[(Qopen517 AND !Inputs.RunOpening594) OR (Qclose519 AND !Inputs.RunClosing590)] OR242→SD249 Tag92 T4 S5T#150mS(0571 RID77,NID1 UID368)→Contact523→S254 같은FAULT. 접촉기 응답이지 모터 회전/끝단 감시가 아닙니다. ON513·RESET_ALLARM575·자기FAULT577→R342에는 정상응답 복귀조건이 직렬로 없습니다.',
        '1756/0506 !Simulation21·EM_OK22(I19.4)→HSC Instruction330 Call23/Instance24 encoder15. 23핀 중4핀 SwGate/ErrorAck/EventAck/CountValue만 결속되고19핀은 ORef에 RefId없음. SetCountValue W60/ORef32를1703의동명변수와 임의 연결하거나 FALSE/0으로 채우지 않습니다.',
        '1762/0512 EM_OK1113·!raw MV01_Close1115 I8.2→gate fill_unit1 Coil1025,Add1030 Encoder.CH00 DInt DB8D0+ACT_CNTV0→Local CNT_Act_0,ENO→Div1034 DInt100→CNTV0_100,ENO→Move1038 Int Encoder.CH00_10 DB8W36. 인코더 모델/하드웨어 채널 주소·물리단위/현재카운트는 미확정입니다.',
        '같은EM_OK·!gate1117→Move1047 CH00_10=Int0와Move1052 CH00에 INT#0 literal327(0675) 병렬. DInt 대상/Int 상수의 원문을 보존합니다. 같은EM_OK→Signal linearization CRef1059(0672 FC5),IN0=ON,Analog=CH00_10,Coeff=DB4W206,Zero=DB4W204,Out=Pot_MV01 DB1W148,OFR=DB3X24.6.',
        '1658/0291 IN0·Analog Int>−1382·Analog≤32767→Convert DInt164/167→Add170→Convert Coeff174→Mul177→Div181 DInt28000→Move185 Out Int. 범위 밖 >32767 OR≤−1382→Move193 −9999→ENO→ordinary Coil23 OFR. Int 상한을 고려하고 OFR를고장래치로확대하지않습니다.1659/0014 !IN0→Move162 Out=0.',
        '원본11/0477 CONT_S366 en ON463,Instance412 PIDMV01 DB21(0665 RID71). COM_RST=!Flag.MV01_Auto DB2X7.2,SP/PV=0669 block Local Real 변수입니다. 색인STL10의 ITD/DTR는 백업검색텍스트이며 네이티브 명령/줄바꿈/주석·현재값 검증을 대신하지않습니다.',
        'LMNR_HS=(ON·Inputs.Open) OR (ON·OFF·Pot_MV01≥100 Ge352);LMNR_LS=(ON·Inputs.Close) OR (ON·OFF·Pot_MV01≤10 Le361). OFF는 비반전 변수이며 현재상태 가정 금지.9핀 LMNS_ON/LMNUP/LMNDN/PVPER_ON/PV_PER/PV_FAC/PV_OFF/PV/ER 미결속;QLMNUP/DN만 M12.0/12.1 명령으로 연결합니다.',
        '8/0480 Data.TC03_SETPOINT Int DB1W50<200 Lt22→Move32 같은값200.0667 RID137 NID16 UID30/36·0668 RID45 UID29/37 Write. 원본 자동보정 분기이지 현장 보호값 변경이나 현재 설정 권고가 아닙니다.',
        '404/0149 ON337 W338→S293 Flag.MV01_Auto(0563 RID42,NID4 UID315) startup 기억.1070/0397 Move27 IW2→Inputs DB13W2(W31/W32)·Move43 IW8→DB13W8(W55/W57),각 선행 ENO 직렬. raw I3.2/3.3/I8.1/8.2와 처리DB입력 및정상극성/실제스캔을구분합니다.',
        '1190/0367 HMI_MotorizedValve14핀:0626 RID20/48 FALSE 4핀,나머지10실인수 미해석. CSV9태그의 DB11X18.0~18.4·DB2X3.3/3.4/7.2·RESET_ENC DB41X50.5를 physicalQ2.4/Q2.5나FAULT DB3X4.7과 동일주소로대체하지않습니다. 현재화면/이벤트/Reset권한 미확정입니다.',
        '1613/0030 CRef21 Recipes ENO W32→CRef23 HMI ENO W33→CRef25 HMI Output ENO W42→NOT Simulation37 M180.0→HMI Inputs CRef28.en. 정적호출경계이며 시뮬레이터 실행/행동검증과 현재CPU확인은 하지않습니다.'
    ]
    control['repair'] += [
        'FG138 MOD14 term25 Q2.4→44KM2 NC31/32→44.1→44KM1 A1/A2;term26 Q2.5→44KM1 NC31/32→44.2→44KM2. 공통 A2→44.3→44QM1보조→44.4→XS29→44QS1보조→XS30→−0Vdc10.6. QM/QS 보조 번호는 원본에 명시되지 않아 채우지 않습니다.',
        '3상440V60Hz8.3L1/L2/L3→44QM1 조정범위3.5~5A→44KM1/2역상→XM44U1/V1/W1→44QS1→M20 2.2kW4.31A PE. 범위와 실제보호설정은 별개입니다. +24V→KM1/2 보조13/14→E3.2/3.3→FG119 MOD8term33/34는접촉기피드백.',
        'FG45 +24V→X1 112(5×20/2A)→45.3→LS23 NC11/12→113 I8.1→FG124 MOD10term2;114→45.4→LS24 NC11/12→115 I8.2→term3. 원본NC심벌·PLC반전·실물정상극성을구분합니다.',
        'ZT02 B+24→107/37.1→FG144term9;C0V→108/37.2→term10;D→109/45.1→term1 CH0.A,E→110/45.2→term2 CH0.B;shield111/45SCH1접지. CH0.Nterm3 미표시·E20.0/.1/.2 SPARE는 카운트주소가 아닙니다.',
        '시공PDF51 No1_11 =FLA+MV01-M20A CR→M20GAC/CV4core1.5spare0 LEN49. PDF57 shared7_1 HE01-FLO2TB1A CVV25G1spare8;7_8/7_9 LS23A/24A DC2C1,E110/120 LEN5;7_10 ZT02A AI4S1 E330 LEN6. OEM A/B펄스와 시공AI 상충·개별심선/준공승인/실물은 미확정입니다.'
    ]
    control['pending'] += ['HSC19미결속핀·SetCountValue동명실인수·HW TM채널/분해능/방향/단위','150ms감시/10ms명령누적·실제스캔·FAULT세원인과복구','HMI10미해석핀/DB11내부멤버·이벤트·Reset권한','44QM1실제설정·QM/QS보조단자·접촉기/모터/댐퍼실물·OEM↔시공심선']
    control['native']=sorted(set(control['native']+[404,1070,1190,1226,1613,1658,1659,1703,1712,1713,1714,1756,1762]))
    pairs=[dict(signal=s,network=n,uid=u,label=l,boundary='명령/접촉기응답/끝단/엔코더를 구분합니다. 도면번호·정상극성·전달·HW TM채널/실물/현재CPU/현장복구는 확인전입니다.') for s,n,u,l in [
        ('열기 방향 명령',1702,'143','Q2.4 최종열기 명령'),('닫기 방향 명령',1702,'156','Q2.5 최종닫기 명령'),
        ('열기 접촉기 응답',1226,'594','Inputs.MV01 RunOpening 부정접점'),('닫기 접촉기 응답',1226,'590','Inputs.MV01 RunClosing 부정접점'),
        ('열림 끝단 위치',1702,'256','Inputs.MV01_Open 부정접점'),('닫힘 끝단 위치',1702,'270','Inputs.MV01_Close 부정접점'),
        ('엔코더 위치 채널 · 주소 미확정',1756,'75','HSC CountValue 출력/미결속19핀')]]
    pairs[-1]['kind']='wire'
    extra=[];mapping=json.loads((root/'sources/decoded-original/network-map.json').read_text())
    for n in [8,11,1190,1658,1659,1702,1703,1712,1756]:
        m=next(x for x in mapping if x['document_id']==n);xml=ET.parse(root/'sources/decoded-original'/m['xml_file']).getroot();ns={'s':xml.tag.split('}')[0][1:]}
        extra.extend((n,'part',p.get('UId')) for p in xml.findall('s:Parts/s:Part',ns));extra.extend((n,'wire',w.get('UId')) for w in xml.findall('s:Wires/s:Wire',ns))
    for n,parts in [(404,'337 293'),(1070,'27 43'),(1613,'37'),(1226,'513 515 517 594 519 590 242 249 523 254 575 577 342'),(1713,'1639 1641 1225 1643 1230 1645 1235 1647 1649 1248 1254 1651 1263 1269'),(1714,'1943 1945 1592 1598 1601 1606 1612 1615'),(1762,'1113 1115 1025 1030 1034 1038 1117 1047 1052')]:
        m=next(x for x in mapping if x['document_id']==n);xml=ET.parse(root/'sources/decoded-original'/m['xml_file']).getroot();ns={'s':xml.tag.split('}')[0][1:]};ids=set(parts.split());extra.extend((n,'part',p)for p in ids)
        extra.extend((n,'wire',w.get('UId'))for w in xml.findall('s:Wires/s:Wire',ns)if any(e.get('UId')in ids for e in w))
    extra += [(1070,'wire',p)for p in ['31','32','55','57']]+[(1613,'wire',p)for p in ['32','33','42','43','44']]+[(1762,'wire',p)for p in ['1107','1108','1109','1110','1111','24']]
    return build_static_profile(root,data,source_rows,dict(catalog_id='MV01',priority_key='P19',type='motorized_valve',control_reference=control,source_pairs=pairs,extra_locations=extra,
        extra_sources=['sources/live_index.json']+['sources/decoded-original/'+f+'-IdentXmlPart.xml'for f in ['0563','0570','0571','0572','0573','0611','0612','0617','0618','0619','0620','0623','0624','0626','0627','0628','0629','0665','0667','0668','0669','0670','0671','0672','0673','0674','0675','0676','0677','0678','0679','0680','0692','0694']],
        internal_names=['ON','OFF','UP MV01 PID','DOWN MV01 PID','MV WORK PULSE','Flag.MV01_Auto','Flag.MV01_Open','Flag.MV01_Close','HMI_DB.Reset_ENC_MV01','Data.Pot_MV01','WorkData.W33','WorkData.W34','Memory_encoder.MV01.NewCountValue','Memory_encoder.MV01.SetCountValue'],
        related_alarm_boundary='FAULT DB3X4.7 하나에150ms접촉기응답실패와명령누적 >2000/<−2000 두원인이합쳐집니다. Reset은응답정상조건을추가하지않습니다. 위치환산OFR DB3X24.6 ordinaryCoil·PID9미결속·HSC19미결속·HMI10미해석은별도입니다. 실제회전/댐퍼이동/원점/현장복구미확정.',
        presentation=dict(identity_title='온도제어 댐퍼·M20·LS23/24·ZT02 실물 식별',identity_pending='HE01/TC03 계통 후보·명판/감속기/댐퍼/공유TB·현재실물미확정',
            oem_baseline='Electrical_Rev2.pdf FG44/45/119/144 개정란공란 DATE27.05.2024;FG124/138 Rev2 17.03.2025. M20 2.2kW4.31A·440V60Hz·QM범위3.5~5A 도면값,실제설정미확정',
            construction_baseline='Electrical_Can_Decoating_20241118.pdf PDF51/57·24.11.11firstdraft. M20 CV4core1.5·HE01-FLO2TB1A shared25G1·LS23/24 DC2C1·ZT02 AI4S1 대OEM A/B펄스;개별심선/준공미확정',
            control_title='PID·개폐 차단·엔코더 리셋·명령 누적 소유',control_links=[['최종출력1702','networks/network-1702.html'],['교정1703','networks/network-1703.html'],['HSC1756','networks/network-1756.html'],['CONT_S11','networks/network-11.html']],
            timer_title='Tag92 T4 · 접촉기 응답150ms와명령누적고장',related_title='HSC/선형환산OFR·PID/HMI핀·startup·복수쓰기',related_links=[['FAULT1226','networks/network-1226.html'],['누적1714','networks/network-1714.html'],['환산1762','networks/network-1762.html'],['HMI1190','networks/network-1190.html']],
            field_title='접촉기·전력·끝단·ZT02 A/B·AI 표기 상충',alarm_recovery='Q/접촉기응답/raw·처리끝단/명령누적/실제카운트/Pot/OFR/FAULT/Reset/실물댐퍼를같은시각에구분합니다. Reset비트0·초기Auto·카운트0만으로원점/안전/현장복구를확정하지않습니다.',
            search_examples='Q2.4, I3.2, I8.2, ZT02, S5T#150mS, WorkData.W33, SetCountValue, CH0.A, CONT_S, DB3X4.7')))

def build_mv03_profile(root,data,source_rows):
    regulation=next(p for p in json.loads((root/'registers/regulation-manual.json').read_text())['loops'] if p['id']=='MV03')
    control=json.loads(json.dumps(regulation))
    control['chain'] += [
        'P20/MV03은 M17·LS19/20·ZT04 오버플로 밸브 후보입니다. P&ID M17 0.25kW440V와 OEM FG38 M17 2.2kW4.31A가 상충합니다. 명판/현재실물/감속기/밸브 소유 확인 전이며 임의 용량·보호값을 채택하지 않습니다.',
        '1705/0344 ON328→Sub256 Data.PSH03_SETPOINT DB1W40−Data.PSH03 DB1W24→Local Int ErrPSH03. !Tag147330→SD263 Tag148 T139 S5T#4S;Tag148332→SD268 Tag147 T138 S5T#10S. !Tag148334→Ge276 Err≥5→Coil279 PID down M14.5;Lt282 Err<−5→Coil285 PID UP M14.4. 비대칭 비교를 ±5 닫힌 데드밴드로 바꾸지 않습니다.',
        '1706/0345 ON489·!FAULT505의 출력 가지: Q1.7 Coil390=((Auto507·UP509·(Pulse511 OR ON513)) OR (Open515·(Pulse517 OR ON519)) OR Washing521)→OR543→!ResetENC44→!Inputs.Open523. 열림 요청에는 세정 OR와 교정 차단이 있습니다.',
        'Q2.0 Coil407=((((Auto525·DN527·(Pulse529 OR ON531)) OR (Close533·(Pulse535 OR ON537)) OR StartupClose36)→OR544→!Washing539) OR ResetENC546)→OR53→!Inputs.Close541. 모든 출력은 공통 ON·!FAULT 앞단을 포함합니다. ResetENC는 !Washing을 우회하는 별도 OR 가지이고 실제 닫힘/영점 완료가 아닙니다.',
        '0345 두 출력 경로에 반대 방향 Q1.7/Q2.0 차단 접점은 없습니다. FG38 하드웨어의 반대 접촉기 NC31/32를 별도로 추적합니다. 기존 회로 안내의 반대 출력 조건 설명은 원본 XML과 불일치하며 보존 원자료를 현행 안전성 증거로 채택하지 않습니다.',
        'ON489→ON491 요청 해제: Inputs.Open493 OR Close495 OR Auto497→R362 Flag.M_MV03_OPEN DB2X9.7;Inputs.Close499 OR Open501 OR Auto503→R369 Flag.M_MV03_CLOSE DB2X10.0. Inputs.Close42→R46 Close MV03 for Burner Startup M180.5. startup404/0149 ON337→S300 Auto DB2X7.0(W329/ORef318). 기억비트 해제/초기 Auto와 물리 위치를 구분합니다.',
        '1707/0353 ResetENC22 DB41X50.6·Inputs.Close26→Move32 DInt0 NewCountValue(RID193) W34/35. ENO W38→!SetCountValue40→Coil44(RID195) W43→R48 ResetENC W51. DB17 HSC의 S=S/IO 내부멤버 offset를 고정 절대주소로 확정하지 않습니다. 원시 opaque2와 미결속 SetCountValue 핀을 보존합니다.',
        '1712/0350 ON846·!Tag154848→SD813 Tag155 T79 S5T#200MS;Tag155850→SD818 Tag154 T78 S5T#2S;!Tag155852→Coil823 MV WORK PULSE M10.0. 출력의 Pulse OR ON을 항상 필수 펄스 조건이라고 해석하지 않습니다.',
        '1713/0351 공유 Tag156 T118/Tag157 T119 S5T#10MS→!Tag1571645→PBox1235 M50.7→ON1659:Qopen1661→Add1316 W29 DB6W58+1/Move1322 W30=0;Qclose1663→Sub1331 W30 DB6W60−1/Move1337 W29=0. 명령 누적과 ZT04 실측 카운트는 별개이며 초 단위로 환산하지 않습니다.',
        '1714/0352 ON1943·ON1949→Gt1656 W29>3400→S1662 FAULT·Move1665 W29=0;Lt1670 W30<−3400→S1676 같은FAULT·Move1679 W30=0. DB3X4.3 하나로 두 원인이 합쳐지고 누적0은 고장Reset이 아닙니다.',
        '1226/0159 ON513·ON535→[(Qopen537·!RunOpening541) OR (Qclose539·!RunClosing34)] OR36→SD281 Tag94 T3 S5T#150S→Contact543→S286 같은FAULT. 0571 RID83 SV150S/V8528=0x2150은 150초입니다. 인접150ms와 혼동하거나 현재 실제 검출시간/안전 적절성으로 확정하지 않습니다. ON513·RESET_ALLARM575·자기FAULT581→R350에는 응답 정상화 직렬조건이 없습니다.',
        '1758/0508 !Simulation75·EM_OK21 I19.4→High_Speed_Counter LRef22/Instance23 MV03_Encoder DB17. 23핀 중 SwGate W51/ORef25와 CountValue W71/ORef45만 결속,21핀 RefId없음. ErrorAck/EventAck/SetCountValue를 MV01 방식으로 연결하거나 0/FALSE로 채우지 않습니다.',
        '1764/0514 EM_OK1217·!처리 Inputs.MV03 Close1219 DB13X7.6→Coil1129 SW_GATE2;Add1134 Encoder_CH02 DInt DB8D8+ACT_CNTV2→Local CNT_Act_2→ENO Div1138 DInt100→Local CNTV2_100→ENO Move1142 Int Encoder_CH02_10 DB8W40. MV01의 raw 끝단 조건과 구분합니다.',
        '같은 EM_OK·!SW_GATE2 Contact1221→Move1151 CH02_10 Int0와 Move1156 CH02 DInt 대상에 INT#0 literal327 병렬. CRef1163 Signal linearization은 EM_OK 공통 W1218;IN0=ON,Analog=CH02_10,Coeff DB4W202,Zero DB4W200,Out Pot_MV03 DB1W144,OFR DB3X25.0(W24). S/IO 및 단위/스케일/모델·현재계수 미확정.',
        '1761/0511 !EM_OK963→Move927 Local CNT_Act_2→Encoder_CH02 W956/957는 별도 기억쓰기입니다. 전원 복귀 보장으로 확정하지 않습니다. Pot_MV03의 다른쓰기 후보0635 RID314 NID2 UID509/517는 보존된 기존1083 관련 선언만 확인하고 원본 블록/시뮬레이터를 작성·수정·생성·실행·행동시험하지 않습니다.',
        '1658/0291 IN0·Analog Int>−1382·≤32767→Convert DInt164/167→Add170(input+Zero)→Convert Coeff174→Mul177→Div181 DInt28000→Move185 Out Int. >32767 OR≤−1382→Move193 −9999→ENO ordinaryCoil23 OFR. 1659/0014 !IN0→Move162 Out0. 단위와 현재 범위/복구는 확인 전입니다.',
        '15/0479 CONT_S LRef507/Instance546 PID_MV03 DB25,제목 not used,en OFF583 M0.1 비반전. COM_RST=!Auto585 OR Washing587;LMNR_HS=!Inputs.Open589,LMNR_LS=!Inputs.Close591. SP/PV Local Real_SPPC02/Real_PC02. 검색STL14의 PSH02_SETPOINT/PSH_02 ITD/DTR 텍스트와 네이티브 명령·현재값 검증을 구분합니다.',
        'CONT_S GAIN−4.0,TI10S,DEADB_W2.0,CYCLE100MS,PULSE_TM200MS,BREAK_TM5S,MTR_TM3S,DISV2.0은 원본 인자입니다. 9핀 LMNS_ON/LMNUP/LMNDN/PVPER_ON/PV_PER/PV_FAC/PV_OFF/PV/ER 미결속. QLMNUP/DN W577/578은 같은 M14.4/14.5를 쓰므로0344와 중복 writer입니다. not used 제목/OFF 이름만으로 미사용을 확정하지 않습니다.',
        '1868/0184 burner control 소유 W=M48.1/B=M180.5:ON1634·!Enable1636→State0/W Reset/Enable Reset. 같은가지 !Inputs.Close28→Inputs.Close1670→S1669 B는0585 RID233 같은값 직렬 상충입니다. 임의 정상화하거나 B 전체가 불발이라고 단정하지 않습니다.',
        '관련 버너 순서:State0 온도≥500→7/<500→1;State1 S1176 Washing→2;State2 !Inputs.Open1642→3;State3 Tag143 T31 S5T#4M/Tag142 T32 S5T#1S CleanTime;State4 R1237 W→5;State5 Inputs.Close1654 OR ON1656→6;State6 Tag144 T37 S5T#1S→7;State7 S1300 Enable/R1303 W/S1306 B→8;BurnerOn→9·Tag145 T38 S5T#30S→10. BR01 전체 안전/현재 스캔 순서로 확대하지 않습니다.',
        '1747/0497 ON495→Signal linearization CRef476:Analog W491/ORef484 PSH03:P Peripherie Int AO2560=PIW320→Data.PSH03 DB1W24;Coeff DB4W220/Zero DB4W218,Out_of_range DB3X22.2. PSH02 AO2288=PIW286는 별도입력. FG75 OUTPUT MV03/PSH02와 우측 PSH03의 PRESSURE CONTROL PSH02 제목 상충을 보존합니다.',
        '1070/0397 선행 ENO→Move27 IW2→Inputs DB13W2 W31/32. rawOpen Contact127→Not142→Coil147 Inputs.Open W122/137/145/146;rawClose149→Not150→Coil151 Inputs.Close W155/156/157/158. 원시 I7.5/7.6·처리 DB13X7.5/7.6·HMI DB11 표시를 구분합니다.',
        '1191/0369 HMI Motorized Valve CRef22/CodeBlock23 14실인수중 Allarme2/3/4/5 W50~53는 FALSE4,10실인수 선언 미결속. CSV9행 DB11X22.0~22.4·DB2X9.7/X10.0/X7.0·Reset DB41X50.6과 물리Q/FAULT는 별도주소. I_PSH_03 DB13INT52와 Data.PSH03 DB1W24도 다른 층입니다.',
        '1613/0030 Recipes→HMI→HMI Output ENO W32/33/42 뒤 !Simulation37 M180.0→W43 HMI Inputs CRef28. 정적 호출 경계만 확인했으며 TIA/현재CPU/현장/가상실행 확인을 대신하지 않습니다.'
    ]
    control['repair'] += [
        'FG137 MOD14term18 Q1.7→38KM2 NC31/32→38.1→38KM1 A1/A2;FG138term21 Q2.0→38KM1 NC31/32→38.2→38KM2. 공통A2→38.3→38QM1보조→38.4→XS25→38QS1보조→XS26→−0Vdc10.6. 보조번호 원문미표기·현재전압/배선미확정.',
        '3상440V60Hz8.3L1/2/3→38QM1 범위3.5~5A→38KM1/2 역상→XM38U1/V1/W1→38QS1→M17 2.2kW4.31A PE. +24V→KM1/2 보조13/14→I2.4/2.5→FG118 MOD8term25/26. 도면범위는 현재설정이 아닙니다.',
        'FG39 +24V→X90 2AF→39.3 LS19 NC11/12→X91 I7.5 FG123term36;X92→LS20 NC→X93 I7.6term37. OEM NC와 PLC NOT 및 정상극성/단선반응을 따로 확인합니다.',
        'ZT04 B+24→X85/35.1 FG146term9,C0→86/35.2term10,D→87/39.1 CH0.Aterm1,E→88/39.2 CH0.Bterm2;shield89/39SCH1접지. CH0.Nterm3 원문연결없음·SPARE I21/A9는 카운트주소아님.',
        'FG75 PSH03 +24→X178 50mAF→75.3→센서+;센서−→X179/PEW320 FG108 I0+term2,−/MANAterm4/18;shield180/75SCH3. 별도PSH02 PEW286 0/10mbar4–20mA 표기를 PSH03 현행범위로 복제하지 않습니다.',
        '시공PDF51 No1_9 =FLA+MV03-M17A CR→M17 GAC/CV4core1.5spare0 LEN46. PDF56shared6_1 FLO1TB1A DC12G1spare3 LEN44,6_3 ZT04 TM4S1 LEN42,6_11 HE01-PSH03A AI4S1spare1 LEN48;6_15/16 LS19/20 DC2C1 LEN5,6_17 ZT04 TM4S1 LEN6. 가려진6_7~10 제외·심선/준공/실물미확정.'
    ]
    control['pending'] += ['P&ID0.25kW/OEM2.2kW M17·현재명판/보호설정','PLC상대Q접점없음/하드웨어NC·현재안전성','150초 감시·누적엄격±3400·복수쓰기/호출','HSC21미결속·HMI10미해석·DB17内部/채널','PSH03 PIW320/PSH02 PIW286·도면소유·센서범위','버너동일Close직렬상충·State2NOTOpen/State5CloseORON·현재프로젝트']
    control['native']=sorted(set(control['native']+[404,1070,1191,1226,1613,1658,1659,1707,1712,1713,1714,1747,1758,1761,1764,1868]))
    rows=[('열기 방향 명령',1706,'390','Q1.7 최종열기'),('닫기 방향 명령',1706,'407','Q2.0 최종닫기'),('열기 접촉기 응답',1226,'541','Inputs.RunOpening 부정접점'),('닫기 접촉기 응답',1226,'34','Inputs.RunClosing 부정접점'),('열림 끝단 위치',1706,'523','처리 Inputs.Open 부정접점'),('닫힘 끝단 위치',1706,'541','처리 Inputs.Close 부정접점'),('엔코더 위치 채널 · 주소 미확정',1758,'71','HSC CountValue/21미결속핀')]
    pairs=[dict(signal=s,network=n,uid=u,label=l,boundary='Q/접촉기응답/raw끝단/처리NOT/실측엔코더를 구분합니다. PLC 상대Q 차단접점은 없고 NC 하드웨어 회로는 별도입니다. 현재CPU·실물·정상극성·현장복구는 확인전입니다.')for s,n,u,l in rows];pairs[-1]['kind']='wire'
    mapping=json.loads((root/'sources/decoded-original/network-map.json').read_text());extra=[]
    for n in [15,1191,1658,1659,1705,1706,1707,1712,1747,1758,1761,1764,1868]:
        m=next(x for x in mapping if x['document_id']==n);xml=ET.parse(root/'sources/decoded-original'/m['xml_file']).getroot();ns={'s':xml.tag.split('}')[0][1:]};extra.extend((n,'part',p.get('UId'))for p in xml.findall('s:Parts/s:Part',ns));extra.extend((n,'wire',w.get('UId'))for w in xml.findall('s:Wires/s:Wire',ns))
    for n,parts in [(404,'337 300'),(1070,'27 127 142 147 149 150 151'),(1613,'37'),(1226,'513 535 537 541 539 34 36 281 543 286 575 581 350'),(1713,'1639 1641 1225 1643 1230 1645 1235 1659 1661 1316 1322 1663 1331 1337'),(1714,'1943 1949 1656 1662 1665 1670 1676 1679')]:
        m=next(x for x in mapping if x['document_id']==n);xml=ET.parse(root/'sources/decoded-original'/m['xml_file']).getroot();ns={'s':xml.tag.split('}')[0][1:]};ids=set(parts.split());extra.extend((n,'part',p)for p in ids);extra.extend((n,'wire',w.get('UId'))for w in xml.findall('s:Wires/s:Wire',ns)if any(e.get('UId')in ids for e in w))
    extra += [(1613,'wire',x)for x in ['32','33','42','43','44']]
    correction='정정 근거:0345/1706 출력에는 반대 방향 Q 차단접점이 없습니다. 모드·고장·처리리미트·세정/기동/교정 가지와 FG38 상대접촉기 NC31/32를 별도로 비교합니다. 보존된 기존 회로 안내의 반대 출력 조건 설명은 XML과 불일치합니다.'
    return build_static_profile(root,data,source_rows,dict(catalog_id='MV03',priority_key='P20',type='motorized_valve',control_reference=control,source_pairs=pairs,extra_locations=extra,
        extra_sources=['sources/live_index.json']+['sources/decoded-original/'+f+'-IdentXmlPart.xml'for f in ['0062','0563','0570','0571','0572','0573','0582','0583','0584','0585','0611','0612','0617','0618','0619','0620','0623','0624','0626','0627','0628','0629','0635','0665','0667','0668','0669','0670','0671','0672','0673','0674','0675','0676','0677','0678','0679','0680','0690','0691','0692']],
        internal_names=['ON','OFF','PID UP MV03','PID down MV03','MV WORK PULSE','Flag.MV03_Auto','Flag.M_MV03_OPEN','Flag.M_MV03_CLOSE','Open MV03 for washing','Close MV03 for Burner Startup','HMI_DB.ResetEncoderProcedure_MV03','Data.Pot_MV03','Data.PSH03','Data.PSH03_SETPOINT','WorkData.W29','WorkData.W30','MV03_Encoder.NewCountValue','MV03_Encoder.SetCountValue'],
        related_alarm_boundary='MV03_FAULT DB3X4.3 하나에150초 방향접촉기응답실패와W29>3400/W30<−3400 두명령누적원인이합쳐집니다. 위치OFR DB3X25.0·압력OFR DB3X22.2·HMI DB11X22.2·HSC진단은 별도층입니다. Reset에정상응답직렬조건없음·물리복구미확정.',
        presentation=dict(identity_title='오버플로 밸브·M17·LS19/20·ZT04 식별',identity_pending='P&ID M17 0.25kW/OEM2.2kW상충·HE01 PSH03 소유/공유함·실물미확정',oem_baseline='Electrical_Rev2.pdf FG38/39/75/146 개정란공란 DATE27.05.2024;FG108/118/123/137/138 Rev2 17.03.2025. M17 2.2kW4.31A 대P&ID0.25kW·현재보호설정미확정',construction_baseline='Electrical_Can_Decoating_20241118.pdf PDF51/56 24.11.11firstdraft·M17 CV4core1.5/FLO1TB1shared/LS19/20 DC2C1/ZT04 TM4S1/HE01 PSH03 AI4S1·가려진행제외/준공미확정',control_title='압력 비교·세정/기동·150초·엔코더 고유 경계',control_links=[['출력1706','networks/network-1706.html'],['교정1707','networks/network-1707.html'],['HSC1758','networks/network-1758.html'],['별도CONT_S15','networks/network-15.html']],timer_title='Tag94 T3 · S5T#150S 방향응답 감시',related_title='±3400누적·입력NOT·압력/위치OFR·버너 요청',related_links=[['누적1714','networks/network-1714.html'],['환산1764','networks/network-1764.html'],['압력1747','networks/network-1747.html'],['버너소유1868','networks/network-1868.html'],['HMI1191','networks/network-1191.html']],field_title='M17 용량상충·NC회로·PSH03 라벨/소유·ZT04 TM',alarm_recovery='정확한DB/태그·최초원인시각·Q/접촉기응답/raw·처리리미트/누적/실카운트/OFR/W/B/Reset을구분합니다. 고장해제·카운트0·교정요청0은 실제영점/안전/현장복구의증명이아닙니다.',search_examples='Q1.7, I7.6, ZT04, PSH03, S5T#150S, W29, 3400, CH0.A, NOT Close AND Close',circuit_destination_by_signal={'열기 방향 명령':correction,'닫기 방향 명령':correction})))

def build_mv06_profile(root,data,source_rows):
    regulation=next(p for p in json.loads((root/'registers/regulation-manual.json').read_text())['loops'] if p['id']=='MV06')
    control=json.loads(json.dumps(regulation))
    control['chain'][0]=control['chain'][0].replace('<-5','≤−5')
    control['chain'][1]=control['chain'][1].replace('원시IW286','원시PIW286')
    control['repair'][1]=control['repair'][1].replace('원시IW286','원시PIW286')
    control['chain'] += [
        'P21/MV06→M14 오버플로 밸브 후보. P&ID·OEM M14 0.25kW,OEM0.76A. OEM LS40/41와 시공 LS34/35,ZT06·FLO4TB2A 중복구간의 동일성은 실물/준공 확인전입니다. 공통30AS1은 MV02/MV05/MV06 세장치 전원으로 MV06 전용으로 병합하지 않습니다.',
        '정정 근거:1709/0347은 Ge618 Err≥5와 Le624 Err≤−5입니다. 보존된 regulation-manual의 <-5는 XML Le와 불일치합니다. 1710/0348 PSH02는 AO2288 Int Peripherie PIW286이며 원자료 IW286 설명과 구분합니다. 파생 원자료와 수신초안은 변경하지 않습니다.',
        '1709 ON675·SP≠0→Sub598 Data.PSH02_SETPOINT DB1W42−Data.PSH_02 DB1W196→Local Int ErrPSH02. !Tag149677 T135→SD605 Tag150 T136 S5T#300MS;Tag150679→SD610 Tag149 S5T#4S. !Tag150681→Ge618≥5 DOWN M13.3/Le624≤−5 UP M13.2. 현재단위·주기·안전 적절성은 미확정입니다.',
        '1710 ON807·Auto809·SP=0 Eq693·!ShotClose811·!ShotOpen813→PIW286 Int≤0 Le701→SD707 Tag151 T140 S5T#20S→815→S712 ShotClose M18.0;>0 Gt715→SD721 Tag152 T143 S5T#2S→817→S726 ShotOpen M18.1. 원시0을0mbar로 단정하지 않습니다.',
        '같은1710 ON807→(ShotClose819 OR ShotOpen821) OR729→SD735 Tag153 T141 S5T#300MS→823→R741/R743 두Shot. 이 Reset 가지에는 Auto·SP=0 직렬조건이 없습니다. SD 값과 실제 밸브 이동시간을 구분합니다.',
        '1711/0349 공통 앞단 !ON915→W916→!FAULT931. Q1.1 Coil821=공통·((Auto933·(UP935 OR ShotOpen937)) OR (FlagOpen939·(Pulse941 OR ON943)))·!Qclose945·!InputsOpen947. Q1.2 Coil837=공통·((Auto949·(DOWN951 OR ShotClose953)) OR (FlagClose955·(Pulse957 OR ON959)))·!Qopen961·!InputsClose963.',
        'ON915는 Negated operand이며0617 RID1 M0.0/ORef28 W27입니다. 다른 ON943/959도 같은 RID1입니다. 보존 원문을 정방향ON으로 정상화하지 않습니다. 정적 반전/분기 상충은 현재 프로젝트·호출·다른쓰기·CPU 동작을 확인한 결과가 아닙니다. 자동경로에는 Pulse OR ON 직렬요구가 없습니다.',
        '1711 !ON915·!ON917→(InputsOpen919 OR FlagClose921 OR Auto923)→R794 Flag.MV06_Open DB2X10.5;대칭 InputsClose925 OR FlagOpen927 OR Auto929→R801 Flag.MV06_Close DB2X10.6. startup404/0149 ON337→S310 Auto DB2X6.5(W334/ORef322 RID47). 요청 비트 해제와 물리위치는 별개입니다.',
        '1712/0350 ON846·!Tag154848 T78→SD813 Tag155 T79 S5T#200MS;Tag155850→SD818 Tag154 S5T#2S;!Tag155852→Coil823 MV WORK PULSE M10.0. 1711 수동 Pulse OR ON을 항상 필수펄스로 해석하지 않습니다.',
        '1713/0351 SD1225/1230 Tag156/157 T118/119 S5T#10MS→!Tag1571645→PBox1235 M50.7→ON1677:Qopen1679→Add1418 W19 DB6W38+1/Move1424 W20=0;Qclose1681→Sub1433 W20 DB6W40−1/Move1439 W19=0. 명령누적과 ZT06 실측카운트는 다른 값이며 초로 환산하지 않습니다.',
        '1714/0352 ON1943·ON1955→Gt1752 W19>2200→S1758 FAULT DB3X11.6/Move1761 W19=0;Lt1766 W20<−2200→S1772 같은FAULT/Move1775 W20=0. ±2200 경계는 엄격비교입니다. 누적0과고장Reset을 혼동하지 않습니다.',
        '1226/0159 ON513·ON565→[(Qopen567·!RunOpening571) OR (Qclose569·!RunClosing50)] OR52→SD329 Tag97 T16 S5T#150MS→573→S334 동일FAULT DB3X11.6. 0571 RID8 SV150MS/V21,인접MV03 150초와 다릅니다. ON513·RESET575·자기FAULT587→R362에는 응답정상화 직렬조건이 없습니다.',
        '1760/0510 !Simulation21 M180.0·EM_OK22 I19.4→High_Speed_Counter LRef23/Instance24 MV06_Encoder DB19. 23핀중 SwGate W55/ORef27·CountValue W75/ORef47만 RefId결속,21핀 미결속입니다. ErrorAck/EventAck/SetCountValue를0/FALSE 또는 MV01 방식으로 채우지 않습니다. 실제TM/IO 내부offset 미확정입니다.',
        '1766/0516 EM_OK1529·!raw MV06_Close1531 I7.0→Coil1441 SW_GATE4;Add1446 Memory encoder.Encoder_CH04 DInt DB8D16+fill_unit1.ACT_CNTV4→Local CNT_Act_4→ENO Div1450 DInt100→Local CNTV4_100→ENO Move1454 DInt→Int CH04_10 DB8W44. ORef1489 RID265는 CNTV4_100입니다. 수신초안 Move입력 표현을 원본으로 구분합니다.',
        '같은 EM_OK·!SW_GATE4 Contact1533→Move1463 Int0 CH04_10·Move1468 INT#0 literal327→DInt CH04. CRef1475 Signal linearization은 EM_OK 공통앞단;IN0=ON,Analog CH04_10,Coeff DB4W224,Zero DB4W222,Out Pot_MV06 DB1W136,OFR DB3X25.2(W24). S=S/IO 내부offset·현재계수·범위·단위는 미확정입니다.',
        '1761/0511 !EM_OK963→Move937 Local CNT_Act_4→CH04 W960/961 별도기억쓰기. 전원복귀 보장은 확인전입니다. 보존0635 RID327 NID2 UID643/651에 Pot_MV06 다른쓰기 선언이 있으나 중지0403을 작성·수정·생성·실행·행동시험하지 않습니다. 네이티브/P&ID/HMI에서 MV06 교정Reset 절차는 확인되지 않아 복제하지 않습니다.',
        '1658/0291 IN0·Analog Int>−1382·≤32767→Convert164/167 DInt→Add170(input+Zero)→Convert174 Coeff→Mul177→Div181 DInt28000→Move185 Out Int. >32767 OR≤−1382→Move193−9999→ENO ordinaryCoil23 OFR. 1659/0014 !IN0 Contact171→Move162 Out0. 실제범위·복구·단위는 확인전입니다.',
        '1746/0496 ON475→Signal linearization CRef456:Analog PSH02:P PIW286 Int AO2288,Coeff DB4W42/Zero DB4W40,Out Data.PSH_02 DB1W196,OFR DB3X22.1. 0642 RID99 NID1 UID3641는 PSH02_SETPOINT DB1W42 다른쓰기 선언입니다. 원인허가·현재설정은 이 선언만으로 확정하지 않습니다.',
        '1186/0363 !Contact63의RID120 Comulativo는 미결속 후보→Coil64 Start Aux INV Q1.0. HMI Standard Motors CRef23/CodeBlock22 실인수8 중3FALSE·5선언미해석입니다. 공통인버터 기동이 MV06 개별방향/개도를 뜻하지 않습니다.',
        '1821/0455 ON1816→StartAux1837 Q1.0·!같은Q Contact22→W25가 두Set가지에 공통입니다. !InputsAuxRUN1818→TON24/Instance27 Aux_Inv_run DB31 PT2s→Q→S1792 Aux_Inverter_Fault DB3X17.2;InputsAuxAll1827→S1828 Aux_INV DB3X20.0. 동일Q 직렬상충을 보존하며 현재알람 불능이라고 단정하지 않습니다.',
        '공통알람Reset ON1816·RESET1820→자기Fault1822·RUN1824→R1798;AuxINV1835→R1836에는RUN 직렬조건이 없습니다. TON ET W39는 RefId없음. 개별MV06_FAULT·공통인버터 Fault/AuxINV·위치/압력OFR·HMI 표시·HSC진단을 각각 기록합니다.',
        '1070/0397 Move22 IW0→Inputs DB13W0,Move42 IW6→DB13W6의 Word전달. MV06 개별 리미트 NOT처리는 확인된 경로에 없습니다. raw I6.7/7.0·처리 DB13X6.7/7.0·접촉기I1.6/1.7·HMI DB11 표시를 별도 층으로 확인합니다.',
        '1187/0364 Motorized Valve CRef23/CodeBlock22 14실인수중4FALSE·10선언미해석입니다. HMI CSV8행 DB11X28.0~28.4/DB2X10.5/X10.6/X6.5와 물리Q/FAULT/엔코더는별개입니다. MV01/MV03 ResetEncoder를 추가하지 않습니다.',
        '1613/0030 Recipes→HMI→HMI Output ENO W32/33/42 뒤 !Simulation37 M180.0→W43 HMI Inputs CRef28. 정적호출 경계만 확인했으며 TIA/현재CPU/현장/가상실행 확인을 대신하지 않습니다.'
    ]
    control['repair'] += [
        'FG137 MOD14term12 Q1.1→32KM2 NC31/32→32.1→32KM1 A1/A2;term13 Q1.2→32KM1 NC→32.2→32KM2. 공통A2→32.3→32QM1보조→32.4→XS19→32QS1보조→XS20→−0Vdc10.6. +24V→접촉기13/14→I1.6/1.7 FG117term17/18. 현재배선·전압·보호값 미확정.',
        'FG30 440V60Hz6.2L1/2/3→30QM1 범위5.5~8A/RATING6.9A→30AS1 ACS35503E04A14 도면1.5kW→공유30U/V/W→32QM1 .7~1A→32KM역상→XM→32QS1→M14 .25kW.76A/PE. 현재ABB모델/설정/실물은 확인전입니다.',
        'FG31 Q1.0 MOD14term11→30QM1보조31.1→31KA1 A1/A2−0V10.6. FG30 inverterterm9 +24→30.1→31KA1 실제부하접점5–9→30.2→DI1term12;Reset17KA2도 실제5–9→30.7→DI4term15. 코일교차참조1/5/9와 그린 부하5/9를 구분합니다. 보존 회로nodes1→9는불일치입니다.',
        'FG14 STO14KA2/6 부하접점1/2·코일13.5/13.4 및13.6/13.5·A2 0Vac9.9는 DC릴레이와다릅니다. FG30 RUNNING17+24→19I1.4/ALARM20+24→21I1.5/−0V22·10GND·11DCOM. 알람현재극성/안전회로 현재기능 미확정입니다.',
        'FG33 +24→X63 2AF→33.5 LS40 NC11/12→64 I6.7 FG122term28;X65→LS41 NC→66 I7.0 FG123term31. OEM LS40/41와 시공 LS34/35 후보를 동일설비로 확정하지 않습니다. NC·raw·처리Word·정상극성/단선반응을 구분합니다.',
        'ZT06 B+24→58/33.1 FG148term9,C0→59/33.2term10,D→60/33.3 CH0.Aterm1,E→61/33.4 Bterm2,shield62/33SCH1. CH0.Nterm3 미배선표시·E22/A10 SPARE는 카운트주소가아닙니다. 실제TM18 모델·채널·분해능/단위미확정.',
        'FG75 PSH02 +24→X175 50mAF→75.2센서+;센서−→176 PEW286 FG107term34 I7+,term36공통−/44M,shield177/75SCH2. P-BADR 0/10mbar4–20mA·OUTPUT MV03 제목과 MV06/PSH02 논리소유를 구분합니다.',
        '시공PDF51 row1_14 FLB+MV06-M14 ADAC/PVCS4core1.5SBspare0 LEN59;PDF33 FLO_BZONE03 M14/LS34·35/ZT06. PDF58 row8_6 FLO4TB2A TM4S1 LEN63와같은ID8_17 UC01→FLO4TB2 LS34/35 DC7G1spare2 LEN9는별개구간입니다. LS34/35 DC2C1 LEN3·ZT06 TM4S1 LEN4/PSH02 AI4S1 LEN55;PDF56 6_6 ZT06과6_20 ZT05는별개대조후보. 가려진행제외/준공미확정.'
    ]
    control['pending'] += ['반전ON·공통인버터동일Q직렬상충/현재호출·다른쓰기','≥5/≤−5 PIW286 대환산단위·저범위20/2초·Shot300ms','150ms방향응답/엄격±2200누적/동일FAULT·현재안전성','HSC21미결속/HMI10미해석/TM18내부offset·Reset절차미확보','LS40/41 대LS34/35·ZT06 대ZT05/중복FLO4TB2A구간','ABB공유30AS1/START·RESET5/9/STO·현행보호/실물','PSH02센서범위/OUTPUT MV03 제목/현재 계수·設定쓰기']
    control['native']=sorted(set(control['native']+[404,1070,1186,1187,1226,1613,1658,1659,1712,1713,1714,1746,1760,1761,1766,1821]))
    rows=[('MV02·MV05·MV06 공통 인버터 기동',1186,'64','공통Q1.0'),('공통 인버터 응답 · 백업 power_ok',1821,'1818','처리 Aux RUN 부정접점'),('공통 인버터 이상',1821,'1827','처리 Aux All 접점'),('열기 방향 명령',1711,'821','Q1.1 최종열기'),('닫기 방향 명령',1711,'837','Q1.2 최종닫기'),('열기 접촉기 응답',1226,'571','처리 RunOpening 부정접점'),('닫기 접촉기 응답',1226,'50','처리 RunClosing 부정접점'),('열림 끝단 위치',1711,'947','처리 Open 부정접점'),('닫힘 끝단 위치',1711,'963','처리 Close 부정접점'),('엔코더 위치 채널 · 주소 미확정',1760,'75','HSC CountValue/21미결속핀')]
    pairs=[dict(signal=s,network=n,uid=u,label=l,boundary='공통인버터와MV06개별방향·접촉기응답/raw·처리끝단·실측엔코더를구분합니다. 반전ON·같은 Q직렬상충은원문그대로이며현재CPU/실물/정상극성/현장복구미확정입니다.')for s,n,u,l in rows];pairs[-1]['kind']='wire'
    mapping=json.loads((root/'sources/decoded-original/network-map.json').read_text());extra=[]
    for n in [1186,1187,1658,1659,1709,1710,1711,1712,1746,1760,1761,1766,1821]:
        m=next(x for x in mapping if x['document_id']==n);xml=ET.parse(root/'sources/decoded-original'/m['xml_file']).getroot();ns={'s':xml.tag.split('}')[0][1:]};extra.extend((n,'part',p.get('UId'))for p in xml.findall('s:Parts/s:Part',ns));extra.extend((n,'wire',w.get('UId'))for w in xml.findall('s:Wires/s:Wire',ns))
    for n,parts in [(404,'337 310'),(1070,'22 42'),(1613,'37'),(1226,'513 565 567 571 569 50 52 329 573 334 575 587 362'),(1713,'1639 1641 1225 1643 1230 1645 1235 1677 1679 1418 1424 1681 1433 1439'),(1714,'1943 1955 1752 1758 1761 1766 1772 1775')]:
        m=next(x for x in mapping if x['document_id']==n);xml=ET.parse(root/'sources/decoded-original'/m['xml_file']).getroot();ns={'s':xml.tag.split('}')[0][1:]};ids=set(parts.split());extra.extend((n,'part',p)for p in ids);extra.extend((n,'wire',w.get('UId'))for w in xml.findall('s:Wires/s:Wire',ns)if any(e.get('UId')in ids for e in w))
    extra += [(1613,'wire',x)for x in ['32','33','42','43','44']]
    corrected='원본1711 !ON915·!FAULT와모드·반대Q·처리끝단 조건을비교합니다. MV06 교정Reset 절차는확인되지않았습니다. PLC반대Q/하드웨어NC31/32·현재호출/실물복구를별도로확인합니다.'
    common='FG30 실제 START31KA1 부하접점5–9입니다. 원자료nodes1→9와불일치하며원본은보존했습니다. MV02/MV05/MV06 공통기동은MV06 개별방향/개도를대신하지않습니다. 현재배선/동작미확정입니다.'
    return build_static_profile(root,data,source_rows,dict(catalog_id='MV06',priority_key='P21',type='motorized_valve_shared_inverter',control_reference=control,source_pairs=pairs,extra_locations=extra,
        extra_sources=['sources/live_index.json']+['sources/decoded-original/'+f+'-IdentXmlPart.xml'for f in ['0062','0063','0563','0564','0570','0571','0572','0573','0611','0612','0617','0618','0619','0620','0623','0624','0626','0627','0628','0635','0642','0654','0655','0656','0657','0658','0659','0672','0673','0674','0675','0676','0677','0678','0680','0690','0691','0692','0694']],
        internal_names=['ON','MV06 PID UP','MV06 PID DOWN','MV WORK PULSE','Shot to open','Shot to close','Flag.MV06_Auto','Flag.MV06_Open','Flag.MV06_Close','Data.Pot_MV06','Data.PSH_02','Data.PSH02_SETPOINT','WorkData.W19','WorkData.W20'],
        related_alarm_boundary='MV06_FAULT DB3X11.6 하나에150ms방향응답실패·W19>2200/W20<−2200 누적원이합쳐집니다. 공통Aux_Inverter_Fault DB3X17.2/Aux_INV DB3X20.0·위치OFR DB3X25.2·압력OFR DB3X22.1·HMI DB11X28.2·HSC진단은별개층입니다. 고장Reset/누적0/끝단/물리복구는서로다릅니다.',
        presentation=dict(identity_title='공통인버터·M14·LS40/41 대LS34/35·ZT06 식별',identity_pending='LS명칭상충/중복FLO4TB2A구간·현재 실물/TM18채널/교정절차미확정',oem_baseline='Electrical_Rev2 FG14/31/32/33/75/148개정란공란 DATE27.05.2024;FG17/30/107/117/122/123/137 Rev2 17.03.2025. M14 .25kW.76A/shared30AS1 1.5kW·현재보호/모델미확정',construction_baseline='시공PDF33/51/56/58 24.11.11 firstdraft·M14 PVCS4core1.5SB/FLO4TB2A TM대DC7G1별개구간/LS34·35 DC2C1/ZT06 TM·준공미확정',control_title='반전ON·≥5/≤−5·저범위Shot·공통인버터 경계',control_links=[['출력1711','networks/network-1711.html'],['압력1709','networks/network-1709.html'],['저범위1710','networks/network-1710.html'],['HSC1760','networks/network-1760.html']],timer_title='Tag97 T16 · S5T#150MS 방향응답 감시',related_title='엄격±2200누적·HSC21미결속·공통알람상충',related_links=[['누적1714','networks/network-1714.html'],['환산1766','networks/network-1766.html'],['공통기동1186','networks/network-1186.html'],['공통알람1821','networks/network-1821.html'],['압력1746','networks/network-1746.html']],field_title='공통30AS1/START5–9·LSalias·ZT06·중복케이블구간',alarm_recovery='DB/태그·최초원인시각·Q/공통RUN·접촉기응답/raw·처리끝단/누적/실카운트/OFR/Reset을구분합니다. 0/고장해제/끝단표시는현재안전/실물복구의증명이아닙니다.',search_examples='PIW286, ≤−5, NOT ON, S5T#150MS, W19, 2200, LS34, ZT06, CH0.A, 5–9',circuit_destination_by_signal={'열기 방향 명령':corrected,'닫기 방향 명령':corrected,'MV02·MV05·MV06 공통 인버터 기동':common},circuit_nodes_by_signal={'MV02·MV05·MV06 공통 인버터 기동':['Q1.0 MOD14term11 → 30QM1보조31.1 → 31KA1 A1/A2 → −0Vdc10.6','FG30 30AS1term9(+24V) → 30.1 → 31KA1 부하접점5–9 → 30.2 → DI1term12','30AS1 U2/V2/W2 → 공유30U1/V1/W1 → MV02/MV05/MV06 개별분기']})))

def build_rd01_profile(root,data,source_rows):
    read=lambda file:json.loads((root/file).read_text())
    spec=next(p for p in read('registers/control-spec.json')['specifications'] if p['id']=='RD01')
    control=dict(id='RD01',applicability='reviewed drum, separate cooling fan and EV03 lubrication; no own PID loop identified',controller_evidence=None,
        chain=[
            'P06 킬른과 RD01은 역할 후보 관계입니다. 본체·M03 드럼 구동·M04 냉각팬·EV03 윤활을 이름만으로 같은 설비로 합치지 않습니다. RD01 전용 PID 루프는 보존 대장에서 확인되지 않았습니다.',
            '1936/0243 ON270 M0.0→OR28: FAULT272,INV22,Eq227 Data.SET_PERC_FR01=0,!Inputs.fan RD01 run26,(!R2_GATE_LOOP_ON278·!STANDBY_ON280·!UNDER TESTING35)→R236 Flag.M_RD_01 DB2X0.1. 마지막 세 조건은 한 가지이며 전체 OR를 반전하지 않습니다.',
            '1936 별도 ON270·Flag282→Coil240 Start RD01 Q0.1. 요청 Reset과 최종Q,현장 릴레이·회전은 별도 층입니다. 1939/0245 ON307→(팬FAULT309 OR !R2loop311·!Standby313·!UnderTesting318)→R283 Flag.M_RD_01_FAN DB2X0.2;ON·Flag315→Coil287 팬Q0.2.',
            '1684/0465 ON455: Lt406 SP<5→Move409 5/Gt414 SP>100→Move417 100,별도 Mul422 SP×272→W453/O437 RD01_SP_SPEED Word Peripherie PQW290. 0662 RID43·0604 RID44는 같은 Data.SET_PERC_FR01 DB1W6입니다. 설정0의 요청 해제와 제한쓰기의 호출순서·최종값은 현재 자료 미확정입니다.',
            '1843/0164 ON785·!Emergency22·Tipo1 Eq400·Auto823→팬 단계19 Eq466 S469/드럼 단계21 Eq472 S478와 Move481 SP25. 1844/0165 ON1145·!Emergency1154·Auto1147·Tipo2 Eq737→팬33 Eq814 S817/드럼35 Eq820 S826와 Move829 SP25. 단계번호를 초로 환산하지 않습니다.',
            '1847/0166 Auto1095·Tipo5 Eq881→(단계15 Eq935 OR Emergency1118) R939 드럼/(단계17 Eq945 OR Emergency1114) R948 팬. 이 네트워크에 임의 ON 직렬조건을 추가하지 않습니다. 0642 RID92 NID1 UID3840은 같은SP 다른쓰기 선언이며 전체 호출·HMI 설정쓰기 최종값 미확정입니다.',
            '1938/0244 ON295·StartRD297→!Tag115 T58 Contact299→SD257 value Data.EVFR01_Work_time DB1W92,operand Tag116 T59;Tag116 Contact301→SD262 value Data.EVFR01_Wait_time DB1W94,operand Tag115 T58. !Tag116 Contact303→ON305→Coil268 EV03 Q5.1. 이 명령으로 실제 윤활 유량/밸브 위치를 확정하지 않습니다.',
            '1937/0275 KF_KT CRef36/CB35 RID241 Interface248: KF Data.EV_03_W DB1W312,SEC Bool0,KT Work Word92;ENO→CRef45/CB44 KF Data.EV_03P DB1W314,SEC Bool0,KT Wait Word94. 0058 FC109 선언과0059 핀형식을 대조했으며 SEC0만으로 단위/변환식/현재주기를 채우지 않습니다. KF_KT 본문·시간설정의 실제 쓰기와 포맷은 자료 대기입니다.',
            '1787/0424 ON351·Start353→(!Inputs.RD01 run374 OR Inputs.RD01_All_inv378) OR32→SD315 Tag54 T49 S5T#5S. 같은 타이머 접점355 이후 !RUN357→S321 RD_01_FAULT DB3X0.1;INV364→S365 RD01_INV DB3X19.1. 두 래치는 독립이며 5초가 실제 정지/보호 적절성을 증명하지 않습니다.',
            '1787 ON351·RESET359→자기FAULT361 R326/자기INV372 R373. 해제 경로에는 원인 입력 정상화 직렬조건이 없습니다. 1788/0425 ON385·Startfan387·!Inputs.fan RD01 run398→SD349 Tag55 T52 S5T#2S→389·!RUN391 S355 팬FAULT DB3X0.2;ON·RESET393·팬FAULT395 R360. 드럼5초와 팬2초를 공유타이머로 합치지 않습니다.',
            '1931/0238 ON91·OR8(LOW TC03 temp95,OxigenFault97,OxHigh99,Standby101,MAXMAXTC09 103,Hydrogen105,!R1Gate107,!raw RD01_Fbk22)→Coil66 Local InterfaceAccess Disable_Load_RD01. 0605 RID16 SSD AO1은 절대M/DB주소가 아닌 Local 오프셋입니다.',
            '1932/0239 Contact155 RID16→OR97.in6→R109 Flag.M_BWF01;1933/0240 Contact193 같은 Local RID16→OR135.in6→R147 Flag.M_BWF02. 공급기 요청 해제와 드럼 자체 요청/팬 출력은 별도이며 BWF02를 P04 본체로 확정하지 않습니다.',
            '1934/0241 ON206·(Flag.M_BWF01 Contact27 OR Flag.M_BWF02 Contact232) OR36→(!Inputs.RD01 run202 OR !Inputs.BC01 run224) OR31→R228 BWF02→R210 BWF01. 다른 OFF·6분 Tag114 가지와 각각 구분합니다. RD01 응답만으로 공급기 전체 소유나 현재 정지를 확정하지 않습니다.',
            '1857/0174 ON207·!MAXMAXTC09·!BURNER_START_FAULT·!BURNER_LDU_FAULT·FN01·FN04·RD01 처리응답32·(FN06응답36 OR BurnerOn228)·FN02→Coil182 Burner_ready. 1955/0257 ON796·(MBVA01_FAULT798 OR !RD01 run22·!UNDER TESTING802)→R772 FN06요청,별도 ON·FN06요청804→Q3.3. 외부 버너 내부 순서를 추정하지 않습니다.',
            '1070/0397 powerrail Move22 IW0→Inputs DB13W0. 보존 확인 경로의 RD01 개별비트 NOT처리는 확인되지 않았으며 raw I0.2/0.3/0.4와 처리 DB13X0.2/0.3/0.4를 구분합니다. 중지 simulation1082의 두 응답쓰기 참조는 정적 원문으로 보존하고 실행하지 않습니다.',
            '1071/0398 powerrail Move144 W157/O148 RID105 RD01_Current Input SAM=None IW332→W159/O149 RID107 Inputs.RD01_ABSORBPTION DB13W64,ENO→다른 FN01 Move145. 1771/0519 같은 바이트의 RD01_Current는 Int Peripherie PIW332 AO2656입니다. process-image 접근과 Peripherie 접근을 같은 전달로 병합하지 않습니다.',
            '1771 ON1515→Signal linearization CRef1496: IN0 ON,Analog PIW332 W1511/O1504 RID285,Coeff DB4W102,Zero DB4W100,Out Data.Amp_RD01 DB1W100 W1514,OFR Allarm.RD01_Absorbption_OFR DB3X24.1 W24. HMI I_RD01_ABSORBPTION DB13W64와 환산 Data.Amp_RD01은 다른 값이며 실제 단위·인버터AO2 기능/스케일 미확정입니다.',
            '1658/0291 IN0·Int Analog>−1382·≤32767→Convert DInt/addZero/mulCoeff/div28000→Out Int. >32767 OR≤−1382는−9999쓰기 이후 ordinaryCoil OFR;1659/0014 !IN0→Move0 Out. 0·−9999·OFR와 고장Reset/실제 측정복구는 별개입니다.',
            '1019/0309 Tag47 T13·raw RD01_Fbk I0.2→Add1162 MIN+1 DB9W80;MIN≥60→Move1172 literal1 HOUR DB9W82→ENO Move1175 MIN0→S1178 FlagAggiornaDB. 1020/0310 팬 rawI0.4의 MIN DB9W84/HOUR DB9W86도 HOUR Move1입니다. 1049/0336 Tag48 T17→Move2822 literal0 드럼HOUR→팬 등 다른 연쇄쓰기. 누적시간 증가로 정상화하거나 타이머 주기를 추정하지 않습니다.',
            '1179/0358 HMI Standard Motors CRef23/CB22의8실인수는3FALSE·5선언미결속입니다.1180/0359 CRef22/CB23은4FALSE·4미결속. RID를 다른 CID/블록 선언에서 차용하지 않습니다. HMI RD_01 DB11X2.0/.1,팬DB11X4.0/.1,요청DB2X0.1/.2,Editor DB26W12·전류DB13W64는 보존 태그 주소이며 현재 이벤트/읽기/쓰기는 확인 전입니다.',
            '1220/0396 EV03 Q5.1 Contact23→Coil27 ORef28 RID790,!EV03 Contact29→Coil30 ORef32 RID791은 출력명령을 따라가는 표시 후보입니다. 두 출력 선언은 미결속이며 HMI LS_Open/Close 이름을 실물 리미트 센서/밸브 위치로 바꾸지 않습니다.',
            '1613/0030 Recipes→HMI→HMI Output ENO W32/33/42 뒤 !Simulation37 M180.0→W43 HMI Inputs CRef28. 정적 호출 경계만 확인했고 TIA/현재CPU/현장 또는 가상실행을 확인한 결과가 아닙니다.'
        ],repair=[
            '드럼 요청/최종Q0.1/21KA1 코일·5/9·DI1/raw I0.2/처리RUN/5초Tag54와 팬 Q0.2·22KM1·I0.4/2초Tag55를 같은 시각의 별도 값으로 기록합니다.',
            '설정0 요청해제·하한5/상한100·25쓰기·다른설정쓰기·PQW290·전기4–20mA/인버터표시를 구분합니다. 호출순서/현행 파라미터 없이 운전·보호값을 바꾸지 않습니다.',
            'EV03 Q5.1·21KA2 DC코일·5/9 AC부하·실제윤활 및 Work/Wait Word/KF_KT를 구분합니다. 출력표시/타이머만으로 실물윤활을 완료 처리하지 않습니다.',
            'IW332→DB13W64,PIW332→DB1W100/OFR·실제측정/AO2 설정을 분리합니다. 서로 다른 접근/환산/단위와 미확정 호출을 남깁니다.',
            '투입차단 Local/원료공급기·버너준비/FN06 등 연동은 원문 소유로 기록합니다. 알람Reset/요청Set/출력변화·실제복구·재발을 별도로 확인합니다.'
        ],pending=['킬른/P06·RD01/M03/M04/EV03 실물대응·준공/현행 승인자료','현재ABB모델/AI1·AO2·RO 설정·STO/보호값·정상극성','SP0/5/100/25 및 다른쓰기 호출순서·HMI 이벤트','KF_KT 본문/시간Word포맷·실제윤활·EV03 표시 미결속','HMI 드럼5/팬4 핀미결속·현재DB/CPU/Tag주기·HOUR Move1','M03 SIZE16 대25SB C04·ROT1TB2 위치/케이블소유·공유EV03/04/05','드럼FAULT/INV·팬FAULT·OFR·연동 재요청/현장복구'],
        native=[1019,1020,1049,1070,1071,1179,1180,1220,1613,1658,1659,1684,1771,1787,1788,1843,1844,1847,1857,1931,1932,1933,1934,1936,1937,1938,1939,1955],
        native_refs=[r for r in spec['direct_rules'] if r['블록']!='simulation' and r.get('opaque')])
    drawing=next(p for p in data['drawing_workspace']['profiles'] if p['key']=='P06')
    paths=json.loads(json.dumps(drawing['circuit']['paths']))
    paths[0].update(nodes=['Q0.1 MOD14term2 → XS3 → 20QS1 보조 → XS4 → 21.1 → 20QM1 보조 → 21.2','21KA1 A1/A2 → −0Vdc10.6','20AS1term10 +24 → 20.1 → 21KA1 부하5/9 → 20.2 → DI1term13'],destination='FG20/PDF21 START21KA1 실제부하5/9. RESET17KA1은6/10,STO14KA1/5는3/4. 코일交차참조1/5/9와 실제그린부하를 구분합니다. 현행접속/기능미확정입니다.'.replace('交차','교차'))
    paths[1]['destination']='I0.2 FG116 MOD8term3→1070 IW0/Inputs DB13W0와1787 처리RUN374를 비교합니다. raw/Word/처리·다른쓰기·현재극성/전달은 별도 확인합니다.'
    paths[3].update(backup='%PQW290 / RD01_SP_SPEED',destination='1684 ON·SP하한5/상한100·×272→Word Peripherie PQW290. FG112 MOD7term5 QV1QI1/term8 MANA→FG20 AI1term2/3 4–20mA표기. 현재출력/AI1모드·스케일미확정.')
    paths[4]['destination']='FG20 AO2term8/9→FG109 MOD4term30 I6+/term32 U6−I6− PEW332 4–20mA표기.1071 IW332 SAM=None→DB13W64와1771 PIW332 Peripherie→DB1W100/OFR를 별도 연결합니다.'
    paths += [dict(signal='냉각팬 기동 명령',drawing='A0.2',backup='%Q0.2 / Start fan RD01',fg=22,nodes=['440V60Hz8.3 L1/2/3 → 22QM1(도면1.4~2A) → 22KM1 → XM/22QS1 → M04 .75kW1.67A/PE','Q0.2 MOD14term3 → XS5 → 22QS1 보조 → XS6 → 22.1 → 22QM1 보조 → 22KM1 A1/A2 → −0Vdc10.6'],destination='1939 ON·팬요청→Coil287과팬FAULT/게이트가지 Reset283을 비교합니다.',check='드럼Q0.1/팬Q0.2·실물냉각·접촉기응답을 분리합니다.'),dict(signal='냉각팬 운전 응답',drawing='E0.4',backup='%I0.4 / RD01_FAN_Fbk',fg=22,nodes=['+24Vdc → 22KM1 보조13/14 → E0.4 FG116 MOD8term5'],destination='1788 팬처리RUN398·Tag55 T52 2초/FAULT DB3X0.2와raw/Word/현재극성을 구분합니다.',check='접촉기보조응답은 실제팬풍량/드럼회전의 증명이 아닙니다.'),dict(signal='EV03 윤활 명령',drawing='A5.1',backup='%Q5.1 / EV03',fg=21,nodes=['Q5.1 FG141/PDF142 MOD15term12(21/5) → 21KA2 A1/A2 → −0Vdc10.6','110Vac9.7 → 21KA2 부하5/9 → 21.3 → X1:50 2AF → 21.4 → EV03 A1/A2 → X1:51 → 0Vac9.9'],destination='1938 Coil268·SD Work/Wait Word와1937 KF_KT를 비교합니다. 코일DC/부하AC·실제윤활·표시후보를 구분합니다. FG141 옆A5.0 66/4를A5.1에 적용하지 않습니다.',check='原본FG21 교차선 접속점은DC에 있으며0Vac코일리턴/출력교차참조상충 주장은 원본검토로 취소합니다.'.replace('原본','원본'))]
    rows=[('기동 명령',1936,'240','드럼Q0.1','part'),('운전 응답',1787,'374','드럼 처리RUN 부정접점','part'),('인버터 이상',1787,'378','드럼 처리INV','part'),('속도 설정',1684,'453','Peripherie PQW290','wire'),('전류 전달',1771,'1511','Peripherie PIW332 환산','wire'),('냉각팬 기동 명령',1939,'287','별도 팬Q0.2','part'),('냉각팬 운전 응답',1788,'398','별도 팬처리RUN 부정접점','part'),('EV03 윤활 명령',1938,'268','EV03 Q5.1·타이머Word','part')]
    pairs=[dict(signal=s,network=n,uid=u,label=l,kind=k,boundary='드럼/팬/윤활과 raw·처리·표시·환산·실물응답을 분리합니다. 보존된 정적 핀/도면 대조이며 현재CPU·극성·호출·현장복구는 확인 전입니다.') for s,n,u,l,k in rows]
    mapping=read('sources/decoded-original/network-map.json');extra=[]
    full=[1070,1179,1180,1220,1613,1658,1659,1684,1771,1787,1788,1857,1931,1932,1933,1934,1936,1937,1938,1939,1955]
    for n in full:
        m=next(x for x in mapping if x['document_id']==n);xml=ET.parse(root/'sources/decoded-original'/m['xml_file']).getroot();ns={'s':xml.tag.split('}')[0][1:]};extra.extend((n,'part',p.get('UId')) for p in xml.findall('s:Parts/s:Part',ns));extra.extend((n,'wire',w.get('UId')) for w in xml.findall('s:Wires/s:Wire',ns))
    for n,parts in [(1019,'1208 1210 1162 1169 1172 1175 1178'),(1020,'1262 1264 1216 1223 1226 1229 1232'),(1049,'2863 2822 2825'),(1071,'144'),(1843,'785 22 400 823 466 469 472 478 481'),(1844,'1145 1154 1147 737 814 817 820 826 829'),(1847,'1095 881 935 1118 42 939 945 1114 39 948')]:
        m=next(x for x in mapping if x['document_id']==n);xml=ET.parse(root/'sources/decoded-original'/m['xml_file']).getroot();ns={'s':xml.tag.split('}')[0][1:]};ids=set(parts.split());extra.extend((n,'part',p)for p in ids);extra.extend((n,'wire',w.get('UId'))for w in xml.findall('s:Wires/s:Wire',ns)if any(e.get('UId')in ids for e in w))
    families='0058 0059 0063 0575 0576 0577 0578 0585 0602 0603 0604 0605 0606 0611 0612 0613 0614 0615 0616 0623 0624 0625 0626 0627 0628 0629 0630 0631 0632 0635 0642 0654 0655 0656 0657 0658 0659 0660 0661 0662 0663 0664 0672 0673 0674 0675 0676 0677 0678 0679 0680 0690 0691 0692 0693 0694'.split()
    for path in paths:path.setdefault('native_symbol_references',[])
    # Overlay only this generated display profile; preserved source registers stay unchanged.
    drawing['circuit']['paths']=paths
    drawing['sheets'].append(dict(id='oem-22',kind='OEM 전기',image='assets/circuits/FG22.png',title='FG22 · PDF23 · 냉각팬',source='sources/Electrical_Rev2.pdf',page=23,fg=22,extent='원본 한 페이지',status='원본 대조 · 실물 동일성 확인 전',revision='개정란공란 · DATE27.05.2024'))
    return build_static_profile(root,data,source_rows,dict(catalog_id='RD01',priority_key='P06',type='drum_drive_fan_lubrication',control_reference=control,source_pairs=pairs,extra_locations=extra,extra_sources=['sources/live_index.json']+['sources/decoded-original/'+f+'-IdentXmlPart.xml'for f in families],internal_names=['ON','Data.SET_PERC_FR01','Data.Amp_RD01','Data.EVFR01_Work_time','Data.EVFR01_Wait_time','Disable_Load_RD01'],related_alarm_boundary='드럼FAULT DB3X0.1/INV DB3X19.1은공유Tag54 T49 5초,팬FAULT DB3X0.2는별도Tag55 T52 2초입니다. PIW332 환산OFR DB3X24.1·HMI 표시·투입차단Local·공급기/버너/FN06연동과 각Reset/실제복구는별개입니다.',presentation=dict(identity_title='킬른 후보·M03 구동/M04 팬·EV03 구분',identity_pending='P06/RD01 본체·구동부/팬/윤활의 실물 대응·현행 승인자료 미확정',oem_baseline='Electrical_Rev2 FG14/21/22/66/109/116 개정란공란 DATE27.05.2024;FG17/20/112/136/141 Rev2 17.03.2025. FG141 A5.1은21/5;21KA2코일DC/EV03부하AC. 도면30kW50.1A/.75kW1.67A·현재설정미확정',construction_baseline='시공PDF24/51/55 24.11.11firstdraft·M03 SIZE16 대25SB C04/M04 CV4×1.5·ROT1TB1 공유EV03/04/05/ROT1TB2 구간·준공/소유미확정',control_title='드럼/팬·윤활Word·PQW290/IW332 대PIW332 제어',control_links=[['드럼1936','networks/network-1936.html'],['팬1939','networks/network-1939.html'],['윤활1937/1938','networks/network-1938.html'],['속도1684','networks/network-1684.html']],timer_title='드럼Tag54 T49 · S5T#5S 공유감시',related_title='팬2초·윤활Word·전류OFR·투입/버너 연동',related_links=[['팬1788','networks/network-1788.html'],['전류1771/1071','networks/network-1771.html'],['투입차단1931','networks/network-1931.html'],['버너1857','networks/network-1857.html'],['운전시간1019','networks/network-1019.html']],field_title='M03/M04/EV03·STO·C04 케이블과 실물 대응',alarm_recovery='드럼/팬/윤활 요청·최종출력·릴레이/raw·처리·HMI·FAULT/INV/OFR·연동과 실물회전/냉각/윤활을 같은 시각의 별도 근거로 확인합니다. Reset·설정0·표시만으로 실제복구를 확정하지 않습니다.',search_examples='PQW290, IW332, PIW332, EV03, S5T#5S, S5T#2S, HOUR Move1, 21/5, 5/9, 6/10',circuit_paths=paths,circuit_sheets=[dict(id='oem-22',image='assets/circuits/FG22.png',title='FG22 · PDF23 · 냉각팬',source='sources/Electrical_Rev2.pdf',page=23)])))

def build_br01_profile(root,data,source_rows):
    read=lambda file:json.loads((root/file).read_text())
    spec=next(p for p in read('registers/control-spec.json')['specifications'] if p['id']=='BR01')
    burner=read('registers/burner-interface.json')
    names=['Allarm.BURNER_LDU_FAULT','Allarm.SERVOMOTOR_MIN_POS_ALL','Allarm.BURNER_START_FAULT','Allarm.BURNER_TIME_LIMIT_22H']
    alarm=dict(id='BR01',priority_key='P11',name='GME 버너 외부 인터페이스',boundary='reviewed_static_external_interface',family='burner',note='기존 burner-interface 정적 분석의 LDU/최소위치/시작실패 Reset/22시간 가지와 타이머를 연결합니다. 외부 연소제어기의 화염·퍼지·점화·차단 내부 순서/안전시간·현재 정상극성·복구는 확인 전입니다.',source_networks=burner['selected_networks'],native_networks=burner['native_networks'],alarms=[dict(name=n,actions=[a for a in burner['actions'] if a['name']==n],usages=[],all_static_writers=[],other_scope_usages=[]) for n in names],timers=[a for a in burner['actions'] if a['gate']=='SdCoil'],context_actions=[],request_reset_actions=[],field_verified=False,tia_verified=False,repairs_completed=0)
    control=dict(id='BR01',applicability='GME requests, external contacts, modulation and reviewed static controller references; dedicated combustion protection unverified',controller_evidence=None,
        chain=[
            'P11/BR01은 GME PLC와 버너 전용반010-390 TYPE BP N300 사이 외부 인터페이스입니다. P&ID BR01/AB01 공정과 별도 도면번호35602201_00은 본체/버너반 소유를 확정하지 않습니다. 외부 화염검출·가스차단·퍼지/점화 안전 내부 절차는 원본 미확보입니다.',
            '원시 I17.0~.7/처리 Inputs DB13X17.x/Flag.Start_Burner DB2X5.2/Ready DB2X5.1/AUTO요청 DB2X4.3과 내부 Enable1 M48.0/Enable M48.2/Start M48.3/Auto허가 M15.0/Lock M28.0/Main flame M25.0은 서로 다른 층입니다. 이름이 비슷한 요청/명령/응답을 합치지 않습니다.',
            '1070/0397 Move62: W76/O67 Input Word SAM=None IW16→W77/O68 DB13W16(BAD4)입니다. I17.x 비트를 포함하는 Word 전달이며 개별 정상극성/현재 입력을 확정하지 않습니다. 중지 simulation0412의 처리입력 쓰기 참조는 정적 원문으로 보존하고 실행하지 않습니다.',
            '1857/0174 ON207·!MAXMAXTC09 209·!STARTFAULT211·!LDUFAULT213·FN01 23·FN04 27·RD01 32·(FN06 36 OR BurnerOn228) OR38·FN02 40→Coil182 Ready DB2X5.1. 드럼/팬 응답과 외부 버너 상태를 각각 확인합니다.',
            '1858/0175 ON273→OR213: !Ready275/MAXMAXTC09 277/STARTFAULT279/LDUFAULT281/(OR219의12알람→ON305)→R232 Flag.Start_Burner DB2X5.2. 내부 OR에는 FN03/SERVO_MIN/MAXTC04/05/MAXMAXTC03/01/RO01신호/TC01TC02비교/LowAspiration/PSL_AIR_LOW/HYDROGEN/EmergencyStopTC1_2가 있습니다. 이 목록을 외부 연소보호 전체로 확대하지 않습니다.',
            '1865/0181 ON630: [(OFF632·(MAXTC01 634 OR MAXTC03 636)) OR ProgrammedStop638] OR652→[Gas환산≤30 Le573 OR(FCGas640·FCAir642)] OR572→S579 Lock M28.0. Reset은ON→[(!MAXTC01 644·!MAXTC03 646) OR ON648] OR586→!Programmed650→R588 동일Lock입니다. ON 대체가 있는 원문을 온도정상화 필수로 고쳐 설명하지 않습니다.',
            '1866/0182에는 ON 앞접점이 없습니다. FlagStart634·!Lock636→!FN03요청638·OFF640 S600 FN03요청;별도 FN03Run642→Coil607 Enable1 M48.0와Enable644 M48.2→Coil611 최종Q6.5. 내부기동허가와외부99KA1 접점/실제버너 응답은별도입니다.',
            '1868/0184 ON1634·!Enable1 1636→Move1122 State0/R1127 세척Open/R1130 Enable. 같은가지 !Close28·Close1670→S1669 CloseStartup M180.5는 같은Inputs.MV03 Close RID233 DB13X7.6의 정·부정직렬입니다. 원문상충을 보존하고 현재 실행/비활성 원인으로 단정하지 않습니다.',
            '1868 Enable1가지 State DB6W22:0에서PID_Ref_Temp≥500 Ge1143→Move1146 7/<500 Lt1151→Move1154 1와CleanTime0. 1에서OFF1640에만PanelSP=Max쓰기,Open Set1176/State2;2에서!MV03Open1642→3입니다. 실제 개방완료 절차로 바꾸지 않습니다.',
            '1868 State3 SD1199 Tag143 T31 4M/Tag142 T32→Add1208 CleanTime+1와!Tag142 SD1215 1S;Tag1431650→4. 4에서OFF1652에만SP0,R1237Open,State5;5에서Close1654 OR ON1656→6;6 SD1262 Tag147 T37 1S→7. MV03의 현재 위치/외부 퍼지 시간 적절성은 미확정입니다.',
            '1868 별도 Eq1272 literal77에서 Oxigen_RO01≥60→7/<60→0이며77 진입원천은 확인 전입니다. 7에서S1300Enable/R1303Open/S1306CloseStartup/State8;8 BurnerOn1660→9;9 SD1329 Tag145 T38 30S→10;10→11;11 BurnerOn1664→Coil1354 Start M48.3, !BurnerOn1666→State0와CleanTime0. 같은네트워크 다중쓰기/호출순서·현재CPU는 별도확인합니다.',
            '1867/0183 ON·Tag142 T32→Add625 BR01_CleanTime DB6W24+1;!Tag142 SD632 1S는1868 State3과 동일T32/Word의 별도쓰기입니다. CleanTime계수만으로 실제4분퍼지 완료를 확정하지 않습니다.',
            '1854/0171 ON219·raw LOCKOUT221 I17.1·!APP223 M10.2→S117 LDU DB3X7.4. ON·RESET225 DB2X6.0·LDU227→S123 m491 M10.1/S125APP;APP229 SD133 Tag135 T26 6S→231 R138APP. rawLockout 정상화접점은Reset시작가지에 없습니다.',
            '1854 m491233→SD145 Tag136 T27 2S와Coil149 Reset Q6.7;Tag136235→R156LDU 및SD159 Tag137 T28 2S;Tag137237→R164m491. 내부래치해제/Reset출력/외부버너반 Reset수용/실제복구를 각각 기록합니다.',
            '1855/0172 ON32·FlagStart238→PBox239 PLS M50.0→(!FCGas240 OR !FCAir242) OR244→S245 SERVOMOTOR_MIN_POS_ALL DB3X7.0;ON·RESET246·자기fault247→R248. 처리 FC닫힘 이름(DB13X17.3/.5)과 도면 최소압력S3 명칭은 상충하며 검증된 서보위치보호로 확정하지 않습니다.',
            '1856/0173 ON160·!MAX_MAX_TC09 162 DB3X8.7·!MAX_MAX_TC01_TEMP164 DB3X8.1→Coil150 TemperatureInterlock Q6.6입니다. 두 MAX_MAX와1862의 MAX_TC01/03를 구분하고 외부 도면 MAX.TEMPERATURE FILTER 라벨로 센서소유를 변경하지 않습니다.',
            '1862/0178 ON549→TC01_SETPOINT+20 Add409 LocalApp00/+15 Add415 App01. !처리 BurnerONandOK551→R422 Q7.0. 별도 rawI17.2 Contact553·Q7.0 555→[(ON557·Temp≥App00) OR MAXTC01 559 OR MAXTC03 561] OR436→SP0/FCGas563·FCAir565 SD448 Tag139 T29 50MS→567 R453 Q7.0. raw/처리응답은 별도입니다.',
            '1862 ON·rawI17.2·!Q7.0 569·Temp<App01 Lt457·!MAXTC01 571·!MAXTC03 573→SD465 Tag140 T12 8S→575 S470 Q7.0. 이50ms/8초는 PLC고화염요청쓰기이며 외부점화/화염검출 안전시간으로 사용하지 않습니다.',
            '1863/0179 ON521·BurnerOn523·Q7.0 525→S464 MainM25.0;BurnerOn·!Q7.0 527·Main529→SD472 Tag141 T122 S5T#4S. !Tag141531→Coil477 Q7.1,Tag141533→R481Main;!BurnerOn535→R485Main. 도면 FG99/143의3초와원본4초 차이를 보존하며 실제안전시간을 추천하지 않습니다.',
            '1869/0185 RESET1130·STARTFAULT1132→R1122 DB3X6.7만 원문으로 확보했습니다. 해당래치의 전체Set원천/기동실패시간은 미확보이며 타임아웃을 만들지 않습니다.',
            '1859/0176 ON317·BurnerOn319·Tag138321 T30→PBox268 M51.5→Add270 W5 DB6W10+1;!Tag138323 SD277 1M. ON·!BurnerOn325→Move282 W5=0. 1861/0177 OFF318→W5≥1440 Ge289→Coil292 ProgrammedStop M1.1,병렬≥1320 Ge295→Coil298 TIME_LIMIT_22H DB3X7.7. OFF를False상수로 대체하지 않습니다.',
            '1860/0193 NID25:Tipo≠1·≠2→R23 HMI memoBurnerON;요청Start OR AUTO·!memo·BurnerOn→Setmemo와Counter_StopBurner/Consumo_GAS/PartialProduction0쓰기. memo·!BurnerOn·!M181.0→TON88 Instance97 PT1M→PBox109 M181.0→Add34 정지계수+1. ResetCounter DB41X50.1→Move90 계수0→ENO R104 Reset비트. ET96 RefId없음;W5/LOCKOUT Reset과별도입니다.',
            '1870/0186 ON·Flag.AUTO_BURNER DB2X4.3·!MAXTC01/03·!ProgramStop·StartM48.3·HighFlame DB13X17.7→Coil1172 Auto허가 M15.0;별도OR1175(!Enable1/두고온/ProgramStop/!HighFlame)→SP0. 1871 M15.0→Add1176 WorkPID DB6W12+0→PanelSP DB1W22. 요청자동과허가/현재PID모드는별도입니다.',
            '1721/0416 NID2 OFF194·Manual196→Move165 LocalI_FFWD→WorkPID;OFF·!Manual198→Add171 0+I_Outvalue→WorkPID. 1722/0023 NID3 ON186→Add174 0+I_Outvalue→같은WorkPID. 색인SCL1719/CONT_C STL1720은 보존텍스트근거이며 현재컴파일·OB순서·실제CONT_C실행 근거로 승격하지 않습니다.',
            '1872/0188 ON1350→BurnerOn·SP>Max Move1265Max/별도SP>100 Move1273 100/RemoteQ6.5·SP<0 Move1282 0/(!Remote·SP≤0 OR !Enable1) OR1293→Move1294 0. RemoteOFF만으로SP항상0이 된다고 단순화하지 않습니다.',
            '1724/0417 ON273·PanelSP>AirOut Gt230→Add233 AirOut+1/< Lt239→Add242 AirOut−1. 블록명ogni1s와 현재 호출주기는 별도이며 실제변화율/가스공기비율을 확정하지 않습니다.',
            '1686/0467 ON582→AirOut0/100제한·Mul536 ×272→LocalCalcolo_Aria;추가ON584→Move543 W580/O560 WordPeripherie PQW310 AO2480.1687/0468 ON626·ON628→GasOut0/100제한·Mul590 ×285 W624/O606 Peripherie PQW308 AO2464;ENO→Move22 W24/O26 Output SAM=None QW308→Localtest_out. 접근층·현재최종값은별도입니다.',
            '1752/0502 W610/O603 PIW360→Coeff DB4W62/ZeroW60→Data.GAS_BR_01 DB1W206/OFR DB3X22.7;1753 PIW362→CoeffW66/ZeroW64→AIR_BR01 DB1W208/OFR DB3X23.0;1754 PIW364→CoeffW70/ZeroW68→MASSICO_GAS DB1W210/OFR DB3X23.1,별도Lt666<1 Move669 1;1755 PIW366→CoeffW74/ZeroW72→MASSICO_AIR DB1W212/OFR DB3X23.2. ガ스의1보정을공기경로에복제하지 않습니다.'.replace('ガ스','가스'),
            '1658/0291선형화는Int>−1382·≤32767→DInt변환/AddZero/MulCoeff/Div28000→Out Int;무효는−9999 및ordinaryOFR,1659 !IN0→Out0입니다. 단위/현재스케일·OFR Reset과실측복구는미확정입니다.',
            '1071/0398 Move170 IW360 SAM=None W187→Inputs DB13W76 W189;Move171 IW362 W190→W78 W191;Move84 IW364 W132→W80 W156;Move194 IW366 W196→W82 W197. 이Word/HMI원시전달과Peripherie환산Data/OFR는서로 다른접근이며같은주소만으로병합하지 않습니다.',
            '1219/0395 Contact23 O24 R781→Coil27 O28 R783;Contact30 O31 R784→Coil34 O35 R785의4핀은0063동일범위 선언미결속입니다. HMI10태그의 요청/자동/Ready/HighFlame/BurnerOn/Resetcount·4원시Word는백업주소이고 표시색/현재이벤트/쓰기방향을확정하지 않습니다.',
            '1830/0194 ON·AirOut≥0/5/.../95 비교별Stechio.Gas_crv*를LocalPortata_Presunta_GAS에 씁니다. 구간곡선과 실제가스성상/비율은미확정입니다.1832/0195 NID3 CONT_C LRef663 RID112/Instance664 PID_Stechio DB40:COM_RST=!HighFlame,MAN_ON=ON·((!HighFlame·M80.0) OR OFF),CYCLE100MS,TM_LAG1M,DEADB_W0.1;LMN→LocalCorrezione_Stechio. 12 ORef에RefId자체없음(INT_HOLD,I_ITL_ON,PV_PER,I_ITLVAL,LMN_PER,QLMN_HLM/LLM,LMN_P/I/D,PV,ER)으로미확정유지;튜닝권고가아닙니다.',
            '1834/0196은GasOut0/100별도쓰기;1835/0197 Correzione≤Limite_min/≥Limite_MAX→Sign_lim_min/MAX ordinaryCoil.1874/0189 ON1359·(min1361 OR max1363)→SD1317 Tag146 T90 20S→1365 S1322 Sechio_Limits DB3X7.2;ON·RESET·자기fault·!min·!max→R1329. 다른알람Reset과원인정상화조건이다릅니다.',
            '1875~1877/0190~192 OFF·W5 특정값→TC01_SETPOINT 다중쓰기는독립건조가열참조입니다. 승인현행레시피/시간절차를재구성하지않습니다.1613 Recipes/HMI/HMIOutput ENO뒤 !Simulation37 M180.0→W43 HMIInputs 호출은정적경계이며가상실행0입니다.'
        ],repair=[
            '요청Flag/Ready/FN03·Enable1/Enable/Start·Q6.5/99KA1 코일/5–9·외부응답을 같은시각의 별도값으로 기록합니다. 출력/clean contact만으로 화염·연소안전 완료를 판정하지 않습니다.',
            'LDU/APP/m491/6초·2초·2초/Q6.7·외부LOCKOUT과Reset수용·재발을 각각확인합니다. STARTFAULT는Set미확보,최소위치명/압력라벨상충을남깁니다.',
            '세척State·MV03Open/Close·동일닫힘정부정직렬·State77·T31/T32/T37/T38와 실제외부퍼지를구분합니다. 새순서/보호값을생성하지않습니다.',
            'TC01/02선택값·고온래치·50ms/8초/Q7·3초도면대4초T122/Q7.1·실물전용010-390을대조합니다. 가스/공기비율과PID계수·안전시간 변경근거로사용하지않습니다.',
            'PIW/원시IW/HMIWord/환산/OFR·PQW308/310 대QW308·0/100/1·복수쓰기·실제4–20mA/서보위치/유량을구분하고 시공BR01F중복/C02·단자양끝·현행승인자료를수집합니다.'
        ],pending=['버너전용010-390 TYPE BP N300 원본/현행승인·연소제어기명판/화염·점화·퍼지·가스차단내부소유','현재CPU·ON/OFF·OB순서·다중쓰기·태그/타이머호출·정상극성','최소압력S3 대FC닫힘·KA41반복·시공BR01F중복/C02·A~F 핀배정','세척닫힘상충·State77진입·STARTFAULT Set원천·HMI4미결속·CONT_C12 RefId없음','TC01/02선택SCL/현재튜닝·4–20mA범위·서보위치/질량유량단위·OFR 복구','도면3초대PLC4초와현재안전시간·외부Reset수용/실측화염·복구/재발'],
        native=[1070,1071,1219,1613,1658,1659,1686,1687,1721,1722,1724,1752,1753,1754,1755,1830,1832,1834,1835,1854,1855,1856,1857,1858,1859,1860,1861,1862,1863,1865,1866,1867,1868,1869,1870,1871,1872,1874,1875,1876,1877],native_refs=[r for r in spec['direct_rules'] if r.get('opaque')])
    drawing=next(p for p in data['drawing_workspace']['profiles'] if p['key']=='P11');paths=json.loads(json.dumps(drawing['circuit']['paths']))
    for p in paths[8:12]:p['nodes']=[s.replace('접점1→9','실제 부하 접점5→9')for s in p['nodes']]
    paths[9]['destination']='1856 ON·!MAX_MAX_TC09·!MAX_MAX_TC01_TEMP→Q6.6. DB3X8.7/8.1과外부MAX.TEMPERATURE FILTER 라벨·현재소유는구분합니다.'.replace('外부','외부')
    paths[12]['destination']='1863 Tag141 T122 원본S5T#4S와FG99/143 인쇄3sec의 차이를보존합니다. X1:398 외부종착단자/전용기능·현재안전시간은미확정입니다.'
    paths[14].update(backup='%PQW308 / BR01_GAS_SP (Peripherie)',nodes=['FG114 MOD8term9 QV2/QI2 +PAW308 → GME X1:401 → 버너X1/2/3','공유귀로 버너X1/2/4 → GME X1:400 −100.1 → MOD8term12 MANA / AI귀로'],destination='1687 GasOut0/100·×285→PQW308와별도QW308 SAM=None→test_out을구분합니다.')
    paths[16].update(backup='%PQW310 / BR01_AIR_SP (Peripherie)',nodes=['FG114 MOD8term13 QV3/QI3 +PAW310 → GME X1:405 → 버너X1/3/3','공유귀로 버너X1/3/4 → GME X1:404 −100.2 → MOD8term16 MANA / AI귀로'],destination='1686 AirOut0/100·×272→LocalCalcolo_Aria→PQW310와현재서보응답을구분합니다.')
    drawing['circuit']['paths']=paths
    for fg in [111,114,142,143]:
        assert (root/f'assets/circuits/FG{fg}.png').exists()
        drawing['sheets'].append(dict(id=f'oem-{fg}',kind='OEM 전기',title=f'FG{fg} · PDF{fg+1} · 버너 모듈 끝점',source='sources/Electrical_Rev2.pdf',page=fg+1,fg=fg,image=f'assets/circuits/FG{fg}.png',extent='원본 한 페이지',status='보존 원본 · 현행 승인자료 확인 전',revision='Rev2 17.03.2025'if fg==143 else'개정란 공란 · DATE27.05.2024'))
    rows=[(1870,'1230','처리 Burner HighFlame','part'),(1854,'221','raw LOCKOUT I17.1','part'),(1862,'553','raw MODULATION I17.2','part'),(1855,'240','FC가스닫힘 대최소압력','part'),(1070,'77','IW16→DB13W16 공통Word','wire'),(1855,'242','FC공기닫힘 대최소압력','part'),(1070,'77','IW16→DB13W16 공통Word','wire'),(1870,'1230','처리 HighFlame 대외부밸브삽입','part'),(1866,'611','최종Q6.5','part'),(1856,'150','최종온도인터록Q6.6','part'),(1854,'149','Reset Q6.7','part'),(1862,'470','고화염요청Set Q7.0','part'),(1863,'477','전환Q7.1·T122 4S','part'),(1752,'610','가스PIW360 환산','wire'),(1687,'624','가스Peripherie PQW308','wire'),(1753,'630','공기PIW362 환산','wire'),(1686,'580','공기Peripherie PQW310','wire'),(1754,'686','가스유량PIW364·최솟값1','wire'),(1755,'691','공기유량PIW366','wire')]
    rows[0]=(1868,'1660','처리BurnerOn 대raw/Word/외부응답','part')
    pairs=[dict(signal=p['signal'],network=n,uid=u,label=l,kind=k,boundary='GME 요청/핀·Word·raw/처리·HMI·환산/OFR·외부접점·실측화염/위치를구분합니다. 개별원문핀없는최대압력은공통IW16전달에연결하고 보호조건을만들지않습니다.')for p,(n,u,l,k)in zip(paths,rows)]
    mapping=read('sources/decoded-original/network-map.json');extra=[]
    full=[1219,1613,1658,1659,1686,1687,1721,1722,1724,1752,1753,1754,1755,1830,1832,1834,1835,1854,1855,1856,1857,1858,1859,1860,1861,1862,1863,1865,1866,1867,1868,1869,1870,1871,1872,1874,1875,1876,1877]
    for n in full:
        m=next(x for x in mapping if x['document_id']==n);xml=ET.parse(root/'sources/decoded-original'/m['xml_file']).getroot();ns={'s':xml.tag.split('}')[0][1:]};extra.extend((n,'part',p.get('UId'))for p in xml.findall('s:Parts/s:Part',ns));extra.extend((n,'wire',w.get('UId'))for w in xml.findall('s:Wires/s:Wire',ns))
    for n,parts in [(1070,'62'),(1071,'170 171 84 194')]:
        m=next(x for x in mapping if x['document_id']==n);xml=ET.parse(root/'sources/decoded-original'/m['xml_file']).getroot();ns={'s':xml.tag.split('}')[0][1:]};ids=set(parts.split());extra.extend((n,'part',p)for p in ids);extra.extend((n,'wire',w.get('UId'))for w in xml.findall('s:Wires/s:Wire',ns)if any(e.get('UId')in ids for e in w))
    families='0055 0063 0582 0583 0584 0585 0586 0588 0589 0590 0591 0592 0593 0594 0611 0612 0613 0614 0615 0616 0627 0628 0629 0630 0631 0632 0635 0648 0649 0650 0651 0652 0660 0661 0662 0663 0664 0672 0673 0674 0675 0676 0677 0678 0679 0680 0690 0691 0692 0693 0694'.split()
    return build_static_profile(root,data,source_rows,dict(catalog_id='BR01',priority_key='P11',type='external_burner_interface',alarm_reference=alarm,control_reference=control,source_pairs=pairs,extra_locations=extra,extra_sources=['registers/burner-interface.json','sources/live_index.json','alarm-guides/BR01.html']+[f'assets/circuits/FG{fg}.png'for fg in [111,114,142,143]]+['sources/decoded-original/'+f+'-IdentXmlPart.xml'for f in families],internal_names=['ON','OFF','Flag.Start_Burner','Flag.Burner_ready','Flag.AUTO_BURNER','Data.Burner_Panel_SetPoint','WorkData.BR01_State','WorkData.BR01_CleanTime','WorkData.W5'],related_alarm_boundary='LDU의6/2/2초 Reset·서보최소위치명/압력라벨상충·STARTFAULT Set미확보·OFF22/24시간·Sechio20초원인정상화 Reset·4아날로그OFR를 구분합니다. 세척4분/1초/30초·고화염50ms/8초·전환4초대도면3초는외부안전시간확정이아닙니다.',presentation=dict(identity_title='GME PLC·외부 버너반과 본체 관계',identity_pending='BR01/버너반010-390 TYPE BP N300·현재명판·연소제어기/본체 대응 확인 전',oem_baseline='FG97/98/99/100/111/114/133/142 개정란공란 DATE27.05.2024;FG143 Rev2 17.03.2025. 99KA1~4 부하5/9·DC코일,99KA5 1/5/9 전환·3sec인쇄 대T122 4S. 현재전압/배선/안전시간미확정',construction_baseline='시공PDF6/64 · 24.11.11 first draft design · CR→CC01/BR01 A~F LEN36·F중복C02 보존;개별핀배정/준공/현행 승인미확정',control_title='기동허가·세척State·Reset·고화염·조절/전달',control_links=[['기존 버너전용 분석','burner-interface.html'],['기동1866','networks/network-1866.html'],['세척1868','networks/network-1868.html'],['온도/조절 보존근거','regulation-manual.html#loop-BR01']],timer_title='LDU6/2/2초·1분·고화염50ms/8초·전환4초·세척4분/1초/30초',related_title='Sechio20초·OFR·START Set미확보·세척/외부 보호 경계',related_links=[['기존 외부 인터페이스','burner-interface.html'],['비율한계1874','networks/network-1874.html'],['PID12핀미확정1832','networks/network-1832.html'],['원시Word1071','networks/network-1071.html']],field_title='010-390 전용반·실물화염/밸브·시공BR01F중복',alarm_recovery='발생·래치·Reset요청/PLC출력·외부Reset수용·재요청·현재응답·실측화염/위치·재발을같은시각의별도근거로기록합니다. 내부LDU Reset/카운터0/상태접점만으로외부연소안전복구를완료처리하지않습니다.',search_examples='PQW308, PQW310, IW360, PIW360, State77, 5/9, S5T#4S, 3sec, 50MS, Sechio, BR01F')))


def build_cc01_profile(root,data,source_rows):
    """Passive body candidate; surrounding references do not assign owned I/O."""
    read=lambda n:json.loads((root/n).read_text())
    body=next(p for p in read('registers/body-manual.json')['profiles']if p['id']=='CC01')
    drawing=next(p for p in data['drawing_workspace']['profiles']if p['key']=='P10')
    distinction='CC챔버↔CC01은 역할 대응 후보입니다. 직접 I/O·HMI·LAD·구동부·알람·타이머는 미확보입니다. TC06/RO04는 주변 참고이며 시공 위치 CC01 대 OEM 기능 AB01/FN01 상충을 유지합니다. 접속함 공유는 제어 소유 증명이 아닙니다.'
    paths=[];pairs=[]
    for signal,fg,network,wire,label in [('주변 TC06 직접 입력',78,1742,'391','PIW278 · TC06 주변 환산'),('주변 TC06 원시 Word',78,1071,'88','IW278 · 주변 Inputs.TC_06'),('주변 RO04 직접 입력',81,1751,'590','PIW358 · OFF 호출/IN0 ON'),('주변 RO04 원시 Word',81,1071,'184','IW358 · 주변 Inputs.RO_04')]:
        sensor=next(x for x in body['sensor_references']if x['id']==('TC06'if fg==78 else'RO04'));c=sensor['circuit'];nodes=[c['path'],c['module_pins']+'; 입력단자14 I3+/16 U3−I3−/18MANA · 현행CPU/배선 확인 전',('PIW278 Peripherie→FC63→DB1W120/OFR3X21.5; IW278 SAM=None→DB13W42'if fg==78 else'PIW358 Peripherie→FC63→DB1W78/OFR3X22.6; IW358 SAM=None→DB13W74'),('TC06 OEM OUTPUT AB01 / 시공CC01 TC06A KX2S 구간 상충'if fg==78 else'RO04 OEM OUTLET FN01 / 시공CC01 81RO04A/B 소유 상충')]
        refs=[dict(network=network,uid='384'if network==1742 else'583'if network==1751 else'78'if fg==78 else'174',source='sources/decoded-original/'+{1742:'0492',1751:'0501',1071:'0398'}[network]+'-FlgNet.xml')]
        paths.append(dict(signal=signal,fg=fg,drawing='주변 참고 · Electrical_Rev2 FG'+str(fg),backup=label,nodes=nodes,destination='본체 고유 신호로 배정하지 않습니다. 원시값·환산·OFR·HMI 표시·실물 소유를 별도 대조합니다.',check=distinction,native_symbol_references=refs,ownership_verified=False))
        pairs.append(dict(signal=signal,network=network,kind='wire',uid=wire,label=label,boundary=distinction))
    drawing['circuit']=dict(id='CC01',equipment='본체 전용 회로 미확보 · 주변 TC06/RO04 전기/환산 참고',distinction=distinction,paths=paths,pending=['실물 명판·위치와 CC01/P10 대응','TC06/RO04 실제 취출·변환기·현행CPU·정상극성/계수·HMI 이벤트','ENT2TB1 A/B 두간선·PB16/PB18·BR01F중복 및 승인 양단 심선표'],source_reference_only=True)
    for fg in [78,81,106,110]:
        drawing['sheets'].append(dict(id='oem-'+str(fg),kind='주변 OEM 전기',title='주변 FG'+str(fg)+' · PDF'+str(fg+1),source='sources/Electrical_Rev2.pdf',page=fg+1,fg=fg,image='assets/sensor-circuits/FG'+str(fg)+'.png',extent='원본 한 페이지 · 본체 고유 회로 아님',status=distinction,revision='FG78 Rev2 17.03.2025; FG81/106/110 개정란 공란'))
    if not any(x['id']=='construction-3'for x in drawing['sheets']):drawing['sheets'].append(dict(id='construction-3',kind='시공 구역',title='시공 PDF3 · 구역/기능 소유 분리',source='sources/Electrical_Can_Decoating_20241118.pdf',page=3,image='assets/construction/P03.png',extent='전체 원본',status=distinction,revision='24.11.11 first draft design'))
    drawing['warnings'].extend(['PDF21 3_16 PB16A 대 PDF53 3_16 PB18A/PB18; 현재 번호/기능 미확정','PDF53 검은 가림 행과 PDF21 Delete를 복원하지 않음; PV04/SC12 제외 유지','TC06 시공 TC KX2S 대 OEM4–20mA는 서로 다른 구간 가능; 자동 배정 금지','RO04 전원110Vac·센서4선·출력4–20mA를 별도 추적'])
    extra=[]
    for name in ['0492','0501','0291','0014']:
        m=next(x for x in read('sources/decoded-original/network-map.json')if x['xml_file']==name+'-FlgNet.xml');xml=ET.parse(root/'sources/decoded-original'/m['xml_file']).getroot();ns={'n':xml.tag.split('}')[0][1:]}
        extra.extend((m['document_id'],'part',x.get('UId'))for x in xml.findall('n:Parts/n:Part',ns));extra.extend((m['document_id'],'wire',x.get('UId'))for x in xml.findall('n:Wires/n:Wire',ns))
    extra.extend((1071,'wire',uid)for uid in ['86','88','89','90','182','184','185','186'])
    control=dict(applicability='own body control not identified; reviewed surrounding sensor references only',controller_evidence=None,native=[1742,1751,1071,1658,1659],native_refs=[],chain=[
        distinction,
        '직접명칭 검색: decoded-original XML695개와 live_index/hmi_plc_tags/hmi-windows에서 (?<![A-Za-z0-9])CC[ _-]?0?1(?![0-9]) 대소문자 무시0건. 이는 검색철자/범위의 결과이며 별칭·현행CPU·실물의 부재 증명이 아닙니다. 검색695는 논리695개 의미검토가 아닙니다.',
        '1742/0492 NID12: Contact395 ON M0.0 (Wire389/396)→CRef376.en; IN0 Wire390 ON;Analog391 PIW278(0678RID81/SAM Peripherie/AO2224);Coeff392 DB4W26/Zero393 W24;Out394 Data.Temp_T6 DB1W120;OFR24 DB3X21.5. FC63 Call388. 현재계수/주기/다른쓰기 미확정.',
        '1751/0501 NID21: Contact594 OFF M0.1 (Wire588/595)→CRef575.en; IN0 Wire589 ON M0.0. Analog590 R004 PIW358(0678RID128/AO2864/SAM Peripherie);Coeff591 DB4W58/Zero592 W56;Out593 Data.RO04 DB1W78;OFR24 DB3X22.6;FC63 Call587. OFF를False상수/사용중지/표시0으로 치환하지 않으며 EN미호출과 IN0false 내부0쓰기는 다릅니다.',
        '1071/0398 NID2: Move73 Wire88 IW278 SAM=None→Wire90 Inputs.TC_06 DB13W42;Move169 Wire184 IW358 SAM=None→Wire186 Inputs.RO_04 DB13W74. 전단 ENO86/182와후속89/185 연쇄쓰기·실행 순서 미확정. Int원시 입력 대Word목적지·PIW직접환산·HMI물리값을 구분합니다.',
        'FC63 1658/0291: IN0→Analog_input>−1382 AND ≤32767→Convert164/167→Add170(입력+Zero)→Convert174(Coeff)→Mul177→Div181(28000)→Move185 OutValue. 입력/Zero/Coeff/OutValue Int·중간DInt 변환/오버플로는실수식으로단순화하지않습니다.',
        '1658: >32767 OR ≤−1382→Move193 literal−9999 (원시V55537)→OutValue, Move.eno Wire21→Coil23 Out_of_range. −9999는 물리온도/산소값이 아닙니다. 1659/0014 NOT IN0 Contact171→Move162 literal0→OutValue는함수내부 분기이며 EN미호출을대체하지않습니다.',
        '시공PDF3/6/21/53/64: CC01 ENT2TB1·주변TC06/RO04·12SB3/17HA1·BR01. 두DC간선3_3 A25G1.0/3_30 B12G1.0는별개·AC3_4 25G·PV01분기3_8~11·제외PV04 3_12/13. TC06A KX2S1.0 LEN41,RO04A CVV-S2S1.0 LEN35,RO04B CVV3G1.0 LEN17,17HA1A LEN15;PDF21 PB16A 대PDF53 PB18A/C02 BR01F중복·가림/삭제를보존합니다.'
    ],repair=['관찰 시각·실물 위치·P10/본체/주변 소유를 먼저 기록합니다. 직접 I/O를 대신 만들지 않습니다.','TC06/RO04 raw·환산·OFR·HMI표시를 같은 시각으로 비교하고 OFF값/EN호출을 별도 확인합니다.','투입 이상은 PV01/RD01/BC01/FN06 고유작업지와 본체 관찰을 나누어 배제합니다. 사이렌/버너를CC01 소유로복제하지않습니다.'],pending=['현행 본체명판·기계도/허용기준·실제연결','전용제어·별칭·현재프로젝트/CPU/HMI 이벤트','TC06/RO04 취출 위치/모델·소자→변환기→간선→입력모듈 양단','현재 ON/OFF·계수/단위·호출/ENO/복수쓰기·관찰/실제복구'])
    alarm=dict(id='CC01',note='CC01 고유 알람·타이머 미확보입니다. 정상/무알람 판정이 아닙니다. TC06_OFR/RO04_OFR는 주변 환산의 별도 출력입니다.',alarms=[],timers=[],native_networks=[],source_reference_only=True)
    family=['0611','0612','0627','0628','0629','0630','0631','0632','0672','0674','0676','0678']
    return build_static_profile(root,data,source_rows,dict(catalog_id='CC01',priority_key='P10',type='passive_body_candidate',source_pairs=pairs,extra_locations=extra,extra_sources=['registers/body-manual.json','registers/sensor-measurement.json','sources/live_index.json','sources/hmi-windows.csv','alarm-guides/CC01.html']+['assets/sensor-circuits/FG'+str(fg)+'.png'for fg in [78,81,106,110]]+['sources/decoded-original/'+n+'-IdentXmlPart.xml'for n in family],internal_names=[],signal_reference=dict(id='CC01',signals=[],note='直接신호 미확보·주변 신호를 고유로 배정하지 않음'.replace('直接','직접')),alarm_reference=alarm,control_reference=control,related_alarm_boundary='CC01 고유 발생/래치/Reset/타이머는 미확보입니다. 주변 TC06_OFR/RO04_OFR·−9999/호출EN/IN0와 공유17HA1·BR01을 분리하며 OFR해제를 본체 복구로판정하지않습니다.',presentation=dict(identity_title='투입 챔버 후보·주변 소유와 자료 경계',identity_pending='P10 CC챔버↔CC01 명판·위치·본체·전용제어 확인 전',io_empty_note=distinction,oem_baseline='주변 TC06 FG78/PDF79 Rev2 17.03.2025;RO04 FG81/PDF82·MOD3 FG106/PDF107·MOD5 FG110/PDF111 개정란공란. 본체 전용 회로 미확보',construction_baseline='시공PDF3/6/21/53/64 · 24.11.11 first draft design;ENT2TB1 두DC간선·PB16/PB18·BR01F중복 보존',control_title='본체 직접제어 미확보·주변 TC06/RO04 환산·OFF 호출',control_links=[['본체·주변 자료','body-manual.html#body-CC01'],['주변 TC06','networks/network-1742.html'],['주변 RO04 OFF호출','networks/network-1751.html']],timer_title='CC01 고유 타이머 미확보',related_title='주변 OFR·공유 접속함/사이렌·버너 경계',related_links=[['주변 계측','sensor-measurement.html'],['공통 환산','networks/network-1658.html'],['별도 BR01','alarm-guides/BR01.html']],field_title='CC01 실물·기계본체·주변 취출/양단 경계',alarm_recovery='본체/주변 소유·최초알람·원시/환산·전용제어·조치·실측·재발을 나누어 기록합니다. 고유 알람 미확보는정상이나자동복구완료의근거가아닙니다.',search_examples='PIW278, IW278, PIW358, IW358, OFF, TC06, RO04, PB16, PB18, ENT2TB1, −9999')))


def build_ab01_profile(root,data,source_rows):
    """AB01 body candidate with reviewed measurements; no owned burner sequence."""
    read=lambda n:json.loads((root/n).read_text())
    body=next(p for p in read('registers/body-manual.json')['profiles']if p['id']=='AB01')
    cc=next(p for p in read('registers/body-manual.json')['profiles']if p['id']=='CC01')
    sensors={p['id']:p for p in body['sensor_references']+cc['sensor_references']}
    drawing=next(p for p in data['drawing_workspace']['profiles']if p['key']=='P12')
    boundary=body['boundary']+' TC01/02 원시 입력 참조2개를 유지합니다. 센서 실제 취출·OEM AB01 대시공 HE01/CC01·BR01 및공통Reset 소유는별도확인 전입니다.'
    defs=[('TC01 주변 직접 입력',77,1739,'wire','331','PIW272 Peripherie / DB1W110 / OFR3X21.2','TC01'),('TC02 주변 직접 입력',77,1740,'wire','351','PIW274 Peripherie / DB1W108 / OFR3X21.3','TC02'),('TC01 주변 원시 Word',77,1071,'wire','67','IW272 SAM=None → DB13W36','TC01'),('TC02 주변 원시 Word',77,1071,'wire','70','IW274 SAM=None → DB13W38','TC02'),('TC06 출구 주변 참고',78,1742,'wire','391','PIW278 / DB1W120 / OFR3X21.5 / 시공CC01','TC06'),('TC07 SPARE·OFF 호출',78,1743,'wire','411','PIW280 / DB1W190 / OFR3X21.6 / OFF EN','TC07'),('RO01 주변 직접 입력',80,1748,'wire','511','PIW352 / DB1W130 / OFR3X22.3 / OFF EN','RO01'),('RO02 주변 직접 입력',80,1749,'wire','531','PIW354 / DB1W128 / OFR3X22.4 / OFF EN','RO02'),('RO01 주변 원시 Word',80,1071,'wire','163','IW352 SAM=None → DB13W68','RO01'),('RO02 주변 원시 Word',80,1071,'wire','166','IW354 SAM=None → DB13W70','RO02'),('온도 MAX 원본 래치',77,1979,'part','160','MAX TC01 6초 / 자동히스테리시스 Reset','TC01'),('온도 MAXMAX 원본 래치',77,1979,'part','203','MAXMAX TC01 6초 / RESET_ALLARM 자기래치','TC01'),('TC01/TC02 차온 원본 래치',77,1986,'part','775','NOT disable / >400 OR / <-100 OR >100 /1분','TC02'),('별도 BR01 온도 Interlock',99,1856,'part','150','Q6.6 / MAXMAX / 외부99KA2 5/9','BR01'),('별도 BR01 원격 기동',99,1866,'part','611','Q6.5 / 요청·Lock·FN03·두Enable /99KA1 5/9','BR01')]
    paths=[];pairs=[]
    for signal,fg,network,kind,uid,label,sensor in defs:
        if sensor!='BR01':
            c=sensors[sensor]['circuit'];nodes=[c['path'],c['module_pins']+' · 현행 모듈/배선 확인 전',label,'OEM 기능·시공구역·실제취출/변환기위치·현재단위/계수 확인 전']
        elif network==1856:nodes=['BR01 ON·NOT MAXMAX_TC09·NOT MAXMAX_TC01 → Q6.6','Q6.6→99KA2 A1 /A2→−0Vdc10.6','외부버너X1/2→X1:390→99.3→5/9→99.4→X1:391→외부X1/4','외부010-390 내부안전순서·실제연료차단 미확보']
        else:nodes=['BR01 Start_Burner 요청·NOT Lock·FN03응답→Enable1 M48.0;추가Enable M48.2→Q6.5','Q6.5→99KA1 A1 /A2→−0Vdc10.6','외부X/220V→X1:388→99.1→5/9→99.2→X1:389→외부X1/7','BR01 GME 상태/외부010-390·실제화염은 AB01 본체 시퀀스와 구분']
        nm=next(n for n in read('sources/decoded-original/network-map.json')if n['document_id']==network);xr=ET.parse(root/'sources/decoded-original'/nm['xml_file']).getroot();xn={'n':xr.tag.split('}')[0][1:]}
        ws=xr.findall('n:Wires/n:Wire',xn);w=next(w for w in ws if (kind=='wire'and w.get('UId')==uid)or(kind=='part'and any(c.get('UId')==uid and c.get('PinName')=='operand'for c in w)));oref=next(c.get('UId')for c in w if c.tag.split('}')[-1]=='OCon')
        paths.append(dict(signal=signal,fg=fg,drawing='주변 계측/BR01 참고 · FG'+str(fg),backup=label,nodes=nodes,destination='원시·환산·선택·래치·공통요청·BR01 출력·외부응답·실물 연소를 같은시각으로 구분합니다.',check=boundary,native_symbol_references=[dict(network=network,uid=oref,kind='ORef',wire=w.get('UId'),source='sources/decoded-original/'+nm['xml_file'])],ownership_verified=False))
        pairs.append(dict(signal=signal,network=network,kind=kind,uid=uid,label=label,boundary=boundary))
    drawing['circuit']=dict(id='AB01',equipment='재연소 챔버 후보 · 주변 온도/산소·별도 BR01 인터페이스',distinction=boundary,paths=paths,source_reference_only=True,pending=['P12↔AB01 명판/본체·실제취출','OEM AB01 대시공HE01/CC01·변환기/양단/구간대응','현재프로젝트/CPU/SCL1719·단위/계수·외부010-390 승인안전자료'])
    for fg in [77,78,80,97,99,106,107,110]:drawing['sheets'].append(dict(id='oem-'+str(fg),kind='주변 OEM 전기',title='주변 FG'+str(fg)+' · PDF'+str(fg+1),source='sources/Electrical_Rev2.pdf',page=fg+1,fg=fg,image=('assets/circuits/'if fg in[97,99]else'assets/sensor-circuits/')+'FG'+str(fg)+'.png',extent='원본 한 페이지 · 주변 계측/BR01 포함',status=boundary,revision='FG78/107 Rev2 17.03.2025; FG77/80/97/99/106/110 개정란 공란'))
    drawing['sheets'].append(dict(id='construction-56',kind='시공 케이블',title='시공 PDF56 · HE01/센서·변환기구간',source='sources/Electrical_Can_Decoating_20241118.pdf',page=56,image='assets/construction/P56.png',extent='전체 원본 · 검은 가림 미복원',status=boundary,revision='24.11.11 first draft design'))
    drawing['warnings'].extend(['TC01/TC02 OEM CHAMBER AB01 대시공HE01; RO01/RO02 OEM OUTLET AB01 대시공HE01/변환기MV03; 실제소유 미확정','시공TC KX2S 대OEM변환기4–20mA는 구간차이 가능·자동통합안함','PDF56 6_25 케이블ID MV02 대도착LOC FLA; 검은6_7~10가림 미복원','PDF64 14_3/4 6SB2A/B 간선만으로안전회로·접점극성·등급·PLC비트배정안함; CC01 BR01F중복보존','TC07 FG78/107 SPARE와OFF호출은현재사용부재 증명이아님'])
    extra=[];native=[1659,1722,1613,1619,1621,931,930,1856,1858,1866,1868,1870,1871,1658,1708,1071,1721,1739,1740,1742,1743,1748,1749,1979,1982,1983,1984,1985,1986,1620]
    for n in read('sources/decoded-original/network-map.json'):
        if n['document_id']not in native:continue
        z=ET.parse(root/'sources/decoded-original'/n['xml_file']).getroot();ns={'n':z.tag.split('}')[0][1:]}
        extra.extend((n['document_id'],'part',p.get('UId'))for p in z.findall('n:Parts/n:Part',ns));extra.extend((n['document_id'],'wire',p.get('UId'))for p in z.findall('n:Wires/n:Wire',ns))
    notes=[
        boundary,
        'TC01/TC02 원본명세 입력참조2/출력0/HMI0/직접LAD·규칙0 보존. 관련30네트워크는본체직접30제어가아닙니다. 기록양식전용신호0개를유지합니다.',
        '0489 NID9 ON→C316.EN,IN0 ON,PIW272(SAM Peripherie)→FC63 CoeffDB4W14/ZeroW12→Data.Temp_TC01 DB1W110/OFR3X21.2.0490 NID10 PIW274→CoeffW18/ZeroW16→Temp_TC02 DB1W108/OFR3X21.3.0398 NID2 IW272/IW274 SAM=None→Word DB13W36/W38 ENO연쇄는별도입니다.',
        'TC06 PIW278→DB1W120/OFR3X21.5는 OEMOUTPUT AB01 대시공CC01. TC07 PIW280→DB1W190/OFR3X21.6,RO01 PIW352→DB1W130/OFR3X22.3,RO02 PIW354→DB1W128/OFR3X22.4는OFF M0.1전단EN·내부IN0 ON M0.0입니다. OFF를FALSE상수/현재미사용/원시0으로치환하지않습니다. RO01 Coeff/Zero DB4W46/44,RO02 W50/48,TC07 W30/28. 원시WordDB13W44/W68/W70는환산Data가아닙니다.',
        'FC63 0291/0014의Int/DInt·입력+Zero·Coeff/28000·>−1382 AND ≤32767,이탈−9999/OFR·Move.ENO,NOT IN0의별도0쓰기를보존합니다. EN미호출과IN0 false는별도입니다. 다른쓰기·현재계수/단위/최종값 미확정.',
        'SCL1719는live_index _7ev의검색색인문자이며네이티브SCL본문/컴파일listing미확보입니다. 0650 NID9 EnableTC01/02 DB39X0.0/.1·PID_REF RealDBD2·EmergencyStopX6.0 읽기/쓰기선언은별도근거. 두Enable 평균/OFR disable 가지의선택값미대입·TC02-only의TC01_OFR/EnableTC01 문자를조용히고치지않습니다.',
        '0527 NID1 MAX:ON 선택온도Real>TC01_MAX_ALL IntDB1W68→SD155 Tag99/T85 S5T#6S→S160 DB3X8.0. ResetON 자기MAX→Sub165(설정−5) LocalInt app00→Wire255 Sub.eno→RealLt169→R173/MAX·S175 STOP_HORN;RESET_ALLARM접점없음.',
        '0527 MAXMAX:ON 허가Wire287은Add179(설정+20)와Real비교186/189/192.pre에각각분기하며Add.eno직렬아님. 선택>Localmax_max_tc1 OR >1250.0 OR <−60.0→SD198 Tag100/T86 S5T#6S→S203 DB3X8.1. ResetON RESET_ALLARM 자기래치→R208;이가지에원인해소/온도정상접점없음. 동시Set/Reset최종값·스캔순서 미확정.',
        '0534 NID8 TC01_TC02_COMP_FAULT:ON NOT disable M80.2·(TC01>400 OR TC02>400)→Wire809 Sub754.en·Lt/Gt.pre병렬. IntTC01−TC02→Localapp02 <-100 OR >100→SD770 Tag108/T116 S5T#1M→S775 DB3X9.1. ±100정확값을범위밖에포함안함. ResetON RESET_ALLARM 자기래치→R780은disable/400/차이/시간가지통과안함.',
        '0530 NID4 Oxigen_Fault DB3X9.6:SetON (RO01≤0 OR≥200) ServiceBitM1000.0; ResetON 자기래치≥5 AND≤195 및STOP_HORN Set.0531 NID5 Too_high DB3X9.7:설정>100 별도Move100·SetON값≥설정;ResetON 자기래치에서Sub(설정−10)/비교.pre Wire654병렬→값<app05. 지연없음·현장산소%단위/현재설정미확정.',
        '0532 NID6 Oxigen_LOW DB3X9.4:OFF 선택온도>650.0 RO01≤5→SD599 Tag106/T68 S5T#1M→Set. ResetOFF RESET_ALLARM 자기래치·(RO01≥20 OR 선택온도≤650.0).0533 NID7 RO01_Signal_Fault DB3X4.4:ON NOTdisableM80.1 선택>650.0,RO01−RO02<-20 OR>20·Sub669/비교.pre병렬Wire718→SD685 Tag107/T117 S5T#1M→Set;ResetON RESET_ALLARM 자기래치.',
        'HMI CSV ResetAlarms DB2X13.4≠PLC RESET_ALLARM DB2X6.0.0158 NID9 (Inputs.Reset DB13X19.7 OR HMIReset)→S33 PLC요청/R40 HMI요청.0154 NID4 RESET OR STOP_HORN→SD229 T47 S5T#1S→R235 Reset/R237Horn/R239Blinking. HMI설정CSV11개는현재화면이벤트·단위/배율·권한·온라인쓰기증거아닙니다.',
        'main0031 NID6 ON Wire283은Analog Input/Allarms1/2/3 EN에각각분기;0549 NID7 Wire351 BR01다중호출분기;0032 NID8 Valve Control/Analog Out 별도.0030 NID19 NOT Simulation 뒤HMIInputs ENO연쇄;원본simulation의다른쓰기가능성은읽기참조만하며현재활성추정/실행안함.',
        '별도BR01 0173 ON NOT MAXMAX_TC09 NOT MAXMAX_TC01→Q6.6.0175 MAXMAX/차온/EmergencyStop→ON경로·R232 Start_Burner요청,정확MAX_TC01_TEMP접점없음.0182 Start요청·NOTLock·FN03응답→M48.0;추가M48.2→Q6.5. 요청Reset/출력/외부010-390 내부안전/실제화염은별도입니다.',
        'BR01 0184 상태77·같은MV03Close 정·부정직렬·세정시간/다중쓰기는기존BR01 검토범위로보존합니다.0186 MAX_TC01/MAX_TC03는자동변조/PanelSP0에별도영향·MAXMAX과다름.0416 OFF/0023 ON의PID결과복수쓰기·0346 MV05 소유를AB01시퀀스로복제하지않습니다.',
        'PDF77/106 개정란공란·FG78/107 Rev2 17.03.2025. TC01/02 MOD3 2/4·6/8,TC06 14/16,TC07 22/24;RO01/02 MOD5 2/4·6/8. OEM110VacH705전원/4선소자/4–20출력과시공TC KX·HE01센서/MV03변환기구간을분리. 시공6_25 MV02 ID 대FLA위치·14_3/4 6SB2 간선·가림/BR01F중복 그대로입니다.'
    ]
    control=dict(applicability='body candidate; surrounding measurements and BR01 reference only',controller_evidence=None,native=native,native_refs=[],chain=notes,repair=['같은시각 raw→환산/OFR→선택/Enable→개별래치→공통Reset→BR01요청/두Enable/출력→외부응답→실물결과를분리기록','TC01/02 OEM/시공상충·RO01/02 센서/변환기구간·TC07 SPARE/현재사용·6SB2 전체회로를확인','래치Reset/표시변화만으로본체과열해소·연소보호·재기동/수리완료를확정하지않음'],pending=['현재 SCL1719/컴파일listing/CPU·계수/단위·최종쓰기','OEM/시공/현장명판·취출/변환기·승인양단','외부010-390/35602201_00 안전자료·현재HMI이벤트/권한','고온/내화재/씰/기계본체기준·실측조치/재발'])
    # Display-only transcription of the separately reviewed alarm pins. No state model.
    def act(network,uid,gate,name,text):return dict(network=network,uid=str(uid),gate=gate,name=name,condition=dict(op='read',name=text),evidence='static wire transcription; no execution/owned-body assignment')
    def group(network,name,setuid,resetuid,settext,resettext):return dict(name=name,source_reference_only=True,actions=[act(network,setuid,'SCoil',name,settext),act(network,resetuid,'RCoil',name,resettext)])
    groups=[group(1979,'Allarm.MAX_TC01_TEMP',160,173,notes[6],notes[6]),group(1979,'Allarm.MAX_MAX_TC01_TEMP',203,208,notes[7],notes[7]),group(1986,'Allarm.TC01_TC02_COMP_FAULT',775,780,notes[8],notes[8]),group(1982,'Allarm.Oxigen_Fault',490,501,notes[9],notes[9]),group(1983,'Allarm.Oxigen_Too_high',628,632,notes[9],notes[9]),group(1984,'Allarm.Oxigen_LOW',604,616,notes[10],notes[10]),group(1985,'Allarm.RO01_Signal_Fault',690,695,notes[10],notes[10])]
    timers=[]
    for net,uid,name,literal,wire,oref,text in [(1979,155,'Tag_99 / T85','S5T#6S',244,212,notes[6]),(1979,198,'Tag_100 / T86','S5T#6S',275,233,notes[7]),(1986,770,'Tag_108 / T116','S5T#1M',820,794,notes[8]),(1984,599,'Tag_106 / T68','S5T#1M',640,622,notes[10]),(1985,685,'Tag_107 / T117','S5T#1M',729,707,notes[10]),(931,229,'공통 Tag_160 / T47','S5T#1S',251,243,notes[11])]:
        a=act(net,uid,'SdCoil',name,text);a.update(preset=dict(op='const',literal=literal),value_wire=str(wire),value_oref=str(oref),source_reference_only=True);timers.append(a)
    alarm=dict(id='AB01',note='아래7개는 주변온도/산소 알람의 원본핀 정적 참고입니다. AB01 본체전용알람이나외부010-390 안전기능으로새배정하지않습니다. 명목시간·Reset과실제원인해소/연소/재기동은별도입니다.',alarms=groups,timers=timers,native_networks=[],source_reference_only=True)
    extra_sources=['AB01-INVESTIGATION.md','registers/ab01-independent-investigation.json','registers/body-manual.json','registers/sensor-measurement.json','registers/process-measurement.json','sources/live_index.json','sources/hmi-windows.csv','alarm-guides/AB01.html']+['assets/sensor-circuits/FG'+str(fg)+'.png'for fg in[77,78,80,106,107,110]]+['assets/circuits/FG'+str(fg)+'.png'for fg in[97,99]]+['sources/decoded-original/'+str(i).zfill(4)+'-IdentXmlPart.xml'for i in[564,565,566,567,568,582,584,585,586,611,612,617,619,627,628,629,630,631,632,634,635,648,649,650,651,652,672,674,676,678,680,682,683,684,685,686,688,692,694]]
    return build_static_profile(root,data,source_rows,dict(catalog_id='AB01',priority_key='P12',type='passive_body_candidate',source_pairs=pairs,extra_locations=extra,extra_sources=extra_sources,internal_names=[],signal_reference=dict(id='AB01',signals=[],note='本体'.replace('本体','본체')+'고유 처리/HMI 신호 미확보·주변계측은 제어참고로 분리'),alarm_reference=alarm,control_reference=control,related_alarm_boundary='MAX 자동히스테리시스Reset·MAXMAX요청Reset·차온/산소/OFR·공통요청1초해제·BR01 요청/두Enable/출력/외부안전/실측화염은서로다릅니다. AB01 본체신규알람·퍼지/재기동조건은만들지않습니다.',presentation=dict(identity_title='재연소 챔버 후보·본체/버너/계측 소유',identity_pending='P12↔AB01 실물명판/위치·전용제어·현재설치 확인 전',io_empty_note='본체 전용 출력·처리/HMI는미확보입니다. TC01/TC02 입력참조2개·주변계측·BR01소유와구분합니다.',oem_baseline='FG77/78/80/97/99/106/107/110; FG78/107만Rev2 17.03.2025·나머지개정란공란. 외부010-390 미확보',construction_baseline='시공PDF3/6/56/64;24.11.11 first draft design·AB01기능대HE01/CC01위치·6SB2간선·가림/중복 유지',control_title='주변온도·산소/선택·알람·BR01 소유 경계',control_links=[['보존 본체분석','body-manual.html#body-AB01'],['독립온도분석','AB01-INVESTIGATION.md'],['원본MAX/MAXMAX','networks/network-1979.html'],['원본차온','networks/network-1986.html']],timer_title='주변/공통 시간6개 · 본체전용 아님',related_title='주변OFR·공통Reset·BR01/외부안전·실측경계',related_links=[['주변계측','sensor-measurement.html'],['공통Reset','networks/network-930.html'],['별도BR01','alarm-guides/BR01.html']],field_title='실물본체·센서취출/변환기·외부버너·6SB2 경계',alarm_recovery='원인관찰·환산/선택·래치·공통요청·BR01요청/두Enable·출력·외부반응·물리연소·재발을분리기록합니다. 자료수치를현장보호설정이나수리완료로대신쓰지않습니다.',search_examples='PIW272, IW272, PIW274, PIW352, OFF, MAX_TC01, MAX_MAX_TC01, S5T#6S, S5T#1M, M80.2, RESET_ALLARM, 6SB2, TC02-only')))


def build_he01_profile(root,data,source_rows):
    """Reviewed surrounding evidence; no new body I/O or field identity."""
    read=lambda n:json.loads((root/n).read_text())
    body=next(p for p in read('registers/body-manual.json')['profiles']if p['id']=='HE01')
    sensors={p['id']:p for p in body['sensor_references']}
    drawing=next(p for p in data['drawing_workspace']['profiles']if p['key']=='P13')
    boundary=body['boundary']+' HE01 전용 제어·HMI·신호·알람·타이머는 미확보입니다. 아래는 주변 참고이며 본체 소유/현행 유로/실물 동일성은 확인 전입니다.'
    defs=[('TC03 주변 직접입력',77,1741,'wire','371','PIW276 Peripherie → DB1W112 / OFR3X21.4','TC03'),('TC03 주변 raw HMI',77,1071,'wire','85','IW276 SAM=None → DB13W40','TC03'),('PSH01 주변 직접입력',75,1745,'wire','451','PIW284 → Press_PC01 DB1W134 / OFR3X22.0','PSH01'),('PSH01 주변 raw HMI',75,1071,'wire','109','IW284 SAM=None → DB13W48','PSH01'),('PSH03 주변 직접입력',75,1747,'wire','491','PIW320 → PSH03 DB1W24 / OFR3X22.2','PSH03'),('PSH03 주변 raw HMI',75,1071,'wire','115','IW320 SAM=None → DB13W52 / Move96→97→98 ENO','PSH03'),('TC03 LOW 주변경보',77,1980,'part','347','BWF01 OR BWF02 RUN / MIN 미만 / 3초','TC03'),('TC03 MAX 주변경보',77,1980,'part','377','MAX 초과 / 3초 / 설정−5 자동 해제','TC03'),('TC03 MAXMAX 주변경보',77,1980,'part','420','MAX+50 OR >750 OR <−60 / 3초 / RESET','TC03'),('별도 MV01 CONT_S',77,11,'wire','442','TC03 설정·처리값 → PIDMV01 / 현재 튜닝 미확인','TC03'),('별도 MV03 PSH03 비교',75,1705,'part','256','Err=setpoint−Data / ≥5·<−5 / 4·10초','PSH03'),('별도 RD01 적재금지',77,1931,'part','95','LOW_TC03 → Local Disable_Load_RD01','TC03'),('별도 BR01 시작요청 해제',77,1858,'part','291','MAXMAX_TC03 → GME Start_Burner Reset','TC03')]
    paths=[];pairs=[]
    for signal,fg,network,kind,uid,label,sensor in defs:
        c=sensors[sensor]['circuit']
        paths.append(dict(signal=signal,fg=fg,drawing='주변 계측 참고 · FG'+str(fg),backup=label,nodes=[c['path'],c['module_pins']+' · 현행 배선/모델 확인 전',label,'관련 제어 소유·센서 취출·단위·현재 호출·실물 대응 확인 전'],destination='원시/환산/HMI/요청/출력/실제 유동과 전열을 같은 시각 기준으로 구분합니다.',check=boundary,native_symbol_references=[dict(network=network,uid=uid,kind=kind)],ownership_verified=False))
        pairs.append(dict(signal=signal,network=network,kind=kind,uid=uid,label=label,boundary=boundary))
    drawing['circuit']=dict(id='HE01',equipment='열교환 본체 후보 · 주변 계측/댐퍼/팬 참고',distinction=boundary,paths=paths,source_reference_only=True,pending=['P13↔HE01 명판·실물 위치','철거 MV04 이후 현행 P&ID·실제 유로','현재 센서 취출·변환기·단위·계수·HMI 이벤트·PLC 호출'])
    for fg in [75,77,106,107,108]:drawing['sheets'].append(dict(id='oem-'+str(fg),kind='주변 OEM 전기',title='주변 FG'+str(fg)+' · PDF'+str(fg+1),source='sources/Electrical_Rev2.pdf',page=fg+1,fg=fg,image='assets/sensor-circuits/FG'+str(fg)+'.png',extent='원본 한 페이지 · 주변 참고',status=boundary,revision='FG107 Rev2 17.03.2025; FG75/77/106/108 개정란 공란'))
    for page in [56,57]:
        sheet=next(s for s in drawing['sheets'] if s['id']=='construction-'+str(page))
        sheet.update(extent='전체 원본 · 가림 미복원',status=boundary)
    drawing['warnings'].extend(['TC03·PSH01·PSH03는 주변 계측이며 HE01 본체 소유로 새 배정하지 않음','FG75 상단 PSH02 대 하단 PSH03 이름 불일치 유지','시공 HE01 위치 대 OEM AB01 기능·KX2S 대 4–20mA 구간 차이 가능','PDF56 6_7~6_10 가림 복원 금지; PDF57 MV04 과거 배선은 철거 제외 보존','팬 요청/표시·TC03 한 점으로 실제 유량·효율·현장 복구를 판정하지 않음'])
    notes=[boundary,'TC03 ON→C356 EN/IN0 ON; PIW276→CoeffDB4W22/ZeroW20→DB1W112/OFR3X21.4. PSH01 PIW284→Press_PC01 DB1W134/OFR3X22.0, PSH03 PIW320→DB1W24/OFR3X22.2; 별도 PC01 센서와 합치지 않습니다.','공통 FC63 Int→DInt/Zero 더함/Coeff 곱함/28000 나눔/최종Move, 원문 >−1382·≤32767 및 범위외−9999·미호출/0쓰기 경계 보존. 현재 계수/단위/절삭/오버플로 미확인.','HMI raw IW276/284/320 SAM=None→WordDB13W40/48/52. PSH03는 Move96→97→98 ENO 연쇄입니다. Editor DB26W20/W16 설정참조는 실제 화면 쓰기 이벤트 증명이 아닙니다.','TC03 LOW: ON·(BWF01 RUN OR BWF02 RUN)·Temp<MIN→SD342 T87 S5T#3S→Set347. 자기래치→MIN+5 Add352 ENO W491→Temp>app00→Reset360/STOP_HORN362. Reset 가지에는 BWF RUN/RESET_ALLARM이 없습니다. MIN<200→200 쓰기는 현재값 보장이 아닙니다.','TC03 MAX: ON·Temp>MAX→SD372 T88 S5T#3S→Set377. 자기래치→MAX−5 Sub382 ENO W512→Temp<app00→Reset390/STOP_HORN392; RESET_ALLARM 접점은 없습니다.','TC03 MAXMAX: Temp>MAX+50 OR >750 OR <−60→SD415 T89 S5T#3S→Set420. Wire544 Add396 EN/비교pre 병렬이며 AddENO 직렬로 바꾸지 않습니다. ON·RESET_ALLARM·자기래치→Reset425, 그 가지에 정상온도 비교가 없습니다.','LOW→RD01 적재금지, MAXMAX→GME 버너요청 Reset. MAX의 OFF 전단 및 ON 병렬 Lock Reset을 보존하며 외부 버너 안전 순서를 추정하지 않습니다.','MV01 CONT_S는 TC03 조절 소유이고 PSH01/MV02와 PSH03/MV03는 별도입니다. MV03 ≥5/<−5,4/10초·별도PSH02 PID 복수쓰기는 본체 고유 제어가 아닙니다. FN02 5/100 제한·×272/기동요청은 실유동 증명이 아닙니다.','역사 P&ID 두 유로: AB01→HE 하부→상부→CY, MV01 배기가스 우회; FN02/MV04→HE 좌상→좌하→AB 공기측. MV04는 사용자 제공 철거 제외이며 현재 배관을 재구성하지 않습니다.','도면 FG75/77/106/107/108과 시공3/6/56/57, HE01 구역 FLO1TB4/FLO2TB1 공유함·PSH03 상단/하단 이름·가림·TC KX/4–20mA를 유지합니다. 제작사 허용압력/성능·현행 센서 취출·실제 입출구 동조건 관찰이 필요합니다.']
    native=[1659,1858,1862,1865,1870,1931,1948,1658,1702,1704,1705,1706,1071,1688,7,11,15,8,1741,1745,1747,1980];extra=[]
    for n in read('sources/decoded-original/network-map.json'):
        if n['document_id']not in native:continue
        z=ET.parse(root/'sources/decoded-original'/n['xml_file']).getroot();ns={'n':z.tag.split('}')[0][1:]}
        extra.extend((n['document_id'],'part',p.get('UId'))for p in z.findall('n:Parts/n:Part',ns));extra.extend((n['document_id'],'wire',p.get('UId'))for p in z.findall('n:Wires/n:Wire',ns))
    control=dict(id='HE01',applicability='본체 전용 제어 미확보; 주변 참고',controller_evidence=None,native=native,native_refs=[],chain=notes,repair=['동조건 입출구·유로·팬/댐퍼 실제 응답을 구분 기록','센서 취출·원시/환산/HMI·단위와 계수·OFR을 대조'],pending=['실물 명판·철거 이후 현행 유로','현재 PLC/HMI·호출·복수 쓰기·단위/계수','제작사 성능/허용압력·승인 도면·복구 관찰'],source_reference_only=True)
    def act(uid,gate,name,text):return dict(network=1980,uid=str(uid),gate=gate,name=name,condition=dict(op='read',name=text),source_reference_only=True,evidence='reviewed static wire transcription; no execution or owned-body assignment')
    alarms=[dict(name=name,source_reference_only=True,actions=[act(s,'SCoil',name,text),act(t,'RCoil',name,text)])for name,s,t,text in [('Allarm.LOW_TC03_TEMP',347,360,notes[4]),('Allarm.MAX_TC03_TEMP',377,390,notes[5]),('Allarm.MAX_MAX_TC03_TEMP',420,425,notes[6])]]
    timers=[]
    for uid,name,wire,oref,text in [(342,'Tag_101 / T87',480,431,notes[4]),(372,'Tag_102 / T88',501,445,notes[5]),(415,'Tag_103 / T89',532,466,notes[6])]:
        t=act(uid,'SdCoil',name,text);t.update(preset={'op':'const','literal':'S5T#3S'},value_wire=str(wire),value_oref=str(oref));timers.append(t)
    alarm=dict(id='HE01',note='TC03 소유 주변 경보3개·타이머3개 정적 참고입니다. HE01 전용 경보·보호값으로 새 배정하지 않습니다.',alarms=alarms,timers=timers,native_networks=[],source_reference_only=True)
    extra_sources=['HE01-INVESTIGATION.md','registers/he01-independent-investigation.json','registers/body-manual.json','registers/sensor-measurement.json','sources/live_index.json','alarm-guides/HE01.html']+['assets/sensor-circuits/FG'+str(f)+'.png'for f in[75,77,106,107,108]]+['sources/decoded-original/'+str(i).zfill(4)+'-IdentXmlPart.xml'for i in[62,611,612,617,619,620,627,629,665,667,668,669,670,671,672,676,678,680,683,684,685,686]]
    return build_static_profile(root,data,source_rows,dict(catalog_id='HE01',priority_key='P13',type='passive_body_candidate',source_pairs=pairs,extra_locations=extra,extra_sources=extra_sources,internal_names=[],signal_reference=dict(id='HE01',signals=[],note='본체 고유 신호 미확보; 주변 참고 분리'),alarm_reference=alarm,control_reference=control,related_alarm_boundary='LOW/MAX 자동 히스테리시스·MAXMAX 요청 해제·OFR·RD01 적재금지·BR01 요청·실제 유동/전열/복구를 구분합니다.',presentation=dict(identity_title='열교환 본체 후보·두 유로/주변 소유',identity_pending='P13↔HE01 실물 명판·철거 이후 현재 배관 확인 전',io_empty_note='본체 전용 I/O·처리/HMI는 미확보입니다. TC03/PSH01/PSH03·댐퍼·팬은 주변 참고입니다.',oem_baseline='FG75/77/106/107/108; FG107만 Rev2 17.03.2025·나머지 개정란 공란·PSH03 이름 상충',construction_baseline='시공3/6/56/57;24.11.11 first draft design·구역/공유함·가림/철거 제외 유지',control_title='주변 환산/HMI·댐퍼·팬/공정 영향',control_links=[['보존 본체 분석','body-manual.html#body-HE01'],['독립 조사','HE01-INVESTIGATION.md'],['TC03 원본 경보','networks/network-1980.html']],timer_title='주변 TC03 시간3개 · 본체 전용 아님',related_title='OFR·RD01/BR01 영향·실측 경계',related_links=[['주변 계측','sensor-measurement.html'],['별도 MV01','alarm-guides/MV01.html'],['별도 BR01','alarm-guides/BR01.html']],field_title='실물 본체·현재 유로·동조건 계측·승인 자료',alarm_recovery='원시·환산·경보·요청·출력·실물 유동/전열·동조건 입출구 관찰을 분리합니다. 백업 숫자를 현장 보호값/효율/수리 완료로 대체하지 않습니다.',search_examples='PIW276, IW276, Press_PC01, PIW320, LOW_TC03, MAX_MAX_TC03, S5T#3S, RESET_ALLARM, FLO2TB1, MV04')))
