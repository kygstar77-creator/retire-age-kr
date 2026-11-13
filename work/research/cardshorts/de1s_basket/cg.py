import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.6-flash', 'gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-2.5-flash']
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 3초에 나오는 말(또는 화면 글) 그대로 2) 화면 형식(사람 실사·표·그래프·자막 위치 등) 3) 처음 나오는 숫자와 그 시각 4) SCHD와 국내 미국배당다우존스 ETF(TIGER·SOL·ACE·KODEX)를 같이 담는 것이 분산이 되는지, 업종(섹터) 비중을 숫자로 비교하는지 5) 숫자의 근거(운용사 자료·추정·뉴스 중 무엇) 6) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['3AklPiXSv8s','zAnTf6ojNck','SaKI_dnddoA','5wcadMDBuqc','mWZHWOOK8J8','UOpHPr3R0kA']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:900])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
