# -*- coding: utf-8 -*-
# N-3 대본 제미나이 검증(사실 대조 + 권유 위험 + 말투). 결과 review_gemini_v1.md (K-1 gemcheck.py 꼴)
import sys, time, pathlib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))
import crosscheck as cc
H = pathlib.Path(__file__).resolve().parent
kv = cc.load_key('gemini_key.txt')
facts = (H / 'research.md').read_text(encoding='utf-8').split('# 대조', 1)[1] + chr(10) + (H / 'calc_out.txt').read_text(encoding='utf-8')
script = (H / 'script.md').read_text(encoding='utf-8')
system = ('너는 한국 직장인 연봉 실수령액(4대보험·근로소득 간이세액·국세청 근로소득 백분위) 유튜브 대본 검증자다. 칭찬은 빼고 문제만. 사실표·계산 결과에 없는 숫자·사실, 사실표와 다른 숫자, 반올림이 틀린 말, '
          '국세청 구간 평균을 경계값처럼 말한 문장, 계약 연봉·총급여·세후를 섞어 쓴 문장, 간이세액(미리 떼는 값)을 최종 세금처럼 말한 문장, 소득세율 구간 설명이 틀린 말, '
          '이직·연봉 협상·투자를 권하는 문장, 가상 인물, 사람이 소리 내 말할 때 어색한 단어를 찾는다. '
          '각 지적: 줄 인용 → 무엇이 문제 → 고칠 문장. 마지막에 "업로드 막을 문제" 개수와 "고치면 좋은 것" 개수.')
user = f'[사실표·계산 결과]\n{facts}\n\n[대본 — "- "로 시작하는 줄만 읽는다. [자막]·(화면)은 화면 글자]\n{script}'
m, out = cc.gemini_chat(kv, system, user)
(H / 'review_gemini_v1.md').write_text(f'[{m} · {time.strftime("%Y-%m-%d %H:%M")}]\n' + out, encoding='utf-8')
print(m); print(out)
