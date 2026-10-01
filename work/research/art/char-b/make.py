# 캐릭터 PNG·썸네일 배치 시안·축소본 — py -3.12 make.py
# 문구 칸은 자리만 둔다(카피라이터가 채움). 오른쪽 아래 25%x20%와 아래 5%는 비움, 캐릭터 상자는 썸네일의 25% 이하(assert).
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import char
SV = {'a': char.svg_a(), 'b': char.svg_b()}
W, HH = 1280, 720
CH_H = 600  # 썸네일 속 캐릭터 높이(px) — r2: 470→600(심사: 320px에서 얼굴이 작다)
CH_W = round(CH_H * 340 / 450)


def thumb(k):
    s = SV[k].replace('width="600" height="794"', f'width="{CH_W}" height="{CH_H}"')
    return f'''<html><body style="margin:0;width:{W}px;height:{HH}px;background:#18191d;font-family:'Pretendard',sans-serif;font-weight:800;position:relative;overflow:hidden">
<div style="position:absolute;left:500px;top:70px;width:720px;height:96px;background:#ffd400;border-radius:6px;display:flex;align-items:center;padding-left:28px;box-sizing:border-box;color:#18191d;font-size:44px">노랑 줄 자리 (카피라이터)</div>
<div style="position:absolute;left:500px;top:196px;width:720px;height:200px;border:4px dashed #fff;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:60px;box-sizing:border-box">흰 큰 줄 = 숫자 자리</div>
<div style="position:absolute;left:500px;top:420px;width:440px;height:120px;border:4px dashed #ff5a00;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#ff5a00;font-size:40px;box-sizing:border-box">강조 숫자(주황)</div>
<div style="position:absolute;left:{W-320}px;top:{HH-144}px;width:320px;height:144px;outline:2px dotted #555;color:#777;font:16px sans-serif;display:flex;align-items:flex-end;justify-content:flex-end;padding:8px;box-sizing:border-box">길이 표시 자리(비움)</div>
<div id="c" style="position:absolute;left:10px;top:{HH-40-CH_H}px;width:{CH_W}px;height:{CH_H}px">{s}</div>
</body></html>'''


res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for k, s in SV.items():
        open(os.path.join(H, f'char_{k}.svg'), 'w', encoding='utf-8').write(s)
        pg = b.new_page(viewport={'width': 600, 'height': 794})
        pg.set_content(f'<html><body style="margin:0;background:transparent">{s}</body></html>')
        cp = os.path.join(H, f'char_{k}.png'); pg.screenshot(path=cp, omit_background=True); pg.close()
        pg = b.new_page(viewport={'width': W, 'height': HH})
        pg.set_content(thumb(k)); pg.wait_for_timeout(300)
        out = os.path.join(H, f'thumb_mock_{k}.png'); pg.screenshot(path=out)
        bb = pg.eval_on_selector('#c', 'e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}'); pg.close()
        im = Image.open(cp).convert('RGBA').resize((CH_W, CH_H))
        a = im.getchannel('A'); tb = a.getbbox()
        ink = sum(1 for v in a.getdata() if v > 20)
        box = (tb[2]-tb[0]) * (tb[3]-tb[1])
        res[k] = {'char_box_px': [bb[0]+tb[0], bb[1]+tb[1], bb[0]+tb[2], bb[1]+tb[3]], 'box_area_pct': round(box/(W*HH)*100, 1),
                  'ink_area_pct': round(ink/(W*HH)*100, 1)}
        r = res[k]['char_box_px']
        assert res[k]['box_area_pct'] <= 25 and r[3] <= HH*0.95 and not (r[2] > W*0.75 and r[3] > HH*0.8), res[k]
        Image.open(out).resize((320, 180), Image.LANCZOS).save(os.path.join(H, f'thumb_mock_{k}_320.png'))
        Image.open(cp).resize((60, 80), Image.LANCZOS).save(os.path.join(H, f'char_{k}_80.png'))
    b.close()
# 비교판: 캐릭터 2 + 배치 2 + 320 축소 2
cmp = Image.new('RGB', (1280*2+30, 720+200+30), '#ffffff')
for i, k in enumerate('ab'):
    cmp.paste(Image.open(os.path.join(H, f'thumb_mock_{k}.png')), (i*1310, 0))
    cmp.paste(Image.open(os.path.join(H, f'thumb_mock_{k}_320.png')), (i*1310, 740))
    c80 = Image.open(os.path.join(H, f'char_{k}_80.png')).convert('RGBA'); cmp.paste(c80, (i*1310+360, 790), c80)
cmp.save(os.path.join(H, 'compare.png'))
json.dump(res, open(os.path.join(H, 'area.json'), 'w'), indent=1); print(res)
