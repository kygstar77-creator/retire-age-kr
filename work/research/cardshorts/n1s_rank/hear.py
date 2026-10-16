# n1s_rank 받아쓰기 대조(10/17 PD) — 자른 말 조각 wav를 제미나이로 받아써서 props 줄 글과 비교(새 녹음 아님). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json, base64, difflib, re
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'); sys.path.insert(0, W)
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
p = json.load(open(os.path.join(W, 'video', 'n1s_rank.json'), encoding='utf-8'))
out = []
for s in p['scenes']:
    for l in s['lines']:
        b = base64.b64encode(open(os.path.join(W, 'video', 'public', l['audio']), 'rb').read()).decode()
        heard = None
        for m in ['gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.1-flash', 'gemini-3.1-flash-lite']:
            try:
                d = crosscheck.http(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key=' + kv['KEY'],
                    {'contents': [{'parts': [{'text': '이 한국어 음성을 들리는 그대로 받아써라. 숫자는 들리는 대로 아라비아 숫자로. 받아쓴 글만 답하라.'}, {'inline_data': {'mime_type': 'audio/wav', 'data': b}}]}]})
                heard = d['candidates'][0]['content']['parts'][0]['text'].strip(); break
            except Exception as e: print(m, 'ERR', str(e)[:80])
        k = lambda t: re.sub(r'[^가-힣0-9]', '', t or '')
        r = difflib.SequenceMatcher(None, k(l['text']), k(heard)).ratio()
        out.append({'audio': l['audio'], 'text': l['text'], 'heard': heard, 'ratio': round(r, 3)})
        print(f"{r:.2f} | {l['text']}\n     | {heard}")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hear.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
