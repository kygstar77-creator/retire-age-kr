import sys, os, re, json, html, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont
HH=os.path.dirname(os.path.abspath(__file__)); V=os.path.join(HH,'..','visual','cafe-covers-1006')
sys.argv=[sys.argv[0]]
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
q='육아휴직 급여'
u='https://m.search.naver.com/search.naver?ssc=tab.m_cafe.all&sm=mtb_jum&query='+urllib.parse.quote(q)
t=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=30).read().decode('utf-8','ignore')
urls=[];seen=set()
for m in re.finditer(r'(https://search\.pstatic\.net/common/\?src=[^"\'\s<>]+?)(?=["\'\s<>])',t):
    x=html.unescape(m.group(1))
    if 'cafefiles' not in x and 'cafeptthumb' not in x and 'naver.net' not in x: continue
    if x in seen: continue
    seen.add(x); urls.append(x)
print('썸네일',len(urls))
files=[]
for i,x in enumerate(urls[:6],1):
    x2=re.sub(r'type=[^&]+','type=f192_192',x); fn=os.path.join(HH,'comp',f'cl_{i}.jpg')
    try: open(fn,'wb').write(urllib.request.urlopen(urllib.request.Request(x2,headers={'User-Agent':UA}),timeout=30).read()); files.append(fn)
    except Exception as e: print('fail',e)
json.dump({'q':q,'urls':urls[:6]},open(os.path.join(HH,'comp','comp.json'),'w',encoding='utf-8'),ensure_ascii=False)
S=110; F=ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf',12)
for k in 'F':
    items=[('우리 새 표지',os.path.join(HH,'covers_try',f'00_{k}.png'))]+[(f'경쟁 {i}',f) for i,f in enumerate(files[:5],1)]
    pad=12; bd=Image.new('RGB',(len(items)*(S+pad)+pad,S+2*pad+20),'white'); d=ImageDraw.Draw(bd)
    for i,(lab,pp) in enumerate(items):
        im=Image.open(pp).convert('RGB'); w,h=im.size; m=min(w,h)
        im=im.crop(((w-m)//2,(h-m)//2,(w-m)//2+m,(h-m)//2+m)).resize((S,S),Image.LANCZOS)
        x=pad+i*(S+pad); bd.paste(im,(x,pad)); d.text((x,pad+S+4),lab,fill='black',font=F)
    bd.save(os.path.join(HH,'covers_try',f'board_{k}.png'))
