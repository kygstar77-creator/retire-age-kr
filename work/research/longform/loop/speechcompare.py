# 사람 말투 실측 — 경쟁 롱폼 자막(사람이 실제로 말한 것) vs 우리 롱폼 대본(10/4 사장님 "그냥 니 생각 아니야?")
#   py -3.12 work/research/longform/loop/speechcompare.py            → 영상별 지표 표 + 무리 중앙값
#   py -3.12 work/research/longform/loop/speechcompare.py --loo      → 지표 하나·둘 조합의 leave-one-out 정확도 표
#   py -3.12 work/research/longform/loop/speechcompare.py --loo --write
#        → 가장 잘 가르는 조합과 기준을 work/research/editor/script_gate.json에 쓴다(aitell --script가 읽는다)
# 자막은 subs/<영상id>.ko-orig.json3(받기 방법은 speechrate.py 머리말). 자막이 없으면 우리 대본만 잰다.
# 10/3 클라우드 ①: 지표 추가(문장 길이 분포·숫자 개수 분포·숫자 하나 이하 비율·반복 표현·접속사·추임새 종류·질문형).
import json, glob, re, sys, os, statistics as st, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
LF = os.path.dirname(HERE)                                   # work/research/longform
SUBS = os.path.join(HERE, 'subs')
OUR_EPS = ['E-1', 'D-1', 'E-2', 'N-1']
GATE_JSON = os.path.join(os.path.dirname(LF), 'editor', 'script_gate.json')

NUM = re.compile(r'\d[\d,.]*')
# 접속사·추임새 후보(말에서 문장 머리에 오는 것). 종류 수와 1,000단어당 빈도를 잰다 — 목록 자체는 규칙이 아니다.
MARKERS = ['자,', '네,', '근데', '그런데', '사실', '그쵸', '그죠', '이제', '그래서', '그러니까', '그러면', '그럼',
           '그리고', '하지만', '다만', '아니', '뭐', '약간', '진짜', '정말', '일단', '솔직히', '여러분', '보시면', '어쨌든', '그냥']


def subs_text(f):
    d = json.load(open(f, encoding='utf-8'))
    return ' '.join(''.join(s.get('utf8', '') for s in e.get('segs', [])) for e in d.get('events', []) if e.get('segs')).replace('\n', ' ')


def voice_text(path):
    v = json.load(open(path, encoding='utf-8'))
    return ' '.join(l['say'] for s in v['sections'] for l in s['lines'])


def ours_text(ep):
    return voice_text(os.path.join(LF, 'ep', ep, 'voice.json'))


def split_sents(t):
    """기존 측정(10/3 PC)과 같은 자르기 — 숫자를 이어 붙이지 않게 마침표 뒤 공백에서만 자른다."""
    return [x.strip() for x in re.split(r'(?<=[.?!])\s+', t) if len(x.strip()) > 3]


def pct(a, b):
    return round(100 * a / max(1, b), 1)


def metrics(t):
    sents = split_sents(t)
    words = t.split(); W = max(1, len(words)); S = max(1, len(sents))
    ends = [s.rstrip('.?! ') for s in sents]
    lens = [len(s) for s in sents] or [0]
    ncount = [len(NUM.findall(s)) for s in sents]
    k = lambda pat: round(len(re.findall(pat, t)) * 1000 / W, 1)
    # 반복 표현: 세 어절 묶음이 3번 이상 나온 것들이 전체 세 어절 묶음에서 차지하는 비율
    tri = [' '.join(words[i:i + 3]) for i in range(len(words) - 2)]
    cnt = {}
    for x in tri: cnt[x] = cnt.get(x, 0) + 1
    rep = sum(c for c in cnt.values() if c >= 3)
    heads = {}
    for s in sents:
        h = ' '.join(s.split()[:2])
        if len(s.split()) >= 4: heads[h] = heads.get(h, 0) + 1
    mk_hits = {m: len(re.findall(r'(?:^|\s)' + re.escape(m) + (r'' if m.endswith(',') else r'(?=\s|,)'), ' ' + t)) for m in MARKERS}
    return {
        '문장수': len(sents),
        '평균 문장 글자': round(sum(lens) / S, 1),
        '문장 글자 중앙': st.median(lens),
        '문장 글자 p90': sorted(lens)[int(0.9 * (len(lens) - 1))],
        '문장 글자 표준편차': round(st.pstdev(lens), 1),
        '-니다 끝 %': pct(sum(bool(re.search(r'(니다|니까)$', e)) for e in ends), S),
        '-요 끝 %': pct(sum(e.endswith('요') for e in ends), S),
        '숫자/1000단어': k(r'\d[\d,.]*'),
        '숫자 0개 문장 %': pct(sum(n == 0 for n in ncount), S),
        '숫자 1개 문장 %': pct(sum(n == 1 for n in ncount), S),
        '숫자 2개 문장 %': pct(sum(n == 2 for n in ncount), S),
        '숫자 3개+ 문장 %': pct(sum(n >= 3 for n in ncount), S),
        '숫자 하나 이하 문장 %': pct(sum(n <= 1 for n in ncount), S),
        '숫자 2개 이상 문장 %': pct(sum(n >= 2 for n in ncount), S),
        '반복 세어절 %': pct(rep, len(tri)),
        '같은 머리 두어절 최다': max(heads.values()) if heads else 0,
        '접속사·추임새 종류': sum(1 for v in mk_hits.values() if v),
        '접속사·추임새/1000': round(sum(mk_hits.values()) * 1000 / W, 1),
        '추임새(자,·네,·근데·사실·그쵸·이제)/1000': k(r'(?:^|\s)(?:자,|네,|근데|사실|그쵸|그죠|이제)\s'),
        '질문 문장 %': pct(sum(s.endswith('?') for s in sents), S),
    }


# ---- leave-one-out: 지표 하나(문턱 하나) 또는 둘(두 문턱 모두 넘어야 '사람') ----
def fit_one(vals, labels):
    """문턱 하나와 방향. labels True = 사람(경쟁). 학습 정확도가 가장 높은 문턱(동점이면 사람 쪽 최대값에 가장 가까운 것)."""
    best = None
    xs = sorted(set(vals))
    cands = [xs[0] - 1] + [(a + b) / 2 for a, b in zip(xs, xs[1:])] + [xs[-1] + 1]
    for d in ('le', 'ge'):
        for c in cands:
            pred = [(v <= c) if d == 'le' else (v >= c) for v in vals]
            acc = sum(p == l for p, l in zip(pred, labels))
            if best is None or acc > best[0]: best = (acc, c, d)
    return best[1], best[2]


def passes(v, c, d):
    return v <= c if d == 'le' else v >= c


def fit_rule(tr, feats):
    """지표 1~2개 기준. 둘이면 AND: 첫 문턱을 넘은 것들만으로 둘째 문턱을 맞춘다."""
    f1 = feats[0]
    rule = [(f1,) + fit_one([r[1][f1] for r in tr], [r[2] for r in tr])]
    if len(feats) == 2:
        keep = [r for r in tr if passes(r[1][f1], rule[0][1], rule[0][2])] or tr
        rule.append((feats[1],) + fit_one([r[1][feats[1]] for r in keep], [r[2] for r in keep]))
    return rule


def loo(rows, feats):
    """rows=[(이름, 지표 dict, 사람?)]. feats=지표 1~2개. 하나 뺀 나머지로 문턱을 정하고 뺀 것을 맞히는지."""
    ok = 0
    for i in range(len(rows)):
        rule = fit_rule(rows[:i] + rows[i + 1:], feats)
        ok += all(passes(rows[i][1][f], c, d) for f, c, d in rule) == rows[i][2]
    return ok / len(rows)


def edge(rows, f, d):
    hv = [r[1][f] for r in rows if r[2]]
    return max(hv) if d == 'le' else min(hv)


def collect():
    rows = []
    for f in sorted(glob.glob(os.path.join(SUBS, '*.ko-orig.json3'))):
        rows.append(('경쟁 ' + os.path.basename(f)[:11], metrics(subs_text(f)), True))
    for ep in OUR_EPS:
        p = os.path.join(LF, 'ep', ep, 'voice.json')
        if os.path.exists(p): rows.append(('우리 ' + ep, metrics(ours_text(ep)), False))
    return rows


def loo_table(rows, top=15):
    keys = [k for k in rows[0][1] if k != '문장수']
    res = [((k,), loo(rows, (k,))) for k in keys]
    res += [(p, loo(rows, p)) for p in itertools.permutations(keys, 2)]
    # 같은 정확도면 지표 하나짜리를 앞에(과적합 덜함)
    res.sort(key=lambda x: (-x[1], len(x[0])))
    return res[:top]


def main(a):
    rows = collect()
    if not rows: print('잴 것이 없다'); return 1
    if '--loo' in a:
        npos = sum(r[2] for r in rows); nneg = len(rows) - npos
        if not npos or not nneg:
            print(f'경쟁 {npos}편·우리 {nneg}편 — 두 무리가 다 있어야 LOO를 잰다(subs/*.ko-orig.json3 확인)'); return 2
        res = loo_table(rows)
        print(f'| 지표 조합 | LOO 정확도 (경쟁 {npos} + 우리 {nneg}) |'); print('|---|---|')
        for feats, acc in res: print(f'| {" + ".join(feats)} | {acc:.0%} |')
        best = res[0][0]
        rule = fit_rule(rows, best)
        # 문을 헐겁게 두지 않는다: 문턱은 가운데값이 아니라 사람 쪽 끝값(경쟁 최대/최소)으로
        rule = [(f, edge(rows, f, d), d) for f, c, d in rule]
        print('전체로 맞춘 기준:', '; '.join(f'{f} {"≤" if d == "le" else "≥"} {c:g}' for f, c, d in rule))
        if '--write' in a:
            os.makedirs(os.path.dirname(GATE_JSON), exist_ok=True)
            json.dump({'source': 'speechcompare.py --loo', 'n_human': npos, 'n_ours': nneg, 'loo': res[0][1],
                       'rules': [{'metric': f, 'op': d, 'value': round(c, 1)} for f, c, d in rule]},
                      open(GATE_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print('썼다:', GATE_JSON)
        return 0
    keys = list(rows[0][1])
    print('| 영상 | ' + ' | '.join(keys) + ' |'); print('|' + '---|' * (len(keys) + 1))
    for n, r, _ in rows: print(f'| {n} | ' + ' | '.join(str(r[k]) for k in keys) + ' |')
    for grp in ['경쟁', '우리']:
        g = [r for n, r, _ in rows if n.startswith(grp)]
        if g: print(f'| **{grp} 중앙값** | ' + ' | '.join(str(st.median([x[k] for x in g])) for k in keys) + ' |')
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
