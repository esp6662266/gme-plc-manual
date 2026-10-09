"""Read-only impact worksheets for the six existing improvement candidates.

No control evaluation, simulator authoring, new test results or PLC changes.
Exact declaration scope and pin identities are retained from native-source trace.
"""
from pathlib import Path
from collections import Counter
import csv, hashlib, html, json, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
review=json.loads((ROOT/'registers/improvement-review.json').read_text())
trace=json.loads((ROOT/'registers/signal-trace.json').read_text())
native=json.loads((ROOT/'registers/program-model.json').read_text())
source_map={n['document_id']:n for n in json.loads((ROOT/'sources/decoded-original/network-map.json').read_text())}
declarations=json.loads((ROOT/'sources/decoded-original/identifier-declarations.json').read_text())
repair=json.loads((ROOT/'registers/repair-decision.json').read_text())
symbols=list(csv.DictReader((ROOT/'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
nets={n['id']:n for n in native['networks']}
canon=lambda s:str(s).replace('"','').casefold()
local=lambda x:x.tag.rsplit('}',1)[-1]
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
e=lambda s:html.escape(str(s))
out=ROOT/'improvement-guides';out.mkdir(exist_ok=True)

# Reviewed focus names. Comparator signals stay separate from the seed's operands.
focus={
 'IMP-01':['Tag_66','Memo_M25_Running','FP_M25_Run','Inputs.FN03 Run','Allarm.FN_03_FAULT'],
 'IMP-02':['ON','Open MV06','Close MV06','Flag.MV06_Auto','Flag.MV06_Open','Flag.MV06_Close'],
 'IMP-03':['Allarm.Maintenance_ON','Flag.Maintenance_ON','Flag.M_MC_04','Inputs.VS01 run','Start MC04'],
 'IMP-04':['Allarm.MBVA01_FAULT','Tag_67','Flag.M_FN_06','Start FN06','Inputs.FEEDBACKMOTOR FN-06','Inputs.RD01 run'],
 'IMP-05':['Close MV03 for Burner Startup','Inputs.MV03 Close','WorkData.BR01_State','Enable start burner','Enable start burner(1)'],
 'IMP-06':['Data.SET_PERC_FN04','FN04_SP','Flag.M_FN_04','Start FN04','Stop_Fan_FN04'],
}
plans={
 'IMP-01':dict(
  baseline='Tag_66의 두 SD와 펄스 기억 FP_M25_Run, Memo_M25_Running을 함께 보존합니다. 두 SD의 같은 RefId는 같은 타이머 참조의 근거이며 실제 실행 결과는 별도 확인 대상입니다.',
  documentation='두 SD의 모드/조건·펄스/기억·시간 설정과 현재 호출 결과를 문서에 나눠 표시합니다. 의미 확인 전에는 하나를 중복이라고 삭제하지 않습니다.',
  plc_review='현재 실행 의미와 각 분기의 필요성이 확인된 경우에만 타이머를 구동하는 주체를 명확히 하는 변경안을 검토합니다. 하나로 합치거나 타이머 형식을 바꾸면 시작·유지·재시작·고장 시점이 달라질 수 있습니다.',
  preserve='35초 설정·운전 응답·펄스 기억·기존 고장 래치와 리셋을 각각 보존할 범위로 검토합니다.',
  evidence=['현재 TIA의 두 SD 표시·타이머 주소/형식·각 입력 조건·호출과 온라인 경과값 근거','FN03 soft starter 응답과 최초 알람·운전 요청의 같은 시각 기록','현재 프로그램과 백업의 블록 비교·유지 설정·펄스 기억 초기화 근거'],
  criteria=['두 SD가 각각 어떤 조건에서 타이머를 구동하는지 근거로 설명할 수 있어야 합니다.','기억/펄스/운전 응답과 최초 고장 시점의 관계를 확인해야 변경 필요성을 판단할 수 있습니다.','검토안의 시작·리셋·재기동 의미를 현재 로직과 대조한 기록이 없으면 PLC 변경안은 미확정으로 남깁니다.']),
 'IMP-02':dict(
  baseline='ON을 상수로 치환하지 않고 MV06 열기·닫기의 반전 접점과 요청·PID/펄스·리미트·출력의 쓰기를 구분합니다.',
  documentation='현재 활성 블록·모드와 실제 ON 값, 열기/닫기 출력의 모든 쓰기 위치를 설명합니다. 정적 NOT ON만으로 오배선·프로그램 오류를 확정하지 않습니다.',
  plc_review='활성 범위와 원래 의도가 확인된 경우에만 미사용 분기의 정리 또는 모드 허가 표현을 검토합니다. 공유 ON 값을 바꾸는 변경은 전체 참조 범위의 영향 검토가 필요합니다.',
  preserve='방향 상호 조건·끝단·수동/자동 요청·PID 펄스·기존 고장 감시와 현장 접촉기 인터록의 범위를 보존합니다.',
  evidence=['ON의 현재 값·초기화·복원 LAD 밖 쓰기 및 현재 호출 근거','1711의 반전 접점과 열기/닫기 출력 사용처, 물리 출력/리미트 대응 근거','MV06 현재 계측 방식·단자·회로 및 모드별 승인 운전 자료'],
  criteria=['반전 접점의 원본 표시와 현재 TIA 표시가 일치하는지 먼저 확인합니다.','어느 경로가 활성인지와 실제 출력의 쓰기 주체를 확인하기 전에는 분기를 제거하지 않습니다.','공유 ON의 참조 영향과 장치별 방향/허가 의미를 구분한 검토가 필요합니다.']),
 'IMP-03':dict(
  baseline='Allarm.Maintenance_ON과 Flag.Maintenance_ON은 서로 다른 이름 공간의 신호로 유지합니다. 동일 의미·동일 주소는 확인 전입니다.',
  documentation='두 신호의 선언·모드 전달·HMI 설명을 각각 표시하고 MC04의 VS01 응답 연동을 설명합니다. 이름이 비슷하다는 이유로 같은 값으로 취급하지 않습니다.',
  plc_review='두 신호의 실제 의미와 전달 주체가 확인된 후에만 명칭·별칭 또는 유지보수 허가 정책의 정리를 검토합니다. DB 피연산자 치환은 별도 영향 대조가 필요한 후보입니다.',
  preserve='MC04 요청 해제·VS01 연동·다른 설비에서 사용하는 유지보수 조건·DB/HMI 참조를 보존할 범위로 검토합니다.',
  evidence=['두 DB 선언의 주소·자료형·현재 값·HMI/외부 쓰기와 유지 설정 근거','MC04 1941, 비교 신호의 다른 사용 위치와 현재 호출 근거','승인된 유지보수 모드의 운전 허가·정지 정책과 현장 해석'],
  criteria=['두 신호의 의미와 주소를 각각 확인해야 동일성 또는 차이를 판단할 수 있습니다.','VS01 미운전과 MC04 요청 해제의 관계를 원본 조건과 현재 자료로 설명해야 합니다.','다른 설비의 모드 허가에 대한 영향을 확인하지 않은 전역 치환은 검토안으로 채택하지 않습니다.']),
 'IMP-04':dict(
  baseline='Allarm.MBVA01_FAULT의 원본 Set/Reset과 FN06 요청 해제, RD01 응답을 별도로 보존합니다. 태그명만으로 과거 실물 장치를 확정하지 않습니다.',
  documentation='원본 이름·현재 알람 문구·확인된 실물 대응을 병기하고 최초 원인과 연동 정지를 구분합니다. 별칭의 의미도 근거 확인 후 표시합니다.',
  plc_review='과거 명칭/별칭 관계가 확인된 경우에만 알람 표시 또는 심볼 명칭 정리를 검토합니다. 이름을 바꾸면 HMI·외부 기록·정비 이력의 참조가 달라질 수 있습니다.',
  preserve='1802 감시와 1955 요청 해제·RD01 연동·시험 비트·리셋·기존 이력의 원본 태그를 보존할 범위로 검토합니다.',
  evidence=['Allarm.MBVA01_FAULT의 선언·1802 Set/Reset·1955 읽기 및 HMI 문구 근거','FN06 명판/회로/실물 ID와 RD01 연동, 최초 알람·응답 기록','현재 유지 설정·외부 알람 수집·관련 정비 이력의 참조 근거'],
  criteria=['실물 대응이 확인되기 전에는 MBVA01이라는 이름을 다른 설비 ID로 바꾸지 않습니다.','감시의 원인 입력과 요청 해제/연동 정지를 각각 설명할 수 있어야 합니다.','명칭 검토 시 기존 기록을 찾을 수 있는 원본 이름·별칭 연결과 참조 누락 여부를 확인합니다.']),
 'IMP-05':dict(
  baseline='1868의 서로 다른 MV03 닫힘 접점·Set 두 경로·BR01 상태와 두 버너 허가 주소를 구분합니다. 한 정적 경로의 충돌이 전체 요청이 발생하지 않는다는 뜻은 아닙니다.',
  documentation='Part 28/1654/1670의 같은 원시 이름·RefId와 반전 표시, Part1306/1669의 다른 Set 경로 및 상태7을 원본 위치와 함께 설명합니다.',
  plc_review='현재 TIA 표시·실제 활성 쓰기 경로·제작사 버너 순서가 확인된 이후에만 미도달 경로 정리 또는 의도 표현을 검토합니다. 버너 전용 제어기의 허가 정책은 자료 확인 대상입니다.',
  preserve='별도 상태7 경로·MV03 실제 위치/허가·버너 전용 제어기 인터페이스와 기존 청소/기동 요청의 범위를 보존합니다.',
  evidence=['1868 피연산자 UID/RID·반전 접점·Set 배선과 현재 TIA 표시 근거','BR01 상태·닫힘/열림 응답·요청의 다른 쓰기 및 현재 호출 근거','버너 전용010-390 상세 회로·승인 운전/복구 순서와 연동 근거'],
  criteria=['하나의 충돌 경로와 별도 Set 경로를 분리해 현재 활성 여부를 확인합니다.','내부 닫힘 요청·처리 응답·물리 위치·외부 버너 허가를 구분한 근거가 필요합니다.','버너 전용 허가 자료가 없으면 해당 정책을 임의로 변경하는 검토안은 확정하지 않습니다.']),
 'IMP-06':dict(
  baseline='설정 제한 쓰기1689·설정0 읽기1965·Filter의 다른 쓰기와 Local Stop_Fan_FN04를 분리합니다. 원본 main 배치는 실제 전체 실행·도달 여부의 확인 근거 중 하나입니다.',
  documentation='운전 설정의 범위·정지 요청·속도 출력 변환을 구분해 설명하고 모든 쓰기 및 main의 블록 배치를 함께 표시합니다. 설정0 조건의 도달 여부를 단독 네트워크로 판단하지 않습니다.',
  plc_review='정지 요청과 운전 설정의 실제 역할 및 제작사 최소값 정책이 확인된 후에만 두 역할을 분리하거나 허가 표현을 정리하는 변경안을 검토합니다. 설정값0을 임의로 허용하거나 최소값을 바꾸지 않습니다.',
  preserve='기존 범위 제한·아날로그 출력 스케일·알람/온도 정지·Local Stop_Fan_FN04·HMI/자동/Filter 요청과 실제 운전 허가의 범위를 보존합니다.',
  evidence=['1689·1900·1965와 HMI/외부의 동일 설정 쓰기·현재 호출 조건·현재 값 근거','main 네트워크9 Motors 1/Filter와 네트워크10 Analog output conversion, 인터럽트/ENO/외부 쓰기의 현재 실행 근거','공통 인버터59AS1 AI1/최소 운전 기준·M31/M36 두 모터·승인 정지 절차 근거'],
  criteria=['원시 설정·제한 이후 값·아날로그 출력·정지 요청의 역할을 각각 설명할 수 있어야 합니다.','main의 원본 배치만으로 모든 스캔의 최종 값을 확정하지 않고 호출·외부/주기 쓰기와 현재 프로그램을 대조합니다.','두 모터/공통 인버터의 허가·속도·알람 의미가 확인되어야 설정/정지 정책의 변경 필요성을 판단할 수 있습니다.']),
}

def expression(v):
    op=v.get('op')
    if op=='const':return str(v.get('literal',v.get('value')))
    if op=='read':return v['name']
    if op=='unknown':return '[미확인: '+v['reason']+']'
    if op=='not':return 'NOT ('+expression(v['arg'])+')'
    if op in ('and','or'):return '('+(' AND ' if op=='and' else ' OR ').join(expression(x) for x in v['args'])+')'
    return json.dumps(v,ensure_ascii=False)

def proof(network,selected):
    n=nets[network];root=ET.parse(ROOT/n['file']).getroot()
    parts={p.get('UId'):p for p in root.iter() if local(p)=='Part'}
    orefs={p.get('UId'):p.get('RefId') for p in root.iter() if local(p)=='ORef'}
    records=[]
    for uid in sorted(selected,key=int):
        p=parts[uid];connections=[]
        for wire in root.iter():
            if local(wire)!='Wire' or not any(local(x)=='PCon' and x.get('UId')==uid for x in wire):continue
            connections.append(dict(wire=wire.get('UId'),endpoints=[dict(kind=local(x),uid=x.get('UId'),pin=x.get('PinName'),
                name=n['refs'].get(x.get('UId'),{}).get('name') if local(x)=='OCon' else None,
                ref_id=orefs.get(x.get('UId')) if local(x)=='OCon' else None) for x in wire]))
        records.append(dict(uid=uid,gate=p.get('Gate'),negated_pins=[x.get('PinName') for x in p if local(x)=='Negated'],connections=connections))
    return dict(network=network,block=n['block'],source_network_index=n['index'],file=n['file'],sha256=sha(n['file']),parts=records)

items=[]
source_paths={'registers/improvement-review.json','registers/signal-trace.json','registers/program-model.json','registers/repair-decision.json','registers/plc-symbols.csv','sources/decoded-original/network-map.json','sources/decoded-original/identifier-declarations.json'}
for issue in review['items']:
    signals=[]
    for name in focus[issue['id']]:
        scope='Local' if name=='Stop_Fan_FN04' else 'Global'
        block='motors 1' if scope=='Local' else None
        uses=[r for r in trace['usages'] if r['scope']==scope and canon(r['name'])==canon(name) and (not block or r['block']==block)]
        others=[r for r in trace['usages'] if canon(r['name'])==canon(name) and not (r['scope']==scope and (not block or r['block']==block))]
        assert uses,(issue['id'],name)
        seed_uses=[r for r in uses if r['network'] in issue['networks']]
        signals.append(dict(name=name,scope=scope,block=block,identity=uses[0]['identity'],
            context='비교 신호 · 해당 후보 네트워크의 피연산자는 아님' if not seed_uses else '후보 네트워크의 직접 참조',
            shared_program_signal=name=='ON',seed_uses=seed_uses,usages=uses,other_scope_usages=others,
            counts=dict(Counter(r['role'] for r in uses)),
            symbol_rows=[s for s in symbols if canon(s['원본 심볼'])==canon(name)] if scope=='Global' else []))
        source_paths.update(r['file'] for r in uses+others)
        source_paths.update(d['file'] for r in uses+others for d in r['declarations'])
    assert all(s['seed_uses'] or s['name']=='Flag.Maintenance_ON' for s in signals)
    owners={nets[n]['block'] for n in issue['networks']}
    owners.update(r['block'] for s in signals if not s['shared_program_signal'] for r in s['usages'])
    known=set(map(canon,owners));calls=[]
    while True:
        found=[c for c in native['calls'] if c['callee'] and canon(c['callee']) in known]
        expanded=known|{canon(c['caller']) for c in found}
        if expanded==known:calls=found;break
        known=expanded
    call_rows=[]
    for c in calls:
        n=nets[c['network']]
        tree=ET.parse(ROOT/n['file']).getroot()
        cref=next(x for x in tree.iter() if local(x)=='CRef' and x.get('UId')==c['uid'])
        code=next(x for x in cref if local(x)=='CodeBlock')
        assert code.get('UId')==c['block_uid']
        decl=[d for d in declarations if d['uid']==code.get('UId') and d['rid']==code.get('RefId') and d['nid']==source_map[n['id']]['inferred_original_nid'] and d['name']==c['callee']]
        assert decl,(c['network'],c['uid'],c['callee'])
        call_rows.append(dict(**c,source_file=n['file'],source_network_index=n['index'],
            cref_ref_id=cref.get('RefId'),block_ref_id=code.get('RefId'),native_declarations=decl))
        source_paths.update('sources/decoded-original/'+d['file'] for d in decl)
    call_rows.sort(key=lambda c:(c['caller'],c['source_network_index'],int(c['uid'])))
    source_paths.update(c['source_file'] for c in call_rows)
    seed_proof=[proof(n,{r['part'] for s in signals for r in s['seed_uses'] if r['network']==n}) for n in issue['networks']]
    primary=issue['equipment'].split('·')
    refs={canon(s['name']) for s in signals if not s['shared_program_signal'] and s['scope']=='Global'}
    related=[r['key'] for r in repair['records'] if r['plc_id'] and r['plc_id'] not in primary and any(canon(b['name']) in refs for b in r['bindings'])]
    priority=[r['key'] for r in repair['records'] if r['plc_id'] in primary]
    items.append(dict(id=issue['id'],original=issue,signals=signals,seed_evidence=seed_proof,
        direct_calls_and_known_ancestors=call_rows,known_source_blocks=sorted(owners),
        unresolved_calls=[c for c in native['calls'] if c['caller'] in owners and not c['callee']],
        primary_priority_keys=priority,reference_related_priority_keys=related,
        review_plan=plans[issue['id']],guide='improvement-guides/'+issue['id']+'.html',
        field_verified=False,tia_verified=False,changes_applied=0,simulator_behavior_tests='not_rerun'))

register=dict(date='2026-10-08',scope='Static source impact and conditional change review; no new control logic or execution',
    items=items,sources={p:sha(p) for p in sorted(source_paths)},
    changes_applied=0,field_verified=0,tia_verified=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun')
(ROOT/'registers/improvement-impact.json').write_text(json.dumps(register,ensure_ascii=False,indent=2)+'\n')

def link(label,path):
    assert (ROOT/path.split('#')[0]).is_file(),path
    return '<a href="../'+e(path)+'">'+e(label)+'</a>'
def table(headers,rows):
    return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def usage_table(usages):
    labels={'read':'읽기','write':'쓰기','pending':'방향 미확정'}
    return table(['방향·블록·선언 범위','원본 위치','핀·선언 근거'],[[e(labels[r['role']]+' / '+r['block']+' / '+r['scope']+(' · 백업 기존 simulation' if r['legacy_simulation_block'] else '')),link(str(r['network'])+' / '+r['title'],'networks/network-'+str(r['network'])+'.html'),e('Part '+r['part']+' '+r['gate']+' / '+r['pin']+' / ORef '+r['oref']+' / Wire '+r['wire']+' · '+r['role_basis'])+'<br>'+', '.join(link(d['kind']+' / '+d['scope']+' / AK '+str(d['access_kind'] or '미표기'),d['file']) for d in r['declarations'])] for r in usages])
for item in items:
    issue=item['original'];plan=item['review_plan']
    body='<h1>'+e(issue['id']+' · '+issue['equipment']+' 개선 영향·확인 작업지')+'</h1><div class="notice">원본 구조의 검토 후보입니다. 현재 오류·변경 필요성·TIA 실행·실물 대응은 확인 전이며 PLC 변경0건입니다. 시뮬레이터 작성·수정·행동 시험은 중지 상태입니다.</div>'
    body+='<nav class="inline-actions">'+link('개선 후보 전체 목록','improvement-review.html')+' '+link('통합 근거 검토','evidence-review.html#review-improvement-'+item['id'])+' '+link('정적 근거 JSON','registers/improvement-impact.json')+'</nav>'
    body+='<h2>1. 관찰과 판단 경계</h2><p>'+e(issue['observation'])+'</p><p><strong>예상 영향</strong> · '+e(issue['impact'])+'</p><p><strong>원본 상태</strong> · '+e(issue['status'])+'</p>'
    body+='<h2>2. 변경 검토안과 보존 범위</h2>'+table(['구분','검토 내용'],[[e('현재 보존할 구조'),e(plan['baseline'])],[e('자료·설명 보완안'),e(plan['documentation'])],[e('근거 확인 후 PLC 변경 검토안'),e(plan['plc_review'])],[e('보존 영향'),e(plan['preserve'])]])
    body+='<h2>3. 판단 전에 필요한 근거</h2><ul>'+''.join('<li>'+e(v)+'</li>' for v in plan['evidence'])+'</ul><h3>변경 필요성의 판단 기준</h3><ol>'+''.join('<li>'+e(v)+'</li>' for v in plan['criteria'])+'</ol><p class="muted">새 시험 실행 결과를 만든 것이 아닙니다. 기존 시험 설계577건과 현장 확인 대장1,060건의 상태는 그대로입니다. PLC 수정·적용은 별도 요청 범위입니다.</p>'
    body+='<h2 id="calls">4. 알려진 호출과 원본 배치</h2><p>직접 호출과 이름이 해석된 상위 호출을 연결합니다. EN/ENO·인터럽트·외부 쓰기·현재 CPU의 실행은 확인 전입니다. 네트워크 번호는 원본 블록 안의 배치 위치이며 같은 네트워크의 UID 순서는 실행 순서를 뜻하지 않습니다. 미해석 호출·다른 언어·현재 변경분은 이 목록 밖에 있을 수 있습니다.</p>'
    body+=table(['호출 주체 → 블록','원본 블록 내 위치','호출 UID·조건·원본 선언'],[[e(c['caller']+' → '+c['callee']+(' · 백업 기존 블록(원본 참조)' if canon(c['callee'])=='simulation' else '')),link('네트워크 '+str(c['source_network_index'])+' / 문서 '+str(c['network']),'networks/network-'+str(c['network'])+'.html'),e('CRef '+c['uid']+' / CodeBlock '+c['block_uid']+' / RID '+c['block_ref_id']+' / '+expression(c['enable']))+'<br>'+', '.join(link(d['kind']+' NID '+d['nid'],'sources/decoded-original/'+d['file']) for d in c['native_declarations'])] for c in item['direct_calls_and_known_ancestors']])
    if item['unresolved_calls']:body+='<p>영향 범위 블록의 이름 미해석 호출 '+str(len(item['unresolved_calls']))+'곳은 확인 전입니다.</p>'
    body+='<h2 id="native">5. 후보 네트워크의 원본 핀·반전·배선</h2><p>Part UID·ORef/RefId·Wire는 각 네트워크의 원본 XML 범위입니다. 같은 번호를 다른 네트워크와 합치지 않습니다. 조건 전체는 해당 원본 자료에서 확인합니다.</p>'
    for proof_row in item['seed_evidence']:
        body+='<details><summary>'+e(proof_row['block']+' / 원본 '+str(proof_row['network']))+'</summary><p>'+link('원본 네트워크','networks/network-'+str(proof_row['network'])+'.html')+' · '+link('원본 XML',proof_row['file'])+'</p>'
        proof_rows=[]
        for part in proof_row['parts']:
            connections='<br>'.join(e('Wire '+wire['wire']+' · '+' | '.join(x['kind']+' '+str(x['uid'] or '')+(' / '+x['pin'] if x['pin'] else '')+(' / '+x['name']+' / RefId '+str(x['ref_id']) if x['name'] else '') for x in wire['endpoints'])) for wire in part['connections'])
            proof_rows.append([e(part['uid']+' / '+part['gate']),e(', '.join(part['negated_pins']) or '원본 Negated 없음'),connections])
        body+=table(['Part·Gate','반전 핀','원본 연결'],proof_rows)+'</details>'
    body+='<h2 id="signals">6. 선택 신호의 전체 읽기·쓰기 참조</h2><p>원본426개 LAD에서 이름과 Global/Local 선언 범위를 정확히 대조한 핀 목록입니다. 방향 미확정은 그대로 남깁니다. 핀 수·복수 쓰기의 존재는 현재 활성이나 오류의 증거가 아닙니다. ON은 공유 신호이며 여기의 전체 참조를 이 설비의 전용 조건으로 배정하지 않습니다. 백업의 기존 simulation 블록은 원본 읽기 자료로만 표시합니다.</p>'
    labels={'read':'읽기','write':'쓰기','pending':'방향 미확정'}
    for i,signal in enumerate(item['signals'],1):
        body+='<details id="focus-'+str(i)+'"><summary>'+e(signal['name']+' · '+signal['scope']+' · '+' / '.join(labels[k]+': '+str(signal['counts'].get(k,0)) for k in ['read','write','pending']))+'</summary><p>'+e(signal['context'])+' · '+e(signal['identity'])+'</p>'
        if signal['symbol_rows']:body+='<p>백업 심볼 주소: '+e(' / '.join(s['백업 주소'] or '주소 없음' for s in signal['symbol_rows']))+' · 현재 모듈·DB·실물 확인 전</p>'
        if signal['scope']=='Local':body+='<p>블록 '+e(signal['block'])+'의 Local 범위입니다. 같은 이름의 다른 블록 변수와 합치지 않습니다.</p>'
        if not signal['counts'].get('write'):body+='<p>이 원본 LAD 핀 목록에서 쓰기를 찾지 못했습니다. HMI·초기화·외부·다른 언어의 쓰기 또는 현재 값이 없다는 뜻은 아닙니다.</p>'
        body+=usage_table(signal['usages'])
        if signal['other_scope_usages']:
            body+='<h4>같은 이름의 다른 범위·범위 미확정 참조</h4><p>아래 '+str(len(signal['other_scope_usages']))+'개 참조는 이름만 같으며 위 신호의 읽기/쓰기 수·영향 주체와 합치지 않습니다. 원본 선언 범위를 추가 확인해야 합니다.</p>'+usage_table(signal['other_scope_usages'])
        body+='</details>'
    body+='<h2>수리 자료와 연결</h2><p>원본 대장에 명시된 설비: '+e(issue['equipment'])+' · 신호 참조 연관은 직접 제어·실물 동일성의 확정이 아닙니다.</p><nav class="inline-actions">'+''.join(link(k+' 수리 판단','repair-guides/'+k+'.html')+' ' for k in item['primary_priority_keys'])+'</nav>'
    if item['reference_related_priority_keys']:body+='<p>선택한 Global 신호의 정확한 이름으로 연관된 참고 작업지: '+', '.join(link(k,'repair-guides/'+k+'.html') for k in item['reference_related_priority_keys'])+'</p>'
    page='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(issue['id']+' 개선 영향·확인')+'</title><link rel="stylesheet" href="../assets/all-in-one.css"><style>td{overflow-wrap:anywhere}details{border:1px solid var(--line);border-radius:8px;padding:14px;margin:12px 0}summary{cursor:pointer;font-weight:600}</style></head><body><main style="max-width:1240px;margin:auto;padding:24px">'+body+'</main></body></html>'
    (ROOT/item['guide']).write_text(page)
print(json.dumps(dict(improvement_impact_guides=len(items),source_files=len(register['sources']),plc_changes=0,simulator_behavior_tests='not_rerun')))
