# defer1027 그림 3장 — 숫자는 calc.py(국민연금법 62조 매달 0.6%·부칙 11143호 6조, 건보 7.19%·연금 50%·장기요양 0.1314) 결과
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
# 00 표지 — 짙은 올리브 바탕(최근 10장: 자줏빛·녹색·갈색·흰·청록·파랑), 주제어 + 미룬 햇수별 같아지는 나이 막대
BG, WH, LG = '#33300F', '#FFFFFF', '#E9E4C4'
rows = [('제때 받기', 140.0, LG), ('5년|절반만 미룸', 165.2, '#FB923C'), ('5년|다 미룸', 190.4, LG)]
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.865, '연기연금 피부양자', fontproperties=Bs(78), color=WH)
fig.text(0.06, 0.765, '월 140만원, 절반만 미뤄도 아슬아슬', fontproperties=Bs(48), color='#FB923C')
fig.text(0.06, 0.695, '한 달에 받는 돈(미루면 70세부터) · 점선 = 피부양자 선', fontsize=26, color=LG)
ax = fig.add_axes([0.06, 0.15, 0.88, 0.48]); ax.set_facecolor(BG)
for i, (lab, v, c) in enumerate(rows):
    ax.bar(i, v, color=c, width=0.7)
    ax.text(i, v - 16 if i == 1 else v + 4, f'{v:g}만원'.replace('.', '만 ').replace('만 2만원', '만 2천원').replace('만 4만원', '만 4천원'), ha='center', fontproperties=Bs(24 if i == 1 else 28), color=BG if i == 1 else c)
    ax.text(i, -6, lab.replace('|', chr(10)), ha='center', va='top', fontsize=23, color=WH, linespacing=1.3)
ax.axhline(166.7, color=WH, ls='--', lw=2.5, xmin=0.02, xmax=0.98)
ax.set_ylim(-48, 215); ax.set_xlim(-0.6, 2.6); ax.axis('off')
fig.text(0.06, 0.035, '오늘 돈 기준 · 연금은 해마다 오르고 선은 고정', fontsize=24, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 미룬 햇수별 피부양자 기준을 넘는 65세 연금
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
lines = [('1년 미룸', 155.4, '155만 4천원'), ('2년 미룸', 145.6, '145만 6천원'), ('3년 미룸', 137.0, '137만원'), ('4년 미룸', 129.3, '129만 3천원'), ('5년 미룸', 122.5, '122만 5천원')]
for i, (lab, v, s) in enumerate(lines):
    y = len(lines) - 1 - i
    ax.barh(y, v, color=ORG if i == 4 else GR, height=0.6)
    ax.text(v + 2, y, f'월 {s}까지 선 아래', va='center', fontproperties=Bs(17), color=INK)
ax.set_yticks(range(len(lines))); ax.set_yticklabels([r[0] for r in lines][::-1], fontsize=16)
ax.set_xticks([]); ax.set_xlim(0, 230)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.92, '미룬 햇수별, 65세 연금이 이만큼까지면 선 아래', fontproperties=Bs(21), color=INK)
fig.text(0.05, 0.865, '미루기 전 65세 연금 기준 · 오래 미룰수록 더 적은 연금으로도 선(월 약 166만 7천원)을 넘어요', fontsize=14, color=SUB)
fig.text(0.05, 0.02, '국민연금법 제62조 · 건강보험 피부양자 소득 기준 · 직접 계산', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.08, left=0.17)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 월 140만원, 세 가지 받는 법
fig = plt.figure(figsize=(9, 6.6), dpi=100); fig.patch.set_facecolor('#FFFFFF')
fig.text(0.05, 0.9, '65세 월 140만원이라면', fontproperties=Bs(23), color=INK)
fig.text(0.40, 0.79, '한 달에 받는 돈', fontsize=15, color=SUB, ha='center'); fig.text(0.80, 0.79, '같아지는 나이', fontsize=15, color=SUB, ha='center')
opts = [('제때 받기', '140만원', '-', '65세부터 · 선 아래'), ('5년 다 미루기', '190만 4천원', '86세쯤', '70세부터 · 선 넘음 · 건보료 월 7만 7천원쯤'), ('절반만 5년 미루기', '165만 2천원', '84세쯤', '70세부터(그전 5년은 월 70만원) · 선보다 1만 5천원 아래')]
for i, (a, b, c, d) in enumerate(opts):
    y = 0.66 - i * 0.2
    fig.text(0.05, y, a, fontproperties=Bs(18), color=INK)
    fig.text(0.40, y, b, fontproperties=Bs(21), color=ORG if i == 2 else INK, ha='center')
    fig.text(0.80, y, c, fontproperties=Bs(21), color=INK, ha='center')
    fig.text(0.05, y - 0.07, d, fontsize=13, color=SUB)
fig.text(0.05, 0.02, '국민연금법 제62조 · 건보료는 재산 없는 혼자 세대, 건강보험료율 7.19% · 오늘 돈·세금 빼고 계산', fontsize=12, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
