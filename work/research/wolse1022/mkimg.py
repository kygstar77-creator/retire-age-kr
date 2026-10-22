# wolse1022 그림 3장 — 숫자는 calc2.py(국토부 아파트 전월세 실거래, 서울 25개 구, 1~8월 계약)
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
# 00 표지 — 남색 바탕 큰 글 두 줄 + 작년·올해 월세 비중(전체·새 계약·갱신)
BG, WH, LG = '#13243F', '#FFFFFF', '#C7D2E3'
G = ['전체', '새 계약', '갱신 계약']; A = [43.7, 46.6, 37.5]; Z = [50.7, 56.5, 44.5]
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.875, '서울 아파트 월세 비중', fontsize=66, fontproperties=B, color=WH)
fig.text(0.06, 0.765, '갱신 계약은 44.5%', fontsize=72, fontproperties=B, color='#FB923C')
fig.text(0.06, 0.715, '1~8월 계약 중 월세가 붙은 비율 · 작년 같은 기간과 비교', fontsize=24, color=LG)
ax = fig.add_axes([0.08, 0.17, 0.86, 0.47]); ax.set_facecolor(BG)
x = range(3); w = 0.36
ax.bar([i - w/2 for i in x], A, w, color='#5B6F94'); ax.bar([i + w/2 for i in x], Z, w, color='#FB923C')
for i in x:
    ax.text(i - w/2, A[i] + 1, f'{A[i]}%', ha='center', fontproperties=Bs(24), color=LG)
    ax.text(i + w/2, Z[i] + 1, f'{Z[i]}%', ha='center', fontproperties=Bs(27), color=WH)
ax.set_xticks(list(x)); ax.set_xticklabels(G, fontproperties=Bs(28), color=WH)
ax.set_yticks([]); ax.set_ylim(20, 62)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.spines['bottom'].set_color(LG); ax.tick_params(length=0)
fig.text(0.06, 0.08, '■ 2025년 1~8월', fontsize=22, fontproperties=B, color='#93A3C4')
fig.text(0.33, 0.08, '■ 2026년 1~8월', fontsize=22, fontproperties=B, color='#FB923C')
fig.text(0.06, 0.025, '국토교통부 아파트 전월세 실거래 15만 7,536건(2026) · 2026.10.22 직접 계산', fontsize=17, color=LG)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 구별 — 높은 다섯·낮은 셋(3칸)
rows = [('종로구', '65.3%', '54.9%'), ('중랑구', '62.2%', '49.0%'), ('구로구', '61.6%', '52.8%'), ('중구', '59.4%', '52.8%'), ('용산구', '57.3%', '45.3%'),
        ('…', '', ''), ('도봉구', '44.2%', '35.7%'), ('성북구', '44.0%', '40.5%'), ('양천구', '41.9%', '35.5%')]
fig = plt.figure(figsize=(9, 8), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.93, '구별 아파트 월세 비중(1~8월 계약)', fontsize=26, fontproperties=B, color=INK)
fig.text(0.05, 0.885, '25개 구 중 높은 다섯 곳과 낮은 세 곳 · 금천구만 작년보다 줄어', fontsize=17, color=SUB)
hy = 0.8; cs = [0.07, 0.45, 0.72]
for c, h in zip(cs, ['구', '2026년', '2025년']):
    fig.text(c, hy, h, fontsize=19, fontproperties=B, color=NAVY)
fig.add_artist(plt.Line2D([0.05, 0.95], [hy - 0.02, hy - 0.02], color=INK, lw=1.5))
for i, (a, b, c) in enumerate(rows):
    y = hy - 0.085 - i * 0.078
    fig.text(cs[0], y, a, fontsize=21, color=INK)
    fig.text(cs[1], y, b, fontsize=21, fontproperties=B, color=ORG if i < 5 else INK)
    fig.text(cs[2], y, c, fontsize=21, color=SUB)
    if a != '…': fig.add_artist(plt.Line2D([0.05, 0.95], [y - 0.025, y - 0.025], color=GR, lw=0.8))
fig.text(0.05, 0.03, '국토교통부 아파트 전월세 실거래(RTMSDataSvcAptRent) · 월세 0원 넘는 계약 비율 · 직접 계산', fontsize=12.5, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 갱신 계약 — 전세가 월세로 바뀐 비율(글자 카드)
fig = plt.figure(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('#F8FAFC')
fig.text(0.05, 0.9, '갱신할 때 전세가 월세로 바뀐 집은?', fontsize=27, fontproperties=B, color=INK)
fig.text(0.05, 0.845, '2026년 1~8월 갱신 계약 · 이전 조건이 적힌 계약 기준', fontsize=17, color=SUB)
L = [('이전에 전세였던 4만 1,942건 중 월세가 붙은 비율', '7.3%', ORG), ('작년 같은 기간', '6.2%', SUB),
     ('이전에 월세였던 2만 8,850건 중 전세로 돌아간 비율', '1.6%', NAVY), ('작년 같은 기간', '3.0%', SUB)]
for i, (a, b, c) in enumerate(L):
    y = 0.70 - i * 0.13
    fig.text(0.07, y, a, fontsize=19 if c != SUB else 18, color=INK if c != SUB else SUB)
    fig.text(0.95, y, b, ha='right', fontsize=28 if c != SUB else 22, fontproperties=B, color=c)
    if i % 2: fig.add_artist(plt.Line2D([0.05, 0.95], [y - 0.05, y - 0.05], color=GR, lw=0.8))
fig.text(0.05, 0.13, '전세였다가 월세가 붙은 집의 월세 중간값은 23만원', fontsize=19, fontproperties=B, color=NAVY)
fig.text(0.05, 0.03, '국토교통부 아파트 전월세 실거래 · 종전 보증금·월세 칸 기준 · 직접 계산', fontsize=12.5, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
