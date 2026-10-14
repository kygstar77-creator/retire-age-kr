# w1s_kospi 제목 심사 — 제미나이(10/13 23시 PD, r1s_startday/titlejudge2.py 복사). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 2025-10-02에 1억을 넣고 2026-10-02에 판 계산(세금·환율 다 뗀 뒤): SCHD 1억 1,599만원(+15.99%) · S&P500(SPY) 1억 1,023만원(+10.23%) · 금(GLD) 1억 337만원 · 정기예금 1억 218만원(+2.18%). 순위는 세금 전후 같음. SCHD와 예금 차이는 세금 떼기 전 1,688만원 → 뗀 뒤 1,380만원(세금이 307만원 줄임). SCHD는 분배금 373만원에서 미국 세금 15%(55만 9천원), 판 이익 세금 291만원. 넣는 날을 바꾸면 순위도 자주 바뀜. 투자 권유 없음.
같은 채널 이미 낸 쇼츠 제목(틀 반복 피함): '달러로 산 미국 ETF, 환율만으로 1억에서 330만원 줄었다' · '미국 SPY 1억, 판 이익 양도세 191만원은 언제 내나' · '1억 넣은 날만 바꾸면 1등도 바뀔까? 251번 계산해 봤다'. 롱폼 제목: '1억 예금 이자 vs 미국 ETF…세금·환율 떼고 남은 돈'.
제목 규칙: 해시태그 빼고 35자 이하, 숫자 1~2개.
후보:
A. SCHD vs 예금 1억, 세금 떼니 차이 1,688만→1,380만원
B. SCHD 1억 vs 예금 1억, 세금 떼고도 1,380만원 차이
C. 예금 vs SCHD 1억 1년, 세금이 줄인 차이 307만원
JSON으로만 답: {"A": {"score": n, "why": "..."}, "B": {...}, "C": {...}, "best": "A|B|C", "fix": "가장 좋은 후보를 고친다면 한 줄(35자 이하, 숫자 1~2개)"}"""
for m in ['gemini-3.8-flash', 'gemini-3.1-flash-lite', 'gemini-2.5-flash']:
    try:
        d = crosscheck.http(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key=' + kv['KEY'],
                            {'contents': [{'parts': [{'text': P}]}], 'generationConfig': {'responseMimeType': 'application/json'}})
        t = d['candidates'][0]['content']['parts'][0]['text']; print(m); print(t)
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'title_gemini.json'), 'w', encoding='utf-8').write(json.dumps({'model': m, 'out': json.loads(t)}, ensure_ascii=False, indent=1))
        break
    except Exception as e:
        print(m, 'ERR', str(e)[:150])
