# convrate1112 그림 2장 — 01 갱신 월세 한도 예시(전세 4억4천→보증금 3억4천) 02 갱신 계약 483건 중 한도 넘음
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, LBLUE, INK, GR, SUBC, ORG = '#1D4ED8', '#93C5FD', '#111827', '#CBD5E1', '#6B7280', '#EA580C'
pd, dp, cap = 44000, 34000, 5.0
a = (pd - dp) * cap / 100 / 12; b = (pd * 1.05 - dp) * cap / 100 / 12
# 01
fig, ax = plt.subplots(figsize=(9, 6.2), dpi=100)
ax.barh([1, 0], [a, b], color=[LBLUE, BLUE], height=0.55)
ax.text(a + 1, 1, f'{a:.0f}만원쯤', va='center', fontproperties=Bs(22), color=INK)
ax.text(b + 1, 0, f'{b:.0f}만원쯤', va='center', fontproperties=Bs(22), color=INK)
ax.set_yticks([1, 0]); ax.set_yticklabels(['줄인 1억원 몫만\n(1억원 × 5% ÷ 12)', '올릴 수 있는 5%까지\n더하면(넘을 수 없는 선)'], fontproperties=Bs(15))
ax.set_xlim(0, 70); ax.set_xticks([])
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.9, '전세 4억 4천 → 보증금 3억 4천으로 갱신하면', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.83, '한 달 월세 한도(기준금리 3% + 2%p = 5%)', fontsize=16, color=SUBC)
fig.text(0.04, 0.03, '주택임대차보호법 제7조의2·시행령 제9조(전환), 제6조의3③·제7조②(갱신 5%) · 계약갱신요구권을 쓴 갱신 기준', fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.78, bottom=0.12, left=0.30, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02
fig, ax = plt.subplots(figsize=(9, 6.2), dpi=100)
grp = [('보증금 그대로 두고\n월세를 붙인 계약', 433, 101), ('보증금을 줄이고\n월세로 바꾼 계약', 50, 14)]
for y, (lab, n, o) in zip((1, 0), grp):
    ax.barh(y, n - o, color=GR, height=0.55); ax.barh(y, o, left=n - o, color=ORG, height=0.55)
    ax.text(n + 6, y, f'{o}건 / {n}건', va='center', fontproperties=Bs(20), color=INK)
ax.set_yticks([1, 0]); ax.set_yticklabels([g[0] for g in grp], fontproperties=Bs(15))
ax.set_xlim(0, 640); ax.set_xticks([])
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=ORG, label='한도보다 월세가 높게 신고'), Patch(color=GR, label='한도 안')], frameon=False, fontsize=14, loc='lower right')
fig.text(0.04, 0.9, '갱신요구권 쓰고 월세 붙은 483건 중 115건(24%)', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.83, '넘은 금액 가운데 값 한 달 18만원쯤', fontsize=16, color=SUBC)
fig.text(0.04, 0.03, '국토교통부 아파트 전월세 실거래 서울 25개 구 2026년 8~10월 계약(11/12 받음) · 원래 전세였던 갱신만 · 5% 인상분까지 월세로 본 넉넉한 한도', fontsize=10, color=SUBC)
fig.subplots_adjust(top=0.78, bottom=0.12, left=0.30, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print(round(a, 1), round(b, 1))
