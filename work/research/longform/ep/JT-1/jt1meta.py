# JT-1 meta.json 설명·챕터 채우기 — jt1.json(장면 시각)·voice.json·bg_used.json(실사 출처) → meta.json desc·chapters·voice·missing + desc_1117.txt(editor 설명란 서명용)
#   py -3.12 work/research/longform/ep/JT-1/jt1meta.py   (jt1props_pd.py 다음에, 녹음·말이 바뀌면 다시)
# 11/17 14시대 PD(정기 14:1x): N-3 n3meta.py 꼴. 제목·썸네일·설명 첫 두 줄·출처는 meta.json desc_tpl(copywriter·youtube-loop 11/16 판) 그대로 —
#   바꾼 것: {CHAPTERS} 채움(장 카드 시작 프레임) · {CAFE}는 짝 글 전이라 카페 대문 · 카페 줄 아래 사이트 줄(ytlong C9 11/11 — firemap.kr 주택연금 안내 글,
#   200 확인 11/17) · '영상 일부' 줄은 bg_used.json 12개로 다시(템플릿 4줄은 11/16 PD 실사 8개를 빠뜨림).
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', 'video'))
P = json.load(open(os.path.join(VID, 'jt1.json'), encoding='utf-8'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
MP = os.path.join(EP, 'meta.json')
m = json.load(open(MP, encoding='utf-8'))
heads = list(m['chapter_titles'])                     # 예고 + 1~7장 (script.md ## 제목과 같음)
starts, a = [0], 0
for s in P['scenes']:
    if s['kind'] == 'ask' and re.match(r'^\d+장$', (s.get('data') or {}).get('n', '')): starts.append(a)
    a += s['frames']
assert len(starts) == len(heads) == 8, (len(starts), len(heads))
fps = P.get('fps', 30)
fmt = lambda f: f"{int(f / fps) // 60}:{int(f / fps) % 60:02d}"
chapters = [[round(st / fps), h] for st, h in zip(starts, heads)]
assert all(b[0] - a_[0] >= 10 for a_, b in zip(chapters, chapters[1:])), chapters
CH = '\n'.join(f"{fmt(st)} {h}" for st, h in zip(starts, heads))
SITE = '주택연금 가입 조건·장단점 정리(파이어맵): https://firemap.kr/guide/housing-pension-reverse-mortgage?utm_source=youtube&utm_medium=description&utm_campaign=jt-1'
tpl = m['desc_tpl']
if 'firemap.kr' not in tpl:
    tpl = tpl.replace('전체 표와 계산 근거(카페): {CAFE}\n', '전체 표와 계산 근거(카페): {CAFE}\n' + SITE + '\n', 1)
credits = [c['desc_line'] for c in json.load(open(os.path.join(EP, 'bg_used.json'), encoding='utf-8'))]
tpl = '\n'.join(l for l in tpl.splitlines() if not l.startswith('영상 일부:')) + '\n' + '\n'.join(dict.fromkeys(credits))
cafe = m.get('cafe_url') or 'https://cafe.naver.com/firemap'
desc = tpl.replace('{CAFE}', cafe).replace('{CHAPTERS}', CH)
m.update({'desc_tpl': tpl, 'desc': desc, 'chapters': chapters,
          'voice': f"Chirp 3 HD Charon {V['speakingRate']} · {V['done']}줄 · {V['seconds']}초 · 11/17 PD 1:4·2:8·4:6 다시 받음(readback)",
          'missing': V['missing'], 'chapters_note': f'jt1.json 장 카드 시작 프레임(11/17 PD jt1meta.py) — 렌더본 길이 {round(a / fps, 1)}초'})
json.dump(m, open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
open(os.path.join(EP, 'desc_1117.txt'), 'w', encoding='utf-8').write(m['title'] + '\n\n' + desc + '\n')
print(CH); print(f'설명 {len(desc)}자 · 출처 줄 {desc.count("Pexels")}개 Pexels · missing {V["missing"]}')
