# cdrate1021 그림 3장 — 숫자는 한국은행 ECOS(raw/ecos_1021.json)·calc.py
import os, json, datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
e = json.load(open('raw/ecos_1021.json', encoding='utf-8'))
cd = {a: float(b) for a, b, c in e['cd91']}; kf = {a: float(b) for a, b, c in e['kofr']}; base = {a: float(b) for a, b, c in e['base']}
D = sorted(d for d in cd if d in kf and d >= '20251020')
X = [datetime.datetime.strptime(d, '%Y%m%d') for d in D]
# 00 표지 — 짙은 초록 바탕(옆 10장의 남색·흰 바탕과 구별), 큰 글 두 줄 + 1년 선 그래프 둘
BG, WH, LG = '#0E2A22', '#FFFFFF', '#A7C4B5'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.875, 'CD금리 vs KOFR 1년', fontsize=64, fontproperties=B, color=WH)
fig.text(0.06, 0.765, '1억이면 약 24만원 차이', fontsize=66, fontproperties=B, color='#FB923C')
fig.text(0.06, 0.715, '지난 1년 평균 2.86% vs 2.63% · 금리 내릴 땐 뒤집힌 적도', fontsize=23, color=LG)
ax = fig.add_axes([0.08, 0.14, 0.86, 0.52]); ax.set_facecolor(BG)
ax.plot(X, [cd[d] for d in D], color='#FB923C', lw=6)
ax.plot(X, [kf[d] for d in D], color=LG, lw=4)
ax.text(X[-1], cd[D[-1]] + 0.05, 'CD금리', ha='right', fontproperties=Bs(34), color='#FB923C')
ax.text(X[-1], kf[D[-1]] - 0.27, 'KOFR', ha='right', fontproperties=Bs(34), color=LG)
ax.set_ylim(2.3, 3.45); ax.set_yticks([]); ax.set_xticks([])
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.spines['bottom'].set_color(LG)
fig.text(0.06, 0.03, '한국은행 경제통계시스템 · 2025.10.20~2026.10.19 영업일 245일', fontsize=19, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 1년 선 그래프 — CD·KOFR·기준금리
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)
ax.plot(X, [cd[d] for d in D], color=ORG, lw=3, label='CD금리(91일)')
ax.plot(X, [kf[d] for d in D], color='#1E3A8A', lw=2.2, label='KOFR')
ax.step(X, [base.get(d, 3.0) for d in D], where='post', color=GR, lw=2, ls='--', label='기준금리')
ax.legend(prop=Bs(17), loc='upper left', frameon=False)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%y.%m')); ax.tick_params(labelsize=14)
ax.set_ylim(2.3, 3.45); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.1f}%'))
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.annotate('10/19 CD 3.25%', (X[-1], cd[D[-1]]), xytext=(-150, 18), textcoords='offset points', fontproperties=Bs(15), color=ORG)
ax.annotate('KOFR 3.05%', (X[-1], kf[D[-1]]), xytext=(-60, -55), textcoords='offset points', fontproperties=Bs(15), color='#1E3A8A')
fig.text(0.05, 0.93, '최근 1년 CD금리·KOFR·기준금리', fontsize=26, fontproperties=B, color=INK)
fig.text(0.05, 0.88, 'KOFR는 기준금리를 따라가고, CD금리는 그 위에서 먼저 움직였어요', fontsize=17, color=SUB)
fig.text(0.05, 0.02, '한국은행 경제통계시스템 시장금리(일별)·기준금리 · 2025.10.20~2026.10.19', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.1)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 1억 1년 단순 계산
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)
vals = [('KOFR 평균 연 2.63%', 263, GR), ('CD금리 평균 연 2.86%', 286, ORG)]
for i, (n, v, c) in enumerate(vals):
    ax.barh(i, v, height=0.5, color=c)
    ax.text(v + 4, i, f'약 {v}만원', va='center', fontsize=28, fontproperties=B, color=INK)
    ax.text(3, i + 0.4, n, va='center', fontsize=19, fontproperties=B, color=INK)
ax.set_xlim(0, 380); ax.set_ylim(-0.6, 1.9); ax.axis('off')
fig.text(0.05, 0.92, '1억원을 1년 두었다면 붙는 금리 몫', fontsize=26, fontproperties=B, color=INK)
fig.text(0.05, 0.86, '차이 약 24만원 · 세금·ETF 보수 떼기 전, 1년 평균 금리 그대로 가정', fontsize=17, color=SUB)
fig.text(0.05, 0.03, '한국은행 경제통계시스템 · 파이어맵 계산 · ETF 실제 수익률이 아님', fontsize=12, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
