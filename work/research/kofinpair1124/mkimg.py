# kofinpair1124 그림 — 00 표지(차트: 7개 금융 비중 막대, 절반 넘는 셋 주황), 01 7개 금융·반도체 둘·나머지 쌓은 막대, 02 RISE 대형고배당10TR 10종목. 숫자는 calc2_out.txt·calc_out.txt·prepub_1121.txt 그대로
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Patch
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
INK, SUBC, ORG, GRAY, NAVY, BLUE = '#111827', '#6B7280', '#EA580C', '#9CA3AF', '#1E3A5F', '#3B82F6'
SRC = '운용사 6곳 구성종목(11/20자, ACE 11/23자) · 금융 비중은 파이어맵 합산'
TOPIC_PX, NUM_PX = 54, 44
N = ['SOL 코리아고배당', 'PLUS 고배당주', 'KODEX 고배당주', 'ACE 고배당주', 'TIGER 코스피고배당', 'RISE 대형고배당10TR', 'RISE 고배당']
FIN = [56.5, 55.6, 52.5, 37.4, 32.6, 32.2, 28.0]
SEMI = [0, 0, 0, 5.9, 0, 50.3, 46.7]
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor(NAVY)
fig.text(0.06, 0.875, '고배당 ETF 금융주 비중', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.06, 0.795, '7개 중 절반 넘는 건 3개', fontproperties=Bs(NUM_PX - 6), color='#FDBA74')
ax = fig.add_axes([0.06, 0.1, 0.9, 0.64]); ax.set_facecolor(NAVY)
y = np.arange(7)[::-1]
ax.barh(y, FIN, color=[ORG if f > 50 else '#94A3B8' for f in FIN], height=0.62)
ax.plot([50, 50], [-0.5, 6.55], color='white', lw=1.5, ls=(0, (4, 3)))
ax.text(50, 6.7, '절반(50%)', ha='center', va='bottom', fontproperties=Bs(17), color='white')
for yi, f, n in zip(y, FIN, N):
    ax.text(1.2, yi, n, va='center', fontproperties=Bs(19), color=NAVY if f > 50 else '#0F172A')
    ax.text(f + 1.0, yi, f'{f:.1f}%', va='center', fontproperties=Bs(22), color='white')
ax.set_xlim(0, 75); ax.set_ylim(-0.6, 7.5); ax.axis('off')
fig.text(0.06, 0.04, '운용사 구성종목(11/20자) · 파이어맵 합산', fontsize=17, color='#BFDBFE')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '운용사 6곳 구성종목 파일(한화 PLUS·신한 SOL·삼성 KODEX·미래에셋 TIGER 11/20자, 한국투자 ACE 11/23자, KB RISE 11/20자) — calc2_out.txt·calc_out.txt·cardshorts/de1s_kofin/prepub_1121.txt, 파이어맵 직접 합산',
           'made_at': '2026-11-23', 'by': 'research/kofinpair1124/mkimg.py', 'out': 'img/00.png', 'topic': '고배당 ETF 금융주 비중', 'num': '7개 중 3개 · 56.5~28.0%',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 money_info_999/224475934017 남색 바탕 큰 글자 카드·경쟁 6 adam6899/224473556520 남색 바탕 큰 글자+차트 → 남색 바탕 큰 글자 아래 7개 막대(절반 선)'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def frame(fig, title, sub):
    fig.text(0.04, 0.93, title, fontproperties=Bs(22), color=INK)
    fig.text(0.04, 0.88, sub, fontsize=13.5, color=SUBC)
    fig.text(0.04, 0.025, SRC, fontsize=10, color=SUBC)
# 01 금융·반도체 둘·나머지
fig, ax = plt.subplots(figsize=(9, 6.8), dpi=100); fig.subplots_adjust(top=0.80, bottom=0.08, left=0.27, right=0.97)
REST = [100 - a - b for a, b in zip(FIN, SEMI)]
ax.barh(y, FIN, color=ORG, height=0.6)
ax.barh(y, SEMI, left=FIN, color=BLUE, height=0.6)
ax.barh(y, REST, left=[a + b for a, b in zip(FIN, SEMI)], color='#E5E7EB', height=0.6)
for yi, f, s in zip(y, FIN, SEMI):
    ax.text(f / 2, yi, f'{f:.1f}', ha='center', va='center', fontproperties=Bs(14), color='white')
    if s > 10: ax.text(f + s / 2, yi, f'{s:.1f}', ha='center', va='center', fontproperties=Bs(14), color='white')
ax.set_yticks(y); ax.set_yticklabels(N, fontproperties=Bs(14)); ax.tick_params(axis='y', length=0)
ax.set_xticks([]); [s.set_visible(False) for s in ax.spines.values()]; ax.set_xlim(0, 100)
ax.legend(handles=[Patch(color=ORG, label='금융'), Patch(color=BLUE, label='삼성전자+SK하이닉스'), Patch(color='#E5E7EB', label='나머지')],
          prop=Bs(13), frameon=False, loc='lower center', bbox_to_anchor=(0.4, 1.0), ncol=3)
frame(fig, '같은 고배당 ETF, 담은 업종은 이만큼 다르다', '담은 돈 100 가운데 · RISE 고배당은 상위 30종목만 공개(93.3%)')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 RISE 대형고배당10TR 10종목
R = json.load(open('raw/rise_315960_20261120.json', encoding='utf-8'))['items']
R = [(x['item_nm'], x['ratio']) for x in R if x['item_nm'] != '원화예금']
FN = {'KB금융', '삼성생명', '신한지주', '하나금융지주', '우리금융지주'}
fig, ax = plt.subplots(figsize=(9, 6.8), dpi=100); fig.subplots_adjust(top=0.80, bottom=0.06, left=0.2, right=0.95)
yy = np.arange(len(R))[::-1]
ax.barh(yy, [w for _, w in R], color=[BLUE if n in ('삼성전자', 'SK하이닉스') else ORG if n in FN else GRAY for n, _ in R], height=0.62)
for yi, (n, w) in zip(yy, R): ax.text(w + 0.4, yi, f'{w:.1f}%', va='center', fontproperties=Bs(13), color=INK)
ax.set_yticks(yy); ax.set_yticklabels([n for n, _ in R], fontproperties=Bs(14)); ax.tick_params(axis='y', length=0)
ax.set_xticks([]); [s.set_visible(False) for s in ax.spines.values()]; ax.set_xlim(0, 31)
ax.legend(handles=[Patch(color=BLUE, label='반도체 두 종목 50.3%'), Patch(color=ORG, label='금융 다섯 곳 32.2%'), Patch(color=GRAY, label='그 밖')],
          prop=Bs(13), frameon=False, loc='lower center', bbox_to_anchor=(0.4, 1.0), ncol=3)
frame(fig, 'RISE 대형고배당10TR이 담은 열 종목', 'KB자산운용 구성종목 11월 20일자 · 비중 %')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
