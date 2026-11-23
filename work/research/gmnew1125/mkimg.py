# gmnew1125 그림(sanbon1123 틀) — 00 표지(차트: 84㎡대 같은 집 1년 지은 해별), 01 쇼츠 24건 단지 구성, 02 2021년 하반기 대비. 숫자는 calc_out 그대로
import os, json, glob
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs('pkg/img', exist_ok=True)
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, GREY = '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = '국토교통부 아파트 매매 실거래 · 경기 광명시(11/23 받음, 취소된 거래 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 54, 36
BG = '#1E3A5F'
# 00 표지 — 84㎡대 같은 집 1년(calc_out §7)
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '광명 신축 아파트', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.77, '84㎡ 같은 집, 1년 새 오른 폭', fontproperties=Bs(34), color='#DBEAFE')
ax = fig.add_axes([0.05, 0.19, 0.9, 0.5]); ax.set_facecolor(BG)
vals = [16.5, 16.2, 20.0, 26.6]; labs = ['2019년 이후', '2010~2018년', '2000~2009년', '1999년까지']; txt = ['+17%', '+16%', '+20%', '+27%']
cols = ['#FB923C', GREY, GREY, '#FDE68A']
ax.bar(range(4), vals, color=cols, width=0.62)
for i in range(4):
    ax.text(i, vals[i] + 0.6, txt[i], ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -0.9, labs[i], ha='center', va='top', fontproperties=Bs(21), color='white')
ax.set_ylim(-6, 33); ax.set_xlim(-0.6, 3.6); ax.axis('off')
fig.text(0.07, 0.115, '지은 해 기준 · 작년 6~10월 → 올해 6~10월 중간값', fontproperties=Bs(22), color='white')
fig.text(0.07, 0.055, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#DBEAFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(경기 광명시 41210) 2025.6~10월 vs 2026.6~10월 계약, 84㎡대 같은 집, calc_out.txt §7 — 파이어맵 직접 계산',
           'made_at': '2026-11-23', 'by': 'research/gmnew1125/mkimg.py', 'out': 'img/00.png', 'topic': '광명 신축 아파트', 'num': '+17% / +27%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 utility_sym/224473457170 첫 그림 단지 순위 표 · 3 mapakc60/224471836687 구축 vs 신축 비교'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 쇼츠 24건 구성(calc_out §5·§10)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['유-플래닛태영데시앙\n(일직동, 12건)', '나머지 새 단지 5곳\n(12건)', '24건 전체']; v = [14.85, 13.50, 14.71]
ax.bar(range(3), v, color=['#FB923C', GREY, '#1D4ED8'], width=0.55)
vt = ['약 14억 8,500만', '약 13억 5,000만', '약 14억 7,100만']
for i in range(3): ax.text(i, v[i] + 0.25, vt[i], ha='center', fontproperties=Bs(21), color=INK)
ax.set_xticks(range(3)); ax.set_xticklabels(labs, fontproperties=Bs(15)); ax.set_yticks([]); ax.set_ylim(0, 18)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
frame(fig, "쇼츠 '광명 15억' 24건 중 절반이 한 단지", '2019년 이후 지은 단지 84㎡대 매매 · 2026년 7~9월 계약 · 중간값')
fig.subplots_adjust(top=0.82, bottom=0.16, left=0.06, right=0.97); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 2021년 하반기 대비(calc_out §3, 모든 넓이)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['1999년까지 (77개 중 55개 넘음)', '2000~2009년 (46개 중 32개)', '2010~2018년 (36개 중 16개)']; v = [8.2, 4.8, -2.3]
y = list(range(3))[::-1]
ax.barh(y, v, color=['#FDE68A', GREY, GREY], height=0.55)
for yy, xx in zip(y, v): ax.text(xx + (0.3 if xx >= 0 else -0.3), yy, f'약 {"+" if xx > 0 else ""}{round(xx)}%', va='center', ha='left' if xx >= 0 else 'right', fontproperties=Bs(22), color=INK)
ax.set_yticks(y); ax.set_yticklabels(labs, fontproperties=Bs(15)); ax.yaxis.tick_right(); ax.tick_params(axis='y', length=0, pad=8)
ax.set_xticks([]); ax.set_xlim(-6, 17); ax.axvline(0, color=INK, lw=1)
for s in ('top', 'left', 'bottom', 'right'): ax.spines[s].set_visible(False)
frame(fig, '2021년 하반기 값과 비교하면', '같은 단지·같은 넓이 매매 중간값 · 2021년 7~12월 → 2026년 6~10월 · 2019년 이후 단지는 3개뿐이라 뺌')
fig.subplots_adjust(top=0.82, bottom=0.08, left=0.04, right=0.58); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'gmnew1125' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok', [os.path.basename(os.path.dirname(os.path.dirname(p))) for p in recent])
