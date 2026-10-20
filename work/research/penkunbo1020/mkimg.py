# penkunbo1020 그림 3장 — 숫자는 calc.py(2026 법령 원문 식)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
def won(v):
    m, r = divmod(v, 10000)
    return f'{m}만 {r:,}원' if r else f'{m}만원'
ORG, NAVY, INK, SUB = '#EA580C', '#1E3A8A', '#111827', '#4B5563'
steps = [('연금 없음', 45050), ('월 30만원', 57250), ('월 50만원', 65390), ('월 100만원', 67850), ('월 150만원', 67860), ('월 200만원', 67850)]
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.87, '이자·배당 1천만원 넘으면', fontsize=46, fontproperties=B, color=INK)
fig.text(0.05, 0.76, '건보료 월 6만 7천원 더', fontsize=56, fontproperties=B, color=ORG)
fig.text(0.05, 0.70, '국민연금 월액별 · 지역가입자 1명 · 2026년', fontsize=20, color=SUB)
ax = fig.add_axes([0.27, 0.08, 0.66, 0.56])
for i, (n, v) in enumerate(steps[::-1]):
    ax.barh(i, v, height=0.62, color=ORG if v > 67000 else NAVY)
    ax.text(v + 1200, i, won(v), va='center', fontsize=22, fontproperties=B, color=INK)
    ax.text(-1500, i, n, ha='right', va='center', fontsize=21, fontproperties=B, color=INK)
ax.set_xlim(0, 100000); ax.axis('off')
fig.text(0.05, 0.02, '1,000만원 → 1,001만원일 때 오르는 월 보험료(장기요양 포함) · 재산 0 가정 · 파이어맵 계산', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/00.png', dpi=100); fig.savefig('pkg/cover_100.png', dpi=11); plt.close(fig)
# 01 연금 150만원 예
fig, ax = plt.subplots(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
vals = [('이자·배당 1,000만원', 61000), ('이자·배당 1,001만원', 128860)]
for i, (n, v) in enumerate(vals[::-1]):
    ax.barh(i, v, height=0.55, color=ORG if v > 100000 else NAVY)
    ax.text(v + 2000, i, '월 '+won(v), va='center', fontsize=24, fontproperties=B, color=INK)
    ax.text(2000, i + 0.42, n, va='center', fontsize=19, fontproperties=B, color=INK)
ax.set_xlim(0, 175000); ax.set_ylim(-0.6, 1.9); ax.axis('off')
fig.text(0.05, 0.92, '국민연금 월 150만원 받는 지역가입자', fontsize=26, fontproperties=B, color=INK)
fig.text(0.05, 0.86, '이자·배당 1만원 차이로 월 6만 7,860원 · 1년 약 81만원 더', fontsize=17, color=SUB)
fig.text(0.05, 0.03, '건보료+장기요양 · 재산 0 · 2026년 · 파이어맵 계산', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 연금 적을 때 3칸 표
rows = [('연금 없음', '2만 2,800원', '+4만 5,050원'), ('월 30만원', '2만 2,800원', '+5만 7,250원'), ('월 50만원', '2만 2,800원', '+6만 5,390원'), ('월 70만원', '2만 8,460원', '+6만 7,860원'), ('월 150만원', '6만 1,000원', '+6만 7,860원')]
fig = plt.figure(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.91, '연금이 월 56만원 이하면 오르는 폭이 작아요', fontsize=25, fontproperties=B, color=INK)
fig.text(0.05, 0.85, '연금만 있을 땐 보험료 하한(월 2만 160원)에 머물러서', fontsize=16, color=SUB)
hdr = ('국민연금', '1,000만원일 때', '1,001만원이면 더')
xs = [0.07, 0.38, 0.68]; y = 0.74
for x, h in zip(xs, hdr): fig.text(x, y, h, fontsize=18, fontproperties=B, color=SUB)
for r in rows:
    y -= 0.12
    for j, (x, c) in enumerate(zip(xs, r)):
        fig.text(x, y, c, fontsize=22, fontproperties=B, color=ORG if j == 2 else INK)
fig.text(0.05, 0.03, '월 보험료(장기요양 포함) · 재산 0 · 2026년 · 파이어맵 계산', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
