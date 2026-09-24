# 블로그 경쟁 강도: 네이버 블로그 탭 상위 결과가 얼마나 최근 글인가(7일 안 글 비율).
# 새 글이 매일 밀려오는 말은 검색수가 아무리 높아도 우리 글이 오래 못 버틴다.
#
# 2026-09-24 (루프 회차): 이 파일은 만들어 놓고 어느 회차도 부르지 않는 도구였다
#   (health.py '어느 회차도 안 부르는 도구' 1건 = 이것). 결과 파일 kw_blog_comp.json 을 읽는 코드도 없었다.
#   그래서 한 번 쓰고 마는 스크립트를 모듈로 갈라, demand.rank() 가 후보를 줄 세울 때 쓰게 했다.
#
#   py -3.12 work/kwcomp.py <개수> <최소검색수> <최대검색수>       → kw_blog_comp.json (기존 사용법 그대로)
#   import kwcomp; kwcomp.compete(['금리계산기','전세보증보험'])   → {말: {'n','week','old'} 또는 None}
import sys, os, json, re, time, datetime, urllib.request, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'kw_blog_comp_cache.json')
FRESH_DAYS = 14          # 상위 10개의 나이 분포는 하루 이틀로 뒤집히지 않는다
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}

# 2026-09-24: 네이버가 검색 결과 날짜를 `>날짜<` 가 아니라
# `sds-comps-profile-info-subtext">날짜` 로 내려주게 바뀌어 아무 날짜도 못 잡고 있었다.
# (이 도구가 몇 달째 빈 결과만 내던 이유. 기준 날짜도 '2026.09.20.'로 박혀 있어 같이 고친다.)
DATE_PAT = re.compile(r'profile-info-subtext"?>\s*(\d{4}\.\d{1,2}\.\d{1,2}\.|\d+(?:일|시간|분|주) 전|어제)')


def days_ago(x, today):
    """네이버가 적은 날짜 표기를 '며칠 전'으로 바꾼다. 못 읽으면 None."""
    if '시간' in x or '분' in x: return 0
    if x == '어제': return 1
    m = re.match(r'(\d+)일 전', x)
    if m: return int(m.group(1))
    m = re.match(r'(\d+)주 전', x)
    if m: return int(m.group(1)) * 7
    m = re.match(r'(\d{4})\.(\d{1,2})\.(\d{1,2})\.', x)
    if m:
        try: return (today - datetime.date(*map(int, m.groups()))).days
        except ValueError: return None
    return None


def fresh(k):
    """말 하나 → {'n':읽은 개수, 'week':7일 안 글 수, 'old':1년 넘은 글 수}. 못 읽으면 None."""
    u = 'https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=' + urllib.parse.quote(k)
    try: s = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20).read().decode('utf-8', 'ignore')
    except Exception: return None
    d = DATE_PAT.findall(s)[:10]
    if not d: return None
    today = datetime.date.today()
    ages = [a for a in (days_ago(x, today) for x in d) if a is not None]
    if not ages: return None
    return {'n': len(ages), 'week': sum(1 for a in ages if a <= 7), 'old': sum(1 for a in ages if a >= 365)}


def _load(p, d):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d


def compete(keys, refresh=True, budget=8):
    """말 목록 → 경쟁 강도. 캐시에 있고 FRESH_DAYS 안이면 그대로 쓴다.
    새로 재는 건 한 번에 budget 개까지 — 네이버 블로그 탭은 연달아 두드리면 금방 막힌다.
    못 잰 것은 None 으로 남긴다(모르는 것을 0으로 적지 않는다)."""
    keys = [k for k in dict.fromkeys(keys) if k]
    cache = _load(CACHE, {})
    today = time.strftime('%Y-%m-%d')
    out, need = {}, []
    for k in keys:
        hit = cache.get(k.upper())
        try: age = time.time() - time.mktime(time.strptime(hit[1], '%Y-%m-%d')) if hit else None
        except Exception: age = None
        if hit and age is not None and age <= FRESH_DAYS * 86400: out[k] = hit[0]
        else: need.append(k)
    todo = need[:budget] if refresh else []
    for k in todo:
        f = fresh(k)
        cache[k.upper()] = [f, today]      # 못 잰 것도 날짜를 남겨 매번 다시 두드리지 않는다
        out[k] = f
        time.sleep(0.5)
    for k in keys: out.setdefault(k, None)
    if todo:
        try: json.dump(cache, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        except Exception as e: print('경쟁강도 캐시 저장 실패:', str(e)[:60])
    return out


def hot(f, week_ratio=0.7, min_n=8):
    """상위 결과가 거의 다 새 글이면 '과열' — 써도 며칠 만에 밀린다. 못 잰 것은 과열로 치지 않는다."""
    if not f or f.get('n', 0) < min_n: return False
    return f['week'] / f['n'] >= week_ratio


INC = re.compile(r'SCHD|JEP[IQ]|QQQ|VOO|SPY|TLT|TMF|QLD|TQQQ|SOXL|ETF|배당|커버드콜|리얼티|나스닥|S&P|미국주식|미국채|국채|채권|ISA|IRP|연금|퇴직|연말정산|세액공제|소득공제|종합과세|소득세|양도세|양도소득|취득세|종부세|종합부동산|재산세|건강보험|건보|피부양|예금|적금|파킹|CMA|금리|환율|달러|환전|금값|금시세|금투자|청약|특별공급|특공|생애최초|디딤돌|보금자리|신생아|주담대|주택담보|전세|월세|보증보험|DSR|LTV|갭투자|아파트|실거래|재건축|재개발|분양|토지거래|부동산|재테크|파이어|노후|월급|연봉|실수령|가계부|순자산|신용점수|부업|앱테크|청년미래|청년도약|대출', re.I)
EXC = re.compile(r'주가$|시세$|지수$|증시|선물|코스피|코스닥|삼성|하이닉스|은행$|증권$|카드|보험사|채용|로그인|고객센터|앱$|어플|홈페이지|날씨|뉴스', re.I)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    allk = json.load(open(os.path.join(HERE, 'kw_blog_all.json'), encoding='utf-8'))
    c = [(k, v['pc'] + v['mo'], v) for k, v in allk.items() if INC.search(k) and not EXC.search(k)]
    c = [x for x in c if int(sys.argv[2]) <= x[1] <= int(sys.argv[3])]
    c.sort(key=lambda x: -x[1]); c = c[:int(sys.argv[1])]
    print(len(c), 'candidates', file=sys.stderr)
    got = compete([k for k, _, _ in c], budget=len(c))
    out = [{'k': k, 'vol': vol, 'mo': v['mo'], 'comp': v['comp'], **got[k]} for k, vol, v in c if got.get(k)]
    json.dump(out, open(os.path.join(HERE, 'kw_blog_comp.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(out))


if __name__ == '__main__':
    main()
