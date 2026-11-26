"""today.md를 '지금 열린 일'만 남게 줄인다 (11/26 총무 실측: 1,210줄·445KB를 정기 작업 24개가 하루 37번 읽음 → 토큰 낭비).

AI 없이 도는 스크립트(토큰 0). 잃는 줄 없음 — 옮긴 줄은 전부 meeting/archive/today-<날짜>.md 끝에 그대로 붙는다.
  py -3.12 work/todaytrim.py [--dry]
규칙
  1) 항목 = 0칸에서 '- '로 시작하는 줄 + 그 아래 들여쓴 줄들.
  2) 끝난 항목(아래 줄에 '- 완료'·'- 취소'·'- 철회'·'- 끝', 또는 항목 줄이 '- 완료'로 시작) → archive.
  3) 머리(##) 날짜가 어제보다 옛날인 묶음: 안 끝난 [지시]·[결정 필요]·[요청]·[편집 검수 요청] 항목만
     맨 아래 '## 이월 — 안 끝난 일' 묶음으로 옮기고(머리 한 줄 출처 붙임), 나머지 줄(막힘·원칙·알림 등)은 archive.
  4) 어제·오늘 묶음은 끝난 항목만 빠지고 그대로.
  5) 끝난 줄에 '완료'라고 적는 건 각 담당 몫 — 스크립트는 판단하지 않는다.
"""
import datetime, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TODAY = os.path.join(HERE, 'research', 'meeting', 'today.md')
ARCH = os.path.join(HERE, 'research', 'meeting', 'archive')
CARRY = '## 이월 — 안 끝난 일(todaytrim이 옛 묶음에서 옮김)'
DONE = re.compile(r'^\s+- (완료|취소|철회|끝)\b|^- 완료')
OPEN = re.compile(r'^- \[(지시|결정 필요|요청|편집 검수 요청)\]|^- 결정 필요')


def sec_date(h, now):
    m = re.search(r'(\d{1,2})/(\d{1,2})', h)
    if not m: return None
    mo, d = int(m.group(1)), int(m.group(2))
    y = now.year - (1 if mo > now.month else 0)
    try: return datetime.date(y, mo, d)
    except ValueError: return None


def items(lines):
    out, cur = [], []
    for l in lines:
        if l.strip() and not l[0].isspace() and cur: out.append(cur); cur = []
        cur.append(l)
    if cur: out.append(cur)
    return out


def main():
    dry = '--dry' in sys.argv
    now = datetime.date.today()
    cut = now - datetime.timedelta(days=1)
    src = open(TODAY, encoding='utf-8').read()
    L = src.split('\n')
    head, secs, cur = [], [], None
    for l in L:
        if l.startswith('## '):
            cur = [l, []]; secs.append(cur)
        elif cur is None: head.append(l)
        else: cur[1].append(l)
    keep, moved, carry = list(head), [], []
    for h, body in secs:
        if h.startswith(CARRY):
            for it in items(body):
                (moved if any(DONE.search(x) for x in it) else carry).append(it if not it[0] == '' else it)
            continue
        d = sec_date(h, now)
        old = d is not None and d < cut
        kept_body = []
        for it in items(body):
            done = any(DONE.search(x) for x in it)
            if done:
                moved.append([f'<!-- from: {h[:80]} -->'] + it)
            elif old:
                if OPEN.search(it[0]):
                    it = list(it); it[0] = it[0] + f' 〔출처: {h[3:60]}〕'
                    carry.append(it)
                else:
                    moved.append([f'<!-- from: {h[:80]} -->'] + it)
            else:
                kept_body += it
        if old:
            moved.append([h])
        else:
            keep.append(h); keep += kept_body
    carry = [it for it in carry if any(x.strip() for x in it)]
    if carry:
        keep.append(CARRY)
        for it in carry: keep += [x for x in it if x.strip() or x == '']
    new = '\n'.join(keep).rstrip('\n') + '\n'
    mv = [x for it in moved for x in it]
    print(f'today.md {len(L)}줄 {len(src.encode())//1024}KB → {new.count(chr(10))}줄 {len(new.encode())//1024}KB · archive로 {len(mv)}줄 · 이월 {len(carry)}항목')
    if dry or not mv: return 0
    if open(TODAY, encoding='utf-8').read() != src:
        print('읽는 사이 today.md가 바뀜 — 이번엔 손대지 않음'); return 1
    os.makedirs(ARCH, exist_ok=True)
    with open(os.path.join(ARCH, f'today-{now:%Y-%m-%d}.md'), 'a', encoding='utf-8') as f:
        f.write(f'\n\n# todaytrim {datetime.datetime.now():%Y-%m-%d %H:%M}\n' + '\n'.join(mv) + '\n')
    tmp = TODAY + '.trim'
    open(tmp, 'w', encoding='utf-8').write(new)
    os.replace(tmp, TODAY)
    return 0


if __name__ == '__main__':
    sys.exit(main())
