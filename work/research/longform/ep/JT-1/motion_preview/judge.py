# JT-1 SumRace — 제미나이 심사(2026-11-16 motion, N-3 judge.py 틀). ask()는 G-1 judge_asym.py 재사용. 판 board_<k>.png
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); G = os.path.abspath(os.path.join(H, '..', '..', 'G-1', 'motion_preview'))
sys.path.insert(0, G)
exec(open(os.path.join(G, 'judge_asym.py'), encoding='utf-8').read().split('\nQ = ')[0])
D = {
 'race': "'늦게 들면 몇 살에 같아지나' 앞 3줄. 가로 = 나이 65~95세, 세로 = 그 나이까지 받은 돈 합(2억·4억 눈금). 나이 바늘이 걸으며 두 선: 65세에 든 쪽(먹 실선, 월 126.4만원)은 바로 오르고, 70세에 든 쪽(회색 점선, 월 153.9만원)은 70세까지 0에 누워 있다가 더 가파르게 오름. 70세 자리 세로 괄호 '못 받은 7,584만원' → 만남 자리 '?' → 70세~만남 가로 괄호 '23년' → 손 동그라미 + 주황 '93세'.",
 'gap': "같은 장 뒤 6줄. 앞 그림에서 70세에 든 쪽 선을 빼서 바닥 점선으로 눕힘(움직이며 바뀜) → 두 선 사이 틈이 언덕(65세에 든 쪽이 더 받은 돈)이 됨: 70세 꼭대기 7,584만원, 말 따라 80세 4,284만원·85세 2,634만원·90세 984만원 점·기둥이 차례로 주황(그 나이부터 93세까지 남은 앞섬 면을 연주황으로), 93세에서 바닥선과 만남(손 동그라미), 마지막 줄에 93세 뒤 세로 띠 연주황 '이 뒤로는 70세 쪽이 더'. 말은 '4,300만원·2,600만원·1,000만원 정도'로 반올림, 화면은 계산 원값.",
}
Q0 = open(os.path.join(H, 'judge_q.txt'), encoding='utf-8').read()
keys = sys.argv[1:] or list(D)
with open(os.path.join(H, 'gemini_jt1.md'), 'a', encoding='utf-8') as fo:
    for k in keys:
        m, out = ask(Q0.replace('{DESC}', D[k]), [os.path.join(H, f'board_{k}.png')])
        fo.write('\n## %s (%s)\n%s\n' % (k, m, out)); print('==', k, m); print(out)
