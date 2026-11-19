import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.6-flash', 'gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-2.5-flash']
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 3초에 나오는 말(또는 화면 글) 그대로 2) 화면 형식(사람 실사·표·그래프·자막 위치 등) 3) 처음 나오는 분배율·배당률 숫자와 그 시각 4) 그 숫자의 근거(최근 12개월 합인지·어느 날 가격 기준·출처) 5) 한두 달 유난히 큰 분배(특별 분배·연말 분배)가 분배율을 부풀린다는 말을 하는지, DIVO를 다루면 무엇을 말하는지 6) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['-ETNsYl3NKo', 'ELBsw2DwRLI', 'Ti-S4luV9wU', '7_EnrxUOTkE', 'vNZ537E5n-k', 'JCBoatiwfyg']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:900])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
