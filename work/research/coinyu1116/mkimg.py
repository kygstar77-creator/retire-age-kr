# coinyu1116 본문 그림 — 01 비트코인 해마다 오르내림(업비트 연말 종가), 02 이월공제 있을 때 세금. 표지 00은 cafecover.py. 숫자는 calc_out.txt 그대로
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, INK, SUBC, ORG, GRY = '#1D4ED8', '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = '업비트 원화 시장 비트코인 연말 종가(11/16 받음) · 파이어맵 계산'
ys = ['2018','2019','2020','2021','2022','2023','2024','2025','2026\n(11/16까지)']
r = [-78.2, 97.9, 285.5, 77.2, -62.9, 170.6, 144.1, -8.0, -30.9]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
cols = [ORG if v < 0 else BLUE for v in r]; cols[-1] = GRY
ax.bar(range(len(ys)), r, color=cols, width=0.62)
for i, v in enumerate(r):
    ax.text(i, v + (8 if v >= 0 else -22), f'{v:+.0f}%', ha='center', fontproperties=Bs(13), color=INK)
ax.axhline(0, color=INK, lw=1)
ax.set_xticks(range(len(ys))); ax.set_xticklabels(ys, fontsize=11.5)
ax.set_yticks([]); ax.set_ylim(-110, 320)
for s in ('top', 'right', 'left', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.93, '비트코인, 해마다 얼마나 오르내렸나', fontproperties=Bs(23), color=INK)
fig.text(0.04, 0.88, '2018~2025년 8해 중 손해 본 해는 세 번(주황)', fontsize=13.5, color=SUBC)
fig.text(0.04, 0.025, SRC, fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.84, bottom=0.12, left=0.03, right=0.98)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02
lab = ['2022년 손해 629만원\n→ 2023년 이익 1,706만원', '2018년 손해 782만원\n→ 2019년 이익 979만원']
now = [320, 160]; cf = [182, 0]
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
x = [0, 1]; w = 0.34
ax.bar([i - w/2 for i in x], now, w, color=GRY, label='지금 법')
ax.bar([i + w/2 for i in x], cf, w, color=BLUE, label='이월공제가 있으면')
for i in x:
    ax.text(i - w/2, now[i] + 6, f'{now[i]}만원', ha='center', fontproperties=Bs(16), color=INK)
    ax.text(i + w/2, cf[i] + 6, f'{cf[i]}만원' if cf[i] else '0원', ha='center', fontproperties=Bs(16), color=BLUE)
ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=12.5); ax.set_yticks([]); ax.set_ylim(0, 380)
ax.legend(frameon=False, fontsize=12.5, loc='upper right')
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.93, '이익 본 해 세금, 지난해 손해를 빼 주면', fontproperties=Bs(22), color=INK)
fig.text(0.04, 0.88, '해마다 1천만원어치 사서 연말에 판다고 친 계산(지방소득세 포함 22%)', fontsize=13, color=SUBC)
fig.text(0.04, 0.025, SRC, fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.82, bottom=0.16, left=0.04, right=0.98)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
