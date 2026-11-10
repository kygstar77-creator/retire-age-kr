# acqseoul1111 그림 2장 — 01 집값별 취득세(1주택·85㎡ 이하) 02 서울 구별 아파트 중간 거래가(8~10월 실거래)
import os, sys, json, glob, re, statistics
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, LBLUE, INK, GR, SUBC = '#1D4ED8', '#93C5FD', '#111827', '#CBD5E1', '#6B7280'
def ratep(e):
    if e <= 6: return 1.0
    if e <= 9: return round(e * 2 / 3 - 3, 4)
    return 3.0
def total(e): return e * 1e8 * ratep(e) / 100 * 1.1
# 01
xs = np.linspace(3, 15, 241); ys = [total(x) / 1e4 for x in xs]
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ax.axvspan(6, 9, color='#EFF6FF')
ax.plot(xs, ys, color=BLUE, lw=3.5)
for e, lab in ((6, '6억\n660만원'), (7.5, '7억5천\n1,650만원'), (9, '9억\n2,970만원'), (12, '12억\n3,960만원')):
    t = total(e) / 1e4; ax.plot([e], [t], 'o', color=BLUE, ms=9)
    ax.text(e, t + 330, lab, ha='center', va='bottom', fontproperties=Bs(14), color=INK)
ax.text(7.5, 5600, '6억~9억\n세율이 1%→3%로\n조금씩 오름', ha='center', fontsize=13, color=BLUE)
ax.set_xlim(3, 15); ax.set_ylim(0, 6800)
ax.set_xticks([3, 6, 9, 12, 15]); ax.set_xticklabels(['3억', '6억', '9억', '12억', '15억'], fontproperties=Bs(15))
ax.set_yticks([]);
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.92, '집값별 취득세 (집 없던 사람이 1채, 85㎡ 이하)', fontproperties=Bs(21), color=INK)
fig.text(0.05, 0.02, '취득세+지방교육세 합계 · 지방세법 제11조①8·제151조 · 생애최초 감면 빼고 계산', fontsize=11, color=SUBC)
fig.subplots_adjust(top=0.84, bottom=0.12, left=0.04, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02
SGG = json.load(open('../seoul_sgg.json', encoding='utf-8'))
def num(s): return float(re.sub(r'[^\d.]', '', str(s) or '0') or 0)
med = {}
for code, name in SGG.items():
    ps = []
    for f in glob.glob(f'raw/{code}_2026*.json'):
        for r in json.load(open(f, encoding='utf-8')):
            if r.get('cdealType') or r.get('buyerGbn') == '공공기관': continue
            ps.append(num(r.get('dealAmount')) / 1e4)
    med[name] = statistics.median(ps)
items = sorted(med.items(), key=lambda x: x[1])
fig, ax = plt.subplots(figsize=(9, 11), dpi=100)
y = np.arange(len(items))
cols = [BLUE if v >= 9 else (LBLUE if v > 6 else GR) for _, v in items]
ax.barh(y, [v for _, v in items], color=cols, height=0.72)
for yi, (n, v) in zip(y, items):
    ax.text(v + 0.3, yi, f'{v:.1f}억', va='center', fontsize=12, color=INK)
ax.set_yticks(y); ax.set_yticklabels([n for n, _ in items], fontproperties=Bs(13))
ax.axvline(6, color=SUBC, lw=1, ls='--'); ax.axvline(9, color=SUBC, lw=1, ls='--')
ax.text(6, len(items) - 0.2, '6억', ha='center', fontsize=12, color=SUBC); ax.text(9, len(items) - 0.2, '9억', ha='center', fontsize=12, color=SUBC)
ax.set_xticks([]); ax.set_xlim(0, 31)
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=BLUE, label='세율 3% (9억 이상)'), Patch(color=LBLUE, label='1~3% 사이'), Patch(color=GR, label='1% (6억 이하)')],
          frameon=False, fontsize=13, loc='lower right')
fig.text(0.04, 0.955, '서울 구별 아파트 중간 거래가 (2026년 8~10월)', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.012, '국토교통부 아파트 매매 실거래 1만 160건(해제·공공기관 매수 뺌, 11/11 받음) · 10월 신고는 아직 다 안 들어옴', fontsize=10.5, color=SUBC)
fig.subplots_adjust(top=0.93, bottom=0.04, left=0.13, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print(items[-3:], items[:3])
