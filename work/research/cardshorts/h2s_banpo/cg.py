# h2s_banpo 11/20 PD: h2s_jamsil/cg.py 사본, 질문·영상만 바꿈
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.1-flash-lite', 'gemini-flash-lite-latest', 'gemini-3-flash-preview']   # 11/20 07:2x flash 429 → lite
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 3초에 나오는 말(또는 화면 글) 그대로 2) 화면 형식(사람 실사·표·지도·자막 위치 등) 3) 처음 나오는 가격 숫자와 그 시각 4) 그 숫자의 근거(국토부 실거래·호가·뉴스·추정 중 무엇인지, 같은 평수끼리인지, 몇 건인지) 5) 한 건 신고가·급락 거래를 그달 다른 거래와 함께 보여 주는지, 층·날짜를 보여 주는지 6) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['l8xFQKCdiMI', 'F3h5fclbpvA', 'sFHlenpMCsQ', 'sx6UtRS1u-A', 'Y7iu13DXzlU', '77By9luF0gw']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:900])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
