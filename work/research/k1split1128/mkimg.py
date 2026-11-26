# k1split1128 그림 — 00 표지(나눈 횟수별 1년 뒤 가장 나빴을 때~가장 좋았을 때), 01 나눠 넣은 쪽이 앞선 5번, 02 2년 뒤.
# 숫자는 calc.py → calc_out.txt(한국은행 ECOS 코스피 일별 종가 11/26 받음).
import os, json, glob, statistics as st, datetime as D
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, BG = '#111827', '#6B7280', '#EA580C', '#2B1B3F'
SRC = '한국은행 경제통계시스템 코스피 일별 종가(원자료 한국거래소) · 파이어맵 계산 · 지수 값만(배당·세금·수수료 뺌)'
rows = json.load(open('raw/kospi_daily_ecos_1126.json'))
ch = [(rows[i][0], rows[i][1], (rows[i][1]/rows[i-1][1]-1)*100, i) for i in range(1, len(rows))]
eps = []; last = -999
for d, v, c, i in ch:
    if c <= -5:
        if i - last > 60: eps.append((d, v, c, i))
        last = i
T = 1e7
def val(i, n, h): return sum((T/n)/rows[i+21*k][1] for k in range(n))*rows[i+h][1]
N = (1, 3, 6, 12)
y1 = {n: [val(i, n, 252) for d, v, c, i in eps if i+252 < len(rows)] for n in N}
d1 = [d for d, v, c, i in eps if i+252 < len(rows)]
y2 = {n: [val(i, n, 504) for d, v, c, i in eps if i+504 < len(rows)] for n in N}
man = lambda x: f'{x/1e4:,.0f}만'
# 00 표지 — 범위 막대
TOPIC_PX, NUM_PX = 54, 36
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.87, '코스피 폭락한 날 1천만원', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.80, '몇 번에 나눠 넣었나 · 1년 뒤 남은 돈(15번)', fontproperties=Bs(28), color='#FED7AA')
ax = fig.add_axes([0.08, 0.17, 0.86, 0.58]); ax.set_facecolor(BG)
lab = {1: '한 번에', 3: '3번', 6: '6번', 12: '12번'}
for k, n in enumerate(N):
    lo, md, hi = min(y1[n]), st.median(y1[n]), max(y1[n])
    ax.plot([k, k], [lo, hi], color='#FB923C' if n != 1 else '#F8FAFC', lw=22, solid_capstyle='butt', alpha=0.9)
    ax.scatter([k], [md], s=260, color=BG, edgecolor='white', lw=3, zorder=3)
    ax.text(k, hi + 9e5, man(hi), ha='center', fontproperties=Bs(21), color='white')
    ax.text(k, lo - 1.6e6, man(lo), ha='center', fontproperties=Bs(21), color='#FED7AA')
    ax.text(k, 1e6, lab[n], ha='center', fontproperties=Bs(25), color='white')
ax.axhline(T, color='#94A3B8', lw=1.2, ls='--'); ax.text(3.55, T, '원금', va='center', fontsize=15, color='#CBD5E1')
ax.set_xlim(-0.6, 3.9); ax.set_ylim(0, 2.95e7); ax.axis('off')
fig.text(0.07, 0.095, '나눌수록 가장 나쁜 해는 덜 잃고, 좋은 해는 덜 벌었다', fontproperties=Bs(25), color='white')
fig.text(0.07, 0.045, '막대 위 가장 좋았을 때 · 아래 가장 나빴을 때 · 동그라미 가운데 값', fontsize=16, color='#FED7AA')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '한국은행 ECOS 802Y001/0001000 코스피 일별 종가(raw/kospi_daily_ecos_1126.json)로 calc.py가 센 1년 뒤 값, calc_out.txt',
           'made_at': str(D.date.today()), 'by': 'research/k1split1128/mkimg.py', 'out': 'img/00.png', 'topic': '코스피 폭락한 날 1천만원',
           'num': '나눈 횟수별 1년 뒤 가장 나빴을 때~가장 좋았을 때', 'topic_px': TOPIC_PX, 'num_px': NUM_PX,
           'follows': '경쟁 1 divfree 첫 그림(정액분할 표) · 경쟁 3 mirandbfk12 글자 카드(한 번에 살까 나눠서 살까) + 우리 잘된 글 k200etf1126·ndxetf1122 막대 차트 표지'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
def table(fname, title, sub, head, body, hi_col=None):
    fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, len(body) + 1.6)
    xs = [0.5, 4.4, 7.4]
    for j, h in enumerate(head): ax.text(xs[j], len(body) + 0.9, h, fontproperties=Bs(16), color=SUBC)
    for r, row in enumerate(body):
        y = len(body) - r - 0.1
        if r % 2 == 0: ax.add_patch(plt.Rectangle((0.3, y - 0.42), 9.4, 0.84, color='#F8FAFC', zorder=0))
        for j, cell in enumerate(row):
            ax.text(xs[j], y, cell, va='center', fontproperties=Bs(18), color=ORG if j == hi_col else INK)
    frame(fig, title, sub)
    fig.subplots_adjust(top=0.84, bottom=0.07, left=0.02, right=0.98); fig.savefig(fname, dpi=100); plt.close(fig)
def ymd(d): return f'{d[:4]}.{int(d[4:6])}.{int(d[6:])}'
won = [(ymd(d), man(a), man(b)) for d, a, b in zip(d1, y1[1], y1[12]) if b > a]
table('pkg/img/01.png', '12번 나눠 넣은 쪽이 더 남은 5번', '1천만원 · 폭락한 첫날부터 21거래일마다 나눠 넣고 1년 뒤 종가로 셈 · 나머지 10번은 한 번에가 더 남음',
      ['폭락한 첫날', '한 번에', '12번 나눠'], won, hi_col=2)
body2 = [(lab[n], man(st.median(y2[n])), f'{sum(x < T for x in y2[n])}번') for n in N]
table('pkg/img/02.png', '2년 뒤로 늘려 보면(14번)', '같은 방법으로 넣고 첫날부터 2년 뒤 종가로 셈 · 2025.4.7은 아직 2년이 안 돼 뺌',
      ['나눈 횟수', '가운데 값', '원금 아래로 끝난 횟수'], body2, hi_col=1)
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'k1split1128' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok', won, body2)
