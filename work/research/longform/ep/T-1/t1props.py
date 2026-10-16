# T-1 화면 재료 — script.md(장·말 줄·[자막]) + voice.json(줄 길이·소리) + calc_out.txt·facts.txt → work/video/t1.json (Remotion T1이 읽는다)
#   py -3.12 work/research/longform/ep/T-1/t1props.py
# p1props와 같은 방식(10/16 PD): 장면은 '그 장에서 이 말이 처음 나오는 줄'(ANCHOR)로 자르고, 장면 길이 = 목소리 길이.
# 숫자: 화면 글자 숫자는 calc_out.txt(사례 A~E·정부 사례①~④)에서 파싱하거나 script.md 자막 문구 그대로(need로 기계 대조).
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

# ───────── 숫자(calc_out 파싱): 사례 → {해: (공제율, 지방세 포함 만원)} ─────────
CASE = {}
for blk in re.split(r'\n(?===)', CALC):
    m = re.match(r'== (\S+)', blk)
    if not m: continue
    rows = re.findall(r'(\d{4}): 공제율 (\d+)% .*?\(지방세 포함 ([\d,]+)만원\)', blk)
    if rows: CASE[m.group(1)] = {int(y): (int(r), int(t.replace(',', ''))) for y, r, t in rows}
B, C, A, D, E = CASE['B'], CASE['C'], CASE['A'], CASE['D'], CASE['E']
assert (C[2026][1], C[2029][1], B[2026][1], B[2027][1], B[2028][1], B[2029][1]) == (1901, 1241, 8135, 8135, 11398, 14777)
assert (B[2027][0], B[2028][0], B[2029][0], C[2029][0]) == (48, 32, 16, 80)

def man(v):   # 만원 → '1억 4,777만원' / '8,135만원'
    e, r = divmod(v, 10000)
    return (f'{e}억 {r:,}만원' if r else f'{e}억원') if e else f'{r:,}만원'
for v in (1901, 1241, 8135, 11398, 14777, 6234, 13536, 3263, 3379, 6642, 414, 73, 10765, 18157, 23651, 29195):
    need(man(v))
assert B[2026][1] - C[2026][1] == 6234 and B[2029][1] - C[2029][1] == 13536
assert B[2028][1] - B[2027][1] == 3263 and B[2029][1] - B[2028][1] == 3379
assert round(B[2029][1] / C[2029][1], 1) == 11.9
G = re.findall(r'(\d{4}): 공제율 \d+% 공제 [\d.]+억 과표 [\d.]+억 기본공제 \S+ 산출 ([\d,]+)만원 \(지방세 포함 [\d,]+만원\) \| 정부 ([\d.]+)억', CALC)
assert len(G) == 6, G
GOV = [[y, f'{int(s.replace(",", "")) / 10000:.2f}억', f'{g}억'] for y, s, g in G]
for y, ours, g in GOV: assert ours == g, (y, ours, g)    # 파이어맵 = 정부(억 둘째 자리)
need('2.36억·3.20억·4.05억', '3.16억·9.23억·13.73억', '3.84억', '250만원 → 2,500만원', '11.9배', '1,284만원 → 744만원', '약 1,280만원 → 약 740만원')

SRC_LAW = '소득세법 §89·95·103(국가법령정보센터) · 파이어맵 계산(지방세 포함·필요경비 0)'
SRC_GOV = '재정경제부 2026 세법개정안 상세본 p.57~60 · 9.1 보도자료 · 파이어맵 계산(지방세 포함)'
SRC_QA = '재정경제부 세법개정안 문답 자료 p.37~38·49 · 파이어맵 계산'
SRC_CUT = '정부안 소득세법 §103 단서(상세본 p.68) · 파이어맵 계산(지방세 포함)'
NOTE = '정부안 기준 · 국회 통과 전'

RULES = [
    ('duel', 'duel', '0.', None),
    ('price', 'price', '1.', None),
    ('ladder', 'ladder', '2.', None), ('taxcard', 'taxcard', '2.', ('올해 판다면',)),
    ('rates', 'rates', '3.', None), ('climb', 'climb', '3.', ('한 해 늦게',)),
    ('basic', 'basic', '4.', None), ('ratio', 'ratio', '4.', ('열두 배 가까이',)),
    ('five', 'five', '5.', None),
    ('verify', 'verify', '6.', None), ('cap', 'cap', '6.', ('공제에 한도가',)),
    ('excluded', 'excluded', '7.', None),
    ('calendar', 'calendar', '8.', None), ('ask', 'ask', '8.', ('여러분 집은',)),
]
CH_NAME = {'0.': None, **{f'{i}.': f'{i}장' for i in range(1, 9)}}
CH_TITLE = {}
END_MIN = 20 * FPS


def spec(key, lines):
    has = lambda w: next((i for i, t in enumerate(lines) if w in t), -1)
    J, S = '정민 씨', '수현 씨'
    if key == 'duel':
        return '같은 집, 같은 값', '2029년에 판다면 · ' + NOTE, SRC_GOV, {
            'price': '20억', 'who': [[J, '10년 삶', man(C[2029][1])], [S, '2년 삶', man(B[2029][1])]], 'times': '열두 배 가까이',
            'gov': ['세법 개정안', '9.1 국무회의 의결', '국회 통과 전'], 'fake': '가상 인물 · 계산용',
            'years': [[y, B[y][1], C[y][1]] for y in (2026, 2027, 2028, 2029)], 'gap': [man(6234), man(13536)], 'q': '왜?',
            'at': [0, has('살았던 햇수'), has('국무회의'), has('가상 인물'), has('올해 팔면'), has('2029년엔'), has('왜')]}
    if key == 'price':
        return CH_TITLE['1.'], '집 한 채 · 비과세 요건 갖춘 경우', '소득세법 §89①3 · 시행령 §160① · 파이어맵 계산(필요경비 0)', {
            'sell': '판 값 20억', 'line': '12억', 'free': '12억까지 0원', 'over': '넘는 몫 8억', 'buy': '산 값 8억', 'gain': '번 돈 12억',
            'pct': '40%', 'taxed': '4.8억', 'taxedSay': '5억이 조금 안 됨',
            'at': [0, has('넘으면'), has('20억짜리'), has('8억에 샀으니'), has('40%'), has('같은 비율'), has('5억이')]}
    if key == 'ladder':
        return CH_TITLE['2.'], '지금 법 · 장기보유특별공제', '소득세법 §95② 표2 · 시행령 §159의4', {
            'rows': [['갖고 있던 해', '해마다 4%'], ['실제로 살았던 해', '해마다 4%']], 'J': [10, 10, '80%'], 'S': [10, 2, '48%'],
            'at': [0, has('갖고 있던 해마다'), has('살았던 해마다'), has('내내'), has('80%'), has('2년뿐'), has('48%')]}
    if key == 'taxcard':
        return '올해(2026년) 판다면', '지방세 포함 · 필요경비 0', SRC_LAW, {
            'J': [J, '80%', man(C[2026][1])], 'S': [S, '48%', man(B[2026][1])], 'cut': '정부안: 둘 중 하나를 없앰',
            'at': [0, has('8,100만원'), has('정부안은')]}
    if key == 'rates':
        return CH_TITLE['3.'], '정부안 공제율 · 2028.1.1 이후 판 집부터', '재정경제부 2026 세법개정안 상세본 p.58', {
            'cols': ['2027년까지', '2028년', '2029년부터'], 'rows': [['살았던 해', '4%', '6%', '8%'], ['갖고 있던 해', '4%', '2%', '없음']],
            'J': [J, '80%', '80%', '80%'], 'S': [S, f'{B[2027][0]}%', f'{B[2028][0]}%', f'{B[2029][0]}%'],
            'at': [0, has('6%로'), has('2%로'), has('아예 안'), has('80% 그대로'), has('16%만')]}
    if key == 'climb':
        return '수현 씨 세금, 해마다 계단', '집도 값도 그대로 · ' + NOTE, SRC_GOV, {
            'bars': [[y, B[y][1], man(B[y][1])] for y in (2027, 2028, 2029)], 'steps': ['+' + man(3263), '+' + man(3379)], 'same': '집 그대로 · 값 그대로 · 규칙만 바뀜',
            'at': [0, has('규칙만')]}
    if key == 'basic':
        return CH_TITLE['4.'], '정부안 · 2027.1.1 이후 판 집부터', SRC_CUT, {
            'from': '250만원', 'to': '2,500만원', 'x': '열 배', 'conds': ['10년 이상 산 집', '집 한 채', '30억 이하에 팔 때'],
            'J': [man(C[2026][1]), man(C[2027][1])],
            'at': [0, has('하나 더'), has('열 배'), has('1,240만원')]}
    if key == 'ratio':
        return '2029년, 열두 배 가까이', '지방세 포함 · ' + NOTE, SRC_GOV, {
            'bars': [[S, B[2029][1], man(B[2029][1])], [J, C[2029][1], man(C[2029][1])]], 'times': '11.9배',
            'why': ['공제율 16% vs 80%', '기본공제 250만 vs 2,500만']}
    if key == 'five':
        rows = [['A', '15억 · 10년 보유 · 10년 삶', A], ['수현', '20억 · 10년 보유 · 2년 삶', B], ['정민', '20억 · 10년 보유 · 10년 삶', C],
                ['D', '25억 · 5년 보유 · 5년 삶', D], ['E', '30억 · 15년 보유 · 5년 삶', E]]
        return CH_TITLE['5.'], '지방세 포함 · 필요경비 0 · ' + NOTE, SRC_GOV, {
            'cols': ['2026', '2027', '2028', '2029'], 'rows': [[n, d, [man(c[y][1]) for y in (2026, 2027, 2028, 2029)]] for n, d, c in rows],
            'tags': ['', '5분의 1도 안 됨', '언제 팔아도 같음', '60% 넘게 늘어남', '보유 − 거주 햇수 차이'],
            'at': [0, has('5분의 1'), has('5년씩'), has('해마다 같'), has('반대로'), has('60%'), has('몇 년 차이')]}
    if key == 'verify':
        return CH_TITLE['6.'], '정부 문답 자료 사례 · 산출세액(지방세 빼고)', SRC_QA, {
            'cases': [['사례 1', '32억 · 10년 보유 · 2년 삶', GOV[:3]], ['사례 2', '75억 · 10년 보유 · 10년 삶', GOV[3:]]], 'heads': ['파는 해', '정부', '파이어맵'],
            'jump': '마지막 해 네 배 넘게',
            'at': [0, has('사례 두 개'), has('32억'), has('똑같이'), has('75억'), has('네 배')]}
    if key == 'cap':
        return '공제에 한도가 생긴다', '정부안 소득세법 §95⑥ 신설', '재정경제부 2026 세법개정안 상세본 p.60 · 파이어맵 계산', {
            'caps': [['2028년', 20, '20억'], ['2029년부터', 10, '10억']], 'mine': ['정민 씨 공제', 3.84, '3.84억'], 'safe': '한도에 안 걸림',
            'at': [0, has('4억이')]}
    if key == 'excluded':
        return CH_TITLE['7.'], '이 영상 계산 밖 · ' + NOTE, '소득세법 §95② 표1 · 정부안 조특법 §71의3(상세본 p.69)', {
            'cards': [['2년 못 산 집 한 채', '지금은 일반 공제(연 2%)', '정부 표에 없음 → 숫자 안 냄'],
                      ['만 65세 이상 · 비수도권 이사', '정부안 감면 특례 따로', '2027년 50% · 2028년 30%'],
                      ['취득세 · 중개수수료', '번 돈에서 빼지 않고 계산', '실제 세금은 더 적을 수 있음']],
            'stamp': '국회 심사에서 바뀔 수 있음',
            'at': [0, has('2년을 못'), has('따로 없어서'), has('65살'), has('취득세'), has('적게'), has('국회 심사')]}
    if key == 'calendar':
        return CH_TITLE['8.'], '보유·거주 모두 10년 이하일 때', '재정경제부 2026 세법개정안 상세본 p.58 · 파이어맵 계산', {
            'rows': [['갖고 있던 해', 10], ['살았던 해', 2]], 'per': '한 해 차이마다 −4%', 'S': ['수현 씨', '8년 차이', '−32%p', '48% → 16%'],
            'at': [0, has('10년을 넘지'), has('16%')]}
    if key == 'ask':
        return '내 집이라면?', '갖고 있던 햇수 − 살았던 햇수', SRC_GOV, {
            'q': '몇 년 차이 나나요?', 'cells': [['갖고 있던 해', '□ 년'], ['살았던 해', '□ 년']], 'tail': '댓글로 남겨 주세요',
            'sum': [['정민 씨', '0년 차이', man(C[2029][1])], ['수현 씨', '8년 차이', man(B[2029][1])]], 'note': NOTE}
    raise KeyError(key)


def script_lines(path):
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
            c = line.strip()[4:].rstrip(']').strip()
            last[1] = (last[1] + ' · ' + c) if last[1] else c
    return out


def main():
    sl = script_lines(os.path.join(EP, 'script.md'))
    voice = {}
    for s in json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8')).get('sections', []):
        for l in s['lines']:
            if l.get('audio'): voice.setdefault(l['text'], l)
    scenes, warn = [], []
    for ch in ['0.'] + [f'{i}.' for i in range(1, 9)]:
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
            frames = sum(x['frames'] for x in out)
            scenes.append({'key': key, 'kind': kind, 'title': title, 'sub': sub, 'source': src, 'chapter': CH_NAME[ch], 'data': data, 'lines': out, 'frames': frames})
    scenes[-1]['frames'] = max(scenes[-1]['frames'], END_MIN)
    missing = sum(1 for s in scenes for l in s['lines'] if not l['audio'])
    nlines = sum(len(v) for v in sl.values())
    res = {'fps': FPS, 'scenes': scenes, 'missing': missing}
    json.dump(res, open(os.path.join(VID, 't1.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    tot = sum(s['frames'] for s in scenes) / FPS
    for w in warn: print('경고 ·', w)
    print(f'장면 {len(scenes)} · 말 줄 {nlines} · 길이 {int(tot // 60)}:{tot % 60:04.1f} · 목소리 없는 줄 {missing} · 그림 종류 {len({s["kind"] for s in scenes})}')
    t = 0
    for i, s in enumerate(scenes):
        print(f"  {i:2} {int(t // 60)}:{t % 60:04.1f} {s['key']:9} {s['frames'] / FPS:5.1f}초 줄{len(s['lines']):2} {s['title']}")
        t += s['frames'] / FPS
    return res


if __name__ == '__main__':
    main()
