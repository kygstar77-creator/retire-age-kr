import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.1-flash-lite', 'gemini-3.1-flash', 'gemini-3-pro-preview', 'gemini-3.1-pro']
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 3초에 나오는 말(또는 화면 글) 그대로 2) 화면 형식(사람 실사·AI 그림·표·자막 위치) 3) 연봉이 오를 때 실수령(통장)이 얼마 느는지를 따지는지, 따진다면 어느 연봉 구간에서 얼마 4) 소득세율 구간(15%·24% 등)을 설명하는지 5) 몇 년 기준 보험료·세액표인지 6) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['OWEOaOC98vs','rx1lPtVjVvc','BgHH7i0953I','UEIxGrEgTSE','jFNr95JRkxU','FskfGfR7zK4','oB-Bi0IRk1c']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:700])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
