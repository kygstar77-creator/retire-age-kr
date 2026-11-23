# kospi1pair1124 그림 — 00 표지(크게 빠진 15번, 1년 뒤 등락), 01 해마다 하루 5% 넘게 빠진 날, 02 1천만원 한 번에 vs 나눠 넣기 1년 뒤. 숫자는 ../longform/ep/KOSPI-1/cafe.md(calc2·3·4 11/23 다시 셈) 그대로
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, BLUE, RED, GRY = '#111827', '#6B7280', '#1D4ED8', '#DC2626', '#94A3B8'
SRC = '한국은행 ECOS 코스피 일별 종가(원자료 한국거래소) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 50, 0
BG = '#EEF2FB'
days = ['97.10', '98.12', '99.06', '00.01', '01.01', '01.09', '02.06', '02.10', '04.05', '07.08', '08.09', '11.08', '20.03', '24.08', '25.04']
yr1 = [-44.9, 73.7, -1.2, -43.4, 26.4, 38.3, -2.1, 32.9, 16.5, -11.7, 19.1, 11.3, 108.3, 28.7, 167.1]
lump = [551, 1737, 988, 566, 1264, 1383, 979, 1329, 1165, 883, 1191, 1113, 2083, 1287, 2671]
dca = [771, 1294, 888, 774, 1307, 946, 1071, 1209, 1085, 850, 1307, 1042, 1341, 1201, 1767]
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.87, '크게 빠진 뒤 1년', fontproperties=Bs(TOPIC_PX), color=INK)
fig.text(0.06, 0.80, '코스피가 하루 5% 넘게 빠진 첫날 → 1년 뒤 등락 · 15번', fontproperties=Bs(21), color='#1E3A8A')
ax = fig.add_axes([0.08, 0.12, 0.88, 0.62]); ax.set_facecolor(BG)
x = range(len(days))
ax.bar(x, yr1, color=[BLUE if v >= 0 else RED for v in yr1], width=0.7)
for i, v in enumerate(yr1):
    ax.text(i, v + (4 if v >= 0 else -4), f'{v:+.0f}%', ha='center', va='bottom' if v >= 0 else 'top', fontproperties=Bs(13), color=INK)
ax.set_xticks(list(x)); ax.set_xticklabels(days, fontproperties=Bs(12), rotation=60); ax.axhline(0, color=INK, lw=1)
ax.set_ylim(-70, 190); ax.set_yticks([]); [s.set_visible(False) for s in ax.spines.values()]
fig.text(0.06, 0.035, '오른 해(파랑) 10번 · 내린 해(빨강) 5번 · 지수 값만, 배당·보수 뺌', fontsize=16, color='#1E3A8A')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '한국은행 ECOS 802Y001 코스피 일별 종가(원자료 한국거래소), longform/ep/KOSPI-1 calc2·calc3·calc4(11/23 다시 셈)',
           'made_at': '2026-11-23', 'by': 'research/kospi1pair1124/mkimg.py', 'out': 'img/00.png', 'topic': '크게 빠진 뒤 1년', 'num': '15번',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 3 5073step/224486714245 실사+큰 글자·경쟁 4 kusi1004/224487257488 시세판 사진 — 오늘 숫자 대신 지난 15번 막대'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 해마다 하루 5% 넘게 빠진 날
ys = ['1997', '1998', '1999', '2000', '2001', '2002', '2004', '2007', '2008', '2009', '2011', '2020', '2024', '2025', '2026']
n = [9, 9, 4, 11, 4, 2, 2, 1, 8, 1, 2, 2, 1, 1, 24]
fig = plt.figure(figsize=(9, 6.5), dpi=100); fig.patch.set_facecolor('white')
frame(fig, '코스피가 하루 5% 넘게 빠진 날, 해마다', '1995년~2026년 11월 20일 종가 · 0번인 해는 뺌')
ax = fig.add_axes([0.07, 0.14, 0.9, 0.66])
ax.bar(range(len(ys)), n, color=[RED if y == '2026' else GRY for y in ys], width=0.7)
for i, v in enumerate(n): ax.text(i, v + 0.4, str(v), ha='center', va='bottom', fontproperties=Bs(15), color=INK)
ax.set_xticks(range(len(ys))); ax.set_xticklabels(ys, fontproperties=Bs(11), rotation=60)
ax.set_ylim(0, 28); ax.set_yticks([]); [s.set_visible(False) for s in ax.spines.values()]
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 1천만원 한 번에 vs 12번 나눠
fig = plt.figure(figsize=(9, 6.5), dpi=100); fig.patch.set_facecolor('white')
frame(fig, '1천만원, 첫날 한 번에 vs 12번 나눠 넣기', '1년 뒤 평가액(만원) · 나눠 넣기는 첫날부터 한 달쯤마다 12번')
ax = fig.add_axes([0.08, 0.16, 0.88, 0.64])
x = list(range(len(days)))
ax.plot(x, lump, 'o', color=BLUE, ms=9, label='한 번에'); ax.plot(x, dca, 's', color='#F59E0B', ms=8, label='나눠 넣기')
for i in x: ax.plot([i, i], [lump[i], dca[i]], color=GRY, lw=1)
ax.axhline(1000, color=INK, lw=1, ls='--'); ax.text(14.4, 1030, '원금 1,000', ha='right', fontproperties=Bs(12), color=INK)
ax.set_xticks(x); ax.set_xticklabels(days, fontproperties=Bs(11), rotation=60)
ax.set_ylim(400, 2800); [ax.spines[k].set_visible(False) for k in ('top', 'right')]
ax.legend(prop=Bs(13), frameon=False, loc='upper left')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
print('ok')
