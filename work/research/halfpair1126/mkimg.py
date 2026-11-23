# halfpair1126 그림(banpopair1123 틀) — 00 표지(차트: 고점 대비 값 비율 점, 절반 이하 2건), 01 60% 이하 27건 해마다(3칸 표), 02 해마다 직거래 비율 막대. 숫자는 calc_out_1124.txt 그대로
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
INK, SUBC, ORG, GRY = '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = '국토교통부 아파트 매매 실거래 · 인천 연수구 송도동 전용 84㎡대(11/24 받음, 해제 거래 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 54, 40
# 00 표지 — 반값 2건 막대
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#1E3A5F')
fig.text(0.07, 0.86, '송도 84㎡ 반값 거래', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.77, '2022년 7월 이후 4,297건을 셌어요', fontproperties=Bs(30), color='#BFDBFE')
ax = fig.add_axes([0.08, 0.32, 0.84, 0.36]); ax.set_facecolor('#1E3A5F')
ax.barh([1, 0], [100, 100], color='#334E73', height=0.5)
ax.barh([1, 0], [46, 50], color='#FB923C', height=0.5)
ax.text(2, 1.42, '금호어울림 3.3억', fontproperties=Bs(28), color='white')
ax.text(2, 0.42, '더샵센트럴시티 4.8억', fontproperties=Bs(28), color='white')
ax.text(47, 1, ' 고점의 46%', va='center', fontproperties=Bs(26), color='white')
ax.text(51, 0, ' 고점의 50%', va='center', fontproperties=Bs(26), color='white')
ax.set_xlim(0, 100); ax.set_ylim(-0.5, 1.8); ax.axis('off')
fig.text(0.07, 0.17, '4,297건 중 2건', fontproperties=Bs(NUM_PX), color='white')
fig.text(0.07, 0.11, '둘 다 직거래', fontproperties=Bs(28), color='#FDBA74')
fig.text(0.07, 0.05, '국토부 실거래(11/24 조회) · 파이어맵 계산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(인천 연수구 28185 송도동) 2022-07 이후 계약 전용 84㎡대 4,297건 중 단지 고점 반기 가운데 값의 절반 이하 2건, calc_out_1124.txt §4 — 파이어맵 직접 계산',
           'made_at': '2026-11-24', 'by': 'research/halfpair1126/mkimg.py', 'out': 'img/00.png', 'topic': '송도 84㎡ 반값 거래', 'num': '4,297건 중 2건',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 songdo-life/224474951053·2 ssss6424/224487234023 실거래 표·차트'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=9.5, color=SUBC)
# 01 60% 이하 27건 해마다 — 3칸 표
rows = [('2022년(7~12월)', '6건', '5건'), ('2023년', '9건', '7건'), ('2024년', '3건', '2건'), ('2025년', '3건', '2건'), ('2026년(~11월)', '6건', '5건'), ('합계', '27건', '21건')]
fig = plt.figure(figsize=(9, 6.4), dpi=100)
frame(fig, '고점의 60% 이하로 팔린 거래 27건', '그 단지 고점 가운데 값의 60% 이하 · 그중 21건이 직거래')
xs = [0.06, 0.52, 0.76]; y = 0.78
for x, h in zip(xs, ('계약한 해', '60% 이하', '그중 직거래')): fig.text(x, y, h, fontproperties=Bs(18), color=SUBC)
fig.add_artist(plt.Line2D([0.04, 0.96], [y - 0.025, y - 0.025], color='#CBD5E1', lw=1.5))
for i, r in enumerate(rows):
    yy = y - 0.1 * (i + 1); last = i == len(rows) - 1
    for x, v in zip(xs, r): fig.text(x, yy, v, fontproperties=Bs(21), color=ORG if last else INK)
    if last: fig.add_artist(plt.Line2D([0.04, 0.96], [yy + 0.065, yy + 0.065], color='#CBD5E1', lw=1.5))
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 해마다 직거래 비율
yrs = ['2022년\n7~12월', '2023년', '2024년', '2025년', '2026년\n~11월']; d = [9.0, 3.3, 2.0, 2.5, 3.0]
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
ax.bar(range(5), d, width=0.55, color=[ORG, '#CBD5E1', '#CBD5E1', '#CBD5E1', '#CBD5E1'])
for i, v in enumerate(d): ax.text(i, v + 0.2, f'{v:.1f}%', ha='center', va='bottom', fontproperties=Bs(20), color=INK)
ax.set_xticks(range(5)); ax.set_xticklabels(yrs, fontproperties=Bs(14)); ax.tick_params(axis='x', length=0, pad=8)
ax.set_yticks([]); ax.set_ylim(0, 11)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
frame(fig, '84㎡대 거래 중 직거래 비율, 해마다', '중개사 없이 당사자끼리 계약한 거래 · 전체 4,297건 중 131건(3.0%)')
fig.subplots_adjust(top=0.82, bottom=0.16, left=0.04, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'halfpair1126' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
