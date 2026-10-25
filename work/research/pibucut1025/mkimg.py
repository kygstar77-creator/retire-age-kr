# pibucut1025 그림 3장 — 숫자는 calc.py(시행규칙 부칙 제907호 제3조 감액 구간·시행령 44조 7.19%·시행규칙 44조 연금 50%) 결과
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
P = 71900
pay = [('80% 감액|22.9~23.10', P*0.2), ('60% 감액|23.11~24.10', P*0.4), ('40% 감액|24.11~25.10', P*0.6), ('20% 감액|25.11~26.8', P*0.8), ('감액 끝|26.9~', P)]
pay = [(a.replace('|', chr(10)), b) for a, b in pay]
won = lambda v: (f'{int(v)//10000}만 {int(v)%10000:,}원' if v >= 10000 else f'{int(v):,}원')
# 00 표지 — 짙은 자줏빛 바탕(최근 10장에 녹색 2장), 주제어 크게 + 낸 돈 계단 막대
BG, WH, LG = '#4A1626', '#FFFFFF', '#F3D3DC'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.865, '피부양자 탈락 건보료', fontproperties=Bs(76), color=WH)
fig.text(0.06, 0.765, '경감(감액) 8월분으로 끝', fontproperties=Bs(54), color='#FB923C')
fig.text(0.06, 0.695, '공적연금 2,400만원 · 구간마다 낸 한 달 보험료(올해 율)', fontsize=28, color=LG)
ax = fig.add_axes([0.06, 0.13, 0.88, 0.5]); ax.set_facecolor(BG)
for i, (lab, v) in enumerate(pay):
    c = '#FB923C' if i == 4 else LG
    ax.bar(i, v, color=c, width=0.62)
    ax.text(i, v + 1800, won(v), ha='center', fontproperties=Bs(25 if i == 4 else 22), color=c)
    ax.text(i, -2500, lab, ha='center', va='top', fontsize=20, color=WH, linespacing=1.4)
ax.set_ylim(-16000, 86000); ax.set_xlim(-0.6, 4.6); ax.axis('off')
fig.text(0.06, 0.035, '시행규칙 부칙 제907호 · 재산 보험료 없을 때 · 장기요양 별도', fontsize=24, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 탈락한 달에 따라 감액 받은 기간
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
rows = [('2022년 9월 탈락', 48), ('2023년 12월 탈락', 33), ('2024년 12월 탈락', 21), ('2025년 12월 탈락', 9), ('앞으로 새로 탈락', 0)]
for i, (lab, n) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.barh(y, n, color=ORG if n else GR, height=0.6)
    ax.text(n + 0.8, y, f'{n}개월' if n else '0개월(감액 없음)', va='center', fontproperties=Bs(17), color=INK)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=15)
ax.set_xticks([]); ax.set_xlim(0, 62)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.92, '탈락한 달에 따라 감액 받은 기간', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.865, '감액률이 달력 구간(80·60·40·20%)으로 정해져 늦게 떨어질수록 짧음', fontsize=15, color=SUB)
fig.text(0.05, 0.02, '국민건강보험법 시행규칙 부칙 제907호 제3조 · 직접 계산', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.08, left=0.25)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 월 7만 1,900원이 나오는 순서
fig = plt.figure(figsize=(9, 6.6), dpi=100); fig.patch.set_facecolor('#FFFFFF')
fig.text(0.05, 0.9, '공적연금 2,400만원이면 월 보험료는', fontproperties=Bs(22), color=INK)
steps = [('1년 공적연금', '2,400만원'), ('보험료 매길 때 절반만', '1,200만원'), ('12로 나눈 소득월액', '100만원'), ('보험료율 7.19% 곱함', '월 7만 1,900원')]
for i, (a, b) in enumerate(steps):
    y = 0.72 - i * 0.16
    fig.text(0.08, y, a, fontsize=19, color=SUB)
    fig.text(0.92, y, b, fontproperties=Bs(26 if i == 3 else 22), color=ORG if i == 3 else INK, ha='right')
    if i < 3: fig.text(0.5, y - 0.085, '↓', fontsize=20, color=GR, ha='center')
fig.text(0.05, 0.08, '재산에 붙는 보험료가 없는 경우 · 장기요양보험료는 별도', fontsize=14, color=SUB)
fig.text(0.05, 0.02, '국민건강보험법 제71조 · 시행령 제44조 · 시행규칙 제44조', fontsize=12, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
