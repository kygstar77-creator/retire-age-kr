# 고점 대비 하락 단지 계산(B10) — 국토부 실거래(work/research/rt/*_trade.json)만 쓴다. '사라/사지 마라' 없음(사장님 규칙).
#   py -3.12 work/peakdrop.py 202110 202112 202609 20      → 고점구간 202110~202112 대비 202609 거래, 하락률 상위 20
# 짝짓기: 같은 구·같은 단지명·같은 면적대(5㎡)에서 고점구간 최고 거래가 vs 비교월 거래(여러 건이면 중앙값).
# 층·향·수리 상태는 실거래 공개자료에 없어 반영하지 못한다 — 같은 단지·같은 면적대라도 층이 다르면 값이 다르다.
import sys, os, re, json, glob, statistics, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'research', 'rt')
sgg = json.load(open(os.path.join(HERE, 'research', 'seoul_sgg.json'), encoding='utf-8'))
p0, p1, now_ym = sys.argv[1], sys.argv[2], sys.argv[3]
TOP = int(sys.argv[4]) if len(sys.argv) > 4 else 20

def num(s): return int(re.sub(r'[^\d]', '', s or '0') or 0)
def band(a):
    try: return int(float(a) // 5 * 5)
    except (TypeError, ValueError): return None
def load(lawd, ym):
    p = os.path.join(RT, f'{lawd}_{ym}_trade.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else []
def key(r):
    nm = (r.get('aptNm') or '').strip(); b = band(r.get('excluUseAr'))
    return (nm, b) if nm and b else None

months = []
y, m = int(p0[:4]), int(p0[4:])
while f'{y}{m:02d}' <= p1: months.append(f'{y}{m:02d}'); m += 1; (y, m) = (y + 1, 1) if m > 12 else (y, m)

rows = []
for lawd, gu in sgg.items():
    peak = collections.defaultdict(list); now = collections.defaultdict(list)
    for ym in months:
        for r in load(lawd, ym):
            k = key(r)
            if k: peak[k].append(num(r.get('dealAmount')))
    for r in load(lawd, now_ym):
        k = key(r)
        if k: now[k].append((num(r.get('dealAmount')), (r.get('dong') or '').strip(), r.get('excluUseAr')))
    for k, cur in now.items():
        if k not in peak: continue
        hi = max(peak[k]); cur_v = int(statistics.median([c[0] for c in cur]))
        if hi <= 0: continue
        rows.append({'구': gu, '단지': k[0], '면적대': f'{k[1]}~{k[1]+5}㎡', '전용': cur[0][2], '법정동': cur[0][1],
                     '고점': hi, '고점건수': len(peak[k]), '비교월': cur_v, '비교월건수': len(cur),
                     '하락률': round((cur_v - hi) / hi * 100, 1)})
rows.sort(key=lambda r: r['하락률'])
print(f'# 고점 {p0}~{p1} 대비 {now_ym} — 짝지어진 단지·면적대 {len(rows)}쌍 (서울 25개 구 아파트 매매 실거래)')
down = [r for r in rows if r['하락률'] <= -20]
print(f'# 20% 넘게 내린 쌍 {len(down)}개 · 내린 쌍 {len([r for r in rows if r["하락률"]<0])}개 · 오른 쌍 {len([r for r in rows if r["하락률"]>0])}개')
if rows: print(f'# 하락률 중앙값 {statistics.median([r["하락률"] for r in rows])}%')
for r in rows[:TOP]: print(json.dumps(r, ensure_ascii=False))
