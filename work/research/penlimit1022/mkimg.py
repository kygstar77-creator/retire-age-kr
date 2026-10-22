# penlimit1022 그림 3장 — 숫자는 calc.py(소득세법 시행령 40조의2 ③3 연금수령한도 식) 결과
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
X = 3e8
def path(s):
    R = X; out = []
    for k in range(s, 11):
        lim = R / (11 - k) * 1.2; t = min(lim, R); out.append((k, lim, t, R)); R -= t
    return out
man = lambda v: f'{v/1e4:,.0f}만원'
# 00 표지 — 짙은 갈색 바탕, 주제어 줄 크게 + 첫해 한도 막대 둘
BG, WH, LG = '#3A2614', '#FFFFFF', '#F5D9B8'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.865, '연금수령한도', fontproperties=Bs(84), color=WH)
fig.text(0.06, 0.765, '연차는 안 받아도 늘어나요', fontproperties=Bs(56), color='#FB923C')
fig.text(0.06, 0.695, '받는 돈·세율은 그대로, 1년 상한만 커짐 · 3억원 계좌', fontsize=28, color=LG)
ax = fig.add_axes([0.14, 0.15, 0.72, 0.47]); ax.set_facecolor(BG)
vals = [(path(1)[0][1], '받을 수 있게 된 해\n(1년차)', LG), (path(6)[0][1], '5년 뒤 시작\n(6년차)', '#FB923C')]
for i, (v, lab, c) in enumerate(vals):
    ax.bar(i, v / 1e4, color=c, width=0.55)
    ax.text(i, v / 1e4 + 250, man(v), ha='center', fontproperties=Bs(40), color=c)
    ax.text(i, -500, lab, ha='center', va='top', fontsize=24, color=WH)
ax.set_ylim(-1900, 9000); ax.set_xlim(-0.6, 1.6); ax.axis('off')
fig.text(0.06, 0.035, '단, 퇴직금 세금 감면은 실제로 받은 해만 셈 · 수익 0% 가정', fontsize=26, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 연차별 첫해 한도(3억)
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ks = list(range(1, 11)); lims = [X / (11 - k) * 1.2 / 1e4 for k in ks]
ax.bar(ks, lims, color=[ORG if k in (1, 6) else GR for k in ks], width=0.7)
for k, v in zip(ks, lims):
    ax.text(k, v + 400, f'{v:,.0f}', ha='center', fontsize=12 if v < 30000 else 12, color=INK)
ax.set_xticks(ks); ax.set_xticklabels([f'{k}년차' for k in ks], fontsize=12); ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.set_ylim(0, 40000)
fig.text(0.05, 0.92, '3억원이 그대로 있을 때 연차별 1년 한도(만원)', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.865, '평가액 ÷ (11 − 연차) × 1.2 · 한도가 계좌보다 크면 다 꺼낼 수 있다는 뜻 · 11년차부터 한도 없음', fontsize=15, color=SUB)
fig.text(0.05, 0.02, '소득세법 시행령 제40조의2 · 직접 계산', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.1)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 해마다 한도만큼 꺼낼 때 남은 돈
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
for s, c, lab in ((1, ORG, '1년차부터 시작'), (6, INK, '6년차부터 시작')):
    p = path(s); xs = [i for i in range(len(p) + 1)]; ys = [r / 1e4 for _, _, _, r in p] + [0]
    ax.plot(xs, ys, marker='o', color=c, lw=3, label=lab)
    ax.text(xs[-1] - 0.1 if s == 6 else xs[-1], 1300 if s == 6 else 4500, f'{len(p)}년 만에 0원', color=c, ha='center' if s == 1 else 'left', fontproperties=Bs(15))
ax.set_xticks(range(0, 11)); ax.set_xticklabels([f'{i}' for i in range(0, 11)], fontsize=12)
ax.set_xlabel('꺼내기 시작한 뒤 몇 년', fontsize=13, color=SUB); ax.set_ylabel('연초 남은 돈(만원)', fontsize=13, color=SUB)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:,.0f}')); ax.set_ylim(0, 32000); ax.legend(fontsize=14, frameon=False)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.92, '3억원 계좌에서 해마다 한도만큼 꺼내면', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.865, '수익 0% 가정 · 수익이 붙어도 마지막 해에 다 꺼낼 수 있음', fontsize=15, color=SUB)
fig.text(0.05, 0.02, '소득세법 시행령 제40조의2 연금수령한도 식 · 직접 계산', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.14)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
