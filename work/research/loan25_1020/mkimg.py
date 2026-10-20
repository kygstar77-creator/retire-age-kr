# loan25_1020 그림 3장 — 숫자는 calc_out.json(국토부 실거래 2026-07~10, 2026-10-20 받음)
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
D = json.load(open('calc_out.json', encoding='utf-8')); G = D['gu']; T = D['total']
ORG, NAVY, GRAY, LG = '#EA580C', '#1E3A8A', '#94A3B8', '#CBD5E1'
by = sorted(G, key=lambda o: -(o['over25'] / o['n']))
top = by[:10]
# 00 표지 — 막대 5곳 + 큰 글
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.86, '서울 84㎡ 25억 넘는 거래', fontsize=56, fontproperties=B, color="#111827")
fig.text(0.05, 0.74, f"전체 {T['a']/T['n']*100:.1f}% · 강남 64%", fontsize=62, fontproperties=B, color=ORG)
fig.text(0.05, 0.68, '구별 비율 · 2026년 7~10월 계약 4,324건', fontsize=20, color='#374151')
ax = fig.add_axes([0.2, 0.08, 0.72, 0.54])
five = top[:5][::-1]
for i, o in enumerate(five):
    p = o['over25'] / o['n'] * 100
    ax.barh(i, p, height=0.62, color=ORG if i == 4 else NAVY)
    ax.text(p + 1.5, i, f"{p:.0f}%", va='center', fontsize=26, fontproperties=B, color='#111827')
    ax.text(-2, i, o['name'], ha='right', va='center', fontsize=24, fontproperties=B, color='#111827')
ax.set_xlim(0, 80); ax.axis('off')
fig.text(0.05, 0.02, '국토교통부 실거래(10월 20일 받음) · 25억 초과 = 주담대 한도 2억원 구간 · 파이어맵', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/00.png', dpi=100); fig.savefig('pkg/cover_100.png', dpi=11); plt.close(fig)
# 01 25억 넘는 비율 10곳
fig, ax = plt.subplots(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
for i, o in enumerate(top[::-1]):
    p = o['over25'] / o['n'] * 100
    ax.barh(i, p, height=0.62, color=ORG if p >= 40 else NAVY)
    ax.text(p + 1, i + 0.12, f"{p:.0f}%", va='center', fontsize=17, fontproperties=B, color='#111827')
    ax.text(p + 1, i - 0.22, f"{o['n']}건 중 {o['over25']}건", va='center', fontsize=12, color='#4B5563')
    ax.text(-1, i, o['name'], ha='right', va='center', fontsize=17, fontproperties=B, color='#111827')
ax.set_xlim(0, 78); ax.set_ylim(-0.6, 9.6); ax.axis('off')
fig.text(0.04, 0.95, '25억원 넘는 84㎡ 거래 비율', fontsize=24, fontproperties=B, color='#111827')
fig.text(0.04, 0.91, '25개 구 중 10곳만 있음 · 나머지 15개 구는 0건 · 2026년 7~10월 계약', fontsize=13, color='#4B5563')
fig.text(0.04, 0.03, '국토교통부 아파트 매매 실거래(2026-10-20 받음, 계약 해제 뺌) · 84㎡대 = 전용 80~86㎡', fontsize=11, color='#6B7280')
plt.subplots_adjust(left=0.2, right=0.97, top=0.88, bottom=0.07)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 25개 구 가격 구간 100% 막대
order = sorted(G, key=lambda o: (-(o['over25'] / o['n']), -(o['mid'] / o['n'])))
fig, ax = plt.subplots(figsize=(9, 10.5), dpi=100); fig.patch.set_facecolor('white')
for i, o in enumerate(order[::-1]):
    a, b, c = (o['over25'] / o['n'] * 100, o['mid'] / o['n'] * 100, o['low'] / o['n'] * 100)
    ax.barh(i, c, color=LG, height=0.72); ax.barh(i, b, left=c, color=NAVY, height=0.72); ax.barh(i, a, left=c + b, color=ORG, height=0.72)
    ax.text(-1, i, o['name'], ha='right', va='center', fontsize=13, fontproperties=B, color='#111827')
    if a >= 6: ax.text(c + b + a / 2, i, f"{a:.0f}", ha='center', va='center', fontsize=11, color='white', fontproperties=B)
    if b >= 8: ax.text(c + b / 2, i, f"{b:.0f}", ha='center', va='center', fontsize=11, color='white', fontproperties=B)
    if c >= 8: ax.text(c / 2, i, f"{c:.0f}", ha='center', va='center', fontsize=11, color='#111827')
ax.set_xlim(0, 100); ax.set_ylim(-0.6, 24.6); ax.axis('off')
fig.text(0.04, 0.955, '구별 84㎡ 거래 가격 구간(%)', fontsize=24, fontproperties=B, color='#111827')
fig.text(0.04, 0.925, '주황 25억 초과(한도 2억) · 남색 15억 초과~25억(한도 4억) · 회색 15억 이하', fontsize=13, color='#4B5563')
fig.text(0.04, 0.02, '국토교통부 아파트 매매 실거래(2026-07~10 계약, 10월 20일 받음) · 금융위원회 주택시장 안정화 대책(2025.10.15)', fontsize=10.5, color='#6B7280')
plt.subplots_adjust(left=0.14, right=0.97, top=0.91, bottom=0.05)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
json.dump({'01.png': {'rows': [[o['name'], f"{o['over25']/o['n']*100:.0f}%", f"{o['over25']}건", f"{o['n']}건"] for o in top]}}, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok')
