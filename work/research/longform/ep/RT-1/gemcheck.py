# -*- coding: utf-8 -*-
# RT-1 대본 제미나이 검증(사실 대조 + 권유 위험 + 말투). 결과 review_gemini_v1.md
import sys, time, pathlib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))
import crosscheck as cc
H = pathlib.Path(__file__).resolve().parent
kv = cc.load_key('gemini_key.txt')
facts = (H / 'facts.txt').read_text(encoding='utf-8') + chr(10) + (H / 'calc_out.txt').read_text(encoding='utf-8') + chr(10) + (H / 'raw1103' / 'law_1103.txt').read_text(encoding='utf-8')
script = (H / 'script.md').read_text(encoding='utf-8')
system = ('너는 한국 퇴직소득세·IRP(퇴직연금) 유튜브 대본 검증자다. 칭찬은 빼고 문제만. 사실표·법 조문에 없는 숫자·사실, 사실표와 다른 숫자, 반올림이 틀린 말, '
          '법 조문 뜻을 잘못 옮긴 문장(70·60·50%, 연금수령한도, 60일, 분리과세 1,500만원, 인출 순서, 55세·5년 요건), 일시금·연금 중 하나나 특정 금융회사·상품을 권하는 문장(권유 위험), '
          '사람이 소리 내 말할 때 어색한 단어, 처음 보는 50~60대가 헷갈릴 문장을 찾는다. '
          '각 지적: 줄 인용 → 무엇이 문제 → 고칠 문장. 마지막에 "업로드 막을 문제" 개수와 "고치면 좋은 것" 개수.')
user = f'[사실표·계산 결과·법 조문]\n{facts}\n\n[대본 — "- "로 시작하는 줄만 읽는다. [자막]·(화면)은 화면 글자]\n{script}'
m, out = cc.gemini_chat(kv, system, user)
(H / 'review_gemini_v1.md').write_text(f'[{m} · {time.strftime("%Y-%m-%d %H:%M")}]\n' + out, encoding='utf-8')
print(m); print(out)
