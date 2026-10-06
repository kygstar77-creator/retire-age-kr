# R-1 28차 시안(2026-10-06 visual) — 27차 판정 '다음 방향': 1초에 '예금 vs 금·S&P·SCHD' 비교 틀이 보이게(지금은 '예금 이자 영상'으로 먼저 읽힘)
# r2m = r2i 틀 유지 + 왼쪽 머리를 '예금' 하나로 크게, '1억·세후 1년'은 아래 줄로 + 두 칸 사이 노란 VS 원
# r2n = 맨 위 가로 띠 '1억 넣고 1년, 세금 떼면'(공통 조건) + 아래 왼쪽 '예금 +218만' vs 오른쪽 세 줄
# 숫자는 facts [영수증] 예금 2,580,000−397,320=2,182,680 → +218만 · 가림 자릿수 금 337만(3)·S&P500 1,023만(4)·SCHD 1,599만(4)
# 오른쪽 아래(x>960·y>576)·아래 5%(y>684) 비움 — assert로 잰다
import os, sys, pathlib
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'R-1')
dep = 2580000 - 397320; assert dep == 2182680 and round(dep / 1e4) == 218
MASK = {'금': '+???만', 'S&P500': '+?,???만', 'SCHD': '+?,???만'}
assert len(str(337)) == 3 and len(str(1023)) == 4 and len(str(1599)) == 4
head = open(os.path.join(H, 'r2i.html'), encoding='utf-8').read().split('</style>')[0] + '</style></head><body>'
tail = """<script>
function fit(id,maxW){const e=document.getElementById(id);let s=parseFloat(getComputedStyle(e).fontSize);
 while(e.getBoundingClientRect().width>maxW&&s>20){s-=2;e.style.fontSize=s+'px'}}
document.fonts.ready.then(()=>{document.querySelectorAll('[data-fit]').forEach(e=>fit(e.id,+e.dataset.fit));document.body.dataset.ready=1});
</script></body></html>"""
BG = "<div style='position:absolute;inset:0;background:#111214'></div>"
def rows(top, h, gap, lab, num):
    out = ''
    for n, (k, v) in enumerate(MASK.items()):
        y = top + n * (h + gap); ls = lab if k == '금' else round(lab * 0.72)
        out += (f"<div style='position:absolute;left:600px;top:{y}px;width:660px;height:{h}px;background:#22262E;border-radius:16px'></div>"
                f"<div class='lab' style='left:668px;top:{y + (h - ls) // 2 - 4}px;font-size:{ls}px;color:#fff'>{k}</div>"
                f"<div class='t' style='right:38px;top:{y + (h - num) // 2}px;font-size:{num}px;color:#2BD98C'>{v}</div>")
    return out
FINE = "<div class='fine' style='left:50px;top:618px;font-size:19px;color:#6B6F76'>2025.10→2026.10 과거 값 · 세금 뗀 뒤 · 미래 보장 아님</div>"
VS = lambda x, y, d: (f"<div style='position:absolute;left:{x - d // 2}px;top:{y - d // 2}px;width:{d}px;height:{d}px;border-radius:50%;background:#FFD43B;"
                      f"border:8px solid #111214;display:flex;align-items:center;justify-content:center'><span style='font:400 {round(d * .42)}px BH;color:#111214'>VS</span></div>")
M = (BG + "<div style='position:absolute;left:24px;top:40px;width:540px;height:628px;background:#F4F1E8;border-radius:18px'></div>"
     "<div class='lab' style='left:48px;top:52px;font-size:176px;color:#0F1720'>예금</div>"
     "<div class='lab' style='left:52px;top:262px;font-size:64px;color:#0F1720'><span style='color:#14A86A'>1억</span> · 세후 1년</div>"
     "<div class='t' id='big' data-fit='490' style='left:40px;top:392px;font-size:158px;color:#0F1720'>+218만</div>" + FINE
     + rows(40, 170, 18, 80, 104) + VS(582, 300, 124))
N = (BG + "<div class='lab' style='left:40px;top:30px;font-size:84px;color:#fff'><span style='color:#FFD43B'>1억</span> 넣고 1년, 세금 떼면</div>"
     "<div style='position:absolute;left:24px;top:160px;width:540px;height:508px;background:#F4F1E8;border-radius:18px'></div>"
     "<div class='lab' style='left:52px;top:182px;font-size:150px;color:#0F1720'>예금</div>"
     "<div class='t' id='big' data-fit='490' style='left:40px;top:392px;font-size:158px;color:#0F1720'>+218만</div>" + FINE
     + rows(160, 130, 14, 72, 96) + VS(582, 400, 124))
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1280, 'height': 720})
    for k, body in (('r2m', M), ('r2n', N)):
        p = os.path.join(H, k + '.html'); open(p, 'w', encoding='utf-8').write(head + body + tail); pg.goto(pathlib.Path(p).as_uri())
        pg.wait_for_selector('body[data-ready]', timeout=15000)
        boxes = pg.evaluate("()=>[...document.querySelectorAll('body *')].filter(e=>e.tagName!='SCRIPT'&&e.textContent.trim()).map(e=>{const r=e.getBoundingClientRect();return [e.textContent.slice(0,12),Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)]})")
        for t, l, tp, r, b in boxes:
            assert b <= 684, (k, t, b); assert not (r > 960 and b > 576), (k, t, r, b); assert r <= 1262 and l >= 0, (k, t, l, r)
        print(k, boxes)
        out = os.path.join(EP, f'thumb_{k}.png'); pg.screenshot(path=out)
        im = Image.open(out).convert('RGB')
        for w in (168, 320): im.resize((w, round(w * 9 / 16)), Image.LANCZOS).save(os.path.join(H, f'{k}_{w}.png'))
    br.close()
