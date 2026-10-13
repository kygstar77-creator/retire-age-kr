# naverpost.py 게시판 자동 선택 — 기존 묶음(pkg) 대조 시험
#   py -3.12 -m pytest work/tests/test_board_pick.py -q
# 2026-10-13 게시판 나누기(research/growth/cafe-menu-1013.md '실행 기록') 때 만들었다.
import os, sys, glob, csv, re
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, '..')
sys.path.insert(0, WORK)
import naverpost as N

BOARDS = ['공지사항', '가입인사', '질문·고민', '경제 이야기', '연금/세금/보험', '돈 관리', '성장주', '배당주',
          'ETF', '부동산', '시리즈', '자유게시판']   # 2026-10-13 SideMenuList 실측 순서
OLD_BOARDS = ['공지사항', '가입인사', '질문·고민', '자유게시판']   # 나누기 전
PKGS = sorted(glob.glob(os.path.join(WORK, 'research', '*', 'pkg', 'order.txt')))
CSV_B = os.path.join(WORK, 'research', 'growth', 'cafe-menu-1013b.csv')


def _want(order_path):
    for line in open(order_path, encoding='utf-8').read().splitlines():
        m = re.match(r'^게시판\s*[:：]\s*(.+)$', line.strip())
        if m: return m.group(1).split('·')[0].strip()
    return None


def test_old_menu_behaviour_unchanged():
    # 게시판이 넷뿐이던 때와 같은 답 — 주제 게시판이 없으면 전부 자유게시판
    for t in ('종부세 고령자 공제', '[아파트 시황] 서울', 'SCHD 배당금', '정기예금 금리'):
        assert N.pick_board('자유게시판', OLD_BOARDS, t) == '자유게시판'
    assert N.pick_board('자유게시판', OLD_BOARDS) == '자유게시판'
    assert N.pick_board('미국주식·배당', OLD_BOARDS) == '자유게시판'
    assert N.pick_board('아무거나', []) == '아무거나'      # 목록 조회 실패 때는 예전처럼 그대로 넘긴다


def test_human_boards_never_auto():
    for hb in ('공지사항', '가입인사', '질문·고민'):
        assert N.pick_board(hb, BOARDS, '아무 제목') not in ('공지사항', '가입인사', '질문·고민')


def test_explicit_board_and_fixed_free():
    assert N.pick_board('부동산', BOARDS, 'SCHD 배당금') == '부동산'          # 묶음이 고른 주제 게시판이 이긴다
    assert N.pick_board('자유게시판(고정)', BOARDS, 'SCHD 배당금') == '자유게시판'
    assert N.pick_board('자동', BOARDS, '이번 주 날씨 이야기') == '자유게시판'  # 규칙에 안 걸리면 자유게시판
    assert N.pick_board('자동', BOARDS, '아무 말', '세금연금') == '연금/세금/보험'  # axis 보조


def test_every_existing_pkg_parses_and_picks_a_real_board():
    assert len(PKGS) > 300
    bad = []
    for o in PKGS:
        pkg = os.path.dirname(o)
        if not os.path.exists(os.path.join(pkg, 'title.txt')): continue
        title = open(os.path.join(pkg, 'title.txt'), encoding='utf-8').read().strip()
        want = _want(o) or '자유게시판'
        b = N.pick_board(want, BOARDS, title, N.pkg_axis(pkg))
        if b not in BOARDS or b in N.HUMAN_ONLY: bad.append((pkg, want, b))
    assert not bad, bad[:5]


def test_published_pkgs_match_1013b_table():
    """올라간 묶음(published.txt)의 제목 규칙 답이 손으로 정한 대응표(1013b)와 얼마나 맞나. 90% 이상이어야 한다."""
    table = {r['글번호']: r for r in csv.DictReader(open(CSV_B, encoding='utf-8-sig'))}
    n = ok = 0; miss = []
    for o in PKGS:
        pkg = os.path.dirname(o)
        pub = os.path.join(pkg, 'published.txt')
        if not os.path.exists(pub): continue
        m = re.search(r'cafe\.naver\.com/(?:firemap|ca-fe/cafes/31789001/articles)/(\d+)', open(pub, encoding='utf-8').read())
        if not m or m.group(1) not in table: continue
        r = table[m.group(1)]
        if r['새 게시판(1013b)'] in ('공지사항', '가입인사'): continue
        title = open(os.path.join(pkg, 'title.txt'), encoding='utf-8').read().strip()
        got = N.pick_board(_want(o) or '자유게시판', BOARDS, title, N.pkg_axis(pkg))
        n += 1
        if got == r['새 게시판(1013b)']: ok += 1
        else: miss.append((m.group(1), title[:30], r['새 게시판(1013b)'], got))
    print(f'\n대응표 일치 {ok}/{n}')
    for x in miss: print('  다름', x)
    assert n >= 150 and ok / n >= 0.9
