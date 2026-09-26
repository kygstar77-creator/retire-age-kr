# 네이버 카페에서 잘 읽히는 글의 말투 실측 — "AI 티 나는 카페 글"을 고치기 위한 근거(사장님 2026-09-23).
#   python work/cafelearn.py "파이어족 배당금 생활" "커버드콜 월배당" "국민연금 조기수령" ...
#   → 통합검색 카페탭 상위 글(전체공개만 읽힘)의 본문을 모아 work/research/cafe_style/benchmark_<날짜>.md 에
#     어미 분포·문장 길이·1인칭·첫 문장·마지막 문장·표본 문장을 적는다. 우리 글과 같은 자로 비교한다.
#
# 우리 글 쪽은 매번 **우리 카페에 실제로 올라간 최근 글**을 다시 읽어 ours_*.txt를 갈아치운다.
# 2026-09-26 확인: ours_*.txt 5개가 9/23 13:26에 손으로 받아 둔 것 그대로였다. 그래서 9/26 실측표가
# 경쟁 글은 그날 것, 우리 글은 사흘 전 것으로 견주고 있었고(문장 48자·조문번호 17%),
# 그 사이 selfcheck 말투 기준으로 고쳐 쓴 글은 표본에 한 편도 안 들어왔다.
import sys, os, re, json, time, glob, collections, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'research', 'cafe_style'); os.makedirs(OUT, exist_ok=True)
JS = "() => { const c=document.querySelector('.se-main-container')||document.querySelector('#tbody')||document.querySelector('.ContentRenderer'); return c? c.innerText : '' }"

def stats(texts):
    sents = []
    for t in texts:
        for s in re.split(r'(?<=[.!?~ㅎㅋ])\s+|\n+', t):
            s = s.strip()
            if 4 <= len(s) <= 200: sents.append(s)
    end = collections.Counter()
    for s in sents:
        m = re.search(r'(습니다|입니다|네요|해요|예요|이에요|거든요|더라고요|더라구요|죠|까요|ㄴ다|는다|다|요|ㅎㅎ|ㅋㅋ)[.!?~]*$', s)
        end[m.group(1) if m else '기타'] += 1
    lens = sorted(len(s) for s in sents) or [0]
    first = sum(1 for s in sents if re.search(r'저는|제가|저도|우리|제 ', s))
    emo = sum(1 for s in sents if re.search(r'ㅎㅎ|ㅋㅋ|ㅠ|\^\^|!', s))
    q = sum(1 for s in sents if s.endswith('?'))
    law = sum(1 for s in sents if re.search(r'제\d+조|시행령|법률 제|공포번호', s))
    return sents, end, lens, first, emo, q, law

UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cafe.naver.com/'}
CAFE_ID = '31789001'; CAFE_URL = 'firemap'

def our_articles(n=10):
    """우리 카페 최근 글 목록(articleId). textloop.cafe_posts와 같은 API를 쓴다."""
    u = (f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={CAFE_ID}'
         f'&search.queryType=lastArticle&search.page=1&search.perPage={max(n, 20)}')
    try:
        arts = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25))['message']['result']['articleList']
    except Exception as e:
        print('우리 글 목록 실패:', str(e)[:80]); return []
    out = []
    for a in arts:
        aid = a.get('articleId')
        if aid: out.append((aid, a.get('subject', ''), a['writeDateTimestamp'] / 1000))
        if len(out) >= n: break
    return out

def refresh_ours(page, body_of, n=8):
    """우리 카페 최근 글 본문을 다시 읽어 ours_*.txt를 갈아치운다.
    3편도 못 읽으면 옛 파일을 그대로 둔다 — 표본을 비우는 것이 사흘 묵은 표본보다 나쁘다."""
    arts = our_articles(n); fresh = {}
    for aid, title, ts in arts:
        try:
            body = body_of(page, f'https://cafe.naver.com/{CAFE_URL}/{aid}')
        except Exception as e:
            print('   우리 글 실패', aid, str(e)[:40]); continue
        if len(body) > 300:
            fresh[aid] = body; print('   우리 글 ok', aid, len(body), '자 |', title[:40])
        else:
            print('   우리 글 본문 못 읽음', aid, '|', title[:40])
    if len(fresh) < 3:
        print(f'   우리 글 {len(fresh)}편만 읽혀 옛 표본을 그대로 둔다'); return None
    for f in glob.glob(os.path.join(OUT, 'ours_*.txt')): os.remove(f)
    for aid, body in fresh.items():
        open(os.path.join(OUT, f'ours_{aid}.txt'), 'w', encoding='utf-8').write(body)
    days = sorted(time.strftime('%m-%d', time.localtime(ts)) for aid, t, ts in arts if aid in fresh)
    return {'n': len(fresh), 'from': days[0], 'to': days[-1]}

def read_body(page, url):
    page.goto(url, wait_until='domcontentloaded'); page.wait_for_timeout(4000)
    best = ''
    for fr in page.frames:
        try:
            x = fr.evaluate(JS)
            if len(x) > len(best): best = x
        except Exception: pass
    return re.sub(r'[​ ]+', ' ', best).strip()

def main():
    qs = sys.argv[1:] or ['파이어족 배당금 생활', '커버드콜 월배당 후기', '국민연금 조기수령 고민', '아파트 갭투자 후기', 'ISA 계좌 연금저축 어떻게']
    posts = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True); page = b.new_page(locale='ko-KR')
        for q in qs:
            page.goto('https://search.naver.com/search.naver?ssc=tab.cafe.all&query=' + urllib.parse.quote(q), wait_until='domcontentloaded'); page.wait_for_timeout(4000)
            links = page.evaluate("() => [...document.querySelectorAll('a[href*=\"cafe.naver.com/\"]')].map(a=>[a.innerText.trim().replace(/\\s+/g,' ').slice(0,70), a.href]).filter(x=>/cafe\\.naver\\.com\\/[^/]+\\/\\d+/.test(x[1]) && x[0].length>5)")
            seen = set(); picked = []
            for t, u in links:
                key = re.sub(r'\?.*', '', u)
                if key in seen: continue
                seen.add(key); picked.append((t, key))
                if len(picked) >= 6: break
            print(f'== "{q}" 상위 글 {len(picked)}개')
            for t, u in picked:
                try:
                    page.goto(u, wait_until='domcontentloaded'); page.wait_for_timeout(4000)
                    best = ''
                    for fr in page.frames:
                        try:
                            x = fr.evaluate(JS)
                            if len(x) > len(best): best = x
                        except Exception: pass
                    best = re.sub(r'[​\xa0]+', ' ', best).strip()
                    if len(best) > 300:
                        posts.append({'q': q, 'title': t, 'url': u, 'text': best}); print('   ok', len(best), '자 |', t[:45])
                    else: print('   본문 못 읽음(멤버공개일 수 있음) |', t[:45])
                except Exception as e: print('   실패', str(e)[:50])
        print('== 우리 카페 최근 글 다시 읽기')
        ours_at = refresh_ours(page, read_body)
        b.close()
    day = time.strftime('%Y-%m-%d')
    json.dump(posts, open(os.path.join(OUT, f'benchmark_{day}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    ours = [open(f, encoding='utf-8').read() for f in glob.glob(os.path.join(OUT, 'ours_*.txt'))]
    ours_note = (f"우리 글 {ours_at['n']}편(카페 {ours_at['from']}~{ours_at['to']} 발행, 이번에 다시 읽음)"
                 if ours_at else f'우리 글 {len(ours)}편(**이번에 다시 읽지 못해 옛 표본**)')
    out = [f'# 카페 글 말투 실측 {day} — 잘 읽히는 글 {len(posts)}편 vs {ours_note}', '']
    for name, texts in (('잘 읽히는 카페 글', [p['text'] for p in posts]), ('우리 카페 글', ours)):
        if not texts: continue
        sents, end, lens, first, emo, q, law = stats(texts); n = len(sents) or 1
        out += [f'## {name} (문장 {n}개)',
                '- 어미: ' + ' · '.join(f'{k} {v*100//n}%' for k, v in end.most_common(8)),
                f'- 문장 길이 중앙값 {lens[len(lens)//2]}자 / 상위 25% {lens[int(len(lens)*0.75)]}자',
                f'- 1인칭(저는·제가) 문장 {first*100//n}% · 감탄/ㅎㅎ/! {emo*100//n}% · 물음표 {q*100//n}% · 조문 번호 언급 {law*100//n}%', '']
    out += ['## 잘 읽히는 글의 첫 문장', *[f"- [{p['title'][:30]}] {p['text'].split(chr(10))[0][:100]}" for p in posts[:15]], '',
            '## 잘 읽히는 글의 마지막 문장', *[f"- {[s for s in p['text'].split(chr(10)) if s.strip()][-1][:100]}" for p in posts[:15]], '']
    import random; random.seed(2)
    sents, *_ = stats([p['text'] for p in posts])
    out += ['## 표본 문장 40', *[f'- {s}' for s in random.sample(sents, min(40, len(sents)))]]
    p = os.path.join(OUT, f'benchmark_{day}.md'); open(p, 'w', encoding='utf-8').write('\n'.join(out)); print('저장', p); print('\n'.join(out[:14]))

if __name__ == '__main__': main()
