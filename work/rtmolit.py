# 국토부 실거래 수집 — 공공데이터포털 키(Documents\datago_key.txt). 대기열 2번(2026-09-23).
#   python work/rtmolit.py 202607 202609            → 서울 25개 구 매매·전월세 전부 work/research/rt/<구코드>_<월>_{trade,rent}.json
#   python work/rtmolit.py 202608 202608 11440      → 마포구만
# 시군구 코드는 VWorld에서 받은 work/research/seoul_sgg.json(25개). 하루 트래픽 10,000회라 페이지 1,000행씩.
import sys, os, re, json, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'research', 'rt'); os.makedirs(OUT, exist_ok=True)
KEY = [l.split('=', 1)[1].strip() for l in open(r'C:\Users\강영준\Documents\datago_key.txt', encoding='utf-8-sig') if l.startswith('KEY=')][0]
EP = {'trade': 'RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev', 'rent': 'RTMSDataSvcAptRent/getRTMSDataSvcAptRent'}

def fetch(kind, lawd, ym):
    rows, page = [], 1
    while True:
        u = f'https://apis.data.go.kr/1613000/{EP[kind]}?serviceKey={KEY}&LAWD_CD={lawd}&DEAL_YMD={ym}&numOfRows=1000&pageNo={page}'
        for attempt in range(3):
            try: s = urllib.request.urlopen(u, timeout=60).read().decode('utf-8', 'ignore'); break
            except Exception as e: s = ''; time.sleep(2)
        if not s: raise RuntimeError('응답 없음')
        root = ET.fromstring(s)
        code = root.findtext('.//resultCode');
        if code not in ('000', '00'): raise RuntimeError(root.findtext('.//resultMsg'))
        total = int(root.findtext('.//totalCount') or 0)
        for it in root.iter('item'):
            rows.append({c.tag: (c.text or '').strip() for c in it})
        if len(rows) >= total or not list(root.iter('item')): break
        page += 1
    return rows

def num(s): return int(re.sub(r'[^\d]', '', s or '0') or 0)

if __name__ == '__main__':
    ym0, ym1 = sys.argv[1], sys.argv[2]; only = sys.argv[3:]
    sgg = json.load(open(os.path.join(HERE, 'research', 'seoul_sgg.json'), encoding='utf-8'))
    months = []; y, m = int(ym0[:4]), int(ym0[4:])
    while f'{y}{m:02d}' <= ym1: months.append(f'{y}{m:02d}'); m += 1; (y, m) = (y + 1, 1) if m > 12 else (y, m)
    calls = 0; t0 = time.time()
    for lawd, name in sgg.items():
        if only and lawd not in only: continue
        for ym in months:
            for kind in ('trade', 'rent'):
                p = os.path.join(OUT, f'{lawd}_{ym}_{kind}.json')
                if os.path.exists(p) and ym < time.strftime('%Y%m'): continue   # 지난달 이전은 다시 안 받음
                try:
                    rows = fetch(kind, lawd, ym); calls += 1
                    json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
                    print(f'{name} {ym} {kind} {len(rows)}건', flush=True)
                except Exception as e: print(f'{name} {ym} {kind} 실패: {e}', flush=True)
                time.sleep(0.3)
    print(f'완료: 호출 {calls}회, {int(time.time()-t0)}초')
