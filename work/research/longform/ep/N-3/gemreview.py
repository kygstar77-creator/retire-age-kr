# -*- coding: utf-8 -*-
# N-3 대본 심사(제미나이 한 자리) — 5항목 0~10점, 경쟁 첫 90초 자막과 나란히. 결과 review_gemini_score_v2.md
import sys, time, pathlib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))
import crosscheck as cc
H = pathlib.Path(__file__).resolve().parent
kv = cc.load_key('gemini_key.txt')
comp = (H / 'review_in_comp.md').read_text(encoding='utf-8')[:3500]
script = (H / 'script.md').read_text(encoding='utf-8')
system = ('너는 한국 경제 유튜브 대본 심사관이다. 경쟁 영상 첫 90초 자막과 나란히 놓고 대본을 5항목 0~10점으로 매긴다: '
          '① 처음 30초 안에 끝까지 볼 이유(약속) ② 지루한 구간(줄 인용) ③ 숫자·사실이 화면 자막의 원값과 맞나 ④ 사람이 말하듯 들리나(줄 인용) ⑤ 끝에 다음 행동 하나. '
          '항목마다 점수와 이유 한 줄, 꼭 고칠 줄 최대 3개(줄 인용 → 고칠 문장, 숫자 값은 바꾸지 말 것), 마지막 줄 "평균: x.x".')
user = f'[경쟁 자막]\n{comp}\n\n[대본 — "- " 줄이 말, [자막]·(화면)은 화면 글자]\n{script}'
m, out = cc.gemini_chat(kv, system, user, prefer='flash')
(H / 'review_gemini_score_v2.md').write_text(f'[{m} · {time.strftime("%Y-%m-%d %H:%M")}]\n' + out, encoding='utf-8')
print(m); print(out)
