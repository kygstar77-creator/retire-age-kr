# work/lfrender.py 렌더 관문 테스트 — python3 -m pytest work/tests/test_lfrender.py
import json, os, sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import lfrender as R


# ───── 가짜 편: ep/X-1 + video/x1.json + video/src/X1.tsx ─────
def make_ep(tmp_path, props, tsx="const t = '화면 제목';\n// 주석 '안 뽑힘'\n<div>막대 이름</div>\n", voice=None):
    vid = tmp_path / 'video'; (vid / 'src' / 'parts').mkdir(parents=True)
    ep = tmp_path / 'ep' / 'X-1'; ep.mkdir(parents=True)
    (vid / 'x1.json').write_text(json.dumps(props, ensure_ascii=False), encoding='utf-8')
    (vid / 'src' / 'X1.tsx').write_text("import {A} from './parts/fm';\n" + tsx, encoding='utf-8')
    (vid / 'src' / 'parts' / 'fm.tsx').write_text("export const A = '공통 부품 글자';\n", encoding='utf-8')
    if voice is not None: (ep / 'voice.json').write_text(json.dumps(voice, ensure_ascii=False), encoding='utf-8')
    return str(ep), str(vid)


def scene(rows, kind='twin', title='받은 몫 vs 낸 세금 몫'):
    return {'kind': kind, 'title': title, 'sub': '% · 전체 중', 'source': '국세청', 'data': {'rows': rows},
            'lines': [{'text': '자막 한 줄입니다.', 'audio': 'audio/x-1/a.wav', 'frames': 100}]}


PASS = {'fps': 30, 'scenes': [scene([['상위 1%', 7.7, 30.3], ['1~10%', 24.0, 41.4], ['10~50%', 47.9, 26.9], ['아래 절반', 20.4, 1.43]])]}
CUM_BAD = {'fps': 30, 'scenes': [scene([['상위 1%', 7.7, 30.3], ['상위 10%', 31.7, 71.7], ['아래 절반', 20.4, 1.43]])]}
CUM_OK = {'fps': 30, 'scenes': [scene([['상위 1%', 7.7, 30.3], ['상위 10% (상위 1% 포함)', 31.7, 71.7], ['아래 절반', 20.4, 1.43]])]}


def line(f0, tempo=1.0, date='2026-10-03', text='한 줄'):
    d = {'text': text, 'say': text, 'audio': 'audio/x-1/h.wav', 'sec': 4.0, 'frames': 128, 'rate': 6.5, 'tempo': tempo, 'f0': f0}
    if date: d['date'] = date
    return d


def voice(lines):
    return {'model': 'gemini-3.8-flash-tts', 'voice': 'Charon', 'fps': 30, 'sections': [{'title': '[0. 여는 장면]', 'lines': lines}], 'done': len(lines), 'missing': 0}


GOOD_VOICE = voice([line(150), line(152), line(148), line(155), line(146)])


# ───── 2. 누적 구간 props 3종 ─────
def test_props_noncumulative_pass():
    ok, msgs = R.cumulative_check(PASS)
    assert ok and msgs == []


def test_props_cumulative_refused():
    ok, msgs = R.cumulative_check(CUM_BAD)
    assert not ok
    assert len(msgs) == 1 and msgs[0].startswith('거부') and '상위 1%' in msgs[0] and '상위 10%' in msgs[0]


def test_props_cumulative_with_inclusion_warns_but_passes():
    ok, msgs = R.cumulative_check(CUM_OK)
    assert ok
    assert len(msgs) == 1 and msgs[0].startswith('경고')


def test_props_cumulative_in_separate_scenes_not_flagged():
    p = {'scenes': [scene([['상위 1%', 1]]), scene([['상위 10%', 2]])]}
    assert R.cumulative_check(p) == (True, [])


def test_props_cumulative_bottom_side_and_dict_labels():
    p = {'scenes': [{'kind': 'bars', 'title': 't', 'data': {'bars': [{'label': '하위 50%', 'v': 1}, {'label': '하위 20%', 'v': 2}]}}]}
    ok, msgs = R.cumulative_check(p)
    assert not ok and '하위 20% 포함' in msgs[0]


# ───── 3. 목소리 ─────
def test_voice_good_passes():
    ok, res = R.voice_check(GOOD_VOICE)
    assert ok and res['redo'] == [] and res['median_f0'] == 150


def test_voice_pitch_outlier_refused():
    ok, res = R.voice_check(voice([line(150), line(152), line(148), line(155), line(130, text='뒤쪽 낮은 목소리')]))  # 130/150 = -13.3%
    assert not ok
    assert [r['text'] for r in res['redo']] == ['뒤쪽 낮은 목소리'] and '음높이' in res['redo'][0]['why'][0]


def test_voice_pitch_inside_12pct_ok():
    ok, _ = R.voice_check(voice([line(150), line(150), line(150), line(167)]))      # +11.3%
    assert ok


def test_voice_tempo_not_one_refused():
    ok, res = R.voice_check(voice([line(150), line(150, tempo=1.25, text='빠르게 늘인 줄'), line(150)]))
    assert not ok and res['redo'][0]['text'] == '빠르게 늘인 줄' and '빠르기 1.25배' in res['redo'][0]['why'][0]


def test_voice_two_days_refused_lists_minority_day():
    ok, res = R.voice_check(voice([line(150), line(150), line(150, date='2026-10-04', text='다음 날 줄')]))
    assert not ok and res['dates'] == {'2026-10-03': 2, '2026-10-04': 1}
    assert [r['text'] for r in res['redo']] == ['다음 날 줄']


def test_voice_missing_dates_is_noted_not_invented():
    ok, res = R.voice_check(voice([line(150, date=None), line(151, date=None)]))
    assert ok                                   # 날짜 기록이 없으면 거부하지 않고 '확인 안 함'으로 적는다
    assert res['dates'] == {} and any('확인 안 함' in n for n in res['notes'])


def test_voice_missing_f0_and_tempo_refused():
    old = voice([{'text': 'A-1 옛 형식', 'audio': 'audio/a1/x.wav', 'sec': 3, 'frames': 90}])
    ok, res = R.voice_check(old)
    assert not ok and any('f0 기록 없음' in n for n in res['notes']) and any('tempo 기록 없음' in n for n in res['notes'])


# ───── 1. 화면 글자 + 편집 통과 해시 ─────
def test_screen_text_extracts_props_and_tsx(tmp_path):
    ep, vid = make_ep(tmp_path, PASS, voice=GOOD_VOICE)
    t = open(R.write_screen_text(ep, vid), encoding='utf-8').read()
    for s in ['받은 몫 vs 낸 세금 몫', '% · 전체 중', '국세청', '자막 한 줄입니다.', '1~10%', '화면 제목', '막대 이름', '공통 부품 글자']:
        assert s in t, s
    assert '안 뽑힘' not in t and 'audio/x-1' not in t and 'twin' not in t
    assert str(tmp_path) not in t                # 절대경로가 없어야 PC·클라우드 해시가 같다


def test_screen_text_gate_missing_stale_and_ok(tmp_path):
    ep, vid = make_ep(tmp_path, PASS, voice=GOOD_VOICE)
    ok, out = R.gates(ep, vid)
    assert not ok and '편집 통과 표시(screen_text.edit.json) 없음' in out[0]
    R.stamp(ep, 'firemap-editor', '테스트')
    ok, out = R.gates(ep, vid)
    assert ok, out
    assert out[0].startswith('통과') and json.load(open(os.path.join(ep, 'screen_text.edit.json'), encoding='utf-8'))['sha_of'] == 'screen_text.txt bytes'
    # 통과 뒤 그래프 제목을 바꾸면 다시 뽑힌 화면 글자의 해시가 달라져 거부
    p = json.loads(json.dumps(PASS)); p['scenes'][0]['title'] = '바뀐 제목'
    open(os.path.join(vid, 'x1.json'), 'w', encoding='utf-8').write(json.dumps(p, ensure_ascii=False))
    ok, out = R.gates(ep, vid)
    assert not ok and '뒤 화면 글자가 바뀌었다' in out[0]


def test_screen_text_hash_ignores_code_line_shift(tmp_path):
    ep, vid = make_ep(tmp_path, PASS, voice=GOOD_VOICE)
    R.write_screen_text(ep, vid); R.stamp(ep, 'firemap-editor')
    tsx = os.path.join(vid, 'src', 'X1.tsx')
    open(tsx, 'w', encoding='utf-8').write("import {A} from './parts/fm';\n\n\nconst t = '화면 제목';\n<div>막대 이름</div>\n")
    ok, out = R.gates(ep, vid)
    assert ok, out


def test_gates_refuse_cumulative_props_even_when_stamped(tmp_path):
    ep, vid = make_ep(tmp_path, CUM_BAD, voice=GOOD_VOICE)
    R.write_screen_text(ep, vid); R.stamp(ep, 'firemap-editor')
    ok, out = R.gates(ep, vid)
    assert not ok and any(o.startswith('거부 · 장면 0') for o in out)


def test_gates_cumulative_with_inclusion_ok(tmp_path):
    ep, vid = make_ep(tmp_path, CUM_OK, voice=GOOD_VOICE)
    R.write_screen_text(ep, vid); R.stamp(ep, 'firemap-editor')
    ok, out = R.gates(ep, vid)
    assert ok and any(o.startswith('경고') for o in out)


def test_gates_refuse_bad_voice(tmp_path):
    ep, vid = make_ep(tmp_path, PASS, voice=voice([line(150), line(150, tempo=1.1)]))
    R.write_screen_text(ep, vid); R.stamp(ep, 'firemap-editor')
    ok, out = R.gates(ep, vid)
    assert not ok and any('목소리 한결같음' in o and o.startswith('거부') for o in out)


def test_render_does_not_call_remotion_when_refused(tmp_path, monkeypatch):
    ep, vid = make_ep(tmp_path, CUM_BAD, voice=GOOD_VOICE)
    called = []
    monkeypatch.setattr(R.subprocess, 'call', lambda *a, **k: called.append(a) or 0)
    assert R.render(ep, vid=vid) == 1 and called == []


def test_render_calls_remotion_when_all_pass(tmp_path, monkeypatch):
    ep, vid = make_ep(tmp_path, PASS, voice=GOOD_VOICE)
    R.write_screen_text(ep, vid); R.stamp(ep, 'firemap-editor')
    called = []
    monkeypatch.setattr(R.subprocess, 'call', lambda cmd, **k: called.append((cmd, k)) or 0)
    assert R.render(ep, vid=vid) == 0
    cmd, k = called[0]
    assert cmd[:7] == ['npx', 'remotion', 'render', 'src/index.ts', 'X1', 'out/x1.mp4', '--pixel-format=yuv420p'] and '--props=x1.json' in cmd
    assert k['cwd'] == vid


def test_comp_id_and_props_path():
    assert R.comp_id('/a/ep/E-2') == 'E2' and R.props_path('/a/ep/N-1', '/v').replace(os.sep, '/') == '/v/n1.json'


# ───── lfvoice.py check 에 붙은 목소리 관문(numpy 있는 PC에서만) ─────
@pytest.mark.skip(reason='10/5 순돌이: lfvoice.py는 PC 영상 담당의 목소리 관문(같은 날 먼저 넣음)을 유지 — 렌더 전 목소리 검사는 lfrender.py voice/check가 맡는다')
def test_lfvoice_check_uses_voice_gate(tmp_path, monkeypatch, capsys):
    np = pytest.importorskip('numpy')
    import wave
    import lfvoice
    pub = tmp_path / 'public'; (pub / 'audio' / 'x-1').mkdir(parents=True)
    sr = 24000; t = np.arange(int(sr * 2.0)) / sr
    a = (8000 * np.sin(2 * np.pi * 150 * t)).astype(np.int16)
    with wave.open(str(pub / 'audio' / 'x-1' / 'h.wav'), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(a.tobytes())
    monkeypatch.setattr(lfvoice, 'PUB', str(pub))
    text = '가' * 14                                    # 2초에 14음절 = 7음절/초(속도 기준 안)
    v = voice([dict(line(150, text=text), frames=60), dict(line(150, tempo=1.25, text=text), frames=60)])
    v['sections'][0]['frames'] = 120
    fn = tmp_path / 'voice.json'; fn.write_text(json.dumps(v, ensure_ascii=False), encoding='utf-8')
    assert lfvoice.check(str(tmp_path), str(fn)) is False
    out = capsys.readouterr().out
    assert '목소리 관문' in out and '빠르기 1.25배' in out and out.strip().endswith('막힘')
