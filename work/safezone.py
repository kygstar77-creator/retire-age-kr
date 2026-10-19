# 쇼츠 안전 영역 관문(10/16 쇼츠 담당 — 사장님 휴대폰에서 g1s_paths 글자가 상단바·채널 이름·오른쪽 버튼 밑에 깔리고 왼쪽 끝이 잘림)
# 기준: Google Ads 고객센터 '세로 동영상' 안전 영역 그림(1080×1920) — 위 288 · 아래 672 · 왼쪽 48 · 오른쪽 192 px. 근거·출처: research/cardshorts/safe-zone-1016.md
# 렌더된 mp4를 1초 간격으로 뜯어 글자 상자(RapidOCR 글자 찾기만, 읽기는 안 함)를 찾고, 상자가 안전 영역 밖으로 나가거나 화면 가장자리에 닿으면(잘림) 걸린다.
#   py -3.12 work/safezone.py <mp4|png …>              # 걸리면 종료코드 1 · 결과는 <mp4>.safezone.json(크기·수정시각이 같으면 다시 재지 않음)
#   py -3.12 work/safezone.py <mp4> --draw out.png [초]  # 그 초 프레임에 안전 영역 선 + 글자 상자(빨강=걸림, 초록=통과)를 그린다
# 올리기 관문: ytupload.upload()·research/cardshorts/*clips_up.py가 gate(mp4)를 부른다. 세로(높이>너비) 영상만 잰다.
import os, sys, json
import numpy as np

W0, H0 = 1080, 1920
TOP, BOTTOM, LEFT, RIGHT = 288, 672, 48, 192          # 1080×1920 기준 가려지는 너비(px)
SAFE = (LEFT, TOP, W0 - RIGHT, H0 - BOTTOM)            # (x0, y0, x1, y1) = (48, 288, 888, 1248)
# 기준 리뉴얼 B-03(10/19, criteria/B-screen-1019.md): 위 288은 광고용 그림 — 앱에서 덮인 건 양 끝 단추(뒤로가기·⋮, 사장님 10/16 화면).
#   경쟁 쇼츠 25편 제목 위끝 중앙 y 145·가로 중앙 218~856 → 가운데 x 180~900 안 글자는 y 150부터 허용, 양 끝은 288 그대로.
#   (보고서의 '넣기 전 앱 화면 1장 확인'은 아직 안 함 — today.md에 사장님 확인 요청)
TOP_C, TOP_CX0, TOP_CX1 = 230, 180, 900   # 10/19 사장님 앱 화면(우리 쇼츠 H04T4PbkGCY): 뒤로가기·검색·⋮ 아이콘이 영상 y 약 161~217(검색 x 약 843~895) → 가운데도 230부터(150이면 검색 아이콘과 겹침)
BTN_X, BTN_Y = 940, 940                                # 오른쪽 버튼 줄: x 940 오른쪽, y 940 아래(10/19 경쟁 쇼츠 화면 실측)
TOL = 6                                                # 글자 찾기 상자는 글자보다 몇 px 넓게 잡힌다
EDGE = 3                                               # 화면 끝 3px 안에 닿으면 '잘림'
VERSION = 'shorts-ui-288-672-48 btn940 top150c v3'
_eng = None


def _engine():
    global _eng
    if _eng is None:
        from rapidocr_onnxruntime import RapidOCR
        _eng = RapidOCR()
    return _eng


def boxes(img):
    """img: RGB numpy(H,W,3). 글자 상자 [(x0,y0,x1,y1)] — 1080×1920 좌표로 맞춘다."""
    h, w = img.shape[:2]
    r, _ = _engine()(img[:, :, ::-1].copy(), use_det=True, use_cls=False, use_rec=False)
    sx, sy = W0 / w, H0 / h; out = []
    for b in (r or []):
        b = np.array(b, dtype=float)
        out.append((b[:, 0].min() * sx, b[:, 1].min() * sy, b[:, 0].max() * sx, b[:, 1].max() * sy))
    return out


def judge(bx):
    x0, y0, x1, y1 = bx; why = []
    if x0 <= EDGE or y0 <= EDGE or x1 >= W0 - EDGE or y1 >= H0 - EDGE: why.append('화면 끝에서 잘림')
    if y0 < SAFE[1] - TOL:
        mid = x0 >= TOP_CX0 - TOL and x1 <= TOP_CX1 + TOL
        if not mid: why.append(f'위 {TOP}px(양 끝 뒤로가기·⋮) 안 — 288 위는 가운데 x {TOP_CX0}~{TOP_CX1}만')
        elif y0 < TOP_C - TOL: why.append(f'위 {TOP_C}px(상단바) 안')
    if y1 > SAFE[3] + TOL: why.append(f'아래 {BOTTOM}px(채널 이름·제목·구독) 안')
    if x0 < SAFE[0] - TOL: why.append(f'왼쪽 {LEFT}px 안')
    # 10/19 사장님 경쟁 쇼츠 화면(명화관cinema, 13만 좋아요): 제목은 화면 가운데에 거의 끝까지(x 약 105~975), 오른쪽 버튼 줄은 y 약 960~1690에만 있다.
    #   → 버튼 줄 높이(y 940 아래)에 걸친 글자만 x 940까지, 그 위(제목 자리)는 왼쪽과 같은 48px 여백(x 1032)까지. 예전 '오른쪽 192px 전체'는 Ads 광고용 그림을 우리가 넓혀 쓴 것.
    xr = BTN_X if y1 > BTN_Y else W0 - LEFT
    if x1 > xr + TOL: why.append(f'오른쪽 x {xr} 밖(' + ('좋아요·댓글·공유 버튼 줄' if y1 > BTN_Y else '화면 오른쪽 여백') + ')')
    return why


def frames(mp4, every=1.0):
    """(초, RGB 배열) — every초마다 한 장. OpenCV로 읽는다(py 3.10·3.12 둘 다 rapidocr와 함께 깔림)."""
    import cv2
    cap = cv2.VideoCapture(mp4); fps = cap.get(cv2.CAP_PROP_FPS) or 30; n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); i = 0; nxt = 0.0
    try:
        while True:
            ok = cap.grab()
            if not ok: break
            t = i / fps
            if t + 1e-6 >= nxt:
                ok, bgr = cap.retrieve()
                if ok: yield t, bgr[:, :, ::-1].copy()
                nxt += every
            i += 1
    finally:
        cap.release()


def is_vertical(mp4):
    import cv2
    cap = cv2.VideoCapture(mp4); w, h = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT); cap.release()
    if not w or not h: raise RuntimeError('영상을 못 읽음: ' + mp4)
    return h > w


def scan(path, every=1.0):
    """[{t, box, why}] — 걸린 상자만. png면 t=0 한 장."""
    if path.lower().endswith('.mp4'): it = frames(path, every)
    else:
        from PIL import Image
        it = [(0.0, np.asarray(Image.open(path).convert('RGB')))]
    hits, n = [], 0
    for t, img in it:
        n += 1
        for bx in boxes(img):
            why = judge(bx)
            if why: hits.append({'t': round(t, 2), 'box': [int(round(v)) for v in bx], 'why': why})
    return hits, n


def _cache(mp4): return mp4 + '.safezone.json'


def gate(mp4, every=1.0, quiet=False):
    """(ok, 메시지). 세로 영상이 아니면 통과. 결과는 <mp4>.safezone.json에 남기고, 크기·수정시각·기준이 같으면 다시 재지 않는다."""
    if not is_vertical(mp4): return True, '안전 영역 관문: 가로 영상이라 재지 않음'
    st = os.stat(mp4); key = {'size': st.st_size, 'mtime': int(st.st_mtime), 'std': VERSION, 'every': every}
    cp = _cache(mp4)
    if os.path.exists(cp):
        try:
            o = json.load(open(cp, encoding='utf-8'))
            if o.get('key') == key: hits, n = o['hits'], o['frames']; return _msg(hits, n, quiet)
        except Exception: pass
    hits, n = scan(mp4, every)
    json.dump({'key': key, 'safe': SAFE, 'frames': n, 'hits': hits}, open(cp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    return _msg(hits, n, quiet)


def _msg(hits, n, quiet=False):
    if not hits: return True, f'안전 영역 관문 통과: {n}프레임(1초 간격) 글자 상자 전부 x {SAFE[0]}~{SAFE[2]} · y {SAFE[1]}~{SAFE[3]} 안'
    secs = sorted({int(h['t']) for h in hits})
    lines = [f'안전 영역 관문 걸림: {len(secs)}초({n}프레임 중) · 상자 {len(hits)}개']
    if not quiet:
        seen = set()
        for h in hits:
            k = (tuple(h['why']), h['box'][1] // 40)
            if k in seen: continue
            seen.add(k); lines.append(f"  {h['t']:>5.1f}초 상자 {h['box']} — {' · '.join(h['why'])}")
            if len(seen) >= 12: lines.append('  …'); break
    return False, '\n'.join(lines)


def draw(path, out, t=None, img=None):
    """안전 영역 선(빨강 띠=가려지는 곳)과 글자 상자를 그린 1080×1920 png."""
    from PIL import Image, ImageDraw
    if img is None:
        if path.lower().endswith('.mp4'):
            img = None
            for tt, a in frames(path, 0.5):
                img = a
                if t is None or tt >= t: break
        else: img = np.asarray(Image.open(path).convert('RGB'))
    im = Image.fromarray(img).resize((W0, H0)); ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    x0, y0, x1, y1 = SAFE; red = (255, 40, 40, 70)
    d.rectangle([0, 0, W0, y0], fill=red); d.rectangle([0, y1, W0, H0], fill=red)
    d.rectangle([0, y0, x0, y1], fill=red); d.rectangle([x1, y0, W0, y1], fill=red)
    im = Image.alpha_composite(im.convert('RGBA'), ov); d = ImageDraw.Draw(im)
    d.rectangle([x0, y0, x1, y1], outline=(255, 0, 0, 255), width=4)
    for bx in boxes(np.asarray(im.convert('RGB'))):
        col = (230, 0, 0, 255) if judge(bx) else (0, 170, 60, 255)
        d.rectangle([int(v) for v in bx], outline=col, width=3)
    im.convert('RGB').save(out)
    return out


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    args = [a for a in sys.argv[1:]]
    if '--draw' in args:
        i = args.index('--draw'); src = args[0]; out = args[i + 1]; t = float(args[i + 2]) if len(args) > i + 2 else None
        print(draw(src, out, t)); sys.exit(0)
    bad = 0
    for p in args:
        if p.lower().endswith('.mp4'): ok, msg = gate(p)
        else:
            hits, n = scan(p); ok, msg = _msg(hits, n)
        print(f'## {p}\n{msg}'); bad += (not ok)
    sys.exit(1 if bad else 0)
