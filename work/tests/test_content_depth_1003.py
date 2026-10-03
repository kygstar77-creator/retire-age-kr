# content-depth-1003 보강 계산이 저장소 원자료 사본에서 같은 값을 내는지 확인 (R-1 facts.additions-1003.txt 근거)
import importlib.util, os

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location('cd1003', os.path.join(HERE, '..', 'research', 'cloud', 'content_depth_1003_calc.py'))
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def test_verify_matches_facts():
    v = M.verify()
    assert v['예금1년']['202508'] == 2.51 and v['예금1년']['202608'] == 3.39 and v['예금1년']['202510'] == 2.58
    assert v['CPI'][2] == 3.09
    assert v['FX'] == ('1406', '1359.6', -3.3)
    assert v['끝값_나스닥'] == {'SPY': 769.64, 'SCHD': 32.72, 'GLD': 380.14}
    assert v['SCHD_분배_슈왑_합'] == 1.0541
    assert v['SPY_분배_FMP_합'] == 7.58272


def test_additions():
    a = M.additions()
    assert a['SPY_4번째']['pay'] == '2026-10-30'
    assert a['SCHD_지급일환율_세후합'] == 3421445
    assert a['SCHD_끝날환율_세후합(facts방식)'] == 3169043
    assert a['SCHD_분배_변화%'] == 1.95
    assert a['SCHD_자본이득분배_합'] == 0.0
    r = a['시작일별_순위']
    assert r['시작일수'] == 251 and r['순위분포']['SCHD>SPY>GLD'] == 25
    assert a['건보_검산_1001만'] == 67850 and a['건보_검산_1000만'] == 22800
    assert a['3억_건보_월'] == 68930 and a['2억_건보_월'] == 22800
