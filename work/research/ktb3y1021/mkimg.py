# ktb3y1021 그림 3장 — 숫자는 한국은행 ECOS(raw/ecos_1021.json)·calc.py
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
k3 = {a: float(b) for a, b, c in e['ktb3']}; base = {a: float(b) for a, b, c in e['base']}
base['20261020'] = 3.0; base['20261021'] = 3.0  # 8/27 뒤 바뀐 적 없음, ECOS 일별 미반영 이틀
D = sorted(d for d in k3 if d in base and d >= '20080307')
X = [datetime.datetime.strptime(d, '%Y%m%d') for d in D]
SP = [k3[d] - base[d] for d in D]
dt = lambda s: datetime.datetime.strptime(s, '%Y%m%d')
# 00 표지 — 짙은 자주 바탕, 큰 글 두 줄 + 2008년 뒤 차이 선
BG, WH, LG = '#2A1630', '#FFFFFF', '#D8B4E2'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.875, '국고채 3년 3.82%', fontsize=66, fontproperties=B, color=WH)
fig.text(0.06, 0.765, '기준금리보다 0.82%p 위', fontsize=66, fontproperties=B, color='#FB923C')
ax = fig.add_axes([0.08, 0.14, 0.86, 0.52]); ax.set_facecolor(BG)
ax.fill_between(X, SP, 0.8, where=[s >= 0.8 for s in SP], color='#FB923C', alpha=0.45, lw=0)
ax.plot(X, SP, color=LG, lw=2.2)
ax.axhline(0.8, color='#FB923C', lw=2, ls='--'); ax.axhline(0, color=LG, lw=1, alpha=0.6)
ax.text(X[0], 0.86, '0.8%p', fontproperties=Bs(26), color='#FB923C')
ax.set_yticks([]); ax.set_xticks([dt('20080701'), dt('20140101'), dt('20200101'), dt('20260101')])
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y')); ax.tick_params(colors=WH, labelsize=22, length=0)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.spines['bottom'].set_color(LG)
fig.text(0.06, 0.03, '한국은행 경제통계시스템 · 국고채 3년 − 기준금리, 2008.3.7~2026.10.21', fontsize=19, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 18년 차이 + 인상 횟수
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)
ax.plot(X, SP, color='#1E3A8A', lw=1.6)
ax.fill_between(X, SP, 0.8, where=[s >= 0.8 for s in SP], color=ORG, alpha=0.5, lw=0)
ax.axhline(0.8, color=ORG, lw=1.6, ls='--'); ax.axhline(0, color=GR, lw=1)
for x, y, t in [('20080401', -0.3, '2008~09 초\n금리 내림'), ('20100801', 2.85, '2010.7~\n인상 5번'), ('20160901', 1.55, '2017.11\n인상 전후'), ('20210301', 2.35, '2021~23\n인상 10번'), ('20250201', 1.85, '2026\n인상 2번')]:
    ax.text(dt(x), y, t, fontproperties=Bs(14), color=ORG if '인상' in t else SUB, va='top')
ax.set_ylim(-1, 3.0); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:+.1f}%p' if v else '0'))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y')); ax.tick_params(labelsize=13)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.93, '국고채 3년이 기준금리보다 얼마나 높았나', fontsize=25, fontproperties=B, color=INK)
fig.text(0.05, 0.88, '주황 = 0.8%p 넘게 벌어진 때 · 올리던 때가 많았지만 내리던 때도 있었어요', fontsize=16, color=SUB)
fig.text(0.05, 0.02, '한국은행 경제통계시스템 시장금리(일별)·기준금리 · 2008.3.7~2026.10.21 영업일 4,609일', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.1)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 올해 국고채 3년과 기준금리, 인상한 날
D2 = [d for d in D if d >= '20260101']; X2 = [dt(d) for d in D2]
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)
ax.plot(X2, [k3[d] for d in D2], color=ORG, lw=3, label='국고채 3년')
ax.step(X2, [base[d] for d in D2], where='post', color='#1E3A8A', lw=2.4, label='기준금리')
for d0, d1, lab, dy in [('20260715', '20260716', '7/16 인상\n3.87→3.85%', 0.28), ('20260826', '20260827', '8/27 인상\n3.82→3.76%', -0.55)]:
    ax.annotate(lab, (dt(d1), k3[d1]), xytext=(dt(d1) - datetime.timedelta(days=75), k3[d1] + dy), fontproperties=Bs(14), color=INK, arrowprops=dict(arrowstyle='->', color=SUB))
ax.text(X2[-1], k3[D2[-1]] - 0.2, '10/21 3.82%', ha='right', fontproperties=Bs(15), color=ORG)
ax.legend(prop=Bs(15), loc='lower right', frameon=False)
ax.set_ylim(2.3, 4.3); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.1f}%'))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m월')); ax.tick_params(labelsize=13)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.93, '올해 국고채 3년은 인상 전에 먼저 올랐어요', fontsize=25, fontproperties=B, color=INK)
fig.text(0.05, 0.88, '두 번 올린 날 모두 국고채 3년 금리는 하루 전보다 내렸어요', fontsize=16, color=SUB)
fig.text(0.05, 0.02, '한국은행 경제통계시스템 · 2026.1.2~10.21 · 기준금리 10/20·21은 8/27 값 3.0%', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.1)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
