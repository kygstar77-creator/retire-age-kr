# jwrate1022 그림 3장 — 숫자는 calc.py(주택임대차보호법 7조의2·시행령 9조, ECOS 기준금리 일별)
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
ORG, INK, SUB, GR, NAVY = '#EA580C', '#111827', '#4B5563', '#CBD5E1', '#1E3A8A'
# 00 표지 — 짙은 남색 바탕, 큰 글 두 줄 + 보증금 1억 전환 시 월세 상한 막대 3개
BG, WH, LG = '#13243F', '#FFFFFF', '#C7D2E3'
P = ['7월 15일까지\n상한 4.5%', '7월 16일부터\n상한 4.75%', '8월 27일부터\n상한 5%']
V = [375000, 395833, 416667]
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.875, '전월세전환율 5% 그대로', fontsize=64, fontproperties=B, color=WH)
fig.text(0.06, 0.765, '1억이면 월 41만 6,667원', fontsize=66, fontproperties=B, color='#FB923C')
fig.text(0.06, 0.715, '보증금 1억원을 월세로 돌릴 때 받을 수 있는 한 달 상한', fontsize=24, color=LG)
ax = fig.add_axes([0.08, 0.2, 0.86, 0.45]); ax.set_facecolor(BG)
cols = ['#5B6F94', '#7C8DB0', '#FB923C']
ax.bar(range(3), V, color=cols, width=0.6)
for i, v in enumerate(V):
    ax.text(i, v + 6000, f'{v/10000:,.1f}만원', ha='center', fontproperties=Bs(30), color=WH)
ax.set_xticks(range(3)); ax.set_xticklabels(P, fontproperties=Bs(22), color=WH)
ax.set_yticks([]); ax.set_ylim(300000, 440000)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.spines['bottom'].set_color(LG); ax.tick_params(length=0)
fig.text(0.06, 0.07, '10월 22일 기준금리 3.00% 동결 → 다음 결정 11월 26일', fontsize=24, fontproperties=B, color='#FDBA74')
fig.text(0.06, 0.025, '주택임대차보호법 제7조의2 · 시행령 제9조 · 한국은행 기준금리 · 2026.10.22 직접 계산', fontsize=17, color=LG)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 표 — 월세로 돌리는 보증금 · 7월 15일까지 · 지금(3칸)
rows = [('5천만원', '18만 7,500원', '20만 8,333원'), ('1억원', '37만 5,000원', '41만 6,667원'),
        ('2억원', '75만원', '83만 3,333원'), ('3억원', '112만 5,000원', '125만원')]
fig = plt.figure(figsize=(9, 6.4), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.91, '보증금을 월세로 돌릴 때 한 달 상한', fontsize=26, fontproperties=B, color=INK)
fig.text(0.05, 0.85, '돌리는 금액 × 상한 비율 ÷ 12', fontsize=18, color=SUB)
hy = 0.74; cs = [0.07, 0.40, 0.70]
for c, h in zip(cs, ['월세로 돌리는 보증금', '7월 15일까지(4.5%)', '지금(5%)']):
    fig.text(c, hy, h, fontsize=18, fontproperties=B, color=NAVY)
fig.add_artist(plt.Line2D([0.05, 0.95], [hy - 0.03, hy - 0.03], color=INK, lw=1.5))
for i, (a, b, c) in enumerate(rows):
    y = hy - 0.13 - i * 0.13
    hl = a == '1억원'
    fig.text(cs[0], y, a, fontsize=22, fontproperties=B if hl else None, color=INK)
    fig.text(cs[1], y, b, fontsize=22, color=SUB)
    fig.text(cs[2], y, c, fontsize=22, fontproperties=B, color=ORG if hl else INK)
    fig.add_artist(plt.Line2D([0.05, 0.95], [y - 0.04, y - 0.04], color=GR, lw=0.8))
fig.text(0.05, 0.04, '주택임대차보호법 제7조의2 · 시행령 제9조 · 한국은행 기준금리(ECOS) · 원 단위 반올림', fontsize=12.5, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 갱신 때 — 글자 카드(생활법령 Q&A 예시 전세 5억을 지금 5%로 다시 계산)
fig = plt.figure(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('#F8FAFC')
fig.text(0.05, 0.9, '갱신 때 전세를 반전세로 바꾼다면', fontsize=27, fontproperties=B, color=INK)
fig.text(0.05, 0.845, '세입자가 동의해야 하고, 동의해도 5% 상한은 그대로', fontsize=17, color=SUB)
fig.text(0.07, 0.72, '전세 5억원 집, 지금 상한 5%로 바꾸면', fontsize=20, fontproperties=B, color=NAVY)
L = [('보증금 3억원으로 낮추면', '월 83만 3,333원까지'), ('보증금 2억원으로 낮추면', '월 125만원까지')]
for i, (a, b) in enumerate(L):
    y = 0.58 - i * 0.15
    fig.text(0.07, y, a, fontsize=22, color=INK)
    fig.text(0.95, y, b, ha='right', fontsize=24, fontproperties=B, color=ORG)
    fig.add_artist(plt.Line2D([0.05, 0.95], [y - 0.05, y - 0.05], color=GR, lw=0.8))
fig.text(0.05, 0.2, '상한보다 더 냈다면 넘게 낸 만큼 돌려 달라고 할 수 있어요', fontsize=18, fontproperties=B, color=NAVY)
fig.text(0.05, 0.14, '(주택임대차보호법 제10조의2)', fontsize=15, color=SUB)
fig.text(0.05, 0.03, '법제처 생활법령 「차임 또는 보증금의 증감청구」 Q&A ④ 예시를 지금 비율로 다시 계산', fontsize=12.5, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
