# 본문 자가발전 — 조회수 높은(상위 노출) 남의 글이 어떻게 생겼는지 재서 우리 글과 견준다.
#   py -3.12 work/bodystudy.py                  → 기본 검색어 한 바퀴
#   py -3.12 work/bodystudy.py "재산세 계산기" "SCHD 배당"
#
# 사장님 2026-09-24: "내용도 글도 잘 쓰고 이해가 잘 되도록 하고 있어?
#                    니 판단이 아니라 조회수 높은 비슷한 주제 글들 보면서?"
#
# 그때까지 남의 것을 보고 배우는 자는 제목(titlestudy)뿐이었다. 본문 길이·문단·이미지 수는
# 내가 정한 "1,900~2,400자"를 쓰고 있었고 그 숫자의 근거는 내 판단이었다.
# 첫 실측(2026-09-24 "재산세 계산기"): 상위 8편 글자 중앙 3,374자인데 우리는 2,120자였다. 1,254자 짧다.
#
# titlestudy(남의 제목) · textloop(우리 성과) 와 같은 자리에 둔다. 셋이 각각 다른 것을 본다.
import sys, os, re, json, time, statistics, glob, collections as _c
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
sys.path.insert(0, HERE)
import toprank
STATS = os.path.join(HERE, 'bodystats.json')
OUT_MD = os.path.join(R, 'bodyrule.md')

# 우리 네 축을 덮는 검색어. 우리가 실제로 쓰는 주제여야 비교가 뜻이 있다.
SEEDS = ['재산세 계산기', 'DSR 계산기', '국민연금 예상수령액', '연금저축 세액공제',
         'SCHD 배당', 'JEPI 배당', '미국 배당주 추천', '나스닥 지수',
         '서울 아파트 전세가율', '오피스텔 월세 수익률', '아파트 실거래가 조회', '청약 가점']

def measure(p):
    """글 하나. 생김새(숫자)와 **무엇을 다뤘는지**(항목)를 같이 본다.
    사장님 2026-09-24: "숫자만 보는 게 아니라 내용도 잘 쓰고 있는지 봐야지."
    글자 수·사진 수만 맞추면 껍데기만 닮는다. 상위 글이 공통으로 다루는 항목을 우리가 빠뜨렸는지가 내용이다."""
    paras = p.get('paras') or []
    lens = [len(x) for x in paras if x]
    if not lens: return None
    heads = [x for x in paras if 4 <= len(x) <= 34 and not x.rstrip().endswith(('.', '다', '요', '?', '!'))]
    body = ' '.join(paras)
    try:
        t = toprank.terms(body)
        top_terms = [w for w, c in t.most_common(40) if c >= 2][:25]
    except Exception:
        top_terms = []
    return {'chars': p.get('chars') or sum(lens), 'imgs': p.get('imgs') or 0,
            'paras': len(paras), 'para_med': int(statistics.median(lens)),
            'heads': len(heads), 'first': lens[0], 'terms': top_terms}

def ours(n=12):
    """우리 최근 발행 글의 같은 자. 묶음(pkg)에서 센다."""
    rows = []
    for pk in glob.glob(os.path.join(R, '*', 'pkg')):
        pub = os.path.join(pk, 'published.txt')
        if not os.path.exists(pub): continue
        texts = []
        for f in sorted(glob.glob(os.path.join(pk, 'b*.txt'))):
            try: texts.append(open(f, encoding='utf-8').read().strip())
            except Exception: pass
        if not texts: continue
        paras = [x.strip() for t in texts for x in t.splitlines() if x.strip()]
        lens = [len(re.sub(r'\s+', '', x)) for x in paras if x]
        if not lens: continue
        heads = [x for x in paras if 4 <= len(x) <= 34 and not x.rstrip().endswith(('.', '다', '요', '?', '!'))]
        try: ours_terms = [w for w, c in toprank.terms(' '.join(paras)).most_common(40) if c >= 2][:25]
        except Exception: ours_terms = []
        try: title = open(os.path.join(pk, 'title.txt'), encoding='utf-8').read().strip()
        except Exception: title = ''
        rows.append({'at': os.path.getmtime(pub), 'title': title, 'kw': os.path.basename(os.path.dirname(pk)),
                     'chars': sum(lens), 'imgs': len(glob.glob(os.path.join(pk, 'img', '*'))),
                     'paras': len(paras), 'para_med': int(statistics.median(lens)),
                     'heads': len(heads), 'first': lens[0], 'terms': ours_terms})
    rows.sort(key=lambda r: -r['at'])
    return rows[:n]

def med(rows, k):
    v = [r[k] for r in rows if r.get(k) is not None]
    return statistics.median(v) if v else None

def main():
    kws = sys.argv[1:] or SEEDS
    seen = json.load(open(STATS, encoding='utf-8')) if os.path.exists(STATS) else {'posts': []}
    known = {(p['id'], p['no']) for p in seen['posts']}
    got = 0
    for kw in kws:
        try: hits, _ = toprank.search(kw, 8)
        except Exception as e:
            print('검색 실패', kw, repr(e)[:60]); continue
        for bid, no in hits:
            if (bid, no) in known: continue
            try: p = toprank.post(bid, no)
            except Exception: p = None
            if not p: continue
            m = measure(p)
            if not m: continue
            m.update({'id': bid, 'no': no, 'kw': kw, 'title': p.get('title', '')[:70],
                      'at': time.strftime('%Y-%m-%d')})
            seen['posts'].append(m); known.add((bid, no)); got += 1
            time.sleep(0.4)
        time.sleep(0.3)
    seen['posts'] = seen['posts'][-600:]
    json.dump(seen, open(STATS, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

    them, us = seen['posts'], ours()
    if len(them) < 8 or len(us) < 4:
        print(f'표본 부족 — 남의 글 {len(them)}편·우리 글 {len(us)}편'); return

    KEYS = [('chars', '본문 글자 수', '자'), ('imgs', '사진 수', '장'), ('paras', '문단 수', '개'),
            ('para_med', '문단 길이 중앙', '자'), ('heads', '소제목 수', '개'), ('first', '첫 문단 길이', '자')]
    lines = ['# 본문 규칙 (bodystudy 자동 생성 — 사람이 고치지 않는다)', '',
             f'측정 {time.strftime("%Y-%m-%d %H:%M")} · 상위 노출 글 {len(them)}편 · 우리 최근 {len(us)}편', '',
             '조회수 높은 글이 실제로 어떻게 생겼는지 잰 값이다. 내 판단이 아니다.',
             '회차는 묶음을 만들기 전에 이 표를 보고 조각 수와 길이를 정한다.', '',
             '| 항목 | 상위 글 | 우리 | 차이 |', '|---|---|---|---|']
    todo = []
    for k, ko, unit in KEYS:
        a, b = med(them, k), med(us, k)
        if a is None or b is None: continue
        d = b - a
        mark = '같음' if abs(d) <= max(1, a * 0.12) else (f'우리가 {abs(d):.0f}{unit} ' + ('많다' if d > 0 else '적다'))
        lines.append(f'| {ko} | {a:.0f}{unit} | {b:.0f}{unit} | {mark} |')
        if abs(d) > max(1, a * 0.12): todo.append((abs(d) / max(a, 1), ko, a, b, unit, d))
    todo.sort(reverse=True)
    lines += ['', '## 이번에 맞출 것 (차이 큰 순)', '']
    if todo:
        for _, ko, a, b, unit, d in todo[:3]:
            lines.append(f'- **{ko}를 {a:.0f}{unit} 쪽으로** — 지금 우리는 {b:.0f}{unit}다'
                         + (' (줄인다)' if d > 0 else ' (늘린다)'))
    else:
        lines.append('- 모든 항목이 상위 글과 12% 안쪽이다. 맞출 것 없음')
    # ── 내용: 우리 글 하나하나를 **같은 주제** 상위 글과 맞댄다.
    # 주제가 다른 글끼리 견주면 "SCHD가 빠졌다" 같은 말이 나온다 — 그 글은 재산세 글인데.
    # 그래서 우리 글 제목으로 직접 검색해 그 주제의 상위 글을 가져와 항목을 견준다.
    lines += ['', '## 내용 — 같은 주제 상위 글이 다루는데 우리가 빠뜨린 항목', '',
              '글자 수를 맞춰도 다루는 항목이 다르면 독자가 찾던 답이 없는 글이 된다.',
              '말을 베끼지 않는다. 다루는 **항목**이 빠졌는지만 본다.', '']
    checked = 0
    for r in us[:5]:
        t = r.get('title') or ''
        q = ' '.join(re.sub(r'[^\w가-힣 ]', ' ', t).split()[:3])
        if len(q) < 4: continue
        try: hits, _ = toprank.search(q, 6)
        except Exception: continue
        rivals = []
        for bid, no in hits:
            if bid == 'kygstar7777': continue
            try: rp = toprank.post(bid, no)
            except Exception: rp = None
            if not rp: continue
            mm = measure(rp)
            if mm: rivals.append(mm)
            time.sleep(0.35)
        if len(rivals) < 3: continue
        cnt = _c.Counter()
        for x in rivals:
            for w in set(x.get('terms') or []): cnt[w] += 1
        need2 = max(2, int(len(rivals) * 0.5))
        miss = [w for w, c in cnt.most_common(80) if c >= need2 and w not in set(r.get('terms') or [])][:10]
        checked += 1
        lines.append(f"**{t[:52]}**")
        lines.append(f"- 같은 주제 상위 {len(rivals)}편 · 글자 {statistics.median([x['chars'] for x in rivals]):.0f}자 (우리 {r['chars']}자)")
        lines.append('- 빠진 항목: ' + (' · '.join(miss) if miss else '없음'))
        lines.append('')
    if not checked:
        lines.append('- 비교할 표본을 못 모았다(검색 실패 또는 상위 글 3편 미만).')

    lines += ['', '## 표본', '']
    for p in them[-6:]:
        lines.append(f"- {p['chars']:,}자 · 사진 {p['imgs']}장 · 소제목 {p['heads']}개 · {p['title'][:44]}")
    os.makedirs(R, exist_ok=True); open(OUT_MD, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    print(f'[본문 루프 {time.strftime("%H:%M")}] 새로 읽은 글 {got}편 · 표본 {len(them)}편')
    for l in lines[6:14]: print(' ', l)
    print(' 규칙표:', OUT_MD)

if __name__ == '__main__': main()
