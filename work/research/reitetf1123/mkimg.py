# reitetf1123 그림 — 00 표지(리츠 ETF 4개 1억 1년 결과), 01 국내 리츠 ETF 월 분배금 12번(9월 뒤 특별배당), 02 1억 → 세후 분배+평가. 숫자는 calc_out.txt 그대로
import os, json
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
INK, SUBC, ORG, NAVY = '#111827', '#6B7280', '#EA580C', '#1E3A5F'
SRC = '야후 파이낸스 일별 종가·분배(11/22 받음) · 미래에셋·삼성 분배금 공지 대조 · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 40
BG = '#4A2C17'
names = ['PLUS\nK리츠', 'TIGER 리츠\n부동산인프라', 'KODEX 한국\n부동산리츠인프라', 'TIGER 미국\nMSCI리츠(H)']
tot = [8579, 9241, 8757, 10787]
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '리츠ETF 1억, 1년 뒤', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.785, '분배금 받고 남은 돈(세후 분배금 + 평가액)', fontproperties=Bs(27), color='#FED7AA')
ax = fig.add_axes([0.05, 0.17, 0.9, 0.55]); ax.set_facecolor(BG)
cols = ['#94A3B8', '#94A3B8', '#94A3B8', '#FB923C']
ax.bar(range(4), [t - 7000 for t in tot], bottom=7000, color=cols, width=0.6)
ax.axhline(10000, color='white', lw=2, ls='--'); ax.text(-0.55, 10080, '넣은 돈 1억', color='white', ha='left', fontproperties=Bs(18))
for i, v in enumerate(tot):
    ax.text(i, v + 60, f'{v/10000:.2f}억'.replace('1.08억', '1.08억'), ha='center', va='bottom', fontproperties=Bs(NUM_PX - 8), color='white')
    ax.text(i, 6950, names[i], ha='center', va='top', fontproperties=Bs(17), color='white')
ax.set_ylim(6300, 11600); ax.set_xlim(-0.6, 3.6); ax.axis('off')
fig.text(0.07, 0.045, '2025.11.20 → 2026.11.20 · 분배금은 15.4% 떼고 다시 안 삼', fontsize=17, color='#FED7AA')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API 429740.KS·329200.KS·476800.KS·182480.KS 일별 종가·분배 events(11/22 받음)로 1억 1년 결과 직접 계산, calc_out.txt',
           'made_at': '2026-11-22', 'by': 'research/reitetf1123/mkimg.py', 'out': 'img/00.png', 'topic': '리츠ETF 1억, 1년 뒤', 'num': '0.86억·0.92억·0.88억·1.08억',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX - 8, 'follows': '경쟁 4 jysherpa/224474861645 리츠 ETF 비교 표지(차트·1억원 질문) + 경쟁 6 agrowingseason 상품명·60원 큰 글자'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 월 분배금 12번
mon = ['25.11·12', '26.1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
plus = [40, 40, 30, 30, 35, 27, 27, 28, 27, 131, 122, None]
kodex = [29, 29, 29, 29, 30, 30, 29, 29, 29, 60, 60, 60]
tiger = [33] * 11 + [None]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); x = np.arange(12); wd = 0.27
for arr, off, c in [(plus, -wd, ORG), (kodex, 0, NAVY), (tiger, wd, '#94A3B8')]:
    for i, v in enumerate(arr):
        if v is None: continue
        ax.bar(x[i] + off, v, wd, color=c)
        if i >= 9 and c != '#94A3B8': ax.text(x[i] + off, v + 2, f'{v}', ha='center', fontproperties=Bs(13), color=INK)
ax.annotate('특별배당 반영\n(9~12월 네 번)', xy=(9.6, 128), xytext=(5.2, 105), fontproperties=Bs(15), color=INK, arrowprops=dict(arrowstyle='->', color=INK))
ax.set_xticks(x); ax.set_xticklabels(mon, fontproperties=Bs(12)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(0, 145)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.legend(handles=[Patch(color=ORG, label='PLUS K리츠'), Patch(color=NAVY, label='KODEX 한국부동산리츠인프라'), Patch(color='#94A3B8', label='TIGER 리츠부동산인프라(매달 33원)')], prop=Bs(13), frameon=False, loc='upper left')
frame(fig, '1주당 월 분배금(원) — 최근 12번', '분배락 달 기준 · 빈칸은 아직 안 나온 달')
fig.subplots_adjust(top=0.83, bottom=0.1, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 1억 → 세후 분배 + 평가
dist = [703, 759, 782, 298]; val = [7876, 8482, 7975, 10489]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); x = np.arange(4)
ax.bar(x, val, 0.55, color=NAVY); ax.bar(x, dist, 0.55, bottom=val, color=ORG)
for i in range(4):
    ax.text(x[i], val[i] / 2, f'평가\n{val[i]:,}', ha='center', va='center', fontproperties=Bs(14), color='white')
    ax.text(x[i], val[i] + dist[i] + 120, f'분배 {dist[i]}', ha='center', fontproperties=Bs(14), color=ORG)
ax.axhline(10000, color=INK, lw=1.5, ls='--'); ax.text(-0.45, 10120, '1억', fontproperties=Bs(14), color=INK)
ax.set_xticks(x); ax.set_xticklabels([n for n in names], fontproperties=Bs(13)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(0, 12300)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
frame(fig, '1억 넣고 1년 — 받은 분배금(세후)과 남은 평가액(만원)', '2025.11.20 종가에 사서 2026.11.20 종가로 잼 · 분배금 15.4% 뗌')
fig.subplots_adjust(top=0.83, bottom=0.14, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
import sys; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import cafecover
Image.open('pkg/img/00.png').resize((100, 100)).save('pkg/cover_100.png')
cafecover.board('pkg/img/00.png', cafecover.recent_covers(10, exclude='pkg'), 'pkg/cover_board.png', '새: reitetf1123')
print('ok')
