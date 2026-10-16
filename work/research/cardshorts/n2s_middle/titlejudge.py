# n2s_middle 제목 심사(10/16 22시 쇼츠 클립 담당, n1s_top10 것 복사) · 옛: n1s_top10 제목 심사(10/16 PD, g1s_asym 것 복사) · 옛: g1s_asym · h1s_forest 제목 심사(10/15 23시 PD, h1s_walk 것 복사) · 옛: h1s_walk 제목 심사(10/15 PD, h1s_gap 것 복사) · 옛: h1s_gap 제목 심사(10/14 PD, r1s_startday 것 복사) — 제미나이(10/13 PD). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나. 쇼츠 제목은 35자 이하·숫자 1~2개가 좋다.
영상 내용(사실): 국가데이터처 2024년 임금근로일자리 소득(2024년 12월 세전 월 보수, 일자리 기준). 직장인 전체를 100명으로 줄여 월급 순서로 한 줄 세우면 딱 한가운데 50등은 세전 290만원쯤(원문 중위 288만원), 통장으로는 260만원쯤. 뉴스에 나오는 평균 월급은 세전 375만원으로 한가운데보다 87만원 높다. 적게 받는 쪽은 0원 밑으로 못 가고 많이 받는 쪽엔 몇 배 받는 사람이 있어 평균이 위로 끌려 올라간다. 그래서 내 자리는 평균 말고 한가운데와 견주라는 내용. 전망·권유 없음. 48초 쇼츠.
경쟁 제목: '내 또래는 얼마나 벌까? 2024 평균소득 vs 중위소득', '40대 평균 월급이 451만원이라고? 연령별 평균·중위소득 한눈에 보기', '내 연봉은 상위 몇 %? 2024년 연봉별 상위 % 총정리', '월 실수령 280만 원이 적다는 말을 들었는데 임금근로자 절반은 288만 원도 못 번다고?!', '내 월급, 직장인 중 상위 몇 %일까?', '평균 연봉 4,475만원의 함정, 연봉 4천도 상위 41%'
후보:
A. 월급 순위 딱 한가운데 50등, 세전 290만원쯤
B. 평균 월급 375만원인데 한가운데 50등은 290만원?
C. 직장인 100명 줄 세우면, 50등 월급은 얼마?
JSON으로만 답: {"A": {"score": n, "why": "..."}, "B": {...}, "C": {...}, "best": "A|B|C", "fix": "가장 좋은 후보를 고친다면 한 줄"}"""
for m in ['gemini-3.1-flash-lite', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-3.1-flash-lite', 'gemini-flash-latest']:
    try:
        d = crosscheck.http(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key=' + kv['KEY'],
                            {'contents': [{'parts': [{'text': P}]}], 'generationConfig': {'responseMimeType': 'application/json'}})
        t = d['candidates'][0]['content']['parts'][0]['text']; print(m); print(t)
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'title_gemini.json'), 'w', encoding='utf-8').write(json.dumps({'model': m, 'out': json.loads(t)}, ensure_ascii=False, indent=1))
        break
    except Exception as e:
        print(m, 'ERR', str(e)[:150])
