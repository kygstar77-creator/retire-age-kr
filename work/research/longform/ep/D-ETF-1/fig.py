# -*- coding: utf-8 -*-
"""D-ETF-1 그림 초안 2장 — calc_out.json만 읽는다(남의 차트 캡처 없음).
 fig/heatmap_draft.png : ETF × 섹터 비중 히트맵(한 색 주황, 옅음→짙음, 칸마다 숫자)
 fig/map_draft.png     : 분배율(가로) × 분배 5년 연평균 성장률(세로) 점 그림
화면 최종본은 visual 담당이 종이 질감·손 동그라미로 다시 그린다(이 파일은 숫자·배치 초안)."""
import json, pathlib
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import LinearSegmentedColormap

HERE = pathlib.Path(__file__).resolve().parent; OUT = HERE / 'fig'; OUT.mkdir(exist_ok=True)
F = pathlib.Path(r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\fonts')
for f in ('pd500.ttf', 'pd700.ttf'): fm.fontManager.addfont(str(F / f))
plt.rcParams['font.family'] = fm.FontProperties(fname=str(F / 'pd700.ttf')).get_name()
INK, MUTED, PAPER = '#1F2328', '#6B6F76', '#FBF8F3'
D = json.load(open(HERE / 'calc_out.json', encoding='utf-8'))
S = D['sectors']; SEC = ['정보기술', '금융', '헬스케어', '필수소비재', '에너지', '산업재', '경기소비재', '통신', '유틸리티', '부동산', '소재', '기타']
ROWS = [('SCHD', 'SCHD'), ('TIGER 미국배당다우존스', '국내 미국배당다우존스\n(TIGER·SOL·ACE·KODEX)'), ('VYM', 'VYM'), ('VIG', 'VIG'), ('DGRO', 'DGRO'),
        ('HDV', 'HDV'), ('SPYD', 'SPYD'), ('DIVO', 'DIVO'), ('JEPI', 'JEPI'), ('JEPQ', 'JEPQ'),
        ('PLUS 고배당주', 'PLUS 고배당주'), ('SOL 코리아고배당', 'SOL 코리아고배당'), ('TIGER 은행고배당플러스TOP10', 'TIGER 은행고배당\n플러스TOP10')]
cmap = LinearSegmentedColormap.from_list('or', ['#FFF7EF', '#FDBA74', '#F97316', '#9A3412'])

fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100); fig.patch.set_facecolor(PAPER); ax.set_facecolor(PAPER)
M = [[S[k][s] for s in SEC] for k, _ in ROWS]
ax.imshow(M, cmap=cmap, vmin=0, vmax=60, aspect='auto')
for i, row in enumerate(M):
    for j, v in enumerate(row):
        if v < 0.5: ax.text(j, i, '·', ha='center', va='center', color='#C9C2B8', fontsize=14); continue
        ax.text(j, i, f'{v:.0f}', ha='center', va='center', fontsize=17 if v >= 20 else 14,
                color='white' if v >= 30 else INK, fontweight='bold' if v >= 20 else 'normal')
ax.set_xticks(range(len(SEC)), SEC, fontsize=15, color=INK); ax.xaxis.tick_top()
ax.set_yticks(range(len(ROWS)), [r[1] for r in ROWS], fontsize=14, color=INK)
ax.set_xticks([x - .5 for x in range(1, len(SEC))], minor=True); ax.set_yticks([y - .5 for y in range(1, len(ROWS))], minor=True)
ax.grid(which='minor', color=PAPER, linewidth=2); ax.tick_params(which='both', length=0)
for s in ax.spines.values(): s.set_visible(False)
ax.axhline(9.5, color=INK, linewidth=1.2)  # 미국 상장·국내 미국배당 ↑ / 국내 주식 고배당 ↓
fig.suptitle('배당 ETF는 어느 업종에 돈을 넣었나 (%)', x=0.02, ha='left', fontsize=30, color=INK, y=0.985)
fig.text(0.02, 0.012, '자료: 슈왑·아이셰어즈·뱅가드·스테이트스트리트·JP모건·앰플리파이 보유 종목/섹터 표(2026-09-30~10-16), 국내는 네이버 증권 ETF 분석(10/16). '
         '뱅가드·SPYD는 종목마다 아이셰어즈 ITOT 섹터를 붙여 우리가 합산. 기타 = 옵션 연계 채권·현금', fontsize=11, color=MUTED)
fig.subplots_adjust(left=0.17, right=0.99, top=0.86, bottom=0.05)
fig.savefig(OUT / 'heatmap_draft.png', facecolor=PAPER); plt.close(fig)

# 점 그림: 분배율 × 분배 성장(5년, 없으면 3년 — 점 모양으로 구분)
st = D['stats']
PTS = [('SCHD', 'SCHD'), ('VYM', 'VYM'), ('VIG', 'VIG'), ('DGRO', 'DGRO'), ('HDV', 'HDV'), ('SPYD', 'SPYD'), ('JEPI', 'JEPI'), ('JEPQ', 'JEPQ'), ('DIVO', 'DIVO'),
       ('SPY', 'S&P500(SPY)'), ('161510.KS', 'PLUS 고배당주')]
fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100); fig.patch.set_facecolor(PAPER); ax.set_facecolor(PAPER)
for t, lab in PTS:
    s = st[t]; y = s.get('divcagr5'); three = y is None
    if three: y = s.get('divcagr3')
    x = s['yield']
    if t == 'DIVO':  # 2025-12-30 한 번 튄 분배(0.953달러) 뺀 값 — calc.py ex_special
        x, y = s['yield_ex_special'], s['divcagr5_ex_special']
    ax.scatter(x, y, s=260, color='#F97316' if t != 'SPY' else '#9AA0A6', marker='D' if three else 'o', edgecolor=PAPER, linewidth=2, zorder=3)
    ax.annotate(lab + (' (3년)' if three else ''), (x, y), xytext=(-60, -30) if t == 'VYM' else (12, 8), textcoords='offset points', fontsize=17, color=INK)
ax.axhline(0, color='#C9C2B8', linewidth=1); ax.set_xlim(0, 13); ax.set_ylim(-2, 16)
ax.set_xlabel('지금 받는 분배율(최근 12개월 분배 ÷ 가격, %)', fontsize=17, color=INK)
ax.set_ylabel('분배금이 해마다 는 속도(5년 연평균, %)', fontsize=17, color=INK)
ax.tick_params(colors=MUTED, labelsize=14); [ax.spines[k].set_visible(False) for k in ('top', 'right')]
ax.spines['left'].set_color('#C9C2B8'); ax.spines['bottom'].set_color('#C9C2B8')
ax.grid(color='#ECE6DC', linewidth=1)
fig.suptitle('지금 얼마 주나(가로) × 해마다 얼마나 늘었나(세로)', x=0.02, ha='left', fontsize=30, color=INK, y=0.97)
fig.text(0.02, 0.012, '자료: 야후 파이낸스 일별 분배 이력(분할 반영), 2026-10-16까지 12개월 합 vs 5년 전 같은 기간. DIVO는 2025-12 한 번 큰 분배를 뺀 값. '
         '◆ = 상장 5년 안 돼 3년 연평균', fontsize=11, color=MUTED)
fig.subplots_adjust(left=0.07, right=0.98, top=0.89, bottom=0.1)
fig.savefig(OUT / 'map_draft.png', facecolor=PAPER); plt.close(fig)
print('ok', OUT)
