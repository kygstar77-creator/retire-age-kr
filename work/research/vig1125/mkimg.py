# vig1125 그림 — 00 표지(10년 전 산 값 대비 지금 배당 VIG 4.6%·VYM 5.4%), 01 1주당 연 배당 2015~2025, 02 1만 달러 10년 결과. 숫자는 calc_out.txt·raw 그대로
import os, json, datetime as D
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, NAVY, GRY = '#111827', '#6B7280', '#EA580C', '#1E3A5F', '#94A3B8'
SRC = '야후 파이낸스 일별 종가·배당 기록(11/23 받음) · 뱅가드 배당 기록 대조 · 파이어맵 계산'
def ann(t):
    r = json.load(open(f'raw/{t}.json'))['chart']['result'][0]; a = {}
    for k, v in r['events']['dividends'].items():
        y = D.datetime.utcfromtimestamp(int(k)).year; a[y] = a.get(y, 0) + v['amount']
    return a
BG = '#14532D'; TOPIC_PX, NUM_PX = 58, 44
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, 'VIG 배당, 11년 뒤', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.785, '2015년 11월에 산 값 대비 지금 1년 배당', fontproperties=Bs(27), color='#BBF7D0')
ax = fig.add_axes([0.1, 0.17, 0.8, 0.55]); ax.set_facecolor(BG)
vals = [(2.3, 4.6), (3.2, 5.4)]
for i, (a, b) in enumerate(vals):
    ax.bar(i * 1.2 - 0.22, a, 0.4, color=GRY); ax.bar(i * 1.2 + 0.22, b, 0.4, color=ORG if i == 0 else '#FDBA74')
    ax.text(i * 1.2 - 0.22, a + 0.1, f'{a}%', ha='center', fontproperties=Bs(24), color='white')
    ax.text(i * 1.2 + 0.22, b + 0.1, f'{b}%', ha='center', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i * 1.2, -0.25, ['VIG(배당성장)', 'VYM(고배당)'][i], ha='center', va='top', fontproperties=Bs(24), color='white')
ax.text(-0.42, 6.3, '회색: 2015년 배당률   주황: 그때 산 사람이 지금 받는 배당률', fontproperties=Bs(17), color='#BBF7D0')
ax.set_ylim(-1.2, 6.8); ax.set_xlim(-0.6, 1.8); ax.axis('off')
fig.text(0.07, 0.045, '달러 기준 · 세전 · 2026.11.20 종가', fontsize=17, color='#BBF7D0')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API VIG·VYM 일별 종가·배당 events(11/23 받음)로 직접 계산, calc_out.txt',
           'made_at': '2026-11-23', 'by': 'research/vig1125/mkimg.py', 'out': 'img/00.png', 'topic': 'VIG 배당, 11년 뒤', 'num': '4.6%·5.4%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 4 jeunkim/224480264482 차트형 표지 + 경쟁 1 campcodemoney 상품명 큰 글자'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK); fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
v, y = ann('VIG'), ann('VYM'); yrs = list(range(2015, 2026))
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.plot(yrs, [v[k] for k in yrs], color=ORG, lw=3.5, marker='o'); ax.plot(yrs, [y[k] for k in yrs], color=NAVY, lw=3.5, marker='o')
for s, c, nm, dy in [(v, ORG, 'VIG', 0.12), (y, NAVY, 'VYM', -0.25)]:
    ax.text(2015, s[2015] + (0.12 if nm == 'VYM' else -0.28), f'{s[2015]:.2f}', ha='center', fontproperties=Bs(14), color=c)
    ax.text(2025.15, s[2025] + dy, f'{nm} {s[2025]:.2f}달러', fontproperties=Bs(15), color=c)
ax.set_xticks(yrs); ax.set_xticklabels([str(k)[2:] + '년' for k in yrs], fontproperties=Bs(12)); ax.set_yticks([])
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.set_xlim(2014.6, 2027.3); ax.set_ylim(1.4, 4.1)
frame(fig, '1주당 1년 배당(달러) — VIG 약 2배, VYM 약 1.6배', '해마다 받은 배당 합 · 2015년 → 2025년')
fig.subplots_adjust(top=0.83, bottom=0.1, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); x = np.arange(2)
dv, ev = [3703, 4865], [29857, 22575]
ax.bar(x, ev, 0.5, color=[ORG, NAVY]); ax.bar(x, dv, 0.5, bottom=ev, color=GRY)
for i in range(2):
    ax.text(i, ev[i] / 2, f'평가액\n{ev[i]:,}달러', ha='center', va='center', fontproperties=Bs(17), color='white')
    ax.text(i, ev[i] + dv[i] + 500, f'받은 배당 {dv[i]:,}달러', ha='center', fontproperties=Bs(15), color=INK)
ax.axhline(10000, color=INK, lw=1.5, ls='--'); ax.text(1.32, 10300, '넣은 돈\n1만 달러', fontproperties=Bs(13), color=INK)
ax.set_xticks(x); ax.set_xticklabels(['VIG', 'VYM'], fontproperties=Bs(18)); ax.tick_params(axis='x', length=0); ax.set_yticks([])
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.set_xlim(-0.6, 1.7); ax.set_ylim(0, 37000)
frame(fig, '11년 전 1만 달러 — 지금 평가액 + 받은 배당', '2015.11.20 → 2026.11.20 · 배당은 다시 안 삼 · 세전')
fig.subplots_adjust(top=0.83, bottom=0.13, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
