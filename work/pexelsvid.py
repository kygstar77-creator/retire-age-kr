# Pexels 영상 검색·내려받기 + 출처 기록(롱폼 실사 장면용, motion 2026-10-12).
# 사용: py -3.12 work/pexelsvid.py "검색어" [장수=4] [편 폴더, 예: work/research/longform/ep/P-1]
#   → <편>/stock/<id>.mp4 (가로 1920 이하 중 가장 큰 HD 파일) + <편>/stock/credits.json에 한 줄씩 누적.
# 라이선스(원문 https://www.pexels.com/license/ 10/12 19:3x 확인): 사진·영상 무료, 출처 의무 없음, 고쳐 써도 됨.
#   금지: 알아볼 수 있는 사람을 나쁘게·불쾌하게 쓰기 / 사람·상표가 우리를 보증하는 듯 쓰기 / 고치지 않은 원본 판매·재배포.
#   우리 규칙(10/11 지시): 출처는 설명란에 적는다 → credits.json의 desc_line을 PD가 설명란 끝에 붙인다.
#   상표·간판·번호판·얼굴은 화면에서 흐리게(StockShot blur 칸). 뉴스 사진·남의 영상은 블러해도 안 씀.
import sys, os, json, re, datetime, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
KEYFILE = r'C:\Users\강영준\Documents\pexels_key.txt'
key = open(KEYFILE, encoding='utf-8-sig').read().strip().split('=')[-1].strip()
q = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
ep = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pexels_out')
out = os.path.join(ep, 'stock'); os.makedirs(out, exist_ok=True)
params = {'query': q, 'per_page': n, 'orientation': 'landscape', 'size': 'medium'}
if re.search('[가-힣]', q): params['locale'] = 'ko-KR'
H = {'Authorization': key, 'User-Agent': 'Mozilla/5.0'}
d = json.load(urllib.request.urlopen(urllib.request.Request('https://api.pexels.com/videos/search?' + urllib.parse.urlencode(params), headers=H), timeout=20))
cpath = os.path.join(out, 'credits.json')
credits = json.load(open(cpath, encoding='utf-8')) if os.path.exists(cpath) else []
have = {c['id'] for c in credits}
for i, v in enumerate(d.get('videos', []), 1):
    files = [f for f in v['video_files'] if f.get('file_type') == 'video/mp4' and f.get('width') and f['width'] <= 1920 and f['width'] >= f['height']]
    if not files: continue
    f = max(files, key=lambda f: f['width'])
    fn = os.path.join(out, f"{v['id']}.mp4")
    if not os.path.exists(fn):
        open(fn, 'wb').write(urllib.request.urlopen(urllib.request.Request(f['link'], headers={'User-Agent': 'Mozilla/5.0'}), timeout=120).read())
    if v['id'] not in have:
        credits.append({'id': v['id'], 'query': q, 'file': os.path.basename(fn), 'w': f['width'], 'h': f['height'], 'sec': v.get('duration'),
                        'author': v['user']['name'], 'author_url': v['user']['url'], 'page': v['url'],
                        'license': 'https://www.pexels.com/license/', 'got': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'used': False, 'desc_line': f"영상 일부: {v['user']['name']} / Pexels ({v['url']})"})
        have.add(v['id'])
    print(f"{i}. {v['id']} {f['width']}x{f['height']} {v.get('duration')}초 | {v['user']['name']} | {v['url']}\n   -> {fn}")
json.dump(credits, open(cpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('총', d.get('total_results'), '편 중', len(d.get('videos', [])), '편 · 출처', cpath)
