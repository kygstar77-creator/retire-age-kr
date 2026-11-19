# jepq1120 그림 — 00 표지(차트: 1억 → 평가 8,792만 + 분배금 1,031만), 01 12번 세후 원화 분배금, 02 원화·달러 기준 1년 뒤. 숫자는 calc_out 그대로
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
SRC = "나스닥 배당 기록 · 야후 파이낸스 JEPQ 종가 · 한국은행 매매기준율 · 파이어맵 계산"
TOPIC_PX, NUM_PX = 58, 44
BG = '#14532D'
TOPIC_PX, NUM_PX = 58, 44
BG = '#1E3A8A'
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, 'JEPQ 1억원, 1년 뒤', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '분배금 받고 남은 돈', fontproperties=Bs(38), color='#BFDBFE')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor(BG)
ax.bar([0], [10000], color='#94A3B8', width=0.5)
ax.bar([1], [8792], color='#60A5FA', width=0.5); ax.bar([1], [1031], bottom=[8792], color='#FB923C', width=0.5)
ax.text(0, 10150, '1억원', ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
ax.text(1, 9973, '9,823만원', ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
ax.text(1, 9300, '분배금 1,031만', ha='center', va='center', fontproperties=Bs(19), color='white')
ax.text(1, 4400, '평가액\n8,792만', ha='center', va='center', fontproperties=Bs(22), color='white')
ax.text(0, -300, '처음 넣은 돈', ha='center', va='top', fontproperties=Bs(26), color='white')
ax.text(1, -300, '1년 뒤(원화)', ha='center', va='top', fontproperties=Bs(26), color='white')
ax.set_ylim(-2200, 12500); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '2025.11.18 매수 · 분배금 12번 세후 15% · 지급일 환율', fontproperties=Bs(22), color='white')
fig.text(0.07, 0.045, '나스닥·야후 종가·한국은행 환율 · 파이어맵 계산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '나스닥 JEPQ 배당 기록(야후 파이낸스 대조) 2025-12~2026-11 12회 + 야후 파이낸스 JEPQ 일별 종가 + 한국은행 ECOS 원/달러 매매기준율 + IRS 조세조약 세율표(한국 배당 15%), calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-19', 'by': 'research/jepq1120/mkimg.py', 'out': 'img/00.png', 'topic': 'JEPQ 1억원, 1년 뒤', 'num': '1억원 · 9,823만원',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 real_bin/224476236930 표지(제목 카드)·5 auto_finance 총손익 표지 — 숫자 둘 표지, 우리는 차트'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
lab = ['25.12', '26.1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
v = [83, 85, 69, 76, 86, 90, 88, 101, 103, 96, 79, 74]
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
cols = [ORG if x in (69, 103) else BLUE for x in v]
ax.bar(range(12), v, color=cols, width=0.62)
for i, x in enumerate(v): ax.text(i, x + 1.5, f'{x}', ha='center', va='bottom', fontproperties=Bs(13), color=INK)
ax.set_xticks(range(12)); ax.set_xticklabels(lab, fontproperties=Bs(13)); ax.tick_params(axis='x', length=0, pad=6)
ax.set_yticks([]); ax.set_ylim(0, 125)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
frame(fig, '1억원어치 JEPQ, 달마다 들어온 분배금(만원)', '지급일 기준 · 미국 원천징수 15% 뗀 뒤 · 지급일 한국은행 매매기준율로 환산')
fig.subplots_adjust(top=0.82, bottom=0.1, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
ax.barh([0, 1], [6.72, -1.77], color=[BLUE, ORG], height=0.5)
ax.text(6.72 + 0.2, 0, '+6.7%', va='center', fontproperties=Bs(22), color=INK)
ax.text(-1.77 - 0.2, 1, '-1.8%', va='center', ha='right', fontproperties=Bs(22), color=INK)
ax.set_yticks([0, 1]); ax.set_yticklabels(['달러로 셌을 때', '원화로 셌을 때'], fontproperties=Bs(17)); ax.invert_yaxis()
ax.axvline(0, color=SUBC, lw=1); ax.set_xticks([]); ax.set_xlim(-5, 10); ax.tick_params(axis='y', length=0)
for s in ('top', 'right', 'bottom', 'left'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.12, '같은 기간 원/달러 환율 1,458.3원 → 1,331.1원(-8.7%)', fontproperties=Bs(15), color=ORG)
frame(fig, '평가액 + 세후 분배금, 처음보다 얼마나', '2025.11.18 매수 → 2026.11.18 종가 · 분배금 12번')
fig.subplots_adjust(top=0.82, bottom=0.2, left=0.24, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'jepq1120' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
