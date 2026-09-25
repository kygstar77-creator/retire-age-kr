# 태그 수 측정기 — audit [1]의 "태그 12~15개" 규칙에 근거를 채우려고 만들었다(2026-09-25).
#   py -3.12 work/tagstudy.py                  → 기본 검색어로 상위 노출 글의 태그 수를 잰다
#   py -3.12 work/tagstudy.py "코픽스" "VYM 배당"
#
# 왜: 규칙표에 "태그 12~15개"가 근거 없이 들어 있었다. 9/24 회차가 태그를 읽는 경로
# (blog.naver.com/BlogTagListInfo.naver)는 찾았지만 블로그탭 검색이 반복 호출로 막혀
# (응답 29바이트) 상위 글 표본을 못 모아 근거를 못 채웠다.
# 여기서는 검색어 사이에 쉬어 가며 조금씩 모으고, 몇 편을 실제로 쟀는지 그대로 적는다.
import sys, os, re, json, time, statistics, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/126 Safari/537.36',
      'Referer': 'https://search.naver.com/'}
KEYWORDS = ['코픽스', 'VYM 배당', 'SCHD 배당', '연금저축 세액공제', '전세가율']

def get(u, ref=None):
    h = dict(UA)
    if ref: h['Referer'] = ref
    try: return urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=25).read().decode('utf-8', 'ignore')
    except Exception as e: print('  가져오기 실패:', str(e)[:60]); return ''

def top_posts(kw):
    """블로그탭 상위에 실제로 뜬 글의 (blogId, logNo). 차단되면 빈 목록."""
    s = get('https://search.naver.com/search.naver?ssc=tab.blog.all&query=' + urllib.parse.quote(kw))
    if len(s) < 2000: print(f'  [{kw}] 검색 차단 의심 — 응답 {len(s)}바이트'); return []
    out, seen = [], set()
    for m in re.finditer(r'https://blog\.naver\.com/([A-Za-z0-9_-]+)/(\d{8,})', s):
        k = m.group(1, 2)
        if k not in seen: seen.add(k); out.append(k)
    return out

def tags_of(blog_id, log_no):
    """글 하나의 태그 목록. 로그인 없이 JSON으로 나온다."""
    u = (f'https://blog.naver.com/BlogTagListInfo.naver?blogId={blog_id}'
         f'&logNoList={log_no}&logType=mylog')
    s = get(u, ref=f'https://blog.naver.com/{blog_id}/{log_no}')
    m = re.search(r'"tagName"\s*:\s*"([^"]*)"', s)
    if not m: return None
    # tagName은 URL 인코딩된 한 줄이고 태그 구분자 쉼표도 %2C로 들어 있다(2026-09-25 실측).
    # 인코딩된 채로 쉼표를 찾으면 언제나 1개로 세어진다.
    raw = urllib.parse.unquote(m.group(1))
    return [t.strip() for t in raw.split(',') if t.strip()]

def main():
    kws = sys.argv[1:] or KEYWORDS
    counts, rows = [], []
    for kw in kws:
        posts = top_posts(kw)[:10]
        print(f'[{kw}] 상위 글 {len(posts)}편')
        for bid, lno in posts:
            tg = tags_of(bid, lno)
            time.sleep(1.2)
            if tg is None: continue
            counts.append(len(tg)); rows.append({'kw': kw, 'blog': bid, 'log': lno, 'n': len(tg)})
            print(f'   {len(tg):2d}개  {bid}/{lno}')
        time.sleep(3)
    if not counts:
        print('잰 글 0편 — 근거를 채울 수 없다. 규칙은 그대로 "근거 없음"으로 둔다.'); return 1
    counts.sort()
    print(f'\n--- 잰 글 {len(counts)}편 · 태그 수 중앙값 {statistics.median(counts):.0f}개 '
          f'· 최소 {counts[0]} · 최대 {counts[-1]}')
    in_rule = sum(1 for c in counts if 12 <= c <= 15)
    print(f'    12~15개 구간에 든 글 {in_rule}/{len(counts)}편 ({in_rule*100//len(counts)}%)')
    out = os.path.join(HERE, 'tagstudy.json')
    json.dump({'at': time.strftime('%Y-%m-%d %H:%M'), 'n': len(counts),
               'median': statistics.median(counts), 'min': counts[0], 'max': counts[-1],
               'in_12_15': in_rule, 'rows': rows}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('기록:', out)
    return 0

if __name__ == '__main__':
    sys.exit(main())
