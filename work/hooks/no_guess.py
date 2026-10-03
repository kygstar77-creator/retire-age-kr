# 사장님 메시지마다 순돌이 답 전에 붙는 점검(UserPromptSubmit 훅) — 2026-10-04 사장님 "계속 추측에 니 생각대로 진행하는 거 왜 그런 거야?"
import json, sys
msg = ("[답하기 전 점검 — 추측 금지] 이 답에 원인·기준·규칙·비교·'사람은 이렇다' 같은 판단이 들어가면, 문장마다 근거(실측 숫자·파일·공식 출처 URL)를 붙인다. "
       "근거가 없으면 그 판단을 말하지 말고 '확인 안 함'이라고 쓴 뒤 무엇을 어떻게 재서 확인할지만 말하거나, 지금 바로 잰다. "
       "내가 지은 분류·비유어(예: 알맹이)·판정 기준을 규칙이나 지시로 내보내지 않는다. 직원·클라우드에게 보내는 지시도 같다.")
print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": msg}}))
