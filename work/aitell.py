# AI 티 자동 검사 — 글이 기계로 찍은 것처럼 읽히는 신호를 점수로 낸다(2026-10-01).
#   py -3.12 work/aitell.py <묶음 폴더|텍스트 파일>          → 점수와 걸린 곳
#   py -3.12 work/aitell.py text "<문장>"                    → 짧은 글(제목·설명·댓글)
#   py -3.12 work/aitell.py gate <묶음>                      → 기준 넘고 편집 통과 표시 없으면 종료코드 4
#   py -3.12 work/aitell.py pass <묶음> <편집자>             → 편집 통과 표시(editor_ok.txt)를 남긴다
#   py -3.12 work/aitell.py scan <묶음 폴더 여러 개>         → 기준 조정용 분포
# 사장님 10/1 "사소한 것까지 모든 글을 다 검토해서 사람이 쓴 글로 바꿔야 하는데" — 순돌이 지시 [지시·긴급].
# 재는 것: ① 사전(work/aitell_dict.json — 한·영 AI 티 말, 과한 설명조, 맺음 틀) ② 같은 끝맺음 연속
#          ③ 같은 틀 반복(문장 머리 두 어절·문장 꼬리 두 어절이 세 번 넘게) ④ 문단 맺음 틀 반복.
# 발행기(naverpost.py·cafeapi.py·ytupload.py·f2_coupang.py)가 올리기 전에 gate를 부른다.
# 편집 통과 표시는 표시 뒤에 원고가 바뀌면 무효다 — 고친 뒤 편집자가 다시 봐야 한다.
import sys, os, re, json, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__))
DICT = json.load(open(os.path.join(HERE, 'aitell_dict.json'), encoding='utf-8'))
KO_TELLS, KO_EXPLAIN, KO_CLOSING, EN_TELLS = DICT['ko'], DICT['ko_explain'], DICT['ko_closing'], DICT['en']
LIMIT = 12.0          # 1,000자당 점수. 10/1 scan: 최근 묶음 59개 중앙 0·상위 25% 5.2 → 12를 넘는 건 5개('~요' 70%대·7문장 넘게 연속)
LIMIT_SHORT = 6.0     # 300자 미만(제목·설명·댓글)은 원점수로 본다.
OK_FILE = 'editor_ok.txt'


def sentences(text):
    text = re.sub(r'^\s*[|#>*-]+\s*', '', text, flags=re.M)
    parts = re.split(r'(?<=[.?!])\s+|\n+', text)
    return [p.strip() for p in parts if len(re.sub(r'[^가-힣A-Za-z]', '', p)) >= 4]


def end_kind(s):
    """문장 끝 두 음절(예: 어요·예요·있다·였다). 평어체 글은 거의 다 '다'로 끝나서 한 글자로는 틀 반복을 못 본다."""
    tail = re.sub(r'[^가-힣]', '', s)[-2:]
    return tail if len(tail) == 2 and re.search(r'(요|다|죠|까)$', tail) else '기타'



def score(text):
    """점수와 걸린 곳 목록. 점수는 1,000자당(짧은 글은 원점수)."""
    sents = sentences(text)
    hits, pts = [], 0.0
    low = text.lower()
    for w in KO_TELLS:
        c = text.count(w)
        if c: pts += 3 * c; hits.append(f'AI 말 "{w}" ×{c}')
    for w in EN_TELLS:
        c = len(re.findall(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', low))
        if c: pts += 3 * c; hits.append(f'AI 말(영) "{w}" ×{c}')
    for w in KO_EXPLAIN:
        c = text.count(w)
        if c: pts += 2 * c; hits.append(f'설명조 "{w}" ×{c}')
    # 문단 맺음 틀: 문단 마지막 문장이 같은 맺음 말로 끝나는 게 두 번 넘으면
    paras = [p for p in re.split(r'\n\s*\n', text) if p.strip()]
    closes = collections.Counter()
    for p in paras:
        ss = sentences(p)
        if not ss: continue
        for w in KO_CLOSING:
            if w in ss[-1]: closes[w] += 1; break
    for w, c in closes.items():
        if c >= 2: pts += 3 * (c - 1); hits.append(f'문단 맺음 틀 "{w}" ×{c}')
    # 같은 끝맺음 연속
    run, best, prev, at = 1, 1, None, ''
    for s in sents:
        e = end_kind(s)
        run = run + 1 if e == prev and e != '기타' else 1
        if run > best: best, at = run, s
        prev = e
    if best >= 3: pts += 3 * (best - 2); hits.append(f'같은 끝 두 음절 {best}연속 — "…{at[-30:]}"')
    # 해요체 쏠림: '~요'만 다섯 문장 넘게 잇따르거나, 문장 열에 여섯 넘게 '~요'(카페 실측 9/27 '요' 16%, 우리 글 75%)
    # 평어체 '~다'는 블로그 기본 말투라 쏠림으로 치지 않는다(editor style-guide 블로그 기준).
    yo = [s for s in sents if re.search(r'요[.?!]?$', s)]
    run, yrun = 0, 0
    for s in sents:
        run = run + 1 if re.search(r'요[.?!]?$', s) else 0; yrun = max(yrun, run)
    if yrun >= 5: pts += 2 * (yrun - 4); hits.append(f"'~요' {yrun}문장 연속")
    if len(sents) >= 10 and len(yo) / len(sents) > 0.6:
        pts += 10 * (len(yo) / len(sents) - 0.6) * 10 / 2; hits.append(f"'~요' 비율 {round(len(yo) / len(sents) * 100)}% (카페 실측 16%)")
    # 같은 틀 반복: 문장 머리 두 어절 / 꼬리 두 어절
    heads = collections.Counter(' '.join(s.split()[:2]) for s in sents if len(s.split()) >= 4)
    tails = collections.Counter(' '.join(s.split()[-2:]) for s in sents if len(s.split()) >= 4)
    for label, cnt in (('머리', heads), ('꼬리', tails)):
        for k, c in cnt.items():
            if c >= 3 and re.search(r'[가-힣A-Za-z]', k):
                pts += 2 * (c - 2); hits.append(f'같은 문장 {label} "{k}" ×{c}')
    n = len(re.sub(r'[\s\W_]', '', text))
    val = pts if n < 300 else pts / (n / 1000)
    return round(val, 1), hits, n


def pkg_text(pkg):
    """묶음의 본문(order.txt 순서의 텍스트 조각) + 제목."""
    parts = []
    tp = os.path.join(pkg, 'title.txt')
    if os.path.exists(tp): parts.append(open(tp, encoding='utf-8').read().strip())
    op = os.path.join(pkg, 'order.txt')
    files = []
    if os.path.exists(op):
        for ln in open(op, encoding='utf-8').read().splitlines():
            tok = (ln.strip().split() or [''])[0]
            if tok.endswith('.txt') and os.path.exists(os.path.join(pkg, tok)): files.append(os.path.join(pkg, tok))
    if not files:
        files = sorted(glob.glob(os.path.join(pkg, 'c[0-9]*.txt')) + glob.glob(os.path.join(pkg, 'b[0-9]*.txt')))
    for f in files: parts.append(open(f, encoding='utf-8').read())
    return '\n\n'.join(parts), files


def editor_ok(pkg, files=None):
    """편집 통과 표시가 있고, 표시 뒤에 원고가 안 바뀌었으면 (True, 누가)."""
    p = os.path.join(pkg, OK_FILE)
    if not os.path.exists(p): return False, ''
    files = files if files is not None else pkg_text(pkg)[1]
    t = os.path.getmtime(p)
    newer = [os.path.basename(f) for f in files if os.path.getmtime(f) > t + 1]
    if newer: return False, '편집 통과 뒤 바뀐 조각: ' + ', '.join(newer)
    return True, open(p, encoding='utf-8').read().strip()[:80]


def gate_pkg(pkg):
    """발행기용. (올려도 되나, 한 줄 사유, 걸린 곳)."""
    text, files = pkg_text(pkg)
    val, hits, n = score(text)
    lim = LIMIT if n >= 300 else LIMIT_SHORT
    if val <= lim: return True, f'AI 티 {val}(기준 {lim})', hits
    ok, who = editor_ok(pkg, files)
    if ok: return True, f'AI 티 {val}(기준 {lim}) — 편집 통과 {who}', hits
    return False, f'AI 티 {val}이 기준 {lim}을 넘는다' + (f' ({who})' if who else ''), hits


def gate_text(text, ok_flag=False):
    """유튜브 제목·설명, 쿠팡 문구 같은 짧은 글용."""
    val, hits, n = score(text)
    lim = LIMIT if n >= 300 else LIMIT_SHORT
    if val <= lim or ok_flag: return True, f'AI 티 {val}(기준 {lim})' + (' — 편집 통과' if val > lim else ''), hits
    return False, f'AI 티 {val}이 기준 {lim}을 넘는다', hits


def refuse(msg, hits):
    print('올리지 않는다:', msg)
    for h in hits[:10]: print('   ', h)
    print('  고친 뒤 다시 올리거나, 편집자가 보고 py -3.12 work/aitell.py pass <묶음> <편집자> 를 남긴다.')


def main(a):
    if not a: print(__doc__ or open(__file__, encoding='utf-8').read().split('import')[0]); return 0
    if a[0] == 'text':
        val, hits, n = score(' '.join(a[1:])); print(f'AI 티 {val} ({n}자)'); [print('  ', h) for h in hits]; return 0
    if a[0] == 'gate':
        ok, msg, hits = gate_pkg(a[1])
        if ok: print(msg); return 0
        refuse(msg, hits); return 4
    if a[0] == 'pass':
        who = a[2] if len(a) > 2 else 'editor'
        import datetime
        val, _, _ = score(pkg_text(a[1])[0])
        open(os.path.join(a[1], OK_FILE), 'w', encoding='utf-8').write(
            f'{who} {datetime.datetime.now():%Y-%m-%d %H:%M} · 그때 점수 {val}\n')
        print('편집 통과 표시', a[1]); return 0
    if a[0] == 'scan':
        rows = []
        for p in a[1:]:
            if os.path.isdir(p) and os.path.exists(os.path.join(p, 'order.txt')):
                val, hits, n = score(pkg_text(p)[0]); rows.append((val, n, p, hits))
        rows.sort(reverse=True)
        for val, n, p, hits in rows: print(f'{val:6} {n:5}자 {os.path.basename(os.path.dirname(p))}  {"; ".join(hits[:3])[:110]}')
        if rows:
            vs = sorted(r[0] for r in rows)
            print(f'묶음 {len(vs)} · 중앙 {vs[len(vs)//2]} · 상위 25% {vs[int(len(vs)*0.75)]} · 기준 {LIMIT} 넘는 것 {sum(v > LIMIT for v in vs)}')
        return 0
    p = a[0]
    if os.path.isdir(p):
        text, files = pkg_text(p)
    else:
        text = open(p, encoding='utf-8').read()
    val, hits, n = score(text)
    lim = LIMIT if n >= 300 else LIMIT_SHORT
    print(f'AI 티 {val} (기준 {lim}, {n}자) — {"넘음" if val > lim else "통과"}')
    for h in hits: print('  ', h)
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
