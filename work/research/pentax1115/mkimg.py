# pentax1115 그림 2장 — 숫자는 calc_out.txt(국세청 원천징수>연금소득)
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
# 1) 1년에 받는 연금저축·IRP 연금과 세금(65세, 다른 소득 없음)
rows = [('1,500만원\n(5.5%)', 82.5, BLU), ('1,600만원\n(16.5%)', 264.0, ORG), ('1,600만원\n(종합과세)', 52.8, LG), ('2,000만원\n(16.5%)', 330.0, ORG), ('2,000만원\n(종합과세)', 76.6, LG)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, v, c) in enumerate(rows):
    ax.bar(i, v, color=c, width=0.6)
    ax.text(i, v + 6, f'{v:,.1f}만원'.replace('.0만', '만'), ha='center', fontproperties=Bs(15), color=INK)
ax.set_xticks(range(len(rows))); ax.set_xticklabels([n for n, _, _ in rows], fontproperties=Bs(13), color=INK)
ax.set_ylim(0, 380); ax.set_yticks([])
for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
ax.set_title('1,500만원 넘으면, 16.5%와 종합과세 세금 차이', fontproperties=Bs(20), color=INK, loc='left', pad=14)
fig.text(0.01, 0.01, '65세·다른 소득 없음·본인 기본공제만·세액공제 빼기 전, 지방소득세 포함 · 자료: 국세청 원천징수>연금소득(2026.11.14 조회)', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/01.png'); plt.close()
# 2) 국민연금(세금 붙는 몫)을 같이 받을 때 — 사적연금 2,000만원에 붙는 세금
Y = [0, 600, 1200, 1800, 2400, 3000, 3600, 4060]; V = [76.6, 141.9, 200.6, 255.4, 302.0, 311.9, 321.8, 330.3]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
ax.plot(range(len(Y)), V, color=BLU, lw=3, marker='o', ms=8)
for i, v in enumerate(V): ax.text(i, v - 26, f'{v:.0f}만원', ha='center', fontproperties=Bs(14), color=BLU)
ax.axhline(330, color=ORG, lw=2, ls='--'); ax.text(0, 340, '16.5% 분리과세 330만원', fontproperties=Bs(14), color=ORG)
ax.set_xticks(range(len(Y))); ax.set_xticklabels([f'{y:,}' if y else '없음' for y in Y], fontproperties=Bs(13), color=INK)
ax.set_xlabel('1년에 받는 국민연금 중 세금 붙는 부분(만원)', fontproperties=Bs(13), color=SUB)
ax.set_ylim(0, 380); ax.set_yticks([])
for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
ax.set_title('연금저축 2,000만원, 종합과세로 늘어나는 세금', fontproperties=Bs(20), color=INK, loc='left', pad=14)
fig.text(0.01, 0.01, '65세·다른 소득 없음·본인 기본공제만·세액공제 빼기 전, 지방소득세 포함 · 갈림점 연 4,060만원 · 자료: 국세청 원천징수>연금소득', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
