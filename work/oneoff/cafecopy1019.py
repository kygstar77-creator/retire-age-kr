# 한 번 쓰는 조사 스크립트(2026-10-19 사장님 "카페도 똑같이 하라고! 포스팅·이미지·썸네일·내용·운영 방식·회원 모아 오는 거·수익화 등등 모두!").
# 잘되는 재테크·은퇴·배당·부동산·짠테크 카페의 '주간 인기글'과 최근 글을 공개 API로 모으고,
# 인기글 본문(전체공개만)을 열어 글 길이·사진 수·사진 자리·표·첫 줄·끝 줄을 잰다. 로그인·가입·글쓰기·댓글 없음.
#   py -3.12 work/oneoff/cafecopy1019.py            → research/growth/cafe-copy-1019/raw.json
import sys, os, re, json, time, html, statistics, collections, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, 'research', 'growth', 'cafe-copy-1019'); os.makedirs(OUT, exist_ok=True)
H = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148',
     'Referer': 'https://m.cafe.naver.com/'}
CAFES = ['wecando7', 'jaegebal', 'onepieceholicplus', 'engmstudy', 'dlxogns01', 'q69', 'divclub', 'likeusstock',
         'wjdrkrjqn', 'freejoa', 'dwqebmhy', 'eovhskfktmak', 'parentsrich', 'ttokjae', 'geobuk2']

def get(u):
    for i in range(2):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=25).read().decode('utf-8', 'ignore'))
        except Exception as e:
            err = str(e); time.sleep(1)
    return {'err': err}

def clean(s): return html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()

def gate(club):
    r = (get(f'https://apis.naver.com/cafe-web/cafe2/CafeGateInfo.json?cluburl={club}').get('message') or {}).get('result') or {}
    v = r.get('cafeInfoView') or {}
    return {'cafeId': v.get('cafeId'), 'name': v.get('cafeName'), 'members': r.get('memberCount'), 'open': v.get('openDate'),
            'level': r.get('useMemberLevel'), 'power': v.get('powerCafe'), 'incomeShareAd': r.get('showIncomeShareAd'),
            'sysop': v.get('sysopNick')}

def boards(cid):
    r = ((get(f'https://apis.naver.com/cafe-web/cafe2/SideMenuList?cafeId={cid}').get('message') or {}).get('result') or {})
    return [{'t': m.get('menuType'), 'id': m.get('menuId'), 'name': clean(m.get('menuName'))} for m in r.get('menus') or []]

def popular(cid):
    r = ((get(f'https://apis.naver.com/cafe-web/cafe2/WeeklyPopularArticleList.json?cafeId={cid}').get('message') or {}).get('result') or {})
    return [{'aid': a['articleId'], 'subject': clean(a.get('subject')), 'read': a.get('readCount') or 0,
             'comment': a.get('commentCount') or 0, 'up': a.get('upCount') or 0, 'img': a.get('imageCount') or 0,
             'menuId': a.get('menuId'), 'nick': a.get('nickname'), 'open': a.get('openArticle'), 'ts': a.get('writeDateTimestamp'),
             'score': a.get('totalScore')} for a in r.get('popularArticleList') or []]

def recent(cid, pages=15):
    out = []
    for p in range(1, pages + 1):
        r = ((get(f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={cid}&search.queryType=lastArticle&search.page={p}&search.perPage=20').get('message') or {}).get('result') or {})
        L = r.get('articleList') or []
        for a in L:
            out.append({'aid': a['articleId'], 'subject': clean(a.get('subject')), 'menu': clean(a.get('menuName')),
                        'nick': a.get('writerNickname'), 'lv': a.get('memberLevel'), 'read': a.get('readCount') or 0,
                        'comment': a.get('commentCount') or 0, 'ts': a.get('writeDateTimestamp'), 'open': a.get('openArticle'),
                        'img': a.get('imageAttachCount') or 0, 'rimg': a.get('representImage'), 'rtype': a.get('representImageType')})
        if not r.get('hasNext') or not L: break
        time.sleep(0.25)
    return out

def body(cid, aid):
    d = get(f'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/{cid}/articles/{aid}?useCafeId=true')
    if 'result' not in d: return None
    a = d['result'].get('article') or {}
    h = a.get('contentHtml') or ''
    # 본문 순서대로 덩어리: 글/사진/표/링크카드/영상
    seq = []
    for m in re.finditer(r'class="se-component (se-[a-z\-]+)', h): seq.append(m.group(1))
    txt = re.sub(r'\n{2,}', '\n', html.unescape(re.sub(r'<(br|/p|/div|/li|/tr|/h\d)[^>]*>', '\n', h)))
    txt = re.sub(r'<[^>]+>', '', txt); lines = [l.strip() for l in txt.splitlines() if l.strip()]
    imgs = len(re.findall(r'<img[^>]+(?:se-image-resource|class="se-image|data-lazy-src|src=")', h))
    comp = collections.Counter(seq)
    first_img = next((i for i, s in enumerate(seq) if s in ('se-image', 'se-imageGroup', 'se-imageStrip')), None)
    cs = ((d['result'].get('comments') or {}).get('items')) or []
    return {'chars': sum(len(l) for l in lines), 'lines': len(lines), 'seq': seq[:60], 'comp': dict(comp),
            'imgTags': imgs, 'tables': h.count('<table'), 'firstImgIdx': first_img, 'nComp': len(seq),
            'head': lines[:6], 'tail': lines[-8:], 'links': re.findall(r'href="(https?://[^"]+)"', h)[:20],
            'writerReplies': sum(1 for c in cs if c.get('isArticleWriter')),
            'comments': [{'w': c.get('isArticleWriter'), 't': (c.get('content') or '')[:120]} for c in cs[:12]]}

def main():
    res = []
    for club in CAFES:
        g = gate(club); cid = g['cafeId']
        if not cid: print(club, '게이트 실패'); continue
        b = boards(cid); time.sleep(0.3)
        pop = popular(cid); time.sleep(0.3)
        rec = recent(cid)
        bmap = {x['id']: x['name'] for x in b}
        for p in pop: p['menu'] = bmap.get(p['menuId'], '')
        # 본문: 인기글 중 전체공개 상위(조회순) 6편
        opened = [p for p in sorted(pop, key=lambda x: -x['read']) if p['open']][:6]
        for p in opened:
            p['body'] = body(cid, p['aid']); time.sleep(0.35)
        res.append({'club': club, **g, 'boards': b, 'popular': pop, 'recent': rec})
        print(f"{club} 회원 {g['members']} 게시판 {len([x for x in b if x['t']=='B'])} 인기글 {len(pop)}(공개 {sum(1 for p in pop if p['open'])}) 최근 {len(rec)} 본문 {sum(1 for p in opened if p.get('body'))}", flush=True)
        json.dump(res, open(os.path.join(OUT, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False)

if __name__ == '__main__':
    main()
