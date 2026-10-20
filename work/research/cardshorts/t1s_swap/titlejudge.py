# t1s_swap 제목 심사(10/20 12시 PD, c2s_deposit 복사 — 사실·후보만) · 옛: c2s_deposit 제목 심사(10/20 PD, c2s_jungwoo 복사 — 사실·후보만) · 옛: c2s_jungwoo 제목 심사(10/14 15:2x PD, p1s_cross 복사) · 옛: p1s_cross 제목 심사(10/14 PD, g1s_why/titlejudge2.py 복사) — 제미나이(10/13 23시 PD, r1s_startday/titlejudge2.py 복사). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 집 한 채가 있는 세대가 새 집을 사서 잠깐 두 채가 되면, 새 집을 산 날부터 3년 안에 헌 집을 팔면 집 한 채처럼 비과세를 받았다. 소득세법 시행령이 바뀌어 2026년 10월 1일 양도분부터, 헌 집과 새 집이 둘 다 조정대상지역이면 기한이 2년이다(이미 시행, 정부안 아님). 이유는 정부 문답 자료: 조정지역 두 채를 3년 동안 한 채처럼 봐 주는 건 혜택이 너무 크다. 서울은 작년 10월 25개 구 전체가 조정대상지역. 2년을 넘겨 팔면 두 채 세금(12억 비과세·장기보유특별공제 빠지고 기본세율+20%p 중과) — 가상 20억 집 계산으로 7억 8천만원쯤, 집 한 채일 때의 5배 넘게. 8월 3일까지 새 집을 샀거나 계약금을 냈다면 예전대로 3년. 적어 둘 날짜: 헌 집 산 날, 새 집 산 날, 새 집 산 날부터 2년 되는 날.
경쟁 제목: '지혜의곳간 ㅣ10월 1일부터 일시적 2주택 3년→2년! 부동산 세금 이렇게 바뀝니다'(9,815) · '[속보] 조정지역 일시적 2주택 처분기한 3년→2년'(6,643) · '일시적 2주택 비과세, 3년 아니라 2년입니다'(2,010) · '조정대상지역 일시적 2주택, 기존 집 3년 아닌 2년 안에 팔아야 하나요?'(1,185) · '집 갈아타는 1주택자, 2년 안에 못 팔면 비과세 놓칩니다'(952)
제목 규칙: 해시태그 빼고 35자 이하, 숫자 1~2개.
후보:
A. 일시적 2주택 2년 넘기면, 20억 집 세금이 5배
B. 일시적 2주택 처분 기한 2년, 넘기면 세금 얼마?
C. 집 갈아타는 중이라면 헌 집 기한 2년, 넘기면 5배
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
