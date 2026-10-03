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

GENERIC_HEAD = {'오늘의', '오늘', '이번', '다음', '지난', '내일', '이번주', '다음주', '지난주', '올해', '내년', '서울', '미국', '한국'}
RESEARCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research')


def local_hits(kind, cand, days=14):
    """발행된 우리 묶음(published.txt 있는 것)의 제목과 본문 조각에서 후보를 찾는다.
    2026-09-27 13시 회차: 네이버 제목만 보던 판단이 두 번 놓쳤다.
      - '레나' — 카페 104번 제목은 "버크셔가 52주 최저가 근처에서 사흘 연속 담은 종목"이라 이름이 본문에만 있었다.
      - '다음 주 미국 실적 캘린더' — 카페 82번·100번이 "다음 주 미국 증시 일정…"으로 같은 주를 이미 다뤘다.
    그래서 (1) 후보가 제목·첫 조각에 있거나 본문에 3번 이상 나오거나 (2) 후보 낱말(2자 이상)의 3/4 이상이 제목에 있으면 겹친 것으로 본다."""
    import glob, time, re
    piece = 'c0*.txt' if kind == 'cafe' else 'b0*.txt'
    words = [w for w in re.split(r'\s+', cand) if len(w) >= 2]
    flat = re.sub(r'\s+', '', cand)
    out = []
    for pub in glob.glob(os.path.join(RESEARCH, '*', 'pkg', 'published.txt')):
        if time.time() - os.path.getmtime(pub) > days * 86400: continue
        pkg = os.path.dirname(pub)
        parts = glob.glob(os.path.join(pkg, piece))
        if not parts: continue
        try:
            title = open(os.path.join(pkg, 'title.txt'), encoding='utf-8').read().strip()
            body = ''.join(open(p, encoding='utf-8').read() for p in parts)
            url = open(pub, encoding='utf-8').read().split()[0]
        except Exception:
            continue
        first = sorted(parts)[0]
        lead = re.sub(r'\s+', '', title + open(first, encoding='utf-8').read())
        n_body = re.sub(r'\s+', '', body).count(flat) if flat else 0
        # 본문에 한 번 스친 이름(쉐브론 글 속 리얼티인컴)은 겹친 게 아니다 — 제목·첫 조각에 있거나 본문에 3번 이상
        if flat and (flat in lead or n_body >= 3):
            out.append((title, url, '제목·첫 조각에 있음' if flat in lead else '본문에 %d번' % n_body))
        elif len(words) >= 2 and sum(w in title for w in words) * 4 >= len(words) * 3:
            out.append((title, url, '제목 낱말 %d/%d 겹침' % (sum(w in title for w in words), len(words))))
        # 2026-09-27 23시 회차: 카페 후보 "리얼티인컴 O 배당 이력 배당락 지급일"이 '새것'으로 나왔는데
        # 카페에 리얼티인컴 글이 이미 셋(o0925·odiv136·realtyo) 있었다. 제목 낱말이 3/5라 3/4 기준에 못 미쳤다.
        # 후보의 첫 낱말은 대상(종목·상품) 자체다. 일반어가 아니면, 일주일 안에 나간 제목에
        # (띄어쓰기 무시) 들어 있을 때 겹친 것으로 본다. '이번'·'오늘의' 같은 머리말은 대상이 아니라 뺀다.
        elif (words and words[0] not in GENERIC_HEAD
              and time.time() - os.path.getmtime(pub) <= 7 * 86400 and words[0] in re.sub(r'\s+', '', title)):
            out.append((title, url, '일주일 안에 같은 대상(%s)이 제목에 있음' % words[0]))
    return out


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
        local = local_hits(kind, cand)
        # 2026-10-03 16시 write: 첫 겹침 하나만 찍어서 '정기예금 금리'가 애플 글(#77, 비교로 한 번 스침)로만 나왔고
        # 같은 공시·같은 각도의 #139(9/28 "정기예금 금리, 길게 묶으면 더 줄까?")를 못 봤다 — 겹친 글을 전부(최대 6) 찍는다.
        if hits or local:
            print(f'  씀   {cand}  — 겹친 글 {len(hits) + len(local)}개')
            for raw, url, keys in hits[:3]:
                print(f'       ← {raw[:52]}  {url}  (겹친 것: {", ".join(keys)})')
            seen = {h[1] for h in hits}
            for title, url, why in [x for x in local if x[1] not in seen][:6]:
                print(f'       ← {title[:52]}  {url}  ({why})')
        else:
            print(f'  새것 {cand}')
            fresh.append(cand)
            # 2026-09-28 04시 회차: "건강보험료 피부양자"는 새것으로 나왔는데 "피부양자"만 넣으면
            # 카페 78번(9/24, 같은 별표를 다룬 글)이 잡혔다. 첫 낱말이 제목에 없어서 놓친 것이다.
            # 여러 낱말 후보는 낱말마다 다시 보고, 걸리면 '각도를 바꿔야 할 수 있음'으로 알린다.
            ws = [w for w in cand.split() if len(w) >= 3 and w not in GENERIC_HEAD]
            if len(ws) >= 2:
                for w in ws:
                    part = local_hits(kind, w)
                    if part:
                        title, url, why = part[0]
                        print(f'       ↳ 낱말 "{w}"로는 겹침 ← {title[:48]}  {url} ({why}) — 각도가 다른지 확인')
                        break
    print()
    if fresh:
        print('이 중에서 고른다(수요 높은 순으로 이미 정렬해 왔다면 맨 앞):', ' · '.join(fresh))
    else:
        print('후보가 전부 이미 쓴 대상이다. 후보를 더 뽑거나 각도를 완전히 바꾼다.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
