# rcut1116 그림 2장 — 숫자는 calc_out.txt(은행연합회 금리인하요구권 비교공시)
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
# 01: 5대 은행 신용 vs 주담 인하폭
rows = [('KB국민', 0.40, 0.06), ('신한', 0.46, 0.03), ('하나', 0.75, 0.04), ('우리', 0.27, 0.04), ('NH농협', 0.48, 0.04)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, s, h) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.barh(y + 0.18, s, color=BLU, height=0.34); ax.text(s + 0.01, y + 0.18, f'{s:.2f}%p', va='center', fontproperties=Bs(15), color=BLU)
    ax.barh(y - 0.18, h, color=ORG, height=0.34); ax.text(h + 0.01, y - 0.18, f'{h:.2f}%p', va='center', fontproperties=Bs(15), color=ORG)
ax.set_yticks(range(5)); ax.set_yticklabels([r[0] for r in rows][::-1], fontproperties=Bs(16), color=INK)
ax.set_xlim(0, 0.9); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.spines['left'].set_color(LG)
fig.suptitle('받아들여지면 몇 %p 깎였나', fontproperties=Bs(24), color=INK, x=0.04, ha='left', y=0.97)
fig.text(0.04, 0.845, '■', fontproperties=Bs(15), color=BLU); fig.text(0.07, 0.845, '신용대출', fontproperties=Bs(15), color=SUB); fig.text(0.20, 0.845, '■', fontproperties=Bs(15), color=ORG); fig.text(0.23, 0.845, '주택담보대출', fontproperties=Bs(15), color=SUB)
fig.text(0.04, 0.03, '은행연합회 금리인하요구권 비교공시 · 2026년 상반기 가계대출 · 인하금리(잔액 가중평균)', fontproperties=Bs(11), color=SUB)
plt.subplots_adjust(left=0.15, right=0.96, top=0.79, bottom=0.1)
fig.savefig('pkg/img/01.png'); plt.close(fig)
# 02: 반기별 신청 건수·수용률
per = [('2025년 상반기', 163.8, 28.8), ('2025년 하반기', 151.3, 27.6), ('2026년 상반기', 267.9, 19.1)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, a, r) in enumerate(per):
    c = ORG if i == 2 else LG
    ax.bar(i, a, color=c, width=0.55)
    ax.text(i, a + 6, f'{a:.0f}만 건', ha='center', fontproperties=Bs(17), color=INK)
    ax.text(i, a / 2, f'받아들여진\n비율 {r}%', ha='center', va='center', fontproperties=Bs(17), color='white' if i == 2 else INK)
ax.set_xticks(range(3)); ax.set_xticklabels([p[0] for p in per], fontproperties=Bs(15), color=INK)
ax.set_ylim(0, 310); ax.set_yticks([])
for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(LG)
fig.suptitle('신청은 늘고, 받아들여진 비율은 줄었어요', fontproperties=Bs(24), color=INK, x=0.04, ha='left', y=0.97)
fig.text(0.04, 0.015, '은행연합회 금리인하요구권 비교공시 · 은행 19곳 가계+기업 합계(직접 합산)', fontproperties=Bs(11), color=SUB)
plt.subplots_adjust(left=0.06, right=0.96, top=0.85, bottom=0.16)
fig.savefig('pkg/img/02.png'); plt.close(fig)
print('ok')
