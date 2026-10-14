# P-1 썸네일·제목 한글 다시(사장님 10/14 오후 "위에 썸네일 제목 한글 이해 안 가는데.") — 제미나이 4(gemini-4-argon)에 같은 조건으로 문구 안 받기.
#   py -3.12 gem4_1014.py  → gem4_1014.md (키는 crosscheck.load_key, 출력하지 않음)
import sys, os, json, urllib.request, urllib.error, time
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..')))
from crosscheck import load_key
KEY = load_key('gemini_key.txt')['KEY']
MODEL = 'gemini-4-argon'
P = """한국 재테크 유튜브 롱폼 한 편의 썸네일 문구와 제목을 만들어 주세요.

[영상 내용 — 사실, 바꾸지 말 것]
- 1969년생은 국민연금을 65세에 받는다(제때). 국민연금법상 1년 일찍 받을 때마다 연금이 6%씩 줄어든다.
- 5년 일찍(60세) 받으면 연금이 30% 줄고, 받은 돈을 쌓아 보면 76.7세부터 제때(65세) 받은 쪽이 더 많아진다.
- 1년 일찍(64세) 받으면 6% 줄고, 80.7세부터 제때 받은 쪽이 더 많아진다. 즉 조금만 당길수록 그 나이가 오히려 늦어진다.
- 영상은 언제 받으라고 권하지 않는다. 답은 건강·다른 돈에 달렸다고 맺는다.

[문제] 지금 문구 '1969년생 · 국민연금 / 제때(65세) 받은 쪽이 따라잡는 나이 / 5년 당김 76.7세 · 1년 당김 80.7세'와
제목 '국민연금 수령나이, 1년만 당기면 따라잡히는 나이가 오히려 늦다'를 채널 주인이 이해하지 못했다.

[같은 주제 상위 영상이 실제로 쓰는 말 — 이런 쉬운 말을 쓸 것]
'국민연금, 몇 살부터 받는게 유리할까?'(91만 회) · '손익분기점 찍어봄 국민연금 조기수령'(21만 회) · '"당겨 받자" "오히려 손해" 국민연금 조기 수령, 진실은?'(38만 회) · 검색어 '국민연금 조기수령 손해'·'국민연금 수령나이'

[조건]
- 50~60대가 한 번 읽고 바로 이해하는 말. 새 말을 지어내지 말 것.
- 낚시 금지: 영상 내용과 다른 말 금지. '받으세요·받지 마세요·무조건' 같은 권유·명령 금지.
- 썸네일: 큰 말 1줄(20자 안팎) + 두 칸(5년 일찍 / 1년 일찍, 각 칸에 76.7세·80.7세) + 작은 줄 '1969년생 기준' 정도. 휴대폰 목록 168px에서도 읽혀야 한다.
- 제목: 숫자 2개 이하, '국민연금' 맨 앞, 45자 이하.

[답 형식]
썸네일 안 5개: 번호 | 큰 말 | 왼쪽 칸 | 오른쪽 칸 | 작은 줄 | 한 줄 이유
제목 안 5개: 번호 | 제목 | 숫자 개수 | 한 줄 이유
마지막 줄: 가장 좋은 조합(썸네일 번호 + 제목 번호)"""


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
stamp = time.strftime('%Y-%m-%d %H:%M')
with open(os.path.join(H, 'gem4_1014.md'), 'a', encoding='utf-8') as f:
    f.write(f'\n## {stamp} [{MODEL}] {st}\n\n{out}\n')
print(st); print(out)
