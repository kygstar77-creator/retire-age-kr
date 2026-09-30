# RULES 5-1: 이번에 새로 쓴 장(3 마이크론 4분기·3-1 삼성 안의 두 얼굴·8 다음 전망)을 제미나이도 같은 사실표로 써서 Claude 초안과 견준다.
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
sys.stdout.reconfigure(encoding='utf-8')
import crosscheck as cc
D = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(D)
facts = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
U = f"""유튜브 재테크 롱폼(AI 음성 내레이션, 해요체, 옆 사람에게 말하듯) 대본 중 세 장을 써 줘. 아래 [사실표]의 [10][11][12]만 쓰고 없는 숫자·해석·전망·권유는 넣지 마. 가상의 전문가·경험담 금지.
장A "마이크론 4분기 실적"(1년 전 대비·6월 회사 전망 대비·사업부) 7문장 안팎 / 장B "삼성전자 안에서 — 메모리를 파는 쪽과 사는 쪽"(DS·DX 부문, 가격 문장 원문) 8문장 안팎 / 장C "다음 분기 회사 전망" 3문장 안팎.
한 줄에 한 문장, 앞에 '- '. 숫자는 귀로 듣기 쉽게 한 문장에 두 개까지. 반기(6개월)와 연간(12개월) 비교면 기간을 꼭 말해.

[사실표]
{facts}"""
model, out = cc.gemini_chat(cc.load_key('gemini_key.txt'), '너는 한국 재테크 유튜브 대본 작가다. 한국 사람이 실제로 말하는 문장으로 쓴다.', U, prefer='pro')
open(os.path.join(D, 'gemini_draft_3_3-1_8.md'), 'w', encoding='utf-8').write(f'[{model} {time.strftime("%Y-%m-%d %H:%M")}]\n' + out)
print(model, len(out))
