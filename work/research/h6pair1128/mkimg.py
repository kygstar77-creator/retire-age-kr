# h6pair1128 그림(jeonse38_1127 틀) — 00 표지(차트: 84㎡ 기간 묶음 가운데 값 4막대), 01 평형×기간 표, 02 월별 매매 건수 막대. 숫자는 calc_out_1126.txt에서 읽는다(손으로 옮기지 않음)
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
SRC = '국토교통부 아파트 매매 실거래 · 서울 강남구 대치동 은마 · 2025년 10월~2026년 11월 계약(11/26 받음, 해제 뺌) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 54, 40
txt = open('calc_out_1126.txt', encoding='utf-8').read()
def meds(a): return [(m[0], int(m[1]), float(m[2])) for m in re.findall(a + r'㎡ (\S+): (\d+)건 가운데 ([\d.]+)억', txt)]
M84, M77 = meds('84'), meds('77')
assert [x[2] for x in M84] == [42.80, 38.83, 37.08, 34.50], M84
assert [x[2] for x in M77] == [37.38, 34.80, 32.10, 31.50], M77
BG = '#3B2F2F'
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '은마 34평 실거래', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.775, '석 달·반년씩 묶은 가운데 값', fontproperties=Bs(30), color='#E7D9C9')
ax = fig.add_axes([0.08, 0.30, 0.84, 0.40]); ax.set_facecolor(BG)
labs = ['25.10~12', '26.1~6', '26.7~9', '26.10~11']
v = [x[2] for x in M84]
ax.bar(range(4), v, color=['#FB923C', '#8C7A6B', '#8C7A6B', '#FB923C'], width=0.62)
for i, y in enumerate(v):
    ax.text(i, y + 0.6, f'{y:.2f}억', ha='center', fontproperties=Bs(24), color='white')
    ax.text(i, 23.4, labs[i], ha='center', fontproperties=Bs(19), color='#E7D9C9', clip_on=False)
ax.set_ylim(25, 46); ax.set_xlim(-0.6, 3.6); ax.axis('off')
fig.text(0.07, 0.19, '1년 새 8억 3천만원 내림', fontproperties=Bs(NUM_PX), color='white')
fig.text(0.07, 0.125, '77건 전체 표는 글 아래에', fontproperties=Bs(28), color='#FDBA74')
fig.text(0.07, 0.05, '국토부 실거래(11/26 조회) · 파이어맵 계산', fontsize=17, color='#E7D9C9')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 매매 실거래 API(서울 강남구 11680, 대치동 은마) 2025-10~2026-11 계약, 해제·공공기관 매수 뺌, 전용 84㎡ 기간 묶음 가운데 값 — calc_out_1126.txt §2, 파이어맵 직접 계산',
           'made_at': '2026-11-26', 'by': 'research/h6pair1128/mkimg.py', 'out': 'img/00.png', 'topic': '은마 34평 실거래', 'num': '1년 새 8억 3천만원 내림',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 dnslekd724/224492353944(층별 실거래 표)·3 engineer_ji/224491409950(실거래 차트 표지)'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=8.0, color=SUBC)
def table(path, title, sub, heads, rows, xs, hl=()):
    fig = plt.figure(figsize=(9, 2.3 + 0.62 * len(rows)), dpi=100)
    frame(fig, title, sub)
    h = fig.get_figheight(); step = 0.62 / h; y = 1 - 1.55 / h
    for x, t in zip(xs, heads): fig.text(x, y, t, fontproperties=Bs(17), color=SUBC)
    fig.add_artist(plt.Line2D([0.04, 0.96], [y - 0.18 / h, y - 0.18 / h], color='#CBD5E1', lw=1.5))
    for i, r in enumerate(rows):
        yy = y - step * (i + 1)
        for x, t in zip(xs, r): fig.text(x, yy, t, fontproperties=Bs(20), color=ORG if i in hl else INK)
    fig.savefig(path, dpi=100); plt.close(fig)
def eok(x): 
    j, c = int(x), round((x - int(x)) * 10000)
    return f'{j}억' + (f' {c:,}만원' if c else '원')
rows = [(M84[i][0], f'{M84[i][2]:.2f}억 ({M84[i][1]}건)', f'{M77[i][2]:.2f}억 ({M77[i][1]}건)') for i in range(4)]
rows.append(('처음→끝', f'{M84[3][2]-M84[0][2]:+.2f}억', f'{M77[3][2]-M77[0][2]:+.2f}억'))
table('pkg/img/01.png', '평형별 가운데 값, 기간 묶음마다', '가운데 값 = 작은 것부터 줄 세웠을 때 한가운데(평균 아님) · 괄호는 거래 건수',
      ('계약 기간', '84㎡(34평)', '77㎡(31평)'), rows, (0.05, 0.36, 0.68), hl=(4,))
# 02 월별 매매 건수
mc = [(m[0], int(m[1]), int(m[2])) for m in re.findall(r'^(20\d\d\.\d\d) 은마 (\d+) · 강남구 (\d+)', txt, re.M)]
assert len(mc) == 14 and mc[-3][1] == 12 and mc[-2][1] == 23, mc
fig = plt.figure(figsize=(9, 6), dpi=100)
frame(fig, '은마 매매, 계약한 달별 건수', '9~10월 두 달에 35건 — 1년 넘게 77건 가운데 45%')
ax = fig.add_axes([0.06, 0.12, 0.90, 0.68])
cols = [ORG if m[0] in ('2026.09', '2026.10') else '#94A3B8' for m in mc]
ax.bar(range(14), [m[1] for m in mc], color=cols, width=0.66)
for i, m in enumerate(mc): ax.text(i, m[1] + 0.4, str(m[1]), ha='center', fontproperties=Bs(15), color=ORG if cols[i] == ORG else INK)
ax.set_xticks(range(14)); ax.set_xticklabels([m[0][2:4] + '.' + m[0][5:] for m in mc], fontsize=10.5, color=SUBC)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.set_yticks([]); ax.set_ylim(0, 26)
ax.text(13, 6.2, '11월은\n신고 중', ha='center', fontsize=11, color=SUBC)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
import glob
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'h6pair1128' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('board', [os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(p)))) for p in recent])
