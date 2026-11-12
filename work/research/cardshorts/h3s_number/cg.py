import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.6-flash', 'gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-2.5-flash']
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 3초에 나오는 말(또는 화면 글) 그대로 2) 화면 형식(사람 실사·표·지도·자막 위치 등) 3) 처음 나오는 가격·비율 숫자와 그 시각 4) 그 숫자의 근거(국토부 실거래·호가·뉴스·추정 중 무엇인지, 같은 평수끼리 비교했는지) 5) 단지 번호(1~14단지)별 차이를 다루는지 6) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['ekzRMAmDGOw', 'ZxQojv6zGmM', '2lBAf2zu9Uc', '0GjLmzMjefM', 'bj5paT5OVZ8', 'AReO42P1tiQ']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:900])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
