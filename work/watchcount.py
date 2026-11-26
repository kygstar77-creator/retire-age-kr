# 감시 세기 — firemap-watchdog 회차가 매번 손으로 세던 것을 코드가 센다.
#   사장님 2026-11-26 "품질 그대로, 읽는 양만 줄이기".
#   py -3.12 work/watchcount.py                          → 지금 상태를 센다
#   py -3.12 work/watchcount.py --replay "2026-11-26 09:54"  → watchdog_log.json의 그 회차 기록으로 다시 센다(대조용)
#
# 하는 일(전부 이미 있는 코드를 부른다 — 기준 값을 새로 짓지 않는다):
#   ① 빵꾸·재고·잠금·사이트·전원·쿠키: `watchdog.py --check`(발행 안 함)를 돌리고 그 기록(watchdog_log.json 마지막 줄)을 읽는다.
#      빵꾸 판정 = watchdog.cafe_late(E-21, 칸+50분) · 재고 목표 = slots.json reserve_min · 잠금 경보 = 60분(LOCK_ALERT_MIN).
#   ② 칸: 마지막 카페 글이 어느 칸 뒤인지, 다음 칸(slots.json cadence)의 장부 item이 대기열(`naverpost.py pending`)에
#      slot.txt 같은 시각으로 걸려 있는지 — 회차가 '[감시]' 줄에 적던 "다음 10:10 칸 X가 대기열에 '10시'로 걸려 있음".
#   ③ 멈춘 회차: beat.py의 stuck()·stale()·abandoned()·cut_off() (= `beat.py list`가 찍는 것).
#   ④ today.md에서 담당이 watchdog인 [지시]·[요청] 중 '완료' 없는 줄.
# 읽기·세기만 한다: 발행·삭제·메시지 보내기 없음. watchdog.py --check는 원래대로 watchdog_log.json에 한 줄을 더한다(계기판이 읽음).
# 로그인(naverpost.py check)은 여기서 돌리지 않는다 — 브라우저 잠금을 잡고, 실패하면 텔레그램을 보내기 때문이다(회차가 따로 돌린다).
# 마지막 줄: 'STATUS: OK' 또는 'STATUS: 이상 — <무엇>'.
import sys, os, re, json, time, datetime as dt, subprocess
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
sys.path.insert(0, HERE)
import watchdog as W, beat as B

SERIES_KEY = '최근 글에 한 편도 없는 시리즈'   # 감시 네 가지(빵꾸·재고·멈춘 회차·로그인) 밖 — 참고로만 찍는다


def run_check():
    """watchdog.py --check를 돌리고 이번에 더해진 기록을 돌려준다."""
    t0 = time.strftime('%Y-%m-%d %H:%M')
    out = subprocess.run([sys.executable, os.path.join(HERE, 'watchdog.py'), '--check'], capture_output=True,
                         text=True, encoding='utf-8', errors='ignore', timeout=600,
                         env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout or ''
    log = W.load(W.LOG, []) or []
    rec = log[-1] if log and log[-1].get('at', '') >= t0 else None
    return rec, out


def pending_rows():
    try:
        out = subprocess.run([sys.executable, os.path.join(HERE, 'naverpost.py'), 'pending'], capture_output=True,
                             text=True, encoding='utf-8', errors='ignore', timeout=300,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout or ''
        return [json.loads(l) for l in out.splitlines() if l.startswith('{')]
    except Exception:
        return None


def name_of(pkg):
    p = os.path.normpath(str(pkg))
    return os.path.basename(os.path.dirname(p)) if os.path.basename(p) == 'pkg' else os.path.basename(p)


def slot_txt(pkg):
    try: return open(os.path.join(pkg, 'slot.txt'), encoding='utf-8').read().strip()[:13]
    except Exception: return None


def cafe_slots(now):
    """cadence 칸 시각을 어제·오늘·내일 날짜로 펼친다."""
    cad = sorted((W._slots().get('cadence') or {}).get('cafe') or [])
    ts = []
    for k in (-1, 0, 1):
        day = (now + dt.timedelta(days=k)).date()
        ts += [dt.datetime.combine(day, dt.time(int(x[:2]), int(x[3:5]))) for x in cad]
    return sorted(ts)


def ledger(at, kind='cafe'):
    key = at.strftime('%Y-%m-%d %H:%M')
    for x in W._slots().get('slots', []):
        if x.get('at') == key and x.get('kind') == kind and not x.get('skip'): return x
    return None


ME = ('watchdog', '감시기')
DONE = re.compile(r'완료\s*[:：]')
REPEAT = re.compile(r'매 ?회차|회차마다|매일|매번')


def open_orders():
    """today.md에서 담당이 감시기인 [지시]·[지시·긴급]·[요청]·[알림] 중 아래 줄에 내 '완료:'가 없는 것 (줄번호, 앞 90자).
    넉넉히 잡는다(놓치는 것보다 한 줄 더 읽는 게 낫다): 담당 칸은 '←' 앞, '←'가 없으면 앞 200자.
    '매 회차·매일' 같은 반복 지시는 완료 줄이 있어도 늘 연다(10/11~21 사이트 4쪽 확인이 그랬다)."""
    try: lines = open(os.path.join(R, 'meeting', 'today.md'), encoding='utf-8').read().splitlines()
    except Exception: return None
    out = []
    for i, ln in enumerate(lines):
        if not re.match(r'\s*-\s*\[(지시|지시·긴급|요청|알림)', ln): continue
        who = ln.split('←')[0] if '←' in ln else ln[:200]
        if not any(w in who for w in ME): continue
        ind = len(ln) - len(ln.lstrip())
        done = False
        for nx in lines[i + 1:]:
            if not nx.strip(): continue
            if len(nx) - len(nx.lstrip()) <= ind: break
            if DONE.search(nx) and (any(w in nx for w in ME) or 'firemap-' not in nx): done = True; break
        rep = bool(REPEAT.search(ln))
        if rep or not done: out.append((i + 1, ('(반복) ' if rep else '') + ln.strip()[:90]))
    return out


def main():
    replay = sys.argv[sys.argv.index('--replay') + 1] if '--replay' in sys.argv else None
    bad, info = [], []
    if replay:
        rec = next((x for x in reversed(W.load(W.LOG, []) or []) if x.get('at') == replay), None)
        if not rec: print(f'watchdog_log.json에 {replay} 기록 없음'); print('STATUS: 이상 — 대조할 기록 없음'); return
        now = dt.datetime.strptime(replay, '%Y-%m-%d %H:%M'); raw = ''
    else:
        rec, raw = run_check(); now = dt.datetime.now()
        if not rec:
            print('watchdog.py --check 기록이 안 남았다. 출력 끝:'); print('\n'.join(raw.strip().splitlines()[-6:]))
            print('STATUS: 이상 — watchdog.py --check 실패'); return
    late, stock = rec.get('late') or {}, rec.get('stock') or {}
    stopped = {k for k in ('blog', 'cafe') if any(n.startswith(f'{k} 정지 중') for n in rec.get('note', []))}
    print(f"[감시 세기 {rec['at']}{' · 다시 셈' if replay else ''}] (watchdog.py --check 기록 기준)")

    # ① 마지막 발행 + 칸
    pend = None if replay else pending_rows()
    m = late.get('cafe')
    if m is None:
        cafe_txt = '카페 최근 발행 못 잼'
    else:
        last = now - dt.timedelta(minutes=m)
        ts = cafe_slots(now)
        after = max([t for t in ts if t <= last], default=None)
        nxt = min([t for t in ts if t > now], default=None)
        islate = bool((rec.get('islate') or {}).get('cafe'))
        cafe_txt = f"카페 {m}분 전({after.strftime('%H:%M') + ' 칸 뒤' if after else '칸 앞'}"
        if nxt:
            lg = ledger(nxt); item = (lg or {}).get('item') or ''
            nm = (re.match(r'[A-Za-z0-9_\-]+', item) or [None])[0] if item and not item.startswith('TBD') else None
            row = next((x for x in (pend or []) if name_of(x['pkg']) == nm), None) if nm else None
            want = nxt.strftime('%Y-%m-%d %H')
            if not lg: nx = '장부 칸 없음'; bad.append(f"다음 칸 {nxt.strftime('%m-%d %H:%M')} 장부에 없음")
            elif not nm: nx = f'장부 {item[:20]}'; bad.append(f"다음 칸 {nxt.strftime('%H:%M')} 배정 안 됨({item[:20]})")
            elif replay:   # 장부 published·대기열은 지금 것이라 보지 않고 slot.txt만 본다
                st = slot_txt(os.path.join(R, nm, 'pkg'))
                nx = f"{nm} slot.txt '{st[11:]}시'" + (' (칸과 같음)' if st == want else f' ≠ 칸 {want}') if st else f'{nm} slot.txt 없음'
            elif lg.get('published'): nx = f'{nm} 이미 발행'
            elif pend is None: nx = f'{nm} — 대기열 못 읽음'; bad.append('naverpost.py pending 실패')
            elif not row: nx = f'{nm} 대기열에 없음'; bad.append(f"다음 칸 {nxt.strftime('%H:%M')} {nm}이 대기열에 없음")
            else:
                st = slot_txt(row['pkg'])
                if st == want: nx = f"{nm}이 대기열에 '{st[11:]}시'로 걸려 있음"
                else:
                    nx = f"{nm} 대기열 있음, slot.txt {st or '없음'} ≠ 칸 {want}"; bad.append(f"다음 칸 {nm} slot.txt 시각 다름")
            cafe_txt += f", 다음 {nxt.strftime('%H:%M')} 칸 {nx}"
        cafe_txt += ' → 빵꾸' if islate else ' → 빵꾸 아님'
        cafe_txt += ')'
        if islate: bad.append(f'카페 빵꾸 {m}분')
    if 'cafe' in stopped: cafe_txt = '카페 정지'
    blog_txt = '블로그 정지' if 'blog' in stopped else f"블로그 {late.get('blog')}분 전" + (' → 빵꾸' if (rec.get('islate') or {}).get('blog') else '')
    if 'blog' not in stopped and (rec.get('islate') or {}).get('blog'): bad.append('블로그 빵꾸')
    print('· ' + cafe_txt); print('· ' + blog_txt)

    # ② 재고
    stock_txt = []
    for k, nm in (('cafe', '카페'), ('blog', '블로그')):
        if k in stopped: continue
        cb, hd, bl = (rec.get('capblocked') or {}).get(k, 0), (rec.get('held') or {}).get(k, 0), (rec.get('blocked') or {}).get(k, 0)
        want = W.stock_want(k)
        stock_txt.append(f"대기 {nm} {stock.get(k)}(시각 대기 {cb}, 보류 {hd} 제외" + (f', 새로 막힘 {bl - hd}' if bl - hd else '') + f') 목표 {want}')
    print('· ' + ' · '.join(stock_txt))

    # ③ 잠금·멈춘 회차
    lm = rec.get('lock_min')
    lock_txt = 'naverpost 잠금 없음' if lm is None else f'naverpost 잠금 {lm}분째(경보 {W.LOCK_ALERT_MIN}분)'
    if replay:
        beat_txt = '멈춘 회차: 다시 셈에서는 안 봄(맥박은 지금 것)'
    else:
        nowt = time.time(); d = B.load()
        st = B.stuck(nowt); sl = B.stale(nowt)
        cut = [t for t in sorted(B.tasks(d)) if B.cut_off(t, nowt, d)]
        ab = [g for g in B.abandoned(24, nowt)
              if not ((d.get(g['task']) or {}).get('end') and (d.get(g['task']) or {}).get('at', '') > (g.get('at') or ''))]
        beat_txt = f'멈춘 회차 {len(st)}' + (' — ' + ', '.join(f'{t}({mm}분/예산 {b}, 단계 {(d.get(t) or {}).get("stage", "-")})' for t, mm, b in st) if st else '')
        if cut: beat_txt += f" · 기계 꺼짐 잔재 {', '.join(cut)}"
        if sl: beat_txt += ' · 예약 간격 넘김 ' + ', '.join(f'{t}({h}시간/정상 {g})' for t, h, g in sl); bad.append('예약 간격 넘긴 회차 ' + ', '.join(t for t, _, _ in sl))
        if ab: beat_txt += ' · 끝 못 찍고 죽음(뒤 회차 없음) ' + ', '.join(f"{g['task']} {g['at']}" for g in ab); bad.append('죽은 회차 ' + ', '.join(g['task'] for g in ab))
        if st: bad.append('멈춘 회차 ' + ', '.join(t for t, _, _ in st))
    print('· ' + lock_txt + ' · ' + beat_txt)

    # ④ watchdog.py 경보(빵꾸·재고는 위에서 셈) — 나머지는 그대로 이상으로 올린다
    did = rec.get('did') or []
    filled = sum(1 for x in did if '빵꾸 메움' in x)
    for a in rec.get('alert', []):
        if a.startswith(SERIES_KEY): info.append('참고(감시 4가지 밖, 매 회차 같음): ' + a[:70] + ('…' if len(a) > 70 else '')); continue
        if '회차를 놓쳤다' in a: continue                # 빵꾸는 ①에서 셈
        if '대기 묶음' in a and '목표' in a: bad.append(a.split(' — ')[0]); continue
        bad.append(a[:110])
    for n in rec.get('note', []):
        if n.startswith('최근 비정상 종료'): info.append(n)
    if rec.get('site') and rec['site'] != 'ok': pass   # 사이트 이상은 alert에 이미 있다
    info.append(f"전원 {'배터리 ' + str((rec.get('power') or {}).get('pct')) + '%' if (rec.get('power') or {}).get('on_battery') else '충전기'} · 사이트 {'정상' if rec.get('site') == 'ok' else rec.get('site')} · 감시기 발행 {filled}")
    for x in info: print('· ' + x)

    # ⑤ today.md 담당 지시
    oo = None if replay else open_orders()
    if oo is None and not replay: print('· today.md 못 읽음'); bad.append('today.md 못 읽음')
    elif oo: print(f'· today.md 내 담당 열린 지시 {len(oo)}건: ' + ' / '.join(f'{n}행 {t}' for n, t in oo)); bad.append(f'열린 지시 {len(oo)}건')
    elif not replay: print('· today.md 내 담당 열린 지시 0')

    # 기록용 한 줄(회차가 [감시] 줄로 옮긴다 — 시각은 date로 찍은 값을 앞에 붙인다)
    stopped_txt = ' · '.join(([blog_txt] if 'blog' in stopped else []))
    print('기록용: ' + cafe_txt + '·' + ' · '.join(stock_txt) + (f'·{stopped_txt}' if stopped_txt else '')
          + f' · {lock_txt} · ' + beat_txt.split(' · 예약')[0] + f' · 감시기 발행 {filled} · 로그인: naverpost.py check 결과를 붙인다')
    print('STATUS: OK' if not bad else 'STATUS: 이상 — ' + ' / '.join(dict.fromkeys(bad)))


if __name__ == '__main__': main()
