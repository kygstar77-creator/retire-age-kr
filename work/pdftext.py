# -*- coding: utf-8 -*-
"""PDF 원문에서 글자를 뽑는다.
WebFetch는 PDF를 주면 "읽을 수 없다"고 답하는 일이 잦다(2026-09-23 제이피모간 배당 캘린더).
운용사 배당 캘린더·정부 보도자료·공시는 PDF로만 나오는 경우가 많아 직접 뽑아 쓴다.

  python work/pdftext.py <URL 또는 파일경로> [페이지수]

출력은 UTF-8로 고정한다(윈도우 cp949에서 ©·— 때문에 죽는 것을 막는다).
"""
import io, os, sys, urllib.request

def load(src):
    if src.startswith('http'):
        req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
        return io.BytesIO(urllib.request.urlopen(req, timeout=60).read())
    return open(src, 'rb')

def main():
    if len(sys.argv) < 2:
        print(__doc__); return 1
    src = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader
    r = PdfReader(load(src))
    pages = r.pages if not limit else r.pages[:limit]
    print('페이지 %d장 중 %d장' % (len(r.pages), len(pages)))
    for i, pg in enumerate(pages):
        print('=== %d쪽 ===' % (i + 1))
        print(pg.extract_text() or '(글자 없음 - 스캔 이미지일 수 있다)')
    return 0

if __name__ == '__main__':
    sys.exit(main())
