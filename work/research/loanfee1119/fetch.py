# 은행연합회 소비자포털 가계대출금리 비교공시 — 분할상환 주담대·일반신용대출, 신규취급액 기준, 상세(기준·가산·가감조정) 월별 (firemap-write 11/18)
import sys, json
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
out={}
months=[(sys.argv[1],m) for m in sys.argv[2].split(',')] if len(sys.argv)>2 else [('2026','06'),('2026','10')]
prods=sys.argv[3].split(',') if len(sys.argv)>3 else ['1','3']
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    for y,m in months:
        for o in prods:
            pg.goto('https://portal.kfb.or.kr/compare/loan_household_new.php',timeout=40000)
            pg.check('#BankAll')
            pg.evaluate(f"""()=>{{document.querySelector('#year').value='{y}';document.querySelector('#month').value='{m}';
              document.querySelector('#select_new_balance_1').checked=true;document.querySelector('#opt_1_{o}').checked=true;document.querySelector('#all_show_1').checked=true;}}""")
            pg.evaluate("LoanHouseholdNewSearch_cur()")
            pg.wait_for_timeout(4500)
            rows=pg.eval_on_selector_all('table tr','trs=>trs.map(t=>Array.from(t.querySelectorAll("th,td")).map(c=>c.innerText.trim()))')
            rows=[[' '.join(c.split()) for c in r] for r in rows]
            rows=[r for r in rows if r]
            out[f'{y}-{m}-p{o}']=rows
            open(f'raw/hh_{y}{m}_p{o}.html','w',encoding='utf-8').write(pg.content())
            print('==',y,m,o,len(rows)); [print(r) for r in rows[:30]]
    b.close()
json.dump(out,open(f'raw/hh_{"_".join(y+m for y,m in months)}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
