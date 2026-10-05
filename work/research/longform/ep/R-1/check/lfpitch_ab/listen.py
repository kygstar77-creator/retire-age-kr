# 원본·음높이 맞춘 것 5쌍을 제미나이에게 '소리로' 들려 같은 사람인지·어색한지 묻는다(순서는 쌍마다 섞어 블라인드).
import sys, json, base64, random, urllib.request, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]  # second_opinion.py와 같은 읽기
models = sys.argv[1:] or ['gemini-3-flash-preview']
pairs = json.load(open(os.path.join(H, 'pairs.json'), encoding='utf-8'))
random.seed(1005)
Q = ('두 녹음 A, B는 같은 한국어 문장이에요. 한쪽은 원본, 한쪽은 음높이를 기계로 옮겼을 수 있어요(아닐 수도 있음). 소리만 듣고 JSON 한 줄로 답해 주세요: '
     '{"same_person":1~10(10=확실히 같은 사람),"processed":"A"|"B"|"모름"(기계 처리 흔적이 들리는 쪽),"awkward_A":1~10,"awkward_B":1~10(10=아주 어색·로봇 같음),"why":"한 문장"}')
res = []
for m in models:
    for p in pairs:
        o = open(os.path.join(H, f"{p['n']}_원본.wav"), 'rb').read(); q = open(os.path.join(H, f"{p['n']}_맞춤.wav"), 'rb').read()
        flip = random.random() < 0.5; A, B = (q, o) if flip else (o, q)
        parts = [{'text': Q + ' 문장: ' + p['text']}, {'text': 'A:'}, {'inline_data': {'mime_type': 'audio/wav', 'data': base64.b64encode(A).decode()}},
                 {'text': 'B:'}, {'inline_data': {'mime_type': 'audio/wav', 'data': base64.b64encode(B).decode()}}]
        body = json.dumps({'contents': [{'parts': parts}], 'generationConfig': {'temperature': 0.2}}).encode()
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', body, {'Content-Type': 'application/json'}), timeout=120))
            t = r['candidates'][0]['content']['parts'][-1]['text']
        except Exception as e:
            t = f'오류 {getattr(e, "code", e)}'
        row = {'model': m, 'n': p['n'], 'ratio': p['ratio'], 'pitched_is': 'A' if flip else 'B', 'answer': t.strip()}
        res.append(row); print(json.dumps(row, ensure_ascii=False))
json.dump(res, open(os.path.join(H, 'listen_' + '_'.join(models) + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
