# rechg1103 그림 2장 — 평균이익별 부담금(제12조), 3억 단지 1주택 보유 기간별(제14조의2) · 값은 calc.py
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from calc import charge, cut, M
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
SRC = '재건축초과이익 환수에 관한 법률 제12조·제14조의2 (국가법령정보센터, 2026년 11월 3일 확인) · 조합원 1인당 평균'
def won(v):
    v = round(v / M)
    if v >= 10000: return f'{v//10000}억 {v%10000:,}만원' if v % 10000 else f'{v//10000}억원'
    return f'{v:,}만원'
def bars(rows, title, out, note):
    fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
    mx = max(v for _, v, _ in rows)
    for i, (lab, v, t) in enumerate(rows):
        y = len(rows) - 1 - i
        ax.barh(y, max(v, mx * 0.01), color=ORG if i == len(rows) - 1 and 'hl' in note else (GR if i == 0 and 'first_gray' in note else ORG), height=0.55)
        ax.text(max(v, mx * 0.01) + mx * 0.02, y, t, va='center', fontproperties=Bs(16), color=INK)
        ax.text(-mx * 0.02, y, lab, va='center', ha='right', fontsize=16, color=INK)
    ax.set_xlim(0, mx * 1.75); ax.set_ylim(-0.6, len(rows) - 0.4); ax.axis('off')
    fig.text(0.05, 0.9, title, fontproperties=Bs(22), color=INK)
    fig.text(0.05, 0.03, SRC, fontsize=10.5, color='#6B7280')
    fig.subplots_adjust(top=0.84, bottom=0.1, left=0.24, right=0.97)
    fig.savefig(out, dpi=100); plt.close(fig)
r1 = []
for a in [1, 2, 3, 5]:
    c = charge(a * 10000 * M); r1.append((f'평균이익 {a}억', c, f'{won(c)} (이익의 {c/(a*10000*M)*100:.0f}%)'))
bars(r1, '부담금은 이익의 몇 %일까', 'pkg/img/01.png', '')
base = charge(3 * 10000 * M)
r2 = [('감경 없음', base, won(base))] + [(f'1주택 {y}년', base * (1 - cut(y)), f'{won(base*(1-cut(y)))} ({int(cut(y)*100)}% 감경)') for y in (6, 10, 15, 20)]
bars(r2, '평균이익 3억 단지, 한 집만 오래 가졌다면', 'pkg/img/02.png', 'first_gray')
print(r1, r2)
