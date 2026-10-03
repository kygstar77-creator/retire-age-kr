# work/audit_screen.py 화면 넘침·대비 관문 테스트 — python3 -m pytest work/tests/test_audit_screen.py
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import audit_screen as S

WHITE = {'r': 255, 'g': 255, 'b': 255, 'a': 1}
INK = {'r': 24, 'g': 25, 'b': 29, 'a': 1}
GREY = {'r': 138, 'g': 144, 'b': 155, 'a': 1}     # --ds-ink-3
ORANGE = {'r': 255, 'g': 90, 'b': 0, 'a': 1}      # --ds-accent


def text(**k):
    t = {'sel': 'p', 'text': '글자', 'x': 16, 'y': 100, 'w': 200, 'h': 20, 'font': 15, 'weight': 400,
         'color': INK, 'bg': WHITE, 'bgImage': False, 'inScroller': False, 'clipped': False}
    t.update(k); return t


def page(texts=(), targets=(), sw=375):
    return {'vw': 375, 'width': 375, 'docScrollWidth': sw, 'texts': list(texts), 'targets': list(targets)}


def test_contrast_values_match_wcag():
    assert round(S.contrast(INK, WHITE), 1) == 17.6
    assert round(S.contrast(GREY, WHITE), 2) == 3.21
    assert round(S.contrast(WHITE, ORANGE), 2) == 3.13
    assert round(S.contrast({'r': 0, 'g': 0, 'b': 0, 'a': 1}, WHITE), 0) == 21


def test_clean_page_passes():
    f, w, u = S.evaluate(page([text()], [{'sel': 'button', 'text': '계산', 'x': 16, 'y': 0, 'w': 343, 'h': 48}]))
    assert f == [] and w == [] and u == []


def test_horizontal_overflow_rejected():
    f, _, _ = S.evaluate(page([text(x=300, w=120)], sw=420))
    kinds = [k for k, _ in f]
    assert kinds.count('넘침') == 2


def test_overflow_inside_scroller_allowed():
    f, _, _ = S.evaluate(page([text(x=300, w=200, inScroller=True)]))
    assert f == []


def test_clipped_text_rejected():
    assert ('잘림' in [k for k, _ in S.evaluate(page([text(clipped=True)]))[0]])


def test_grey_caption_and_orange_button_rejected_large_text_relaxed():
    f, _, _ = S.evaluate(page([text(color=GREY, font=13), text(color=WHITE, bg=ORANGE, font=17, weight=700)]))
    assert len([k for k, _ in f if k == '대비']) == 2
    f2, _, _ = S.evaluate(page([text(color=WHITE, bg=ORANGE, font=24, weight=700)]))
    assert f2 == []  # 큰 글자는 3:1 기준 → 3.13 통과


def test_small_font_and_small_target_warn():
    _, w, _ = S.evaluate(page([text(font=11)], [{'sel': 'a', 'text': '›', 'x': 0, 'y': 0, 'w': 18, 'h': 18}]))
    assert {k for k, _ in w} == {'글자 크기', '누르는 칸'}
    _, w2, _ = S.evaluate(page([], [{'sel': 'a', 'text': '면책', 'x': 0, 'y': 0, 'w': 18, 'h': 18, 'inline': True}]))
    assert w2 == []


def test_background_image_is_unknown():
    _, _, u = S.evaluate(page([text(bgImage=True, bg=None)]))
    assert u and u[0][0] == '대비'


def test_alpha_text_blended():
    half = {'r': 255, 'g': 255, 'b': 255, 'a': 0.7}
    assert 4.5 < S.contrast(half, INK) < S.contrast(WHITE, INK)


def test_main_reads_files(tmp_path, capsys):
    good = tmp_path / 'g.json'; good.write_text(json.dumps(page([text()])), encoding='utf-8')
    bad = tmp_path / 'b.json'; bad.write_text(json.dumps(page([text(color=GREY)])), encoding='utf-8')
    assert S.main([str(good)]) == 0
    assert S.main([str(good), str(bad)]) == 1
