import sys, json, re
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
seen=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    def on(r):
        u=r.url
        if 'plusetf' in u and not u.endswith(('.js','.css','.png','.svg','.woff2','.jpg')):
            try: seen.append((u, r.text()))
            except Exception: pass
    pg.on('response', on)
    pg.goto('https://www.plusetf.co.kr/product/list', wait_until='networkidle', timeout=60000); pg.wait_for_timeout(3000)
    body=pg.inner_text('body')
    links=sorted(set(pg.eval_on_selector_all('a', "a=>a.map(x=>x.href+'|'+x.innerText.slice(0,30))")))
    b.close()
print([l for l in links if '고배당' in l][:10])
for u,t in seen:
    if '161510' in t:
        i=t.find('161510'); print('HIT',u,t[max(0,i-300):i+200])
print(len(seen))
