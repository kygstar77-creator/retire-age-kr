# mkifrec1120 그림(hanam1120 틀) — 00 표지(차트: 분배금 vs 배당락 날 빠진 폭 중간), 01 아홉 번 분배금·빠진 폭, 02 돌아오는 데 걸린 거래일(12월·6월). 숫자는 calc_out 그대로
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
SRC = '한국거래소 정규장 일별 종가(야후·네이버 대조) · 맥쿼리인프라 분배금 지급 실적 · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 44
BG = '#14532D'
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '맥쿼리인프라 배당락', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '분배금만큼 빠졌을까', fontproperties=Bs(38), color='#BBF7D0')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor(BG)
vals = [380, 300]; labs = ['분배금(주로)', '배당락 날 빠진 폭']; lab2 = ['380원', '-300원']
ax.bar(range(2), vals, color=['#94A3B8', '#FB923C'], width=0.5)
for i, v in enumerate(vals):
    ax.text(i, v + 10, lab2[i], ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -20, labs[i], ha='center', va='top', fontproperties=Bs(26), color='white')
ax.set_ylim(-140, 500); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '2022~2026년 기준일 9번 · 빠진 폭은 중간값', fontproperties=Bs(23), color='white')
fig.text(0.07, 0.045, '한국거래소 종가 · 파이어맵 계산', fontsize=17, color='#BBF7D0')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '한국거래소 정규장 일별 종가(야후 파이낸스 088980.KS, 네이버 금융 일별 시세로 대조) 2022-06~2026-11-19 + 맥쿼리인프라 분배금 지급 실적(mkif.com), calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-19', 'by': 'research/mkifrec1120/mkimg.py', 'out': 'img/00.png', 'topic': '맥쿼리인프라 배당락', 'num': '380원 · -300원',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 ac9832/224477866604 표지(숫자 카드)·6 etf1217 표지 — 숫자 둘 표지, 우리는 차트'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 아홉 번
lab = ['22.6', '22.12', '23.6', '23.12', '24.6', '24.12', '25.6', '25.12', '26.6']
dist = [380, 390, 385, 390, 380, 380, 380, 380, 350]; drop = [350, 350, 180, 390, 300, 280, 350, 290, 120]
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
x = range(9)
ax.bar([i - 0.2 for i in x], dist, width=0.38, color='#CBD5E1', label='분배금')
ax.bar([i + 0.2 for i in x], drop, width=0.38, color=ORG, label='배당락 날 빠진 폭')
for i in x: ax.text(i + 0.2, drop[i] + 6, f'{drop[i]}', ha='center', va='bottom', fontproperties=Bs(12), color=INK)
ax.set_xticks(list(x)); ax.set_xticklabels(lab, fontproperties=Bs(13)); ax.tick_params(axis='x', length=0, pad=6)
ax.set_yticks([]); ax.set_ylim(0, 470)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(prop=Bs(13), frameon=False, loc='upper right', ncol=2)
frame(fig, '기준일마다 분배금과 배당락 날 빠진 폭(원)', '빠진 폭 = 마지막 받는 날 종가 - 배당락 날 종가 · 아홉 번 모두 내림')
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 돌아온 거래일
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
lab = ['22.12', '23.12', '24.12', '25.12']; v = [12, 26, 24, 32]
ax.barh(range(4), v, color=BLUE, height=0.55)
for i, d in enumerate(v): ax.text(d + 0.8, i, f'{d}거래일', va='center', fontproperties=Bs(18), color=INK)
ax.set_yticks(range(4)); ax.set_yticklabels(['2022년 12월', '2023년 12월', '2024년 12월', '2025년 12월'], fontproperties=Bs(15)); ax.invert_yaxis()
ax.set_xticks([]); ax.set_xlim(0, 48); ax.tick_params(axis='y', length=0)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.12, '6월 기준일 다섯 번 — 돌아온 건 2022년 한 번(233거래일), 네 번은 아직', fontproperties=Bs(15), color=ORG)
frame(fig, '배당락 전 값으로 돌아오기까지', '배당락 뒤 종가가 처음 마지막 받는 날 종가 이상이 된 날까지')
fig.subplots_adjust(top=0.82, bottom=0.2, left=0.2, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'mkifrec1120' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
