# x1s_deposit 제목 심사 2회째(1회째 A 8·B 7·C 9 → 이해 시험에서 0원=원금 오해) (10/22 18시 PD, x1s_hedge/titlejudge.py 복사 — 사실·후보만) · 옛: x1s_hedge 제목 심사 3회째(2회째 flash-lite A 6·B 8·옛 C 7, C를 A·B 섞은 안으로) · 2회째(이해 시험 뒤 후보 바꿈) · 1회째 A 9.2·B 6.8·C 8.0 (10/21 16시 PD, t1s_live/titlejudge.py 복사 — 사실·후보만) · 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 은행 달러 예금도 원화로 따지면 마이너스가 될 수 있다. 이자는 달러로 붙고 원화로 바꾸는 날 환율이 적용되기 때문. KB국민은행 달러 1년 정기예금 연 3.64833%(조회기준일 2026.10.16), 이자소득세 15.4%를 떼면 손에 남는 건 3%쯤. 2026년 10월 15일 환율 1,338.6원에 1억을 달러로 바꿔 1년 맡기면, 1년 뒤 환율이 3%쯤만 내려도 받은 이자가 다 사라지고 1,298원 아래면 이자보다 환율 손실이 더 크다. 예금보험공사 안내: 외화예금도 1억원까지 보호, 원화로 바꿔 계산하고 한 은행 예금과 이자를 합쳐 1억원까지. 사라·팔라 권유 없음.
경쟁 제목(최근 3일): '달러 이자를 받아도, 원화로는 손해일 수 있습니다'(1,082) · '환율 2년 만에 최저, 내 지갑엔 좋은 소식일까?'(1,192) · '원·달러 환율 2년 만에 최저 — 100달러 직구, 얼마나 덜 낼까?'(1,171) · '예금 이자 3%대, 세금·물가 빼면 얼마 남을까?'(1,265) · '달러 예금 통장 손해 안 보는 법'(401)
제목 규칙: 해시태그 빼고 35자 이하, 숫자 1~2개.
후보:
A. 달러 예금 이자 3%, 환율 몇 % 내리면 마이너스일까
B. 달러 예금 이자 3%, 환율 몇 % 내리면 이자 0원 될까
C. 달러 예금 이자 3%, 환율 3%쯤 내리면 이자 0원
참고: 1회째 '이자, 환율이 몇 % 내리면 0이 될까' 9점이었으나 40·50·60세 이해 시험에서 '0원'을 원금 0원으로 읽음(2명).
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
