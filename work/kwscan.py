# 블로그 주제 찾기: 씨앗 키워드 -> 검색광고 API 연관어 전체 수집 -> 월 검색수·모바일 비중·광고경쟁도 저장
import sys, time, hmac, hashlib, base64, json, urllib.request, urllib.parse, os
sys.stdout.reconfigure(encoding='utf-8')
KEYFILE = r'C:\Users\강영준\Documents\naver_searchad.txt'
kv = {}
for line in open(KEYFILE, encoding='utf-8-sig'):
    if '=' in line:
        k, v = line.strip().split('=', 1); kv[k.strip().upper()] = v.strip()
def call(hints):
    ts = str(int(time.time() * 1000)); uri = '/keywordstool'
    sig = base64.b64encode(hmac.new(kv['SECRET_KEY'].encode(), f'{ts}.GET.{uri}'.encode(), hashlib.sha256).digest()).decode()
    q = urllib.parse.urlencode({'hintKeywords': ','.join(hints), 'showDetail': '1'})
    req = urllib.request.Request('https://api.searchad.naver.com' + uri + '?' + q, headers={
        'X-Timestamp': ts, 'X-API-KEY': kv['ACCESS_LICENSE'], 'X-Customer': kv['CUSTOMER_ID'], 'X-Signature': sig})
    for attempt in range(3):
        try: return json.load(urllib.request.urlopen(req, timeout=25))['keywordList']
        except Exception as e:
            time.sleep(1.5)
    return []
num = lambda v: int(v) if str(v).isdigit() else 5
seeds = [l.strip().replace(' ', '') for l in open(sys.argv[1], encoding='utf-8') if l.strip() and not l.startswith('#')]
out = {}
for i in range(0, len(seeds), 5):
    for r in call(seeds[i:i+5]):
        out[r['relKeyword']] = {'pc': num(r['monthlyPcQcCnt']), 'mo': num(r['monthlyMobileQcCnt']), 'comp': r.get('compIdx', ''), 'ads': r.get('plAvgDepth', 0)}
    time.sleep(0.35)
    print(f'{i+5}/{len(seeds)} seeds, {len(out)} keywords', file=sys.stderr)
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False)
print(len(out))
