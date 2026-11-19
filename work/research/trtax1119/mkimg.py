# trtax1119 그림 2장 — 숫자는 calc_out.txt(시행령 5조·농특세법 5조 세율, 1천만원 같은 값 사고팔기 가정)
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
# 01: 1천만원 한 번 팔 때 세금, 작년 vs 올해
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
rows = [('코스피', 1.5, 2.0), ('코스닥', 1.5, 2.0)]
for i, (n, a, b) in enumerate(rows):
    y = 1 - i
    ax.barh(y + 0.18, a, color=LG, height=0.32); ax.text(a + 0.04, y + 0.18, f'작년 1만 5천원', va='center', fontproperties=Bs(15), color=SUB)
    ax.barh(y - 0.18, b, color=ORG, height=0.32); ax.text(b + 0.04, y - 0.18, f'올해 2만원', va='center', fontproperties=Bs(17), color=ORG)
ax.set_yticks([0, 1]); ax.set_yticklabels(['코스닥', '코스피'], fontproperties=Bs(18), color=INK)
ax.set_xlim(0, 2.9); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.spines['left'].set_color(LG)
fig.suptitle('1천만원어치 한 번 팔 때 빠지는 세금', fontproperties=Bs(23), color=INK, x=0.04, ha='left', y=0.96)
fig.text(0.04, 0.10, '코스피 = 증권거래세 0.05% + 농어촌특별세 0.15% · 코스닥 = 0.20%', fontproperties=Bs(14), color=BLU)
fig.text(0.04, 0.03, '2026년 1월 1일 판 것부터 · 증권거래세법 시행령 제5조 · 농어촌특별세법 제5조', fontproperties=Bs(11), color=SUB)
plt.subplots_adjust(left=0.16, right=0.97, top=0.86, bottom=0.2)
fig.savefig('pkg/img/01.png'); plt.close(fig)
# 02: 사고파는 횟수별 1년 세금
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
rows = [('1년에 한 번', 2, '2만원 (원금의 0.2%)'), ('한 달에 한 번', 24, '24만원 (2.4%)'), ('일주일에 한 번', 104, '104만원 (10.4%)')]
for i, (n, v, lab) in enumerate(rows):
    ax.barh(2 - i, v, color=ORG if v > 50 else '#F59E0B', height=0.55)
    ax.text(v + 2, 2 - i, lab, va='center', fontproperties=Bs(18), color=INK)
ax.set_yticks(range(3)); ax.set_yticklabels([r[0] for r in rows][::-1], fontproperties=Bs(17), color=INK)
ax.set_xlim(0, 160); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.spines['left'].set_color(LG)
fig.suptitle('1천만원으로 1년 사고팔면 거래세만', fontproperties=Bs(23), color=INK, x=0.04, ha='left', y=0.96)
fig.text(0.04, 0.10, '작년 세율이었다면 일주일에 한 번 = 78만원', fontproperties=Bs(14), color=BLU)
fig.text(0.04, 0.03, '세율 0.20% · 같은 값에 사고판다고 가정 · 증권사 수수료 뺌 · 직접 계산', fontproperties=Bs(11), color=SUB)
plt.subplots_adjust(left=0.22, right=0.97, top=0.86, bottom=0.2)
fig.savefig('pkg/img/02.png'); plt.close(fig)
print('ok')
