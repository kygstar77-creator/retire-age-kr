# 구글 클라우드 Text-to-Speech (Chirp 3 HD) — 2026-10-11 사장님 "진짜 돈 나가게 하면 안 된다".
#   py -3.12 work/cloudtts.py say "<문장>" <출력.wav> [목소리] [--nomark]   # 기본 ko-KR-Chirp3-HD-Charon · 쉼 태그 켬
#   markup: synth(..., mark=True, 10/19부터 기본) → input.markup에 쉼 태그(쉼표 뒤 [pause short]·줄 안 문장 끝 [pause], 글에 이미 있는 태그는 그대로) — 글자 수 장부는 보내는 글(태그 포함) 길이
#     mark=False면 글 속 태그를 빼고 text로 보낸다(태그를 소리 내 읽지 않게)
#   py -3.12 work/cloudtts.py usage                              # 이번 달 쓴 글자 수
# 돈 안 나가게 하는 장치(코드로 막는다):
#   ① Chirp 3 HD 목소리만 허용 — 가격표상 무료 사용 한도가 있는 모델은 이것뿐(매달 0~100만 자, cloud.google.com/text-to-speech/pricing 10/11 확인).
#      Gemini-TTS·Studio·즉석 커스텀 음성은 무료 한도가 없거나 비싸서 이 도구로는 못 부른다.
#   ② 이번 달 누적 90만 자(무료 100만의 90%, 10/19 사장님 지시로 50만→90만)를 넘기면 부르기 전에 멈춘다. 장부 = work/research/tts_usage.jsonl
#   ③ 열쇠는 저장소 밖 C:\Users\강영준\Documents\google_tts_sa.json (서비스 계정 firemap-tts@firemap-509507). 절대 커밋·출력하지 않는다.
#   ④ 프로젝트 firemap-509507은 무료 체험(2027-01-10까지): "You will not be billed for any Google Cloud usage during your Free Trial."
#      체험 뒤 '업그레이드'는 사장님만 누른다 — 업그레이드 전에는 이 도구가 멈출 뿐 청구되지 않는다.
import sys, os, re, json, base64, datetime, wave, io
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
KEY = r'C:\Users\강영준\Documents\google_tts_sa.json'
LEDGER = os.path.join(HERE, 'research', 'tts_usage.jsonl')
MONTH_CAP = 900_000   # 10/19 사장님 "50만도 우리가 정한 거잖아, 100만 자까지 무료라며" → 무료 100만의 90%(장부 오차 여유 10%)
SR = 24000

def month_used(month=None):
    month = month or datetime.date.today().strftime('%Y-%m')
    if not os.path.exists(LEDGER): return 0
    return sum(json.loads(l)['chars'] for l in open(LEDGER, encoding='utf-8') if l.strip() and json.loads(l)['ts'][:7] == month)

def session():
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    return AuthorizedSession(service_account.Credentials.from_service_account_file(KEY, scopes=['https://www.googleapis.com/auth/cloud-platform']))

_S = None
def markup(text):
    # 10/12 순돌이 [지시·긴급]: Chirp 3 HD markup 쉼 태그 — 쉼표 뒤 [pause short], 줄 안 문장 끝 뒤 [pause](줄 끝 쉼은 lfvoice가 자르고 붙인다)
    # 10/19 voice-naturalness: 글에 이미 쉼 태그가 있으면(korsay.phrase가 넣은 [pause short]) 그 자리엔 더 넣지 않는다 — 넣으면 쉼이 두 번 겹친다.
    t = re.sub(r',\s*(?!\[pause)(?=\S)', ', [pause short] ', text)
    return re.sub(r'([.?!])\s+(?!\[pause)(?=\S)', lambda m: m.group(1) + ' [pause] ', t)

TAG = re.compile(r'\s*\[pause[^\]]*\]')
def plain(text):
    # 쉼 태그를 뺀 글(markup을 안 쓰는 요청·글자 수 비교용)
    return re.sub(r'\s{2,}', ' ', TAG.sub(' ', text)).strip()

def synth(text, voice='ko-KR-Chirp3-HD-Charon', tag='', rate=None, mark=True):
    """문장 하나 → 24kHz mono int16 PCM bytes. 막히면 예외.
    rate = audioConfig.speakingRate(0.25~2.0, Chirp 3 HD 'pace control' — docs.cloud.google.com/text-to-speech/docs/chirp3-hd 10/11 확인). 글자 수 과금은 같다."""
    global _S
    if 'Chirp3-HD' not in voice: raise SystemExit(f'막음: {voice} — Chirp 3 HD만 허용(무료 한도 있는 모델)')
    # 10/19: 쉼 태그 기본 켬(mark=True, 사장님 10/13 '3번' 고름) — 쇼츠·CLI도 같은 기본. 글자 수는 보내는 글(태그 포함) 길이로 센다(장부를 넉넉히).
    sent = markup(text) if mark else plain(text)
    n = len(sent)
    used = month_used()
    if used + n > MONTH_CAP: raise SystemExit(f'막음: 이번 달 {used:,}자 + {n:,}자 > 상한 {MONTH_CAP:,}자(무료 100만 자의 90%)')
    _S = _S or session()
    body = {'input': {'markup': sent} if mark else {'text': sent}, 'voice': {'languageCode': voice[:5], 'name': voice},
            'audioConfig': {'audioEncoding': 'LINEAR16', 'sampleRateHertz': SR}}
    if rate and float(rate) != 1.0:
        if not 0.25 <= float(rate) <= 2.0: raise SystemExit(f'막음: speakingRate {rate} — 0.25~2.0만')
        body['audioConfig']['speakingRate'] = float(rate)
    r = _S.post('https://texttospeech.googleapis.com/v1/text:synthesize', json=body, timeout=120)
    if not r.ok: raise RuntimeError(f'{r.status_code} {r.text[:200]}')
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    with open(LEDGER, 'a', encoding='utf-8') as f:
        f.write(json.dumps({'ts': datetime.datetime.now().isoformat(timespec='seconds'), 'chars': n, 'voice': voice, 'tag': tag, **({'rate': float(rate)} if rate and float(rate) != 1.0 else {})}, ensure_ascii=False) + '\n')
    wav = base64.b64decode(r.json()['audioContent'])
    with wave.open(io.BytesIO(wav)) as w: return w.readframes(w.getnframes())

def save(pcm, fn):
    with wave.open(fn, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm)

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'usage'
    if cmd == 'usage':
        u = month_used(); print(f'이번 달 {u:,}자 / 상한 {MONTH_CAP:,}자 / 무료 1,000,000자')
    elif cmd == 'say':
        save(synth(sys.argv[2], sys.argv[4] if len(sys.argv) > 4 and not sys.argv[4].startswith('--') else 'ko-KR-Chirp3-HD-Charon', 'cli', mark='--nomark' not in sys.argv), sys.argv[3]); print('저장', sys.argv[3])
