# newrenew1112 본문 그림 — 01 갱신 보증금 구간별 차이 02 7곳 새 계약 vs 갱신 (표지 00은 cafecover.py, 43% 그림은 안 씀)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, LBLUE, INK, GR, SUBC, ORG = '#1D4ED8', '#93C5FD', '#111827', '#CBD5E1', '#6B7280', '#EA580C'
SRC = '국토교통부 아파트 전월세 실거래 · 서울 25개 구 2026년 8~10월 계약 순수 전세(11/13 다시 받음) · 파이어맵 계산'
# 00 표지 — 갱신 보증금 구간별 새 계약이 비싼 비율(가운데 값)
fig, ax = plt.subplots(figsize=(9, 6.2), dpi=100)
lab = ['갱신 3억 미만\n(83곳)', '3억~6억\n(213곳)', '6억 이상\n(321곳)']; v = [25.9, 15.0, 8.0]
ax.bar(range(3), v, color=[ORG, BLUE, LBLUE], width=0.6)
for i, x in enumerate(v): ax.text(i, x + 0.8, f'+{int(x+0.5)}%', ha='center', fontproperties=Bs(26), color=INK)
ax.set_xticks(range(3)); ax.set_xticklabels(lab, fontproperties=Bs(16)); ax.set_yticks([]); ax.set_ylim(0, 33)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.9, '전세 새 계약, 갱신보다 얼마나 비쌀까', fontproperties=Bs(26), color=INK)
fig.text(0.05, 0.83, '서울 아파트 617곳 중 88%는 새 계약이 더 비쌌어요(중간값 +12%)', fontsize=15.5, color=SUBC)
fig.text(0.05, 0.03, SRC, fontsize=10, color=SUBC)
fig.subplots_adjust(top=0.76, bottom=0.17, left=0.06, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 01 7곳 — 새 계약 vs 갱신 가운데 값(억원), 2025.11~2026.10
rows = [('목동신시가지 11단지 65㎡대', 5.00, 4.20), ('장미2차 81~83㎡', 7.50, 6.50), ('목동신시가지 3단지 64~66㎡', 6.50, 5.75),
        ('파크리오 84㎡대', 11.05, 10.50), ('목동신시가지 7단지 66~68㎡', 7.00, 6.51), ('압구정 한양1차 49~51㎡', 5.35, 5.20), ('압구정 신현대12차 107~113㎡', 8.50, 8.40)]
fig, ax = plt.subplots(figsize=(9, 7.2), dpi=100)
ys = list(range(len(rows)))[::-1]
for y, (n, a, b) in zip(ys, rows):
    ax.barh(y + 0.18, a, height=0.34, color=BLUE); ax.barh(y - 0.18, b, height=0.34, color=GR)
    ax.text(a + 0.15, y + 0.18, f'새 계약 {a:.2f}억', va='center', fontsize=12.5, color=INK)
    ax.text(b + 0.15, y - 0.18, f'갱신 {b:.2f}억  (차이 {"1억원" if round((a-b)*10000)==10000 else format(round((a-b)*10000),",")+"만원"})', va='center', fontsize=12.5, color=SUBC)
ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows], fontproperties=Bs(13)); ax.set_xticks([]); ax.set_xlim(0, 17)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.93, '쇼츠에 나온 7곳 — 같은 집 새 전세 vs 갱신', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.885, '순수 전세 보증금 가운데 값 · 2025년 11월~2026년 10월 계약', fontsize=14, color=SUBC)
fig.text(0.04, 0.025, '국토교통부 아파트 전월세 실거래(강남·송파·양천, 11/13 다시 받음) · 파이어맵 계산', fontsize=10, color=SUBC)
fig.subplots_adjust(top=0.85, bottom=0.07, left=0.33, right=0.98)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
# 02 갱신 5% 넘게 올린 비율
fig, ax = plt.subplots(figsize=(9, 6.2), dpi=100)
grp = [('갱신요구권 쓴 갱신\n(6,690건)', 0), ('요구권 표시 없는 갱신\n(합의 갱신 등, 5,954건)', 43)]
for y, (lb, p) in zip((1, 0), grp):
    ax.barh(y, 100, color=GR, height=0.5); ax.barh(y, p, color=ORG, height=0.5)
    ax.text(102, y, f'{p}%', va='center', fontproperties=Bs(26), color=INK)
ax.set_yticks([1, 0]); ax.set_yticklabels([g[0] for g in grp], fontproperties=Bs(15)); ax.set_xlim(0, 118); ax.set_xticks([])
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.9, '전세 갱신, 보증금을 5% 넘게 올린 비율', fontproperties=Bs(22), color=INK)
fig.text(0.04, 0.83, '요구권을 쓰면 5%까지(주택임대차보호법 제7조) · 표시 없는 합의 갱신은 한도 없음', fontsize=14.5, color=SUBC)
fig.text(0.04, 0.03, SRC + ' · 이전도 전세였던 갱신', fontsize=9.5, color=SUBC)
fig.subplots_adjust(top=0.76, bottom=0.12, left=0.28, right=0.95)
fig.savefig('43pct_unused.png', dpi=100); plt.close(fig)
