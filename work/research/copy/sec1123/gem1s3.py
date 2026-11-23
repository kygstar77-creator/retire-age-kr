# 1초 시험 제미나이 심사(순서 바꿔 2번) — copywriter 11/14 (JT-1 sec1112/gem1s.py 복사, 질문 ⑥만 편별). 키는 파일에서만 읽고 출력하지 않는다.
# 쓰는 법: py -3.12 gem1s.py <폴더> <접두어> <판...>  예) K-1-thumb/sec1114 k1y y1 y2
import sys, os, json, base64, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
Q6 = {'cc1': "⑥ 큰 숫자 두 줄이 각각 무엇의 값인지(어떤 상품, 처음 넣은 돈, 언제부터 언제), '커버드콜'과 '일반형'이 무엇인지 아는지, '커버드콜 상품은 늘(언제나) 손해'라는 뜻으로 읽히나(예/약간/아니오), '이걸 사라/팔아라'고 권하는 것처럼 보이나(예/약간/아니오, 이유)", 'h6': "⑥ 큰 숫자 두 개 사이 차이가 몇 억으로 읽히나(숫자로), 몇 평 집 이야기로 읽히나(모르면 모름), 재건축 인가 때문에 값이 내렸다는 뜻으로 읽히나(예/아니오), '지금 싸졌으니 사라'고 권하는 것처럼 보이나(예/약간/아니오, 이유)", 'sq1': "⑥ '반반'이 무엇과 무엇을 반씩인지, 16억·12억이 무엇의 값인지(원·달러, 언제 넣은 돈), 알약의 -28%·-14%가 무엇이 빠진 폭인지, '이걸 사라/팔아라'고 권하는 것처럼 보이나(예/약간/아니오, 이유)"}
D, P = sys.argv[1], sys.argv[2]
Q = """(지금은 2026년 11월 23일입니다.) 유튜브 썸네일 1초 시험입니다. 이미지 두 장은 같은 썸네일을 크기만 달리한 것입니다(앞에 온 것을 먼저 1초 봤다고 생각하세요). 크기마다 따로, 한국어로 짧게:
① 무슨 내용인지 한 문장 ② 왜 눌러야 하는지(궁금증) 한 문장 ③ 안 읽히는 글자 ④ 헷갈리는 점 ⑤ 맨 위 흰 작은 줄을 그대로 읽어 적기 """ + Q6[P]
for v in sys.argv[3:]:
    out = []
    for order in ((f'{P}_{v}_168.png', f'{P}_{v}_412.png'), (f'{P}_{v}_412.png', f'{P}_{v}_168.png')):
        parts = [{'text': Q + f'\n이미지 순서: {order[0]} 먼저, {order[1]} 다음.'}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(os.path.join(D, p), 'rb').read()).decode()}} for p in order]
        for m in ('gemini-3-flash-preview', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite'):
            try:
                r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
                out.append(f'## 순서 {order[0]} → {order[1]} · 모델 {m}\n' + r['candidates'][0]['content']['parts'][0]['text']); break
            except Exception as e:
                print('재시도', m, str(e)[:80]); time.sleep(5)
    open(os.path.join(D, f'gemini_1s_{P}_{v}.md'), 'w', encoding='utf-8').write('\n\n'.join(out)); print(f'#### {v}\n' + '\n\n'.join(out))
