# spx10y1122 그림 — 00 표지(차트: 보유 기간별 손해 비율), 01 달러·원화·가격만 손해 비율, 02 10년 보유 결과(산 날별). 숫자는 calc_out.txt 그대로
import os, json, sys, datetime, bisect
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, GRAY, NAVY = '#111827', '#6B7280', '#EA580C', '#9CA3AF', '#1E3A5F'
SRC = '야후 파이낸스 S&P500 토탈리턴·가격 지수, FRED 원·달러(11/21 받음) · 파이어맵 계산'
P = ['1년', '5년', '10년', '15년', '20년']
usd = [16.7, 12.5, 6.5, 0, 0]; krw = [15.1, 13.7, 7.4, 0, 0]; px = [30.1, 19.6, 11.0, 3.5, 3.5]
TOPIC_PX, NUM_PX = 58, 44
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.07, 0.85, 'S&P500 10년 보유', fontproperties=Bs(TOPIC_PX), color=INK)
fig.text(0.07, 0.75, '손해 본 경우 6.5%', fontproperties=Bs(NUM_PX), color='#DC2626')
ax = fig.add_axes([0.07, 0.16, 0.86, 0.5])
b = ax.bar(range(5), usd, color=[GRAY, GRAY, '#DC2626', '#0F766E', '#0F766E'], width=0.62)
for i, v in enumerate(usd): ax.text(i, v + 0.6, (f'{v}%' if v else '0번'), ha='center', fontproperties=Bs(28), color=INK)
ax.set_xticks(range(5)); ax.set_xticklabels([p + ' 보유' for p in P], fontproperties=Bs(22)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(0, 21)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
fig.text(0.07, 0.05, '배당 재투자 · 1988~2026.11.20 · 파이어맵 계산', fontsize=18, color=SUBC)
fig.savefig('pkg/img/00.png', dpi=100); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API ^SP500TR 일별 1988-01-04~2026-11-20(SPY 수정 종가·FRED SP500과 대조), 거래일마다 산 경우 보유 기간별 손해 비율 — calc_out.txt 파이어맵 직접 계산',
           'made_at': '2026-11-21', 'by': 'research/spx10y1122/mkimg.py', 'out': 'img/00.png', 'topic': 'S&P500 10년 보유', 'num': '손해 본 경우 6.5%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 7 julyasd/224484368469 흰 바탕·검은 큰 제목·빨간 숫자 한 줄·아래 선 그림 (장식 선 대신 실제 기간별 막대)'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
import numpy as np
x = np.arange(5); w = 0.27
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
for k, (vals, c, lab) in enumerate([(usd, ORG, '배당 재투자(달러) 1988~'), (krw, NAVY, '배당 재투자(원화) 1988~'), (px, GRAY, '가격만(달러) 1928~')]):
    ax.bar(x + (k - 1) * w, vals, w, color=c, label=lab)
    for i, v in enumerate(vals): ax.text(x[i] + (k - 1) * w, v + 0.5, (f'{v:.1f}' if v else '0'), ha='center', fontproperties=Bs(11), color=INK)
ax.set_xticks(x); ax.set_xticklabels([p + ' 보유' for p in P], fontproperties=Bs(14)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(0, 34); ax.legend(frameon=False, fontsize=12, loc='upper right')
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
frame(fig, '들고 있던 기간별 손해로 끝난 비율(%)', '거래일마다 그날 한 번에 샀다고 치고 N년 뒤 값과 비교')
fig.subplots_adjust(top=0.83, bottom=0.1, left=0.03, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 산 날별 10년 결과
q = json.load(open('raw/sp500tr_20261121.json'))['chart']['result'][0]
r = [((datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=a)).date(), c) for a, c in zip(q['timestamp'], q['indicators']['quote'][0]['close']) if c]
ds = [a for a, _ in r]; xs = []; ys = []
for d, v in r:
    t = (d.replace(day=28) if (d.month, d.day) == (2, 29) else d).replace(year=d.year + 10)
    j = bisect.bisect_left(ds, t)
    if j >= len(r): break
    xs.append(d); ys.append((r[j][1] / v - 1) * 100)
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.fill_between(xs, ys, 0, where=[y >= 0 for y in ys], color='#FDBA74', lw=0)
ax.fill_between(xs, ys, 0, where=[y < 0 for y in ys], color='#DC2626', lw=0)
ax.axhline(0, color=INK, lw=1)
ax.annotate('1999.3.8에 산 경우 -37.3%', xy=(datetime.date(1999, 3, 8), -37.3), xytext=(datetime.date(2002, 6, 1), -60), fontproperties=Bs(13), color='#DC2626', arrowprops=dict(arrowstyle='-', color='#DC2626'))
ax.text(datetime.date(1999, 6, 1), 40, '손해 473번\n1998.10~2000.10에 산 경우', fontproperties=Bs(13), color='#DC2626')
for s_ in ('top', 'right'): ax.spines[s_].set_visible(False)
ax.set_ylabel('10년 뒤 등락(%)', fontsize=12); ax.tick_params(labelsize=11)
frame(fig, '산 날마다 10년 뒤 결과(배당 재투자, 달러)', '가로 = 산 날(1988.1~2016.11) · 세로 = 10년 뒤 값과의 차이(%)')
fig.subplots_adjust(top=0.83, bottom=0.12, left=0.1, right=0.97); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
import glob
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'spx10y1122' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
