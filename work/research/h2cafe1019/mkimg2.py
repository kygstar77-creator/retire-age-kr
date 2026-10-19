# img/01.png 다시 그림 — 경쟁 5(everythn) 막대그래프 꼴: 오래된 단지 vs 새 단지, 매매·새 전세 겹 막대. 숫자는 H-2 calc_out.txt.orig1012(10/12)
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
fam = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
plt.rcParams['font.family'] = fam
B = fm.FontProperties(fname=F + r'\pd700.ttf')
rows = [('잠실', '잠실주공5단지', '1978', 43.45, 5.20, 'old'), ('잠실', '리센츠', '2008', 34.15, 13.50, 'new'),
        ('대치', '은마', '1979', 38.90, 8.30, 'old'), ('대치', '래미안대치팰리스', '2015', 42.75, 18.25, 'new'),
        ('반포', '반포미도', '1987', 40.70, 8.00, 'old'), ('반포', '래미안원베일리', '2023', 59.00, 21.00, 'new')]
lab = {43.45: '약 43억', 34.15: '약 34억', 38.90: '약 39억', 42.75: '약 43억', 40.70: '약 41억', 59.00: '약 59억',
       5.20: '5억 2천', 13.50: '13억 5천', 8.30: '8억 3천', 18.25: '18억', 8.00: '8억', 21.00: '21억'}
fig, ax = plt.subplots(figsize=(9, 9.6), dpi=100)
fig.patch.set_facecolor('white')
ys = [0, 1, 2.6, 3.6, 5.2, 6.2][::-1]
for y, (d, n, yr, m, j, k) in zip(ys, rows):
    c = '#1D4ED8' if k == 'old' else '#94A3B8'
    ax.barh(y + 0.18, m, height=0.36, color=c)
    ax.barh(y - 0.18, j, height=0.36, color='#F59E0B')
    ax.text(m + 0.6, y + 0.18, '매매 ' + lab[m], va='center', fontsize=15, fontproperties=B, color='#111827')
    ax.text(j + 0.6, y - 0.18, '새 전세 ' + lab[j], va='center', fontsize=14, color='#92400E')
    ax.text(-1, y, f'{n}\n({yr}년)', ha='right', va='center', fontsize=15, fontproperties=B if k == 'old' else None, color='#111827')
for y, d in zip([0.5, 3.1, 5.7][::-1], ['잠실', '대치', '반포']):
    ax.text(73, y, d, ha='right', va='center', fontsize=22, fontproperties=B, color='#CBD5E1')
ax.set_xlim(0, 74); ax.set_ylim(-0.7, 6.9); ax.axis('off')
fig.text(0.04, 0.955, '오래된 단지 vs 같은 동네 새 단지', fontsize=24, fontproperties=B, color='#111827')
fig.text(0.04, 0.918, '84㎡ 한 채 · 1년 계약의 중간 가격 · 파랑 = 1990년 전에 지은 단지', fontsize=14, color='#4B5563')
fig.text(0.04, 0.03, '국토교통부 아파트 매매·전월세 실거래(10월 12일 받음) · 새 전세 = 월세 없는 신규 계약', fontsize=12, color='#6B7280')
plt.subplots_adjust(left=0.3, right=0.97, top=0.89, bottom=0.07)
fig.savefig('pkg/img/01.png', dpi=100)
t = json.load(open('pkg/tables.json', encoding='utf-8'))
t['01.png'] = {'rows': [[n + f' ({yr}년)', lab[m], lab[j]] for d, n, yr, m, j, k in rows]}
json.dump(t, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
