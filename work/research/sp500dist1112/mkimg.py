# sp500dist1112 그림 2장 — 숫자는 운용사 분배 기록(raw/kodex_divid_2ETFE4.json·ACE API·raw/tiger_click.txt)과 calc_out.txt
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
# 01 2026년 분배금 합계(원) 막대 + 오른쪽에 1년 수익률
rows = [('KODEX 미국S&P500', 486, '1.18%'), ('TIGER 미국S&P500', 253, '1.15%'), ('ACE 미국S&P500', 252, '1.17%')]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, v, r) in enumerate(rows[::-1]):
    c = ORG if v > 400 else BLU
    ax.barh(i, v, color=c, height=0.55)
    ax.text(v + 8, i, f'{v}원', va='center', ha='left', fontproperties=Bs(17), color=c)
    ax.text(700, i, r, va='center', ha='center', fontproperties=Bs(17), color=INK)
ax.text(700, 2.62, '1년 수익률', ha='center', fontproperties=Bs(13), color=SUB)
ax.text(0, 2.62, '2026년 분배금 합계(주당)', ha='left', fontproperties=Bs(13), color=SUB)
ax.set_yticks(range(3)); ax.set_yticklabels([r[0] for r in rows[::-1]], fontproperties=Bs(14))
ax.set_xlim(0, 780); ax.set_ylim(-0.5, 2.9); ax.set_xticks([])
for s in ('top', 'right', 'left', 'bottom'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
fig.text(0.04, 0.92, '분배금은 두 배, 1년 수익률은 거의 같아요', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.02, '각 운용사 분배금 기록·기준가격 1년 수익률(2026.11.11 기준, 분배금 재투자 가정)', fontsize=10.5, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.27, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 한눈에 — 세 칸
fig = plt.figure(figsize=(9, 5.6), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.88, 'KODEX 분배금이 큰 이유와 끝나는 때', fontproperties=Bs(22), color=INK)
L = [('2024년까지 펀드 안에 쌓아 둔 배당', '15번에 나눠 분기마다 약 0.27% 더 줘요'),
     ('나눠 주는 기간', '2025년 7월 ~ 2029년 1월 기준일'),
     ('끝난 뒤 KODEX 1년 분배율', '약 0.98% · TIGER·ACE와 비슷해져요')]
for i, (a, b) in enumerate(L):
    y = 0.68 - i * 0.22
    fig.patches.append(plt.Rectangle((0.05, y - 0.07), 0.9, 0.17, transform=fig.transFigure, color='#F3F4F6', zorder=0))
    fig.text(0.08, y + 0.035, a, fontproperties=Bs(15), color=SUB)
    fig.text(0.08, y - 0.035, b, fontproperties=Bs(18), color=ORG if i == 2 else INK)
fig.text(0.05, 0.03, '삼성자산운용 KODEX 미국대표지수 ETF 분배금 지급 정책 안내(2025.5.7) · 2026년 분배율로 계산', fontsize=10.5, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
