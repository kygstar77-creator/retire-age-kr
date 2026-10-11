# 롱폼 문장 wav 앞머리를 잘라 새 wav로(새 녹음 없음) + 잘린 것·남은 것 받아쓰기로 확인 (10/11 순돌이: minmonth 첫 말 '그래서'만 뺀다)
#   py -3.12 work/research/cardshorts/m1clips_trim.py <audio 상대경로> <자를 초> [--hear]
# 쉼(무음) 안에서 자른다. 앞에 0.10초 무음을 두고 8ms 페이드인 — 치직이 생기지 않게. 원본 wav는 그대로 둔다.
import os, sys, wave, io, json, base64, urllib.request
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..'))
PUB = os.path.join(WORK, 'video', 'public')
sys.path.insert(0, WORK)


def hear(pcm, sr):
    import lfvoice
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.astype(np.int16).tobytes())
    body = {'contents': [{'parts': [{'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(buf.getvalue()).decode()}},
                                    {'text': 'Transcribe this Korean audio verbatim. Output only the transcript. If there is no speech, output (무음).'}]}],
            'generationConfig': {'temperature': 0}}
    for m in lfvoice.ALIGN_MODELS + ['gemini-3.1-flash-lite', 'gemini-flash-lite-latest']:   # 10/11 flash 전부 429 → lite로 받아씀
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={lfvoice.key()}',
                data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=120))
            return m, r['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception as e: print('  받아쓰기 실패', m, str(e)[:40])
    return None, None


def main(rel, at, do_hear):
    src = os.path.join(PUB, rel)
    with wave.open(src) as w: sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
    i = int(at * sr)
    k = sr // 100; seg = a[max(0, i - k): i + k]
    print(f'자를 곳 ±10ms rms {np.sqrt((seg ** 2).mean()):.0f} (무음이면 수백 이하)')
    head, tail = a[:i], a[i:].copy()
    f = int(0.008 * sr); tail[:f] *= np.linspace(0, 1, f)
    out = np.concatenate([np.zeros(int(0.10 * sr), np.float32), tail])
    dst_rel = rel.replace('.wav', f'_from{int(round(at * 100)):03d}.wav')
    with wave.open(os.path.join(PUB, dst_rel), 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.clip(out, -32768, 32767).astype(np.int16).tobytes())
    sec = len(out) / sr
    print(f'새 wav {dst_rel} · {sec:.2f}초 (원본 {len(a) / sr:.2f}초) · frames {int(round(sec * 30)) + 8}')
    if do_hear:
        print('잘라 낸 앞머리 받아쓰기:', hear(head, sr))
        print('남은 문장 받아쓰기:', hear(out, sr))
    return dst_rel, sec


if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]), '--hear' in sys.argv)
