# 글이 읽히는지 본다 — 맞는 사실을 틀린 한국어로 쓰면 못 읽는다.
#   py -3.12 work/readcheck.py work/research/<주제>/pkg
#   py -3.12 work/readcheck.py --all 12          → 최근 발행 12편을 한꺼번에
#
# 사장님 2026-09-24: "우리가 글도 이해 잘 되게 쓰고 한글 문맥이 맞게 쓰는지도!
#                    글을 잘 쓴다는 게 무슨 말인지 몰라?"
#
# selfcheck는 사실 대조와 말투(문장 길이·어미 비율)만 본다. bodystudy는 구조와 항목을 본다.
# 문장이 말이 되는지, 앞뒤가 이어지는지, 처음 보는 말을 설명했는지는 아무도 안 봤다.
#
# 여기서는 **기계가 틀렸다고 단정할 수 있는 것만** 잡는다.
# 문체가 좋은지 나쁜지는 재지 않는다 — 그건 취향이고, 취향을 기계가 판정하면 글이 납작해진다.
import sys, os, re, glob, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')

def jong_of(ch):
    """한글 음절의 받침 번호. 0이면 받침 없음, 8이면 ㄹ."""
    if not ('가' <= ch <= '힣'): return None
    return (ord(ch) - 0xAC00) % 28

def has_jong(ch):
    j = jong_of(ch)
    return None if j is None else j != 0

# 받침에 따라 갈리는 조사 짝 — (받침 있을 때, 받침 없을 때)
PAIRS = {'을': '를', '은': '는', '이': '가', '과': '와', '으로': '로'}
BACK = {v: k for k, v in PAIRS.items()}

_kiwi = None
def kiwi():
    """형태소 분석 없이 조사를 보면 안 된다. 첫 판(2026-09-24)에서
    '남는 건'을 '남은 건'으로, '물가 3.35%'를 '물이'로 잡았다 — 오탐이 90%였다.
    '-는'은 동사 관형형 어미이기도 하고, '물가·종가·차이·사이'는 끝 글자가 조사처럼 생겼을 뿐이다.
    kiwi가 J로 시작하는 태그를 붙인 것만 조사로 본다."""
    global _kiwi
    if _kiwi is None:
        from kiwipiepy import Kiwi
        _kiwi = Kiwi()
    return _kiwi

def josa_errors(text):
    """받침과 안 맞는 조사. 한국어에서 이건 취향이 아니라 오류다.
    숫자·영문 뒤는 읽는 법이 사람마다 갈려(3을/3를) 건드리지 않는다."""
    bad = []
    try: toks = kiwi().tokenize(text)
    except Exception: return bad
    for i, t in enumerate(toks):
        if not t.tag.startswith('J') or i == 0: continue
        j = t.form
        if j not in PAIRS and j not in BACK: continue
        prev = toks[i - 1]
        if prev.end != t.start: continue          # 붙어 있지 않으면 건너뛴다
        last = (prev.form or '')[-1:]
        jong = has_jong(last)
        if jong is None: continue                  # 숫자·영문 뒤는 안 본다
        # ㄹ 받침 뒤에는 '로'가 맞다 — 12월로·구별로·헤알로. 이걸 빼면 멀쩡한 말을 고치게 된다
        # (2026-09-24 첫 판이 '월로 → 월으로'를 지적했다).
        if jong_of(last) == 8 and j in ('로', '으로'):
            if j == '으로': bad.append((t.start, prev.form + j, prev.form + '로'))
            continue
        want = None
        if j in PAIRS and jong is False: want = PAIRS[j]      # 받침 없는데 받침용 조사
        elif j in BACK and jong is True: want = BACK[j]       # 받침 있는데 받침없음용 조사
        if want: bad.append((t.start, prev.form + j, prev.form + want))
    return bad

DUP = [(r'가장\s+최(고|선|우선)', '가장 최고 — 겹말'), (r'약\s*[\d,]+\s*(원|만원|억원)\s*정도', '약~정도 — 겹말'),
       (r'미리\s+예(상|측|고)', '미리 예상 — 겹말'), (r'다시\s+재(개|검토|확인)', '다시 재개 — 겹말'),
       (r'스스로\s+자(각|발)', '스스로 자발 — 겹말'), (r'과반수\s*이상', '과반수 이상 — 겹말'),
       (r'매\s*시간\s*마다', '매 시간마다 — 겹말'), (r'결(론|과)적으로\s+결(론|과)', '결론 겹말')]

VAGUE = re.compile(r'(이것|그것|저것|이런\s*점|해당\s*(부분|내용)|여기서\s*말하는)')

def sents(t):
    out = []
    for line in t.splitlines():
        line = line.strip()
        if not line: continue
        # 표 행·소제목은 문장이 아니다. 2026-09-24: 표 행 "| 1.75억 | 25건 |"이 문장으로 잡혀
        # "'억건'로 끝나는 문장이 세 번 이어진다"는 어미반복 오탐이 났다.
        if line[0] in '|■#': continue
        for s in re.split(r'(?<=[.!?])\s+|(?<=다\.)\s*', line):
            s = s.strip()
            if s: out.append(s)
    return out

def acronyms(text):
    """설명 없이 튀어나온 영문 약어·티커. 사장님 2026-09-24 "레나 주가가 뭔데?" —
    처음 나올 때 무엇인지 안 밝히면 독자가 못 따라온다."""
    KNOWN = {'ETF', 'API', 'GDP', 'CPI', 'PPI', 'FOMC', 'EPS', 'PER', 'PBR', 'ROE', 'ISA', 'IRP',
             'DSR', 'LTV', 'DTI', 'IPO', 'CEO', 'GDP', 'US', 'EU', 'PDF', 'TV', 'AI'}
    first, bad = {}, []
    ss = sents(text)
    # 한글 조사가 붙으면('ACE는') 가 경계로 안 잡혀 첫 등장을 놓쳤다 — 영문자만 경계로 본다
    PAT = re.compile(r'(?<![A-Za-z])([A-Z]{2,5})(?![A-Za-z])')
    EXPLAIN = re.compile(r'이름|운용사|브랜드|운용하는|약자|줄임말|지수|종목코드|지표|뜻하|가리키|부른다|부릅니다')
    for i, s in enumerate(ss, 1):
        for m in PAT.finditer(s):
            w = m.group(1)
            if w in KNOWN or w in first: continue
            first[w] = i
            # 같은 문장 안에 괄호 설명이나 한글 이름이 붙어 있으면 설명한 것으로 본다
            # 약어 바로 뒤에 괄호로 풀어 쓰면 설명한 것으로 본다(긴 정식명은 24자 창을 넘어간다)
            if s[m.end():m.end() + 1] in '(（': continue
            near = s[max(0, m.start() - 24):m.end() + 24]
            if re.search(r'[(（][^)）]*[)）]', near) or re.search(r'[가-힣]{2,}\s*\(' + w, s): continue
            # 같은 문장에서 "...를 AFFO라고 합니다"처럼 풀어 쓴 것도 설명으로 본다.
            # 2026-09-25: 괄호로만 인정해서, 앞에 뜻을 다 적고 "~라고 합니다"로 받은 문장을 설명 없음으로 잡았다.
            if re.search(w + r'\s*(?:라고|라곤|라 부|라 한)', s) and len(re.findall(r'[가-힣]', s[:m.start()])) >= 6: continue
            # 바로 다음 문장에서 풀어 쓰는 것도 설명으로 본다(한국어 글에서 흔한 순서)
            nxt = ss[i] if i < len(ss) else ''
            if w in nxt and EXPLAIN.search(nxt): continue
            bad.append((i, w, s[:70]))
    return bad


KW_STOP = set('다음 이번 지난 최근 정도 관련 내용 확인 가능 필요 경우 기준 방법 이유 시작 정리 총정리 얼마 무엇 어디 언제'.split())

def title_nouns(title):
    """제목에서 그 글의 핵심어를 뽑는다. 조사가 붙은 채로 세면 '주가와'가 핵심어가 된다."""
    try:
        toks = kiwi().tokenize(title or '')
        ws = [t.form for t in toks if t.tag in ('NNG', 'NNP', 'SL') and len(t.form) >= 2]
    except Exception:
        ws = [w for w in re.split(r'[^가-힣A-Za-z]+', title or '') if len(w) >= 2]
    return [w for w in ws if w not in KW_STOP][:3]

def title_kw_in_body(title, body):
    """제목에 건 말을 본문에서 **한 번도 안 쓴 것만** 잡는다.

    2026-09-24: 처음에 "상위 글은 23~43회 쓰니 우리도 20~40회 쓰라"는 기준을 넣었다가 뺐다.
    네이버 공식 문서(2024-02-28 '생성형 AI 활용 문서에 대한 검색 노출 정책 안내')가
    어뷰징 행위로 못박은 첫 항목이 바로 그것이다 —
      "검색 노출을 위해 유사한 키워드를 반복적으로 사용하는 행위".
    상위 글이 33회 쓰는 것은 글이 3,900자라 자연히 그렇게 된 것이지 일부러 넣은 것이 아니다.
    밀도로 보면 우리가 오히려 높았다(1.01% 대 0.84%).

    그래서 여기서는 횟수를 요구하지 않는다. **0회만 잡는다** —
    "국채금리 2026…"이 본문에 '국채금리'를 한 번도 안 쓰고 '국고채 금리·10년물'로만 쓴 것,
    "미국증시 섹터별로 갈린 하루"가 '증시'를 한 번도 안 쓴 것은 제목과 본문이 따로 노는 것이라
    키워드 채우기와 다른 문제다. 길이는 bodyrule.md가 따로 본다."""
    out = []
    for w in title_nouns(title):
        if body.count(w) == 0:
            out.append((w, 0, '제목에 걸어 놓고 본문에서 한 번도 안 썼다 — 제목과 본문이 따로 논다'))
    return out

def check(text, title=None):
    out = []
    ss = sents(text)
    for i, s in enumerate(ss, 1):
        plain = re.sub(r'\s', '', s)
        for pos, wrong, right in josa_errors(s):
            out.append(('조사', i, f'"{wrong}" → "{right}" · {s[:60]}'))
        for pat, why in DUP:
            if re.search(pat, s): out.append(('겹말', i, f'{why} · {s[:60]}'))
        if len(plain) > 80:
            out.append(('긴문장', i, f'{len(plain)}자 — 한 문장에 하나만 말한다 · {s[:60]}'))
        n = len(re.findall(r'\d[\d,.]*\s*(?:%|원|만원|억원|배|명|건|년|월|일|%p)', s))
        if n >= 5:
            out.append(('숫자과다', i, f'한 문장에 숫자 {n}개 — 표로 빼거나 문장을 나눈다 · {s[:60]}'))
        if VAGUE.search(s) and i > 1:
            out.append(('지시어', i, f'가리키는 대상이 분명한지 확인 · {s[:60]}'))
    if title:
        for w, n, why in title_kw_in_body(title, text):
            out.append(('제목말빠짐', 0, f'"{w}" {why}'))
    for i, w, s in acronyms(text):
        out.append(('설명없음', i, f'"{w}"가 처음 나오는데 무엇인지 안 밝혔다 · {s}'))
    # 같은 어미가 세 문장 연속이면 읽는 리듬이 죽는다
    ends = [re.sub(r'[^가-힣]', '', s)[-2:] for s in ss if len(re.sub(r'[^가-힣]', '', s)) >= 2]
    run, prev = 1, None
    for i, e in enumerate(ends, 1):
        if e == prev:
            run += 1
            if run == 3: out.append(('어미반복', i, f'"{e}"로 끝나는 문장이 세 번 이어진다'))
        else: run, prev = 1, e
    return out

def body_of(pkg):
    t = []
    # 'c*.txt'로 훑으면 check_self.txt·check_gpt.txt 같은 검사 결과까지 본문으로 읽는다(2026-09-24 실제).
    files = sorted(glob.glob(os.path.join(pkg, 'b[0-9]*.txt'))) or sorted(glob.glob(os.path.join(pkg, 'c[0-9]*.txt')))
    for f in files:
        try: t.append(open(f, encoding='utf-8').read())
        except Exception: pass
    return '\n'.join(t)

def main():
    a = sys.argv[1:]
    if a and a[0] == '--all':
        n = int(a[1]) if len(a) > 1 else 12
        pks = [p for p in glob.glob(os.path.join(R, '*', 'pkg')) if os.path.exists(os.path.join(p, 'published.txt'))]
        pks.sort(key=lambda p: -os.path.getmtime(os.path.join(p, 'published.txt')))
        pks = pks[:n]
    elif a:
        pks = [os.path.abspath(a[0])]
    else:
        sys.exit('묶음 경로 또는 --all N')
    total = 0
    for pk in pks:
        body = body_of(pk)
        if not body: continue
        try: title = open(os.path.join(pk, 'title.txt'), encoding='utf-8').read().strip()
        except Exception: title = None
        probs = check(body, title)
        name = os.path.basename(os.path.dirname(pk))
        if probs:
            print(f'\n[{name}] {len(probs)}건')
            for kind, i, msg in probs[:12]: print(f'  {kind} {i}번 문장: {msg}')
        total += len(probs)
        try: open(os.path.join(pk, 'check_read.txt'), 'w', encoding='utf-8').write(
            '\n'.join(f'{k}\t{i}\t{m}' for k, i, m in probs) or '지적 없음\n')
        except Exception: pass
    print(f'\n검사 {len(pks)}편 · 지적 {total}건')
    sys.exit(1 if total else 0)

if __name__ == '__main__': main()
