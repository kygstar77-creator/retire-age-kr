# hfguar1006 표지 A9 한 수 시험 — firemap-write 2026-10-06 02:5x. 그래프는 visual-designer A9(diffchart) 그대로, 숫자 calc.py
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, 'covers_try')
ROOT = os.path.abspath(os.path.join(H, '..', '..', '..'))
F = os.path.join(ROOT, 'work', 'video', 'public', 'fonts').replace(os.sep, '/')
NEW = [410,433,468,518,582,661,756,868,998,1146,1315,1504,1716,1951,2210,2494,2807,3147,3518,3921]
OLD = [610,629,659,699,751,815,892,982,1086,1204,1339,1489,1656,1842,2046,2270,2515,2782,3073,3387]
CSS = f"""@font-face{{font-family:BH;src:url('file:///{F}/BlackHanSans.ttf')}}
@font-face{{font-family:PD;src:url('file:///{F}/pd700.ttf');font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1080px;background:#0F1B3D;color:#fff;font-family:PD;position:relative;overflow:hidden}}
.y{{color:#FFD43B}} .g{{color:#A5B4D4}}"""
def diffchart(x0, y0, w, h, lab533='+533만', lab199='-199만', l1='1년'):
    D = [n - o for n, o in zip(NEW, OLD)]
    lo, hi = -250, 600
    px = lambda i: x0 + w * i / 19
    py = lambda v: y0 + h * (hi - v) / (hi - lo)
    pts = ' '.join(f'{px(i):.0f},{py(v):.0f}' for i, v in enumerate(D)); z = py(0)
    neg = ' '.join(f'{px(i):.0f},{py(min(v,0)):.0f}' for i, v in enumerate(D))
    pos = ' '.join(f'{px(i):.0f},{py(max(v,0)):.0f}' for i, v in enumerate(D))
    return f"""<svg width=1080 height=1080 style="position:absolute;left:0;top:0">
<polygon points="{px(0):.0f},{z:.0f} {neg} {px(19):.0f},{z:.0f}" fill="#4C6FBF" opacity=.55 />
<polygon points="{px(0):.0f},{z:.0f} {pos} {px(19):.0f},{z:.0f}" fill="#FF6B6B" opacity=.85 />
<line x1={x0} y1={z:.0f} x2={x0+w} y2={z:.0f} stroke="#fff" stroke-width=5 />
<polyline points="{pts}" fill=none stroke="#fff" stroke-width=8 stroke-linejoin=round />
<text x={px(19):.0f} y={py(533)-22:.0f} text-anchor=end font-family=BH font-size=76 fill="#FF6B6B">{lab533}</text>
<text x={px(0)+10:.0f} y={z-24:.0f} font-family=BH font-size=64 fill="#9DB4EE">{lab199}</text><text x={px(0):.0f} y={y0+h+60:.0f} font-family=PD font-weight=700 font-size=40 fill="#A5B4D4">{l1}</text>
<text x={px(11):.0f} y={z+56:.0f} text-anchor=middle font-family=PD font-weight=700 font-size=44 fill="#fff">12년</text>
<text x={px(19):.0f} y={y0+h+60:.0f} text-anchor=end font-family=PD font-weight=700 font-size=40 fill="#A5B4D4">20년</text>

</svg>"""
V = {
 'A22': f"""<style>{CSS}</style><div style="position:absolute;left:80px;top:72px;font-size:84px">주택연금 보증료 개편 후</div>
<div class=y style="position:absolute;left:76px;top:190px;font-family:BH;font-size:90px;line-height:1">12년부터 대출에 더 붙어요</div>""" + diffchart(110, 400, 860, 450, '+533만', '-199만', '1년') + '''<div class=g style="position:absolute;left:80px;top:975px;font-size:48px">개편 전과 비교 · 65세·4억 집 가정</div>''',
 'A23': f"""<style>{CSS}</style><div style="position:absolute;left:80px;top:72px;font-size:84px">주택연금 보증료, 개편 후엔</div>
<div class=y style="position:absolute;left:76px;top:190px;font-family:BH;font-size:92px;line-height:1">12년부터 대출이 더 불어요</div>""" + diffchart(110, 400, 860, 450, '+533만', '-199만', '1년') + '''<div class=g style="position:absolute;left:80px;top:975px;font-size:48px">개편 전과 비교 · 65세·4억 집 가정</div>''',
}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080})
    for n, html in V.items():
        hp = os.path.join(OUT, f'cover_{n}.html'); open(hp, 'w', encoding='utf-8').write('<meta charset=utf-8>' + html)
        pg.goto('file:///' + hp.replace(os.sep, '/')); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(OUT, f'00_{n}.png')); os.remove(hp)
    b.close()
from PIL import Image
for n in V: Image.open(os.path.join(OUT, f'00_{n}.png')).resize((168,168), Image.LANCZOS).save(os.path.join(OUT, f's168_{n}.png'))
print('ok')
