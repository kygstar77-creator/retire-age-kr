# realdep1112 그림 2장 — 01 해마다 9월에 맡긴 1억, 이자 − 물건 값 오름(14번) 02 세 경우(5년 전·작년·지금)
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, LBLUE, INK, GR, SUBC, RED = '#1D4ED8', '#93C5FD', '#111827', '#CBD5E1', '#6B7280', '#DC2626'
d = json.load(open('raw/ecos_1112.json', encoding='utf-8')); dep1, cpi = d['dep1'], d['cpi']
P, T = 1e8, .846
ys, vals = [], []
for y in range(2012, 2026):
    a, b = f'{y}09', f'{y+1}09'
    vals.append((P*dep1[a]/100*T - P*(cpi[b]/cpi[a]-1)) / 1e4); ys.append(y)
# 01
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
cols = [BLUE if v >= 0 else RED for v in vals]
ax.bar(range(len(ys)), vals, color=cols, width=0.7)
ax.axhline(0, color=INK, lw=1)
for i, v in enumerate(vals):
    ax.text(i, v + (12 if v >= 0 else -12), f'{v:+.0f}', ha='center', va='bottom' if v >= 0 else 'top', fontsize=10.5, color=INK)
ax.set_xticks(range(len(ys))); ax.set_xticklabels([f"'{y%100:02d}" for y in ys], fontsize=12)
ax.set_ylim(-520, 300); ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.92, '9월에 1억 맡겨 1년 뒤, 이자에서 물건 값 오른 만큼 빼면', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.86, '단위 만원 · +는 남은 돈, −는 모자란 돈 · 빨간 막대 14번 중 6번', fontsize=15, color=SUBC)
fig.text(0.04, 0.025, "맡긴 해 9월 기준('12=2012년) · 한국은행 정기예금(1년) 신규취급 평균 금리, 세금 15.4% 뗌 · 소비자물가지수 9월→다음 해 9월", fontsize=9.5, color=SUBC)
fig.subplots_adjust(top=0.80, bottom=0.10, left=0.04, right=0.98)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02
cases = [('2021년 9월\n금리 1.31%', '202109', '202209'), ('2025년 9월\n금리 2.54%', '202509', '202609'), ('2026년 9월\n금리 3.57%\n(물가 2.82% 가정)', '202609', None)]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
for i, (lab, a, b) in enumerate(cases):
    it = P*dep1[a]/100*T/1e4
    pi = cpi[b]/cpi[a]-1 if b else cpi['202610']/cpi['202510']-1
    up = P*pi/1e4
    ax.bar(i - 0.18, it, width=0.34, color=BLUE); ax.bar(i + 0.18, up, width=0.34, color=GR)
    ax.text(i - 0.18, it + 8, f'{it:.0f}', ha='center', fontproperties=Bs(15), color=INK)
    ax.text(i + 0.18, up + 8, f'{up:.0f}', ha='center', fontproperties=Bs(15), color=INK)
    diff = it - up
    ax.text(i, -95, f'{abs(diff):.0f}만원 ' + ('남음' if diff >= 0 else '모자람'), ha='center', fontproperties=Bs(16), color=BLUE if diff >= 0 else RED)
ax.set_xticks(range(3)); ax.set_xticklabels([c[0] for c in cases], fontsize=13)
ax.tick_params(axis='x', pad=42, length=0)
ax.set_ylim(-130, 620); ax.set_yticks([])
for s in ('top', 'right', 'left', 'bottom'): ax.spines[s].set_visible(False)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=BLUE, label='세금 뗀 이자'), Patch(color=GR, label='1억어치 물건 값 오름')], frameon=False, fontsize=13, loc='upper right')
fig.text(0.04, 0.92, '1억 정기예금 1년, 이자와 물건 값 오름', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.86, '단위 만원 · 원금 1억은 어느 해든 그대로 돌려받아요', fontsize=15, color=SUBC)
fig.text(0.04, 0.025, '한국은행 정기예금(1년) 신규취급 평균 금리 · 소비자물가지수 · 2026년은 10월 물가 2.82%가 1년 이어진다는 가정', fontsize=9.5, color=SUBC)
fig.subplots_adjust(top=0.80, bottom=0.27, left=0.04, right=0.98)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print([round(v) for v in vals])
