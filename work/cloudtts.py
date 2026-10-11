# 구글 클라우드 Text-to-Speech (Chirp 3 HD) — 2026-10-11 사장님 "진짜 돈 나가게 하면 안 된다".
#   py -3.12 work/cloudtts.py say "<문장>" <출력.wav> [목소리]   # 기본 ko-KR-Chirp3-HD-Charon
#   py -3.12 work/cloudtts.py usage                              # 이번 달 쓴 글자 수
# 돈 안 나가게 하는 장치(코드로 막는다):
#   ① Chirp 3 HD 목소리만 허용 — 가격표상 무료 사용 한도가 있는 모델은 이것뿐(매달 0~100만 자, cloud.google.com/text-to-speech/pricing 10/11 확인).
#      Gemini-TTS·Studio·즉석 커스텀 음성은 무료 한도가 없거나 비싸서 이 도구로는 못 부른다.
#   ② 이번 달 누적 50만 자(무료 한도의 절반)를 넘기면 부르기 전에 멈춘다. 장부 = work/research/tts_usage.jsonl
#   ③ 열쇠는 저장소 밖 C:\Users\강영준\Documents\google_tts_sa.json (서비스 계정 firemap-tts@firemap-509507). 절대 커밋·출력하지 않는다.
#   ④ 프로젝트 firemap-509507은 무료 체험(2027-01-10까지): "You will not be billed for any Google Cloud usage during your Free Trial."
#      체험 뒤 '업그레이드'는 사장님만 누른다 — 업그레이드 전에는 이 도구가 멈출 뿐 청구되지 않는다.
import sys, os, json, base64, datetime, wave, io
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
KEY = r'C:\Users\강영준\Documents\google_tts_sa.json'
LEDGER = os.path.join(HERE, 'research', 'tts_usage.jsonl')
MONTH_CAP = 500_000
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
def synth(text, voice='ko-KR-Chirp3-HD-Charon', tag=''):
    """문장 하나 → 24kHz mono int16 PCM bytes. 막히면 예외."""
    global _S
    if 'Chirp3-HD' not in voice: raise SystemExit(f'막음: {voice} — Chirp 3 HD만 허용(무료 한도 있는 모델)')
    n = len(text)
    used = month_used()
    if used + n > MONTH_CAP: raise SystemExit(f'막음: 이번 달 {used:,}자 + {n:,}자 > 상한 {MONTH_CAP:,}자(무료 100만 자의 절반)')
    _S = _S or session()
    body = {'input': {'text': text}, 'voice': {'languageCode': voice[:5], 'name': voice},
            'audioConfig': {'audioEncoding': 'LINEAR16', 'sampleRateHertz': SR}}
    r = _S.post('https://texttospeech.googleapis.com/v1/text:synthesize', json=body, timeout=120)
    if not r.ok: raise RuntimeError(f'{r.status_code} {r.text[:200]}')
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    with open(LEDGER, 'a', encoding='utf-8') as f:
        f.write(json.dumps({'ts': datetime.datetime.now().isoformat(timespec='seconds'), 'chars': n, 'voice': voice, 'tag': tag}, ensure_ascii=False) + '\n')
    wav = base64.b64decode(r.json()['audioContent'])
    with wave.open(io.BytesIO(wav)) as w: return w.readframes(w.getnframes())

def save(pcm, fn):
    with wave.open(fn, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm)

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'usage'
    if cmd == 'usage':
        u = month_used(); print(f'이번 달 {u:,}자 / 상한 {MONTH_CAP:,}자 / 무료 1,000,000자')
    elif cmd == 'say':
        save(synth(sys.argv[2], sys.argv[4] if len(sys.argv) > 4 else 'ko-KR-Chirp3-HD-Charon', 'cli'), sys.argv[3]); print('저장', sys.argv[3])
