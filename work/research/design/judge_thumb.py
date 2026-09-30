# 썸네일 미감 심사(제미나이, 이미지 읽기) — conductor-manual '눈으로 보는 결과물의 검수' 2번.
#   py -3.12 work/research/design/judge_thumb.py <우리 시안.png> <경쟁1.jpg> [경쟁2.jpg ...]  → 표준출력
# 경쟁 상위작과 나란히 보여 주고 "먼저 누르고 싶은가 1~10점과 이유"를 묻는다. 무료 텍스트 모델 한도 안에서 한 번.
import sys, json, base64, mimetypes, urllib.request, urllib.error
sys.stdout.reconfigure(encoding='utf-8')
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-2.5-flash']
ASK = """당신은 한국 유튜브에서 배당 ETF 영상을 자주 보는 40대 시청자이자 썸네일 심사위원입니다.
첫 이미지가 심사 대상(A)이고, 나머지는 같은 주제의 경쟁 상위작(조회 수만~수십만)입니다.
휴대폰 목록에서 이 썸네일들이 나란히 보인다고 상상하세요. 한국어로, 칭찬보다 냉정하게.
1) A를 경쟁작보다 먼저 누르고 싶은가? 1~10점(6점 = 경쟁작과 비슷)
2) 그 점수의 이유 3가지
3) A에서 가장 먼저 눈에 들어오는 것, 3초 안에 이해되는 내용
4) 점수를 2점 올릴 가장 효과 큰 고칠 점 3가지(구체적으로: 크기·위치·그림·문구)
5) 오해를 부르거나 과장으로 보이는 부분이 있나
첫 줄은 반드시 '점수: N' 형식으로."""

def part(path):
    mt = mimetypes.guess_type(path)[0] or 'image/png'
    return {'inline_data': {'mime_type': mt, 'data': base64.b64encode(open(path, 'rb').read()).decode()}}

def main(paths):
    body = {'contents': [{'parts': [{'text': ASK}] + [part(p) for p in paths]}]}
    for m in MODELS:
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(
                f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
            print(f'[모델 {m}]')
            print(r['candidates'][0]['content']['parts'][0]['text'])
            return
        except urllib.error.HTTPError as e:
            print(f'[{m} 실패 {e.code}]', file=sys.stderr)
        except Exception as e:
            print(f'[{m} 실패 {e}]', file=sys.stderr)
    sys.exit('모든 모델 실패')

if __name__ == '__main__':
    main(sys.argv[1:])
