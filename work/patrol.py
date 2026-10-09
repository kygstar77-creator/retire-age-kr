# 순돌이 순찰 점검표(2026-10-02) — 사장님: "30분마다 순찰 돌면서 왜 우리가 이야기한 대로 감시하고 지시하지 못했지?"
# 순찰 때 git log만 보던 것을 '규칙을 실제로 지켰나'를 파일로 재는 점검으로 바꾼다. 결과는 표준 출력.
#   py -3.12 work/patrol.py
import os, re, glob, json, datetime, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
now = datetime.datetime.now()
bad = []

# 1. 카페 대기 묶음(naverpost pending = 아직 안 나간 것만): 보류 안 걸린 것은 경쟁 조사·편집 통과가 있어야 한다
try:
    out = subprocess.run([sys.executable, os.path.join(HERE, 'naverpost.py'), 'pending', '--raw'], capture_output=True, text=True, encoding='utf-8', timeout=120).stdout
    pend = [json.loads(l) for l in out.splitlines() if l.strip().startswith('{')]
except Exception as e:
    pend = []; bad.append(f'카페 대기 목록을 못 읽음: {e}')
for x in pend:
    pkg = x.get('pkg', ''); d = os.path.dirname(pkg); name = os.path.basename(d)
    if x.get('kind') not in (None, 'cafe') and 'cafe' not in str(x.get('kind')): continue
    if os.path.exists(os.path.join(pkg, 'hold.txt')): continue
    miss = [f for f, ok in [('compare.md', os.path.exists(os.path.join(d, 'compare.md')) or os.path.exists(os.path.join(d, 'compete.md'))),
                            ('편집 통과', any(os.path.exists(x) for x in [pkg + '.edit.json', os.path.join(pkg, '.edit.json'), os.path.join(pkg, 'editor_ok.txt')]))] if not ok]
    if miss: bad.append(f'카페 대기 {name}({x.get("kind")}): {"·".join(miss)} 없음 (보류 안 걸림)')

# 2. 롱폼: 예약 대기 편은 경쟁 비교·심사 기록이 있어야 한다
for meta in glob.glob(os.path.join(R, 'longform', 'ep', '*', 'meta.json')):
    ep = os.path.dirname(meta); n = os.path.basename(ep)
    try: m = json.load(open(meta, encoding='utf-8'))
    except Exception: continue
    pa = m.get('publishAt')
    if not pa: continue
    try:
        if datetime.datetime.fromisoformat(pa).replace(tzinfo=None) < now: continue
    except Exception: pass
    for f in ['compare.md', 'review.md']:
        if not os.path.exists(os.path.join(ep, f)): bad.append(f'롱폼 {n}({pa[:16]}): {f} 없음')

# 3. 쇼츠 대기: compete.md
for d in glob.glob(os.path.join(R, 'cardshorts', '*')):
    if os.path.isdir(d) and not os.path.exists(os.path.join(d, 'compete.md')) and os.path.getmtime(d) > (now - datetime.timedelta(days=2)).timestamp():
        bad.append(f'쇼츠 {os.path.basename(d)}: compete.md 없음')

# 4. 영상 속 카페 약속
for s in glob.glob(os.path.join(R, 'longform', 'ep', '*', 'script.md')):
    t = open(s, encoding='utf-8').read()
    if re.search(r'카페에\s*올려', t):
        n = os.path.basename(os.path.dirname(s))
        pr = os.path.join(R, 'longform', 'loop', 'promises.md')
        if not (os.path.exists(pr) and re.search(rf'\b{re.escape(n)}\b.*(cafe\.naver\.com|firemap/\d+)', open(pr, encoding='utf-8').read())):
            bad.append(f'약속: {n} 대본 "카페에 올려" → promises.md에 글 주소 없음')

# 5. today.md 크기(토큰)
td = os.path.join(R, 'meeting', 'today.md')
if os.path.exists(td):
    lines = open(td, encoding='utf-8').read().count('\n')
    if lines > 200: bad.append(f'today.md {lines}줄 — 150줄 넘음(스프린트가 archive로 옮겨야)')



# 10. 가설엔 근거가 있어야 한다(10/2 사장님) — 실험 장부의 진행 중 ID마다 research/experiments/<ID>.md(근거 데이터·분석·예측·판정 기준)
try:
    reg = open(os.path.join(R, 'experiments-registry.md'), encoding='utf-8').read()
    ids = sorted(set(m.group(1) for m in re.finditer(r'^\| (X-[A-Z0-9-]+) \|.*$', reg, re.M) if '종료' not in m.group(0)))  # 종료된 실험은 뺀다
    miss = [i for i in ids if not os.path.exists(os.path.join(R, 'experiments', i + '.md'))]
    if miss: bad.append(f'가설 근거 파일 없음 {len(miss)}/{len(ids)}: ' + ', '.join(miss[:12]))
except Exception as e:
    bad.append(f'실험 장부 못 읽음: {e}')

# 12. 미리 통과(10/2 15:1x 사장님: "관문 못 넘어서 발행 안 할 게 아니라 미리미리 8점 넘겨서 계획한 시간에 발행해야지")
#     research/slots.json — 칸마다 편·관문 통과 시각. 기한 = 발행 시각 - lead. 기한 넘도록 편이 없거나 통과 못 했으면 위반.
#     다음 36시간 안 칸이 아예 장부에 없어도 위반(회의가 배정 안 한 것). 비축분이 reserve_min보다 적으면 위반.
SLOT_SOON = []
try:
    S = json.load(open(os.path.join(R, 'slots.json'), encoding='utf-8'))
    lead = S['lead_hours']; have = set()
    for x in S['slots']:
        at = datetime.datetime.strptime(x['at'], '%Y-%m-%d %H:%M'); have.add((x['kind'], x['at']))
        if x.get('skip'):
            # skip은 롱폼 칸만, 사유·대체 계획(note)이 있어야 인정. 아니면 칸 비우기=실패 규칙 위반.
            note = x.get('note') or ''
            if x['kind'] != 'long': bad.append(f"skip 불가: {x['at'][5:]} {x['kind']} — 쇼츠·카페 칸은 건너뛰지 못함(비축분으로 채움)")
            elif at >= now and (len(note) < 40 or not re.search(r'빨라야|늦어도|지우고|대체|비축|\d+/\d+', note)): bad.append(f"skip 근거 부족: {x['at'][5:]} long — note에 사유와 대체 계획(다음 편·날짜) 필요")
            if x['kind'] != 'long' and at >= now: pass
            else: continue
        if at < now: continue
        dl = at - datetime.timedelta(hours=lead[x['kind']])
        # 10/7 write: 10/8 08:10 칸 nhisrent1005가 gates_ok인데도 발행기가 '같은 대상 이미 씀'(#209)으로 막고 있었다.
        # 관문 통과 표시만 보면 칸이 찬 것처럼 보이니, 다음 36시간 카페 칸 묶음은 발행기 막힘(hold·같은 대상)도 미리 잰다.
        if x['kind'] == 'cafe' and x.get('item') and at <= now + datetime.timedelta(hours=36):
            pk = os.path.join(R, x['item'], 'pkg')
            try:
                if os.path.exists(os.path.join(pk, 'hold.txt')):
                    bad.append(f"칸 묶음 보류됨: {x['at'][5:]} cafe {x['item']} — hold.txt가 있어 발행기가 안 올림, 칸 편 교체 필요")
                elif os.path.exists(os.path.join(pk, 'title.txt')) and not os.path.exists(os.path.join(pk, 'published.txt')):
                    if HERE not in sys.path: sys.path.insert(0, HERE)
                    import naverpost as _np
                    _dup = _np.same_subject_today('cafe', open(os.path.join(pk, 'title.txt'), encoding='utf-8').read().strip())
                    if _dup: bad.append(f"칸 묶음 중복 막힘: {x['at'][5:]} cafe {x['item']} — 발행기 '같은 대상 이미 씀'({_dup[0][1]}), 칸 편 교체 필요")
                    # 10/9 회의: 장부(slots.json)와 발행 코드가 읽는 pkg/slot.txt 시각이 따로 놀았다(schdacct1007 10/7 12 vs 10/10 16:10).
                    _lm = _np.ledger_mismatch(pk)
                    if _lm.startswith('두 시각 다름'): bad.append(f"칸 묶음 {_lm}: {x['item']} — slot.txt를 장부 칸 시각으로 고칠 것(발행기는 slot.txt만 본다)")
            except Exception as e:
                print('칸 묶음 막힘 검사 못 함:', x['item'], e)
        if x.get('gates_ok'): continue
        what = f"{x['at'][5:]} {x['kind']} {x.get('item') or '편 없음'}({x.get('owner','')})"
        if now >= dl: bad.append(f'미리 통과 못 함: {what} — 관문 기한 {dl:%m/%d %H:%M} 지남, 비축분으로 바꾸거나 오늘 안에 통과')
        elif now >= dl - datetime.timedelta(hours=lead[x['kind']]): SLOT_SOON.append(f'{what} 관문 기한 {dl:%m/%d %H:%M}')
    cad = {'cafe': ['08:10','10:10','12:10','14:10','16:10','18:10','20:10','22:10'], 'shorts': ['12:20','19:20']}  # 롱폼은 하루 1편 이하 '상한'이지 매일 칸이 아님(10/5) — 칸이 있으면 위 관문 검사, 편 준비는 reserve_min.long이 지킴
    for k, ts in cad.items():
        for d in range(0, 3):
            day = (now + datetime.timedelta(days=d)).strftime('%Y-%m-%d')
            for t in ts:
                at = datetime.datetime.strptime(f'{day} {t}', '%Y-%m-%d %H:%M')
                if now < at <= now + datetime.timedelta(hours=36) and (k, f'{day} {t}') not in have:
                    bad.append(f'칸 배정 없음: {day[5:]} {t} {k} — slots.json에 편·담당을 적어야 함')
    _ld = {}
    for x in S['slots']:
        if x['kind'] == 'long' and not x.get('skip'): _ld[x['at'][:10]] = _ld.get(x['at'][:10], 0) + 1
    for d_, n_ in _ld.items():
        if n_ > 1: bad.append(f'롱폼 하루 1편 초과: {d_} {n_}칸')
    for k, n in S.get('reserve_min', {}).items():
        if len(S.get('reserve', {}).get(k, [])) < n: bad.append(f'비축분 부족: {k} {len(S["reserve"].get(k, []))}/{n} — 관문 통과한 예비 편')
    for l in SLOT_SOON: print('곧 관문 기한:', l)
except Exception as e:
    bad.append(f'slots.json 못 읽음: {e}')

# 7. 약속 점검표(research/commitments.json — 사장님과 정한 것마다 증거 파일·기한). 기한 지났는데 증거 없으면 위반.
try:
    C = json.load(open(os.path.join(R, 'commitments.json'), encoding='utf-8'))
except Exception as e:
    C = []; bad.append(f'commitments.json 못 읽음: {e}')
done = 0
for c in C:
    due = datetime.datetime.strptime(c['due'], '%Y-%m-%d %H:%M')
    ok = False
    if c.get('evidence'):
        f = os.path.join(R, c['evidence']); ok = os.path.exists(f)
        if ok and c.get('fresh_hours'): ok = (now.timestamp() - os.path.getmtime(f)) < c['fresh_hours'] * 3600
    elif c.get('evidence_glob'):
        ok = bool(glob.glob(os.path.join(R, c['evidence_glob'])))
    elif c.get('evidence_grep'):
        f, pat = c['evidence_grep']; f = os.path.join(R, f)
        ok = os.path.exists(f) and re.search(pat, open(f, encoding='utf-8', errors='ignore').read()) is not None
    if ok: done += 1
    elif now > due: bad.append(f'약속 기한 넘김: {c["what"]} (기한 {c["due"]}, 담당 {c["owner"]})')
print(f'약속 점검표 {done}/{len(C)} 끝남')


# 8. 발전하고 있나 — 증명 기준 4개(10/15 목표) 지금 값
def last_line(f, pat):
    f = os.path.join(R, f)
    if not os.path.exists(f): return '파일 없음'
    L = [l for l in open(f, encoding='utf-8', errors='ignore').read().splitlines() if re.search(pat, l)]
    return L[-1][:140] if L else '줄 없음'
M = {}
M['visits'] = last_line('growth/daily.md', r'^20\d\d-\d\d-\d\d'); print('지표 · 방문:', M['visits'])
M['revenue'] = last_line('growth/revenue.md', r'^20\d\d-\d\d-\d\d'); print('지표 · 수익·쿠팡:', M['revenue'])
try:
    sys.path.insert(0, HERE); import ytupload
    y = ytupload.service()
    up = y.channels().list(part='contentDetails,statistics', mine=True).execute()['items'][0]
    ids = [i['contentDetails']['videoId'] for i in y.playlistItems().list(part='contentDetails', playlistId=up['contentDetails']['relatedPlaylists']['uploads'], maxResults=15).execute()['items']]
    vs = y.videos().list(part='snippet,statistics,status,contentDetails', id=','.join(ids)).execute()['items']
    pub = [v for v in vs if v['status']['privacyStatus'] == 'public']
    for v in pub:  # 10/2 E-1: status만 update하면 embeddable·publicStatsViewable이 False로 초기화됐다(순돌이 실수) — 공개 영상은 둘 다 켜져 있어야
        if not (v['status'].get('embeddable') and v['status'].get('publicStatsViewable')): bad.append(f"유튜브 {v['id']}: 퍼가기·조회수 공개 꺼짐 — status update 때 두 값을 같이 보내야 함")
        if v['snippet'].get('defaultAudioLanguage') != 'ko': bad.append(f"유튜브 {v['id']}: 오디오 언어 {v['snippet'].get('defaultAudioLanguage')} — 한국어(ko)여야 함, snippet update 때 defaultAudioLanguage를 같이 보낼 것(10/5 E-1·N-1 en-US 사고)")
    sh = [int(v['statistics'].get('viewCount', 0)) for v in pub if 'PT1M' not in v['contentDetails']['duration'] and re.match(r'PT\d+S$', v['contentDetails']['duration'])]
    M['subs'] = int(up['statistics']['subscriberCount']); M['shorts_avg'] = sum(sh)//max(1,len(sh)); M['shorts_n'] = len(sh)
    print(f"지표 · 유튜브 구독 {M['subs']} · 공개 쇼츠 {len(sh)}편 평균 조회 {M['shorts_avg']}(목표 460)")
except Exception as e:
    print('지표 · 유튜브 확인 안 됨:', str(e)[:80])

# 11. 시각 관문(10/2 대역): today.md·decisions/log.md 새 줄의 기록 시각이 커밋보다 5분 넘게 늦으면 위반, today.md 줄에 표시
try:
    sys.path.insert(0, HERE); import timecheck
    th = timecheck.check_today(); timecheck.mark(th)
    th = [t for t in th if t[1].replace(tzinfo=None) > now - datetime.timedelta(hours=3)]  # 순돌이 15:0x: 지난 기록 47건이 요약을 덮어 최근 3시간 것만 위반으로
    for f, at, g, l in th[-5:]: bad.append(f'시각 확인 · {os.path.basename(f)} 커밋 {at:%H:%M}보다 {int(g)}분 늦음: {l.strip()[:70]}')
    if len(th) > 5: bad.append(f'시각 확인 · 오늘 미래 시각 기록 총 {len(th)}건(위 5건만 표시)')
except Exception as e:
    bad.append(f'시각 관문 못 돌림: {e}')

# 6. 최근 2시간 커밋 수(회사가 도는가)
try:
    c = subprocess.run(['git', '-C', os.path.dirname(HERE), 'log', '--since=2 hours ago', '--oneline'], capture_output=True, text=True, encoding='utf-8').stdout.count('\n')
except Exception: c = -1
print(f'순찰 {now:%m/%d %H:%M} · 최근 2시간 커밋 {c} · 규칙 위반 {len(bad)}')
for b in bad: print(' -', b)

# 9. 사장님 요약 → work/dashboard/summary.json (순돌이가 상황판 db board/summary에 그대로 올린다 — 페이지 재게시 없이 토큰 최소)
today = now.strftime('%Y-%m-%d')
cafe_today = 0
try:
    rt = json.load(open(os.path.join(HERE, 'runs_today.json'), encoding='utf-8'))
    if rt.get('date') == today: cafe_today = sum(1 for r in rt.get('runs', []) if r.get('cafe'))
except Exception: pass
long_sched = []
try:
    for l in open(os.path.join(R, 'longform', 'loop', 'uploads.jsonl'), encoding='utf-8'):
        u = json.loads(l)
        if u.get('publishAt') and u['publishAt'][:10] >= today: long_sched.append(u['publishAt'][5:16].replace('T', ' ') + ' ' + u.get('ep', ''))
except Exception: pass
overdue = [b.replace('약속 기한 넘김: ', '') for b in bad if b.startswith('약속 기한 넘김')]
summ = {
    'at': now.strftime('%m/%d %H:%M'),
    'proof': {'visits_target': '하루 100세션', 'visits_now': M.get('visits', '확인 안 함')[:90] if 'M' in dir() else '확인 안 함',
              'shorts_avg': M.get('shorts_avg') if 'M' in dir() else None, 'shorts_target': 460,
              'coupang': (M.get('revenue', '') if 'M' in dir() else '')[:120], 'subs': M.get('subs') if 'M' in dir() else None},
    'publish_today': {'cafe': cafe_today, 'cafe_cap': 8, 'long_scheduled': long_sched[:3]},
    'commitments': {'done': done, 'total': len(C), 'overdue': overdue[:6]},
    'violations': {'count': len(bad), 'top': [b for b in bad if not b.startswith('약속 기한 넘김')][:6]},
}
json.dump(summ, open(os.path.join(HERE, 'dashboard', 'summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('요약 저장: work/dashboard/summary.json')
