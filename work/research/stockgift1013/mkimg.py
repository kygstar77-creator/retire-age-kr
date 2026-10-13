# stockgift1013 표·그림 — kidcred1012 mkimg 틀
import sys, json, os, datetime as D
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1 = [['증여일 종가 그대로라면(참고)', '9,988만원', '484만원'],
      ['뒤 두 달 22만원 그대로', '1억 1,948만원', '674만원'],
      ['뒤 두 달 20% 회복', '1억 2,935만원', '770만원'],
      ['뒤 두 달 10% 더 하락', '1억 1,455만원', '626만원'],
      ['실제 종가(9월 28일까지)', '1억 2,749만원', '752만원']]
B.table('pkg/img/01.png', '7월 28일 급락일에 454주 증여, 평가액과 세금', ['뒤 두 달 주가', '증여세 평가액', '신고 시 낼 세금'], r1, hl_col=1,
        note='성인 자녀 · 10년 안 다른 증여 없음 · 5천만원 공제 · 신고세액공제 3% · 앞 두 달은 실제 종가',
        src='상속세 및 증여세법 · 한국거래소 종가(다음 금융, 2026.10.13 조회)')
# 02: 7/28 앞뒤 두 달 종가 선 + 4개월 평균선
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
rows = {D.date.fromisoformat(k): v for k, v in json.load(open('daum_005930.json', encoding='utf-8'))}
g = D.date(2026, 7, 28); a, b = D.date(2026, 5, 28), D.date(2026, 9, 28)
ds = [d for d in sorted(rows) if a <= d <= b]; ys = [rows[d] / 10000 for d in ds]
avg = sum(ys) / len(ys)
fp = fm.FontProperties(fname=os.path.join(B.FD, 'pd500.ttf')); fb = fm.FontProperties(fname=os.path.join(B.FD, 'pd700.ttf'))
fig, ax = plt.subplots(figsize=(9, 5.4), dpi=100)
x = list(range(len(ds)))
ax.plot(x, ys, color='#2060e0', lw=2)
ax.axhline(avg, color='#d64541', lw=2, ls='--')
gi = ds.index(g)
ax.scatter([gi], [rows[g] / 10000], color='#181c26', zorder=5)
ax.annotate('증여일 7/28 종가 22만원', (gi, rows[g] / 10000), xytext=(10, -26), textcoords='offset points', fontproperties=fb, fontsize=13, color='#181c26',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))
ax.annotate(f'4개월 평균 {avg:.1f}만원', (len(x) - 1, avg), xytext=(-4, 8), textcoords='offset points', ha='right', fontproperties=fb, fontsize=13, color='#d64541',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))
ax.axvline(gi, color='#9aa3b5', lw=1)
ticks = [i for i, d in enumerate(ds) if d.day in (1,) or d == g][:]
ticks = sorted(set([0, gi, len(ds) - 1] + [i for i, d in enumerate(ds) if d.day == 1 or (i and ds[i-1].month != d.month)]))
keep = []
for i in ticks:
    if all(abs(i - k) >= 5 for k in keep) or i in (gi,): keep = [k for k in keep if abs(k - i) >= 5 or i not in (gi,)] + [i]
ticks = sorted(keep)
ax.set_xticks(ticks); ax.set_xticklabels([f'{ds[i].month}/{ds[i].day}' for i in ticks], fontproperties=fp, fontsize=11)
for t in ax.get_yticklabels(): t.set_fontproperties(fp)
ax.set_ylabel('삼성전자 종가(만원)', fontproperties=fp, fontsize=12)
ax.set_title('급락일에 증여해도 평가액은 4개월 평균', fontproperties=fb, fontsize=19, loc='left', pad=14)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.grid(axis='y', color='#e2e6ee')
fig.text(0.01, 0.01, '한국거래소 정규장 종가(다음 금융 일별 시세, 2026.10.13 조회) · 5/28~9/28', fontproperties=fp, fontsize=11, color='#626a7a')
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('pkg/img/02.png'); plt.close(fig)
print('avg', avg)
json.dump({'01.png': {'rows': r1}}, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
