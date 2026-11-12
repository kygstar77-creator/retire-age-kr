# 공지 본문 그림을 원본 그대로 저장(본문이 이미지라 글자로 안 읽힘)
import sys
from playwright.sync_api import sync_playwright
url, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 900, 'height': 1200})
    pg.goto(url, wait_until='networkidle', timeout=60000); pg.wait_for_timeout(2000)
    imgs = pg.locator('img').evaluate_all("els=>els.filter(e=>e.naturalHeight>400).map(e=>e.src)")
    print(imgs)
    for i, s in enumerate(imgs[:3]):
        r = pg.request.get(s); open(f'{out}_{i}.png', 'wb').write(r.body())
    b.close()
