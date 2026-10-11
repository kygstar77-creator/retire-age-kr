# -*- coding: utf-8 -*-
"""법령 조문을 번호로 뽑아 사람이 읽는 글자로 찍는다.

실행:
  py -3.12 work/lawtext.py 소득세법 129
  py -3.12 work/lawtext.py 소득세법 118-7        # 제118조의7
  py -3.12 work/lawtext.py 소득세법 129 --out lawout.txt
  py -3.12 work/lawtext.py 예금자보호법 --find 1억원   # 조문 번호를 모를 때 낱말로 찾는다

만든 이유(2026-09-24 02시 회차): 회차마다 법령 API를 손으로 긁다가 두 번 헛돌았다.
  (1) 조문 묶음 태그가 <조문단위>가 아니라 <조문단위 조문키="0129001">라서
      정규식 <조문단위>로는 하나도 안 잡힌다. 오늘 이 한 글자 때문에 '찾은 조문 0건'이 세 번 나왔다.
  (2) 조문 본문은 전부 CDATA 안에 들어 있어서 태그를 지우는 방식으로는 내용이 통째로 날아간다.
  (3) Windows PowerShell에서 py -3.12 -c "..." 로 한글을 넘기면 인자가 깨진다. 파일로 둬야 한다.
그래서 확인 못 한 세율을 글에 못 쓰고 빼는 일이 생겼다. 다음 회차부터는 이 파일을 쓴다.
"""
import re
import sys
import urllib.parse
import urllib.request

API = 'http://www.law.go.kr/DRF/lawService.do?OC=test&target=law&LM=%s&type=XML'
JO = re.compile(r'<조문단위[^>]*>(.*?)</조문단위>', re.S)
CDATA = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.S)


def _get(url):
    return urllib.request.urlopen(url, timeout=90).read().decode('utf-8', 'replace')


def latest_ef(law_name, today=None):
    """오늘 시행 중인 판 가운데 가장 늦게 공포된 판의 (MST, 공포일자)를 찾는다.

    2026-10-11 14시 회차: LM=소득세법(현행)이 공포 2025.12.23판(시행 2026.7.1)을 돌려줘
    제59조의2가 '8세 이상'으로 나왔다. 실제로는 2026.4.21 공포·시행 법률 제21548호가
    '13세 이상'+부칙(2026년 9세)으로 바꿨다. API 목록에서 그 판은 '연혁'으로 찍혀
    '현행'만 받으면 놓친다. 그래서 eflaw 목록에서 시행일 ≤ 오늘인 판 중 공포가 가장 늦은 것을 고른다.
    """
    import datetime
    today = today or datetime.date.today().strftime('%Y%m%d')
    url = ('http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=eflaw&type=XML&display=100&query=%s'
           % urllib.parse.quote(law_name))
    best = None
    for b in re.findall(r'<law [^>]*>(.*?)</law>', _get(url), re.S):
        if _tag(b, '법령명한글') != law_name:
            continue
        ef, pub, mst = _tag(b, '시행일자'), _tag(b, '공포일자'), _tag(b, '법령일련번호')
        if ef and ef <= today and (best is None or (pub, ef) > best[1:]):
            best = (mst, pub, ef)
    return best, today


def fetch(law_name):
    xml = _get(API % urllib.parse.quote(law_name))
    try:
        best, today = latest_ef(law_name)
        cur = _tag(xml[:3000], '공포일자')
        if best and best[1] > cur:
            print('[lawtext] 현행 응답은 공포 %s판 — 그 뒤 공포·시행된 %s판(MST %s)으로 읽는다'
                  % (cur, best[1], best[0]), file=sys.stderr)
            # efYd는 그 판의 시행일자와 같아야 한다(오늘 날짜를 넣으면 '일치하는 법령이 없습니다').
            new = _get('http://www.law.go.kr/DRF/lawService.do?OC=test&target=eflaw&MST=%s&efYd=%s&type=XML'
                       % (best[0], best[2]))
            if '<조문단위' in new:
                fetch.older = xml  # 현행 응답(나중 시행일 조문은 이쪽에만 있을 수 있다) — 조문이 다르면 둘 다 보인다
                xml = new
            else:
                print('[lawtext] 최신판 본문을 못 받음 — 현행 응답 그대로', file=sys.stderr)
    except Exception as e:  # 목록 조회가 막혀도 예전처럼 현행으로 읽는다
        print('[lawtext] 최신판 확인 실패(%s) — 현행 응답 그대로' % e, file=sys.stderr)
    return xml


def _tag(block, name):
    m = re.search(r'<%s>(.*?)</%s>' % (name, name), block, re.S)
    if not m:
        return ''
    inner = m.group(1)
    cd = CDATA.search(inner)
    return (cd.group(1) if cd else inner).strip()


def articles(xml):
    """조문 하나를 {'번호','가지','제목','글'} 로 돌려준다."""
    out = []
    for block in JO.findall(xml):
        num = _tag(block, '조문번호')
        gaji = _tag(block, '조문가지번호')
        title = _tag(block, '조문제목')
        # 장·절 제목도 '조문단위'로 오고 바로 뒤 조의 번호를 달고 온다(조문여부=전문).
        # 2026-09-27: '소득세법 14'가 제14조 대신 "제2절 과세표준과 세액의 계산"을 돌려줬다.
        if _tag(block, '조문여부') == '전문':
            continue
        # 조문내용 + 항내용 + 호내용 + 목내용을 순서대로 이어 붙인다(전부 CDATA).
        lines = []
        for m in re.finditer(r'<(조문내용|항내용|호내용|목내용)>(.*?)</\1>', block, re.S):
            cd = CDATA.search(m.group(2))
            t = (cd.group(1) if cd else m.group(2)).strip()
            if t:
                lines.append(t)
        out.append({'번호': num, '가지': gaji, '제목': title, '글': '\n'.join(lines)})
    return out


def pick(xml, jo, gaji=''):
    """제<jo>조(의<gaji>) 하나를 찾는다. 없으면 None."""
    for a in articles(xml):
        if a['번호'] == str(jo) and (a['가지'] or '') == (str(gaji) if gaji else ''):
            return a
    return None


def find(xml, word, span=500):
    """낱말이 들어 있는 조문을 모두 찾는다. 조문 번호를 모를 때 쓴다."""
    hits = []
    for a in articles(xml):
        if word in a['글']:
            i = a['글'].find(word)
            hits.append((a, a['글'][max(0, i - span // 2):i + span]))
    return hits


def label(a):
    n = '제%s조' % a['번호'] + ('의%s' % a['가지'] if a['가지'] else '')
    return n + ('(%s)' % a['제목'] if a['제목'] else '')


def main():
    # --find/--out 뒤의 값은 위치 인자가 아니다. 예전에는 이것까지 법령 이름으로 세어
    # 'soc 소득세법 시행령 1월 15일'처럼 붙었다.
    argv, args, skip = sys.argv[1:], [], False
    for x in argv:
        if skip:
            skip = False
            continue
        if x in ('--find', '--out'):
            skip = True
            continue
        if x.startswith('--'):
            continue
        args.append(x)
    if not args:
        raise SystemExit(__doc__)
    # 법령 이름에 띄어쓰기가 있으면(예: "소득세법 시행령") 셸이 인자를 쪼개 보낸다.
    # 예전에는 args[0]만 써서 "소득세법 시행령"을 조용히 "소득세법"으로 바꿔 엉뚱한 법을 읽었다
    # (2026-09-24 12:30 회차에서 실제로 당함). 조문 번호가 아닌 인자는 이름에 이어 붙인다.
    law = args[0]
    rest = args[1:]
    while rest and not re.fullmatch(r'\d+(-\d+)?', rest[0]):
        law += ' ' + rest.pop(0)
    args = [law] + rest
    out_path = None
    if '--out' in sys.argv:
        out_path = sys.argv[sys.argv.index('--out') + 1]
    xml = fetch(law)

    if '--find' in sys.argv:
        word = sys.argv[sys.argv.index('--find') + 1]
        hits = find(xml, word)
        body = '\n\n'.join('[%s]\n%s' % (label(a), seg) for a, seg in hits[:8])
        head = '%s 에서 "%s" 가 든 조문 %d건' % (law, word, len(hits))
    else:
        if len(args) < 2:
            raise SystemExit('조문 번호를 적어라 — 예: py -3.12 work/lawtext.py 소득세법 129')
        jo, gaji = (args[1].split('-') + [''])[:2]
        a = pick(xml, jo, gaji)
        if not a:
            raise SystemExit('%s 에 제%s조%s 가 없다' % (law, jo, ('의' + gaji) if gaji else ''))
        body = a['글']
        old = getattr(fetch, 'older', None)
        b = pick(old, jo, gaji) if old else None
        if b and b['글'] != body:
            body += ('\n\n[참고: 현행 응답(공포 %s판)의 같은 조문 — 위와 다르다. 시행일이 다른 조항은 둘 다 확인]\n%s'
                     % (_tag(old[:3000], '공포일자'), b['글']))
        head = '%s %s' % (law, label(a))

    text = head + '\n\n' + body
    if out_path:
        open(out_path, 'w', encoding='utf-8').write(text)
        print(head)
        print('→ ' + out_path)
    else:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        print(text)


if __name__ == '__main__':
    # 2026-09-27 17시 회차: '조문이 없다' 메시지(SystemExit)는 stderr로 나가는데 Windows 기본 cp949라
    # Git Bash에서 '�ҵ漼���'로 깨져 무슨 말인지 못 읽었다. 둘 다 utf-8로 맞춘다.
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass
    main()
