# cudep1020 그림 3장 — 숫자는 calc.py(조특법 89조의3·농특세법 5조·소득세법 129조)와 finlife 9월 공시
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
ORG, NAVY, GRAY, INK, SUB = '#EA580C', '#1E3A8A', '#9CA3AF', '#111827', '#4B5563'
def won(v):
    m, r = divmod(v, 10000)
    return f'{m}만 {r:,}원' if r else f'{m}만원'
# 00 표지 — 3천만원 4.4% 1년 세후 이자
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.87, '신협 특판 4.4% 비과세면', fontsize=48, fontproperties=B, color=INK)
fig.text(0.05, 0.76, '은행 예금 5.13%와 같아요', fontsize=54, fontproperties=B, color=ORG)
fig.text(0.05, 0.70, '3천만원 · 1년 · 손에 남는 이자 · 2026년 세법', fontsize=20, color=SUB)
rows = [('은행 예금 4.4%\n(15.4% 뗌)', 1116720, NAVY), ('조합 · 소득 기준 넘음\n(5.9% 뗌)', 1242120, NAVY), ('조합 비과세\n(1.4%만 뗌)', 1301520, ORG)]
ax = fig.add_axes([0.38, 0.08, 0.58, 0.56])
for i, (n, v, c) in enumerate(rows):
    ax.barh(i, v, height=0.6, color=c)
    ax.text(v - 20000, i, won(v), ha='right', va='center', fontsize=22, fontproperties=B, color='white')
    ax.text(-30000, i, n, ha='right', va='center', fontsize=19, fontproperties=B, color=INK)
ax.set_xlim(0, 1350000); ax.axis('off')
fig.text(0.05, 0.02, '세전 이자 132만원 기준 · 농어촌특별세 포함 · 파이어맵 계산', fontsize=12, color='#6B7280')
fig.savefig('pkg/img/00.png', dpi=100); fig.savefig('pkg/cover_100.png', dpi=11); plt.close(fig)
# 01 은행으로 치면 몇 %
fig, ax = plt.subplots(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
vals = [('조합 4.4% 비과세', 5.13, ORG), ('조합 4.4% · 2026년 5.9%', 4.89, NAVY), ('조합 4.4% · 2027년 9.5%', 4.71, NAVY), ('은행 기본금리 최고(9월)', 3.92, GRAY)]
for i, (n, v, c) in enumerate(vals[::-1]):
    ax.barh(i, v, height=0.55, color=c)
    ax.text(v + 0.06, i, f'연 {v:.2f}%', va='center', fontsize=24, fontproperties=B, color=INK)
    ax.text(0.08, i + 0.42, n, va='center', fontsize=18, fontproperties=B, color=INK)
ax.set_xlim(0, 6.6); ax.set_ylim(-0.6, 3.9); ax.axis('off')
fig.text(0.05, 0.92, '은행 예금으로 치면 몇 %일까', fontsize=28, fontproperties=B, color=INK)
fig.text(0.05, 0.86, '은행에서 15.4%를 떼고도 같은 이자가 남는 금리', fontsize=17, color=SUB)
fig.text(0.05, 0.03, '은행 금리: 금융감독원 비교공시 2026년 9월 · 12개월 단리 38개 · 파이어맵 계산', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 누가 얼마 내나 3칸 표
rows = [('2025년까지 가입', '1.4%', '연 5.13%'), ('농축협·수협·산림 조합원', '1.4%', '연 5.13%'), ('총급여 7천·종합소득 6천↓', '1.4%', '연 5.13%'), ('소득 기준 넘음(2026년 가입)', '5.9%', '연 4.89%'), ('소득 기준 넘음(2027년 가입~)', '9.5%', '연 4.71%')]
fig = plt.figure(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.91, '2026년부터는 소득에 따라 세금이 갈려요', fontsize=26, fontproperties=B, color=INK)
fig.text(0.05, 0.85, '조합 예탁금 1인 3천만원까지 · 연 4.4% 예시', fontsize=16, color=SUB)
hdr = ('누구', '떼는 세금', '은행으로 치면')
xs = [0.06, 0.55, 0.75]; y = 0.74
for x, h in zip(xs, hdr): fig.text(x, y, h, fontsize=18, fontproperties=B, color=SUB)
for r in rows:
    y -= 0.12
    for j, (x, c) in enumerate(zip(xs, r)):
        fig.text(x, y, c, fontsize=21, fontproperties=B, color=ORG if j == 2 else INK)
fig.text(0.05, 0.03, '소득은 전년도 기준(총급여 7천만원·종합소득금액 6천만원) · 조세특례제한법 제89조의3 · 파이어맵 계산', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
