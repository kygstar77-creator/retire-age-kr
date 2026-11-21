# qqqi1123 그림 — 00 표지(차트: 34번 분배금 막대 + 전날 종가×1.17% 선), 01 2025년 2~6월 분배금, 02 1만 달러 세 ETF. 숫자는 calc_out.txt·calc2_out.txt 그대로
import os, json, re, datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, GRAY, NAVY = '#111827', '#6B7280', '#EA580C', '#9CA3AF', '#1E3A5F'
TOPIC_PX, NUM_PX = 56, 46
s = open('neos_qqqi_1121.txt', encoding='utf-8').read()
rows = re.findall(r"(\d\d/\d\d/\d{4}) (\d\d/\d\d/\d{4}) (\d\d/\d\d/\d{4}) (\d\d/\d\d/\d{4}) \$(\d\.\d{4})", s)
neos = dict(sorted({datetime.datetime.strptime(r[1], "%m/%d/%Y").date(): float(r[4]) for r in rows}.items()))
r = json.load(open('yahoo_QQQI_1121.json'))['chart']['result'][0]
ds = [datetime.date.fromtimestamp(x) for x in r['timestamp']]; c = r['indicators']['quote'][0]['close']
D = list(neos); V = [neos[d] for d in D]; P = [c[ds.index(d) - 1] for d in D]
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(NAVY)
fig.text(0.07, 0.86, 'QQQI 분배금', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.775, '34번 모두 전날 주가의 1.14~1.25%', fontproperties=Bs(30), color='#BFDBFE')
ax = fig.add_axes([0.07, 0.22, 0.86, 0.48]); ax.set_facecolor(NAVY)
x = np.arange(len(D))
ax.bar(x, V, color=[ORG if i == len(D) - 1 else '#94A3B8' for i in x], width=0.62)
ax.plot(x, [p * 0.0117 for p in P], color='white', lw=2.4)
ax.annotate('11월 0.58달러', xy=(len(D) - 1, V[-1] + 0.003), xytext=(len(D) - 4, 0.725), ha='center', fontproperties=Bs(22), color='white', arrowprops=dict(arrowstyle='-', color='white', lw=1.5))
ax.text(10, 0.725, '흰 선 = 전날 종가 × 1.17%', ha='center', fontproperties=Bs(20), color='white')
ax.text(0, 0.43, '2024년 2월', ha='left', fontproperties=Bs(18), color='#BFDBFE')
ax.text(len(D) - 1, 0.43, '2026년 11월', ha='right', fontproperties=Bs(18), color='#BFDBFE')
ax.set_ylim(0.45, 0.76); ax.set_xlim(-0.8, len(D) - 0.2); ax.axis('off')
fig.text(0.07, 0.115, '주가가 8.5% 내리자 분배금도 8% 줄었어요', fontproperties=Bs(NUM_PX - 16), color='white')
fig.text(0.07, 0.05, 'NEOS 분배 기록 · 야후 파이낸스 종가 · 파이어맵 계산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': 'NEOS QQQI 분배 기록 34번(neosfunds.com/qqqi, 11/21) × 야후 파이낸스 분배락 전날 종가 — 파이어맵 직접 계산(calc2_out.txt)',
           'made_at': '2026-11-21', 'by': 'research/qqqi1123/mkimg.py', 'out': 'img/00.png', 'topic': 'QQQI 분배금', 'num': '1.14~1.25% · 0.58달러 · 8.5%·8%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 7 poslee777/224483985591·경쟁 3 hyjoyer/224482587016 첫 그림 = 분배금 숫자 정리 그림 → 분배금 막대 차트 위 큰 숫자'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub, src):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, src, fontsize=10, color=SUBC)
# 01 2025년 2~6월
L = ['2월', '3월', '4월', '5월', '6월']; v = [0.6138, 0.5867, 0.5309, 0.6374, 0.6282]; p = [52.40, 50.40, 45.32, 50.91, 51.99]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); fig.subplots_adjust(top=0.80, bottom=0.12, left=0.06, right=0.97)
xx = np.arange(5)
ax.bar(xx, v, color=[ORG if i == 2 else NAVY for i in xx], width=0.55)
for i in xx:
    ax.text(i, v[i] + 0.006, f'{v[i]:.4f}달러', ha='center', fontproperties=Bs(15), color=INK)
    ax.text(i, 0.455, f'전날 종가\n{p[i]:.2f}달러', ha='center', va='bottom', fontsize=12.5, color='white')
ax.set_xticks(xx); ax.set_xticklabels(L, fontproperties=Bs(16)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); [q.set_visible(False) for q in ax.spines.values()]; ax.set_ylim(0.45, 0.68)
frame(fig, '2025년 4월, 분배금 9.5% 줄었다가 5월에 돌아옴', 'QQQI 1주당 분배금 · 2025년 2~6월 분배락', 'NEOS QQQI 분배 기록(11/21 확인) · 야후 파이낸스 종가')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 1만 달러
N = ['QQQ', 'QQQI', 'JEPQ']; st_ = [14306, 9146, 9784]; dv = [187, 4238, 3346]; tot = [14493, 13384, 13131]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); fig.subplots_adjust(top=0.80, bottom=0.10, left=0.06, right=0.97)
xx = np.arange(3)
ax.bar(xx, st_, color=NAVY, width=0.5, label='남은 주식 값')
ax.bar(xx, dv, bottom=st_, color=ORG, width=0.5, label='현금으로 받은 분배금')
ax.axhline(10000, color=GRAY, lw=1.5, ls='--'); ax.text(0.5, 10200, '넣은 돈 1만 달러', ha='center', fontsize=12.5, color=SUBC)
for i in xx:
    ax.text(i, st_[i] + dv[i] + 200, f'{tot[i]:,}달러', ha='center', fontproperties=Bs(16), color=INK)
    ax.text(i, st_[i] / 2, f'주식\n{st_[i]:,}', ha='center', va='center', fontsize=13, color='white')
ax.set_xticks(xx); ax.set_xticklabels(N, fontproperties=Bs(17)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); [q.set_visible(False) for q in ax.spines.values()]; ax.set_ylim(0, 17500)
ax.legend(prop=Bs(13), frameon=False, loc='upper center', ncol=2)
frame(fig, '2024년 1월 30일에 1만 달러씩 넣었다면', '2026년 11월 20일 종가 · 분배금은 현금으로 받음 · 세금·환율 뺌', '야후 파이낸스 종가·분배 기록(11/21 받음) · 파이어맵 계산')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
