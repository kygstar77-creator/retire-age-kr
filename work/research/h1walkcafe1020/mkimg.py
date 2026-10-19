# h1walkcafe1020 그림 3장 — 숫자는 raw/tour_godeok_1020.json·calc_out.json(국토부 실거래 2026-10-20 받음), 지도는 오픈스트리트맵(ODbL) 단지 경계·보행로.
import os, json, glob
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
T = json.load(open('raw/tour_godeok_1020.json', encoding='utf-8'))
C = {c['name']: c for c in T['complexes']}
show = ['고덕 그라시움', '래미안힐스테이트 고덕', '고덕아남', '고덕아이파크', '고덕풍경채어바니티']
eok = {'고덕 그라시움': '약 24억 3천', '래미안힐스테이트 고덕': '약 20억 3,500', '고덕아남': '약 15억', '고덕아이파크': '약 20억', '고덕풍경채어바니티': '약 17억 5천'}
ORG, NAVY, GRAY = '#EA580C', '#1E3A8A', '#94A3B8'

def polys(c):
    p = c['poly']
    return p if isinstance(p[0][0], list) else [p]

# 00 표지: 지도(단지 경계·역까지 걷는 길)
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
ax = fig.add_axes([0.03, 0.05, 0.94, 0.42])
for n in show:
    c = C[n]; col = ORG if n == '고덕 그라시움' else (NAVY if n == '래미안힐스테이트 고덕' else GRAY)
    for p in polys(c): ax.add_patch(Polygon(p, closed=True, fc=col, ec='white', alpha=0.85 if col != GRAY else 0.5, lw=1))
    r = c['walk']['station']['route']
    ax.plot([x for x, y in r], [y for x, y in r], color=col if col != GRAY else '#64748B', lw=3.5 if col != GRAY else 1.6, ls='-' if col != GRAY else '--')
for s in T['stations']:
    if s['name'] in ('상일동', '고덕', '암사역사공원'):
        ax.plot(s['lon'], s['lat'], 'o', ms=13, mfc='white', mec='#111827', mew=3)
        ax.text(s['lon'], s['lat'] - 0.0008, s['name'] + '역', ha='center', va='top', fontsize=15, fontproperties=B, color='#111827')
for n, t in (('고덕 그라시움', '고덕 그라시움\n역까지 180m'), ('래미안힐스테이트 고덕', '래미안힐스테이트 고덕\n역까지 640m')):
    c = C[n]
    ax.text(c['lon'], c['lat'] + 0.0017, t, ha='center', va='bottom', fontsize=17, fontproperties=B, color=ORG if '그라' in n else NAVY,
            bbox=dict(fc='white', ec='none', alpha=0.85, pad=2))
ax.set_aspect(1 / 0.79); ax.set_xlim(127.136, 127.174); ax.set_ylim(37.5515, 37.5650); ax.axis('off')
fig.text(0.05, 0.835, '그라시움 20%↑', fontsize=88, fontproperties=B, color='#111827')
fig.text(0.05, 0.66, '역 때문일까?', fontsize=88, fontproperties=B, color=ORG)
fig.text(0.05, 0.59, '고덕동 5개 단지 · 84㎡ 한 평 가격 · 걷는 거리', fontsize=20, color='#374151')
fig.text(0.05, 0.02, '지도 © OpenStreetMap 기여자(ODbL) · 국토교통부 실거래(10월 20일 받음) · 파이어맵', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/00.png', dpi=100); plt.close(fig)

# 01 역 거리 순 한 평 값 막대
fig, ax = plt.subplots(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
order = sorted(show, key=lambda n: C[n]['walk']['station']['m'])
for i, n in enumerate(order[::-1]):
    c = C[n]; v = c['ppyTop']; col = ORG if n == '고덕 그라시움' else (NAVY if n == '래미안힐스테이트 고덕' else GRAY)
    ax.barh(i, v, height=0.6, color=col)
    ax.text(v + 120, i + 0.12, f"{v:,}만원", va='center', fontsize=17, fontproperties=B, color='#111827')
    ax.text(v + 120, i - 0.2, f"한 채 {eok[n]}", va='center', fontsize=13, color='#4B5563')
    ax.text(-150, i + 0.12, n, ha='right', va='center', fontsize=16, fontproperties=B, color='#111827')
    ax.text(-150, i - 0.2, f"역 {c['walk']['station']['m']}m · {c['kapt']['use'][:4]}년 입주", ha='right', va='center', fontsize=13, color='#4B5563')
ax.set_xlim(0, 12500); ax.set_ylim(-0.6, 4.6); ax.axis('off')
fig.text(0.04, 0.95, '역에서 가까운 순서로 본 한 평 값', fontsize=24, fontproperties=B, color='#111827')
fig.text(0.04, 0.91, '84㎡대 1년 매매 · 전용면적 한 평 · 가운데 값에서 20% 넘게 벗어난 거래 뺌', fontsize=13, color='#4B5563')
fig.text(0.04, 0.03, '국토교통부 아파트 매매 실거래(2025.11~2026.10 계약, 10월 20일 받음) · 걷는 거리 OpenStreetMap', fontsize=11, color='#6B7280')
plt.subplots_adjust(left=0.36, right=0.97, top=0.88, bottom=0.07)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 25억 선: 두 단지 84㎡ 거래 점
rows = []
for f in sorted(f for f in glob.glob('../rt/11740_2*_trade.json') if 'offi' not in f)[-12:]:
    d = json.load(open(f, encoding='utf-8')); rows += d if isinstance(d, list) else d.get('rows', [])
num = lambda s: float(str(s).replace(',', '') or 0)
pts = {}
for r in rows:
    if r.get('umdNm') != '고덕동' or r.get('cdealType') or r.get('buyerGbn') == '공공기관': continue
    a = r['aptNm'].replace(' ', '')
    n = '고덕 그라시움' if '그라시움' in a else ('래미안힐스테이트 고덕' if '래미안' in a and '힐스' in a else None)
    if not n or not (80 <= num(r['excluUseAr']) < 86): continue
    x = (int(r['dealYear']) - 2025) * 12 + int(r['dealMonth']) - 11 + int(r['dealDay']) / 31
    pts.setdefault(n, []).append((x, num(r['dealAmount']) / 10000))
fig, ax = plt.subplots(figsize=(9, 8), dpi=100); fig.patch.set_facecolor('white')
for n, col in (('고덕 그라시움', ORG), ('래미안힐스테이트 고덕', NAVY)):
    xs, ys = zip(*pts[n]); ax.scatter(xs, ys, s=70, color=col, alpha=0.85, label=n, edgecolor='white')
ax.axhline(25, color='#DC2626', lw=2, ls='--')
ax.text(0.1, 25.68, '25억원 넘으면 주담대 한도 2억원(15억~25억은 4억원)', fontsize=14, fontproperties=B, color='#DC2626')
ax.set_xticks(range(0, 12)); ax.set_xticklabels(['25.11', '12', '26.1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], fontsize=12)
ax.set_ylabel('억원', fontsize=13); ax.set_ylim(19, 26); ax.tick_params(axis='y', labelsize=12)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.grid(axis='y', color='#E5E7EB'); ax.legend(fontsize=14, loc='lower left', frameon=False)
fig.text(0.04, 0.95, '84㎡ 실제 거래, 25억 선 위아래', fontsize=24, fontproperties=B, color='#111827')
fig.text(0.04, 0.91, '점 하나 = 거래 1건(계약한 날) · 해제·공공기관 매수 뺌', fontsize=13, color='#4B5563')
fig.text(0.04, 0.02, '국토교통부 실거래(10월 20일 받음) · 대출 한도: 금융위원회 주택시장 안정화 대책(2025.10.15)', fontsize=11, color='#6B7280')
plt.subplots_adjust(left=0.1, right=0.97, top=0.87, bottom=0.1)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print({n: (len(v), min(y for x, y in v), max(y for x, y in v), sum(1 for x, y in v if y > 25)) for n, v in pts.items()})
json.dump({'01.png': {'rows': [[n, f"역 {C[n]['walk']['station']['m']}m", f"{C[n]['ppyTop']:,}만원", eok[n]] for n in order]}},
          open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
