# 롱폼 목소리 음높이 맞춤 시험 — 녹음은 됐는데 lfvoice check가 음높이(줄 ±25%·앞뒤 차 7%·퍼짐 0.16)로 막힐 때,
# 문장마다 f0를 편 목표 높이로 옮긴 사본을 따로 만든다(원본 audio/<편>은 그대로, 사본은 audio/<편>_pitch/).
#   py -3.12 work/lfpitch.py make <ep폴더> [--target 150] [--keep 0.06] [--cap 0.15] [--trim 0.1]   # 사본 + voice_pitch.json → 끝에 lfvoice check를 그 json으로 돌림
# 빠르기는 건드리지 않는다(rubberband pitch만, tempo 1.0 — RULES '빠르기 고정'). 포먼트 보존(formant=preserved)으로 목소리 결은 그대로 둔다.
# 목표 높이와 ±keep 안인 문장은 손대지 않는다(덜 건드릴수록 소리 손상이 적다). 공개에 쓸지는 들어 본 판단·순돌이 결정 몫 — 이 도구는 시험본만 만든다.
import sys, os, json, subprocess
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
import lfvoice as V

def trim(fn, pad=0.1):
    # 앞뒤 무음을 pad초만 남기고 자른다(10/3 N-1 손자르기 교훈: 편 전체 5.35→5.77) — 빠르기는 그대로, 문장 사이 쉼은 lfvoice GAP_F가 맡는다
    a, sr = V.read(fn); m, w = V.loud_mask(a, sr); i = np.where(m)[0]
    if len(i): V.write(fn, a[max(0, i[0] * w - int(pad * sr)):min(len(a), (i[-1] + 1) * w + int(pad * sr))], sr)

def make(ep, target=None, keep=0.06, cap=0.15, pad=None):
    d = json.load(open(os.path.join(ep, 'voice.json'), encoding='utf-8'))
    src = os.path.join(V.PUB, 'audio', os.path.basename(os.path.normpath(ep)).lower()); dst = src + '_pitch'; os.makedirs(dst, exist_ok=True)
    lines = [l for s in d['sections'] for l in s['lines'] if l.get('audio')]
    f = {l['audio']: V.f0(*V.read(os.path.join(V.PUB, l['audio']))) for l in lines}
    tgt = target or float(np.median([v for v in f.values() if v])); moved = 0; ratios = []; redo = []
    for l in lines:
        p = f[l['audio']]; fn = os.path.basename(l['audio']); out = os.path.join(dst, fn)
        r = tgt / p if p else 1.0
        if abs(r - 1) <= keep:
            a, sr = V.read(os.path.join(V.PUB, l['audio'])); V.write(out, a, sr)
        else:
            if abs(r - 1) > cap: redo.append(f"{p:.0f}Hz ×{r:.2f} | {l['text'][:30]}")
            r = min(1 + cap, max(1 / (1 + cap), r)); moved += 1; ratios.append(r)
            subprocess.run([V.ffmpeg(), '-y', '-loglevel', 'error', '-i', os.path.join(V.PUB, l['audio']),
                            '-af', f'rubberband=pitch={r:.4f}:formant=preserved:pitchq=quality:transients=smooth', '-ar', str(V.SR), '-ac', '1', out], check=True)
        if pad is not None: trim(out, pad)
        a2, sr2 = V.read(out); sec = len(a2) / sr2; l['sec'] = round(sec, 2); l['frames'] = int(sec * V.FPS + 0.999) + V.GAP_F
        l['audio'] = l['audio'].replace(os.path.basename(src) + '/', os.path.basename(dst) + '/'); l['pitch_ratio'] = round(r, 3)
    for s in d['sections']: s['frames'] = sum(l.get('frames', 0) for l in s['lines']) + (V.SEC_F if s['lines'] else 0)
    d['seconds'] = round(sum(s['frames'] for s in d['sections']) / V.FPS, 1)
    json.dump(d, open(os.path.join(ep, 'voice_pitch.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'목표 {tgt:.0f}Hz · 옮긴 문장 {moved}/{len(lines)} · 옮긴 비율 중앙 {np.median(ratios) if ratios else 1:.3f}(최소 {min(ratios, default=1):.3f}·최대 {max(ratios, default=1):.3f})')
    print(f'옮김 한도 ±{cap:.0%} 넘는 문장 {len(redo)} — 크게 옮기면 받아쓰기 일치가 떨어진다(10/5 시험: ×1.35에서 0.83→0.64), 이 문장들은 다시 녹음 몫', *redo, sep='\n  ')
    return V.check(ep, os.path.join(ep, 'voice_pitch.json'))

if __name__ == '__main__':
    a = sys.argv; ep = os.path.abspath(a[2])
    if a[1] == 'make':
        ok = make(ep, float(a[a.index('--target') + 1]) if '--target' in a else None, float(a[a.index('--keep') + 1]) if '--keep' in a else 0.06,
                  float(a[a.index('--cap') + 1]) if '--cap' in a else 0.15,
                  float(a[a.index('--trim') + 1]) if '--trim' in a else None)
        sys.exit(0 if ok else 1)
