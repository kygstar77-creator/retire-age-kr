# rtcancel1022 그림 3장 — 숫자는 calc.py가 raw/(국토부 아파트 매매 실거래, 서울 25개 구, 2026-10-22 21:2x 받음)로 계산한 calc_out.txt 값
import os, json, glob, datetime as dt, collections
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def B(s): return fm.FontProperties(fname=F + r'\pd700.ttf', size=s)
ORG, NAVY, GRAY = '#EA580C', '#1E3A8A', '#9CA3AF'
os.makedirs('pkg/img', exist_ok=True)
SRC = '국토교통부 아파트 매매 실거래(서울 25개 구, 10월 22일 받음) · 파이어맵 계산'

# 계약월별 해제 비율 다시 셈(calc §2와 같은 식)
mon = collections.defaultdict(lambda: [0, 0])
for f in glob.glob('raw/*_trade.json'):
    for r in json.load(open(f, encoding='utf-8')):
        k = f"{r['dealYear']}-{int(r['dealMonth']):02d}"; mon[k][0] += 1; mon[k][1] += r['cdealType'] == 'O'

# 00 표지(차트): 1년 해제 1,933건이 어떻게 갈렸나 — 띠 하나 (calc_out §12·§9)
same, near, none = 1438, 1719 - 1438, 214
tot = same + near + none
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.86, '아파트 실거래가', fontproperties=B(66), color='#111827')
fig.text(0.06, 0.765, "'해제' 붙은 거래 1,933건", fontproperties=B(44), color='#374151')
fig.text(0.06, 0.62, '4건 중 3건은', fontproperties=B(56), color='#111827')
fig.text(0.06, 0.53, '계약일·가격 같은 재신고', fontproperties=B(52), color=ORG)
fig.text(0.06, 0.465, '서울 최근 1년 계약 · 같은 단지·면적·층', fontsize=18, color='#374151')
ax = fig.add_axes([0.06, 0.2, 0.88, 0.17])
x = 0
NL = chr(10)
for v, c, lab in [(same, ORG, f'계약일·가격 같은{NL}다시 신고 {same:,}'), (near, '#FDBA74', f'비슷한{NL}거래{NL}{near}'), (none, NAVY, f'다시 신고{NL}없음 {none}')]:
    ax.barh(0, v, left=x, color=c, edgecolor='white', lw=3)
    ax.text(x + v / 2, 0, lab, ha='center', va='center', color='white' if c != '#FDBA74' else '#7C2D12', fontproperties=B(20 if v > 500 else 14))
    x += v
ax.set_xlim(0, tot); ax.axis('off')
fig.text(0.06, 0.03, SRC + ' · 해제 아닌 거래끼리는 계약일·가격 같은 짝이 40건 중 1건꼴', fontsize=10, color='#6B7280')
fig.savefig('pkg/img/00.png', dpi=100); plt.close(fig)

# 01 계약월별 해제 비율 — 최근 두 달은 회색(해제가 더 붙을 수 있음)
ks = [k for k in sorted(mon) if k >= '2025-11']
fig, ax = plt.subplots(figsize=(9, 7.5), dpi=100); fig.patch.set_facecolor('white')
for i, k in enumerate(ks):
    t, c = mon[k]; p = c / t * 100
    col = GRAY if k >= '2026-09' else NAVY
    ax.bar(i, p, color=col, width=0.7)
    ax.text(i, p + 0.08, f'{p:.1f}', ha='center', fontsize=11.5, color='#111827')
NL = chr(10)
ax.set_xticks(range(len(ks))); ax.set_xticklabels([(k[2:4] + '년' + NL if k.endswith('-11') or k.endswith('-01') else NL) + k[5:].lstrip('0') + '월' for k in ks], fontsize=12)
ax.set_ylim(0, 5); ax.set_yticks([0, 1, 2, 3, 4, 5]); ax.set_yticklabels(['0%', '1%', '2%', '3%', '4%', '5%'], fontsize=12)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.grid(axis='y', color='#E5E7EB', lw=1); ax.set_axisbelow(True)
fig.text(0.05, 0.94, '서울 아파트 매매, 계약한 달별 해제 비율', fontproperties=B(22), color='#111827')
fig.text(0.05, 0.895, '2025년 11월~2026년 10월 계약 · 회색(9·10월)은 해제가 아직 덜 들어온 달', fontsize=14, color='#4B5563')
fig.text(0.05, 0.02, SRC + ' · 해제 건수 ÷ 그달 계약 신고 건수(%)', fontsize=10, color='#6B7280')
plt.subplots_adjust(left=0.09, right=0.97, top=0.85, bottom=0.15)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 계약 뒤 해제까지 걸린 날 — calc §3 (해제 3,595건, 2025.7~2026.10 계약)
parts = [('30일 안', 44.2), ('31~60일', 29.3), ('61~90일', 15.7), ('90일 넘어서', 10.8)]   # calc §11
fig, ax = plt.subplots(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
for i, (lab, p) in enumerate(parts):
    y = 3 - i
    ax.barh(y, p, color=ORG if i == 0 else NAVY, height=0.6)
    ax.text(-1, y, lab, ha='right', va='center', fontproperties=B(19), color='#111827')
    ax.text(p + 1, y, f'{p:.0f}%', va='center', fontproperties=B(19), color='#111827')
ax.set_xlim(-22, 60); ax.set_ylim(-0.6, 3.6); ax.axis('off')
fig.text(0.05, 0.92, '계약하고 해제되기까지 걸린 날', fontproperties=B(23), color='#111827')
fig.text(0.05, 0.875, '해제 1,933건(2025년 11월~2026년 10월 계약) · 계약일부터 해제일까지', fontsize=14, color='#4B5563')
fig.text(0.05, 0.03, SRC, fontsize=10, color='#6B7280')
plt.subplots_adjust(left=0.03, right=0.97, top=0.83, bottom=0.08)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok', {k: mon[k] for k in ks})
