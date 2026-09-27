# SH(서울주택도시개발공사) 공고 첨부파일 내려받기 + 글자 추출.
# 사용: py -3.12 work/shfile.py "<SH 공고 view.do 주소>" <저장폴더>
# 2026-09-27: SH 첨부는 링크가 아니라 existFile('n') 자바스크립트로만 내려받아진다.
#   requests로 htmlConverter.do를 받으면 뷰어 껍데기(28KB)만 온다 — 그래서 Playwright로 누른다.
#   PDF 글자 추출은 pypdf. 일부 표 줄은 KSCms-UHC-H 인코딩이라 빠질 수 있다(473호 중 2줄) — 건수는 공고문 숫자와 맞춰 본다.
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
url, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(accept_downloads=True)
    pg.goto(url, timeout=60000)
    n = len(re.findall(r"existFile\('(\d+)'\)", pg.content()))
    for i in range(n):
        try:
            with pg.expect_download(timeout=60000) as d:
                pg.evaluate(f"existFile('{i}')")
            fn = os.path.join(out, d.value.suggested_filename)
            d.value.save_as(fn); print('받음', fn)
            if fn.lower().endswith('.pdf'):
                import pypdf
                t = '\n'.join(pg_.extract_text() or '' for pg_ in pypdf.PdfReader(fn).pages)
                open(fn[:-4] + '.txt', 'w', encoding='utf-8').write(t); print('  글자', len(t))
        except Exception as e:
            print('실패', i, e)
    b.close()
