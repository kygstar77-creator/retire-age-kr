# parking1109 그림 2장 — 숫자는 diff_out.txt·calc_out.txt(저축은행중앙회 공시 10/6·11/9, 카카오뱅크 11/9)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR, LG = '#EA580C', '#111827', '#4B5563', '#94A3B8', '#CBD5E1'
SRC = '저축은행중앙회 소비자포털 입출금자유예금 공시(2026.10.6·11.9 조회)'

# 01 한 달 새 바뀐 금리 (10/6 → 11/9, 같은 구간끼리)
rows = [('우리금융 첫번째저축예금\n(5천만원까지)', 2.5, 3.5), ('대신 더드리고입출금\n(2억원까지)', 3.0, 3.4),
        ('에스앤티 우리가족사랑\n(1천만원~1억원)', 2.75, 3.1), ('예가람 The프리미엄 멤버십', 2.9, 3.2),
        ('다올 쌈짓돈Ⅲ\n(5백만~5천만원)', 3.3, 3.5), ('고려 보고파플러스', 3.1, 3.1)]
fig, ax = plt.subplots(figsize=(9, 7.0), dpi=100)
for i, (n, a, b) in enumerate(rows[::-1]):
    up = b > a
    ax.plot([a, b], [i, i], color=ORG if up else LG, lw=4, solid_capstyle='round', zorder=1)
    ax.scatter([a], [i], s=70, color=GR, zorder=2)
    ax.scatter([b], [i], s=110, color=ORG if up else SUB, zorder=3)
    ax.text(b + 0.04, i, f'{b:g}%' + (f'  (+{b-a:.2f}%p)'.replace('.00', '.0') if up else '  그대로'), va='center',
            fontproperties=Bs(14), color=ORG if up else SUB)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]], fontproperties=Bs(12.5))
ax.set_xlim(2.3, 4.3); ax.set_xticks([2.5, 3.0, 3.5, 4.0]); ax.set_xticklabels(['2.5%', '3.0%', '3.5%', '4.0%'], fontsize=12, color=SUB)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0); ax.grid(axis='x', color='#EEF2F7')
fig.text(0.04, 0.93, '파킹통장 금리, 한 달 새 올린 곳', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.885, '회색 점 10월 6일 → 주황 점 11월 9일 (우대 뺀 금리)', fontsize=13, color=SUB)
fig.text(0.04, 0.02, SRC, fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.33, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 광고 최고금리 vs 5천만원 넣었을 때 실제 금리
rows = [('다올 쌈짓돈Ⅲ', 5.0, 3.53), ('우리금융 첫번째저축예금', 3.5, 3.50), ('키움 더 키움 플러스', 3.3, 3.30),
        ('HB 하루플러스통장', 5.0, 3.22), ('카카오뱅크 세이프박스', 1.8, 1.80), ('모아 e-모아파킹통장', 4.0, 1.51)]
fig, ax = plt.subplots(figsize=(9, 6.8), dpi=100)
for i, (n, hi, real) in enumerate(rows[::-1]):
    ax.barh(i, hi, color='#F1F5F9', height=0.62, zorder=1)
    ax.barh(i, real, color=ORG if real >= 3 else GR, height=0.62, zorder=2)
    ax.text(real + 0.06, i, f'{real:.2f}%', va='center', fontproperties=Bs(15), color=ORG if real >= 3 else SUB, zorder=3)
    if hi > real + 0.3: ax.text(hi + 0.06, i, f'최고 {hi:g}%', va='center', fontsize=12, color=GR)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]], fontproperties=Bs(13.5))
ax.set_xlim(0, 6.0); ax.set_xticks([]); 
for s in ('top', 'right', 'left', 'bottom'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
fig.text(0.04, 0.93, '5천만원 넣으면 실제로 붙는 금리', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.885, '연한 막대는 광고하는 최고금리, 진한 막대는 돈 전체로 나눈 금리', fontsize=13, color=SUB)
fig.text(0.04, 0.02, SRC.replace(')', '') + ' · 카카오뱅크 11.9 · 우대 없음)', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.08, left=0.3, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
