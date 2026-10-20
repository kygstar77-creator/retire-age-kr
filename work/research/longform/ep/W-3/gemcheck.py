# -*- coding: utf-8 -*-
# W-3 대본 제미나이 검증(사실 대조 + 권유 위험 + 말투). 결과 review_gemini_v1.md
import sys, re, time, pathlib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))
import crosscheck as cc
H = pathlib.Path(__file__).resolve().parent
kv = cc.load_key('gemini_key.txt')
r = (H / 'research.md').read_text(encoding='utf-8')
m = re.search(r'^# 대조.*?(?=^#\s|\Z)', r, re.M | re.S)
facts = (H / 'facts.txt').read_text(encoding='utf-8') + chr(10) + (m.group(0) if m else '')
script = (H / 'script.md').read_text(encoding='utf-8')
system = ('너는 한국 배당소득 세금 유튜브 대본 검증자다. 칭찬은 빼고 문제만. 사실표에 없는 숫자·사실, 사실표와 다른 숫자, 반올림이 틀린 말, '
          '고배당기업 배당소득 분리과세(조세특례제한법 §104의27) 요건·세율 구간·적용 시기·신청 방법 설명이 틀리거나 빠져 오해를 부를 말, '
          '금융소득 2천만원 종합과세 기준·원천징수 14%·지방소득세 설명이 틀린 말, 건보료처럼 아직 정해지지 않은 것을 정해진 듯 말한 문장, '
          '특정 종목을 사라·팔라는 권유나 세무 상담으로 들릴 문장(자본시장법·세무사법·유튜브 정책 위험), 사람이 소리 내 말할 때 어색한 단어를 찾는다. '
          '각 지적: 줄 인용 → 무엇이 문제 → 고칠 문장. 마지막에 "업로드 막을 문제" 개수와 "고치면 좋은 것" 개수.')
user = f'[사실표·대조표]\n{facts}\n\n[대본 — "- "로 시작하는 줄만 읽는다. [자막]·(화면)은 화면 글자]\n{script}'
mm, out = cc.gemini_chat(kv, system, user)
(H / 'review_gemini_v1.md').write_text(f'[{mm} · {time.strftime("%Y-%m-%d %H:%M")}]\n' + out, encoding='utf-8')
print(mm); print(out)
