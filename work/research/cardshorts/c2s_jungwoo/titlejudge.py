# c2s_jungwoo 제목 심사(10/14 15:2x PD, p1s_cross 복사) · 옛: p1s_cross 제목 심사(10/14 PD, g1s_why/titlejudge2.py 복사) — 제미나이(10/13 23시 PD, r1s_startday/titlejudge2.py 복사). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 가상 인물 정우 씨가 1998년 1월 퇴직금 3억을 S&P500(총수익, 원화 환산)에 넣고 매달 200만원씩(1월에 1년 치) 팔아 썼다. 2000~2002년 3년 연속 하락, 2002년 말 통장 1억 6천만원, 금융위기 직전 1억 밑, 2010년 말 1,150만원 남짓, 2011년 1월 한 해 치를 처음으로 못 꺼냈다(바닥). 같은 돈·같은 규칙으로 5년 늦게(2003년) 시작한 사람은 2025년 말 2억 넘게(2.72억원) 남았다. 37번 시작 중 바닥 6번. 가른 건 상품이 아니라 시작한 해. 물가 미반영. 지수·환율은 실제, 통장은 계산.
경쟁 제목: '은퇴 앞두고 S&P500 올인하면 절대 안 되는 이유'(13만) · '2억 들고 60세에 은퇴하면 몇 살까지 버틸까?' · '은퇴 자금 매년 4%씩 쓰면 안전할까요?' · '3억 파이어 대기업 퇴사했는데… 9개월 뒤'
제목 규칙: 해시태그 빼고 35자 이하, 숫자 1~2개.
후보:
A. 퇴직금 3억, 매달 200만원 쓰면 언제 바닥났을까
B. S&P500에 3억 넣고 매달 200만원, 14년 만에 바닥
C. 같은 3억인데 5년 늦게 시작한 사람만 살아남았다
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
