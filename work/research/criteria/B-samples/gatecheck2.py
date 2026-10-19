# ⑥ UI 상자 관문 고친 안 시험(white = 띠 빼고 안 밝기 200↑ 흰 판만): bgcheck.ui_boxes와 같은 법 + '화면 너비 85% 넘는 띠'(경쟁 위 제목 띠·아래 채널 띠)는 세지 않음.
#   py -3.12 gatecheck2.py media → gatecheck2.json {id: {old: 상자1개↑ 프레임 비율, band_ex: 띠 뺀 비율}}
import os, sys, json
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); M = sys.argv[1]
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))
import safezone
S = json.load(open(os.path.join(HERE, 'sample.json'), encoding='utf-8'))
OURS = {x['id']: x['path'] for x in json.load(open(os.path.join(HERE, 'ours.json'), encoding='utf-8')) if x['kind'] == 'short'}

def boxes(img):   # bgcheck.ui_boxes 그대로 옮기고 상자 모양을 돌려준다
    h0, w0 = img.shape[:2]; W = 852; H = int(round(h0 * W / w0))
    s = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA); g = cv2.cvtColor(s, cv2.COLOR_RGB2GRAY)
    e = cv2.dilate(cv2.Canny(g, 20, 60), np.ones((3, 3), np.uint8))
    cs, _ = cv2.findContours(e, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE); out = []
    for c in cs:
        x, y, w, h = cv2.boundingRect(c); fa = w * h / (W * H)
        if fa < 0.004 or fa > 0.7 or w < 40 or h < 16: continue
        if cv2.contourArea(c) / (w * h) < 0.82: continue
        inner = g[y + 3:y + h - 3, x + 3:x + w - 3]
        if inner.size < 50: continue
        hist = np.bincount(inner.ravel(), minlength=256); m = int(hist.argmax())
        if hist[max(0, m - 8):m + 9].sum() / inner.size < 0.65: continue
        if any(abs(x - a) < 6 and abs(y - b) < 6 and abs(w - c2) < 10 and abs(h - d) < 10 for a, b, c2, d, _ in out): continue
        out.append((x, y, w, h, m))
    return out, W

out_p = os.path.join(HERE, 'gatecheck2.json'); out = json.load(open(out_p, encoding='utf-8')) if os.path.exists(out_p) else {}
jobs = [(v, os.path.join(M, f'short_{v}.v.mp4')) for _, v in S['short']] + list(OURS.items())
for vid, p in jobs:
    if vid in out or not os.path.exists(p): continue
    a = b = c = n = 0
    for t, img in safezone.frames(p, 1.0):
        bs, W = boxes(img); n += 1
        a += len(bs) >= 1; b += sum(1 for x, y, w, h, m in bs if w < 0.85 * W) >= 1
        c += sum(1 for x, y, w, h, m in bs if w < 0.85 * W and m >= 200) >= 1   # 흰 판만(안 밝기 200↑)
    out[vid] = {'n': n, 'old': round(a / max(n, 1), 2), 'band_ex': round(b / max(n, 1), 2), 'white': round(c / max(n, 1), 2)}
    json.dump(out, open(out_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(vid, out[vid], flush=True)
