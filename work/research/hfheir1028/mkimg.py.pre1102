# hfheir1028 그림 3장 — 숫자는 calc.py(HF 월지급금 예시 70세 4억 1,231천원·초기보증료 1.0%·연보증료 0.95%·CD 3.27%+1.1%p 고정, 집값 그대로)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
# 00 표지 — 짙은 와인 바탕(최근 표지: 자줏빛·녹색·갈색·흰·청록·파랑·올리브), 주제어 + 나이별 자녀에게 남는 돈 막대
BG, WH, LG = '#4A1D2A', '#FFFFFF', '#F3D9DF'
rows = [('75세', 31001), ('80세', 19788), ('85세', 5166), ('90세', 0)]
lab = {31001: '3억 1,000만원', 19788: '1억 9,800만원', 5166: '5,200만원', 0: '0원'}
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.865, '주택연금 상속', fontproperties=Bs(84), color=WH)
fig.text(0.06, 0.765, '85세면 자녀 몫 약 5,200만원', fontproperties=Bs(50), color='#FB923C')
fig.text(0.06, 0.695, '두 분 모두 떠난 나이(나이 적은 분 기준) · 70세·4억원 집', fontsize=25, color=LG)
ax = fig.add_axes([0.06, 0.15, 0.88, 0.48]); ax.set_facecolor(BG)
for i, (a, v) in enumerate(rows):
    c = '#FB923C' if a == '85세' else LG
    ax.bar(i, max(v, 300), color=c, width=0.68)
    ax.text(i, max(v, 300) + 800, lab[v], ha='center', fontproperties=Bs(28), color=c)
    ax.text(i, -1200, a, ha='center', va='top', fontproperties=Bs(30), color=WH)
ax.set_ylim(-5200, 36000); ax.set_xlim(-0.6, 3.6); ax.axis('off')
fig.text(0.06, 0.035, '집값 그대로 · 모자라도 자녀에게 청구 없음', fontsize=26, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 받은 돈 vs 대출잔액, 집값 4억 선
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ages = ['75세', '80세', '85세', '90세']; paid = [7386, 14772, 22158, 29544]; bal = [8999, 20212, 34834, 53900]
x = range(4)
def man(v):
    v=int(round(v/100.0))*100; e,r=divmod(v,10000)
    return (f'{e}억 ' if e else '')+(f'{r:,}만' if r else '')
ax.bar([i - 0.19 for i in x], paid, width=0.36, color=GR, label='받은 돈')
ax.bar([i + 0.19 for i in x], bal, width=0.36, color=ORG, label='대출잔액(보증료·이자 포함)')
for i in x:
    ax.text(i - 0.19, paid[i] + 700, man(paid[i]), ha='center', fontsize=11, color=SUB)
    ax.text(i + 0.19, bal[i] + 700, man(bal[i]), ha='center', fontproperties=Bs(12), color=ORG)
ax.axhline(40000, color=INK, ls='--', lw=1.8); ax.text(3.55, 40800, '집값 4억원', ha='right', fontproperties=Bs(14), color=INK)
ax.set_xticks(list(x)); ax.set_xticklabels(ages, fontsize=16); ax.set_yticks([]); ax.set_ylim(0, 60000)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=13, loc='upper left')
fig.text(0.05, 0.92, '받은 돈보다 대출잔액이 빨리 불어납니다', fontproperties=Bs(21), color=INK)
fig.text(0.05, 0.865, '70세·4억원 집·월 123만 1천원 · 86세 6개월쯤 집값을 넘어요', fontsize=14, color=SUB)
fig.text(0.05, 0.02, '한국주택금융공사 월지급금 예시(2026.3.1)·보증료 · 금리 CD 3.27%+1.1%p 고정 · 직접 계산', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.82, bottom=0.1, left=0.05, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 자녀가 집을 지키려면 갚을 돈 = 적은 쪽
fig = plt.figure(figsize=(9, 6.6), dpi=100); fig.patch.set_facecolor('#FFFFFF')
fig.text(0.05, 0.9, '자녀가 집을 지키려면 얼마를 갚나', fontproperties=Bs(23), color=INK)
fig.text(0.05, 0.84, '집값과 대출잔액 중 적은 금액만 갚습니다 (집값 4억원 그대로)', fontsize=14, color=SUB)
fig.text(0.40, 0.75, '대출잔액', fontsize=15, color=SUB, ha='center'); fig.text(0.78, 0.75, '갚을 돈', fontsize=15, color=SUB, ha='center')
opts = [('80세에 떠나면', '2억 200만원', '2억 200만원', '잔액이 더 적어 잔액만큼'), ('85세에 떠나면', '3억 4,800만원', '3억 4,800만원', '잔액이 더 적어 잔액만큼'), ('90세에 떠나면', '5억 3,900만원', '4억원', '집값이 더 적어 집값만큼')]
for i, (a, b, c, d) in enumerate(opts):
    y = 0.62 - i * 0.2
    fig.text(0.05, y, a, fontproperties=Bs(18), color=INK)
    fig.text(0.40, y, b, fontproperties=Bs(20), color=INK, ha='center')
    fig.text(0.78, y, c, fontproperties=Bs(21), color=ORG if i == 2 else INK, ha='center')
    fig.text(0.05, y - 0.07, d, fontsize=13, color=SUB)
fig.text(0.05, 0.02, '한국주택금융공사 「가입고객 사망 후 절차 안내」 · 70세·4억원 집·월 123만 1천원 · 직접 계산', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
