# 1초 시험 제미나이 심사(순서 바꿔 2번) — visual 10/29 S-1 (N-3-thumb/sec1028/gem1s.py 복사). 키는 파일에서만 읽고 출력하지 않는다.
import sys, os, json, base64, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
Q = """유튜브 썸네일 1초 시험입니다. 이미지 두 장은 같은 썸네일을 크기만 달리한 것입니다(앞에 온 것을 먼저 1초 봤다고 생각하세요). 크기마다 따로, 한국어로 짧게:
① 무슨 내용인지 한 문장 ② 왜 눌러야 하는지(궁금증) 한 문장 ③ 안 읽히는 글자 ④ 헷갈리는 점(숫자가 무엇의 숫자인지 등) ⑤ AI가 만든 디자인 티 예/아니오와 이유"""
out = []
for order in (('d_168.png', 'd_412.png'), ('d_412.png', 'd_168.png')):
    parts = [{'text': Q + f'\n이미지 순서: {order[0]} 먼저, {order[1]} 다음.'}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(os.path.join(H, p), 'rb').read()).decode()}} for p in order]
    for m in ('gemini-3-flash-preview', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite'):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
            out.append(f'## 순서 {order[0]} → {order[1]} · 모델 {m}\n' + r['candidates'][0]['content']['parts'][0]['text']); break
        except Exception as e:
            print('재시도', m, str(e)[:80]); time.sleep(5)
open(os.path.join(H, 'gemini_1s_d.md'), 'w', encoding='utf-8').write('\n\n'.join(out)); print('\n\n'.join(out))
