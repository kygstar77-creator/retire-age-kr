# eitclate1009 카페 표지 K안 — G3~G17 글자만 판이 6.5에서 멈춤 → 하루 차이(11/30·12/1)와 지급 기한(3/30·4/30) 두 줄 비교 도식
# 숫자 출처: pkg/facts.txt 36~38줄(조특법 제100조의7①·제100조의8③ 계산), '까지'·'기한'으로 확정 지급월 오독(레드팀 G6) 막음
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); C = os.path.normpath(os.path.join(D, '..', '..', 'eitclate1009', 'covers_try'))
FT = Path(os.path.normpath(os.path.join(D, '..', '..', '..', 'video', 'public', 'fonts'))).as_uri()
NAV, YEL, RED, WHT = '#0F1B3D', '#FFD43B', '#D7261E', '#FFFFFF'
CSS = """@font-face{font-family:P;src:url(%(ft)s/pd700.ttf)}@font-face{font-family:B;src:url(%(ft)s/BlackHanSans.ttf)}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1080px;background:%(bg)s;font-family:P;overflow:hidden;position:relative}
.h{position:absolute;left:50px;right:50px;text-align:center;font-family:B;line-height:1;white-space:nowrap}
.row{position:absolute;left:50px;right:50px;height:190px;display:flex;align-items:center;justify-content:space-between}
.d{width:390px;height:190px;border-radius:32px;display:flex;align-items:center;justify-content:center;font-family:B;font-size:82px;white-space:nowrap}
.a{flex:1;display:flex;justify-content:center}
.lab{position:absolute;left:50px;right:50px;font-size:44px;display:flex;justify-content:space-between;white-space:nowrap}
"""
AR = '<svg width="120" height="90" viewBox="0 0 150 90"><path d="M8 45H112" stroke="%s" stroke-width="20" stroke-linecap="round"/><path d="M95 12L140 45L95 78" fill="none" stroke="%s" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/></svg>'
V = {
 # 노랑: 위 제목 2줄, 아래 신청일→지급 기한 두 줄(둘째 줄 빨강)
 'K1': dict(bg=YEL, fg=NAV, head=[('근로장려금 기한 후 신청', 84, NAV, 70), ('하루 차이, 한 달 차이', 120, RED, 180)],
            lab=('신청', '지급 기한'), laby=380, rows=[(450, ('11월 30일', NAV, YEL), ('3월 30일', WHT, NAV)), (690, ('12월 1일', NAV, YEL), ('4월 30일', RED, WHT))]),
 # 남색: 같은 구성
 'K2': dict(bg=NAV, fg=WHT, head=[('근로장려금 기한 후 신청', 84, '#A5B4D4', 70), ('하루 차이, 한 달 차이', 120, YEL, 180)],
            lab=('신청', '지급 기한'), laby=380, rows=[(450, ('11월 30일', WHT, NAV), ('3월 30일', YEL, NAV)), (690, ('12월 1일', WHT, NAV), ('4월 30일', RED, WHT))]),
 # 레드팀 K2(7) 오독 3개 고침: 왼쪽 '11월 중'·'12월 1일 마감일', 오른쪽 '까지'를 같은 크기로, 4월 칸 빨강→흰색, 아래 '2027년 법정 지급 기한'
 'K3': dict(bg=NAV, fg=WHT, head=[('근로장려금 기한 후 신청', 84, '#A5B4D4', 70), ('하루 차이, 한 달 차이', 120, YEL, 180)],
            lab=('신청', '지급 기한'), laby=380, w=(420, 440), fs=66, foot=('2027년 · 법이 정한 지급 기한', 46, '#A5B4D4', 950),
            rows=[(450, ('11월 중', WHT, NAV), ('3월 30일까지', YEL, NAV)), (690, ('12월 1일 마감', WHT, NAV), ('4월 30일까지', WHT, NAV))]),
 # 제미나이 K3(5·6) '도표 복잡' → 도표 빼고 큰 말 2줄 + 아래 작은 날짜 한 줄(사실: 11/30 신청 3/30까지, 12/1 마감일 4/30까지)
 'K4': dict(bg=NAV, fg=WHT, head=[('근로장려금 기한 후 신청', 84, '#A5B4D4', 90), ('하루 늦으면', 170, WHT, 260), ('지급 기한', 150, YEL, 490), ('한 달 밀림', 190, YEL, 660)],
            rows=[], foot=('11/30 신청 3/30까지 · 12/1 마감일 4/30까지', 50, '#A5B4D4', 920)),
}
def html(v):
    h = ''.join(f'<div class="h" style="top:{t}px;font-size:{s}px;color:{c}">{x}</div>' for x, s, c, t in v['head'])
    lab = '' if not v['rows'] else f'<div class="lab" style="top:{v.get("laby",0)}px;color:{v["fg"]}"><span style="width:390px;text-align:center">{v.get("lab",("",""))[0]}</span><span style="width:390px;text-align:center">{v.get("lab",("",""))[1]}</span></div>'
    w = v.get('w', (390, 390)); fs = v.get('fs', 82)
    lab = lab.replace('width:390px', f'width:{w[0]}px', 1).replace('width:390px', f'width:{w[1]}px', 1)
    rows = ''.join(f'<div class="row" style="top:{t}px"><div class="d" style="width:{w[0]}px;font-size:{fs}px;background:{a[1]};color:{a[2]}">{a[0]}</div><div class="a">{AR % (v["fg"], v["fg"])}</div><div class="d" style="width:{w[1]}px;font-size:{fs}px;background:{b[1]};color:{b[2]}">{b[0]}</div></div>' for t, a, b in v['rows'])
    if v.get('foot'): x, sz, c, t = v['foot']; rows += f'<div class="h" style="top:{t}px;font-size:{sz}px;color:{c};font-family:P">{x}</div>'
    return f'<html><head><meta charset="utf-8"><style>{CSS % dict(ft=FT, bg=v["bg"])}</style></head><body>{h}{lab}{rows}</body></html>'
names = sys.argv[1:] or list(V)
S = 110; F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 12)
comp = json.load(open(os.path.join(C, 'comp', 'comp.json'), encoding='utf-8'))['files'][:5]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080})
    for n in names:
        h = os.path.join(D, n + '.html'); open(h, 'w', encoding='utf-8').write(html(V[n]))
        pg.goto(Path(h).as_uri()); pg.evaluate('document.fonts.ready')
        box = pg.evaluate("[...document.querySelectorAll('.h,.row,.d')].map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.right),Math.round(r.bottom),e.scrollWidth>e.clientWidth]})")
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
