# 후보를 수요(월 검색수) 순으로 세운다.
#
# 사장님 2026-09-24: "기획한 시리즈물대로 쓰되, 그 안에서 어떤 걸 조사하고 포스팅할 때
#                    수요가 높은 걸 선택하냐는 말이야. 단지 중에서라도."
#
# 시리즈(B2 종목·B4 도시·B11 손품 동네…)는 그대로 둔다. 바뀌는 건 그 안에서 무엇을 고르냐다.
# 지금까지 planner의 rot()은 목록을 그냥 순서대로 돌렸다 — 수요와 아무 상관이 없었다.
# 상계동을 고른 것도, 상계주공9단지를 고른 것도 검색수를 본 적이 없다.
#
#   py -3.12 work/demand.py 상계주공 은마 잠실주공5단지      → 검색수 순으로 출력
#   import demand; demand.rank(['서울','부산','제주'])        → 수요 높은 순 목록
#
# 측정은 네이버 검색광고 키워드도구(kwvol.py). 캐시에 없거나 7일 지난 것만 새로 잰다.
import sys, os, re, json, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'demand_cache.json')
FRESH_DAYS = 7
# 검색광고 API는 없는 말에도 '< 10'(=5)을 준다. 그래서 20 미만은 '사람들이 검색하는 말이 아니다'로 본다.
# 시리즈 고정 주제('공시가격 대비 실거래 비율' 같은 서술형)가 여기 걸린다 — 검색수로 줄 세울 대상이 아니다.
# 이걸 안 가르면 편성표에 '검색 10'이 찍혀 실제로 잰 값처럼 보인다.
MIN_REAL = 20

def _load(p, d):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d

def key_of(item):
    """목록 항목에서 검색할 말을 뽑는다.
    'SOXL(ETF)' → 'SOXL' · '리얼티인컴(O·배당주)' → '리얼티인컴' · '순자산 10억' → '순자산 10억'"""
    s = re.split(r'[(（]', str(item))[0].strip()
    return re.sub(r'\s+', ' ', s)[:40]

def _measure(keys):
    """검색광고 API로 잰다. 키가 없거나 실패하면 빈 dict — 그 경우 원래 순서를 그대로 쓴다."""
    out = {}
    try:
        sys.path.insert(0, HERE)
        import kwvol
        kv = kwvol.load()
        for i in range(0, len(keys), 5):               # 힌트는 한 번에 5개까지
            chunk = [k.replace(' ', '') for k in keys[i:i + 5] if k]
            if not chunk: continue
            try:
                for r in kwvol.call(kv, chunk):
                    k = (r.get('relKeyword') or '').strip()
                    if not k: continue
                    out[k.upper()] = kwvol.num(r.get('monthlyPcQcCnt')) + kwvol.num(r.get('monthlyMobileQcCnt'))
            except Exception as e:
                print('검색수 조회 실패:', str(e)[:70])
            time.sleep(0.3)
    except SystemExit as e:                            # kwvol.load()가 키 없으면 sys.exit
        print('검색수 못 잼(키 파일):', str(e)[:70])
    except Exception as e:
        print('검색수 못 잼:', repr(e)[:70])
    return out

def vols(items, refresh=True):
    """항목 → 월 검색수. 모르는 것은 None."""
    cache = _load(CACHE, {})
    today = time.strftime('%Y-%m-%d')
    need, keys = [], {}
    for it in items:
        k = key_of(it); keys[it] = k
        hit = cache.get(k.upper())
        old = (not hit) or (time.time() - time.mktime(time.strptime(hit[1], '%Y-%m-%d'))) > FRESH_DAYS * 86400
        if old: need.append(k)
    if need and refresh:
        got = _measure(need)
        for k in need:
            v = got.get(k.upper().replace(' ', ''), got.get(k.upper()))
            if v is not None: cache[k.upper()] = [v, today]
        # 못 잰 것도 날짜를 남겨 매일 다시 두드리지 않는다(값은 None)
        for k in need:
            if k.upper() not in cache: cache[k.upper()] = [None, today]
        try: json.dump(cache, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        except Exception as e: print('캐시 저장 실패:', str(e)[:60])
    return {it: (cache.get(keys[it].upper()) or [None])[0] for it in items}

def compete(items, refresh=True, budget=6):
    """상위 후보의 블로그 탭 경쟁 강도(kwcomp). 못 재면 빈 dict — 그러면 검색수 순서를 그대로 쓴다.
    2026-09-24: 검색수만 보고 고르면 '금리계산기'처럼 매일 새 글이 밀려오는 말을 계속 집는다.
    kwcomp.py 는 그걸 재라고 만든 도구인데 어느 회차도 부르지 않고 있었다."""
    try:
        sys.path.insert(0, HERE)
        import kwcomp
        return kwcomp.compete([key_of(x) for x in items], refresh=refresh, budget=budget), kwcomp.hot
    except Exception as e:
        print('경쟁강도 못 잼:', repr(e)[:70])
        return {}, (lambda f: False)

def rank(items, refresh=True):
    """수요 높은 순. 검색어가 아닌 것(MIN_REAL 미만)은 뒤로 보내되 원래 순서를 지킨다.
    뒤로 보내기만 하고 빼지는 않는다 — 빼면 그 시리즈가 영영 안 나간다.
    검색수가 높아도 블로그 탭 상위가 거의 다 새 글인 '과열' 말은 real 안에서 뒤로 보낸다
    (검색수 순서 자체는 건드리지 않고 과열/아님 두 덩이로만 가른다)."""
    items = list(items)
    if not items: return items
    v = vols(items, refresh)
    real = sorted([x for x in items if isinstance(v.get(x), int) and v[x] >= MIN_REAL], key=lambda x: -v[x])
    rest = [x for x in items if x not in real]
    if len(real) > 1:
        comp, is_hot = compete(real[:6], refresh)
        cool = [x for x in real if not is_hot(comp.get(key_of(x)))]
        warm = [x for x in real if x not in cool]
        if warm: print('경쟁 과열(상위가 거의 다 새 글)로 뒤로:', ', '.join(str(x)[:20] for x in warm))
        real = cool + warm
    return real + rest

def label(item, v):
    """수치를 적을 때는 잰 것만 적는다. 안 잰 것을 0이나 10으로 적지 않는다."""
    if isinstance(v, int) and v >= MIN_REAL: return f'{item} (검색 {v:,})'
    if isinstance(v, int): return f'{item} (검색어 아님 — 시리즈 고정 주제)'
    return f'{item} (검색수 못 잼)' 

def main():
    args = sys.argv[1:]
    if not args: sys.exit('후보를 주세요: py -3.12 work/demand.py 상계주공 은마 ...')
    v = vols(args)
    for it in rank(args, refresh=False):
        print(f'{(v.get(it) if v.get(it) is not None else 0):>9,}  {it}' + ('' if v.get(it) is not None else '  (못 잼)'))

if __name__ == '__main__': main()
