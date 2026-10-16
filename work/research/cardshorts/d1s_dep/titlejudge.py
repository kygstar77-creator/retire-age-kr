# d1s_dep 제목 심사(10/16 07시 PD, n1s_top10 것 복사) — 제미나이. 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나. 쇼츠 제목은 35자 이하·숫자 1~2개가 좋다.
영상 내용(사실): 국민건강보험공단 피부양자 소득·재산요건 안내(2026년). 퇴직 뒤 직장 다니는 가족의 피부양자로 들어가면 본인 건보료 0원. 조건이 안 맞으면 지역가입자가 되어 소득·재산으로 보험료를 낸다. 피부양자 조건은 두 가지: 소득(사업·금융·연금·근로 소득 합계 1년 2,000만원 이하, 사업소득은 원칙적으로 없어야), 재산(재산세 과세표준 5억 4,000만원 이하면 통과, 5억 4,000만원~9억원이면 1년 소득 1,000만원 이하여야). 하나라도 넘으면 지역가입자. 영상은 권유를 하지 않는다.
경쟁 제목: '퇴직 후 건보료 폭탄 맞는 3가지 조건', '공단은 절대 먼저 안 알려줌! 11월 건보료 폭탄 부르는 피부양자 탈락 기준 8가지', '연금 받다가 건보료 폭탄? 피부양자 탈락 기준', '국민연금 월 167만원 넘으면, 아내도 피부양자에서 빠집니다', '건강보험 피부양자 탈락 기준 | 집 과세표준 따라 소득 한도 달라짐'
후보:
A. 퇴직 후 건보료 0원, 피부양자 조건은 딱 두 줄
B. 피부양자 조건, 소득 2,000만원·재산 5억 4천 넘으면 지역가입자
C. 퇴직 후 건보료 0원 남으려면? 소득 2,000만원이 첫 선
JSON으로만 답: {"A": {"score": n, "why": "..."}, "B": {...}, "C": {...}, "best": "A|B|C", "fix": "가장 좋은 후보를 고친다면 한 줄"}"""
for m in ['gemini-3.1-flash-lite', 'gemini-3.8-flash-lite', 'gemini-3.1-flash']:
    try:
        d = crosscheck.http(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key=' + kv['KEY'],
                            {'contents': [{'parts': [{'text': P}]}], 'generationConfig': {'responseMimeType': 'application/json'}})
        t = d['candidates'][0]['content']['parts'][0]['text']; print(m); print(t)
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'title_gemini.json'), 'w', encoding='utf-8').write(json.dumps({'model': m, 'out': json.loads(t)}, ensure_ascii=False, indent=1))
        break
    except Exception as e:
        print(m, 'ERR', str(e)[:150])
