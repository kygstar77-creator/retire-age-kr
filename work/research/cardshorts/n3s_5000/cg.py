import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.1-flash-lite', 'gemini-3.1-flash', 'gemini-3-pro-preview', 'gemini-3.1-pro']
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 1초 화면 글과 처음 3초 말 그대로 2) 화면 형식(사람 실사·AI 그림·표·자막 위치: 위/가운데/아래) 3) 연봉 5천(5,000만원)의 월 실수령액을 말하는지, 한다면 얼마 4) 연봉이 전체 직장인 중 몇 번째(상위 몇 %)인지 말하는지, 한다면 출처 5) 몇 년 기준인지 6) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['rx1lPtVjVvc','BgHH7i0953I','UEIxGrEgTSE','jY84ZLYS9IY','jFNr95JRkxU','6oAGHbJgF10','oB-Bi0IRk1c']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:700])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
