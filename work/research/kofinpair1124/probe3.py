# 운용사 구성종목 3차 — KODEX(창 띄움)·ACE 펀드 화면·RISE 상품 찾기·HANARO 구성종목 화면 (firemap-write-b 2026-11-23)
import sys, json, pathlib, re
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
R = pathlib.Path(__file__).resolve().parent / 'raw'
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
def cap(ctx, name, url, words=(), wait=7000, keep=('api', 'ajax', '.do')):
    got = {}
    q = ctx.new_page()
    def on(r):
        ct = r.headers.get('content-type') or ''
        if 'json' in ct and any(k in r.url for k in keep):
            try: got[r.url] = r.text()
            except Exception: pass
    q.on('response', on)
    try:
        q.goto(url, timeout=60000); q.wait_for_timeout(wait)
        for t in words:
            try: q.get_by_text(t, exact=False).first.click(timeout=3000); q.wait_for_timeout(4000)
            except Exception: pass
        (R / 'pw' / f'{name}.txt').write_text(q.inner_text('body'), encoding='utf-8')
        print(name, q.url, len(q.inner_text('body')))
    except Exception as e: print(name, 'ERR', str(e)[:150])
    for u, t in got.items(): print('   ', u[:170], len(t))
    json.dump(got, open(R / 'pw' / f'{name}_api.json', 'w', encoding='utf-8'), ensure_ascii=False)
    return q
with sync_playwright() as p:
    b = p.chromium.launch(headless=False, args=["--window-position=-2000,0"]); ctx = b.new_context(user_agent=UA)
    q = ctx.new_page(); q.goto('https://m.samsungfund.com/etf/product/view.do?id=2ETFT8', timeout=60000); q.wait_for_timeout(9000)
    t = q.evaluate("fetch('/api/v1/kodex/product-pdf/2ETFT8.do?gijunYMD=20261120').then(r=>r.text())")
    (R / 'kodex_0153K0_20261120.json').write_text(t, encoding='utf-8'); print('kodex', t[:120])
    cap(ctx, 'ace_0139P0', 'https://www.aceetf.co.kr/fund/K55101EQ7660', ('구성종목', 'PDF'))
    t = q.evaluate("1")
    qq = cap(ctx, 'rise_find', 'https://kbam.co.kr/find?searchText=%EA%B3%A0%EB%B0%B0%EB%8B%B9', (), 8000, ('kbam',))
    links = qq.evaluate("Array.from(document.querySelectorAll('a')).map(a=>[a.href,a.innerText.slice(0,40)]).filter(x=>/products\//.test(x[0]))")
    print([l for l in links if '고배당' in l[1]][:10])
    cap(ctx, 'hanaro_hold', 'https://www.hanaroetf.com/fund/fund-holdings-list', (), 8000, ('hanaro',))
    cap(ctx, 'kiwoom_list', 'https://www.kiwoometf.com/service/etf/KO02010100M', (), 8000, ('kiwoom',))
    b.close()
