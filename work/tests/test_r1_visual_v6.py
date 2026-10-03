# R-1 v6 화면 검사(cloud/r1-remake-1003): r1.json 장면 길이·움직임 종류·글자 출처, 렌더된 장면별 대표 프레임의 안전 구역
#   python3 -m pytest work/tests/test_r1_visual_v6.py -q
import glob, json, os, re, sys
WORK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'R-1')
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as sc  # noqa: E402

R1 = json.load(open(os.path.join(WORK, 'video', 'r1.json'), encoding='utf-8'))
FACTS = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
STILLS = sorted(glob.glob(os.path.join(EP, 'preview', 'stills', '*.png')))
MOTION = {'open': 'bars', 'road': 'receipt', 'receipt': 'receipt', 'fx': 'count', 'bars': 'bars', 'count': 'count', 'zoom': 'zoom', 'logo': 'zoom', 'end': 'zoom', 'promise': 'receipt', 'swing': 'line', 'person': 'bars', 'act': 'receipt'}

def test_props_built_from_v6_and_durations_from_chars():
    assert R1['script'] == 'script.v6.md' and R1['rate'] == 5.65
    v6 = [l for s in sc.parse(os.path.join(EP, 'script.v6.md')) for l in s['lines']]
    got = [l for s in R1['scenes'] for l in s['lines']]
    assert [l['text'] for l in got] == v6          # 모든 문장이 순서대로 한 번씩
    for l in got:
        if not l['audio']:
            assert l['frames'] == max(12, round(sc.syl(sc.speak(l['text'])) / 5.65 * R1['fps'])), l['text']
    mins = sum(s['frames'] for s in R1['scenes']) / R1['fps'] / 60
    assert 12 <= mins <= 15, mins

def test_every_scene_has_exactly_one_motion_kind():
    for s in R1['scenes']:
        assert s['kind'] in MOTION, s['kind']

def test_no_calculator_scene_x_calc_vid():
    """RULES '영상 본문에 계산기 장면 넣지 않기'(X-CALC-VID): 본문에 계산기 장면·'계산기에서 해 보세요' 말 없음"""
    assert all('계산기' not in json.dumps([s['title'], s.get('sub'), s['data'], [l['text'] for l in s['lines']]], ensure_ascii=False) for s in R1['scenes'])

def test_end_screen_slot_at_least_20s_and_last():
    assert R1['scenes'][-1]['kind'] == 'end' and R1['scenes'][-1]['frames'] >= 20 * R1['fps']

def test_no_cumulative_groups_in_bar_labels():
    for s in R1['scenes']:
        for b in s['data'].get('bars', []):
            label = str(b[0])
            assert not re.search(r'상위\s*\d+%', label), label     # '상위 N%' 누적 구간 막대 금지

def test_plain_words_on_screen():
    screen = json.dumps([[s['title'], s.get('sub'), s['data']] for s in R1['scenes']], ensure_ascii=False)
    for w in ['결정세액', '총급여', '과세표준', '양도차익']:
        assert w not in screen, w

def test_screen_money_strings_exist_in_facts():
    """화면에 찍히는 원 단위 큰 숫자(7자리 이상)는 facts.txt에 같은 글자로 있다"""
    screen = json.dumps([s['data'] for s in R1['scenes']], ensure_ascii=False)
    for m in set(re.findall(r'\d{1,3}(?:,\d{3}){2,}', screen)):
        assert m in FACTS or m == '100,000,000' or m == '2,500,000', m

def test_stills_one_per_scene():
    assert len(STILLS) == len(R1['scenes'])

def test_safe_zones_empty_in_stills():
    """오른쪽 아래 25%×20%(x>1440·y>864)와 맨 아래 5%(y>1026)는 바탕색만(글자·그림 없음)"""
    from PIL import Image
    bad = []
    for f in STILLS:
        im = Image.open(f).convert('RGB'); W, H = im.size
        bg = im.getpixel((W - 4, 4))
        px = im.load()
        zones = [(int(W * 0.75), int(H * 0.80), W, H), (0, int(H * 0.95), W, H)]
        for x0, y0, x1, y1 in zones:
            n = diff = 0
            for y in range(y0, y1, 2):
                for x in range(x0, x1, 2):
                    n += 1
                    p = px[x, y]
                    if max(abs(p[0] - bg[0]), abs(p[1] - bg[1]), abs(p[2] - bg[2])) > 14: diff += 1
            if diff / n > 0.001: bad.append((os.path.basename(f), (x0, y0), round(diff / n, 4)))
    assert not bad, bad
