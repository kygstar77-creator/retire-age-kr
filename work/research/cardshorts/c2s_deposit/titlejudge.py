# c2s_deposit 제목 심사(10/20 PD, c2s_jungwoo 복사 — 사실·후보만) · 옛: c2s_jungwoo 제목 심사(10/14 15:2x PD, p1s_cross 복사) · 옛: p1s_cross 제목 심사(10/14 PD, g1s_why/titlejudge2.py 복사) — 제미나이(10/13 23시 PD, r1s_startday/titlejudge2.py 복사). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 가상 인물 정우 씨가 1998년 1월 퇴직금 3억으로 매달 200만원씩(1월에 1년 치) 꺼내 썼다. S&P500(총수익, 원화)에 넣었으면 2011년 1월에 바닥, 같은 규칙으로 은행 정기예금(한국은행 1월 실제 금리)에 넣었으면 2018년 1월에 바닥 — 예금이 일곱 해 더 갔다. 1998년 예금 금리가 15%를 넘었고(외환위기), 그 뒤 세 해도 높았으며 그동안 지수는 떨어졌다. 2003년에 시작했다면 반대: 예금은 2019년에 바닥, S&P500 쪽은 2025년 말 2억 7천만원이 남았다. 결론은 상품이 아니라 시작한 해. 물가 미반영, 지나간 기록, 투자 권유 아님.
경쟁 제목: '10년 전 은행에 1억 묶어둔 분들 큰일 났습니다'(49만) · '은퇴 후 통장 잔액 3억 언제 바닥날지 아시나요?'(6만) · '은행만 믿다간 결국 0원 노후 자금 이렇게 굴려요!'(6만) · '은행 예금 vs 삼성 주식, 전문가 답은?'(3만)
제목 규칙: 해시태그 빼고 35자 이하, 숫자 1~2개.
후보:
A. 퇴직금 3억, 예금이 S&P500보다 7년 더 버틴 해
B. 퇴직금 3억 예금 vs S&P500, 먼저 바닥난 쪽은?
C. 예금이 주식을 이긴 해, 퇴직금 3억이 7년 더 갔다
JSON으로만 답: {"A": {"score": n, "why": "..."}, "B": {...}, "C": {...}, "best": "A|B|C", "fix": "가장 좋은 후보를 고친다면 한 줄(35자 이하, 숫자 1~2개)"}"""
for m in ['gemini-3.8-flash', 'gemini-3.1-flash-lite', 'gemini-flash-latest', 'gemini-flash-lite-latest', 'gemini-3.5-flash']:
    try:
        d = crosscheck.http(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key=' + kv['KEY'],
                            {'contents': [{'parts': [{'text': P}]}], 'generationConfig': {'responseMimeType': 'application/json'}})
        t = d['candidates'][0]['content']['parts'][0]['text']; print(m); print(t)
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'title_gemini.json'), 'w', encoding='utf-8').write(json.dumps({'model': m, 'out': json.loads(t)}, ensure_ascii=False, indent=1))
        break
    except Exception as e:
        print(m, 'ERR', str(e)[:150])
