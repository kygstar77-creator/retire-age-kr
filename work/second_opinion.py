# 순돌이의 의논 상대 — 큰 결정 전에 다른 AI(제미나이)에게 반대 의견을 받는다(2026-09-30).
#   py -3.12 work/second_opinion.py <결정 문서.md> [전략|사용자|법]   → 같은 폴더에 <이름>_<역할>.md (기본 전략)
# 참모 셋(2026-09-30 사장님 "참모는 한 명이면 되나?"): 전략(반대편) · 사용자(35세 직장인 파이어 준비자 입장) · 법(약관·정책·금융광고·저작권).
# 큰 결정엔 전략, 화면·기능엔 사용자까지, 발행·광고·데이터 사용엔 법까지 부른다.
# 사장님 2026-09-30: "니랑 의논할 AI는 필요 없나" — 오늘만 해도 주제 좁히기·요일 묶기·앱 먼저 같은 판단을 사장님이 짚어 고쳤다.
# 같은 모델끼리 검토하면 같은 곳을 못 본다. 그래서 다른 회사 모델(제미나이)을 '반대편 참모'로 쓴다. 무료 한도라 큰 결정에만:
#   전략·편성 변경, 운영 사이트 구조 변경, 새 채널·사업 착수, 유료 결재 요청, 정책 위험이 걸린 판단.
import sys, os, json, time, urllib.request, urllib.error
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite']  # lite는 flash 한도(429) 때 예비 — 결과 머리줄에 모델명이 남는다 (admin 10-01)
ASK = """당신은 이 사업의 냉정한 반대편 참모입니다. 아래 결정안을 칭찬하지 말고 공격하세요. 한국어로.
1) 이 결정이 틀릴 수 있는 가장 큰 이유 3가지(각각 어떤 근거·숫자가 부족한지)
2) 빠진 선택지(더 싸거나 빠르거나 안전한 대안) 2~3개
3) 숨은 위험(정책·법·브랜드·중구난방·비용)
4) 이 결정을 해도 된다면, 그 전에 반드시 확인할 것 3가지와 실패를 알아챌 신호
5) 한 줄 판정: 그대로 / 고쳐서 / 보류
모르는 건 모른다고 쓰고 지어내지 마세요.

[결정안]
"""

ROLES = {
    '전략': ASK,
    '사용자': """당신은 35세 직장인이고 월 300만원 저축, 자산 1억, '몇 살에 은퇴할 수 있나'가 궁금해 파이어맵을 처음 써 보는 사람입니다. 아래 기획을 실제 사용자로서 솔직하게 평가하세요. 한국어로.
1) 처음 30초에 무엇을 하게 되고, 어디서 헷갈리거나 그만두고 싶어지나
2) 다시 오고 싶게 만드는 것이 있나, 없다면 무엇이 있으면 오겠나
3) 친구에게 공유하고 싶은 순간이 있나
4) 믿음이 안 가는 부분(숫자·말투·광고)
5) 한 줄 판정: 쓰겠다 / 고치면 쓰겠다 / 안 쓰겠다
지어내지 말고 기획서에 있는 것만으로 판단하세요.

[기획]
""",
    # 카피 심사(사장님 10/02 06:18 "대본과 카피라이팅도 심사에 넣어") — 제목 후보·경쟁 상위 5개·본문을 한 파일에 넣고 부른다 (editor 10-02)
    '카피': """당신은 네이버 카페·유튜브 제목 심사위원입니다. 아래 [후보] 제목을 [경쟁 상위]와 나란히 놓고, 후보마다 다섯 항목을 0~10점으로 매기세요. 칭찬보다 깎을 이유부터. 한국어로.
① 1초에 주제가 보이나 ② 궁금증 장치가 하나 있나 ③ 낚시·과장이 아닌가(본문 사실과 일치) ④ 경쟁 제목 틀이나 우리 지난 제목 틀('~할까?' 질문형)을 반복하지 않나 ⑤ 검색어가 앞에 있나
형식: 후보마다 '①②③④⑤ 점수 / 평균 / 한 줄 이유', 끝에 '1위 후보'와, 8점 미만이면 고칠 점 한 줄. 본문에 없는 사실을 지어내지 마세요.

""",
    '법': """당신은 한국 온라인 서비스의 법·정책 검토 담당입니다. 아래 결정안을 한국 법(저작권법·금융소비자보호법·자본시장법 유사투자자문·개인정보보호법·표시광고법)과 플랫폼 정책(유튜브·네이버·구글 애드센스)에 비춰 위험을 찾으세요. 한국어로.
1) 걸릴 수 있는 조항·정책과 이유(조문 번호는 확실할 때만, 모르면 '확인 필요')
2) 위험도(높음/중간/낮음)
3) 안전하게 바꾸는 방법
4) 사람 전문가(변호사 등) 확인이 꼭 필요한 부분
지어내지 마세요.

[결정안]
"""}

def main(path, role='전략'):
    doc = open(path, encoding='utf-8').read()[:60000]
    body = {'contents': [{'parts': [{'text': ROLES.get(role, ASK) + doc}]}]}
    for m in MODELS:
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(
                f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=300))
            t = ''.join(p.get('text', '') for p in r['candidates'][0]['content']['parts'])
            out = os.path.splitext(path)[0] + f'_{role}.md'
            open(out, 'w', encoding='utf-8').write(f'[{m} · {time.strftime("%Y-%m-%d %H:%M")}]\n' + t)
            print('저장', out); return
        except urllib.error.HTTPError as e: print(' ', m, e.code); time.sleep(5)
        except Exception as e: print(' ', m, str(e)[:100])
    print('제미나이가 모두 막힘 — Claude 하위 작업자에게 같은 질문으로 반론을 받는다'); sys.exit(1)

if __name__ == '__main__': main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '전략')
