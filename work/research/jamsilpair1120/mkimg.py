# jamsilpair1120 그림(songdo1119 틀) — 00 표지(차트: 최근 1년 국민평형 가운데 값 둘), 01 해마다 가운데 값 두 선, 02 매매·전세 가운데 값. 숫자는 calc_out.txt 그대로
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
SRC = '국토교통부 아파트 매매·전월세 실거래 · 서울 송파구 잠실동(11/20 받음, 전용 80~85㎡, 취소 매매·월세 낀 계약 뺌) · 파이어맵 계산'

TOPIC_PX, NUM_PX = 58, 40
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#1E3A5F')
fig.text(0.07, 0.86, '잠실주공5단지', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '새 리센츠보다 얼마나 비쌀까', fontproperties=Bs(36), color='#BFDBFE')
ax = fig.add_axes([0.08, 0.17, 0.84, 0.5]); ax.set_facecolor('#1E3A5F')
vals = [43.25, 33.98]; labs = ['5단지 (1978년)', '리센츠 (2008년)']
ax.bar([0, 1], vals, color=['#FB923C', '#94A3B8'], width=0.55)
for i, v in enumerate(vals):
    ax.text(i, v + 1, f'약 {v:.0f}억', ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -1.2, labs[i], ha='center', va='top', fontproperties=Bs(26), color='white')
ax.set_ylim(-8, 56); ax.set_xlim(-0.6, 1.6); ax.axis('off')
fig.text(0.07, 0.1, '국민평형(전용 80~85㎡) · 최근 1년 실거래 가운데 값', fontproperties=Bs(24), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(서울 송파구 11710 잠실동) 2025.12~2026.11 계약 전용 80~85㎡, calc_out.txt §1 — 파이어맵 직접 계산',
           'made_at': '2026-11-20', 'by': 'research/jamsilpair1120/mkimg.py', 'out': 'img/00.png', 'topic': '잠실주공5단지', 'num': '약 43억 · 약 34억',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 ricenz-ella2472/224468059405 단지별 실거래 표 · 2 financelawyer 단지 비교'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=9.5, color=SUBC)
# 01 해마다
yrs = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
a = [22.28, 26.81, 23.46, 25.76, 30.25, 40.67, 43.35]; b = [20.00, 23.75, 20.60, 22.20, 24.90, 31.50, 33.95]
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
ax.plot(yrs, a, color=ORG, lw=4, marker='o', ms=9); ax.plot(yrs, b, color='#94A3B8', lw=4, marker='o', ms=9)
ax.text(2026.15, a[-1], '5단지', fontproperties=Bs(17), color=ORG, va='center'); ax.text(2026.15, b[-1], '리센츠', fontproperties=Bs(17), color='#64748B', va='center')
for y, x1, x2 in ((2020, a[0], b[0]), (2025, a[5], b[5])):
    ax.annotate('', xy=(y, x2), xytext=(y, x1), arrowprops=dict(arrowstyle='<->', color=INK, lw=1.5))
    ax.text(y + (0.12 if y == 2025 else -0.12), (x1 + x2) / 2, f'{x1-x2:.0f}억 차이', ha='left' if y == 2025 else 'right', va='center', fontproperties=Bs(16), color=INK)
ax.set_xticks(yrs); ax.set_xticklabels([f'{y}년' for y in yrs], fontproperties=Bs(13)); ax.set_xlim(2019.3, 2026.9)
ax.set_ylim(15, 48); ax.set_yticks([20, 30, 40]); ax.set_yticklabels(['20억', '30억', '40억'], fontsize=12, color=SUBC)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.grid(axis='y', color='#E5E7EB')
frame(fig, '해마다 국민평형 가운데 값', '잠실동 전용 80~85㎡ 매매 · 2026년은 1~11월 계약')
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.09, right=0.93); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 매매·전세
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
x = [0, 1]; m = [43.25, 33.98]; j = [5.18, 13.00]
ax.bar([i - 0.18 for i in x], m, width=0.34, color=['#FDBA74', '#CBD5E1'])
ax.bar([i + 0.18 for i in x], j, width=0.34, color=[ORG, '#64748B'])
for i in x:
    ax.text(i - 0.18, m[i] + 0.8, f'매매\n약 {m[i]:.0f}억', ha='center', va='bottom', fontproperties=Bs(16), color=INK)
    ax.text(i + 0.18, j[i] + 0.8, f'전세\n약 {j[i]:.0f}억', ha='center', va='bottom', fontproperties=Bs(16), color=INK)
ax.set_xticks(x); ax.set_xticklabels(['잠실주공5단지', '리센츠'], fontproperties=Bs(17)); ax.tick_params(axis='x', length=0, pad=8)
ax.set_yticks([]); ax.set_ylim(0, 56)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
frame(fig, '매매와 전세, 가운데 값', '최근 1년(2025.12~2026.11 계약) 전용 80~85㎡ · 전세는 월세 없는 계약')
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'jamsilpair1120' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
