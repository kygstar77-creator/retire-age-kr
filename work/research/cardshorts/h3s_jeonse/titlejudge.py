# h3s_jeonse 제목 심사 1회째(10/23 PD, x1s_deposit/titlejudge.py 복사 — 사실·후보만) · 옛: x1s_deposit 제목 심사 2회째(1회째 A 8·B 7·C 9 → 이해 시험에서 0원=원금 오해) (10/22 18시 PD, x1s_hedge/titlejudge.py 복사 — 사실·후보만) · 옛: x1s_hedge 제목 심사 3회째(2회째 flash-lite A 6·B 8·옛 C 7, C를 A·B 섞은 안으로) · 2회째(이해 시험 뒤 후보 바꿈) · 1회째 A 9.2·B 6.8·C 8.0 (10/21 16시 PD, t1s_live/titlejudge.py 복사 — 사실·후보만) · 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 국토교통부 실거래(계약 2025.11~2026.10)로 같은 집의 새로 맺은 전세 보증금 중앙값 ÷ 매매 중앙값(전세가율)을 비교. 송파 신천동 파크리오 국민평형 38%(새 전세 11억 정도, 매매 29억대)로 가장 높고, 압구정 한양아파트 가장 작은 집 14%(새 전세 5억 반, 매매 40억 넘음)로 가장 낮음. 같은 신천동 장미아파트 23%. 살던 사람이 다시 맺은 계약은 새 계약보다 5천만원쯤 낮아 섞으면 싸 보임. 이유는 실거래 자료에 없음, 새 단지 파크리오만 30% 넘고 1980년대까지 지은 단지는 모두 아래. '싸다·비싸다'·사라 말 없음.
경쟁 제목(최근 3일): '전세 대신 매매? 서울 아파트 전세가율 높은 동네 TOP10'(387) · '매매·전세 차이 1억 이하 서울 아파트 단지 TOP10'(687) · '전세 살면 바보다? 6억 전세가 13억'(1,183) · '광명 34평 전세, 1년 새 얼마 올랐을까?'(947) · '목동 재건축, 2만 6천 가구가 이사하면 전셋값은?'(1,099)
제목 규칙: 해시태그 빼고 35자 이하, 숫자 1~2개.
후보:
A. 파크리오 전세가율 38%, 압구정 한양은 14%
B. 아파트 전세가율, 같은 서울인데 14%부터 38%까지
C. 전세는 매매값의 몇 %? 파크리오 38%·압구정 14%
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
