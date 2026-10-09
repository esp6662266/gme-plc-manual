"""Temperature/pressure/oxygen source manual; documentation only, no execution."""
from pathlib import Path
from collections import Counter
import hashlib, html, json, csv, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
tag=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s or '').replace('"','').casefold()
e=lambda s:html.escape(str(s))
model=load('registers/program-model.json');nets={n['id']:n for n in model['networks']}
trace=load('registers/signal-trace.json')['usages']
source_map={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
declarations=load('sources/decoded-original/identifier-declarations.json')
def expression(v):
    op=v['op']
    if op=='read':return v['name']
    if op=='const':return str(v.get('literal',v.get('value')))
    if op=='unknown':return '[원본 추가 해석: '+v['reason']+']'
    if op=='not':return 'NOT ('+expression(v['arg'])+')'
    if op in ('and','or'):
        args=[a for a in v['args'] if not(op=='and' and a.get('op')=='const' and a.get('value') is True)]
        return '('+(' AND ' if op=='and' else ' OR ').join(expression(a) for a in args)+')'
    if op in ('eq','ne','gt','ge','lt','le'):
        return '('+expression(v['left'])+' '+{'eq':'=','ne':'<>','gt':'>','ge':'>=','lt':'<','le':'<='}[op]+' '+expression(v['right'])+')'
    return json.dumps(v,ensure_ascii=False)

source_paths={'registers/program-model.json','registers/signal-trace.json','registers/plc-symbols.csv',
 'registers/electrical-trace.json','registers/equipment-hmi.csv','sources/decoded-original/network-map.json',
 'sources/decoded-original/identifier-declarations.json','sources/Electrical_Rev2.pdf'}

def native(i):
    n=nets[i];root=ET.parse(ROOT/n['file']).getroot();source_paths.add(n['file'])
    parts=[dict(uid=x.get('UId'),gate=x.get('Gate'),attributes=dict(x.attrib),
        negated_pins=[c.get('PinName') for c in x if tag(c)=='Negated'],
        templates=[dict(attributes=dict(c.attrib),value=c.text) for c in x if tag(c)=='TemplateValue']) for x in root.iter() if tag(x)=='Part']
    refs={x.get('UId'):dict(ref_id=x.get('RefId'),name=n['refs'][x.get('UId')].get('name')) for x in root.iter() if tag(x)=='ORef'}
    for uid,r in refs.items():
        r['declarations']=[d for d in declarations if d['uid']==uid and d['rid']==r['ref_id'] and d['nid']==source_map[i]['inferred_original_nid'] and d['name']==r['name']]
        source_paths.update('sources/decoded-original/'+d['file'] for d in r['declarations'])
    calls=[]
    for c in [x for x in model['calls'] if x['network']==i]:
        ref=next(x for x in root.iter() if tag(x)=='CRef' and x.get('UId')==c['uid']);block=next(x for x in ref if tag(x)=='CodeBlock')
        decl=[d for d in declarations if d['uid']==block.get('UId') and d['rid']==block.get('RefId') and d['nid']==source_map[i]['inferred_original_nid'] and d['name']==c['callee']]
        assert decl,(i,c['callee']);source_paths.update('sources/decoded-original/'+d['file'] for d in decl)
        calls.append(dict(**c,cref_ref_id=ref.get('RefId'),block_ref_id=block.get('RefId'),native_declarations=decl))
    wires=[dict(uid=w.get('UId'),endpoints=[dict(kind=tag(x),uid=x.get('UId'),pin=x.get('PinName')) for x in w]) for w in root.iter() if tag(w)=='Wire']
    return dict(network=i,block=n['block'],index=n['index'],title=n['title'],file=n['file'],sha256=sha(n['file']),parts=parts,refs=refs,calls=calls,wires=wires)

def proof(p,uid):
    nodes={x['uid']:x for x in p['parts']};nodes.update({c['uid']:dict(uid=c['uid'],gate='CRef',negated_pins=[]) for c in p['calls']})
    seen=set();todo=[uid]
    while todo:
        current=todo.pop()
        if current in seen:continue
        seen.add(current)
        for w in p['wires']:
            if any(x['kind']=='PCon' and x['uid']==current and (x['pin'] in ['in','en','pre'] or x['pin'] and x['pin'].startswith('in') and x['pin'][2:].isdigit()) for x in w['endpoints']):
                todo.extend(x['uid'] for x in w['endpoints'] if x['kind']=='PCon' and x['pin'] in ['out','eno'])
    pins=[];contacts=[]
    for w in p['wires']:
        for x in w['endpoints']:
            if x['kind']=='PCon' and x['uid'] in seen:
                for c in w['endpoints']:
                    if c['kind']!='OCon':continue
                    row=dict(part=x['uid'],gate=nodes[x['uid']]['gate'],pin=x['pin'],wire=w['uid'],oref=c['uid'],name=p['refs'][c['uid']]['name'],ref_id=p['refs'][c['uid']]['ref_id'])
                    pins.append(row)
                    if row['gate'] in ['Contact','PContact','NContact'] and row['pin']=='operand':contacts.append(dict(**row,negated_pins=nodes[x['uid']]['negated_pins']))
    return dict(nodes=sorted(seen,key=int),reference_pins=pins,contacts=contacts)

def reads(v):
    if isinstance(v,dict):
        if v.get('op')=='read':yield v['name']
        for value in v.values():yield from reads(value)
    elif isinstance(v,list):
        for value in v:yield from reads(value)

# Paths are transcriptions of the rendered OEM pages, not live hardware settings.
specs=[
 ('TC01',1739,77,106,'0/1300 °C','+24Vdc → X1:186(50mA F) → TC01:+5; TC01:-6 → X1:187 → +PEW272; X1:188 / 77SCH1','CPU515 / MOD3 / PEW272: I0+2, U0-/I0-4'),
 ('TC02',1740,77,106,'0/1300 °C','+24Vdc → X1:189(50mA F) → TC02:+5; TC02:-6 → X1:190 → +PEW274; X1:191 / 77SCH2','CPU515 / MOD3 / PEW274: I1+6, U1-/I1-8'),
 ('TC03',1741,77,106,'0/750 °C','+24Vdc → X1:192(50mA F) → TC03:+5; TC03:-6 → X1:193 → +PEW276; X1:194 / 77SCH3','CPU515 / MOD3 / PEW276: I2+10, U2-/I2-12'),
 ('TC04',1731,79,104,'FG79 -30~250°C; FG104 -30~250°C','PT100 → X1:201/202/203 → 79KA1(PHOENIX CONTACT2864273) 7+/8-/1; 변환기 5+/6- → +PEW256/-PEW256; X1:204 / 79SCH1; 출력실드79SCH2','CPU515 / MOD2 / PEW256: I0+2, U0-/I0-4'),
 ('TC05',1732,79,104,'FG79 -30~250°C; FG104 -30~350°C / 범위 확인 필요','PT100 → X1:205/206/207 → 79KA2(PHOENIX CONTACT2864273) 7+/8-/1; 변환기 5+/6- → +PEW260/-PEW260; X1:208 / 79SCH3; 출력실드79SCH4','CPU515 / MOD2 / PEW260: I2+10, U2-/I2-12'),
 ('TC06',1742,78,106,'0/1300 °C','+24Vdc → X1:195(50mA F) → TC06:+5; TC06:-6 → X1:196 → +PEW278; X1:197 / 78SCH1','CPU515 / MOD3 / PEW278: I3+14, U3-/I3-16'),
 ('TC07',1743,78,107,'0/750 °C / FG78 SPARE 경계','+24Vdc → X1:198(50mA F) → TC07:+5; TC07:-6 → X1:199 → +PEW280; X1:200 / 78SCH2; FG78·107 SPARE 표기','CPU515 / MOD3 / PEW280: I4+22, U4-/I4-24'),
 ('TC09',1733,171,171,'별도 범위 미표기 / 현재 설정 확인','TC09 도면4선 → X3:100/101/102/103 → +PEW386/-PEW386/+PEW388/-PEW388; X3:104 / 171SCH1. PLC 호출은TC09(%IW386); PEW388을 별도 실제 센서로 배정하지 않음','CPU515 / MOD2 / PEW386: I0+2, U0-/I0-4; PEW388: I1+6, U1-/I1-8'),
 ('TC10',1734,171,171,'TC-10 SPARE / 센서·범위 확인 전','FG171 PEW390/392는SPARE 표기이며 현장 센서·배선 연결 미확정. 원본 호출의TC-10(%IW390)을 보존','CPU515 / MOD2 / PEW390: I2+10, U2-/I2-12; PEW392: I3+14, U3-/I3-16'),
 ('PSH01',1745,75,107,'0/10 mbar','+24Vdc → X1:172(50mA F) → PSH01:+; PSH01:- → X1:173 → +PEW284; X1:174 / 75SCH1','CPU515 / MOD3 / PEW284: I6+30, U6-/I6-32'),
 ('PSH02',1746,75,107,'0/10 mbar','+24Vdc → X1:175(50mA F) → PSH02:+; PSH02:- → X1:176 → +PEW286; X1:177 / 75SCH2','CPU515 / MOD3 / PEW286: I7+34, U7-/I7-36'),
 ('PSH03',1747,75,108,'0/10 mbar / 원본 제목PRESSURE CONTROL PSH-02 보존','+24Vdc → X1:178(50mA F) → PSH03:+; PSH03:- → X1:179 → +PEW320; X1:180 / 75SCH3','CPU515 / MOD4 / PEW320: I0+2, U0-/I0-4'),
 ('PC01',1775,76,108,'-/+200 mbar','+24Vdc → X1:181(50mA F) → PC01:+; PC01:- → X1:182 → +PEW322; X1:183 / 76SCH1. 같은 도면의 PSL05는 별도 접점','CPU515 / MOD4 / PEW322: I1+6, U1-/I1-8'),
 ('DP01',1773,169,172,'0/50 mbar','110Vac → X3:90(2A F)/91 → DP01 전원; DP01 출력+/- → X3:92/93 → +PEW398/-PEW398; X3:94 / 169SCH1','CPU515 / MOD2 / PEW398: I6+30, U6-/I6-32'),
 ('DP02',1774,169,172,'0/50 mbar','110Vac → X3:95(2A F)/96 → DP02 전원; DP02 출력+/- → X3:97/98 → +PEW400/-PEW400; X3:99 / 169SCH2','CPU515 / MOD2 / PEW400: I7+34, U7-/I7-36'),
 ('RO01',1748,80,110,'4–20mA / 산소 표시 환산·단위 확인 전','RO01 소자+S/-S/-T/+T → 80RO01 H705:1+/2-/3-/4+; 110Vac X1:209(2A F)→15, 0Vac X1:210→16, GND17; 출력7+/8- → X1:211/212 → +PEW352/-PEW352; X1:213 / 80SCH1','CPU515 / MOD5 / PEW352: I0+2, U0-/I0-4'),
 ('RO02',1749,80,110,'4–20mA / 산소 표시 환산·단위 확인 전','RO02 소자+S/-S/-T/+T → 80RO02 H705:1+/2-/3-/4+; 110Vac X1:214(2A F)→15, 0Vac X1:215→16, GND17; 출력7+/8- → X1:216/217 → +PEW354/-PEW354; X1:218 / 80SCH3','CPU515 / MOD5 / PEW354: I1+6, U1-/I1-8'),
 ('RO03',1750,81,110,'4–20mA / 산소 표시 환산·단위 확인 전','RO03 소자+S/-S/-T/+T → 81RO03 H705:1+/2-/3-/4+; 110Vac X1:219(2A F)→15, 0Vac X1:220→16, GND17; 출력7+/8- → X1:221/222 → +PEW356/-PEW356; X1:223 / 81SCH1','CPU515 / MOD5 / PEW356: I2+10, U2-/I2-12'),
 ('RO04',1751,81,110,'4–20mA / 산소 표시 환산·단위 확인 전','RO04 소자+S/-S/-T/+T → 81RO04 H705:1+/2-/3-/4+; 110Vac X1:224(2A F)→15, 0Vac X1:225→16, GND17; 출력7+/8- → X1:226/227 → +PEW358/-PEW358; X1:228 / 81SCH3','CPU515 / MOD5 / PEW358: I3+14, U3-/I3-16'),
]
symbols=list(csv.DictReader((ROOT/'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
hmi=list(csv.DictReader((ROOT/'registers/equipment-hmi.csv').open(encoding='utf-8-sig')))
pages={p['page']:p for p in load('sources/electrical-page-text.json')}
source_paths.add('sources/electrical-page-text.json')
channels=[];names=[]
for id,i,fg,module_fg,range_,path,module in specs:
    call=next(c for c in model['calls'] if c['network']==i)
    assert call['callee']=='Signal linearization'
    raw=call['bindings']['Analog_input'][0]
    symbol=next(s for s in symbols if canon(s['원본 심볼'])==canon(raw))
    assert symbol['백업 주소'].casefold().startswith('%iw')
    focus=list(dict.fromkeys(v for k,vs in call['bindings'].items() if k!='IN0' for v in vs))
    names+=focus
    transfers=[dict(network=1071,**a) for a in nets[1071]['actions'] if a.get('value',{}).get('op')=='read' and canon(a['value']['name'])==canon(raw)]
    channels.append(dict(id=id,network=i,call=call,raw_symbol=symbol,focus=focus,raw_transfers=transfers,
        circuit=dict(fg=fg,page=fg+1,module_fg=module_fg,module_page=module_fg+1,range_label=range_,path=path,module_pins=module,
                     diagram_visually_reviewed=True,current_hardware_verified=False),
        hmi_reference_rows=[x for x in hmi if x['설비 ID']==id]))
signals=[]
for name in dict.fromkeys(names):
    uses=[u for u in trace if u['scope']=='Global' and canon(u['name'])==canon(name)]
    other=[u for u in trace if u['scope']!='Global' and canon(u['name'])==canon(name)]
    source_paths.update(u['file'] for u in uses+other);source_paths.update(v['file'] for u in uses+other for v in u['declarations'])
    signals.append(dict(name=name,scope='Global',usages=uses,other_scope_usages=other))
selected=sorted({1658,1659,1071}|{u['network'] for s in signals for u in s['usages']+s['other_scope_usages']})
proofs=[native(i) for i in selected];pn={p['network']:p for p in proofs}
for c in channels:
    c['native_upstream']=proof(pn[c['network']],c['call']['uid'])
    for a in c['raw_transfers']:a['native_upstream']=proof(pn[1071],a['uid'])
    c['post_actions']=[dict(network=c['network'],**a,native_upstream=proof(pn[c['network']],a['uid'])) for a in nets[c['network']]['actions']]
    out=next(s for s in signals if s['name']==c['call']['bindings']['OutValue'][0])
    c['value_usages']=out['usages'];c['ofr_usages']=next(s for s in signals if s['name']==c['call']['bindings']['Out_of_range'][0])['usages']
    c['value_writes']=[u for u in out['usages'] if u['role']=='write'];c['value_reads']=[u for u in out['usages'] if u['role']=='read']
    comparison_uses=list({(u['network'],u['part']):u for u in c['value_reads'] if u['gate'] in ['Gt','Ge','Lt','Le','Eq','Ne','Sub','Add','Mul','Div']}.values())
    c['comparison_uses']=[dict(usage=u,native_upstream=proof(pn[u['network']],u['part'])) for u in comparison_uses]
fgs=sorted({f for c in channels for f in [c['circuit']['fg'],c['circuit']['module_fg']]})
for fg in fgs:source_paths.add('assets/sensor-circuits/FG'+str(fg)+'.png')
observations=[
 dict(id='SM-07',title='호출 앞 OFF와 내부 IN0=ON의 차이',text='TC05·TC07·TC10·RO01~RO04의 호출 앞 en 접점은 OFF이며 IN0 값 핀은 ON입니다. 두 조건과 현재 호출·OFF 값을 각각 확인합니다. 호출되지 않았을 때와 호출 후 IN0가 해제됐을 때의 출력/OFR 유지·0 쓰기를 구분하며 접점을 임의로 바꾸지 않습니다.',channels=['TC05','TC07','TC10','RO01','RO02','RO03','RO04']),
 dict(id='SM-01',title='PT100 변환기와 TC05 범위 차이',text='TC04/05는 FG79 PT100→79KA1/2→아날로그 입력 경로입니다. TC05의FG79 -30~250°C와FG104 -30~350°C, 심볼 설명의TC04 이름을 각 출처대로 보존합니다. 현재 명판·변환기범위·모듈설정·계수/영점을 대조합니다.',channels=['TC04','TC05']),
 dict(id='SM-02',title='PSH01과 PC01의 다른 값',text='PSH01 %IW284→Data.Press_PC01과 PC01 %IW322→Data.PC_01은 다른 입력/출력입니다. Data.Press_PC01은 복원된정확한 Global에서 호출 출력만 확인했고 Data.PC_01은1901/1987에서 읽습니다. 현재 PID·HMI 매핑은 별도 확인합니다.',channels=['PSH01','PC01']),
 dict(id='SM-03',title='RO03의 후속 Add',text='1750 Part566은 Int Add이며 원본 피연산자 Data.Oxigen_RO02와 상수11·출력Data.RO03을 보존합니다. RO03 원시입력의 호출환산값과 RO02+11의 후속쓰기는 다른 값의 출처이며 현재 호출·쓰기 순서를 확인합니다. 이 문서는 계산 실행 결과가 아닙니다.',channels=['RO03']),
 dict(id='SM-04',title='백업 기존 simulation 쓰기',text='TC01/02의 변환값에는 원본1092 simulation 블록의 추가 쓰기가 있습니다. 현재 호출·모드·쓰기 순서는 확인 전이며 이 참조는 원본 구조 분석입니다. 새 시뮬레이터 작성·수정·행동 시험은 진행하지 않습니다.',channels=['TC01','TC02']),
 dict(id='SM-05',title='SPARE와 보조 채널을 실물로 확정하지 않음',text='TC07는FG78/107 SPARE 표시, TC10는FG171 PEW390/392 SPARE입니다. TC09는386/388 회로와원본IW386 호출을 따로봅니다. 예약IW258/262와나머지채널을새실물센서로배정하지 않습니다.',channels=['TC07','TC09','TC10']),
 dict(id='SM-06',title='HMI 설정 주소와 물리 단위',text='기존 HMI 행의 주소를 보존하되 같은 이름만으로 현재 DB의 멤버 오프셋·전달·표시 단위·스케일을 확정하지 않습니다. TC09/10와 DP01/02의기존 설비 분류 행은 없으므로 별칭으로 찾거나 자동 배정하지 않습니다. 산소 원본 비교0/5/20/195/200은현재 %단위로 환산하지 않습니다.',channels=[c['id'] for c in channels]),
]
data=dict(date='2026-10-08',channels=channels,signals=signals,selected_networks=selected,native_networks=proofs,
 reviewed_fgs=fgs,observations=observations,sources={f:sha(f) for f in sorted(source_paths)},
 scope='Visually reviewed OEM channel paths and native input/conversion/value references; no execution or setting approval',
 field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun')
(ROOT/'registers/sensor-measurement.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def link(label,path):return '<a href="'+e(path)+'">'+e(label)+'</a>'
def nl(i,uid=None):return link('원본 '+str(i)+(' / Part '+str(uid) if uid else ''),'networks/network-'+str(i)+'.html')
def table(headers,rows):return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def pins(p,uid):return table(['Gate/핀·값','원본 식별'],[[e(x['gate']+'/'+str(x['pin'])+' / '+str(x['name'])),e('Part '+x['part']+' / Wire '+x['wire']+' / ORef '+x['oref']+' / RID '+str(x['ref_id']))] for x in proof(p,uid)['reference_pins']])
def usages(rows):return table(['방향·블록','핀·정확한 근거','현재 확인'],[[e(u['role']+' / '+u['block']),nl(u['network'],u['part'])+'<br>'+e(u['gate']+'/'+u['pin']+' / Wire '+u['wire']+' / ORef '+u['oref']),e('백업 simulation 참고 / 현재 호출 확인 전' if u['legacy_simulation_block'] else '현재 실행·값·설정 확인 전')] for u in rows])
body='<h1>온도·압력·산소 계측 수리 매뉴얼</h1><div class="notice">19개 채널 · 도면15개 FG 시각 대조 · 원본 정적 분석입니다. 현재 모듈·계수·단위·CPU/TIA·배선·복구는 확인 전입니다. PLC 변경0건, 시뮬레이터 작성·수정·행동 시험 중지.</div>'
body+='<nav class="inline-actions">'+link('가스·공기 환산','measurement-trace.html')+link('공정 정지 알람','process-stop-alarms.html')+link('BR01 수리 기록','index.html#view=repair-record&equipment=P11&scope=priority')+link('근거 검토·확인','index.html#view=review&equipment=P11&scope=priority')+'</nav>'
body+='<p>설비별로 물리 센서→전원/변환기→단자·아날로그 입력→원본 심볼→환산 호출→값의 다른 쓰기/읽기→HMI 설정을 비교합니다. 도면 범위와 원본 보호 비교값은 현재 승인값으로 사용하지 않습니다.</p>'
body+='<h2 id="index">1. 채널 선택</h2>'+table(['채널','백업 입력·환산값','도면·현재 확인'],[[link(c['id'],'#sensor-'+c['id']),e(c['raw_symbol']['원본 심볼']+' / '+c['raw_symbol']['백업 주소'])+'<br>'+e(c['call']['bindings']['OutValue'][0]),e(c['circuit']['range_label'])+'<br>'+e('FG'+str(c['circuit']['fg'])+' / FG'+str(c['circuit']['module_fg'])+' · 현장 확인 전')] for c in channels])
body+='<h2 id="repair">2. 값 이상·고정·불일치의 확인 순서</h2><ol><li>실물ID·위치·센서/변환기 명판·현재도면·PLC/HMI 버전·운전모드·관찰시각을 기록합니다.</li><li>현재 작업허가에 따라 전원·신호·실드·단자·모듈 진단과 실제 물리 상태를 대조합니다. PT100 소자/변환기 출력, RO 소자/전원/전류 출력은 각각 다른 확인 구간입니다.</li><li>원시 IW, IN0/en, Coeff/Zero, 환산값, OFR, 후속쓰기와 HMI표시를 같은 시각 기준으로 비교합니다. 원본 Inputs 복사와 환산값을 합치지 않습니다.</li><li>범위이상 -9999/OFR·허가해제0과 값의 복수쓰기를 대조합니다. 정상처럼 보이는 표시값만으로 센서 정상·복구를 판정하지 않습니다.</li><li>정확한 읽기위치에서 비교 피연산자·타이머·알람·리셋·운전응답을 확인합니다. 현장조치·원인해소·래치해제·재기동을 각각 기록합니다.</li></ol><p>'+link('공통 정수 환산: Int→DInt·Div28000·범위이상·허가해제','measurement-trace.html#linear')+' · '+link('공정 알람과 버너 정지 원인','process-stop-alarms.html')+'</p>'
for c in channels:
    b=c['call']['bindings'];cir=c['circuit'];p=pn[c['network']]
    body+='<h2 id="sensor-'+c['id']+'">'+e(c['id'])+' · 입력부터 사용값까지</h2>'
    body+=table(['구간','원본·관찰 대상'],[[e('백업 심볼'),e(json.dumps(c['raw_symbol'],ensure_ascii=False))],[e('센서/전원/단자 경로'),e(cir['path'])],[e('모듈 도면 표기'),e(cir['module_pins'])+'<br>'+e(cir['range_label'])],[e('환산 호출'),nl(c['network'],c['call']['uid'])+'<br>'+e('CRefRID '+p['calls'][0]['cref_ref_id']+' / CodeBlock '+c['call']['block_uid']+' RID '+p['calls'][0]['block_ref_id'])+'<br>'+e('호출 앞 en 조건: '+expression(c['call']['enable']))+'<br>'+e('IN0 값 핀: '+', '.join(b['IN0']))],[e('각 호출의 값 핀'),'<br>'.join(e(k+' ← '+', '.join(v)) for k,v in b.items())]])
    body+='<details><summary>호출 앞 접점·원본 핀배선</summary>'+pins(p,c['call']['uid'])+'</details>'
    out_name=b['OutValue'][0];ofr_name=b['Out_of_range'][0]
    extra_writes=[u for u in c['value_writes'] if u['network']!=c['network'] or u['gate']!='CRef']
    body+='<h3>증상별 관찰·배제·다음 확인</h3>'+table(['증상','확인할 구간','결과에 따른 다음 확인·근거'],[
        [e('값이0·고정이거나 물리 상태와 다름'),e(c['raw_symbol']['백업 주소']+' 원시값과 '+out_name+'을 같은 시각에 기록. '+cir['path']),e('원시값도 고정이면 센서·전원·변환기·단자·모듈진단을 구간별로 대조합니다. 원시값이 변하면 IN0/en·각Coeff/Zero·환산·쓰기 위치를 대조합니다. 실제 허가와 모듈 설정은 확인 전입니다.')+'<br>'+nl(c['network'],c['call']['uid'])],
        [e('변환값이 범위를 벗어나거나 갑자기 변함'),e(ofr_name+'·원시값·환산 직후 값·후속값을 분리합니다. 도면 참고 범위: '+cir['range_label']),e('OFR·범위 이상 -9999와 허가 해제0의 근거를 확인합니다. 계수·영점·현재 단위·정수 자료형·ENO·호출 순서를 대조합니다. 값을 임의로 보정하지 않습니다.')+'<br>'+link('원본 환산·범위 이상','measurement-trace.html#linear')],
        [e('HMI 표시와 PLC값이 맞지 않음'),e('참고 OutValue '+out_name+'와 기존 HMI 설정 주소를 비교합니다. 서로 다른 값의 출처·시각·자료형·단위를 기록합니다.'),e('다른 원본 쓰기가 '+str(len(extra_writes))+'곳 있습니다. 아래 정확한 쓰기 목록과 현재 호출을 대조합니다. HMI 설정 행이 없어도 임의 주소를 배정하지 않습니다.')],
        [e('알람이 반복되거나 리셋 뒤 응답이 다름'),e('아래 읽기 위치에서 실제 사용 변수·비교값·기억·운전 허가와 최초 알람을 확인합니다. '+out_name+'만으로 원인을 확정하지 않습니다.'),e('센서 원인 해소·알람 래치·Reset 접점·재기동 허가·최종 출력·물리 응답을 각각 기록합니다. OFR 읽기가 없음을 미사용으로 해석하지 않습니다.')+'<br>'+link('관련 공정 정지·복구 근거','process-stop-alarms.html')]
    ])
    body+='<h3>원시 입력의 Inputs 복사</h3>'
    if c['raw_transfers']:
        body+=table(['복사·정적 조건','값·근거'],[[e(a['name'])+'<br>'+e(expression(a['condition'])),e(expression(a['value']))+'<br>'+nl(1071,a['uid'])] for a in c['raw_transfers']])
    else:body+='<p>원본1071에서 이 심볼의 Inputs 복사는 확인하지 못했습니다. 다른 블록/현재 전달은 별도 확인합니다.</p>'
    body+='<h3>환산값의 전체 정확한 Global 쓰기·읽기</h3>'+usages(c['value_usages'])
    if c['comparison_uses']:
        body+='<details><summary>읽는 비교·연산의 값 출처·자료형·원본 핀</summary>'+table(['읽기 위치·원본 형식','접점·비교·값 연결'],[[nl(x['usage']['network'],x['usage']['part'])+'<br>'+e(json.dumps(next(p for p in pn[x['usage']['network']]['parts'] if p['uid']==x['usage']['part'])['templates'],ensure_ascii=False)),pins(pn[x['usage']['network']],x['usage']['part'])] for x in c['comparison_uses']])+'</details>'
    body+='<h3>범위 이상 OFR의 정확한 Global 참조</h3>'+usages(c['ofr_usages'])+'<p>색인에 읽기가 없더라도 HMI/외부 경보·미복원 자료·현재 프로그램의 사용 여부를 확정하지 않습니다.</p>'
    if c['post_actions']:
        body+='<h3>호출과 같은 네트워크의 후속 값 명령</h3>'+table(['명령·정적 조건','값 핀'],[[nl(c['network'],a['uid'])+'<br>'+e(a['gate']+' / '+a['name'])+'<br>'+e(expression(a['condition'])),pins(p,a['uid'])] for a in c['post_actions']])
    body+='<h3>기존 HMI 설정 참고</h3>'+(table(['태그','설정 주소','Access Name'],[[e(x[k]) for k in ['HMI 태그','설정 주소','Access Name']] for x in c['hmi_reference_rows']]) if c['hmi_reference_rows'] else '<p>기존 설비별 HMI 분류에서 이 ID의 행을 확인하지 못했습니다. HMI가 없다는 뜻은 아니며 다른 이름·현재 주소는 추가 확인합니다.</p>')
    body+='<p>같은 이름의 HMI 설정과 OutValue 사이의 현재 DB멤버·주소·표시환산 연결은 확인 전입니다.</p>'
    for fg in dict.fromkeys([cir['fg'],cir['module_fg']]):
        body+='<details><summary>원본 도면 FG'+str(fg)+' · PDF'+str(fg+1)+'</summary>'+link('원본 PDF 열기','sources/Electrical_Rev2.pdf#page='+str(fg+1))+'<img class="source-image" loading="lazy" alt="센서 원본 FG'+str(fg)+'" src="assets/sensor-circuits/FG'+str(fg)+'.png"></details>'
body+='<h2 id="checks">3. 차이·미확인 사항</h2>'+table(['항목','관찰·다음 확인','채널'],[[e(o['id']+' / '+o['title']),e(o['text']),', '.join(link(c,'#sensor-'+c) for c in o['channels'])] for o in observations])
body+='<p>기존 자료 불일치18건·현장 확인1,060건·설계 시험577건은 미확정 상태를 유지합니다. 이 작업지는 근거 대조이며 수리완료·보호설정 승인·현재 CPU 실행 검증이 아닙니다.</p>'
body+='<h2 id="native">4. 원본 구조·범위 확인</h2><p>'+str(len(proofs))+'개 네트워크의 Part·Wire·ORef·CRef/CodeBlock 선언을 '+link('정적 근거 JSON','registers/sensor-measurement.json')+'에 보존합니다. Local/다른범위는 정확한 Global 참조와 합치지 않습니다. 모든 계수·영점값의 전체 참조도 JSON에 포함합니다.</p>'+table(['블록·제목','원본 XML'],[[nl(p['network'])+'<br>'+e(p['block']+' / '+p['title']),link('원본 XML',p['file'])] for p in proofs])
page='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>온도·압력·산소 계측 수리 매뉴얼</title><link rel="stylesheet" href="assets/all-in-one.css"><style>main{max-width:1320px;margin:auto;padding:24px}td{vertical-align:top;overflow-wrap:anywhere}code{white-space:normal;overflow-wrap:anywhere}details{margin:16px 0}summary{cursor:pointer}</style></head><body><main>'+body+'</main></body></html>'
(ROOT/'sensor-measurement.html').write_text(page)
print(json.dumps(dict(channels=len(channels),native_networks=len(proofs),source_files=len(source_paths),reviewed_fgs=len(fgs),simulator_behavior_tests='not_rerun'),ensure_ascii=False))
