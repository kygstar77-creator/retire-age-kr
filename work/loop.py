# 자가개선 루프 — 사장님 2026-09-23 "루프를 돌려라. 내가 물어보지 않아도 전부 발전하게".
#   py -3.12 work/loop.py            → 한 바퀴 돌고 work/loop_log.json에 기록
# 한 바퀴:
#   1) 수집  경쟁 채널 썸네일·제목·조회(ytdesign) + 우리 채널 성과(ytupload stats) + 블로그/카페 성과(perf·visitors)
#   2) 측정  경쟁 썸네일을 픽셀로 재고(thumbstat) 우리 썸네일도 같은 자로 잰다
#   3) 비교  우리 값 − 경쟁 상위 값 = 차이(gap). 차이가 큰 항목을 고른다
#   4) 조정  design.json(생성기가 읽는 값)을 그 방향으로 한 칸 움직인다. 한 번에 최대 3개만.
#   5) 기록  무엇을 왜 바꿨는지, 지난번 조정 뒤 성과가 올랐는지 loop_log.json에 남긴다
# 규칙: 한 번에 다 바꾸지 않는다(무엇이 효과였는지 알 수 없어서). 성과가 내려가면 되돌린다.
import sys, os, re, json, glob, time, subprocess, statistics
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
DESIGN = os.path.join(HERE, 'design.json'); LOG = os.path.join(HERE, 'loop_log.json')
SPEC = os.path.join(R, 'yt', 'design', 'spec.json')
SAMPLE = os.path.join(R, 'yt', 'design', 'ours'); os.makedirs(SAMPLE, exist_ok=True)
PY = [sys.executable]
LOCK = os.path.join(HERE, '.loop.lock')

def take_lock(stale=3600):
    """한 번에 한 바퀴만 돈다. 2026-09-24 15시 회차에 바퀴 둘이 겹쳐 돌아 격자 측정이 섞였다 —
    앞 바퀴가 그린 샘플을 뒤 바퀴가 재는 바람에 text_spread 격자 7점이 전부 같은 값(0.2653)으로 나왔고,
    그 '전부 같음'을 최선으로 골라 손잡이를 0.45→0.0 으로 옮겨 판형 오차가 0.2653 → 2.213 으로 뛰었다."""
    try:
        if os.path.exists(LOCK) and time.time() - os.path.getmtime(LOCK) < stale:
            age = int(time.time() - os.path.getmtime(LOCK))
            print(f'다른 바퀴가 {age}초째 돌고 있다 — 이번 바퀴는 돌지 않는다 ({LOCK})')
            return False
        open(LOCK, 'w', encoding='utf-8').write(str(os.getpid()))
        return True
    except Exception:
        return True

def drop_lock():
    try: os.remove(LOCK)
    except Exception: pass

DEFAULT = {   # 생성기가 읽는 값. 처음 값은 2026-09-23 첫 측정에서 나온 경쟁 상위 중앙값
    'long':  {'yellow': 0.050, 'contrast': 0.372, 'white': 0.101, 'text_top': 0.911, 'bright': 0.447},
    'short': {'yellow': 0.007, 'contrast': 0.187, 'white': 0.012, 'text_mid': 0.430, 'bright': 0.216},
    'title': {'quote': True, 'region': True, 'number': True, 'warn': False, 'len': 33},
    'video': {'scene_sec': 9.0, 'total_sec': 45, 'zoom': 0.0009},
    'step': 0,
}

def sh(*a, timeout=1800):
    r = subprocess.run(PY + list(a), capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=timeout, cwd=os.path.dirname(HERE))
    return (r.stdout or '') + (r.stderr or '')

def load(p, d):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d

def our_shorts_stats():
    """우리가 올린 영상의 조회수 — 조정이 효과 있었는지 보는 유일한 답.
    id·공개상태까지 돌려준다. 2026-09-24에 알아낸 것: 최근 10편을 '합계'로 재면 새 영상을 올릴 때마다
    합계가 무너진다(2089 → 120 → 6). 새로 올린 영상은 조회 0이라 최신 10편 합계가 떨어지는 것이지
    디자인이 나빠진 게 아니다. 그래서 회차 판정은 채널 총조회(누적, 절대 안 줄어든다)로 한다."""
    out = sh(os.path.join(HERE, 'ytupload.py'), 'stats')
    vids = re.findall(r'(\d{4}-\d{2}-\d{2})\s+(\d+)\s*회\s*\|\s*(\w+)\s*\|\s*([\w-]{6,})\s*\|\s*(.+)', out)
    rows = [{'date': d, 'views': int(v), 'privacy': pv, 'id': vid, 'title': t.strip()} for d, v, pv, vid, t in vids]
    if not rows:   # 옛 형식(아이디 없음)도 읽는다
        rows = [{'date': d, 'views': int(v), 'privacy': '?', 'id': '', 'title': t.strip()}
                for d, v, t in re.findall(r'(\d{4}-\d{2}-\d{2})\s+(\d+)\s*회\s*\|\s*(.+)', out)]
    m = re.search(r'총조회\s*(\d+)', out)
    total = int(m.group(1)) if m else None
    return rows, total

def render_samples(keep_chart=False):
    """지금 설정으로 샘플 썸네일을 새로 그린다 — 이게 있어야 조정 효과가 다음 측정에 나타난다.
    쇼츠 샘플을 '배경 없이' 그리던 것이 6회차 막힘의 진짜 원인이었다(step19~26). 실제 쇼츠(shorts.py:116)는
    첫 장면 자료 화면을 배경으로 깔고 썸네일을 만드는데, 여기서만 맨 그라데이션 위에 글자 두 줄을 그렸다.
    자료 화면이 없으면 글자 말고는 가장자리가 없어 text_top이 손잡이를 어떻게 돌려도 0.0329에 얼어붙는다
    (실측: 같은 설정 + 차트 배경 → text_top 0.0329→0.5178, text_mid 0.1167→0.3902, text_bot 0.1299→0.2211).
    경쟁은 전부 사진·자료 위에 글자를 얹은 판형이라, 배경 없는 샘플로 재는 것은 애초에 다른 물건을 재는 것이었다.
    그래서 production이 실제로 쓰는 자료 화면 세 종류(차트·히트맵·부동산 화면) 위에 그려 중앙값을 낸다(2026-09-23).
    """
    for p in glob.glob(os.path.join(SAMPLE, '*.png')):
        if keep_chart and os.path.basename(p) == '_bg_chart.png': continue
        try: os.remove(p)
        except OSError: pass
    shots = os.path.join(R, '_shots')
    chart = os.path.join(SAMPLE, '_bg_chart.png')   # 이름이 short*/long* 이 아니라 측정에서는 빠진다
    if not (keep_chart and os.path.exists(chart)):
        sh(os.path.join(HERE, 'chartimg.py'), 'bar', '서울 구별 전세가율', chart,
           '금천=61', '구로=58', '중랑=56', '강북=55', '노원=53', '강남=36',
           '--unit', '%', '--hi', '3', '--short', '--source', '국토부 실거래가')
    bgs = [chart, os.path.join(shots, 'heatmap_re_jeonse_2026-09-23.png'), os.path.join(shots, 'naverland_test.png')]
    for i, bg in enumerate([b for b in bgs if os.path.exists(b)]):
        sh(os.path.join(HERE, 'thumb.py'), '금천 61% 강남 36%', '서울 전세가율 전수 조사',
           os.path.join(SAMPLE, f'short{i}.png'), bg, '--short')
    bg = os.path.join(shots, 'heatmap_2026-09-23.png')
    sh(os.path.join(HERE, 'thumb.py'), '전세가율 61% vs 36%', '서울 25개 구 전부 계산', os.path.join(SAMPLE, 'long.png'), *( [bg] if os.path.exists(bg) else [] ))

def measure_ours():
    """우리 썸네일을 경쟁과 같은 자로 잰다. 쇼츠는 배경 종류별로 여러 장이라 뒤에서 중앙값을 낸다"""
    sys.path.insert(0, HERE)
    import thumbstat
    rows = []
    for pat, isshort in (('short*.png', True), ('long*.png', False)):
        for p in sorted(glob.glob(os.path.join(SAMPLE, pat))):
            st = thumbstat.measure(p)
            if st: rows.append({**st, 'file': os.path.basename(p), 'short': isshort})
    return rows

def thumb_defaults():
    """thumb.py가 design.json 없이 쓰는 기본값 — 새 손잡이의 출발점"""
    sys.path.insert(0, HERE)
    try:
        import thumb
        return {k: thumb.cfg(k) for k in ('long', 'short')}
    except Exception:
        return {}

THUMB_DEFAULT = {}

# ── 세 칸(위·가운데·아래)은 손잡이 하나를 나눠 쓴다 ────────────────────────────────
# 한 칸씩 "우리-경쟁" 만큼 밀면 서로 반대로 밀어 영원히 흔들린다. 2026-09-23 실측(쇼츠, 배경 3종 중앙값):
#   text_spread  0.0    top 0.2264  mid 0.4856  bot 0.2149
#                0.3    top 0.2264  mid 0.4903  bot 0.2149
#                0.45   top 0.3079  mid 0.3792  bot 0.1711
#                0.6304 top 0.3441  mid 0.2375  bot 0.2831   ← 지금 값
#                1.0    top 0.3804  mid 0.2375  bot 0.2318
#   경쟁 상위     top 0.2748  mid 0.4241  bot 0.3093
# 위·가운데는 낮은 쪽을, 아래는 높은 쪽을 원한다 — 한 손잡이로 셋을 동시에 맞출 수 없다.
# 그래서 밀지 않고 "재서 고른다": 격자마다 실제로 그려 재고, 세 칸 상대오차 합이 가장 작은 값을 쓴다.
# (text_mid 가 5회차 넘게 "듣지 않는 손잡이"로 막혀 있던 진짜 이유 — 쇼츠에서 text_y 를 보고 있었다.
#  실측하면 text_y 는 text_mid 를 0.2375~0.3674 안에서만 흔들어 목표 0.4241 에 닿지 못한다.)
BAND_KEYS = ('text_top', 'text_mid', 'text_bot')
BAND_KNOB = {'long': 'text_y', 'short': 'text_spread'}
BAND_GRID = {'long':  [0.20, 0.35, 0.50, 0.62, 0.72, 0.80],
             'short': [0.0, 0.15, 0.30, 0.45, 0.60, 0.80, 1.0]}
# 손잡이 하나로는 세 칸을 못 맞춘다(2026-09-24 실측): 쇼츠 두 줄 판형은 text_spread 를 한계 1.0 까지 올려도
# text_bot 0.203 에서 멈췄다(경쟁 0.3093). 칸이 둘뿐인데 목표는 셋이라 구조적으로 못 닿는 것이었다.
# 그래서 아랫줄을 띄어쓰기에서 둘로 나눠 세 칸을 채우고(thumb.lines=3), 나뉘어 짧아진 두 줄을
# 폭 여유만큼 키우는 split_scale 을 두 번째 손잡이로 뒀다. 실측(lines=3): 1.0 → bot 0.1091,
# 1.3 → 0.1565, 1.6 → 0.2144, 2.0 → 0.3035(세 칸 오차 합 0.8496 → 0.4092; 두 줄 판형 최선은 0.7165).
BAND_KNOB2 = {'short': ('split_scale', [1.0, 1.3, 1.6, 2.0, 2.4, 2.8])}
# 격자 끝점에 최선이 붙으면 "유지(가장 작다)"는 수렴이 아니라 격자가 짧다는 뜻이다.
# split_scale 은 72회차까지 늘 끝점 2.0 이 최선이었고(오차 1.0121→0.728→0.5784→0.2653, 계속 내려감)
# 그릴 때 thumb.py 가 2.0 으로 깎고 있어 판형 오차가 0.2653 에 얼어 있었다(2026-09-24).
# 그래서 (1) thumb.py 한계를 3.2 로 넓히고 (2) 끝점에 붙으면 아래 한계까지 격자를 저절로 늘린다.
KNOB_LIMIT = {'text_spread': (0.0, 1.0),      # thumb.py 가 0~1 로 깎는다
              'text_y':      (0.15, 0.80),    # thumb.py 가 0.15~0.80 으로 깎는다
              'split_scale': (1.0, 3.2)}      # thumb.py 윗한계와 같게 유지한다

def band_err(rows, kind, spec):
    """세 칸 상대오차 합. 작을수록 경쟁 판형에 가깝다"""
    tgt = spec.get(kind) or {}
    mine = [r for r in rows if (r['short'] if kind == 'short' else not r['short'])]
    if not mine or not tgt: return None, {}
    got = {k: statistics.median(r[k] for r in mine) for k in BAND_KEYS if k in tgt}
    if not got: return None, {}
    return sum(abs(got[k] - tgt[k]) / max(tgt[k], 1e-3) for k in got), got

def ctx_tag(design, kind, knob):
    """그 판형에서 '지금 움직이려는 손잡이 말고 나머지'가 어디에 있는지를 짧은 지문으로 만든다.
    같은 지문에서 잰 값끼리만 견줄 수 있다 — 다른 손잡이가 움직인 뒤의 값과 섞으면 손잡이가 듣는지 안 듣는지,
    목표를 지나쳤는지 아닌지를 알 수 없다."""
    import hashlib
    d = design.get(kind, {})
    body = ';'.join(f'{k}={round(float(v), 4) if isinstance(v, (int, float)) else v}'
                    for k, v in sorted(d.items()) if k != knob)
    return hashlib.md5(body.encode('utf-8')).hexdigest()[:6]


def grid_pick(design, spec, kind, knob, base_grid, did, blocked):
    """손잡이 하나를 격자로 실제로 그려 재고 가장 나은 값을 고른다. 미는 게 아니라 재는 것이라 흔들리지 않는다"""
    d = design.setdefault(kind, {})
    cur = d.get(knob)
    if cur is None:
        cur = float(THUMB_DEFAULT.get(kind, {}).get(knob, 0.0))
    grid = sorted(set(base_grid + [round(float(cur), 4)]))
    table, failed = [], []

    def measure(vals):
        """격자 점들을 실제로 그려 재서 table 에 넣는다. 못 재면 failed 에 표시한다"""
        for v in vals:
            if any(abs(t['v'] - v) < 1e-9 for t in table): continue
            d[knob] = v
            json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            render_samples(keep_chart=True)
            err, got = band_err(measure_ours(), kind, spec)
            if err is None: failed.append(v); return
            table.append({'v': v, 'err': round(err, 4), **{k: round(x, 4) for k, x in got.items()}})
        table.sort(key=lambda t: t['v'])

    measure(grid)
    if failed or not table:
        blocked.append(f'{kind} 세 칸 맞추기 — 샘플이나 경쟁 기준이 없어 못 쟀다'); d[knob] = cur; return
    def pick():
        # 비긴 값끼리는 지금 값을 이긴 것으로 치지 않는다. 격자 전체가 같은 값으로 나오는 경우(손잡이가
        # 안 듣거나 측정이 섞인 경우)에 min() 은 늘 격자의 맨 아래값을 골라 손잡이를 끝으로 밀어 버린다.
        best = min(table, key=lambda t: t['err'])
        here = next((t for t in table if abs(t['v'] - cur) < 1e-9), None)
        if here is not None and here['err'] <= best['err'] + 1e-4: return here
        return best

    # 끝점에 최선이 붙어 있으면 수렴이 아니다 — 한계까지 격자를 늘려 실제로 넘어가 본다.
    lo_lim, hi_lim = KNOB_LIMIT.get(knob, (None, None))
    for _ in range(3):
        best, vs = pick(), [t['v'] for t in table]
        step = max((round(b - a, 4) for a, b in zip(vs, vs[1:])), default=0) or 0.1
        if abs(best['v'] - vs[-1]) < 1e-9 and hi_lim is not None and vs[-1] < hi_lim - 1e-9:
            nxt = [round(min(vs[-1] + step * i, hi_lim), 4) for i in (1, 2)]
        elif abs(best['v'] - vs[0]) < 1e-9 and lo_lim is not None and vs[0] > lo_lim + 1e-9:
            nxt = [round(max(vs[0] - step * i, lo_lim), 4) for i in (1, 2)]
        else:
            break                                   # 안쪽에서 최선이 나왔다 = 진짜 수렴
        measure(sorted(set(nxt)))
        if failed: break
        did.append(f'{kind}.{knob} 격자 끝점({best["v"]})에 최선이 붙어 한계 {hi_lim if nxt[0] > best["v"] else lo_lim} 쪽으로 {nxt} 를 더 재 봤다')
    best = pick()
    vs = [t['v'] for t in table]
    if abs(best['v'] - vs[-1]) < 1e-9 and hi_lim is not None and abs(vs[-1] - hi_lim) < 1e-9:
        # 한계까지 갔는데도 끝점이 최선이다 — 격자가 아니라 그리기 한계가 막고 있다. 숨기지 않고 남긴다.
        blocked.append(f'{kind}.{knob} 가 그리기 한계 {hi_lim} 에서 멈췄다 — 오차 {best["err"]} 는 손잡이를 더 넓혀야 줄어든다')
    d[knob] = best['v']
    json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if best['v'] != cur:
        was = next((t for t in table if t['v'] == cur), None)
        did.append(f"{kind}.{knob} {cur} → {best['v']} (세 칸 오차 합 {was['err'] if was else '?'} → {best['err']}, 격자 {len(table)}점 실측)")
    else:
        did.append(f"{kind}.{knob} {cur} 유지 (격자 {len(table)}점 중 오차 합 {best['err']} 이 가장 작다)")
    return table


def tune_bands(design, spec, kind, did, blocked):
    """세 칸 맞추기. 손잡이를 하나씩 차례로 골라 내려간다(좌표 하강) — 곱으로 다 돌면 너무 오래 걸린다."""
    table = grid_pick(design, spec, kind, BAND_KNOB[kind], BAND_GRID[kind], did, blocked)
    if kind in BAND_KNOB2 and table:
        k2, g2 = BAND_KNOB2[kind]
        table = grid_pick(design, spec, kind, k2, g2, did, blocked) or table
    return table


def main():
    global THUMB_DEFAULT
    THUMB_DEFAULT = thumb_defaults()
    if not take_lock(): return
    t0 = time.time(); log = load(LOG, []); design = load(DESIGN, DEFAULT)
    step = design.get('step', 0) + 1
    did, blocked = [], []

    # 1) 수집 — 경쟁(하루 한 번이면 충분하므로 마지막 수집이 12시간 넘었을 때만)
    last = log[-1]['at'] if log else '2000-01-01 00:00'
    if time.time() - time.mktime(time.strptime(last, '%Y-%m-%d %H:%M')) > 12 * 3600:
        out = sh(os.path.join(HERE, 'ytdesign.py'), '--all', '40', timeout=2400)
        did.append('경쟁 수집: ' + str(len(re.findall(r'구독', out))) + '채널')
    ours_before, ch_views = our_shorts_stats()

    # 2) 측정
    out = sh(os.path.join(HERE, 'thumbstat.py'), timeout=1200)
    m = re.search(r'썸네일 (\d+) 장 측정', out); did.append(f'경쟁 썸네일 {m.group(1) if m else "?"}장 재측정')
    spec = load(SPEC, {})
    # 2-b) 세 칸(위·가운데·아래)은 손잡이 하나를 나눠 쓰므로 밀지 않고 격자로 재서 고른다
    bands = {}
    for kind in ('short', 'long'):
        if spec.get(kind): bands[kind] = tune_bands(design, spec, kind, did, blocked)
    render_samples(keep_chart=True)   # 고른 값으로 샘플을 새로 그린다
    ours = measure_ours()             # 그 샘플만 잰다
    # 조회로는 판정할 수 없을 때(전부 비공개) 쓸 판정 눈금 — 경쟁 판형과의 세 칸 거리.
    # 이 값은 공개 여부와 무관하게 매 회차 재어지므로, 조정이 실제로 경쟁에 가까워졌는지 숫자로 남는다.
    px_err = {}
    for kind in ('short', 'long'):
        e, _ = band_err(ours, kind, spec)
        if e is not None: px_err[kind] = round(e, 4)

    # 3) 비교 — 우리 평균 vs 경쟁 상위 중앙값
    gaps = []
    for kind in ('short', 'long'):
        tgt = spec.get(kind) or {}
        mine = [r for r in ours if (r['short'] if kind == 'short' else not r['short'])]
        if not mine or not tgt: continue
        for k, want in tgt.items():
            if k not in ('yellow', 'contrast', 'white', 'bright', 'text_top', 'text_mid', 'text_bot', 'sat', 'dark'): continue
            got = statistics.median(r[k] for r in mine)
            if want and abs(got - want) / max(want, 1e-3) > 0.25:
                gaps.append({'kind': kind, 'key': k, 'ours': round(got, 4), 'target': round(want, 4), 'diff': round(got - want, 4)})
    gaps.sort(key=lambda g: -abs(g['diff'] / max(g['target'], 1e-3)))

    # 4) 조정 — 측정 차이를 '그리기 손잡이'로 옮긴다. (손잡이, 방향계수, 최소~최대)
    BINARY = {'yellow_bottom', 'num_yellow'}
    RULE = {
      # ※ text_top/text_mid/text_bot 항목은 2026-09-23부터 tune_bands(격자 실측)가 맡는다. 아래 계수는 그때까지의 기록으로 남겨 둔다.
      # 손잡이·계수·한계는 판형별로 다르게 둘 수 있다({'long':..,'short':..}). 쇼츠는 세로 1920이라 두 줄을 붙여 두면
      # text_y를 어디로 옮겨도 top·bot 두 칸을 같이 못 채운다 — 5회차 연속 "듣지 않는 손잡이"로 막혀 있었다(step19~23).
      # 그래서 쇼츠는 두 줄을 위·아래로 벌리는 text_spread(thumb.py)로 바꿨다. 롱폼(1280x720)은 text_y가 듣는다.
      # 쇼츠 계수는 실측 5점(spread 0/.3/.5/.7/1.0)에서 나온 기울기다: text_bot 0→0.1265(0.5에서 포화),
      # text_top 0.0329→0.1496, text_mid 0.2245→0(반대로 줄어든다). 기울기 0.25/단위 → 계수 -4.0.
      # 0.55 위로는 아랫줄이 화면 아래 한계에 붙어 더 안 움직이므로 한계를 0.55로 둔다.
      # 2026-09-23 step30 재실측(쇼츠 배경 3종 중앙값, spread 0.4/0.55/0.7/0.85/1.0):
      #   text_bot 0.1117/0.1117/0.1260/0.2310/0.2416 — 0.55~0.7 구간이 평평해서 "한계에 붙었다"고 오판했을 뿐,
      #   0.85를 넘기면 다시 오른다. 한계를 1.0으로 열고 기울기 0.2887/단위에서 계수 -3.5를 다시 냈다.
      'text_top': ({'long': 'text_y', 'short': 'text_spread'}, {'long': +0.45, 'short': -3.5},
                   {'long': 0.15, 'short': 0.0}, {'long': 0.80, 'short': 1.0}),
      'text_bot': ({'long': 'text_y', 'short': 'text_spread'}, {'long': -0.45, 'short': -3.5},
                   {'long': 0.15, 'short': 0.0}, {'long': 0.80, 'short': 1.0}),
      # 밝기: 상한 0.9는 '원본 그대로'라 롱폼이 0.2825에서 멈춰 목표 0.4307에 닿지 못했다(step30 막힘).
      # thumb.py 클램프를 1.8까지 열고 실측(0.6/0.9/1.2/1.5/1.8 → bright 0.2255/0.2825/0.3386/0.3926/0.4402),
      # 기울기 0.1752/단위 → 계수 -5.7. 옛 -1.2는 기울기의 1/5라 한 칸에 0.02씩만 올라가 상한에 먼저 붙었다.
      'bright':   ('bg_bright', -5.7, 0.12, 1.80),
      'dark':     ('bg_bright', +3.8, 0.12, 1.80),
      # 배경 채도. 2026-09-23 실측(bg_sat 0.4/0.8/1.5/2.2/3.0 → sat 0.0985/0.1871/0.3197/0.4167/0.4971),
      # 기울기 0.1533/단위 → 계수 -6.5. 여섯 회차 "그리기 손잡이 없음"이던 항목이다.
      'sat':      ('bg_sat', -6.5, 0.0, 3.0),
      # 흰 면적은 흰 글자 픽셀에서 나온다. 외곽선은 검정이라 아무리 얇게 해도 흰 면적이 안 줄어 stroke_ratio가 한계 40에 붙어
      # 버렸다(2026-09-23 step20). 그래서 글자 크기 배율로 바꿨다. 면적은 크기의 제곱이라 계수를 작게 잡아 한 칸씩 간다.
      # 흰 면적과 아랫줄 글자량이 같은 손잡이(text_scale)를 공유한다 — 2026-09-23 실측(spread 1.0 고정,
      # text_scale 0.66/0.8/0.9/1.0 → text_bot 0.2251/0.2603/0.2803/0.3112, white 0.0114/0.0167/0.0205/0.0257).
      # 쇼츠는 목표가 서로 반대라(text_bot 0.3093 ↑ / white 0.0107 ↓) 둘 다 만족하는 값이 없어 하한 0.9에 붙어
      # step38~39 두 회차 연속 "한계에 붙어 더 못 감"으로 막혔다.
      # 2026-09-24: 쇼츠를 text_tint(줄마다 아래쪽 몇 %를 아이보리로 칠하나, thumb.py)로 바꿨다. 글자 크기를
      # 건드리지 않으므로 white 와 text_bot 이 더는 싸우지 않는다 — 실측(tint 0/0.2/0.4/0.6/0.8/1.0):
      #   white     0.0273/0.0273/0.0236/0.0150/0.0066/0.0003   (목표 0.0107 이 구간 안에 있다)
      #   yellow    0.0086 전 구간 그대로 — 강조색을 얼음빛 파랑으로 잡아 노랑 손잡이와 안 싸운다
      #   text      0.2667 전 구간 그대로, text_bot 0.1898 도 그대로 — 글자량은 1픽셀도 안 줄어든다
      # 0.4~1.0 기울기 -0.0388/단위 → 계수 +25.8(흰 면적은 tint가 커질수록 줄어들어 부호가 text_scale과 반대).
      # 0~0.2는 아직 임계(채도 40)를 못 넘어 평평하다. 롱폼은 white 차이가 없어 그대로 text_scale 을 쓴다.
      # 2026-09-24 화면 검증: 75회차가 text_tint 를 0.726 → 1.0(한계)로 올렸다. 숫자로는 white 가 목표에
      # 다가가지만 실제 썸네일을 보니 글자가 흰빛을 잃고 잿빛 파랑으로 죽어 배경 차트 위에서 안 읽힌다.
      # 같은 배경·같은 문구로 0.7 / 0.85 / 1.0 을 그려 눈으로 견줬고 0.7 에서만 글자가 희게 남았다.
      # tint_v 하한 0.75 와 같은 이유로 윗한계를 0.7 로 막는다 — 숫자를 맞추려고 글자를 죽이지 않는다.
      # 그래서 short.white 는 앞으로 '한계에 붙어 막힘'으로 남는다. 그게 맞는 상태다.
      'white':    ({'long': 'text_scale', 'short': 'text_tint'}, {'long': -10.0, 'short': +25.8},
                   {'long': 0.66, 'short': 0.0}, {'long': 1.0, 'short': 0.7}),
      # 아랫줄 노랑 글자 비율(0~1). 2026-09-23 실측 5점(0/.25/.5/.75/1): 롱폼 0.0007→0.0533, 쇼츠 0.0003→0.0199.
      # 기울기가 판형마다 달라(롱폼 0.052 · 쇼츠 0.020) 계수를 판형별로 둔다.
      # 2026-09-24: 쇼츠는 yellow_frac 으로 못 맞춘다. 그 손잡이는 '글자 몇 개'라 계단이기 때문이다 —
      # 실측 0/0.0997 → 0.0003 · 0.1088~0.2 → 0.0099 · 0.3~0.6 → 0.0169 · 1.0 → 0.0345.
      # 경쟁 목표 0.0067 이 '0개'와 '1개' 사이에 있어 53~61회차 내내 "사이를 좁혔는데도 못 맞춘다"로 막혔다.
      # 그래서 쇼츠는 yellow_tint(마지막 줄 글자의 아래쪽 몇 %를 노랑으로 칠하나, thumb.py)로 바꿨다.
      # 새 잉크를 안 더해서 글자량·대비가 안 흔들린다 — 실측(tint 0.34/0.38/0.42/0.46):
      #   yellow   0.0006/0.0022/0.0049/0.0071   (목표 0.0067 이 구간 안에 있다)
      #   text_bot 0.3008/0.3007/0.3009/0.3009 · text 0.3397 전 구간 그대로 · contrast 0.2622~0.2639 그대로
      # 0.30 아래는 글자 아래 빈 공간이라 평평하다(0.0003) — 하한을 0.30 으로 둬 죽은 구간에 안 들어가게 한다.
      # 기울기 0.061/단위 → 계수 -16.4.
      # 밑줄(형광펜) 안도 실측했지만 버렸다: 노랑은 잘 듣는데 text_bot 이 0.3009 → 0.3894 로 뛴다
      # (측정의 글자 지도가 가장자리를 25x9 로 부풀려 가로줄 하나가 아래 칸을 통째로 글자로 만든다).
      'yellow':   ({'long': 'yellow_frac', 'short': 'yellow_tint'}, {'long': -19.0, 'short': -16.4},
                   {'long': 0.0, 'short': 0.30}, 1.0),
      # 대비. 롱폼은 패널 진하기로 민다. 쇼츠는 panel_alpha 가 듣지 않는 손잡이였다(128→0.2623, 150→0.2638).
      # 2026-09-24 갈라 재서 원인을 찾았다(경쟁 상위 10장 vs 우리 3장, 글자 지도로 갈라 잰 값):
      #   배경만 대비   우리 0.0531 < 경쟁 0.0734  ← 우리 배경은 이미 경쟁보다 평평하다
      #   글자자리 대비 우리 0.4063 > 경쟁 0.2732 · 아주 밝은 픽셀(V>0.80) 우리 0.0913 vs 경쟁 0.0235
      # tools-wanted.md 에 "배경을 누르는 손잡이(bg_flat)를 달아야 하나, 자료가 보여야 한다는 지시와 부딪힌다"고
      # 사람 판단을 올려 뒀던 항목인데, 숫자가 아니라고 답했다 — 배경은 건드릴 것이 아니다.
      # 넘치는 대비는 얼음빛 파랑(V=255)으로 글자 아래 88%를 칠한 데서 온다. 그래서 강조색 밝기(tint_v)를 단다.
      # 실측(tint_v 1.0/0.85/0.7/0.55/0.4): contrast 0.2619/0.2285/0.1977/0.1698/0.1463
      #   white 0.0137/0.0126/0.0125/0.0110/0.0106 · yellow 0.0071~0.0077 · text_bot 0.3009 전 구간 그대로.
      # 기울기 0.1827/단위 → 계수 -5.47.
      # 하한 0.75 는 화면 검증에서 나왔다(2026-09-24). tint_v 0.6 은 숫자로는 목표(0.1791)에 딱 맞는데
      # 실제 그림을 보니 글자가 흰빛을 잃고 회색으로 죽는다 — 썸네일이 해야 할 일(눈에 띄기)을 잃는다.
      # 숫자를 맞추려고 글자를 죽이지 않는다. 0.75 아래로는 안 내려간다. 그래서 못 닫으면 '막힘'으로 남는 게 맞다.
      'contrast': ({'long': 'panel_alpha', 'short': 'tint_v'}, {'long': -260.0, 'short': -5.47},
                   {'long': 60, 'short': 0.75}, {'long': 230, 'short': 1.0}),
      'text_mid': ('text_y', 'center', 0.15, 0.80),   # 가운데 띠에 글자가 없으면 text_y를 0.5 쪽으로 당긴다
    }
    # 손잡이 없는 차이가 위쪽 세 자리를 잡아먹지 않게 먼저 갈라 둔다
    knobbed = [g for g in gaps if g['key'] in RULE and g['key'] not in BAND_KEYS]
    for g in gaps:
        if g['key'] in BAND_KEYS: continue      # 2-b 격자 탐색이 이미 최선을 골랐다. 여기서 또 밀면 서로 밀쳐 흔들린다
        if g['key'] not in RULE:
            blocked.append(f"{g['kind']}.{g['key']} 우리 {g['ours']} vs 경쟁 {g['target']} — 그리기 손잡이 없음")
    memo = design.setdefault('_memo', {})   # "종류.항목.손잡이=값" → 그 값일 때 실측치. 같은 자리를 또 밟지 않으려고 적어 둔다
    moved_knobs = set()   # 같은 손잡이를 한 바퀴에 두 번 움직이면 뒤 항목이 앞 항목을 덮어써 값이 계속 뒤집힌다(2026-09-23)
    def bykind(v, kind):
        return v.get(kind) if isinstance(v, dict) else v
    for g in knobbed[:3]:
        knob, coef, lo, hi = (bykind(v, g['kind']) for v in RULE[g['key']])
        if knob is None: continue
        if (g['kind'], knob) in moved_knobs:
            blocked.append(f"{g['kind']}.{g['key']} — 같은 손잡이 {knob} 를 이번 바퀴에 다른 항목이 이미 움직였다, 다음 바퀴에 잰다")
            continue
        if coef is None: continue
        d = design.setdefault(g['kind'], {})
        cur = d.get(knob)
        if cur is None:
            # 새로 생긴 손잡이는 thumb.py가 쓰는 기본값에서 시작한다. 예전에는 text_spread만 열어 둬서
            # bg_sat 같은 새 손잡이를 RULE에 넣어도 design.json에 없다는 이유로 영영 건너뛰었다(2026-09-23).
            cur = d[knob] = float(THUMB_DEFAULT.get(g['kind'], {}).get(knob, 0.0))
        tag = f"{g['kind']}.{g['key']}.{knob}"
        # 실측치는 '그때 나머지 손잡이가 어디에 있었나'에 딸려 있다. 예전에는 손잡이 값만 적어 둬서, 다른 손잡이가
        # 움직인 뒤에 잰 값과 그 전에 잰 값을 같은 줄에 놓고 비교했다 — short.white 실측이 text_tint 0.7689/0.8059/
        # 0.85/0.9455 에서 0.0076/0.0184/0.0144/0.0028 로 오르락내리락한 것이 그 탓이다(강조색 얼음빛 파랑이
        # 채도 40 아래라 흰 면적으로 세어져, yellow_frac 이 움직이면 white 도 같이 움직인다). 그래서 나머지 설정을
        # 지문으로 같이 적고, 값끼리 견줄 때는 지문이 같은 것만 쓴다.
        ctx = ctx_tag(design, g['kind'], knob)
        memo[f'{tag}={cur}@{ctx}'] = g['ours']
        seen, same = {}, {}   # seen: 지문 상관없이 전부(듣는 손잡이인지 보는 용도) · same: 지문이 지금과 같은 것만
        for mk, mo in memo.items():
            if not mk.startswith(tag + '='): continue
            v, _, c = mk[len(tag) + 1:].partition('@')
            seen[v] = mo
            if c == ctx: same[v] = mo
        # 손잡이를 움직였는데 실측이 그대로면 그 항목에 듣지 않는 손잡이다 — 더 돌리지 않는다
        if len(seen) > 1 and max(seen.values()) - min(seen.values()) < 0.002:
            blocked.append(f"{g['kind']}.{g['key']} — {knob} 를 {'/'.join(sorted(seen))} 로 바꿔도 실측 그대로, 듣지 않는 손잡이")
            continue
        # 이미 잰 값들이 목표를 위·아래로 끼고 있으면(사이에 낀다) 계수로 미는 대신 그 사이를 갈라 들어간다.
        # 계수 밀기는 한 방향으로만 가므로 한 번 목표를 지나쳐 버리면 되돌아올 길이 없다 — 다음 회차에 그 값을
        # 다시 제안해도 "이미 재봤고 더 나빴다"에 걸려 영영 그 자리에 선다. short.white 가 그 꼴이었다:
        # text_tint 0.85 → 0.0144(목표 0.0107 위), 0.9455 → 0.0028(아래). 답은 두 값 사이인데 38~50회차 내내
        # 못 들어갔다. 사이에 낀 두 점을 직선으로 이어 목표를 지나는 자리를 집으면 한 번에 들어간다.
        if coef != 'center' and knob not in BINARY and len(same) > 1:
            pts = []
            for v, o in same.items():
                try: pts.append((float(v), o))
                except ValueError: pass
            hi_pts = [(v, o) for v, o in pts if o > g['target']]
            lo_pts = [(v, o) for v, o in pts if o < g['target']]
            pair = min(((a, b) for a in hi_pts for b in lo_pts), key=lambda ab: abs(ab[0][0] - ab[1][0]), default=None)
            if pair:
                (va, oa), (vb, ob) = pair
                span = abs(hi - lo) if hi is not None and lo is not None else 1.0
                if abs(va - vb) <= max(span * 0.01, 1e-4):
                    blocked.append(f"{g['kind']}.{g['key']} — {knob} {min(va, vb)}~{max(va, vb)} 까지 좁혔는데도 목표 {g['target']} 를 못 맞춘다, 다른 손잡이가 필요")
                    continue
                hit = va + (vb - va) * (g['target'] - oa) / (ob - oa)
                hit = min(max(hit, min(va, vb)), max(va, vb))
                cand = round(hit, 4) if isinstance(cur, float) else int(round(hit))
                if str(cand) in same or cand == cur:
                    blocked.append(f"{g['kind']}.{g['key']} — {knob} 사이 가르기가 이미 재본 {cand} 로 돌아온다, 다른 손잡이가 필요")
                    continue
                moved_knobs.add((g['kind'], knob))
                d[knob] = cand
                did.append(f"{g['kind']}.{knob} {cur} → {cand} ({g['key']} 목표 {g['target']} 를 {va}={oa}/{vb}={ob} 사이에서 갈라 집음)")
                continue
        # 계수는 모두 '우리 - 경쟁' 기준으로 적혀 있다(주석 참고). 부호를 뒤집지 말 것.
        if coef == 'center':
            # 가운데 띠 비율은 text_y에 대해 단조가 아니다 — 0.5 쪽으로 당기기만 한다
            if g['ours'] >= g['target']: continue
            delta = (g['target'] - g['ours']) * 0.45 * (1 if 0.5 > cur else -1)
        else:
            delta = (g['ours'] - g['target']) * coef
        new = min(max(cur + delta, lo), hi)
        if knob in BINARY:                       # 0/1 스위치 — 0.5를 넘어서면 뒤집는다
            new = 1 if cur + delta >= 0.5 else 0
        else:
            new = round(new, 4) if isinstance(cur, float) else int(round(new))
        if new == cur:
            if cur in (lo, hi): blocked.append(f"{g['kind']}.{g['key']} — {knob} 가 한계 {cur} 에 붙어 더 못 감, 다른 손잡이가 필요")
            continue
        moved_knobs.add((g['kind'], knob))
        prev = same.get(str(new))
        if prev is not None and abs(prev - g['target']) >= abs(g['ours'] - g['target']):
            blocked.append(f"{g['kind']}.{g['key']} — {knob}={new} 는 이미 재봤고 더 나빴다({prev} vs 지금 {g['ours']}), 그대로 둠")
            continue
        d[knob] = new
        did.append(f"{g['kind']}.{knob} {cur} → {new} ({g['key']} 우리 {g['ours']} vs 경쟁 {g['target']})")
    if not gaps: did.append('썸네일 수치는 경쟁 상위와 25% 안쪽 — 조정 없음')

    # 5) 지난 조정의 효과 판정
    # 2026-09-24에 고친 것: 예전에는 '최신 10편 조회 합계'로 판정했다. 새 영상을 올리면 그 합계가
    # 무너지므로(실측 2089 -> 120 -> 6) 발행할 때마다 "조회 하락"으로 읽혀 직전 회차의 조정을 전부 되돌렸다.
    # 그래서 short.contrast / short.white 는 회차마다 넣었다 뺐다만 반복하고 영영 안 닫혔다(step 64~66).
    # 이제는 (a) 누적이라 절대 줄지 않는 채널 총조회로 '시간당 늘어난 조회'를 재고,
    #        (b) 그 창에서 실제로 늘어난 조회가 MIN_GAIN 미만이면 판정을 보류한다(되돌리지 않는다).
    #        (c) 최근 10편이 전부 비공개면 조회는 영영 0이므로 그 사실을 판정문에 적어 둔다.
    MIN_GAIN = 30
    verdict, now_rate, prev_rate = '', None, None
    if ch_views is not None and log:
        pv, pat = log[-1].get('ch_views'), log[-1].get('at')
        if pv is None:
            verdict = f'채널 총조회 {ch_views} — 지난 회차 기록이 없어 이번 회차부터 비교한다'
        else:
            hours = max(0.25, (time.time() - time.mktime(time.strptime(pat, '%Y-%m-%d %H:%M'))) / 3600)
            gain = ch_views - pv
            now_rate = round(gain / hours, 2)
            prev_rate = log[-1].get('gain_rate')
            pub = sum(1 for v in ours_before if v.get('privacy') == 'public')
            verdict = (f'채널 총조회 {pv} -> {ch_views} ({gain:+}회 / {hours:.1f}시간 = 시간당 {now_rate})'
                       f' · 최근 10편 중 공개 {pub}편')
            if pub == 0:
                # 2026-09-24에 고친 것: 최근 10편이 전부 비공개면 채널 총조회가 늘어도 그건 **옛 공개 영상**이
                # 번 조회다 — 이번 회차 썸네일 손잡이와 아무 상관이 없다. 그런데도 아래 되돌리기 가지는
                # gain >= MIN_GAIN 만 넘으면 '시간당 조회가 떨어졌다'며 직전 조정을 되돌릴 수 있었다.
                # 공개 0편이면 조회는 판정 근거가 못 되므로 되돌리기에 쓰지 않는다.
                verdict += ' -> 조회로는 판정 안 함(공개 0편, 늘어난 조회는 옛 공개 영상 몫)'
            elif gain < MIN_GAIN:
                verdict += f' -> 판정 보류(늘어난 조회 {gain}회 < {MIN_GAIN}회, 되돌리지 않는다)'
            elif prev_rate is not None and now_rate < prev_rate * 0.7 and log[-1].get('changed'):
                for c in log[-1]['changed']:
                    mm = re.match(r'(\w+)\.(\w+) ([\d.]+) ', c)
                    if mm and mm.group(1) in design and mm.group(2) in design[mm.group(1)]:
                        design[mm.group(1)][mm.group(2)] = float(mm.group(3))
                        did.append(f'되돌림 {mm.group(1)}.{mm.group(2)} -> {mm.group(3)} '
                                   f'(시간당 조회 {prev_rate} -> {now_rate})')

    # 조회가 못 재는 회차에도 '나아졌나'를 숫자로 남긴다 — 경쟁 판형과의 세 칸 거리 비교.
    if px_err:
        prev_px = next((r.get('px_err') for r in reversed(log) if r.get('px_err')), None)
        now_sum = round(sum(px_err.values()), 4)
        if prev_px:
            was_sum = round(sum(prev_px.values()), 4)
            arrow = '줄었다' if now_sum < was_sum - 1e-4 else ('늘었다' if now_sum > was_sum + 1e-4 else '그대로')
            verdict += f' · 경쟁 판형 거리 {was_sum} -> {now_sum} ({arrow})'
        else:
            verdict += f' · 경쟁 판형 거리 {now_sum} (이번 회차부터 비교한다)'

    design['step'] = step
    json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # 바꾼 값으로 우리 샘플을 다시 만든다 — 안 그러면 다음 회차가 같은 차이를 또 잡는다
    if any('→' in d for d in did): did.append('다음 회차가 바뀐 값으로 다시 그려 잰다')
    rec = {'step': step, 'at': time.strftime('%Y-%m-%d %H:%M'), 'sec': int(time.time() - t0),
           'changed': [d for d in did if '→' in d], 'did': did, 'gaps': gaps[:6], 'blocked': blocked[:8], 'bands': bands,
           'ours_views': sum(v['views'] for v in ours_before[:10]) if ours_before else None,
           'ch_views': ch_views, 'gain_rate': now_rate, 'px_err': px_err, 'verdict': verdict}
    log.append(rec); json.dump(log[-200:], open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"[루프 {step}회차] {rec['sec']}초")
    for d in did: print(' ·', d)
    for b in blocked[:8]: print(' · 막힘:', b)
    if verdict: print(' ·', verdict)
    if gaps: print(' 남은 차이:', ', '.join(f"{g['kind']}.{g['key']} {g['ours']}→{g['target']}" for g in gaps[:5]))

if __name__ == '__main__':
    try: main()
    finally: drop_lock()
