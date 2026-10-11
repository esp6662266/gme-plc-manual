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
        locations.extend(dict(network=number,kind=kind,uid=uid,path=f'networks/network-{number}.html#{prefix}-{kind}-{uid}',xml=file) for kind,uid in sorted(rows))
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
