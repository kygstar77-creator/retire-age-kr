# etfdistday1022 그림 3장 — 숫자는 calc.py(네이버 증권 KRX 일별 시세·야후 분배 기록) 결과
import os, json, datetime, glob, statistics as st
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
import importlib.util
# calc.py 결과 다시 계산(같은 식)
TAX = 0.154; num = lambda s: int(str(s).replace(',', ''))
names = [('458730', 'TIGER 미국배당다우존스'), ('489250', 'KODEX 미국배당다우존스'), ('458760', 'TIGER 미국배당+7%프리미엄'), ('441680', 'TIGER 나스닥100커버드콜')]
res = []; allod = []
for t, nm in names:
    r = json.load(open(f'raw/yh_{t}.json'))['chart']['result'][0]
    ev = {datetime.datetime.fromtimestamp(int(k)).date(): v['amount'] for k, v in r['events']['dividends'].items()}
    px = {}
    for f in glob.glob(f'raw/nvm_{t}_*.json'):
        for x in json.load(open(f, encoding='utf-8')): px[datetime.date.fromisoformat(x['localTradedAt'][:10])] = (num(x['openPrice']), num(x['closePrice']))
    days = sorted(px); a = []; do = []; od = []
    for d, amt in sorted(ev.items()):
        if d not in px: continue
        i = days.index(d); pc = px[days[i - 1]][1]; o = px[d][0]
        a.append(amt); do.append(pc - o); od.append((o - pc) + amt * (1 - TAX))
    res.append((nm, st.mean(a), st.mean(do), sum(v > 0 for v in od), len(od))); allod += od
# 00 표지 — 짙은 청록 바탕, 큰 글 두 줄 + 분배금 vs 분배락 날 시가 하락 막대
BG, WH, LG = '#0F3B3A', '#FFFFFF', '#A7D7D2'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.875, '분배금 받고 바로 팔면?', fontsize=64, fontproperties=B, color=WH)
fig.text(0.06, 0.765, f'평균은 1주당 {abs(st.mean(allod)):.1f}원 손해', fontsize=60, fontproperties=B, color='#FB923C')
ax = fig.add_axes([0.08, 0.14, 0.86, 0.50]); ax.set_facecolor(BG)
for i, (nm, ma, md, w, n) in enumerate(res):
    ax.bar(i * 3, ma, color=LG, width=1.1); ax.bar(i * 3 + 1.2, md, color='#FB923C', width=1.1)
    ax.text(i * 3, ma + 3, f'{int(ma+0.5)}원', ha='center', fontproperties=Bs(20), color=LG); ax.text(i * 3 + 1.2, md + 3, f'{int(md+0.5)}원', ha='center', fontproperties=Bs(20), color='#FB923C')
    ax.text(i * 3 + 0.6, -14, nm.replace('TIGER ', 'TIGER\n').replace('KODEX ', 'KODEX\n'), ha='center', va='top', fontsize=15, color=WH)
ax.set_ylim(-40, 135); ax.set_yticks([]); ax.set_xticks([])
for s_ in ('top', 'right', 'left', 'bottom'): ax.spines[s_].set_visible(False)
ax.axhline(0, color=LG, lw=1)
ax.text(-0.6, 128, '■ 왼쪽: 평균 분배금', color=LG, fontproperties=Bs(22)); ax.text(4.2, 128, '■ 오른쪽: 다음 날 아침 하락', color='#FB923C', fontproperties=Bs(22))
fig.text(0.06, 0.695, f'ETF 4개 2년 {len(allod)}번 — 이득 {sum(v>0 for v in allod)}번·손해 {sum(v<0 for v in allod)}번 (세금 뗀 뒤)', fontsize=28, color=WH)
fig.text(0.06, 0.03, 'ETF 4개 분배락일 2024.10~2026.10 · 1주당 · KRX 시세 직접 계산', fontsize=19, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 10월 달력 — 매수 마감 10/28 · 분배락 10/29 · 기준일 10/30
fig, ax = plt.subplots(figsize=(9, 6), dpi=100)
days_ = [('10/26', '월', ''), ('10/27', '화', ''), ('10/28', '수', '이날까지 사야\n10월분 받음'), ('10/29', '목', '분배락\n오늘 사면 못 받음'), ('10/30', '금', '기준일\n(마지막 영업일)')]
for i, (d, w, lab) in enumerate(days_):
    c = ORG if d == '10/28' else ('#FDE7D6' if d == '10/29' else ('#E5E7EB' if d == '10/30' else 'white'))
    ax.add_patch(plt.Rectangle((i * 1.9, 0), 1.75, 2.2, fc=c, ec='#CBD5E1', lw=1.5))
    ax.text(i * 1.9 + 0.875, 1.75, f'{d}({w})', ha='center', fontproperties=Bs(17), color='white' if d == '10/28' else INK)
    ax.text(i * 1.9 + 0.875, 0.75, lab, ha='center', va='center', fontsize=13, color='white' if d == '10/28' else INK)
ax.set_xlim(-0.2, 9.6); ax.set_ylim(-0.6, 2.6); ax.axis('off')
fig.text(0.05, 0.9, '말일 기준 월배당 ETF, 10월분 받으려면', fontsize=24, fontproperties=B, color=INK)
fig.text(0.05, 0.83, '사고 이틀 뒤(T+2)에 계좌에 들어오니까 기준일 2영업일 전까지', fontsize=16, color=SUB)
fig.text(0.05, 0.04, '15일 기준 ETF는 날짜가 다름 · 상품마다 운용사 공시로 확인', fontsize=13, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 96번 하루 손익 — 앞날 종가에 사서 분배락 날 시가에 팔고 분배금 세후 받은 결과(1주당 원)
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)
vals = sorted(allod)
ax.bar(range(len(vals)), vals, color=[ORG if v > 0 else GR for v in vals], width=0.8)
ax.axhline(0, color=INK, lw=1)
ax.set_xticks([]); ax.tick_params(labelsize=12); ax.set_ylabel('1주당 원', fontsize=12, color=SUB)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.text(len(vals) * 0.55, max(vals) * 0.85, f'이득 {sum(v>0 for v in vals)}번', ha='right', fontproperties=Bs(18), color=ORG)
ax.text(len(vals) * 0.03, min(vals) * 0.85, f'손해 {sum(v<0 for v in vals)}번', ha='left', fontproperties=Bs(18), color=SUB)
fig.text(0.05, 0.93, f'분배락 하루 전에 사서 다음 날 아침 판 {len(vals)}번', fontsize=23, fontproperties=B, color=INK)
fig.text(0.05, 0.88, f'평균 1주당 {st.mean(vals):+.1f}원 (분배금 세금 15.4% 뗀 뒤, 수수료 빼기 전)', fontsize=16, color=SUB)
fig.text(0.05, 0.02, 'ETF 4개 · 2024.10~2026.10 분배락일 · 네이버 증권 일별 시세(KRX) · 직접 계산', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.08)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print(res, len(allod), sum(v>0 for v in allod), st.mean(allod))
