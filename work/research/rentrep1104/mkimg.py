# rentrep1104 그림 2장 — 늦게 낸 기간별 과태료(시행령 별표3 마.1)·서울 아파트 월세 계약 칸(calc.py)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
# 01 늦게 낸 기간별 과태료 — 계약금액 4칸 모두(별표3 마.1)
per = ['3개월\n이하', '6개월\n이하', '1년\n이하', '2년\n이하', '2년\n넘음']
rows = [('1억 미만', (2, 4, 6, 8, 10), '#CBD5E1'), ('1억~3억', (3, 8, 10, 13, 15), '#64748B'), ('3억~5억', (4, 12, 16, 20, 25), '#F59E0B'), ('5억 이상', (5, 15, 20, 25, 30), ORG)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for k, (n, v, c) in enumerate(rows):
    off = (k - 1.5) * 0.2
    ax.bar([x + off for x in range(5)], v, width=0.19, color=c)
    for x, y in enumerate(v): ax.text(x + off, y + 0.5, str(y), ha='center', fontsize=10.5, color=INK if k < 3 else ORG)
for x in range(5): ax.text(x, -1.2, per[x], ha='center', va='top', fontsize=13, color=SUB)
for k, (n, v, c) in enumerate(rows):
    ax.bar(-0.55 + k * 1.15, 0, color=c); fig.text(0.07 + k * 0.17, 0.765, '■ ' + n, fontsize=13, color=c if k else '#94A3B8')
ax.set_ylim(-6.5, 33); ax.set_xlim(-0.6, 4.6); ax.axis('off')
fig.text(0.05, 0.9, '늦게 낸 기간별 과태료(만원)', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.83, '계약금액 칸별 · 거짓 신고는 금액과 상관없이 100만원', fontsize=14, color=SUB)
fig.text(0.05, 0.03, '부동산 거래신고 등에 관한 법률 시행령 별표3(2025.4.29 개정, 11월 4일 확인)', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.74, bottom=0.08, left=0.03, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 서울 아파트 월세 계약 칸 — 보증금만 볼 때 vs 보증금+월세×200 (calc_out.txt)
names = ['1억원 미만', '1억~3억원', '3억~5억원', '5억원 이상']
a, b = (38.0, 33.0, 13.2, 15.8), (8.7, 35.3, 18.4, 37.6)
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
y = 3.3
for n, p, q in zip(names, a, b):
    ax.text(-2, y, n, ha='right', va='center', fontproperties=Bs(16), color=INK)
    ax.barh(y + 0.2, p, color=GR, height=0.36); ax.text(p + 0.8, y + 0.2, f'보증금만 {p:.0f}%', va='center', fontsize=13, color=SUB)
    ax.barh(y - 0.2, q, color=ORG, height=0.36); ax.text(q + 0.8, y - 0.2, f'월세×200 더하면 {q:.0f}%', va='center', fontproperties=Bs(14), color=ORG)
    y -= 1.05
ax.set_xlim(-17, 60); ax.set_ylim(-0.4, 3.8); ax.axis('off')
fig.text(0.05, 0.9, '서울 아파트 월세 계약, 과태료 칸이 올라가요', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.83, '9~10월 계약 1만 5,597건 · 계약금액 = 보증금 + 월세×200', fontsize=14, color=SUB)
fig.text(0.05, 0.03, '국토교통부 아파트 전월세 실거래(11월 4일 받음)로 직접 계산', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.8, bottom=0.08, left=0.03, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
