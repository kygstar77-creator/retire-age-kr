# 10/19 재썸네일용 Pexels 찾기·받기(키는 Documents\pexels_key.txt에서만 읽고 출력하지 않는다).
#   py -3.12 pex.py search "<영어 검색어>" [장수=8]   → cand/<검색어>/ 작은 그림 + cand_<검색어>.jpg 견본판(번호·id)
#   py -3.12 pex.py get <id> <저장이름>               → photo/<저장이름>.jpg (large2x) + photo/sources.json에 출처·라이선스 기록
import sys, os, json, urllib.request, urllib.parse
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = open(r'C:\Users\강영준\Documents\pexels_key.txt', encoding='utf-8-sig').read().strip().split('=')[-1].strip()
UA = {'User-Agent': 'Mozilla/5.0'}


def api(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': KEY, **UA}), timeout=30))


def search(q, n=8):
    d = api('https://api.pexels.com/v1/search?' + urllib.parse.urlencode({'query': q, 'per_page': n, 'orientation': 'landscape'}))
    out = os.path.join(H, 'cand', q.replace(' ', '_')); os.makedirs(out, exist_ok=True)
    ims = []
    for p in d.get('photos', []):
        fn = os.path.join(out, f"{p['id']}.jpg")
        if not os.path.exists(fn): open(fn, 'wb').write(urllib.request.urlopen(urllib.request.Request(p['src']['medium'], headers=UA), timeout=30).read())
        ims.append((p['id'], fn, p.get('alt', '')[:60]))
    W, HH = 360, 240; bd = Image.new('RGB', (4 * W, ((len(ims) + 3) // 4) * (HH + 18)), 'white'); dr = ImageDraw.Draw(bd)
    F = ImageFont.truetype(r'C:\Windows\Fonts\malgun.ttf', 13)
    for k, (pid, fn, alt) in enumerate(ims):
        im = Image.open(fn).convert('RGB'); im.thumbnail((W, HH)); x = (k % 4) * W; y = (k // 4) * (HH + 18)
        bd.paste(im, (x, y)); dr.text((x + 2, y + HH + 1), f'{pid} {alt}', fill='black', font=F)
    p = os.path.join(H, 'cand', 'sheet_' + q.replace(' ', '_') + '.jpg'); bd.save(p, quality=80); print(p)


def get(pid, name):
    p = api(f'https://api.pexels.com/v1/photos/{pid}')
    os.makedirs(os.path.join(H, 'photo'), exist_ok=True)
    fn = os.path.join(H, 'photo', name + '.jpg')
    open(fn, 'wb').write(urllib.request.urlopen(urllib.request.Request(p['src']['large2x'], headers=UA), timeout=60).read())
    sp = os.path.join(H, 'photo', 'sources.json')
    src = json.load(open(sp, encoding='utf-8')) if os.path.exists(sp) else {}
    src[name + '.jpg'] = {'site': 'Pexels', 'id': p['id'], 'by': p['photographer'], 'url': p['url'], 'alt': p.get('alt', ''),
                         'license': 'Pexels License(무료·상업 이용 가능·출처 표기 의무 없음)'}
    json.dump(src, open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(fn, Image.open(fn).size)


if __name__ == '__main__':
    if sys.argv[1] == 'search': search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 8)
    else: get(sys.argv[2], sys.argv[3])
