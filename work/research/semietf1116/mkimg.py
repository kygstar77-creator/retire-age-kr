# semietf1116 그림 2장 — 숫자는 calc_out.txt(FunETF NAV 26.11.13·구성종목 PDF)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
from decimal import Decimal as D, ROUND_HALF_UP
def f1(x): return str(D(str(x)).quantize(D('0.1'),rounding=ROUND_HALF_UP))
ORG, INK, SUB, BLU, LG = '#EA580C', '#111827', '#4B5563', '#2563EB', '#CBD5E1'
rows = [ # 이름, 두 종목 합, 3개월, 1개월
('KODEX AI반도체TOP2플러스',51.8,-28.25,-19.02),('HANARO Fn K-반도체',52.7,-27.51,-19.62),('SOL AI반도체TOP2플러스',54.2,-26.71,-21.21),
('TIGER 반도체TOP10',53.2,-22.61,-17.34),('ACE AI반도체TOP3+',49.9,-22.09,-21.04),('TIGER 반도체',37.0,-20.93,-26.05),
('KODEX 반도체',37.0,-20.52,-26.01),('SOL AI반도체소부장',0,-15.34,-30.18),('KODEX AI반도체핵심장비',0,-10.33,-27.91)]
def col(s): return ORG if s > 45 else (BLU if s > 30 else '#059669')
fig, (a, b) = plt.subplots(1, 2, figsize=(10, 6.4), dpi=100, sharey=True)
for i, (n, s, r3, r1) in enumerate(rows):
    y = len(rows) - 1 - i; c = col(s)
    a.barh(y, -r3, color=c, height=0.62); a.text(-r3 + 0.5, y, f'{f1(r3)}%', va='center', fontproperties=Bs(13), color=c)
    b.barh(y, -r1, color=c, height=0.62); b.text(-r1 + 0.5, y, f'{f1(r1)}%', va='center', fontproperties=Bs(13), color=c)
a.set_yticks(range(len(rows))); a.set_yticklabels([r[0] for r in rows][::-1], fontproperties=Bs(12), color=INK)
for ax, t in ((a, '석 달(8/13~11/13)'), (b, '한 달(10/13~11/13)')):
    ax.set_xlim(0, 37); ax.set_xticks([]); [ax.spines[s].set_visible(False) for s in ['top', 'right', 'bottom']]
    ax.set_title(t, fontproperties=Bs(17), color=INK, loc='left', pad=10)
fig.suptitle('같은 반도체 ETF, 기간을 바꾸면 순서가 뒤집혔다', fontproperties=Bs(20), color=INK, x=0.02, ha='left')
fig.text(0.01, 0.045, '주황: 삼성전자·SK하이닉스 합 50% 안팎   파랑: 37%   초록: 0%(소부장)', fontproperties=Bs(11), color=SUB)
fig.text(0.01, 0.01, '하락폭 · 분배금 재투자 기준가(NAV) 2026.11.13 기준 · 자료: FunETF(운용사 공시)', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.07, 1, 0.93)); plt.savefig('pkg/img/01.png'); plt.close()
# 02: 담은 종목 — 삼성전자·SK하이닉스·나머지
hold = [('SOL AI반도체TOP2플러스',27.9,26.3),('TIGER 반도체TOP10',27.4,25.8),('HANARO Fn K-반도체',27.6,25.1),('KODEX AI반도체TOP2플러스',28.0,23.8),
('ACE AI반도체TOP3+',26.6,23.3),('KODEX 반도체',19.7,17.3),('TIGER 반도체',19.7,17.3),('SOL AI반도체소부장',0,0),('KODEX AI반도체핵심장비',0,0)]
fig, ax = plt.subplots(figsize=(10, 6.2), dpi=100)
for i, (n, s, h) in enumerate(hold):
    y = len(hold) - 1 - i
    ax.barh(y, s, color=ORG, height=0.62); ax.barh(y, h, left=s, color='#FB923C', height=0.62); ax.barh(y, 100 - s - h, left=s + h, color=LG, height=0.62)
    ax.text(s + h + 1.2 if s + h else 1.2, y, f'{s+h:.1f}%' if s + h else '0% — 장비·부품 회사', va='center', fontproperties=Bs(13), color=INK)
ax.set_yticks(range(len(hold))); ax.set_yticklabels([r[0] for r in hold][::-1], fontproperties=Bs(12), color=INK)
ax.set_xlim(0, 100); ax.set_xticks([]); [ax.spines[s].set_visible(False) for s in ['top', 'right', 'bottom']]
ax.set_title('삼성전자·SK하이닉스를 얼마나 담았나', fontproperties=Bs(20), color=INK, loc='left', pad=14)
fig.text(0.01, 0.045, '진한 주황: 삼성전자   연한 주황: SK하이닉스   회색: 나머지 종목', fontproperties=Bs(11), color=SUB)
fig.text(0.01, 0.01, '구성종목(PDF) 비중 · 2026.11.13 종가 기준 화면(11/15 조회) · 자료: FunETF(운용사 공시)', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.07, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
