# R-1 v1 대본 제미나이 검증(사실 대조 pro → 말투 flash). crosscheck.py의 gemini_chat을 그대로 쓴다(429/503이면 모델을 바꿔 재시도).
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
sys.stdout.reconfigure(encoding='utf-8')
import crosscheck as cc
D = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(D)
facts = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
body = open(os.path.join(EP, 'script.md'), encoding='utf-8').read().split('\n---')[0]
gm = cc.load_key('gemini_key.txt')
FACT = f"""아래는 유튜브 롱폼 영상 대본(AI 음성 내레이션으로 읽음)과 그 [사실표]다. 오늘은 {cc.TODAY}(한국).
1) 대본을 한 문장씩 사실표와 대조해 — 사실표에 없는 숫자·날짜·주장, 다르게 옮긴 것, 조건(과거 1년 실제 값 vs 미래, 신규 가입 평균 vs 공시 최고, 지난 1년 물가 vs 앞으로 물가, 세전 vs 세후, 확인 안 함 줄)을 빠뜨려 오해를 부를 문장.
2) 투자 권유로 들릴 문장, 과장·낚시로 볼 수 있는 문장(유튜브 정책), 원자료를 넘어선 짐작, 낙인·비하로 들릴 말.
형식: 틀림 / 오해 소지 / 권유·과장 항목만 번호로 — 원문 문장 · 문제 · 근거 · 고친 문장. 맞는 문장은 적지 마. 새 정보 추가 제안 금지.

[사실표]
{facts}

[대본]
{body}"""
STYLE = f"""아래 유튜브 롱폼 대본을 귀로 듣는 시청자 입장에서 봐 줘(화면 설명 괄호는 읽지 않음). 오늘은 {cc.TODAY}.
지적할 것만: (1) 첫 30초가 끝까지 볼 이유를 주는지 (2) 장 순서가 자연스러운지 (3) 귀로 듣기에 너무 긴 문장·숫자가 한 문장에 너무 많은 곳 (4) 같은 말 반복 (5) 사람이 말할 때 안 쓰는 표현·번역투·AI 티.
형식: 번호 · 원문 문장(그대로) · 문제 · 고친 문장(그대로 붙여 넣을 수 있게, 사실·숫자 바꾸지 말 것). 많으면 15개까지. 잘한 점은 적지 마.

[대본]
{body}"""
for name, sysmsg, user, prefer in (('check_fact_v0.txt', '너는 한국 금융·세법(한국은행·금감원·소득세법) 영상 사실검증 담당이다.', FACT, 'pro'), ('check_style_v0.txt', '너는 유튜브 대본 편집자다.', STYLE, 'flash')):
    try:
        model, out = cc.gemini_chat(gm, sysmsg, user, prefer=prefer)
        open(os.path.join(D, name), 'w', encoding='utf-8').write(f'[{model} {time.strftime("%Y-%m-%d %H:%M")}]\n' + out)
        print(name, model, len(out))
    except Exception as e:
        print(name, '실패', str(e)[:300])
