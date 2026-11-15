# 은행연합회 소비자포털 금리인하요구권 비교공시 — 반기별 전체 은행 표 받기(firemap-write 11/15)
import sys, re, json
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for y, h in [('2026','1'), ('2025','2'), ('2025','1')]:
        pg.goto('https://portal.kfb.or.kr/compare/loan_reduce_new.php', timeout=40000)
        pg.check('#BankAll')
        pg.select_option('#year', y); pg.select_option('#month', h)
        pg.evaluate("LoanReduceSearch()")
        pg.wait_for_timeout(4000)
        rows = pg.eval_on_selector_all('#SearchResult table tr', 'trs=>trs.map(t=>Array.from(t.querySelectorAll("th,td")).map(c=>c.innerText.trim()))')
        out[f'{y}-{h}'] = rows
        open(f'raw/kfb_{y}_{h}.html','w',encoding='utf-8').write(pg.content())
        print(y, h, len(rows)); [print(r) for r in rows[:30]]
    b.close()
json.dump(out, open('raw/kfb_tables.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
