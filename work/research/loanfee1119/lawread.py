import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    for name,art,kw in [('한국주택금융공사법시행령','제22조','출연'),('서민의금융생활지원에관한법률시행령','제21조','출연'),('은행법','제30조의3',''),('은행법시행령','제18조의5','')]:
        pg.goto(f'https://www.law.go.kr/법령/{name}/{art}',timeout=40000); pg.wait_for_timeout(4000)
        txt=''
        for f in pg.frames:
            try: txt+=f.inner_text('body')
            except Exception: pass
        open(f'raw/law_{name}_{art}.txt','w',encoding='utf-8').write(txt)
        i=txt.find(art); print('=====',name,art,len(txt)); print(txt[i:i+1500])
    b.close()
