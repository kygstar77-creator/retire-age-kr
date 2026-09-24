# 계기판 — 파이어맵 전 영역을 한 자로 재고, 목표 대비 부족분(gap)을 순위로 낸다.
#   py -3.12 work/health.py            → 화면 출력 + work/health.json
# selfloop.py가 이걸 읽어 "이번 회차에 무엇을 고칠지"를 정한다. 사람이 고르지 않는다.
# 각 항목: value(실측) / target(목표) / weight(중요도) / how(못 미치면 무엇을 봐야 하는지)
import sys, os, re, json, glob, time, subprocess, statistics, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cafe.naver.com/'}

def load(p, d=None):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d

def sh(*a, timeout=900):
    try:
        r = subprocess.run([sys.executable] + list(a), capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=timeout, cwd=os.path.dirname(HERE))
        return (r.stdout or '') + (r.stderr or '')
    except Exception as e: return 'ERR ' + str(e)[:80]

def rss_today():
    try:
        s = urllib.request.urlopen(urllib.request.Request('https://rss.blog.naver.com/kygstar7777.xml', headers=UA), timeout=20).read().decode('utf-8', 'ignore')
        return len([d for d in re.findall(r'<pubDate>(.*?)</pubDate>', s) if time.strftime('%d %b %Y') in d])
    except Exception: return None

def cafe_today():
    try:
        u = 'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid=31789001&search.queryType=lastArticle&search.page=1&search.perPage=50'
        arts = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20))['message']['result']['articleList']
        today = time.strftime('%Y-%m-%d')
        n = sum(1 for a in arts if time.strftime('%Y-%m-%d', time.localtime(a['writeDateTimestamp'] / 1000)) == today)
        reads = [a.get('readCount', 0) for a in arts[:20]]
        return n, (statistics.median(reads) if reads else 0)
    except Exception: return None, None

def main():
    M = []   # (영역, 항목, 값, 목표, 중요도, 어떻게 고치나)
    runs = load(os.path.join(HERE, 'runs_today.json'), {'runs': []})['runs']
    nb = sum(1 for r in runs if (r.get('blog') or {}).get('url')); nc = sum(1 for r in runs if (r.get('cafe') or {}).get('url'))
    # 발행 의무가 있는 회차만 센다. 감시기(:45)·보고 회차도 같은 파일에 append하는데
    # 그 회차는 발행이 일이 아니라서, 예전엔 2026-09-24 03시처럼 발행 3회차가 전부 2편씩
    # 나갔는데도 '0편 회차 3'으로 잡혀 일감표 1번을 계속 차지했다.
    def 발행회차(r):
        if r.get('role') in ('watchdog', 'report', 'improve'): return False
        return not re.match(r'\s*(감시기? 회차|보고 회차|자가발전 회차)', r.get('note') or '')
    zero = sum(1 for r in runs if 발행회차(r)
               and not (r.get('blog') or {}).get('url') and not (r.get('cafe') or {}).get('url'))
    M += [('발행', '오늘 블로그 편수', nb, 24, 3, 'firemap-write 회차 note에서 0편 사유 확인 → 대기 묶음·가드·시간초과'),
          ('발행', '오늘 카페 편수', nc, 24, 3, '위와 같음'),
          ('발행', '0편 회차 수', zero, 0, 3, '0편 사유를 없앤다(대기 묶음 3+3 유지가 가장 흔한 원인)')]
    pend = sh(os.path.join(HERE, 'naverpost.py'), 'pending')
    pb = len(re.findall(r'"kind": "blog"', pend)); pc = len(re.findall(r'"kind": "cafe"', pend))
    M += [('발행', '대기 묶음 블로그', pb, 3, 3, 'firemap-improve B/F 회차가 완성 묶음을 만든다'),
          ('발행', '대기 묶음 카페', pc, 3, 3, '위와 같음')]

    # 빵꾸 감시 — 2026-09-23 오후 내내 0편이었는데 아무도 몰랐다(예약이 오전까지만 있었다).
    # 회차 기록이 아니라 실제 네이버에서 잰다. 1이면 한 회차를 놓친 것.
    try:
        sys.path.insert(0, HERE); import naverpost as _np
        for kind, ko in (('blog', '블로그'), ('cafe', '카페')):
            mm = _np.last_published_minutes(kind)
            if mm is not None:
                M.append(('발행', f'{ko} 발행 빵꾸(75분 초과)', 1 if mm > 75 else 0, 0, 3,
                          f'지금 {mm/60:.1f}시간 전이 마지막. py -3.12 work/watchdog.py 로 즉시 메운다'))
    except Exception as e: print('빵꾸 측정 실패:', str(e)[:60])

    # 글 자가발전 — 규칙표가 낡으면 회차가 옛 규칙으로 쓴다
    tr = load(os.path.join(HERE, 'textrule.json'), {})
    if tr:
        try: old_h = (time.time() - time.mktime(time.strptime(tr['at'], '%Y-%m-%d %H:%M'))) / 3600
        except Exception: old_h = 99
        M.append(('품질', '글 규칙 낡음(12시간 초과)', 1 if old_h > 12 else 0, 0, 2, 'py -3.12 work/textloop.py 로 성과→규칙을 다시 뽑는다'))
        M.append(('품질', '카페 하루당 조회 중앙값', tr.get('cafe_median_per_day') or 0, 5, 2,
                  'work/research/textrule.md의 규칙을 회차가 실제로 따르는지 확인'))

    pkgs = [p for p in glob.glob(os.path.join(R, '*', 'pkg')) if os.path.exists(os.path.join(p, 'published.txt'))]
    recent = sorted(pkgs, key=lambda p: -os.path.getmtime(os.path.join(p, 'published.txt')))[:20]
    ver = [load(os.path.join(p, 'verify.txt'), {}) for p in recent]
    okv = sum(1 for v in ver if v and v.get('ok'))
    # 2026-09-24: 검증 비율이 check_gpt.txt만 세는 바람에 제미나이 무료 할당량(429)이 차는 날은
    # 모든 묶음이 selfcheck로 제대로 검증됐는데도 0.0으로 찍혔다. 그러면 일감표 맨 위에 영영 남고
    # 회차가 닫을 수 없는 항목이 된다. 사장님 지시(2026-09-23)대로 selfcheck도 검증으로 센다.
    # 다만 바깥 모델을 못 쓴 사실은 따로 보이게 남긴다 — 429가 숨지 않도록.
    def _has(p, *names): return any(os.path.exists(os.path.join(p, n)) for n in names)
    cc = sum(1 for p in recent if _has(p, 'check_gpt.txt', 'check_gemini.txt', 'check_self.txt'))
    ext = sum(1 for p in recent if _has(p, 'check_gpt.txt', 'check_gemini.txt'))
    M += [('품질', '최근 20편 실물검증 통과율', round(okv / max(1, len(recent)), 3), 0.95, 3, 'naverpost verify BAD → rewrite'),
          ('품질', '최근 20편 검증 비율(교차 또는 자체)', round(cc / max(1, len(recent)), 3), 1.0, 3, '검증 없이 발행한 회차 확인 → crosscheck 실패 시 selfcheck 필수'),
          ('품질', '최근 20편 바깥모델 교차검증 비율', round(ext / max(1, len(recent)), 3), 1.0, 1, '제미나이 429면 selfcheck로 대체됨 — 유료 키가 생기면 올라간다')]

    perf = load(os.path.join(HERE, 'perf_log.json'), {})
    if perf:
        last = perf[sorted(perf)[-1]]; b = last.get('blog', [])
        # 색인율은 '하루 지난 글'로 잰다. 그날 발행분을 그날 재면 색인될 시간이 없어 언제나 낮다
        # (2026-09-24: 당일 글 0% · 같은 측정에서 어제 글 80%). mature가 없으면 당일 값으로 두되 목표를 낮춘다.
        mt = last.get('mature')
        if mt:
            M.append(('검색', '색인율(하루 지난 글)', mt['rate'], 0.8, 3,
                      f"{mt['n']}편 중 {mt['indexed']}편 · 색인 안 된 글의 본문 문장 검색 → 유사문서·품질 확인"))
        if b:
            M += [('검색', '색인율(당일 글 — 참고용)', round(sum(1 for x in b if x.get('indexed')) / len(b), 3), 0.3, 1, '색인은 하루쯤 걸린다. 이 값이 낮은 것만으로 발행량을 줄이지 않는다'),
                  ('검색', '제목검색 10위 안 비율', round(sum(1 for x in b if (x.get('self_rank') or 99) <= 10) / len(b), 3), 0.6, 2, '제목 규칙(series-plan)·toprank 항목 채우기')]
    vis = load(os.path.join(HERE, 'visitors_log.json'), {})
    if vis:
        days = sorted(vis); today_v = vis[days[-1]]['today']
        M.append(('성장', '블로그 오늘 방문', today_v, 100, 3, '색인·순위가 먼저. 발행량만 늘리면 안 오른다'))
    ncafe, medread = cafe_today()
    if medread is not None: M.append(('성장', '카페 최근 20편 조회 중앙값', medread, 50, 2, '카페 축(커버드콜·배당·파이어 금액)·제목·회원 상호작용'))

    yt = sh(os.path.join(HERE, 'ytupload.py'), 'stats')
    vids = [int(v) for v in re.findall(r'\d{4}-\d{2}-\d{2}\s+(\d+)\s*회', yt)]
    # 2026-09-24: '최근 10편 조회 합계'는 새 영상을 올릴 때마다 떨어진다(새 영상은 조회 0이라
    # 조회가 쌓인 옛 영상을 10편 밖으로 밀어낸다). 실측 2089 -> 120 -> 6. 발행을 잘할수록 계기판이
    # 나빠지는 셈이라 채널 총조회(누적, 절대 안 줄어든다)로 바꿨다. loop.py 의 회차 판정도 같이 고쳤다.
    m_tot = re.search(r'총조회\s*(\d+)', yt)
    if m_tot: M.append(('영상', '채널 총조회(누적)', int(m_tot.group(1)), 50000, 2, '제목 규칙·썸네일 손잡이(design.json)·루프'))
    pub = len(re.findall(r'\|\s*public\s*\|', yt))
    M.append(('영상', '공개한 영상 수(최근 10편 중)', pub, 10, 2, '지금은 전부 private — 비공개면 조회가 영영 0이라 조정 효과를 잴 수 없다'))
    M.append(('영상', '올린 숏폼 수', len(glob.glob(os.path.join(R, 'shorts', '*.mp4'))), 10, 2, 'firemap-loop 6)에서 회차마다 한 편'))

    # 2026-09-24: 이 숫자가 2에서 멈춰 있었는데 그 2는 short.white·short.contrast 였다.
    # 둘 다 "더 밀면 글자가 죽는다"고 화면으로 확인해 한계를 박아 둔 자리다(loop.py CAPPED).
    # 풀지 않기로 한 것을 '미해결'로 세니 회차마다 끝난 판단을 다시 뒤지게 됐다. 갈라 센다.
    llog = load(os.path.join(HERE, 'loop_log.json'), [])
    last = llog[-1] if llog else {}
    gaps = last.get('gaps', [])
    capped = set(last.get('capped') or [])
    open_gaps = [g for g in gaps if f"{g.get('kind')}.{g.get('key')}" not in capped]
    M.append(('디자인', '경쟁 대비 미해결 차이 수', len(open_gaps), 0, 2,
              'loop.py RULE에 손잡이 추가 또는 thumbstat 측정 수정'))
    if capped:
        # 점수 0 — 줄일 것이 아니라 "이렇게 두기로 했다"를 보이게만 한다
        M.append(('디자인', '한계 확정(사람 눈으로 정함)', len(capped), len(capped), 0,
                  '다시 밀지 않는다 · 지금: ' + ', '.join(sorted(capped))))

    # 회차 자체가 멈췄나. 2026-09-24: 감시기 회차 하나가 새벽 3:52에 시작해 16시간 23분 동안
    # 안 끝났고, 예약은 앞 회차가 끝나야 다음을 돌리므로 그동안 감시기가 한 번도 안 돌았다.
    # 원고 재고를 채우는 유일한 장치가 멈춘 것인데 아무도 몰랐다. 사장님이 물어서야 찾았다.
    try:
        sys.path.insert(0, HERE)
        import beat
        st = beat.stuck()
        M.append(('회차', '예산 시간을 넘겨 멈춘 회차', len(st), 0, 3,
                  '예약 목록에서 running인 세션을 끊고(stop_session) 그 회차를 다시 돌린다'
                  + (' · 지금: ' + ', '.join(f'{t} {m}분' for t, m, _ in st[:3]) if st else '')))
        d = beat.load() or {}
        old_t = [t for t in beat.BUDGET
                 if not d.get(t, {}).get('start') or (time.time() - d[t]['start']) / 3600 > 6]
        M.append(('회차', '6시간 넘게 맥박 없는 회차', len(old_t), 0, 2,
                  '그 회차 지시문에 beat.py start/end 가 들어 있는지 확인'
                  + (' · 지금: ' + ', '.join(old_t[:4]) if old_t else '')))
    except Exception as e: print('회차 맥박 점검 실패:', repr(e)[:90])

    # 만들어 놓고 아무 회차도 안 부르는 도구가 있나.
    # 2026-09-24 하루에만 이 패턴이 네 번 나왔다 — 오피스텔 단지표·건축물대장·유튜버 시리즈 조사,
    # 그리고 발굴 종목(결과를 파일로 안 남겨 분석이 못 썼다). 전부 사장님이 지적해서 알았다.
    # 지시문 어디에도 이름이 안 나오는 도구는 영영 안 돈다. 그걸 기계가 센다.
    try:
        skills = ''
        for sk in glob.glob(os.path.expanduser('~/.claude/scheduled-tasks/*/SKILL.md')):
            try: skills += open(sk, encoding='utf-8').read()
            except Exception: pass
        mine = [os.path.basename(f) for f in glob.glob(os.path.join(HERE, '*.py'))]
        # 다른 도구가 import해서 쓰는 것은 직접 불리지 않아도 된다
        srcs = ''.join(open(f, encoding='utf-8', errors='ignore').read() for f in glob.glob(os.path.join(HERE, '*.py')))
        orphan = [m for m in mine
                  if m not in skills and m[:-3] not in skills
                  and f'import {m[:-3]}' not in srcs and f'{m[:-3]}.py' not in srcs]
        M.append(('도구', '어느 회차도 안 부르는 도구', len(orphan), 0, 3,
                  '지시문에 넣어 회차가 돌게 하거나, 쓸모없으면 지운다'
                  + (' · 지금: ' + ', '.join(sorted(orphan)[:4]) if orphan else '')))
    except Exception as e: print('도구 점검 실패:', repr(e)[:90])

    # 부동산을 서울 밖에서도 보고 있나. 2026-09-24까지 실거래 602개 파일이 전부 서울(11)이었다.
    try:
        codes = {os.path.basename(f).split('_')[0] for f in glob.glob(os.path.join(R, 'rt', '*.json'))}
        codes = {c for c in codes if c.isdigit() and len(c) == 5}
        outside = len({c for c in codes if not c.startswith('11')})
        M.append(('자료', '서울 밖 시군구 실거래', outside, 10, 2,
                  'py -3.12 work/lawdscan.py 41 <월> 로 코드를 확인하고 rtmolit로 받는다'))
    except Exception: pass

    # 글 루프가 규칙을 만들기만 하고 채점을 못 하고 있나.
    # 2026-09-24: 30회 연속 "규칙 뒤 0편"으로 보류였는데 아무도 못 봤다. 계기판에 없었기 때문이다.
    tl = load(os.path.join(HERE, 'textloop_log.json'), []) or []
    streak = 0
    for r in reversed(tl):
        if '보류' in (r.get('verdict') or ''): streak += 1
        else: break
    # 적을수록 좋은 항목이다. 계기판의 gap 식은 '목표보다 모자란 것'만 재므로
    # 목표 6에 값 48이면 점수가 0으로 찍혔다(2026-09-24 확인). 목표 0에 초과분만 넣는다.
    M.append(('품질', '글 규칙 자기채점 보류가 이어진 회차(6회 초과분)', max(0, streak - 6), 0, 3,
              'textloop 판정이 왜 보류인지 verdict 문구를 읽는다 — 표본이 안 쌓인 것인지, 기준 잡는 식이 틀린 것인지'))

    # 같은 글이 두 번 올라간 적이 있나. 0이 아니면 발행기가 중복을 냈다는 뜻이다.
    # 2026-09-24 국채금리 글이 07:13·07:35 두 번 올라갔고 사장님이 화면으로 잡아 줬다. 이제 기계가 잡는다.
    try:
        sys.path.insert(0, HERE)
        from naverpost import dup_titles
        for kind, name in (('blog', '블로그'), ('cafe', '카페')):
            d = dup_titles(kind)
            M.append(('발행', f'{name} 같은 글 두 번 올라간 수', len(d), 0, 3,
                      '올라간 제목과 대조하고 올린다(naverpost already_up) · 겹친 글은 work/blogfix.py private 로 내린다'
                      + (' · 지금: ' + ', '.join(list(d)[:2]) if d else '')))
    except Exception as e: print('중복 검사 실패:', repr(e)[:120])

    tw = open(os.path.join(R, 'tools-wanted.md'), encoding='utf-8').read() if os.path.exists(os.path.join(R, 'tools-wanted.md')) else ''
    M.append(('도구', '사람 손 필요 항목', tw.count('| 대기 |'), 0, 1, '12:30 보고 "확인 필요"에 올린다'))
    bq = open(os.path.join(R, 'build-queue.md'), encoding='utf-8').read() if os.path.exists(os.path.join(R, 'build-queue.md')) else ''
    M.append(('도구', '만들기 대기열 미완', len(re.findall(r'^\d+\.', bq, re.M)) - bq.count('완료'), 0, 2, 'firemap-improve C 회차가 위에서부터 만든다'))

    # 루틴 권한 밖의 항목 — 사장님만 움직일 수 있다(키 발급·계정 가입·영상 공개 전환).
    # 이 둘은 점수가 높아도 회차가 닫을 수 없어, 일감표 1순위를 매번 차지하면서
    # 정작 루틴이 고칠 수 있는 항목(대기 묶음·안 쓰는 도구)을 밀어냈다(2026-09-24 19시 확인:
    # '사람 손 필요 항목' 4.0이 =변화없음으로 며칠째 1순위). 계기판에는 그대로 두되 주인을 표시한다.
    HUMAN = {'사람 손 필요 항목', '공개한 영상 수(최근 10편 중)'}
    rows = []
    for area, name, val, tgt, w, how in M:
        if val is None: continue
        gap = 0.0 if tgt == 0 and val == 0 else (abs(val - tgt) / max(abs(tgt), 1) if val < tgt or tgt == 0 else 0.0)
        if tgt == 0: gap = float(val)
        rows.append({'area': area, 'name': name, 'value': val, 'target': tgt, 'weight': w, 'gap': round(gap, 3), 'score': round(gap * w, 3), 'how': how,
                     'owner': '사람' if name in HUMAN else '루틴'})
    rows.sort(key=lambda r: -r['score'])
    out = {'at': time.strftime('%Y-%m-%d %H:%M'), 'items': rows}
    json.dump(out, open(os.path.join(HERE, 'health.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"[계기판 {out['at']}]  영역별 부족분 순위 (점수 = 부족분 × 중요도)")
    for r in rows:
        flag = '■' if r['score'] >= 1 else ('·' if r['score'] > 0 else ' ')
        print(f"{flag} {r['score']:5.2f} [{r['area']}] {r['name']}: {r['value']} / 목표 {r['target']}")
    top = [r for r in rows if r['score'] > 0][:3]
    print('\n이번에 고칠 것:', ' | '.join(f"{t['name']} → {t['how']}" for t in top) if top else '없음(전 항목 목표 달성)')

if __name__ == '__main__': main()
