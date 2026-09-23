# 교차검증 — 사장님 지시(2026-09-14): 내 초안 → ChatGPT(사실·정확성) → Gemini(구조·말투) → 지적은 원문으로 다시 확인해 반영/근거 들어 유지 → 반영·미반영 보고.
# 예전엔 웨일 창에서 손으로 했는데 무인 루틴은 화면을 못 쓰므로 API로 한다. 프롬프트는 예전 gpt_prompt.txt·gemini_blog.txt 그대로.
#
#   python work/crosscheck.py check <pkg폴더>      # facts.txt + 조각(b*/c*)을 GPT(사실)·Gemini(구조·말투)에 보내 pkg/check_gpt.txt, pkg/check_gemini.txt 저장
#   python work/crosscheck.py draft <pkg폴더>      # (선택) facts.txt로 Gemini가 초안 → pkg/gemini_draft.txt
#   python work/crosscheck.py models              # 키가 맞는지·쓸 모델 이름 확인
#
# 키 파일(사장님이 넣는다):
#   C:\Users\강영준\Documents\openai_key.txt   KEY=sk-...   (선택: MODEL=gpt-...)
#   C:\Users\강영준\Documents\gemini_key.txt   KEY=AIza...  (선택: MODEL=gemini-...)
# 키가 없는 역할은 건너뛰고 그 사실을 출력한다. 지어내지 않는다.
import sys, os, re, json, glob, time, urllib.request, urllib.error
sys.stdout.reconfigure(encoding='utf-8')
DOCS = r'C:\Users\강영준\Documents'
TODAY = time.strftime('%Y년 %m월 %d일')

def load_key(name):
    p = os.path.join(DOCS, name)
    if not os.path.exists(p): return None
    kv = {}
    for line in open(p, encoding='utf-8-sig'):
        if '=' in line: k, v = line.strip().split('=', 1); kv[k.strip().upper()] = v.strip()
    return kv if kv.get('KEY') else None

def http(url, body=None, headers=None, timeout=180):
    body_ = body
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers={'Content-Type': 'application/json', **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r: return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read()[:300].decode("utf-8", "ignore")
        # 503(혼잡)·429(속도제한)은 잠시 뒤 되는 경우가 많다 — 세 번까지 기다렸다 다시 건다
        if e.code in (429, 503) and getattr(http, '_try', 0) < 3:
            http._try = getattr(http, '_try', 0) + 1
            time.sleep(8 * http._try)
            try: return http(url, body=body_, headers=headers, timeout=timeout)
            finally: http._try = 0
        raise RuntimeError(f'HTTP {e.code} {body}')

# ---- OpenAI ----
def openai_models(kv):
    d = http('https://api.openai.com/v1/models', headers={'Authorization': 'Bearer ' + kv['KEY']})
    return sorted(m['id'] for m in d.get('data', []))

def openai_pick(kv):
    if kv.get('MODEL'): return kv['MODEL']
    ids = openai_models(kv)
    for pat in (r'^gpt-5(\.\d+)?$', r'^gpt-5', r'^gpt-4\.1$', r'^gpt-4o$'):
        c = [i for i in ids if re.match(pat, i) and 'mini' not in i and 'nano' not in i and 'realtime' not in i and 'audio' not in i]
        if c: return sorted(c)[-1]
    return ids[-1]

def openai_chat(kv, system, user):
    model = openai_pick(kv)
    d = http('https://api.openai.com/v1/chat/completions', {'model': model, 'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]},
             headers={'Authorization': 'Bearer ' + kv['KEY']})
    return model, d['choices'][0]['message']['content']

# ---- Gemini ----
def gemini_models(kv):
    d = http('https://generativelanguage.googleapis.com/v1beta/models?key=' + kv['KEY'])
    return sorted(m['name'].split('/')[-1] for m in d.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', []))

def gemini_pick(kv, prefer='pro'):
    if kv.get('MODEL'): return kv['MODEL']
    ids = [i for i in gemini_models(kv) if not re.search(r'tts|image|embed|audio|live|omni|lite|robot|computer|customtools|thinking|exp', i)]
    def ver(i):
        m = re.search(r'gemini-(\d+(?:\.\d+)?)', i); return float(m.group(1)) if m else 0
    order = ('pro', 'flash') if prefer == 'pro' else ('flash', 'pro')
    for kind in order:
        c = [i for i in ids if kind in i]
        if c: return sorted(c, key=lambda i: (ver(i), 'preview' not in i))[-1]
    return ids[-1]

def gemini_candidates(kv, prefer='pro'):
    ids = [i for i in gemini_models(kv) if not re.search(r'tts|image|embed|audio|live|omni|lite|robot|computer|customtools|thinking|exp', i)]
    def ver(i):
        m = re.search(r'gemini-(\d+(?:\.\d+)?)', i); return float(m.group(1)) if m else 0
    pro = sorted([i for i in ids if 'pro' in i], key=lambda i: (ver(i), 'preview' not in i), reverse=True)
    flash = sorted([i for i in ids if 'flash' in i], key=lambda i: (ver(i), 'preview' not in i), reverse=True)
    if kv.get('MODEL'): return [kv['MODEL']] + flash[:3]
    return (pro[:1] + flash[:4]) if prefer == 'pro' else flash[:4]

def gemini_chat(kv, system, user, prefer='pro'):
    # 무료 등급은 Pro 한도가 없거나 작고(429), 인기 모델은 한때 503이 난다(2026-09-23 실측). 후보를 차례로 시도하고 성공한 모델 이름을 돌려준다.
    last = None
    for model in gemini_candidates(kv, prefer):
        try:
            d = http(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={kv["KEY"]}',
                     {'system_instruction': {'parts': [{'text': system}]}, 'contents': [{'parts': [{'text': user}]}]})
            return model, ''.join(p.get('text', '') for p in d['candidates'][0]['content']['parts'])
        except RuntimeError as e:
            last = e
            if any(x in str(e) for x in ('HTTP 429', 'HTTP 404', 'HTTP 503', 'quota', 'UNAVAILABLE')): time.sleep(2); continue
            raise
    raise last

# ---- 묶음 읽기 ----
def read_pkg(pkg):
    root = os.path.dirname(pkg.rstrip('\\/')) if os.path.basename(pkg.rstrip('\\/')) == 'pkg' else pkg
    # facts.txt는 주제 폴더에 두는 게 규약이지만, pkg 안에 둔 회차도 있어 둘 다 본다.
    # (빈 사실표로 검증이 돌면 전 항목이 '확인 불가'로 나와 검증이 무의미해진다)
    facts = ''
    for facts_p in (os.path.join(root, 'facts.txt'), os.path.join(pkg, 'facts.txt')):
        if os.path.exists(facts_p):
            facts = open(facts_p, encoding='utf-8').read()
            break
    if not facts.strip():
        print('경고: facts.txt를 찾지 못했다 — 사실 대조는 전부 확인 불가로 나온다', file=sys.stderr)
    title_p = os.path.join(pkg, 'title.txt'); title = open(title_p, encoding='utf-8').read().strip() if os.path.exists(title_p) else ''
    pieces = sorted(glob.glob(os.path.join(pkg, 'b[0-9]*.txt')) + glob.glob(os.path.join(pkg, 'c[0-9]*.txt')))
    body = '\n\n'.join(open(p, encoding='utf-8').read().strip() for p in pieces)
    kind = '블로그' if any(os.path.basename(p).startswith('b') for p in pieces) else '카페'
    return facts, title, body, kind

GPT_SYSTEM = '너는 사실검증 담당이다. 새 정보·해석 추가 제안은 하지 마라. 맞는 문장은 적지 마라.'
GPT_USER = """아래는 [사실표]로 쓴 네이버 {kind} 글이다. 오늘은 {today}(한국)이다.
1) [사실표]와 글을 한 문장씩 대조해서, 글에 있는데 사실표에 없는 숫자·날짜·주장, 사실표와 다르게 옮긴 것, 조건을 빠뜨려 오해를 부를 문장을 찾아 줘.
2) 사실표에 적힌 출처(URL·법령명)를 아는 범위에서 대조하고, 확인 못 하는 것은 '확인 불가'라고 적어.
형식: 틀림 / 확인 불가 / 오해 소지 항목만 번호로 — 원문 문장 · 문제 · 근거 · 고친 문장. 마지막에 AI가 쓴 것 같은 어색한 문장을 따로 적어.

[제목] {title}

[사실표]
{facts}

[글]
{body}"""
GEMINI_SYSTEM = '너는 네이버 블로그·카페 글의 구조와 말투를 보는 편집자다. 사실·숫자는 건드리지 말고, 새 정보·전망·권유·질문형 마무리를 넣자고 하지 마라.'
GEMINI_USER = """아래 네이버 {kind} 글({tone_word})을 모바일 독자 눈으로 봐 줘. 오늘은 {today}.
지적할 것만: (1) 첫 세 줄이 읽는 사람이 바로 얻는 게 뭔지 말해 주는지 (2) 소제목·문단 순서가 자연스러운지 (3) 한 문단이 길어 끊어야 할 곳 (4) 같은 말 반복 (5) 사람이 안 쓰는 표현·번역투 (6) 숫자가 문장 속에서 읽히는지.
형식: 번호 · 원문 문장(그대로) · 문제 · 고친 문장. 고친 문장은 그대로 붙여 넣을 수 있게 완성된 문장으로 써. 사실·숫자·결론은 바꾸지 마. 잘한 점은 적지 마. 어색한 문장은 많으면 15개까지 전부 골라.

[제목] {title}

[글]
{body}"""
DRAFT_USER = """네이버 {kind}(개인 재테크, 모바일 독자)에 올릴 글을 써 줘. 아래 [확인된 사실]만 쓰고, 여기 없는 숫자·날짜·해석·전망·권유·경험담은 절대 추가하지 마. 글쓴이의 개인 경험이나 지인 이야기를 지어내지 마. 오늘은 {today}.
[제목] {title}
[꼭 담을 항목 — 사람들이 검색하는 것] {wants}

말투와 형식:
{tone}
- 소제목은 줄 하나로 따로 쓰고 앞에 '## '를 붙여. 소제목 3~4개.
- 사진이 들어갈 자리에 '[이미지]' 한 줄을 {img}번 넣어(첫 문단 뒤에 하나).
- 마지막은 질문이 아니라 사실 문장으로 끝내. 이모지 없음. "정리하면·핵심은·결론적으로·시사한다" 쓰지 마.
- 글이 스스로를 설명하는 문장("원문을 대조했습니다", "이 글은 ~만 다뤘습니다") 쓰지 마. 출처는 맨 끝에 한 줄.
- 분량: {length}.

[확인된 사실]
{facts}"""
TONE_BLOG = """- 평어체(~다·~이다), 담백하게. 첫 문단은 읽는 사람이 바로 얻는 게 뭔지 세 줄 안에.
- 한 문단 2~4문장, 숫자는 문장 속에서 읽히게(예: "12억을 넘으면 그때부터 세금이 붙는다")."""
TONE_CAFE = """- 카페 회원에게 말하듯. 첫 문장은 회원이 겪는 상황 한 줄(예: "집은 있는데 매달 들어오는 돈이 없다는 글이 자주 올라오죠").
- 문장은 짧게(평균 30자 안팎). ~습니다·~입니다는 네 문장 중 하나만, 나머지는 ~죠·~네요·~요·~다를 섞어.
- 법 조문 번호를 본문에 나열하지 마(출처 줄에만). 본문은 "그래서 뭐가 달라지나"로 풀어.
- 저는·제가 같은 1인칭은 열 문장에 한 번 정도, 단 경험은 지어내지 마."""

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'models'
    oa, gm = load_key('openai_key.txt'), load_key('gemini_key.txt')
    if cmd == 'models':
        print('OpenAI:', ('키 없음' if not oa else openai_pick(oa)), '| Gemini:', ('키 없음' if not gm else gemini_pick(gm))); return
    pkg = os.path.abspath(sys.argv[2]); facts, title, body, kind = read_pkg(pkg)
    if cmd == 'draft':
        op = os.path.join(pkg, 'order.txt')
        if os.path.exists(op): kind = '카페' if '카페' in open(op, encoding='utf-8').readline() else '블로그'
        elif len(sys.argv) > 3: kind = '카페' if sys.argv[3] == 'cafe' else '블로그'
    if not body and cmd == 'check': print('조각 파일 없음:', pkg); sys.exit(2)
    if cmd == 'draft':   # 글은 Gemini가 쓴다(사장님 2026-09-23: 내 한국어 문장은 전·후 다 이상하다). 나는 사실표·검증·조립만.
        if not gm: print('Gemini 키 없음 — 초안 건너뜀'); sys.exit(3)
        wp = os.path.join(pkg, 'wants.txt'); wants = open(wp, encoding='utf-8').read().strip() if os.path.exists(wp) else '(없음)'
        tone = TONE_BLOG if kind == '블로그' else TONE_CAFE
        length = '2,400~3,000자(공백 포함)' if kind == '블로그' else '1,500~1,900자(공백 포함)'
        model, out = gemini_chat(gm, '너는 한국 개인 재테크 블로그·카페에 글을 쓰는 사람이다. 한국 사람이 실제로 쓰는 문장으로 쓴다.',
                                 DRAFT_USER.format(kind=kind, today=TODAY, title=title, wants=wants, tone=tone, img=6 if kind == '블로그' else 3, length=length, facts=facts), prefer='pro')
        open(os.path.join(pkg, 'gemini_draft.txt'), 'w', encoding='utf-8').write(out); print(f'Gemini({model}) 초안 {len(out)}자 → pkg/gemini_draft.txt'); return
    done = []
    if oa:
        try:
            model, out = openai_chat(oa, GPT_SYSTEM, GPT_USER.format(kind=kind, today=TODAY, title=title, facts=facts, body=body))
            open(os.path.join(pkg, 'check_gpt.txt'), 'w', encoding='utf-8').write(f'[{model} {time.strftime("%Y-%m-%d %H:%M")}]\n' + out); done.append(f'GPT({model}) 사실검증 {len(out)}자 → check_gpt.txt')
        except Exception as e: done.append('GPT 실패: ' + str(e)[:200])
    elif gm:   # 전부 무료로(사장님 2026-09-23): OpenAI 키가 없으면 사실 대조도 Gemini(Pro)가 맡는다. 결과 파일 머리에 어느 모델인지 적힌다
        try:
            model, out = gemini_chat(gm, GPT_SYSTEM, GPT_USER.format(kind=kind, today=TODAY, title=title, facts=facts, body=body), prefer='pro')
            open(os.path.join(pkg, 'check_gpt.txt'), 'w', encoding='utf-8').write(f'[{model} {time.strftime("%Y-%m-%d %H:%M")} — OpenAI 키 없어 Gemini가 사실 대조]\n' + out); done.append(f'사실 대조를 Gemini({model})가 대신 {len(out)}자 → check_gpt.txt')
        except Exception as e: done.append('사실 대조(Gemini 대체) 실패: ' + str(e)[:200])
    else: done.append('GPT 건너뜀 — openai_key.txt 없음')
    if gm:
        try:
            model, out = gemini_chat(gm, GEMINI_SYSTEM, GEMINI_USER.format(kind=kind, tone_word=('평어체' if kind == '블로그' else '합쇼체'), today=TODAY, title=title, body=body), prefer='flash')
            open(os.path.join(pkg, 'check_gemini.txt'), 'w', encoding='utf-8').write(f'[{model} {time.strftime("%Y-%m-%d %H:%M")}]\n' + out); done.append(f'Gemini({model}) 구조·말투 {len(out)}자 → check_gemini.txt')
        except Exception as e: done.append('Gemini 실패: ' + str(e)[:200])
    else: done.append('Gemini 건너뜀 — gemini_key.txt 없음')
    for d in done: print(d)
    if not oa and not gm: sys.exit(3)

if __name__ == '__main__': main()
