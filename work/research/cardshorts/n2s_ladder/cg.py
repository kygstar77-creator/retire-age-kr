import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.1-flash-lite', 'gemini-3.1-flash', 'gemini-3-pro-preview', 'gemini-3.1-pro']
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 3초에 나오는 말(또는 화면 글) 그대로 2) 화면 형식(사람 실사·AI 그림·표·자막 위치) 3) 월급 금액마다 순위나 상위 몇 %를 보여 주는지, 몇 개 금액을 보여 주는지 4) 출처 통계(기관·연도)를 밝히는지, 세전·세후 중 무엇인지 말하는지 5) 통장 실수령으로 바꾸는 법을 알려 주는지 6) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['6n9gbTrYQEQ','mRFVo86Q7Vw','rqcmT5Rv7hA','jxDoMxfylkE','UAayEC8sZcc','y49IIrtI3Ys','4KreJHF_7Pg']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:700])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
