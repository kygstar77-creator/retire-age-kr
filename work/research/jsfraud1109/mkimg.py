# jsfraud1109 그림 2장 — 숫자는 research.md 대조 칸(국토부 2026.11.9 보도자료 3쪽 예시·특별법 제25조의9~11·부칙)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, LG = '#EA580C', '#111827', '#4B5563', '#CBD5E1'

# 01 보증금 2억원, 배당 3천만원
fig = plt.figure(figsize=(9, 5.6), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.86, '보증금 2억원, 배당 3천만원이면', fontproperties=Bs(24), color=INK)
ax = fig.add_axes([0.06, 0.3, 0.88, 0.4]); ax.set_xlim(0, 20000); ax.set_ylim(0, 1); ax.axis('off')
ax.barh(0.5, 20000, height=0.5, color='#F1F5F9')
ax.barh(0.5, 3000, height=0.5, color=LG)
ax.barh(0.5, 3667, left=3000, height=0.5, color=ORG)
ax.axvline(6667, ymin=0.1, ymax=0.9, color=INK, lw=2)
ax.text(1500, 0.5, '배당\n3천만원', ha='center', va='center', fontproperties=Bs(14), color=INK)
ax.text(4833, 0.5, '받는 돈\n3,667만원', ha='center', va='center', fontproperties=Bs(14), color='white')
ax.text(6800, 0.95, '기준선 6,667만원(보증금의 3분의 1)', fontproperties=Bs(14), color=INK, va='center')
ax.text(19800, 0.5, '보증금 2억원', ha='right', va='center', fontproperties=Bs(14), color=SUB)
fig.text(0.06, 0.16, '기준선까지 모자란 만큼만 채워 줘요', fontproperties=Bs(18), color=ORG)
fig.text(0.06, 0.05, '국토교통부 보도자료(2026.11.9) 계산식 · 특별법 제25조의9 · 파이어맵 계산', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 신청 순서
fig = plt.figure(figsize=(9, 5.6), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.86, '신청은 이 순서로', fontproperties=Bs(24), color=INK)
ax = fig.add_axes([0.04, 0.2, 0.92, 0.55]); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
ax.plot([0.6, 9.4], [3, 3], color=LG, lw=6, solid_capstyle='round')
pts = [(0.9, '11월 10일', '온라인 신청 시작', ORG),
       (3.4, '11월 13일', 'LH 지역본부도', INK),
       (6.0, '90일 안', '신청 뒤 결과 통지', INK),
       (8.9, '2029년\n11월 13일', '기존 피해자\n신청 기한', SUB)]
for x, a, b, c in pts:
    ax.scatter([x], [3], s=260, color=c, zorder=3)
    ax.text(x, 4.0, a, ha='center', va='bottom', fontproperties=Bs(16), color=c)
    ax.text(x, 2.1, b, ha='center', va='top', fontsize=13.5, color=SUB)
fig.text(0.06, 0.1, '온라인은 LH 청약플러스 · 문의 1600-1004', fontproperties=Bs(16), color=ORG)
fig.text(0.06, 0.03, '국토교통부 보도자료(2026.11.9) 3·8쪽 · 특별법 부칙(2026.11.13 시행)', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
