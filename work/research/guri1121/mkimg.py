# guri1121 그림(hanam1120 틀) — 00 표지(차트: 같은 집 신규 전세 지정 전·후), 01 84㎡ 신규 전세 가운데 세 기간, 02 신규 전세 한 달 건수. 숫자는 calc_rent_out 그대로
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
SRC = '국토교통부 아파트 전월세 실거래 · 경기 구리시(11/20 받음) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 44
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#1E3A5F')
fig.text(0.07, 0.86, '구리 아파트 전세', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '토지거래허가 뒤 올랐을까', fontproperties=Bs(38), color='#BFDBFE')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor('#1E3A5F')
vals = [9, 17]; labs = ['반년 전보다', '1년 전보다']
ax.bar(range(2), vals, color=['#FB923C', '#FB923C'], width=0.5)
for i, v in enumerate(vals):
    ax.text(i, v + 0.6, f'+{v}%', ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -0.8, labs[i], ha='center', va='top', fontproperties=Bs(24), color='white')
ax.set_ylim(-8, 23); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '같은 단지·같은 넓이 새 전세 계약 중간값', fontproperties=Bs(23), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 전월세 실거래 API(경기 구리시 41310) 신규 전세 2026.1~6월·2025.7~10월 vs 2026.7~10월 계약, calc_rent_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-20', 'by': 'research/guri1121/mkimg.py', 'out': 'img/00.png', 'topic': '구리 아파트 전세', 'num': '+9% · +17%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 4 econokong/224467986904 거래 건수 막대 차트 표지'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 84㎡ 신규 전세 가운데
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['2025년\n7~10월', '2026년\n1~6월', '2026년\n7~10월']; v = [4.8, 5.0, 5.6]; sub2 = ['160건', '410건', '131건']
ax.bar(range(3), v, color=['#93C5FD', '#93C5FD', ORG], width=0.55)
for i, x in enumerate(v):
    ax.text(i, x + 0.08, f'약 {x:.1f}억'.replace('.0억', '억').replace('4.8억', '4억 8천').replace('5.6억', '5억 6천'), ha='center', va='bottom', fontproperties=Bs(24), color=INK)
    ax.text(i, x / 2, sub2[i], ha='center', va='center', fontproperties=Bs(16), color='white' if i == 2 else INK)
ax.set_xticks(range(3)); ax.set_xticklabels(labs, fontproperties=Bs(16)); ax.tick_params(axis='x', length=0, pad=8)
ax.set_yticks([]); ax.set_ylim(0, 6.6); ax.set_xlim(-0.6, 2.6)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
frame(fig, '구리 84㎡ 새 전세, 중간 보증금', '전용 83~86㎡ 신규 전세 계약 한가운데 값 · 2026년 7월부터 규제지역·토지거래허가')
fig.subplots_adjust(top=0.82, bottom=0.14, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 신규 전세 한 달 건수
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['2025년\n7~10월', '2026년\n1~6월', '2026년\n7~10월']; v = [126, 177, 89]
ax.bar(range(3), v, color=['#93C5FD', BLUE, ORG], width=0.55)
for i, x in enumerate(v): ax.text(i, x + 3, f'{x}건', ha='center', va='bottom', fontproperties=Bs(24), color=INK)
ax.set_xticks(range(3)); ax.set_xticklabels(labs, fontproperties=Bs(16)); ax.tick_params(axis='x', length=0, pad=8)
ax.set_yticks([]); ax.set_ylim(0, 215); ax.set_xlim(-0.6, 2.6)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
frame(fig, '구리 아파트 새 전세 계약, 한 달에 몇 건', '월세 없는 신규 계약 · 기간마다 한 달 평균 · 10월 계약은 신고가 더 들어올 수 있음')
fig.subplots_adjust(top=0.82, bottom=0.14, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'guri1121' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
