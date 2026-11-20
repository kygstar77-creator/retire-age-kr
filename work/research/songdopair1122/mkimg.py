# songdopair1122 그림(jamsilpair1120 틀) — 00 표지(33곳 점 그림), 01 구간별 단지 수, 02 동 전체 고점·바닥·지금 가운데 값. 숫자는 calc_out.txt에서 읽는다
import os, re, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, INK, SUBC, ORG = '#1D4ED8', '#111827', '#6B7280', '#EA580C'
T = open('calc_out.txt', encoding='utf-8').read()
sec2 = T.split('## 2')[1].split('## 3')[0]
pct = [int(m) for m in re.findall(r'→ (\d+)%', sec2)]
assert len(pct) == 33, len(pct)
sec1 = re.search(r'고점 반기 (\d+)건 중앙 ([\d.]+)억 · 바닥 반기 (\d+)건 중앙 ([\d.]+)억 · 최근 (\d+)건 중앙 ([\d.]+)억', T)
hi, lo, rc = float(sec1.group(2)), float(sec1.group(4)), float(sec1.group(6))
SRC = '국토교통부 아파트 매매 실거래 · 인천 연수구 송도동(11/21 받음, 전용 80~86㎡, 취소 계약·공공기관 매수 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 52
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#1E3A5F')
fig.text(0.07, 0.86, '송도 아파트 33단지', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.77, '고점 때 값의 몇 %일까', fontproperties=Bs(36), color='#BFDBFE')
ax = fig.add_axes([0.08, 0.30, 0.84, 0.32]); ax.set_facecolor('#1E3A5F')
from collections import Counter
cnt = Counter(); ys = []
for p in sorted(pct):
    ys.append(cnt[p]); cnt[p] += 1
ax.scatter(sorted(pct), [y * 1.0 + 1 for y in ys], s=330, color='#FB923C', zorder=3, edgecolor='white', linewidth=1.2)
ax.axvline(84, color='white', lw=2.5, ls='--', zorder=2)
ax.set_xlim(66, 101); ax.set_ylim(-0.2, max(ys) + 2.2)
ax.set_yticks([]); ax.set_xticks([70, 80, 90, 100]); ax.set_xticklabels(['70%', '80%', '90%', '100%'], fontproperties=Bs(20), color='white')
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color('#BFDBFE'); ax.tick_params(axis='x', colors='white', length=6)
fig.text(0.07, 0.19, '70~97%', fontproperties=Bs(NUM_PX), color='white')
fig.text(0.50, 0.205, '한가운데 84%', fontproperties=Bs(34), color='#FDBA74')
fig.text(0.07, 0.115, '점 하나 = 단지 하나 · 전용 84㎡대 · 2026년 7월 이후 가운데 값', fontproperties=Bs(21), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(인천 연수구 28185 송도동) 2021.01~2026.11 계약 전용 80~86㎡, calc_out.txt §2 — 파이어맵 직접 계산',
           'made_at': '2026-11-21', 'by': 'research/songdopair1122/mkimg.py', 'out': 'img/00.png', 'topic': '송도 아파트 33단지', 'num': '70~97% · 한가운데 84%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 shoien629/224483006658 단지별 84㎡ 순위 · 4 utility_sym/224478145772 신축 순위'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=9.5, color=SUBC)
# 01 구간별 단지 수
bands = [('70~79%', sum(1 for p in pct if 70 <= p < 80)), ('80~84%', sum(1 for p in pct if 80 <= p < 85)),
         ('85~89%', sum(1 for p in pct if 85 <= p < 90)), ('90% 이상', sum(1 for p in pct if p >= 90))]
assert sum(b[1] for b in bands) == 33
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
cols = ['#94A3B8', '#94A3B8', '#94A3B8', ORG]
ax.bar(range(4), [b[1] for b in bands], color=cols, width=0.6)
for i, b in enumerate(bands):
    ax.text(i, b[1] + 0.35, f'{b[1]}곳', ha='center', va='bottom', fontproperties=Bs(24), color=INK)
ax.set_xticks(range(4)); ax.set_xticklabels([b[0] for b in bands], fontproperties=Bs(18)); ax.tick_params(axis='x', length=0, pad=8)
ax.set_yticks([]); ax.set_ylim(0, 15)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
frame(fig, '지금 값이 고점의 몇 %인 단지가 몇 곳일까', '송도동 84㎡대 단지 33곳 · 2026년 7월 이후 가운데 값 ÷ 2021.7~2022.6 가운데 값')
fig.subplots_adjust(top=0.82, bottom=0.14, left=0.06, right=0.94); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 동 전체
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
vals = [hi, lo, rc]; labs = ['고점 때\n2021.7~2022.6', '바닥 때\n2022.7~2023.6', '지금\n2026년 7월 이후']
ax.bar(range(3), vals, color=['#CBD5E1', '#94A3B8', ORG], width=0.55)
for i, v in enumerate(vals):
    ax.text(i, v + 0.15, f'약 {v:.2f}억', ha='center', va='bottom', fontproperties=Bs(22), color=INK)
ax.set_xticks(range(3)); ax.set_xticklabels(labs, fontproperties=Bs(15)); ax.tick_params(axis='x', length=0, pad=8)
ax.set_yticks([]); ax.set_ylim(0, 10.6)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
frame(fig, '송도동 84㎡대 전체 거래 가운데 값', '단지를 섞어 한 줄로 세운 값 · 고점의 82%')
fig.subplots_adjust(top=0.82, bottom=0.16, left=0.06, right=0.94); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok', bands, hi, lo, rc)
# 표지 100px·최근 10장 옆 비교판(jamsilpair1120 방식)
import sys; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import cafecover
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100), Image.LANCZOS).save('pkg/cover_100.png')
rec = cafecover.recent_covers(10, exclude=None)
cafecover.board(os.path.abspath('pkg/img/00.png'), rec, os.path.abspath('pkg/cover_board.png'), '새: songdopair1122')
print('board ok')
