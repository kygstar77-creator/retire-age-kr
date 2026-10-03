# lfvoice 자르기가 실패한 묶음(저장본 _raw/*.pcm)을 받아쓰기 시각으로 손수 자른다 — API는 받아쓰기만, TTS 재요청 없음. (PD 2026-10-03 E-2)
#   py -3.12 work/lfcut.py hear <ep폴더> <묶음번호> [--maxreq N]          # 저장본 받아쓰기(문장마다 [초]) + 0.12초 넘는 쉼 목록
#   py -3.12 work/lfcut.py cut  <ep폴더> <묶음번호> <시작1,시작2,...> [--apply] [--maxreq N]
#     시작 시각은 '아직 파일 없는 문장' 수만큼. 각 시각에 가장 가까운 쉼에서 자른다. 첫 시각 앞(TTS가 읽은 영어 지시문)은 버린다.
#     받아쓰기 시각은 실제보다 0.5~1초 늦게 찍히는 일이 많다 — 쉼 목록에서 긴 쉼(0.3초+)을 고르고 음절/초(5~8)로 확인한 뒤 --apply.
#   이미 잘못 잘린 문장 파일이 있으면 그 wav를 다른 이름으로 옮겨 '없는 문장'으로 만든 뒤 쓴다(같은 todo면 같은 저장본을 찾는다).
import sys, os, hashlib, io, wave, base64, json, urllib.request, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lfvoice as V
sys.stdout.reconfigure(encoding='utf-8')

def load(ep, gi, mr):
    cfg = V.lock(ep); g = V.pack(V.sections(ep), mr)[gi]
    texts = [V.speak(ep, t) for s in g for t in s['lines']]; todo = [t for t in texts if not os.path.exists(V.wav_of(ep, cfg, t)[1])]
    rk = hashlib.md5(('|'.join([cfg['model'], cfg['voice']] + todo)).encode()).hexdigest()[:16]
    raw = os.path.join(V.aud_dir(ep), '_raw', rk + '.pcm'); assert os.path.exists(raw), f'저장본 없음 {raw} (todo {len(todo)})'
    return cfg, todo, np.fromfile(raw, dtype=np.int16)

def gaps(pcm, mn=0.12):
    m, win = V.loud_mask(pcm.astype(np.float32), V.SR); out, i = [], 0
    while i < len(m):
        if not m[i]:
            k = i
            while k < len(m) and not m[k]: k += 1
            if i > 0 and k < len(m) and (k - i) * win / V.SR >= mn: out.append(((i + k) // 2 * win, (k - i) * win / V.SR))
            i = k
        else: i += 1
    return out

def hear(pcm):
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(V.SR); w.writeframes(pcm.tobytes())
    body = {'contents': [{'parts': [{'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(buf.getvalue()).decode()}},
            {'text': 'Transcribe this audio verbatim (it may begin with English words), one sentence per line, each line starting with its start time in seconds like [12.3].'}]}],
            'generationConfig': {'temperature': 0}}
    # LFCUT_MODELS=모델1,모델2 — flash 받아쓰기 하루 한도 429일 때 lite로 시각만 받는다(목소리 모델 아님, 규칙 1과 무관). 10/3 PD
    ms = [x for x in os.environ.get('LFCUT_MODELS', '').split(',') if x] or V.ALIGN_MODELS
    for t in range(6 if ms is V.ALIGN_MODELS else 2):
        for m in ms:
            try:
                r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={V.key()}",
                    data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
                return m + '\n' + r['candidates'][0]['content']['parts'][0]['text']
            except Exception as e: print('  받아쓰기 실패', m, str(e)[:40], file=sys.stderr)
        time.sleep(30)
    return None

if __name__ == '__main__':
    a = sys.argv[1:]; cmd, ep, gi = a[0], os.path.abspath(a[1]), int(a[2]); mr = int(a[a.index('--maxreq') + 1]) if '--maxreq' in a else 9
    cfg, todo, pcm = load(ep, gi, mr); G = gaps(pcm)
    print(f'묶음 {gi} · 없는 문장 {len(todo)} · 저장본 {len(pcm)/V.SR:.1f}초')
    for t in todo: print(f'  {V.syl(t)/6.3:4.1f}초(어림) {t[:40]}')
    print('쉼', [(round(p / V.SR, 2), round(d, 2)) for p, d in G])
    if cmd == 'hear': print(hear(pcm))
    elif cmd == 'cut':
        starts = [float(x) for x in a[3].split(',')]; assert len(starts) == len(todo), (len(starts), len(todo))
        cuts = [min(G, key=lambda x: abs(x[0] - s * V.SR))[0] for s in starts]; assert cuts == sorted(set(cuts)), '같은 쉼을 두 번 고름'
        segs = [pcm[x:y].astype(np.float32) for x, y in zip(cuts, cuts[1:] + [len(pcm)])]
        for t, sg in zip(todo, segs): print(f'  {len(sg)/V.SR:5.1f}초 {V.syl(t)/(len(sg)/V.SR):4.1f}음절/초 {t[:30]}')
        if '--apply' in a:
            pad = np.zeros(int(V.SR * 0.08), dtype=np.float32)
            for t, sg in zip(todo, segs): V.write(V.wav_of(ep, cfg, t)[1], np.concatenate([pad, sg, pad]))
            V.build(ep)
