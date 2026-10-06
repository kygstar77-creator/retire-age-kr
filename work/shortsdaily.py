# 쇼츠 하루 2~3편 발행 — 2026-09-29 사장님 "그럼 그렇게 해"
#   py -3.12 work/shortsdaily.py status                      오늘 올린 편수·마지막 발행·쓴 원고 목록
#   py -3.12 work/shortsdaily.py check   <spec.json>          숫자 대조·글 길이만 본다(만들지 않음)
#   py -3.12 work/shortsdaily.py publish <spec.json>          대조 → 영상 → 유튜브 공개 → 기록
#   py -3.12 work/shortsdaily.py d7                          편별 공개 뒤 7일 조회·구독 증가를 log.jsonl에 채운다(ytanalytics 토큰)
#
# 왜 하루 3편까지인가(work/research/shorts-research.md):
#   - 유튜브 스팸 정책 원문: "자동화 도구나 AI를 사용해 최소한의 수정만 거친 유사 콘텐츠를 대량으로 생성하는 행위",
#     "콘텐츠를 반복적으로 또는 템플릿을 사용해 제작하는 행위" — 삭제·경고 대상.
#   - 경쟁 최대가 하루 4.6편(어른의금융수업), 추천 신호에 업로드 빈도는 없다.
# 숫자 규칙: 영상·제목·설명에 나오는 숫자는 전부 spec의 facts 파일(원고 조사 사실표)에 있어야 한다. 없으면 올리지 않는다.
import sys, os, re, json, time, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
OUT = os.path.join(HERE, 'research', 'cardshorts'); os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, 'log.jsonl')
DAY_CAP, MIN_GAP_H = min(2, int(os.environ.get('SHORTS_DAY_CAP', '2'))), 6   # 기본 하루 2편(10/2 사장님 지시 X-YT-FREQ, 12:20·19:20), 간격 6시간   # 2026-09-30 정책 조사 뒤 3편→2편: 유튜브 "frequently sharing content that doesn't resonate ... affect your channel's overall performance", 업로드 빈도는 성장과 "not correlated" (research/longform/yt-policy-algorithm.md)
CAFE = 'https://cafe.naver.com/firemap'

def log_rows():
    if not os.path.exists(LOG): return []
    return [json.loads(l) for l in open(LOG, encoding='utf-8') if l.strip()]

def today_rows():
    d = time.strftime('%Y-%m-%d'); return [r for r in log_rows() if r['at'][:10] == d]

NUM = re.compile(r'\d[\d,]*(?:\.\d+)?')
def nums(text):
    return {n.replace(',', '').rstrip('.') for n in NUM.findall(text or '')}

def card_text(c):
    """B형 카드 한 장의 화면 글자 전부(막대 길이용 숫자 rows[i][1]는 화면에 안 찍혀서 뺀다)."""
    out = list(c.get('q', [])) + list(c.get('head', [])) + list(c.get('points', [])) + list(c.get('lines', []))
    out += [c.get('small', ''), c.get('note', ''), c.get('unit_label', '')]
    out += [f'{l} {v:,}{u}' for l, v, u in c.get('steps', [])]
    out += [f'{l} {txt}' for l, _, txt in c.get('rows', [])]
    return ' '.join(x for x in out if x)

def spec_text(spec):
    parts = [spec.get('chip', ''), ' '.join(spec.get('title', [])), ' '.join(spec.get('sub', [])),
             ' '.join(spec.get('points', [])), spec.get('yt_title', ''), spec.get('yt_desc', '')]
    parts += [f'{l} {v}' for l, v, _ in spec.get('bars', [])]
    parts += spec.get('cover', [])                                   # 표지 글자도 사실표 대조(2026-10-03)
    parts += [card_text(c) for c in spec.get('cards', [])]          # B형 카드 글자(2026-10-06)
    cc = spec.get('cover_chart') or {}
    parts += [cc.get('big', ''), cc.get('span', '')]
    return ' '.join(parts)

_BHS_CMAP = None
def bhs_missing(texts):
    """제목체(BlackHanSans)에 글자가 없어 카드에 빈칸으로 찍히는 글자(2026-10-06: '자가·전세'가 '자가   전세'로, 10/3·10/5 두 번).
    cardshort.py가 BHS로 그리는 글만 본다 — 제목 줄·표지·표지 큰 글자. fontTools가 없으면 못 잼(빈 목록)."""
    global _BHS_CMAP
    if _BHS_CMAP is None:
        try:
            from fontTools.ttLib import TTFont
            _BHS_CMAP = set(TTFont(os.path.join(HERE, 'fonts', 'BlackHanSans.ttf')).getBestCmap())
        except Exception: _BHS_CMAP = False
    if not _BHS_CMAP: return []
    out = []
    for t in texts:
        for ch in t or '':
            if not ch.isspace() and ord(ch) not in _BHS_CMAP and ch not in out: out.append(ch)
    return out

def check(spec):
    """(문제 목록). 날짜·연도·순번 같은 숫자는 사실표에 없어도 된다(ALLOW)."""
    bad = []
    fp = spec.get('facts')
    if not fp or not os.path.exists(fp): return ['facts 파일 없음: %s' % fp]
    facts = open(fp, encoding='utf-8').read()
    have = nums(facts)
    # 사실표에 '1억 2,000만원'처럼 적혀 있고 spec엔 '12000'로 쓰는 일은 막는다 — 적힌 모양 그대로 쓴다.
    allow = set(spec.get('allow', [])) | {'1', '2', '3', '4', '5', '12', '2026'}
    for n in sorted(nums(spec_text(spec)) - have - allow):
        bad.append('사실표에 없는 숫자: ' + n)
    for i, c in enumerate(spec.get('cards', []), 1):   # B형: 카드 한 장에 숫자 3개까지(계기판은 한 번에 숫자 하나라 뺀다) · 장마다 6~10초 · 합 25~40초
        if c.get('kind') != 'gauge':
            ns = nums(' '.join(list(c.get('head', [])) + list(c.get('points', [])) + list(c.get('lines', [])) + [c.get('note', '')] + [f'{l} {x}' for l, _, x in c.get('rows', [])]))  # 줄 이름(라벨)도 화면 숫자
            if len(ns) > 3: bad.append(f'카드 {i}에 숫자 {len(ns)}개(3개까지): ' + ', '.join(sorted(ns)))
        if not 6 <= c.get('sec', 0) <= 10: bad.append(f'카드 {i} 길이 {c.get("sec")}초(6~10초)')
    if spec.get('cards'):
        tot = sum(c.get('sec', 0) for c in spec['cards'])
        if not 25 <= tot <= 40: bad.append(f'카드 합 {tot}초(25~40초)')
    bhs_cards = [x for c in spec.get('cards', []) for x in list(c.get('q', [])) + list(c.get('head', [])) + [r[2] for r in c.get('rows', [])]]
    bhs_cards += [f'{v:,}{u}' for c in spec.get('cards', []) for _, v, u in c.get('steps', [])]
    cc = spec.get('cover_chart') or {}
    for ch in bhs_missing(bhs_cards + list(spec.get('title', [])) + list(spec.get('cover', [])) + [cc.get('big', '')]):
        bad.append("카드 제목 글꼴에 '%s'(U+%04X) 글자가 없어 빈칸으로 나옴 — '와'·','로 바꾸기" % (ch, ord(ch)))
    t = spec.get('yt_title', '')
    if not t: bad.append('yt_title 없음')
    if len(t) > 70: bad.append('yt_title 70자 넘음(%d)' % len(t))
    for w in ('사세요', '사지 마', '팔아라', '무조건', '당장', '폭탄', '패가망신', '지우세요'):
        if w in t or w in spec.get('yt_desc', ''): bad.append('쓰지 않는 말: ' + w)
    tags = spec.get('hashtags', [])
    if not 3 <= len(tags) <= 5: bad.append('해시태그는 3~5개(지금 %d)' % len(tags))
    if not spec.get('source'): bad.append('출처 줄 없음')
    # ── 유튜브 정책 관문(research/longform/yt-policy-algorithm.md §5, 2026-09-30) ──
    for w in ('추천 종목', '수익 보장', '원금 보장', '전문가인 제가', '제가 추천', '!!'):          # C7
        if w in t or w in spec.get('yt_desc', '') or w in ' '.join(spec.get('points', [])): bad.append('쓰지 않는 말: ' + w)
    if re.search(r'[A-Z]{5,}', t) and not re.search(r'(SCHD|JEPQ|JEPI|QQQM|TQQQ|SPYI|QQQI|NVIDIA|KODEX|TIGER)', t): bad.append('영어 대문자 단어로 외치는 제목')
    foot = spec.get('foot', '')                                                                   # C13
    if re.search(r'https?://|\.com|\.kr|naver', foot): bad.append('카드 화면에 외부 주소(foot) — 쇼츠에선 빼기')
    rows = log_rows()
    if rows and spec.get('layout', 'bars') == rows[-1].get('layout'): bad.append('직전 편과 같은 틀(layout) — 바꿔야 함')   # C3
    last10 = [r.get('layout') for r in rows[-10:]] + [spec.get('layout', 'bars')]
    # 틀이 bars·rank 둘뿐이라 편 수가 홀수면 번갈아 써도 한쪽이 절반을 넘는다(2026-10-03 e1_micron_q4: 7편 중 4 = 어느 쪽을 골라도 위반).
    # → 한 틀이 다른 틀보다 2편 이상 많을 때만 위반.
    mx = max(last10.count(x) for x in set(last10))
    if len(last10) >= 6 and mx / len(last10) > 0.5 and mx - (len(last10) - mx) > 1: bad.append('최근 10편 중 한 틀이 절반 넘음')
    def g3(x): x = re.sub(r'\s|#\S+', '', x); return {x[i:i + 3] for i in range(len(x) - 2)}           # C4
    me = g3(t)
    for r in rows[-30:]:
        o = g3(r.get('title', ''))
        if me and o and len(me & o) / len(me | o) >= 0.6: bad.append('최근 제목과 너무 비슷함: ' + r.get('title', '')[:30])
    import hashlib                                                                                 # C2
    aseed = hashlib.md5((t + spec.get('facts', '')).encode('utf-8')).hexdigest()
    if spec.get('music', True) and aseed in {r.get('audio_seed') for r in rows[-30:]}: bad.append('배경음이 최근 30편과 같음')
    if 'music' not in spec: bad.append('spec에 "music": true/false를 적어야 함 — 음악 실험 중(직전 편과 반대로, experiments.md)')
    return bad

GAP_WARN = 0.2   # 읽히는 칸의 20% 넘게 비면 경고(막지는 않는다 — 사실이 아니라 화면 문제)

def warn(spec):
    """공개를 막지 않는 화면 경고. 2026-10-06: 카드 아래 약 23% 빈칸이 세 편에서 반복(backlog)."""
    out = []
    try:
        import cardshort
        g = cardshort.bottom_gap(spec)
        if g and g[1] > GAP_WARN:
            out.append(f'카드 아래 {g[1]:.0%} 빈칸(글 끝 y={g[0]}, 읽히는 칸 끝 {cardshort.SAFE_B}) — 점(points) 한 줄을 더하거나 막대·순위 줄을 늘린다')
    except Exception as e:
        out.append(f'빈칸 재기 실패: {e}')
    return out

def channel_today():
    """채널 전체의 오늘(한국 시간) 공개 쇼츠 수 — 이 로그 말고 다른 루틴(동네 쇼츠 등)이 올린 것까지 센다.
    2026-09-30: 한도를 이 파일 로그로만 세면 firemap-youtube-loop의 동네 쇼츠가 빠져 하루 3편을 넘길 수 있었다. 못 재면 None."""
    try:
        import ytupload
        yt = ytupload.service()
        up = yt.channels().list(part='contentDetails', mine=True).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        ids = [i['contentDetails']['videoId'] for i in yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=15).execute()['items']]
        kst = datetime.timezone(datetime.timedelta(hours=9)); today = datetime.datetime.now(kst).date(); n = 0
        for v in yt.videos().list(part='snippet,status,contentDetails', id=','.join(ids)).execute()['items']:
            at = datetime.datetime.fromisoformat(v['snippet']['publishedAt'].replace('Z', '+00:00')).astimezone(kst)
            m = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?$', v['contentDetails']['duration'])
            secs = (int(m[1] or 0) * 60 + int(m[2] or 0)) if m else 999
            if at.date() == today and v['status']['privacyStatus'] == 'public' and secs <= 180: n += 1
        return n
    except Exception as e:
        print('  (채널 쇼츠 수를 못 잼 — 로그로만 센다:', str(e)[:80], ')'); return None

def gate():
    for nm in ('STOP_youtube', 'STOP_shorts'):   # 감사 담당(firemap-audit)의 정지 스위치(2026-09-30)
        f = os.path.join(HERE, 'research', nm)
        if os.path.exists(f): return '감사 정지 스위치: ' + (open(f, encoding='utf-8', errors='ignore').read().strip() or nm)[:200]
    rows = today_rows(); ch = channel_today(); n = max(len(rows), ch or 0)
    if n >= DAY_CAP: return f'오늘 채널 전체 {n}편 — 하루 {DAY_CAP}편까지(동네 쇼츠 포함)'
    if rows:
        last = datetime.datetime.fromisoformat(rows[-1]['at'])
        gap = (datetime.datetime.now() - last).total_seconds() / 3600
        if gap < MIN_GAP_H: return f'마지막 발행 {gap:.1f}시간 전 — {MIN_GAP_H}시간 간격'
    return ''

def build_desc(spec):
    """설명란 글. spec "cafe_line": false면 카페 주소 줄을 뺀다(없으면 true — 기존 쇼츠 그대로).
    2026-10-01 F5 sevpay: 계산기 utm 링크 1개 원칙인데 publish가 카페 주소를 자동으로 붙여 링크가 2개가 됐다."""
    cafe = ('금리·예금·연금·부동산 숫자를 매일 정리하는 곳 — 파이어맵 카페\n' + CAFE + '\n\n') if spec.get('cafe_line', True) else ''
    # 10/5 audit xWAnTpGJTHg: source가 '출처 …'로 시작하면 '출처: 출처'가 됐다 — 앞머리 '출처'를 떼고 붙인다
    src = re.sub(r'^\s*출처\s*[:：]?\s*', '', spec['source'])
    return spec['yt_desc'].strip() + '\n\n' + '출처: ' + src + '\n\n' + cafe + ' '.join('#' + h for h in spec['hashtags'])

def publish(sp):
    spec = json.load(open(sp, encoding='utf-8'))
    bad = check(spec)
    for w in warn(spec): print('경고(막지 않음):', w)
    # 경쟁 비교 관문(10/2 대역): cardshorts/<편>/compete.md에 경쟁 5편 표(| 1 | … | 5 |)가 없으면 공개하지 않는다. 이름은 compete.md 하나로 통일
    cp = os.path.join(os.path.splitext(sp)[0], 'compete.md')
    if not os.path.exists(cp): bad.append('경쟁 비교 없음: ' + os.path.relpath(cp, HERE) + ' (경쟁 5편 표 + 잘된 이유·다른 한 가지)')
    elif len(re.findall(r'^\|\s*\d+\s*\|', open(cp, encoding='utf-8').read(), re.M)) < 5: bad.append('compete.md 경쟁 표가 5편 미만')
    if bad: print('올리지 않는다:'); [print('  -', b) for b in bad]; sys.exit(2)
    g = gate()
    if g and os.environ.get('SHORTS_FORCE') != '1': print('올리지 않는다:', g); sys.exit(3)
    # 같은 사실표라도 주인공(제목 첫 어절 — 종목·제도 이름)이 다르면 다른 편이다(10/3 순돌이 결정: 롱폼 E-1 사실표로 하이닉스·마이크론 각각).
    # 같은 사실표 + 같은 주인공이거나, 한 사실표로 3편째면 막는다(재탕 방지는 그대로).
    subj = lambda t: re.sub(r'[^\w가-힣]', '', (t or '').split()[0]) if t else ''
    same = [r for r in log_rows() if r.get('facts') and r.get('facts') == spec.get('facts')]
    if any(subj(r.get('title')) == subj(spec.get('yt_title')) for r in same) or len(same) >= 2:
        print('올리지 않는다: 이 사실표로 같은 주인공 쇼츠가 있거나 이미 2편 —', spec['facts']); sys.exit(4)
    import cardshort, ytupload
    mp4 = os.path.splitext(sp)[0] + '.mp4'
    cardshort.build(spec, mp4)
    desc = build_desc(spec)
    vid = ytupload.upload(mp4, spec['yt_title'], desc, privacy='public', tags=','.join(spec.get('tags', spec['hashtags'])))
    import hashlib
    row = {'at': datetime.datetime.now().isoformat(timespec='seconds'), 'id': vid, 'title': spec['yt_title'],
           'audio_seed': hashlib.md5((spec['yt_title'] + spec.get('facts', '')).encode('utf-8')).hexdigest(),
           'layout': spec.get('layout', 'bars'), 'music': spec.get('music', True), 'facts': spec.get('facts'), 'spec': sp,
           'd7_views': None, 'd7_subs': None}   # 7일 성과 칸 — `d7`이 공개 10일 뒤 채움
    open(LOG, 'a', encoding='utf-8').write(json.dumps(row, ensure_ascii=False) + '\n')
    print('기록', json.dumps(row, ensure_ascii=False))

def d7():
    """2026-09-30 전체 회의 배정: 편별 7일 성과 기준선. 공개일~+6일(7일) 조회·구독 증가를 YouTube Analytics로 잰다.
    분석 API는 2~3일 늦게 차므로 공개 뒤 10일이 지난 편만 채운다(덜 찬 값을 7일치로 적지 않으려고). 채운 편은 다시 안 잰다."""
    import ytanalytics
    rows = log_rows(); today = datetime.date.today(); n = 0
    for r in rows:
        if r.get('d7_views') is not None or not r.get('id'): continue
        pub = datetime.date.fromisoformat(r['at'][:10])
        if (today - pub).days < 10: print('  아직', r['at'][:10], r['id'], f'({(today - pub).days}일째)'); continue
        rep = ytanalytics.q('views,subscribersGained', filters='video==' + r['id'], start=pub.isoformat(), end=(pub + datetime.timedelta(days=6)).isoformat())
        v, sub = (rep.get('rows') or [[0, 0]])[0]
        r['d7_views'], r['d7_subs'], r['d7_at'] = int(v), int(sub), today.isoformat(); n += 1
        print('  채움', r['id'], '조회', v, '구독', sub, r['title'][:30])
    if n:
        tmp = LOG + '.tmp'; open(tmp, 'w', encoding='utf-8').write(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows)); os.replace(tmp, LOG)
    print(f'7일 성과 {n}편 채움')

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    if cmd == 'status':
        rows = today_rows(); print(f'오늘 {len(rows)}/{DAY_CAP}편', '| 막힘:', gate() or '없음')
        for r in log_rows()[-10:]: print(' ', r['at'], r['layout'], r['id'], r['title'][:40])
    elif cmd == 'check':
        sp_ = json.load(open(sys.argv[2], encoding='utf-8'))
        b = check(sp_); print('\n'.join(b) if b else '문제 없음')
        for w in warn(sp_): print('경고(막지 않음):', w)
    elif cmd == 'publish': publish(sys.argv[2])
    elif cmd == 'desc':   # 올리지 않고 설명란만 찍는다(링크 수 확인용)
        d = build_desc(json.load(open(sys.argv[2], encoding='utf-8'))); links = re.findall(r'https?://\S+', d)
        print(d); print('---\n링크', len(links), '개:', links)
    elif cmd == 'd7': d7()
