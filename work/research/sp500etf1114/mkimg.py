# sp500etf1114 그림 2장 — 숫자는 calc_out.txt(FunETF 11/12 기준 NAV 수익률·실부담비율, 운용사 API 대조)
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
# 01 3년 수익률(1억원이 3년 뒤 얼마) — 높은 순
rows = [('KODEX', 17852), ('RISE', 17846), ('TIGER', 17809), ('ACE', 17797), ('SOL', 17782)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, v) in enumerate(rows):
    c = BLU
    ax.barh(len(rows)-1-i, v - 17700, color=c, height=0.6, left=17700)
    ax.text(v + 4, len(rows)-1-i, f'1억 {v-10000:,}만원', va='center', fontproperties=Bs(15), color=c)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([n for n, _ in rows][::-1], fontproperties=Bs(16), color=INK)
ax.set_xlim(17700, 17960); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.set_title('1억원을 3년 넣었다면 지금 얼마', fontproperties=Bs(21), color=INK, loc='left', pad=14)
ax.text(17700, -0.95, '1등과 5등 차이 약 70만원 (3년 수익률 0.70%p)', fontproperties=Bs(14), color=SUB)
fig.text(0.01, 0.01, '2026년 11월 13일 기준 3년 기준가격 수익률(분배금 재투자·세전) · 자료: FunETF, 삼성·한국투자 운용사 공시 · 막대는 1억 7,700만원부터', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/01.png'); plt.close()
# 02 1억원 1년 비용: 총보수 vs 실부담비용
rows = [('ACE', 4700, 92200), ('TIGER', 6800, 93900), ('RISE', 4700, 97300), ('KODEX', 6200, 106700), ('SOL', 4700, 142400)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, a, b) in enumerate(rows):
    y = len(rows)-1-i
    ax.barh(y + 0.18, b, color=ORG, height=0.34); ax.barh(y - 0.18, a, color=LG, height=0.34)
    ax.text(b + 1500, y + 0.18, f'{b/10000:.1f}만원', va='center', fontproperties=Bs(14), color=ORG)
    ax.text(a + 1500, y - 0.18, f'{a:,}원', va='center', fontproperties=Bs(12), color=SUB)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([n for n, _, _ in rows][::-1], fontproperties=Bs(16), color=INK)
ax.set_xlim(0, 175000); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.set_title('1억원에 1년 드는 비용', fontproperties=Bs(21), color=INK, loc='left', pad=14)
ax.text(70000, 4.55, '주황 = 실부담비용  ·  회색 = 광고 속 총보수', fontproperties=Bs(13), color=SUB)
fig.text(0.01, 0.01, '2026년 11월 13일 기준 · 실부담비용 = 총보수 + 기타비용 + 매매·중개수수료 · 자료: FunETF 상품 정보', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
