# wytd1124 그림 — 00 표지(현지 통화 vs 원화 올해 수익률 5개 지수), 01 원화 대비 달러·엔·유로 변화, 02 코스피 올해 흐름. 숫자는 calc_out.txt 그대로
import os, json, datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, BLUE, RED, GRY = '#111827', '#6B7280', '#1D4ED8', '#DC2626', '#94A3B8'
SRC = '야후 파이낸스 지수 종가 · 한국은행 매매기준율 · 파이어맵 계산'
TOPIC_PX, NUM_PX = 50, 0
BG = '#EEF6EE'
names = ['코스피', '닛케이225', 'S&P500', '나스닥100', '유로스톡스50']
loc = [11.7, 12.1, 5.7, 5.9, 4.8]; krw = [11.7, 3.0, -1.5, -1.3, -8.8]
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.87, '올해 지수 성적, 원화로', fontproperties=Bs(TOPIC_PX), color=INK)
fig.text(0.06, 0.80, '현지 돈 수익률(회색)과 원화 수익률(색) · 11월 23일 종가', fontproperties=Bs(21), color='#166534')
ax = fig.add_axes([0.30, 0.10, 0.66, 0.64]); ax.set_facecolor(BG)
y = list(range(len(names)))[::-1]
for yy, a, b, n in zip(y, loc, krw, names):
    ax.barh(yy + 0.2, a, height=0.36, color=GRY)
    ax.barh(yy - 0.2, b, height=0.36, color=BLUE if b >= 0 else RED)
    ax.text(a + (0.4 if a >= 0 else -0.4), yy + 0.2, f'{a:+.1f}%', va='center', ha='left' if a >= 0 else 'right', fontproperties=Bs(16), color=SUBC)
    ax.text(b + (0.4 if b >= 0 else -0.4), yy - 0.2, f'{b:+.1f}%', va='center', ha='left' if b >= 0 else 'right', fontproperties=Bs(22), color=INK)
ax.set_yticks(y); ax.set_yticklabels(names, fontproperties=Bs(22)); ax.axvline(0, color=INK, lw=1)
ax.set_xlim(-21, 21); ax.set_xticks([]); [s.set_visible(False) for s in ax.spines.values()]
fig.text(0.06, 0.035, '2025년 마지막 거래일 → 2026년 11월 23일(닛케이 20일) · 배당 빼고 가격만', fontsize=16, color='#166534')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 ^KS11·^N225·^GSPC·^NDX·^STOXX50E 종가, 한국은행 ECOS 731Y001 매매기준율, calc_out.txt',
           'made_at': '2026-11-24', 'by': 'research/wytd1124/mkimg.py', 'out': 'img/00.png', 'topic': '올해 지수 성적, 원화로', 'num': '+11.7%·-1.5%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 winnerking/224475984112 표·경쟁 5 joyuldrama/224469529724 칠판 표 — 가정 환율 대신 실제 다섯 지수'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 원화 대비 통화 변화
lab = ['1달러', '100엔', '1유로']; a = ['1,434.9원', '917.63원', '1,685.72원']; b = ['1,337.3원', '842.95원', '1,467.69원']; ch = [-6.8, -8.1, -12.9]
fig = plt.figure(figsize=(9, 6.5), dpi=100); fig.patch.set_facecolor('white')
frame(fig, '올해 달러·엔·유로 값이 얼마나 내렸나', '한국은행 매매기준율 · 2025년 12월 31일 → 2026년 11월 23일')
ax = fig.add_axes([0.16, 0.1, 0.78, 0.7])
yy = [2, 1, 0]
ax.barh(yy, ch, color=RED, height=0.55)
for i in range(3):
    ax.text(ch[i] - 0.3, yy[i], f'{ch[i]:.1f}%', va='center', ha='right', fontproperties=Bs(20), color=INK)
    ax.text(0.3, yy[i], f'{a[i]} → {b[i]}', va='center', ha='left', fontproperties=Bs(15), color=SUBC)
ax.set_yticks(yy); ax.set_yticklabels(lab, fontproperties=Bs(18)); ax.axvline(0, color=INK, lw=1)
ax.set_xlim(-24, 12); ax.set_xticks([]); [s.set_visible(False) for s in ax.spines.values()]
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 코스피 올해 흐름
d = json.load(open('raw/KS11.json', encoding='utf-8'))['chart']['result'][0]; tz = d['meta']['gmtoffset']
s = [((datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=t + tz)).date(), v) for t, v in zip(d['timestamp'], d['indicators']['quote'][0]['close']) if v]
s = [x for x in s if datetime.date(2025, 12, 30) <= x[0] <= datetime.date(2026, 11, 23)]
fig = plt.figure(figsize=(9, 6.5), dpi=100); fig.patch.set_facecolor('white')
frame(fig, '코스피 올해 흐름', '2025년 12월 30일 종가 → 2026년 11월 23일 종가 · 단위 포인트')
ax = fig.add_axes([0.1, 0.1, 0.84, 0.7])
ax.plot([x[0] for x in s], [x[1] for x in s], color=BLUE, lw=2.2)
pk = max(s, key=lambda x: x[1])
for (dt, v), t, va in [(s[0], '      연말 4,214', 'top'), (pk, '6월 22일 최고 9,115', 'bottom'), (s[-1], '11월 23일 4,709', 'top')]:
    ax.scatter([dt], [v], color=RED, zorder=3); ax.annotate(t, (dt, v), xytext=(0, 10 if va == 'bottom' else -14), textcoords='offset points', ha='left' if t.startswith(' ') else 'center', va=va, fontproperties=Bs(15), color=INK)
ax.set_ylim(3000, 10200); [ax.spines[k].set_visible(False) for k in ('top', 'right')]
import matplotlib.dates as md; ax.xaxis.set_major_formatter(md.DateFormatter('%-m월' if os.name != 'nt' else '%m월'))
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
# 100px·보드용 축소본
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
print('ok', pk)
