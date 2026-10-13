"""칸 장부(research/slots.json)의 앞으로 올 카페 칸 시각을 각 묶음 pkg/slot.txt에 맞춘다.

2026-10-13 21:2x: 카페 칸이 하루 12개(90분 간격)로 바뀌었는데(36e3940) 장부만 고치고 slot.txt는 옛 2시간 칸
그대로였다. 10/14 배정 8편이 전부 '두 시각 다름' — 06:10 칸 글이 08시에 나갈 뻔했다. 발행기는 slot.txt만 본다.
칸표를 바꾸거나 배정을 옮긴 사람은 이걸 한 번 돌린다.

  py -3.12 work/slotsync.py        # 어긋난 것만 보여 준다
  py -3.12 work/slotsync.py --fix  # slot.txt를 장부 시각으로 고친다
"""
import datetime, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, 'research')


def main(fix):
    sl = json.load(open(os.path.join(RES, 'slots.json'), encoding='utf-8'))
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    n = 0
    for s in sl.get('slots', []):
        item, at = s.get('item') or '', s.get('at') or ''
        if s.get('skip') or at < now or not item or item.startswith('TBD'):
            continue
        pkg = os.path.join(RES, item, 'pkg')
        if not os.path.isdir(pkg):
            continue
        f = os.path.join(pkg, 'slot.txt')
        cur = open(f, encoding='utf-8').read().strip()[:13] if os.path.exists(f) else ''
        want = at[:13]
        if cur == want:
            continue
        n += 1
        print('%s  %s  slot.txt %s -> %s' % (at, item, cur or '(없음)', want))
        if fix:
            open(f, 'w', encoding='utf-8').write(want + '\n')
    print('어긋남 %d건%s' % (n, ' 고침' if fix and n else ''))


if __name__ == '__main__':
    main('--fix' in sys.argv)
