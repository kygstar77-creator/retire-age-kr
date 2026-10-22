# bokrate1022 그림 3장 — 숫자는 한국은행 ECOS 722Y001(raw/ecos_base_daily.json)·calc.py·한국은행 보도자료(raw/bok_2610_press.txt)
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
ORG, INK, SUB, GR, NAVY = '#EA580C', '#111827', '#4B5563', '#94A3B8', '#1E3A8A'
r = json.load(open('raw/ecos_base_daily.json', encoding='utf-8'))
dt = lambda s: datetime.datetime.strptime(s, '%Y%m%d')
X = [dt(t) for t, v, _ in r] + [dt('20261022')]; Y = [float(v) for t, v, _ in r] + [3.0]  # 10/22 동결(보도자료)
# 00 표지 — 짙은 남색 바탕, 큰 글 두 줄 + 1999년 뒤 기준금리 계단
BG, WH, LG = '#14213D', '#FFFFFF', '#BFD3F2'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.875, '기준금리 3.00% 동결', fontsize=66, fontproperties=B, color=WH)
fig.text(0.06, 0.765, '쉰 뒤엔? 인상 14번·인하 6번', fontsize=60, fontproperties=B, color='#FB923C')
ax = fig.add_axes([0.08, 0.14, 0.86, 0.52]); ax.set_facecolor(BG)
ax.step(X, Y, where='post', color=LG, lw=2.6)
ax.plot([X[-1]], [3.0], 'o', ms=16, color='#FB923C')
ax.text(X[-1], 2.25, '오늘', ha='center', fontproperties=Bs(26), color='#FB923C')
ax.set_yticks([]); ax.set_xticks([dt('20000101'), dt('20080101'), dt('20160101'), dt('20240101')])
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y')); ax.tick_params(colors=WH, labelsize=22, length=0)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.spines['bottom'].set_color(LG)
fig.text(0.06, 0.03, '한국은행 경제통계시스템 기준금리 1999.5~2026.9 · 10/22 통화정책방향', fontsize=19, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 쉬어 간 20번 — 다시 올리기까지 걸린 달 / 내린 경우
res = [l for l in open('calc_out.txt', encoding='utf-8') if l.startswith('(datetime')]
import re
rows = []
for l in res:
    d = re.findall(r'date\((\d+), (\d+), (\d+)\)', l); k = '인상' if "'인상'" in l else '인하'; m = float(re.search(r"', ([\d.]+)\)", l).group(1))
    rows.append((datetime.date(*map(int, d[0])), k, m))
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)
for i, (d0, k, m) in enumerate(rows):
    y = len(rows) - i
    ax.barh(y, m, color=ORG if k == '인상' else GR, height=0.7)
    ax.text(-0.3, y, f'{d0.year}.{d0.month}', ha='right', va='center', fontsize=12, color=SUB)
    ax.text(m + 0.2, y, f'{m:.0f}개월 뒤 {"또 인상" if k == "인상" else "인하"}', va='center', fontsize=11, color=INK if k == '인상' else SUB, bbox=dict(fc='white', ec='none', pad=0.6), zorder=3)
ax.axvline(3, color=NAVY, lw=1.2, ls='--', zorder=1); ax.text(3.1, len(rows) + 0.9, '3개월', fontproperties=Bs(13), color=NAVY)
ax.set_xlim(-2.6, 26); ax.set_ylim(0.3, len(rows) + 1.4); ax.set_yticks([]); ax.set_xticks([0, 6, 12, 18, 24]); ax.tick_params(labelsize=12)
ax.set_xlabel('올린 뒤 다음 결정까지(개월)', fontsize=12, color=SUB)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.93, '올린 뒤 쉬어 간 20번, 그다음은?', fontsize=25, fontproperties=B, color=INK)
fig.text(0.05, 0.88, '주황 = 다시 올림 14번 · 회색 = 쉬다가 내림 6번', fontsize=16, color=SUB)
fig.text(0.05, 0.02, '한국은행 경제통계시스템 기준금리(2008.2까지 콜금리 목표) · 1999.5~2026.9 · 직접 집계', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.12)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 올해 기준금리 계단과 다음 회의
X2 = [x for x in X if x >= dt('20260101')]; Y2 = Y[-len(X2):]
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)
ax.step(X2 + [dt('20261126')], Y2 + [3.0], where='post', color=NAVY, lw=3)
for d, lab, y in [('20260716', '7/16 인상\n2.50→2.75%', 2.92), ('20260827', '8/27 인상\n2.75→3.00%', 3.17), ('20261022', '10/22 동결\n3.00%', 3.17)]:
    ax.plot([dt(d)], [2.75 if d == '20260716' else 3.0], 'o', ms=10, color=ORG)
    ax.text(dt(d), y, lab, ha='center', fontproperties=Bs(14), color=INK)
ax.axvline(dt('20261126'), color=GR, lw=1.4, ls='--'); ax.text(dt('20261126'), 2.42, '다음 회의\n11/26', ha='center', fontproperties=Bs(14), color=SUB)
ax.set_ylim(2.3, 3.45); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.2f}%'))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m월')); ax.tick_params(labelsize=13)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.93, '올해 두 번 올리고, 오늘 처음 쉬었어요', fontsize=25, fontproperties=B, color=INK)
fig.text(0.05, 0.88, '결정문: 물가·경기·금융안정 점검하며 추가 인상 시기·속도 결정', fontsize=16, color=SUB)
fig.text(0.05, 0.02, '한국은행 경제통계시스템 기준금리 · 보도자료 「통화정책방향」 2026.10.22 · 회의 일정', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.1)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
