# fin2kpct1114 그림 2장 — 숫자는 calc_out.txt(TASIS 3-1-5, 2024년 귀속)
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
rows = [('2천만~3천만원', 178207), ('3천만~4천만원', 80468), ('4천만~1억원', 121240), ('1억~5억원', 45029), ('5억원 초과', 7159)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, v) in enumerate(rows):
    y = len(rows)-1-i
    ax.barh(y, v, color=BLU, height=0.6)
    ax.text(v + 2500, y, f'{v:,}명', va='center', fontproperties=Bs(15), color=BLU)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([n for n, _ in rows][::-1], fontproperties=Bs(15), color=INK)
ax.set_xlim(0, 225000); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.set_title('금융소득 크기별 신고자 수 (2024년)', fontproperties=Bs(21), color=INK, loc='left', pad=14)
fig.text(0.01, 0.01, '자료: 국세청 국세통계포털 3-1-5(2024년 귀속) · 구간 폭이 서로 다름 · 전체 43만 5,380명 중 표의 \'2천만 이하\' 3,277명은 뺌', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/01.png'); plt.close()
rows = [('금융소득 2천만~3천만원', 40.9, 11.6), ('금융소득 5억원 초과', 1.6, 38.3)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, a, b) in enumerate(rows):
    y = len(rows)-1-i
    ax.barh(y + 0.2, a, color=LG, height=0.36); ax.barh(y - 0.2, b, color=ORG, height=0.36)
    ax.text(a + 0.8, y + 0.2, f'사람 {round(a)}%' if a>10 else f'사람 {a}%', va='center', fontproperties=Bs(15), color=SUB)
    ax.text(b + 0.8, y - 0.2, f'금융소득 {round(b)}%', va='center', fontproperties=Bs(15), color=ORG)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([n for n, _, _ in rows][::-1], fontproperties=Bs(15), color=INK)
ax.set_xlim(0, 60); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.set_title('사람 수 비중과 금융소득 비중', fontproperties=Bs(21), color=INK, loc='left', pad=14)
fig.text(0.01, 0.01, '전체 신고자 43만 5,380명·전체 금융소득 약 36조 9천억원 대비 · 자료: 국세청 국세통계포털 3-1-5(2024년 귀속)', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
