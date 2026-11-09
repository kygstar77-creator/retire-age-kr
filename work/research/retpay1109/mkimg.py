# retpay1109 그림 2장 — 01 퇴직 나이에 따라 갈리는 길(퇴직급여법 제9조·시행령 제3조의2·고시 2026-65·소득세법 시행령 제40조의2), 02 퇴직금 1억 근속별 세금(calc.py)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR, LG = '#EA580C', '#111827', '#4B5563', '#94A3B8', '#E5E7EB'
# 01 길
fig = plt.figure(figsize=(9, 6.6), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.9, '퇴직할 때 나이에 따라 갈리는 길', fontproperties=Bs(23), color=INK)
def box(x, y, w, h, t, c, tc=INK, fs=15):
    fig.patches.append(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.008,rounding_size=0.02', transform=fig.transFigure, fc=c, ec='none'))
    fig.text(x + w/2, y + h/2, t, ha='center', va='center', fontproperties=Bs(fs), color=tc, linespacing=1.4)
box(0.05, 0.66, 0.4, 0.13, '55세 전에 퇴직', ORG, 'white', 18)
box(0.55, 0.66, 0.4, 0.13, '55세 넘어 퇴직\n(또는 300만원 이하)', INK, 'white', 16)
box(0.05, 0.43, 0.4, 0.15, '퇴직금이 IRP로 들어옴', LG)
box(0.55, 0.43, 0.4, 0.15, '바로 현금으로 받거나\nIRP로 받기 중 고름', LG)
box(0.03, 0.17, 0.2, 0.18, '해지해서\n한 번에\n(감면 없음)', '#FDE7D7', fs=14)
box(0.25, 0.17, 0.22, 0.18, '55세 뒤\n연금으로\n(30~50% 감면)', '#FDE7D7', fs=14)
box(0.55, 0.17, 0.4, 0.18, '현금 = 퇴직소득세 전부\nIRP 연금 = 30~50% 감면\n(60일 안에 넣으면 환급 신청)', '#FDE7D7', fs=14)
for x in (0.25, 0.75): fig.text(x, 0.605, '▼', ha='center', fontsize=14, color=GR)
fig.text(0.13, 0.365, '▼', ha='center', fontsize=12, color=GR); fig.text(0.36, 0.365, '▼', ha='center', fontsize=12, color=GR); fig.text(0.75, 0.365, '▼', ha='center', fontsize=12, color=GR)
fig.text(0.05, 0.05, '퇴직급여법 제9조·시행령 제3조의2 · 고용노동부고시 제2026-65호 · 소득세법 제129조·제146조', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 세금
rows = [('근속 10년', 4262500, 2983750), ('근속 20년', 1232000, 862400), ('근속 30년', 264000, 184800)]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
y = np.arange(3)[::-1]; h = 0.36
ax.barh(y + h/2, [r[1] for r in rows], h, color=GR, label='일시금으로 받을 때')
ax.barh(y - h/2, [r[2] for r in rows], h, color=ORG, label='연금으로 받을 때 (처음 10년)')
def man(v): return f'약 {round(v/10000):,}만원'
for yi, r in zip(y, rows):
    ax.text(r[1] + 60000, yi + h/2, man(r[1]), va='center', fontsize=14, color=INK)
    ax.text(r[2] + 60000, yi - h/2, man(r[2]), va='center', fontsize=14, color=ORG)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontproperties=Bs(16)); ax.set_xticks([]); ax.set_xlim(0, 5600000)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=14, loc='lower right')
fig.text(0.05, 0.92, '퇴직금 1억원, 내는 퇴직소득세', fontproperties=Bs(23), color=INK)
fig.text(0.05, 0.02, '지방소득세 포함 · 소득세법 제48조·제55조·제129조로 계산(홈택스 모의계산과 같은 방식)', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.16, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
