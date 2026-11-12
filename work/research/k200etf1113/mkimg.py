# k200etf1113 그림 2장 — 숫자는 calc_out.txt(야후 종가·삼성 분배 기록)
import os, json, datetime as dt
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, BLU, LG = '#EA580C', '#111827', '#4B5563', '#2563EB', '#CBD5E1'
# 01 KODEX 200 1년 종가 선 + 매달 산 점
d = json.load(open('raw/yh_069500.json', encoding='utf-8'))['chart']['result'][0]
ts = [dt.datetime.fromtimestamp(t).date() for t in d['timestamp']]; cl = d['indicators']['quote'][0]['close']
pts = [(t, p) for t, p in zip(ts, cl) if p and dt.date(2025, 11, 12) <= t <= dt.date(2026, 11, 12)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
ax.plot([t for t, _ in pts], [p / 10000 for _, p in pts], color=BLU, lw=2.4)
avg = 8.653
ax.axhline(avg, color=ORG, lw=1.6, ls='--')
ax.text(pts[0][0], 12.9, '주황 점선 = 매달 산 평균 가격 약 8만 6,530원', color=ORG, fontproperties=Bs(14))
ax.annotate('6월 22일 14만 8,355원', xy=(dt.date(2026, 6, 22), 14.8355), xytext=(dt.date(2026, 1, 20), 14.6), fontproperties=Bs(14), color=INK, arrowprops=dict(arrowstyle='->', color=SUB))
ax.annotate('11월 12일\n8만 4,240원', xy=(pts[-1][0], pts[-1][1] / 10000), xytext=(dt.date(2026, 8, 25), 5.9), fontproperties=Bs(14), color=INK, arrowprops=dict(arrowstyle='->', color=SUB))
ax.text(pts[0][0], 4.95, '2025년 11월 12일 5만 8,800원', fontproperties=Bs(12), color=SUB)
ax.set_ylabel('만원', color=SUB); ax.set_ylim(4.8, 16)
for s in ['top', 'right']: ax.spines[s].set_visible(False)
ax.set_title('KODEX 200 1년 종가', fontproperties=Bs(20), color=INK, loc='left', pad=14)
fig.text(0.01, 0.01, '자료: 야후 파이낸스 일별 종가(네이버페이 증권과 대조) · 파이어맵 계산', fontsize=10, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/01.png'); plt.close()
# 02 산 달별 50만원의 지금 값
rows = [('25년 11월', 72), ('12월', 71), ('26년 1월', 62), ('2월', 51), ('3월', 51), ('4월', 48), ('5월', 35), ('6월', 33), ('7월', 39), ('8월', 41), ('9월', 40), ('10월', 41)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, v) in enumerate(rows):
    c = BLU if v >= 50 else ORG
    ax.bar(i, v, color=c, width=0.62); ax.text(i, v + 1, f'{v}', ha='center', fontproperties=Bs(13), color=c)
ax.axhline(50, color=INK, lw=1.2); ax.text(11.4, 51.5, '넣은 돈 50만원', ha='right', fontproperties=Bs(12), color=INK)
ax.set_xticks(range(len(rows))); ax.set_xticklabels([n for n, _ in rows], fontsize=11, color=SUB)
ax.set_ylim(0, 82); ax.set_yticks([])
for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
ax.set_title('산 달마다 50만원이 지금 얼마(만원)', fontproperties=Bs(20), color=INK, loc='left', pad=14)
fig.text(0.01, 0.01, '2026년 11월 12일 종가 · 분배금 빼고 · 파란색=이익, 주황=손해', fontsize=10, color=SUB)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
