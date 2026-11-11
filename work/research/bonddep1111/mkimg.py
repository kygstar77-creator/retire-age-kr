# bonddep1111 그림 2장 — 01 국고채 3년 vs 정기예금(신규) 2021~2026.9 · 02 2025.8→2026.9 오른 폭
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, ORG, INK, SUBC, GR = '#1D4ED8', '#EA580C', '#111827', '#6B7280', '#CBD5E1'
d = json.load(open('raw/ecos_1111.json', encoding='utf-8'))
k = {t: float(v) for t, v, _ in d['ktb3_m']}; p = {t: float(v) for t, v, _ in d['dep_BEABAA211']}
ms = [m for m in sorted(set(k) & set(p)) if m >= '202101']
x = list(range(len(ms)))
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.plot(x, [k[m] for m in ms], color=GR, lw=3.5)
ax.plot(x, [p[m] for m in ms], color=BLUE, lw=3.5)
ia, ib = ms.index('202210'), ms.index('202211')
ax.plot([ia], [k['202210']], 'o', color=SUBC, ms=9); ax.plot([ib], [p['202211']], 'o', color=BLUE, ms=9)
ax.text(ia - 1, k['202210'] + 0.15, '국고채 꼭대기\n2022년 10월', ha='right', fontproperties=Bs(13), color=SUBC)
ax.text(ib + 1, p['202211'] + 0.12, '예금 꼭대기\n2022년 11월', ha='left', fontproperties=Bs(13), color=BLUE)
il = len(ms) - 1
ax.annotate('', xy=(il, p[ms[il]]), xytext=(il, k[ms[il]]), arrowprops=dict(arrowstyle='<->', color=ORG, lw=2.5))
ax.text(il - 1, (p[ms[il]] + k[ms[il]]) / 2, '지금 차이\n0.6%p', ha='right', va='center', fontproperties=Bs(15), color=ORG)
ax.text(2, 3.1, '국고채 3년', fontproperties=Bs(14), color=SUBC); ax.text(2, 0.55, '정기예금(새로 든 것)', fontproperties=Bs(14), color=BLUE)
yi = [ms.index(f'{y}01') for y in range(2021, 2027)]
ax.set_xticks(yi); ax.set_xticklabels([f'{y}' for y in range(2021, 2027)], fontproperties=Bs(14))
ax.set_ylim(0, 4.8); ax.set_yticks([1, 2, 3, 4]); ax.set_yticklabels(['1%', '2%', '3%', '4%'], fontsize=13, color=SUBC)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.grid(axis='y', color='#F1F5F9')
fig.text(0.05, 0.92, '예금 금리는 국고채를 한 달쯤 뒤에 따라갔다', fontproperties=Bs(21), color=INK)
fig.text(0.05, 0.02, '한국은행 경제통계(ECOS) 월평균 · 정기예금은 예금은행 신규취급액 가중평균 · 2026년 9월까지', fontsize=11, color=SUBC)
fig.subplots_adjust(top=0.85, bottom=0.12, left=0.07, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
lab = ['기준금리', '국고채 3년', '정기예금']; val = [0.5, 1.56, 0.91]; col = [GR, SUBC, BLUE]
ax.barh([2, 1, 0], val, color=col, height=0.55)
for i, (l, v) in enumerate(zip(lab, val)):
    ax.text(-0.05, 2 - i, l, ha='right', va='center', fontproperties=Bs(17), color=INK)
    ax.text(v + 0.04, 2 - i, f'+{v:.2f}%p', va='center', fontproperties=Bs(19), color=BLUE if i == 2 else INK)
ax.set_xlim(-0.75, 2.0); ax.set_ylim(-0.6, 2.6); ax.axis('off')
fig.text(0.05, 0.9, '1년 1개월 동안 오른 폭 (2025년 8월 → 2026년 9월)', fontproperties=Bs(20), color=INK)
fig.text(0.05, 0.02, '한국은행 경제통계(ECOS) 월 자료 · 기준금리 2.50%→3.00%', fontsize=11, color=SUBC)
fig.subplots_adjust(top=0.82, bottom=0.1)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
