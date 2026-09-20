# Pexels 사진 검색·내려받기. 키는 사장님이 저장한 파일에서만 읽는다.
# 사용: python pexels.py "검색어" [장수=6] [저장폴더]
# 실측(2026-09-20): 한글 검색어는 locale=ko-KR을 붙여야 맞는 사진이 나온다(안 붙이면 '적금 저축'에 아파트가 나옴). 한글+ko-KR은 한국 풍경(용인·서울 아파트)이 상위에 오고,
# 영어는 장수는 많지만 달러 지폐·외국 건물이 섞인다. 그래서 한 주제를 한글·영어 둘 다 돌려 상위 결과를 비교한 뒤 한국 글에 어색하지 않은 쪽을 고른다.
# 결과: 후보 목록(번호·크기·작가·페이지 주소) + 가로형 large 이미지를 폴더에 저장. 출처 표기는 의무 아님(Pexels 라이선스).
import sys, os, json, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
KEYFILE = r'C:\Users\강영준\Documents\pexels_key.txt'
if not os.path.exists(KEYFILE): sys.exit('키 파일 없음: ' + KEYFILE)
key = open(KEYFILE, encoding='utf-8-sig').read().strip().split('=')[-1].strip()
if not key: sys.exit('키가 비어 있음')
q = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pexels_out')
os.makedirs(out, exist_ok=True)
import re
params = {'query': q, 'per_page': n, 'orientation': 'landscape'}
if re.search('[가-힣]', q): params['locale'] = 'ko-KR'
u = 'https://api.pexels.com/v1/search?' + urllib.parse.urlencode(params)
d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': key, 'User-Agent': 'Mozilla/5.0'}), timeout=20))
for i, p in enumerate(d.get('photos', []), 1):
    fn = os.path.join(out, f"{q.replace(' ', '_')}_{i}_{p['id']}.jpg")
    req = urllib.request.Request(p['src']['large'], headers={'User-Agent': 'Mozilla/5.0'})
    open(fn, 'wb').write(urllib.request.urlopen(req, timeout=30).read())
    print(f"{i}. {p['width']}x{p['height']} | {p['photographer']} | {p['url']} | {p.get('alt','')[:50]}\n   -> {fn}")
print('총', d.get('total_results'), '장 중', len(d.get('photos', [])), '장 저장')
