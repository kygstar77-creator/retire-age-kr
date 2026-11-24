# sanbon1123 그림(bundang1122 틀) — 00 표지(차트: 1년 같은 집 선도지구 vs 나머지 오래된 단지), 01 넓이 나눠 1년, 02 2021년 하반기 대비. 숫자는 calc_out 그대로
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
BLUE, INK, SUBC, ORG, GREY = '#1D4ED8', '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = '국토교통부 아파트 매매 실거래 · 경기 군포시 산본동(11/25 받음, 취소된 거래 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 44
BG = '#831843'
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '산본 아파트 시세', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '1년 새 같은 집 오른 폭', fontproperties=Bs(38), color='#FCE7F3')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor(BG)
vals = [17.0, 11.2]; labs = ['재건축 선도지구', '나머지 오래된 단지']; txt = ['+17%', '+11%']
ax.bar(range(2), vals, color=['#FB923C', GREY], width=0.5)
for i in range(2):
    ax.text(i, vals[i] + 0.6, txt[i], ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -0.8, labs[i], ha='center', va='top', fontproperties=Bs(26), color='white')
ax.set_ylim(-5.5, 23); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '같은 단지·같은 넓이 · 작년 6~10월 → 올해 6~10월 중간값', fontproperties=Bs(22), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#FCE7F3')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(경기 군포시 41410, 산본동) 2025.6~10월 vs 2026.6~10월 계약, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-23', 'by': 'research/sanbon1123/mkimg.py', 'out': 'img/00.png', 'topic': '산본 아파트 시세', 'num': '+17% / +11%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 5 lifeforwhat_/224482432000 1기 신도시 거래량 표 · 1 rytesmy/224485772464 시세 차트'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 넓이 나눠 1년
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
groups = ['85㎡ 넘는 집', '60㎡ 이하 집']; sd = [16.2, 22.8]; ot = [11.1, 9.3]
import numpy as np
x = np.arange(2); w = 0.34
ax.bar(x - w/2, sd, w, color='#FB923C', label='선도지구'); ax.bar(x + w/2, ot, w, color=GREY, label='나머지 오래된 단지')
for i in range(2):
    ax.text(x[i] - w/2, sd[i] + 0.5, f'약 {round(sd[i])}%', ha='center', fontproperties=Bs(20), color=INK)
    ax.text(x[i] + w/2, ot[i] + 0.5, f'약 {round(ot[i])}%', ha='center', fontproperties=Bs(20), color=INK)
ax.set_xticks(x); ax.set_xticklabels(groups, fontproperties=Bs(17)); ax.set_yticks([]); ax.set_ylim(0, 28)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(prop=Bs(14), frameon=False, loc='upper left')
frame(fig, '넓이를 나눠도 선도지구가 더 올랐다', '같은 단지·같은 넓이 매매 중간값 · 작년 6~10월 → 올해 6~10월 · 60㎡ 이하 선도지구는 평형 5개')
fig.subplots_adjust(top=0.82, bottom=0.1, left=0.06, right=0.97); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 2021년 하반기 대비
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['선도지구 (13개 중 5개 넘음)', '나머지 오래된 단지 (57개 중 10개)', '1997년 이후 단지 (16개 중 4개)']; v = [-3.0, -11.8, -9.1]
y = list(range(3))[::-1]
ax.barh(y, v, color=['#FB923C', GREY, '#93C5FD'], height=0.55)
for yy, xx in zip(y, v): ax.text(xx - 0.4, yy, f'약 {round(xx)}%', va='center', ha='right', fontproperties=Bs(22), color=INK)
ax.set_yticks(y); ax.set_yticklabels(labs, fontproperties=Bs(15)); ax.yaxis.tick_right(); ax.tick_params(axis='y', length=0, pad=8)
ax.set_xticks([]); ax.set_xlim(-16, 0.5); ax.axvline(0, color=INK, lw=1)
for s in ('top', 'left', 'bottom', 'right'): ax.spines[s].set_visible(False)
frame(fig, '2021년 하반기 값보다는 아직 아래', '같은 단지·같은 넓이 매매 중간값 · 2021년 7~12월 → 2026년 6~10월')
fig.subplots_adjust(top=0.82, bottom=0.08, left=0.04, right=0.62); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'sanbon1123' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok', [os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(p)))) for p in recent])
