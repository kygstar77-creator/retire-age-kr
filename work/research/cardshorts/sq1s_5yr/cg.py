# sq1s_5yr 11/28 PD: h6s_before/cg.py 사본, 질문·영상만 바꿈
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.argv = ['ytbreak']   # ytbreak 본체 loop 안 돌게
import importlib.util
spec = importlib.util.spec_from_file_location('ytb', r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\ytbreak.py'); ytb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytb)
ytb.MODELS = ['gemini-3.1-flash-lite', 'gemini-flash-lite-latest', 'gemini-3-flash-preview']   # 11/20 07:2x flash 429 → lite
P = '이 쇼츠를 보고 한국어로 짧게 답하세요. 1) 처음 3초에 나오는 말(또는 화면 글) 그대로 2) 화면 형식(사람 실사·표·그래프·자막 위치 등) 3) 수익·금액 숫자를 처음 말하는 시각과 그 숫자 4) 숫자의 근거(기간·시작일·배당 재투자 여부·원화/달러·세금 반영·출처 표기) 5) 두 상품을 섞는(비율) 이야기가 나오는지 6) 사라·팔라 같은 권유 말이 있는지 7) 마지막 문장 그대로. 모르면 모른다고.'
IDS = ['G_vh1FDk5hA', 'mE7rSyTsUlI', 'zAnTf6ojNck', 'IaKsR-rixfM', 'BW1GUmC_56w', 'mBHoI5ZCbKs']
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compete_gemini.json')
out = json.load(open(fn, encoding='utf-8')) if os.path.exists(fn) else {}
for v in IDS:
    if v in out: continue
    m, t = ytb.ask(v, P, 3000)
    if t: out[v] = [m, t]; print('##', v, m, '\n', t[:900])
    json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
