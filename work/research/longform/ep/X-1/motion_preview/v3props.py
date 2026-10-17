# X-1 대본 v3(10/17) 새 장면 세 개 props (2026-10-17 motion)
#   hedge = 질문 2 '같은 1억 막대 두 개'(HedgeFlip) · even = 질문 1 '본전 환율'(EvenLadder) · below = 질문 5 '지금보다 쌌던 날'(DaysBelow)
# 숫자 글자는 calc_out·script(말·자막)에 있는 것만(assert). 선·점 = raw/collect_20261016.json(ECOS 일별·KRX 종가) 그대로.
# 길이: ep/X-1/voice.json에 같은 문장이 있으면 그 녹음 프레임, 없으면 P-1 녹음 속도(spf) 어림 — v3 녹음 뒤 다시 돌린다.
#   py -3.12 work/research/longform/ep/X-1/motion_preview/v3props.py → x1_v3.json
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H); WORK = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
script = os.path.join(EP, 'script.md'); txt = open(script, encoding='utf-8').read()
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
SRC = txt + calc
def has(*ws):
    for w in ws: assert w in SRC, w
secs = SC.parse(script)
caps, last = {}, None
for line in txt.splitlines():
    s = line.strip()
    if s.startswith('- '): last = s[2:].strip()
    elif s.startswith('[자막:') and last and last not in caps: caps[last] = s[4:].rstrip(']').strip()
voice = {}
vj = os.path.join(EP, 'voice.json')
if os.path.exists(vj):
    for s in json.load(open(vj, encoding='utf-8')).get('sections', []):
        for l in s['lines']:
            if l.get('audio'): voice[l['text']] = l
SPF = json.load(open(os.path.join(EP, '..', 'P-1', 'motion_preview', 'p1_timing.json'), encoding='utf-8'))['spf']
def cut(sec, a, b):
    s = next(x for x in secs if x['title'].startswith(sec))['lines']
    i = next(k for k, t in enumerate(s) if t.startswith(a)); j = next(k for k, t in enumerate(s) if t.startswith(b))
    out = []
    for t in s[i:j + 1]:
        v = voice.get(t)
        out.append({'text': t, 'cap': caps.get(t), 'frames': v['frames'] if v else max(12, round(SC.syl(SC.speak(t)) / SPF)), 'audio': v['audio'] if v else None})
    return out
def scene(key, title, sub, chapter, source, lines, data):
    has(title)
    return {'key': key, 'title': title, 'sub': sub, 'chapter': chapter, 'source': source, 'lines': lines, 'frames': sum(l['frames'] for l in lines) + 12, 'data': data}
raw = json.load(open(os.path.join(EP, 'raw', 'collect_20261016.json'), encoding='utf-8'))

# 8·9줄 작은 환율 선: 2024.1.2~2026.10.15 일별 원문 3일 간격(끝날 포함)
_u = [v for d, v in json.load(open(os.path.join(EP, 'raw', 'collect_20261016.json'), encoding='utf-8'))['USD'] if '20240102' <= d <= '20261015']
assert round(_u[0]) == 1289 and round(max(_u)) == 1554 and round(_u[-1]) == 1339
fx24 = _u[::3] + ([_u[-1]] if (len(_u) - 1) % 3 else []); fx24pk = fx24.index(max(fx24))
# ── 1. 질문 2: 환노출 vs (H) — 날짜 순 세 쌍, 말 순서(7.2 → 1년 전 → 재작년 첫날)로 켜짐
L = cut('2.', '달러가 제일 비쌌던 날 1억을', '환율을 막아 두면')
assert len(L) == 12, [l['text'] for l in L]
pairs = [  # 날짜, 이름, 환노출 원, %, 환헤지 원, %, 차 말
 ('2024.1.2', '재작년 첫날', 175678252, '+75.68%', 160354815, '+60.35%', '환노출형이 1,500만원 넘게 더'),
 ('2025.10.13', '1년 전', 112402588, '+12.40%', 116528815, '+16.53%', 'H형이 400만원 넘게 더'),
 ('2026.7.2', '달러 가장 비싸던 날', 89583254, '−10.42%', 103805193, '+3.81%', '차 1,400만원 넘게'),
]
for d, n, a, ap, b, bp, gap in pairs:
    has(f'{a:,}원', f'{b:,}원', ap.replace('−', '-'), bp)
    assert gap.replace('차 ', '') in txt or gap.replace('차 ', '차이가 ').replace('넘게', '을 넘') in txt.replace('1,400만원을 넘', '1,400만원 을 넘'), gap
has('재작년 첫날', '1년 전', '달러가 제일 비쌌던 날', '1,289원', '9천만원이 조금 안', 'H형은 오히려 1억을 넘었어요',
    '지수가 올라도 환율이 더 내리면 떨어집니다', '그럼 H형이 늘 나을까요?', '결과가 뒤집혀요', '내릴 때 손실도 막지만, 오를 때 이익도 같이 막는', 'KODEX 미국S&P500', '(H)')
hedge = {'seed': 'X-1-hedge', 'pairs': [{'date': d, 'name': n, 'a': a, 'ap': ap, 'b': b, 'bp': bp, 'gap': gap} for d, n, a, ap, b, bp, gap in pairs],
  'order': [2, 1, 0], 'base': 100000000, 'baseText': '넣은 1억', 'nameA': 'KODEX 미국S&P500', 'tagA': '환노출', 'nameB': 'KODEX 미국S&P500(H)', 'tagB': '환헤지',
  'sayA': '9천만원이 조금 안', 'sayB': '1억을 넘었어요', 'why': '지수가 올라도 환율이 더 내리면 떨어집니다', 'ask': '그럼 H형이 늘 나을까요?', 'flip': '결과가 뒤집혀요',
  'rate24': '1,289원', 'rates': ['1,289원', '1,554원', '1,339원'], 'fx24': fx24, 'fx24pk': fx24pk, 'end': '내릴 때 손실도 막지만, 오를 때 이익도 같이 막는다',
  # 말 줄 → 일: 0 7.2 노출 · 1 7.2 헤지 · 2 7.2 차 · 3 1년 전 · 4 답 · 5 이유 띠 · 6 물음 · 7 재작년 · 8 그때 환율 · 9 올랐다 내림 · 10 차(노출 쪽) · 11 끝 띠
}
assert hedge['end'].replace('막는다', '막는') in txt
src2 = '한국은행 ECOS · KRX 종가 2024.1.2·2025.10.13·2026.7.2 → 끝 날짜 2026.10.16 + 분배금(세전·재투자 안 함) · 삼성자산운용'

# ── 2. 질문 1: 본전 환율 — 세로 환율 눈금, 지금 1,339원 점선 위아래로 날짜별 본전 줄
L2 = cut('1.', '그래서 내 계좌는', '지난 석 달 방향이')
assert len(L2) == 12, [l['text'] for l in L2]
evens = [  # 이름, 산 날 환율, 배수, 본전, 말 글자
 ('달러 가장 비싸던 날', '1,554.4', '1.0363', 1500.0, '1,500원'),
 ('석 달 전', '1,507.1', '1.0302', 1462.9, '1,463원'),
 ('올해 첫날', '1,434.9', '1.1297', 1270.1, '1,270원'),
 ('1년 전', '1,420.5', '1.1640', 1220.3, '1,220원'),
]
for n, r, m, e, s in evens:
    has(f'그날 환율 {r} ÷ SPY 배수 {m} = 본전 환율 {e:,.1f}원')
has('1,500원은 돼야 본전', '160원쯤 위', '1,463원이 본전', '1,220원까지 내려가도 아직 본전', '1.16배로 나누면', '본전 환율', '상하방 요인이 병존', '주가가 움직이면 같이 움직입니다')
even = {'seed': 'X-1-even', 'now': 1338.6, 'nowText': '지금 1,339원', 'min': 1150, 'max': 1600,
  'ticks': [[1200, '1,200원'], [1300, '1,300원'], [1400, '1,400원'], [1500, '1,500원'], [1600, '1,600원']],
  'evens': [{'name': n, 'rate': r, 'mult': m, 'even': e, 'say': s} for n, r, m, e, s in evens],
  'show': [None, None, None, None, 0, 0, 1, 3, None, None, None, None],   # 줄마다 켜는 본전 줄(4·5 가장 비싸던 날, 6 석 달 전, 7 1년 전 → 올해 첫날 함께)
  'formula': ['본전 환율', '산 날 환율', '주가 배수'], 'ex': ['1,554.4', '1.0363', '1,500.0'], 'app': ['앱 달러 수익률 16%(1년 전에 산 경우)', '1.16배로 나누면'],
  'gapSay': '160원쯤 위', 'aboveTag': '아직 손실 — 환율이 이만큼 올라야 본전', 'belowTag': '이미 이익 — 여기까지 내려가도 본전',
  'warn': '주가가 움직이면 같이 움직입니다', 'both': '환율의 상하방 요인이 병존', 'end': '지난 석 달 방향이 그대로 이어진다고 보면 틀리기 쉽다'}
assert '지난 석 달 방향이 그대로 이어진다고 보고 계산하면 틀리기 쉽습니다' in txt
has('아직 본전', '본전이에요')
src1 = '한국은행 ECOS · 파이어맵 계산 · 본전 환율 = 산 날 환율 ÷ (2026.10.15 SPY ÷ 산 날 SPY), 주가가 지금 그대로일 때만'

# ── 3. 질문 5: 지금보다 쌌던 날 — 2024.1.2~2026.10.15 선, 지금 높이 가로줄, 줄 아래 날 색칠 → 엔화
L3 = cut('5.', '언제 바꿀지는', '쓸 날이 정해져 있다면')
assert len(L3) == 7, [l['text'] for l in L3]
usd = [(d, v) for d, v in raw['USD'] if '20240102' <= d <= '20261015']
jpy = [(d, v) for d, v in raw['JPY100'] if '20240102' <= d <= '20261015']
assert len(usd) == 679 and len(jpy) == 679 and usd[-1] == ('20261015', 1338.6) and jpy[-1] == ('20261015', 846.65)
nu = sum(v <= 1338.6 for _, v in usd); nj = sum(v <= 846.65 for _, v in jpy)
assert nu == 81 and nj == 4, (nu, nj)
has('679거래일 중 끝날(1,338.6)보다 같거나 낮았던 날 81일 = 11.9%', '679거래일 중 끝날(846.65)보다 같거나 낮았던 날 4일 = 0.6%', '679일', '81일', '여드레에 하루꼴', '4일밖에', '달러는 싼 쪽이고 엔화는 거의 가장 싼 값', '결과가 가운데로 모입니다')
# usdRatio: 대본 '여드레에 하루꼴'(10/17 youtube-loop 고침, 81/679 = 8.4일에 하루) — 화면엔 calc 비율 11.9%만
has('= 11.9%')
yr = [[i, d[:4]] for i, (d, _) in enumerate(usd) if i == 0 or d[:4] != usd[i - 1][0][:4]]
below = {'seed': 'X-1-below', 'usd': [v for _, v in usd], 'jpy': [v for _, v in jpy], 'years': yr,
  'usdMin': 1280, 'usdMax': 1580, 'jpyMin': 820, 'jpyMax': 1030,
  'usdNow': 1338.6, 'jpyNow': 846.65, 'usdNowText': '지금 1,338.6원', 'jpyNowText': '지금 100엔 846.65원',
  'usdName': '원/달러', 'jpyName': '원/100엔', 'noAns': '앞날 환율 — 누구도 정답을 줄 수 없음', 'past': '지나간 날과 견주면',
  'total': '679일', 'usdCount': '81일', 'usdRatio': '11.9%', 'jpyCount': '4일밖에', 'sumUp': ['달러는 싼 쪽', '엔화는 거의 가장 싼 값'], 'mid': '나눠 바꾸면 결과가 가운데로'}
src3 = '한국은행 ECOS 매매기준율 일별 2024.1.2~2026.10.15(679거래일) · 같거나 낮은 날'

# 2024 쌍이 켜지는 7줄부터 [정확한 값] 띠도 2024 값으로(레드팀: 띠와 화면 어긋남) — 같은 대본 [자막] 원문을 앞줄로 당김
assert L[10]['cap'] and '2024.1.2' in L[10]['cap']; L[7]['cap'] = L[10]['cap']
for e in even['evens']: e['evenText'] = f"{e['even']:,.1f}원"
out = {'fps': 30,
 'hedge': scene('hedge', '같은 1억 막대 두 개', '같은 회사 두 상품 · 분배금 포함 · 2026.10.16', '2', src2, L, hedge),
 'even': scene('even', '본전 환율', '산 날 환율 ÷ 주가 배수 · 지금 1,339원과 견주기', '1', src1, L2, even),
 'below': scene('below', '지금보다 쌌던 날', '2024.1.2 ~ 2026.10.15 · 679거래일', '5', src3, L3, below)}
json.dump(out, open(os.path.join(H, 'x1_v3.json'), 'w', encoding='utf-8'), ensure_ascii=False)
for k in ('hedge', 'even', 'below'):
    s = out[k]; print(k, s['frames'], 'f', round(s['frames'] / 30, 1), 's', '녹음 줄', sum(1 for l in s['lines'] if l['audio']), '/', len(s['lines']), '최장 줄', round(max(l['frames'] for l in s['lines']) / 30, 1), 's')
