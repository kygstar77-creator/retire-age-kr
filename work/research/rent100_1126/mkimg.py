# rent100_1126 그림(geomdan1125 틀) — 00 표지(차트: 부동산원 평균 168만 vs 실거래 중간 80만), 01 구별 월세 중간값 2026.8~10, 02 1년 전 vs 지금(전체·59㎡·84㎡·신규·갱신 중 비교 가능한 것). 숫자는 calc_out 그대로
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
BLUE, INK, SUBC, ORG, GRAY = '#1D4ED8', '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = '국토교통부 아파트 전월세 실거래 · 서울 25개 구 월세 계약(월세 1만원 이상, 11/24 받음) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 44
BG = '#3B1F4A'
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '서울 아파트 월세', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '평균 말고 한가운데는?', fontproperties=Bs(38), color='#F5D0FE')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor(BG)
vals = [168.1, 80]; labs = ['부동산원 평균', '실거래 중간값']; txt = ['168만', '80만']
ax.bar(range(2), vals, color=[GRAY, '#FB923C'], width=0.5)
for i in range(2):
    ax.text(i, vals[i] + 5, txt[i], ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -6, labs[i], ha='center', va='top', fontproperties=Bs(26), color='white')
ax.set_ylim(-40, 215); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '2026년 8~10월 월세 계약 2만 5,978건', fontproperties=Bs(22), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산 / 평균은 한국부동산원 10월', fontsize=17, color='#F5D0FE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 전월세 실거래 API(서울 25개 구) 2026.8~10월 월세 계약 중간값(calc_out.txt, 파이어맵 직접 계산) · 평균 168만 1천원은 한국부동산원 2026년 10월 전국주택가격동향조사(2차: 경쟁 2·5 글)',
           'made_at': '2026-11-24', 'by': 'research/rent100_1126/mkimg.py', 'out': 'img/00.png', 'topic': '서울 아파트 월세', 'num': '168만 / 80만',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 2 twal3/224487861043 구별 평균 월세 막대 차트 · 7 saltzzza/224486860235 첫 그림 큰 숫자 카드'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.95, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.915, sub, fontsize=13, color=SUBC)
    fig.text(0.04, 0.015, SRC, fontsize=9.5, color=SUBC)
G = [('용산구',160),('서초구',160),('중구',144),('성동구',140),('강남구',132),('송파구',120),('종로구',118.5),('성북구',100),('서대문구',100),('마포구',95),('광진구',90),('양천구',88),('강북구',85),('강동구',85),('동대문구',80),('도봉구',80),('노원구',80),('동작구',80),('관악구',67),('영등포구',60),('강서구',54),('구로구',52),('금천구',52),('은평구',41),('중랑구',35)]
fig, ax = plt.subplots(figsize=(9, 11), dpi=100)
ys = range(len(G))[::-1]
ax.barh(list(ys), [g[1] for g in G], color=[ORG if g[1] >= 100 else BLUE for g in G], height=0.68)
for y, (nm, v) in zip(ys, G):
    ax.text(v + 2, y, (f'{v:g}만'), va='center', fontproperties=Bs(13), color=INK)
ax.set_yticks(list(ys)); ax.set_yticklabels([g[0] for g in G], fontproperties=Bs(13)); ax.tick_params(axis='y', length=0)
ax.axvline(100, color=SUBC, lw=1, ls='--'); ax.text(101, len(G) - 0.3, '100만원', fontsize=11, color=SUBC)
ax.set_xticks([]); ax.set_xlim(0, 185)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
frame(fig, '구별 아파트 월세 중간값', '2026년 8~10월 월세 계약 · 주황 = 중간값 100만원 이상(9곳)')
fig.subplots_adjust(top=0.89, bottom=0.04, left=0.13, right=0.97); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
G = [('서울 전체', 80, 80), ('59㎡ 안팎\n(55~61㎡)', 100, 110), ('84㎡ 안팎\n(80~86㎡)', 150, 158)]
w = 0.36
for i, (lab, a, b) in enumerate(G):
    ax.bar(i - w/2, a, w, color=GRAY); ax.bar(i + w/2, b, w, color=ORG)
    ax.text(i - w/2, a + 3, f'{a}만', ha='center', fontproperties=Bs(15), color=SUBC)
    ax.text(i + w/2, b + 3, f'{b}만', ha='center', fontproperties=Bs(15), color=ORG)
ax.set_xticks(range(3)); ax.set_xticklabels([g[0] for g in G], fontproperties=Bs(15)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(0, 190)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.bar([0], [0], color=GRAY, label='2025년 8~10월'); ax.bar([0], [0], color=ORG, label='2026년 8~10월'); ax.legend(frameon=False, loc='upper left', fontsize=12)
ax.text(0, 118, '월세 계약 보증금 중간\n1억 → 1억 2,240만', ha='center', fontproperties=Bs(13), color=INK)
frame(fig, '전체는 그대로, 넓이별로는 올랐다', '서울 아파트 월세 계약 중간값 · 1년 전 같은 석 달과 비교')
fig.subplots_adjust(top=0.86, bottom=0.12, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [q for q in recent if 'rent100_1126' not in q][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, q in enumerate(recent): board.paste(Image.open(q).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
