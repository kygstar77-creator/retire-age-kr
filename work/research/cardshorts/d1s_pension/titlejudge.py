# d1s_pension 제목 심사(10/14 23시 PD, d1s_when 것 복사) — 제미나이. 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크·노후 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나. 쇼츠 제목은 35자 이하·숫자 1~2개가 좋다.
영상 내용(사실): 지역가입자 건보료(재산 0 가정, 2026년 법령·공단 계산식). 연금 없이 1년 배당·이자 1,000만원이면 월 2만 2,800원, 1,001만원이면 월 6만 7,850원(금융소득 1,000만원 넘으면 전액 합산). 국민연금 월 150만원(1년 1,800만원)은 보험료에 50%만 반영돼 900만원, 건보료 월 6만 1,000원. 여기에 배당·이자 1,000만원이면 그대로 6만 1,000원, 1,001만원이면 12만 8,860원. 한 달 6만 7,860원, 1년 81만 4,320원 차이 — 연금 없을 때(1년 54만원 넘게)보다 절벽이 크다.
경쟁 제목: '퇴사 후 건보료 폭탄? 3년 손해 안 보는 숨은 비법!', '국민연금 많이 받는 부모님, 이 금액 넘으면 피부양자 끝', '퇴직 후 건보료 폭탄 맞는 3가지 조건', '“연 2,000만원 넘으면 건보료가 새로 생긴다?” 60대 은퇴자 국민연금 건강보험료', '배당·이자로 오른 건보료, 몇 월 고지서부터 붙을까'(우리 채널 이전 쇼츠)
후보:
A. 국민연금 받는 사람, 배당 1만원 더 받으면 건보료는?
B. 국민연금 월 150만원이면 건보료 절벽이 더 커지는 이유
C. 연금 받는데 배당 1만원 더, 건보료 1년 81만원 차이
JSON으로만 답: {"A": {"score": n, "why": "..."}, "B": {...}, "C": {...}, "best": "A|B|C", "fix": "가장 좋은 후보를 고친다면 한 줄"}"""
for m in ['gemini-3.1-flash-lite', 'gemini-flash-lite-latest', 'gemini-3.1-flash-lite']:
    try:
        d = crosscheck.http(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key=' + kv['KEY'],
                            {'contents': [{'parts': [{'text': P}]}], 'generationConfig': {'responseMimeType': 'application/json'}})
        t = d['candidates'][0]['content']['parts'][0]['text']; print(m); print(t)
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'title_gemini.json'), 'w', encoding='utf-8').write(json.dumps({'model': m, 'out': json.loads(t)}, ensure_ascii=False, indent=1))
        break
    except Exception as e:
        print(m, 'ERR', str(e)[:150])
