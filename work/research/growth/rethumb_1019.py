# 10/19 조회 적은 공개 롱폼 썸네일 교체 — 효과 재기(바꾸기 전 기준 · 7일 뒤 다시).
#   py -3.12 work/research/growth/rethumb_1019.py before   # 기준: 지금 조회(Data API) + 노출·클릭률(Reporting CSV) → rethumb-1019.csv 'before' 줄
#   py -3.12 work/research/growth/rethumb_1019.py after    # 10/26: ytreach.py로 새 보고서 받은 뒤 같은 영상 다시 → 'after' 줄 + 전/후 표 출력
# 노출·클릭률: research/longform/loop/reach/<날짜>.csv(channel_reach_basic_a1, 이틀 늦음). before = 교체 전 7일(10/10~10/16), after = 교체 다음 날부터 받은 날까지.
# 대상·교체 여부는 rethumb-1019.csv 'before' 줄(changed 칸)에서 읽는다. 교체 안 한 편은 대조군.
import sys, os, csv, glob, datetime, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(H, '..', '..'))
sys.path.insert(0, WORK)
CSV = os.path.join(H, 'rethumb-1019.csv')
REACH = os.path.join(WORK, 'research', 'longform', 'loop', 'reach')
COLS = ['measured_at', 'phase', 'video_id', 'ep', 'changed', 'thumb_before', 'thumb_after', 'views', 'reach_from', 'reach_to', 'reach_days', 'impressions', 'ctr_pct', 'note']
SWAP_DAY = '2026-10-19'


def views(ids):
    import ytupload
    yt = ytupload.service(); out = {}
    for i in range(0, len(ids), 50):
        for v in yt.videos().list(part='statistics', id=','.join(ids[i:i + 50])).execute()['items']:
            out[v['id']] = int(v['statistics'].get('viewCount', 0))
    return out


def reach(ids, d0, d1):
    """d0~d1(포함) 날짜 csv에서 영상별 노출 합·가중 클릭률. 받은 날 수도 돌려준다."""
    agg = collections.defaultdict(lambda: [0, 0.0]); days = []
    for f in sorted(glob.glob(os.path.join(REACH, '*.csv'))):
        d = os.path.basename(f)[:10]
        if not (d0 <= d <= d1): continue
        days.append(d)
        for r in csv.DictReader(open(f, encoding='utf-8')):
            if r['video_id'] in ids:
                imp = int(r.get('video_thumbnail_impressions') or 0)
                agg[r['video_id']][0] += imp; agg[r['video_id']][1] += imp * float(r.get('video_thumbnail_impressions_ctr') or 0)
    res = {v: (agg[v][0], round(agg[v][1] / agg[v][0] * 100, 2) if agg[v][0] else '') for v in ids}
    return res, (days[0] if days else '', days[-1] if days else '', len(days))


def rows():
    return list(csv.DictReader(open(CSV, encoding='utf-8-sig'))) if os.path.exists(CSV) else []


def write(new):
    old = rows(); exists = os.path.exists(CSV)
    with open(CSV, 'a', encoding='utf-8-sig' if not exists else 'utf-8', newline='') as fh:
        w = csv.DictWriter(fh, COLS)
        if not exists: w.writeheader()
        for r in new: w.writerow(r)


def before(targets):
    """targets: [(video_id, ep, changed, thumb_before, thumb_after, note)]"""
    ids = [t[0] for t in targets]; vw = views(ids)
    rc, (f, t, n) = reach(set(ids), '2026-10-10', '2026-10-16')
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    write([dict(measured_at=now, phase='before', video_id=v, ep=e, changed=c, thumb_before=tb, thumb_after=ta, views=vw.get(v, ''),
                reach_from=f, reach_to=t, reach_days=n, impressions=rc[v][0], ctr_pct=rc[v][1], note=no) for v, e, c, tb, ta, no in targets])


def after():
    base = [r for r in rows() if r['phase'] == 'before']
    ids = [r['video_id'] for r in base]; vw = views(ids)
    d0 = (datetime.date.fromisoformat(SWAP_DAY) + datetime.timedelta(days=1)).isoformat()
    rc, (f, t, n) = reach(set(ids), d0, '2099-12-31')
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M'); new = []
    print(f'교체 다음 날부터 노출 {f}~{t}({n}일) · 기준은 교체 전 7일')
    print('| 편 | 교체 | 조회 전→후(+늘어난 수) | 노출 7일 전 → 후(일평균) | 클릭률 전 → 후 |\n|---|---|---|---|---|')
    for r in base:
        v = r['video_id']; imp, ctr = rc[v]
        new.append(dict(measured_at=now, phase='after', video_id=v, ep=r['ep'], changed=r['changed'], thumb_before=r['thumb_before'], thumb_after=r['thumb_after'],
                        views=vw.get(v, ''), reach_from=f, reach_to=t, reach_days=n, impressions=imp, ctr_pct=ctr, note=''))
        bd = int(r['reach_days'] or 0); bi = int(r['impressions'] or 0)
        per_b = round(bi / bd, 1) if bd else ''; per_a = round(imp / n, 1) if n else ''
        dv = vw.get(v, 0) - int(r['views'] or 0)
        print(f"| {r['ep']} {v} | {r['changed']} | {r['views']}→{vw.get(v, '')}(+{dv}) | {bi}({per_b}/일) → {imp}({per_a}/일) | {r['ctr_pct'] or '-'}% → {ctr or '-'}% |")
    write(new)


if __name__ == '__main__':
    if sys.argv[1] == 'after': after()
    else: print('before는 교체 작업 스크립트에서 before(targets)로 부른다')
