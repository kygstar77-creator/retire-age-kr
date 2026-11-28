# krndx1129 그림 — 00 표지(올해 1억 두 곳 끝값), 01 올해 흐름(QQQ 달러·TIGER·TIGER(H), 12/30=100), 02 올해 고점 날짜·고점 대비(3칸 목록)
# 숫자: 야후 chart API 수정종가(네이버 siseJson 수정주가와 같음, raw/), 환율 ECOS 731Y001 매매기준율(raw/fx_ecos.json)
import os, json, glob, datetime as D, warnings; warnings.filterwarnings('ignore')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs('pkg/img', exist_ok=True)
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, NAVY, GRY = '#111827', '#6B7280', '#EA580C', '#1E3A5F', '#94A3B8'
BG = '#E3EEF8'  # 11/28: 남색(#14324A)이 옆 sq1pair1128·JEPI 남색과 겹쳐 연하늘로
SRC = '야후 파이낸스·네이버 증권 분배 반영 종가(2026.11.27까지) · 한국은행 원·달러 매매기준율 · 파이어맵 계산'
def load(n):
    r = json.load(open(f'raw/{n}_1d.json', encoding='utf-8'))['chart']['result'][0]; tz = r['meta']['gmtoffset']
    ts = [D.datetime.utcfromtimestamp(x + tz).date() for x in r['timestamp']]
    return {d: a for d, a in zip(ts, r['indicators']['adjclose'][0]['adjclose']) if a}
Q, T, H = load('QQQ'), load('133690.KS'), load('448300.KS')
d0k, d0u, d1 = D.date(2025, 12, 30), D.date(2025, 12, 31), D.date(2026, 11, 27)
r = lambda s, a, b: s[b] / s[a] - 1
rq, rt, rh = r(Q, d0u, d1), r(T, d0k, d1), r(H, d0k, d1)
assert round(rq * 100, 1) == 6.3 and round(rt * 100, 1) == -2.2 and round(rh * 100, 1) == 3.2, (rq, rt, rh)
def man(v):
    m = round(v / 1e4)
    if m >= 10000: return f'{m//10000}억 {m%10000:,}만' if m % 10000 else f'{m//10000}억'
    return f'{m:,}만'
vt, vh = 1e8 * (1 + rt), 1e8 * (1 + rh)
print('1억 ->', man(vt), man(vh), '7/1까지', round(r(T, d0k, D.date(2026, 7, 1)) * 100, 1), round(r(H, d0k, D.date(2026, 7, 1)) * 100, 1))
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '국내상장 나스닥100', fontproperties=Bs(50), color=INK)
fig.text(0.07, 0.785, '올해 1억 넣었다면 (12/30 → 11/27)', fontproperties=Bs(28), color='#B45309')
ax = fig.add_axes([0.08, 0.2, 0.84, 0.52]); ax.set_facecolor(BG)
R = [('환노출\nTIGER 미국나스닥100', vt / 1e8, '#64748B'), ('환헤지\nTIGER 미국나스닥100(H)', vh / 1e8, ORG)]
ax.bar(range(2), [v - 0.6 for _, v, _ in R], bottom=0.6, color=[c for _, _, c in R], width=0.55)
for i, (n, v, _) in enumerate(R):
    ax.text(i, max(v, 1.0) + 0.014, man(v * 1e8) + '원', ha='center', va='bottom', fontproperties=Bs(34), color=INK)
    ax.text(i, 0.59, n, ha='center', va='top', fontproperties=Bs(19), color=INK)
ax.axhline(1.0, color='#B45309', lw=2, ls='--'); ax.text(1.95, 0.997, '넣은 돈 1억', ha='right', va='top', fontproperties=Bs(18), color='#B45309')
ax.set_ylim(0.48, 1.1); ax.set_xlim(-0.6, 1.95); ax.axis('off')
fig.text(0.07, 0.085, '같은 나스닥100인데 갈린 건 환율', fontproperties=Bs(30), color=INK)
fig.text(0.07, 0.035, '2026.11.27 종가 · 분배금 반영 · 세금·수수료 전', fontsize=17, color='#B45309')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API 133690.KS·448300.KS 수정종가(네이버 증권 siseJson 수정주가와 대조) 2025-12-30→2026-11-27 직접 계산, calc2_out.txt',
           'made_at': D.datetime.now().strftime('%Y-%m-%d %H:%M'), 'by': 'research/krndx1129/mkimg.py', 'out': 'img/00.png', 'topic': '국내상장 나스닥100',
           'num': f'{man(vt)}원 · {man(vh)}원 (넣은 돈 1억)', 'topic_px': 50, 'num_px': 34,
           'follows': '경쟁 1 healthy_life_365·6 whduddnd49 표지(환노출 vs 환헤지 두 상품 비교) + plusdiv1128 막대 위 큰 숫자'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK); fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 올해 흐름 (11/28 이해 시험 3차: QQQ 선이 'QQQ×환율' 셈을 부르는데 날짜가 하루 어긋나 안 맞음 → 한국 두 상품만)
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
for s, a, c, n in ((H, d0k, ORG, 'TIGER 미국나스닥100(H) 환헤지'), (T, d0k, GRY, 'TIGER 미국나스닥100 환노출')):
    ks = sorted(k for k in s if k >= a); ax.plot(ks, [s[k] / s[a] * 100 for k in ks], color=c, lw=2.4, label=n)
    ax.annotate(f'{(s[d1]/s[a]-1)*100:+.1f}%', (d1, s[d1] / s[a] * 100), xytext=(6, 0), textcoords='offset points', fontproperties=Bs(14), color=c, va='center')
pk = D.date(2026, 7, 1); ax.scatter([pk], [T[pk] / T[d0k] * 100], color=GRY, s=40, zorder=5)
ax.annotate('7월 1일 환노출형 고점\n(환율 최고 7월 2일 하루 전)', (pk, T[pk] / T[d0k] * 100), xytext=(D.date(2026, 8, 5), 128), fontproperties=Bs(13), color=SUBC, arrowprops=dict(arrowstyle='-', color=GRY, lw=1))
ax.axhline(100, color='#D1D5DB', lw=1)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 3, 5, 7, 9, 11])); ax.xaxis.set_major_formatter(mdates.DateFormatter('%#m월'))
ax.tick_params(labelsize=12); ax.grid(axis='y', color='#E5E7EB')
for s_ in ('top', 'right'): ax.spines[s_].set_visible(False)
ax.legend(loc='upper left', frameon=False, prop=Bs(12.5)); ax.set_ylim(88, 132); ax.set_xlim(d0k, D.date(2026, 12, 31))
frame(fig, '올해 같은 나스닥100, 두 상품 흐름', '작년 마지막 거래일 = 100 · 분배금 반영 · 원·달러 환율 1,433.9원 → 1,342.7원')
fig.subplots_adjust(top=0.84, bottom=0.11, left=0.08, right=0.95); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 올해 고점 — 3칸 목록
def pkd(s):
    k = max((x for x in s if x >= D.date(2026, 1, 1)), key=lambda x: s[x]); return k, (s[d1] / s[k] - 1) * 100
G = [('TIGER (H) 환헤지', *pkd(H), ORG), ('TIGER 환노출', *pkd(T), GRY)]
print([(n, str(k), round(v, 1)) for n, k, v, _ in G])
fig, ax = plt.subplots(figsize=(9, 5.4), dpi=100); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0.9, 4.2)
for x, h in ((0.3, '상품'), (4.6, '올해 고점'), (7.4, '고점 대비 지금')): ax.text(x, 3.65, h, fontproperties=Bs(16), color=SUBC)
for i, (n, k, v, c) in enumerate(G):
    yy = 2.85 - i * 1.0
    ax.text(0.3, yy, n, fontproperties=Bs(19), color=INK, va='center')
    ax.text(4.6, yy, f'{k.month}월 {k.day}일', fontproperties=Bs(22), color=c, va='center')
    ax.text(7.4, yy, f'{v:.1f}%', fontproperties=Bs(22), color=c, va='center')
    if i < 1: ax.plot([0.3, 9.7], [yy - 0.5, yy - 0.5], color='#E5E7EB', lw=1.5)
frame(fig, '고점도 다른 날 찍었어요', '2026.11.27 종가 · 분배금 반영 · 원·달러 환율 올해 최고 7월 2일 1,554.4원')
fig.subplots_adjust(top=0.8, bottom=0.08, left=0.02, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'krndx1129' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok', [p.split(os.sep)[-4] if os.sep in p else p for p in recent])
