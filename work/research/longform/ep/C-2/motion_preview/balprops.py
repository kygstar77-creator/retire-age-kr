# BalancePath 미리보기 재료 — C-2 '28년 통장 잔액' (10/19 벤치마크 지시, quality-gap-1019 ①)
# 숫자는 전부 calc_n1_out.txt(월 200만원 표)에서 뽑는다. 점 = 그해 1월 남은 돈(억), 민수 씨 마지막 점 = 2025년 말.
#   py -3.12 work/research/longform/ep/C-2/motion_preview/balprops.py  → c2_balance.json
import re, json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = pathlib.Path(__file__).parent
TXT = (HERE.parent / 'calc_n1_out.txt').read_text(encoding='utf-8')

def table(start):
    m = re.search(rf'## 월 200만원 · {start}년 1월 시작 → ([^\n]+)\n  해:[^\n]*\n((?:  \d{{4}}:[^\n]*\n)+)', TXT)
    assert m, start
    rows = [re.match(r'  (\d{4}): ([\d.]+) → [^→]+→ (못 꺼냄|[\d.]+)', r).groups() for r in m.group(2).splitlines()]
    return m.group(1), [(int(y), float(a), b) for y, a, b in rows]

hj, jw = table(1998); hm, ms = table(2003)
assert hj.startswith('바닥 2011년') and jw[-1][0] == 2011 and jw[-1][2] == '못 꺼냄'
assert hm.startswith('2025년 말 2.72억원') and ms[-1][0] == 2025 and ms[-1][2] == '2.72'
jv = [a for _, a, _ in jw]                       # 1998~2011 1월
mv = [a for _, a, _ in ms] + [float(ms[-1][2])]   # 2003~2025 1월 + 2025년 말(=2026 자리)
assert jv[0] == 3.00 and jv[4] == 2.51 and jv[5] == 1.60 and jv[-1] == 0.12 and len(jv) == 14
assert mv[0] == 3.00 and len(mv) == 24

FPS = 30
J_AT, J_PER = 24, 28
M_AT, M_PER = J_AT + 13 * J_PER + 70, 17
END = M_AT + 23 * M_PER + 96
props = {
  'scene': {'key': 'bal', 'kind': 'bal', 'title': '같은 3억, 두 사람의 통장', 'sub': None, 'chapter': None,
            'source': 'S&P500 총수익 ^SP500TR · 한국은행 ECOS 연말 환율 · 월 200만원 · 1월에 1년 치 매도 · 정우·민수 씨는 가상 인물',
            'lines': [{'text': '정우 씨 통장은 언제 바닥났을까요?', 'cap': None, 'frames': M_AT - 20},
                      {'text': '같은 돈, 같은 규칙으로 5년 늦게 시작한 민수 씨는 지난해 말에도 2억 7천만원이 남아 있었습니다.', 'cap': None, 'frames': END - (M_AT - 20)}],
            'frames': END, 'data': {}},
  'data': {
    'seed': 'C-2', 'y0': 1998, 'y1': 2026, 'min': 0, 'max': 4,
    'ticks': [[0, '0'], [1, '1억'], [2, '2억'], [3, '3억'], [4, '4억']],
    'xlabels': [[1998, '1998'], [2003, '2003'], [2011, '2011'], [2018, '2018'], [2026, '2025 말']],
    'base': [3, '처음 3억'],
    'people': [
      {'name': '정우 씨', 'color': 'ink', 'start': 1998, 'vals': jv, 'at': J_AT, 'per': J_PER,
       'floor': {'year': 2011, 'text': '2011년 1월 · 1년 치가 안 남음'}},
      {'name': '민수 씨', 'color': 'accent', 'start': 2003, 'vals': mv, 'at': M_AT, 'per': M_PER,
       'end': '2025년 말 2.72억'},
    ],
  },
}
json.dump(props, open(HERE / 'c2_balance.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('c2_balance.json', END, 'frames', round(END / FPS, 1), 's · 정우', jv[0], '→', jv[-1], '· 민수', mv[0], '→', mv[-1])
