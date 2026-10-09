"""Read-only reconstruction of XML fragments from the original TIA V18 PLF.

This does not implement the Siemens project file format, compile a PLC program,
or assert that every stored object is active. Network identity is matched to the
non-deleted search-index record with its persistent object key.
"""
from pathlib import Path
import base64, collections, json, re, sys, zlib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
ORIGINAL = Path('/private/tmp/gme-original-project-review-20261007')
ANALYSIS = Path('/private/tmp/gme-pv01-analysis-20261007')
OUT = ROOT / 'sources' / 'decoded-original'
OUT.mkdir(parents=True, exist_ok=True)
data = (ORIGINAL / 'GME_20250605/System/PEData.plf').read_bytes()
live = json.loads((ANALYSIS / 'live_index.json').read_text())
blocks = json.loads((ANALYSIS / 'block_summary.json').read_text())

def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

streams = {}
for match in re.finditer(rb'\x78[\x01\x5e\x9c\xda]', data):
    pos = match.start()
    try:
        dec = zlib.decompressobj()
        raw = dec.decompress(data[pos:], 16000000)
        if dec.eof and len(raw) > 20:
            streams[pos] = (raw, len(data)-pos-len(dec.unused_data))
    except zlib.error:
        pass

pattern = rb'<(FlgNet|IdentXmlPart|XmlPartIdentMapping|ICPayload)\b[^>]*>'
fragments = []
seen = set()
candidates = [(0, data, 0)] + [(p, x[0], x[1]) for p, x in streams.items()]
for pos, raw, packed in candidates:
    for m in re.finditer(pattern, raw):
        kind = m.group(1).decode()
        endtag = b'</' + m.group(1) + b'>'
        content = raw[m.start():]
        chunks = [pos] if packed else []
        end = pos + packed
        # Chunk length prefixes use one or two bytes, depending on packed size.
        while endtag not in content and packed and len(chunks) < 256:
            nextpos = next((end+gap for gap in (1,2,4) if end+gap in streams), None)
            if nextpos is None:
                break
            nxt, length = streams[nextpos]
            content += nxt
            chunks.append(nextpos)
            end = nextpos + length
        if endtag not in content:
            continue
        content = content[:content.index(endtag)+len(endtag)]
        offset = pos if packed else m.start()
        if (offset, kind) in seen:
            continue
        try:
            xml = ET.fromstring(content)
        except ET.ParseError:
            continue
        seen.add((offset, kind))
        filename = f'{len(fragments):04d}-{kind}.xml'
        (OUT / filename).write_bytes(content)
        fragments.append(dict(file=filename, source_offset=offset,
            compressed_chunks=chunks, root=kind, xml_bytes=len(content),
            parts=sum(1 for e in xml.iter() if e.tag.rsplit('}',1)[-1]=='Part'),
            wires=sum(1 for e in xml.iter() if e.tag.rsplit('}',1)[-1]=='Wire')))
save(OUT / 'fragment-inventory.json', fragments)

lad = [r for r in live if r.get('values',{}).get('LADFBD Code') and not r['deleted']]
blockmap = {(n['segment'],n['doc']):(b['name'], i+1) for b in blocks for i,n in enumerate(b['networks'])}
networks = []
for row in lad:
    fld = next(x for x in row['fields'] if x['id']==0)
    token = base64.b64decode(fld['value'])[7:19]
    hits = [m.start() for m in re.finditer(re.escape(token), data)]
    possible = [(f['source_offset']-h, h, f) for h in hits for f in fragments
                if f['root']=='FlgNet' and 0 < f['source_offset']-h < 1200]
    block, order = blockmap.get((row['segment'],row['i']), ('unmatched',0))
    item = dict(segment=row['segment'], document_id=row['i'], block=block,
                index_order=order, title=row['values'].get('Network title',''),
                index_code=row['values']['LADFBD Code'], object_key_hex=token.hex(),
                object_offsets=hits)
    if possible:
        dist, h, f = min(possible,key=lambda x:x[0])
        item.update(xml_file=f['file'],source_offset=f['source_offset'],
                    object_offset=h,distance=dist,parts=f['parts'],wires=f['wires'])
    networks.append(item)

def unescape(s):
    return re.sub(r'_x([0-9a-fA-F]{4})_',lambda m:chr(int(m[1],16)),s)

def norm(s):
    return re.sub(r'\s+', ' ', unescape(s).replace('"','').casefold()).strip()

idents = []
for f in fragments:
    if f['root']!='IdentXmlPart': continue
    xml = ET.parse(OUT/f['file']).getroot()
    for entry in xml:
        idnode = next((e for e in entry if e.tag.rsplit('}',1)[-1]=='ID'),None)
        if idnode is None: continue
        name = unescape(idnode.get('N',''))
        if not name:
            path = [unescape(e.get('N','')) for e in entry.iter()
                    if e.tag.rsplit('}',1)[-1]=='AO' and e.get('N')]
            name = '.'.join(path)
        if not name:
            constant = next((e for e in entry.iter() if e.tag.rsplit('}',1)[-1]=='CB'),None)
            if constant is not None:
                name = unescape(constant.get('SV',constant.get('V','')))
        if not name: continue
        for e in idnode.iter():
            if e.tag.rsplit('}',1)[-1]=='C':
                idents.append(dict(file=f['file'],nid=e.get('NID'),uid=e.get('UID'),
                    rid=idnode.get('RID'),name=name,kind=entry.tag.rsplit('}',1)[-1]))

# Resolve names conservatively: a candidate must both match UID/RID and appear
# in the source search text. Ambiguous names are retained as unresolved RefId.
# NID voting is recorded explicitly, rather than assuming index order == NID.
byref=collections.defaultdict(list)
for e in idents: byref[(e['uid'],e['rid'])].append(e)
for n in networks:
    if 'xml_file' not in n: continue
    xml=ET.parse(OUT/n['xml_file']).getroot()
    refs=[(e.get('UId'),e.get('RefId')) for e in xml.iter() if e.tag.rsplit('}',1)[-1]=='ORef']
    code=norm(n['index_code'])
    votes=collections.Counter()
    candidates={}
    for uid,rid in refs:
        hits=[e for e in byref[(uid,rid)] if e['kind']!='LiteralConstant'
              and norm(e['name']) in code]
        # A duplicated declaration should not create multiple NID votes.
        for nid in set(e['nid'] for e in hits): votes[nid]+=1
        candidates[uid]=hits
    top=votes.most_common(2)
    nid=top[0][0] if top and (len(top)==1 or top[0][1]>top[1][1]) else None
    n['inferred_original_nid']=nid
    n['nid_votes']=dict(votes)
    resolved={}
    for uid,rid in refs:
        hits=candidates[uid]
        if nid is not None: hits=[e for e in hits if e['nid']==nid]
        names=set(e['name'] for e in hits)
        if len(names)==1:
            resolved[uid]=dict(name=next(iter(names)),ref_id=rid,
                identifier_files=sorted(set(e['file'] for e in hits)),
                status='UID/RID + search-text + NID agreement')
    # Literal-only fragments have no symbol names to compare. Restrict them to
    # nearby identifier fragments already supported by several named matches,
    # and retain the different resolution method for review.
    file_votes=collections.Counter(f for v in resolved.values() for f in v['identifier_files'])
    supported=[int(f.split('-')[0]) for f,count in file_votes.items() if count>=2]
    if nid is not None and supported:
        for uid,rid in refs:
            if uid in resolved: continue
            hits=[e for e in byref[(uid,rid)] if e['kind']=='LiteralConstant'
                  and e['nid']==nid and any(abs(int(e['file'].split('-')[0])-i)<=3 for i in supported)
                  and norm(e['name']) and re.search(r'(?<![a-z0-9_])'+re.escape(norm(e['name']))+r'(?![a-z0-9_])',code)]
            names=set(e['name'] for e in hits)
            if len(names)==1:
                resolved[uid]=dict(name=next(iter(names)),ref_id=rid,
                    identifier_files=sorted(set(e['file'] for e in hits)),
                    status='literal candidate: UID/RID/NID + nearby named declarations + search-text agreement')
    n['resolved_operands']=resolved
    n['operand_count']=len(refs)
    n['resolved_operand_count']=len(resolved)
save(OUT/'network-map.json',networks)
save(OUT/'identifier-declarations.json',idents)
stats=dict(valid_xml_fragments=len(fragments),roots=dict(collections.Counter(f['root'] for f in fragments)),
    indexed_lad_networks=len(lad),matched_networks=sum('xml_file' in n for n in networks),
    unique_network_xml=len(set(n.get('xml_file') for n in networks if 'xml_file' in n)),
    operands=sum(n.get('operand_count',0) for n in networks),
    resolved_operands=sum(n.get('resolved_operand_count',0) for n in networks),
    method='read-only original PLF XML decompression; no TIA compile or execution')
save(OUT/'decode-summary.json',stats)
print(json.dumps(stats,ensure_ascii=False,indent=2))
