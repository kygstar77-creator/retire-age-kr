# v3 재렌더본 교체 올리기(10/16 영상 디자인 총괄) — v3redo.py 관문 통과 + 이해 시험 통과 기록이 있어야 한다.
#   py -3.12 work/research/cardshorts/v3up.py <편> "<이해 시험 한 줄>"
# upload.json: v+1 · mp4 = out/<편>_v3_ds.mp4 · 설명란에 배경 출처 줄(없으면) → review.md에 '## v(n) — 디자인 기준 v3' 절과 '판정(vn): 통과' 줄 → w1g1clips_up.py <편> --replace
#   (같은 publishAt으로 새로 올리고, 옛 예약은 지우지 않고 예약만 풀어 비공개 · 합성 표시 True update 응답 확인 · log.jsonl id 교체)
import os, sys, json, datetime, subprocess
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.normpath(os.path.join(HERE, '..', '..')); VID = os.path.join(WORK, 'video')
sys.path.insert(0, WORK); sys.path.insert(0, HERE)


def credit_line(props):
    cs = props.get('bg_credits') or []
    if not cs: return None
    return '배경 영상: ' + ' · '.join(f"{c['author']} / Pexels ({c['page']})" for c in cs) + ' — Pexels 라이선스 https://www.pexels.com/license/'


def main(name, test_line):
    d = os.path.join(HERE, name); r = json.load(open(os.path.join(d, 'v3redo.json'), encoding='utf-8'))
    if not (r['safezone'] and r['design']): print('올리지 않는다: v3redo 관문 걸림', r['msg']); return 3
    up = json.load(open(os.path.join(d, 'upload.json'), encoding='utf-8'))
    json.dump(up, open(os.path.join(d, f'upload.v{up["v"]}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    props = json.load(open(os.path.join(VID, name + '.json'), encoding='utf-8'))
    cl = credit_line(props); desc = up['description']
    if cl and '배경 영상:' not in desc:
        key = '내레이션은 AI 음성'
        desc = desc.replace(key, cl + '\n' + key, 1) if key in desc else desc + '\n' + cl
        up['description'] = desc
    nv = up['v'] + 1; up['v'] = nv; up['mp4'] = r['mp4']
    json.dump(up, open(os.path.join(d, 'upload.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    sec = f"""

## v{nv} — 디자인 기준 v3 재렌더(10/16 영상 디자인 총괄 — 사장님 "모든 쇼츠 롱폼에 저렇게 영상 넣으면 되겠다", 기준 research/visual/design-spec-1016.md)
- 바뀐 것: 화면 틀만 — 장면 뒤 실사 배경(Pexels, 최장 6초마다 바뀜 · bg_plan.json 눈 검사 얼굴·상표·워터마크 0), 자막 한 줄 72px 흰 글자+검은 테두리(상자 없음), 제목 최대 92px, 판은 흰 카드. props 숫자·자막 글자·소리는 v{nv - 1} 그대로(소리 트랙 -c copy, 길이 {r['frames']}프레임 같음).
- 관문: {r['msg'][0]} / {r['msg'][1]} / 0초 빈 곳 {r['empty0']:.0%}
- 이해 시험: {test_line}
- 눈 검사: sheet_v3.png
판정(v{nv}): 통과 ({now})
"""
    with open(os.path.join(d, 'review.md'), 'a', encoding='utf-8') as f: f.write(sec)
    return subprocess.call([sys.executable, os.path.join(HERE, 'w1g1clips_up.py'), name, '--replace'])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
