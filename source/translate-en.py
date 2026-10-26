from html.parser import HTMLParser
from html import escape
import json,re
texts=json.loads((src/'texts.json').read_text())
translations={texts[int(i)]:v for i,v in (line.split('|',1) for line in (src/'en-translations.txt').read_text().splitlines() if line)}
translations.update({
 'Cărți, capitole și lucrări științifice în măsurări, energie, instrumentație și aplicații interdisciplinare.':'Books, chapters and scientific papers on measurements, energy, instrumentation and interdisciplinary applications.',
 'Caută după titlu, autor sau cuvânt-cheie':'Search by title, author or keyword', 'An':'Year','Toți anii':'All years','Toate categoriile':'All categories','Capitole internaționale':'International book chapters','Cărți naționale':'National books','Reviste ISI':'ISI-indexed journals','Conferințe ISI':'ISI-indexed conferences','Reviste BDI':'Internationally indexed journals','Conferințe BDI':'Internationally indexed conferences','Suporturi didactice și îndrumare':'Teaching materials and laboratory manuals','Resetează':'Reset','146 înregistrări':'146 records','Descarcă datele (JSON)':'Download data (JSON)',
 'Referințe transcrise din lista lucrărilor și completate din fișa CNATDCU 251006. Clasificarea și metadatele bibliografice păstrează informațiile din document; nu reprezintă o verificare independentă a indexării.':'References transcribed from the publication list and supplemented by CNATDCU record 251006. Bibliographic metadata and classifications follow the source documents and do not represent independent verification of indexing.',
 'Nicio lucrare nu corespunde filtrelor. Încercați alt termen sau resetați filtrele.':'No publications match these filters. Try another term or reset the filters.',
 'De exemplu: energy, senzori, Seritan':'For example: energy, sensors, Seritan', 'Navigare principală':'Main navigation','Profiluri academice':'Academic profiles','Profesorul George-Călin Serițan':'Professor George-Călin Serițan',
 'Profilul academic al profesorului George-Călin Serițan: cercetare, publicații și educație în inginerie electrică.':'Academic profile of Professor George-Călin Serițan: research, publications and teaching in electrical engineering.'
})
def tr(s):
 stripped=s.strip()
 if stripped in translations:return s.replace(stripped,translations[stripped])
 if ' | ' in stripped:
  title,name=stripped.split(' | ',1);return tr(title)+' | '+name
 return s
class Translate(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.result=[]
 def handle_decl(self,d):self.result.append('<!'+d+'>')
 def handle_starttag(self,t,attrs):
  at=[]
  for k,v in attrs:
   if k=='lang':v='en-GB'
   elif k=='src' and v=='app.js':v='app.js?v=en-1'
   elif k in ('alt','aria-label','placeholder','data-type') or (k=='content' and t=='meta'):v=tr(v) if v else v
   at.append(k if v is None else k+'="'+escape(v,quote=True)+'"')
  self.result.append('<'+t+(' '+' '.join(at) if at else '')+'>')
 def handle_endtag(self,t):self.result.append('</'+t+'>')
 def handle_data(self,s):self.result.append(escape(tr(s),quote=False))
 def handle_comment(self,s):self.result.append('<!--'+s+'-->')
for f in out.glob('*.html'):
 p=Translate();p.feed(f.read_text());f.write_text(''.join(p.result))
# Keep menu state and live filter announcements in English too.
(out/'app.js').write_text((src/'app.js').read_text().replace("filterForm.dataset.noun||'publications'", "filterForm.dataset.noun||'records'"))
pubs_en=json.loads((out/'data/publications.json').read_text())
for item in pubs_en:item['category']=tr(item['category'])
(out/'data/publications.json').write_text(json.dumps(pubs_en,ensure_ascii=False,indent=2))
