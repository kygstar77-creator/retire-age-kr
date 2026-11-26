# decdiv1126 그림 — 00 표지(12월 배당락 달력 7개), 01 작년 12월 배당이 1년 배당의 몇 %, 02 1만 달러어치 작년 12월 세후. 숫자는 raw·calc_out.txt 그대로
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
T = ['JEPI', 'JEPQ', 'SCHD', 'DGRO', 'VYM', 'VIG', 'VOO']
def yh(t):
    r = json.load(open(f'raw/yahoo_{t}.json', encoding='utf-8'))['chart']['result'][0]
    cl = r['indicators']['quote'][0]['close']; px = r.get('meta', {}).get('regularMarketPrice') or [c for c in cl if c is not None][-1]  # 11/26: 마지막 날 막대가 비면 meta 정규장 종가
    dv = sorted((D.datetime.fromtimestamp(int(k), D.UTC).date(), v['amount']) for k, v in r['events']['dividends'].items())
    y = sum(a for d, a in dv if d.year == 2025); dec = sum(a for d, a in dv if d.year == 2025 and d.month == 12)
    return px, y, dec
V = {t: yh(t) for t in T}
# 운용사 일정표(raw/*.pdf) 12월 배당락일·지급일
SCHED = [('JEPI·JEPQ', 1, 3), ('SCHD', 9, 14), ('DGRO', 15, 18), ('VYM', 18, 22), ('VIG·VOO', 21, 23)]
BG = '#123B34'; TOPIC_PX, NUM_PX = 58, 40
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '12월 배당락일', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.785, '미국 배당 ETF 7개 · 운용사 일정표 기준', fontproperties=Bs(27), color='#BFE8DC')
ax = fig.add_axes([0.08, 0.17, 0.86, 0.55]); ax.set_facecolor(BG)
for i, (n, ex, pay) in enumerate(SCHED):
    y = len(SCHED) - 1 - i
    ax.plot([ex, pay], [y, y], color='#5E9C8C', lw=3, zorder=1)
    ax.scatter([ex], [y], s=260, color=ORG, zorder=3); ax.scatter([pay], [y], s=120, color='white', zorder=3)
    ax.text(0.2, y + 0.28, n, fontproperties=Bs(22), color='white')
    ax.text(ex, y - 0.42, f'{ex}일', fontproperties=Bs(17), color='#FDBA74', ha='center')
for d in (1, 8, 15, 22, 29): ax.text(d, -1.05, f'12/{d}', fontsize=14, color='#BFE8DC', ha='center')
ax.text(16.5, 4.35, '가장 빠른 날 12월 1일', fontproperties=Bs(NUM_PX - 12), color='#FDBA74', ha='left')
ax.set_xlim(0, 31.5); ax.set_ylim(-1.3, 4.9); ax.axis('off')
fig.text(0.07, 0.075, '주황 점 = 배당락일 · 흰 점 = 지급일 (미국 날짜, 2026년)', fontsize=17, color='#BFE8DC')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '슈왑 2026 주식 ETF 분배 일정표(7/28자)·뱅가드 2026 배당 일정표·아이셰어즈 2026-2028 분배 일정표(11/18자)·JP모건 ETF 2026 배당 달력(11/24 받음)',
           'made_at': '2026-11-24', 'by': 'research/decdiv1126/mkimg.py', 'out': 'img/00.png', 'topic': '12월 배당락일', 'num': '가장 빠른 날 12월 1일',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX - 12, 'follows': '경쟁 1 few_economy/224477589614 12월 배당 달력 표지 + dgro1125 차트형 표지'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
SRC = '야후 파이낸스 배당 기록·11/25 종가(11/26 받음) · 파이어맵 계산'
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK); fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
order = sorted(T, key=lambda t: V[t][2] / V[t][1])
fig = plt.figure(figsize=(9, 6), dpi=100); fig.patch.set_facecolor('white')
frame(fig, '2025년 12월 배당, 1년 배당의 몇 %', '1주당 2025년 12월에 배당락된 금액 ÷ 2025년 1년 합 · 점선 = 4분의 1(25%)')
ax = fig.add_axes([0.12, 0.1, 0.84, 0.72])
vals = [V[t][2] / V[t][1] * 100 for t in order]
b = ax.barh(order, vals, color=[ORG if t == 'DGRO' else (GRY if t in ('JEPI', 'JEPQ') else NAVY) for t in order])
for x, v in zip(b, vals): ax.text(v + 0.4, x.get_y() + x.get_height() / 2, f'{v:.1f}%', va='center', fontsize=14, color=INK)
ax.axvline(25, color=SUBC, lw=1, ls='--'); ax.set_xlim(0, 36)
ax.spines[['top', 'right', 'bottom']].set_visible(False); ax.set_xticks([]); ax.tick_params(labelsize=14)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
order2 = sorted(T, key=lambda t: 10000 / V[t][0] * V[t][2])
fig = plt.figure(figsize=(9, 6), dpi=100); fig.patch.set_facecolor('white')
frame(fig, '1만 달러어치라면 12월 배당 얼마', '11/25 종가로 산 주식 수 × 2025년 12월 1주당 배당 · 미국 세금 15% 뗀 뒤(달러)')
ax = fig.add_axes([0.12, 0.1, 0.84, 0.72])
vals = [10000 / V[t][0] * V[t][2] * 0.85 for t in order2]
b = ax.barh(order2, vals, color=[GRY if t in ('JEPI', 'JEPQ') else NAVY for t in order2])
for x, v in zip(b, vals): ax.text(v + 2, x.get_y() + x.get_height() / 2, f'약 {v:.0f}달러', va='center', fontsize=14, color=INK)
ax.set_xlim(0, 230); ax.spines[['top', 'right', 'bottom']].set_visible(False); ax.set_xticks([]); ax.tick_params(labelsize=14)
fig.text(0.12, 0.83, '회색 = 2025년 12월에 배당락이 두 번(12/1·12/31)', fontsize=11.5, color=SUBC)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print({t: (round(V[t][2] / V[t][1] * 100, 1), round(10000 / V[t][0] * V[t][2] * 0.85, 1)) for t in T})
