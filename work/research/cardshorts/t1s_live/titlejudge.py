# t1s_live 제목 심사(10/21 06시 PD, t1s_swap 복사 — 사실·후보만) · 옛: t1s_swap 제목 심사(10/20 12시 PD, c2s_deposit 복사 — 사실·후보만) · 옛: c2s_deposit 제목 심사(10/20 PD, c2s_jungwoo 복사 — 사실·후보만) · 옛: c2s_jungwoo 제목 심사(10/14 15:2x PD, p1s_cross 복사) · 옛: p1s_cross 제목 심사(10/14 PD, g1s_why/titlejudge2.py 복사) — 제미나이(10/13 23시 PD, r1s_startday/titlejudge2.py 복사). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 정부가 2026년 9월 국회에 낸 세법 개정안(아직 국회 통과 전)대로라면, 집 한 채 양도세의 장기보유특별공제가 바뀐다. 지금은 갖고 있던 해마다 4%, 살았던 해마다 4%(둘 다 10년이면 80%). 2028년엔 살았던 해 6%·갖고 있던 해 2%, 2029년부터는 갖고 있던 해를 안 치고 살았던 해만 8%씩. 가상 인물 수진 씨(10년 갖고 2년 삶)는 지금 48%, 2029년 16%. 같은 집을 판 해만 다르게 계산하면 수진 씨 세금은 해마다 3천만원 넘게 차이. 둘 다 10년을 넘지 않으면 갖고 있던 해가 살았던 해보다 한 해 많을 때마다 2029년 공제율이 지금보다 4%포인트씩 낮아진다. 살았던 햇수는 주민등록등본 전입일~전출일. 팔 시기 권유 없음.
경쟁 제목: '집 팔기 전 이것 모르고 계약하면 세금 폭탄!'(11,255) · ''팔아라' 그 집… 조건부 양도세, 지금과 정부안 내년 차이(국회 전)'(5,456) · '장기보유특별공제 한도 생긴다｜초고가 주택 양도세 폭증'(2,066) · '안 살고 갖고만 있으면 공제 0원, 장특공제 2029년부터'(1,344) · '10년 가진 집 한 채도 2년만 살았으면, 정부안 2029년 양도세 공제 48%가 16%로'(1,268) · '14년 갖고 있던 집, 실거주 3년뿐이면… 양도세 5,700만 → 1억'(1,183)
제목 규칙: 해시태그 빼고 35자 이하, 숫자 1~2개.
후보:
A. 양도세 공제, 살았던 해 짧으면 한 해마다 4%포인트 깎여요
B. 장특공제 2029년부터 살았던 해만, 내 집은 몇 %?
C. 2년만 산 집 양도세 공제, 한 해 차이마다 4%p 깎여요
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
