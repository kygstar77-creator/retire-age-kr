# -*- coding: utf-8 -*-
# M-1 대본 v1 제미나이 검증(사실 대조 + 정책·권유 위험). 결과 review_v1_gemini.md
import sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))
import crosscheck as cc
H = pathlib.Path(__file__).resolve().parent
kv = cc.load_key('gemini_key.txt')
facts = (H / 'facts.txt').read_text(encoding='utf-8') + '\n' + (H / 'calc_out.txt').read_text(encoding='utf-8')
d1 = (H.parent / 'D-1' / 'facts.txt').read_text(encoding='utf-8')[:6000]
script = (H / 'script.v1.md').read_text(encoding='utf-8')
system = ('너는 한국 금융 유튜브 대본 검증자다. 칭찬은 빼고 문제만. 사실표에 없는 숫자·사실, 사실표와 다른 숫자, 반올림이 틀린 말, '
          '오해를 부를 단정(세법·건보 규정 설명 포함), 투자 권유로 들릴 문장, 유튜브 금융 정책 위험을 찾는다. 각 지적: 줄 인용 → 무엇이 틀렸나 → 고칠 문장. '
          '마지막에 "업로드 막을 문제" 개수와 "고치면 좋은 것" 개수를 적어라.')
user = f'[사실표]\n{facts}\n\n[D-1 건보 사실표 일부]\n{d1}\n\n[대본]\n{script}'
m, out = cc.gemini_chat(kv, system, user)
(H / 'review_v1_gemini.md').write_text(f'[{m} · {time.strftime("%Y-%m-%d %H:%M")}]\n' + out, encoding='utf-8')
print(m); print(out)
