# 제목 → 장르 번호(제미나이 flash, 200편씩 묶음). 결과는 labels.json {영상id: 번호}에 쌓인다(이미 붙은 것은 건너뜀).
#   py -3.12 classify.py <csv 또는 json 목록 파일>   — csv는 id·title 칸, json은 [{id,title}]
import sys, os, json, csv, re, time
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(H, '..', '..', '..')); sys.path.insert(0, WORK)
os.environ.setdefault('CROSSCHECK_BUDGET', '3000')
import crosscheck as cc
GENRES = {
 1: '연예·방송 클립(남의 예능·드라마·방송 장면을 잘라 올림)', 2: '연예인·스타 정보(목록·근황·가족·집)', 3: '사연·가족 드라마(대본·재연·썰, 시댁·부부 갈등)',
 4: '심리·인간관계·인생조언·명언', 5: '건강·노화·병원비·의학', 6: '시니어 생활(실버타운·요양원·노인 일상·노년 지혜)', 7: '죽음·장례·사망 뒤 절차',
 8: '법률·생활 법 상식(상속·이혼·층간소음·계약·소송)', 9: '살림·생활 꿀팁', 10: '이사·전원주택·귀농귀촌', 11: '직업·직장 생활(공무원·대기업·퇴직·재취업)',
 12: '육아·교육·교육비', 13: '지역·여행·나라 비교', 14: '과학·AI·IT·기술', 15: '자동차', 16: '음식·요리·외식 가격', 17: '역사·사건·미스터리·범죄',
 18: '인물 일대기(기업인·연예인·위인의 인생 이야기)', 19: '뉴스·정치·시사 해설', 20: '스포츠', 21: '군대·군사', 22: '운세·사주·관상·띠',
 23: '잡학·상식·퀴즈·순위', 24: '동물·자연', 25: '돈·경제(투자·세금·연금·부동산·월급·물가·기업 실적)', 26: '기타', 27: '외국어 채널(한국어 아님)'}
SYS = '너는 유튜브 영상 제목을 장르로 나누는 분류기다. 제목만 보고 가장 맞는 번호 하나를 고른다. 설명 없이 JSON만 낸다.'
def ask(batch):
    g = '\n'.join(f'{k}: {v}' for k, v in GENRES.items())
    lines = '\n'.join(f'{i}|{t}' for i, t in batch)
    user = f'장르 번호표:\n{g}\n\n규칙: 돈 이야기가 중심이면 25. 남의 방송 화면 클립으로 보이면 1. 연예인 인생 이야기는 18, 연예인 목록·근황은 2.\n\n아래 "영상id|제목"마다 번호를 붙여 {{"영상id": 번호}} JSON 하나로만 답해라.\n\n{lines}'
    kv = cc.load_key('gemini_key.txt')
    model, txt = cc.gemini_chat(kv, SYS, user, prefer='flash')
    m = re.search(r'\{.*\}', txt, re.S)
    return model, json.loads(m.group(0))
if __name__ == '__main__':
    src = sys.argv[1]
    if src.endswith('.csv'): items = [(r['id'], r['title']) for r in csv.DictReader(open(src, encoding='utf-8-sig'))]
    else: items = [(r['id'], r['title']) for r in json.load(open(src, encoding='utf-8'))]
    LP = os.path.join(H, 'labels.json'); lab = json.load(open(LP, encoding='utf-8')) if os.path.exists(LP) else {}
    todo = [(i, t.replace('|', ' ').replace('\n', ' ')[:90]) for i, t in dict(items).items() if i not in lab]
    print('붙일 것', len(todo))
    for k in range(0, len(todo), 150):
        b = todo[k:k+150]
        for tr in range(3):
            try:
                model, d = ask(b); break
            except Exception as e:
                print('재시도', tr, str(e)[:150]); time.sleep(5); d = {}
        for i, _ in b:
            if str(d.get(i, '')).isdigit(): lab[i] = int(d[i])
        json.dump(lab, open(LP, 'w', encoding='utf-8'), ensure_ascii=False)
        print(k, len(b), '붙음', sum(1 for i, _ in b if i in lab), model if d else '')
