# x1s_hedge 제목 심사 3회째(2회째 flash-lite A 6·B 8·옛 C 7, C를 A·B 섞은 안으로) · 2회째(이해 시험 뒤 후보 바꿈) · 1회째 A 9.2·B 6.8·C 8.0 (10/21 16시 PD, t1s_live/titlejudge.py 복사 — 사실·후보만) · 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 같은 회사가 만든 국내 상장 S&P500 ETF 두 개(환노출형 KODEX 미국S&P500, 이름 끝에 H가 붙은 환헤지형)에 같은 날 1억을 넣고 2026-10-16 종가·분배금으로 계산. 달러가 제일 비쌌던 2026년 7월 2일에 넣었다면 환노출형 8,958만원, H형 1억 381만원 — 차이 1,400만원 넘게. 그런데 2024년 1월 2일(환율 1,289원)에 넣었다면 뒤집혀서 환노출형이 1,500만원 넘게 더 남음. 환율을 막아 두면 내릴 때 손실도 막지만 오를 때 이익도 같이 막는다. 고르는 기준은 이 돈을 결국 원화로 쓸지 달러로 쓸지. 어느 쪽을 사라는 권유 없음.
경쟁 제목: '같은 S&P500 ETF 수익률 -9.08% vs +2.18%, 환헤지(H) 차이'(1,247) · '같은 S&P500인데 -10% vs +5%… 이름 끝 (H) 하나 차이'(1,218) · '미국 주식 올랐는데 내 계좌는 마이너스인 이유'(1,298) · 'S&P500 지수 +12%인데 제일 많이 산 ETF는 +4%대? 사라진 수익의 행방'(1,195) · '환헤지 ETF, 환율 막았는데 왜 수익률이 다를까?'(1,141) · '같은 미국 주식인데 15% 차이 난 이유?'(982)
제목 규칙: 해시태그 빼고 35자 이하, 숫자 1~2개.
후보:
A. S&P500 환헤지 H형, 1억 넣은 날 따라 이기고 졌다
B. S&P500 환헤지 H형, 1,400만원 이긴 날과 진 날
C. S&P500 환헤지 H형, 1억 넣은 날 따라 1,400만원 갈렸다
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
