# psfund1021 그림 3장 — 숫자는 금융위·금감원 '2025년 연금저축 투자 백서' 별첨 p.9, calc.py
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, NAVY, INK, SUB = '#EA580C', '#1E3A8A', '#111827', '#4B5563'
# 00 표지 1080x1080 — 남색 바탕(옆 10장 흰 바탕과 구별) · 10년 연평균 수익률 막대 둘
BG, WH, LG = '#0F1E4A', '#FFFFFF', '#CBD5E1'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.875, '연금저축 10년 연평균 수익률', fontsize=54, fontproperties=B, color=WH)
fig.text(0.06, 0.765, '펀드 8.8% vs 보험 0.8%', fontsize=62, fontproperties=B, color='#FB923C')
fig.text(0.06, 0.715, '2025년 말 기준 · 보험과 펀드는 재는 방식이 달라요', fontsize=22, color=LG)
ax = fig.add_axes([0.08, 0.17, 0.86, 0.47]); ax.set_facecolor(BG)
vals = [('연금저축펀드·ETF', 8.8, '#FB923C'), ('연금저축보험', 0.8, LG)]
for i, (n, v, c) in enumerate(vals):
    ax.bar(i, v, width=0.55, color=c)
    ax.text(i, v + 0.25, f'연 {v}%', ha='center', fontsize=40, fontproperties=B, color=WH)
ax.set_xticks([0, 1]); ax.set_xticklabels([v[0] for v in vals], fontproperties=Bs(30), color=WH)
ax.tick_params(colors=WH, length=0)
ax.set_ylim(0, 10.8); ax.set_yticks([])
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.spines['bottom'].set_color(LG)
fig.text(0.06, 0.03, "금융위원회·금융감독원 '2025년 연금저축 투자 백서'(2026.6) · 지난 수익률이며 앞으로를 뜻하지 않음", fontsize=17, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 1,000만원 10년
fig, ax = plt.subplots(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
vals = [('연금저축보험 (연 0.8%)', 1083, '#94A3B8'), ('연금저축펀드·ETF (연 8.8%)', 2324, ORG)]
for i, (n, v, c) in enumerate(vals):
    ax.barh(i, v, height=0.5, color=c)
    ax.text(v + 30, i, f'약 {v:,}만원', va='center', fontsize=26, fontproperties=B, color=INK)
    ax.text(20, i + 0.4, n, va='center', fontsize=19, fontproperties=B, color=INK)
ax.set_xlim(0, 3100); ax.set_ylim(-0.6, 1.9); ax.axis('off')
fig.text(0.05, 0.92, '1,000만원을 10년 전에 넣었다면', fontsize=26, fontproperties=B, color=INK)
fig.text(0.05, 0.86, '참고용 단순 계산 · 한 번에 넣고 10년 연평균이 그대로 쌓였다고 가정', fontsize=18, color=SUB)
fig.text(0.05, 0.03, '연금저축 투자 백서(2026.6) 별첨 수익률 · 파이어맵 계산 · 지난 숫자이며 앞으로를 뜻하지 않음', fontsize=12, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 해지 vs 이전 세금
fig, ax = plt.subplots(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
vals = [('해지하면 (16.5%)', 165, '#94A3B8'), ('연금 받기 전 계좌로 전액 이전', 0, ORG)]
for i, (n, v, c) in enumerate(vals):
    ax.bar(i, max(v, 2), width=0.55, color=c)
    ax.text(i, v + 6, f'{v}만원' if v else '0원', ha='center', fontsize=34, fontproperties=B, color=INK)
ax.set_xticks([0, 1]); ax.set_xticklabels([v[0] for v in vals], fontproperties=Bs(19))
ax.set_ylim(0, 205); ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.92, '세액공제 받은 돈+불어난 돈 1,000만원일 때 세금', fontsize=23, fontproperties=B, color=INK)
fig.text(0.05, 0.86, '세금만 비교 · 해지공제액(통상 가입 7년 안)·펀드 가격 변동은 따로', fontsize=17, color=SUB)
fig.text(0.05, 0.02, '소득세법 제20조의3·제129조·시행령 제40조의4 · 지방세법 제103조의13 · 파이어맵 계산', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.14)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
