# H-2 걸린 줄: 다시 받기(retake 1) → 그 줄 readback(첫 귀 FIRST·둘째 귀 turbo) → 표시 없으면 멈춤, 최대 4번
import sys, os, json, io, contextlib
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import lfvoice, cloudtts
lfvoice.WHISPER_SIZE, lfvoice.WHISPER = 'large-v3-turbo', 'whisper-turbo'
lfvoice.SECOND[:] = []          # 제미나이 둘째 귀(3.5-flash·flash-latest)는 오늘 한도 — 바로 turbo
ep = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\longform\ep\H-2'
rj = os.path.join(ep, 'check', 'voice_readback.json')
ats = sys.argv[1].split(',')
log = []
for at in ats:
    for k in range(4):
        lfvoice.retake(ep, [at], 1)
        lfvoice.readback(ep, [at])
        r = {x['at']: x for x in json.load(open(rj, encoding='utf-8'))}[at]
        print("@@", at, k + 1, r['models'], '|', r['flag'] or '통과', '|', (r['heard'][1] or '')[:50], flush=True)
        log.append({'at': at, 'try': k + 1, 'flag': r['flag'], 'heard': r['heard'], 'models': r['models']})
        if not r['flag']: break
json.dump(log, open(os.path.join(ep, 'check', 'retake_loop_1019.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
