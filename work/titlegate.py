# 카페 제목 후보를 심사에 보내기 전에 기계 관문부터 본다.
# 10/12 22시 m1stot1013: 심사 통과안 셋이 차례로 카페 틀 v2(왜·는데)·readcheck(숫자·길이)에 걸려
# 제미나이·레드팀 심사를 세 번 다시 돌렸다. 후보를 여기 먼저 넣고 '통과'만 심사에 보낸다.
# 쓰는 법: py -3.12 work/titlegate.py "후보1" "후보2" ...
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import readcheck, naverpost


# 10/16 벤치마크 2판 ④: 우리 카페 제목 연도·날짜 0/20(남 9/38). '2026 OO'(검색 40~480)은 검색어 원형(국민연금수령나이 49,980)보다 훨씬 적어 맨 앞엔 두지 않는다.
DATED = re.compile(r'20\d\d|\d{1,2}월|\d{1,2}일|올해|작년|내년|이번 달')


def frame(t):
    """aitell.frame_check의 제목 줄만(쉼표 하루 규칙은 slot이 있어야 해서 뺌).
    기준 리뉴얼 D-20·D-21(10/19): '물음은 얼마·몇만'·'왜·~는데 금지'는 뺐다(상위 카페 제목 3,908개: 물음 1.04배·이유·왜 1.09배).
    D-23: 30자 넘으면 참고 줄만(막지 않음, 상위 제목 중앙 20자)."""
    core = re.sub(r"[\s\)\]\.!·~…\"']+$", '', t)
    if len(core) > 30: print(f'   · 참고(막지 않음): {len(core)}자 — 30자 넘음(D-23, 상위 카페 제목 중앙 20자)')
    return []


def gate(t):
    bad = frame(t)
    try: bad += [str(x) for x in (readcheck.title_check(t) or [])]
    except Exception as e: bad.append('readcheck 실패 ' + repr(e)[:60])
    ks = naverpost.subject_keys(t)
    hits = naverpost.same_subject_today('cafe', t)
    if hits: bad += [f'발행기 겹침 {h[2]} — {h[0][:30]}' for h in hits]
    return ks, bad


if __name__ == '__main__':
    for t in sys.argv[1:]:
        ks, bad = gate(t)
        print(('통과' if not bad else '걸림') + f' · {len(t)}자 · 대상 {sorted(ks) or "-"} · {t}')
        for b in bad: print('   -', b)
        if not DATED.search(t): print('   · 참고(막지 않음): 연도·날짜 없음 — 시점이 있는 글(시행일·기준일·종가 날)이면 검색어 뒤에 넣기. 남 9/38·우리 0/20, 10편 중 3편 목표(copywriter 10/16)')
