import sys, re, json, urllib.request, urllib.parse, html, os
sys.stdout.reconfigure(encoding='utf-8')
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
H=os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(H,'covers_try','comp'),exist_ok=True)
q='ISA 만기 연금저축'
u='https://m.search.naver.com/search.naver?ssc=tab.m_cafe.all&sm=mtb_jum&query='+urllib.parse.quote(q)
t=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=30).read().decode('utf-8','ignore')
open(os.path.join(H,'covers_try','cafe_tab.html'),'w',encoding='utf-8').write(t)
urls=[];seen=set()
for m in re.finditer(r'(https://search\.pstatic\.net/common/\?src=[^"\'\s<>]+?)(?=["\'\s<>])',t):
    x=html.unescape(m.group(1))
    if 'cafefiles' not in x and 'cafeptthumb' not in x and 'naver.net' not in x: continue
    if x in seen: continue
    seen.add(x); urls.append(x)
print(len(t),len(urls)); res=[]
for i,x in enumerate(urls[:14],1):
  try:
      x2=re.sub(r'type=[^&]+','type=f192_192',x); fn=f'ej_{i}.jpg'
      open(os.path.join(H,'covers_try','comp',fn),'wb').write(urllib.request.urlopen(urllib.request.Request(x2,headers={'User-Agent':UA}),timeout=30).read()); res.append(fn)
  except Exception as e: print('fail',i,e)
json.dump({'q':q,'ts':'10/9 08:3x','files':res},open(os.path.join(H,'covers_try','comp','comp.json'),'w',encoding='utf-8'))
# titles
tt=re.findall(r'<a[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</a>',t,re.S)
out=[]
for s in tt:
    s=html.unescape(re.sub(r'<[^>]+>','',s)).strip()
    if s and s not in out: out.append(s)
open(os.path.join(H,'comp_titles.txt'),'w',encoding='utf-8').write('\n'.join(out[:30]))
print(len(out)); print('\n'.join(out[:30]))
