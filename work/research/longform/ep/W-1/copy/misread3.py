# (카드 문구판) W-1 썸네일 2차 오독 시험(copywriter 10/10) — '공시한 사흘'이 '공시 뒤 사흘'로 읽히나, '−???만'은 어떻게 읽히나. 시안마다 따로(블라인드) 제미나이에 묻는다.
import sys, json, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
V = {'K1': '내 100주 −???만', 'K2': '내 100주는?', 'K3': '내 100주 −140만'}
Q = """너는 유튜브 홈 화면을 넘기던 평범한 한국 시청자다. 아래 영상 하나가 지나갔다. 영상은 아직 안 봤다. 배경 설명 없이 이것만 보고 답한다.

- 썸네일 글자(위에서 아래로): 삼성전자 3분기 영업이익 / 107조 (잠정) / 공시까지 사흘, / {L}   (오른쪽 작은 선 그래프: 10/2·10/6·10/7·10/8 종가, 10/8에 '공시' 표시)
- 제목: 삼성전자 주가 사흘 −5.07%, 100주 평가액 −140만원 = 분기 배당 44번치

질문(각 한 줄, 짐작이면 짐작이라고):
1. 주가가 내린 사흘은 공시 '전'인가, 공시 '뒤'인가, 공시를 '포함'하는가? 하나 고르고 이유 한 줄.
2. 그래서 이 영상은 '공시 때문에 주가가 내렸다'는 말로 읽히나? 예/아니오.
3. 썸네일 마지막 줄을 보고 든 생각 한 줄. 낚시 같나? 예/아니오.
4. 썸네일 글자 중 어색하거나 무슨 말인지 모르겠는 말이 있으면 적기(없으면 없음)."""
out = []
for k, l in V.items():
    for m in ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite']:
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(
                f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps({'contents': [{'parts': [{'text': Q.format(L=l)}]}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=200))
            t = ''.join(p.get('text', '') for p in r['candidates'][0]['content']['parts'])
            out.append(f'## {k} "{l}" [{m} · {time.strftime("%Y-%m-%d %H:%M")}]\n{t}\n'); break
        except Exception as e: print(k, m, str(e)[:80]); time.sleep(3)
open(__file__.replace('.py', '_card_gemini.md'), 'w', encoding='utf-8').write('\n'.join(out)); print('\n'.join(out))
