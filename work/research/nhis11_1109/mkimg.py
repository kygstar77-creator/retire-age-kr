# nhis11_1109 그림 2장 — 근거 research.md 대조 칸(시행령 제41조③·제41조의2, 법 제78조)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, LG, BL = '#EA580C', '#111827', '#4B5563', '#CBD5E1', '#2563EB'

# 01 2026년 달마다 쓰는 소득 자료
fig = plt.figure(figsize=(9, 6.2), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.88, '2026년 보험료, 어느 해 소득으로 매기나', fontproperties=Bs(23), color=INK)
ax = fig.add_axes([0.06, 0.24, 0.9, 0.56]); ax.set_xlim(0, 12); ax.set_ylim(0, 4); ax.axis('off')
for m in range(12):
    ax.text(m + 0.5, 3.6, f'{m+1}월', ha='center', fontsize=13, color=SUB)
rows = [(2.4, '이자·배당·사업', [(0, 10, '2024년 소득', LG, INK), (10, 12, '2025년', ORG, 'white')]),
        (0.9, '연금', [(0, 12, '2025년 소득', BL, 'white')])]
for y, lab, segs in rows:
    for a, b, txt, c, tc in segs:
        ax.add_patch(FancyBboxPatch((a + 0.06, y), b - a - 0.12, 0.9, boxstyle='round,pad=0,rounding_size=0.15', color=c))
        ax.text((a + b) / 2, y + 0.45, txt, ha='center', va='center', fontproperties=Bs(16), color=tc)
fig.text(0.06, 0.82, '이자·배당·사업소득', fontproperties=Bs(14), color=SUB)
fig.text(0.06, 0.555, '연금소득', fontproperties=Bs(14), color=SUB)
fig.text(0.06, 0.13, '11월분부터 바뀌는 건 연금을 뺀 나머지 소득', fontproperties=Bs(18), color=ORG)
fig.text(0.06, 0.04, '국민건강보험법 시행령 제41조③ (2026.11.9 국가법령정보센터)', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 조정 신청 흐름
fig = plt.figure(figsize=(9, 6.2), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.88, '올해 소득이 줄었다면, 이 순서로', fontproperties=Bs(23), color=INK)
steps = [('① 서류 준비', '폐업·퇴직처럼 사유를 보여 주는 서류'),
         ('② 공단에 조정 신청', '11월분 납부 기한 12월 10일'),
         ('③ 남은 달은 지금 소득으로', '조정된 보험료를 냄'),
         ('④ 나중에 그해 소득으로 정산', '덜 냈으면 최대 12회로 나눠 냄 · 더 냈으면 돌려줌')]
for i, (a, b) in enumerate(steps):
    y = 0.70 - i * 0.165
    c = ORG if i == 3 else INK
    fig.patches.append(FancyBboxPatch((0.06, y), 0.88, 0.13, boxstyle='round,pad=0,rounding_size=0.02', transform=fig.transFigure, color='#F3F4F6'))
    fig.text(0.09, y + 0.075, a, fontproperties=Bs(18), color=c, va='center')
    fig.text(0.09, y + 0.028, b, fontsize=13, color=SUB, va='center')
fig.text(0.06, 0.04, '국민건강보험법 제78조 · 시행령 제41조의2 ①②④⑤⑥⑦ (2026.11.9 국가법령정보센터)', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
