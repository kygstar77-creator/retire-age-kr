# isacut1104 그림 2장 — 일반형 이익별 세금(3년 채움 vs 중도해지, calc.py 식), 퇴직 뒤 6개월 창(시행령 제93조의4⑭·제81조⑥3)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, GR = '#EA580C', '#111827', '#94A3B8'
def man(v): return f'약 {round(v/10000):,}만원'
# 01
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
rows = [(p, max(0, p-2_000_000)*0.099, p*0.154) for p in (3_000_000, 5_000_000, 10_000_000)]
mx = max(r[2] for r in rows)
for i, (p, a, b) in enumerate(rows):
    y = (len(rows)-1-i)*1.3
    ax.barh(y+0.25, a, color=GR, height=0.42); ax.barh(y-0.25, b, color=ORG, height=0.42)
    ax.text(a+mx*0.02, y+0.25, f'3년 채움 {man(a)}', va='center', fontsize=14, color=INK)
    ax.text(b+mx*0.02, y-0.25, f'중도해지 {man(b)}', va='center', fontproperties=Bs(14), color=ORG)
    ax.text(-mx*0.03, y, f'이익 {p//10000:,}만원', va='center', ha='right', fontproperties=Bs(16), color=INK)
ax.set_xlim(0, mx*1.7); ax.set_ylim(-0.8, 3.1); ax.axis('off')
fig.text(0.05, 0.9, 'ISA 일반형, 3년 전에 깨면 세금이 이만큼', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.03, '조세특례제한법 제91조의18 · 소득세법 제129조 · 지방세법 제103조의13 (2026년 11월 4일 확인) · 이익은 모두 이자·배당으로 가정', fontsize=10, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.2, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02
fig, ax = plt.subplots(figsize=(9, 4.6), dpi=100)
ax.barh(0, 6, left=0, color=ORG, height=0.5); ax.barh(0, 3, left=6, color=GR, height=0.5)
ax.text(3, 0, '이때 해지하면 예외\n(3년 채운 것처럼)', ha='center', va='center', fontproperties=Bs(17), color='white')
ax.text(7.5, 0, '보통 중도해지', ha='center', va='center', fontproperties=Bs(15), color=INK)
for x, t in ((0, '퇴직한 날'), (6, '6개월')):
    ax.plot([x, x], [-0.45, 0.45], color=INK, lw=2); ax.text(x, -0.62, t, ha='center', va='top', fontproperties=Bs(15), color=INK)
ax.set_xlim(-0.6, 9.3); ax.set_ylim(-1.2, 0.9); ax.axis('off')
fig.text(0.05, 0.86, '3년 전 ISA 해지, 퇴직 뒤 6개월이 갈림길', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.04, '조세특례제한법 시행령 제93조의4 ⑭·제81조 ⑥ 3호 (2026년 11월 4일 확인) · 특별해지사유신고서를 내야 적용', fontsize=10, color='#6B7280')
fig.subplots_adjust(top=0.78, bottom=0.12, left=0.04, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print(rows)
