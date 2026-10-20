import sys, json, wave, numpy as np
sys.path.insert(0, '.'); import voicenat
def sim(js):
    p = json.load(open(js, encoding='utf-8')); out = np.zeros(16000 * 182, np.float32); a = 0
    for s in p['scenes']:
        b = a
        for l in s['lines']:
            if l.get('audio') and b / 30 < 180:
                w = wave.open('video/public/' + l['audio']); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; sr = w.getframerate()
                x = np.interp(np.arange(0, len(x), sr / 16000), np.arange(len(x)), x)
                i = int(b / 30 * 16000); n = min(len(x), len(out) - i); out[i:i + n] += x[:n]
            b += l['frames']
        a += s['frames']
    out = out[:16000 * 180]; db = voicenat.env_db(out); th = voicenat.thresh(db)
    runs = [r1 - r0 for r0, r1 in voicenat.quiet_runs(db, th, minrun=0.25)]; runs = runs[1:-1]
    return round(float(np.median(runs)), 2), round(sum(runs) / 180, 3)
for j in sys.argv[1:]: print(j, sim(j))
