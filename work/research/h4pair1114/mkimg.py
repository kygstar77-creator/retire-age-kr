# h4pair1114 그림 2장 — 숫자는 calc_out_1112.txt(국토부 실거래 11/12 받음)
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
def eok(v):
    a = int(v); r = round((v - a) * 10000)
    return f'{a}억 {r:,}만' if r else f'{a}억'
# 01 광명 앞뒤 — 26곳 중 13~26번째
rows = [('종로구', 12.00), ('양천구', 12.00), ('강서구', 11.00), ('성북구', 10.00), ('광명시', 9.78), ('관악구', 9.47), ('은평구', 9.40), ('구로구', 8.30), ('노원구', 8.20), ('강북구', 8.18), ('중랑구', 8.07), ('금천구', 7.12), ('도봉구', 6.20)]
fig, ax = plt.subplots(figsize=(9, 8), dpi=100)
for i, (n, v) in enumerate(rows):
    c = ORG if n == '광명시' else (BLU if i > 4 else LG)
    ax.barh(i, v, color=c, height=0.62)
    ax.text(v + 0.15, i, eok(v), va='center', fontproperties=Bs(14), color=ORG if n == '광명시' else INK)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([f'{14 + i}. {r[0]}' for i, r in enumerate(rows)], fontproperties=Bs(14))
ax.invert_yaxis(); ax.set_xlim(0, 14.5); ax.set_xticks([])
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
fig.text(0.04, 0.95, '광명은 26곳 중 18번째 — 아래 파란 8곳이 광명보다 낮은 서울 구', fontproperties=Bs(17), color=INK)
fig.text(0.04, 0.915, '84㎡대(전용 80~85㎡) 매매 가운데 값 · 2026년 7~9월 계약 · 14~26번째만 (1위 강남구 30억)', fontsize=11.5, color=SUB)
fig.text(0.04, 0.02, '국토교통부 실거래 신고 2026.11.12 받음 · 해제 거래·공공기관 매수 제외 · 파이어맵 계산', fontsize=10.5, color='#6B7280')
fig.subplots_adjust(top=0.89, bottom=0.07, left=0.2, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 철산동 단지 사다리 + 새 단지 전세 선
L = [('철산역롯데캐슬&SKVIEW (2022)', 15.95), ('철산센트럴푸르지오 (2021)', 15.20), ('주공13 (1986)', 13.90), ('철산래미안자이 (2009)', 13.47), ('주공12 (1986)', 13.30), ('철산푸르지오하늘채 (2010)', 12.90), ('광명푸르지오 (2007)', 10.00), ('브라운스톤2차 (2007)', 9.40), ('브라운스톤 (2006)', 9.39), ('쌍마한신 (1992)', 8.90), ('도덕파크타운1단지 (2002)', 8.48), ('두산위브 (2007)', 8.08), ('우성 (1990)', 7.25), ('롯데낙천대 (2005)', 7.10), ('광복현대 (1998)', 6.76), ('철산리버빌주공 (2001)', 6.35)]
fig, ax = plt.subplots(figsize=(9, 9.5), dpi=100)
for i, (n, v) in enumerate(L):
    c = BLU if v <= 8.70 else LG
    ax.barh(i, v, color=c, height=0.62)
    ax.text(max(v, 8.70) + 0.15, i, eok(v), va='center', fontproperties=Bs(13), color=INK, zorder=5)
ax.axvline(8.70, color=ORG, lw=2.2, ls='--')
ax.text(8.75, -1.0, '새 단지 전세 8억 7,000만', color=ORG, fontproperties=Bs(13))
ax.set_yticks(range(len(L))); ax.set_yticklabels([r[0] for r in L], fontproperties=Bs(12.5))
ax.invert_yaxis(); ax.set_ylim(len(L) - 0.5, -1.6); ax.set_xlim(0, 18.5); ax.set_xticks([])
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
fig.text(0.04, 0.955, '철산동 84㎡대 단지별 매매 가운데 값 (1년)', fontproperties=Bs(18), color=INK)
fig.text(0.04, 0.925, '파란 6곳은 매매가 철산자이더헤리티지(2025 입주) 신규 전세보다 낮아요', fontsize=12, color=SUB)
fig.text(0.04, 0.015, '국토교통부 실거래 2025.11~2026.10 계약 · 5건 이상 거래된 16단지 · 2026.11.12 받음', fontsize=10.5, color='#6B7280')
fig.subplots_adjust(top=0.9, bottom=0.05, left=0.33, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
