# h6s_gangnam 11/26 PD: h6s_before/cg.py 사본, 질문·영상만 바꿈
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.1-flash-lite', 'gemini-flash-lite-latest', 'gemini-3-flash-preview']   # 11/20 07:2x flash 429 → lite
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 3초에 나오는 말(또는 화면 글) 그대로 2) 화면 형식(사람 실사·표·그래프·자막 위치 등) 3) 가격·하락 숫자를 처음 말하는 시각과 그 숫자 4) 숫자의 근거(실거래 신고인지 호가·매물인지, 몇 건인지, 출처 표기 있는지) 5) 한 단지 이야기인지, 여러 단지·지역을 견주는지(몇 곳) 6) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['zp9VRXKOG_A', 'Z_yU2U5qhLM', 'mWYJFXUdB60', '5ZXvfBXwWd4', 'bPiw5zc64AA', 'H8bPBKkhiI4']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:900])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
