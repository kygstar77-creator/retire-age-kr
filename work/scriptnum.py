# 대본 숫자 기계 대조 — 대본에 나오는 숫자가 전부 사실표에 있는지 본다(RULES 2장, 2026-09-30 루프 2회차).
#   py -3.12 work/scriptnum.py <대본.md> <facts.txt> [더 볼 파일 ...]
# 맞다고 보는 경우: 사실표 숫자를 대본 자릿수로 반올림하면 같다(82 ← 82.08, 13.7 ← 13.74, 13 ← 12.81).
# "끝자리 0" 무시(16.90 = 16.9). 쉼표 무시(1,679 = 1679). 대본의 '숫자 출처' 절(--- 아래)과 (화면: …)은 보지 않는다.
# 판정은 사람이 한다 — "사실표에 없음"으로 나온 숫자는 사실표에 근거를 더하거나 대본에서 뺀다.
import sys, re
from decimal import Decimal, ROUND_HALF_UP
sys.stdout.reconfigure(encoding='utf-8')

NUM = re.compile(r'(?<![\w.])-?\d[\d,]*(?:\.\d+)?')

def nums(text):
    out = []
    for m in NUM.finditer(text):
        s = m.group(0).replace(',', '').lstrip('-')
        try: out.append(Decimal(s))
        except Exception: pass
    return out

def places(d):
    t = d.normalize().as_tuple()
    return max(0, -t.exponent)

def main():
    if len(sys.argv) < 3:
        print(__doc__ or '사용법: scriptnum.py 대본 사실표 [...]'); sys.exit(2)
    script = open(sys.argv[1], encoding='utf-8').read().split('\n---', 1)[0]
    fact_text = '\n'.join(open(p, encoding='utf-8').read() for p in sys.argv[2:])
    facts = set(nums(fact_text))
    bad, total = [], 0
    for ln, line in enumerate(script.splitlines(), 1):
        if not line.lstrip().startswith('-'): continue          # 말하는 문장만(제목·장 이름 빼고)
        body = re.sub(r'\(화면[^)]*\)', ' ', line)
        for m in NUM.finditer(body):
            raw = m.group(0); total += 1
            d = Decimal(raw.replace(',', '').lstrip('-'))
            q = Decimal(1).scaleb(-places(d))
            ok = d in facts or any(f.quantize(q, rounding=ROUND_HALF_UP) == d.normalize().quantize(q) for f in facts)
            if not ok: bad.append((ln, raw, body.strip()[:90]))
    print(f'대본 숫자 {total}개 · 사실표에 없음 {len(bad)}개')
    for ln, raw, ctx in bad: print(f'  {ln}행 {raw} — {ctx}')
    sys.exit(1 if bad else 0)

if __name__ == '__main__': main()
