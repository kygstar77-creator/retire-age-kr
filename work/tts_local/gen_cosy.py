# CosyVoice 2/3 시험(zero-shot, 참고 음성 = 우리 E-1 제미나이 녹음 ref_e1.wav만). .venv/cosy 파이썬으로 실행.
#   work/tts_local/.venv/cosy/Scripts/python work/tts_local/gen_cosy.py 3     # Fun-CosyVoice3-0.5B-2512
#   work/tts_local/.venv/cosy/Scripts/python work/tts_local/gen_cosy.py 2     # CosyVoice2-0.5B
import sys, os, json, time, wave
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.join(HERE, '.venv', 'repos', 'CosyVoice')
sys.path[:0] = [REPO, os.path.join(REPO, 'third_party', 'Matcha-TTS')]
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np, torch
from huggingface_hub import snapshot_download
ver = sys.argv[1]; name = {'2': 'CosyVoice2-0.5B', '3': 'Fun-CosyVoice3-0.5B-2512'}[ver]; tag = {'2': 'cosyvoice2', '3': 'cosyvoice3'}[ver]
md = os.path.join(HERE, 'models', name)
t0 = time.time(); snapshot_download('FunAudioLLM/' + name, local_dir=md); print('모델 받기', round(time.time() - t0), '초')
from cosyvoice.cli.cosyvoice import AutoModel
t0 = time.time(); cv = AutoModel(model_dir=md, fp16=True if '--fp16' in sys.argv else False); load = time.time() - t0
L = json.load(open(os.path.join(HERE, 'lines.json'), encoding='utf-8'))
ref = json.load(open(os.path.join(HERE, 'ref_e1.json'), encoding='utf-8'))['text']
ptext = ('You are a helpful assistant.<|endofprompt|>' + ref) if ver == '3' else ref
pwav = os.path.join(HERE, 'ref_e1.wav')
speed = float(sys.argv[sys.argv.index('--speed') + 1]) if '--speed' in sys.argv else 1.0
out = tag + ('' if speed == 1.0 else f'_s{speed}')
gen = {}
for run, seed in (('run1', 0), ('run2', 1)):
    d = os.path.join(HERE, 'out', out, run); os.makedirs(d, exist_ok=True); torch.manual_seed(seed); np.random.seed(seed)
    t0 = time.time(); audio_sec = 0
    for i, l in enumerate(L):
        parts = [j['tts_speech'] for j in cv.inference_zero_shot(l['kor'], ptext, pwav, stream=False, speed=speed)]
        a = torch.cat(parts, dim=1).squeeze(0).cpu().numpy(); audio_sec += len(a) / cv.sample_rate
        with wave.open(os.path.join(d, f'{i:02d}.wav'), 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(cv.sample_rate); w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())
        print(run, i, round(len(a) / cv.sample_rate, 1), 's', flush=True)
    gen[run] = {'sec': round(time.time() - t0, 1), 'audio_sec': round(audio_sec, 1), 'rtf': round((time.time() - t0) / audio_sec, 2)}
json.dump({'engine': name, 'mode': 'zero-shot, 참고 음성 E-1 우리 제미나이 녹음 2줄(10.3초)', 'speed': speed, 'device': torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu',
           'load_sec': round(load, 1), 'gen': gen}, open(os.path.join(HERE, 'out', out, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(gen)
