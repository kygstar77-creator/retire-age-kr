# hidiv1128 그림(divdj1127 틀) — 00 표지(10년 전 1억 세 곳 + 1년 배당률), 01 배당 현금으로 받기(남은 주식+받은 배당), 02 지수·배당 주기·총보수 표.
# 숫자는 calc_out.txt(11/25 종가) 값 — 발행 회차가 calc.py 다시 돌리면 아래 R·C·Y를 calc_out에서 다시 옮긴다.
import os, json, glob, datetime as D
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, GRY = '#111827', '#6B7280', '#EA580C', '#94A3B8'
BG = '#5B1F2C'
ES = '2026.11.25'
SRC = f'야후 파이낸스 일별 종가·배당({ES}까지) · 뱅가드·블랙록 iShares·스테이트스트리트 상품 정보 · 파이어맵 계산'
R = [('VYM', 2.8766, 2.32), ('HDV', 2.7158, 3.36), ('SPYD', 2.2289, 4.16)]   # 10년 재투자 · 1년 배당률
C = [('VYM', 2.1248, 0.4162), ('HDV', 1.8849, 0.4510), ('SPYD', 1.4060, 0.4998)]  # 현금으로 받기: 남은 주식 · 받은 배당
def won(v): m = round(v * 1e4); return f'{m//10000}억 {m%10000:,}만' if m % 10000 else f'{m//10000}억'
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '고배당 ETF 3종 10년', fontproperties=Bs(50), color='white')
fig.text(0.07, 0.785, '2016년 11월 1억원 → 지금 남은 돈', fontproperties=Bs(32), color='#FED7AA')
ax = fig.add_axes([0.06, 0.2, 0.88, 0.52]); ax.set_facecolor(BG)
vals = [v for _, v, _ in R]
ax.bar(range(3), vals, color=[ORG, GRY, GRY], width=0.6)
for i, (n, v, y) in enumerate(R):
    ax.text(i, v + 0.06, won(v).replace(' ', '\n'), ha='center', va='bottom', fontproperties=Bs(30), color='white', linespacing=1.1)
    ax.text(i, -0.08, n, ha='center', va='top', fontproperties=Bs(30), color='white')
    ax.text(i, -0.48, f'배당률 {y:.2f}%', ha='center', va='top', fontproperties=Bs(22), color='#FED7AA')
ax.set_ylim(-0.9, 3.9); ax.set_xlim(-0.55, 2.55); ax.axis('off')
fig.text(0.07, 0.085, '배당률 높은 순서와 남은 돈 순서는 거꾸로', fontproperties=Bs(28), color='white')
fig.text(0.07, 0.035, f'{ES} 종가 · 배당 다시 산 값 · 세금 떼기 전 · 달러 기준', fontsize=17, color='#FED7AA')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API VYM·HDV·SPYD 일별 종가·배당 events(11/27 받음)로 2016-11-25~2026-11-25 총수익 직접 계산, calc_out.txt',
           'made_at': str(D.date.today()), 'by': 'research/hidiv1128/mkimg.py', 'out': 'img/00.png', 'topic': '고배당 ETF 3종 10년',
           'num': '2억 8,766만 · 2억 7,158만 · 2억 2,289만 (배당률 2.32·3.36·4.16%)', 'topic_px': 50, 'num_px': 30,
           'follows': '경쟁 4 stockstudy999 표지(상품 비교 표·숫자) + 경쟁 1 royal23- 표지(VYM·HDV 이름+물음) + divdj1127 막대 위 큰 숫자'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 배당을 현금으로 받았다면 — 남은 주식 + 받은 배당(쌓은 막대)
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
x = range(3)
st = [s for _, s, _ in C]; dv = [d for _, _, d in C]
ax.bar(x, st, 0.55, color='#334155', label='남은 주식')
ax.bar(x, dv, 0.55, bottom=st, color=ORG, label='받은 배당')
for i, (n, s, d) in enumerate(C):
    ax.text(i, s / 2, f'주식\n{won(s)}', ha='center', va='center', fontproperties=Bs(15), color='white', linespacing=1.2)
    ax.text(i, s + d / 2, f'배당 {round(d*1e4):,}만', ha='center', va='center', fontproperties=Bs(14), color='white')
    ax.text(i, s + d + 0.05, f'합 {won(s + d)}', ha='center', va='bottom', fontproperties=Bs(16), color=INK)
ax.set_xticks(list(x)); ax.set_xticklabels([n for n, _, _ in C], fontproperties=Bs(18)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(0, 3.0)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
frame(fig, '배당을 현금으로 받았다면 — 10년 뒤', '2016년 11월 1억원 · 받은 배당은 SPYD가 가장 많고, 남은 주식은 VYM이 가장 많음 · 세금 떼기 전')
fig.subplots_adjust(top=0.82, bottom=0.1, left=0.04, right=0.96); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 표 — 이름 · 배당 주는 때 · 총보수 (3칸)
G = [('VYM', '석 달마다', '연 0.04%'), ('HDV', '매달 (2026년 6월부터)', '연 0.08%'), ('SPYD', '석 달마다', '연 0.07%')]
fig, ax = plt.subplots(figsize=(9, 6.0), dpi=100); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 4.4)
ax.text(0.3, 3.85, '이름', fontproperties=Bs(16), color=SUBC); ax.text(2.4, 3.85, '배당 주는 때', fontproperties=Bs(16), color=SUBC)
ax.text(7.6, 3.85, '총보수', fontproperties=Bs(16), color=SUBC)
for i, (n, g, f) in enumerate(G):
    yy = 3.0 - i * 1.05
    ax.text(0.3, yy, n, fontproperties=Bs(24), color=INK, va='center')
    ax.text(2.4, yy, g, fontproperties=Bs(20), color=ORG if '매달' in g else INK, va='center')
    ax.text(7.6, yy, f, fontproperties=Bs(20), color=INK, va='center')
    if i < 2: ax.plot([0.3, 9.7], [yy - 0.52, yy - 0.52], color='#E5E7EB', lw=1.5)
frame(fig, '배당 주는 때와 총보수', '운용사 상품 페이지 기준(11/27 확인) · 총보수는 1년에 떼는 운용 비용')
fig.subplots_adjust(top=0.8, bottom=0.08, left=0.02, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'hidiv1128' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
