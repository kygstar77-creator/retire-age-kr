# yen1021 그림 3장 — 숫자는 calc.py(ECOS 731Y001 · 하나은행 10/20 21시 고시)
import os, json, datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
ORG, NAVY, INK, SUB, GRY = '#EA580C', '#1E3A8A', '#111827', '#4B5563', '#9CA3AF'
r = sorted((d, float(v)) for d, v, _ in json.load(open('raw/ecos_jpy_daily.json', encoding='utf-8')) if v and v != '-')
xs = [datetime.datetime.strptime(d, '%Y%m%d') for d, _ in r]; ys = [v for _, v in r]
# 00 표지 1080x1080 — 큰 글 두 줄(위) + 2005~2026 선 그래프(아래)
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.875, '엔화 환율 18년 만에 최저', fontsize=60, fontproperties=B, color=INK)
fig.text(0.06, 0.765, '100엔 = 840원', fontsize=78, fontproperties=B, color=ORG)
fig.text(0.06, 0.715, '한국은행 원/100엔 매매기준율 · 2005년 1월 ~ 2026년 10월 20일', fontsize=20, color=SUB)
ax = fig.add_axes([0.09, 0.10, 0.84, 0.56])
ax.plot(xs, ys, color=NAVY, lw=2.2)
ax.axhline(840.18, color=ORG, lw=1.5, ls='--')
ax.scatter([xs[-1]], [ys[-1]], s=160, color=ORG, zorder=5)
ax.annotate('2026.10.20\n840원', (xs[-1], ys[-1]), xytext=(-150, -75), textcoords='offset points', fontsize=24, fontproperties=B, color=ORG)
d08 = datetime.datetime(2008, 1, 2)
ax.scatter([d08], [838.2], s=110, color=ORG, zorder=5)
ax.annotate('2008.1.2\n838원', (d08, 838.2), xytext=(15, -75), textcoords='offset points', fontsize=22, fontproperties=B, color=ORG)
d09 = datetime.datetime(2009, 3, 3)
ax.annotate('2009.3.3  1,621원', (d09, 1620.76), xytext=(18, -8), textcoords='offset points', fontsize=20, fontproperties=B, color=INK)
ax.set_ylim(650, 1720); ax.xaxis.set_major_locator(mdates.YearLocator(5)); ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(labelsize=18, colors=SUB); ax.set_yticks([800, 1000, 1200, 1400, 1600]); ax.grid(axis='y', color='#E5E7EB')
fig.text(0.06, 0.03, '자료: 한국은행 경제통계시스템(ECOS) 731Y001 · 파이어맵 정리', fontsize=16, color='#6B7280')
fig.savefig('pkg/img/00.png', dpi=100); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080); plt.close(fig)
# 01 10만엔 바꿀 때
fig, ax = plt.subplots(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
vals = [('매매기준율(실제로 바꾸는 값 아님)', 840910, GRY), ('하나은행 영업점 현찰 살 때', 855620, NAVY), ('하나은행 공항 영업점 현찰 살 때', 876000, ORG)]
def won(v): m, k = divmod(v, 10000); return f'{m}만 {k:,}원' if k else f'{m}만원'
for i, (n, v, c) in enumerate(vals[::-1]):
    ax.barh(i, v, height=0.5, color=c)
    ax.text(v + 6000, i, won(v), va='center', fontsize=24, fontproperties=B, color=INK)
    ax.text(8000, i + 0.4, n, va='center', fontsize=17, fontproperties=B, color=INK)
ax.set_xlim(0, 1150000); ax.set_ylim(-0.6, 2.9); ax.axis('off')
fig.text(0.05, 0.92, '10만엔을 원화로 사면', fontsize=28, fontproperties=B, color=INK)
fig.text(0.05, 0.86, '공항 영업점이 일반 영업점보다 2만 380원 더', fontsize=19, color=SUB)
fig.text(0.05, 0.03, '하나은행 2026.10.20 21시 고시(580회차) · 공항은 같은 날 21:28 공항환율 조회 · 우대 전 · 파이어맵 계산', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 연말 값
ye = {}
for d, v in r: ye[d[:4]] = v
pts = [('2007년 말', ye['2007']), ('2011년 말', ye['2011']), ('2015년 말', ye['2015']), ('2020년 말', ye['2020']), ('2025년 말', ye['2025']), ('2026.10.20', ys[-1])]
fig, ax = plt.subplots(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
for i, (n, v) in enumerate(pts):
    ax.bar(i, v, width=0.6, color=ORG if i in (0, 5) else NAVY)
    ax.text(i, v + 25, f'{v:,.0f}원', ha='center', fontsize=19, fontproperties=B, color=INK)
ax.set_xticks(range(len(pts))); ax.set_xticklabels([p[0] for p in pts], fontsize=15)
ax.set_ylim(0, 1750); ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.92, '100엔이 원화로 얼마였나(연말 값)', fontsize=26, fontproperties=B, color=INK)
fig.text(0.05, 0.86, '지금 값은 2007년 말과 거의 같아요', fontsize=18, color=SUB)
fig.text(0.05, 0.02, '한국은행 ECOS 731Y001 원/100엔 매매기준율 · 그해 마지막 영업일', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.1)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
