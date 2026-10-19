# 나란히 판(우리 vs 경쟁) — 남의 화면이 들어가 커밋하지 않는다(.gitignore board*).
#   py -3.12 board.py <media 폴더>  → board_B_1019_shorts.jpg · board_B_1019_long.jpg
# 쇼츠 칸마다: 영상 길이 45% 지점 한 장 + 글자 상자(초록) + Ads 안전 영역(빨강 선 x48~888·y288~1248) + 버튼 줄 규칙(파랑: y940 아래 x940) + 화면 가운데 540(노랑 점선)
import os, sys, json, glob
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); M = sys.argv[1]
S = json.load(open(os.path.join(HERE, 'sample.json'), encoding='utf-8'))
OURS = {x['id']: x['path'] for x in json.load(open(os.path.join(HERE, 'ours.json'), encoding='utf-8'))}
from PIL import Image, ImageDraw, ImageFont
FONT = ImageFont.truetype(os.path.join(HERE, '..', '..', '..', 'fonts', 'pd700.ttf'), 26)

def grab(path, frac=0.45):
    cap = cv2.VideoCapture(path); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); fps = cap.get(cv2.CAP_PROP_FPS) or 30
    n = min(n, int(600 * fps)); cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * frac)); ok, f = cap.read(); cap.release()
    return f[:, :, ::-1] if ok else None

def res(kind, vid):
    p = os.path.join(HERE, 'res', f'{kind}_{vid}.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None

def tile_short(vid, label, path):
    img = grab(path)
    if img is None: return None
    im = Image.fromarray(img).resize((1080, 1920)); d = ImageDraw.Draw(im)
    r = res('short', vid)
    if r:   # 45% 지점에 가장 가까운 프레임의 상자
        fr = min(r['frames'], key=lambda f: abs(f['t'] - r['dur'] * 0.45))
        for b in fr['boxes']: d.rectangle(b, outline=(0, 230, 90), width=5)
    d.rectangle([48, 288, 888, 1248], outline=(255, 40, 40), width=6)
    d.line([940, 940, 940, 1920], fill=(40, 120, 255), width=6); d.line([940, 940, 1080, 940], fill=(40, 120, 255), width=6)
    for y in range(0, 1920, 40): d.line([540, y, 540, y + 20], fill=(255, 220, 0), width=4)
    im = im.resize((270, 480)); d = ImageDraw.Draw(im)
    d.rectangle([0, 440, 270, 480], fill=(0, 0, 0)); d.text((6, 446), label[:14], fill=(255, 255, 255), font=FONT)
    return np.asarray(im)

def tile_long(vid, label, path):
    img = grab(path, 0.5)
    if img is None: return None
    im = Image.fromarray(img).resize((1920, 1080)); d = ImageDraw.Draw(im)
    r = res('long', vid)
    if r:
        fr = min(r['frames'], key=lambda f: abs(f['t'] - r['measured'] * 0.5))
        for b in fr['boxes']: d.rectangle(b, outline=(0, 230, 90), width=6)
    d.line([0, 864, 1920, 864], fill=(255, 40, 40), width=4)   # 아래 20%(자막 띠)
    im = im.resize((480, 270)); d = ImageDraw.Draw(im)
    d.rectangle([0, 236, 480, 270], fill=(0, 0, 0)); d.text((6, 240), label[:20], fill=(255, 255, 255), font=FONT)
    return np.asarray(im)

def sheet(tiles, cols, name):
    tiles = [t for t in tiles if t is not None]
    while len(tiles) % cols: tiles.append(np.zeros_like(tiles[0]))
    rows = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
    Image.fromarray(np.vstack(rows)).save(os.path.join(HERE, name), quality=85)
    print(name, len(tiles))

sh = [tile_short(v, '우리 ' + v[5:], p) for v, p in OURS.items() if v.startswith('OURS') and 'c2' not in v]
sh += [tile_short(v, c, os.path.join(M, f'short_{v}.v.mp4')) for c, v in S['short'] if os.path.exists(os.path.join(M, f'short_{v}.v.mp4'))]
sheet(sh, 7, 'board_B_1019_shorts.jpg')
lg = [tile_long('OURS_c2', '우리 C-2', OURS['OURS_c2'])]
lg += [tile_long(v, c, os.path.join(M, f'long_{v}.v.mp4')) for c, v in S['long'] if os.path.exists(os.path.join(M, f'long_{v}.v.mp4'))]
sheet(lg, 5, 'board_B_1019_long.jpg')
