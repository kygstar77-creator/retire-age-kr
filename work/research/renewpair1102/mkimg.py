# renewpair1102 그림 3장 — 숫자는 raw/(국토부 아파트 전월세 실거래, 2026-11-02 21시 받음) · 거르기는 calc.py와 같음
import os, json, glob, statistics as st, random
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bf(s): return fm.FontProperties(fname=F + r'\pd700.ttf', size=s)
ORG, NAVY = '#EA580C', '#1E3A8A'
FOCUS = {'잠실동': ['주공아파트5단지', '리센츠', '잠실엘스', '트리지움', '우성아파트'],
         '대치동': ['은마', '래미안대치팰리스', '대치르엘', '한보미도맨션1'],
         '반포동': ['래미안원베일리', '아크로리버파크', '래미안퍼스티지', '반포자이', '반포미도']}
def num(s): return float(str(s or '0').replace(',', '') or 0)
rows = [r for p in glob.glob('raw/*_rent.json') for r in json.load(open(p, encoding='utf-8')) if isinstance(r, dict) and 'aptNm' in r]
ren = [r for r in rows if r['umdNm'] in FOCUS and r['aptNm'].replace(' ', '') in FOCUS[r['umdNm']] and 80 <= num(r['excluUseAr']) < 85
       and num(r['monthlyRent']) == 0 and r.get('contractType') == '갱신' and num(r.get('preDeposit')) > 0]
def rate(r): return (num(r['deposit']) / num(r['preDeposit']) - 1) * 100
U = [rate(r) for r in ren if r.get('useRRRight') == '사용']; N = [rate(r) for r in ren if r.get('useRRRight') != '사용']
print(len(U), len(N), sum(v > 5.0001 for v in U), sum(v > 5.0001 for v in N))
SRC = '국토교통부 아파트 전월세 실거래(2025.11~2026.10 계약, 11월 2일 받음) · 잠실·대치·반포 14단지 전용 80~85㎡ 전세 갱신 · 파이어맵 계산'

# 00 표지(차트): 큰 글 + 올린 폭 점
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.06, 0.85, '계약갱신요구권 쓰면', fontproperties=Bf(58), color='#111827')
fig.text(0.06, 0.755, '전세 보증금 몇 %까지?', fontproperties=Bf(46), color='#374151')
fig.text(0.06, 0.615, f'쓴 {len(U)}건', fontproperties=Bf(52), color=NAVY)
fig.text(0.47, 0.615, '5% 넘김 0건', fontproperties=Bf(52), color=ORG)
fig.text(0.06, 0.55, '강남·서초·송파 14단지 84㎡ 갱신 계약을 하나씩 셌어요', fontsize=19, color='#374151')
ax = fig.add_axes([0.24, 0.13, 0.70, 0.33]); random.seed(1)
for y, xs, c in ((1, U, NAVY), (0, N, ORG)):
    for v in xs: ax.scatter(max(-5, min(v, 25)), y + random.uniform(-0.2, 0.2), s=40, color=c, alpha=0.45, edgecolor='none')
ax.axvline(5, color='#111827', lw=2.5, ls='--'); ax.text(5.3, 1.55, '5%', fontproperties=Bf(18), color='#111827')
ax.set_yticks([1, 0]); ax.set_yticklabels([f'권리 씀 {len(U)}건', f'표시 없음 {len(N)}건'], fontproperties=Bf(18))
ax.set_xlim(-6, 26); ax.set_ylim(-0.5, 1.75); ax.set_xticks([0, 5, 10, 15, 20, 25]); ax.set_xticklabels(['0%', '5%', '10%', '15%', '20%', '25%↑'], fontsize=14)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
fig.text(0.06, 0.04, SRC, fontsize=9.5, color='#6B7280')
fig.savefig('pkg/img/00.png', dpi=100); plt.close(fig)

# 01 두 묶음 비교 막대: 딱 5% / 5% 넘김 비율
def share(xs, f): return sum(f(v) for v in xs) / len(xs) * 100
fig, ax = plt.subplots(figsize=(9, 7.5), dpi=100); fig.patch.set_facecolor('white')
cats = [('5% 넘게 올림', lambda v: v > 5.0001), ('딱 5% 올림', lambda v: 4.95 <= v <= 5.0001), ('그대로 두거나 내림', lambda v: v < 0.01)]
for i, (nm, f) in enumerate(cats):
    y = 2 - i
    a, b = share(U, f), share(N, f)
    ax.barh(y + 0.18, a, height=0.32, color=NAVY); ax.barh(y - 0.18, b, height=0.32, color=ORG)
    ax.text(a + 1, y + 0.18, f'{a:.0f}%', va='center', fontproperties=Bf(17), color=NAVY)
    ax.text(b + 1, y - 0.18, f'{b:.0f}%', va='center', fontproperties=Bf(17), color=ORG)
ax.set_yticks([2, 1, 0]); ax.set_yticklabels([c[0] for c in cats], fontproperties=Bf(17))
ax.set_xlim(0, 80); ax.set_xticks([])
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
fig.text(0.05, 0.93, '갱신 계약, 권리를 썼느냐에 따라', fontproperties=Bf(24), color='#111827')
fig.text(0.05, 0.885, f'파랑 = 계약갱신요구권 썼다고 신고 {len(U)}건 · 주황 = 그 표시 없음 {len(N)}건', fontsize=14, color='#4B5563')
fig.text(0.05, 0.03, SRC, fontsize=9.5, color='#6B7280')
plt.subplots_adjust(left=0.27, right=0.95, top=0.84, bottom=0.08)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 10억 전세 예시: 5%면 얼마, 표시 없는 5% 초과 가운데 12.5%면 얼마
over = sorted(v for v in N if v > 5.0001); mo = st.median(over)
fig, ax = plt.subplots(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
vals = [('권리 쓰면 최대', 10 * 1.05, NAVY), (f'5% 넘긴 계약 가운데({mo:.1f}%)', 10 * (1 + mo / 100), ORG)]
for i, (nm, v, c) in enumerate(vals):
    y = 1 - i
    ax.barh(y, v, height=0.5, color=c); ax.text(v + 0.1, y, f'{v:.2f}억', va='center', fontproperties=Bf(22), color=c)
    ax.text(0.15, y + 0.38, nm, fontproperties=Bf(17), color='#111827')
ax.axvline(10, color='#9CA3AF', lw=1.5, ls='--'); ax.text(9.85, -0.62, '지금 보증금 10억', ha='right', fontsize=14, color='#4B5563')
ax.set_xlim(0, 13.5); ax.set_ylim(-0.75, 1.7); ax.axis('off')
fig.text(0.05, 0.92, '지금 전세 10억이라면, 다시 계약할 때', fontproperties=Bf(24), color='#111827')
fig.text(0.05, 0.875, f'5% = 5,000만원 · 표시 없는 갱신 중 5% 넘긴 {len(over)}건의 가운데 {mo:.1f}%를 10억에 대 본 값', fontsize=13, color='#4B5563')
fig.text(0.05, 0.03, SRC, fontsize=9.5, color='#6B7280')
plt.subplots_adjust(left=0.04, right=0.96, top=0.83, bottom=0.1)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok', mo)
