# 10/19 회의 지시(공정위 추천·보증 심사지침 Ⅴ.6·A-31): 영상 안 대가 자막 없는 공개 영상 설명란에서 쿠팡 고지·링크 줄을 뺀다.
#   py -3.12 work/research/longform/loop/coupang1019/strip.py GMc2Rd1-JYA SCOI0DP-l-s scV67BQvC4Q
# 원본 설명은 before_<id>.txt로 먼저 남긴다(되돌리기: 그 파일로 videos.update). 영상 삭제·제목·태그·유료 표시 변경 없음.
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')
W = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'
sys.path.insert(0, W)
import f2_coupang
HERE = os.path.dirname(os.path.abspath(__file__))
yt = f2_coupang.service()
out = []
for vid in sys.argv[1:]:
    v = yt.videos().list(part='snippet', id=vid).execute()['items'][0]
    sn = v['snippet']; d = sn['description']
    open(os.path.join(HERE, f'before_{vid}.txt'), 'w', encoding='utf-8').write(d)
    keep = [l for l in d.split('\n') if not re.search(r'coupa\.ng|link\.coupang|쿠팡 파트너스 활동', l)]
    nd = re.sub(r'^\n+', '', '\n'.join(keep)); nd = re.sub(r'\n{3,}', '\n\n', nd)
    body = {'id': vid, 'snippet': {'title': sn['title'], 'description': nd, 'categoryId': sn['categoryId'], 'tags': sn.get('tags', []),
            'defaultLanguage': sn.get('defaultLanguage', 'ko'), 'defaultAudioLanguage': sn.get('defaultAudioLanguage', 'ko')}}  # 오디오 언어 빼면 en-US로 바뀐 적 있음(10/5)
    yt.videos().update(part='snippet', body=body).execute()
    chk = yt.videos().list(part='snippet', id=vid).execute()['items'][0]['snippet']
    ok = not re.search(r'coupa\.ng|link\.coupang|쿠팡', chk['description']) and chk['title'] == sn['title']
    print(vid, '되읽기', 'OK' if ok else '불일치', len(d), '->', len(chk['description']), '| 첫 줄:', chk['description'].split('\n')[0][:60])
    out.append({'id': vid, 'ok': ok})
json.dump(out, open(os.path.join(HERE, 'strip_result.json'), 'w', encoding='utf-8'), ensure_ascii=False)
