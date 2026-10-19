# 편집 통과 해시 관문(2026-10-02, 대역 지시 10/1 21:35) — 편집자가 통과시킨 원고와 실제로 나가는 원고가 같은지 본다.
# 10/2 카페 190: 06:40 통과본과 08:28 공개본 해시가 달랐다(editor 10:50 확인). 통과 뒤에 제목·조각을 바꾸면 통과가 아니다.
# 해시 = title.txt + c??.txt(이름순) 파일 바이트를 그대로 이어 붙인 sha256 — editor가 10/2 07:43부터 쓰는 방식(e1table1002·b10cafe1002 재현).
#   py -3.12 work/editgate.py check <pkg>                지금 원고가 .edit.json과 같은지
#   py -3.12 work/editgate.py stamp <pkg> <by> [note]    편집 통과 표시(.edit.json)를 이 방식으로 찍는다(카페는 틀 v2·compare.md 먼저)
#   py -3.12 work/editgate.py compare <pkg>              카페 경쟁 비교 관문만
#   py -3.12 work/editgate.py sise <pkg>                 출처 줄이 네이버·다음 증권 단독인지만
#   py -3.12 work/editgate.py cover <pkg>                카페 표지 관문만(10/17 10:00 이후 묶음: cafecover.py·cover_review 두 줄)
#   py -3.12 work/editgate.py calc <pkg>                 카페 끝 계산기 줄(제목 주제 → 계산기 대응표 CALC)만
#   카페 stamp는 review.md/compare.md의 '전제: 가능 — <facts 근거>' 줄도 본다(10/12 레드팀 R2)
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


COVER2_FROM = datetime.datetime(2026, 10, 17, 10, 0)


def cover_check(pkg):
    """카페 표지 관문(visual 10/17, 벤치마크 cafe-gap-1016 ①~③). 문제 목록, 비면 통과.
    10/17 10:00 이후 만든 묶음(order.txt 시각 — understand_block과 같은 방식)만 본다. 그 전 묶음은 그대로 나간다.
    ① 표지는 work/cafecover.py로 만든다(cover_meta.json: 주제 사물 그림 1개·주제어 줄 > 숫자 줄)
    ② cover_review.md에 '100px 읽힘: …'·'최근 10장 옆 구별: …' 두 줄(10/13~15 묶음 26개 중 0)."""
    pkg = os.path.abspath(pkg.rstrip(chr(47) + chr(92)))
    order = os.path.join(pkg, 'order.txt')
    if not os.path.exists(order) or datetime.datetime.fromtimestamp(os.path.getmtime(order)) < COVER2_FROM:
        return []
    bad = []
    mp = os.path.join(pkg, 'cover_meta.json')
    if not os.path.exists(mp):
        bad.append('cover_meta.json 없음 — 표지를 py -3.12 work/cafecover.py <pkg> --topic … --num … 로 만든다(주제 사물 그림·주제어 가장 크게). 경쟁 표지가 캡처·차트면 {"type": "capture"|"chart", "source": …}(D-04)')
    else:
        try:
            m = json.load(open(mp, encoding='utf-8'))
            # D-04(기준 리뉴얼 10/19, registry): 첫 사진 종류는 경쟁 글 표지 종류를 따른다 — 상위 24장: 차트·표·지도 6·화면 캡처 5·직접 찍은 사진 4·글자 카드 3·기타 6.
            #   캡처·차트면 cover_meta.json {"type": "capture"|"chart", "source": 원본 출처} + bench.md '따라 한 것'의 '표지' 줄에 같은 종류(캡처·화면 / 차트·표·그래프·지도)가 있어야 한다.
            #   카드(기본, type 없음)는 지금처럼 cafecover.py(주제 사물 그림·주제어 줄 > 숫자 줄).
            ty = m.get('type', 'card')
            if ty in ('capture', 'chart'):
                if not str(m.get('source', '')).strip(): bad.append(f'표지 {ty} — cover_meta.json source(원본 출처) 없음')
                bp = os.path.join(os.path.dirname(pkg), 'bench.md')
                bt = open(bp, encoding='utf-8', errors='ignore').read() if os.path.exists(bp) else ''
                row = [l for l in bt.splitlines() if l.strip().startswith('|') and '표지' in l.split('|')[1]] if bt else []
                kw = r'캡처|화면' if ty == 'capture' else r'차트|표|그래프|지도'
                if not any(re.search(kw, l) for l in row): bad.append(f"표지 종류 {ty}인데 bench.md '표지' 줄에 경쟁 글 표지 종류({kw.replace('|', '·')})가 없다 — 경쟁 표지 종류를 따른다")
                raise StopIteration
            if not m.get('icon'): bad.append('표지에 주제 사물 그림 없음(cover_meta.json icon)')
            if m.get('num_px') and not m.get('topic_px', 0) > m['num_px']: bad.append(f"표지 주제어 줄 {m.get('topic_px')}px ≤ 숫자 줄 {m['num_px']}px")
            first = next((l.strip() for l in open(order, encoding='utf-8') if l.strip().startswith('img/')), '')
            img = os.path.join(pkg, first) if first else ''
            if img and os.path.exists(img) and os.path.getmtime(img) > os.path.getmtime(mp) + 5:
                bad.append(f'첫 사진 {first}이 cafecover.py 뒤에 바뀜 — cafecover.py로 다시 만든다')
        except StopIteration:
            pass
        except Exception as e:
            bad.append(f'cover_meta.json 못 읽음: {e}')
    cr = os.path.join(pkg, 'cover_review.md')
    t = open(cr, encoding='utf-8', errors='ignore').read() if os.path.exists(cr) else ''
    for key in ('100px 읽힘', '최근 10장 옆 구별'):
        v = re.findall(r'^\W*' + key + r'\W*[:：]\s*(.+)$', t, re.M)
        if not v or not v[-1].strip():
            bad.append(f"cover_review.md에 '{key}: …' 줄 없음(cover_100.png·cover_board.png를 보고 적는다)")
        elif re.search(r'안 ?읽|구별 ?안|안 ?됨|확인 ?안|못 ?읽|미달', v[-1]):
            bad.append(f"cover_review.md '{key}' 미달: {v[-1].strip()[:40]}")
    return bad


def compare_check(pkg):
    """카페 묶음 경쟁 비교 관문(10/10 회의 21:41: facts의 toprank 한 줄로는 인정 안 함). 문제 목록, 비면 통과.
    compare.md(pkg 또는 그 위 폴더)에 경쟁 상위 3편 이상(표 줄 '| 순위 |' 또는 주소)과 3줄(잘하는 것·따라갈 것·다르게 할 것)."""
    pkg = os.path.abspath(pkg.rstrip('/\\'))
    f = next((os.path.join(d, 'compare.md') for d in (pkg, os.path.dirname(pkg)) if os.path.exists(os.path.join(d, 'compare.md'))), None)
    if not f: return ['compare.md 없음(경쟁 상위 3편과 우리 차이 3줄)']
    t = open(f, encoding='utf-8', errors='ignore').read()
    rows = len(re.findall(r'(?m)^\|\s*\d+\s*\|', t)) or len(set(re.findall(r'https?://\S+', t)))
    bad = [] if rows >= 3 else [f'compare.md 경쟁 글 {rows}편(3편 이상)']
    bad += [f"compare.md에 '{k}' 줄 없음" for k in ('잘하는 것', '따라갈 것', '다르게 할 것') if k not in t]
    return bad


def premise_check(pkg):
    """카페 전제 관문(10/12 레드팀 R2 — C-1 짝 글이 '3억 배당 월 200만원'처럼 불가능한 전제로 관문을 넘었다).
    review.md 또는 compare.md(pkg 또는 그 위 폴더)에 '전제: 가능 — <facts 근거>' 줄. 없거나 '불가능'이면 문제 목록."""
    pkg = os.path.abspath(pkg.rstrip('/\\'))
    lines = []
    for d in (pkg, os.path.dirname(pkg)):
        for n in ('review.md', 'compare.md'):
            p = os.path.join(d, n)
            if os.path.exists(p):
                lines += [ln.strip() for ln in open(p, encoding='utf-8', errors='ignore') if re.match(r'\s*[-*]?\s*\**전제\**\s*[:：]', ln)]
    if not lines: return ["review.md/compare.md에 '전제: 가능 — <facts 근거>' 줄 없음"]
    last = lines[-1]
    if re.search(r'불가능', last): return [f'전제 불가능으로 적힘 — {last[:80]}']
    if not re.search(r'가능', last): return [f"전제 줄에 가능/불가능 판정이 없다 — {last[:80]}"]
    if len(re.sub(r'.*?가능', '', last, count=1).strip(' —-:·')) < 8: return [f'전제 줄에 근거(facts)가 없다 — {last[:80]}']
    return []


# 10/14 감사(경미): 상품·종목 비교 카페 글의 '권유 아님' 줄이 들쭉날쭉(qqqm1014·r1cafe1014·r1cafe_fx1014 없음) — 상품·종목 이름이 있으면 필수.
# 10/19 감사(경미): coin1019(#321)가 '권유 아님' 줄 없이 통과 — 가상자산 말도 상품으로 본다('코인'은 코인노래방 등과 섞여 투자·시세·거래가 붙을 때만).
PRODUCT = re.compile(r'ETF|리츠|펀드|커버드콜|주가|종목|배당주|상장|비트코인|이더리움|가상자산|암호화폐|코인\s?(투자|시세|거래|가격)')  # 티커(대문자)는 기관 약어(API·KOSIS)와 섞여 오탐 — 티커 글은 이 말들이 같이 나온다

# 10/15 감사(경미): 10/14 회의 지시 '카페 끝 관련 계산기 한 줄'이 공개 10편 중 2편만 — 제목이 아래 주제면 그 계산기 줄(utm_source=cafe) 필수.
# 대응표 = src/firemap-v2/toolPages.js에 등록된 공개 계산기만(/calc/loan은 dev 전용이라 뺌). 제목으로만 본다(본문 지나가는 말은 주제가 아님).
CALC = [
    (r'실업급여|구직급여', 'calc/unemployment-benefit'),
    # 10/16 회의 지시: '퇴직소득세' 제목이 세전 퇴직금 계산기로 가면 글 질문과 다른 도구 — 퇴직소득세 계산기는 src에 없어 줄을 요구하지 않는다.
    # 예금·이자(정기예금·적금·저축은행) 계산기도 toolPages.js에 없음(10/17 확인) → 대응표 줄 없음.
    # 10/18: '퇴직금 넣어도/굴리기/어디에'처럼 퇴직금을 어디 둘지 묻는 글(cma1017)은 금액 계산 질문이 아니다(교훈 37·39).
    (r'^(?!.*퇴직소득세)(?!.*퇴직금\s?(을|를)?\s?(넣|굴|맡|투자|어디|운용)).*퇴직금', 'calc/severance'),
    (r'실수령|연봉 ?계산|4대 ?보험', 'calc/salary'),
    (r'건강보험료|건보료|피부양자', 'health-insurance'),
    (r'해외주식 ?양도세|배당소득세|금융소득 ?종합과세', 'tax'),
    (r'국민연금.*(조기|수령 ?나이|당기|미루|연기)|조기수령|연기연금', 'pension'),
    (r'월 ?배당|배당으로 ?(생활|월)|은행주|배당주|배당 ?수익률|배당률', 'dividend'),
]


def calc_check(pkg):
    """제목이 CALC 주제면 본문에 firemap.kr/<그 계산기>?…utm_source=cafe 줄 필수. 문제 목록, 비면 통과."""
    tp = os.path.join(pkg, 'title.txt')
    title = open(tp, encoding='utf-8', errors='ignore').read() if os.path.exists(tp) else ''
    body = '\n'.join(open(f, encoding='utf-8', errors='ignore').read() for f in files(pkg)[1:])
    for pat, path in CALC:
        # 10/17 report 요청: #296(retax1016)은 'firemap.kr/…'로 시작해 https:// 가 없어 편집기가 링크로 안 바꿨다(contentHtml <a href> 0) → https:// 필수
        if re.search(pat, title) and not re.search(r'https://firemap\.kr/' + re.escape(path) + r'\?[^\s]*utm_source=cafe', body):
            return [f"제목이 '{re.search(pat, title).group(0)}' 주제인데 끝에 눌리는 계산기 줄 없음(https:// 빠지면 링크가 안 됨) — 예: https://firemap.kr/{path}?utm_source=cafe&utm_medium=post&utm_campaign=<묶음>"]
    # 10/18 회의 지시 ⓑ: 반대 방향 — 본문에 걸린 계산기가 제목 주제와 안 맞으면 막는다(cma1017 CMA 글 → 퇴직금 계산기).
    bad = []
    for path in sorted(set(re.findall(r'https?://firemap\.kr/([a-z0-9\-/]+)', body))):
        pats = [pt for pt, ph in CALC if ph == path.rstrip('/')]
        if pats and not any(re.search(pt, title) for pt in pats):
            bad.append(f"본문 계산기 firemap.kr/{path}가 제목 주제와 안 맞음 — 맞는 계산기가 없으면 줄을 뺀다")
    return bad


# 10/15 회의 지시·audit/sise-terms-1015.md: 출처 줄에 네이버·다음 증권만 적힌 시세는 거부 — 원 데이터 주인(KRX·DART·운용사·SEC 등)이 함께 있어야 한다.
SISE_PORTAL = r'네이버 ?(페이 ?)?증권|네이버 ?금융|다음 ?금융|finance\.naver|finance\.daum|m\.stock\.naver'
SISE_OWNER = r'한국거래소|KRX|DART|전자공시|금융위원회|공공데이터|운용|SEC|EDGAR|나스닥|Nasdaq|NYSE|야후|Yahoo|한국은행|ECOS|FRED|IR'


def sise_source_check(pkg):
    """출처 줄(출처·자료가 들어간 줄)에 포털 증권만 있고 원 데이터 주인이 없으면 문제. 비면 통과."""
    bad = []
    for f in files(pkg):
        for ln in open(f, encoding='utf-8', errors='ignore').read().splitlines():
            if re.search(r'출처|자료[:：]|기준[:：]', ln) and re.search(SISE_PORTAL, ln) and not re.search(SISE_OWNER, ln):
                bad.append(f"{os.path.basename(f)}: 출처가 포털 증권뿐 — '{ln.strip()[:60]}' → 한국거래소 정규장 종가(날짜) 등 원 데이터 주인으로")
    return bad



def disclaim_check(pkg):
    """상품·종목이 나오는 글이면 '권유 아님' 줄(work/disclaim.py 꼴) 필수. 문제 목록, 비면 통과."""
    sys.path.insert(0, HERE)
    import disclaim
    t = '\n'.join(open(f, encoding='utf-8', errors='ignore').read() for f in files(pkg))
    t = re.sub(r'https?://\S+', '', t)
    m = PRODUCT.search(t)
    if not m or disclaim.line(t): return []
    return [f"상품·종목('{m.group(0)}')이 나오는데 '권유 아님' 줄 없음 — 예: '특정 상품을 사거나 팔라는 뜻이 아닙니다.'"]


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
    if len(a) >= 2 and a[0] == 'compare':
        cb = compare_check(a[1]); print('통과 · compare.md' if not cb else '미달 · ' + '; '.join(cb)); sys.exit(1 if cb else 0)
    if len(a) >= 2 and a[0] == 'calc':
        cc = calc_check(os.path.abspath(a[1])); print('통과 · 계산기 줄' if not cc else '미달 · ' + '; '.join(cc)); sys.exit(1 if cc else 0)
    if len(a) >= 2 and a[0] == 'sise':
        sb = sise_source_check(os.path.abspath(a[1])); print('통과 · 시세 출처' if not sb else '미달 · ' + '; '.join(sb)); sys.exit(1 if sb else 0)
    if len(a) >= 2 and a[0] == 'cover':
        vb = cover_check(os.path.abspath(a[1])); print('통과 · 표지' if not vb else '미달 · ' + '; '.join(vb)); sys.exit(1 if vb else 0)
    if len(a) >= 2 and a[0] == 'disclaim':
        db = disclaim_check(os.path.abspath(a[1])); print('통과 · 권유 아님 줄' if not db else '미달 · ' + '; '.join(db)); sys.exit(1 if db else 0)
    if len(a) >= 3 and a[0] == 'stamp':
        # 10/3 editor: auto로 찍힌 카페 묶음 3편(offimkt·schd·deadfin)이 틀 v2에 걸려 발행 당일 gate_pkg에 막힐 뻔했다 — 찍기 전에 틀부터 본다.
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import aitell
        pk = os.path.abspath(a[1])
        # 10/10·10/13 editor: pkg 대신 상위 폴더에 찍어 빈 해시(e3b0c4…) 파일이 두 번 생겼다 — 글 파일 없는 폴더는 거부.
        if not os.path.exists(os.path.join(pk, 'title.txt')) and not any(re.fullmatch(r'c\d\d\.txt', f) for f in os.listdir(pk)):
            print('안 찍음 · title.txt·c??.txt가 없는 폴더 — 묶음(pkg) 폴더를 주세요: ' + pk); sys.exit(1)
        if aitell.is_cafe_pkg(pk):
            fb = aitell.frame_check(pk)
            if fb: print('안 찍음 · 카페 틀 v2 어김 — ' + '; '.join(fb)); sys.exit(1)
            cb = compare_check(pk)
            if cb: print('안 찍음 · 경쟁 비교 없음 — ' + '; '.join(cb)); sys.exit(1)
            pb = premise_check(pk)
            if pb: print('안 찍음 · 전제 관문 — ' + '; '.join(pb)); sys.exit(1)
            db = disclaim_check(pk)
            if db: print('안 찍음 · ' + '; '.join(db)); sys.exit(1)
            cc = calc_check(pk)
            if cc: print('안 찍음 · ' + '; '.join(cc)); sys.exit(1)
            sb = sise_source_check(pk)
            if sb: print('안 찍음 · ' + '; '.join(sb)); sys.exit(1)
            vb = cover_check(pk)
            if vb: print('안 찍음 · 표지 관문 — ' + '; '.join(vb)); sys.exit(1)
        print('찍음', stamp(os.path.abspath(a[1]), a[2], ' '.join(a[3:])))
        sys.exit(0)
    print(__doc__ or open(__file__, encoding='utf-8').read().split('import')[0]); sys.exit(2)
