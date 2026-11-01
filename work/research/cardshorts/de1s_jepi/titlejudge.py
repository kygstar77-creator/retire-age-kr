# de1s_jepi 제목 심사 1회째 (10/29 22시대 PD, x1s_deposit/titlejudge.py 복사 — 사실·후보만) · 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): JEPI는 지금 분배율 8%. 배당을 다시 넣고 주가까지 합친 5년 총수익(2021-10~2026-10, 달러)은 매년 7.5%로, S&P500 매년 12.8%(말로는 13% 정도), SCHD 9.8%(10% 정도)보다 낮았다. 주는 돈에 비해 주가는 거의 오르지 않았다. 반대로 배당 ETF HDV는 매년 13.1%로 S&P500과 거의 같거나 조금 더. 기간을 어디서 자르느냐에 따라 순서가 바뀌니 두 기간을 같이 보라. 사라·팔라 권유 없음.
경쟁 쇼츠 제목(최근 30일): '1억 넣으면 매달 57만원 주는 ETF, JEPI'(1,543) · 'JEPI vs JEPQ, 4.4년 결과는? 배당 재투자 비교'(1,333) · '미국 월배당 ETF 분배율 TOP 10'(1,194) · '10억을 JEPQ, JEPI에 투자하면 배당금 실수령액은?'(1,223) · '"월배당 10%"의 진짜 비밀, 커버드콜형'(708)
제목 규칙: 해시태그 빼고 35자 이하, 숫자 1~2개.
후보:
A. JEPI 분배율 8%, 5년 동안 돈은 얼마나 불었을까
B. JEPI 8% 주는데, 5년 수익은 S&P500보다 낮았다
C. 많이 주는 JEPI, 배당 다시 넣으면 매년 7.5%
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
