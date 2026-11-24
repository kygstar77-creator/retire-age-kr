# k1s_bottom 11/24 PD: k1s_recover/cg.py 사본, 질문·영상만 바꿈 ('바닥·어디까지' 쇼츠)
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.1-flash-lite', 'gemini-flash-lite-latest', 'gemini-3-flash-preview']   # 11/20 07:2x flash 429 → lite
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 3초에 나오는 말(또는 화면 글) 그대로 2) 화면 형식(사람 실사·표·그래프·자막 위치 등) 3) "바닥인가·어디까지 빠지나"에 답을 하는지, 한다면 근거(과거 기록 숫자·차트 지지선·전문가 의견) 4) 과거 급락 기록을 숫자로 세는지(몇 번 중 몇 번 등) 5) 사라·팔라·버텨라 같은 권유가 있는지 6) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['OGM34zYGAVo', 'zv3tmjaXecE', 'illxbT04KvU', 'vyJVL9y-yYM', 'LA25pODuS2g', 'HCX0Tz3ngAw']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:900])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
