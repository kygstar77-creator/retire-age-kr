# D-ETF-1 운용사 원문 받기(브라우저로만 열리는 곳): 페이지 글자 + 페이지가 부른 JSON 응답을 raw/에 남긴다.
#   py -3.12 fetch_pw.py SCHD VYM VIG JEPI JEPQ DIVO
import sys, json, re, pathlib, datetime
from playwright.sync_api import sync_playwright
RAW = pathlib.Path(__file__).resolve().parent / 'raw'; D = datetime.date.today().strftime('%Y%m%d')
PAGES = {
  'SCHD': ['https://www.schwabassetmanagement.com/products/schd'],
  'VYM': ['https://investor.vanguard.com/investment-products/etfs/profile/vym#portfolio-composition'],
  'VIG': ['https://investor.vanguard.com/investment-products/etfs/profile/vig#portfolio-composition'],
  'JEPI': ['https://am.jpmorgan.com/us/en/asset-management/adv/products/jpmorgan-equity-premium-income-etf-etf-shares-46641q332'],
  'JEPQ': ['https://am.jpmorgan.com/us/en/asset-management/adv/products/jpmorgan-nasdaq-equity-premium-income-etf-etf-shares-46654q203'],
  'DIVO': ['https://amplifyetfs.com/divo/'],
}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
with sync_playwright() as p:
    b = p.chromium.launch(headless=False, args=["--window-position=-2000,0"])
    for t in sys.argv[1:]:
        for url in PAGES[t]:
            pg = b.new_page(user_agent=UA); got = []
            def on(r):
                try:
                    ct = r.headers.get('content-type', '')
                    if ('json' in ct or r.url.endswith('.csv')) and r.status == 200:
                        got.append({'url': r.url, 'body': r.text()[:400000]})
                except Exception: pass
            pg.on('response', on)
            try:
                pg.goto(url, timeout=90000); pg.wait_for_timeout(9000)
                pg.evaluate("document.querySelectorAll('.ui-dialog,.ui-widget-overlay,#onetrust-banner-sdk').forEach(e=>e.remove())")
                for lab in ('Portfolio', 'Holdings', 'Portfolio composition', 'Distributions'):
                    try: pg.get_by_text(lab, exact=True).first.click(force=True, timeout=3000); pg.wait_for_timeout(4000)
                    except Exception: pass
                (RAW / f'{t}_page_{D}.txt').write_text(pg.inner_text('body'), encoding='utf-8')
            except Exception as e:
                print(t, 'ERR', str(e)[:120])
            (RAW / f'{t}_net_{D}.json').write_text(json.dumps(got, ensure_ascii=False), encoding='utf-8')
            print(t, 'json', len(got), [g['url'][:90] for g in got][:12])
            pg.close()
    b.close()
