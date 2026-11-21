# tigerdj1122 그림(divbear1121 틀) — 00 표지(SCHD vs TIGER 상장 뒤 총수익), 01 해마다 수익, 02 TIGER 월 분배금 40번. 숫자는 calc_out.txt 그대로
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
SRC = '야후 파이낸스 일별 종가·분배·환율(11/21 받음) · 미래에셋 분배금 현황 · 파이어맵 계산'
TOPIC_PX, NUM_PX = 60, 50
import numpy as np, datetime as dt
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#3B1F4A')
fig.text(0.07, 0.86, 'TIGER vs SCHD', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.775, '미국배당다우존스 3년 5개월 수익', fontproperties=Bs(34), color='#E9D5FF')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.52]); ax.set_facecolor('#3B1F4A')
vals = [63.2, 61.7]; labs = ['TIGER 미국배당다우존스', 'SCHD 직접(원화)']
ax.bar(range(2), vals, color=['#FB923C', '#94A3B8'], width=0.5)
for i, v in enumerate(vals):
    ax.text(i, v + 1.5, f'+{v}%', ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -2, labs[i], ha='center', va='top', fontproperties=Bs(24), color='white')
ax.set_ylim(-18, 85); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '1억원이면 차이 150만원쯤', fontproperties=Bs(27), color='white')
fig.text(0.07, 0.045, '2023.6.20~2026.11.20 · 받은 분배금으로 다시 산 값 · 한국 세금 떼기 전', fontsize=17, color='#E9D5FF')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API 458730.KS·SCHD·KRW=X 일별 종가·분배 events(11/21 받음)로 상장 뒤 총수익 직접 계산, calc_out.txt',
           'made_at': '2026-11-21', 'by': 'research/tigerdj1122/mkimg.py', 'out': 'img/00.png', 'topic': 'TIGER vs SCHD', 'num': '+63.2% · +61.7%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 6 korjap9633/224477771227 SCHD vs TIGER 글자 카드 표지 + 경쟁 divbear 막대 위 큰 숫자'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
from matplotlib.patches import Patch
# 01 해마다
yrs = ['2024년', '2025년', '2026년\n(11/20까지)', '3년 5개월\n전체']
tv = [25.6, 2.6, 17.0, 63.2]; sv = [27.1, 1.7, 17.7, 61.7]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); x = np.arange(4); wd = 0.36
for i in range(4):
    ax.bar(x[i] - wd/2, tv[i], wd, color=ORG); ax.text(x[i] - wd/2, tv[i] + 1, f'{tv[i]}', ha='center', fontproperties=Bs(15), color=INK)
    ax.bar(x[i] + wd/2, sv[i], wd, color='#1E3A5F'); ax.text(x[i] + wd/2, sv[i] + 1, f'{sv[i]}', ha='center', fontproperties=Bs(15), color=INK)
ax.set_xticks(x); ax.set_xticklabels(yrs, fontproperties=Bs(15)); ax.tick_params(axis='x', length=0, pad=6)
ax.set_yticks([]); ax.set_ylim(0, 75)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.legend(handles=[Patch(color=ORG, label='TIGER 미국배당다우존스'), Patch(color='#1E3A5F', label='SCHD 직접(원화, 미국 세금 15% 뗌)')], prop=Bs(14), frameon=False, loc='upper left')
frame(fig, '해마다 수익(%) — 이긴 쪽이 해마다 바뀜', '분배금·배당 받은 날 다시 삼 · 한국 세금 빼기 전 · 원화')
fig.subplots_adjust(top=0.83, bottom=0.14, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 TIGER 월 분배금
d = json.load(open('raw/458730.KS_chart_20261121.json'))['chart']['result'][0]['events']['dividends']
ev = {dt.datetime.fromtimestamp(int(k), dt.UTC).date(): v['amount'] for k, v in d.items()}; ev[dt.date(2023, 9, 26)] = 33.0
ks = sorted(ev); vs = [ev[k] for k in ks]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.bar(range(len(ks)), vs, color=[ORG if k.month in (3, 6, 9, 12) else '#FDBA74' for k in ks], width=0.75)
for i, (k, v) in enumerate(zip(ks, vs)):
    if v in (max(vs), min(vs)): ax.text(i, v + 0.8, f'{v:g}원', ha='center', fontproperties=Bs(13), color=INK)
ticks = [i for i, k in enumerate(ks) if k.month == 1 or i == 0]
ax.set_xticks(ticks); ax.set_xticklabels([f'{ks[i].year}.{ks[i].month}' for i in ticks], fontproperties=Bs(13)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(0, 56)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.legend(handles=[Patch(color=ORG, label='3·6·9·12월(SCHD 배당 달)'), Patch(color='#FDBA74', label='나머지 달')], prop=Bs(13), frameon=False, loc='upper left')
frame(fig, 'TIGER 미국배당다우존스 1주당 분배금 40번', '2023년 7월~2026년 10월 · 매달 26~48원 · 최근 12번 합 439원')
fig.subplots_adjust(top=0.83, bottom=0.1, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
import glob, os
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'tigerdj1122' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
