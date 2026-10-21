# g1asymcafe1022 그림 3장 — 숫자는 calc.py(KRX 금시장 금 1kg 일별 종가, 네이버 증권 M04020000, 2026-10-22 받음)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
PEAK, NOW = 269_810, 175_250
# 00 표지 — 짙은 갈색 바탕, 큰 글 두 줄 + 1월 고점 1천만원의 달마다 값(월말 종가)
BG, WH, LG, GOLD = '#2B2118', '#FFFFFF', '#E7D8C3', '#F59E0B'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.875, '1월 고점에 산 금 1천만원', fontsize=62, fontproperties=B, color=WH)
fig.text(0.06, 0.765, '본전까지 54% 올라야', fontsize=66, fontproperties=B, color=GOLD)
fig.text(0.06, 0.715, '10월 21일 KRX 금시장 종가로 650만원쯤', fontsize=23, color=LG)
ax = fig.add_axes([0.08, 0.13, 0.86, 0.52]); ax.set_facecolor(BG)
rows = [('1/29 고점', 1000), ('3월', 834), ('5월', 802), ('7월', 695), ('9월', 678), ('10/21', 650)]
for i, (n, v) in enumerate(rows):
    ax.bar(i, v, width=0.62, color=GOLD if i in (0, len(rows) - 1) else '#8C6A3F')
    ax.text(i, v + 25, f'{v}', ha='center', fontproperties=Bs(30), color=WH)
    ax.text(i, -70, n, ha='center', fontproperties=Bs(24), color=LG)
ax.set_ylim(-110, 1150); ax.set_xlim(-0.6, len(rows) - 0.4); ax.axis('off')
fig.text(0.06, 0.03, '단위 만원 · 1/29 고점에 산 날, 나머지는 그달 마지막 거래일 종가 · 수수료 뺌', fontsize=19, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 떨어진 폭 → 본전까지 올라야 할 폭
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)
ds = [10, 20, 30, 35, 50]; us = [round((1 / (1 - d / 100) - 1) * 100) for d in ds]
for i, (d, u) in enumerate(zip(ds, us)):
    y = len(ds) - 1 - i
    ax.barh(y + 0.18, d, height=0.34, color=GR); ax.barh(y - 0.18, u, height=0.34, color=ORG)
    ax.text(d + 1.5, y + 0.18, f'{d}% 떨어지면', va='center', fontproperties=Bs(15), color=SUB)
    ax.text(u + 1.5, y - 0.18, f'{u}% 올라야 본전', va='center', fontproperties=Bs(17), color=ORG)
ax.set_xlim(0, 135); ax.axis('off')
fig.text(0.05, 0.93, '떨어진 만큼 올라서는 본전이 안 돼요', fontsize=26, fontproperties=B, color=INK)
fig.text(0.05, 0.88, '떨어질 땐 처음 돈에서, 오를 땐 줄어든 돈에서 세니까요', fontsize=17, color=SUB)
fig.text(0.05, 0.02, '파이어맵 계산 · 수수료·세금 뺌 · 35%는 1월 고점에 산 금(10월 21일 기준)', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.08)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 쇼츠 기준일(10/6)과 지금(10/21)
fig = plt.figure(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('#FFFFFF')
fig.text(0.05, 0.92, '2주 사이 본전이 더 멀어졌어요', fontsize=26, fontproperties=B, color=INK)
fig.text(0.05, 0.86, '1월 29일 금 1천만원어치를 산 경우', fontsize=17, color=SUB)
for i, (d, g, v, u) in enumerate([('10월 6일', '1g 17만 9천원', '663만원', '51%'), ('10월 21일', '1g 17만 5천원', '650만원', '54%')]):
    x = 0.07 + i * 0.47
    fig.text(x, 0.72, d, fontsize=24, fontproperties=B, color=INK)
    fig.text(x, 0.66, g, fontsize=17, color=SUB)
    fig.text(x, 0.47, v, fontsize=48, fontproperties=B, color=INK if i == 0 else ORG)
    fig.text(x, 0.40, '그날 값', fontsize=17, color=SUB)
    fig.text(x, 0.20, u, fontsize=48, fontproperties=B, color=INK if i == 0 else ORG)
    fig.text(x, 0.13, '본전까지 올라야 할 폭', fontsize=17, color=SUB)
fig.text(0.05, 0.03, 'KRX 금시장 금 1kg 종가(네이버 증권 일별 시세) · 파이어맵 계산 · 수수료 뺌', fontsize=12, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
