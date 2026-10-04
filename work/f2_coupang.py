# F2(2026-10-01) — 공개 롱폼 설명란 첫 줄에 쿠팡 대가성 문구 + 링크 1개, '유료 프로모션 포함' 켜기.
#   py -3.12 work/f2_coupang.py auth     # 한 번: 설명 수정 권한(youtube.force-ssl) 토큰 — 사장님 구글 동의 화면
#   py -3.12 work/f2_coupang.py dry      # 바뀔 설명 미리 보기(아무것도 안 바꿈)
#   py -3.12 work/f2_coupang.py apply    # 적용 + 되읽기 확인 → research/longform/loop/f2_after.json
# 계획표: research/longform/loop/f2_plan.json — link가 비어 있거나 link.coupang.com이 아니면 그 영상은 건너뛴다.
# 전제(coupang-policy.md 체크리스트 1): 쿠팡 '내 정보'에 youtube.com/@firemapkr 등록 확인 전에는 apply하지 않는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ytupload, aitell
DOCS = r'C:\Users\강영준\Documents'
TOKEN = os.path.join(DOCS, 'youtube_manage_token.json')
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
PLAN = os.path.join(HERE, 'research', 'longform', 'loop', 'f2_plan.json')
AFTER = os.path.join(HERE, 'research', 'longform', 'loop', 'f2_after.json')

def auth():
    from google_auth_oauthlib.flow import InstalledAppFlow
    c = InstalledAppFlow.from_client_secrets_file(ytupload.CLIENT, SCOPES).run_local_server(port=0, prompt='consent', access_type='offline')
    open(TOKEN, 'w').write(c.to_json()); print('저장:', TOKEN)

def service():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    if not os.path.exists(TOKEN): print('토큰 없음 — py -3.12 work/f2_coupang.py auth'); sys.exit(2)
    c = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if c.expired and c.refresh_token: c.refresh(Request()); open(TOKEN, 'w').write(c.to_json())
    return build('youtube', 'v3', credentials=c)

def new_desc(old, link, label):
    body = old
    if body.startswith(ytupload.COUPANG_NOTE): return None  # 이미 적용됨
    return f'{ytupload.COUPANG_NOTE}\n{label} {link}\n\n{body}'

def main(mode):
    plan = json.load(open(PLAN, encoding='utf-8'))
    yt = service() if mode == 'apply' else ytupload.service()
    done = []
    for p in plan['videos']:
        link = p.get('link', '')
        if p.get('skip') or not link.startswith('https://link.coupang.com/'):
            print('건너뜀', p['id'], p.get('skip') or '링크 없음'); continue
        v = yt.videos().list(part='snippet,status', id=p['id']).execute()['items'][0]
        sn = v['snippet']
        nd = new_desc(sn['description'], link, p['label'])
        if nd is None: print('이미 적용', p['id']); continue
        if len(nd) > 5000: print('5000자 넘음', p['id']); continue
        print('---', p['id'], sn['title'][:40]); print(nd[:220])
        # AI 티 검사(10/1) — 새로 붙이는 줄(라벨)만 본다. 기존 설명은 ytupload에서 이미 봤다.
        ok_ai, msg_ai, hits_ai = aitell.gate_text(p['label'], os.environ.get('FIREMAP_EDITOR_OK') == '1')
        if not ok_ai: aitell.refuse(msg_ai, hits_ai); continue
        if mode != 'apply': continue
        body = {'id': p['id'],
                'snippet': {'title': sn['title'], 'description': nd, 'categoryId': sn['categoryId'], 'tags': sn.get('tags', []),
                            'defaultLanguage': 'ko', 'defaultAudioLanguage': 'ko'},  # 오디오 언어 빼면 en-US로 바뀐 적 있음(10/5)
                'paidProductPlacementDetails': {'hasPaidProductPlacement': True}}
        yt.videos().update(part='snippet,paidProductPlacementDetails', body=body).execute()
        chk = yt.videos().list(part='snippet,paidProductPlacementDetails', id=p['id']).execute()['items'][0]
        ok = chk['snippet']['description'].startswith(ytupload.COUPANG_NOTE) and chk.get('paidProductPlacementDetails', {}).get('hasPaidProductPlacement')
        print('되읽기', 'OK' if ok else '불일치')
        done.append({'id': p['id'], 'ok': bool(ok), 'link': link, 'paid': chk.get('paidProductPlacementDetails')})
    if mode == 'apply': json.dump(done, open(AFTER, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    m = sys.argv[1] if len(sys.argv) > 1 else 'dry'
    auth() if m == 'auth' else main(m)
