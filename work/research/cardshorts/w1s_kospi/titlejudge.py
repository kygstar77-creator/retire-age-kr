# w1s_kospi 제목 심사 — 제미나이(10/13 23시 PD, r1s_startday/titlejudge2.py 복사). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 10월 둘째 주(10/5~10/9)는 개천절 대체공휴일·한글날로 한국 증시가 사흘만 열렸다. 코스피 종가 10/2 7,003.74 → 10/8 6,625.93(−5.39%), 코스피를 따라가는 1천만원이면 −539,440원(약 54만원).
같은 주 삼성전자는 3분기 영업이익(잠정) 107.40조원을 공시했지만 100주 평가액은 −140만원(−5.07%)로 시장과 비슷한 비율. 이유는 원문으로 확인 안 됨이라 말하지 않음. 공개 시점은 10/16 전후(그 사이 10/12·13에도 코스피 급락 뉴스가 많음).
경쟁 제목: '삼성전자 107조 벌었는데 왜 빠짐? 코스피 폭락 진짜 이유', '코스피 6000선 붕괴 한국만 털린 검은 화요일 진짜 이유', '삼성전자 역대급 실적에도 반응이 싸늘한 이유', '코스피 역대급 대폭락 6000 붕괴... 하락의 진짜 이유'
후보:
A. 코스피 1천만원, 사흘 장에 얼마 빠졌을까?
B. 10월 둘째 주 코스피 1천만원, 장 선 사흘에 얼마 줄었나
C. 107조 실적 주에 코스피 1천만원은 얼마 줄었을까
JSON으로만 답: {"A": {"score": n, "why": "..."}, "B": {...}, "C": {...}, "best": "A|B|C", "fix": "가장 좋은 후보를 고친다면 한 줄(35자 이하, 숫자 1~2개)"}"""
for m in ['gemini-3.8-flash', 'gemini-3.1-flash-lite', 'gemini-2.5-flash']:
    try:
        d = crosscheck.http(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key=' + kv['KEY'],
                            {'contents': [{'parts': [{'text': P}]}], 'generationConfig': {'responseMimeType': 'application/json'}})
        t = d['candidates'][0]['content']['parts'][0]['text']; print(m); print(t)
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'title_gemini.json'), 'w', encoding='utf-8').write(json.dumps({'model': m, 'out': json.loads(t)}, ensure_ascii=False, indent=1))
        break
    except Exception as e:
        print(m, 'ERR', str(e)[:150])
