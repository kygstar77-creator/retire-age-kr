# R-1 대본 v6 검사(cloud/r1-remake-1003): 실측 목표 + 숫자 출처(facts.txt) + 자막 줄은 읽지 않음
#   python3 -m pytest work/tests/test_r1_script_v6.py -q
import os, re, sys
WORK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
LF = os.path.join(WORK, 'research', 'longform')
sys.path.insert(0, os.path.join(LF, 'loop'))
import speechcompare_script as sc  # noqa: E402

EP = os.path.join(LF, 'ep', 'R-1')
V6 = os.path.join(EP, 'script.v6.md')
FACTS = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()

# 말에서 반올림해 부른 값 → facts.txt에 있는 정확값(오차 2% 이내, 아래 테스트가 계산으로 확인)
ROUND = {
    '40만원': 397320, '16만원': 164357, '192만원': 1916240, '56만원': 559242, '24만원': 244007,
    '52만원': 522060, '212만원': 2123460, '22만원': 222060, '97만원': 966540, '332만원': 3316320, '419만원': 4187700,
    '15%': 15.01, '20%': 19.68, '7%': 7.15, '16%': 15.99, '10%': 10.23, '3%': 3.37, '2%': 2.18,
}

def won(v):
    return f'{v:,}'

def test_targets_met():
    r = sc.measure(V6)
    assert r['숫자/1000단어'] <= 90, r
    assert r['숫자 2개 이상 문장 %'] <= 20, r
    assert 12 <= r['예상 길이(분, 글자÷5.65)'] <= 15, r

def test_v5_baseline_is_worse():
    r5, r6 = sc.measure(os.path.join(EP, 'script.md')), sc.measure(V6)
    assert r6['숫자/1000단어'] < r5['숫자/1000단어'] and r6['숫자 2개 이상 문장 %'] < r5['숫자 2개 이상 문장 %']

def test_caption_lines_not_spoken():
    secs = sc.parse(V6)
    spoken = [l for s in secs for l in s['lines']]
    assert spoken and all('[자막' not in l and '(화면' not in l for l in spoken)
    caps = [c for s in secs for c in s['captions']]
    assert len(caps) >= 30
    # lfvoice.sections와 같은 규칙으로 읽어도 자막·화면 줄이 섞이지 않는다
    body = open(V6, encoding='utf-8').read().split('\n---', 1)[0]
    for line in body.splitlines():
        if '[자막:' in line:
            assert not line.lstrip().startswith('- '), line

def round_sig(x, n):
    from math import floor, log10
    return round(x, -int(floor(log10(abs(x)))) + (n - 1))

def test_round_values_are_roundings_of_facts():
    """반올림 값 = facts 정확값을 유효숫자 1~3자리로 반올림한 값(새 숫자를 지어내지 않았다는 증거)"""
    for k, exact in ROUND.items():
        if k.endswith('만원'):
            v = int(k[:-2]) * 10000
            assert won(exact) in FACTS, (k, exact)
        else:
            v = float(k[:-1])
            assert f'{exact:.2f}%' in FACTS, (k, exact)
        assert any(abs(round_sig(exact, n) - v) < 1e-9 for n in (1, 2, 3)), (k, exact)

MULT = {'억': 1e8, '천만': 1e7, '만': 1e4, '천': 1e3, None: 1}
TOK = re.compile(r'(\d[\d,]*(?:\.\d+)?)\s*(억|천만|만|천)?')

def nums(t):
    """글 속 숫자를 값으로: '1억 1,599만원'→115,990,000 · '39만 7천원'→397,000 · '2.58%'→2.58 · '2,580,000원'→2,580,000"""
    toks, out, i = list(TOK.finditer(t)), [], 0
    while i < len(toks):
        m = toks[i]
        val, raw = float(m[1].replace(',', '')) * MULT[m[2]], m[0]
        while i + 1 < len(toks) and toks[i + 1].start() - m.end() <= 1 and m[2] in ('억', '만') and toks[i + 1][2] in ('천만', '만', '천') \
                and MULT[toks[i + 1][2]] < MULT[m[2]]:
            i += 1; m = toks[i]; val += float(m[1].replace(',', '')) * MULT[m[2]]; raw += ' ' + m[0]
        out.append((round(val, 6), raw.strip())); i += 1
    return out

FACTSET = {v for v, _ in nums(FACTS)}

def test_nums_parser():
    assert [v for v, _ in nums('1억 1,599만원 · 39만 7천원 · 2.58% · 2,580,000원 · 2천만원')] == [115990000, 397000, 2.58, 2580000, 20000000]

def test_every_number_comes_from_facts():
    """말·자막의 모든 숫자 값이 facts.txt에 있거나, ROUND(반올림 → facts 정확값)에 있다. 날짜·조문 번호는 facts에 있는 숫자인지만 본다."""
    secs = sc.parse(V6)
    texts = [l for s in secs for l in s['lines']] + [c for s in secs for c in s['captions']]
    rounded = {round(int(k[:-2]) * 1e4, 6) if k.endswith('만원') else float(k[:-1]) for k in ROUND}
    norm = lambda t: re.sub(r'(\d{4})\.(\d{1,2})\.(\d{1,2})', r'\1-\2-\3', t)
    bad = [(t, raw) for t in texts for v, raw in nums(norm(t)) if v not in FACTSET and v not in rounded]
    assert not bad, '\n'.join(f'{b[1]!r} <- {b[0]}' for b in bad)

def test_spoken_lines_use_one_number_mostly():
    sents = sc.sentences(sc.spoken(V6))
    multi = [s for s in sents if len(nums(s)) >= 2]
    assert len(multi) / len(sents) <= 0.10, multi    # 값 기준(억·만 묶음을 숫자 하나로)으로도 10% 이하

def test_no_product_recommendation_words():
    spoken = sc.spoken(V6)
    for w in ['추천', '사세요', '사라', '좋은 상품', '무조건 사']:
        assert w not in spoken, w
