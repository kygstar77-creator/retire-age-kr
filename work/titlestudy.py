# 제목 분석기 — 사장님 2026-09-23 "제목 분석 안 해?! 니 맘대로 니 생각대로 지어버린다".
#   py -3.12 work/titlestudy.py                 → 기본 검색어로 한 바퀴
#   py -3.12 work/titlestudy.py "코픽스" "VYM"  → 검색어를 직접 준다
#
# 내가 제목을 지어내지 않기 위한 도구다. 네이버 검색에서 **실제로 상위에 뜬 글의 제목**을 긁어
# 모양을 재고, 우리 제목을 같은 자로 재서 어디가 다른지만 말한다. 규칙은 숫자에서 나온다.
# 메모리 firemap-korean-copy: "문구를 새로 쓰지 않는다. 실제로 쓰이는 말을 찾아 출처와 함께 쓴다."
import sys, os, re, json, html, time, statistics, collections, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
OUT_MD = os.path.join(R, 'titlerule.md'); OUT_JSON = os.path.join(HERE, 'titlerule.json')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'}

# 우리 네 축을 덮는 검색어. 실제로 우리가 쓰는 주제여야 비교가 뜻이 있다.
KEYWORDS = ['코픽스', 'VYM 배당', 'SOXL', 'SCHD 배당', '연금저축 세액공제',
            '전세가율', 'FOMC 점도표', '리얼티인컴 배당', '커버드콜 ETF', '가구 순자산']

def get(u):
    try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25).read().decode('utf-8', 'ignore')
    except Exception as e: print('  가져오기 실패:', str(e)[:60]); return ''

def clean(t):
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', t))).strip()

def ranked_titles(kw, tab):
    """네이버 검색 상위에 실제로 뜬 제목. 블로그 이름이 아니라 글 제목만 고른다
    (글 제목에만 titleHref 뒤에 글 번호가 붙는다)."""
    host = 'blog' if tab == 'blog' else 'cafe'
    s = get(f'https://search.naver.com/search.naver?ssc=tab.{tab}.all&query=' + urllib.parse.quote(kw))
    pat = r'"title":"(.{6,90}?)","titleEllipsis":\d+,"titleHref":"https://' + host + r'\.naver\.com/[^/"]+/\d+"'
    out, seen = [], set()
    for m in re.finditer(pat, s):
        t = clean(m.group(1))
        if t and t not in seen: seen.add(t); out.append(t)
    return out

# ── 제목의 모양을 재는 자 ────────────────────────────────────────────────
def ending(t):
    t = t.strip().rstrip('.')
    if t.endswith('?') or re.search(r'(까요|나요|ㄹ까|가요|건가요)$', t): return '물음'
    if t.endswith('다'): return '다로 끝'
    return '명사로 끝'

def sep(t):
    if '?' in t: return '물음표'
    if ',' in t: return '쉼표'
    if '·' in t: return '가운뎃점'
    if ':' in t or '|' in t: return '콜론·막대'
    if ' - ' in t or '–' in t: return '대시'
    return '없음'

def shape(t, kw=None):
    nums = re.findall(r'\d[\d,.]*', t)
    head = None
    if kw:
        k = kw.split()[0]
        head = '맨 앞' if t.strip().startswith(k) else ('중간' if k in t else '없음')
    return {'길이': len(t), '어절': len(t.split()), '끝맺음': ending(t), '구분자': sep(t),
            '숫자 개수': len(nums), '숫자 있음': '있음' if nums else '없음',
            '괄호': '있음' if re.search(r'[\(\[]', t) else '없음',
            # 상위 제목을 눈으로 읽고 찾은 두 가지. 사실 나열이 아니라 독자 쪽으로 돌려놓는 장치다.
            #   "내 대출은?" "내 대출금리에 어떻게 반영될까" — 독자 자신의 돈으로 연결
            #   "코픽스는 멈췄는데 주담대는 왜 오르나" — 상반된 사실을 붙여 궁금하게 만든다
            '독자 지칭(내·우리)': '있음' if re.search(r'(^|\s)(내|제|우리|당신|본인)\s?\S', t) else '없음',
            '반전 연결(~는데·왜·vs)': '있음' if re.search(r'[는은ㄴ린]데|인데|지만|왜|\bvs\b|보다|차이|그런데', t, re.I) else '없음',
            '검색어 위치': head}


TICKERS = (r'\b(LEN|NVDA|TSLA|AAPL|MSFT|AVGO|SCHD|JEPI|JEPQ|QQQ|QQQM|VOO|SPY|TQQQ|QLD|SOXL|SOXX|'
           r'QYLD|XYLD|DIVO|DGRO|VYM|HDV|SPYD|NOBL|KO|JNJ|PG|MO|VZ|PEP|MCD|ABBV|CVX|XOM|BRK)\b')

def ticker_rate(titles):
    """상위 노출 제목이 티커를 쓰는 비율.
    사장님 2026-09-24 "제목에 티커라도 병기해서 넣어줘야 하는 거 아니야".
    2026-09-24 실측: SCHD 93% · 리얼티인컴 37% · 엔비디아 7% · 커버드콜 ETF 3% · 레나 3%.
    70% 넘으면 티커만, 20~70%면 한글(티커) 병기, 20% 밑이면 한글만 쓴다.
    다만 한글 이름이 낯선 종목은 비율과 무관하게 병기한다(사장님이 "레나 주가가 뭔데?"라고 물으셨다)."""
    if not titles:
        return None
    # 한 글자 티커(리얼티인컴 O)는 일반 영문과 구분이 안 돼 괄호 안에 있을 때만 센다.
    # 안 그러면 리얼티인컴 제목이 통째로 안 잡혀 비율이 37%에서 0%로 떨어진다(2026-09-24 확인).
    one = r'[(（]\s*(O|V|F|T|C)\s*[)）]'
    n = sum(1 for t in titles if re.search(TICKERS, t) or re.search(one, t))
    return n / len(titles)

def ticker_advice(kw):
    """그 검색어로 상위 제목을 긁어 티커를 어떻게 쓸지 한 줄로 돌려준다."""
    ts = ranked_titles(kw, 'blog')
    r = ticker_rate(ts)
    if r is None:
        return kw, None, '상위 제목을 못 받음 — 한글(티커) 병기로 간다'
    if r >= 0.7:
        how = '티커를 그대로 쓴다'
    elif r >= 0.2:
        how = '한글(티커)로 병기한다'
    else:
        how = '한글만 쓴다. 다만 한글 이름이 낯선 종목이면 병기한다'
    return kw, r, how

def tally(rows, key):
    c = collections.Counter(r[key] for r in rows if r.get(key) is not None)
    n = sum(c.values()) or 1
    return [(k, v, v / n) for k, v in c.most_common()]

def med(rows, key):
    v = [r[key] for r in rows if isinstance(r.get(key), (int, float))]
    return statistics.median(v) if v else None

def our_titles():
    """우리 카페 글 — 하루당 조회를 성적으로 붙인다(textloop과 같은 잣대)."""
    sys.path.insert(0, HERE)
    import textloop as T
    now = time.time()
    cp = [p for p in T.cafe_posts() if (now - p['ts']) / 3600 >= 18]
    for p in cp: p['per'] = p['read'] / max((now - p['ts']) / 86400, 0.75)
    return sorted(cp, key=lambda p: -p['per'])

def main():
    kws = [a for a in sys.argv[1:] if not a.startswith('--')] or KEYWORDS
    ranked = []
    for kw in kws:
        for tab in ('blog', 'cafe'):
            ts = ranked_titles(kw, tab)
            print(f'  {kw} / {tab} 탭 상위 {len(ts)}개')
            for i, t in enumerate(ts):
                ranked.append({'kw': kw, 'tab': tab, 'rank': i + 1, 'title': t, **shape(t, kw)})
            time.sleep(1.2)                       # 검색 서버에 부담 주지 않는다
    if not ranked: print('상위 제목을 하나도 못 가져왔다 — 규칙 없음'); return

    ours = our_titles()
    ours_rows = [{'title': p['title'], 'per': p['per'], **shape(p['title'])} for p in ours]
    top_ours = ours_rows[:max(5, len(ours_rows) // 3)]

    res = {'at': time.strftime('%Y-%m-%d %H:%M'), 'keywords': kws,
           'ranked_n': len(ranked), 'ours_n': len(ours_rows)}

    md = ['# 제목 규칙 (titlestudy 자동 생성 — 내가 지어내지 않는다)', '',
          f"측정 {res['at']} · 검색어 {len(kws)}개 · 네이버 상위 노출 제목 {len(ranked)}개 · 우리 카페 제목 {len(ours_rows)}개",
          '', f"검색어: {', '.join(kws)}", '',
          '아래 숫자는 네이버 검색 블로그·카페 탭에 **실제로 상위 노출된 제목**을 센 것이다.',
          '제목을 새로 지을 때 이 모양을 따른다. 내 취향으로 정하지 않는다.', '']

    md += ['## 한눈에', '', '| 항목 | 네이버 상위 | 우리 전체 | 우리 잘된 글 |', '|---|---|---|---|']
    for key, label in (('길이', '제목 길이(자)'), ('어절', '어절 수'), ('숫자 개수', '숫자 개수')):
        md.append(f"| {label} 중앙값 | {med(ranked, key)} | {med(ours_rows, key)} | {med(top_ours, key)} |")
    for key in ('끝맺음', '구분자', '숫자 있음', '독자 지칭(내·우리)', '반전 연결(~는데·왜·vs)'):
        a = tally(ranked, key); b = tally(ours_rows, key); c = tally(top_ours, key)
        f = lambda x: f'{x[0][0]} {x[0][2]:.0%}' if x else '-'
        md.append(f"| {key} 1위 | {f(a)} | {f(b)} | {f(c)} |")

    for key in ('끝맺음', '구분자', '숫자 개수', '독자 지칭(내·우리)', '반전 연결(~는데·왜·vs)', '검색어 위치'):
        md += ['', f'## {key} — 네이버 상위 {len(ranked)}개']
        for k, v, p in tally(ranked, key): md.append(f'- {k}: {v}개 {p:.0%}')
        if key != '검색어 위치':
            md.append(f'- (우리) ' + ' / '.join(f'{k} {p:.0%}' for k, v, p in tally(ours_rows, key)))

    md += ['', '## 상위 노출 제목 그대로 (앞 20개)']
    for r in ranked[:20]:
        md.append(f"- [{r['tab']} {r['rank']}위 · {r['kw']}] {r['title']}")
    md += ['', '## 우리 잘된 제목 (하루당 조회)']
    for p in ours[:8]: md.append(f"- {p['per']:.1f}/일 · {p['title']}")

    os.makedirs(R, exist_ok=True); open(OUT_MD, 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    res['ranked'] = ranked[:200]; res['ours'] = ours_rows
    json.dump(res, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    print(f"\n[제목 분석 {res['at']}] 상위 노출 {len(ranked)}개 · 우리 {len(ours_rows)}개")
    print('  길이 중앙값  상위', med(ranked, '길이'), '/ 우리', med(ours_rows, '길이'))
    for key in ('끝맺음', '구분자', '숫자 개수', '독자 지칭(내·우리)', '반전 연결(~는데·왜·vs)'):
        print(f"  {key}  상위: " + ', '.join(f'{k} {p:.0%}' for k, v, p in tally(ranked, key)[:3]))
        print(f"  {' ' * len(key)}  우리: " + ', '.join(f'{k} {p:.0%}' for k, v, p in tally(ours_rows, key)[:3]))
    print('  규칙표:', OUT_MD)

if __name__ == '__main__': main()
