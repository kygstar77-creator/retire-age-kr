# bunrinhis1111 그림 2장 — 근거 research.md 대조 칸(시행규칙 제44조①, 시행령 제44조①, 기사 S7·S8)
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
ORG, INK, SUB, LG = '#EA580C', '#111827', '#4B5563', '#CBD5E1'

# 01 1천만원 문턱 — 지역가입자 이자 몫 월 보험료
fig = plt.figure(figsize=(9, 6.2), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.88, '이자·배당 1천만원을 넘는 순간', fontproperties=Bs(23), color=INK)
fig.text(0.06, 0.82, '지역가입자, 이자 몫 한 달 보험료(7.19%)', fontsize=14, color=SUB)
ax = fig.add_axes([0.10, 0.20, 0.84, 0.54])
xs = ['1천만원', '1천만원 조금 넘음', '1,200만원']; ys = [0, 59917, 71900]; cs = [LG, ORG, ORG]
b = ax.bar(xs, ys, color=cs, width=0.55)
for i, v in enumerate(ys):
    ax.text(i, v + 2000, '0원' if v == 0 else ('약 6만원' if i == 1 else '7만 1,900원'), ha='center', fontproperties=Bs(18), color=INK)
ax.set_ylim(0, 85000); ax.set_yticks([]); [s.set_visible(False) for s in ax.spines.values()]
ax.tick_params(axis='x', labelsize=14, colors=INK, length=0)
fig.text(0.06, 0.09, '넘으면 넘은 부분이 아니라 전부가 들어가요', fontproperties=Bs(18), color=ORG)
fig.text(0.06, 0.03, '국민건강보험법 시행규칙 제44조①·시행령 제44조① (2026.11.11 국가법령정보센터) · 파이어맵 계산', fontsize=10.5, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 지금 붙는 분리과세 / 안 붙는 분리과세
fig = plt.figure(figsize=(9, 6.2), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.88, '분리과세 소득, 지금 건보료는', fontproperties=Bs(23), color=INK)
cols = [(0.06, '붙어요', ORG, ['이자·배당 합계 1천만원 초과\n(초과하면 전부)', '분리과세 주택임대소득']),
        (0.52, '안 붙어요', INK, ['연금저축·IRP 사적연금\n연 1,500만원 이하', '일용근로 소득', '건당 300만원 이하\n강연료·원고료', 'ISA 비과세 한도 넘은 수익'])]
for x, head, c, items in cols:
    fig.patches.append(FancyBboxPatch((x, 0.13), 0.42, 0.66, boxstyle='round,pad=0,rounding_size=0.02', transform=fig.transFigure, color='#F3F4F6'))
    fig.text(x + 0.03, 0.73, head, fontproperties=Bs(21), color=c, va='center')
    y = 0.63
    for t in items:
        fig.text(x + 0.03, y, '· ' + t, fontsize=14, color=INK, va='top', linespacing=1.3)
        y -= 0.055 * (t.count(chr(10)) + 1) + 0.045
fig.text(0.06, 0.07, '안 붙는 쪽 부과는 공단이 국회에 보고만 · 복지부 "결정된 바 없음"(11.4)', fontsize=13, color=ORG)
fig.text(0.06, 0.02, '시행규칙 제44조① · 보건복지부 보도설명자료 2026.11.4 · 스페셜타임스 11.4·이코노미스트 11.6', fontsize=10.5, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
