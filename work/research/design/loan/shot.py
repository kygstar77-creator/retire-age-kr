# 대출 v1 시안 캡처 + 비교판 (우리 375 | 우리 375 #b | 네이버 | 부동산계산기 | 핀다 | 금감원 | 토스)
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
D = Path(__file__).resolve().parent; Q = D.parent / "quality"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for tag, vp, sc, scheme, h in (("375", {"width":375,"height":812}, 2, "light", ""), ("375-b", {"width":375,"height":812}, 2, "light", "#b"), ("375-dark", {"width":375,"height":812}, 2, "dark", ""), ("1280", {"width":1280,"height":800}, 1, "light", ""), ("320", {"width":320,"height":568}, 2, "light", "")):
            ctx = await b.new_context(viewport=vp, device_scale_factor=sc, color_scheme=scheme)
            pg = await ctx.new_page(); await pg.goto((D/"preview.html").as_uri() + h); await pg.wait_for_timeout(1500)
            sw = await pg.evaluate("document.documentElement.scrollWidth")
            cta = await pg.evaluate("document.querySelector('.cta a').getBoundingClientRect().bottom")
            await pg.screenshot(path=str(D/f"v1-{tag}.png"))
            if tag == "375": await pg.screenshot(path=str(D/"v1-375-full.png"), full_page=True)
            print(tag, "scrollWidth", sw, "cta bottom", round(cta)); await ctx.close()
        await b.close()
asyncio.run(main())
F = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 36)
C = D / "cap"
items = [("우리 v1", D/"v1-375.png"), ("우리 v1 (저장값 있음)", D/"v1-375-b.png"), ("네이버 위젯", C/"naver-375.png"), ("부동산계산기.com", C/"budongsan-375.png"),
         ("핀다", C/"finda-375.png"), ("금감원 파인", C/"fss-375.png"), ("기준: 토스", Q/"cap"/"toss-m.png")]
ims = []
for lab, f in items:
    if not f.exists(): print("빠짐", f); continue
    im = Image.open(f).convert("RGB"); w = 750; hh = int(im.height * w / im.width)
    ims.append((lab, im.resize((w, hh)).crop((0, 0, w, 1624))))
pad, top = 40, 70
board = Image.new("RGB", (len(ims)*(750+pad)+pad, 1624+top+pad), (230,230,230)); d = ImageDraw.Draw(board)
for i, (lab, im) in enumerate(ims):
    x = pad + i*(750+pad); board.paste(im, (x, top)); d.text((x, 15), lab, fill=(200,0,0) if i < 2 else (0,0,0), font=F)
board.save(D/"compare-v1.png"); board.resize((board.width//3, board.height//3)).save(D/"compare-v1-small.png"); print("칸", len(ims), board.size)
