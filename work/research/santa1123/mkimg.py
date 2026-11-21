# santa1123 그림 — 00 표지(차트: 나스닥100 해마다 12월 등락), 01 12월·산타 7일·아무 7일 오른 비율, 02 11월 크게 빠진 해의 12월. 숫자는 calc_out.txt·calc2_out.txt 그대로
import os, json, sys, datetime, glob
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, GRAY, NAVY, BG = '#111827', '#6B7280', '#EA580C', '#9CA3AF', '#1E3A5F', '#FAF7F0'
SRC = '야후 파이낸스 S&P500·나스닥100 지수 일별 종가(11/21 받음) · 파이어맵 계산'
def load(n):
    r = json.load(open(f'raw/{n}_20261121.json'))['chart']['result'][0]; dd = {}
    for t, v in zip(r['timestamp'], r['indicators']['quote'][0]['close']):
        if v is None: continue
        dd[(datetime.datetime(1970,1,1)+datetime.timedelta(seconds=t+9*3600)).date()] = v
    return sorted(dd.items())
S = load('ndx'); last = {}
for d, v in S: last[(d.year, d.month)] = v
yrs = list(range(1986, 2026)); dec = [(last[(y,12)]/last[(y,11)]-1)*100 for y in yrs]
assert sum(1 for x in dec if x > 0) == 21
TOPIC_PX, NUM_PX = 56, 44
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '나스닥100의 12월', fontproperties=Bs(TOPIC_PX), color=INK)
fig.text(0.07, 0.76, '40년 중 21번 올랐다', fontproperties=Bs(NUM_PX), color=ORG)
fig.text(0.07, 0.70, '같은 40년 S&P500은 29번', fontproperties=Bs(26), color=NAVY)
ax = fig.add_axes([0.07, 0.13, 0.86, 0.5]); ax.set_facecolor(BG)
ax.bar(yrs, dec, color=[ORG if x > 0 else GRAY for x in dec], width=0.75)
ax.axhline(0, color=INK, lw=1)
ax.set_xticks([1986, 2000, 2025]); ax.set_xticklabels(['1986', '2000', '2025'], fontproperties=Bs(20)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]);
for s_ in ('top', 'right', 'left', 'bottom'): ax.spines[s_].set_visible(False)
fig.text(0.07, 0.05, '해마다 12월 한 달 등락 · 주황 = 오른 해 · 파이어맵 계산', fontsize=18, color=SUBC)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API ^NDX 일별 1985-10-01~2026-11-20(^GSPC와 같은 기간 맞대기), 1986~2025 해마다 12월 등락 — calc_out.txt·calc2_out.txt 파이어맵 직접 계산',
           'made_at': '2026-11-21', 'by': 'research/santa1123/mkimg.py', 'out': 'img/00.png', 'topic': '나스닥100의 12월', 'num': '40년 중 21번 올랐다',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 7 jeffrey0218/224476176211 크림 바탕·큰 제목·주황 한 줄·해마다 막대(코스피 7거래일) — 같은 꼴, 나스닥100 40년 12월 막대'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01
lab = ['12월 한 달', '산타랠리 7거래일', '아무 7거래일']
spx = [72.5, 72.5, 59.2]; ndx = [52.5, 62.5, 58.7]
x = np.arange(3); w = 0.36
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
for k, (vals, c, l) in enumerate([(spx, NAVY, 'S&P500'), (ndx, ORG, '나스닥100')]):
    ax.bar(x + (k - 0.5) * w, vals, w, color=c, label=l)
    for i, v in enumerate(vals): ax.text(x[i] + (k - 0.5) * w, v + 1.2, f'{v}%', ha='center', fontproperties=Bs(14), color=INK)
ax.set_xticks(x); ax.set_xticklabels(lab, fontproperties=Bs(15)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(0, 88); ax.legend(frameon=False, fontsize=13, loc='upper right')
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
frame(fig, '오른 해 비율(1986~2025, 40년)', "'아무 7거래일' = 같은 40년 안 모든 7거래일(1만 72번)")
fig.subplots_adjust(top=0.83, bottom=0.1, left=0.03, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02
ys = ['1987', '1988', '2000', '2007', '2008']; nov = [-8.6, -3.2, -23.6, -6.7, -11.2]; dc = [13.9, 4.9, -6.6, -0.2, 2.2]
x = np.arange(5)
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.bar(x - 0.19, nov, 0.36, color=GRAY, label='11월'); ax.bar(x + 0.19, dc, 0.36, color=[ORG if v > 0 else '#DC2626' for v in dc], label='12월')
for i in range(5):
    ax.text(x[i] - 0.19, nov[i] - 2.2, f'{nov[i]}', ha='center', fontproperties=Bs(13), color=INK)
    ax.text(x[i] + 0.19, dc[i] + (0.8 if dc[i] > 0 else -2.2), f'{dc[i]:+}', ha='center', fontproperties=Bs(13), color=INK)
ax.axhline(0, color=INK, lw=1)
ax.set_xticks(x); ax.set_xticklabels(ys, fontproperties=Bs(15)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(-28, 18); ax.legend(frameon=False, fontsize=13, loc='lower right')
for s_ in ('top', 'right', 'left', 'bottom'): ax.spines[s_].set_visible(False)
frame(fig, '나스닥100, 11월에 3% 넘게 빠진 해의 12월(%)', '1986~2025 다섯 번 — 12월에 오른 해 세 번')
fig.subplots_adjust(top=0.83, bottom=0.14, left=0.03, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'santa1123' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
