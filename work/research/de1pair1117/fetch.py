# de1pair1117(de1s_basket 짝 글) 원문 다시 받기 — 2026-11-17 firemap-write
#  ① 슈왑 SCHD 전체 보유 종목 CSV(Export All Holdings) ② 미래에셋 TIGER 미국배당다우존스 구성종목(운용사 ajax)
import pathlib, datetime, json, urllib.request
from playwright.sync_api import sync_playwright
RAW = pathlib.Path(__file__).resolve().parent / 'raw'; RAW.mkdir(exist_ok=True); D = datetime.date.today().strftime('%Y%m%d')
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
u = 'https://investments.miraeasset.com/tigeretf/ko/product/chart/prdct-item-list.ajax?ksdFund=KR7458730009'
try:
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA, 'Referer': 'https://investments.miraeasset.com/'}), timeout=40).read()
    (RAW / f'tiger_458730_items_{D}.json').write_bytes(r); print('TIGER items', len(r))
except Exception as e: print('TIGER ERR', str(e)[:200])
with sync_playwright() as p:
    b = p.chromium.launch(headless=False, args=["--window-position=-2000,0"])
    ctx = b.new_context(user_agent=UA, accept_downloads=True); pg = ctx.new_page()
    try:
        pg.goto('https://www.schwabassetmanagement.com/products/schd', timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("document.querySelectorAll('.ui-dialog,.ui-widget-overlay,#onetrust-banner-sdk').forEach(e=>e.remove())")
        (RAW / f'SCHD_page_{D}.txt').write_text(pg.inner_text('body'), encoding='utf-8')
        try: pg.get_by_text('Portfolio', exact=True).first.click(force=True, timeout=4000); pg.wait_for_timeout(3000)
        except Exception: pass
        with pg.expect_download(timeout=40000) as dl:
            pg.get_by_text('Export All Holdings').first.click(force=True)
        f = dl.value; f.save_as(str(RAW / f'schwab_SCHD_holdings_{D}.csv')); print('SCHD saved', f.suggested_filename)
    except Exception as e: print('SCHD ERR', str(e)[:200])
    b.close()
