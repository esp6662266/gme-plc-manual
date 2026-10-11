"""Explicitly reviewed catalog profiles; display/record data only, no PLC execution."""
import copy
import hashlib
import html
import json
import re
from pathlib import Path
from equipment_standard_profiles import build_static_profile

SECTIONS=['overview','io','control','circuits','alarms','repair','completion']
SECTION_TITLES=dict(zip(SECTIONS,['설비·자료 기준','I/O·HMI','제어 구조','전기 전달 경로','알람·복구','증상별 수리','완료 기준']))

def table_cells(line):
    # An odd run of backslashes escapes a pipe; an even run leaves a separator.
    cells=[];start=0
    for index,char in enumerate(line):
        if char!='|':continue
        slash=index-1
        while slash>=0 and line[slash]=='\\':slash-=1
        if (index-slash-1)%2:continue
        cells.append(line[start:index].strip());start=index+1
    cells.append(line[start:].strip())
    return cells[1:-1]

def blocks(text):
    result=[];lines=text.strip().splitlines();i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                rows.append(table_cells(lines[i].strip()));i+=1
            assert len(rows)>1 and all(re.fullmatch(r':?-+:?',c.replace(' ','')) for c in rows[1]),rows
            assert all(len(row)==len(rows[0]) for row in rows[2:]),rows
            result.append(dict(type='table',headers=rows[0],rows=rows[2:]));continue
        if line.startswith('```'):
            i+=1;code=[]
            while i<len(lines) and not lines[i].strip().startswith('```'):code.append(lines[i]);i+=1
            assert i<len(lines),'unterminated source code block'
            result.append(dict(type='code',text='\n'.join(code)));i+=1;continue
        if re.match(r'^(?:- |\d+\. )',line):
            values=[]
            while i<len(lines) and re.match(r'^(?:- |\d+\. )',lines[i].strip()):
                values.append(re.sub(r'^(?:- |\d+\. )','',lines[i].strip()));i+=1
            result.append(dict(type='list',items=values));continue
        if line.startswith('#'):
            result.append(dict(type='heading',text=line.lstrip('#').strip()));i+=1;continue
        paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(?:#|\||- |\d+\. |```)',lines[i].strip()):paragraph.append(lines[i].strip());i+=1
        result.append(dict(type='paragraph',text=' '.join(paragraph)))
    return result

def reviewed_sections(text,config):
    result={s:[] for s in SECTIONS}
    headings=list(re.finditer(r'^## (\d+)(?:\.)?\s+(.+)$',text,re.M))
    selected=config.get('section_numbers',[1,2,3,4,5,6,7])
    assert len(selected)==7 and len(set(selected))==7,'reviewed seven areas required'
    by_number={int(h.group(1)):h for h in headings}
    assert len(by_number)==len(headings),'duplicate draft sections'
    for index,number in enumerate(selected):
        assert number in by_number,(config['catalog_id'],number)
        h=by_number[number];position=headings.index(h)
        end=headings[position+1].start() if position+1<len(headings) else (re.search(r'^## 부록',text[h.end():],re.M).start()+h.end() if re.search(r'^## 부록',text[h.end():],re.M) else len(text))
        body=text[h.end():end];section=SECTIONS[index]
        if section=='completion' and config.get('completion_blocks'):
            result[section].append(dict(id='review-completion-current',title='현재 근거 공백과 판정 기준',type='reviewed',value=dict(blocks=config['completion_blocks']),links=[]))
            continue
        if index==6:
            # Historical cloud UI/publication/task status remains in the original
            # draft. The application shows only the current evidence gaps here.
            stop=re.search(r'^### 7\.[2-9]',body,re.M)
            if stop:body=body[:stop.start()]
            if config.get('completion_excerpt'):
                start,end=config['completion_excerpt']
                assert body.count(start)==1 and body.count(end)==1
                body=body.split(start,1)[1].split(end,1)[0]
        sub=list(re.finditer(r'^### (\d+\.\d+)\s+(.+)$',body,re.M))
        if not sub:
            result[section].append(dict(id='review-'+str(index+1),title=h.group(2),type='reviewed',value=dict(blocks=blocks(body)),links=[]))
        else:
            intro=body[:sub[0].start()].strip()
            if intro:result[section].append(dict(id='review-'+str(index+1),title=h.group(2),type='reviewed',value=dict(blocks=blocks(intro)),links=[]))
            for j,sh in enumerate(sub):
                part=body[sh.end():sub[j+1].start() if j+1<len(sub) else len(body)]
                result[section].append(dict(id='review-'+sh.group(1).replace('.','-'),title=sh.group(2),type='reviewed',value=dict(blocks=blocks(part)),links=[]))
    for section,items in config.get('supplements',{}).items():result[section].extend(items)
    for section in SECTIONS:assert result[section],section
    return result

def render_blocks(values):
    esc=lambda value:html.escape(str(value))
    output=[]
    for block in values:
        if block['type']=='table':
            output.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+esc(c)+'</th>'for c in block['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(c)+'</td>'for c in row)+'</tr>'for row in block['rows'])+'</tbody></table></div>')
        elif block['type']=='list':output.append('<ul>'+''.join('<li>'+esc(x)+'</li>'for x in block['items'])+'</ul>')
        else:
            tag={'heading':'h3','code':'pre'}.get(block['type'],'p');output.append('<'+tag+'>'+esc(block['text'])+'</'+tag+'>')
    return ''.join(output)

def add_catalog_profiles(root,data,source_rows):
    folder=root/'catalog-profiles'
    if not folder.exists():return
    for definition in sorted(folder.glob('*.json')):
        config=json.loads(definition.read_text(encoding='utf-8'));key=config['catalog_id']
        assert config['selection_key']==key and config['priority_key'] is None
        assert any(e['id']==key for e in data['equipment']),key
        assert not any(p['catalog_id']==key for p in data['equipment_standards']['profiles']),key
        draft=root/config['draft'];assert hashlib.sha256(draft.read_bytes()).hexdigest()==config['draft_sha256']
        sections=reviewed_sections(draft.read_text(encoding='utf-8'),config)
        for rule in config.get('text_corrections',[]):
            matches=0
            for items in sections.values():
                for item in items:
                    encoded=json.dumps(item,ensure_ascii=False)
                    matches+=encoded.count(rule['before']);encoded=encoded.replace(rule['before'],rule['after'])
                    item.clear();item.update(json.loads(encoded))
            assert matches==rule['expected_matches'],(key,rule['before'],matches)
        guide='catalog-guides/'+key+'.html'
        form=copy.deepcopy(config['record_form']);assert form['key']==key
        form['manual']=guide;form['blank_template']='';form['field_verified']=False;form['identity_confirmed']=False
        data['repair_record_forms']['profiles'].append(form)
        forms=data['repair_record_forms'];forms['counts']=dict(profiles=len(forms['profiles']),signals=sum(len(p['signals'])for p in forms['profiles']),steps=sum(len(p['steps'])for p in forms['profiles']))
        drawing=copy.deepcopy(config['drawing']);assert drawing['key']==key
        drawing['identity_verified']=False;drawing['field_verified']=False
        data['drawing_workspace']['profiles'].append(drawing)
        cfg={**config,'reviewed_sections':sections,'extra_sources':config['extra_sources']+[str(definition.relative_to(root)),config['draft']], 'reviewed_native_only':True}
        profile=build_static_profile(root,data,source_rows,cfg)
        sections['overview'].append(dict(id='review-source-hashes',title='검토 원본·해시와 자료 기준',type='reviewed',value=dict(blocks=[
            dict(type='paragraph',text='Dots 조사 기준 abcf31c5030bc7ef8749ed8e869a857f2387a28a / v1.12.0. 아래 해시는 현재 통합에 사용한 보존 원본·초안·검토 정의·도면 이미지의 전체 바이트 기준입니다. 원본 대응과 현재 CPU·현장 확인은 별개입니다.'),
            dict(type='table',headers=['파일','SHA-256'],rows=[[path,digest]for path,digest in profile['source_hashes'].items()]),
            dict(type='paragraph',text='자료 묶음 SHA-256: '+profile['source_bundle_sha256'])]),links=[]))
        # Link each reviewed section to its actual original scope and PDF sheets.
        for section,items in sections.items():
            sources=[]
            for label,path in config['section_sources'].get(section,[]):
                match=re.fullmatch(r'networks/network-(\d+)\.html#gme-[a-z0-9-]+-(part|wire)-(\d+)',path)
                if match:
                    number,kind,uid=match.groups()
                    location=next((loc for loc in profile['source_locations'] if loc['network']==int(number) and loc['kind']==kind and loc['uid']==uid),None)
                    assert location,(key,path)
                    path=location['path']
                sources.append([label,path])
            for item in items:item['links']=sources
        profile['reviewed_sections']=sections
        data['equipment_standards']['profiles'].append(profile)
        target=root/guide;target.parent.mkdir(exist_ok=True)
        content='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(key)+' 설비 근거</title><link rel="stylesheet" href="../assets/manual.css"></head><body><header><h1>'+html.escape(key)+' · 설비 근거와 관찰 기준</h1><p>백업·정적 근거. 현재 CPU·실물·현장 복구 확인 전.</p><a href="../index.html#view=manual&amp;equipment='+key+'&amp;scope=all">표준 작업실</a></header><main>'
        for section,items in sections.items():
            content+='<section id="'+section+'"><h2>'+html.escape(SECTION_TITLES[section])+'</h2>'
            for item in items:content+='<article id="'+item['id']+'"><h3>'+html.escape(item['title'])+'</h3>'+render_blocks(item['value']['blocks'])+'<p>'+ ' · '.join('<a href="../'+html.escape(path,quote=True)+'">'+html.escape(label)+'</a>' for label,path in item['links'])+'</p></article>'
            content+='</section>'
        for step in form['steps']:content+='<section id="'+step['common']+'"><h2>'+html.escape(step['title'])+'</h2><p>'+html.escape(step['observe'])+'</p><p>'+html.escape(step['compare'])+'</p><p>'+html.escape(step['next'])+'</p></section>'
        content+='</main></body></html>';target.write_text(content,encoding='utf-8')
        for path in [guide,config['draft'],str(definition.relative_to(root))]+config['extra_sources']+[s['image']for s in drawing['sheets']if s['image']]:
            if path not in data['resources']:data['resources'].append(path)
