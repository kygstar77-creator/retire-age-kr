# 신사업 사이트 실험 채점용 375 첫 화면 캡처 + 비교판 (firemap-venture 10/2) — py -3.12 cap.py
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
D = Path(__file__).parent; R = D.parent.parent / "design"
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
LIVE = {
 "xv1": "https://kygstar77-creator.github.io/uk-take-home-pay/?fm_internal=1",
 "xcn1": "https://kygstar77-creator.github.io/exam-dates-kr/hanneunggeom/?fm_internal=1",
 "tsc": "https://www.thesalarycalculator.co.uk/salary.php",
 "official": "https://m.historyexam.go.kr/main/examSchedule.do",
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 375, "height": 812}, device_scale_factor=2, user_agent=UA, locale="ko-KR")
        for k, u in LIVE.items():
            pg = await ctx.new_page()
            try:
                await pg.goto(u, wait_until="networkidle", timeout=45000); await pg.wait_for_timeout(1500)
                await pg.screenshot(path=str(D / f"{k}-375.png")); print("ok", k)
            except Exception as e: print("fail", k, e)
            await pg.close()
        await b.close()
asyncio.run(main())
F = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 36)
def board(name, items):
    ims = [(lab, Image.open(f).convert("RGB").resize((750, 1624))) for lab, f in items if Path(f).exists()]
    pad, top = 40, 70
    bd = Image.new("RGB", (len(ims)*(750+pad)+pad, 1624+top+pad), (230,230,230)); d = ImageDraw.Draw(bd)
    for i, (lab, im) in enumerate(ims):
        x = pad + i*(750+pad); bd.paste(im, (x, top)); d.text((x, 15), lab, fill=(200,0,0) if i == 0 else (0,0,0), font=F)
    bd.save(D / f"compare-{name}.png"); bd.resize((bd.width//3, bd.height//3)).save(D / f"compare-{name}-small.png"); print(name, bd.size)
tsc = D / "tsc-375.png"
board("xv1", [("우리: X-V1", D/"xv1-375.png"), ("1등: thesalarycalculator", tsc if tsc.exists() else R/"uk-pay/beat1/tsc-375-start.jpg"), ("1등 결과(£60k)", R/"uk-pay/beat1/tsc-375-60000.jpg"), ("기준: 토스", R/"quality/cap/toss-m.png")])
board("xcn1", [("우리: X-CN-1", D/"xcn1-375.png"), ("1등: 공식 누리집", D/"official-375.png"), ("구글 첫 화면", D.parent/"x-cn-1/shots/1002-google-serp.jpg"), ("기준: 토스", R/"quality/cap/toss-m.png")])
