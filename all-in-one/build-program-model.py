"""Extract a conservative executable subset and call sites from original LAD.

No expression strings are evaluated. UID/RID/NID resolved operands and original
wire topology form a typed AST. Missing operands, unsupported instructions and
call bodies block isolated execution. Source order is a model assumption until
checked against TIA; the tool is not a full CPU emulator.
"""
from pathlib import Path
from collections import defaultdict, Counter
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
DECODED = ROOT / 'sources/decoded-original'
original = json.loads((DECODED / 'network-map.json').read_text())
identifiers = json.loads((DECODED / 'identifier-declarations.json').read_text())
blocks = json.loads((ROOT / 'sources/block_summary.json').read_text())
lookup = defaultdict(list)
for d in identifiers:
    lookup[(d['uid'], d['rid'])].append(d)

def local(e):
    return e.tag.rsplit('}', 1)[-1]

def canon(name):
    return str(name).replace('"', '').casefold()

def constant(name):
    text = name.strip()
    if text.upper() in ('TRUE', 'FALSE'):
        return {'op': 'const', 'value': text.upper() == 'TRUE', 'literal': text}
    if re.fullmatch(r'[+-]?\d+(?:\.\d+)?', text):
        return {'op': 'const', 'value': float(text) if '.' in text else int(text), 'literal': text}
    match = re.fullmatch(r'(2|8|10|16)#([0-9A-Fa-f]+)', text)
    if match:
        return {'op': 'const', 'value': int(match[2], int(match[1])), 'literal': text}
    if text.upper().startswith(('S5T#', 'T#', 'TIME#')):
        body = text.split('#', 1)[1].replace('_', '').upper()
        pieces = re.findall(r'(\d+(?:\.\d+)?)(MS|D|H|M|S)', body)
        if pieces and ''.join(a+b for a, b in pieces) == body:
            ms = sum(float(a) * {'D':86400000, 'H':3600000, 'M':60000, 'S':1000, 'MS':1}[b] for a, b in pieces)
            return {'op': 'const', 'value': ms, 'literal': text, 'unit': 'ms'}
    return None

def ident_name(e, n):
    values = lookup[(e.get('UId'), e.get('RefId'))]
    exact = sorted({x['name'] for x in values if x['nid'] == n['inferred_original_nid']})
    if len(exact) == 1:
        return exact[0]
    literals = sorted({x['name'] for x in values if x['kind'] == 'LiteralConstant'
                       and canon(x['name']) in n['index_code'].replace('"', '').casefold()})
    return literals[0] if len(literals) == 1 else None

def combine(op, values):
    if len(values) == 1:
        return values[0]
    return {'op':op, 'args':values} if values else {'op':'unknown', 'reason':'연결된 입력이 없음'}

networks = []
call_sites = []
access = []
gate_counts = Counter()
write_gates = {'Coil', 'SCoil', 'RCoil', 'SdCoil', 'Move', 'Add', 'Sub', 'Mul', 'Div', 'Convert'}
supported = {'Contact', 'Coil', 'SCoil', 'RCoil', 'SdCoil', 'O', 'Not', 'Eq', 'Ne', 'Lt', 'Le', 'Gt', 'Ge', 'Move'}
for n in original:
    root = ET.parse(DECODED / n['xml_file']).getroot()
    elements = next(x for x in root if local(x) == 'Parts')
    parts = [x for x in elements if local(x) == 'Part']
    pmap = {p.get('UId'):p for p in parts}
    pinmap = defaultdict(list)
    wires = []
    for wire in next(x for x in root if local(x) == 'Wires'):
        ends = [{'kind':local(e), 'uid':e.get('UId'), 'pin':e.get('PinName')} for e in wire]
        wires.append({'uid':wire.get('UId'), 'ends':ends})
        for e in ends:
            if e['kind'] == 'PCon':
                pinmap[(e['uid'], e['pin'])].append(ends)
    refs = {}
    for ref in elements:
        if local(ref) != 'ORef':
            continue
        uid = ref.get('UId')
        name = n['resolved_operands'].get(uid, {}).get('name')
        # Extra resolution is intentionally restricted to literal constants.
        extra = ident_name(ref, n) if not name else None
        if extra and constant(extra) is not None:
            name = extra
        refs[uid] = {'name':name, 'ref_id':ref.get('RefId'), 'resolved':bool(name)}

    def operand(uid):
        name = refs.get(uid, {}).get('name')
        if not name:
            return {'op':'unknown', 'reason':f'피연산자 ORef {uid} 미해석'}
        return constant(name) or {'op':'read', 'key':canon(name), 'name':name}

    def pin(uid, name, seen=frozenset()):
        mark = (uid, name)
        if mark in seen:
            return {'op':'unknown', 'reason':f'연결 순환 {uid}.{name}'}
        results = []
        for ends in pinmap[mark]:
            for e in ends:
                if e['kind'] == 'Powerrail':
                    results.append({'op':'const', 'value':True})
                elif e['kind'] == 'OCon':
                    results.append(operand(e['uid']))
                elif e['kind'] == 'PCon' and (e['uid'], e['pin']) != mark and re.fullmatch(r'out\d*|eno|q', e['pin'] or ''):
                    results.append(output(e['uid'], e['pin'], seen | {mark}))
        return combine('and', results)

    def output(uid, port, seen):
        p = pmap.get(uid)
        if p is None:
            return {'op':'unknown', 'reason':f'호출 또는 외부 출력 {uid}.{port}'}
        gate = p.get('Gate')
        if gate == 'Contact':
            op = pin(uid, 'operand', seen)
            if any(local(e) == 'Negated' and e.get('PinName') == 'operand' for e in p):
                op = {'op':'not', 'arg':op}
            return combine('and', [pin(uid, 'in', seen), op])
        if gate == 'O':
            pins = sorted([v for u, v in pinmap if u == uid and re.fullmatch(r'in\d+', v or '')], key=lambda v:int(v[2:]))
            return combine('or', [pin(uid, v, seen) for v in pins])
        if gate in ('Eq', 'Ne', 'Lt', 'Le', 'Gt', 'Ge'):
            return combine('and', [pin(uid, 'pre', seen), {'op':gate.lower(), 'left':pin(uid, 'in1', seen), 'right':pin(uid, 'in2', seen)}])
        if gate == 'Not':
            return {'op':'not', 'arg':pin(uid, 'in', seen)}
        if gate in ('Coil', 'SCoil', 'RCoil', 'SdCoil'):
            # An SD coil's through output is RLO, not delayed timer status.
            return pin(uid, 'in', seen)
        if gate == 'Move' and port == 'eno':
            return pin(uid, 'en', seen)
        return {'op':'unknown', 'reason':f'지원 전 명령 {gate} {uid}.{port}'}

    def connected_refs(uid, port):
        return [e['uid'] for ends in pinmap[(uid, port)] for e in ends if e['kind'] == 'OCon']

    actions = []
    issues = []
    for order, p in enumerate(parts):
        uid, gate = p.get('UId'), p.get('Gate')
        gate_counts[gate] += 1
        if gate not in supported:
            issues.append(f'지원 전 명령: {gate} / Part {uid}')
        if gate not in write_gates:
            continue
        ports = ['operand'] if gate != 'Move' and gate not in ('Add', 'Sub', 'Mul', 'Div', 'Convert') else sorted({v for u, v in pinmap if u == uid and re.fullmatch(r'out\d*', v or '')})
        for port in ports:
            targets = connected_refs(uid, port)
            if len(targets) != 1 or not refs.get(targets[0], {}).get('name'):
                issues.append(f'쓰기 대상 미해석: {uid}.{port}')
                continue
            name = refs[targets[0]]['name']
            if constant(name) is not None:
                issues.append(f'상수 쓰기 대상: {uid}.{port}')
                continue
            action = dict(uid=uid, gate=gate, order=order, target=canon(name), name=name,
                          condition=pin(uid, 'en' if gate == 'Move' else 'in'))
            if gate == 'Move':
                action['value'] = pin(uid, 'in')
            if gate == 'SdCoil':
                action['preset'] = pin(uid, 'value')
            if gate not in supported:
                action['condition'] = {'op':'unknown', 'reason':f'지원 전 명령 {gate}'}
            actions.append(action)
    calls = []
    for call in elements:
        if local(call) != 'CRef':
            continue
        code = next((e for e in call if local(e) == 'CodeBlock'), None)
        name = ident_name(code, n) if code is not None else None
        args = {port:[refs.get(u, {}).get('name') or f'ORef {u} 미해석' for u in connected_refs(call.get('UId'), port)]
                for uid, port in pinmap if uid == call.get('UId') and connected_refs(uid, port)}
        site = dict(caller=n['block'], callee=name, network=n['document_id'], uid=call.get('UId'),
                    block_uid=code.get('UId') if code is not None else None,
                    enable=pin(call.get('UId'), 'en'), bindings=args,
                    callee_found=bool(name and any(canon(b['name']) == canon(name) for b in blocks)))
        calls.append(site)
        call_sites.append(site)
        issues.append(f'블록 호출 본문 실행 미지원: {name or "미해석"}')

    def walk(value):
        if isinstance(value, dict):
            yield value
            for v in value.values():
                yield from walk(v)
        elif isinstance(value, list):
            for v in value:
                yield from walk(v)
    for a in actions:
        issues.extend(x['reason'] for x in walk(a) if x.get('op') == 'unknown')
    # An unresolved unused reference also prevents declaring a complete network.
    issues.extend(f'ORef {u} 미해석' for u, v in refs.items() if not v['resolved'])
    writes = sorted({a['target'] for a in actions})
    reads = sorted({x['key'] for a in actions for x in walk(a) if x.get('op') == 'read'})
    refs_named = {canon(v['name']):v['name'] for v in refs.values() if v['name'] and constant(v['name']) is None}
    for key, name in refs_named.items():
        is_read, is_write = key in reads, key in writes
        access.append(dict(signal=key, name=name, block=n['block'], network=n['document_id'],
                           read=is_read, write=is_write,
                           role='읽기·쓰기' if is_read and is_write else '쓰기' if is_write else '읽기' if is_read else '호출 인자·미지원 명령 참조'))
    networks.append(dict(id=n['document_id'], block=n['block'], index=n['index_order'], title=n['title'],
                         file='sources/decoded-original/'+n['xml_file'], parts=[dict(uid=p.get('UId'), gate=p.get('Gate')) for p in parts],
                         actions=actions, calls=calls, refs=refs, reads=reads, writes=writes,
                         blockers=sorted(set(issues)), executable=bool(actions) and not issues))

by_id = {n['id']:n for n in networks}
specs = json.loads((ROOT / 'registers/control-spec.json').read_text())['specifications']
equipment = {}
for s in specs:
    linked = [by_id[int(n['문서 ID'])] for n in s['networks'] if int(n['문서 ID']) in by_id]
    equipment[s['id']] = dict(networks=[n['id'] for n in linked], executable=[n['id'] for n in linked if n['executable']],
                              blockers=[{'network':n['id'], 'reasons':n['blockers']} for n in linked if not n['executable']])

profiles = {
    'BC01':dict(networks=[1785, 1786, 1935], command='Flag.M_BC_01', output='Start BC01', feedback='Inputs.BC01 run',
                inverter='Inputs.BC01_All_inv', reset='Flag.RESET_ALLARM', timer='Tag_51', delay_ms=2000,
                fault='Allarm.BC_01_FAULT', inv_alarm='Allarm.BC01_INV',
                defaults={'ON':True, 'Flag.R1_GATE_LOOP_ON':True, 'MemoCMD_BC01_Startup':False, 'Flag.Maintenance_ON':False,
                          'UNDER TESTING':False, 'Inputs.BC01 trip wire':False, 'Allarm.BC_01_FC':False}),
    'FN04':dict(networks=[1809,1964,1965], command='Flag.M_FN_04', output='Start FN04', feedback='Inputs.FN04 Run',
                inverter='Inputs.FN04_All_inv', reset='Flag.RESET_ALLARM', timer='Tag_74', delay_ms=17000,
                fault='Allarm.FN_04_FAULT', inv_alarm='Allarm.FN04_INV',
                defaults={'ON':True, 'Data.SET_PERC_FN04':70, 'Stop_Fan_FN04':False, 'Allarm.MAX_MAX_TC09':False,
                          'Inputs.FEEDBACKMOTOR SC-01':True, 'Inputs.VR03 Run':True, 'Inputs.FEEDBACKMOTOR SC-10':True,
                          'Inputs.VR04 Run':True, 'Inputs.FEEDBACKMOTOR SC-11':True, 'Inputs.VR05 Run':True,
                          'Allarm.Prealarms_FN04':False}),
}
for key, p in profiles.items():
    assert all(by_id[n]['executable'] for n in p['networks']), [(n,by_id[n]['blockers']) for n in p['networks']]
    p['assumptions'] = ['원본 main 색인에서 알람 블록은 모터 블록보다 먼저 호출됩니다. 선택한 네트워크만 같은 순서로 반복합니다.',
                        '네트워크 내부 쓰기 순서는 XML Parts 순서를 사용한 모델 가정이며 TIA에서 확인 전입니다.',
                        '가상 기동 요청은 해당 Flag에 직접 주입합니다. HMI 전체 허가·입출력 전달·실제 기동 회로는 이 모델 밖입니다.',
                        '정상 센서 응답 지연은 500ms인 가상 장치 가정입니다. 시간 진행은 결정적 가상 시계이며 CPU 스캔·S5 시간 기반 오차를 모사하지 않습니다.',
                        '명시된 기본값은 시험 초기 조건입니다. 실제 설비의 정상 극성·현재 상태를 뜻하지 않습니다.']

multi = defaultdict(set)
for a in access:
    if a['write']:
        multi[a['signal']].add((a['block'],a['network']))
result = dict(version='0.1.0', source='GME_20250506.zap18 / decoded LAD', networks=networks,
              blocks=blocks, calls=call_sites, accesses=access, equipment=equipment, profiles=profiles,
              multiple_writers=[dict(signal=k, locations=[dict(block=b,network=n) for b,n in sorted(v)]) for k,v in sorted(multi.items()) if len(v)>1],
              semantics_sources=[dict(title='Siemens SD on-delay timer, S7-1500', url='https://docs.tia.siemens.cloud/r/en-us/v21/lad-s7-1200-s7-1500-s7-1200-g2/timer-operations-s7-1200-s7-1500-s7-1200-g2/legacy-s7-1500/sd-start-on-delay-timer-s7-1500',
                                     used_for='SD 타이머 상태와 통과 출력의 구분. V21 설명은 참고이며 V18 프로젝트의 TIA 실행 검증과 구분.')],
              counts=dict(networks=len(networks), executable=sum(n['executable'] for n in networks), calls=len(call_sites),
                          resolved_calls=sum(c['callee_found'] for c in call_sites), accesses=len(access), gates=dict(gate_counts)),
              limitations=['실제 PLC 연결 없음', '전체 CPU·블록 호출 실행 미구현', 'TIA 컴파일·현장 동일성 검증 전', '지원 명령 부분집합의 독립 네트워크 시험'])
(ROOT/'registers/program-model.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
payload=json.dumps(result,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
(ROOT/'assets/program-model-data.js').write_text('window.GME_PROGRAM_MODEL = '+payload+';\n')
print(json.dumps(result['counts'],ensure_ascii=False))
