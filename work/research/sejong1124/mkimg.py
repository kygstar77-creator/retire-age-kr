# sejong1124 그림(bundang1122 틀) — 00 표지(차트: 같은 집 2021년 상반기 대비·1년 대비), 01 동별 2021년 상반기 대비, 02 동 지역 84㎡ 반기 중간 가격. 숫자는 calc_out 그대로
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
BLUE, INK, SUBC, ORG = '#1D4ED8', '#111827', '#6B7280', '#EA580C'
SRC = '국토교통부 아파트 매매 실거래 · 세종특별자치시(11/22 받음, 취소된 거래 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 44
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#0F3D3E')
fig.text(0.07, 0.86, '세종 아파트 시세', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '같은 집 값이 얼마나 내렸나', fontproperties=Bs(38), color='#A7F3D0')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor('#0F3D3E')
vals = [-26.5, -0.6]; labs = ['2021년 상반기보다', '1년 전보다']; txt = ['-26.5%', '-0.6%']
ax.bar(range(2), vals, color=['#FB923C', '#94A3B8'], width=0.5)
for i in range(2):
    ax.text(i, vals[i] - 1.2, txt[i], ha='center', va='top', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, 1.2, labs[i], ha='center', va='bottom', fontproperties=Bs(26), color='white')
ax.set_ylim(-36, 8); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '같은 단지·같은 넓이 내린 폭의 중간값 · 올해 6~10월 계약 기준', fontproperties=Bs(22), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#A7F3D0')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(세종특별자치시 36110) 2021.1~6월·2025.6~10월 vs 2026.6~10월 계약, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-22', 'by': 'research/sejong1124/mkimg.py', 'out': 'img/00.png', 'topic': '세종 아파트 시세', 'num': '-26.5% / -0.6%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 4 ladderprice/224484586049 동별 시세 순위 차트 · 1 noonesejong/224484897012 실거래 표 그림'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
D = [('나성동', 24, -10.9), ('어진동', 11, -16.6), ('새롬동', 18, -19.9), ('보람동', 14, -23.7), ('소담동', 17, -24.2), ('도담동', 24, -25.1),
     ('다정동', 23, -25.5), ('종촌동', 20, -27.5), ('아름동', 15, -28.7), ('한솔동', 27, -28.8), ('반곡동', 11, -29.8), ('고운동', 37, -31.8)]
fig, ax = plt.subplots(figsize=(9, 8.4), dpi=100)
labs = [f'{u} ({n}개)' for u, n, _ in D]; v = [abs(x) for _, _, x in D]
y = list(range(len(labs)))[::-1]
ax.barh(y, v, color=[ORG if x in (min(v), max(v)) else '#93C5FD' for x in v], height=0.6)
for yy, x in zip(y, v): ax.text(x + 0.5, yy, f'-{x:.1f}%', va='center', fontproperties=Bs(17), color=INK)
ax.set_yticks(y); ax.set_yticklabels(labs, fontproperties=Bs(15)); ax.tick_params(axis='y', length=0, pad=8)
ax.set_xticks([]); ax.set_xlim(0, 39)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
frame(fig, '동별로 2021년 상반기보다 얼마나 아래인가', '같은 단지·같은 넓이 매매 중간값 · 2021년 1~6월 → 올해 6~10월 · 괄호는 비교한 평형 수')
fig.subplots_adjust(top=0.85, bottom=0.07, left=0.24, right=0.96); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
xs = [str(y) + chr(10) + h for y in range(2020, 2027) for h in ('상', '하')]
p = [4.85, 6.80, 7.60, 7.50, 6.70, 5.70, 5.80, 6.00, 5.75, 5.90, 5.88, 6.20, 6.20, 6.08]
ax.plot(range(len(p)), p, color=BLUE, lw=3, marker='o')
ax.text(2, p[2] + 0.18, '7억 6천', ha='center', fontproperties=Bs(16), color=ORG)
ax.text(len(p) - 1, p[-1] + 0.18, '6억 800만', ha='center', fontproperties=Bs(16), color=BLUE)
ax.text(0.25, p[0] + 0.15, '4억 8,500만', ha='left', fontproperties=Bs(14), color=SUBC)
ax.set_xticks(range(len(p))); ax.set_xticklabels(xs, fontsize=11); ax.set_yticks([4, 5, 6, 7, 8]); ax.set_yticklabels(['4억', '5억', '6억', '7억', '8억'], fontsize=12)
ax.set_xlim(-0.6, len(p) - 0.4); ax.set_ylim(4, 8.2)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
frame(fig, '동 지역 84㎡ 중간 가격, 2021년 상반기가 가장 높았다', '전용 83~86㎡ 반기별 중간 가격 · 상=1~6월, 하=7~12월(2026 하는 7~10월) · 읍·면 뺌')
fig.subplots_adjust(top=0.82, bottom=0.15, left=0.08, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [q for q in recent if 'sejong1124' not in q][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, q in enumerate(recent): board.paste(Image.open(q).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
