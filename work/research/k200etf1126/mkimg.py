# k200etf1126 그림(ndxetf1122 틀) — 00 표지(네 곳 1억 결과), 01 해마다 네 곳 차이, 02 1년 분배금·총보수. 숫자는 calc.py로 바로 셈(다시 받으면 그대로 다시 그림)
import os, json, glob, sys, datetime as D
os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '.')
import calc
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG = '#111827', '#6B7280', '#EA580C'
E = calc.END; ES = f'{E.year}.{E.month:02d}.{E.day:02d}'
SRC = f'야후 파이낸스 일별 종가·분배({ES}까지) · 네이버페이 증권 · 미래에셋 상품 정보 · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 40
def won(v):  # 억 단위 → '4억\n1,597만'
    m = round(v * 1e4); return f'{m//10000}억\n{m%10000:,}만'
out = sorted(calc.run(D.date(2011, 10, 20), quiet=True), key=lambda r: -r[3])
nm = [r[0].split()[0] for r in out]; vals = [r[3] for r in out]
gap = round((max(vals) - min(vals)) * 1e4)
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#0F2A44')
fig.text(0.07, 0.86, '코스피200 ETF 4종', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.785, '2011년 10월 20일 1억원씩 넣었다면', fontproperties=Bs(32), color='#FED7AA')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.55]); ax.set_facecolor('#0F2A44')
ax.bar(range(4), vals, color=['#FB923C', '#94A3B8', '#94A3B8', '#94A3B8'], width=0.62)
for i, v in enumerate(vals):
    ax.text(i, v + 0.1, won(v), ha='center', va='bottom', fontproperties=Bs(28 if i else 30), color='white', linespacing=1.1)
    ax.text(i, -0.12, nm[i], ha='center', va='top', fontproperties=Bs(26), color='white')
ax.set_ylim(-0.8, 5.6); ax.set_xlim(-0.6, 3.6); ax.axis('off')
fig.text(0.07, 0.1, f'15년 뒤 차이 {gap:,}만원', fontproperties=Bs(NUM_PX - 10), color='white')
fig.text(0.07, 0.045, f'{ES} 종가 · 받은 분배금으로 다시 산 값 · 세금 떼기 전', fontsize=17, color='#FED7AA')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': f'야후 파이낸스 chart API 069500·102110·148020·105190.KS 일별 종가·분배 events(11/24 받음)로 2011-10-20~{E} 총수익 직접 계산, calc_out.txt',
           'made_at': str(D.date.today()), 'by': 'research/k200etf1126/mkimg.py', 'out': 'img/00.png', 'topic': '코스피200 ETF 4종',
           'num': f'{won(min(vals)).replace(chr(10)," ")}~{won(max(vals)).replace(chr(10)," ")} · 차이 {gap:,}만원',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 3 healthy_life_365·1 doorway2 비교 표지(상품 이름 4개+숫자) + ndxetf1122 막대 위 큰 숫자(잘된 글 1위)'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 해마다 네 곳 차이(막대) + 그해 수익(위 글자)
Y = calc.yearly(); yrs = sorted(Y)
sp = [(max(r for _, r in Y[y]) - min(r for _, r in Y[y])) * 100 for y in yrs]
mid = [sorted(r for _, r in Y[y])[1] * 100 for y in yrs]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); x = np.arange(len(yrs))
mx = int(np.argmax(sp))
ax.bar(x, sp, 0.62, color=[ORG if i == mx else '#94A3B8' for i in range(len(yrs))])
for i in range(len(yrs)):
    ax.text(x[i], sp[i] + 0.03, f'{sp[i]:.2f}', ha='center', fontproperties=Bs(11.5), color=INK)
    ax.text(x[i], 1.32, ('0%' if abs(mid[i])<0.5 else f'{mid[i]:+.0f}%'), ha='center', fontsize=11, color=SUBC)
ax.text(-0.6, 1.42, '그해 수익', fontsize=11, color=SUBC)
ax.set_xticks(x); ax.set_xticklabels([f"'{str(y)[2:]}" for y in yrs], fontproperties=Bs(13)); ax.tick_params(axis='x', length=0, pad=6)
ax.set_yticks([]); ax.set_ylim(0, 1.55)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
last = Y[yrs[-1]]
frame(fig, f'해마다 네 곳 수익 차이(%포인트) — 가장 벌어진 해도 {max(sp):.2f}', f"분배금 받은 날 다시 삼 · 세금 떼기 전 · '{str(yrs[-1])[2:]}년은 {E.month}/{E.day}까지 · 위 회색 글자는 그해 수익(네 곳 가운데 값 근처)")
fig.subplots_adjust(top=0.83, bottom=0.12, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 최근 1년 분배금(1주)·총보수
FEE = {'KODEX': 0.15, 'TIGER': 0.05, 'RISE': 0.017, 'ACE': 0.017}
dv = {}
for t, (px, d_) in calc.data.items():
    last = max(px); dv[calc.N[t].split()[0]] = (sum(v for d, v in d_.items() if d > last - D.timedelta(days=365)), px[last])
order = sorted(dv, key=lambda n: -dv[n][0])
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); y = np.arange(4)[::-1]
ax.barh(y, [dv[n][0] for n in order], color=[ORG if i == 0 else '#94A3B8' for i in range(4)], height=0.55)
for yy, n in zip(y, order):
    ax.text(-30, yy, n, ha='right', va='center', fontproperties=Bs(18), color=INK)
    ax.text(dv[n][0] + 30, yy + 0.08, f'1년 분배금 {dv[n][0]:,.0f}원', va='center', fontproperties=Bs(16), color=INK)
    ax.text(dv[n][0] + 30, yy - 0.25, f'총보수 연 {FEE[n]}%', va='center', fontsize=13, color=SUBC)
ax.set_xlim(-300, 2400); ax.set_ylim(-0.7, 3.6); ax.axis('off')
frame(fig, '최근 1년 분배금(1주)과 지금 총보수', f'{ES} 종가 기준 1주 가격은 네 곳 모두 7만 3천~7만 4천원대 · 분배금은 최근 4번 합')
fig.subplots_adjust(top=0.83, bottom=0.08, left=0.02, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'k200etf1126' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok', gap, [f'{v:.4f}' for v in vals], f'{max(sp):.2f}', dv)
