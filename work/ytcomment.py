# 공개 롱폼 첫 댓글(채널 이름) — 2026-10-13 사장님 "댓글도 니가 알아서 잘 썼었잖아"(PD 작업 지시 '공개 직후 첫 댓글').
#   py -3.12 work/ytcomment.py post <videoId> <댓글.txt>   # 영상이 public일 때만 단다 → research/longform/loop/yt_comments.jsonl 한 줄
#   py -3.12 work/ytcomment.py list                        # 단 댓글 목록
# 막는 것: 비공개·예약 영상에 달기(공개 전 댓글은 시청자에게 안 보임), 이미 단 영상에 또 달기,
#   예전 댓글과 같은 문장·같은 링크만 있는 댓글(유튜브 스팸 정책 — 영상마다 다른 숫자 하나를 넣는다).
# 고정은 API로 못 한다 → STATE.md에 '고정 대기: 영상ID'.
import sys, os, json, re, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import f2_coupang
LOG = os.path.join(HERE, 'research', 'longform', 'loop', 'yt_comments.jsonl')

def load():
    if not os.path.exists(LOG): return []
    return [json.loads(l) for l in open(LOG, encoding='utf-8') if l.strip()]

def lines_of(t): return {re.sub(r'\s+', ' ', x).strip() for x in t.splitlines() if len(x.strip()) >= 15 and not x.strip().startswith('http')}

def post(vid, path):
    text = open(path, encoding='utf-8').read().strip()
    old = load()
    assert not any(o['videoId'] == vid for o in old), f'{vid}에 이미 댓글 있음'
    for o in old:
        same = lines_of(text) & lines_of(o['text'])
        assert not same, f'예전 댓글({o["videoId"]})과 같은 문장: {same}'
    assert re.search(r'\d', re.sub(r'https?://\S+', '', text)), '숫자 하나는 넣는다(영상에서 못 보여준 숫자)'
    yt = f2_coupang.service()
    st = yt.videos().list(part='status', id=vid).execute()['items'][0]['status']
    assert st['privacyStatus'] == 'public', f'아직 공개 전: {st}'
    r = yt.commentThreads().insert(part='snippet', body={'snippet': {'videoId': vid, 'topLevelComment': {'snippet': {'textOriginal': text}}}}).execute()
    rec = {'videoId': vid, 'commentId': r['id'], 'at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'text': text, 'pinned': False}
    open(LOG, 'a', encoding='utf-8').write(json.dumps(rec, ensure_ascii=False) + '\n')
    print('달림', r['id'])

if __name__ == '__main__':
    if sys.argv[1] == 'post': post(sys.argv[2], sys.argv[3])
    else:
        for o in load(): print(o['at'], o['videoId'], o['commentId'], o['text'][:40].replace('\n', ' '))
