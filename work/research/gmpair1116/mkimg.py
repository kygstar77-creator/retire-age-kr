# gmpair1116 본문 그림 — 01 84㎡대 반기별 가운데 값(광명·구로·금천), 02 2026년 상반기 '가운데 값 vs 같은 집' 함정. 표지 00은 cafecover.py. 숫자는 calc_out·calc2_out 그대로
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, LBLUE, INK, SUBC, ORG, GRY = '#1D4ED8', '#93C5FD', '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = '국토교통부 아파트 매매 실거래(11/16 받음, 해제 제외) · 전용 80~85㎡ · 파이어맵 계산'
hs = ['23 상', '23 하', '24 상', '24 하', '25 상', '25 하', '26 상', '26.7~11']
gm = [8.60, 8.415, 8.15, 8.10, 9.35, 9.60, 8.45, 9.90]
gr = [7.35, 7.80, 7.50, 8.00, 8.10, 8.30, 7.90, 8.35]
gc = [6.875, 6.40, 6.40, 6.77, 6.40, 7.10, 7.20, 7.10]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
xs = range(len(hs))
for ys, c, nm in ((gm, ORG, '광명'), (gr, BLUE, '구로'), (gc, GRY, '금천')):
    ax.plot(xs, ys, color=c, lw=3.2, marker='o', ms=7)
    ax.text(len(hs) - 0.85, ys[-1], f'{nm} {ys[-1]:.2f}억', va='center', fontproperties=Bs(15), color=c)
ax.annotate('거의 같은 값\n(1천만원 차이)', xy=(3, 8.05), xytext=(2.2, 9.35), fontproperties=Bs(13), color=INK,
            arrowprops=dict(arrowstyle='->', color=INK, lw=1.4))
ax.set_xticks(list(xs)); ax.set_xticklabels(hs, fontsize=12.5); ax.set_xlim(-0.3, len(hs) + 0.9)
ax.set_ylim(5.8, 10.6); ax.set_yticks([6, 7, 8, 9, 10]); ax.set_yticklabels(['6억', '7억', '8억', '9억', '10억'], fontsize=12)
ax.grid(axis='y', color='#E5E7EB'); ax.set_axisbelow(True)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.93, '84㎡대 중간값, 반기마다', fontproperties=Bs(23), color=INK)
fig.text(0.04, 0.88, '광명과 구로 차이는 좁아졌다 벌어졌다 · 금천과는 내내 1억원 넘게', fontsize=13.5, color=SUBC)
fig.text(0.04, 0.025, SRC, fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.09, right=0.98)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 함정
fig, axs = plt.subplots(1, 2, figsize=(9, 6.4), dpi=100, gridspec_kw={'width_ratios': [1, 1]})
ax = axs[0]
ax.bar([0, 1], [9.60, 8.45], width=0.6, color=[GRY, ORG])
for i, v in enumerate([9.60, 8.45]): ax.text(i, v + 0.12, f'{v:.2f}억', ha='center', fontproperties=Bs(16), color=INK)
ax.set_xticks([0, 1]); ax.set_xticklabels(['2025 하반기', '2026 상반기'], fontsize=12.5); ax.set_yticks([]); ax.set_ylim(0, 11)
ax.set_title('광명 중간값', fontproperties=Bs(17), color=INK, pad=10)
ax = axs[1]
ax.bar([0, 1], [12, 23], width=0.6, color=[GRY, BLUE])
for i, v in enumerate([12, 23]): ax.text(i, v + 0.5, f'{v}%', ha='center', fontproperties=Bs(16), color=INK)
ax.set_xticks([0, 1]); ax.set_xticklabels(['2025 하반기', '2026 상반기'], fontsize=12.5); ax.set_yticks([]); ax.set_ylim(0, 28)
ax.set_title('광명에서 팔린 집 중 소하동 비율', fontproperties=Bs(17), color=INK, pad=10)
for a in axs:
    for s in ('top', 'right', 'left'): a.spines[s].set_visible(False)
fig.text(0.04, 0.93, '중간값은 내렸는데, 같은 집은 약 9% 올랐다', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.88, '값이 낮은 소하동(7.5억) 거래가 늘어서 · 철산동은 9.24억', fontsize=13.5, color=SUBC)
fig.text(0.04, 0.025, SRC, fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.76, bottom=0.1, left=0.04, right=0.98, wspace=0.25)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
