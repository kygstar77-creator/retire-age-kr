# 새 묶음 폴더를 만든다. 이미 있는 이름이면 거부한다.
# 실행: py -3.12 work/newpkg.py <이름>
# 만든 이유(2026-09-23 22시 회차): 이미 발행까지 끝난 묶음 이름(jeonseratio)을 그대로 골라
# facts.txt·title.txt·order.txt를 덮어썼다. git으로 되돌렸지만 발행 기록을 날릴 뻔했다.
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research')


def make(slug):
    d = os.path.join(ROOT, slug)
    if os.path.exists(d):
        pub = os.path.join(d, 'pkg', 'published.txt')
        state = '이미 발행됨' if os.path.exists(pub) else '아직 대기'
        cand = next(s for s in (slug + str(i) for i in range(2, 99))
                    if not os.path.exists(os.path.join(ROOT, s)))
        raise SystemExit('거부: %s 이(가) 이미 있다 (%s). 덮어쓰지 말고 다른 이름을 써라 — 예: %s' % (slug, state, cand))
    os.makedirs(os.path.join(d, 'pkg', 'img'))
    print(d)
    return d


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('사용법: py -3.12 work/newpkg.py <이름>')
    make(sys.argv[1])
