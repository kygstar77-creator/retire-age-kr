# RULES 5-1: 새로 쓴 장(5 원금·8 보유 종목·14 은퇴 나이)을 제미나이도 같은 사실표로 써서 Claude 초안과 견준다.
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
sys.stdout.reconfigure(encoding='utf-8')
import crosscheck as cc
D = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(D)
facts = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
U = f"""유튜브 재테크 롱폼(AI 음성 내레이션, 해요체, 옆 사람에게 말하듯) 대본 중 세 장을 써 줘. 아래 [사실표]의 [12][14][15][16]만 쓰고 없는 숫자·해석·전망·권유는 넣지 마. 가상의 전문가·경험담 금지.
장5 "원금은 깎이나"(주가만 수익 → 재투자 포함) 8문장 안팎 / 장8 "안에 뭐가 들었나"(JEPI·JEPQ·SCHD 상위 10종목) 6문장 안팎 / 장14 "은퇴 나이로 바꾸면"(파이어맵 계산기) 6문장 안팎.
한 줄에 한 문장, 앞에 '- '. 숫자는 귀로 듣기 쉽게 한 문장에 두 개까지.

[사실표]
{facts}"""
model, out = cc.gemini_chat(cc.load_key('gemini_key.txt'), '너는 한국 재테크 유튜브 대본 작가다. 한국 사람이 실제로 말하는 문장으로 쓴다.', U, prefer='pro')
open(os.path.join(D, 'gemini_draft_5_8_14.md'), 'w', encoding='utf-8').write(f'[{model} {time.strftime("%Y-%m-%d %H:%M")}]\n' + out)
print(model, len(out))
