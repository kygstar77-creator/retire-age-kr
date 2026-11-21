# wirye1123 그림(bundang1122 틀) — 00 표지(차트: 1년 같은 집 송파·성남·하남 위례), 01 84㎡ 중간 가격 1년 전 vs 올해, 02 한 달 평균 매매 건수 대책 전·후. 숫자는 calc_out 그대로
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
SRC = '국토교통부 아파트 매매 실거래 · 송파구·성남시 수정구·하남시 위례 단지 36곳(11/22 받음, 취소된 거래 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 44
BG = '#134E4A'
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '위례 아파트 시세', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '1년 새 같은 집 오른 폭', fontproperties=Bs(38), color='#99F6E4')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor(BG)
vals = [27.2, 23.7, 23.0]; labs = ['송파 쪽', '성남 쪽', '하남 쪽']; txt = ['+27%', '+24%', '+23%']
ax.bar(range(3), vals, color=['#FB923C', '#5EEAD4', '#5EEAD4'], width=0.55)
for i in range(3):
    ax.text(i, vals[i] + 0.8, txt[i], ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -1, labs[i], ha='center', va='top', fontproperties=Bs(28), color='white')
ax.set_ylim(-7, 35); ax.set_xlim(-0.6, 2.6); ax.axis('off')
fig.text(0.07, 0.1, '같은 단지·같은 넓이 · 작년 6~10월 → 올해 6~10월 중간값', fontproperties=Bs(22), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#99F6E4')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(서울 송파구 11710·성남시 수정구 41131·하남시 41450, 이름에 위례 든 36개 단지) 2025.6~10월 vs 2026.6~10월 계약, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-22', 'by': 'research/wirye1123/mkimg.py', 'out': 'img/00.png', 'topic': '위례 아파트 시세', 'num': '+27% / +24% / +23%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 economy_nya/224477862794 숫자 먼저(23억) · 경쟁 4 kokoko9ko/224481718361 송파·성남·하남 나눠 보기'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['송파 쪽 (올해 3건)', '성남 쪽 (27건)', '하남 쪽 (16건)']; a = [17.48, 14.70, 13.25]; b = [21.60, 18.40, 16.68]
t_a = ['약 17억 5천', '약 14억 7천', '약 13억 3천']; t_b = ['약 21억 6천', '약 18억 4천', '약 16억 7천']
y = [2, 1, 0]
ax.barh([v + 0.18 for v in y], a, height=0.34, color='#CBD5E1', label='작년 6~10월')
ax.barh([v - 0.18 for v in y], b, height=0.34, color=ORG, label='올해 6~10월')
for yy, x1, x2, s1, s2 in zip(y, a, b, t_a, t_b):
    ax.text(x1 + 0.2, yy + 0.18, s1, va='center', fontsize=13, color=SUBC)
    ax.text(x2 + 0.2, yy - 0.18, s2, va='center', fontproperties=Bs(16), color=INK)
ax.set_yticks(y); ax.set_yticklabels(labs, fontproperties=Bs(16)); ax.tick_params(axis='y', length=0, pad=8)
ax.set_xticks([]); ax.set_xlim(0, 27); ax.legend(loc='lower left', bbox_to_anchor=(0.0, 0.98), ncol=2, frameon=False, fontsize=12)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
frame(fig, '84㎡ 중간 가격, 순서는 그대로', '전용 83~86㎡ 매매 중간값 · 그때 팔린 단지에 따라 흔들림(송파 쪽은 올해 3건)')
fig.subplots_adjust(top=0.82, bottom=0.08, left=0.27, right=0.96); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['송파 쪽', '성남 쪽', '하남 쪽']; a = [13, 58, 44]; b = [6, 12, 13]
x = range(3)
ax.bar([i - 0.2 for i in x], a, width=0.38, color='#CBD5E1', label='작년 7~9월(대책 전)')
ax.bar([i + 0.2 for i in x], b, width=0.38, color=ORG, label='올해 6~10월')
for i in x:
    ax.text(i - 0.2, a[i] + 1, f'{a[i]}건', ha='center', fontsize=14, color=SUBC)
    ax.text(i + 0.2, b[i] + 1, f'{b[i]}건', ha='center', fontproperties=Bs(16), color=INK)
ax.set_xticks(list(x)); ax.set_xticklabels(labs, fontproperties=Bs(17)); ax.set_yticks([]); ax.set_ylim(0, 68)
ax.legend(loc='upper right', frameon=False, fontsize=12)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
frame(fig, '한 달에 팔린 위례 아파트, 대책 뒤 크게 줄었다', '한 달 평균 매매 건수 · 2025년 10월 20일부터 세 곳 모두 토지거래허가구역')
fig.subplots_adjust(top=0.82, bottom=0.15, left=0.06, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'wirye1123' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
