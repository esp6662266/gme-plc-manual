"""Render unassigned identification reports; never generate or assign PLC logic."""
from pathlib import Path
from html import escape as e
import json,hashlib,re
R=Path(__file__).resolve().parent
d=json.loads((R/'registers/identification-reports.json').read_text())
for f,h in d['source_hashes'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
out=R/'identification-guides';out.mkdir(exist_ok=True)
style='body{margin:0;padding:24px;background:#edf3f7;color:#183247;font:16px/1.7 system-ui}main{max-width:1000px;margin:auto}section{background:white;border:1px solid #cddce7;border-radius:10px;padding:22px;margin:16px 0}h1,h2{line-height:1.4}a{color:#076888;overflow-wrap:anywhere}nav{display:flex;gap:14px;flex-wrap:wrap}.notice{padding:16px;background:#fff3cf;border-left:5px solid #c39127}p,code{overflow-wrap:anywhere}.proof p{font-size:14px}@media(max-width:720px){body{padding:10px}section{padding:14px}}@media print{@page{size:A4;margin:14mm}body{background:white;padding:0;font-size:9.5pt;line-height:1.45}section{border:0;border-radius:0;padding:0;margin:8px 0;break-inside:avoid}nav,.screen-only{display:none}h1{font-size:18pt}h2{font-size:13pt}.notice{font-size:10pt}.proof{break-before:page}.proof p{font-size:9pt}p{margin:8px 0}a{color:inherit;text-decoration:none}}'
for p in d['profiles']:
 assert p['plc_id'] is None and not p['identity_verified'] and not p['assigned_signals']
 body='<h1>'+e(p['key']+' · '+p['title']+' 식별 조사')+'</h1><p class="notice">문서 complete_with_gaps · PLC 미배정 · 실물 동일성 미확정 · 전용 신호/알람/타이머0. 주변 후보와 본체 소유를 구분합니다. TIA·현재 CPU·현장 복구 확인 전.</p>'
 body+='<nav>'+''.join('<a href="#'+sid+'">'+e(title)+'</a>'for sid,title,_ in p['areas'])+'</nav>'
 for sid,title,text in p['areas']:body+='<section id="'+sid+'"><h2>'+e(title)+'</h2><p>'+e(text)+'</p></section>'
 body+='<section class="proof" id="sources"><h2>독립 확인한 원본 범위</h2><p>선택 핀·배선·UID/RID/NID 선언과 표시한 실제 PDF쪽에 한정합니다. 전체 첨부의 해시 일치는 전체 논리 검토나 실물 동일성의 증거가 아닙니다. 원본·미확정·기존 관찰 양식·중지5를 보존했습니다.</p><p><a href="../sources/PID_1684n002I.pdf#page=1">P&amp;ID PDF1 · 두 유로/배치</a></p>'
 for fn,label,nums in [('Electrical_Rev2.pdf','OEM',p['oem_pages']),('Electrical_Can_Decoating_20241118.pdf','시공',p['construction_pages'])]:
  body+='<p>'+''.join('<a href="../sources/'+fn+'#page='+str(num)+'">'+label+' PDF'+str(num)+'</a> · 'for num in nums)+'</p>'
 for name in p['networks']:
  n=d['native'][name];body+='<p>'+e('LAD'+str(n['network'])+' / NID'+str(n['nid']))+' · <a href="../networks/network-'+str(n['network'])+'.html">원본 네트워크</a> · <a href="../sources/decoded-original/'+name+'-FlgNet.xml">XML '+name+'</a><br>'+e('Parts '+', '.join(z['UId']+':'+z.get('Gate','RID'+z.get('RefId',''))for z in n['parts']))+'<br>'+e('Wires '+', '.join(z['UId']for z in n['wires']))+'</p>'
 body+='<p><a href="../registers/identification-reports.json">핀·배선·선언·해시 JSON</a> · <a href="../'+p['key']+'-IDENTIFICATION.md">식별 보고서 MD</a></p></section><section id="tools"><h2>관찰 기록과 보고서</h2><p>기존 관찰 양식은 미확정/신호0을 유지합니다. 공통 기록·백업·비교 도구와 식별 문서의 A4 인쇄를 사용할 수 있으나 설비 표준 프로파일/전용 원본 비교쌍을 새로 만들지 않았습니다.</p><p><a href="../index.html#view=repair-record&amp;equipment='+p['key']+'&amp;scope=priority">자기 관찰·수리 기록</a> · <a href="../unresolved-identity.html#identity-'+p['key']+'">식별 후보 작업지</a> · <a href="../priority-guides/'+p['key']+'.html">기존 대응 작업지로 돌아가기</a></p></section>'
 (out/(p['key']+'.html')).write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(p['key']+' 식별 조사 | GME')+'</title><style>'+style+'</style></head><body><main>'+body+'</main></body></html>')
# This HTML-only extension leaves the historical identity JSON and all record
# schema provenance intact. Run after build-unresolved-identity.py if rebuilt.
page=R/'unresolved-identity.html';html=page.read_text();html=re.sub(r'<p class="identification-extension".*?</p>','',html)
for p in d['profiles']:
 marker='<section id="identity-'+p['key']+'">';assert marker in html
 html=html.replace(marker,marker+'<p class="identification-extension"><a href="identification-guides/'+p['key']+'.html">2026-10-11 독립 식별 보고서 · 7영역·원본·필요 자료</a></p>')
page.write_text(html)
print(json.dumps(dict(reports=len(d['profiles']),assigned_signals=0,identity_verified=0,raw_identity_JSON_unchanged=True)))
