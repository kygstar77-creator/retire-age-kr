# fxdepfee1026 그림 3장 — 숫자는 calc.py(KB 2026-10-26 15:18 고시·USD 12개월(12개월이상~18개월미만) 연 3.60740%·이자 세금 15.4%) 결과
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
# 00 표지 — 숯색 바탕(최근 10장에 남색·파랑 3장), 주제어 크게 + 우대율별 본전 환율 막대
BG, WH, LG = '#262626', '#FFFFFF', '#D6D3D1'
be = [('우대 0%', 1309.6), ('우대 50%', 1297.0), ('우대 90%', 1287.0), ('수수료 없을 때', 1284.5)]
NOW = 1323.7
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.865, '달러예금 환전수수료', fontproperties=Bs(76), color=WH)
fig.text(0.06, 0.765, '우대 없으면 1%만 내려도 손해', fontproperties=Bs(54), color='#FB923C')
fig.text(0.06, 0.695, '막대 = 손해 없이 버티는 환율 하락 폭 (높을수록 여유)', fontsize=30, color=LG)
ax = fig.add_axes([0.06, 0.13, 0.88, 0.5]); ax.set_facecolor(BG)
for i, (lab, v) in enumerate(be):
    d = (NOW - v) / NOW * 100
    c = '#FB923C' if i == 0 else LG
    ax.bar(i, d, color=c, width=0.62)
    ax.text(i, d + 0.12, f'{d:.1f}%', ha='center', fontproperties=Bs(34 if i == 0 else 30), color=c)
    ax.text(i, -0.12, lab, ha='center', va='top', fontsize=24, color=WH)
    ax.text(i, -0.5, f'{int(v + 0.5):,}원 아래면 손해', ha='center', va='top', fontsize=19, color=LG)
ax.set_ylim(-1.1, 3.8); ax.set_xlim(-0.6, 3.6); ax.axis('off')
fig.text(0.06, 0.035, '10/26 KB 1,323.7원 기준 · 12개월 연 3.61% · 세금 15.4% 뗀 뒤', fontsize=24, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 원화로 넣고 찾을 때 쓰는 환율
fig = plt.figure(figsize=(9, 6.6), dpi=100); fig.patch.set_facecolor('#FFFFFF')
fig.text(0.05, 0.9, '원화로 넣고 찾을 때 쓰는 환율', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.84, 'KB국민은행 2026년 10월 26일 15시 18분 고시(달러)', fontsize=15, color=SUB)
rows = [('넣을 때(송금 보낼 때)', '1,336.5원', ORG), ('매매기준율(은행 기준 환율)', '1,323.7원', INK), ('찾을 때(송금 받을 때)', '1,310.9원', ORG)]
for i, (a, b, c) in enumerate(rows):
    y = 0.66 - i * 0.18
    fig.text(0.08, y, a, fontsize=20, color=SUB)
    fig.text(0.92, y, b, fontproperties=Bs(28), color=c, ha='right')
fig.text(0.08, 0.17, '같은 날 바로 넣었다 찾으면 1억이 약 192만원 줄어요(우대 없을 때)', fontproperties=Bs(16), color=INK)
fig.text(0.05, 0.02, 'KB국민은행 환율조회 · 씨티·하나은행 외화예금 상품설명서(원화 입금 전신환 매도율, 지급 매입율)', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 환율이 그대로일 때 1년 뒤 늘어난 돈
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
rows = [('수수료 없을 때', 305.2), ('우대 90%', 285.3), ('우대 50%', 206.0), ('우대 0%', 107.8)]
for i, (lab, v) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.barh(y, v, color=ORG if lab == '우대 0%' else GR, height=0.6)
    ax.text(v + 4, y, f'약 {v:,.0f}만원', va='center', fontproperties=Bs(18), color=INK)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=16)
ax.set_xticks([]); ax.set_xlim(0, 380)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.92, '환율이 그대로면 1억이 1년 뒤 얼마 늘까', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.865, '이자는 같아도 환전 우대에 따라 늘어난 돈이 크게 갈림', fontsize=15, color=SUB)
fig.text(0.05, 0.02, 'KB 10/26 고시·12개월 연 3.61% · 세금 15.4% · 직접 계산', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.08, left=0.22)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
