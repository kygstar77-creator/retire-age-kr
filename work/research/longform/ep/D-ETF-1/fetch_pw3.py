# D-ETF-1: 미래에셋 TIGER 구성종목(PDF) — 페이지 안에서 같은 주소를 불러 세션째 받는다
import pathlib, datetime, json
from playwright.sync_api import sync_playwright
RAW = pathlib.Path(__file__).resolve().parent / 'raw'; D = datetime.date.today().strftime('%Y%m%d')
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
with sync_playwright() as p:
    b = p.chromium.launch(headless=False, args=["--window-position=-2000,0"]); pg = b.new_page(user_agent=UA)
    for c in ['KR7466940007', 'KR7458730002']:
        pg.goto(f'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund={c}', timeout=90000); pg.wait_for_timeout(6000)
        r = pg.evaluate("""async (c) => { const u = `/tigeretf/ko/product/chart/prdct-item-list.ajax?ksdFund=${c}&prfPrd=Week01&fixDate=&listCnt=200`;
              const x = await fetch(u, {headers: {'X-Requested-With': 'XMLHttpRequest'}}); return await x.text(); }""", c)
        (RAW / f'tiger_{c}_items_{D}.json').write_text(r, encoding='utf-8')
        d = json.loads(r).get('rtnData', []); print(c, len(d), json.dumps(d[:1], ensure_ascii=False)[:400])
    b.close()
