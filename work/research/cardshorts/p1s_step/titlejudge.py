# p1s_step 제목 심사(10/15 PD, p1s_cross 복사, g1s_why/titlejudge2.py 복사) — 제미나이(10/13 23시 PD, r1s_startday/titlejudge2.py 복사). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 국민연금을 받으면서 일하는 사람(1969년생, 연금 월 100만원 가정). 2026년 6월 17일부터 근로소득공제 등을 뺀 한 달 소득이 519만원을 넘어야 연금이 깎인다(옛 기준 319만원). 월급만 있으면 비과세 뺀 한 해 총급여 7,600만원쯤부터. 국민연금법 조문대로 계산하면 깎이는 돈이 조금씩 늘지 않고, 선을 넘는 순간 한 달 15만원부터 깎인다(계단). 공제 뒤 600만원이면 27만원쯤, 700만원이면 46만원쯤, 800만원이면 50만원(상한 = 노령연금의 절반). 깎이는 기간은 정해진 받는 나이부터 최대 5년. 그래서 선 바로 위라면 몇만원 더 버는 사이 연금이 한 번에 빠지는 구간이 생긴다.
같은 채널 이미 낸 쇼츠: '국민연금 5년 당기면 76.67세에 따라잡힌다'(10/19 공개 예정). 경쟁 제목: '국민연금 일해도 월 519만원까지 안 깎입니다 소득활동 감액 새 기준'(1,493) · '월 519만원 벌어도 국민연금 안 깎인다? 감액 기준 완화'(733) · '국민연금 받으며 일하면 무조건 감액? 2026년 달라진 기준'(911)
제목 규칙: 해시태그 빼고 35자 이하, 숫자 1~2개.
후보:
A. 국민연금 받으며 일하면, 519만원 넘는 순간 15만원
B. 일하면서 국민연금 받으면 얼마부터 깎일까
C. 국민연금 감액, 519만원 넘으면 조금씩이 아니라 한 번에
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
