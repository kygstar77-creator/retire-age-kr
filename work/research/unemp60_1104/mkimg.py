# unemp60_1104 그림 2장 — 실업크레딧 나라 지원(60세 전·정년) · 실업 신고 늦을 때 못 받는 돈(calc.py)
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
# 01 실업크레딧 나라 지원 — 실업급여 270일(9번) · 인정소득 상한 70만원
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
rows = [('60세 전에 퇴직', 448875, GR, '약 44만 9천원'), ('60세 정년퇴직', 0, ORG, '0원')]
y = 2.0
for lab, v, c, t in rows:
    ax.text(-3, y, lab, ha='right', va='center', fontproperties=Bs(19), color=INK)
    ax.barh(y, max(v / 1e4, 0.6), color=c, height=0.6)
    ax.text(max(v / 1e4, 0.6) + 1.5, y, t, va='center', fontproperties=Bs(20), color=c if v == 0 else INK)
    y -= 1.1
ax.set_xlim(-22, 62); ax.set_ylim(0.3, 2.6); ax.axis('off')
fig.text(0.05, 0.9, '실업급여 270일 동안 나라가 내 주는 연금 보험료', fontproperties=Bs(21), color=INK)
fig.text(0.05, 0.83, '실업크레딧 · 인정소득 상한 70만원 · 9.5%의 75% × 9번 · 다 받을 때까지 60세 전이면', fontsize=14, color=SUB)
fig.text(0.05, 0.03, '국민연금법 제19조의2 · 국민연금공단 실업크레딧 안내(11월 3일 조회)로 직접 계산', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.8, bottom=0.08, left=0.03, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 실업 신고를 늦게 하면 못 받는 돈 — 50세 이상·10년 이상(270일)·하루 66,048원
rows = [('89일째까지 신고', 0, '못 받는 돈 없음'), ('120일째 신고', 2047488, '약 205만원 (31일)'), ('150일째 신고', 4028928, '약 403만원 (61일)')]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
y = 3.0
for lab, v, t in rows:
    ax.text(-8, y, lab, ha='right', va='center', fontproperties=Bs(18), color=INK)
    ax.barh(y, max(v / 1e4, 2), color=ORG if v else GR, height=0.6)
    ax.text(max(v / 1e4, 2) + 6, y, t, va='center', fontproperties=Bs(18), color=ORG if v else SUB)
    y -= 1.1
ax.set_xlim(-130, 560); ax.set_ylim(0.4, 3.6); ax.axis('off')
fig.text(0.05, 0.9, '실업 신고가 늦으면 못 받는 실업급여', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.83, '퇴직 다음 날부터 센 날 · 50세 이상 10년 넘게 가입(270일) · 하루 66,048원', fontsize=14, color=SUB)
fig.text(0.05, 0.03, '고용보험법 제48조(12개월)·제49조(대기 7일)·별표1로 직접 계산, 12개월은 365일로 셈', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.8, bottom=0.08, left=0.03, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
