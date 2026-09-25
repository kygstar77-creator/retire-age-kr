# 후보 대상(종목·ETF·단지·제도)을 우리가 이미 쓴 적 있는지, 글을 쓰기 전에 본다.
# 왜 필요한가: 2026-09-25 23시 회차가 ACE 미국배당다우존스로 카페 묶음을 통째로 써 놓고
#   발행 직전에야 "같은 대상 이미 씀"으로 막혔다. 카페 84번 글이 같은 상품에 같은 각도
#   (세후 월 100만원·분배금 기록)를 이미 다뤘던 것이다. 그때까지 확인한 것은
#   오늘 나간 글과 내일 편성표뿐이었고, 우리 과거 글은 아무도 안 봤다.
#   naverpost.same_subject_today가 그 판단을 이미 할 수 있는데 발행 단계에서만 불렸다.
#   원고를 쓰기 전에 부르면 버리는 원고가 없다.
# 쓰는 법: py -3.12 work/dupcheck.py cafe SCHD JEPQ "ACE 미국배당다우존스"
#          py -3.12 work/dupcheck.py blog 버라이즌 리얼티인컴
#   demand.py로 수요를 잰 다음, 높은 후보부터 이걸로 걸러 첫 번째 '새 대상'을 고른다.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import naverpost as np


def main():
    if len(sys.argv) < 3:
        print('쓰는 법: py -3.12 work/dupcheck.py <cafe|blog> <후보1> <후보2> ...')
        return 1
    kind = sys.argv[1]
    if kind not in ('cafe', 'blog'):
        print('첫 인자는 cafe 또는 blog'); return 1
    fresh = []
    for cand in sys.argv[2:]:
        # 후보 이름만으로 제목 흉내를 내 같은 판단 함수에 넣는다
        hits = np.same_subject_today(kind, cand + ' 기록')
        if hits:
            raw, url, keys = hits[0]
            print(f'  씀   {cand}  ← {raw[:52]}')
            print(f'       {url}  (겹친 것: {", ".join(keys)})')
        else:
            print(f'  새것 {cand}')
            fresh.append(cand)
    print()
    if fresh:
        print('이 중에서 고른다(수요 높은 순으로 이미 정렬해 왔다면 맨 앞):', ' · '.join(fresh))
    else:
        print('후보가 전부 이미 쓴 대상이다. 후보를 더 뽑거나 각도를 완전히 바꾼다.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
