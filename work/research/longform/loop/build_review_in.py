# 대본 심사 입력 만들기(사장님 10/02 06:18 "대본과 카피라이팅도 심사에 넣어") — youtube-loop 10-02
#   py -3.12 work/research/longform/loop/build_review_in.py <편> <경쟁id> [<경쟁id> ...]
#   → ep/<편>/review_in_script.md : [우리 대본] + [사실표] + [경쟁 상위 자막](편마다 앞 7,000자)
#   그다음 py -3.12 work/second_opinion.py ep/<편>/review_in_script.md 대본
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); LF = os.path.dirname(HERE)
ep, ids = sys.argv[1], sys.argv[2:]
d = os.path.join(LF, 'ep', ep)
rd = lambda p: open(p, encoding='utf-8').read()
out = ['[우리 대본]\n' + rd(os.path.join(d, 'script.md')), '\n[사실표]\n' + rd(os.path.join(d, 'facts.txt'))[:14000], '\n[경쟁 상위 자막]']
n = 0
for v in ids:
    p = os.path.join(LF, 'breakdown', f'{v}_transcript.txt')
    if not os.path.exists(p) or os.path.getsize(p) < 3000:
        p = os.path.join(LF, 'breakdown', f'{v}_break.md')   # 받아쓰기가 잘리면 쪼개기 분석(타임라인 요약)으로 대신
        if not os.path.exists(p):
            print('자막·분석 없음(빼고 진행):', v); continue
        print('자막 대신 쪼개기 분석:', v)
    out.append(f'\n--- 경쟁 {v} ---\n' + rd(p)[:7000]); n += 1
open(os.path.join(d, 'review_in_script.md'), 'w', encoding='utf-8').write('\n'.join(out))
print(ep, '경쟁 자막', n, '편 →', os.path.join(d, 'review_in_script.md'))
