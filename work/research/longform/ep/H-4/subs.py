# H-4 경쟁 영상 자막(자동 자막 포함) 받아 raw/subs_<id>.txt로 — 읽기만, 영상 파일은 받지 않는다
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from youtube_transcript_api import YouTubeTranscriptApi
HERE = os.path.dirname(os.path.abspath(__file__))
api = YouTubeTranscriptApi()
for vid in sys.argv[1:]:
    try:
        t = api.fetch(vid, languages=['ko'])
        lines = [f'{int(s.start//60)}:{int(s.start%60):02d} {s.text}' for s in t]
        open(os.path.join(HERE, 'raw', f'subs_{vid}.txt'), 'w', encoding='utf-8').write('\n'.join(lines))
        print(vid, len(lines), '줄')
    except Exception as e: print(vid, '실패', type(e).__name__, str(e)[:120])
