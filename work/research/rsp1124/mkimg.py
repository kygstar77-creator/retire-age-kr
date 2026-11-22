# rsp1124 그림 — 00 표지(보유 기간별 동일가중 앞선 비율), 01 해마다 차이(2004~2025), 02 하락장 낙폭·회복. 숫자는 calc_out.txt 그대로
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, NAVY, GRY = '#111827', '#6B7280', '#EA580C', '#1E3A5F', '#94A3B8'
SRC = '야후 파이낸스 일별 수정 종가 RSP·SPY(11/22 받음) · 세전·분배금 재투자·달러 · 파이어맵 계산'
TOPIC_PX, NUM_PX = 54, 40
BG = '#4A1D2E'
# 00 표지
lab = ['1년', '3년', '5년', '10년']; pct = [44, 45, 45, 46]
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, 'S&P500 동일가중', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.785, '아무 날 사서 들고 있었다면, SPY보다 앞선 날', fontproperties=Bs(25), color='#FED7AA')
ax = fig.add_axes([0.07, 0.15, 0.86, 0.57]); ax.set_facecolor(BG)
ax.bar(range(4), pct, color=ORG, width=0.6)
ax.axhline(50, color='white', lw=2, ls='--'); ax.text(-0.55, 51, '반반 50%', color='white', ha='left', fontproperties=Bs(18))
for i, v in enumerate(pct):
    ax.text(i, v - 2, f'{v}%', ha='center', va='top', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -2, lab[i] + ' 보유', ha='center', va='top', fontproperties=Bs(20), color='white')
ax.set_ylim(0, 62); ax.set_xlim(-0.6, 3.6); ax.axis('off')
fig.text(0.07, 0.045, '2003.5~2026.11.20 거래일마다 시작 · 분배금 재투자 · 세전', fontsize=17, color='#FED7AA')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API RSP·SPY 일별 수정 종가(11/22 받음)로 보유 기간별 앞선 비율 직접 계산, calc_out.txt',
           'made_at': '2026-11-22', 'by': 'research/rsp1124/mkimg.py', 'out': 'img/00.png', 'topic': 'S&P500 동일가중', 'num': '44%·45%·45%·46%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 5 read_sijang/224473157319 SPY·VOO vs RSP 비교 표지(표·숫자) + 경쟁 3 neighbormrbear 비교 인포그래픽'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 해마다 차이
yrs = list(range(2004, 2026))
diff = [5.8, 2.6, -0.4, -4.2, -3.3, 18.3, 6.3, -2.6, 1.2, 3.2, 0.6, -3.9, 2.5, -3.2, -3.3, -2.3, -5.7, 0.7, 6.6, -12.5, -12.1, -6.5]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.bar(yrs, diff, 0.7, color=[ORG if d > 0 else GRY for d in diff])
for y, d in zip(yrs, diff):
    if abs(d) >= 6: ax.text(y + (-0.25 if y==2023 else 0.25 if y==2024 else 0), d + (0.6 if d > 0 else -0.6), f'{d:+.1f}', ha='center', va='bottom' if d > 0 else 'top', fontproperties=Bs(12), color=INK)
ax.axhline(0, color=INK, lw=1)
ax.text(2011.3, 17.5, '주황 = 동일가중이 앞선 해 10번', fontproperties=Bs(15), color=ORG)
ax.text(2011.3, 15.3, '회색 = SPY가 앞선 해 12번', fontproperties=Bs(15), color=SUBC)
ax.set_xticks([2004, 2008, 2012, 2016, 2020, 2025]); ax.tick_params(axis='x', length=0, labelsize=12)
ax.set_yticks([]); ax.set_ylim(-15.5, 21)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
frame(fig, '해마다 동일가중 수익률 − SPY 수익률(%p)', '2004~2025년 달력 해 22번 · 분배금 재투자·세전·달러')
fig.subplots_adjust(top=0.83, bottom=0.1, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 하락장 낙폭과 회복
ev = ['2008 금융위기', '2020 코로나', '2022 금리 인상']
dR = [59.9, 39.0, 21.4]; dS = [55.2, 33.7, 24.5]; mR = [43, 9, 25]; mS = [58, 6, 23]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); x = np.arange(3); wd = 0.34
ax.bar(x - wd/2, [-v for v in dR], wd, color=ORG); ax.bar(x + wd/2, [-v for v in dS], wd, color=NAVY)
for i in range(3):
    ax.text(x[i] - wd/2, -dR[i] - 1.5, f'-{dR[i]}%\n회복 {mR[i]}달', ha='center', va='top', fontproperties=Bs(13), color=ORG)
    ax.text(x[i] + wd/2, -dS[i] - 1.5, f'-{dS[i]}%\n회복 {mS[i]}달', ha='center', va='top', fontproperties=Bs(13), color=NAVY)
    ax.text(x[i], 2, ev[i], ha='center', va='bottom', fontproperties=Bs(15), color=INK)
ax.text(1.55, -52, '주황 동일가중(RSP)', fontproperties=Bs(15), color=ORG)
ax.text(1.55, -57, '남색 시가총액 가중(SPY)', fontproperties=Bs(15), color=NAVY)
ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(-78, 8); ax.set_xlim(-0.6, 2.6)
for s_ in ('top', 'right', 'left', 'bottom'): ax.spines[s_].set_visible(False)
frame(fig, '하락장 고점 대비 최대 하락과 전 고점 회복까지 걸린 달', '분배금 재투자 값 기준 · 고점·바닥 날짜는 두 상품이 조금 다름')
fig.subplots_adjust(top=0.83, bottom=0.06, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
import sys; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import cafecover
Image.open('pkg/img/00.png').resize((100, 100)).save('pkg/cover_100.png')
cafecover.board('pkg/img/00.png', cafecover.recent_covers(10, exclude='pkg'), 'pkg/cover_board.png', '새: rsp1124')
print('ok')
