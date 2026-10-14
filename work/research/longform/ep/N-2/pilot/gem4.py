# N-2 시범작 — 제미나이 4(gemini-4-argon)에게 같은 장을 다시 쓰게 해서 더 쉬운 쪽을 고른다(지시 10/14 ③).
#   py -3.12 gem4.py [say 파일]  → gem4_out.md (키는 crosscheck.load_key, 출력하지 않음). 429면 1시간 뒤 다시(우회 금지).
import sys, os, json, urllib.request, urllib.error, time
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..')))
from crosscheck import load_key
KEY = load_key('gemini_key.txt')['KEY']
MODEL = 'gemini-4-argon'
script = open(os.path.join(H, 'script.md'), encoding='utf-8').read().split('\n---\n')[1]
P = f"""한국 유튜브 롱폼 영상 내레이션을 더 쉽게 다시 써 주세요.

[듣는 사람] 경제 지식이 없는 50~60대. 휴대폰으로 한 번 듣고 지나간다. '중위·분포·백분위·구간' 같은 말을 모른다.

[사실 — 바꾸지 말 것] 국가데이터처 「2024년 임금근로일자리 소득(보수) 결과」(2026-02-23), 2024년 12월 세전 월 보수, 일자리 기준.
- 55~59세 평균 424만원, 가운데(중위) 287만원, 월 1,000만원 이상 7.2%, 월 350만원 이상 39.9%
- 55~59세 가운데 월급: 중소기업 253만원, 대기업 621만원
- 월 350만원 이상: 25~29세 28.8%, 40~44세 55.6%
- 그달 하루 이상 일한 사람이 모두 들어 있다(짧게 일한 사람 포함).
- 상호 씨는 가상 인물(57세, 작은 부품 공장 관리직, 세전 월 350만원).

[조건]
- 장마다 '말' 줄만 다시 쓴다. 장 제목·순서·인물은 그대로. 말에는 반올림한 숫자만(정확한 값은 화면에 따로 나온다).
- 문장은 짧게, 한 문장에 숫자 하나. 빌린 비유(영수증 등)·과장·'놀랍게도/정리하면/첫 번째' 같은 말 금지. 권유·전망 금지.
- 새 사실을 지어내지 말 것.

[지금 대본 — '- '로 시작하는 줄이 말, 괄호와 대괄호는 화면]
{script}

[답 형식]
장마다: '## 장 제목' 다음 줄에 다시 쓴 말 줄('- '로 시작).
맨 끝에 '바꾼 이유' 5줄 이하."""


def ask():
    body = json.dumps({'contents': [{'parts': [{'text': P}]}]}).encode()
    req = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}', data=body,
                                 headers={'Content-Type': 'application/json'})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=300))
        return 'ok', r['candidates'][0]['content']['parts'][0]['text']
    except urllib.error.HTTPError as e:
        return f'HTTP {e.code}', e.read().decode('utf-8', 'replace')[:600].replace(KEY, '***')
    except Exception as e:
        return 'err', str(e).replace(KEY, '***')


st, out = ask()
open(os.path.join(H, 'gem4_out.md'), 'w', encoding='utf-8').write(f'# 제미나이 4 다시 쓰기 ({MODEL}, {time.strftime("%Y-%m-%d %H:%M")}, {st})\n\n{out}\n')
print(st)
