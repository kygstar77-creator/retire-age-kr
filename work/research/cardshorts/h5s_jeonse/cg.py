# h5s_jeonse 11/21 PD: h5s_half/cg.py 사본, 질문·영상만 바꿈
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.1-flash-lite', 'gemini-flash-lite-latest', 'gemini-3-flash-preview']   # 11/20 07:2x flash 429 → lite
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 3초에 나오는 말(또는 화면 글) 그대로 2) 화면 형식(사람 실사·표·지도·자막 위치 등) 3) 처음 나오는 전세가·전세가율 숫자와 그 시각 4) 그 숫자의 근거(국토부 실거래·KB·한국부동산원·호가·추정 중 무엇인지, 어느 지역·평수인지, 몇 건인지) 5) 전세가율을 단지별로 나눠 보여 주는지, 지역 평균 하나인지 6) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['kb4B4GUp6Xw', '9KHmoo5QsT8', '-O-0ijOxtG4', 'xWQTZ2Db9gM', 'J2do1HGTxE0', 'c3f26iRGblA']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:900])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
