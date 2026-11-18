# loanfee1119 그림 2장 — 숫자는 calc_out.txt(은행연합회 가계대출금리 비교공시, 신규취급액 기준 평균 가산금리 2026.6·2026.10)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, BLU, LG = '#EA580C', '#111827', '#4B5563', '#2563EB', '#CBD5E1'
d = [(-0.38,'카카오뱅크'),(-0.22,'전북은행'),(-0.20,'신한은행'),(-0.11,'IBK기업은행'),(-0.11,'NH농협은행'),(-0.09,'우리은행'),(-0.07,'하나은행'),(-0.01,'SC제일은행'),(0.01,'KB국민은행'),(0.06,'광주은행'),(0.13,'케이뱅크'),(0.32,'BNK부산은행'),(0.37,'iM뱅크'),(0.41,'제주은행'),(0.47,'Sh수협은행'),(0.75,'BNK경남은행')]
fig, ax = plt.subplots(figsize=(9, 8.2), dpi=100)
for i,(v,n) in enumerate(d):
    y = len(d)-1-i; c = BLU if v < 0 else ORG
    ax.barh(y, v, color=c, height=0.62)
    ax.text(-0.02 if v >= 0 else 0.02, y, n, va='center', ha='right' if v >= 0 else 'left', fontproperties=Bs(13), color=INK)
    ax.text(v + (0.015 if v >= 0 else -0.015), y, f'{v:+.2f}', va='center', ha='left' if v >= 0 else 'right', fontproperties=Bs(12), color=c)
ax.axvline(0, color=SUB, lw=1)
ax.set_xlim(-0.75, 0.95); ax.set_yticks([]); ax.set_xticks([])
for s in ['top','right','left','bottom']: ax.spines[s].set_visible(False)
fig.suptitle('주택담보대출 가산금리, 내린 곳 8 · 올린 곳 8', fontproperties=Bs(23), color=INK, x=0.04, ha='left', y=0.965)
fig.text(0.04, 0.885, '6월 → 10월 변화(%p) · 파랑 = 내림, 주황 = 올림', fontproperties=Bs(14), color=SUB)
fig.text(0.04, 0.02, '은행연합회 가계대출금리 비교공시 · 분할상환 주택담보대출 · 신규취급액 기준 평균 가산금리', fontproperties=Bs(11), color=SUB)
plt.subplots_adjust(left=0.04, right=0.97, top=0.86, bottom=0.06)
fig.savefig('pkg/img/01.png'); plt.close(fig)
rows = [('주택담보대출\n(16곳)', 8, 8), ('일반신용대출\n(17곳)', 4, 13)]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i,(n,dn,up) in enumerate(rows):
    y = 1-i
    ax.barh(y, dn, color=BLU, height=0.5); ax.barh(y, up, left=dn, color=ORG, height=0.5)
    ax.text(dn/2, y, f'내림 {dn}곳', ha='center', va='center', fontproperties=Bs(17), color='white')
    ax.text(dn+up/2, y, f'올림 {up}곳', ha='center', va='center', fontproperties=Bs(17), color='white')
ax.set_yticks([1,0]); ax.set_yticklabels([r[0] for r in rows], fontproperties=Bs(15), color=INK)
ax.set_xlim(0, 17); ax.set_xticks([])
for s in ['top','right','bottom']: ax.spines[s].set_visible(False)
ax.spines['left'].set_color(LG)
fig.suptitle('7월 법 시행 뒤, 가산금리 내린 은행 수', fontproperties=Bs(23), color=INK, x=0.04, ha='left', y=0.95)
fig.text(0.04, 0.03, '2026년 6월 → 10월 · 은행연합회 가계대출금리 비교공시(신규취급액 기준 평균 가산금리)', fontproperties=Bs(11), color=SUB)
plt.subplots_adjust(left=0.2, right=0.96, top=0.82, bottom=0.12)
fig.savefig('pkg/img/02.png'); plt.close(fig)
print('ok')
