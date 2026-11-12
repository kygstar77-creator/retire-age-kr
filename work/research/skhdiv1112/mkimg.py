# skhdiv1112 그림 2장 — 2026년 1주당 배당(DART 공시 4건)·1천만원/2천만원 넘는 주식 수(calc.py)
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
# 01 2026년에 받는 1주당 배당
rows = [('2025년 결산', 1875), ('1분기', 375), ('2분기', 375), ('3분기', 20000)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (lab, v) in enumerate(rows):
    ax.bar(i, v, color=ORG if v > 5000 else GR, width=0.6)
    ax.text(i, v + 400, f'{v:,}원', ha='center', fontproperties=Bs(17), color=ORG if v > 5000 else SUB)
    ax.text(i, -1400, lab, ha='center', fontsize=15, color=INK)
ax.set_xlim(-0.6, 3.6); ax.set_ylim(-2100, 23000); ax.axis('off')
fig.text(0.05, 0.9, 'SK하이닉스 2026년 1주당 배당 합계 22,625원', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.03, '금융감독원 DART 배당 결정 공시(2026.1.28·4.22·8.7·10.28) · 3분기는 실적 1만원+특별 1만원', fontsize=11.5, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.08, left=0.03, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 연 배당이 1천만원·2천만원을 넘는 주식 수
rows = [('1천만원', 3810, 442), ('2천만원', 7620, 884)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
y = 3.0
for lab, before, now in rows:
    ax.text(-150, y + 0.05, f'연 {lab} 넘는', ha='right', va='center', fontproperties=Bs(16), color=INK)
    ax.barh(y + 0.35, before, color=GR, height=0.5); ax.text(before + 100, y + 0.35, f'3분기 없을 때 {before:,}주', va='center', fontsize=14, color=SUB)
    ax.barh(y - 0.3, now, color=ORG, height=0.5); ax.text(now + 100, y - 0.3, f'지금 {now:,}주', va='center', fontproperties=Bs(16), color=ORG)
    y -= 1.9
ax.set_xlim(-3100, 11800); ax.set_ylim(0.3, 3.8); ax.axis('off')
fig.text(0.05, 0.9, 'SK하이닉스 배당만 있다면, 몇 주부터?', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.03, '2026년 1주당 22,625원(3분기 빼면 2,625원) · 소득세법 제14조·건보 시행규칙 제44조 · 직접 계산', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.08, left=0.03, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
