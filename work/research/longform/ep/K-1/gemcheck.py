# -*- coding: utf-8 -*-
# K-1 대본 제미나이 검증(사실 대조 + 전망·권유 위험 + 말투). 결과 review_gemini_v2.md
import sys, time, pathlib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))
import crosscheck as cc
H = pathlib.Path(__file__).resolve().parent
kv = cc.load_key('gemini_key.txt')
facts = (H / 'facts.txt').read_text(encoding='utf-8') + chr(10) + (H / 'calc_out.txt').read_text(encoding='utf-8') + chr(10) + (H / 'calc2_out.txt').read_text(encoding='utf-8') + chr(10) + (H / 'calc3_out.txt').read_text(encoding='utf-8')
script = (H / 'script.md').read_text(encoding='utf-8')
system = ('너는 한국 금리(예금·주택담보대출·국채) 유튜브 대본 검증자다. 칭찬은 빼고 문제만. 사실표에 없는 숫자·사실, 사실표와 다른 숫자, 반올림이 틀린 말, '
          '상관관계를 인과처럼 말한 문장, 한국은행 신규취급액 평균을 이미 빌린 사람 금리처럼 말한 문장, COFIX 설명이 틀린 말, 금리 전망으로 들리는 문장, '
          '고정·변동 중 하나나 특정 은행·상품을 권하는 문장(투자·대출 권유 위험), 사람이 소리 내 말할 때 어색한 단어를 찾는다. '
          '각 지적: 줄 인용 → 무엇이 문제 → 고칠 문장. 마지막에 "업로드 막을 문제" 개수와 "고치면 좋은 것" 개수.')
user = f'[사실표·계산 결과]\n{facts}\n\n[대본 — "- "로 시작하는 줄만 읽는다. [자막]·(화면)은 화면 글자]\n{script}'
m, out = cc.gemini_chat(kv, system, user)
(H / 'review_gemini_v2.md').write_text(f'[{m} · {time.strftime("%Y-%m-%d %H:%M")}]\n' + out, encoding='utf-8')
print(m); print(out)
