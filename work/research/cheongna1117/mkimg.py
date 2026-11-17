# cheongna1117 그림 — 00 표지(차트 — 경쟁 1 kyuseokworld 표지가 실거래 막대 차트), 01 같은 평형 변화(두 기간×두 곳), 02 반기별 흐름. 숫자는 calc_out 그대로
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
SRC = '국토교통부 아파트 매매 실거래 · 인천 청라동·검단 쪽 9개 동(11/17 받음, 취소 거래 뺌) · 파이어맵 계산'
# 00 표지 — 주제어 줄 58pt > 숫자 줄 44pt
TOPIC_PX, NUM_PX = 58, 44
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#0F2A5C')
fig.text(0.07, 0.86, '청라 아파트', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '고점 회복 얼마나 남았나', fontproperties=Bs(38), color='#BFDBFE')
ax = fig.add_axes([0.1, 0.17, 0.8, 0.5]); ax.set_facecolor('#0F2A5C')
vals = [-14.0, -17.4]; labs = ['청라동', '검단 쪽']
ax.bar([0, 1], vals, color=['#FB923C', '#94A3B8'], width=0.55)
ax.axhline(0, color='white', lw=1.5)
for i, v in enumerate(vals):
    ax.text(i, v - 1.2, f'{v:.0f}%', ha='center', va='top', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, 1.2, labs[i], ha='center', va='bottom', fontproperties=Bs(30), color='white')
ax.set_ylim(-30, 7); ax.set_xlim(-0.6, 1.6); ax.axis('off')
fig.text(0.07, 0.1, '같은 평형 · 2021년 하반기 대비 올해 6~10월', fontproperties=Bs(24), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(인천 28275 청라동·28290 9개 동) 2021.7~12월 vs 2026.6~10월 계약, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-17', 'by': 'research/cheongna1117/mkimg.py', 'out': 'img/00.png', 'topic': '청라 아파트', 'num': '-14% · -17%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 kyuseokworld/224477708235 표지(실거래 막대 차트)'},
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
    ax.legend(prop=Bs(13), frameon=False, loc='upper right')
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10.5, color=SUBC)
    fig.subplots_adjust(top=0.82, bottom=0.12, left=0.04, right=0.98)
    fig.savefig(fname, dpi=100); plt.close(fig)
bars('pkg/img/01.png', '같은 평형, 올해 6~10월은 그때보다 얼마나', '같은 단지·같은 넓이 집이 두 시기에 모두 팔린 단지·평형 수 · 가운데 값',
     ['청라동', '검단 쪽 9개 동'], [('2021년 하반기보다', [-14.0, -17.4], [72, 151]), ('2023년 상반기보다', [9.9, 7.9], [78, 185])], -26, 30)
# 02 반기별(2021H2 = 0)
H = ['21년 하', '22년 상', '22년 하', '23년 상', '23년 하', '24년 상', '24년 하', '25년 상', '25년 하', '26년 상', '26년 7~10월']
H = [h.replace(' ', chr(10), 1) for h in H]
C1 = [0, -2.4, -23.0, -22.5, -17.6, -17.1, -14.5, -14.8, -15.0, -14.3, -13.5]
C2 = [0, 0.8, -11.1, -19.2, -18.3, -17.2, -15.4, -15.9, -16.3, -16.8, -17.3]
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
ax.plot(range(len(H)), C1, color=ORG, lw=3.5, marker='o', label='청라동')
ax.plot(range(len(H)), C2, color=SUBC, lw=3, marker='o', label='검단 쪽 9개 동')
ax.axhline(0, color=INK, lw=1, ls='--')
ax.text(2, C1[2] - 1.5, f'{C1[2]:.0f}%', ha='center', va='top', fontproperties=Bs(15), color=ORG)
ax.set_xticks(range(len(H))); ax.set_xticklabels(H, fontsize=10.5)
ax.set_ylim(-28, 5); ax.set_yticks([0, -10, -20]); ax.set_yticklabels(['고점', '-10%', '-20%'], fontsize=12)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.legend(prop=Bs(14), frameon=False, loc='lower right')
fig.text(0.04, 0.93, '같은 평형, 2021년 하반기를 0으로 놓고 본 흐름', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.88, '상=1~6월, 하=7~12월 · 반기마다 2021년 7~12월과 같은 단지·같은 넓이로 짝지은 가운데 값', fontsize=13.5, color=SUBC)
fig.text(0.04, 0.025, SRC, fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.1, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
# 100px 축소본·최근 10장 옆에 놓은 판
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'cheongna1117' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white')
board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png')
print('ok', [os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(p)))) for p in recent])
