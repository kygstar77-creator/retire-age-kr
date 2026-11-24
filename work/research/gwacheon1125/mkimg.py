# gwacheon1125 그림(gwanggyo1125 틀) — 00 표지(차트: 1년 평당가 vs 같은 집), 01 반기 매매 건수, 02 갈래별 1년. 숫자는 calc_out 그대로
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
BLUE, INK, SUBC, ORG, GREY = '#1D4ED8', '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = '국토교통부 아파트 매매 실거래 · 경기 과천시(11/25 받음, 취소된 거래 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 44
BG = '#7C2D12'
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '과천 아파트 시세', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '1년, 무엇으로 재느냐에 따라', fontproperties=Bs(38), color='#FFEDD5')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor(BG)
vals = [-1.5, 6.7]; labs = ['평당가', '같은 집끼리']; txt = ['-1.5%', '+7%']
ax.bar(range(2), vals, color=[GREY, '#FB923C'], width=0.5)
for i in range(2):
    ax.text(i, max(vals[i], 0) + 0.4, txt[i], ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -2.4, labs[i], ha='center', va='top', fontproperties=Bs(26), color='white')
ax.axhline(0, color='#FFEDD5', lw=1.5)
ax.set_ylim(-6, 11); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '평당가: 시세 사이트 래더프라이스 · 같은 집: 같은 단지·같은 넓이 중간값', fontproperties=Bs(20), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#FFEDD5')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(경기 과천시 41290) 2025.6~10월 vs 2026.6~10월 계약 같은 집 중간값(calc_out.txt) · 평당가 1년 -1.5%는 래더프라이스 https://blog.naver.com/ladderprice/224484575044 (2차)',
           'made_at': '2026-11-25', 'by': 'research/gwacheon1125/mkimg.py', 'out': 'img/00.png', 'topic': '과천 아파트 시세', 'num': '-1.5% / +7%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 2 ladderprice/224484575044 동별 시세 표 · 5 team_12/224486930728 국평 비교 표'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
import numpy as np
# 01 반기 매매 건수
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
hl = ['2024년 하반기', '2025년 상반기', '2025년 하반기', '2026년 상반기']; tot = [314, 596, 189, 165]; jg = [59, 81, 16, 4]
x = np.arange(4)
ax.bar(x, tot, 0.55, color=['#CBD5E1', '#CBD5E1', '#FB923C', '#FB923C'])
ax.bar(x, jg, 0.55, color='#475569', label='그중 남은 주공 5개 단지')
for i in range(4):
    ax.text(x[i], tot[i] + 10, f'{tot[i]}건', ha='center', fontproperties=Bs(20), color=INK)
ax.set_xticks(x); ax.set_xticklabels(hl, fontproperties=Bs(15)); ax.set_yticks([]); ax.set_ylim(0, 690)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.legend(prop=Bs(14), frameon=False, loc='upper right')
frame(fig, '과천 아파트 매매, 반년마다 몇 건', '계약 기준 · 취소된 거래 뺌 · 2026년 상반기 주공은 4건')
fig.subplots_adjust(top=0.82, bottom=0.16, left=0.06, right=0.97); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 갈래별 1년
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['지식정보타운 갈현동 (평형 7개)', '재건축 새 단지 5곳 (평형 15개)', '래미안 두 단지 (평형 8개)']; v = [11.5, 6.9, 4.0]
y = list(range(3))[::-1]
ax.barh(y, v, color=['#93C5FD', '#FB923C', GREY], height=0.55)
for yy, xx in zip(y, v): ax.text(xx + 0.3, yy, f'약 {int(xx + 0.5)}%', va='center', ha='left', fontproperties=Bs(22), color=INK)
ax.set_yticks(y); ax.set_yticklabels(labs, fontproperties=Bs(15)); ax.tick_params(axis='y', length=0, pad=8)
ax.set_xticks([]); ax.set_xlim(0, 16); ax.axvline(0, color=INK, lw=1)
for s_ in ('top', 'left', 'bottom', 'right'): ax.spines[s_].set_visible(False)
frame(fig, '단지 갈래별 1년 오른 폭', '같은 단지·같은 넓이 매매 중간값 · 2025년 6~10월 → 2026년 6~10월 · 주공은 평형 3개뿐이라 뺌')
fig.subplots_adjust(top=0.82, bottom=0.08, left=0.4, right=0.97); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'gwacheon1125' not in p and 'gwanggyo1125' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok', [os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(p)))) for p in recent])
