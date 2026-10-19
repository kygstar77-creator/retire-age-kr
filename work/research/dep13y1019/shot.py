from playwright.sync_api import sync_playwright
U={'c1':'https://m.blog.naver.com/imhogun/224374817734','c3':'https://m.blog.naver.com/hublessing100/224433921215'}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':420,'height':900},user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)')
    for k,u in U.items():
        pg.goto(u,timeout=40000); pg.wait_for_timeout(2500)
        imgs=pg.query_selector_all('img.se-image-resource, .se-module-image img')
        print(k,len(imgs))
        for i,im in enumerate(imgs[:3]):
            try: im.scroll_into_view_if_needed(); pg.wait_for_timeout(600); im.screenshot(path=f'bench_shots/{k}_{i}.png')
            except Exception as e: print(e)
    b.close()
