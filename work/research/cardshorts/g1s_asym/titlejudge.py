# g1s_asym 제목 심사(10/16 PD, h1s_forest 것 복사) · 옛: h1s_forest 제목 심사(10/15 23시 PD, h1s_walk 것 복사) · 옛: h1s_walk 제목 심사(10/15 PD, h1s_gap 것 복사) · 옛: h1s_gap 제목 심사(10/14 PD, r1s_startday 것 복사) — 제미나이(10/13 PD). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나. 쇼츠 제목은 35자 이하·숫자 1~2개가 좋다.
영상 내용(사실): 올해 1월 고점(2026-01-29)에 1천만원어치 산 금은 2026-10-06 한국거래소 KRX 금시장 종가로 663만원(−33.66%). 1g 269,810원 → 179,000원. 산 값으로 돌아가려면 179,000원에서 +50.7%(약 51%) 올라야 한다 — 떨어진 비율(34%)만큼 올라서는 모자란다. 고점에 산 금은 달러 금값 −21.62%, KRX 웃돈 −10.99%가 컸다. 수수료 별도. 영상은 앞으로를 전망하지 않는다.
경쟁 제목: '고점 찍은 금값 26% 빠진 이유', '금값 40% 폭락? 112만 원짜리 금이 70만 원 된 진짜 이유', '금값이 30% 가까이 빠진 진짜 이유', '손실 났을 때 복구가 힘든 이유', '본전 오면 감사합니다 하고 나와야 하는 이유'
후보:
A. 금값 34% 빠지면, 본전까지 몇 % 올라야 할까?
B. 1월 고점에 산 금, 본전까지 몇 % 올라야 하나
C. 금값 34% 떨어졌는데 34% 오르면 본전일까?
JSON으로만 답: {"A": {"score": n, "why": "..."}, "B": {...}, "C": {...}, "best": "A|B|C", "fix": "가장 좋은 후보를 고친다면 한 줄"}"""
for m in ['gemini-3.1-flash-lite', 'gemini-3.1-flash-lite', 'gemini-3.8-flash-lite', 'gemini-3.1-flash']:
    try:
        d = crosscheck.http(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key=' + kv['KEY'],
                            {'contents': [{'parts': [{'text': P}]}], 'generationConfig': {'responseMimeType': 'application/json'}})
        t = d['candidates'][0]['content']['parts'][0]['text']; print(m); print(t)
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'title_gemini.json'), 'w', encoding='utf-8').write(json.dumps({'model': m, 'out': json.loads(t)}, ensure_ascii=False, indent=1))
        break
    except Exception as e:
        print(m, 'ERR', str(e)[:150])
