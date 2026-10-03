# work/audit_links.py 링크 관문 테스트 — python3 -m pytest work/tests/test_audit_links.py
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import audit_links as L

PATHS = {'/', '/calc/salary', '/calc/severance', '/calc/unemployment-benefit'}
GOOD = 'https://firemap.kr/calc/salary?utm_source=cafe&utm_medium=post&utm_campaign=ubjob1003'


def kinds(issues, k='거부'):
    return [s for kk, s in issues if kk == k]


def test_good_link_passes():
    urls, issues = L.check_text('x', '계산기: ' + GOOD, PATHS)
    assert urls == [GOOD] and issues == []


def test_missing_medium_rejected():
    _, issues = L.check_text('x', 'https://firemap.kr/?utm_source=cafe&utm_campaign=gift1003', PATHS)
    assert any('utm_medium 없음' in s for s in kinds(issues))


def test_unknown_path_rejected():
    _, issues = L.check_text('x', 'https://firemap.kr/calc/pension?utm_source=cafe&utm_medium=post&utm_campaign=a', PATHS)
    assert any('없는 경로' in s for s in kinds(issues))


def test_uppercase_and_unknown_source_rejected():
    _, issues = L.check_text('x', 'https://firemap.kr/?utm_source=Naver&utm_medium=post&utm_campaign=A-1', PATHS)
    f = kinds(issues)
    assert any('utm_source=Naver' in s for s in f) and any('utm_campaign=A-1' in s for s in f)


def test_two_links_and_campaign_mismatch_rejected():
    t = ('https://firemap.kr/?utm_source=youtube&utm_medium=desc&utm_campaign=d-1\n'
         'https://firemap.kr/calc/salary?utm_source=youtube&utm_medium=desc&utm_campaign=d1')
    f = kinds(L.check_text('x', t, PATHS)[1])
    assert any('링크 2개' in s for s in f) and any('utm_campaign이 서로 다름' in s for s in f)


def test_trailing_punct_and_http():
    f = kinds(L.check_text('x', '여기(http://firemap.kr/?utm_source=cafe&utm_medium=post&utm_campaign=a).', PATHS)[1])
    assert any('http://' in s for s in f)
    f2 = kinds(L.check_text('x', GOOD + '.', PATHS)[1])
    assert any('문장부호' in s for s in f2)


def test_cafe_home_is_warning_not_failure():
    issues = L.check_text('x', '전체 표: https://cafe.naver.com/firemap', PATHS)[1]
    assert kinds(issues) == [] and kinds(issues, '경고')
    assert L.check_text('x', 'https://cafe.naver.com/firemap/187', PATHS)[1] == []


def test_pkg_and_meta_targets(tmp_path):
    pkg = tmp_path / 'abc1003' / 'pkg'; pkg.mkdir(parents=True)
    (pkg / 'title.txt').write_text('제목', encoding='utf-8')
    (pkg / 'c00.txt').write_text('본문 ' + GOOD, encoding='utf-8')
    (pkg / 'c00.txt.orig').write_text('https://firemap.kr/?utm_source=cafe', encoding='utf-8')  # 옛 파일은 안 봄
    (name, text), = L.texts_of(str(pkg))
    assert name == 'abc1003' and GOOD in text and 'c00.txt.orig' not in text and text.count('firemap.kr') == 1
    meta = tmp_path / 'meta.json'
    meta.write_text(json.dumps({'desc': 'https://firemap.kr/?utm_source=youtube&utm_campaign=n-1'}), encoding='utf-8')
    assert L.main([str(pkg)]) == 0
    assert L.main([str(meta)]) == 1


def test_known_paths_reads_toolpages(tmp_path):
    d = tmp_path / 'src' / 'firemap-v2'; d.mkdir(parents=True)
    (d / 'toolPages.js').write_text("[{ path: '/calc/salary', og: 'x' }, { path: '/calc/severance' }]", encoding='utf-8')
    assert L.known_paths(str(tmp_path)) == {'/', '/calc/salary', '/calc/severance'}
