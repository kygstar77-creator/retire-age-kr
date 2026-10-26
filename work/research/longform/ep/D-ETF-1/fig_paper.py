# -*- coding: utf-8 -*-
"""D-ETF-1 히트맵·점 그림 종이판(visual, 10/21) — fig.py 초안과 같은 숫자(calc_out.json만), 꼴만 바꿈.
 - 바탕: work/video/public/human/paper_crumple.jpg(자체 합성 종이 결), 상자·카드·알약 없음
 - 칸 색은 연필 음영(잉크 계열) — 주황은 손 동그라미(답)에만(클로드 티 금지 목록 '주황은 그 화면의 답 하나만')
 - 손 동그라미 3곳: SCHD 세 업종 55% · 국내 은행 100% · JEPI 분배 성장 0.2%
 나오는 것(fig/): heatmap_paper.png(동그라미 없음) · heatmap_paper_schd.png · heatmap_paper_bank.png
                  map_paper.png · map_paper_jepi.png · paper_circles.json(Remotion HandCircle용 1920×1080 좌표)"""
import json, math, pathlib
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent; OUT = HERE / 'fig'; OUT.mkdir(exist_ok=True)
ROOT = HERE.parents[4]
F = ROOT / 'work' / 'fonts'
for f in ('pd500.ttf', 'pd700.ttf'): fm.fontManager.addfont(str(F / f))
plt.rcParams['font.family'] = fm.FontProperties(fname=str(F / 'pd700.ttf')).get_name()
INK, MUTED, OR = '#1F2328', '#5E574E', '#FF5A00'
PAPER = Image.open(ROOT / 'work' / 'video' / 'public' / 'human' / 'paper_crumple.jpg').convert('RGB').resize((1920, 1080))
D = json.load(open(HERE / 'calc_out.json', encoding='utf-8'))
W, H = 1920, 1080
CIRC = {}


def new_fig():
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.figimage(PAPER, 0, 0, zorder=-10)
    return fig


def hand(fig, cx, cy, rx, ry, seed=0, lw=6.5):
    """fm.tsx HandCircle과 같은 식(2.15바퀴 끝이 살짝 넘침). cx,cy = 그림 픽셀(왼쪽 아래 0)."""
    xs, ys = [], []
    for i in range(65):
        t = (i / 64) * math.pi * 2.15 - 0.4 + seed * 0.3
        wob = 1 + 0.035 * math.sin(t * 3.1) + (i / 64) * 0.06
        xs.append((cx + rx * wob * math.cos(t)) / W); ys.append((cy + ry * wob * math.sin(t)) / H)
    fig.add_artist(Line2D(xs, ys, color=OR, linewidth=lw, solid_capstyle='round', solid_joinstyle='round', transform=fig.transFigure, zorder=20))


def to_px(ax, x, y):
    return tuple(ax.transData.transform((x, y)))


# ---------- 히트맵 ----------
S = D['sectors']; SEC = ['정보기술', '금융', '헬스케어', '필수소비재', '에너지', '산업재', '경기소비재', '통신', '유틸리티', '부동산', '소재', '기타']
ROWS = [('SCHD', 'SCHD'), ('TIGER 미국배당다우존스', '국내 미국배당다우존스'), ('VYM', 'VYM'), ('VIG', 'VIG'), ('DGRO', 'DGRO'),
        ('HDV', 'HDV'), ('SPYD', 'SPYD'), ('DIVO', 'DIVO'), ('JEPI', 'JEPI'), ('JEPQ', 'JEPQ'),
        ('PLUS 고배당주', 'PLUS 고배당주'), ('SOL 코리아고배당', 'SOL 코리아고배당'), ('TIGER 은행고배당플러스TOP10', 'TIGER 은행고배당+TOP10')]
# 연필 음영: 투명 → 짙은 먹(종이 결이 비치게 alpha로)
# 10/27 visual: 연필 회색 → 파란 잉크(대본 '업종마다 색을 칠한 표'와 맞춤, 새 심사관 3차 못함). 주황은 여전히 손 동그라미 답에만
pencil = LinearSegmentedColormap.from_list('pencil', [(0.13, 0.33, 0.58, 0.0), (0.13, 0.33, 0.58, 0.22), (0.12, 0.30, 0.55, 0.55), (0.09, 0.24, 0.47, 0.92)])
M = [[S[k][s] for s in SEC] for k, _ in ROWS]


def heatmap(mark=None):
    fig = new_fig()
    ax = fig.add_axes([0.2, 0.065, 0.785, 0.765]); ax.patch.set_alpha(0)   # 10/27: 글자 키운 만큼 왼쪽 자리
    ax.imshow(M, cmap=pencil, vmin=0, vmax=60, aspect='auto', interpolation='nearest')
    for i, row in enumerate(M):
        for j, v in enumerate(row):
            if v < 0.5: ax.text(j, i, '·', ha='center', va='center', color='#9C9183', fontsize=16); continue
            ax.text(j, i, f'{v:.0f}', ha='center', va='center', fontsize=24 if v >= 20 else 20,
                    color='white' if v >= 30 else INK, fontweight='bold')
    ax.set_xticks(range(len(SEC)), SEC, fontsize=21, color=INK); ax.xaxis.tick_top()   # 10/27: 17→21·23, 칸 숫자 19·16→24·20(휴대폰에서 안 읽힘)
    ax.set_yticks(range(len(ROWS)), [r[1] for r in ROWS], fontsize=23, color=INK)
    ax.set_xticks([x - .5 for x in range(1, len(SEC))], minor=True); ax.set_yticks([y - .5 for y in range(1, len(ROWS))], minor=True)
    ax.grid(which='minor', color=(0.35, 0.3, 0.25, 0.18), linewidth=1); ax.tick_params(which='both', length=0)
    for s in ax.spines.values(): s.set_visible(False)
    ax.axhline(9.5, color=INK, linewidth=1.6)  # 위: 미국 상장·국내 미국배당 / 아래: 국내 주식 고배당
    fig.text(0.5, 0.955, '배당 ETF는 어느 업종에 돈을 넣었나', ha='center', va='center', fontsize=40, color=INK)
    fig.text(0.5, 0.022, '자료: 각 운용사 보유 종목·섹터 표(2026-09-30~10-16), 국내는 네이버 증권(10/16) · 단위 % · 기타 = 옵션 연계 채권·현금',
             ha='center', fontsize=14, color=MUTED)
    fig.canvas.draw()
    # 좌표(픽셀, 왼쪽 아래 0)
    c = {}
    x0, y0 = to_px(ax, 2 - .5, 0 + .5); x1, y1 = to_px(ax, 4 + .5, 0 - .5)  # SCHD 헬스케어~에너지 세 칸
    c['schd'] = dict(cx=(x0 + x1) / 2, cy=(y0 + y1) / 2, rx=(x1 - x0) / 2 + 8, ry=(y1 - y0) / 2 + 1)
    bx0, by0 = to_px(ax, 1 - .5, 12 + .5); bx1, by1 = to_px(ax, 1 + .5, 12 - .5)
    c['bank'] = dict(cx=(bx0 + bx1) / 2, cy=(by0 + by1) / 2, rx=(bx1 - bx0) / 2 + 12, ry=(by1 - by0) / 2 + 4)
    if mark == 'schd':
        k = c['schd']; hand(fig, **k)
        lx, ly = to_px(ax, 9.5, 0)  # SCHD 줄 오른쪽 빈 칸(유틸리티~기타 0%)
        fig.text(lx / W, ly / H, '세 업종에 55%', fontsize=32, color=OR, ha='center', va='center')
    if mark == 'bank':
        k = c['bank']; hand(fig, **k, seed=1)
        fig.text((k['cx'] + k['rx'] + 18) / W, k['cy'] / H, '금융 한 업종에 100%', fontsize=30, color=OR, va='center')
    return fig, c


for mark, name in ((None, 'heatmap_paper'), ('schd', 'heatmap_paper_schd'), ('bank', 'heatmap_paper_bank')):
    fig, c = heatmap(mark); fig.savefig(OUT / f'{name}.png', dpi=100); plt.close(fig)
CIRC['heatmap'] = c

# ---------- 점 그림 ----------
st = D['stats']
PTS = [('SCHD', 'SCHD'), ('VYM', 'VYM'), ('VIG', 'VIG'), ('DGRO', 'DGRO'), ('HDV', 'HDV'), ('SPYD', 'SPYD'), ('JEPI', 'JEPI'), ('JEPQ', 'JEPQ'), ('DIVO', 'DIVO'),
       ('SPY', 'S&P500(SPY)'), ('161510.KS', 'PLUS 고배당주')]
OFF = {'VYM': (-62, -34), 'VIG': (-30, 16), 'DGRO': (14, 10)}


def scatter(mark=None):
    fig = new_fig()
    ax = fig.add_axes([0.075, 0.145, 0.9, 0.73]); ax.patch.set_alpha(0)
    pos = {}
    for t, lab in PTS:
        s = st[t]; y = s.get('divcagr5'); three = y is None
        if three: y = s.get('divcagr3')
        x = s['yield']
        if t == 'DIVO': x, y = s['yield_ex_special'], s['divcagr5_ex_special']
        pos[t] = (x, y)
        ax.scatter(x, y, s=300, color=INK if t != 'SPY' else '#8E867B', marker='D' if three else 'o', edgecolor='none', zorder=3)
        ax.annotate(lab + (' (3년)' if three else ''), (x, y), xytext=OFF.get(t, (14, 10)), textcoords='offset points', fontsize=21, color=INK)
    ax.axhline(0, color=(0.3, 0.25, 0.2, 0.5), linewidth=1.4); ax.set_xlim(0, 13); ax.set_ylim(-1.5, 16); ax.set_yticks(range(0, 17, 2))
    ax.set_xlabel('지금 받는 분배율(최근 12개월, %)', fontsize=20, color=INK, labelpad=10)
    ax.set_ylabel('분배금이 해마다 는 속도(5년 평균, %)', fontsize=20, color=INK, labelpad=10)
    ax.tick_params(colors=MUTED, labelsize=16, length=0)
    for k in ax.spines: ax.spines[k].set_visible(False)
    ax.grid(color=(0.3, 0.25, 0.2, 0.12), linewidth=1)
    fig.text(0.5, 0.955, '지금 얼마 주나 × 해마다 얼마나 늘었나', ha='center', va='center', fontsize=40, color=INK)
    fig.text(0.5, 0.022, '자료: 야후 파이낸스 분배 이력(2026-10-16까지 12개월 vs 5년 전) · DIVO는 2025-12 한 번 큰 분배 뺌 · ◆ = 상장 5년 안 돼 3년 평균',
             ha='center', fontsize=14, color=MUTED)
    fig.canvas.draw()
    jx, jy = to_px(ax, *pos['JEPI'])
    c = {'jepi': dict(cx=jx + 34, cy=jy + 6, rx=86, ry=52)}
    if mark == 'jepi':
        k = c['jepi']; hand(fig, **k, seed=2)
        fig.text((k['cx']) / W, (k['cy'] + k['ry'] + 34) / H, f"해마다 {st['JEPI']['divcagr5']:.1f}%씩", fontsize=30, color=OR, ha='center', va='center')
    return fig, c


for mark, name in ((None, 'map_paper'), ('jepi', 'map_paper_jepi')):
    fig, c = scatter(mark); fig.savefig(OUT / f'{name}.png', dpi=100); plt.close(fig)
CIRC['map'] = c

# Remotion은 위가 0 → y 뒤집어 같이 적음
for g in CIRC.values():
    for k in g.values():
        k['cy_top'] = round(H - k['cy'], 1)
        for kk in ('cx', 'cy', 'rx', 'ry'): k[kk] = round(k[kk], 1)
json.dump({'size': [W, H], 'note': 'cy=왼쪽 아래 0, cy_top=Remotion(위 0). HandCircle({cx, cy:cy_top, rx, ry, p})', **CIRC},
          open(OUT / 'paper_circles.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', OUT)
