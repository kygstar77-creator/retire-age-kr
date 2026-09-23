# 발행 감시기 — 사장님 2026-09-23 18:30 "6시에도 블로그랑 카페 안 올라갔다. 검사도 자동으로 하고 있었던 거 아니야?"
#   py -3.12 work/watchdog.py            → 지금 상태를 재고, 빵꾸면 대기 묶음으로 즉시 메운다
#   py -3.12 work/watchdog.py --check    → 재기만 하고 발행은 안 한다
#
# 왜 필요한가(실제 사고):
#   1) firemap-write 예약이 '0 2-11'이라 새벽 2시~오전 11시만 돌았다. 오후·밤은 예약 자체가 없었다.
#      → 오후 내내 0편인데 아무도 몰랐다. 검사(health.py)가 루틴 안에서만 돌았기 때문이다.
#   2) 대기 묶음이 0이면 회차가 처음부터 글을 쓰다 40분 창을 넘겨 그냥 건너뛴다(16시·17시).
# 그래서 감시기는 루틴과 별개로 매시 돌면서, 사람이 보지 않아도 빵꾸를 메우고 기록을 남긴다.
import sys, os, re, json, time, subprocess
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
    rec = {'at': time.strftime('%Y-%m-%d %H:%M'), 'late': {}, 'stock': {}, 'did': [], 'alert': []}

    # 1) 언제 마지막으로 올라갔나 — 실제 네이버에서 잰다(우리 기록이 아니라)
    for kind in ('blog', 'cafe'):
        m = N.last_published_minutes(kind)
        rec['late'][kind] = None if m is None else round(m)
        if m is None: rec['alert'].append(f'{kind} 최근 발행 시각을 못 쟀다(RSS·API 실패)')
        elif m > LATE_MIN: rec['alert'].append(f'{kind} 마지막 발행이 {m/60:.1f}시간 전 — 회차를 놓쳤다')

    # 2) 미리 써 둔 묶음이 몇 개인가 — 0이면 다음 회차도 놓친다
    pend = N.list_pending()
    for kind in ('blog', 'cafe'):
        n = sum(1 for x in pend if x['kind'] == kind)
        rec['stock'][kind] = n
        if n < STOCK_WANT: rec['alert'].append(f'{kind} 대기 묶음 {n}개 (목표 {STOCK_WANT}) — 회차가 처음부터 쓰느라 밀린다')

    gaps = series_gap()
    rec['안 나간 시리즈'] = gaps
    if gaps: rec['alert'].append('최근 글에 한 편도 없는 시리즈: ' + ', '.join(gaps))

    # 3) 빵꾸 메우기 — 늦었고, 올릴 묶음이 있으면 지금 올린다
    need = [k for k in ('blog', 'cafe') if (rec['late'][k] or 0) > LATE_MIN and any(x['kind'] == k for x in pend)]
    if need and not check_only:
        # 잠금은 여기서 잡지 않는다. naverpost.py가 launch()에서 스스로 잡는다.
        # 감시기가 먼저 잡으면 제 자식을 막아 15분을 기다리다 실패한다(2026-09-23 18:49 실제 발생).
        for kind in need:
            pkg = next(x['pkg'] for x in pend if x['kind'] == kind)
            # 교차검증이 없는 묶음은 먼저 돌린다(회차 규칙 1): 2026-09-23 19:22 감시기가 paycalc를
            # 검증 전에 올려 Gemini 말투 수정을 못 받은 채로 나갔다. 실패해도 발행은 막지 않는다.
            if not os.path.exists(os.path.join(pkg, 'check_gemini.txt')) and not os.path.exists(os.path.join(pkg, 'check_gpt.txt')):
                try:
                    subprocess.run([sys.executable, os.path.join(HERE, 'crosscheck.py'), 'check', pkg],
                                   capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=300)
                    rec['did'].append(f'{kind} 올리기 전 교차검증 실행')
                except Exception as e:
                    rec['did'].append(f'{kind} 올리기 전 교차검증 실패(발행은 계속): {str(e)[:80]}')
            try:
                r = subprocess.run([sys.executable, os.path.join(HERE, 'naverpost.py'), kind, pkg],
                                   capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=1500)
                out = ((r.stdout or '') + (r.stderr or '')).strip()
            except Exception as e:
                rec['did'].append(f'{kind} 메우다 멈춤: {str(e)[:100]}'); continue
            u = re.search(r'URL (\S+)', out)
            if u: rec['did'].append(f'{kind} 빵꾸 메움 → {u.group(1)}')
            else: rec['did'].append(f'{kind} 메우기 실패: ' + (out.splitlines()[-1][:120] if out else '(출력 없음)'))
    elif need:
        rec['did'].append('--check 라서 올리지는 않았다: ' + ', '.join(need))
    elif rec['alert'] and not any(any(x['kind'] == k for x in pend) for k in ('blog', 'cafe')):
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
