# M-1 쇼츠에 쓴 문장 wav를 하나씩 받아써서 voice.json 글(자막)과 맞는지 본다 (10/11 발견: 줄 28 wav 앞에 줄 27 끝 '선을 넘어요.'가 붙어 있음 —
# 롱폼에서는 27→28이 이어져 티가 안 났지만, 쇼츠에서 줄을 옮기면 말과 자막이 어긋난다).
#   py -3.12 work/research/cardshorts/m1clips_hear.py <props json …>     # → cardshorts/hear_<날짜>.json 에 줄마다 받아쓰기 저장(이미 들은 wav는 다시 안 들음)
import os, sys, json, wave, re, time, difflib, datetime
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE); sys.path.insert(0, WORK)
import m1clips_trim as T
CACHE = os.path.join(HERE, 'm1clips_hear.json')
norm = lambda s: re.sub(r'[^가-힣A-Za-z0-9]', '', s.replace('만 원', '만원'))

if __name__ == '__main__':
    cache = json.load(open(CACHE, encoding='utf-8')) if os.path.exists(CACHE) else {}
    bad = []
    for pf in sys.argv[1:]:
        p = json.load(open(pf, encoding='utf-8'))
        for s in p['scenes']:
            for l in s['lines']:
                a = l['audio']
                if a not in cache:
                    with wave.open(os.path.join(WORK, 'video', 'public', a)) as w: sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
                    for _ in range(3):
                        m, t = T.hear(x, sr)
                        if t: break
                        time.sleep(20)
                    cache[a] = {'heard': t, 'model': m, 'at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
                    json.dump(cache, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
                h = cache[a]['heard'] or ''
                r = difflib.SequenceMatcher(None, norm(l['text']), norm(h)).ratio()
                flag = 'OK ' if r >= 0.85 else '?? '
                if r < 0.85: bad.append((p['name'], l['n'], l['text'], h))
                print(f"{flag}{r:.2f} {p['name']} 줄{l['n']} | 글: {l['text']} | 들림: {h}")
    print('어긋남', len(bad))
