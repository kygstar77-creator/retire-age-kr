# work/audit_text.py 카페 글짓기 관문 테스트 — python3 -m pytest work/tests/test_audit_text.py
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import audit_text as T

BASE = {'n': 3, 'dens_med': 80, 'dens_max': 150, 'multi_med': 20, 'multi_max': 40}


def make(tmp_path, name, title, body):
    p = tmp_path / name / 'pkg'; p.mkdir(parents=True)
    (p / 'title.txt').write_text(title, encoding='utf-8')
    (p / 'c00.txt').write_text(body, encoding='utf-8')
    return str(p)


def test_density_counts_numbers_like_speechcompare():
    d, m, w = T.density('월 2만 2,800원이에요. 그다음은 쉬어요.')
    assert w == 5 and round(d) == round(1000 * 2 / 5) and m == 50.0


def test_density_skips_tables_and_urls():
    d, _, _ = T.density('| 1 | 2 | 3 |\nhttps://firemap.kr/?utm_campaign=a1\n말로 하는 문장이에요.')
    assert d == 0


def test_number_heavy_post_rejected_and_plain_post_passes(tmp_path):
    heavy = make(tmp_path, 'heavy', '배당 얼마일까?', '1년 3.2% 4,000만원 12개월 0.25달러 7.5%였어요. 2,800원 3,100원 4.4%예요.')
    plain = make(tmp_path, 'plain', '배당은 왜 줄었을까', '배당이 줄었어요. 회사가 이익을 더 남겨 두기로 했거든요. 그래도 1년 전보다는 많아요.')
    r = T.audit([heavy, plain], BASE)
    by = {x['name']: x for x in r['posts']}
    assert any('숫자 밀도' in f for f in by['heavy']['fails'])
    assert any('숫자 2개+' in f for f in by['heavy']['fails'])
    assert by['plain']['fails'] == []


def test_rules_jargon_rejected(tmp_path):
    p = make(tmp_path, 'j', '연봉 상위', '상위 1%가 낸 결정세액 몫이 커요. 총급여 기준이에요.')
    fails = T.audit([p], BASE)['posts'][0]['fails']
    assert any("'결정세액'" in f for f in fails) and any("'몫'" in f for f in fails) and any("'총급여'" in f for f in fails)
    assert T.jargon_hits('상위 51%부터 100%까지')[0][1] == '아래 절반'


def test_comma_title_template_rejected_when_all_comma(tmp_path):
    ps = [make(tmp_path, f'p{i}', f'키워드{i}, 이야기', '말이에요.') for i in range(8)]
    assert any(k == '거부' and '쉼표 없는 제목 0/8' in s for k, s in T.audit(ps, BASE)['batch'])
    ps[0] = make(tmp_path, 'q0', '질문 한 문장이면 어떨까', '말이에요.')
    ps[1] = make(tmp_path, 'q1', '숫자 하나로 끝나는 제목', '말이에요.')
    assert not any(k == '거부' for k, s in T.audit(ps, BASE)['batch'])


def test_shared_phrase_warning():
    bodies = {f'p{i}': f'글{i} 내용이에요. 자료 정리와 초안 작성에 생성형 AI를 썼습니다.' for i in range(5)}
    bodies['p5'] = '전혀 다른 마무리예요.'
    got = dict(T.shared_phrases(bodies))
    assert '자료 정리와 초안 작성에' in got and len(got['자료 정리와 초안 작성에']) == 5


def test_baseline_from_repo_benchmark():
    b = T.baseline()
    if b is None:  # 표본 파일이 없는 체크아웃
        return
    assert b['n'] >= 10 and b['dens_med'] < b['dens_max']
