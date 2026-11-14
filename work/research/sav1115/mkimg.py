# sav1115 그림 2장 — 01 적금(1-2년)·예금(1년) 신규취급 평균 금리 2012~2026 02 7% 광고 vs 기본금리 vs 실제 평균
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, ORG, INK, GR, SUBC = '#1D4ED8', '#EA580C', '#111827', '#CBD5E1', '#6B7280'
d = json.load(open('raw/ecos_rates.json', encoding='utf-8'))
sav = dict(d['BEABAA2122']); dep = dict(d['BEABAA2118'])
m = sorted(set(sav) & set(dep)); x = range(len(m))
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
for i, t in enumerate(m):
    if sav[t] < dep[t]: ax.axvspan(i - .5, i + .5, color='#FEF3C7', lw=0)
ax.plot(x, [dep[t] for t in m], color=BLUE, lw=2.4, label='정기예금(1년)')
ax.plot(x, [sav[t] for t in m], color=ORG, lw=2.4, label='정기적금(1~2년)')
ticks = [i for i, t in enumerate(m) if t.endswith('01') and int(t[:4]) % 2 == 0]
ax.set_xticks(ticks); ax.set_xticklabels([m[i][:4] for i in ticks], fontsize=11)
ax.text(len(m) - 3, 2.35, f"적금 {sav['202609']}%", ha='right', fontproperties=Bs(15), color=ORG, bbox=dict(fc='white', ec='none', pad=1))
ax.text(len(m) - 3, 4.35, f"예금 {dep['202609']}%", ha='right', fontproperties=Bs(15), color=BLUE, bbox=dict(fc='white', ec='none', pad=1))
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', labelsize=11); ax.legend(frameon=False, fontsize=13, loc='upper center', ncol=2)
fig.text(0.04, 0.92, '은행 적금 금리, 예금보다 낮은 달이 이어지는 중', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.86, '단위 % · 노란 칸 = 적금이 예금보다 낮았던 달(177개월 중 73개월)', fontsize=15, color=SUBC)
fig.text(0.04, 0.025, '한국은행 경제통계 예금은행 수신금리(신규취급액 기준) 2012년 1월~2026년 9월', fontsize=10, color=SUBC)
fig.subplots_adjust(top=0.80, bottom=0.10, left=0.07, right=0.98)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02
labs = ['광고 최고금리\n(우대 다 채움)', '그 상품들\n기본금리', '은행이 실제로 준\n적금 평균(9월)']
vals = [7.0, 3.0, sav['202609']]; txt = ['7%', '1.9~3%', f"{sav['202609']}%"]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.bar(range(3), vals, color=[GR, GR, ORG], width=.6)
for i, (v, t) in enumerate(zip(vals, txt)): ax.text(i, v + .15, t, ha='center', fontproperties=Bs(20), color=INK)
ax.set_xticks(range(3)); ax.set_xticklabels(labs, fontsize=14); ax.tick_params(axis='x', length=0, pad=10)
ax.set_ylim(0, 8.2); ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.92, '적금 7% 광고와 실제 평균 금리', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.86, '7% 상품 3개(경남은행·케이뱅크·카카오뱅크) · 오른쪽은 은행 전체 평균(참고)', fontsize=15, color=SUBC)
fig.text(0.04, 0.025, '금융감독원 금융상품통합비교공시(2026년 10월 공시) · 한국은행 정기적금(1~2년) 신규취급액 기준 2026년 9월', fontsize=10, color=SUBC)
fig.subplots_adjust(top=0.80, bottom=0.17, left=0.04, right=0.98)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
