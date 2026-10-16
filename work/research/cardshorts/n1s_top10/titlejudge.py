# n1s_top10 제목 심사(10/16 PD, g1s_asym 것 복사) · 옛: g1s_asym · h1s_forest 제목 심사(10/15 23시 PD, h1s_walk 것 복사) · 옛: h1s_walk 제목 심사(10/15 PD, h1s_gap 것 복사) · 옛: h1s_gap 제목 심사(10/14 PD, r1s_startday 것 복사) — 제미나이(10/13 PD). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나. 쇼츠 제목은 35자 이하·숫자 1~2개가 좋다.
영상 내용(사실): 2025년 가계금융복지조사(국가데이터처·금감원·한은) 가구 순자산(2025년 3월 말). 상위 10%에 들려면 11억 20만원(1년 전 10억 4,592만원 → 1년 새 +5,428만원, +5.2%, 한 달로 나누면 452만원꼴). 순자산 10억원은 위에서 10~20% 사이(상위 10% 아님). 딱 중간 집(중앙값)은 2억 4,000만원 → 2억 3,860만원(−140만원, 거의 그대로). 위 30% 선 +824만원, 위 20% 선 +2,930만원. 영상은 전망·권유를 하지 않는다.
경쟁 제목: '대한민국 순자산 기준 상위 10% 얼마일까?', '순자산 10억이면 상위 몇 %일까? 순자산 금액별 순위', '우리 집 순자산, 또래 평균은?', '저소득층은 소득 96% 쓰고 고소득층은 47% 남긴다 순자산 상위 10%가 46.1% 차지', '내 순자산은 상위 몇 %일까?'
후보:
A. 순자산 상위 10% 문턱, 1년 새 5,428만원 올랐다
B. 순자산 10억, 상위 10% 안일까? 문턱은 11억
C. 순자산 상위 10% 선, 중간 집은 그대로인데 혼자 올랐다
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
