# 숏폼 대본은 Gemini가 쓴다 — 내(클로드) 한국어 문구가 어색하다는 사장님 판단(2026-09-23). 나는 숫자(facts)만 넘긴다.
#   py -3.12 work/shortscript.py <facts.txt 또는 사실 요약 파일> "<주제 한 줄>" <출력.json>
# Gemini에게 주는 규칙: 말하듯이, 짧게, 숫자는 그대로, 과장·권유·예측 없음. 결과는 shorts.py가 읽는 JSON.
import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crosscheck as cc

SYSTEM = '너는 한국 유튜브 쇼츠·릴스 대본을 쓰는 사람이다. 한국 사람이 실제로 말하는 문장으로 쓴다. 번역투, 보고서투, "~일까", "~해보자", "정리하면" 같은 표현을 쓰지 않는다.'
PROMPT = '''아래 [숫자]만 가지고 45~60초 세로 영상(쇼츠) 대본을 JSON으로 써 줘. 주제: {topic}

규칙
- 장면 4~5개. 첫 장면 3초 안에 "이걸 왜 봐야 하는지"가 숫자로 나와야 한다.
- head: 화면에 크게 박힐 한 줄(공백 포함 22자 이내). 숫자가 반드시 들어간다.
- label: head 위에 붙는 작은 글(15자 이내, 없으면 빈 문자열).
- lines: 화면에 작게 붙는 줄 1~3개, 각 24자 이내.
- say: 그 장면에서 읽어 줄 말. 말하듯이 자연스럽게. head/lines를 그대로 읽지 말고 사람이 설명하듯 풀어서. 한 장면 40~60자.
- 마지막 outro: 한 줄. 출처를 밝히되 딱딱하지 않게.
- [숫자]에 없는 수치·주장·전망·추천은 절대 넣지 마. 과장 표현("충격", "역대급", "대박") 금지. 물음표로 끝내는 문장 금지.

형식(이 구조 그대로, 다른 키 추가 금지):
{{"title": "...", "scenes": [{{"label": "...", "head": "...", "lines": ["...", "..."], "say": "..."}}], "outro": "..."}}

[숫자]
{facts}'''

def main():
    facts = open(sys.argv[1], encoding='utf-8').read()[:12000]
    topic = sys.argv[2]; out = sys.argv[3]
    gm = cc.load_key('gemini_key.txt')
    if not gm: print('Gemini 키 없음 — 대본을 쓰지 않는다(내가 대신 쓰지 않음)'); sys.exit(3)
    model, txt = cc.gemini_chat(gm, SYSTEM, PROMPT.format(topic=topic, facts=facts), prefer='pro')
    m = re.search(r'\{.*\}', txt, re.S)
    if not m: print('JSON을 못 찾음:', txt[:300]); sys.exit(1)
    data = json.loads(m.group(0))
    json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{model} 대본 → {out}')
    for s in data['scenes']: print(' ·', s.get('head'), '|', s.get('say'))
    print(' outro:', data.get('outro'))

if __name__ == '__main__': main()
