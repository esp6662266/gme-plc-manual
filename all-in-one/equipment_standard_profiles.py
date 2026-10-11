"""Equipment-specific display profiles over preserved static evidence, no simulation."""
from pathlib import Path
import json,hashlib
import xml.etree.ElementTree as ET

def build_static_profile(root,data,source_rows,config):
    catalog_id,key=config["catalog_id"],config["priority_key"]
    prefix="gme-"+catalog_id.lower()
    def read(file):return json.loads((root/file).read_text(encoding='utf-8'))
    spec=next(p for p in read('registers/control-spec.json')['specifications'] if p['id']==catalog_id)
    alarm=next(p for p in read('registers/alarm-recovery.json')['profiles'] if p['id']==catalog_id)
    regulation=next((p for p in read('registers/regulation-manual.json')['loops'] if p['id']==catalog_id),None)
    control_reference=config.get('control_reference',regulation)
    assert control_reference is not None,(catalog_id,'reviewed control reference required')
    completion=next(p for p in read('registers/requirements-audit.json')['priority_open_work'] if p['key']==key)
    repair=next(p for p in read('registers/repair-decision.json')['records'] if p['key']==key)
    form=next(p for p in data['repair_record_forms']['profiles'] if p['key']==key)
    drawing=next(p for p in data['drawing_workspace']['profiles'] if p['key']==key)
    signal_trace=next(p for p in read('registers/signal-trace.json')['devices'] if p['id']==catalog_id)
    networks={p['document_id']:p for p in read('sources/decoded-original/network-map.json')}
    allowed={}
    def add(network,kind,uid):allowed.setdefault(int(network),set()).add((kind,str(uid)))
    for rule in spec['direct_rules']:add(rule['네트워크 문서'],'part',rule['Part UID'])
    for entry in alarm['timers']+[a for group in alarm['alarms'] for a in group['actions']]:
        add(entry['network'],'part',entry['uid'])
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
    native_ids.update(int(n['문서 ID']) for n in spec['networks'])
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
    profile=dict(priority_key=key,catalog_id=catalog_id,type=config['type'],version=1,
        scope='preserved '+catalog_id+' analysis linked to seven areas; no new PLC execution or field claims',
        tools=dict(sources=True,restore=True,compare=True,report=True),sections=['overview','io','control','circuits','alarms','repair','completion'],
        specification=spec,signal_trace=signal_trace,alarm=alarm,regulation=regulation,control_reference=control_reference,completion=completion,repair=repair,
        presentation=config['presentation'],internal_names=config['internal_names'],
        source_pairs=pairs,source_locations=locations,source_hashes=hashes,
        source_bundle_sha256=hashlib.sha256(json.dumps(hashes,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        field_verified=False,tia_verified=False,repairs_completed=0,
        related_alarm_boundary=config['related_alarm_boundary'])
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
        repair=['FG141 MOD15 단자13/Q5.2→FG69 69KA1 DC코일;110Vac9.7→69KA1 1/9→X1 126(5x20/2A F)→EV01 A1/A2→127/0Vac9.9. B 단자14/Q5.3→69KA2 DC코일·접점1/9→128/EV02→129/0Vac. 출력/접점/밸브/공압·기계/위치단계를구분합니다.',
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
