# de1s_jepi 제목 심사 1회째 (10/29 22시대 PD, x1s_deposit/titlejudge.py 복사 — 사실·후보만) · 키는 crosscheck.load_key로 읽고 출력하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import crosscheck
kv = crosscheck.load_key('gemini_key.txt')
P = """당신은 한국 재테크 유튜브 쇼츠 제목 심사관입니다. 아래 쇼츠 제목 후보 3개를 각각 10점 만점으로 매기세요.
기준: ① 1초에 주제가 보이나 ② 궁금증 장치 하나 ③ 낚시·과장 아님(내용과 일치) ④ 경쟁 제목 틀 반복 아님 ⑤ 검색어가 앞에 있나.
영상 내용(사실): 국토교통부 전월세 실거래(2025.11~2026.10 계약) 반포 래미안원베일리 84㎡대 전세 가운데 값 — 새로 들어간 전세 21억(30건), 살던 사람이 다시 맺은 전세 17억 8,500만원(19건), 3억쯤 차이. 다시 맺은 19건 중 18건이 계약갱신요구권을 썼다고 신고. 잠실·대치·반포 84㎡대 권리 쓴 갱신 466건 중 보증금을 5% 넘게 올린 계약은 0건, 권리를 안 쓴 갱신 중엔 5% 넘게 올린 것도 있었다. 그래서 더 살 거면 다시 계약할 때 이 권리를 쓴다고 말하고 계약서·신고에 남기라. 사라·계약하라 권유 없음.
경쟁 쇼츠 제목: '토허제의 후폭풍, 심각한 전세 상황'(57,696) · '집주인이 들어와 산다는데 나가야 하나요 | 계약갱신청구권 거절 사유'(3,412) · '실거주 매수인이 세입자 갱신요구권 거절하는 2가지 필수 조건'(3,423) · '계약갱신요구권 행사했는데 전세금 5% 협의 안 되면 나가야 하나요?'(1,637) · '세입자가 5% 상한을 포기하는 이유'(1,064)
제목 규칙: 해시태그 빼고 35자 이하, 숫자 1~2개.
후보:
A. 같은 아파트 같은 크기, 전세 3억 차이 난 이유
B. 원베일리 전세 21억 vs 18억, 차이는 이 권리
C. 전세 다시 계약할 때 이 말 안 하면 3억 손해?
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
