# R2(2026-10-01) — 공개 롱폼 설명란 둘째 줄에 주제 맞는 계산기 링크 1개(utm_campaign=영상id).
#   py -3.12 work/calc_links.py dry     # 미리 보기
#   py -3.12 work/calc_links.py apply   # 적용 + 되읽기 → research/longform/loop/calc_links_after.json
# 롱폼 6편은 전부 파이어·ETF·배당 주제라 맞는 계산기는 첫 화면 '은퇴 나이 계산'(연봉·퇴직금·실업급여 계산기는 주제 불일치).
# A-1(SCOI0DP-l-s)은 이미 utm 링크가 셋째 줄에 있어 건드리지 않는다. 쿠팡 줄(f2_coupang.py)은 나중에 이 위에 붙는다.
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import f2_coupang, ytupload
AFTER = os.path.join(HERE, 'research', 'longform', 'loop', 'calc_links_after.json')
IDS = ['zhTjJwy1mwQ', 'wwfFszPl06g', 'scV67BQvC4Q', 'JVTYZ208hgw', 'gSKsQWjTabo', 'cxls2Ve18-k']
LABEL = '▶ 내 은퇴 나이 계산하기:'

def url(vid): return f'https://firemap.kr/?utm_source=youtube&utm_medium=desc&utm_campaign={vid}'

def new_desc(old, vid):
    u = url(vid)
    if u in old: return None
    lines = old.split('\n')
    # 첫 문단이 2줄 이하면 그 문단 뒤, 길면 첫 줄 뒤(한 생각으로 이어진 두 문장을 가르지 않는다)
    k = lines.index('') if '' in lines else len(lines)
    cut = k if k <= 2 else 1
    # 아래쪽 맨 주소(https://firemap.kr 또는 줄 전체가 firemap.kr)는 같은 utm 주소로 바꿔 클릭을 한곳에서 잰다
    body = re.sub(r'https://firemap\.kr(?![/?\w.])', u, '\n'.join(lines[cut:]))
    body = re.sub(r'(?m)^firemap\.kr\s*$', u, body)
    return '\n'.join(lines[:cut]) + f'\n{LABEL} {u}\n' + body

def main(mode):
    yt = f2_coupang.service() if mode == 'apply' else ytupload.service()
    done = []
    for vid in IDS:
        v = yt.videos().list(part='snippet', id=vid).execute()['items'][0]
        sn = v['snippet']
        nd = new_desc(sn['description'], vid)
        if nd is None: print('이미 적용', vid); continue
        if len(nd) > 5000: print('5000자 넘음', vid); continue
        print('---', vid, sn['title'][:40]); print(nd[:260]); print('...바뀐 아래 주소 수:', nd.count(url(vid)))
        if mode != 'apply': continue
        body = {'id': vid, 'snippet': {'title': sn['title'], 'description': nd, 'categoryId': sn['categoryId'],
                                       'tags': sn.get('tags', []), 'defaultLanguage': sn.get('defaultLanguage', 'ko')}}
        if sn.get('defaultAudioLanguage'): body['snippet']['defaultAudioLanguage'] = sn['defaultAudioLanguage']
        yt.videos().update(part='snippet', body=body).execute()
        chk = yt.videos().list(part='snippet', id=vid).execute()['items'][0]['snippet']
        ok = f'{LABEL} {url(vid)}' in chk['description'].split('\n')[:4] and chk['title'] == sn['title'] and chk.get('tags', []) == sn.get('tags', [])
        print('되읽기', 'OK' if ok else '불일치')
        done.append({'id': vid, 'ok': ok, 'url': url(vid), 'old_desc': sn['description']})
    if mode == 'apply': json.dump(done, open(AFTER, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'dry')
