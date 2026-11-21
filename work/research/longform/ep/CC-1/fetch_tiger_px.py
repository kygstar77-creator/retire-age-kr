# 미래에셋 TIGER 458730 상품 상세의 '기준가·시장가격' 표 요청 꼴 잡기(price.ajax 폼 값) — youtube-loop 2026-11-22
import json
from playwright.sync_api import sync_playwright
reqs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.on('request', lambda r: reqs.append({'url':r.url,'post':r.post_data}) if 'price.ajax' in r.url or 'profit' in r.url else None)
    res=[]
    pg.on('response', lambda r: res.append({'url':r.url,'body':r.text()[:20000]}) if 'price.ajax' in r.url else None)
    pg.goto('https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008',timeout=60000)
    pg.wait_for_load_state('networkidle',timeout=60000); pg.wait_for_timeout(4000)
    print(json.dumps(reqs,ensure_ascii=False)[:1500])
    for x in res: print(x['url'], x['body'][:300].replace('\n',' '))
    b.close()
