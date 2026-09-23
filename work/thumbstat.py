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
    """글자처럼 보이는 영역: 강한 가장자리가 촘촘한 곳(형태학 팽창으로 덩어리화)"""
    e = cv2.Canny(g, 120, 240)
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 9))
    return cv2.dilate(e, k, iterations=2) > 0

def measure(path):
    im = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)   # 한글 경로는 imread가 못 읽는다
    if im is None: return None
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
