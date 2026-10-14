# h1s_helio 제목 심사(10/15 PD, h1s_walk 것 복사) — 제미나이. 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 부동산·재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나. 쇼츠 제목은 35자 이하·숫자 1~2개가 좋다.
영상 내용(사실): 송파구 가락동 헬리오시티 84㎡대 국토교통부 실거래 1년 85건(2025.11~2026.10). 2026년 5월 28일 26층 20.00억은 직거래로 신고(같은 달 나머지 17건 가운데 값 28.10억). 2026년 2월 같은 달 4건은 9층 23.82억(중개거래·등기 마침)·18층 30.70억·28층 31.50억·15층 30.00억 — 왜 이 값이었는지는 실거래 자료에 나오지 않는다고 말하고 이유를 짐작하지 않는다. 한 건이 아니라 달마다 가운데 값을 보면 4월 28.00억(25건)이 가장 낮고, 1년 가운데 값은 28.50억. 경쟁 쇼츠 제목 예: '강남 신축 아파트 13억 떨어진 이유', '실거래 9.9억인데 매물은 11억', '헬리오시티 그동안 얼마에 샀을까?'.
경쟁 제목: '같은 아파트 고층 프리미엄, 7천만원', '15억으로 요즘 실제로 산 서울 아파트', '7호선 상도역 초역세권 59타입 6억대 내집마련', '연봉 7천, 종잣돈 2억 살 수 있는 서울 저평가 4곳', '“학교 생기면 끝이죠” 집에서 등하교 다 보인다'
후보:
A. 헬리오시티 20억·23억 거래, 그게 단지 값일까?
B. 헬리오시티 같은 달 23억과 31억, 어느 쪽이 값일까?
C. 헬리오시티 84㎡ 20억 직거래, 같은 달 가운데 값은?
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
