# de1pair1117 그림 2장 — 숫자는 calc_out.txt(raw/ 2026-11-17 받음, 기준 11/13)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, LG, LINE = '#EA580C', '#111827', '#4B5563', '#94A3B8', '#E5E7EB'
rows = [('필수소비재', '20.4%', '20.1~20.2%'), ('헬스케어', '18.6%', '18.5%'), ('에너지', '15.1%', '14.9~15.0%'), ('IT', '12.1%', '12.4%'),
        ('산업재', '11.9%', '11.7%'), ('금융', '9.0%', '8.7%'), ('경기소비재', '7.0%', '7.0%'), ('통신', '5.8%', '5.8%')]
fig, ax = plt.subplots(figsize=(10, 7.6), dpi=100); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, len(rows) + 2.2)
ax.text(0, len(rows) + 1.75, '업종별로 담긴 돈의 비율', fontproperties=Bs(24), color=INK, va='center')
hy = len(rows) + 0.8
for x, h in [(0.2, '업종'), (4.2, 'SCHD'), (6.9, '국내 4종')]:
    ax.text(x, hy, h, fontproperties=Bs(17), color=SUB, va='center')
for i, (n, a, b) in enumerate(rows):
    y = len(rows) - 1 - i + 0.3; c = ORG if i < 3 else INK
    ax.plot([0, 10], [y - 0.5, y - 0.5], color=LINE, lw=1)
    ax.text(0.2, y, n, fontproperties=Bs(19), color=c, va='center')
    ax.text(4.2, y, a, fontproperties=Bs(19), color=INK, va='center')
    ax.text(6.9, y, b, fontproperties=Bs(19), color=INK, va='center')
fig.text(0.02, 0.045, '업종마다 SCHD와 국내 4종(TIGER·SOL·ACE·KODEX 미국배당다우존스) 차이 0.3%포인트 안 · 주황 세 업종 합 SCHD 54.1%', fontsize=10.5, color=SUB)
fig.text(0.02, 0.012, '자료: 찰스 슈왑 SCHD 보유 종목(2026-11-13)을 업종별로 더함 · 네이버 증권 ETF 분석(2026-11-13)', fontsize=10, color=SUB)
plt.subplots_adjust(left=0.03, right=0.98, top=0.97, bottom=0.08); plt.savefig('pkg/img/01.png'); plt.close()
r = [('ACE', 23.55), ('SOL', 23.37), ('TIGER', 23.42), ('KODEX', 23.74)]
fig, ax = plt.subplots(figsize=(10, 5.2), dpi=100)
for i, (n, v) in enumerate(r):
    y = len(r) - 1 - i
    ax.barh(y, v, color=ORG, height=0.6); ax.text(v + 0.3, y, f'{v:.1f}%', va='center', fontproperties=Bs(19), color=INK)
ax.set_yticks(range(len(r))); ax.set_yticklabels([s[0] for s in r][::-1], fontproperties=Bs(18), color=INK)
ax.set_xlim(0, 30); ax.set_xticks([]); [ax.spines[s].set_visible(False) for s in ['top', 'right', 'bottom']]
ax.set_title('국내 미국배당다우존스 4종, 최근 1년 수익률', fontproperties=Bs(21), color=INK, loc='left', pad=14)
fig.text(0.01, 0.04, '상품이 가진 주식의 가치로 잰 수익률 · 네 상품 차이 0.4%포인트 안', fontproperties=Bs(12), color=SUB)
fig.text(0.01, 0.005, '자료: 네이버 증권 ETF 분석(2026-11-13 기준)', fontsize=10, color=SUB)
plt.tight_layout(rect=(0, 0.07, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
