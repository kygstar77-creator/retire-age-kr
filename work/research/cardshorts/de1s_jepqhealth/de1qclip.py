# de1s_jepqhealth — D-ETF-1 롱폼 5장(5:10~5:15) '1억 넣으면 통장에 남는 돈' 중 JEPQ 건보료를 자른 세로 쇼츠 props · c1clip 틀(C1S live, E-18 통과 틀) (firemap-video-producer 2026-11-03, de1s_schdgrow/de1sclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/de1s_jepqhealth/de1qclip.py   → work/video/de1s_jepqhealth.json
# 목소리 = D-ETF-1 voice.json 문장 wav 그대로(새 녹음 0) · 브랜드 첫·끝 줄 뺌
# 답 5초 안(A-49): 5:13(지역가입자·세금 15%) → 5:14(건보료 95만원) → 5:15(900만원)을 앞으로, 이유 5:10(세전 1,170만원·함정)·5:11(1,000만원 선)·5:12(JEPQ 하나뿐)을 뒤로
# 11/3 꼴 관문 ⓐ 첫 줄 36자 > 35: 5:13 wav를 쉼(1.52~1.80초) 1.64초에서 잘라 뒤 토막 'JEPQ는 세금 15%를 먼저 떼요.'만 씀(앞 '지역가입자로 놓고 계산하면,'은 화면 칸 이름 '지역가입자로 계산'·5:11 말로) — 받아쓰기(gemini-3.6-flash) '제피큐는 세금 15%를 먼저 떼요.' 확인, 새 녹음 0
# 11/3 이해 시험 1차(40·50·60세): 뜻 3/3·사라/팔라 0 · 900만원 다음 1,170만원 숫자 흐름 3/3 멈칫 → 첫 칸을 세전 1,170만원으로, 900만원 칸 이름 '세금과 건보료 빼면' · '전부 들어간다' 2/3 낯섦 → 칸 '1,000만원 넘으면 / 전부 건보료에' · 'JEPQ 하나' 2/3 갑작스러움 → '배당 ETF 12개 중'(calc_out §3 12줄) · JEPQ가 뭔지 2/3 → 0초 질문 '배당 ETF JEPQ' · 직장가입자 2/3 → 설명란 한 줄
#   '그리고' 빼고 1,170만원 줄을 맨 앞으로 옮기기는 시험(0.40·0.56·0.62초 자르기)에서 'JEPQ' 앞소리까지 잘려 버림 — 녹음 그대로
# 11/3 이해 시험 2차(43·54·63세): 뜻 3/3·사라/팔라 0 · 여전히 '900만원 → 다시 1,170만원' 3/3 멈칫, '세금 먼저 뗀다 ↔ 떼기 전 금액' 2/3 반대로 들림 → 900만원 줄(5:15)을 맨 끝 결론으로(세전 → 선 → 남는 돈), 5:10 칸 이름 '건보료는 이 돈으로'
# 11/3 이해 시험 3차(41·52·61세): 뜻·할 일 3/3·사라/팔라 0 · 900만원 식이 안 보임 3/3 → 끝 칸 '1,170만원에서 빼면 / 900만원'(세금 15%·건보료 95만원은 바로 앞에 나옴 — 반올림 176만은 숫자 대조가 원문 없음으로 거부해 안 씀, 식은 설명란) · '12개' 무엇 2/3 → '1억 계산한 12개 중' · 세금 먼저↔떼기 전 2/3, '함정' 2/3은 녹음 말이라 그대로(설명란 첫 줄에 풀어 씀)
# 11/3 눈 검사(sheet_1103.png): 긴 값 '세금 떼기 전 1,170만원'·'넘는 건 JEPQ 하나'는 글자가 작아져 손 동그라미(세로 폭이 글자 크기 따라감)가 글자 한가운데를 가로지름 → 값을 짧게, 말은 칸 이름으로('건보료는 세금 떼기 전'·'12개 중 넘는 건')
# 5:16~5:19(직장가입자·피부양자 2,000만원)는 다른 가입자 얘기라 뺌(곁가지) — 설명란 한 줄로만
# 화면 숫자 = calc_out.txt §3 JEPQ 줄(세전 11,710,000 · 건보 952,585 · 1년 통장 9,000,915)을 말 단위로
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'D-ETF-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out.txt', 'facts.txt') if os.path.exists(os.path.join(EP, f)))
CRED = {str(c['id']): c for c in json.load(open(os.path.join(VID, 'public', 'bg', 'detf', 'stock', 'credits.json'), encoding='utf-8'))}
TAIL = 36
SRC += ' ' + [k for k in BYTEXT if k.startswith('그리고 JEPQ는 세금 떼기 전에')][0]   # 11/3: 첫 칸 1,170만원은 이 클립 4번째 말 줄(5:10)이 말하는 값 — 먼저 화면에 띄움
SPLIT = {'지역가입자로 놓고 계산하면, JEPQ는': ('JEPQ는 세금 15%를 먼저 떼요.', 'audio/de1s_jepqhealth/jepq15_b.wav', 68)}
n = 0


def L(t):
    global n
    if t in SPLIT:
        txt, au, fr = SPLIT[t]; assert os.path.exists(os.path.join(VID, 'public', au)), au
        n += 1; return {'n': n, 'text': txt, 'audio': au, 'frames': fr}
    hit = [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)
    l = BYTEXT[hit[0]]; assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), t
    n += 1
    return {'n': n, 'text': l['text'], 'audio': l['audio'], 'frames': l['frames']}


def sc(label, lines, data):
    ls = [L(t) for t in lines]
    spoken = ' '.join(l['text'] for l in ls)
    strs = []
    walk = lambda x: [walk(y) for y in x] if isinstance(x, list) else ([walk(y) for y in x.values()] if isinstance(x, dict) else (strs.append(x) if isinstance(x, str) else None))
    walk(data)
    for d in re.findall(r'\d[\d,.]*', ' '.join(strs)):
        d = d.rstrip('.,')
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·D-ETF-1 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


scenes = [
    sc('1억 JEPQ', ['지역가입자로 놓고 계산하면, JEPQ는', '건보료도 95만원'],
       {'tiles': [['1년 배당 · 세금 떼기 전', '1,170만원', '', 0, 'ink'], ['지역가입자 건보료', '95만원 더', '', 68, 'ink']]}),
    sc('왜 붙나', ['그리고 JEPQ는 세금 떼기 전에'],
       {'tiles': [['건보료는 세금 떼기 전', '1,170만원', '', 0, 'ink']]}),
    sc('1,000만원 선', ['지역가입자는 예금 이자와 배당을', '다른 이자가 없다면, 1억으로'],
       {'tiles': [['1,000만원 넘으면', '전부 건보료에', '', 0, 'ink'], ['12개 중 넘는 건', 'JEPQ 하나', '', 184, 'ink']]}),
    sc('손에 남는 돈', ['그래서 손에 남는 건 900만원'],
       {'tiles': [['1,170만원에서 빼면', '900만원', '', 0, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
_c3 = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read().split('## 3.')[1]
assert sum(1 for l in _c3.split(chr(10) + '## ')[0].splitlines() if '분배율' in l and '세전' in l) == 12, '§3 ETF 수가 12가 아님'
for x in ('세전 11,710,000원', '건보 더 냄 952,585원', '1년 통장 9,000,915원', '[연 1,000만원 넘음]', '다른 금융소득 0 가정'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0].split('·')[0].strip()) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
# 배경: de1s_jepi·schdgrow 11/2 밝기 실측(LiveDim 뒤 Y≥52)·눈 검사를 넘은 같은 클립·구간만(얼굴·상표·글자 없음 확인된 것)
# 11/3 렌더 1판: 7118320 1.83초 'No frame found'(합성기) → 6343634 10초~(같은 편 다른 구간, 눈 검사)
# 11/3 렌더 3판: 6343634 12.2초 또 No frame found(남은 메모리 0.7GB) → 6343634·7118320 빼고 이 묶음에서 렌더된 클립만: 5981346 28초~·5546876 9초~
# 11/3 토막 렌더: 5번 줄 8661806 10초~(잘라 낸 파일 1.23·1.37초)에서 토막 6번 연속 No frame found → 6343634 2초~(schdgrow 눈·밝기 통과 구간) · 1번 줄 5981346 28초~가 3번 줄(20~28.6초)과 0.6초 겹쳐 29초~
# 06:5x: cut30/·cuti/ 판은 5981346_29에서 매번 죽고 cut/(원본 fps·GOP 10) 5981346_28은 0-599 통과 → cut/로 돌아가고 1번 줄 28초~(3번 줄 끝과 0.6초 겹침 감수)
BG = [(1, '5981346', 28), (2, '8661806', 2), (3, '5981346', 20), (4, '5546876', 1), (5, '6343634', 2), (6, '5546876', 9)]   # 11/3 2차: 900만원 줄을 끝으로 옮겨 순서만 바꿈
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'detf', 'stock', cid + '.mp4')), cid
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    cut = f'bg/detf/stock/cut/{cid}_{st}.mp4'   # 11/3: 원본 긴 클립 찾기(seek)가 빈 메모리 0.7GB에서 No frame found로 4번+토막 3번 죽음 → 쓰는 구간만 잘라(0초부터 — 2판 cut/ 25fps·GOP 10은 8661806_10, 3판 cut30/ 30fps는 5981346_29·8661806_10에서 또 죽어 4판 cuti/ = 원본 fps·모든 프레임 키프레임·B프레임 0) 읽음, 그림은 같음
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', os.path.join(VID, 'public', 'bg', 'detf', 'stock', cid + '.mp4'), '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-c:v', 'libx264', '-g', '10', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({f"{c} {CRED[c]['author'].strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'de1s_jepqhealth', 'v': 2, 'look': 'live', 'question': ['1억을 배당 ETF JEPQ에', '넣으면 건보료가 붙을까'], 'hot': '건보료',
     'answer': {'label': '1억 JEPQ · 지역가입자 1년', 'items': ['건보료 95만원 더', '손에 남는 돈 900만원'], 'arrow': False, 'note': '건보료 95만원 더'},
     'base': '야후 파이낸스 분배 기록(2026-10-16 마감, 최근 12개월 그대로) · 지역가입자·다른 금융소득 0 가정 · 파이어맵 계산', 'long': 'mkAxQPGaDqc',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'de1s_jepqhealth.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'de1s_jepqhealth: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
