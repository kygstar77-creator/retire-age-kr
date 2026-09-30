# 대본이 사람이 말한 것처럼 들리는지 — 잘되는 사람 채널의 실제 말(받아쓰기)과 숫자로 견준다(2026-09-30).
#   py -3.12 work/humanlike.py <대본 파일(.md/.txt)>            → 기준(사람 채널 받아쓰기)과 다른 점 목록
#   py -3.12 work/humanlike.py --ref                            → 기준 통계만
# 사장님 2026-09-30: "대본도 사람이 쓴 것처럼 AI 티가 안 나야 하는데 이것도 계속 개선하는 루프 돌리는 거지?
#                    어떤 AI 도구를 써야 사람이 쓴 것처럼 하는지도? AI도 계속 발전하고 있어"
# 기준: work/research/longform/breakdown/*_transcript.txt (ytbreak.py가 쌓는 잘된 영상 받아쓰기 — 쌓일수록 기준이 넓어진다).
# 재는 것(말투의 모양만, 내용은 안 본다):
#   문장 길이(음절) 분포 · 문장 끝 모양 비율(~요/~죠/~거든요/~는데요/~습니다/~다) · 질문 비율
#   AI 글에 잘 나오는 말(아래 AI_TELLS) 빈도 · 같은 연결어 반복 · 같은 끝맺음 연속
# 판정은 기계가 하지 않는다 — 차이를 보여 주고, 고칠지는 대본 쓰는 쪽이 판단한다(readcheck.py와 같은 원칙).
import sys, os, re, glob, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, 'research', 'longform', 'breakdown')

# AI가 쓴 한국어 대본에 자주 보이는 표현(사람 채널 받아쓰기엔 드물다 — --ref로 실제 빈도를 확인하고 늘려 간다)
AI_TELLS = ['결론적으로', '요약하자면', '다양한', '중요한 점은', '살펴보겠습니다', '알아보겠습니다', '라고 할 수 있습니다',
            '것으로 보입니다', '측면에서', '에 있어서', '를 통해', '뿐만 아니라', '또한', '이처럼', '한편', '즉,',
            '매우 중요', '핵심은', '주목할 만한', '눈여겨볼', '도움이 되셨길', '여러분의 투자', '현명한', '신중한 판단',
            '인 셈이죠', '셈입니다', '짚어 보겠습니다', '결론부터 말씀드리면', '라는 점을 확인했습니다', '에 해당합니다']  # 10/1 editor: write 금지 목록에서 옮김
ENDS = [('거든요', r'거든요[.?!]?$'), ('죠', r'죠[.?!]?$'), ('는데요', r'(는|은|인)데요[.?!]?$'), ('네요', r'네요[.?!]?$'),
        ('요(그 밖)', r'요[.?!]?$'), ('습니다', r'(습|ㅂ)니다[.?!]?$|니다[.?!]?$'), ('다(평서)', r'다[.!]?$'), ('까?', r'까\?$')]

def sentences(text):
    text = re.sub(r'\[\d+:\d+(:\d+)?\]', ' ', text)                          # [분:초]
    text = re.sub(r'^\s*[-#>|*].*?$', lambda m: m.group(0).lstrip('-#>|* '), text, flags=re.M)
    text = re.sub(r'\([^)]*화면[^)]*\)', ' ', text)
    parts = re.split(r'(?<=[.?!])\s+|\n+', text)
    return [p.strip() for p in parts if len(re.sub(r'[^가-힣]', '', p)) >= 4]

def stats(sents):
    syl = [len(re.sub(r'[^가-힣0-9]', '', s)) for s in sents]
    ends = collections.Counter()
    for s in sents:
        for name, pat in ENDS:
            if re.search(pat, s): ends[name] += 1; break
        else: ends['기타'] += 1
    n = len(sents) or 1
    joined = ' '.join(sents)
    tells = {w: joined.count(w) for w in AI_TELLS if joined.count(w)}
    conn = collections.Counter(re.findall(r'^(그리고|그런데|그래서|하지만|또|이제|자,|다만|반면)', ' \n'.join(sents), flags=re.M))
    run = best = 1
    prev = None
    for s in sents:
        e = next((nm for nm, pat in ENDS if re.search(pat, s)), '기타')
        run = run + 1 if e == prev else 1; best = max(best, run); prev = e
    return {'n': len(sents), 'len_med': st.median(syl) if syl else 0, 'len_p90': sorted(syl)[int(len(syl) * 0.9)] if syl else 0,
            'ends': {k: round(v / n * 100, 1) for k, v in ends.items()}, 'q': round(sum(s.endswith('?') for s in sents) / n * 100, 1),
            'tells_per100': round(sum(tells.values()) / n * 100, 1), 'tells': tells, 'same_end_run': best, 'conn': dict(conn)}

def ref_stats():
    fs = glob.glob(os.path.join(REF, '*_transcript.txt')) + glob.glob(os.path.join(REF, '*_break.md'))
    sents = []
    for f in fs:
        t = open(f, encoding='utf-8').read()
        if f.endswith('_break.md'):
            if '## 받아쓰기' not in t: continue
            t = t.split('## 받아쓰기', 1)[1]
        sents += sentences(t)
    return stats(sents), len(fs)

if __name__ == '__main__':
    ref, nf = ref_stats()
    if len(sys.argv) < 2 or sys.argv[1] == '--ref':
        print(f'기준: 사람 채널 받아쓰기 {nf}개 · 문장 {ref["n"]}'); print(ref); sys.exit()
    me = stats(sentences(open(sys.argv[1], encoding='utf-8').read()))
    print(f'기준(사람 채널 받아쓰기 {nf}개, 문장 {ref["n"]}) vs 이 대본(문장 {me["n"]})')
    print(f'  문장 길이 중앙: 기준 {ref["len_med"]} · 우리 {me["len_med"]}  (상위 10%: {ref["len_p90"]} · {me["len_p90"]})')
    print(f'  질문 문장 비율: 기준 {ref["q"]}% · 우리 {me["q"]}%')
    print('  문장 끝 모양(%):')
    for k in sorted(set(ref['ends']) | set(me['ends'])): print(f'    {k:8} 기준 {ref["ends"].get(k, 0):5} · 우리 {me["ends"].get(k, 0):5}')
    print(f'  AI 티 나는 말 100문장당: 기준 {ref["tells_per100"]} · 우리 {me["tells_per100"]}  {me["tells"]}')
    print(f'  같은 끝맺음 최장 연속: 기준 {ref["same_end_run"]} · 우리 {me["same_end_run"]}')
    flags = []
    if me['len_med'] > ref['len_med'] * 1.35: flags.append('문장이 사람 채널보다 길다 — 쪼갠다')
    if me['tells_per100'] > max(2, ref['tells_per100'] * 2): flags.append('AI 티 나는 말이 많다 — ' + ', '.join(me['tells']))
    if me['same_end_run'] >= 5: flags.append('같은 끝맺음이 5번 넘게 이어진다 — 섞는다')
    for k in ('습니다', '다(평서)'):
        if me['ends'].get(k, 0) > ref['ends'].get(k, 0) + 20: flags.append(f'"{k}" 끝이 사람 채널보다 20%p 넘게 많다 — 말하듯 바꾼다')
    print('\n고칠 곳:' if flags else '\n눈에 띄는 차이 없음'); [print('  -', f) for f in flags]
