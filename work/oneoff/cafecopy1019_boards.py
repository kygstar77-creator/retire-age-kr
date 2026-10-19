# cafecopy1019.py 다음 단계: 정보 게시판(칼럼·특판·연금·필독자료)에서 전체공개·사흘 넘은 글 중 조회 상위 3편씩 본문을 연다.
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cafecopy1019 as cc
T = {27549420: [76, 144, 250], 12730407: [350, 301], 22290117: [288, 160, 121], 14028420: [1684, 1726, 1593],
     23676262: [111, 107, 493, 491], 20898041: [13, 110], 30852806: [5, 39, 45], 31097286: [8, 55, 11],
     31050378: [15, 6], 28497937: [115, 121], 18251503: [26, 24], 10346911: [263, 148], 30786704: [53, 49]}
out = []
now = time.time() * 1000
for cid, menus in T.items():
    for mid in menus:
        arts = []
        for p in range(1, 4):
            r = ((cc.get(f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={cid}&search.menuid={mid}&search.queryType=lastArticle&search.page={p}&search.perPage=20').get('message') or {}).get('result') or {})
            L = r.get('articleList') or []
            arts += L
            if not r.get('hasNext') or not L: break
            time.sleep(0.25)
        ripe = [a for a in arts if a.get('writeDateTimestamp') and now - a['writeDateTimestamp'] > 3 * 86400000]
        opn = sorted([a for a in ripe if a.get('openArticle')], key=lambda a: -(a.get('readCount') or 0))[:3]
        stat = {'cid': cid, 'menuId': mid, 'menu': cc.clean(arts[0].get('menuName')) if arts else '', 'n': len(arts), 'ripe': len(ripe),
                'openShare': round(sum(1 for a in arts if a.get('openArticle')) / max(1, len(arts)), 2),
                'readMed': sorted(a.get('readCount') or 0 for a in ripe)[len(ripe)//2] if ripe else None,
                'cmtMed': sorted(a.get('commentCount') or 0 for a in ripe)[len(ripe)//2] if ripe else None,
                'top': [{'aid': a['articleId'], 'subject': cc.clean(a.get('subject')), 'read': a.get('readCount'), 'comment': a.get('commentCount'),
                         'open': a.get('openArticle'), 'img': a.get('imageAttachCount'), 'rimg': a.get('representImage'), 'nick': a.get('writerNickname'),
                         'ts': a.get('writeDateTimestamp')} for a in sorted(ripe, key=lambda a: -(a.get('readCount') or 0))[:8]],
                'bodies': []}
        for a in opn:
            b = cc.body(cid, a['articleId']); time.sleep(0.35)
            if b: stat['bodies'].append({'aid': a['articleId'], 'subject': cc.clean(a.get('subject')), 'read': a.get('readCount'), 'comment': a.get('commentCount'), 'rimg': a.get('representImage'), 'body': b})
        out.append(stat)
        print(cid, mid, stat['menu'][:20], 'n', stat['n'], 'ripe', stat['ripe'], 'open', stat['openShare'], 'readMed', stat['readMed'], 'cmtMed', stat['cmtMed'], 'bodies', len(stat['bodies']), flush=True)
        json.dump(out, open(os.path.join(cc.OUT, 'boards.json'), 'w', encoding='utf-8'), ensure_ascii=False)
