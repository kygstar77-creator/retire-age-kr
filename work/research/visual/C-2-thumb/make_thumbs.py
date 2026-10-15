# C-2 '같은 3억, 5년 차이' 썸네일 시안 (2026-10-15 visual-designer, 요청 meta.json thumb_status 10/14 14:38 · 기한 10/17 06:00)
# 문구: ep/C-2/copy/titles.md thumb_text '같은 3억, 5년 차이' · small '1998년 시작은 바닥 · 2003년은 2.7억'(레드팀: '바닥'·'2.7억'을 크게)
# 숫자: calc_n1_out.txt 월 200만원 1998년 1월 시작 → 2011년 바닥 · 2003년 1월 시작 → 2025년 말 2.72억원 (assert)
# 피한 것: 경쟁 1·2(생성 그림 인물·책상) · 3~5(사진+노랑 테두리 글) · 우리 N-2(남색 두 칸) — 주제 사물 = 통장 두 권(사람 얼굴 0)
# 금지(titles.md): '0원'·'파산'·'평생'·15.9억·정우 씨 이름 · '1998년에 바닥'으로 읽히는 배치(실제 바닥 2011년)
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.join(HERE, '..', '..', 'longform', 'ep', 'C-2')
calc = open(os.path.join(EP, 'calc_n1_out.txt'), encoding='utf-8').read()
assert '월 200만원 · 1998년 1월 시작 → 바닥 2011년' in calc
LEFT = float(re.search(r'월 200만원 · 2003년 1월 시작 → 2025년 말 ([\d.]+)억원 남음', calc).group(1))
assert round(LEFT, 1) == 2.7, LEFT
R = f'{round(LEFT, 1)}억'
BASE = open(os.path.join(HERE, '..', 'E-2-thumb', 'e2f.html'), encoding='utf-8').read()
HEAD, TAIL = BASE.split('<body>')[0] + '<body>', '<script>' + BASE.split('<script>')[1]


def book(x, y, w, h, cover, inner, tag='', tagc='#14171C'):
    """펼친 통장 — 위 표지 띠 + 안쪽 흰 면(줄 3개) + 가운데 큰 글(inner)"""
    rows = ''.join(f"<div style='position:absolute;left:{w*0.08:.0f}px;top:{h*(0.3+i*0.1):.0f}px;width:{w*0.84:.0f}px;height:3px;background:#E3E6EC'></div>" for i in range(3))
    t = f"<div class='t' style='left:0;top:{h*0.04:.0f}px;width:{w}px;text-align:center;font-size:{h*0.15:.0f}px;color:#FFFFFF'>{tag}</div>" if tag else ''
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#FFFFFF;border-radius:18px;box-shadow:0 14px 0 rgba(0,0,0,.35);overflow:hidden'>"
            f"<div style='position:absolute;left:0;top:0;width:{w}px;height:{h*0.24:.0f}px;background:{cover}'></div>{t}{rows}"
            f"<div class='t' style='left:0;top:{h*0.4:.0f}px;width:{w}px;text-align:center;{inner}'></div></div>")


def stamp(word, size):
    return f"font-size:{size}px;color:#D7261E'><span style='display:inline-block;border:10px solid #D7261E;border-radius:16px;padding:0 24px;transform:rotate(-8deg)'>{word}</span"


def big(word, size, col='#0E7A3E'):
    return f"font-size:{size}px;color:{col}'>{word}<span style='display:none'></span"


V = {}
HEADLINE = ("<div class='t' style='left:0;top:26px;width:1280px;text-align:center;font-size:132px;color:#FFD23F'>같은 3억,"
            " <span style='color:#FFFFFF'>5년 차이</span></div>")
BG = "<div style='position:absolute;inset:0;background:#14171C'></div>"
# c2a — 통장 두 권: 왼쪽 '바닥' 빨간 도장 · 오른쪽 '2.7억' 초록 (숫자 3개: 3억·5년·2.7억)
V['c2a'] = BG + HEADLINE + book(60, 214, 520, 340, '#6B7280', stamp('바닥', 120).replace("'></div></div>", "")) + book(640, 214, 520, 340, '#2B6BE4', big(R, 150))
# c2b — 같은 틀, 오른쪽 '남음'(숫자 2개 기준 지킴: 3억·5년)
V['c2b'] = BG + HEADLINE + book(60, 214, 520, 340, '#6B7280', stamp('바닥', 120)) + book(640, 214, 520, 340, '#2B6BE4', big('남음', 150))
# c2c — c2a + 표지 띠에 시작 해(titles small 줄 '1998년 시작은 바닥 · 2003년은 2.7억' 그대로 나눔) — 숫자 5개, 1초 시험 비교용
V['c2c'] = BG + HEADLINE + book(60, 214, 520, 340, '#6B7280', stamp('바닥', 120), tag='1998년 시작') + book(640, 214, 520, 340, '#2B6BE4', big(R, 150), tag='2003년 시작')
for k in V: V[k] = V[k].replace("<span style='display:none'></span'></div>", "</div>")
assert all('같은 3억' in v and '0원' not in v and '정우' not in v for v in V.values())


def check_zones(page):
    return page.evaluate("""()=>{const bad=[];document.querySelectorAll('body *').forEach(e=>{
      if(e.tagName==='SCRIPT'||!e.textContent.trim())return;
      if(e.children.length&&[...e.children].some(c=>c.textContent.trim()&&c.tagName!=='SPAN'))return;
      const r=document.createRange();r.selectNodeContents(e);const b=r.getBoundingClientRect();
      if((b.right>960&&b.bottom>576)||b.bottom>684||b.right>1280||b.left<0)bad.push(e.textContent.trim().slice(0,20)+' '+Math.round(b.left)+'-'+Math.round(b.right)+','+Math.round(b.bottom));});return bad}""")


if __name__ == '__main__':
    keys = sys.argv[1].split(',') if len(sys.argv) > 1 else list(V)
    import numpy as n
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
        for k in keys:
            html = os.path.join(HERE, f'{k}.html'); open(html, 'w', encoding='utf-8').write(HEAD + V[k] + '\n' + TAIL)
            pg.goto('file:///' + html.replace(chr(92), '/')); pg.wait_for_selector('body[data-ready]')
            out = os.path.join(EP, f'thumb_{k}.png'); pg.screenshot(path=out); im = Image.open(out)
            im.resize((320, 180), Image.LANCZOS).save(os.path.join(HERE, f'{k}_320.png'))
            im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, f'{k}_168.png'))
            a = n.asarray(im.convert('L'), float)
            print(k, os.path.getsize(out) // 1024, 'KB 명암폭', round(a.std()), '가려짐:', check_zones(pg) or '없음')
        b.close()
