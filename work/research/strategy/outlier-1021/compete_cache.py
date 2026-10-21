# 이미 받은 검색 결과(시드 39개 × 조회순 50편, 90일)에서 구조별로 '이미 만드는 채널' 세기 — 추가 할당량 0
import json, re, sys, collections, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
c = json.load(open(os.path.join(H,'cache_search.json'),encoding='utf-8')); ch = json.load(open(os.path.join(H,'channels.json'),encoding='utf-8'))
vids = {v['id']: v for vs in c.values() for v in vs}
import html
S = {
 'A 한장표·기준표 쇼츠(총정리/한눈에/기준표/TOP)': r'한눈에|총정리|완전정리|기준표|한 장|TOP ?\d+',
 'B 모르면 손해·놓치는 N가지': r'모르면|놓치|손해 보는|날리지',
 'C 퇴직금으로 ○○하면 실제로 남은 돈': r'실제로 남|남은 돈|퇴직금으로',
 'D 50대 은퇴 함정·실수 N가지(롱폼)': r'함정|실수',
 'E A vs B 싹 다 비교': r'vs|VS|비교',
 'F 몇 살부터·얼마 받나 계산': r'몇 살|몇살|얼마 받|계산해',
 'G 몰락·폭탄의 진짜 이유(사건)': r'몰락|폭탄|추락',
 'H 연예인·재벌 집·재산': r'연예인|가계도|재벌|회장님',
 'I 동네 입지·아파트 이야기': r'입지|시범단지|시민아파트',
 'J 발표·개편 반응·속보': r'반응|속보|긴급|발표',
}
out = {}
for k, p in S.items():
    m = [v for v in vids.values() if re.search(p, html.unescape(v['title']))]
    cids = collections.Counter(v['cid'] for v in m)
    sz = collections.Counter()
    for cid in cids:
        s = (ch.get(cid) or {}).get('subs')
        sz['?' if s is None else ('<1만' if s < 1e4 else '1만~10만' if s < 1e5 else '10만+')] += 1
    out[k] = dict(videos=len(m), channels=len(cids), size=dict(sz))
    print(k, out[k])
json.dump(out, open(os.path.join(H,'compete_from_cache.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('검색 결과 전체', len(vids), '편', len({v['cid'] for v in vids.values()}), '채널')
