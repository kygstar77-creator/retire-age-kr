# 파이프라인 점검 — 우리가 지키는 규칙 중 근거 없는 것과 오래된 것을 뽑는다.
# 사용: python work/audit.py [며칠 지나면 오래된 것으로 볼지=30]
# 내가 스스로 만든 규칙을 내가 검사하는 게 이 도구의 요점이다.
# "무엇을 점검할지"를 고정 목록으로 박아두면 새로 생긴 구멍은 영영 안 보이므로,
# rules.json은 회차가 단계를 새로 알게 될 때마다 늘려야 한다.
import sys, os, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
STALE = int(sys.argv[1]) if len(sys.argv) > 1 else 30
TODAY = datetime.date.today()

R = json.load(open(os.path.join(HERE, 'rules.json'), encoding='utf-8'))
rules = R['rules']
order = {s: i for i, s in enumerate(R['stages'])}

def age(d):
    if not d: return None
    try: return (TODAY - datetime.date(*map(int, d.split('-')))).days
    except Exception: return None

none_src = [r for r in rules if r['src'] == '없음' or r['src'].startswith('없음')]
partial  = [r for r in rules if r not in none_src and ('미확인' in r['src'] or '실패' in r['src'])]
stale    = [r for r in rules if r not in none_src and (age(r['measured']) or 0) > STALE]

print('=== 파이프라인 점검 %s — 규칙 %d개, 단계 %d개\n' % (TODAY, len(rules), len(R['stages'])))

print('[1] 근거 없이 지키고 있는 규칙 %d개 — 재서 채우거나 버려야 한다' % len(none_src))
for r in sorted(none_src, key=lambda r: order.get(r['stage'], 99)):
    print('   %-10s %s' % (r['stage'], r['rule']))
    tail = r['src'][3:].lstrip(' -–') if len(r['src']) > 3 else ''
    if tail: print('   %-10s   %s' % ('', tail))

print('\n[2] 절반만 확인된 규칙 %d개' % len(partial))
for r in sorted(partial, key=lambda r: order.get(r['stage'], 99)):
    print('   %-10s %s' % (r['stage'], r['rule']))
    print('   %-10s   %s' % ('', r['src']))

print('\n[3] %d일 넘게 다시 안 잰 규칙 %d개' % (STALE, len(stale)))
for r in sorted(stale, key=lambda r: -(age(r['measured']) or 0)):
    print('   %-10s %3d일 전 | %s' % (r['stage'], age(r['measured']), r['rule']))
if not stale: print('   없음')

# 단계별로 근거 있는 규칙이 하나도 없으면 그 단계는 통째로 감으로 하고 있는 것이다
print('\n[4] 단계별 근거 상태')
for s in R['stages']:
    mine = [r for r in rules if r['stage'] == s]
    ok = [r for r in mine if r not in none_src and r not in partial]
    mark = '비었음' if not mine else ('전부 근거 없음' if not ok else '%d/%d 근거 있음' % (len(ok), len(mine)))
    print('   %-10s %s' % (s, mark))

print('\n다음 회차가 할 일: [1]에서 한 줄을 골라 실제로 재고, rules.json의 src와 measured를 채운다.')
print('잴 수 없으면 그 규칙을 버리고 rules.json에서 지운다. 근거 없는 규칙을 그대로 두지 않는다.')
