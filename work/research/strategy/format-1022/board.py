# 나란히 판: 경쟁(위) vs 우리(아래, 노란 테두리) — 같은 시각 비율(0초·10초·30초·25%·50%·75%·끝)에서 스토리보드 한 장씩. 커밋 안 함(남의 화면).
#   py -3.12 work/research/strategy/format-1022/board.py → board_A.jpg, board_B.jpg
import os, json
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FB = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 17); FS = ImageFont.truetype(r'C:\Windows\Fonts\malgun.ttf', 14)
pool = {p['id']: p for p in json.load(open(os.path.join(HERE, 'pool.json'), encoding='utf-8'))}
OURS = {'SCOI0DP-l-s': ('A-1 파이어맵', 2402, 61, 902), '420buEFKB8k': ('N-1 파이어맵', 2741, 61, 376), 'SGx7UD-6RNE': ('C-2 파이어맵', 71, 61, 872)}
ROWS = {'A': ['ydVAKqIiRos', '1HRUFrOiNes', 'TjF_me927zs', 'Q94kgkPSp2I', 'Hx6ifDveuQ4', '97zLvnO3BnY', 'SCOI0DP-l-s', 'SGx7UD-6RNE'],
        'B': ['76GaqpIWtaU', 'i_mkrokDWgg', 'EGF6neqw3hs', 'zwbPgDs11OM', 'SVfRPKmIiYI', 'C94230lZDQQ', '420buEFKB8k']}
TITLE = {'A': "틀 A — '퇴직금(같은 돈)으로 ○○하면 실제로 남는 돈'", 'B': "틀 B — '○○이면 상위 몇 %'"}
W, H, LW = 240, 135, 250
for k, ids in ROWS.items():
    M = Image.new('RGB', (LW + 7 * W, 40 + len(ids) * (H + 6)), (20, 20, 20)); d = ImageDraw.Draw(M)
    d.text((8, 8), TITLE[k] + '   (칸: 0초 · 10초 · 30초 · 25% · 50% · 75% · 끝, 유튜브 스토리보드 320×180)', font=FB, fill='white')
    for r, v in enumerate(ids):
        y = 40 + r * (H + 6); ix = json.load(open(os.path.join(HERE, 'frames', v, 'index.json')))['frames']
        dur = ix[-1][0]
        if v in OURS: name, views, subs, sec = OURS[v]
        else: p = pool[v]; name, views, subs, sec = p['ch'], p['views'], p['subs'], p['sec']
        col = (255, 210, 0) if v in OURS else (230, 230, 230)
        d.text((8, y + 8), name[:14], font=FB, fill=col)
        d.text((8, y + 36), f'조회 {views:,}', font=FS, fill=col); d.text((8, y + 56), f'구독 {subs:,}', font=FS, fill=col)
        d.text((8, y + 76), f'길이 {sec//60}:{sec%60:02d}', font=FS, fill=col); d.text((8, y + 96), v, font=FS, fill=(150, 150, 150))
        for c, t in enumerate([0, 10, 30, dur * .25, dur * .5, dur * .75, max(dur - 10, 0)]):
            fn = min(ix, key=lambda f: abs(f[0] - t))[1]
            M.paste(Image.open(os.path.join(HERE, 'frames', v, fn)).resize((W, H)), (LW + c * W, y))
        if v in OURS: d.rectangle((LW, y, LW + 7 * W - 1, y + H - 1), outline=(255, 210, 0), width=3)
    M.save(os.path.join(HERE, f'board_{k}.jpg'), quality=85); print('board', k)
