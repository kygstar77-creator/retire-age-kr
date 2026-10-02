# b10danji1003 이미지 — 숫자는 rank.json(rank.py 출력) 그대로. 표지는 visual cafe-covers-1002/make_covers.py 틀 재사용.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__)); W = os.path.join(D, '..', '..'); sys.path.insert(0, W)
import blogimg as B
IMG = os.path.join(D, 'pkg', 'img'); os.makedirs(IMG, exist_ok=True)
rows = json.load(open(os.path.join(D, 'rank.json'), encoding='utf-8'))
hi = rows[:10]; lo = [r for r in rows[-11:] if not r['apt'].startswith('상림마을7단지')][::-1]
assert len(lo) == 10
eok = lambda v: f"{v/10000:.2f}억"
def tb(path, title, rs, note):
    B.table(path, title, ['구·동', '단지', '전용', '지은 해', '매매 중간', '전세 중간', '전세가율', '건수(매·전)'],
            [[f"{r['gu'][:-1]} {r['dong']}", r['apt'].replace('(101동~103동)', ''), f"{r['band']}㎡대", r['year'], eok(r['sale']), eok(r['jeonse']), f"{r['ratio']*100:.1f}%", f"{r['ns']}·{r['nj']}"] for r in rs],
            hl_col=6, note=note, src='국토교통부 아파트 매매·전월세 실거래(공공데이터포털), 2026년 7~9월 계약분')
tb(os.path.join(IMG, '01.png'), '서울 전세가율 높은 단지·면적대 10 (2026년 7~9월)', hi,
   '같은 동·단지·5㎡ 면적대에서 매매·전세 각 2건 이상, 전용 40㎡대 이상. 건수 2~3건은 한 건에도 바뀔 수 있음.')
tb(os.path.join(IMG, '02.png'), '서울 전세가율 낮은 단지·면적대 10 (2026년 7~9월)', lo,
   '상림마을7단지아이파크 BL1-3(20.0%)은 전세 중간값이 유난히 낮아 뺐음. 9월 계약은 신고가 더 들어올 수 있음.')
print('ok', [r['apt'] for r in lo])
