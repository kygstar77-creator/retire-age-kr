# 편집 통과 해시 관문(2026-10-02, 대역 지시 10/1 21:35) — 편집자가 통과시킨 원고와 실제로 나가는 원고가 같은지 본다.
# 10/2 카페 190: 06:40 통과본과 08:28 공개본 해시가 달랐다(editor 10:50 확인). 통과 뒤에 제목·조각을 바꾸면 통과가 아니다.
# 해시 = title.txt + c??.txt(이름순) 파일 바이트를 그대로 이어 붙인 sha256 — editor가 10/2 07:43부터 쓰는 방식(e1table1002·b10cafe1002 재현).
#   py -3.12 work/editgate.py check <pkg>                지금 원고가 .edit.json과 같은지
#   py -3.12 work/editgate.py stamp <pkg> <by> [note]    편집 통과 표시(.edit.json)를 이 방식으로 찍는다
import os, re, sys, json, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, 'research', 'editor', 'gate-refusals.md')


def files(pkg):
    cs = sorted(f for f in os.listdir(pkg) if re.fullmatch(r'c\d\d\.txt', f))
    return [os.path.join(pkg, f) for f in ['title.txt'] + cs if os.path.exists(os.path.join(pkg, f))]


def sha(pkg):
    return hashlib.sha256(b''.join(open(f, 'rb').read() for f in files(pkg))).hexdigest()


def mark_path(pkg):
    pkg = pkg.rstrip('/\\')
    for p in [pkg + '.edit.json', os.path.join(pkg, '.edit.json')]:
        if os.path.exists(p): return p
    return None


def check(pkg):
    """(ok, 이유). 표시가 없으면 ok=None — 대조할 것이 없다(막을지는 부르는 쪽이 정한다)."""
    p = mark_path(pkg)
    if not p: return None, '편집 통과 표시(.edit.json) 없음'
    try: d = json.load(open(p, encoding='utf-8'))
    except Exception as e: return False, f'.edit.json을 못 읽음: {e}'
    want, now = d.get('sha'), sha(pkg)
    fs = d.get('files')
    if isinstance(fs, dict) and fs:  # 10/2 06:40 방식: 파일마다 sha256 — 표시에 적힌 파일이 하나라도 다르면 불일치
        diff = [f for f, h in fs.items() if not os.path.exists(os.path.join(pkg, f))
                or hashlib.sha256(open(os.path.join(pkg, f), 'rb').read()).hexdigest() != h]
        if diff: return False, f'편집 통과({d.get("by", "?")} {d.get("at", "?")}) 뒤 바뀐 파일: {", ".join(diff)}'
        return True, f'편집 통과 파일별 해시 일치({d.get("by", "?")} {d.get("at", "?")}, {len(fs)}개)'
    if not want: return False, '.edit.json에 sha 없음'
    if want != now:
        newer = [os.path.basename(f) for f in files(pkg) if os.path.getmtime(f) > os.path.getmtime(p) + 1]
        return False, f'편집 통과({d.get("by", "?")} {d.get("at", "?")}) 뒤 원고가 바뀌었다' + (f' — 바뀐 파일: {", ".join(newer)}' if newer else '')
    return True, f'편집 통과 해시 일치({d.get("by", "?")} {d.get("at", "?")})'


def refuse(pkg, why, where):
    line = f'{datetime.datetime.now():%Y-%m-%d %H:%M} · {where} 거부 · {os.path.basename(os.path.dirname(pkg.rstrip(chr(47) + chr(92))))} · {why}\n'
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    new = not os.path.exists(LOG)
    with open(LOG, 'a', encoding='utf-8') as f:
        if new: f.write('# 편집 해시 관문 거부 기록(editgate.py) — 편집 통과 뒤 바뀐 묶음은 editor가 다시 보고 stamp 해야 나간다\n\n')
        f.write(line)
    print('올리지 않는다 —', why)
    print(f'  firemap-editor가 다시 확인한 뒤: py -3.12 work/editgate.py stamp {pkg} firemap-editor "<무엇을 봤는지>"')


def stamp(pkg, by, note=''):
    p = pkg.rstrip('/\\') + '.edit.json'
    d = {}
    if os.path.exists(p):
        try: d = json.load(open(p, encoding='utf-8'))
        except Exception: d = {}
    d.update({'by': by, 'at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'sha': sha(pkg), 'sha_of': 'title.txt+c??.txt bytes'})
    if note: d['note'] = note
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    return d['sha']


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == 'check':
        ok, why = check(os.path.abspath(a[1])); print(('통과 · ' if ok else '없음 · ' if ok is None else '불일치 · ') + why)
        sys.exit(0 if ok else 1)
    if len(a) >= 3 and a[0] == 'stamp':
        print('찍음', stamp(os.path.abspath(a[1]), a[2], ' '.join(a[3:])))
        sys.exit(0)
    print(__doc__ or open(__file__, encoding='utf-8').read().split('import')[0]); sys.exit(2)
