# 롱폼 업로드 + 관문 — ytupload.py(쇼츠용)에 없는 것: 예약 공개(publishAt), 합성 미디어 표시(containsSyntheticMedia), 썸네일(thumbnails.set),
# 그리고 yt-policy-algorithm.md §5.1 관문(C1·C5·C7·C8·C9·C11)을 코드로 막는다. §5.2 판단 5문항 답은 meta.json에 적혀 있어야 올린다.
#   py -3.12 work/ytlong.py gate <ep폴더>            # 관문만(업로드 안 함)
#   py -3.12 work/ytlong.py up <ep폴더>              # 관문 통과 시 업로드 → uploads.jsonl 기록
# ep폴더/meta.json: {"video": mp4, "thumb": png, "title", "desc", "tags": [...], "publishAt": "2026-10-01T19:30:00+09:00",
#                   "synthetic": bool, "veo": bool, "answers": {"q1".."q5"}, "missing": 0}
# 예약 공개는 API 규칙상 privacyStatus=private + publishAt이어야 한다(videos 문서 status.publishAt). 그래서 C11(비공개 금지)은
# "publishAt 없는 private"만 막는다 — 정해진 시각에 자동으로 공개로 바뀌므로 비공개 쌓기가 아니다.
import sys, os, json, re, glob, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
LOOP = os.path.join(HERE, 'research', 'longform', 'loop'); UPL = os.path.join(LOOP, 'uploads.jsonl')
EPS = os.path.join(HERE, 'research', 'longform', 'ep')
BANNED = ['사세요', '사지 마', '무조건', '추천 종목', '수익 보장', '원금 보장', '!!', '전문가인 제가', '제가 추천', '지금 당장', '파세요']
KST = datetime.timezone(datetime.timedelta(hours=9))

def uploads():
    if not os.path.exists(UPL): return []
    return [json.loads(l) for l in open(UPL, encoding='utf-8') if l.strip()]

def body_sentences(md):
    t = open(md, encoding='utf-8').read().split('\n---', 1)[0]
    return [re.sub(r'\s*\(화면.*$', '', l.strip()[2:]).strip() for l in t.splitlines() if l.lstrip().startswith('- ')]

def gate(ep):
    m = json.load(open(os.path.join(ep, 'meta.json'), encoding='utf-8')); bad = []
    # 경쟁 비교 관문(10/2 대역): ep/<편>/compare.md에 3줄(경쟁이 잘하는 것·우리가 따라갈 것·우리가 다르게 할 것)이 있어야 올린다. 이름은 compare.md 하나로 통일
    cp = os.path.join(ep, 'compare.md')
    if not os.path.exists(cp): bad.append('경쟁 비교 compare.md 없음(경쟁 5+ 실측 · 잘하는 것/따라갈 것/다르게 할 것)')
    else:
        ct = open(cp, encoding='utf-8').read()
        miss = [w for w in ('잘하는', '따라갈', '다르게') if w not in ct]
        if miss: bad.append('compare.md 3줄 중 빠짐: ' + '·'.join(miss))
    # 대본 심사 관문(10/5 improve, commitments '경쟁 조사·review 코드 관문'): ep/<편>/review.md에 심사 기록과 통과 판정이 있어야 올린다.
    # D-1은 '평균 7.6 — 통과선 8 미달'인 채 공개 조건을 사람이 따로 챙겼다 → 판정을 코드가 읽는다.
    # 본문의 '통과'는 편집 통과·통과선 등과 섞여 못 믿는다(D-1이 '편집 통과 10/1'로 빠져나감) → 맨 앞이 '판정:'인 줄 하나만 본다.
    #   예) 판정: 통과 — 평균 7.47(통과선 7) · youtube-loop 20:51
    rv = os.path.join(ep, 'review.md')
    if not os.path.exists(rv): bad.append('대본 심사 review.md 없음(심사 3명 점수·판정)')
    else:
        rt = open(rv, encoding='utf-8').read()
        vd = re.findall(r'^\s*\**판정\**\s*[:：](.*)$', rt, re.M)
        if not vd: bad.append("review.md에 '판정: 통과 — 평균 N(통과선 N)' 줄 없음")
        elif not ('통과' in vd[-1] and not re.search(r'미달|보류|미통과|막힘', vd[-1])): bad.append('review.md 마지막 판정이 통과 아님: ' + vd[-1].strip()[:40])
    # C1 롱폼 주 2편·하루 1편(uploads.jsonl 기준, 예약 시각으로 센다)
    if not m.get('publishAt'):  # R-1처럼 칸을 skip해 publishAt이 비면 여기서 죽었다(10/5)
        return m, bad + ['예약 시각(publishAt) 없음']
    pa =datetime.datetime.fromisoformat(m['publishAt'])
    me = m.get('ep', os.path.basename(os.path.normpath(ep)))   # 같은 편 교체 업로드(옛 판은 비공개로 둠)는 편 수로 세지 않는다
    prev = [datetime.datetime.fromisoformat(u['publishAt']) for u in uploads() if u.get('publishAt') and not u.get('replaced') and u.get('ep') != me]
    # 2026-10-02 사장님 지시로 '주 2편' 제한 해제 → 하루 1편만(X-YT-FREQ). 주 7편 넘으면 막는다.
    if sum(1 for p in prev if abs((pa - p).total_seconds()) < 7 * 86400) >= 7: bad.append('C1 롱폼 주 7편 넘음')
    if any(p.astimezone(KST).date() == pa.astimezone(KST).date() for p in prev): bad.append('C1 같은 날 롱폼 2편')
    if not (19 <= pa.astimezone(KST).hour < 21): bad.append('예약 시각이 한국 19~21시 밖')
    if pa < datetime.datetime.now(KST) + datetime.timedelta(minutes=20): bad.append('예약 시각이 너무 가깝거나 지났다')
    # C5 이전 편 대본과 같은 문장 20% 초과(첫·끝 문장 제외)
    mine = body_sentences(os.path.join(ep, 'script.md'))[1:-1]
    others = set()
    for s in glob.glob(os.path.join(EPS, '*', 'script.md')):
        if os.path.abspath(os.path.dirname(s)) != os.path.abspath(ep): others |= set(body_sentences(s))
    same = sum(1 for s in mine if s in others)
    if mine and same / len(mine) > 0.2: bad.append(f'C5 이전 편과 같은 문장 {same}/{len(mine)}')
    # C7 금지 표현(제목·설명·대본)
    txt = m['title'] + '\n' + m['desc'] + '\n' + '\n'.join(mine)
    hit = [w for w in BANNED if w in txt]
    if hit: bad.append('C7 금지 표현 ' + ','.join(hit))
    if re.search(r'\b[A-Z]{5,}\b', m['title']) and not re.search(r'\b(KODEX|TIGER)\b', m['title']): bad.append('C7 제목 전부 대문자 단어')
    # C8 AI 공개
    if m.get('veo') and not m.get('synthetic'): bad.append('C8 Veo 사용인데 합성 미디어 표시 없음')
    # C9 설명란
    d = m['desc']
    if '출처' not in d: bad.append('C9 출처 줄 없음')
    if len(re.findall(r'cafe\.naver\.com', d)) > 1: bad.append('C9 카페 링크 2개 이상')
    if not (3 <= len(m['tags']) <= 5): bad.append('C9 태그 3~5개 아님')
    ch = re.findall(r'^(\d+):(\d\d) ', d, flags=re.M)
    secs = [int(a) * 60 + int(b) for a, b in ch]
    if len(secs) < 3 or secs[0] != 0 or any(b - a < 10 for a, b in zip(secs, secs[1:])): bad.append('C9 챕터(00:00 시작·3개 이상·10초 이상)')
    if 'AI 음성' not in d: bad.append('AI 음성 내레이션 명시 없음')
    for u in uploads():
        if u.get('replaced') or u.get('ep') == m.get('ep', os.path.basename(os.path.normpath(ep))): continue  # 같은 편 교체본·자기 자신은 비교 안 함
        a, b = set(d.split()), set(u.get('desc', '').split())
        if a and len(a & b) / len(a) > 0.8: bad.append('C9 설명이 이전 편과 80% 넘게 같다')
    # C11 · 목소리 빠짐 · 5문항
    if m.get('privacy', 'private') == 'private' and not m.get('publishAt'): bad.append('C11 예약 없는 비공개')
    if m.get('missing', 1): bad.append(f'목소리 없는 문장 {m.get("missing")}개')
    ans = m.get('answers', {})
    if len(ans) < 5 or any(not str(v).strip() for v in ans.values()): bad.append('§5.2 판단 5문항 답 없음')
    for f in ('video', 'thumb'):
        if not os.path.exists(os.path.join(ep, m[f]) if not os.path.isabs(m[f]) else m[f]): bad.append(f'{f} 파일 없음')
    # 목소리 '치익'(ㅅ·ㅊ 쉿소리) — 2026-10-01 사장님 "치익~ 하는 소리 너무 거슬린다". 렌더 뒤 video/deess.py 거친 파일만(RULES 4. 소리)
    vp = os.path.join(ep, m['video']) if not os.path.isabs(m['video']) else m['video']
    if os.path.exists(vp):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video')); import deess
        r = deess.measure(vp)
        if r and r['sib_vs_voiced_db'] > deess.LIMIT_DB: bad.append(f'쉿소리 {r["sib_vs_voiced_db"]}dB > {deess.LIMIT_DB}dB — py -3.12 work/video/deess.py <영상>')
    # 말 끝난 직후 '치직' — 10/02 사장님 "유튜브 말 끝나고 치직 했는데". TTS 응답 끝 잡음이 문장 wav에 남았는지(렌더 전 원천 검사, work/video/clickscan.py)
    import glob as _g
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video')); import clickscan
    ad = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video', 'public', 'audio', os.path.basename(os.path.normpath(ep)).lower())
    n = mute = 0
    for f in _g.glob(os.path.join(ad, '*.wav')):
        a_, sr_ = clickscan.load(f); n += len(clickscan.bursts(a_, sr_)); mute += int(abs(a_).max() < 1000)
    if mute: bad.append(f'문장 wav 무음 {mute}개')
    if n: bad.append(f'문장 wav 치직 {n}곳 — py -3.12 work/video/clickscan.py fix {ad} 뒤 다시 렌더')
    # 목소리 한결같음 — 10/3 22시 사장님 "뒤쪽에 다른 목소리". f0 ±12%·빠르기 1.0·한 날 녹음(lfvoice check 규칙 3·4)
    if os.path.exists(os.path.join(ep, 'voice.json')):
        import io, contextlib, importlib; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); lfv = importlib.import_module('lfvoice')
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            okv = lfv.check(ep)
        if not okv: bad.append('목소리 한결같음 막힘 — py -3.12 work/lfvoice.py check ' + ep + ' | ' + buf.getvalue().strip().splitlines()[-1])
    return m, bad

def up(ep):
    m, bad = gate(ep)
    if bad: print('관문 막힘:', *bad, sep='\n  '); sys.exit(3)
    from ytupload import service
    from googleapiclient.http import MediaFileUpload
    yt = service(); p = lambda f: m[f] if os.path.isabs(m[f]) else os.path.join(ep, m[f])
    title, desc = [x.replace('<', '＜').replace('>', '＞') for x in (m['title'], m['desc'])]
    body = {'snippet': {'title': title[:100], 'description': desc[:5000], 'tags': m['tags'], 'categoryId': '27', 'defaultLanguage': 'ko', 'defaultAudioLanguage': 'ko'},
            'status': {'privacyStatus': 'private', 'publishAt': datetime.datetime.fromisoformat(m['publishAt']).astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                       'selfDeclaredMadeForKids': False, 'containsSyntheticMedia': bool(m.get('synthetic')),
                       'embeddable': True, 'publicStatsViewable': True, 'license': 'youtube'}}   # 교훈 13: status 칸 전부 명시
    import ytplaceholder   # 자리표시자 관문(10/5): VIDEOID는 올린 뒤 실제 ID로, 나머지는 막음
    other = [x for x in ytplaceholder.find(title + '\n' + desc) if x != 'VIDEOID']
    if other: print('관문 막힘: 자리표시자', other); sys.exit(3)
    notes = []; part = 'snippet,status'
    if m.get('paid') or 'link.coupang.com' in desc:     # 쿠팡 링크 = '유료 프로모션 포함' 표시(ytupload.py와 같은 규칙)
        body['paidProductPlacementDetails'] = {'hasPaidProductPlacement': True}; part += ',paidProductPlacementDetails'
    req = yt.videos().insert(part=part, body=body, media_body=MediaFileUpload(p('video'), chunksize=8 * 1024 * 1024, resumable=True))
    res = None
    while res is None:
        st, res = req.next_chunk()
        if st: print(f'업로드 {int(st.progress() * 100)}%', flush=True)
    vid = res['id']; print('완료 https://youtu.be/' + vid)
    try: import ytupload; ytupload.fill_videoid(yt, vid, body['snippet'])
    except Exception as e: notes.append('VIDEOID 치환 실패 ' + str(e)[:120])
    try: yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(p('thumb'))).execute(); notes.append('썸네일 설정')
    except Exception as e: notes.append('썸네일 실패 ' + str(e)[:120])
    v = yt.videos().list(part='status,snippet', id=vid).execute()['items'][0]['status']
    rec = {'ep': os.path.basename(os.path.normpath(ep)), 'videoId': vid, 'title': m['title'], 'publishAt': m['publishAt'], 'desc': m['desc'],
           'status': v, 'answers': m['answers'], 'notes': notes, 'at': datetime.datetime.now(KST).isoformat(timespec='minutes')}
    open(UPL, 'a', encoding='utf-8').write(json.dumps(rec, ensure_ascii=False) + '\n')
    print(json.dumps({'videoId': vid, 'status': v, 'notes': notes}, ensure_ascii=False))

if __name__ == '__main__':
    cmd, ep = sys.argv[1], os.path.abspath(sys.argv[2])
    if cmd == 'gate':
        m, bad = gate(ep); print('통과' if not bad else '막힘:\n  ' + '\n  '.join(bad))
    elif cmd == 'up': up(ep)
