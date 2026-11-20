import sys, json
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
seen=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    def on(r):
        u=r.url
        if 'plusetf' in u and not u.endswith(('.js','.css','.png','.svg','.woff2','.jpg')):
            try: seen.append((u, r.text()[:30000]))
            except Exception: pass
    pg.on('response', on)
    pg.goto('https://www.plusetf.co.kr/', wait_until='networkidle', timeout=60000); pg.wait_for_timeout(2000)
    links=sorted(set(pg.eval_on_selector_all('a', "a=>a.map(x=>x.href)")))
    print([l for l in links if 'product' in l][:15])
    json.dump(seen, open('raw/plus_home_api.json','w',encoding='utf-8'), ensure_ascii=False)
    b.close()
for u,t in seen:
    if '161510' in t or '고배당주' in t: print('HIT', u)
print(len(seen), [u for u,_ in seen][:15])
