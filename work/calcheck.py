# 계산 검산 — 대기열 0-b(2026-09-24 19시 D 회차가 올림).
#   selfcheck.py 는 "본문 숫자가 사실표 숫자에 들어 있나"만 보고 계산은 분류만 했다.
#   그래서 (가) 사실표가 틀리면 같이 통과하고 (나) 사실표 숫자로 만든 파생값이 틀려도 통과했다.
#   실제로 acediv0924 의 4억 5,340만원(맞는 값 4억 5,336만원)과 jnj0925 의 날짜 오류가
#   '지적 0건'으로 통과했다. 여기서는 값을 **다시 계산해서** 어긋나면 잡는다.
#
# 원칙 — 헛짚으면 아무도 안 본다.
#   · 관계가 문장에 말로 적혀 있을 때만 검산한다("~에서 ~로 N% 늘었다", "N%를 떼면", "다 더하면").
#   · 어긋남이 1%를 넘고 30% 안일 때만 잡는다. 30%를 넘으면 그 문장이 말하는 관계가 아니라고 보고 넘긴다
#     (본문에 안 적힌 다른 값에서 나온 숫자를 억지로 엮지 않기 위해서다).
#   · 표시 자릿수 반올림은 어긋남으로 세지 않는다(38.3 × 12 = 459.6 을 460 으로 적어도 통과).
#
#   py -3.12 work/calcheck.py <pkg>   # 단독 실행도 된다(검산만 본다)
import sys, os, re, glob
sys.stdout.reconfigure(encoding='utf-8')

NUM = r'\d[\d,]*(?:\.\d+)?'


def _f(x):
    return float(str(x).replace(',', ''))


# 긴 표기부터 본다. '4억 5,336만원'을 '4'와 '5,336'으로 쪼개면 검산이 통째로 무너진다.
_PATS = [
    (re.compile(r'(' + NUM + r')\s*조\s*(' + NUM + r')\s*억\s*원?'),
     lambda m: (_f(m.group(1)) * 1e12 + _f(m.group(2)) * 1e8, 'money')),
    (re.compile(r'(' + NUM + r')\s*억\s*(' + NUM + r')\s*만\s*원?'),
     lambda m: (_f(m.group(1)) * 1e8 + _f(m.group(2)) * 1e4, 'money')),
    # '49만 2,187원' 처럼 만 단위와 원 단위를 띄어 적는 표기도 한 값으로 읽는다
    (re.compile(r'(' + NUM + r')\s*만\s*(' + NUM + r')\s*원'),
     lambda m: (_f(m.group(1)) * 1e4 + _f(m.group(2)), 'money')),
    (re.compile(r'(' + NUM + r')\s*(조|억|만)\s*원'),
     lambda m: (_f(m.group(1)) * {'조': 1e12, '억': 1e8, '만': 1e4}[m.group(2)], 'money')),
    # 부동산 글은 '평당 0.44억' 처럼 원을 안 붙이고 적는다. 만은 '2만 가구'처럼 돈이 아닌 데도
    # 쓰이므로 조·억만 돈으로 본다.
    (re.compile(r'(' + NUM + r')\s*(조|억)(?!\s*원)(?!\s*' + NUM + r')'),
     lambda m: (_f(m.group(1)) * {'조': 1e12, '억': 1e8}[m.group(2)], 'money')),
    (re.compile(r'(' + NUM + r')\s*(?:%\s*p|%p|퍼센트\s*포인트|%\s*포인트)'),
     lambda m: (_f(m.group(1)), 'pctp')),
    (re.compile(r'(' + NUM + r')\s*%'), lambda m: (_f(m.group(1)), 'pct')),
    (re.compile(r'(' + NUM + r')\s*달러'), lambda m: (_f(m.group(1)), 'usd')),
    (re.compile(r'(' + NUM + r')\s*원'), lambda m: (_f(m.group(1)), 'money')),
    (re.compile(r'(' + NUM + r')\s*배'), lambda m: (_f(m.group(1)), 'x')),
    (re.compile(r'(' + NUM + r')\s*(?:주|명|건|편|번|곳|채|가구|세대|개(?!월))'),
     lambda m: (_f(m.group(1)), 'cnt')),
    (re.compile(r'(' + NUM + r')'), lambda m: (_f(m.group(1)), 'bare')),
]


def tokens(s):
    """문장에서 (값·종류·자리·쓴 그대로)를 뽑는다. 앞 패턴이 먹은 자리는 뒤 패턴이 다시 안 먹는다."""
    taken, out = [], []
    for pat, get in _PATS:
        for m in pat.finditer(s):
            if any(m.start() < e and b < m.end() for b, e in taken):
                continue
            taken.append((m.start(), m.end()))
            v, kind = get(m)
            raw = m.group(0).strip()
            # 반올림 여유는 단위를 따라가야 한다. '1.11억'의 ±0.005 는 0.005원이 아니라 50만원이다.
            lit = _f(m.group(1))
            scale = (v / lit) if lit else 1.0
            out.append({'v': v, 'k': kind, 'i': m.start(), 'raw': raw,
                        'd': _digits(raw) * abs(scale)})
    return sorted(out, key=lambda d: d['i'])


def _digits(raw):
    """적힌 자릿수로 반올림 여유를 정한다. '38.3'은 ±0.05, '460'은 ±0.5."""
    m = re.search(r'\.(\d+)', raw)
    return 0.5 * (10 ** -len(m.group(1))) if m else 0.5


def near(got, want, raw='', rel=0.01):
    """반올림 여유와 1% 안이면 맞다고 본다."""
    if want == 0:
        return abs(got) < 1e-9
    return abs(got - want) <= max(abs(want) * rel, _digits(raw))


def off(got, want):
    return abs(got - want) / abs(want) if want else 9e9


FAR = 0.30   # 이보다 크게 어긋나면 그 문장이 말하는 관계가 아니라고 본다


def _say(v, k):
    if k == 'money':
        if v >= 1e8:
            return '%s억원' % ('%,.4g' % (v / 1e8)).replace('%', '')
        if v >= 1e4:
            return '%.4g만원' % (v / 1e4)
        return '%.0f원' % v
    tail = {'pct': '%', 'pctp': '%p', 'usd': '달러', 'x': '배'}.get(k, '')
    return '%.4g%s' % (v, tail)


def check_sents(ss):
    """문장 목록을 받아 [(문장번호, 지적)] 을 돌려준다."""
    bad = []

    def hit(i, msg):
        bad.append((i, msg))

    for i, s in enumerate(ss, 1):
        ts = tokens(s)
        # 기준값은 앞 문장에 적어 놓고 결과만 다음 문장에 쓰는 일이 흔하다
        # ("100주면 536달러다." → "15%를 떼면 455.60달러가 남는다.").
        # 앞 한 문장까지만 뒤돌아본다. 더 멀리 보면 엉뚱한 값을 기준으로 삼는다.
        prev = ss[i - 2] if i >= 2 else ''
        pts = tokens(prev)
        ctx = (prev + ' ' + s)
        if len(ts) < 2 and len(ts) + len(pts) < 2:
            continue

        # 1) 증감률 — "A에서 B로 … N% 늘었다/줄었다/올랐다"
        m = re.search(r'(' + NUM + r')\s*(?:조원|억원|만원|원|달러|%|배|주|명|건)?\s*(?:에서|→)\s*'
                      r'(' + NUM + r')\s*(?:조원|억원|만원|원|달러|%|배|주|명|건)?\s*(?:으로|로)', s)
        # 한 문장에 비율이 둘 이상 나오는 일이 흔하다
        # ("연봉은 100% 늘었는데 실수령액은 221만원에서 414만원으로 87% 느는 데 그친다").
        # 'A에서 B로' **뒤에** 오는 비율만 그 둘의 증감률로 본다. 앞의 비율은 다른 것을 말한다.
        r = None
        if m:
            for mm in re.finditer(r'(' + NUM + r')\s*%\s*(?:나|씩|가|를|쯤|가량|,)?\s*'
                                  r'(?:늘|줄|올|내|증가|감소|상승|하락|뛰|빠|많|적)', s):
                if mm.start() > m.end():
                    r = mm
                    break
        if m and r and not re.search(r'포인트|%p', s):
            a, b, got = _f(m.group(1)), _f(m.group(2)), _f(r.group(1))
            if a and b and a != b:
                want = abs(b - a) / a * 100
                if not near(got, want, r.group(1)) and off(got, want) < FAR:
                    hit(i, '증감률이 안 맞는다 — %s→%s 이면 %.2f%% 인데 본문은 %s%% · %s'
                        % (m.group(1), m.group(2), want, r.group(1), s[:70]))

        # 2) %포인트 — "A%에서 B%로 … N%포인트"
        m = re.search(r'(' + NUM + r')\s*%\s*(?:에서|→)\s*(' + NUM + r')\s*%', s)
        p = [t for t in ts if t['k'] == 'pctp']
        if m and p:
            want = abs(_f(m.group(2)) - _f(m.group(1)))
            got = p[0]['v']
            if not near(got, want, p[0]['raw']) and off(got, want) < FAR:
                hit(i, '%%포인트가 안 맞는다 — %s%%와 %s%% 사이는 %.2f%%p 인데 본문은 %s%%p · %s'
                    % (m.group(1), m.group(2), want, got, s[:70]))

        # 2-b) 해 대 해 비교 — "2022년과 2025년을 비교하면 N% 늘었다"
        m = re.search(r'(\d{4})\s*년\s*(?:과|와|에서)\s*(\d{4})\s*년\s*(?:을|를|과|와)?\s*(?:비교|견주|대면)', s)
        r2 = re.search(r'(' + NUM + r')\s*%\s*(?:나|씩|가|를|쯤|가량|,)?\s*(?:늘|줄|올|내|증가|감소|상승|하락)', s)
        if m and r2:
            ymap = {}
            for mm in re.finditer(r'(\d{4})\s*년\s*(?:에는|은|는|,)?\s*(' + NUM + r')\s*(달러|원|만원|억원)', ctx):
                ymap.setdefault(mm.group(1), _f(mm.group(2)))
            a, b = ymap.get(m.group(1)), ymap.get(m.group(2))
            if a and b and a != b:
                want = abs(b - a) / a * 100
                got = _f(r2.group(1))
                if not near(got, want, r2.group(1)) and off(got, want) < FAR:
                    hit(i, '해 대 해 증감률이 안 맞는다 — %s년 %g → %s년 %g 면 %.2f%% 인데 본문은 %s%% · %s'
                        % (m.group(1), a, m.group(2), b, want, r2.group(1), s[:70]))

        # 3) 배수 — "가장 많은 A, 가장 적은 B … N배" (짝은 앞 문장에 적혀 있기도 하다)
        xs = [t for t in ts if t['k'] == 'x']
        others = [t for t in (ts + pts) if t['k'] in ('money', 'usd', 'cnt', 'pct') and t['v'] > 0]
        # "1.5배 넘게", "두 배 가까이" 처럼 어림잡은 말은 검산 대상이 아니다.
        about = bool(re.search(r'배\s*(?:쯤|가까|넘|남짓|안팎|정도)|약\s*' + NUM + r'\s*배|' + NUM + r'\s*배\s*이상', s))
        if xs and not about and len(others) >= 2 and re.search(r'차이|많|적|크|작|높|낮|넘', ctx):
            got = xs[0]['v']
            # 본문에 적힌 값 자체가 반올림한 값이다('1.11억'은 1.105~1.115억).
            # 그 폭을 감안한 비율 구간 안에 들면 맞는 것이다 — 감안하지 않으면
            # 평당가 표처럼 소수 둘째 자리로 줄여 적은 글이 통째로 걸린다(2026-09-25 pyeong0924).
            pairs, bands = [], []
            for a in others:
                for b in others:
                    if a['k'] != b['k'] or min(a['v'], b['v']) <= 0:
                        continue
                    hi_t, lo_t = (a, b) if a['v'] >= b['v'] else (b, a)
                    w = hi_t['v'] / lo_t['v']
                    if w <= 1.0001:
                        continue
                    dh, dl = hi_t['d'], lo_t['d']
                    pairs.append(w)
                    bands.append(((hi_t['v'] - dh) / (lo_t['v'] + dl),
                                  (hi_t['v'] + dh) / max(lo_t['v'] - dl, 1e-9)))
            inside = any(lo <= got <= hi for lo, hi in bands)
            if pairs and not inside and not any(near(got, w, xs[0]['raw']) for w in pairs):
                best = min(pairs, key=lambda w: off(got, w))
                if off(got, best) < FAR:
                    hit(i, '배수가 안 맞는다 — 본문 숫자로는 %.2f배 인데 %s배라고 적었다 · %s'
                        % (best, got, s[:70]))

        # 4) 비율 떼기 — "N%를 떼면 C" (기준값과 결과값이 같은 문장에 다 있을 때만)
        m = re.search(r'(' + NUM + r')\s*%\s*(?:를|을)?\s*(?:떼|빼|공제|원천징수)', s)
        if m:
            rate = _f(m.group(1)) / 100
            before = [t for t in ts if t['i'] < m.start() and t['k'] in ('money', 'usd')]
            after = [t for t in ts if t['i'] > m.end() and t['k'] in ('money', 'usd')]
            if after and not before:      # 기준값은 앞 문장에 있기도 하다
                before = [t for t in pts if t['k'] == after[0]['k']]
            if before and after:
                base, got = before[-1], after[0]
                if base['k'] == got['k'] and base['v'] > 0:
                    want = base['v'] * (1 - rate)
                    if not near(got['v'], want, got['raw']) and off(got['v'], want) < FAR:
                        hit(i, '공제 계산이 안 맞는다 — %s에서 %s%% 떼면 %s 인데 본문은 %s · %s'
                            % (base['raw'], m.group(1), _say(want, got['k']), got['raw'], s[:70]))

        # 5) 나누기 — "A를 B로 나누면 C" / "열두 달로 나누면 월 C"
        m = re.search(r'(?:으로|로)\s*나누(?:면|고|니|어)', s)
        if m:
            left = [t for t in ts if t['i'] < m.start()]
            right = [t for t in ts if t['i'] > m.end()]
            words = {'열두': 12, '스물넷': 24, '스무': 20, '열': 10, '넷': 4, '셋': 3, '둘': 2}
            div = left[-1]['v'] if len(left) >= 2 else None
            for w, v in words.items():
                if w in s[max(0, m.start() - 8):m.start()]:
                    div = v
                    break
            if right and div and not left and pts:     # 나눌 값이 앞 문장에 있는 경우
                same = [t for t in pts if t['k'] == right[0]['k']]
                if same:
                    left = [same[-1]]
            if right and div and left:
                base = left[0]['v'] if len(left) >= 2 else left[-1]['v']
                got = right[0]
                if base and got['k'] in ('money', 'usd', 'pct'):
                    want = base / div * (100 if got['k'] == 'pct' else 1)
                    if not near(got['v'], want, got['raw']) and off(got['v'], want) < FAR:
                        hit(i, '나눗셈이 안 맞는다 — %.6g ÷ %g = %.6g 인데 본문은 %s · %s'
                            % (base, div, want, got['raw'], s[:70]))

    # 6) 합계·평균 — 바로 앞 표의 한 열을 실제로 더한다
    for i, s in enumerate(ss, 1):
        is_sum = bool(re.search(r'더하면|합치면|합계', s))
        is_avg = bool(re.search(r'평균(?:이|은|을|적으로)', s))
        if not (is_sum or is_avg):
            continue
        res = [t for t in tokens(s) if t['k'] in ('money', 'usd')]
        if not res:
            continue
        got = res[-1]
        pool = table_col(ss, i, got['k'])
        if len(pool) < 3:
            continue
        # 문장이 몇 건이라고 말했으면 그 수와 표의 줄 수가 같을 때만 검산한다.
        # (표를 덜 읽고 "합계가 틀렸다"고 하면 그게 헛짚기다 — 2026-09-25 acediv0924 에서 먼저 겪었다)
        said = stated_count(s)
        if said and said != len(pool):
            continue
        total = sum(pool)
        avg = total / len(pool)
        if near(got['v'], total, got['raw']) or near(got['v'], avg, got['raw']):
            continue
        cand, what = (total, '합계가') if is_sum else (avg, '평균이')
        if off(got['v'], cand) < FAR:
            hit(i, '%s 안 맞는다 — 위 표 %d줄을 실제로 세면 %s 인데 본문은 %s · %s'
                % (what, len(pool), _say(cand, got['k']), got['raw'], s[:70]))
    return sorted(bad)


_NUMWORD = {'두': 2, '세': 3, '네': 4, '다섯': 5, '여섯': 6, '일곱': 7, '여덟': 8, '아홉': 9,
            '열': 10, '열두': 12, '스무': 20, '스물넷': 24}


def stated_count(s):
    """"열 건을 다 더하면", "여섯 번 평균" 처럼 문장이 말한 개수."""
    m = re.search(r'(' + NUM + r')\s*(?:건|번|개|달|줄|곳)\s*(?:을|의|,)?\s*(?:다\s*)?(?:더하|합치|평균)', s)
    if m:
        return int(_f(m.group(1)))
    for w, v in sorted(_NUMWORD.items(), key=lambda kv: -len(kv[0])):
        if re.search(w + r'\s*(?:건|번|개|달|줄|곳)', s):
            return v
    return None


def table_col(ss, i, kind):
    """문장 i 바로 앞에 붙은 표 덩어리에서 kind 종류의 열 하나를 통째로 읽는다.
    고정 창(앞 14줄)으로 자르면 열 줄짜리 표가 여덟 줄로 잘려 합계가 어긋난 것처럼 보인다."""
    j, skipped = i - 2, 0
    while j >= 0 and not ss[j].startswith('|') and skipped < 6:
        j -= 1
        skipped += 1
    if j < 0 or not ss[j].startswith('|'):
        return []
    end = j
    while j >= 0 and ss[j].startswith('|'):
        j -= 1
    rows = [r for r in ss[j + 1:end + 1] if not re.fullmatch(r'[|\-: ]+', r)]
    pool = []
    for r in rows:
        got = [t['v'] for t in tokens(r) if t['k'] == kind]
        if not got:
            continue           # 머리글 줄
        if len(got) > 1:
            return []          # 한 줄에 같은 종류가 여럿이면 어느 열인지 알 수 없다
        pool.append(got[0])
    return pool


def check_title(title, body):
    """제목 숫자가 본문에 없으면 잡는다. 제목은 발행 뒤에 못 고친다(대기열 0-b (3)).

    자릿수 문자열로 맞대면 헛짚는다 — 제목 '4,400만원'을 본문은 '0.44억'으로, 제목 '4.46%'를
    본문은 '4.457%'로 적는다(2026-09-25 ktbrate·pyeong0924·jepqdist 에서 먼저 겪었다).
    그래서 값으로 맞대고, 제목에 적힌 자릿수만큼 반올림 여유를 준다."""
    if not title.strip():
        return []
    bt = tokens(body)
    bdigits = re.sub(r'\D', '', body)
    bad = []
    for t in tokens(title):
        if t['k'] == 'bare':
            # 단위 없이 적은 제목 숫자('165·285·330만원'의 285)는 종류를 알 수 없다.
            # 자릿수만 본문에 있으면 맞다고 본다.
            d = re.sub(r'\D', '', t['raw'])
            if t['v'] < 100 or 1900 <= t['v'] <= 2100 or len(d) < 2 or d in bdigits:
                continue
            bad.append('제목의 "%s" 가 본문에 없다 — 제목은 발행 뒤에 못 고친다' % t['raw'])
            continue
        same = [b for b in bt if b['k'] == t['k']]
        # 제목은 자리를 아끼느라 내려 적는다("41.94%포인트"를 "41%포인트"로).
        # 본문 값을 제목이 적은 자리에서 내림·반올림한 값이 같으면 맞다고 본다.
        step = _digits(t['raw']) * 2
        if any(near(b['v'], t['v'], t['raw']) or abs(b['v'] - b['v'] % step - t['v']) < 1e-9
               for b in same):
            continue
        bad.append('제목의 "%s" 가 본문에 없다 — 제목은 발행 뒤에 못 고친다' % t['raw'])
    return bad


def check_dates(body, facts):
    """본문이 말하는 날짜가 사실표에 있는 날짜인지 본다.
    jnj0925 에서 9월 23일 종가를 9월 24일 마감이라고 쓴 것이 이 검사로 잡히는 꼴이다."""
    if not facts.strip():
        return []

    def days(t):
        out = set()
        for m in re.finditer(r'(\d{1,2})\s*월\s*(\d{1,2})\s*일', t):
            out.add((int(m.group(1)), int(m.group(2))))
        for m in re.finditer(r'(\d{4})[-./](\d{1,2})[-./](\d{1,2})', t):
            out.add((int(m.group(2)), int(m.group(3))))
        # 점 표기(1.34)는 소수라서 날짜로 세지 않는다. 빗금(9/24)만 날짜로 본다.
        for m in re.finditer(r'\b(\d{1,2})/(\d{1,2})\b', t):
            out.add((int(m.group(1)), int(m.group(2))))
        return out

    fd = days(facts)
    if not fd:
        return []
    bad = []
    # 날짜와 '마감' 사이에 '269.17달러로' 처럼 소수점이 끼는 일이 많다.
    # [^.\n] 로 막으면 그 문장을 통째로 못 읽는다 — 숫자 사이의 점만 넘어가게 한다.
    #
    # 잡는 것은 **시세의 날짜**뿐이다(종가·마감). 지급일·발표일·공시일은 앞으로 올 일정으로 적는 일이
    # 많아 사실표에 날짜로 없는 게 정상이다 — 그것까지 잡으면 헛짚기가 된다(2026-09-25 실측 5건 중 4건).
    # 값이 붙은 시세 문장만 잡는다. '9월 28일은 …분기 마감' 같은 일정 문장은 시세가 아니다.
    for m in re.finditer(r'(\d{1,2})\s*월\s*(\d{1,2})\s*일(?:[^.\n]|\.(?=\d)){0,24}?'
                         r'\d[\d,]*(?:\.\d+)?\s*(?:달러|원)(?:[^.\n]|\.(?=\d)){0,8}?(종가|마감)', body):
        d = (int(m.group(1)), int(m.group(2)))
        # 그 달의 날짜가 사실표에 하나도 없으면 견줄 기준이 없는 것이다.
        if not any(x[0] == d[0] for x in fd):
            continue
        # 사실표의 마지막 날짜보다 뒤면 앞으로 올 일정이다(주간 캘린더 글이 그렇다).
        # 아직 오지 않은 날의 종가를 사실표가 가지고 있을 수는 없다.
        if d > max(fd):
            continue
        if d not in fd:
            bad.append('%d월 %d일(%s)이 사실표에 없는 날짜다 — 원자료 날짜와 맞는지 본다'
                       % (d[0], d[1], m.group(3)))
    return sorted(set(bad))


def run(pkg):
    body = ''
    for p in sorted(glob.glob(os.path.join(pkg, 'b*.txt')) + glob.glob(os.path.join(pkg, 'c*.txt'))):
        if os.path.basename(p).startswith('check'):
            continue
        body += open(p, encoding='utf-8').read() + '\n'
    facts = ''
    for c in (os.path.join(pkg, 'facts.txt'), os.path.join(os.path.dirname(pkg), 'facts.txt')):
        if os.path.exists(c):
            facts = open(c, encoding='utf-8').read()
            break
    tp = os.path.join(pkg, 'title.txt')
    title = open(tp, encoding='utf-8').read() if os.path.exists(tp) else ''
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from selfcheck import sents
    ss = sents(body)
    out = [('문장 %d' % i, m) for i, m in check_sents(ss)]
    out += [('제목', m) for m in check_title(title, body)]
    out += [('날짜', m) for m in check_dates(body, facts)]
    return out


if __name__ == '__main__':
    from selfcheck import resolve_pkg
    pkg = resolve_pkg(sys.argv[1])
    res = run(pkg)
    print('[검산] %s · 지적 %d건' % (os.path.basename(os.path.dirname(pkg)), len(res)))
    for where, msg in res:
        print('  [%s] %s' % (where, msg))
