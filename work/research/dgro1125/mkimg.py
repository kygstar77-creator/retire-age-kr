# dgro1125 그림 — 00 표지(분기 배당 38번 중 4번 감소), 01 1년 배당 2017~2025, 02 1만 달러 10년. 숫자는 raw·calc_out.txt 그대로
import os, json, datetime as D
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, NAVY, GRY = '#111827', '#6B7280', '#EA580C', '#1E3A5F', '#94A3B8'
SRC = '아이셰어즈 DGRO 배당 기록 · 야후 파이낸스 일별 종가·배당(11/23 받음) · 파이어맵 계산'
r = json.load(open('raw/DGRO.json'))['chart']['result'][0]
dv = sorted((D.datetime.fromtimestamp(int(k), D.UTC).date(), v['amount']) for k, v in r['events']['dividends'].items())
q = {}
for a, v in dv:
    if a >= D.date(2016, 6, 1): q[(a.year, (a.month - 1) // 3)] = q.get((a.year, (a.month - 1) // 3), 0) + v
keys = [k for k in sorted(q) if k >= (2017, 1)]
BG = '#3B1F5C'; TOPIC_PX, NUM_PX = 58, 44
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, 'DGRO 배당금', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.785, '1년 전 같은 분기보다 줄어든 때', fontproperties=Bs(27), color='#E9D5FF')
ax = fig.add_axes([0.08, 0.2, 0.86, 0.5]); ax.set_facecolor(BG)
for i, k in enumerate(keys):
    down = (k[0] - 1, k[1]) in q and q[k] < q[(k[0] - 1, k[1])]
    ax.bar(i, q[k], 0.75, color=ORG if down else '#8B7BAA')
ax.text(0, 0.47, '38번 중 4번', fontproperties=Bs(NUM_PX), color='#FDBA74')
ax.text(0, 0.425, '주황 = 1년 전보다 적게 나온 분기', fontproperties=Bs(17), color='#E9D5FF')
for y in (2017, 2020, 2023, 2026):
    i = [j for j, k in enumerate(keys) if k[0] == y][0]; ax.text(i, -0.03, str(y), fontproperties=Bs(17), color='white', va='top')
ax.set_ylim(-0.06, 0.5); ax.axis('off')
fig.text(0.07, 0.07, '1주당 분기 배당(달러) · 2017년 2분기~2026년 3분기', fontsize=17, color='#E9D5FF')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '아이셰어즈 DGRO 배당 기록·야후 파이낸스 chart API DGRO 배당 events(11/23 받음)로 직접 계산, calc_out.txt',
           'made_at': '2026-11-23', 'by': 'research/dgro1125/mkimg.py', 'out': 'img/00.png', 'topic': 'DGRO 배당금', 'num': '38번 중 4번',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 3 real_bin/224465288342 상품명 큰 글자 표지 + vig1125 차트형 표지'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK); fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
ann = {}
for a, v in dv: ann[a.year] = ann.get(a.year, 0) + v
ys = list(range(2017, 2026))
fig = plt.figure(figsize=(9, 6), dpi=100); fig.patch.set_facecolor('white')
frame(fig, 'DGRO 1년 배당, 2017~2025년', '1주당 1년 동안 받은 배당 합(달러) · 한 해도 줄지 않음')
ax = fig.add_axes([0.08, 0.12, 0.88, 0.7])
b = ax.bar([str(y) for y in ys], [ann[y] for y in ys], color=[ORG if y in (2017, 2025) else NAVY for y in ys])
for x, y in zip(b, ys): ax.text(x.get_x() + x.get_width() / 2, ann[y] + 0.02, f'{ann[y]:.3f}', ha='center', fontsize=12, color=INK)
ax.spines[['top', 'right', 'left']].set_visible(False); ax.set_yticks([]); ax.tick_params(labelsize=12)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
v = [('DGRO', 37828), ('SCHD', 37511), ('VIG', 36823), ('SPY', 39422)]
fig = plt.figure(figsize=(9, 6), dpi=100); fig.patch.set_facecolor('white')
frame(fig, '1만 달러, 11년 뒤', '2015.11.20에 넣고 배당은 다시 샀다면 · 2026.11.20 종가 기준(달러, 세전)')
ax = fig.add_axes([0.08, 0.12, 0.88, 0.7])
b = ax.bar([n for n, _ in v], [x for _, x in v], color=[ORG, NAVY, NAVY, GRY])
for x, (n, val) in zip(b, v): ax.text(x.get_x() + x.get_width() / 2, val + 500, f'약 {round(val, -2):,.0f}', ha='center', fontsize=14, color=INK)
ax.axhline(10000, color=SUBC, lw=1, ls='--'); ax.text(-0.55, 10600, '넣은 돈 1만 달러', fontsize=11, color='white', ha='left', zorder=5)
ax.spines[['top', 'right', 'left']].set_visible(False); ax.set_yticks([]); ax.tick_params(labelsize=14)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
