# 오피스텔 저평가 단지표 — 사장님 2026-09-23 "저평가 된 게 어느 오피스텔인지도 찾아줘야 완성형 아니야?"
#   py -3.12 work/offitable.py [상위N=15]
# 구 단위에서 멈추지 않고 **단지 이름·전용면적·세대수·주차·연식**까지 적는다.
#
# 자료: 국토교통부 실거래(work/research/rt/) + 건축물대장(apis.building)
# 거르는 조건(2026-09-23에 실제로 겪은 왜곡을 막는다):
#   - 같은 단지·같은 5㎡ 면적대끼리만 짝짓는다
#   - 매매 2건·월세 4건 이상만
#   - 월세 30만원 미만 제외(관리비형·반전세 잔여가 섞인다)
#   - 보증금이 매매가의 절반을 넘으면 제외 — 실투자금이 200만원이라 수익률이 72%로 튀었다(관악 노블리)
# 규칙: '사라·사지 마라'는 쓰지 않는다. 조건과 순위와 숫자만 적는다.
import sys, os, re, json, glob, time, collections, statistics
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apis
RT = os.path.join(HERE, 'research', 'rt')
OUT = os.path.join(HERE, 'research', 'offitable')

def num(s):
    try: return float(re.sub(r'[^\d.]', '', str(s) or '0') or 0)
    except Exception: return 0.0

def dong_codes():
    """오피스텔 실거래에는 법정동코드(umdCd)가 없고 동 이름만 있다.
    아파트 실거래에는 둘 다 있으므로 거기서 이름→코드 표를 만든다(2026-09-24 확인, 282건)."""
    m = {}
    for f in glob.glob(os.path.join(RT, '*_trade.json')):
        if '_offi_' in os.path.basename(f): continue
        try: rows = json.load(open(f, encoding='utf-8'))
        except Exception: continue
        for r in rows:
            if r.get('umdNm') and r.get('umdCd'): m[(r['sggCd'], r['umdNm'])] = r['umdCd']
    return m

def build(topn=15):
    trade, rent, meta = collections.defaultdict(list), collections.defaultdict(list), {}
    for f in glob.glob(os.path.join(RT, '*_offi_trade.json')):
        for r in json.load(open(f, encoding='utf-8')):
            k = (r.get('sggNm'), (r.get('offiNm') or '').strip(), int(num(r.get('excluUseAr')) // 5 * 5))
            trade[k].append(num(r.get('dealAmount'))); meta.setdefault(k, r)
    for f in glob.glob(os.path.join(RT, '*_offi_rent.json')):
        for r in json.load(open(f, encoding='utf-8')):
            mr = num(r.get('monthlyRent'))
            if mr <= 0: continue
            rent[(r.get('sggNm'), (r.get('offiNm') or '').strip(), int(num(r.get('excluUseAr')) // 5 * 5))].append((num(r.get('deposit')), mr))
    rows = []
    for k in set(trade) & set(rent):
        t, rs = trade[k], rent[k]
        if len(t) < 2 or len(rs) < 4: continue
        mm = statistics.median(t); dep = statistics.median(d for d, _ in rs); mo = statistics.median(m for _, m in rs)
        if mo < 30 or dep > mm * 0.5: continue
        rows.append({'구': k[0], '단지': k[1], '면적': k[2], '매매': mm, '보증금': dep, '월세': mo,
                     '수익률': mo * 12 / (mm - dep) * 100, '매매건': len(t), '월세건': len(rs), '_r': meta[k]})
    rows.sort(key=lambda r: -r['수익률'])

    codes = dong_codes(); got = 0
    pick = rows[:topn] + rows[-5:]
    for r in pick:
        x = r['_r']; j = str(x.get('jibun') or '0').split('-')
        cd = codes.get((x.get('sggCd'), x.get('umdNm')))
        b = apis.building(x.get('sggCd'), cd, j[0], j[1] if len(j) > 1 else '0') if cd else None
        r['건물'] = b or {}; got += 1 if (b and b.get('세대수')) else 0
        r['동'] = x.get('umdNm'); r['준공'] = str(x.get('buildYear') or '')
        time.sleep(0.5)
    return rows, pick, got

def main():
    topn = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    rows, pick, got = build(topn)
    os.makedirs(OUT, exist_ok=True)
    day = time.strftime('%Y-%m-%d')
    med = statistics.median(r['수익률'] for r in rows)
    L = [f'# 서울 오피스텔 월세 수익률 단지표 ({day})', '',
         f'실거래로 계산한 {len(rows)}곳. 수익률 중앙값 {med:.2f}%. 건축물대장이 붙은 곳 {got}/{len(pick)}.',
         '',
         '계산: 월세×12 ÷ (매매 중앙값 − 보증금 중앙값). 같은 단지·같은 5㎡ 면적대끼리만 짝지었다.',
         '거른 것: 매매 2건·월세 4건 미만, 월세 30만원 미만, 보증금이 매매가의 절반을 넘는 반전세.',
         '취득세·재산세·중개수수료·공실·관리비는 들어 있지 않다. 집값 등락도 계산에 없다.',
         '호가가 아니라 실제로 신고된 거래다. "사라·사지 마라"는 적지 않는다.', '',
         '| 순위 | 구 | 동 | 단지 | 전용 | 수익률 | 매매 | 보증금 | 월세 | 호실 | 주차 | 호당주차 | 준공 | 거래 |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(pick, 1):
        b = r['건물']
        rank = i if i <= topn else f'하위{i-topn}'
        L.append(f"| {rank} | {r['구']} | {r['동'] or '-'} | {r['단지']} | {r['면적']}~{r['면적']+5}㎡ | "
                 f"{r['수익률']:.2f}% | {r['매매']:,.0f} | {r['보증금']:,.0f} | {r['월세']:,.0f} | "
                 f"{b.get('세대수') or '-'} | {b.get('주차대수') or '-'} | {b.get('세대당주차') or '-'} | "
                 f"{b.get('준공') or (r['준공'] + '년' if r['준공'] else '-')} | 매{r['매매건']}/월{r['월세건']} |")
    L += ['', '단위: 만원. 전용은 전용면적 기준이다(시중에서 말하는 평형은 공급면적이라 더 넓게 적힌다).','호실·주차·준공은 건축물대장. 오피스텔은 세대가 아니라 호실로 센다.']
    p = os.path.join(OUT, f'{day}.md')
    open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L[:10]))
    print(f'\n... 표 {len(pick)}줄 · 저장 {p}')

if __name__ == '__main__': main()
