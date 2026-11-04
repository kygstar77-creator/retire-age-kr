# yellow1105 그림 2장 — 같은 3,000만원 폐업 vs 해지 세금(S6 예시표·calc.py), 해지 세금 셈 순서(S1④·S3·S4)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, GR, SUB = '#EA580C', '#111827', '#94A3B8', '#6B7280'
# 01
fig, ax = plt.subplots(figsize=(9, 5.4), dpi=100)
rows = [('폐업해서 공제금으로', 1_025_183, GR, '퇴직소득세 약 103만원'), ('폐업 전에 그냥 해지', 4_950_000, ORG, '기타소득세 최소 약 495만원')]
mx = 4_950_000
for i, (lab, v, c, t) in enumerate(rows):
    y = 1 - i
    ax.barh(y, v, color=c, height=0.5)
    ax.text(-mx*0.03, y, lab, va='center', ha='right', fontproperties=Bs(16), color=INK)
    ax.text(v + mx*0.02, y, t, va='center', fontproperties=Bs(15), color=c if c == ORG else INK)
ax.axvline(4_950_000, ymin=0.08, ymax=0.92, color=INK, ls='--', lw=1.2)
ax.text(4_950_000, 1.55, '5년 동안 공제로 아낀 세금 약 495만원', ha='center', fontsize=13, color=INK)
ax.set_xlim(0, mx*1.75); ax.set_ylim(-0.6, 1.8); ax.axis('off')
fig.text(0.05, 0.9, '노란우산 3,000만원, 받는 길에 따라 세금이 이만큼 달라요', fontproperties=Bs(21), color=INK)
fig.text(0.05, 0.03, '월 50만원씩 5년 · 세율 16.5% 구간 · 중소기업중앙회 공제금 지급예시표, 조세특례제한법 제86조의3 (2026년 11월 4일 확인)', fontsize=10, color=SUB)
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.27, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02
fig, ax = plt.subplots(figsize=(9, 5.0), dpi=100)
steps = [('1', '해지 환급금에서\n공제 못 받고 낸 돈을 빼요', '남은 돈 = 기타소득'),
         ('2', '기타소득의 16.5%를\n먼저 떼요', '소득세 15% + 지방세 1.5%'),
         ('3', '300만원을 넘으면\n다음 해 다른 소득과 합쳐요', '세율이 더 오를 수 있어요')]
for i, (n, a, b) in enumerate(steps):
    x = 0.5 + i * 3.1
    ax.scatter([x], [1.55], s=2600, color=ORG if i != 1 else INK, zorder=3)
    ax.text(x, 1.55, n, ha='center', va='center', fontproperties=Bs(18), color='white', zorder=4)
    ax.text(x - 0.35, 0.85, a, ha='left', va='top', fontproperties=Bs(15), color=INK, linespacing=1.4)
    ax.text(x - 0.35, -0.05, b, ha='left', va='top', fontsize=12, color=SUB)
    if i < 2: ax.annotate('', xy=(x + 2.5, 1.55), xytext=(x + 0.5, 1.55), arrowprops=dict(arrowstyle='->', color=GR, lw=2))
ax.set_xlim(-0.2, 9.2); ax.set_ylim(-0.6, 2.2); ax.axis('off')
fig.text(0.05, 0.88, '폐업 전 노란우산 해지, 세금은 이 순서로 붙어요', fontproperties=Bs(21), color=INK)
fig.text(0.05, 0.04, '조세특례제한법 제86조의3 ④ · 소득세법 제129조 ①6호나 · 제14조 ③8호가 · 중소기업중앙회 해약환급금 안내 (2026년 11월 4일 확인)', fontsize=10, color=SUB)
fig.subplots_adjust(top=0.8, bottom=0.1, left=0.03, right=0.98)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
