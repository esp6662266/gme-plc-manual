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
