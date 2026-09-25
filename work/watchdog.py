# 발행 감시기 — 사장님 2026-09-23 18:30 "6시에도 블로그랑 카페 안 올라갔다. 검사도 자동으로 하고 있었던 거 아니야?"
#   py -3.12 work/watchdog.py            → 지금 상태를 재고, 빵꾸면 대기 묶음으로 즉시 메운다
#   py -3.12 work/watchdog.py --check    → 재기만 하고 발행은 안 한다
#
# 왜 필요한가(실제 사고):
#   1) firemap-write 예약이 '0 2-11'이라 새벽 2시~오전 11시만 돌았다. 오후·밤은 예약 자체가 없었다.
#      → 오후 내내 0편인데 아무도 몰랐다. 검사(health.py)가 루틴 안에서만 돌았기 때문이다.
#   2) 대기 묶음이 0이면 회차가 처음부터 글을 쓰다 40분 창을 넘겨 그냥 건너뛴다(16시·17시).
# 그래서 감시기는 루틴과 별개로 매시 돌면서, 사람이 보지 않아도 빵꾸를 메우고 기록을 남긴다.
import sys, os, re, io, json, time, subprocess

def kill_tree(pid):
    """자식(크로미움)까지 끊는다. Popen.kill() 은 파이썬 하나만 죽여서 손자가 남는다."""
    try:
        subprocess.run(['taskkill', '/PID', str(pid), '/T', '/F'],
                       capture_output=True, timeout=60)
    except Exception:
        try: os.kill(pid, 9)
        except Exception: pass
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
LOG = os.path.join(HERE, 'watchdog_log.json')
LATE_MIN = 75          # 이 시간 넘게 안 올라갔으면 한 회차를 놓친 것으로 본다(정각 간격 60분 + 지터 여유)
STOCK_WANT = 3         # 매체별로 이만큼은 미리 써 둬야 회차가 안 밀린다

def load(p, d):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d


SERIES = {  # 시리즈가 실제로 발행됐는지 제목으로 확인한다
            # 2026-09-24: 여덟 개 중 일곱 개가 한 편도 안 나갔다. 도구는 다 있는데 편성이 없어 안 쓰였다.
    'B6 미국증시 한 장': r'미국증시|증시 한 장|섹터별',
    'B8 부동산 한 장': r'부동산 한 장|구별 전세가율',
    'B12/C8 배당 히트맵': r'히트맵',
    'C7 내부자 매수': r'내부자',
    'C4 주간 캘린더': r'이번 주.{0,6}캘린더|주간.{0,6}일정',
    'C6 유튜버 숫자 검증': r'유튜[브버].{0,10}(숫자|검증)',
    'B13 종목 발굴': r'발굴|조건에 걸린',
    'B11 손품': r'손품',
}

def series_gap():
    """며칠째 한 편도 안 나간 시리즈를 찾는다. 도구만 만들고 안 쓰는 일을 막는다."""
    import urllib.request
    UA2 = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cafe.naver.com/'}
    titles = []
    try:
        s = urllib.request.urlopen(urllib.request.Request(
            'https://rss.blog.naver.com/kygstar7777.xml', headers=UA2), timeout=20).read().decode('utf-8', 'ignore')
        titles += [re.sub(r'<!\[CDATA\[|\]\]>', '', m.group(1)).strip()
                   for m in re.finditer(r'<title>(.*?)</title>', s, re.S)][1:]
    except Exception:
        pass
    try:
        u = ('https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json'
             '?search.clubid=31789001&search.queryType=lastArticle&search.page=1&search.perPage=50')
        arts = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA2), timeout=20))
        titles += [a.get('subject', '') for a in arts['message']['result']['articleList']]
    except Exception:
        pass
    if not titles:
        return []
    return [n for n, pat in SERIES.items() if not any(re.search(pat, t) for t in titles)]

def main():
    import naverpost as N
    check_only = '--check' in sys.argv
    t0 = time.time()
    rec = {'at': time.strftime('%Y-%m-%d %H:%M'), 'late': {}, 'stock': {}, 'blocked': {}, 'did': [], 'alert': []}

    # 0) 쉬는 시간대인가. 사장님 2026-09-24 지시로 새벽 2~7시 발행을 뺐다(하루 24편 → 18편).
    # 여기서 안 막으면 감시기가 새벽마다 "빵꾸"로 보고 대신 메워 줄인 의미가 없어진다.
    # 네이버 공식이 어뷰징 오판 요인으로 든 "다량의 반복적 포스팅"을 줄이려는 것이 목적이다.
    hour = time.localtime().tm_hour
    quiet = 2 <= hour < 8
    rec['quiet'] = quiet
    if quiet: print(f'{hour}시 — 쉬는 시간대(2~7시)라 발행으로 메우지 않는다. 묶음 재고만 본다.')

    # 0-b) 오늘 상한을 이미 채운 매체인가. naverpost 는 하루 상한(카페 4편)을 넘으면 발행을 거부하는데
    # 감시기는 그걸 몰라 "빵꾸"로 보고 메우러 갔다. 2026-09-26 04:52 실측: 카페가 03:38에 4편째를
    # 올려 그날치가 끝났는데도 76분 빵꾸로 알리고 브라우저까지 띄웠다가 day_guard 에 거부당했다.
    # 그대로 두면 자정까지 매시 같은 헛발질을 한다. 상한에 닿은 매체는 알리지도, 메우지도 않는다.
    capped = {}
    for kind in ('blog', 'cafe'):
        cap = getattr(N, 'DAY_CAP', {}).get(kind)
        if cap is None: continue
        try: n = N.published_today(kind)
        except Exception: n = None
        if n is not None and n >= cap:
            capped[kind] = (n, cap)
            print(f'{kind} 오늘 {n}편 — 상한 {cap}편을 채웠다. 빵꾸로 보지 않고 메우지도 않는다.')
    rec['capped'] = {k: v[0] for k, v in capped.items()}

    # 1) 언제 마지막으로 올라갔나 — 실제 네이버에서 잰다(우리 기록이 아니라)
    for kind in ('blog', 'cafe'):
        m = N.last_published_minutes(kind)
        rec['late'][kind] = None if m is None else round(m)
        if m is None: rec['alert'].append(f'{kind} 최근 발행 시각을 못 쟀다(RSS·API 실패)')
        elif m > LATE_MIN and not (quiet and kind == 'blog') and kind not in capped:
            rec['alert'].append(f'{kind} 마지막 발행이 {m/60:.1f}시간 전 — 회차를 놓쳤다')

    # 2) 미리 써 둔 묶음이 몇 개인가 — 0이면 다음 회차도 놓친다
    pend = N.list_pending()
    # 막힌 묶음(같은 대상 이미 씀 등)은 올릴 수 없으니 재고로 세지 않는다.
    # 2026-09-25: 카페 2개로 보였는데 하나가 AVGO 중복이라 실제로 올릴 건 1개였다.
    for kind in ('blog', 'cafe'):
        mine = [x for x in pend if x['kind'] == kind]
        for x in mine:
            try: x['block'] = N.pending_block(x['kind'], x['pkg'], x['title'])
            except Exception: x['block'] = ''
        n = sum(1 for x in mine if not x['block'])
        blocked = len(mine) - n
        rec['stock'][kind] = n
        rec['blocked'][kind] = blocked
        if blocked: rec['alert'].append(f'{kind} 막힌 묶음 {blocked}개 — 올릴 수 없다(주제 겹침). 재고에서 뺐다')
        if n < STOCK_WANT: rec['alert'].append(f'{kind} 대기 묶음 {n}개 (목표 {STOCK_WANT}) — 회차가 처음부터 쓰느라 밀린다')

    # 2-b) 로그인이 살아 있나. 2026-09-25: 쿠키가 만료됐는데 아무도 못 알려
    # 카페가 10시간, 어제는 블로그가 2시간 멈췄다. 사장님이 물어서야 알았다.
    # 이건 사람 손이 필요한 유일한 항목이라 맨 앞에 알린다.
    try:
        import json as _j, time as _t
        st = os.path.join(os.path.dirname(N.PROFILE), os.path.basename(N.PROFILE), 'storage_state.json')
        if os.path.exists(st):
            age_h = (_t.time() - os.path.getmtime(st)) / 3600
            sess = sum(1 for c in _j.load(open(st, encoding='utf-8')).get('cookies', [])
                       if c['name'] in ('NID_AUT', 'NID_SES') and (c.get('expires') or -1) <= 0)
            rec['login_age_h'] = round(age_h, 1)
            if sess:
                rec['alert'].append(
                    f'로그인 쿠키가 세션형이라 곧 풀린다(저장 {age_h:.0f}시간 전) — '
                    '다음 로그인 때 "로그인 상태 유지"를 켜면 만료일이 붙어 오래 간다')
    except Exception as e: print('로그인 쿠키 점검 실패:', repr(e)[:80])

    gaps = series_gap()
    rec['안 나간 시리즈'] = gaps
    if gaps: rec['alert'].append('최근 글에 한 편도 없는 시리즈: ' + ', '.join(gaps))

    # 3) 빵꾸 메우기 — 늦었고, 올릴 묶음이 있으면 지금 올린다
    # 쉬는 시간대(2~7시)에 쉬는 것은 **블로그뿐**이다. 카페는 24시간 간다
    # (2026-09-25 사장님 "카페는 그대로 24시간 아니었어?" — 카페는 색인이 정상이라 줄일 이유가 없다).
    kinds = ['cafe'] if quiet else ['blog', 'cafe']
    kinds = [k for k in kinds if k not in capped]
    # 막힌 묶음은 메우기 대상이 아니다. 2026-09-26 00:52 실측: 카페가 89분 빵꾸인데
    # 첫 묶음(avgo0925)이 AVGO 중복으로 막혀 있어 naverpost 가 거부했고, 뒤에 있던
    # 멀쩡한 cvx0926·pg0926 은 손도 못 댔다. 재고에서는 빼면서 메울 때는 첫 개를
    # 그냥 집던 탓이다.
    okpend = [x for x in pend if not x.get('block')]
    need = [k for k in kinds
            if (rec['late'][k] or 0) > LATE_MIN and any(x['kind'] == k for x in okpend)]
    if need and not check_only:
        # 잠금은 여기서 잡지 않는다. naverpost.py가 launch()에서 스스로 잡는다.
        # 감시기가 먼저 잡으면 제 자식을 막아 15분을 기다리다 실패한다(2026-09-23 18:49 실제 발생).
        for kind in need:
            # 메우기 직전에 한 번 더 잰다. 2026-09-26 00:52 실측: 카페 89분 빵꾸로 판정한 뒤
            # 교차검증·발행에 23분이 걸렸고 그 사이 00시 write 회차가 01:10에 먼저 올렸다.
            # 내 메우기는 5분 뒤 겹쳐 그 시간에 카페 글이 두 편 나갔다.
            m2 = None
            try: m2 = N.last_published_minutes(kind)
            except Exception: pass
            if m2 is not None and m2 <= LATE_MIN:
                rec['did'].append(f'{kind} 메우기 취소 — 다시 재니 {round(m2)}분 전에 올라가 있다(다른 회차가 먼저 채웠다)')
                continue
            pkg = next(x['pkg'] for x in okpend if x['kind'] == kind)
            # 교차검증이 없는 묶음은 먼저 돌린다(회차 규칙 1): 2026-09-23 19:22 감시기가 paycalc를
            # 검증 전에 올려 Gemini 말투 수정을 못 받은 채로 나갔다. 실패해도 발행은 막지 않는다.
            if not os.path.exists(os.path.join(pkg, 'check_gemini.txt')) and not os.path.exists(os.path.join(pkg, 'check_gpt.txt')):
                try:
                    subprocess.run([sys.executable, os.path.join(HERE, 'crosscheck.py'), 'check', pkg],
                                   capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=300)
                    rec['did'].append(f'{kind} 올리기 전 교차검증 실행')
                except Exception as e:
                    rec['did'].append(f'{kind} 올리기 전 교차검증 실패(발행은 계속): {str(e)[:80]}')
            # 파이프로 받지 않고 파일로 받는다. 2026-09-25 05:52·08:12·(그 전 08:30 회차가 기록)
            # 두 번 다 감시기가 메우기 실패 뒤 영영 안 끝나 빵꾸를 아무에게도 못 알렸다.
            # 원인: capture_output 파이프를 naverpost.py 의 손자(크로미움)까지 물려받아,
            # timeout 으로 naverpost.py 만 죽여도 파이프가 안 닫혀 communicate() 가 무한 대기한다.
            # 파일로 받으면 파이프가 없어 timeout 이 제때 돌아오고, 자식 트리는 taskkill 로 정리한다.
            out = ''
            logf = os.path.join(HERE, 'research', f'_fill_{kind}.log')
            try:
                with open(logf, 'w', encoding='utf-8') as fh:
                    pr = subprocess.Popen([sys.executable, os.path.join(HERE, 'naverpost.py'), kind, pkg],
                                          stdout=fh, stderr=subprocess.STDOUT)
                    try:
                        pr.wait(timeout=1500)
                    except subprocess.TimeoutExpired:
                        kill_tree(pr.pid)
                        rec['did'].append(f'{kind} 메우기 25분 초과 — 자식까지 끊었다')
                out = io.open(logf, encoding='utf-8', errors='ignore').read().strip()
            except Exception as e:
                rec['did'].append(f'{kind} 메우다 멈춤: {str(e)[:100]}'); continue
            u = re.search(r'URL (\S+)', out)
            if u: rec['did'].append(f'{kind} 빵꾸 메움 → {u.group(1)}')
            else: rec['did'].append(f'{kind} 메우기 실패: ' + (out.splitlines()[-1][:120] if out else '(출력 없음)'))
    elif need:
        rec['did'].append('--check 라서 올리지는 않았다: ' + ', '.join(need))
    elif rec['alert'] and not any(any(x['kind'] == k for x in okpend) for k in ('blog', 'cafe')):
        rec['did'].append('메울 묶음이 하나도 없다 — 회차 루틴이 새로 써야 한다')

    rec['sec'] = int(time.time() - t0)
    log = load(LOG, []) or []; log.append(rec)
    json.dump(log[-400:], open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    print(f"[감시 {rec['at']}] 블로그 {rec['late']['blog']}분 전 / 카페 {rec['late']['cafe']}분 전 · 대기 블로그 {rec['stock']['blog']} 카페 {rec['stock']['cafe']}")
    for a in rec['alert']: print('  ! ' + a)
    for d in rec['did']: print('  → ' + d)
    if not rec['alert']: print('  이상 없음')
    sys.exit(1 if rec['alert'] else 0)

if __name__ == '__main__': main()
