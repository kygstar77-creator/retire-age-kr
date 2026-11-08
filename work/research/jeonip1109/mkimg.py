# jeonip1109 그림 2장 — 숫자는 research.md 대조 칸(주택임대차보호법 제3조·부동산등기법 제6조·시행령 제10조·제11조·2023 부칙)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Ellipse
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR, LG = '#EA580C', '#111827', '#4B5563', '#94A3B8', '#CBD5E1'

# 01 이사 당일 시간선
fig = plt.figure(figsize=(9, 6.2), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.88, '이사 당일, 누가 먼저일까', fontproperties=Bs(24), color=INK)
ax = fig.add_axes([0.06, 0.22, 0.88, 0.56]); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
ax.plot([0.4, 9.6], [3, 3], color=LG, lw=6, solid_capstyle='round')
ax.text(0.4, 2.2, '이사 당일', fontproperties=Bs(15), color=SUB)
ax.text(8.8, 2.2, '다음 날 0시', ha='center', fontproperties=Bs(15), color=SUB)
pts = [(2.6, '전입신고', '대항력은 아직 없음', GR, 4.4),
       (5.4, '근저당 등기 접수', '접수한 때 바로 효력', ORG, 1.2),
       (8.8, '세입자 대항력', '이때부터 생김', INK, 4.4)]
for x, a, b, c, y in pts:
    ax.add_patch(Ellipse((x, 3), 0.42, 0.42 * 10 / 6 * 0.56 / 0.88 * 6.2 / 9 * 1.6, color=c))
    ax.text(x, y + 0.25, a, ha='center', fontproperties=Bs(17), color=c)
    ax.text(x, y - 0.45, b, ha='center', fontsize=13.5, color=SUB)
fig.text(0.06, 0.12, '같은 날 잡힌 근저당이 세입자보다 앞선다', fontproperties=Bs(17), color=ORG)
fig.text(0.06, 0.04, '주택임대차보호법 제3조① · 부동산등기법 제6조② (2026.11.8 국가법령정보센터)', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 근저당 날짜로 갈리는 최우선변제 (서울 보증금 1억6천만원)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labels = ['근저당 2023.2.21 이후', '근저당 2021.5.11~2023.2.20']
vals = [5500, 0]
ax.barh([1, 0], vals, color=[ORG, LG], height=0.5)
ax.text(5500 + 120, 1, '5,500만원까지', va='center', fontproperties=Bs(20), color=ORG)
ax.text(120, 0, '0원 (기준 1억5천만원 넘음)', va='center', fontproperties=Bs(18), color=SUB)
ax.set_yticks([1, 0]); ax.set_yticklabels(labels, fontproperties=Bs(15)); ax.set_xticks([]); ax.set_xlim(0, 9000); ax.set_ylim(-0.6, 1.6)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.9, '서울 보증금 1억6천만원, 근저당보다 먼저 받는 돈', fontproperties=Bs(21), color=INK)
fig.text(0.05, 0.83, '지금 기준 1억6,500만원 이하 → 5,500만원 · 예전 기준 1억5천만원 이하 → 5천만원', fontsize=12.5, color=SUB)
fig.text(0.05, 0.08, '0원이어도 확정일자에 따른 우선변제는 남음(앞선 근저당 뒤 순서) · 집값 절반 한도', fontsize=12, color=SUB)
fig.text(0.05, 0.02, '주택임대차보호법 시행령 제10조·제11조, 대통령령 제33254호 부칙 제2조, 제31673호(2021.5.11)', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.76, bottom=0.17, left=0.33, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
