# divbear1121 그림(guri1121 틀) — 00 표지(차트: 2022년 고점→바닥 S&P500 vs SCHD), 01 하락장 둘 낙폭, 02 바닥에서 원래 값까지 걸린 달. 숫자는 calc_out.txt 그대로
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, GRAY, BLUE = '#111827', '#6B7280', '#EA580C', '#9CA3AF', '#2563EB'
SRC = '야후 파이낸스 일별 가격(배당 다시 넣은 값, 11/20 받음) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 56, 46
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#1E3A5F')
fig.text(0.07, 0.86, '배당 ETF 하락장', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.77, '2022년 고점에서 바닥까지', fontproperties=Bs(36), color='#BFDBFE')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.52]); ax.set_facecolor('#1E3A5F')
vals = [24.5, 16.8]; labs = ['S&P500 ETF', '배당 ETF SCHD']
ax.bar(range(2), vals, color=['#94A3B8', '#FB923C'], width=0.5)
for i, v in enumerate(vals):
    ax.text(i, v + 0.6, f'-{v}%', ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -0.9, labs[i], ha='center', va='top', fontproperties=Bs(25), color='white')
ax.set_ylim(-8, 32); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '그런데 코로나 땐 SCHD도 -33.4%', fontproperties=Bs(25), color='white')
fig.text(0.07, 0.045, '야후 파이낸스 가격 · 파이어맵 계산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API 일별 adjclose(배당 재투자) SPY·SCHD 2022년 안 최대 낙폭, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-20', 'by': 'research/divbear1121/mkimg.py', 'out': 'img/00.png', 'topic': '배당 ETF 하락장', 'num': '-24.5% · -16.8%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 etflab_us/224480895309 막대 그림 위 큰 숫자 표지'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 하락장 둘 낙폭
names = ['S&P500\n(SPY)', 'SCHD', 'JEPI', 'HDV', 'SPYD']
d22 = [24.5, 16.8, 13.7, 15.4, 20.3]; d20 = [33.7, 33.4, None, 37.0, 46.4]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
import numpy as np
x = np.arange(5); wd = 0.36
for i in range(5):
    ax.bar(x[i] - wd/2, d22[i], wd, color=ORG if i else GRAY)
    ax.text(x[i] - wd/2, d22[i] + 0.8, f'-{d22[i]}', ha='center', fontproperties=Bs(14), color=INK)
    if d20[i] is not None:
        ax.bar(x[i] + wd/2, d20[i], wd, color='#1E3A5F' if i else '#4B5563')
        ax.text(x[i] + wd/2, d20[i] + 0.8, f'-{d20[i]}', ha='center', fontproperties=Bs(14), color=INK)
    else:
        ax.text(x[i] + wd/2, 2, '상장 전', ha='center', fontproperties=Bs(12), color=SUBC, rotation=90)
ax.set_xticks(x); ax.set_xticklabels(names, fontproperties=Bs(15)); ax.tick_params(axis='x', length=0, pad=6)
ax.set_yticks([]); ax.set_ylim(0, 52)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=ORG, label='2022년'), Patch(color='#1E3A5F', label='2020년 코로나')], prop=Bs(14), frameon=False, loc='upper left')
frame(fig, '하락장 두 번, 고점에서 바닥까지 몇 % 빠졌나', '배당 다시 넣은 값 · 2022년은 그해 안 고점→바닥 · 코로나는 2020년 고점→3월 23일')
fig.subplots_adjust(top=0.83, bottom=0.14, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 바닥에서 원래 값까지 걸린 달
m22 = [14.0, 14.9, 8.5, 2.0, 21.4]; m20 = [4.6, 5.4, None, 11.5, 11.1]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
for i in range(5):
    ax.bar(x[i] - wd/2, m22[i], wd, color=ORG if i else GRAY)
    ax.text(x[i] - wd/2, m22[i] + 0.3, f'{m22[i]:g}', ha='center', fontproperties=Bs(14), color=INK)
    if m20[i] is not None:
        ax.bar(x[i] + wd/2, m20[i], wd, color='#1E3A5F' if i else '#4B5563')
        ax.text(x[i] + wd/2, m20[i] + 0.3, f'{m20[i]:g}', ha='center', fontproperties=Bs(14), color=INK)
    else:
        ax.text(x[i] + wd/2, 1, '상장 전', ha='center', fontproperties=Bs(12), color=SUBC, rotation=90)
ax.set_xticks(x); ax.set_xticklabels(names, fontproperties=Bs(15)); ax.tick_params(axis='x', length=0, pad=6)
ax.set_yticks([]); ax.set_ylim(0, 24)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.legend(handles=[Patch(color=ORG, label='2022년 하락 뒤'), Patch(color='#1E3A5F', label='코로나 뒤')], prop=Bs(14), frameon=False, loc='upper left')
frame(fig, '바닥에서 원래 고점까지 걸린 기간(달)', '배당 다시 넣은 값이 하락 전 고점을 처음 다시 넘은 날까지')
fig.subplots_adjust(top=0.83, bottom=0.14, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
# 표지 100px·최근 10장 옆(guri1121 틀)
import glob
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'divbear1121' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('board', [p.split('/')[1] if '/' in p else p for p in recent])
