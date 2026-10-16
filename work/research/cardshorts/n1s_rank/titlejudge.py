# n1s_rank 제목 심사(10/17 PD, n1s_top10 것 복사) · 옛: n1s_top10 제목 심사(10/16 PD, g1s_asym 것 복사) · 옛: g1s_asym · h1s_forest 제목 심사(10/15 23시 PD, h1s_walk 것 복사) · 옛: h1s_walk 제목 심사(10/15 PD, h1s_gap 것 복사) · 옛: h1s_gap 제목 심사(10/14 PD, r1s_startday 것 복사) — 제미나이(10/13 PD). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나. 쇼츠 제목은 35자 이하·숫자 1~2개가 좋다.
영상 내용(사실): 2025년 가계금융복지조사(국가데이터처·금감원·한은) 가구 순자산(집·예금·주식에서 빚을 뺀 값, 2025년 3월 말). 순자산 1억원이면 아래에서 20~30% 사이, 5억원이면 위에서 20~30% 사이. 딱 중간 가구(중앙값)는 2억 3,860만원. 평균은 4억 7,144만원으로 중앙값의 두 배 가까이이고, 평균 가구는 위에서 20~30% 사이(맨 위가 평균을 끌어올림). 위 20% 가구가 전체 순자산의 64.56%를 가짐(1년 전보다 1.48%포인트 늘어). 이 줄은 모든 나이가 섞여 있어 젊을수록 아래쪽이 자연스럽다. 영상은 전망·권유를 하지 않는다.
경쟁 제목: '대한민국 가구 순자산 순위｜상위 1%는 얼마일까?', '순자산 10억이면 상위 몇 %일까? 순자산 금액별 순위', '평균 자산 5억 나라 진짜 중간은 2.4억', '요즘 한국 중산층 특징 재산이 평균의 딱 절반임', '우리 집 자산, 평균보다 많을까?'
후보:
A. 순자산 5억, 상위 몇 %일까? 평균도 이 자리
B. 순자산 5억이면 상위 몇 %? 딱 중간은 2억대
C. 순자산 평균 4억 7천, 우리 집은 평균 위일까
JSON으로만 답: {"A": {"score": n, "why": "..."}, "B": {...}, "C": {...}, "best": "A|B|C", "fix": "가장 좋은 후보를 고친다면 한 줄"}"""
for m in ['gemini-3.1-flash-lite', 'gemini-3.1-flash-lite', 'gemini-3.8-flash-lite', 'gemini-3.1-flash']:
    try:
        d = crosscheck.http(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key=' + kv['KEY'],
                            {'contents': [{'parts': [{'text': P}]}], 'generationConfig': {'responseMimeType': 'application/json'}})
        t = d['candidates'][0]['content']['parts'][0]['text']; print(m); print(t)
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'title_gemini.json'), 'w', encoding='utf-8').write(json.dumps({'model': m, 'out': json.loads(t)}, ensure_ascii=False, indent=1))
        break
    except Exception as e:
        print(m, 'ERR', str(e)[:150])
