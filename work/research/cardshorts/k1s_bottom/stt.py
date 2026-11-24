# k1s_bottom 새 첫 줄 받아쓰기(제미나이, de1s_kofin/stt.py 사본) — 키는 출력하지 않음
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..')); sys.path.insert(0, WORK)
import lfvoice
K = lfvoice.key()
f = os.path.join(WORK, 'video', 'public', 'audio', 'k1s', '62a48f33869e3b18.wav')
for m in sys.argv[1:] or ['gemini-3.8-flash', 'gemini-3.5-flash-lite']:
    b = open(f, 'rb').read()
    body = {'contents': [{'parts': [{'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(b).decode()}}, {'text': 'Transcribe this Korean audio verbatim, including fillers and partial syllables at the edges. Write numbers exactly as spoken using digits.'}]}], 'generationConfig': {'temperature': 0}}
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={K}', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=120))
        print(m, '|', r['candidates'][0]['content']['parts'][0].get('text', '').strip())
    except Exception as e: print(m, 'ERR', str(e)[:80])
