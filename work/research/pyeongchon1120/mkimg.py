# pyeongchon1120 그림(gwanggyo1118 틀) — 00 표지(차트 — 경쟁 3 chaekim4711 표지 '시세 요약' 꼴), 01 같은 평형 변화(두 기간×두 곳), 02 반기별 흐름. 숫자는 calc_out 그대로
import os, json, glob
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, INK, SUBC, ORG, BG = '#1D4ED8', '#111827', '#6B7280', '#EA580C', '#FFFFFF'
SRC = '국토교통부 아파트 매매 실거래 · 안양 동안구 평촌동·호계동(11/18 받음, 취소 거래 뺌) · 파이어맵 계산'
# 00 표지 — 주제어 줄 58pt > 숫자 줄 44pt
TOPIC_PX, NUM_PX = 58, 44
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#134E4A')
fig.text(0.07, 0.86, '평촌 아파트', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '옆 호계동보다 얼마나', fontproperties=Bs(38), color='#99F6E4')
ax = fig.add_axes([0.1, 0.17, 0.8, 0.5]); ax.set_facecolor('#134E4A')
vals = [21.9, 6.7]; labs = ['평촌동', '호계동']
ax.bar([0, 1], vals, color=['#FB923C', '#94A3B8'], width=0.55)
ax.axhline(0, color='white', lw=1.5)
for i, v in enumerate(vals):
    ax.text(i, v + 0.6, f'+{v:.0f}%', ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -0.6, labs[i], ha='center', va='top', fontproperties=Bs(30), color='white')
ax.set_ylim(-5, 30); ax.set_xlim(-0.6, 1.6); ax.axis('off')
fig.text(0.07, 0.1, '같은 단지·같은 넓이 · 2021년 하반기 대비 올해 6~10월', fontproperties=Bs(24), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#99F6E4')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(경기 안양 동안구 41173 평촌동·호계동) 2021.7~12월 vs 2026.6~10월 계약, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-18', 'by': 'research/pyeongchon1120/mkimg.py', 'out': 'img/00.png', 'topic': '평촌 아파트', 'num': '+22% · +7%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 3 chaekim4711/224475935231 30초 요약 표지'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def bars(fname, title, sub, groups, series, lo, hi):
    fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
    w = 0.36; cols = ['#93C5FD', BLUE]
    for j, (sl, vals, cnts) in enumerate(series):
        xs = [i + (j - 0.5) * w for i in range(len(groups))]
        ax.bar(xs, vals, width=w * 0.92, color=[cols[j] if v > 0 else (ORG if j else '#FDBA74') for v in vals], label=sl)
        for x, v, c in zip(xs, vals, cnts):
            ax.text(x, v + (1.2 if v > 0 else -1.2), f'{v:+.0f}%', ha='center', va='bottom' if v > 0 else 'top', fontproperties=Bs(19), color=INK)
            ax.text(x, (-1 if v > 0 else 1), f'{c}개', ha='center', va='top' if v > 0 else 'bottom', fontproperties=Bs(12), color=SUBC)
    ax.axhline(0, color=INK, lw=1)
    ax.set_xticks(range(len(groups))); ax.set_xticklabels(groups, fontproperties=Bs(16)); ax.tick_params(axis='x', length=0, pad=8)
    ax.set_yticks([]); ax.set_ylim(lo, hi)
    for s in ('top', 'right', 'left', 'bottom'): ax.spines[s].set_visible(False)
    ax.legend(prop=Bs(13), frameon=False, loc='upper left')
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10.5, color=SUBC)
    fig.subplots_adjust(top=0.82, bottom=0.12, left=0.04, right=0.98)
    fig.savefig(fname, dpi=100); plt.close(fig)
bars('pkg/img/01.png', '같은 단지·같은 넓이, 올해 6~10월은 그때보다 얼마나', '두 시기에 모두 팔린 단지·넓이 개수 · 중간값',
     ['평촌동', '호계동'], [('2021년 하반기보다', [21.9, 6.7], [33, 93]), ('2023년 상반기보다', [54.9, 37.2], [39, 98])], -8, 68)
# 02 반기별(2021H2 = 0)
H = ['21년 하', '22년 상', '22년 하', '23년 상', '23년 하', '24년 상', '24년 하', '25년 상', '25년 하', '26년 상', '26년 7~10월']
H = [h.replace(' ', chr(10), 1) for h in H]
C1 = [0, -3.6, -21.8, -20.7, -15.4, -16.1, -12.5, -7.3, 0.1, 11.8, 22.4]
C2 = [0, -4.7, -16.4, -22.1, -19.7, -18.5, -16.4, -13.8, -9.4, -1.8, 7.4]
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
ax.plot(range(len(H)), C1, color=ORG, lw=3.5, marker='o', label='평촌동')
ax.plot(range(len(H)), C2, color=SUBC, lw=3, marker='o', label='호계동')
ax.axhline(0, color=INK, lw=1, ls='--')
ax.text(2, C1[2] - 1.5, f'{C1[2]:.0f}%', ha='center', va='top', fontproperties=Bs(15), color=ORG)
ax.text(10, C1[10] + 1.5, f'+{C1[10]:.0f}%', ha='center', va='bottom', fontproperties=Bs(15), color=ORG)
ax.set_xticks(range(len(H))); ax.set_xticklabels(H, fontsize=10.5)
ax.set_ylim(-30, 28); ax.set_yticks([20, 0, -10, -20]); ax.set_yticklabels(['+20%', '기준', '-10%', '-20%'], fontsize=12)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.legend(prop=Bs(14), frameon=False, loc='upper left')
fig.text(0.04, 0.93, '같은 단지·같은 넓이, 2021년 하반기를 0으로 놓고 본 흐름', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.88, '상=1~6월, 하=7~12월 · 반기마다 2021년 7~12월과 같은 단지·같은 넓이로 짝지은 중간값', fontsize=13.5, color=SUBC)
fig.text(0.04, 0.025, SRC, fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.1, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
# 100px 축소본·최근 10장 옆에 놓은 판
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'pyeongchon1120' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white')
board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png')
print('ok', [os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(p)))) for p in recent])
