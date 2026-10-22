"""Extract preserved public documents for search; never executes their content."""
from pathlib import Path
from html.parser import HTMLParser
import gzip, hashlib, json, re
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
MANUAL = ROOT / 'all-in-one'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

class Text(HTMLParser):
    skip_tags = {'script','style','nav','header','footer','aside','template','noscript'}
    blocks = {'p','div','section','article','h1','h2','h3','h4','li','tr','td','th','br','pre'}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.main = 0; self.article = 0; self.skip = 0; self.in_title = False
        self.body = []; self.fallback = []; self.title = []
    def handle_starttag(self, tag, attrs):
        if tag == 'title': self.in_title = True
        if tag in self.skip_tags: self.skip += 1
        if tag == 'main': self.main += 1
        if tag == 'article': self.article += 1
        if not self.skip and tag in self.blocks: self.add('\n')
    def handle_endtag(self, tag):
        if not self.skip and tag in self.blocks: self.add('\n')
        if tag == 'main': self.main = max(0,self.main-1)
        if tag == 'article': self.article = max(0,self.article-1)
        if tag in self.skip_tags: self.skip = max(0,self.skip-1)
        if tag == 'title': self.in_title = False
    def add(self, value):
        if self.main: self.body.append(value)
        elif self.article: self.fallback.append(value)
    def handle_data(self, value):
        if self.in_title: self.title.append(value)
        if not self.skip: self.add(value+' ')
    def result(self):
        text=''.join(self.body or self.fallback)
        text=re.sub(r'[ \t\r\f\v]+',' ',text)
        text=re.sub(r' *\n *','\n',text)
        return re.sub(r'\n{3,}','\n\n',text).strip()

data=json.loads((MANUAL/'registers/all-in-one-data.json').read_text())
equipment={e['id']:e for e in data['equipment']}
priority={p['key']:p.get('plc_id') for p in data['priority']}
page_refs={}
for profile in data.get('drawing_workspace',{}).get('profiles',[]):
    ident=profile.get('plc_id')
    if not ident: continue
    for sheet in profile.get('sheets',[]):
        if sheet.get('source') and sheet.get('page'):
            page_refs.setdefault((sheet['source'],sheet['page']),set()).add(ident)
records=[]; hashes={}; counts={'pdf_pages':0,'pdf_pages_without_text':0,'manual_documents':0}
pdfs=[('sources/Electrical_Rev2.pdf','OEM 전기도면'),('sources/Electrical_Can_Decoating_20241118.pdf','시공·케이블 도면'),('sources/PID_1684n002I.pdf','P&ID 공정도')]
for relative,label in pdfs:
    path=MANUAL/relative; hashes[relative]=sha(path)
    reader=PdfReader(path)
    for page_number,page in enumerate(reader.pages,1):
        # Layout extraction separates adjacent electrical tags that the old
        # plain-text export joined together. Vertical/vector text may be absent.
        text=page.extract_text(extraction_mode='layout',layout_mode_strip_rotated=False) or ''
        text=re.sub(r'[ \t]+',' ',text); text=re.sub(r'\n{3,}','\n\n',text).strip()
        counts['pdf_pages']+=1
        if not text: counts['pdf_pages_without_text']+=1
        refs=sorted(page_refs.get((relative,page_number),set()))
        records.append(dict(id=f'pdf-{Path(relative).stem}-{page_number}',kind='source',title=f'{label} · PDF {page_number}쪽',text=text,address='',symbol='',equipment=refs,equipment_names=[label],status='',source=f'{Path(relative).name} · PDF {page_number}쪽 · 텍스트 추출문',links=[dict(url=f'{relative}#page={page_number}',label=f'원본 도면 {page_number}쪽')],boundary='도면 텍스트 문맥입니다. 설비 필터는 기존 자료의 페이지 참조이며 전용 회로·현장 동일성 증명이 아닙니다. 세로 글자·벡터 선번·스캔 표기는 추출에서 빠질 수 있습니다.'))

for relative in sorted(set(data['resources'])):
    if not relative.endswith('.html') or relative=='index.html': continue
    path=MANUAL/relative; hashes[relative]=sha(path)
    parser=Text(); parser.feed(path.read_text(encoding='utf-8'))
    text=parser.result()
    if not text: continue
    title=' '.join(parser.title).strip() or relative
    stem=Path(relative).stem
    ident=stem if stem in equipment else priority.get(stem)
    if not ident and relative.startswith('PV01-detail/'): ident='PV01'
    refs=[ident] if ident in equipment else []
    stopped=any(x in relative for x in ['SYS-SIMULATION','manual-catalog']) or bool(re.search(r'networks/network-(?:1079|108[0-9]|109[0-2])\.html',relative))
    records.append(dict(id='manual-'+relative,kind='manual',title=title,text=text,address='',symbol='',equipment=refs,equipment_names=[ident+' · '+equipment[ident]['name']] if refs else ['공통·미배정 문서'],status='시뮬레이터 영구 중지 · 과거 보존 문맥' if stopped else '',source=relative,links=[dict(url=relative,label='해당 문서 열기')],boundary='기존 문서 ID의 참조이며 현재값·실행 결과·현장 대응을 확인한 것이 아닙니다. 과거 시험·시뮬레이션 안내는 영구 중지된 보존 자료입니다.'))
    counts['manual_documents']+=1

payload=dict(schema_version=1,extractor='pypdf layout + Python HTMLParser; no OCR; no operational records',source_hashes=hashes,counts=counts,records=records)
target=MANUAL/'registers/document-search-data.json.gz'
target.write_bytes(gzip.compress((json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n').encode(),compresslevel=9,mtime=0))
print(json.dumps(dict(**counts,compressed_bytes=target.stat().st_size),ensure_ascii=False))
