"""Verify source preservation, reference integrity and documented coverage."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit,parse_qs
import csv, hashlib, json, re, zipfile, zlib
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
(ROOT/'verification-result.json').write_text(json.dumps(dict(status='checking',scope='Current document/source integrity checks; no execution'))+'\n')
def readcsv(name):return list(csv.DictReader((ROOT/'registers'/name).open(encoding='utf-8-sig')))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class Links(HTMLParser):
    def __init__(self):super().__init__();self.refs=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag in ('a','link') and 'href' in a:self.refs.append(a['href'])
        if tag in ('img','script') and 'src' in a:self.refs.append(a['src'])

guide=(ROOT/'operator-guide.html').read_text()
for key in ['P01','P02']:
    assert f'href="index.html#view=drawings&amp;equipment={key}&amp;scope=priority" target="_top"' in guide,key
errors=[];link_count=0;htmlfiles=list(ROOT.rglob('*.html'))
parsers={}
for p in htmlfiles:
    parser=Links();parser.feed(p.read_text());parsers[p.resolve()]=parser
for p,parser in parsers.items():
    for value in parser.refs:
        u=urlsplit(value)
        if u.scheme or u.netloc:continue
        link_count+=1
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        if not target.exists():errors.append(f'Missing link {p.relative_to(ROOT)} -> {value}')
        if target.suffix=='.html' and u.fragment and target in parsers and u.fragment not in parsers[target].ids:
            params=parse_qs(u.fragment)
            if target==(ROOT/'index.html').resolve() and params.get('view')==['drawings']:
                profiles=json.loads((ROOT/'registers/all-in-one-data.json').read_text())['drawing_workspace']['profiles']
                profile=next((r for r in profiles if params.get('equipment')==[r['key']]),None)
                if profile and params.get('scope')==['priority'] and set(params)<={'view','equipment','scope','drawing'} and ('drawing' not in params or params['drawing'] in [[s['id']] for s in profile['sheets']]):
                    assert "params.get('view')==='drawings'" in (ROOT/'assets/all-in-one.js').read_text()
                    continue
            if target==(ROOT/'index.html').resolve() and params.get('view')==['repair']:
                profiles=json.loads((ROOT/'registers/repair-record-forms.json').read_text())['profiles']
                profile=next((r for r in profiles if r['key'] in ['P01','P02'] and params.get('equipment')==[r['key']]),None)
                if profile and params.get('scope')==['priority'] and set(params)<={'view','equipment','scope','symptom'} and ('symptom' not in params or params['symptom'] in [[s['id']] for s in profile['steps']]):
                    assert "params.get('view')==='repair'" in (ROOT/'assets/all-in-one.js').read_text()
                    continue
            if target==(ROOT/'index.html').resolve() and params.get('view') in [['repair-record'],['review']]:
                profiles=json.loads((ROOT/'registers/repair-record-forms.json').read_text())['profiles']
                if params.get('equipment') in [[r['key']] for r in profiles] and params.get('scope')==['priority'] and set(params)<={'view','equipment','scope'}:
                    js=(ROOT/'assets/all-in-one.js').read_text()
                    assert "params.get('view')==='"+params['view'][0]+"'" in js
                    continue
            errors.append(f'Missing anchor {p.relative_to(ROOT)} -> {value}')

equipment=readcsv('equipment.csv');io=readcsv('equipment-io.csv');hmi=readcsv('equipment-hmi.csv')
source_symbols=readcsv('plc-symbols.csv');source_hmi=list(csv.DictReader((ROOT/'sources/hmi_plc_tags.csv').open(encoding='utf-8-sig')))
symbol_keys={(s['원본 심볼'],s['백업 주소'],s['자료형'],s['문서 ID']) for s in source_symbols}
hmi_keys={(h['HMI 태그'],h['설정 주소'],h['Access Name'],h['태그 내부 ID']) for h in source_hmi}
ids=[d['ID'] for d in equipment]
assert len(ids)==len(set(ids))
assert all(not d['상위 설비'] or d['상위 설비'] in ids for d in equipment)
assert all((ROOT/'devices'/f'{id}.html').exists() for id in ids)
assert all((r['원본 심볼'],r['백업 주소'],r['자료형'],r['문서 ID']) in symbol_keys for r in io)
assert all((r['HMI 태그'],r['설정 주소'],r['Access Name'],r['내부 ID']) in hmi_keys for r in hmi)
assert len(source_hmi)==782 and len(source_symbols)==789
assert {r['백업 주소'] for r in io if r['설비 ID']=='PV01' and re.match(r'%[iq]',r['백업 주소'],re.I)}=={'%i8.6','%i8.7','%i9.0','%i9.1','%i9.2','%i9.3','%q5.2','%q5.3'}
assert {r['백업 주소'] for r in io if r['설비 ID']=='PV02' and re.match(r'%[iq]',r['백업 주소'],re.I)}=={'%i9.4','%i9.5','%i9.6','%i9.7','%i10.0','%i10.1','%q5.4','%q5.5'}
assert all(d['ID'].startswith('CYL-') or d['ID'].startswith('CLIENT-') for d in equipment if 'CL' in d['ID'] and re.search(r'CL\d',d['ID']))
for i in range(11,91):
    rows=[r for r in io if r['설비 ID']==f'EV{i:02}' and r['백업 주소'].startswith('%q')]
    assert len(rows)==1,(i,rows)
    d=next(d for d in equipment if d['ID']==f'EV{i:02}')
    assert d['상위 설비']==('BF01' if i<=50 else 'BF02')
    assert d['전기 회로'].count('FG ')==1,(i,d['전기 회로'])

decode=ROOT/'sources/decoded-original';networks=json.loads((decode/'network-map.json').read_text());inventory=json.loads((decode/'fragment-inventory.json').read_text())
inv={f['file']:f for f in inventory};plf=(ROOT/'sources/PEData.plf').read_bytes()
assert len(networks)==426 and len({n['xml_file'] for n in networks})==426
rebuilt=0;dangling=[]
for n in networks:
    f=inv[n['xml_file']];stored=(decode/n['xml_file']).read_bytes()
    if f['compressed_chunks']:
        raw=b''.join(zlib.decompress(plf[pos:]) for pos in f['compressed_chunks'])
        start=raw.index(b'<FlgNet');end=raw.index(b'</FlgNet>')+len(b'</FlgNet>')
        assert raw[start:end]==stored
    else:assert plf[f['source_offset']:f['source_offset']+len(stored)]==stored
    assert plf[n['object_offset']:n['object_offset']+12]==bytes.fromhex(n['object_key_hex'])
    assert n['distance']==n['source_offset']-n['object_offset'] and 0<n['distance']<1200
    root=ET.fromstring(stored)
    part_container=next(e for e in root if e.tag.rsplit('}',1)[-1]=='Parts')
    declared={e.get('UId') for e in part_container.iter() if e.get('UId')}
    for e in root.iter():
        if e.tag.rsplit('}',1)[-1] in ('PCon','OCon') and e.get('UId') not in declared:dangling.append((n['document_id'],dict(e.attrib)))
    assert (ROOT/'networks'/f"network-{n['document_id']}.html").exists()
    rebuilt+=1
assert not dangling,dangling
tests=readcsv('simulation-tests.csv');checks=readcsv('verification.csv')
assert len({t['시험 ID'] for t in tests})==len(tests)
assert all(t['상태']=='설계·미실행' for t in tests)
assert all(c['상태']=='확인 대기' for c in checks)
assert {t['설비 ID'] for t in tests}==set(ids)
for item in json.loads((ROOT/'sources/source-manifest.json').read_text()):assert sha(ROOT/item['file'])==item['sha256']
for item in json.loads((ROOT/'registers/additional-source-manifest.json').read_text()):assert sha(ROOT/item['file'])==item['sha256']
if errors:raise AssertionError('\n'.join(errors[:30]))
result=dict(status='passed',html_pages=len(htmlfiles),local_links_checked=link_count,
    unique_equipment_ids=len(ids),original_lad_reconstructed_from_plf=rebuilt,
    indexed_object_keys_verified=426,pulse_valve_channels_checked=80,
    source_symbol_rows_verified=len(io),source_hmi_rows_verified=len(hmi),
    no_dangling_wire_endpoints=True,tests_marked_unexecuted=len(tests),
    pending_verification_rows=len(checks),broken_links=0,
    scope='document/source integrity only; not TIA compilation, PLC execution or field verification')
(ROOT/'verification-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
