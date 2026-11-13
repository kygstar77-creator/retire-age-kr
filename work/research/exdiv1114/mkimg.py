# exdiv1114 그림 2장 — 숫자는 calc_out.txt(DART 결산배당 공시 556건·배당락일 종가)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, BLU, LG = '#EA580C', '#111827', '#4B5563', '#2563EB', '#CBD5E1'
# 1) 기준일 달별 회사 수
rows = [('2025년 12월 말', 269, LG), ('2026년 1월', 1, BLU), ('2026년 2월', 68, BLU), ('2026년 3월', 182, BLU), ('2026년 4월', 36, BLU)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, v, c) in enumerate(rows):
    y = len(rows)-1-i
    ax.barh(y, v, color=c, height=0.6)
    ax.text(v + 4, y, f'{v}곳', va='center', fontproperties=Bs(16), color=INK if c == LG else BLU)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([n for n, _, _ in rows][::-1], fontproperties=Bs(15), color=INK)
ax.set_xlim(0, 320); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.set_title('결산배당 기준일, 12월 말 48% · 이듬해 52%', fontproperties=Bs(21), color=INK, loc='left', pad=14)
fig.text(0.01, 0.01, '코스피 2025 사업연도 결산배당 556곳 · 자료: 금융감독원 DART 현금ㆍ현물배당결정 공시(2026.1.15~4.15 접수)', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/01.png'); plt.close()
# 2) 배당락일 하루 하락폭 ÷ 배당금
rows = [('전체 554곳', 1.00, BLU), ('배당금이 주가의\n3% 이상 202곳', 0.92, ORG), ('12월 말 기준 269곳\n(그날 코스피 +2.2%)', 0.70, LG)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, v, c) in enumerate(rows):
    y = len(rows)-1-i
    ax.barh(y, v, color=c, height=0.55)
    ax.text(v + 0.02, y, f'{v:.2f}배', va='center', fontproperties=Bs(17), color=SUB if c == LG else c)
ax.axvline(1.0, color=INK, lw=1, ls='--'); ax.text(1.01, -0.55, '← 1배 = 배당금만큼 빠짐', ha='left', fontproperties=Bs(12), color=INK)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([n for n, _, _ in rows][::-1], fontproperties=Bs(14), color=INK)
ax.set_xlim(0, 1.3); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.set_title('배당락일 하루 주가 하락폭 ÷ 배당금 (중간값)', fontproperties=Bs(20), color=INK, loc='left', pad=14)
fig.text(0.01, 0.01, '배당락일 전날 종가 − 당일 종가 ÷ 1주당 배당금 · 자료: DART 공시, Yahoo Finance 종가(네이버페이 증권 13곳 대조)', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
