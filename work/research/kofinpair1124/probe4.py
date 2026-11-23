# ACE 구성종목(PDF) 탭 · RISE 상품 찾기 (firemap-write-b 2026-11-23)
import sys, json, pathlib
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
R = pathlib.Path(__file__).resolve().parent / 'raw'
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(user_agent=UA, viewport={'width': 1400, 'height': 1000})
    got = {}
    def on(r):
        if 'json' in (r.headers.get('content-type') or '') and ('papi' in r.url or 'kbam.co.kr/api' in r.url):
            try: got[r.url] = r.text()
            except Exception: pass
    ctx.on('response', on)
    q = ctx.new_page(); q.goto('https://www.aceetf.co.kr/fund/K55101EQ7660', timeout=60000); q.wait_for_timeout(6000)
    try: q.get_by_text('구성종목(PDF)', exact=True).first.click(timeout=5000); q.wait_for_timeout(5000)
    except Exception as e: print('ace click', str(e)[:100])
    (R / 'pw' / 'ace_0139P0_pdf.txt').write_text(q.inner_text('body'), encoding='utf-8')
    q2 = ctx.new_page(); q2.goto('https://kbam.co.kr/find', timeout=60000); q2.wait_for_timeout(5000)
    try:
        box = q2.locator('input').first; box.click(); box.fill('대형고배당'); box.press('Enter'); q2.wait_for_timeout(6000)
    except Exception as e: print('rise search', str(e)[:100])
    links = q2.evaluate("Array.from(document.querySelectorAll('a')).map(a=>[a.href,a.innerText.slice(0,40)])")
    print([l for l in links if '고배당' in l[1]][:10])
    for u, t in got.items(): print('   ', u[:170], len(t))
    json.dump(got, open(R / 'pw' / 'probe4_api.json', 'w', encoding='utf-8'), ensure_ascii=False)
    b.close()
