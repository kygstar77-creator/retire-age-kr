# hidden1116 그림 2장 — 숫자는 calc_out.txt(금융위 2026-02-11 보도자료 표1·표3·참고1)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, LG = '#EA580C', '#111827', '#4B5563', '#94A3B8'
rows = [('카드포인트', 6309, 29060), ('증권', 4037, 20686), ('예·적금', 3388, 75209), ('보험금', 2579, 58506)]
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=100)
for i, (n, r, b) in enumerate(rows):
    y = len(rows) - 1 - i; v = r / b * 100; c = ORG if v > 10 else LG
    ax.barh(y, v, color=c, height=0.6)
    ax.text(v + 0.4, y, f'약 {v:.0f}만원', va='center', fontproperties=Bs(18), color=c if v > 10 else INK)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1], fontproperties=Bs(17), color=INK)
ax.set_xlim(0, 30); ax.set_xticks([]); [ax.spines[s].set_visible(False) for s in ['top', 'right', 'bottom']]
ax.set_title('잠자던 돈 100만원 중 캠페인 두 달에 돌아온 돈', fontproperties=Bs(21), color=INK, loc='left', pad=14)
fig.text(0.01, 0.04, '돌아온 돈 = 2025.9.15~10.31 캠페인 환급, 잠자던 돈 = 2025.6월 말 잔액 · 직접 계산', fontproperties=Bs(11), color=SUB)
fig.text(0.01, 0.005, '자료: 금융위원회·금융감독원 보도자료(2026.2.11) [표1]·[참고1]', fontsize=10, color=SUB)
plt.tight_layout(rect=(0, 0.07, 1, 1)); plt.savefig('pkg/img/01.png'); plt.close()
ages = [('60대 이상', 42.5), ('50대', 24.9), ('40대', 16.6), ('30대', 10.2), ('20대', 3.2), ('10대 이하', 2.6)]
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=100)
for i, (n, v) in enumerate(ages):
    y = len(ages) - 1 - i; c = ORG if v > 20 else LG
    ax.barh(y, v, color=c, height=0.6); ax.text(v + 0.6, y, f'{v}%', va='center', fontproperties=Bs(17), color=c if v > 20 else INK)
ax.set_yticks(range(len(ages))); ax.set_yticklabels([a[0] for a in ages][::-1], fontproperties=Bs(16), color=INK)
ax.set_xlim(0, 50); ax.set_xticks([]); [ax.spines[s].set_visible(False) for s in ['top', 'right', 'bottom']]
ax.set_title('숨은 돈을 찾아간 사람, 나이별 비중', fontproperties=Bs(21), color=INK, loc='left', pad=14)
fig.text(0.01, 0.005, '2025년 숨은 금융자산 찾아주기 캠페인 환급 · 자료: 금융위원회·금융감독원 보도자료(2026.2.11) [표3]', fontsize=10, color=SUB)
plt.tight_layout(rect=(0, 0.05, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
