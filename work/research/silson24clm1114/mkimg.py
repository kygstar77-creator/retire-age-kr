# silson24clm1114 그림 2장 — fin2kpct1114 mkimg.py 틀 재사용, 숫자는 calc_out.txt(금융위 2026-05-11·09-30 보도자료)
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
# 01: 연계율 5/6 → 9/28 → 연말 목표
rows = [('5월 6일', 29.0, BLU, '29.0%'), ('9월 28일', 47.7, BLU, '47.7%'), ('연말 목표', 80, LG, '80~90%')]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, v, c, lab) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.barh(y, v, color=c, height=0.6)
    if n == '연말 목표': ax.barh(y, 10, left=80, color=LG, height=0.6, alpha=0.5)
    ax.text((90 if n == '연말 목표' else v) + 1.5, y, lab, va='center', fontproperties=Bs(17), color=SUB if n == '연말 목표' else BLU)
ax.text(29.0 / 2, 2, '3만 614곳', va='center', ha='center', fontproperties=Bs(13), color='white')
ax.text(47.7 / 2, 1, '5만 340곳', va='center', ha='center', fontproperties=Bs(13), color='white')
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1], fontproperties=Bs(16), color=INK)
ax.set_xlim(0, 108); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.set_title('실손24 연결된 병원·의원·약국 비율', fontproperties=Bs(21), color=INK, loc='left', pad=14)
fig.text(0.01, 0.01, '전체 10만 5,643곳(9월 28일 기준) 대비 · 자료: 금융위원회 보도자료(2026년 5월 11일·9월 30일)', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/01.png'); plt.close()
# 02: 하루에 늘어난 곳 vs 연말 목표에 필요한 속도
rows = [('5월~9월 실제', 136.0, BLU, '하루 136곳'), ('연말 80%까지', 363.6, ORG, '하루 364곳'), ('연말 90%까지', 475.9, ORG, '하루 476곳')]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, v, c, lab) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.barh(y, v, color=c, height=0.6, alpha=1 if i < 2 else 0.55)
    ax.text(v + 8, y, lab, va='center', fontproperties=Bs(17), color=c)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1], fontproperties=Bs(16), color=INK)
ax.set_xlim(0, 620); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.set_title('하루에 몇 곳씩 연결돼야 할까', fontproperties=Bs(21), color=INK, loc='left', pad=14)
fig.text(0.01, 0.01, '실제: 5월 6일~9월 28일(145일) 평균 · 필요: 9월 28일~12월 31일(94일) · 금융위원회 보도자료로 직접 계산', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
