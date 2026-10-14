# P-1 화면 재료 — script.md(장·말 줄·[자막]) + voice.json(줄 길이·소리) + calc_out.txt·facts.txt + motion_preview/p1_step.json·p1_stock.json → work/video/p1.json (Remotion P1이 읽는다)
#   py -3.12 work/research/longform/ep/P-1/p1props.py
# 장면은 줄 번호가 아니라 '그 장에서 이 말이 처음 나오는 줄'(ANCHOR)로 자른다(h1props와 같은 방식, 10/13 PD).
# 장면 길이 = 목소리 길이(voice.json frames). 목소리 없는 줄은 5.65음절/초 어림 + missing으로 센다(렌더는 missing 0일 때만).
# 숫자: 화면 글자 숫자는 calc_out.txt·facts.txt·script.md 자막 문구 그대로(need로 기계 대조). 누적 선·막대 위치는 calc_out 월액·나이에서 계산.
# 실사 장 머리(1·4·5·6장): 그 장 첫 말 줄 위에 StockShot을 덮는다(dur = 그 줄 길이, 8초 이하 assert). 5장은 StepCliff(p1_step.json, beats = 5장 15줄 시작) 그대로.
import json, os, re, sys
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
    for s in ss: assert s in CALC or s in FACTS or s in SCRIPT, f'calc_out·facts·대본 자막에 없는 글: {s}'

# ───────── 숫자(calc_out 파싱) ─────────
m = re.search(r'1969년생 제때 65세 \| 조기 60세 월 ([\d,]+)원 \| 연기 70세 월 ([\d,]+)원 \| 조기=제때 같아지는 나이 ([\d.]+)세 \| 제때=연기 ([\d.]+)세', CALC)
E_AMT, D_AMT, X_E, X_D = int(m.group(1).replace(',', '')) / 10000, int(m.group(2).replace(',', '')) / 10000, float(m.group(3)), float(m.group(4))
assert (E_AMT, D_AMT, X_E, X_D) == (70, 136, 76.67, 83.89)
YEARS = []
for n, e, xe, d, xd in re.findall(r'(\d)년 당김 월 ([\d,]+)원 → 제때와 같아지는 나이 ([\d.]+)세 \| \d년 미룸 월 ([\d,]+)원 → 같아지는 나이 ([\d.]+)세', CALC):
    YEARS.append([int(n), e, xe, d, xd])
assert len(YEARS) == 5 and YEARS[0][2] == '80.67' and YEARS[0][4] == '79.89'
m64 = re.search(r'1964년생 제때 63세 .*?조기=제때 같아지는 나이 ([\d.]+)세 \| 제때=연기 ([\d.]+)세', CALC); assert m64.groups() == ('74.67', '81.89')
LIFE = {}
for sex, age, a, b, c, d1, d2 in re.findall(r'(남|여) ([\d.]+)세까지: 조기 ([\d,]+)원 · 제때 ([\d,]+)원 · 연기 ([\d,]+)원 · 제때-조기 \+([\d,]+)원 · 연기-제때 \+([\d,]+)원', CALC):
    LIFE[sex] = [float(age)] + [int(x.replace(',', '')) for x in (a, b, c, d1, d2)]
assert LIFE['남'][0] == 84.5 and LIFE['여'][0] == 88.7
need('19.5년', '23.7년', '84.5세', '88.7세', '0.6년', '2억 580만원', '2억 3,400만원', '2억 3,664만원', '2억 4,108만원', '2억 8,440만원', '3억 518만원',
     '2,820만원', '264만원', '2,078만원', '4,332만원', '445억원', '10만 명', '60만원', '410만원', '4만 5,500원', '308만 9,062원', '508만 9,062원',
     '1968년 12월 31일생', '1969년 1월 1일생', '1953~56', '1957~60', '1961~64', '1965~68', '1969~', '100만원', '70만원', '136만원', '6%', '7.2%',
     '제61조②', '제63조의2', '2026-06-17', '법률 제21203호', '법률 제8541호', '519만원', '15만원', '68세', '발제안', '법 개정 아님')
for won, man in [(LIFE['남'][1], '2억 580만원'), (LIFE['남'][2], '2억 3,400만원'), (LIFE['남'][3], '2억 3,664만원'), (LIFE['여'][1], '2억 4,108만원'),
                 (LIFE['여'][2], '2억 8,440만원'), (LIFE['여'][3], '3억 518만원'), (LIFE['남'][4], '2,820만원'), (LIFE['남'][5], '264만원'), (LIFE['여'][5], '2,078만원')]:
    eok, rest = divmod(won // 10000, 10000)
    assert man.replace(',', '') == ((f'{eok}억 ' if eok else '') + f'{rest}만원').replace(',', ''), (won, man)

def cum(start, amt, age): return max(0.0, (age - start) * 12 * amt)   # 만원, 받기 시작한 나이부터 쌓인 돈(월 100만원 가정)
for start, amt, sex, idx in [(60, 70, '남', 1), (65, 100, '남', 2), (70, 136, '남', 3), (60, 70, '여', 1), (65, 100, '여', 2), (70, 136, '여', 3)]:
    assert abs(cum(start, amt, LIFE[sex][0]) * 10000 - LIFE[sex][idx]) < 1, (start, sex)
CURVE = [[a, round(cum(60, 70, a)), round(cum(65, 100, a)), round(cum(70, 136, a))] for a in range(60, 91)]

STEP = json.load(open(os.path.join(EP, 'motion_preview', 'p1_step.json'), encoding='utf-8'))
STOCK = {s['chapter']: s for s in json.load(open(os.path.join(EP, 'motion_preview', 'p1_stock.json'), encoding='utf-8'))['shots']}

SRC_LAW = '국민연금법 제61조②·제62조②·제63조②(국가법령정보센터) · 파이어맵 계산(월 100만원 가정)'
SRC_AGE = '국민연금법 부칙(법률 제8541호) 제8조 · 국민연금공단 노령연금 안내'
SRC_LIFE = 'KOSIS 간이생명표 2024(국가데이터처) · 파이어맵 계산(월 100만원 가정, 65세까지 산 사람 기준)'
SRC_MOHW = '보건복지부 보도자료(개선된 노령연금 감액제도 본격 시행) · 국민연금법 부칙(법률 제21203호) 제2조'
SRC_68 = '국회 토론회 발제안(자료집 원문 미확인) · 국민연금법 부칙(법률 제8541호) 제8조'

# ───────── 장면 규칙: (키, 종류, 장, 이 말이 처음 나오는 줄 — None = 장 첫 줄) ─────────
RULES = [
    ('teaser', 'teaser', '0.', None), ('concl', 'concl', '결론부터', None),
    ('birth', 'birth', '1.', None), ('stairs', 'stairs', '1.', ('네 해 묶음',)), ('person', 'person', '1.', ('오늘 계산은',)),
    ('board', 'board', '2.', None),
    ('cross', 'cross', '3.', None), ('years', 'years', '3.', ('조금만 당기거나',)),
    ('life', 'life', '4.', None), ('race', 'race', '4.', ('평균 나이까지',)),
    ('step', 'step', '5.', None),
    ('refund', 'refund', '6.', None),
    ('stamp', 'stamp', '7.', None),
    ('sum', 'sum', '마무리', None),
]
CH_NAME = {'0.': None, '결론부터': None, '1.': '1장', '2.': '2장', '3.': '3장', '4.': '4장', '5.': '5장', '6.': '6장', '7.': '7장', '마무리': None}
CH_TITLE = {}
END_MIN = 20 * FPS


def spec(key, lines):
    has = lambda w: next((i for i, t in enumerate(lines) if w in t), -1)
    if key == 'teaser':
        cards = [['step', '519만원 넘으면', '15만원부터 깎임', '연금 월 100만원 가정'], ['cross', '1년 당김 80.67세', '5년 당김 76.67세', '따라잡히는 나이'],
                 ['bars', '남 84.5세', '여 88.7세', '65세 기대여명 · 평균일 뿐'], ['refund', '445억원', '약 10만 명 · 신청 없이 환급', '복지부 발표 그대로'],
                 ['stamp', '68세', '법 개정 아님', '국회 토론회 발제안'], ['ask', '당김 60 · 제때 65 · 미룸 70', '몇 살을 넘기면?', '']]
        return '본편에서', None, None, {'cards': cards}
    if key == 'concl':
        return '결론부터', '누구에게나 맞는 나이는 없다 · 앞서는 나이는 숫자로 나온다', SRC_LAW, {
            'cells': [['당김', '60세'], ['제때', '65세'], ['미룸', '70세']], 'q': '?', 'stair': '519만원 위 계단', 'chip': '국민연금법 제63조의2 · 2026-06-17 시행'}
    if key == 'birth':
        return CH_TITLE['1.'], '하루 차이 생일 · 받기 시작하는 나이', SRC_AGE, {
            'cards': [['1968.12.31', '1965~68년생', '64세'], ['1969.1.1', '1969년생부터', '65세']], 'band': '하루'}
    if key == 'stairs':
        return '네 해 묶음마다 한 살씩', '출생연도별 노령연금 받기 시작하는 나이', SRC_AGE, {
            'rows': [['1953~56', '61세'], ['1957~60', '62세'], ['1961~64', '63세'], ['1965~68', '64세'], ['1969~', '65세']], 'mine': '내 칸 찾기'}
    if key == 'person':
        return '오늘 계산은 1969년생', '가상 인물로 계산 · 실제 사람 아님', SRC_AGE, {
            'name': '69년생 연금 씨', 'tag': '가상 인물', 'bill': ['65세부터', '월 100만원', '(가정)'], 'first': '65세로 늦춰진 첫 해',
            'same': '조기·연기 비율은 출생연도와 상관없이 같음'}
    if key == 'board':
        return CH_TITLE['2.'], '65세 월 100만원 가정 · 당김 5년·미룸 5년', SRC_LAW, {
            'cells': [['당김', '60세부터', '70만원', '한 해 −6%'], ['제때', '65세부터', '100만원', '가정'], ['미룸', '70세부터', '136만원', '한 해 +7.2%']],
            'speed': [['깎이는 속도', 6, '한 해 6%'], ['붙는 속도', 7.2, '한 해 7.2%']],
            'warn': '조심', 'rule': ['당겨 받기 조건', '소득이 있는 업무에 종사하지 아니하는 경우', '국민연금법 제61조②'],
            'dep': '부양가족연금액엔 비율 안 붙음',
            'at': [has('매달 100만원'), has('70만원'), has('6%'), has('136만원'), has('7.2%'), has('붙는 속도'), has('조심'), has('일정 기준'), has('부양가족')]}
    if key == 'cross':
        return CH_TITLE['3.'], '받은 돈을 쌓아 보면 · 월 100만원 가정', SRC_LAW, {
            'curve': CURVE, 'xe': X_E, 'xd': X_D, 'names': ['당김(60세·70만원)', '제때(65세·100만원)', '미룸(70세·136만원)'],
            'flags': ['76.67세', '83.89세'], 'at': [0, has('처음엔'), has('따라잡아요'), has('77세'), has('84세')]}
    if key == 'years':
        rows = [[f'{n}년', f'{int(e.replace(",", "")) // 10000}만원' if int(e.replace(',', '')) % 10000 == 0 else e + '원', f'{xe}세',
                 (f'{int(d.replace(",", "")) // 10000}만 {int(d.replace(",", "")) % 10000 // 1000}천원' if int(d.replace(',', '')) % 10000 else f'{int(d.replace(",", "")) // 10000}만원'), f'{xd}세']
                for n, e, xe, d, xd in YEARS]
        for r in rows: need(r[2], r[4])
        need('94만원', '107만 2천원')
        return '조금만 당기거나 미루면', '1969년생 · 제때 65세 월 100만원 가정 · 같아지는 나이', SRC_LAW, {
            'cols': ['기간', '당김 월액', '따라잡히는 나이', '미룸 월액', '앞서는 나이'], 'rows': rows, 'b64': ['1964년생(제때 63세)', '5년 당김 74.67세', '5년 미룸 81.89세'],
            'at': [0, has('1년만 당기면'), has('1년만 미루면'), has('오래 당길수록'), has('이른 해')]}
    if key == 'life':
        return CH_TITLE['4.'], '65세 기대여명 · 평균일 뿐, 개인 수명 예측 아님', SRC_LIFE, {
            'bars': [['남', 84.5, '84.5세', '19.5년 더'], ['여', 88.7, '88.7세', '23.7년 더']], 'ticks': [[X_E, '76.67세', '당김이 따라잡힘'], [X_D, '83.89세', '미룸이 앞섬']],
            'gap': '0.6년', 'at': [0, has('남자는'), has('여자는'), has('당긴 쪽'), has('미룬 쪽'), has('아슬아슬')]}
    if key == 'race':
        man = lambda w: f'{w // 100000000}억 {w % 100000000 // 10000:,}만원' if w % 100000000 else f'{w // 100000000}억원'
        rows = lambda s: [['당김', LIFE[s][1], man(LIFE[s][1])], ['제때', LIFE[s][2], man(LIFE[s][2])], ['미룸', LIFE[s][3], man(LIFE[s][3])]]
        for s in ('남', '여'):
            for r in rows(s): need(r[2])
        return '평균 나이까지 쌓으면', '1969년생 · 월 100만원 가정 · 65세까지 산 사람 기준', SRC_LIFE, {
            'm': rows('남'), 'w': rows('여'), 'mAge': '84.5세까지(남 평균)', 'wAge': '88.7세까지(여 평균)',
            'chips': ['제때 − 당김 2,820만원', '미룸 − 제때 264만원', '미룸 − 제때 2,078만원'],
            'arrow': ['오래 받을수록 → 미룸', '일찍 끝날수록 → 당김'], 'ans': '답은 평균에 있지 않다', 'two': ['내 건강', '그 사이에 쓸 다른 돈'],
            'at': [0, has('2,800만원'), has('264만원'), has('여자 평균'), has('2,000만원'), has('오래 받을수록'), has('답은'), has('내 건강')]}
    if key == 'step':
        return STEP['scene']['title'], STEP['scene']['sub'], STEP['scene']['source'], {'step': STEP['step']}
    if key == 'refund':
        return CH_TITLE['6.'], '바뀐 기준은 2025년 소득부터 적용 · 보건복지부 발표', SRC_MOHW, {
            'law': '부칙(법률 제21203호) 제2조 · 2025년 1월 1일 이후 소득부터',
            'who': ['2025년 소득분으로 깎였던 사람', '308만 9,062원 초과 ~ 508만 9,062원 미만'], 'stamp': '신청 없이 7월 말부터',
            'big': ['445억원', '약 10만 명'], 'avg': ['1인 평균', '약 60만원'], 'ex': ['복지부 예시', '64세 · 월소득 410만원', '1구간 감액 4만 5,500원 → 중단'],
            'at': [0, has('안 깎일'), has('7월 말'), has('445억'), has('60만원'), has('410만원')]}
    if key == 'stamp':
        return CH_TITLE['7.'], '받는 나이 68세 이야기 · 지금 법과 비교', SRC_68, {
            'big': '68세', 'tag': '국회 토론회 발제안', 'stamp': '법 개정 아님', 'now': ['지금 법', '1969년생부터 65세'], 'at': [0, has('토론회'), has('법이 바뀐'), has('지금 법')]}
    if key == 'sum':
        return '정리', '1969년생 · 월 100만원 가정', SRC_LAW + ' · 제63조의2', {
            'cells': [['당김 5년', '76.67세', '따라잡힘'], ['미룸 5년', '83.89세', '앞섬']], 'line': ['공제 뒤', '519만원', '이 선'], 'stair': ['선 위', '15만원부터', '계단'],
            'kb': ['연금도', '건강보험료 계산에 들어가요'],
            'd1': {'img': 'p1_d1thumb.png', 'tag': '앞서 올린 편', 'title': '퇴직 후 건강보험료', 'q': '피부양자로 남을 수 있는지'},
            'link': ['설명란 파이어맵 글', 'firemap.kr/guide/national-pension-early', '표와 계산 근거'],
            'ask': {'q': '당기실 건가요, 미루실 건가요?', 'cells': [['당김', '60세'], ['제때', '65세'], ['미룸', '70세']], 'tail': '이유도 댓글로'},
            'at': [0, has('피부양자'), has('설명란'), has('댓글')]}
    raise KeyError(key)


def script_lines(path):
    """script.md → {장 키: [(말, 자막|None)]}. 장 키는 '1.'처럼 번호, 번호 없는 장은 '[결론부터]' → '결론부터'."""
    out, cur, last = {}, None, None
    for line in open(path, encoding='utf-8').read().split('\n---', 1)[0].splitlines():
        if line.startswith('## '):
            t = line[3:].strip(); cur = re.sub(r'^\[', '', t).split()[0].rstrip(']'); out[cur] = []; last = None
            mm = re.match(r'(\d+)\. (.+)$', t)
            if mm: CH_TITLE[mm.group(1) + '.'] = mm.group(2).strip()
        elif cur is not None and line.lstrip().startswith('- '):
            t = re.sub(r'\s*\(화면.*$', '', line.strip()[2:]).strip(); t = re.sub(r'\s*\[자막:.*?\]', '', t).strip()
            if t: out[cur].append([t, None]); last = out[cur][-1]
        elif cur is not None and line.strip().startswith('[자막:') and last is not None:
            last[1] = line.strip()[4:].rstrip(']').strip()
    return out


def main():
    sl = script_lines(os.path.join(EP, 'script.md'))
    voice = {}
    for s in json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8')).get('sections', []):
        for l in s['lines']:
            if l.get('audio'): voice.setdefault(l['text'], l)
    scenes, warn = [], []
    for ch in ['0.', '결론부터', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '마무리']:
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
            frames = sum(x['frames'] for x in out)
            sc = {'key': key, 'kind': kind, 'title': title, 'sub': sub, 'source': src, 'chapter': CH_NAME[ch], 'data': data, 'lines': out, 'frames': frames}
            if j == 0 and CH_NAME[ch] in STOCK:
                shot = dict(STOCK[CH_NAME[ch]]); assert shot['title'] == CH_TITLE[ch], (shot['title'], CH_TITLE[ch])
                shot['dur'] = out[0]['frames']; assert shot['dur'] <= 8 * FPS, (ch, shot['dur'])
                shot['chipAt'] = min(shot.get('chipAt', 43), shot['dur'] - 30)
                sc['stock'] = shot
            scenes.append(sc)
    st = next(s for s in scenes if s['key'] == 'step')
    beats, a = [], 0
    for l in st['lines']: beats.append(a); a += l['frames']
    assert beats == STEP['step']['beats'], 'p1_step.json beats가 지금 녹음 길이와 다름 — motion_preview/stepprops.py 다시'
    scenes[-1]['frames'] = max(scenes[-1]['frames'], END_MIN)
    missing = sum(1 for s in scenes for l in s['lines'] if not l['audio'])
    nlines = sum(len(v) for v in sl.values())
    res = {'fps': FPS, 'scenes': scenes, 'missing': missing}
    json.dump(res, open(os.path.join(VID, 'p1.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    tot = sum(s['frames'] for s in scenes) / FPS
    for w in warn: print('경고 ·', w)
    print(f'장면 {len(scenes)} · 말 줄 {nlines} · 길이 {int(tot // 60)}:{tot % 60:04.1f} · 목소리 없는 줄 {missing} · 그림 종류 {len({s["kind"] for s in scenes}) + 1}(실사 포함) {sorted({s["kind"] for s in scenes})}')
    t = 0
    for i, s in enumerate(scenes):
        print(f"  {i:2} {int(t // 60)}:{t % 60:04.1f} {s['key']:8} {s['frames'] / FPS:5.1f}초 줄{len(s['lines']):2} {'[실사]' if s.get('stock') else ''} {s['title']}")
        t += s['frames'] / FPS
    return res


if __name__ == '__main__':
    main()
