# dow1124 그림 — 00 표지(골드만삭스·엔비디아 다우 비중 vs S&P500 비중), 01 5% 오르면 다우 몇 포인트, 02 다우 비중 vs S&P500 비중. 숫자는 calc_out.txt 그대로
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, NAVY, GRY = '#111827', '#6B7280', '#EA580C', '#1E3A5F', '#94A3B8'
SRC = 'State Street DIA·SPY 보유 종목(2026-11-19) · 야후 파이낸스 종가 · 파이어맵 계산'
TOPIC_PX, NUM_PX = 54, 40
BG = '#FFF1DC'
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '다우지수 비중', fontproperties=Bs(TOPIC_PX), color=INK)
fig.text(0.07, 0.785, '1주 값이 비싼 회사가 더 크게 담겨요', fontproperties=Bs(25), color='#9A3412')
ax = fig.add_axes([0.07, 0.15, 0.86, 0.57]); ax.set_facecolor(BG)
names = ['골드만삭스\n1주 848달러', '엔비디아\n1주 146달러']; dow = [10.3, 1.8]; spx = [0.4, 5.7]
for i in range(2):
    ax.bar(i*1.0-0.2, dow[i], width=0.36, color=ORG); ax.bar(i*1.0+0.2, spx[i], width=0.36, color='#64748B')
    ax.text(i-0.2, dow[i]+0.3, f'{dow[i]}%', ha='center', va='bottom', fontproperties=Bs(NUM_PX), color=INK)
    ax.text(i+0.2, spx[i]+0.3, f'{spx[i]}%', ha='center', va='bottom', fontproperties=Bs(30), color=INK)
    ax.text(i, -0.5, names[i], ha='center', va='top', fontproperties=Bs(21), color=INK)
ax.text(0.95, 12.6, '■ 다우지수', color=ORG, ha='right', fontproperties=Bs(20)); ax.text(1.5, 12.6, '■ S&P500', color='#64748B', ha='right', fontproperties=Bs(20))
ax.set_ylim(-3.2, 13.5); ax.set_xlim(-0.6, 1.6); ax.axis('off')
fig.text(0.07, 0.045, '2026년 11월 19일 · DIA·SPY 보유 종목 비중', fontsize=17, color='#9A3412')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': 'State Street DIA·SPY 보유 종목 파일(As of 19-Nov-2026) 비중, calc_out.txt',
           'made_at': '2026-11-22', 'by': 'research/dow1124/mkimg.py', 'out': 'img/00.png', 'topic': '다우지수 비중', 'num': '10.3%·1.8%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 joaijoa1/224473009068·경쟁 6 dlfdjdl/224474884006 계산 방식 설명 그림(표·숫자) — 가정 숫자 대신 실제 비중'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 5% 오르면
lab = ['골드만삭스', '캐터필러', '마이크로소프트', '암젠', '비자', '애플', '엔비디아', '나이키']; pt = [252, 160, 148, 130, 120, 104, 43, 10]
fig = plt.figure(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
frame(fig, '주가가 5% 오르면 다우지수는 몇 포인트?', '11월 19일 종가 기준 · 1달러 움직이면 지수 약 5.94포인트')
ax = fig.add_axes([0.24, 0.1, 0.68, 0.74])
c = [ORG if v >= 150 else (NAVY if v > 50 else GRY) for v in pt]
ax.barh(range(len(pt))[::-1], pt, color=c, height=0.62)
for i, v in enumerate(pt):
    ax.text(v + 4, len(pt)-1-i, f'{v}포인트', va='center', fontproperties=Bs(15), color=INK)
ax.set_yticks(range(len(pt))[::-1]); ax.set_yticklabels(lab, fontproperties=Bs(15))
ax.set_xlim(0, 300); ax.set_xticks([]); [s.set_visible(False) for s in ax.spines.values()]
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 다우 비중 vs S&P500 비중
lab = ['골드만삭스', '캐터필러', '마이크로소프트', '애플', '아마존', '엔비디아']; dw = [10.3, 6.5, 6.0, 4.2, 3.1, 1.8]; sp = [0.4, 0.4, 6.0, 8.2, 4.1, 5.7]
fig = plt.figure(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
frame(fig, '같은 회사, 다우와 S&P500 비중', '2026년 11월 19일 DIA·SPY 보유 종목 · 단위 %')
ax = fig.add_axes([0.24, 0.1, 0.68, 0.72])
y = list(range(len(lab)))[::-1]
ax.barh([v+0.18 for v in y], dw, height=0.34, color=ORG, label='다우지수')
ax.barh([v-0.18 for v in y], sp, height=0.34, color=GRY, label='S&P500')
for yy, a, b in zip(y, dw, sp):
    ax.text(a+0.15, yy+0.18, f'{a}%', va='center', fontproperties=Bs(13), color=INK)
    ax.text(b+0.15, yy-0.18, f'{b}%', va='center', fontproperties=Bs(13), color=SUBC)
ax.set_yticks(y); ax.set_yticklabels(lab, fontproperties=Bs(15)); ax.set_xlim(0, 12.5); ax.set_xticks([])
[s.set_visible(False) for s in ax.spines.values()]; ax.legend(prop=Bs(13), frameon=False, loc='lower right')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
