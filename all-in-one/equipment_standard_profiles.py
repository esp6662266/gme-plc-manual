"""Equipment-specific display profiles over preserved static evidence, no simulation."""
from pathlib import Path
import json,hashlib
import xml.etree.ElementTree as ET

def build_fn04_profile(root,data,source_rows):
    def read(file):return json.loads((root/file).read_text(encoding='utf-8'))
    spec=next(p for p in read('registers/control-spec.json')['specifications'] if p['id']=='FN04')
    alarm=next(p for p in read('registers/alarm-recovery.json')['profiles'] if p['id']=='FN04')
    regulation=next(p for p in read('registers/regulation-manual.json')['loops'] if p['id']=='FN04')
    completion=next(p for p in read('registers/requirements-audit.json')['priority_open_work'] if p['key']=='P02')
    repair=next(p for p in read('registers/repair-decision.json')['records'] if p['key']=='P02')
    form=next(p for p in data['repair_record_forms']['profiles'] if p['key']=='P02')
    drawing=next(p for p in data['drawing_workspace']['profiles'] if p['key']=='P02')
    signal_trace=next(p for p in read('registers/signal-trace.json')['devices'] if p['id']=='FN04')
    networks={p['document_id']:p for p in read('sources/decoded-original/network-map.json')}
    allowed={}
    def add(network,kind,uid):allowed.setdefault(int(network),set()).add((kind,str(uid)))
    for rule in spec['direct_rules']:add(rule['네트워크 문서'],'part',rule['Part UID'])
    for entry in alarm['timers']+[a for group in alarm['alarms'] for a in group['actions']]:
        add(entry['network'],'part',entry['uid'])
        for part in entry.get('native_upstream',{}).get('parts',[]):add(entry['network'],'part',part)
        for ref in entry.get('native_upstream',{}).get('reference_pins',[]):add(entry['network'],'wire',ref['wire'])
    add(1689,'wire','875');add(1770,'wire','1491');add(1770,'wire','24')
    for signal in signal_trace['signals']:
        if signal['name'].startswith(('Inputs.','Flag.','Stop_')) or signal['name'] in ('Data.SET_PERC_FN04','Data.FN_04_ASPIRATOR'):
            for use in signal['usages']:add(use['network'],'wire',use['wire'])
    sources=['registers/control-spec.json','registers/alarm-recovery.json','registers/regulation-manual.json',
             'registers/electrical-trace.json','registers/construction-reference.json','registers/construction-review.json',
             'registers/repair-decision.json','registers/repair-record-forms.json','registers/requirements-audit.json',
             'registers/signal-trace.json','registers/hmi-transfer.json','registers/vendor-reference-review.json',
             'registers/plc-symbols.csv','sources/hmi_plc_tags.csv','sources/Electrical_Rev2.pdf',
             'sources/Electrical_Can_Decoating_20241118.pdf','sources/PID_1684n002I.pdf','sources/decoded-original/network-map.json']
    # Hash original XML and all declarations in the reviewed network scope.
    native_ids=set(allowed)|set(regulation['native'])
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
        path=root/f'networks/network-{number}.html';text=path.read_text(encoding='utf-8');parser=source_rows(text,rows,prefix='gme-fn04');parser.feed(text)
        assert parser.found==rows,(number,rows-parser.found)
        for pos,length,value in sorted(parser.edits,reverse=True):text=text[:pos]+value+text[pos+length:]
        style='<style id="gme-fn04-source-locations">tr[id^="gme-fn04-"]{scroll-margin-top:65px}tr[id^="gme-fn04-"]:target td{background:#e0f2e9!important;outline:1px solid #167769}</style>'
        if 'id="gme-fn04-source-locations"' not in text:text=text.replace('</head>',style+'</head>',1)
        if text!=path.read_text(encoding='utf-8'):path.write_text(text,encoding='utf-8')
        locations.extend(dict(network=number,kind=kind,uid=uid,path=f'networks/network-{number}.html#gme-fn04-{kind}-{uid}',xml=file) for kind,uid in sorted(rows))
    pairs=[
      dict(signal='기동 명령',network=1965,uid='1014',label='최종 출력 · Start FN04',boundary='ON·요청 → Q17.1과 공통 인버터·두 모터 회로를 비교합니다. 출력1만으로 두 모터 운전을 확정하지 않습니다.'),
      dict(signal='운전 응답',network=1809,uid='1114',label='처리 응답 · Inputs.FN04 Run',boundary='I28.2 원시 응답과 Inputs.FN04 Run의 전달·정상 극성·현재 CPU 대응은 확인 전입니다.'),
      dict(signal='인버터 이상',network=1809,uid='1118',label='처리 입력 · Inputs.FN04_All_inv',boundary='I28.3 원시 입력과 처리 신호를 구분합니다. 공동 인버터 RO·현재 극성은 확인 전입니다.'),
      dict(signal='속도 설정',network=1689,kind='wire',uid='875',label='속도 출력 · FN04_SP',boundary='5/100 제한·×272 출력과 QW336→AI1 전달을 비교합니다. 실제 환산·현재 인버터 파라미터·복수쓰기 최종값은 확인 전입니다.'),
      dict(signal='전류 전달',network=1770,kind='wire',uid='1491',label='전류 입력 · 별도 범위 오류',boundary='IW394→환산/범위 오류와 AO2 전달을 비교합니다. 공동 인버터 전류를 각 모터 개별 전류로 적용하지 않습니다.')]
    for pair in pairs:
        match=next((s for s in locations if s['network']==pair['network'] and s['kind']==pair.get('kind','part') and s['uid']==pair['uid']),None)
        pair['path']=match['path'] if match else f"networks/network-{pair['network']}.html"
    hashes={file:hashlib.sha256((root/file).read_bytes()).hexdigest() for file in sorted(set(sources))}
    profile=dict(priority_key='P02',catalog_id='FN04',type='motor_fan',version=1,
        scope='existing FN04 analysis linked to seven areas; no new PLC execution or field claims',
        tools=dict(sources=True,restore=True,compare=True,report=True),sections=['overview','io','control','circuits','alarms','repair','completion'],
        specification=spec,signal_trace=signal_trace,alarm=alarm,regulation=regulation,completion=completion,repair=repair,
        source_pairs=pairs,source_locations=locations,source_hashes=hashes,
        source_bundle_sha256=hashlib.sha256(json.dumps(hashes,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        field_verified=False,tia_verified=False,repairs_completed=0,
        related_alarm_boundary='직접 FAULT/INV2개와 공유17초 감시를 구분합니다. 1964의 Prealarms_FN04/90분 Local 정지와1770 전류 범위 오류는 별도 근거입니다. 설정0 요청 해제와5/100 제한을 현재 실행 오류로 단정하지 않습니다.')
    return profile
