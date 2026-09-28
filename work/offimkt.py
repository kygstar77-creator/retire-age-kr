# [오피스텔 시황] 코너(카페 16시) 숫자 뽑기 — 2026-09-28 15시 write 회차가 만들었다.
# 그전까지 이 코너용 도구가 없어 회차마다 즉석 스크립트를 짜야 했다.
#   py -3.12 work/offimkt.py 202609 [<저장폴더>]
# 국토부 오피스텔 매매·전월세 실거래(rtmolit.fetch)를 서울 25개 구 전부 새로 받아 요약한다.
# 한 건물 몰림(법인 일괄 매매 등)은 구별 순위를 왜곡하니 10건 넘게 몰린 건물은 따로 빼서 보여 준다.
import sys, os, re, json, time, statistics as st
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import rtmolit

def n(s): return int(re.sub(r'[^\d]', '', s or '0') or 0)

def main(ym, outdir=None):
    sgg = json.load(open(os.path.join(HERE, 'research', 'seoul_sgg.json'), encoding='utf-8'))
    raw = {}
    for code, name in sgg.items():
        for kind in ('offi_trade', 'offi_rent'):
            try: raw[f'{code}|{name}|{kind}'] = rtmolit.fetch(kind, code, ym)
            except Exception as e: print(name, kind, '실패', e); raw[f'{code}|{name}|{kind}'] = None
            time.sleep(0.2)
    if outdir:
        os.makedirs(outdir, exist_ok=True)
        json.dump(raw, open(os.path.join(outdir, f'raw_{ym}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    fails = [k for k, v in raw.items() if v is None]
    allt = [r for k, v in raw.items() if k.endswith('offi_trade') for r in (v or [])]
    tr = [r for r in allt if not r.get('cdealType')]
    rn = [r for k, v in raw.items() if k.endswith('offi_rent') for r in (v or [])]
    print(f'조회 {time.strftime("%Y-%m-%d %H:%M")} · {ym} · 실패 {len(fails)}')
    print(f'매매 {len(allt)}건, 해제 {len(allt)-len(tr)}건 → {len(tr)}건 · 마지막 계약일 {max((int(r["dealDay"]) for r in tr), default=0)}일')
    bulk = [b for b, c in Counter(r['offiNm'] for r in tr).items() if c > 10]
    for b in bulk:
        x = [r for r in tr if r['offiNm'] == b]
        print(f'  몰림: {b}({x[0]["sggNm"]} {x[0]["umdNm"]}) {len(x)}건 · 계약일 {sorted(set(r["dealDay"] for r in x))} · 매도 {Counter(r["slerGbn"] for r in x)} 매수 {Counter(r["buyerGbn"] for r in x)} · 합계 {sum(n(r["dealAmount"]) for r in x):,}만원')
    ex = [r for r in tr if r['offiNm'] not in bulk]
    if ex: print(f'몰림 제외 {len(ex)}건 · 평당 중앙 {round(st.median(n(r["dealAmount"])*3.3058/float(r["excluUseAr"]) for r in ex)):,}만원')
    g = defaultdict(list)
    for r in ex: g[r['sggNm']].append(r)
    for k, v in sorted(g.items(), key=lambda kv: -st.median(n(r['dealAmount'])*3.3058/float(r['excluUseAr']) for r in kv[1])):
        if len(v) >= 15:
            print(f'  {k} {len(v)}건 평당 {round(st.median(n(r["dealAmount"])*3.3058/float(r["excluUseAr"]) for r in v)):,} 매매가 {st.median(n(r["dealAmount"]) for r in v):,.0f} 전용 {st.median(float(r["excluUseAr"]) for r in v)}')
    mon = [r for r in rn if n(r.get('monthlyRent')) > 0]; js = [r for r in rn if n(r.get('monthlyRent')) == 0]
    if rn:
        print(f'전월세 {len(rn)}건 · 월세 {len(mon)}({len(mon)/len(rn):.1%}) 중앙 {st.median(n(r["monthlyRent"]) for r in mon) if mon else "-"}만원 · 전세 {len(js)} 보증금 중앙 {st.median(n(r["deposit"]) for r in js) if js else "-"}만원')
        for t in ('신규', '갱신'):
            x = [r for r in mon if r.get('contractType') == t]
            if x: print(f'  월세 {t} {len(x)}건 중앙 {st.median(n(r["monthlyRent"]) for r in x)}만원')
        print('  전월세 많은 구', Counter(r['sggNm'] for r in rn).most_common(3))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else time.strftime('%Y%m'), sys.argv[2] if len(sys.argv) > 2 else None)
