# D-ETF-1: 슈왑 SCHD 전체 보유 종목 내려받기 + 미래에셋 TIGER·한화 PLUS 상품 페이지 글자
import pathlib, datetime, json
from playwright.sync_api import sync_playwright
RAW = pathlib.Path(__file__).resolve().parent / 'raw'; D = datetime.date.today().strftime('%Y%m%d')
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
with sync_playwright() as p:
    b = p.chromium.launch(headless=False, args=["--window-position=-2000,0"])
    ctx = b.new_context(user_agent=UA, accept_downloads=True)
    pg = ctx.new_page()
    try:
        pg.goto('https://www.schwabassetmanagement.com/products/schd', timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("document.querySelectorAll('.ui-dialog,.ui-widget-overlay,#onetrust-banner-sdk').forEach(e=>e.remove())")
        try: pg.get_by_text('Portfolio', exact=True).first.click(force=True, timeout=4000); pg.wait_for_timeout(3000)
        except Exception: pass
        with pg.expect_download(timeout=40000) as dl:
            pg.get_by_text('Export All Holdings').first.click(force=True)
        f = dl.value; f.save_as(str(RAW / f'schwab_SCHD_holdings_{D}{pathlib.Path(f.suggested_filename).suffix}')); print('SCHD saved', f.suggested_filename)
    except Exception as e: print('SCHD ERR', str(e)[:200])
    for name, url in [('TIGER458730', 'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730002'),
                      ('TIGER466940', 'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7466940007'),
                      ('PLUS161510', 'https://www.plusetf.co.kr/product/detail?n=161510')]:
        got = []
        pg2 = ctx.new_page()
        pg2.on('response', lambda r: got.append(r.url) if ('json' in r.headers.get('content-type', '') or 'ajax' in r.url.lower() or '.do' in r.url) else None)
        try:
            pg2.goto(url, timeout=90000); pg2.wait_for_timeout(8000)
            (RAW / f'{name}_page_{D}.txt').write_text(pg2.inner_text('body'), encoding='utf-8')
            print(name, 'ok', len(pg2.inner_text('body')), got[:25])
        except Exception as e: print(name, 'ERR', str(e)[:150])
        pg2.close()
    b.close()
