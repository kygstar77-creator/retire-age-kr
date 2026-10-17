# 롱폼 업로드 + 관문 — ytupload.py(쇼츠용)에 없는 것: 예약 공개(publishAt), 합성 미디어 표시(containsSyntheticMedia), 썸네일(thumbnails.set),
# 그리고 yt-policy-algorithm.md §5.1 관문(C1·C5·C7·C8·C9·C11)을 코드로 막는다. §5.2 판단 5문항 답은 meta.json에 적혀 있어야 올린다.
#   py -3.12 work/ytlong.py gate <ep폴더>            # 관문만(업로드 안 함)
#   py -3.12 work/ytlong.py up <ep폴더>              # 관문 통과 시 업로드 → uploads.jsonl 기록
#   py -3.12 work/ytlong.py up <ep폴더> --replace <옛 videoId>   # 같은 편 새 판(옛 판은 비공개로 따로 정리) — 없으면 중복 검사가 막는다
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

def order_warn(pa, me):
    """slots.json 롱폼 칸 중 지금~pa 사이에 있는데 uploads.jsonl에 없는 편(앞 칸 미업로드) — 10/17 회의 체크리스트 52"""
    try:
        sl = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', 'slots.json'), encoding='utf-8'))
    except Exception as e:
        return [f'slots.json 못 읽음 {e}']
    done = {u.get('ep') for u in uploads() if not u.get('replaced')}
    now = datetime.datetime.now(KST); out = []
    for x in (sl.get('slots', []) if isinstance(sl, dict) else sl):
        if x.get('kind') not in ('long', 'longform', '롱폼'): continue
        try: t = datetime.datetime.fromisoformat(x.get('due') or x.get('at') or x.get('time'))
        except Exception: continue
        if t.tzinfo is None: t = t.replace(tzinfo=KST)
        it = str(x.get('item', ''))
        if now < t < pa and it and me not in it and not any(e and e in it for e in done) and '비움' not in it:
            out.append(f'{t:%m/%d %H:%M} {it} 아직 안 올라감')
    return out


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
    # 대본 AI 티(10/17 PD): N-2가 `aitell.py script` 실패('1할'·'1할 5푼')인 채 예약까지 갔다 — ytupload는 제목·설명만, 이 관문은 대본을 안 봤다.
    import aitell
    try:
        ok_s, _, _, _, bad_s = aitell.script_check(aitell.script_text(ep))
        hab = aitell.script_habits(aitell.script_lines(ep), aitell.script_lines(ep, 'say'))
        if not ok_s or hab: bad.append('대본 aitell script 실패 — ' + ' · '.join(bad_s[:3] + [f'말 습관 {len(hab)}건'] * bool(hab)) + f' — py -3.12 work/aitell.py script {ep}')
    except Exception as e:
        bad.append(f'대본 aitell script 못 돌림({e})')
    rv = os.path.join(ep, 'review.md')
    if not os.path.exists(rv): bad.append('대본 심사 review.md 없음(심사 3명 점수·판정)')
    else:
        rt = open(rv, encoding='utf-8').read()
        vd = re.findall(r'^\s*\**판정\**\s*[:：](.*)$', rt, re.M)
        if not vd: bad.append("review.md에 '판정: 통과 — 평균 N(통과선 N)' 줄 없음")
        elif not ('통과' in vd[-1] and not re.search(r'미달|보류|미통과|막힘', vd[-1])): bad.append('review.md 마지막 판정이 통과 아님: ' + vd[-1].strip()[:40])
    # 10/11 사장님 "잘된 동영상 비교해서 만들기로 했는데 왜 안 했어?" — 분석(10/11 gap 파일들)과 대조하지 않은 편은 못 올린다.
    #   ep/<편>/bench_check.md: 제목·썸네일·첫 60초·자막·대본 각각 [잘된 예 ID·근거 파일 → 우리 편 → 맞춤/안 맞춤] 표 + 맨 끝 '대조: 통과' 줄.
    # 10/15 사장님 "유튜브도 카페도 쉽게 설명해 주고 쉽게 이해되게 써야 할 거 아니야" — 점수 관문은 '이해되는가'를 안 쟀다
    #   (P-1 썸네일 7.23 통과 → 사장님이 읽고 이해 못 함). 처음 보는 심사관이 제목·썸네일·대본 각 장을 한 문장으로 다시 말해 뜻이 맞아야 올린다.
    #   ep/<편>/understand_test.md: 항목마다 [보여 준 것 → 심사관 한 문장 → 맞음/틀림·헷갈린 곳 → 고친 것] + 맨 끝 '판정: 통과'.
    import research_gate
    bad += research_gate.research_check(os.path.join(ep, 'research.md'))
    ut = os.path.join(ep, 'understand_test.md')
    if not os.path.exists(ut): bad.append('understand_test.md 없음 — 처음 보는 사람 이해 시험(제목·썸네일·대본) 없이 못 올림')
    else:
        utt = open(ut, encoding='utf-8').read()
        miss_u = [k for k in ('제목', '썸네일', '대본') if k not in utt]
        vd3 = re.findall(r'^\s*\**판정\**\s*[:：](.*)$', utt, re.M)
        if miss_u: bad.append('understand_test.md에 빠진 항목: ' + '·'.join(miss_u))
        if not vd3 or '통과' not in vd3[-1] or re.search(r'미달|보류|미통과|틀림', vd3[-1]): bad.append("understand_test.md 마지막 '판정: 통과' 줄 없음")
    bc = os.path.join(ep, 'bench_check.md')
    if not os.path.exists(bc): bad.append('bench_check.md 없음 — 잘된 영상 대조(제목·썸네일·첫 60초·자막·대본) 없이 못 올림')
    else:
        bt = open(bc, encoding='utf-8').read()
        miss = [k for k in ('제목', '썸네일', '첫 60초', '자막', '대본') if k not in bt]
        vd2 = re.findall(r'^\s*\**대조\**\s*[:：](.*)$', bt, re.M)
        if miss: bad.append('bench_check.md에 빠진 항목: ' + '·'.join(miss))
        if not vd2 or '통과' not in vd2[-1] or re.search(r'미달|보류|미통과', vd2[-1]): bad.append("bench_check.md 마지막 '대조: 통과' 줄 없음")
        tt = m.get('title', ''); tn = len(re.findall(r'\d[\d,.]*', tt))
        if tn > 2: bad.append(f'제목 숫자 {tn}개 — 조회 1만+ 롱폼 108편 중앙 1개(10/11 실측), 2개 이하로')
    # C1 롱폼 주 2편·하루 1편(uploads.jsonl 기준, 예약 시각으로 센다)
    if not m.get('publishAt'):  # R-1처럼 칸을 skip해 publishAt이 비면 여기서 죽었다(10/5)
        return m, bad + ['예약 시각(publishAt) 없음']
    pa =datetime.datetime.fromisoformat(m['publishAt'])
    me = m.get('ep', os.path.basename(os.path.normpath(ep)))   # 같은 편 교체 업로드(옛 판은 비공개로 둠)는 편 수로 세지 않는다
    prev = [datetime.datetime.fromisoformat(u['publishAt']) for u in uploads() if u.get('publishAt') and not u.get('replaced') and u.get('ep') != me]
    # 2026-10-02 사장님 지시로 '주 2편' 제한 해제 → 하루 1편만(X-YT-FREQ). 주 7편 넘으면 막는다.
    if sum(1 for p in prev if abs((pa - p).total_seconds()) < 7 * 86400) >= 7: bad.append('C1 롱폼 주 7편 넘음')
    if any(p.astimezone(KST).date() == pa.astimezone(KST).date() for p in prev): bad.append('C1 같은 날 롱폼 2편')
    # 10/17 회의(체크리스트 52): 롱폼은 날짜 순서로만 — 앞 칸(slots 롱폼, 이 편보다 이른 미래 칸)이 아직 안 올라갔으면 경고
    for w in order_warn(pa, me): print('[경고] 날짜 순서:', w)
    # 10/11 10:2x 사장님: 롱폼 정규 시각 매일 11:30(전 19:30). 그날 밀린 편은 관문을 다 넘는 즉시 공개 → 한국 11~21시만 허용(새벽·밤 공개는 계속 막음)
    if not (11 <= pa.astimezone(KST).hour < 21): bad.append('예약 시각이 한국 11~21시 밖')
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
    # 10/17 회의(체크리스트 51): AI 목소리 편은 Veo가 없어도 합성 표시 True — 설명란 'AI 음성'이 있으면 곧 AI 목소리 편
    if not m.get('synthetic') and 'AI 음성' in m.get('desc', ''): bad.append('C8 AI 목소리 편인데 합성 미디어 표시(synthetic) 없음')
    # C9 설명란
    d = m['desc']
    if '출처' not in d: bad.append('C9 출처 줄 없음')
    import disclaim   # 10/14 회의 지시: 영상 끝 면책(A23)을 뺀 대신 설명란 '권유 아님' 줄 필수
    if not disclaim.line(d): bad.append(disclaim.NEED)
    if len(re.findall(r'cafe\.naver\.com', d)) > 1: bad.append('C9 카페 링크 2개 이상')
    # 10/17 회의(레드팀 R3): 짝 카페 글 주소는 설명 첫 5줄 안(접힘 위) — 없으면 cafe.naver.com/firemap
    if '{CAFE}' in d: bad.append('C9 설명에 {CAFE} 그대로 — 짝 카페 글 주소로 바꿔야 함(글이 아직 없으면 cafe.naver.com/firemap)')
    if not re.search(r'cafe\.naver\.com|\{CAFE\}', ' '.join(d.splitlines()[:5])): bad.append('C9 설명 첫 5줄에 카페 줄 없음(짝 글 주소, 없으면 cafe.naver.com/firemap)')
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
        if not m.get(f): bad.append(f'meta.json에 {f} 칸 없음'); m[f] = ''; continue
        if not os.path.exists(os.path.join(ep, m[f]) if not os.path.isabs(m[f]) else m[f]): bad.append(f'{f} 파일 없음')
    # 목소리 '치익'(ㅅ·ㅊ 쉿소리) — 2026-10-01 사장님 "치익~ 하는 소리 너무 거슬린다". 렌더 뒤 video/deess.py 거친 파일만(RULES 4. 소리)
    vp = os.path.join(ep, m['video']) if not os.path.isabs(m['video']) else m['video']
    if m['video'] and os.path.isfile(vp):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video')); import deess
        r = deess.measure(vp)
        if r and r['sib_vs_voiced_db'] > deess.LIMIT_DB: bad.append(f'쉿소리 {r["sib_vs_voiced_db"]}dB > {deess.LIMIT_DB}dB — py -3.12 work/video/deess.py <영상>')
        # 10/17 롱폼 화면 기준(research/longform/visual-gap-1017.md 7절): 실사 10%↑·컷 분당 3↑·같은 판 20초↓·판 큰 글자 9%↑·판 글자 8줄↓ — work/bgcheck.py
        #   (10/16 v3 '모든 장면 뒤 실사 배경'은 롱폼에서 뺐다. 쇼츠는 v3 그대로)
        import bgcheck
        ok_bg, msg_bg = bgcheck.gate(vp)
        if not ok_bg: bad.append(msg_bg + ' — 판(TallyFrame 큰 제목·art)과 꽉 찬 실사(TallyBroll·StockShot)를 번갈아 다시 렌더')
    # 말 끝난 직후 '치직' — 10/02 사장님 "유튜브 말 끝나고 치직 했는데". TTS 응답 끝 잡음이 문장 wav에 남았는지(렌더 전 원천 검사, work/video/clickscan.py)
    import glob as _g
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video')); import clickscan
    ad = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video', 'public', 'audio', os.path.basename(os.path.normpath(ep)).lower())
    n = mute = 0
    for f in _g.glob(os.path.join(ad, '*.wav')):
        a_, sr_ = clickscan.load(f); n += len(clickscan.bursts(a_, sr_)); mute += int(abs(a_).max() < 1000)
    if mute: bad.append(f'문장 wav 무음 {mute}개')
    if n: bad.append(f'문장 wav 치직 {n}곳 — py -3.12 work/video/clickscan.py fix {ad} 뒤 다시 렌더')
    # 10/6 순돌이: 문장 wav만 보고 완성 영상은 안 봤다 — 공개된 E-2(347.8·368.4초)·N-1(57.5·363.9초) 완성본에서 검사기가 4곳을 잡았다(귀 확인 안 함). 완성 영상도 본다.
    if m['video'] and os.path.isfile(vp):
        a_, sr_ = clickscan.load(vp); ok_ = m.get('click_ok', [])   # 들어서 말소리로 확인한 자리(초)만 meta.json click_ok에 — 누가 어떻게 들었는지 click_ok_note에
        fb = [b for b in clickscan.bursts(a_, sr_) if not any(abs(b[0] / sr_ - x) < 0.3 for x in ok_)]
        # 10/17 사장님 "롱폼도 갈수록 수페tv처럼 알차게 만드는 게 아니라 대충 하는 거 같애" — 실측: 우리 최근 롱폼 2:15~6:41,
        #   수페TV 최근 30편 길이 중앙 17.1분·월급쟁이부자들 17.7분. 8분 아래 롱폼은 못 올린다.
        if len(a_) / sr_ < 8 * 60: bad.append(f'롱폼 길이 {len(a_)/sr_/60:.1f}분 — 8분 이상(경쟁 중앙 17분). research.md 질문·예외·우리만 숫자를 대본에 더 담는다')
        if fb: bad.append('완성 영상 치직 의심 ' + ', '.join(f'{s/sr_:.1f}초' for s, _, _ in fb[:8]) + ' — 그 자리 1초를 들어 보고(제미나이 듣기 또는 사람) 말소리가 아니면 문장 wav를 고쳐 다시 렌더')
    # 목소리 한결같음 — 10/3 22시 사장님 "뒤쪽에 다른 목소리". f0 ±12%·빠르기 1.0·한 날 녹음(lfvoice check 규칙 3·4)
    if os.path.exists(os.path.join(ep, 'voice.json')):
        import io, contextlib, importlib; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); lfv = importlib.import_module('lfvoice')
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            okv = lfv.check(ep)
        if not okv: bad.append('목소리 한결같음 막힘 — py -3.12 work/lfvoice.py check ' + ep + ' | ' + buf.getvalue().strip().splitlines()[-1])
    return m, bad

def dup_check(ep, m, replace=None):
    # 교훈 31·체크리스트 41(10/12 회의): W-1 같은 판을 두 회차가 따로 올려 중복 영상(0yWQ·dPrE). 배차 메시지가 아니라 장부를 믿는다.
    #   uploads.jsonl에 같은 편의 살아 있는(replaced 없는) 줄, slots.json에 같은 편이나 같은 칸(publishAt 시각)의 published가 있으면 멈춘다.
    #   새 판으로 바꾸는 게 맞으면 --replace <옛 videoId>로 그 하나만 허용한다.
    me = m.get('ep', os.path.basename(os.path.normpath(ep))); bad = []
    for u in uploads():
        if u.get('ep') == me and not u.get('replaced') and u.get('videoId') != replace:
            bad.append(f"중복: uploads.jsonl에 {me} {u.get('videoId')}({u.get('publishAt')}) 이미 있음 — 새 판이면 --replace {u.get('videoId')}")
    sp = os.path.join(HERE, 'research', 'slots.json')
    if os.path.exists(sp) and m.get('publishAt'):
        at = datetime.datetime.fromisoformat(m['publishAt']).astimezone(KST).strftime('%Y-%m-%d %H:%M')
        for x in json.load(open(sp, encoding='utf-8')).get('slots', []):
            if x.get('kind') != 'long' or not x.get('published'): continue
            if x.get('item') == me or x.get('ep') == me or x.get('at') == at:
                pub = str(x['published'])
                if replace and replace in pub: continue
                bad.append(f"중복: slots.json {x.get('at')} {x.get('item')} published 있음 — {pub[:70]}")
    return bad

def up(ep, replace=None):
    m, bad = gate(ep)
    bad += dup_check(ep, m, replace)
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
    if replace:   # 옛 판 줄에 replaced 표시 — C1 같은 날 2편·중복 검사가 옛 판을 세지 않게
        ls = [json.loads(l) for l in open(UPL, encoding='utf-8') if l.strip()]
        for u in ls:
            if u.get('videoId') == replace and not u.get('replaced'): u['replaced'] = vid
        open(UPL, 'w', encoding='utf-8').write(''.join(json.dumps(u, ensure_ascii=False) + '\n' for u in ls))
    open(UPL, 'a', encoding='utf-8').write(json.dumps(rec, ensure_ascii=False) + '\n')
    print(json.dumps({'videoId': vid, 'status': v, 'notes': notes}, ensure_ascii=False))

def preview(ep, vid):
    # 10/16 감사 경미 ②(썸네일 규칙 3): 공개 뒤 실제 걸린 썸네일을 앱 목록 크기(412px·168px)로 줄이고 길이 표시 자리(오른쪽 아래 검은 칸)를 얹어
    #   ep/<편>/app_preview.png로 남긴다 — 감사가 대신 만든 P-1 app_preview_1016_audit.png와 같은 꼴. 큰 줄이 168px에서 읽히는지·길이 칸이 글자를 가리는지 눈으로 본다.
    import io, urllib.request
    from PIL import Image, ImageDraw
    img = None
    for q in ('maxresdefault', 'sddefault', 'hqdefault'):
        try: img = Image.open(io.BytesIO(urllib.request.urlopen(f'https://i.ytimg.com/vi/{vid}/{q}.jpg', timeout=20).read())).convert('RGB'); break
        except Exception: continue
    if img is None: sys.exit('썸네일 못 받음 ' + vid)
    W, H = 900, 420; out = Image.new('RGB', (W, H), (15, 15, 15)); x = 20
    for w in (412, 168):
        t = img.resize((w, round(w * img.height / img.width)), Image.LANCZOS); d = ImageDraw.Draw(t)
        bw, bh = round(w * 0.095), round(w * 0.045); d.rectangle([w - bw - round(w * 0.012), t.height - bh - round(w * 0.012), w - round(w * 0.012), t.height - round(w * 0.012)], fill=(0, 0, 0))
        out.paste(t, (x, 20)); x += w + 28
    fp = os.path.join(ep, 'app_preview.png'); out.save(fp); print('저장', fp, '— Read로 열어 168px에서 큰 줄이 읽히는지·길이 칸이 글자를 가리는지 본다')

if __name__ == '__main__':
    cmd, ep = sys.argv[1], os.path.abspath(sys.argv[2])
    if cmd == 'gate':
        m, bad = gate(ep); print('통과' if not bad else '막힘:\n  ' + '\n  '.join(bad))
    elif cmd == 'up': up(ep, sys.argv[sys.argv.index('--replace') + 1] if '--replace' in sys.argv else None)
    elif cmd == 'preview': preview(ep, sys.argv[3])   # 공개 뒤: py -3.12 work/ytlong.py preview <ep폴더> <videoId>
    elif cmd == 'dup':   # 중복 검사만
        m = json.load(open(os.path.join(ep, 'meta.json'), encoding='utf-8')); b = dup_check(ep, m, sys.argv[sys.argv.index('--replace') + 1] if '--replace' in sys.argv else None)
        print('중복 없음' if not b else chr(10).join(b))
