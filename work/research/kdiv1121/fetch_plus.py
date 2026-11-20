# PLUS 고배당주(161510) 한화자산운용 상품 페이지 — 분배금 기록 글자·응답 주소 저장
import sys, json
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
seen=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    def on(r):
        if 'plusetf' in r.url and ('api' in r.url or 'json' in r.url):
            try: seen.append((r.url, r.text()[:20000]))
            except Exception: seen.append((r.url,''))
    pg.on('response', on)
    pg.goto('https://www.plusetf.co.kr/search?keyword=161510', wait_until='networkidle', timeout=60000)
    pg.wait_for_timeout(2500)
    links=pg.eval_on_selector_all('a', "a=>a.map(x=>x.href).filter(h=>h.includes('product'))")
    print('links', links[:10])
    tgt=[l for l in links if 'detail' in l]
    if tgt:
        pg.goto(tgt[0], wait_until='networkidle', timeout=60000); pg.wait_for_timeout(3000)
        for t in ('분배금','분배'):
            try: pg.locator(f'text={t}').first.click(timeout=3000); pg.wait_for_timeout(2000); break
            except Exception: pass
    print('url', pg.url)
    open('raw/plus_page.txt','w',encoding='utf-8').write(pg.inner_text('body'))
    json.dump(seen, open('raw/plus_api.json','w',encoding='utf-8'), ensure_ascii=False)
    b.close()
for u,_ in seen: print(u)
