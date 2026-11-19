# tigersp1121 그림 — 00 표지(차트: 3,000만원 → 매달 vs 한 번에), 01 5년 동안 가치 흐름(series.json), 02 2022-06-17 손해 비교. 숫자는 calc_out.txt
import os, json, glob, datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
from PIL import Image
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, INK, SUBC, ORG, GRY = '#1D4ED8', '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = "미래에셋자산운용 상품 정보·분배금 · 야후 파이낸스 360750.KS 종가 · 파이어맵 계산"
BG = '#0F3D3E'
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, 'TIGER 미국S&P500', fontproperties=Bs(46), color='white')
fig.text(0.07, 0.77, '3,000만원 넣고 5년 뒤', fontproperties=Bs(38), color='#99F6E4')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.52]); ax.set_facecolor(BG)
vals = [3000, 4353, 5571]; cols = [GRY, '#5EEAD4', '#FB923C']
ax.bar([0, 1, 2], vals, color=cols, width=0.62)
for x, t, v in zip([0, 1, 2], ['3,000만원', '4,353만원', '5,571만원'], vals): ax.text(x, v + 80, t, ha='center', va='bottom', fontproperties=Bs(34), color='white')
for x, t in zip([0, 1, 2], ['넣은 돈', '매달\n50만원씩', '첫 달에\n한 번에']): ax.text(x, 2300, t, ha='center', va='top', fontproperties=Bs(24), color='white')
ax.set_ylim(2300 - 1000, 6300); ax.set_xlim(-0.6, 2.6); ax.axis('off')
fig.text(0.07, 0.1, '2021.12 시작 → 2026.11.19 종가 · 분배금 포함 세전', fontproperties=Bs(22), color='white')
fig.text(0.07, 0.045, '미래에셋자산운용·야후 파이낸스 · 파이어맵 계산', fontsize=17, color='#99F6E4')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '미래에셋자산운용 TIGER 미국S&P500 상품 정보·연도별 분배금 + 야후 파이낸스 360750.KS 일별 종가·분배 기록, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-20', 'by': 'research/tigersp1121/mkimg.py', 'out': 'img/00.png', 'topic': 'TIGER 미국S'topic': 'TIGER 미국S&P500 3,000만원, 5년 뒤'P500 3,000만원 넣고 5년 뒤', 'num': '4,353만 · 5,571만',
           'topic_px': 46, 'num_px': 34, 'follows': '경쟁 2 ckskck123/224482194081 전략별 결과 막대·4 winnerking/224470663135 60개월 표 — 숫자 막대, 우리는 넣은 돈·매달·한 번에 셋'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
S = json.load(open('series.json'))
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
for key, col, name in (('500000', '#0D9488', '매달 50만원씩 (분배금 포함)'), ('30000000', ORG, '첫 달에 3,000만원 (분배금 포함)')):
    d = [datetime.datetime.strptime(r[0], '%Y%m%d') for r in S[key]]
    ax.plot(d, [r[2] / 1e4 for r in S[key]], color=col, lw=2.4, label=name)
d = [datetime.datetime.strptime(r[0], '%Y%m%d') for r in S['500000']]
ax.plot(d, [r[1] / 1e4 for r in S['500000']], color=GRY, lw=2, ls='--', label='매달 넣은 돈 누적')
ax.text(d[-1] + datetime.timedelta(days=12), 4353, '4,353만', fontproperties=Bs(15), color='#0D9488', ha='left', va='center')
ax.text(d[-1] + datetime.timedelta(days=12), 5571, '5,571만', fontproperties=Bs(15), color=ORG, ha='left', va='center')
ax.set_xlim(d[0] - datetime.timedelta(days=30), d[-1] + datetime.timedelta(days=200))
ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
for t in ax.get_xticklabels(): t.set_fontproperties(Bs(13))
ax.set_ylabel('만원', fontsize=12, color=SUBC); ax.tick_params(axis='y', labelsize=11, colors=SUBC)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.legend(prop=fm.FontProperties(fname=F + r'\pd500.ttf', size=12), frameon=False, loc='upper left')
frame(fig, '5년 동안 내 돈은 이렇게 움직였어요(만원)', '2021.12.1~2026.11.19 매일 종가 · 분배금은 받은 돈으로 더함 · 세전')
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.1, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
names = ['매달 50만원씩\n(넣은 돈 350만원)', '첫 달에 한 번에\n(넣은 돈 3,000만원)']; v = [40, 363]
ax.bar([0, 1], v, color=['#0D9488', ORG], width=0.5)
for i, x in enumerate(v): ax.text(i, x + 8, f'약 {x}만원 손해', ha='center', va='bottom', fontproperties=Bs(20), color=INK)
ax.set_xticks([0, 1]); ax.set_xticklabels(names, fontproperties=Bs(15)); ax.tick_params(axis='x', length=0, pad=6)
ax.set_yticks([]); ax.set_ylim(0, 430)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
frame(fig, '가장 많이 빠졌던 날, 손해는 얼마였나', '2022년 6월 17일 종가 11,960원 · 5년 중 가장 낮은 날 · 분배금 포함 세전')
fig.subplots_adjust(top=0.82, bottom=0.16, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'tigersp1121' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
