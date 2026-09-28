# 잘나가는 유튜버 학습 — 사장님 지시(2026-09-23): 부동산·주식 가리지 말고 상위 채널의 스크립트와 화면을 계속 받아 배운다.
#   python work/ytlearn.py "부동산" "미국주식" "배당" ...   → 검색어별 상위 채널을 찾고, 채널마다 최신 영상 2개의 자막(전문)·스토리보드(장면 모음)를 저장,
#                                                          work/research/yt/lessons_<날짜>.md 에 훅(첫 30초)·구조(분 단위 첫 문장)·제목 패턴·자주 쓰는 말을 정리
#   python work/ytlearn.py --channels UCxxxx UCyyyy        → 채널 ID 직접
#   python work/ytlearn.py --re                            → 부동산 상위 11채널(build-queue 4번, 2026-09-28) + 저평가 판단 기준 집계
#                                                          → work/research/yt/re_criteria_<날짜>.md (자막에서 기준 낱말이 몇 영상에서 몇 번 나왔나)
# 키 없음. youtube_transcript_api(자막)·yt-dlp(스토리보드 URL만, 영상 다운로드 안 함)·RSS 사용. 자막 없는 영상은 건너뛴다.
import sys, os, re, json, time, subprocess, collections, urllib.request, urllib.parse, urllib.error
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'research', 'yt'); os.makedirs(OUT, exist_ok=True)
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) Chrome/126', 'Accept-Language': 'ko'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=25).read().decode('utf-8', 'ignore')
def subs_num(s):
    m = re.search(r'(\d+(?:\.\d+)?)\s*(만|천)?', s or '')
    if not m: return 0
    n = float(m.group(1)); return int(n * (10000 if m.group(2) == '만' else 1000 if m.group(2) == '천' else 1))

def unesc(t):
    # JSON 안의 유니코드 이스케이프를 글자로 되돌린다(채널 이름에 섞여 나온다).
    try: return json.loads('"' + t + '"')
    except Exception: return t

def search_channels(q, n=5):
    s = get('https://www.youtube.com/results?' + urllib.parse.urlencode({'search_query': q, 'sp': 'EgIQAg%3D%3D'}))
    out = []
    # 2026-09-24 실측: 유튜브가 필드를 뒤바꿨다. subscriberCountText 에는 @핸들이, videoCountText 에는 '구독자 3.71만명'이 들어온다.
    # 그래서 예전 정규식은 구독자 수 자리에 @핸들을 넣었고 subs 가 전부 0이 돼 '상위 채널' 정렬이 무의미했다.
    # 필드 이름을 믿지 말고 채널 블록 안에서 '구독자 …명' 글자를 직접 찾는다.
    for blk in s.split('{"channelRenderer":')[1:]:
        blk = blk[:4000]
        cid = re.match(r'\{"channelId":"(UC[\w-]+)"', blk)
        ttl = re.search(r'"title":\{"simpleText":"([^"]+)"', blk)
        if not (cid and ttl): continue
        sub = re.search(r'"(구독자 [^"]+명)"', blk)
        han = re.search(r'"canonicalBaseUrl":"/(@[\w.-]+)"', blk)
        out.append({'id': cid.group(1), 'name': unesc(ttl.group(1)),
                    'subs': subs_num(sub.group(1) if sub else ''), 'subs_text': sub.group(1) if sub else '?',
                    'handle': han.group(1) if han else None})
    out.sort(key=lambda x: -x['subs']); return out[:n]

def resolve_handle(handle):
    # 채널 ID가 낡아 RSS 가 404 일 때 핸들(@xxx) 페이지에서 지금 ID를 다시 읽는다.
    try:
        m = re.search(r'"(?:externalId|channelId)":"(UC[\w-]+)"', get(f'https://www.youtube.com/{handle}'))
        return m.group(1) if m else None
    except Exception: return None

def channel_videos(cid, n=2, handle=None):
    f = None
    for attempt in (1, 2, 3):
        try:
            f = get(f'https://www.youtube.com/feeds/videos.xml?channel_id={cid}'); break
        except urllib.error.HTTPError as e:
            if e.code >= 500 and attempt < 3: time.sleep(3); continue      # 500·503 은 일시 오류 — 쉬고 다시
            if e.code == 404 and handle and attempt < 3:
                c2 = resolve_handle(handle)
                if c2 and c2 != cid: cid = c2; continue                    # 404 는 ID가 낡은 것 — 핸들로 다시 찾는다
            raise
    if f is None: raise RuntimeError('RSS 응답 없음')
    vids = []
    for e in re.findall(r'<entry>(.*?)</entry>', f, re.S):   # 한 항목에 조회수가 빠져도 그 항목만 0으로 두고 살린다(예전엔 통째로 버렸다)
        t = re.search(r'<title>(.*?)</title>', e, re.S); v = re.search(r'<yt:videoId>(.*?)</yt:videoId>', e)
        p = re.search(r'<published>(.*?)</published>', e); c = re.search(r'<media:statistics views="(\d+)"', e)
        if not (t and v): continue
        vids.append({'title': t.group(1), 'id': v.group(1), 'pub': p.group(1)[:10] if p else '', 'views': int(c.group(1)) if c else 0})
    vids.sort(key=lambda x: -x['views']); return vids[:n], [x['title'] for x in vids]

BLOCKED = []  # 차단을 한 번 맞으면 이 회차는 자막을 더 부르지 않는다(더 부르면 차단이 길어진다).

def transcript(vid):
    # 2026-09-28 17시: 부동산 11채널 22편이 전부 '자막 없음'으로 적혔다. 실제로는 ko 자동자막이 있었고
    # youtube_transcript_api 가 IpBlocked, yt-dlp 자막도 429였다. 예외를 삼켜 차단이 '자막 없음'으로 숨었다.
    # 차단은 'BLOCKED' 로 돌려 기록에 그대로 남긴다. 사장님 계정 쿠키로 우회하지 않는다.
    if BLOCKED: return 'BLOCKED'
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        tr = YouTubeTranscriptApi().list(vid).find_transcript(['ko']).fetch()
        return [(round(x.start), x.text) for x in tr]
    except Exception as e:
        n = type(e).__name__
        if n in ('IpBlocked', 'RequestBlocked', 'TooManyRequests') or '429' in str(e):
            BLOCKED.append(n); print('자막 차단:', n, '— 이 회차는 자막을 더 부르지 않는다'); return 'BLOCKED'
        return None

def storyboard(vid):
    try:
        j = json.loads(subprocess.run([sys.executable, '-m', 'yt_dlp', '--js-runtimes', 'node', '-j', f'https://www.youtube.com/watch?v={vid}'], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=120).stdout)
        sb = [f for f in j['formats'] if f.get('format_id') == 'sb0']
        if not sb: return []
        frags = sb[0].get('fragments', []); saved = []
        for i in sorted({0, len(frags) // 2, len(frags) - 1}):
            if i < len(frags):
                b = urllib.request.urlopen(urllib.request.Request(frags[i]['url'], headers=H), timeout=30).read()
                p = os.path.join(OUT, f'sb_{vid}_{i}.jpg'); open(p, 'wb').write(b); saved.append(p)
        return saved
    except Exception: return []

# build-queue 4번: 부동산 상위 채널. 자막에서 '사람들이 궁금해하는 저평가 판단 기준'을 센다.
RE_CHANNELS = [('UC9meL6XNNckzlleWelmO9tQ', '투미TV'), ('UClWhdsAcFX-t5OsBC7yWuSA', '부동산쿨TV'), ('UCMsuAb9v3Q1AB89bB5EFK7A', '하이클래스'),
               ('UCHmXGmj6JA-4iQ1UFMC7LYw', 'KB부동산TV'), ('UC3nsb3SxlRrJQ9egkKNnlfg', '리치고TV'), ('UCaXYdIFec07keCSvEQ87-Bg', '저평가 아파트 발굴단'),
               ('UCEoF-IS2vWlL1MGIMBry5Lw', '아파트써처'), ('UCGzEAhEIZuQA7EibT-W-lCg', '시크릿브라더'), ('UCU09s-DZfqlZsbIm49WbOZw', '김경민의 노트'),
               ('UCjtt1zQiVYuVgtSPyLj9wwA', '오피스텔TV'), ('UCJ6pu5zitBOSNALEnGOSbCw', '월세냄비')]
# 기준 이름 → (자막에서 찾을 말, B10 지표(undervalue.py·offitable.py)에 이미 있나)
RE_CRITERIA = {'전세가율': (r'전세가율|전세 ?비율|갭 ?투자|매매.{0,6}전세.{0,4}차이', '있음'),
               '고점 대비 하락': (r'고점 대비|전고점|최고가 대비|고점에서', '있음'), '평당가': (r'평당|평단가', '있음'),
               '월세 수익률': (r'수익률', '있음'), '공시가격': (r'공시가', '있음'),
               '입주 물량·공급': (r'입주 ?물량|공급 ?물량|공급 ?부족|입주량', '없음'), '거래량': (r'거래량|거래 ?건수', '없음'),
               '미분양': (r'미분양', '없음'), '역세권·교통': (r'역세권|GTX|지하철|노선', '없음'), '학군': (r'학군|학원가', '없음'),
               '신축·연식': (r'신축|구축|연식|준공', '없음'), '재건축·재개발': (r'재건축|재개발|정비사업', '없음'),
               '대장 단지·키 맞추기': (r'대장|키 ?맞추|갭 ?메우', '없음'), '대출·DSR·금리': (r'DSR|LTV|대출|금리', '없음'),
               '소득 대비 가격(PIR)': (r'PIR|소득 대비', '없음'), '인구·일자리': (r'인구|일자리|직주', '없음')}

def re_criteria(texts, day, basis='자막'):
    # texts: [(채널, 제목, 자막 전문)] — 기준마다 몇 영상에서, 모두 몇 번 나왔는지 센다. 센 것만 적는다.
    rows = []
    for name, (pat, have) in RE_CRITERIA.items():
        hits = [(c, ti, len(re.findall(pat, tx))) for c, ti, tx in texts]
        vids = [h for h in hits if h[2]]
        rows.append((len(vids), sum(h[2] for h in hits), name, have, vids[:3]))
    rows.sort(key=lambda r: (r[0], r[1]), reverse=True)
    L = [f'# 부동산 채널 저평가 판단 기준 {day} — {basis} {len(texts)}편', '',
         '| 기준 | 나온 영상 수 | 나온 횟수 | B10 지표 | 예 |', '|---|---|---|---|---|']
    for nv, nn, name, have, ex in rows:
        L.append(f"| {name} | {nv}/{len(texts)} | {nn} | {have} | {' / '.join(f'{c}: {ti[:24]}' for c, ti, _ in ex)} |")
    miss = [r for r in rows if r[3] == '없음' and len(texts) and r[0] >= max(2, len(texts) / 3)]
    L += ['', '## B10 지표에 없는데 자주 나온 기준(영상 3분의 1 이상)', *([f'- {r[2]} — {r[0]}편' for r in miss] or ['- 없음'])]
    p = os.path.join(OUT, f're_criteria_{day}.md'); open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('저장', p)
    return p

def main():
    args = sys.argv[1:]
    channels = []
    RE = bool(args) and args[0] == '--re'
    if RE: args = ['--channels'] + [c for c, _ in RE_CHANNELS]
    names = dict(RE_CHANNELS)
    re_texts = []; re_titles = []
    if args and args[0] == '--channels':
        channels = [({'id': c, 'name': names.get(c, c), 'subs_text': '?', 'handle': None} if c.startswith('UC')
                     else {'id': resolve_handle(c) or c, 'name': c, 'subs_text': '?', 'handle': c}) for c in args[1:]]
    else:
        for q in (args or ['부동산', '미국주식', '배당', '연금', 'ETF']):
            found = search_channels(q); print(f'== "{q}" 상위 채널:', ' · '.join(f"{c['name']}({c['subs_text']})" for c in found))
            for c in found:
                if c['id'] not in [x['id'] for x in channels]: c['q'] = q; channels.append(c)
    day = time.strftime('%Y-%m-%d'); lessons = [f'# 유튜브 학습 {day} — 채널 {len(channels)}개', '']
    words = collections.Counter(); hooks = []; titles_all = []
    for c in channels:
        try: top, titles = channel_videos(c['id'], handle=c.get('handle'))
        except Exception as e: print(c['name'], 'RSS 실패', str(e)[:60]); continue
        titles_all += titles
        import html; re_titles.extend((c['name'], html.unescape(ti), html.unescape(ti)) for ti in titles)
        lessons.append(f"## {c['name']} ({c.get('subs_text','?')}, 검색어 {c.get('q','-')})")
        lessons.append('최근 제목: ' + ' | '.join(t[:40] for t in titles[:8]))
        for v in top:
            segs = transcript(v['id'])
            if segs == 'BLOCKED': lessons.append(f"- {v['title'][:50]} ({v['views']:,}회) — 자막 차단({BLOCKED[0]}, 자막 유무 확인 못 함)"); continue
            if not segs: lessons.append(f"- {v['title'][:50]} ({v['views']:,}회) — 자막 없음"); continue
            open(os.path.join(OUT, f"{c['id'][:8]}_{v['id']}.txt"), 'w', encoding='utf-8').write(f"# {c['name']} | {v['title']} | {v['pub']} | {v['views']}회\n" + '\n'.join(f'{s//60:02d}:{s%60:02d} {t}' for s, t in segs))
            hook = ' '.join(t for s, t in segs if s < 30)[:220]; hooks.append((c['name'], hook))
            re_texts.append((c['name'], v['title'], ' '.join(t for _, t in segs)))
            marks = []
            for mk in (60, 180, 300, 480, 720):
                near = [t for s, t in segs if s >= mk][:2]
                if near: marks.append(f'{mk//60}분: ' + ' '.join(near)[:70])
            for s, t in segs:
                for w in re.findall(r'[가-힣]{2,}', t): words[w] += 1
            sb = storyboard(v['id'])
            lessons.append(f"- **{v['title'][:60]}** ({v['views']:,}회, {segs[-1][0]//60}분, 자막 {sum(len(t) for _,t in segs):,}자)")
            lessons.append(f'  - 훅(0~30초): {hook}')
            for m in marks: lessons.append(f'  - {m}')
            if sb: lessons.append('  - 장면: ' + ', '.join(os.path.basename(p) for p in sb))
        lessons.append('')
    stop = set('그래서 그리고 그런데 지금 이제 우리 여러분 하는 있는 하고 정도 때문에 그냥 이런 이렇게 저는 제가 근데 진짜 그럼 다시 같은 오늘 대한 그게 이거 좀 그 뭐 자 네 예 아 음'.split())
    common = [w for w, _ in words.most_common(300) if w not in stop][:50]
    pats = collections.Counter()
    for t in titles_all:
        if '?' in t: pats['질문형'] += 1
        if re.search(r'\d', t): pats['숫자'] += 1
        if re.search(r'"|“|\'', t): pats['따옴표 인용'] += 1
        if re.search(r'이유|방법|정리|총정리', t): pats['이유·방법·정리'] += 1
        if re.search(r'수혜|기회|위기|폭락|급등|역대', t): pats['자극어'] += 1
    lessons += ['## 제목 패턴(최근 제목 %d개)' % len(titles_all), ' · '.join(f'{k} {v}' for k, v in pats.most_common()), '',
                '## 말하는 방식에서 자주 나온 말', ' · '.join(common), '',
                '## 훅 모음(글 첫 세 줄에 옮길 것)', *[f'- [{n}] {h}' for n, h in hooks]]
    # 하루에 여러 회차가 다른 검색어로 돌기 때문에 'w'로 쓰면 앞 회차 학습이 사라진다(2026-09-23 21시 회차가 배당주 회차분을 덮어썼다).
    NL = chr(10)
    p = os.path.join(OUT, f'lessons_{day}.md')
    head = ('%s%s---%s%s## %s 회차 (검색어 %s)%s' % (NL, NL, NL, NL, time.strftime('%H:%M'), ', '.join(sys.argv[1:]), NL)) if os.path.exists(p) else ''
    with open(p, 'a', encoding='utf-8') as f: f.write(head + NL.join(lessons))
    print('저장', p)
    # 자막이 막힌 날은 최근 제목으로 센다(제목 기준이라고 파일 첫 줄에 밝힌다).
    if RE: re_criteria(re_texts or re_titles, day, '자막' if re_texts else f"제목(자막 차단 {BLOCKED[0] if BLOCKED else '0편'})")
    print('\n'.join(lessons[:12]))

if __name__ == '__main__': main()
