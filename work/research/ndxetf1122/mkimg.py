# ndxetf1122 그림(tigerdj1122 틀) — 00 표지(네 곳 1억 결과), 01 해마다 수익, 02 1주 가격·분배금. 숫자는 calc_out.txt·calc2_out.txt 그대로
import os, json, glob
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Patch
import numpy as np
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG = '#111827', '#6B7280', '#EA580C'
SRC = '야후 파이낸스 일별 종가·분배(11/21 받음) · 미래에셋 분배금 현황 · 네이버페이 증권 · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 40
N = ['KODEX', 'RISE', 'ACE', 'TIGER']
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#3F1D0B')
fig.text(0.07, 0.86, '나스닥100 ETF 4종', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.785, '2021년 4월 9일 1억원씩 넣었다면', fontproperties=Bs(32), color='#FED7AA')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.55]); ax.set_facecolor('#3F1D0B')
vals = [2.3304, 2.3209, 2.3135, 2.3115]; labs = ['2억\n3,304만', '2억\n3,209만', '2억\n3,135만', '2억\n3,115만']
ax.bar(range(4), vals, color=['#FB923C', '#94A3B8', '#94A3B8', '#94A3B8'], width=0.62)
for i, v in enumerate(vals):
    ax.text(i, v + 0.06, labs[i], ha='center', va='bottom', fontproperties=Bs(28 if i else 30), color='white', linespacing=1.1)
    ax.text(i, -0.08, N[i], ha='center', va='top', fontproperties=Bs(26), color='white')
ax.set_ylim(-0.5, 3.1); ax.set_xlim(-0.6, 3.6); ax.axis('off')
fig.text(0.07, 0.1, '5년 7개월 뒤 차이 189만원', fontproperties=Bs(NUM_PX - 10), color='white')
fig.text(0.07, 0.045, '2026.11.20 종가 · 받은 분배금으로 다시 산 값 · 세금 떼기 전', fontsize=17, color='#FED7AA')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API 133690·379810·367380·368590.KS 일별 종가·분배 events(11/21 받음)로 2021-04-09~2026-11-20 총수익 직접 계산, calc_out.txt',
           'made_at': '2026-11-21', 'by': 'research/ndxetf1122/mkimg.py', 'out': 'img/00.png', 'topic': '나스닥100 ETF 4종', 'num': '2억 3,115만~3,304만 · 차이 189만원',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 cndtlr1221/224484911136·3 doorway2 비교 표지(상품 이름 4개+숫자) + tigerdj1122 막대 위 큰 숫자'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 해마다 (calc2_out.txt)
yrs = ['2021년\n(4/9부터)', '2022년', '2023년', '2024년', '2025년', '2026년\n(11/20까지)']
R = {'TIGER': [27.4, -30.5, 61.4, 45.0, 16.5, -4.3], 'KODEX': [27.4, -30.5, 61.8, 45.7, 16.5, -4.1],
     'ACE': [27.5, -30.5, 61.3, 45.0, 16.5, -4.3], 'RISE': [27.5, -30.6, 61.6, 45.3, 16.5, -4.1]}
C = {'TIGER': '#1E3A5F', 'KODEX': ORG, 'ACE': '#64748B', 'RISE': '#CBD5E1'}
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); x = np.arange(6); wd = 0.2
for j, n in enumerate(['TIGER', 'KODEX', 'ACE', 'RISE']):
    ax.bar(x + (j - 1.5) * wd, R[n], wd, color=C[n], label=n)
for i in range(6):
    lo, hi = min(R[n][i] for n in R), max(R[n][i] for n in R)
    lab = f'{lo}~{hi}' if lo != hi else f'{lo}'
    if hi >= 0: ax.text(x[i], hi + 2, lab, ha='center', fontproperties=Bs(14), color=INK)
    else: ax.text(x[i], lo - 2, lab, ha='center', va='top', fontproperties=Bs(14), color=INK)
ax.axhline(0, color='#9CA3AF', lw=1)
ax.set_xticks(x); ax.set_xticklabels(yrs, fontproperties=Bs(14)); ax.tick_params(axis='x', length=0, pad=6)
ax.set_yticks([]); ax.set_ylim(-42, 84)
for s_ in ('top', 'right', 'left', 'bottom'): ax.spines[s_].set_visible(False)
ax.legend(prop=Bs(13), frameon=False, loc='upper right', ncol=4)
frame(fig, '해마다 수익(%) — 네 곳 차이는 가장 커도 0.7%포인트', '분배금 받은 날 다시 삼 · 세금 떼기 전 · 숫자는 네 곳 중 가장 낮은 값~높은 값')
fig.subplots_adjust(top=0.83, bottom=0.14, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 1주 가격·최근 1년 분배금
P = {'TIGER': 155220, 'KODEX': 23180, 'ACE': 26680, 'RISE': 25875}; D_ = {'TIGER': 935, 'KODEX': 290, 'ACE': 160, 'RISE': 181}
M = {'TIGER': '1·4·7·10월', 'KODEX': '1·4·7·10월', 'ACE': '1·4·7·10월', 'RISE': '3·6·9·12월'}
order = ['TIGER', 'ACE', 'RISE', 'KODEX']
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
y = np.arange(4)[::-1]
ax.barh(y, [P[n] for n in order], color=[ORG if n == 'TIGER' else '#94A3B8' for n in order], height=0.55)
for yy, n in zip(y, order):
    ax.text(-3000, yy, n, ha='right', va='center', fontproperties=Bs(18), color=INK)
    ax.text(P[n] + 3000, yy + 0.08, f'1주 {P[n]:,}원', va='center', fontproperties=Bs(16), color=INK)
    ax.text(P[n] + 3000, yy - 0.25, f'1년 분배금 {D_[n]}원 · {M[n]}', va='center', fontsize=13, color=SUBC)
ax.set_xlim(-30000, 240000); ax.set_ylim(-0.7, 3.6); ax.axis('off')
frame(fig, '1주 가격과 최근 1년 분배금', '2026년 11월 20일 종가 · 분배금은 1주당, 최근 4번 합 · 달은 분배금 받을 사람을 정하는 달')
fig.subplots_adjust(top=0.83, bottom=0.08, left=0.02, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'ndxetf1122' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
