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

def render_samples():
    """지금 설정으로 샘플 썸네일 2장을 새로 그린다 — 이게 있어야 조정 효과가 다음 측정에 나타난다"""
    sh(os.path.join(HERE, 'thumb.py'), '금천 61% 강남 36%', '서울 전세가율 전수 조사', os.path.join(SAMPLE, 'short.png'), '--short')
    bg = os.path.join(R, '_shots', 'heatmap_2026-09-23.png')
    sh(os.path.join(HERE, 'thumb.py'), '전세가율 61% vs 36%', '서울 25개 구 전부 계산', os.path.join(SAMPLE, 'long.png'), *( [bg] if os.path.exists(bg) else [] ))

def measure_ours():
    """우리 썸네일을 경쟁과 같은 자로 잰다"""
    sys.path.insert(0, HERE)
    import thumbstat
    rows = []
    for p, isshort in ((os.path.join(SAMPLE, 'short.png'), True), (os.path.join(SAMPLE, 'long.png'), False)):
        st = thumbstat.measure(p)
        if st: rows.append({**st, 'file': os.path.basename(p), 'short': isshort})
    return rows

def main():
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
    render_samples()          # 지금 design.json 값으로 샘플을 새로 그린다
    ours = measure_ours()     # 그 샘플만 잰다

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
      'text_top': ('text_y', +0.45, 0.15, 0.80),      # 위쪽 글자가 많으면 text_y를 키워 아래로 민다
      'text_bot': ('text_y', -0.45, 0.15, 0.80),      # 아래쪽이 모자라면 text_y를 키운다(부호 반대로 들어옴)
      'bright':   ('bg_bright', -1.2, 0.12, 0.90),
      'dark':     ('bg_bright', +0.8, 0.12, 0.90),
      # 흰 면적은 흰 글자 픽셀에서 나온다. 외곽선은 검정이라 아무리 얇게 해도 흰 면적이 안 줄어 stroke_ratio가 한계 40에 붙어
      # 버렸다(2026-09-23 step20). 그래서 글자 크기 배율로 바꿨다. 면적은 크기의 제곱이라 계수를 작게 잡아 한 칸씩 간다.
      'white':    ('text_scale', -10.0, 0.66, 1.0),
      # 아랫줄 노랑 글자 비율(0~1). 2026-09-23 실측 5점(0/.25/.5/.75/1): 롱폼 0.0007→0.0533, 쇼츠 0.0003→0.0199.
      # 기울기가 판형마다 달라(롱폼 0.052 · 쇼츠 0.020) 계수를 판형별로 둔다.
      'yellow':   ('yellow_frac', {'long': -19.0, 'short': -51.0}, 0.0, 1.0),
      'contrast': ('panel_alpha', -260.0, 60, 230),   # 대비가 모자라면 패널을 더 진하게
      'text_mid': ('text_y', 'center', 0.15, 0.80),   # 가운데 띠에 글자가 없으면 text_y를 0.5 쪽으로 당긴다
    }
    # 손잡이 없는 차이가 위쪽 세 자리를 잡아먹지 않게 먼저 갈라 둔다
    knobbed = [g for g in gaps if g['key'] in RULE]
    for g in gaps:
        if g['key'] not in RULE:
            blocked.append(f"{g['kind']}.{g['key']} 우리 {g['ours']} vs 경쟁 {g['target']} — 그리기 손잡이 없음")
    memo = design.setdefault('_memo', {})   # "종류.항목.손잡이=값" → 그 값일 때 실측치. 같은 자리를 또 밟지 않으려고 적어 둔다
    moved_knobs = set()   # 같은 손잡이를 한 바퀴에 두 번 움직이면 뒤 항목이 앞 항목을 덮어써 값이 계속 뒤집힌다(2026-09-23)
    for g in knobbed[:3]:
        knob, coef, lo, hi = RULE[g['key']]
        if (g['kind'], knob) in moved_knobs:
            blocked.append(f"{g['kind']}.{g['key']} — 같은 손잡이 {knob} 를 이번 바퀴에 다른 항목이 이미 움직였다, 다음 바퀴에 잰다")
            continue
        if isinstance(coef, dict): coef = coef.get(g['kind'])   # 판형마다 손잡이 기울기가 다른 항목
        if coef is None: continue
        d = design.setdefault(g['kind'], {})
        cur = d.get(knob)
        if cur is None: continue
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
           'changed': [d for d in did if '→' in d], 'did': did, 'gaps': gaps[:6], 'blocked': blocked[:8],
           'ours_views': sum(v['views'] for v in ours_before[:10]) if ours_before else None, 'verdict': verdict}
    log.append(rec); json.dump(log[-200:], open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"[루프 {step}회차] {rec['sec']}초")
    for d in did: print(' ·', d)
    for b in blocked[:8]: print(' · 막힘:', b)
    if verdict: print(' ·', verdict)
    if gaps: print(' 남은 차이:', ', '.join(f"{g['kind']}.{g['key']} {g['ours']}→{g['target']}" for g in gaps[:5]))

if __name__ == '__main__': main()
