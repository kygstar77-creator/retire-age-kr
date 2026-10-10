# MeloTTS 한국어(KR) 시험. .venv/melo 파이썬으로 실행.
#   work/tts_local/.venv/melo/Scripts/python work/tts_local/gen_melo.py [--speed 1.0] [--cpu]
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HF_HOME', os.path.join(HERE, 'models', 'hf'))
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(HERE, '.venv', 'mecabko'))   # python-mecab-ko(한국어 형태소)를 따로 둔다 — mecab-python3의 MeCab 폴더와 윈도에서 이름이 겹친다
import torch
from melo.api import TTS
speed = float(sys.argv[sys.argv.index('--speed') + 1]) if '--speed' in sys.argv else 1.0
dev = 'cpu' if '--cpu' in sys.argv else ('cuda' if torch.cuda.is_available() else 'cpu')
t0 = time.time(); m = TTS(language='KR', device=dev); load = time.time() - t0; spk = m.hps.data.spk2id['KR']
L = json.load(open(os.path.join(HERE, 'lines.json'), encoding='utf-8'))
out = 'melo' + ('' if speed == 1.0 else f'_s{speed}') + ('_cpu' if dev == 'cpu' else ''); gen = {}
for run, seed in (('run1', 0), ('run2', 1)):
    d = os.path.join(HERE, 'out', out, run); os.makedirs(d, exist_ok=True); torch.manual_seed(seed)
    t0 = time.time()
    for i, l in enumerate(L): m.tts_to_file(l['kor'], spk, os.path.join(d, f'{i:02d}.wav'), speed=speed, quiet=True)
    gen[run] = round(time.time() - t0, 1); print(run, gen[run], '초', flush=True)
json.dump({'engine': 'MeloTTS KR (myshell-ai/MeloTTS-Korean)', 'speaker': 'KR(유일)', 'speed': speed, 'device': torch.cuda.get_device_name(0) if dev == 'cuda' else 'cpu',
           'load_sec': round(load, 1), 'gen_sec': gen}, open(os.path.join(HERE, 'out', out, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
