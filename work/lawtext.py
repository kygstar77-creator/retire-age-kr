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


def fetch(law_name):
    url = API % urllib.parse.quote(law_name)
    return urllib.request.urlopen(url, timeout=90).read().decode('utf-8', 'replace')


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
    args = [x for x in sys.argv[1:] if not x.startswith('--')]
    if not args:
        raise SystemExit(__doc__)
    law = args[0]
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
    main()
