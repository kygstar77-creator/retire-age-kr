# forenon1128 그림 — 00 표지(차트: 84㎡ 기간 묶음 중간 가격 3막대), 01 달별 매매 신고 건수, 02 강동 새 아파트 84㎡ 3칸 표. 숫자는 calc_out.txt에서 읽는다(손으로 옮기지 않음)
import os, json, re, glob
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG = '#111827', '#6B7280', '#EA580C'
SRC = '국토교통부 아파트 매매 실거래 · 서울 강동구 · 2024년 11월~2026년 11월 계약(11/27 받음, 취소 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 50, 40
txt = open('calc_out.txt', encoding='utf-8').read()
m84 = re.search(r'포레온 84㎡대 \d+건: (.*)', txt).group(1)
d24 = float(re.search(r'2024-12 3건 가운데 ([\d.]+)억', m84).group(1))
h1 = float(re.search(r'84㎡대 2026-04~06 38건 가운데 ([\d.]+)억', txt).group(1))
h2 = float(re.search(r'84㎡대 2026-08~11 16건 가운데 ([\d.]+)억', txt).group(1))
assert (d24, h1, h2) == (22.08, 28.00, 29.70), (d24, h1, h2)
total = int(re.search(r'취소 뺌\) 2024-11~2026-11-27 받은 날까지: (\d+)건', txt).group(1)); assert total == 145
BG = '#1F3B34'
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '올림픽파크포레온 34평', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.775, '실거래 중간 가격, 기간마다', fontproperties=Bs(30), color='#D1E7DD')
ax = fig.add_axes([0.08, 0.30, 0.84, 0.40]); ax.set_facecolor(BG)
labs = ['24년 12월', '26년 4~6월', '26년 8~11월']; v = [d24, h1, h2]
ax.bar(range(3), v, color=['#7FA89A', '#7FA89A', '#FB923C'], width=0.58)
for i, y in enumerate(v):
    ax.text(i, y + 0.5, f'{y:.2f}억', ha='center', fontproperties=Bs(26), color='white')
    ax.text(i, 15.2, labs[i], ha='center', fontproperties=Bs(20), color='#D1E7DD', clip_on=False)
ax.set_ylim(16, 33); ax.set_xlim(-0.6, 2.6); ax.axis('off')
fig.text(0.07, 0.19, f'입주 2년, 매매 신고 {total}건', fontproperties=Bs(NUM_PX), color='white')
fig.text(0.07, 0.125, '그중 97건이 올해 4~5월', fontproperties=Bs(28), color='#FDBA74')
fig.text(0.07, 0.05, '국토부 실거래(11/27 조회) · 파이어맵 계산', fontsize=17, color='#D1E7DD')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(서울 강동구 11740, 올림픽파크포레온) 2024-11~2026-11 계약, 취소 뺌, 전용 84㎡대 기간 묶음 중간 가격 — calc_out.txt, 파이어맵 직접 계산',
           'made_at': '2026-11-27', 'by': 'research/forenon1128/mkimg.py', 'out': 'img/00.png', 'topic': '올림픽파크포레온 34평', 'num': f'입주 2년, 매매 신고 {total}건',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 3 rkddnjs73/224482324957(입주 이후 실거래가 차트 표지)·8 ziplab365/224488885909(34평 숫자 썸네일)'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=8.0, color=SUBC)
# 01 달별 매매 신고 건수
mc = dict((k, int(v)) for k, v in re.findall(r'(\d{4}-\d\d) (\d+)', re.search(r'달별: (.*)', txt).group(1)))
ms = []; y, m = 2024, 12
while (y, m) <= (2026, 11):
    ms.append(f'{y}-{m:02d}'); m += 1
    if m == 13: y, m = y + 1, 1
cnt = [mc.get(k, 0) for k in ms]; assert sum(cnt) == total and cnt[ms.index('2026-04')] + cnt[ms.index('2026-05')] == 97, cnt
fig = plt.figure(figsize=(9, 6), dpi=100)
frame(fig, '올림픽파크포레온 매매, 계약한 달별 건수', '2025년은 4건 — 등기 전이라 입주권·분양권 거래로 따로 신고(헤럴드경제 보도)')
ax = fig.add_axes([0.06, 0.12, 0.90, 0.68])
cols = [ORG if k in ('2026-04', '2026-05') else '#94A3B8' for k in ms]
ax.bar(range(len(ms)), cnt, color=cols, width=0.66)
for i, c in enumerate(cnt):
    if c: ax.text(i, c + 0.8, str(c), ha='center', fontproperties=Bs(13), color=ORG if cols[i] == ORG else INK)
ax.set_xticks([i for i, k in enumerate(ms) if k[5:] in ('01', '04', '07', '10', '12')])
ax.set_xticklabels([k[2:4] + '.' + k[5:] for k in ms if k[5:] in ('01', '04', '07', '10', '12')], fontsize=10.5, color=SUBC)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.set_yticks([]); ax.set_ylim(0, 66)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 강동 새 아파트 84㎡ 표(3칸)
rows = []
for apt in ['고덕그라시움', '고덕아르테온', '래미안힐스테이트고덕']:
    mm = re.search(apt + r'\((\d{4})\) 84㎡대: 2025-04~06 (\d+)건 ([\d.]+)억 · 2026-04~06 (\d+)건 ([\d.]+)억', txt)
    rows.append((f'{apt}({mm.group(1)})', f'{float(mm.group(3)):.2f}억', f'{float(mm.group(5)):.2f}억'))
rows.insert(0, ('올림픽파크포레온(2024)', '기록 없음', f'{h1:.2f}억'))
assert rows[1][2] == '24.00억' and rows[0][2] == '28.00억', rows
fig = plt.figure(figsize=(9, 2.3 + 0.62 * len(rows)), dpi=100)
frame(fig, '강동 새 아파트 84㎡대, 4~6월 중간 가격', '같은 석 달 계약끼리 · 괄호는 준공 해')
h = fig.get_figheight(); step = 0.62 / h; yy0 = 1 - 1.55 / h; xs = (0.05, 0.52, 0.76)
for x, t in zip(xs, ('단지', '2025년', '2026년')): fig.text(x, yy0, t, fontproperties=Bs(17), color=SUBC)
fig.add_artist(plt.Line2D([0.04, 0.96], [yy0 - 0.18 / h, yy0 - 0.18 / h], color='#CBD5E1', lw=1.5))
for i, r in enumerate(rows):
    for x, t in zip(xs, r): fig.text(x, yy0 - step * (i + 1), t, fontproperties=Bs(19), color=ORG if i == 0 else INK)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'forenon1128' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
