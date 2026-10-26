# jbcalc1027 그림 3장 — 숫자는 calc.py(종부세법 8·9·10조·시행령·시행규칙 서식, 지방세법 110·111조, 2026 1주택 재산세 비율 45%) 결과
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
rows = [('13억', 24.9), ('15억', 74.6), ('18억', 163.0), ('20억', 241.0), ('25억', 500.52)]  # 만원, 종부세+농특세, 공제 없음
# 00 표지 — 짙은 초록 바탕, 주제어 크게 + 공시가격별 막대
BG, WH, LG = '#1F3B2D', '#FFFFFF', '#D6D3D1'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.865, '종부세 1주택', fontproperties=Bs(84), color=WH)
fig.text(0.06, 0.765, '공시가격 15억이면 약 75만원', fontproperties=Bs(54), color='#FB923C')
fig.text(0.06, 0.695, '농어촌특별세 포함 · 나이·보유 공제 없을 때', fontsize=30, color=LG)
ax = fig.add_axes([0.06, 0.13, 0.88, 0.5]); ax.set_facecolor(BG)
for i, (lab, v) in enumerate(rows):
    c = '#FB923C' if lab == '15억' else LG
    ax.bar(i, v, color=c, width=0.62)
    ax.text(i, v + 12, f'약 {v:,.0f}만원', ha='center', fontproperties=Bs(28 if lab == '15억' else 24), color=c)
    ax.text(i, -14, lab, ha='center', va='top', fontsize=28, color=WH)
ax.set_ylim(-60, 580); ax.set_xlim(-0.6, 4.6); ax.axis('off')
fig.text(0.06, 0.035, '공시가격 · 작년보다 18.67% 오른 집 가정 · 2026년 법 기준 직접 계산', fontsize=24, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 15억 집 계산 순서
fig = plt.figure(figsize=(9, 6.6), dpi=100); fig.patch.set_facecolor('#FFFFFF')
fig.text(0.05, 0.9, '공시가격 15억원 한 채, 종부세 계산 순서(원 단위)', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.84, '2026년 법 기준 · 나이·보유 공제 없을 때', fontsize=15, color=SUB)
steps = [('12억원 빼고 남은 금액', '3억원', INK), ('그 60%에 세금 매김', '1억 8천만원', INK), ('세율 0.5%', '90만원', INK),
         ('겹치는 재산세 빼기', '−278,640원', SUB), ('농어촌특별세 20% 더하기', '+124,272원', SUB), ('12월에 낼 돈', '745,632원', ORG)]
for i, (a, b, c) in enumerate(steps):
    y = 0.72 - i * 0.11
    fig.text(0.08, y, a, fontsize=19, color=SUB)
    fig.text(0.92, y, b, fontproperties=Bs(24 if i == 5 else 21), color=c, ha='right')
fig.text(0.05, 0.02, '종합부동산세법 8·9조, 시행령 2조의4·4조의3, 농어촌특별세법 5조 · 직접 계산', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 나이·보유 공제에 따라
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
r2 = [('공제 없음', 74.6), ('공제 20%', 59.7), ('공제 40%', 44.7), ('공제 50%', 37.3), ('공제 70%', 22.4), ('공제 80%', 14.9)]
for i, (lab, v) in enumerate(r2):
    y = len(r2) - 1 - i
    ax.barh(y, v, color=ORG if lab == '공제 없음' else GR, height=0.6)
    ax.text(v + 1.5, y, f'약 {v:,.0f}만원', va='center', fontproperties=Bs(18), color=INK)
ax.set_yticks(range(len(r2))); ax.set_yticklabels([r[0] for r in r2][::-1], fontsize=16)
ax.set_xticks([]); ax.set_xlim(0, 95)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.92, '15억원 집, 나이·보유 공제를 받으면', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.865, '만 60세 이상 20~40% · 5년 이상 보유 20~50% · 합쳐 80%까지', fontsize=15, color=SUB)
fig.text(0.05, 0.02, '종합부동산세법 9조 ⑤~⑧ · 종부세+농어촌특별세 · 직접 계산', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.08, left=0.22)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
json.dump({"type": "chart", "source": "종합부동산세법 8·9·10조·시행령 2조의4·4조의3·5조·시행규칙 별지 31호 부표 작성방법, 지방세법 110·111조·시행령 109·109조의2, 농어촌특별세법 5조로 공시가격별 2026 종부세(농특세 포함)를 직접 계산(calc.py), mkimg.py로 그린 막대",
           "made_at": "2026-10-27", "by": "research/jbcalc1027/mkimg.py", "out": "img/00.png", "topic_px": 84, "num_px": 54,
           "note": "작년보다 공시가격 18.67% 오른 집, 재산세 감면 없음 가정"}, open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok')
