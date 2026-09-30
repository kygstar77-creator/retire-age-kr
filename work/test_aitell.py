# aitell.py 시험(2026-10-01): py -3.12 work/test_aitell.py
import os, sys, time, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aitell
sys.stdout.reconfigure(encoding="utf-8")

# 1) 평범한 사람 글은 통과
human = '압구정 현대 전용 84는 석 달에 한 건 팔렸다. 값은 52억. 작년 이맘때보다 7억 올랐다. 근데 옆 단지는 거래가 없었다. 왜일까.'
assert aitell.score(human)[0] <= aitell.LIMIT_SHORT, aitell.score(human)
# 2) AI 말·설명조가 쌓이면 걸린다
ai = '결론적으로 다양한 측면에서 살펴보겠습니다. 또한 쉽게 말해 핵심은 현명한 판단입니다. Let us delve into it.'
v, hits, n = aitell.score(ai)
assert v > aitell.LIMIT_SHORT and any('결론적으로' in h for h in hits) and any('delve' in h for h in hits), (v, hits)
# 3) '~요' 연속·쏠림
yo = ' '.join(f'{i}월에는 값이 {i}억 올랐어요.' for i in range(1, 13))
v, hits, _ = aitell.score(yo)
assert any("'~요'" in h for h in hits), hits
# 4) 평어체 '~다'는 끝 두 음절이 달라지면 벌점 없음(블로그 기본 말투)
flat = '값은 52억이다. 거래는 한 건이었다. 옆 단지는 조용했다. 작년보다 올랐다. 이유는 재건축이다.'
assert not any('끝 두 음절' in h for h in aitell.score(flat)[1]), aitell.score(flat)
# 5) 관문: 기준 넘는 묶음은 거절, 편집 통과 표시가 있으면 통과, 표시 뒤 원고가 바뀌면 다시 거절
d = tempfile.mkdtemp()
open(os.path.join(d, 'title.txt'), 'w', encoding='utf-8').write('시험')
open(os.path.join(d, 'order.txt'), 'w', encoding='utf-8').write('c00.txt\n')
open(os.path.join(d, 'c00.txt'), 'w', encoding='utf-8').write(ai * 3)
assert aitell.gate_pkg(d)[0] is False
aitell.main(['pass', d, 'firemap-editor'])
assert aitell.gate_pkg(d)[0] is True
time.sleep(1.2); open(os.path.join(d, 'c00.txt'), 'a', encoding='utf-8').write('\n또한 추가.')
os.utime(os.path.join(d, 'c00.txt'), (time.time() + 5, time.time() + 5))
ok, msg, _ = aitell.gate_pkg(d)
assert ok is False and '바뀐 조각' in msg, msg
assert aitell.main(['gate', d]) == 4
# 6) 짧은 글(유튜브 제목·쿠팡 라벨)
assert aitell.gate_text('은퇴까지 몇 년 남았을까?')[0]
assert not aitell.gate_text('결론적으로 다양한 측면에서 핵심은 현명한 투자')[0]
assert aitell.gate_text('결론적으로 다양한 측면에서 핵심은 현명한 투자', ok_flag=True)[0]
print('test_aitell: ok')
