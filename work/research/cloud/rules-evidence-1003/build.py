"""rules-evidence-1003 표 만들기 — 일회성.

1) extract.py로 규칙 후보 줄을 뽑는다.
2) classify.auto()로 1차 판정(붙은 근거 표시만 본다).
3) verdicts_manual.tsv(손 판정)로 덮어쓴다. 열: 위치 \t 판정 \t 근거 \t 재측정 \t 확인하는 법  ('제외'면 규칙 아님)
4) code_rules.tsv(코드 숫자·slots.json, 손으로 적음)를 더한다. 열: 위치 \t 규칙 요약 \t 판정 \t 근거 \t 재측정 \t 확인하는 법
5) table.tsv 와 counts.txt 를 쓴다(보고서 본문은 사람이 쓴다).
사용: python build.py [--dump-auto]
"""
import os, sys, re, collections, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract, classify

R = extract.R
VERDICTS = ('실측', '출처', '사장님 결정', '약함', '근거 없음')


def ahead(rel, line):
    try:
        ls = open(os.path.join(R, rel), encoding='utf-8').read().splitlines()
    except OSError:
        return ''
    return '\n'.join(ls[line:line + 3])


def howto(text):
    t = text
    if re.search(r'공식|정책|약관|법|규정', t):
        return '공식 문서·법령 원문 URL을 찾아 붙인다(저장소 naver-policy.md·longform/yt-policy*.md에 이미 있는지 먼저 본다).'
    if re.search(r'\d+\s?(편|건)|상한|하루\s?\d|간격', t):
        return '편수·간격별 글당 조회·검색 노출을 나눠 비교한다(데이터 일부 있음: slots.json·naverpost 발행 기록·caferank.py 조회).'
    if re.search(r'\d+(\.\d+)?\s?점|점수|평균', t):
        return '심사 점수와 공개 뒤 성과(CTR·조회)를 편별로 대조한다(점수는 review.md에 있음, 성과 표본은 아직 적음).'
    if re.search(r'\d+\s?(시간|분|h)\b|시한|기한', t):
        return 'today.md git 역사에서 요청→착수→완료 시각을 재서 실제 걸린 시간 분포와 비교한다(데이터 있음).'
    if re.search(r'\d+\s?(자|문장|개|장|%)', t):
        return '우리 글·영상을 이 수치로 나눠 조회·시청 지속을 비교하거나 상위 노출 글의 같은 수치를 실측한다(묶음 폴더는 있음, 성과 연결은 일부).'
    return '이 규칙이 막으려는 사고(또는 늘리려는 지표)를 정하고, 규칙이 생기기 전후 그 건수를 lessons.md·audit 기록으로 센다(데이터 있음).'


def load_tsv(name, ncol):
    p = os.path.join(HERE, name)
    out = []
    if not os.path.exists(p):
        return out
    for ln in open(p, encoding='utf-8'):
        if not ln.strip() or ln.startswith('#'):
            continue
        c = ln.rstrip('\n').split('\t')
        c += [''] * (ncol - len(c))
        out.append(c[:ncol])
    return out


def main():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        extract.main()
    rows = []
    for ln in buf.getvalue().splitlines():
        loc, text = ln.split('\t', 1)
        rel, line = loc.rsplit(':', 1)
        v, ev = classify.auto(text, ahead(rel, int(line)))
        rows.append({'loc': loc, 'text': text, 'v': v, 'ev': ev, 're': '', 'how': '', 'src': 'auto'})
    if '--dump-auto' in sys.argv:
        for r in rows:
            print(f"{r['loc']}\t{r['v']}\t{r['ev']}\t{r['text'][:160]}")
        return
    man = {c[0]: c for c in load_tsv('verdicts_manual.tsv', 5)}
    keep = []
    for r in rows:
        m = man.pop(r['loc'], None)
        if m:
            if m[1] == '제외':
                continue
            r.update(v=m[1], ev=m[2] or r['ev'], re=m[3], how=m[4], src='손')
        keep.append(r)
    if man:
        print('손 판정 중 후보에 없는 위치:', ', '.join(man), file=sys.stderr)
    for c in load_tsv('code_rules.tsv', 6):
        keep.append({'loc': c[0], 'text': c[1], 'v': c[2], 'ev': c[3], 're': c[4], 'how': c[5], 'src': '손'})
    bad = [r['loc'] for r in keep if r['v'] not in VERDICTS]
    assert not bad, f'판정 이름 틀림: {bad[:5]}'
    for r in keep:
        if r['v'] in ('근거 없음', '약함') and not r['how']:
            r['how'] = howto(r['text'])
        if not r['re']:
            r['re'] = '재측정 안 함' if r['v'] == '실측' else '—'
    with open(os.path.join(HERE, 'table.tsv'), 'w', encoding='utf-8') as f:
        for r in keep:
            summ = re.sub(r'\s+', ' ', r['text']).replace('|', '/')[:140]
            f.write('\t'.join([r['loc'], summ, r['v'], r['ev'].replace('|', '/'), r['re'].replace('|', '/'),
                               r['how'].replace('|', '/'), r['src']]) + '\n')
    tot = collections.Counter(r['v'] for r in keep)
    per = collections.defaultdict(collections.Counter)
    for r in keep:
        f = r['loc'].rsplit(':', 1)[0]
        f = 'playbooks/*.md' if f.startswith('playbooks/') else f
        per[f][r['v']] += 1
    srcc = collections.Counter(r['src'] for r in keep)
    nore = sum(1 for r in keep if r['v'] == '실측' and r['re'].startswith('재측정 안 함'))
    with open(os.path.join(HERE, 'counts.txt'), 'w', encoding='utf-8') as f:
        f.write(f'전체 {len(keep)} · 손 판정 {srcc["손"]} · 자동 {srcc["auto"]} · 실측 중 재측정 안 함 {nore}\n')
        f.write('전체\t' + '\t'.join(f'{v} {tot[v]}' for v in VERDICTS) + '\n')
        for k in sorted(per, key=lambda x: -sum(per[x].values())):
            f.write(f'{k}\t' + '\t'.join(f'{v} {per[k][v]}' for v in VERDICTS) + f'\t합 {sum(per[k].values())}\n')
    print(open(os.path.join(HERE, 'counts.txt'), encoding='utf-8').read())


if __name__ == '__main__':
    main()
