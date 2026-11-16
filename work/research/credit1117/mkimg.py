# credit1117 그림 2장 — KCB 별첨2(금융위 2026.1.20) 3·5쪽, calc_out.txt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, LG = '#EA580C', '#111827', '#4B5563', '#94A3B8'
rows = [('카드포인트', 6309, 29060), ('증권', 4037, 20686), ('예·적금', 3388, 75209), ('보험금', 2579, 58506)]
band = [('950~1000점',28.6),('900~949점',16.1),('850~899점',7.6),('800~849점',5.5),('750~799점',10.2),('700~749점',16.4),('600~699점',9.6),('300~599점',2.1),('1~299점',3.9)]
fig, ax = plt.subplots(figsize=(10, 6.4), dpi=100)
for i, (n, v) in enumerate(band):
    y = len(band) - 1 - i; c = ORG if n.startswith('600') else (INK if n.startswith('950') else LG)
    ax.barh(y, v, color=c, height=0.62)
    ax.text(v + 0.4, y, f'{v}%', va='center', fontproperties=Bs(16), color=ORG if n.startswith('600') else INK)
ax.text(9.6 + 4.2, len(band) - 7, '← 697점(61세 이상 정보 부족자 평균)', va='center', fontproperties=Bs(15), color=ORG)
ax.set_yticks(range(len(band))); ax.set_yticklabels([b[0] for b in band][::-1], fontproperties=Bs(15), color=INK)
ax.set_xlim(0, 40); ax.set_xticks([]); [ax.spines[s].set_visible(False) for s in ['top', 'right', 'bottom']]
ax.set_title('신용점수 구간별 사람 비중 (KCB 평가 대상 5,030만 명)', fontproperties=Bs(20), color=INK, loc='left', pad=14)
fig.text(0.01, 0.04, '950점 이상 28.6% · 900점 이상 44.7% · 700점 미만 15.6% (직접 더함)', fontproperties=Bs(12), color=SUB)
fig.text(0.01, 0.005, '자료: 코리아크레딧뷰로(KCB) 2025년 검증 기준, 금융위원회 신용평가체계 개편 TF(2026.1.20) 별첨2', fontsize=10, color=SUB)
plt.tight_layout(rect=(0, 0.07, 1, 1)); plt.savefig('pkg/img/01.png'); plt.close()
g = [('청년(18~34세)', 734), ('외국인', 722), ('주부', 704), ('시니어(61세 이상)', 697)]
fig, ax = plt.subplots(figsize=(10, 5.2), dpi=100)
for i, (n, v) in enumerate(g):
    y = len(g) - 1 - i; c = ORG if n.startswith('시니어') else LG
    ax.barh(y, v, color=c, height=0.6)
    ax.text(v + 4, y, f'{v}점', va='center', fontproperties=Bs(18), color=ORG if n.startswith('시니어') else INK)
ax.set_yticks(range(len(g))); ax.set_yticklabels([x[0] for x in g][::-1], fontproperties=Bs(16), color=INK)
ax.set_xlim(600, 780); ax.set_xticks([]); [ax.spines[s].set_visible(False) for s in ['top', 'right', 'bottom']]
ax.set_title('3년간 카드·대출 없는 사람의 평균 신용점수', fontproperties=Bs(21), color=INK, loc='left', pad=14)
fig.text(0.01, 0.04, '막대는 600점부터 그림 · 시니어 387만 명으로 정보 부족자 중 가장 많음', fontproperties=Bs(12), color=SUB)
fig.text(0.01, 0.005, '자료: 코리아크레딧뷰로(KCB) 2024년 말 기준, 금융위원회 신용평가체계 개편 TF(2026.1.20) 별첨2', fontsize=10, color=SUB)
plt.tight_layout(rect=(0, 0.08, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
