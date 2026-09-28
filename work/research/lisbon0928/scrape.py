import sys,io,json
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
from playwright.sync_api import sync_playwright
out=[]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    pg=b.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36",locale="en-GB")
    pg.goto("https://www.idealista.pt/en/arrendar-casas/lisboa/campo-de-ourique/",timeout=60000,wait_until="domcontentloaded"); pg.wait_for_timeout(5000)
    for art in pg.query_selector_all("article.item"):
        a=art.query_selector("a.item-link")
        out.append({"href":"https://www.idealista.pt"+(a.get_attribute("href") if a else ""),"text":art.inner_text()})
    b.close()
json.dump(out,open("list.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for o in out: print(o["href"]); print(o["text"].replace("\n"," | ")[:400]); print()
