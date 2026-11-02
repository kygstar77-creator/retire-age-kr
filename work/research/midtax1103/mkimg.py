# midtax1103 그림 2장 — 대상 판단(시행령 제123조)·기준액별 고지 금액(calc.py, 제65조·제86조·제77조·시행령 제140조)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR, BLU = '#EA580C', '#111827', '#4B5563', '#94A3B8', '#2563EB'
# 01 누가 고지 받나
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
fig.text(0.05, 0.9, '중간예납 고지, 누가 받나', fontproperties=Bs(22), color=INK)
L = [('연금·이자·배당만', '고지 없음'), ('주택 월세 2천만원 이하만', '고지 없음'), ('올해 새로 시작한 사업', '고지 없음')]
R = [('연금 + 상가 월세', '고지 대상'), ('주택 월세 2천만원 초과', '고지 대상'), ('작년부터 하던 사업', '고지 대상')]
for i, ((a, b), (c, d)) in enumerate(zip(L, R)):
    y = 7.2 - i * 2.4
    ax.text(0.3, y, a, fontsize=16, color=INK, va='center'); ax.text(0.3, y - 0.8, b, fontproperties=Bs(16), color=BLU, va='center')
    ax.text(5.3, y, c, fontsize=16, color=INK, va='center'); ax.text(5.3, y - 0.8, d, fontproperties=Bs(16), color=ORG, va='center')
ax.plot([5.0, 5.0], [0.6, 8.2], color=GR, lw=1.5)
fig.text(0.05, 0.03, '소득세법 제65조①·시행령 제123조 (국가법령정보센터, 2026년 11월 3일 확인)', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.08, left=0.03, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 기준액별 고지 금액
rows = [('기준액 90만원', 0, '고지 없음 (절반 45만원 < 50만원)'), ('기준액 300만원', 150, '150만원'), ('기준액 2,400만원', 1200, '1,200만원 (200만원은 나눠 내기)')]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (lab, v, t) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.barh(y, max(v, 8), color=GR if v == 0 else ORG, height=0.5)
    ax.text(max(v, 8) + 25, y, t, va='center', fontproperties=Bs(16), color=SUB if v == 0 else ORG)
    ax.text(-30, y, lab, ha='right', va='center', fontsize=15, color=INK)
ax.set_xlim(-560, 2100); ax.set_ylim(-0.7, 2.7); ax.axis('off')
fig.text(0.05, 0.9, '고지 금액 = 작년 세금의 절반', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.03, '기준액 = 작년 11월 중간예납 + 올해 5월 확정신고 납부 − 환급 · 소득세법 제65조·제86조·제77조, 시행령 제140조', fontsize=10.5, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.03, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
