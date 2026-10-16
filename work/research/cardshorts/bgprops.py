# 쇼츠 실사 배경 props(디자인 기준 v3, 10/16 영상 디자인 총괄 — research/visual/design-spec-1016.md)
#   py -3.12 work/research/cardshorts/bgprops.py <편>   → work/video/<편>.json 에 bg(장면 뒤 실사 구간) 추가
# 재료: research/cardshorts/<편>/bg_plan.json(배경 담당이 눈으로 고른 Pexels 세로 영상, 얼굴·상표·워터마크 0, 시작 초·쓸 수 있는 길이)
# 규칙: 말 줄 경계에서 배경을 바꾸고, 한 배경은 최장 6초(DS.segMax, 경쟁 장면 길이 중앙 5.0초). 한 줄이 6초 넘으면 그 줄 안에서 나눈다.
#       클립은 고른 순서대로 돌려 쓰고, 다시 쓰면 지난번 끝난 곳부터(쓸 수 있는 길이를 넘으면 처음으로).
import os, sys, json, math
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(HERE, '..', '..', 'video'))
SEG_MAX = 180   # 프레임(6초)


def build(name):
    plan = json.load(open(os.path.join(HERE, name, 'bg_plan.json'), encoding='utf-8'))
    clips = [c for c in plan['clips'] if os.path.exists(os.path.join(VID, 'public', c['file']))]
    assert clips, '배경 클립 없음'
    pp = os.path.join(VID, name + '.json'); p = json.load(open(pp, encoding='utf-8'))
    pieces = []; a = 0
    for s in p['scenes']:
        lines = s['lines']; used = sum(l['frames'] for l in lines)
        for i, l in enumerate(lines):
            fr = l['frames'] + (s['frames'] - used if i == len(lines) - 1 else 0)   # 장면 끝 꼬리(TAIL)는 마지막 줄에
            k = max(1, math.ceil(fr / SEG_MAX))
            for j in range(k):
                d = fr // k + (fr % k if j == k - 1 else 0); pieces.append((a, d)); a += d
    total = sum(s['frames'] for s in p['scenes']); assert a == total, (a, total)
    # 짧은 조각(1.5초 미만)은 앞 조각에 붙인다 — 합쳐도 6초 넘지 않을 때만
    segs = []
    for st, d in pieces:
        if segs and d < 45 and segs[-1][1] + d <= SEG_MAX: segs[-1] = (segs[-1][0], segs[-1][1] + d)
        else: segs.append((st, d))
    pos = {c['file']: float(c.get('start', 0)) for c in clips}
    out = []
    for i, (st, d) in enumerate(segs):
        c = clips[i % len(clips)]; sec = d / 30; s0 = pos[c['file']]
        lim = float(c.get('start', 0)) + float(c.get('usable_sec', 6))
        if s0 + sec > lim + 0.01: s0 = float(c.get('start', 0))
        out.append({'src': c['file'], 'from': st, 'frames': d, 'start': round(s0, 2), 'kind': 'video'})
        pos[c['file']] = s0 + sec
    p['bg'] = out
    p['bg_credits'] = [{'id': c['id'], 'page': c['page'], 'author': c['author'], 'license': c.get('license', 'https://www.pexels.com/license/')} for c in clips if any(o['src'] == c['file'] for o in out)]
    json.dump(p, open(pp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{name}: 배경 {len(out)}구간 · 최장 {max(o["frames"] for o in out) / 30:.1f}초 · 클립 {len(p["bg_credits"])}개')
    return p


if __name__ == '__main__':
    for n in sys.argv[1:]: build(n)
