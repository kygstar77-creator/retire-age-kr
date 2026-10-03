"""work/sentencetypes.py 테스트: 문장 나누기·줄 번호·숫자 세기·통계·뽑기 재현."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sentencetypes as st  # noqa: E402


def test_split_keeps_decimals():
    s = st.split_sentences("코스피가 1.4% 올랐어. 그런데 제자리였지! 왜일까요? 끝")
    assert s == ["코스피가 1.4% 올랐어.", "그런데 제자리였지!", "왜일까요?", "끝"]


def test_lines_join_and_line_numbers():
    lines = [(3, "회사를 그만두고 두 달쯤 지나면,"), (4, "우편물이 하나 옵니다. 건강보험료"), (5, "고지서입니다.")]
    out = st.sentences_from_lines(lines)
    assert out == [(3, "회사를 그만두고 두 달쯤 지나면, 우편물이 하나 옵니다."),
                   (4, "건강보험료 고지서입니다.")]


def test_unpunctuated_transcript_falls_back_to_lines():
    lines = [(i, f"문장부호 없는 받아쓰기 {i}번째 줄") for i in range(1, 7)]
    out = st.sentences_from_lines(lines)
    assert len(out) == 6 and out[0][0] == 1


def test_count_numbers():
    assert st.count_numbers("제피큐는 1억 1,679만원, 슈드는 1억 2,462만원") == 4
    assert st.count_numbers("기준금리 3.0%가 됐습니다.") == 1
    assert st.count_numbers("세 배쯤 더 받았는데") == 0


def test_wilson_and_fisher():
    lo, hi = st.wilson(0, 100)
    assert lo == 0.0 and 0.03 < hi < 0.04
    # 2x2 [[2,98],[16,84]] 양측 피셔 p ≈ 0.0008
    p = st.fisher_two_sided(2, 98, 16, 84)
    assert 0.0005 < p < 0.0012
    assert st.fisher_two_sided(5, 5, 5, 5) == 1.0


def test_sample_is_reproducible_and_balanced():
    a = st.sample(seed=st.SEED)
    b = st.sample(seed=st.SEED)
    key = lambda rows: sorted((r["id"], r["src"], r["line"], r["text"]) for r in rows)
    assert key(a) == key(b)
    assert sum(r["side"] == "경쟁" for r in a) == 100
    assert sum(r["side"] == "우리" for r in a) == 100
    assert len({r["id"] for r in a}) == 200


def test_coding_sheet_covers_every_sample():
    samples = st.read_tsv(os.path.join(st.OUT, "samples.tsv"))
    codes = st.read_tsv(os.path.join(st.OUT, "codes.tsv"))
    assert {r["id"] for r in samples} == {r["id"] for r in codes}
    assert all(r["type"] and r["note"] for r in codes)
    assert len({r["type"] for r in codes}) == 13
