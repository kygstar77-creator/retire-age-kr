# 유튜브 웹 검색(innertube) — 쇼츠 칸까지 영상ID 수집
import sys, json, re, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
URL = 'https://www.youtube.com/youtubei/v1/search?prettyPrint=false'
def search(q, params='EgIIBA%3D%3D', pages=3):
    import urllib.parse
    params = urllib.parse.unquote(params)
    body = {'context': {'client': {'clientName': 'WEB', 'clientVersion': '2.20260901.00.00', 'hl': 'ko', 'gl': 'KR'}}, 'query': q, 'params': params}
    ids = []; cont = None
    for _ in range(pages):
        b = dict(body)
        if cont: b = {'context': body['context'], 'continuation': cont}
        req = urllib.request.Request(URL, data=json.dumps(b).encode(), headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
        d = json.load(urllib.request.urlopen(req, timeout=30))
        s = json.dumps(d, ensure_ascii=False)
        for m in re.finditer(r'"(?:videoId|reelWatchEndpoint)"\s*:\s*\{?"?(?:videoId"\s*:\s*")?([A-Za-z0-9_-]{11})"', s):
            if m[1] not in ids: ids.append(m[1])
        cs = re.findall(r'"continuationCommand":\{"token":"([^"]+)"', s)
        if not cs: break
        cont = cs[-1]
    return ids
if __name__ == '__main__':
    print(search(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'EgIIBA%3D%3D'))
