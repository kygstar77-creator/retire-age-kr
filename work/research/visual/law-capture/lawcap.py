# 국가법령정보센터 조문 원문 캡처 (2026-11-09 visual — today.md 지시: 표지에 조문 이름 단 카페 글은 본문 그림 1장을 원문 캡처로)
# 실행: PYTHONIOENCODING=utf-8 py -3.12 lawcap.py <법령명> <제N조> <out.png> [강조할 낱말 ...]
# law.go.kr/법령/<법>/<조> 페이지의 조문 본문 프레임(lsSideInfoP)을 그대로 찍는다. 글자는 손대지 않고 강조 낱말만 노란 형광펜.
import sys, urllib.parse, time
from playwright.sync_api import sync_playwright
law, jo, out = sys.argv[1], sys.argv[2], sys.argv[3]
marks = sys.argv[4:]
u = "https://www.law.go.kr/" + urllib.parse.quote(f"법령/{law}/{jo}")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 900, "height": 1400}, device_scale_factor=1.5, locale="ko-KR")
    pg.goto(u, wait_until="networkidle", timeout=60000)
    time.sleep(2)
    fr = next((f for f in pg.frames if "lsSideInfoP" in f.url), None)
    tgt = fr if fr else pg
    if marks:
        tgt.evaluate("""(ws)=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);const ns=[];while(w.nextNode())ns.push(w.currentNode);
        for(const n of ns){for(const m of ws){const i=n.nodeValue.indexOf(m);if(i<0)continue;const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+m.length);
        const s=document.createElement('mark');s.style.background='#FFE14D';s.style.padding='0 1px';try{r.surroundContents(s);}catch(e){};break;}}}""", marks)
    if fr:
        el = pg.frame_locator('iframe[src*="lsSideInfoP"], iframe').first.locator("body")
        el.screenshot(path=out)
    else:
        pg.screenshot(path=out, full_page=True)
    print(u, "frame" if fr else "page", out)
    b.close()
