import json, os, sys, statistics as st, random, datetime, math
sys.stdout.reconfigure(encoding='utf-8')
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S); import sst
rows = json.load(open(os.path.join(S, 'views.json'), encoding='utf-8'))
now = datetime.datetime.now(datetime.timezone.utc)
def pub(r):
    d = datetime.datetime.fromisoformat(r['publishAt'].replace('Z', '+00:00'))
    return d if d.tzinfo else d.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
rows = [r for r in rows if r.get('priv') == 'public' and r['views'] is not None and pub(r) <= now - datetime.timedelta(hours=48)]
rows.sort(key=pub)
print('공개 48h+ 쇼츠', len(rows))
# 1. 연속 순서별
pos = {}; prev = None; k = 0; seq = []
for r in rows:
    k = k + 1 if r['layout'] == prev else 1; prev = r['layout']; seq.append(k)
    if r['layout'] in ('c1clip', 'm1clip', 'c2person'): pos.setdefault(min(k, 5), []).append(r['views'])
for p in sorted(pos): print(f'  클립 틀 연속 {p}{"+" if p==5 else ""}번째: n={len(pos[p])} 중앙 {st.median(pos[p]):,.0f}')
clip = [(s, r['views']) for s, r in zip(seq, rows) if r['layout'] in ('c1clip', 'm1clip', 'c2person')]
print('  연속 순서 vs 조회 순위상관', round(sst.spearman([a for a, _ in clip], [b for _, b in clip]), 3), 'n=', len(clip))
# c1clip 각 연속 구간
print('  c1clip 연속 구간:')
run = []
for s, r in zip(seq, rows):
    if r['layout'] == 'c1clip':
        if s == 1 and run: print('   ', run); run = []
        run.append(r['views'])
print('   ', run)
for lay in ('c1clip', 'm1clip', 'c2person', 'bars', 'rank', 'cards'):
    v = [r['views'] for r in rows if r['layout'] == lay]
    if v: print(f'  {lay}: n={len(v)} 중앙 {st.median(v):,.0f} 최소 {min(v)} 최대 {max(v)}')
# 2. 우리 채널 신호 사후 검증
tab = [[0, 0], [0, 0]]
for i in range(20, len(rows)):
    lay = rows[i]['layout']; prior = rows[:i]
    lv = [r['views'] for r in prior if r['layout'] == lay][-3:]
    if len(lv) < 3: continue
    cm = st.median([r['views'] for r in prior[-20:]]); s = st.median(lv) < cm; o = rows[i]['views'] < cm
    tab[s][o] += 1
print('우리 신호 사후:', tab, '쉼 뒤 아래', f'{tab[1][1]}/{sum(tab[1])}', '아님 뒤 아래', f'{tab[0][1]}/{sum(tab[0])}', 'Fisher p=', round(sst.fisher(tab), 3))
# 3. 구조: 틀과 무관(라벨 무작위)일 때 쉼 확률
last20 = [r['views'] for r in rows[-20:]]; cm = st.median(last20)
pool = [r['views'] for r in rows if r['layout'] in ('c1clip', 'm1clip', 'c2person')]
random.seed(1); N = 100000
one = sum(st.median(random.sample(pool, 3)) < cm for _ in range(N)) / N
allp = sum(all(st.median(random.sample(pool, 3)) < cm for _ in range(3)) for _ in range(N)) / N
print(f'틀 무관 가정: 채널 20편 중앙 {cm:,.0f} · 클립 쇼츠 {len(pool)}편에서 3편 뽑아 쉼 확률 {one:.1%} · 세 틀 모두 쉼 {allp:.1%}')
# 중앙 3편의 흔들림
meds = sorted(st.median(random.sample(pool, 3)) for _ in range(N))
print(f'3편 중앙 95% 범위 {meds[int(.025*N)]:,.0f}~{meds[int(.975*N)]:,.0f} · 20편 중앙 95%', end=' ')
m20 = sorted(st.median(random.sample(pool, 20)) for _ in range(20000)); print(f'{m20[500]:,.0f}~{m20[19500]:,.0f}')
# 틀끼리 차이: 순열검정 c1clip vs m1clip 중앙 차
a = [r['views'] for r in rows if r['layout'] == 'c1clip']; b = [r['views'] for r in rows if r['layout'] == 'm1clip']; c = [r['views'] for r in rows if r['layout'] == 'c2person']
obs = st.median(a) - st.median(b); ab = a + b; cnt = 0
for _ in range(20000):
    random.shuffle(ab); cnt += abs(st.median(ab[:len(a)]) - st.median(ab[len(a):])) >= abs(obs)
print(f'c1clip {st.median(a):,.0f}(n={len(a)}) vs m1clip {st.median(b):,.0f}(n={len(b)}) 순열 p={cnt/20000:.3f}')
print('클립 시절 조회 변동계수', round(st.pstdev(pool) / st.mean(pool), 2), '사분위', [round(x) for x in st.quantiles(pool, n=4)])
