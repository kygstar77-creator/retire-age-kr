# h1s_gap 제목 심사(10/14 PD, r1s_startday 것 복사) — 제미나이(10/13 PD). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 부동산·재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나. 쇼츠 제목은 35자 이하·숫자 1~2개가 좋다.
영상 내용(사실): 가상 인물이 고덕동 래미안힐스테이트고덕 84㎡대 전세(보증금 9.50억 = 같은 평형 신규 전세 65건 가운데 값)에 산다. 국토교통부 실거래 1년(2025.11~2026.10) 84㎡대 매매 가운데 값에서 보증금을 빼면 더 드는 돈: 고덕아남 +5.70억, 래미안힐스테이트고덕 +10.70억, 고덕그라시움 +14.60억, 올림픽파크포레온 +18.75억, 헬리오시티 +19.00억. 전세로만 옮기면 그라시움 +0.50억, 헬리오시티 +3.00억, 포레온 +4.50억, 고덕아남은 −4.20억(1996년 입주). 세금·중개보수·대출 넣지 않은 단순 차액, '어디로 가라는 말은 아니에요'로 끝남.
경쟁 제목: '헬리오시티, 직접 걸어보면 이런 곳입니다', '3단지 고층 25평 전세11.5억', '서울 전세 역대 최고인데, 서초는 왜 6주째 내릴까?', '20년 장기전세 살면 내집?', '송파구 거래 많은 아파트 5곳, 84㎡ 최고가 작년 vs 올해'
후보:
A. 헬리오시티 84㎡, 전세 9.5억에서 얼마 더 들까
B. 전세 9.5억으로 헬리오시티·포레온 가려면 얼마 더?
C. 헬리오시티 84㎡ 사려면 전세 9.5억에 19억 더
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
