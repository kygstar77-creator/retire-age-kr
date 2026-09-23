# 이미 올라간 블로그 글을 손본다. 지금은 비공개 전환만 한다(지우지 않는다 — 되돌릴 수 있게).
#
#   py -3.12 work/blogfix.py private 224421542224 [<logNo> ...]
#
# 쓰는 곳: 같은 글이 두 번 올라갔을 때 뒤에 올라간 쪽, 기준 미달로 내려야 하는 글.
# 2026-09-24: 국채금리 글이 07:13·07:35 두 번 올라가 뒤엣것을 이걸로 내렸다.
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from naverpost import launch, logged_in, close_popups, shot, BLOG_ID


def make_private(page, log_no):
    page.goto(f'https://blog.naver.com/PostUpdateForm.naver?blogId={BLOG_ID}&logNo={log_no}',
              wait_until='domcontentloaded')
    page.wait_for_timeout(7000)
    frame = page.main_frame
    for f in page.frames:
        if f != page.main_frame and ('postwrite' in f.url.lower() or 'update' in f.url.lower()): frame = f
    close_popups(frame)
    frame.locator('button[class^="publish_btn"]').first.click(); page.wait_for_timeout(2500)
    shot(page, f'private_panel_{log_no}')
    frame.locator('label:has-text("비공개")').first.click(); page.wait_for_timeout(500)
    frame.get_by_role('button', name=re.compile(r'^\s*발행\s*$')).last.click()
    page.wait_for_url(re.compile(r'logNo=\d+|blog\.naver\.com/' + BLOG_ID + r'/\d+'), timeout=30000)
    page.wait_for_timeout(2000)
    return page.url


def is_public(log_no):
    """공개 목록(로그인 없이 보이는 글 목록)에 아직 있나. 비공개가 되면 사라진다."""
    from naverpost import live_map
    return any(u.endswith('/' + str(log_no)) for u in live_map('blog').values())


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd != 'private' or len(sys.argv) < 3:
        print(__doc__ or 'py -3.12 work/blogfix.py private <logNo> ...'); sys.exit(2)
    nos = sys.argv[2:]
    with sync_playwright() as p:
        ctx = launch(p, headless=os.environ.get('NAVER_HEADED') != '1')
        page = ctx.new_page()
        try:
            if not logged_in(page): print('로그인 안 됨 — py -3.12 work/naverpost.py login'); sys.exit(2)
            bad = 0
            for no in nos:
                try:
                    make_private(page, no)
                    ok = not is_public(no)          # 화면 말고 공개 목록으로 확인한다
                    print(('비공개 확인 ' if ok else '비공개 안 됨 ') + no)
                    bad += (not ok)
                except Exception as e:
                    print('실패', no, repr(e)[:200]); shot(page, 'error_private_' + str(no)); bad += 1
            sys.exit(1 if bad else 0)
        finally:
            ctx.close()


if __name__ == '__main__':
    main()
