# plusdiv1128 그림(hidiv1128 틀) — 00 표지(10년 매달 100만원 두 곳 끝값), 01 10년 적립 평가액 흐름(6/22 고점 표시), 02 기간별 3칸 표.
# 숫자는 calc_out.txt(2026-11-27 종가) — calc.py와 같은 규칙으로 흐름을 다시 셈(세후 15.4% 재투자, 11월 분배 103원 보탬).
import os, json, glob, datetime as D
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, NAVY, GRY = '#111827', '#6B7280', '#EA580C', '#1E3A5F', '#94A3B8'
BG = '#3A2F0B'
ES = '2026.11.27'
SRC = f'야후 파이낸스 일별 종가·분배({ES}까지) · 한화자산운용·삼성자산운용 상품 정보 · 파이어맵 계산'
END = D.date(2026, 11, 27); START = D.date(2016, 12, 1)
def load(t):
    r = json.load(open(f'raw/{t}.json'))['chart']['result'][0]
    ts = [D.date.fromtimestamp(x) for x in r['timestamp']]
    cl = r['indicators']['quote'][0]['close']
    px = [(d, c) for d, c in zip(ts, cl) if c and START <= d <= END]
    dv = {D.date.fromtimestamp(int(k)): v['amount'] for k, v in r.get('events', {}).get('dividends', {}).items()}
    if t == '161510.KS': dv.setdefault(D.date(2026, 11, 27), 103.0)
    return px, dv
def series(t):
    px, dv = load(t); sh = 0; mon = None; out = []
    for d, c in px:
        if (d.year, d.month) != mon: mon = (d.year, d.month); sh += 1_000_000 / c
        if d in dv: sh += sh * dv[d] * 0.846 / c
        out.append((d, sh * c / 1e8))
    return out
P = series('161510.KS'); K = series('069500.KS')
assert abs(P[-1][1] - 2.5013) < 0.0006 and abs(K[-1][1] - 2.9005) < 0.0006, (P[-1], K[-1])
def won(v): m = round(v * 1e4); return f'{m//10000}억 {m%10000:,}만' if m % 10000 else f'{m//10000}억'
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, 'PLUS 고배당주 10년 적립', fontproperties=Bs(48), color='white')
fig.text(0.07, 0.785, '매달 100만원씩 120번, 넣은 돈 1억 2,000만원', fontproperties=Bs(28), color='#FDE68A')
ax = fig.add_axes([0.08, 0.2, 0.84, 0.52]); ax.set_facecolor(BG)
R = [('KODEX 200', K[-1][1], GRY), ('PLUS 고배당주', P[-1][1], ORG)]
ax.bar(range(2), [v for _, v, _ in R], color=[c for _, _, c in R], width=0.55)
for i, (n, v, _) in enumerate(R):
    ax.text(i, v + 0.07, won(v) + '원', ha='center', va='bottom', fontproperties=Bs(34), color='white')
    ax.text(i, -0.1, n, ha='center', va='top', fontproperties=Bs(30), color='white')
ax.axhline(1.2, color='#FDE68A', lw=2, ls='--'); ax.text(-0.52, 1.25, '넣은 돈', ha='left', va='bottom', fontproperties=Bs(20), color='#FDE68A')
ax.set_ylim(-0.55, 3.6); ax.set_xlim(-0.55, 1.55); ax.axis('off')
fig.text(0.07, 0.085, '10년 끝값은 코스피200 쪽이 4,000만원 가까이 더', fontproperties=Bs(28), color='white')
fig.text(0.07, 0.035, f'{ES} 종가 · 분배금 세금 15.4% 떼고 다시 산 값', fontsize=17, color='#FDE68A')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API 161510.KS·069500.KS 일별 종가·분배 events(11/28 받음, 네이버페이 증권 종가와 대조)로 2016-12~2026-11 매달 100만원 적립 직접 계산, calc_out.txt',
           'made_at': str(D.date.today()), 'by': 'research/plusdiv1128/mkimg.py', 'out': 'img/00.png', 'topic': 'PLUS 고배당주 10년 적립',
           'num': '2억 9,005만 · 2억 5,013만 (넣은 돈 1억 2,000만)', 'topic_px': 48, 'num_px': 34,
           'follows': '경쟁 3 wisefather1113 표지(PLUS vs 코스피200 숫자 비교 표) + 경쟁 7 stock_nomad 적립식 회차 카드 + hidiv1128 막대 위 큰 숫자'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 10년 적립 평가액 흐름
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.plot([d for d, _ in K], [v for _, v in K], color=NAVY, lw=2.4, label='KODEX 200')
ax.plot([d for d, _ in P], [v for _, v in P], color=ORG, lw=2.4, label='PLUS 고배당주')
paid = []; mon = None; s = 0
for d, _ in K:
    if (d.year, d.month) != mon: mon = (d.year, d.month); s += 0.01
    paid.append((d, s))
ax.plot([d for d, _ in paid], [v for _, v in paid], color=GRY, lw=1.6, ls='--', label='넣은 돈')
pk = D.date(2026, 6, 22)
kv = dict(K)[pk]; pv = dict(P)[pk]
ax.scatter([pk, pk], [kv, pv], color=[NAVY, ORG], zorder=5, s=40)
ax.annotate(f'6월 22일\n{won(kv)}', (pk, kv), xytext=(D.date(2023, 6, 1), 5.0), fontproperties=Bs(14), color=NAVY, arrowprops=dict(arrowstyle='-', color=NAVY, lw=1))
ax.annotate(f'6월 22일 {won(pv)}', (pk, pv), xytext=(D.date(2021, 1, 1), 3.55), fontproperties=Bs(13), color=ORG, arrowprops=dict(arrowstyle='-', color=ORG, lw=1))
ax.annotate(f'11월 27일 {won(K[-1][1])}', (END, K[-1][1]), xytext=(D.date(2021, 3, 1), 2.75), fontproperties=Bs(14), color=NAVY, arrowprops=dict(arrowstyle='-', color=NAVY, lw=1))
ax.annotate(f'11월 27일 {won(P[-1][1])}', (END, P[-1][1]), xytext=(D.date(2023, 9, 1), 0.35), fontproperties=Bs(14), color=ORG, arrowprops=dict(arrowstyle='-', color=ORG, lw=1))
ax.set_yticks([0, 1, 2, 3, 4, 5, 6]); ax.set_yticklabels(['0', '1억', '2억', '3억', '4억', '5억', '6억'], fontsize=12)
ax.xaxis.set_major_locator(mdates.YearLocator(2)); ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.tick_params(labelsize=12); ax.grid(axis='y', color='#E5E7EB'); ax.set_ylim(0, 6.2)
for s_ in ('top', 'right'): ax.spines[s_].set_visible(False)
ax.legend(loc='upper left', frameon=False, prop=Bs(13))
frame(fig, '10년 모은 돈, 날마다 얼마였나', '2016년 12월부터 매달 100만원 · 분배금은 세금 떼고 다시 삼 · 6월 22일은 코스피200 쪽이 가장 높았던 날')
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.08, right=0.97); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 표 — 기간 · KODEX 200 · PLUS 고배당주 (3칸)
G = [('10년 (1억 2,000만)', '2억 9,005만', '2억 5,013만'), ('5년 (6,000만)', '1억 2,041만', '9,917만'), ('3년 (3,600만)', '6,155만', '4,692만')]
fig, ax = plt.subplots(figsize=(9, 6.0), dpi=100); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 4.4)
ax.text(0.3, 3.85, '기간 (넣은 돈)', fontproperties=Bs(16), color=SUBC); ax.text(4.6, 3.85, 'KODEX 200', fontproperties=Bs(16), color=SUBC)
ax.text(7.4, 3.85, 'PLUS 고배당주', fontproperties=Bs(16), color=SUBC)
for i, (n, k, p) in enumerate(G):
    yy = 3.0 - i * 1.05
    ax.text(0.3, yy, n, fontproperties=Bs(19), color=INK, va='center')
    ax.text(4.6, yy, k, fontproperties=Bs(22), color=NAVY, va='center')
    ax.text(7.4, yy, p, fontproperties=Bs(22), color=ORG, va='center')
    if i < 2: ax.plot([0.3, 9.7], [yy - 0.52, yy - 0.52], color='#E5E7EB', lw=1.5)
frame(fig, '매달 100만원, 기간별로 지금 남은 돈', f'{ES} 종가 · 분배금 세금 떼고 다시 산 값 · 단위 원')
fig.subplots_adjust(top=0.8, bottom=0.08, left=0.02, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'plusdiv1128' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok', won(kv), won(pv))
