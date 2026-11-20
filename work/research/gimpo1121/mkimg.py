# gimpo1121 그림(hanam1120 틀) — 00 표지(차트: 같은 집 2021년 하반기 대비 지금), 01 동네별 2021년 하반기 대비, 02 최근 1년 동네별. 숫자는 calc_out 그대로
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
SRC = '국토교통부 아파트 매매 실거래 · 경기 김포시(11/20 받음, 취소된 거래 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 44
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#14532D')
fig.text(0.07, 0.86, '김포 아파트 시세', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '2021년 고점까지 얼마나', fontproperties=Bs(38), color='#BBF7D0')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor('#14532D')
vals = [100, 80]; labs = ['2021년 하반기', '지금']
ax.bar(range(2), vals, color=['#94A3B8', '#FB923C'], width=0.5)
ax.text(1, 80 + 2.5, '-20%', ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
for i in range(2): ax.text(i, -3, labs[i], ha='center', va='top', fontproperties=Bs(28), color='white')
ax.set_ylim(-20, 112); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '같은 단지·같은 넓이끼리 맞춘 288개 · 중간값', fontproperties=Bs(23), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#BBF7D0')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(경기 김포시 41570) 2021.7~12월 vs 2026.6~10월 계약, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-20', 'by': 'research/gimpo1121/mkimg.py', 'out': 'img/00.png', 'topic': '김포 아파트 시세', 'num': '-20%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 3 rytesmy/224478321264 실거래 가격 흐름 그래프 · 4 eastblue911 5년 가격 흐름 차트'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
def hbars(path, title, sub, labs, v, fmt, xmax):
    fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
    y = range(len(labs))[::-1]
    cols = [ORG if x == min(v) else '#93C5FD' for x in v]
    ax.barh(list(y), [abs(x) for x in v], color=cols, height=0.55)
    for yy, x, l in zip(y, v, labs):
        ax.text(abs(x) + xmax * 0.015, yy, fmt(x), va='center', fontproperties=Bs(22), color=INK)
    ax.set_yticks(list(y)); ax.set_yticklabels(labs, fontproperties=Bs(17)); ax.tick_params(axis='y', length=0, pad=8)
    ax.set_xticks([]); ax.set_xlim(0, xmax)
    for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
    frame(fig, title, sub)
    fig.subplots_adjust(top=0.82, bottom=0.08, left=0.3, right=0.96); fig.savefig(path, dpi=100); plt.close(fig)
hbars('pkg/img/01.png', '2021년 하반기보다 지금 얼마나 낮나', '같은 단지·같은 넓이 매매 중간값 · 2021년 7~12월 → 올해 6~10월',
      ['고촌 (33개)', '구도심 (76개)', '풍무 (55개)', '한강신도시 (110개)'], [-15.7, -16.4, -18.3, -22.8], lambda x: f'약 {round(-x)}% 아래', 32)
# 02 최근 1년 — 오르내림이 섞여 세로 막대(0선 기준)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['풍무', '고촌', '한강신도시', '구도심']; v = [1.3, 0.3, -1.7, -2.4]
ax.bar(range(4), v, color=[BLUE if x > 0 else ORG for x in v], width=0.55)
ax.axhline(0, color=INK, lw=1)
for i, x in enumerate(v):
    ax.text(i, x + (0.15 if x >= 0 else -0.15), f'{x:+.1f}%', ha='center', va='bottom' if x >= 0 else 'top', fontproperties=Bs(22), color=INK)
ax.set_xticks([])
for i, l in enumerate(labs): ax.text(i, -3.55, l, ha='center', va='top', fontproperties=Bs(19), color=INK)
ax.set_yticks([]); ax.set_ylim(-4.3, 2.4)
for s in ('top', 'right', 'left', 'bottom'): ax.spines[s].set_visible(False)
frame(fig, '최근 1년은 거의 제자리', '같은 단지·같은 넓이 매매 중간값 · 작년 6~10월 → 올해 6~10월 · 김포 전체 299개 -1.2%')
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'gimpo1121' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
