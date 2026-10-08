# -*- coding: utf-8 -*-
# W-1 1화 대본 제미나이 검증(사실 대조 + 정책·권유 위험). 결과 review_v1_gemini.md
import sys, time, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))
import crosscheck as cc
H = pathlib.Path(__file__).resolve().parent
kv = cc.load_key('gemini_key.txt')
raw = H / 'w1009' / 'raw'
src = ''.join(f'\n[원문 {p.name}]\n' + p.read_text(encoding='utf-8')[p.read_text(encoding='utf-8').find('삼성전자/'):][:2500] for p in sorted(raw.glob('dart_*.txt')))
facts = (H / 'calc_out.txt').read_text(encoding='utf-8') + '\n' + (H / 'facts_2026-10-09.txt').read_text(encoding='utf-8') + src
script = (H / 'script.md').read_text(encoding='utf-8')
system = ('너는 한국 금융 유튜브 대본 검증자다. 칭찬은 빼고 문제만. 사실표·공시 원문에 없는 숫자·사실, 사실표와 다른 숫자, 반올림이 틀린 말, '
          '오해를 부를 단정, 날짜·요일 오류, 원인을 단정하는 문장, 투자 권유로 들릴 문장, 유튜브 금융 정책 위험을 찾는다. '
          '각 지적: 줄 인용 → 무엇이 틀렸나 → 고칠 문장. 마지막에 "업로드 막을 문제" 개수와 "고치면 좋은 것" 개수를 적어라. '
          '참고: 2026-10-03은 토요일, 10-05(월) 대체공휴일, 10-09(금) 한글날. {F} 표시는 미국 금요일 종가로 갱신 예정인 가안이다.')
m, out = cc.gemini_chat(kv, system, f'[사실표·계산·원문]\n{facts}\n\n[대본]\n{script}')
(H / 'review_v1_gemini.md').write_text(f'[{m} · {time.strftime("%Y-%m-%d %H:%M")}]\n' + out, encoding='utf-8')
print(m); print(out)
