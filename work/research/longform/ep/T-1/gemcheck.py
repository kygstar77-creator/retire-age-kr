# -*- coding: utf-8 -*-
# T-1 대본 제미나이 검증(사실 대조 + 권유·세무 상담 위험 + 말투). 결과 review_gemini_v3.md
import sys, time, pathlib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))
import crosscheck as cc
H = pathlib.Path(__file__).resolve().parent
kv = cc.load_key('gemini_key.txt')
facts = (H / 'facts.txt').read_text(encoding='utf-8') + chr(10) + (H / 'calc_out.txt').read_text(encoding='utf-8')
script = (H / 'script.md').read_text(encoding='utf-8')
system = ('너는 한국 세금(양도소득세) 유튜브 대본 검증자다. 칭찬은 빼고 문제만. 사실표에 없는 숫자·사실, 사실표와 다른 숫자, 반올림이 틀린 말, '
          '정부안(국회 통과 전)을 확정된 법처럼 말한 문장, 계산 가정(필요경비 0·지방세 10%)을 빠뜨려 오해를 부를 말, 비과세 요건을 잘못 줄인 말, '
          '언제 팔라는 권유나 세무 상담으로 들릴 문장, 유튜브 정책 위험, 사람이 소리 내 말할 때 어색한 단어를 찾는다. '
          '각 지적: 줄 인용 → 무엇이 문제 → 고칠 문장. 마지막에 "업로드 막을 문제" 개수와 "고치면 좋은 것" 개수.')
user = f'[사실표·계산 결과]\n{facts}\n\n[대본 — "- "로 시작하는 줄만 읽는다. [자막]·(화면)은 화면 글자]\n{script}'
m, out = cc.gemini_chat(kv, system, user)
(H / 'review_gemini_v3.md').write_text(f'[{m} · {time.strftime("%Y-%m-%d %H:%M")}]\n' + out, encoding='utf-8')
print(m); print(out)
