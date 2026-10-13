# r1s_startday 제목 심사 — 제미나이(10/13 PD). 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 2025-10-02에 1억을 예금·S&P500(SPY)·SCHD·금에 넣고 세금·환율 떼고 1년 뒤 보면 SCHD>S&P500>금>예금 순서.
넣는 날을 2024-10-02~2025-10-02 거래일 251번 하루씩 옮겨 1년씩 들고 판 순서(달러 기준·세금 전)를 세면, 같은 순서는 251번 중 25번(10.0%), 금이 1등인 날 187번(74.5%).
뒤에 1년 안에 꺼낼 돈(30대 집 계약금)이면 S&P500은 꺼내는 날 따라 2,574만원 폭.
경쟁 제목: '10년 전 1억을 투자했다면 지금얼마??', '삼성전자 vs 금, 3년 전 1,000만 원 넣었다면?', '1억 들고 과거로 간다면?', '1억 은행에 넣으면 월 이자 겨우 이 정도?'
후보:
A. 1억 넣는 날을 251번 바꿔 계산하면, 1등은?
B. 예금·S&P500·금, 시작일 251개로 따져 보니
C. 1억 넣은 날만 바꾸면 1등도 바뀔까? 251번 넣어 봤다
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
