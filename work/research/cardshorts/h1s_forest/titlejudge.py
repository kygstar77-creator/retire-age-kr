# h1s_forest 제목 심사(10/15 23시 PD, h1s_walk 것 복사) · 옛: h1s_walk 제목 심사(10/15 PD, h1s_gap 것 복사) · 옛: h1s_gap 제목 심사(10/14 PD, r1s_startday 것 복사) — 제미나이(10/13 PD). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 부동산·재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나. 쇼츠 제목은 35자 이하·숫자 1~2개가 좋다.
영상 내용(사실): 서울 강동구 둔촌동 올림픽파크포레온(2024.11 입주·12,032세대). 국토교통부 실거래 1년(2025.11~2026.10) 84㎡대 매매 가운데 값은 28.25억으로 헬리오시티(2018.12 입주) 28.50억과 거의 같다(평당 −0.6%). 그런데 전세 가운데 값은 14억으로 헬리오시티 12억 5천만원보다 높고, 집값 중 전세 비율도 49.6%(헬리오시티 43.9%)로 세 동네 대표 단지 중 가장 높다. 한 해 거래 113건 중 94건(83%)이 2026년 4~5월 두 달에 몰렸고, 그 앞 다섯 달은 1건. 영상은 몰린 이유를 짐작하지 않는다. 역(둔촌오륜역 출입구)까지 걸어서 430m.
경쟁 제목: '8억에서 16.5억으로 폭등한 올림픽파크포레온 전세', '올림픽파크포레온 34평 매매 28억? 지금 매매·전세 얼마일까', '강남은 전세가율이 낮은데 위험한 걸까요?', '20년 살면 내 집 될까?', '공사가 반년 멈추고 부엌뷰로 욕먹던 아파트, 지금 30억'
후보:
A. 올림픽파크포레온, 집값은 헬리오시티와 같은데 전세는 14억
B. 포레온·헬리오시티 집값 같은데 전세는 왜 포레온이 높을까
C. 올림픽파크포레온 1년 거래 83%가 봄 두 달에 몰렸다
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
