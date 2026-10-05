# IndexNow 제출 — 사용자 사이트(kygstar77-creator.github.io) 페이지가 바뀌면 4곳에 같은 POST를 보낸다(README 5절).
# 사용: py -3.12 indexnow.py <URL> [URL ...]      URL 생략 시 아무것도 안 보냄
#       py -3.12 indexnow.py --sitemap <sitemap 주소>   sitemap의 <loc> 전부
# 키 파일은 공개 파일(비밀 아님). 구글은 IndexNow를 받지 않는다 → 서치콘솔이 따로 필요.
import sys, json, re, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HOST = 'kygstar77-creator.github.io'
KEY = '7fac259e36e5f4929ac442e7d451b11f'
ENDPOINTS = ('https://api.indexnow.org/indexnow', 'https://www.bing.com/indexnow',
             'https://yandex.com/indexnow', 'https://searchadvisor.naver.com/indexnow')


def from_sitemap(u):
    t = urllib.request.urlopen(u, timeout=20).read().decode('utf-8')
    return re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', t)


def submit(urls):
    urls = [u for u in urls if u.startswith(f'https://{HOST}/')]
    if not urls:
        print('보낼 URL 없음')
        return {}
    body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': f'https://{HOST}/{KEY}.txt',
                       'urlList': urls}).encode()
    out = {}
    for ep in ENDPOINTS:
        req = urllib.request.Request(ep, data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
        try:
            out[ep] = urllib.request.urlopen(req, timeout=20).status
        except urllib.error.HTTPError as e:
            out[ep] = e.code
        except Exception as e:  # 네트워크 오류는 코드 대신 이름
            out[ep] = type(e).__name__
        print(f'{out[ep]} {ep} ({len(urls)}개)')
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['--sitemap']:
        a = from_sitemap(a[1])
    submit(a)
