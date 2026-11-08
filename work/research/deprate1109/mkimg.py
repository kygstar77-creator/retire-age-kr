# deprate1109 그림 2장 — 숫자는 calc_out.txt(금감원 금융상품 한눈에 10/20·11/9, 한국은행 ECOS 11/9 조회)
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR, LG = '#EA580C', '#111827', '#4B5563', '#94A3B8', '#CBD5E1'

# 01 한 달 새 1년 기본금리 (10/20 → 11/9)
rows = [('전북은행 JB 다이렉트', 3.92, 3.98), ('수협은행 헤이정기예금', 3.81, 3.91), ('케이뱅크 내맘대로', 3.71, 3.81),
        ('산업은행 KDB', 3.6, 3.8), ('카카오뱅크 정기예금', 3.7, 3.8), ('기업은행 굴리기통장', 3.6, 3.62),
        ('우리은행 WON플러스', 3.6, 3.6), ('국민은행 KB Star', 2.4, 2.4), ('하나은행 하나의정기예금', 2.3, 2.3)]
fig, ax = plt.subplots(figsize=(9, 7.2), dpi=100)
for i, (n, a, b) in enumerate(rows[::-1]):
    up = b > a
    ax.plot([a, b], [i, i], color=ORG if up else LG, lw=4, solid_capstyle='round', zorder=1)
    ax.scatter([a], [i], s=70, color=GR, zorder=2)
    ax.scatter([b], [i], s=110, color=ORG if up else SUB, zorder=3)
    ax.text(b + 0.05, i, f'{b:g}%' + (f'  (+{b-a:.2f}%p)' if up else '  그대로'), va='center',
            fontproperties=Bs(14), color=ORG if up else SUB)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]], fontproperties=Bs(13.5))
ax.set_xlim(2.1, 4.75); ax.set_xticks([2.5, 3.0, 3.5, 4.0]); ax.set_xticklabels(['2.5%', '3.0%', '3.5%', '4.0%'], fontsize=12, color=SUB)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0); ax.grid(axis='x', color='#EEF2F7')
fig.text(0.04, 0.93, '1년 정기예금 기본금리, 한 달 새 바뀐 곳', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.885, '회색 점 10월 20일 → 주황 점 11월 9일 (우대 뺀 금리)', fontsize=13, color=SUB)
fig.text(0.04, 0.02, '금융감독원 금융상품 한눈에 정기예금 공시(2026.10.20·11.9 조회)', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.3, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 한국은행 평균 예금금리와 기준금리
e = json.load(open('raw/ecos_1109.json', encoding='utf-8'))
dep = [(m[4:6], float(v)) for m, v, _ in e['dep_1to2y']]
base = {m[4:6]: float(v) for m, v, _ in e['base']}
x = list(range(len(dep))); fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
ax.plot(x, [v for _, v in dep], color=ORG, lw=3.5, marker='o', ms=7)
ax.step(x, [base[m] for m, _ in dep], where='post', color=GR, lw=2.5)
ax.text(x[0], dep[0][1] + 0.08, f'{dep[0][1]:g}%', ha='center', fontproperties=Bs(14), color=ORG)
ax.text(x[-1], dep[-1][1] + 0.08, f'{dep[-1][1]:g}%', ha='center', fontproperties=Bs(16), color=ORG)
ax.text(x[-1] + 0.15, 3.0 - 0.13, '기준금리 3.0%', ha='right', fontproperties=Bs(13), color=SUB)
ax.text(0.1, 2.5 - 0.13, '기준금리 2.5%', fontproperties=Bs(13), color=SUB)
ax.set_xticks(x); ax.set_xticklabels([f'{int(m)}월' for m, _ in dep], fontsize=12.5, color=SUB)
ax.set_ylim(2.2, 3.95); ax.set_yticks([2.5, 3.0, 3.5]); ax.set_yticklabels(['2.5%', '3.0%', '3.5%'], fontsize=12, color=SUB)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.grid(axis='y', color='#EEF2F7')
fig.text(0.05, 0.92, '은행 정기예금 평균 금리, 올해 얼마나 올랐나', fontproperties=Bs(21), color=INK)
fig.text(0.05, 0.865, '주황: 새로 든 1~2년 정기예금 평균 · 회색: 기준금리 (2026년)', fontsize=13, color=SUB)
fig.text(0.05, 0.02, '한국은행 경제통계시스템 121Y002·722Y001 (2026.11.9 조회, 평균금리는 9월이 최신)', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.1, left=0.1, right=0.96)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
