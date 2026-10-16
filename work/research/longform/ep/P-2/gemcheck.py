# -*- coding: utf-8 -*-
# P-2 대본 제미나이 검증. 결과 review_gemini_v1.md
import sys, time, pathlib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))
import crosscheck as cc
H = pathlib.Path(__file__).resolve().parent
kv = cc.load_key('gemini_key.txt')
facts = (H / 'facts.txt').read_text(encoding='utf-8') + chr(10) + (H / 'calc_out.txt').read_text(encoding='utf-8')
script = (H / 'script.md').read_text(encoding='utf-8')
system = ('너는 한국 국민연금 유튜브 대본 검증자다. 칭찬은 빼고 문제만. 사실표에 없는 숫자·사실, 사실표와 다른 숫자, 반올림이 틀린 말, '
          '국민연금법 조문 해석 오류(임의가입·지급률·가산·A값/B값·추납), 가정(오늘 돈 기준·이자 물가 0·최저 기준 금액)을 빠뜨려 오해를 부를 말, 임의가입을 권하거나 이득/손해로 단정한 말, '
          '원문 없는 정책 전망, 유튜브 정책 위험(금융 오해·낚시), 사람이 소리 내 말할 때 어색한 단어를 찾는다. '
          '각 지적: 줄 인용 → 무엇이 문제 → 고칠 문장. 마지막에 "업로드 막을 문제" 개수와 "고치면 좋은 것" 개수.')
user = f'[사실표·계산 결과]\n{facts}\n\n[대본 — "- "로 시작하는 줄만 읽는다. [자막]·(화면)은 화면 글자]\n{script}'
m, out = cc.gemini_chat(kv, system, user)
(H / 'review_gemini_v1.md').write_text(f'[{m} · {time.strftime("%Y-%m-%d %H:%M")}]\n' + out, encoding='utf-8')
print(m); print(out)
