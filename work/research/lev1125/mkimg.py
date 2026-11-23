# lev1125 그림 — 00 표지(올해 QQQ·QLD·TQQQ), 01 6/2→10/6 세 상품 100 기준 선, 02 1년 제자리 손실 비율·2021 고점 회복 날. 숫자는 calc.py에서 바로
import os, json, datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, NAVY, GRY = '#111827', '#6B7280', '#EA580C', '#1E3A5F', '#94A3B8'
SRC = '야후 파이낸스 일별 수정 종가 QQQ·QLD·TQQQ(11/23 받음) · 세전·분배금 재투자·달러 · 파이어맵 계산'
exec(open('calc.py', encoding='utf-8').read().split('def common')[0])   # Q, L, T, pct
def common(*ds):
    s = set(ds[0]); [s := s & set(x) for x in ds[1:]]; return sorted(s)
def pct(a, b): return (b / a - 1) * 100
d0 = common(Q, L, T); last = d0[-1]; y0 = max(x for x in d0 if x.year == 2025)
ytd = [pct(X[y0], X[last]) for X in (Q, L, T)]
TOPIC_PX, NUM_PX = 54, 40
BG = '#0F3B3A'
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '나스닥100 레버리지', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.785, f'올해 수익률 (1월 1일~{last.month}월 {last.day}일)', fontproperties=Bs(25), color='#99F6E4')
ax = fig.add_axes([0.07, 0.12, 0.86, 0.6]); ax.set_facecolor(BG)
lab = ['QQQ\n지수', 'QLD\n2배', 'TQQQ\n3배']; col = ['#E5E7EB', '#FDBA74', ORG]
ax.bar(range(3), ytd, color=col, width=0.6)
ax.axhline(0, color='white', lw=2)
for i, v in enumerate(ytd):
    ax.text(i, v - 0.8, f'{v:.1f}%', ha='center', va='top', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, 1.0, lab[i], ha='center', va='bottom', fontproperties=Bs(22), color='white')
ax.set_ylim(-30, 7); ax.set_xlim(-0.6, 2.6); ax.axis('off')
fig.text(0.07, 0.045, '야후 일별 수정 종가 · 분배금 재투자 · 세전 · 달러', fontsize=17, color='#99F6E4')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API QQQ·QLD·TQQQ 일별 수정 종가(11/23 받음)로 올해 수익률 직접 계산, calc_out.txt',
           'made_at': '2026-11-23', 'by': 'research/lev1125/mkimg.py', 'out': 'img/00.png', 'topic': '나스닥100 레버리지',
           'num': '·'.join(f'{v:.1f}%' for v in ytd), 'topic_px': TOPIC_PX, 'num_px': NUM_PX,
           'follows': '경쟁 3 yunsdaq/224471815686 기간별 수익률 막대 차트 표지 + 경쟁 6 todayisgood2/224481195777 QQQ vs TQQQ 비교 그림'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 6/2→10/6
a, b = datetime.date(2026, 6, 2), datetime.date(2026, 10, 6)
seg = [x for x in d0 if a <= x <= b]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
for X, c, n, dy in [(Q, INK, 'QQQ', 2.5), (L, '#F59E0B', 'QLD 2배', -1.5), (T, ORG, 'TQQQ 3배', -4.5)]:
    ys = [X[x] / X[a] * 100 for x in seg]; ax.plot(seg, ys, color=c, lw=2.6)
    ax.text(seg[-1] + datetime.timedelta(days=3), ys[-1] + dy, f'{n} {ys[-1]-100:+.1f}%', fontproperties=Bs(14), color=c, va='center')
ax.axhline(100, color=GRY, lw=1, ls='--'); ax.text(seg[0], 100.6, '6월 2일 = 100', fontsize=12, color=SUBC)
ax.set_xlim(seg[0], seg[-1] + datetime.timedelta(days=34))
import matplotlib.dates as md; ax.xaxis.set_major_formatter(md.DateFormatter('%m/%d')); ax.tick_params(labelsize=12)
for s_ in ('top', 'right'): ax.spines[s_].set_visible(False)
frame(fig, '지수는 올랐는데 3배는 내린 넉 달 (6/2 → 10/6)', '6월 2일 값을 100으로 놓고 그림 · 그 사이 QQQ가 하루 2% 넘게 움직인 날 10일')
fig.subplots_adjust(top=0.83, bottom=0.1, left=0.08, right=0.97); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 손실 비율 + 회복 날
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 6.6), dpi=100)
a1.bar([0, 1], [76, 91], color=['#F59E0B', ORG], width=0.6)
for i, v in enumerate([76, 91]): a1.text(i, v - 3, f'{v}%', ha='center', va='top', fontproperties=Bs(26), color='white')
a1.set_xticks([0, 1]); a1.set_xticklabels(['QLD 2배', 'TQQQ 3배'], fontproperties=Bs(14)); a1.set_yticks([]); a1.set_ylim(0, 105)
a1.set_title('QQQ가 1년 제자리(±5%)일 때\n1년 뒤 손실이 난 비율', fontproperties=Bs(15), color=INK)
a2.barh([2, 1, 0], [716, 917, 1111], color=[INK, '#F59E0B', ORG], height=0.6)
for y, v in zip([2, 1, 0], [716, 917, 1111]): a2.text(v - 30, y, f'{v:,}일', ha='right', va='center', fontproperties=Bs(18), color='white')
a2.set_yticks([2, 1, 0]); a2.set_yticklabels(['QQQ', 'QLD', 'TQQQ'], fontproperties=Bs(14)); a2.set_xticks([])
a2.set_title('2021년 고점을\n되찾기까지 걸린 날', fontproperties=Bs(15), color=INK)
for ax_ in (a1, a2):
    for s_ in ('top', 'right', 'left', 'bottom'): ax_.spines[s_].set_visible(False)
frame(fig, '제자리 1년, 그리고 회복까지', 'TQQQ 상장(2010) 뒤 사는 날 3,969번 중 QQQ 제자리 370번 · QLD는 상장(2006) 뒤 502번')
fig.subplots_adjust(top=0.72, bottom=0.13, left=0.06, right=0.97, wspace=0.35); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
import sys; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import cafecover
Image.open('pkg/img/00.png').resize((100, 100)).save('pkg/cover_100.png')
cafecover.board('pkg/img/00.png', cafecover.recent_covers(10, exclude='pkg'), 'pkg/cover_board.png', '새: lev1125')
print('ok', ytd)
