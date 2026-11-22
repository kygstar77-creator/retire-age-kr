# kosdaq1123 그림 — 00 표지(차트: 2006-01-02 1억 두 지수 선), 01 매달 100만원 나눠 넣기(세 기간), 02 5·10년 보유 손해 비율. 숫자는 calc_out·calc_dca_out·calc2_out 그대로
import os, json, sys, datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, GRAY, NAVY, RED = '#111827', '#6B7280', '#EA580C', '#9CA3AF', '#1E3A5F', '#DC2626'
SRC = '한국은행 ECOS 코스닥·코스피 일별 종가(11/22 받음, 11/20 종가까지) · 파이어맵 계산 · 지수 값만'
d = json.load(open('raw_ecos.json', encoding='utf-8'))
def ser(name):
    r = [(datetime.datetime.strptime(t, '%Y%m%d').date(), v) for t, v in d[name] if t >= '20060102']
    b = r[0][1]; return [a for a, _ in r], [v / b for _, v in r]
xq, yq = ser('kosdaq'); xp, yp = ser('kospi')
TOPIC_PX, NUM_PX = 56, 42
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.07, 0.86, '코스닥 20년 보유', fontproperties=Bs(TOPIC_PX), color=INK)
fig.text(0.07, 0.77, '1억 → 약 8,900만원', fontproperties=Bs(NUM_PX), color=RED)
ax = fig.add_axes([0.07, 0.13, 0.86, 0.55])
ax.plot(xp, yp, color=GRAY, lw=2.2); ax.plot(xq, yq, color=RED, lw=3)
ax.axhline(1, color=INK, lw=1, ls=':')
ax.text(xp[-1], yp[-1] + 0.12, '코스피 3.5배', ha='right', fontproperties=Bs(24), color=SUBC)
ax.text(xq[-1], yq[-1] - 0.42, '코스닥 0.89배', ha='right', fontproperties=Bs(24), color=RED)
ax.set_yticks([]); ax.tick_params(axis='x', labelsize=15)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
fig.text(0.07, 0.04, '2006.1.2에 1억 넣었다면 · 2026.11.20 종가 · 파이어맵 계산', fontsize=17, color=SUBC)
fig.savefig('pkg/img/00.png', dpi=100); plt.close(fig)
json.dump({'type': 'chart', 'source': '한국은행 ECOS 802Y001 코스닥(0089000)·코스피(0001000) 일별 종가 2006-01-02~2026-11-20, 같은 날 1억원 넣은 경우 — calc_out.txt 파이어맵 직접 계산',
           'made_at': '2026-11-22', 'by': 'research/kosdaq1123/mkimg.py', 'out': 'img/00.png', 'topic': '코스닥 20년 보유', 'num': '1억 → 약 8,900만원',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 3 graham4/224486741100 표지의 큰 숫자 대비(4,869 vs 645)를 따르되, 사진 위 글자 대신 흰 바탕·큰 제목·빨간 숫자 한 줄·실제 두 지수 선(spx10y1122 표지 꼴)'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 나눠 넣기
lab = ['2006년부터\n251달', '2016년부터\n131달', '2021년부터\n71달']
qv = [0.3, -16.8, -24.0]; pv = [135.8, 92.1, 64.0]
x = np.arange(3); w = 0.36
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.bar(x - w/2, qv, w, color=RED, label='코스닥'); ax.bar(x + w/2, pv, w, color=GRAY, label='코스피')
for i in range(3):
    ax.text(x[i] - w/2, qv[i] + (3 if qv[i] >= 0 else -9), f'{qv[i]:+.1f}%', ha='center', fontproperties=Bs(15), color=RED)
    ax.text(x[i] + w/2, pv[i] + 3, f'{pv[i]:+.1f}%', ha='center', fontproperties=Bs(15), color=INK)
ax.axhline(0, color=INK, lw=1)
ax.set_xticks(x); ax.set_xticklabels(lab, fontproperties=Bs(14)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(-40, 155); ax.legend(frameon=False, fontsize=14, loc='upper right')
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
frame(fig, '매달 첫 거래일 100만원씩 넣었다면(넣은 돈 대비)', '2026년 11월 20일 종가로 평가 · 배당·보수·세금 뺌')
fig.subplots_adjust(top=0.83, bottom=0.14, left=0.03, right=0.98); fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 보유 기간별 손해 비율
lab = ['5년 보유', '10년 보유']; qv = [27.8, 7.9]; pv = [9.4, 0.2]
x = np.arange(2); w = 0.34
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.bar(x - w/2, qv, w, color=RED, label='코스닥'); ax.bar(x + w/2, pv, w, color=GRAY, label='코스피')
for i in range(2):
    ax.text(x[i] - w/2, qv[i] + 0.8, f'{qv[i]}%', ha='center', fontproperties=Bs(18), color=RED)
    ax.text(x[i] + w/2, pv[i] + 0.8, f'{pv[i]}%', ha='center', fontproperties=Bs(18), color=INK)
ax.set_xticks(x); ax.set_xticklabels(lab, fontproperties=Bs(16)); ax.tick_params(axis='x', length=0)
ax.set_yticks([]); ax.set_ylim(0, 33); ax.legend(frameon=False, fontsize=14, loc='upper right')
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
frame(fig, '들고 있던 기간별 손해로 끝난 비율', '2003년부터 거래일마다 그날 샀다고 치고 N년 뒤 값과 비교(10년 3,443번)')
fig.subplots_adjust(top=0.83, bottom=0.1, left=0.03, right=0.98); fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
import glob
from PIL import Image
im = Image.open('pkg/img/00.png'); im.resize((100, 100)).save('pkg/cover_100.png')
recent = [p for p in sorted(glob.glob('../*/pkg/img/00.png'), key=os.path.getmtime, reverse=True) if 'kosdaq1123' not in p][:10]
board = Image.new('RGB', (11 * 160, 160), 'white'); board.paste(im.convert('RGB').resize((160, 160)), (0, 0))
for i, p in enumerate(recent): board.paste(Image.open(p).convert('RGB').resize((160, 160)), ((i + 1) * 160, 0))
board.save('pkg/cover_board.png'); print('ok')
