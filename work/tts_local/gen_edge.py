# edge-tts 참고 샘플(약관 근거 없음 — 쓰지 않음). 줄마다 mp3 → 24k wav. py -3.12 work/tts_local/gen_edge.py [목소리]
import sys, os, json, asyncio, subprocess, time
import edge_tts, imageio_ffmpeg
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); V = sys.argv[1] if len(sys.argv) > 1 else 'ko-KR-InJoonNeural'
L = json.load(open(os.path.join(HERE, 'lines.json'), encoding='utf-8'))
async def main():
    t0 = time.time()
    for run in ('run1', 'run2'):
        d = os.path.join(HERE, 'out', 'edge', run); os.makedirs(d, exist_ok=True)
        for i, l in enumerate(L):
            mp3 = os.path.join(d, f'{i:02d}.mp3')
            await edge_tts.Communicate(l['kor'], V).save(mp3)
            subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', mp3, '-ar', '24000', '-ac', '1', os.path.join(d, f'{i:02d}.wav')], check=True); os.remove(mp3)
    json.dump({'engine': 'edge-tts ' + edge_tts.__version__ if hasattr(edge_tts, '__version__') else 'edge-tts', 'voice': V, 'gen_sec_2runs': round(time.time() - t0, 1), 'device': 'Microsoft 온라인 서비스'},
              open(os.path.join(HERE, 'out', 'edge', 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False)
asyncio.run(main())
