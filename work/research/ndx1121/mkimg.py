# ndx1121 그림(divbear1121 틀) — 00 표지(차트: 지난 15번 1년 뒤), 01 15번 1년 뒤 등락, 02 더 빠진 깊이·되찾은 기간. 숫자는 calc_out.txt 그대로
import os, json, ast
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, GRAY = '#111827', '#6B7280', '#EA580C', '#9CA3AF'
SRC = '야후 파이낸스 나스닥100 일별 종가(11/20 받음, FRED와 대조) · 파이어맵 계산'
ev = [ast.literal_eval(l) for l in open('calc_out.txt', encoding='utf-8') if l.startswith('{')]
past = [e for e in ev if e['y1'] is not None]
yrs = [e['hit'][:7].replace('-', '.') for e in past]; y1 = [e['y1'] for e in past]
TOPIC_PX, NUM_PX = 56, 46
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#262626')
fig.text(0.07, 0.86, '나스닥100 -15%', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.77, '지난 15번, 1년 뒤는?', fontproperties=Bs(36), color='#D4D4D4')
ax = fig.add_axes([0.06, 0.2, 0.88, 0.48]); ax.set_facecolor('#262626')
ax.bar(range(15), y1, color=['#FB923C' if v > 0 else '#94A3B8' for v in y1], width=0.7)
ax.axhline(0, color='white', lw=1.2); ax.set_ylim(-70, 150); ax.axis('off')
ax.text(7, 122, '13번 오름 · 중간 +30.9%', ha='center', fontproperties=Bs(NUM_PX), color='white')
fig.text(0.07, 0.11, '내린 2번: 2000년 -60.0%, 2022년 -13.1%', fontproperties=Bs(25), color='white')
fig.text(0.07, 0.045, '야후 파이낸스·FRED 지수 · 파이어맵 계산', fontsize=17, color='#D4D4D4')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 chart API ^NDX 일별 종가 1985-10~2026-11-19(FRED NASDAQ100과 대조), 직전 최고 대비 처음 -15% 닿은 날 1년 뒤 등락 — calc_out.txt 파이어맵 직접 계산',
           'made_at': '2026-11-20', 'by': 'research/ndx1121/mkimg.py', 'out': 'img/00.png', 'topic': '나스닥100 -15%', 'num': '13번 오름 · 중간 +30.9%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 jpo03664/224480364227 짙은 남색 바탕·하락 차트 위 큰 글자 표지 (캐릭터 대신 실제 막대)'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
x = np.arange(15)
# 01 1년 뒤
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.bar(x, y1, color=[ORG if v > 0 else GRAY for v in y1], width=0.7)
for i, v in enumerate(y1): ax.text(i, v + (2 if v > 0 else -9), f'{v:+.0f}', ha='center', fontproperties=Bs(12), color=INK)
ax.axhline(0, color=INK, lw=1); ax.set_xticks(x); ax.set_xticklabels(yrs, rotation=60, fontsize=11); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(-72, 122)
for s_ in ('top', 'right', 'left', 'bottom'): ax.spines[s_].set_visible(False)
frame(fig, '-15% 처음 닿은 날 사서 1년 들고 있었다면(%)', '1985년 10월~2026년 11월 19일 · 직전 최고 대비 처음 -15% 닿은 날 종가 → 1년 뒤 종가')
fig.subplots_adjust(top=0.83, bottom=0.16, left=0.03, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 더 빠진 깊이와 되찾은 기간
dd = [e['lowdd'] for e in past]; mo = [e['recdays'] / 30.44 for e in past]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.bar(x, dd, color=['#1E3A5F' if v <= -20 else '#93C5FD' for v in dd], width=0.7)
ax.axhline(-15, color=ORG, lw=1.5, ls='--'); ax.text(-0.6, -13.5, '-15%', ha='left', fontproperties=Bs(12), color=ORG)
for i, v in enumerate(dd):
    lab = f'{v:.0f}%'; m = mo[i]
    ax.text(i, v - 3.5, lab, ha='center', va='top', fontproperties=Bs(11), color=INK)
    ax.text(i, 3, (f'{m:.0f}달' if m < 24 else f'{m/12:.1f}년'), ha='center', fontproperties=Bs(11), color=ORG if m >= 12 else SUBC)
ax.set_xticks(x); ax.set_xticklabels(yrs, rotation=60, fontsize=11); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(-95, 12)
for s_ in ('top', 'right', 'left', 'bottom'): ax.spines[s_].set_visible(False)
frame(fig, '그 뒤 가장 깊이 빠진 폭과 최고를 되찾기까지', '막대 = 직전 최고 대비 바닥(%) · 위 숫자 = -15% 닿은 날부터 직전 최고 다시 넘은 날까지')
fig.subplots_adjust(top=0.83, bottom=0.16, left=0.03, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
import glob
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'ndx1121' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
