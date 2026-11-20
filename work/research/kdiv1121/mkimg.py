# kdiv1121 그림 — 00 표지(차트: 1년 새 월 분배금 늘어난 비율 4개), 01 1년 전 vs 지금 월 분배금(원), 02 1억원 한 달 분배금(세전). 숫자는 calc_out.txt
import os, json, glob
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image
import numpy as np
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, INK, SUBC, ORG, GRY = '#1D4ED8', '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = "한화자산운용 · 야후 파이낸스 분배 기록·종가 · 네이버페이 증권 · 파이어맵 계산"
D = json.load(open('calc.json', encoding='utf-8'))
BG = '#0F3D3E'
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '고배당 ETF 5개 월 분배금', fontproperties=Bs(46), color='white')
fig.text(0.07, 0.77, '1년 새 얼마나 늘었나', fontproperties=Bs(38), color='#99F6E4')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.52]); ax.set_facecolor(BG)
names = ['KIWOOM', 'TIGER\n은행', 'KODEX', 'PLUS']; v = [D['g']['104530'], D['g']['466940'], D['g']['279530'], D['g']['161510']]
cols = ['#5EEAD4', '#5EEAD4', '#5EEAD4', '#FB923C']
ax.bar(range(4), v, color=cols, width=0.62)
for i, x in enumerate(v): ax.text(i, x + 3, f'{x:.0f}%', ha='center', va='bottom', fontproperties=Bs(36 if i in (0, 3) else 28), color='white')
for i, t in enumerate(names): ax.text(i, -6, t, ha='center', va='top', fontproperties=Bs(24), color='white')
ax.set_ylim(-30, 125); ax.set_xlim(-0.6, 3.6); ax.axis('off')
fig.text(0.07, 0.1, '1년 전 같은 달 → 최근 달 주당 분배금 · SOL은 1년 기록 없음', fontproperties=Bs(21), color='white')
fig.text(0.07, 0.045, '야후·네이버·한화자산운용 · 파이어맵 계산', fontsize=17, color='#99F6E4')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 분배 events + 네이버페이 증권 ETF 분석 + 한화자산운용 PLUS 고배당주 분배금 지급현황, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-20', 'by': 'research/kdiv1121/mkimg.py', 'out': 'img/00.png', 'topic': '고배당 ETF 5개 월 분배금',
           'num': f"{D['g']['104530']:.0f}% · {D['g']['161510']:.0f}%", 'topic_px': 46, 'num_px': 36,
           'follows': '경쟁 3 wisefather1113/224479160003 기간별 성적표(표·숫자 비교) — 같은 종류 차트, 다섯 개를 한 잣대로'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
L = ['161510', '279530', '104530', '466940', '0105E0']; LN = ['PLUS\n고배당주', 'KODEX\n고배당주', 'KIWOOM\n코리아고배당', 'TIGER 은행\n고배당플러스', 'SOL\n코리아고배당']
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
x = np.arange(5); w = 0.36
a0 = [D['a0'][c] or 0 for c in L]; a1 = [D['a1'][c] for c in L]
ax.bar(x - w / 2, a0, w, color=GRY, label='1년 전 같은 달'); ax.bar(x + w / 2, a1, w, color=[ORG if c == '161510' else BLUE for c in L], label='최근 달')
for xx, vv in zip(x - w / 2, a0):
    ax.text(xx, vv + 2, f'{vv:.0f}' if vv else '없음', ha='center', va='bottom', fontproperties=Bs(14), color=SUBC)
for xx, vv in zip(x + w / 2, a1): ax.text(xx, vv + 2, f'{vv:.0f}원', ha='center', va='bottom', fontproperties=Bs(15), color=INK)
ax.set_xticks(x); ax.set_xticklabels(LN, fontproperties=Bs(12.5)); ax.tick_params(axis='x', length=0, pad=6)
ax.set_yticks([]); ax.set_ylim(0, 145)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(prop=fm.FontProperties(fname=F + r'\pd500.ttf', size=13), frameon=False, loc='upper left', ncol=2)
frame(fig, '주당 월 분배금, 1년 전 같은 달과 최근 달(원)', '세금 떼기 전 · SOL은 2025년 11월 첫 분배라 1년 전 없음')
fig.subplots_adjust(top=0.82, bottom=0.18, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
o = sorted(L, key=lambda c: -D['m'][c]); nm = dict(zip(L, LN))
vals = [D['m'][c] / 1e4 for c in o]
ax.barh(range(5)[::-1], vals, color=[ORG if c == '161510' else BLUE for c in o], height=0.6)
for i, (c, vv) in enumerate(zip(o, vals)): ax.text(vv + 0.6, 4 - i, f'약 {round(vv):.0f}만원', va='center', fontproperties=Bs(17), color=INK)
ax.set_yticks(range(5)[::-1]); ax.set_yticklabels([nm[c].replace('\n', ' ') for c in o], fontproperties=Bs(14)); ax.tick_params(axis='y', length=0)
ax.set_xticks([]); ax.set_xlim(0, 70)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
frame(fig, '1억원어치 샀다면 한 달 분배금(세전)', f"최근 달 분배금이 그대로 나온다고 칠 때 · {D['day']} 종가로 산 주식 수")
fig.subplots_adjust(top=0.82, bottom=0.1, left=0.3, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'kdiv1121' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
