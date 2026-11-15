import sys,time
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
U={'type':'DISISAJoinType.xml&divisionId=MDIS07002002000000&serviceId=SDIS07002002010',
   'asset':'DISISAAssetMgmtStat.xml&divisionId=MDIS07003001000000&serviceId=SDIS07003001000',
   'age':'DISISAAgeJoinStut.xml&divisionId=MDIS07002005000000&serviceId=SDIS07002005000',
   'amt':'DISISAMMJoinAmt.xml&divisionId=MDIS07002004000000&serviceId=SDIS07002004000'}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    for k,v in U.items():
        url='https://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/isa/'+v
        pg.goto(url, timeout=40000); pg.wait_for_timeout(5000)
        t=pg.inner_text('#main_content') if pg.query_selector('#main_content') else pg.inner_text('body')
        open(f'raw/kofia_{k}.txt','w',encoding='utf-8').write(f'# {url}\n# 받은 날 {time.strftime("%Y-%m-%d %H:%M")}\n\n{t}')
        print('=====',k,len(t)); print(t[:1800])
    b.close()
