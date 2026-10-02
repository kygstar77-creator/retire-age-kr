# B10 카페 첫 글 이미지 — 숫자는 undervalue.py·peakdrop.py 출력 그대로(같은 기준 하나: 같은 단지·같은 면적대 짝)
import sys, os, re, json, statistics
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__)); W = os.path.join(D, '..', '..')
sys.path.insert(0, W)
import blogimg as B, heatmap as HM
IMG = os.path.join(D, '..', 'editor', '2026-10-03', 'cafe', '193', 'img'); os.makedirs(IMG, exist_ok=True)
rows = []
for ln in open(os.path.join(D, 'undervalue_out_1003.txt'), encoding='utf-8'):
    m = re.match(r'(\S+구) \| ([\d,]+) \| ([\d,]+) \| (\d+) \| ([\d.]+)% \| ([\d.]+)%', ln)
    if m: rows.append(dict(g=m[1], n=int(m[2].replace(',', '')), r=int(m[3].replace(',', '')), p=int(m[4]), j=float(m[5]), y=float(m[6])))
assert len(rows) == 25, len(rows)
mid = statistics.median(r['j'] for r in rows)
# 00 대표 이미지: 숫자 하나
B.bignum(os.path.join(IMG, '00.png'), '서울 아파트 전세가율, 25개 구 중 가장 높은 금천구', '60.9%',
         sub='가장 낮은 강남구는 35.9% · 2026년 7~9월 실거래', src='국토교통부 실거래가 공개시스템 · 같은 단지·같은 면적대 짝 기준')
# 01 히트맵: 크기=매매 건수, 색=중앙값 대비
hm = [{'sym': re.sub(r'구$', '', r['g']), 'sector': '서울', 'cap': r['n'], 'pct': (r['j'] - mid) / mid * 100 / 8, 'label': f"{r['j']:.1f}%"} for r in rows]
HM.draw(hm, os.path.join(IMG, '01.png'), f'서울 25개 구 아파트 전세가율 · 2026년 7~9월 실거래 · 크기=매매 건수, 색=중앙값({mid:.1f}%) 대비')
# 02 25개 구 표
B.table(os.path.join(IMG, '02.png'), '서울 25개 구 아파트 전세가율·월세 수익률 (2026년 7~9월)',
        ['순위', '구', '전세가율', '월세 수익률', '매매 건수', '짝 수'],
        [[str(i + 1), r['g'], f"{r['j']:.1f}%", f"{r['y']:.2f}%", f"{r['n']:,}", str(r['p'])] for i, r in enumerate(rows)],
        hl_col=2, note='짝 수 = 같은 단지·같은 면적대(5㎡)에서 매매·전세가 각 2건 이상 있는 경우. 종로구(6)·광진구(12)·중구(14)는 짝이 적어 흔들릴 수 있음.',
        src='국토교통부 아파트 매매·전월세 실거래(공공데이터포털), 2026.10.1 수집')
# 03 하락 상위 10
pk = [json.loads(l) for l in open(os.path.join(D, 'peakdrop_out.txt'), encoding='utf-8') if l.startswith('{')][:10]
B.table(os.path.join(IMG, '03.png'), '2021년 10~12월 최고가 대비 많이 내린 단지 10 (전용 40㎡ 이상)',
        ['구', '단지', '전용', '2021.10~12 최고', '2026.7~9 중앙', '변동'],
        [[p['구'], p['단지'], f"{float(p['전용']):.1f}㎡", f"{p['고점']/10000:.2f}억", f"{p['비교월']/10000:.2f}억", f"{p['하락률']:+.1f}%"] for p in pk],
        hl_col=5, note='같은 단지·같은 면적대(5㎡)에서 양쪽 거래 2건 이상만. 층·향은 공개 자료에 없어 반영 못 함.',
        src='국토교통부 아파트 매매 실거래(공공데이터포털), 2026.10.1 수집')
print('mid', mid); print(json.dumps(pk[:3], ensure_ascii=False))
