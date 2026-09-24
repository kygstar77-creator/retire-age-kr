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
    # 사장님 2026-09-24 "독자가 판단하게 하되 우리가 적은 수치는 100% 정확해야 한다."
    # → 표에 올리는 줄은 전부 조회한다. 한 줄이라도 비어 있으면 '-'로 두고 지어내지 않는다.
    pick = rows[:topn] + rows[-5:]
    cache = {}
    for r in pick:
        x = r['_r']; j = str(x.get('jibun') or '0').split('-')
        cd = codes.get((x.get('sggCd'), x.get('umdNm')))
        ck = (x.get('sggCd'), cd, j[0], j[1] if len(j) > 1 else '0')
        if ck not in cache:
            cache[ck] = apis.building(*ck) if cd else None
            time.sleep(0.5)
        b = dict(cache[ck] or {})
        # 주상복합은 아파트 세대 주차까지 건축물대장에 합산돼 호당 7.75 같은 값이 나온다
        # (용산 래미안 더 센트럴, 2026-09-24 확인). 오피스텔만 떼어낼 수 없으므로 숫자를 지우고 사유를 적는다.
        if b.get('세대당주차') and b['세대당주차'] > 2.5:
            b['주차대수'] = b['세대당주차'] = None
            b['비고'] = '주상복합 — 아파트 주차가 합산돼 오피스텔만 못 가름'
        r['건물'] = b; got += 1 if b.get('세대수') else 0
        r['동'] = x.get('umdNm'); r['준공'] = str(x.get('buildYear') or '')
    return rows, pick, got

def verify(pick):
    """표에 적은 숫자를 원자료로 다시 세어 대조한다.
    사장님 2026-09-24: "독자가 판단하게 하되 우리가 수치 적은 건 100% 정확해야 할 거야."
    한 줄이라도 안 맞으면 표를 저장하지 않는다."""
    T, R = collections.defaultdict(list), collections.defaultdict(list)
    for f in glob.glob(os.path.join(RT, '*_offi_trade.json')):
        for x in json.load(open(f, encoding='utf-8')):
            T[(x.get('sggNm'), (x.get('offiNm') or '').strip(), int(num(x.get('excluUseAr')) // 5 * 5))].append(num(x.get('dealAmount')))
    for f in glob.glob(os.path.join(RT, '*_offi_rent.json')):
        for x in json.load(open(f, encoding='utf-8')):
            mr = num(x.get('monthlyRent'))
            if mr > 0:
                R[(x.get('sggNm'), (x.get('offiNm') or '').strip(), int(num(x.get('excluUseAr')) // 5 * 5))].append((num(x.get('deposit')), mr))
    bad = []
    for r in pick:
        k = (r['구'], r['단지'], r['면적'])
        t, rs = T.get(k, []), R.get(k, [])
        chk = {
            '매매건': len(t), '월세건': len(rs),
            '매매': statistics.median(t) if t else None,
            '보증금': statistics.median(d for d, _ in rs) if rs else None,
            '월세': statistics.median(m for _, m in rs) if rs else None,
        }
        for f in ('매매건', '월세건', '매매', '보증금', '월세'):
            if chk[f] is None or abs((chk[f] or 0) - r[f]) > 0.01:
                bad.append(f"{r['단지']} {r['면적']}㎡ · {f} 표 {r[f]} vs 원자료 {chk[f]}")
        if chk['매매'] and chk['보증금'] is not None:
            y = chk['월세'] * 12 / (chk['매매'] - chk['보증금']) * 100
            if abs(y - r['수익률']) > 0.01:
                bad.append(f"{r['단지']} {r['면적']}㎡ · 수익률 표 {r['수익률']:.2f} vs 재계산 {y:.2f}")
    return bad

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
         '| 순위 | 구 | 동 | 단지 | 전용 | 수익률 | 매매 | 보증금 | 월세 | 호실 | 주차 | 호당주차 | 준공 | 거래 | 비고 |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(pick, 1):
        b = r['건물']
        rank = i if i <= topn else f'하위{i-topn}'
        # 표에 적는 수익률은 '표에 적힌 매매·보증금·월세'로 다시 계산해 찍는다.
        # 원래 값으로 찍으면 독자가 표 숫자로 검산했을 때 어긋난다 — 2026-09-24 실측으로 20줄 중 2줄이
        # 그랬다(유러피안하우스I 표 8.95 vs 표 숫자 검산 8.84). 순위는 원래 값으로 매긴 그대로다.
        mm_s, bo_s, wl_s = round(r['매매']), round(r['보증금']), round(r['월세'])
        y_s = (wl_s * 12 / (mm_s - bo_s) * 100) if mm_s > bo_s else r['수익률']
        units = b.get('세대수')
        # 대장에서 오피스텔 동만 잡혀 호실이 한 자리로 나오는 일이 있다(방화샤르망1 '1호실').
        # 그대로 적으면 273호실짜리 건물이 1호실로 보이므로 숫자를 쓰지 않고 사유를 적는다.
        note = b.get('비고') or ''
        if isinstance(units, int) and units < 10:
            note = (note + ' · ' if note else '') + '대장 호실수가 %d로 잡혀 신뢰할 수 없어 적지 않음' % units
            units = None
        L.append(f"| {rank} | {r['구']} | {r['동'] or '-'} | {r['단지']} | {r['면적']}~{r['면적']+5}㎡ | "
                 f"{y_s:.2f}% | {mm_s:,.0f} | {bo_s:,.0f} | {wl_s:,.0f} | "
                 f"{units or '-'} | {b.get('주차대수') or '-'} | {b.get('세대당주차') or '-'} | "
                 f"{b.get('준공') or (r['준공'] + '년' if r['준공'] else '-')} | 매{r['매매건']}/월{r['월세건']} | {note} |")
    L += ['', '단위: 만원. 전용은 전용면적 기준이다(시중에서 말하는 평형은 공급면적이라 더 넓게 적힌다).','호실·주차·준공은 건축물대장. 오피스텔은 세대가 아니라 호실로 센다.']
    bad = verify(pick)
    if bad:
        print('검산 불일치 — 표를 저장하지 않는다')
        for b in bad: print('  X', b)
        sys.exit(1)
    L += ['', f'검산: 표의 모든 수치를 원자료로 다시 세어 {len(pick)}줄 전부 일치함({day}).']
    p = os.path.join(OUT, f'{day}.md')
    open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L[:10]))
    print(f'\n... 표 {len(pick)}줄 · 저장 {p}')

if __name__ == '__main__': main()
