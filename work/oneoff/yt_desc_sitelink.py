"""설명란에 firemap.kr 링크가 없는 공개 쇼츠 6편에 주제에 맞는 화면 + utm 한 줄을 더한다(today.md 10/5 firemap-loop 지시).
snippet 통째로 받아 description만 바꿔 보낸다(교훈 18, defaultAudioLanguage 유지). 백업: longform/loop/desc_before_<id>.json
/calc/* 세 개(연봉·퇴직금·실업급여)는 이 6편 주제와 맞지 않아 같은 주제의 도구 화면을 쓴다(toolPages.js 제목 그대로)."""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
import f2_coupang
D = os.path.join(os.path.dirname(__file__), 'research', 'longform', 'loop')
U = 'utm_source=youtube&utm_medium=desc&utm_campaign='
PLAN = {
 'INvS3EzWelY': ('내 나이·모은 돈에 낙폭 넣어 보기(파이어맵 은퇴 계산기)', '/'),
 'lNqM_tai2H4': ('파이어 후 건보료 계산(파이어맵)', '/health-insurance'),
 'DNpdFtZyfE8': ('계산하면 내 등수가 나와요(파이어맵 랭킹)', '/ranking'),
 'P8Papm8Yxpw': ('부동산·부채 넣어 은퇴 나이 바꿔보기(파이어맵)', '/experiment'),
 'KiHLbeioWNg': ('예금 이자가 건보료에 붙는지 — 파이어 후 건보료 계산(파이어맵)', '/health-insurance'),
 'XzMCiAwQhAo': ('오늘의 참고 지표(파이어맵 소식)', '/news'),
}
yt = f2_coupang.service()
go = '--go' in sys.argv
res = []
for vid, (label, path) in PLAN.items():
    sn = yt.videos().list(part='snippet', id=vid).execute()['items'][0]['snippet']
    d = sn['description']
    if 'firemap.kr' in d:
        print(vid, '이미 있음'); res.append((vid, 'skip')); continue
    line = f'{label}: https://firemap.kr{path}?{U}{vid}'
    nd = d.rstrip() + '\n\n' + line
    print(vid, '|', sn['title'][:30], '| audio', sn.get('defaultAudioLanguage'), '\n  +', line)
    if not go: continue
    json.dump(sn, open(os.path.join(D, f'desc_before_{vid}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    new = dict(sn); new['description'] = nd
    for k in ('thumbnails', 'channelId', 'channelTitle', 'publishedAt', 'liveBroadcastContent', 'localized'): new.pop(k, None)
    try:
        yt.videos().update(part='snippet', body={'id': vid, 'snippet': new}).execute()
    except Exception as e:
        print('  거절', str(e)[:200]); res.append((vid, 'fail')); continue
    c = yt.videos().list(part='snippet', id=vid).execute()['items'][0]['snippet']
    ok = all(c.get(k) == sn.get(k) for k in ('title', 'categoryId', 'tags', 'defaultLanguage', 'defaultAudioLanguage')) and 'firemap.kr' in c['description']
    print('  되읽기', 'OK' if ok else '불일치', '| audio', c.get('defaultAudioLanguage'), '| 길이', len(d), '->', len(c['description']))
    res.append((vid, 'ok' if ok else 'mismatch'))
print(res)
