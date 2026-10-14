# h1s_walk 제목 심사(10/15 PD, h1s_gap 것 복사) · 옛: h1s_gap 제목 심사(10/14 PD, r1s_startday 것 복사) — 제미나이(10/13 PD). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 부동산·재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나. 쇼츠 제목은 35자 이하·숫자 1~2개가 좋다.
영상 내용(사실): 서울 강동구 고덕동 두 단지. 고덕그라시움(2019.09 입주·4,932세대)은 상일동역 출입구까지 걸어서 180m, 래미안힐스테이트고덕(2016.12·3,658세대, 가상 인물 '손품 씨'가 사는 곳)은 고덕역 출입구까지 640m(OSM 보행로로 잼). 84㎡대 평당 값(국토교통부 실거래 1년 2025.11~2026.10)은 그라시움 9,457만원(25건)·래미안힐스테이트고덕 7,865만원(33건)으로 그라시움이 20.2% 높다. 다만 영상은 '평당 값 차이가 역 때문이라고는 말할 수 없다(지은 해·세대 수가 다름)'고 말한다. 가장 가까운 초등학교는 그라시움 390m·래미안 600m, 이마트는 래미안 960m·그라시움 1,170m로 뒤집힌다.
경쟁 제목: '같은 아파트 고층 프리미엄, 7천만원', '15억으로 요즘 실제로 산 서울 아파트', '7호선 상도역 초역세권 59타입 6억대 내집마련', '연봉 7천, 종잣돈 2억 살 수 있는 서울 저평가 4곳', '“학교 생기면 끝이죠” 집에서 등하교 다 보인다'
후보:
A. 고덕그라시움 역 180m, 래미안힐스테이트고덕 640m 평당은?
B. 고덕동 역까지 180m vs 640m, 평당 값은 얼마나 달랐나
C. 역 180m 고덕그라시움, 이마트는 오히려 더 멀었다
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
