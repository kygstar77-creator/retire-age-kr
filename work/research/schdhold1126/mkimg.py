# schdhold1126 그림 — 00 표지(보유 기간별 손해 비율), 01 배당 재투자 달러·원화·가격만, 02 산 날별 1년 뒤 결과. 숫자는 calc.py와 같은 셈으로 다시 냄
import os, json, sys, datetime, bisect
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, GRAY, NAVY, RED, TEAL = '#111827', '#6B7280', '#EA580C', '#9CA3AF', '#1E3A5F', '#DC2626', '#0F766E'
def load(n):
    q = json.load(open(f'raw/{n}_20261124.json'))['chart']['result'][0]
    d = lambda a: (datetime.datetime(1970,1,1)+datetime.timedelta(seconds=a+9*3600)).date()
    return ([(d(a), b) for a, b in zip(q['timestamp'], q['indicators']['adjclose'][0]['adjclose']) if b],
            [(d(a), b) for a, b in zip(q['timestamp'], q['indicators']['quote'][0]['close']) if b])
tr, px = load('schd')
fx = sorted((datetime.date.fromisoformat(a), float(b)) for a, b in json.load(open('raw/fred_DEXKOUS_20261124.json')) if b not in ('.', None, ''))
fd = [a for a, _ in fx]
def fxat(d):
    j = bisect.bisect_right(fd, d) - 1
    return fx[j][1] if j >= 0 else None
trk = [(d, v * fxat(d)) for d, v in tr if fxat(d)]
def roll(r, yrs):
    ds = [a for a, _ in r]; out = []
    for d, v in r:
        try: t = d.replace(year=d.year + yrs)
        except ValueError: t = d.replace(year=d.year + yrs, day=28)
        j = bisect.bisect_left(ds, t)
        if j >= len(r): break
        out.append((d, r[j][0], r[j][1] / v - 1))
    return out
def lossp(r, y):
    o = roll(r, y); return round(sum(x[2] < 0 for x in o) / len(o) * 100, 1)
P = [1, 2, 3, 4, 5, 10]
usd = [lossp(tr, y) for y in P]; krw = [lossp(trk, y) for y in P]; pxl = [lossp(px, y) for y in P]
def cnt(r, y): return sum(x[2] < 0 for x in roll(r, y))
CN = {'usd': [cnt(tr, y) for y in P], 'krw': [cnt(trk, y) for y in P], 'px': [cnt(px, y) for y in P]}
print('건수', CN)
print('달러', usd, '원화', krw, '가격만', pxl)
last = tr[-1][0]; LAST = f'{last.year}.{last.month}.{last.day}'
SRC = f'야후 파이낸스 SCHD 일별 수정 종가·종가, FRED 원·달러(2026.11.26 받음) · 파이어맵 계산'
lab = lambda v, n: ('0번' if v == 0 else (f'{n}번' if v < 0.5 else f'{v}%'))
cnt3 = sum(x[2] < 0 for x in roll(tr, 3))
TOPIC_PX, NUM_PX = 58, 44
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.07, 0.85, 'SCHD 오래 들면', fontproperties=Bs(TOPIC_PX), color=INK)
fig.text(0.07, 0.75, f'4년부터 손해 0번', fontproperties=Bs(NUM_PX), color=RED)
ax = fig.add_axes([0.07, 0.16, 0.86, 0.5])
cols = [RED, GRAY, GRAY, TEAL, TEAL, TEAL]
ax.bar(range(6), [max(v, 0.25) if v else 0 for v in usd], color=cols, width=0.62)
for i, v in enumerate(usd): ax.text(i, max(v, 0) + 0.4, (f'{v}%' if v else '0%'), ha='center', fontproperties=Bs(26), color=INK)
ax.set_xticks(range(6)); ax.set_xticklabels([f'{p}년' for p in P], fontproperties=Bs(24)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(0, 15.5)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
fig.text(0.07, 0.05, f'배당 재투자 · 2011.10~{LAST} · 파이어맵 계산', fontsize=18, color=SUBC)
fig.savefig('pkg/img/00.png', dpi=100); plt.close(fig)
json.dump({'type': 'chart', 'source': f'야후 파이낸스 chart API SCHD 일별 수정 종가(배당 재투자·분할 반영) 2011-10-20~{last}, 거래일마다 산 경우 보유 기간별 손해 비율 — calc_out.txt 파이어맵 직접 계산',
           'made_at': '2026-11-24', 'by': 'research/schdhold1126/mkimg.py', 'out': 'img/00.png', 'topic': 'SCHD 오래 들면', 'num': '4년부터 손해 0번',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '우리 잘된 글 spx10y1122(15.9회/일) 표지 꼴 — 흰 바탕·검은 큰 제목·빨간 숫자 한 줄·기간별 막대'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
import numpy as np
x = np.arange(6); w = 0.27
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
for k, (vals, c, lb, kk) in enumerate([(usd, ORG, '배당 다시 넣음(달러)', 'usd'), (krw, NAVY, '배당 다시 넣음(원화)', 'krw'), (pxl, GRAY, '배당 빼고 가격만(달러)', 'px')]):
    ax.bar(x + (k - 1) * w, vals, w, color=c, label=lb)
    for i, v in enumerate(vals):
        n = CN[kk][i]; t = (f'{v:.1f}' if v >= 0.5 else (f'{n}번' if n else '0'))
        ax.text(x[i] + (k - 1) * w, v + 0.4, t, ha='center', fontproperties=Bs(10 if n and v < 0.5 else 11), color=INK)
ax.set_xticks(x); ax.set_xticklabels([f'{p}년 보유' for p in P], fontproperties=Bs(14)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(0, 25); ax.legend(frameon=False, fontsize=12, loc='upper right')
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
frame(fig, 'SCHD 들고 있던 기간별 손해로 끝난 비율(%)', '거래일마다 그날 한 번에 샀다고 치고 N년 뒤 값과 비교')
fig.subplots_adjust(top=0.83, bottom=0.1, left=0.03, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
o = roll(tr, 1); xs = [a for a, _, _ in o]; ys = [c * 100 for _, _, c in o]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.fill_between(xs, ys, 0, where=[y >= 0 for y in ys], color='#FDBA74', lw=0)
ax.fill_between(xs, ys, 0, where=[y < 0 for y in ys], color=RED, lw=0)
ax.axhline(0, color=INK, lw=1)
w_ = min(o, key=lambda t: t[2])
ax.annotate(f'{w_[0].year}.{w_[0].month}.{w_[0].day}에 산 경우 {w_[2]*100:.1f}%', xy=(w_[0], w_[2]*100), xytext=(datetime.date(2015, 6, 1), -40), fontproperties=Bs(13), color=RED, arrowprops=dict(arrowstyle='-', color=RED))
for s_ in ('top', 'right'): ax.spines[s_].set_visible(False)
ax.set_ylabel('1년 뒤 등락(%)', fontsize=12); ax.tick_params(labelsize=11); ax.set_ylim(-50, 95)
frame(fig, 'SCHD 산 날마다 1년 뒤 결과(배당 다시 넣음, 달러)', f'가로 = 산 날(2011.10~{o[-1][0].year}.{o[-1][0].month}) · 빨간 곳 = 1년 뒤 손해')
fig.subplots_adjust(top=0.83, bottom=0.12, left=0.1, right=0.97); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
import glob
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'schdhold1126' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
