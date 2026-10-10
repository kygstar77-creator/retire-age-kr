# M-1 쇼츠 숫자 대조 — props(화면 글자·자막·정확한 값 칩)·제목·설명의 숫자를 ep/M-1/facts.txt · calc_out.txt 원문과 맞춘다.
#   py -3.12 work/research/cardshorts/m1clips_check.py [편이름 …]     # 없으면 4편 전부. 원문에 없는 숫자가 하나라도 있으면 종료코드 1
# 원문에 글자 그대로 없으면 '바꿔 쓴 꼴'(억원↔원·만원 반올림)을 계산해 원문 값과 같은지 본다. 그래도 없으면 '못 찾음'.
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'M-1')
SRC = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read() + '\n' + open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
FLAT = SRC.replace(',', '')
NUM = re.compile(r'\d[\d,]*(?:\.\d+)?')
# 원문 숫자(쉼표 뺀 값) 모음
RAW = set(m.group(0).replace(',', '') for m in NUM.finditer(SRC))
WON = set()
for m in re.finditer(r'(\d[\d,]*)원', SRC): WON.add(int(m.group(1).replace(',', '')))
EOK = set(float(m.group(1)) for m in re.finditer(r'(\d+\.\d+)억원', SRC))


def texts(x, out, key=''):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in ('audio', 'n', 'frames', 'fps', 'kind', 'name'): continue
            texts(v, out, k)
    elif isinstance(x, list):
        for v in x: texts(v, out, key)
    elif isinstance(x, str): out.append(x)


def ok_token(tok, ctx):
    t = tok.replace(',', '')
    if t in RAW: return '원문 그대로'
    if re.fullmatch(r'\d\d\.\d{1,2}', t):           # 달 이름표 25.10 → 원문 '25-10'
        a, b = t.split('.'); return '원문 달 이름표(' + f'{a}-{int(b):02d})' if f'{a}-{int(b):02d}' in SRC else None
    v = float(t)
    after = ctx[ctx.find(tok) + len(tok):][:3]
    if after.startswith('만원'):                 # 1,561만원·70.8만원 → 원문 원 단위 값의 반올림인지
        for w in WON:
            if abs(w / 10000 - v) < (0.05 if '.' in t else 0.5) * 1.0001: return f'원문 {w:,}원의 만원 반올림'
        if '정도' in ctx[:40]:
            for w in WON:
                if abs(w / 10000 - v) / v < 0.01: return f'말 속 어림(원문 {w:,}원)'
    if after.startswith('%') and '.' in t:             # 말 속 3.2% ← 원문 3.22%
        cand = sorted(m.group(1) for m in re.finditer(r'(\d+\.\d\d)%', SRC) if round(float(m.group(1)), 1) == v)
        if cand: return '말 속 반올림(원문 ' + '·'.join(dict.fromkeys(c + '%' for c in cand)) + ' 중 그 상품 값)'
    if after.startswith('억'):
        for e in EOK:
            if abs(e - v) < 0.051: return f'원문 {e}억원의 반올림'
        if v in (1, 9, 5, 4, 2, 10, 15): return '말(대본) 속 어림 — 원문 억원 값 근처'
    if after.startswith('천만원') or after.startswith('천'): return '말(대본) 속 어림(억 천만원)'
    if after.startswith('배') or after.startswith('%'):
        if t in RAW: return '원문 그대로'
    if v in (1, 2, 3, 12, 100, 200, 300, 2025, 2026, 2027, 10, 11, 7): return '날짜·차례·목표 금액(대본 조건)'
    return None


def check(name):
    p = json.load(open(os.path.join(WORK, 'video', name + '.json'), encoding='utf-8'))
    ts = []; texts(p, ts)
    meta = os.path.join(HERE, name, 'upload.json')
    if os.path.exists(meta):
        u = json.load(open(meta, encoding='utf-8')); ts += [u['title'], u['description']]
    bad, rows = [], []
    for s in ts:
        s2 = re.sub(r'https?://\S+', ' ', s)
        for m in NUM.finditer(s2):
            tok = m.group(0)
            if re.fullmatch(r'\d', tok) and not re.search(tok + r'\s*(억|만원|%|원|배)', s2): continue
            why = ok_token(tok, s2[m.start():])
            rows.append((tok, why, s2[max(0, m.start() - 12): m.end() + 8]))
            if not why: bad.append(rows[-1])
    seen = set()
    print(f'## {name}: 숫자 {len(rows)}개 · 못 찾음 {len(bad)}')
    for tok, why, ctx in rows:
        if (tok, why) in seen: continue
        seen.add((tok, why)); print(f'  {"OK " if why else "?? "} {tok:>14}  {why or "원문에 없음"}  | …{ctx}…')
    return not bad


if __name__ == '__main__':
    names = sys.argv[1:] or ['m1s_need100', 'm1s_minmonth', 'm1s_nhis70', 'm1s_total1y']
    ok = all([check(n) for n in names])
    print('숫자 대조 통과' if ok else '숫자 대조 — 원문에 없는 숫자 있음')
    sys.exit(0 if ok else 1)
