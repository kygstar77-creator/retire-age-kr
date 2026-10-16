# 설명란 '권유 아님' 줄 검사 (firemap-video-producer 2026-10-14, 회의 10/14 21:43 지시 — 영상 끝 줄 면책(A23)을 뺀 대신 설명란 면책이 빠지지 않게)
#   py -3.12 work/disclaim.py <upload.json 또는 meta.json>...   # 줄 찾기만
# 통과 = 한 줄 안에 '권유|사거나|팔라|사라는|넣으라|받으라' 하나 + (10/16 엄격화) ('권유'·'팔라는'·'~라는 말'·'~라는 뜻') + ('아닙니다'·'아니'·'아님') — 10/14 공개·예약 설명 23편에서 쓰인 꼴 그대로.
import re, sys, json

PAT = re.compile(r'(권유|팔라는|라는 말|라는 뜻)[^\n]{0,30}?(아닙니다|아니|아님)')
# 10/16 감사(21:16)·회의 받아들임: '…아니라는 뜻입니다'처럼 무엇을 권하지 않는지 없는 줄도 통과하던 것 막음 — 같은 줄에 권유 낱말 필수
ACT = re.compile(r'권유|사거나|팔라|사라는|넣으라|받으라')
NEED = "설명란에 '권유 아님' 줄 없음 — 예: '지나간 값이고, 투자 권유가 아닙니다.' / '특정 상품을 사거나 팔라는 뜻이 아닙니다.'"


def line(desc):
    for l in (desc or '').splitlines():
        if PAT.search(l) and ACT.search(l): return l.strip()
    return None


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    for p in sys.argv[1:]:
        d = json.load(open(p, encoding='utf-8'))
        l = line(d.get('description') or d.get('desc'))
        print(p, '|', l or '★ ' + NEED)
