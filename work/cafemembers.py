# 카페 회원 수를 잰다 — 카페 조회수가 낮은 것이 글 탓인지 카페 규모 탓인지 가르는 데 쓴다.
# 사용: python work/cafemembers.py
# 근거: 카페 웹 API CafeGateInfo.json (로그인 불필요, Referer만 필요). 2026-09-23 확인.
#      CafeInfo.json은 "존재하지 않는 API", MyCafeIntro.nhn은 KSC5601 HTML이라 쓰지 않는다.
import sys, os, json, datetime, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
CLUBID = '31789001'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Referer': 'https://cafe.naver.com/'}
LOG = os.path.join(HERE, 'cafe_members.json')

def member_count():
    u = 'https://apis.naver.com/cafe-web/cafe2/CafeGateInfo.json?cafeId=' + CLUBID
    d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20).read().decode('utf-8', 'ignore'))
    return d['message']['result']['memberCount']

if __name__ == '__main__':
    n = member_count()
    today = datetime.date.today().isoformat()
    log = json.load(open(LOG, encoding='utf-8')) if os.path.exists(LOG) else {}
    log[today] = n
    json.dump(log, open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('%s 카페 회원 %d명' % (today, n))
    for d in sorted(log)[-7:]:
        print('  ', d, log[d])
