# w1s_kospi 제목 심사 — 제미나이(10/13 23시 PD, r1s_startday/titlejudge2.py 복사). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 2025-10-02에 산 금을 2026-10-06 기준으로 보면, 국제 금값(금 선물, 달러)은 +6.65%인데 한국 KRX 금시장 금은 −4.43%(1천만원 → 약 956만원). 한국 금값 = 달러 금값 × 원/달러 환율 × KRX 웃돈. 환율 −3.38%(1,406.0원 → 1,358.5원), KRX 웃돈이 +6.3%에서 −1.4%로 바뀌어 −7.26% — 가장 큰 조각은 웃돈. 전망·매수 권유 없음.
같은 채널 이미 낸 쇼츠 제목(틀 반복 피함): '금 1천만원어치 언제 샀나요? 1월 고점이면 지금 663만원' · '작년 금 1천만원, 골드바·KRX 따라 87만원 갈렸다'. 경쟁 제목: '국제 금 가격은 오르는데, 왜 국내 금 가격은 떨어질까?'(답은 환율 하나뿐) · '금값 폭등? VS 작년보다 떨어졌다?' · '금값 떨어졌는데...금 매수타밍일까 매도타이밍일까?'
제목 규칙: 해시태그 빼고 35자 이하, 숫자 1~2개.
후보:
A. 국제 금값 +6.65%인데 한국 금은 왜 −4.43%?
B. 국제 금값 +6.65%, KRX 금은 −4.43% 주범은 웃돈
C. 국제 금값 +6.65%, KRX 금은 −4.43%, 가장 큰 몫은 웃돈
JSON으로만 답: {"A": {"score": n, "why": "..."}, "B": {...}, "C": {...}, "best": "A|B|C", "fix": "가장 좋은 후보를 고친다면 한 줄(35자 이하, 숫자 1~2개)"}"""
for m in ['gemini-3.8-flash', 'gemini-3.1-flash-lite', 'gemini-2.5-flash']:
    try:
        d = crosscheck.http(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key=' + kv['KEY'],
                            {'contents': [{'parts': [{'text': P}]}], 'generationConfig': {'responseMimeType': 'application/json'}})
        t = d['candidates'][0]['content']['parts'][0]['text']; print(m); print(t)
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'title_gemini2.json'), 'w', encoding='utf-8').write(json.dumps({'model': m, 'out': json.loads(t)}, ensure_ascii=False, indent=1))
        break
    except Exception as e:
        print(m, 'ERR', str(e)[:150])
