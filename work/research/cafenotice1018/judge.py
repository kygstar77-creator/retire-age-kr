# 공지 묶음 2개 제목·표지 심사(제미나이 2회) — 카페 운영 설계자 10/18
import sys, os, json, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
M = 'gemini-3.1-flash-lite'
def ask(text):
    err = ''
    for t in range(4):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={KEY}', data=json.dumps({'contents': [{'parts': [{'text': text}]}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            err = str(e); time.sleep(5)
    return '(실패 ' + err + ')'
R = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research'
def body(n): return '\n'.join(open(os.path.join(R, n, 'pkg', f), encoding='utf-8').read() for f in sorted(os.listdir(os.path.join(R, n, 'pkg'))) if f[:1] == 'c' and f[1:3].isdigit())
comp = '''[다른 재테크 카페의 신입 안내·질문 공지 제목(공개 API 10/18)]
서집달 신입 회원님 혜택 + 서집달 가이드 영상 입니다. ^^
[신입회원 필독] 서집달 로드맵 (26.10.3. 업데이트)
정회원 등업 신청 방법
[가입 EVENT] 가입만 해도 커피 쿠폰이!? 노후연 회원 환영 이벤트 안내
네이버 카페에서도 '이읽남'을 구독하세요'''
covers = {'cafenotice1018': "파란 바탕, 열린 문 그림. 큰 글 '처음 오셨나요 / 가입인사 한 줄이면', 노란 줄 '궁금한 것부터 답해요', 작은 줄 '퇴직 · 연금 · 건보료 계산 카페'",
          'cafeqna1018': "파란 바탕, 손 내미는 그림. 큰 글 '질문 받습니다 / 퇴직 뒤 건보료·연금', 노란 줄 '댓글 한 줄이면 답해요', 작은 줄 '가입하면 바로 댓글'"}
out = []
for n in ('cafenotice1018', 'cafeqna1018'):
    title = open(os.path.join(R, n, 'pkg', 'title.txt'), encoding='utf-8').read().strip()
    P = ('네이버 카페(회원 3명, 은퇴·연금·건보료·배당 계산 정보 카페)의 공지 글 심사. 처음 들어온 50대가 이 글을 눌러 읽고 가입·댓글을 하게 만드는 게 목표.\n' + comp +
         f'\n[제목]\n{title}\n[대표 이미지]\n{covers[n]}\n[본문]\n{body(n)}\n' +
         '기준: ①1초에 무슨 글인지 ②눌러 볼 이유 ③과장·낚시 아님(본문과 일치) ④AI 티·군더더기 없음 ⑤처음 온 사람이 할 행동이 하나로 분명. 6=보통, 7=통과, 8=목표.\n'
         '답 형식: "제목: N — 이유" / "표지: N — 이유" / "고칠 문장: <원문> → <고친 문장>"(있으면 최대 3개).')
    for i in (1, 2):
        t = ask(P); out.append(f'## {n} 제미나이 {i}회\n{t}'); print(f'## {n} {i}\n{t[:1500]}\n--')
open(os.path.join(R, 'cafenotice1018', 'judge_raw.md'), 'a', encoding='utf-8').write('\n\n'.join(out) + '\n===\n')
