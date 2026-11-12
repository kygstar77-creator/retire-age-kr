# 11/12 visual — 경쟁 롱폼 판 중 '몸통에 사물·도식 그림'이 있는 판 비율 실측 (지시: quality-gap-1112 ②, 50% 값 registry 등록 전 표본 5편)
#   py -3.12 measure.py <videoId> ...  → out/<id>.json (10초 프레임마다 판정) · 맨 끝 요약표
#   프레임: research/strategy/format-1022/frames/<id>/t*.jpg (10/22 받은 것, 320x180, 10초 간격) · 남의 영상 파일은 받지 않음
import sys, os, json, base64, urllib.request, urllib.error, time, glob, re
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(H, '..', '..', '..'))
FR = os.path.join(WORK, 'research', 'strategy', 'format-1022', 'frames')
MODEL = os.environ.get('M', 'gemini-3-flash-preview')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
OUT = os.path.join(H, 'out'); os.makedirs(OUT, exist_ok=True)
Q = """아래는 유튜브 경제 영상에서 10초마다 뽑은 화면들입니다. 각 화면 앞에 번호가 있습니다. 화면마다 아래 세 가지를 판정해 JSON 배열로만 답하세요.
- kind: "board"(만든 그래픽 화면: 글자·숫자·표·차트·도식이 주인공인 판) / "photo"(실사 사진·영상, AI 실사 장면 포함) / "illust_scene"(사람·장소가 나오는 그림 장면, 만화) / "other"(로고·검은 화면 등)
- obj: kind가 board일 때만 true/false — 판 몸통에 사물·건물·도식 그림(아이콘보다 큰 그림: 집·아파트·은행·통장·돈·달력·서류·계산기·화살표 흐름도 등)이 있으면 true. 숫자·글자·표·막대/선 차트만 있으면 false. 사람 그림만 있으면 false이고 person=true로.
- q: kind가 board일 때만 — 화면의 주인공이 물음표('?')로 가린 숫자·질문이면 true.
형식: [{"i":번호,"kind":"...","obj":true,"person":false,"q":false}, ...] 모든 번호를 빠짐없이."""

def ask(imgs, idx):
    parts = [{'text': Q}]
    for i, p in zip(idx, imgs):
        parts += [{'text': f'[{i}]'}, {'inline_data': {'mime_type': 'image/jpeg', 'data': base64.b64encode(open(p, 'rb').read()).decode()}}]
    for k in range(6):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(
                f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}',
                data=json.dumps({'contents': [{'parts': parts}], 'generationConfig': {'responseMimeType': 'application/json'}}).encode(),
                headers={'Content-Type': 'application/json'}), timeout=240))
            return json.loads(r['candidates'][0]['content']['parts'][0]['text'])
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 503) or k == 5: raise
            time.sleep(15 * (k + 1))

rows = []
for vid in sys.argv[1:]:
    fn = os.path.join(OUT, vid + '.json')
    if not os.path.exists(fn):
        fs = sorted(glob.glob(os.path.join(FR, vid, 't*.jpg')))
        res = []
        for s in range(0, len(fs), 15):
            b = fs[s:s + 15]; idx = list(range(s, s + len(b)))
            ans = ask(b, idx)
            got = {a['i']: a for a in ans}
            for i, p in zip(idx, b): res.append(dict(t=os.path.basename(p), **{k: v for k, v in got.get(i, {}).items() if k != 'i'}))
        json.dump(dict(vid=vid, model=MODEL, frames=res), open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    d = json.load(open(fn, encoding='utf-8'))['frames']
    bd = [x for x in d if x.get('kind') == 'board']
    rows.append((vid, len(d), len(bd), sum(1 for x in bd if x.get('obj')), sum(1 for x in bd if x.get('person')), sum(1 for x in bd if x.get('q'))))
print('| 영상 | 프레임 | 판 | 사물그림 판 | 비율 | 사람그림 판 | ? 판 |')
for v, n, b, o, pe, q in rows: print(f'| {v} | {n} | {b} | {o} | {o / b:.0%} | {pe} | {q} |' if b else f'| {v} | {n} | 0 | - | - | - | - |')
