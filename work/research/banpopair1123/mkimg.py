# banpopair1123 그림(jamsilpair1120 틀) — 00 표지(차트: 2026년 5월 84㎡대 11건 값 점), 01 최근 1년 20건 계약 달·값, 02 해마다 같은 달 가장 큰 차이. 숫자는 calc_out.txt 그대로
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
INK, SUBC, ORG, GRY = '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = '국토교통부 아파트 매매 실거래 · 서울 서초구 반포동 래미안원베일리(11/22 받음, 전용 84㎡대, 해제 거래 뺌) · 파이어맵 계산'
may = [53.5, 53.5, 55.5, 56.0, 57.5, 59.0, 59.0, 60.0, 60.3, 65.0, 71.5]
TOPIC_PX, NUM_PX = 54, 40
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#1E3A5F')
fig.text(0.07, 0.86, '래미안원베일리 84㎡', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.77, '2026년 5월 한 달, 거래 11건', fontproperties=Bs(32), color='#BFDBFE')
ax = fig.add_axes([0.08, 0.3, 0.84, 0.36]); ax.set_facecolor('#1E3A5F')
seen = {}
for v in may:
    k = seen.get(v, 0); seen[v] = k + 1
    ax.scatter(v, 0.35 * k, s=520, color='#FB923C' if v in (53.5, 71.5) else '#CBD5E1', zorder=3)
ax.annotate('', xy=(71.5, -0.75), xytext=(53.5, -0.75), arrowprops=dict(arrowstyle='<->', color='white', lw=2.5))
ax.text(62.5, -1.05, '18억 차이', ha='center', va='top', fontproperties=Bs(NUM_PX), color='white')
ax.text(54.2, 0.8, '53억 5천', ha='center', fontproperties=Bs(36), color='white')
ax.text(70.6, 0.45, '71억 5천', ha='center', fontproperties=Bs(36), color='white')
ax.set_xlim(50, 75); ax.set_ylim(-1.9, 1.3); ax.axis('off')
fig.text(0.07, 0.15, '가운데 값 59억 · 모두 중개거래', fontproperties=Bs(28), color='white')
fig.text(0.07, 0.07, '국토부 실거래(11/22 조회) · 파이어맵 계산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(서울 서초구 11650 반포동 래미안원베일리) 2026-05 계약 전용 84㎡대 11건, calc_out.txt §2 — 파이어맵 직접 계산',
           'made_at': '2026-11-22', 'by': 'research/banpopair1123/mkimg.py', 'out': 'img/00.png', 'topic': '래미안원베일리 84㎡', 'num': '18억 차이',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 dividendqueen/224469111492·2 trader_wooahpapa/224468569672 실거래 표·값 비교'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=9.5, color=SUBC)
# 01 최근 1년 20건
pts = [(0, 60.0), (2, 60.8)] + [(5, v) for v in (54.5, 56.3, 58.5, 59.5, 64.0)] + [(6, v) for v in may] + [(7, 56.3), (11, 57.0)]
mon = ['25.11', '12', '26.1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
ax.axhline(58.75, color=GRY, lw=1.5, ls='--'); ax.text(11.4, 58.75, '가운데 값\n약 58.8억', va='center', fontsize=12, color=SUBC)
for x, v in pts:
    c = ORG if (x, v) in ((6, 71.5), (11, 57.0)) else '#64748B'
    ax.scatter(x, v, s=110, color=c, zorder=3, alpha=0.85)
ax.annotate('71억 5천 (13층)', xy=(6, 71.5), xytext=(7.3, 70.5), fontproperties=Bs(15), color=ORG, arrowprops=dict(arrowstyle='-', color=ORG))
ax.annotate('57억 (7층)\n10월 14일 계약', xy=(11, 57.0), xytext=(8.6, 52.2), fontproperties=Bs(15), color=ORG, arrowprops=dict(arrowstyle='-', color=ORG))
ax.annotate('53억 5천 (6층·2층)', xy=(6, 53.5), xytext=(1.4, 51.5), fontproperties=Bs(15), color=INK, arrowprops=dict(arrowstyle='-', color=SUBC))
ax.set_xticks(range(12)); ax.set_xticklabels(mon, fontsize=12); ax.set_xlim(-0.6, 12.6)
ax.set_ylim(50, 74); ax.set_yticks([55, 60, 65, 70]); ax.set_yticklabels(['55억', '60억', '65억', '70억'], fontsize=12, color=SUBC)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.grid(axis='y', color='#E5E7EB')
frame(fig, '최근 1년 거래 20건, 계약한 달과 값', '2025년 11월~2026년 10월 계약 · 점 하나가 거래 한 건 · 20건 중 16건이 4~5월')
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.09, right=0.97); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 해마다 같은 달 가장 큰 차이
yrs = ['2023년 9월\n(4건)', '2024년 8월\n(6건)', '2025년 2월\n(9건)', '2026년 5월\n(11건)']; d = [5.5, 13.0, 17.5, 18.0]
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
ax.bar(range(4), d, width=0.55, color=['#CBD5E1', '#CBD5E1', '#CBD5E1', ORG])
for i, v in enumerate(d): ax.text(i, v + 0.4, f'{v:g}억', ha='center', va='bottom', fontproperties=Bs(20), color=INK)
ax.set_xticks(range(4)); ax.set_xticklabels(yrs, fontproperties=Bs(14)); ax.tick_params(axis='x', length=0, pad=8)
ax.set_yticks([]); ax.set_ylim(0, 22)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
frame(fig, '한 달 안에서 가장 싼 거래와 비싼 거래의 차이', '해마다 그 차이가 가장 컸던 달(거래 3건 이상인 달) · 84㎡대')
fig.subplots_adjust(top=0.82, bottom=0.16, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'banpopair1123' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
