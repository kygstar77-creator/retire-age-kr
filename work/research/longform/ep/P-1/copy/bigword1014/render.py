import sys, os, json, base64, urllib.request
sys.argv=[sys.argv[0]]
V=r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\visual\P-1-thumb'
sys.path.insert(0,V)
import make_thumbs as M
from playwright.sync_api import sync_playwright
from PIL import Image
OUT=os.path.dirname(os.path.abspath(__file__))
C={'A':'손익분기 나이','B':'이득 끝나는 나이','C':'65세가 앞서는 나이','D':'이 나이부터 손해','E':'65세 수령에 역전'}
base=M.p1cake('#0F3A33','#0B2C27')
old="<div class='lab' style='left:330px;top:40px;font-size:52px;color:#fff'>"+M.SM0+"</div>"
assert old in base
V2={'Z':base}
for k,s in C.items():
    V2[k]=base.replace(old,f"<div class='t' style='left:330px;top:26px;font-size:74px;color:#fff'>{s}</div>")
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720})
    for k,h in V2.items():
        f=os.path.join(OUT,k+'.html'); open(f,'w',encoding='utf-8').write(M.HEAD+h+'\n'+M.TAIL)
        pg.goto('file:///'+f.replace(chr(92),chr(47))); pg.wait_for_selector('body[data-ready]')
        o=os.path.join(OUT,k+'.png'); pg.screenshot(path=o)
        bad=M.check_zones(pg)
        Image.open(o).resize((168,94),Image.LANCZOS).save(os.path.join(OUT,k+'_168.png')); print(k,'zones',bad or 'ok')
    b.close()
