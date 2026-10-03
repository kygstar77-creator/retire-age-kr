# 대본 말투 관문(aitell --script)과 speechcompare 지표·LOO 테스트 — 10/3 클라우드 ①
#   python3 -m pytest work/tests/test_script_gate.py
import os, sys, json, importlib.util

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WORK)
import aitell  # noqa: E402

spec = importlib.util.spec_from_file_location('speechcompare', os.path.join(WORK, 'research', 'longform', 'loop', 'speechcompare.py'))
sc = importlib.util.module_from_spec(spec); spec.loader.exec_module(sc)
EP = os.path.join(WORK, 'research', 'longform', 'ep')


def test_number_counts_per_sentence():
    t = '연봉은 4,475만원입니다. 위에서 35%와 36% 사이예요. 숫자가 없는 문장이에요. 2,107만 8,535명에 3개 숫자요.'
    m = sc.metrics(t)
    assert m['문장수'] == 4
    assert m['숫자 0개 문장 %'] == 25.0
    assert m['숫자 1개 문장 %'] == 25.0
    assert m['숫자 2개 문장 %'] == 25.0
    assert m['숫자 3개+ 문장 %'] == 25.0
    assert m['숫자 하나 이하 문장 %'] == 50.0
    assert m['숫자 2개 이상 문장 %'] == 50.0
    assert m['질문 문장 %'] == 0.0


def test_markers_and_questions():
    m = sc.metrics('그런데 이건 뭘까요? 근데 사실 그렇지 않아요. 그리고 이제 봅니다.')
    assert m['질문 문장 %'] == round(100 / 3, 1)
    assert m['접속사·추임새 종류'] >= 4      # 그런데·근데·사실·그리고·이제


def test_loo_perfect_on_separable_and_rule_direction():
    rows = [(f'h{i}', {'x': v}, True) for i, v in enumerate([40, 50, 52, 60, 91])] + \
           [(f'o{i}', {'x': v}, False) for i, v in enumerate([148, 187, 188, 197])]
    assert sc.loo(rows, ('x',)) == 1.0
    (f, c, d), = sc.fit_rule(rows, ('x',))
    assert d == 'le' and 91 < c < 148
    assert sc.edge(rows, 'x', 'le') == 91


def test_loo_two_metrics_and_noise():
    rows = [('h', {'a': 1, 'b': 1}, True), ('h', {'a': 2, 'b': 1}, True), ('h', {'a': 1, 'b': 2}, True),
            ('o', {'a': 9, 'b': 9}, False), ('o', {'a': 8, 'b': 9}, False), ('o', {'a': 9, 'b': 8}, False)]
    assert sc.loo(rows, ('a', 'b')) == 1.0
    mixed = [('h', {'a': 1}, True), ('o', {'a': 1}, False), ('h', {'a': 2}, True), ('o', {'a': 2}, False)]
    assert sc.loo(mixed, ('a',)) <= 0.5


def test_script_say_strips_screen_and_caption_markers(tmp_path):
    p = tmp_path / 's.md'
    p.write_text('# 제목 2026 10 03\n작성 메모 1 2 3\n## 1. 칸\n  (화면: 9억 9,937만원)\n'
                 '- 거의 10억원입니다. [자막: 평균 9억 9,937만원]\n- 숫자 없는 말이에요.\n', encoding='utf-8')
    t = aitell.script_say(str(p))
    assert t == '거의 10억원입니다. 숫자 없는 말이에요.'


def test_script_score_pass_and_fail():
    dense = ' '.join(f'{i}만원과 {i + 1}%가 있습니다.' for i in range(1, 30))
    ok, m, bad = aitell.script_score(dense, aitell.SCRIPT_RULES)
    assert not ok and len(bad) == 2
    calm = ' '.join(['이건 숫자가 없는 평범한 말입니다.'] * 20 + ['평균은 4,500만원쯤이에요.'])
    ok, m, bad = aitell.script_score(calm, aitell.SCRIPT_RULES)
    assert ok and bad == []


def test_script_rules_default_without_json(monkeypatch, tmp_path):
    monkeypatch.setattr(aitell, 'SCRIPT_GATE_JSON', str(tmp_path / 'none.json'))
    assert aitell.script_rules() == aitell.SCRIPT_RULES
    j = tmp_path / 'g.json'
    j.write_text(json.dumps({'rules': [{'metric': '숫자/1000단어', 'op': 'le', 'value': 80}]}), encoding='utf-8')
    monkeypatch.setattr(aitell, 'SCRIPT_GATE_JSON', str(j))
    assert aitell.script_rules()[0]['value'] == 80


def test_our_four_scripts_fail_and_human_example_passes(monkeypatch, tmp_path):
    monkeypatch.setattr(aitell, 'SCRIPT_GATE_JSON', str(tmp_path / 'none.json'))
    for ep in ['E-1', 'D-1', 'E-2', 'N-1']:
        assert aitell.main(['--script', os.path.join(EP, ep, 'voice.json')]) == 6, ep
    assert aitell.main(['--script', os.path.join(EP, 'N-1', 'script.md')]) == 6
    assert aitell.main(['--script', os.path.join(EP, 'N-1', 'script.human-example.md')]) == 0


def test_human_example_keeps_exact_values_on_screen():
    raw = open(os.path.join(EP, 'N-1', 'script.human-example.md'), encoding='utf-8').read()
    for exact in ['4,475만원', '2,107만 8,535명', '3,417만원', '9억 9,937만원', '65조 1,605억원', '71.7%',
                  '2억 3,860만원', '11억 20만원', '4억 7,144만원', '64.56%', '+5,428만원', '452만원']:
        assert exact in raw, exact


def test_existing_modes_unchanged():
    assert aitell.main(['text', '짧은 제목입니다']) == 0
    val, hits, n = aitell.score('평범한 문장입니다. 두 번째 문장이에요.')
    assert n < 300 and val >= 0
