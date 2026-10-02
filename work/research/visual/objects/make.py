# 오브젝트 PNG(투명 512)·64px 축소·비교판(어두운 바탕·밝은 바탕·64px·썸네일 축소) — py -3.12 make.py
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import objs
SRC, PNG = os.path.join(H, 'src'), os.path.join(H, 'png')
os.makedirs(SRC, exist_ok=True); os.makedirs(PNG, exist_ok=True)
ks = list(objs.OBJS)
with sync_playwright() as p:
    b = p.chromium.launch()
    for k in ks:
        sv = objs.svg(k)
        open(os.path.join(SRC, f'{k}.svg'), 'w', encoding='utf-8').write(sv)
        pg = b.new_page(viewport={'width': 512, 'height': 512})
        pg.set_content(f'<html><body style="margin:0;background:transparent">{sv}</body></html>')
        pg.screenshot(path=os.path.join(PNG, f'{k}.png'), omit_background=True); pg.close()
        Image.open(os.path.join(PNG, f'{k}.png')).resize((64, 64), Image.LANCZOS).save(os.path.join(PNG, f'{k}_64.png'))
    # 썸네일 안 배치 예(r2: 300→440px, 심사 '면적 5%라 장식'): 어두운 바탕 1280x720에 오브젝트 하나 + 문구 자리
    for k in ks:
        pg = b.new_page(viewport={'width': 1280, 'height': 720})
        sv = objs.svg(k).replace('width="512" height="512"', 'width="440" height="440"')
        pg.set_content(f'''<html><body style="margin:0;width:1280px;height:720px;background:#18191d;position:relative;font-family:Pretendard,sans-serif;font-weight:800">
<div style="position:absolute;left:60px;top:90px;width:720px;height:96px;background:#ffd400;border-radius:6px;color:#18191d;font-size:44px;display:flex;align-items:center;padding-left:28px;box-sizing:border-box">노랑 줄 자리</div>
<div style="position:absolute;left:60px;top:220px;width:720px;height:200px;border:4px dashed #fff;border-radius:8px;color:#fff;font-size:60px;display:flex;align-items:center;justify-content:center;box-sizing:border-box">숫자 자리</div>
<div style="position:absolute;left:800px;top:140px">{sv}</div></body></html>''')
        pg.screenshot(path=os.path.join(H, f'_mock_{k}.png')); pg.close()
    b.close()
cell = 220
board = Image.new('RGB', (cell * len(ks), cell * 2 + 100 + 130), '#ffffff')
for i, k in enumerate(ks):
    im = Image.open(os.path.join(PNG, f'{k}.png')).convert('RGBA').resize((200, 200), Image.LANCZOS)
    dk = Image.new('RGBA', (cell, cell), '#18191d'); dk.alpha_composite(im, (10, 10)); board.paste(dk.convert('RGB'), (i * cell, 0))
    lt = Image.new('RGBA', (cell, cell), '#f6f7f9'); lt.alpha_composite(im, (10, 10)); board.paste(lt.convert('RGB'), (i * cell, cell))
    sm = Image.open(os.path.join(PNG, f'{k}_64.png')).convert('RGBA')
    bg = Image.new('RGBA', (cell, 100), '#18191d'); bg.alpha_composite(sm, ((cell - 64) // 2, 18)); board.paste(bg.convert('RGB'), (i * cell, cell * 2))
    t = Image.open(os.path.join(H, f'_mock_{k}.png')).resize((cell - 10, round((cell - 10) * 720 / 1280)), Image.LANCZOS)
    board.paste(t, (i * cell + 5, cell * 2 + 110))
    os.remove(os.path.join(H, f'_mock_{k}.png'))
board.save(os.path.join(H, 'board.png'))
print('ok', ks)
