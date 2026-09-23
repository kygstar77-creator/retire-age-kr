# 정부 보도자료 첨부파일(통계표 엑셀·HWP·PDF) 내려받기.
# 2026-09-24 회차에서 막혀서 만들었다. 같은 파일인데 korea.kr 경로는 HTML(로그인/차단 안내)을
# 돌려주고, 기관 사이트(mods.go.kr 등) 경로에 Referer를 붙이면 진짜 파일이 온다.
# eGovFrame board.es / boardDownload.es 를 쓰는 기관은 전부 같은 모양이다.
#
#   py -3.12 work/govfile.py list https://mods.go.kr/board.es?mid=a10301010000&bid=215&list_no=439535&act=view
#   py -3.12 work/govfile.py get  <같은 주소> <seq> [저장폴더]
#
# 파이썬에서:
#   from govfile import attachments, download
import os, re, sys, urllib.parse, urllib.request

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36'
# 앞 4~8바이트로 실제 형식을 알아낸다. 확장자를 서버가 안 알려줄 때가 많다.
SIGS = [(b'%PDF', '.pdf'), (b'PK\x03\x04', '.zip'), (b'\xd0\xcf\x11\xe0', '.hwp'), (b'<!DO', '.html'), (b'<htm', '.html')]


def _open(url, referer=None, timeout=60):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    if referer:
        req.add_header('Referer', referer)
    return urllib.request.urlopen(req, timeout=timeout)


def attachments(page_url, timeout=60):
    """보도자료 화면에서 첨부 목록을 뽑는다. [{'seq','name','url'}] 을 돌려준다."""
    html = _open(page_url, timeout=timeout).read().decode('utf-8', 'replace')
    base = urllib.parse.urlsplit(page_url)
    origin = f'{base.scheme}://{base.netloc}'
    out, seen = [], set()
    for m in re.finditer(r'href="([^"]*boardDownload\.es[^"]*)"[^>]*>(.*?)</a>', html, re.S | re.I):
        href, label = m.group(1), re.sub(r'<[^>]+>', ' ', m.group(2))
        url = href if href.startswith('http') else origin + href
        if url in seen:
            continue
        seen.add(url)
        seq = re.search(r'seq=(\d+)', url)
        out.append({'seq': seq.group(1) if seq else '', 'name': ' '.join(label.split())[:120], 'url': url})
    return out


def _looks_html(data, content_type=''):
    """차단·안내 화면이 파일인 척 오는 걸 잡는다. BOM·공백·주석으로 시작하는 HTML도 걸린다."""
    if 'html' in (content_type or '').lower():
        return True
    head = data[:600].lstrip(bytes([0xEF,0xBB,0xBF,0x20,0x09,0x0D,0x0A])).lower()
    return head.startswith(b'<!doctype') or head.startswith(b'<html') or head.startswith(b'<?xml') and b'<html' in data[:2000].lower()


def _ext(head, fallback=''):
    for sig, ext in SIGS:
        if head.startswith(sig):
            # hwpx·xlsx·docx는 전부 zip이다. zip 안을 봐야 갈린다.
            return ext
    return fallback


def download(file_url, out_dir='.', referer=None, stem=None, timeout=180):
    """첨부 하나를 내려받고 실제 형식에 맞는 확장자를 붙여 저장한다. 경로를 돌려준다.
    HTML이 오면(차단·안내 화면) RuntimeError 를 낸다 — 엑셀인 줄 알고 파싱하다 죽는 걸 막는다."""
    os.makedirs(out_dir, exist_ok=True)
    referer = referer or file_url.split('boardDownload.es')[0]
    with _open(file_url, referer=referer, timeout=timeout) as r:
        data = r.read()
        cd = r.headers.get('Content-Disposition') or ''
        ct = r.headers.get('Content-Type') or ''
    if _looks_html(data, ct):
        raise RuntimeError(f'파일 대신 HTML이 왔다({len(data)}바이트) — 기관 사이트 주소와 Referer를 확인할 것: {file_url}')
    ext = _ext(data[:8])
    if ext == '.zip':
        ext = '.xlsx' if b'xl/workbook.xml' in data[:6000] or b'xl/' in data[:4000] else '.hwpx'
        if b'word/' in data[:4000]:
            ext = '.docx'
    name = re.search(r'filename="?([^";]+)', cd)
    stem = stem or (os.path.splitext(os.path.basename(urllib.parse.unquote(name.group(1))))[0] if name else '')
    stem = re.sub(r'[\/:*?"<>|]', '_', stem).strip() or ('att_' + (re.search(r'seq=(\d+)', file_url).group(1) if 'seq=' in file_url else 'file'))
    path = os.path.join(out_dir, stem + ext)
    with open(path, 'wb') as f:
        f.write(data)
    return path


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__ or '', '\n사용법: govfile.py list <보도자료주소> | govfile.py get <보도자료주소> <seq> [저장폴더]')
        sys.exit(1)
    cmd, page = sys.argv[1], sys.argv[2]
    if cmd == 'list':
        for a in attachments(page):
            print(f"seq={a['seq']:>3}  {a['name']}")
            print(f"        {a['url']}")
    elif cmd == 'get':
        seq = sys.argv[3]
        out = sys.argv[4] if len(sys.argv) > 4 else '.'
        hit = [a for a in attachments(page) if a['seq'] == seq]
        if not hit:
            print(f'seq={seq} 없음'); sys.exit(2)
        print(download(hit[0]['url'], out, referer=page))
