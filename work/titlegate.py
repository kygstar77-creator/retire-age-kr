# 카페 제목 후보를 심사에 보내기 전에 기계 관문부터 본다.
# 10/12 22시 m1stot1013: 심사 통과안 셋이 차례로 카페 틀 v2(왜·는데)·readcheck(숫자·길이)에 걸려
# 제미나이·레드팀 심사를 세 번 다시 돌렸다. 후보를 여기 먼저 넣고 '통과'만 심사에 보낸다.
# 쓰는 법: py -3.12 work/titlegate.py "후보1" "후보2" ...
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import readcheck, naverpost


def frame(t):
    """aitell.frame_check의 제목 줄만(쉼표 하루 규칙은 slot이 있어야 해서 뺌)."""
    core = re.sub(r"[\s\)\]\.!·~…\"']+$", '', t)
    if re.search(r'왜|는데', t): return ['반전 연결(왜·~는데) — 카페 틀 v2 금지']
    if (t.endswith('?') or re.search(r'(까|나요|가요|죠|요|니다)$', core)) and not re.search(r'얼마|몇', t):
        return ['물음 제목은 얼마·몇만']
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
