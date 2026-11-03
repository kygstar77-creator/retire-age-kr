# j1pair1104 그림 3장 — 숫자는 longform/ep/J-1/calc_out.txt(9/1 정부안, 공시가격 그대로·재산세 공정시장가액비율 45% 가정, 단위 만원) 그대로
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bf(s): return fm.FontProperties(fname=F + r'\pd700.ttf', size=s)
ORG, NAVY, INK, SUB = '#EA580C', '#1E3A8A', '#111827', '#4B5563'
SRC = '9월 1일 정부안(국회 통과 전) · 1세대 1주택 55세·10년 가진 집 · 공시가격 그대로 · 재산세+종부세 · 파이어맵 계산'
# calc_out: 2028 보유세 − 2026 보유세(만원) — 55세·10년 거주 / 55세·거주 0년
P = [12, 14, 15, 16, 18, 20, 22, 25, 30, 40]
LIVE = {12: 0.0, 14: -27.6, 15: -25.3, 16: -23.0, 18: -27.1, 20: -22.5, 22: -15.0, 25: 30.8, 30: 135.9, 40: 820.1}
AWAY = {12: 0.0, 14: -27.6, 15: 39.2, 16: 52.2, 18: 98.5, 20: 140.9, 22: 255.4, 25: 431.3, 30: 775.0, 40: 1845.9}
def won(v):
    if abs(v) < 0.05: return '0원'
    return ('+' if v > 0 else '−') + f'{abs(v):,.0f}만원'

# 00 표지(차트): 큰 글 + 20억 두 막대
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.86, '종부세 개편안', fontproperties=Bf(58), color=INK)
fig.text(0.06, 0.775, '공시가격 20억이면 보유세는?', fontproperties=Bf(40), color='#374151')
fig.text(0.06, 0.64, '직접 사는 집 −22만원', fontproperties=Bf(46), color=NAVY)
fig.text(0.06, 0.555, '안 사는 집 +141만원', fontproperties=Bf(46), color=ORG)
ax = fig.add_axes([0.10, 0.13, 0.82, 0.33])
xs = [p for p in P if p <= 30]
ax.plot(xs, [LIVE[p] for p in xs], color=NAVY, lw=4, marker='o', ms=8, label='10년 살았다')
ax.plot(xs, [AWAY[p] for p in xs], color=ORG, lw=4, marker='o', ms=8, label='10년 가졌지만 안 산다')
ax.axhline(0, color='#9CA3AF', lw=1.5)
ax.set_xticks(xs); ax.set_xticklabels([f'{p}억' for p in xs], fontsize=13)
ax.set_yticks([0, 200, 400, 600, 800]); ax.set_yticklabels(['0', '+200만', '+400만', '+600만', '+800만'], fontsize=12)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.legend(prop=Bf(15), frameon=False, loc='upper left')
fig.text(0.06, 0.475, '55세 1주택 · 2026년 대비 2028년 보유세 변화 · 12억~30억', fontsize=16, color=SUB)
fig.text(0.06, 0.04, SRC, fontsize=9.5, color='#6B7280')
fig.savefig('pkg/img/00.png', dpi=100); plt.close(fig)

# 01 20억 집 네 갈래(calc_out 2028−2026)
rows = [('45세 · 3년 살았다', -75.5, NAVY), ('55세 · 10년 살았다', -22.5, NAVY), ('70세 · 15년 살았다', -7.5, NAVY), ('55세 · 10년 가졌지만 안 산다', 140.9, ORG)]
fig, ax = plt.subplots(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
for i, (nm, v, c) in enumerate(rows):
    y = 3 - i
    ax.barh(y, v, height=0.5, color=c)
    ax.text(v + (4 if v > 0 else -4), y, won(v), va='center', ha='left' if v > 0 else 'right', fontproperties=Bf(20), color=c)
ax.axvline(0, color='#9CA3AF', lw=1.5)
ax.set_yticks([3, 2, 1, 0]); ax.set_yticklabels([r[0] for r in rows], fontproperties=Bf(16))
ax.set_xlim(-210, 230); ax.set_xticks([])
for s in ('top', 'right', 'bottom', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
fig.text(0.05, 0.92, '공시가격 20억 집, 누구냐에 따라', fontproperties=Bf(26), color=INK)
fig.text(0.05, 0.87, '2026년 대비 2028년 보유세(재산세+종부세) 변화', fontsize=15, color=SUB)
fig.text(0.05, 0.03, '9월 1일 정부안(국회 통과 전) · 1세대 1주택 · 공시가격 그대로 · 파이어맵 계산', fontsize=9.5, color='#6B7280')
plt.subplots_adjust(left=0.36, right=0.95, top=0.82, bottom=0.08)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 공시가격별 표(3칸·10줄)
fig = plt.figure(figsize=(9, 10), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.93, '공시가격별 보유세 변화', fontproperties=Bf(30), color=INK)
fig.text(0.06, 0.885, '55세 · 10년 가진 집 · 2026년 대비 2028년', fontsize=16, color=SUB)
X = [0.08, 0.40, 0.70]; y0 = 0.82; dy = 0.068
for x, h, c in zip(X, ['공시가격', '10년 살았다', '안 산다'], [INK, NAVY, ORG]):
    fig.text(x, y0, h, fontproperties=Bf(20), color=c)
for i, p in enumerate(P):
    y = y0 - dy * (i + 1)
    if i % 2 == 0: fig.patches.append(plt.Rectangle((0.05, y - 0.022), 0.9, dy, transform=fig.transFigure, color='#F3F4F6', zorder=0))
    fig.text(X[0], y, f'{p}억', fontproperties=Bf(19), color=INK)
    fig.text(X[1], y, won(LIVE[p]), fontproperties=Bf(19), color=NAVY)
    fig.text(X[2], y, won(AWAY[p]), fontproperties=Bf(19), color=ORG)
fig.text(0.06, 0.04, SRC, fontsize=9.5, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
