# 귀 대신 제미나이로 듣기(약한 근거 — 표에 '제미나이 듣기'로 따로 적는다). 롱폼 앞 240초·쇼츠 전체.
#   py -3.12 listen.py <media 폴더>   → listen.json (이미 들은 것은 건너뜀)
# 묻는 것: 말 밑 음악 유무·크기, 효과음(띠링·휙·딩·뿅 등) 시각과 종류, 목소리가 사람 녹음인지 TTS인지
import os, sys, json, base64, subprocess, urllib.request, time, glob
HERE = os.path.dirname(os.path.abspath(__file__)); M = sys.argv[1]
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))
import imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()
KEY = [l.split('=', 1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt', encoding='utf-8-sig') if l.strip()][0]
MODELS = ['gemini-3.5-flash-lite', 'gemini-3.1-flash-lite']
S = json.load(open(os.path.join(HERE, 'sample.json'), encoding='utf-8'))
OURS = json.load(open(os.path.join(HERE, 'ours.json'), encoding='utf-8'))
out_p = os.path.join(HERE, 'listen.json'); out = json.load(open(out_p, encoding='utf-8')) if os.path.exists(out_p) else {}
PROMPT = ('You are an audio engineer. Listen to this Korean YouTube audio clip. Answer ONLY JSON: '
          '{"music_under_speech": "none|very_quiet|quiet|medium|loud", "music_in_pauses": "none|present", '
          '"sfx": [{"t": seconds, "type": "chime|whoosh|ding|pop|click|swoosh|laugh|other", "note": "short"}], '
          '"voice": "human_recording|synthetic_tts|unsure", "voice_reason": "short", "speakers": number}. '
          'List every distinct sound effect you hear (not music, not speech). If none, sfx=[].')
jobs = [('short', v, os.path.join(M, f'short_{v}.a.m4a')) for _, v in S['short']] + [('long', v, os.path.join(M, f'long_{v}.a.m4a')) for _, v in S['long']]
jobs += [(x['kind'], x['id'], x['path']) for x in OURS]
for kind, vid, src in jobs:
    k = f'{kind}_{vid}'
    if k in out or not os.path.exists(src): continue
    mp3 = os.path.join(M, k + '.listen.mp3')
    subprocess.run([FF, '-y', '-loglevel', 'error', '-i', src, '-t', '240' if kind == 'long' else '180', '-vn', '-ac', '1', '-b:a', '48k', mp3], check=True)
    body = {'contents': [{'parts': [{'inlineData': {'mimeType': 'audio/mp3', 'data': base64.b64encode(open(mp3, 'rb').read()).decode()}}, {'text': PROMPT}]}],
            'generationConfig': {'temperature': 0, 'responseMimeType': 'application/json'}}
    for m in MODELS:
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
                          data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=180))
            txt = r['candidates'][0]['content']['parts'][0]['text']; out[k] = {'model': m, **json.loads(txt)}; break
        except Exception as e:
            print(k, m, 'ERR', str(e)[:150], flush=True); time.sleep(5)
    json.dump(out, open(out_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    if k in out: print(k, out[k].get('model'), out[k].get('voice'), out[k].get('music_under_speech'), len(out[k].get('sfx', [])), flush=True)
    os.remove(mp3); time.sleep(4)
