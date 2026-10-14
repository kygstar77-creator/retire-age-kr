# p1s_cross 제목 심사(10/14 PD, g1s_why/titlejudge2.py 복사) — 제미나이(10/13 23시 PD, r1s_startday/titlejudge2.py 복사). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 국민연금 1969년생(제때 65세), 제때 받으면 월 100만원이라고 가정. 5년 당기면(60세) 월 70만원(한 해 6%씩 깎임), 5년 미루면(70세) 월 136만원(한 해 7.2%씩 붙음). 받은 돈을 쌓아 보면 5년 당긴 쪽은 76.67세에 제때 받은 쪽에 따라잡히고, 5년 미룬 쪽은 83.89세에 제때를 넘어선다. 1년만 당기면 따라잡히는 나이가 80.67세로 오히려 늦어지고, 1년만 미루면 79.89세로 빨라진다. 국민연금법 조문 비율로 계산, 물가·세금·건보료 넣지 않음. 어느 쪽을 고르라는 말 없음.
같은 채널 이미 낸 쇼츠: 국민연금 주제 없음. 경쟁 제목: '조기수령 하면 평생 30% 감액? 출생연도별 국민연금 수령 나이 총정리'(36.7만) · '국민연금 5년 늦추면 호구?! 84세의 충격적 진실!'(3.6만) · '국민연금 5년 일찍 받을까, 5년 늦출까? 금액으로 보기' · '조기연금 함부로 신청하면 땅을 치고 후회하는 이유'
제목 규칙: 해시태그 빼고 35자 이하, 숫자 1~2개.
후보:
A. 국민연금 5년 당겨 받으면, 몇 살에 따라잡힐까
B. 국민연금 5년 당기면 76.67세에 따라잡힌다
C. 국민연금 1년만 당기면 오히려 늦게 따라잡히는 이유
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
