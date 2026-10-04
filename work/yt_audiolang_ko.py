"""defaultAudioLanguage가 비거나 ko가 아닌 영상을 ko로 고친다(10/5 patrol 실측). 다른 snippet 필드는 그대로 다시 보낸다.
사용: py -3.12 work/yt_audiolang_ko.py <videoId> ...  (원본 snippet은 longform/loop/lang_before_<id>.json에 백업)"""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
import f2_coupang
D = os.path.join(os.path.dirname(__file__), 'research', 'longform', 'loop')

def main(ids):
    yt = f2_coupang.service()
    for vid in ids:
        sn = yt.videos().list(part='snippet', id=vid).execute()['items'][0]['snippet']
        json.dump(sn, open(os.path.join(D, f'lang_before_{vid}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        if sn.get('defaultAudioLanguage') == 'ko': print('이미 ko', vid); continue
        new = {k: sn[k] for k in ('title', 'description', 'categoryId') if k in sn}
        if 'tags' in sn: new['tags'] = sn['tags']
        if 'defaultLanguage' in sn: new['defaultLanguage'] = sn['defaultLanguage']
        new['defaultAudioLanguage'] = 'ko'
        yt.videos().update(part='snippet', body={'id': vid, 'snippet': new}).execute()
        c = yt.videos().list(part='snippet', id=vid).execute()['items'][0]['snippet']
        ok = c.get('defaultAudioLanguage') == 'ko' and all(c.get(k) == sn.get(k) for k in ('title', 'description', 'categoryId', 'tags', 'defaultLanguage'))
        print(vid, '되읽기', 'OK' if ok else '불일치')

if __name__ == '__main__':
    main(sys.argv[1:])
