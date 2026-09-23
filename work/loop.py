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
    """우리가 올린 영상의 조회수 — 조정이 효과 있었는지 보는 유일한 답"""
    out = sh(os.path.join(HERE, 'ytupload.py'), 'stats')
    vids = re.findall(r'(\d{4}-\d{2}-\d{2})\s+(\d+)\s*회\s*\|\s*(.+)', out)
    return [{'date': d, 'views': int(v), 'title': t.strip()} for d, v, t in vids]

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

def band_err(rows, kind, spec):
    """세 칸 상대오차 합. 작을수록 경쟁 판형에 가깝다"""
    tgt = spec.get(kind) or {}
    mine = [r for r in rows if (r['short'] if kind == 'short' else not r['short'])]
    if not mine or not tgt: return None, {}
    got = {k: statistics.median(r[k] for r in mine) for k in BAND_KEYS if k in tgt}
    if not got: return None, {}
    return sum(abs(got[k] - tgt[k]) / max(tgt[k], 1e-3) for k in got), got

def tune_bands(design, spec, kind, did, blocked):
    """격자를 실제로 그려 재고 가장 나은 값을 고른다. 미는 게 아니라 재는 것이라 흔들리지 않는다"""
    knob = BAND_KNOB[kind]; d = design.setdefault(kind, {})
    cur = d.get(knob)
    if cur is None:
        cur = float(THUMB_DEFAULT.get(kind, {}).get(knob, 0.0))
    grid = sorted(set(BAND_GRID[kind] + [round(float(cur), 4)]))
    best, table = None, []
    for v in grid:
        d[knob] = v
        json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        render_samples(keep_chart=True)
        err, got = band_err(measure_ours(), kind, spec)
        if err is None:
            blocked.append(f'{kind} 세 칸 맞추기 — 샘플이나 경쟁 기준이 없어 못 쟀다'); d[knob] = cur; return
        table.append({'v': v, 'err': round(err, 4), **{k: round(x, 4) for k, x in got.items()}})
        if best is None or err < best['err'] - 1e-9: best = table[-1]
    d[knob] = best['v']
    json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if best['v'] != cur:
        was = next((t for t in table if t['v'] == cur), None)
        did.append(f"{kind}.{knob} {cur} → {best['v']} (세 칸 오차 합 {was['err'] if was else '?'} → {best['err']}, 격자 {len(grid)}점 실측)")
    else:
        did.append(f"{kind}.{knob} {cur} 유지 (격자 {len(grid)}점 중 오차 합 {best['err']} 이 가장 작다)")
    return table


def main():
    global THUMB_DEFAULT
    THUMB_DEFAULT = thumb_defaults()
    t0 = time.time(); log = load(LOG, []); design = load(DESIGN, DEFAULT)
    step = design.get('step', 0) + 1
    did, blocked = [], []

    # 1) 수집 — 경쟁(하루 한 번이면 충분하므로 마지막 수집이 12시간 넘었을 때만)
    last = log[-1]['at'] if log else '2000-01-01 00:00'
    if time.time() - time.mktime(time.strptime(last, '%Y-%m-%d %H:%M')) > 12 * 3600:
        out = sh(os.path.join(HERE, 'ytdesign.py'), '--all', '40', timeout=2400)
        did.append('경쟁 수집: ' + str(len(re.findall(r'구독', out))) + '채널')
    ours_before = our_shorts_stats()

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
      'white':    ({'long': 'text_scale', 'short': 'text_tint'}, {'long': -10.0, 'short': +25.8},
                   {'long': 0.66, 'short': 0.0}, {'long': 1.0, 'short': 1.0}),
      # 아랫줄 노랑 글자 비율(0~1). 2026-09-23 실측 5점(0/.25/.5/.75/1): 롱폼 0.0007→0.0533, 쇼츠 0.0003→0.0199.
      # 기울기가 판형마다 달라(롱폼 0.052 · 쇼츠 0.020) 계수를 판형별로 둔다.
      'yellow':   ('yellow_frac', {'long': -19.0, 'short': -51.0}, 0.0, 1.0),
      'contrast': ('panel_alpha', -260.0, 60, 230),   # 대비가 모자라면 패널을 더 진하게
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
        memo[f'{tag}={cur}'] = g['ours']
        seen = {v: o for k, v, o in ((k, k.split('=')[1], o) for k, o in memo.items() if k.startswith(tag + '='))}
        # 손잡이를 움직였는데 실측이 그대로면 그 항목에 듣지 않는 손잡이다 — 더 돌리지 않는다
        if len(seen) > 1 and max(seen.values()) - min(seen.values()) < 0.002:
            blocked.append(f"{g['kind']}.{g['key']} — {knob} 를 {'/'.join(sorted(seen))} 로 바꿔도 실측 그대로, 듣지 않는 손잡이")
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
        prev = seen.get(str(new))
        if prev is not None and abs(prev - g['target']) >= abs(g['ours'] - g['target']):
            blocked.append(f"{g['kind']}.{g['key']} — {knob}={new} 는 이미 재봤고 더 나빴다({prev} vs 지금 {g['ours']}), 그대로 둠")
            continue
        d[knob] = new
        did.append(f"{g['kind']}.{knob} {cur} → {new} ({g['key']} 우리 {g['ours']} vs 경쟁 {g['target']})")
    if not gaps: did.append('썸네일 수치는 경쟁 상위와 25% 안쪽 — 조정 없음')

    # 5) 지난 조정의 효과 판정
    verdict = ''
    if log and log[-1].get('ours_views') is not None and ours_before:
        prev = log[-1]['ours_views']; now = sum(v['views'] for v in ours_before[:10])
        verdict = f"지난 회차 이후 우리 영상 조회 합계 {prev} → {now}"
        if now < prev * 0.98 and log[-1].get('changed'):
            for c in log[-1]['changed']:
                mm = re.match(r'(\w+)\.(\w+) ([\d.]+) →', c)
                if mm and mm.group(1) in design and mm.group(2) in design[mm.group(1)]:
                    design[mm.group(1)][mm.group(2)] = float(mm.group(3)); did.append(f'되돌림 {mm.group(1)}.{mm.group(2)} → {mm.group(3)} (조회 하락)')

    design['step'] = step
    json.dump(design, open(DESIGN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # 바꾼 값으로 우리 샘플을 다시 만든다 — 안 그러면 다음 회차가 같은 차이를 또 잡는다
    if any('→' in d for d in did): did.append('다음 회차가 바뀐 값으로 다시 그려 잰다')
    rec = {'step': step, 'at': time.strftime('%Y-%m-%d %H:%M'), 'sec': int(time.time() - t0),
           'changed': [d for d in did if '→' in d], 'did': did, 'gaps': gaps[:6], 'blocked': blocked[:8], 'bands': bands,
           'ours_views': sum(v['views'] for v in ours_before[:10]) if ours_before else None, 'verdict': verdict}
    log.append(rec); json.dump(log[-200:], open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"[루프 {step}회차] {rec['sec']}초")
    for d in did: print(' ·', d)
    for b in blocked[:8]: print(' · 막힘:', b)
    if verdict: print(' ·', verdict)
    if gaps: print(' 남은 차이:', ', '.join(f"{g['kind']}.{g['key']} {g['ours']}→{g['target']}" for g in gaps[:5]))

if __name__ == '__main__': main()
