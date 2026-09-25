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
        # 2026-09-25: 같은 오탐이 글머리표 목록에서도 났다. 카페 글 한 편에서 세 건이 그랬다 —
        # "· 1953~1956년 — 61세" 여섯 줄이 "'년세'로 끝나는 문장 세 번"으로, "· 혼자 최소 — 8,352만원"
        # 네 줄이 "'만원'로 끝나는 문장 세 번"으로 잡힌다. 목록은 나란히 놓으려고 일부러 모양을 맞춘 것이라
        # 어미가 같은 게 정상이다. 회차마다 고칠 수 없는 지적이 남으면 진짜 지적이 묻힌다.
        if line[0] in '|■#·•-*': continue
        # 출처 URL만 있는 줄은 문장이 아니다. 2026-09-25: SEC EDGAR 주소 한 줄이
        # '95자 긴문장'으로 잡혔다. 출처를 적으라는 규칙을 지킬수록 이 지적이 늘고,
        # 고칠 수 없는 지적이 매 회차 남으면 진짜 지적이 묻힌다.
        if re.fullmatch(r'https?://\S+', line): continue
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
            # 약어 바로 앞에 관형절이 붙으면 설명한 것으로 본다 — "나스닥 종목에 커버드콜을 거는 JEPQ",
            # "AMD를 따라가는 AMYY" 처럼 한국어에서 가장 흔한 꼴인데 괄호만 인정해서 계속 잡혔다(2026-09-25 19시 회차).
            # 단순히 가리키기만 하는 말(앞서 본·해당·위의)은 설명이 아니므로 뺀다.
            before = s[:m.start()].rstrip()
            mod = re.search(r'([가-힣]{2,})\s*$', before)
            # 동사를 하나씩 적어 두니 계속 빈틈이 생겼다(2026-09-26: "설계도를 파는 ARM",
            # "인텔을 뒤쫓는 AMD"가 목록에 없어 설명을 붙였는데도 지적으로 잡혔다).
            # 관형형 어미 '-는/-인'으로 끝나는 말이면 관형절로 본다. 가리키기만 하는 말은 아래에서 뺀다.
            if (mod
                    and re.search(r'(?:는|인)$', mod.group(1))
                    and not re.search(r'(?:앞서\s*본|해당|위의|같은|그런|이런)\s*$', before)
                    and len(re.findall(r'[가-힣]', before)) >= 6):
                continue
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
    # 형태소 분석기가 붙여 쓴 고유명사를 쪼개 돌려준다("프록터앤갬블" → "프록터 앤 갬블").
    # 그대로 본문과 맞추면 쓴 말도 안 썼다고 잡혔다(2026-09-26). 공백을 뺀 쪽도 같이 본다.
    body_ns = ''.join(body.split())
    for w in title_nouns(title):
        if body.count(w) == 0 and body_ns.count(''.join(w.split())) == 0:
            out.append((w, 0, '제목에 걸어 놓고 본문에서 한 번도 안 썼다 — 제목과 본문이 따로 논다'))
    return out


# ── 제목이 말이 되는지 ──────────────────────────────────────────────────
# 사장님 2026-09-26: "제목이 일반적으로 쓰는 문장이 아닌데 한국인이."
#   "비는 5년", "헐어 쓸 때의 차이", "돈 빌려주는 회사", "300원짜리가 167원짜리보다"
# 숫자를 욱여넣고 쉼표로 이어 붙이다 보니 말로는 안 하는 문어체 압축이 나온다.
# 실측(2026-09-26 · 네이버 상위 699개 대 우리 74개):
#   쉼표 19% 대 70% · 숫자 0개 59% 대 5% · 물음으로 끝 16% 대 3% · '다'로 끝 6% 대 24%
TITLE_BAD = [
    (r'(하는|되는|드는|비는|남는|받는|주는|나는)\s*\d+\s*(년|개월|곳|건|개|명)',
     '관형형 + 숫자 + 단위로 압축("비는 5년") — 말로는 이렇게 안 한다'),
    (r'\S*[할쓸울들볼줄؟]\s*때[의와과]', '"~할 때의 차이" 식 압축 — 풀어서 쓴다'),
    (r'\S+[을를]?\s*(헐어|메울|메워|비는|남는)\s', '"헐어 쓸 때·메울 때" — 일상에서 안 쓰는 말이다'),
    (r'\d+원짜리', '"300원짜리" — 무엇이 300원인지 제목만 보고 모른다'),
    (r'(저점|고점)의\s*\d', '"저점의 7배" — 주가인지 실적인지 안 밝혔다'),
    (r'돈\s*(빌려주는|빌리는)\s*회사', '"돈 빌려주는 회사" — 그렇게 부르는 사람이 없다. 원말을 쓰고 한 줄 풀어 준다'),
    (r'[가-힣]+의\s+[가-힣]+의\s', "'의'가 겹침 — 한 번만 쓴다"),
]

def title_check(t):
    """제목 하나를 읽고 말이 되는지 본다. 길이가 아니라 **표현**을 본다."""
    out = []
    if not t: return out
    for pat, why in TITLE_BAD:
        if re.search(pat, t): out.append(why)
    n = len(re.findall(r'\d[\d,.]*', t))
    if n >= 3: out.append(f'숫자 {n}개 — 상위 노출 제목은 59%가 0개다. 하나만 남긴다')
    if t.count(',') >= 2: out.append('쉼표 2개 이상 — 한 제목에 한 가지만 말한다')
    if re.search(r'다$', t.strip().rstrip('.')): out.append('"~다"로 끝남 — 상위 6%뿐이다. 명사나 물음으로 끝낸다')
    if len(t) > 45: out.append(f'{len(t)}자 — 상위 중앙값 33자')
    return out


# ── 본문이 읽히는지 ────────────────────────────────────────────────────
# 사장님 2026-09-26: "내용에도 문어체 압축, 말로는 안 하는 내용들 넣은 거 전부 확인해 봐.
#   데이터를 마구잡이로 나열해서 사람들이 글을 도저히 읽을 수가 없어.
#   그리고 출처만 말하면 되지 끝에 쓸데없는 말을 왜 해."
# 실제 글(쉐브론 배당편)에서 센 것: 표 5개 · 숫자 60개 넘음 · "~인 셈이죠" 3번 ·
#   맺음말 "앞으로 어떻게 될지는 쓰지 않았습니다" 같은 변명 2줄.
BODY_BAD = [
    (r'(인|한|된|하는)\s*셈이(죠|에요|예요|다|네요)', '"~인 셈이죠" — 말로는 잘 안 한다. 그냥 단정해서 쓴다'),
    (r'제가\s*(보기에|보니|봤|만들어|계산해|세어|열어)', '"제가 보기에·제가 표를 만들어 보니" — 글쓴이를 내세우지 않는다'),
    (r'저는\s.{0,12}(봤|했|썼)', '"저는 ~했어요" — 필요 없으면 뺀다'),
    (r'\S+로\s*바꾸면\s*\d+주', '"돈을 주식으로 바꾸면" — 산다고 쓴다'),
    (r'(쪽\s*사정|서\s*있는\s*자리|꼭대기\s*가까이)', '문어체 압축 — 풀어서 쓴다'),
    (r'(어느\s*쪽이\s*좋고\s*나쁘|좋다\s*나쁘다는\s*얘기는\s*아)', '안 한다는 말을 굳이 쓰지 않는다'),
    (r'(쓰지\s*않았습니다|적지\s*않았습니다|말하지\s*않)\s*[.。]?\s*$', '맺음말에 변명 — 출처만 남긴다'),
    (r'여기까지가\s', '"여기까지가 ~입니다" — 맺음말 군더더기'),
]

def body_style(text):
    """본문 표현과 숫자 밀도. 사장님이 "읽을 수가 없다"고 한 것을 숫자로 잡는다."""
    out, ss = [], sents(text)
    for i, x in enumerate(ss, 1):
        for pat, why in BODY_BAD:
            if re.search(pat, x): out.append((why, i, x[:56]))
    # 계산 과정을 한 줄씩 읊는 것 — 연달아 숫자 문장이 이어지면 읽기가 막힌다
    run = 0
    for i, x in enumerate(ss, 1):
        if len(re.findall(r'\d[\d,.]*', x)) >= 2:
            run += 1
            if run == 4: out.append(('숫자가 많은 문장이 네 줄 연달아 — 표로 빼거나 결론만 남긴다', i, x[:56]))
        else: run = 0
    # 표 개수는 구분선 '줄'을 센다. 전에는 '|---' 출현 횟수를 세서
    # |---|---|---| 한 줄이 표 3개로 잡혔다(2026-09-26 3개짜리 글이 10개로 나왔다).
    tables = sum(1 for ln in text.splitlines() if re.match(r'^\s*\|[\s|:-]*-[\s|:-]*\|?\s*$', ln))
    if tables >= 4: out.append((f'표 {tables}개 — 한 글에 셋까지. 넘으면 글이 자료집이 된다', 0, ''))
    nums = len(re.findall(r'\d[\d,.]*\s*(?:%|달러|원|배|주|곳|개|건)', text))
    body_n = max(len(re.sub(r'\s', '', text)), 1)
    if nums / body_n * 1000 > 35:
        out.append((f'1,000자당 숫자 {nums/body_n*1000:.0f}개 — 35개 넘으면 읽다가 놓친다', 0, ''))
    return out


# ── 여는 방식이 매번 같은가 ────────────────────────────────────────────
# 사장님 2026-09-26: "이상한 거 다른 것도 전부 다 확인해 봐."
# 최근 12편 중 8편이 같은 틀로 시작했다 — "~하게 되죠" 뒤에 "저도 그랬습니다".
# "저도 그랬습니다"만 네 번이다. 공감하는 척하는 같은 수법을 반복한 것이고,
# 네이버 공식 스팸 사례의 "동일·유사한 템플릿"에 그대로 해당한다.
OPEN_BAD = [
    (r'(보게\s*되죠|보시게\s*되죠|하게\s*되죠)', '"~하게 되죠"로 열지 않는다 — 최근 글 대부분이 이 틀이다'),
    (r'저도\s*(그랬|그렇게\s*알|처음엔|처음에는)', '"저도 그랬습니다" — 최근 12편에 네 번 나온 상투구다'),
    (r'(본\s*적\s*있으실|보신\s*적\s*있으실)', '"~보신 적 있으실 겁니다" — 같은 수법이다'),
]

def opening(text):
    """글 앞 세 문장이 늘 같은 틀이면 잡는다."""
    ss = sents(text)[:3]
    out = []
    for i, x in enumerate(ss, 1):
        for pat, why in OPEN_BAD:
            if re.search(pat, x): out.append((why, i, x[:50]))
    return out

def speech_mix(text):
    """한 글 안에서 평어체와 존댓말이 섞였나. 카페·블로그 통틀어 말투는 하나로 간다."""
    ss = [re.sub(r'\s', '', x) for x in sents(text)]
    ss = [x for x in ss if len(x) >= 8]
    if len(ss) < 10: return []
    polite = sum(1 for x in ss if re.search(r'(습니다|어요|에요|예요|죠|네요|군요)[.!?]?$', x))
    # 존댓말 종결은 'ㅂ니다' 전체다. 전에는 습니다·합니다·입니다 셋만 빼서
    # 들어옵니다·내려옵니다·됩니다 같은 문장이 평어체로 잡혔다(2026-09-26).
    plain  = sum(1 for x in ss if re.search(r'(다|음|함)[.!?]?$', x) and not re.search(r'(니다|니까)[.!?]?$', x))
    tot = polite + plain
    if tot < 8: return []
    r = min(polite, plain) / tot
    if r > 0.25:
        return [(f'말투가 섞였다 — 존댓말 {polite}문장, 평어체 {plain}문장. 한 글은 하나로 간다', 0, '')]
    return []

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
        for why in title_check(title):
            out.append(('제목', 0, f'{why} · {title[:44]}'))
        for w, n, why in title_kw_in_body(title, text):
            out.append(('제목말빠짐', 0, f'"{w}" {why}'))
    for why, i, frag in opening(text) + speech_mix(text) + body_style(text):
        out.append(('본문말투', i, f'{why}' + (f' · {frag}' if frag else '')))
    # 숫자가 중간에서 갈라진 것. 2026-09-26 06시 회차: 문단을 잘게 나누려고 돌린 스크립트가
    # 소수점을 문장 끝으로 보고 잘라 "5.18%"가 "5. 18%"로, "0.93%"가 "0. 93%"로 깨졌다.
    # 본문 세 조각이 그렇게 망가졌는데 readcheck도 selfcheck도 지적 0건으로 통과시켰다.
    # 숫자가 틀린 채 나가는 것은 가장 큰 사고라 발행 전에 반드시 걸러야 한다.
    for m in re.finditer(r'\d\.\s+\d', text):
        out.append(('숫자깨짐', 0, f'숫자가 소수점에서 갈라졌다 · …{text[max(0, m.start() - 14):m.end() + 14]}…'))
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
