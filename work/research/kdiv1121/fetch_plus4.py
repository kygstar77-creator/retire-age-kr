# PLUS 고배당주(161510) 한화자산운용 상품 페이지 n=006273 — 분배금 탭 글자·응답 저장
import sys, json
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
seen=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    def on(r):
        u=r.url
        if 'plusetf' in u and not u.endswith(('.js','.css','.png','.svg','.woff2','.jpg','.gif')):
            try: seen.append((u, r.text()))
            except Exception: pass
    pg.on('response', on)
    pg.goto('https://www.plusetf.co.kr/product/detail?n=006273', wait_until='networkidle', timeout=60000); pg.wait_for_timeout(2500)
    for t in ('분배금','분배'):
        try: pg.get_by_text(t, exact=True).first.click(timeout=4000); pg.wait_for_timeout(2500); break
        except Exception as e: print('noclick',t)
    for i in range(6):
        try: pg.get_by_text('더보기').first.click(timeout=2000); pg.wait_for_timeout(1200)
        except Exception: break
    open('raw/plus_006273.txt','w',encoding='utf-8').write(pg.inner_text('body'))
    json.dump(seen, open('raw/plus_006273_api.json','w',encoding='utf-8'), ensure_ascii=False)
    b.close()
for u,t in seen:
    if '분배' in t or 'dist' in u.lower() or 'divid' in u.lower(): print('API',u,len(t))
