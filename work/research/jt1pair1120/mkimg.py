# jt1pair1120 그림(gwanggyo1118 틀) — 00 표지(차트: 같아지는 나이 93세 vs 65세 평균 남·여 — 경쟁 3min_daily_info 첫 그림 '본전 나이' 막대 꼴), 01 같아지는 나이 세 비교, 02 5억 집 65세 vs 70세 받은 돈 합. 숫자는 calc_out 그대로
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
BLUE, INK, SUBC, ORG = '#1D4ED8', '#111827', '#6B7280', '#EA580C'
SRC = '한국주택금융공사 월지급금 예시(2026.3.1, 종신·정액형·일반주택) · 국가데이터처 2026 고령자 통계(2024년 65세 기대여명) · 파이어맵 계산'
TOPIC_PX, NUM_PX = 58, 44
# 00 표지
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('#134E4A')
fig.text(0.07, 0.86, '주택연금', fontproperties=Bs(TOPIC_PX), color='white')
fig.text(0.07, 0.76, '늦게 들면 몇 살에 같아지나', fontproperties=Bs(36), color='#99F6E4')
ax = fig.add_axes([0.1, 0.17, 0.8, 0.5]); ax.set_facecolor('#134E4A')
vals = [93.0, 84.5, 88.7]; labs = ['65세 대신 70세\n따라잡는 나이', '65세 남자\n평균', '65세 여자\n평균']
ax.bar([0, 1, 2], [v - 60 for v in vals], bottom=60, color=['#FB923C', '#94A3B8', '#94A3B8'], width=0.6)
for i, v in enumerate(vals):
    ax.text(i, v + 0.8, f'{v:g}세', ha='center', va='bottom', fontproperties=Bs(NUM_PX if i == 0 else 30), color='white')
    ax.text(i, 59, labs[i], ha='center', va='top', fontproperties=Bs(22), color='white')
ax.set_ylim(52, 102); ax.set_xlim(-0.6, 2.6); ax.axis('off')
fig.text(0.07, 0.06, '공사 월지급금 표 · 국가데이터처 기대여명 · 파이어맵 계산', fontsize=17, color='#99F6E4')
fig.savefig('pkg/img/00.png', dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
json.dump({'type': 'chart', 'source': '한국주택금융공사 월지급금 예시(2026.03.01, 종신·정액형·일반주택) 65세·70세 칸으로 계산한 같아지는 나이 + 국가데이터처 2026 고령자 통계 2024년 65세 기대여명(남 19.5·여 23.7년), calc_out.txt — 파이어맵 직접 계산',
           'made_at': '2026-11-19', 'by': 'research/jt1pair1120/mkimg.py', 'out': 'img/00.png', 'topic': '주택연금', 'num': '93세 · 84.5세 · 88.7세',
           'topic_px': TOPIC_PX, 'num_px': NUM_PX, 'follows': '경쟁 1 3min_daily_info/224482088195 본전 나이 막대 그림 · 2 radishblue 차트 표지'},
          open('pkg/cover_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# 01 같아지는 나이 세 비교 + 평균선
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
G = ['55세 대신\n65세에 들면', '60세 대신\n65세에 들면', '65세 대신\n70세에 들면']; V = [81.1, 90.0, 93.0]
ax.bar(range(3), [v - 60 for v in V], bottom=60, color=['#93C5FD', BLUE, ORG], width=0.55)
for i, v in enumerate(V): ax.text(i, v + 0.6, f'{v:.0f}세', ha='center', va='bottom', fontproperties=Bs(22), color=INK)
for y, t in ((84.5, '65세 남자 평균 84.5세'), (88.7, '65세 여자 평균 88.7세')):
    ax.axhline(y, color=SUBC, lw=1.4, ls='--'); ax.text(-0.42, y + 0.3, t, ha='left', va='bottom', fontsize=12.5, color=SUBC, backgroundcolor='white')
ax.set_xticks(range(3)); ax.set_xticklabels(G, fontproperties=Bs(15)); ax.tick_params(axis='x', length=0, pad=8)
ax.set_ylim(60, 98); ax.set_yticks([60, 70, 80, 90]); ax.set_yticklabels(['60세', '70세', '80세', '90세'], fontsize=12)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.93, '받은 돈 합이 같아지는 나이 — 집값과 상관없이 거의 같아요', fontproperties=Bs(20), color=INK)
fig.text(0.04, 0.88, '3억·5억·9억 집 모두 같은 나이 · 집값 그대로 가정 · 부부는 젊은 사람 나이', fontsize=13.5, color=SUBC)
fig.text(0.04, 0.025, SRC, fontsize=9.5, color=SUBC)
fig.subplots_adjust(top=0.84, bottom=0.14, left=0.1, right=0.98)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 5억 집 받은 돈 합
A = list(range(65, 97)); a65 = [1264*12*(u-65)/10/10000 for u in A]; a70 = [1539*12*max(0, u-70)/10/10000 for u in A]
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=100)
ax.plot(A, a65, color=BLUE, lw=3.5, label='65세에 들면(매달 약 126만원)')
ax.plot(A, a70, color=ORG, lw=3.5, label='70세에 들면(매달 약 154만원)')
for u, t in ((84.5, '남자 평균\n84.5세'), (88.7, '여자 평균\n88.7세'), (93, '같아짐\n93세')):
    ax.axvline(u, color=SUBC, lw=1.2, ls='--'); ax.text(u, 4.75, t, ha='center', va='top', fontsize=11.5, color=INK, backgroundcolor='white')
ax.text(84.5, 2.96 + 0.15, '차 약 2,800만원', ha='right', va='bottom', fontproperties=Bs(13), color=INK)
ax.text(88.7, 3.6 + 0.12, '차 약 1,400만원', ha='right', va='bottom', fontproperties=Bs(13), color=INK)
ax.set_xlim(65, 96); ax.set_ylim(0, 4.8); ax.set_yticks([0, 1, 2, 3, 4]); ax.set_yticklabels(['0', '1억', '2억', '3억', '4억'], fontsize=12)
ax.set_xticks([65, 70, 75, 80, 85, 90, 95]); ax.set_xticklabels([f'{x}세' for x in (65, 70, 75, 80, 85, 90, 95)], fontsize=12)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.legend(prop=Bs(13), frameon=False, loc='upper left', bbox_to_anchor=(0, 0.86))
fig.text(0.04, 0.93, '5억 집, 그 나이까지 받은 돈을 다 더하면', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.88, '보증료·이자 빼고 받은 돈만 · 집값 그대로 가정', fontsize=13.5, color=SUBC)
fig.text(0.04, 0.025, SRC, fontsize=9.5, color=SUBC)
fig.subplots_adjust(top=0.84, bottom=0.1, left=0.08, right=0.98)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
