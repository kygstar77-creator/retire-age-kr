# 경쟁 썸네일을 눈대중이 아니라 수치로 잰다 — 사장님 2026-09-23 "니 생각대로 만들지 말고 다 조사해서".
#   py -3.12 work/thumbstat.py            → work/research/yt/design/spec.json + 화면 출력
# 재는 것(전부 픽셀에서 계산): 밝기·대비·채도, 노랑/빨강/흰색 면적 비율, 글자 영역이 위·가운데·아래 중 어디에 얼마나,
#   글자 덩어리 높이 비율, 얼굴 유무·크기(OpenCV Haar). 조회수 상·하위로 갈라 차이를 낸다.
# 결과 spec.json을 thumb.py·shorts.py가 읽어 쓴다. 매일 자가발전 회차가 다시 돌려 갱신한다.
import sys, os, re, json, glob, statistics, collections
sys.stdout.reconfigure(encoding='utf-8')
import cv2, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, 'research', 'yt', 'design')
FACE = None   # cv2 5.0이 4.x 캐스케이드를 못 읽고 측정값도 전부 0이라 뺐다(2026-09-23)

def text_map(g):
    """글자처럼 보이는 영역만 — 글자꼴 성분을 골라낸다.

    2026-09-25에 찾았다. 예전 방식은 Canny 가장자리를 25x9 커널로 두 번 팽창한 것이었다. 그건 '글자'가
    아니라 '가장자리가 있나'를 재는 자였고, 사진을 꽉 채운 경쟁 썸네일에서는 늘 켜져 있었다.
    실측(경쟁 60장 중앙값): 위 0.767 / 가운데 0.922 / 아래 0.903. 0.9는 '그림의 90%가 글자'라는 뜻인데
    그럴 리가 없다 — 자가 포화된 것이다. 루프는 그 0.9434를 목표로 잡고 롱폼 text_mid 를 쫓다가
    닿지 못해 '한계 확정'으로 세워 뒀다(98회차). 없는 목표를 쫓고 있었다.

    새 방식: 흰 글자(top-hat)와 검은 글자(black-hat)를 함께 뽑고 Otsu로 자른 뒤, 성분마다
    높이(그림 높이의 2~30%)·가로세로비(0.06~14)·채움비(0.12~0.92)로 글자꼴만 남긴다.
    가로폭 상한은 두지 않는다 — 큰 글씨 한 줄은 통째로 한 성분이 되는데(우리 쇼츠가 그렇다)
    폭으로 자르면 그 줄이 통째로 버려져 우리 쇼츠가 0.000 으로 나왔다.
    같은 60장 실측: 위 0.115 / 가운데 0.081 / 아래 0.010 — 글자가 차지하는 넓이로 말이 된다.
    """
    h, w = g.shape
    kh = max(3, int(h * 0.045)) | 1
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (kh, kh))
    m = cv2.max(cv2.morphologyEx(g, cv2.MORPH_TOPHAT, k), cv2.morphologyEx(g, cv2.MORPH_BLACKHAT, k))
    _, bw = cv2.threshold(m, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    n, lab, st, _ = cv2.connectedComponentsWithStats(bw, 8)
    keep = np.zeros_like(bw)
    for i in range(1, n):
        cw, ch, a = st[i][2], st[i][3], st[i][4]
        if ch < h * 0.02 or ch > h * 0.30: continue          # 먼지·배경 덩어리
        ar = cw / max(1, ch)
        if ar < 0.06 or ar > 14: continue                    # 세로줄·가로 테두리
        fill = a / max(1, cw * ch)
        if fill < 0.12 or fill > 0.92: continue              # 속이 꽉 찬 사진 조각
        keep[lab == i] = 255
    kx = cv2.getStructuringElement(cv2.MORPH_RECT, (max(9, int(w * 0.03)) | 1, 3))
    return cv2.dilate(keep, kx, 1) > 0

def debar(im):
    """유튜브가 끼워 넣은 새까만 여백(레터박스·필러박스)을 잘라낸다.

    2026-09-25에 찾았다: 경쟁 '쇼츠' 썸네일 41장이 전부 가로형(1280x720)이었다. 유튜브는 9:16 영상의
    썸네일도 16:9 칸에 담아 주고, 남는 좌우를 새까맣게 채운다. 41장 중 18장이 그랬고 가운데 실제 그림은
    가로의 71%뿐이었다. 그 검은 여백까지 '경쟁사의 그림'으로 세는 바람에 면적 비율이 전부 묽어졌다 —
    흰 면적 기준값 0.0107, 대비 0.1791. 우리 쇼츠(1080x1920)는 여백이 없으니 늘 기준보다 높게 나왔고,
    회차들은 그 차이를 메우려고 글자 흰빛(text_tint)과 tint_v 를 끝까지 밀었다. 숫자는 가까워졌지만
    글자가 잿빛으로 죽어 2026-09-24에 두 손잡이를 모두 한계에 묶어 세웠다 — 없는 차이를 쫓고 있었다.
    여백을 떼고 재면 기준값이 흰 면적 0.0158, 대비 0.2085 로 올라간다(대비는 우리 0.2294 와 10% 차이라
    더는 차이 항목이 아니다). 그림을 바꾸는 게 아니라 여백을 안 세는 것뿐이다.
    """
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); h, w = g.shape
    cm = g.max(axis=0); rm = g.max(axis=1)
    l = 0
    while l < w and cm[l] < 40: l += 1
    r = w - 1
    while r > l and cm[r] < 40: r -= 1
    t = 0
    while t < h and rm[t] < 40: t += 1
    b = h - 1
    while b > t and rm[b] < 40: b -= 1
    nw, nh = r + 1 - l, b + 1 - t
    if nw < w * 0.3 or nh < h * 0.3: return im      # 통째로 어두운 그림은 건드리지 않는다
    if nw > w * 0.98 and nh > h * 0.98: return im   # 여백이 없으면 그대로
    return im[t:b + 1, l:r + 1]


def measure(path, pad=True):
    """pad=False 면 여백 깎기를 건너뛴다 — 우리가 그린 그림에는 유튜브 여백이 없다.

    2026-09-25 실측: debar 가 우리 쇼츠 short0.png 를 1920 → 1699 로 잘랐다(세로 13%). 위아래가
    어두운 우리 판형을 유튜브 레터박스로 잘못 본 것이다. 띠(위·가운데·아래)를 잘린 그림에서 나누면
    글자가 실제보다 위에 있는 것으로 재어지고, 루프는 그 어긋난 숫자에 맞춰 text_y 를 움직인다.
    같은 그림을 안 깎고 재면 쇼츠 가운데 띠가 0.237 → 0.000 으로 바뀐다(글자가 실제로는 가운데에 없다).
    경쟁 jpg 는 유튜브가 16:9 칸에 담아 주므로 pad=True 그대로 둔다."""
    im = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)   # 한글 경로는 imread가 못 읽는다
    if im is None: return None
    if pad: im = debar(im)
    im = cv2.resize(im, (640, 360)) if im.shape[0] < im.shape[1] else cv2.resize(im, (360, 640))
    h, w = im.shape[:2]; hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    H, S, V = hsv[:, :, 0].astype(int), hsv[:, :, 1].astype(int), hsv[:, :, 2].astype(int)
    tm = text_map(g); tot = h * w
    bands = {'top': tm[:h // 3].mean(), 'mid': tm[h // 3:2 * h // 3].mean(), 'bot': tm[2 * h // 3:].mean()}
    rows = tm.mean(axis=1); thick = (rows > 0.25).sum() / h
    fa = 0.0
    if FACE is not None and not FACE.empty():
        faces = FACE.detectMultiScale(g, 1.2, 5, minSize=(40, 40))
        fa = max([fw * fh for (x, y, fw, fh) in faces], default=0) / tot
    return {
        'bright': float(V.mean()) / 255, 'contrast': float(V.std()) / 255, 'sat': float(S.mean()) / 255,
        'yellow': float((((H >= 20) & (H <= 35)) & (S > 110) & (V > 140)).mean()),
        'red': float(((((H <= 8) | (H >= 172)) & (S > 110) & (V > 110))).mean()),
        'white': float(((S < 40) & (V > 205)).mean()),
        'dark': float((V < 70).mean()),
        'text': float(tm.mean()), 'text_top': float(bands['top']), 'text_mid': float(bands['mid']), 'text_bot': float(bands['bot']),
        'text_thick': float(thick),
    }

def main():
    rows = []
    for meta in glob.glob(os.path.join(D, '*', 'meta.json')):
        d = json.load(open(meta, encoding='utf-8')); folder = os.path.dirname(meta)
        byid = {v['id']: v for v in d['videos']}
        for p in glob.glob(os.path.join(folder, '*.jpg')):
            m = re.match(r'(\d+)_([SL])_(.+)\.jpg', os.path.basename(p))
            if not m: continue
            st = measure(p)
            if st: rows.append({**st, 'views': int(m.group(1)), 'short': m.group(2) == 'S', 'ch': d['channel'], 'title': byid.get(m.group(3), {}).get('title', '')})
    print('썸네일', len(rows), '장 측정')
    keys = ['bright', 'contrast', 'sat', 'yellow', 'red', 'white', 'dark', 'text', 'text_top', 'text_mid', 'text_bot', 'text_thick']
    spec = {'n': len(rows)}
    for kind, rs in (('long', [r for r in rows if not r['short']]), ('short', [r for r in rows if r['short']])):
        if len(rs) < 6: continue
        rs.sort(key=lambda r: -r['views']); half = max(3, len(rs) // 3)
        hi, lo = rs[:half], rs[-half:]
        print(f"\n[{'롱폼' if kind == 'long' else '쇼츠'}] {len(rs)}장 · 상위 {len(hi)}장(조회 중앙 {statistics.median(r['views'] for r in hi):,.0f}) vs 하위 {len(lo)}장({statistics.median(r['views'] for r in lo):,.0f})")
        s = {}
        for k in keys:
            a, b = statistics.median(r[k] for r in hi), statistics.median(r[k] for r in lo)
            s[k] = round(a, 4)
            mark = '↑' if a > b * 1.15 else ('↓' if a * 1.15 < b else ' ')
            print(f'  {k:11s} 상위 {a:.3f} / 하위 {b:.3f} {mark}')
        spec[kind] = s
    json.dump(spec, open(os.path.join(D, 'spec.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n저장', os.path.join(D, 'spec.json'))

if __name__ == '__main__': main()
