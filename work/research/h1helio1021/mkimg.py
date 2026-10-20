# h1helio1021 그림 3장 — 숫자는 calc_out.json(국토부 실거래 송파구, 2026-10-20 23:13 받음).
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
D = json.load(open('calc_out.json', encoding='utf-8'))
ORG, NAVY, GRAY = '#EA580C', '#1E3A8A', '#94A3B8'
os.makedirs('pkg/img', exist_ok=True)
ML = ['25.11', '12', '26.1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
MS = ['202511','202512','202601','202602','202603','202604','202605','202606','202607','202608','202609','202610']
import statistics as st
hel = D['helio']
# 01 헬리오시티 84㎡대 1년 거래 점 + 달별 가운데 값
fig, ax = plt.subplots(figsize=(9, 8), dpi=100); fig.patch.set_facecolor('white')
for r in hel:
    x = MS.index(r['ym']) + int(r['day']) / 32
    y = r['amt'] / 10000
    if r['gbn'] == '직거래': ax.scatter(x, y, s=190, color=ORG, zorder=5, edgecolor='white')
    else: ax.scatter(x, y, s=55, color=NAVY, alpha=0.55, edgecolor='white')
meds = []
for i, ym in enumerate(MS):
    v = [r['amt'] / 10000 for r in hel if r['ym'] == ym and r['gbn'] != '직거래']
    if v: meds.append((i + 0.5, st.median(v)))
ax.plot([m[0] for m in meds], [m[1] for m in meds], color='#111827', lw=2.2, ls='--', zorder=3)
ax.text(6.6, 21.0, '5월 28일 26층 20억원 직거래', fontsize=15, fontproperties=B, color=ORG, va='center', ha='right')
ax.text(6.6, 20.35, '같은 달 나머지 17건 가운데 값은 28억 1천만원', fontsize=13, color='#374151', va='center', ha='right')
ax.set_xticks([i + 0.5 for i in range(12)]); ax.set_xticklabels(ML, fontsize=12)
ax.set_ylim(19, 33); ax.set_xlim(0, 12); ax.set_yticks([20, 24, 28, 32]); ax.set_yticklabels(['20억', '24억', '28억', '32억'], fontsize=13)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.grid(axis='y', color='#E5E7EB', lw=1)
fig.text(0.05, 0.945, '헬리오시티 84㎡ 1년 거래 86건', fontsize=24, fontproperties=B, color='#111827')
fig.text(0.05, 0.905, '주황 = 직거래 1건 · 파랑 = 중개거래 85건 · 점선 = 달마다 중개거래 가운데 값', fontsize=13, color='#4B5563')
fig.text(0.05, 0.02, '국토교통부 아파트 매매 실거래(2025.11~2026.10 계약, 10월 20일 받음, 해제 제외) · 파이어맵 계산', fontsize=11, color='#6B7280')
plt.subplots_adjust(left=0.1, right=0.97, top=0.87, bottom=0.1)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 송파구 직거래 8건: 직거래 값 vs 같은 단지·같은 달 중개거래 가운데 값
c = sorted(D['cmp'], key=lambda r: r['pct'])
fig, ax = plt.subplots(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
for i, r in enumerate(c[::-1]):
    y = i; a = r['amt'] / 10000; m = r['med'] / 10000
    ax.plot([a, m], [y, y], color='#CBD5E1', lw=5, zorder=1)
    ax.scatter(m, y, s=120, color=NAVY, zorder=3); ax.scatter(a, y, s=170, color=ORG, zorder=4)
    nm = r['apt'].replace('아파트', '')
    ax.text(5, y + 0.14, f"{nm} {int(r['ym'][4:])}월", fontsize=15, fontproperties=B, color='#111827', va='center')
    col = '#DC2626' if r['pct'] < 0 else NAVY
    ax.text(5, y - 0.2, f"직거래 {a:.2f}억 · 중개 가운데 {m:.2f}억", fontsize=12, color='#4B5563', va='center')
    ax.text(37.8, y, f"{r['pct']:+.0f}%", fontsize=19, fontproperties=B, color=col, va='center', ha='right')
ax.set_xlim(5, 38); ax.set_ylim(-0.7, 7.7); ax.axis('off')
fig.text(0.05, 0.95, '송파구 84㎡ 직거래 8건, 같은 달 중개거래보다', fontsize=21, fontproperties=B, color='#111827')
fig.text(0.05, 0.915, '주황 = 직거래 · 파랑 = 같은 단지·같은 달 중개거래 가운데 값(3건 이상)', fontsize=13, color='#4B5563')
fig.text(0.05, 0.02, '국토교통부 아파트 매매 실거래(2025.11~2026.10 계약, 10월 20일 받음) · 8건 외 35건은 비교할 중개거래 3건 미만', fontsize=11, color='#6B7280')
plt.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.07)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)

# 00 표지(차트): 큰 글 + 8건 점 띠
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.82, '헬리오시티 20억', fontsize=86, fontproperties=B, color='#111827')
fig.text(0.06, 0.66, '직거래, 싼 걸까?', fontsize=86, fontproperties=ORG and B, color=ORG)
fig.text(0.06, 0.585, '송파구 84㎡ 직거래 8건 비교 · 같은 달 중개거래와 · 직접 계산', fontsize=20, color='#374151')
ax = fig.add_axes([0.06, 0.1, 0.88, 0.42])
for i, r in enumerate(c):
    x = r['pct']
    ax.scatter(x, 0, s=420, color=ORG if x < 0 else NAVY, alpha=0.9, edgecolor='white', zorder=3)
ax.axvline(0, color='#111827', lw=2)
ax.set_xlim(-34, 14); ax.set_ylim(-1, 1); ax.set_yticks([])
ax.set_xticks([-30, -20, -10, 0, 10]); ax.set_xticklabels(['-30%', '-20%', '-10%', '같은 값', '+10%'], fontsize=15)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.text(-33, 0.55, '더 쌌다 (7건)', fontsize=17, fontproperties=B, color=ORG)
ax.text(14, 0.55, '더 비쌌다 (1건)', fontsize=17, fontproperties=B, color=NAVY, ha='right')
fig.text(0.06, 0.03, '국토교통부 실거래(2025.11~2026.10, 10월 20일 받음) · 같은 단지·같은 달 중개 3건 이상인 8건 · 파이어맵', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/00.png', dpi=100); plt.close(fig)
print('ok')
