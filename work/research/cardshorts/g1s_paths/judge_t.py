# g1s_paths 쇼츠 제목 심사(제미나이 2회, 503/429면 다른 모델) — c1cafe1011/judge_t.py 틀, 10/13 PD
#   py -3.12 judge_t.py '{"T1":"…"}'
import sys, os, json, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.5-flash', 'gemini-flash-latest', 'gemini-3.1-flash-lite']
def ask(text):
    err = ''
    for m in MODELS:
        for t in range(2):
            try:
                r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}', data=json.dumps({'contents': [{'parts': [{'text': text}]}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
                return m, r['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                err = str(e); time.sleep(4)
    return None, '(실패 ' + err + ')'
T = json.loads(sys.argv[1])
raw = json.load(open(H + '/compete_raw.json', encoding='utf-8'))
comp = '\n'.join(f"- {r['title'][:70]} (조회 {r['views']:,})" for r in raw[:20])
fact = ('[영상 내용] 유튜브 쇼츠 49초. 2025-10-02 같은 날 금 1천만원어치를 산 길별로 2026-10-06 KRX 종가 기준: KRX 금시장 9,556,861원, 금 ETF 9,472,686원, '
        '골드바 금값 몫 어림 8,688,055원(부가세 10% 909,091원 뺀 몫, 수수료 별도). KRX−골드바 868,806원(87만원 가까이). 골드뱅킹은 살 때 +1%·팔 때 −1%. '
        '추천·전망 없음, 지나간 값. 첫 문장 "작년에 골드바로 샀다면, 지금 금값 몫은 869만원이에요." 화면 위 질문 "금 1천만원, 어느 길로 샀나요?"')
P = ('유튜브 쇼츠 제목 심사. 주제: 금 사는 길(KRX 금시장·금 ETF·골드뱅킹·골드바) 비교.\n[경쟁 쇼츠 제목(최근 30일, 조회순)]\n' + comp + '\n' + fact + '\n[후보 — 실제 제목엔 끝에 #shorts가 붙음]\n' +
     '\n'.join(f'{k}. {v}' for k, v in T.items()) +
     '\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장·사실 어긋남 아님(숫자가 영상과 맞나) ④경쟁 틀 반복 아님 ⑤검색어(금·골드바·KRX) 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "T1: 점수 N — 이유", 마지막 "1위: 기호".')
out = []
for i in (1, 2):
    m, t = ask(P); out.append(f'[{m}]\n{t}'); print(m); print(t[:1500]); print('--')
open(H + '/judge_title_raw.md', 'a', encoding='utf-8').write('\n---\n'.join(out) + '\n===\n')
