# 네이버 공개 페이지 읽기(로그인·프로필 없음 → 발행 루틴의 브라우저 프로필과 안 겹친다). WebFetch는 naver.com을 막는다.
#   python work/nvread.py search naver_search "키워드"     # 공식 블로그 글 목록(제목|logNo)
#   python work/nvread.py post naver_search 223367781299 [정규식]   # 본문 전체 또는 정규식에 맞는 줄만
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from urllib.parse import quote
def run(cmd, blog, arg, pat=None):
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True); page = b.new_page(locale='ko-KR')
        if cmd == 'search':
            page.goto(f'https://m.blog.naver.com/PostSearchList.naver?blogId={blog}&searchText={quote(arg)}', wait_until='domcontentloaded'); page.wait_for_timeout(5000)
            items = page.evaluate("() => [...document.querySelectorAll('a')].map(a=>[a.innerText.trim().replace(/\s+/g,' ').slice(0,90), (a.href.match(/logNo=(\d+)/)||[])[1]]).filter(x=>x[1] && x[0].length>8)")
            seen = set()
            for t, l in items:
                if l in seen: continue
                seen.add(l); print(t, '|', l)
        else:
            page.goto(f'https://m.blog.naver.com/PostView.naver?blogId={blog}&logNo={arg}', wait_until='domcontentloaded'); page.wait_for_timeout(5000)
            body = page.evaluate("() => (document.querySelector('.se-main-container')||document.querySelector('#postViewArea')||document.body).innerText")
            date = re.search(r'20\d\d\. ?\d{1,2}\. ?\d{1,2}\.', page.evaluate('document.body.innerText'))
            print('##', page.title()[:80], '|', date.group(0) if date else '?', '| 글자', len(body))
            for line in body.split('\n'):
                l = line.strip()
                if l and (pat is None or re.search(pat, l)): print(l)
        b.close()
if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
