# gwanggyo1125 그림(sanbon1123 틀) — 00 표지(차트: 1년 같은 집 광교 vs 수지 오래된 단지), 01 넓이 나눠 1년, 02 2021년 하반기 대비. 숫자는 calc_out 그대로
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
BLUE, INK, SUBC, ORG, GREY = '#1D4ED8', '#111827', '#6B7280', '#EA580C', '#94A3B8'
SRC = '국토교통부 아파트 매매 실거래 · 수원 영통구·용인 수지구(11/25 받음, 취소된 거래 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 44
BG = '#334155'
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '광교 아파트 시세', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '1년 새 같은 집 오른 폭', fontproperties=Bs(38), color='#E2E8F0')
ax = fig.add_axes([0.06, 0.17, 0.88, 0.5]); ax.set_facecolor(BG)
vals = [18.1, 25.2]; labs = ['광교', '수지 오래된 단지']; txt = ['+18%', '+25%']
ax.bar(range(2), vals, color=['#FB923C', GREY], width=0.5)
for i in range(2):
    ax.text(i, vals[i] + 0.6, txt[i], ha='center', va='bottom', fontproperties=Bs(NUM_PX), color='white')
    ax.text(i, -0.8, labs[i], ha='center', va='top', fontproperties=Bs(26), color='white')
ax.set_ylim(-5.5, 32); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.07, 0.1, '같은 단지·같은 넓이 · 2025년 6~10월 → 2026년 6~10월 중간값', fontproperties=Bs(22), color='white')
fig.text(0.07, 0.045, '국토부 실거래 · 파이어맵 계산', fontsize=17, color='#E2E8F0')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(수원 영통구 41117·용인 수지구 41465) 2025.6~10월 vs 2026.6~10월 계약, calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-25', 'by': 'research/gwanggyo1125/mkimg.py', 'out': 'img/00.png', 'topic': '광교 아파트 시세', 'num': '+18% / +25%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 3 ladderprice/224484518660 동별 시세 표 · 4 rytesmy/224488941676 가격 비교 그림'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
import numpy as np
# 01 넓이 나눠 1년
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
groups = ['전용 60~85㎡', '85㎡ 넘는 집']; gw = [20.4, 15.4]; so = [28.5, 18.7]; yo = [16.7, 10.4]
x = np.arange(2); w = 0.26
ax.bar(x - w, gw, w, color='#FB923C', label='광교 수원 쪽'); ax.bar(x, so, w, color=GREY, label='수지 오래된 단지'); ax.bar(x + w, yo, w, color='#93C5FD', label='영통 오래된 단지')
for i in range(2):
    for dx, v in ((-w, gw[i]), (0, so[i]), (w, yo[i])):
        ax.text(x[i] + dx, v + 0.5, f'약 {int(v + 0.5)}%', ha='center', fontproperties=Bs(17), color=INK)
ax.set_xticks(x); ax.set_xticklabels(groups, fontproperties=Bs(17)); ax.set_yticks([]); ax.set_ylim(0, 36)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(prop=Bs(14), frameon=False, loc='upper right')
frame(fig, '넓이를 나눠도 비율은 수지 오래된 단지가 컸다', '같은 단지·같은 넓이 매매 중간값 · 2025년 6~10월 → 2026년 6~10월')
fig.subplots_adjust(top=0.82, bottom=0.14, left=0.06, right=0.97); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 2021년 하반기 대비
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
labs = ['광교 (75개 중 53개 넘음)', '수지 오래된 단지 (253개 중 208개)', '영통 오래된 단지 (94개 중 44개)']; v = [5.8, 14.7, -0.6]
y = list(range(3))[::-1]
ax.barh(y, v, color=['#FB923C', GREY, '#93C5FD'], height=0.55)
for yy, xx in zip(y, v): ax.text(max(xx, 0) + 0.4, yy, (f'약 +{round(xx)}%' if xx > 1 else '거의 같음'), va='center', ha='left', fontproperties=Bs(22), color=INK)
ax.set_yticks(y); ax.set_yticklabels(labs, fontproperties=Bs(15)); ax.tick_params(axis='y', length=0, pad=8)
ax.set_xticks([]); ax.set_xlim(-2, 22); ax.axvline(0, color=INK, lw=1)
for s in ('top', 'left', 'bottom', 'right'): ax.spines[s].set_visible(False)
frame(fig, '2021년 하반기 값과 비교하면', '같은 단지·같은 넓이 매매 중간값 · 2021년 7~12월 → 2026년 6~10월')
fig.subplots_adjust(top=0.82, bottom=0.08, left=0.38, right=0.97); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'gwanggyo1125' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok', [os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(p)))) for p in recent])
