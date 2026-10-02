# 롱폼 설명란 챕터 시각을 props json(장면 frames 순서대로 이어 붙임)에서 계산해 meta.json desc의 {CHAPTERS} 자리에 넣는다.
#   py -3.12 work/video/chapters.py <props.json> <ep폴더>        # meta.json의 "chapters": [[장면번호, "제목"], ...] 사용
#   --dry 를 붙이면 meta.json을 바꾸지 않고 출력만
# 장면 사이 겹침이 없는 구성(E2.tsx·N1.tsx: from = 앞 장면 frames 합)에만 맞다. 목소리 넣은 뒤 props를 다시 만든 다음 돌린다.
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

def main(pj, ep, dry=False):
    p = json.load(open(pj, encoding='utf-8')); fps = p['fps']
    starts, acc = [], 0
    for s in p['scenes']: starts.append(acc); acc += s['frames']
    mp = os.path.join(ep, 'meta.json'); m = json.load(open(mp, encoding='utf-8'))
    lines = []
    for idx, title in m['chapters']:
        t = starts[idx] // fps
        lines.append(f'{t // 60}:{t % 60:02d} {title}')
    out = '\n'.join(lines)
    print(out); print(f'전체 {acc / fps / 60:.1f}분 · 목소리 없는 문장 {p.get("missing")}')
    if dry: return
    tpl = m.get('desc_tpl') or m['desc']
    if '{CHAPTERS}' not in tpl: sys.exit('desc_tpl에 {CHAPTERS} 자리가 없다')
    m['desc_tpl'] = tpl; m['desc'] = tpl.replace('{CHAPTERS}', out)
    json.dump(m, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('meta.json desc 챕터 채움')

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if x != '--dry']
    main(a[0], a[1], '--dry' in sys.argv)
