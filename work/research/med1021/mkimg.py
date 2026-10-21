# med1021 그림 3장 — 숫자는 calc.py(소득세법 59조의4②·시행령 118조의5, 총급여 5,000만원 예시)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, NAVY, INK, SUB, GRY = '#EA580C', '#1E3A8A', '#111827', '#4B5563', '#9CA3AF'
def won(v):
    m, k = divmod(int(v), 10000); return f'{m}만 {k:,}원' if k else f'{m}만원'
# 00 표지 1080x1080 — 큰 글 두 줄 + 막대 둘(65세 이상 vs 미만)
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.875, '부모님 병원비 1,000만원 냈다면', fontsize=52, fontproperties=B, color=INK)
fig.text(0.06, 0.765, '세금 127만 5천원 줄어요', fontsize=66, fontproperties=B, color=ORG)
fig.text(0.06, 0.715, '총급여 5,000만원 · 실손보험금 없음 · 의료비 세액공제 15%', fontsize=21, color=SUB)
ax = fig.add_axes([0.08, 0.17, 0.86, 0.47])
vals = [('부모님 65세 이상\n(700만원 한도 없음)', 1275000, ORG), ('부모님 65세 미만\n(700만원 한도)', 1050000, NAVY)]
for i, (n, v, c) in enumerate(vals):
    ax.bar(i, v, width=0.55, color=c)
    ax.text(i, v + 40000, won(v), ha='center', fontsize=36, fontproperties=B, color=INK)
ax.set_xticks([0, 1]); ax.set_xticklabels([v[0] for v in vals], fontproperties=Bs(26))
ax.set_ylim(0, 1550000); ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.06, 0.03, '소득세법 제59조의4 제2항 · 파이어맵 계산(낸 세금 안에서만 줄어듦)', fontsize=16, color='#6B7280')
fig.savefig('pkg/img/00.png', dpi=100); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080); plt.close(fig)
# 01 실손보험금을 받으면
fig, ax = plt.subplots(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
vals = [('실손보험금 없음', 1275000, ORG), ('실손보험금 400만원 받음', 675000, NAVY)]
for i, (n, v, c) in enumerate(vals[::-1]):
    ax.barh(i, v, height=0.5, color=c)
    ax.text(v + 20000, i, won(v), va='center', fontsize=26, fontproperties=B, color=INK)
    ax.text(15000, i + 0.4, n, va='center', fontsize=19, fontproperties=B, color=INK)
ax.set_xlim(0, 1800000); ax.set_ylim(-0.6, 1.9); ax.axis('off')
fig.text(0.05, 0.92, '부모님(70세) 병원비 1,000만원일 때 줄어드는 세금', fontsize=24, fontproperties=B, color=INK)
fig.text(0.05, 0.86, '실손보험금으로 돌려받은 돈은 의료비에서 빼요', fontsize=19, color=SUB)
fig.text(0.05, 0.03, '소득세법 시행령 제118조의5 제1항 · 총급여 5,000만원 · 파이어맵 계산', fontsize=12, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 총급여별 문턱(3%)
pts = [('3,000만원', 900000), ('5,000만원', 1500000), ('7,000만원', 2100000), ('1억원', 3000000)]
fig, ax = plt.subplots(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
for i, (n, v) in enumerate(pts):
    ax.bar(i, v, width=0.6, color=ORG if i == 1 else NAVY)
    ax.text(i, v + 60000, won(v), ha='center', fontsize=22, fontproperties=B, color=INK)
ax.set_xticks(range(4)); ax.set_xticklabels([p[0] for p in pts], fontproperties=Bs(20))
ax.set_ylim(0, 3600000); ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.92, '총급여별로 이만큼은 넘어야 공제가 시작돼요', fontsize=24, fontproperties=B, color=INK)
fig.text(0.05, 0.86, '한 해 의료비 합계가 총급여의 3%를 넘는 부분부터', fontsize=19, color=SUB)
fig.text(0.05, 0.02, '소득세법 제59조의4 제2항 제1호 · 파이어맵 계산', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.14)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
