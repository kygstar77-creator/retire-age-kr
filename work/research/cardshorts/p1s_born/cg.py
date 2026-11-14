import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.1-flash-lite', 'gemini-3.1-flash', 'gemini-3-pro-preview', 'gemini-3.1-pro']
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 3초에 나오는 말(또는 화면 글) 그대로 2) 화면 형식(사람 실사·AI 그림·표·자막 위치) 3) 출생연도별 받는 나이를 보여 주는지, 어떤 모양(표·계단·말)으로 몇 초에 4) 68세 이야기를 하는지, 하면 확정처럼 말하는지 제안이라고 말하는지 5) 1968년 12월 31일생과 1969년 1월 1일생처럼 하루 차이 예를 드는지 6) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['23NmJrC6qtA','qYdn-bOofmM','iw8BgyF-waE','AIM23jDEIqY','r93Cxdza9dI','RrTvl5-qySU','yGlcaHrqR7w']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:700])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
