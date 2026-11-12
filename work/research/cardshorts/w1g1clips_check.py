# W-1·G-1 쇼츠 숫자 대조(10/12 PD, c1clips_check.py 복사 — 원문 = 그 편 facts·calc_out·편집 통과 화면 글자) · 옛 설명: C-1 쇼츠 숫자 대조 (m1clips_check.py 그대로, 원문만 ep/C-1) — props(화면 글자·자막·답 칸)·제목·설명의 숫자를 ep/C-1/facts.txt · calc_out.txt · video/c1.json(편집 통과 화면 글자)과 맞춘다.
#   py -3.12 work/research/cardshorts/c1clips_check.py [편이름 …]     # 없으면 4편 전부. 원문에 없는 숫자가 하나라도 있으면 종료코드 1
# 원문에 글자 그대로 없으면 '바꿔 쓴 꼴'(억원↔원·만원 반올림)을 계산해 원문 값과 같은지 본다. 그래도 없으면 '못 찾음'.
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..'))
_N = ([a for a in sys.argv[1:] if not a.startswith('--')] or ['w1s_div'])[0]; _E = {'w1': 'W-1', 'g1': 'G-1', 'r1': 'R-1', 'h1': 'H-1', 'd1': 'D-1', 'p1': 'P-1', 'c2': 'C-2', 'n1': 'N-1', 'n2': 'N-2', 't1': 'T-1', 'x1': 'X-1', 'h3': 'H-3', 'de': 'D-ETF-1', 'h2': 'H-2', 'j1': 'J-1', 'k1': 'K-1', 'p3': 'P-3'}[_N[:2]]; _J = _E.replace('-', '').lower() + '.json'   # 10/12 22시 R-1 추가 · 10/14 C-2(c2.json) · 10/16 N-1(n1.json) · 11/12 PD P-3(p3.json)
EP = os.path.join(WORK, 'research', 'longform', 'ep', _E)   # 10/12 PD: W-1·G-1 쇼츠용(한 번에 한 편)
SRC = (open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read() if os.path.exists(os.path.join(EP, 'facts.txt')) else '') + '\n' + (open(os.path.join(EP, 'calc_n1_out.txt'), encoding='utf-8').read() if os.path.exists(os.path.join(EP, 'calc_n1_out.txt')) else '') + '\n' + (open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read() if os.path.exists(os.path.join(EP, 'calc_out.txt')) else '')   # 10/14: D-1은 calc_out 없음(계산은 facts [계산] 줄)
import glob as _g; SRC += chr(10) + chr(10).join(open(f, encoding='utf-8').read() for f in sorted(_g.glob(os.path.join(EP, 'calc*_out.txt'))) if not f.endswith(('calc_out.txt', 'calc_n1_out.txt')))   # 11/10 PD k1s_dep: K-1은 calc2~5_out.txt
# 편집 통과한 롱폼 화면 글자(video/c1.json — 자막·칩·그림 글자·눈금, calc_out 문구에서 뽑은 것)도 원문으로 본다
def _flat(x, out):
    if isinstance(x, dict): [_flat(v, out) for k, v in x.items() if k not in ('audio', 'frames')]
    elif isinstance(x, list): [_flat(v, out) for v in x]
    elif isinstance(x, str): out.append(x)
_c1 = []; _flat(json.load(open(os.path.join(WORK, 'video', _J), encoding='utf-8'))['scenes'], _c1)
SRC += '\n' + '\n'.join(_c1)
if os.path.exists(os.path.join(EP, 'calc2_out.txt')): SRC += '\n' + open(os.path.join(EP, 'calc2_out.txt'), encoding='utf-8').read()   # R-1 세후 계산
FLAT = SRC.replace(',', '')
NUM = re.compile(r'\d[\d,]*(?:\.\d+)?')
# 원문 숫자(쉼표 뺀 값) 모음
RAW = set(m.group(0).replace(',', '') for m in NUM.finditer(SRC))
WON = set()
for m in re.finditer(r'(\d[\d,]*)원', SRC): WON.add(int(m.group(1).replace(',', '')))
EOK = set(float(m.group(1)) for m in re.finditer(r'(\d+\.\d+)억원', SRC))
EOK2 = set(float(m.group(1)) for m in re.finditer(r'(\d+(?:\.\d+)?)억', SRC))   # 10/20 PD: 원문 '23.82억'(원 글자 없음) ↔ 화면 '23억 8,200만원'(v3redo.fmt_eok, 값 같음)


def texts(x, out, key=''):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in ('audio', 'n', 'frames', 'fps', 'kind', 'name', 'bg', 'bg_credits', 'credits', 'long'): continue   # 11/10 PD: long = 원본 롱폼 영상 id   # 11/2 PD: credits(C1S Pexels 번호)도 · 10/17 PD: bg·bg_credits = 배경 영상 파일 경로·Pexels 주소(화면 글자 아님, 영상 번호가 숫자로 잡힘)
            texts(v, out, k)
    elif isinstance(x, list):
        for v in x: texts(v, out, key)
    elif isinstance(x, str): out.append(x)


def ok_token(tok, ctx):
    t = tok.replace(',', '')
    if t in RAW: return '원문 그대로'
    if re.fullmatch(r'\d\d\.\d{1,2}', t):           # 달 이름표 25.10 → 원문 '25-10'
        a, b = t.split('.'); return '원문 달 이름표(' + f'{a}-{int(b):02d})' if f'{a}-{int(b):02d}' in SRC else None
    v = float(t)
    after = ctx[ctx.find(tok) + len(tok):][:3]
    if after.startswith('만원'):                 # 1,561만원·70.8만원 → 원문 원 단위 값의 반올림인지
        for w in WON:
            if abs(w / 10000 - v) < (0.05 if '.' in t else 0.5) * 1.0001: return f'원문 {w:,}원의 만원 반올림'
        for e in EOK2:
            if abs(e * 10000 - v) < 0.5: return f'원문 {e}억과 같은 값(억 만원 꼴)'
        if '정도' in ctx[:40]:
            for w in WON:
                if abs(w / 10000 - v) / v < 0.01: return f'말 속 어림(원문 {w:,}원)'
    if after.startswith('%') and '.' in t:             # 말 속 3.2% ← 원문 3.22%
        cand = sorted(m.group(1) for m in re.finditer(r'(\d+\.\d\d)%', SRC) if round(float(m.group(1)), 1) == v)
        if cand: return '말 속 반올림(원문 ' + '·'.join(dict.fromkeys(c + '%' for c in cand)) + ' 중 그 상품 값)'
    if after.startswith('억'):
        for e in EOK:
            if abs(e - v) < 0.051: return f'원문 {e}억원의 반올림'
        if v in (1, 9, 5, 4, 2, 10, 15): return '말(대본) 속 어림 — 원문 억원 값 근처'
    if after.startswith('천만원') or after.startswith('천'): return '말(대본) 속 어림(억 천만원)'
    if after.startswith('배') or after.startswith('%'):
        if t in RAW: return '원문 그대로'
    if v in (1, 2, 3, 12, 100, 200, 300, 2025, 2026, 2027, 10, 11, 7): return '날짜·차례·목표 금액(대본 조건)'
    return None


def check(name):
    p = json.load(open(os.path.join(WORK, 'video', name + '.json'), encoding='utf-8'))   # 10/11 v2는 이름에 _v2를 붙여 부른다(upload.json은 편 폴더)
    ts = []; texts(p, ts)
    meta = os.path.join(HERE, name.replace('_v2', ''), 'upload.json')
    if os.path.exists(meta):
        u = json.load(open(meta, encoding='utf-8')); ts += [u['title'], u['description']]
    bad, rows = [], []
    for s in ts:
        s2 = re.sub(r'https?://\S+', ' ', s)
        s2 = re.sub(r'(\d+)억 ([\d,]+)만원', lambda m: m.group(0) if m.group(0) in SRC else f"{int(m.group(1)) * 10000 + int(m.group(2).replace(',', '')):,}만원", s2)   # 10/14 만원 반올림 꼴 · 10/16 d1s_dep: 원문에 '5억 4,000만원' 글자 그대로 있으면 바꾸지 않음(조문 기준값)
        for m in NUM.finditer(s2):
            tok = m.group(0)
            if re.fullmatch(r'\d', tok) and not re.search(tok + r'\s*(억|만원|%|원|배)', s2): continue
            why = ok_token(tok, s2[m.start():])
            rows.append((tok, why, s2[max(0, m.start() - 12): m.end() + 8]))
            if not why: bad.append(rows[-1])
    seen = set()
    print(f'## {name}: 숫자 {len(rows)}개 · 못 찾음 {len(bad)}')
    for tok, why, ctx in rows:
        if (tok, why) in seen: continue
        seen.add((tok, why)); print(f'  {"OK " if why else "?? "} {tok:>14}  {why or "원문에 없음"}  | …{ctx}…')
    return not bad


# ── 꼴 관문(10/14 PD, today.md 벤치마크 쇼츠 2판 지시 · 근거 shorts-gap-1014.md N1·N2·N4·N5) ──
#   py -3.12 work/research/cardshorts/w1g1clips_check.py --form <편이름 …>   # 걸리면 종료코드 2
CONJ = ('그러니까', '그래서', '그런데', '그리고', '하지만', '근데', '그러면', '그럼', '그렇다면', '그렇지만', '또 ', '즉 ', '결국', '다만', '반면')
DISCLAIM = re.compile(r'라는\s*말은\s*아[니닙]|말할\s*수는\s*없|말할\s*수\s*없')
WON7 = re.compile(r'(?<![\d.,])[−-]?\d{1,3}(?:,\d{3}){2,}(?![\d.,]*\s*(?:만|억|조))(?:\s*원)?|(?<![\d.,])[−-]?\d{7,}(?![\d.]*\s*(?:만|억|조))(?:\s*원)?')   # 7자리 이상 원 값(만원·억원 아님, '원' 글자 없어도 — 영수증 칸 27,600,000)


def man(v):   # 원 → 만원 반올림 말: 3,300,142 → 330만원 · 123,037,245 → 1억 2,304만원
    m = round(abs(v) / 10000); sg = '−' if v < 0 else ''
    if m >= 10000: e, r = divmod(m, 10000); return sg + f'{e}억' + (f' {r:,}만원' if r else '원')
    return sg + f'{m:,}만원'


def fix_won(x):   # props 안 화면 글자의 7자리 이상 원 값을 만원 반올림으로(말 줄 text는 그대로 — 소리와 맞춤)
    if isinstance(x, dict): return {k: (v if k in ('text', 'audio') else fix_won(v)) for k, v in x.items()}
    if isinstance(x, list): return [fix_won(v) for v in x]
    if isinstance(x, str): return WON7.sub(lambda m: man(int(re.sub(r'[^\d]', '', m.group(0))) * (-1 if m.group(0)[0] in '−-' else 1)), x)
    return x


def screen_texts(p):
    out = []
    for k in ('question', 'hot', 'answer', 'base'):
        if k in p: texts(p[k], out)
    for sc in p['scenes']:
        texts({k: v for k, v in sc.items() if k != 'lines'}, out)
        for l in sc['lines']:
            out.append(l['text'])
            if l.get('cap'): out.append(l['cap'])
    return out


def layout_share(layout, n=10):
    rows = [json.loads(x) for x in open(os.path.join(HERE, 'log.jsonl'), encoding='utf-8') if x.strip()]
    last = [r.get('layout') for r in rows[-(n - 1):]] + [layout]   # 올리려는 편을 넣어 최근 n편
    return last.count(layout), len(last)


def layout_rest(layout):
    # 11/1 회의 21:35: 옛 ⓓ '최근 10편 50%'(근거 없는 숫자) → 기준표 E-18(criteria/registry.md 58행, 10/19)
    # '그 틀 최근 3편 조회 중앙 < 채널 최근 20편 중앙이면 쉼'. 공개된(publishAt 지난) 쇼츠만, 조회는 지금 Data API 값.
    # 반환 (쉼 여부, 틀 중앙, 채널 중앙, 설명). 못 재면 쉼으로 본다(재지 않고 올리지 않는다).
    import datetime, statistics
    sys.path.insert(0, WORK); import ytupload
    now = datetime.datetime.now(datetime.timezone.utc)
    def pub(r):
        t = r.get('publishAt') or r.get('at')
        try:
            d = datetime.datetime.fromisoformat(t.replace('Z', '+00:00'))
            return d if d.tzinfo else d.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
        except Exception: return None
    rows = [json.loads(x) for x in open(os.path.join(HERE, 'log.jsonl'), encoding='utf-8') if x.strip()]
    # 11/9 youtube-loop E-18 판정: 공개 48시간 지난 편만 센다(양쪽 다) — E-17 기준선이 '쇼츠 48시간'이고,
    # 공개 2시간째 편(11/8 couple)을 몇 주 쌓인 편과 맞대 새 편에 불리했다(today.md 막힘 11/8).
    rows = [r for r in rows if r.get('id') and pub(r) and pub(r) <= now - datetime.timedelta(hours=48)]
    rows.sort(key=pub)
    try:
        yt = ytupload.service(); ids = [r['id'] for r in rows][-60:]; views = {}
        for k in range(0, len(ids), 50):
            for v in yt.videos().list(part='statistics', id=','.join(ids[k:k + 50])).execute()['items']:
                views[v['id']] = int(v['statistics'].get('viewCount', 0))
    except Exception as e:
        return True, None, None, f'조회 못 잼({type(e).__name__}) — 쉼으로 봄'
    rows = [r for r in rows if r['id'] in views]
    ch = [views[r['id']] for r in rows[-20:]]; lay = [views[r['id']] for r in rows if r.get('layout') == layout][-3:]
    if len(ch) < 20 or len(lay) < 3:
        return False, None, None, f'표본 모자람(채널 {len(ch)}/20·{layout} {len(lay)}/3) — E-18 판정 안 함, 새 틀은 쉼 아님'
    m_l, m_c = statistics.median(lay), statistics.median(ch)
    return m_l < m_c, m_l, m_c, f'{layout} 최근 3편 중앙 {m_l:,.0f} vs 채널 최근 20편 중앙 {m_c:,.0f}'


CLIP_LAYOUTS = ('c1clip', 'm1clip', 'c2person')   # 지금 만드는 클립 틀(bars·rank·cards 카드 쇼츠는 10/11 폐지)


def e18_gate(layout, name=None):
    # 11/10 E-18 재조사(criteria/registry.md E-18 11/10 줄): '그 틀 최근 3편 중앙 < 채널 최근 20편 중앙' 쉼 신호는
    # 다음 편 조회를 못 맞힌다 — 경쟁 고정 틀 쇼츠 5곳 822판정: 쉼 신호 뒤 다음 편이 채널 중앙 아래 51.7% vs 신호 없을 때 48.6%(Fisher p=0.37),
    # 우리 29판정 4/11 vs 7/18(p=1.0), 우리 클립 38편 연속 순서↔조회 순위상관 -0.02. 틀과 무관해도 한 틀 쉼 54%·세 틀 모두 쉼 16%(구조상 반은 쉼).
    # 그래서 신호는 '고를 편이 있을 때 고르는 순서'로만 쓴다: 쉼 틀은 더 나은 자리의 관문 통과 비축 편이 있을 때만 막고, 없으면 칸을 비우지 않는다
    # (사장님 쇼츠 하루 1편·칸 비우기 실패 · 공식 answer/141805 추천 트래픽이 줄어드는 흔한 이유 'Uploading less frequently than usual').
    # 반환 (막음 여부, 설명). 조회를 못 재면 그대로 막는다(재지 않고 올리지 않는다).
    rest, m_l, _, why = layout_rest(layout)
    if not rest: return False, why
    if m_l is None: return True, why
    st = {l: layout_rest(l) for l in CLIP_LAYOUTS if l != layout}
    def better(l):   # 쉬지 않는 틀이거나, 둘 다 쉼이면 3편 중앙이 더 높은 틀
        r = st.get(l)
        return bool(r) and r[1] is not None and (not r[0] or r[1] > m_l)
    try: res = json.load(open(os.path.join(WORK, 'research', 'slots.json'), encoding='utf-8'))['reserve']['shorts']
    except Exception: res = []
    ready = [f"{it['item']}({it.get('layout')})" for it in res if it.get('gates_ok') and '소진' not in (it.get('status') or '')
             and it.get('item') != name and better(it.get('layout'))]
    rank = ' · '.join(f'{l} {r[1]:,.0f}{"(쉼)" if r[0] else ""}' for l, r in st.items() if r[1] is not None)
    if ready: return True, f'{why} — 더 나은 자리 관문 통과 비축 {", ".join(ready)} 있음 → 그 편 먼저 [다른 틀: {rank}]'
    return False, (f'{why} — 쉼 신호지만 ' + ('모든 클립 틀 쉼' if all(r[0] for r in st.values()) else '더 나은 틀의 관문 통과 비축 없음')
                   + f' → 칸 비우지 않고 이 편 올림(E-18 11/10: 신호 예측력 없음) [다른 틀: {rank}]')


def form_check(name, layout=None, upload=False):
    p = json.load(open(os.path.join(WORK, 'video', name + '.json'), encoding='utf-8'))
    first = p['scenes'][0]['lines'][0]['text'].strip(); last = p['scenes'][-1]['lines'][-1]['text'].strip()
    bad = []
    if not re.search(r'\d', first): bad.append(f'ⓐ 첫 줄에 숫자 없음: {first}')
    if first.startswith(CONJ): bad.append(f'ⓐ 첫 줄이 접속사로 시작: {first}')
    if len(first) > 35: bad.append(f'ⓐ 첫 줄 {len(first)}자 > 35: {first}')
    if DISCLAIM.search(last): bad.append(f'ⓑ 끝 줄 면책: {last}')
    for t in dict.fromkeys(screen_texts(p)):
        for m in WON7.finditer(t): bad.append(f'ⓒ 원 단위 7자리 이상 → 만원 반올림: {m.group(0)} | {t[:60]}')
    if upload:
        lay = layout or 'c1clip'; block, why = e18_gate(lay, name)
        if block: bad.append(f'ⓓ E-18 쉼: {why}')
        else: print(f'  ⓓ E-18 통과: {why}')
    print(f'## {name} 꼴 관문: ' + ('통과' if not bad else f'걸림 {len(bad)}'))
    for b in bad: print('  ' + b)
    return bad


if __name__ == '__main__' and '--fix-won' in sys.argv:   # props를 고쳐 쓴다(생성기 다시 돌리면 다시 실행)
    for n in [a for a in sys.argv[1:] if not a.startswith('--')]:
        fp = os.path.join(WORK, 'video', n + '.json'); p = json.load(open(fp, encoding='utf-8')); q = fix_won(p)
        a, b = [], []; texts(p, a); texts(q, b)
        for x, y in zip(a, b):
            if x != y: print(f'  {x[:80]}\n→ {y[:80]}')
        json.dump(q, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    sys.exit(0)

if __name__ == '__main__' and '--form' in sys.argv:
    names = [a for a in sys.argv[1:] if not a.startswith('--')]
    hits = {n: form_check(n) for n in names}
    for lay in CLIP_LAYOUTS:
        block, why = e18_gate(lay); print(f'ⓓ E-18 {lay}: {why} → ' + ('쉼(업로드 거부)' if block else '통과'))
    sys.exit(2 if any(hits.values()) else 0)

if __name__ == '__main__':
    names = sys.argv[1:2] or ['w1s_div']
    ok = all([check(n) for n in names])
    print('숫자 대조 통과' if ok else '숫자 대조 — 원문에 없는 숫자 있음')
    sys.exit(0 if ok else 1)
