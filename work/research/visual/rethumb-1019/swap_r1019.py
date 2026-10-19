# 10/19 저조 롱폼 썸네일 교체 — 판정(decisions.json)대로 thumbnails.set(f2_coupang 관리 토큰) → i.ytimg.com에서 다시 받아 바뀐 것 확인.
#   제목·설명·영상은 건드리지 않는다(thumbnails.set만 부른다). 키·토큰은 출력하지 않는다.
#   py -3.12 swap_r1019.py            # 교체 + 확인 → judge/swap_log.json
import sys, os, json, time, hashlib, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(H, '..', '..', '..'))
sys.path.insert(0, WORK)
EPD = os.path.join(WORK, 'research', 'longform', 'ep')
D = json.load(open(os.path.join(H, 'decisions.json'), encoding='utf-8'))


def md5url(u):
    try: return hashlib.md5(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read()).hexdigest()
    except Exception as e: return f'ERR {e}'


def main():
    import f2_coupang
    from googleapiclient.http import MediaFileUpload
    yt = f2_coupang.service(); log = []
    for d in D:
        if d['pick'] in ('', 'keep'): continue
        p = os.path.join(EPD, d['folder'], f"thumb_{d['pick']}.png")
        before = md5url(f"https://i.ytimg.com/vi/{d['id']}/maxresdefault.jpg?b={int(time.time())}")
        r = yt.thumbnails().set(videoId=d['id'], media_body=MediaFileUpload(p, mimetype='image/png')).execute()
        log.append({'id': d['id'], 'key': d['key'], 'pick': d['pick'], 'set_at': time.strftime('%Y-%m-%d %H:%M'), 'api_maxres': r['items'][0].get('maxres', {}).get('url', ''), 'md5_before': before})
        print('set', d['key'], d['id'], d['pick'])
    time.sleep(20)
    for l in log:
        l['md5_after'] = md5url(f"https://i.ytimg.com/vi/{l['id']}/maxresdefault.jpg?a={int(time.time())}")
        l['changed'] = l['md5_after'] != l['md5_before'] and not l['md5_after'].startswith('ERR')
        print(l['key'], l['md5_before'][:8], '→', l['md5_after'][:8], '바뀜' if l['changed'] else '아직 같음')
    json.dump(log, open(os.path.join(H, 'judge', 'swap_log.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
