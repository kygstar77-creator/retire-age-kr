# X-1 화면 재료 — script.md(장·말 줄·[자막]) + voice.json(줄 길이·소리) + calc_out.txt·facts.txt·raw 원문 → work/video/x1.json (Remotion X1이 읽는다)
#   py -3.12 work/research/longform/ep/X-1/x1props.py
# T-1(t1props.py)과 같은 방식(10/16 PD): 장면은 '그 장에서 이 말이 처음 나오는 줄'(ANCHOR)로 자르고, 장면 길이 = 목소리 길이(빠르기 1.0).
# 1·2장은 motion의 FxDates(motion_preview/fxprops.py → x1_fx.json)를 그대로 붙인다. 선·막대 높이는 raw 원문(ECOS·야후)에서, 화면 글자 숫자는 need()로 대조.
import json, os, re, sys, runpy
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
RATE, FPS = 5.65, 30
SCRIPT = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
CALC = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
FACTS = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
def need(*ss):
    for s in ss:
        s2 = s.replace('−', '-')
        assert any(x in src for src in (CALC, FACTS, SCRIPT) for x in (s, s2)), f'calc_out·facts·대본 자막에 없는 글: {s}'
    return ss[0] if len(ss) == 1 else ss
def neg(s): return s.replace('-', '−')   # 화면 빼기표

# ───────── 원문 ─────────
RAW = json.load(open(os.path.join(EP, 'raw', 'ecos_731Y001_20261013.json'), encoding='utf-8'))
YH = json.load(open(os.path.join(EP, 'raw', 'yahoo_spy_qqq_20261013.json'), encoding='utf-8'))
USD = {k: v for k, v in RAW['USD']}; JPY = {k: v for k, v in RAW['JPY100']}
SPY = {d.replace('-', ''): v for d, v in YH['SPY']}
END = '20261012'
assert USD[END] == 1338.0 and JPY[END] == 845.42

# ───────── calc_out 파싱 ─────────
C1 = {m[0]: m for m in re.findall(r'^(\d?\D+?) (\d{4}-\d{2}-\d{2}): 환율 ([\d,.]+) → 달러 ([\d,]+) → ([\d,]+)원 \(([+-][\d,]+)원, ([+-][\d.]+)%\)', CALC, re.M)}
C2 = {(m[0], m[2]): m for m in re.findall(r'^(\d?\D+?) (\d{4}-\d{2}-\d{2}) (SPY|QQQ): 달러 ([+-][\d.]+)% · 환율 ([+-][\d.]+)% · 원화 ([+-][\d.]+)% → 1억 → ([\d,]+)원', CALC, re.M)}
assert len(C1) == 4 and len(C2) == 8, (C1.keys(), C2.keys())
NAMES = [('1년 전', '작년 이맘때', '2025.10.13'), ('올해 첫날', '올해 첫날', '2026.1.2'), ('환율 최고점', '가장 높던 날', '2026.7.2'), ('석 달 전', '석 달 전', '2026.7.13')]
for _, say, _d in NAMES: need(say)

SRC_ETF = 'SPY 종가(야후, 배당 미포함 가격) · 한국은행 ECOS 731Y001 원/달러 매매기준율 · 파이어맵 계산(수수료·세금 없음)'
SRC_FX = '한국은행 ECOS 731Y001 원/달러 매매기준율 일별 · 파이어맵 계산(수수료 없음)'
SRC_BANK = '은행연합회 외환길잡이(환전수수료 안내)'
SRC_HANA = '하나은행 고시 2026.10.12 · 은행연합회 외환길잡이(은행별 수수료율, 2026.8~9 기준) · 파이어맵 계산'
SRC_NOTE = '은행연합회 외환길잡이 · 파이어맵 계산 기준(매매기준율, 수수료·세금·배당 없음)'
SRC_USE = '한국은행 ECOS 731Y001 원/달러·원/100엔 매매기준율 · 파이어맵 계산(카드 수수료 없음)'
SRC_JPY = '한국은행 ECOS 731Y001 원/100엔 매매기준율 일별(2024.1.2~2026.10.12) · 파이어맵 계산(카드 수수료 없음)'
SRC_PREV = "파이어맵 지난 편 '1억, 1년 뒤 남은 돈'(2026.10.14 공개)"
SRC_ALL = 'SPY·QQQ 종가(야후, 배당 미포함) · 한국은행 ECOS 731Y001 매매기준율 · 파이어맵 계산(수수료·세금·배당 없음)'

RULES = [
    ('twoline', 'twoline', '0.', None), ('promise', 'promise', '0.', ('그날 바꾼 1억',)),
    ('why4', 'fxline', '1.', None),
    ('cash', 'fxbars', '2.', None),
    ('wf1', 'wf', '3.', None), ('wf2', 'wf', '3.', ('맨 처음 본 숫자',)), ('two', 'two', '3.', ('두 숫자를',)),
    ('bank', 'bank', '4.', None), ('band', 'band', '4.', ('하나은행 고시로',)), ('note', 'note', '4.', ('증권사에서',)),
    ('seesaw1', 'seesaw', '5.', None), ('cards', 'cards', '5.', ('미국 직구나',)), ('yen', 'yen', '5.', ('엔화도',)), ('seesaw2', 'seesaw', '5.', ('환율이 내린 건 같은데',)),
    ('prev', 'prev', '6.', None), ('table', 'table', '6.', ('언제 바꾸셨나요',)),
]
CH_NAME = {'0.': None, **{f'{i}.': f'{i}장' for i in range(1, 7)}}
END_MIN = 20 * FPS
FX = None   # x1_fx.json(FxDates)


def series(keys, f):
    return [round(f(k), 3) for k in keys]


def wfcol(nm, sym, head):
    m = C2[(nm, sym)]; r, fx, k = float(m[3]), float(m[4]), float(m[5])
    gap = None
    for s, d, w, g in re.findall(r'(SPY|QQQ) ([\d.]+)−\(?(−?[\d.]+)\)?=([\d.]+)', CALC):
        if s == sym and abs(float(d) - r) < 1e-9 and abs(float(w.replace('−', '-')) - k) < 1e-9: gap = g + '%p'
    assert gap is None or abs(float(gap[:-2]) - round(r - k, 2)) < 1e-9
    return {'head': head, 'date': dict((a, c) for a, _, c in NAMES)[nm], 'r': r, 'k': k,
            'rText': neg(need(f'달러 {m[3]}%')), 'kText': neg(need(f'원화 {m[5]}%')),
            'gap': gap, 'won': need(m[6] + '원')}


def spec(key, lines):
    has = lambda w: next((i for i, t in enumerate(lines) if w in t), -1)
    if key == 'twoline':
        keys = sorted(k for k in USD if k in SPY and '20260702' <= k <= END)
        s0, u0 = SPY[keys[0]], USD[keys[0]]
        up = series(keys, lambda k: (SPY[k] / s0 - 1) * 100); dn = series(keys, lambda k: (SPY[k] * USD[k] / (s0 * u0) - 1) * 100)
        m = C2[('환율 최고점', 'SPY')]
        assert round(up[-1], 2) == float(m[3]) and round(dn[-1], 2) == float(m[5]), (up[-1], dn[-1])
        xl = [[0, '7.2']] + [[i, f'{int(k[4:6])}.1'] for i, k in enumerate(keys) if i and k[4:6] != keys[i - 1][4:6]]
        xl[-1:] = xl[-1:] if keys.index(END) - xl[-1][0] > 6 else []
        xl.append([len(keys) - 1, '10.12'])
        return '주가는 올랐는데 원화 계좌는 빠졌다', '같은 S&P500 ETF · 2026.7.2 → 10.12', SRC_ETF, {
            'up': up, 'dn': dn, 'min': -14, 'max': 8, 'yt': [[5, '+5%'], [0, '0%'], [-5, '−5%'], [-10, '−10%']], 'xl': xl,
            'nameUp': 'S&P500 ETF(달러로)', 'nameDn': '같은 투자, 원화 계좌', 'tagUp': need('4% 넘게') + ' ↑', 'tagDn': need('10%') + ' ↓',
            'q': '어디서 새 나갔나?', 'leak': '새 나간 건 환율', 'from': need('1,554원'), 'to': need('1,338원'), 'rateName': '원/달러',
            'at': [0, has('그런데 7월'), has('어디서'), has('새 나간 건')]}
    if key == 'promise':
        return '같은 1억, 바꾼 날마다', '바꾼 날 네 개 · 지금 값은 모두 10월 12일 기준', SRC_FX, {
            'cards': [[say, d] for _, say, d in NAMES], 'base': '1억', 'q': '지금은?', 'qNote': need('지금 값은 모두 10월 12일 기준'), 'otherHead': '끝에는 반대로', 'other': need('덜 쓰게 된 돈'), 'otherSub': '달러를 쓸 사람 쪽',
            'at': [0, has('끝에는')]}
    if key == 'why4':
        return '왜 날짜가 네 개인가', '환율 1년 · 바꾼 날 네 개', FX['src'], FX['fx'] | {'phase': 'line'}
    if key == 'cash':
        return '달러로만 바꿔 뒀다면', '같은 1억, 바꾼 날마다 지금 원화로', FX['src'], FX['fx'] | {'phase': 'bars'}
    if key == 'wf1':
        return '미국 ETF를 샀다면', '작년 이맘때(2025.10.13) 1억으로 산 경우 · 지금 값 10.12', SRC_ETF.replace('SPY 종가', 'SPY·QQQ 종가'), {
            'groups': [wfcol('1년 전', 'SPY', 'S&P500 ETF'), wfcol('1년 전', 'QQQ', '나스닥100 ETF')], 'min': 0, 'max': 25,
            'cols': ['달러로 번 몫', '환율이 깎은 몫', '원화 결과'], 'base': '1억',
            'calls': [[3, 0, need('700만원 가까이') + ' 덜 남음'], [5, 1, need('700만원 넘게') + ' 덜 남음']],
            'show': [1, 4], 'grow': [[1, 2], [5, 5]], 'at': [0, has('17%'), has('10%대'), has('1억으로 치면'), has('나스닥100'), has('여기도')]}
    if key == 'wf2':
        return '가장 높던 날 샀다면', '같은 S&P500 ETF · 바꾼 날만 다름 · 지금 값 10.12', SRC_ETF, {
            'groups': [wfcol('환율 최고점', 'SPY', '가장 높던 날(2026.7.2)'), wfcol('석 달 전', 'SPY', '석 달 전(2026.7.13)')], 'min': -11, 'max': 6,
            'cols': ['달러로 번 몫', '환율이 깎은 몫', '원화 결과'], 'base': '1억',
            'calls': [[1, 0, need('9천만원 아래') + '로'], [2, 1, '석 달 전도 마이너스']], 'first': '맨 처음 본 숫자',
            'show': [0, 2], 'grow': [[0, 0], [2, 2]], 'at': [0, has('9천만원'), has('석 달 전에')]}
    if key == 'two':
        return '주가와 환율, 두 숫자', '원화로 미국 주식을 사면', SRC_ETF, {
            'a': ['주가', '달러로 매긴 값'], 'b': ['환율', '달러 → 원화'], 'eq': '원화 계좌', 'tail': need('두 숫자를 같이 들고 있는 겁니다').replace('겁니다', '것')}
    if key == 'bank':
        return '바꾸는 순간 드는 돈', '은행이 날마다 알리는 기준 환율 = 매매기준율', SRC_BANK, {
            'mid': need('매매기준율'), 'buy': need('현찰 살 때'), 'pricier': '기준보다 비싸게', 'fee': need('환전수수료'), 'pref': need('우대 대상'),
            'counter': '은행 창구', 'at': [0, has('현찰을 살 땐'), has('은행연합회는')]}
    if key == 'band':
        need('1,336.00', '1,359.38', '1,312.62', '+23.38원, 1.75%', '+23,380원', '46,760원', '최대 우대 75~90%')
        return '하나은행 고시로 보면', '2026.10.12 고시 · 달러 현찰', SRC_HANA, {
            'mid': 1336.00, 'buy': 1359.38, 'sell': 1312.62, 'midText': '매매기준율 1,336.00원', 'buyText': '현찰 살 때 1,359.38원', 'sellText': '현찰 팔 때 1,312.62원',
            'pct': '+23.38원 (1.75%)', 'k1': ['천 달러, 우대 없이', need('2만원 넘게') + ' 더', '23,380원'], 'k2': ['사서 바로 팔면', need('5만원 가까이') + ' 사라짐', '46,760원'],
            'k3': ['우대를 받으면', '이 차이가 줄어듦', '최대 우대 75~90%'], 'pref': [0.75, 0.9],
            'at': [0, has('천 달러를'), has('사자마자'), has('우대를 받으면')]}
    if key == 'note':
        t = lines[0]; a = t.index('. ') + 1
        q = SC.syl(SC.speak(t[:a])) / SC.syl(SC.speak(t))
        return '이 영상 계산에 안 들어간 것', '환전 비용', SRC_NOTE, {
            'c1': ['증권사에서 바꾸는 달러도', '우대율에 따라 환전 비용이 붙을 수 있음'], 'c2': ['이 영상 계산', '환전 비용 0원으로 계산'], 'c3': '실제로 남는 돈은 조금 더 적음',
            'mid': q}
    if key in ('seesaw1', 'seesaw2'):
        t = lines[0]; a = t.index('?') + 1 if '?' in t else t.index(', ') + 1
        q = SC.syl(SC.speak(t[:a])) / SC.syl(SC.speak(t))
        return ('반대편 — 덜 쓰게 된 돈' if key == 'seesaw1' else '같은 환율, 반대 결과'), '달러 값이 내리면', SRC_USE, {
            'L': ['달러를 들고 있던 사람', '원화로 바꾸면 줄어듦'], 'R': ['달러를 쓸 사람', '원화로 덜 냄'], 'tagL': '손해', 'tagR': '이득',
            'both': key == 'seesaw2', 'mid': q}
    if key == 'cards':
        need('1,554,400원', '1,338,000원', '−216,400원', '−82,500원', '155만원쯤', '134만원쯤', '20만원 넘게', '8만원쯤')
        return '천 달러를 쓴다면', '미국 직구·여행 · 매매기준율 · 카드 수수료 없음', SRC_USE, {
            'bill': '1,000달러', 'billSub': '직구 · 여행', 'c': [['7월 2일', '가장 높던 날', '155만원쯤'], ['10월 12일', '지금', '134만원쯤']],
            'diff': '20만원 넘게 덜', 'c3': ['작년 이맘때', '2025.10.13 보다', '8만원쯤 덜'],
            'at': [0, has('가장 높던'), has('작년 이맘때')]}
    if key == 'yen':
        keys = sorted(k for k in JPY if '20240102' <= k <= END)
        need('845.42원', '956,320원', '845,420원', '96만원쯤', '85만원쯤', '11만원쯤', '2024년 이후')
        return '엔화도 같이 내려왔다', '원/100엔 매매기준율 · 2024.1 → 2026.10.12', SRC_JPY, {
            'vals': [JPY[k] for k in keys], 'min': 820, 'max': 1040, 'yt': [[850, '850원'], [950, '950원'], [1000, '1,000원']],
            'xl': [[i, k[:4]] for i, k in enumerate(keys) if i == 0 or k[:4] != keys[i - 1][:4]],
            'hi7': keys.index('20260702'), 'name': '원/100엔 매매기준율', 'endText': '10.12 · 845.42원', 'lowTag': '2024년 이후 거의 가장 싼 값', 'jul': '7월 초',
            'k': ['일본에서 쓸 10만엔', '7월 초', '96만원쯤', '지금', '85만원쯤', '11만원쯤 덜'],
            'at': [0, has('10만엔')]}
    if key == 'prev':
        need('예금·S&P500·SCHD·금', "'1억, 1년 뒤 남은 돈'")
        t = lines[0]; a = t.index('죠.') + 2
        q = SC.syl(SC.speak(t[:a])) / SC.syl(SC.speak(t))
        return '지난 편과 이어서', "지난 편 '1억, 1년 뒤 남은 돈'", SRC_PREV, {
            'head': '지난 편에서 비교한 네 곳', 'tiles': [['예금', 0], ['S&P500', 1], ['SCHD', 1], ['금', 1]], 'etf': '미국 ETF', 'cut': '환율이 수익을 깎음', 'now': '이번 편', 'nowBig': '환율만 따로 자세히',
            'q1': 0.3, 'mid': q}
    if key == 'table':
        rows = []
        for nm, say, d in NAMES:
            m1, s, q = C1[nm], C2[(nm, 'SPY')], C2[(nm, 'QQQ')]
            rows.append([say, d, need(m1[2] + '원' if m1[2] + '원' in SCRIPT else m1[2]), neg(need(m1[6] + '%')), neg(need(s[5] + '%')), neg(need(q[5] + '%'))])
        return '바꾼 날 네 개, 한 장으로', '같은 1억 → 10.12 원화로 · 수수료·세금·배당 없음', SRC_ALL, {
            'cols': ['바꾼 날', '그날 환율', '달러로만', 'S&P500 ETF', '나스닥100 ETF'], 'rows': rows, 'endRate': '지금(10.12) ' + need('1,338.0원'),
            'q': '달러, 언제 바꾸셨나요?', 'ask': ['날짜를 댓글로 남겨 주세요', '같은 식으로 계산해 답글 드립니다'], 'cafe': ['전체 표', '고정 댓글 카페 글']}
    raise KeyError(key)


def script_lines(path):
    out, cur, last = {}, None, None
    for line in open(path, encoding='utf-8').read().split('\n---', 1)[0].splitlines():
        if line.startswith('## '):
            t = line[3:].strip(); cur = re.sub(r'^\[', '', t).split()[0].rstrip(']'); out[cur] = []; last = None
        elif cur is not None and line.lstrip().startswith('- '):
            t = re.sub(r'\s*\(화면.*$', '', line.strip()[2:]).strip(); t = re.sub(r'\s*\[자막:.*?\]', '', t).strip()
            if t: out[cur].append([t, None]); last = out[cur][-1]
        elif cur is not None and line.strip().startswith('[자막:') and last is not None:
            c = line.strip()[4:].rstrip(']').strip()
            last[1] = (last[1] + ' · ' + c) if last[1] else c
    return out


def main():
    global FX
    runpy.run_path(os.path.join(EP, 'motion_preview', 'fxprops.py'), run_name='__main__')
    d = json.load(open(os.path.join(EP, 'motion_preview', 'x1_fx.json'), encoding='utf-8'))
    FX = {'fx': d['fx'], 'src': d['s1']['source']}
    sl = script_lines(os.path.join(EP, 'script.md'))
    voice = {}
    for s in json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8')).get('sections', []):
        for l in s['lines']:
            if l.get('audio'):
                assert abs(float(l.get('tempo', 1.0)) - 1.0) < 1e-9, ('빠르기 1.0 아님', l['text'])
                voice.setdefault(l['text'], l)
    scenes, warn = [], []
    for ch in ['0.'] + [f'{i}.' for i in range(1, 7)]:
        lines = sl.get(ch, [])
        assert lines, f'대본에 장 {ch} 없음'
        found = []
        for key, kind, c, anc in RULES:
            if c != ch: continue
            idx = 0 if anc is None else next((i for w in anc for i, (t, _) in enumerate(lines) if w in t), None)
            if idx is None: warn.append(f'{key}: {anc} 못 찾음 — 장면 뺌'); continue
            found.append((idx, key, kind))
        found.sort()
        for j, (idx, key, kind) in enumerate(found):
            part = lines[idx:(found[j + 1][0] if j + 1 < len(found) else None)]
            out = []
            for t, cap in part:
                v = voice.get(t)
                fr = v['frames'] if v else max(12, round(SC.syl(SC.speak(t)) / RATE * FPS))
                out.append({'text': t, 'cap': cap, 'frames': fr, 'audio': v['audio'] if v else None})
            title, sub, src, data = spec(key, [x['text'] for x in out])
            if -1 in data.get('at', []): warn.append(f'{key}: 박자 못 찾음 {data["at"]}')
            if kind in ('fxline', 'fxbars'):   # FxDates 박자(b1·b2)는 이 장면 줄 시작과 같아야 한다
                st, a = [], 0
                for x in out: st.append(a); a += x['frames']
                assert data['b1' if kind == 'fxline' else 'b2'] == st, (key, st)
            frames = sum(x['frames'] for x in out)
            scenes.append({'key': key, 'kind': kind, 'title': title, 'sub': sub, 'source': src, 'chapter': CH_NAME[ch], 'data': data, 'lines': out, 'frames': frames})
    scenes[-1]['frames'] = max(scenes[-1]['frames'], END_MIN)
    missing = sum(1 for s in scenes for l in s['lines'] if not l['audio'])
    nlines = sum(len(v) for v in sl.values())
    assert nlines == 43, nlines
    res = {'fps': FPS, 'scenes': scenes, 'missing': missing}
    json.dump(res, open(os.path.join(VID, 'x1.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    tot = sum(s['frames'] for s in scenes) / FPS
    for w in warn: print('경고 ·', w)
    print(f'장면 {len(scenes)} · 말 줄 {nlines} · 길이 {int(tot // 60)}:{tot % 60:04.1f} · 목소리 없는 줄 {missing} · 그림 종류 {len({s["kind"] for s in scenes})}')
    t = 0
    for i, s in enumerate(scenes):
        mx = max(l['frames'] for l in s['lines']) / FPS
        print(f"  {i:2} {int(t // 60)}:{t % 60:04.1f} {s['key']:8} {s['frames'] / FPS:5.1f}초 줄{len(s['lines']):2} 최장줄 {mx:4.1f}초 {s['title']}")
        t += s['frames'] / FPS
    return res


if __name__ == '__main__':
    main()
