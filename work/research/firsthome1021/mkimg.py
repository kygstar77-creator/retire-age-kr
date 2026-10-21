# firsthome1021 그림 3장 — 숫자는 calc.py(지방세법 11조·지특법 36조의3·행안부 개편안 8/26)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR, NAVY = '#EA580C', '#111827', '#4B5563', '#CBD5E1', '#1E3A8A'
P = ['2억', '3억', '4억', '6억', '9억', '12억']
TAX = [200, 300, 400, 600, 2700, 3600]          # 만원, 본세
NOW = [max(0, t - 200) for t in TAX]
# 00 표지 — 짙은 자주 바탕, 큰 글 두 줄 + 집값별 낼 돈 막대(감면 몫 주황)
BG, WH, LG = '#2A1530', '#FFFFFF', '#D8C3DD'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.875, '생애최초 취득세 감면', fontsize=64, fontproperties=B, color=WH)
fig.text(0.06, 0.765, '6억 집 본세 400만원', fontsize=70, fontproperties=B, color='#FB923C')
fig.text(0.06, 0.715, '빠지는 돈은 200만원으로 같아서, 비싼 집일수록 효과가 작아요', fontsize=24, color=LG)
ax = fig.add_axes([0.08, 0.19, 0.86, 0.47]); ax.set_facecolor(BG)
x = range(len(P))
ax.bar(x, NOW, color='#9F7AA8', width=0.62)
ax.bar(x, [t - n for t, n in zip(TAX, NOW)], bottom=NOW, color='#FB923C', width=0.62)
for i, n in enumerate(NOW):
    ax.text(i, TAX[i] + 60, f'{n:,}만' if n else '0원', ha='center', fontproperties=Bs(26), color=WH)
ax.set_xticks(list(x)); ax.set_xticklabels(P, fontproperties=Bs(28), color=WH)
ax.set_yticks([]); ax.set_ylim(0, 4100)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.spines['bottom'].set_color(LG); ax.tick_params(length=0)
fig.text(0.06, 0.08, '■ 감면 200만원', fontsize=22, fontproperties=B, color='#FB923C')
fig.text(0.32, 0.08, '■ 감면 뒤 내는 취득세(본세)', fontsize=22, fontproperties=B, color='#C9A7D1')
fig.text(0.06, 0.025, '지방세법 제11조 · 지방세특례제한법 제36조의3 · 2026.10.21 기준 직접 계산', fontsize=18, color=LG)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 표 — 집값 · 지금 · 40세 미만 개편안(3칸)
rows = [('2억원', '0원', '0원'), ('3억원', '100만원', '0원'), ('4억원', '200만원', '100만원'), ('6억원', '400만원', '300만원'),
        ('7억 5천만원', '1,300만원', '1,200만원'), ('9억원', '2,500만원', '2,400만원'), ('12억원', '3,400만원', '3,300만원'), ('12억 100만원', '3,603만원', '3,603만원')]
fig = plt.figure(figsize=(9, 8.6), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.93, '집값별 생애최초 감면 뒤 내는 취득세', fontsize=26, fontproperties=B, color=INK)
fig.text(0.05, 0.885, '본세 기준 · *개편안은 국회 통과 전, 아직 적용 안 돼요', fontsize=17, color=SUB)
hy = 0.81; cols = [0.07, 0.45, 0.72]
for c, h in zip(cols, ['집값', '지금(200만원)', '40세 미만 개편안*']):
    fig.text(c, hy, h, fontsize=19, fontproperties=B, color=NAVY)
fig.add_artist(plt.Line2D([0.05, 0.95], [hy - 0.02, hy - 0.02], color=INK, lw=1.5))
for i, (a, b, c) in enumerate(rows):
    y = hy - 0.09 - i * 0.083
    hl = a in ('6억원', '12억 100만원')
    fig.text(cols[0], y, a, fontsize=21, fontproperties=B if hl else None, color=INK)
    fig.text(cols[1], y, b, fontsize=21, fontproperties=B, color=ORG if hl else INK)
    fig.text(cols[2], y, c, fontsize=21, color=SUB)
    fig.add_artist(plt.Line2D([0.05, 0.95], [y - 0.025, y - 0.025], color=GR, lw=0.8))
fig.text(0.05, 0.03, '지방세법 제11조 · 지방세특례제한법 제36조의3 · 행정안전부 2026년 지방세제 개편안(8.26)', fontsize=12.5, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 바뀐 것 — 추징 조건 전·후(글자 카드)
fig = plt.figure(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('#F8FAFC')
fig.text(0.05, 0.9, '감면 뒤 추징(다시 걷는) 경우', fontsize=27, fontproperties=B, color=INK)
fig.text(0.05, 0.845, '2026년 1월 1일부터 바뀐 것', fontsize=17, color=SUB)
L = [('3개월 안에 안 들어가 살면', '이제 추징 안 함', '#16A34A'), ('3개월 안에 집을 더 사면', '이제 추징 안 함', '#16A34A'),
     ('3년 안에 팔거나 증여하면', '지금도 추징', ORG), ('3년 안에 전세·월세를 주면', '지금도 추징', ORG)]
for i, (a, b, c) in enumerate(L):
    y = 0.68 - i * 0.14
    fig.text(0.07, y, a, fontsize=22, color=INK)
    fig.text(0.95, y, b, ha='right', fontsize=24, fontproperties=B, color=c)
    fig.add_artist(plt.Line2D([0.05, 0.95], [y - 0.045, y - 0.045], color=GR, lw=0.8))
fig.text(0.05, 0.06, '배우자에게 지분을 넘기는 건 추징하지 않아요', fontsize=17, fontproperties=B, color=NAVY)
fig.text(0.05, 0.02, '지방세특례제한법 제36조의3 제4항 · 부칙(법률 제21309호) 제5조', fontsize=12.5, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
