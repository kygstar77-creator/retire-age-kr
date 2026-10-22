# h1forest1022 그림 3장 — 숫자는 raw/(국토부 아파트 전월세·매매 실거래, 2026-10-22 19:4x 받음). 84㎡대=전용 80~85㎡, 전세=월세 0원.
import os, json, glob, statistics as st
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
ORG, NAVY = '#EA580C', '#1E3A8A'
def n(s): return int((s or '0').replace(',', '') or 0)
def jeon(name, l):
    R = [x for f in sorted(glob.glob(f'raw/{l}_??????_rent.json')) for x in json.load(open(f, encoding='utf-8'))
         if x['aptNm'] == name and 80 <= float(x['excluUseAr']) <= 85 and n(x['monthlyRent']) == 0]
    R = list({json.dumps(x, sort_keys=True): x for x in R}.values())
    for x in R: x['ym'] = int(x['dealYear']) * 100 + int(x['dealMonth']); x['d'] = n(x['deposit']) / 1e4
    return R
fo = jeon('올림픽파크포레온', '11740'); he = jeon('헬리오시티', '11710')
Y = [x for x in fo if 202511 <= x['ym'] <= 202610]
new = [x['d'] for x in Y if x['contractType'] == '신규']; ren = [x['d'] for x in Y if x['contractType'] == '갱신']
HY = [x for x in he if 202511 <= x['ym'] <= 202610]
hnew = [x['d'] for x in HY if x['contractType'] == '신규']; hren = [x['d'] for x in HY if x['contractType'] == '갱신']
print(len(new), st.median(new), len(ren), st.median(ren), len(hnew), st.median(hnew), len(hren), st.median(hren))
os.makedirs('pkg/img', exist_ok=True)
SRC = '국토교통부 아파트 전월세 실거래(2025.11~2026.10 계약, 10월 22일 받음) · 전용 80~85㎡ 전세(월세 0원) · 파이어맵 계산'

# 00 표지(차트): 큰 글 + 79건 점 두 줄
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.84, '올림픽파크포레온', fontsize=74, fontproperties=fm.FontProperties(fname=F + r'\pd700.ttf', size=74), color='#111827')
fig.text(0.06, 0.735, '84㎡ 전세, 갱신과 새 계약', fontsize=40, fontproperties=fm.FontProperties(fname=F + r'\pd700.ttf', size=40), color='#374151')
fig.text(0.06, 0.59, '갱신 10억', fontproperties=fm.FontProperties(fname=F + r'\pd700.ttf', size=58), color=NAVY)
fig.text(0.50, 0.59, '새 계약 14억', fontproperties=fm.FontProperties(fname=F + r'\pd700.ttf', size=58), color=ORG)
fig.text(0.06, 0.515, '1년 전세 계약 79건을 갱신·새 계약으로 나눠 직접 셌어요', fontsize=19, color='#374151')
ax = fig.add_axes([0.2, 0.12, 0.74, 0.33])
import random; random.seed(1)
for v in ren: ax.scatter(v, 1 + random.uniform(-0.18, 0.18), s=150, color=NAVY, alpha=0.75, edgecolor='white')
for v in new: ax.scatter(v, 0 + random.uniform(-0.18, 0.18), s=150, color=ORG, alpha=0.8, edgecolor='white')
for y, v, c in [(1, st.median(ren), NAVY), (0, st.median(new), ORG)]:
    ax.plot([v, v], [y - 0.36, y + 0.36], color='#111827', lw=3)
ax.set_yticks([1, 0]); ax.set_yticklabels([f'갱신 {len(ren)}건', f'새 계약 {len(new)}건'], fontproperties=fm.FontProperties(fname=F + '\pd700.ttf', size=19))
ax.set_xlim(8, 17); ax.set_ylim(-0.6, 1.6)
ax.set_xticks([8, 10, 12, 14, 16]); ax.set_xticklabels(['8억', '10억', '12억', '14억', '16억'], fontsize=15)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
fig.text(0.94, 0.455, '검은 선 = 가운데 값', fontsize=13, color='#4B5563', ha='right')
fig.text(0.06, 0.03, SRC, fontsize=10.5, color='#6B7280')
fig.savefig('pkg/img/00.png', dpi=100); plt.close(fig)

# 01 입주 뒤 2년 전세 계약 점(달별) — 신규 주황, 갱신 파랑
A = [x for x in fo if 202411 <= x['ym'] <= 202610]
MS = []; y, m = 2024, 11
while y * 100 + m <= 202610:
    MS.append(y * 100 + m); m += 1
    if m > 12: y, m = y + 1, 1
fig, ax = plt.subplots(figsize=(9, 8), dpi=100); fig.patch.set_facecolor('white')
for x in A:
    xi = MS.index(x['ym']) + int(x['dealDay']) / 32
    if x['contractType'] == '갱신': ax.scatter(xi, x['d'], s=70, color=NAVY, alpha=0.75, edgecolor='white', zorder=4)
    else: ax.scatter(xi, x['d'], s=55, color=ORG, alpha=0.6, edgecolor='white', zorder=3)
first = [x['d'] for x in fo if 202411 <= x['ym'] <= 202504]
ax.axhline(st.median(first), color='#9CA3AF', lw=1.5, ls='--')
ax.text(12, st.median(first) - 0.55, f'입주 첫 반년 전세 가운데 {st.median(first):.1f}억', fontsize=13, color='#4B5563', ha='center')
ax.set_xticks([0.5, 2.5, 8.5, 14.5, 20.5, 23.5]); ax.set_xticklabels(['24.11', '25.1', '7', '26.1', '7', '10'], fontsize=12)
ax.set_xlim(0, 24); ax.set_ylim(3.5, 17.5); ax.set_yticks([4, 8, 12, 16]); ax.set_yticklabels(['4억', '8억', '12억', '16억'], fontsize=13)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.grid(axis='y', color='#E5E7EB', lw=1)
fig.text(0.05, 0.945, f'올림픽파크포레온 84㎡ 입주 뒤 전세 {len(A)}건', fontsize=23, fontproperties=B, color='#111827')
fig.text(0.05, 0.905, '주황 = 새 계약 · 파랑 = 갱신 계약(올해 6월부터 신고)', fontsize=14, color='#4B5563')
fig.text(0.05, 0.02, '국토교통부 아파트 전월세 실거래(2024.11~2026.10 계약, 10월 22일 받음) · 전용 80~85㎡ 전세 · 파이어맵', fontsize=10.5, color='#6B7280')
plt.subplots_adjust(left=0.1, right=0.97, top=0.87, bottom=0.1)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 두 단지 갱신 vs 새 계약 가운데 값
fig, ax = plt.subplots(figsize=(9, 7.5), dpi=100); fig.patch.set_facecolor('white')
rows = [('올림픽파크포레온', st.median(ren), st.median(new), len(ren), len(new)), ('헬리오시티', st.median(hren), st.median(hnew), len(hren), len(hnew))]
for i, (nm, r, w, cr, cw) in enumerate(rows):
    y = 1 - i
    ax.plot([r, w], [y, y], color='#CBD5E1', lw=8, zorder=1)
    ax.scatter(r, y, s=380, color=NAVY, zorder=3); ax.scatter(w, y, s=380, color=ORG, zorder=3)
    ax.text(8.2, y + 0.3, nm, fontsize=19, fontproperties=B, color='#111827')
    ax.text(r, y - 0.24, f'갱신 {r:.1f}억', fontsize=14, color=NAVY, ha='center', fontproperties=B)
    ax.text(w, y - 0.24, f'새 계약 {w:.1f}억', fontsize=14, color=ORG, ha='center', fontproperties=B)
    gap = w - r
    ax.text(16.8, y, f'차이 {gap:.1f}억', fontsize=20, fontproperties=B, color='#DC2626', ha='right', va='center')
ax.set_xlim(8, 17); ax.set_ylim(-0.6, 1.6); ax.axis('off')
fig.text(0.05, 0.93, '같은 84㎡ 전세, 갱신과 새 계약 가운데 값', fontsize=22, fontproperties=B, color='#111827')
fig.text(0.05, 0.885, f'포레온 갱신 {len(ren)}건·새 계약 {len(new)}건 · 헬리오시티 갱신 {len(hren)}건·새 계약 {len(hnew)}건(최근 1년)', fontsize=13, color='#4B5563')
fig.text(0.05, 0.03, SRC, fontsize=10.5, color='#6B7280')
plt.subplots_adjust(left=0.03, right=0.97, top=0.85, bottom=0.08)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
