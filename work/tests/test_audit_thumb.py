# work/audit_thumb.py 그림 글자 크기·가림 관문 테스트 — python3 -m pytest work/tests/test_audit_thumb.py
import os, sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
PIL = pytest.importorskip('PIL')
from PIL import Image, ImageDraw, ImageFont
import audit_thumb as A

FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fonts', 'pd700.ttf')


def font(n):
    return ImageFont.truetype(FONT, n)


def thumb(tmp_path, name, draws, size=(1280, 720), bg='#111216'):
    im = Image.new('RGB', size, bg); d = ImageDraw.Draw(im)
    for fn in draws:
        fn(d)
    p = tmp_path / name; im.save(p)
    return str(p)


def test_kind_by_ratio():
    assert A.guess_kind(1280, 720) == 'thumb' and A.guess_kind(1080, 1920) == 'card' and A.guess_kind(900, 402) == 'cafe'


def test_big_text_passes(tmp_path):
    p = thumb(tmp_path, 'big.png', [lambda d: d.text((60, 120), '영업이익률 1.4%', font=font(150), fill='white')])
    m = A.measure(p)
    assert m['lines'] and A.judge(m) == []
    assert max(L['h_orig'] for L in m['lines']) > 80


def test_small_footer_rejected(tmp_path):
    p = thumb(tmp_path, 'foot.png', [lambda d: d.text((60, 100), '평균 연봉인데', font=font(140), fill='white'),
                                     lambda d: d.text((60, 600), '국세청 근로소득 백분위 · 2024년 귀속', font=font(24), fill='#9aa0aa')])
    f = A.judge(A.measure(p))
    assert any('작은 글자' in x for x in f)
    assert not any('y=1' in x for x in f if '작은 글자' in x)  # 큰 줄은 안 걸림


def test_duration_corner_rejected(tmp_path):
    p = thumb(tmp_path, 'corner.png', [lambda d: d.text((60, 100), '큰 글자', font=font(140), fill='white'),
                                       lambda d: d.text((1010, 610), '파이어맵', font=font(48), fill='#8b8f98')])
    assert any('영상 길이 표시' in x for x in A.judge(A.measure(p)))


def test_solid_bars_are_not_text(tmp_path):
    def bars(d):
        for i in range(10):
            d.rectangle((700 + i * 52, 520 - 30 * i, 740 + i * 52, 520), fill='#4a5160')
        for i in range(60):
            d.rectangle((60 + i * 19, 430, 72 + i * 19, 520), fill='#3a3f4b')
    p = thumb(tmp_path, 'bars.png', [lambda d: d.text((60, 60), '테슬라', font=font(120), fill='white'), bars])
    assert A.judge(A.measure(p)) == []


def test_two_tone_background(tmp_path):
    """위는 밝고 아래는 어두운 그림(A-1 실제 썸네일 꼴)에서도 아래쪽 작은 글자를 찾는다."""
    def split(d):
        d.rectangle((0, 0, 1280, 280), fill='#f3efe8')
        d.text((60, 120), 'JEPQ 분배금', font=font(110), fill='#111111')
        d.text((60, 360), '783만원 덜 남았다', font=font(130), fill='white')
        d.text((60, 600), '1억씩·1년 · 미국 배당세 15%만', font=font(24), fill='#9aa0aa')
    m = A.measure(thumb(tmp_path, 'two.png', [split]))
    small = [L for L in m['lines'] if L['h_view'] < A.MIN_VIEW_PX]
    assert small and all(L['y0'] > 560 for L in small)


def test_card_view_width(tmp_path):
    p = thumb(tmp_path, 'card.png', [lambda d: d.text((64, 300), '퇴직금 얼마 나올까?', font=font(100), fill='white'),
                                     lambda d: d.text((64, 1250), '근로자퇴직급여 보장법 제8조', font=font(26), fill='#8a8f9c')], size=(1080, 1920))
    m = A.measure(p)
    assert m['kind'] == 'card' and any('375px' in x for x in A.judge(m))


def test_main_exit_codes(tmp_path, capsys):
    ok = thumb(tmp_path, 'ok.png', [lambda d: d.text((60, 120), '큰 글자 하나', font=font(150), fill='white')])
    bad = thumb(tmp_path, 'bad.png', [lambda d: d.text((60, 120), '큰 글자 하나', font=font(150), fill='white'),
                                      lambda d: d.text((60, 640), '아주 작은 출처 글자 줄', font=font(20), fill='#aaaaaa')])
    assert A.main([ok]) == 0
    assert A.main([bad]) == 1
    assert A.main(['--kind', 'cafe', ok]) in (0, 1)
