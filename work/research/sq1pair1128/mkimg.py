# sq1pair1128 그림 — 00 표지(차트: 15년 비율별 끝값 5막대), 01 비율별 끝값·최대낙폭 표, 02 일반 계좌 한 번에 판 세후 표.
# 숫자는 ../longform/ep/SQ-1/calc_mix_out_1112.txt · calc_tax_out_1121b.txt에서 읽는다(손으로 옮기지 않음)
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
EP = '../longform/ep/SQ-1/'
mix = open(EP + 'calc_mix_out_1112.txt', encoding='utf-8').read()
R = [(int(m[0]), float(m[1]), m[2]) for m in re.findall(r'^\s*(\d+)%\s+([\d.]+)억\s+[\d.]+%\s+(-[\d.]+%)', mix, re.M)]
assert [r[1] for r in R] == [6.77, 8.72, 10.10, 11.50, 13.56], R
tax = open(EP + 'calc_tax_out_1121b.txt', encoding='utf-8').read().split('■ 최근 10년')[0]
T = re.findall(r'SCHD\s+(\d+)% .*?\n\s+\[다른 소득 0\] 직투 세후 ([\d.]+)억.*?국내 상장 세후 ([\d.]+)억', tax)
assert [(t[1], t[2]) for t in T] == [('6.47', '5.61'), ('9.67', '7.69'), ('12.87', '9.62')], T
def eok(x):
    j, c = int(x), round((x - int(x)) * 10000)
    return f'{j}억' + (f' {c:,}만원' if c else '원')
BG = '#1E3A2F'
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.07, 0.86, '나스닥100+SCHD 15년', fontproperties=Bs(50), color='white')
fig.text(0.07, 0.775, 'SCHD 비율별 1억의 끝값(달러 기준)', fontproperties=Bs(28), color='#CFE3D8')
ax = fig.add_axes([0.08, 0.30, 0.84, 0.40]); ax.set_facecolor(BG)
v = [r[1] for r in R]
ax.bar(range(5), v, color=['#8FA89B', '#8FA89B', '#FBBF24', '#8FA89B', '#8FA89B'], width=0.62)
for i, y in enumerate(v):
    ax.text(i, y + 0.3, f'{y:.2f}억', ha='center', fontproperties=Bs(22), color='white')
    ax.text(i, -1.6, f'SCHD {R[i][0]}%', ha='center', fontproperties=Bs(18), color='#CFE3D8', clip_on=False)
ax.set_ylim(0, 15); ax.set_xlim(-0.6, 4.6); ax.axis('off')
fig.text(0.07, 0.17, '반반 1억 → 10억 1천만원', fontproperties=Bs(40), color='white')
fig.text(0.07, 0.105, '10년·5년·원화·세후 표는 글 안에', fontproperties=Bs(26), color='#FDE68A')
fig.text(0.07, 0.04, '야후 수정종가 2011.10~2026.10 · 파이어맵 계산', fontsize=17, color='#CFE3D8')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '야후 파이낸스 QQQ·SCHD 월말 수정종가 2011-10~2026-10, 분배 재투자·매년 10월 말 비율 맞춤 — longform/ep/SQ-1/calc_mix_out_1112.txt, 파이어맵 직접 계산',
           'made_at': '2026-11-27', 'by': 'research/sq1pair1128/mkimg.py', 'out': 'img/00.png', 'topic': '나스닥100+SCHD 15년', 'num': '반반 1억 → 10억 1천만원',
           'topic_px': 50, 'num_px': 40, 'follows': '경쟁 2 firelife__90/224490383070(비율 막대 그림 표지)·3 cpath/224492495808(차트)'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def table(path, title, sub, src, heads, rows, xs, hl=()):
    fig = plt.figure(figsize=(9, 2.3 + 0.62 * len(rows)), dpi=100)
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88 - 0.02 * (5 - len(rows)) / 2, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, src, fontsize=8.5, color=SUBC)
    h = fig.get_figheight(); step = 0.62 / h; y = 1 - 1.55 / h
    for x, t in zip(xs, heads): fig.text(x, y, t, fontproperties=Bs(17), color=SUBC)
    fig.add_artist(plt.Line2D([0.04, 0.96], [y - 0.18 / h, y - 0.18 / h], color='#CBD5E1', lw=1.5))
    for i, r in enumerate(rows):
        yy = y - step * (i + 1)
        for x, t in zip(xs, r): fig.text(x, yy, t, fontproperties=Bs(20), color=ORG if i in hl else INK)
    fig.savefig(path, dpi=100); plt.close(fig)
table('pkg/img/01.png', '15년, SCHD를 섞은 비율마다', '2011년 10월 말 1억 · 분배 재투자 · 해마다 10월 말 비율 맞춤 · 달러 기준',
      '야후 파이낸스 QQQ·SCHD 수정 종가(2011.10~2026.10) · 파이어맵 계산 · 지난 값이며 앞날을 말해 주지 않음',
      ('SCHD 비율', '끝값', '가장 크게 빠진 폭'), [(f'{r[0]}%' + (' (나스닥100만)' if r[0] == 0 else ''), eok(r[1]), r[2].replace('-', '−')) for r in R], (0.05, 0.40, 0.66), hl=(2,))
names = {'100': 'SCHD만', '50': '반반', '0': '나스닥100만'}
table('pkg/img/02.png', '일반 계좌, 15년 뒤 한 번에 팔면', '원화 · 다른 소득 0원 · 국내 상장 ETF가 같은 지수로 똑같이 움직였다고 가정',
      '야후 수정 종가 · 한국은행 원·달러 매매기준율 · 소득세법(2026.11 현행) · 파이어맵 계산 · 건보료 영향 제외',
      ('비율', '직접 산 쪽', '국내 상장'), [(names[t[0]], eok(float(t[1])), eok(float(t[2]))) for t in T], (0.05, 0.36, 0.68))
print('ok', R, T)
import glob
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'sq1pair1128' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('board', [os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(p)))) for p in recent])
