# yejung1115 그림 2장 — 숫자는 calc_out.txt(TASIS 4-2-4 2024년 귀속)
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
def bars(rows, fmt, xmax, title, foot, out):
    fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
    for i, (n, v, c) in enumerate(rows):
        y = len(rows)-1-i
        ax.barh(y, v, color=c, height=0.6)
        ax.text(v + xmax*0.015, y, fmt(v), va='center', fontproperties=Bs(17), color=c if c != LG else SUB)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([n for n, _, _ in rows][::-1], fontproperties=Bs(15), color=INK)
    ax.set_xlim(0, xmax); ax.set_xticks([])
    for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
    ax.set_title(title, fontproperties=Bs(21), color=INK, loc='left', pad=14)
    fig.text(0.01, 0.01, foot, fontsize=9.5, color=SUB)
    plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig(out); plt.close()
foot = '2024년 귀속 근로소득 연말정산 2,108만 명 · 자료: 국세청 국세통계포털(TASIS) 4-2-4'
bars([('3천만원 이하', 9.5, LG), ('3천만원 초과~5천만원', 23.1, BLU), ('5천만원 초과~8천만원', 23.2, BLU), ('8천만원 초과~1억원', 24.7, BLU), ('1억원 초과', 31.2, ORG)],
     lambda v: f'{v}%', 38, '연말정산 때 세금을 더 낸 사람 비율 (총급여별)', foot, 'pkg/img/01.png')
bars([('3천만원 이하', 10, LG), ('3천만원 초과~5천만원', 37, BLU), ('5천만원 초과~8천만원', 79, BLU), ('8천만원 초과~1억원', 137, BLU), ('1억원 초과', 577, ORG)],
     lambda v: f'약 {v}만원', 700, '더 낸 사람 1인당 평균 추가납부액 (총급여별)', foot, 'pkg/img/02.png')
print('ok')
