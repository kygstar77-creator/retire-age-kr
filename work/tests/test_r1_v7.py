# R-1 v7(10/6): 하루 녹음 한도(lfvoice make 100줄) 안에 들어가고, 대본 숫자 관문(aitell script)을 지키는지
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'R-1')
sys.path.insert(0, WORK)
import lfvoice, aitell


def spoken():
    return [l for s in lfvoice.sections(EP) for l in s['lines']]


def test_line_limit():
    assert len(spoken()) <= 100


def test_number_gate():
    ok, per, multi, n, bad = aitell.script_check(' '.join(spoken()))
    assert ok, bad


def test_no_calculator_in_body():
    assert not [t for t in spoken() if '계산기' in t]


def test_only_v6_sentences():
    # 새 문장을 짓지 않는다: v7 말하는 줄은 v6 문장 그대로이거나, 앞머리('두 번째는/세 번째는')만 바꾼 두 줄
    v6 = set()
    for line in open(os.path.join(EP, 'script.v6.md'), encoding='utf-8').read().split('\n---', 1)[0].splitlines():
        if line.lstrip().startswith('- '): v6.add(re.sub(r'\s*\(화면.*$', '', line.strip()[2:]).strip())
    trimmed = {t.replace('먼저 건강보험료예요.', '두 번째는 건강보험료예요.').replace('다음은 2천만원이에요.', '세 번째는 2천만원이에요.') for t in spoken()}
    assert trimmed <= v6, trimmed - v6


def test_leftover_has_cut_chapters():
    lo = open(os.path.join(EP, 'leftover.md'), encoding='utf-8').read()
    for ch in ['## 7.', '## 8.', '## 9.', '## 10.']:
        assert ch in lo
