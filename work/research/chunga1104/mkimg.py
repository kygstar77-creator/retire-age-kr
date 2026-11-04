# chunga1104 그림 2장 — 50대 경우별 점수(calc.py)·부모님 집이 있을 때(별표1·제53조)
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
# 01 50대 경우별 가점
rows = [('부모님(무주택) 모심', 77, ORG), ('부부+미혼 자녀 둘', 67, INK), ('자녀 한 명 등본 분리', 62, GR), ('부부만', 57, GR), ('5년 전 집 팔았음', 47, GR)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (lab, v, c) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.barh(y, v, color=c, height=0.55)
    ax.text(-1.5, y, lab, ha='right', va='center', fontproperties=Bs(16), color=INK)
    ax.text(v + 1, y, f'{v}점', va='center', fontproperties=Bs(18), color=c if c != GR else SUB)
ax.set_xlim(-38, 92); ax.set_ylim(-0.6, len(rows) - 0.4); ax.axis('off')
fig.text(0.05, 0.89, '52세 무주택 부부, 경우마다 청약 가점은', fontproperties=Bs(23), color=INK)
fig.text(0.05, 0.815, '84점 만점 · 무주택 기간은 모두 만점(32점)인데 차이는 부양가족에서', fontsize=15, color=SUB)
fig.text(0.05, 0.03, '주택공급에 관한 규칙 별표1 점수표로 계산 · 부부 통장 각 10년(본인 12점+배우자 3점) · 5년 전 집을 판 경우만 무주택 12점', fontsize=10.5, color='#6B7280')
fig.subplots_adjust(top=0.78, bottom=0.08, left=0.03, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 부모님 집이 있을 때
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100); ax.axis('off')
fig.text(0.05, 0.88, '등본에 같이 사는 아버지(60세 넘음)가 집이 있다면', fontproperties=Bs(22), color=INK)
for x, head, mark, body, c in [(0.05, '무주택인지 볼 때', '무주택 그대로', '60세 넘은 부모님 집은\n없는 것으로 봄', INK), (0.52, '부양가족을 셀 때', '두 분 모두 빠짐', '한 분이라도 집이 있으면\n부모님 둘 다 안 셈', ORG)]:
    from matplotlib.lines import Line2D; fig.add_artist(Line2D([x, x + 0.40], [0.70, 0.70], color=c, lw=5, transform=fig.transFigure))
    fig.text(x, 0.62, head, fontsize=17, color=SUB)
    fig.text(x, 0.49, mark, fontproperties=Bs(25), color=c)
    fig.text(x, 0.25, body, fontsize=16, color=INK, linespacing=1.5)
fig.text(0.05, 0.03, '주택공급에 관한 규칙 제53조제6호 · 별표1 제1호나목2) 단서·라목 단서(부양가족 판단엔 제53조제6호를 쓰지 않음)', fontsize=10.5, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
