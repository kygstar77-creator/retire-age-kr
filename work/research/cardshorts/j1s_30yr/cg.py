import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.6-flash', 'gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-2.5-flash']
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 3초에 나오는 말 그대로 2) 화면 형식(사람 실사·표·자막 위치 등) 3) 종부세 숫자(거주·보유 기간 공제율, 나이 공제율, 80% 한도, 세액 등)가 처음 나오는 시각과 그 숫자 4) 15년을 넘게 살면 공제가 더 늘지 않는다(15년=30년)거나 나이+햇수 합쳐 80% 한도라고 말하는지 5) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['KGmZDNcaA3o', 'bAyV3ghQwRo', 'x76hWnW3-Tc', '_qsFvt0SsFw', 'aoawEq1ADAQ', 'uxh8sh5zz4U']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:700])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
