# H-1 설명 앞 줄 쉬운 말 교체(검수 09:26 요청, understand_test.md) — 앞 두 줄·카페 줄만, 옛 숫자는 계산 가정 칸으로 내림
import sys, json, os
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
sys.path.insert(0, W)
import ytupload, disclaim
H = os.path.dirname(os.path.abspath(__file__))
b = json.load(open(os.path.join(H, 'desc_before_1015.json'), encoding='utf-8'))
old = b['snippet']['description']
L = old.split('\n')
assert L[0].startswith('올림픽파크포레온(2024.11 입주)') and L[1].startswith('헬리오시티 2026년 2월 23.82억')
L[0] = '84㎡ 아파트 한 채 값은 헬리오시티 28억 5천만원쯤, 올림픽파크포레온 28억 2천만원쯤으로 거의 같았습니다. 올림픽파크포레온이 6년 가까이 더 새 아파트인데도 값은 비슷했습니다(국토교통부에 신고된 1년 치 거래 전부로 계산).'
L[1] = '헬리오시티는 2026년 2월에 23억 8천만원에 팔린 집이 있었지만, 같은 달 다른 3채는 30억~31억 5천만원에 팔렸습니다. 한 건만 보고 값을 판단하면 안 되는 이유입니다(투자 권유 아님).'
i = [k for k, l in enumerate(L) if l.startswith('세 동네 지도 단지 37곳')][0]
L[i] = '송파구 가락동·강동구 둔촌동·고덕동 아파트 37곳 값과 역·학교까지 걸어서 몇 m인지 전체 표(카페): https://cafe.naver.com/firemap'
j = [k for k, l in enumerate(L) if l.startswith('계산 가정:')][0]
L.insert(j + 1, '앞 줄 숫자 자세히: 84㎡대(전용 80~85㎡) 매매 가운데 값 헬리오시티 28.50억·올림픽파크포레온 28.25억, 평당 1억 1,087만원 vs 1억 1,017만원 · 같은 동네라도 지은 해가 다른 단지끼리는 평당 25% 넘게 갈림 · 헬리오시티 2026년 2월 23.82억(9층)은 중개거래·등기 마침 · 따로 떨어진 낮은 거래 2건(헬리오시티 5월 20.00억·올림픽파크포레온 9월 23.00억)은 직거래 신고 · 매물·호가 없이 신고된 거래와 오픈스트리트맵 걸음 거리만 씀(가상 인물 계산).')
new = '\n'.join(L)
assert disclaim.line(new) and len(new) < 5000
s = dict(b['snippet']); s['description'] = new
s = {k: s[k] for k in ('title', 'description', 'tags', 'categoryId', 'defaultLanguage', 'defaultAudioLanguage') if k in s}
open(os.path.join(H, 'desc_new_1015.txt'), 'w', encoding='utf-8').write(new)
if 'apply' in sys.argv:
    import f2_coupang
    f2_coupang.service().videos().update(part='snippet', body={'id': 'rVg0pQVo_wk', 'snippet': s}).execute()
    r = ytupload.service().videos().list(part='snippet,status', id='rVg0pQVo_wk').execute()['items'][0]
    json.dump(r, open(os.path.join(H, 'desc_after_1015.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('same' if r['snippet']['description'].strip() == new.strip() else 'DIFF', r['status']['publishAt'], r['snippet']['title'])
else:
    print(new[:900])
