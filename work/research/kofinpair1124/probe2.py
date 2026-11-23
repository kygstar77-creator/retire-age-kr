# 운용사 구성종목 2차 탐색 — KODEX(브라우저 안 fetch)·ACE·RISE·HANARO·KIWOOM (firemap-write-b 2026-11-23)
import sys, json, pathlib
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
R = pathlib.Path(__file__).resolve().parent / 'raw'
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(user_agent=UA)
    pg = ctx.new_page()
    pg.goto('https://m.samsungfund.com/etf/product/list.do', timeout=60000); pg.wait_for_timeout(5000)
    for fid, code in (('2ETFT8', '0153K0'),):
        t = pg.evaluate(f"fetch('/api/v1/kodex/product-pdf/{fid}.do?gijunYMD=20261120').then(r=>r.text())")
        (R / f'kodex_{code}_20261120.json').write_text(t, encoding='utf-8'); print('kodex', code, t[:150])
    # ACE: 검색
    pg.goto('https://www.aceetf.co.kr/', timeout=60000); pg.wait_for_timeout(4000)
    for q in ('고배당주',):
        t = pg.evaluate(f"fetch('https://papi.aceetf.co.kr/api/funds?searchValue={q}&page=1&size=50').then(r=>r.text())")
        (R / 'ace_search.json').write_text(t, encoding='utf-8'); print('ace search', t[:600])
    for name, url, words in (('rise', 'https://kbam.co.kr/find?searchText=315960', ('구성종목', 'PDF')),
                             ('hanaro', 'https://www.hanaroetf.com/', ()),
                             ('kiwoom', 'https://www.kiwoometf.com/', ())):
        got = []
        q = ctx.new_page(); q.on('response', lambda r, got=got: got.append(r.url) if 'json' in (r.headers.get('content-type') or '') else None)
        try:
            q.goto(url, timeout=60000); q.wait_for_timeout(8000)
            (R / 'pw' / f'{name}_home.txt').write_text(q.inner_text('body'), encoding='utf-8')
            links = q.evaluate("Array.from(document.querySelectorAll('a')).map(a=>a.href).filter(h=>/product|prod|fund|etf/i.test(h)).slice(0,40)")
            print(name, q.url, len(q.inner_text('body')), links[:15])
        except Exception as e: print(name, 'ERR', str(e)[:150])
        for u in got[:25]: print('   ', u[:180])
        q.close()
    b.close()
