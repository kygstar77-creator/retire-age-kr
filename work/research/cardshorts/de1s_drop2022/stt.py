# 나눈 wav 3토막 받아쓰기(제미나이, lfvoice와 같은 요청 꼴) — 키는 출력하지 않음
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, WORK)
import lfvoice
K = lfvoice.key()
D = os.path.join(WORK, 'video', 'public', 'audio', 'de1s_drop2022')
for m in ('gemini-3-flash-preview', 'gemini-flash-latest'):
    for x in 'c':
        b = open(os.path.join(D, f'drop_{x}.wav'), 'rb').read()
        body = {'contents': [{'parts': [{'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(b).decode()}}, {'text': 'Transcribe this Korean audio verbatim, including fillers and partial syllables at the edges. Write numbers exactly as spoken using digits.'}]}], 'generationConfig': {'temperature': 0}}
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={K}', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=120))
            print(m, x, '|', r['candidates'][0]['content']['parts'][0].get('text', '').strip())
        except Exception as e: print(m, x, 'ERR', str(e)[:80])
