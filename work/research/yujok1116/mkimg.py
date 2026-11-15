# yujok1116 그림 2장 — 숫자는 calc_out.txt(국민연금공단 금액별 현황 2026년 7월)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, BLU, LG = '#EA580C', '#111827', '#4B5563', '#2563EB', '#CBD5E1'
# 01 구간 비율: 유족 vs 노령
B = ['20만원 미만', '20만~40만원', '40만~60만원', '60만~80만원', '80만~100만원', '100만원 이상']
yu = [3.2, 65.3, 20.0, 7.0, 3.1, 1.5]; no = [7.5, 33.6, 21.1, 12.7, 7.7, 17.4]
fig, ax = plt.subplots(figsize=(9, 5.8), dpi=100)
y = np.arange(len(B))[::-1]; h = 0.38
ax.barh(y + h/2, yu, h, color=ORG, label='유족연금')
ax.barh(y - h/2, no, h, color=LG, label='노령연금(본인 연금)')
for yy, a, b in zip(y, yu, no):
    ax.text(a + 0.8, yy + h/2, f'{a}%', va='center', fontproperties=Bs(15), color=ORG)
    ax.text(b + 0.8, yy - h/2, f'{b}%', va='center', fontproperties=Bs(13), color=SUB)
ax.set_yticks(y); ax.set_yticklabels(B, fontproperties=Bs(15), color=INK)
ax.set_xlim(0, 76); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.legend(prop=Bs(13), frameon=False, loc='lower right')
ax.set_title('월 받는 금액별 수급자 비율 (2026년 7월)', fontproperties=Bs(21), color=INK, loc='left', pad=14)
fig.text(0.01, 0.01, '유족연금 112만 6,837명 · 노령연금 666만 9,689명 · 자료: 국민연금공단 국민연금 통계 금액별 현황', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/01.png'); plt.close()
# 02 선택 비교: 유족연금 60만원일 때
rows = [('내 연금 30만원', 30, 18), ('내 연금 50만원', 50, 18)]
fig, ax = plt.subplots(figsize=(9, 5.0), dpi=100)
for i, (n, own, add) in enumerate(rows):
    yy = 3 - i*1.6
    ax.barh(yy + 0.3, own, 0.5, color=LG); ax.barh(yy + 0.3, add, 0.5, left=own, color=BLU)
    ax.text(own + add + 1, yy + 0.3, f'내 연금+30% = {own+add}만원', va='center', fontproperties=Bs(15), color=BLU)
    ax.barh(yy - 0.3, 60, 0.5, color=ORG)
    ax.text(61, yy - 0.3, '유족연금만 = 60만원', va='center', fontproperties=Bs(15), color=ORG)
    ax.text(-1, yy, n, va='center', ha='right', fontproperties=Bs(16), color=INK)
ax.set_xlim(-22, 100); ax.set_ylim(0.6, 3.8); ax.axis('off')
ax.set_title('유족연금이 월 60만원일 때, 어느 쪽이 많을까', fontproperties=Bs(20), color=INK, loc='left', pad=10)
fig.text(0.01, 0.02, '예시: 가입 20년 넘은 분의 기본연금액 100만원 × 60%(부양가족연금 뺌) · 내 연금 42만원(유족연금의 70%)에서 갈림 · 규칙: 국민연금공단 급여의 조정', fontsize=9, color=SUB)
plt.tight_layout(rect=(0, 0.04, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
