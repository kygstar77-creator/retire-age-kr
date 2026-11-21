# divoone1122 그림 — 00 표지(차트: DIVO 최근 12회 분배, 12월만 주황), 01 해마다 12월 vs 다른 달 평균, 02 배당 ETF 9개 '가장 큰 한 번'이 부풀린 폭. 숫자는 calc_out.txt·calc2_out.txt 그대로
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, GRAY, NAVY = '#111827', '#6B7280', '#EA580C', '#9CA3AF', '#1E3A5F'
SRC = '야후 파이낸스 분배 기록(11/21 받음) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 56, 46
# 00 표지 — 최근 12회 분배금
m = ['25.11','25.12','26.1','26.2','26.3','26.4','26.5','26.6','26.7','26.8','26.9','26.10']
v = [0.214,0.953,0.183,0.186,0.179,0.181,0.184,0.183,0.188,0.195,0.189,0.191]
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(NAVY)
fig.text(0.07, 0.86, 'DIVO 분배율', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.77, '6.88% 중 12월 한 번', fontproperties=Bs(38), color='#BFDBFE')
ax = fig.add_axes([0.06, 0.2, 0.88, 0.5]); ax.set_facecolor(NAVY)
ax.bar(range(12), v, color=[ORG if i == 1 else '#94A3B8' for i in range(12)], width=0.62)
ax.text(1, 0.953 + 0.02, '0.95달러', ha='center', va='bottom', fontproperties=Bs(30), color='white')
ax.text(7, 0.26, '다른 달 0.18~0.21달러', ha='center', va='bottom', fontproperties=Bs(24), color='white')
for i in (1, 11): ax.text(i, -0.03, ('2025년 12월' if i == 1 else '2026년 10월'), ha='center', va='top', fontproperties=Bs(19), color='#BFDBFE')
ax.set_ylim(-0.12, 1.12); ax.set_xlim(-0.7, 11.7); ax.axis('off')
fig.text(0.07, 0.11, '그 달을 다른 달처럼 치면 5.14%', fontproperties=Bs(NUM_PX - 14), color='white')
fig.text(0.07, 0.045, '야후 파이낸스 분배 기록 · 파이어맵 계산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API DIVO 분배 기록(events=div) 2025-11~2026-10 12회, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-21', 'by': 'research/divoone1122/mkimg.py', 'out': 'img/00.png', 'topic': 'DIVO 분배율', 'num': '6.88% · 0.95달러 · 5.14%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 5 hyjoyer/224454617770·경쟁 7 lim_and_jin/224436629727 첫 그림 = 큰 글자+숫자 정리 그림 → 막대 차트 위 큰 숫자'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 해마다 12월
Y = [2019,2020,2021,2022,2023,2024,2025]; dec = [1.004,0.149,0.153,0.144,0.146,0.165,0.953]; avg = [0.1365,0.1326,0.1523,0.1422,0.1420,0.1578,0.1738]
import numpy as np
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); fig.subplots_adjust(top=0.82, bottom=0.12, left=0.06, right=0.97)
x = np.arange(7); wd = 0.36
for i in range(7):
    ax.bar(x[i] - wd/2, avg[i], wd, color=GRAY)
    ax.bar(x[i] + wd/2, dec[i], wd, color=ORG if dec[i] > 0.5 else NAVY)
    ax.text(x[i] + wd/2, dec[i] + 0.015, f'{dec[i]:.2f}', ha='center', fontproperties=Bs(14), color=INK)
ax.set_xticks(x); ax.set_xticklabels([f'{y}년' for y in Y], fontproperties=Bs(15)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); [s.set_visible(False) for s in ax.spines.values()]; ax.set_ylim(0, 1.12)
from matplotlib.patches import Patch; ax.legend(handles=[Patch(color=GRAY, label='그해 다른 달 평균'), Patch(color=NAVY, label='12월'), Patch(color=ORG, label='12월(크게 튄 해)')], prop=Bs(13), frameon=False, loc='upper center', ncol=3)
frame(fig, 'DIVO 12월 분배, 크게 튄 해는 7년 중 두 번', '1주당 달러 · 열두 번 다 나눠 준 2019~2025년')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 배당 ETF 9개
N = ['DIVO','JEPQ','XYLD','JEPI','DGRO','SPYD','SCHD','VYM','QYLD']; G = [1.74,0.27,0.16,0.14,0.13,0.09,0.06,0.05,0.04]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); fig.subplots_adjust(top=0.82, bottom=0.08, left=0.14, right=0.95)
y = np.arange(9)[::-1]
ax.barh(y, G, color=[ORG if n == 'DIVO' else GRAY for n in N], height=0.6)
for yi, g in zip(y, G): ax.text(g + 0.03, yi, f'{g:.2f}%p', va='center', fontproperties=Bs(14), color=INK)
ax.set_yticks(y); ax.set_yticklabels(N, fontproperties=Bs(15)); ax.tick_params(axis='y', length=0)
ax.set_xticks([]); [s.set_visible(False) for s in ax.spines.values()]; ax.set_xlim(0, 2.1)
frame(fig, '가장 큰 한 번이 분배율을 얼마나 올렸나', '그 한 번을 다른 회차 평균으로 바꾸면 내려가는 폭 · 11월 20일 종가')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
