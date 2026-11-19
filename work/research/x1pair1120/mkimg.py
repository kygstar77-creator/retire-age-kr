# x1pair1120 그림 2장 — 숫자는 calc_out.txt(ECOS 매매기준율·야후 SPY 종가, 끝날 2026-11-18)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, LINE, BLU = '#EA580C', '#111827', '#4B5563', '#E5E7EB', '#2563EB'
# 01 식 카드
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=100); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
ax.text(0.3, 5.3, '본전 환율 셈하는 법', fontproperties=Bs(26), color=INK, va='center')
ax.text(0.3, 4.1, '산 날 환율  ÷  (지금 주가 ÷ 산 날 주가)', fontproperties=Bs(25), color=ORG, va='center')
ax.plot([0.3, 9.7], [3.3, 3.3], color=LINE, lw=1.5)
ax.text(0.3, 2.6, '예) 1,450원에 샀고 앱 달러 수익률이 +16%라면', fontproperties=Bs(19), color=INK, va='center')
ax.text(0.3, 1.6, '1,450 ÷ 1.16 = 1,250원', fontproperties=Bs(25), color=INK, va='center')
ax.text(0.3, 0.75, '환율이 1,250원까지 내려와도 원화로 본전(주가가 그대로일 때)', fontproperties=Bs(15), color=SUB, va='center')
fig.text(0.02, 0.02, '배당·환전 수수료 빼고 가격만 · 1,450원은 예로 든 값', fontsize=10.5, color=SUB)
plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.07); plt.savefig('pkg/img/01.png'); plt.close()
# 02 매달 첫 거래일 표 3칸
rows = [('2025년 11월 3일', '1,427원', '1,336원', '+0.2%'), ('12월 1일', '1,466원', '1,366원', '-2.0%'), ('2026년 1월 2일', '1,435원', '1,343원', '-0.3%'),
        ('2월 2일', '1,437원', '1,368원', '-2.2%'), ('3월 3일', '1,435원', '1,337원', '+0.1%'), ('4월 1일', '1,531원', '1,373원', '-2.5%'),
        ('5월 4일', '1,485원', '1,460원', '-8.3%'), ('6월 1일', '1,503원', '1,562원', '-14.3%'), ('7월 1일', '1,548원', '1,581원', '-15.3%'),
        ('8월 3일', '1,434원', '1,488원', '-10.0%'), ('9월 1일', '1,374원', '1,433원', '-6.6%'), ('10월 1일', '1,356원', '1,418원', '-5.6%'),
        ('11월 2일', '1,337원', '1,377원', '-2.8%')]
n = len(rows)
fig, ax = plt.subplots(figsize=(10, 10.4), dpi=100); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, n + 2.4)
ax.text(0, n + 1.9, '그날 SPY를 샀다면, 본전 환율은', fontproperties=Bs(24), color=INK, va='center')
hy = n + 0.9
for x, h in [(0.2, '산 날'), (4.0, '산 날 환율'), (6.0, '본전 환율'), (8.2, '원화 손익')]:
    ax.text(x, hy, h, fontproperties=Bs(16), color=SUB, va='center')
for i, (d, a, b, c) in enumerate(rows):
    y = n - 1 - i + 0.35
    ax.plot([0, 10], [y - 0.5, y - 0.5], color=LINE, lw=1)
    col = BLU if c.startswith('+') else ORG
    ax.text(0.2, y, d, fontproperties=Bs(17), color=INK, va='center')
    ax.text(4.0, y, a, fontproperties=Bs(17), color=SUB, va='center')
    ax.text(6.0, y, b, fontproperties=Bs(18), color=INK, va='center')
    ax.text(8.2, y, c, fontproperties=Bs(18), color=col, va='center')
fig.text(0.02, 0.04, '11월 18일 환율 1,338.8원·SPY 종가로 셈 · 13번 중 11번 원화 손해 · 배당·환전 수수료 빼고 가격만', fontsize=10.5, color=SUB)
fig.text(0.02, 0.012, '자료: 한국은행 경제통계시스템 원/달러 매매기준율 · 야후 파이낸스 SPY 종가 · 매달 첫 거래일', fontsize=10, color=SUB)
plt.subplots_adjust(left=0.03, right=0.98, top=0.98, bottom=0.07); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
