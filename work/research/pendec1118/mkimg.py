# pendec1118 그림 2장 — 숫자는 calc_out.txt(소득세법 59조의3 공제율·한도, 금감원 정기예금 12개월 중앙 3.29%)
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
# 01: 넣은 돈별·공제율별 줄어드는 세금(지방세 포함)
rows = [('600만원 · 16.5%', 99.0, ORG), ('600만원 · 13.2%', 79.2, '#F59E0B'), ('900만원 · 16.5%', 148.5, ORG), ('900만원 · 13.2%', 118.8, '#F59E0B')]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, v, c) in enumerate(rows):
    ax.barh(3 - i, v, color=c, height=0.55)
    ax.text(v + 2, 3 - i, f'{v:.1f}만원'.replace('.0만', '만'), va='center', fontproperties=Bs(19), color=INK)
ax.set_yticks(range(4)); ax.set_yticklabels([r[0] for r in rows][::-1], fontproperties=Bs(16), color=INK)
ax.set_xlim(0, 185); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.spines['left'].set_color(LG)
fig.suptitle('12월에 넣어도 줄어드는 세금은 같아요', fontproperties=Bs(23), color=INK, x=0.04, ha='left', y=0.96)
fig.text(0.04, 0.10, '16.5% = 총급여 5,500만원 이하 · 13.2% = 그보다 많을 때', fontproperties=Bs(14), color=BLU)
fig.text(0.04, 0.03, '지방소득세 포함 · 소득세법 제59조의3 · 낼 세금이 그보다 적으면 덜 돌려받음', fontproperties=Bs(11), color=SUB)
plt.subplots_adjust(left=0.24, right=0.97, top=0.86, bottom=0.2)
fig.savefig('pkg/img/01.png'); plt.close(fig)
# 02: 매달 75만원 vs 12월 말 900만원 — 공제(같음)+이자(다름)
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, it) in enumerate([('매달 75만원씩', 16.0), ('12월 말 한 번에', 0.0)]):
    y = 1 - i
    ax.barh(y, 148.5, color=ORG, height=0.5)
    ax.text(74, y, '세금 공제 148만 5천원', ha='center', va='center', fontproperties=Bs(16), color='white')
    if it:
        ax.barh(y, it, left=148.5, color=BLU, height=0.5)
        ax.text(148.5 + it + 2, y, '+ 이자 약 16만원', va='center', fontproperties=Bs(17), color=BLU)
    else:
        ax.text(150.5, y, '+ 이자 거의 0원', va='center', fontproperties=Bs(17), color=SUB)
ax.set_yticks([0, 1]); ax.set_yticklabels(['12월 말 한 번에', '매달 75만원씩'], fontproperties=Bs(17), color=INK)
ax.set_xlim(0, 215); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.spines['left'].set_color(LG)
fig.suptitle('900만원 넣었을 때, 달라지는 건 이자뿐', fontproperties=Bs(23), color=INK, x=0.04, ha='left', y=0.96)
fig.text(0.04, 0.03, '공제율 16.5% · 정기예금 12개월 기본금리 중앙 연 3.29%(금감원 10월 공시 40개) 단리 · 직접 계산', fontproperties=Bs(11), color=SUB)
plt.subplots_adjust(left=0.24, right=0.97, top=0.86, bottom=0.14)
fig.savefig('pkg/img/02.png'); plt.close(fig)
print('ok')
