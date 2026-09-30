# -*- coding: utf-8 -*-
"""파이어맵 상황판 데이터 빌더.

사용:
  py -3.12 work/dashboard/build.py                       # mcp_input.json 읽고 data.json·board.html 쓴다
  py -3.12 work/dashboard/build.py --mcp 다른파일.json --now "2026-10-01 09:00"

MCP에서만 나오는 것(예약 작업·회차·사용량)은 Python이 못 가져온다.
다른 세션이 MCP로 모아 mcp_input.json에 넣고 이 스크립트를 돌린다(README.md).
나머지(조직도·오늘 지시·결재함·결정·실험·유입·발행·커밋)는 저장소 파일에서 직접 읽는다.

원칙: 추측 금지. 못 찾은 값은 '확인 안 함'. 키·토큰·계정 식별자는 가린다.
스꾸(seukku) 예약 작업은 입력에 있어도 버린다.
"""
import hashlib
import sys, os, re, json, subprocess, argparse, datetime as dt

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
REPO = os.path.dirname(WORK)
RES = os.path.join(WORK, 'research')
KST = dt.timezone(dt.timedelta(hours=9))
NA = '확인 안 함'

# ── 조직 배치(agents.md 본부 기준, 2026-10-01). 사무실 방 순서 = 화면 순서 ──
DEPTS = [
    ('exec', '경영', ['soondol', 'firemap-meeting']),
    ('content', '콘텐츠본부', ['firemap-youtube-loop', 'firemap-video-producer', 'firemap-shorts',
                           'firemap-write', 'firemap-copywriter', 'firemap-editor']),
    ('design', '디자인실', ['firemap-visual-designer', 'firemap-motion-designer', 'firemap-illustrator',
                        'firemap-artist', 'firemap-designer-orgchart']),
    ('product', '제품본부', ['firemap-product-dev', 'firemap-designer', 'firemap-loop']),
    ('brand', '브랜드팀', ['firemap-brand-director', 'firemap-brand-researcher']),
    ('growth', '성장·수익본부', ['firemap-growth', 'firemap-bizdev']),
    ('venture', '신사업본부', ['firemap-venture', 'firemap-venture-research-global', 'firemap-venture-research-kr', 'firemap-venture-builder']),
    ('ops', '운영·품질본부', ['firemap-dispatcher', 'firemap-dispatcher-2', 'firemap-finishline-check', 'firemap-audit', 'firemap-watchdog', 'firemap-improve', 'firemap-report']),
    ('admin', '총무·인사팀', ['firemap-admin']),
    ('lab', 'AI 연구소', ['firemap-ai-lab']),
]
# 책상 이름(agents.md '자리' 열·예약 작업 제목에서 줄인 것)
NAME = {
    'soondol': '순돌이', 'firemap-meeting': '회의 의장',
    'firemap-youtube-loop': '유튜브·카페 총괄', 'firemap-video-producer': '영상 PD', 'firemap-shorts': '쇼츠 PD',
    'firemap-write': '카페·블로그 작가', 'firemap-copywriter': '카피라이터', 'firemap-editor': '문장 편집자',
    'firemap-visual-designer': '비주얼 디자이너', 'firemap-motion-designer': '모션 디자이너',
    'firemap-illustrator': '일러스트레이터', 'firemap-artist': '예술가', 'firemap-designer-orgchart': '조직도 그림(1회)',
    'firemap-product-dev': '제품 개발', 'firemap-designer': '프로덕트 디자이너', 'firemap-loop': '디자인 개선',
    'firemap-brand-director': '브랜드 디렉터', 'firemap-brand-researcher': '브랜드 리서처',
    'firemap-growth': '성장·유입', 'firemap-bizdev': '사업개발', 'firemap-venture': '신사업본부장',
    'firemap-audit': '감사관', 'firemap-watchdog': '발행 감시', 'firemap-improve': '생산·개선',
    'firemap-report': '보고 비서', 'firemap-venture-research-global': '해외 시장조사원', 'firemap-venture-research-kr': '국내 시장조사원', 'firemap-venture-builder': '신사업 빌더', 'firemap-dispatcher': '운영실장', 'firemap-dispatcher-2': '운영실장 2', 'firemap-finishline-check': '결승선 점검관', 'firemap-admin': '총무·인사', 'firemap-ai-lab': 'AI 연구소장',
}
# 역할 덮어쓰기(근거가 있는 것만)
ROLE_OVERRIDE = {
    'soondol': '조직·전략·직원 관리, 사장님 보고(공동대표·총괄)',
    'firemap-illustrator': '사물·아이콘 일러스트·채널 브랜딩 자산(9/30 사장님 결정: 캐릭터 없음)',
}
# 커밋 접두어 → 직원. 접두어가 없거나 모르는 말이면 '기타'
PREFIX = {
    'write': 'firemap-write', 'naverpost': 'firemap-write', 'runs': 'firemap-write',
    'yt-loop': 'firemap-youtube-loop', 'pd': 'firemap-video-producer', 'shorts': 'firemap-shorts',
    'product-dev': 'firemap-product-dev', 'loop': 'firemap-loop',
    'improve': 'firemap-improve', 'cafeapi.py': 'firemap-improve',
    'audit': 'firemap-audit', 'growth': 'firemap-growth', 'meeting': 'firemap-meeting',
    'venture': 'firemap-venture', 'ventures': 'firemap-venture', 'research-global': 'firemap-venture-research-global', 'research-kr': 'firemap-venture-research-kr', 'builder': 'firemap-venture-builder', 'dispatch': 'firemap-dispatcher', 'finishline': 'firemap-finishline-check', 'report': 'firemap-report',
    'beat': 'firemap-watchdog', 'watchdog': 'firemap-watchdog', 'bizdev': 'firemap-bizdev',
    'designer': 'firemap-designer', 'copywriter': 'firemap-copywriter', 'editor': 'firemap-editor',
    'artist': 'firemap-artist', 'admin': 'firemap-admin', 'visual': 'firemap-visual-designer',
    'motion': 'firemap-motion-designer', 'illustrator': 'firemap-illustrator',
    'brand-director': 'firemap-brand-director', 'brand-researcher': 'firemap-brand-researcher',
    'ai-lab': 'firemap-ai-lab', 'lab': 'firemap-ai-lab', 'orgchart': 'firemap-designer-orgchart',
    'org': 'soondol', 'ops': 'soondol', 'decision': 'soondol', 'roadmap': 'soondol', 'tools': 'soondol',
}
IDLE = re.compile(r'발행 없음|대본 없음|만들 편 없음|할 일 없음|헛회차|헛돎')
BLOCK = re.compile(r'막힘|막혀|만료|실패|429|403|미발행')

# ── 가림: 키·토큰·계정 식별자 ──
REDACT = [
    (re.compile(r'ca-pub-\d+'), 'ca-pub-•••'),
    (re.compile(r'\bG-[A-Z0-9]{6,}\b'), 'G-•••'),
    (re.compile(r'\bAF\d{5,}\b'), 'AF•••'),
    (re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+'), '(메일 주소 가림)'),
    (re.compile(r'\b(sk|pk|rk)-[A-Za-z0-9_-]{16,}'), '(키 가림)'),
    (re.compile(r'\bgh[pousr]_[A-Za-z0-9]{20,}'), '(토큰 가림)'),
    (re.compile(r'\bAIza[0-9A-Za-z_-]{20,}'), '(키 가림)'),
    (re.compile(r'\bey[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'), '(토큰 가림)'),
    (re.compile(r'(?i)(api[_-]?key|token|secret|password)\s*[=:]\s*\S+'), r'\1=(가림)'),
    (re.compile(r'\b[A-Fa-f0-9]{32,}\b'), '(긴 식별자 가림)'),
]


def redact(v):
    if isinstance(v, str):
        for rx, rep in REDACT:
            v = rx.sub(rep, v)
        return v
    if isinstance(v, list):
        return [redact(x) for x in v]
    if isinstance(v, dict):
        return {k: redact(x) for k, x in v.items()}
    return v


def read(rel):
    p = os.path.join(REPO, rel) if not os.path.isabs(rel) else rel
    try:
        with open(p, encoding='utf-8') as f:
            return f.read()
    except OSError:
        return None


def md_plain(s):
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
    s = re.sub(r'`([^`]+)`', r'\1', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    return s.strip()


def iso_kst(s):
    if not s:
        return None
    try:
        d = dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=KST)
    return d.astimezone(KST)


def fmt(d):
    return d.strftime('%m-%d %H:%M') if d else NA


def clip(s, n=140):
    s = ' '.join(s.split())
    return s if len(s) <= n else s[:n - 1] + '…'


# ── 저장소 읽기 ──
def agents_roles():
    txt = read('work/research/agents.md') or ''
    out = {}
    for line in txt.splitlines():
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) < 4:
            continue
        m = re.search(r'firemap-[a-z\-]+', cells[1])
        if m:
            out[m.group(0)] = {'seat': md_plain(cells[0]), 'hours': md_plain(cells[2]), 'role': md_plain(cells[3])}
    return out


def git_commits(now):
    since = (now - dt.timedelta(hours=24)).isoformat()
    try:
        raw = subprocess.run(
            ['git', '-c', 'i18n.logOutputEncoding=utf-8', '-C', REPO, 'log', f'--since={since}',
             '--pretty=%aI|%s'], capture_output=True, text=True, encoding='utf-8', timeout=60).stdout
    except Exception:
        return None
    rows = []
    for line in raw.splitlines():
        if '|' not in line:
            continue
        when, subj = line.split('|', 1)
        if subj.startswith('Merge '):
            continue
        head = subj.split(':', 1)[0] if ':' in subj else ''
        who = None
        for tok in re.findall(r'[A-Za-z][\w\-.]*', head):
            if tok in PREFIX:
                who = PREFIX[tok]
                break
        body = subj.split(':', 1)[1].strip() if (who and ':' in subj) else subj
        # 'write 22시: ...' 같은 회차 표기는 앞에 남긴다
        hour = re.search(r'(\d{2})시', head)
        if who and hour:
            body = f'{hour.group(1)}시 회차 — ' + body
        rows.append({'at': iso_kst(when), 'who': who, 'subject': subj, 'summary': body})
    return rows


def watchdog_last():
    txt = read('work/watchdog_log.json')
    if not txt:
        return None
    try:
        d = json.loads(txt)[-1]
    except Exception:
        return None
    at = None
    try:
        at = dt.datetime.strptime(d.get('at', ''), '%Y-%m-%d %H:%M').replace(tzinfo=KST)
    except ValueError:
        pass
    alerts = d.get('alert') or []
    stock = d.get('stock') or {}
    s = f"감시 기록: 경고 {len(alerts)}건 · 대기 묶음 블로그 {stock.get('blog', '?')}·카페 {stock.get('cafe', '?')}"
    return {'at': at, 'summary': s}


def today_md():
    txt = read('work/research/meeting/today.md')
    if txt is None:
        return None
    lines = txt.splitlines()
    sections, cur = [], None
    for ln in lines:
        m = re.match(r'^(#{1,2}) (.+)$', ln)
        if m:
            cur = {'title': md_plain(m.group(2)), 'level': len(m.group(1)), 'body': []}
            sections.append(cur)
        elif cur:
            cur['body'].append(ln)
    orders, priorities, urgent, blocked, done, per_staff = [], [], [], [], [], {}
    for s in sections:
        body = '\n'.join(s['body'])
        t = s['title']
        if t.startswith('[지시]'):
            staff = sorted(set(re.findall(r'firemap-[a-z\-]+', body)))
            owner = re.search(r'담당:\s*(.+?)(?:\. 기한|$)', body, re.M)
            due = re.search(r'기한:\s*([^\n.]+)', body)
            orders.append({'title': t.replace('[지시]', '').strip(), 'owner': md_plain(owner.group(1)) if owner else NA,
                           'due': md_plain(due.group(1)) if due else NA, 'staff': staff})
            for sid in staff:
                per_staff.setdefault(sid, []).append('[지시] ' + t.replace('[지시]', '').split('(')[0].strip())
        elif t.startswith('최우선'):
            for ln in s['body']:
                m = re.match(r'^\s*\d+\.\s+(.+)$', ln)
                if m:
                    priorities.append(md_plain(m.group(1)))
        elif t.startswith('긴급'):
            urgent.append(t)
        if '막힘' in t:
            items = [md_plain(re.sub(r'^\s*[-*\d.]+\s*', '', ln)) for ln in s['body'] if ln.strip()]
            blocked.append({'title': t, 'items': items})
        if t.startswith('직원별'):
            sid = None
            for ln in s['body']:
                m = re.match(r'^- \*\*(firemap-[a-z\-]+)[^*]*\*\*(.*)$', ln)
                if m:
                    sid = m.group(1)
                    rest = m.group(2).strip()
                    rest = rest[1:].strip() if rest.startswith(':') else ''
                    if rest:
                        per_staff.setdefault(sid, []).append(md_plain(rest))
                        sid = None
                    continue
                m2 = re.match(r'^\s+1\.\s+(.+)$', ln)
                if sid and m2:
                    per_staff.setdefault(sid, []).append(md_plain(m2.group(1)))
                    sid = None
    for ln in lines:
        if re.match(r'^\s*[-*]?\s*완료:', ln):
            done.append(md_plain(re.sub(r'^\s*[-*]?\s*', '', ln)))
    return {'orders': orders, 'priorities': priorities, 'urgent': urgent, 'blocked': blocked,
            'done': done, 'per_staff': per_staff, 'headline': next((md_plain(l) for l in lines if l.startswith('로드맵 판정')), None)}


def approvals():
    txt = read('work/research/approvals.md')
    if txt is None:
        return None
    out, head, sec_date = [], None, ''
    WAIT = re.compile(r'결재 대기|허락 필요')
    for line in txt.splitlines():
        h = re.match(r'^## (\d{4}-\d{2}-\d{2}(?: \S+)?)', line)
        if h:
            sec_date = h.group(1)
        if not line.startswith('|'):
            head = None if not line.strip() else head
            continue
        if re.match(r'^\|[\s\-|]+\|$', line):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if head is None:
            head = cells
            continue
        col = lambda *names: next((cells[i] for i, h_ in enumerate(head) if any(n in h_ for n in names) and i < len(cells)), '')
        status = col('상태')
        if not WAIT.search(status):
            continue
        req = md_plain(col('요청', '도구'))
        title = re.split(r'\s—\s', req)[0]
        title = re.sub(r'^\[[^\]]+\]\s*', '', title)
        out.append({'date': col('날짜') or sec_date or NA, 'title': clip(title, 70), 'detail': clip(req, 260),
                    'cost': clip(md_plain(col('비용')), 90) or NA, 'why': clip(md_plain(col('기대', '좋아지나')), 220),
                    'status': clip(md_plain(status), 120)})
    # '## 날짜 결재 요청 — 제목' 절(예고 제외)
    for m in re.finditer(r'^## (\S+ \S+) 결재 요청 — (.+)$\n((?:(?!^## ).*\n?)*)', txt, re.M):
        date, title, body = m.group(1), md_plain(m.group(2)), m.group(3)
        req = re.search(r'결재 요청[^:]*:\*\*\s*(.+)', body) or re.search(r'결재 요청[^:\n]*:\s*(.+)', body)
        cost = '확인 안 함' if '확인 안 함' in body else NA
        out.append({'date': date, 'title': clip(title, 70), 'detail': clip(md_plain(req.group(1)) if req else '', 260),
                    'cost': cost, 'why': clip(md_plain(' '.join(l.strip('- ') for l in body.splitlines()[:3])), 220),
                    'status': '결재 대기'})
    for x in out:
        x['id'] = hashlib.sha1(x['title'].encode('utf-8')).hexdigest()[:12]
    return out


def decisions(n=10):
    txt = read('work/research/decisions/log.md')
    if txt is None:
        return None
    rows = []
    for ln in txt.splitlines():
        m = re.match(r'^(\d{4}-\d{2}-\d{2} \S+) · (.+)$', ln.strip())
        if m:
            parts = [p.strip() for p in m.group(2).split(' · ')]
            rows.append({'at': m.group(1)[5:], 'who': parts[0], 'what': clip(md_plain(parts[1]) if len(parts) > 1 else '', 200),
                         'why': clip(md_plain(' · '.join(parts[2:])), 200) if len(parts) > 2 else ''})
    return list(reversed(rows[-n:]))


def experiments():
    txt = read('work/research/experiments-registry.md')
    if txt is None:
        return None
    m = re.search(r'^## 진행 중\n((?:(?!^## ).*\n?)*)', txt, re.M)
    if not m:
        return []
    out = []
    for line in m.group(1).splitlines():
        if not line.startswith('|') or '---' in line:
            continue
        c = [md_plain(x.strip()) for x in line.strip('|').split('|')]
        if c[0] == 'ID' or len(c) < 6:
            continue
        out.append({'id': c[0], 'what': c[1], 'ab': c[2], 'metric': c[3], 'period': c[4], 'due': c[5]})
    return out


def revenue(now, manual):
    txt = read('work/research/roadmap.md') or ''
    ym = now.strftime('%Y-%m')
    rows = re.findall(r'^\| (\d{4}-\d{2}) \| ([\d,]+만) \|', txt, re.M)
    target = next(((m, t) for m, t in rows if m >= ym), None)
    actual = manual.get('revenue_krw') if manual else None
    return {'month': target[0] if target else NA, 'target': (target[1] + '원') if target else NA,
            'target_krw': int(target[1].replace(',', '').replace('만', '')) * 10000 if target else None,
            'actual_krw': actual, 'source': (manual or {}).get('revenue_source', NA)}


def visitors():
    txt = read('work/research/growth/daily.md')
    if txt is None:
        return None
    last = None
    for ln in txt.splitlines():
        m = re.match(r'^(\d{4}-\d{2}-\d{2}[^·]*)· 세션 (\d+) / 고유 (\d+) · 화면 (\d+)', ln)
        if m:
            last = {'date': m.group(1).strip(), 'sessions': int(m.group(2)), 'uniques': int(m.group(3)),
                    'views': int(m.group(4)), 'note': '내부 점검 추정 제외' if '뺀 값' in ln or '제외' in ln else ''}
    t = re.search(r'하루 약 ([\d,]+) 화면', txt)
    if last:
        last['target_views'] = int(t.group(1).replace(',', '')) if t else None
    return last


def outputs_today(now):
    day = now.strftime('%Y-%m-%d')
    res = {'cafe': None, 'blog': None, 'shorts': None, 'longform': None}
    rt = read('work/runs_today.json')
    if rt:
        try:
            d = json.loads(rt)
            if d.get('date') == day:
                res['cafe'] = sum(1 for r in d['runs'] if (r.get('cafe') or {}).get('url'))
                res['blog'] = sum(1 for r in d['runs'] if (r.get('blog') or {}).get('url'))
        except Exception:
            pass
    sl = read('work/research/cardshorts/log.jsonl')
    if sl is not None:
        n = 0
        for ln in sl.splitlines():
            try:
                r = json.loads(ln)
            except Exception:
                continue
            if str(r.get('at', '')).startswith(day) and r.get('id'):
                n += 1
        res['shorts'] = n
    ul = read('work/research/longform/loop/uploads.jsonl')
    if ul is not None:
        n = 0
        for ln in ul.splitlines():
            try:
                r = json.loads(ln)
            except Exception:
                continue
            p = iso_kst(r.get('publishAt'))
            if p and p.strftime('%Y-%m-%d') == day and p <= now:
                n += 1
        res['longform'] = n
    return res


def stop_switches():
    out = []
    for f in sorted(os.listdir(RES)):
        if f.startswith('STOP_'):
            out.append(f)
    return out


# ── 직원 상태 판정 ──
def judge(tid, runs, ev, now):
    """runs: 최신순. ev: 최근 기록(커밋 또는 로그). 칩: 일함/헛돎/실패/대기/확인 안 함"""
    if tid == 'soondol':
        if ev and ev['at'] and (now - ev['at']).total_seconds() < 3 * 3600:
            return '일함', '3시간 안에 기록 있음'
        return '대기', '최근 3시간 기록 없음(채팅 세션)'
    if runs is None:
        return NA, '회차 정보 없음'
    if not runs:
        return '대기', '아직 첫 근무 전'
    r = runs[0]
    if r.get('status') == 'failed':
        return '실패', r.get('error') or '실패(사유 확인 안 함)'
    if r.get('status') == 'running':
        return '일함', '지금 근무 중'
    if ev:
        if IDLE.search(ev['summary']):
            return '헛돎', '마지막 기록이 "할 일 없음"'
        return '일함', '마지막 근무에 기록 남김'
    return NA, '24시간 안 기록 없음'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mcp', default=os.path.join(HERE, 'mcp_input.json'))
    ap.add_argument('--now')
    ap.add_argument('--out', default=HERE)
    a = ap.parse_args()
    now = dt.datetime.strptime(a.now, '%Y-%m-%d %H:%M').replace(tzinfo=KST) if a.now else dt.datetime.now(KST)

    mcp = {}
    try:
        with open(a.mcp, encoding='utf-8') as f:
            mcp = json.load(f)
    except OSError:
        print('mcp 입력 없음 — 예약 작업·사용량은 확인 안 함으로 둔다')
    tasks = {t['taskId']: t for t in mcp.get('tasks', [])
             if t.get('taskId', '').startswith('firemap-') and t.get('enabled') and 'seukku' not in t['taskId']}
    runs_all = mcp.get('runs', {})
    roles = agents_roles()
    commits = git_commits(now)
    wd = watchdog_last()
    td = today_md()

    by_staff = {}
    for c in commits or []:
        if c['who']:
            by_staff.setdefault(c['who'], []).append(c)

    placed = {sid for _, _, ids in DEPTS for sid in ids}
    extra = [tid for tid in tasks if tid not in placed]
    depts = DEPTS + ([('etc', '미분류', extra)] if extra else [])

    staff_out, dept_out = [], []
    for key, dname, ids in depts:
        members = []
        for sid in ids:
            if sid != 'soondol' and sid not in tasks:
                continue  # 꺼졌거나 없는 작업
            t = tasks.get(sid, {})
            runs = runs_all.get(sid) if sid != 'soondol' else None
            cs = sorted(by_staff.get(sid, []), key=lambda c: c['at'], reverse=True)
            ev = cs[0] if cs else None
            if sid == 'firemap-watchdog' and wd and (not ev or (wd['at'] and wd['at'] > ev['at'])):
                ev = wd
            chip, why = judge(sid, runs, ev, now)
            info = roles.get(sid, {})
            role = ROLE_OVERRIDE.get(sid) or info.get('role') or re.sub(r'^[^—]*—\s*', '', t.get('description', '')) or NA
            last_run = iso_kst(runs[0]['started_at']) if runs else None
            last_end = iso_kst(runs[0].get('last_activity_at')) if runs else None
            summary = ev['summary'] if ev else (why if chip in ('대기', '일함') else NA)
            members.append({
                'id': sid, 'name': NAME.get(sid, t.get('title') or sid), 'dept': key,
                'role': clip(role, 90), 'hours': info.get('hours') or NA,
                'chip': chip, 'chip_why': why,
                'last_run': (fmt(ev['at']) if ev else NA) if sid == 'soondol'
                            else (fmt(last_run) if runs else (NA if runs is None else '첫 근무 전')),
                'last_run_iso': last_run.isoformat() if last_run else None,
                'last_end_iso': last_end.isoformat() if last_end else None,
                'run_status': runs[0]['status'] if runs else None,
                'fails_in_last3': sum(1 for r in (runs or []) if r.get('status') == 'failed'),
                'next_run': fmt(iso_kst(t.get('nextRunAt'))) if t.get('nextRunAt') else (NA if sid != 'soondol' else '대화 때'),
                'summary': clip(summary, 150),
                'summary_at': fmt(ev['at']) if ev and ev.get('at') else None,
                'commits24': len(cs),
                'today': (td or {}).get('per_staff', {}).get(sid, [])[:2],
            })
        staff_out += members
        dept_out.append({'key': key, 'name': dname, 'ids': [m['id'] for m in members]})

    known = {m['id'] for m in staff_out}
    if td:
        for o in td['orders']:
            o['staff'] = [s for s in o['staff'] if s in known]
    chips = {}
    for m in staff_out:
        chips[m['chip']] = chips.get(m['chip'], 0) + 1

    blockers = []
    for c in commits or []:
        if BLOCK.search(c['subject']):
            blockers.append({'at': fmt(c['at']), 'who': NAME.get(c['who'], '기타'), 'text': clip(c['summary'], 140)})
    usage = mcp.get('usage') or {}
    wk = usage.get('weekly_all') or {}
    fh = usage.get('five_hour') or {}

    data = {
        'generated_at': now.isoformat(timespec='minutes'),
        'generated_label': now.strftime('%Y-%m-%d %H:%M'),
        'mcp_captured_at': fmt(iso_kst(mcp.get('captured_at'))) if mcp.get('captured_at') else NA,
        'approvals': approvals(),
        'numbers': {
            'revenue': revenue(now, mcp.get('manual')),
            'visitors': visitors(),
            'outputs': outputs_today(now),
            'usage': {'weekly_pct': wk.get('percentUsed'), 'weekly_reset': fmt(iso_kst(wk.get('resetsAt'))) if wk else NA,
                      'five_hour_pct': fh.get('percentUsed'), 'five_hour_reset': fmt(iso_kst(fh.get('resetsAt'))) if fh else NA},
            'commits24': len(commits) if commits is not None else None,
            'commits24_unmapped': sum(1 for c in (commits or []) if not c['who']),
        },
        'chips': chips,
        'depts': dept_out,
        'staff': staff_out,
        'queue': {
            'headline': (td or {}).get('headline'),
            'orders': (td or {}).get('orders', []),
            'priorities': (td or {}).get('priorities', []),
            'urgent': (td or {}).get('urgent', []),
            'done': (td or {}).get('done', []),
            'blocked_section': (td or {}).get('blocked', []),
            'blocked_commits': blockers[:8],
            'stop_switches': stop_switches(),
        } if td is not None else None,
        'decisions': decisions(10),
        'experiments': experiments(),
    }
    data = redact(data)
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, 'data.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    tpl = read(os.path.join(HERE, 'board.template.html'))
    if tpl:
        blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
        html = tpl.replace('/*__DATA__*/null', blob)
        with open(os.path.join(a.out, 'board.html'), 'w', encoding='utf-8') as f:
            f.write(html)
    print(f"data.json 씀 · 직원 {len(staff_out)}명 · 칩 {chips} · 결재 {len(data['approvals'] or [])}건 · 커밋24h {data['numbers']['commits24']}")


if __name__ == '__main__':
    main()
