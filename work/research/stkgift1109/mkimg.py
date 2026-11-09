# stkgift1109 그림 2장 — 01 7/28 삼성전자 종가 vs 넉 달 평균(네이버 금융 일별 종가, 상증법 제63조), 02 11/6 증여 일정표(상증법 제63조·제68조·제4조④, 국세기본법 제5조)
import os, json, datetime as dt
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLU, INK, SUB, GR, LG, RED = '#1D4ED8', '#111827', '#4B5563', '#94A3B8', '#E5E7EB', '#C2410C'
rows = [(dt.date.fromisoformat(a), c) for a, c in json.load(open('raw/px_005930.KS.json', encoding='utf-8'))['rows']]
a, g, b = dt.date(2026, 5, 28), dt.date(2026, 7, 28), dt.date(2026, 9, 28)
w = [(d, c) for d, c in rows if a <= d <= b]
avg = sum(c for _, c in w) / len(w); close = dict(rows)[g]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); fig.patch.set_facecolor('white')
ax.plot([d for d, _ in w], [c/10000 for _, c in w], color=GR, lw=2)
ax.axhline(avg/10000, color=BLU, lw=2.5, ls='--')
ax.scatter([g], [close/10000], s=110, color=RED, zorder=5)
ax.annotate('증여한 날 종가\n22만원', (g, close/10000), xytext=(-150, -38), textcoords='offset points', fontproperties=Bs(16), color=RED)
ax.text(w[0][0], avg/10000 + 0.6, f'신고할 값 = 넉 달 평균 약 28만 1천원', fontproperties=Bs(16), color=BLU)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%-m월' if os.name != 'nt' else '%#m월'))
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.set_ylabel('만원', fontsize=12, color=SUB)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.93, '7월 28일 삼성전자를 증여했다면', fontproperties=Bs(23), color=INK)
fig.text(0.05, 0.875, '5천만원어치(227주) → 신고할 값 약 6,377만원 · 성인 자녀 세금 약 134만원', fontsize=13.5, color=SUB)
fig.text(0.05, 0.02, '한국거래소 종가(5/28~9/28, 네이버 금융) · 상속세 및 증여세법 제63조·제53조·제26조·제69조로 계산', fontsize=10.5, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.1, left=0.1, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

fig = plt.figure(figsize=(9, 6.6), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.9, '11월 6일에 주식을 넘겼다면', fontproperties=Bs(23), color=INK)
fig.text(0.05, 0.845, '값이 정해지는 날과 돌려받을 수 있는 마지막 날', fontsize=14, color=SUB)
def box(x, y, wd, h, t, c, tc=INK, fs=15):
    fig.patches.append(FancyBboxPatch((x, y), wd, h, boxstyle='round,pad=0.008,rounding_size=0.02', transform=fig.transFigure, fc=c, ec='none'))
    fig.text(x + wd/2, y + h/2, t, ha='center', va='center', fontproperties=Bs(fs), color=tc, linespacing=1.45)
steps = [('9월 6일', '평가 기간 시작\n(이미 지난 두 달)', LG, INK), ('11월 6일', '증여한 날', '#FED7AA', INK),
         ('1월 6일', '평가 기간 끝\n신고할 값이 정해짐', '#DBEAFE', INK), ('2월 28일', '신고기한\n(일요일이라 뒤 첫 평일)', BLU, 'white')]
for i, (d, t, c, tc) in enumerate(steps):
    x = 0.05 + i * 0.235
    fig.text(x + 0.1, 0.72, d, ha='center', fontproperties=Bs(19), color=BLU if i else SUB)
    box(x, 0.45, 0.2, 0.22, t, c, tc, 14)
    if i < 3: fig.text(x + 0.217, 0.56, '▶', ha='center', va='center', fontsize=13, color=GR)
box(0.05, 0.13, 0.9, 0.22, '1월 6일에 평균을 보고, 너무 높게 잡혔으면\n신고기한 안에 주식을 그대로 돌려받으면 처음부터 증여가 없던 것으로 봄 (현금은 안 됨)', '#F1F5F9', INK, 14.5)
fig.text(0.05, 0.03, '상속세 및 증여세법 제63조·제68조·제4조④, 국세기본법 제5조', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok', round(avg), close, len(w))
