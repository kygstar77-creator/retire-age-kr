# newold1112 그림 2장 — 01 서울 84㎡ 안팎 연식별 중간값(calc_out.txt) 02 같은 동 안 신축 vs 21~30년(calc2_out.txt)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, LBLUE, INK, GR, SUBC, ORG = '#1D4ED8', '#93C5FD', '#111827', '#CBD5E1', '#6B7280', '#EA580C'
# 01
lab = ['5년 이내', '6~10년', '11~20년', '21~30년', '31년 이상']
val = [17.30, 15.34, 12.15, 9.15, 9.03]; cnt = [153, 312, 799, 1470, 624]
fig, ax = plt.subplots(figsize=(9, 6.2), dpi=100)
ys = list(range(len(lab)))[::-1]
ax.barh(ys, val, color=[ORG, LBLUE, LBLUE, BLUE, LBLUE], height=0.6)
for y, v, c in zip(ys, val, cnt): ax.text(v + 0.3, y, f'약 {v:.1f}억  ({c:,}건)', va='center', fontproperties=Bs(18), color=INK)
ax.set_yticks(ys); ax.set_yticklabels(lab, fontproperties=Bs(17))
ax.set_xlim(0, 25); ax.set_xticks([])
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.9, '서울 아파트 84㎡ 안팎, 지은 지 몇 년이냐에 따라', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.83, '매매가 중간값 · 2026년 8~10월 거래 3,358건', fontsize=16, color=SUBC)
fig.text(0.04, 0.03, '국토교통부 아파트 매매 실거래(서울 25개 구, 11/12 받음) · 전용 80~86㎡ · 해제 거래 뺌 · 구가 섞인 값이라 입지 차이가 들어 있음', fontsize=10, color=SUBC)
fig.subplots_adjust(top=0.78, bottom=0.12, left=0.20, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 같은 동(신축·21~30년 각 3건 이상, 합 10건 이상) 9곳
rows = [('노원구 상계동', 11.52, 7.20), ('은평구 응암동', 11.45, 6.90), ('은평구 수색동', 14.02, 8.80), ('동작구 신대방동', 14.10, 12.75),
        ('서대문구 홍제동', 16.90, 9.55), ('양천구 신정동', 19.00, 11.95), ('동대문구 전농동', 20.00, 12.40), ('동작구 사당동', 23.05, 14.70), ('강동구 둔촌동', 29.95, 10.70)]
fig, ax = plt.subplots(figsize=(9, 7.2), dpi=100)
ys = list(range(len(rows)))[::-1]
for y, (nm, a, b) in zip(ys, rows):
    ax.plot([b, a], [y, y], color=GR, lw=6, solid_capstyle='round', zorder=1)
    ax.scatter([b], [y], s=150, color=BLUE, zorder=2); ax.scatter([a], [y], s=150, color=ORG, zorder=2)
    ax.text(a + 0.6, y, f'+{a - b:.1f}억', va='center', fontproperties=Bs(16), color=INK)
ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows], fontproperties=Bs(15))
ax.set_xlim(4, 38); ax.set_xlabel('매매가 중간값(억원)', fontsize=13, color=SUBC)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.scatter([], [], s=120, color=ORG, label='5년 이내 신축'); ax.scatter([], [], s=120, color=BLUE, label='21~30년 구축')
ax.legend(frameon=False, fontsize=14, loc='upper right')
fig.text(0.04, 0.92, '같은 동 안에서 84㎡ 안팎끼리 비교하면', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.86, '신축이 보통 5억원쯤 더 비쌌어요(동 11곳 모두 신축이 비쌈)', fontsize=15, color=SUBC)
fig.text(0.04, 0.02, '국토교통부 아파트 매매 실거래 서울 2026년 8~10월 · 전용 80~86㎡ · 신축·구축 각 3건 이상인 동 11곳 중 거래 많은 9곳', fontsize=10, color=SUBC)
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.22, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
