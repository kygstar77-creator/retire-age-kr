# jepivix1127 그림 — 00 표지(앞 달 VIX 20 이상 10.3% vs 15 미만 7.1%), 01 VIX 묶음별 1년 환산 분배율, 02 월 분배금·앞 달 VIX 시간 흐름. 숫자는 calc.py와 같은 raw
import os, json, datetime as D, statistics as S, warnings
warnings.filterwarnings('ignore')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, NAVY, GRY = '#111827', '#6B7280', '#EA580C', '#1E3A5F', '#94A3B8'
CUT = D.date(2026, 11, 24)
SRC = '야후 파이낸스 JEPI 분배 기록·VIX 일별 종가(11/25 받음) · 파이어맵 계산'
def load(t):
    r = json.load(open(f'raw/{t}.json'))['chart']['result'][0]
    ts = [D.datetime.utcfromtimestamp(x).date() for x in r['timestamp']]; q = r['indicators']['quote'][0]['close']
    dv = sorted((D.datetime.utcfromtimestamp(int(k)).date(), v['amount']) for k, v in r.get('events', {}).get('dividends', {}).items())
    n = sum(1 for a in ts if a <= CUT); return ts[:n], q[:n], [x for x in dv if x[0] <= CUT]
ts, c, dv = load('JEPI'); vt, vc, _ = load('VIX'); px = dict(zip(ts, c))
mv = {}
for a, b in zip(vt, vc):
    if b: mv.setdefault((a.year, a.month), []).append(b)
mv = {k: S.mean(v) for k, v in mv.items()}
rows = []
for a, v in dv:
    p = px[max(d for d in ts if d < a)]; pm = (a.year, a.month - 1) if a.month > 1 else (a.year - 1, 12)
    rows.append((a, v, v * 12 / p * 100, mv[pm]))
g = [[r[2] for r in rows if r[3] >= 20], [r[2] for r in rows if 15 <= r[3] < 20], [r[2] for r in rows if r[3] < 15]]
med = [round(S.median(x), 1) for x in g]; cnt = [len(x) for x in g]
print('groups', med, cnt)
BG = '#1E293B'; TOPIC_PX, NUM_PX = 60, 46
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, 'JEPI 분배금과 VIX', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.785, '앞 달 변동성(VIX)에 따른 1년 환산 분배율', fontproperties=Bs(27), color='#CBD5E1')
ax = fig.add_axes([0.1, 0.17, 0.8, 0.55]); ax.set_facecolor(BG)
for i, (val, lab, col) in enumerate([(med[2], 'VIX 15 미만', GRY), (med[0], 'VIX 20 이상', ORG)]):
    ax.bar(i, val, 0.55, color=col)
    ax.text(i, val + 0.3, f'{val}%', ha='center', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -0.5, lab, ha='center', va='top', fontproperties=Bs(26), color='white')
ax.set_ylim(-2.5, 13.5); ax.set_xlim(-0.6, 1.6); ax.axis('off')
fig.text(0.07, 0.045, '분배 77번의 묶음별 중간값 · 달러 · 세전 · 2026.11.24까지', fontsize=17, color='#CBD5E1')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API JEPI 분배 events·일별 종가, ^VIX 일별 종가(11/25 받음)로 직접 계산, calc_out.txt',
           'made_at': '2026-11-25', 'by': 'research/jepivix1127/mkimg.py', 'out': 'img/00.png', 'topic': 'JEPI 분배금과 VIX', 'num': f'{med[2]}%·{med[0]}%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 3 coldbull_iy 차트형 첫 사진 + 경쟁 1 quf02071227 상품명 큰 글자'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK); fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
labs = [f'VIX 15 미만\n({cnt[2]}번)', f'VIX 15~20\n({cnt[1]}번)', f'VIX 20 이상\n({cnt[0]}번)']; vals = [med[2], med[1], med[0]]
ax.bar(range(3), vals, 0.55, color=[GRY, NAVY, ORG])
for i, v in enumerate(vals): ax.text(i, v + 0.2, f'{v}%', ha='center', fontproperties=Bs(20), color=INK)
ax.set_xticks(range(3)); ax.set_xticklabels(labs, fontproperties=Bs(15)); ax.tick_params(axis='x', length=0); ax.set_yticks([])
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.set_ylim(0, 12.5)
frame(fig, '앞 달 VIX가 높을수록 분배율도 높았다', '그달 분배금 × 12 ÷ 배당락 전날 주가 · 묶음별 가운데 값 · 2020.7~2026.11')
fig.subplots_adjust(top=0.83, bottom=0.14, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); ax2 = ax.twinx()
xs = [r[0] for r in rows]
ax.bar(xs, [r[1] for r in rows], width=20, color=ORG, label='1주당 분배금(달러, 왼쪽)')
ax2.plot(xs, [r[3] for r in rows], color=NAVY, lw=2.5, label='앞 달 VIX 평균(오른쪽)')
ax.set_ylim(0, 0.75); ax2.set_ylim(0, 40)
for a_ in (ax, ax2):
    for s_ in ('top',): a_.spines[s_].set_visible(False)
ax.tick_params(labelsize=11); ax2.tick_params(labelsize=11)
i22 = max(range(len(rows)), key=lambda i: rows[i][1])
ax.annotate(f'{rows[i22][0]:%Y.%m} {rows[i22][1]:.2f}달러', (rows[i22][0], rows[i22][1]), xytext=(0, 12), textcoords='offset points', ha='center', fontproperties=Bs(13), color=ORG)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc='upper right', frameon=False, prop=Bs(12))
frame(fig, '월 분배금(막대)과 앞 달 VIX(선)', '2022년처럼 VIX가 높던 때 분배금 막대도 길었다')
fig.subplots_adjust(top=0.83, bottom=0.1, left=0.08, right=0.93); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
