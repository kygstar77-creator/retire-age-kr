# 썸네일·제목 짝 비교 — 기준 리뉴얼 C갈래(10/19, work/research/criteria/registry.md C-08·C-20·C-21·C-22·C-23·C-31)
# 왜: 절대 점수 문턱(6·7·8)은 근거가 없고 AI 심사는 판·질문·순서에 따라 1~2점 흔들린다(judge-drift-1006, MT-Bench·Wang 2023 순서 편향·G-Eval·Thakur 2024).
#   그래서 '지금판 vs 새판'을 같은 차수·같은 비교판(경쟁 상위 5와 나란히)에 놓고, 순서를 바꿔 2번 묻는다. **2번 모두 새판이 이겨야** 바꾼다. 점수는 참고로만 적는다.
#   판 크기는 412px(휴대폰 홈 피드, 기본) + 168px(검색·관련 영상, 보조) — C-08(우리 롱폼 조회 98.7%가 탐색, 412px 한 글자 약 0.83° > 고령 임계 0.52°).
#   모델은 하나 고정(C-23, 기본 gemini-3.1-flash-lite — JUDGE_MODEL로 바꾸면 결과 첫 줄에 이름이 남는다).
#   AI 심사는 사람 대신이 아니다(가상 인물 한계 Nature MI 2024) — 실제 판정은 유튜브 '테스트 및 비교'(C-25, 사장님 고급 기능 확인 전이라 이 도구는 거기까지 하지 않는다).
# 쓰는 법:
#   py -3.12 work/thumbpair.py thumb <지금.png> <새.png> <경쟁1.jpg> … [--ctx 설명.txt] [--out 폴더]
#   py -3.12 work/thumbpair.py title "<지금 제목>" "<새 제목>" --comp 경쟁제목.txt [--body 본문요약.txt] [--out 폴더]
# 결과: 폴더에 pair_<종류>.md(두 번 답 원문·판정), 종료코드 0 = 새판 2번 다 이김(바꿔도 됨), 3 = 아님(지금 것 유지).
import sys, os, json, base64, urllib.request, re, datetime
sys.stdout.reconfigure(encoding='utf-8')
MODEL = os.environ.get('JUDGE_MODEL', 'gemini-3.1-flash-lite')
KEYF = r'C:\Users\강영준\Documents\gemini_key.txt'
SIZES = (412, 168)   # C-08: 412 기본 + 168 보조 (옛 320px은 근거 없어 뺌)


def key():
    return [l.split('=', 1)[-1].strip() for l in open(KEYF, encoding='utf-8-sig') if l.strip()][0]


def ask(text, imgs=()):
    parts = [{'text': text}] + [{'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(open(p, 'rb').read()).decode()}} for p in imgs]
    r = json.load(urllib.request.urlopen(urllib.request.Request(
        f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key()}',
        data=json.dumps({'contents': [{'parts': parts}]}).encode(), headers={'Content-Type': 'application/json'}), timeout=240))
    return r['candidates'][0]['content']['parts'][0]['text']


def board(first, second, comps, W, path):
    """맨 위 줄: A·B(우리 두 판), 아래: 경쟁. 16:9로 잘라 W px 폭."""
    from PIL import Image, ImageDraw, ImageFont
    F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 13)
    def fit(p):
        im = Image.open(p).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)
        if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
        return im.resize((W, round(W * 9 / 16)), Image.LANCZOS)
    items = [(first, 'A'), (second, 'B')] + [(c, f'경쟁 {i + 1}') for i, c in enumerate(comps)]
    HH = round(W * 9 / 16); cols = 3 if W < 300 else 2; pad = 12; rows = (len(items) + cols - 1) // cols
    bd = Image.new('RGB', (cols * (W + pad) + pad, rows * (HH + 26) + pad), 'white'); d = ImageDraw.Draw(bd)
    for n, (p, lab) in enumerate(items):
        x = pad + (n % cols) * (W + pad); y = pad + (n // cols) * (HH + 26)
        bd.paste(fit(p), (x, y)); d.text((x, y + HH + 4), lab, fill='black', font=F)
    bd.save(path); return path


def verdict(ans):
    m = re.findall(r'(?:더 나은 쪽|승자|이긴 쪽)\s*[:：]\s*\**\s*([AB])', ans)
    return m[-1] if m else None


THUMB_Q = ('한국 재테크 유튜브 썸네일 짝 비교입니다. 판 위쪽 A·B는 같은 영상의 썸네일 두 안, 아래는 같은 주제 경쟁 상위작입니다. '
           '이미지 1장째는 휴대폰 홈 피드 크기(가로 412px), 2장째는 검색·관련 영상 크기(168px)입니다. 시청자는 40~60대.\n'
           '물음: 경쟁작 옆에서 1초 봤을 때 (1) 무슨 내용인지 바로 알고 (2) 먼저 누르고 싶은 쪽은 A와 B 중 어느 쪽인가요? 412px 판을 먼저 보고 168px은 보조로.\n'
           '낚시·과장(내용과 다른 말)이 있으면 그쪽은 집니다. 비슷하면 그래도 하나를 고르세요.\n'
           '형식: A 한 줄 평 / B 한 줄 평 / 마지막 줄 정확히 "더 나은 쪽: A" 또는 "더 나은 쪽: B".')

TITLE_Q = ('한국 재테크 유튜브 제목 짝 비교입니다. [경쟁 상위 제목]과 나란히 놓고 A·B 두 안 중 하나를 고르세요. 시청자는 40~60대.\n'
           '보는 것(C-31): ① 1초에 주제가 보이나 ② 궁금증이 있나 ③ 낚시·과장이 아닌가(본문 요약과 일치 — 어긋나면 그쪽은 집니다) ⑤ 가장 중요한 검색어가 앞에 있나. '
           '경쟁 제목 틀과 닮은 것은 감점하지 않습니다(사장님 10/19 "좋은 건 따라 해야지").\n'
           '형식: A 한 줄 평 / B 한 줄 평 / 마지막 줄 정확히 "더 나은 쪽: A" 또는 "더 나은 쪽: B".\n')


def run_pair(kind, cur, new, ask_fn):
    """순서를 바꿔 두 번. 새 안이 두 번 다 이겨야 True."""
    a1 = ask_fn(cur, new)     # 1번째: A=지금, B=새
    a2 = ask_fn(new, cur)     # 2번째: A=새, B=지금
    w1 = {'A': '지금', 'B': '새'}.get(verdict(a1)); w2 = {'A': '새', 'B': '지금'}.get(verdict(a2))
    ok = (w1 == '새' and w2 == '새')
    return ok, w1, w2, a1, a2


def main(a):
    out = a[a.index('--out') + 1] if '--out' in a else os.getcwd()
    os.makedirs(out, exist_ok=True)
    kind = a[0]
    if kind == 'thumb':
        pos = [x for i, x in enumerate(a[1:], 1) if not x.startswith('--') and a[i - 1] not in ('--ctx', '--out')]
        cur, new, comps = pos[0], pos[1], pos[2:]
        if len(comps) < 5: print(f'[경고] 경쟁 썸네일 {len(comps)}장 — 비교판은 같은 주제 경쟁 상위 5(C-22)')
        ctx = open(a[a.index('--ctx') + 1], encoding='utf-8').read() if '--ctx' in a else ''
        def f(x, y):
            ps = [board(x, y, comps, W, os.path.join(out, f'pair_{W}_{os.path.basename(x)[:20]}.png')) for W in SIZES]
            return ask(THUMB_Q + ('\n영상 내용: ' + ctx if ctx else ''), ps)
    elif kind == 'title':
        cur, new = a[1], a[2]
        comp = open(a[a.index('--comp') + 1], encoding='utf-8').read() if '--comp' in a else ''
        body = open(a[a.index('--body') + 1], encoding='utf-8').read()[:4000] if '--body' in a else ''
        if comp.count('\n') < 4: print('[경고] 경쟁 상위 제목 5개 미만(C-22)')
        f = lambda x, y: ask(TITLE_Q + f'[경쟁 상위 제목]\n{comp}\n[본문 요약]\n{body}\n[A] {x}\n[B] {y}')
    else:
        sys.exit('thumb | title')
    ok, w1, w2, a1, a2 = run_pair(kind, cur, new, f)
    rep = (f'# 짝 비교 {kind} · {datetime.datetime.now():%Y-%m-%d %H:%M} · 모델 {MODEL}\n지금: {cur}\n새: {new}\n'
           f'1번째(A=지금,B=새) 이긴 쪽: {w1}\n2번째(A=새,B=지금) 이긴 쪽: {w2}\n'
           f'판정: {"바꿈 — 새 안이 두 번 다 이김" if ok else "지금 것 유지 — 두 번 다 이기지 못함"}\n\n## 1번째 답\n{a1}\n\n## 2번째 답\n{a2}\n')
    p = os.path.join(out, f'pair_{kind}.md'); open(p, 'w', encoding='utf-8').write(rep)
    print(rep.split('\n\n## ')[0]); print('기록', p)
    return 0 if ok else 3


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
