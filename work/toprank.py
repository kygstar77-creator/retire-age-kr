# 상위 글 내용 분석기 — 목표 검색어로 네이버 블로그 탭 상위 글 본문을 읽어
# (1) 각 글이 뭘 담았는지 (2) 상위 글 다수가 쓰는데 내 초안에 없는 항목을 뽑는다.
# HTTP만 쓰므로 스크린샷 비용 없음. 공개 페이지만 읽는다.
# 사용: python toprank.py "검색어" [내초안.txt] [상위N=8]
import sys, re, html, time, json, urllib.request, urllib.parse, collections, os
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'}
MUA = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Mobile Safari/604.1'}

def get(u, h=UA, t=20):
    try: return urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=t).read().decode('utf-8', 'ignore')
    except Exception as e: return ''

def search(kw, n):
    s = get('https://search.naver.com/search.naver?ssc=tab.blog.all&query=' + urllib.parse.quote(kw))
    dates = re.findall(r'>(\d{4}\.\d{1,2}\.\d{1,2}\.|\d+(?:일|시간|분|주|개월) 전|어제)<', s)
    seen, out = set(), []
    for m in re.finditer(r'blog\.naver\.com/([A-Za-z0-9_-]{3,30})/(\d{9,})', s):
        k = m.group(1) + '/' + m.group(2)
        if k in seen: continue
        seen.add(k); out.append((m.group(1), m.group(2)))
        if len(out) >= n: break
    return out, dates[:n]

def post(bid, no):
    p = get(f'https://m.blog.naver.com/{bid}/{no}', MUA, 25)
    if not p: return None
    i = p.find('se-main-container'); body = p[i:] if i > 0 else p
    j = body.find('post_footer'); body = body[:j] if j > 0 else body
    paras = [re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', x))).strip()
             for x in re.findall(r'<p class="se-text-paragraph[^>]*>(.*?)</p>', body, re.S)]
    paras = [x for x in paras if x and x != '\u200b']
    ti = re.search(r'<meta property="og:title" content="([^"]*)"', p)
    return {'id': bid, 'no': no, 'title': html.unescape(ti.group(1)) if ti else '',
            'paras': paras, 'chars': sum(len(x) for x in paras),
            'imgs': len(set(re.findall(r'data-lazy-src="([^"?]+)', body)))}

STOP = set('것 수 등 때 점 분 이 그 저 곳 중 내 더 잘 후 전 및 년 월 일 원 명 개 번 차 말 말씀 경우 대해 통해 위해 우리 여러분 오늘 이번 지난 최근 정도 관련 내용 확인 가능 필요 생각 사람 부분 이상 이하 다음 각각 모두 정말 진짜 바로 특히 물론 거의 자신 여기 저기 사실 이유 방법 기준 시작 가지 얘기 이야기 블로그 포스팅 안녕 감사 구독 이웃 공감 댓글 참고 아래 위 링크 사진 이미지'.split())

_kiwi = None
def kiwi():
    global _kiwi
    if _kiwi is None:
        from kiwipiepy import Kiwi
        _kiwi = Kiwi()
    return _kiwi

def terms(txt):
    """명사(고유명사 포함)와 붙어 있는 명사 묶음(복합명사)을 뽑는다."""
    out = collections.Counter()
    for sent in kiwi().tokenize(txt):
        pass
    toks = kiwi().tokenize(txt)
    run = []
    for t in toks:
        if t.tag in ('NNG', 'NNP', 'SL'):
            run.append(t.form)
        else:
            if run:
                for i in range(len(run)):
                    for j in range(i + 1, min(i + 4, len(run)) + 1):
                        g = ''.join(run[i:j])
                        if len(g) >= 2 and g not in STOP and not g.isdigit():
                            out[g] += 1
                run = []
    if run:
        for i in range(len(run)):
            for j in range(i + 1, min(i + 4, len(run)) + 1):
                g = ''.join(run[i:j])
                if len(g) >= 2 and g not in STOP and not g.isdigit():
                    out[g] += 1
    return out

def nums(txt):
    pats = [r'\d[\d,]*\.?\d*\s?(?:만원|억원|원|만명|명|퍼센트|%p|%포인트|%|년|개월|월|일|주|배|회|세|조원|억|만)']
    out = collections.Counter()
    for p in pats:
        for m in re.findall(p, txt): out[re.sub(r'\s', '', m)] += 1
    return out

def main():
    kw = sys.argv[1]
    draft = ''
    if len(sys.argv) > 2 and os.path.exists(sys.argv[2]): draft = open(sys.argv[2], encoding='utf-8').read()
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    hits, dates = search(kw, n)
    print(f'=== "{kw}" 블로그 탭 상위 {len(hits)}개')
    posts = []
    for i, (bid, no) in enumerate(hits):
        d = post(bid, no); time.sleep(0.7)
        if not d: print(f'  {i+1}. (본문 못 읽음) {bid}/{no}'); continue
        d['date'] = dates[i] if i < len(dates) else ''
        posts.append(d)
        head = [x for x in d['paras'] if 4 < len(x) < 34][:5]
        print(f"\n  {i+1}. {d['title'][:58]}")
        print(f"     {d['date']} | {d['chars']}자 | 사진 {d['imgs']}장 | blog.naver.com/{bid}/{no}")
        if head: print('     짧은 줄(소제목 후보): ' + ' / '.join(head))
    if not posts: return
    alltxt = '\n'.join('\n'.join(p['paras']) for p in posts)
    print(f"\n=== 상위 글 평균: {sum(p['chars'] for p in posts)//len(posts)}자, 사진 {sum(p['imgs'] for p in posts)//len(posts)}장")
    # 여러 글이 공통으로 쓰는 말 중 내 초안에 없는 것
    docfreq = collections.Counter()
    for p in posts:
        for t in set(terms('\n'.join(p['paras']))): docfreq[t] += 1
    half = max(2, len(posts) // 2 + 1)
    cand = [(c, t) for t, c in docfreq.items() if c >= half and len(t) >= 3]
    # 부분문자열 제거(긴 것 우선)
    cand.sort(key=lambda x: (-x[0], -len(x[1])))
    kept = []
    for c, t in cand:
        if any(t in k and t != k for _, k in kept): continue
        kept.append((c, t))
    kept = [(c, t) for c, t in kept if len(t) >= 2]
    miss = [(c, t) for c, t in kept if draft and t not in draft]
    print(f"\n=== 상위 글 {half}편 이상이 쓰는데 내 초안에 없는 말 (상위 30)")
    for c, t in miss[:30]: print(f"   {c}/{len(posts)}편  {t}")
    dn = nums(alltxt); mynum = nums(draft)
    misn = [(c, t) for t, c in dn.most_common(60) if c >= 2 and t not in mynum]
    print(f"\n=== 상위 글에 2번 이상 나오는데 내 초안에 없는 숫자 (상위 25)")
    for c, t in misn[:25]: print(f"   {c}회  {t}")
    json.dump({'kw': kw, 'posts': [{k: v for k, v in p.items() if k != 'paras'} for p in posts],
               'missing_terms': miss[:60], 'missing_numbers': misn[:40]},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'toprank_last.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# bodystudy.py가 search()·post()를 가져다 쓴다. 가드가 없으면 import만 해도 main이 돈다.
if __name__ == '__main__': main()
