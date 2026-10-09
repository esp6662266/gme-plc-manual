"""Static controller evidence and repair manual. No evaluator or PLC mutation."""
from pathlib import Path
import csv,hashlib,html,json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
e=lambda s:html.escape(str(s))
tag=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s or '').replace('"','').casefold()
m=load('registers/program-model.json');nets={n['id']:n for n in m['networks']}
mp={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
decls=load('sources/decoded-original/identifier-declarations.json')
trace=load('registers/signal-trace.json')['usages']
live={(r['segment'],r['i']):r for r in load('sources/live_index.json') if not r['deleted']}
blocks=load('sources/block_summary.json')
paths={'registers/program-model.json','registers/signal-trace.json','sources/live_index.json','sources/block_summary.json','sources/decoded-original/network-map.json','sources/decoded-original/identifier-declarations.json','registers/plc-symbols.csv','registers/equipment-hmi.csv'}
def tree(x):return dict(tag=tag(x),attributes=dict(x.attrib),text=x.text.strip() if x.text else None,children=[tree(c) for c in x])
def declarations(i,x):
    return [d for d in decls if d['nid']==mp[i]['inferred_original_nid'] and d['uid']==x.get('UId') and d['rid']==x.get('RefId')]
def native(i):
    n=nets[i];r=ET.parse(ROOT/n['file']).getroot();paths.add(n['file'])
    refs={x.get('UId'):dict(ref_id=x.get('RefId'),name=n['refs'][x.get('UId')]['name'],declarations=declarations(i,x)) for x in r.iter() if tag(x)=='ORef'}
    wires=[dict(uid=w.get('UId'),ends=[dict(kind=tag(x),uid=x.get('UId'),pin=x.get('PinName')) for x in w]) for w in r.iter() if tag(w)=='Wire']
    nodes=[]
    for x in next(x for x in r if tag(x)=='Parts'):
        if tag(x) not in ['Part','LRef','CRef']:continue
        pins=[]
        for w in wires:
            for p in w['ends']:
                if p['kind']=='PCon' and p['uid']==x.get('UId'):
                    pins.append(dict(pin=p['pin'],wire=w['uid'],references=[dict(oref=a['uid'],**refs[a['uid']]) for a in w['ends'] if a['kind']=='OCon'],peers=[a for a in w['ends'] if a!=p and a['kind']!='OCon']))
        node=dict(uid=x.get('UId'),kind=tag(x),gate=x.get('Gate'),tree=tree(x),declarations=declarations(i,x),children_declarations=[dict(kind=tag(y),uid=y.get('UId'),rid=y.get('RefId'),declarations=declarations(i,y)) for y in x if tag(y) in ['Instance','CodeBlock']],pins=pins)
        nodes.append(node)
    for ref in refs.values():paths.update('sources/decoded-original/'+d['file'] for d in ref['declarations'])
    for node in nodes:
        paths.update('sources/decoded-original/'+d['file'] for d in node['declarations'])
        paths.update('sources/decoded-original/'+d['file'] for c in node['children_declarations'] for d in c['declarations'])
    return dict(id=i,block=n['block'],index=n['index'],title=n['title'],file=n['file'],sha256=sha(n['file']),tree=tree(r),refs=refs,wires=wires,nodes=nodes)
selected=[5,7,8,11,12,15,16,1686,1687,1688,1689,1702,1704,1705,1706,1708,1709,1710,1711,1712,1713,1714,1721,1722,1724,1830,1832,1834,1835,1870,1871,1900,1901]
proofs=[native(i) for i in selected];pn={p['id']:p for p in proofs}
text_keys=[('_7ex',4),('_7ex',6),('_7ex',9),('_7ex',10),('_7ex',13),('_7ex',14),('_7ev',1719),('_7ev',1720),('_7ev',1831),('_7ev',1833)]
texts=[]
for segment,i in text_keys:
    r=live[segment,i];b=next(b for b in blocks if any(n['segment']==segment and n['doc']==i for n in b['networks']));n=next(n for n in b['networks'] if n['segment']==segment and n['doc']==i)
    language=next(k for k in ['STL Code','SCL Code'] if k in r['values']);assert r['values'][language]==n[language]
    texts.append(dict(segment=segment,id=i,block=b['name'],language=language,title=r['values'].get('Network title',''),text=r['values'][language],text_sha256=hashlib.sha256(r['values'][language].encode()).hexdigest(),source='sources/live_index.json',evidence='backup_search_index_text_not_compiled_or_native_instruction_listing'))
# Curated annotations distinguish native LAD bindings from flattened search text.
loops=[
 dict(id='FN04',title='FN04 · PC01 비교에 따른 흡인팬 속도',priority='P02',equipment=['FN04','PC01'],native=[1900,1901,1689],texts=[],controller=None,
 chain=['원본1901 Sub: Data.PC_01 − Coeff.SET_PC01 → App02 (Int). 제목 DP-01과 실제 PC01 입력을 구분합니다.','Flag.FN_04_AUTO와 Tag_133 접점 뒤: App02 ≥ 5 및 Data.FN_04_ASPIRATOR < 250일 때 Add(1, Data.SET_PERC_FN04). 반대 분기는 App02 ≤ -1 및 Data.SET_PERC_FN04 > 20일 때 Add(-1, 같은 설정).','Tag_133에는 S5T#4S SD와 반전 접점이 연결됩니다. 실제 반복 주기·스캔 우선순위는 현재 CPU 확인 전입니다.','1900 Start FN04/PLS 50 4 분기는 설정에20을 씁니다.1689는5·100 제한과×272 → FN04_SP(%QW336)를 연결합니다. 비교 분기의20과 출력 제한5를 혼동하지 않습니다.'],
 repair=['측정값·설정값·App02·Auto·Tag_133을 같은 시각에 비교합니다. PC01 원시IW322와 Data.PC_01 환산의 원본 경로를 계측 작업지에서 확인합니다.','증가 요청이 없으면 압력 오차 조건과 별도로 Data.FN_04_ASPIRATOR의250 비교를 확인합니다. 이 값의 단위·정상 전류·정격은 확인 전입니다.','설정은 바뀌는데 회전이 변하지 않으면 FN04_SP·아날로그 출력 단자·인버터 수신/운전·실제 속도와 응답을 비교합니다.','20 쓰기, ±1 변경,5/100 제한이 함께 존재하므로 마지막 값을 한 분기만으로 단정하지 않습니다.'],
 pending=['DP-01 제목과PC01 실제 피연산자 관계','250의단위·현장 부하 한계','Tag_133 실제시간·현재호출·복수쓰기 순서']),
 dict(id='MV01',title='MV01 · TC03 CONT_S와 열림·닫힘',priority='P19',equipment=['MV01','TC03'],native=[8,11,1702],texts=[10],controller=(11,'366'),
 chain=['색인STL10: Data.TC03_SETPOINT + 0 → Real_SP_TC03xMV01, Data.Temp_TC03 → Real_TC03xMV01의 ITD/DTR 전달이 표시됩니다. // l Data.Temp_T6 문구는 주석과 줄바꿈 경계 확인 전입니다.','원본11 CONT_S/PIDMV01: SP_INT와 PV_IN은 위 블록 Local입니다. GAIN3.0·TI T#3M·DEADB_W1.0·CYCLE T#100MS·PULSE_TM T#500MS·BREAK_TM T#1S·MTR_TM T#31S를 보존합니다.','COM_RST에는 반전 Flag.MV01_Auto가 연결됩니다. LMNR_HS/LS는 리미트 접점 경로와 OFF→Pot_MV01 비교 경로를 각각 보존합니다.','QLMNUP/DN → UP MV01 PID/DOWN MV01 PID →1702 Start Open MV-01/Start Close MV-01. 백업Q2.4/Q2.5와 리미트·고장·수동·엔코더 리셋 경계를 기존 회로에서 확인합니다.'],
 repair=['TC03 값과 SP_INT/PV_IN의 Local 전달을 함께 확인합니다. 이름이 같은 다른 블록 변수로 대체하지 않습니다.','Auto,COM_RST,LMNR_HS/LS,QLMNUP/DN,최종Q2.4/Q2.5를 차례로 비교해 멈춘 구간을 구분합니다.','조절기 펄스와 MV WORK PULSE·최종 명령을 구분합니다. 엔코더리셋 중 출력 억제와 현재 위치/리미트를 대조합니다.','원본8은 TC03_SETPOINT<200일 때200을 쓰는 분기입니다. 설정 자동 보정과 현장 보호값을 동일하게 해석하지 않습니다.'],pending=['STL 줄바꿈·주석·실제 변환 명령','현재 자동/수동 전환·조절기 인스턴스 값','엔코더 위치와 리미트 정상극성']),
 dict(id='MV02',title='MV02 · 제목 PC01과 실제 PSH01 계측',priority='',equipment=['MV02','PSH01'],native=[7,1704],texts=[6],controller=(7,'172'),
 chain=['색인STL6은 Data.PSH01_SETPOINT와 Data.Press_PC01을 Local Real_SPPC01/Real_PC01로 변환하는 문구입니다. 원본 PSH01 환산IW284→Data.Press_PC01이며 PC01 IW322→Data.PC_01과 다릅니다.','원본7 CONT_S/PID_MV-02: GAIN-0.22·TI T#2S·DEADB_W2.0·CYCLE T#100MS·PULSE_TM T#200MS·BREAK_TM T#2S_500MS·MTR_TM T#18S.','COM_RST의 반전 Auto와 두 LMNR 리미트의 반전 연결, QLMNUP/DN→PID MV02 UP/Down을 보존합니다.','1704는 여러 ON 반전 접점을 포함합니다. 현재 ON 값과 실제 호출을 확인하지 않고 폐기·항상 정지·정상 작동으로 확정하지 않습니다.'],
 repair=['PC01이라는 제목보다 실제 Data.Press_PC01과 PSH01 경로를 먼저 대조합니다.','조절기 출력과1704최종 Open/Close의 반전접점·고장·리미트를 비교합니다.','GAIN의 부호를 현장 회전 방향·정상극성·제작사 의도 없이 바꾸지 않습니다.','설정/표시의 주소와 현재 전달을 확인하고 다른 계측의 표시값을 대신 사용하지 않습니다.'],pending=['PSH01/PC01 제목·표시 대응','ON반전 접점과 현장 사용 여부','현재 인스턴스·튜닝·회전방향']),
 dict(id='MV03',title='MV03 · PSH03 비교 루프와 별도 미사용 표기 PID',priority='P20',equipment=['MV03','PSH03','PSH02'],native=[15,1705,1706],texts=[14],controller=(15,'507'),
 chain=['1705 Sub: Data.PSH03_SETPOINT − Data.PSH03 → ErrPSH03. ≥5는 PID down MV03, <-5는 PID UP MV03에 연결되고 Tag_148 반전 및4초/10초 SD를 보존합니다.','별도 색인STL14은 PSH02_SETPOINT/PSH_02→Real_SPPC02/Real_PC02를 표시합니다. 원본15 CONT_S/PID_MV03는 en 앞OFF, 제목not used입니다.','원본15와1705는 같은 Global PID UP MV03/PID down MV03에 쓰는 경로입니다. OFF 값·현재 호출·OB간 순서를 확인하기 전 최종 쓰기와 사용 여부를 확정하지 않습니다.','1706 최종 Start open MV03/Start Close MV03는 자동·수동·세정·버너 기동닫힘·엔코더리셋·리미트를 함께 비교합니다.'],
 repair=['PSH03 비교와 PSH02 PID 경로를 별개로 관찰하고 현재 사용 경로를 제작사/CPU에서 확인합니다.','ErrPSH03와 두 방향명령·Tag147/148을 기록해 출력 미발생 구간을 구분합니다.','같은 방향명령의 두 쓰기 위치를 비교하고 not used 제목만으로 현재 미사용을 확정하지 않습니다.','세정/버너 기동 요청이 위치를 바꿀 수 있으므로 BR01 연동·리미트·리셋 상태를 함께 봅니다.'],pending=['두 압력 경로의 개정·사용 의도','OB와Valve Control loop 호출 순서','세정·기동닫힘과조절 요청 우선순위']),
 dict(id='MV05',title='MV05 · RO01 산소 CONT_S',priority='',equipment=['MV05','RO01'],native=[5,1708],texts=[4],controller=(5,'109'),
 chain=['색인STL4: Data.RO01_SETPOINT와 Data.Oxigen_RO01 → Real_SPO2/Real_O2 (블록Local). 단위·표시 배율·현재산소 교정은 확인 전입니다.','원본5 CONT_S/PID_MV05: GAIN2.0·TI T#1M·DEADB_W1.0·CYCLE T#100MS·PULSE_TM T#200MS·BREAK_TM T#3S·MTR_TM T#5S.','COM_RST는 반전Auto 또는 Oxigen_Fault와 반전 UNDER TESTING의 직렬 경로로 연결됩니다. LMNR_HS/LS의 리미트 접점은 반전입니다.','QLMNUP/DN → PID UP MV05/PID DOWN MV05 →1708 최종 Open MV05/Close MV05. RO01 원시IW352·외부호출enOFF와 IN0 ON의 경계는 계측 작업지에서 확인합니다.'],
 repair=['RO01 실측값/환산값/LocalPV/표시값을 같은 시각에 기록합니다. 산소 단위나 현재값을 임의 환산하지 않습니다.','Auto·Oxigen_Fault·UNDER TESTING과 COM_RST 경로를 비교합니다.','방향명령이 있어도 리미트·고장·수동·최종 출력을 따로 확인합니다.','반전 리미트와 실제 배선극성·실제 방향의 대응을 확인합니다.'],pending=['산소단위·교정·PV전달','UNDER TESTING 현재값·의도','현재호출·리미트정상극성']),
 dict(id='MV06',title='MV06 · PSH02 비교·저범위 순간 명령',priority='P21',equipment=['MV06','PSH02'],native=[1709,1710,1711],texts=[],controller=None,
 chain=['1709는 Data.PSH02_SETPOINT≠0 분기에서 설정−Data.PSH_02→ErrPSH02를 사용하며 ≥5→MV06 PID DOWN, <-5→MV06 PID UP을 연결합니다.','1710은 설정0의 별도 저범위 경로입니다. 비교 입력 PSH02는 원시IW286 심볼이며 Data.PSH_02와 분리합니다.','원시PSH02≤0 경로20초,>0 경로2초,Shot명령 뒤300ms SD를 보존합니다.1709의300ms/4초 SD와 다른 경로입니다.','1711은 두PID명령·Shot to open/close·수동요청·리미트·고장·MV WORK PULSE를 최종 Open MV06/Close MV06에 연결합니다.'],
 repair=['설정이0인지 먼저 확인해 정상 비교 경로와 저범위 경로를 구분합니다.','원시IW286와환산Data.PSH_02의 부호·영점·단위를 비교합니다.','Shot명령의 발생·유지·해제와 실제리미트를 확인하고300ms를실제기계이동시간으로 단정하지 않습니다.','비교출력→1711최종명령→회로→응답을 추적합니다. 리미트 명칭 불일치는 확인 대기로 유지합니다.'],pending=['원시/환산 비교의제작사 의도','저범위0·순간동작의실제사용','리미트명칭·현재시간·안전복구']),
 dict(id='VT02',title='VT02 제어 변수와 FN02 아날로그 출력',priority='P16',equipment=['FN02','TC03'],native=[8,12,1688],texts=[9,13],controller=None,
 chain=['색인STL9의 실제표기 l -15와 주석 meno30°C를 분리합니다. TC03_SETPOINT와Temp_TC03→Local Real_SP_TC03xMV04/Real_TC03xMV04가 표시됩니다.','색인STL13은 CONT_C/PID_VT02, GAIN Data_PID.GAIN_FN02·TI Data_PID.TI_FN02·CYCLE T#100MS·DEADB_W1.5·LMN상한100.0/하한35.0·RND→Data.Set_Perc_VT02를 표시합니다. 원본 실행명령·빈핀 기본값은 확인 전입니다.','원본12 VT02Manuale의 OR 분기에는 NOT Flag.MV04_Auto, NOT Start FN02, ON이 연결됩니다. 현재 ON 값 없이 항상 수동이라고 단정하지 않습니다.','1688 FN02 ventilation은 Data.Set_Perc_VT02를5/100제한·×272→FN02_SP(%QW306)에 연결합니다. 변수VT02·제목MV04·실제FN02의관계를 보존하되 실물별칭은확정하지 않습니다.'],
 repair=['TC03 설정의-15표기·30°C주석·실제활성코드를 대조합니다.','VT02Manuale와색인MAN_ON 연결·실제Local/SP/PV를 확인합니다.','PID하한35와출력제한5가서로다른단계임을 구분합니다.','FN02_SP/인버터/실제팬응답을 확인하고VT02/MV04를다른실물로 임의병합하지않습니다.'],pending=['-15표기/30°C주석·줄바꿈','VT02/MV04/FN02 명칭대응','색인PID의빈핀·현재인스턴스·실행코드']),
 dict(id='BR01',title='BR01 · TC01/TC02 선택과 버너 PID 전달',priority='P11',equipment=['BR01','TC01','TC02'],native=[1721,1722,1870,1871,1724,1686,1687],texts=[1719,1720],controller=None,
 chain=['색인SCL1719에는EnableTC01/02와OFR에따른 평균·단일값 선택 및Enable비트false쓰기, 둘다비활성의EmergencyStop, Allarm.EmergencyStopTC1_2 대입이 표시됩니다. 기존LAD핀색인의쓰기미확정과 별도문자근거로 유지합니다.','색인STL1720 CONT_C/PID-Burner: TC01_SETPOINT→SPvalue,PID_Ref_Temp→Procvalue,NOT Flag AutoBurner→Manuale,GAIN1.35·TI6분·TD5초·CYCLE1초·DEADB_W2.0·LMN하한5.0/상한Maxvalue·RND→I_Outvalue를 표시합니다.','원본1721OFF분기의수동Move/반자동Add와1722ON분기의Add(0,I_Outvalue)는WorkData.Burner_PID_Result에씁니다.1871Flag AutoBurner뒤Add(Result,0)는Data.Burner_Panel_SetPoint에씁니다.1870의0쓰기와함께대조합니다.','1724의공기설정±1,1686×272→QW310,가스경로1687×285→QW308을 별도추적합니다. 전용연소제어기 내부의보호와PLC조절출력을구분합니다.'],
 repair=['TC01/02 원시·환산·Enable·OFR·선택값을 같은시각에확인합니다.백업SCL표시만으로현재센서사용을확정하지않습니다.','Flag.AUTO_BURNER 요청과Flag AutoBurner의 실제허가를 구분하고Manuale·High Flame·Start·최대온도알람을 함께기록합니다.','PID결과→PanelSetPoint→AirOut/GasOut→QW→서보응답을비교합니다.0쓰기와결과전달의현재순서를확인합니다.','EmergencyStop의색인대입은추가근거로제공하며 기존공정알람대장의발생조건확정이나해소로처리하지않습니다.'],pending=['1719현재SCL·초기Enable·영구기억·동시OFR처리','1초OB와100msOB·주주기의실제순서','전용010-390내부연소보호·현재튜닝']),
 dict(id='STECHIO',title='가스·공기 비율 · CONT_C 보정과 가스 출력',priority='P11',equipment=['BR01'],native=[16,1830,1832,1834,1835,1687],texts=[1831,1833],controller=(1832,'663'),
 chain=['색인STL1831은Massico_Flow_AIR/GAS의ITD/DTR→Air_Flow/Gas_Flow, /R→Stechio_attuale→Stechio.Real_Stechio,Stechio.SET_STECHIO→SetPoint_Stechio를표시합니다. 현재단위·0나눗셈·범위외처리는확인전입니다.','1830은Burner_Air_Out과0,5,…,95의Ge분기·20개Gas_crv피연산자Move→Portata_Presunta_GAS를보존합니다.일련의≥조건이겹치며현재마지막값·호출순서를확인해야합니다.','1832 CONT_C/PID_Stechio: SP_INT SetPoint_Stechio/PV_IN Stechio_attuale는Local,LMN Correzione_Stechio도Local. GAIN/TI/TD/상하한은Stechio DB피연산자입니다. COM_RST와MAN_ON의High Flame·Disable masses·ON/OFF경로를함께봅니다.','색인STL1833은보정RND와Portata_Presunta_GAS+보정정수→Burner_Gas_Out을표시합니다.1834의0/100제한·1835의보정한계표시·1687×285→QW308을구분합니다.'],
 repair=['Air/Gas원시·환산·비율Local·SET_STECHIO를 비교합니다.단위와센서유효성없이목표비율을정하지않습니다.','COM_RST·MAN_ON·High Flame·Disable masses와조절기실제출력을함께봅니다.','Portata_Presunta_GAS·Correzione_Stechio·RND후정수·GasOut·QW308의각전달단계를확인합니다.','가스곡선·게인·한계값의변경은제작사자료와현재TIA에서 검토하며문서에서자동권장값을생성하지않습니다.'],pending=['현재물리단위·비율·분모보호','20구간곡선·겹치는조건과쓰기순서','현재인스턴스값·전용연소제어기경계'])]
for l in loops:
    l['field_verified']=False;l['plc_changes']=0
    l['text_refs']=[t for t in texts if t['id'] in l['texts']]
    l['native_refs']=[i for i in l['native']]
    if l['controller']:
        i,uid=l['controller'];c=next(n for n in pn[i]['nodes'] if n['uid']==uid);l['controller_evidence']=dict(network=i,**c)
    else:l['controller_evidence']=None
# Scope-aware trace is copied exactly. Local identity remains qualified by block.
selectors=[]
for p in proofs:
    for uid,ref in p['refs'].items():
        use=[u for u in trace if u['network']==p['id'] and u['oref']==uid]
        for u in use:
            if u['scope'] in ['Global','Local'] and u['name']:
                s=(u['name'],u['scope'],u['block'] if u['scope']=='Local' else None)
                if s not in selectors:selectors.append(s)
symbols=list(csv.DictReader((ROOT/'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
signals=[]
for name,scope,block in selectors:
    same=lambda u:canon(u['name'])==canon(name) and u['scope']==scope and (scope!='Local' or u['block']==block)
    uses=[u for u in trace if same(u)];other=[u for u in trace if canon(u['name'])==canon(name) and not same(u)]
    paths.update(u['file'] for u in uses+other);paths.update(d['file'] for u in uses+other for d in u['declarations'])
    signals.append(dict(name=name,scope=scope,block=block,usages=uses,other_scope_usages=other,symbols=[s for s in symbols if scope=='Global' and canon(s['원본 심볼'])==canon(name)]))
register=dict(date='2026-10-08',scope='Static native LAD and separately preserved backup search-index STL/SCL text; not PLC execution',loops=loops,native_ids=selected,native=proofs,indexed_texts=texts,signals=signals,sources={p:sha(p) for p in sorted(paths)},field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun')
hmi=list(csv.DictReader((ROOT/'registers/equipment-hmi.csv').open(encoding='utf-8-sig')))
for l in loops:l['hmi_reference_rows']=[r for r in hmi if r['설비 ID'] in l['equipment']]
(ROOT/'registers/regulation-manual.json').write_text(json.dumps(register,ensure_ascii=False,indent=2)+'\n')
def link(path,label):return '<a href="'+e(path)+'">'+e(label)+'</a>'
def table(headers,rows):return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def netlink(i):return link('networks/network-'+str(i)+'.html','원본 '+str(i))
def refsdisplay(pin):
    refs=' / '.join(('ORef '+r['oref']+' · '+(r['name'] if r['name'] is not None else '[미해석·RefId 없음; 기본값 추정 금지]')) for r in pin['references'])
    peers=' / '.join(x['kind']+' '+str(x['uid'])+'.'+str(x['pin']) for x in pin['peers'])
    return e(refs or peers or '[연결 추가 확인]')
hmi=list(csv.DictReader((ROOT/'registers/equipment-hmi.csv').open(encoding='utf-8-sig')))
body='<h1>주요 조절 루프 · 입력·설정·출력·수리 근거</h1><p>9개 분석 작업지 · 원본 LAD33네트워크 · CONT_S4개/CONT_C1개 native LRef · 색인 STL/SCL10항목</p><div class="notice info">실행 모델을 만들거나 시뮬레이터를 수정하지 않습니다. 원본 LAD의 UID/RID/NID·배선 근거와 백업 검색 색인의 STL/SCL 문자 근거를 구분합니다. 색인 문자에는 원래 줄바꿈·주석 경계·빈 인수·현재 컴파일·CPU 실행이 확인되지 않은 부분이 있습니다. 현재값·튜닝·물리 단위·실물 동일성·수리 완료는 확인 전입니다.</div>'
body+='<nav class="inline-actions">'+link('sensor-measurement.html','온도·압력·산소 계측')+link('measurement-trace.html','가스·공기 환산·출력')+link('burner-interface.html','버너 연동·복구')+link('index.html#view=review&equipment=P11&scope=priority','근거 검토·확인')+'</nav><h2 id="index">루프 선택</h2>'
body+=table(['작업지','원본 LAD','STL/SCL 색인','확인 경계'],[[link('#loop-'+l['id'],l['title']),e(' · '.join(map(str,l['native']))),e(' · '.join(map(str,l['texts'])) or '해당 선택 없음'),e(' · '.join(l['pending']))] for l in loops])
for l in loops:
    body+='<section><h2 id="loop-'+l['id']+'">'+e(l['title'])+'</h2><nav class="inline-actions">'
    if l['priority']:body+=link('index.html#view=repair-record&equipment='+l['priority']+'&scope=priority','관련 우선 설비 수리 기록')
    for equipment in l['equipment']:
        if (ROOT/'procedures'/f'{equipment}.html').exists():body+=link('procedures/'+equipment+'.html',equipment+' 증상별 수리')
        if (ROOT/'circuit-guides'/f'{equipment}.html').exists():body+=link('circuit-guides/'+equipment+'.html',equipment+' 회로·전달')
        if (ROOT/'signal-guides'/f'{equipment}.html').exists():body+=link('signal-guides/'+equipment+'.html',equipment+' 읽기·쓰기')
    if l['id'] in ['MV01','MV02','MV03','MV05','MV06']:body+=link('encoder-position.html#position-'+l['id'],'엔코더·위치·교정 수리')
    body+='</nav><h3>입력 → 설정·모드 → 조절·비교 → 출력</h3><ol>'+''.join('<li>'+e(s)+'</li>' for s in l['chain'])+'</ol>'
    body+='<h3>증상별 관찰·배제·다음 확인</h3>'+table(['증상','관찰·비교','판단 근거'],[[e(t),e(s),'현재값·현재버전·관찰시각과 '+ ' · '.join(netlink(i) for i in l['native'])] for t,s in zip(['자동인데 출력이 없음','입력·설정과 동작 방향이 맞지 않음','명령은 변하는데 실물이 반응하지 않음','값이 되돌아가거나 정지·모드전환 후 재발'],l['repair'])])
    c=l['controller_evidence']
    if c:
        body+='<h3>원본 조절기 호출·인스턴스·핀 배선</h3><p>'+netlink(c['network'])+' · LRef '+e(c['uid'])+' / '+e(c['tree']['attributes'])+' · '+e(' / '.join(d['name'] for d in c['declarations']))+' · 인스턴스 '+e(' / '.join(d['name'] for x in c['children_declarations'] for d in x['declarations']))+'</p>'
        body+=table(['원본 핀','ORef 이름 또는 연결 노드','Wire'],[[e(p['pin']),refsdisplay(p),link('#wire-'+str(c['network'])+'-'+p['wire'],p['wire'])] for p in c['pins']])
        body+='<p>핀의 방향·빈 RefId·기본값·현재 인스턴스는 일반 추정으로 채우지 않습니다. Local SP/PV는 같은 블록의 변수이며 Global 값과 동일성은 별도 문자/현재 TIA 근거가 필요합니다.</p>'
    body+='<h3>선택 원본 근거</h3><p>'+' · '.join(link('#native-'+str(i),'LAD '+str(i)+' 핀·조건') for i in l['native'])+'</p><p>'+' · '.join(link('#text-'+str(i),'색인 문자 '+str(i)) for i in l['texts'])+'</p>'
    rows=l['hmi_reference_rows']
    body+='<details><summary>기존 HMI 설정 참고 · '+str(len(rows))+'행</summary>'+table(['설비ID','HMI 태그','설정주소','Access','내부ID'],[[e(r[k]) for k in ['설비 ID','HMI 태그','설정 주소','Access Name','내부 ID']] for r in rows])+'<p>원본 설정 참고입니다. PLC 변수·DB 오프셋·단위·현재 표시값 일치를 증명하지 않습니다.</p></details>'
    body+='<h3>추가 확인</h3><ul>'+''.join('<li>'+e(p)+'</li>' for p in l['pending'])+'</ul></section>'
body+='<h2 id="texts">STL/SCL 원본 색인 문자 · 줄바꿈 복원·실행 확인 전</h2><p>sources/live_index.json의 segment·문서ID·Code 필드를 삭제하지 않고 그대로 보존합니다. block_summary.json과 일치 대조합니다. 이 자료는 LAD Wire/ORef 목록이나 현재 TIA 컴파일 결과가 아닙니다.</p>'
for t in texts:
    body+='<details id="text-'+str(t['id'])+'"><summary>'+e(str(t['id'])+' · '+t['block']+' · '+t['language'])+'</summary><p>'+e(t['segment'])+' / 문서 '+str(t['id'])+' · '+link(t['source'],'백업 색인 JSON')+' · 문자 SHA256 '+e(t['text_sha256'])+'</p><pre>'+e(t['text'])+'</pre></details>'
body+='<h2 id="native">원본 LAD · 접점·연산·배선 증거</h2><p>표의 나열 순서는 실행 순서나 직렬·병렬 조건을 대신하지 않습니다. 같은 Wire의 PCon 연결과 원본을 함께 확인합니다. NOT 표기는 해당 Part의 원본 Negated PinName입니다.</p>'
for p in proofs:
    body+='<details id="native-'+str(p['id'])+'"><summary>'+e(str(p['id'])+' · '+p['block']+' · '+p['title'])+'</summary><p>'+netlink(p['id'])+' · '+link(p['file'],'원본 XML')+' · SHA256 '+e(p['sha256'])+'</p>'
    rows=[]
    for n in p['nodes']:
        meta=' / '.join(d['name'] for d in n['declarations']);attrs=n['tree']['attributes'];neg=[x['attributes'].get('PinName') for x in n['tree']['children'] if x['tag']=='Negated'];templates=[(x['attributes'].get('Name'),x['text']) for x in n['tree']['children'] if x['tag']=='TemplateValue']
        for pin in n['pins']:rows.append([e(n['uid']),e(n['gate'] or n['kind']),e(meta+' '+str(attrs)+' NOT '+str(neg)+' '+str(templates)),e(pin['pin']),refsdisplay(pin),link('#wire-'+str(p['id'])+'-'+pin['wire'],pin['wire'])])
    body+=table(['Part/LRef/CRef','종류','원본속성·반전·형식','핀','피연산자/노드','Wire'],rows)
    body+=table(['Wire','전체 원본 연결'],[['<span id="wire-'+str(p['id'])+'-'+w['uid']+'">'+e(w['uid'])+'</span>',e(' / '.join(x['kind']+' '+str(x['uid'])+'.'+str(x['pin']) for x in w['ends']))] for w in p['wires']])+'</details>'
body+='<h2 id="writes">같은 이름의 읽기·쓰기와 Local 경계</h2><p>기존 전체 LAD핀 색인에서 해당 정확한 범위를 추적합니다. STL/SCL 문자에만 표시된 전달·대입을 LAD핀으로 생성하지 않습니다. 이름 일치만으로 다른 블록 Local을 합치지 않습니다. pending은 방향 확인 전이며 읽기나 쓰기로 단정하지 않습니다.</p>'
for s in signals:
    body+='<details><summary>'+e(s['name']+' · '+s['scope']+' · '+str(s['block'] or ''))+' · '+str(len(s['usages']))+'핀 / 다른범위 '+str(len(s['other_scope_usages']))+'</summary>'
    body+=table(['네트워크·핀','분류','블록·범위','백업 주소'],[[' · '.join([netlink(u['network']),e(u['part']+'.'+str(u['pin']))]),e(u['role']),e(u['block']+' / '+u['scope']),e(' / '.join(sy['백업 주소'] for sy in s['symbols']))] for u in s['usages']])
    if s['other_scope_usages']:body+='<p>같은 이름의 다른범위: '+e(' / '.join(str(u['network'])+' '+u['scope']+' '+u['block'] for u in s['other_scope_usages']))+'</p>'
    body+='</details>'
body+='<h2 id="checks">현장·현재 TIA에서 확정할 항목</h2><p>현재 CPU 백업/온라인 비교·OB 이벤트 주기·호출/쓰기 순서·초기 ON/OFF·인스턴스 값·STL/SCL 줄바꿈과 주석·빈 인수·센서 단위·실제 출력/응답·제작사 보호기준을 확인합니다. 기존 자료 불일치18건, 확인 대장1,060건, 설계시험577건의 상태는 변경하지 않습니다. PLC변경·실제 수리 완료0건입니다.</p>'+link('registers/regulation-manual.json','선택 원본·색인 문자·범위 근거 JSON')
body+='''<script>function revealEvidence(){let id;try{id=decodeURIComponent(location.hash.slice(1));}catch(_){return;}const target=document.getElementById(id);if(!target)return;let parent=target;while(parent){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}target.scrollIntoView({block:'start'});}addEventListener('hashchange',revealEvidence);revealEvidence();</script>'''
(ROOT/'regulation-manual.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>주요 조절 루프 수리·구조 매뉴얼</title><link rel="stylesheet" href="assets/all-in-one.css"><style>main{max-width:1320px;margin:auto;padding:24px}td{vertical-align:top;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f5f9;padding:16px}h2{scroll-margin-top:20px}li{margin:.6em 0}details{margin:12px 0}summary{cursor:pointer;font-weight:600}.inline-actions{flex-wrap:wrap}@media print{details{display:block}.table-wrap{overflow:visible}}</style></head><body><main>'+body+'</main></body></html>')
print(json.dumps(dict(status='built',loops=len(loops),native_networks=len(proofs),native_pid_calls=5,indexed_texts=len(texts),signals=len(signals),sources=len(paths),simulator_development='stopped_by_user'),ensure_ascii=False))
