# spxyield1128 그림 — 00 표지(SPY 1년 배당수익률 1994~2026 선), 01 주가·배당금 늘어난 배(10·20·30년), 02 해마다 배당 합(줄어든 해 주황).
# 숫자는 raw/SPY.json(야후, 11/25 종가까지)에서 calc.py와 같은 셈으로 다시 뽑는다 — 발행 회차가 fetch.py 다시 돌리면 이 파일만 다시 돌리면 됨.
import os, json, glob, datetime as dt
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG = '#111827', '#6B7280', '#EA580C'
BG = '#0F3B3A'
def load(t):
    j = json.load(open(f'raw/{t}.json', encoding='utf-8'))['chart']['result'][0]
    px = [(dt.datetime.utcfromtimestamp(a).date(), b) for a, b in zip(j['timestamp'], j['indicators']['quote'][0]['close']) if b]
    dv = sorted((dt.datetime.utcfromtimestamp(int(v['date'])).date(), v['amount']) for v in j['events']['dividends'].values())
    return px, dv
def ttm(dv, d): return sum(a for x, a in dv if d - dt.timedelta(days=365) < x <= d)
px, dv = load('SPY')
me = {}
for d, c in px: me[(d.year, d.month)] = (d, c)
rows = [(d, ttm(dv, d) / c * 100) for k, (d, c) in sorted(me.items()) if d >= px[0][0] + dt.timedelta(days=366)]
last = px[-1]; cur = ttm(dv, last[0]) / last[1] * 100
rows[-1] = (last[0], cur)
ES = last[0].strftime('%Y.%m.%d')
SRC = f'야후 파이낸스 SPY 일별 종가·배당({ES}까지) · 스테이트스트리트 SPY 상품 정보 · 파이어맵 계산'
low_share = (sum(1 for _, y in rows if y < cur - 1e-9) + 1) / len(rows) * 100
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.865, 'S&P500 배당률 33년', fontproperties=Bs(50), color='white')
fig.text(0.07, 0.79, f'지금 {cur:.2f}% · {len(rows)}달 가운데 낮은 쪽 {low_share:.0f}%', fontproperties=Bs(30), color='#A7F3D0')
ax = fig.add_axes([0.1, 0.2, 0.84, 0.52]); ax.set_facecolor(BG)
xs = [r[0] for r in rows]; ys = [r[1] for r in rows]
ax.plot(xs, ys, color='#CBD5E1', lw=2.2)
mn = min(rows, key=lambda r: r[1]); mx = max(rows, key=lambda r: r[1])
for (d, y), lab, va, dy in ((mn, f'2000년 8월\n{mn[1]:.2f}%', 'top', -0.18), (mx, f'2009년 2월\n{mx[1]:.2f}%', 'bottom', 0.12)):
    ax.scatter([d], [y], s=60, color='white', zorder=3)
    ax.text(d, y + dy, lab, ha='center', va=va, fontproperties=Bs(20), color='white', linespacing=1.15)
ax.scatter([last[0]], [cur], s=160, color=ORG, zorder=4)
ax.plot([last[0], last[0]], [cur + 0.12, cur + 1.9], color=ORG, lw=2)
ax.text(last[0], cur + 1.95, f'지금\n{cur:.2f}%', ha='right', va='bottom', fontproperties=Bs(30), color=ORG, linespacing=1.1)
ax.set_ylim(0.2, 4.3); ax.set_yticks([1, 2, 3, 4]); ax.set_yticklabels(['1%', '2%', '3%', '4%'], fontsize=16, color='#A7F3D0')
ax.tick_params(axis='x', colors='#A7F3D0', labelsize=16); ax.tick_params(length=0)
for s_ in ax.spines.values(): s_.set_visible(False)
ax.grid(axis='y', color='#1F5554', lw=1)
fig.text(0.07, 0.085, '배당금은 늘었는데 주가가 더 올라서', fontproperties=Bs(28), color='white')
fig.text(0.07, 0.035, f'{ES} 종가 · SPY 지난 1년 배당 ÷ 주가 · 달마다 마지막 날', fontsize=17, color='#A7F3D0')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': f'야후 파이낸스 chart API SPY 일별 종가·배당 events(11/27 받음)로 1994-01~{last[0]} 달마다 지난 1년 배당수익률 직접 계산, calc_out.txt · 지금 값은 스테이트스트리트 SPY 분배수익률 1.06%와 같음',
           'made_at': str(dt.date.today()), 'by': 'research/spxyield1128/mkimg.py', 'out': 'img/00.png', 'topic': 'S&P500 배당률 33년',
           'num': f'지금 {cur:.2f}% · 2000년 8월 {mn[1]:.2f}% · 2009년 2월 {mx[1]:.2f}%', 'topic_px': 50, 'num_px': 30,
           'follows': '경쟁 2 donview 표지(S&P500 수익률 글자 카드) + 경쟁 5 hwakseye1(댓글 76) 첫 줄 SPY 분배율 숫자 + hidiv1128 큰 숫자 차트'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 주가 vs 배당금 늘어난 배
G = []
for yrs in (10, 20, 30):
    dd = last[0] - dt.timedelta(days=round(365.25 * yrs)); old = [r for r in px if r[0] <= dd][-1]
    G.append((f'{yrs}년 전부터\n({old[0].year}년 {old[0].month}월)', last[1] / old[1], ttm(dv, last[0]) / ttm(dv, old[0])))
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
x = np.arange(3); w = 0.36
ax.bar(x - w / 2, [g[1] for g in G], w, color='#334155')
ax.bar(x + w / 2, [g[2] for g in G], w, color=ORG)
for i, g in enumerate(G):
    ax.text(i - w / 2, g[1] + 0.15, f'주가\n{g[1]:.1f}배', ha='center', va='bottom', fontproperties=Bs(15), color=INK, linespacing=1.1)
    ax.text(i + w / 2, g[2] + 0.15, f'배당금\n{g[2]:.1f}배', ha='center', va='bottom', fontproperties=Bs(15), color=ORG, linespacing=1.1)
ax.set_xticks(x); ax.set_xticklabels([g[0] for g in G], fontproperties=Bs(15)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(0, 11.8)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
frame(fig, '배당금도 늘었지만 주가가 더 많이 올랐어요', f'SPY 기준 · 지금({ES}) 대비 배수 · 그래서 배당률(배당금 ÷ 주가)이 내려감')
fig.subplots_adjust(top=0.82, bottom=0.17, left=0.04, right=0.96); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 해마다 배당 합 1994~2025, 줄어든 해 주황
ys_ = {}
for d, a in dv: ys_[d.year] = ys_.get(d.year, 0) + a
Y = list(range(1994, 2026)); V = [ys_[y] for y in Y]
down = {y for i, y in enumerate(Y) if i and V[i] < V[i - 1]}
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.bar(Y, V, 0.75, color=[ORG if y in down else '#334155' for y in Y])
for y in sorted(down):
    i = Y.index(y); ax.text(y, max(V[max(0, i - 1):i + 2]) + 0.15, f'{y}\n{(V[i] / V[i - 1] - 1) * 100:.0f}%', ha='center', va='bottom', fontproperties=Bs(14), color=ORG, linespacing=1.1)
ax.text(2025, V[-1] + 0.15, f'{V[-1]:.2f}달러', ha='center', va='bottom', fontproperties=Bs(14), color=INK)
ax.text(1995, V[0] + 0.15, f'{V[0]:.2f}달러', ha='center', va='bottom', fontproperties=Bs(14), color=INK)
ax.set_yticks([]); ax.set_ylim(0, 8.6); ax.tick_params(axis='x', labelsize=13, length=0)
ax.set_xticks([1994, 2000, 2005, 2010, 2015, 2020, 2025])
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
frame(fig, '해마다 받은 배당 합 — 줄어든 해는 세 번', 'SPY 1주 기준 · 배당락일이 그해에 든 배당을 더함 · 1994~2025년')
fig.subplots_adjust(top=0.82, bottom=0.09, left=0.04, right=0.96); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'spxyield1128' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok', [(g[0].split(chr(10))[0], round(g[1], 2), round(g[2], 2)) for g in G], round(low_share, 1))
