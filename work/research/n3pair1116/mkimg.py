# n3pair1116 그림 2장 — 숫자는 ep/N-3/calc_out.txt §A·§C(2026)와 calc_out.txt(2027, 이 폴더)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, LG, LINE = '#EA580C', '#111827', '#4B5563', '#94A3B8', '#E5E7EB'
rows = [('3천만원', 2244440, 2238060), ('4천만원', 2935813, 2927123), ('5천만원', 3571586, 3560576), ('6천만원', 4195410, 4182100),
        ('7천만원', 4821313, 4805683), ('8천만원', 5367086, 5349146), ('1억원', 6530923, 6512223)]
fig, ax = plt.subplots(figsize=(10, 7.2), dpi=100); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, len(rows) + 2.2)
ax.text(0, len(rows) + 1.75, '연봉별 통장에 들어오는 돈(월)', fontproperties=Bs(24), color=INK, va='center')
hy = len(rows) + 0.8
for x, h in [(0.2, '연봉'), (4.2, '2026년'), (7.4, '2027년 1월부터')]:
    ax.text(x, hy, h, fontproperties=Bs(17), color=SUB, va='center')
for i, (n, a, b) in enumerate(rows):
    y = len(rows) - 1 - i + 0.3
    ax.plot([0, 10], [y - 0.5, y - 0.5], color=LINE, lw=1)
    ax.text(0.2, y, n, fontproperties=Bs(19), color=INK, va='center')
    ax.text(4.2, y, f'{a:,}원', fontproperties=Bs(19), color=INK, va='center')
    ax.text(7.4, y, f'{b:,}원', fontproperties=Bs(19), color=ORG, va='center')
fig.text(0.02, 0.045, '1인·식대 비과세 월 20만원·세금은 간이세액표 그대로 · 2027년은 국민연금 5%·장기요양(건강보험료의 13.90%)만 바꿔 직접 계산', fontsize=10.5, color=SUB)
fig.text(0.02, 0.012, '자료: 국민연금법 부칙·국민건강보험법 시행령 44조·소득세법 시행령 별표 2·보건복지부(2026.11.2)', fontsize=10, color=SUB)
plt.subplots_adjust(left=0.03, right=0.98, top=0.97, bottom=0.08); plt.savefig('pkg/img/01.png'); plt.close()
steps = [('3천→4천', 83.0), ('4천→5천', 76.3), ('5천→6천', 74.9), ('6천→7천', 75.1), ('7천→8천', 65.5), ('8천→1억(2천만원)', 69.8)]
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=100)
for i, (n, v) in enumerate(steps):
    y = len(steps) - 1 - i; c = ORG if v < 70 else LG
    ax.barh(y, v, color=c, height=0.6)
    ax.text(v + 0.8, y, f'{v}%', va='center', fontproperties=Bs(18), color=c if v < 70 else INK)
ax.set_yticks(range(len(steps))); ax.set_yticklabels([s[0] for s in steps][::-1], fontproperties=Bs(17), color=INK)
ax.set_xlim(0, 100); ax.set_xticks([]); [ax.spines[s].set_visible(False) for s in ['top', 'right', 'bottom']]
ax.set_title('연봉 1천만원 오를 때 통장에 남는 비율', fontproperties=Bs(21), color=INK, loc='left', pad=14)
fig.text(0.01, 0.04, '세전 월 증가분 중 통장에 남는 비율(8천→1억은 2천만원 오를 때) · 1인·식대 비과세 20만원·2026년 기준 직접 계산', fontproperties=Bs(11), color=SUB)
fig.text(0.01, 0.005, '자료: 소득세법 시행령 별표 2 간이세액표(2026.2.27)·4대보험 시행령', fontsize=10, color=SUB)
plt.tight_layout(rect=(0, 0.07, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
