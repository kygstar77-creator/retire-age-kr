# geomdan1125 그림(sejong1124 틀) — 00 표지(차트: 84㎡ 중간 가격 1년 vs 같은 집 1년), 01 새 단지·옛 단지 84㎡ 1년 전 vs 지금, 02 84㎡ 반기 중간 가격 새·옛·전체. 숫자는 calc_out 그대로
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
BLUE, INK, SUBC, ORG, GRAY = '#1D4ED8', '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = '국토교통부 아파트 매매 실거래 · 인천 검단(당하·원당·마전·불로·왕길동 등, 11/25 받음, 취소된 거래 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 44
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#0F3D3E')
fig.text(0.07, 0.86, '검단 아파트 시세', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '1년 새 정말 1억 올랐나', fontproperties=Bs(38), color='#A7F3D0')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor('#0F3D3E')
vals = [26.0, -1.1]; labs = ['84㎡ 중간 가격', '같은 집끼리']; txt = ['+26%', '-1.1%']
ax.bar(range(2), vals, color=['#FB923C', GRAY], width=0.5)
ax.text(0, vals[0] + 1.2, txt[0], ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
ax.text(1, vals[1] - 1.2, txt[1], ha='center', va='top', fontproperties=Bs(NUM_PX), color='white')
ax.text(0, -1.5, labs[0], ha='center', va='top', fontproperties=Bs(26), color='white')
ax.text(1, 1.2, labs[1], ha='center', va='bottom', fontproperties=Bs(26), color='white')
ax.set_ylim(-12, 38); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '2025년 6~10월 → 2026년 6~10월 계약 기준', fontproperties=Bs(22), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#A7F3D0')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(인천 28290 검단) 2025.6~10월 vs 2026.6~10월 계약, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-24', 'by': 'research/geomdan1125/mkimg.py', 'out': 'img/00.png', 'topic': '검단 아파트 시세', 'num': '+26% / -1.1%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 7 ladderprice/224484580902 동별 시세 순위 차트 · 4 kyuseokworld/224477739353 30평대 TOP20 표 그림'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=9.5, color=SUBC)
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)
G = [('새 단지\n(2019년 이후 준공)', 6.07, 6.00), ('오래된 단지', 3.26, 3.15), ('검단 전체', 4.05, 5.10)]
w = 0.36
for i, (lab, a, b) in enumerate(G):
    ax.bar(i - w/2, a, w, color=GRAY); ax.bar(i + w/2, b, w, color=ORG if i == 2 else BLUE)
    ax.text(i - w/2, a + 0.08, f'{a:.2f}억', ha='center', fontproperties=Bs(15), color=SUBC)
    ax.text(i + w/2, b + 0.08, f'{b:.2f}억', ha='center', fontproperties=Bs(15), color=ORG if i == 2 else BLUE)
ax.set_xticks(range(3)); ax.set_xticklabels([g[0] for g in G], fontproperties=Bs(15)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(0, 7.2)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.text(2, 5.75, '새 단지 비중\n47% → 58%', ha='center', fontproperties=Bs(15), color=INK)
ax.bar([0], [0], color=GRAY, label='2025년 6~10월'); ax.bar([0], [0], color=BLUE, label='2026년 6~10월'); ax.legend(frameon=False, loc='upper right', fontsize=12, bbox_to_anchor=(0.78, 1.0))
frame(fig, '새 단지도 오래된 단지도 그대로인데 전체만 올랐다', '전용 83~86㎡ 매매 중간 가격 · 전체가 오른 건 비싼 새 단지 거래 비중이 늘어서')
fig.subplots_adjust(top=0.84, bottom=0.12, left=0.04, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
xs = [str(y) + chr(10) + h for y in range(2020, 2027) for h in ('상', '하')]
allp = [2.58, 2.64, 3.25, 3.95, 3.85, 3.70, 3.20, 3.37, 3.50, 3.60, 3.50, 4.73, 5.00, 5.10]
old = [2.58, 2.64, 3.25, 3.95, 3.80, 3.20, 3.04, 3.15, 3.15, 3.18, 3.20, 3.25, 3.20, 3.15]
new = [None, None, None, None, None, 4.37, 4.50, 5.90, 6.00, 6.50, 6.10, 6.03, 6.20, 5.99]
ax.plot(range(14), old, color=GRAY, lw=3, marker='o', label='오래된 단지')
ax.plot(range(5, 14), new[5:], color=BLUE, lw=3, marker='o', label='새 단지(2019년 이후 준공)')
ax.plot(range(14), allp, color=ORG, lw=2.5, ls='--', marker='s', label='검단 전체')
ax.text(13.2, 5.32, '전체 5억 1,000만', ha='right', fontproperties=Bs(14), color=ORG)
ax.text(9.4, 4.15, '2025년 하반기\n새 단지 비중 절반', ha='center', fontproperties=Bs(13), color=INK)
ax.set_xticks(range(14)); ax.set_xticklabels(xs, fontsize=11); ax.set_yticks([2, 3, 4, 5, 6, 7]); ax.set_yticklabels(['2억', '3억', '4억', '5억', '6억', '7억'], fontsize=12)
ax.set_xlim(-0.6, 13.4); ax.set_ylim(2, 7.2); ax.legend(frameon=False, loc='upper left', fontsize=12)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
frame(fig, '84㎡ 중간 가격, 묶음마다 따로 보면', '전용 83~86㎡ 반기별 중간 가격 · 상=1~6월, 하=7~12월(2026 하는 7~11월) · 새 단지는 2022년 하반기부터')
fig.subplots_adjust(top=0.82, bottom=0.15, left=0.08, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [q for q in recent if 'geomdan1125' not in q][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, q in enumerate(recent): board.paste(Image.open(q).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
