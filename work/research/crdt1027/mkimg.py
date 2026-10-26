# crdt1027 그림 3장 — 숫자는 calc.py(국민연금법 제18·19조 세 시기 판)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
BG, WH, LG = '#0F3B44', '#FFFFFF', '#CFE6EA'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.865, '출산크레딧 2027', fontproperties=Bs(76), color=WH)
fig.text(0.06, 0.765, '자녀 2명 24 → 27개월', fontproperties=Bs(54), color='#FB923C')
fig.text(0.06, 0.695, '인정받는 가입기간, 시기별 · 둘째 몫 12→15개월', fontsize=28, color=LG)
ax = fig.add_axes([0.06, 0.13, 0.88, 0.5]); ax.set_facecolor(BG)
bars = [('2025년 안\n첫째 얻음', 12), ('2026년 이후\n첫째 얻음', 24), ('2027년 1월 뒤\n둘째 얻음', 27)]
for i, (lab, v) in enumerate(bars):
    c = '#FB923C' if i == 2 else LG
    ax.bar(i, v, color=c, width=0.55)
    ax.text(i, v + 0.9, f'{v}개월', ha='center', fontproperties=Bs(30 if i == 2 else 26), color=c)
    ax.text(i, -1.2, lab, ha='center', va='top', fontsize=22, color=WH, linespacing=1.4)
ax.set_ylim(-9, 34); ax.set_xlim(-0.6, 2.6); ax.axis('off')
fig.text(0.06, 0.035, '국민연금법 제19조 · 법률 제22096호 부칙', fontsize=24, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 자녀 수별 세 시기
import numpy as np
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
data = {'자녀 1명': (0, 12, 12), '자녀 2명': (12, 24, 27), '자녀 3명': (30, 42, 45), '자녀 4명': (48, 60, 63)}
cols = [GR, '#F2B27A', ORG]; names = ['2025년 안 첫째', '2026년 이후 첫째', '2027년 1월 뒤 둘째']
x = np.arange(len(data)); w = 0.26
for k in range(3):
    vals = [v[k] for v in data.values()]
    ax.bar(x + (k - 1) * w, vals, w, color=cols[k], label=names[k])
    for xi, v in zip(x + (k - 1) * w, vals):
        ax.text(xi, v + 1, str(v), ha='center', fontsize=12, color=INK)
ax.set_xticks(x); ax.set_xticklabels(list(data.keys()), fontsize=15); ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=13, loc='upper left')
fig.text(0.05, 0.92, '자녀 수별 인정 가입기간(개월)', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.02, '국민연금법 제19조 세 시기 판 · 직접 계산(calc.py)', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.05, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 군 복무 크레딧
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
rows = [('2025년까지 전역', '6개월', 6), ('2026년 이후 전역', '복무기간, 최대 12개월', 12), ('2027년 1월 이후 전역', '복무기간 전부', 18)]
for i, (lab, t, n) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.barh(y, n, color=ORG if i == 2 else GR, height=0.55)
    ax.text(n + 0.5, y, t, va='center', fontproperties=Bs(16), color=INK)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=15)
ax.set_xticks([]); ax.set_xlim(0, 36)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.92, '군 복무 크레딧, 인정되는 기간', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.865, '막대 길이는 보기 위한 예시(복무 18개월일 때)', fontsize=14, color=SUB)
fig.text(0.05, 0.02, '국민연금법 제18조 세 시기 판', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.08, left=0.27)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
