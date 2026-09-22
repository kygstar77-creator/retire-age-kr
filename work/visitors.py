# 블로그 방문자(오늘/전체)를 매일 기록 — 발행량을 올릴 때 불이익이 시작되는지 보는 조기 신호.
# 모바일 블로그 첫 화면의 "오늘 N  전체 M"을 읽는다(2026-09-23 실측). 로그인·프로필 불필요.
#   python work/visitors.py            → work/visitors_log.json 에 {날짜: {today, total, at}} 추가
import sys, re, json, os, time
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
BLOG_ID = 'kygstar7777'
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'visitors_log.json')
with sync_playwright() as p:
    b = p.chromium.launch(headless=True); page = b.new_page(locale='ko-KR')
    page.goto(f'https://m.blog.naver.com/{BLOG_ID}?tab=1', wait_until='domcontentloaded'); page.wait_for_timeout(4000)
    txt = page.evaluate('document.body.innerText'); b.close()
m = re.search(r'오늘\s*([\d,]+)\s*전체\s*([\d,]+)', txt)
if not m: print('방문자 숫자를 못 읽음'); sys.exit(1)
log = json.load(open(LOG, encoding='utf-8')) if os.path.exists(LOG) else {}
day = time.strftime('%Y-%m-%d')
log[day] = {'today': int(m.group(1).replace(',', '')), 'total': int(m.group(2).replace(',', '')), 'at': time.strftime('%H:%M')}
json.dump(log, open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
prev = [k for k in sorted(log) if k < day]
diff = f" (전체 어제보다 +{log[day]['total'] - log[prev[-1]]['total']})" if prev else ''
print(f"{day} {log[day]['at']} 오늘 {log[day]['today']} 전체 {log[day]['total']}{diff}")
