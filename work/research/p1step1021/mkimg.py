# p1step1021 그림 3장 — 숫자는 calc.py(국민연금법 제63조의2·소득세법 제47조)·공단 안내·복지부 보도자료
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
A = 3_193_511
def cut(inc, p):
    e = inc - A
    c = 0 if e < 2e6 else 150_000 + (e-2e6)*.15 if e < 3e6 else 300_000 + (e-3e6)*.2 if e < 4e6 else 500_000 + (e-4e6)*.25
    return min(c, p/2)
def ded(t):
    d = t*.7 if t <= 5e6 else 3.5e6+(t-5e6)*.4 if t <= 15e6 else 7.5e6+(t-15e6)*.15 if t <= 45e6 else 12e6+(t-45e6)*.05 if t <= 100e6 else 14.75e6+(t-100e6)*.02
    return min(d, 20e6)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
# 00 표지 — 짙은 보라 바탕, 큰 글 두 줄 + 월급별 월 감액 막대
BG, WH, LG = '#3B1F52', '#FFFFFF', '#D6C4E8'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.875, '국민연금 감액 519만원', fontsize=66, fontproperties=B, color=WH)
fig.text(0.06, 0.765, '세전 월급 632만원쯤부터', fontsize=66, fontproperties=B, color='#FB923C')
fig.text(0.06, 0.715, '넘는 순간 월 15만원이 깎여요 · 연금 월 100만원 기준', fontsize=23, color=LG)
ax = fig.add_axes([0.08, 0.14, 0.86, 0.5]); ax.set_facecolor(BG)
rows = [('월급 600만원', 0), ('월급 632만원', 150), ('월급 700만원', 247), ('월급 800만원', 419)]
for i, (n, v) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.barh(y, max(v, 3), height=0.55, color='#FB923C' if v else LG)
    ax.text(max(v, 3) + 6, y, '안 깎여요' if v == 0 else f'월 {round(v/10)}만원', va='center', fontproperties=Bs(36), color=WH)
    ax.text(0, y + 0.43, n, va='center', fontproperties=Bs(25), color=LG)
ax.set_xlim(0, 560); ax.set_ylim(-0.5, 3.8); ax.axis('off')
fig.text(0.06, 0.03, '국민연금법 제63조의2 · 소득세법 제47조로 계산 · 세전 월급 12개월, 다른 소득 없음', fontsize=19, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100*100/1080, facecolor=BG); plt.close(fig)
# 01 공제 뒤 한 달 소득 → 월 감액, 연금 100만원 vs 60만원
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)
xs = [x*1e4 for x in range(450, 821, 1)]
ax.plot([x/1e4 for x in xs], [cut(x, 1e6)/1e4 for x in xs], color=ORG, lw=3.5, label='연금 월 100만원')
ax.plot([x/1e4 for x in xs], [cut(x, 6e5)/1e4 for x in xs], color='#1E3A8A', lw=3, label='연금 월 60만원')
ax.axvline(519.35, color=GR, ls='--', lw=1.5)
ax.text(524, 4, '519만원', fontproperties=Bs(16), color=SUB)
ax.legend(prop=Bs(17), loc='upper left', frameon=False)
ax.set_xlabel('공제를 뺀 한 달 소득(만원)', fontproperties=Bs(15)); ax.tick_params(labelsize=14)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.93, '한 달 소득별 연금이 깎이는 돈', fontsize=26, fontproperties=B, color=INK)
fig.text(0.05, 0.88, '519만원을 넘으면 15만원부터, 한도는 연금의 절반이에요', fontsize=17, color=SUB)
fig.text(0.05, 0.02, '국민연금법 제63조의2(2026-06-17 시행)·공단 A값 3,193,511원 · 파이어맵 계산', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.14)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 환급 숫자 세 개
fig = plt.figure(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('#FFFFFF')
fig.text(0.05, 0.92, '2025년에 깎인 연금, 돌려받아요', fontsize=26, fontproperties=B, color=INK)
fig.text(0.05, 0.86, '신청 없이 7월 말부터 차례로 들어와요', fontsize=17, color=SUB)
for i, (big, small) in enumerate([('약 10만 명', '환급 대상'), ('약 445억원', '환급 규모'), ('약 60만원', '한 사람 평균(12개월분)')]):
    y = 0.64 - i*0.24
    fig.text(0.07, y, big, fontsize=46, fontproperties=B, color=ORG)
    fig.text(0.07, y-0.07, small, fontsize=20, color=SUB)
fig.text(0.05, 0.03, '보건복지부 보도자료 2026-06-16 · 2025년 소득 508만 9,062원 미만 기준', fontsize=12, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
