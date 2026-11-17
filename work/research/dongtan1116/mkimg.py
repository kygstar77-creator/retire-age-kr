# dongtan1116 본문 그림 — 01 동탄구 아파트 매매 달별 건수(2025.01~2026.10), 02 같은 집 값 변화. 표지 00은 cafecover.py. 숫자는 calc_out·calc2_out 그대로
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, LBLUE, INK, SUBC, ORG, GRY = '#1D4ED8', '#93C5FD', '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = '국토교통부 아파트 매매 실거래 · 화성시 동탄구(11/17 받음, 취소 거래 뺌) · 파이어맵 계산'
ms = ['25.1','2','3','4','5','6','7','8','9','10','11','12','26.1','2','3','4','5','6','7','8','9','10']
n = [235,359,524,420,503,876,385,347,578,1043,1064,693,961,775,964,953,1256,1913,153,139,246,354]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
cols = [GRY]*17 + [ORG] + [BLUE]*4
bars = ax.bar(range(len(ms)), n, color=cols, width=0.7)
bars[-1].set_hatch('//'); bars[-1].set_alpha(0.6)
ax.text(17, 1913 + 40, '1,913건', ha='center', fontproperties=Bs(15), color=ORG)
for i in (18, 19, 20): ax.text(i, n[i] + 40, f'{n[i]}', ha='center', fontproperties=Bs(12), color=BLUE)
ax.axvline(17.5, color=INK, lw=1.2, ls='--')
ax.text(17.65, 1700, '7월 규제지역\n7월 5일 토지거래허가', fontproperties=Bs(12.5), color=INK, va='top')
ax.text(21, 353 + 40, '신고\n덜 들어옴', ha='center', fontsize=10.5, color=SUBC)
ax.set_xticks(range(len(ms))); ax.set_xticklabels(ms, fontsize=10.5)
ax.set_ylim(0, 2150); ax.set_yticks([0, 500, 1000, 1500, 2000]); ax.set_yticklabels(['0', '500', '1,000', '1,500', '2,000'], fontsize=11)
ax.grid(axis='y', color='#E5E7EB'); ax.set_axisbelow(True)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.93, '동탄구 아파트 매매, 달마다 몇 건', fontproperties=Bs(23), color=INK)
fig.text(0.04, 0.88, '6월에 몰렸다가 7월부터 한 달 200건 안팎으로', fontsize=13.5, color=SUBC)
fig.text(0.04, 0.025, SRC, fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.08, right=0.98)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 같은 집
lab = ['2026년 6월\n→ 9~11월', '2026년 1~6월\n→ 7~11월', '1년 전 7~11월\n→ 올해 7~11월']
v = [13.5, 22.4]; pairs = [231, 273]; lab = lab[:2]
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
ax.bar(range(2), v, color=[ORG, BLUE], width=0.5)
for i in range(2):
    ax.text(i, v[i] + 0.8, f'+{v[i]:g}%', ha='center', fontproperties=Bs(20), color=INK)
    ax.text(i, 1.2, f'{pairs[i]}곳', ha='center', fontproperties=Bs(12.5), color='white')
ax.set_xticks(range(2)); ax.set_xticklabels(lab, fontsize=13); ax.set_yticks([]); ax.set_ylim(0, 27)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.93, '같은 단지·같은 넓이 집, 규제 뒤 값은', fontproperties=Bs(22), color=INK)
fig.text(0.04, 0.88, '6월과 9~11월에 모두 팔린 231곳 중 95%가 더 비싸게 팔림', fontsize=13.5, color=SUBC)
fig.text(0.04, 0.025, SRC, fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.82, bottom=0.14, left=0.04, right=0.98)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
