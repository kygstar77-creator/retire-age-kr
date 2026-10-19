# H-2 10/19 PD 14:17 회차: '은마'를 Chirp가 자주 [음마]로 읽는 줄 — 다시 받기 뒤 첫 귀(제미나이 3.1-flash-lite)만 빨리 들어 '은마'로 들리는 판이 나올 때까지(최대 N번).
#   둘째 귀 Whisper turbo는 CPU가 바빠 한 번에 3분 — 고른 판만 마지막에 readback으로 정식 판정한다(관문은 그대로).
import sys, os, json, re, base64, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
W = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'
sys.path.insert(0, W)
import lfvoice
ep = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = int(os.environ.get('TRIES', '10'))
import difflib
MODEL = lfvoice.FIRST[0]   # 18시: readback 첫 귀와 같은 모델·같은 문구(temperature 0) — 고른 판을 관문도 같게 듣는다

def gem(fn):
    body = {'contents': [{'parts': [{'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(open(fn, 'rb').read()).decode()}},
            {'text': 'Transcribe this Korean audio verbatim. Write numbers exactly as spoken using digits.'}]}], 'generationConfig': {'temperature': 0}}
    for _ in range(3):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(
                f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={lfvoice.key()}",
                data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=120))
            return r['candidates'][0]['content']['parts'][0].get('text', '').strip()
        except Exception as e:
            print('  gem 실패', str(e)[:60]); time.sleep(10)
    return ''

for at in sys.argv[1].split(','):
    si, li = map(int, at.split(':'))
    for k in range(N):
        lfvoice.retake(ep, [at], 1)
        v = json.load(open(os.path.join(ep, 'voice.json'), encoding='utf-8'))
        l = v['sections'][si]['lines'][li]
        h = gem(os.path.join(lfvoice.PUB, l['audio'].replace('/', os.sep)))
        hg, tg = re.sub(r'[^가-힣]', '', h), re.sub(r'[^가-힣]', '', l['text'])
        sp = re.sub(r'\s*\(재사용 \d+장\)', '', l['text']); hgs = lambda x: re.sub(r'[^가-힣]', '', lfvoice._same_sound(x))
        sim = max(difflib.SequenceMatcher(None, hgs(sp), hgs(h)).ratio(), difflib.SequenceMatcher(None, hgs(l['say']), hgs(h)).ratio())
        ok = not lfvoice._spots(sp, h) and sim >= 0.85   # 첫 귀가 대본과 다르게 들은 자리 0 + 전체 일치율 0.85 이상 → 둘째 귀와 합의오독이 날 수 없다
        print('@@', at, k + 1, 'OK' if ok else '--', h[:60], flush=True)
        if ok: break
