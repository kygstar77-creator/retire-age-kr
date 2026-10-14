# 롱폼 편집 서명 대조(2026-10-14 editor). 근무 시작 때 돌린다.
#   py -3.12 work/research/editor/sigcheck.py
# ep/*/script.md · screen_text.txt 옆 .edit.json의 sha가 지금 파일 해시와 다른 편, 서명이 없는 편을 적는다.
# 요청 줄 없이 바뀐 대본(10/14 P-1)을 렌더·녹음 전에 잡으려는 것. 이미 공개된 편도 같이 나오니 날짜를 보고 판단한다.
import os, glob, json, hashlib, sys

EP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'longform', 'ep')

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def main():
    bad = 0
    for d in sorted(glob.glob(os.path.join(EP, '*'))):
        name = os.path.basename(d)
        for f in ('script.md', 'screen_text.txt'):
            p = os.path.join(d, f)
            if not os.path.exists(p):
                continue
            sj = os.path.join(d, 'screen_text.edit.json') if f == 'screen_text.txt' else p + '.edit.json'
            now = sha(p)
            if not os.path.exists(sj):
                print(f'서명 없음  {name}/{f}  ({now[:12]})'); bad += 1
                continue
            j = json.load(open(sj, encoding='utf-8'))
            old = str(j.get('sha', ''))
            if not old or not now.startswith(old[:16]):
                print(f'서명 다름  {name}/{f}  서명 {old[:12]} {j.get("at", "")} · 지금 {now[:12]}'); bad += 1
    print(f'— 대조 끝, 볼 것 {bad}건')

if __name__ == '__main__':
    main()
