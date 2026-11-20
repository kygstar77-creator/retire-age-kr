# bundang1122 그림(gimpo1121 틀) — 00 표지(차트: 1년 같은 집 선도지구 vs 나머지 오래된 단지), 01 묶음별 1년, 02 84㎡ 판교 vs 서현수내정자 반기. 숫자는 calc_out 그대로
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
SRC = '국토교통부 아파트 매매 실거래 · 경기 성남시 분당구(11/20 받음, 취소된 거래 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 44
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#4C1D95')
fig.text(0.07, 0.86, '분당 아파트 시세', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '1년 새 같은 집 오른 폭', fontproperties=Bs(38), color='#DDD6FE')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor('#4C1D95')
vals = [18.0, 29.3]; labs = ['재건축 선도지구', '나머지 오래된 단지']; txt = ['+18%', '+29%']
ax.bar(range(2), vals, color=['#94A3B8', '#FB923C'], width=0.5)
for i in range(2):
    ax.text(i, vals[i] + 0.8, txt[i], ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -1, labs[i], ha='center', va='top', fontproperties=Bs(26), color='white')
ax.set_ylim(-7, 37); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '같은 단지·같은 넓이 · 작년 6~10월 → 올해 6~10월 중간값', fontproperties=Bs(22), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#DDD6FE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(경기 성남시 분당구 41135) 2025.6~10월 vs 2026.6~10월 계약, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-20', 'by': 'research/bundang1122/mkimg.py', 'out': 'img/00.png', 'topic': '분당 아파트 시세', 'num': '+18% / +29%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 2 ladderprice/224484693004 동별 시세 순위 차트 · 1 kh6645/224483295742 지표 카드'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['구미·금곡 (67개)', '야탑·이매·분당동 (107개)', '서현·수내·정자 (175개)', '판교 (89개)']; v = [33.8, 27.7, 20.7, 18.4]
y = list(range(len(labs)))[::-1]
ax.barh(y, v, color=[ORG if x == max(v) else '#93C5FD' for x in v], height=0.55)
for yy, x in zip(y, v): ax.text(x + 0.6, yy, f'약 {round(x)}%', va='center', fontproperties=Bs(22), color=INK)
ax.set_yticks(y); ax.set_yticklabels(labs, fontproperties=Bs(16)); ax.tick_params(axis='y', length=0, pad=8)
ax.set_xticks([]); ax.set_xlim(0, 42)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
frame(fig, '분당 1년 새 같은 집 오른 폭', '같은 단지·같은 넓이 매매 중간값 · 작년 6~10월 → 올해 6~10월')
fig.subplots_adjust(top=0.82, bottom=0.08, left=0.36, right=0.96); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
xs = ['21상', '21하', '22상', '22하', '23상', '23하', '24상', '24하', '25상', '25하', '26상', '26하']
pg = [15.20, 15.60, 15.40, 11.65, 12.65, 13.28, 13.70, 14.22, 14.85, 14.96, 15.20, 18.00]
sj = [14.03, 14.40, 14.07, 10.35, 12.00, 13.53, 14.07, 14.70, 15.39, 18.32, 19.70, 21.70]
ax.plot(range(12), pg, color=BLUE, lw=3, marker='o'); ax.plot(range(12), sj, color=ORG, lw=3, marker='o')
ax.text(11.2, pg[-1], '판교\n약 18억', va='center', fontproperties=Bs(16), color=BLUE)
ax.text(11.2, sj[-1], '서현·수내·정자\n약 21억 7천', va='center', fontproperties=Bs(16), color=ORG)
ax.set_xticks(range(12)); ax.set_xticklabels(xs, fontsize=12); ax.set_yticks([10, 15, 20]); ax.set_yticklabels(['10억', '15억', '20억'], fontsize=12)
ax.set_xlim(-0.4, 14.2); ax.set_ylim(9, 23)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
frame(fig, '84㎡ 중간 가격, 2023년 하반기에 뒤집혔다', '84㎡ 안팎 매매 반기별 중간 가격 · 26하는 7월 이후 · 그때 팔린 단지에 따라 흔들림')
fig.subplots_adjust(top=0.82, bottom=0.1, left=0.08, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'bundang1122' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
