# cafeedit.py 시험(2026-10-01, 브라우저·네트워크 없이): py -3.12 work/test_cafeedit.py
import os, sys, json, tempfile, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cafeedit as C
sys.stdout.reconfigure(encoding='utf-8')

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', 'editor', '2026-10-01', 'cafe')
html = open(os.path.join(D, '44.html.orig'), encoding='utf-8').read()
subj = '가구 순자산 상위 10%는 11억 20만원, 중앙값은 2억 3,860만원'
tmp = tempfile.mkdtemp()
def w(name, s):
    p = os.path.join(tmp, name); open(p, 'w', encoding='utf-8').write(s); return p
new = open(os.path.join(D, '44.txt'), encoding='utf-8').read()

# 1) 첫 대상 44: 사진 3장 자리 그대로, 글 덩어리 3개, 숫자 동일
p = C.plan(44, os.path.join(D, '44.txt'), subj, html)
assert p['layout'] == ['image', 'text', 'image', 'text', 'image', 'text'], p['layout']
assert len(p['images']) == 3 and len(p['blocks']) == 3
assert p['blocks'][1][0] == '10억원 이상 가구는 11.8%입니다' and p['blocks'][2][0] == '가구주 나이별로는 차이가 큽니다'
assert C.norm(subj) not in C.norm(p['blocks'][0][0])           # 원고 첫 줄 제목은 본문에 안 들어간다
# 2) 되돌리기 길: 원본 원고(.orig)로도 같은 계획이 선다
assert len(C.plan(44, os.path.join(D, '44.txt.orig'), subj, html)['blocks']) == 3
# 3) 숫자가 바뀌면 거절
try: C.plan(44, w('n.txt', new.replace('0.625', '0.626')), subj, html); assert False
except ValueError as e: assert '숫자' in str(e)
# 4) 소제목(닻)이 바뀌면 사진 자리를 못 정하니 거절
try: C.plan(44, w('a.txt', new.replace('가구주 나이별로는 차이가 큽니다', '나이별로 보면')), subj, html); assert False
except ValueError as e: assert '사진 자리' in str(e)
# 5) 쿠팡 링크 원고 거절
try: C.plan(44, w('c.txt', new + '\nhttps://link.coupang.com/x'), subj, html); assert False
except ValueError as e: assert '쿠팡' in str(e)
# 6) 적용 뒤 대조: 같은 사진·새 글이면 통과, 사진 주소가 바뀌면 실패
def fake(blocks, imgs):
    out = ''
    for k in p['layout']:
        if k == 'image': out += f'<div class="se-component se-image"><img src="{imgs.pop(0)}?type=w800"></div>'
        else: out += '<div class="se-component se-text">' + ''.join(f'<p class="se-text-paragraph">{l}</p>' for l in blocks.pop(0)) + '</div>'
    return out
assert C.compare_after(p, fake([b[:] for b in p['blocks']], p['images'][:])) == []
assert C.compare_after(p, fake([b[:] for b in p['blocks']], ['x'] + p['images'][1:]))
assert C.compare_after(p, fake([b[:] for b in p['old']], p['images'][:]))   # 옛 글 그대로면 실패
# 7) editor 통과 표시: 없으면 거절, 있으면 통과, 뒤에 원고가 바뀌면 거절
t = w('ok.txt', new)
assert not C.check_ok(t, C.plan(44, t, subj, html)['sha_txt'])[0]
C.mark_ok(t, 'firemap-editor'); assert C.check_ok(t, C.plan(44, t, subj, html)['sha_txt'])[0]
open(t, 'a', encoding='utf-8').write('\n')
assert not C.check_ok(t, C.plan(44, t, subj, html)['sha_txt'])[0]
# 8) 하루 상한: 적용된 것만 센다(dry는 안 셈)
C.LOG = os.path.join(tmp, 'log.jsonl'); now = datetime.datetime.now().isoformat(timespec='seconds')
for a in (True, True, False, True): C.log({'at': now, 'applied': a})
C.log({'at': '2000-01-01T00:00:00', 'applied': True})
assert C.edits_today() == 3 and C.EDIT_CAP == 3
print('test_cafeedit: ok')
