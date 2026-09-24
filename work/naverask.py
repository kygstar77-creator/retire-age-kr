# 네이버 고객센터 '검색 노출 정상화' 문의 — 폼을 열고 구조를 보거나, 내용을 채워 제출한다.
#   py -3.12 work/naverask.py look                 # 폼이 어떻게 생겼는지만 본다(제출 안 함)
#   py -3.12 work/naverask.py fill  <본문파일>      # 채우기만 하고 멈춘다(사람이 확인 후 제출)
#   py -3.12 work/naverask.py send  <본문파일>      # 채우고 제출까지
#
# 사장님 2026-09-25: "니가 요청 넣어줘."
# 2026-09-24 새벽 이후 블로그 신규 글이 검색에서 빠졌다. 중복 발행 두 쌍을 내리고
# 발행량·간격을 고친 뒤 정상화를 요청한다. 공식 창구는 categoryNo=5228 하나뿐이다
# (5749는 남을 신고하는 곳이라 우리 건이 아니다).
#
# 안내문에 이렇게 적혀 있다 — "반영 여부 및 시기는 보장되지 않으며 개별 답변을 드리지 않습니다."
# 답장은 안 온다. 넣었다는 기록만 남는다.
import sys, os, time
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from naverpost import launch, shot, SHOTS

URL = 'https://help.naver.com/inquiry/input.help?categoryNo=5228&serviceNo=5626&lang=ko'

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'look'
    body = ''
    if len(sys.argv) > 2:
        body = open(sys.argv[2], encoding='utf-8').read().strip()
    with sync_playwright() as p:
        ctx = launch(p, headless=os.environ.get('NAVER_HEADED') != '1')
        page = ctx.new_page()
        try:
            page.goto(URL, wait_until='domcontentloaded', timeout=60000)
            page.wait_for_timeout(5000)
            print('주소:', page.url)
            if 'nidlogin' in page.url or 'nid.naver.com' in page.url:
                print('로그인이 필요하다 — py -3.12 work/naverpost.py login 을 먼저 돌린다')
                shot(page, 'ask_login'); return

            # 입력칸이 무엇무엇인지 그대로 훑는다(이름을 지어내지 않는다)
            fields = page.evaluate("""() => [...document.querySelectorAll('input,textarea,select')]
                .filter(e => e.type !== 'hidden')
                .map(e => ({tag: e.tagName, type: e.type||'', name: e.name||'', id: e.id||'',
                            ph: e.placeholder||'', label: (e.labels&&e.labels[0]?e.labels[0].innerText:'').trim().slice(0,30)}))""")
            print(f'입력칸 {len(fields)}개')
            for f in fields: print('  ', f)
            btns = page.evaluate("""() => [...document.querySelectorAll('button,a[role=button],input[type=submit]')]
                .map(e => (e.innerText||e.value||'').trim()).filter(t => t && t.length < 20).slice(0, 25)""")
            print('버튼:', btns)
            print('스크린샷', shot(page, 'ask_form'))

            if cmd == 'look': return
            if not body: print('본문 파일이 없다'); return

            # 이 창구는 사연을 적는 곳이 아니다. 받는 것은 게시물 URL 최대 3개뿐이고
            # 아이디·이메일은 로그인에서 자동으로 채워진다(2026-09-25 화면 확인).
            # 그래서 '무엇을 적느냐'가 아니라 '어느 글을 넣느냐'가 전부다.
            urls = [x.strip() for x in body.splitlines() if x.strip().startswith('http')][:3]
            if not urls: print('넣을 글 주소가 없다'); return
            for i, fid in enumerate(['requiredUrl1', 'requiredUrl11', 'requiredUrl12']):
                if i >= len(urls): break
                el = page.locator('#' + fid)
                if not el.count(): print('입력칸 없음:', fid); continue
                el.click(); el.fill(urls[i]); page.wait_for_timeout(300)
                print(f'  {fid} ← {urls[i]}')
            page.wait_for_timeout(500)
            print('스크린샷', shot(page, 'ask_filled'))
            if cmd != 'send':
                print('채우기만 했다. 제출하려면 send 로 다시 돌린다.'); return

            for name in ('문의하기', '보내기', '등록', '접수'):
                b = page.get_by_role('button', name=name)
                if b.count():
                    b.first.click(); page.wait_for_timeout(4000)
                    print('제출 눌렀다:', name); break
            else:
                print('제출 버튼을 못 찾았다'); return
            print('제출 뒤 주소:', page.url)
            print('스크린샷', shot(page, 'ask_done'))
        finally:
            ctx.close()

if __name__ == '__main__': main()
