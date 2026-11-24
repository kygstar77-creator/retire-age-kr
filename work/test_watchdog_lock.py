# watchdog.lock_alert 시험 — 2026-11-24 회의 지시: 'naverpost 잠금 나이 > 60분 = 경보'
#   py -3.12 work/test_watchdog_lock.py
import os, sys, time, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watchdog as W

d = tempfile.mkdtemp(); p = os.path.join(d, '.firemap.lock')
assert W.lock_alert(p) is None, '잠금 없음 → 경보 없음'
open(p, 'w', encoding='utf-8').write('297284')
now = time.time()
os.utime(p, (now - 59 * 60, now - 59 * 60))
assert W.lock_alert(p, now=now) is None, '59분 → 정상(jitter 52분 안쪽)'
os.utime(p, (now - 72 * 60, now - 72 * 60))   # 11/24 16:00 실제 72분 멈춤
m = W.lock_alert(p, now=now, alive=lambda pid: True)
assert m and '72분' in m and '297284' in m and '살아 있음' in m, m
m = W.lock_alert(p, now=now, alive=lambda pid: False)
assert '죽음' in m, m
os.remove(p); os.rmdir(d)
print('ok — 59분 조용·72분 경보·잠금 없음 조용')
