# 교차검증 대체 — 사장님 2026-09-23 밤: "교차검증 못 받을 경우엔 어떻게든 알아서 잘 검증해보라고!"
#   py -3.12 work/selfcheck.py <pkg폴더>
#
# 제미나이 무료 하루 할당량이 차면 crosscheck.py가 통째로 건너뛰었다(오늘 묶음 6개가 검증 없이 대기).
# 그래서 키가 없어도 도는 검증을 만든다. 두 가지를 기계로 잰다.
#   1) 사실 대조 — 본문의 숫자·날짜가 facts.txt에 있는가 (GPT가 하던 일의 핵심)
#   2) 말투     — 문장 길이·어미 분포·1인칭·조문 번호·물음표를 실측 기준과 견준다 (Gemini가 하던 일)
# 결과는 pkg/check_self.txt 에 '몇 번 문장이 왜 문제인지'로 남는다. 고치는 건 회차 루틴(클로드)이 한다.
# 기준 출처: work/research/cafe_style/benchmark_2026-09-23.md (잘 읽히는 카페 글 15편 730문장 실측)
import sys, os, re, json, glob, statistics
sys.stdout.reconfigure(encoding='utf-8')

TARGET = {   # 실측값. 지어낸 값이 아니다.
    'cafe': {'문장길이중앙': (24, 40), '습니다비율': (0.10, 0.35), '1인칭비율': (0.03, 0.20),
             '조문번호': (0, 0), '물음표비율': (0.0, 0.08)},
    # 블로그는 평어체가 기준이다(사장님 "담백하잖아") — ~습니다로 끝나는 문장이 적은 게 정상이다.
    # 2026-09-24 실측: 발행된 블로그 39편의 문장 길이 중앙값이 24~54자(중앙 39). 그 범위로 잡는다.
    'blog': {'문장길이중앙': (24, 56), '습니다비율': (0.0, 0.30), '1인칭비율': (0.0, 0.20),
             '조문번호': (0, 1), '물음표비율': (0.0, 0.08)},
}
BAN = ['정리하면', '핵심은', '결론적으로', '시사한다', '살펴보겠습니다', '알아보겠습니다',
       '중요합니다', '주목할 필요', '~라 할 수 있다', '것으로 보인다', '전망이다']
SELF_TALK = ['이 글은', '본 글에서는', '원문을 그대로', '조문 내용만', '투자 판단은 적지']

def sents(t):
    # 줄바꿈을 먼저 가르고 줄 안에서만 문장을 나눈다. 표처럼 줄마다 한 항목을 적은 목록은
    # 끝에 마침표가 없어서, 전체를 한 줄로 펴면 여러 줄이 통째로 묶여 '177자 한 문장'으로 잡혔다
    # (2026-09-24 firereview 묶음에서 확인한 헛짚형).
    out = []
    for line in t.splitlines():
        line = re.sub(r'[ 	]+', ' ', line).strip()
        if not line: continue
        for s in re.split(r'(?<=[.!?])\s+|(?<=다\.)\s*', line):
            if len(s.strip()) > 4: out.append(s.strip())
    return out

def money_norm(t):
    """'1억 8,907만원'과 사실표의 '18,907'(만원)을 같은 값으로 본다.
    안 맞추면 억/만원 표기가 쪼개져 멀쩡한 숫자를 '사실표에 없다'고 잡는다(2026-09-23 확인)."""
    def f(x): return float(x.replace(',', ''))
    # '원'으로 끝나는 것만 만원 단위로 맞춘다. 달러 금액은 건드리지 않는다.
    t = re.sub(r'(\d[\d,]*(?:\.\d+)?)\s*억\s*([\d,]+)\s*만\s*원',
               lambda m: f'{f(m.group(1)) * 10000 + f(m.group(2)):.0f}', t)
    t = re.sub(r'(\d[\d,]*(?:\.\d+)?)\s*억\s*원', lambda m: f'{f(m.group(1)) * 10000:.0f}', t)
    t = re.sub(r'(\d[\d,]*)\s*만\s*원', lambda m: f'{f(m.group(1)):.0f}', t)
    return t

def numbers(t):
    """비교할 만한 숫자만. 한 자리 수·연도 조각은 오탐이 많아 뺀다.
    사실표는 '28.38'처럼 원래 단위로, 본문은 '28.38억원'처럼 쓰는 일이 많다.
    그래서 쓴 그대로와 만원으로 맞춘 것 **둘 다** 모아 비교한다(2026-09-23)."""
    out = set()
    for m in re.findall(r'\d[\d,]*\.?\d*', t):
        x = m.replace(',', '').rstrip('.')
        if len(x.replace('.', '')) >= 2: out.add(x)
        if x.endswith('.0'): out.add(x[:-2])
    return out

def unit_expand(t):
    """사실표의 '542.52억'과 본문의 '542억 5,200만'을 같은 값으로 본다.
    소수점 억 표기를 만 단위 정수로 펴서 자릿수 문자열에 넣어 둔다.
    2026-09-24: 애플 실적 글에서 제품별 매출 7줄이 통째로 '사실표에 없는 숫자'로 잡혔다.
    값은 같은데 표기만 달랐다. 사실표를 매번 두 벌로 적는 대신 여기서 편다."""
    out = []
    for m in re.finditer(r'(\d[\d,]*\.\d+)\s*억', t):
        out.append(f'{float(m.group(1).replace(",", "")) * 10000:.0f}')   # 억 -> 만 단위
    for m in re.finditer(r'(\d[\d,]*\.\d+)\s*조', t):
        out.append(f'{float(m.group(1).replace(",", "")) * 10000:.0f}')
    return ' '.join(out)

def facts_numbers(t):
    """사실표 쪽만 표기를 넓혀서 모은다. 본문 숫자를 가공하면 없던 값이 생겨 헛짚는다(2026-09-23)."""
    return numbers(t) | numbers(money_norm(t)) | numbers(unit_expand(t))


# 표본이 너무 적은데 일반화하는 글을 막는다.
# 사장님 2026-09-24: "네 편만 보고 일반화를 시켜버렸네? 이딴 쓰레기 글을 올려놨어."
def thin_sample(body, facts):
    """남의 글 몇 편을 세어 결론을 내는 글을 막는다.
    2026-09-24 사고: 블로그 후기 4편을 읽고 "자산을 밝힌 건 0편"을 제목으로 뽑아 발행했다.
    숫자가 사실표와 맞아 [사실] 0건으로 통과했다. 맞는 숫자여도 표본이 4면 결론이 될 수 없다.

    글 전체에서 '읽은 글 수'를 찾아, 그 수가 30 미만인데 전부/하나도 같은 말로
    결론을 내면 잡는다. 공식 조사(응답자 수천 명)는 예외다."""
    ss = sents(body)
    text = ' '.join(ss)
    # 이 글이 몇 편을 읽었는지
    ns = [int(m.group(1)) for m in re.finditer(r'(\d+)\s*편', text)]
    han = re.search(r'(글|후기|포스팅|사례)\s*(\d+)\s*편|(\d+)\s*편.{0,6}(골라|읽|봤|확인)', text)
    small = [n for n in ns if 1 <= n < 30]
    if not small:
        return []
    n_read = min(small)
    CONCLUDE = r'(한 편도|하나도|전혀|모두|전부|다)\s*(없|않|아니|같)|공통|하나같이|뿐이|0편'
    OFFICIAL = r'조사|패널|통계청|국민연금|가계금융|응답자|\d{3,}명|설문'
    bad = []
    for i, x in enumerate(ss, 1):
        if not re.search(CONCLUDE, x): continue
        if re.search(OFFICIAL, x): continue
        bad.append((i, x[:80], n_read))
    return bad


def resolve_pkg(arg):
    """묶음 경로를 받아준다. 다음을 모두 허용한다.
      work/research/foo/pkg  ·  work/research/foo  ·  foo
    이름만 준 경우 work/research/<이름>/pkg 를 찾는다(2026-09-24 13시 회차: 이름만 줬다가
    저장소 루트로 해석돼 '조각 파일 없음'이 났다)."""
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [arg, os.path.join(arg, 'pkg'),
             os.path.join(here, 'research', arg, 'pkg'),
             os.path.join(here, 'research', arg)]
    for c in cands:
        if os.path.isdir(c) and (glob.glob(os.path.join(c, 'b[0-9]*.txt')) or glob.glob(os.path.join(c, 'c[0-9]*.txt'))):
            return os.path.abspath(c)
    return os.path.abspath(arg)


def main(pkg):
    kind = 'cafe' if any(os.path.basename(p).startswith('c') for p in glob.glob(os.path.join(pkg, 'c0*.txt'))) else 'blog'
    # 사실표는 pkg 안에 있기도 하고 한 단계 위에 있기도 하다(묶음마다 다르다 — 2026-09-23 확인)
    facts, fp = '', None
    for cand in (os.path.join(pkg, 'facts.txt'), os.path.join(os.path.dirname(pkg), 'facts.txt')):
        if os.path.exists(cand) and os.path.getsize(cand) > 100:
            fp = cand; facts = open(cand, encoding='utf-8').read(); break
    body = ''
    for p in sorted(glob.glob(os.path.join(pkg, 'b*.txt')) + glob.glob(os.path.join(pkg, 'c*.txt'))):
        if os.path.basename(p).startswith('check'): continue
        body += open(p, encoding='utf-8').read() + '\n'
    if not body.strip(): print('본문 조각이 없다:', pkg); return 2

    ss = sents(body)
    problems = []

    # 1) 사실 대조 — 본문에 있는데 사실표에 없는 숫자
    if not facts.strip():
        problems.append(('사실', 0, '(facts.txt가 비어 있다 — 사실 대조를 할 수 없다)'))
    else:
        fnum = facts_numbers(facts)
        # 사실표는 '18,907'로, 본문은 '1억 8,907만원'으로 쓴다. 단위 표기를 아무리 맞춰도 끝이 없어서,
        # 사실표의 숫자만 이어 붙인 문자열에 그 자릿수가 들어 있으면 '있는 숫자'로 본다(2026-09-23).
        fdigits = re.sub(r'\D', '', facts + ' ' + money_norm(facts) + ' ' + unit_expand(facts))
        for i, s in enumerate(ss, 1):
            extra = {x for x in numbers(s) - fnum if x.replace('.', '').replace(',', '') not in fdigits}
            if not extra: continue
            # 사실표 숫자끼리 더하고 빼서 나온 값은 '없는 숫자'가 아니다. 계산 문장은 참고로만 표시한다.
            calc = re.search(r'빼|더하|곱하|나누|차이|합치|배다|배로|%p|퍼센트포인트|이 되고|쯤|그러니까|즉|곧|환산|기준으로', s)
            problems.append(('계산' if calc else '사실', i,
                             f'사실표에 없는 숫자 {sorted(extra)} · {s[:70]}'))

    # 2) 말투 — 실측 기준과 견준다
    # 표 행과 소제목은 문장이 아니다. 숫자 검사(1)에는 그대로 두되 말투 통계에서는 뺀다.
    # 2026-09-25: 표 두 개(52행·중앙 19자)가 산문 79문장(중앙 29자, 기준 안)을 20자로 끌어내려
    # 멀쩡한 글에 '문장이 짧다'는 지적이 붙었다. 표가 많은 통계형 글은 늘 이렇게 걸린다.
    prose = [s for s in ss if not s.startswith(('|', '#', '-'))] or ss
    lo, hi = TARGET[kind]['문장길이중앙']
    med = statistics.median(len(s) for s in prose)
    if not lo <= med <= hi:
        problems.append(('말투', 0, f'문장 길이 중앙값 {med:.0f}자 — 기준 {lo}~{hi}자. 긴 문장을 끊어야 한다'))
    ss = prose
    n = len(ss)
    r_sum = sum(1 for s in ss if s.rstrip('.').endswith(('습니다', '입니다'))) / n
    lo, hi = TARGET[kind]['습니다비율']
    if not lo <= r_sum <= hi:
        problems.append(('말투', 0, f'~습니다/입니다로 끝나는 문장 {r_sum:.0%} — 기준 {lo:.0%}~{hi:.0%}. 어미를 섞어야 한다'))
    r_i = sum(1 for s in ss if re.search(r'(저는|제가|저도|우리)', s)) / n
    lo, hi = TARGET[kind]['1인칭비율']
    if not lo <= r_i <= hi:
        problems.append(('말투', 0, f'1인칭 문장 {r_i:.0%} — 기준 {lo:.0%}~{hi:.0%}'))
    r_q = sum(1 for s in ss if '?' in s) / n
    if r_q > TARGET[kind]['물음표비율'][1]:
        problems.append(('말투', 0, f'물음표 문장 {r_q:.0%} — 기준 {TARGET[kind]["물음표비율"][1]:.0%} 이하'))
    law = [i for i, s in enumerate(ss, 1) if re.search(r'제\s?\d+조(의\d+)?\s?제?\d*항?', s)]
    if len(law) > TARGET[kind]['조문번호'][1]:
        problems.append(('말투', law[0], f'조문 번호를 {len(law)}문장에서 읽는다 — 출처로 한 번만 적고 본문은 풀어 쓴다'))
    for i, s in enumerate(ss, 1):
        for w in BAN:
            if w in s: problems.append(('말투', i, f'보고서투 "{w}" · {s[:60]}'))
        for w in SELF_TALK:
            if w in s: problems.append(('말투', i, f'글이 스스로를 설명 "{w}" · {s[:60]}'))
        if len(s) > 120: problems.append(('말투', i, f'{len(s)}자 한 문장 — 끊어야 한다 · {s[:60]}'))

    # 2-b) 계산 검산 — 값을 실제로 다시 계산한다(calcheck.py, 2026-09-25 17시 C 회차).
    # 여기까지의 검사는 "본문 숫자가 사실표에 있나"만 본다. 사실표 숫자로 만든 파생값이 틀려도
    # 자릿수가 섞여 있으면 통과했다(acediv0924 의 4억 5,340만원, jnj0925 의 9월 23일→24일).
    # 그 구멍을 막는다. 발행된 123묶음에 돌려 지적 2건(둘 다 실제 문제)만 나오는 걸 확인했다.
    try:
        import calcheck
        tpath = os.path.join(pkg, 'title.txt')
        title = open(tpath, encoding='utf-8').read() if os.path.exists(tpath) else ''
        for i, msg in calcheck.check_sents(sents(body)):
            problems.append(('검산', i, msg))
        for msg in calcheck.check_title(title, body) + calcheck.check_dates(body, facts):
            problems.append(('검산', 0, msg))
    except Exception as e:
        problems.append(('검산', 0, f'계산 검산이 돌지 않았다: {e}'))

    # 표본이 적은데 일반화하는 문장 — 발행을 막는다
    for i, s, nread in thin_sample(body, facts):
        problems.append(('표본', i, (f'{nread}편으로 일반화' if nread else '적은 표본으로 일반화')
                         + f' — 남의 글 몇 편을 세어 결론을 내지 않는다 · {s}'))

    # 3) 출처 개수
    # 출처는 URL로만 적히지 않는다(기관명·법령명으로 적힌 묶음도 있다 — 2026-09-23 확인)
    # 출처가 'proshares.com/...' 처럼 http 없이 적힌 묶음이 많다(2026-09-23 확인) → 맨 도메인도 센다
    urls = len(set(re.findall(r'https?://\S+', facts))) + len(set(re.findall(r'\b[a-z0-9-]+\.(?:com|org|net|go\.kr|or\.kr|co\.kr|gov)\b/?\S*', facts)))
    # 2026-09-25: 정식 명칭('국토교통부')이 약칭('국토부')에 안 걸려 출처를 다 적고도 '기관 0곳'이 떴다.
    # 정식 명칭과 약칭을 같이 센다. 같은 기관을 두 꼴로 적어도 set 이 하나로 접는다.
    ORG = (r'국토교통부|국토부|한국부동산원|한국은행|국세청|금융감독원|금융위원회|한국거래소|예금보험공사|'
           r'통계청|보건복지부|고용노동부|기획재정부|행정안전부|국민연금|건강보험공단|근로복지공단|공공데이터포털|'
           r'SEC|EDGAR|Nasdaq|NYSE|FRED|연준|은행연합회|생명보험협회|손해보험협회|'
           r'ProShares|Yahoo|Vanguard|Invesco|Schwab|JPMorgan|BlackRock|미래에셋|삼성자산|삼성자산운용|법령|공시')
    orgs = len({m.replace('국토교통부', '국토부') for m in re.findall(ORG, facts, re.I)})
    if urls + orgs < 3: problems.append(('출처', 0, f'출처가 URL {urls}개 + 기관 {orgs}곳뿐 — 최소 3개'))

    # 4) 주제축 이름
    # 2026-09-25: 규격 밖 축은 pick.py 가 발행 뒤에야 알려 줬고, 그동안 그 묶음은 축 상한에서 빠져
    # 하루 6편 제한이 헐거워졌다. 발행 전에 도는 이 검사에서 먼저 잡는다.
    try:
        import axisname
        ax = os.path.join(pkg, 'axis.txt')
        raw = open(ax, encoding='utf-8').read().strip() if os.path.exists(ax) else ''
        if not raw:
            problems.append(('축', 0, 'pkg/axis.txt 가 없거나 비었다 — pick.py 축 상한에서 빠진다'))
        elif axisname.off_spec(raw):
            problems.append(('축', 0, f'축 이름 "{raw}"가 규격 밖 — {"|".join(axisname.CANON)} 중 하나로 고치거나 '
                                     f'axisname.ALIAS 에 접는 규칙을 넣는다'))
    except Exception as e:
        problems.append(('축', 0, f'축 이름 검사 실패: {e}'))

    out = [f'# 자체 검증 (제미나이 할당량 없을 때 쓰는 대체 검증)',
           f'# 묶음: {os.path.basename(os.path.dirname(pkg))} · 종류: {kind} · 문장 {n}개 · 기준 출처: cafe_style/benchmark_2026-09-23.md', '']
    if not problems: out.append('지적 없음')
    for tag, i, msg in problems:
        out.append(f'[{tag}] {("문장 " + str(i)) if i else "전체"} — {msg}')
    open(os.path.join(pkg, 'check_self.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')

    # 검산 지적은 사실 지적과 같이 센다 — 되돌아온 값이 틀린 글은 발행하면 안 된다.
    fact_n = sum(1 for t, _, _ in problems if t in ('사실', '표본', '검산'))
    calc_n = sum(1 for t, _, _ in problems if t == '계산')
    recalc_n = sum(1 for t, _, _ in problems if t == '검산')
    tone_n = sum(1 for t, _, _ in problems if t == '말투')
    print(f'[자체 검증] {os.path.basename(os.path.dirname(pkg))} · {kind} · 문장 {n}개')
    print(f'  사실 지적 {fact_n}건(검산 {recalc_n}건 포함) · 계산 확인 {calc_n}건 · 말투 지적 {tone_n}건 · 출처 {urls+orgs}개')
    for tag, i, msg in problems[:20]: print(f'  [{tag}] {("문장 "+str(i)) if i else "전체"} — {msg[:110]}')
    if len(problems) > 20: print(f'  … 외 {len(problems)-20}건 (check_self.txt)')
    print('  →', os.path.join(pkg, 'check_self.txt'))
    return 1 if fact_n else 0

if __name__ == '__main__':
    sys.exit(main(resolve_pkg(sys.argv[1])))
