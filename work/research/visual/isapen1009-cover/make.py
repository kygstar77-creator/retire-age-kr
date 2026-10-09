# isapen1009 카페 표지 J안 — 글자만 있던 I1~I10 공통 지적(흐름 그림 없음) 고침: ISA→연금 화살표 도식 + 숫자 2개(한도 +300만원 / 환급 0원)
# 숫자 출처: pkg/facts.txt 14줄(제59조의3④ min(10%,300만원)), 제목 L2(소득 없는 해엔 환급 0원). 결과는 ../../isapen1009/covers_try/00_J*.png·board_J*.png
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); C = os.path.normpath(os.path.join(D, '..', '..', 'isapen1009', 'covers_try'))
FT = Path(os.path.normpath(os.path.join(D, '..', '..', '..', 'video', 'public', 'fonts'))).as_uri()
CSS = """@font-face{font-family:P;src:url(%(ft)s/pd700.ttf)}@font-face{font-family:B;src:url(%(ft)s/BlackHanSans.ttf)}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1080px;background:%(bg)s;font-family:P;overflow:hidden;position:relative}
.flow{position:absolute;left:70px;right:70px;top:80px;height:230px;display:flex;align-items:center;justify-content:space-between}
.box{width:330px;height:210px;border-radius:36px;display:flex;align-items:center;justify-content:center;font-family:B;font-size:120px}
.arr{flex:1;height:210px;display:flex;align-items:center;justify-content:center}
.big{position:absolute;white-space:nowrap;left:60px;right:60px;text-align:center;font-family:B;line-height:1}
.src{position:absolute;left:0;right:0;bottom:44px;text-align:center;font-size:30px;opacity:.75}
"""
ARROW = '<svg width="230" height="120" viewBox="0 0 230 120"><path d="M10 60H175" stroke="%s" stroke-width="26" stroke-linecap="round"/><path d="M150 14L218 60L150 106" fill="none" stroke="%s" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SRC = '소득세법 제59조의3'
V = {
 # 노랑 바탕: 위 도식, 가운데 '한도 +300만원'(남색), 아래 '소득 없으면 환급 0원'(빨강)
 'J1': dict(bg='#FFD43B', fg='#0F1B3D', b1=('#0F1B3D', '#FFD43B'), b2=('#FFFFFF', '#0F1B3D'),
            rows=[('한도 +300만원', 150, '#0F1B3D', 400), ('소득 없는 해엔', 96, '#0F1B3D', 600), ('환급 0원', 190, '#D7261E', 720)]),
 # 남색 바탕: 같은 구성, 0원을 노랑
 'J2': dict(bg='#0F1B3D', fg='#FFFFFF', b1=('#FFFFFF', '#0F1B3D'), b2=('#FFD43B', '#0F1B3D'),
            rows=[('한도 +300만원', 150, '#FFFFFF', 400), ('소득 없는 해엔', 96, '#A5B4D4', 600), ('환급 0원', 190, '#FFD43B', 720)]),
 # 노랑 바탕, 대비 2줄: '한도 ↑300만' vs '환급 0원' 좌우 아닌 위아래 큰 두 줄만(글자 수 최소)
 'J3': dict(bg='#FFD43B', fg='#0F1B3D', b1=('#0F1B3D', '#FFD43B'), b2=('#FFFFFF', '#0F1B3D'),
            rows=[('한도는 +300만', 160, '#0F1B3D', 400), ('환급은 0원', 200, '#D7261E', 640)]),
 # J2 고침: '소득 없는 해엔' 조건을 96→124px 흰 글자로 키움(심사 2명 '안 읽힘'), 한도 줄은 140으로
 'J4': dict(bg='#0F1B3D', fg='#FFFFFF', b1=('#FFFFFF', '#0F1B3D'), b2=('#FFD43B', '#0F1B3D'),
            rows=[('한도 +300만원', 136, '#A5B4D4', 380), ('소득 없는 해엔', 124, '#FFFFFF', 560), ('환급 0원', 200, '#FFD43B', 730)]),
 # 레드팀 처방(J1 7.3·J2 7.0): 상한 '최대' 밝힘 + 조건을 결론에 붙여 굵게, 노랑 바탕, 아래 법조문 줄 뺌
 'J5': dict(bg='#FFD43B', fg='#0F1B3D', b1=('#0F1B3D', '#FFD43B'), b2=('#FFFFFF', '#0F1B3D'), nosrc=1,
            rows=[('한도 최대 +300만원', 118, '#0F1B3D', 390), ('소득 없는 해엔', 140, '#0F1B3D', 570), ('환급 0원', 210, '#D7261E', 760)]),
 # J2 + 레드팀 오독 처방 최소분: 조건 '소득 없는 해엔'을 회청→흰색·104px, 크기 순서는 그대로
 'J6': dict(bg='#0F1B3D', fg='#FFFFFF', b1=('#FFFFFF', '#0F1B3D'), b2=('#FFD43B', '#0F1B3D'),
            rows=[('한도 +300만원', 150, '#FFFFFF', 400), ('소득 없는 해엔', 104, '#FFFFFF', 598), ('환급 0원', 190, '#FFD43B', 724)]),
}
def html(v):
    rows = ''.join(f'<div class="big" style="top:{t}px;font-size:{s}px;color:{c}">{x}</div>' for x, s, c, t in v['rows'])
    return (f'<html><head><meta charset="utf-8"><style>{CSS % dict(ft=FT, bg=v["bg"])}</style></head><body>'
            f'<div class="flow"><div class="box" style="background:{v["b1"][0]};color:{v["b1"][1]}">ISA</div>'
            f'<div class="arr">{ARROW % (v["fg"], v["fg"])}</div>'
            f'<div class="box" style="background:{v["b2"][0]};color:{v["b2"][1]}">연금</div></div>'
            f'{rows}' + ('' if v.get('nosrc') else f'<div class="src" style="color:{v["fg"]}">{SRC}</div>') + '</body></html>')
names = sys.argv[1:] or list(V)
S = 110; F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 12)
comp = json.load(open(os.path.join(C, 'comp', 'comp.json'), encoding='utf-8'))['files'][:5]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080})
    for n in names:
        h = os.path.join(D, n + '.html'); open(h, 'w', encoding='utf-8').write(html(V[n]))
        pg.goto(Path(h).as_uri()); pg.evaluate('document.fonts.ready')
        box = pg.evaluate("[...document.querySelectorAll('.big,.flow')].map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.right),Math.round(r.bottom),e.scrollWidth>e.clientWidth]})")
        for bx in box: assert bx[0] >= 40 and bx[1] <= 1040 and bx[2] <= 1040 and not bx[3], (n, bx)
        out = os.path.join(C, f'00_{n}.png'); pg.screenshot(path=out)
        Image.open(out).resize((168, 168), Image.LANCZOS).save(os.path.join(C, f'00_{n}_168.png'))
        items = [('우리 새 표지', out)] + [(f'경쟁 {i+1}', os.path.join(C, 'comp', c)) for i, c in enumerate(comp)]
        pad = 12; bd = Image.new('RGB', (len(items) * (S + pad) + pad, S + 2 * pad + 20), 'white'); d = ImageDraw.Draw(bd)
        for i, (lab, pp) in enumerate(items):
            im = Image.open(pp).convert('RGB'); w, hh = im.size; m = min(w, hh)
            im = im.crop(((w - m) // 2, (hh - m) // 2, (w - m) // 2 + m, (hh - m) // 2 + m)).resize((S, S), Image.LANCZOS)
            x = pad + i * (S + pad); bd.paste(im, (x, pad)); d.text((x, pad + S + 4), lab, fill='black', font=F)
        bd.save(os.path.join(C, f'board_{n}.png')); print(n, 'ok')
    b.close()
