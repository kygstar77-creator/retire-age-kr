# 네이버 검색광고 키워드도구 = 월간 검색수(PC·모바일). 주제 고를 때 이 숫자로 줄 세운다.
# 키는 사장님이 저장한 파일에서만 읽는다(출력·로그에 찍지 않는다).
# 사용: python kwvol.py 키워드1 키워드2 ...   또는   python kwvol.py @keywords.txt
import sys, time, hmac, hashlib, base64, json, urllib.request, urllib.parse, os
sys.stdout.reconfigure(encoding='utf-8')
KEYFILE = r'C:\Users\강영준\Documents\naver_searchad.txt'

def load():
    if not os.path.exists(KEYFILE): sys.exit('키 파일 없음: ' + KEYFILE)
    kv = {}
    for line in open(KEYFILE, encoding='utf-8-sig'):
        if '=' in line:
            k, v = line.strip().split('=', 1); kv[k.strip().upper()] = v.strip()
    for k in ('CUSTOMER_ID', 'ACCESS_LICENSE', 'SECRET_KEY'):
        if not kv.get(k) or '(' in kv[k]: sys.exit(k + ' 값이 비어 있음')
    return kv

def call(kv, hints):
    ts = str(int(time.time() * 1000)); uri = '/keywordstool'
    sig = base64.b64encode(hmac.new(kv['SECRET_KEY'].encode(), f'{ts}.GET.{uri}'.encode(), hashlib.sha256).digest()).decode()
    q = urllib.parse.urlencode({'hintKeywords': ','.join(hints), 'showDetail': '1'})
    req = urllib.request.Request('https://api.searchad.naver.com' + uri + '?' + q, headers={
        'X-Timestamp': ts, 'X-API-KEY': kv['ACCESS_LICENSE'], 'X-Customer': kv['CUSTOMER_ID'], 'X-Signature': sig})
    return json.load(urllib.request.urlopen(req, timeout=20))['keywordList']

def num(v):  # '< 10' 같은 값은 5로
    try: return int(v)
    except Exception: return 5

def main():
    args = sys.argv[1:]
    if args and args[0].startswith('@'):
        args = [l.strip() for l in open(args[0][1:], encoding='utf-8') if l.strip()]
    if not args: sys.exit('키워드를 주세요')
    kv = load(); seen = {}; asked = set(a.replace(' ', '').upper() for a in args)
    for i in range(0, len(args), 5):  # 힌트는 한 번에 5개까지, 공백 불가
        for r in call(kv, [a.replace(' ', '') for a in args[i:i+5]]):
            seen[r['relKeyword']] = (num(r['monthlyPcQcCnt']), num(r['monthlyMobileQcCnt']), r.get('compIdx', ''))
        time.sleep(0.4)
    rows = sorted(seen.items(), key=lambda x: -(x[1][0] + x[1][1]))
    json.dump({k: {'pc': v[0], 'mo': v[1]} for k, v in rows}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kwvol_last.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('== 물어본 키워드'); 
    for k, v in rows:
        if k.upper() in asked: print(f'{v[0]+v[1]:>9,}  (PC {v[0]:,} / 모바일 {v[1]:,})  {k}')
    print('\n== 연관 키워드 상위 40')
    for k, v in [r for r in rows if r[0].upper() not in asked][:40]: print(f'{v[0]+v[1]:>9,}  {k}')

main()
