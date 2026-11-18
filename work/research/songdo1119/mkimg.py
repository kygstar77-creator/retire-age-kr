# songdo1119 그림(gwanggyo1118 틀) — 00 표지(차트: 같은 집 1년 오른 폭 셋), 01 신규 전세 오른 금액 구간, 02 전세가율. 숫자는 calc_out 그대로
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
SRC = '국토교통부 아파트 전월세·매매 실거래 · 인천 연수구 송도동(11/18 받음, 월세 낀 계약·취소 매매 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 40
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#1E3A5F')
fig.text(0.07, 0.86, '송도 아파트 전세', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '정말 1억 올랐나', fontproperties=Bs(38), color='#BFDBFE')
ax = fig.add_axes([0.08, 0.17, 0.84, 0.5]); ax.set_facecolor('#1E3A5F')
vals = [17, 3]; labs = ['새 전세', '매매']
ax.bar([0, 1], vals, color=['#FB923C', '#94A3B8'], width=0.55)
for i, v in enumerate(vals):
    ax.text(i, v + 0.5, f'+{v:.0f}%', ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -0.6, labs[i], ha='center', va='top', fontproperties=Bs(28), color='white')
ax.set_ylim(-4, 24); ax.set_xlim(-0.6, 1.6); ax.axis('off')
fig.text(0.07, 0.1, '같은 단지·같은 넓이 · 작년 6~10월 대비 올해 6~10월', fontproperties=Bs(24), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 전월세·매매 실거래 API(인천 연수구 28185 송도동) 2025.6~10월 vs 2026.6~10월 계약, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-18', 'by': 'research/songdo1119/mkimg.py', 'out': 'img/00.png', 'topic': '송도 아파트 전세', 'num': '+17% · +3%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 2 songdo-life/224473471539 기간별 보증금 표·차트 · 1 flalspwlq 글자 카드'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 구간
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['내리거나\n그대로', '5천만원\n미만', '5천만원\n~1억원', '1억원\n이상']; n = [23, 34, 78, 51]
cols = ['#94A3B8', '#93C5FD', BLUE, ORG]
ax.bar(range(4), n, color=cols, width=0.62)
for i, v in enumerate(n): ax.text(i, v + 1.5, f'{v}개 ({v/186*100:.0f}%)', ha='center', va='bottom', fontproperties=Bs(18), color=INK)
ax.set_xticks(range(4)); ax.set_xticklabels(labs, fontproperties=Bs(15)); ax.tick_params(axis='x', length=0, pad=8)
ax.set_yticks([]); ax.set_ylim(0, 95)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
frame(fig, '새 전세 보증금, 1년 사이 얼마나 올랐나', '송도동 같은 단지·같은 넓이 186개 · 작년 6~10월 → 올해 6~10월 신규 계약 중간값')
fig.subplots_adjust(top=0.82, bottom=0.18, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 전세가율
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['2021년\n7~12월', '2024년\n6~10월', '2025년\n6~10월', '2026년\n6~10월']; v = [52.0, 53.3, 53.4, 58.5]
ax.bar(range(4), v, color=['#93C5FD', '#93C5FD', '#93C5FD', ORG], width=0.6)
for i, x in enumerate(v): ax.text(i, x + 1, f'{int(x+0.5)}%', ha='center', va='bottom', fontproperties=Bs(22), color=INK)
ax.set_xticks(range(4)); ax.set_xticklabels(labs, fontproperties=Bs(15)); ax.tick_params(axis='x', length=0, pad=8)
ax.set_yticks([]); ax.set_ylim(0, 72)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
frame(fig, '전세가율, 매매가의 몇 %까지 왔나', '같은 단지·같은 넓이 집마다 그 기간 전세 중간값 ÷ 매매 중간값 · 그 값들의 중간값')
fig.subplots_adjust(top=0.82, bottom=0.18, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'songdo1119' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
