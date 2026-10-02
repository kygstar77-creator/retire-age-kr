# judge_flash.py 복사 — flash 429일 때 lite로(10/02 15:2x 순돌이 13:2x 결정)
#   py -3.12 judge_flash.py d1k d1l d1m ...
import sys, os, json, base64, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3.1-flash-lite']  # flash 3종 15:2x 429 → 순돌이 결정대로 lite, 표에 'lite' 표시
def ask(m, text, paths):
    parts = [{'text': text}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in paths]
    r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
        data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
    return r['candidates'][0]['content']['parts'][0]['text']
def prompt(T):
    return ('한국 재테크 유튜브 썸네일 심사. 이미지는 휴대폰 목록 크기(가로 168px) 비교판. "우리 ' + T.upper() + '"가 공개 전 시안, "경쟁"은 같은 주제 상위작.\n'
      '영상: 퇴직 후 지역가입자 건강보험료 — 배당·이자 연 1,000만원과 1,001만원 경계에서 월 건보료 22,800원→67,850원(2.98배), 1년 54만원 차이.\n'
      '제목: "퇴직 후 건강보험료, 배당·이자 1만원 차이에 1년 54만원?" (썸네일은 제목 반복 말고 보완)\n'
      '제약: 인물·캐릭터 금지, 과장·낚시 금지, 오른쪽 아래 비움, 경쟁 배치·색을 따라 하지 않음.\n'
      '답 형식: 첫 줄 "' + T.upper() + ' 점수: N"(1~10, 경쟁 상위작 옆에서 먼저 누르고 싶은가, 6=경쟁 평균, 7=통과) · 1초 주제 한 문장 · 후킹 장치 · 경쟁과 비슷해 보이는 점 수 · 7점 미만이면 고칠 것 2가지.')
targets = sys.argv[1:]
for m in MODELS:
    try:
        out = {}
        for T in targets:
            out[T] = ask(m, prompt(T), [os.path.join(H, 'board4_' + T + '.png')])
        txt = f'[모델 {m}] (같은 모델로 {", ".join(targets)} 함께)\n\n' + '\n\n---\n'.join(f'## {t}\n{o}' for t, o in out.items())
        open(os.path.join(H, 'gemini_lite_' + '_'.join(targets) + '.md'), 'w', encoding='utf-8').write(txt); print(txt); break
    except Exception as e: print(f'[{m} 실패 {e}]', file=sys.stderr)
else: print('(flash 전부 실패)')
