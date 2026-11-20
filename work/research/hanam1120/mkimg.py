# hanam1120 그림(songdo1119 틀) — 00 표지(차트: 같은 집 매매 1년 오른 폭 네 동네), 01 2021년 하반기 대비 미사·구도심, 02 월평균 매매 건수. 숫자는 calc_out 그대로
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
SRC = '국토교통부 아파트 매매 실거래 · 경기 하남시(11/19 받음, 취소된 거래 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 44
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#1E3A5F')
fig.text(0.07, 0.86, '하남 아파트 시세', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '1년 새 어느 동네가 더', fontproperties=Bs(38), color='#BFDBFE')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor('#1E3A5F')
vals = [24, 18]; labs = ['신도시 셋', '구도심']
ax.bar(range(2), vals, color=['#FB923C', '#94A3B8'], width=0.5)
for i, v in enumerate(vals):
    ax.text(i, v + 0.6, f'+{v}%', ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -0.8, labs[i], ha='center', va='top', fontproperties=Bs(28), color='white')
ax.set_ylim(-6, 31); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '신도시 셋 = 감일·미사·위례 · 같은 집 매매 1년 중간값', fontproperties=Bs(23), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(경기 하남시 41450) 2025.6~10월 vs 2026.6~10월 계약, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-19', 'by': 'research/hanam1120/mkimg.py', 'out': 'img/00.png', 'topic': '하남 아파트 시세', 'num': '+24% · +18%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 2 phillius9/224480717756 월별 평균가·평당가 표 · 4 kokoko9ko 단지 사진'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 2021년 하반기 대비
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['미사', '구도심']; v = [16.7, 6.8]; sub2 = ['68개 중 67개가\n그때보다 높음', '64개 중 51개가\n그때보다 높음']
ax.bar(range(2), v, color=[ORG, '#93C5FD'], width=0.5)
for i, x in enumerate(v):
    ax.text(i, x + 0.5, f'+{round(x)}%', ha='center', va='bottom', fontproperties=Bs(26), color=INK)
    ax.text(i, x / 2, sub2[i], ha='center', va='center', fontproperties=Bs(14), color='white' if i == 0 else INK)
ax.set_xticks(range(2)); ax.set_xticklabels(labs, fontproperties=Bs(18)); ax.tick_params(axis='x', length=0, pad=8)
ax.set_yticks([]); ax.set_ylim(0, 21); ax.set_xlim(-0.7, 1.7)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
frame(fig, '2021년 하반기 값보다 지금 얼마나 높나', '같은 단지·같은 넓이 매매 중간값 · 2021년 7~12월 → 올해 6~10월')
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 월평균 거래 건수
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['2024년\n6~10월', '2025년\n6~10월', '2025년 11월\n~2026년 3월', '2026년\n6~10월']; v = [364, 492, 247, 259]
ax.bar(range(4), v, color=['#93C5FD', BLUE, '#93C5FD', ORG], width=0.6)
for i, x in enumerate(v): ax.text(i, x + 8, f'{x}건', ha='center', va='bottom', fontproperties=Bs(22), color=INK)
ax.set_xticks(range(4)); ax.set_xticklabels(labs, fontproperties=Bs(14)); ax.tick_params(axis='x', length=0, pad=8)
ax.set_yticks([]); ax.set_ylim(0, 580)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
frame(fig, '하남 아파트 매매, 한 달에 몇 건', '취소된 거래 뺀 매매 계약 · 기간마다 다섯 달 평균 · 2025년 10월 20일부터 토지거래허가')
fig.subplots_adjust(top=0.82, bottom=0.18, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'hanam1120' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
