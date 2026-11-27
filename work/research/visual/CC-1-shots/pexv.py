# CC-1 실사 다시(visual 11/27 09시) — Pexels 동영상 찾기(키는 Documentspexels_key.txt, 출력 안 함)
#   py -3.12 pexv.py search "<검색어>" [n]  → stock_try/sheet_<q>.jpg (영상 첫 그림·id·길이)
#   py -3.12 pexv.py get <id>               → bg 후보 stock_try/<id>.mp4 (HD 1920 이하 가장 큰 것) + 출처 json
import sys, os, json, urllib.request, urllib.parse
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, 'stock_try'); os.makedirs(OUT, exist_ok=True)
KEY = open(r'C:\Users\강영준\Documents\pexels_key.txt', encoding='utf-8-sig').read().strip().split('=')[-1].strip()
UA = {'User-Agent': 'Mozilla/5.0'}
def api(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': KEY, **UA}), timeout=30))
def search(q, n=12):
    d = api('https://api.pexels.com/videos/search?' + urllib.parse.urlencode({'query': q, 'per_page': n, 'orientation': 'landscape'}))
    ims = []
    for v in d.get('videos', []):
        fn = os.path.join(OUT, f"t_{v['id']}.jpg")
        if not os.path.exists(fn): open(fn, 'wb').write(urllib.request.urlopen(urllib.request.Request(v['image'], headers=UA), timeout=30).read())
        ims.append((v['id'], fn, v['duration'], v['user']['name'][:16]))
    W, HH = 360, 203; bd = Image.new('RGB', (4 * W, ((len(ims) + 3) // 4) * (HH + 18)), 'white'); dr = ImageDraw.Draw(bd)
    F = ImageFont.truetype(r'C:\Windows\Fonts\malgun.ttf', 13)
    for k, (vid, fn, du, us) in enumerate(ims):
        im = Image.open(fn).convert('RGB'); im = im.resize((W, HH)); x = (k % 4) * W; y = (k // 4) * (HH + 18)
        bd.paste(im, (x, y)); dr.text((x + 2, y + HH + 1), f'{vid} {du}s {us}', fill='black', font=F)
    p = os.path.join(OUT, 'sheet_' + q.replace(' ', '_') + '.jpg'); bd.save(p, quality=80); print(p)
def get(vid):
    v = api(f'https://api.pexels.com/videos/videos/{vid}')
    fs = sorted([f for f in v['video_files'] if f.get('width') and f['width'] <= 1920 and f.get('file_type') == 'video/mp4'], key=lambda f: f['width'])
    f = fs[-1]; fn = os.path.join(OUT, f'{vid}.mp4')
    open(fn, 'wb').write(urllib.request.urlopen(urllib.request.Request(f['link'], headers=UA), timeout=120).read())
    json.dump({'id': vid, 'url': v['url'], 'author': v['user']['name'], 'author_url': v['user']['url'], 'license': 'Pexels License (free, commercial, no attribution required)', 'width': f['width'], 'duration': v['duration']},
              open(os.path.join(OUT, f'{vid}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(fn, f['width'], v['duration'])
if __name__ == '__main__':
    if sys.argv[1] == 'search': search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 12)
    else: get(int(sys.argv[2]))
