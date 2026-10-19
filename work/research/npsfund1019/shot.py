import json
from playwright.sync_api import sync_playwright
U={'c1':'https://m.blog.naver.com/skmfood/224446155048','c2':'https://m.blog.naver.com/absung35/224445972817','c6':'https://m.blog.naver.com/bareumlab/224446672425'}
out={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':420,'height':900},user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)')
    for k,u in U.items():
        pg.goto(u,timeout=40000); pg.wait_for_timeout(3000)
        txt=pg.inner_text('body')
        imgs=pg.query_selector_all('img.se-image-resource, .se-module-image img')
        r={}
        for lab in ('공감','댓글'):
            el=pg.query_selector(f'.u_likeit_text._count, .u_cnt._count') 
        r['body_head']=txt[:200]; r['imgs']=len(imgs)
        import re
        m=re.findall(r'(공감|댓글)\s*(\d+)',txt); r['react']=m[:4]
        out[k]=r; print(k,len(imgs),m[:4])
        for i,im in enumerate(imgs[:3]):
            try: im.scroll_into_view_if_needed(); pg.wait_for_timeout(600); im.screenshot(path=f'bench_shots/{k}_{i}.png')
            except Exception as e: print(e)
    b.close()
json.dump(out,open('bench_shots/meta.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
