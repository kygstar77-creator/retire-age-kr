# ndxspx1118 그림 2장 — 숫자는 calc_out.txt(Yahoo ^NDX·^GSPC 일별 종가, 가격 지수)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, BLU, LG = '#EA580C', '#111827', '#4B5563', '#2563EB', '#CBD5E1'
EP = ['2000 닷컴 버블', '2008 금융위기', '2020 코로나', '2022 금리 인상', '2025 관세 충격']
DD = [(82.9, 49.1), (53.7, 56.8), (28.0, 33.9), (35.6, 25.4), (22.9, 18.9)]
REC = [(15.6, '15년 7개월', 7.2, '7년 2개월'), (3.2, '3년 2개월', 5.45, '5년 5개월'), (0.29, '3개월 반', 0.5, '6개월'),
       (2.07, '2년 1개월', 2.05, '2년'), (0.34, '4개월', 0.35, '4개월')]
def base(title, foot):
    fig, ax = plt.subplots(figsize=(9, 6.2), dpi=100)
    fig.suptitle(title, fontproperties=Bs(23), color=INK, x=0.04, ha='left', y=0.965)
    fig.text(0.04, 0.035, foot, fontproperties=Bs(11), color=SUB)
    for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
    ax.spines['left'].set_color(LG); ax.set_xticks([])
    return fig, ax
# 01: 하락장 다섯 번, 고점에서 바닥까지
fig, ax = base('하락장 다섯 번, 고점에서 바닥까지 몇 % 빠졌나', 'Yahoo Finance 일별 종가(배당 뺀 가격 지수) · 1985년 10월~2026년 11월 18일 · 직접 계산')
for i, (n, (a, b)) in enumerate(zip(EP, DD)):
    y = (4 - i) * 1.0
    ax.barh(y + 0.19, a, color=ORG, height=0.36); ax.barh(y - 0.19, b, color=BLU, height=0.36)
    ax.text(a + 1, y + 0.19, f'-{a:.0f}%', va='center', fontproperties=Bs(15), color=ORG if a >= b else SUB)
    ax.text(b + 1, y - 0.19, f'-{b:.0f}%', va='center', fontproperties=Bs(15), color=BLU if b > a else SUB)
ax.set_yticks([4 - i for i in range(5)]); ax.set_yticklabels(EP, fontproperties=Bs(15), color=INK)
ax.set_xlim(0, 100)
fig.text(0.62, 0.86, '■ 나스닥100', fontproperties=Bs(15), color=ORG); fig.text(0.80, 0.86, '■ S&P500', fontproperties=Bs(15), color=BLU)
plt.subplots_adjust(left=0.24, right=0.97, top=0.83, bottom=0.1)
fig.savefig('pkg/img/01.png'); plt.close(fig)
# 02: 직전 고점 되찾기까지
fig, ax = base('직전 고점을 되찾기까지 걸린 시간', '고점일부터 그 값을 처음 다시 넘은 날까지 · 같은 자료 직접 계산')
for i, (n, (a, at, b, bt)) in enumerate(zip(EP, REC)):
    y = (4 - i) * 1.0
    ax.barh(y + 0.19, a, color=ORG, height=0.36); ax.barh(y - 0.19, b, color=BLU, height=0.36)
    ax.text(a + 0.2, y + 0.19, at, va='center', fontproperties=Bs(14), color=ORG)
    ax.text(b + 0.2, y - 0.19, bt, va='center', fontproperties=Bs(14), color=BLU)
ax.set_yticks([4 - i for i in range(5)]); ax.set_yticklabels(EP, fontproperties=Bs(15), color=INK)
ax.set_xlim(0, 19.5)
fig.text(0.62, 0.86, '■ 나스닥100', fontproperties=Bs(15), color=ORG); fig.text(0.80, 0.86, '■ S&P500', fontproperties=Bs(15), color=BLU)
plt.subplots_adjust(left=0.24, right=0.97, top=0.83, bottom=0.1)
fig.savefig('pkg/img/02.png'); plt.close(fig)
print('ok')
