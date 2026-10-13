# d1s_when 제목 심사(10/14 PD, h1s_gap 것 복사) — 제미나이(10/13 PD). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크·노후 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나. 쇼츠 제목은 35자 이하·숫자 1~2개가 좋다.
영상 내용(사실): 지역가입자 건보료에서 1년 이자+배당(금융소득)이 1,000만원 이하면 합산 안 하고, 넘으면 전액 합산(국민건강보험법 시행규칙 제44조① 단서). 이자·배당·사업·근로 소득은 전년도 소득이 11월분 고지서부터 다음 해 10월분까지, 연금소득은 전년도 연금이 1월~12월분에 반영(시행령 제41조③). 예: 2026년에 배당·이자 1,001만원 받으면 2027년 11월분부터 2028년 10월분까지. 끝: 퇴직 첫해 고지서가 생각과 다르면 몇 년도 소득으로 계산됐는지부터 보라.
경쟁 제목: '예금이자 2천만 원 넘으면 벌어지는 끔찍한 일', '연금 받으면 건보료 폭탄? 피부양자 탈락 기준 총정리', '퇴직하고 나서 건강보험료 고지서 보고 놀란 분 이야기', '“연 2,000만원 넘으면 건보료가 새로 생긴다?” 60대 은퇴자', '퇴직 후 건강보험료, 배당·이자 1,000만원과 1,001만원 월 보험료 비교'(우리 채널 이전 쇼츠)
후보:
A. 배당·이자 1,000만원 넘은 건보료, 고지서엔 언제 붙나
B. 건보료 고지서, 2026년 배당은 2027년 11월분부터 붙는다
C. 배당·이자로 오른 건보료, 몇 월 고지서부터 붙을까
JSON으로만 답: {"A": {"score": n, "why": "..."}, "B": {...}, "C": {...}, "best": "A|B|C", "fix": "가장 좋은 후보를 고친다면 한 줄"}"""
for m in ['gemini-3.8-flash', 'gemini-3.1-flash-lite', 'gemini-2.5-flash']:
    try:
        d = crosscheck.http(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key=' + kv['KEY'],
                            {'contents': [{'parts': [{'text': P}]}], 'generationConfig': {'responseMimeType': 'application/json'}})
        t = d['candidates'][0]['content']['parts'][0]['text']; print(m); print(t)
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'title_gemini2.json'), 'w', encoding='utf-8').write(json.dumps({'model': m, 'out': json.loads(t)}, ensure_ascii=False, indent=1))
        break
    except Exception as e:
        print(m, 'ERR', str(e)[:150])
