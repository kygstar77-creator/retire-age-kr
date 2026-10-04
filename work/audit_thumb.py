# 썸네일·카드·카페 그림의 글자 크기·가림 관문 — png에서 글자 줄 높이를 직접 잰다(생성 코드가 편마다 달라서).
#   python3 work/audit_thumb.py [--kind thumb|card|cafe] <그림.png> [...]
#   종류를 안 주면 비율로 고른다: 16:9 → thumb, 9:16 → card, 그 밖 → cafe.
# 판정(근거):
#   - 글자 줄 높이: 보이는 크기로 줄였을 때 9px 미만이면 '작은 글자'로 거부.
#       9px = Google Lighthouse 'legible font sizes' 12px × 한글 글자 몸통/글자 크기 약 0.75.
#       보이는 폭: thumb 320px(RULES.md 썸네일 관문 규칙 2 '320×180으로 줄여도 읽혀야'),
#                 card 375px(휴대폰 세로 전체 화면), cafe 343px(375px 화면 − 좌우 16px 여백).
#   - thumb 가림: 오른쪽 아래 25%×20%(영상 길이 표시)·아래 5%(진행 막대)에 글자가 있으면 거부(RULES.md 썸네일 관문 규칙 2).
# 한계: 글자와 도형을 모양으로만 가른다(막대·선은 꽉 찬 사각형·가늘고 긴 선으로 보고 뺀다). 판정은 사람이 그림을 보고 확정한다.
import sys
import numpy as np
from PIL import Image

VIEW_W = {'thumb': 320, 'card': 375, 'cafe': 343}
MIN_VIEW_PX = 9.0
WORK_W = 640  # 이 폭으로 줄여서 잰다(속도)


def guess_kind(w, h):
    r = w / h
    if abs(r - 16 / 9) < 0.05:
        return 'thumb'
    if abs(r - 9 / 16) < 0.05:
        return 'card'
    return 'cafe'


def background(a):
    """테두리 픽셀 가운데 가장 흔한 색(16단계로 묶음)."""
    edge = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    q = (edge // 16).astype(np.int32)
    keys = q[:, 0] * 256 + q[:, 1] * 16 + q[:, 2]
    k = np.bincount(keys).argmax()
    sel = edge[keys == k]
    return sel.mean(axis=0)


def local_background(a, tile=16, reach=2):
    """칸(16px)마다 둘레 5×5칸(80px)에서 가장 흔한 색 → 바탕 지도. 위·아래 바탕색이 다른 그림(A-1)도 잰다."""
    H, W, _ = a.shape
    q = (a // 16).astype(np.int32)
    keys = q[..., 0] * 256 + q[..., 1] * 16 + q[..., 2]
    ty, tx = (H + tile - 1) // tile, (W + tile - 1) // tile
    out = np.zeros_like(a, dtype=np.float64)
    for j in range(ty):
        for i in range(tx):
            y0, y1 = max(0, (j - reach) * tile), min(H, (j + reach + 1) * tile)
            x0, x1 = max(0, (i - reach) * tile), min(W, (i + reach + 1) * tile)
            win = keys[y0:y1, x0:x1].ravel()
            k = np.bincount(win).argmax()
            col = a[y0:y1, x0:x1].reshape(-1, 3)[win == k].mean(axis=0)
            out[j * tile:(j + 1) * tile, i * tile:(i + 1) * tile] = col
    return out


def label(mask):
    """4방향 연결 성분 → 성분별 (y0, x0, y1, x1, 픽셀 수). 두 번 훑는 union-find."""
    h, w = mask.shape
    lab = np.zeros((h, w), dtype=np.int32)
    parent = [0]

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    nxt = 1
    for y in range(h):
        row = mask[y]
        if not row.any():
            continue
        up = lab[y - 1] if y else None
        for x in np.flatnonzero(row):
            l = lab[y, x - 1] if x and row[x - 1] else 0
            u = up[x] if up is not None and mask[y - 1, x] else 0
            if l and u:
                a, b = find(l), find(u)
                lab[y, x] = min(a, b)
                if a != b:
                    parent[max(a, b)] = min(a, b)
            elif l or u:
                lab[y, x] = l or u
            else:
                parent.append(nxt); lab[y, x] = nxt; nxt += 1
    roots = np.array([find(i) for i in range(nxt)], dtype=np.int32)
    lab = roots[lab]
    comps = {}
    ys, xs = np.nonzero(lab)
    for y, x, l in zip(ys, xs, lab[ys, xs]):
        c = comps.get(l)
        if c is None:
            comps[l] = [y, x, y, x, 1]
        else:
            if y < c[0]: c[0] = y
            if x < c[1]: c[1] = x
            if y > c[2]: c[2] = y
            if x > c[3]: c[3] = x
            c[4] += 1
    return [tuple(c) for c in comps.values()]


def glyph_like(c, H, W):
    y0, x0, y1, x1, n = c
    h, w = y1 - y0 + 1, x1 - x0 + 1
    if max(h, w) < 3 or h > 0.45 * H:
        return False
    fill = n / (h * w)
    if (w > 0.2 * W and w / h > 6) or (h > 0.2 * H and h / w > 6):   # 긴 선(축·격자·그래프 선)
        return False
    if fill > 0.85 and h * w > 400:      # 꽉 찬 사각형(막대·칩 바탕)
        return False
    if fill > 0.85 and (w / h > 6 or h / w > 6):   # 꽉 찬 가는 막대(띠 그래프 칸)
        return False
    if fill < 0.08:                      # 테두리만 있는 상자
        return False
    return True


def syllables(comps):
    """한글 한 글자는 위(초성·중성)와 아래(받침) 조각으로 나뉜다 → 가로로 겹치고 세로로 붙은 조각을 한 글자로 합친다.
    합친 높이는 그 무리에서 가장 큰 원래 조각의 1.8배를 넘지 못한다(그래프·여러 줄이 한 덩어리로 번지지 않게)."""
    groups = []  # [y0, x0, y1, x1, n, 가장 큰 원래 조각 높이]
    for c in sorted(comps, key=lambda c: (c[0], c[1])):
        ch = c[2] - c[0] + 1
        for o in groups:
            ovx = min(c[3], o[3]) - max(c[1], o[1]) + 1
            minw = min(c[3] - c[1], o[3] - o[1]) + 1
            gap = max(c[0], o[0]) - min(c[2], o[2])
            base = max(o[5], ch)
            merged_h = max(c[2], o[2]) - min(c[0], o[0]) + 1
            if ovx >= 0.5 * minw and gap <= 0.4 * base and merged_h <= 1.8 * base:
                o[0], o[1] = min(o[0], c[0]), min(o[1], c[1]); o[2], o[3] = max(o[2], c[2]), max(o[3], c[3]); o[4] += c[4]; o[5] = base
                break
        else:
            groups.append([c[0], c[1], c[2], c[3], c[4], ch])
    return [tuple(g[:5]) for g in groups]


def lines_of(comps):
    """글자 성분을 줄로 묶는다: 세로로 반 이상 겹치고 가로 간격이 줄 높이 1.2배 이하."""
    comps = sorted(comps, key=lambda c: c[1])
    lines = []
    for c in comps:
        y0, x0, y1, x1, _ = c
        for L in lines:
            ly0, ly1 = L['y0'], L['y1']
            ov = min(y1, ly1) - max(y0, ly0)
            hh = max(y1 - y0, ly1 - ly0) + 1
            ch, lh = y1 - y0 + 1, L['h']
            if ov >= 0.5 * min(ch, ly1 - ly0 + 1) and max(ch, lh) <= 1.6 * min(ch, lh) and x0 - L['x1'] <= 1.2 * hh:
                L['y0'] = min(ly0, y0); L['y1'] = max(ly1, y1); L['x1'] = max(L['x1'], x1); L['x0'] = min(L['x0'], x0); L['n'] += 1
                break
        else:
            lines.append({'y0': y0, 'y1': y1, 'x0': x0, 'x1': x1, 'n': 1, 'h': y1 - y0 + 1})
    return [L for L in lines if L['n'] >= 2]  # 성분 1개짜리는 글자 줄로 보지 않는다(점·아이콘)


def measure(path, kind=None, thresh=60):
    im = Image.open(path).convert('RGB')
    W0, H0 = im.size
    kind = kind or guess_kind(W0, H0)
    s = WORK_W / W0
    small = im.resize((WORK_W, max(1, round(H0 * s))), Image.BILINEAR)
    a = np.asarray(small).astype(np.int32)
    bg = local_background(a)
    mask = np.abs(a - bg).sum(axis=2) > thresh
    H, W = mask.shape
    comps = syllables([c for c in label(mask) if glyph_like(c, H, W)])
    lines = lines_of([c for c in comps if c[2] - c[0] + 1 <= 0.45 * H])
    view = VIEW_W[kind] / WORK_W
    out = []
    for L in lines:
        hpx = L['y1'] - L['y0'] + 1
        out.append({'x0': L['x0'] / s, 'y0': L['y0'] / s, 'x1': L['x1'] / s, 'y1': L['y1'] / s,
                    'h_orig': hpx / s, 'h_view': hpx * view})
    return {'path': path, 'kind': kind, 'size': (W0, H0), 'lines': sorted(out, key=lambda r: r['y0'])}


def judge(m):
    fail = []
    W0, H0 = m['size']
    for L in m['lines']:
        if L['h_view'] < MIN_VIEW_PX:
            fail.append(f"작은 글자: y={L['y0']:.0f}~{L['y1']:.0f}px 줄 높이 {L['h_orig']:.0f}px → {VIEW_W[m['kind']]}px 폭에서 {L['h_view']:.1f}px < {MIN_VIEW_PX:.0f}px")
        if m['kind'] == 'thumb':
            if L['x1'] > 0.75 * W0 and L['y1'] > 0.80 * H0:
                fail.append(f"가림: 영상 길이 표시 자리(오른쪽 아래 25%×20%)에 글자 x={L['x0']:.0f}~{L['x1']:.0f}, y={L['y0']:.0f}~{L['y1']:.0f}")
            elif L['y1'] > 0.95 * H0:
                fail.append(f"가림: 진행 막대 자리(아래 5%)에 글자 y={L['y0']:.0f}~{L['y1']:.0f}")
    return fail


def main(argv):
    kind = None
    if argv[:1] == ['--kind']:
        kind, argv = argv[1], argv[2:]
    if not argv:
        print('사용법: python3 work/audit_thumb.py [--kind thumb|card|cafe] <그림.png> [...]'); return 2
    bad = 0
    for p in argv:
        m = measure(p, kind)
        f = judge(m)
        hs = [L['h_view'] for L in m['lines']]
        mn = f"{min(hs):.1f}" if hs else '-'
        print(f"== {p} [{m['kind']} {m['size'][0]}×{m['size'][1]}] 글자 줄 {len(hs)} · 가장 작은 줄 {mn}px(보이는 크기) · {'거부 ' + str(len(f)) if f else '통과'}")
        for x in f:
            print('  ' + x)
        bad += bool(f)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
