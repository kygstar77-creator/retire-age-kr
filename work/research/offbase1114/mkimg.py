# offbase1114 그림 2장 — 숫자는 calc_out.txt(국세청 2026-11-12 보도참고자료 붙임 3)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, BLU, LG = '#EA580C', '#111827', '#4B5563', '#2563EB', '#94A3B8'
# 1) 2023년 고시 기준시가 1억원이 2027년 안에서 얼마인지(만원) — 지역별
rows = [('서울',10178),('대전',9492),('부산',9387),('전국',9388),('세종',9080),('울산',8996),('경기',8997),('전남광주',8745),('인천',8715),('대구',8040)]
rows.sort(key=lambda r: -r[1])
fig, ax = plt.subplots(figsize=(9, 6.2), dpi=100)
for i,(n,v) in enumerate(rows):
    c = ORG if n=='서울' else (BLU if n=='전국' else LG)
    ax.barh(i, v-7000, left=7000, color=c, height=0.62)
    ax.text(v+40, i, f'{v:,}만원', va='center', fontproperties=Bs(14), color=INK)
ax.axvline(10000, color=INK, lw=1.2, ls='--'); ax.text(10000, -0.9, '2023년 1억원', ha='center', fontproperties=Bs(12), color=INK)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([n for n,_ in rows], fontproperties=Bs(15), color=INK)
ax.invert_yaxis(); ax.set_xlim(7000, 10900); ax.set_xticks([])
for s in ['top','right','bottom']: ax.spines[s].set_visible(False)
ax.set_title('2023년에 기준시가 1억원이던 오피스텔, 2027년 안은?', fontproperties=Bs(19), color=INK, loc='left', pad=22)
fig.text(0.01, 0.01, '지역 전체 총액 변동률(2024~2027년 고시 4번)을 곱한 값 · 내 호실은 다를 수 있음 · 자료: 국세청 보도참고자료(2026.11.12) 붙임 3', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0,0.03,1,1)); plt.savefig('pkg/img/01.png'); plt.close()
# 2) 해마다 변동률 — 서울·전국·대구(2023~2027년 고시)
yrs=[2023,2024,2025,2026,2027]
S=[7.31,-2.67,1.34,1.10,2.07]; A=[6.06,-4.78,-0.31,-0.63,-0.47]; D=[-1.56,-7.90,-4.37,-3.62,-5.28]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for v,c,n in [(S,ORG,'서울'),(A,BLU,'전국'),(D,LG,'대구')]:
    ax.plot(range(5), v, color=c, lw=3, marker='o', ms=8, label=n)
    for i,x in enumerate(v):
        if n=='서울' and i==1: ax.text(i+0.1, x-0.3, f'{x:+.2f}%', ha='left', fontproperties=Bs(12), color=c)
        else: ax.text(i, x+(0.8 if n=='서울' else -1.5), f'{x:+.2f}%', ha='center', fontproperties=Bs(12), color=c)
ax.axhline(0, color=INK, lw=1)
ax.set_xticks(range(5)); ax.set_xticklabels([f'{y}년' for y in yrs], fontproperties=Bs(14), color=INK)
ax.set_yticks([]); ax.set_ylim(-10.5, 9.5)
for s in ['top','right','left']: ax.spines[s].set_visible(False)
ax.legend(prop=Bs(13), frameon=False, loc='lower left')
ax.set_title('오피스텔 기준시가 해마다 얼마나 바뀌었나', fontproperties=Bs(20), color=INK, loc='left', pad=14)
fig.text(0.01, 0.01, '시행 연도 기준(2027년은 안) · 전년 대비 총액 기준 · 자료: 국세청 보도참고자료(2026.11.12) 붙임 3', fontsize=9.5, color=SUB)
plt.tight_layout(rect=(0,0.03,1,1)); plt.savefig('pkg/img/02.png'); plt.close()
print('ok')
