# elsjeonse1129 그림(jeonse38_1127 틀) — 00 표지(차트: 반년별 새 계약·갱신 가운데), 01 갱신 145건 3칸 표, 02 넓이별 3칸 표. 숫자는 calc_out_1127.txt 그대로 읽음
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
BG = '#3B1F5C'
SRC = '국토교통부 아파트 전월세 실거래 · 서울 송파구 잠실엘스 · 월세 없는 전세 · 계약 2025년 6월~2026년 11월(11/27 받음) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 54, 40
txt = open('calc_out_1127.txt', encoding='utf-8').read()
F_ = txt.split('§F')[1].split('§G')[0]
halves = [(lab, float(n) / 10000, float(g) / 10000, float(d)) for lab, n, g, d in re.findall(r'(\S+): 신규 \d+ (\d+)\.?\d* · 갱신 \d+ (\d+)\.?\d* · 차이 (\d+)', F_)]
assert len(halves) == 3 and halves[2][3] == 11500, halves
def eok(v):
    a = int(round(v * 10000)); e, m = divmod(a, 10000)
    return f'{e}억' + (f' {m:,}' if m else '')
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '잠실엘스 84㎡ 전세', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.775, '새 계약과 갱신, 반년마다 가운데 값', fontproperties=Bs(30), color='#DDD6FE')
ax = fig.add_axes([0.08, 0.27, 0.84, 0.45]); ax.set_facecolor(BG)
labs = ['1년 전 반년', '그다음 반년', '최근 반년']
for i, (lab, n, g, d) in enumerate(halves):
    ax.bar(i - 0.2, n - 9.2, bottom=9.2, width=0.36, color='#FB923C' if i == 2 else '#C4B5FD')
    ax.bar(i + 0.2, g - 9.2, bottom=9.2, width=0.36, color='#8B7BBE')
    ax.text(i - 0.2, n + 0.12, eok(n), ha='center', fontproperties=Bs(17), color='white')
    ax.text(i + 0.2, g + 0.12, eok(g), ha='center', fontproperties=Bs(17), color='#DDD6FE')
    ax.text(i, 8.7, labs[i], ha='center', fontproperties=Bs(19), color='#DDD6FE')
ax.text(-0.45, 14.75, '■ 새 계약', fontproperties=Bs(18), color='#C4B5FD'); ax.text(0.35, 14.75, '■ 갱신', fontproperties=Bs(18), color='#B8A9E6')
ax.set_ylim(8.5, 15.2); ax.set_xlim(-0.6, 2.6); ax.axis('off')
fig.text(0.07, 0.17, '차이 1억 1,500만원', fontproperties=Bs(NUM_PX), color='white')
fig.text(0.07, 0.105, '최근 반년, 그 전의 두 배 넘게 벌어졌어요', fontproperties=Bs(28), color='#FDBA74')
fig.text(0.07, 0.04, '국토부 실거래(11/27 조회) · 단위 만원 · 파이어맵 계산', fontsize=17, color='#DDD6FE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '국토교통부 아파트 전월세 실거래 API(서울 송파구 11710 잠실동 잠실엘스) 2025-06~2026-11 계약 전용 80~86㎡ 월세 0 전세, 계약 구분(신규·갱신)별 보증금 가운데 값 반년씩, calc_out_1127.txt §F — 파이어맵 직접 계산',
           'made_at': '2026-11-27', 'by': 'research/elsjeonse1129/mkimg.py', 'out': 'img/00.png', 'topic': '잠실엘스 84㎡ 전세', 'num': '차이 1억 1,500만원',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 307720/224492241424(매매·전세 엇박자 차트)·3 msmzzang2030/224492261140 실거래 표'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=8.2, color=SUBC)
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
# 01 갱신 145건 (84㎡대, 12개월) — calc_out §84 갱신요구권 줄
s84 = txt.split('===== 84')[1].split('===== 59')[0]
m_use = re.search(r'갱신요구권 사용: (\d+)건 올린 비율 가운데 ([\d.]+)%', s84); m_no = re.search(r'갱신요구권 빈칸: (\d+)건 올린 비율 가운데 ([\d.]+)%', s84)
assert m_use.group(1) == '86' and m_no.group(1) == '59'
table('pkg/img/01.png', '84㎡대 갱신 145건, 보증금 올린 비율', '이전 보증금 대비 · 2025년 12월~2026년 11월 계약 · 5%를 넘긴 41건은 모두 표시 없는 갱신',
      ('갱신 구분', '건수', '올린 비율 가운데'),
      [('갱신요구권 사용', m_use.group(1) + '건', f'{float(m_use.group(2)):.1f}%'), ('사용 표시 없음', m_no.group(1) + '건', f'{float(m_no.group(2)):.1f}%'), ('합계', '145건', '5.0%')],
      (0.06, 0.45, 0.66), hl=(1,))
# 02 넓이별 12개월
table('pkg/img/02.png', '12개월 전체, 넓이별 전세 가운데 값', '2025년 12월~2026년 11월 계약 · 월세 없는 전세만',
      ('넓이·구분', '건수', '보증금 가운데'),
      [('84㎡대 새 계약', '134건', '12억 8,500만원'), ('84㎡대 갱신', '145건', '12억 1,000만원'), ('59㎡대 새 계약', '41건', '10억 8,000만원'), ('59㎡대 갱신', '64건', '9억 9,750만원')],
      (0.06, 0.45, 0.63), hl=(0,))
print('ok')
import glob
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'elsjeonse1129' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('board', [os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(p)))) for p in recent])
