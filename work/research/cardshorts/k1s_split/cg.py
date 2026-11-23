# k1s_split 11/23 PD: k1s_recover/cg.py 사본, 질문·영상만 바꿈
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.1-flash-lite', 'gemini-flash-lite-latest', 'gemini-3-flash-preview']   # 11/20 07:2x flash 429 → lite
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 3초에 나오는 말(또는 화면 글) 그대로 2) 화면 형식(사람 실사·표·그래프·자막 위치 등) 3) 한 번에 사기(거치식) vs 나눠 사기(분할·적립식) 결과 숫자를 처음 말하는 시각과 그 숫자 4) 숫자의 근거(실제 지수 과거 자료인지 가상 예시인지, 어느 지수·기간, 출처 표기) 5) 어느 쪽이 낫다고 결론 내리는지, 아니면 갈린다고 하는지 6) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['o8Osf-aEO20', 'reZ5tG0b6k0', 'pN-aC-MKcaA', 'B7B5OMh0HCY', 'ui4LK9daC8w', 'nG-TLIUCQtA']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:900])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
