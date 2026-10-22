"""Offline drawing previews/locations. Reads originals; OCR runs locally on macOS.

Requires pdfplumber, pypdfium2, Pillow, Swift/Vision. Generated files are committed;
Netlify/browser never need an OCR runtime or external upload.
"""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import hashlib, json, subprocess, tempfile, time
import pdfplumber
import pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parent.parent
MANUAL=ROOT/'all-in-one'
SOURCES=[('oem','sources/Electrical_Rev2.pdf'),('construction','sources/Electrical_Can_Decoating_20241118.pdf'),('pid','sources/PID_1684n002I.pdf')]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def page_job(job):
    prefix,relative,number,source_hash,binary,scratch=job
    key=f'{prefix}-{number:03d}'
    pdf=pdfium.PdfDocument(str(MANUAL/relative)); page=pdf[number-1]
    image=page.render(scale=220/72).to_pil().convert('RGB')
    input_path=Path(scratch)/(key+'.png'); image.save(input_path)
    raw=json.loads(subprocess.check_output([binary,str(input_path)]))
    ocr=[]
    for record in raw['records']:
        original=record['candidates'][0]['text']
        for token in record['tokens']:
            if token['confidence']>=0.7:
                ocr.append(dict(text=token['text'],bbox=[round(x,7) for x in token['bbox']],confidence=round(token['confidence'],4),raw=original,method='vision-ocr'))
    # Read rotated native text in the direction of its character matrix.
    # Do not reverse numeric strings or synthesize aliases for another wire.
    with pdfplumber.open(MANUAL/relative) as doc:
        p=doc.pages[number-1]; width,height=p.width,p.height
        native=p.extract_words(x_tolerance=1,y_tolerance=2)
        native=[w for w in native if w.get('upright')]
        for sign,direction in [(1,'btt'),(-1,'ttb')]:
            rotated=p.filter(lambda c:c.get('object_type')=='char' and not c.get('upright',True) and c.get('matrix',[0,0])[1]*sign>0)
            native.extend(rotated.extract_words(x_tolerance=1,y_tolerance=2,line_dir_rotated='ltr',char_dir_rotated=direction))
        words=[dict(text=w['text'],bbox=[round(w['x0']/width,7),round(w['top']/height,7),round(w['x1']/width,7),round(w['bottom']/height,7)],method='pdf-text') for w in native]
    for word in words+ocr:
        b=word['bbox']
        if not(0<=b[0]<b[2]<=1.001 and 0<=b[1]<b[3]<=1.001):
            raise ValueError(f'Invalid bbox {key}: {word}')
    image.thumbnail((round(image.width*160/220),round(image.height*160/220)))
    image_path=f'assets/search-drawings/{key}.png'
    # Palette conversion preserves full-page geometry while keeping offline
    # packaging/browser download size practical. Original PDF remains intact.
    image.quantize(colors=128).save(MANUAL/image_path,optimize=True)
    output=f'registers/drawing-search/{key}.json'
    payload=dict(schema_version=1,key=key,source=relative,source_sha256=source_hash,page=number,width=width,height=height,image=image_path,words=words,ocr=ocr)
    (MANUAL/output).write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n')
    input_path.unlink()
    return dict(key=key,source=relative,page=number,image=image_path,data=output,image_sha256=sha(MANUAL/image_path),data_sha256=sha(MANUAL/output),native_words=len(words),ocr_tokens=len(ocr))

if __name__=='__main__':
    started=time.monotonic()
    for relative in ['assets/search-drawings','registers/drawing-search']:(MANUAL/relative).mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gme-drawing-search-',dir='/private/tmp') as scratch:
        binary=str(Path(scratch)/'vision-ocr')
        subprocess.run(['/usr/bin/swiftc','-O',str(ROOT/'scripts/drawing-ocr.swift'),'-o',binary],check=True)
        hashes={r:sha(MANUAL/r) for _,r in SOURCES};jobs=[]
        for prefix,relative in SOURCES:
            doc=pdfium.PdfDocument(str(MANUAL/relative))
            jobs.extend((prefix,relative,n,hashes[relative],binary,scratch) for n in range(1,len(doc)+1))
        pages=[]
        with ProcessPoolExecutor(max_workers=4) as pool:
            for item in pool.map(page_job,jobs,chunksize=1):
                pages.append(item)
                if len(pages)%25==0: print(f'{len(pages)}/{len(jobs)} pages',flush=True)
        result=dict(schema_version=1,coordinate_system='normalized top-left [x0,y0,x1,y1]',method='pdfplumber native words (rotation matrix direction) + local Apple Vision accurate en-US; OCR confidence >= 0.7; no language correction',source_hashes=hashes,pages=pages)
        (MANUAL/'registers/drawing-search-pages.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
        print(json.dumps(dict(pages=len(pages),native_words=sum(p['native_words'] for p in pages),ocr_tokens=sum(p['ocr_tokens'] for p in pages),seconds=round(time.monotonic()-started,1))))
