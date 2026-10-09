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
from collections import Counter
readcsv=lambda f:list(csv.DictReader((ROOT/f).open(encoding='utf-8-sig',newline='')))
priority=readcsv('registers/priority-equipment.csv');hmi=readcsv('sources/hmi_plc_tags.csv')
paths.update(['registers/priority-equipment.csv','sources/hmi_plc_tags.csv'])
fields=[('bwf01','Data.SET_PERC_BWF01','Editor_BWF01'),('bwf02','Data.SET_PERC_BWF02','Editor_BWF02'),('rd01','Data.SET_PERC_FR01','Editor_RD01'),('fn01','Data.SET_PERC_VT01','Editor_FN01'),('psh01','Data.PSH01_SETPOINT','Editor_PSH01'),('psh02','Data.PSH02_SETPOINT','Editor_PSH02'),('tc03','Data.TC03_SETPOINT','Editor_TC03'),('tc01','Data.TC01_SETPOINT','Editor_TC01')]
recipe_block=next(b for b in blocks if b['name']=='recipes handler');recipe_entry=recipe_block['networks'][0]
code=live[recipe_entry['segment'],recipe_entry['doc']]['values']['SCL Code']
pattern=r'"data"\.([a-z0-9_]+) := "recipesdb"\.recipes\[0\]\.([a-z0-9_]+);'
load_assignments=[dict(target='Data.'+a,field=b,source_span=[x.start(),x.end()],source_text=x.group()) for x in re.finditer(pattern,code,re.I) for a,b in [x.groups()]]
assert [(canon(a['target']),a['field']) for a in load_assignments]==[(canon(t),f) for f,t,_ in fields]
indexed=[]
for b in blocks:
 for entry in b['networks']:
  values=live[entry['segment'],entry['doc']]['values']
  for key in ['SCL Code','STL Code']:
   txt=values.get(key)
   if txt and (entry['doc']==401 or re.search(r'"data"\.(?:set_perc_bwf0[12]|set_perc_fr01|set_perc_vt01|psh0[12]_setpoint|tc0[13]_setpoint)\b',txt,re.I)):
    indexed.append(dict(block=b['name'],block_properties=b['properties'],segment=entry['segment'],id=entry['doc'],kind=key,text=txt,values=values,sha256=hashlib.sha256(txt.encode()).hexdigest(),status='exact_backup_index_text_not_current_compiled_source'))
writer_ids={u['network'] for u in trace if u['scope']=='Global' and any(canon(u['name'])==canon(t) for _,t,_ in fields) and u['role']=='write' and not u['legacy_simulation_block']}
selected=sorted(writer_ids|{402,403,404,405,1613,1723,1841,1621})
proofs=[native(i) for i in selected]
field_rows=[]
for f,target,hmi_name in fields:
 uses=[u for u in trace if u['scope']=='Global' and canon(u['name'])==canon(target)]
 others=[u for u in trace if canon(u['name'])==canon(target) and u['scope']!='Global']
 paths.update(u['file'] for u in uses+others)
 field_rows.append(dict(field=f,target=target,hmi=[r for r in hmi if r['HMI 태그']==hmi_name],assignment=next(x for x in load_assignments if x['field']==f),usages=uses,other_scope_usages=others,screen_mapping_verified=False,current_write_owner_verified=False))
control_names={'HMI_Index','Editor_Active_Recipe','Editor_Vis_SaveUndo','Editor_Vis_Modify','Editor_Vis_LoadRecipe','Editor_Load_Recipe','Editor_Save_Recipe','Editor_Modify_Recipe','Editor_Undo_Modification'}
controls=[r for r in hmi if r['HMI 태그'] in control_names]
# Literal source excerpts and positions preserve the exact source basis for each interpretation.
claims=[
 ('index_range','1…100 번호 검사', '#in_range := ("recipesdb".hmi_index >= 1 and "recipesdb".hmi_index <= 100);','조건값은 원본 색인의 검사 범위입니다. 배열 선언의 실제 상·하한을 증명하지 않습니다.'),
 ('early_array','범위 분기 전 배열 참조', '#differing := "recipesdb".recipes[0] <> "recipesdb".recipes["recipesdb".hmi_index];','범위 보정 분기 앞에 동적 배열 참조가 있습니다. 해당 임시변수는 이후 색인 텍스트에 다시 나오지 않습니다. 현재 컴파일·최적화·예외 처리는 확인 전입니다.'),
 ('selection','선택 번호 변경', 'if ("recipesdb".hmi_index <> "recipesdb".oldhmi_idx) and #in_range then','이어지는 구문은 저장본을 recipes[0]에 복사하고 modify_recipe/vis_saveundo를0, vis_modify/vis_loadrecipe를1로 씁니다. 편집 중 번호가 실제로 변경 가능한지는 HMI 이벤트 확인이 필요합니다.'),
 ('range_correction','범위 밖 번호 보정', 'elsif not #in_range then "recipesdb".hmi_index := 1; end_if;','번호를1로 보정합니다. #in_range는 이 구문 뒤 다시 계산되지 않습니다. 같은 호출 안의 버퍼 복사·불러오기 결과는 현재 원본에서 확인해야 합니다.'),
 ('edited','편집 상태', 'if ("recipesdb".recipes[0] <> "recipesdb".recipes["recipesdb".hmi_index]) and "recipesdb".modify_recipe then','버퍼와 저장본이 다르고 modify_recipe가 참인 분기에서 saveundo 표시1, modify/loadrecipe 표시0을 씁니다. 표시 변수만으로 화면 접근 제어가 보장되지는 않습니다.'),
 ('save','저장', 'if "recipesdb".vis_saveundo and "recipesdb".save_recipe then','recipes[0]을 선택 저장본에 복사합니다. 운전 Data 설정8개에 쓰는 경로는 뒤의 불러오기 분기입니다. save_recipe/modify_recipe는 이 분기에서0으로 씁니다.'),
 ('undo','취소', 'if "recipesdb".vis_saveundo and "recipesdb".undo_modification then','선택 저장본을 버퍼에 복사하고 undo_modification/modify_recipe를0으로 씁니다. 저장 if 다음에 별도의 if로 나열되며 앞선 저장은 vis_saveundo를0으로 변경합니다.'),
 ('load','운전값 적용', 'if ("recipesdb".recipes[0] = "recipesdb".recipes["recipesdb".hmi_index]) and "recipesdb".vis_loadrecipe and "recipesdb".load_recipe then','운전 Data 설정8개를 대입하고 active_recipe에hmi_index, load_recipe에0을 씁니다. 이 조건에는 #in_range가 직접 적혀 있지 않습니다. active_recipe 번호는 이후 다른 쓰기에 의한 설정 변경까지 증명하지 않습니다.'),
 ('last_index','선택 번호 기억', '"recipesdb".oldhmi_idx := "recipesdb".hmi_index;','마지막 구문에 선택 번호를 기록합니다. 저장 유지·전원 재기동 후 복원 근거는 아닙니다.')]
cla=[]
for key,title,excerpt,note in claims:
 start=code.index(excerpt);cla.append(dict(key=key,title=title,excerpt=excerpt,source_span=[start,start+len(excerpt)],interpretation=note,status='static_index_reading_not_execution'))
guidance=[
 ('saved_not_applied','저장했는데 운전값이 그대로임','save_recipe/버퍼/저장본 대조 → load_recipe/vis_loadrecipe/버퍼 동일 여부 → Data8개 값과 active_recipe 시각을 따로 기록합니다.','저장과 운전 적용은 별도 분기입니다. 저장 버튼이 자동 불러오기도 요청하는지는 화면 프로젝트 확인이 필요합니다.'),
 ('reverted','입력한 운전값이 되돌아감','HMI 실제 쓰기 멤버 → 레시피 불러오기 시각 → 자동 기동 단계 → FN01 온도 단계 → 클램프/건조 램프 → 현재 OB 호출을 대조합니다.','동일 Global 멤버의 LAD 쓰기와 SCL 색인 쓰기를 모두 봅니다. 표의 순서는 실제 OB 간 우선순위가 아닙니다.'),
 ('selection_loss','편집 중 레시피 번호 변경','hmi_index/oldhmi_idx/modify_recipe와 recipes[0]/선택 저장본을 같은 시각에 기록합니다.','번호 변경 분기가 버퍼를 덮어쓰는 후보입니다. 실제 변경 가능 여부와 미저장 경고는 현재 HMI에서 확인합니다.'),
 ('load_blocked','불러오기가 반응하지 않음','버퍼와 선택 저장본 전체 구조 동일 여부, vis_loadrecipe, load_recipe, 선택번호 범위와 버튼 이벤트를 확인합니다.','자료형·문자열/구조 비교 가능 여부와 실제 DB배치/쓰기 품질은 현재 TIA/HMI에서 확인합니다.'),
 ('requests','저장·취소·불러오기 요청이 남음','한 요청씩 화면 이벤트·요청/소비·표시 상태·버퍼/저장본/Data변화를 기록합니다. 동시에 들어온 요청은 현재 소스 순서를 대조합니다.','선택번호 변경 분기에서 세 요청비트를 일괄 해제하는 구문은 이 색인에 없습니다. 요청 펄스/래치 정책은 화면 프로젝트 확인 전입니다.'),
 ('invalid_index','레시피 번호가 범위 밖이거나 CPU 진단 발생','현재 배열 선언의 실제 범위, 동적 참조 전 가드, 현재 컴파일·CPU 진단·HMI입력 제한을 확인합니다.','범위 보호 분기 전 #differing 배열 참조와 별도 load조건을 검토합니다. 실제 설비에서 잘못된 번호를 주입하지 않습니다.'),
 ('power_return','전원 복귀 후 자동·닫힘 상태가 달라짐','startup only 호출/현재 초기화·Retain·DB시작값 → 운전 플래그 → 실제 응답·리미트와 재기동 허가를 분리 기록합니다.','메모리 닫힘 플래그 Set은 밸브가 물리적으로 닫혔다는 근거가 아닙니다. DB2/DB3초기화 대상은 색인 표기와 원본 미해석 핀을 구분합니다.'),
 ('active_mismatch','활성 레시피 번호와 운전 설정값이 다름','active_recipe/선택번호/불러오기 시각과 현재 Data8개 값의 다른 쓰기를 비교합니다.','active_recipe만 표시하면 운전값이 저장본과 계속 같다는 결론을 내릴 수 없습니다.')]
startup=[dict(id=i,block=next(b for b in blocks if b['name']=='startup only')['properties'],values=live['_7ev',i]['values'],native_available=i in selected,status='index_text_and_native_refs_separated') for i in range(401,406)]
profiles=[dict(key=p['key'],name=p['name'],plc_id=p['plc_id'],identity_verified=False,scope='common_settings_and_restart_context_not_equipment_ownership') for p in priority]
counts=dict(recipe_load_fields=len(field_rows),hmi_control_tags=len(controls),hmi_editor_tags=sum(len(x['hmi']) for x in field_rows),native_networks=len(proofs),indexed_text_records=len(indexed),recipe_claims=len(cla),symptoms=len(guidance),priority_profiles=len(profiles))
result=dict(date='2026-10-08',scope='Recipe index text, native setting writers and restart manual; not executed SCL, current DB layout or operating instruction',counts=counts,recipe_source=dict(segment=recipe_entry['segment'],id=recipe_entry['doc'],block='recipes handler',text=code,sha256=hashlib.sha256(code.encode()).hexdigest()),claims=cla,load_fields=field_rows,hmi_controls=controls,indexed_texts=indexed,startup=startup,native_ids=selected,native=proofs,writer_network_ids=sorted(writer_ids),profiles=profiles,guidance=[dict(key=k,symptom=s,steps=a,limit=b) for k,s,a,b in guidance],sources={p:sha(p) for p in sorted(paths)},field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun')
(ROOT/'registers/recipe-settings.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
def link(path,label):return '<a href="'+e(path)+'">'+e(label)+'</a>'
def netlink(i):return link('networks/network-'+str(i)+'.html','원본 '+str(i))
def table(headers,rows):return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
body='<h1>레시피·설정값·초기화 확인 매뉴얼</h1><p>편집 버퍼 → 저장본 → 운전 적용 → 다른 쓰기 → 출력/응답을 따로 추적합니다.</p><div class="notice info">백업 SCL/STL 색인과 원본 LAD를 구분합니다. 줄바꿈·주석이 평탄화된 색인은 실행 가능한 SCL 소스가 아니며 현재 TIA 컴파일을 증명하지 않습니다. DB26 태그와 recipesdb 멤버의 절대 주소·현재 화면 이벤트는 확인 전입니다. PLC 변경·실제수리 완료0건 · 시뮬레이터 작성/수정/행동 시험 중지.</div>'
body+='<nav class="inline-actions">'+''.join(link('#'+k,t) for k,t in [('repair','증상별 진단'),('recipe','레시피 분기'),('fields','운전 설정8개'),('writers','다른 쓰기'),('startup','전원 복귀'),('hmi','HMI 설정'),('native','원본 배선'),('profiles','우선23개 작업지')])+link('hmi-transfer.html','HMI 전체 확인')+'</nav>'
body+='<h2 id="repair">증상별 확인 순서</h2>'+table(['증상','확인 순서','범위/한계'],[[e(s),e(a),e(b)] for _,s,a,b in guidance])
body+='<h2 id="recipe">레시피 편집·저장·취소·불러오기 분기</h2><p>색인 읽기: recipes[0]은 편집/전달 버퍼, recipes[hmi_index]는 선택 저장본입니다. 저장은 버퍼→저장본, 취소는 저장본→버퍼, 불러오기는 버퍼→Data8개 설정입니다. 실제 배열 선언·자료형·Retain은 확인 전입니다.</p>'+table(['원본 위치','구문','대조 해석'],[['<span id="claim-'+x['key']+'">'+e(x['title'])+'</span> · 문자 '+e(x['source_span']),'<code>'+e(x['excerpt'])+'</code>',e(x['interpretation'])] for x in cla])
body+='<details id="index-364"><summary>364 · recipes handler · 백업 SCL 색인 전체</summary><p>아래 원문은 주석과 줄바꿈이 평탄화된 색인 텍스트입니다. 재구성 코드로 실행하지 않습니다. SHA256 '+e(result['recipe_source']['sha256'])+'</p><pre>'+e(code)+'</pre></details>'
body+='<h2 id="fields">불러오기에서 쓰는 운전 설정8개</h2><p>태그 이름은 화면 편집 항목의 참고입니다. HMI DB26 절대 주소와 recipesdb/운전Data 멤버를 이름만으로 같은 주소로 합치지 않습니다.</p>'+table(['레시피 필드','SCL 색인의 대상','기존 편집 태그','LAD 쓰기·읽기'],[['<span id="field-'+x['field']+'">'+e(x['field'])+'</span>',e(x['target'])+'<br><code>'+e(x['assignment']['source_text'])+'</code>','<br>'.join(link('hmi-transfer.html#tag-'+r['태그 내부 ID'],r['HMI 태그'])+' '+e(r['설정 주소']) for r in x['hmi']),' · '.join(netlink(i) for i in sorted({u['network'] for u in x['usages']})) or 'LAD색인 참조 없음 · SCL/현재소스 확인'] for x in field_rows])
body+='<h2 id="writers">설정값의 다른 쓰기와 호출 경계</h2><p>레시피 SCL364의 대입은 LAD핀 색인에 들어 있지 않습니다. 아래는 정확한 Global 멤버의 LAD핀 목록이며 Local 동명이름은 별도로 보존합니다. 실행 순서·마지막 쓰기·현재 소유권을 확정하지 않습니다.</p>'
for x in field_rows:
 body+='<details id="writers-'+x['field']+'"><summary>'+e(x['target'])+' · LAD '+str(len(x['usages']))+'핀</summary>'+table(['원본','핀','역할·블록'],[[netlink(u['network']),e(u['part']+'.'+str(u['pin'])),e(u['role']+' · '+u['block'])+(' · 기존 simulation 블록의 정적 참조' if u['legacy_simulation_block'] else '')] for u in x['usages']])+'</details>'
body+='<h3>되돌림을 설명할 수 있는 원본 경로</h3>'+table(['근거','확인 내용'],[[netlink(1843)+' / '+netlink(1844),'자동 기동 단계에서 FR01=25, VT01=35, VT02=75/80 및 TC01=850/TC03=500 쓰기가 있습니다. 조건·OFF접점과 실제 단계 경과를 원본 배선에서 확인합니다.'],[netlink(1845),'FN01 온도 구간별 설정과 T#10s 타이머 뒤 VT01 쓰기5개가 있습니다. 실제 호출 주기·현재 온도/설정·중첩 구간을 확인합니다.'],[netlink(1684)+' / '+netlink(1685),'FR01/VT01 <5→5, >100→100으로 멤버 자체를 쓰는 원본 경로가 있습니다. 입력 제한과 출력 배율은 구분합니다.'],[netlink(8),'TC03_SETPOINT <200 조건에서200을 쓰는 원본이 있습니다. 운전 허용 설정 승인은 별도입니다.'],[netlink(1679)+' / '+netlink(1680)+' / '+netlink(1682),'BWF01/02의 설정과 생산량 연동 및 제한 쓰기를 원본으로 대조합니다.'],[netlink(1875)+' / '+netlink(1876)+' / '+netlink(1877),'건조 단계의 TC01_SETPOINT 쓰기도 별도입니다. 현재 건조 모드·허가·시간 조건을 확인합니다.'],[netlink(1613)+' / '+netlink(1723)+' / '+netlink(1621),'Recipes Handler, Auto start motors, Analog output conversion 호출의 원본 en/eno 배선을 보존합니다. 서로 다른 OB 호출 사이의 마지막 쓰기 순서는 이 목록으로 증명되지 않습니다.']])
body+='<h2 id="startup">전원 복귀·기동 초기화</h2><p>startup only 블록은 색인 속성 Event class=startup입니다. 실제 CPU시작·Warm/Cold/Retain·DB초기값·호출 조건은 현재 TIA에서 확인합니다.</p>'+table(['원본','색인에 기록된 내용','확인 경계'],[[link('#index-401','401 · 특별 플래그'),'STL 색인: set s "on" clr s "off"','STL 상태·실제 값은 현재 소스로 확인. ON/OFF를 상수로 치환하지 않습니다.'],[netlink(402),'DB2.DBW0,2,4,6,8,10,12,14에 INT#0을 쓰는 LADFBD 색인','원본402 Move의 ORef는 이름 미해석입니다. 절대 주소를 원본 핀에 임의 배정하지 않습니다. DB2 전체/모든 운전값 초기화라고 확대하지 않습니다.'],[netlink(403),'DB3.DBW0,2,4,6,8,10,12,14,16에 INT#0을 쓰는 LADFBD 색인','원본403 Move ORef도 미해석입니다. 현장 알람 원인 해제·안전 복구 완료를 뜻하지 않습니다.'],[netlink(404),'MV01~06_Auto, FN_04_AUTO에 SCoil','자동 모드 플래그와 최종 출력·재기동 허가는 별도입니다. 각 ON접점/배선을 확인합니다.'],[netlink(405),'PV01 A/B, PV02 A/B, PV03 닫힘 메모리에 SCoil','닫힘 메모리 설정은 실물 닫힘·리미트 확인 근거가 아닙니다.']])
for x in startup:
 body+='<details id="index-'+str(x['id'])+'"><summary>'+str(x['id'])+' · startup only · 원본 색인 값</summary><pre>'+e(x['values'].get('STL Code',''))+'</pre><pre>'+e(json.dumps(x['values'],ensure_ascii=False,indent=2))+'</pre></details>'
body+='<h2 id="hmi">레시피 제어·활성번호·표시 태그</h2><p>Access Name은 접속 이름이며 버튼 이벤트·쓰기 권한·현재 DB 멤버 일치를 증명하지 않습니다.</p>'+table(['태그','설정 주소','Access Name','근거'],[[e(r['HMI 태그']),e(r['설정 주소']),e(r['Access Name']),link('hmi-transfer.html#tag-'+r['태그 내부 ID'],'원본 CSV 태그')] for r in controls])
body+='<h2 id="indexed">설정값을 읽는 STL/SCL 색인</h2>'
for x in indexed:
 if x['id'] in [364,401]:continue
 body+='<details id="index-'+str(x['id'])+'"><summary>'+e(str(x['id'])+' · '+x['block']+' · '+x['kind'])+'</summary><p>해시 '+e(x['sha256'])+' · 현재 컴파일 확인 전</p><pre>'+e(x['text'])+'</pre></details>'
body+='<h2 id="native">원본 LAD 핀·형식·반전·전체 배선</h2>'
for p in proofs:
 body+='<details id="native-'+str(p['id'])+'"><summary>'+e(str(p['id'])+' · '+p['block']+' · '+p['title'])+'</summary><p>'+netlink(p['id'])+' · '+link(p['file'],'원본 XML')+' · '+e(p['sha256'])+'</p>'
 rows=[]
 for n in p['nodes']:
  for pin in n['pins']:
   refs=' / '.join('ORef '+r['oref']+' · '+(r['name'] or '[미해석·RefId 없음]') for r in pin['references']);peers=' / '.join(q['kind']+' '+str(q['uid'])+'.'+str(q['pin']) for q in pin['peers'])
   rows.append([e(n['uid']+' · '+str(n['gate'] or n['kind'])),e(str(n['tree']['attributes'])+' / '+str(n['tree']['children'])+' / '+str(n['declarations'])+' / '+str(n['children_declarations'])),e(pin['pin']),e(refs or peers),link('#wire-'+str(p['id'])+'-'+pin['wire'],pin['wire'])])
 body+=table(['노드','반전·형식·선언','핀','연결','Wire'],rows)+table(['Wire','전체 연결'],[['<span id="wire-'+str(p['id'])+'-'+w['uid']+'">'+e(w['uid'])+'</span>',e(' / '.join(x['kind']+' '+str(x['uid'])+'.'+str(x['pin']) for x in w['ends']))] for w in p['wires']])+'</details>'
body+='<h2 id="profiles">우선23개 공통 설정·재기동 확인 작업지</h2><p>공통 검토 경로입니다. 각 설비가 모든 레시피 필드의 소유자라고 배정하지 않습니다. 현재 시안↔실물↔PLC 동일성은 확인 전입니다.</p>'
for p in profiles:
 body+='<details id="profile-'+p['key']+'"><summary>'+e(p['key']+' · '+p['name'])+'</summary><p>PLC 참고 '+e(p['plc_id'] or '대응 미확정')+' · 직접 레시피 소유 관계는 현재 원본/현장 확인 필요</p>'+link('#repair','설정·재기동 증상별 확인')+' · '+link('hmi-transfer.html#profile-'+p['key'],'이 설비의 기존 HMI 참조')+' · '+link('index.html#view=repair-record&equipment='+p['key']+'&scope=priority','이 설비 수리 기록')+'</details>'
body+='<h2 id="checks">추가 확인할 근거</h2><p>현재 Recipes Handler 소스·DB 배열 상하한/구조형·Retain/절대 멤버 주소·버튼 이벤트·요청 소비 정책·OB 호출 순서/주기·설정 소유자·기동 초기화 범위와 실제 응답을 확인합니다. 기존 불일치18건/확인 대장1060건/설계시험577건은 확인 완료로 바꾸지 않았습니다.</p>'+link('registers/recipe-settings.json','전체 근거·필드·원본·해시 JSON')
body+='''<script>function revealEvidence(){let id;try{id=decodeURIComponent(location.hash.slice(1));}catch(_){return;}const target=document.getElementById(id);if(!target)return;let parent=target;while(parent){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}target.scrollIntoView({block:'start'});}addEventListener('hashchange',revealEvidence);revealEvidence();</script>'''
(ROOT/'recipe-settings.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>레시피·설정값·초기화 확인</title><link rel="stylesheet" href="assets/all-in-one.css"><style>main{max-width:1320px;margin:auto;padding:24px}td{vertical-align:top;overflow-wrap:anywhere}h2{scroll-margin-top:20px}details{margin:12px 0}summary{cursor:pointer;font-weight:600}pre{white-space:pre-wrap;overflow-wrap:anywhere}.inline-actions{flex-wrap:wrap}</style></head><body><main>'+body+'</main></body></html>')
print(json.dumps(dict(status='built',**counts,writer_networks=len(writer_ids),source_hashes=len(paths),simulator_development='stopped_by_user'),ensure_ascii=False))
