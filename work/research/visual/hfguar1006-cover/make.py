# hfguar1006 카페 표지 시안 A·B·C — firemap-visual-designer 2026-10-06
# 숫자 출처: work/research/hfguar1006/calc.py (65세·4억 집·월 101만1천원 고정, 보증료 누계 만원)
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(H, '..', '..', '..', '..'))
F = os.path.join(ROOT, 'work', 'video', 'public', 'fonts').replace(os.sep, '/')
NEW = [410,433,468,518,582,661,756,868,998,1146,1315,1504,1716,1951,2210,2494,2807,3147,3518,3921]
OLD = [610,629,659,699,751,815,892,982,1086,1204,1339,1489,1656,1842,2046,2270,2515,2782,3073,3387]
CSS = f"""@font-face{{font-family:BH;src:url('file:///{F}/BlackHanSans.ttf')}}
@font-face{{font-family:PD;src:url('file:///{F}/pd700.ttf');font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1080px;background:#0F1B3D;color:#fff;font-family:PD;position:relative;overflow:hidden}}
.y{{color:#FFD43B}} .g{{color:#A5B4D4}}"""

def chart(x0, y0, w, h, big=True):
    mx = 4000
    px = lambda i: x0 + w * i / 19
    py = lambda v: y0 + h - h * v / mx
    pn = ' '.join(f'{px(i):.0f},{py(v):.0f}' for i, v in enumerate(NEW))
    po = ' '.join(f'{px(i):.0f},{py(v):.0f}' for i, v in enumerate(OLD))
    cx, cy = px(11), py(1497)
    return f"""<svg width=1080 height=1080 style="position:absolute;left:0;top:0">
<polyline points="{po}" fill=none stroke="#7C8DB5" stroke-width=12 stroke-linecap=round stroke-linejoin=round />
<polyline points="{pn}" fill=none stroke="#FFD43B" stroke-width=16 stroke-linecap=round stroke-linejoin=round />
<circle cx={cx:.0f} cy={cy:.0f} r=30 fill="#0F1B3D" stroke="#fff" stroke-width=9 />
<line x1={cx:.0f} y1={cy+34:.0f} x2={cx:.0f} y2={y0+h+6} stroke="#fff" stroke-width=4 stroke-dasharray="10 10"/>
<text x={px(19)+0:.0f} y={py(3921)-28:.0f} text-anchor=end font-family=PD font-weight=700 font-size=44 fill="#FFD43B">개편 후</text>
<text x={px(19):.0f} y={py(3387)+120:.0f} text-anchor=end font-family=PD font-weight=700 font-size=44 fill="#A5B4D4">개편 전</text>
<text x={x0:.0f} y={y0+h+64} font-family=PD font-weight=700 font-size=40 fill="#A5B4D4">받은 지 1년</text>
<text x={cx:.0f} y={y0+h+64} text-anchor=middle font-family=PD font-weight=700 font-size=40 fill="#fff">12년</text>
<text x={px(19):.0f} y={y0+h+64} text-anchor=end font-family=PD font-weight=700 font-size=40 fill="#A5B4D4">20년</text>
</svg>"""

A = f"""<style>{CSS}</style>
<div style="position:absolute;left:80px;top:80px;font-size:66px">주택연금 보증료 합계</div>
<div class=y style="position:absolute;left:76px;top:170px;font-family:BH;font-size:150px;line-height:1">12년째 역전</div>
{chart(110, 420, 860, 420)}
<div class=g style="position:absolute;left:80px;top:985px;font-size:34px">65세·4억 집 가정 · 금융위 2026.3 개편</div>"""

B = f"""<style>{CSS}</style>
<div style="position:absolute;left:80px;top:96px;font-size:70px">주택연금 새 보증료</div>
<div style="position:absolute;left:80px;top:250px;font-size:84px">20년 받으면</div>
<div class=y style="position:absolute;left:72px;top:360px;font-family:BH;font-size:230px;line-height:1">533만원</div>
<div class=y style="position:absolute;left:80px;top:610px;font-size:84px">더 붙어요</div>
<div style="position:absolute;left:80px;top:790px;width:920px;height:4px;background:#2B3A66"></div>
<div class=g style="position:absolute;left:80px;top:830px;font-size:56px">10년이면 58만원 덜</div>
<div class=g style="position:absolute;left:80px;top:985px;font-size:34px">65세·4억 집 · 개편 전과 비교</div>"""

def bar(x, v, top, col, lab, val):
    hh = v / 4000 * 520
    return (f'<div style="position:absolute;left:{x}px;top:{top+520-hh:.0f}px;width:150px;height:{hh:.0f}px;background:{col};border-radius:10px 10px 0 0"></div>'
            f'<div style="position:absolute;left:{x}px;width:150px;text-align:center;top:{top+520-hh-60:.0f}px;font-size:40px;color:{col}">{val}</div>'
            f'<div style="position:absolute;left:{x}px;width:150px;text-align:center;top:{top+540}px;font-size:36px;color:#A5B4D4">{lab}</div>')
T = 360
C = f"""<style>{CSS}</style>
<div style="position:absolute;left:80px;top:80px;font-size:66px">주택연금 보증료, 개편 뒤</div>
<div class=y style="position:absolute;left:76px;top:170px;font-family:BH;font-size:112px;line-height:1">오래 받으면 손해?</div>
{bar(110, 1204, T, '#7C8DB5', '개편 전', '1,204')}{bar(275, 1146, T, '#FFD43B', '개편 후', '1,146')}
{bar(600, 3387, T, '#7C8DB5', '개편 전', '3,387')}{bar(765, 3921, T, '#FFD43B', '개편 후', '3,921')}
<div style="position:absolute;left:110px;width:315px;text-align:center;top:{T+600}px;font-size:48px">10년</div>
<div style="position:absolute;left:600px;width:315px;text-align:center;top:{T+600}px;font-size:48px">20년</div>
<div class=g style="position:absolute;left:80px;top:1010px;font-size:30px">보증료 합계(만원) · 65세·4억 집 가정</div>"""

B2 = f"""<style>{CSS}</style>
<div style="position:absolute;left:80px;top:90px;font-size:74px">주택연금 새 보증료</div>
<div style="position:absolute;left:80px;top:240px;font-size:88px">20년 받으면 총</div>
<div class=y style="position:absolute;left:72px;top:350px;font-family:BH;font-size:240px;line-height:1">533만원</div>
<div class=y style="position:absolute;left:80px;top:610px;font-size:88px">더 붙어요</div>
<div style="position:absolute;left:80px;top:780px;width:920px;height:4px;background:#2B3A66"></div>
<div style="position:absolute;left:80px;top:820px;font-size:70px;color:#C9D4EE">10년이면 58만원 덜</div>
<div class=g style="position:absolute;left:80px;top:975px;font-size:40px">65세·4억 집 · 개편 전과 비교</div>"""
B3 = f"""<style>{CSS}</style>
<div style="position:absolute;left:80px;top:90px;font-size:74px">주택연금 새 보증료</div>
<div style="position:absolute;left:80px;top:220px;font-size:84px">빚에 붙는 보증료 합계</div>
<div class=y style="position:absolute;left:72px;top:340px;font-family:BH;font-size:240px;line-height:1">+533만</div>
<div class=y style="position:absolute;left:80px;top:600px;font-size:88px">20년 받으면</div>
<div style="position:absolute;left:80px;top:780px;width:920px;height:4px;background:#2B3A66"></div>
<div style="position:absolute;left:80px;top:820px;font-size:70px;color:#C9D4EE">10년이면 58만원 덜</div>
<div class=g style="position:absolute;left:80px;top:975px;font-size:40px">65세·4억 집 · 개편 전과 비교</div>"""

def Avar(top, head, hs=150):
    return f"""<style>{CSS}</style>
<div style="position:absolute;left:80px;top:80px;font-size:66px">{top}</div>
<div class=y style="position:absolute;left:76px;top:170px;font-family:BH;font-size:{hs}px;line-height:1">{head}</div>
{chart(110, 440, 860, 400)}
<div class=g style="position:absolute;left:80px;top:975px;font-size:42px">65세·4억 집 가정 · 개편 전과 비교</div>"""
A2 = Avar('빚에 붙는 주택연금 보증료', '12년째부터 손해', 128)
A3 = Avar('빚에 붙는 보증료, 개편 뒤', '12년째부터 더', 140)

A4 = (f"""<style>{CSS}</style>
<div style="position:absolute;left:80px;top:80px;font-size:70px">주택연금 새 보증료</div>
<div style="position:absolute;left:76px;top:175px;font-family:BH;font-size:150px;line-height:1;color:#FF6B6B">12년째부터 손해</div>
""" + chart(110, 450, 860, 420).replace('#FFD43B', '#FF6B6B').replace('개편 후', '새 보증료').replace('개편 전', '옛 보증료').replace('받은 지 1년', '1년'))

A5 = A2.replace('stroke="#FFD43B"', 'stroke="#FF6B6B"').replace('fill="#FFD43B">개편 후', 'fill="#FF6B6B">개편 후')

A6 = (f"""<style>{CSS}</style>
<div style="position:absolute;left:80px;top:70px;font-family:BH;font-size:110px;line-height:1">주택연금 보증료</div>
<div class=y style="position:absolute;left:76px;top:200px;font-family:BH;font-size:128px;line-height:1">12년째부터 손해</div>
""" + chart(110, 460, 860, 380).replace('stroke="#FFD43B"', 'stroke="#FF6B6B"').replace('fill="#FFD43B">개편 후', 'fill="#FF6B6B">개편 후') +
"""<div class=g style="position:absolute;left:80px;top:975px;font-size:42px">빚에 더해지는 돈 · 65세·4억 집 가정</div>""")

A7 = (f"""<style>{CSS}</style>
<div style="position:absolute;left:80px;top:72px;font-size:78px">빚에 붙는 주택연금 보증료</div>
<div class=y style="position:absolute;left:76px;top:190px;font-family:BH;font-size:118px;line-height:1">12년째부터 더 쌓여요</div>
""" + chart(110, 450, 860, 400) +
"""<div class=g style="position:absolute;left:80px;top:975px;font-size:42px">65세·4억 집 가정 · 11년까진 덜 쌓임</div>""")

A8 = A7.replace('빚에 붙는 주택연금 보증료', '대출에 붙는 주택연금 보증료')

def diffchart(x0, y0, w, h):
    D = [n - o for n, o in zip(NEW, OLD)]  # 개편 후 - 개편 전 (만원)
    lo, hi = -250, 600
    px = lambda i: x0 + w * i / 19
    py = lambda v: y0 + h * (hi - v) / (hi - lo)
    pts = ' '.join(f'{px(i):.0f},{py(v):.0f}' for i, v in enumerate(D))
    z = py(0)
    neg = ' '.join(f'{px(i):.0f},{py(min(v,0)):.0f}' for i, v in enumerate(D))
    pos = ' '.join(f'{px(i):.0f},{py(max(v,0)):.0f}' for i, v in enumerate(D))
    return f"""<svg width=1080 height=1080 style="position:absolute;left:0;top:0">
<polygon points="{px(0):.0f},{z:.0f} {neg} {px(19):.0f},{z:.0f}" fill="#4C6FBF" opacity=.55 />
<polygon points="{px(0):.0f},{z:.0f} {pos} {px(19):.0f},{z:.0f}" fill="#FF6B6B" opacity=.85 />
<line x1={x0} y1={z:.0f} x2={x0+w} y2={z:.0f} stroke="#fff" stroke-width=5 />
<polyline points="{pts}" fill=none stroke="#fff" stroke-width=8 stroke-linejoin=round />
<text x={px(19):.0f} y={py(533)-22:.0f} text-anchor=end font-family=BH font-size=76 fill="#FF6B6B">+533만</text>
<text x={px(0)+10:.0f} y={z-24:.0f} font-family=BH font-size=64 fill="#9DB4EE">-199만</text>
<text x={px(11):.0f} y={z+56:.0f} text-anchor=middle font-family=PD font-weight=700 font-size=44 fill="#fff">12년</text>
<text x={px(19):.0f} y={y0+h+60:.0f} text-anchor=end font-family=PD font-weight=700 font-size=40 fill="#A5B4D4">20년</text>
<text x={px(0):.0f} y={y0+h+60:.0f} font-family=PD font-weight=700 font-size=40 fill="#A5B4D4">1년</text>
</svg>"""
A9 = (f"""<style>{CSS}</style>
<div style="position:absolute;left:80px;top:72px;font-size:78px">대출에 붙는 주택연금 보증료</div>
<div class=y style="position:absolute;left:76px;top:190px;font-family:BH;font-size:110px;line-height:1">12년째부터 더 쌓여요</div>
""" + diffchart(110, 400, 860, 470) +
"""<div class=g style="position:absolute;left:80px;top:985px;font-size:40px">개편 전과 차이 · 65세·4억 집 가정</div>""")

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080})
    for n, html in (('A', A), ('B', B), ('C', C), ('B2', B2), ('B3', B3), ('A2', A2), ('A3', A3), ('A4', A4), ('A5', A5), ('A6', A6), ('A7', A7), ('A8', A8), ('A9', A9)):
        hp=os.path.join(H, f'cover_{n}.html'); open(hp,'w',encoding='utf-8').write('<meta charset=utf-8>'+html); pg.goto('file:///'+hp.replace(os.sep,'/')); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
        out = os.path.join(H, f'cover_{n}.png'); pg.screenshot(path=out)
    b.close()
from PIL import Image
ims = [Image.open(os.path.join(H, f'cover_{n}.png')) for n in 'ABC']
s = Image.new('RGB', (168*3+40, 208), '#FFFFFF')
for i, im in enumerate(ims): s.paste(im.resize((168, 168), Image.LANCZOS), (10 + i*178, 20))
s.save(os.path.join(H, 'small168.png'))
print('ok')
