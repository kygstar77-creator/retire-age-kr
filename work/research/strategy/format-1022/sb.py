# 화면 표본: 유튜브 스토리보드(재생 막대 미리보기, 320×180·약 10초마다 1장)를 받아 시각별 낱장으로 자른다(10/22).
#   py -3.12 work/research/strategy/format-1022/sb.py <videoId> ...   → frames/<id>/t0000.jpg … (커밋 안 함, .gitignore)
# 영상 파일은 받지 않는다(ytbreak.py 머리말: 남의 영상 파일 다운로드는 약관 위반). 미리보기 그림만 받는다.
import sys, os, re, json, urllib.request
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36', 'Accept-Language': 'ko-KR,ko'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
for vid in sys.argv[1:]:
    od = os.path.join(HERE, 'frames', vid); os.makedirs(od, exist_ok=True)
    if os.path.exists(os.path.join(od, 'index.json')): print('있음', vid); continue
    html = get(f'https://www.youtube.com/watch?v={vid}&hl=ko').decode('utf-8', 'ignore')
    m = re.search(r'"playerStoryboardSpecRenderer":\{"spec":"([^"]+)"', html)
    if not m: print('스토리보드 없음', vid); continue
    spec = m.group(1).replace('\\u0026', '&').split('|')
    base = spec[0]; lv = len(spec) - 2; w, h, cnt, cols, rows, iv, name, sigh = spec[-1].split('#')
    w, h, cnt, cols, rows, iv = map(int, (w, h, cnt, cols, rows, iv))
    per = cols * rows; idx = []
    for s in range((cnt + per - 1) // per):
        u = base.replace('$L', str(lv)).replace('$N', name.replace('$M', str(s))) + '&sigh=' + sigh
        p = os.path.join(od, f'sheet{s:03d}.jpg'); open(p, 'wb').write(get(u))
        im = Image.open(p)
        for k in range(per):
            n = s * per + k
            if n >= cnt: break
            t = n * iv / 1000
            fr = im.crop(((k % cols) * w, (k // cols) * h, (k % cols + 1) * w, (k // cols + 1) * h))
            fn = f't{int(t):04d}.jpg'; fr.save(os.path.join(od, fn), quality=90); idx.append((round(t, 1), fn))
    json.dump(dict(vid=vid, w=w, h=h, interval_ms=iv, frames=idx), open(os.path.join(od, 'index.json'), 'w'))
    print(vid, len(idx), '장', w, 'x', h, iv, 'ms')
