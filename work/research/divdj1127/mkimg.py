# divdj1127 그림(k200etf1126 틀) — 00 표지(2024-08-13 1억 네 곳), 01 해마다 폭, 02 기준일·1년 분배율. 숫자는 calc_out.txt(11/25 종가) 값
import os, json, glob, datetime as D
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG = '#111827', '#6B7280', '#EA580C'
ES = '2026.11.25'
SRC = f'야후 파이낸스 일별 종가·분배({ES}까지) · 운용사 상품 정보 · 네이버페이 증권 · 파이어맵 계산'
R = [('KODEX', 1.3748), ('TIGER', 1.3681), ('ACE', 1.3653), ('SOL', 1.3645)]
def won(v): m = round(v * 1e4); return f'{m//10000}억\n{m%10000:,}만'
vals = [v for _, v in R]; gap = round((max(vals) - min(vals)) * 1e4)
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#0E4A43')
fig.text(0.07, 0.86, '미국배당다우존스 ETF 4종', fontproperties=Bs(50), color='white')
fig.text(0.07, 0.785, '2024년 8월 13일 1억원씩 넣었다면', fontproperties=Bs(32), color='#FED7AA')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.55]); ax.set_facecolor('#0E4A43')
ax.bar(range(4), vals, color=['#FB923C', '#94A3B8', '#94A3B8', '#94A3B8'], width=0.62)
for i, (n, v) in enumerate(R):
    ax.text(i, v + 0.03, won(v), ha='center', va='bottom', fontproperties=Bs(28 if i else 30), color='white', linespacing=1.1)
    ax.text(i, -0.03, n, ha='center', va='top', fontproperties=Bs(26), color='white')
ax.set_ylim(-0.2, 1.75); ax.set_xlim(-0.6, 3.6); ax.axis('off')
fig.text(0.07, 0.1, f'네 곳 차이 {gap:,}만원', fontproperties=Bs(30), color='white')
fig.text(0.07, 0.045, f'{ES} 종가 · 받은 분배금으로 더 산 값 · 세금 떼기 전', fontsize=17, color='#FED7AA')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API 402970·446720·458730·489250.KS 일별 종가·분배 events(11/26 받음)로 2024-08-13~2026-11-25 총수익 직접 계산, calc_out.txt',
           'made_at': str(D.date.today()), 'by': 'research/divdj1127/mkimg.py', 'out': 'img/00.png', 'topic': '미국배당다우존스 ETF 4종',
           'num': f'1억 3,645만~1억 3,748만 · 차이 {gap:,}만원', 'topic_px': 50, 'num_px': 30,
           'follows': '경쟁 1 kjckyl4632 4종 비교 표지(상품 이름 4개+숫자) + k200etf1126·ndxetf1122 막대 위 큰 숫자'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 해마다 폭
Y = {2025: {'ACE': 1.52, 'SOL': 1.87, 'TIGER': 2.35, 'KODEX': 1.98}, 2026: {'ACE': 19.77, 'SOL': 19.27, 'TIGER': 19.35, 'KODEX': 19.72}}
fig, axs = plt.subplots(1, 2, figsize=(9, 6.6), dpi=100)
for ax, y in zip(axs, Y):
    d = sorted(Y[y].items(), key=lambda kv: -kv[1]); x = np.arange(4)
    ax.bar(x, [v for _, v in d], 0.6, color=[ORG] + ['#94A3B8'] * 3)
    for i, (n, v) in enumerate(d):
        ax.text(i, v * 1.02, f'{v:.2f}%', ha='center', va='bottom', fontproperties=Bs(13), color=INK)
    ax.set_xticks(x); ax.set_xticklabels([n for n, _ in d], fontproperties=Bs(13)); ax.tick_params(axis='x', length=0)
    ax.set_yticks([]); ax.set_ylim(0, max(Y[y].values()) * 1.22)
    for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
    sp = max(Y[y].values()) - min(Y[y].values())
    ax.set_title(f"{y}년{'(11/25까지)' if y == 2026 else ''} · 폭 {sp:.2f}%p", fontproperties=Bs(15), color=INK, pad=14)
frame(fig, '해마다 네 곳 수익률 — 폭은 1%포인트 안', '분배금 받은 날 다시 삼 · 세금 떼기 전 · 네 곳이 한 해를 다 채운 해부터')
fig.subplots_adjust(top=0.78, bottom=0.1, left=0.03, right=0.97, wspace=0.15); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 기준일 두 갈래 + 1년 분배율·총보수
G = [('SOL', '매월 마지막 영업일', 2.99, '0.01%'), ('TIGER', '매월 마지막 영업일', 2.96, '0.01%'),
     ('KODEX', '매월 15일', 2.98, '0.0099%'), ('ACE', '달 중순(월중)', 2.96, '0.01%')]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 5)
ax.text(0.2, 4.55, '이름', fontproperties=Bs(15), color=SUBC); ax.text(2.4, 4.55, '분배금 기준일', fontproperties=Bs(15), color=SUBC)
ax.text(7.4, 4.55, '1년 분배율', fontproperties=Bs(15), color=SUBC)
for i, (n, g, r, f) in enumerate(G):
    yy = 3.7 - i * 0.95 - (0.25 if i >= 2 else 0)
    c = ORG if i < 2 else '#2563EB'
    ax.text(0.2, yy, n, fontproperties=Bs(22), color=INK, va='center'); ax.text(2.4, yy, g, fontproperties=Bs(19), color=c, va='center')
    ax.text(7.4, yy, f'{r:.2f}%', fontproperties=Bs(19), color=INK, va='center')
ax.plot([0.2, 9.8], [2.05, 2.05], color='#E5E7EB', lw=2)
frame(fig, '분배금 기준일은 월말과 월중 두 갈래', f'1년 분배율 = 최근 1년 1주 분배금 합 ÷ {ES} 종가 · ACE 기준일은 2차 자료(펀드닷컴·네이버)')
fig.subplots_adjust(top=0.82, bottom=0.08, left=0.02, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'divdj1127' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok', gap)
