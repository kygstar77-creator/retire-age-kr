# ndxrecon1127 그림 — 00 표지(12월마다 새로 들어온 회사 수), 01 들어왔다 나간 회사, 02 올해 12월 일정. 숫자는 count_out.txt(나스닥 발표문 7건+6월 분기)
import os, json, glob, sys, datetime as D
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, NAVY = '#111827', '#6B7280', '#EA580C', '#0F2A44'
SRC = '나스닥 연례 교체 발표문 2019~2025 · 2026년 6월 분기 발표 · 나스닥100 규칙 문서(2026.5)'
TOPIC_PX, NUM_PX = 58, 40
yrs = [2019, 2020, 2021, 2022, 2023, 2024, 2025]; add = [6, 6, 6, 6, 6, 3, 6]
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(NAVY)
fig.text(0.07, 0.86, '나스닥100 종목 교체', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.785, '12월마다 새로 들어온 회사 수', fontproperties=Bs(32), color='#FED7AA')
ax = fig.add_axes([0.06, 0.2, 0.88, 0.52]); ax.set_facecolor(NAVY)
ax.bar(range(7), add, color=['#FB923C' if a != 3 else '#94A3B8' for a in add], width=0.62)
for i, a in enumerate(add):
    ax.text(i, a + 0.15, f'{a}개', ha='center', va='bottom', fontproperties=Bs(26), color='white')
    ax.text(i, -0.3, f"'{str(yrs[i])[2:]}", ha='center', va='top', fontproperties=Bs(24), color='white')
ax.set_ylim(-1.6, 8.2); ax.set_xlim(-0.6, 6.6); ax.axis('off')
fig.text(0.07, 0.1, f'7년 동안 {sum(add)}개가 새로 들어왔다', fontproperties=Bs(NUM_PX - 8), color='white')
fig.text(0.07, 0.045, '나스닥 12월 연례 교체 발표문 7건 · 2026년 6월 분기 심사는 따로 5개', fontsize=17, color='#FED7AA')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '나스닥 Annual Changes to the Nasdaq-100 Index 발표문 2019~2025(raw/pr20xx.html)에서 count.py로 센 12월 새로 넣은 회사 수, count_out.txt',
           'made_at': str(D.date.today()), 'by': 'research/ndxrecon1127/mkimg.py', 'out': 'img/00.png', 'topic': '나스닥100 종목 교체',
           'num': f'7년 {sum(add)}개 · 해마다 6개(2024년 3개)', 'topic_px': TOPIC_PX, 'num_px': NUM_PX,
           'follows': '경쟁 2 whitecoffee0528 대표 썸네일(글자 카드+핵심 숫자 3주) · 경쟁 3 sovbks 표지(나스닥100선물 글자) + 우리 잘된 글 ndxetf1122·k200etf1126 막대 위 큰 숫자 차트 표지'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 들어왔다 나간 회사 — 가로 줄(해 칸) 위에 들어옴●·빠짐×
rows = [('CDW', [(2019, 'in'), (2021, 'out'), (2023, 'in'), (2025, 'out')]),
        ('매치그룹', [(2020, 'in'), (2022, 'out')]),
        ('루시드', [(2021, 'in'), (2023, 'out')]),
        ('지스케일러', [(2021, 'in'), (2026.45, 'out')]),
        ('글로벌파운드리스', [(2022, 'in'), (2025, 'out')]),
        ('인스메드', [(2025, 'in'), (2026.45, 'out')])]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
for k, (nm, ev) in enumerate(rows):
    y = len(rows) - 1 - k
    ax.text(2018.55, y, nm, ha='right', va='center', fontproperties=Bs(15), color=INK)
    ax.plot([2018.8, 2026.7], [y, y], color='#E5E7EB', lw=1, zorder=0)
    for a, b in zip(ev, ev[1:]):
        if a[1] == 'in': ax.plot([a[0], b[0]], [y, y], color='#FDBA74', lw=6, zorder=1, solid_capstyle='butt')
    for x, t in ev:
        if t == 'in': ax.scatter([x], [y], s=150, color=ORG, zorder=3)
        else: ax.scatter([x], [y], s=150, marker='X', color='#475569', zorder=3)
for x in range(2019, 2027): ax.text(x, -0.9, f"'{str(x)[2:]}" if x < 2026 else "'26.6", ha='center', fontproperties=Bs(12.5), color=SUBC)
ax.scatter([2019.1], [7.0], s=110, color=ORG); ax.text(2019.3, 7.0, '들어옴', va='center', fontsize=12.5, color=INK)
ax.scatter([2020.4], [7.0], marker='X', s=110, color='#475569'); ax.text(2020.6, 7.0, '빠짐', va='center', fontsize=12.5, color=INK)
ax.set_xlim(2016.2, 2026.9); ax.set_ylim(-1.2, 7.5); ax.axis('off')
frame(fig, '들어왔다가 다시 빠진 회사들', "12월 연례 교체 기준 · '26.6은 올해 6월 분기 심사 · CDW는 7년 사이 두 번 들어오고 두 번 빠짐")
fig.subplots_adjust(top=0.84, bottom=0.08, left=0.03, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 올해 12월 일정(지난 7번과 같은 날짜 규칙이면)
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
steps = [('12월 11일(금)', '장 마감 뒤 발표', '한국 시각 12일(토) 오전'), ('12월 18일(금)', '셋째 금요일', '이날까지는 지금 명단 그대로'), ('12월 21일(월)', '장 시작 전 적용', '한국 시각 21일 밤 개장부터')]
for i, (d, a, b) in enumerate(steps):
    x = 0.4 + i * 3.25
    ax.add_patch(plt.Rectangle((x, 3.2), 2.95, 4.2, color='#FFF7ED' if i != 2 else '#FFEDD5', ec=ORG if i == 2 else '#FDBA74', lw=2))
    ax.text(x + 1.475, 6.3, d, ha='center', fontproperties=Bs(19), color=ORG if i == 2 else INK)
    ax.text(x + 1.475, 5.1, a, ha='center', fontproperties=Bs(16), color=INK)
    ax.text(x + 1.475, 4.0, b, ha='center', fontsize=12.5, color=SUBC)
    if i < 2: ax.annotate('', xy=(x + 3.2, 5.3), xytext=(x + 2.98, 5.3), arrowprops=dict(arrowstyle='->', color=SUBC, lw=2))
ax.text(0.4, 1.9, '2019~2025년 7번 모두 둘째 금요일 발표 · 셋째 금요일 다음 월요일 적용', fontsize=13.5, color=INK)
ax.text(0.4, 1.0, '올해 날짜는 같은 규칙으로 센 값 · 나스닥 공식 발표가 나오면 그 날짜가 맞음', fontsize=12.5, color=SUBC)
frame(fig, '올해 12월 나스닥100 정기 교체 날짜', '미국 시각 기준 · 발표 시각은 지난 발표문 오후 8시(미국 동부)')
fig.subplots_adjust(top=0.84, bottom=0.06, left=0.02, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True)
recent = [p for p in recent if 'ndxrecon1127' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png')
