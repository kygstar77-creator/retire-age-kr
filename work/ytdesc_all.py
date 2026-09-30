# 설명란 한 번에 적용(2026-10-01) — 롱폼 설명란에 걸린 세 가지 변경을 영상마다 videos.update 1번으로 합친다.
#   ① 편집자 원고(research/editor/2026-10-01/ytdesc/<id>.txt) — 지금 설명이 <id>.txt.orig와 같을 때만 바꾼다.
#      다르면(남이 먼저 고쳤으면) 지금 설명을 그대로 두고 ②③만 얹는다.
#   ② R2 계산기 utm 링크(calc_links.new_desc 그대로 — 첫 문단 뒤 '▶ 내 은퇴 나이 계산하기', 아래 맨 주소도 같은 utm)
#   ③ F2 쿠팡 줄(f2_plan.json에 link.coupang.com 링크가 있을 때만) — 맨 위 대가성 문구 + 링크, '유료 프로모션 포함' 켬
#   py -3.12 work/ytdesc_all.py dry     # 아무것도 안 바꿈. 미리 보기 research/longform/loop/ytdesc_all_dry.md
#   py -3.12 work/ytdesc_all.py apply   # 적용 전 원본 ytdesc_all_before.json, 되읽기 ytdesc_all_after.json
# 쓰기 권한 토큰은 f2_coupang.py(youtube.force-ssl)를 쓴다. 쿠팡 링크가 비어 있으면 ③만 건너뛰고 ①②는 적용한다
# — 쿠팡 발급 뒤 다시 돌리면 ①②는 '이미 적용'으로 넘어가고 ③만 붙는다(여러 번 돌려도 같은 결과).
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ytupload, aitell, calc_links, f2_coupang
ED = os.path.join(HERE, 'research', 'editor', '2026-10-01', 'ytdesc')
LOOP = os.path.join(HERE, 'research', 'longform', 'loop')
DRY, BEFORE, AFTER = [os.path.join(LOOP, f'ytdesc_all_{x}') for x in ('dry.md', 'before.json', 'after.json')]
CALC_IDS = set(calc_links.IDS)
PLAN = {p['id']: p for p in json.load(open(f2_coupang.PLAN, encoding='utf-8'))['videos'] if not p.get('skip')}
IDS = list(PLAN)  # 롱폼 7편(A-1 + 6편). 쇼츠는 f2_plan에서 skip.

def norm(s): return '\n'.join(l.rstrip() for l in s.replace('\r\n', '\n').strip().split('\n'))

def facts(s):
    """편집자 약속('면책·숫자·링크·해시태그는 한 글자도 안 바꿨다')을 기계로 대조할 조각들."""
    # 값의 종류로 견준다 — 같은 숫자가 한 번 덜 나오는 건(겹친 문장 삭제) 사실 변경이 아니다(scV67BQvC4Q '5억' 14→13회).
    urls = sorted(set(re.findall(r'https?://\S+|firemap\.kr\S*', s)))
    tags = sorted(set(re.findall(r'#\S+', s)))
    nums = sorted(set(re.findall(r'\d[\d,.]*', re.sub(r'https?://\S+', '', s))))
    return urls, tags, nums

def editor_base(vid, cur):
    t, o = os.path.join(ED, vid + '.txt'), os.path.join(ED, vid + '.txt.orig')
    if not os.path.exists(t): return cur, '편집 원고 없음'
    new, orig = open(t, encoding='utf-8').read(), open(o, encoding='utf-8').read()
    if norm(cur) == norm(new): return cur, '편집 이미 적용'
    if norm(cur) != norm(orig): return cur, '지금 설명이 .orig와 다름 — 편집 원고 안 씀(②③만)'
    fo, fn = facts(orig), facts(new)
    bad = [k for k, a, b in zip(('링크', '해시태그', '숫자'), fo, fn) if a != b]
    if bad: return cur, f'편집 원고의 {"·".join(bad)}가 원본과 다름 — 편집 원고 안 씀'
    return new.strip(), '편집 원고 적용'

def build(vid, cur):
    notes = []
    d, n = editor_base(vid, cur); notes.append(n)
    if vid in CALC_IDS:
        c = calc_links.new_desc(d, vid)
        if c is None: notes.append('계산기 링크 이미 있음')
        else: d = c; notes.append('계산기 링크 추가')
    p = PLAN.get(vid, {}); link = p.get('link', ''); paid = False
    if link.startswith('https://link.coupang.com/'):
        c = f2_coupang.new_desc(d, link, p['label'])
        if c is None: notes.append('쿠팡 줄 이미 있음')
        else: d = c; notes.append('쿠팡 줄 추가')
        paid = True
    else: notes.append('쿠팡 링크 미발급 — 쿠팡 줄 보류')
    if d.startswith(ytupload.COUPANG_NOTE): paid = True
    return d.replace('<', '＜').replace('>', '＞'), paid, notes

def gates(d, paid, from_editor):
    errs = []
    if len(d) > 5000: errs.append('5000자 넘음')
    if 'coupang.com' in d and (ytupload.COUPANG_NOTE not in d.strip().splitlines()[0] or not paid):
        errs.append('쿠팡 링크가 있는데 첫 줄 대가성 문구 또는 유료 표시 없음')
    plain = re.sub(r'https?://\S+', ' ', d.replace(ytupload.COUPANG_NOTE, ''))
    ok, msg, hits = aitell.gate_text(plain, from_editor or os.environ.get('FIREMAP_EDITOR_OK') == '1')
    if not ok: errs.append(msg + ' ' + ' / '.join(map(str, hits[:3])))
    return errs, msg

def main(mode):
    yt = f2_coupang.service() if mode == 'apply' else ytupload.service()
    out, before, after = [f'# 설명란 합치기 미리 보기 ({mode})\n'], [], []
    for vid in IDS:
        v = yt.videos().list(part='snippet,status,paidProductPlacementDetails', id=vid).execute()['items'][0]
        sn = v['snippet']; cur = sn['description']
        new, paid, notes = build(vid, cur)
        errs, ai = gates(new, paid, '편집 원고 적용' in notes or '편집 이미 적용' in notes)
        same = norm(new) == norm(cur)
        print('---', vid, sn['title'][:36], '|', ' · '.join(notes), '|', ai, '|', '변경 없음' if same else f'{len(cur)}→{len(new)}자', '| 막힘: ' + '; '.join(errs) if errs else '')
        out += [f'\n## {vid} — {sn["title"]}\n', f'- {" · ".join(notes)} · {ai} · 유료 표시 {"켬" if paid else "그대로"}' + (f' · **막힘: {"; ".join(errs)}**' if errs else '') + '\n',
                '\n```\n' + (new if not same else '(변경 없음)') + '\n```\n']
        if mode != 'apply' or same or errs: continue
        before.append({'id': vid, 'snippet': sn, 'paid': v.get('paidProductPlacementDetails')})
        json.dump(before, open(BEFORE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)  # 한 편마다 먼저 저장
        body = {'id': vid, 'snippet': {'title': sn['title'], 'description': new, 'categoryId': sn['categoryId'],
                                       'tags': sn.get('tags', []), 'defaultLanguage': sn.get('defaultLanguage', 'ko')}}
        if sn.get('defaultAudioLanguage'): body['snippet']['defaultAudioLanguage'] = sn['defaultAudioLanguage']
        part = 'snippet'
        if paid: body['paidProductPlacementDetails'] = {'hasPaidProductPlacement': True}; part += ',paidProductPlacementDetails'
        yt.videos().update(part=part, body=body).execute()
        chk = yt.videos().list(part='snippet,paidProductPlacementDetails', id=vid).execute()['items'][0]
        ok = (norm(chk['snippet']['description']) == norm(new) and chk['snippet']['title'] == sn['title']
              and chk['snippet'].get('tags', []) == sn.get('tags', [])
              and (not paid or chk.get('paidProductPlacementDetails', {}).get('hasPaidProductPlacement')))
        print('되읽기', 'OK' if ok else '불일치')
        after.append({'id': vid, 'ok': bool(ok), 'notes': notes, 'paid': chk.get('paidProductPlacementDetails')})
        json.dump(after, open(AFTER, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if mode != 'apply': open(DRY, 'w', encoding='utf-8').write(''.join(out)); print('미리 보기:', DRY)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'dry')
