# stkded1109 그림 2장 — 01 환급 확인 순서(국세청 11/3 보도참고자료 참고2), 02 공제 250만원 빠뜨렸을 때 더 낸 세금(calc.py, 소득세법 제104조)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLU, INK, SUB, GR, LG = '#1D4ED8', '#111827', '#4B5563', '#94A3B8', '#E5E7EB'

# 01 확인 순서
fig = plt.figure(figsize=(9, 6.6), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.9, '내가 이번 환급을 받았는지 보는 순서', fontproperties=Bs(23), color=INK)
def box(x, y, w, h, t, c, tc=INK, fs=15):
    fig.patches.append(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.008,rounding_size=0.02', transform=fig.transFigure, fc=c, ec='none'))
    fig.text(x + w/2, y + h/2, t, ha='center', va='center', fontproperties=Bs(fs), color=tc, linespacing=1.4)
steps = ['홈택스 로그인\n(모바일은 손택스)', '납부·고지·환급금', '환급금 상세조회', '세목 양도소득세\n환급결정 2026년 10월']
for i, s in enumerate(steps):
    x = 0.05 + i * 0.235
    box(x, 0.5, 0.2, 0.22, s, BLU if i == 3 else LG, 'white' if i == 3 else INK, 14)
    fig.text(x + 0.015, 0.74, f'{i+1}', fontproperties=Bs(18), color=BLU)
    if i < 3: fig.text(x + 0.217, 0.6, '▶', ha='center', va='center', fontsize=13, color=GR)
box(0.05, 0.2, 0.43, 0.2, '환급 계좌가 있으면\n그 계좌로 이미 들어옴', '#DBEAFE', fs=15)
box(0.52, 0.2, 0.43, 0.2, '계좌가 없으면 같은 화면 지급신청\n또는 통지서·신분증으로 우체국', '#DBEAFE', fs=14)
fig.text(0.05, 0.08, '국세청은 계좌 비밀번호·카드번호를 묻지 않음 — 이런 문자는 112·1332 신고', fontproperties=Bs(13), color='#B91C1C')
fig.text(0.05, 0.03, '국세청 보도참고자료(2026.11.3.) 참고2', fontsize=11, color='#6B7280')
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 더 낸 세금
rows = [('해외주식\n(20%)', 550000), ('중소기업 주식\n(10%)', 275000), ('국내 비상장 대주주\n1년 안에 판 경우(30%)', 825000)]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
y = np.arange(3)[::-1]
ax.barh(y, [r[1] for r in rows], 0.5, color=[BLU, GR, GR])
labels = ['55만원', '27만 5천원', '82만 5천원']
for yi, r, l in zip(y, rows, labels):
    ax.text(r[1] + 15000, yi, l, va='center', fontproperties=Bs(17), color=BLU if yi == 2 else INK)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontproperties=Bs(14)); ax.set_xticks([]); ax.set_xlim(0, 1050000)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.92, '공제 250만원을 빠뜨리면 더 내는 세금', fontproperties=Bs(23), color=INK)
fig.text(0.05, 0.86, '이익이 250만원 넘을 때 · 지방소득세 포함 · 환급가산금 빼고', fontsize=13, color=SUB)
fig.text(0.05, 0.02, '소득세법 제103조·제104조로 계산 · 지방소득세는 양도소득세의 10%', fontsize=11, color='#6B7280')
fig.subplots_adjust(top=0.8, bottom=0.1, left=0.3, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
