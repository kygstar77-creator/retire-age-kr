# jeonse38_1127 그림(halfpair1126 틀) — 00 표지(차트: 단지 39곳 전세가율 줄 세움, 가운데 57%), 01 준공 시기별 3칸 표, 02 높은 곳·낮은 곳 6곳 3칸 표. 숫자는 calc_out_1126.txt §B 그대로
import os, json, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG = '#111827', '#6B7280', '#EA580C'
SRC = '국토교통부 아파트 매매·전월세 실거래 · 인천 연수구 송도동 전용 80~86㎡ · 2026년 7~11월 계약(11/26 받음) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 54, 40
# §B 줄에서 전세가율 읽기 — 손으로 옮기지 않는다
txt = open('calc_out_1126.txt', encoding='utf-8').read()
B = txt.split('## B.')[1].split('## C.')[0]
rates = [int(m) for m in re.findall(r'= (\d+)% · 차이', B)]
assert len(rates) == 39 and rates[0] == 70 and rates[-1] == 39, rates
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#1E3A5F')
fig.text(0.07, 0.86, '송도 84㎡ 전세가율', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.775, '단지 39곳을 높은 순으로 줄 세웠어요', fontproperties=Bs(30), color='#BFDBFE')
ax = fig.add_axes([0.08, 0.30, 0.84, 0.40]); ax.set_facecolor('#1E3A5F')
cols = ['#FB923C' if i in (0, 19, 38) else '#5B7BA6' for i in range(39)]
ax.bar(range(39), rates, color=cols, width=0.72)
ax.axhline(57, color='#FDBA74', lw=1.6, ls='--')
ax.text(0, 73, '70%', ha='center', fontproperties=Bs(24), color='white')
ax.text(38, 42, '39%', ha='center', fontproperties=Bs(24), color='white')
ax.text(19, 61, '가운데 57%', ha='center', fontproperties=Bs(24), color='#FDBA74')
ax.set_ylim(0, 82); ax.set_xlim(-1, 39); ax.axis('off')
fig.text(0.07, 0.19, '가운데 57%', fontproperties=Bs(NUM_PX), color='white')
fig.text(0.07, 0.125, '오래된 단지일수록 높았어요', fontproperties=Bs(28), color='#FDBA74')
fig.text(0.07, 0.05, '국토부 실거래(11/26 조회) · 파이어맵 계산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매·전월세 실거래 API(인천 연수구 28185 송도동) 2026-07~11 계약 전용 80~86㎡, 단지 39곳 순수전세 가운데 값 ÷ 매매 가운데 값, calc_out_1126.txt §B — 파이어맵 직접 계산',
           'made_at': '2026-11-26', 'by': 'research/jeonse38_1127/mkimg.py', 'out': 'img/00.png', 'topic': '송도 84㎡ 전세가율', 'num': '가운데 57%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 realbestlog/224427924941(입주 시기별 표)·2 songdo-life/224474951053 실거래 표·차트'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=8.6, color=SUBC)
def table(path, title, sub, heads, rows, xs, hl=()):
    fig = plt.figure(figsize=(9, 2.3 + 0.62 * len(rows)), dpi=100)
    frame(fig, title, sub)
    h = fig.get_figheight(); step = 0.62 / h; y = 1 - 1.55 / h
    for x, t in zip(xs, heads): fig.text(x, y, t, fontproperties=Bs(17), color=SUBC)
    fig.add_artist(plt.Line2D([0.04, 0.96], [y - 0.18 / h, y - 0.18 / h], color='#CBD5E1', lw=1.5))
    for i, r in enumerate(rows):
        yy = y - step * (i + 1)
        for x, v in zip(xs, r): fig.text(x, yy, v, fontproperties=Bs(20), color=ORG if i in hl else INK)
    fig.savefig(path, dpi=100); plt.close(fig)
# 01 준공 시기별
table('pkg/img/01.png', '준공 시기별 전세가율', '전세 가운데 값 ÷ 매매 가운데 값, 단지마다 낸 뒤 그 가운데',
      ('준공', '단지 수', '전세가율 가운데'),
      [('2009년 이전', '7곳', '62%'), ('2010~2016년', '17곳', '58%'), ('2017년 이후', '15곳', '55%')], (0.06, 0.45, 0.68), hl=(0,))
# 02 높은 곳·낮은 곳
table('pkg/img/02.png', '전세가율 높은 곳 3, 낮은 곳 3', '매매와 전세 차이 = 매매 가운데 값 − 전세 가운데 값',
      ('단지(준공)', '전세가율', '매매와 전세 차이'),
      [('송도금호어울림(2005)', '70%', '1억 7,525만원'), ('풍림아이원1단지(2005)', '65%', '2억 100만원'), ('풍림아이원3단지(2005)', '64%', '2억 650만원'),
       ('퍼스트파크F13-1BL(2017)', '44%', '6억 500만원'), ('마스터뷰23-1BL(2015)', '43%', '5억 4,030만원'), ('퍼스트파크F15BL(2017)', '39%', '7억 4,000만원')],
      (0.05, 0.53, 0.70), hl=(0, 5))
print('ok')
# 표지 검토용 100px·최근 10장 옆(divdj1127 틀)
import glob
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'jeonse38_1127' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('board', [p.split('/')[1] if '/' in p else p for p in recent])
