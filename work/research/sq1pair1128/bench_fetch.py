import json, urllib.request, re, os
UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://m.cafe.naver.com/'}
cafes = {'배투모': 31050378, '은오': 23676262, '월재연': 22290117, '짠돌이': 14028420, '평생ETF': 31097286, '티끌': 30852806, '미주미': 28497937, '노후연구소': 20898041, '정가거부': 30786704}
pat = re.compile(r'SCHD|슈드|나스닥|QQQ|배당다우|S&P|에스앤피|섞', re.I)
rows = []
for n, cid in cafes.items():
    try:
        j = json.load(urllib.request.urlopen(urllib.request.Request(f'https://apis.naver.com/cafe-web/cafe2/WeeklyPopularArticleList.json?cafeId={cid}', headers=UA), timeout=20))
        open(f'bench_raw/weekly_{cid}.json', 'w', encoding='utf-8').write(json.dumps(j, ensure_ascii=False))
        arts = j['message']['result'].get('popularArticleList', [])
        for a in arts:
            t = a.get('subject', '')
            if pat.search(t):
                rows.append((n, cid, a.get('articleId'), t, a.get('readCount'), a.get('commentCount'), a.get('likeItCount') or a.get('likeCount')))
        print(n, len(arts))
    except Exception as e:
        print(n, 'ERR', e)
for r in sorted(rows, key=lambda r: -(r[4] or 0)): print(r)
