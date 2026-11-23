# 운용사 상품 페이지가 부르는 구성종목 API 찾기 (firemap-write-b 2026-11-23)
import sys, json, pathlib
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
R = pathlib.Path(__file__).resolve().parent / 'raw' / 'pw'
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
SITES = [
 ('tiger210780', 'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7210780003'),
 ('ace_home', 'https://www.aceetf.co.kr/fund/K55101DN4471'),
 ('rise_home', 'https://www.riseetf.co.kr/prod/finder?searchText=315960'),
 ('hanaro_home', 'https://www.hanaroetf.com/product/list'),
 ('kiwoom_home', 'https://www.kiwoometf.com/service/etf/KO02010200M'),
 ('kodex_home', 'https://www.samsungfund.com/etf/product/list.do'),
]
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(user_agent=UA)
    for name, url in SITES:
        got = []
        pg = ctx.new_page()
        pg.on('response', lambda r, got=got: got.append((r.status, r.url)) if ('json' in (r.headers.get('content-type') or '') ) else None)
        try:
            pg.goto(url, timeout=60000, wait_until='domcontentloaded'); pg.wait_for_timeout(6000)
            for t in ('구성종목', 'PDF', '구성 종목'):
                try: pg.get_by_text(t, exact=False).first.click(timeout=2500); pg.wait_for_timeout(3000); break
                except Exception: pass
            (R / f'{name}.txt').write_text(pg.inner_text('body'), encoding='utf-8')
            print(name, pg.url, len(pg.inner_text('body')))
        except Exception as e: print(name, 'ERR', str(e)[:120])
        for s, u in got[:40]: print('   ', s, u[:200])
        pg.close()
    b.close()
