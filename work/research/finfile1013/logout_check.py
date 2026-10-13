# 로그아웃 상태(새 브라우저 컨텍스트, 쿠키 없음)로 멤버공개 글을 열어 본문·첨부가 안 보이는지 본다.
# 사용: py -3.12 logout_check.py <글 주소>  → logout_*.png 캡처와 판정 한 줄
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
url = sys.argv[1]; H = os.path.dirname(os.path.abspath(__file__))
PROBES = ['금융소득_건보료_판정_2026', '쓰는 법', '근거 표는 세 덩어리', '343,594', '자주 묻는 질문', '회색 칸']
out = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, ua, vp in [('pc', None, {'width': 1280, 'height': 1600}),
                         ('mobile', 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1', {'width': 390, 'height': 1400})]:
        ctx = b.new_context(user_agent=ua, viewport=vp) if ua else b.new_context(viewport=vp)
        assert ctx.cookies() == []
        pg = ctx.new_page()
        u = url if name == 'pc' else re.sub(r'https://cafe\.naver\.com/', 'https://m.cafe.naver.com/', url)
        pg.goto(u, wait_until='domcontentloaded'); pg.wait_for_timeout(8000)
        texts = [pg.inner_text('body')] + [f.evaluate("() => document.body ? document.body.innerText : ''") for f in pg.frames if f != pg.main_frame]
        allt = '\n'.join(t for t in texts if t)
        shot = os.path.join(H, f'logout_{name}.png'); pg.screenshot(path=shot, full_page=True)
        hits = [k for k in PROBES if k in allt]
        out[name] = {'final_url': pg.url, 'shot': shot, 'body_probe_hits': hits, 'cookies_at_start': 0,
                     'login_wall': bool(re.search(r'멤버공개|카페 멤버만|가입|로그인', allt)), 'text_head': allt[:300]}
        ctx.close()
    b.close()
ok = all(not v['body_probe_hits'] for v in out.values())
json.dump(out, open(os.path.join(H, 'logout_check.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(('OK 본문·첨부 안 보임' if ok else 'BAD 본문·첨부가 보임'), json.dumps({k: (v['final_url'], v['body_probe_hits'], v['login_wall']) for k, v in out.items()}, ensure_ascii=False))
sys.exit(0 if ok else 1)
