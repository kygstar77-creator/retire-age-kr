# 카페 글을 게시판끼리 옮긴다(삭제 없음). 대응표는 research/growth/cafe-menu-1013b.csv.
#
#   py -3.12 work/cafemove.py rank [글번호]            # 카페 탭 검색 순위(모바일·PC) + 주소 열림 + 지금 게시판
#   py -3.12 work/cafemove.py plan                     # 옮길 글 목록(차례 2 → 3 마지막, 게시판별로 묶음). 화면은 열지 않는다
#   py -3.12 work/cafemove.py move [--max N] [--apply] # 실제 이동. 기본 dry(이동 창만 열고 닫음). --apply 때만 확인을 누른다
#
# 2026-10-13 확인한 화면(관리자 계정, naverpost.py 프로필):
#   - 게시판 목록에서 글 체크 → '이동' 을 누르면 새 창 ArticleMove.nhn?m=view&clubid=&menuid=<지금 게시판>&articleid=<글> 이 뜬다.
#   - 창 안 select#targetmenuid_select 에서 게시판을 고르고 #footer img[alt=확인] → confirm('해당 게시판으로 게시글을 이동하시겠습니까?')
#     → alert('게시글이 이동되었습니다.') → 창이 스스로 닫힌다.
#   - 그래서 이 도구는 목록을 넘기지 않고 그 창 주소를 글마다 바로 연다.
#   - 이동 뒤 확인은 비로그인 글 API(cafe-articleapi v2.1)의 menu.name 으로 한다.
#   - 247번 시험 이동(2026-10-13 17:17): 주소 그대로 200, 카페 탭 1위 그대로.
# 안전: 삭제 버튼은 어디서도 누르지 않는다. 대응표에 없는 글, 지금 게시판이 '지금 게시판' 열과 다른 글은 건너뛴다.
import sys, os, re, csv, json, time, subprocess, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CAFE_ID = '31789001'
CSV = os.path.join(HERE, 'research', 'growth', 'cafe-menu-1013b.csv')
LOG = os.path.join(HERE, 'research', 'growth', 'cafe-move-log.jsonl')
SHOTS = os.path.join(HERE, 'research', '_shots')
UA_M = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
UA_PC = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'
RANK_QUERIES = {'247': ['종부세 고령자 공제 일흔 30%', '종부세 고령자 공제, 올해 일흔이어도 30%인 경우']}

def curl(url, ua=UA_PC):
    # urllib는 검색 페이지에서 403을 받는다(2026-10-13). curl은 된다.
    return subprocess.run(['curl', '-s', '-L', '-A', ua, url], capture_output=True, timeout=40).stdout.decode('utf-8', 'ignore')

def article_board(aid):
    """비로그인 글 API로 지금 게시판 이름. 못 읽으면 None."""
    try:
        d = json.loads(curl(f'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/{CAFE_ID}/articles/{aid}', 'Mozilla/5.0'))
        a = d['result']['article']
        return a['menu']['name'], a['menu']['id']
    except Exception:
        return None

def url_status(aid):
    r = subprocess.run(['curl', '-s', '-o', os.devnull, '-w', '%{http_code}', '-L', f'https://cafe.naver.com/firemap/{aid}'],
                       capture_output=True, timeout=40)
    return r.stdout.decode().strip()

def search_rank(aid, queries):
    """카페 탭 순위. where=m_article 만 주면 통합검색이 온다 — ssc=tab.m_cafe.all / tab.cafe.all 이 카페 탭이다(2026-10-13 확인)."""
    rows = []
    for q in queries:
        for label, base, ua in (('모바일 카페탭', 'https://m.search.naver.com/search.naver?ssc=tab.m_cafe.all&where=m_cafe&query=', UA_M),
                                ('PC 카페탭', 'https://search.naver.com/search.naver?ssc=tab.cafe.all&where=article&query=', UA_PC)):
            h = curl(base + urllib.parse.quote(q), ua)
            seen = []
            for m in re.finditer(r'cafe\.naver\.com/([A-Za-z0-9_-]+)/(\d+)', h):
                k = m.group(1) + '/' + m.group(2)
                if k not in seen: seen.append(k)
            me = f'firemap/{aid}'
            rows.append({'q': q, 'where': label, 'rank': (seen.index(me) + 1) if me in seen else None,
                         'links': len(seen), 'bytes': len(h), 'top3': seen[:3]})
            time.sleep(2)
    return rows

def plan():
    rows = list(csv.DictReader(open(CSV, encoding='utf-8-sig')))
    todo = [r for r in rows if r['이동(1013b)'] == '이동' and r['이동 차례(1013b)'] in ('2', '3 마지막')]
    order = {'2': 0, '3 마지막': 1}
    todo.sort(key=lambda r: (order[r['이동 차례(1013b)']], r['새 게시판(1013b)'], int(r['글번호'])))
    return todo

def log(rec):
    rec['at'] = time.strftime('%Y-%m-%d %H:%M:%S')
    open(LOG, 'a', encoding='utf-8').write(json.dumps(rec, ensure_ascii=False) + '\n')

def move(max_n, apply):
    import naverpost as np_
    from playwright.sync_api import sync_playwright
    todo = plan()
    done = 0
    with sync_playwright() as p:
        ctx = np_.launch(p, True)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            if not np_.logged_in(page, deep=False):
                print('로그인 필요 — 멈춤'); log({'event': 'login_required'}); sys.exit(2)
            for r in todo:
                if done >= max_n: break
                aid, want, was = r['글번호'], r['새 게시판(1013b)'], r['지금 게시판']
                cur = article_board(aid)
                if not cur: print(aid, '글 API 못 읽음 — 건너뜀'); continue
                if cur[0] == want: continue                       # 이미 옮겨짐
                if cur[0] != was: print(aid, f'지금 게시판 {cur[0]} ≠ 대응표 {was} — 건너뜀'); continue
                pop = ctx.new_page()
                msgs = []
                pop.on('dialog', lambda d: (msgs.append(d.message), d.accept()))
                pop.goto(f'https://cafe.naver.com/ArticleMove.nhn?m=view&clubid={CAFE_ID}&menuid={cur[1]}&articleid={aid}',
                         wait_until='domcontentloaded')
                pop.wait_for_timeout(1500)
                sel = pop.locator('#targetmenuid_select')
                if not sel.count():
                    np_.shot(pop, f'cafemove_fail_{aid}'); print(aid, '이동 창이 안 열림 — 멈춤'); log({'id': aid, 'event': 'no_dialog'}); break
                sel.select_option(label=want); pop.wait_for_timeout(1200)
                got = sel.evaluate('e => e.options[e.selectedIndex].text').strip()
                if got != want:
                    print(aid, f'게시판 선택 실패({got}) — 멈춤'); pop.close(); break
                if not apply:
                    print('DRY', aid, was, '→', want, r['제목'][:30]); pop.close(); done += 1; continue
                pop.locator('#footer img[alt="확인"]').click()
                for _ in range(20):
                    if pop.is_closed() or any('이동되었습니다' in m for m in msgs): break
                    time.sleep(0.5)
                if not pop.is_closed(): pop.close()
                time.sleep(1.5)
                after = article_board(aid)
                ok = bool(after and after[0] == want)
                print('MOVE', aid, was, '→', want, 'OK' if ok else f'확인 실패({after})', r['제목'][:30])
                log({'id': aid, 'from': was, 'to': want, 'ok': ok, 'dialogs': msgs})
                if not ok: break
                done += 1
                time.sleep(3)
        finally:
            ctx.close(); np_.release_lock()
    left = sum(1 for r in plan() if (article_board(r['글번호']) or ('',))[0] != r['새 게시판(1013b)']) if apply else None
    print('이번에', done, '편', '/ 남은 것', left)

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'plan'
    if cmd == 'rank':
        aid = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].isdigit() else '247'
        qs = RANK_QUERIES.get(aid) or [sys.argv[3]]
        res = {'at': time.strftime('%Y-%m-%d %H:%M'), 'id': aid, 'url_status': url_status(aid),
               'board': (article_board(aid) or (None,))[0], 'rank': search_rank(aid, qs)}
        print(json.dumps(res, ensure_ascii=False, indent=1))
        log({'event': 'rank', **res})
    elif cmd == 'plan':
        from collections import Counter
        todo = plan()
        print('옮길 글', len(todo), dict(Counter((r['이동 차례(1013b)'], r['새 게시판(1013b)']) for r in todo)))
    elif cmd == 'move':
        n = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 40
        move(n, '--apply' in sys.argv)

if __name__ == '__main__':
    main()
