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
import re
from collections import Counter,defaultdict
groups=['hmi','hmi inputs','hmi output','hmi standard motors','hmi standard motorized valve','hmi pv_1gate','hmi pv_2gate']
selected=sorted(n['id'] for n in m['networks'] if n['block'] in groups)
proofs=[native(i) for i in selected]
readcsv=lambda f:list(csv.DictReader((ROOT/f).open(encoding='utf-8-sig',newline='')))
tags=readcsv('sources/hmi_plc_tags.csv');windows=readcsv('sources/hmi-windows.csv');assigned=readcsv('registers/equipment-hmi.csv');symbols=readcsv('registers/plc-symbols.csv');equipment_networks=readcsv('registers/equipment-networks.csv')
priority=readcsv('registers/priority-equipment.csv')
paths.update(['sources/hmi_plc_tags.csv','sources/hmi-windows.csv','registers/hmi-window-provenance.json','registers/equipment-networks.csv','registers/equipment-hmi.csv','registers/plc-symbols.csv'])
def address(s,access):
 db=re.fullmatch(r'DB(\d+),(X|INT|W|REAL|D)(\d+)(?:\.(\d+))?',s)
 if db:
  num,kind,offset,bit=db.groups();offset=int(offset)
  if kind=='X':
   if bit is None or not 0<=int(bit)<=7:return dict(kind='unparsed',raw=s)
   start=offset*8+int(bit);width=1
  else:
   if bit is not None:return dict(kind='unparsed',raw=s)
   start=offset*8;width={'INT':16,'W':16,'REAL':32,'D':32}[kind]
  return dict(kind='db',area='DB'+str(int(num)),notation=kind,start_bit=start,end_bit=start+width,width_bits=width,access=access,raw=s,plc_member_offset_verified=False)
 p=re.fullmatch(r'(E|A)(B|W)(\d+)',s)
 if p:
  area,kind,offset=p.groups();width={'B':8,'W':16}[kind];start=int(offset)*8
  return dict(kind='physical',area={'E':'I','A':'Q'}[area],notation=area+kind,start_bit=start,end_bit=start+width,width_bits=width,access=access,raw=s,interpretation='notation_and_address_range_candidate_not_current_connection')
 p=re.fullmatch(r'MX(\d+)\.([0-7])',s)
 if p:
  start=int(p[1])*8+int(p[2]);return dict(kind='memory',area='M',notation='MX',start_bit=start,end_bit=start+1,width_bits=1,access=access,raw=s,interpretation='notation_and_address_range_candidate_not_current_connection')
 if s=='$SYS$Status':return dict(kind='driver_status',raw=s,interpretation='driver_status_not_a_physical_PLC_address')
 return dict(kind='unparsed',raw=s)
def plc_address(s):
 p=re.fullmatch(r'%([IQM])([BWD]?)(\d+)(?:\.([0-7]))?',s.upper())
 if not p:return None
 area,kind,byte,bit=p.groups()
 if bit is not None:
  if kind:return None
  start=int(byte)*8+int(bit);width=1
 else:
  if not kind:return None
  start=int(byte)*8;width={'B':8,'W':16,'D':32}[kind]
 return dict(area=area,start_bit=start,end_bit=start+width,width_bits=width)
def overlap(a,b):return a['area']==b['area'] and a['start_bit']<b['end_bit'] and b['start_bit']<a['end_bit']
audits=[]
for index,row in enumerate(tags):
 parsed=address(row['설정 주소'],row['Access Name']);matches=[]
 if parsed['kind'] in ['physical','memory']:
  for sym in symbols:
   p=plc_address(sym['백업 주소'])
   if p and overlap(parsed,p):
    use=[u for u in trace if u['scope']=='Global' and canon(u['name'])==canon(sym['원본 심볼'])]
    matches.append(dict(symbol=sym,relation='same_span_candidate' if parsed['start_bit']==p['start_bit'] and parsed['end_bit']==p['end_bit'] else 'overlapping_span_candidate',usages=use))
    paths.update(u['file'] for u in use)
 eq=[x['설비 ID'] for x in assigned if x['HMI 태그']==row['HMI 태그'] and x['설정 주소']==row['설정 주소'] and x['Access Name']==row['Access Name'] and x['내부 ID']==row['태그 내부 ID']]
 audits.append(dict(index=index,anchor='tag-'+row['태그 내부 ID'],source=row,parsed=parsed,existing_equipment_references=eq,physical_symbol_candidates=matches,current_mapping_verified=False,screen_read_write_verified=False))
same=defaultdict(list)
for x in audits:same[x['source']['Access Name'],x['source']['설정 주소']].append(x['index'])
shared=[dict(access=k[0],address=k[1],tag_indices=v,status='shared_configuration_address_not_confirmed_error') for k,v in same.items() if len(v)>1]
range_overlaps=[]
for i,a in enumerate(audits):
 pa=a['parsed']
 if 'area' not in pa:continue
 for b in audits[i+1:]:
  pb=b['parsed']
  if 'area' not in pb or pa['access']!=pb['access'] or not overlap(pa,pb):continue
  range_overlaps.append(dict(a=a['index'],b=b['index'],relation='same_span' if pa['start_bit']==pb['start_bit'] and pa['end_bit']==pb['end_bit'] else 'overlapping_span',status='configuration_range_comparison_not_confirmed_error'))
profiles=[]
for p in priority:
 indices=[a['index'] for a in audits if p['plc_id'] and p['plc_id'] in a['existing_equipment_references']]
 existing=[x for x in equipment_networks if x['설비 ID']==p['plc_id'] and int(x['문서 ID']) in selected] if p['plc_id'] else []
 profiles.append(dict(key=p['key'],name=p['name'],plc_id=p['plc_id'],identity_verified=False,tag_indices=indices,existing_native_reference_rows=existing,field_verified=False))
selectors=[]
for p in proofs:
 for uid in p['refs']:
  for u in trace:
   if u['network']==p['id'] and u['oref']==uid and u['scope'] in ['Global','Local'] and u['name']:
    s=(u['name'],u['scope'],u['block'] if u['scope']=='Local' else None)
    if s not in selectors:selectors.append(s)
signals=[]
for name,scope,block in selectors:
 same_scope=lambda u:canon(u['name'])==canon(name) and u['scope']==scope and (scope!='Local' or u['block']==block)
 uses=[u for u in trace if same_scope(u)];other=[u for u in trace if canon(u['name'])==canon(name) and not same_scope(u)]
 paths.update(u['file'] for u in uses+other)
 signals.append(dict(name=name,scope=scope,block=block,usages=uses,other_scope_usages=other))
title_only=[dict(segment=n['segment'],id=n['doc'],values=live[n['segment'],n['doc']]['values'],status='index_title_only_no_native_LAD') for b in blocks if b['name']=='hmi' for n in b['networks'] if n['doc'] not in selected]
counts=dict(tags=len(tags),windows=len(windows),native_networks=len(proofs),priority_profiles=len(profiles),shared_address_groups=len(shared),overlapping_tag_pairs=len(range_overlaps),address_kinds=dict(Counter(a['parsed']['kind'] for a in audits)),symbol_candidate_tags=sum(bool(a['physical_symbol_candidates']) for a in audits),same_span_candidate_tags=sum(any(s['relation']=='same_span_candidate' for s in a['physical_symbol_candidates']) for a in audits),title_only_networks=len(title_only))
# The priority register is a preserved input; source register identity stays explicit.
priority_path='registers/priority-equipment.csv'
paths.add(priority_path)
result=dict(date='2026-10-08',scope='Exported HMI CSV address audit and native LAD interface evidence; not DB member layout, original screen events or current PLC communication',counts=counts,tags=audits,shared_addresses=shared,address_overlaps=range_overlaps,windows=windows,window_provenance=load('registers/hmi-window-provenance.json'),profiles=profiles,native_ids=selected,native=proofs,title_only_networks=title_only,signals=signals,sources={p:sha(p) for p in sorted(paths)},field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun')
(ROOT/'registers/hmi-transfer.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
def link(path,label):return '<a href="'+e(path)+'">'+e(label)+'</a>'
def netlink(i):return link('networks/network-'+str(i)+'.html','원본 '+str(i))
def table(headers,rows):return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
taglink=lambda i:link('#'+audits[i]['anchor'],audits[i]['source']['HMI 태그'])
body='<h1>HMI 설정·표시·PLC 전달 확인 매뉴얼</h1><p>'+str(len(tags))+'개 설정 태그 · '+str(len(windows))+'개 화면 메타데이터 · 원본 LAD'+str(len(proofs))+'네트워크 · 우선23개 참조 작업지</p><div class="notice info">태그 설정 주소와 현재 HMI 동작·PLC 연결을 구분합니다. DB 번호/바이트 주소로 PLC 멤버를 역산하지 않습니다. Access Name은 이 설정의 접속 이름이며 화면 객체의 읽기/쓰기 권한·명령 실행을 증명하지 않습니다. E/A↔I/Q 표기와 주소 범위 비교는 대조 후보이며 현재 연결·설비 소유·실물 동일성은 확인 전입니다. 시뮬레이터 작성·수정·행동 시험은 중지합니다.</div>'
body+='<nav class="inline-actions">'+link('#tags','782개 태그 검색')+link('#profiles','우선 설비별 확인')+link('#shared','같은 주소·범위 교차')+link('#windows','화면 목록')+link('#native','원본 HMI 가공')+link('#repair','증상별 확인')+link('regulation-manual.html','조절 루프')+link('encoder-position.html','엔코더·위치')+'</nav>'
body+='<h2 id="repair">증상별 확인 순서</h2>'+table(['증상','관찰·대조 순서','확인 경계'],[
 ['화면 값이 고정되거나 다른 화면과 다름','같은 시각의 화면 이름/객체/태그/Access Name/설정 주소/품질·시각 → PLC 원시/환산/가공 값 → 호출·다른 쓰기를 기록합니다.','촬영된 HMI 이미지나 드라이버 상태 태그만으로 전체 PLC 통신을 정상 판정하지 않습니다.'],
 ['입력한 설정이 되돌아감','화면 이벤트와 쓰기 대상·자료형·입력 제한 → PLC 변수의 다른 쓰기·초기화·레시피·클램프 → 전달 순서와 실제값을 비교합니다.','입력란 이름이나 설정 CSV에는 버튼/스크립트의 실제 쓰기 이벤트 근거가 없습니다. 현재 화면 프로젝트가 필요합니다.'],
 ['운전/교정 요청 버튼을 눌러도 반응 없음','객체 이벤트 → HMI 요청 태그 → 정확한 PLC 멤버/현재DB오프셋 → 최종 명령의 허가·고장·리미트 → 응답을 따로 비교합니다.','DB41,X50.5/X50.6 RESET_ENC와 HMI_DB 교정 필드의 이름 대조만으로 실제 오프셋 연결을 확정하지 않습니다.'],
 ['상태·알람 표시와 센서가 다름','물리 I/접촉기 응답/리미트 → 처리 Inputs → HMI 가공 호출/출력/알람 누적 → 화면 색상/점멸 조건을 비교합니다.','Risposta·Allarme·DB11 상태 주소는 원시 입력 주소와 다릅니다. RefId 없는 호출 핀은 기본값으로 채우지 않습니다.'],
 ['두 태그가 같이 바뀌거나 단위가 맞지 않음','Access Name+주소·폭·범위 교차·정수/실수 형식·배율·단위·워드/비트 가공과 실제 화면 식을 확인합니다.','주소 공유는 오류 확정이 아닙니다. DB14 I_W20/O_W20, I_W22/O_W22의 의도와 현재 멤버 배치를 확인합니다.']])
body+='<h2 id="profiles">우선23개 설비의 기존 참조와 연결 경계</h2>'+table(['선택 설비','PLC 참고','HMI 기존 참조 태그','HMI 원본 기존 참조'],[[link('#profile-'+p['key'],p['key']+' · '+p['name']),e(p['plc_id'] or '대응 미확정'),str(len(p['tag_indices'])),' · '.join(netlink(int(x['문서 ID'])) for x in p['existing_native_reference_rows']) or '현재 선택 없음'] for p in profiles])
for p in profiles:
 body+='<details id="profile-'+p['key']+'"><summary>'+e(p['key']+' · '+p['name'])+' · '+str(len(p['tag_indices']))+'태그</summary><p>기존 설비 이름 참조이며 실물 동일성·DB 멤버·현재 연결을 확정하지 않습니다. 대응 미확정 설비에는 다른 장치의 태그를 부여하지 않습니다.</p>'+link('index.html#view=repair-record&equipment='+p['key']+'&scope=priority','이 설비 수리 기록')+table(['HMI 태그','주소','형식 범위','대조 근거'],[[taglink(i),e(audits[i]['source']['설정 주소']),e(audits[i]['parsed']['kind']), '설정 CSV · 현재 DB/이벤트 확인 전'] for i in p['tag_indices']])+'</details>'
body+='<h2 id="tags">전체 태그 · 설정 주소 검색</h2><label for="hmi-search">태그·주소·설비·심볼 검색</label><input id="hmi-search" type="search" placeholder="예: RESET_ENC, DB14,W20, FN04, EW394"><label for="hmi-kind">주소 종류</label><select id="hmi-kind"><option value="">전체</option>'+''.join('<option value="'+e(k)+'">'+e(k)+'</option>' for k in counts['address_kinds'])+'</select><p id="hmi-filter-count" aria-live="polite">'+str(len(tags))+' / '+str(len(tags))+'태그</p><div class="table-wrap"><table id="hmi-tag-table"><thead><tr>'+''.join('<th>'+e(k)+'</th>' for k in ['태그·내부ID','주소·Access Name','표기·범위','기존 설비 참조','PLC 주소 범위 후보'])+'</tr></thead><tbody>'
for a in audits:
 row=a['source'];pa=a['parsed'];sy=a['physical_symbol_candidates'];terms=' '.join([row['HMI 태그'],row['설정 주소'],row['Access Name'],row['태그 내부 ID'],*a['existing_equipment_references'],*(s['symbol']['원본 심볼'] for s in sy)])
 span=pa['kind']+' / '+(pa.get('area','')+' / '+pa.get('notation','')+' / bit '+str(pa['start_bit'])+'…'+str(pa['end_bit']-1) if 'area' in pa else 'PLC 바이트 주소로 해석하지 않음')
 candidates=[]
 for s in sy:
  text=s['symbol']['원본 심볼']+' '+s['symbol']['백업 주소']+' '+s['relation'];nets_=sorted({u['network'] for u in s['usages']});candidates.append(e(text)+'<br>'+' · '.join(netlink(n) for n in nets_))
 body+='<tr id="'+a['anchor']+'" data-kind="'+pa['kind']+'" data-search="'+e(terms.casefold())+'"><td>'+e(row['HMI 태그'])+'<br>'+e(row['태그 내부 ID'])+'</td><td>'+e(row['설정 주소'])+'<br>'+e(row['Access Name'])+'</td><td>'+e(span)+'</td><td>'+e(' / '.join(a['existing_equipment_references']) or '미배정/공통 참조')+'</td><td>'+('<br>'.join(candidates) if candidates else 'DB 멤버/현재 화면·통신 추가 확인')+'</td></tr>'
body+='</tbody></table></div><p>'+link('sources/hmi_plc_tags.csv','기존 782태그 원본 CSV')+' · 주소 해석은 표기/범위 대조입니다. INT/W16bit와REAL/D32bit의 폭 비교가 현재 DB 타입·엔디안·단위를 증명하지 않습니다.</p>'
body+='<h2 id="shared">같은 설정 주소와 다른 폭의 범위 교차</h2><p>같은 Access Name·주소 '+str(len(shared))+'그룹, 표기상 같은/겹치는 범위 '+str(len(range_overlaps))+'태그쌍입니다. 워드와 비트의 교차는 상태 비트 가공처럼 의도된 구조일 수 있습니다. 새 불일치나 확인 완료로 처리하지 않습니다.</p>'+table(['Access Name','주소','태그','상태'],[[e(x['access']),e(x['address']),' / '.join(taglink(i) for i in x['tag_indices']),'설정 공유 · 의도/현재 연결 확인 전'] for x in shared])
body+='<details><summary>전체 범위 교차 '+str(len(range_overlaps))+'쌍</summary>'+table(['태그A','주소A','태그B','주소B','관계'],[[taglink(x['a']),e(tags[x['a']]['설정 주소']),taglink(x['b']),e(tags[x['b']]['설정 주소']),e(x['relation'])] for x in range_overlaps])+'</details>'
body+='<h2 id="windows">기존 화면 메타데이터17개</h2><p>기존 GitHub 내보내기 CSV를 그대로 보존했습니다. 이름·ID·Parent ID는 현재 메뉴 노출·객체 연결·태그/스크립트·실행 상태를 증명하지 않습니다. SIN1_DECOATER 이름과 제공된 HMI 이미지를 참고하며 각 객체의 이벤트는 현재 화면 프로젝트에서 확인합니다.</p>'+table(['화면 이름','ID','Parent ID','설명','한계'],[[e(w[k]) for k in ['화면 이름','ID','Parent ID','설명','근거와 한계']] for w in windows])+link('sources/hmi-windows.csv','화면 내보내기 CSV')+' · '+link('registers/hmi-window-provenance.json','보존·이전 GitHub 아카이브 대조 근거')+' · '+link('assets/HMI_DECOATER.png','제공된 기본 HMI 이미지')
body+='<h2 id="native">원본 HMI 상태 가공·호출·배선</h2><p>hmi 블록의 원본 네트워크 '+str(sum(p['block']=='hmi' for p in proofs))+'개와 공통 가공/입력/출력 원본을 보존합니다. RefId가 없는 ORef는 실제 태그·기본값을 역산하지 않습니다. Local helper핀과 Global DB주소가 연결됐다고 단정하지 않습니다. 표의 나열은 실행 순서가 아닙니다.</p>'
for p in proofs:
 body+='<details id="native-'+str(p['id'])+'"><summary>'+e(str(p['id'])+' · '+p['block']+' · '+p['title'])+'</summary><p>'+netlink(p['id'])+' · '+link(p['file'],'원본 XML')+' · '+e(p['sha256'])+'</p>'
 rows=[]
 for n in p['nodes']:
  for pin in n['pins']:
   refs=' / '.join('ORef '+r['oref']+' · '+(r['name'] or '[미해석·RefId 없음]') for r in pin['references']);peers=' / '.join(q['kind']+' '+str(q['uid'])+'.'+str(q['pin']) for q in pin['peers'])
   rows.append([e(n['uid']+' · '+str(n['gate'] or n['kind'])),e(str(n['tree']['attributes'])+' / '+str(n['tree']['children'])+' / '+str(n['declarations'])+' / '+str(n['children_declarations'])),e(pin['pin']),e(refs or peers),link('#wire-'+str(p['id'])+'-'+pin['wire'],pin['wire'])])
 body+=table(['노드','반전·형식·선언','핀','연결','Wire'],rows)+table(['Wire','전체 연결'],[['<span id="wire-'+str(p['id'])+'-'+w['uid']+'">'+e(w['uid'])+'</span>',e(' / '.join(x['kind']+' '+str(x['uid'])+'.'+str(x['pin']) for x in w['ends']))] for w in p['wires']])+'</details>'
body+='<h3>색인 제목만 있고 선택 원본 LAD가 없는 항목</h3>'+table(['문서ID','원본 색인 값','상태'],[[e(x['id']),e(x['values']),'제목의 deleted 표기 · 현재 프로그램/사용 여부 확인 전'] for x in title_only])
body+='<h2 id="writes">같은 신호의 읽기·쓰기와 Local 경계</h2><p>전체 LAD핀 색인의 정확한 범위를 대조합니다. HMI 이름/DB바이트 주소와 Local 변수를 합치지 않습니다. pending은 방향 확인 전입니다.</p>'
for s in signals:
 body+='<details><summary>'+e(s['name']+' · '+s['scope']+' · '+str(s['block'] or ''))+' · '+str(len(s['usages']))+'핀 / 다른범위 '+str(len(s['other_scope_usages']))+'</summary>'+table(['네트워크·핀','역할','블록·범위'],[[netlink(u['network'])+' · '+e(u['part']+'.'+str(u['pin'])),e(u['role']),e(u['block']+' / '+u['scope'])] for u in s['usages']])
 if s['other_scope_usages']:body+='<p>'+e(' / '.join(str(u['network'])+' '+u['scope']+' '+u['block'] for u in s['other_scope_usages']))+'</p>'
 body+='</details>'
body+='<h2 id="checks">현재 화면·TIA에서 추가 확보할 근거</h2><p>현재 HMI 프로젝트/화면 객체·버튼/스크립트의 읽기·쓰기 이벤트·Access Name의 실제 Topic/장치 그룹·통신 품질/시각·PLC DB번호/멤버 오프셋/최적화·현재 자료형/배율·초기값/레시피/복수쓰기·OB 호출을 확인합니다. 기존 자료 불일치18건·확인 대장1,060건·설계시험577건의 상태는 변경하지 않습니다. PLC변경·실제수리완료0건입니다.</p>'+link('registers/hmi-transfer.json','전체 태그·범위 후보·원본·해시 JSON')
body+='''<script>const hmiRows=[...document.querySelectorAll('#hmi-tag-table tbody tr')];function filterHmi(){const q=document.getElementById('hmi-search').value.toLocaleLowerCase().trim();const kind=document.getElementById('hmi-kind').value;let count=0;for(const row of hmiRows){const show=(!kind||row.dataset.kind===kind)&&(!q||row.dataset.search.includes(q));row.hidden=!show;if(show)count++;}document.getElementById('hmi-filter-count').textContent=count+' / '+hmiRows.length+'태그';}document.getElementById('hmi-search').addEventListener('input',filterHmi);document.getElementById('hmi-kind').addEventListener('change',filterHmi);function revealEvidence(){let id;try{id=decodeURIComponent(location.hash.slice(1));}catch(_){return;}const target=document.getElementById(id);if(!target)return;if(target.matches('#hmi-tag-table tbody tr')){document.getElementById('hmi-search').value='';document.getElementById('hmi-kind').value='';filterHmi();}let parent=target;while(parent){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}target.scrollIntoView({block:'start'});}addEventListener('hashchange',revealEvidence);revealEvidence();</script>'''
(ROOT/'hmi-transfer.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HMI 설정·표시·PLC 전달 확인</title><link rel="stylesheet" href="assets/all-in-one.css"><style>main{max-width:1320px;margin:auto;padding:24px}td{vertical-align:top;overflow-wrap:anywhere}h2{scroll-margin-top:20px}details{margin:12px 0}summary{cursor:pointer;font-weight:600}.inline-actions{flex-wrap:wrap}#hmi-search{max-width:620px}tr[hidden]{display:none!important}label{display:inline-block;margin:8px}</style></head><body><main>'+body+'</main></body></html>')
print(json.dumps(dict(status='built',**counts,source_hashes=len(paths),simulator_development='stopped_by_user'),ensure_ascii=False))
