# R-1 썸네일 오브젝트 조합 제안 — r2e(visual-designer 22차 7.97) 위에 사물 4개를 얹은 A·B 두 안 + 비교판
# py -3.12 build.py  → a.png·b.png(1280x720), board480.png·board168.png(r2e·A·B 나란히)
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); O = os.path.dirname(H)
sys.path.insert(0, O); import objs
R2E = os.path.join(O, '..', 'R-1-thumb', 'r2e.html')
html = open(R2E, encoding='utf-8').read()


def ic(k, x, y, w):
    sv = objs.svg(k).replace('width="512" height="512"', f'width="{w}" height="{w}"')
    return f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{w}px'>{sv}</div>"


# A안: 줄마다 앞에 사물 아이콘(124px), 이름 글자는 아이콘 오른쪽으로, 왼쪽 카드 오른쪽 위에 통장
A = html
A = re.sub(r"<div class='lab' style='left:590px;(top:\d+px);font-size:(\d+)px", lambda m: f"<div class='lab' style='left:716px;{m.group(1)};font-size:{min(int(m.group(2)), 46)}px", A)
A = A.replace("font-size:120px;color:#2BD98C", "font-size:104px;color:#2BD98C").replace("top:64px;font-size:104px", "top:72px;font-size:104px").replace("top:248px;font-size:104px", "top:256px;font-size:104px").replace("top:432px;font-size:104px", "top:440px;font-size:104px")
iconsA = ic('gold_bar', 582, 61, 124) + ic('us_index', 582, 245, 124) + ic('div_coins', 582, 429, 124) + ic('bankbook', 400, 64, 140)
A = A.replace('<script>', iconsA + '<script>')
# B안: 최소 변경 — 왼쪽 카드 오른쪽 위 통장 하나만, 숫자 줄은 r2e 그대로(아래 띠안은 오른쪽 아래 재생시간 자리·지어낸 문구라 버림)
B = html.replace('<script>', ic('bankbook', 384, 60, 156) + '<script>')
with sync_playwright() as p:
    b = p.chromium.launch()
    for n, h in (('a', A), ('b', B)):
        open(os.path.join(H, n + '.html'), 'w', encoding='utf-8').write(h)
        pg = b.new_page(viewport={'width': 1280, 'height': 720}); pg.goto(__import__('pathlib').Path(H, n + '.html').as_uri())
        pg.wait_for_selector('body[data-ready]', timeout=15000)
        # 겹침 검사: 이름 글자와 숫자 상자
        ov = pg.evaluate("""()=>{const L=[...document.querySelectorAll('.lab')].map(e=>e.getBoundingClientRect()),T=[...document.querySelectorAll('.t')].map(e=>e.getBoundingClientRect());
          let o=0;for(const a of L)for(const c of T){if(a.right>c.left&&a.left<c.right&&a.bottom>c.top&&a.top<c.bottom)o++}return o}""")
        print(n, '겹침', ov)
        pg.screenshot(path=os.path.join(H, n + '.png')); pg.close()
    b.close()
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 15)
src = [('r2e(지금 후보)', os.path.join(O, '..', '..', 'longform', 'ep', 'R-1', 'thumb_r2e.png')), ('A 줄 앞 아이콘', os.path.join(H, 'a.png')), ('B 통장 하나', os.path.join(H, 'b.png'))]
for W in (480, 168):
    HH = round(W * 9 / 16); bd = Image.new('RGB', (3 * (W + 12) + 12, HH + 40), 'white'); d = ImageDraw.Draw(bd)
    for i, (lab, pth) in enumerate(src):
        bd.paste(Image.open(pth).convert('RGB').resize((W, HH), Image.LANCZOS), (12 + i * (W + 12), 10)); d.text((12 + i * (W + 12), HH + 14), lab, fill='black', font=F)
    bd.save(os.path.join(H, f'board{W}.png'))
print('ok')
