# kodex200_1120 그림 — 00 표지(차트: 1억 5년 뒤 지수·종가만·분배금 포함), 01 연도별 받은 분배금, 02 1년·5년 비교. 숫자는 calc_out.txt
import os, json, glob
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, INK, SUBC, ORG = '#1D4ED8', '#111827', '#6B7280', '#EA580C'
SRC = "삼성자산운용 분배금 현황 · 야후 파이낸스 종가 · 네이버 코스피200 지수 · 파이어맵 계산"
BG = '#7C2D12'
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, 'KODEX 200 1억원, 5년 뒤', fontproperties=Bs(46), color='white')
fig.text(0.07, 0.76, '분배금까지 합친 돈', fontproperties=Bs(38), color='#FED7AA')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor(BG)
vals = [19341, 19518, 20526]; cols = ['#94A3B8', '#60A5FA', '#FB923C']
ax.bar([0, 1, 2], vals, color=cols, width=0.62)
ax.bar([2], [1008], bottom=[19518], color='#FB923C', width=0.62); ax.bar([2], [19518], color='#60A5FA', width=0.62)
for x, t, v in zip([0, 1, 2], ['1억 9,341만', '', '2억 526만'], vals): ax.text(x, v + 250, t, ha='center', va='bottom', fontproperties=Bs(34), color='white')

for x, t in zip([0, 1, 2], ['코스피200\n지수', 'KODEX 200\n종가만', '종가+\n분배금']): ax.text(x, 17900, t, ha='center', va='top', fontproperties=Bs(24), color='white')
ax.set_ylim(17900 - 2600, 22500); ax.set_xlim(-0.6, 2.6); ax.axis('off')
fig.text(0.07, 0.1, '2021.11.19 매수 → 2026.11.20 종가 · 분배금 20번 세전', fontproperties=Bs(22), color='white')
fig.text(0.07, 0.045, '삼성자산운용·야후·네이버 지수 · 파이어맵 계산', fontsize=17, color='#FED7AA')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '삼성자산운용 KODEX 200 분배금 현황·상품 정보 API + 야후 파이낸스 069500.KS 일별 종가 + 네이버 코스피200 지수 일별, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-20', 'by': 'research/kodex200_1120/mkimg.py', 'out': 'img/00.png', 'topic': 'KODEX 200 1억원, 5년 뒤', 'num': '1억 9,341만 · 2억 526만',
           'topic_px': 46, 'num_px': 34, 'follows': '경쟁 4 nmnpvv/224461073089 3년 전 1억 표지·1 wisefather1113 총수익 비교 표지 — 숫자 막대, 우리는 지수·종가만·분배금 포함 셋을 나란히'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
yrs = ['2022', '2023', '2024', '2025', '2026']; v = [188, 178, 206, 219, 216]
ax.bar(range(5), v, color=[BLUE] * 5, width=0.6)
for i, x in enumerate(v): ax.text(i, x + 4, f'{x}만', ha='center', va='bottom', fontproperties=Bs(18), color=INK)
ax.set_xticks(range(5)); ax.set_xticklabels([y + '년' for y in yrs], fontproperties=Bs(15)); ax.tick_params(axis='x', length=0, pad=6)
ax.set_yticks([]); ax.set_ylim(0, 260)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.13, '5년 합계 1,008만원 · 분배 20번, 4월에 가장 크게 들어옴', fontproperties=Bs(15), color=ORG)
frame(fig, '1억원어치 KODEX 200, 해마다 받은 분배금(만원)', '2021.11.19 매수 2,561주 · 세금 떼기 전 · 분배금 쓰고 다시 사지 않았을 때')
fig.subplots_adjust(top=0.82, bottom=0.2, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
import numpy as np
x = np.arange(2); w = 0.26
data = [[33.88, 93.41], [34.63, 95.18], [36.12, 105.26]]; names = ['코스피200 지수', 'KODEX 200 종가만', '종가+분배금']
cs = ['#94A3B8', BLUE, ORG]
for i, (d, n, c) in enumerate(zip(data, names, cs)):
    b = ax.bar(x + (i - 1) * w, d, w, color=c, label=n)
    for xx, vv in zip(x + (i - 1) * w, d): ax.text(xx, vv + 1.5, f'{vv:.1f}%', ha='center', va='bottom', fontproperties=Bs(14), color=INK)
ax.set_xticks(x); ax.set_xticklabels(['1년', '5년'], fontproperties=Bs(18)); ax.tick_params(axis='x', length=0, pad=6)
ax.set_yticks([]); ax.set_ylim(0, 120)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(prop=fm.FontProperties(fname=F + r'\pd500.ttf', size=13), frameon=False, loc='upper left')
frame(fig, '처음 돈 대비 얼마나 늘었나(%)', '1년: 2025.11.20~2026.11.20 · 5년: 2021.11.19~2026.11.20 · 분배금은 세전')
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'kodex200_1120' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
