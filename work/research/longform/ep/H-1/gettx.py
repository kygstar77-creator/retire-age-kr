# 경쟁 자막을 받아 raw/tx_<id>.txt로 — 읽고 지운다(남의 저작물이라 커밋 금지, 대본에 옮기지 않는다)
import sys
sys.stdout.reconfigure(encoding='utf-8')
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
for vid in sys.argv[1:]:
    try:
        t = api.fetch(vid, languages=['ko'])
        lines = [f"{int(s.start)//60}:{int(s.start)%60:02d} {s.text}" for s in t]
        open(f'raw/tx_{vid}.txt', 'w', encoding='utf-8').write('\n'.join(lines))
        print(vid, len(lines), '조각')
    except Exception as e:
        print(vid, '실패', type(e).__name__, str(e)[:120])
